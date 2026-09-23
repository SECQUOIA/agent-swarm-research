"""Independent original-model checks; no production witness validator is used.

Run with ``python -m unittest lbesh_research.test_instances_independent -v``.
The optional ``--enumerate`` script mode uses CVXPY/Clarabel in a separate
environment to enumerate the 27 assignments of each small pilot instance.
"""
import itertools
import json
import math
import sys
import unittest

import pyomo.environ as pyo
from pyomo.gdp import Disjunct, Disjunction
from pyomo.core.expr.visitor import identify_variables

from .instances import build, manifest


def original_violation(model, modes):
    """Evaluate original variable bounds and active GDP rows directly."""
    worst = 0.0
    for v in model.component_data_objects(pyo.Var, descend_into=(pyo.Block, Disjunct)):
        value = float(pyo.value(v))
        if not math.isfinite(value):
            return math.inf
        if v.lb is not None:
            worst = max(worst, pyo.value(v.lb) - value)
        if v.ub is not None:
            worst = max(worst, value - pyo.value(v.ub))
        if v.is_integer():
            worst = max(worst, abs(value - round(value)))
    rows = list(model.component_data_objects(pyo.Constraint, active=True))
    for i, j in enumerate(modes):
        rows.extend(model.mode[i, j].component_data_objects(pyo.Constraint, active=True))
        worst = max(worst, abs(sum(pyo.value(model.mode[i, k].binary_indicator_var)
                                  for k in model.J) - 1))
    for row in rows:
        value = float(pyo.value(row.body))
        if not math.isfinite(value):
            return math.inf
        if row.lower is not None:
            worst = max(worst, pyo.value(row.lower) - value)
        if row.upper is not None:
            worst = max(worst, value - pyo.value(row.upper))
    return worst


class IndependentInstances(unittest.TestCase):
    def test_all_original_witnesses_and_structure(self):
        records = manifest()
        self.assertEqual(len(records), 51)
        self.assertEqual(sum(r['split'] == 'pilot' for r in records.values()), 18)
        self.assertEqual(sum(r['split'] == 'held_out' for r in records.values()), 33)
        for name, info in records.items():
            with self.subTest(name=name):
                m = build(name)
                n = info['units']
                self.assertLessEqual(original_violation(m, [1] * n), 1e-10)
                variables = list(m.component_data_objects(pyo.Var, descend_into=(pyo.Block, Disjunct)))
                self.assertEqual(sum(v.is_binary() for v in variables), info['n_binary'])
                self.assertEqual(sum(v.is_continuous() for v in variables), info['n_continuous'])
                choices = list(m.component_data_objects(Disjunction))
                self.assertEqual(len(choices), info['n_disjunctions'])
                self.assertTrue(all(d.xor and len(d.disjuncts) == 3 for d in choices))
                disjuncts = list(m.component_data_objects(Disjunct))
                self.assertEqual(len(disjuncts), info['n_disjuncts'])
                nonlinear = lambda row: row.body.polynomial_degree() not in (0, 1)
                self.assertEqual(sum(nonlinear(row) for d in disjuncts for row in
                                     d.component_data_objects(pyo.Constraint)),
                                 info['n_nonlinear_disjunct_rows'])
                self.assertEqual(sum(nonlinear(row) for row in m.component_data_objects(pyo.Constraint)),
                                 info['n_nonlinear_global_rows'])
                # Each congestion row couples neighboring disjunctions.
                involved = {v.index()[0] for v in identify_variables(m.congestion.body)
                            if v.parent_component() is m.x}
                self.assertEqual(involved, set(range(n)))

    def test_generation_is_deterministic_and_split_is_disjoint(self):
        records = manifest()
        seeds = {split: {r['seed'] for r in records.values() if r['split'] == split}
                 for split in ('pilot', 'held_out')}
        self.assertFalse(seeds['pilot'] & seeds['held_out'])
        for name in records:
            a, b = build(name), build(name)
            self.assertEqual(a._research_data, b._research_data)
            va = [(v.name, v.lb, v.ub, pyo.value(v)) for v in a.component_data_objects(
                pyo.Var, descend_into=(pyo.Block, Disjunct))]
            vb = [(v.name, v.lb, v.ub, pyo.value(v)) for v in b.component_data_objects(
                pyo.Var, descend_into=(pyo.Block, Disjunct))]
            self.assertEqual(va, vb)
            rows = lambda m: [(c.name, str(c.expr)) for c in m.component_data_objects(
                pyo.Constraint, descend_into=(pyo.Block, Disjunct))]
            self.assertEqual(rows(a), rows(b))

    def test_trigonometric_box_curvature(self):
        from .instances import _phi
        normalization = 1-math.cos(.75)
        # phi'' is minimized at the upper endpoint because cosine decreases
        # on [0, 15/11], strictly inside [0, pi/2].
        self.assertLess(15/11, math.pi/2)
        self.assertGreater(2.25*math.cos(15/11)/normalization, 0)
        self.assertEqual(_phi(0., 'trig'), 0.)
        self.assertEqual(_phi(.5, 'trig'), 1.)
        for z in (0., .5, 10/11):
            self.assertAlmostEqual(_phi(z, 'trig'),
                                   (1-math.cos(1.5*z))/normalization)


def enumerate_small_pilots():
    """Independent convex formulations; numerical evidence, not exact certificates."""
    import cvxpy as cp
    import numpy as np
    results = []
    for name, info in manifest().items():
        if (info['split'] != 'pilot' or info['size'] != 'small'
                or info['family'] not in ('exp', 'log', 'reciprocal', 'quadratic', 'logsumexp')):
            continue
        m = build(name)
        data = m._research_data['parameters']
        n, law = info['units'], info['family']
        best = None
        statuses = {}
        unresolved = []
        for modes in itertools.product(range(3), repeat=n):
            x = cp.Variable((n, 2))
            constraints = []
            if law == 'logsumexp':
                t = cp.Variable()
                constraints += [x >= -2, x <= 2, t >= 0, t <= 9*n,
                                cp.sum(x[:, 0]) >= 0, cp.sum(x[:, 1]) >= .1*n,
                                cp.sum_squares(x[:, 0] - .5*x[np.roll(np.arange(n), -1), 1]) <= t,
                                cp.sum_squares(x - x[np.roll(np.arange(n), -1), :]) <= .55*n]
                for i, j in enumerate(modes):
                    delta = cp.multiply(data[i]['scale'][j], x[i] - data[i]['centers'][j])
                    constraints.append(cp.sum(cp.exp(delta) + cp.exp(-delta)) <= data[i]['radius'][j])
                objective = cp.sum(cp.multiply(np.array([d['price'] for d in data]), x)) + .1*t
                objective += sum(data[i]['fixed'][j] for i, j in enumerate(modes))
            else:
                caps = np.array([d['capacity'] for d in data])
                t = cp.Variable(n)
                constraints += [x >= 0, x <= caps[:, None], t >= 0,
                                t <= np.array([m.t[i].ub for i in range(n)]),
                                cp.sum(x, axis=1) <= caps,
                                cp.sum(x[:, 0]) >= .28*sum(caps),
                                cp.sum(x[:, 1]) >= .22*sum(caps)]
                resources = np.array([d['resource'] for d in data])
                w = caps[:, None] * np.array([.28, .22])
                constraints += [cp.sum(cp.multiply(resources, x)) <= 1.08*np.sum(resources*w),
                                cp.sum_squares(cp.multiply(1/caps, x[:, 0] + .35*x[np.roll(np.arange(n), -1), 1]))
                                <= 1.08*np.sum(((w[:, 0] + .35*w[np.roll(np.arange(n), -1), 1])/caps)**2)]
                def phi(z):
                    if law == 'exp':
                        return (cp.exp(3*z)-1)/(math.exp(1.5)-1)
                    if law == 'log':
                        return -cp.log(1-z)/math.log(2)
                    if law == 'reciprocal':
                        return cp.inv_pos(1-z)-1
                    if law == 'quadratic':
                        return 4*cp.square(z)
                    raise ValueError(f'Unsupported cone law: {law}')
                for i, j in enumerate(modes):
                    d = data[i]
                    constraints.append(cp.sum(x[i]) <= caps[i]*d['mode_capacity'][j])
                    if j == 0:
                        constraints.append(t[i] == 0)
                    else:
                        z = x[i]/(1.1*caps[i])
                        cost = caps[i]*d['operating'][j]*(d['weight'][0]*phi(z[0])
                               + d['weight'][1]*phi(z[1]) + d['cross']*phi(cp.sum(z)/2))
                        constraints.append(t[i] >= cost)
                objective = cp.sum(t) + sum(data[i]['capacity']*data[i]['fixed'][j]
                                            for i, j in enumerate(modes))
            problem = cp.Problem(cp.Minimize(objective), constraints)
            assert problem.is_dcp()
            problem.solve(solver='CLARABEL', max_threads=1, time_limit=30,
                          tol_gap_abs=1e-9, tol_gap_rel=1e-9, tol_feas=1e-9)
            statuses[problem.status] = statuses.get(problem.status, 0) + 1
            if problem.status == cp.OPTIMAL_INACCURATE:
                problem.solve(solver='CLARABEL', max_threads=1, time_limit=30,
                              tol_gap_abs=1e-8, tol_gap_rel=1e-8, tol_feas=1e-8)
            if problem.status != cp.OPTIMAL:
                if problem.status != cp.INFEASIBLE:
                    unresolved.append({'modes': modes, 'status': problem.status,
                                       'objective': problem.value})
                continue
            for i in range(n):
                for p in range(2):
                    m.x[i, p].set_value(x.value[i, p], skip_validation=True)
                for j in range(3):
                    m.mode[i, j].indicator_var.set_value(j == modes[i])
            if law == 'logsumexp':
                m.t.set_value(float(t.value), skip_validation=True)
            else:
                for i in range(n):
                    m.t[i].set_value(float(t.value[i]), skip_validation=True)
            residual = original_violation(m, modes)
            original_objective = pyo.value(m.objective)
            assert residual < 2e-7, (name, modes, residual)
            assert abs(original_objective - problem.value) < 1e-7
            if best is None or original_objective < best['objective']:
                best = {'objective': original_objective, 'modes': modes,
                        'original_model_max_violation': residual}
        results.append({'name': name, 'assignments': 27, 'first_solve_statuses': statuses,
                        'unresolved_after_retry': unresolved, 'best': best})
    print(json.dumps({'cvxpy': cp.__version__, 'results': results}, indent=2))


if __name__ == '__main__':
    if '--enumerate' in sys.argv:
        enumerate_small_pilots()
    else:
        unittest.main()
