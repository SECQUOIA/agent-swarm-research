"""Compare two GAMS scalar models (as written by GAMS Convert) by evaluating
all equations at random points in 40-digit arithmetic and comparing bounds.
Evidence of model identity, not a proof. Usage: compare_gms.py a.gms b.gms [npts]"""
import re, sys, random
from mpmath import mp, mpf, log, exp, sqrt, cos, sin
mp.dps = 40

def parse(path):
    t = open(path).read()
    t = re.sub(r'(?m)^\*.*$', '', t)          # full-line comments only
    t = re.sub(r'(?m)^\$.*$', '', t)
    eqs = {}
    for m in re.finditer(r'(?m)^(e\d+)\.\.(.*?);', t, re.S):
        body = ' '.join(m.group(2).split())
        mm = re.match(r'(.*)=([EGLN])=(.*)', body)
        eqs[m.group(1)] = (mm.group(1), mm.group(2), mm.group(3))
    bnd = {}
    for m in re.finditer(r'(\w+)\.(lo|up|fx)\s*=\s*([-+0-9.eE]+)\s*;', t):
        bnd.setdefault(m.group(1), {})[m.group(2)] = mpf(m.group(3))
    pos = set()
    for m in re.finditer(r'Positive Variables(.*?);', t, re.S):
        pos |= set(v.strip() for v in m.group(1).replace('\n', ' ').split(',') if v.strip())
    var = set()
    for m in re.finditer(r'(?m)^\s*Variables(.*?);', t, re.S):
        var |= set(v.strip() for v in m.group(1).replace('\n', ' ').split(',') if v.strip())
    for m in re.finditer(r'(?m)^\s*(?:Integer|Binary) Variables(.*?);', t, re.S):
        var |= set(v.strip() for v in m.group(1).replace('\n', ' ').split(',') if v.strip())
    return eqs, bnd, pos, var

def pyexpr(s):
    s = s.replace('**', '^').replace('^', '**')
    s = re.sub(r'\bsqr\s*\(', 'SQR(', s)
    s = re.sub(r'\bpower\s*\(', 'POW(', s)
    s = re.sub(r'\bvcpower\s*\(', 'POW(', s)
    s = re.sub(r'\bcvpower\s*\(', 'POW(', s)
    return s

def ev(s, x):
    env = dict(x); env.update(log=log, exp=exp, sqrt=sqrt, cos=cos, sin=sin,
               SQR=lambda a: a*a, POW=lambda a, b: a**b, mpf=mpf)
    s = re.sub(r'(?<![\w.])(\d+\.?\d*(?:[eE][-+]?\d+)?)', r"mpf('\1')", pyexpr(s))
    return eval(s, {'__builtins__': {}}, env)

def resid(eq, x):
    l, k, r = eq
    return ev(l, x) - ev(r, x), k

a, b = sys.argv[1], sys.argv[2]
npts = int(sys.argv[3]) if len(sys.argv) > 3 else 20
A, B = parse(a), parse(b)
print('equations', len(A[0]), len(B[0]), 'same names:', set(A[0]) == set(B[0]))
print('variables', len(A[3]), len(B[3]), 'same:', A[3] == B[3])
print('positive-var sets equal:', A[2] == B[2], ' diff A-B', sorted(A[2]-B[2]), ' B-A', sorted(B[2]-A[2]))
bd = {v for v in set(A[1]) | set(B[1]) if A[1].get(v) != B[1].get(v)}
print('variables with differing explicit bounds:', sorted(bd)[:20])
for v in sorted(bd)[:10]: print('   ', v, A[1].get(v), B[1].get(v))
random.seed(1)
def box(v):
    lo = A[1].get(v, {}).get('lo', mpf(0) if v in A[2] else mpf(-5))
    up = A[1].get(v, {}).get('up', lo + 10)
    if 'fx' in A[1].get(v, {}): return A[1][v]['fx']
    return lo + (up - lo) * mpf(random.random()) if up > lo else lo
worst = mpf(0)
for _ in range(npts):
    x = {v: box(v) for v in A[3]}
    for v in list(x):
        if x[v] == 0: x[v] = mpf('1e-3')
    for e in A[0]:
        try:
            ra, ka = resid(A[0][e], x); rb, kb = resid(B[0][e], x)
        except ZeroDivisionError:
            continue
        assert ka == kb, (e, ka, kb)
        d = abs(ra - rb) / (1 + abs(ra))
        if d > worst: worst, we = d, e
print('max relative difference of equation residuals over', npts, 'points:', mp.nstr(worst, 5), '' if worst == 0 else we)
