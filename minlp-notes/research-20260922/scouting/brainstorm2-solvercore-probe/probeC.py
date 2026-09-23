"""Probe C: box-parametric Lagrangian bounds for McCormick LPs of QCQPs.

For a QCQP, build the lifted McCormick LP (w_ij = x_i x_j; secant plus three tangents for squares)
on a box B. Solve it at the root and keep the row duals y of the bound-dependent rows (McCormick rows)
and of the bound-independent rows (original linear rows in lifted space). For a sub-box B' the value

    Phi_y(B') = sum_r y_r b_r(B') + sum_k min_{z_k in box_k(B')} (c - A(B')^T y)_k z_k

is a valid lower bound on the McCormick LP over B' (weak duality; box_k for w are interval products).
We compare, for each candidate branching (variable i in a violated product, point p = SCIP-like
clamped LP value), the children's true LP bounds with:
  phi_aware : Phi_y with rows rebuilt for the child box,
  phi_fixed : same y, rows of the parent kept, only the child box changed (classical reduced-cost view).
We also compare the resulting strong-branching choices (product score).
"""
import sys, os, math, json, itertools
import numpy as np
import gurobipy as gp
from gurobipy import GRB
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'minlplib-open-data'))
from osil import read

OSIL = os.path.expanduser('~/.cache/minlplib/minlplib/osil')


# ---------- polynomial expansion of OSiL trees (degree <= 2) ----------
def poly(t):
    """Return dict: () -> const, (i,) -> coef, (i,j) i<=j -> coef. Raise if degree > 2 or not polynomial."""
    op = t[0]
    if op == 'num':
        return {(): t[1]}
    if op == 'var':
        return {(t[1],): 1.0}
    if op == 'sum':
        out = {}
        for c in t[1:]:
            for k, v in poly(c).items():
                out[k] = out.get(k, 0.0) + v
        return out
    if op == 'negate':
        return {k: -v for k, v in poly(t[1]).items()}
    if op == 'times':
        out = {(): 1.0}
        for c in t[1:]:
            pc = poly(c); new = {}
            for k1, v1 in out.items():
                for k2, v2 in pc.items():
                    k = tuple(sorted(k1 + k2))
                    if len(k) > 2:
                        raise ValueError('deg>2')
                    new[k] = new.get(k, 0.0) + v1 * v2
            out = new
        return out
    if op == 'square':
        return poly(('times', t[1], t[1]))
    if op == 'power' and t[2][0] == 'num' and t[2][1] == 2.0:
        return poly(('times', t[1], t[1]))
    if op == 'divide' and t[2][0] == 'num':
        return {k: v / t[2][1] for k, v in poly(t[1]).items()}
    raise ValueError('op ' + op)


def qcqp(name):
    I = read(os.path.join(OSIL, name + '.osil'))
    rows = []
    for r, R in I['rows'].items():
        p = {}
        for j, a in R['lin'].items():
            p[(j,)] = p.get((j,), 0.0) + a
        for i, j, a in R['quad']:
            k = tuple(sorted((i, j)))
            p[k] = p.get(k, 0.0) + a
        if R['nl'] is not None:
            for k, v in poly(R['nl']).items():
                p[k] = p.get(k, 0.0) + v
        rows.append((r, p, R['lb'], R['ub']))
    return I, rows


# ---------- McCormick LP ----------
class McCormick:
    def __init__(self, I, rows):
        self.I, self.rows = I, rows
        self.n = len(I['lb'])
        self.prods = sorted({k for _, p, _, _ in rows for k in p if len(k) == 2})
        self.pidx = {k: self.n + t for t, k in enumerate(self.prods)}
        self.N = self.n + len(self.prods)
        # objective (minimize)
        obj = [p for r, p, _, _ in rows if r == -1]
        self.c = np.zeros(self.N); self.c0 = 0.0
        sgn = -1.0 if I['sense'] == 'max' else 1.0
        if obj:
            for k, v in obj[0].items():
                if k == ():
                    self.c0 += sgn * v
                else:
                    self.c[k[0] if len(k) == 1 else self.pidx[k]] += sgn * v
        self.sgn = sgn
        # bound-independent rows: lo <= a^T z <= hi  (split into >= rows)
        self.fixed = []  # (dict col->coef, rhs) meaning a^T z >= rhs
        for r, p, lo, hi in rows:
            if r == -1:
                continue
            a = {}
            k0 = p.get((), 0.0)
            for k, v in p.items():
                if k == ():
                    continue
                col = k[0] if len(k) == 1 else self.pidx[k]
                a[col] = a.get(col, 0.0) + v
            if lo is not None and lo > -1e20:
                self.fixed.append((a, lo - k0))
            if hi is not None and hi < 1e20:
                self.fixed.append(({j: -v for j, v in a.items()}, -(hi - k0)))

    def mc_rows(self, L, U):
        """Bound-dependent rows g(z) = a^T z - rhs >= 0 for box (L,U) of original vars.
        Returns list of (dict, rhs). Each row is inclusion-isotone (tightens on sub-boxes)."""
        out = []
        for (i, j) in self.prods:
            w = self.pidx[(i, j)]
            li, ui, lj, uj = L[i], U[i], L[j], U[j]
            if i != j:
                # w >= lj x_i + li x_j - li lj ; w >= uj x_i + ui x_j - ui uj
                out.append(({w: 1.0, i: -lj, j: -li}, -li * lj))
                out.append(({w: 1.0, i: -uj, j: -ui}, -ui * uj))
                # w <= uj x_i + li x_j - li uj ; w <= lj x_i + ui x_j - ui lj
                out.append(({w: -1.0, i: uj, j: li}, li * uj))
                out.append(({w: -1.0, i: lj, j: ui}, ui * lj))
            else:
                # secant: w <= (l+u) x - l u ; tangents at l, u (and midpoint, NOT isotone -> omitted)
                out.append(({w: -1.0, i: li + ui}, li * ui))
                out.append(({w: 1.0, i: -2 * li}, -li * li))
                out.append(({w: 1.0, i: -2 * ui}, -ui * ui))
        return out

    def zbox(self, L, U):
        lo = np.empty(self.N); hi = np.empty(self.N)
        lo[:self.n] = L; hi[:self.n] = U
        for (i, j), w in self.pidx.items():
            if i == j:
                a, b = L[i], U[i]
                lo[w] = 0.0 if a <= 0 <= b else min(a * a, b * b); hi[w] = max(a * a, b * b)
            else:
                cands = [L[i] * L[j], L[i] * U[j], U[i] * L[j], U[i] * U[j]]
                lo[w], hi[w] = min(cands), max(cands)
        return lo, hi

    def solve(self, L, U):
        lo, hi = self.zbox(L, U)
        m = gp.Model(); m.Params.OutputFlag = 0; m.Params.Method = 1; m.Params.Threads = 1
        z = m.addMVar(self.N, lb=lo, ub=hi)
        m.setObjective(self.c @ z + self.c0)
        rowsF = [m.addConstr(gp.quicksum(v * z[k] for k, v in a.items()) >= rhs) for a, rhs in self.fixed]
        mc = self.mc_rows(L, U)
        rowsM = [m.addConstr(gp.quicksum(v * z[k] for k, v in a.items()) >= rhs) for a, rhs in mc]
        m.optimize()
        if m.Status == GRB.INFEASIBLE:
            return math.inf, None, None, None
        if m.Status != GRB.OPTIMAL:
            return None, None, None, None
        yF = np.array([r.Pi for r in rowsF]); yM = np.array([r.Pi for r in rowsM])
        return m.ObjVal, z.X, yF, yM

    def phi(self, yF, yM, L, U, rows_box=None):
        """Lagrangian bound over box (L,U). McCormick rows built from rows_box (default: (L,U))."""
        rb = rows_box or (L, U)
        mc = self.mc_rows(*rb)
        r = self.c.copy(); val = self.c0
        for (a, rhs), y in zip(self.fixed, yF):
            val += y * rhs
            for k, v in a.items():
                r[k] -= y * v
        for (a, rhs), y in zip(mc, yM):
            val += y * rhs
            for k, v in a.items():
                r[k] -= y * v
        lo, hi = self.zbox(L, U)
        with np.errstate(invalid='ignore'):
            t = np.where(np.abs(r) <= 1e-12, 0.0, np.where(r > 0, r * lo, r * hi))
        val += np.sum(t)
        return val


def run(name, bounds=None, maxcand=40):
    I, rows = qcqp(name)
    for t in I['vt']:
        pass
    mc = McCormick(I, rows)
    L = np.array(I['lb'], float); U = np.array(I['ub'], float)
    if bounds:
        for j, nm in enumerate(I['names']):
            if nm in bounds:
                L[j] = max(L[j], bounds[nm][0]); U[j] = min(U[j], bounds[nm][1])
    used = sorted({i for k in mc.prods for i in k})
    if any(not (np.isfinite(L[i]) and np.isfinite(U[i])) for i in used):
        return dict(name=name, skip='unbounded product variable')
    if not mc.prods:
        return dict(name=name, skip='no products')
    if len(mc.prods) > 300 or len(mc.fixed) > 2000:
        return dict(name=name, skip='too large')
    z0, x, yF, yM = mc.solve(L, U)
    if x is None or not np.isfinite(z0):
        return dict(name=name, skip='root LP status')
    # candidates: variables in products with largest violation
    viol = {}
    for (i, j), w in mc.pidx.items():
        v = abs(x[w] - x[i] * x[j])
        for k in (i, j):
            viol[k] = viol.get(k, 0.0) + v
    cand = [k for k, v in sorted(viol.items(), key=lambda t: -t[1]) if v > 1e-6 and U[k] - L[k] > 1e-6][:maxcand]
    recs = []
    for i in cand:
        wdt = U[i] - L[i]
        p = min(max(x[i], L[i] + 0.2 * wdt), U[i] - 0.2 * wdt)
        ch = []
        for side in ('L', 'R'):
            Lc, Uc = L.copy(), U.copy()
            if side == 'L':
                Uc[i] = p
            else:
                Lc[i] = p
            zt = mc.solve(Lc, Uc)[0]
            pa = mc.phi(yF, yM, Lc, Uc)
            pf = mc.phi(yF, yM, Lc, Uc, rows_box=(L, U))
            ch.append((zt, pa, pf))
        recs.append(dict(var=int(i), vt=I['vt'][i], p=float(p), true=[c[0] for c in ch], aware=[c[1] for c in ch], fixed=[c[2] for c in ch]))
    return dict(name=name, z0=z0, phi0=mc.phi(yF, yM, L, U), nprod=len(mc.prods), n=mc.n, recs=recs)


if __name__ == '__main__':
    import pandas as pd
    from multiprocessing import Pool
    names = sys.argv[1:]
    def job(nm):
        try:
            bnds = json.load(open('bounds/%s.json' % nm)) if os.path.exists('bounds/%s.json' % nm) else None
            r = run(nm, bnds, maxcand=10)
        except Exception as e:
            r = dict(name=nm, skip='error ' + str(e)[:100])
        os.makedirs('probeC_out', exist_ok=True)
        json.dump(r, open('probeC_out/%s.json' % nm, 'w'))
        return r
    with Pool(30, maxtasksperchild=1) as p:
        res = p.map(job, names, chunksize=1)
    json.dump(res, open('probeC.json', 'w'))
    for r in res:
        print(r['name'], r.get('skip', 'ok %d cands' % len(r.get('recs', []))))
