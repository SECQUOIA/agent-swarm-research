from fractions import Fraction as Q
from math import comb, factorial
from itertools import product
from pathlib import Path
import json
import sympy as s

out = {}
# Exact, finite checks of the binomial derivative and deletion inequalities.
ns = [3, 4, 5, 8, 9, 16, 32, 64, 128]
for n in ns:
    N, p = 8*n, Q(3,n)
    masses = [Q(comb(N,k))*p**k*(1-p)**(N-k) for k in range(N+1)]
    assert sum(masses) == 1
    weighted = sum(Q(k)*2**k*mass for k,mass in enumerate(masses))
    tail = sum(Q(k)*mass for k,mass in enumerate(masses) if k>64)
    assert weighted == 48*(1+p)**(8*n-1)
    assert tail <= weighted / 2**64 < Q(1,8)
# Pure integer sufficient bound for the manuscript's exponential constant.
assert 384*3**24 < 2**64
# e^(7/8)>2 follows already from three Taylor terms, implying ln2<7/8.
assert 1+Q(7,8)+Q(7,8)**2/2 > 2
out['exact_binomial_n'] = ns
out['deletion_integer_bound'] = str(Q(48*3**24,2**64))
# Rational enclosure for the actual exponential numerical scale, used only as annotation.
lo = sum(Q(24)**k / factorial(k) for k in range(160))
next_term = Q(24)**160 / factorial(160)
hi = lo + next_term/(1-Q(24,161))
assert Q(48,2**64)*hi < Q(1,8)
out['48_exp24_over_2pow64_enclosure'] = [str(Q(48,2**64)*v) for v in (lo,hi)]
out['enclosure_display_only'] = [float(Q(48,2**64)*v) for v in (lo,hi)]
assert Q(7,16*64)==Q(7,1024)
assert Q(7,16*64*3)==Q(7,3072)
assert Q(7,3072*17)==Q(7,52224)
assert 3/Q(1,16)==48
out['normalization_constants'] = 'exact pass'

# Formal polynomial identity, no numerical optimization and no graph support assumption.
x,y,z,u,v,a,b,c,h,sign = s.symbols('x y z u v a b c h sign')
q=3*h/2-sign*(u*(z-c)+c*(x*y-a*b))/2
lhs=(1-sign*v)/2-(1-sign*a*b*c)/2+3*h/2
rhs=q-sign*((v-u*z)+c*(u-x*y))/2
assert s.expand(lhs-rhs)==0
assert s.Poly(q,x,y,z,u,v).total_degree()==2
assert s.expand(v-x*y*z-((v-u*z)+z*(u-x*y)))==0
# Test full box quadratic cuts at corners, for 1,2,3,4,8,48 grid widths.
# Each expression is multiaffine in the variables, so vertex tests certify each selected box.
cases=0
for M in [1,2,3,4,8,48]:
    width=Q(2,M)
    indices=sorted(set([0,M//2,M-1]))
    for idx in product(indices,repeat=3):
        corner=tuple(-1+width*j for j in idx)
        for ends in product([0,1],repeat=3):
            xx=tuple(aa+width*ee for aa,ee in zip(corner,ends))
            for uu,ss in product([-1,1],repeat=2):
                qval=3*width/2-Q(ss,2)*(uu*(xx[2]-corner[2])+corner[2]*(xx[0]*xx[1]-corner[0]*corner[1]))
                assert qval>=0
                cases+=1
out['order_one_full_box_vertex_cases']=cases
out['symbolic_graph_and_cut_identities']='exact pass'

# Width-3 versus width-4 closure on a four-clause inconsistent system.
clauses=[(0b000111,1),(0b011001,1),(0b101010,1),(0b110100,-1)]
def closure(w):
    seen={(0,1),*clauses}
    while True:
        new={(A^B,aa*bb) for A,aa in seen for B,bb in seen if (A^B).bit_count()<=w}
        if new<=seen:return seen
        seen|=new
cw3,cw4=closure(3),closure(4)
assert (0,-1) not in cw3 and (0,-1) in cw4
assert all(A.bit_count() in [0,3] for A,_ in cw3)
# Consequently every off-diagonal entry of the constant/singletons Gram is zero.
assert len(cw3)==5
out['width3_signed_degree3_identity_gram_and_width4_contradiction']='exact pass'

p=Path(__file__).with_name('results.json')
p.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if 'enclosure' not in k},indent=2))
