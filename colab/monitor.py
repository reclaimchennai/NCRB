"""Watch the background job from a notebook cell: a live progress bar, quality against NCRB's own totals,
then hand back the result and free the GPU.

Runs inside the Colab kernel (it needs google.colab for the download and for runtime.unassign); run_all.py
does the work in a separate process. A running cell also keeps the session counted as active, so Colab does
not recycle the VM for idleness while the job runs.

    exec(open('/content/NCRB/colab/monitor.py').read()); watch()

The bar's line shows, for the stage running now:
    pages done / total, speed (s/page), time left, pages the model failed on (err), the GPU (util, memory),
    "totals": the share of NCRB's printed row and column totals that the model's tables reproduce on the
    files it has finished, next to what the current (Tesseract) reading gets on the same files, and the
    compute units used since the VM started (an estimate; Colab's Resources panel has the real figure).
"""

import json
import random
import re
import subprocess
import sys
import time
from pathlib import Path

REPO = Path("/content/NCRB")
UNITS_PER_HOUR = 5.4        # A100 at the March 2026 rate; the Resources panel shows what Colab really charges


def job_alive() -> bool:
    return bool(subprocess.run(["pgrep", "-f", "[c]olab/run_all.py"], capture_output=True).stdout.strip())


def gpu() -> str:
    try:
        o = subprocess.run(["nvidia-smi", "--query-gpu=utilization.gpu,memory.used,memory.total", "--format=csv,noheader,nounits"],
                           capture_output=True, text=True, timeout=10).stdout.strip().split(",")
        return f"GPU {int(o[0])}% {int(o[1]) / 1024:.0f}/{int(o[2]) / 1024:.0f} GB"
    except Exception:
        return "GPU ?"


def _read(path: Path):
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


class Quality:
    """Totals-check score of the model's finished files, against the Tesseract reading of the same files."""

    def __init__(self, manifest, slug_dir: Path, sample=True):
        sys.path.insert(0, str(REPO / "src"))
        from ncrb.vlm_tables import score_tables, tables_from_texts
        self.score_tables, self.tables_from_texts = score_tables, tables_from_texts
        self.files = manifest
        self.dir = slug_dir
        self.seen = {}                  # sha16 -> (matched, checked)
        self.tess = [0, 0]
        self.new = [0, 0]
        self.order = list(manifest)
        if sample:
            random.Random(7).shuffle(self.order)

    def update(self, budget_s=20):
        t0 = time.time()
        for f in self.order:
            if f["sha16"] in self.seen:
                continue
            d = self.dir / f["sha16"]
            paths = [d / f"{p:04d}.txt" for p in f["pages"]]
            if not d.exists() or not all(x.exists() for x in paths):
                continue
            try:
                texts = {p: x.read_text(encoding="utf-8") for p, x in zip(f["pages"], paths)}
                a, b, _ = self.score_tables(self.tables_from_texts(texts))
            except Exception:
                a = b = 0
            self.seen[f["sha16"]] = (a, b)
            if b:
                self.new[0] += a
                self.new[1] += b
                self.tess[0] += f["checks"][0] if f["checks"][1] else 0
                self.tess[1] += f["checks"][1]
            if time.time() - t0 > budget_s:
                break

    def text(self) -> str:
        n = sum(1 for v in self.seen.values() if v[1])
        if not self.new[1]:
            return "totals: –"
        t = f", Tesseract {self.tess[0] / self.tess[1]:.0%}" if self.tess[1] else ""
        return f"totals {self.new[0] / self.new[1]:.0%} ({n} files{t})"


class Monitor:
    def __init__(self, root, every, release, units_per_hour, state="status.json"):
        from tqdm.auto import tqdm
        self.tqdm = tqdm
        self.root, self.every, self.release, self.rate = Path(root), every, release, units_per_hour
        self.status_path = self.root / state
        self.bar, self.key, self.quality = None, None, None
        self.said = {}
        self.dead_since = None
        self.n_err, self.err_checked = 0, 0
        self.manifest = None

    def say(self, topic, text):
        if self.said.get(topic) != text:
            self.said[topic] = text
            (self.bar.write if self.bar else print)(f"{time.strftime('%H:%M')}  {text}")

    def board(self, s):
        for key, label in (("bench_1600", "bake-off at 1600 px"), ("bench_2048", "bake-off, best two at 2048 px")):
            b = s.get(key)
            if not b:
                continue
            rows = []
            for m, r in b.items():
                if "share" in r:
                    rows.append(f"{m.split('/')[-1]} {r['share']:.1%}")
                else:                              # {"1600": {...}, "2048": {...}}
                    rows.append(f"{m.split('/')[-1]} " + " / ".join(f"{k}px {v['share']:.1%}" for k, v in r.items()))
            self.say(key, f"{label}, share of printed totals reproduced: " + "; ".join(rows))

    def stage(self, s):
        st = s.get("stage")
        if not st:
            return
        slug = re.sub(r"[^A-Za-z0-9.]+", "-", st["model"].split("/")[-1]).strip("-")      # as ncrb.vlm_tables.model_slug
        d = Path(st["out"]) / slug
        key = (st["kind"], st["model"], st["edge"])
        if key != self.key:
            if self.bar:
                self.bar.close()
            self.key = key
            if self.manifest is None:
                m = _read(Path("/content/ocr_pages/manifest.json"))
                self.manifest = m["files"] if m else []
            files = [f for f in self.manifest if f.get("bench")] if st["kind"] == "bench" else self.manifest
            only = self.root / f"{(_read(self.status_path) or {}).get('plan', '')}-files.json"
            if st["kind"] != "bench" and only.name != "-files.json" and only.exists():
                keep = set(json.loads(only.read_text()))
                files = [f for f in files if f["sha16"] in keep]
            try:
                self.quality = Quality(files, d, sample=st["kind"] == "full") if files else None
            except Exception as e:
                self.say("qerr", f"(quality check unavailable: {type(e).__name__}: {e})")
                self.quality = None
            # no tqdm rate/ETA: the count is set from the job's own progress file, so tqdm's would be wrong
            self.bar = self.tqdm(total=sum(len(f["pages"]) for f in files) or None, unit="page", dynamic_ncols=True, leave=True,
                                 bar_format="{desc} {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} pages [{elapsed}] {postfix}",
                                 desc=f"{'test' if st['kind'] == 'bench' else 'FULL'} {slug} @{st['edge']}px")
            self.err_checked = 0
        prog = _read(d / "_progress.json") or {}
        if prog:
            self.bar.total = prog["total"]
            self.bar.n = prog["done"]
            sp = prog.get("s_per_page")
            left = (prog["total"] - prog["done"]) * sp / 3600 if sp else None
        else:
            sp = left = None
        if time.time() - self.err_checked > 120 and d.exists():
            self.err_checked = time.time()
            self.n_err = sum(1 for _ in d.glob("*/*.err"))
        parts = []
        if sp:
            parts.append(f"{sp:.2f}s/page")
        if left is not None:
            parts.append(f"{left:.1f}h left" if left >= 0.1 else f"{left * 60:.0f}min left")
        if not prog:
            parts.append("loading the model")
        parts.append(f"err {self.n_err}")
        parts.append(gpu())
        if self.quality:
            self.quality.update()
            parts.append(self.quality.text())
        used = (time.time() - s.get("vm_started", time.time())) / 3600 * self.rate
        parts.append(f"≈{used:.0f} units")
        self.bar.set_postfix_str(" | ".join(parts), refresh=False)
        self.bar.refresh()

    def poll(self) -> dict:
        s = _read(self.status_path) or {}
        phase = s.get("phase", "starting")
        if phase not in ("finished", "stopped", "failed") and not job_alive():
            self.dead_since = self.dead_since or time.time()
            waited = time.time() - self.dead_since
            if waited > 120:
                log = self.root.parent / "ncrb_ocr_run.log"
                self.say("dead", "the background job is not running. Start it again (it resumes from the pages on Drive); "
                                 "the GPU is released in 10 minutes if it is still not running. Last lines of its log:\n"
                         + (log.read_text()[-2000:] if log.exists() else "(no log)"))
            if waited > 720:
                s["phase"] = "abandoned"
                return s
        else:
            self.dead_since = None
            self.said.pop("dead", None)
        self.say("phase", f"phase: {phase}" + (f" ({s['part']})" if phase == "download" and s.get("part") else ""))
        if s.get("last_error"):
            self.say("err", f"problem: {s['last_error']}")
        self.board(s)
        if s.get("winner"):
            w = s["winner"]
            self.say("winner", f"winner: {w['model']} at {w['edge']} px")
        self.stage(s)
        return s

    def finish(self, s):
        if self.bar:
            self.bar.close()
        keys = ("phase", "pages_done", "pages_total", "hours", "zip", "error")
        print(json.dumps({k: s.get(k) for k in keys}, indent=1))
        z = s.get("zip")
        if s.get("phase") == "finished" and z and Path(z).exists():  # (a plan's zip too)      # a partial zip from a stopped run is not the result
            try:
                from google.colab import files
                files.download(z)          # lands in the laptop's Downloads folder (it is also on Drive)
                time.sleep(60)
            except Exception as e:
                print("download from the browser failed; the zip is on Drive:", z, e)
        if self.release:
            from google.colab import runtime
            print("releasing the GPU so no more compute units are used")
            runtime.unassign()


def watch(root="/content/drive/MyDrive/ncrb_ocr", every=15, release=True, units_per_hour=UNITS_PER_HOUR, state="status.json"):
    m = Monitor(root, every, release, units_per_hour, state)
    while True:
        s = m.poll()
        if s.get("phase") in ("finished", "stopped", "failed", "abandoned"):
            break
        time.sleep(every)
    m.finish(s)
