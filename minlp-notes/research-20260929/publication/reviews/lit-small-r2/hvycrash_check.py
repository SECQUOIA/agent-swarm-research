"""Reviewer r2 (lit-small): independent checks of the hvycrash provenance claims.

1. Decode the BOUNDS section of HVYCRASH.SIF (both versions) by applying the
   bound cards in file order (SIFDecode rule: a later individual card overwrites
   an earlier one). Default after 'FR DEFAULT' is free.
2. Compare with the AMPL file hvycrash.mod bounds (N = 50).
3. Evaluate the SIF rows C(1,T), C(2,T), C(3,T) at N = 50, as transcribed by hand
   from GROUPS / ELEMENT USES / GROUP USES / ELEMENTS, and compare them with the
   rows of the cached MINLPLib OSIL at random points (mpmath, 50 digits).
   Variable map (read from hvycrash.gms): theta_T = x_T (T=1..50), theta_0 = x101,
   U(T) = x_{50+T}, X(2,T) = x_{101+T}, X(1,T) = x_{202-T} (T=1..50); X(1,0)=0.
Numerical evidence only, except part 1 (pure card bookkeeping, no arithmetic).
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])
_PUBLIC_HOME = str(_PublicPath.home())

import re, sys, random
sys.path.insert(0, (_PUBLIC_REPO + '/research-20260929/publication/reviews/lit-small-r1'))
from mpmath import mp, mpf, cos
SRC = (_PUBLIC_REPO + '/research-20260929/publication/literature/small/sources/hvycrash/')
INF = float('inf')

def decode_bounds(path, N):
    lines = open(path).read().split('\n')
    i0 = lines.index('BOUNDS'); i1 = lines.index('START POINT')
    body = [l for l in lines[i0 + 1:i1] if l.strip() and not l.startswith('*')]
    names = [f'X({k},{t})' for t in range(N + 1) for k in (1, 2, 3)] + [f'U({t})' for t in range(N + 1)]
    lb = {v: 0.0 for v in names}; ub = {v: INF for v in names}   # SIF default before FR
    env = {'N': N}
    def idx(s):
        s = s.strip()
        return int(s) if re.fullmatch(r'-?\d+', s) else env[s]
    def var(tok):
        m = re.fullmatch(r'(\w+)\(([^)]*)\)', tok)
        return f"{m.group(1)}({','.join(str(idx(a)) for a in m.group(2).split(','))})"
    def run(block):
        k = 0
        while k < len(block):
            l = block[k]; f = l.split()
            if f[0] == 'DO':
                depth = 1; j = k + 1
                while depth:
                    g = block[j].split()[0]
                    depth += (g == 'DO') - (g in ('OD', 'ND')); j += 1
                for t in range(idx(f[2]), idx(f[3]) + 1):
                    env[f[1]] = t; run(block[k + 1:j - 1])
                k = j; continue
            if f[0] == 'FR' and f[2] == "'DEFAULT'":
                for v in names: lb[v] = -INF; ub[v] = INF
            elif f[0] in ('XX', 'XL', 'XU', 'FR', 'MI', 'PL'):
                v = var(f[2])
                if f[0] == 'XX': lb[v] = ub[v] = float(f[3])
                elif f[0] == 'XL': lb[v] = float(f[3])
                elif f[0] == 'XU': ub[v] = float(f[3])
                elif f[0] == 'FR': lb[v] = -INF; ub[v] = INF
                else: raise ValueError(l)
            else:
                raise ValueError('unhandled card: ' + l)
            k += 1
    run(body)
    return names, lb, ub

def summarize(names, lb, ub):
    fixed = [v for v in names if lb[v] == ub[v]]
    th = [(lb[v], ub[v]) for v in names if v.startswith('X(3,')]
    return fixed, sorted(set(th))

for fn in ('HVYCRASH.SIF', 'HVYCRASH_2013_a4c9117d7d.SIF'):
    for N in (50, 1000):
        names, lb, ub = decode_bounds(SRC + fn, N)
        fixed, th = summarize(names, lb, ub)
        print(fn, 'N', N, 'nvars', len(names), 'fixed', [(v, lb[v]) for v in fixed], 'theta bound sets', th)

# AMPL bounds (N = 50)
names, lb, ub = decode_bounds(SRC + 'HVYCRASH.SIF', 50)
amap = {}
for l in open(SRC + 'hvycrash.mod'):
    m = re.match(r'var (x(\d)_(\d+)|u(\d+))\s*(.*);', l)
    if not m: continue
    v = f'X({m.group(2)},{m.group(3)})' if m.group(2) else f'U({m.group(4)})'
    lo = re.search(r'>=\s*([-\d.eE]+)', m.group(5)); hi = re.search(r'<=\s*([-\d.eE]+)', m.group(5))
    amap[v] = (float(lo.group(1)) if lo else -INF, float(hi.group(1)) if hi else INF)
diff = [v for v in names if amap.get(v) != (lb[v], ub[v])]
print('AMPL vars', len(amap), 'SIF vs AMPL bound differences:', diff[:10], len(diff))

# Row comparison SIF (hand transcription) vs OSIL
from osil_eval import Model
mp.dps = 50
M = Model((_PUBLIC_HOME + '/.cache/minlplib/minlplib/osil/hvycrash.osil'))
print('OSIL n', M.n, 'm', M.m, 'objective coef', M.obj_lin)
N = 50; TT = mpf('0.2185'); H = TT / N; EPS = mpf('0.1'); A = mpf('1.62079')
def C(u): return mpf('0.01') + mpf('0.3') * u * u
def sif_rows(X1, X2, X3, U):
    rows = []
    for T in range(1, N + 1):
        th, r, u = X3[T], X2[T], U[T]
        E1 = cos(th) / (A * C(u) * r * r)
        E2 = 1 / r
        E3 = cos(th) / (A * C(u) * r ** 3)
        E4 = u / (C(u) * r * r)
        E5 = cos(th) / (A * C(u) * r ** 4)
        rows.append(X1[T - 1] - X1[T] + H * E1)
        rows.append(-E2 - E3)
        rows.append(EPS * X3[T - 1] - EPS * X3[T] + H * E4 - H * E5)
    return rows
random.seed(2026)
worst = mpf(0); worst_rel = mpf(0); signs = set()
for trial in range(20):
    X1 = [mpf(0)] + [mpf(random.uniform(-1, 1)) for _ in range(N)]
    X2 = [mpf('2.19905')] + [mpf(random.choice((-1, 1)) * random.uniform(0.3, 3)) for _ in range(N)]
    X3 = [mpf(random.uniform(0, 6.2831854)) for _ in range(N + 1)]
    U = [None] + [mpf(random.uniform(0.08, 0.417)) for _ in range(N)]
    x = [mpf(0)] * M.n
    for T in range(1, N + 1):
        x[T - 1] = X3[T]; x[50 + T - 1] = U[T]; x[101 + T - 1] = X2[T]; x[202 - T - 1] = X1[T]
    x[100] = X3[0]
    s = sif_rows(X1, X2, X3, U)
    for r in range(M.m):
        b = M.body(r, x) - (mpf(M.cons[r]['lb']) if M.cons[r]['lb'] not in ('-INF',) else 0)
        d1 = abs(b - s[r]); d2 = abs(b + s[r])
        sg = '+' if d1 <= d2 else '-'
        signs.add(sg); d = min(d1, d2)
        worst = max(worst, d); worst_rel = max(worst_rel, d / max(1, abs(s[r])))
    if trial == 0:
        print('objective at trial 0:', M.objective(x), 'X1[50] =', X1[50])
print('row comparison, 20 random points x 150 rows: max abs diff', mp.nstr(worst, 5), 'max rel diff', mp.nstr(worst_rel, 5), 'sign(s) used', signs)
print('OSIL row bounds:', set((c['lb'], c['ub']) for c in M.cons))
