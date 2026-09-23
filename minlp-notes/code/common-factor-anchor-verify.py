"""Exact envelope construction, with independent finite-measure LP checks."""
from fractions import Fraction as F
from itertools import combinations
import random
import numpy as np
from scipy.optimize import linprog


def envelope(a, b, m, qs, ws):
    # line = intercept + slope*s; exact intersections, robust to duplicate lines.
    lines = [(F(0), F(0)), (m, F(-1))]
    for q, w in zip(qs, ws):
        lines.extend([(w, -q), (m-w, q-1)])
    points = {a, b}
    for (v, d), (vv, dd) in combinations(lines, 2):
        if d != dd:
            x = (vv-v)/(d-dd)
            if a < x < b:
                points.add(x)
    points = sorted(points)
    active = []
    for left, right in zip(points, points[1:]):
        mid = (left+right)/2
        line = max(lines, key=lambda z: z[0]+z[1]*mid)
        if active and active[-1][2] == line:
            active[-1] = (active[-1][0], right, line)
        else:
            active.append((left, right, line))
    atoms = []
    prev = F(-1)
    for left, right, (v, d) in active:
        if d > prev:
            atoms.append((left, d-prev))
        assert d >= prev
        prev = d
    if prev < 0:
        atoms.append((b, -prev))
    assert sum(p for x, p in atoms) == 1
    assert sum(x*p for x, p in atoms) == m
    tmin = sum(p/x for x, p in atoms)
    integral = 1/a-(m-a)/(a*a)
    for left, right, (v, d) in active:
        integral += v*(1/(left*left)-1/(right*right))+2*d*(1/left-1/right)
    assert integral == tmin
    return tmin, atoms, active


def finite_measure_lp(a,b,m,qs,ws,atoms,integer=False):
    # μ_h is the shared scalar law; ν_jh is the leaf's selected submeasure.
    xs = list(map(F,range(int(a),int(b)+1))) if integer else sorted({x for x,p in atoms} | {a+(b-a)*F(i,30) for i in range(31)})
    n,h = len(qs),len(xs)
    obj = np.zeros((n+1)*h)
    obj[:h] = [float(1/x) for x in xs]
    eq, rhs = [], []
    for block, mass, moment in [(0,F(1),m)]+[(j+1,q,w) for j,(q,w) in enumerate(zip(qs,ws))]:
        row = np.zeros((n+1)*h); row[block*h:(block+1)*h] = 1
        eq.append(row); rhs.append(float(mass))
        row = np.zeros((n+1)*h); row[block*h:(block+1)*h] = list(map(float,xs))
        eq.append(row); rhs.append(float(moment))
    ub=[]
    for j in range(n):
        for i in range(h):
            row=np.zeros((n+1)*h); row[(j+1)*h+i]=1; row[i]=-1; ub.append(row)
    res=linprog(obj,A_ub=np.array(ub),b_ub=np.zeros(len(ub)),A_eq=np.array(eq),b_eq=np.array(rhs),bounds=(0,None),method='highs')
    assert res.success,res.message
    return res.fun


def construct_leaf(atoms, q, w):
    """Fractional threshold selections, with exact interpolation for a leaf."""
    h=len(atoms)
    def threshold(reverse):
        remaining=q
        theta=[F(0)]*h
        for i in sorted(range(h),key=lambda i:atoms[i][0],reverse=reverse):
            x,p=atoms[i]
            take=min(p,remaining)
            theta[i]=take/p
            remaining-=take
        assert remaining==0
        value=sum(x*p*z for (x,p),z in zip(atoms,theta))
        return theta,value
    low,vl=threshold(False);high,vh=threshold(True)
    assert vl<=w<=vh
    weight=F(0) if vh==vl else (w-vl)/(vh-vl)
    theta=[(1-weight)*l+weight*u for l,u in zip(low,high)]
    assert all(0<=z<=1 for z in theta)
    assert sum(p*z for (x,p),z in zip(atoms,theta))==q
    assert sum(x*p*z for (x,p),z in zip(atoms,theta))==w
    return theta


def round_atoms(atoms):
    masses={}
    for x,p in atoms:
        lo=x.numerator//x.denominator
        hi=lo+1
        masses[F(lo)]=masses.get(F(lo),F(0))+p*(hi-x)
        masses[F(hi)]=masses.get(F(hi),F(0))+p*(x-lo)
    return sorted((x,p) for x,p in masses.items() if p)


def integer_telescoping(a,b,m,active):
    value=1/a+(1/(a+1)-1/a)*(m-a)
    for left,right,(u,slope) in active:
        ceil_left=-((-left.numerator)//left.denominator)
        ceil_right=-((-right.numerator)//right.denominator)
        ll=max(int(a)+1,ceil_left);rr=min(int(b)-1,ceil_right-1)
        if ll>rr:
            continue
        sd=F(1,ll-1)-F(1,ll)-F(1,rr)+F(1,rr+1)
        skd=F(1,ll-1)+F(1,ll)-F(1,rr)-F(1,rr+1)
        value+=u*sd+slope*skd
    return value


def main():
    rng=random.Random(94214)
    a,b=F(1),F(3)
    count=0
    for n in range(1,11):
        for rep in range(15):
            m=F(rng.randrange(101),50)+a
            qs=[F(rng.randrange(101),100) for _ in range(n)]
            ws=[]
            for q in qs:
                lo=max(a*q,m-b*(1-q)); hi=min(b*q,m-a*(1-q))
                ws.append(lo+(hi-lo)*F(rng.randrange(101),100))
            tmin,atoms,active=envelope(a,b,m,qs,ws)
            val=finite_measure_lp(a,b,m,qs,ws,atoms)
            assert abs(float(tmin)-val)<1e-8,(n,rep,tmin,val)
            assert 1/m <= tmin <= (a+b-m)/(a*b)
            # Construct a hull point at an intermediate reciprocal moment.
            weight=F(rng.randrange(101),100)
            mass={x:(1-weight)*p for x,p in atoms}
            mass[a]=mass.get(a,F(0))+weight*(b-m)/(b-a)
            mass[b]=mass.get(b,F(0))+weight*(m-a)/(b-a)
            mixture=sorted((x,p) for x,p in mass.items() if p)
            assert len(mixture)<=2*n+3
            assert sum(p/x for x,p in mixture)==(1-weight)*tmin+weight*(a+b-m)/(a*b)
            for q,w in zip(qs,ws):
                construct_leaf(mixture,q,w)
            count+=1
    qs=[F(2,3),F(14,29)]; ws=[F(5,3),F(40,29)]
    tmin,atoms,active=envelope(a,b,F(2),qs,ws)
    assert tmin>F(3,5)
    print(f'Passed {count} exact-envelope vs independent shared-measure LP comparisons.')
    print(f'Passed {count} exact rational graph-point decompositions at intermediate reciprocal moments.')
    print(f'Two-leaf incompatible point: minimum reciprocal moment = {tmin} = {float(tmin):.12f} > 3/5.')
    print(f'Exact minimizing common distribution (location, mass): {atoms}')
    integer_count=0
    a,b=F(1),F(11)
    for n in range(1,9):
        for rep in range(15):
            m=a+(b-a)*F(rng.randrange(101),100)
            qs=[F(rng.randrange(101),100) for _ in range(n)]
            ws=[]
            for q in qs:
                lo=max(a*q,m-b*(1-q));hi=min(b*q,m-a*(1-q))
                ws.append(lo+(hi-lo)*F(rng.randrange(101),100))
            tmin,atoms,active=envelope(a,b,m,qs,ws)
            rounded=round_atoms(atoms)
            tz=sum(p/x for x,p in rounded)
            assert integer_telescoping(a,b,m,active)==tz
            val=finite_measure_lp(a,b,m,qs,ws,rounded,integer=True)
            assert abs(float(tz)-val)<1e-8,(n,rep,tz,val)
            assert tz>=tmin
            assert sum(p*x for x,p in rounded)==m
            for q,w in zip(qs,ws):
                construct_leaf(rounded,q,w)
            integer_count+=1
    print(f'Passed {integer_count} integer-law rounded-envelope vs full integer-support LP comparisons, plus exact decompositions.')
    a,b,m=F(1),F(10**12),F(7*10**11,3)
    qs=[F(2,7),F(4,9),F(1,13)]
    ws=[]
    for q in qs:
        lo=max(a*q,m-b*(1-q));hi=min(b*q,m-a*(1-q))
        ws.append((2*lo+hi)/3)
    tmin,atoms,active=envelope(a,b,m,qs,ws)
    rounded=round_atoms(atoms)
    assert integer_telescoping(a,b,m,active)==sum(p/x for x,p in rounded)
    print(f'Passed exact telescoping vs rounding on 10^12 scalar levels using {len(active)} envelope pieces and {len(rounded)} integer atoms.')
    print('Envelope construction uses all pairwise intersections; it verifies the theorem, not the faster O(n log n) implementation.')


if __name__=='__main__':
    main()
