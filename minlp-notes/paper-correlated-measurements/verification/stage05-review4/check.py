import json, itertools, time
from pathlib import Path
from fractions import Fraction as Q
import sympy as s
ROOT=Path(__file__).resolve().parents[2]; DATA=ROOT/'supplement/legacy/results'
def read(name): return json.loads((DATA/name).read_text(),parse_float=str)
def mat(x): return s.Matrix([[s.Rational(a) for a in row] for row in x])
def cov(d, indices):
 r,v,w=map(s.Rational,(d['rho'],d['latent_variance'],d['nugget_variance']))
 return s.Matrix([[v*r**abs(i-j)+(w if i==j else 0) for j in indices] for i in indices])
def info(d,S):
 F=mat(d['F']).extract(S,range(len(d['prior'])));return mat(d['prior'])+F.T*cov(d,S).inv(method='DM')*F
# Independent positive rational logarithm series, without historical helpers.
def logbounds(x):
 x=Q(x); h=0
 while x>=2: x/=2; h+=1
 while x<1: x*=2; h-=1
 def base(x):
  u=(x-1)/(x+1); m=40
  low=sum((2*u**(2*j+1)/Q(2*j+1) for j in range(m)),Q(0))
  return low,low+2*u**(2*m+1)/((2*m+1)*(1-u*u))
 lo,hi=base(x); a,b=base(Q(2))
 return (lo+h*a,hi+h*b) if h>=0 else (lo+h*b,hi+h*a)
def encloses_saved(det, pair):
 lo,hi=logbounds(det); assert Q(pair[0])<=lo<=hi<=Q(pair[1])
start=time.perf_counter(); report={}
# Robust exact same models, independent selected inverse and final interval algebra.
robust=[]
for n,suffix in [(48,''),(96,''),(96,'-polished')]:
 c=read(f'robust-kinetic-n{n}{suffix}-certificate.json'); source=read(f'robust-kinetic-n{n}.json')
 for d, original in zip(c['problem_data'],source['scenarios']):
  assert mat(d['F'])==mat(original['F']) and mat(d['prior'])==mat(original['prior'])
  assert all(Q(d[x])==Q(original[x]) for x in ('rho','latent_variance','nugget_variance'))
  assert d['k']==original['k']==c['k']
 assert len(set(c['selected']))==c['k']
 if suffix: assert c['selected']==read(f'robust-dense-n{n}.json')['hull_polish']['selected']
 else: assert c['selected']==source['greedy_exchange' if n==48 else 'robust']['selected']
 for d,pair in zip(c['problem_data'],c['selected_logdet_intervals']): encloses_saved(info(d,c['selected']).det(),pair)
 for d,individual in zip(c['problem_data'],c['individual_certificates']):
  encloses_saved(info(d,individual['selected']).det(),[individual['lower_bound'],individual['upper_bound']])
 lo=min(Q(pair[0])-Q(U) for pair,U in zip(c['selected_logdet_intervals'],c['individual_optimum_upper_bounds']))
 assert lo==Q(c['standardized']['lower_bound'])
 assert sum(map(Q,c['dual_weights']))==1 and min(map(Q,c['dual_weights']))>=0
 # Independent tangent constants from rounded references plus shared integer price.
 constant=Q(c['integer_price'],c['score_grid'])
 for d,N,w in zip(c['problem_data'],c['tangent_references'],map(Q,c['dual_weights'])):
  N=mat(N); assert all(N[:j,:j].det()>0 for j in range(1,N.rows+1))
  l,h=logbounds(N.det()); grid=c['log_grid']; upper=Q(-((-h.numerator*grid)//h.denominator),grid)
  constant+=w*(upper-N.rows+Q(s.trace(N.inv(method='DM')*mat(d['prior']))))
 U=min(Q(0),constant-sum((Q(w)*Q(b) for w,b in zip(c['dual_weights'],c['individual_optimum_lower_bounds'])),Q(0)))
 grid=c['log_grid']; U=Q(-((-U.numerator*grid)//U.denominator),grid)
 assert U==Q(c['standardized']['upper_bound'])
 robust.append({'n':n,'polished':bool(suffix),'independent_selected_and_reference_determinants':6,'standardized_interval_exact':True})
report['robust']=robust
# Independent exact nesting and shared sensitivities.
models={n:read(f'latent-separator-n{n}-probe.json')['problem_data'] for n in (48,96,192)}
for n in (48,96):
 coarse,fine=models[n],models[192];factor=192//n
 assert Q(coarse['rho'])==Q(fine['rho'])**factor
 assert mat(coarse['F'])==mat(fine['F']).extract(range(factor-1,192,factor),range(3))
 assert mat(coarse['prior'])==mat(fine['prior']) and coarse['k']==fine['k']==16
report['exact_nesting']=True
# Every separator incumbent re-evaluated under direct selected covariance.
sep=[]
for n,b in [(48,8),(96,12),(96,16),(192,12),(192,16)]:
 c=read(f'latent-separator-n{n}-b{b}-certificate.json');d=c['problem_data']
 assert mat(d['F'])==mat(models[n]['F'])
 assert all(Q(d[x])==Q(models[n][x]) for x in ('rho','latent_variance','nugget_variance'))
 encloses_saved(info(d,c['selected']).det(),[c['lower_bound'],c['upper_bound']])
 A=c['anchors'];G=mat(c['nuisance_witness']);W=mat(c['tangent_reference']).inv(method='DM')
 latent={**d,'nugget_variance':'0'}
 prior=s.trace(W*G.T*cov(latent,A).inv(method='DM')*G)
 assert prior==s.Rational(c['anchor_prior_trace'])
 sep.append({'n':n,'b':b,'selected_inverse_and_anchor_prior_exact':True})
report['separator']=sep
# Independently enumerate all local pattern quadratic scores for archived n48,b8.
c=read('latent-separator-n48-b8-certificate.json');d=c['problem_data'];A=c['anchors'];G=mat(c['nuisance_witness']);W=mat(c['tangent_reference']).inv(method='DM');F=mat(d['F']);K=cov({**d,'nugget_variance':'0'},range(c['n']));H=K[:,A]*K.extract(A,A).inv(method='DM');D=cov(d,range(c['n']))-H*K.extract(A,A)*H.T; adjusted=F+H*G
states={0:s.Rational(0)}; total_patterns=0
for bi,block in enumerate(c['blocks']):
 best={0:s.Rational(0)}
 for size in range(1,len(block)+1):
  for T in itertools.combinations(block,size):
   B=adjusted.extract(T,range(3));value=s.trace(W*B.T*D.extract(T,T).inv(method='DM')*B)
   best[size]=max(best.get(size,value),value); total_patterns+=1
 for size,value in best.items(): assert value<=s.Rational(c['local_count_choices'][bi][str(size)]['integer_score'],c['score_grid'])
 following={}
 for used,value in states.items():
  for size,local in best.items():
   if used+size<=c['k']: following[used+size]=max(following.get(used+size,value+local),value+local)
 states=following
assert states[c['k']]<=s.Rational(c['integer_price'],c['score_grid'])
report['direct_separator_pattern_support']={'patterns':total_patterns,'exact_max':str(states[c['k']]),'saved_integer_price_dominates':True}
report['seconds']=time.perf_counter()-start
Path(__file__).with_name('results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='direct_separator_pattern_support'},indent=2))
print('Exact pattern check PASS:',total_patterns)
