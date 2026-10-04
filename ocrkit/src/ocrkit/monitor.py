"""Watch a job from a notebook cell: a progress bar, how well the readings add up, then free the GPU.

    from ocrkit.monitor import watch; watch('/content/drive/MyDrive/ocrkit/myproject')

Runs in the notebook kernel (it needs google.colab to release the runtime); the job is a separate, detached
process, so stopping this cell never stops the job. A running cell also keeps Colab from recycling the
machine for idleness. When the job is finished (or gone for 10 minutes) the GPU is released, so no compute
units are spent after the last page.
"""

from __future__ import annotations

import json
import random
import subprocess
import time
from pathlib import Path

from .score import consistency

UNITS_PER_HOUR = 5.4      # A100 40 GB, Colab, 2026; the Resources panel has the real figure


def _read(p: Path):
    try:
        return json.loads(p.read_text())
    except Exception:
        return None


def alive() -> bool:
    return bool(subprocess.run(["pgrep", "-f", "[o]crkit.job"], capture_output=True).stdout.strip())


def gpu() -> str:
    try:
        u, used, tot = subprocess.run(["nvidia-smi", "--query-gpu=utilization.gpu,memory.used,memory.total", "--format=csv,noheader,nounits"],
                                      capture_output=True, text=True, timeout=10).stdout.strip().split(",")
        return f"GPU {int(u)}% {int(used) / 1024:.0f}/{int(tot) / 1024:.0f} GB"
    except Exception:
        return "GPU ?"


def watch(out: str, every: int = 15, release: bool = True, units_per_hour: float = UNITS_PER_HOUR):
    from tqdm.auto import tqdm

    out = Path(out)
    files = {f["id"]: f for f in (_read(Path("/content/ocrkit_work/manifest.json")) or {}).get("files", [])}
    bar, key, said, dead, scored, tally = None, None, {}, None, set(), [0, 0]

    def say(topic, text):
        if said.get(topic) != text:
            said[topic] = text
            (bar.write if bar else print)(f"{time.strftime('%H:%M')}  {text}")

    while True:
        s = _read(out / "status.json") or {}
        phase = s.get("phase", "starting")
        if phase not in ("finished", "failed") and not alive():
            dead = dead or time.time()
            if time.time() - dead > 120:
                say("dead", "the job is not running; start it again (it resumes). The GPU is released in 10 minutes otherwise.")
            if time.time() - dead > 600:
                phase = "abandoned"
        else:
            dead = None
        say("phase", f"phase: {phase}" + (f" ({s.get('bench')})" if phase == "bench" else ""))
        if s.get("last_error"):
            say("err", f"problem: {s['last_error']}")
        if s.get("board"):
            say("board", "bake-off: " + "; ".join(f"{k.split('/')[-1]} {v['share']:.0%} sums, {v['agree']:.0%} agree" for k, v in s["board"].items()))
        if s.get("winner"):
            say("winner", f"winner: {s['winner']}")
        st = s.get("stage")
        if st:
            k = (st["kind"], st["slug"])
            d = out / st["slug"]
            if k != key:
                if bar:
                    bar.close()
                key, scored, tally = k, set(), [0, 0]
                bar = tqdm(total=None, unit="page", dynamic_ncols=True,
                           bar_format="{desc} {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} pages [{elapsed}] {postfix}",
                           desc=f"{'test' if st['kind'] == 'bench' else 'FULL'} {st['slug']}")
            prog = _read(d / "_progress.json") or {}
            parts = []
            if prog:
                bar.total, bar.n = prog["total"], prog["done"]
                left = (prog["total"] - prog["done"]) * prog["s_per_page"] / 3600
                parts += [f"{prog['s_per_page']:.2f}s/page", f"{left:.1f}h left" if left >= 0.1 else f"{left * 60:.0f}min left"]
            else:
                parts.append("loading the model")
            # sums matched on a sample of finished files
            if d.exists() and files:
                todo = [i for i in (p.name for p in d.iterdir() if p.is_dir()) if i not in scored and i in files]
                for fid in random.Random(1).sample(todo, min(15, len(todo))):
                    f = files[fid]
                    paths = [d / fid / f"{p:04d}.txt" for p in f["pages"]]
                    if all(x.exists() for x in paths):
                        a, c = consistency({p: x.read_text(encoding="utf-8") for p, x in zip(f["pages"], paths)})
                        tally[0] += a
                        tally[1] += c
                        scored.add(fid)
                if tally[1]:
                    parts.append(f"sums {tally[0] / tally[1]:.0%} ({len(scored)} files)")
                errs = sum(1 for _ in d.glob("*/*.err"))
                parts.append(f"err {errs}")
            parts += [gpu(), f"≈{(time.time() - s.get('vm_started', time.time())) / 3600 * units_per_hour:.0f} units"]
            bar.set_postfix_str(" | ".join(parts), refresh=False)
            bar.refresh()
        if phase in ("finished", "failed", "abandoned"):
            break
        time.sleep(every)
    if bar:
        bar.close()
    print(json.dumps({k: s.get(k) for k in ("phase", "winner", "runs_done", "hours", "error")}, indent=1))
    print(f"Readings are in {out} on Drive. Download that folder from drive.google.com (right-click, Download) and run "
          f"`ocrkit fetch <zips or folder> --cache <your cache>` on your computer.")
    if release:
        from google.colab import runtime
        print("releasing the GPU")
        runtime.unassign()
