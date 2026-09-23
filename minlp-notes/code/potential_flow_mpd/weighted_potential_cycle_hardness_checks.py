"""Exact symbolic and high-precision checks for weighted-potential cycle hardness."""
from fractions import Fraction as F
from itertools import product

import mpmath as mp
import networkx as nx
import numpy as np
import sympy as sp


def mp_fraction(value):
    value=F(value)
    return mp.mpf(value.numerator)/value.denominator


def run():
    q,theta=sp.symbols('q theta',real=True)
    assert sp.expand((q+2)**2-(q-1)**2-theta*q*q-(6*q+3-theta*q*q))==0
    assert sp.expand(-5*(q+2)**2-7*(q-1)**2+sp.Rational(105,4)+12*(q+sp.Rational(1,4))**2)==0
    assert sp.expand((theta*q*q-6*q-3)-(theta/16-sp.Rational(3,2))-(q+sp.Rational(1,4))*(theta*(q-sp.Rational(1,4))-6))==0
    for resistance,root in [(sp.Rational(16,3),-sp.Rational(3,8)),(24,-sp.Rational(1,4)),(144,-sp.Rational(1,8))]:
        assert 6*root+3-resistance*root**2==0
    mp.mp.dps=90
    rng=np.random.default_rng(591926)
    cases=[([1,2,3],3),([2,4],3),([1],1),([2],3)]
    cases += [(list(map(int,rng.integers(1,13,int(rng.integers(1,8))))),
               int(rng.integers(1,30))) for _ in range(40)]
    scenarios=equalities=0
    worst=mp.mpf(0)
    for aa,K in cases:
        n=len(aa);S=sum(aa)
        Delta=F(3,4*(5*K+3*S)**2)
        chain=[2]+list(range(3,n+2))+[0]
        arcs=[(0,1),(1,2)]+list(zip(chain,chain[1:]))
        graph=nx.Graph();graph.add_edges_from(arcs)
        assert nx.is_connected(graph) and all(degree==2 for _,degree in graph.degree())
        assert len(graph.edges)-len(graph)+1==1
        best=None;found=False
        for bits in product([0,1],repeat=n):
            value=sum(a*bit for a,bit in zip(aa,bits))
            theta=F(12)+F(12*value,K)
            beta=[F(1),F(1)]+[F(12,n)+F(12*a*bit,K) for a,bit in zip(aa,bits)]
            assert sum(beta[2:])==theta
            q=-6/(6+mp.sqrt(36+12*mp_fraction(theta)))
            assert -mp.mpf('.5')<q<0
            flows=[q+2,q-1]+[q]*n
            loads=[mp.mpf(0)]*(n+2)
            drop_sum=mp.mpf(0)
            for (u,v),coefficient,flow in zip(arcs,beta,flows):
                loads[u]+=flow;loads[v]-=flow
                drop_sum+=mp_fraction(coefficient)*flow*abs(flow)
            assert max(abs(loads[v]-([2,-3,1]+[0]*(n-1))[v]) for v in range(n+2))<mp.mpf('1e-75')
            worst=max(worst,abs(drop_sum))
            objective=-5*(q+2)**2-7*(q-1)**2
            threshold=-mp.mpf(105)/4
            if value==K:
                assert abs(objective-threshold)<mp.mpf('1e-75')
                found=True;equalities+=1
            else:
                assert objective<=threshold-mp_fraction(Delta)
            robust_limit=threshold-mp_fraction(Delta)/2
            assert (objective>robust_limit)==(value==K)
            scale=4*n*K
            assert all((scale*c).denominator==1 for c in beta)
            assert scale*F(-105,4)==-105*n*K
            best=objective if best is None else max(best,objective)
            scenarios+=1
        assert (best>-mp.mpf(105)/4-mp_fraction(Delta)/2)==found
    assert worst<mp.mpf('1e-75')
    print(f'Three symbolic identities and three rational triangle states passed.')
    print(f'{scenarios} resistance scenarios across{len(cases)} single-cycle instances passed; {equalities} exact target subsets.')
    print('Max cycle pressure residual:',mp.nstr(worst,8))


if __name__=='__main__':
    run()
