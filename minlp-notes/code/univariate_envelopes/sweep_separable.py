"""Grid over run_quartic.py (SCIP native / hybrid / uenv) with resumable JSON-lines output."""
import argparse, itertools, json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

ap = argparse.ArgumentParser()
ap.add_argument("out"); ap.add_argument("--families", nargs="+", required=True); ap.add_argument("--n", nargs="+", type=int, required=True)
ap.add_argument("--m", nargs="+", type=int, default=[1]); ap.add_argument("--seeds", nargs="+", type=int, default=[1])
ap.add_argument("--modes", nargs="+", default=["native", "hybrid", "uenv"]); ap.add_argument("--tl", type=float, default=120)
ap.add_argument("--workers", type=int, default=6)
a = ap.parse_args()
done = {r["cell"] for r in map(json.loads, open(a.out))} if os.path.exists(a.out) else set()

def run(cell):
    key = "/".join(map(str, cell))
    if key in done:
        return
    fam, n, m, seed, mode = cell
    try:
        out = subprocess.run([sys.executable, "run_quartic.py", fam, str(n), str(m), str(seed), mode, "--tl", str(a.tl)],
                             capture_output=True, text=True, timeout=a.tl + 300).stdout
        rec = json.loads([l for l in out.split("\n") if l.startswith("{")][-1])
    except Exception as e:
        rec = {"status": f"error:{type(e).__name__}"}
    rec.update(cell=key, family=fam, n=n, m=m, seed=seed, mode=mode, tl=a.tl)
    with open(a.out, "a") as fh:
        fh.write(json.dumps(rec) + "\n")
    print(key, rec.get("status"), rec.get("time"), flush=True)

with ThreadPoolExecutor(a.workers) as ex:
    list(ex.map(run, itertools.product(a.families, a.n, a.m, a.seeds, a.modes)))
