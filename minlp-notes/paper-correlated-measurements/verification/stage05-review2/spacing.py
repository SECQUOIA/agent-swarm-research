from pathlib import Path
import sys,json,time
import sympy as s
from fractions import Fraction as Q
sys.set_int_max_str_digits(0);sys.dont_write_bytecode=True
B=Path(__file__).resolve().parents[2]/'supplement';sys.path.insert(0,str(B/'legacy'))
from integer_interval_scores import IntegerIntervalScores
def read(n):return json.loads((B/'legacy/results'/f'{n}.json').read_text(),parse_float=str)
start=time.perf_counter();old=read('noisy-markov-spacing-kinetics-certificate');interval=read('noisy-markov-spacing-kinetics-integer-certificate')
assert old['problem_data']==interval['problem_data'] and old['tangent_reference']==interval['tangent_reference'] and old['delta']==interval['delta']
d=old['problem_data'];n=old['n'];L=old['L'];k=d['k'];g=d['minimum_gap'];r=Q(d['rho']);v=Q(d['latent_variance']);w=Q(d['nugget_variance'])
F=[list(map(Q,row)) for row in d['F']];NN=s.Matrix([[s.Rational(x) for x in row] for row in old['tangent_reference']]);HI=NN.inv()/(1-s.Rational(old['delta']));H=[[Q(x) for x in row] for row in HI.tolist()]
sc= IntegerIntervalScores(F,H,coefficient_grid=10**12,feature_grid=10**18,score_grid=10**8)
patterns={};scores={};diffs=[]
def score(t,hist):
 key=t,hist
 if key in scores:return scores[key]
 ages=tuple(t-u for u in hist)
 if ages not in patterns:
  C=s.Matrix(len(ages),len(ages),lambda i,j:s.Rational(v*r**abs(ages[i]-ages[j])+(w if i==j else 0)))
  cross=s.Matrix(1,len(ages),lambda i,j:s.Rational(v*r**ages[j]))
  beta=cross*C.inv(method='DM') if ages else s.zeros(1,0)
  variance=s.Rational(v+w)-(beta*cross.T)[0] if ages else s.Rational(v+w)
  bb=tuple(Q(x) for x in beta);dd=Q(variance)
  patterns[ages]=(bb,dd,sc.prepare(ages,bb,dd))
 bb,dd,prepared=patterns[ages]
 f=[F[t][j]-sum((b*F[u][j] for b,u in zip(bb,hist)),Q(0)) for j in range(3)]
 exact=sum((H[i][j]*f[i]*f[j] for i in range(3) for j in range(3)),Q(0))/dd
 e=-((-exact.numerator*10**8)//exact.denominator);i=sc.upper(t,prepared)
 assert i>=e
 diffs.append(i-e);scores[key]=(e,i);return e,i
states={(0,()):(0,0)}
for t in range(n):
 nxt={}
 def offer(key,a,b):
  old=nxt.get(key,(-1,-1));nxt[key]=(max(old[0],a),max(old[1],b))
 for (count,hist),(e,i) in states.items():
  nh=tuple(u for u in hist if u>=t+1-L)
  if count+n-t-1>=k:offer((count,nh),e,i)
  if count<k and (not hist or t-hist[-1]>=g):
   de,di=score(t,hist);offer((count+1,nh+(t,)),e+de,i+di)
 states=nxt
priceE=max(x[0] for (c,h),x in states.items() if c==k);priceI=max(x[1] for (c,h),x in states.items() if c==k)
assert priceE==old['integer_price'] and priceI==interval['integer_price']
assert len(diffs)==31900 and diffs.count(1)==418 and max(diffs)==1
out={'status':'passed','independent_covariance_patterns':len(patterns),'direct_exact_quadratics':len(diffs),'interval_one_unit_increases':diffs.count(1),'exact_price':priceE,'interval_price':priceI,'seconds':time.perf_counter()-start}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
