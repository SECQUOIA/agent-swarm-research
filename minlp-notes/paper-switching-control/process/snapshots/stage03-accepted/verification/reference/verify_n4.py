"""Exact dual-certificate proof of the four-mode, three-block reach lemma.

Run directly with Python's standard library. The numerical optimizer that proposed
the stored certificates is not imported or trusted by this checker.
"""
from fractions import Fraction as F
from itertools import permutations
import json
from pathlib import Path


def orders():
    first=[f'r{i}' for i in [3,2,1,0]]
    for p in permutations(range(4)):
        yield first+[f'm{i}' for i in p]
    for p in permutations([1,2,3]):
        yield ['r3','r2','r1','m0','r0']+[f'm{i}' for i in p]


def program(order):
    """Return integer A,b,E,e,c for min c*x, A*x<=b, E*x=e, x>=0."""
    pos={name:t for t,name in enumerate(order)}
    def ti(name):return pos[name]*5
    def ai(name,i):return pos[name]*5+1+i
    eq=[];er=[];ineq=[];ir=[]
    for t,name in enumerate(order):
        row=[0]*40;row[ti(name)]=-1
        for i in range(4):row[ai(name,i)]=1
        eq.append(row);er.append(0)
        if t:
            prev=order[t-1]
            for i in range(4):
                row=[0]*40;row[ai(prev,i)]=1;row[ai(name,i)]=-1
                ineq.append(row);ir.append(0)
    for i in range(4):
        row=[0]*40;row[ti(f'r{i}')]=1;row[ai(f'r{i}',i)]=-1
        eq.append(row);er.append(1)
    for i in range(4):
        for j,k in permutations([h for h in range(4) if h!=i],2):
            row=[0]*40
            row[ti(f'r{j}')]=1
            row[ti(f'm{i}')]=-1
            row[ai(f'm{i}',k)]=1
            ineq.append(row);ir.append(-1)
    obj=[0]*40
    for i in range(4):obj[ti(f'm{i}')]=1
    return ineq,ir,eq,er,obj


def check_one(order,certificate):
    A,b,E,e,c=program(order)
    y=[F(0)]*len(A);z=[F(0)]*len(E)
    for i,v in certificate['inequality'].items():
        assert 0<=int(i)<len(y)
        y[int(i)]=F(v)
    for i,v in certificate['equality'].items():
        assert 0<=int(i)<len(z)
        z[int(i)]=F(v)
    assert all(v<=0 for v in y), 'Wrong sign on inequality multiplier'
    residual=[F(c[j])-sum(y[i]*A[i][j] for i in range(len(A)))
              -sum(z[i]*E[i][j] for i in range(len(E))) for j in range(40)]
    assert all(v>=0 for v in residual), 'Dual residual is negative'
    lower=sum(v*r for v,r in zip(y,b))+sum(v*r for v,r in zip(z,e))
    assert lower==F(certificate['lower_bound'])
    assert lower>=F(112,9), 'Insufficient lower bound'
    return lower


def main():
    if not __debug__:
        raise RuntimeError("Run without -O: certificate checks require assertions")
    data=json.loads(Path(__file__).with_name('certificates_n4.json').read_text())
    expected=list(orders())
    assert len(data)==len(expected)==30
    values=[]
    for order,certificate in zip(expected,data):
        assert certificate['order']==order, 'Missing or reordered case'
        values.append(check_one(order,certificate))
    assert values[:24]==[F(112,9)]*24
    assert values[24:]==[F(43,3)]*6
    print('Verified 30 event-order cases using exact rational arithmetic.')
    print('24 regular cases: sum M_i >= 112/9.')
    print('6 interleaved cases: sum M_i >= 43/3 > 112/9.')
    print('No numerical solver, tolerance, or approximate coefficient is used.')


if __name__=='__main__':
    main()
