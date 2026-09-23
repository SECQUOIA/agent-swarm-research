"""Independent exact checks of stage 5 identities and rational recovery."""
import itertools
import json
import math
from fractions import Fraction as F
from pathlib import Path
import sympy as s


def clip(x):
    return min(F(1), max(F(0), x))


def box_oracle(Q, t):
    n = Q.rows
    for status in itertools.product((0, 1, 2), repeat=n):
        free = [i for i, a in enumerate(status) if a == 1]
        z = s.Matrix([int(a == 2) for a in status])
        if free:
            rhs = -(t + Q*z).extract(free, [0])
            v = Q.extract(free, free).inv()*rhs
            for i, value in zip(free, v):
                z[i] = value
        if not all(0 <= a <= 1 for a in z):
            continue
        g = Q*z+t
        if all((a == 0 and b >= 0) or (a == 1 and b <= 0)
               or (0 < a < 1 and b == 0) for a, b in zip(z, g)):
            return z
    raise AssertionError('No box KKT solution')


def oracle_check(Q, t):
    n = Q.rows
    exact = box_oracle(Q, t)
    L = max(sum(abs(Q[i,j]) for j in range(n)) for i in range(n))
    Qi = Q.inv()
    K = L*max(sum(abs(Qi[i,j]) for j in range(n)) for i in range(n))
    den = s.ilcm(*[a.q for a in list(Q)+list(t)])
    H = max(1, *[abs(int(a*den)) for a in list(Q)+list(t)])
    B = math.factorial(n)*H**n
    ceil_log = lambda a: (int(a)-1).bit_length()
    count = int(math.ceil(K*(2*ceil_log(B)+ceil_log(n)+4)))
    z = s.zeros(n, 1)
    for _ in range(count):
        z = (z-(Q*z+t)/L).applyfunc(lambda a:min(s.Integer(1),max(s.Integer(0),a)))
    error = s.Rational(1,4*B**2)
    assert all(abs(a-b)<error for a,b in zip(z,exact))
    recovered = []
    for a in z:
        # Independent bounded-denominator reconstruction; the proof was
        # separately checked for its continued-fraction implementation.
        f = F(int(a.p),int(a.q)).limit_denominator(B)
        recovered.append(s.Rational(f.numerator,f.denominator))
    assert s.Matrix(recovered)==exact
    return {'dimension':n,'iterations':count,'denominator_bound':str(B),
            'response':[str(a) for a in exact]}


def dense_check():
    n = 3
    clauses = list(itertools.product((0,1),repeat=n))
    rho = F(1,100*3**n)
    weights = [rho**i for i in range(n)]
    eta = rho**n
    xi = eta/(len(clauses)+1)
    scores=[]
    for d in itertools.product((0,1),repeat=n):
        x = sum(F(2*d[i],3**(i+1)) for i in range(n))+F(1,2*3**n)
        r = [d[i]-3**(i+1)*x+2*sum(3**(i-j)*d[j] for j in range(i))+1 for i in range(n)]
        grad = [weights[i]*r[i]+sum(2*3**(j-i)*weights[j]*r[j] for j in range(i+1,n)) for i in range(n)]
        for i in range(n):
            p=clip(2*d[i]-1)
            grad[i] += -2*eta*(p-2*d[i]+1)
        shortfalls=[]
        for signs in clauses:
            literal_sum=sum(d[i] if signs[i] else 1-d[i] for i in range(n))
            v=max(0,1-literal_sum)
            residual=v-1+literal_sum
            shortfalls.append(v)
            for i in range(n):
                grad[i] += xi*residual*(1 if signs[i] else -1)
        assert all((1-2*d[i])*grad[i]>0 for i in range(n))
        scores.append(2*sum(shortfalls))
    assert scores==[2]*8
    return {'assignments':8,'clauses':8,'all_strict_box_signs':True,'all_upper_scores':2}


def padded_check():
    weights=[1,2]
    W=sum(weights)
    r=0
    while F(1,4**(r+1))>F(1,8*W):
        r+=1
    n=2+r
    gamma=F(1,4)
    vertices=[]
    for bits in itertools.product((0,1),repeat=n):
        v=[]
        prev=F(0)
        for d in bits:
            prev=d+(1-2*d)*gamma*prev
            v.append(prev)
        vertices.append((bits,v))
    c=[(1-gamma)*gamma**(2*(n-i-1)-1) for i in range(n-1)]+[F(0)]
    D=4**(n-1)
    Delta=F(1,D**2)
    tau=Delta/(2*n)
    padded=[(b,v) for b,v in vertices if all(v[i]<=F(1,2) for i in range(1,n-1))]
    assert len(padded)==4
    checked=0
    for bits,v in padded:
        assert not any(bits[1:-1])
        assert abs(v[-1]-bits[-1])<=F(1,8*W)
        lam=2*v[-1]-1
        for _,u in vertices:
            F_u=u[-1]-sum(a*b for a,b in zip(c,u))-u[-1]**2
            assert F_u==0
            if u==v:
                continue
            # First-order cone optimality implies global QP optimality:
            # this is independent of bounding the full objective difference.
            dot=sum((tau*v[i]-c[i]-(lam if i==n-1 else 0))*(u[i]-v[i]) for i in range(n))
            assert dot>=Delta/2
            checked+=1
    z=s.symbols('z:'+str(n))
    telescope=sum(s.Rational(gamma)**(2*(n-j-1))*(z[j]-s.Rational(gamma)*(z[j-1] if j else 0))*(1-s.Rational(gamma)*(z[j-1] if j else 0)-z[j]) for j in range(n))
    assert s.expand(telescope-(z[-1]-sum(s.Rational(c[i])*z[i] for i in range(n))-z[-1]**2))==0
    for T in range(W+1):
        found=any(abs(weights[0]*v[0]+weights[1]*v[-1]-T)<=F(1,4) for _,v in padded)
        expected=any(sum(w*b for w,b in zip(weights,bits))==T for bits in itertools.product((0,1),repeat=2))
        assert found==expected
    return {'padding_length':r,'dimension':n,'retained_vertices':4,'strict_gradient_vertex_tests':checked,'symbolic_telescope':True}


if __name__=='__main__':
    result={'dense_constant_gap':dense_check(),'padded_path':padded_check(),
            'oracle':[
                oracle_check(s.Matrix([[2,1],[1,2]]),s.Matrix([-1,0])),
                oracle_check(s.Matrix([[s.Rational(2,3),s.Rational(-1,6)],[s.Rational(-1,6),s.Rational(1,2)]]),s.Matrix([s.Rational(-1,7),s.Rational(-5,9)])),
                oracle_check(s.diag(s.Rational(1,8),s.Rational(1,8)),s.Matrix([0,s.Rational(-1,8)]))]}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
