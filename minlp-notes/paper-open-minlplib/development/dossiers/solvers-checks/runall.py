import sys; sys.set_int_max_str_digits(0)
exec(open('cambound.py').read().replace("if __name__=='__main__':","if False:"))
from fractions import Fraction as F
import mpmath, time
mpmath.mp.dps=40
claims={'QPLIB_2738.gms':('ANTIGONE 2026 "Global minimum" value',F('-4.284302')),'QPLIB_3177.gms':('MINOTAUR 0.4.1 "Optimal" value',F('-4.2774')),'QPLIB_2480.gms':('ANTIGONE 2026 time-limit bound',F('-4.601964')),'QPLIB_2703.gms':('SCIP 9.2.1 primal',F('-4.33023953971002'))}
res={}
for p in ['camshape100.gms','QPLIB_2738.gms','camshape200.gms','QPLIB_2480.gms','camshape400.gms','QPLIB_2703.gms','camshape800.gms','QPLIB_3177.gms']:
    t=time.time()
    n,c,val,inb,minS,a1=bound(p)
    res[p]=val
    s=mpmath.mpf(val.numerator)/val.denominator
    print(f"{p:16s} n={n} c={mpmath.nstr(mpmath.mpf(c.numerator)/c.denominator,17)} bound={mpmath.nstr(s,18)} E-in-bounds={inb} minS={minS:.4f} d1free={a1 is None} ({time.time()-t:.1f}s)",flush=True)
    if p in claims:
        lab,v=claims[p]
        print(f"   {lab}: {float(v)}  value - bound = {float(v-val):.6e}",flush=True)
for a,b in [('camshape100.gms','QPLIB_2738.gms'),('camshape200.gms','QPLIB_2480.gms'),('camshape400.gms','QPLIB_2703.gms'),('camshape800.gms','QPLIB_3177.gms')]:
    print(a,b,'QPLIB bound - MINLPLib bound = %.3e'%float(res[b]-res[a]))
