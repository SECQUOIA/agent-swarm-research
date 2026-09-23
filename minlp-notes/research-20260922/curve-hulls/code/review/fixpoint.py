"""Fix the MINLPLib best point (sols/) in (a) reviewer's orig, sub, sub+cuts models and (b) the author's
model.py sub + cuts model; report status and objective.  python fixpoint.py <instance>"""
import glob, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import rbuild

name = sys.argv[1]
solf = glob.glob(os.path.join(HERE, "..", "sols", f"{name}.p*.sol"))
assert len(solf) == 1, solf
sol = {}
for line in open(solf[0]):
    p = line.split()
    if len(p) >= 2:
        sol[p[0]] = float(p[1])
cuts = json.load(open(os.path.join(HERE, "..", "cuts", f"{name}.json")))
P = rbuild.parse(name)
missing = [d["name"] for d in P["V"] if d["name"] not in sol]
print(name, os.path.basename(solf[0]), "objvar in sol:", sol.get("objvar"), "vars missing from sol (set 0):", len(missing))


def fix(m, xs, names):
    for v, n in zip(xs, names):
        val = sol.get(n, 0.0)
        v.LB = v.UB = val
    m.Params.TimeLimit = 120
    m.Params.FeasibilityTol = 1e-6
    m.optimize()
    return m.Status, (m.ObjVal if m.SolCount else None)


names = [d["name"] for d in P["V"]]
for mode in ["orig", "sub", "sub+cuts"]:
    m, x, y, z, _ = rbuild.build(name, "orig" if mode == "orig" else "sub", P=P)
    if mode == "sub+cuts":
        rbuild.add_cuts(m, x, y, z, cuts)
    print("reviewer", mode, fix(m, x, names), flush=True)

# author's model.py, sub + saved cuts via run.add_static
import model, run
B = model.build(name, "sub")
run.add_static(B, [(c["v"], {"c": c["c"], "c0": c["c0"]}) for c in cuts])
print("author sub+cuts", fix(B.m, B.x, B.inst.var_names), flush=True)
