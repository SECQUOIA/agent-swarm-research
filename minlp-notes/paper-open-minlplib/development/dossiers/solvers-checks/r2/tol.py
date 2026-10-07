import sys
from fractions import Fraction as F
from cambd import structure, bound
cases=[('camshape100.gms','1e-10','5.2581469e-7','BARON claim'),('camshape100.gms','7.72e-10','1.5191022e-7','SCIP campaign'),
 ('camshape100.gms','1e-8','5.3e-5','exploratory SCIP (unchecked)'),
 ('camshape200.gms','1e-10','2.05270746e-6','BARON claim'),('camshape400.gms','1e-10','8.15450068e-6','BARON'),
 ('camshape400.gms','3e-10','8.15e-6','MINLPLib p2'),('camshape800.gms','3e-10','3.27e-5','MINLPLib p2'),
 ('camshape800.gms','3.32e-7','0.09365569719715','BARON'),('camshape800.gms','9.75e-7','0.02328447110410','GUROBI'),
 ('QPLIB_2738.gms','1e-8',None,''),('QPLIB_2738.gms','2.6e-8',None,''),('QPLIB_2738.gms','1e-6',None,''),
 ('QPLIB_3177.gms','1e-9',None,''),('QPLIB_3177.gms','1e-8',None,''),('QPLIB_3177.gms','1e-6',None,'')]
cache={}
for p,e,obs,who in cases:
    if p not in cache: cache[p]=(structure(p),)
    st=cache[p][0]
    v0,_,_=bound(st); v,mU,Wn=bound(st,F(e),Q=10**30)
    D=v0-v
    s=f"{p} eps={e}: D={float(D):.5g}  (D/eps={float(D/F(e)):.4g}; maxU={float(mU):.4g}; sumU={float(Wn):.4g})"
    if obs: s+=f"  observed {who} {float(F(obs)):.5g} ratio {float(F(obs)/D):.3f}"
    print(s,flush=True)
