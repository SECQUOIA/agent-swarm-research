"""60-digit feasibility check of the best local-search patterns against the OSiL rows (osil_eval, mpmath).
Writes ../runs/primal_verified.json with pattern, objective, max row / bound violation.
usage: verify_primal.py names..."""
import sys, os, json
import mpmath as mp
from nucsim import Data
from reform import solve_mp, to_osil
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../benchmark-observations/code"))
from osil_eval import Model, mp_backend

best = json.load(open("../runs/ls_best.json"))
path = "../runs/primal_verified.json"
out = json.load(open(path)) if os.path.exists(path) else {}
for name in sys.argv[1:]:
    D = Data(name); typ = best[name]["typ"]
    ks, ps, lams, Gx, Vx, KF, fpres = solve_mp(D, typ)
    x = to_osil(D, typ, ks, ps, lams, Gx, Vx)
    M = Model(os.path.expanduser(f"~/.cache/minlplib/minlplib/osil/{name}.osil"))
    B = mp_backend(60); chk = M.check(x, B); obj = M.objective(x, B)
    out[name] = dict(pattern=typ, objective=mp.nstr(obj, 20), max_row_violation=mp.nstr(chk["row"][0], 3),
                     max_bound_violation=mp.nstr(chk["bound"][0], 3), max_int_violation=chk["int"][0],
                     x=[mp.nstr(v, 25) for v in x])
    print(name, out[name]["objective"], out[name]["max_row_violation"], out[name]["max_bound_violation"], flush=True)
json.dump(out, open(path, "w"), indent=0)
