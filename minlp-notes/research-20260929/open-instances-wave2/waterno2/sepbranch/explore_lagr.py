"""Lagrangian period solutions at the wave-2 multipliers (SCIP, exploration only)."""
import sys, json
sys.path.insert(0, "..")
import period, bundle
T = int(sys.argv[1]); mult = sys.argv[2]; impl = sys.argv[3]
D = period.setup(T, impl)
k = json.load(open(mult))
lam, mu = k["lam"], k["mu"]
M, S = D["M"], D["S"]
tot = mu * float(D["hor_rhs"])
for t in range(T):
    r = period.solve_window(D, t, t + 1, lam, mu, 120, bundle.NOPROP)
    x = r["x"]
    vs = S["per_vars"][t]
    bins = [int(round(x[v])) for v in vs if M["vt"][v] == "B"]
    cost = sum(x[v] for v in vs if v in M["obj"])
    Ls = ["%.3f" % x[b] for (i, a, b) in S["link"][t - 1]] if t > 0 else None
    Le = ["%.3f" % x[a] for (i, a, b) in S["link"][t]] if t < T - 1 else None
    h = [x[v] for v in D["hor"] if D["per_of"][v] == t][0]
    tot += r["dual"]
    print(t, "phi %.4f" % r["dual"], bins, "cost %.3f" % cost, "QA %.4f" % h, "Ls", Ls, "Le", Le, flush=True)
print("L =", tot)
