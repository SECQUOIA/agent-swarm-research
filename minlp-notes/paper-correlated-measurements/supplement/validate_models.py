"""Independent model-level diagnostics and exact saved fresh-hull checks."""
from pathlib import Path
from itertools import combinations
from fractions import Fraction as Q
import sys,json
from time import perf_counter
sys.set_int_max_str_digits(0);sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE/'legacy'))
import numpy as np
import mpmath as mp
import sympy as s
from review_noisy_markov_kinetics import augmented_generator,augmented_trajectory,exact_number
from certify_noisy_markov import log_enclosure

def verify_mixture_information(M,p,G,stored):
 """Check the minimizing nuisance witness before using a mixture lower bound."""
 q=M.rows-p
 assert M==M.T and G.shape==(q,p)
 E=s.eye(p).col_join(G);quadratic=E.T*M*E
 if q:
  C=M[p:,p:];B=M[:p,p:]
  assert all(C[:i,:i].det()>0 for i in range(1,q+1)),'nuisance block is not SPD'
  assert C*G+B.T==s.zeros(q,p),'nuisance witness is not stationary'
  direct=M[:p,:p]-B*C.inv()*B.T
 else:
  direct=M[:p,:p]
 assert direct==quadratic==s.Matrix(stored),'mixture Schur information mismatch'
 return direct

def run():
 t=perf_counter();rows=[];entries=0;hp_rows=0
 for n in (48,96):
  name='noisy-markov-kinetics-'+('probe' if n==48 else 'n96-probe')+'.json'
  data=json.loads((HERE/'legacy/results'/name).read_text())
  for r in data['results']:
   model=r['kinetics'];times=np.array(model['candidate_times']);pars=[model[k] for k in ('A0','k1','k2')]
   trajectory=augmented_trajectory(times,*pars);error=float(abs(trajectory[:,[4,7,10]]-r['F']).max());assert error<2e-11
   entries+=3*n
   hp_error=mp.mpf(0)
   with mp.workdps(70):
    M,y0=augmented_generator(*map(exact_number,pars),high_precision=True)
    for j in sorted(set((0,int(np.argmin(abs(times-model['nominal_peak_time']))),n//2-1,n-1))):
     y=mp.expm(M*exact_number(times[j]))*y0
     for c,ix in enumerate((4,7,10)):hp_error=max(hp_error,abs(y[ix]-exact_number(r['F'][j][c])))
     hp_rows+=1
    assert hp_error<mp.mpf('2e-14')
    hp_display=mp.nstr(hp_error,18)
   rows.append({'n':n,'rates':pars[1:],'ode_max_absolute_error':error,'matrix_exponential_max_error':hp_display})
 # Independently reconstruct joint nuisance information using the complete
 # inverse joint covariance of (U,Y_S), rather than the producer's block formula.
 fresh=json.loads((HERE/'results/fresh-all.json').read_text());d=fresh['nested'];model=d['model'];n=d['n'];p=d['p']
 F=s.Matrix(model['F']);prior=s.Matrix(model['prior']);rho=s.Rational(model['rho']);K=s.Matrix(n,n,lambda i,j:rho**abs(i-j));R=K+s.eye(n)
 assert n==8 and p==2 and model['k']==3 and rho==s.Rational(3,5)
 assert prior==s.diag(s.Rational(1,10),s.Rational(1,5))
 assert F==s.Matrix([[1,s.Rational((3*t+2)%7-3,3)] for t in range(n)])
 schedules=[tuple(S) for S in d['schedules']];assert schedules==list(combinations(range(n),model['k']))
 lower=Q(d['common_discrete_log_interval'][0]);true_dets=[];true_matrices=[];identities=0;priced=0
 for S in schedules:
  FS=F.extract(S,range(p));Jtrue=prior+FS.T*R.extract(S,S).inv()*FS;true_matrices.append(Jtrue);true_dets.append(Jtrue.det())
 assert max(true_dets)==s.Rational(d['common_optimal_determinant'])
 for row in d['nested']:
  A=row['anchors'];q=len(A);atoms=[]
  for j,S in enumerate(schedules):
   joint=K.extract(A,A).row_join(K.extract(A,S)).col_join(K.extract(S,A).row_join(R.extract(S,S)))
   # The nuisance variable is a mean-shift coefficient of the latent anchor;
   # its induced observed loading is H, so whitened joint response means are
   # (u, F theta + H u), with covariance blockdiag(K_A,D_SS).
   # A direct equivalent precision uses transform from (U,Y) to (U,Y-HU).
   H=K.extract(S,A)*K.extract(A,A).inv() if q else s.zeros(len(S),0)
   means=s.zeros(q,p).row_join(s.eye(q)).col_join(F.extract(S,range(p)).row_join(H))
   # Cov(U, residual Y-HU)=0; form it by an explicit congruence of joint data.
   T=s.eye(q+len(S));T[q:,:q]=-H;C=T*joint*T.T
   M=s.diag(prior,s.zeros(q))+means.T*C.inv()*means
   J=M[:p,:p]-M[:p,p:]*M[p:,p:].inv()*M[p:,:p] if q else M
   assert J==true_matrices[j];identities+=1;atoms.append(M)
  weights=[s.Rational(v) for v in row['mixture_weights']];assert all(x>=0 for x in weights) and sum(weights)==1
  M=sum((w*B for w,B in zip(weights,atoms)),s.zeros(p+q));G=s.Matrix(row['nuisance_witness']) if q else s.zeros(0,p);W=s.Matrix(row['weight_witness'])
  assert all(W[:i,:i].det()>0 for i in range(1,p+1));E=s.eye(p).col_join(G)
  N=verify_mixture_information(M,p,G,row['mixture_information']);assert W*N==s.eye(p)
  atomprices=[s.trace(W*E.T*B*E) for B in atoms];lo,hi=log_enclosure(Q(str(N.det())))
  upper=hi+Q(str(max(atomprices)-p));assert lo==Q(row['lower']) and upper==Q(row['upper']);priced+=len(atoms)
 for a,b in zip(d['nested'],d['nested'][1:]):assert Q(a['upper'])<Q(b['lower'])
 return {'status':'passed','ode_entries':entries,'matrix_exponential_rows':hp_rows,'sensitivity_cases':rows,
 'fresh_joint_schur_identities':identities,'fresh_exact_support_prices':priced,'wall_seconds':perf_counter()-t,
 'scope':'ODE/matrix-exponential comparisons are numerical diagnostics; rational fresh-hull identities and supports are exact'}
if __name__=='__main__':
 result=run();(HERE/'results/model-validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
