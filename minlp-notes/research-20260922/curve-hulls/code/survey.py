"""Which open candidate instances have variables with >= 2 independent univariate atoms?
python survey.py > survey.out"""
import sys, time, collections
import model
from model import read_osil

CANDS = open(sys.argv[1]).read().split() if len(sys.argv) > 1 else []
for name in CANDS:
    t0 = time.time()
    try:
        inst = read_osil(model.OSIL.format(name))
        det = model.Detected(inst, kmin=2)
    except Exception as e:
        print(f"{name}: ERROR {type(e).__name__}: {e}", flush=True); continue
    multi = sum(1 for v, a in det.all_atoms.items() if len(a) >= 2)
    rej = collections.Counter(det.rejected[v] for v, a in det.all_atoms.items() if len(a) >= 2 and v in det.rejected)
    print(f"{name}: vars with >=2 atom keys {multi}, selected {len(det.sel)}, rejected {dict(rej)}  ({time.time()-t0:.1f}s)", flush=True)
    for k, n in model.summary(det).items():
        print(f"    {n} x  ({k})", flush=True)
