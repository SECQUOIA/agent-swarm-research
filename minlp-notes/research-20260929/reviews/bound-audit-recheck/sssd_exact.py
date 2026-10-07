"""Exactly feasible points for sssd*persp instances from a listed point's binaries (own code).

Structure used to construct the point (every piece is asserted from the OSIL file):
  * binaries b; continuous "utilization" variables u (each in exactly one link row u - b <= 0
    and in exactly one load equality) and "queue" variables q (objective only, plus quadratic rows);
  * load equalities:  sum_i a_i b_i - sum_l c_l u_l = 0   (binaries and u only);
  * quadratic rows:   -b q + b u + q u <= 0               (one b, one q, one u each);
  * all other rows involve binaries only.
With b fixed, u_l = 0 whenever its link binary is 0, and the load equality then fixes the one
u_l whose link binary is 1 (or requires the binary part to be 0 if none is). A quadratic row with
b = 1 reads q (u - 1) + u <= 0, i.e. q >= u / (1 - u) for u < 1; with b = 0 it reads q u <= 0,
which holds because u = 0. So q := max(0, u/(1 - u) over its rows with b = 1) is the least
feasible q, and the objective (linear, positive q coefficients) is the optimum for these binaries.

The construction is only a way to produce a candidate. The proof is the final step: every row,
bound and integrality condition of the full OSIL model is checked in exact rational arithmetic,
and the objective is evaluated exactly.

Usage: python3 sssd_exact.py name.pK[=listed_dual] ...
"""
import os
import sys
from fractions import Fraction as F

import qosil

HERE = os.path.dirname(os.path.abspath(__file__))


def slack(d):
    """Half a unit in the last shown digit of the displayed decimal d, at least half a unit in
    the 10th significant digit (the audit's rule, restated)."""
    s = d.strip().lstrip("+-")
    mant = s.split("e")[0]
    dec = len(mant.split(".")[1]) if "." in mant else 0
    last = F(1, 10 ** dec)
    v = abs(F(d))
    if v == 0:
        return F(5, 10 ** 9)
    # exponent of the leading digit
    e = 0
    while F(10) ** (e + 1) <= v:
        e += 1
    while F(10) ** e > v:
        e -= 1
    tenth = F(10) ** (e - 9)
    return max(last, tenth) / 2


def build(M, xs):
    B = [j for j in range(M.n) if M.type[j] == "B"]
    Bset = set(B)
    assert all(M.type[j] in ("B", "C") for j in range(M.n))
    C = [j for j in range(M.n) if M.type[j] == "C"]
    assert all(M.lb[j] == 0 and M.ub[j] is None for j in C)
    assert M.sense == "min" and M.obj_const == 0 and not M.obj_Q
    x = [None] * M.n
    worst_int = F(0)
    for j in B:
        r = F(round(xs[j]))
        worst_int = max(worst_int, abs(xs[j] - r))
        assert abs(xs[j] - r) <= F(1, 10 ** 9)
        x[j] = r
    # classify rows
    link, load, quad = {}, [], []
    for i in range(M.m):
        vs = set(M.A[i]) | {a for a, b, c in M.Q[i]} | {b for a, b, c in M.Q[i]}
        cont = [j for j in vs if j not in Bset]
        if not cont:
            continue
        if M.Q[i]:
            assert not M.A[i] and M.cconst[i] == 0 and M.clb[i] is None and M.cub[i] == 0
            assert len(M.Q[i]) == 3
            quad.append(i)
        elif len(M.A[i]) == 2 and len(cont) == 1:
            (u,) = cont
            (b,) = [j for j in M.A[i] if j in Bset]
            assert M.A[i][u] == 1 and M.A[i][b] == -1 and M.cub[i] == 0 and M.clb[i] is None and M.cconst[i] == 0
            assert u not in link
            link[u] = b
        else:
            assert M.clb[i] == 0 and M.cub[i] == 0 and M.cconst[i] == 0
            load.append(i)
    U = set(link)
    Qv = set(C) - U
    assert set(M.obj_lin) <= Bset | Qv and all(M.obj_lin.get(q, F(1)) > 0 for q in Qv)
    # utilization variables from the load equalities
    seen = set()
    for i in load:
        us = [j for j in M.A[i] if j not in Bset]
        assert set(us) <= U and not (set(us) & seen)
        seen |= set(us)
        bin_part = sum((M.A[i][j] * x[j] for j in M.A[i] if j in Bset), F(0))
        on = [u for u in us if x[link[u]] == 1]
        for u in us:
            x[u] = F(0)
        assert len(on) <= 1
        if on:
            u = on[0]
            x[u] = -bin_part / M.A[i][u]
        else:
            assert bin_part == 0
    assert seen == U
    # queue variables: least value allowed by the quadratic rows
    for q in Qv:
        x[q] = F(0)
    for i in quad:
        terms = {(min(a, b), max(a, b)): c for a, b, c in M.Q[i]}
        vs = {a for k in terms for a in k}
        (b,) = [j for j in vs if j in Bset]
        (u,) = [j for j in vs if j in U]
        (q,) = [j for j in vs if j in Qv]
        assert terms == {tuple(sorted((b, q))): -1, tuple(sorted((b, u))): 1, tuple(sorted((q, u))): 1}
        if x[b] == 1:
            assert x[u] < 1
            x[q] = max(x[q], x[u] / (1 - x[u]))
    assert all(v is not None for v in x)
    return x, worst_int, U, Qv


def main(arg):
    tag, _, d = arg.partition("=")
    name, pt = tag.rsplit(".", 1)
    M = qosil.Model(os.path.join(HERE, "data", name + ".osil"))
    xs, missing, unknown = qosil.read_sol(os.path.join(HERE, "data", f"{name}.{pt}.sol"), M)
    xs = [v if v is not None else F(0) for v in xs]  # missing entries are 0 (reported below)
    x, worst_int, U, Qv = build(M, xs)
    viol = M.violations(x)
    f = M.objective(x)
    listed_f = M.objective(xs)
    listed_viol = max((v for v, _, _ in M.violations(xs)), default=F(0))
    dev = max(abs(x[j] - xs[j]) for j in range(M.n))
    print(f"{name}.{pt}: {M.n} vars, {M.m} rows; {len(U)} utilization and {len(Qv)} queue variables; "
          f"missing in .sol: {len(missing)} ({', '.join(missing[:5])}); unknown names: {unknown}")
    print(f"  listed point: exact objective {float(listed_f)!r}, largest exact violation {float(listed_viol):.3g}; "
          f"binaries off 0/1 by at most {float(worst_int):.3g}")
    print(f"  constructed point: {len(viol)} exact violations; max |x - listed| = {float(dev):.3g}")
    assert not viol, viol[:5]
    print(f"  EXACTLY FEASIBLE, objective = {f.numerator}/{f.denominator}")
    print(f"  objective (truncated to 25 decimals) = {fmt(f)}")
    if d:
        dd, sl = F(d), slack(d)
        margin = dd - f
        verdict = "INVALID (class (i))" if margin > sl else ("within rounding slack (i-r)" if margin > 0 else "not beyond d")
        print(f"  listed dual d = {d}: d - f = {float(margin):.6g}, (d - f)/|d| = {float(margin / abs(dd)):.3g}, "
              f"slack {float(sl):.1g}, margin/slack = {float(margin / sl):.4g}, 1e-6|d| = {float(abs(dd) / 10**6):.3g} "
              f"-> {verdict}; {'gross' if margin > abs(dd) / 10**6 else 'tolerance-scale'}")
    return f


def fmt(f, digits=25):
    """Decimal string of the Fraction f truncated toward -inf to `digits` decimals."""
    s = -1 if f < 0 else 1
    a = abs(f)
    ip = a.numerator // a.denominator
    fr = a - ip
    dec = (fr.numerator * 10 ** digits) // fr.denominator
    return f"{'-' if s < 0 else ''}{ip}.{dec:0{digits}d}"


if __name__ == "__main__":
    for a in sys.argv[1:]:
        main(a)
