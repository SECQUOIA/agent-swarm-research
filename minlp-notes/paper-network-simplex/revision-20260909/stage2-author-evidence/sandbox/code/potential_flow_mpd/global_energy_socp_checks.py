"""Numerical SOCP designs with exact global rational quality certificates.

The solver is only a producer. Every reported design bound is independently
checked with the standard-library certificate module.
"""
from fractions import Fraction as F
import math
import cvxpy as cp
import networkx as nx
import numpy as np
from energy_design_certificate import verify
from envelope_rational_certificates import conserved_rounding, dyadic, upward_root


def run():
    rng = np.random.default_rng(285317)
    largest_gap = F(0)
    statuses = []
    for case in range(6):
        n = 3+case % 4
        graph = nx.complete_graph(n) if case % 2 else nx.cycle_graph(n)
        edges = list(graph.edges())
        m = len(edges)
        incidence = np.zeros((n, m))
        for e, (u, v) in enumerate(edges):
            incidence[u, e] = 1; incidence[v, e] = -1
        b = [int(x) for x in rng.integers(-2, 3, n-1)]
        b.append(-sum(b))
        if not any(b):
            b[0], b[-1] = 1, -1
        lower, total = F(1, 2), F(2*m)
        upper = total-(m-1)*lower
        beta = cp.Variable(m)
        pi = cp.Variable(n)
        z, u, t = cp.Variable(m, nonneg=True), cp.Variable(m, nonneg=True), cp.Variable(m, nonneg=True)
        drops = incidence.T @ pi
        constraints = [beta >= float(lower), beta <= float(upper), cp.sum(beta) == float(total),
                       pi[0] == 0, z >= drops, z >= -drops]
        for e in range(m):
            constraints += [cp.SOC(t[e]+u[e], cp.hstack([2*z[e], t[e]-u[e]])),
                            cp.SOC(beta[e]+z[e], cp.hstack([2*u[e], beta[e]-z[e]]))]
        problem = cp.Problem(cp.Maximize(3*np.array(b) @ pi-2*cp.sum(t)), constraints)
        problem.solve(solver='CLARABEL', tol_gap_abs=1e-10, tol_gap_rel=1e-10,
                      tol_feas=1e-10, max_iter=500)
        assert problem.status in ('optimal', 'optimal_inaccurate')
        statuses.append(problem.status)
        surplus = [max(F(0), dyadic(x-float(lower), 60)) for x in beta.value]
        assert sum(surplus) > 0
        profile = [lower+(total-m*lower)*x/sum(surplus) for x in surplus]
        potentials = [dyadic(x, 60) for x in pi.value]
        numerical_flow = []
        for (a, c), resistance in zip(edges, profile):
            drop = float(potentials[a]-potentials[c])
            numerical_flow.append(math.copysign(math.sqrt(abs(drop)/float(resistance)), drop))
        trial = conserved_rounding(edges, b, numerical_flow, bits=60)
        weights = [abs(x)**3/3 for x in trial]
        alpha = max(weights)
        multipliers = [F(0)]*m+[alpha-w for w in weights]+[alpha, F(0)]
        roots = [upward_root(abs(potentials[a]-potentials[c])**3/be, 2, bits=80)
                 for (a, c), be in zip(edges, profile)]
        upper_value = total*alpha-lower*sum(alpha-w for w in weights)
        lower_value = sum(F(x)*p for x, p in zip(b, potentials))-F(2, 3)*sum(roots)
        gap = 3*(upper_value-lower_value)
        certificate = {'format': 'quadratic-energy-design-v1', 'edges': [list(e) for e in edges],
                       'nominations': b, 'beta_lower': [str(lower)]*m, 'beta_upper': [str(upper)]*m,
                       'polytope_rows': [[1]*m, [-1]*m], 'polytope_rhs': [str(total), str(-total)],
                       'profile': list(map(str, profile)), 'potentials': list(map(str, potentials)),
                       'trial_flow': list(map(str, trial)), 'dual_multipliers': list(map(str, multipliers)),
                       'root_upper': list(map(str, roots)), 'tolerance': str(gap)}
        result = verify(certificate)
        assert F(result['certified_suboptimality']) == gap and 0 <= gap < F(1, 1000)
        largest_gap = max(largest_gap, gap)
    print('PASS: six SOCP designs with exact global rational certificates; statuses', statuses)
    print('Largest certified additive dissipation loss', float(largest_gap))


if __name__ == '__main__':
    run()
