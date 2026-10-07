"""M5: exact checks of the rational domain net (Report B Lemma domain-net).

  * floor rounding over all s vertices gives ||x - xhat||_inf < D_inf (s-1)/M
    and xhat in S_M (exactly feasible);
  * Caratheodory refinement: rounding a basic representation with at most
    dim(P)+1 vertices gives ||x - xhat||_inf < dim(P) D_inf / M;
  * the infinity-norm Lipschitz bound with L = sum_j sum_r sup_box |d_r F_j|;
  * the support bracket min_{S_M} c^T F - delta_M <= min_P c^T F <= min_{S_M} c^T F
    on a quartic over a thin equality domain with known minimum.
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[2])

import random
import sys
from fractions import Fraction as F

sys.dont_write_bytecode = True  # never write into Report B
sys.path.insert(0, (_PUBLIC_REPO + '/research-20261003-convexification/theory'))
import quadratic_polytope as qp  # noqa: E402
import M5_exactlp as lp  # noqa: E402

random.seed(7)


def inf_norm(v):
    return max(abs(x) for x in v)


def combo(weights, verts):
    d = len(verts[0])
    return tuple(sum((w * v[r] for w, v in zip(weights, verts)), F(0)) for r in range(d))


def floor_round(alpha, M):
    n = [int(a * M // 1) for a in alpha[:-1]]
    n.append(M - sum(n))
    assert n[-1] >= 0
    return [F(k, M) for k in n]


def basic_representation(x, verts):
    """A vertex (basic) solution of {lam >= 0, sum lam = 1, sum lam v = x}."""
    s, d = len(verts), len(x)
    A_eq = [[v[r] for v in verts] for r in range(d)] + [[1] * s]
    b_eq = list(x) + [1]
    st, _, lam = lp.solve([0] * s, A_eq=A_eq, b_eq=b_eq)
    assert st == "optimal"
    return lam


def affine_dim(verts):
    import sympy as sp
    base = verts[0]
    M = sp.Matrix([[sp.Rational(v[r] - base[r]) for r in range(len(base))] for v in verts[1:]]) if len(verts) > 1 else None
    return 0 if M is None else M.rank()


def main():
    worst_ratio = F(0)
    for trial in range(60):
        d = random.choice([2, 3])
        box = [(F(random.randint(-3, 0)), F(random.randint(1, 3))) for _ in range(d)]
        rows = []
        for _ in range(random.randint(0, 3)):
            a = [F(random.randint(-3, 3)) for _ in range(d)]
            rows.append(tuple(a) + (F(random.randint(0, 4)),))
        if trial % 5 == 0:  # thin domain: an equality
            a = [F(random.randint(1, 3)) for _ in range(d)]
            rows += [tuple(a) + (F(1, 3),), tuple(-x for x in a) + (-F(1, 3),)]
        verts = [tuple(map(F, v)) for v in qp.polytope_vertices(box, rows)]
        if not verts:
            continue
        s = len(verts)
        dim = affine_dim(verts)
        D = max(max(v[r] for v in verts) - min(v[r] for v in verts) for r in range(d))
        for M in (1, 2, 5, 13):
            for _ in range(5):
                alpha = [F(random.randint(0, 9)) for _ in range(s)]
                if sum(alpha) == 0:
                    alpha[0] = F(1)
                alpha = [a / sum(alpha) for a in alpha]
                x = combo(alpha, verts)
                xhat = combo(floor_round(alpha, M), verts)
                err = inf_norm([a - b for a, b in zip(x, xhat)])
                assert err <= D * (s - 1) / M and (D == 0 or s == 1 or err < D * (s - 1) / M)
                assert all(lo <= c <= hi for c, (lo, hi) in zip(xhat, box))
                assert all(sum(r[i] * xhat[i] for i in range(d)) <= r[-1] for r in rows)
                lam = basic_representation(x, verts)
                support = [i for i, l in enumerate(lam) if l > 0]
                assert len(support) <= dim + 1
                sub = [verts[i] for i in support]
                xhat2 = combo(floor_round([lam[i] for i in support], M), sub)
                err2 = inf_norm([a - b for a, b in zip(x, xhat2)])
                assert err2 <= D * dim / M
                if D:
                    worst_ratio = max(worst_ratio, err2 * M / D)
    # Lipschitz check for random cubic features in d = 2
    import sympy as sp
    X, Y = sp.symbols("x y")
    for _ in range(40):
        feats = [sum(sp.Rational(random.randint(-3, 3), random.randint(1, 3)) * X**i * Y**j
                     for i in range(3) for j in range(3 - i)) for _ in range(3)]
        box = [(F(random.randint(-2, 0)), F(random.randint(1, 2))) for _ in range(2)]

        def sup_abs(expr):
            # interval bound of |expr| on the box, monomial by monomial
            poly = sp.Poly(expr, X, Y)
            total = F(0)
            for (i, j), coef in zip(poly.monoms(), poly.coeffs()):
                bx = max(abs(box[0][0]) ** i, abs(box[0][1]) ** i)
                by = max(abs(box[1][0]) ** j, abs(box[1][1]) ** j)
                total += abs(F(int(coef.p), int(coef.q))) * bx * by
            return total
        L = sum(sup_abs(sp.diff(f, v)) for f in feats for v in (X, Y))
        for _ in range(20):
            p1 = [F(random.randint(int(lo * 10), int(hi * 10)), 10) for lo, hi in box]
            p2 = [F(random.randint(int(lo * 10), int(hi * 10)), 10) for lo, hi in box]
            c = [F(random.randint(-10, 10), 10) for _ in feats]
            diff = sum(cj * (F(str(f.subs({X: sp.Rational(p1[0]), Y: sp.Rational(p1[1])})))
                             - F(str(f.subs({X: sp.Rational(p2[0]), Y: sp.Rational(p2[1])}))))
                       for cj, f in zip(c, feats))
            assert abs(diff) <= L * inf_norm([a - b for a, b in zip(p1, p2)])
    # support bracket on a thin domain: P = {x + y = 1/3, 0 <= x, y <= 1}, F = (x - 2y)^4, min 0
    verts = [(F(0), F(1, 3)), (F(1, 3), F(0))]
    D = F(1, 3)
    # d/dx (x-2y)^4 = 4(x-2y)^3, |.| <= 4*3^3 on [0,1]^2 ; d/dy: 8|x-2y|^3 <= 8*27
    L = F(4 * 27 + 8 * 27)
    for M in (1, 3, 10, 40):
        net = [combo([F(i, M), F(M - i, M)], verts) for i in range(M + 1)]
        vals = [(x - 2 * y) ** 4 for x, y in net]
        delta = L * D * (len(verts) - 1) / M
        assert min(vals) - delta <= 0 <= min(vals)
    print(f"domain-net checks passed; worst observed err*M/D for the Caratheodory rounding = {worst_ratio}")


if __name__ == "__main__":
    main()
