"""LP relaxations R0 / R1 of min sense * net(x) over a box, with cut loops.

Variables: x (input), and per hidden layer z = W y_prev + b and y = sigma(z).
R0: outer approximation of the 1-D convex/concave envelopes of sigma over
    [Lz_j, Uz_j] (tangent-type cuts in (z_j, y_j), separated at the LP point).
R1: R0 plus Theorem 1 cuts in (y_prev, y_j) over the box of y_prev bounds
    (the input box for the first layer), both envelope sides.
Every cut comes from envelope.solve_batch and is certified valid.
"""
import time

import numpy as np
import scipy.sparse as sp
from gurobipy import GRB

from envelope import Problem, lp_model, solve_batch

TOL_ADD = 1e-6       # add a cut if it is violated by more than this at the LP point
ACTIVE_TOL = 1e-6    # cuts with slack below this are inherited by child nodes


class Bounds:
    def __init__(self, lx, ux, Lz, Uz, ly, uy):
        self.lx, self.ux, self.Lz, self.Uz, self.ly, self.uy = lx, ux, Lz, Uz, ly, uy

    def prev(self, l):
        return (self.lx, self.ux) if l == 0 else (self.ly[l - 1], self.uy[l - 1])

    def width_summary(self):
        return float(np.mean(np.concatenate([U - L for L, U in zip(self.Lz, self.Uz)])))


def ibp(net, lx, ux, inherit=None):
    """Interval bounds; intersected with inherited bounds (valid on a superset box)."""
    Lz, Uz, ly, uy = [], [], [], []
    lo, hi = np.asarray(lx, float), np.asarray(ux, float)
    for l, (W, b) in enumerate(zip(net.Ws, net.bs)):
        Wp, Wn = np.maximum(W, 0), np.minimum(W, 0)
        L = Wp @ lo + Wn @ hi + b
        U = Wp @ hi + Wn @ lo + b
        pad = 1e-12 * (1 + np.abs(L) + np.abs(U))
        L, U = L - pad, U + pad
        if inherit is not None:
            L, U = np.maximum(L, inherit.Lz[l]), np.minimum(U, inherit.Uz[l])
            U = np.maximum(U, L)
        yl, yu = net.act.range(L, U)
        if inherit is not None:
            yl, yu = np.maximum(yl, inherit.ly[l]), np.minimum(yu, inherit.uy[l])
            yu = np.maximum(yu, yl)
        Lz.append(L), Uz.append(U), ly.append(yl), uy.append(yu)
        lo, hi = yl, yu
    return Bounds(np.asarray(lx, float), np.asarray(ux, float), Lz, Uz, ly, uy)


class Cut:
    __slots__ = ("l", "j", "sgn", "kind", "c0", "g")

    def __init__(self, l, j, sgn, kind, c0, g):
        self.l, self.j, self.sgn, self.kind, self.c0, self.g = l, j, sgn, kind, c0, g


class NodeLP:
    """One LP: variables V = [x, z_0, y_0, z_1, y_1, ...]."""

    def __init__(self, net, sense, B, nlayers=None):
        self.net, self.sense, self.B = net, sense, B
        L = len(net.Ws) if nlayers is None else nlayers
        self.L = L
        d = net.d
        self.ix = np.arange(d)
        self.iz, self.iy = [], []
        off = d
        lb, ub = [B.lx], [B.ux]
        for l in range(L):
            n = net.Ws[l].shape[0]
            self.iz.append(np.arange(off, off + n))
            self.iy.append(np.arange(off + n, off + 2 * n))
            off += 2 * n
            lb += [B.Lz[l], B.ly[l]]
            ub += [B.Uz[l], B.uy[l]]
        self.N = off
        m = lp_model()
        m.Params.Method = 1
        self.V = m.addMVar(off, lb=np.concatenate(lb), ub=np.concatenate(ub))
        rows, cols, vals, rhs = [], [], [], []
        r = 0
        for l in range(L):
            W, b = net.Ws[l], net.bs[l]
            prev = self.ix if l == 0 else self.iy[l - 1]
            n, k = W.shape
            rr = np.repeat(np.arange(r, r + n), k)
            rows += [rr, np.arange(r, r + n)]
            cols += [np.tile(prev, n), self.iz[l]]
            vals += [W.ravel(), -np.ones(n)]
            rhs.append(-b)
            r += n
        A = sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(r, off))
        m.addMConstr(A, self.V, "=", np.concatenate(rhs))
        self.m = m
        self.cuts, self.constrs = [], []

    def set_output_objective(self):
        c = np.zeros(self.N)
        c[self.iy[self.L - 1]] = self.sense * self.net.w_out
        self.m.setObjective(c @ self.V, GRB.MINIMIZE)
        self.m.ObjCon = self.sense * self.net.b_out

    def add_cuts(self, cuts):
        if not cuts:
            return
        rows, cols, vals, rhs = [], [], [], []
        for i, c in enumerate(cuts):
            if c.kind == 0:
                idx = np.array([self.iz[c.l][c.j]])
                g = np.array([c.g[0]])
            else:
                idx = self.ix if c.l == 0 else self.iy[c.l - 1]
                g = c.g
            rows.append(np.full(len(idx) + 1, i))
            cols.append(np.concatenate([[self.iy[c.l][c.j]], idx]))
            vals.append(np.concatenate([[c.sgn], -g]))
            rhs.append(c.c0)
        A = sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(len(cuts), self.N))
        cons = self.m.addMConstr(A, self.V, ">", np.array(rhs))
        self.cuts += cuts
        self.constrs.append(cons)

    def solve(self):
        self.m.optimize()
        if self.m.Status != GRB.OPTIMAL:
            # numerical trouble: retry with barrier-free primal simplex from scratch
            self.m.reset()
            self.m.Params.Method = 0
            self.m.optimize()
            self.m.Params.Method = 1
        if self.m.Status != GRB.OPTIMAL:
            raise RuntimeError("LP status %d" % self.m.Status)
        return float(self.m.ObjVal), self.V.X

    def active_cuts(self):
        if not self.cuts:
            return []
        slack = np.concatenate([np.atleast_1d(c.Slack) for c in self.constrs])
        return [c for c, s in zip(self.cuts, slack) if abs(s) <= ACTIVE_TOL]

    def dispose(self):
        self.m.dispose()


def r0_problems(net, B, layers, fracs):
    """1-D envelope problems at z = L + f (U - L) for each neuron and side."""
    probs = []
    for l in layers:
        for j in range(len(B.Lz[l])):
            L, U = B.Lz[l][j], B.Uz[l][j]
            for f in fracs:
                for sgn in (1, -1):
                    probs.append(Problem(sgn, [L], [U], [1.0], 0.0, [L + f * (U - L)], tag=(l, j, sgn, 0)))
    return probs


def problems_to_cuts(probs):
    return [Cut(*P.tag, P.c0, P.g) for P in probs]


def separate(net, B, lp, v, mode):
    """Build separation problems at the LP point v; returns list of Problems."""
    act = net.act
    probs = []
    for l in range(lp.L):
        z, y = v[lp.iz[l]], v[lp.iy[l]]
        fz = act.f(z)
        prev_idx = lp.ix if l == 0 else lp.iy[l - 1]
        pl, pu = B.prev(l)
        pv = v[prev_idx]
        for sgn in (1, -1):
            cand = np.nonzero(sgn * (fz - y) > TOL_ADD)[0]
            for j in cand:
                probs.append(Problem(sgn, [B.Lz[l][j]], [B.Uz[l][j]], [1.0], 0.0, [z[j]], tag=(l, j, sgn, 0)))
                if mode == "R1":
                    probs.append(Problem(sgn, pl, pu, net.Ws[l][j], net.bs[l][j], pv, tag=(l, j, sgn, 1)))
    return probs


def cut_loop(net, lp, B, mode, max_rounds=100, stall_rounds=5, stall_tol=1e-6, record=None,
             cutoff=None, tail_frac=None, tail_rounds=2):
    """Iterate LP solve + separation. Returns dict with bound, point and statistics.

    Stops when no cut is violated, after max_rounds, when the bound improved by
    less than stall_tol * max(1, |bound|) over stall_rounds rounds, and (B&B only)
    when the bound reaches cutoff or improved by less than tail_frac of the
    remaining gap to cutoff over tail_rounds rounds.
    """
    t_lp = t_sep = 0.0
    hist = []
    ncuts = {0: 0, 1: 0}
    status = "max_rounds"
    for rnd in range(max_rounds):
        t0 = time.process_time()
        obj, v = lp.solve()
        t_lp += time.process_time() - t0
        hist.append(obj)
        if cutoff is not None and obj >= cutoff:
            status = "cutoff"
            break
        if (tail_frac is not None and len(hist) > tail_rounds
                and hist[-1] - hist[-1 - tail_rounds] < tail_frac * (cutoff - hist[-1])):
            status = "tailing"
            break
        t0 = time.process_time()
        probs = separate(net, B, lp, v, mode)
        probs = solve_batch(net.actname, probs)
        new = []
        for P in probs:
            l, j, sgn, kind = P.tag
            if P.value - sgn * v[lp.iy[l][j]] > TOL_ADD:
                new.append(Cut(l, j, sgn, kind, P.c0, P.g))
                if record is not None:
                    record.append(P)
        t_sep += time.process_time() - t0
        if not new:
            status = "converged"
            break
        if len(hist) > stall_rounds and hist[-1] - hist[-1 - stall_rounds] < stall_tol * max(1.0, abs(hist[-1])):
            status = "stalled"
            break
        for c in new:
            ncuts[c.kind] += 1
        lp.add_cuts(new)
    else:
        t0 = time.process_time()
        obj, v = lp.solve()
        t_lp += time.process_time() - t0
        hist.append(obj)
    return dict(bound=obj, v=v, rounds=len(hist), status=status, t_lp=t_lp, t_sep=t_sep,
                cuts_r0=ncuts[0], cuts_r1=ncuts[1], hist=hist)


def obbt(net, B, fracs=(0.0, 1 / 6, 1 / 3, 0.5, 2 / 3, 5 / 6, 1.0)):
    """OBBT of z bounds for layers >= 1 on a static R0 outer approximation.

    Layer 0 pre-activation bounds are exact from IBP (linear in x). Bounds are
    tightened layer by layer and pushed forward by IBP. Returns new Bounds.
    """
    B = ibp(net, B.lx, B.ux, inherit=B)
    nlp = 0
    for l in range(1, len(net.Ws)):
        lp = NodeLP(net, 1, B, nlayers=l + 1)
        lp.add_cuts(problems_to_cuts(solve_batch(net.actname, r0_problems(net, B, range(l), fracs))))
        iz = lp.iz[l]
        Lz, Uz = B.Lz[l].copy(), B.Uz[l].copy()
        for j in range(len(iz)):
            for s in (1, -1):
                c = np.zeros(lp.N)
                c[iz[j]] = s
                lp.m.setObjective(c @ lp.V, GRB.MINIMIZE)
                obj, _ = lp.solve()
                nlp += 1
                val = s * obj
                marg = 1e-7 * max(1.0, abs(val))
                if s > 0:
                    Lz[j] = max(Lz[j], val - marg)
                else:
                    Uz[j] = min(Uz[j], val + marg)
        lp.dispose()
        Uz = np.maximum(Uz, Lz)
        Bn = Bounds(B.lx, B.ux, list(B.Lz), list(B.Uz), list(B.ly), list(B.uy))
        Bn.Lz[l], Bn.Uz[l] = Lz, Uz
        B = ibp(net, B.lx, B.ux, inherit=Bn)
    return B, nlp


def root_bound(net, sense, B, mode, max_rounds=200, init_fracs=(1 / 6, 0.5, 5 / 6), record=None, inherit_cuts=None):
    lp = NodeLP(net, sense, B)
    lp.set_output_objective()
    t0 = time.process_time()
    lp.add_cuts(problems_to_cuts(solve_batch(net.actname, r0_problems(net, B, range(lp.L), init_fracs))))
    if inherit_cuts:
        lp.add_cuts(inherit_cuts)
    t_init = time.process_time() - t0
    res = cut_loop(net, lp, B, mode, max_rounds=max_rounds, record=record)
    res["t_init"] = t_init
    res["lp"] = lp
    return res
