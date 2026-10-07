"""Reviewer r2: exact-rational comparison of the cached OSIL models powerflow0030p (polar) and
powerflow0030r (rectangular) under the map
    u_i = V_i cos(th_i),  w_i = -V_i sin(th_i),  flows and generator variables copied.
Points: random rational V_i and rational-parametrized angles (cos = (1-t^2)/(1+t^2), sin = 2t/(1+t^2)),
so every row value is an exact rational. Rows are matched as exact multisets of (value, lb, ub).
Agreement at random rational points is strong (Schwartz-Zippel type) evidence of polynomial identity,
not a symbolic proof."""
import os, random, xml.etree.ElementTree as ET
from fractions import Fraction as F
from collections import Counter
D = os.path.expanduser('~/.cache/minlplib/minlplib/osil/')
NS = '{os.optimizationservices.org}'

def expand(el_parent, kind):
    out = []
    for el in el_parent:
        mult = int(el.get('mult', '1'))
        if kind == 'int':
            v = int(el.text); inc = int(el.get('incr', '0'))
            out += [v + k * inc for k in range(mult)]
        else:
            out += [F(el.text)] * mult
    return out

class Ang:
    def __init__(self, c, s): self.c, self.s = c, s
    def scale(self, k):
        assert k in (1, -1), k
        return Ang(self.c, self.s * k)
    def add(self, o): return Ang(self.c * o.c - self.s * o.s, self.s * o.c + self.c * o.s)

def load(name):
    r = ET.parse(D + name + '.osil').getroot()
    cons = r.find(f'.//{NS}constraints')
    rows = [[F(c.get('lb')) if c.get('lb') not in (None, '-INF') else None,
             F(c.get('ub')) if c.get('ub') not in (None, 'INF') else None] for c in cons]
    lin = r.find(f'.//{NS}linearConstraintCoefficients')
    terms = [[] for _ in rows]
    if lin is not None:
        start = expand(lin.find(f'{NS}start'), 'int')
        idxel = lin.find(f'{NS}colIdx'); rowmajor = idxel is not None
        if not rowmajor: idxel = lin.find(f'{NS}rowIdx')
        idx = expand(idxel, 'int'); val = expand(lin.find(f'{NS}value'), 'val')
        for k in range(len(start) - 1):
            for p in range(start[k], start[k + 1]):
                if rowmajor: terms[k].append(('l', idx[p], val[p]))
                else: terms[idx[p]].append(('l', k, val[p]))
    obj = []
    o = r.find(f'.//{NS}obj')
    for c in o: obj.append(('l', int(c.get('idx')), F(c.text)))
    q = r.find(f'.//{NS}quadraticCoefficients')
    if q is not None:
        for t in q:
            i = int(t.get('idx')); tt = ('q', int(t.get('idxOne')), int(t.get('idxTwo')), F(t.get('coef')))
            (obj if i == -1 else terms[i]).append(tt)
    nl = r.find(f'.//{NS}nonlinearExpressions')
    if nl is not None:
        for e in nl:
            i = int(e.get('idx')); (obj if i == -1 else terms[i]).append(('n', e[0]))
    return rows, terms, obj

def ev(node, x, ang):
    t = node.tag[len(NS):]
    if t == 'variable':
        i = int(node.get('idx')); k = F(node.get('coef', '1'))
        if i in ang: return ang[i].scale(int(k))
        return k * x[i]
    if t == 'number': return F(node.get('value'))
    ch = [ev(c, x, ang) for c in node]
    if t == 'sum':
        if isinstance(ch[0], Ang):
            a = ch[0]
            for b in ch[1:]: a = a.add(b)
            return a
        return sum(ch, F(0))
    if t == 'product':
        p = F(1)
        for c in ch: p *= c
        return p
    if t == 'square': return ch[0] * ch[0]
    if t == 'negate': return -ch[0]
    if t == 'sin': return ch[0].s
    if t == 'cos': return ch[0].c
    raise ValueError(t)

def body(tl, x, ang):
    v = F(0)
    for t in tl:
        if t[0] == 'l': v += t[2] * x[t[1]]
        elif t[0] == 'q': v += t[3] * x[t[1]] * x[t[2]]
        else: v += ev(t[1], x, ang)
    return v

P = load('powerflow0030p'); R = load('powerflow0030r')
nb, nf, ng = 30, 164, 12
random.seed(2026)
for trial in range(2):
    V = [F(random.randint(900, 1100), 1000) for _ in range(nb)]
    tt = [F(0)] + [F(random.randint(-300, 300), 1000) for _ in range(nb - 1)]
    cs = [((1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)) for t in tt]
    flows = [F(random.randint(-2000, 2000), 997) for _ in range(nf)]
    gens = [F(random.randint(0, 1000), 991) for _ in range(ng)]
    xp = {}; xr = {}; ang = {}
    for i in range(nb):
        xp[i] = V[i]; ang[194 + i] = Ang(*cs[i]); xp[194 + i] = None
        xr[164 + i] = V[i] * cs[i][0]; xr[194 + i] = -V[i] * cs[i][1]
    for k in range(nf): xp[30 + k] = flows[k]; xr[k] = flows[k]
    for g in range(ng): xp[224 + g] = gens[g]; xr[224 + g] = gens[g]
    # polar: the reference-angle row 'th_1 = 0' is linear in an angle variable; evaluate angles as 0-offset
    xp_lin = dict(xp); 
    for i in range(nb): xp_lin[194 + i] = tt[i]  # only used for rows linear in angles (ref row, angle rows)
    def pbody(tl):
        if all(t[0] == 'l' for t in tl) and any(194 <= t[1] < 224 for t in tl):
            return ('angle-linear', tuple(sorted((t[1], t[2]) for t in tl)))
        return body(tl, xp, ang)
    vp = [(pbody(tl), lb, ub) for tl, (lb, ub) in zip(P[1], P[0])]
    vr = [(body(tl, xr, {}), lb, ub) for tl, (lb, ub) in zip(R[1], R[0])]
    objp = body(P[2], xp, ang); objr = body(R[2], xr, {})
    pool = Counter(vp)
    unmatched = []
    for item in vr:
        if pool[item] > 0: pool[item] -= 1
        else: unmatched.append(item)
    # voltage rows: rect u^2+w^2 in [lb, ub] vs polar V_i in [sqrt lb, sqrt ub]
    vmatched = 0; bad = []
    sq = {F(9025, 10000): F(95, 100), F(11025, 10000): F(105, 100), F(121, 100): F(11, 10)}
    for val, lb, ub in unmatched:
        cand = [i for i in range(nb) if V[i] * V[i] == val]
        ok = False
        for i in cand:
            key = (V[i], sq.get(lb) if lb is not None else None, sq.get(ub) if ub is not None else None)
            if (lb is None or lb in sq) and (ub is None or ub in sq) and pool[key] > 0:
                pool[key] -= 1; ok = True; vmatched += 1; break
        if not ok: bad.append((val, lb, ub))
    left = [k for k, c in pool.items() for _ in range(c)]
    kinds = Counter((k[0][0] if isinstance(k[0], tuple) else 'value') for k in left)
    angle_left = [k for k in left if isinstance(k[0], tuple)]
    angle_ok = all(len(k[0][1]) == 2 and sorted(c for _, c in k[0][1]) == [-1, 1] and (k[1], k[2]) in ((F(-26, 100), None), (None, F(26, 100))) for k in angle_left)
    ref = [k for k in angle_left if len(k[0][1]) == 1]
    print('trial %d: objective equal: %s; rect rows %d, matched exactly %d, voltage rows matched via V^2: %d, unmatched rect rows: %d'
          % (trial, objp == objr, len(vr), len(vr) - len(unmatched), vmatched, len(bad)))
    print('   polar rows left: %d (%s); all are +-0.26 angle-difference rows: %s' % (len(left), dict(kinds), angle_ok and len(angle_left) == len(left)))
    # diagnose: nearest polar 'value' row for each unmatched rect row
    lv = [k for k in left if not isinstance(k[0], tuple)]
    diffs = []
    for val, lb, ub in bad:
        best = min(lv, key=lambda k: abs(k[0] - val)) if lv else None
        if best is not None: diffs.append((abs(best[0] - val), (lb, ub) == (best[1], best[2])))
    diffs.sort()
    if diffs:
        print('   unmatched rect rows: nearest polar row |diff| min %.3e max %.3e; same bounds: %d/%d' % (float(diffs[0][0]), float(diffs[-1][0]), sum(d[1] for d in diffs), len(diffs)))
    big = [d for d in diffs if d[0] > F(1, 10**12)]
    print('   diffs > 1e-12: %d (the rect reference row w_1 = 0 has no polar value-row counterpart); largest of the rest: %.3e'
          % (len(big), float(max(d[0] for d in diffs if d[0] <= F(1, 10**12)))))
# coefficient-level example: polar -1.86832740213523 vs rect 2 x 0.934163701067616
print('example coefficient: polar 1.86832740213523 vs 2*0.934163701067616 =', 2 * F('0.934163701067616'), '; equal:', 2 * F('0.934163701067616') == F('1.86832740213523'))
