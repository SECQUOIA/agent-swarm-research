"""Symbolic and high-precision checks for weighted arc-flow rank-two hardness."""
from fractions import Fraction as F
from itertools import product
import mpmath as mp
import networkx as nx
import numpy as np
import sympy as sp


def mpf(value):
    value=F(value)
    return mp.mpf(value.numerator)/value.denominator


def solve(theta):
    theta=mpf(theta);lo=mp.mpf(0);hi=mp.mpf(3);q=mp.mpf(1)
    for _ in range(200):
        u=mp.sqrt(2*q+18);a=q+9-2*u
        f=theta*q*q+8*a-16
        if abs(f)<mp.mpf('1e-82'):return q,a
        if f>0:hi=q
        else:lo=q
        derivative=2*theta*q+8*(1-2/u)
        new=q-f/derivative
        q=new if lo<new<hi else (lo+hi)/2
    raise AssertionError('root iteration did not converge')


def run():
    q,u=sp.symbols('q u');a=q+9-2*u
    outer=sp.expand(a*a+(a+3-q)**2-(4-a)**2-2*(1-a+q)**2)
    assert sp.rem(outer,u*u-2*q-18,u)==0
    perf=sp.expand(-9*a+5*q+sp.Rational(9,2)+2*(u-sp.Rational(9,2))**2)
    assert sp.rem(perf,u*u-2*q-18,u)==0
    assert sp.expand((4-a)**2-a*a-(16-8*a))==0
    for th,qq,aa in [(sp.Rational(448,81),sp.Rational(9,8),sp.Rational(9,8)),
                     (sp.Rational(1792,5329),sp.Rational(73,32),sp.Rational(57,32)),
                     (12032,sp.Rational(1,32),sp.Rational(17,32))]:
        assert th*qq**2==16-8*aa
        assert aa**2+(aa+3-qq)**2==(4-aa)**2+2*(1-aa+qq)**2
    mp.mp.dps=90
    rng=np.random.default_rng(491307)
    cases=[([1],1),([2,4],3),([1,2,3],3),([2],3)]
    cases += [(list(map(int,rng.integers(1,15,int(rng.integers(1,8))))),int(rng.integers(1,35))) for _ in range(36)]
    count=yes=0;worst=mp.mpf(0)
    for items,K in cases:
        n=len(items);S=sum(items);H=23*K+15*S;gap=F(1,4*H*H)
        chain=[2]+list(range(4,n+3))+[3]
        edges=[(0,2),(2,1),(0,3),(3,1)]+list(zip(chain,chain[1:]))
        graph=nx.Graph();graph.add_edges_from(edges)
        assert nx.is_connected(graph) and len(graph.edges())-len(graph)+1==2
        assert max(dict(graph.degree()).values())==3
        for choices in product((0,1),repeat=n):
            total=sum(a*bit for a,bit in zip(items,choices))
            theta=F(224,81)*(1+F(total,K));q,a=solve(theta)
            assert 0<q<3
            flows=[a,a+3-q,4-a,1-a+q]+[q]*n
            beta=[F(1),F(1),F(1),F(2)]+[F(224,81*n)+F(224*ai*bit,81*K) for ai,bit in zip(items,choices)]
            assert sum(beta[4:])==theta and min(flows)>0
            balance=[mp.mpf(0)]*len(graph)
            pi=[None]*len(graph);pi[0]=mp.mpf(0);pi[2]=-a*a;pi[3]=-(4-a)**2;pi[1]=pi[2]-(a+3-q)**2
            for j,(s,t) in enumerate(zip(chain,chain[1:])):
                if t!=3:pi[t]=pi[s]-mpf(beta[4+j])*q*q
            residual=mp.mpf(0)
            for (s,t),x,be in zip(edges,flows,beta):
                balance[s]+=x;balance[t]-=x
                residual=max(residual,abs(pi[s]-pi[t]-mpf(be)*x*x))
            nominations=[4,-4,3,-3]+[0]*(n-1)
            residual=max(residual,max(abs(z-v) for z,v in zip(balance,nominations)))
            worst=max(worst,residual);assert residual<mp.mpf('1e-75')
            value=-9*a+5*q;peak=-mp.mpf(9)/2;limit=peak-mpf(gap)/2
            assert abs(value-(peak-2*(mp.sqrt(2*q+18)-mp.mpf(9)/2)**2))<mp.mpf('1e-78')
            if total==K:
                yes+=1;assert abs(value-peak)<mp.mpf('1e-75') and value>limit
            else:
                assert value<peak-mpf(gap) and value<limit
            scale=81*n*K
            assert all((be*scale).denominator==1 for be in beta)
            assert beta[4]*scale==224*K+224*n*items[0]*choices[0]
            N=16*H*H
            assert N*gap==4
            if total!=K:assert N*value<N*peak-4
            count+=1
    print('PASS: 3 symbolic identities, 3 exact theta states,',count,'scenarios across',len(cases),'instances;',yes,'target subsets')
    print('Max full physical residual:',mp.nstr(worst,8))


if __name__=='__main__':run()
