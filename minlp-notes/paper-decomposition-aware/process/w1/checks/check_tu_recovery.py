"""Check the stationary-face recovery lemma (TU version) with exact arithmetic.

Slice P = {x : M x <= d}, M = [A; I; -I] TU, objective
F(x) = (x^T H x + c^T x + e)/D, gradient direction G x + g with G = 2H, g = c.
Constants (lemma in tu-proofs.tex):
  Lambda = (2 n^2 C_H)^n, Q = #rows(M), tau = 1/(4 Q Lambda), delta = tau/(2n).
For feasible y with dist(y, S) <= delta, select J = {i : slack_i(y) <= tau};
the recovery polytope
  Pi = {x in P : M_J x = d_J, N^T (G x + g) = 0},  N = basis of ker M_J,
must be nonempty and consist of global minimizers. We enumerate the vertices
of Pi and check them (F is affine-free constant on Pi by the lemma; we also
check the centroid).
"""
import random
from fractions import Fraction as Fr
from tu_exact_util import vertices, nullspace, dot

random.seed(5)


def build(A, b, l, u):
    n = len(l)
    M = [list(r) for r in A] + [[int(i == k) for k in range(n)] for i in range(n)] + \
        [[-int(i == k) for k in range(n)] for i in range(n)]
    d = [Fr(v) for v in b] + [Fr(v) for v in u] + [-Fr(v) for v in l]
    return M, d


def Fval(H, c, e, D, x):
    n = len(x)
    return (sum(H[i][k] * x[i] * x[k] for i in range(n) for k in range(n))
            + dot(c, x) + e) / D


def recover(M, d, H, c, y, tau):
    n = len(y)
    J = [i for i in range(len(M)) if d[i] - dot(M[i], y) <= tau]
    MJ = [M[i] for i in J]
    N = nullspace(MJ, n)
    G = [[2 * H[i][k] for k in range(n)] for i in range(n)]
    eq_rows = [list(M[i]) for i in J]
    eq_rhs = [d[i] for i in J]
    for v in N:
        # v^T (G x + c) = 0  ->  (G^T v)^T x = -v^T c
        row = [sum(v[i] * G[i][k] for i in range(n)) for k in range(n)]
        eq_rows.append(row)
        eq_rhs.append(-dot(v, c))
    V = vertices(M, d, eq_rows, eq_rhs)
    return J, V


def run_case(name, A, b, l, u, H, c, e, D, Fstar, optimal_points, nprobe=6):
    n = len(l)
    M, d = build(A, b, l, u)
    # constants of tu-proofs.tex: F = (x^T H x + c^T x + e)/D has Hessian 2H/D;
    # Delta = D clears all monomial coefficients, so P = Delta*Hess = 2H.
    CP = max(1, max(abs(2 * v) for row in H for v in row))
    R = (2 * n * CP) ** n
    Q = len(M)                       # m' = m + 2 n
    tau = Fr(1, 4 * Q * R)           # D_0 = 1
    delta = tau / (2 * n)            # <= tau/(2 sqrt(n))
    # vertex heights of stationary face polytopes (Lemma tu-statpoly (c))
    for s in optimal_points:
        s = [Fr(v) for v in s]
        J0 = [i for i in range(len(M)) if dot(M[i], s) == d[i]]
        N0 = nullspace([M[i] for i in J0], n)
        G = [[2 * H[i][k] for k in range(n)] for i in range(n)]
        eqr = [list(M[i]) for i in J0]
        eqb = [d[i] for i in J0]
        for v in N0:
            eqr.append([sum(v[i] * G[i][k] for i in range(n)) for k in range(n)])
            eqb.append(-dot(v, c))
        for vert in vertices(M, d, eqr, eqb):
            den = 1
            for xi in vert:
                den = den * xi.denominator // __import__("math").gcd(den, xi.denominator)
            assert den <= R, (name, vert, den, R)
            assert Fval(H, c, e, D, vert) == Fstar, (name, vert)
    checked = 0
    for s in optimal_points:
        s = [Fr(v) for v in s]
        assert Fval(H, c, e, D, s) == Fstar
        for _ in range(nprobe):
            # random feasible perturbation within delta
            for _try in range(200):
                dirn = [Fr(random.randint(-8, 8)) for _ in range(n)]
                nrm2 = sum(v * v for v in dirn)
                if nrm2 == 0:
                    continue
                # scale so that ||step||_2 <= delta (use ||.||_1 >= ||.||_2)
                l1 = sum(abs(v) for v in dirn)
                step = [v * delta / l1 * Fr(random.randint(0, 10), 10) for v in dirn]
                y = [si + st for si, st in zip(s, step)]
                if all(dot(M[i], y) <= d[i] for i in range(len(M))):
                    break
            else:
                y = s
            J, V = recover(M, d, H, c, y, tau)
            assert V, (name, s, y, "recovery polytope empty")
            for v in V:
                assert Fval(H, c, e, D, v) == Fstar, (name, s, y, v)
            cen = [sum(v[i] for v in V) / len(V) for i in range(n)]
            assert Fval(H, c, e, D, cen) == Fstar
            checked += 1
    return checked, tau, delta


if __name__ == "__main__":
    total = 0
    # 1. (x1-x2)^2 on [0,1]^2, continuum optimal set (diagonal)
    H = [[1, -1], [-1, 1]]
    t, tau, delta = 0, None, None
    k, tau, delta = run_case("diag", [], [], [0, 0], [1, 1], H, [0, 0], 0, 1, Fr(0),
                             [(0, 0), (1, 1), (Fr(1, 2), Fr(1, 2)), (Fr(1, 3), Fr(1, 3))])
    total += k
    # near-boundary optimizer: extra rows with slack < 3 tau/2 get snapped
    k, _, _ = run_case("diag-near", [], [], [0, 0], [1, 1], H, [0, 0], 0, 1, Fr(0),
                       [(tau / 2, tau / 2), (1 - tau / 3, 1 - tau / 3)])
    total += k
    # 2. two-optima block: x + t = z (equality as two rows)
    Hb = [[4, 0, -2], [0, 0, 0], [-2, 0, 1]]  # (2x-z)^2 = 4x^2 -4xz + z^2
    # plus z(1-z)/4 -> multiply everything by 4: 16x^2 -16xz +4z^2 + z - z^2
    Hb4 = [[16, 0, -8], [0, 0, 0], [-8, 0, 3]]
    k, _, _ = run_case("block", [[1, 1, -1], [-1, -1, 1]], [0, 0], [0, 0, 0], [1, 1, 1],
                       Hb4, [0, 0, 1], 0, 4, Fr(0), [(0, 0, 0), (Fr(1, 2), Fr(1, 2), 1)])
    total += k
    # 3. nonconvex with continuum: x0(1-x0) + (x1-x2)^2 on [0,1]^3
    H3 = [[-1, 0, 0], [0, 1, -1], [0, -1, 1]]
    k, _, _ = run_case("nonconvex-cont", [], [], [0, 0, 0], [1, 1, 1], H3, [1, 0, 0], 0, 1,
                       Fr(0), [(0, Fr(1, 4), Fr(1, 4)), (1, 1, 1), (1, 0, 0)])
    total += k
    # 4. TU row x1 + x2 <= 1 with optimal face on the row
    #    F = x0(1-x0) + (x1 + x2 - 1)^2  (optimal set: x0 in {0,1}, x1+x2=1)
    #    integral form: -x0^2 + x0 + x1^2 + 2x1x2 + x2^2 - 2x1 - 2x2 + 1
    H4 = [[-1, 0, 0], [0, 1, 1], [0, 1, 1]]
    k, _, _ = run_case("row-face", [[0, 1, 1]], [1], [0, 0, 0], [1, 1, 1], H4, [1, -2, -2], 1,
                       1, Fr(0), [(0, Fr(1, 3), Fr(2, 3)), (1, 1, 0), (0, Fr(1, 2), Fr(1, 2))])
    total += k
    print("recovery probes passed:", total)
    # 5. premature recovery can return a nonglobal stationary point:
    #    F = x - x^2 on x = t, from y = (1/2, 1/2) far from S = {(0,0),(1,1)}
    M, d = build([[1, -1], [-1, 1]], [0, 0], [0, 0], [1, 1])
    J, V = recover(M, d, [[-1, 0], [0, 0]], [1, 0], [Fr(1, 2), Fr(1, 2)], Fr(1, 100))
    vals = sorted({Fval([[-1, 0], [0, 0]], [1, 0], 0, 1, v) for v in V})
    print("premature recovery output values:", [str(v) for v in vals], "(global value 0)")
    assert vals == [Fr(1, 4)]
    print("ALL RECOVERY CHECKS PASSED")
