"""Watch the background job from a notebook cell, then hand back the result and free the GPU.

Runs inside the Colab kernel (it needs google.colab for the download and for
runtime.unassign); run_all.py does the work in a separate process. A running
cell also keeps the session counted as active, so Colab does not recycle the
VM for idleness while the job runs.

    exec(open('/content/NCRB/colab/monitor.py').read()); watch()
"""

import json
import time
from pathlib import Path


def job_alive() -> bool:
    import subprocess
    return bool(subprocess.run(["pgrep", "-f", "[c]olab/run_all.py"], capture_output=True).stdout.strip())


def watch(root="/content/drive/MyDrive/ncrb_ocr", every=300, release=True):
    status_path = Path(root) / "status.json"
    last, dead_since = None, None
    while True:
        s = json.loads(status_path.read_text()) if status_path.exists() else {}
        phase = s.get("phase", "starting")
        # the job process is gone but never said it finished: stop waiting (and stop paying for an idle GPU)
        if phase not in ("finished", "stopped", "failed") and not job_alive():
            dead_since = dead_since or time.time()
            if time.time() - dead_since > 120:
                log = Path(root).parent / "ncrb_ocr_run.log"
                print("the background job is not running. Last lines of its log:")
                print(log.read_text()[-3000:] if log.exists() else "(no log)")
                s["phase"] = "failed"
                break
        else:
            dead_since = None
        if phase == "full" and s.get("full"):
            f = s["full"]
            line = f"full run, {f['model'].split('/')[-1]} @{f['edge']}px: {f['done']}/{f['total']} pages, {f['s_per_page']} s/page, about {f['eta_h']} h left"
        elif phase == "bench":
            line = f"bake-off: {s.get('bench_model', '').split('/')[-1]} @{s.get('edge')}px"
        else:
            line = phase
        if s.get("last_error"):
            line += f"  (last problem: {s['last_error']})"
        hrs = (time.time() - s.get("started", time.time())) / 3600
        if line != last:
            print(f"{time.strftime('%H:%M')} [{hrs:.1f} h] {line}", flush=True)
            last = line
        if phase in ("finished", "stopped", "failed"):
            break
        time.sleep(every if job_alive() else 30)
    print(json.dumps({k: s.get(k) for k in ("phase", "winner", "pages_done", "pages_total", "hours", "zip", "error")}, indent=1)[:3000])
    z = s.get("zip")
    if z and Path(z).exists():
        try:
            from google.colab import files
            files.download(z)          # lands in the laptop's Downloads folder (it is also on Drive)
            time.sleep(60)
        except Exception as e:
            print("download from the browser failed; the zip is on Drive:", z, e)
    if release:
        from google.colab import runtime
        print("releasing the GPU so no more compute units are used")
        runtime.unassign()
