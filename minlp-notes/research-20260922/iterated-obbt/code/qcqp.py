"""QCQP data model for MINLPLib OSiL instances: parser, evaluation, FBBT, solver models.

All objectives are stored in minimization form: f_min(x) = sense * f(x), sense = +1 (min) or -1 (max).
Only instances whose nonlinear parts are given as OSiL <quadraticCoefficients> are supported.
"""
import os, math, re
import xml.etree.ElementTree as ET
from collections import defaultdict
import numpy as np
import scipy.sparse as sp

OSIL = os.path.expanduser('~/.cache/minlplib/minlplib/osil')
SOLDIR = os.path.expanduser('~/.cache/minlplib/sol')
INF = math.inf


def _num(s, default):
    if s is None:
        return default
    s = s.strip()
    if s in ('INF', 'Infinity', 'inf'):
        return INF
    if s in ('-INF', '-Infinity', '-inf'):
        return -INF
    return float(s)


def _els(node, cast=float):
    out = []
    for el in node:
        v = cast(el.text)
        mult = int(el.get('mult', 1))
        incr = cast(el.get('incr', 0))
        out.extend(v + k * incr for k in range(mult))
    return out


class QCQP:
    def __init__(self, name):
        self.name = name
        root = ET.parse(os.path.join(OSIL, name + '.osil')).getroot()
        ns = {'o': root.tag[1:].split('}')[0]} if root.tag.startswith('{') else None
        strip = lambda t: t.split('}')[-1]
        data = next(c for c in root if strip(c.tag) == 'instanceData')
        sec = {strip(c.tag): c for c in data}
        if 'nonlinearExpressions' in sec:
            raise ValueError('general nonlinear expressions not supported')
        vs = list(sec['variables'])
        n = len(vs)
        self.n = n
        self.names = [v.get('name') for v in vs]
        self.vtype = np.array([v.get('type', 'C') for v in vs])
        self.lb = np.array([_num(v.get('lb'), 0.0) for v in vs])
        self.ub = np.array([_num(v.get('ub'), INF) for v in vs])
        isb = self.vtype == 'B'
        self.lb[isb] = np.maximum(self.lb[isb], 0.0)
        self.ub[isb] = np.minimum(self.ub[isb], 1.0)
        self.isint = np.isin(self.vtype, ['B', 'I'])
        # objective
        objs = list(sec['objectives']) if 'objectives' in sec else []
        self.c = np.zeros(n)
        self.c0 = 0.0
        self.sense = 1
        if objs:
            o = objs[0]
            self.sense = -1 if o.get('maxOrMin', 'min') == 'max' else 1
            self.c0 = float(o.get('constant', 0.0))
            for cf in o:
                self.c[int(cf.get('idx'))] += float(cf.text)
        # constraints
        cons = list(sec['constraints']) if 'constraints' in sec else []
        m = len(cons)
        self.m = m
        self.rlo = np.array([_num(c.get('lb'), -INF) for c in cons])
        self.rhi = np.array([_num(c.get('ub'), INF) for c in cons])
        const = np.array([float(c.get('constant', 0.0)) for c in cons])
        self.rlo -= const
        self.rhi -= const
        if 'linearConstraintCoefficients' in sec:
            L = {strip(c.tag): c for c in sec['linearConstraintCoefficients']}
            start = _els(L['start'], int)
            val = _els(L['value'], float)
            if 'colIdx' in L:
                idx = _els(L['colIdx'], int)
                A = sp.csr_matrix((val, idx, start), shape=(m, n))
            else:
                idx = _els(L['rowIdx'], int)
                A = sp.csc_matrix((val, idx, start), shape=(m, n)).tocsr()
        else:
            A = sp.csr_matrix((m, n))
        A.sum_duplicates()
        self.A = A
        # quadratic terms, normalized i <= j and merged
        oq = defaultdict(float)
        rq = defaultdict(lambda: defaultdict(float))
        if 'quadraticCoefficients' in sec:
            for q in sec['quadraticCoefficients']:
                r, i, j, v = int(q.get('idx')), int(q.get('idxOne')), int(q.get('idxTwo')), float(q.get('coef'))
                if i > j:
                    i, j = j, i
                if r == -1:
                    oq[(i, j)] += v
                else:
                    rq[r][(i, j)] += v
        self.oq = {k: v for k, v in oq.items() if v != 0}
        self.rq = {r: {k: v for k, v in d.items() if v != 0} for r, d in rq.items()}
        self.rq = {r: d for r, d in self.rq.items() if d}
        # nonlinear variables and terms
        terms = set(self.oq)
        for d in self.rq.values():
            terms |= set(d)
        self.terms = sorted(terms)
        self.nlvars = sorted({i for t in terms for i in t})

    # ---- minimization-form objective ----
    def fmin(self, x):
        v = self.c0 + self.c @ x + sum(q * x[i] * x[j] for (i, j), q in self.oq.items())
        return self.sense * v

    def rows(self, x):
        g = self.A @ x
        for r, d in self.rq.items():
            g[r] += sum(q * x[i] * x[j] for (i, j), q in d.items())
        return g

    def violation(self, x):
        """Max absolute violation of rows, bounds and integrality."""
        g = self.rows(x)
        v = 0.0
        if self.m:
            v = max(np.max(np.maximum(self.rlo - g, 0)), np.max(np.maximum(g - self.rhi, 0)))
        v = max(v, np.max(np.maximum(self.lb - x, 0)), np.max(np.maximum(x - self.ub, 0)))
        if self.isint.any():
            xi = x[self.isint]
            v = max(v, np.max(np.abs(xi - np.round(xi))))
        return float(v)

    # ---- known solution ----
    def load_sol(self, fstar=None):
        """Known solution from MINLPLib .pK.sol files: the one whose minimization-form objective is
        closest to fstar (if given), else p1."""
        pos = {nm: k for k, nm in enumerate(self.names)}
        best = None
        for k in range(1, 10):
            path = os.path.join(SOLDIR, '%s.p%d.sol' % (self.name, k))
            if not os.path.exists(path):
                break
            x = np.zeros(self.n)
            for line in open(path):
                p = line.split()
                if len(p) >= 2 and p[0] in pos:
                    x[pos[p[0]]] = float(p[1])
            if fstar is None:
                return x
            err = abs(self.fmin(x) - fstar)
            if best is None or err < best[0]:
                best = (err, x)
        return None if best is None else best[1]

    # ---- FBBT (term-wise interval propagation) ----
    def fbbt(self, lb=None, ub=None, passes=50, rtol=1e-4):
        lb = self.lb.copy() if lb is None else lb.copy()
        ub = self.ub.copy() if ub is None else ub.copy()
        A = self.A
        rowterms = []
        for r in range(self.m):
            ts = [('l', int(k), -1, float(a)) for k, a in zip(A.indices[A.indptr[r]:A.indptr[r + 1]],
                                                            A.data[A.indptr[r]:A.indptr[r + 1]]) if a != 0]
            ts += [('q', i, j, q) for (i, j), q in self.rq.get(r, {}).items()]
            rowterms.append(ts)
        for _ in range(passes):
            changed = False
            for r, ts in enumerate(rowterms):
                if not ts or (self.rlo[r] == -INF and self.rhi[r] == INF):
                    continue
                ivs = [_term_iv(t, lb, ub) for t in ts]
                lo_fin = sum(a for a, b in ivs if a > -INF)
                lo_inf = sum(1 for a, b in ivs if a == -INF)
                hi_fin = sum(b for a, b in ivs if b < INF)
                hi_inf = sum(1 for a, b in ivs if b == INF)
                if lo_inf == 0 and hi_inf == 0 and (lo_fin > self.rhi[r] + 1e-6 * (1 + abs(lo_fin)) or
                                                    hi_fin < self.rlo[r] - 1e-6 * (1 + abs(hi_fin))):
                    raise RuntimeError('FBBT: infeasible row %d' % r)
                for t, (a, b) in zip(ts, ivs):
                    # others' interval
                    olo = -INF if lo_inf - (a == -INF) > 0 else lo_fin - (a if a > -INF else 0)
                    ohi = INF if hi_inf - (b == INF) > 0 else hi_fin - (b if b < INF else 0)
                    tlo = self.rlo[r] - ohi if self.rlo[r] > -INF and ohi < INF else -INF
                    thi = self.rhi[r] - olo if self.rhi[r] < INF and olo > -INF else INF
                    if tlo == -INF and thi == INF:
                        continue
                    for k, nl, nu in _term_back(t, tlo, thi, lb, ub):
                        if self.isint[k]:
                            nl = math.ceil(nl - 1e-6) if nl > -INF else nl
                            nu = math.floor(nu + 1e-6) if nu < INF else nu
                        # relax slightly to protect against rounding
                        if nl > -INF:
                            nl -= 1e-9 * (1 + abs(nl)) if not self.isint[k] else 0
                        if nu < INF:
                            nu += 1e-9 * (1 + abs(nu)) if not self.isint[k] else 0
                        if nl < -1e12:
                            nl = -INF
                        if nu > 1e12:
                            nu = INF
                        w = ub[k] - lb[k]
                        thr = rtol * (w if w < INF else 1.0) + 1e-9
                        if nl > -INF and (lb[k] == -INF or nl > lb[k] + thr):
                            lb[k] = nl
                            changed = True
                        if nu < INF and (ub[k] == INF or nu < ub[k] - thr):
                            ub[k] = nu
                            changed = True
                        if lb[k] > ub[k]:
                            if lb[k] > ub[k] + 1e-6 * (1 + abs(ub[k])):
                                raise RuntimeError('FBBT: empty domain for %s' % self.names[k])
                            lb[k] = ub[k] = 0.5 * (lb[k] + ub[k])
            if not changed:
                break
        return lb, ub

    # ---- solver models ----
    def gurobi_model(self, env, lb=None, ub=None):
        import gurobipy as gp
        from gurobipy import GRB
        lb = self.lb if lb is None else lb
        ub = self.ub if ub is None else ub
        m = gp.Model(self.name, env=env)
        vt = [GRB.BINARY if t == 'B' else GRB.INTEGER if t == 'I' else GRB.CONTINUOUS for t in self.vtype]
        x = m.addMVar(self.n, lb=_g(lb), ub=_g(ub), vtype=vt)
        xs = x.tolist()
        for k, v in enumerate(xs):
            v.VarName = self.names[k]
        obj = gp.QuadExpr()
        obj.addTerms(self.c.tolist(), xs)
        for (i, j), q in self.oq.items():
            obj.addTerms(q, xs[i], xs[j])
        obj.addConstant(self.c0)
        m.setObjective(obj, GRB.MINIMIZE if self.sense == 1 else GRB.MAXIMIZE)
        A = self.A
        for r in range(self.m):
            e = gp.QuadExpr()
            s, t = A.indptr[r], A.indptr[r + 1]
            e.addTerms(A.data[s:t].tolist(), [xs[k] for k in A.indices[s:t]])
            for (i, j), q in self.rq.get(r, {}).items():
                e.addTerms(q, xs[i], xs[j])
            lo, hi = self.rlo[r], self.rhi[r]
            if lo == hi:
                m.addConstr(e == lo)
            else:
                if lo > -INF:
                    m.addConstr(e >= lo)
                if hi < INF:
                    m.addConstr(e <= hi)
        m.update()
        return m, xs


def _g(a):
    return np.where(np.isinf(a), np.sign(a) * 1e100, a)


def imul(al, au, bl, bu):
    ps = []
    for p in (al, au):
        for q in (bl, bu):
            if p == 0 or q == 0:
                ps.append(0.0)
            else:
                ps.append(p * q)
    return min(ps), max(ps)


def _term_iv(t, lb, ub):
    kind, i, j, a = t
    if kind == 'l':
        lo, hi = a * lb[i], a * ub[i]
        if a < 0:
            lo, hi = hi, lo
        return lo, hi
    if i == j:
        l, u = lb[i], ub[i]
        slo = 0.0 if l <= 0 <= u else min(l * l, u * u)
        shi = max(l * l, u * u)
        lo, hi = a * slo, a * shi
    else:
        lo, hi = imul(lb[i], ub[i], lb[j], ub[j])
        lo, hi = a * lo, a * hi
    if a < 0:
        lo, hi = hi, lo
    return lo, hi


def _term_back(t, tlo, thi, lb, ub):
    """Implied bounds on variables of term t whose value lies in [tlo, thi]."""
    kind, i, j, a = t
    lo, hi = (tlo / a, thi / a) if a > 0 else (thi / a, tlo / a)
    if kind == 'l':
        return [(i, lo, hi)]
    if i == j:  # x^2 in [lo, hi]
        out = []
        if hi < INF:
            if hi < 0:
                raise RuntimeError('FBBT: square below zero')
            r = math.sqrt(hi)
            nl, nu = -r, r
        else:
            nl, nu = -INF, INF
        if lo > 0:
            r = math.sqrt(lo)
            if lb[i] > -r:
                nl = max(nl, r)
            if ub[i] < r:
                nu = min(nu, -r)
        return [(i, nl, nu)]
    out = []
    for p, q in ((i, j), (j, i)):
        ql, qu = lb[q], ub[q]
        if ql > 0 or qu < 0:
            # p in [lo, hi] / [ql, qu]
            cands = []
            ok = True
            for num in (lo, hi):
                for den in (ql, qu):
                    if math.isinf(den) and math.isinf(num):
                        ok = False
                    elif math.isinf(den):
                        cands.append(0.0)
                    else:
                        cands.append(num / den)
            if ok:
                out.append((p, min(cands), max(cands)))
    return out


def fetch_sol(name):
    """Download all MINLPLib solution files <name>.pK.sol (K = 1, 2, ...)."""
    import urllib.request, urllib.error
    os.makedirs(SOLDIR, exist_ok=True)
    if os.path.exists(os.path.join(SOLDIR, name + '.done')):
        return
    got = []
    for k in range(1, 10):
        path = os.path.join(SOLDIR, '%s.p%d.sol' % (name, k))
        if not os.path.exists(path):
            try:
                with urllib.request.urlopen('https://www.minlplib.org/sol/%s.p%d.sol' % (name, k),
                                            timeout=30) as r:
                    data = r.read()
            except urllib.error.HTTPError:
                break
            except Exception:       # network failure: leave unmarked, retry another time
                return got
            if not data.strip():
                break
            open(path, 'wb').write(data)
        got.append(path)
    open(os.path.join(SOLDIR, name + '.done'), 'w').close()
    return got
