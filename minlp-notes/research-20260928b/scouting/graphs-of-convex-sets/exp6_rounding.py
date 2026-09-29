"""Exp 6: pair-point (lambda-driven) randomized rounding from the vertex-hull relaxation.
Checks  OPT <= E[rounded cost] <= sum_e kappa_e * ytilde-cost_e <= kappa_max * REL_hull
exactly (expectation computed in closed form), on random 2D ball DAGs with sizeable
balls (gaps present) plus the fork gadget.  Also samples paths and re-optimises positions."""
import numpy as np
from gcs import *
from exp2_aperture import make, aperture
from exp4_forkgadget import gadget

def g(w): return np.linalg.norm(w)

def kappa_edge(I, u, v):
    Su, Sv = I.sets[u], I.sets[v]
    cu, cv = np.asarray(Su[1], float), np.asarray(Sv[1], float)
    rr = (Su[2] if Su[0]=='ball' else 0) + (Sv[2] if Sv[0]=='ball' else 0)
    dd = np.linalg.norm(cv - cu)
    return np.inf if rr >= dd else 1/np.cos(np.arcsin(rr/dd))

def analyse(I):
    rh, sol = relax(I, hull=True, return_sol=True)
    y, z, zp, pair = sol['y'], sol['z'], sol['zp'], sol['pair']
    s, t = I.s, I.t
    Ecost, kbound = 0.0, 0.0
    for e in I.edges:
        if y[e] < 1e-9: continue
        u, v = e
        # tail distribution of x_u given e
        if u == s: tails = [(1.0, z[e]/y[e])]
        else: tails = [(pair[(d,e)][0]/y[e], pair[(d,e)][1]/max(pair[(d,e)][0],1e-300)) for d in I.inn[u] if pair[(d,e)][0] > 1e-10]
        if v == t: heads = [(1.0, zp[e]/y[e])]
        else: heads = [(pair[(e,f)][0]/y[e], pair[(e,f)][1]/max(pair[(e,f)][0],1e-300)) for f in I.out[v] if pair[(e,f)][0] > 1e-10]
        Ecost += y[e]*sum(pt*ph*g(xh - xt) for pt, xt in tails for ph, xh in heads)
        kbound += kappa_edge(I, u, v)*g(zp[e] - z[e])
    return rh, Ecost, kbound

rng = np.random.default_rng(7)
viol = 0
for trial in range(40):
    I = make(rng, L=rng.integers(2, 4), k=rng.integers(2, 4), d=2, D=3.0, spread=rng.choice([0.5, 1.0, 2.0]), rmax=1.4, skip=0.3)
    kmax = max(kappa_edge(I, u, v) for u, v in I.edges)
    if not np.isfinite(kmax): continue
    rh, Ec, kb = analyse(I); o = exact(I)
    ok = (o <= Ec + 1e-6) and (Ec <= kb + 1e-6) and (kb <= kmax*rh + 1e-6)
    viol += (not ok)
    if Ec - rh > 1e-6 or not ok:
        print(f"REL_H={rh:.5f} OPT={o:.5f} E[round]={Ec:.5f} sum-kappa={kb:.5f} kmax*REL_H={kmax*rh:.5f} ok={ok}")
print("violations:", viol)
I = gadget(4.8, 0.61, 1.5, 4.6)
rh, Ec, kb = analyse(I); o = exact(I)
print(f"gadget: REL_H={rh:.5f} OPT={o:.5f} E[round]={Ec:.5f} sum-kappa={kb:.5f}")
