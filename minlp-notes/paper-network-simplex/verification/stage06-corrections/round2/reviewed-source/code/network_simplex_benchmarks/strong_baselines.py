"""Vectorized numerical disaggregation baselines, without graph compression.

Instance balances use outgoing-minus-incoming, as in baselines.py. Optimization
keeps every original y and its objective when weights are free. Fixed weights
use positive state flows, native scaled bounds, and a constant y objective.
Point membership keeps only positive state flows; with two positive states it
can use the elementary f,x-f network reduction. Status 0 is numerical feasibility,
not an exact certificate. Input-domain flow checks use numerical LP tolerance.
"""
from fractions import Fraction as F
from time import perf_counter

import numpy as np
from scipy.optimize import OptimizeResult, linprog
from scipy.sparse import coo_matrix, csr_matrix, eye, hstack, kron, vstack

from .baselines import incidence, matrix_stats


def _rational(value):
    return F(str(value)) if isinstance(value, (float, np.floating)) else F(value)


def _finish(result, started, assembled, matrices, variables, **metadata):
    result.assembly_seconds = assembled-started
    result.solve_seconds = perf_counter()-assembled
    result.model_stats = dict(variables=variables, **matrix_stats(*matrices), **metadata)
    if result.status not in (0, 2):
        raise RuntimeError(f"Numerical LP failed with status {result.status}: {result.message}")
    return result


def optimize_ef(instance, objective, y_fixed=None, merge=False, extra_rows=()):
    """Known full or globally observed-label-merged EF, sparse block assembly."""
    started = perf_counter()
    E, m, obs = instance.edge_count, instance.simplex_size, instance.observations
    objective = np.asarray(objective, dtype=float)
    if objective.shape != (E+m+len(obs),) or not np.all(np.isfinite(objective)):
        raise ValueError("Objective must be finite and in original x,y,z order")
    labels = sorted({j for _, j in obs}) if merge else list(range(m))
    if y_fixed is not None:
        yf = np.asarray(y_fixed, float)
        if yf.shape != (m,) or not np.all(np.isfinite(yf)):
            raise ValueError("Fixed y must have m finite values")
        y = tuple(map(_rational, y_fixed))
        if any(v < 0 for v in y) or sum(y) > 1:
            result = OptimizeResult(success=False, status=2, message='Fixed y outside simplex')
            return _finish(result, started, perf_counter(), (), 0, states=0, merged=merge,
                           reduction='fixed-weight-domain-check')
        grouped = [y[j] for j in labels]+[1-sum(y[j] for j in labels)]
        states = [(j, w) for j, w in zip(labels+[m], grouped) if w > 0]
        slots = {j: i for i, (j, _) in enumerate(states)}
        q = len(states)
        weights = np.asarray([w for _, w in states], float)
        A, b = incidence(instance), np.asarray(instance.balances, float)
        u = np.asarray([arc[2] for arc in instance.arcs], float)
        eq = kron(eye(q, format='csr'), A, format='csr')
        rhs_eq = np.kron(weights, b)
        active = [(k, e, slots[j]) for k, (e, j) in enumerate(obs) if j in slots]
        positions = [slot*E+e for _, e, slot in active]
        c = np.tile(objective[:E], q)
        np.add.at(c, positions, [objective[E+m+k] for k, _, _ in active])
        rows, rhs_ub = [], []
        for coefficients, rhs in extra_rows:
            coefficients = np.asarray(coefficients, float)
            if coefficients.shape != objective.shape:
                raise ValueError("Additional rows must use original x,y,z order")
            row = np.tile(coefficients[:E], q)
            np.add.at(row, positions, [coefficients[E+m+k] for k, _, _ in active])
            rows.append(csr_matrix(row[None, :]))
            rhs_ub.append(float(rhs)-coefficients[E:E+m]@yf)
        ub = vstack(rows, format='csr') if rows else csr_matrix((0, q*E))
        bounds = np.column_stack((np.zeros(q*E), np.kron(weights, u)))
        assembled = perf_counter()
        result = linprog(c, A_eq=eq, b_eq=rhs_eq,
                         A_ub=ub if rows else None, b_ub=rhs_ub if rows else None,
                         bounds=bounds, method='highs')
        _finish(result, started, assembled, (eq, ub), q*E, states=q, merged=merge,
                reduction='fixed-positive-state-blocks')
        if result.success:
            flows = result.x.reshape(q, E)
            result.fun += float(objective[E:E+m]@yf)
            result.original_point = np.r_[flows.sum(axis=0), yf,
                [flows[slots[j], e] if j in slots else 0. for e, j in obs]]
        return result
    slots = {j: i for i, j in enumerate(labels)}
    q = len(labels)+1
    # State weights are offset + W*y. All original y columns are retained.
    W = coo_matrix(([1.]*len(labels)+[-1.]*len(labels),
                    (list(range(len(labels)))+[q-1]*len(labels), labels+labels)),
                   shape=(q, m)).tocsr()
    offset = np.zeros(q); offset[-1] = 1
    A, b = incidence(instance), np.asarray(instance.balances, float)
    u = np.asarray([arc[2] for arc in instance.arcs], float)
    eq = hstack((-kron(W, csr_matrix(b[:, None]), format='csr'),
                 kron(eye(q, format='csr'), A, format='csr')), format='csr')
    rhs_eq = np.kron(offset, b)
    capacities = hstack((-kron(W, csr_matrix(u[:, None]), format='csr'),
                         eye(q*E, format='csr')), format='csr')
    simplex = hstack((csr_matrix(np.ones((1, m))), csr_matrix((1, q*E))), format='csr')
    ub = vstack((capacities, simplex), format='csr')
    rhs_ub = np.r_[np.kron(offset, u), 1.]
    c = np.r_[objective[E:E+m], np.tile(objective[:E], q)]
    if obs:
        np.add.at(c, [m+slots[j]*E+e for e, j in obs], objective[E+m:])
    for coefficients, rhs in extra_rows:
        coefficients = np.asarray(coefficients, float)
        if coefficients.shape != objective.shape:
            raise ValueError("Additional rows must use original x,y,z order")
        row = np.r_[coefficients[E:E+m], np.tile(coefficients[:E], q)]
        if obs:
            np.add.at(row, [m+slots[j]*E+e for e, j in obs], coefficients[E+m:])
        ub = vstack((ub, csr_matrix(row[None, :])), format='csr')
        rhs_ub = np.r_[rhs_ub, float(rhs)]
    bounds = [(0., 1.)]*m + [(0., None)]*(q*E)
    assembled = perf_counter()
    result = linprog(c, A_eq=eq, b_eq=rhs_eq, A_ub=ub, b_ub=rhs_ub,
                     bounds=bounds, method='highs')
    _finish(result, started, assembled, (eq, ub), m+q*E, states=q, merged=merge)
    if result.success:
        flows = result.x[m:].reshape(q, E)
        result.original_point = np.r_[flows.sum(axis=0), result.x[:m],
                                      [flows[slots[j], e] for e, j in obs]]
    return result


def optimize_independent_states(instance, objective, y_fixed):
    """Fixed-y linear optimization factors into independent network LPs.

This applies only without additional coupled original-coordinate constraints.
Globally unobserved labels have the same flow cost and share one network solve.
Solver times are summed; the incidence matrix is assembled once.
"""
    started = perf_counter()
    E, m, obs = instance.edge_count, instance.simplex_size, instance.observations
    objective = np.asarray(objective, float)
    y = tuple(map(_rational, y_fixed))
    if len(y) != m or any(v < 0 for v in y) or sum(y) > 1:
        raise ValueError("Fixed weights must lie in the simplex")
    if objective.shape != (E+m+len(obs),):
        raise ValueError("Objective must use original x,y,z order")
    labels = sorted({j for _, j in obs})
    weights = [y[j] for j in labels]+[1-sum(y[j] for j in labels)]
    slots = {j: i for i, j in enumerate(labels)}
    costs = np.tile(objective[:E], (len(labels)+1, 1))
    for k, (edge, state) in enumerate(obs):
        costs[slots[state], edge] += objective[E+m+k]
    A = incidence(instance)
    b = np.asarray(instance.balances, float)
    bounds = [(0., float(cap)) for _, _, cap in instance.arcs]
    flows = np.zeros_like(costs)
    assembled = perf_counter()
    calls = 0
    for slot, weight in enumerate(weights):
        if weight == 0: continue
        result = linprog(costs[slot], A_eq=A, b_eq=b, bounds=bounds, method='highs')
        calls += 1
        if result.status not in (0, 2):
            raise RuntimeError(f"Network LP failure: {result.status}: {result.message}")
        if not result.success:
            return _finish(result, started, assembled, (A,), E, network_solves=calls)
        flows[slot] = float(weight)*result.x
    original = np.r_[flows.sum(axis=0), np.asarray(y, float),
                      [flows[slots[j], e] for e, j in obs]]
    result = OptimizeResult(success=True, status=0, fun=float(objective@original), original_point=original)
    return _finish(result, started, assembled, (A,), E, network_solves=calls,
                   storage_note='one reused network matrix; number of sequential solves reported')


def membership_ef(instance, x, y, z, merge=False, two_state=True):
    """Numerical point membership with exact zero-weight detection.

The two-state reduction uses exact input bounds and observation consistency,
then calls a single network LP. At >=3 states, state and aggregate matrices
are assembled by Kronecker products. x,y,z are data, never LP variables.
"""
    started = perf_counter()
    E, m, obs = instance.edge_count, instance.simplex_size, instance.observations
    if len(x) != E or len(y) != m or len(z) != len(obs):
        raise ValueError("Point dimensions do not match instance")
    xq, yq, zq = tuple(map(_rational, x)), tuple(map(_rational, y)), tuple(map(_rational, z))
    uq = tuple(_rational(arc[2]) for arc in instance.arcs)
    A, b = incidence(instance), np.asarray(instance.balances, float)
    xf = np.asarray(xq, float)

    def direct(feasible, reason, states=0):
        now = perf_counter()
        result = OptimizeResult(success=feasible, status=0 if feasible else 2, message=reason)
        return _finish(result, started, now, (), 0, states=states, merged=merge,
                       reduction='direct-domain-check')

    if any(v < 0 for v in yq) or sum(yq) > 1:
        return direct(False, 'Simplex domain violation')
    if any(v < 0 or v > cap for v, cap in zip(xq, uq)):
        return direct(False, 'Aggregate flow bound violation')
    if np.max(np.abs(A@xf-b), initial=0.) > 1e-9:
        return direct(False, 'Aggregate balance fails numerical tolerance')
    original_weights = yq+(1-sum(yq),)
    if any(v < 0 or v > original_weights[j]*uq[e] for (e, j), v in zip(obs, zq)):
        return direct(False, 'Observed state bound violation')
    labels = sorted({j for _, j in obs}) if merge else list(range(m))
    grouped_weights = [yq[j] for j in labels]+[1-sum(yq[j] for j in labels)]
    states = [(j, weight) for j, weight in zip(labels+[m], grouped_weights) if weight != 0]
    slots = {j: i for i, (j, _) in enumerate(states)}
    q = len(states)
    assert q >= 1
    if q == 1:
        return direct(all(v == xq[e] for (e, j), v in zip(obs, zq) if original_weights[j] != 0),
                      'Single positive state checked directly', states=1)
    if q == 2 and two_state:
        first, second = states[0][1], states[1][1]
        lower = [max(F(0), value-second*cap) for value, cap in zip(xq, uq)]
        upper = [min(first*cap, value) for value, cap in zip(xq, uq)]
        for (edge, state), value in zip(obs, zq):
            if state not in slots:
                assert value == 0
                continue
            fixed = value if slots[state] == 0 else xq[edge]-value
            lower[edge] = max(lower[edge], fixed)
            upper[edge] = min(upper[edge], fixed)
        if any(lo > hi for lo, hi in zip(lower, upper)):
            return direct(False, 'Two-state bounds contradict observations', states=2)
        assembled = perf_counter()
        result = linprog(np.zeros(E), A_eq=A, b_eq=float(first)*b,
                         bounds=list(zip(map(float, lower), map(float, upper))), method='highs')
        return _finish(result, started, assembled, (A,), E, states=2, merged=merge,
                       reduction='one-flow-network')
    balances = kron(eye(q, format='csr'), A, format='csr')
    aggregates = kron(csr_matrix(np.ones((1, q))), eye(E, format='csr'), format='csr')
    active_obs = [(e, slots[j], value) for (e, j), value in zip(obs, zq) if j in slots]
    observations = coo_matrix((np.ones(len(active_obs)),
                               (np.arange(len(active_obs)), [j*E+e for e, j, _ in active_obs])),
                              shape=(len(active_obs), q*E)).tocsr()
    eq = vstack((balances, aggregates, observations), format='csr')
    weights = np.asarray([weight for _, weight in states], float)
    rhs = np.r_[np.kron(weights, b), xf, [float(v) for _, _, v in active_obs]]
    capacities = np.kron(weights, np.asarray(uq, float))
    bounds = np.column_stack((np.zeros(q*E), capacities))
    assembled = perf_counter()
    result = linprog(np.zeros(q*E), A_eq=eq, b_eq=rhs, bounds=bounds, method='highs')
    return _finish(result, started, assembled, (eq,), q*E, states=q, merged=merge,
                   reduction='positive-state-blocks')
