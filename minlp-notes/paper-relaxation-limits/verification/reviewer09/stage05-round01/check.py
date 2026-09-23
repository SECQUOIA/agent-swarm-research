"""Independent exact finite checks for reviewer09; no universal claim."""
from fractions import Fraction as Q
from itertools import product
from math import comb
from pathlib import Path
import hashlib
import json
import sympy as sp

out = {}
count = 0
for n in range(1, 16):
    mass = sum(comb(n, j) for j in range((n + 1)//2, n + 1))
    assert Q(mass, 2**n) >= Q(1, 2)
    assert sum(Q(comb(n,j), 2**n)*(2*j-n) for j in range(n+1)) == 0
    assert sum(Q(comb(n,j), 2**n)*(2*j-n)**2 for j in range(n+1)) == n
    for r in range(1, 11):
        for t in range(min(r-1, (n+1)//2)):
            for a in range(-t, t+1, 2):
                s = n-t
                if a < 0:
                    value = Q(a)
                else:
                    k = a+1
                    assert k <= s and 1+2*k <= 2*r
                    # Direct binomial average on the remaining unselected signs.
                    value = sum(Q(comb(s-k,j), 2**s)*(a-k+2*j-(s-k))
                                for j in range(s-k+1))
                    assert value == -Q(1, 2**k)
                assert value < 0
                count += 1
out['affine_negative_localizers'] = count
out['affine_uniform_dimensions'] = [1, 15]

x,y,z,u,v,a,b,c,h,sgn = sp.symbols('x y z u v a b c h s')
cut = 3*h/2-sgn*(u*(z-c)+c*(x*y-a*b))/2
lhs = (1-sgn*v)/2-(1-sgn*a*b*c)/2+3*h/2
assert sp.expand(lhs-cut+sgn*((v-u*z)+c*(u-x*y))/2) == 0
assert sp.expand((v-x*y*z)-((v-u*z)+z*(u-x*y))) == 0
out['symbolic_identities'] = ['order-one quadratic cut', 'order-two graph transfer']

vertex_count = 0
for M in range(1, 6):
    width = Q(2, M)
    for lower in product([Q(-1)+j*width for j in range(M)], repeat=3):
        aa,bb,cc = lower
        for bits in product([0,1], repeat=3):
            xx,yy,zz = [lower[i]+width*bits[i] for i in range(3)]
            for uu,ss in product([-1,1], repeat=2):
                q = 3*width/2-ss*(uu*(zz-cc)+cc*(xx*yy-aa*bb))/2
                assert q >= 0
                vertex_count += 1
out['exact_quadratic_box_vertices'] = vertex_count

# A full-box law satisfies both graph equations only on moments.
# Its clause cost beats the exact feasible-graph minimum in the same box.
rho = Q(1,4)
atoms = []
for i,j,k,l in product([-1,1], repeat=4):
    atoms.append((Q(1,8)*(1+l*rho)/2, (rho*i,rho*j,rho*k,k,l)))
def avg(f):
    return sum(weight*f(*point) for weight,point in atoms)
assert avg(lambda x,y,z,u,v: 1) == 1
assert avg(lambda x,y,z,u,v: u-x*y) == 0
assert avg(lambda x,y,z,u,v: v-u*z) == 0
cost = avg(lambda x,y,z,u,v: Q(1-v,2))
graph_opt = (1-rho**3)/2
assert cost < graph_opt
assert all(point[3] != point[0]*point[1] for _,point in atoms)
out['non_graph_law'] = {'atoms':len(atoms),'cost':str(cost),'graph_optimum':str(graph_opt),
                        'all_atoms_outside_graph':True}
assert 384*3**24 < 2**64
assert Q(7,16*64)==Q(7,1024)
assert Q(7,16*64*3)==Q(7,3072)
out['constants_exact'] = True
out['script_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
