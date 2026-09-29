"""Directed numerical search for four-variable star SDP-RLT gaps.

This is exploratory floating-point computation, never a counterexample certificate.
"""
import itertools
import json
import warnings
import cvxpy as cp
import numpy as np


def star_minimum(A):
    """Eliminate leaves and minimize the resulting piecewise quadratic on [0,1]."""
    q=np.diag(A)[1:]; b=2*A[0,1:]; a=2*A[1,2:]
    cuts=[0.,1.]
    for qi,bi,ai in zip(q[1:],b[1:],a):
        if abs(ai)<1e-14: continue
        for threshold in ([0.,-2*qi] if qi>0 else [-qi]):
            t=(threshold-bi)/ai
            if 0<t<1: cuts.append(t)
    cuts=sorted(set(cuts)); best=(np.inf,None)
    def evaluate(t):
        linear=b[1:]+a*t
        yy=np.array([np.clip(-c/(2*d),0,1) if d>0 else float(d+c<0)
                     for d,c in zip(q[1:],linear)])
        z=np.r_[1,t,yy]
        return float(z@A@z),z[1:]
    for lo,hi in zip(cuts,cuts[1:]):
        mid=(lo+hi)/2; qa=q[0]; qb=b[0]
        for qi,bi,ai in zip(q[1:],b[1:],a):
            c=bi+ai*mid
            if qi>0 and -2*qi<c<0:
                qa-=ai*ai/(4*qi); qb-=bi*ai/(2*qi)
            elif (qi+c<0 if qi<=0 else c<=-2*qi):
                qb+=ai
        points=[lo,hi]
        if qa>0 and lo<-qb/(2*qa)<hi: points.append(-qb/(2*qa))
        for t in points:
            result=evaluate(t)
            if result[0]<best[0]: best=result
    return best


class Relaxation:
    def __init__(self,n=4):
        self.Y=cp.Variable((n+1,n+1),symmetric=True)
        self.A=cp.Parameter((n+1,n+1),symmetric=True)
        x=self.Y[0,1:]; X=self.Y[1:,1:]
        column=cp.reshape(x,(n,1),order='C'); row=cp.reshape(x,(1,n),order='C')
        self.problem=cp.Problem(cp.Minimize(cp.sum(cp.multiply(self.A,self.Y))),
            [self.Y>>0,self.Y[0,0]==1,X>=0,X>=column+row-1,X<=column,X<=row])
    def solve(self,A):
        self.A.value=A
        value=self.problem.solve(solver='CLARABEL',tol_gap_abs=2e-9,
                                 tol_feas=2e-9,tol_gap_rel=2e-9)
        return value,self.Y.value.copy()


def drury_matrix():
    # Drury (2.1); the coefficients below agree with the exact retained example.
    return np.array([[625,-600,527,-600,-175,625],[-600,625,-600,527,625,-175],
                     [527,-600,625,0,0,0],[-600,527,0,625,0,0],
                     [-175,625,0,0,625,0],[625,-175,0,0,0,625]],dtype=float)/625


def restriction(A,pair,endpoints,upper=4):
    """Two selected leaves are affine functions of one common unit variable."""
    T=np.zeros((6,5));T[0,0]=1;T[1,1]=upper
    keep=[i for i in range(2,6) if i not in pair]
    for col,i in enumerate(keep,start=2): T[i,col]=upper
    for i,(left,right) in zip(pair,endpoints):
        T[i,0]=left;T[i,4]=right-left
    B=T.T@A@T
    return B,T


def main():
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--seed',type=int,default=20925)
    parser.add_argument('--samples',type=int,default=3000)
    args=parser.parse_args()
    rng=np.random.default_rng(args.seed); solver=Relaxation(); A=drury_matrix()
    maximum=-np.inf; record=None; count=0
    pairs=list(itertools.combinations(range(2,6),2))
    with warnings.catch_warnings():
        warnings.simplefilter('ignore',UserWarning)
        for k in range(args.samples):
            pair=pairs[k%len(pairs)]
            # Opposite orientations are the only affine merges that need not
            # preserve copositivity of the five-by-five coefficient matrix.
            # Endpoints biased toward the small leaf range in the known witness.
            upper=float(rng.choice([1.,2.,4.,8.]))
            extent=upper if k%4==0 else float(np.exp(rng.uniform(-3,np.log(upper))))
            p=np.sort(rng.uniform(0,extent,2)); r=np.sort(rng.uniform(0,extent,2))[::-1]
            if k%4==0: p[0]=0; r[1]=0
            B,T=restriction(A,pair,[p,r],upper)
            scale=np.linalg.norm(B); B=B/scale
            exact,z=star_minimum(B)
            value,Y=solver.solve(B); gap=exact-value;count+=1
            if gap>maximum:
                maximum=gap; record=dict(k=k,pair=pair,upper=upper,endpoints=[p.tolist(),r.tolist()],
                    true=exact,sdp=value,gap=gap,coefficients=B.tolist(),witness=Y.tolist(),minimizer=z.tolist())
            if gap>1e-6:
                print(json.dumps(dict(status='candidate_only',**record)),flush=True)
                return
            if count%500==0: print(json.dumps(dict(completed=count,maximum_gap=maximum)),flush=True)
    print(json.dumps(dict(status='no_candidate',count=count,best=record)),flush=True)

if __name__=='__main__': main()
