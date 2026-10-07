"""Relaxations of box-constrained QP  min x'Hx + g'x  over [0,1]^n.

Moment variables are registered by monomial keys: sorted tuples of global
indices with repetition, e.g. (i,) = x_i, (i, j) = Y_ij, (i, i) = Y_ii,
(i, j, k) = x_i x_j x_k, (i, i, j) = x_i^2 x_j, (i, i, j, k) = x_i^2 x_j x_k.

Families of constraints (all valid for the true moments of points of the cube):
  base   Shor PSD on [1 x'; x Y] (dense, order n+1), McCormick on all pairs,
         Y_ii <= x_i, 0 <= x <= 1, triangle inequalities added by separation.
  K      Khajavirad, arXiv 2601.18545v2, Theorem 3, LMIs (17) with plus set
         P = {i,j,k}, minus set M = empty: 8 level-3 RLT inequalities,
         12 order-2 blocks (as rotated SOC), 6 order-3 PSD blocks.  The order-4
         block (R = P) is a principal submatrix of the Shor block and is omitted.
  A      Anstreicher-Puges, arXiv 2501.09150v1, equations (14) (8 linear
         inequalities in the trilinear moment z = x_ijk), (15) (24 switched
         rotated SOC) and (16) (48 switched/permuted rotated SOC).
  F      The three-positive family of research-20260925/three-positive-family-sdp.md
         for one triple and one orientation (choice of the 'z' coordinate and of
         complements of the three coordinates): one order-5 PSD block with six
         nonnegative auxiliaries N.
  Fcut   A single family inequality with fixed parameters (linear).
  X      Anstreicher-Burer Theorem 7 exact DNN lift of the 3-cube moment hull
         with a 5-tetrahedron triangulation: five 4x4 DNN blocks.
  Xcut   A single valid linear inequality <C, M_T> >= 0 for the triple moment
         matrix with C in the dual of the 3-cube moment cone.
"""

import itertools
import numpy as np
from conic import Model, add_aff

# ---------------------------------------------------------------------------
# Instances


def read_boxqp(path):
    """Burer's format: max 0.5 x'Qx + c'x.  Return (H, g) for min x'Hx + g'x."""
    toks = open(path).read().split()
    n = int(toks[0])
    vals = np.array([float(t) for t in toks[1:]])
    c = vals[:n]
    Q = vals[n:n + n * n].reshape(n, n)
    assert np.allclose(Q, Q.T)
    return -0.5 * Q, -c


# ---------------------------------------------------------------------------
# Tetrahedra for the exact lift (5-tetrahedron triangulation of the cube)
TETRA5 = [
    [(0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1)],
    [(1, 0, 0), (0, 0, 0), (1, 1, 0), (1, 0, 1)],
    [(0, 1, 0), (0, 0, 0), (1, 1, 0), (0, 1, 1)],
    [(0, 0, 1), (0, 0, 0), (1, 0, 1), (0, 1, 1)],
    [(1, 1, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1)],
]
ABAR5 = [np.array([[1.0] * 4] + [[v[r] for v in tet] for r in range(3)]) for tet in TETRA5]
TETRA6 = []
for perm in itertools.permutations(range(3)):
    # simplex 0 <= x_perm[0] <= x_perm[1] <= x_perm[2] <= 1 has vertices
    verts = []
    for m in range(4):  # number of coordinates equal to one (largest ones)
        v = [0, 0, 0]
        for t in range(3 - m, 3):
            v[perm[t]] = 1
        verts.append(tuple(v))
    TETRA6.append(verts)
ABAR6 = [np.array([[1.0] * 4] + [[v[r] for v in tet] for r in range(3)]) for tet in TETRA6]

# uniform-distribution moment matrix on the 3-cube (interior point of the moment cone)
MC = np.array([[1, .5, .5, .5], [.5, 1 / 3, .25, .25], [.5, .25, 1 / 3, .25], [.5, .25, .25, 1 / 3]])

ORIENTS = [(c, s) for c in range(3) for s in itertools.product((0, 1), repeat=3)]  # 24


class Relax:
    def __init__(self, H, g, name='', cliques=None):
        """cliques=None: dense Shor on all pairs.  Otherwise a list of cliques of a
        chordal graph containing the support of H; Y_ij exists only for pairs inside a
        clique and the Shor condition is imposed on each clique block (this is the
        exact PSD-completion form of the Shor relaxation projected on those pairs)."""
        self.H = np.array(H, float)
        self.g = np.array(g, float)
        self.n = n = len(g)
        self.name = name
        m = self.m = Model()
        self.mon = {}
        if cliques is None:
            cliques = [tuple(range(n))]
        self.cliques = [tuple(sorted(c)) for c in cliques]
        pairs = set()
        for c in self.cliques:
            for a in range(len(c)):
                for b in range(a + 1, len(c)):
                    pairs.add((c[a], c[b]))
        self.pairs = sorted(pairs)
        for (i, j) in zip(*np.nonzero(np.triu(self.H, 1))):
            assert (i, j) in pairs, 'objective support must lie in the clique pattern'
        for i in range(n):
            self.mon[(i,)] = m.var(0, 1)
        for i in range(n):
            self.mon[(i, i)] = m.var(0, 1)
        for (i, j) in self.pairs:
            self.mon[(i, j)] = m.var(0, 1)
        # bounds on x (explicit); Y bounds are implied by McCormick / PSD / Y_ii <= x_i
        for i in range(n):
            m.add_ge(({self.mon[(i,)]: 1.0}, 0.0), 'bounds')
            m.add_ge(({self.mon[(i,)]: -1.0}, 1.0), 'bounds')
        # Shor (dense, or one block per clique)
        for c in self.cliques:
            keys = [()] + [(i,) for i in c]
            mat = [[self.expr(tuple(sorted(a + b))) for b in keys] for a in keys]
            m.add_psd(mat, 'shor')
        # McCormick
        for i in range(n):
            m.add_ge(({self.mon[(i,)]: 1.0, self.mon[(i, i)]: -1.0}, 0.0), 'rlt')
        for (i, j) in self.pairs:
            xi, xj, y = self.mon[(i,)], self.mon[(j,)], self.mon[(i, j)]
            m.add_ge(({y: 1.0}, 0.0), 'rlt')
            m.add_ge(({y: 1.0, xi: -1.0, xj: -1.0}, 1.0), 'rlt')
            m.add_ge(({xi: 1.0, y: -1.0}, 0.0), 'rlt')
            m.add_ge(({xj: 1.0, y: -1.0}, 0.0), 'rlt')
        obj = {}
        for i in range(n):
            if g[i]:
                obj[self.mon[(i,)]] = obj.get(self.mon[(i,)], 0) + g[i]
            for j in range(i, n):
                c = self.H[i, j] if i == j else 2 * self.H[i, j]
                if c:
                    obj[self.mon[(i, j)]] = obj.get(self.mon[(i, j)], 0) + c
        self.triples = clique_triples(self.cliques)
        m.set_obj(obj)
        self.tri_added = set()
        self.K_added = set()
        self.A_added = set()
        self.rlt3_added = set()
        self.F_added = set()
        self.X_added = set()
        self.ncuts = {'Fcut': 0, 'Xcut': 0}

    # ------------------------------------------------------------------
    def var_of(self, key):
        if key not in self.mon:
            v = self.m.var(0, 1)
            self.mon[key] = v
            # explicit valid bounds for auxiliary moments (needed by the safe bound)
            self.m.add_ge(({v: 1.0}, 0.0), 'auxbounds')
            self.m.add_ge(({v: -1.0}, 1.0), 'auxbounds')
        return self.mon[key]

    def expr(self, key):
        if key == ():
            return ({}, 1.0)
        return ({self.var_of(key): 1.0}, 0.0)

    def mom(self, factors):
        """Moment of a product of factors (index, switched): x_i or 1 - x_i."""
        poly = {(): 1.0}
        for (i, s) in factors:
            new = {}
            for key, c in poly.items():
                k2 = tuple(sorted(key + (i,)))
                new[k2] = new.get(k2, 0.0) + (-c if s else c)
                if s:
                    new[key] = new.get(key, 0.0) + c
            poly = new
        d, const = {}, 0.0
        for key, c in poly.items():
            if c == 0:
                continue
            if key == ():
                const += c
            else:
                v = self.var_of(key)
                d[v] = d.get(v, 0.0) + c
        return (d, const)

    # ------------------------------------------------------------------
    def add_triangle(self, i, j, k, t):
        key = (i, j, k, t)
        if key in self.tri_added:
            return
        self.tri_added.add(key)
        X = lambda a, b: self.mon[(min(a, b), max(a, b))]
        x = lambda a: self.mon[(a,)]
        if t < 3:
            a, b, c = [(i, j, k), (j, i, k), (k, i, j)][t]
            # Y_ab + Y_ac - x_a - Y_bc <= 0
            self.m.add_ge(({X(a, b): -1, X(a, c): -1, x(a): 1, X(b, c): 1}, 0.0), 'tri')
        else:
            self.m.add_ge(({x(i): -1, x(j): -1, x(k): -1, X(i, j): 1, X(i, k): 1, X(j, k): 1}, 1.0), 'tri')

    def add_rlt3(self, T):
        if T in self.rlt3_added:
            return
        self.rlt3_added.add(T)
        for s in itertools.product((0, 1), repeat=3):
            self.m.add_ge(self.mom([(T[r], s[r]) for r in range(3)]), 'rlt3')

    def add_K(self, T):
        """Khajavirad (17) with P = T, M = empty."""
        if T in self.K_added:
            return
        self.K_added.add(T)
        self.add_rlt3(T)                       # R = empty
        for a in range(3):                      # R = {a}: 4 order-2 blocks
            others = [r for r in range(3) if r != a]
            for s in itertools.product((0, 1), repeat=2):
                f = [(T[others[r]], s[r]) for r in range(2)]
                u = self.mom(f)
                w = self.mom(f + [(T[a], 0)])
                v = self.mom(f + [(T[a], 0), (T[a], 0)])
                self.m.add_rsoc(u, v, w, 'K')
        for c in range(3):                      # R = {a,b}: 2 order-3 blocks
            a, b = [r for r in range(3) if r != c]
            for s in (0, 1):
                f = [(T[c], s)]
                fa = f + [(T[a], 0)]
                fb = f + [(T[b], 0)]
                mat = [[self.mom(f), self.mom(fa), self.mom(fb)],
                       [None, self.mom(fa + [(T[a], 0)]), self.mom(fa + [(T[b], 0)])],
                       [None, None, self.mom(fb + [(T[b], 0)])]]
                self.m.add_psd(mat, 'K')

    def add_A(self, T):
        """Anstreicher-Puges (14)-(16) for triple T."""
        if T in self.A_added:
            return
        self.A_added.add(T)
        self.add_rlt3(T)                        # (14)
        for s in itertools.product((0, 1), repeat=3):
            f = lambda *rs: self.mom([(T[r], s[r]) for r in rs])
            z = f(0, 1, 2)
            for i in range(3):                  # (15)
                j, k = [r for r in range(3) if r != i]
                self.m.add_rsoc(f(i, i), f(j, k), z, 'A')
            for (i, j, k) in itertools.permutations(range(3)):   # (16)
                self.m.add_rsoc(f(i, i), add_aff((1, f(j, j)), (3, f(j, k))), add_aff((1, f(i, j)), (1, z)), 'A')

    def family_bB(self, T, orient):
        """Affine expressions b (4) and B (4x4) for a triple and orientation."""
        c, s = orient
        a, b_ = [r for r in range(3) if r != c]
        X, Yv, Z = (T[a], s[a]), (T[b_], s[b_]), (T[c], s[c])
        mx, my, mz = self.mom([X]), self.mom([Yv]), self.mom([Z])
        yxx, yyy, yzz = self.mom([X, X]), self.mom([Yv, Yv]), self.mom([Z, Z])
        yxy, yxz, yyz = self.mom([X, Yv]), self.mom([X, Z]), self.mom([Yv, Z])
        neg = lambda e: add_aff((-1, e))
        bvec = [neg(mx), neg(my), mz, neg(yxy)]
        e34 = add_aff((1, mz), (-1, yxz), (-1, yyz))
        B = [[yxx, yxy, neg(yxz), yxy],
             [yxy, yyy, neg(yyz), yxy],
             [neg(yxz), neg(yyz), yzz, e34],
             [yxy, yxy, e34, yxy]]
        return bvec, B

    def add_F(self, T, orient):
        key = (T, orient)
        if key in self.F_added:
            return
        self.F_added.add(key)
        bvec, B = self.family_bB(T, orient)
        N = {}
        for i in range(4):
            for j in range(i + 1, 4):
                v = self.m.var(0, 3)
                N[(i, j)] = v
                self.m.add_ge(({v: 1.0}, 0.0), 'F')
                # N_ij <= 3 is implied (see note); stated explicitly so the safe bound is unconditional
                self.m.add_ge(({v: -1.0}, 3.0), 'F')
        mat = [[None] * 5 for _ in range(5)]
        mat[0][0] = ({}, 1.0)
        for i in range(4):
            mat[0][i + 1] = bvec[i]
            for j in range(i, 4):
                e = B[i][j]
                if i != j:
                    e = add_aff((1, e), (-1, ({N[(i, j)]: 1.0}, 0.0)))
                mat[i + 1][j + 1] = e
        self.m.add_psd(mat, 'F')

    def add_Fcut(self, T, orient, v):
        """Single family inequality with parameters v=(d1,d2,d3,k)>=0 and h=-b(y*)'v
        chosen by the caller (passed as v with h appended: v = (d1,d2,d3,k,h))."""
        d = np.asarray(v[:4], float)
        h = float(v[4])
        bvec, B = self.family_bB(T, orient)
        terms = [(h * h, ({}, 1.0))]
        for i in range(4):
            if d[i]:
                terms.append((2 * h * d[i], bvec[i]))
            for j in range(4):
                if d[i] * d[j]:
                    terms.append((d[i] * d[j], B[i][j]))
        self.m.add_ge(add_aff(*terms), 'Fcut')
        self.ncuts['Fcut'] += 1

    def tri_moment_matrix(self, T):
        keys = [()] + [(t,) for t in T]
        return [[self.expr(tuple(sorted(a + b))) for b in keys] for a in keys]

    def add_X(self, T, tets=None):
        if T in self.X_added:
            return
        self.X_added.add(T)
        tets = ABAR5 if tets is None else tets
        M = self.tri_moment_matrix(T)
        acc = [[[] for _ in range(4)] for _ in range(4)]
        for Ab in tets:
            W = {}
            for i in range(4):
                for j in range(i, 4):
                    W[(i, j)] = self.m.var(0, 1)   # implied: W >= 0 and sum of e'W e = 1
            Wm = lambda i, j: W[(min(i, j), max(i, j))]
            mat = [[({Wm(i, j): 1.0}, 0.0) for j in range(4)] for i in range(4)]
            self.m.add_psd(mat, 'X')
            for i in range(4):
                for j in range(i + 1, 4):
                    self.m.add_ge(({W[(i, j)]: 1.0}, 0.0), 'X')
            # (Ab W Ab')[r][c] = sum_ij Ab[r,i] W_ij Ab[c,j]
            for r in range(4):
                for c in range(r, 4):
                    for i in range(4):
                        for j in range(4):
                            co = Ab[r, i] * Ab[c, j]
                            if co:
                                acc[r][c].append((Wm(i, j), co))
        for r in range(4):
            for c in range(r, 4):
                d = {}
                for v, co in acc[r][c]:
                    d[v] = d.get(v, 0.0) + co
                e = add_aff((1, M[r][c]), (-1, (d, 0.0)))
                self.m.add_eq(e, 'X')

    def add_Xcut(self, T, C):
        """<C, M_T> >= 0 with C a valid (cube-nonnegative) quadratic, 4x4 symmetric."""
        M = self.tri_moment_matrix(T)
        terms = []
        for r in range(4):
            for c in range(4):
                if C[r, c]:
                    terms.append((C[r, c], M[r][c]))
        self.m.add_ge(add_aff(*terms), 'Xcut')
        self.ncuts['Xcut'] += 1

    # ------------------------------------------------------------------
    def solve(self, solver='clarabel', **kw):
        res = self.m.solve(solver, **kw)
        x = res['x']
        n = self.n
        xv = np.array([x[self.mon[(i,)]] for i in range(n)])
        Y = np.full((n, n), np.nan)
        for i in range(n):
            Y[i, i] = x[self.mon[(i, i)]]
        for (i, j) in self.pairs:
            Y[i, j] = Y[j, i] = x[self.mon[(i, j)]]
        res['xv'] = xv
        res['Y'] = Y
        return res

    def size(self):
        s = self.m.size_summary()
        s['tri'] = len(self.tri_added)
        s['K'] = len(self.K_added)
        s['A'] = len(self.A_added)
        s['F'] = len(self.F_added)
        s['X'] = len(self.X_added)
        s.update(self.ncuts)
        return s


# ---------------------------------------------------------------------------
# Separation routines (numpy)


def clique_triples(cliques):
    out = set()
    for c in cliques:
        for t in itertools.combinations(sorted(c), 3):
            out.add(t)
    return np.array(sorted(out), dtype=np.int64).reshape(-1, 3)


def all_triples(n):
    return np.array(list(itertools.combinations(range(n), 3)), dtype=np.int64).reshape(-1, 3)


def separate_triangles(x, Y, tol=1e-6, cap=None, triples=None):
    n = len(x)
    T = all_triples(n) if triples is None else triples
    i, j, k = T[:, 0], T[:, 1], T[:, 2]
    Yij, Yik, Yjk = Y[i, j], Y[i, k], Y[j, k]
    viol = np.stack([Yij + Yik - x[i] - Yjk, Yij + Yjk - x[j] - Yik, Yik + Yjk - x[k] - Yij,
                     x[i] + x[j] + x[k] - Yij - Yik - Yjk - 1], axis=1)
    idx = np.argwhere(viol > tol)
    vals = viol[idx[:, 0], idx[:, 1]]
    order = np.argsort(-vals)
    if cap is not None:
        order = order[:cap]
    return [(int(T[idx[o, 0], 0]), int(T[idx[o, 0], 1]), int(T[idx[o, 0], 2]), int(idx[o, 1])) for o in order], \
        (float(vals.max()) if len(vals) else 0.0)


def switched_moments(x, Y, T, s):
    """Arrays m (N,3), M2 (N,3,3) of moments of (x'_a) with x'_a = 1-x_a if s[a]."""
    m = x[T].copy()
    M2 = Y[T[:, :, None], T[:, None, :]].copy()
    for a in range(3):
        if s[a]:
            # rows/cols a: E[(1-x_a) x_b] = m_b - Y_ab ; diag: 1 - 2m_a + Y_aa
            ma = m[:, a].copy()
            for b in range(3):
                if b == a:
                    continue
                M2[:, a, b] = m[:, b] - M2[:, a, b]
                M2[:, b, a] = M2[:, a, b]
            M2[:, a, a] = 1 - 2 * ma + M2[:, a, a]
            m[:, a] = 1 - ma
    return m, M2


def family_AB(x, Y, T, orient):
    c, s = orient
    a, b = [r for r in range(3) if r != c]
    m, M2 = switched_moments(x, Y, T, s)
    mx, my, mz = m[:, a], m[:, b], m[:, c]
    yxx, yyy, yzz = M2[:, a, a], M2[:, b, b], M2[:, c, c]
    yxy, yxz, yyz = M2[:, a, b], M2[:, a, c], M2[:, b, c]
    N = len(T)
    bv = np.stack([-mx, -my, mz, -yxy], axis=1)
    e34 = mz - yxz - yyz
    B = np.empty((N, 4, 4))
    B[:, 0] = np.stack([yxx, yxy, -yxz, yxy], 1)
    B[:, 1] = np.stack([yxy, yyy, -yyz, yxy], 1)
    B[:, 2] = np.stack([-yxz, -yyz, yzz, e34], 1)
    B[:, 3] = np.stack([yxy, yxy, e34, yxy], 1)
    return bv, B


SUPPORTS = [S for r in range(1, 5) for S in itertools.combinations(range(4), r)]


def stqp_min(A):
    """Exact (up to floating point) min of v'Av over the simplex, batched (N,4,4).
    Returns (value (N,), argmin v (N,4))."""
    N = A.shape[0]
    best = np.full(N, np.inf)
    bestv = np.zeros((N, 4))
    for S in SUPPORTS:
        k = len(S)
        if k == 1:
            val = A[:, S[0], S[0]]
            upd = val < best
            best[upd] = val[upd]
            bestv[upd] = 0
            bestv[upd, S[0]] = 1
            continue
        As = A[:, S][:, :, S]
        K = np.zeros((N, k + 1, k + 1))
        K[:, :k, :k] = As
        K[:, :k, k] = 1
        K[:, k, :k] = 1
        rhs = np.zeros((N, k + 1))
        rhs[:, k] = 1
        det = np.linalg.det(K)
        scale = np.abs(As).max(axis=(1, 2)) ** (k - 1) + 1e-300
        ok = np.abs(det) > 1e-10 * scale
        if not ok.any():
            continue
        sol = np.linalg.solve(K[ok], rhs[ok][:, :, None])[:, :, 0]
        vS = sol[:, :k]
        feas = (vS >= -1e-12).all(axis=1)
        vS = np.maximum(vS, 0)
        vS = vS / vS.sum(axis=1, keepdims=True)
        val = np.einsum('ni,nij,nj->n', vS, As[ok], vS)
        idx = np.nonzero(ok)[0]
        upd = feas & (val < best[idx])
        if upd.any():
            ii = idx[upd]
            best[ii] = val[upd]
            bestv[ii] = 0
            for t, col in enumerate(S):
                bestv[ii, col] = vS[upd, t]
    return best, bestv


def separate_family(x, Y, T, tol=1e-6):
    """For each triple and orientation: StQP value of A = B - bb'.  Returns list of
    (row index, orient index, value, v (4), h)."""
    out = []
    for oi, orient in enumerate(ORIENTS):
        bv, B = family_AB(x, Y, T, orient)
        A = B - bv[:, :, None] * bv[:, None, :]
        # quick filter: PSD A is copositive
        w = np.linalg.eigvalsh(A)[:, 0]
        cand = np.nonzero(w < -tol)[0]
        if len(cand) == 0:
            continue
        val, v = stqp_min(A[cand])
        for t in np.nonzero(val < -tol)[0]:
            r = cand[t]
            h = -float(bv[r] @ v[t])
            out.append((int(r), oi, float(val[t]), v[t].copy(), h))
    return out


def triple_moment_matrices(x, Y, T):
    N = len(T)
    M = np.empty((N, 4, 4))
    M[:, 0, 0] = 1
    M[:, 0, 1:] = x[T]
    M[:, 1:, 0] = x[T]
    M[:, 1:, 1:] = Y[T[:, :, None], T[:, None, :]]
    return M
