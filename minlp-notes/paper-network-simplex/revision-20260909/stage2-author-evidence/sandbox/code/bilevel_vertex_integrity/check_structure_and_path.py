"""Exact small-instance checks for fixed-core PWL and path Subset Sum."""
from fractions import Fraction as F
from itertools import combinations, product


def clip(x):
    return min(F(1), max(F(0), x))


def solve(rows, rhs):
    n = len(rows)
    A = [[F(v) for v in row] + [F(b)] for row,b in zip(rows,rhs)]
    for j in range(n):
        p = next((i for i in range(j,n) if A[i][j]), None)
        if p is None:
            return None
        A[j],A[p] = A[p],A[j]
        d = A[j][j]
        A[j] = [v/d for v in A[j]]
        for i in range(n):
            if i != j:
                d = A[i][j]
                A[i] = [v-d*w for v,w in zip(A[i],A[j])]
    return tuple(A[i][-1] for i in range(n))


def vertices(dim, hyperplanes):
    rows = list(hyperplanes)
    for j in range(dim):
        normal = tuple(F(int(i==j)) for i in range(dim))
        rows.extend([(normal,F(0)),(normal,F(1))])
    points = set()
    for basis in combinations(rows,dim):
        x = solve([r[0] for r in basis],[r[1] for r in basis])
        if x is not None and all(0<=v<=1 for v in x):
            points.add(x)
    return points


def path_case(weights,target):
    n = len(weights)
    W = sum(weights)
    r = [F(a,W) for a in weights]
    tau = F(target,W)
    planes = []
    for i,ri in enumerate(r,1):
        row = tuple(F(int(j==i)-int(j==i-1)) for j in range(n+1))
        planes.extend((row,b) for b in (F(0),ri/2,ri))
    planes.append((tuple(F(int(j==n)) for j in range(n+1)),tau))
    points = vertices(n+1,planes)
    def objective(x):
        direct = x[0]+abs(x[-1]-tau)
        ramp = 2*x[0]-2*x[-1]+tau+2*clip(x[-1]-tau)
        for i,ri in enumerate(r,1):
            d=x[i]-x[i-1]
            direct += min(abs(d),abs(d-ri))
            ramp += 2*(clip(d)-clip(d-ri/2)+clip(d-ri))
        assert direct == ramp
        return direct
    best = min(map(objective,points))
    subset = min(abs(sum(a*b for a,b in zip(weights,bits))-target)
                 for bits in product((0,1),repeat=n))
    assert best == F(subset,W)
    return len(points)


# A block ramp is (weight, constant, core coefficient, leaf coefficient).
def block_value(block,u,v):
    return sum(w*clip(a+b*u+c*v) for w,a,b,c in block)


def candidates(block):
    result={(F(0),F(0)),(F(0),F(1))}
    for w,a,b,c in block:
        if c:
            result.update((-b/c,(t-a)/c) for t in (F(0),F(1)))
    return result


def core_check(blocks):
    blocks=[[tuple(map(F,row)) for row in block] for block in blocks]
    cand=[candidates(block) for block in blocks]
    breaks={F(0),F(1)}
    def add_root(slope,constant):
        if slope:
            u=-constant/slope
            if 0<=u<=1:
                breaks.add(u)
    for block,cs in zip(blocks,cand):
        for p,q in cs:
            for t in (F(0),F(1)):
                add_root(p,q-t)
            for w,a,b,c in block:
                for t in (F(0),F(1)):
                    add_root(b+c*p,a+c*q-t)
    first=sorted(breaks)
    for left,right in zip(first,first[1:]):
        mid=(left+right)/2
        for block,cs in zip(blocks,cand):
            feasible=[(p,q) for p,q in cs if 0<=p*mid+q<=1]
            values=[]
            for p,q in feasible:
                vl=block_value(block,left,p*left+q)
                vr=block_value(block,right,p*right+q)
                slope=(vr-vl)/(right-left)
                values.append((slope,vl-slope*left))
            for (s1,c1),(s2,c2) in combinations(values,2):
                if s1!=s2:
                    u=-(c1-c2)/(s1-s2)
                    if left<=u<=right:
                        breaks.add(u)
    def reduced(u):
        return sum(min(block_value(block,u,p*u+q)
                       for p,q in cs if 0<=p*u+q<=1)
                   for block,cs in zip(blocks,cand))
    cell_best=min(map(reduced,breaks))
    planes=[]
    for j,block in enumerate(blocks,1):
        for w,a,b,c in block:
            normal=[F(0)]*(len(blocks)+1)
            normal[0]=b; normal[j]=c
            planes.extend((tuple(normal),t-a) for t in (F(0),F(1)))
    pts=vertices(len(blocks)+1,planes)
    global_best=min(sum(block_value(block,x[0],x[j])
                        for j,block in enumerate(blocks,1)) for x in pts)
    assert global_best == cell_best
    return len(pts),len(breaks)


def main():
    count=sum(path_case(w,t) for w,t in [([2,4],3),([2,4],2),([1,3,5],2),([1,3,5],4)])
    examples=[
        [[(1,0,1,1),(-2,0,-1,2)],[(2,1,-2,1),(-1,0,1,-1)]],
        [[(-1,0,0,1),(2,-1,2,1)],[(1,1,0,-1),(-2,0,-1,1)]],
        [[(1,1,2,1),(-1,0,-1,2)],[(1,0,1,0),(-1,1,-1,1)]],
    ]
    results=[core_check(blocks) for blocks in examples]
    print(f'PASS: {count} exact path arrangement vertices across4 instances; fixed-core comparisons {results}')


if __name__ == '__main__':
    main()
