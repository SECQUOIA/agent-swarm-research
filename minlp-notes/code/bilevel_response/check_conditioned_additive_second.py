"""Exact scalar-leader diagnostics for the conditioned-box additive proof.

Enumerate follower active faces to obtain an independent exact global
benchmark, then exercise the saturation/basis grid. Not a general solver.
Run with Python and SymPy.
"""

from itertools import combinations, product
import random
import sympy as s


def constrain(lo, hi, slope, intercept):
    """Intersect with slope*x+intercept >= 0."""
    if slope > 0:
        lo = max(lo, -intercept / slope)
    elif slope < 0:
        hi = min(hi, -intercept / slope)
    elif intercept < 0:
        return None
    return (lo, hi) if lo <= hi else None


def pieces(Q, c, D, domain):
    n = Q.rows
    result = []
    for status in product((0, 1, 2), repeat=n):
        free = [i for i in range(n) if status[i] == 2]
        d = s.Matrix([int(t == 1) for t in status])
        p = s.zeros(n, 1)
        if free:
            inverse = Q.extract(free, free).inv()
            rhs = c + Q * d
            dd = -inverse * rhs.extract(free, [0])
            pp = -inverse * D.extract(free, [0])
            for j, i in enumerate(free):
                d[i], p[i] = dd[j], pp[j]
        gd, gp = Q * d + c, Q * p + D
        bounds = domain
        for i, t in enumerate(status):
            constraints = ((p[i], d[i]), (-p[i], 1-d[i])) if t == 2 else (
                ((gp[i], gd[i]),) if t == 0 else ((-gp[i], -gd[i]),)
            )
            for slope, intercept in constraints:
                bounds = constrain(*bounds, slope, intercept)
                if bounds is None:
                    break
            if bounds is None:
                break
        if bounds is not None:
            result.append((*bounds, p, d))
    return result


def check(Q, c, D, a, b, domain=(s.S(0), s.S(1))):
    n = Q.rows
    eps = s.Rational(1, 8)
    delta = eps / n
    inv_norm = max(sum(abs(v) for v in Q.inv().row(i)) for i in range(n))
    mu = 1 / inv_norm
    low = [-sum(max(v, 0) for v in Q.row(i)) for i in range(n)]
    high = [-sum(min(v, 0) for v in Q.row(i)) for i in range(n)]
    affine = pieces(Q, c, D, domain)
    assert affine

    def value(x):
        values = [s.expand((a.T * (p*x+d))[0] + b*x)
                  for lo, hi, p, d in affine if lo <= x <= hi]
        assert values and len(set(values)) == 1
        return values[0]

    exact = min(value(x) for lo, hi, _, _ in affine for x in (lo, hi))
    cuts = set(domain)
    for i in range(n):
        if D[i]:
            cuts.update(x for t in (low[i], high[i])
                        if domain[0] <= (x := (t-c[i])/D[i]) <= domain[1])
    cuts = sorted(cuts)
    cells = [(x, x) for x in cuts] + list(zip(cuts, cuts[1:]))
    candidates = []
    for left, right in cells:
        mid = (left + right) / 2
        J = [i for i in range(n) if low[i] < c[i]+D[i]*mid < high[i]]
        if not J or all(D[i] == 0 for i in J):
            candidates.append(left if b >= 0 else right)
            continue
        selected = max(J, key=lambda i: abs(D[i]))
        B = D[selected] / mu
        start = (low[selected]-c[selected]) / mu
        end = (high[selected]-c[selected]) / mu
        for k in range(int(s.ceiling((end-start)/delta))):
            lo, hi = start+k*delta, min(start+(k+1)*delta, end)
            xlo, xhi = sorted((lo/B, hi/B))
            xlo, xhi = max(left, xlo), min(right, xhi)
            if xlo <= xhi:
                candidates.append(xlo if b >= 0 else xhi)
    achieved = min(map(value, candidates))
    A = sum(abs(v) for v in a)
    assert exact <= achieved <= exact + eps*A
    return len(affine), len(candidates), achieved-exact


def check_row_bases():
    rng = random.Random(381)
    for _ in range(60):
        target_rank = rng.randrange(1, 4)
        C = s.Matrix(6, target_rank, lambda i, j: rng.randrange(-5, 6))
        P = s.Matrix(target_rank, 3, lambda i, j: rng.randrange(-5, 6))
        E = C * P
        columns = E.rref()[1]
        q = len(columns)
        assert q
        rows = max(combinations(range(6), q),
                   key=lambda I: abs(E.extract(I, columns).det()))
        B = E.extract(rows, range(3))
        inverse = E.extract(rows, columns).inv()
        for i in range(6):
            coefficients = E.extract([i], columns) * inverse
            assert all(abs(v) <= 1 for v in coefficients)
            assert coefficients * B == E.row(i)
    print('PASS: 60 exact maximum-minor row-basis cases')


if __name__ == '__main__':
    check_row_bases()
    huge = s.Integer(2)**80
    cases = [
        ([[2, -1], [-1, 2]], [-huge/2, 0], [huge, 0], [1, -2], 3, (0, 1)),
        ([[2, 1], [1, 2]], [-huge/2, huge/2], [huge, -huge], [-3, 2], -huge, (0, 1)),
        ([[2, -1], [-1, 2]], [-1, 0], [0, 3], [2, -1], huge, (0, 1)),
        ([[2, -1], [-1, 2]], [0, -1], [1, 0], [1, 1], -huge, (0, 0)),
        ([[2, 0], [0, 2]], [huge, -huge], [0, 0], [1, -1], huge, (0, 1)),
        ([[2, -1], [-1, 2]], [-2, -3], [3, 5], [4, 3], 1, (0, 1)),
        ([[3, -1, 1], [-1, 3, -1], [1, -1, 3]], [-1, -2, 0], [3, 0, -2], [1, -3, 2], -2, (0, 1)),
    ]
    totals = [0, 0]
    for Q, c, D, a, b, domain in cases:
        result = check(s.Matrix(Q), s.Matrix(c), s.Matrix(D), s.Matrix(a),
                       s.sympify(b), tuple(map(s.sympify, domain)))
        totals[0] += result[0]
        totals[1] += result[1]
        print('PASS: affine pieces, candidates, exact error =', result)
    print('TOTAL:', len(cases), 'cases;', *totals, 'pieces/candidates')
