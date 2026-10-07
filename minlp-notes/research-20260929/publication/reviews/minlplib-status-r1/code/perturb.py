"""Verifier (minlplib-status r1): find a tiny perturbation of the independent
continuous variables (those not defined by an equality in tri_proof's
order) that moves the listed point strictly inside all nearly active
bounds and inequality rows. Heuristic only (mpmath, finite differences);
the proof is the subsequent interval run of tri_proof.py with the printed
name=value settings.

Usage: python3 perturb.py MODEL.osil POINT.sol [target_slack]
"""
import sys
from fractions import Fraction

import mpmath
from mpmath import mp

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from osil_eval_cmp import read, row_value, mpf  # noqa: E402
from tri_proof import build_order, load_sol  # noqa: E402

mp.dps = 60


def forward(M, order, base):
    x = list(base)
    for (i, v) in order:
        if v is None:
            continue
        c = M["lin"][i][v]
        x[v] = mpmath.mpf(0)
        rest = row_value(M, i, x) - mpf(M["lin"][i][v]) * x[v] + mpf(M["cconst"][i])
        x[v] = (mpf(M["clb"][i]) - rest) / mpf(c)
    return x


def slacks(M, eq, x):
    out = []
    n = len(M["vars"])
    for j in range(n):
        if M["lb"][j] is not None:
            out.append((("lb", M["vars"][j]), x[j] - mpf(M["lb"][j])))
        if M["ub"][j] is not None:
            out.append((("ub", M["vars"][j]), mpf(M["ub"][j]) - x[j]))
    for i in range(len(M["cons"])):
        if i in eq:
            continue
        val = row_value(M, i, x) + mpf(M["cconst"][i])
        if M["clb"][i] is not None:
            out.append((("row-lb", M["cons"][i]), val - mpf(M["clb"][i])))
        if M["cub"][i] is not None:
            out.append((("row-ub", M["cons"][i]), mpf(M["cub"][i]) - val))
    return out


def main(osil, sol, target="1e-11"):
    M = read(osil)
    n = len(M["vars"])
    eq, order, _ = build_order(M)
    eqs = set(eq)
    defined = set(v for i, v in order if v is not None)
    listed = load_sol(sol)
    base = [mpf(listed.get(M["vars"][j], Fraction(0))) for j in range(n)]
    eps = mpmath.mpf("1e-12")
    free = [j for j in range(n) if j not in defined and M["type"][j] not in ("B", "I")
            and (M["lb"][j] is None or base[j] - mpf(M["lb"][j]) > eps)
            and (M["ub"][j] is None or mpf(M["ub"][j]) - base[j] > eps)]
    fixed_names = set(M["vars"][j] for j in range(n) if j not in defined)
    x0 = forward(M, order, base)
    s0 = slacks(M, eqs, x0)
    tgt = mpmath.mpf(target)
    active = [k for k, (key, s) in enumerate(s0) if s < 100 * tgt
              and not (key[0] in ("lb", "ub") and key[1] in fixed_names)]
    print("free continuous:", [M["vars"][j] for j in free])
    print("nearly active:", [(s0[k][0], mpmath.nstr(s0[k][1], 3)) for k in active])
    # free variables that are themselves at a bound must not move outward:
    # their own bound slack is part of the active set, so the solve handles it.
    h = mpmath.mpf("1e-25")
    J = mpmath.matrix(len(active), len(free))
    for c, j in enumerate(free):
        b2 = list(base)
        b2[j] += h
        s1 = slacks(M, eqs, forward(M, order, b2))
        for r, k in enumerate(active):
            J[r, c] = (s1[k][1] - s0[k][1]) / h
    keep = [r for r in range(len(active)) if any(abs(J[r, c]) > 0 for c in range(len(free)))]
    drop = [active[r] for r in range(len(active)) if r not in keep]
    bad = [s0[k][0] for k in drop if s0[k][1] < 0]
    if bad:
        print("violated rows independent of free variables:", bad)
    print("active rows depending on free variables:", [s0[active[r]][0] for r in keep])
    J = mpmath.matrix([[J[r, c] for c in range(len(free))] for r in keep])
    active = [active[r] for r in keep]
    rhs = mpmath.matrix([tgt - s0[k][1] for k in active])
    JJt = J * J.T
    d = J.T * mpmath.lu_solve(JJt, rhs)
    sets = []
    for c, j in enumerate(free):
        v = base[j] + d[c]
        f = Fraction(mpmath.nstr(v, 30))
        sets.append(f"{M['vars'][j]}={mpmath.nstr(v, 30)}")
    print("max |delta|:", mpmath.nstr(max(abs(t) for t in d), 3))
    print("SETS", " ".join(sets))


if __name__ == "__main__":
    main(*sys.argv[1:])
