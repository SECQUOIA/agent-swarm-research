"""Print the per-period structure of MINLPLib point p4 of waterno2_06 (exploration)."""
import sys
sys.path.insert(0, "..")
import period, evalpt
from fractions import Fraction
T = 6
D = period.setup(T, "../logs/implied_06.json")
M, S = D["M"], D["S"]
x, obj = evalpt.read_sol("../data/waterno2_06.p4.sol", M["names"])
print("obj", float(obj))
nm = M["names"]
for t in range(T):
    vs = S["per_vars"][t]
    bins = [int(x[v]) for v in vs if M["vt"][v] == "B"]
    cost = sum(float(x[v]) for v in vs if v in M["obj"])
    # demand row: single-variable equality row
    dem = [M["rows"][i] for i in S["per_rows"][t] if len(M["rows"][i]["poly"]) == 1 and M["rows"][i]["lb"] == M["rows"][i]["ub"]]
    Ls = [float(x[b]) for (i, a, b) in S["link"][t - 1]] if t > 0 else None
    Le = [float(x[a]) for (i, a, b) in S["link"][t]] if t < T - 1 else None
    h = [float(x[v]) for v in D["hor"] if D["per_of"][v] == t][0]
    print(t, "cost %.4f" % cost, "bins", bins, "QA %.5f" % h, "Ls", Ls, "Le", Le,
          "dem", [(r["name"], r["lb"], [nm[m[0]] for m in r["poly"]]) for r in dem])
print("horizon rhs", D["hor_rhs"], "sum QA", sum(float(x[v]) for v in D["hor"]))
