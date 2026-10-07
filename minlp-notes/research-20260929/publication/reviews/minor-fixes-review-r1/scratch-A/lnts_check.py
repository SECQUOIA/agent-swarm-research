"""Group A independent lnts check: own closed-form F, own 2-step Krawczyk (step 2 centred at
the midpoint of the step-1 box), objective width, gaps, display validity, old-vector distances,
middle control. Does not import any track code."""
import json, random
from fractions import Fraction as Q
from pathlib import Path
from mpmath import iv, mp
from mpmath.libmp import to_rational
ROOT = Path(__file__).resolve().parents[4]   # research-20260929
LN = ROOT/'publication/primal/lnts'
mp.dps = iv.dps = 110

def ivq(q):
    q = Q(q); return iv.mpf(q.numerator)/iv.mpf(q.denominator)
def ends(x):
    a, b = x._mpi_; return Q(*to_rational(a)), Q(*to_rational(b))
def box(lo, hi):  # outward enclosure of rational [lo, hi]
    return iv.mpf([ivq(lo).a, ivq(hi).b])
def up(q, sig):
    e = 0
    while q >= Q(10)**(e+1): e += 1
    while q < Q(10)**e: e -= 1
    s = Q(10)**(e-sig+1); m = -((-q)//s); return f"{m}e{e-sig+1}"

def coeffs(N):
    w = [1] + [2]*(N-1) + [1]
    # T_i = sum_j a[i][j] s_j  (vy_i = 50 h T_i);  py_N = 25 h^2 sum_j b_j s_j
    T = [[0]*(N+1)]
    for i in range(N):
        r = T[-1][:]; r[i] += 1; r[i+1] += 1; T.append(r)
    b = [sum(T[i][j] + T[i+1][j] for i in range(N)) for j in range(N+1)]
    return w, b

def selftest(N, w, b):  # closed form vs exact recursion, arbitrary rational "sin/cos" values
    rnd = random.Random(N)
    s = [Q(rnd.randint(-99, 99), 97) for _ in range(N+1)]; c = [Q(rnd.randint(1, 99), 89) for _ in range(N+1)]; h = Q(3, 7)
    px = py = vx = vy = Q(0)
    for i in range(N):
        vx1 = vx + 50*h*(c[i]+c[i+1]); vy1 = vy + 50*h*(s[i]+s[i+1])
        px += h*(vx+vx1)/2; py += h*(vy+vy1)/2; vx, vy = vx1, vy1
    assert vx == 50*h*sum(wj*cj for wj, cj in zip(w, c))
    assert vy == 50*h*sum(wj*sj for wj, sj in zip(w, s))
    assert py == 25*h*h*sum(bj*sj for bj, sj in zip(b, s))

def F_J(th_mid, w, b, z, jac):
    a, bb, h = z; N = len(w)-1
    Cm = sum(2*iv.cos(t) for t in th_mid); Sm = sum(2*iv.sin(t) for t in th_mid)
    Bm = sum(b[j+1]*iv.sin(t) for j, t in enumerate(th_mid))
    C = Cm + iv.cos(a) + iv.cos(bb); S = Sm + iv.sin(a) + iv.sin(bb); B = Bm + b[0]*iv.sin(a) + b[N]*iv.sin(bb)
    F = [50*h*C - 45, 50*h*S, 25*h*h*B - 5]
    if not jac: return F
    J = [[-50*h*iv.sin(a), -50*h*iv.sin(bb), 50*C],
         [50*h*iv.cos(a), 50*h*iv.cos(bb), 50*S],
         [25*h*h*b[0]*iv.cos(a), 25*h*h*b[N]*iv.cos(bb), 50*h*B]]
    return F, J

def kraw(th_mid, w, b, y, X):
    Fy = F_J(th_mid, w, b, y, False); _, J = F_J(th_mid, w, b, X, True)
    M = mp.matrix([[mp.mpf((J[i][j].a + J[i][j].b).a)/2 for j in range(3)] for i in range(3)])
    Ci = M**-1; C = [[iv.mpf(Ci[i, j]) for j in range(3)] for i in range(3)]
    K = []
    for i in range(3):
        s = y[i] - sum(C[i][k]*Fy[k] for k in range(3))
        for j in range(3):
            s += ((1 if i == j else 0) - sum(C[i][k]*J[k][j] for k in range(3))) * (X[j] - y[j])
        K.append(s)
    return K

summ = json.loads((ROOT/'reviews/open-instances-verification/logs/lnts_verify.json').read_text())
summ = {d['name']: d for d in summ}
sum_dual = {50: '0.5546687649381', 100: '0.5545954011663', 200: '0.5545770161025', 400: '0.5545724137001'}
sum_primal = {50: '0.5546687649387', 100: '0.5545954011669', 200: '0.5545770161031', 400: '0.5545724137007'}
for N in (50, 100, 200, 400):
    v = json.loads((LN/f'points/lnts{N}_point.json').read_text())
    w, b = coeffs(N); selftest(N, w, b)
    fc = v['fixed_controls']; assert list(fc) == [f'x{j+1}' for j in range(1, N)]
    th_mid = [iv.mpf(fc[k]) for k in fc]   # outward enclosure of the decimal string
    ub = v['unknowns_box']; keys = list(ub); assert keys == ['x1', f'x{N+1}', f'x{5*N+7}'], keys  # OSIL names skip x{5N+6} (GAMS objvar)
    cen = [Q(ub[k]['centre']) for k in keys]; rad = [Q(ub[k]['radius']) for k in keys]
    X = [box(cen[k]-rad[k], cen[k]+rad[k]) for k in range(3)]
    Y = [ivq(c) for c in cen]
    K = kraw(th_mid, w, b, Y, X)
    ok1 = all(ends(X[k])[0] < ends(K[k])[0] and ends(K[k])[1] < ends(X[k])[1] for k in range(3))
    Z = [iv.mpf([K[k].a, K[k].b]) for k in range(3)]  # K inside X, so Z = K
    old_in = all(ends(Z[k])[0] <= cen[k] <= ends(Z[k])[1] for k in range(3))
    mids = [(ends(z)[0]+ends(z)[1])/2 for z in Z]; Y2 = [ivq(m) for m in mids]
    assert all(ends(Z[k])[0] <= ends(Y2[k])[0] and ends(Y2[k])[1] <= ends(Z[k])[1] for k in range(3))
    K2 = kraw(th_mid, w, b, Y2, Z)
    Z2 = [(max(ends(K2[k])[0], ends(Z[k])[0]), min(ends(K2[k])[1], ends(Z[k])[1])) for k in range(3)]
    wid = [hi-lo for lo, hi in Z2]; ow = N*wid[2]
    objlo, objhi = N*Z2[2][0], N*Z2[2][1]
    so = [Q(x) for x in v['objective_enclosure']]
    print(f'lnts{N}: step1 K in int X: {ok1}; stored centre in Z1: {old_in}; Z1 widths {[float(e[1]-e[0]) for e in map(ends, Z)]}')
    print(f'  step2 widths {[float(x) for x in wid]} max<2.1e-106: {max(wid) < Q("2.1e-106")}; objective width {float(ow):.3e} <3e-109: {ow < Q("3e-109")}')
    print(f'  N*h(Z2) inside stored 25-digit objective enclosure: {so[0] <= objlo and objhi <= so[1]}; Z2 inside stored box: {all(cen[k]-rad[k] < Z2[k][0] and Z2[k][1] < cen[k]+rad[k] for k in range(3))}')
    # gaps (use stored 25-digit upper end, as the report does)
    d = summ[f'lnts{N}']['cert_1e-12']; vb = Q(d['bound']); h2N = N*Q(d['h2'])
    sd = Q(sum_dual[N]); sp = Q(sum_primal[N])
    print(f'  verifier bound str {d["bound"]} == repr(float)? {repr(float(d["bound"])) == d["bound"]}; bound<=N*h2: {vb <= h2N}; float(bound)<=N*h2: {Q(float(d["bound"])) <= h2N}')
    print(f'  summary dual {sum_dual[N]} <= verifier bound: {sd <= vb} (and <= float value: {sd <= Q(float(d["bound"]))})')
    print(f'  summary primal {sum_primal[N]} >= objective upper end: {sp >= so[1]}  (display - f_hi = {float(sp - so[1]):.3e})')
    gs, gv = so[1]-sd, so[1]-vb
    print(f'  gap vs summary dual {float(gs):.6e} up3 {up(gs,3)} up2 {up(gs,2)} rel up3 {up(gs/sd,3)}; gap vs verifier {float(gv):.6e} up3 {up(gv,3)} up2 {up(gv,2)} rel up3 {up(gv/vb,3)}')
    # old vector distances
    old = [Q(float(s)) for s in (ROOT/f'open-instances/logs/lnts_lnts{N}_primal.txt').read_text().split()]
    enc = v['enclosures']; assert len(enc) == len(old) == 5*N+6
    dist = [max(abs(o-Q(a)), abs(o-Q(bb))) for o, (_, a, bb) in zip(old, enc)]
    diff = [i for i, (o, (_, a, bb)) in enumerate(zip(old, enc)) if not (float(Q(a)) == float(Q(bb)) == float(o))]
    print(f'  old-vector max distance upper {float(max(dist)):.4e}; coordinates whose double rounding differs from old: {[enc[i][0] for i in diff]}')
    mid = Q(fc[f'x{N//2+1}']); small = [k for k in fc if abs(Q(fc[k])) < Q('1e-50')]
    print(f'  middle control x{N//2+1} = {float(mid):.4e}, |.|<1e-110: {abs(mid) < Q("1e-110")}; tiny controls: {small}; old value there: {old[N//2]}')
