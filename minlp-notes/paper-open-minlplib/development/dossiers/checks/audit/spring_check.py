# Independent numerical scan (mpmath, 50 digits) of spring over all (i4, wire) assignments, then exact check of the optimum.
from mpmath import mp, mpf, cbrt
mp.dps=50
K=mpf('6.95652173913044e-7'); lb3=mpf('1.78571428571429e-3'); ub3=mpf('2e-2')
cs=[mpf(s) for s in ['.207','.225','.244','.263','.283','.307','.331','.362','.394','.4375','.5']]
a0=mpf('1.570796327'); a1=mpf('.7853981635'); S=mpf('2546.47908913782')
def g(x): return S*((4*x-1)/(4*x-4)+mpf('.615')/x)*x
res=[]
for n in range(1,101):
    for ci,c in enumerate(cs):
        lo=max(mpf('1.1'), mpf('.414')/c, cbrt(lb3*c/(K*n)))
        hi=min(cbrt(ub3*c/(K*n)), (3-c)/c, cbrt((14-mpf('2.1')*c-mpf('1.05')*c*n)*c/(1000*K*n)) if 14-mpf('2.1')*c-mpf('1.05')*c*n>0 else mpf(-1))
        if lo>hi: continue
        # stress row g(x5)/c^2 <= 189000: g convex for x>1 -> feasible set interval; find smallest x in [lo,hi] with g<=189000 c^2
        C=189000*c**2
        if g(lo)<=C: x=lo
        else:
            # g decreasing on (1,1.866): bisection for smallest feasible
            xm=min(hi, mpf('1.8660254037844386'))
            if lo<xm and g(xm)<=C:
                a,b=lo,xm
                for _ in range(200):
                    m=(a+b)/2
                    if g(m)<=C: b=m
                    else: a=m
                x=b
            else: continue
        f=(a0+a1*n)*(c*x)*c**2
        res.append((f,n,ci,x))
res.sort()
print('feasible assignments',len(res))
for f,n,ci,x in res[:3]: print(mp.nstr(f,30),'n',n,'wire',cs[ci],'b%d'%(7+ci),'x5',mp.nstr(x,20))
f0=res[0][0]
print('rounded to 8 decimals:', mp.nstr(f0,9), ' d - f =', mp.nstr(mpf('0.84624567')-f0,10), ' slack 5e-9')
