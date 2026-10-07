"""Check the Hadamard-diagonal height bound and the stationary-polytope lemma.

For random and hand-built rational mixed box QPs (n <= 3):
  * F* from exhaustive nonsingular-face enumeration, sandwiched by a
    corrected-grid lower bound and grid upper bound;
  * every enumerated optimizer has common denominator dividing D*det(P_SS)
    with S its free set, and <= R_had = D * prod_{i cont, P_ii>0} P_ii;
  * den(F*) <= V_had = D R_had^2;
  * R_had <= R_code (row-norm product) and R_had <= R_rep ((2 n C_H)^n);
  * for optimizers s in the relative interior of flat optimal pieces:
    P_{J0 J0} is PSD, every vertex v of the stationary polytope P(s) is
    optimal, P_TT is positive definite for T = interior coordinates of v,
    and v has common denominator dividing D det(P_TT).
"""
import random
from fractions import Fraction as Fr
from itertools import combinations, product

from exact_common import (value, grad, det, rank, solve_unique, is_pd, is_psd,
                          common_den, heights, face_candidates,
                          corrected_grid_lower_bound)

random.seed(20261003)


def rand_frac(lo, hi, dens=(1, 2, 3, 4, 6)):
    d = random.choice(dens)
    return Fr(random.randint(lo * d, hi * d), d)


def random_instance(n):
    H = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        H[i][i] = rand_frac(-3, 4)
        for j in range(i + 1, n):
            H[i][j] = H[j][i] = rand_frac(-3, 3) if random.random() < 0.7 else Fr(0)
    b = [rand_frac(-3, 3) for _ in range(n)]
    c = rand_frac(-2, 2)
    integers = set(i for i in range(n) if random.random() < 0.3)
    bounds = []
    for i in range(n):
        if i in integers:
            l = random.randint(-2, 1)
            bounds.append((Fr(l), Fr(l + random.randint(1, 3))))
        else:
            l = rand_frac(-2, 1)
            bounds.append((l, l + rand_frac(1, 3, dens=(1, 2, 3, 5))))
    return H, b, c, bounds, integers


def hand_instances():
    out = []
    # (x+y-1/3)^2 + z(1-z): flat optimal segment, singular free Hessian
    H = [[Fr(2), Fr(2), Fr(0)], [Fr(2), Fr(2), Fr(0)], [Fr(0), Fr(0), Fr(-2)]]
    b = [Fr(-2, 3), Fr(-2, 3), Fr(1)]
    out.append((H, b, Fr(1, 9), [(Fr(0), Fr(1))] * 3, set()))
    # (x-y)^2 on [0,1]^2 : diagonal of optima
    H = [[Fr(2), Fr(-2)], [Fr(-2), Fr(2)]]
    out.append((H, [Fr(0), Fr(0)], Fr(0), [(Fr(0), Fr(1))] * 2, set()))
    # x^2 - 2xz + 4z on [0,4]^2 (two isolated optima), continuous
    H = [[Fr(2), Fr(-2)], [Fr(-2), Fr(0)]]
    out.append((H, [Fr(0), Fr(4)], Fr(0), [(Fr(0), Fr(4))] * 2, set()))
    # (x - y/3)^2 + (y - 2)^2/7 with y integer and a flat third coordinate
    H = [[Fr(2), Fr(-2, 3), Fr(0)], [Fr(-2, 3), Fr(2, 9) + Fr(2, 7), Fr(0)],
         [Fr(0), Fr(0), Fr(0)]]
    b = [Fr(0), Fr(-4, 7), Fr(0)]
    out.append((H, b, Fr(4, 7), [(Fr(-1), Fr(1)), (Fr(0), Fr(3)), (Fr(0), Fr(1, 2))], {1}))
    # (x + 2y + 3z - 1)^2 : two-dimensional flat optimal face
    a = [Fr(1), Fr(2), Fr(3)]
    H = [[2 * a[i] * a[j] for j in range(3)] for i in range(3)]
    b = [-2 * a[i] for i in range(3)]
    out.append((H, b, Fr(1), [(Fr(-1, 2), Fr(1))] * 3, set()))
    return out


stats = dict(instances=0, optimizers=0, polytope_vertices=0, flat_pieces=0,
             had_le_code=0, had_lt_code=0, had_lt_rep=0)


def check_instance(H, b, c, bounds, integers):
    n = len(b)
    hs = heights(H, b, c, bounds, integers)
    D, P = hs["D"], hs["P"]
    cands = face_candidates(H, b, c, bounds, integers)
    vals = [(value(H, b, c, list(x)), x, S) for x, S in cands]
    Fstar = min(v for v, _, _ in vals)
    beta = corrected_grid_lower_bound(H, b, c, bounds, integers, 6)
    assert beta <= Fstar, (beta, Fstar)
    stats["instances"] += 1
    assert hs["R_had"] <= hs["R_code"] and hs["R_had"] <= hs["R_rep"]
    stats["had_le_code"] += 1
    stats["had_lt_code"] += hs["R_had"] < hs["R_code"]
    stats["had_lt_rep"] += hs["R_had"] < hs["R_rep"]
    assert Fstar.denominator <= hs["V_had"], (Fstar, hs)
    opt = [(x, S) for v, x, S in vals if v == Fstar]
    for x, S in opt:
        stats["optimizers"] += 1
        q = common_den(list(x))
        dS = det([[P[i][j] for j in S] for i in S]) if S else Fr(1)
        assert dS > 0
        assert (D * dS) % q == 0, (x, S, D, dS)
        assert q <= hs["R_had"]
    # flat pieces: midpoints of optimal pairs in the same integer slice
    for (x1, _), (x2, _) in combinations(opt, 2):
        if any(x1[i] != x2[i] for i in integers):
            continue
        s = [(x1[i] + x2[i]) / 2 for i in range(n)]
        if value(H, b, c, s) != Fstar:
            continue
        stats["flat_pieces"] += 1
        check_polytope(H, b, c, bounds, integers, s, Fstar, D, P, hs)


def check_polytope(H, b, c, bounds, integers, s, Fstar, D, P, hs):
    n = len(b)
    J0 = [i for i in range(n) if i not in integers and bounds[i][0] < s[i] < bounds[i][1]]
    g = grad(H, b, s)
    assert all(g[i] == 0 for i in J0)
    assert is_psd([[P[i][j] for j in J0] for i in J0])
    fixed = {i: s[i] for i in range(n) if i not in J0}
    A = [[H[i][j] for j in J0] for i in J0]
    rhs = [-b[i] - sum(H[i][j] * fixed[j] for j in fixed) for i in J0]
    m = len(J0)
    for k in range(m + 1):
        for Kpos in combinations(range(m), k):
            T = [t for t in range(m) if t not in Kpos]
            for pat in product((0, 1), repeat=k):
                xK = {t: bounds[J0[t]][p] for t, p in zip(Kpos, pat)}
                AT = [[A[r][t] for t in T] for r in range(m)]
                r2 = [rhs[r] - sum(A[r][t] * xK[t] for t in Kpos) for r in range(m)]
                if T and rank(AT) < len(T):
                    continue
                sol = solve_unique(AT, r2) if T else ([] if all(v == 0 for v in r2) else None)
                if sol is None:
                    continue
                w = dict(xK)
                w.update(zip(T, sol))
                v = list(s)
                for t in range(m):
                    v[J0[t]] = w[t]
                if not all(bounds[i][0] <= v[i] <= bounds[i][1] for i in range(n)):
                    continue
                stats["polytope_vertices"] += 1
                assert value(H, b, c, v) == Fstar
                Tint = [i for i in J0 if bounds[i][0] < v[i] < bounds[i][1]]
                PT = [[P[i][j] for j in Tint] for i in Tint]
                assert not Tint or is_pd(PT), (v, Tint)
                dT = det(PT) if Tint else Fr(1)
                q = common_den(v)
                assert (D * dT) % q == 0 and q <= hs["R_had"], (v, D, dT, q)


for inst in hand_instances():
    check_instance(*inst)
for trial in range(220):
    n = random.choice([1, 2, 2, 3, 3])
    check_instance(*random_instance(n))
print(stats)
