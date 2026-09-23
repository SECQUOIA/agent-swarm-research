from pathlib import Path
from itertools import combinations
import sys,json
import sympy as s
import mpmath as mp
sys.set_int_max_str_digits(0)
Q=s.Rational
ROOT=Path(__file__).resolve().parents[2]
d=json.loads((ROOT/'supplement/results/fresh-all.json').read_text())
def mat(x):return s.Matrix([[Q(v) for v in row] for row in x])
def schur(M,p):return M[:p,:p]-M[:p,p:]*M[p:,p:].inv()*M[p:,:p] if M.rows>p else M
# Independent high-precision logarithms supplement exact rational identities.
mp.mp.dps=90
def ln(x):return mp.log(mp.mpf(str(s.numer(x)))/mp.mpf(str(s.denom(x))))
def num(x):x=Q(x);return mp.mpf(str(s.numer(x)))/mp.mpf(str(s.denom(x)))
def pd(M):
 assert M==M.T
 _,D=M.LDLdecomposition(hermitian=False)
 assert all(v>0 for v in D.diagonal())
r=d['nested'];n=8;p=2;rho=Q(3,5);K=s.Matrix(n,n,lambda i,j:rho**abs(i-j));R=K+s.eye(n)
F=s.Matrix([[1,Q((3*t+2)%7-3,3)] for t in range(n)]);prior=s.diag(Q(1,10),Q(1,5));ss=list(combinations(range(n),3))
assert [list(x) for x in ss]==r['schedules']
true=[prior+F.extract(S,range(p)).T*R.extract(S,S).inv()*F.extract(S,range(p)) for S in ss]
best=max(M.det() for M in true);bestsets=[S for S,M in zip(ss,true) if M.det()==best]
assert bestsets==[tuple(r['common_optimal_selection'])]==[(1,4,6)]
assert best==Q(r['common_optimal_determinant'])
assert num(r['common_discrete_log_interval'][0])<=ln(best)<=num(r['common_discrete_log_interval'][1])
levels=[]
for row in r['nested']:
 A=row['anchors'];q=len(A)
 # Derive information through joint precision using observed Y and independent
 # latent anchor prior, then eliminate anchors. Model arrays constructed above.
 KA=K.extract(A,A);H=K[:,A]*KA.inv() if q else s.zeros(n,0);D=R-H*KA*H.T
 atoms=[]
 for i,S in enumerate(ss):
  B=F.extract(S,range(p)).row_join(H.extract(S,range(q)))
  M=s.diag(prior,KA.inv())+B.T*D.extract(S,S).inv()*B if q else true[i]
  assert schur(M,p)==true[i];atoms.append(M)
 weights=list(map(Q,row['mixture_weights']));assert len(weights)==len(ss) and min(weights)>=0 and sum(weights)==1
 M=sum((w*B for w,B in zip(weights,atoms)),s.zeros(p+q));J=schur(M,p);G=mat(row['nuisance_witness']) if q else s.zeros(0,p);W=mat(row['weight_witness'])
 assert J==mat(row['mixture_information']);pd(J);pd(W);assert W*J==s.eye(p)
 assert M[p:,:p]+M[p:,p:]*G==s.zeros(q,p)
 E=s.eye(p).col_join(G);prices=[s.trace(W*E.T*B*E) for B in atoms]
 assert max(prices)==Q(row['price_max']) and prices[row['maximizing_atom']]==max(prices)
 assert num(row['lower'])<=ln(J.det())<=num(row['upper'])-num(max(prices)-p)
 levels.append((num(row['lower']),num(row['upper'])))
for a,b in zip(levels,levels[1:]):assert a[1]<b[0]
# Dense extension: compute inverse effective covariance directly on positive support.
x=r['dense'];a=Q(x['a']);z=list(map(Q,x['tangent_z']));assert sum(z)==3 and min(z)>=0 and max(z)<=1;pd(R-a*s.eye(n))
T=[i for i,v in enumerate(z) if v>0];Rt=R.extract(T,T)+s.diag(*[a*(1-z[i])/z[i] for i in T]);Ft=F.extract(T,range(p));J=prior+Ft.T*Rt.inv()*Ft
assert J==mat(x['information'])
V=(s.eye(n)+(R-a*s.eye(n))*s.diag(*[v/a for v in z])).inv()*F
g=[(V[i,:]*J.inv()*V[i,:].T)[0]/a for i in range(n)];gap=sum(sorted(g,reverse=True)[:3])-sum(gg*zz for gg,zz in zip(g,z))
assert g==list(map(Q,x['gradient'])) and gap==Q(x['tangent_gap'])
assert num(x['continuous_lower_bound'])<=ln(J.det())<=num(x['upper_bound'])-num(gap)
assert levels[2][1]<num(x['continuous_lower_bound'])<num(x['upper_bound'])<levels[3][0]
assert num(x['upper_bound'])<mp.mpf('.839905825') and num(x['continuous_certificate_gap'])<mp.mpf('1.14e-7')
# Complete-block fixture. Independent state-space construction using independent
# initial state and process noises rather than direct lag covariance formula.
b=d['blocks'];dd=3;nn=8;A=mat(b['model']['A']);FF=mat(b['model']['F']);PP=Q(1,100);rho=Q(2,5);L=3
pd(s.eye(dd)-A*A.T);assert A*A.T!=A.T*A
B=s.zeros(nn*dd)
for t in range(nn):
 for j in range(t+1):B[t*dd:(t+1)*dd,j*dd:(j+1)*dd]=A**(t-j)
Qbig=s.diag(s.eye(dd),*[s.eye(dd)-A*A.T]*(nn-1));RR=B*Qbig*B.T+s.eye(nn*dd)
T=rho**(L+1)/(1-rho);N=rho**(L+2)*(1-rho**L)*(1-rho**(L+1))/((1-rho)*(1-rho**2))
old=2*T*(1+rho*(1-rho**L)/(2*(1-rho)));new=2*(T+N/2);assert old==Q(b['old_delta']) and new==Q(b['sharp_far_delta'])
vals=[]
for S in ss:
 idx=[dd*t+j for t in S for j in range(dd)];RS=RR.extract(idx,idx);FS=FF.extract(idx,[0]);local=Q(0);tr=s.eye(dd*3);D=s.zeros(dd*3)
 for pos,t in enumerate(S):
  hist=[u for u in S if t-L<=u<t];hi=[dd*u+j for u in hist for j in range(dd)];ti=list(range(dd*t,dd*(t+1)))
  beta=RR.extract(ti,hi)*RR.extract(hi,hi).inv() if hi else s.zeros(dd,0)
  Dt=RR.extract(ti,ti)-beta*RR.extract(hi,ti);ft=FF.extract(ti,[0])-beta*FF.extract(hi,[0]);local+=(ft.T*Dt.inv()*ft)[0]
  D[pos*dd:(pos+1)*dd,pos*dd:(pos+1)*dd]=Dt
  for hpos,u in enumerate(hist):
   j=S.index(u);tr[pos*dd:(pos+1)*dd,j*dd:(j+1)*dd]=-beta[:,hpos*dd:(hpos+1)*dd]
 C=tr*RS*tr.T
 pd(C-(1-new)*D);pd((1+new)*D-C)
 trueinfo=PP+(FS.T*RS.inv()*FS)[0];vals.append((S,local,trueinfo))
 assert (1-new)*(trueinfo-PP)<=local<=(1+new)*(trueinfo-PP)
locmax=max(v[1] for v in vals);sel=tuple(b['selected']);lb=next(v[2] for v in vals if v[0]==sel)
assert next(v[1] for v in vals if v[0]==sel)==locmax==Q(b['local_price'])
assert max(v[2] for v in vals)==Q(b['exhaustive_true_optimum'])==lb
for name,delta in [('old',old),('sharp_far',new)]:
 ub=PP+locmax/(1-delta);assert ub==Q(b[name+'_upper']);assert (ub-lb)/lb==Q(b[name+'_relative_gap'])
assert lb>Q('.90391527') and Q(b['old_upper'])<Q('1.01644959') and Q(b['sharp_far_upper'])<Q('1.00735957')
assert old<Q('.111957334') and new<Q('.103863638')
assert 100*Q(b['old_relative_gap'])<Q('12.4497') and 100*Q(b['sharp_far_relative_gap'])<Q('11.4441')
report={'status':'passed','nested_exact_atoms':224,'nested_optimal_nuisance_residuals':4,'nested_complete_support_prices':224,'dense_effective_covariance_gradient_and_comparison':'passed','block_independent_state_space_covariance':'passed','block_full_matrix_sandwiches':112,'block_complete_schedules':56,'all_fresh_reported_inequalities':'passed','note':'Log checks use independent 90-digit diagnostics; rational identities and full matrix LDL signs are exact.'}
(Path(__file__).resolve().parent/'checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
