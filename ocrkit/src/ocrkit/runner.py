"""Read pages with one model on the GPU (vLLM), writing each page's output as soon as its batch finishes.

    python -m ocrkit.runner --manifest work/manifest.json --model ATH-MaaS/OvisOCR2 --edge 1600 --out /content/drive/MyDrive/ocr/x

Speed: pages are fetched (from their URL or the bundle) and rendered in background threads while the GPU
works on the previous batch, so the GPU does not wait for the CPU. Robustness: a batch that fails is retried
page by page; a page that fails alone gets <page>.err and is not retried; pages already written are skipped,
so a run that is cut off resumes. Progress goes to <out>/<slug>/_progress.json.
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import queue
import tarfile
import threading
import time
import urllib.request
from pathlib import Path

from .manifest import sha256
from .models import slug, spec


class Sources:
    """Gets a file's PDF on the GPU machine: from the bundle (extracted once) or by downloading its URL."""

    def __init__(self, manifest: dict, workdir: Path):
        self.m, self.dir = manifest, workdir
        self.dir.mkdir(parents=True, exist_ok=True)
        self.lock = threading.Lock()
        self.parts_done: set[str] = set()

    def _part(self, name: str):
        with self.lock:
            if name in self.parts_done or (self.dir / f"{name}.done").exists():
                self.parts_done.add(name)
                return
            base = self.m.get("parts_base")
            src = f"{base.rstrip('/')}/{name}" if base else str(self.dir / name)
            tmp = self.dir / f"{name}.download"
            if src.startswith("http"):
                urllib.request.urlretrieve(src, tmp)
            else:
                tmp = Path(src)
            with tarfile.open(tmp) as tar:
                tar.extractall(self.dir)
            (self.dir / f"{name}.done").touch()
            self.parts_done.add(name)

    def pdf(self, f: dict) -> tuple[Path, list[int] | None]:
        """(path, page index map) for a file: bundled PDFs hold only the listed pages, in order."""
        if f.get("part"):
            self._part(f["part"])
            return self.dir / "pages" / f"{f['id']}.pdf", list(range(len(f["pages"])))
        dst = self.dir / "src" / f"{f['id']}.pdf"
        if not dst.exists():
            dst.parent.mkdir(exist_ok=True)
            tmp = dst.with_suffix(".part")
            for attempt in range(4):
                try:
                    req = urllib.request.Request(f["url"], headers={"User-Agent": "Mozilla/5.0 ocrkit"})
                    with urllib.request.urlopen(req, timeout=120) as r, tmp.open("wb") as w:
                        w.write(r.read())
                    break
                except Exception:
                    time.sleep(5 * (attempt + 1))
            if f.get("sha256") and tmp.exists() and sha256(tmp) != f["sha256"]:
                raise RuntimeError(f"{f['url']}: file changed since the manifest was made")
            tmp.replace(dst)
        return dst, [p - 1 for p in f["pages"]]


def render(pdf: Path, index: int, edge: int):
    import pymupdf
    from PIL import Image

    with pymupdf.open(pdf) as doc:
        page = doc[index]
        zoom = edge / max(page.rect.width, page.rect.height)
        pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), alpha=False)
        return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--edge", type=int, default=1600, help="page image size (long edge, pixels)")
    ap.add_argument("--out", required=True, help="cache root: <out>/<slug>/<file id>/<page>.txt")
    ap.add_argument("--work", default="/content/ocrkit_work", help="where sources are fetched / extracted")
    ap.add_argument("--only", help="JSON list of file ids")
    ap.add_argument("--bench", action="store_true", help="only the bake-off sample")
    ap.add_argument("--batch", type=int, default=48)
    ap.add_argument("--gpu-mem", type=float, default=0.88)
    ap.add_argument("--dtype", default="auto")
    ap.add_argument("--model-impl", default=None)
    args = ap.parse_args()

    from vllm import LLM, SamplingParams

    man = json.loads(Path(args.manifest).read_text())
    files = man["files"]
    if args.bench:
        files = [f for f in files if f.get("bench")]
    if args.only:
        keep = set(json.loads(Path(args.only).read_text()))
        files = [f for f in files if f["id"] in keep]
    files.sort(key=lambda f: f.get("order", 0))
    out = Path(args.out) / slug(args.model, args.edge)
    todo = [(f, k, p) for f in files for k, p in enumerate(f["pages"])
            if not (out / f["id"] / f"{p:04d}.txt").exists() and not (out / f["id"] / f"{p:04d}.err").exists()]
    total = sum(len(f["pages"]) for f in files)
    print(f"{args.model} @{args.edge}: {total - len(todo)} of {total} pages done, {len(todo)} to go", flush=True)
    if not todo:
        return

    s = spec(args.model)
    engine = {"max_model_len": s["max_model_len"]} | s["engine"] | ({"model_impl": args.model_impl} if args.model_impl else {})
    llm = LLM(model=s["hf"], trust_remote_code=True, limit_mm_per_prompt={"image": 1}, gpu_memory_utilization=args.gpu_mem,
              dtype=args.dtype, **engine)
    params = SamplingParams(temperature=0.0, max_tokens=s["max_tokens"])
    src = Sources(man, Path(args.work))

    # producer: fetch + render ahead of the GPU, a few batches deep
    q: queue.Queue = queue.Queue(maxsize=3)
    pool = cf.ThreadPoolExecutor(max_workers=8)

    def load(item):
        f, k, p = item
        try:
            path, index = src.pdf(f)
            return item, render(path, index[k], args.edge)
        except Exception as e:
            return item, e

    def producer():
        for i in range(0, len(todo), args.batch):
            q.put(list(pool.map(load, todo[i:i + args.batch])))
        q.put(None)

    threading.Thread(target=producer, daemon=True).start()
    t0, done = time.time(), 0
    while (batch := q.get()) is not None:
        ok = [(item, img) for item, img in batch if not isinstance(img, Exception)]
        msgs = [[{"role": "user", "content": [{"type": "image_pil", "image_pil": img}, {"type": "text", "text": s["prompt"]}]}] for _, img in ok]
        try:
            texts = [o.outputs[0].text for o in llm.chat(msgs, params, use_tqdm=False)] if msgs else []
        except Exception as e:      # one bad page must not stop the run: retry the batch page by page
            print(f"  batch failed ({type(e).__name__}: {e}); retrying page by page", flush=True)
            texts = []
            for m in msgs:
                try:
                    texts.append(llm.chat([m], params, use_tqdm=False)[0].outputs[0].text)
                except Exception as e2:
                    texts.append(e2)
        results = [(item, t) for (item, _), t in zip(ok, texts)] + [(item, img) for item, img in batch if isinstance(img, Exception)]
        for (f, k, p), text in results:
            path = out / f["id"] / f"{p:04d}.txt"
            path.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(text, Exception):
                path.with_suffix(".err").write_text(f"{type(text).__name__}: {text}", encoding="utf-8")
                continue
            tmp = path.with_suffix(".part")
            tmp.write_text(text, encoding="utf-8")
            tmp.replace(path)
        done += len(batch)
        rate = (time.time() - t0) / done
        (out / "_progress.json").write_text(json.dumps({"done": total - len(todo) + done, "total": total,
                                                        "s_per_page": round(rate, 3), "time": time.time()}))
        print(f"  {done}/{len(todo)} pages, {rate:.2f} s/page, about {rate * (len(todo) - done) / 3600:.1f} h left", flush=True)


if __name__ == "__main__":
    main()
