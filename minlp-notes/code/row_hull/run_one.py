"""One cell: python run_one.py <m> <n> <seed> <cap> <cost> <form:orig|cuts> <solver> [--tl 120]"""
import argparse, json, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "vertex_binarization"))
from instances import transport, netflow, transport_fc
from rowhull.strengthen import cut_loop, cut_ir, closed_form_ir
from sob.model import original_ir
from sob.backends import SOLVERS

ap = argparse.ArgumentParser()
ap.add_argument("m"); ap.add_argument("n", type=int); ap.add_argument("seed", type=int)
ap.add_argument("cap"); ap.add_argument("cost"); ap.add_argument("form"); ap.add_argument("solver")
ap.add_argument("--tl", type=float, default=120); ap.add_argument("--threads", type=int, default=4)
ap.add_argument("--log", action="store_true")
a = ap.parse_args()
if a.m.startswith('g'):
    p = netflow(int(a.m[1:]), a.n, a.seed, a.cap, a.cost)
elif a.m.startswith('f'):
    p = transport_fc(int(a.m[1:]), a.n, a.seed, a.cap, a.cost)
else:
    p = transport(int(a.m), a.n, a.seed, a.cap, a.cost)
rec = {"name": p.name, "form": a.form, "solver": a.solver, "tl": a.tl}
t0 = time.time()
if a.form == "cuts":
    cuts, extra, info = cut_loop(p, log=a.log)
    rec["cutinfo"] = info
    ir = cut_ir(p, cuts, extra)
elif a.form == "cf":
    ir, info = closed_form_ir(p)
    rec["cutinfo"] = info
else:
    ir = original_ir(p)
res = SOLVERS[a.solver](ir, max(a.tl - (time.time() - t0), 1.0), threads=a.threads, log=a.log)
res.pop("x", None)
rec.update(res); rec["total_time"] = time.time() - t0
print(json.dumps(rec))
