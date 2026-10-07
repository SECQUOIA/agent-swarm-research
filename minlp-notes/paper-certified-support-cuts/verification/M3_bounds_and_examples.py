"""M3: tightness of breakpoint counts, the lower-bound family, certificate
size of the inherited oracle, and the gain corollary examples.

Run:  python M3_bounds_and_examples.py      (single-threaded, < 1 minute)
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[2])

import sys
sys.dont_write_bytecode = True
sys.path.insert(0, (_PUBLIC_REPO + '/paper-certified-support-cuts/verification'))
sys.path.insert(0, (_PUBLIC_REPO + '/research-20261002-convexification/theory'))
from fractions import Fraction as F
import random
from M3_star_sweep import sweep_star, inherited, kkt_oracle
from quadratic_star import support_star


def pl_lines(start_value, breaks, slopes):
    """Lines of a PL function on [0, inf) with given breakpoints and slopes."""
    lines, value, x = [], F(start_value), F(0)
    for j, s in enumerate(slopes):
        lines.append((value - s * x, F(s)))
        if j < len(breaks):
            value += s * (breaks[j] - x)
            x = breaks[j]
    return lines


def zigzag(N):
    """One concave leaf whose endpoint preference flips on every envelope piece."""
    A = F(N * N + 2)
    lb = [F(j) for j in range(1, N, 2)]          # L breaks at odd integers
    ub = [F(j) for j in range(2, N, 2)]          # U breaks at even integers
    L = pl_lines(-A, lb, [2 * j for j in range(len(lb) + 1)])
    U = pl_lines(A, ub, [-(2 * j + 1) for j in range(len(ub) + 1)])
    rows = [(b, F(-1), -a) for a, b in L] + [(-b, F(1), a) for a, b in U]
    B = 10 * A
    leaf = dict(l=-B, u=B, d=F(-1), e=F(0), f=F(-1, 2), rows=rows)
    center = dict(ly=F(0), uy=F(N), a0=F(0), a1=F(0), a2=F(0), rows=[])
    return center, [leaf], len(L) + len(U)


def tent_family(z, w, R):
    """Phi_z(y) = -sum_j T((y - z_j)/w) on y in [0, R]: 3 leaves and 1 row per z_j.

    T(t) = max(0, 1 - |t|).  Uses -T = h1 + h2 + 2*max(0, t) - t - 1 with
    concave box hinges h1 = min(0, t + 1), h2 = min(0, 1 - t) (t = (y - z)/w)
    and the convex hinge max(0, t) produced by one row x_C >= (y - z)/w.
    """
    leaves = []
    for zj in z:
        leaves.append(dict(l=F(0), u=F(1), d=F(0), e=1 / w, f=(w - zj) / w, rows=[]))   # min(0,(y-z+w)/w)
        leaves.append(dict(l=F(0), u=F(1), d=F(0), e=-1 / w, f=(zj + w) / w, rows=[]))  # min(0,(z+w-y)/w)
        leaves.append(dict(l=F(0), u=R / w + 1, d=F(0), e=F(0), f=F(2),                # 2 max(0,(y-z)/w)
                           rows=[(1 / w, F(-1), zj / w)]))
    k = len(z)
    center = dict(ly=F(0), uy=R, a0=-k + sum(z) / w, a1=-k / w, a2=F(0), rows=[])
    return center, leaves


def tent_sum_max(z, w):
    T = lambda t: max(F(0), 1 - abs(t) / w)
    pts = set(z) | {zj + s * w for zj in z for s in (-1, 1)}
    return max(sum(T(p - zj) for zj in z) for p in pts)


def main():
    # 1. Zigzag: rule changes versus lines for a concave leaf.
    for N in (6, 11, 20):
        center, leaves, active_lines = zigzag(N)
        res = sweep_star(center, leaves)
        Bi = res["breakpoints"][0]
        assert Bi == 2 * N - 1 == 2 * active_lines - 3, (N, Bi, active_lines)
        assert res["value"] == inherited(center, leaves)
        print(f"zigzag N={N}: {active_lines} active envelope lines (+2 inactive box lines), "
              f"{Bi} rule changes = 2*{active_lines}-3; value {res['value']} matches inherited oracle")

    # 2. Lower-bound family: min Phi_z >= -1 iff z is w-separated.
    rng = random.Random(77)
    w, R = F(1), F(40)
    count = sep = 0
    for trial in range(60):
        k = rng.randint(2, 7)
        z = [F(rng.randint(2, 76), 2) for _ in range(k)]
        if trial % 5 == 0:
            z[1] = z[0]                                      # coincidence
        center, leaves = tent_family(z, w, R)
        res = sweep_star(center, leaves)
        expected = -tent_sum_max(z, w)
        assert res["value"] == expected, (z, res["value"], expected)
        separated = all(abs(a - b) >= w for i, a in enumerate(z) for b in z[i + 1:])
        assert (res["value"] >= -1) == separated
        if trial < 6:
            assert inherited(center, leaves) == expected
        count += 1
        sep += separated
    print(f"tent family: {count} instances ({sep} w-separated); min = -max sum of tents; "
          f"min >= -1 exactly when w-separated (first 6 also match inherited oracle)")

    # 3. Inherited certificate size for box hinge stars: (k+1) pieces x k leaf rules.
    for k in (5, 10, 20):
        n = k + 1
        coeff = {}
        for j in range(1, n):
            e = [0] * n; e[0] = e[j] = 1; coeff[tuple(e)] = 1
            e = [0] * n; e[j] = 1; coeff[tuple(e)] = -F(j, n)     # (y - j/n) x_j
        res = support_star(((0, 1),) * n, (), coeff)
        entries = sum(len(p["leaf_rules"]) for p in res["pieces"])
        assert len(res["pieces"]) == k + 1 and entries == k * (k + 1)
    print("inherited certificate: box hinge star with k leaves has k+1 pieces and k(k+1) rule entries (k=5,10,20)")

    # 3b. Center-leaf rows destroy concavity of a leaf message (DK Lemma 2 needs a box).
    leaf = dict(l=F(0), u=F(1), d=F(0), e=F(0), f=F(1), rows=[(F(1), F(-1), F(1, 2)), (F(-1), F(-1), F(-1, 2))])
    vals = [sweep_star(dict(ly=y, uy=y, a0=F(0), a1=F(0), a2=F(0), rows=[]), [leaf])["value"]
            for y in (F(0), F(1, 4), F(1, 2), F(3, 4), F(1))]
    assert vals == [F(1, 2), F(1, 4), 0, F(1, 4), F(1, 2)]
    assert vals[2] < (vals[1] + vals[3]) / 2
    print(f"rows x>=y-1/2, x>=1/2-y, min x: message values {[str(v) for v in vals]} = |y-1/2| (convex kink, not concave)")

    # 4. Gain corollary examples.
    c = {(0, 0, 0): F(1, 16), (1, 0, 0): F(-1, 2), (2, 0, 0): 2,
         (0, 1, 0): F(5, 4), (0, 2, 0): F(-3, 4), (1, 1, 0): -1,
         (0, 0, 1): 1, (0, 0, 2): F(-39, 64), (1, 0, 1): F(-5, 4)}
    # pair parts: D1=(y-1/4-x/2)^2 + x(1-x), D2=(y-5z/8)^2 + z(1-z); both have min 0 on [0,1]^2.
    d1 = {(0, 0): F(1, 16), (1, 0): F(-1, 2), (2, 0): 1, (0, 1): F(1, 4) + 1, (0, 2): F(1, 4) - 1, (1, 1): -1}
    d2 = {(2, 0): 1, (0, 1): 1, (0, 2): F(25, 64) - 1, (1, 1): F(-5, 4)}
    b1 = F(support_star(((0, 1),) * 2, (), d1)["bound"])
    b2 = F(support_star(((0, 1),) * 2, (), d2)["bound"])
    bstar = F(support_star(((0, 1),) * 3, (), c)["bound"])
    assert (b1, b2, bstar) == (0, 0, F(1, 128))
    print(f"gain example (overlap witness): beta1={b1}, beta2={b2}, beta*={bstar}, Delta={bstar - b1 - b2}")
    # Three pairs whose minimizing center sets intersect pairwise but have no common point.
    # q1=(y-x1)^2, x1 in [0,1/2]; q2=(y-x2)^2, x2 in [1/2,1]; q3 = y - y^2 (x3 idle); y in [0,1].
    bounds = ((0, 1), (0, F(1, 2)), (F(1, 2), 1), (0, 1))
    q = {(2, 0, 0, 0): 2 - 1, (1, 1, 0, 0): -2, (0, 2, 0, 0): 1,
         (1, 0, 1, 0): -2, (0, 0, 2, 0): 1, (1, 0, 0, 0): 1}
    # (y-x1)^2+(y-x2)^2+y-y^2 = y^2 - 2y x1 + x1^2 - 2y x2 + x2^2 + y
    total = F(support_star(bounds, (), q)["bound"])
    singles = [F(support_star(((0, 1), b), (), p)["bound"]) for b, p in
               [((0, F(1, 2)), {(2, 0): 1, (1, 1): -2, (0, 2): 1}),
                ((F(1, 2), 1), {(2, 0): 1, (1, 1): -2, (0, 2): 1}),
                ((0, 1), {(1, 0): 1, (2, 0): -1})]]
    assert singles == [0, 0, 0] and total == F(1, 4)
    print(f"gain example (pairwise-intersecting projections {{[0,1/2],[1/2,1],{{0,1}}}}): Delta = {total}")
    # independent check of the last value by exact KKT enumeration
    center = dict(ly=F(0), uy=F(1), a0=F(0), a1=F(1), a2=F(1), rows=[])
    leaves = [dict(l=F(0), u=F(1, 2), d=F(1), e=F(-2), f=F(0), rows=[]),
              dict(l=F(1, 2), u=F(1), d=F(1), e=F(-2), f=F(0), rows=[]),
              dict(l=F(0), u=F(1), d=F(0), e=F(0), f=F(0), rows=[])]
    assert kkt_oracle(center, leaves) == F(1, 4) == sweep_star(center, leaves)["value"]
    print("  confirmed by KKT face enumeration and by the M3 sweep")


if __name__ == "__main__":
    main()
