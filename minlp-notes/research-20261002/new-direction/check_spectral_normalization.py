"""Small exact checks for the rational negative-subspace normalization lemma."""
from itertools import combinations
from math import lcm
import sympy as sp


def psd(M):
    assert M == M.T
    for size in range(1, M.rows + 1):
        for indices in combinations(range(M.rows), size):
            assert M.extract(indices, indices).det(method="domain-ge") >= 0


def normalize(A):
    n = A.rows
    H = max(sum(abs(A[i, j]) for j in range(n)) for i in range(n))
    columns = A.columnspace()
    if not columns:
        return sp.zeros(n, 0), 0, 0
    C = sp.Matrix.hstack(*columns)
    R = C * (C.T * C).inv() * C.T
    denominator = lcm(*(int(v.q) for v in A))
    mu = 1 / (sp.Integer(denominator) ** len(columns) * H ** (len(columns) - 1))
    tau = mu**2 / (16 * n**2 * H)
    Q, B, steps = sp.eye(n), A.copy(), 0
    while n > 1:
        p, q = max(combinations(range(n), 2), key=lambda ij: abs(B[ij]))
        b = B[p, q]
        if abs(b) <= tau:
            break
        delta = B[q, q] - B[p, p]
        endpoint = -sp.sign(b * delta) / 2 if delta else sp.Rational(1, 2)
        left, right = sorted([sp.S.Zero, endpoint])

        def f(t):
            return b * (1 - 6 * t**2 + t**4) + 2 * delta * t * (1 - t**2)

        fl = f(left)
        while right - left > tau / (8 * H):
            middle = (left + right) / 2
            fm = f(middle)
            if fm == 0:
                left = right = middle
                break
            if sp.sign(fm) == sp.sign(fl):
                left, fl = middle, fm
            else:
                right = middle
        t = (left + right) / 2
        c, s = (1 - t*t) / (1 + t*t), 2*t / (1 + t*t)
        G = sp.eye(n)
        G[p, p] = G[q, q] = c
        G[p, q], G[q, p] = -s, s
        old_energy = sum(B[i, j]**2 for i in range(n) for j in range(n) if i != j)
        B = G.T * B * G
        Q = Q * G
        assert abs(B[p, q]) <= tau / 2
        new_energy = sum(B[i, j]**2 for i in range(n) for j in range(n) if i != j)
        assert new_energy <= old_energy - 3*b*b/2
        steps += 1
        assert steps < 10000
    selected = [i for i in range(n) if B[i, i] < -mu/2]
    U = R * Q[:, selected]
    assert Q.T * Q == sp.eye(n)
    assert Q.T * A * Q == B
    assert R * U == U
    assert U.rank() == len(selected)
    psd(sp.eye(U.cols) - U.T * U)
    psd(A + 2*H*U*U.T)
    for v in A.nullspace():
        assert U.T * v == sp.zeros(U.cols, 1)
    return U, steps, max((max(int(v.p).bit_length(), int(v.q).bit_length()) for v in U), default=0)


def main():
    q = sp.Matrix([[sp.Rational(3, 5), -sp.Rational(4, 5), 0],
                   [sp.Rational(4, 5), sp.Rational(3, 5), 0], [0, 0, 1]])
    r = sp.Matrix([[1, 0, 0], [0, sp.Rational(5, 13), -sp.Rational(12, 13)],
                   [0, sp.Rational(12, 13), sp.Rational(5, 13)]])
    C = sp.Matrix([[1, 2], [3, 1], [2, -1]])
    M = sp.Matrix([[1, 1, 0], [0, 1, 1], [1, 0, 1]])
    cases = [
        ("zero", sp.zeros(3), 0),
        ("scalar-negative", sp.Matrix([[-3]]), 1),
        ("psd-singular", sp.Matrix([[1, 1], [1, 1]]), 0),
        ("mixed", sp.Matrix([[0, 1], [1, 0]]), 1),
        ("singular-negative-rotated", sp.Matrix([[-1, -1], [-1, -1]]), 1),
        ("repeated-negative", -sp.eye(3), 3),
        ("two-negative-mixed", M*sp.diag(-1, -2, 3)*M.T, 2),
        ("mixed-singular-dense", q*r*sp.diag(-1, 0, 2)*r.T*q.T, 1),
        ("mixed-singular-oblique", C*sp.diag(-1, 1)*C.T, 1),
        ("ill-conditioned-singular-oblique", C*sp.diag(-1, sp.Rational(1, 4096))*C.T, 1),
        ("small-positive-eigenvalue", sp.Matrix([[1, 1], [1, 1]])/8192 - sp.Matrix([[1, -1], [-1, 1]]), 1),
        ("small-negative-eigenvalue", sp.Matrix([[1, 1], [1, 1]]) - sp.Matrix([[1, -1], [-1, 1]])/8192, 1),
    ]
    total = 0
    for name, A, k in cases:
        U, steps, bits = normalize(A)
        assert U.cols == k
        total += steps
        print(f"PASS {name}: inertia={k}, rotations={steps}, output_bits_per_entry<={bits}", flush=True)
    # Exact kernel leakage counterexample used in the proof.
    v = sp.Matrix([sp.Rational(3, 5), sp.Rational(4, 5)])
    assert (sp.diag(-1, 0) + 2*v*v.T).det() == -sp.Rational(32, 25)
    print(f"PASS: {len(cases)} normalization cases, {total} rational rotations, kernel-leakage counterexample")


if __name__ == "__main__":
    main()
