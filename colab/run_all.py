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
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
from ncrb.vlm_tables import model_slug, score_tables, tables_from_texts  # noqa: E402

REL = "https://github.com/reclaimchennai/NCRB/releases/download/ocr-pages"
# best first on OmniDocBench v1.6 tables (Oct 2026); the bake-off on NCRB's own scans decides
CANDIDATES = ["XingChen-AGI/TeleOCR", "ATH-MaaS/OvisOCR2", "PaddlePaddle/PaddleOCR-VL-1.6", "zai-org/GLM-OCR"]


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
        while True:
            cmd = [sys.executable, str(REPO / "colab" / "ocr_pages.py"), "--model", model, "--bundle", self.a.bundle,
                   "--out", str(out), "--long-edge", str(edge), "--dtype", self.a.dtype] + (["--bench"] if bench else [])
            log = open(self.root / f"log-{model_slug(model)}-{edge}{'-bench' if bench else ''}.txt", "a")
            p = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT)
            last_done, last_change = -1, time.time()
            while p.poll() is None:
                time.sleep(30)
                if prog.exists():
                    d = json.loads(prog.read_text())
                    if d["done"] != last_done:
                        last_done, last_change = d["done"], time.time()
                        if not bench:
                            eta = (d["total"] - d["done"]) * d["s_per_page"] / 3600
                            self.save(full={"model": model, "edge": edge, "done": d["done"], "total": d["total"],
                                            "s_per_page": d["s_per_page"], "eta_h": round(eta, 2), "restarts": restarts})
                stalled = time.time() - last_change > self.a.stall_min * 60
                if stalled or time.time() - start > limit_s or self.over_time():
                    p.kill()
                    p.wait()
                    break
            log.close()
            if p.returncode == 0:
                return True
            if time.time() - start > limit_s or self.over_time():
                return False
            restarts += 1
            self.save(last_error=f"{model_slug(model)} exited {p.returncode}; restart {restarts}")
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
        if self.status.get("phase") == "finished":
            return
        # bake-off at the laptop's page size, then the two best again at a larger size (small typed digits)
        board = self.status.get("bench_1600")
        if not board:
            ok = []
            for m in self.a.candidates:
                self.save(phase="bench", bench_model=m, edge=1600)
                if self.run(m, self.root / "bench" / "1600", 1600, True, self.a.bench_min * 60):
                    ok.append(m)
                else:
                    self.save(last_error=f"bake-off: {m} failed or ran out of time; skipped")
            if not ok:
                return self.save(phase="failed", error="no model finished the bake-off")
            board = self.score([(m, self.root / "bench" / "1600", m) for m in ok])
            self.save(bench_1600=board)
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
    a = ap.parse_args()
    job = Job(a)
    try:
        job.main()
    except Exception as e:
        job.save(phase="failed", error=f"{type(e).__name__}: {e}")
        raise


if __name__ == "__main__":
    main()
