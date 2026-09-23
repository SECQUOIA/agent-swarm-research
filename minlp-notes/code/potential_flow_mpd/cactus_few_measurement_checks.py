"""Numerical arrangement enumeration against every endpoint scenario."""
from itertools import product
import mpmath as mp
import numpy as np
from scipy.optimize import linprog


def cones(A):
    patterns=[()]
    for index,row in enumerate(A):
        new=[]
        for prefix in patterns:
            for sign in (-1,1):
                signs=prefix+(sign,)
                result=linprog(np.zeros(A.shape[1]),A_ub=-np.array(signs)[:,None]*A[:index+1],
                               b_ub=-np.ones(index+1),bounds=[(None,None)]*A.shape[1],method='highs')
                if result.success:new.append(signs)
        patterns=new
    return patterns


def run():
    mp.mp.dps=70;rng=np.random.default_rng(661709)
    corners=patterns_count=0
    for trial in range(18):
        count=3+trial%6;dim=1+trial%3
        A=rng.integers(-3,4,(count,dim))
        if trial%3==0:A[-1]=0
        if trial%4==0:A[-2]=A[0]
        low_beta=rng.integers(1,5,count);high_beta=low_beta+rng.integers(0,5,count)
        lo=[1/(1+mp.sqrt(int(b))) for b in high_beta]
        hi=[1/(1+mp.sqrt(int(b))) for b in low_beta]
        linear=list(map(int,rng.integers(-2,3,dim)));offset=list(map(int,rng.integers(-2,3,dim)))
        def value(bits):
            q=[h if bit else l for bit,l,h in zip(bits,lo,hi)]
            y=[mp.mpf(offset[j])+sum(int(A[i,j])*q[i] for i in range(count)) for j in range(dim)]
            return sum(v**4+v*v+linear[j]*v for j,v in enumerate(y))
        exact=max(value(bits) for bits in product((0,1),repeat=count));corners+=2**count
        keep=[i for i,row in enumerate(A) if any(row)]
        patterns=cones(A[keep]) if keep else [()]
        best=-mp.inf
        for pattern in patterns:
            bits=[0]*count
            for i,sig in zip(keep,pattern):bits[i]=sig>0
            best=max(best,value(bits))
        assert abs(best-exact)<mp.mpf('1e-55')
        patterns_count+=len(patterns)
    print('PASS: 18 projected convex quartic examples;',corners,'exhaustive corners;',patterns_count,'rational-direction sign cones')


if __name__=='__main__':run()
