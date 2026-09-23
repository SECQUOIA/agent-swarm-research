"""Independent bounded-rank theorem checks; does not import the candidate oracle.

Exact integer minors and dual multipliers are checked exhaustively for two small
graphs. Numerical support and Minkowski membership checks use SciPy HiGHS.
Run from any directory with Python, NumPy, and SciPy; JSON is saved beside script.
"""
import json
from pathlib import Path
from itertools import combinations
from math import gcd, floor
from functools import reduce
import numpy as np
from scipy.optimize import linprog

def det(a):
    a=np.asarray(a,dtype=object)
    if len(a)==0:return 1
    if len(a)==1:return int(a[0,0])
    return sum((-1)**j*int(a[0,j])*det(np.delete(a[1:],j,axis=1)) for j in range(len(a)))
def null(a):
    a=np.asarray(a,dtype=int); s=a.shape[1]
    h=tuple((-1)**i*det(np.delete(a,i,axis=1)) for i in range(s))
    g=reduce(gcd,map(abs,h))
    if not g:return None
    h=tuple(x//g for x in h)
    return h if next(x for x in h if x)>0 else tuple(-x for x in h)
def audit(C,seed):
    rng=np.random.default_rng(seed); s=C.shape[1]
    M=np.array(sorted({tuple(a) for a in C}|{tuple(-a) for a in C}),int)
    # All square minors: verify TU independently, including full-size minors.
    minorcount=0
    for k in range(1,s+1):
      for rows in combinations(range(len(M)),k):
       for cols in combinations(range(s),k):
        assert abs(det(M[np.ix_(rows,cols)]))<=1
        minorcount+=1
    D=sorted({d for rows in combinations(M,s-1) if (d:=null(rows)) is not None})
    assert all(abs(int(v))<=1 for v in (M@np.array(D).T).flat)
    R=sorted({q for rows in combinations(D,s-1) if (h:=null(rows)) is not None for q in (h,tuple(-x for x in h))})
    H=max(1,floor((s-1)**((s-1)/2)))
    assert max(abs(v) for h in R for v in h)<=H
    bases=[]
    for ids in combinations(range(len(M)),s):
      B=M[list(ids)]; delta=det(B)
      if delta:
       inv=np.array([[(-1)**(i+j)*det(np.delete(np.delete(B,i,axis=0),j,axis=1))//delta for j in range(s)] for i in range(s)])
       assert np.array_equal(B.T@inv,np.eye(s,dtype=int))
       bases.append((ids,inv))
    libs=[]; maxq=0
    for h in R:
      lib=[]
      for ids,inv in bases:
       q=inv@h
       assert max(abs(int(v)) for v in q)<=H
       if min(q)>=0:lib.append((ids,q));maxq=max(maxq,max(q))
      assert lib
      libs.append(lib)
    # Exercise full-dimensional, point, and intermediate-dimensional state slices.
    comparisons=0; membership_comparisons=0; fixed_rows=M[list(bases[0][0])]
    for trial in range(30):
      ds=[]; weights=rng.dirichlet(np.ones(3)); chosen=[]
      if trial == 29:
       weights[0]=0; weights/=sum(weights)
      for state in range(3):
       w=weights[state]; d=np.full(len(M),w); center=rng.uniform(-.1,.1,s)*w
       fix=trial%(s+1)
       chosen.append(center)
       for a in fixed_rows[:fix]:
        val=a@center
        d[np.all(M==a,axis=1)]=val
        d[np.all(M==-a,axis=1)]=-val
       ds.append(d)
       for h,lib in zip(R,libs):
        expected=linprog(-np.array(h,float),A_ub=M,b_ub=d,bounds=[(None,None)]*s,method='highs')
        assert expected.success
        actual=min(q@d[list(ids)] for ids,q in lib)
        assert abs(actual+expected.fun)<1e-8
        comparisons+=1
      # Compare R inequalities with full disaggregated feasibility for arbitrary sums.
      A=np.zeros((3*len(M),3*s))
      for j in range(3):A[j*len(M):(j+1)*len(M),j*s:(j+1)*s]=M
      center_sum=sum(chosen)
      for theta in (rng.uniform(-1.5,1.5,s), center_sum, center_sum+10):
       support_ok=all(np.dot(h,theta)<=sum(min(q@d[list(ids)] for ids,q in lib) for d in ds)+1e-8 for h,lib in zip(R,libs))
       lp=linprog(np.zeros(3*s),A_ub=A,b_ub=np.concatenate(ds),A_eq=np.tile(np.eye(s),(1,3)),b_eq=theta,bounds=[(None,None)]*(3*s),method='highs')
       assert support_ok==lp.success
       membership_comparisons+=1
    return {'rank':s,'normals':len(M),'directions':len(D),'ray_candidates':len(R),'bases':len(bases),'all_square_minors':minorcount,'max_multiplier':int(maxq),'H':H,'support_LP_comparisons':comparisons,'sum_membership_comparisons':membership_comparisons}

# Incidence tree is the star rooted at vertex 0. Chords join the other vertices.
# K4 and K4 with one duplicated chord. Each displayed tree row is a signed incidence row.
C3=np.array([[-1,-1,0],[1,0,-1],[0,1,1],[1,0,0],[0,1,0],[0,0,1]])
C4=np.array([[-1,-1,0,-1],[1,0,-1,1],[0,1,1,0],[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])

def audit_sharp_k4():
    """Check the sharp section with exact arc flows and a raw 24-variable EF."""
    from fractions import Fraction as F

    arcs = [(1, 2), (1, 3), (2, 3), (0, 1), (0, 2), (0, 3)]
    C = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1],
                  [1, 1, 0], [-1, 0, 1], [0, -1, -1]], dtype=object)
    A = np.zeros((4, 6), dtype=object)
    for e, (tail, head) in enumerate(arcs):
        A[tail, e] = -1
        A[head, e] = 1
    assert not np.any(A @ C)
    v = np.array([F(1, 2)] * 6, dtype=object)
    b = A @ v
    target = np.array([F(1, 8), F(0), F(1, 8)], dtype=object)
    xbar = v + C @ target
    assert tuple(xbar) == (F(5, 8), F(1, 2), F(5, 8),
                            F(5, 8), F(1, 2), F(3, 8))
    assert np.array_equal(A @ xbar, b)
    observations = [(0, 0), (1, 0), (4, 0), (0, 1),
                    (5, 1), (2, 2), (3, 2)]
    eq = []
    rhs_base = []
    for state in range(4):
        for node in range(4):
            row = np.zeros(24)
            row[state * 6:(state + 1) * 6] = A[node]
            eq.append(row)
            rhs_base.append(float(b[node] / 4))
    for e in range(6):
        row = np.zeros(24)
        row[e::6] = 1
        eq.append(row)
        rhs_base.append(float(xbar[e]))
    for e, state in observations:
        row = np.zeros(24)
        row[state * 6 + e] = 1
        eq.append(row)
    eq = np.array(eq)
    feasible_checks = 0
    infeasible_checks = 0
    boundary_checks = 0
    for pa in range(-7, 8):
        for qa in range(-7, 8):
            p, q = F(pa, 256), F(qa, 256)
            U, V = F(1, 8) + p, F(1, 8) + q
            w = 2 * p + q
            z = [U, V] + [F(1, 8)] * 5
            rhs = np.array(rhs_base + list(map(float, z)))
            lp = linprog(np.zeros(24), A_eq=eq, b_eq=rhs,
                         bounds=[(0, .25)] * 24, method='highs')
            assert lp.success == (w >= 0)
            # The support certificate is exact even when the LP is infeasible.
            assert (2 * U + V >= F(3, 8)) == (w >= 0)
            if w >= 0:
                theta = [np.array([p, q, p], dtype=object),
                         np.array([F(0), -q/2, q/2], dtype=object),
                         np.array([q/2, -q/2, F(0)], dtype=object),
                         np.array([F(1, 8)-w/2, F(0), F(1, 8)-w/2], dtype=object)]
                assert np.array_equal(sum(theta), target)
                flows = [v/4 + C @ t for t in theta]
                assert np.array_equal(sum(flows), xbar)
                for f in flows:
                    assert all(F(0) <= value <= F(1, 4) for value in f)
                    assert np.array_equal(A @ f, b/4)
                assert [flows[state][e] for e, state in observations] == z
                assert sum(theta[-1]) == F(1, 4)-w
                feasible_checks += 1
                boundary_checks += (w == 0)
            else:
                infeasible_checks += 1
    return {"raw_state_LP_grid_comparisons": feasible_checks + infeasible_checks,
            "exact_feasible_arc_decompositions": feasible_checks,
            "exact_negative_support_certificates": infeasible_checks,
            "boundary_points": boundary_checks,
            "section": "2 U + V >= 3/8",
            "status": "passed"}

if __name__ == "__main__":
    output = {
        "seed_rank_three": 20260907,
        "seed_rank_four": 20260908,
        "checks": [audit(C3, 20260907), audit(C4, 20260908)],
        "sharp_k4": audit_sharp_k4(),
        "status": "passed",
        "caveat": "Floating-point LP comparisons are computational checks, not proofs."
    }
    destination = Path(__file__).with_name("bounded_rank_results.json")
    destination.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))
