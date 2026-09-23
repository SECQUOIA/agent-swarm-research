"""Do the cuts handed to the solver in the experiments cut off the optimal solution of the original model?"""
import sys, json
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE.parents[1] / "vertex_binarization"))
from instances import transport, netflow
from rowhull.strengthen import cut_loop
from sob.model import original_ir
from sob.backends import solve_gurobi

cells = [("t", 10, 15, 3, "random", "quad"), ("t", 10, 15, 0, "random", "quad"), ("g", 40, 3, 3, "random", "quad"),
         ("t", 8, 12, 1, "random", "quad"), ("t", 10, 15, 1, "random", "quad"), ("t", 10, 15, 4, "random", "quad")]
for kind, m, n, s, cap, cost in cells:
    p = transport(m, n, s, cap, cost) if kind == "t" else netflow(m, n, s, cap, cost)
    res = solve_gurobi(original_ir(p), 200, threads=4, gap=1e-6)
    x = res["x"]
    val = dict(x)
    for i, f in enumerate(p.funcs):
        val[f"w{i}"] = f(x[f"x{i}"])
    cuts, extra, info = cut_loop(p)
    viol = [rhs - sum(c * val[k] for k, c in coefs.items()) for coefs, rhs in cuts]
    nb = sum(v > 1e-6 for v in viol)
    print(json.dumps({"name": p.name, "orig_status": res["status"], "orig_opt": res["primal"], "kept_cuts": len(cuts),
                      "cuts_violated_by_optimum": int(nb), "max_scaled_violation": float(max(viol))}), flush=True)
