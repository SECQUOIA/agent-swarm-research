"""Rerun gurobi_link.py unchanged (its own source, its own optimize()) and check the returned incumbent against the
ORIGINAL OSiL model with the plain-float evaluator of note_model_point_check.py (osil_eval.Model.check).
python rerun_point_check.py <instance> <mode> [tl] [threads]   -> one JSON line on stdout"""
import contextlib, io, json, sys
from pathlib import Path
D = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent)); sys.path.insert(0, str(D))
from osil_eval import Model

args = sys.argv[1:]
sys.argv = ["gurobi_link.py", *args]
g = {"__name__": "gl", "__file__": str(D / "gurobi_link.py")}
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(compile(open(D / "gurobi_link.py").read(), str(D / "gurobi_link.py"), "exec"), g)
rec = json.loads([l for l in buf.getvalue().splitlines() if l.startswith("{")][-1])
m, x = g["m"], g["x"]
if m.SolCount:
    pt = [v.X for v in x]
    chk = Model(args[0]).check(pt)
    rec.update({"solver_MaxVio": m.MaxVio, "solver_ConstrVio": m.ConstrVio,
                "orig_obj": chk["obj"], "orig_row_viol": chk["row"], "orig_row_viol_rel": chk["row_rel"],
                "orig_worst_row": chk["worst_row"], "orig_bound_viol": chk["bound"], "orig_int_viol": chk["int"], "x": pt})
print(json.dumps(rec))
