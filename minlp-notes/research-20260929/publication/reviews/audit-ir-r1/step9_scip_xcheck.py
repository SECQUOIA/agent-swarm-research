"""Floating-point cross-check of the reviewer's OSIL reading with SCIP's own
OSiL reader (evidence only). For each exactly feasible point found by the
reviewer's code: SCIP must accept the point (feastol 1e-9) with nlobjvar (if
present) set to the exact objective rounded up by 1e-12 relative, and must
reject it with nlobjvar 1e-7 relative below; a perturbed point must be rejected."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import os
from fractions import Fraction as F
import pyscipopt
import rv_osil as R
import step2_eniplac as E   # builds the eniplac points (prints its report)

OS = os.path.expanduser('~/.cache/minlplib/minlplib/osil/')
BA = (_PUBLIC_REPO + '/research-20260929/bound-audit/')


def scip_check(name, m, x, f, perturb=None):
    s = pyscipopt.Model()
    s.hideOutput()
    s.readProblem(OS + name + '.osil')
    s.setParam('numerics/feastol', 1e-9)
    vs = s.getVars()
    pos = {n: j for j, n in enumerate(m.vname)}
    names_ok = all(v.name in pos or v.name == 'nlobjvar' for v in vs)

    def run(t, pert):
        sol = s.createSol()
        for v in vs:
            if v.name == 'nlobjvar':
                s.setSolVal(sol, v, t)
            else:
                val = x[pos[v.name]]
                if pert and v.name == pert[0]:
                    val += pert[1]
                s.setSolVal(sol, v, float(val))
        ok = s.checkSol(sol, printreason=False, completely=True, checkbounds=True,
                        checkintegrality=True, checklprows=True, original=True)
        return ok, s.getSolObjVal(sol, original=True)
    has = any(v.name == 'nlobjvar' for v in vs)
    ff = float(f)
    # nonlinear part of the objective = f - constant - linear part
    g = float(f - m.obj_const - sum(c * x[j] for j, c in m.obj_lin.items()))
    up = g + abs(ff) * 1e-12 if has else 0.0
    ok_up, obj_up = run(up, None)
    ok_dn = run(g - abs(ff) * 1e-7, None)[0] if has else None
    ok_pert = run(up, perturb)[0] if perturb else None
    return dict(vars_match=names_ok, nvars=len(vs), nlobjvar=has, accepted=ok_up, scip_obj=obj_up,
                exact_obj=ff, rel_diff=abs(obj_up - ff) / max(1.0, abs(ff)),
                rejected_below_obj=(ok_dn is False) if has else 'n/a', perturbed_rejected=(ok_pert is False) if perturb else 'n/a')


import step3_spring  # noqa  (prints its report)
cases = []
for name in ('lop97icx', 'stockcycle'):
    m = R.load(name)
    x, _ = R.read_sol(m, BA + 'sol/%s.p2.sol' % name)
    cases.append((name, m, x, R.obj_value(m, x), ('x1', F(1, 10 ** 5))))
cases.append(('eniplac', E.m, E.y0, E.f0, ('x1', F(1, 1000))))
cases.append(('eniplac', E.m, E.y1, E.f1, None))
ms = step3_spring.m
xs = step3_spring.x
cases.append(('spring', ms, xs, R.obj_value(ms, xs), ('x3', F(-1, 10 ** 6))))
print()
for c in cases:
    print(c[0], scip_check(*c))
