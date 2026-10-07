"""SDP relaxations of ternary QP with the cut families of de Meijer et al.

Matrix Y = [[1, x^T], [x, X]] of order N = n+1, index 0 = constant.
A cut is a sparse linear inequality  sum_k coef_k * Y[I_k, J_k] >= rhs  with
I_k <= J_k (each off-diagonal entry is counted once).

Families (numbers refer to arXiv:2603.28979v1):
  tri    triangle (2.1)-(2.2) on X
  pair   pair / non-standard split (2.3): X_ii -+ X_ij >= 0
  rlt    RLT (4.5)-(4.8)
  split1 1-index split (4.3): X_ii -+ x_i >= 0  (part of the base relaxation (4.1))
  split2 2-index split (4.11)-(4.12)
  odd5   odd-set (4.4) with |S| = 5 (pentagonal), heuristic separation
  gsplit general split <v(v+e0)^T, Y> >= 0 for given integer v
"""
import itertools
import time

import cvxpy as cp
import numpy as np
import scipy.sparse as sp


# ---------------------------------------------------------------- cut store
class Cuts:
    def __init__(self, N):
        self.N = N
        self.rows, self.cols, self.vals, self.rhs, self.fam = [], [], [], [], []
        self.m = 0
        self.keys = set()

    def add(self, I, J, C, rhs, fam):
        """I, J, C: arrays (m, k); rhs: (m,)."""
        I = np.atleast_2d(I); J = np.atleast_2d(J); C = np.atleast_2d(C)
        lo = np.minimum(I, J); hi = np.maximum(I, J)
        added = 0
        for r in range(I.shape[0]):
            key = (fam, tuple(lo[r]), tuple(hi[r]), tuple(np.round(C[r], 9)), float(rhs[r]))
            if key in self.keys:
                continue
            self.keys.add(key)
            idx = lo[r] + hi[r] * self.N  # column-major index of Y[lo,hi]
            self.rows.append(np.full(len(idx), self.m))
            self.cols.append(idx)
            self.vals.append(C[r].astype(float))
            self.rhs.append(float(rhs[r]))
            self.fam.append(fam)
            self.m += 1
            added += 1
        return added

    def matrix(self):
        if self.m == 0:
            return None, None
        A = sp.csr_matrix((np.concatenate(self.vals),
                           (np.concatenate(self.rows), np.concatenate(self.cols))),
                          shape=(self.m, self.N * self.N))
        return A, np.array(self.rhs)

    def keep(self, mask):
        """Keep only cuts with mask True."""
        new = Cuts(self.N)
        A, b = self.matrix()
        for r in np.nonzero(mask)[0]:
            new.rows.append(np.full(len(self.cols[r]), new.m))
            new.cols.append(self.cols[r]); new.vals.append(self.vals[r])
            new.rhs.append(self.rhs[r]); new.fam.append(self.fam[r]); new.m += 1
        new.keys = self.keys  # never re-add a dropped cut in the same pass
        return new


# ---------------------------------------------------------------- separation
def _top(viol, I, J, C, rhs, tol, cap):
    k = np.nonzero(viol > tol)[0]
    if len(k) > cap:
        k = k[np.argsort(-viol[k])[:cap]]
    return viol[k], I[k], J[k], C[k], rhs[k]


def sep_tri(Y, tol, cap=10**9):
    N = Y.shape[0]; n = N - 1
    T = np.array(list(itertools.combinations(range(1, N), 3)))
    if len(T) == 0:
        return [np.zeros(0)] * 5
    a = Y[T[:, 0], T[:, 1]]; b = Y[T[:, 0], T[:, 2]]; c = Y[T[:, 1], T[:, 2]]
    pats = np.array([[1, 1, 1], [-1, 1, -1], [1, -1, -1], [-1, -1, 1]], dtype=float)
    out = []
    for s in pats:
        lhs = s[0] * a + s[1] * b + s[2] * c
        viol = -1 - lhs
        I = np.stack([T[:, 0], T[:, 0], T[:, 1]], 1); J = np.stack([T[:, 1], T[:, 2], T[:, 2]], 1)
        C = np.tile(s, (len(T), 1))
        out.append((viol, I, J, C, np.full(len(T), -1.0)))
    return [np.concatenate([o[i] for o in out]) for i in range(5)]


def sep_pair(Y, tol=None, cap=None):
    N = Y.shape[0]
    P = np.array([(i, j) for i in range(1, N) for j in range(1, N) if i != j])
    out = []
    for s in (-1.0, 1.0):
        lhs = Y[P[:, 0], P[:, 0]] + s * Y[P[:, 0], P[:, 1]]
        I = np.stack([P[:, 0], P[:, 0]], 1); J = np.stack([P[:, 0], P[:, 1]], 1)
        C = np.tile([1.0, s], (len(P), 1))
        out.append((-lhs, I, J, C, np.zeros(len(P))))
    return [np.concatenate([o[i] for o in out]) for i in range(5)]


def sep_rlt(Y, tol=None, cap=None):
    N = Y.shape[0]
    P = np.array(list(itertools.combinations(range(1, N), 2)))
    out = []
    for si in (1.0, -1.0):
        for sj in (1.0, -1.0):
            lhs = si * sj * Y[P[:, 0], P[:, 1]] + si * Y[0, P[:, 0]] + sj * Y[0, P[:, 1]]
            I = np.stack([P[:, 0], np.zeros(len(P), int), np.zeros(len(P), int)], 1)
            J = np.stack([P[:, 1], P[:, 0], P[:, 1]], 1)
            C = np.tile([si * sj, si, sj], (len(P), 1))
            out.append((-1 - lhs, I, J, C, np.full(len(P), -1.0)))
    return [np.concatenate([o[i] for o in out]) for i in range(5)]


def sep_split1(Y, tol=None, cap=None):
    N = Y.shape[0]
    idx = np.arange(1, N)
    out = []
    for s in (1.0, -1.0):
        lhs = Y[idx, idx] - s * Y[0, idx]
        I = np.stack([idx, np.zeros(N - 1, int)], 1); J = np.stack([idx, idx], 1)
        C = np.tile([1.0, -s], (N - 1, 1))
        out.append((-lhs, I, J, C, np.zeros(N - 1)))
    return [np.concatenate([o[i] for o in out]) for i in range(5)]


def sep_split2(Y, tol=None, cap=None):
    N = Y.shape[0]
    P = np.array(list(itertools.combinations(range(1, N), 2)))
    z = np.zeros(len(P), int)
    out = []
    for sg in (1.0, -1.0):
        for tau in (1.0, -1.0):
            lhs = (Y[P[:, 0], P[:, 0]] + Y[P[:, 1], P[:, 1]] + 2 * sg * Y[P[:, 0], P[:, 1]]
                   + tau * Y[0, P[:, 0]] + tau * sg * Y[0, P[:, 1]])
            I = np.stack([P[:, 0], P[:, 1], P[:, 0], z, z], 1)
            J = np.stack([P[:, 0], P[:, 1], P[:, 1], P[:, 0], P[:, 1]], 1)
            C = np.tile([1.0, 1.0, 2 * sg, tau, tau * sg], (len(P), 1))
            out.append((-lhs, I, J, C, z.astype(float)))
    return [np.concatenate([o[i] for o in out]) for i in range(5)]


def sep_odd5(Y, tol, cap=5000, restarts=None, rng=None):
    """Heuristic for sum_{i<j in S} v_i v_j X_ij >= -2, |S| = 5, v in {+-1}^S.
    Local search over (S, v): start from random S, v; swap elements / flip
    signs while the left side decreases."""
    N = Y.shape[0]; n = N - 1
    if n < 5:
        return [np.zeros(0)] * 5
    rng = rng or np.random.default_rng(0)
    X = Y[1:, 1:]
    restarts = restarts or 20 * n
    found = {}
    for _ in range(restarts):
        S = list(rng.choice(n, 5, replace=False)); v = rng.choice([-1.0, 1.0], 5)
        def val(S, v):
            return sum(v[a] * v[b] * X[S[a], S[b]] for a in range(5) for b in range(a + 1, 5))
        cur = val(S, v)
        improved = True
        while improved:
            improved = False
            for a in range(5):          # sign flips
                v[a] = -v[a]; t = val(S, v)
                if t < cur - 1e-12:
                    cur = t; improved = True
                else:
                    v[a] = -v[a]
            for a in range(5):          # element swaps (with both signs)
                for e in range(n):
                    if e in S:
                        continue
                    old = S[a]; oldv = v[a]
                    for sg in (1.0, -1.0):
                        S[a] = e; v[a] = sg; t = val(S, v)
                        if t < cur - 1e-12:
                            cur = t; improved = True; oldv = sg; old = e
                    S[a] = old; v[a] = oldv
        if -2 - cur > tol:
            o = np.argsort(S); Ss = tuple(int(S[k]) + 1 for k in o); vs = v[o]
            if vs[0] < 0:
                vs = -vs
            found[(Ss, tuple(vs))] = -2 - cur
    if not found:
        return [np.zeros(0)] * 5
    viol, I, J, C = [], [], [], []
    for (Ss, vs), vi in found.items():
        pr = list(itertools.combinations(range(5), 2))
        I.append([Ss[a] for a, b in pr]); J.append([Ss[b] for a, b in pr])
        C.append([vs[a] * vs[b] for a, b in pr]); viol.append(vi)
    return (np.array(viol), np.array(I), np.array(J), np.array(C, float), np.full(len(viol), -2.0))


def split_cut(v):
    """Rows (I, J, C, rhs) of <v(v+e0)^T, Y> >= 0 in upper-triangular form."""
    v = np.asarray(v, dtype=float)
    N = len(v); I, J, C = [], [], []
    for a in range(N):
        for b in range(a, N):
            if a == b:
                c = v[a] * (v[a] + (a == 0))
            else:
                c = 2 * v[a] * v[b] + (v[b] if a == 0 else 0.0)
            if c != 0:
                I.append(a); J.append(b); C.append(c)
    return np.array([I]), np.array([J]), np.array([C]), np.array([0.0])


def split_value(Y, v):
    v = np.asarray(v, dtype=float)
    return float(v @ Y @ v + v @ Y[:, 0])


SEP = dict(tri=sep_tri, pair=sep_pair, rlt=sep_rlt, split1=sep_split1, split2=sep_split2,
           odd5=sep_odd5)


# ---------------------------------------------------------------- model
class Relaxation:
    """base in {'BT', 'DM'}.  BT: B-T's SDP (bounds on x and diag X).
    DM: (4.1), with (5.2) for QUTO and the facially reduced (5.7) for TQP-Linear."""

    def __init__(self, inst, base):
        self.inst = inst; self.base = base
        self.n = inst["n"]; self.N = self.n + 1
        self.cuts = Cuts(self.N)
        Qt = np.zeros((self.N, self.N))
        Qt[1:, 1:] = inst["Q"]; Qt[0, 1:] = Qt[1:, 0] = inst["c"] / 2
        self.Qt = Qt

    def build(self, extra_obj=None, obj_bound=None):
        N, n = self.N, self.n
        if self.inst["linear"] and self.base == "DM":
            W = np.zeros((N, n)); W[0, 0] = 1.0
            W[1, 1:] = 1.0; W[2:, 1:] = -np.eye(n - 1)
            Z = cp.Variable((n, n), PSD=True)
            Y = W @ Z @ W.T
            cons = [Y[0, 0] == 1]
            self.Zvar = Z
        else:
            Yv = cp.Variable((N, N), PSD=True)
            Y = Yv
            cons = [Y[0, 0] == 1]
        d = cp.hstack([Y[i, i] for i in range(1, N)])
        x = Y[0, 1:]
        if self.base == "BT":
            cons += [x >= -1, x <= 1, d >= 0, d <= 1]
        else:
            cons += [d >= x, d >= -x, d <= 1]
            if not self.inst["linear"]:
                fixed = [i for i in range(n) if self.inst["Q"][i, i] <= 0]
                cons += [Y[i + 1, i + 1] == 1 for i in fixed]
        A, b = self.cuts.matrix()
        if A is not None:
            cons.append(A @ cp.vec(Y, order="F") >= b)
        obj = cp.trace(self.Qt @ Y)
        if obj_bound is not None:
            cons.append(obj <= obj_bound)
            obj = extra_obj(Y)
        self.Y = Y
        self.cons = cons
        return cp.Problem(cp.Minimize(obj), cons)

    def solve(self, extra_obj=None, obj_bound=None, tol=1e-9, max_iter=400, solver="CLARABEL"):
        prob = self.build(extra_obj, obj_bound)
        t = time.time()
        if solver == "CLARABEL":
            prob.solve(solver=cp.CLARABEL, tol_gap_abs=tol, tol_gap_rel=tol, tol_feas=tol,
                       tol_ktratio=1e-7, max_iter=max_iter)
        else:
            prob.solve(solver=cp.SCS, eps_abs=tol, eps_rel=tol, max_iters=200000)
        dt = time.time() - t
        Y = np.array(self.Y.value)
        Y = (Y + Y.T) / 2
        return dict(status=prob.status, obj=float(np.trace(self.Qt @ Y)), Y=Y, time=dt,
                    pobj=prob.value)


def cut_loop(rel, families, tol=1e-3, cap=5000, max_rounds=60, stop_rule="dm", log=None,
             odd5_rng=None):
    """Iterate: solve, separate the families, add up to `cap` most violated.
    stop_rule 'dm': stop when fewer than n violated cuts are found (dMPSS 6.4);
    'none': stop when no cut is violated by more than tol."""
    hist = []
    res = rel.solve()
    for rnd in range(max_rounds):
        Y = res["Y"]
        pool = []
        for f in families:
            if f == "odd5":
                out = sep_odd5(Y, tol, rng=odd5_rng)
            else:
                out = SEP[f](Y, tol)
            viol, I, J, C, rhs = out
            k = np.nonzero(viol > tol)[0]
            for r in k:
                pool.append((viol[r], f, I[r], J[r], C[r], rhs[r]))
        pool.sort(key=lambda t: -t[0])
        nviol = len(pool)
        hist.append(dict(round=rnd, obj=res["obj"], status=res["status"], nviol=nviol,
                         maxviol=pool[0][0] if pool else 0.0, ncuts=rel.cuts.m,
                         time=res["time"]))
        if log:
            log(hist[-1])
        if nviol == 0 or (stop_rule == "dm" and nviol < rel.n):
            break
        added = 0
        for viol, f, I, J, C, rhs in pool[:cap]:
            added += rel.cuts.add(I[None], J[None], C[None], np.array([rhs]), f)
        if added == 0:
            break
        res = rel.solve()
    return res, hist


def eig_rank(Y, thresholds=(1e-3, 1e-5, 1e-7, 1e-9)):
    w = np.linalg.eigvalsh(Y)[::-1]
    lam = w[0]
    return {f"{t:g}": int(np.sum(w > t * lam)) for t in thresholds}, w
