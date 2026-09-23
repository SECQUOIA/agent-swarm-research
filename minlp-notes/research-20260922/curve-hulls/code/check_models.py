"""Model-level check at the best known MINLPLib point: fix the original variables at the point and
solve the "orig", "sub" and "sub + saved cuts" models (Gurobi); all should be feasible with the same
objective.  Prints an IIS when not.  Cut files that record the scaling (factors, written by run.py) must match
the current model.  python check_models.py <instance> [pb] [cuts file]"""
import sys, json, math, model, run, validate
import gurobipy as gp
name = sys.argv[1]; pb = "pb" in sys.argv[2:]
path = next((p for p in sys.argv[2:] if p.endswith(".json")), f"cuts/{name}{'_pb' if pb else ''}.json")
inst = model.read_osil(model.OSIL.format(name))
if pb: inst.var_lb, inst.var_ub = run.presolve_bounds(name)
det = model.Detected(inst)
sol = validate.sol_values(name)
cutsj = json.load(open(path))
bad = [c for c in cutsj if "factors" in c and c["factors"] != [sc.factor for _, _, sc in det.sel[c["v"]]]]
print(path, "cuts", len(cutsj), "scaling recorded", sum("factors" in c for c in cutsj), "scaling mismatches", len(bad), flush=True)
for variant in ["orig", "sub", "sub+cuts"]:
    B = model.build(name, "orig" if variant == "orig" else "sub", det=det if variant != "orig" else None)
    if variant == "sub+cuts":
        run.add_static(B, [(c["v"], {"c": c["c"], "c0": c["c0"]}) for c in cutsj])
    m = B.m
    for j, x in enumerate(B.x):
        val = sol.get(inst.var_names[j], 0.0)
        x.LB = x.UB = val
    m.Params.TimeLimit = 60
    m.optimize()
    print(variant, "status", m.Status, "obj", m.ObjVal if m.SolCount else None, flush=True)
    if m.Status == 3:
        m.computeIIS()
        names = [c.ConstrName for c in m.getConstrs() if c.IISConstr] + [c.QCName for c in m.getQConstrs() if c.IISQConstr] + \
                [c.GenConstrName for c in m.getGenConstrs() if c.IISGenConstr] + [v.VarName for v in m.getVars() if v.IISLB or v.IISUB]
        print("IIS", names[:20])
