"""Exact verification tools (rational arithmetic only).

in_PBH(n, z): decides exactly whether z satisfies ALL Boros-Hammer inequalities (9),
  i.e. g(w) = w^T M w - c^T w >= 0 for every w = (w0, w_1..w_n) in Z^{n+1}, c = (1, x).
  For M positive definite, g(w) = (w-m)^T M (w-m) - R with m = M^{-1} c / 2, R = m^T M m,
  so z is in P_BH iff no integer point lies strictly inside the ellipsoid (w-m)^T M (w-m) < R.
  All integer points with (w-m)^T M (w-m) <= R are enumerated (Fincke-Pohst on an exact LDL^T).
"""
import math
from fractions import Fraction as Fr
from bh import pairs


def moment_matrix_exact(n, z):
    M = [[Fr(0)] * (n + 1) for _ in range(n + 1)]
    M[0][0] = Fr(1)
    for i in range(n):
        M[0][i + 1] = M[i + 1][0] = z[i]
        M[i + 1][i + 1] = z[i]
    for k, (i, j) in enumerate(pairs(n)):
        M[i + 1][j + 1] = M[j + 1][i + 1] = z[n + k]
    return M


def ldl(M):
    """Exact LDL^T; returns (L, D) or raises if a pivot is <= 0 (M not positive definite)."""
    N = len(M)
    L = [[Fr(0)] * N for _ in range(N)]
    D = [Fr(0)] * N
    for j in range(N):
        D[j] = M[j][j] - sum(L[j][k] ** 2 * D[k] for k in range(j))
        if D[j] <= 0:
            raise ValueError("M is not positive definite (pivot %s at %d)" % (D[j], j))
        L[j][j] = Fr(1)
        for i in range(j + 1, N):
            L[i][j] = (M[i][j] - sum(L[i][k] * L[j][k] * D[k] for k in range(j))) / D[j]
    return L, D


def solve(M, b):
    N = len(M)
    A = [row[:] + [b[i]] for i, row in enumerate(M)]
    for c in range(N):
        p = next(r for r in range(c, N) if A[r][c] != 0)
        A[c], A[p] = A[p], A[c]
        for r in range(N):
            if r != c and A[r][c] != 0:
                f = A[r][c] / A[c][c]
                A[r] = [A[r][k] - f * A[c][k] for k in range(N + 1)]
    return [A[i][N] / A[i][i] for i in range(N)]


def enumerate_ellipsoid(M, m, R):
    """All integer w with (w-m)^T M (w-m) <= R (exact)."""
    L, D = ldl(M)
    N = len(M)
    out = []
    w = [0] * N

    def rec(k, rem):
        # y_k = (w_k - m_k) + sum_{j>k} L[j][k] (w_j - m_j)
        shift = sum(L[j][k] * (w[j] - m[j]) for j in range(k + 1, N))
        centre = m[k] - shift
        rad = math.sqrt(float(rem / D[k])) if rem > 0 else 0.0
        lo = math.floor(float(centre) - rad) - 1
        hi = math.ceil(float(centre) + rad) + 1
        for t in range(lo, hi + 1):
            y = t - centre
            r2 = rem - D[k] * y * y
            if r2 < 0:
                continue
            w[k] = t
            if k == 0:
                out.append(list(w))
            else:
                rec(k - 1, r2)
        w[k] = 0

    rec(N - 1, R)
    return out


def in_PBH(n, z):
    """Returns (True, tight_list) if z satisfies all BH inequalities, else (False, violated_w)."""
    M = moment_matrix_exact(n, z)
    c = [Fr(1)] + list(z[:n])
    m = [t / 2 for t in solve(M, c)]
    R = sum(m[i] * M[i][j] * m[j] for i in range(n + 1) for j in range(n + 1))
    pts = enumerate_ellipsoid(M, m, R)
    tight = []
    for w in pts:
        g = sum(w[i] * M[i][j] * w[j] for i in range(n + 1) for j in range(n + 1)) - sum(c[i] * w[i] for i in range(n + 1))
        if g < 0:
            return False, w
        if g == 0:
            tight.append(w)
    return True, tight


def ecg_exact_rational(v0, v):
    n = len(v)
    a = [math.ceil(v[i] * v[i] + 2 * v[i] * v0) for i in range(n)]
    a += [math.ceil(2 * v[i] * v[j]) for (i, j) in pairs(n)]
    return a, math.floor(v0 * v0)


def value(a, c, z):
    return sum(Fr(ai) * zi for ai, zi in zip(a, z)) + c


def valid_on_binaries(n, a, c):
    worst = None
    for mask in range(2 ** n):
        x = [(mask >> i) & 1 for i in range(n)]
        z = x + [x[i] * x[j] for (i, j) in pairs(n)]
        val = value(a, c, z)
        if worst is None or val < worst[0]:
            worst = (val, x)
    return worst


# ---------------------------------------------------------------------------------------------
# Exact BH separation for arbitrary rational z (handles indefinite and singular M).
# ---------------------------------------------------------------------------------------------
def _g(M, c, w):
    N = len(M)
    return sum(w[i] * M[i][j] * w[j] for i in range(N) for j in range(N)) - sum(c[i] * w[i] for i in range(N))


def _neg_direction(M):
    """Exact symmetric-pivot LDL; returns a rational y with y^T M y < 0 if M is not PSD, else None,
    together with the rational kernel basis when M is PSD."""
    import sympy as sp
    S = sp.Matrix(len(M), len(M), lambda i, j: sp.Rational(M[i][j].numerator, M[i][j].denominator))
    # PSD test through all principal minors is too slow; use eigen-decomposition over algebraics
    # only for the sign pattern, then find a rational negative direction by rounding eigenvectors.
    ev = S.eigenvects()
    for val, mult, vecs in ev:
        if val.is_negative or (val.is_real and sp.N(val, 50) < 0):
            for vec in vecs:
                y = [sp.nsimplify(sp.N(t, 60), rational=True, tolerance=sp.Rational(1, 10 ** 30)) for t in vec]
                q = sum(y[i] * S[i, j] * y[j] for i in range(len(M)) for j in range(len(M)))
                if q < 0:
                    return [Fr(int(sp.fraction(t)[0]), int(sp.fraction(t)[1])) for t in y], None
            raise RuntimeError("negative eigenvalue but rational rounding failed")
    ker = [[Fr(int(sp.fraction(t)[0]), int(sp.fraction(t)[1])) for t in v] for v in S.nullspace()]
    return None, ker


def exact_bh_separation(n, z):
    """Returns (None, info) if z satisfies ALL BH inequalities, or (w, g) with g = BH value < 0.
    Exact: rational arithmetic, complete enumeration."""
    M = moment_matrix_exact(n, z)
    c = [Fr(1)] + list(z[:n])
    N = n + 1
    y, ker = _neg_direction(M)
    if y is not None:
        den = 1
        for t in y:
            den = den * t.denominator // math.gcd(den, t.denominator)
        yi = [int(t * den) for t in y]
        q = _g(M, [0] * N, yi)          # < 0
        lin = sum(c[i] * yi[i] for i in range(N))
        tmult = 1
        while True:
            w = [tmult * t for t in yi]
            g = _g(M, c, w)
            if g < 0:
                return w, g
            tmult *= 2
    # M is PSD with rational kernel 'ker'
    if len(ker) > 1:
        raise NotImplementedError("kernel dimension > 1")
    J = []
    kint = None
    if ker:
        k = ker[0]
        den = 1
        for t in k:
            den = den * t.denominator // math.gcd(den, t.denominator)
        kint = [int(t * den) for t in k]
        gg = 0
        for t in kint:
            gg = math.gcd(gg, abs(t))
        kint = [t // gg for t in kint]                      # primitive integer kernel vector
        ck = sum(c[i] * kint[i] for i in range(N))
        if ck != 0:
            w = kint if ck > 0 else [-t for t in kint]
            return w, _g(M, c, w)
        j = min((i for i in range(N) if kint[i] != 0), key=lambda i: abs(kint[i]))
        J = [j]
    F = [i for i in range(N) if i not in J]
    MFF = [[M[i][l] for l in F] for i in F]
    residues = range(abs(kint[J[0]])) if J else [None]
    tight = 0
    for r in residues:
        rJ = {J[0]: r} if J else {}
        # g(w) restricted: w_F free, w_J = r
        bF = [c[F[a]] / 2 - sum(M[F[a]][jj] * rv for jj, rv in rJ.items()) for a in range(len(F))]
        mF = solve(MFF, bF)
        const = sum(rv * M[jj][kk] * rv2 for jj, rv in rJ.items() for kk, rv2 in rJ.items()) \
            - sum(c[jj] * rv for jj, rv in rJ.items())
        # g = (wF-mF)^T MFF (wF-mF) - mF^T MFF mF + const
        R = sum(mF[a] * MFF[a][b] * mF[b] for a in range(len(F)) for b in range(len(F))) - const
        if R < 0:
            continue
        for wF in enumerate_ellipsoid(MFF, mF, R):
            w = [0] * N
            for a, i in enumerate(F):
                w[i] = wF[a]
            for jj, rv in rJ.items():
                w[jj] = rv
            g = _g(M, c, w)
            if g < 0:
                return w, g
            tight += (g == 0)
    return None, dict(kernel=kint, tight_count=tight)


def column_echelon(A):
    """Integer column operations: returns (H, U) with H = A U, U unimodular, and the last
    columns of H (from index 'rank' on) identically zero; then U[:, rank:] is a basis of the
    integer kernel {w in Z^N : A w = 0} (saturated, because U is unimodular)."""
    N = len(A[0])
    H = [row[:] for row in A]
    U = [[int(i == j) for j in range(N)] for i in range(N)]

    def colop(i, j, a, b, c, d):  # (col_i, col_j) <- (a col_i + b col_j, c col_i + d col_j)
        for M_ in (H, U):
            for row in M_:
                x, y = row[i], row[j]
                row[i], row[j] = a * x + b * y, c * x + d * y

    piv = 0
    for r in range(len(H)):
        if piv >= N:
            break
        for c in range(piv + 1, N):
            while H[r][c] != 0:
                q = H[r][piv] // H[r][c]
                colop(piv, c, 1, -q, 0, 1)  # col_piv -= q col_c
                colop(piv, c, 0, 1, 1, 0)   # swap
        if H[r][piv] != 0:
            piv += 1
    return H, U, piv


def exact_bh_separation_general(n, z):
    """Exact BH separation for any rational z (M indefinite, singular or definite).
    Returns (None, info) if z satisfies all BH inequalities, else (w, g<0)."""
    M = moment_matrix_exact(n, z)
    c = [Fr(1)] + list(z[:n])
    N = n + 1
    y, _ = _neg_direction(M)
    if y is not None:
        return exact_bh_separation(n, z)          # indefinite case handled there
    den = 1
    for row in M:
        for t in row:
            den = den * t.denominator // math.gcd(den, t.denominator)
    A = [[int(t * den) for t in row] for row in M]
    H, U, r = column_echelon(A)
    Ucols = [[U[i][j] for i in range(N)] for j in range(N)]
    for kvec in Ucols[r:]:
        ck = sum(c[i] * kvec[i] for i in range(N))
        if ck != 0:
            w = kvec if ck > 0 else [-t for t in kvec]
            return w, _g(M, c, w)
    B = Ucols[:r]                                   # w = sum_a y_a B_a  (mod integer kernel)
    Mp = [[sum(B[a][i] * M[i][j] * B[b][j] for i in range(N) for j in range(N)) for b in range(r)] for a in range(r)]
    cp_ = [sum(c[i] * B[a][i] for i in range(N)) for a in range(r)]
    m = [t / 2 for t in solve(Mp, cp_)]
    R = sum(m[a] * Mp[a][b] * m[b] for a in range(r) for b in range(r))
    tight = 0
    for yv in enumerate_ellipsoid(Mp, m, R):
        w = [sum(yv[a] * B[a][i] for a in range(r)) for i in range(N)]
        g = _g(M, c, w)
        if g < 0:
            return w, g
        tight += (g == 0)
    return None, dict(kernel_dim=N - r, tight_count=tight)
