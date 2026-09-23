"""Independent re-check of nuclear-global/runs/primal_verified.json with the
separately written OSiL evaluator of benchmark-observations/code/osil_eval.py."""
import json, sys, os, mpmath
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../benchmark-observations/code"))
from osil_eval import Model, mp_backend
B = mp_backend(60)
d = json.load(open(os.path.join(os.path.dirname(__file__), "../runs/primal_verified.json")))
for name, e in d.items():
    m = Model(os.path.expanduser(f"~/.cache/minlplib/minlplib/osil/{name}.osil"))
    x = e["x"]
    if isinstance(x, dict):
        x = [x[v] for v in m.vnames]
    xv = [mpmath.mpf(str(v)) for v in x]
    r = m.check(xv, B)
    print(name, "obj", mpmath.nstr(m.objective(xv, B), 12), "bound", mpmath.nstr(r["bound"][0], 3),
          "row", mpmath.nstr(r["row"][0], 3), "int", r["int"][0], flush=True)
