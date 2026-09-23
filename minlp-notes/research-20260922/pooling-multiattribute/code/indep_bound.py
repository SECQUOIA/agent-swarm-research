"""Independent verification of the pq + disaggregated single-pool single-output ("D") root bound.

Built directly from the MINLPLib OSiL file (decimal data read by benchmark-observations/code/osil_eval.py);
does not use spp.py, instance.py or gridrelax.py.

Relaxation (all rows valid for every feasible point of the original pq model):
  * every original linear row and variable bound;
  * McCormick rows for every bilinear row w = q*y (q in [0,qU], y in [0,XU]);
  * implied rows: sum_i w_ilj = y_lj (simplex times y), and q_il * (C - pool-capacity row) >= 0;
  * for every y_lj (block b): the disjunctive (Balas) relaxation of
        S_b = {(x,q,w,v): x in [0,XU], q in pool simplex, w_i = x q_i, sum w = x, 0 <= v,
               every original linear row whose support lies in the flows into the block's output}
    where v aggregates the other flows into the output that have identical coefficient vectors in those
    rows, and the x-range [0,XU] is split into intervals with McCormick rows per interval.
Safe bound: Neumaier-Shcherbina style: y = sign-corrected row duals, d = c - A^T y with a rigorous error bound
(including 2^-52 relative uncertainty of every float coefficient vs. its decimal), then
b^T y + sum_j min_{x_j in [l_j,u_j], d_j in [dlo,dhi]} d_j x_j, final sums in exact rational arithmetic.
"""
import sys, json, time, math
from fractions import Fraction as Fr
from collections import defaultdict
import numpy as np
import scipy.sparse as sp
import gurobipy as gp
from gurobipy import GRB

sys.path.insert(0, "/home/sgusev/repo/minlp-notes/research-20260922/benchmark-observations/code")
import osil_eval as O

INF = float("inf")


class Struct:
    def __init__(self, path):
        M = O.Model(path); self.M = M; n = M.n; self.n = n
        assert M.objsense == "min" and not M.nl and not M.quad.get(-1) and Fr(M.objconst) == 0
        assert all(Fr(s) == 0 for s in M.vlb) and all(t == "C" for t in M.vtype)
        self.ub = [Fr(s) for s in M.vub]
        self.c = {j: Fr(s) for j, s in M.objlin.items()}
        self.W = {}
        self.lin = []  # (dict var->Fr, lb, ub) for linear rows
        for r in range(M.m):
            assert Fr(M.cconst[r]) == 0
            if M.quad.get(r):
                (w, cw), = M.lin[r].items(); (a, b, cq), = M.quad[r]
                assert Fr(cw) == 1 and Fr(cq) == -1 and Fr(M.clb[r]) == 0 and Fr(M.cub[r]) == 0
                self.W[w] = (a, b)
            else:
                lb = None if M.clb[r] == "-INF" else Fr(M.clb[r]); ub = None if M.cub[r] == "INF" else Fr(M.cub[r])
                self.lin.append(({j: Fr(s) for j, s in M.lin[r].items()}, lb, ub, r))
        Qv = {a for a, b in self.W.values()}; Yv = {b for a, b in self.W.values()}
        assert not (Qv & Yv) and not (Qv & set(self.W)) and not (Yv & set(self.W))
        # pools: simplex rows sum q = 1
        self.pool_of_q = {}; self.pools = []
        for k, (row, lb, ub, r) in enumerate(self.lin):
            if lb == ub == 1 and set(row) <= Qv:
                assert all(v == 1 for v in row.values())
                for q in row: assert q not in self.pool_of_q; self.pool_of_q[q] = len(self.pools)
                self.pools.append(sorted(row))
        assert set(self.pool_of_q) == Qv
        # y variables occur only in bilinear rows (checked) -> blocks keyed by y
        for row, lb, ub, r in self.lin: assert not (set(row) & Yv) and not (set(row) & Qv and not set(row) <= Qv)
        assert not (set(self.c) & (Qv | Yv))
        self.blocks = []
        wy = defaultdict(list)
        for w, (a, b) in self.W.items(): wy[b].append(w)
        rows_of = defaultdict(list)
        for k, (row, lb, ub, r) in enumerate(self.lin):
            for v in row: rows_of[v].append(k)
        for y in sorted(wy):
            Wb = sorted(wy[y], key=lambda w: self.W[w][0])
            qs = [self.W[w][0] for w in Wb]
            pools = {self.pool_of_q[q] for q in qs}; assert len(pools) == 1; p = pools.pop()
            assert len(set(qs)) == len(qs)
            complete = sorted(qs) == self.pools[p]
            # flows of the output: supports of the "<= 0" (quality) rows touching Wb
            Fb = set(Wb)
            for w in Wb:
                for k in rows_of[w]:
                    row, lb, ub, r = self.lin[k]
                    if lb is None and ub == 0: Fb |= set(row)
            brows = sorted({k for w in Wb for k in rows_of[w] if set(self.lin[k][0]) <= Fb})
            others = sorted(Fb - set(Wb))
            # group other flows by coefficient vector over the block rows
            grp = defaultdict(list)
            for f in others: grp[tuple(self.lin[k][0].get(f, Fr(0)) for k in brows)].append(f)
            groups = list(grp.values())
            # XU: y bound, sum of w bounds, and rows with coefficient 1 on every w of the block and >=0 elsewhere
            XU = min(self.ub[y], sum(self.ub[w] for w in Wb))
            if complete:
                for k in {k for w in Wb for k in rows_of[w]}:
                    row, lb, ub, r = self.lin[k]
                    if ub is not None and all(row.get(w) == 1 for w in Wb) and all(v >= 0 for v in row.values()):
                        XU = min(XU, ub)
            self.blocks.append(dict(y=y, W=Wb, q=qs, pool=p, complete=complete, rows=brows, groups=groups, XU=XU))

    def summary(self):
        b = self.blocks
        return dict(n=self.n, bil=len(self.W), lin=len(self.lin), pools=len(self.pools), blocks=len(b),
                    all_complete=all(x["complete"] for x in b),
                    rows_per_block=[min(len(x["rows"]) for x in b), max(len(x["rows"]) for x in b)],
                    groups_per_block=[min(len(x["groups"]) for x in b), max(len(x["groups"]) for x in b)],
                    XU_tightened=sum(x["XU"] < self.ub[x["y"]] for x in b))


class LP:
    """Sparse LP in rows: sum a x (sense) b; exact data kept as floats (all entries treated as uncertain by 2^-52)."""
    def __init__(self):
        self.ri, self.ci, self.v = [], [], []; self.rhs = []; self.sense = []; self.m = 0
        self.lb, self.ub, self.obj = [], [], []

    def var(self, lb, ub, obj=0.0, k=1):
        s = len(self.lb); self.lb += [float(lb)] * k; self.ub += [float(ub)] * k; self.obj += [float(obj)] * k
        return s

    def row(self, coefs, sense, rhs):
        r = self.m; self.m += 1
        for j, a in coefs:
            if a != 0: self.ri.append(r); self.ci.append(j); self.v.append(float(a))
        self.sense.append(sense); self.rhs.append(float(rhs))
        return r


def f_down(x):
    """largest float <= Fraction x"""
    f = float(x)
    return f if Fr(f) <= x else math.nextafter(f, -INF)


def build(S, grid, blocks=True):
    lp = LP(); n = S.n
    for j in range(n):
        assert Fr(float(S.ub[j])) == S.ub[j]  # bounds are exactly representable (certificate treats bounds as exact)
        lp.var(0.0, S.ub[j], S.c.get(j, 0))
    for (row, lb, ub, r) in S.lin:
        if ub is not None: lp.row(list(row.items()), "<", ub)
        if lb is not None: lp.row(list(row.items()), ">", lb)
    for b in S.blocks:
        y, XU = b["y"], b["XU"]
        assert Fr(float(XU)) == XU
        lp.ub[y] = min(lp.ub[y], float(XU))  # valid tightening (every feasible y_lj <= XU)
        XUf = lp.ub[y]
        for w, q in zip(b["W"], b["q"]):
            qu = float(S.ub[q]); assert Fr(qu) == S.ub[q]
            lp.row([(w, 1), (q, -XUf)], "<", 0)            # w <= XU q
            lp.row([(w, 1), (y, -qu)], "<", 0)             # w <= qU y
            assert Fr(XUf) * Fr(qu) == Fr(XUf * qu)
            lp.row([(w, 1), (q, -XUf), (y, -qu)], ">", -XUf * qu)  # (XU-y)(qU-q) >= 0 ... rearranged: w >= XU q + qU y - XU qU
        if b["complete"]:
            lp.row([(w, 1) for w in b["W"]] + [(y, -1)], "=", 0)
    # q_il * (C - row) >= 0 for capacity rows equal to all paths of one pool through a set of complete blocks
    by_pool = defaultdict(list)
    for b in S.blocks: by_pool[b["pool"]].append(b)
    nrlt = 0
    for (row, lb, ub, r) in S.lin:
        if ub is None or not all(v == 1 for v in row.values()) or not set(row) <= set(S.W): continue
        ys = {S.W[w][1] for w in row}; bl = [b for b in S.blocks if b["y"] in ys]
        if not all(b["complete"] for b in bl) or set(row) != {w for b in bl for w in b["W"]}: continue
        p = bl[0]["pool"]; assert all(b["pool"] == p for b in bl)
        for q in S.pools[p]:
            lp.row([(w, 1) for w in row if S.W[w][0] == q] + [(q, -float(ub))], "<", 0); nrlt += 1
    if not blocks:
        return lp, dict(nrlt=nrlt)
    npieces = 0
    for b in S.blocks:
        XU = lp.ub[b["y"]]; xs = [XU * t for t in grid]; xs[-1] = XU
        ivs = list(zip(xs[:-1], xs[1:]))
        k = len(b["W"]); G = len(b["groups"]); qs = S.pools[b["pool"]]
        qu = [float(S.ub[q]) for q in qs]
        wub = [float(S.ub[w]) for w in b["W"]]
        vub = [float(sum(S.ub[f] for f in g)) for g in b["groups"]]
        assert all(Fr(v) == sum(S.ub[f] for f in g) for v, g in zip(vub, b["groups"]))
        qpos = [qs.index(q) for q in b["q"]]
        lam0 = lp.var(0, 1, k=len(ivs))
        lp.row([(lam0 + g, 1) for g in range(len(ivs))], "=", 1)
        coord = {"x": [], "q": [[] for _ in qs], "w": [[] for _ in range(k)], "v": [[] for _ in range(G)]}
        b["_pieces"] = []
        for g, (lo, hi) in enumerate(ivs):
            L = lam0 + g
            x = lp.var(0, hi); q0 = lp.var(0, 1, k=len(qs)); w0 = lp.var(0, max(wub), k=k); v0 = lp.var(0, max(vub + [0]), k=G)
            for a in range(len(qs)): lp.ub[q0 + a] = qu[a]
            for a in range(k): lp.ub[w0 + a] = min(wub[a], hi * qu[qpos[a]]) if hi * qu[qpos[a]] == Fr(hi) * Fr(qu[qpos[a]]) else wub[a]
            for a in range(G): lp.ub[v0 + a] = vub[a]
            coord["x"].append(x); b["_pieces"].append((lo, hi, L, x, q0, w0, v0))
            for a in range(len(qs)): coord["q"][a].append(q0 + a)
            for a in range(k): coord["w"][a].append(w0 + a)
            for a in range(G): coord["v"][a].append(v0 + a)
            lp.row([(x, 1), (L, -lo)], ">", 0); lp.row([(x, 1), (L, -hi)], "<", 0)
            for a in range(len(qs)): lp.row([(q0 + a, 1), (L, -qu[a])], "<", 0)
            for a in range(k): lp.row([(w0 + a, 1), (L, -wub[a])], "<", 0)
            for a in range(G): lp.row([(v0 + a, 1), (L, -vub[a])], "<", 0)
            lp.row([(q0 + a, 1) for a in range(len(qs))] + [(L, -1)], "=", 0)
            if b["complete"]:
                lp.row([(w0 + a, 1) for a in range(k)] + [(x, -1)], "=", 0)
            for a in range(k):
                qa, U = q0 + qpos[a], qu[qpos[a]]; wa = w0 + a
                assert Fr(hi) * Fr(U) == Fr(hi * U) and Fr(lo) * Fr(U) == Fr(lo * U)  # exact products
                lp.row([(wa, 1), (qa, -lo)], ">", 0)                                    # (x-lo)(q-0) >= 0
                lp.row([(wa, 1), (qa, -hi), (x, -U), (L, hi * U)], ">", 0)              # (hi-x)(U-q) >= 0
                lp.row([(wa, 1), (qa, -hi)], "<", 0)                                    # (hi-x)(q-0) >= 0
                lp.row([(wa, 1), (qa, -lo), (x, -U), (L, lo * U)], "<", 0)              # (x-lo)(U-q) >= 0
            for kk in b["rows"]:
                row, rlb, rub, r = S.lin[kk]
                co = [(w0 + a, row.get(w, 0)) for a, w in enumerate(b["W"])]
                co += [(v0 + a, row.get(grp[0], 0)) for a, grp in enumerate(b["groups"])]
                if rub is not None: lp.row(co + [(L, -rub)], "<", 0)
                if rlb is not None: lp.row(co + [(L, -rlb)], ">", 0)
            npieces += 1
        # linking: original coordinates = sum of piece copies
        lp.row([(b["y"], 1)] + [(c, -1) for c in coord["x"]], "=", 0)
        for a, q in enumerate(qs): lp.row([(q, 1)] + [(c, -1) for c in coord["q"][a]], "=", 0)
        for a, w in enumerate(b["W"]): lp.row([(w, 1)] + [(c, -1) for c in coord["w"][a]], "=", 0)
        for a, grp in enumerate(b["groups"]): lp.row([(f, 1) for f in grp] + [(c, -1) for c in coord["v"][a]], "=", 0)
    return lp, dict(nrlt=nrlt, npieces=npieces)


def lift(S, lp, z):
    """Lift an original point z (length n) into the LP space: lambda = 1 on one piece containing y_lj."""
    Z = np.zeros(len(lp.lb)); Z[:S.n] = z
    for b in S.blocks:
        xv = z[b["y"]]; qs = S.pools[b["pool"]]
        pcs = b.get("_pieces", [])
        if not pcs: continue
        g = next((i for i, pc in enumerate(pcs) if pc[0] <= xv <= pc[1]), len(pcs) - 1 if xv > pcs[-1][1] else 0)
        lo, hi, L, x, q0, w0, v0 = pcs[g]
        Z[L] = 1.0; Z[x] = xv
        for a, q in enumerate(qs): Z[q0 + a] = z[q]
        for a, w in enumerate(b["W"]): Z[w0 + a] = z[w]
        for a, grp in enumerate(b["groups"]): Z[v0 + a] = sum(z[f] for f in grp)
    return Z


def violation(A, rhs, sense, lb, ub, Z):
    """max violation of rows and bounds, absolute and relative to row scale (1 + |a|.|Z| + |b|)."""
    act = A @ Z; scale = 1.0 + abs(A) @ np.abs(Z) + np.abs(rhs)
    v = np.where(sense == "<", act - rhs, np.where(sense == ">", rhs - act, np.abs(act - rhs)))
    vb = max(float(np.max(lb - Z)), float(np.max(Z - ub)))
    i = int(np.argmax(v / scale))
    return dict(row_abs=float(v.max()), row_rel=float((v / scale).max()), worst_row=i, bound=vb)


def to_arrays(lp):
    A = sp.csr_matrix((np.array(lp.v), (np.array(lp.ri), np.array(lp.ci))), shape=(lp.m, len(lp.lb)))
    return A, np.array(lp.rhs), np.array(lp.sense), np.array(lp.lb), np.array(lp.ub), np.array(lp.obj)


def solve(A, rhs, sense, lb, ub, c, threads=16, crossover=True, method=2):
    m = gp.Model(); m.Params.OutputFlag = 1; m.Params.Threads = threads; m.Params.Method = method
    if not crossover: m.Params.Crossover = 0; m.Params.BarConvTol = 1e-10
    x = m.addMVar(A.shape[1], lb=lb, ub=ub, obj=c)
    m.addMConstr(A, x, sense, rhs)
    m.optimize()
    return m, x


def safe_bound(A, rhs, sense, lb, ub, c, pi):
    """Rigorous lower bound for min c x s.t. A x (sense) rhs, lb <= x <= ub, using any multipliers pi."""
    u = 2.0 ** -52
    y = pi.copy()
    y[(sense == "<") & (y > 0)] = 0.0; y[(sense == ">") & (y < 0)] = 0.0
    At = A.T.tocsr()
    d = c - At @ y
    absAy = abs(At) @ np.abs(y)
    nnz = np.diff(At.indptr)
    err = 2.0 * (nnz + 4) * u * (np.abs(c) + absAy) * (1 + 1e-6) + 1e-300
    dlo = d - err; dhi = d + err
    # rigorous float sums: each product rounded (rel. err <= u), fsum correctly rounded (err <= u|S|)
    assert np.all(np.isfinite(lb)) and np.all(np.isfinite(ub))
    tb = rhs * y
    tb = tb - np.abs(tb) * (4 * u)          # rhs decimal uncertainty + product rounding
    corners = np.stack([dlo * lb, dlo * ub, dhi * lb, dhi * ub])
    tx = corners.min(0)
    tx = tx - np.abs(tx) * (2 * u)          # product rounding
    tot = math.fsum(tb.tolist()); corr = math.fsum(tx.tolist())
    tot -= 2 * u * abs(tot) + 1e-300; corr -= 2 * u * abs(corr) + 1e-300
    return f_down(Fr(tot) + Fr(corr)), dict(max_err=float(err.max()), dual_sign_fixed=int(np.sum(pi != y)),
                            sum_neg_red=float(np.sum(np.minimum(dlo * lb, dlo * ub) - np.minimum(d * lb, d * ub))))


if __name__ == "__main__":
    path = sys.argv[1]; G = int(sys.argv[2]); mode = sys.argv[3] if len(sys.argv) > 3 else "D"
    t0 = time.time()
    S = Struct(path)
    print("STRUCT", json.dumps(S.summary()), flush=True)
    grid = np.unique(np.concatenate([np.linspace(0, 1, G), np.geomspace(1e-3, 0.05, 6)]))
    lp, info = build(S, list(grid), blocks=(mode == "D"))
    A, rhs, sense, lb, ub, c = to_arrays(lp)
    print("LP", A.shape, A.nnz, info, "build", time.time() - t0, flush=True)
    m, x = solve(A, rhs, sense, lb, ub, c, crossover=("nox" not in sys.argv))
    val = m.ObjVal
    pi = np.array(m.getAttr("Pi", m.getConstrs()))
    sb, sinfo = safe_bound(A, rhs, sense, lb, ub, c, pi)
    print("RESULT", json.dumps(dict(inst=S.M.name, mode=mode, grid=len(grid), lp_value=val, safe_bound=sb, **sinfo, time=time.time() - t0)), flush=True)
