"""Independent complete continuous-price stationary-face baseline.

Input is a mapping of rational instance DATA. No compressed solver is imported.
All principal Hessian minors are checked; singular inputs are rejected. The
original quadratic is compared globally, retaining every exact tie. Optimistic
and universally feasible pessimistic tariff maximization use separate code.
This exponential reference method is intended only for small instances.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from functools import cmp_to_key
from itertools import combinations, product
import sympy as s


def rational(v):
    if isinstance(v,float) or isinstance(v,s.Float):
        raise TypeError('Exact rational input required')
    return F(v)


def algebraic(v): return s.Rational(v.numerator,v.denominator) if isinstance(v,F) else s.sympify(v)
def compare(a,b):
    v=algebraic(a)-algebraic(b)
    if v.is_Rational: return 1 if v > 0 else -1 if v < 0 else 0
    v=s.simplify(v)
    if v==0: return 0
    if v.is_positive is True: return 1
    if v.is_negative is True: return -1
    if bool(v>0): return 1
    if bool(v<0): return -1
    raise ArithmeticError('Could not decide algebraic order')


def sorted_distinct(values):
    result=[]
    for v in sorted(values,key=cmp_to_key(compare)):
        if not result or compare(v,result[-1]): result.append(v)
    return result


def interior(a,b):
    if compare(a,b)>=0: raise ValueError('Nonempty open interval required')
    a,b=algebraic(a),algebraic(b)
    if a.is_Rational and b.is_Rational: return (a+b)/2
    q=1
    while True:
        v=(s.floor(q*a)+1)/s.Integer(q)
        if compare(v,b)<0: return v
        q*=2


def intersect(interval,constant,slope):
    lo,hi=interval
    if slope>0:
        edge=-constant/slope
        if compare(edge,hi)<0: hi=edge
    elif slope<0:
        edge=-constant/slope
        if compare(edge,lo)>0: lo=edge
    elif constant>0: return None
    return None if compare(lo,hi)>0 else (lo,hi)


def evaluate(coeff,x):
    x=algebraic(x)
    return s.expand(algebraic(coeff[0])+x*(algebraic(coeff[1])+x*algebraic(coeff[2])))


def roots(coeff):
    c,b,a=coeff
    if not a: return [] if not b else [-c/b]
    d=b*b-4*a*c
    if d<0: return []
    return [(-algebraic(b)+s.sqrt(algebraic(d)))/(2*algebraic(a)),
            (-algebraic(b)-s.sqrt(algebraic(d)))/(2*algebraic(a))]


@dataclass(frozen=True)
class Face:
    a: tuple
    b: tuple
    lo: F
    hi: F
    cost: tuple
    w: tuple
    def point(self,x): return tuple(s.expand(algebraic(a)+algebraic(b)*algebraic(x)) for a,b in zip(self.a,self.b))


@dataclass
class FaceAtlas:
    data: dict
    faces: list
    cuts: list
    cells: list
    points: list
    principal_minors: dict
    patterns_examined: int


def build(data):
    """Check all minors; enumerate original stationary faces and all cost crossings."""
    d={name:tuple(map(rational,data[name])) for name in ('d','c','u','lower','upper')}
    d.update({name:rational(data[name]) for name in ('h','gamma','x_lower','x_upper')})
    n=len(d['d'])
    if n==0 or any(len(d[k])!=n for k in ('c','u','lower','upper')): raise ValueError('Bad dimensions')
    if any(v<=0 for v in d['d']) or d['h']<0 or not d['gamma'] or d['x_lower']>d['x_upper']: raise ValueError('Unsupported data')
    if any(lo>hi for lo,hi in zip(d['lower'],d['upper'])): raise ValueError('Reversed box')
    Q=[[d['d'][i]*int(i==j)-d['h']*d['u'][i]*d['u'][j] for j in range(n)] for i in range(n)]
    matrix=s.Matrix(Q); minors={():F(1)}; positive={():True}
    for size in range(1,n+1):
        for subset in combinations(range(n),size):
            det=F(matrix.extract(subset,subset).det()); minors[subset]=det
            if det==0: raise ValueError(f'Singular principal Hessian minor {subset}; baseline unsupported')
            positive[subset]=all(minors[subset[:j]]>0 for j in range(1,len(subset)+1))
    faces=[]; examined=0; seen=set()
    states=[(-1,) if lo==hi else (-1,0,1) for lo,hi in zip(d['lower'],d['upper'])]
    for pattern in product(*states):
        examined+=1
        free=tuple(i for i,v in enumerate(pattern) if v==0)
        if not positive[free]: continue
        fixed=[i for i in range(n) if i not in free]
        a=[F(0) if i in free else d['lower'][i] if pattern[i]==-1 else d['upper'][i] for i in range(n)]
        b=[F(0)]*n
        if free:
            inv=matrix.extract(free,free).inv()
            intercept=inv*s.Matrix([-d['c'][i]-sum(Q[i][j]*a[j] for j in fixed) for i in free])
            slope=inv*s.Matrix([-d['gamma']*d['u'][i] for i in free])
            for i,v,w in zip(free,intercept,slope): a[i],b[i]=F(v),F(w)
        interval=(d['x_lower'],d['x_upper'])
        for i in range(n):
            if i in free:
                rows=[(d['lower'][i]-a[i],-b[i]),(a[i]-d['upper'][i],b[i])]
            elif d['lower'][i]==d['upper'][i]: rows=[]
            else:
                ga=d['c'][i]+sum(Q[i][j]*a[j] for j in range(n))
                gb=d['gamma']*d['u'][i]+sum(Q[i][j]*b[j] for j in range(n))
                rows=[(-ga,-gb)] if pattern[i]==-1 else [(ga,gb)]
            for const,slope in rows:
                interval=intersect(interval,const,slope)
                if interval is None: break
            if interval is None: break
        if interval is None: continue
        # Direct substitution into the ORIGINAL dense quadratic, never C(w).
        cost=(sum(a[i]*Q[i][j]*a[j]/2 for i in range(n) for j in range(n))+sum(ci*ai for ci,ai in zip(d['c'],a)),
              sum(a[i]*Q[i][j]*b[j] for i in range(n) for j in range(n))+sum(ci*bi+d['gamma']*ui*ai for ci,ui,ai,bi in zip(d['c'],d['u'],a,b)),
              sum(b[i]*Q[i][j]*b[j]/2 for i in range(n) for j in range(n))+d['gamma']*sum(ui*bi for ui,bi in zip(d['u'],b)))
        w=(sum(ui*ai for ui,ai in zip(d['u'],a)),sum(ui*bi for ui,bi in zip(d['u'],b)))
        key=(tuple(a),tuple(b),interval)
        if key not in seen:
            faces.append(Face(tuple(a),tuple(b),*interval,cost,w));seen.add(key)
    if not faces: raise ArithmeticError('No stationary face: completeness contract failed')
    cuts=[d['x_lower'],d['x_upper']]+[v for f in faces for v in (f.lo,f.hi)]
    for f,g in combinations(faces,2):
        lo,hi=max(f.lo,g.lo),min(f.hi,g.hi)
        if lo>hi: continue
        for root in roots(tuple(a-b for a,b in zip(f.cost,g.cost))):
            if compare(root,lo)>=0 and compare(root,hi)<=0: cuts.append(root)
    cuts=sorted_distinct(cuts)
    def winners(x):
        available=[i for i,f in enumerate(faces) if compare(x,f.lo)>=0 and compare(x,f.hi)<=0]
        if not available: raise ArithmeticError('Uncovered price')
        values={i:evaluate(faces[i].cost,x) for i in available}
        best=min(values.values(),key=cmp_to_key(compare))
        return tuple(i for i in available if compare(values[i],best)==0)
    cells=[(a,b,winners(interior(a,b))) for a,b in zip(cuts,cuts[1:])]
    points=[(x,winners(x)) for x in cuts]
    return FaceAtlas(d,faces,cuts,cells,points,minors,examined)


def optimize(atlas,rows=(),semantics='optimistic'):
    """Independent upper solver: maximize x*u'z with exact endpoint inclusion."""
    if semantics not in ('optimistic','pessimistic'): raise ValueError('Unknown semantics')
    rows=[(rational(row['a']),tuple(map(rational,row['b'])),rational(row['rhs'])) for row in rows]
    if any(len(b)!=len(atlas.data['d']) for _,b,_ in rows): raise ValueError('Upper row dimension')
    best=None
    def save(x,face,attained):
        nonlocal best
        x=algebraic(x); w=s.expand(algebraic(face.w[0])+algebraic(face.w[1])*x); value=s.expand(x*w)
        if best is None or compare(value,best['value'])>0 or (compare(value,best['value'])==0 and attained and not best['attained']):
            best=dict(value=value,attained=attained,x=x if attained else None,w=w if attained else None,
                      z=face.point(x) if attained else None,limit_x=None if attained else x,limit_w=None if attained else w)
    for left,right,win in atlas.cells:
        # Equal winning value polynomials have equal gamma*u'z derivatives.
        assert all(atlas.faces[i].w==atlas.faces[win[0]].w for i in win)
        groups=[win] if semantics=='pessimistic' else [(i,) for i in win]
        for group in groups:
            interval=(left,right)
            for i in group:
                f=atlas.faces[i]
                for a,b,rhs in rows:
                    interval=intersect(interval,sum(bi*ai for bi,ai in zip(b,f.a))-rhs,a+sum(bi*vi for bi,vi in zip(b,f.b)))
                    if interval is None: break
                if interval is None: break
            if interval is None: continue
            lo,hi=interval
            if compare(hi,left)<=0 or compare(lo,right)>=0: continue
            f=atlas.faces[group[0]]; candidates=[lo,hi]
            if compare(lo,hi)<0: candidates.append(interior(lo,hi))
            if f.w[1]<0:
                stationary=-f.w[0]/(2*f.w[1])
                if compare(stationary,lo)>=0 and compare(stationary,hi)<=0:candidates.append(stationary)
            for x in candidates: save(x,f,compare(x,left)>0 and compare(x,right)<0)
    for x,win in atlas.points:
        valid=[]
        for i in win:
            f=atlas.faces[i];z=f.point(x)
            if all(compare(algebraic(a)*algebraic(x)+sum(algebraic(bi)*zi for bi,zi in zip(b,z)),rhs)<=0 for a,b,rhs in rows):valid.append(i)
        if semantics=='pessimistic':
            if len(valid)!=len(win): continue
            i=min(win,key=cmp_to_key(lambda i,j:compare(evaluate((0,*atlas.faces[i].w),x),evaluate((0,*atlas.faces[j].w),x))))
            save(x,atlas.faces[i],True)
        else:
            for i in valid:save(x,atlas.faces[i],True)
    return best
