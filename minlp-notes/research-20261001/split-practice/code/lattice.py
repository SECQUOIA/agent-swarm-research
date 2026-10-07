"""Lattice tools for split separation.

Notation (split note, research-20260928b/side-results/split-separation-np-complete.md):
  q_X(v) = v^T X v + v^T X e0,  u = 2v + e0,  q_X(v) = (u^T X u - X00)/4.
For X = B^T B with X00 = 1 and lattice L = B Z^N, q_X(v) = |Bv + b0/2|^2 - 1/4,
so the maximum violation is 1/4 - dist(-b0/2, L)^2 (CVP with target -b0/2).

Contents
  lll_gram_float     floating LLL on a Gram matrix, returns unimodular U
  cvp_enum           Schnorr-Euchner enumeration for min (z-c)^T A (z-c), z in Z^r
  sep_pd_float       exact (up to floating point) max-violation split for PD X
  thm3_exact         Theorem 3: exact rational separation at rank r (HNF + LLL + enum)
  thm4_rank1         Theorem 4: closed-form most violated split for rank-1 rational X
"""
import math
import time
from fractions import Fraction as F

import numpy as np


# ---------------------------------------------------------------- LLL
def lll_gram_float(A, delta=0.99, max_iter=10**6):
    """LLL on the lattice with Gram matrix A (r x r, PD), in floating point,
    with Gram-Schmidt data recomputed by QR.  Returns an integer unimodular U
    (numpy object array of python ints) such that U^T A U is LLL-reduced."""
    A = np.array(A, dtype=float)
    return lll_cols(np.linalg.cholesky(A).T.copy(), delta, max_iter)


def lll_cols(B, delta=0.99, max_iter=10**6):
    """Floating LLL on the columns of B (linearly independent).  Returns U."""
    B = np.array(B, dtype=float)
    r = B.shape[1]
    U = np.eye(r, dtype=object)
    for i in range(r):
        for j in range(r):
            U[i, j] = int(i == j)
    k = 1; it = 0
    while k < r and it < max_iter:
        it += 1
        R = np.linalg.qr(B[:, :k + 1], mode="r")
        for j in range(k - 1, -1, -1):
            m = int(np.rint(R[j, k] / R[j, j]))
            if m:
                B[:, k] -= m * B[:, j]
                U[:, k] = U[:, k] - m * U[:, j]
                R[:j + 1, k] -= m * R[:j + 1, j]
        if delta * R[k - 1, k - 1] ** 2 > R[k - 1, k] ** 2 + R[k, k] ** 2:
            B[:, [k - 1, k]] = B[:, [k, k - 1]]
            U[:, [k - 1, k]] = U[:, [k, k - 1]]
            k = max(k - 1, 1)
        else:
            k += 1
    return U


def lll_gram_exact(A, delta=F(99, 100)):
    """Exact LLL on a rational Gram matrix A (list of lists of Fractions).
    Returns integer unimodular U (list of lists) with U^T A U LLL-reduced."""
    r = len(A)
    G = [row[:] for row in A]
    U = [[int(i == j) for j in range(r)] for i in range(r)]

    def gso():
        mu = [[F(0)] * r for _ in range(r)]; Bn = [F(0)] * r
        for i in range(r):
            for j in range(i):
                mu[i][j] = (G[i][j] - sum(mu[j][k] * mu[i][k] * Bn[k] for k in range(j))) / Bn[j]
            Bn[i] = G[i][i] - sum(mu[i][k] ** 2 * Bn[k] for k in range(i))
        return mu, Bn

    def colop(k, j, m):  # b_k -= m b_j
        for row in U:
            row[k] -= m * row[j]
        for i in range(r):
            G[i][k] -= m * G[i][j]
        for i in range(r):
            G[k][i] -= m * G[j][i]

    def swap(k):
        for row in U:
            row[k - 1], row[k] = row[k], row[k - 1]
        G[k - 1], G[k] = G[k], G[k - 1]
        for row in G:
            row[k - 1], row[k] = row[k], row[k - 1]

    mu, Bn = gso(); k = 1
    while k < r:
        for j in range(k - 1, -1, -1):
            m = round(mu[k][j])
            if m:
                colop(k, j, m)
                mu, Bn = gso()
        if Bn[k] < (delta - mu[k][k - 1] ** 2) * Bn[k - 1]:
            swap(k); mu, Bn = gso(); k = max(k - 1, 1)
        else:
            k += 1
    return U


def lll_basis_float(B, delta=0.99):
    """LLL on the columns of a real basis matrix B (d x r) by the
    numerically stable route: QR-based size reduction.  Returns U."""
    A = B.T @ B
    return lll_gram_float(A, delta)


# ---------------------------------------------------------------- enumeration
def cvp_enum(A, c, radius2, max_nodes=10**8, collect=False, shrink=True):
    """Minimise (z-c)^T A (z-c) over z in Z^r subject to value < radius2.
    Schnorr-Euchner enumeration (zig-zag order, pruning by the current best
    when shrink=True).  Returns (z, val, nodes, complete, found); `found`
    lists every point with value < radius2 visited (all of them if
    shrink=False and complete)."""
    import sys
    A = np.asarray(A, float); c = np.asarray(c, float)
    r = len(c)
    R = np.linalg.cholesky(A).T
    d = np.diag(R) ** 2
    mu = R / np.diag(R)[:, None]
    state = dict(best=None, bestv=radius2, nodes=0, complete=True)
    found = []
    z = np.zeros(r, dtype=np.int64)
    sys.setrecursionlimit(max(10000, 4 * r + 100))

    def rec(k, partial):
        state["nodes"] += 1
        if state["nodes"] > max_nodes:
            state["complete"] = False
            return
        ck = c[k] - float(np.dot(mu[k, k + 1:], z[k + 1:] - c[k + 1:]))
        z0 = int(np.floor(ck + 0.5))
        s = 1 if ck >= z0 else -1
        step = 0
        while True:
            off = (step + 1) // 2
            zk = z0 + (off * s if step % 2 == 1 else -off * s)
            y = zk - ck
            val = partial + d[k] * y * y
            if val >= state["bestv"]:
                # candidates come in order of increasing |zk - ck|
                break
            z[k] = zk
            if k == 0:
                if collect:
                    found.append((val, z.copy()))
                state["best"] = (z.copy(), val)
                if shrink:
                    state["bestv"] = val
            else:
                rec(k - 1, val)
                if not state["complete"]:
                    return
            step += 1

    rec(r - 1, 0.0)
    if state["best"] is None:
        return None, None, state["nodes"], state["complete"], found
    return state["best"][0], state["best"][1], state["nodes"], state["complete"], found


def _enum_simple(A, c, radius2, max_nodes=10**8):
    """Reference Fincke-Pohst (no zig-zag) for testing."""
    A = np.asarray(A, float); c = np.asarray(c, float); r = len(c)
    L = np.linalg.cholesky(A); R = L.T
    d = np.diag(R) ** 2; mu = R / np.diag(R)[:, None]
    best = [None, radius2]; nodes = [0]
    z = np.zeros(r, dtype=np.int64)

    def rec(k, partial):
        nodes[0] += 1
        ck = c[k] - sum(mu[k, j] * (z[j] - c[j]) for j in range(k + 1, r))
        rad = math.sqrt(max(best[1] - partial, 0) / d[k])
        for zk in range(math.ceil(ck - rad), math.floor(ck + rad) + 1):
            z[k] = zk
            val = partial + d[k] * (zk - ck) ** 2
            if val < best[1]:
                if k == 0:
                    best[0] = z.copy(); best[1] = val
                else:
                    rec(k - 1, val)
    rec(r - 1, 0.0)
    return best[0], best[1], nodes[0]


# ---------------------------------------------------------------- PD separation
def sep_pd_float(X, max_nodes=10**7, margin=0.0):
    """Most violated split of a PD (floating) X with X00 = 1, over all of Z^N.
    CVP in the lattice with Gram X, target -e0/2:  q(v) = (v+e0/2)^T X (v+e0/2) - 1/4.
    Returns dict with v, q, nodes, complete, time."""
    t = time.time()
    X = np.asarray(X, float)
    N = X.shape[0]
    U = lll_gram_float(X)
    Uf = np.array(U, dtype=float)
    A = Uf.T @ X @ Uf
    target = np.zeros(N); target[0] = -0.5
    c = np.linalg.solve(Uf, target)
    z, val, nodes, complete = cvp_enum_c(A, c, 0.25 - margin, max_nodes=max_nodes)
    if z is None:
        return dict(v=None, q=0.0, nodes=nodes, complete=complete, time=time.time() - t)
    v = (U @ np.array([int(a) for a in z], dtype=object))
    v = np.array([int(a) for a in v], dtype=object)
    vf = v.astype(float)
    q = float(vf @ X @ vf + vf @ X[:, 0])
    return dict(v=v, q=q, nodes=nodes, complete=complete, time=time.time() - t)


# ---------------------------------------------------------------- exact rational tools
def frac_matrix(M):
    return [[F(x) for x in row] for row in M]


def lemma4(X):
    """Symmetric elimination (Lemma 4 of the split note) in exact arithmetic.
    Returns ('psd', K) or ('notpsd', z)."""
    N = len(X)
    S = [row[:] for row in X]
    act = list(range(N)); K = []
    # we keep S as full matrix and eliminate in place on active indices
    Z = {i: {i: F(1)} for i in range(N)}  # not needed for PSD branch
    while act:
        neg = [i for i in act if S[i][i] < 0]
        if neg:
            return ("notpsd", neg[0])
        piv = None
        for i in act:
            if S[i][i] == 0 and any(S[i][j] != 0 for j in act):
                return ("notpsd", i)
        cand = [i for i in act if S[i][i] > 0]
        if not cand:
            break
        p = cand[0]
        K.append(p); act.remove(p)
        for i in act:
            f = S[i][p] / S[p][p]
            if f != 0:
                for j in act:
                    S[i][j] -= f * S[p][j]
    return ("psd", K)


def mat_inv_frac(A):
    n = len(A)
    M = [row[:] + [F(int(i == j)) for j in range(n)] for i, row in enumerate(A)]
    for col in range(n):
        piv = next(r for r in range(col, n) if M[r][col] != 0)
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        M[col] = [x / pv for x in M[col]]
        for r in range(n):
            if r != col and M[r][col] != 0:
                f = M[r][col]
                M[r] = [a - f * b for a, b in zip(M[r], M[col])]
    return [row[n:] for row in M]


def col_hnf(M):
    """Integer matrix M (r x N, python ints, rank r).  Column operations with a
    unimodular U so that M U = [H | 0], H lower triangular r x r with
    positive diagonal and 0 <= H[i][j] < H[i][i] for j < i.
    Returns H (r x r), U (N x N)."""
    r = len(M); N = len(M[0])
    A = [row[:] for row in M]
    U = [[int(i == j) for j in range(N)] for i in range(N)]

    def colop(j, k, a, b, c, d):
        # (col_j, col_k) <- (a col_j + b col_k, c col_j + d col_k)
        for row in A:
            x, y = row[j], row[k]
            row[j], row[k] = a * x + b * y, c * x + d * y
        for row in U:
            x, y = row[j], row[k]
            row[j], row[k] = a * x + b * y, c * x + d * y

    piv_col = 0
    for i in range(r):
        if piv_col >= N:
            break
        for k in range(piv_col + 1, N):
            if A[i][k] == 0:
                continue
            a, b = A[i][piv_col], A[i][k]
            g, s, t = _egcd(a, b)
            # new col_piv = s*col_piv + t*col_k  (entry g); new col_k = (-b/g) col_piv + (a/g) col_k (entry 0)
            colop(piv_col, k, s, t, -b // g, a // g)
        if A[i][piv_col] != 0:
            if A[i][piv_col] < 0:
                for row in A:
                    row[piv_col] = -row[piv_col]
                for row in U:
                    row[piv_col] = -row[piv_col]
            # Reduce the entries left of this pivot, retaining all earlier
            # rows because the pivot column is zero in those rows.
            for j in range(piv_col):
                m = A[i][j] // A[i][piv_col]
                if m:
                    for row in A:
                        row[j] -= m * row[piv_col]
                    for row in U:
                        row[j] -= m * row[piv_col]
            piv_col += 1
    H = [row[:r] for row in A]
    return H, U


def _egcd(a, b):
    """g = s a + t b, g = gcd >= 0 (with g > 0 unless a = b = 0)."""
    old_r, rr = a, b; old_s, s = 1, 0; old_t, t = 0, 1
    while rr != 0:
        qq = old_r // rr
        old_r, rr = rr, old_r - qq * rr
        old_s, s = s, old_s - qq * s
        old_t, t = t, old_t - qq * t
    if old_r < 0:
        old_r, old_s, old_t = -old_r, -old_s, -old_t
    return old_r, old_s, old_t


def _lcm(a, b):
    return a * b // math.gcd(a, b)


def thm3_exact(X, max_nodes=10**7, want_all=False, factor=None):
    """Fixed-rank separation with exact algebra and floating CVP enumeration.
    X is rational PSD (Fractions, X00 = 1). Returns dict(v, q, rank, flags).
    Returned q is exact; global optimality relies on finished floating
    enumeration/verification, unless q = -1/4 certifies the lower bound.
    """
    t0 = time.time()
    N = len(X)
    if factor is None:
        st, K = lemma4(X)
        if st != "psd":
            raise ValueError("not PSD")
        r = len(K)
        P = [X[k][:] for k in K]
        XKK = [[X[a][b] for b in K] for a in K]
        G = mat_inv_frac(XKK)
    else:
        # X = P^T G P supplied by the caller (P: r x N, G: r x r PD), X00 = 1
        P, G = factor
        r = len(P)
    w0 = [P[k][0] for k in range(r)]
    # P = content * M with M an integer matrix whose entries have gcd 1
    den = 1; num = 0
    for row in P:
        for x in row:
            den = _lcm(den, x.denominator)
    for row in P:
        for x in row:
            num = math.gcd(num, int(x * den))
    content = F(num, den)
    delta = den
    M = [[int(x / content) for x in row] for row in P]
    # Pre-reduce the integer graph lattice before HNF. Its first N entries
    # track a unimodular change of coordinates in Z^N, while the last r
    # entries penalize nonzero images. This avoids huge intermediate kernel
    # bases; HNF still establishes the full image and saturated kernel.
    if N > r:
        graph = [[int(i == j) for j in range(N)] + [10**6 * M[k][i] for k in range(r)]
                 for i in range(N)]
        graph = lll_rows_exact(graph)
        graph.sort(key=lambda row: not any(row[N:]))
        pre = [[graph[j][i] for j in range(N)] for i in range(N)]
        reduced_M = [[sum(M[k][i] * pre[i][j] for i in range(N))
                      for j in range(N)] for k in range(r)]
        H, U0 = col_hnf(reduced_M)
        U = [[sum(pre[i][k] * U0[k][j] for k in range(N))
              for j in range(N)] for i in range(N)]
    else:
        H, U = col_hnf(M)
    T = [[U[i][j] for j in range(r)] for i in range(N)]        # N x r
    Kern = [[U[i][j] for j in range(r, N)] for i in range(N)]  # N x (N-r)
    W = [[content * H[i][j] for j in range(r)] for i in range(r)]  # basis columns
    # Gram A = W^T G W
    GW = [[sum(G[i][k] * W[k][j] for k in range(r)) for j in range(r)] for i in range(r)]
    A = [[sum(W[k][i] * GW[k][j] for k in range(r)) for j in range(r)] for i in range(r)]
    # target in coordinates: solve W c = -w0/2
    Winv = mat_inv_frac(W)
    c = [sum(Winv[i][k] * (-w0[k] / 2) for k in range(r)) for i in range(r)]
    t1 = time.time()
    Ulist = lll_gram_exact(A)
    A2x = [[sum(Ulist[k][i] * A[k][l] * Ulist[l][j] for k in range(r) for l in range(r))
            for j in range(r)] for i in range(r)]
    A2 = np.array([[float(a) for a in row] for row in A2x])
    Uinv = mat_inv_frac([[F(a) for a in row] for row in Ulist])
    cf = np.array([float(sum(Uinv[i][k] * c[k] for k in range(r))) for i in range(r)])
    # floating minimum (C enumeration), then all points within 1e-9 of it
    # (Python enumeration, collect mode), each verified in exact arithmetic
    z, val, nodes, complete = cvp_enum_c(A2, cf, 0.25 + 1e-9, max_nodes=max_nodes)
    first_complete = complete
    second_complete = True
    found = []
    if z is not None:
        _, _, n2, c2, found = cvp_enum(A2, cf, val + 1e-9 * (1 + abs(val)), max_nodes=2 * 10**5,
                                       collect=True, shrink=False)
        nodes += n2
        second_complete = c2
        complete = first_complete and second_complete
        # A capped collection can miss the first enumeration's minimizer.
        found.append((val, z))
    t2 = time.time()
    best = None
    # Verify every collected candidate, with one common denominator instead
    # of millions of Fraction operations. In reduced coordinates q(z) is
    # z^T A2 z - 2 z^T A2 c2; the constant is zero since X00 = 1.
    c2x = [sum(Uinv[i][k] * c[k] for k in range(r)) for i in range(r)]
    linear = [-2 * sum(A2x[i][j] * c2x[j] for j in range(r)) for i in range(r)]
    qden = 1
    for a in [e for row in A2x for e in row] + linear:
        qden = _lcm(qden, a.denominator)
    terms = [(i, j, int(A2x[i][j] * qden) * (1 if i == j else 2))
             for i in range(r) for j in range(i, r) if A2x[i][j]]
    linint = [int(a * qden) for a in linear]
    for _, zz in found:
        z = [int(a) for a in zz]
        numerator = sum(a * z[i] * z[j] for i, j, a in terms) + sum(a * b for a, b in zip(linint, z))
        if numerator < 0 and (best is None or numerator < best[0]):
            best = (numerator, z)
            if 4 * numerator == -qden:
                break  # Proposition C(a) supplies an exact lower bound.
    res = dict(rank=r, delta=delta, nodes=nodes, complete=complete,
               first_complete=first_complete, second_complete=second_complete,
               optimum_certified=best is not None and 4 * best[0] == -qden,
               t_setup=t1 - t0, t_enum=t2 - t1, time=time.time() - t0)
    if best is None:
        res.update(v=None, q=F(0))
        return res
    numerator, z = best
    qq = F(numerator, qden)
    zint = [sum(Ulist[i][j] * z[j] for j in range(r)) for i in range(r)]
    v = [sum(T[i][j] * zint[j] for j in range(r)) for i in range(N)]
    res.update(v=v, q=qq, vmax_raw=max(abs(a) for a in v))
    # shorten v modulo the integer kernel of P (does not change q)
    if N > r:
        v2 = shorten_mod_kernel(v, Kern)
        assert all(sum(M[k][i] * (v2[i] - v[i]) for i in range(N)) == 0 for k in range(r))
        res.update(v=v2, vmax=max(abs(a) for a in v2))
    else:
        res.update(vmax=res["vmax_raw"])
    res["time"] = time.time() - t0
    return res


def lll_rows_exact(rows, delta=F(3, 4)):
    """LLL of independent integer rows, with Fraction GSO and integer rounding.

    Update GSO after row operations and swaps instead of recomputing it.
    No floating conversion is used, including for nearest-integer choices.
    """
    rows = [list(row) for row in rows]
    r = len(rows)
    mu = [[F(0)] * r for _ in range(r)]
    orthogonal, norms = [], []
    for i, row in enumerate(rows):
        b = [F(a) for a in row]
        for j, bs in enumerate(orthogonal):
            mu[i][j] = sum(a * c for a, c in zip(row, bs)) / norms[j]
            b = [a - mu[i][j] * c for a, c in zip(b, bs)]
        orthogonal.append(b)
        norms.append(sum(a * a for a in b))
        if norms[-1] == 0:
            raise ValueError("dependent LLL rows")

    def reduce(k, j):
        m = round(mu[k][j])
        rows[k] = [a - m * b for a, b in zip(rows[k], rows[j])]
        for i in range(j):
            mu[k][i] -= m * mu[j][i]
        mu[k][j] -= m

    k = 1
    while k < r:
        reduce(k, k - 1)
        if norms[k] >= (delta - mu[k][k - 1] ** 2) * norms[k - 1]:
            for j in range(k - 2, -1, -1):
                reduce(k, j)
            k += 1
        else:
            nu = mu[k][k - 1]
            alpha = norms[k] + nu ** 2 * norms[k - 1]
            beta = norms[k - 1] / alpha
            mu[k][k - 1] = nu * beta
            norms[k] *= beta
            norms[k - 1] = alpha
            rows[k], rows[k - 1] = rows[k - 1], rows[k]
            mu[k][:k - 1], mu[k - 1][:k - 1] = mu[k - 1][:k - 1], mu[k][:k - 1]
            for i in range(k + 1, r):
                xi = mu[i][k]
                mu[i][k] = mu[i][k - 1] - nu * xi
                mu[i][k - 1] = mu[k][k - 1] * mu[i][k] + xi
            k = max(1, k - 1)
    assert all(abs(mu[i][j]) <= F(1, 2) for i in range(r) for j in range(i))
    assert all(norms[i] >= (delta - mu[i][i - 1] ** 2) * norms[i - 1] for i in range(1, r))
    return rows


def shorten_mod_kernel(v, Kern):
    """Reduce an integer vector v modulo the lattice spanned by the columns of
    Kern (integer), by exact LLL followed by exact Babai nearest-plane.
    Reduction preserves the coset; it does not prove a shortest representative."""
    if not Kern or not Kern[0]:
        return v
    rows = lll_rows_exact(zip(*Kern))
    orthogonal = []
    norms = []
    for row in rows:
        b = [F(a) for a in row]
        for bs, norm in zip(orthogonal, norms):
            mu = sum(a * c for a, c in zip(row, bs)) / norm
            b = [a - mu * c for a, c in zip(b, bs)]
        orthogonal.append(b)
        norms.append(sum(a * a for a in b))
    vv = list(v)
    for row, bs, norm in reversed(list(zip(rows, orthogonal, norms))):
        m = round(sum(a * b for a, b in zip(vv, bs)) / norm)
        vv = [a - m * b for a, b in zip(vv, row)]
    # Embed the affine coset: a reduced row whose last entry is +/-1
    # gives another representative. The Babai result remains a candidate.
    embedded = lll_rows_exact([row + [0] for row in rows] + [vv + [1]])
    candidates = [vv] + [[a * row[-1] for a in row[:-1]]
                         for row in embedded if abs(row[-1]) == 1]
    return min(candidates, key=lambda row: (sum(a * a for a in row), max(map(abs, row))))


def q_exact(X, v):
    N = len(X)
    return sum(F(v[i]) * X[i][j] * v[j] for i in range(N) for j in range(N)) + \
        sum(F(v[i]) * X[i][0] for i in range(N))


# ---------------------------------------------------------------- Theorem 4
def thm4_rank1(x):
    """x: list of Fractions (the rank-1 point X = l(x)).  Returns the most
    violated split v and its value q = -floor(D^2/4)/D^2 (or None)."""
    D = 1
    for a in x:
        D = _lcm(D, F(a).denominator)
    if D == 1:
        return None, F(0), D
    p = [D] + [int(F(a) * D) for a in x]
    target = -(D // 2)
    # extended Euclid over the vector p (gcd(p) = 1)
    g, coef = p[0], [1] + [0] * (len(p) - 1)
    for i in range(1, len(p)):
        g2, s, t = _egcd(g, p[i])
        coef = [s * cc for cc in coef]
        coef[i] = t
        g = g2
    assert g == 1
    v = [target * cc for cc in coef]
    m = sum(a * b for a, b in zip(p, v))
    assert m == target
    q = F(m * (m + D), D * D)
    return v, q, D


# ---------------------------------------------------------------- ratio separation
def sep_ratio(Y, eta0=None, tol=1e-10, max_iter=60, max_nodes=10**7):
    """Most violated split in the normalised sense  max_v -q(v)/|w|^2  (w = v_1..n),
    by Dinkelbach iteration: each step solves min_v q(v) + eta |w|^2 exactly,
    i.e. exact split separation for the positive definite matrix
    Y + eta * diag(0, 1, ..., 1).  Exact up to floating point for PSD Y.
    Returns dict(v, q, ratio, iters, nodes, time, complete)."""
    t0 = time.time()
    Y = np.asarray(Y, float)
    w_, V_ = np.linalg.eigh((Y + Y.T) / 2)
    Y = (V_ * np.maximum(w_, 0)) @ V_.T
    # restore Y00 = 1 by the congruence diag(1/sqrt(Y00), 1, ..., 1), which
    # keeps Y PSD (resetting the entry alone can make Y indefinite; this
    # happened at dm_QUTO_t2_n30_p25_s0 root, where Y00 = 1 + 4.4e-7)
    s = 1.0 / np.sqrt(Y[0, 0])
    Y[0, :] *= s; Y[:, 0] *= s
    N = Y.shape[0]
    # start: best elementary split ratio (|w|^2 = 1), or eta0
    x = Y[0, 1:]; d = np.diag(Y)[1:]
    v0 = np.floor(-x - 0.5 + 0.5)  # candidate rounding, both checked below
    best_v, best_ratio = None, 0.0
    for i in range(N - 1):
        for s in (np.floor(x[i]), np.ceil(x[i])):
            # split x_i <= s-1 or x_i >= s  ->  v = (-s, e_i) with (w=e_i, s'=s-1)
            vv = np.zeros(N); vv[i + 1] = 1; vv[0] = -s
            qq = vv @ Y @ vv + vv @ Y[:, 0]
            if -qq > best_ratio:
                best_ratio, best_v = -qq, vv.astype(np.int64)
    eta = max(best_ratio, eta0 or 1e-6)
    iters = 0; nodes = 0; complete = True
    cands = [] if best_v is None else [[int(a) for a in best_v]]
    while iters < max_iter:
        iters += 1
        Xe = Y.copy(); Xe[np.arange(1, N), np.arange(1, N)] += eta
        res = sep_pd_float(Xe, max_nodes=max_nodes)
        nodes += res["nodes"]; complete &= res["complete"]
        if res["v"] is None or res["q"] >= -tol:
            break
        vv = np.array(res["v"], dtype=float)
        qq = float(vv @ Y @ vv + vv @ Y[:, 0])
        w2 = float(vv[1:] @ vv[1:])
        ratio = -qq / w2 if w2 > 0 else 0.0
        if ratio <= eta * (1 + 1e-12):
            break
        best_v, best_ratio, eta = res["v"], ratio, ratio
        cands.append([int(a) for a in res["v"]])
    q = None
    if best_v is not None:
        vv = np.array(best_v, dtype=float)
        q = float(vv @ Y @ vv + vv @ Y[:, 0])
    return dict(v=best_v, q=q, ratio=best_ratio, iters=iters, nodes=nodes,
                complete=complete, time=time.time() - t0, cands=cands)


# ---------------------------------------------------------------- C enumeration
_LIB = None


def _lib():
    global _LIB
    if _LIB is None:
        import ctypes, os
        here = os.path.dirname(os.path.abspath(__file__))
        so = os.path.join(here, "libenum.so")
        if not os.path.exists(so) or os.path.getmtime(so) < os.path.getmtime(os.path.join(here, "enum.c")):
            import subprocess
            subprocess.run(["gcc", "-O2", "-shared", "-fPIC", "-o", so, os.path.join(here, "enum.c"), "-lm"],
                           check=True)
        L = ctypes.CDLL(so)
        dp = ctypes.POINTER(ctypes.c_double); lp = ctypes.POINTER(ctypes.c_long)
        ip = ctypes.POINTER(ctypes.c_int)
        L.se_enum.restype = ctypes.c_long
        L.se_enum.argtypes = [ctypes.c_int, dp, dp, dp, ctypes.c_double, ctypes.c_long, lp, dp, ip, ip]
        _LIB = L
    return _LIB


def cvp_enum_c(A, c, radius2, max_nodes=10**9):
    """C version of cvp_enum (minimum only).  Returns (z, val, nodes, complete)."""
    import ctypes
    A = np.asarray(A, float); c = np.ascontiguousarray(c, float); r = len(c)
    R = np.linalg.cholesky(A).T
    d = np.ascontiguousarray(np.diag(R) ** 2)
    mu = np.ascontiguousarray(R / np.diag(R)[:, None])
    z = np.zeros(r, dtype=np.int64)
    val = ctypes.c_double(0); found = ctypes.c_int(0); comp = ctypes.c_int(0)
    L = _lib()
    dp = ctypes.POINTER(ctypes.c_double)
    nodes = L.se_enum(r, mu.ctypes.data_as(dp), d.ctypes.data_as(dp), c.ctypes.data_as(dp),
                      float(radius2), int(max_nodes), z.ctypes.data_as(ctypes.POINTER(ctypes.c_long)),
                      ctypes.byref(val), ctypes.byref(found), ctypes.byref(comp))
    if not found.value:
        return None, None, nodes, bool(comp.value)
    return z, val.value, nodes, bool(comp.value)
