"""For each candidate instance, build the hybrid model (no solve) and report how many subexpressions are usable."""
import json, os, sys, time
from concurrent.futures import ProcessPoolExecutor
from uenv.osil import build_scip, presolved_bounds, read_osil

def one(name):
    t0 = time.time()
    try:
        inst = read_osil(os.path.expanduser(f"~/.cache/minlplib/minlplib/osil/{name}.osil"))
        _, _, stats = build_scip(inst, "hybrid", bounds=presolved_bounds(inst))
        rec = dict(instance=name, nvars=len(inst.var_lb), ncons=len(inst.rows) - 1, **stats)
    except BaseException as e:
        rec = dict(instance=name, error=f"{type(e).__name__}: {e}"[:200])
    rec["time"] = time.time() - t0
    return rec

def guarded(name):
    """Run ``one`` in a subprocess so a crash or timeout loses one instance only."""
    import subprocess
    try:
        p = subprocess.run([sys.executable, __file__, "--one", name], capture_output=True, text=True, timeout=400)
        return json.loads(p.stdout.strip().split("\n")[-1])
    except Exception as e:
        return dict(instance=name, error=f"{type(e).__name__}"[:200])


if __name__ == "__main__":
    if sys.argv[1] == "--one":
        print(json.dumps(one(sys.argv[2]))); sys.exit()
    from concurrent.futures import ThreadPoolExecutor
    names = [l.strip() for l in open(sys.argv[1]) if l.strip()]
    with ThreadPoolExecutor(16) as ex, open(sys.argv[2], "w") as out:
        for rec in ex.map(guarded, names):
            out.write(json.dumps(rec) + "\n"); out.flush()
