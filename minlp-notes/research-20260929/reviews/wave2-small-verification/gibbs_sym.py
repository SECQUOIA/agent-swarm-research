"""Gibbs instances (ex6_2_7, ex6_2_5): exact symbolic structure checks (sympy,
exact rationals from the OSIL decimals).

Checks
  * the 3 rows are sum_p n_{p,i} = b_i;
  * phase separability: every objective term uses variables of one phase only;
  * which phases are identical (after renaming);
  * the scaling identity G_p(t y) = t G_p(y) + t ln t R_p(y), with R_p derived
    as R_p(y) = t * d/dt [G_p(t y)/t] and checked to be independent of t and linear.
Exports phase functions for the numeric scripts.
"""
import sys

import sympy as sp

import common


def to_sym(t, X):
    op = t[0]
    if op == "num":
        return sp.Rational(t[1])
    if op == "var":
        return sp.Rational(t[2]) * X[t[1]]
    a = [to_sym(c, X) for c in t[1:]]
    if op in ("sum", "plus"):
        return sp.Add(*a)
    if op in ("product", "times"):
        return sp.Mul(*a)
    if op == "minus":
        return a[0] - a[1]
    if op == "negate":
        return -a[0]
    if op == "divide":
        return a[0] / a[1]
    if op == "ln":
        return sp.log(a[0])
    if op == "square":
        return a[0] ** 2
    raise NotImplementedError(op)


def varsof(t, acc):
    if t[0] == "var":
        acc.add(t[1])
    elif t[0] != "num":
        for c in t[1:]:
            varsof(c, acc)
    return acc


def analyse(name, verbose=True):
    m = common.load(name)
    n = len(m["names"])
    assert n == 9
    X = sp.symbols("x0:9", positive=True)
    # rows: sum over phases of component i equals b_i ; phase p = (x_p, x_{3+p}, x_{6+p})
    b = []
    for i, row in enumerate(m["cons"]):
        assert row["lb"] == row["ub"] and row["constant"] == "0" and not row["quad"] and row["nl"] is None
        assert row["lin"] == {3 * i: "1", 3 * i + 1: "1", 3 * i + 2: "1"}, row["lin"]
        b.append(row["lb"])
    for j in range(n):
        assert m["lb"][j] == "1e-7" and m["ub"][j] == b[j // 3]
    phases = [(p, 3 + p, 6 + p) for p in range(3)]
    o = m["obj"]
    assert o["constant"] == "0" and o["lin"] == {} and not o["quad"] and o["sense"] == "min"
    terms = o["nl"][1:]
    assert o["nl"][0] == "sum"
    parts = {p: [] for p in range(3)}
    for t in terms:
        vs = varsof(t, set())
        ph = {v % 3 for v in vs}
        assert len(ph) == 1, ("term mixes phases", t)
        parts[ph.pop()].append(t)
    y = sp.symbols("y1:4", positive=True)
    G = {}
    for p in range(3):
        e = sp.Add(*[to_sym(t, X) for t in parts[p]])
        # rename phase-p variables to (y1, y2, y3)
        G[p] = sp.expand(e.subs({X[phases[p][i]]: y[i] for i in range(3)}))
    same = {(p, q): sp.simplify(G[p] - G[q]) == 0 for p in range(3) for q in range(p + 1, 3)}
    tt = sp.symbols("t", positive=True)
    R = {}
    for p in range(3):
        Gt = G[p].subs({y[i]: tt * y[i] for i in range(3)}, simultaneous=True)
        Gt = sp.expand(sp.expand_log(Gt, force=True))
        Rp = sp.simplify(sp.expand(sp.expand_log(tt * sp.diff(Gt / tt, tt), force=True)))
        assert tt not in Rp.free_symbols, Rp
        poly = sp.Poly(Rp, *y)
        assert poly.total_degree() <= 1 and poly.coeff_monomial(1) == 0
        # full identity check: G(ty) - t G(y) - t ln t R(y) == 0
        ident = sp.simplify(sp.expand(sp.expand_log(Gt - tt * G[p] - tt * sp.log(tt) * Rp, force=True)))
        assert ident == 0, ident
        R[p] = [poly.coeff_monomial(y[i]) for i in range(3)]
    if verbose:
        print(name, "b =", b, "terms per phase:", {p: len(parts[p]) for p in range(3)})
        print("  identical phases:", same)
        print("  R_p coefficients:", {p: [str(c) for c in R[p]] for p in range(3)})
    return dict(m=m, b=b, G=G, y=y, R=R, same=same, parts=parts, phases=phases)


if __name__ == "__main__":
    for nm in sys.argv[1:] or ["ex6_2_7", "ex6_2_5"]:
        analyse(nm)
