"""Exp 7: squared Euclidean lengths. Conjectured bound OPT <= K_max * REL_hull with
K_e = sec^2(theta_e) * (M_e+m_e)^2/(4 M_e m_e), m_e/M_e = min/max |w| over X_v - X_u."""
import numpy as np
from gcs import *
from exp2_aperture import make

def K_edge(I, u, v):
    Su, Sv = I.sets[u], I.sets[v]
    cu, cv = np.asarray(Su[1], float), np.asarray(Sv[1], float)
    rr = (Su[2] if Su[0]=='ball' else 0) + (Sv[2] if Sv[0]=='ball' else 0)
    dd = np.linalg.norm(cv - cu)
    if rr >= dd: return np.inf
    m, M = dd - rr, dd + rr
    return (1/np.cos(np.arcsin(rr/dd)))**2 * (M + m)**2/(4*M*m)

rng = np.random.default_rng(11)
worst = []
for trial in range(40):
    I = make(rng, L=rng.integers(2, 5), k=rng.integers(2, 4), d=int(rng.choice([2, 3])), D=3.0,
             spread=float(rng.choice([1.0, 2.0, 4.0])), rmax=float(rng.choice([0.5, 1.0])), skip=0.4)
    I.norm = 'sq'
    Kmax = max(K_edge(I, u, v) for u, v in I.edges)
    if not np.isfinite(Kmax): continue
    r = relax(I); rh = relax(I, hull=True); o = exact(I)
    worst.append(((o/rh - 1)/(Kmax - 1), o/r, o/rh, Kmax))
    if o > Kmax*rh*(1 + 1e-6): print("VIOLATION", o, rh, Kmax)
w = np.array(worst)
print(f"n={len(w)} max OPT/REL={w[:,1].max():.4f} max OPT/REL_hull={w[:,2].max():.4f} max excess ratio={w[:,0].max():.3f} median K_max={np.median(w[:,3]):.3f}")
print("fraction exact basic:", np.mean(w[:,1] < 1+1e-5), " hull:", np.mean(w[:,2] < 1+1e-5))
