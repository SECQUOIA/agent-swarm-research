"""Are the cuts produced on the EXPERIMENT instances valid?

For every separated cut of cut_loop (unpatched code) we recompute the true minimum of
omega*gamma - pi.v over the row vertices with the corrected pricing (exact: no merging happens at
these sizes; the corrected pricing is itself checked against brute force in check_pricing.py --patch).
A cut whose constant exceeds that minimum cuts off a row vertex.  For such a cut we then look for a
point feasible for the WHOLE problem that extends the violated row vertex (LP with the row's
variables fixed), set w = f(x) exactly, and evaluate the cleaned model cut there."""
import sys, json, argparse, time
from pathlib import Path
import numpy as np
import gurobipy as gp
from gurobipy import GRB
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "vertex_binarization"))
from instances import transport, netflow, transport_fc
import rowhull.strengthen as S
import rowhull.pricing as pricing
import patched_pricing

ENV = gp.Env(params={"OutputFlag": 0})
orig_compress = pricing._compress


def exact_min(row, pi, omega):
    pricing._compress = patched_pricing._compress
    try:
        lower, cols = pricing.price(row, pi, omega, kmax=10 ** 7)
    finally:
        pricing._compress = orig_compress
    best = min(cols, key=lambda c: c[3])
    return lower, best


def extend(p, row, mask, j, r):
    """Feasible x of the whole problem agreeing with the row vertex, or None."""
    m = gp.Model(env=ENV)
    x = {f"x{i}": m.addVar(lb=f.lo, ub=f.hi) for i, f in enumerate(p.funcs)}
    for q in range(p.A.shape[0]):
        if p.B is not None and np.any(p.B[q] != 0):
            continue
        lhs = gp.quicksum(p.A[q, i] * x[f"x{i}"] for i in range(p.n) if p.A[q, i] != 0)
        s = p.sense[q]
        m.addConstr(lhs <= p.b[q] if s == "<=" else lhs >= p.b[q] if s == ">=" else lhs == p.b[q])
    for k, it in enumerate(row.items):
        if it.var is None:
            continue
        z = it.width if mask >> k & 1 else (r if k == j else 0.0)
        v = it.lo if (z == 0.0 and it.a > 0) or (z == it.width and it.a < 0) else \
            it.hi if (z == it.width and it.a > 0) or (z == 0.0 and it.a < 0) else float(it.v_of_z(z))
        x[it.var].LB = x[it.var].UB = v
    m.optimize()
    if m.Status != GRB.OPTIMAL:
        return None
    return {k: v.X for k, v in x.items()}


def run(p, out):
    rec = []
    real_ctm = S.cut_to_model

    def spy(row, cut):
        rec.append((row, {k: (v.copy() if hasattr(v, "copy") else v) for k, v in cut.items()}))
        return real_ctm(row, cut)

    S.cut_to_model = spy
    t0 = time.time()
    cuts, extra, info = S.cut_loop(p, keep="all")
    S.cut_to_model = real_ctm
    ninv = nconf = 0; worst = worst_pt = 0.0
    badpts = []
    fixed = getattr(p, "fixed_charge", {})
    for row, cut in rec:
        lower, (mask, j, r, val) = exact_min(row, cut["pi"], cut["omega"])
        excess = cut["pi0"] - val          # > 0: the row vertex (mask, j, r) violates the cut
        if excess > 1e-6 * max(1.0, abs(val)):
            ninv += 1; worst = max(worst, excess)
            xv = extend(p, row, mask, j, r)
            if xv is not None:
                val_ = dict(xv)
                for i, f in enumerate(p.funcs):
                    val_[f"w{i}"] = f(xv[f"x{i}"])
                for i, (jj, c) in fixed.items():
                    val_[f"y{jj}"] = 1.0 if xv[f"x{i}"] > 0 else 0.0
                bounds = {k: (-1e9, 1e9) for k in val_}
                coefs, rhs = real_ctm(row, cut)
                scale = max(abs(c) for c in coefs.values())
                v = (rhs - sum(c * val_[k] for k, c in coefs.items())) / scale
                if v > 1e-6:
                    nconf += 1; worst_pt = max(worst_pt, v); badpts.append(val_)
    # the experiments keep only cuts binding at the last root LP: are invalid cuts among the kept ones?
    kept, _, _ = S.cut_loop(p)
    kept_bad = sum(any(rhs - sum(c * pt[k] for k, c in coefs.items()) > 1e-6 for pt in badpts) for coefs, rhs in kept)
    # bound with corrected pricing
    pricing._compress = patched_pricing._compress
    _, _, info2 = S.cut_loop(p, keep="all")
    pricing._compress = orig_compress
    r = {"name": p.name, "cuts_generated": len(rec), "invalid_at_row_vertex": ninv, "worst_excess": worst,
         "confirmed_at_feasible_point_of_problem": nconf, "worst_scaled_violation": worst_pt,
         "kept_cuts": len(kept), "kept_cuts_violated_at_feasible_point": kept_bad, "bound_unpatched": info["bound"], "bound_patched": info2["bound"], "bound0": info["bound0"],
         "cutloop_s": info["time"], "cutloop_patched_s": info2["time"]}
    print(json.dumps(r), flush=True)
    if out:
        out.write(json.dumps(r) + "\n"); out.flush()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", default="small"); ap.add_argument("--out", default=None)
    a = ap.parse_args()
    fh = open(a.out, "a") if a.out else None
    if a.set == "small":
        ps = [transport(8, 12, s, "random", c) for s in range(5) for c in ("quad", "log", "sqrt")]
    elif a.set == "uncap":
        ps = [transport(8, 12, s, "uncap", c) for s in range(5) for c in ("quad",)]
    elif a.set == "net":
        ps = [netflow(40, 3, s, "random", c) for s in range(5) for c in ("quad", "log")]
    elif a.set == "large":
        ps = [transport(10, 15, s, "random", c) for s in range(5) for c in ("quad",)]
    elif a.set == "fc":
        ps = [transport_fc(8, 12, s, "random", c) for s in range(3) for c in ("quad",)]
    for p in ps:
        run(p, fh)
