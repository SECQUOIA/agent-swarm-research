# Critic: epsilon-relaxed bound (Proposition 5 recipe) on top of indep_bound.py; reproduces D(eps) and violation thresholds.
import sys
from fractions import Fraction as F
src=open('indep_bound.py').read()
src=src.replace("def run(fn):","def run(fn,eps=F(0)):")
src=src.replace("    L=[F(1),1/ub[0]]\n","    ub=[u+eps for u in ub]\n    delta=eps/(1-eps)**3\n    L=[F(1),1/ub[0]]\n")
src=src.replace("    E=[]\n    for j in range(1,n+1):\n        if L[j]>0:\n            q=1/L[j]","    Wc=[F(0),F(0)]\n    for j in range(2,n+1): Wc.append(Wc[-1]+Uq[j-2])\n    E=[]\n    for j in range(1,n+1):\n        Lj=L[j]-delta*Wc[j]\n        if Lj>0:\n            q=1/Lj")
src=src.replace("alpha.append(up[dv])","alpha.append(up[dv]+2*eps)")
src=src.replace("    print(fn,'n',n","    return val\n    print(fn,'n',n")
src=src.replace("for f in sys.argv[1:]: run(f)","")
exec(compile(src,'indep_bound_eps','exec'))
for fn,e,obs in [('camshape100.gms','1e-10','5.2581469e-7'),('camshape200.gms','1e-10','2.05270746e-6'),('camshape400.gms','3e-10','8.15e-6'),('QPLIB_2738.gms','1e-8',None),('QPLIB_2738.gms','2.6e-8',None),('QPLIB_3177.gms','1e-9',None),('QPLIB_3177.gms','1e-8',None)]:
    v0=run(fn); v=run(fn,F(e)); D=v0-v
    print(fn,'eps',e,'D=%.5g'%float(D),'' if obs is None else 'observed/D %.3f'%float(F(obs)/D),flush=True)
for fn,e,claim in [('QPLIB_2738.gms','2.5e-8','-4.2843015'),('QPLIB_3177.gms','8e-9','-4.27735')]:
    v=run(fn,F(e)); print(fn,'eps',e,'v_eps=%.10f'%float(v),'top of claim interval',claim,'below v_eps:',F(claim)<v,flush=True)
