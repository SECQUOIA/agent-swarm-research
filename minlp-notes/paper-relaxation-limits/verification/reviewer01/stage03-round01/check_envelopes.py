"""Independent finite rational checks; not a proof of the universal bounds."""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb, prod
import json
from pathlib import Path
import sympy as sp


def choose(n, j):
    return comb(n, j) if 0 <= j <= n else 0


def orientation_moments(p, ambient, fair=False):
    d = len(p)
    patterns = list(product((0, 1), repeat=d)) if fair else [
        tuple(int(i in J) for i in range(d))
        for J in combinations(range(ambient), ambient // 2)
    ]
    cuts = sorted({F(0), F(1), *p, *(1-x for x in p)})
    ans = [F(0)] * (d+2)
    for pattern in patterns:
        for left, right in zip(cuts, cuts[1:]):
            u = (left+right)/2
            k = sum(u < x if bit else u > 1-x for x, bit in zip(p, pattern))
            for j in range(d+2):
                ans[j] += (right-left)*choose(k,j)/len(patterns)
    return ans


def moments(p, ambient, fair=False):
    d = len(p)
    C = [F(1)] + [sum(min(p[i] for i in S) for S in combinations(range(d),j))
                    for j in range(1,d+2)]
    P = [sum(prod(p[i] for i in S) for S in combinations(range(d),j))
         for j in range(d+2)]
    s = sum(p); k = s.numerator // s.denominator; theta = s-k
    V = [(1-theta)*choose(k,j)+theta*choose(k+1,j) for j in range(d+2)]
    O = orientation_moments(p,ambient,fair)
    beta = F(2) if fair else F(ambient*(ambient-1),2*(ambient//2)*(ambient-ambient//2))
    coeff = [beta*(C[j]-O[j])+V[j]-P[j]+(C[j-1]-P[j-1] if j else 0)
             for j in range(d+2)]
    return C,P,V,O,beta,coeff


coefficient_cases = 0
regularity_cases = 0
grid = [F(0),F(1,100),F(1,4),F(1,2),F(3,4),F(99,100),F(1)]
for ambient in range(2,8):
    for d in range(2,min(4,ambient)+1):
        for case in range(21):
            p = tuple(grid[(case*(i+1)+i*i)%len(grid)] for i in range(d))
            C,P,V,O,beta,coeff = moments(p,ambient)
            assert all(x >= 0 for x in coeff), (ambient,p,coeff)
            coefficient_cases += 1
            for L in (F(0),F(1,3),F(2)):
                a = [F(2),F(3)] + [F(5)*L**(j-2) for j in range(2,d+1)]
                c,ind,v,o = [sum(a[j]*seq[j] for j in range(d+1)) for seq in (C,P,V,O)]
                assert c-v <= (L+1)*(c-ind)+beta*(c-o)
                regularity_cases += 1

p = (F(2,5),F(7,10),F(24,25),F(97,100))
p2 = (F(2,5),F(7,10),F(959,1000),F(971,1000))
assert moments(p,4,True)[-1][3] == F(6201,12500)
assert moments(p2,4,True)[-1][3] == F(4961031,10000000)

# Enumerate every basic feasible distribution for the three-variable mean.
vertices = list(product((0,1),repeat=3))
rhs = sp.Matrix([1,sp.Rational(1,4),sp.Rational(1,4),sp.Rational(3,4)])
laws=[]
for indices in combinations(range(8),4):
    matrix=sp.Matrix([[1]+list(vertices[i]) for i in indices]).T
    if matrix.det() == 0:
        continue
    weights=matrix.inv()*rhs
    if min(weights) >= 0:
        laws.append((indices,tuple(F(w) for w in weights)))


def extrema(values):
    vals=[sum(w*values[i] for i,w in zip(indices,weights)) for indices,weights in laws]
    return min(vals),max(vals)


xy=[F((1+a)*(1+b)) for a,b,c in vertices]
xyz=[F((1+a)*(1+b)*(1+2*c)) for a,b,c in vertices]
assert extrema(xy)==(F(3,2),F(7,4))
assert extrema(xyz)==(F(13,4),F(19,4))
assert extrema([a+b for a,b in zip(xy,xyz)])==(F(5),F(13,2))
epsilon_cases=0
for eps in (F(1,100),F(1,7),F(1,2),F(1),F(3,2),F(2)):
    av=[2*eps*a*b for a,b,c in vertices]
    bv=[eps**2*a*b+2*eps*a*c+2*eps*b*c+2*eps**2*a*b*c for a,b,c in vertices]
    al,au=extrema(av); bl,bu=extrema(bv)
    cl,cu=extrema([a+b for a,b in zip(av,bv)])
    assert (au-al+bu-bl)/(cu-cl)==2*(eps+3)/(3*eps+4)
    epsilon_cases+=1

payoffs={}
for z in product((0,1),repeat=6):
    ab,bc,ca = z[0]==z[1],z[2]==z[3],z[4]==z[5]
    payoff=(int(ab and ca),int(not ab and bc),int(not bc and not ca))
    payoffs[payoff]=payoffs.get(payoff,0)+1
assert set(payoffs.values())=={16} and len(payoffs)==4

result={"arithmetic":"exact rational", "coefficient_cases":coefficient_cases,
        "regularity_cases":regularity_cases,"feasible_three_variable_bases":len(laws),
        "unequal_epsilon_cases":epsilon_cases,"parity_vertices":64,
        "status":"PASS", "scope":"Finite checks supplement the separately reviewed analytic proofs."}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
