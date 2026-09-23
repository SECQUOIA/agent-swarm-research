"""Independent exact-rational checks of surrogate-cell safe screening.

Run from repository root: python code/bilevel_reopened/screening_review_checks.py
Uses SymPy rational arithmetic, exhaustive true active-set enumeration, and
one-dimensional LP elimination. Does not import the implementation under review.
"""
from itertools import product
import json
import random
import sympy as s

R = s.Rational

def intersect(interval, constant, slope):
    """Intersect a closed rational interval with constant + slope*x >= 0."""
    if interval is None:
        return None
    lo, hi = interval
    if slope > 0:
        lo = max(lo, -constant / slope)
    elif slope < 0:
        hi = min(hi, -constant / slope)
    elif constant < 0:
        return None
    return (lo, hi) if lo <= hi else None


def active_piece(Q, c, C, statuses, interval):
    n = len(c)
    free = [i for i in range(n) if statuses[i] == 'F']
    upper = [i for i in range(n) if statuses[i] == 'U']
    z0, z1 = s.zeros(n, 1), s.zeros(n, 1)
    for i in upper:
        z0[i] = 1
    if free:
        inv = Q.extract(free, free).inv()
        p0 = -inv * (c + Q*z0).extract(free, [0])
        p1 = -inv * C.extract(free, [0])
        for j, i in enumerate(free):
            z0[i], z1[i] = p0[j], p1[j]
    g0, g1 = Q*z0+c, Q*z1+C
    for i, status in enumerate(statuses):
        if status == 'F':
            interval = intersect(interval, z0[i], z1[i])
            interval = intersect(interval, 1-z0[i], -z1[i])
            assert g0[i] == g1[i] == 0
        else:
            sign = 1 if status == 'L' else -1
            interval = intersect(interval, sign*g0[i], sign*g1[i])
    return interval, z0, z1


def greater_radical(a, b, strict=True):
    assert b >= 0
    return (a > 0 and 4*a*a > b) if strict else (a >= 0 and 4*a*a >= b)


def screen(Q, D, c, C, y0, y1, interval):
    lo, hi = interval
    inv, E = Q.inv(), Q-D
    p0, p1 = E*y0, E*y1
    endpoint_p = [p0+p1*x for x in interval]
    eta = max((p.T*inv*p)[0] for p in endpoint_p)
    center0, center1 = y0-inv*p0/2, y1-inv*p1/2
    grad0, grad1 = D*y0+c+p0/2, D*y1+C+p1/2
    statuses = []
    for i in range(len(c)):
        smin, smax = sorted([center0[i]+center1[i]*x for x in interval])
        tmin, tmax = sorted([grad0[i]+grad1[i]*x for x in interval])
        rb, sb = inv[i,i]*eta, Q[i,i]*eta
        certificates = []
        if greater_radical(tmin, sb) or greater_radical(-smax, rb, False):
            certificates.append('L')
        if greater_radical(-tmax, sb) or greater_radical(smin-1, rb, False):
            certificates.append('U')
        if (greater_radical(smin, rb, False) and greater_radical(1-smax, rb, False)
                and greater_radical(smax, rb) and greater_radical(1-smin, rb)):
            certificates.append('F')
        assert len(certificates) <= 1
        statuses.append(certificates[0] if certificates else None)
    return statuses, eta


def objective_value(pieces, objective, upper_rows):
    values = []
    alpha, b = objective
    for interval, z0, z1 in pieces:
        for a, row, h in upper_rows:
            interval = intersect(interval, h-(row.T*z0)[0], -a-(row.T*z1)[0])
        if interval is not None:
            values.extend((b.T*z0)[0]+(alpha+(b.T*z1)[0])*x for x in interval)
    return min(values) if values else None


def run(seed=97013, cases=24):
    rng = random.Random(seed)
    results = {'seed': seed, 'random_cases': cases, 'cells': 0,
               'certified_statuses': 0, 'recovery_assignments': 0,
               'full_assignments': 0, 'directional_checks': 0}
    for case in range(cases):
        n = 3 + case % 2
        D = s.diag(*[R(rng.randint(2, 5)) for _ in range(n)])
        A = s.Matrix(n, n, [R(rng.randint(-2, 2)) for _ in range(n*n)])
        Q = D + A.T*A/R(400 if case % 3 else 3)
        c = s.Matrix([R(rng.randint(-10, 4), 4) for _ in range(n)])
        C = s.Matrix([R(rng.randint(-8, 8), 3) for _ in range(n)])
        all_statuses = list(product('LFU', repeat=n))
        full = [active_piece(Q, c, C, st, (R(0), R(1))) for st in all_statuses]
        full = [piece for piece in full if piece[0] is not None]
        knots = {R(0), R(1)}
        for i in range(n):
            if C[i]:
                knots.update(x for x in [-c[i]/C[i], (-D[i,i]-c[i])/C[i]] if 0 < x < 1)
        knots = sorted(knots)
        reduced = []
        for lo, hi in zip(knots, knots[1:]):
            mid = (lo+hi)/2
            y0, y1 = s.zeros(n, 1), s.zeros(n, 1)
            for i in range(n):
                value = -(c[i]+C[i]*mid)/D[i,i]
                if value >= 1:
                    y0[i] = 1
                elif value > 0:
                    y0[i], y1[i] = -c[i]/D[i,i], -C[i]/D[i,i]
            fixed, eta = screen(Q, D, c, C, y0, y1, (lo, hi))
            ambiguous = [i for i in range(n) if fixed[i] is None]
            results['cells'] += 1
            results['certified_statuses'] += n-len(ambiguous)
            results['recovery_assignments'] += 3**len(ambiguous)
            results['full_assignments'] += 3**n
            cell_reduced = []
            for choice in product('LFU', repeat=len(ambiguous)):
                statuses = fixed[:]
                for i, status in zip(ambiguous, choice):
                    statuses[i] = status
                piece = active_piece(Q, c, C, statuses, (lo, hi))
                if piece[0] is not None:
                    cell_reduced.append(piece)
            # Full coverage checked by exact interval union, including boundaries.
            intervals = sorted(piece[0] for piece in cell_reduced)
            assert intervals and intervals[0][0] == lo
            covered = lo
            for left, right in intervals:
                assert left <= covered
                covered = max(covered, right)
            assert covered == hi
            reduced.extend(cell_reduced)
            inv = Q.inv()
            for interval, z0, z1 in cell_reduced:
                for x in [interval[0], sum(interval)/2, interval[1]]:
                    y, z = y0+y1*x, z0+z1*x
                    e, p = z-y, (Q-D)*y
                    assert (e.T*Q*e+p.T*e)[0] <= 0
                    assert (p.T*inv*p)[0] <= eta
                    g = Q*z+c+C*x
                    for i, status in enumerate(fixed):
                        assert status != 'L' or z[i] == 0
                        assert status != 'U' or z[i] == 1
                        assert status != 'F' or g[i] == 0
                    for b in [s.eye(n)[:,0], Q[:,0], s.Matrix([R(rng.randint(-2,2)) for _ in range(n)])]:
                        centered = 2*(b.T*e)[0] + (b.T*inv*p)[0]
                        assert centered**2 <= (b.T*inv*b)[0]*(p.T*inv*p)[0]
                        results['directional_checks'] += 1
        for _ in range(6):
            objective = R(rng.randint(-2, 2)), s.Matrix([R(rng.randint(-3, 3)) for _ in range(n)])
            rows = [(R(rng.randint(-2, 2)), s.Matrix([R(rng.randint(-2, 2)) for _ in range(n)]), R(rng.randint(-2, 3))) for _ in range(2)]
            assert objective_value(full, objective, rows) == objective_value(reduced, objective, rows)
    # Singleton cell, zero residual, and a zero-gradient bound degeneracy.
    Q = s.eye(3)
    c, C = s.Matrix([0, -R(1,2), -1]), s.zeros(3,1)
    y = -c
    status, eta = screen(Q,Q,c,C,y,C,(R(0),R(0)))
    assert status == ['L','F','U'] and eta == 0
    assert active_piece(Q,c,C,['F','F','F'],(R(0),R(0)))[0] == (0,0)
    results['singleton_zero_residual_degeneracy'] = 'passed'
    # A closed free cell meets both clipping thresholds: F means zero gradient,
    # so the weak-closure certificate remains valid at degenerate endpoints.
    status, eta = screen(Q,Q,s.zeros(3,1),-s.ones(3,1),s.zeros(3,1),s.ones(3,1),(R(0),R(1)))
    assert status == ['F','F','F'] and eta == 0
    results['weak_closure_free_status'] = 'passed'
    # Perturbation corollary: one transition coordinate per original vertex,
    # at most two per one-dimensional simplex, with a full dense true Hessian.
    n = 8
    D = s.eye(n)
    c, C = s.Matrix([R(i,10) for i in range(n)]), -s.ones(n,1)
    A = s.Matrix(n,n,[R(rng.randint(-2,2)) for _ in range(n*n)])
    E = A.T*A/100000
    Q = D+E
    eps = max(sum(abs(E[i,j]) for j in range(n)) for i in range(n))
    radius_bound = 3  # ceil(sqrt(8)); m=L=1 and sigma=1/10 below.
    assert eps < R(1,10)/(4*radius_bound)
    knots = [R(i,10) for i in range(n)] + [R(1)]
    maximum_ambiguity = 0
    for lo,hi in zip(knots,knots[1:]):
        mid = (lo+hi)/2
        y0 = s.Matrix([-c[i] if mid>c[i] else 0 for i in range(n)])
        y1 = s.Matrix([1 if mid>c[i] else 0 for i in range(n)])
        transition_union = set()
        for x in (lo,hi):
            y = y0+y1*x
            g = D*y+c+C*x
            transitions = {i for i in range(n) if y[i] in (0,1) and g[i] == 0}
            assert len(transitions) <= 1
            transition_union.update(transitions)
        statuses, _ = screen(Q,D,c,C,y0,y1,(lo,hi))
        ambiguous = {i for i in range(n) if statuses[i] is None}
        assert ambiguous <= transition_union
        maximum_ambiguity = max(maximum_ambiguity,len(ambiguous))
    results['dense_8_coordinate_transition_corollary'] = {
        'q': 1, 'theorem_ambiguity_bound': 2,
        'observed_maximum_ambiguity': maximum_ambiguity,
        'perturbation_infinity_norm': str(eps), 'margin': '1/10'}
    return results

if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
