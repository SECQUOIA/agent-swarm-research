# Critic check: for each (L,k) flagged by the pattern scan, does the tightest binary64 enclosure of fl(L)^k miss fl(L^k)?
# Lower-bound side: empty exact intersection requires roundup(fl(L)^k) < fl(L^k); upper side: rounddown(fl(L)^k) > fl(L^k).
from fractions import Fraction as F
import math
def up(q):
    d=float(q)
    if F(d)<q: d=math.nextafter(d,math.inf)
    return d
def dn(q):
    d=float(q)
    if F(d)>q: d=math.nextafter(d,-math.inf)
    return d
for L,side in [('0.6','lb'),('0.7','lb'),('0.85','lb'),('0.8','ub')]:
    for k in (2,3):
        ex=F(float(L))**k; y=float(F(L)**k)
        miss=(up(ex)<y) if side=='lb' else (dn(ex)>y)
        print(f"L={L} k={k} side={side}: fl(L)^k-fl(L^k)={float(ex-F(y)):+.4e}  tight enclosure=[{dn(ex)!r}, {up(ex)!r}]  fl(L^k)={y!r}  enclosure misses bound: {miss}")
x=F(0.7)**3; p=F(0.343)
print('0.7 cube: tight lower end - fl(0.343) = %.4e ; SCIP traced lower end 0.34299999999999986 - fl(0.343) = %.4e'%(float(F(dn(x))-p), float(F(0.34299999999999986)-p)))
