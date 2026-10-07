"""Does SCIP's sepa_interminor generate exactly the intersection cut of C_U (U = polar rotation of
the minor's LP value)?  Targeted check with the SCIP 10.0.3 bundled in PySCIPOpt 6.2.1 (built with
Ipopt, which sepa_interminor requires; the local binary has IPOPT=OFF and never runs it).

Model: random bipartite bilinear program, x in [lx, ux]^p, y in [ly, uy]^q, two nonconvex quadratic
constraints containing every product x_i y_k, linear objective.  Separators other than interminor
are switched off; interminor runs at the root (freq 0).  A Python separator with priority +1 runs
before interminor in each round and records the LP (basis, tableau rows of the minor variables).
From that record we predict the cut of every violated minor:
    sum_j (1/alpha_j) lambda_j >= 1,  alpha_j = step length of C_U along ray j,
assembled in the original variables exactly as addColToCut()/addRowToCut() do.  Cuts that SCIP
applied in that round (LP rows with empty name and origin SEPA that appear in the next round) are
matched with the predictions after normalization.
Usage: python3 scip_fidelity.py SEED NINST [p q]
"""
import sys
import json
import numpy as np
import pyscipopt as ps
from pyscipopt import SCIP_RESULT, SCIP_PARAMSETTING
from minor_core import mat, step, polar_rotation, scip_interminor_step

FEASTOL = 1e-6


def build(rng, p, q):
    m = ps.Model()
    m.hideOutput()
    x = [m.addVar('x%d' % i, lb=rng.uniform(-2, 0), ub=rng.uniform(0.5, 2)) for i in range(p)]
    y = [m.addVar('y%d' % k, lb=rng.uniform(-2, 0), ub=rng.uniform(0.5, 2)) for k in range(q)]
    for side in (1, -1):
        E = rng.normal(size=(p, q))
        expr = ps.quicksum(E[i, k] * x[i] * y[k] for i in range(p) for k in range(q)) \
            + ps.quicksum(rng.normal() * v for v in x + y)
        if side == 1:
            m.addCons(expr <= rng.uniform(0, 1))
        else:
            m.addCons(expr >= -rng.uniform(0, 1))
    m.setObjective(ps.quicksum(rng.normal() * v for v in x + y))
    return m, x, y


class Recorder(ps.Sepa):
    def __init__(self, p, q):
        self.p, self.q = p, q
        self.records = []
        self.prod = None      # (i, k) -> LP column position of the aux variable of x_i y_k

    def map_products(self, cols, rows):
        name_of = {c.getLPPos(): c.getVar().name for c in cols}
        pos_of = {v: k for k, v in name_of.items()}
        prod = {}
        for r in rows:
            cs = r.getCols()
            if len(cs) != 3:
                continue
            names = [c.getVar().name for c in cs]
            xs = [n for n in names if n.startswith('t_x')]
            ys = [n for n in names if n.startswith('t_y')]
            aux = [n for n in names if n.startswith('auxvar_prod')]
            if len(xs) == 1 and len(ys) == 1 and len(aux) == 1:
                prod[(int(xs[0][3:]), int(ys[0][3:]))] = pos_of[aux[0]]
        return prod

    def sepaexeclp(self):
        m = self.model
        if m.getLPSolstat() != 1:      # optimal
            return {'result': SCIP_RESULT.DIDNOTRUN}
        cols = m.getLPColsData()
        rows = m.getLPRowsData()
        if self.prod is None:
            self.prod = self.map_products(cols, rows)
        ncols, nrows = len(cols), len(rows)
        xbar = np.array([c.getPrimsol() for c in cols])
        cstat = [c.getBasisStatus() for c in cols]
        rstat = [r.getBasisStatus() for r in rows]
        lb = np.array([c.getLb() for c in cols])
        ub = np.array([c.getUb() for c in cols])
        basisind = m.getLPBasisInd()
        brow = {b: i for i, b in enumerate(basisind) if b >= 0}
        need = sorted(set(self.prod.values()))
        tab = {}
        for c in need:
            if cstat[c] == 'basic':
                i = brow[c]
                tab[c] = (np.array(m.getLPBInvARow(i)), np.array(m.getLPBInvRow(i)))
        rowdata = []
        for r in rows:
            rc = r.getCols()
            rowdata.append(dict(cols=[c.getLPPos() for c in rc], vals=list(r.getVals()), lhs=r.getLhs(),
                                rhs=r.getRhs(), const=r.getConstant(), name=r.name, origin=r.getOrigintype(),
                                act=m.getRowLPActivity(r)))
        inter = [k for k, rd in enumerate(rowdata) if rd['name'] == '' and rd['origin'] == 3]
        self.records.append(dict(xbar=xbar, cstat=cstat, rstat=rstat, lb=lb, ub=ub, tab=tab, rows=rowdata,
                                 inter_rows=[self.row_key(rowdata[k]) for k in inter], ncols=ncols, nrows=nrows,
                                 inter_full=[rowdata[k] for k in inter]))
        return {'result': SCIP_RESULT.DIDNOTFIND}

    @staticmethod
    def row_key(rd):
        return (tuple(rd['cols']), tuple(np.round(rd['vals'], 12)), rd['lhs'], rd['rhs'])


def predict_cuts(rec, prod, p, q, use_scip_formula=False):
    """Predicted interminor cuts (pi over LP columns, pi0): pi^T x >= pi0, normalized later."""
    xbar, cstat, rstat, tab, rows = rec['xbar'], rec['cstat'], rec['rstat'], rec['tab'], rec['rows']
    ncols, nrows = rec['ncols'], rec['nrows']
    out = []
    for i1 in range(p):
        for i2 in range(i1 + 1, p):
            for k1 in range(q):
                for k2 in range(k1 + 1, q):
                    vars4 = [prod[(i1, k1)], prod[(i1, k2)], prod[(i2, k1)], prod[(i2, k2)]]   # a, b, c, d
                    sb = xbar[vars4]
                    dt = sb[0] * sb[3] - sb[1] * sb[2]
                    if abs(dt) <= FEASTOL:
                        continue
                    if dt < 0:      # SCIP swaps the columns: (a, b, c, d) -> (b, a, d, c)
                        vars4 = [vars4[1], vars4[0], vars4[3], vars4[2]]
                        sb = xbar[vars4]
                    UT = polar_rotation(mat(sb)).T
                    pi = np.zeros(ncols)
                    pi0 = 1.0
                    ok = True
                    # nonbasic columns
                    for j in range(ncols):
                        if cstat[j] == 'basic':
                            continue
                        if cstat[j] == 'zero':
                            ok = False
                            break
                        factor = -1.0 if cstat[j] == 'lower' else 1.0
                        ray = np.zeros(4)
                        for v, cv in enumerate(vars4):
                            if cv in tab:
                                t = tab[cv][0][j]
                                ray[v] = factor * (0.0 if abs(t) <= 1e-9 else t)
                            else:
                                ray[v] = -factor if cv == j else 0.0
                        if not ray.any():
                            continue
                        al = scip_interminor_step(sb, ray) if use_scip_formula else step(UT, sb, ray)
                        a = 0.0 if not np.isfinite(al) else 1.0 / al
                        s = a if cstat[j] == 'lower' else -a
                        pi[j] += s
                        pi0 += s * xbar[j]
                    if not ok:
                        continue
                    # nonbasic rows (slacks)
                    for r in range(nrows):
                        if rstat[r] == 'basic':
                            continue
                        factor = 1.0 if rstat[r] == 'lower' else -1.0
                        ray = np.zeros(4)
                        for v, cv in enumerate(vars4):
                            if cv in tab:
                                t = tab[cv][1][r]
                                ray[v] = factor * (0.0 if abs(t) <= 1e-9 else t)
                        if not ray.any():
                            continue
                        al = scip_interminor_step(sb, ray) if use_scip_formula else step(UT, sb, ray)
                        a = 0.0 if not np.isfinite(al) else 1.0 / al
                        rd = rows[r]
                        cc = a if rstat[r] == 'upper' else -a      # sign used by addRowToCut
                        side = rd['rhs'] if rstat[r] == 'upper' else rd['lhs']
                        # adds cc * (side - a^T x - const)
                        pi0 -= cc * (side - rd['const'])
                        for cpos, val in zip(rd['cols'], rd['vals']):
                            pi[cpos] -= cc * val
                    out.append(dict(minor=(i1, i2, k1, k2), pi=pi, pi0=pi0))
    return out


def normalize(pi, pi0):
    n = np.linalg.norm(pi)
    return pi / n, pi0 / n


if __name__ == '__main__':
    seed, ninst = int(sys.argv[1]), int(sys.argv[2])
    p = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    q = int(sys.argv[4]) if len(sys.argv) > 4 else 3
    rng = np.random.default_rng(seed)
    tot = dict(rounds=0, applied=0, matched=0, worst_coef=0.0, worst_rhs=0.0, predicted=0)
    for inst in range(ninst):
        m, x, y = build(rng, p, q)
        m.setSeparating(SCIP_PARAMSETTING.OFF)
        m.setParam('separating/interminor/freq', 0)
        m.setParam('separating/interminor/maxroundsroot', 5)
        m.setParam('limits/nodes', 1)
        m.setPresolve(SCIP_PARAMSETTING.OFF)
        m.setHeuristics(SCIP_PARAMSETTING.OFF)
        rec = Recorder(p, q)
        m.includeSepa(rec, 'recorder', 'records LP before interminor', priority=1, freq=0, maxbounddist=1.0,
                      usessubscip=False, delay=False)
        m.optimize()
        R = rec.records
        if rec.prod is None or len(rec.prod) < p * q:
            print(json.dumps(dict(inst=inst, skipped='product map incomplete', nprod=0 if rec.prod is None else len(rec.prod))))
            continue
        for r in range(len(R) - 1):
            before = set(R[r]['inter_rows'])
            new = [rd for rd in R[r + 1]['inter_full'] if Recorder.row_key(rd) not in before]
            preds = predict_cuts(R[r], rec.prod, p, q)
            tot['rounds'] += 1
            tot['predicted'] += len(preds)
            for rd in new:
                ncols = R[r]['ncols']
                pi = np.zeros(ncols)
                for cpos, val in zip(rd['cols'], rd['vals']):
                    pi[cpos] += val
                pi0 = rd['lhs'] - rd['const']
                piS, pi0S = normalize(pi, pi0)
                best = None
                for pr in preds:
                    a, b = normalize(pr['pi'], pr['pi0'])
                    dc = np.abs(a - piS).max()
                    dr = abs(b - pi0S)
                    if best is None or dc + dr < best[0] + best[1]:
                        best = (dc, dr, pr['minor'])
                tot['applied'] += 1
                if best is not None and best[0] < 1e-6 and best[1] < 1e-6:
                    tot['matched'] += 1
                if best is not None:
                    tot['worst_coef'] = max(tot['worst_coef'], best[0])
                    tot['worst_rhs'] = max(tot['worst_rhs'], best[1])
                print(json.dumps(dict(inst=inst, round=r, minor=best[2] if best else None,
                                      coef_diff=best[0] if best else None, rhs_diff=best[1] if best else None)),
                      flush=True)
    print('SUMMARY', json.dumps(tot))
