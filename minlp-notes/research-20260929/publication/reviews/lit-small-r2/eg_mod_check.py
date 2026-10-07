"""Reviewer r2: (1) check that the MINLPLib AMPL .mod files of eg_disc2_s, eg_disc_s, eg_int_s
(the files CAMINO's SCIP/Gurobi runs read) define the same rows as the cached OSIL, at random points;
(2) evaluate the project's recorded feasible points on the .mod rows and report the smallest
objective value x8 that satisfies every row. Compare with Gurobi 13.0.0's 'bestbound' in the
CAMINO benchmark data. mpmath, 40 digits; numerical evidence (the exact feasibility of these points
was proved elsewhere in the project)."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])
_PUBLIC_HOME = str(_PublicPath.home())

import re, sys, random
sys.path.insert(0, (_PUBLIC_REPO + '/research-20260929/publication/reviews/lit-small-r1'))
from osil_eval import Model
from mpmath import mp, mpf, exp
mp.dps = 40
GUROBI_BOUND = {'eg_disc2_s': '5.88669499573929', 'eg_disc_s': '6.191829847658548', 'eg_int_s': '11.65415903480683'}

def parse_mod(path):
    s = open(path).read()
    body = s.split('subject to', 1)[1]
    rows = []
    for m in re.finditer(r'(e\d+):\s*(.*?);', body, re.S):
        txt = ' '.join(m.group(2).split())
        mm = re.match(r'(.*?)\s*(>=|<=|=)\s*([-+0-9.eE]+)$', txt)
        expr, sense, rhs = mm.group(1), mm.group(2), mm.group(3)
        expr = expr.replace('^', '**')
        expr = re.sub(r'(?<![\w.])(\d+\.?\d*(?:[eE][-+]?\d+)?)', r"mpf('\1')", expr)
        rows.append((m.group(1), compile(expr, m.group(1), 'eval'), sense, mpf(rhs)))
    return rows

NAMES = None
def ev(rows, x):
    env = {'exp': exp, 'mpf': mpf}
    env.update({(n if n != 'objvar' else 'x8'): v for n, v in zip(NAMES, x)})
    return [eval(c, env) for _, c, _, _ in rows]

for name in ('eg_disc2_s', 'eg_disc_s', 'eg_int_s'):
    rows = parse_mod(f'/tmp/lsr2/{name}.mod')
    M = Model(f'{_PUBLIC_HOME}/.cache/minlplib/minlplib/osil/{name}.osil')
    NAMES = [v['name'] for v in M.vars]
    assert NAMES[-1] == 'objvar' and len(NAMES) == 8
    lbub = [(mpf(v['lb']), mpf(v['ub'])) for v in M.vars[:7]]
    random.seed(7)
    worst = mpf(0)
    for t in range(5):
        x = [mpf(random.randint(int(lo), int(hi))) if v['type'] == 'I' else lo + (hi - lo) * mpf(random.random())
             for (lo, hi), v in zip(lbub, M.vars[:7])] + [mpf(random.uniform(-5, 10))]
        if t == 0: print('  sample row e1 value', mp.nstr(a0 if False else 0, 3)) if False else None
        a = ev(rows, x)
        for r in range(M.m):
            lo, hi = M.cons[r]['lb'], M.cons[r]['ub']
            # compare as (body - bound) with the .mod's (expr - rhs)
            ob = M.body(r, x)
            bnd = mpf(lo) if lo not in ('-INF',) else mpf(hi)
            d = abs((ob - bnd) - (a[r] - rows[r][3]))
            if t == 0 and r == 0: print('  ', name, 'row e1 at random point: OSIL', mp.nstr(ob - bnd, 12), '.mod', mp.nstr(a[r] - rows[r][3], 12))
            worst = max(worst, d / max(1, abs(a[r])))
    # recorded feasible point
    pt = {}
    for line in open(f'{_PUBLIC_REPO}/research-20260929/open-instances-wave3/eg/retry/sol/{name}.retry.sol'):
        k, v = line.split()
        pt[k] = mpf(v)
    x = [pt[n] for n in NAMES[:7]] + [mpf(0)]
    a0 = ev(rows, x); x[7] = mpf(1); a1 = ev(rows, x)
    need = mpf('-inf')
    for (rn, _, sense, rhs), v0, v1 in zip(rows, a0, a1):
        c = v1 - v0
        if c == 0:
            ok = (v0 >= rhs) if sense == '>=' else (v0 <= rhs) if sense == '<=' else (v0 == rhs)
            if not ok: print('  row without x8 violated', rn, v0 - rhs)
            continue
        if sense == '>=' and c > 0: need = max(need, (rhs - v0) / c)
        elif sense == '<=' and c < 0: need = max(need, (v0 - rhs) / (-c))
        else: print('  unexpected row form', rn, sense, c)
    print(name, 'rows', len(rows), 'max rel diff .mod vs OSIL', mp.nstr(worst, 3),
          '| recorded point objvar', mp.nstr(pt['objvar'], 20), '| min x8 feasible on .mod', mp.nstr(need, 20),
          '| Gurobi 13.0.0 bestbound (CAMINO)', GUROBI_BOUND[name], '| bound exceeds feasible value by', mp.nstr(mpf(GUROBI_BOUND[name]) - need, 6))
