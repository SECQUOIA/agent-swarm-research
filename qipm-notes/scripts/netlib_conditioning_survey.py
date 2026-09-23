"""Empirical survey: central-path conditioning exponents on small Netlib instances.

For each instance: log-barrier central path, fit kappa(g) ~ g^{-alpha} on the tail,
report cluster count and CG iterations at the smallest mu. Chord law predicts
alpha in {0, 1, 1.5, 2} universality classes (vertex / quadratic growth /
singularity-degree-2 / positive-dim face).
"""
import numpy as np, sys
sys.path.insert(0, '/home/sgusev/repo/qipm')
from pathlib import Path
from standard_form import load_standard_form
from scipy.optimize import linprog
import scipy.linalg as sla

rng = np.random.default_rng(2)
CACHE = Path('/home/sgusev/repo/qipm/cache_dir/netlib')

def survey(name, max_dim=260):
    c, b, A, off = load_standard_form(CACHE/name/f'{name}.std')
    A = A.toarray(); m, n = A.shape
    if n > max_dim: return None
    r = np.linalg.matrix_rank(A)
    if r < m:
        Q, R, P = sla.qr(A.T, pivoting=True)
        keep = sorted(P[:r]); A = A[keep]; b = b[keep]; m = r
    res = linprog(np.r_[np.zeros(n), -1.0], A_eq=np.c_[A, np.zeros(m)], b_eq=b,
                  A_ub=np.c_[-np.eye(n), np.ones(n)], b_ub=np.zeros(n),
                  bounds=[(None,None)]*n + [(None, 1.0)], method='highs')
    if res.status != 0 or res.x is None or res.x[n] <= 1e-9: return None
    x = res.x[:n]
    res2 = linprog(c, A_eq=A, b_eq=b, bounds=[(0,None)]*n, method='highs')
    if res2.status != 0: return None
    OPT = res2.fun
    _,_,Vt = np.linalg.svd(A); Z = Vt[m:].T
    scale = max(1.0, abs(c@x - OPT))
    rows = []
    for mu in scale*np.array([1e-2,1e-3,1e-4,1e-5,1e-6,1e-7]):
        ok = True
        for _ in range(800):
            g = Z.T@(c - mu/x); H = Z.T@np.diag(mu/x**2)@Z
            try: d = np.linalg.solve(H,-g)
            except np.linalg.LinAlgError: ok=False; break
            lam = np.sqrt(max(d@H@d,0)); step = 1.0 if lam<0.25 else 1/(1+lam)
            while np.any(x+step*(Z@d)<=0): step*=0.5
            x = x+step*(Z@d)
            if lam<1e-10: break
        if not ok: break
        H = Z.T@np.diag(1/x**2)@Z
        w = np.linalg.eigvalsh(H)
        gap = c@x - OPT
        if gap <= 0: break
        rows.append((gap, w[-1]/w[0], w))
    if len(rows) < 3: return None
    gaps = np.log10([r[0] for r in rows[-4:]]); ks = np.log10([r[1] for r in rows[-4:]])
    alpha = -np.polyfit(gaps, ks, 1)[0]
    # cluster count at last point: split eigenvalues by gaps > 10x in log scale
    w = rows[-1][2]
    lw = np.log10(w); splits = np.sum(np.diff(lw) > 1.0) + 1
    # CG at last point
    H = Z.T@np.diag(1/x**2)@Z
    bb = rng.standard_normal(n-m); bb/=np.linalg.norm(bb)
    xk = np.zeros(n-m); rr = bb.copy(); p = rr.copy(); rs = rr@rr; it=0
    while np.sqrt(rs) > 1e-8 and it < 4000:
        Hp = H@p; al = rs/(p@Hp); xk+=al*p; rr-=al*Hp
        rsn = rr@rr; p = rr + (rsn/rs)*p; rs = rsn; it+=1
    return (name, m, n, alpha, rows[-1][1], splits, it)

names = sorted(p.name for p in CACHE.iterdir() if p.is_dir())
print(f"{'instance':>10} {'m':>4} {'n':>4} {'alpha':>6} {'kappa_end':>10} {'#clust':>6} {'CGits':>6}")
done = 0
for name in names:
    try:
        r = survey(name)
    except Exception:
        r = None
    if r:
        print(f"{r[0]:>10} {r[1]:>4} {r[2]:>4} {r[3]:>6.2f} {r[4]:>10.2e} {r[5]:>6} {r[6]:>6}")
        done += 1
    if done >= 14: break
