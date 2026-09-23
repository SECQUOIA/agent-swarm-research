"""McCormick LP relaxation of a QCQP with in-place bound updates, and iterated OBBT on it.

Relaxation (integrality dropped):
  * w_ij for each bilinear term x_i x_j (i != j): the four McCormick inequalities;
  * s_i for each square x_i^2: tangents at 5 equally spaced points of [l_i, u_i] and the secant;
    for binary x_i, x_i^2 is replaced by x_i;
  * every original row with its quadratic terms replaced by w / s;
  * an objective cutoff row  f_relax(x, w, s) <= U.
When a bound of x_i changes, the coefficients and right-hand sides of the rows of the terms that
contain x_i are rewritten in place, so Gurobi warm-starts from the previous basis.
"""
import math, time
import numpy as np
import gurobipy as gp
from gurobipy import GRB

NTAN = 5
MARGIN = 1e-6      # safety margin on each new bound: relax by MARGIN * (1 + |b|)
MINREL = 1e-4      # accept a tightening only if it shrinks the width by at least MINREL (relative)
MOVED = 1e-3       # a variable "moved" in a round if its width shrank by at least this fraction


class Relaxation:
    def __init__(self, P, lb, ub, env, U=math.inf):
        self.P = P
        self.lb = lb.astype(float).copy()
        self.ub = ub.astype(float).copy()
        m = gp.Model(env=env)
        m.Params.OutputFlag = 0
        m.Params.Threads = 1
        m.Params.Presolve = 0   # warm-started simplex; presolve is slower and misjudged thin LPs as infeasible
        self.m = m
        n = P.n
        big = lambda a: np.where(np.isinf(a), np.sign(a) * GRB.INFINITY, a)
        self.x = m.addMVar(n, lb=big(self.lb), ub=big(self.ub)).tolist()
        binsq = lambda i: P.isint[i] and self.lb[i] >= 0 and self.ub[i] <= 1
        self.aux = {}          # term -> variable (or x_i for binary squares)
        self.rows = {}         # term -> list of constraints
        self.byvar = {i: [] for i in P.nlvars}
        for t in P.terms:
            i, j = t
            if i == j and binsq(i):
                self.aux[t] = self.x[i]
                continue
            v = m.addVar(lb=0.0 if i == j else -GRB.INFINITY, ub=GRB.INFINITY)
            self.aux[t] = v
            if i == j:
                cs = [m.addConstr(v >= 0) for _ in range(NTAN)] + [m.addConstr(v <= 0)]
            else:
                cs = [m.addConstr(v >= 0), m.addConstr(v >= 0), m.addConstr(v <= 0), m.addConstr(v <= 0)]
            self.rows[t] = cs
            self.byvar[i].append(t)
            if j != i:
                self.byvar[j].append(t)
        m.update()
        for t in self.rows:
            self._write(t)
        # original rows
        A = P.A
        for r in range(P.m):
            e = gp.LinExpr()
            s, u = A.indptr[r], A.indptr[r + 1]
            e.addTerms(A.data[s:u].tolist(), [self.x[k] for k in A.indices[s:u]])
            for t, q in P.rq.get(r, {}).items():
                e.addTerms(q, self.aux[t])
            lo, hi = P.rlo[r], P.rhi[r]
            if lo == hi:
                m.addConstr(e == lo)
            else:
                if lo > -math.inf:
                    m.addConstr(e >= lo)
                if hi < math.inf:
                    m.addConstr(e <= hi)
        # objective in minimization form
        f = gp.LinExpr()
        f.addTerms((P.sense * P.c).tolist(), self.x)
        for t, q in P.oq.items():
            f.addTerms(P.sense * q, self.aux[t])
        self.fexpr = f
        self.fconst = P.sense * P.c0
        self.cut = m.addConstr(f <= GRB.INFINITY)
        m.update()
        self.set_cutoff(U)
        self.nlp = 0
        self.lptime = 0.0

    def set_cutoff(self, U):
        self.U = U
        self.cut.RHS = GRB.INFINITY if not math.isfinite(U) else U - self.fconst

    def _write(self, t):
        """Rewrite the relaxation rows of term t for the current bounds."""
        i, j = t
        m, v, cs = self.m, self.aux[t], self.rows[t]
        xi, xj = self.x[i], self.x[j]
        li, ui, lj, uj = self.lb[i], self.ub[i], self.lb[j], self.ub[j]
        if i == j:
            for k in range(NTAN):
                p = li + (ui - li) * k / (NTAN - 1)
                m.chgCoeff(cs[k], xi, -2 * p)
                cs[k].RHS = -p * p
            m.chgCoeff(cs[NTAN], xi, -(li + ui))
            cs[NTAN].RHS = -li * ui
            return
        for c, (a, b) in zip(cs, ((lj, li), (uj, ui), (uj, li), (lj, ui))):
            # w - a x_i - b x_j (>= or <=) -a*b  with (a, b) = (partner bound for x_i, bound of x_i)
            m.chgCoeff(c, xi, -a)
            m.chgCoeff(c, xj, -b)
            c.RHS = -a * b

    def set_bounds(self, k, l, u):
        self.lb[k], self.ub[k] = l, u
        self.x[k].LB, self.x[k].UB = l, u
        for t in self.byvar.get(k, ()):
            self._write(t)

    def solve(self, obj, sense):
        """Optimize a linear objective; returns (status, value, x-values)."""
        m = self.m
        m.setObjective(obj, sense)
        t = time.time()
        m.optimize()
        self.lptime += time.time() - t
        self.nlp += 1
        if m.Status == GRB.OPTIMAL:
            return m.Status, m.ObjVal, np.array(m.getAttr('X', self.x))
        return m.Status, None, None

    def bound(self):
        """Relaxation lower bound on the minimization-form objective (inf if infeasible)."""
        st, val, xv = self.solve(self.fexpr, GRB.MINIMIZE)
        if st == GRB.OPTIMAL:
            return val + self.fconst, xv
        if st in (GRB.INFEASIBLE, GRB.INF_OR_UNBD):
            return math.inf, None
        return -math.inf, None


def _newbound(P, k, val, lower):
    b = val - MARGIN * (1 + abs(val)) if lower else val + MARGIN * (1 + abs(val))
    if P.isint[k]:
        b = math.ceil(b - 1e-6) if lower else math.floor(b + 1e-6)
    return b


def obbt_round(R, cands, mode='GS', filtering=True, deadline=math.inf, xstart=None):
    """One OBBT round over the variables in cands.  Returns dict with the tightened set and flags."""
    P = R.P
    lo_done, hi_done = set(), set()

    def filt(xv):
        if not filtering or xv is None:
            return
        for k in cands:
            if xv[k] <= R.lb[k] + 1e-6 * (1 + abs(R.lb[k])):
                lo_done.add(k)
            if xv[k] >= R.ub[k] - 1e-6 * (1 + abs(R.ub[k])):
                hi_done.add(k)

    filt(xstart)
    pending = {}  # Jacobi: new bounds applied at the end
    changed = set()
    infeasible = capped = False
    nsolved = ninf = 0
    for k in cands:
        for lower in (True, False):
            if (k in lo_done) if lower else (k in hi_done):
                continue
            if time.time() > deadline:
                capped = True
                break
            left = deadline - time.time()
            R.m.Params.TimeLimit = min(left, 1e9) if math.isfinite(left) else GRB.INFINITY
            st, val, xv = R.solve(R.x[k], GRB.MINIMIZE if lower else GRB.MAXIMIZE)
            nsolved += 1
            if st == GRB.INFEASIBLE or st == GRB.INF_OR_UNBD:
                # With U >= f* the LP cannot be truly infeasible; this is a numerical artifact of the
                # tight cutoff (seen with the known-optimum cutoff).  Ignore the LP.
                ninf += 1
                continue
            if val is None:
                continue
            filt(xv)
            (lo_done if lower else hi_done).add(k)
            l, u = pending.get(k, (R.lb[k], R.ub[k]))
            w = u - l
            b = _newbound(P, k, val, lower)
            if lower and b > l + max(MINREL * w, 1e-9):
                l = min(b, u)
            elif not lower and b < u - max(MINREL * w, 1e-9):
                u = max(b, l)
            else:
                continue
            changed.add(k)
            if mode == 'GS':
                R.set_bounds(k, l, u)
            else:
                pending[k] = (l, u)
        if capped:
            break
    if mode != 'GS':
        for k, (l, u) in pending.items():
            R.set_bounds(k, l, u)
    R.m.Params.TimeLimit = GRB.INFINITY
    return dict(changed=changed, infeasible=ninf, capped=capped, nlp=nsolved)


def partners(P):
    nb = {i: set() for i in P.nlvars}
    for i, j in P.terms:
        nb[i].add(j)
        nb[j].add(i)
    return nb


def iterate(R, mode='GS', restrict=False, filtering=True, max_rounds=50, time_cap=math.inf,
            snap_rounds=(1, 5), thetas=(0.5, 0.8), theta_cap=math.inf, w0=None, stop_when_ad_done=False,
            prefix=None):
    """Iterated OBBT.  Records per-round statistics and snapshots of the box for stopping rules:
      'r<k>'   : after round k (fixed rounds);
      'ad<th>' : adaptive: stop after the first round whose contraction ratio rho > th, or once the
                 cumulative OBBT time reaches theta_cap (checked between rounds);
      'fp'     : last round (fixed point, round limit or time cap).
    rho of a round = sum of normalized widths after / before, over the variables that moved in it
    (widths normalized by w0, the widths at the start of OBBT).
    prefix: continue a trajectory whose first round was computed elsewhere (dict with 'hist' of
    that round, 'changed' and 'LB0'); R must then be built on the box after that round."""
    P = R.P
    nl = np.array(P.nlvars)
    w0 = (R.ub - R.lb)[nl] if w0 is None else w0
    pos = w0 > 0
    nb = partners(P)
    t0 = time.time()
    hist = []
    snaps = {}
    alive = {th: True for th in thetas}
    cands = list(P.nlvars)
    changed1 = None

    def record(h, res_changed, res_infeasible):
        hist.append(h)
        box = (R.lb.copy(), R.ub.copy())
        rnd = h['round']
        if rnd in snap_rounds:
            snaps['r%d' % rnd] = dict(box=box, round=rnd, time=h['cum'])
        for th in thetas:
            if alive[th]:
                snaps['ad%g' % th] = dict(box=box, round=rnd, time=h['cum'])
                if h['rho'] > th or h['cum'] >= theta_cap or not res_changed:
                    alive[th] = False

    def next_cands(changed):
        if not restrict:
            return list(P.nlvars)
        nxt = set(changed)
        for k in changed:
            nxt |= nb.get(k, set())
        return [k for k in P.nlvars if k in nxt]

    start = 1
    if prefix is not None:
        h = dict(prefix['hist'][0])
        t0 -= h['cum']
        record(h, prefix['changed'], h['infeasible'])
        lb0 = prefix['LB0']
        start = 2
        cands = next_cands(prefix['changed'])
        stop = h['capped'] or not prefix['changed'] or \
            (stop_when_ad_done and not any(alive.values()))
        if stop:
            max_rounds = 1
    deadline = t0 + time_cap
    LB, xstart = R.bound()
    if prefix is None:
        lb0 = LB
    for rnd in range(start, max_rounds + 1):
        wb = (R.ub - R.lb)[nl]
        tr = time.time()
        res = obbt_round(R, cands, mode, filtering, deadline, xstart)
        LB, xstart = R.bound()
        wa = (R.ub - R.lb)[nl]
        tr = time.time() - tr
        if rnd == 1:
            changed1 = sorted(res['changed'])
        mv = pos & (wa < wb * (1 - MOVED))
        nwb, nwa = wb[mv] / w0[mv], wa[mv] / w0[mv]
        rho = float(nwa.sum() / nwb.sum()) if mv.any() else 1.0
        r_i = np.maximum(wa[mv] / np.where(wb[mv] > 0, wb[mv], 1), 1e-3)
        gm = float(np.exp(np.mean(np.log(r_i)))) if mv.any() else 1.0
        S = float((wa[pos] / w0[pos]).sum())
        h = dict(round=rnd, time=tr, cum=time.time() - t0, nlp=res['nlp'], ncand=len(cands),
                 nchanged=len(res['changed']), nmoved=int(mv.sum()), rho=rho, gm=gm, S=S,
                 maxw=float((wa[pos] / w0[pos]).max()) if pos.any() else 0.0, LB=LB,
                 infeasible=res['infeasible'], capped=res['capped'])
        record(h, res['changed'], res['infeasible'])
        if res['capped'] or not res['changed']:
            break
        if stop_when_ad_done and not any(alive.values()):
            break
        cands = next_cands(res['changed'])
    for r in snap_rounds:  # converged before round r: same box
        if 'r%d' % r not in snaps:
            snaps['r%d' % r] = dict(box=(R.lb.copy(), R.ub.copy()), round=len(hist), time=hist[-1]['cum'])
    snaps['fp'] = dict(box=(R.lb.copy(), R.ub.copy()), round=len(hist), time=hist[-1]['cum'])
    return dict(hist=hist, snaps=snaps, LB0=lb0, total=time.time() - t0, changed1=changed1)
