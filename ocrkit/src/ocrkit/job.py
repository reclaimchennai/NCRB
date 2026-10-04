"""The whole GPU job, unattended: optional bake-off, then every page with the chosen (model, page size).

    python -m ocrkit.job plan.json            # started detached by the notebook (start_new_session)

plan.json:
    {
      "name": "myproject",
      "manifest": "manifest.json" (path or URL),
      "out": "/content/drive/MyDrive/ocrkit/myproject",
      "bakeoff": {"models": ["ATH-MaaS/OvisOCR2", "PaddlePaddle/PaddleOCR-VL-1.6"], "edges": [1600], "top_edges": [2048],
                  "scorer": "ocrkit.score:consistency"},             # optional
      "runs": "winner"  or  [{"model": "...", "edge": 2048}, ...],
      "files": [file id, ...]                                         # optional: only these
      "hours": 9
    }

Everything is written to <out> as it goes (status.json, one .txt per page), so a reset machine resumes.
Guards: a model that cannot start is tried once with vLLM's transformers backend, then dropped; a run is
restarted after a crash or 25 minutes without a page (6 times at most); leftover vLLM processes are killed
before every start (an orphaned engine keeps its GPU memory); everything stops at 'hours'. No zip is made:
download the <out> folder from Drive (Drive zips it on its side) and import it with `ocrkit fetch`.
"""

from __future__ import annotations

import importlib
import json
import os
import signal
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from .models import slug
from .score import agreement, figures, score


def gpu_used_mib() -> int:
    try:
        return int(subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
                                  capture_output=True, text=True, timeout=15).stdout.split()[0])
    except Exception:
        return 0


def free_gpu(wait_s: int = 90) -> int:
    try:
        pids = subprocess.run(["nvidia-smi", "--query-compute-apps=pid", "--format=csv,noheader"], capture_output=True,
                              text=True, timeout=15).stdout.split()
    except Exception:
        pids = []
    for pid in pids:
        try:
            cmd = subprocess.run(["ps", "-p", pid, "-o", "args="], capture_output=True, text=True).stdout.lower()
            if any(w in cmd for w in ("vllm", "enginecore", "ocrkit.runner")):
                os.kill(int(pid), signal.SIGKILL)
        except Exception:
            pass
    t = time.time()
    while gpu_used_mib() > 1500 and time.time() - t < wait_s:
        time.sleep(3)
    return gpu_used_mib()


class Job:
    def __init__(self, plan: dict, plan_path: Path):
        self.p = plan
        self.out = Path(plan["out"])
        self.out.mkdir(parents=True, exist_ok=True)
        self.status_path = self.out / "status.json"
        self.s = json.loads(self.status_path.read_text()) if self.status_path.exists() else {}
        self.s.setdefault("started", time.time())
        self.s["vm_started"] = time.time()
        self.hours = float(plan.get("hours", 9))
        self.work = Path(plan.get("work", "/content/ocrkit_work"))
        self.work.mkdir(parents=True, exist_ok=True)
        m = plan["manifest"]
        self.manifest = self.work / "manifest.json"
        if str(m).startswith("http"):
            urllib.request.urlretrieve(m, self.manifest)
        else:
            mp = Path(m) if Path(m).is_absolute() else plan_path.parent / m
            self.manifest.write_text(mp.read_text())
        self.files = json.loads(self.manifest.read_text())["files"]
        if plan.get("files"):
            (self.work / "only.json").write_text(json.dumps(plan["files"]))

    def save(self, **kw):
        self.s.update(kw, updated=time.time())
        tmp = self.status_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.s, indent=1))
        tmp.replace(self.status_path)
        print(time.strftime("%H:%M:%S"), json.dumps(kw)[:300], flush=True)

    def over(self) -> bool:
        return (time.time() - self.s["started"]) / 3600 > self.hours

    def run(self, model: str, edge: int, bench: bool, limit_s: float) -> bool:
        key = f"{model}@{edge}"
        prog = self.out / slug(model, edge) / "_progress.json"
        impl = self.s.get("impl", {}).get(key)
        worked = self.s.get("worked", {}).get(key, False)
        started_ok, restarts, start = False, 0, time.time()
        self.save(stage={"kind": "bench" if bench else "full", "model": model, "edge": edge, "slug": slug(model, edge)})
        while True:
            cmd = [sys.executable, "-m", "ocrkit.runner", "--manifest", str(self.manifest), "--model", model, "--edge", str(edge),
                   "--out", str(self.out), "--work", str(self.work), "--dtype", self.p.get("dtype", "auto")]
            cmd += ["--bench"] if bench else []
            cmd += ["--only", str(self.work / "only.json")] if (self.work / "only.json").exists() and not bench else []
            cmd += ["--model-impl", impl] if impl else []
            if free_gpu() > 1500:
                self.save(last_error=f"GPU still busy before starting {key}")
            log = open(self.out / f"log-{slug(model, edge)}{'-bench' if bench else ''}.txt", "a")
            proc = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
            last, changed = -1, time.time()
            while proc.poll() is None:
                time.sleep(30)
                if prog.exists():
                    d = json.loads(prog.read_text())
                    if d["done"] != last:
                        last, changed = d["done"], time.time()
                        if not started_ok:
                            started_ok = worked = True
                            self.s.setdefault("worked", {})[key] = True
                            self.s.setdefault("impl", {})[key] = impl
                        self.save(progress={"key": key, "done": d["done"], "total": d["total"], "s_per_page": d["s_per_page"],
                                            "eta_h": round((d["total"] - d["done"]) * d["s_per_page"] / 3600, 2)})
                if time.time() - changed > 25 * 60 or time.time() - start > limit_s or self.over():
                    break
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except Exception:
                pass
            proc.wait()
            log.close()
            if proc.returncode == 0:
                return True
            if time.time() - start > limit_s or self.over():
                return False
            restarts += 1
            self.save(last_error=f"{key} exited {proc.returncode}; restart {restarts}")
            if not started_ok and not worked:
                if impl is None and restarts == 1:
                    impl = "transformers"     # vLLM's own code for the model failed: try the Hugging Face model code
                    continue
                return False
            if restarts > 6:
                return False

    def texts(self, model: str, edge: int, f: dict) -> dict | None:
        d = self.out / slug(model, edge) / f["id"]
        paths = [d / f"{p:04d}.txt" for p in f["pages"]]
        return {p: x.read_text(encoding="utf-8") for p, x in zip(f["pages"], paths)} if all(x.exists() for x in paths) else None

    def bakeoff(self) -> tuple[str, int]:
        b = self.p["bakeoff"]
        scorer = b.get("scorer", "ocrkit.score:consistency")
        mod, fn = scorer.split(":")
        sys.path[:0] = [p for p in b.get("pythonpath", [])]
        score_fn = getattr(importlib.import_module(mod), fn)
        cands = [(m, e) for m in b["models"] for e in b.get("edges", [1600])]
        board = self.s.get("board", {})
        for m, e in cands:
            k = f"{m}@{e}"
            if k in board or k in self.s.get("bench_failed", []):
                continue
            self.save(phase="bench", bench=k)
            if not self.run(m, e, True, b.get("minutes", 35) * 60):
                self.save(bench_failed=self.s.get("bench_failed", []) + [k])
        bench = [f for f in self.files if f.get("bench")]

        def mk(k):
            m, e = k.rsplit("@", 1)
            return m, int(e)

        def rank(keys):
            """Each (model, size) on the bake-off files every one of them read: sums matched, and agreement with the others."""
            common = [f for f in bench if all(self.texts(*mk(k), f) is not None for k in keys)]
            out = {}
            for k in keys:
                mt = ck = 0
                agree = []
                for f in common:
                    t = self.texts(*mk(k), f)
                    a, c = score_fn(t, f) if score_fn.__code__.co_argcount > 1 else score_fn(t)
                    mt, ck = mt + a, ck + c
                    agree += [agreement(figures(t), figures(self.texts(*mk(o), f))) for o in keys if o != k]
                out[k] = {"matched": mt, "checked": ck, "share": round(mt / ck, 4) if ck else 0, "score": score(mt, ck),
                          "agree": round(sum(agree) / len(agree), 4) if agree else 0, "files": len(common)}
            return out

        ok = [f"{m}@{e}" for m, e in cands if f"{m}@{e}" not in self.s.get("bench_failed", [])]
        board = rank(ok)
        self.save(board=board)
        # the best few again at larger page sizes
        top = sorted(board, key=lambda k: (-board[k]["share"], -board[k]["agree"]))[:2]
        for e2 in b.get("top_edges", []):
            for k in top:
                m = k.rsplit("@", 1)[0]
                k2 = f"{m}@{e2}"
                if k2 not in board and k2 not in self.s.get("bench_failed", []):
                    self.save(phase="bench", bench=k2)
                    if not self.run(m, e2, True, b.get("minutes", 35) * 60):
                        self.save(bench_failed=self.s.get("bench_failed", []) + [k2])
        ok = [k for k in set(ok) | {f"{k.rsplit('@', 1)[0]}@{e}" for k in top for e in b.get("top_edges", [])}
              if k not in self.s.get("bench_failed", [])]
        board = rank(sorted(ok))
        best = max(board, key=lambda k: (board[k]["share"], board[k]["score"], board[k]["agree"]))
        self.save(board=board, winner=best)
        m, e = best.rsplit("@", 1)
        return m, int(e)

    def main(self):
        if self.s.get("phase") == "finished":
            return
        runs = self.p.get("runs", "winner")
        if runs == "winner":
            m, e = self.bakeoff() if self.p.get("bakeoff") else (None, None)
            if not m:
                return self.save(phase="failed", error="runs is 'winner' but there is no bake-off")
            runs = [{"model": m, "edge": e}]
        done = set(self.s.get("runs_done", []))
        for r in runs:
            k = f"{r['model']}@{r['edge']}"
            if k in done:
                continue
            self.save(phase="full")
            if self.run(r["model"], int(r["edge"]), False, self.hours * 3600):
                done.add(k)
                self.save(runs_done=sorted(done))
            else:
                self.save(last_error=f"{k} did not finish; moving on")
            if self.over():
                break
        self.save(phase="finished", hours=round((time.time() - self.s["started"]) / 3600, 2), out=str(self.out))


def main():
    path = Path(sys.argv[1])
    job = Job(json.loads(path.read_text()), path)
    try:
        job.main()
    except Exception as e:
        job.save(phase="failed", error=f"{type(e).__name__}: {e}")
        raise


if __name__ == "__main__":
    main()
