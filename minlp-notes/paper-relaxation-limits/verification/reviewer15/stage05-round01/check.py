"""Independent exact finite audit; does not prove asymptotic existence."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json
import sympy as s
x,y,z,u,v,a,b,c,h,sg,beta=s.symbols('x y z u v a b c h sg beta')
ce=(1-sg*x*y*z)/2
cut=3*h/2-sg*(u*(z-c)+c*(x*y-a*b))/2
assert s.expand((1-sg*v)/2-(1-sg*a*b*c)/2+3*h/2-cut+sg*((v-u*z)+c*(u-x*y))/2)==0
assert s.expand(v-x*y*z-((v-u*z)+z*(u-x*y)))==0
bern=0
for bits in product((0,1),repeat=3):
    corner=ce.subs(dict(zip((x,y,z),(a+h*bits[0],b+h*bits[1],c+h*bits[2]))))
    basis=s.prod((t-lo if bit else lo+h-t)/h for t,lo,bit in zip((x,y,z),(a,b,c),bits))
    bern+=(corner-beta)*basis
assert s.expand(h**3*(ce-beta-bern))==0
# Non-graph-supported box law satisfying both quadratic graph moment equations.
# i,j fixed at 0, k uniform +1/-1, u uniform independent +1/-1, v=u*k.
points=[(Q(0),Q(0),Q(k),Q(j),Q(j*k)) for k,j in product((-1,1),repeat=2)]
assert sum(p[3]-p[0]*p[1] for p in points)==0
assert sum(p[4]-p[3]*p[2] for p in points)==0
assert all(p[3]!=p[0]*p[1] for p in points)
# Rank/support and exact fibers for every family of proper nonempty n=4 supports.
rows=[i for i in range(1,16) if i.bit_count()<=3]
nfamilies=0
for mask in range(1<<len(rows)):
    family=[row for j,row in enumerate(rows) if mask>>j&1]
    basis={}; union=0; basis_union=0
    for row in family:
        union|=row; red=row
        while red:
            p=red.bit_length()-1
            if p in basis: red^=basis[p]
            else: basis[p]=red; basis_union|=row; break
    assert union==basis_union and union.bit_count()<=3*len(basis)
    fibers={}
    for t in range(16):
        rhs=tuple((row&t).bit_count()%2 for row in family)
        fibers[rhs]=fibers.get(rhs,0)+1
    assert set(fibers.values())=={1<<(4-len(basis))}
    nfamilies+=1
# Odd-width closure: all four triples have negative product, each variable twice.
clauses=[(0b000111,1),(0b011001,1),(0b101010,1),(0b110100,-1)]
def closure(w):
    cl={(0,1),*clauses}
    while True:
        add={(A^B,aa*bb) for A,aa in cl for B,bb in cl if (A^B).bit_count()<=w}
        if add<=cl: return cl
        cl|=add
cl3=closure(3); cl4=closure(4)
assert (0,-1) not in cl3 and (0,-1) in cl4
for A in [0]+[1<<i for i in range(6)]:
    for B in [0]+[1<<i for i in range(6)]:
        assert ((A^B,1) in cl3)==(A==B)
        assert (A^B,-1) not in cl3
# Pointwise quadratic-box cut at rational vertices, both signs; unequal/singleton widths.
intervals=[(Q(-1),Q(-1)),(Q(-1),Q(-1,2)),(Q(-1,2),Q(1,2)),(Q(0),Q(0)),(Q(1,2),Q(1))]
cases=0
for box in product(intervals,repeat=3):
    lows=[p[0] for p in box]; width=max(hi-lo for lo,hi in box)
    for xx,yy,zz,uu,sign in product(*box,(-1,1),(-1,1)):
        aa,bb,cc=lows
        q=3*width/2-Q(sign,2)*(uu*(zz-cc)+cc*(xx*yy-aa*bb))
        assert q>=0; cases+=1
assert 384*3**24<2**64
assert Q(7,16*64)==Q(7,1024)
assert Q(7,16*64*3*17)==Q(7,52224)
result={'kind':'exact symbolic and rational finite checks','symbolic_identities':3,'rank_families':nfamilies,'odd_width_closure':{'width3_nonrefuted':True,'width4_refuted':True},'quadratic_vertex_cases':cases,'non_graph_supported_graph_moment_law':True,'constants':'passed'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
