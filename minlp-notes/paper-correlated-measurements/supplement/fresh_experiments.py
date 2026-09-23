"""Fresh, fully specified exact-witness experiments; no commercial solver.

The exhaustive families are intentionally small. Numerical optimization only
proposes witnesses; rational recomputation supplies every certified interval.
"""
from pathlib import Path
from itertools import combinations
from fractions import Fraction
from time import perf_counter
import argparse, json, sys, platform, os
sys.set_int_max_str_digits(0)
sys.dont_write_bytecode = True
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'legacy'))
import sympy as s
import numpy as np
import scipy
from scipy.optimize import minimize
from certify_noisy_markov import log_enclosure
from certify_dense_design import Problem, certify as dense_certify

Q=s.Rational

def frac(x):return Fraction(int(s.numer(x)),int(s.denom(x)))
def logs(x):return log_enclosure(frac(x))
def serial(x):
 if isinstance(x,s.MatrixBase):return [[str(a) for a in row] for row in x.tolist()]
 if isinstance(x,(s.Basic,Fraction)):return str(x)
 if isinstance(x,np.integer):return int(x)
 if isinstance(x,np.floating):return float(x)
 raise TypeError(type(x).__name__)
def trace(A):return s.trace(A)
def schur(M,p):
 if M.rows==p:return M
 return M[:p,:p]-M[:p,p:]*M[p:,p:].inv()*M[p:,:p]
def numeric_schur(M,p):
 if M.shape[0]==p:return M, np.eye(p)
 G=-np.linalg.solve(M[p:,p:],M[p:,:p]);E=np.vstack((np.eye(p),G))
 return E.T@M@E,E

def mixture(atoms,p):
 arr=np.array([np.array(M,float) for M in atoms]);m=len(atoms);price_seconds=0.;calls=0
 def fun(x):
  nonlocal price_seconds,calls
  M=np.einsum('i,ijk->jk',x,arr);J,E=numeric_schur(M,p);W=np.linalg.inv(J)
  t=perf_counter();g=np.einsum('ij,kji->k',E@W@E.T,arr);price_seconds+=perf_counter()-t;calls+=1
  return -np.linalg.slogdet(J)[1],-g
 t=perf_counter();res=minimize(fun,np.full(m,1/m),jac=True,method='SLSQP',bounds=[(0,1)]*m,
  constraints={'type':'eq','fun':lambda x:x.sum()-1,'jac':lambda x:np.ones(m)},
  options={'ftol':1e-12,'maxiter':1000});proposal=perf_counter()-t
 # Feasibility of the certificate mixture is established by construction.
 ints=np.floor(np.maximum(res.x,0)*10**9).astype(np.int64);total=int(ints.sum())
 if total==0:ints[0]=1;total=1
 weights=[Q(int(a),total) for a in ints]
 t=perf_counter();M=sum((a*B for a,B in zip(weights,atoms)),s.zeros(atoms[0].rows));J=schur(M,p)
 G=-M[p:,p:].inv()*M[p:,:p] if M.rows>p else s.zeros(0,p)
 E=s.eye(p).col_join(G);W=J.inv();prices=[trace(W*E.T*B*E) for B in atoms]
 lo,hi=logs(J.det());gap=max(prices)-p
 assert gap>=0 and sum(weights)==1
 upper=hi+frac(gap);cert=perf_counter()-t
 return {'mixture_weights':weights,'mixture_information':J,'nuisance_witness':G,'weight_witness':W,
  'lower':lo,'upper':upper,'gap':upper-lo,'display_lower':float(lo),'display_upper':float(upper),
  'display_gap':float(upper-lo),'price_max':max(prices),'maximizing_atom':prices.index(max(prices)),
  'seconds':{'proposal_total_including_pricing':proposal,'numeric_gradient_pricing_component':price_seconds,
             'exact_certification_including_all_atom_prices':cert},
  'optimizer':{'success':bool(res.success),'message':str(res.message),'iterations':int(res.nit),'evaluations':calls}}

def nested():
 started=perf_counter();n=8;k=3;p=2;rho=Q(3,5)
 F=s.Matrix([[Q(1),Q((3*t+2)%7-3,3)] for t in range(n)]);prior=s.diag(Q(1,10),Q(1,5))
 K=s.Matrix(n,n,lambda i,j:rho**abs(i-j));R=K+s.eye(n)
 schedules=list(combinations(range(n),k));true=[]
 for S in schedules:true.append(prior+F.extract(S,range(p)).T*R.extract(S,S).inv()*F.extract(S,range(p)))
 dets=[M.det() for M in true];best=max(range(len(schedules)),key=lambda i:dets[i]);bestlog=logs(dets[best])
 common_setup=perf_counter()-started;rows=[]
 for A in ((),(3,),(1,3,5),tuple(range(n))):
  t=perf_counter();q=len(A);KA=K.extract(A,A);H=K[:,list(A)]*KA.inv() if q else s.zeros(n,0)
  D=R-H*KA*H.T;Z=F.row_join(H);base=s.diag(prior,KA.inv()) if q else prior
  atoms=[]
  for ix,S in enumerate(schedules):
   ZS=Z.extract(S,range(p+q));M=base+ZS.T*D.extract(S,S).inv()*ZS
   assert schur(M,p)==true[ix];atoms.append(M)
  setup=perf_counter()-t;record=mixture(atoms,p)
  record.update(anchors=A,model_matrix_setup_seconds=setup,discrete_lower=bestlog[0],
                global_discrete_upper=record['upper'],discrete_gap=record['upper']-bestlog[0]);rows.append(record)
 # Exact certificate intervals, not floating optimizer labels, establish strictness.
 for a,b in zip(rows,rows[1:]):assert a['upper']<b['lower']
 # Same true-data incumbent, one scalar virtual-noise relaxation.
 t=perf_counter();Rn=np.array(R,float);Fn=np.array(F,float);Jn=np.array(prior,float)
 aval=Q(int(np.floor(np.linalg.eigvalsh(Rn)[0]*.99*10**8)),10**8)
 assert all((R-aval*s.eye(n))[:i,:i].det()>0 for i in range(1,n+1))
 def densefun(z):
  a=float(aval);V=np.linalg.solve(np.eye(n)+(Rn-a*np.eye(n))*z[None,:]/a,Fn)
  J=Jn+Fn.T@(z[:,None]*V)/a;g=np.einsum('ij,jk,ik->i',V,np.linalg.inv(J),V)/a
  return -np.linalg.slogdet(J)[1],-g
 res=minimize(densefun,np.full(n,k/n),jac=True,method='SLSQP',bounds=[(0,1)]*n,
   constraints={'type':'eq','fun':lambda z:z.sum()-k,'jac':lambda z:np.ones(n)},options={'ftol':1e-12,'maxiter':1000})
 proposal=perf_counter()-t
 from certify_dense_design import round_feasible
 z=round_feasible([str(float(x)) for x in res.x],k,10**8);record={'F':serial(F),'prior':serial(prior),'rho':str(rho),'latent_variance':'1','nugget_variance':'1','k':k}
 t=perf_counter();dc=dense_certify(Problem.read(record),z,frac(aval),{schedules[best]:['common exact optimum']});dc['replay_total_seconds']=perf_counter()-t;dc['proposal_seconds']=proposal
 dc['optimizer']={'success':bool(res.success),'message':str(res.message)}
 # Exact local-information hulls on the identical feasible family.
 local=[]
 for L in (2,4,7):
  t=perf_counter();atoms=[]
  for S in schedules:
   J=prior.copy()
   for tt in S:
    h=[j for j in S if tt-L<=j<tt]
    b=R.extract([tt],h)*R.extract(h,h).inv() if h else s.zeros(1,0)
    d=R[tt,tt]-(b*R.extract(h,[tt]))[0] if h else R[tt,tt]
    f=F[tt,:]-b*F.extract(h,range(p));J+=f.T*f/d
   atoms.append(J)
  setup=perf_counter()-t
  T=rho**(L+1)/(1-rho);N=rho**(L+2)*(1-rho**L)*(1-rho**(L+1))/((1-rho)*(1-rho**2))
  delta=Q(0) if L==n-1 else 2*(T+Q(1,2)*N)
  if delta>=1:local.append({'L':L,'delta':delta,'status':'bound >= 1; no transfer'});continue
  upperatoms=[prior+(J-prior)/(1-delta) for J in atoms]
  rr=mixture(upperatoms,p);rr.update(L=L,delta=delta,model_matrix_setup_seconds=setup,discrete_gap=rr['upper']-bestlog[0]);local.append(rr)
 assert local[-1]['lower']==rows[0]['lower'] and local[-1]['upper']==rows[0]['upper']
 return {'status':'passed','model':record,'n':n,'p':p,'schedule_count':len(schedules),'schedules':schedules,
  'common_optimal_selection':schedules[best],'common_optimal_determinant':dets[best],
  'common_discrete_log_interval':bestlog,'common_setup_seconds':common_setup,'nested':rows,'local':local,'dense':dc,
  'exact_schur_identities_checked':len(schedules)*len(rows),'total_wall_seconds':perf_counter()-started}

def blocks():
 started=perf_counter();n=8;d=3;k=3;L=3;rho=Q(2,5);prior=Q(1,100)
 shift=s.zeros(d)
 for i in range(d):shift[i,(i+1)%d]=1
 A=rho*(shift+s.diag(*[(-1)**i for i in range(d)]))/2
 assert A*A.T!=A.T*A
 # Triangle bound ||A|| <= rho is exact; no eigenvalue assertion is needed.
 F=s.Matrix([Q((7*t+3*j)%13-6,10) for t in range(n) for j in range(d)])
 R=s.zeros(n*d)
 for i in range(n):
  for j in range(n):R[i*d:(i+1)*d,j*d:(j+1)*d]=2*s.eye(d) if i==j else A**(i-j) if i>j else (A**(j-i)).T
 T=rho**(L+1)/(1-rho);N=rho**(L+2)*(1-rho**L)*(1-rho**(L+1))/((1-rho)*(1-rho**2))
 old=2*T*(1+rho*(1-rho**L)/(2*(1-rho)));new=2*(T+N/2)
 cache={};values=[];schedules=list(combinations(range(n),k));setup=perf_counter()-started;t=perf_counter()
 for S in schedules:
  local=Q(0)
  for tt in S:
   h=tuple(j for j in S if tt-L<=j<tt);key=(tt,h)
   if key not in cache:
    ti=list(range(d*tt,d*(tt+1)));hi=[d*j+c for j in h for c in range(d)]
    b=R.extract(ti,hi)*R.extract(hi,hi).inv() if hi else s.zeros(d,0)
    D=R.extract(ti,ti)-b*R.extract(hi,ti);f=F.extract(ti,[0])-b*F.extract(hi,[0])
    cache[key]=(f.T*D.inv()*f)[0]
   local+=cache[key]
  si=[d*j+c for j in S for c in range(d)];true=prior+(F.extract(si,[0]).T*R.extract(si,si).inv()*F.extract(si,[0]))[0]
  assert (1-new)*(true-prior)<=local<=(1+new)*(true-prior)
  values.append((local,true))
 exact_seconds=perf_counter()-t;best=max(range(len(values)),key=lambda j:values[j][0]);lb=values[best][1]
 upperold=prior+values[best][0]/(1-old);uppernew=prior+values[best][0]/(1-new)
 assert uppernew<upperold and max(v[1] for v in values)<=uppernew
 # Same formulas evaluated on archived d=4,d=16 examples; these are fresh
 # constant comparisons, not changes to the archived numerical certificates.
 archived=[]
 for dd in (4,16):
  record=json.loads((HERE/'legacy/results'/f'block-snapshot-d{dd}-probe.json').read_text(),parse_float=str)
  assert record['d']==dd and record['L']==6 and Q(record['rho'])==rho
  assert record['metadata']['noise_model']=='STYLIZED stationary latent VAR(1) with P=I, V=I, Q=I-AA^T; known mean-independent covariance'
  stored_A=s.Matrix([[Q(v) for v in row] for row in record['A']]);cyclic=2*stored_A/rho-s.diag(*[(-1)**i for i in range(dd)])
  assert cyclic*cyclic.T==s.eye(dd) and all(v in (0,1) for v in cyclic)
  assert all(sum(cyclic[i,j] for j in range(dd))==1 for i in range(dd))
  assert stored_A*stored_A.T!=stored_A.T*stored_A
  np.testing.assert_allclose(np.array(record['Q'],float),np.array(s.eye(dd)-stored_A*stored_A.T,float),atol=2e-16,rtol=0)
  ll=record['L'];tt=rho**(ll+1)/(1-rho);nn=rho**(ll+2)*(1-rho**ll)*(1-rho**(ll+1))/((1-rho)*(1-rho**2))
  archived.append({'d':dd,'L':ll,'old_delta':2*tt*(1+rho*(1-rho**ll)/(2*(1-rho))),
                   'sharp_far_delta':2*(tt+nn/2)})
 return {'status':'passed','model':{'n':n,'d':d,'k':k,'L':L,'rho':rho,'A':A,'F':F,'prior':prior,'latent_covariance':'I','noise_covariance':'I'},
  'schedule_count':len(schedules),'selected':schedules[best],'local_price':values[best][0],
  'true_lower':lb,'exhaustive_true_optimum':max(v[1] for v in values),'old_delta':old,'sharp_far_delta':new,
  'old_upper':upperold,'sharp_far_upper':uppernew,'old_relative_gap':(upperold-lb)/lb,'sharp_far_relative_gap':(uppernew-lb)/lb,
  'exact_sandwiches_checked':len(values),'unique_local_regressions':len(cache),'archived_constant_comparisons':archived,
  'seconds':{'model_setup':setup,'exact_exhaustive_pricing_and_certification':exact_seconds,'total':perf_counter()-started}}

def main():
 parser=argparse.ArgumentParser();parser.add_argument('study',choices=['nested','blocks','all']);parser.add_argument('--output',type=Path);args=parser.parse_args()
 report={'provenance':'Fresh 2026-09-13 study; exact rational inputs and certificates, numerical SLSQP proposals',
 'environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'sympy':s.__version__,
 'threads':{v:os.environ.get(v) for v in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS')}}}
 for name in ('nested','blocks'):
  if args.study in (name,'all'):report[name]=globals()[name]()
 output=args.output or HERE/'results'/f'fresh-{args.study}.json';output.parent.mkdir(parents=True,exist_ok=True)
 output.write_text(json.dumps(report,default=serial,indent=2)+'\n');print(output)
if __name__=='__main__':main()
