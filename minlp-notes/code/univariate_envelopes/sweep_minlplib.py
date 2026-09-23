"""Run run_minlplib.py over a list of instances and modes in parallel; append JSON lines."""
import argparse, json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

ap = argparse.ArgumentParser()
ap.add_argument("out"); ap.add_argument("--list", required=True); ap.add_argument("--osil", default=os.path.expanduser("~/.cache/minlplib/minlplib/osil"))
ap.add_argument("--modes", nargs="+", default=["native", "hybrid"]); ap.add_argument("--tl", type=float, default=120)
ap.add_argument("--workers", type=int, default=12)
a = ap.parse_args()
names = [l.strip() for l in open(a.list) if l.strip()]
done = set()
if os.path.exists(a.out):
    done = {(r["instance"], r["mode"]) for r in map(json.loads, open(a.out))}

def run(cell):
    name, mode = cell
    if cell in done:
        return
    cmd = [sys.executable, "run_minlplib.py", f"{a.osil}/{name}.osil", mode, "--tl", str(a.tl)]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=a.tl + 600)
        lines = [l for l in p.stdout.split("\n") if l.startswith("{")]
        rec = json.loads(lines[-1]) if lines else {"status": "error", "err": (p.stderr or p.stdout)[-400:]}
    except subprocess.TimeoutExpired:
        rec = {"status": "error", "err": "harness timeout"}
    rec.update(instance=name, mode=mode, tl=a.tl)
    with open(a.out, "a") as fh:
        fh.write(json.dumps(rec) + "\n")
    print(name, mode, rec.get("status"), rec.get("time"), flush=True)

with ThreadPoolExecutor(a.workers) as ex:
    list(ex.map(run, [(n, m) for n in names for m in a.modes]))
