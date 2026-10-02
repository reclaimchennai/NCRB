"""Read NCRB's scanned table pages with a document OCR model on a cloud GPU (vLLM).

Runs on Google Colab (or any CUDA machine). Input is the `ocr-pages` release:
manifest.json plus tars of one PDF per source file holding only its scanned
pages. Output is the page cache the pipeline already reads,

    <out>/<model slug>/<first 16 hex of the source file's SHA-256>/<page:04d>.txt

holding the model's raw text for that page, so the folder can be copied into
data/ocr_cache/ on the laptop (python -m ncrb.vlm_import) and extraction weighs
it against every other reading by the totals check. Finished pages are skipped,
so a run that is cut off (Colab sessions end) picks up where it stopped.

    python colab/ocr_pages.py --model XingChen-AGI/TeleOCR --bench
    python colab/ocr_pages.py --model XingChen-AGI/TeleOCR
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
from ncrb.vlm import MODELS  # noqa: E402  (prompts per model, shared with the laptop runner)
from ncrb.vlm_tables import model_slug  # noqa: E402

# vLLM settings per model, from each model's card / vLLM recipe
ENGINE = {
    "PaddlePaddle/PaddleOCR-VL-1.6": dict(enable_prefix_caching=False, mm_processor_cache_gb=0, max_num_batched_tokens=16384),
}


def render(pdf, index: int, long_edge: int):
    import pymupdf as fitz
    from PIL import Image

    page = pdf[index]
    zoom = long_edge / max(page.rect.width, page.rect.height)
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--model", required=True)
    ap.add_argument("--bundle", default="/content/ocr_pages", help="folder with manifest.json and pages/")
    ap.add_argument("--out", default="/content/drive/MyDrive/ncrb_ocr/ocr_cache")
    ap.add_argument("--bench", action="store_true", help="only the bake-off sample")
    ap.add_argument("--long-edge", type=int, default=1600, help="page image size in pixels (the laptop runs use 1600)")
    ap.add_argument("--batch", type=int, default=48)
    ap.add_argument("--max-tokens", type=int, default=None)
    ap.add_argument("--gpu-mem", type=float, default=0.88)
    ap.add_argument("--dtype", default="auto", help="'half' on a T4, which has no bfloat16")
    args = ap.parse_args()

    import pymupdf as fitz
    from vllm import LLM, SamplingParams

    bundle = Path(args.bundle)
    files = json.loads((bundle / "manifest.json").read_text())["files"]
    if args.bench:
        files = [f for f in files if f.get("bench")]
    files.sort(key=lambda f: f["order"])
    out = Path(args.out) / model_slug(args.model)
    todo = [(f, k, p) for f in files for k, p in enumerate(f["pages"]) if not (out / f["sha16"] / f"{p:04d}.txt").exists()]
    total = sum(len(f["pages"]) for f in files)
    print(f"{args.model}: {total - len(todo)} of {total} pages done, {len(todo)} to go", flush=True)
    if not todo:
        return

    prompt, max_tokens = MODELS.get(args.model, ("Table Recognition:", 8192))
    llm = LLM(model=args.model, trust_remote_code=True, max_model_len=16384, limit_mm_per_prompt={"image": 1},
              gpu_memory_utilization=args.gpu_mem, dtype=args.dtype, **ENGINE.get(args.model, {}))
    params = SamplingParams(temperature=0.0, max_tokens=args.max_tokens or max_tokens)

    t0, done, open_pdfs = time.time(), 0, {}
    for i in range(0, len(todo), args.batch):
        chunk = todo[i : i + args.batch]
        msgs = []
        for f, k, p in chunk:
            pdf = open_pdfs.get(f["sha16"]) or open_pdfs.setdefault(f["sha16"], fitz.open(bundle / "pages" / f"{f['sha16']}.pdf"))
            img = render(pdf, k, args.long_edge)
            msgs.append([{"role": "user", "content": [{"type": "image_pil", "image_pil": img}, {"type": "text", "text": prompt}]}])
        outs = llm.chat(msgs, params, use_tqdm=False)
        for (f, k, p), o in zip(chunk, outs):
            path = out / f["sha16"] / f"{p:04d}.txt"
            path.parent.mkdir(parents=True, exist_ok=True)
            tmp = path.with_suffix(".part")
            tmp.write_text(o.outputs[0].text, encoding="utf-8")
            tmp.replace(path)
        done += len(chunk)
        if len(open_pdfs) > 64:
            for d in open_pdfs.values():
                d.close()
            open_pdfs = {}
        rate = (time.time() - t0) / done
        print(f"  {done}/{len(todo)} pages, {rate:.2f} s/page, about {rate * (len(todo) - done) / 3600:.1f} h left", flush=True)


if __name__ == "__main__":
    main()
