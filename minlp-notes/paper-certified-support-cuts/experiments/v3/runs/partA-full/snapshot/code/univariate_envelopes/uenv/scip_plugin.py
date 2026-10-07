"""SCIP constraint handler for  w == g(x)  with g an arbitrary univariate expression.

Relaxation: exact convex/concave envelope cuts on the local interval of x.
Enforcement: envelope cut if violated, otherwise spatial branching on x.
Propagation: exact range of g forwards; interval trimming of x backwards.
"""
from __future__ import annotations

from types import SimpleNamespace

from pyscipopt import SCIP_PRESOLTIMING, SCIP_PROPTIMING, SCIP_RESULT, Conshdlr

from .envelope import Univariate


class UnivariateHdlr(Conshdlr):
    """``hybrid=True``: the model also contains the native constraint w == g(x).  SCIP then
    owns feasibility, branching and NLP heuristics, and this handler only supplies envelope
    cuts and propagation.  ``hybrid=False``: this handler alone enforces the constraint."""

    def __init__(self, hybrid: bool = False):
        self.hybrid = hybrid
        self.max_cuts_per_node = 12
        self.ncuts = self.nbranch = self.nprop = 0

    # ------------------------------------------------------------ helpers
    def _vars(self, cons):
        d = cons.data
        if d.tx is None:
            d.tx, d.tw = self.model.getTransformedVar(d.x), self.model.getTransformedVar(d.w)
        return d, d.tx, d.tw

    def _violation(self, cons, sol):
        d = cons.data
        xv, wv = self.model.getSolVal(sol, d.x), self.model.getSolVal(sol, d.w)
        xv = min(max(xv, d.f.lo), d.f.hi)
        gv = d.f.g(xv)
        return abs(wv - gv) / max(1.0, abs(gv)), xv, wv

    def _cut(self, cons, sol, min_viol):
        """Add the most violated envelope cut; returns (added, cutoff)."""
        m = self.model
        d, tx, tw = self._vars(cons)
        l, u = max(tx.getLbLocal(), d.f.lo), min(tx.getUbLocal(), d.f.hi)
        if l > u:
            return False, True
        node = m.getCurrentNode().getNumber()
        if d.node != node:
            d.node, d.node_cuts = node, 0
        if d.node_cuts >= self.max_cuts_per_node:
            return False, False
        xv, wv = m.getSolVal(sol, d.x), m.getSolVal(sol, d.w)
        xv = min(max(xv, l), u)
        is_local = l > tx.getLbGlobal() or u < tx.getUbGlobal()
        a, c = d.f.under(l, u, xv)
        if a * xv + c - wv > min_viol * max(1.0, abs(wv)):
            lhs, rhs, coef = c, None, a            # w - a x >= c
        else:
            a, c = d.f.over(l, u, xv)
            if wv - (a * xv + c) <= min_viol * max(1.0, abs(wv)):
                return False, False
            lhs, rhs, coef = None, c, a            # w - a x <= c
        row = m.createEmptyRowUnspec(f"uenv_{cons.name}_{self.ncuts}", lhs=lhs, rhs=rhs,
                                     local=is_local, removable=True)
        m.cacheRowExtensions(row)
        m.addVarToRow(row, tw, 1.0)
        m.addVarToRow(row, tx, -coef)
        m.flushRowExtensions(row)
        infeasible = m.addCut(row, forcecut=True)
        m.releaseRow(row)
        self.ncuts += 1
        d.node_cuts += 1
        return True, bool(infeasible)

    def _branch(self, cons, xv):
        m = self.model
        d, tx, tw = self._vars(cons)
        l, u = tx.getLbLocal(), tx.getUbLocal()
        if u - l <= 1e-9 * max(1.0, abs(l), abs(u)):
            return False
        point = min(max(xv, l + 0.2 * (u - l)), u - 0.2 * (u - l))
        m.branchVarVal(tx, point)
        self.nbranch += 1
        return True

    def _enforce(self, constraints, sol, allow_cuts):
        m = self.model
        feastol = m.feastol()
        violated = []
        for cons in constraints:
            viol, xv, _ = self._violation(cons, sol)
            if viol > feastol:
                violated.append((viol, cons, xv))
        if not violated:
            return {"result": SCIP_RESULT.FEASIBLE}
        violated.sort(key=lambda t: -t[0])
        self._try_completion(constraints, sol)
        separated = False
        if allow_cuts:
            for _, cons, _ in violated:
                added, cutoff = self._cut(cons, sol, feastol)
                if cutoff:
                    return {"result": SCIP_RESULT.CUTOFF}
                separated |= added
        if separated:
            return {"result": SCIP_RESULT.SEPARATED}
        if self.hybrid:
            return {"result": SCIP_RESULT.FEASIBLE}
        for _, cons, xv in violated:
            if self._branch(cons, xv):
                return {"result": SCIP_RESULT.BRANCHED}
        # Every violated x interval is below the branching width: fix x at its LP value,
        # after which propagation pins w to g(x).
        for _, cons, xv in violated:
            d, tx, tw = self._vars(cons)
            for tighten in (m.tightenVarLb, m.tightenVarUb):
                infeas, _ = tighten(tx, xv, force=True)
                if infeas:
                    return {"result": SCIP_RESULT.CUTOFF}
            if self._propagate(cons) == SCIP_RESULT.CUTOFF:
                return {"result": SCIP_RESULT.CUTOFF}
        return {"result": SCIP_RESULT.REDUCEDDOM}

    def _try_completion(self, constraints, sol):
        """Primal heuristic: keep x from the current point and set every w to g(x)."""
        m = self.model
        cand = m.createSol(None)
        for v in m.getVars(transformed=True):
            m.setSolVal(cand, v, m.getSolVal(sol, v))
        for cons in constraints:
            d, tx, tw = self._vars(cons)
            xv = min(max(m.getSolVal(sol, tx), d.f.lo), d.f.hi)
            m.setSolVal(cand, tw, d.f.g(xv))
        m.trySol(cand, printreason=False, completely=False, checkbounds=True,
                 checkintegrality=True, checklprows=True, free=True)

    def _propagate(self, cons):
        m = self.model
        d, tx, tw = self._vars(cons)
        l, u = max(tx.getLbLocal(), d.f.lo), min(tx.getUbLocal(), d.f.hi)
        wl, wu = tw.getLbLocal(), tw.getUbLocal()
        key = (l, u, wl, wu)
        if d.last == key:
            return SCIP_RESULT.DIDNOTFIND
        d.last = key
        if l > u:
            return SCIP_RESULT.CUTOFF
        glo, ghi = d.f.range(l, u)
        if glo > wu + 1e-9 * max(1, abs(wu)) or ghi < wl - 1e-9 * max(1, abs(wl)):
            return SCIP_RESULT.CUTOFF
        reduced = False
        for bound, tighten in ((glo, m.tightenVarLb), (ghi, m.tightenVarUb)):
            infeas, tightened = tighten(tw, bound)
            if infeas:
                return SCIP_RESULT.CUTOFF
            reduced |= tightened

        def disjoint(a, b):
            lo, hi = d.f.range(a, b)
            return lo > wu + 1e-9 * max(1, abs(wu)) or hi < wl - 1e-9 * max(1, abs(wl))

        # Trim x from the left and from the right while g cannot reach [wl, wu] there.
        # Nothing can be trimmed when [wl, wu] already contains the range of g.
        if u - l > 1e-9 and (wl > glo or wu < ghi):
            for side in (0, 1):
                keep, drop = (u, l) if side == 0 else (l, u)   # [l, t] or [t, u] is tested
                t_ok, t_bad = drop, keep
                for _ in range(14):
                    t = 0.5 * (t_ok + t_bad)
                    if disjoint(*((l, t) if side == 0 else (t, u))):
                        t_ok = t
                    else:
                        t_bad = t
                if abs(t_ok - drop) > 1e-6 * (u - l):
                    infeas, tightened = (m.tightenVarLb if side == 0 else m.tightenVarUb)(tx, t_ok)
                    if infeas:
                        return SCIP_RESULT.CUTOFF
                    reduced |= tightened
                    l, u = (t_ok, u) if side == 0 else (l, t_ok)
        self.nprop += reduced
        return SCIP_RESULT.REDUCEDDOM if reduced else SCIP_RESULT.DIDNOTFIND

    def _initial_cuts(self, cons):
        """Envelope cuts at both ends and the middle of the global interval."""
        m = self.model
        d, tx, tw = self._vars(cons)
        l, u = max(tx.getLbGlobal(), d.f.lo), min(tx.getUbGlobal(), d.f.hi)
        if l > u:
            return
        for xv in (l, 0.5 * (l + u), u):
            for side in ("under", "over"):
                a, c = getattr(d.f, side)(l, u, xv)
                lhs, rhs = (c, None) if side == "under" else (None, c)
                row = m.createEmptyRowUnspec(f"uenv0_{cons.name}_{side}_{self.ncuts}", lhs=lhs, rhs=rhs,
                                             local=False, removable=False)
                m.cacheRowExtensions(row)
                m.addVarToRow(row, tw, 1.0)
                m.addVarToRow(row, tx, -a)
                m.flushRowExtensions(row)
                m.addCut(row, forcecut=True)
                m.releaseRow(row)
                self.ncuts += 1

    # ------------------------------------------------------------ callbacks
    def consinitlp(self, constraints):
        for cons in constraints:
            self._initial_cuts(cons)
        return {"infeasible": False}

    def conslock(self, constraint, locktype, nlockspos, nlocksneg):
        d = constraint.data
        for v in (d.x, d.w):
            self.model.addVarLocks(v, nlockspos + nlocksneg, nlockspos + nlocksneg)

    def conscheck(self, constraints, solution, checkintegrality, checklprows, printreason, completely):
        if self.hybrid:
            return {"result": SCIP_RESULT.FEASIBLE}
        tol = self.model.feastol()
        ok = all(self._violation(c, solution)[0] <= tol for c in constraints)
        return {"result": SCIP_RESULT.FEASIBLE if ok else SCIP_RESULT.INFEASIBLE}

    def consenfolp(self, constraints, nusefulconss, solinfeasible):
        return self._enforce(constraints, None, allow_cuts=True)

    def consenfops(self, constraints, nusefulconss, solinfeasible, objinfeasible):
        return self._enforce(constraints, None, allow_cuts=False)

    def conssepalp(self, constraints, nusefulconss):
        separated = False
        for cons in constraints:
            added, cutoff = self._cut(cons, None, 1e-4)
            if cutoff:
                return {"result": SCIP_RESULT.CUTOFF}
            separated |= added
        return {"result": SCIP_RESULT.SEPARATED if separated else SCIP_RESULT.DIDNOTFIND}

    def consprop(self, constraints, nusefulconss, nmarkedconss, proptiming):
        result = SCIP_RESULT.DIDNOTFIND
        for cons in constraints:
            r = self._propagate(cons)
            if r == SCIP_RESULT.CUTOFF:
                return {"result": r}
            if r == SCIP_RESULT.REDUCEDDOM:
                result = r
        return {"result": result}


def install(model, hybrid: bool = False) -> UnivariateHdlr:
    hdlr = UnivariateHdlr(hybrid)
    model.includeConshdlr(hdlr, "univariate", "w == g(x) with exact univariate envelopes",
                          sepapriority=20, enfopriority=60, chckpriority=-4000020, sepafreq=1,
                          propfreq=1, eagerfreq=100, maxprerounds=0, delaysepa=False,
                          delayprop=False, needscons=True,
                          presoltiming=SCIP_PRESOLTIMING.FAST, proptiming=SCIP_PROPTIMING.BEFORELP)
    return hdlr


def add_univariate(model, hdlr: UnivariateHdlr, w, x, f: Univariate, name: str):
    """Add the constraint  w == f(x).  Bounds of x must lie inside the domain of f."""
    for v in (w, x):
        model.markDoNotAggrVar(v)
        model.markDoNotMultaggrVar(v)
    glo, ghi = f.range(f.lo, f.hi)
    if w.getLbOriginal() < glo:
        model.chgVarLb(w, glo)
    if w.getUbOriginal() > ghi:
        model.chgVarUb(w, ghi)
    cons = model.createCons(hdlr, name, initial=True, separate=True, enforce=True, check=True,
                            propagate=True, local=False, modifiable=False, dynamic=False,
                            removable=False, stickingatnode=False)
    cons.data = SimpleNamespace(x=x, w=w, f=f, tx=None, tw=None, last=None, node=-1, node_cuts=0)
    model.addPyCons(cons)
    return cons
