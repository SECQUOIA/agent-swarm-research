"""Exact arithmetic checks of the mixed Gaussian support/precision budget.

These are synthetic rational bounds, not end-to-end MIQP instances.
"""
from fractions import Fraction as Q
import json


def log_ceiling(x):
    exponent=0
    while Q(2)**exponent<x:
        exponent+=1
    return exponent


def check(name,n,k,q,Z,G,widths,row_bounds,alpha,sigma,H0):
    widths=list(map(Q,widths)); row_bounds=list(map(Q,row_bounds))
    alpha,sigma,H0=map(Q,(alpha,sigma,H0))
    R=Z*2**q
    B=max(2,R)
    K=R*(q+n+1)
    sections=(2*(2*k+1)*R*R+1)*(8*k+2)
    Lambda=alpha*k*max(Q(1),sum(widths))
    checks=0
    for t in range(100):
        support=2**t
        s=max(w+2*support*sigma*d/alpha for w,d in zip(widths,row_bounds))
        Cgap=k*alpha*s/4+Lambda
        Cbad=K*k*(alpha+H0)+G*Cgap
        h=s
        J=0
        while h>sigma/(4*B*Cbad):
            h/=2;J+=1
        all_nodes=(J+1)*(2**J+1)**k
        demand=max(8*B*(n*K+G),2*n*sections*all_nodes)
        b=max(1,(demand-1).bit_length())
        delta=Q(1,2**b)
        assert Cbad*h/sigma<=Q(1,4*B)
        assert 2*(n*K+G)*delta<=Q(1,4*B)
        assert Cbad*h/sigma+2*(n*K+G)*delta<=Q(1,2*B)
        assert 2*n*sections*all_nodes*delta<=1
        if t==0:J0,b0=J,b
        assert J<=J0+2*t
        ratio=Q(J0+2*t+1,J0+1)
        assert b<=b0+2*k*t+log_ceiling(ratio)
        checks+=1
        if support>=b+20:
            assert sigma*(b+20)<=sigma*support
            return dict(name=name,trials=checks,support_exponent=t,
                        terminal_level=J,accuracy_bits=b,initial_level=J0)
    raise AssertionError('support loop did not terminate')


def main():
    records=[
        check('mixed moderate',5,2,6,12,5,[Q(3,2),Q(5,3)],
              [Q(6,5),Q(7,5)],Q(7,4),Q(1,3),2**40),
        check('large integer ranges and 1000-bit response bound',4,2,8,
              (2**40+1)*3,2**40+2,[1,2**20],[2,2],Q(1,2),Q(1,64),2**1000),
        check('pure integer counts',3,3,6,8,3,[1,1,1],[1,1,1],2,1,2),
        check('no integer alternatives',10,1,20,1,0,[Q(1,3)],[2],Q(1,7),2,10),
        check('label-gap term controls support growth',2,1,4,2,1,
              [1],[1],1,2**100,1),
        check('wide precision scales',30,5,12,(2**50+1)**2,2**51,
              [Q(1,3),1,2,3,5],[2]*5,2**100,Q(1,2**200),2**400),
    ]
    print(json.dumps({'status':'passed','budget_trials':sum(r['trials'] for r in records),
                      'fixtures':records},indent=2))


if __name__=='__main__':main()
