"""Review r2: recompute the changed numbers from the raw logs (no stream imports).

Checks: DM60 row of the Section 6 table, BT10 general-only rounds (2057/2688 and
per-p means), total sep_ratio calls in the BT loops (5168), finished/certified
counts (103, 17, 120/123), Theorem 3 rerun table in Section 8 and the rank-1
short-split records.
Usage from split-practice/: python3 reviews/r2-code/r2_numbers.py
"""
import collections
import json
import statistics as st
from fractions import Fraction as F
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
L = ROOT / 'logs'


def jl(path):
    return [json.loads(x) for x in open(path) if x.strip()]


# ---------------------------------------------------------------- Section 6, DM60 row
opt = {d['name']: d for d in jl(L / 'opt_gurobi.jsonl')}
for s in ['DM30', 'DM60', 'BT50']:
    by = collections.defaultdict(dict)
    for d in jl(L / f'points_{s}.jsonl'):
        if 'stage' in d:
            by[d['name']][d['stage']] = d
    gaps, closures, closed, rr, rc = [], [], 0, [], []
    for name, d in by.items():
        root, cut = d['root'], d['cut']
        best = root['opt'] if root['opt'] is not None else opt[name]['best']
        # Best known value for minimization: the smaller of the incumbent and
        # the objective of an integral feasible final SDP point.
        Z = np.load(ROOT / f'data/points_{s}/{name}__{"BT" if s.startswith("BT") else "DM"}__cut.npz')
        x = Z['Y'][0, 1:] / Z['Y'][0, 0]
        xi = np.round(x)
        integral = np.max(np.abs(x - xi)) < 1e-4
        feasible = np.all(np.abs(xi) <= 1) and (not bool(Z['linear']) or abs(xi.sum()) < 0.5)
        if integral and feasible:
            fx = float(xi @ Z['Q'] @ xi + Z['c'] @ xi)
            if fx < best - 1e-9:
                print(f'  {s} {name}: integral final point {fx:.6f} better than incumbent {best:.6f}')
            best = min(best, fx)
        gaps.append(100 * (best - root['obj']) / abs(best))
        cl = 100 * (cut['obj'] - root['obj']) / (best - root['obj']) if best - root['obj'] > 1e-9 else 100.0
        closures.append(min(cl, 100.0))
        closed += (best - cut['obj']) <= 1e-4 * abs(best)
        rr.append(root['rank']['1e-05']); rc.append(cut['rank']['1e-05'])
    print(f'{s}: inst {len(by)}, root rank {min(rr)}/{st.median(rr):g}/{max(rr)}, '
          f'SDP gap mean {st.mean(gaps):.4f}, closed {closed}, mean closure {st.mean(closures):.4f}, '
          f'final rank {min(rc)}/{st.median(rc):g}/{max(rc)}')

# ---------------------------------------------------------------- Section 7
tot_rounds = gen_rounds = 0
per_p = collections.defaultdict(list)
for d in jl(L / 'loop_bt_BT10.jsonl'):
    p = int(d['name'].split('_p')[1].split('_')[0])
    g = 0
    for h in d['hist']:
        tot_rounds += 1
        fam_ok = all(h['fam_viol'].get(k, 0) <= 1e-6 for k in ('1', '2', '3'))
        if fam_ok and h['ratio_q'] is not None and -h['ratio_q'] > 1e-6:
            g += 1
    gen_rounds += g
    open_ = d['opt'] - d['root'] > 1e-7
    per_p[p].append((g, open_))
print(f'BT10 general-only rounds {gen_rounds} of {tot_rounds} ({100*gen_rounds/tot_rounds:.1f}%)')
print('per-p mean (all instances):', [round(st.mean(g for g, _ in per_p[p]), 1) for p in range(11)])
print('per-p mean (open instances):', [round(st.mean([g for g, o in per_p[p] if o] or [0]), 1) for p in range(11)])
calls = collections.Counter(); capped = 0
for mode in ('bt', 'btfam'):
    for s in ('BT10', 'BT20'):
        for d in jl(L / f'loop_{mode}_{s}.jsonl'):
            for h in d['hist']:
                if 'ratio_nodes' in h:
                    calls[mode] += 1
                    capped += not h['ratio_complete']
print(f'sep_ratio calls in BT loops: {dict(calls)}, total {sum(calls.values())}, capped {capped}')

# ---------------------------------------------------------------- Section 8 counts
recs = [d for k in range(3) for d in jl(L / f'sep_run2_s{k}.jsonl')]
opn = set(open(L / 'open_gap.txt').read().split())


def group(f):
    name, stage = f[:-4].split('__')[0], f[:-4].split('__')[-1]
    return 'root' if stage == 'root' else ('open' if name in opn else 'near')


fin = collections.Counter(group(d['file']) for d in recs if d['ratio']['complete'])
print('records', len(recs), 'finished by class', dict(fin), 'total', sum(fin.values()))
cert = {d['file']: d for d in jl(L / 'ratio_certificates_r1.jsonl')}
fc = collections.Counter()
for d in recs:
    c = cert[d['file']]
    assert c['finished'] == d['ratio']['complete'] and abs(c['rho'] - d['ratio']['ratio']) == 0
    if d['ratio']['complete'] or c['certified']:
        fc[group(d['file'])] += 1
print('finished or certified by class', dict(fc), 'total', sum(fc.values()))
newc = [f for f, c in cert.items() if c['certified'] and not c['finished']]
print('newly certified', len(newc), collections.Counter(group(f) for f in newc))
print('uncertified capped', [(f, cert[f].get('bound')) for f, c in cert.items() if not c['finished'] and not c['certified']])

# ---------------------------------------------------------------- Theorem 3 rerun
T = jl(L / 'thm3_r1.jsonl')
rows = collections.defaultdict(list)
for d in T:
    assert 'error' not in d, d['file']
    rows[group(d['file'])].append(d['thm3'])
for g in ('root', 'open', 'near'):
    R = rows[g]
    ret = [t for t in R if t['v'] is not None]
    qex = [F(t['q_exact']) for t in R]
    vm = [max(abs(a) for a in t['v']) for t in ret]
    # Recompute vmax from v (includes v0) and support from v[1:].
    sup = [sum(a != 0 for a in t['v'][1:]) for t in ret]
    sane = sum(-0.25 - 1e-6 <= t['q_at_Y'] < 0 for t in ret)
    print(f'thm3 {g}: attempts {len(R)}, returned {len(ret)}, both complete {sum(t["complete"] for t in R)}, '
          f'first complete {sum(t["first_complete"] for t in R)}, second complete {sum(t["second_complete"] for t in R)}, '
          f'exact -1/4 {sum(q == F(-1, 4) for q in qex)}, within 1e-9 {sum(abs(q + F(1, 4)) < F(1, 10**9) for q in qex)}, '
          f'vmax median {st.median(vm)} max {max(vm)} min {min(vm)}, support {min(sup)}-{max(sup)}, sane {sane}, '
          f'time median {st.median(t["total_time"] for t in R):.3f} max {max(t["total_time"] for t in R):.3f}')
    nr = [t['ratio_at_Y'] for t in ret]
    print(f'   normalized at stored point: median {st.median(nr):.3g}, max {max(nr):.3g}; '
          f'q_at_Y range {min(t["q_at_Y"] for t in ret):.6g} .. {max(t["q_at_Y"] for t in ret):.6g}')
# exactness of each logged q_at_Y_exact vs logged v and stored Y (all returned)
bad = 0
for d in T:
    t = d['thm3']
    if t['v'] is None:
        continue
    f = d['file']; n = f.split('_n')[1].split('_')[0]
    Y = np.load(ROOT / f'data/points_{"BT" if f.startswith("bt") else "DM"}{n}/{f}')['Y']
    Y = (Y + Y.T) / 2
    v = t['v']; N = len(v)
    YF = [[F(float(a)) for a in row] for row in Y]
    q = sum(F(v[i]) * YF[i][j] * v[j] for i in range(N) for j in range(N) if v[i] and v[j]) + \
        sum(F(v[i]) * YF[i][0] for i in range(N) if v[i])
    bad += q != F(t['q_at_Y_exact'])
print('stored-point q recomputed exactly for all returned thm3 vectors; mismatches:', bad)

# ---------------------------------------------------------------- rank-1 check records
R1 = jl(L / 'rank1_short_r1.jsonl')
for d in R1:
    f = d['file']; n = f.split('_n')[1].split('_')[0]
    Y = np.load(ROOT / f'data/points_BT{n}/{f}')['Y']; Y = (Y + Y.T) / 2
    x = [F(round(float(a) * 10**6), 10**6) for a in Y[0, 1:] / Y[0, 0]]
    D = 1
    for a in x:
        D = D * a.denominator // __import__('math').gcd(D, a.denominator)
    p = [D] + [int(a * D) for a in x]
    v = d['v']
    m = sum(a * b for a, b in zip(p, v))
    qn = F(m * (m + D), D * D)
    N = len(v)
    YF = [[F(float(a)) for a in row] for row in Y]
    qY = sum(F(v[i]) * YF[i][j] * v[j] for i in range(N) for j in range(N)) + sum(F(v[i]) * YF[i][0] for i in range(N))
    print(f'rank1 {f}: D={D} m=-D/2? {m == -(D // 2)} q_nb={qn} q_Y={float(qY):.9f} '
          f'vmax={max(map(abs, v))} supp={sum(a != 0 for a in v[1:])} norm={float(-qY / sum(a*a for a in v[1:])):.6g} '
          f'best_norm={d["best_normalized"]:.6g}')
