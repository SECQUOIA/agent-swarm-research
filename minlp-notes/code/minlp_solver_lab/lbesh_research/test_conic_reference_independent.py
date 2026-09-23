"""Independent cone checks. Run in the optional conic-reference environment.

The alternative hull uses CVXPY's perspective atom rather than the author's
explicit ExpCone and rotated-SOC maps. Only small pilot instances are solved.
"""
import math
import unittest

import cvxpy as cp
import numpy as np

from .conic_reference import _phi_cone, solve
from .instances import build


def _phi(z, law):
    if law == 'exp':
        return (cp.exp(3*z)-1)/(math.exp(1.5)-1)
    if law == 'log':
        return -cp.log(1-z)/math.log(2)
    if law == 'reciprocal':
        return cp.inv_pos(1-z)-1
    if law == 'quadratic':
        return 4*cp.square(z)
    raise ValueError(law)


def independent_perspective_root(name):
    m = build(name)
    data = m._research_data['parameters']
    law = m._research_metadata['family']
    n = len(data)
    x = cp.Variable((n, 2))
    t = cp.Variable() if law == 'logsumexp' else cp.Variable(n)
    next_indices = np.roll(np.arange(n), -1)
    cons = []
    objective = 0
    if law == 'logsumexp':
        cons += [x >= -2, x <= 2, t >= 0, t <= 9*n,
                 cp.sum(x[:, 0]) >= 0, cp.sum(x[:, 1]) >= .1*n,
                 cp.sum_squares(x[:, 0]-.5*x[next_indices, 1]) <= t,
                 cp.sum_squares(x-x[next_indices, :]) <= .55*n]
        objective += cp.sum(cp.multiply(np.array([d['price'] for d in data]), x))+.1*t
    else:
        caps = np.array([d['capacity'] for d in data])
        resources = np.array([d['resource'] for d in data])
        witness = caps[:, None]*np.array([.28, .22])
        upper = np.array([m.t[i].ub for i in range(n)])
        cons += [x >= 0, x <= caps[:, None], cp.sum(x, axis=1) <= caps,
                 t >= 0, t <= upper,
                 cp.sum(x[:, 0]) >= .28*sum(caps), cp.sum(x[:, 1]) >= .22*sum(caps),
                 cp.sum(cp.multiply(resources, x)) <= 1.08*np.sum(resources*witness),
                 cp.sum_squares(cp.multiply(1/caps, x[:, 0]+.35*x[next_indices, 1]))
                 <= 1.08*np.sum(((witness[:, 0]+.35*witness[next_indices, 1])/caps)**2)]
        objective += cp.sum(t)
    for i, d in enumerate(data):
        weights, local_x, local_t = [], [], []
        for j in range(3):
            lam = cp.Variable(nonneg=True)
            u = cp.Variable(2)
            weights.append(lam)
            local_x.append(u)
            objective += d['fixed'][j]*lam*(1 if law == 'logsumexp' else caps[i])
            if law == 'logsumexp':
                cons += [u >= -2*lam, u <= 2*lam]
                delta = cp.multiply(d['scale'][j], u-np.array(d['centers'][j]))
                f = cp.sum(cp.exp(delta)+cp.exp(-delta))
                cons.append(cp.perspective(f, lam, f_recession=cp.Constant(0)) <= d['radius'][j]*lam)
            else:
                v = cp.Variable()
                local_t.append(v)
                cons += [u >= 0, u <= caps[i]*lam, v >= 0, v <= upper[i]*lam,
                         cp.sum(u) <= caps[i]*d['mode_capacity'][j]*lam]
                if j == 0:
                    cons.append(v == 0)
                else:
                    z = u/(1.1*caps[i])
                    cost = caps[i]*d['operating'][j]*(d['weight'][0]*_phi(z[0], law)
                           + d['weight'][1]*_phi(z[1], law)+d['cross']*_phi(cp.sum(z)/2, law))
                    cons.append(cp.perspective(cost, lam, f_recession=cp.Constant(0)) <= v)
        cons += [sum(weights) == 1, x[i] == sum(local_x)]
        if law != 'logsumexp':
            cons.append(t[i] == sum(local_t))
    problem = cp.Problem(cp.Minimize(objective), cons)
    assert problem.is_dcp()
    problem.solve(solver='CLARABEL', max_threads=1, time_limit=30,
                  tol_gap_abs=1e-9, tol_gap_rel=1e-9, tol_feas=1e-9)
    return problem


class IndependentConicReference(unittest.TestCase):
    def test_fractional_closed_scalar_perspectives(self):
        for law in ('exp', 'log', 'reciprocal', 'quadratic'):
            for lam in (0., 1e-5, .35, 1.):
                for zbar in (.1, .5, .85):
                    with self.subTest(law=law, lam=lam, zbar=zbar):
                        cons = []
                        q = _phi_cone(cp.Constant(lam*zbar), cp.Constant(lam), law, cons)
                        problem = cp.Problem(cp.Minimize(q), cons)
                        problem.solve(solver='CLARABEL', max_threads=1, time_limit=30,
                                      tol_gap_abs=1e-9, tol_gap_rel=1e-9, tol_feas=1e-9)
                        self.assertEqual(problem.status, cp.OPTIMAL)
                        expected = lam*float(_phi(cp.Constant(zbar), law).value)
                        self.assertLess(abs(problem.value-expected), 2e-8)

    def test_five_pilot_roots_against_perspective_atoms(self):
        for law in ('exp', 'log', 'reciprocal', 'quadratic', 'logsumexp'):
            with self.subTest(law=law):
                name = f'lbesh.{law}.small.s104729'
                independent = independent_perspective_root(name)
                reference = solve(name, time_limit=30)
                self.assertEqual(independent.status, cp.OPTIMAL)
                self.assertEqual(reference['status'], 'optimal')
                self.assertFalse(reference['bound_certified'])
                self.assertLess(abs(independent.value-reference['obj']), 2e-7)
                self.assertLess(abs(reference['obj']-reference['lb']), 2e-7)
                print(f'{name}: independent_root={independent.value:.12g}, '
                      f'explicit_cone_root={reference["obj"]:.12g}, '
                      f'dual_estimate={reference["lb"]:.12g}')


if __name__ == '__main__':
    unittest.main()
