"""Independent exact diagnostics for stage 5; finite checks, not proof substitutes."""
from fractions import Fraction as F
from itertools import product
from math import prod

def vertex(bits, g):
    out = []
    prev = F(0)
    for bit in bits:
        prev = bit + (1 - 2 * bit) * g * prev
        out.append(prev)
    return tuple(out)

def coeff(n, g):
    return tuple((1-g)*g**(2*(n-i)-1) for i in range(1,n)) + (F(0),)

def dot(a,b):
    return sum(x*y for x,y in zip(a,b))

def vertex_polynomial(z,g):
    return z[-1]-z[-1]**2-dot(coeff(len(z),g),z)

padding_pairs = 0
for weights in [(1,), (1,1), (1,2), (1,2,3), (2,3,4)]:
    n, W = len(weights), sum(weights)
    r = 0
    while F(1,4)**(r+1) > F(1,8*W):
        r += 1
    N = n+(n-1)*r
    free = [i*(r+1) for i in range(n)]
    c = coeff(N,F(1,4))
    delta = F(1,4)**(2*(N-1))
    tau = delta/(2*N)
    originals = [vertex(b,F(1,4)) for b in product([0,1],repeat=N)]
    assert len({v[-1] for v in originals}) == 2**N
    for v in originals:
        assert vertex_polynomial(v,F(1,4)) == 0
    for bits in product([0,1],repeat=n):
        padded = [0]*N
        for i,b in zip(free,bits):
            padded[i] = b
        v = vertex(padded,F(1,4))
        assert all(v[i] <= F(1,2) for i in range(N) if i not in free)
        total = sum(a*v[i] for a,i in zip(weights,free))
        integer_total = dot(weights,bits)
        assert abs(total-integer_total) <= F(1,8)
        for target in range(W+1):
            assert (abs(total-target) <= F(1,4)) == (integer_total == target)
        price = 2*v[-1]-1
        for h in [-delta/4,F(0),delta/4]:
            if not -1 <= price+h <= 1:
                continue
            # Gradient of the identity-Hessian rescaling at v.
            gradient = tuple(v[i]-(c[i]+(price+h if i==N-1 else 0))/tau for i in range(N))
            for u in originals:
                if u == v:
                    continue
                assert dot(gradient,tuple(a-b for a,b in zip(u,v))) > 0
                padding_pairs += 1
        # Test the telescoping identity at an interior point of the full polytope.
        z = tuple((a+2*b)/3 for a,b in zip(v, originals[-1]))
        prev, expanded = F(0), F(0)
        for j,zj in enumerate(z,1):
            expanded += F(1,4)**(2*(N-j))*(zj-prev/4)*(1-prev/4-zj)
            prev = zj
        assert vertex_polynomial(z,F(1,4)) == expanded >= 0
print('padded identity-Hessian exact global direction inequalities:', padding_pairs)

shadow_pairs=0
for n in range(1,7):
    g=F(1,4)
    c=tuple(g**(3*(n-j)) for j in range(1,n))+(F(0),)
    vertices=[(b,vertex(b,g)) for b in product([0,1],repeat=n)]
    for bits,v in vertices:
        price=-sum(prod(1-2*b for b in bits[j:])*g**(2*(n-j)) for j in range(n))
        assert abs(price)<F(1,15)
        score=dot(c,v)+price*v[-1]
        for _,u in vertices:
            if u!=v:
                assert score>dot(c,u)+price*u[-1]
                shadow_pairs+=1
        a=price
        value=max(0,a)
        for j in range(n-2,-1,-1):
            a=c[j]-g*abs(a)
            value+=max(0,a)
        assert value==score
print('sparse shadow exact exposure comparisons and value recurrence:', shadow_pairs)

def clip(t):
    return min(F(1),max(F(0),t))

for r in [F(1),F(1,2),F(1,7)]:
    for j in range(-100,101):
        t=F(j,100)
        assert min(abs(t),abs(t-r)) == -t+2*clip(t)-2*clip(t-r/2)+2*clip(t-r)
for P in [1,2,3,16,256,1024]:
    x=F(5,8)**P
    assert x.denominator >= F(8,5)**P
    assert F(1,2)**P <= x
    assert (F(5,8)-F(1,2))**2 == F(1,64)
print('leader-path clipping identity and one-power endpoint/output bounds: passed')

# Dense ternary construction: all bit encodings, including an unsatisfiable
# conjunction of all eight clauses, are exact box responses at their leaders.
for n in range(3,6):
    clauses=list(product([0,1],repeat=3))
    m=len(clauses)
    rho=F(1,100*3**n)
    w=[rho**i for i in range(n)]
    eta=rho**n
    xi=eta/(m+1)
    for bits in product([0,1],repeat=n):
        x=sum(F(2*b,3**(i+1)) for i,b in enumerate(bits))+F(1,2*3**n)
        residual=[bits[i]-3**(i+1)*x+2*sum(3**(i-j)*bits[j] for j in range(i))+1 for i in range(n)]
        gradient=[w[i]*residual[i]+sum(2*3**(k-i)*w[k]*residual[k] for k in range(i+1,n)) for i in range(n)]
        for i,b in enumerate(bits):
            gradient[i] += -2*eta if b==0 else 0
        for clause in clauses:
            literal_sum=sum(bits[i] if positive else 1-bits[i] for i,positive in enumerate(clause))
            v=max(0,1-literal_sum)
            for i,positive in enumerate(clause):
                gradient[i]+=xi*(v-1+literal_sum)*(1 if positive else -1)
        assert all(g>0 if b==0 else g<0 for b,g in zip(bits,gradient))
print('dense ternary Boolean encoding and signed clause-feedback KKT: passed')
