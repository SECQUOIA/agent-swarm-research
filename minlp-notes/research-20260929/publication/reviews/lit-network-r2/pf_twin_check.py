"""Reviewer r2: does every point of powerflow0030p (polar) map to a point of
powerflow0030r (rectangular) with the same cost and feasibility?
Random-point test in floating point (evidence, not proof).

Layout read from the GAMS files:
  0030p: x1..x30 = V, x31..x194 = flows, x195..x224 = theta, x225..x236 = gens; x195 = 0 (ref)
  0030r: x1..x164 = flows, x165..x194 = u, x195..x224 = w, x225..x236 = gens; x195 = 0 (ref)
Candidate maps: (u_i, w_i) = V_i * (c(th_i + phi), s(th_i + phi)) for (c,s) in {(cos,sin),(sin,cos)}
and phi in {0, pi/2, -pi/2, pi}. Flows are copied with offset 30, gens copied.
All rows are evaluated as (sense, body - rhs) and matched as multisets.
Voltage rows: polar 'V_i >= vmin' vs rect 'u^2 + w^2 >= vmin^2' are compared by sign only.
"""
import re, math, random, sys, itertools
from collections import Counter

def load(path):
    s = open(path).read()
    rows = []
    for name, body in re.findall(r'^(e\d+)\.\.(.*?);', s, re.S | re.M):
        b = ' '.join(body.split())
        m = re.search(r'=([ELG])=', b)
        lhs, rhs = b[:m.start()], b[m.end():]
        rows.append((name, m.group(1), compile(re.sub(r'\bsqr\(', 'sq(', lhs), name, 'eval'), float(eval(rhs)), b))
    return rows

def ev(rows, x):
    env = {'sq': lambda t: t * t, 'sin': math.sin, 'cos': math.cos}
    env.update(x)
    return [(name, sense, eval(code, env) - rhs, b) for name, sense, code, rhs, b in rows]

P = load('powerflow0030p.gms'); R = load('powerflow0030r.gms')
vre = re.compile(r'\s*sqr\(x(\d+)\) \+ sqr\(x(\d+)\) =([GL])= ([0-9.]+)\s*$')
nb, nf, ng = 30, 164, 12
random.seed(11)
for swap, phi in itertools.product([False, True], [0.0, math.pi / 2, -math.pi / 2, math.pi]):
    ok = True; report = []
    for trial in range(3):
        V = [random.uniform(0.9, 1.1) for _ in range(nb)]
        th = [0.0] + [random.uniform(-0.6, 0.6) for _ in range(nb - 1)]
        flows = [random.uniform(-2, 2) for _ in range(nf)]
        gens = [random.uniform(0, 1) for _ in range(ng)]
        xp, xr = {'objvar': 1234.5}, {'objvar': 1234.5}
        for i in range(nb):
            a, b = V[i] * math.cos(th[i] + phi), V[i] * math.sin(th[i] + phi)
            if swap: a, b = b, a
            xp['x%d' % (i + 1)] = V[i]; xp['x%d' % (195 + i)] = th[i]
            xr['x%d' % (165 + i)] = a; xr['x%d' % (195 + i)] = b
        for k in range(nf):
            xp['x%d' % (31 + k)] = flows[k]; xr['x%d' % (1 + k)] = flows[k]
        for g in range(ng):
            xp['x%d' % (225 + g)] = gens[g]; xr['x%d' % (225 + g)] = gens[g]
        vp = ev(P, xp); vr = ev(R, xr)
        pool = Counter((s, round(v, 8)) for _, s, v, _ in vp)
        unmatched = []
        for name, s, v, b in vr:
            key = (s, round(v, 8))
            if pool[key] > 0: pool[key] -= 1
            else: unmatched.append((name, s, v, b))
        bad = []
        for name, s, v, b in unmatched:
            mm = vre.match(b)
            if not mm: bad.append(name); continue
            i = int(mm.group(1)) - 165; lim = float(mm.group(4))
            if int(mm.group(2)) - 195 != i: bad.append(name); continue
            key = (s, round(V[i] - math.sqrt(lim), 8))
            if pool[key] > 0: pool[key] -= 1
            else: bad.append(name)
        left = [k for k, c in pool.items() for _ in range(c)]
        angle_rows = sum(1 for _, s, v, b in vp if re.fullmatch(r'\s*x\d+ - x\d+ =[LG]= -?0\.26\s*', b))
        report.append((len(unmatched), len(bad), len(left), angle_rows))
        if bad or len(left) != angle_rows: ok = False
    print('swap=%s phi=%+.4f' % (swap, phi), 'OK' if ok else 'no', report)
