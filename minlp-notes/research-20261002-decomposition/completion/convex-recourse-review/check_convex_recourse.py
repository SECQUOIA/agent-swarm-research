"""Independent analytic oracle check for conditional-convex factor solver."""
from fractions import Fraction as F
from pathlib import Path
import sys, json
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'solver'))
from certified_grid import BoxQP

def analytic(a, b, interval, pieces, integer=False):
    lo, hi = map(F, interval)
    breaks = {lo, hi}
    for c, d, e, l, u in pieces:
        c,d,e,l,u=map(F,(c,d,e,l,u))
        if d:
            for x in ([(-e-c*l)/d, (-e-c*u)/d] if c else [-e/d]):
                if lo < x < hi:
                    breaks.add(x)
    candidates=set(breaks)
    order=sorted(breaks)
    for left,right in zip(order,order[1:]):
        mid=(left+right)/2
        alpha,beta=F(a)/2,F(b)
        for c,d,e,l,u in pieces:
            c,d,e,l,u=map(F,(c,d,e,l,u))
            lin=d*mid+e
            y=max(l,min(u,-lin/c)) if c else l if lin>=0 else u
            if c and l < y < u:
                alpha-=d*d/(2*c)
                beta-=d*e/c
            else:
                beta+=d*y
        if alpha>0:
            station=-beta/(2*alpha)
            if left<station<right:
                candidates.add(station)
    if integer:
        candidates=set(map(F,range(int(lo),int(hi)+1)))
    def val(z):
        v=F(a)*z*z/2+F(b)*z
        for c,d,e,l,u in pieces:
            c,d,e,l,u=map(F,(c,d,e,l,u))
            lin=d*z+e
            y=max(l,min(u,-lin/c)) if c else l if lin>=0 else u
            v+=c*y*y/2+lin*y
        return v
    return min((val(z),z) for z in candidates)

def model(a,b,interval,pieces,integer=False):
    n=1+len(pieces)
    H=[[F(0)]*n for _ in range(n)]
    H[0][0]=F(a)
    lin=[F(b)]
    bounds=[tuple(map(F,interval))]
    for i,(c,d,e,lo,hi) in enumerate(pieces,1):
        H[i][i]=F(c)
        H[0][i]=H[i][0]=F(d)
        lin.append(F(e)); bounds.append((F(lo),F(hi)))
    return BoxQP(H,lin,bounds,[0] if integer else [],[list(range(n))],[])


from convex_recourse import solve_convex_recourse, verify_convex_recourse, ConvexRecourseError
from copy import deepcopy
from unittest.mock import patch

cases=[]
for a in (-2,0,2,5):
    for integer in (False,True):
        cases.append((a,F(-1,3),(-1,2),[(2,-2,0,0,1)],integer))
        cases.append((a,F(2,5),(-1,2),[(0,2,-1,-1,2),(4,-3,F(1,2),0,1)],integer))
cases.extend([(4,-2,(-1,2),[(0,0,1,F(1,3),F(1,3))],False),
              (0,1,(-1,2),[(2,0,-1,0,1)],False)])
results=[]
certificates=[]
for k,(a,b,iv,pieces,integer) in enumerate(cases):
    p=model(a,b,iv,pieces,integer)
    truth,_=analytic(a,b,iv,pieces,integer)
    c=solve_convex_recourse(p,[[i] for i in range(1,len(p.b))],epsilon=F(1,100),max_levels=14,max_table_states=10000,time_limit=5)
    assert verify_convex_recourse(c,p)
    assert F(c['lower'])<=truth<=F(c['upper']), (k,c['lower'],truth,c['upper'])
    if c['status'] in ('certified','exact'):
        assert F(c['gap'])<=F(1,100)
    if a<=0 or integer:
        assert F(c['gap'])==0, (k,c['status'],c['gap'])
    results.append((k,c['status'],c['gap'],len(c['stages'])))
    certificates.append((p,c))

# An independently scoped verifier must never optimize private QPs or LPs.
with patch('convex_recourse.solve_convex_box_qp',side_effect=AssertionError('QP optimization called')), patch('rational_optimization.solve_lp',side_effect=AssertionError('LP optimization called')):
    for p,c in certificates:
        assert verify_convex_recourse(json.loads(json.dumps(c)),p)

# Check scalar analytic formulas against direct feasible samples as a sanity check.
for a,b,iv,pieces,integer in cases:
    truth,_=analytic(a,b,iv,pieces,integer)
    if not integer:
        for k in range(121):
            z=F(iv[0])+(F(iv[1])-F(iv[0]))*k/120
            direct=F(a)*z*z/2+F(b)*z
            for c,d,e,l,u in pieces:
                c,d,e,l,u=map(F,(c,d,e,l,u));lin=d*z+e
                y=max(l,min(u,-lin/c)) if c else l if lin>=0 else u
                direct+=c*y*y/2+lin*y
            assert direct>=truth

mutations=0
for p,c in certificates:
    bads=[]
    bad=deepcopy(c);bad['lower']=str(F(bad['upper'])+1);bads.append(bad)
    bad=deepcopy(c);bad['upper']=str(F(bad['upper'])+1);bads.append(bad)
    if c['queries']:
        bad=deepcopy(c);bad['queries'][0]['value']=str(F(bad['queries'][0]['value'])+1);bads.append(bad)
        bad=deepcopy(c);bad['queries'][0]['lower_multipliers'][0]='-1';bads.append(bad)
        bad=deepcopy(c);bad['queries'][0]['parameters']=['0','0','0'];bads.append(bad)
        bad=deepcopy(c);bad['queries'].pop(0);bads.append(bad)
    if c['stages']:
        bad=deepcopy(c);bad['stages'][0]['grid_minimum']=str(F(bad['stages'][0]['grid_minimum'])+1);bads.append(bad)
    for bad in bads:
        try: verify_convex_recourse(bad,p)
        except ConvexRecourseError: mutations+=1
        else: raise AssertionError('mutation accepted')

# Limits always preserve original-model valid lower and upper bounds.
p=certificates[6][0]
limit_results=[]
for options in ({'time_limit':0},{'max_levels':0},{'max_table_states':1},{'max_faces':0}):
    c=solve_convex_recourse(p,[[1]],**options)
    assert verify_convex_recourse(c,p)
    assert c['status'] in ('time_limit','level_limit','table_limit','oracle_limit')
    limit_results.append(c['status'])

print(json.dumps({'analytic_cases':results,'replay_without_optimization':len(certificates),'rejected_mutations':mutations,'limit_results':limit_results}))

def linear(A,b):
 n=len(b);M=[list(row)+[bi] for row,bi in zip(A,b)]
 for k in range(n):
  pivot=next((i for i in range(k,n) if M[i][k]),None)
  if pivot is None:return None
  M[k],M[pivot]=M[pivot],M[k];d=M[k][k];M[k]=[x/d for x in M[k]]
  for i in range(n):
   if i!=k:
    d=M[i][k];M[i]=[x-d*y for x,y in zip(M[i],M[k])]
 return tuple(row[-1] for row in M)

def brute(p):
 n=len(p.b);best=None
 domains=[tuple(range(int(lo),int(hi)+1)) if i in p.integers else ('l','u','f') for i,(lo,hi) in enumerate(p.bounds)]
 for face in product(*domains):
  free=[i for i,x in enumerate(face) if x=='f'];active=[i for i in range(n) if i not in free]
  x=[None]*n
  for i in active:x[i]=p.bounds[i][0] if face[i]=='l' else p.bounds[i][1] if face[i]=='u' else F(face[i])
  xf=linear([[p.A[i][j] for j in free] for i in free],[-p.b[i]-sum((p.A[i][j]*x[j] for j in active),F(0)) for i in free])
  if xf is None:continue
  for i,v in zip(free,xf):x[i]=v
  if p.feasible(x):
   v=p.value(x)
   if best is None or v<best:best=v
 return best

from random import Random
from itertools import product
r=Random(7033);counts={};largest_gap=F(0)
for k in range(24):
 H=[[F(0)]*4 for _ in range(4)]
 for i in range(2):H[i][i]=F(r.choice([-2,0,2,4]))
 H[2][2]=H[3][3]=F(2);H[2][3]=H[3][2]=F(r.choice([-2,-1,0,1,2]))
 for i in range(2):
  for j in range(i+1,4):H[i][j]=H[j][i]=F(r.randint(-3,3))
 p=BoxQP(H,[F(r.randint(-3,3),2) for _ in range(4)],[(-1,1)]*4,[0] if k%3==0 else [],[list(range(4))],[])
 truth=brute(p)
 c=solve_convex_recourse(p,[[2,3]],epsilon=F(1,20),max_levels=10,max_table_states=5000,time_limit=3)
 assert verify_convex_recourse(c,p)
 assert F(c['lower'])<=truth<=F(c['upper']), (k,truth,c)
 counts[c['status']]=counts.get(c['status'],0)+1
 largest_gap=max(largest_gap,F(c['gap']))
print(json.dumps({'cases':24,'status_counts':counts,'largest_gap':str(largest_gap)}))


# Empty retained vector still consumes a local solve and honors every cap.
all_private=BoxQP([[2,2],[2,2]],[-1,-1],[(0,1)]*2,[],[[0,1]],[])
empty_results=[]
for options,status in (({"max_levels":0},"level_limit"),
                       ({"time_limit":0},"time_limit"),
                       ({"max_faces":0},"oracle_limit"),
                       ({"max_table_states":1},"exact")):
    c=solve_convex_recourse(all_private,[[0,1]],exact=True,**options)
    assert c["status"]==status and verify_convex_recourse(c,all_private)
    assert F(c["lower"])<=F(-1,4)<=F(c["upper"])
    assert c["retained"]==[] and c["exact_requested"] is True
    empty_results.append(status)

# The exact-request flag cannot reclassify a nonzero certified gap.
p,c=next((p,c) for p,c in certificates if c["status"]=="certified" and F(c["gap"])>0)
for flag in (True,"false",1):
    bad=deepcopy(c);bad["exact_requested"]=flag
    try:verify_convex_recourse(bad,p)
    except ConvexRecourseError:pass
    else:raise AssertionError("invalid exact request was accepted")
print(json.dumps({"empty_retained_limits":empty_results,"exact_request_rejections":3}))

# Piecewise cancellation must stay independent of the private stiffness M.
stiff_results=[]
for magnitude in (1,100,1000000):
    M=F(magnitude)
    p=BoxQP([[2*M+6,-2*M-4,-2*M],[-2*M-4,2*M+2,2*M],[-2*M,2*M,2*M]],
            [-2,1,0],[(0,F(3,4)),(0,1),(0,1)],[],[[0,1,2]],[],F(1,4))
    truth=-(8*M+9)/(16*(M+1))
    c=solve_convex_recourse(p,[[1,2]],epsilon=F(1,10000),max_levels=48,
                            max_table_states=10000,time_limit=5)
    from convex_recourse import _piecewise_module
    with patch.object(_piecewise_module(), 'construct', side_effect=AssertionError('partition construction called')), patch('convex_recourse.solve_convex_box_qp', side_effect=AssertionError('QP optimization called')), patch('rational_optimization.solve_lp', side_effect=AssertionError('LP optimization called')):
        assert verify_convex_recourse(json.loads(json.dumps(c)),p)
    assert F(c['lower'])<=truth<=F(c['upper']) and F(c['gap'])<=F(1,10000)
    assert len(c['curvature_proofs'])==1
    for alter in ('value','coverage','duplicate'):
        bad=deepcopy(c)
        if alter=='value':
            bad['curvature_proofs'][0]['pieces'][0]['value'][2]='0'
        elif alter=='coverage':
            bad['curvature_proofs'][0]['pieces'].pop(0)
        else:
            bad['curvature_proofs'].append(deepcopy(bad['curvature_proofs'][0]))
        try:verify_convex_recourse(bad,p)
        except ConvexRecourseError:pass
        else:raise AssertionError('invalid scalar curvature accepted')
    stiff_results.append([magnitude,c['status'],len(c['stages']),len(c['queries']),c['gap']])
print(json.dumps({'stiff_piecewise_cases':stiff_results,'invalid_scalar_proofs_rejected':9}))

# Independent local bounds are summed before taking the positive part.
# Each recourse value is -z^2: direct curvature 3 becomes 3-2-2=-1.
curvature_sum_results=[]
for integer,hi in ((False,1),(True,3)):
    p=BoxQP([[3,-2,-2],[-2,2,0],[-2,0,2]],[0,0,0],[(0,hi)]*3,
            [0] if integer else [],[[0,1,2]],[])
    c=solve_convex_recourse(p,[[1],[2]],epsilon=0,max_levels=1)
    assert c['status']=='exact' and F(c['upper'])==-F(hi*hi,2)
    assert len(c['curvature_proofs'])==2 and verify_convex_recourse(c,p)
    curvature_sum_results.append(c['upper'])
print(json.dumps({'summed_curvature_exact_values':curvature_sum_results}))

# Exercise actual conditioning restarts without the optional scalar tightening.
d=1-F(1,1024);h=1-d*d
p=BoxQP([[1,-d],[-d,1]],[-h/3,0],[(0,1)]*2,[],[[0,1]],[])
c=solve_convex_recourse(p,[[1]],epsilon=F(1,1000000),max_levels=100,
                        max_table_states=10000,time_limit=10,scalar_curvature=False)
assert c['status']=='certified' and verify_convex_recourse(c,p)
assert F(c['lower'])<=-h/18<=F(c['upper'])
trials=sorted({s['trial'] for s in c['stages']})
assert len(trials)>1
print(json.dumps({'conditioning_trials':trials,'completed_levels':len(c['stages']),
                  'local_queries':len(c['queries'])}))
