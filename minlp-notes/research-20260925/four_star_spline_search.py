"""Exploratory search at nonnegative scalar-envelope boundary; floating point only."""
import argparse
import json
import warnings
import numpy as np
from scipy.optimize import linprog
from four_star_countersearch import Relaxation, star_minimum


def coefficients(intervals,weights,parabola,binary=0):
    A=np.zeros((5,5)); A[0,0]=parabola[2];A[0,1]=A[1,0]=parabola[1]/2;A[1,1]=parabola[0]
    for j,((lo,hi),c) in enumerate(zip(intervals,weights),start=2):
        if j<2+binary:
            A[j,j]=-c;A[0,j]=A[j,0]=c*(1+lo)/2;A[1,j]=A[j,1]=-c/2
        else:
            w=hi-lo;A[j,j]=c*w*w;A[0,j]=A[j,0]=c*w*lo;A[1,j]=A[j,1]=-c*w
    return A


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--samples',type=int,default=3000)
    parser.add_argument('--seed',type=int,default=89252);parser.add_argument('--binary',type=int,default=0,choices=range(4));args=parser.parse_args()
    rng=np.random.default_rng(args.seed);solver=Relaxation();maximum=-np.inf;best=None
    grid=np.linspace(0,1,401);parabolas=np.array([grid**2,grid,np.ones_like(grid)]).T
    with warnings.catch_warnings():
        warnings.simplefilter('ignore',UserWarning)
        for k in range(args.samples):
            if k%4==0:
                # Three separated clipping intervals can create four convex basins.
                six=np.sort(rng.uniform(-.1,1.1,6));intervals=six.reshape(3,2)
            elif k%4==1:
                points=np.sort(rng.uniform(-.3,1.3,(3,2)),axis=1);intervals=points
            elif k%4==2:
                lo=rng.uniform(-.1,.8,3);width=np.exp(rng.uniform(-2.8,.2,3));intervals=np.c_[lo,lo+width]
            else:
                lo=rng.uniform(-.3,.6);hi=lo+rng.uniform(.1,.9);w=rng.uniform(.1,1.3)
                intervals=np.array([[lo,hi],[1-hi,1-lo],[(1-w)/2,(1+w)/2]])
            weights=np.exp(rng.uniform(-2,2,3));weights/=weights.sum()
            if k%4==3: weights[1]=weights[0];weights/=weights.sum()
            g=sum(c*np.maximum(grid-lo,0) if j<args.binary else c*(np.maximum(grid-lo,0)**2-np.maximum(grid-hi,0)**2) for j,((lo,hi),c) in enumerate(zip(intervals,weights)))
            mu=rng.uniform(.05,.95);nu=mu*mu+rng.uniform(.05,.95)*(mu-mu*mu)
            if k%4==3:mu=.5;nu=.25+rng.uniform(.05,.95)*.25
            lp=linprog([nu,mu,1],A_ub=-parabolas,b_ub=-g,bounds=[(None,None)]*3,method='highs')
            if not lp.success:raise RuntimeError(lp.message)
            matrix=coefficients(intervals,weights,lp.x,args.binary);norm=np.linalg.norm(matrix);matrix/=norm
            exact,z=star_minimum(matrix);value,Y=solver.solve(matrix);gap=exact-value
            if gap>maximum:
                maximum=gap;best=dict(k=k,intervals=intervals.tolist(),weights=weights.tolist(),
                    parabola=lp.x.tolist(),true=exact,sdp=value,gap=gap,coefficients=matrix.tolist(),
                    witness=Y.tolist(),minimizer=z.tolist())
            if gap>1e-6:
                print(json.dumps(dict(status='candidate_only',**best)),flush=True);return
            if (k+1)%500==0:print(json.dumps(dict(completed=k+1,maximum_gap=maximum)),flush=True)
    print(json.dumps(dict(status='no_candidate',count=args.samples,best=best)),flush=True)

if __name__=='__main__':main()
