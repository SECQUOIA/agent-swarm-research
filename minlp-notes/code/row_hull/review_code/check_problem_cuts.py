"""Problem-level validity of cut_loop / closed_form_ir.

For each small instance: sample feasible points of the WHOLE problem (LP vertices under random
objectives, and convex combinations of them), set w_i = f_i(x_i) exactly and y_i = 1[x_i > 0];
check every cut, check that the extended closed-form rows are satisfiable (LP in zeta), and check
root bound <= best sampled vertex value (rigorous upper bound on the optimum) and <= Gurobi optimum
of the original model."""
import sys, argparse, json
from pathlib import Path
import numpy as np
import sympy as sp
import gurobipy as gp
from gurobipy import GRB
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "vertex_binarization"))
from instances import transport, netflow, transport_fc, _concave
from rowhull.strengthen import cut_loop, closed_form_ir
from sob.model import SeparableProblem, original_ir
from sob.functions import X
from sob.backends import solve_gurobi

ENV = gp.Env(params={"OutputFlag": 0})


def custom(seed, decimals=1):
    """Mixed-sign coefficients, shifted bounds, ==, <=, >= rows."""
    rng = np.random.default_rng(seed)
    n, mrows = 8, 4
    funcs = []
    for i in range(n):
        lo = float(np.round(rng.uniform(0, 1), 1)); hi = lo + float(np.round(rng.uniform(1, 5), decimals))
        kind = rng.integers(0, 3)
        c = float(rng.uniform(1, 4))
        if kind == 0:
            b = rng.uniform(0.3, 1.0) / hi
            expr = sp.Float(c) * X - sp.Float(b) * X ** 2
        elif kind == 1:
            expr = sp.Float(c) * sp.sqrt(X)
        else:
            expr = sp.Float(c) * sp.log(1 + X)
        funcs.append(_concave(expr, lo, hi))
    lo = np.array([f.lo for f in funcs]); hi = np.array([f.hi for f in funcs])
    x0 = lo + rng.uniform(0.2, 0.8, n) * (hi - lo)            # a feasible point
    A = np.zeros((mrows, n)); sense = []; b = np.zeros(mrows)
    for r in range(mrows):
        idx = rng.choice(n, 5, replace=False)
        A[r, idx] = rng.choice([-1.0, 1.0, 2.0, -0.5], 5)
        s = ["==", "<=", ">=", "<="][r]
        sense.append(s)
        act = A[r] @ x0
        b[r] = np.round(act, 3) if s == "==" else np.round(act + (0.3 if s == "<=" else -0.3), 2)
    if "==" in sense:                                        # keep x0 feasible after rounding of the == rhs
        r = sense.index("=="); k = np.flatnonzero(A[r])[0]
        x0[k] += (b[r] - A[r] @ x0) / A[r, k]
    return SeparableProblem(f"custom-s{seed}", funcs, A, sense, b), x0


def feas_lp(p):
    m = gp.Model(env=ENV)
    x = [m.addVar(lb=f.lo, ub=f.hi) for f in p.funcs]
    nA = p.A.shape[0]
    fixed = getattr(p, "fixed_charge", {})
    for r in range(nA):
        if p.B is not None and np.any(p.B[r] != 0):
            continue                                        # VUB rows: satisfied by y = 1[x>0]
        lhs = gp.quicksum(p.A[r, i] * x[i] for i in range(p.n) if p.A[r, i] != 0)
        s = p.sense[r]
        m.addConstr(lhs <= p.b[r] if s == "<=" else lhs >= p.b[r] if s == ">=" else lhs == p.b[r])
    m.update()
    return m, x


def sample_points(p, rng, nvert, ncomb):
    m, x = feas_lp(p)
    verts = []
    for _ in range(nvert):
        c = rng.normal(size=p.n) * (rng.random(p.n) < rng.uniform(0.3, 1.0))
        m.setObjective(gp.quicksum(float(c[i]) * x[i] for i in range(p.n)))
        m.optimize()
        if m.Status != GRB.OPTIMAL:
            return [], []
        xv = np.array([v.X for v in x])
        lo = np.array([f.lo for f in p.funcs]); hi = np.array([f.hi for f in p.funcs])
        xv = np.where(np.abs(xv - lo) < 1e-9, lo, np.where(np.abs(xv - hi) < 1e-9, hi, xv))
        verts.append(xv)
    combs = []
    for _ in range(ncomb):
        k = rng.integers(2, 5)
        idx = rng.choice(len(verts), k)
        lam = rng.dirichlet(np.ones(k))
        combs.append(sum(l * verts[i] for l, i in zip(lam, idx)))
    return verts, combs


def point_values(p, xv, y_all_one=False):
    val = {}
    fixed = getattr(p, "fixed_charge", {})
    obj = 0.0
    for i, f in enumerate(p.funcs):
        val[f"x{i}"] = float(xv[i]); val[f"w{i}"] = f(float(xv[i])); obj += val[f"w{i}"]
    if p.B is not None:
        for i, (j, c) in fixed.items():
            val[f"y{j}"] = 1.0 if (xv[i] > 0 or y_all_one) else 0.0
            obj += c * val[f"y{j}"]
    return val, obj


def ext_violation(new_vars, lin, val):
    if not lin:
        return 0.0
    m = gp.Model(env=ENV)
    zv = {k: m.addVar(lb=lb, ub=ub) for k, (lb, ub, _t) in new_vars.items()}
    s = m.addVar(lb=0.0, obj=1.0)
    for rowd, sense, rhs in lin:
        const = sum(c * val[k] for k, c in rowd.items() if k not in zv)
        lhs = gp.quicksum(c * zv[k] for k, c in rowd.items() if k in zv) + const
        scale = max(1.0, max(abs(c) for c in rowd.values()))
        if sense in ("<=", "=="):
            m.addConstr(lhs - scale * s <= rhs)
        if sense in (">=", "=="):
            m.addConstr(lhs + scale * s >= rhs)
    m.optimize()
    return m.ObjVal


def check(p, rng, args, solve=True):
    out = {"name": p.name}
    verts, combs = sample_points(p, rng, args.nvert, args.ncomb)
    if not verts:
        out["skip"] = "infeasible"; return out
    pts = [point_values(p, xv) for xv in verts + combs]
    if p.B is not None:
        pts += [point_values(p, xv, y_all_one=True) for xv in verts[:20]]
    ub = min(o for _, o in pts)
    out["best_sampled"] = ub
    if solve:
        res = solve_gurobi(original_ir(p), 120, threads=2, gap=1e-6)
        out["opt_status"], out["opt_primal"], out["opt_dual"] = res["status"], res["primal"], res["dual"]
    for label, kw in (("cuts", {}), ("cuts_nocf", {"closed_form": False})):
        cuts, extra, info = cut_loop(p, **kw)
        nbad, worst = 0, 0.0
        for coefs, rhs in cuts:
            v = max(rhs - sum(c * val[k] for k, c in coefs.items()) for val, _ in pts)   # coefs scaled to max 1
            if v > 1e-6:
                nbad += 1; worst = max(worst, v)
        extv = max(ext_violation(extra[0], extra[1], val) for val, _ in pts[: args.next]) if extra[1] else 0.0
        out[label] = {"ncuts": len(cuts), "invalid": nbad, "worst": worst, "ext_rows": len(extra[1]), "ext_viol": extv,
                      "bound0": info["bound0"], "bound": info["bound"],
                      "bound_gt_sampled": bool(info["bound"] is not None and info["bound"] > ub + 1e-6 * max(1, abs(ub))),
                      "bound_gt_opt": bool(solve and info["bound"] is not None and out["opt_status"] == "optimal"
                                           and info["bound"] > out["opt_primal"] + 1e-5 * max(1, abs(out["opt_primal"])))}
    ir, info = closed_form_ir(p)
    n0 = len(original_ir(p).lin)
    new_vars = {k: v for k, v in ir.vars.items() if k.startswith("zeta")}
    extv = max(ext_violation(new_vars, ir.lin[n0:], val) for val, _ in pts[: args.next]) if new_vars else 0.0
    out["cf"] = {"rows_used": info["rows_used"], "ext_viol": extv, "bound": info["bound"],
                 "bound_gt_sampled": bool(info["bound"] is not None and info["bound"] > ub + 1e-6 * max(1, abs(ub)))}
    return out


def instances(args):
    for seed in range(args.seeds):
        for cap in ("uniform", "random", "uncap"):
            for cost in ("quad", "log", "sqrt", "pow"):
                for (m, n) in ((3, 4), (4, 5)):
                    yield transport(m, n, seed, cap, cost)
        for cap in ("uniform", "random"):
            for cost in ("quad", "log", "sqrt"):
                yield netflow(8, 2, seed, cap, cost)
            for cost in ("quad", "log"):
                yield transport_fc(3, 4, seed, cap, cost)
        for d in (1, 2):
            yield custom(seed * 10 + d, d)[0]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=3); ap.add_argument("--nvert", type=int, default=150)
    ap.add_argument("--ncomb", type=int, default=150); ap.add_argument("--next", type=int, default=120)
    ap.add_argument("--patch", action="store_true"); ap.add_argument("--out", default=None)
    ap.add_argument("--filter", default="")
    a = ap.parse_args()
    if a.patch:
        from patched_pricing import install; install()
    rng = np.random.default_rng(12345)
    fh = open(a.out, "w") if a.out else None
    tot = {"inst": 0, "cuts": 0, "invalid": 0, "inst_invalid": 0, "bound_bad": 0, "ext_bad": 0}
    for p in instances(a):
        if a.filter and a.filter not in p.name:
            continue
        r = check(p, rng, a)
        if fh:
            fh.write(json.dumps(r) + "\n"); fh.flush()
        if "skip" in r:
            continue
        tot["inst"] += 1
        flag = []
        for lab in ("cuts", "cuts_nocf"):
            tot["cuts"] += r[lab]["ncuts"]; tot["invalid"] += r[lab]["invalid"]
            if r[lab]["invalid"]:
                flag.append(f"{lab}: {r[lab]['invalid']}/{r[lab]['ncuts']} invalid cuts, worst {r[lab]['worst']:.3g}")
            if r[lab]["bound_gt_sampled"] or r[lab]["bound_gt_opt"]:
                flag.append(f"{lab}: bound {r[lab]['bound']:.6f} > optimum {r.get('opt_primal')} (best sampled {r['best_sampled']:.6f})")
                tot["bound_bad"] += 1
            if r[lab]["ext_viol"] > 1e-6:
                flag.append(f"{lab}: extended rows unsatisfiable by {r[lab]['ext_viol']:.3g}"); tot["ext_bad"] += 1
        if r["cf"]["ext_viol"] > 1e-6 or r["cf"]["bound_gt_sampled"]:
            flag.append(f"cf: ext viol {r['cf']['ext_viol']:.3g} bound {r['cf']['bound']}"); tot["ext_bad"] += 1
        tot["inst_invalid"] += bool(flag)
        print(p.name, "OK" if not flag else "PROBLEM: " + "; ".join(flag), flush=True)
    print(tot)
