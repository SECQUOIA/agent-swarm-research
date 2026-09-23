"""Independent exact Stage 5 contract checks; no asymptotic verification."""
from fractions import Fraction as Q
from itertools import product, combinations
from pathlib import Path
import hashlib, json
import sympy as s
out=Path(__file__).parent
root=out.parents[2]
snap=root/'process/snapshots/stage05-round01'
manifest=json.loads((snap/'manifest.json').read_text())
files=['sections/13-xor-quadratic-hulls.tex','sections/14-monomial-reformulations.tex','sections/15-finite-certificates-affine.tex']
for p in files: assert hashlib.sha256((snap/p).read_bytes()).hexdigest()==manifest[p]
# Exact formal identities, independent of Boolean reduction.
x,y,z,u,v,a,b,c,h,sign,beta=s.symbols('x y z u v a b c h sign beta')
cut=3*h/2-sign*(u*(z-c)+c*(x*y-a*b))/2
lhs=(1-sign*v)/2-(1-sign*a*b*c)/2+3*h/2
assert s.expand(lhs-cut+sign*((v-u*z)+c*(u-x*y))/2)==0
assert s.expand(v-x*y*z-((v-u*z)+z*(u-x*y)))==0
bern=0
for bits in product((0,1),repeat=3):
    corner=(1-sign*(a+h*bits[0])*(b+h*bits[1])*(c+h*bits[2]))/2
    basis=s.prod((X-A) if bit else (A+h-X) for X,A,bit in zip((x,y,z),(a,b,c),bits))
    bern+=(corner-beta)*basis
assert s.expand(h**3*((1-sign*x*y*z)/2-beta)-bern)==0
# A full-box actual distribution that respects every degree<=2 graph identity
# but has no point on the graph. The original box is [0,1/4]^3.
H=Q(1,4)
points=[(Q(0),Q(0),Q(0),Q(-1),H/2),(Q(0),Q(0),H,Q(1),H/2)]
E=lambda f:sum(f(*p) for p in points)/2
assert E(lambda x,y,z,u,v:u-x*y)==0
assert E(lambda x,y,z,u,v:v-u*z)==0
assert all(p[3]!=p[0]*p[1] for p in points)
# Pullback monomial coefficient map: its nullity equals two and these two
# independent equations vanish, so every degree<=2 graph identity is covered.
coords=[x,y,z,u,v]
mons=[s.Integer(1)]+coords+[coords[i]*coords[j] for i in range(5) for j in range(i,5)]
pulls=[s.Poly(m.subs({u:x*y,v:x*y*z},simultaneous=True),x,y,z) for m in mons]
exps=sorted(set().union(*(set(p.monoms()) for p in pulls)))
A=s.Matrix([[p.coeff_monomial(e) for p in pulls] for e in exps])
assert len(A.nullspace())==2
cost=E(lambda x,y,z,u,v:(1-v)/2)
true_opt=(1-H**3)/2
assert cost==Q(7,16)<true_opt==Q(63,128)
assert cost >= Q(1,2)-3*H/2
# r=1 includes every allowed (generator degree, square degree) budget.
budgets=[]
for D in (2,3):
    for generator in range(3):
        for multiplier in range(2):
            if generator+2*multiplier<=2:
                assert 2*D*(generator+multiplier)<=4*D
                budgets.append([D,generator,multiplier])
# Exhaustive support/fiber check, including dependent and duplicate rows.
rows=[i for i in range(1,16) if i.bit_count()<=2]
rank_cases=0
for selection in range(1<<len(rows)):
    chosen=[v for j,v in enumerate(rows) if selection>>j&1]
    if chosen:chosen.append(chosen[0])
    basis={}; originals=[]
    for row in chosen:
        q=row
        for p in sorted(basis,reverse=True):
            if q>>p&1:q^=basis[p]
        if q:
            basis[q.bit_length()-1]=q
            originals.append(row)
    union=0; union_basis=0
    for row in chosen:union|=row
    for row in originals:union_basis|=row
    assert union==union_basis and union.bit_count()<=2*len(basis)
    for witness in range(16):
        count=sum(all(((candidate^witness)&row).bit_count()%2==0 for row in chosen) for candidate in range(16))
        assert count==2**(4-len(basis))
    rank_cases+=1
assert 384*3**24<2**64
assert Q(7,16*64)==Q(7,1024)
assert Q(7,16*64*3)==Q(7,3072)
assert Q(7,3072*17)==Q(7,52224)
result={'status':'PASS','arithmetic':'exact rational, integer and symbolic', 'snapshot_files':{p:manifest[p] for p in files},'formal_identities':3,'graph_degree_two_kernel_dimension':2,'off_graph_distribution':{'atoms':[[str(v) for v in p] for p in points],'weights':['1/2','1/2'],'moment_cost':str(cost),'graph_box_optimum':str(true_opt)},'order_one_degree_budgets':budgets,'support_families':rank_cases,'all_16_consistent_fibers_per_family':True,'limits':'Finite checks do not establish random-XOR width or universal positivity; these are checked by proof/source reading.'}
(out/'check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
