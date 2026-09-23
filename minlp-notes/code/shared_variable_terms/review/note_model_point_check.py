"""Task 1: faithfulness of gurobi_link.py's translation.  Build the note's Gurobi model by executing gurobi_link.py's
own code (with optimize() removed), fix every original variable to the native incumbent found by the reviewer's builder,
and let Gurobi report whether the note's model accepts the point and with which objective.  Also the linked model.
python note_model_point_check.py <instances...>"""
import json, math, sys, re
from pathlib import Path
D = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent)); sys.path.insert(0, str(D))
from gmodel import build
src = open(D / "gurobi_link.py").read()
src = src.replace("t0 = time.time(); m.optimize()", "t0 = time.time()")
src = re.sub(r'print\(json\.dumps\(\{"name".*', "", src, flags=re.S)
for name in sys.argv[1:]:
    M, mine, x, _, _ = build(name, linked=False)
    mine.Params.TimeLimit = 60; mine.Params.Threads = 2; mine.Params.MIPGap = 1e-4; mine.optimize()
    if not mine.SolCount: print(name, "no point"); continue
    pt = [v.X for v in x]; chk = M.check(pt)
    for mode in ("native", "linked"):
        g = {"__name__": "gl", "__file__": str(D / "gurobi_link.py")}
        sys.argv = ["gurobi_link.py", name, mode, "60", "1"]
        exec(compile(src, str(D / "gurobi_link.py"), "exec"), g)
        m, xs = g["m"], g["x"]
        for v, val in zip(xs, pt): v.LB = v.UB = val
        m.Params.Threads = 1; m.Params.TimeLimit = 60; m.Params.OutputFlag = 0; m.optimize()
        print(json.dumps({"name": name, "note_model": mode, "status": m.Status, "obj_note_model": m.ObjVal if m.SolCount else None,
                          "obj_evaluator": chk["obj"], "evaluator_row_viol": chk["row"], "gurobi_ConstrVio": m.ConstrVio if m.SolCount else None,
                          "n_note_vars": m.NumVars, "n_note_constrs": m.NumConstrs, "n_note_genconstrs": m.NumGenConstrs}))
