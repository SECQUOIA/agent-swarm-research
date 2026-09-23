from pathlib import Path
import json, sys, time
import sympy as s
from fractions import Fraction as Q
sys.set_int_max_str_digits(0)
sys.dont_write_bytecode=True
BASE=Path(__file__).resolve().parents[2]/'supplement'
DATA=BASE/'legacy/results'
sys.path.insert(0,str(BASE/'legacy'))
from certify_noisy_markov import log_enclosure, local_coefficients
from certify_partial_trace import local_pattern
from integer_interval_scores import IntegerIntervalScores
def read(n):return json.loads((DATA/(n+'.json')).read_text(),parse_float=str)
def mat(a):return s.Matrix([[s.Rational(x) for x in row] for row in a])
def cov(d):
 n=len(d['F']);r=s.Rational(d['rho']);v=s.Rational(d['latent_variance']);w=s.Rational(d['nugget_variance'])
 return s.Matrix(n,n,lambda i,j:v*r**abs(i-j)+(w if i==j else 0))
def logbounds(x):return tuple(map(s.Rational,log_enclosure(Q(x))))
def selected_J(d,S):
 R=cov(d).extract(S,S);F=mat(d['F']).extract(S,range(len(d['prior'])))
 return mat(d['prior'])+F.T*R.inv(method='DM')*F
start=time.perf_counter();checks=[]
# Independent dense linear solve, rather than the archived tridiagonal oracle.
dense=read('dense-design-kinetics-n48-certificates')['results'][0]
d=dense['problem_data'];R=cov(d);F=mat(d['F']);P=mat(d['prior']);n=R.rows
z=list(map(s.Rational,dense['tangent_z']));a=s.Rational(dense['a']);Z=s.diag(*[x/a for x in z])
V=(s.eye(n)+(R-a*s.eye(n))*Z).inv(method='DM')*F
J=P+F.T*Z*V
assert J==mat(dense['information'])
gradient=[(V[i,:]*J.inv()*V[i,:].T)[0]/a for i in range(n)]
assert gradient==list(map(s.Rational,dense['gradient']))
Jinc=selected_J(d,dense['incumbent_selection']);assert Jinc.det()==s.Rational(dense['incumbent_determinant'])
checks.append('direct dense inverse: complete n48 kinetic information, 48 gradients and incumbent determinant')
print(checks[-1],flush=True)
# All scalar endpoint value reconstructed as a selected virtual covariance.
aa=read('dense-all-splits-kinetics-n48-certificates')['results'][0]
za=list(map(s.Rational,aa['feasible_point']));T=[i for i,x in enumerate(za) if x>0]
Sa=R.extract(T,T)+s.diag(*[s.Rational(aa['upper_split'])*(1-za[i])/za[i] for i in T])
Fa=F.extract(T,range(F.cols));Ja=P+Fa.T*Sa.inv(method='DM')*Fa
assert Ja.det()==s.Rational(aa['information_determinant'])
checks.append('direct all-scalar endpoint virtual covariance determinant')
print(checks[-1],flush=True)
# Diagonal split: reconstruct point and gradient independently of legacy filter.
dd=read('diagonal-split-kinetics-certificate');zd=list(map(s.Rational,dd['selection_point']));ad=list(map(s.Rational,dd['reference_diagonal']))
T=[i for i,x in enumerate(zd) if x>0];h=[(1-zd[i])/zd[i] for i in T]
Sd=R.extract(T,T)+s.diag(*[ad[i]*hh for i,hh in zip(T,h)])
Fd=F.extract(T,range(F.cols));Vi=Sd.inv(method='DM')*Fd;Jd=P+Fd.T*Vi
gd=[s.S(0)]*n
for row,(i,hh) in enumerate(zip(T,h)):gd[i]=-hh*(Vi[row,:]*Jd.inv()*Vi[row,:].T)[0]
dual=dd['dual_certificate'];B=mat(dual['factor']);c=list(map(s.Rational,dual['diagonal_correction']));Y=B*B.T+s.diag(*c)
assert min(c)>=0 and all(Y[i,i]>=-gd[i] for i in range(n))
lb=logbounds(Jd.det())[0]-sum(gd[i]*ad[i] for i in range(n))-s.trace(R*Y)
assert lb==s.Rational(dd['all_diagonal_lower_bound'])
checks.append('direct all-diagonal covariance, 48 derivative entries and factor-certified dual lower bound')
print(checks[-1],flush=True)
# All table scalar certified inequalities checked against exact fractions.
gm=['.00270073','.00187230','.00387283','.00183482','.00186234','.00178161','.00190758','.00182972','.00193602','.00194271']
gc=['1.12e-7','6.48e-8','8.39e-8','1.62e-7','6.63e-8','3.54e-7','5.19e-7','6.27e-7','6.64e-7','1.30e-6']
sep=['.04721614','.03593564','.04639027','.03913455','.02276202','.02635127','.10923746','.08378101','.10436604','.08771349']
mem=[read(f'noisy-markov-extended-certificate-{i}') for i in range(6)]+[read(f'noisy-markov-kinetics-certificate-n{n}-{r}') for n in (48,96) for r in ('fast','slow')]
denses=sum([read(name)['results'] for name in ['dense-design-exact-certificates','dense-design-kinetics-n48-certificates','dense-design-kinetics-n96-certificates']],[])
alls=sum([read(name)['results'] for name in ['dense-all-splits-certificates','dense-all-splits-kinetics-n48-certificates','dense-all-splits-kinetics-n96-certificates']],[])
for i,(m,de,al) in enumerate(zip(mem,denses,alls)):
 assert Q(m['gap'])<=Q(gm[i]) and Q(de['continuous_certificate_gap'])<=Q(gc[i]) and Q(al['all_splits_lower_bound'])-Q(m['upper_bound'])>=Q(sep[i])
checks.append('all 30 scalar-table certified inequalities round outward')
# Independent covariance conditioning for scalar and partial local patterns.
for ages in [(),(1,),(8,4,1),(8,7,5,3,1),tuple(range(8,0,-1))]:
 for partial in (False,True):
  ts=tuple(-x for x in ages)+(0,);v=s.Rational(1,800)
  def cv(i,j):
   h=abs(ts[i]-ts[j]);return v*((s.Rational(9,25)*s.Rational(2,5)**h+s.Rational(16,25)*s.Rational(1,5)**h) if partial else s.Rational(2,5)**h)+(v if i==j else 0)
  C=s.Matrix(len(ts),len(ts),cv)
  if ages:b=C[-1,:-1]*C[:-1,:-1].inv(method='DM');dv=C[-1,-1]-(b*C[:-1,-1])[0]
  else:b=s.zeros(1,0);dv=C[-1,-1]
  got=local_pattern(ages,Q(1,800)) if partial else local_coefficients(ts[:-1],0,Q(2,5),Q(1,800),Q(1,800))
  assert list(b)==list(map(s.Rational,got[0])) and dv==s.Rational(got[1])
checks.append('10 independent scalar/two-mode local covariance Schur checks')
# Direct covariance selected inverse for all 4 partial incumbents.
partialrows=read('partial-observation-trace-probe')['results']
for ix in range(4):
 rr=read(f'partial-observation-trace-certificate-{ix}');dd=partialrows[rr['input_case_index']];S=rr['selected'];v=s.Rational(dd['variance'])
 C=s.Matrix(len(S),len(S),lambda i,j:v*(s.Rational(9,25)*s.Rational(2,5)**abs(S[i]-S[j])+s.Rational(16,25)*s.Rational(1,5)**abs(S[i]-S[j])+(1 if i==j else 0)))
 FF=mat(dd['F']).extract(S,range(3));JJ=mat(dd['prior'])+FF.T*C.inv(method='DM')*FF
 assert s.trace(mat(dd['W'])*JJ)==s.Rational(rr['lower_bound'])
 assert Q(rr['relative_gap'])*100<=Q(['.059924','.059732','.060361','.059925'][ix])
checks.append('four complete partial-incumbent covariance inverses and all rounded percentages')
out={'status':'passed','checks':checks,'seconds':time.perf_counter()-start}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
