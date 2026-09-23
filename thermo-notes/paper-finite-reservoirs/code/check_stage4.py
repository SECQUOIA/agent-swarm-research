"""Independent quadrature checks for the Stage 4 derived formulas."""
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import ndtr
from scipy.stats import norm

def contribution(w, r, d):
    if r == 0:
        return 0.
    if d == 0:
        return max(r-w, 0.)
    a = np.log(r/w)/d
    return r*ndtr(a+d/2)-w*ndtr(a-d/2)

for weights, ds in [((.3,.7),(.4,1.7)), ((.8,.2),(2.,.3)), ((.35,.65),(.9,.9))]:
    def deriv(r):
        return ndtr(np.log(r/weights[0])/ds[0]+ds[0]/2)-ndtr(np.log((1-r)/weights[1])/ds[1]+ds[1]/2)
    r = brentq(deriv, 1e-12, 1-1e-12)
    cdf = sum(contribution(w,t,d) for w,t,d in zip(weights,(r,1-r),ds))
    direct = .5*sum(quad(lambda z: abs(w*norm.pdf(z)-t*norm.pdf(z-d)), -12, 12, epsabs=1e-11)[0]
                      for w,t,d in zip(weights,(r,1-r),ds))
    assert abs(cdf-direct) < 2e-8
    if ds[0] == ds[1]:
        assert abs(r-weights[0]) < 1e-10
    print("CDF/root check:", weights, ds, r, cdf, direct)

# Actual power-law likelihood, not a quadratic surrogate.
weights = (.4,.6)
variances = (2.,.7)
gamma = 2.
b = 1/(2*gamma)
correction = (variances[0]-variances[1])/(8*gamma)
predicted_tv = sum(w*(2*ndtr(b*np.sqrt(v)/2)-1) for w,v in zip(weights,variances))
for n in (100, 1000, 10000):
    c = gamma*n**1.5
    cal = n/(-np.expm1(-n/c))+correction*np.sqrt(n)
    def h(z, i):
        e = np.longdouble(i*n+np.sqrt(n)*z)
        return float(e+np.longdouble(c)*np.log1p(-e/np.longdouble(cal)))
    factors = [quad(lambda z: np.exp(h(z,i))*norm.pdf(z,scale=np.sqrt(v)), -12*np.sqrt(v),12*np.sqrt(v),epsabs=1e-10)[0]
               for i,v in enumerate(variances)]
    ztot = np.dot(weights, factors)
    # Conditional phase expectations give the actual full likelihood TV
    # (the Gaussian components need not have exactly disjoint supports).
    tv = .5*sum(w*quad(lambda z: abs(np.exp(h(z,i))/ztot-1)*norm.pdf(z,scale=np.sqrt(v)),
                           -12*np.sqrt(v),12*np.sqrt(v),epsabs=1e-10)[0]
                 for i,(w,v) in enumerate(zip(weights,variances)))
    print("Physical compensation:", n, weights[0]*factors[0]/ztot, tv, "limit", predicted_tv)
    if n == 10000:
        assert abs(weights[0]*factors[0]/ztot-weights[0]) < 1e-3
        assert abs(tv-predicted_tv) < 1e-3

theta = np.linspace(0,1,10001)
tau=1.
rate=tau*np.minimum(np.minimum(2*np.sqrt(np.pi*theta),2),2*np.sqrt(np.pi*(1-theta)))
assert np.min(rate-8*tau*theta*(1-theta)) >= -1e-12
for a in (7.,8.,9.):
    f=rate-a*theta*(1-theta)
    print("Square model A/minimum:", a, theta[np.argmin(f)], f.min())
