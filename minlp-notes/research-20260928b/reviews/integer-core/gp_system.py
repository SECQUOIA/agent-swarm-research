"""Reviewer checks for Theorem 2.3 (separation via Glaser-Pfetsch).

System (2) of Glaser-Pfetsch (arXiv 2308.04320, p. 5, read from the local PDF):
  (2a) x_il + x_jl <= 2 - z_ij      for all pairs {i,j}, colours l in [k-1]
  (2b) sum_l x_il >= 1               for all vertices i
  (2c) y_i + y_j <= 1 + z_ij         for all pairs {i,j}
  (2d) sum_i y_i >= k
  (2e) x, y, z in [0,1]  (box rows)
with k = floor((1/8)(r / log2 r)^{2/3}).

Part 1 (encoding sizes).  n = r(k-1) + r + C(r,2) variables, m rows.  GP state L = Theta(n^2).
  We print log(L)/log(n) for a dense encoding (m+1)(n+1) and a sparse one (nonzeros), for large r.
Part 2 (the reduction used in Theorem 2.3(b)).  For a small instance (r = 4, k = 3, n = 18) we
  check exactly: every binary w violates some row by an integer >= 1, so t* = min_{w in Z^n}
  max_j (a_j.w - b_j) >= 1 (non-binary integer points violate a box row by >= 1); the LP
  relaxation P_r is nonempty (exact feasible point); for psi(t) = t^2 (not monotone on R) the
  projected relaxation of min psi(t) s.t. Aw - b <= t 1 is max(0, M(w))^2, equal to 0 = psi(0)
  on P_r, so the leaf argument of Theorem 2.3(b) goes through for eps < 1 even though psi is not
  "strictly increasing".
"""
import math
from fractions import Fraction as F
from itertools import combinations
import numpy as np


def sizes(r):
    k = math.floor((r / math.log2(r)) ** (2 / 3) / 8)
    pairs = r * (r - 1) // 2
    n = r * (k - 1) + r + pairs
    m_nonbox = pairs * (k - 1) + r + pairs + 1
    m = m_nonbox + 2 * n
    nnz = 3 * pairs * (k - 1) + r * (k - 1) + 3 * pairs + r + 2 * n
    return k, n, m, nnz


def part1():
    print("== Part 1: sizes of GP system (2) ==")
    for e in (4, 6, 8, 10, 12, 15, 20):
        r = 10 ** e
        k, n, m, nnz = sizes(r)
        dense = (m + 1) * (n + 1)
        print(f"r=1e{e:<2d} k={k:<8d} n={n:.3e} m={m:.3e}  log L_dense/log n = {math.log(dense)/math.log(n):.3f}  "
              f"log L_sparse/log n = {math.log(nnz)/math.log(n):.3f}")
    print("   (as r -> inf the dense ratio tends to 7/3 and the sparse ratio to 4/3, since m/n ~ k grows)")


def build(r, k):
    pairs = list(combinations(range(r), 2))
    nx, ny = r * (k - 1), r
    n = nx + ny + len(pairs)
    X = lambda i, l: i * (k - 1) + l
    Y = lambda i: nx + i
    Z = {p: nx + ny + t for t, p in enumerate(pairs)}
    rows, rhs = [], []
    for (i, j) in pairs:
        for l in range(k - 1):
            a = [0] * n
            a[X(i, l)] = 1; a[X(j, l)] = 1; a[Z[(i, j)]] = 1
            rows.append(a); rhs.append(2)
    for i in range(r):
        a = [0] * n
        for l in range(k - 1):
            a[X(i, l)] = -1
        rows.append(a); rhs.append(-1)
    for (i, j) in pairs:
        a = [0] * n
        a[Y(i)] = 1; a[Y(j)] = 1; a[Z[(i, j)]] = -1
        rows.append(a); rhs.append(1)
    a = [0] * n
    for i in range(r):
        a[Y(i)] = -1
    rows.append(a); rhs.append(-k)
    nonbox = len(rows)
    for v in range(n):
        a = [0] * n; a[v] = 1; rows.append(a); rhs.append(1)
        a = [0] * n; a[v] = -1; rows.append(a); rhs.append(0)
    return np.array(rows, dtype=np.int64), np.array(rhs, dtype=np.int64), n, nonbox, (X, Y, Z, pairs)


def part2(r=4, k=3):
    print(f"== Part 2: small instance r={r}, k={k} ==")
    A, b, n, nonbox, (X, Y, Z, pairs) = build(r, k)
    An, bn = A[:nonbox], b[:nonbox]
    best = None
    cnt_at_best = 0
    chunk = 1 << 14
    for start in range(0, 1 << n, chunk):
        idx = np.arange(start, start + chunk, dtype=np.int64)
        W = ((idx[:, None] >> np.arange(n)) & 1).astype(np.int64)
        M = (W @ An.T - bn).max(axis=1)
        mv = int(M.min())
        if best is None or mv < best:
            best, cnt_at_best = mv, int((M == mv).sum())
        elif mv == best:
            cnt_at_best += int((M == mv).sum())
    print(f"   n={n}, rows: {nonbox} non-box + {2*n} box = {len(b)}; min over {{0,1}}^n of max_j(a_j.w - b_j) = {best} "
          f"(attained by {cnt_at_best} binary points) -> t* = {best} >= 1: {best >= 1}")
    # exact LP-feasible point: x = 1/(k-1), y = k/r, z = 1/2 ... check with Fractions
    w = [F(0)] * n
    for i in range(r):
        for l in range(k - 1):
            w[X(i, l)] = F(1, k - 1)
        w[Y(i)] = F(k, r)
    for p in pairs:
        w[Z[p]] = F(1, 2)
    Mw = max(sum(F(int(A[j, v])) * w[v] for v in range(n) if A[j, v]) - int(b[j]) for j in range(len(b)))
    print(f"   exact point w0 (x=1/(k-1), y=k/r, z=1/2): max_j(a_j.w0 - b_j) = {Mw} -> P_r nonempty: {Mw <= 0}")
    print(f"   psi(t)=t^2: projected relaxation phi(w) = max(0, M(w))^2; phi(w0) = {max(F(0), Mw)**2} = psi(0); "
          f"OPT = t*^2 = {best**2}; leaves with bound >= OPT - eps > 0 miss P_r for every eps < {best**2}")


if __name__ == "__main__":
    part1()
    part2()
