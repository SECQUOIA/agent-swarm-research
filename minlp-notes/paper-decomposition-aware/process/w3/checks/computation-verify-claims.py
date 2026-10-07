"""Verifier checks of Section 11 claims that summarize.py does not test directly.

(1) S1 failure: two optimal vertices that differ in a concave coordinate.
(2) E6: on the 29 instances without a growth certificate, H + 2M is (exactly)
    not positive definite at the candidate (Lemma growthcert(a) fails there).
(3) E6 table: the time column (max over q) is attained at q = 50.
(4) E5 SCIP times (rounding of the table entries).
(5) Off-grid claim: decompose the free coordinates of x* that are nodes of the
    last grid into k = 0 (dyadic) and those set to x*_i by the initial descent.
(6) S1 replay of the eps = 2^-60 run valid on all 30 instances.
"""
import csv
import json
import sys
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

EXP = Path(__file__).resolve().parents[3] / 'experiments'
sys.path.insert(0, str(EXP))
from instances import planted, random_small, random_continuous  # noqa: E402
from certified_grid import solve  # noqa: E402
from exact_output import solve_exact  # noqa: E402


def rows(name):
    with open(EXP / 'results' / f'{name}.csv') as fh:
        return list(csv.DictReader(fh))


def is_pd(m):
    """Exact positive definiteness: all pivots of symmetric elimination > 0."""
    a = [list(r) for r in m]
    n = len(a)
    for k in range(n):
        if a[k][k] <= 0:
            return False
        for i in range(k + 1, n):
            f = a[i][k] / a[k][k]
            for j in range(k, n):
                a[i][j] -= f * a[k][j]
    return True


# (1)
p = random_small(8, 'path', 2, 7014)
ex = solve_exact(p, time_limit=60, max_rounds=12, max_stages=3000, max_table_states=300000)
x = tuple(F(v) for v in ex['point'])
opt = F(ex['upper'])
cont = [i for i in range(8) if i not in p.integers]
print('(1) S1 failure: OPT', opt, 'EX point', [str(v) for v in x])
print('    vertex (all continuous coords at a bound):', all(x[i] in p.bounds[i] for i in cont))
for i in range(8):
    if p.A[i][i] <= 0:
        lo, hi = p.bounds[i]
        y = list(x)
        y[i] = hi if x[i] == lo else lo if x[i] == hi else None
        if y[i] is None:
            continue
        print(f'    coord {i} (A_ii={p.A[i][i]}, integer={i in p.integers}): flipped value',
              p.value(tuple(y)), 'optimal' if p.value(tuple(y)) == opt else '')

# (2), (3)
e6 = rows('E6_random_growth')
byname = defaultdict(dict)
for r in e6:
    byname[r['name']][int(r['q'])] = r
notpd, checked = 0, 0
time_at_q50 = defaultdict(lambda: [0.0, 0.0])
for name, qs in byname.items():
    r = qs[50]
    grp = f"{r['kind']}{r['n']}"
    time_at_q50[grp][0] = max(time_at_q50[grp][0], float(r['solve_s']))
    time_at_q50[grp][1] = max(time_at_q50[grp][1], max(float(v['solve_s']) for v in qs.values()))
    if r['growth_status'] == 'certified':
        continue
    raw = json.loads((EXP / 'results' / 'raw' / f"E6_{r['kind']}_n{r['n']}_s{r['seed']}.json").read_text())
    prob = random_continuous(r['kind'], int(r['n']), int(r['seed']))
    # candidate of the growth test: stationary point of the face of the final incumbent
    from localized import candidate
    best = solve(prob, epsilon=F(1, 2 ** 50), max_stages=600, time_limit=120,
                 max_table_states=10 ** 6, convex_presolve=False)
    xh = candidate(prob, tuple(F(v) for v in best['point']))
    n = len(xh)
    H, b = prob.A, prob.b
    z = [b[i] + sum(H[i][j] * xh[j] for j in range(n)) for i in range(n)]
    S = [i for i in range(n) if prob.bounds[i][0] < xh[i] < prob.bounds[i][1]]
    ok_first_order = all(z[i] == 0 for i in S) and all(
        not ((xh[i] == prob.bounds[i][0] and z[i] < 0) or (xh[i] == prob.bounds[i][1] and z[i] > 0))
        for i in range(n) if i not in S)
    mu = {i: abs(z[i]) / (prob.bounds[i][1] - prob.bounds[i][0]) for i in range(n) if i not in S}
    K = [[H[i][j] + (2 * mu.get(i, 0) if i == j else 0) for j in range(n)] for i in range(n)]
    checked += 1
    notpd += (not is_pd(K))
    if is_pd(K) or not ok_first_order:
        print('   ', name, 'first-order ok:', ok_first_order, 'PD:', is_pd(K))
print(f'(2) E6 without growth certificate: {checked} instances, H+2M exactly not PD on {notpd}')
print('(3) E6 max solve time at q=50 vs over all q, per row:')
for g, (a, b_) in sorted(time_at_q50.items()):
    print(f'    {g}: q=50 {a:.2f}  all q {b_:.2f}')

# (4)
print('(4) E5 SCIP wall times per row:')
sc = defaultdict(list)
for r in rows('E5_scip'):
    sc[f"{r['kind']}{r['n']}"].append(float(r['wall_s']))
for k, v in sc.items():
    print('   ', k, sorted(round(t, 4) for t in v))

# (5)
print('(5) free coordinates of x* on the last grid (E1-E3, kappa_target >= 4)')
tot = defaultdict(int)
for e in ('E1', 'E2', 'E3'):
    st = rows(f'{e}_stages')
    last = {}
    for r in st:
        if r['key'] not in last or int(r['stage']) > int(last[r['key']]['stage']):
            last[r['key']] = r
    runs = {r['key']: r for r in rows(f'{e}_runs')}
    cache = {}
    for key, r in last.items():
        info = runs[key]
        if int(info['kappa_target']) < 4:
            continue
        inst = (info['kind'], int(info['n']), int(info['kappa_target']), int(info['seed']))
        if inst not in cache:
            prob, pinfo = planted(*inst)
            c0 = solve(prob, epsilon=F(1, 10 ** 6), max_stages=0, time_limit=60, convex_presolve=False)
            y0 = [F(v) for v in c0['initial']['point']]
            xs = [F(v) for v in pinfo['xstar']]
            free = [i for i in range(inst[1]) if i not in set(pinfo['active'])]
            cache[inst] = (sum(1 for i in free if xs[i] == 0),
                           sum(1 for i in free if xs[i] != 0 and y0[i] == xs[i]),
                           sum(1 for i in free if xs[i] != 0 and y0[i] != xs[i]
                               and (y0[i] - xs[i]).denominator & ((y0[i] - xs[i]).denominator - 1) == 0))
        z, d, other = cache[inst]
        tot['on_grid'] += int(r['xstar_nodes_free'])
        tot['free'] += int(r['n_free'])
        tot['k0'] += z
        tot['set_by_descent'] += d
        tot['dyadic_offset_other'] += other
print('   ', dict(tot))

# (6)
s1 = rows('S1_localized')
print('(6) S1 history replays valid:', sum(r['history_valid'] == 'True' for r in s1), 'of', len(s1))
