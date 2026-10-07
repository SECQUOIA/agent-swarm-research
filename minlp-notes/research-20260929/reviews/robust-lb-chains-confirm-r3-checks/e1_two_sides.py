"""Referee check (round 3 confirmation) of robust-chains.md, Section 4.6.

Independent code (shares nothing with chains/ or earlier review checks).
Chiral chain f_n = sum_i a x_i^2 + b sum_i x_i x_{i+1} + (g/2) sum_i x_i x_{i+1} (x_{i+1} - x_i),
(b, g, ev) = (0.6, 0.3, 0.05), a = b + ev, on [-1, 1]^n, f* = 0.

Two routes for each placement:
  sos : maximize gamma s.t. f_n - gamma = sum_e sigma_e(x_e, x_{e+1}) (deg 4 SOS on pair cliques)
        + sum (SOS multiplier) * constraint + sum lam_alpha * p_alpha  (lam >= 0 for linear moment bounds)
        coefficient matching on n-variate monomials (global polynomial ring).
  mom : one global moment vector y indexed by n-variate exponents; clique moment matrices, localizing matrices,
        linear moment bounds.

Placements:
  uni   : linear box constraints 1 -+ x_i, univariate SOS multiplier in basis (1, x_i)  (Waki et al. (20))
  opp   : 1 - x_i in clique (i-1, i), 1 + x_i in clique (i, i+1) (ends: the only clique), multiplier basis (1, x_e, x_f)
  match : 1 - x_i in clique (i, i+1), 1 + x_i in clique (i-1, i)   (case (b), control)
Moment bounds:
  zb : 0 <= L(z^alpha) <= 1, z = (1 + x)/2, every clique monomial of degree 1..4 (Waki et al. Section 5.6)
  yb : |L(x^alpha)| <= 1, every clique monomial of degree 1..4
Ball: 2M^2 - x_e^2 - x_f^2 in every clique, multiplier basis (1, x_e, x_f).
Floating point (Clarabel; SCS where stated).
"""
import sys
import json
import itertools
from math import comb

import cvxpy as cp

B, G, EV = 0.6, 0.3, 0.05
A = B + EV


def mono(n, pairs):
    e = [0] * n
    for i, p in pairs:
        e[i] += p
    return tuple(e)


def add(t1, t2):
    return tuple(a + b for a, b in zip(t1, t2))


def objective_poly(n):
    f = {}
    def put(k, c):
        f[k] = f.get(k, 0.0) + c
    for i in range(n):
        put(mono(n, [(i, 2)]), A)
    for i in range(n - 1):
        put(mono(n, [(i, 1), (i + 1, 1)]), B)
        put(mono(n, [(i, 1), (i + 1, 2)]), G / 2)
        put(mono(n, [(i, 2), (i + 1, 1)]), -G / 2)
    return f


def clique_monos(n, e, maxdeg):
    return [mono(n, [(e, p), (e + 1, q)]) for d in range(maxdeg + 1) for p in range(d + 1) for q in [d - p]]


def zpoly(n, e, p, q):
    # z_e^p z_{e+1}^q with z = (1 + x)/2, as {exponent: coef}
    out = {}
    for r in range(p + 1):
        for s in range(q + 1):
            k = mono(n, [(e, r), (e + 1, s)])
            out[k] = out.get(k, 0.0) + comb(p, r) * comb(q, s) / 2 ** (p + q)
    return out


def constraints_list(n, place, ball):
    """Return list of (basis, poly) for localized constraints; poly as {exp: coef}."""
    out = []
    zero = tuple([0] * n)
    def lin(i, s):  # 1 + s x_i
        return {zero: 1.0, mono(n, [(i, 1)]): float(s)}
    def cb(e):
        return [zero, mono(n, [(e, 1)]), mono(n, [(e + 1, 1)])]
    for i in range(n):
        if place == "uni":
            ub = [zero, mono(n, [(i, 1)])]
            out.append((ub, lin(i, -1)))
            out.append((ub, lin(i, +1)))
        elif place in ("opp", "match"):
            left = i - 1 if i >= 1 else 0          # clique (i-1, i) 0-based index i-1
            right = i if i <= n - 2 else n - 2     # clique (i, i+1)
            if place == "opp":
                out.append((cb(left), lin(i, -1)))
                out.append((cb(right), lin(i, +1)))
            else:
                out.append((cb(right), lin(i, -1)))
                out.append((cb(left), lin(i, +1)))
        else:
            raise ValueError(place)
    if ball is not None:
        for e in range(n - 1):
            out.append((cb(e), {zero: 2 * ball ** 2, mono(n, [(e, 2)]): -1.0, mono(n, [(e + 1, 2)]): -1.0}))
    return out


def bound_polys(n, bounds):
    """Linear moment bounds as polynomials p with L(p) >= 0."""
    zero = tuple([0] * n)
    out = []
    for e in range(n - 1):
        for d in range(1, 5):
            for p in range(d + 1):
                q = d - p
                if bounds == "zb":
                    zp = zpoly(n, e, p, q)
                    out.append(zp)
                    neg = {k: -v for k, v in zp.items()}
                    neg[zero] = neg.get(zero, 0.0) + 1.0
                    out.append(neg)
                elif bounds == "yb":
                    k = mono(n, [(e, p), (e + 1, q)])
                    out.append({zero: 1.0, k: 1.0})
                    out.append({zero: 1.0, k: -1.0})
    return out


def sos_side(n, place, ball=None, bounds=None, solver="CLARABEL"):
    zero = tuple([0] * n)
    acc = {}
    def put(k, expr):
        acc.setdefault(k, []).append(expr)
    cons = []
    gamma = cp.Variable()
    put(zero, gamma)
    for e in range(n - 1):
        basis = clique_monos(n, e, 2)
        Q = cp.Variable((len(basis), len(basis)), PSD=True)
        for i, j in itertools.product(range(len(basis)), repeat=2):
            put(add(basis[i], basis[j]), Q[i, j])
    for basis, poly in constraints_list(n, place, ball):
        Q = cp.Variable((len(basis), len(basis)), PSD=True)
        for i, j in itertools.product(range(len(basis)), repeat=2):
            for k, c in poly.items():
                put(add(add(basis[i], basis[j]), k), c * Q[i, j])
    if bounds:
        bp = bound_polys(n, bounds)
        lam = cp.Variable(len(bp), nonneg=True)
        for t, poly in enumerate(bp):
            for k, c in poly.items():
                put(k, c * lam[t])
    f = objective_poly(n)
    keys = set(acc) | set(f)
    for k in keys:
        cons.append(cp.sum(cp.hstack(acc.get(k, [cp.Constant(0.0)]))) == f.get(k, 0.0))
    prob = cp.Problem(cp.Maximize(gamma), cons)
    kw = dict(eps=1e-9, max_iters=300000) if solver == "SCS" else {}
    prob.solve(solver=solver, **kw)
    return prob.status, (None if prob.value is None else float(f"{prob.value:.7g}"))


def mom_side(n, place, ball=None, bounds=None, solver="CLARABEL"):
    zero = tuple([0] * n)
    y = {}
    def Y(k):
        if k == zero:
            return 1.0
        if k not in y:
            y[k] = cp.Variable()
        return y[k]
    cons = []
    def L(poly):
        return sum(c * Y(k) for k, c in poly.items())
    def psd_loc(basis, poly):
        m = len(basis)
        rows = [[L({add(add(basis[i], basis[j]), k): c for k, c in poly.items()}) for j in range(m)] for i in range(m)]
        Mx = cp.bmat([[r if isinstance(r, cp.Expression) else cp.Constant(r) for r in row] for row in rows])
        S = cp.Variable((m, m), PSD=True)
        cons.append(S == Mx)
    for e in range(n - 1):
        psd_loc(clique_monos(n, e, 2), {zero: 1.0})
    for basis, poly in constraints_list(n, place, ball):
        psd_loc(basis, poly)
    if bounds:
        for poly in bound_polys(n, bounds):
            cons.append(L(poly) >= 0)
    obj = L(objective_poly(n))
    prob = cp.Problem(cp.Minimize(obj), cons)
    kw = dict(eps=1e-9, max_iters=300000) if solver == "SCS" else {}
    prob.solve(solver=solver, **kw)
    return prob.status, (None if prob.value is None else float(f"{prob.value:.7g}"))


def run(n, place, ball=None, bounds=None, sides=("sos", "mom"), scs=False):
    out = dict(n=n, place=place, ball=ball, bounds=bounds)
    for side in sides:
        fn = sos_side if side == "sos" else mom_side
        for solver in ["CLARABEL"] + (["SCS"] if scs else []):
            try:
                out[f"{side}_{solver}"] = fn(n, place, ball, bounds, solver)
            except Exception as exc:  # noqa: BLE001
                out[f"{side}_{solver}"] = ("error", str(exc)[:100])
    print(json.dumps(out), flush=True)


if __name__ == "__main__":
    what = sys.argv[1]
    if what == "waki":
        for n in (5, 8):
            run(n, "uni", bounds="zb", scs=True)
            run(n, "opp", bounds="zb", scs=True)
            run(n, "uni", bounds="yb")
            run(n, "match", bounds="zb")
            run(n, "opp")
    elif what == "radius":
        for M, n in [(1.5, 16), (1.5, 32), (2.0, 16), (2.0, 32), (1.7, 8), (1.7, 32)]:
            run(n, "opp", ball=M)
    elif what == "monotone":
        # value is nonincreasing in M (feasible set grows); sample M at n = 8 and n = 16
        for n in (8, 16):
            for M in (1.5, 1.6, 1.7, 1.8, 1.9, 2.0):
                run(n, "opp", ball=M, sides=("mom",))
