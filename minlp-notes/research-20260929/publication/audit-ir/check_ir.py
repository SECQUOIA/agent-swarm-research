"""Independent exact check of the bound audit's class (i-r) pairs.

Own code (osilq.py + this file). Uses only the cached OSiL files, the stored
MINLPLib points (bound-audit/sol/) and the listed dual strings. All
feasibility decisions use exact rational arithmetic (Python Fraction).

Output: logs/check_ir.json and a printed summary.
"""
import json
import os
from fractions import Fraction as Q

import osilq
from osilq import RI

HERE = os.path.dirname(os.path.abspath(__file__))
OSIL = os.path.expanduser('~/.cache/minlplib/minlplib/osil/')
SOL = os.path.join(HERE, '..', '..', 'bound-audit', 'sol')

# The 12 (instance, solver) pairs of class (i-r), with the listed dual
# strings as shown on the instance pages, the flagged points and the
# enclosures stated in bound-audit/audit-report.md (Section 4 table).
PAIRS = {
    'eniplac': dict(points=['p2'], d='-132117.', solvers=['COUENNE', 'LINDO', 'SCIP'],
                    stated=('-132117.0830149', '-132117.0830141')),
    'lop97icx': dict(points=['p2'], d='4099.06', solvers=['ANTIGONE'],
                     stated=('4099.059953600', '4099.059953601')),
    'spring': dict(points=['p3', 'p2'], d='0.84624567',
                   solvers=['ANTIGONE', 'BARON', 'COUENNE', 'LINDO', 'SCIP'],
                   stated=('0.8462456656363', '0.8462456656500')),
    'stockcycle': dict(points=['p2'], d='119949.', solvers=['ANTIGONE', 'BARON', 'COUENNE'],
                       stated=('119948.6883333', '119948.6883334')),
}


def fstr(q, digits=25):
    """Decimal string of a Fraction, truncated toward zero (for display)."""
    s = '-' if q < 0 else ''
    q = abs(q)
    ip = q.numerator // q.denominator
    fr = q - ip
    return s + str(ip) + '.' + str(int(fr * 10 ** digits)).rjust(digits, '0')


def last_digit_unit(s):
    """Unit of the last shown digit of a plain decimal string."""
    assert 'e' not in s.lower()
    t = s.lstrip('-+')
    _, dot, frac = t.partition('.')
    return Q(1, 10 ** len(frac))


def display_unit(s):
    """Unit of the coarser of the 10th significant digit and the 8th
    decimal: the finest unit to which MINLPLib's page display (at most 10
    significant digits, at most 8 decimals) can have rounded the value."""
    v = abs(Q(s))
    assert v != 0
    e = 0                       # v in [10^e, 10^(e+1))
    while Q(10) ** (e + 1) <= v:
        e += 1
    while Q(10) ** e > v:
        e -= 1
    u10 = Q(10) ** (e - 9)      # unit of the 10th significant digit
    return max(u10, Q(1, 10 ** 8))


def nonlinear_vars(model, i):
    s = set(model.nlvars.get(i, set()))
    for (j, k, a) in model.quad.get(i, []):
        s.update((j, k))
    return s


def propagate(model, x, unknown):
    """Solve equality rows that contain exactly one unknown variable, which
    appears only in the row's linear part. Exact. Returns the solve order
    and the set of variables left unknown."""
    unknown = set(unknown)
    order = []
    changed = True
    while unknown and changed:
        changed = False
        for i in range(model.m):
            if not model.is_eq(i):
                continue
            u = model.row_vars(i) & unknown
            if len(u) != 1:
                continue
            (j,) = u
            if j not in model.lin[i] or j in nonlinear_vars(model, i):
                continue
            x[j] = Q(0)
            rest = model.row(i, x)
            x[j] = (model.rlb[i] - rest) / model.lin[i][j]
            unknown.discard(j)
            order.append((model.names[j], model.rnames[i]))
            changed = True
    return order, unknown


def summarize_bad(bad, k=5):
    bad = sorted(bad, key=lambda t: -t[2])
    return [(a, b, float(c)) for a, b, c in bad[:k]], len(bad)


def margins(name, f_hi, sense='min'):
    """Margin of each listed dual over an exactly feasible objective value."""
    p = PAIRS[name]
    d = Q(p['d'])
    assert sense == 'min'
    marg = d - f_hi
    half = last_digit_unit(p['d']) / 2
    disp = display_unit(p['d']) / 2
    return dict(d=p['d'], margin=float(marg), margin_exact=fstr(marg, 20),
                rel=float(marg / abs(d)),
                slack_audit=float(half),               # half unit, last shown digit
                ratio_audit=float(marg / half),
                full_unit=float(2 * half),
                ratio_full_unit=float(marg / (2 * half)),
                slack_display=float(disp),             # display rule only
                ratio_display=float(marg / disp),
                invalid_as_listed=marg > 0,
                within_audit_slack=0 < marg <= half,
                within_display_slack=0 < marg <= disp)


def stated_contains(name, f):
    lo, hi = PAIRS[name]['stated']
    return Q(lo) <= f <= Q(hi)


def as_listed(name, pt):
    m = osilq.Model(OSIL + name + '.osil')
    x, ign = osilq.read_sol(os.path.join(SOL, '%s.%s.sol' % (name, pt)), m)
    bad, f = osilq.check_exact(m, x)
    return m, x, ign, bad, f


# ------------------------------------------------------------------ routes
def route_as_listed(name, pt):
    m, x, ign, bad, f = as_listed(name, pt)
    out = dict(instance=name, point=pt, sense=m.sense, n=m.n, m=m.m,
               ignored_sol_names=ign, route='listed point, exact check',
               n_violations=len(bad), violations=summarize_bad(bad)[0],
               exactly_feasible=not bad, obj_exact=fstr(f, 30),
               obj_is_rational=str(f) if f.denominator < 10 ** 40 else None)
    if not bad:
        out['in_stated_enclosure'] = stated_contains(name, f)
        out['margins'] = margins(name, f)
    return out


def route_eniplac(pt='p2', start=None):
    """Keep the given decimals of the generator outputs x1..x24, the
    transfer variables x99..x110 and the binaries; recompute every other
    variable exactly from the equality rows (each is linear in the variable
    it determines once x1..x24 and the binaries are fixed). If a demand row
    e27..e32 does not hold exactly at the kept values, the variable of that
    row with the most room (distance to its bounds and to every linear
    inequality row it enters, at the start point) is recomputed from it.
    start=None uses the listed point; otherwise a .sol path (the audit's
    proof-box centre, used as input data only)."""
    m, x, ign, bad0, f0 = as_listed('eniplac', pt)
    x_listed = list(x)
    if start is not None:
        x, _ = osilq.read_sol(start, m)
    for j in range(m.n):
        if m.vtype[j] == 'B':
            assert x[j] in (0, 1), m.names[j]
    keep = {'x%d' % k for k in range(1, 25)} | {'x%d' % k for k in range(99, 111)}
    keep |= {m.names[j] for j in range(m.n) if m.vtype[j] == 'B'}

    def room(j):
        r = []
        if m.lb[j] is not None:
            r.append(x[j] - m.lb[j])
        if m.ub[j] is not None:
            r.append(m.ub[j] - x[j])
        for i in range(m.m):
            if m.is_eq(i) or j not in m.lin[i] or nonlinear_vars(m, i):
                continue
            v = m.row(i, x)
            for b in (m.rlb[i], m.rub[i]):
                if b is not None:
                    r.append(abs(v - b) / abs(m.lin[i][j]))
        return min(r)

    adjusted = []
    for rn in ('e27', 'e28', 'e29', 'e30', 'e31', 'e32'):
        i = m.rnames.index(rn)
        if m.row(i, x) != m.rlb[i]:
            rm, nm = max((room(j), m.names[j]) for j in m.lin[i])
            assert rm > 0
            keep.discard(nm)
            adjusted.append((rn, nm, float(rm)))
    unknown = {j for j in range(m.n) if m.names[j] not in keep}
    x = list(x)
    order, left = propagate(m, x, unknown)
    assert not left, [m.names[j] for j in left]
    bad, f = osilq.check_exact(m, x)
    moved = max(abs(a - b) for a, b in zip(x, x_listed))
    # tightest inequality rows / bounds at the new point
    act = []
    for i in range(m.m):
        if m.is_eq(i):
            continue
        v = m.row(i, x)
        for side, b in (('ub', m.rub[i]), ('lb', m.rlb[i])):
            if b is not None:
                act.append((abs(v - b), m.rnames[i], side))
    act.sort()
    nb_at = sum(1 for j in range(m.n)
                if (m.lb[j] is not None and x[j] == m.lb[j]) or
                (m.ub[j] is not None and x[j] == m.ub[j]))
    out = dict(instance='eniplac', point=pt,
               route='propagation of exact equalities from ' +
               ('the listed point' if start is None else os.path.basename(start)),
               demand_rows_adjusted=adjusted,
               listed_point_violations=summarize_bad(bad0)[1],
               listed_point_worst=summarize_bad(bad0)[0][:3],
               listed_point_obj=fstr(f0, 20),
               n_recomputed=len(order), max_change_from_listed=float(moved),
               n_violations=len(bad), violations=summarize_bad(bad)[0],
               exactly_feasible=not bad, obj_exact=fstr(f, 30),
               obj_denominator_digits=len(str(f.denominator)),
               rows_at_bound=[(r, s) for d, r, s in act if d == 0],
               vars_at_bound=nb_at,
               in_stated_enclosure=stated_contains('eniplac', f))
    if not bad:
        out['margins'] = margins('eniplac', f)
    return out, x


def icbrt_exact(n):
    """Largest integer r >= 0 with r^3 <= n (bisection, exact)."""
    lo, hi = 0, 1
    while hi ** 3 <= n:
        hi *= 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid ** 3 <= n:
            lo = mid
        else:
            hi = mid
    return lo


def route_spring(pts=('p3', 'p2'), k=30):
    """spring with i4 = 9 and b11 = 1 (as in the listed points) has
    x2 = 0.283 and x3 = c*9*x5^3/x2 with x5 = x1/x2. The objective
    (1.570796327 + 0.7853981635*i4)*x1*x2^2 increases with x1, and x3 >=
    lb(x3) is the binding constraint. The infimum point has x3 = lb(x3) and
    x5* = cbrt(A), A = lb(x3)*x2/(9c), irrational. We (a) build an exactly
    feasible rational point with x5 = x5* rounded up at 10^-k, and (b)
    enclose the infimum point exactly (rational bracket of the cube root;
    the point exists by construction and its inequalities are checked by
    exact rational interval arithmetic)."""
    m = osilq.Model(OSIL + 'spring.osil')
    N = m.index
    res = dict(instance='spring', listed={})
    xs = {}
    for pt in pts + ('p1',):
        path = os.path.join(SOL, 'spring.%s.sol' % pt)
        if not os.path.exists(path):
            path = os.path.join(HERE, 'sol_live', 'spring.%s.sol' % pt)
        if not os.path.exists(path):
            continue
        x, ign = osilq.read_sol(path, m)
        bad, f = osilq.check_exact(m, x)
        xs[pt] = x
        res['listed'][pt] = dict(obj=fstr(f, 20), n_violations=len(bad),
                                 violations=summarize_bad(bad)[0],
                                 i4=str(x[N['i4']]),
                                 ones=[m.names[j] for j in range(m.n)
                                       if m.vtype[j] == 'B' and x[j] == 1])
    # the integer assignment shared by p3 and p2
    for pt in pts:
        assert xs[pt][N['i4']] == 9 and res['listed'][pt]['ones'] == ['b11']
    i4 = Q(9)
    # constants read from the model (not retyped): x3 lower bound, and the
    # coefficient c of e5 and the e8 coefficient of b11
    lb3 = m.lb[N['x3']]
    e8 = m.rnames.index('e8')
    x2 = -m.lin[e8][N['b11']]
    assert x2 == Q('0.283')
    c = Q('6.95652173913044e-7')
    # check c against the model: row e5 at a test point equals x3 - c*x5^3*i4/x2
    t = [Q(0)] * m.n
    t[N['x3']], t[N['x5']], t[N['i4']], t[N['x2']] = Q(1, 7), Q(3, 2), i4, x2
    e5 = m.rnames.index('e5')
    assert m.row(e5, t) == Q(1, 7) - c * Q(3, 2) ** 3 * i4 / x2
    A = lb3 * x2 / (c * i4)
    # rational bracket lo <= cbrt(A) <= hi, width 10^-k
    s = 10 ** k
    r = icbrt_exact((A * s ** 3).numerator // (A * s ** 3).denominator)
    lo5, hi5 = Q(r, s), Q(r + 1, s)
    assert lo5 ** 3 <= A <= hi5 ** 3
    # (a) exactly feasible rational point: x5 = hi5, x1 = x2*hi5
    x = list(xs[pts[0]])
    for j in range(m.n):
        if m.vtype[j] == 'B':
            x[j] = Q(1) if m.names[j] == 'b11' else Q(0)
    x[N['i4']] = i4
    x[N['x1']] = x2 * hi5
    order, left = propagate(m, x, {N['x2'], N['x3'], N['x5'], N['x6']})
    assert not left
    bad, f = osilq.check_exact(m, x)
    assert x[N['x5']] == hi5
    res['rational_point'] = dict(
        x={nm: fstr(x[N[nm]], 32) for nm in ('x1', 'x2', 'x3', 'i4', 'x5', 'x6')},
        solve_order=order, n_violations=len(bad), exactly_feasible=not bad,
        obj_exact=fstr(f, 30), x3_minus_lb=float(x[N['x3']] - lb3),
        in_stated_enclosure=stated_contains('spring', f))
    if not bad:
        res['rational_point']['margins'] = margins('spring', f)
    x_rational = list(x)
    # (b) the infimum point (x3 = lb exactly, x5 = cbrt(A)) enclosed in a box
    X5 = RI(lo5, hi5)
    box = [RI(v) for v in x]
    box[N['x5']] = X5
    box[N['x1']] = RI(x2) * X5
    box[N['x3']] = RI(lb3)
    box[N['x6']] = (4 * X5 - 1) / (4 * X5 - 4) + Q('.615') / X5
    ineq = {}
    for i in range(m.m):
        if m.is_eq(i):
            continue
        v = m.row(i, box)
        ok = ((m.rlb[i] is None or v.lo >= m.rlb[i]) and
              (m.rub[i] is None or v.hi <= m.rub[i]))
        ineq[m.rnames[i]] = dict(ok=ok, lo=float(v.lo), hi=float(v.hi),
                                 lb=None if m.rlb[i] is None else float(m.rlb[i]),
                                 ub=None if m.rub[i] is None else float(m.rub[i]))
    bnd = all((m.lb[j] is None or box[j].lo >= m.lb[j]) and
              (m.ub[j] is None or box[j].hi <= m.ub[j]) for j in range(m.n))
    F = m.obj(box)
    res['infimum_point'] = dict(
        inequalities=ineq, all_inequalities_ok=all(v['ok'] for v in ineq.values()),
        bounds_ok=bnd, obj_lo=fstr(F.lo, 30), obj_hi=fstr(F.hi, 30),
        obj_width=float(F.hi - F.lo),
        in_stated_enclosure=stated_contains('spring', F.lo) and stated_contains('spring', F.hi),
        margins_at_infimum=margins('spring', F.lo))
    return res, x_rational


def main():
    out = {}
    out['lop97icx'] = route_as_listed('lop97icx', 'p2')
    out['stockcycle'] = route_as_listed('stockcycle', 'p2')
    out['eniplac'], xen = route_eniplac()
    out['eniplac_from_audit_centre'], xen2 = route_eniplac(start=os.path.join(
        HERE, '..', '..', 'bound-audit', 'logs', 'verify', 'eniplac.p2.center.sol'))
    out['spring'], xsp = route_spring()
    os.makedirs(os.path.join(HERE, 'logs'), exist_ok=True)
    with open(os.path.join(HERE, 'logs', 'check_ir.json'), 'w') as fh:
        json.dump(out, fh, indent=1, default=str)
    # the constructed exactly feasible points, as exact fractions
    for nm, fn, xx in (('eniplac', 'eniplac.p2.exact.sol', xen),
                       ('eniplac', 'eniplac.p2.centre.exact.sol', xen2),
                       ('spring', 'spring.p3.exact.sol', xsp)):
        m = osilq.Model(OSIL + nm + '.osil')
        with open(os.path.join(HERE, 'logs', fn), 'w') as fh:
            for j in range(m.n):
                fh.write('%s %s\n' % (m.names[j], xx[j]))
    print(json.dumps(out, indent=1, default=str))


if __name__ == '__main__':
    main()
