"""Separator branching with cell-dependent slopes for waterno2_T (planning state).

Setting (as in ../separator-branching.md, Section 2.1).  Period t has start
levels s_t (copies of link t-1) and end levels e_t (copies of link t); the link
rows are s_{t+1} = e_t.  Every link t carries a partition P_t of its level box
into cells (leaves of a split tree).  NEW: every cell D of link t carries its own
slope vector lam_{t,D} in R^3.  The pair value of period t on (D, D') is

    phi_t(D, D') = min cost_t(x) + lam_{t-1,D} . s_t(x) - lam_{t,D'} . e_t(x)
                   over period t's rows, s_t(x) in D, e_t(x) in D'.

Validity (see cell-slopes.md, Section 2): for a feasible x with link levels
y_t in D_t, sum_t lam_{t,D_t} . (s_{t+1}(x) - e_t(x)) = 0 because s_{t+1}(x) =
e_t(x) = y_t, PROVIDED the slope used for cell D_t in period t (exit term) is
the same vector as the slope used for D_t in period t+1 (entry term).  So the
shortest path over cell sequences of rigorous pair bounds is a lower bound.

Records.  A rigorous record r (rbb run) bounds the pair problem on boxes
(A_in, A_out) with slopes (a_in, a_out).  For leaf cells D in A_in, D' in A_out
with slopes (l_in, l_out) the record gives the bound

    B_r + min_{s in D} (l_in - a_in) . s + min_{e in D'} -(l_out - a_out) . e,

because the leaf objective equals the record objective plus these two linear
terms and the leaf feasible set is a subset of the record's.  verify_cs.py
evaluates the correction exactly in rational arithmetic.

This module holds the planning state: cells, slopes, a pool of SCIP points
(upper estimates), rigorous records, the DP and the slope LP.
"""
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
WDIR = os.path.dirname(HERE)
SB = os.path.join(WDIR, "sepbranch")
for p in (WDIR, SB):
    if p not in sys.path:
        sys.path.insert(0, p)

INF = math.inf
TOL = 1e-6   # membership tolerance of SCIP points in cells (planning only)


def corr_in(lam, a, lo, hi):
    """min over s in [lo, hi] of (lam - a) . s  (float; planning)."""
    d = np.asarray(lam, float) - np.asarray(a, float)
    return np.minimum(d * lo, d * hi).sum(axis=-1)


def corr_out(lam, a, lo, hi):
    """min over e in [lo, hi] of -(lam - a) . e  (float; planning)."""
    d = np.asarray(lam, float) - np.asarray(a, float)
    return np.minimum(-d * lo, -d * hi).sum(axis=-1)


class State:
    """Planning / certificate state.  Plain attributes only (pickled)."""

    def __init__(self, T, cells, leaves, base):
        self.T = T
        self.cells = cells            # cells[link][cid] = dict(lo, hi, parent, split)
        self.leaves = leaves          # leaves[link] = list of cids
        self.base = base              # base[link] = wave-2 folded slope (cert3)
        self.lam = [{cid: list(map(float, base[l])) for cid in range(len(cells[l]))} for l in range(T - 1)]
        self.pts = [[] for _ in range(T)]   # pts[t] = list of (s, e, c0) ; s/e None at the ends
        self.evals = {}               # (t, cin, cout) -> {slope_key: dict(est, status, best)}
        self.scip_inf = set()         # (t, cin, cout) reported infeasible by SCIP (planning only)
        self.recs = []                # rigorous records (cert3 records and new rbb runs)
        self.log = []

    # ------------------------------------------------------------- cells
    def nlink(self):
        return self.T - 1

    def leaf_box(self, link, cid):
        c = self.cells[link][cid]
        return np.array(c["lo"]), np.array(c["hi"])

    def split(self, link, cid, k, m):
        c = self.cells[link][cid]
        assert c["split"] is None and c["lo"][k] < m < c["hi"][k]
        lo1, hi1 = list(c["lo"]), list(c["hi"])
        hi1[k] = float(m)
        lo2, hi2 = list(c["lo"]), list(c["hi"])
        lo2[k] = float(m)
        n = len(self.cells[link])
        self.cells[link].append(dict(lo=lo1, hi=hi1, parent=cid, split=None))
        self.cells[link].append(dict(lo=lo2, hi=hi2, parent=cid, split=None))
        c["split"] = (k, float(m), n, n + 1)
        self._ver = getattr(self, "_ver", 0) + 1
        pos = self.leaves[link].index(cid)
        self.leaves[link][pos] = n
        self.leaves[link].append(n + 1)
        self.lam[link][n] = list(self.lam[link][cid])
        self.lam[link][n + 1] = list(self.lam[link][cid])
        return n, n + 1

    def under(self, link):
        """cid -> list of leaf positions below it (link-level map)."""
        pos = {cid: i for i, cid in enumerate(self.leaves[link])}
        out = {}

        def rec(cid):
            c = self.cells[link][cid]
            if c["split"] is None:
                r = [pos[cid]]
            else:
                r = rec(c["split"][2]) + rec(c["split"][3])
            out[cid] = r
            return r
        rec(0)
        return out

    def locate(self, link, y, tol=TOL):
        """Leaf cids whose closed box contains y (within tol)."""
        out = []
        stack = [0]
        while stack:
            cid = stack.pop()
            c = self.cells[link][cid]
            if any(y[k] < c["lo"][k] - tol or y[k] > c["hi"][k] + tol for k in range(3)):
                continue
            if c["split"] is None:
                out.append(cid)
            else:
                stack += [c["split"][2], c["split"][3]]
        return out

    # ------------------------------------------------------------- slopes
    def lam_arr(self, link):
        return np.array([self.lam[link][cid] for cid in self.leaves[link]], float)

    def boxes(self, link):
        lo = np.array([self.cells[link][cid]["lo"] for cid in self.leaves[link]], float)
        hi = np.array([self.cells[link][cid]["hi"] for cid in self.leaves[link]], float)
        return lo, hi

    def nrow(self, t):
        return 1 if t == 0 else len(self.leaves[t - 1])

    def ncol(self, t):
        return 1 if t == self.T - 1 else len(self.leaves[t])

    def rcid(self, t, r):
        return -1 if t == 0 else self.leaves[t - 1][r]

    def ccid(self, t, c):
        return -1 if t == self.T - 1 else self.leaves[t][c]

    def pair_slopes(self, t, cin, cout):
        lin = self.lam[t - 1][cin] if t > 0 else [0.0, 0.0, 0.0]
        lout = self.lam[t][cout] if t < self.T - 1 else [0.0, 0.0, 0.0]
        return list(map(float, lin)), list(map(float, lout))

    @staticmethod
    def skey(lin, lout):
        return tuple(float(v) for v in lin) + tuple(float(v) for v in lout)

    # ------------------------------------------------------------- tables
    def __getstate__(self):
        d = dict(self.__dict__)
        d.pop("_inc", None)
        return d

    def incidence(self):
        """For every period: arrays (point index, row pos, col pos) of pool points
        in leaf pairs (a point on a cell boundary belongs to every adjacent leaf).
        Cached; only new points are located unless a cell was split."""
        T = self.T
        ver = getattr(self, "_ver", 0)
        cache = getattr(self, "_inc", None)
        if cache is None or cache["ver"] != ver:
            cache = dict(ver=ver, n=[0] * T, P=[[] for _ in range(T)], R=[[] for _ in range(T)],
                         C=[[] for _ in range(T)])
        for t in range(T):
            P, R, C = cache["P"][t], cache["R"][t], cache["C"][t]
            for i in range(cache["n"][t], len(self.pts[t])):
                s, e, c0 = self.pts[t][i]
                rows = [-1] if t == 0 else self.locate(t - 1, s)
                cols = [-1] if t == T - 1 else self.locate(t, e)
                for r in rows:
                    for c in cols:
                        P.append(i); R.append(r); C.append(c)
            cache["n"][t] = len(self.pts[t])
        self._inc = cache
        out = []
        for t in range(T):
            P = np.array(cache["P"][t], int)
            if t == 0:
                R = np.zeros(len(P), int)
            else:
                rmap = np.full(len(self.cells[t - 1]), -1, int)
                rmap[self.leaves[t - 1]] = np.arange(len(self.leaves[t - 1]))
                R = rmap[np.array(cache["R"][t], int)]
            if t == T - 1:
                C = np.zeros(len(P), int)
            else:
                cmap = np.full(len(self.cells[t]), -1, int)
                cmap[self.leaves[t]] = np.arange(len(self.leaves[t]))
                C = cmap[np.array(cache["C"][t], int)]
            assert (len(P) == 0) or (R.min() >= 0 and C.min() >= 0)
            out.append((P, R, C))
        return out

    def incidence_full(self):
        """Uncached version (reference)."""
        T = self.T
        inc = []
        for t in range(T):
            rpos = {cid: i for i, cid in enumerate(self.leaves[t - 1])} if t > 0 else None
            cpos = {cid: i for i, cid in enumerate(self.leaves[t])} if t < T - 1 else None
            P, R, C = [], [], []
            for i, (s, e, c0) in enumerate(self.pts[t]):
                rows = [0] if t == 0 else [rpos[c] for c in self.locate(t - 1, s)]
                cols = [0] if t == T - 1 else [cpos[c] for c in self.locate(t, e)]
                for r in rows:
                    for c in cols:
                        P.append(i); R.append(r); C.append(c)
            inc.append((np.array(P, int), np.array(R, int), np.array(C, int)))
        return inc

    def point_arrays(self, t):
        T = self.T
        n = len(self.pts[t])
        S = np.zeros((n, 3)); E = np.zeros((n, 3)); C0 = np.zeros(n)
        for i, (s, e, c0) in enumerate(self.pts[t]):
            if t > 0:
                S[i] = s
            if t < T - 1:
                E[i] = e
            C0[i] = c0
        return S, E, C0

    def tables(self, inc=None):
        """Per period: U (min over pool points at current slopes; +inf if none),
        UARG (pool index of the minimizing point, -1), L (best rigorous bound at
        current slopes, float), FRESH (evaluated by SCIP at the current slopes),
        SINF (SCIP reported infeasible)."""
        T = self.T
        if inc is None:
            inc = self.incidence()
        LAM = [self.lam_arr(l) for l in range(T - 1)]
        BOX = [self.boxes(l) for l in range(T - 1)]
        out = []
        for t in range(T):
            nr, nc = self.nrow(t), self.ncol(t)
            U = np.full((nr, nc), INF)
            UARG = np.full((nr, nc), -1, int)
            S, E, C0 = self.point_arrays(t)
            P, R, C = inc[t]
            if len(P):
                v = C0[P].copy()
                if t > 0:
                    v += (LAM[t - 1][R] * S[P]).sum(1)
                if t < T - 1:
                    v -= (LAM[t][C] * E[P]).sum(1)
                order = np.argsort(-v)       # assign largest first so the min wins
                U[R[order], C[order]] = v[order]
                UARG[R[order], C[order]] = P[order]
            out.append(dict(U=U, UARG=UARG, L=np.full((nr, nc), -INF), FRESH=np.zeros((nr, nc), bool),
                            SINF=np.zeros((nr, nc), bool)))
        # rigorous records
        unders = [self.under(l) for l in range(T - 1)]
        for rec in self.recs:
            t = rec["t"]
            rows = [0] if t == 0 else unders[t - 1][rec["cin"]]
            cols = [0] if t == T - 1 else unders[t][rec["cout"]]
            B = rec["bound"]
            L = out[t]["L"]
            if B == INF:
                L[np.ix_(rows, cols)] = INF
                continue
            ci = np.zeros(len(rows))
            co = np.zeros(len(cols))
            if t > 0:
                lo, hi = BOX[t - 1][0][rows], BOX[t - 1][1][rows]
                ci = corr_in(LAM[t - 1][rows], rec["lam_in"], lo, hi)
            if t < T - 1:
                lo, hi = BOX[t][0][cols], BOX[t][1][cols]
                co = corr_out(LAM[t][cols], rec["lam_out"], lo, hi)
            val = B + ci[:, None] + co[None, :]
            sub = L[np.ix_(rows, cols)]
            L[np.ix_(rows, cols)] = np.maximum(sub, val)
        # pessimistic estimates: every SCIP evaluation (value est at slopes (a, a') on
        # boxes (A, A')) gives, by Lemma 2 applied to estimates, est + corrections
        # for every leaf pair inside (A, A') at the current slopes (planning only).
        for d in out:
            d["P"] = np.full(d["U"].shape, -INF)
        for (t, a, b), evs in self.evals.items():
            rows = [0] if t == 0 else unders[t - 1].get(a)
            cols = [0] if t == T - 1 else unders[t].get(b)
            if rows is None or cols is None:
                continue
            for sk, ev in evs.items():
                est = ev["est"]
                if est is None or not np.isfinite(est):
                    continue
                ci = np.zeros(len(rows))
                co = np.zeros(len(cols))
                if t > 0:
                    lo, hi = BOX[t - 1][0][rows], BOX[t - 1][1][rows]
                    ci = corr_in(LAM[t - 1][rows], sk[0:3], lo, hi)
                if t < T - 1:
                    lo, hi = BOX[t][0][cols], BOX[t][1][cols]
                    co = corr_out(LAM[t][cols], sk[3:6], lo, hi)
                Pt = out[t]["P"]
                sub = Pt[np.ix_(rows, cols)]
                Pt[np.ix_(rows, cols)] = np.maximum(sub, est + ci[:, None] + co[None, :])
        for (t, a, b) in self.scip_inf:
            rows = [0] if t == 0 else unders[t - 1].get(a)
            cols = [0] if t == T - 1 else unders[t].get(b)
            if rows is None or cols is None:
                continue
            out[t]["SINF"][np.ix_(rows, cols)] = True
        for t in range(T):
            F = out[t]["FRESH"]
            for r in range(self.nrow(t)):
                cin = self.rcid(t, r)
                for c in range(self.ncol(t)):
                    cout = self.ccid(t, c)
                    ev = self.evals.get((t, cin, cout))
                    if ev:
                        lin, lout = self.pair_slopes(t, cin, cout)
                        if self.skey(lin, lout) in ev:
                            F[r, c] = True
            F |= out[t]["SINF"]
        return out

    @staticmethod
    def model(tab):
        """Planning value per pair: +inf if rigorously empty or SCIP-infeasible;
        U if the pool has a point in the pair; else the rigorous bound L."""
        out = []
        for d in tab:
            # max(L, min(U, P)): fresh pairs -> about U; stale pairs -> pessimistic estimate
            M = np.maximum(d["L"], np.minimum(d["U"], d["P"]))
            M = np.where(np.isfinite(M), M, np.where(np.isfinite(d["U"]), np.maximum(d["U"], d["L"]), M))
            M = np.where(d["SINF"] & ~np.isfinite(d["U"]), INF, M)
            M = np.where(d["L"] == INF, INF, M)
            out.append(M)
        return out

    # ------------------------------------------------------------- DP
    def dp(self, B):
        T = self.T
        f = [None] * T
        f[0] = B[0][0, :].astype(float)
        for t in range(1, T - 1):
            f[t] = (f[t - 1][:, None] + B[t]).min(axis=0)
        V = float((f[T - 2] + B[T - 1][:, 0]).min())
        g = [None] * T
        g[T - 2] = B[T - 1][:, 0].astype(float)
        for t in range(T - 2, 0, -1):
            g[t - 1] = (B[t] + g[t][None, :]).min(axis=1)
        return V, f, g

    def through(self, B, t, f, g):
        T = self.T
        fin = np.zeros(1) if t == 0 else f[t - 1]
        gout = np.zeros(1) if t == T - 1 else g[t]
        return fin[:, None] + B[t] + gout[None, :]

    def best_path(self, B, f, g):
        T = self.T
        path = [None] * (T - 1)
        path[T - 2] = int(np.argmin(f[T - 2] + B[T - 1][:, 0]))
        for t in range(T - 2, 0, -1):
            path[t - 1] = int(np.argmin(f[t - 1] + B[t][:, path[t]]))
        return path

    # ------------------------------------------------------------- pool / evals
    def add_eval(self, t, cin, cout, lin, lout, res):
        """res from scip_task: est, status, sols [(s, e, obj)]."""
        key = (t, cin, cout)
        if res["status"] == "infeasible":
            self.scip_inf.add(key)
        best = None
        kept = []
        for (s, e, obj) in res.get("sols", []):
            y = np.array((s if s is not None else []) + (e if e is not None else []), float)
            if any(np.max(np.abs(y - z), initial=0.0) < 1e-4 for z in kept):
                continue
            kept.append(y)
            c0 = obj
            if t > 0:
                c0 -= float(np.dot(lin, s))
            if t < self.T - 1:
                c0 += float(np.dot(lout, e))
            self.pts[t].append((None if s is None else list(map(float, s)),
                                None if e is None else list(map(float, e)), float(c0)))
            if best is None:
                best = len(self.pts[t]) - 1
        self.evals.setdefault(key, {})[self.skey(lin, lout)] = dict(est=res["est"], status=res["status"],
                                                                    best=best, time=res["time"])


# ------------------------------------------------------------------ SCIP worker
_W = {}


def init_worker(T, implied, term=True):
    import core
    import terminal
    D = core.setup(T, implied)
    if term:
        terminal.add_terminal_row(D)
    _W["D"] = D
    _W["PB"] = {}


def _box(D, t, cin, cout):
    S = D["S"]
    box = {}
    if cin is not None:
        for k, (i, va, vb) in enumerate(S["link"][t - 1]):
            box[vb] = (float(cin[0][k]), float(cin[1][k]))
    if cout is not None:
        for k, (i, va, vb) in enumerate(S["link"][t]):
            box[va] = (float(cout[0][k]), float(cout[1][k]))
    return box


def scip_task(a):
    """SCIP (no propagation) on one pair with the pair's slopes.  Returns the
    value of the best solution and ALL stored solutions (start levels, end
    levels, objective value) as planning points.  Never a bound."""
    import period
    import bundle
    key, t, cin, cout, lin, lout, tl, maxsols = a
    D = _W["D"]
    T = D["T"]
    lam = [[0.0, 0.0, 0.0] for _ in range(T - 1)]
    if t > 0:
        lam[t - 1] = list(lin)
    if t < T - 1:
        lam[t] = list(lout)
    tic = time.time()
    S = D["S"]
    try:
        objc = period.window_objective(D, t, t + 1, lam, 0.0)
        m, X = period.build(D, t, t + 1, objc, bundle.NOPROP, _box(D, t, cin, cout))
    except ValueError:
        return key, dict(est=INF, status="infeasible", sols=[], time=time.time() - tic)
    m.setParam("limits/time", tl)
    m.optimize()
    st = m.getStatus()
    sols = []
    for sol in m.getSols()[:maxsols]:
        x = {v: m.getSolVal(sol, X[v]) for v in X}
        s = [x[b] for (i, a_, b) in S["link"][t - 1]] if t > 0 else None
        e = [x[a_] for (i, a_, b) in S["link"][t]] if t < T - 1 else None
        obj = sum(c * x[v] for v, c in objc.items())
        sols.append((s, e, obj))
    est = sols[0][2] if sols else (INF if st == "infeasible" else math.nan)
    m.freeProb()
    return key, dict(est=est, status=st, sols=sols, time=time.time() - tic)


def rbb_task(a):
    """Rigorous lower bound on one pair (core.PeriodBounder -> rbb.solve), with
    the rc=False retry of sepbranch/tasks.py."""
    import warnings
    import core
    key, t, cin, cout, lin, lout, target, node_limit, time_limit = a
    D = _W["D"]
    if t not in _W["PB"]:
        _W["PB"][t] = core.PeriodBounder(D, t)
    PB = _W["PB"][t]
    ci = None if cin is None else (np.array(cin[0]), np.array(cin[1]))
    co = None if cout is None else (np.array(cout[0]), np.array(cout[1]))
    tic = time.time()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        res = PB.bound(ci, co, lin, lout, 0.0, target, node_limit=node_limit, time_limit=time_limit)
        retry = None
        if res["bound"] < target and res.get("nodes", 0) < node_limit and time.time() - tic < time_limit:
            r2 = PB.bound(ci, co, lin, lout, 0.0, target, node_limit=node_limit, time_limit=time_limit, rc=False)
            retry = dict(bound=float(r2["bound"]), status=r2["status"], nodes=int(r2.get("nodes", 0)))
            if r2["bound"] > res["bound"]:
                res = dict(r2, nodes=res.get("nodes", 0) + r2.get("nodes", 0))
    return key, dict(bound=float(res["bound"]), status=res["status"], nodes=int(res.get("nodes", 0)), retry=retry,
                     time=time.time() - tic, target=float(target), lam_in=[float(v) for v in lin],
                     lam_out=[float(v) for v in lout], mu=0.0, cin_box=cin, cout_box=cout)


# ------------------------------------------------------------------ from cert3
def from_cert3(pkl):
    """Initial state: cells, slopes, SCIP points and rigorous records of cert3."""
    import pickle
    from dpcells import CellPlan  # noqa: F401
    P = pickle.load(open(pkl, "rb"))
    T = P.T
    import copy
    st = State(T, copy.deepcopy(P.cells), copy.deepcopy(P.leaves), [list(map(float, l)) for l in P.lam])
    for rec in P.erecs:
        t = rec["t"]
        lin, lout = P.slopes(t)
        if rec["status"] == "infeasible" or (rec["est"] == INF):
            st.scip_inf.add((t, rec["cin"], rec["cout"]))
        sols = []
        if rec["s"] is not None or rec["e"] is not None:
            if math.isfinite(rec["est"]):
                sols = [(rec["s"], rec["e"], rec["est"])]
        st.add_eval(t, rec["cin"], rec["cout"], lin, lout,
                    dict(est=rec["est"], status=rec["status"], sols=sols, time=rec["time"]))
    for i, rec in enumerate(P.crecs):
        r = dict(rec)
        r["src"] = ("cert3", i)
        st.recs.append(r)
    return st


# ------------------------------------------------------------------ slope LP
def slope_lp(st, tab, inc, delta, active=None, fcap=1e6, pmargin=INF):
    """Trust-region LP over the cell slopes (planning).

    Maximizes the shortest-path value of the concave piecewise-linear pair model
      U-pairs (pool points in the pair):  min_p c0_p + lam_in . s_p - lam_out . e_p
      L-pairs (no point; not proved empty): L(center) + min_{s in D}(lam_in - c_in).s
                                                      + min_{e in D'} -(lam_out - c_out).e
    (the L-model is a valid lower bound of the rigorous record bound at the new
    slopes), over |lam - center|_k <= delta_k per cell.  active[link]: boolean
    mask of leaves whose slope may move (others fixed at the center).
    Returns (z, new slopes per link as arrays)."""
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix
    T = st.T
    nl = [len(st.leaves[l]) for l in range(T - 1)]
    off = 0
    o_lam, o_f, o_ui, o_uo = [], [], [], []
    for l in range(T - 1):
        o_lam.append(off); off += 3 * nl[l]
    for l in range(T - 1):
        o_f.append(off); off += nl[l]
    oz = off; off += 1
    for l in range(T - 1):
        o_ui.append(off); off += 3 * nl[l]
    for l in range(T - 1):
        o_uo.append(off); off += 3 * nl[l]
    nv = off
    LAMC = [st.lam_arr(l) for l in range(T - 1)]
    BOX = [st.boxes(l) for l in range(T - 1)]
    rows, cols, vals, rhs = [], [], [], []
    nr = [0]

    def add(entries, b):
        i = nr[0]
        for (j, a) in entries:
            rows.append(i); cols.append(j); vals.append(a)
        rhs.append(b)
        nr[0] += 1

    def fvar(t, r, c):
        """(lhs entries for 'value-to-node' side): +head - tail."""
        ent = []
        if t < T - 1:
            ent.append((o_f[t] + c, 1.0))
        else:
            ent.append((oz, 1.0))
        if t > 0:
            ent.append((o_f[t - 1] + r, -1.0))
        return ent

    nU = nL = 0
    for t in range(T):
        d = tab[t]
        S, E, C0 = st.point_arrays(t)
        P, R, C = inc[t]
        okU = np.isfinite(d["U"]) & (d["L"] < INF)
        vc = C0[P].copy() if len(P) else np.zeros(0)
        if len(P):
            if t > 0:
                vc += (LAMC[t - 1][R] * S[P]).sum(1)
            if t < T - 1:
                vc -= (LAMC[t][C] * E[P]).sum(1)
        for p, r, c, v in zip(P, R, C, vc):
            if not okU[r, c] or v > d["U"][r, c] + pmargin:
                continue
            ent = fvar(t, r, c)
            if t > 0:
                for k in range(3):
                    ent.append((o_lam[t - 1] + 3 * r + k, -S[p, k]))
            if t < T - 1:
                for k in range(3):
                    ent.append((o_lam[t] + 3 * c + k, E[p, k]))
            add(ent, C0[p])
            nU += 1
        okL = (~np.isfinite(d["U"])) & (~d["SINF"]) & (d["L"] < INF) & (d["L"] > -INF)
        for r, c in zip(*np.nonzero(okL)):
            ent = fvar(t, r, c)
            if t > 0:
                for k in range(3):
                    ent.append((o_ui[t - 1] + 3 * r + k, -1.0))
            if t < T - 1:
                for k in range(3):
                    ent.append((o_uo[t] + 3 * c + k, -1.0))
            add(ent, d["L"][r, c])
            nL += 1
    for l in range(T - 1):
        lo, hi = BOX[l]
        for r in range(nl[l]):
            for k in range(3):
                jl = o_lam[l] + 3 * r + k
                lc = LAMC[l][r, k]
                add([(o_ui[l] + 3 * r + k, 1.0), (jl, -lo[r, k])], -lo[r, k] * lc)
                add([(o_ui[l] + 3 * r + k, 1.0), (jl, -hi[r, k])], -hi[r, k] * lc)
                add([(o_uo[l] + 3 * r + k, 1.0), (jl, lo[r, k])], lo[r, k] * lc)
                add([(o_uo[l] + 3 * r + k, 1.0), (jl, hi[r, k])], hi[r, k] * lc)
    A = coo_matrix((vals, (rows, cols)), shape=(nr[0], nv)).tocsr()
    b = np.array(rhs)
    lb = np.full(nv, -fcap)
    ub = np.full(nv, fcap)
    for l in range(T - 1):
        for r in range(nl[l]):
            for k in range(3):
                j = o_lam[l] + 3 * r + k
                dk = delta[k] if (active is None or active[l][r]) else 0.0
                lb[j] = LAMC[l][r, k] - dk
                ub[j] = LAMC[l][r, k] + dk
    cvec = np.zeros(nv)
    cvec[oz] = -1.0
    tic = time.time()
    res = linprog(cvec, A_ub=A, b_ub=b, bounds=list(zip(lb, ub)), method="highs")
    el = time.time() - tic
    if res.status != 0:
        raise RuntimeError(f"slope LP failed: {res.message}")
    x = res.x
    new = [x[o_lam[l]:o_lam[l] + 3 * nl[l]].reshape(nl[l], 3) for l in range(T - 1)]
    return float(x[oz]), new, dict(nU=nU, nL=nL, rows=nr[0], vars=nv, time=el)


def set_slopes(st, new):
    for l in range(st.T - 1):
        for r, cid in enumerate(st.leaves[l]):
            st.lam[l][cid] = [float(v) for v in new[l][r]]


def load(path):
    """Load a pickled state (plain or gzip-compressed)."""
    import gzip
    import pickle
    with (gzip.open(path, "rb") if path.endswith(".gz") else open(path, "rb")) as fh:
        return pickle.load(fh)
