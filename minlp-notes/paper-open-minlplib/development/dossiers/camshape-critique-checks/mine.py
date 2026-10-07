"""Critic's independent camshape check: regex OSIL parser, exact rationals for S/U,
exact Fraction envelope for small n, and a directed-rounding fixed-point enclosure for all n."""
import re, sys, json
from fractions import Fraction as Fr
sys.set_int_max_str_digits(0)

def expand(block):
    out = []
    for m in re.finditer(r'<el(?P<attr>[^>]*)>(?P<v>[^<]+)</el>', block):
        attr = m.group('attr'); v = m.group('v').strip()
        mult = re.search(r'mult="(\d+)"', attr); incr = re.search(r'incr="([^"]+)"', attr)
        k = int(mult.group(1)) if mult else 1
        for t in range(k):
            out.append(Fr(v) + (Fr(incr.group(1)) * t if incr else 0))
    return out

def parse(path):
    s = open(path).read()
    assert 'nonlinearExpressions' not in s
    vars_ = re.findall(r'<var ([^/]*)/>', s)
    def att(a, k):
        m = re.search(k + r'="([^"]+)"', a); return m.group(1) if m else None
    V = []
    for a in vars_:
        lb = att(a, 'lb'); ub = att(a, 'ub')
        assert att(a, 'type') in (None, 'C')
        V.append((None if lb == '-INF' else Fr(lb if lb is not None else '0'),
                  None if (ub is None or ub == 'INF') else Fr(ub)))
    cons = re.findall(r'<con ([^/]*)/>', s)
    C = []
    for a in cons:
        lb = att(a, 'lb'); ub = att(a, 'ub')
        assert att(a, 'constant') is None
        C.append((att(a, 'name'), None if lb is None else Fr(lb), None if ub is None else Fr(ub)))
    obj = s[s.find('<objectives'):s.find('</objectives>')]
    assert 'constant=' not in obj and obj.count('<obj ') == 1 and 'maxOrMin="min"' in obj
    ocoef = {int(i): Fr(v) for i, v in re.findall(r'<coef idx="(\d+)">([^<]+)</coef>', obj)}
    L = s[s.find('<linearConstraintCoefficients'):s.find('</linearConstraintCoefficients>')]
    start = [int(x) for x in expand(L[L.find('<start>'):L.find('</start>')])]
    col = [int(x) for x in expand(L[L.find('<colIdx>'):L.find('</colIdx>')])]
    val = expand(L[L.find('<value>'):L.find('</value>')])
    assert len(start) == len(C) + 1 and start[-1] == len(col) == len(val)
    lin = [dict() for _ in C]
    for i in range(len(C)):
        for k in range(start[i], start[i + 1]):
            assert col[k] not in lin[i]; lin[i][col[k]] = val[k]
    quad = [dict() for _ in C]
    for i, a, b, v in re.findall(r'<qTerm idx="(-?\d+)" idxOne="(\d+)" idxTwo="(\d+)" coef="([^"]+)"/>', s):
        i = int(i); a, b = sorted((int(a), int(b)))
        assert i >= 0 and (a, b) not in quad[i]; quad[i][(a, b)] = Fr(v)
    nq = int(re.search(r'numberOfQuadraticTerms="(\d+)"', s).group(1))
    assert sum(len(q) for q in quad) == nq
    return V, C, ocoef, lin, quad

def structure(path, n):
    V, C, oc, lin, quad = parse(path)
    assert len(V) == 2 * n - 1 and len(C) == 2 * n
    assert set(oc) == set(range(n)) and len(set(oc.values())) == 1
    c0 = -oc[0]
    c = quad[0][(0, 2)]
    for j in range(2, n):   # G_j rows 0..n-3
        i = j - 2; a, b, d = j - 2, j - 1, j
        assert lin[i] == {} and quad[i] == {(a, b): -1, (a, d): c, (b, d): -1}
        assert C[i][1] is None and C[i][2] == 0 and C[i][0] == f'e{j}'
    i = n - 2; assert lin[i] == {0: -1, 1: c} and quad[i] == {(0, 1): -1} and C[i][1] is None and C[i][2] == 0
    i = n - 1; c2 = lin[i][n - 2]; assert lin[i] == {n - 2: c2, n - 1: -2} and quad[i] == {(n - 2, n - 1): -1} and C[i][2] == 0 and C[i][1] is None
    i = n; assert lin[i] == {n - 1: -4} and quad[i] == {(n - 1, n - 1): c} and C[i][2] == 0 and C[i][1] is None
    for k in range(1, n):
        i = n + k; assert lin[i] == {k - 1: 1, k: -1, n + k - 1: 1} and quad[i] == {} and C[i][1] == 0 and C[i][2] == 0
    ub1 = V[0][1]; assert V[0][0] == 1
    for j in range(1, n - 1): assert V[j] == (1, 2)
    lbn = V[n - 1][0]; assert V[n - 1][1] == 2
    assert V[n] == (None, None)
    al = V[n + 1][1]
    for k in range(n + 1, 2 * n - 1): assert V[k] == (-al, al)
    return dict(c0=c0, c=c, c2=c2, ub1=ub1, lbn=lbn, alpha=al)

def envelope_exact(K, n):
    c, ub1, al = K['c'], K['ub1'], K['alpha']
    U = [Fr(1), c]
    while len(U) < n: U.append(c * U[-1] - U[-2])
    S = [Fr(1), 1 / ub1]
    while len(S) < n + 1: S.append(c * S[-1] - S[-2])
    B = [None] + [min(1 / S[j], 2 if j > 1 else ub1) if S[j] > 0 else (2 if j > 1 else ub1) for j in range(1, n + 1)]
    E = [None, B[1]] + [min(B[k] + al * abs(j - k) for k in range(2, n + 1)) for j in range(2, n + 1)]
    return U, S, B, E

def enclosure(K, n, P=10**120):
    """directed-rounding fixed point: integers scaled by P. Returns (lo, hi) for sum E."""
    c, ub1, al = K['c'], K['ub1'], K['alpha']
    S = [Fr(1), 1 / ub1]
    while len(S) < n + 1: S.append(c * S[-1] - S[-2])
    assert all(s > 0 for s in S[1:])
    def fl(q): return (q.numerator * P) // q.denominator
    def ce(q): return -((-q.numerator * P) // q.denominator)
    Blo = [None]; Bhi = [None]
    for j in range(1, n + 1):
        cap = ub1 if j == 1 else Fr(2)
        R = 1 / S[j]
        Blo.append(min(fl(R), fl(cap))); Bhi.append(min(ce(R), ce(cap)))
    alo, ahi = fl(al), ce(al)
    def env(B, a):
        F = B[:]
        for j in range(3, n + 1): F[j] = min(F[j], F[j - 1] + a)
        for j in range(n - 1, 1, -1): F[j] = min(F[j], F[j + 1] + a)
        return F
    Elo = env(Blo, alo); Ehi = env(Bhi, ahi)
    return Fr(sum(Elo[1:]), P), Fr(sum(Ehi[1:]), P), Elo, Ehi

def digits(q, d, up=False):
    s = 10 ** d
    v = -((-q.numerator * s) // q.denominator) if up else (q.numerator * s) // q.denominator
    sg = '-' if v < 0 else ''; v = abs(v)
    return f"{sg}{v // s}.{str(v % s).zfill(d)}"

if __name__ == '__main__':
    for n in map(int, sys.argv[1:]):
        K = structure(f'camshape{n}.osil', n)
        slo, shi, Elo, Ehi = enclosure(K, n)
        vlo = -K['c0'] * shi; vhi = -K['c0'] * slo
        rec = dict(n=n, K={k: str(v) for k, v in K.items()}, v_lo30=digits(vlo, 30), v_hi30=digits(vhi, 30, True),
                   width=float(vhi - vlo), floor14=digits(vlo, 14), ceil14=digits(vhi, 14, True))
        print(json.dumps(rec), flush=True)
