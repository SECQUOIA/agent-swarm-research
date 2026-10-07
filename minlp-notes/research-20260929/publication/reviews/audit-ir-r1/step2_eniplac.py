"""eniplac p2: build exactly feasible points from (a) the listed point and
(b) the audit's proof-box centre (logs/verify/eniplac.p2.center.sol), by
keeping flows x1..x24, x99..x110 (exact decimals), rounding binaries, forcing
the six demand equalities e27..e32 by moving one interior flow per period,
and computing every other variable from its defining equality. The final
point is checked exactly against every row and bound of the OSIL model with
rv_osil.check (independent of the construction)."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

from fractions import Fraction as F
import rv_osil as R

BA = (_PUBLIC_REPO + '/research-20260929/bound-audit/')
m = R.load('eniplac')
pos = {n: j for j, n in enumerate(m.vname)}
row = {n: r for r, n in enumerate(m.cname)}


def build(path, label):
    x, unk = R.read_sol(m, path)
    y = list(x)
    # binaries rounded
    for j, t in enumerate(m.vtype):
        if t == 'B':
            y[j] = F(round(x[j]))
    keep = ['x%d' % i for i in range(1, 25)] + ['x%d' % i for i in range(99, 111)]
    keepset = set(pos[v] for v in keep) | {j for j, t in enumerate(m.vtype) if t == 'B'}
    adjusted = []
    # demand rows e27..e32: sum flows(period) - x(98+p) + x(104+p) = D
    for r in ['e27', 'e28', 'e29', 'e30', 'e31', 'e32']:
        ri = row[r]
        val = R.row_value(m, ri, y)
        resid = m.clb[ri] - val  # needed change of the row body
        if resid != 0:
            # move the flow with coefficient 1 that has the most room to its
            # capacity row (x <= cap*b) and to its lower bound 0
            best = None
            for j, c in m.lin[ri].items():
                if c != 1 or m.vname[j] not in keep[:24]:
                    continue
                room = y[j]
                if room > 0 and (best is None or room > best[1]):
                    best = (j, room)
            j = best[0]
            y[j] += resid
            adjusted.append((r, m.vname[j], float(resid)))
        assert R.row_value(m, ri, y) == m.clb[ri]
    # propagate: equality rows with exactly one non-kept variable whose value is
    # not yet set, linear in it -> solve. Repeat.
    known = set(keepset)
    eq_rows = [r for r in range(len(m.cname)) if m.clb[r] == m.cub[r]]
    changed = True
    while changed:
        changed = False
        for r in eq_rows:
            unknown = set()
            for j in m.lin[r]:
                if j not in known:
                    unknown.add(j)
            for i, j, c in m.quad.get(r, []):
                for k in (i, j):
                    if k not in known:
                        unknown.add(k)
            # nl variables: collect
            def collect(e, acc):
                if R.tag(e) == 'variable':
                    acc.add(int(e.get('idx')))
                for c in e:
                    collect(c, acc)
            nlv = set()
            for e in m.nl.get(r, []):
                collect(e, nlv)
            unknown |= {k for k in nlv if k not in known}
            if len(unknown) != 1:
                continue
            k = unknown.pop()
            assert k in m.lin[r] and k not in nlv and all(k not in (i, j) for i, j, c in m.quad.get(r, []))
            y[k] = F(0)
            base = R.row_value(m, r, y)
            y[k] = (m.clb[r] - base) / m.lin[r][k]
            assert R.row_value(m, r, y) == m.clb[r]
            known.add(k)
            changed = True
    missing = [m.vname[j] for j in range(len(m.vname)) if j not in known]
    bad = R.check(m, y)
    f = R.obj_value(m, y)
    maxchg = max(abs(float(y[j] - x[j])) for j in range(len(y)))
    print('==', label)
    print('  demand adjustments:', adjusted)
    print('  undetermined variables:', missing)
    print('  exact violations:', len(bad), bad[:5])
    print('  max |change| vs input point: %.3e' % maxchg)
    print('  objective exact: %s/%s' % (f.numerator, f.denominator) if len(str(f.denominator)) < 60 else '  objective denominator digits %d' % len(str(f.denominator)))
    from decimal import Decimal, getcontext
    getcontext().prec = 40
    print('  objective ~', Decimal(f.numerator) / Decimal(f.denominator))
    lo, hi = F('-132117.0830149'), F('-132117.0830141')
    print('  in audit enclosure [-132117.0830149, -132117.0830141]:', lo <= f <= hi)
    d = F(-132117)
    print('  d - f =', Decimal((d - f).numerator) / Decimal((d - f).denominator), ' (d-f)/|d| = %.4e' % float((d - f) / abs(d)),
          ' (d-f)/0.5 = %.4f' % float((d - f) / F(1, 2)))
    # tight rows
    tight = [m.cname[r] for r in range(len(m.cname)) if m.clb[r] != m.cub[r] and
             ((m.clb[r] != '-INF' and R.row_value(m, r, y) == m.clb[r]) or
              (m.cub[r] != 'INF' and R.row_value(m, r, y) == m.cub[r]))]
    print('  inequality rows exactly at a side:', len(tight))
    return y, f


y0, f0 = build(BA + 'sol/eniplac.p2.sol', 'from listed point')
y1, f1 = build(BA + 'logs/verify/eniplac.p2.center.sol', 'from audit proof-box centre')
