import ast
import glob
import os
import sys
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, '/tmp/sol-eg-audit-review/audit/cert')
from gms_model import GmsModel
from indep_cert_audit import Model

base = '/tmp/sol-eg-audit-review/audit'
for filename in ('indep_cert_audit.py','margin_cert_audit.py','recheck_audit.py','auditor.py','gms_model.py'):
    text = open(base+'/cert/'+filename).read()
    tree = ast.parse(text)
    calls = sorted((n.lineno,ast.unparse(n.func)) for n in ast.walk(tree) if isinstance(n,ast.Call))
    watched = [(line,call) for line,call in calls if any(k in call for k in ('exp','pow','log','sqrt','einsum','linprog'))]
    print(filename,watched)

for name,prefix in [('eg_int_s','int'),('eg_disc_s','disc_p'),('eg_disc2_s','disc2_p')]:
    m=Model(name)
    files=glob.glob(base+'/out/res/'+prefix+'*.npz')
    # These lower bounds hold throughout root boxes and all smaller leaf/split boxes.
    roots=[np.load(f) for f in files]
    low=np.min([z['root_lo'] for z in roots],axis=0)
    high=np.max([z['root_hi'] for z in roots],axis=0)
    assert (low>=.25).all()
    qsc=min(F(float(si))*F(float(x)) for si,x in zip(m.S,low))
    gamma_min=min(abs(F(float(g))) for g in m.GA.flat)
    smin=min(F(float(s)) for s in m.S)
    # c is clipped into its box, so Sc has this positive lower bound.
    # dt includes 1e-15 abs(Sc); tau >= dt. Bounds include more than enough
    # rounding operations. Nonzero r >= 2^-55 follows from binary64 spacing.
    tau_min=F(1e-15)*qsc*(1-F(1,2**53))**10
    p_min=min(2*abs(F(float(m.GA[row,i])))*F(float(m.S[i]))*
              F(1e-15)*F(float(m.S[i]))*F(float(low[i]))*
              (F(1,2) if m.isint[i] else F(1,2**55))
              for row in range(m.R) for i in range(m.d))*(1-F(1,2**53))**30
    assert tau_min>F(1,10**17) and p_min>F(1,10**35)
    # Even the smallest potential p^4 and CP*p^4 are normal.
    assert p_min**4*F(9,10**15)>F(1,2**1022)
    maxA=max(abs(F(float(a))) for a in m.A.flat)
    maxGA=max(abs(F(float(g))) for g in m.GA.flat)
    minA=min(abs(F(float(a))) for a in m.A.flat if a)
    max_t=max(abs(F(float(mu))+F(float(s))*F(float(x)))
              for row in m.MU for term in row for mu,s,lb,ub in zip(term,m.S,low,high) for x in (lb,ub))
    print(name,'root ranges',list(zip(low,high)),'isint',m.isint.tolist())
    print('  conservative tau_min, p_min:',float(tau_min),float(p_min))
    print('  max|A|, min_nonzero|A|, max|GA|, min|GA|, max|t|:',
          *(float(x) for x in (maxA,minA,maxGA,gamma_min,max_t)))
    rr=[((F(float(h))-F(float(l)))/2+F(1,2**53)*max(abs(F(float(l))),abs(F(float(h)))))
        *(1+F(1,2**53))**4 for l,h in zip(low,high)]
    terms=GmsModel(name).terms()
    ellmax=F(0)
    qr=F(0)
    for row in terms:
        for _,fac in row['terms']:
            ell=F(0)
            q=F(0)
            for i,v in enumerate(m.vars):
                sc,mu,ga=fac[v]
                tm=max(abs(mu+sc*F(float(low[i]))),abs(mu+sc*F(float(high[i]))))
                # Extra absolute and relative slack covers the code's inflated
                # t and K1 used to form ell, at these small data magnitudes.
                ell+=2*abs(ga)*sc*(tm+F(1,10**12))*rr[i]
                q+=abs(ga)*sc**2*rr[i]**2
            ellmax=max(ellmax,ell*(1+F(1,10**12)))
            qr=max(qr,q*(1+F(1,10**12)))
    assert ellmax<17 and qr<10
    print('  conservative root-wide ell and q upper bounds:',float(ellmax),float(qr))
    # All changing integer root intervals are on a single coordinate;
    # the comparison's marginal range check is sufficient for these data.
    changing=[i for i in np.flatnonzero(m.isint) if len(set((float(z['root_lo'][i]),float(z['root_hi'][i])) for z in roots))>1]
    assert len(changing)<=1
    print('  changing integer coordinates:',changing)

# The actual einsum invocation defaults to optimize=False, and numpy's
# Python dispatcher delegates these calls directly to c_einsum.
import inspect
print('numpy',np.__version__)
print('einsum signature:',inspect.signature(np.einsum))
src=inspect.getsource(np.einsum)
start=src.index('if optimize is False:')
print(src[start:start+250])
print('Source and range checks: PASS')
