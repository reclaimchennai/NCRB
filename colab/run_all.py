"""The whole cloud OCR job, unattended: pages, bake-off, winner, full run, result zip.

Started in the background on the Colab VM (colab/NCRB_OCR.ipynb, or by an agent
through the Colab MCP server) so that no notebook cell has to stay attached:

    nohup python colab/run_all.py > /content/run_all.log 2>&1 &

Everything it makes lives on Google Drive under --root, so a VM that is reset
picks up where the last one stopped (pages already read are skipped):

    <root>/status.json            phase, progress, winner, errors (the monitor cell reads this)
    <root>/bench/<edge>/<model>/  bake-off readings
    <root>/ocr_cache/<model>/     the full run (the layout data/ocr_cache uses)
    <root>/<model>.zip            the result to import on the laptop

Guards against wasting compute units: each bake-off model has a time limit and
is skipped if it fails; the full run is restarted when it crashes or stops
making progress (at most --restarts times) and stopped at --hours. The monitor
cell releases the GPU (runtime.unassign) as soon as status says finished.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import signal
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
from ncrb.vlm_tables import model_slug, score_tables, tables_from_texts  # noqa: E402

REL = "https://github.com/reclaimchennai/NCRB/releases/download/ocr-pages"
# whole-page models, best first on OmniDocBench v1.6 (Oct 2026); the bake-off on NCRB's own scans decides.
# TeleOCR (top of that table) is left out: it reads one cropped region at a time behind a separate layout step,
# and vLLM's Qwen2 code ignores its head_dim (AssertionError in get_rope), see colab/README.md
CANDIDATES = ["ATH-MaaS/OvisOCR2", "PaddlePaddle/PaddleOCR-VL-1.6", "zai-org/GLM-OCR"]


def gpu_used_mib() -> int:
    try:
        return int(subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
                                  capture_output=True, text=True, timeout=15).stdout.strip().split("\n")[0])
    except Exception:
        return 0


def free_gpu(wait_s=90) -> int:
    """Kill vLLM processes left over from an interrupted run (an orphaned EngineCore keeps its memory and makes the
    next start fail), then wait for the memory to come back. The notebook kernel is not touched. Returns MiB still used."""
    try:
        pids = subprocess.run(["nvidia-smi", "--query-compute-apps=pid", "--format=csv,noheader"],
                              capture_output=True, text=True, timeout=15).stdout.split()
    except Exception:
        pids = []
    for pid in pids:
        try:
            args = subprocess.run(["ps", "-p", pid, "-o", "args="], capture_output=True, text=True).stdout
            if any(w in args.lower() for w in ("vllm", "enginecore", "ocr_pages")):
                os.kill(int(pid), signal.SIGKILL)
        except Exception:
            pass
    t = time.time()
    while gpu_used_mib() > 1500 and time.time() - t < wait_s:
        time.sleep(3)
    return gpu_used_mib()


class Job:
    def __init__(self, a):
        self.a = a
        self.root = Path(a.root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.status_path = self.root / "status.json"
        self.status = json.loads(self.status_path.read_text()) if self.status_path.exists() else {}
        self.status.setdefault("started", time.time())
        self.status["vm_started"] = time.time()
        self.t0 = self.status["started"]

    def save(self, **kw):
        self.status.update(kw, updated=time.time())
        tmp = self.status_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.status, indent=1))
        tmp.replace(self.status_path)
        print(time.strftime("%H:%M:%S"), json.dumps(kw)[:300], flush=True)

    def over_time(self) -> bool:
        return (time.time() - self.t0) / 3600 > self.a.hours

    # ------------------------------------------------------------- pages
    def pages(self):
        b = Path(self.a.bundle)
        b.mkdir(parents=True, exist_ok=True)
        man = b / "manifest.json"
        if not man.exists():
            urllib.request.urlretrieve(f"{REL}/manifest.json", man)
        parts = json.loads(man.read_text())["parts"]
        for part in parts:
            if (b / f"{part}.done").exists():
                continue
            self.save(phase="download", part=part)
            subprocess.run(f"curl -sSfL --retry 5 {REL}/{part} | tar -x -C {b}", shell=True, check=True)
            (b / f"{part}.done").touch()
        self.files = json.loads(man.read_text())["files"]

    # ------------------------------------------------------------- runs
    def run(self, model, out, edge, bench, limit_s):
        """One ocr_pages.py process, supervised: restarted on a crash or a stall, stopped at the time limit."""
        prog = Path(out) / model_slug(model) / "_progress.json"
        restarts = 0
        start = time.time()
        self.save(stage={"kind": "bench" if bench else "full", "model": model, "edge": edge, "out": str(out)})
        impl = self.status.get("impl", {}).get(model)      # a backend that worked (or is being tried) for this model
        started_ok = False
        while True:
            cmd = [sys.executable, str(REPO / "colab" / "ocr_pages.py"), "--model", model, "--bundle", self.a.bundle,
                   "--out", str(out), "--long-edge", str(edge), "--dtype", self.a.dtype] + (["--bench"] if bench else [])
            if impl:
                cmd += ["--model-impl", impl]
            left = free_gpu()
            if left > 1500:
                self.save(last_error=f"GPU still holds {left} MiB from another process before starting {model_slug(model)}")
            log = open(self.root / f"log-{model_slug(model)}-{edge}{'-bench' if bench else ''}.txt", "a")
            # its own process group, so a kill takes the vLLM worker too (an orphaned worker keeps the GPU memory)
            p = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
            last_done, last_change = -1, time.time()
            while p.poll() is None:
                time.sleep(30)
                if prog.exists():
                    d = json.loads(prog.read_text())
                    if d["done"] != last_done:
                        last_done, last_change = d["done"], time.time()
                        if not started_ok:
                            started_ok = True
                            self.status.setdefault("impl", {})[model] = impl or "vllm"
                            self.save()
                        if not bench:
                            eta = (d["total"] - d["done"]) * d["s_per_page"] / 3600
                            self.save(full={"model": model, "edge": edge, "done": d["done"], "total": d["total"],
                                            "s_per_page": d["s_per_page"], "eta_h": round(eta, 2), "restarts": restarts})
                stalled = time.time() - last_change > self.a.stall_min * 60
                if stalled or time.time() - start > limit_s or self.over_time():
                    try:
                        os.killpg(p.pid, signal.SIGKILL)
                    except Exception:
                        p.kill()
                    p.wait()
                    break
            try:
                os.killpg(p.pid, signal.SIGKILL)       # whatever the run left behind
            except Exception:
                pass
            log.close()
            if p.returncode == 0:
                return True
            if time.time() - start > limit_s or self.over_time():
                return False
            restarts += 1
            self.save(last_error=f"{model_slug(model)} exited {p.returncode}; restart {restarts}")
            if not started_ok:
                # it never read a page: a startup failure
                if self.status.get("impl", {}).get(model) == "vllm":
                    # this model has worked here before, so it is the environment (GPU memory, a download), not
                    # the model: free the GPU and try again a few times
                    if restarts > 3:
                        return False
                    continue
                # a model never seen working: vLLM's own code for it failed, so try the Hugging Face model code
                # once; if that fails too, drop the model rather than retry it
                if impl is None and restarts == 1:
                    impl = "transformers"
                    self.save(last_error=f"{model_slug(model)} could not start with vLLM's own model code; trying the transformers backend")
                    continue
                return False
            if restarts > self.a.restarts:
                return False

    def score(self, combos):
        """Totals matched for each (label, folder, model), on the bake-off files every one of them read in full."""
        def texts(d, m, f):
            d = Path(d) / model_slug(m) / f["sha16"]
            ps = [d / f"{p:04d}.txt" for p in f["pages"]]
            return {p: x.read_text(encoding="utf-8") for p, x in zip(f["pages"], ps)} if all(x.exists() for x in ps) else None

        bench = [f for f in self.files if f["bench"]]
        common = [f for f in bench if all(texts(d, m, f) is not None for _, d, m in combos)]
        rows = {}
        for label, d, m in combos:
            a = b = 0
            for f in common:
                x, y, _ = score_tables(tables_from_texts(texts(d, m, f)))
                a, b = a + x, b + y
            rows[label] = {"matched": a, "checked": b, "share": round(a / b, 4) if b else 0, "score": a - 2 * (b - a), "files": len(common)}
        return rows

    # ------------------------------------------------------------- the job
    def main(self):
        self.pages()
        if self.status.get("phase") == "finished" and not self.a.retry:
            return
        # bake-off at the laptop's page size, then the two best again at a larger size (small typed digits)
        board = dict(self.status.get("bench_1600") or {})
        failed = list(self.status.get("bench_failed", []))
        todo = [m for m in self.a.candidates if m not in board and (self.a.retry or m not in failed)]
        if todo:
            ok = []
            for m in todo:
                self.save(phase="bench", bench_model=m, edge=1600)
                if self.run(m, self.root / "bench" / "1600", 1600, True, self.a.bench_min * 60):
                    ok.append(m)
                    failed = [x for x in failed if x != m]
                else:
                    failed = failed + [m] if m not in failed else failed
                    self.save(last_error=f"bake-off: {m} failed or ran out of time; skipped", bench_failed=failed)
            if not (ok or board):
                return self.save(phase="failed", error="no model finished the bake-off")
            board = self.score([(m, self.root / "bench" / "1600", m) for m in list(board) + ok])
            self.save(bench_1600=board, bench_failed=failed, bench_2048=None)      # new models: the 2048 round is redone
        top = sorted(board, key=lambda m: -board[m]["score"])[:2]
        big = self.status.get("bench_2048")
        if big is None:
            done = [m for m in top if self.run(m, self.root / "bench" / "2048", 2048, True, self.a.bench_min * 60)]
            # each of the two at both sizes, on the files read at both, so the sizes are compared like for like
            big = {}
            for m in done:
                r = self.score([("1600", self.root / "bench" / "1600", m), ("2048", self.root / "bench" / "2048", m)])
                big[m] = r
            self.save(bench_2048=big)
        cands = {(m, 1600): board[m] for m in board}
        for m, r in big.items():
            cands[(m, 1600)], cands[(m, 2048)] = r["1600"], r["2048"]
        model, edge = max(cands, key=lambda k: (cands[k]["share"], cands[k]["score"]))
        why = {f"{m}@{e}": r for (m, e), r in cands.items()}
        self.save(phase="full", winner={"model": model, "edge": edge, "why": why})
        # pages the bake-off already read at the winning size need not be read again
        src = self.root / "bench" / str(edge) / model_slug(model)
        dst = self.root / "ocr_cache" / model_slug(model)
        if src.exists() and not dst.exists():
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns("_progress.json"))
        ok = self.run(model, self.root / "ocr_cache", edge, False, self.a.hours * 3600)
        prog = json.loads((dst / "_progress.json").read_text()) if (dst / "_progress.json").exists() else {}
        # the result, zipped on Drive (with the bake-off scores)
        (dst / "bakeoff.json").write_text(json.dumps({"bench_1600": board, "bench_2048": big, "winner": self.status["winner"]}, indent=1))
        zip_base = self.root / model_slug(model)
        shutil.make_archive(str(zip_base), "zip", root_dir=self.root / "ocr_cache", base_dir=model_slug(model))
        self.save(phase="finished" if ok else "stopped", zip=f"{zip_base}.zip", pages_done=prog.get("done"), pages_total=prog.get("total"),
                  hours=round((time.time() - self.t0) / 3600, 2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="/content/drive/MyDrive/ncrb_ocr")
    ap.add_argument("--bundle", default="/content/ocr_pages")
    ap.add_argument("--dtype", default="auto")
    ap.add_argument("--candidates", nargs="*", default=CANDIDATES)
    ap.add_argument("--hours", type=float, default=14, help="stop everything after this many hours since the first start")
    ap.add_argument("--bench-min", type=float, default=35, help="time limit per bake-off run, minutes")
    ap.add_argument("--stall-min", type=float, default=25, help="restart a run that has read no page for this long")
    ap.add_argument("--restarts", type=int, default=6)
    ap.add_argument("--retry", action="store_true", help="run the bake-off again for models that failed earlier, and add them to it")
    a = ap.parse_args()
    job = Job(a)
    try:
        job.main()
    except Exception as e:
        job.save(phase="failed", error=f"{type(e).__name__}: {e}")
        raise


if __name__ == "__main__":
    main()
