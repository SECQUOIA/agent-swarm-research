import ast
import hashlib
import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path
import os
import numpy as np
import mpmath as mp

BASE = Path(__file__).resolve().parent
sys.path[:0] = [str(BASE/'tree/research-20260929/reviews/wave3-verification'),
                str(BASE/'tree/research-20260929/open-instances-wave3/kan')]
import kan_decode
kan_decode.OSIL = str(BASE/'osil')
import kan_bnb_rigexp as B
import kan_iv as K

def exact(x):
    return F(float(x))
def rational_exp(q, n=60):
    # Absolute bound on the omitted tail, since successive absolute terms
    # after n+1 have ratio at most |q|/(n+2).
    t = s = F(1)
    for j in range(1, n+1):
        t *= q / j
        s += t
    tail = abs(q)**(n+1) / math.factorial(n+1) / (1-abs(q)/F(n+2))
    return s-tail, s+tail
def plus(x,y): return x[0]+y[0], x[1]+y[1]
def neg(x): return -x[1], -x[0]
def times(x,y):
    p = [a*b for a in x for b in y]
    return min(p),max(p)
def reciprocal(x):
    assert x[0]>0
    return 1/x[1],1/x[0]
def sigmoid(z):
    elo = rational_exp(-z[1])[0]
    ehi = rational_exp(-z[0])[1]
    return reciprocal((1+elo,1+ehi))
def silu(z): return times(z,sigmoid(z))
def d1(z):
    s=sigmoid(z)
    return times(s,plus((F(1),F(1)),times(z,plus((F(1),F(1)),neg(s)))))

files = ['kan_bnb.py','kan_bnb_rigexp.py','kan_decode.py']
for file in files:
    p=BASE/'tree/research-20260929/reviews/wave3-verification'/file
    print('SHA256',file,hashlib.sha256(p.read_bytes()).hexdigest())
for file in [BASE/'tree/research-20260929/open-instances-wave3/kan/kan_iv.py',
             BASE/'tree/research-20260929/open-instances-wave2/small/ia.py']:
    print('SHA256',file.name,hashlib.sha256(file.read_bytes()).hexdigest())
a=ast.parse((BASE/'tree/research-20260929/reviews/wave3-verification/kan_bnb.py').read_text())
b=ast.parse((BASE/'tree/research-20260929/reviews/wave3-verification/kan_bnb_rigexp.py').read_text())
def stripped(tree):
    tree.body=[n for n in tree.body if not (isinstance(n,ast.FunctionDef) and n.name=='iexp')
               and not (isinstance(n,ast.Import) and any(x.name=='kan_iv' for x in n.names))]
    return ast.dump(tree,include_attributes=False)
assert stripped(a)==stripped(b)
print('AST outside kan_iv import and iexp: identical')

lnlo=sum((F(1,j*2**j) for j in range(1,221)),F(0))
lnhi=lnlo+F(1,221*2**220)
assert exact(K.LN2.lo)<=lnlo<=lnhi<=exact(K.LN2.hi)
assert exact(K.LN2_64.lo)<=lnlo/64<=lnhi/64<=exact(K.LN2_64.hi)
print('LN2 exact enclosure',float(lnhi-lnlo),float(K.LN2.lo).hex(),float(K.LN2.hi).hex())
table=[]
for j in range(64):
    lo=rational_exp(j*lnlo/64)[0]
    hi=rational_exp(j*lnhi/64)[1]
    assert exact(K._TLO[j])<=lo<=hi<=exact(K._THI[j])
    table.append({'j':j,'lo_hex':float(K._TLO[j]).hex(),'hi_hex':float(K._THI[j]).hex(),
                  'lower_margin':float(lo-exact(K._TLO[j])),
                  'upper_margin':float(exact(K._THI[j])-hi)})
(BASE/'evidence/table-exact.json').write_text(json.dumps(table,indent=2)+'\n')
print('TABLE 64/64 entries: exact rational pass')
for j in range(19):
    prod=1.0 if j==0 else float(np.prod(np.arange(1,j+1,dtype=np.float64)))
    assert exact(prod)==math.factorial(j)
    q=F(1,math.factorial(j))
    assert exact(K._INVFACT[j].lo)<=q<=exact(K._INVFACT[j].hi)
print('FACTORIALS and reciprocal coefficient enclosures 0..18: exact pass')
for degree, radius, remainder in [(8,0.0055,K._REM2),(18,0.36,K._REM)]:
    radius=exact(radius)
    expupper=rational_exp(radius)[1]
    rem=radius**(degree+1)/math.factorial(degree+1)*expupper
    assert rem<=exact(remainder)
    print('REMAINDER',degree,float(rem),'<=',float(remainder),'exact pass')
z=(exact(B.ZS_LO),exact(B.ZS_HI))
assert d1((z[0],z[0]))[1]<0<d1((z[1],z[1]))[0]
c=(z[0]+z[1])/2
minlo=plus(silu((c,c)),times(d1(z),(z[0]-c,z[1]-c)))[0]
assert exact(B.SMIN_LO)<=minlo
print('VERIFIER SiLU constants exact pass',B.ZS_LO,B.ZS_HI,B.SMIN_LO,
      'safe margin',float(minlo-exact(B.SMIN_LO)))
zk=(exact(K._ZS_LO),exact(K._ZS_HI))
assert d1((zk[0],zk[0]))[1]<0<d1((zk[1],zk[1]))[0]
ck=(zk[0]+zk[1])/2
kminlo=plus(silu((ck,ck)),times(d1(zk),(zk[0]-ck,zk[1]-ck)))[0]
assert exact(K.SILU_MIN_LO)<=kminlo
print('kan_iv import-time SiLU constants exact pass')

mp.mp.dps=100
vals=[0.0,-0.0,700.,-700.,np.nextafter(700.,0.),np.nextafter(-700.,0.),
      np.nextafter(0.,1.),np.nextafter(0.,-1.), B.ZS_LO,B.ZS_HI,-B.ZS_LO,-B.ZS_HI]
for n in [-64633,-64001,-4097,-65,-64,-1,0,1,63,64,4095,64001,64633]:
    for shift in [0,0.5,-0.5]:
        v=float((mp.mpf(n)+shift)*mp.log(2)/64)
        if abs(v)<=700:
            vals.extend([np.nextafter(v,-np.inf),v,np.nextafter(v,np.inf)])
vals.extend(np.random.default_rng(62026).uniform(-700,700,10000).tolist())
domains={}
observed=K.iexp_pt_fast
captured=[]
def capture(x):
    captured.extend(np.asarray(x).ravel().tolist())
    return observed(x)
K.iexp_pt_fast=capture
names=['kan_r3_h1_n4','kan_r3_h1_n5','kan_r3_h1_n9','kan_r5_h1_n3','kan_r5_h1_n5','kan_r5_h1_n8']
for name in names:
    captured.clear()
    M=B.Model(name)
    M.evaluate(M.ulo[None,:],M.uhi[None,:],want_ub=False)
    # Probe around the archived incumbent too, to exercise LB3 where useful.
    archived=(Path(os.environ['MINLP_REPO_ROOT']) / 'paper-open-minlplib/development/dossiers/ann-kan-checks/logs')/(name+'.bnb.json')
    u=np.array(json.loads(archived.read_text())['ub_u'])
    for width in [0.,1e-8,1e-4,0.04]:
        lo=np.maximum(M.ulo,u-width)
        hi=np.minimum(M.uhi,u+width)
        # The explicit thr and force3 request exercises the LB3 path.
        M.evaluate(lo[None,:],hi[None,:],thr=float('inf'),force3=True)
    domains[name]=[min(captured),max(captured)]
    vals.extend(captured)
K.iexp_pt_fast=observed
for f in sorted((BASE/'evidence').glob('*.args.json')):
    data=json.loads(f.read_text())
    vals.extend(data['samples'])
    vals.extend([data['stats']['lo'],data['stats']['hi']])
    print('FULL RUN ARGUMENT RANGE',f.stem,data['stats'])
vals=sorted(set(float(v) for v in vals if abs(v)<=700))
v=np.array(vals)
y=observed(v)
worst=0.0
min_margin=float('inf')
for x,lo,hi in zip(v,y.lo,y.hi):
    true=mp.exp(mp.mpf(float(x)))
    assert mp.mpf(float(lo))<=true<=mp.mpf(float(hi)),(x,lo,hi,true)
    worst=max(worst,float((mp.mpf(float(hi))-mp.mpf(float(lo)))/true))
    min_margin=min(min_margin,float(min(true-mp.mpf(float(lo)),mp.mpf(float(hi))-true)/true))
print('100-DIGIT EXP tests',len(v),'all enclosed; max relative width',worst,'min relative margin',min_margin)
print('SIX-MODEL ROOT/CENTRE/LB3 PROBE ARGUMENT RANGES',json.dumps(domains,sort_keys=True))
(BASE/'evidence/exp-test-summary.json').write_text(json.dumps({'count':len(v),'max_relative_width':worst,
     'min_relative_margin':min_margin,'six_model_probe_ranges':domains},indent=2)+'\n')

# Check minquad against the exact minima for realistic signed displacements.
rng=np.random.default_rng(97)
args=[]
for i in range(2000):
    gl,gh=sorted(rng.uniform(-100,100,2))
    m=float(rng.uniform(-100,100))
    sl=-float(10**rng.uniform(-12,1))
    sh=float(10**rng.uniform(-12,1))
    args.append((gl,gh,m,sl,sh))
arr=np.array(args)
ans=B.minquad(*arr.T)
for row,out in zip(args,ans):
    gl,gh,m,sl,sh=map(exact,row)
    candidates=[]
    for g in [gl,gh]:
        for s in [sl,sh]: candidates.append(g*s+m*s*s/2)
        if m>0 and sl<=-g/m<=sh: candidates.append(-g*g/(2*m))
    assert exact(out)<=min(candidates)
print('MINQUAD 2000 exact rational reference comparisons: pass')

for name in names:
    repo=Path(os.environ['MINLP_REPO_ROOT'])
    logs=repo/'paper-open-minlplib/development/dossiers/ann-kan-checks/logs'
    new=json.loads((logs/(name+'.bnb.json')).read_text())
    log=(logs/(name+'.rigexp.log')).read_text()
    logged=json.loads(log[log.index('{'):])
    assert new==logged
    old=json.loads((repo/'research-20260929/reviews/wave3-verification/logs'/(name+'.bnb_v2.json')).read_text())
    author=json.loads((repo/'research-20260929/open-instances-wave3/logs'/(name+'.result.json')).read_text())
    # Locate the author's lower bound by the documented result field.
    L=author['dual_bound']
    assert exact(L)<exact(new['lower_bound'])
    print('ARCHIVE',name,'bit_identical_L',float(old['lower_bound']).hex()==float(new['lower_bound']).hex(),
          'change',float(exact(new['lower_bound'])-exact(old['lower_bound'])),
          'above_author',float(exact(new['lower_bound'])-exact(L)))
    own=BASE/'evidence'/(name+'.result.json')
    if own.exists():
        own=json.loads(own.read_text())
        matches={k:own[k]==new[k] for k in own if k!='time'}
        print('REPRODUCTION',name,'time',own['time'],json.dumps(matches))
        assert all(matches.values())
print('ALL AUDIT CHECKS PASSED')
