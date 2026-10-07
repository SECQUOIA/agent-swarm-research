"""Floating-point cross-check of the model reading (evidence, not proof).

SCIP's own OSiL reader (pyscipopt 6.2.1 / SCIP 10) loads each model; the
points that osilq.py declares exactly feasible are rounded to double and
checked by SCIP with feasibility tolerance 1e-9. SCIP moves a nonlinear
objective part into a variable nlobjvar with a row nlobjvar >= g(x); the
script finds the smallest nlobjvar value SCIP accepts (bisection) and
reports SCIP's objective at that value, to compare with the exact objective
from osilq.py. Negative controls perturb one variable and must fail.
"""
import os
from fractions import Fraction as Q

import pyscipopt

import osilq

HERE = os.path.dirname(os.path.abspath(__file__))
OSIL = os.path.expanduser('~/.cache/minlplib/minlplib/osil/')
SOL = os.path.join(HERE, '..', '..', 'bound-audit', 'sol')
LOG = os.path.join(HERE, 'logs')


def read_pairs(path):
    d = {}
    for line in open(path):
        p = line.split()
        if p:
            d[p[0]] = Q(p[1])
    return d


class Scip:
    def __init__(self, name):
        self.m = pyscipopt.Model()
        self.m.hideOutput()
        self.m.readProblem(OSIL + name + '.osil')
        self.m.setParam('numerics/feastol', 1e-9)
        self.vars = self.m.getVars()
        self.has_objvar = any(v.name == 'nlobjvar' for v in self.vars)

    def check(self, vals, t, perturb=None):
        s = self.m.createSol()
        for v in self.vars:
            if v.name == 'nlobjvar':
                self.m.setSolVal(s, v, t)
                continue
            val = vals.get(v.name, Q(0))
            if perturb and v.name == perturb[0]:
                val += perturb[1]
            self.m.setSolVal(s, v, float(val))
        ok = self.m.checkSol(s, printreason=False, completely=True, checkbounds=True,
                             checkintegrality=True, checklprows=True, original=True)
        return ok, self.m.getSolObjVal(s, original=True)

    def evaluate(self, vals, perturb=None):
        """Feasibility (with nlobjvar large) and SCIP's objective."""
        if not self.has_objvar:
            return self.check(vals, 0.0, perturb)
        big = 1e12
        ok, _ = self.check(vals, big, perturb)
        if not ok:
            return False, None
        lo, hi = -big, big            # smallest accepted nlobjvar value
        for _ in range(200):
            mid = (lo + hi) / 2
            if mid in (lo, hi):
                break
            if self.check(vals, mid, perturb)[0]:
                hi = mid
            else:
                lo = mid
        return True, self.check(vals, hi, perturb)[1]


CASES = [
    ('lop97icx', os.path.join(SOL, 'lop97icx.p2.sol'), ('x1', Q(1, 10 ** 6))),
    ('stockcycle', os.path.join(SOL, 'stockcycle.p2.sol'), ('x1', Q(-1, 10 ** 6))),
    ('eniplac', os.path.join(LOG, 'eniplac.p2.exact.sol'), ('x73', Q(1, 1000))),
    ('eniplac', os.path.join(LOG, 'eniplac.p2.centre.exact.sol'), None),
    ('spring', os.path.join(LOG, 'spring.p3.exact.sol'), ('x3', Q(-1, 10 ** 6))),
]

for name, path, neg in CASES:
    model = osilq.Model(OSIL + name + '.osil')
    vals = read_pairs(path)
    x = [vals.get(nm, Q(0)) for nm in model.names]
    bad, f = osilq.check_exact(model, x)
    sc = Scip(name)
    ok, fs = sc.evaluate(vals)
    print('%-10s %-28s exact: %s, obj %.15g | SCIP feastol 1e-9: %s, obj %.15g, '
          'rel. diff %.1e' % (
              name, os.path.basename(path), 'feasible' if not bad else 'VIOLATED',
              float(f), 'feasible' if ok else 'INFEASIBLE', fs,
              abs(fs - float(f)) / max(1, abs(float(f)))))
    if neg:
        xp = list(x)
        xp[model.index[neg[0]]] += neg[1]
        badp, _ = osilq.check_exact(model, xp)
        okp, _ = sc.evaluate(vals, perturb=neg)
        print('%-10s   negative control %s %+g: exact %d violations (%s); SCIP %s' % (
            name, neg[0], float(neg[1]), len(badp),
            ', '.join('%s %s' % (b[0], b[1]) for b in badp[:3]),
            'feasible' if okp else 'infeasible'))
