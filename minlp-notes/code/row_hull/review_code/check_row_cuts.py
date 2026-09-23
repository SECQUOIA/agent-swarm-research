"""Row-level validity: RowSeparator + cut_to_model + clean_cut, and closed_form_rows, checked in MODEL
variables against every vertex of the row polytope with the TRUE functions (t = f(v), fixed charge
t = g(v) + c*1[v>0] with y = 1[v>0]).  Rows: mixed signs, shifted bounds, ==/<=/>=, decimal widths."""
import sys, argparse
from pathlib import Path
import numpy as np
import gurobipy as gp
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rowhull.rows import normalize_row
from rowhull.separate import RowSeparator, cut_to_model
from rowhull.closedform import closed_form_rows
from rowhull.strengthen import clean_cut, _row_point
import rowhull.pricing as pricing

ENV = gp.Env(params={"OutputFlag": 0})


def make_row(rng, n, sense, decimals, fc, equal):
    entries, truef = [], {}
    for i in range(n):
        if fc:
            lo = 0.0
        else:
            lo = float(np.round(rng.uniform(-1, 1), 1))
        wdt = 1.0 if equal else float(np.round(rng.uniform(1, 6), decimals))
        a = 1.0 if equal else float(rng.choice([-1.0, 1.0]) * rng.choice([1.0, 1.0, 2.0, 0.5]))
        hi = lo + wdt / abs(a)
        kind = rng.integers(0, 4)
        q = float(rng.uniform(0.5, 2)); s = float(rng.uniform(-1, 1)); c = float(rng.uniform(0.5, 2))
        if kind == 3:
            entries.append((f"x{i}", a, lo, hi, None, None)); continue
        if kind == 0:
            g = lambda v, q=q, s=s: -q * np.asarray(v, float) ** 2 + s * np.asarray(v, float)
        elif kind == 1:
            g = lambda v, q=q, lo=lo: q * np.sqrt(np.maximum(np.asarray(v, float) - lo, 0.0))
        else:
            g = lambda v, q=q, lo=lo: q * np.log1p(2.0 * (np.asarray(v, float) - lo))
        if fc and kind != 0:   # fixed charge needs g(0)=0: sqrt/log with lo=0 qualify
            u = hi
            f_code = lambda v, g=g, c=c, u=u: np.asarray(g(v), float) + c * (np.asarray(v) > 1e-9 * u)
            entries.append((f"x{i}", a, lo, hi, {f"w{i}": 1.0, f"y{i}": c}, f_code))
            truef[i] = ("fc", g, c)
        else:
            entries.append((f"x{i}", a, lo, hi, f"w{i}", g))
            truef[i] = ("plain", g, 0.0)
    const = sum(a * (lo if a > 0 else hi) for _, a, lo, hi, _, _ in entries)
    total = sum(abs(a) * (hi - lo) for _, a, lo, hi, _, _ in entries)
    B = float(np.round(total * rng.uniform(0.15, 0.85), decimals + 1))
    if equal:
        B = float(np.floor(B) + rng.choice([0.25, 0.5, 0.7]))
    return normalize_row(entries, sense, const + B), entries, truef


def model_vertices(row, truef):
    """All vertices of the row polytope as dicts of model values (x, w, y) with true functions."""
    n, B, w = row.n, row.B, row.widths
    out = []
    seen = set()
    for mask in range(1 << n):
        tot = sum(w[i] for i in range(n) if mask >> i & 1)
        r = B - tot
        for j in range(n):
            if mask >> j & 1 or not (-1e-9 <= r <= w[j] + 1e-9):
                continue
            z = np.array([w[i] if mask >> i & 1 else 0.0 for i in range(n)]); z[j] = min(max(r, 0.0), w[j])
            key = tuple(np.round(z, 9))
            if key in seen:
                continue
            seen.add(key)
            val = {}
            for k, it in enumerate(row.items):
                if it.var is None:
                    continue
                # exact endpoints, to evaluate the true function at the true bound
                v = it.lo if (z[k] == 0.0 and it.a > 0) or (z[k] == w[k] and it.a < 0) else \
                    it.hi if (z[k] == w[k] and it.a > 0) or (z[k] == 0.0 and it.a < 0) else float(it.v_of_z(z[k]))
                val[it.var] = v
                i = int(it.var[1:])
                if i in truef:
                    kind, g, c = truef[i]
                    val[f"w{i}"] = float(g(v))
                    if kind == "fc":
                        val[f"y{i}"] = 1.0 if v > 0 else 0.0
            out.append(val)
    return out


def check_extended(new_vars, lin, val):
    """min max-violation of the extended rows over zeta with model values fixed."""
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


def run(args):
    rng = np.random.default_rng(args.seed)
    ncut = nbad = ncf = ncfbad = 0
    worst = worstcf = 0.0
    for t in range(args.trials):
        sense = ["==", "<=", ">="][t % 3]
        n = int(rng.integers(4, args.nmax + 1))
        fc = (t % 4 == 3)
        equal = (t % 5 == 4)
        row, entries, truef = make_row(rng, n, sense, args.decimals, fc, equal)
        if row is None:
            continue
        V = model_vertices(row, truef)
        if not V:
            continue
        bounds = {}
        for var, a, lo, hi, tvar, f in entries:
            bounds[var] = (lo, hi); i = int(var[1:])
            bounds[f"w{i}"] = (-1e3, 1e3); bounds[f"y{i}"] = (0.0, 1.0)
        # closed form
        cf = closed_form_rows(row, "t")
        if cf is not None:
            ncf += 1
            viol = max(check_extended(cf[0], cf[1], val) for val in V)
            worstcf = max(worstcf, viol)
            if viol > 1e-6:
                ncfbad += 1
                print(f"  CLOSED FORM violated: trial {t} sense {sense} fc {fc} equal {equal} viol {viol:.3g}")
        # separation at random points: random convex combination of vertices, with w shrunk toward the chord
        sep = RowSeparator(row, env=ENV)
        for _ in range(args.points):
            lam = rng.dirichlet(np.ones(len(V)) * 0.3)
            val = {k: sum(l * v.get(k, 0.0) for l, v in zip(lam, V)) for k in set().union(*V)}
            zhat, tp = _row_point(row, val)
            sh = rng.uniform(0, 1.0)
            tp = {k: sh * x for k, x in tp.items()}
            cut = sep.separate(zhat, tp, 1e-6)
            if cut is None:
                continue
            for cleaned in (False, True):
                coefs, rhs = cut_to_model(row, cut)
                if cleaned:
                    cc = clean_cut(coefs, rhs, bounds)
                    if cc is None:
                        continue
                    coefs, rhs = cc
                scale = max(abs(c) for c in coefs.values())
                v_ = max((rhs - sum(c * val_[k] for k, c in coefs.items())) / scale for val_ in V)
                ncut += 1
                if v_ > 1e-6:
                    nbad += 1; worst = max(worst, v_)
    print(f"decimals={args.decimals} patched={args.patch}: cuts checked {ncut}, INVALID {nbad} (worst scaled violation {worst:.3g}); "
          f"closed-form systems {ncf}, violated {ncfbad} (worst {worstcf:.3g})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=120); ap.add_argument("--points", type=int, default=8)
    ap.add_argument("--nmax", type=int, default=9); ap.add_argument("--decimals", type=int, default=1)
    ap.add_argument("--seed", type=int, default=0); ap.add_argument("--patch", action="store_true")
    a = ap.parse_args()
    if a.patch:
        from patched_pricing import install; install()
    run(a)
