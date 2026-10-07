import sys
from fractions import Fraction as F
from math import factorial
import numpy as np
import mpmath as mp

sys.path.insert(0, '/tmp/sol-eg-audit-review/audit/cert')
import auditor as A

mp.mp.prec = 512
u, eps = F(1, 2**53), F(1, 10**14)
# A second, independently tighter ln(2) bracket: 2 atanh(1/3).
n = 200
s = 2 * sum(F(1, (2*j+1)*3**(2*j+1)) for j in range(n))
tail = F(2, (2*n+1)*3**(2*n+1)) / (1-F(1, 9))
assert A._LN2_LO < s < s+tail < A._LN2_HI
assert max(abs(s/64-F(A.L1)-F(A.L2)), abs((s+tail)/64-F(A.L1)-F(A.L2))) <= A.DL
for j, (lo, hi) in enumerate(zip(A.TLO, A.THI)):
    l, h = F(lo), F(hi)
    assert l.numerator**64 <= 2**j*l.denominator**64
    assert h.numerator**64 >= 2**j*h.denominator**64
assert F(A.FUP)*(1+u) <= 1+eps
assert F(A.FDN)*(1-u) >= 1-eps
assert F(A.CP)*(1+A.GZ)*(1+u)+A.GZ <= eps
print('Independent exact ln2 bracket, reduction and table constants: PASS')
print('DL, DR, EH, RHO_H:', *(float(x) for x in (A.DL,A.DR,A.EH,A.RHO_H)))

# Exact versions of the two near-tight natural-end inequalities.
c = F(1e-14)
lower_factor = F(1-1e-14)*(1+u)**4*(1-c*(1-u))
upper_factor = F(1+1e-14)*(1-u)**4*(1+c*(1-u))
elo_max = 1/lower_factor-1
ehi_max = 1-1/upper_factor
assert (1+eps)*lower_factor <= 1 <= (1-eps)*upper_factor
print('Natural end eps limits:', float(elo_max), float(ehi_max))

# Prove a conservative dw bound for all dE <= 1e-6, including the
# denominators absent from the prose's abbreviated first-order expression.
dmax = F(1,10**6)
exp_d = sum(dmax**j/F(factorial(j)) for j in range(30)) + 2*dmax**30/F(factorial(30))
slope = (exp_d-1)/dmax
den = (1-u)**2*(1-eps)
need0, need1 = 1/den-1, slope/den
pad0 = F(1.1e-14)*(1-u)**4
pad1 = F(1.02)*(1-u)**4
assert pad0 >= need0 and pad1 >= need1
print('dw pad vs rigorous error intercept / slope:', float(pad0/need0), float(pad1/need1))

# Form true high-precision reduction half-points, then round once to float;
# do not form them with a previously rounded float L.
L = mp.log(2)/64
ms = range(-65370,65465,5)
mid = np.array([float((mp.mpf(m)+mp.mpf('0.5'))*L) for m in ms])
bins = np.array([float(k*mp.log(2)) for k in range(-1021,1023)])
x = np.concatenate([mid,np.nextafter(mid,np.inf),np.nextafter(mid,-np.inf),
                    bins,np.nextafter(bins,np.inf),np.nextafter(bins,-np.inf),
                    [-708.,709.,0.,5e-324,-5e-324,2**-1022,-2**-1022]])
x = x[(x>=-708)&(x<=709)]
lo,hi,valid = A.exp_enclosure(x)
assert valid.all()
width = 0
for v,l,h in zip(x,lo,hi):
    ex = mp.exp(mp.mpf(float(v)))
    assert mp.mpf(float(l)) <= ex <= mp.mpf(float(h)), (v,l,h,ex)
    width = max(width,float((mp.mpf(float(h))-mp.mpf(float(l)))/ex))
print('512-bit exp references:',len(x),'hard arguments; enclosure PASS; max relative width',width)

# Independent powers stress test, including the CP*z subnormal range.
rng = np.random.default_rng(104)
xs = np.concatenate([np.ldexp(rng.uniform(1,2,8000),rng.integers(-250,250,8000)),
                     np.ldexp(rng.uniform(1,2,8000),-250),[2**-250,2**-251,0.,.1,1.]])
for k in (2,3,4):
    good = xs**k
    accepted = A.pow_ok(xs,k,good)
    for v,y,ok in zip(xs,good,accepted):
        if ok:
            ex = F(float(v))**k
            assert abs(F(float(y))-ex) <= eps*ex
    for sign in (1,-1):
        out = []
        for v in xs:
            ex = F(float(v))**k
            edge = ex*(1+sign*eps)
            y = float(edge)
            if sign==1:
                while F(y) <= edge:
                    y = float(np.nextafter(y,np.inf))
            else:
                while F(y) >= edge:
                    y = float(np.nextafter(y,-np.inf))
            out.append(y)
        assert not A.pow_ok(xs,k,np.array(out)).any()
    print('Exact power boundary tests k=',k,'PASS;',len(xs),'bases, both signs')
z = np.array([2**-250])**4
print('CP*z at smallest ordinary k=4 base:', float(A.CP*z[0]),
      'normal?',bool(A.CP*z[0]>=np.finfo(float).tiny))
print('Independent numerical checks: PASS')
