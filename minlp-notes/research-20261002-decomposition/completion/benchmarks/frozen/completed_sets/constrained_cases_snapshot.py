"""Independent tiny constrained-QP corpus and exhaustive rational face oracle."""
from fractions import Fraction as F
from itertools import combinations, product
from time import perf_counter
from corpus import from_squares, random_band
from baseline_corpus import linear_solve, value


def cases():
    data={}
    p=from_squares('network_mixed_5',5,
                  [(1,{0:F(1)},F(-2,5)),(1,{1:F(1)},F(-3,5)),(1,{2:F(1)},-1)],
                  linear=[F(0),F(0),F(0),F(2),F(-2)],diagonal={3:-1},
                  bounds=[(F(0),F(1))]*5,integers=(4,));p.c+=2
    data[p.name]=(p,dict(labels={4:[0,1]},rows=[[1,1,-1,0,0],[0,0,1,1,-1]],rhs=[0,0],senses=['==','=='],tu_certificate={'kind':'network'}))
    p=random_band('ordered_nonconvex_4',4,1,2903)
    data[p.name]=(p,dict(labels={},rows=[[1,-1,0,0],[0,1,-1,0],[0,0,1,-1]],rhs=[0,0,0],senses=['<=']*3,tu_certificate={'kind':'network'}))
    p=from_squares('weighted_integer_column',3,[(1,{0:F(1)},F(-4,3)),(1,{1:F(1)},F(-5,3))],
                   linear=[F(0),F(0),F(-2)],bounds=[(F(0),F(3))]*2+[(F(0),F(1))],integers=(2,));p.c+=2
    data[p.name]=(p,dict(labels={2:[0,1]},rows=[[1,1,-3]],rhs=[0],senses=['=='],tu_certificate={'kind':'network'}))
    for projected in (False,True):
        p=from_squares('large_equality_energy_'+('projected' if projected else 'full'),2,
                       [(1000,{0:F(1),1:F(-1)},0),(1,{0:F(1)},F(-1,3))],bounds=[(F(0),F(1))]*2)
        d=dict(labels={},rows=[[1,-1]],rhs=[0],senses=['=='],tu_certificate={'kind':'network'})
        if projected:d['curvature']={'L':'1','mode':'equalities'}
        data[p.name]=(p,d)
    p=from_squares('infeasible_flow',2,[(1,{0:F(1)},0)],bounds=[(F(0),F(1))]*2)
    data[p.name]=(p,dict(labels={},rows=[[1,1]],rhs=[3],senses=['=='],tu_certificate={'kind':'network'}))
    p=from_squares('invalid_tu_input',1,[(1,{0:F(1)},0)],bounds=[(F(0),F(1))])
    data[p.name]=(p,dict(labels={},rows=[[2]],rhs=[1],senses=['<='],tu_certificate={'kind':'network'}))
    return data


def exact_reference(p, model):
    """All active faces, with no use of a solver's grid or certificate code.

    Singular stationary faces have a flat tangent direction to a smaller face;
    thus considering all nonsingular face KKT systems suffices on this compact
    polytope. This corpus has linearly independent equality rows; redundant
    equalities would require row reduction before using this narrow oracle.
    All comparisons and feasibility checks use rational arithmetic.
    """
    started=perf_counter();labels=model['labels'];discrete=sorted(labels)
    free=[i for i in range(len(p.b)) if i not in labels];n=len(free)
    best=None;witness=None;systems=0
    for assignment in product(*(labels[i] for i in discrete)):
        fixed=dict(zip(discrete,map(F,assignment)))
        equal=[];ineq=[]
        for row,rhs,sense in zip(model['rows'],model['rhs'],model['senses']):
            pair=([F(row[i]) for i in free], F(rhs)-sum((F(row[i])*x for i,x in fixed.items()),F(0)))
            (equal if sense=='==' else ineq).append(pair)
        echelon=[]
        for row,_ in equal:
            reduced=list(row)
            for pivot,base in echelon:
                factor=reduced[pivot]
                reduced=[a-factor*b for a,b in zip(reduced,base)]
            pivot=next((j for j,v in enumerate(reduced) if v),None)
            if pivot is None:
                raise ValueError('Narrow reference oracle requires independent equality rows')
            scale=reduced[pivot]
            echelon.append((pivot,[v/scale for v in reduced]))
        for j,i in enumerate(free):
            unit=[F(k==j) for k in range(n)]
            ineq.extend([(unit,p.bounds[i][1]),([-v for v in unit],-p.bounds[i][0])])
        for k in range(max(0,n-len(equal))+1):
            for chosen in combinations(ineq,k):
                active=equal+list(chosen);m=len(active)
                h=[[p.A[i][j] for j in free] for i in free]
                b=[p.b[i]+sum((p.A[i][j]*x for j,x in fixed.items()),F(0)) for i in free]
                mat=[h[j]+[a[j] for a,_ in active] for j in range(n)]
                mat += [a+[F(0)]*m for a,_ in active]
                rhs=[-v for v in b]+[v for _,v in active]
                systems+=1;sol=linear_solve(mat,rhs)
                if sol is None:continue
                x=sol[:n]
                if any(sum(a[j]*x[j] for j in range(n))!=rhs for a,rhs in equal):continue
                if any(sum(a[j]*x[j] for j in range(n))>rhs for a,rhs in ineq):continue
                point=dict(fixed);point.update(zip(free,x));point=tuple(point[i] for i in range(len(p.b)))
                objective=value(p,point)
                if best is None or objective<best:best,witness=objective,point
    return {'objective':None if best is None else str(best),'point':None if witness is None else list(map(str,witness)),
            'infeasible':best is None,'kkt_systems':systems,'seconds':perf_counter()-started}
