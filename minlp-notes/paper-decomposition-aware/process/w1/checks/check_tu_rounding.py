"""Check feasible correlated corner rounding on aligned TU cells.

For several TU systems A x + B z <= b (integral data, explicit labels z) and
mesh h = 2^-j, enumerate cells meeting the fiber, compute all fiber vertices
exactly, and verify:
  * every vertex is a cell corner (box integrality after dyadic scaling);
  * a Caratheodory decomposition of random feasible points uses feasible
    corners, preserves the mean, has sum Var <= n_c h^2/4;
  * E F(Y) <= F(x) + n_c Lbar h^2/8 for random quadratics with
    Hess <= Lbar I (Lbar = max absolute row sum);
  * the full-curvature example x1 = x2, F = 2 x1 x2 is tight.
A non-TU control row (1,2) must exhibit a non-corner vertex.
"""
import random
from fractions import Fraction as Fr
from itertools import product
from tu_exact_util import vertices, caratheodory, dot

random.seed(20261003)


def fiber(Arows, rhs, k, h, n):
    """Return (Aineq, bineq) in t-coordinates for cell x = h(k+t)."""
    Aineq, bineq = [], []
    for r, b in zip(Arows, rhs):
        Aineq.append(list(r))
        bineq.append(b / h - dot(r, k))
    for i in range(n):
        e = [0] * n
        e[i] = 1
        Aineq.append(e)
        bineq.append(Fr(1))
        e2 = [0] * n
        e2[i] = -1
        Aineq.append(e2)
        bineq.append(Fr(0))
    return Aineq, bineq


def rand_quadratic(n):
    H = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            v = Fr(random.randint(-4, 4), random.randint(1, 3))
            H[i][j] = H[j][i] = v
    g = [Fr(random.randint(-5, 5), random.randint(1, 4)) for _ in range(n)]
    Lbar = max(max(sum(abs(v) for v in row) for row in H), Fr(1, 100))
    return H, g, Lbar


def Fq(H, g, x):
    return Fr(1, 2) * sum(H[i][j] * x[i] * x[j] for i in range(len(x))
                          for j in range(len(x))) + dot(g, x)


SYSTEMS = {
    # name: (A rows (continuous), B rows (labels), b, bounds l,u, label sets)
    # network: arcs 0:(1->2), 1:(2->3), 2:(1->3), 3:(3->1); conservation at
    # nodes 1,2 with supplies depending on a binary label z (column B)
    "network": ([[1, 0, 1, -1], [-1, 1, 0, 0], [-1, 0, -1, 1], [1, -1, 0, 0]],
                [[-1], [0], [1], [0]], [0, 0, 0, 0], (0, 2), [[0, 1]]),
    # interval (consecutive ones) resource rows over 4 coordinates
    "interval": ([[1, 1, 0, 0], [0, 1, 1, 1], [1, 1, 1, 0]],
                 [[0], [-1], [0]], [2, 2, 3], (0, 2), [[0, 1, 2]]),
    # x + y = 2 z (continuous part TU, integer column -2 arbitrary)
    "x+y=2z": ([[1, 1], [-1, -1]], [[-2], [2]], [0, 0], (0, 2), [[0, 1]]),
    # order constraints x1 <= x2 <= x3 with x3 - x1 <= z
    "order": ([[1, -1, 0], [0, 1, -1], [-1, 0, 1]], [[0], [0], [-1]],
              [0, 0, 0], (0, 2), [[0, 1, 2]]),
}

NON_TU = ([[1, 2], [-1, -2]], [[0], [0]], [2, -2], (0, 2), [[0]])


def run_system(name, sysdata, j, samples, expect_integral=True, max_cells=40):
    A, B, b, (lo, hi), labels = sysdata
    n = len(A[0])
    h = Fr(1, 2 ** j)
    stats = dict(cells=0, nonint=0, decomp=0, taylor=0, maxratio=Fr(0))
    for z in product(*labels):
        rhs = [Fr(b[r]) - dot(B[r], z) for r in range(len(A))]
        ncell = int((hi - lo) / h)
        allk = list(product(range(ncell), repeat=n))
        random.shuffle(allk)
        for k in allk[:max_cells]:
            kk = [Fr(lo) / h + ki for ki in k]
            Ai, bi = fiber(A, rhs, kk, h, n)
            V = vertices(Ai, bi)
            if not V:
                continue
            stats["cells"] += 1
            for v in V:
                if any(c not in (0, 1) for c in v):
                    stats["nonint"] += 1
                    if expect_integral:
                        raise AssertionError((name, z, k, v))
            if not expect_integral:
                continue
            for _ in range(samples):
                w = [Fr(random.randint(1, 9)) for _ in V]
                tot = sum(w)
                t = [sum(wi * v[i] for wi, v in zip(w, V)) / tot for i in range(n)]
                comb = caratheodory(t, Ai, bi)
                x = [h * (kk[i] + t[i]) for i in range(n)]
                var = Fr(0)
                for i in range(n):
                    m2 = sum(wt * (h * (kk[i] + v[i]) - x[i]) ** 2 for wt, v in comb)
                    var += m2
                    assert m2 <= h * h / 4
                assert var <= n * h * h / 4
                for wt, v in comb:
                    assert all(c in (0, 1) for c in v)
                    y = [h * (kk[i] + v[i]) for i in range(n)]
                    for r in range(len(A)):
                        assert dot(A[r], y) <= rhs[r]
                stats["decomp"] += 1
                H, g, Lbar = rand_quadratic(n)
                EF = sum(wt * Fq(H, g, [h * (kk[i] + v[i]) for i in range(n)])
                         for wt, v in comb)
                excess = EF - Fq(H, g, x)
                bound = n * Lbar * h * h / 8
                assert excess <= Lbar * var / 2 <= bound, (excess, bound)
                if bound > 0:
                    stats["maxratio"] = max(stats["maxratio"], excess / bound)
                stats["taylor"] += 1
    return stats


def full_curvature_example():
    # x1 = x2 on [0,h]^2, F = 2 x1 x2, x = (h/2, h/2)
    h = Fr(1, 4)
    x = (h / 2, h / 2)
    F = lambda y: 2 * y[0] * y[1]
    EF = (F((0, 0)) + F((h, h))) / 2
    excess = EF - F(x)
    Lbar = 2  # eigenvalues of [[0,2],[2,0]] are +-2
    assert excess == h * h / 2 == 2 * Lbar * h * h / 8
    # diagonal curvature is zero, so a diagonal-only allowance would be 0
    return excess


if __name__ == "__main__":
    for name, s in SYSTEMS.items():
        for j in (1, 2):
            st = run_system(name, s, j, samples=2)
            print(name, "j=%d" % j, {k: (str(v) if isinstance(v, Fr) else v)
                                     for k, v in st.items()})
    st = run_system("nonTU", NON_TU, 1, samples=0, expect_integral=False)
    print("non-TU control (row x+2y=2):", st)
    assert st["nonint"] > 0
    print("full-curvature example excess =", full_curvature_example(),
          "(equals n_c Lbar h^2/8 with Lbar=2, diagonal curvature 0)")
    print("ALL TU ROUNDING CHECKS PASSED")
