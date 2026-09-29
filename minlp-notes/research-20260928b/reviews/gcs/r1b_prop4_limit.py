"""Prop 4: R^2 (OPT/REL_H - 1) for larger R with tight Clarabel tolerances.
Also Prop B' score at theta = 1..30 deg with exact sec(theta)."""
import numpy as np, cvxpy as cp
import rgcs
from rgcs import *

def solve_tight(prob):
    prob.solve(solver="CLARABEL", tol_gap_abs=1e-12, tol_gap_rel=1e-12, tol_feas=1e-12, max_iter=500)
    return prob.value
rgcs.solve = solve_tight

sq = Poly(np.array([[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]],float), np.array([1,1,1,1,0,0],float),
          np.array([[1,1,0],[1,-1,0],[-1,1,0],[-1,-1,0]],float))
for R in [20, 40, 80, 160, 320]:
    a = R/np.sqrt(2)
    sets = dict(s=Pt([0,0,-R]), u1=Pt([a,a,0]), u2=Pt([-a,-a,0]), v=sq, w1=Pt([a,-a,0]), w2=Pt([-a,a,0]), t=Pt([0,0,R]))
    E = [("s","u1"),("s","u2"),("u1","v"),("u2","v"),("v","w1"),("v","w2"),("w1","t"),("w2","t")]
    g = G(sets, E, "s", "t", L2)
    of = 2*np.sqrt(2)*R + 2*np.sqrt(R*R-np.sqrt(2)*R+1)
    rh = relax(g, hull=True)
    print(f"R={R:4d} OPT(formula)={of:.10f} REL_H={rh:.10f}  R^2(OPT/REL_H-1)={R*R*(of/rh-1):.5f}")

print()
for th_deg in [1, 2, 5, 10, 15, 20, 25, 30, 40]:
    th = np.radians(th_deg); D = 10.0; r = D*np.sin(th)
    sA = np.array([-D,0.0]); ell = np.sqrt(D*D-r*r)
    Pp = sA + 2*ell*np.array([np.cos(th), np.sin(th)]); Pm = sA + 2*ell*np.array([np.cos(th), -np.sin(th)])
    X0 = Pp[0]
    sets = dict(s=Pt(sA), A=Ball([0,0],r), Pp=Pt(Pp), Pm=Pt(Pm), B=Ball([2*X0,0],r), t=Pt([2*X0+D,0]))
    E = [("s","A"),("A","Pp"),("A","Pm"),("Pp","B"),("Pm","B"),("B","t")]
    g = G(sets, E, "s", "t", L2)
    o = 4*ell; rh = relax(g, hull=True)
    print(f"theta={th_deg:2d} score={(o/rh-1)/(1/np.cos(th)-1):.6f}  score-1/2={(o/rh-1)/(1/np.cos(th)-1)-0.5:.2e}")
