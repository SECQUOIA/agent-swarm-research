"""Cross-check qosil.py against the previous verifier's reader (reviews/bound-audit-verification/osil.py).

Compares every bound, type, objective coefficient, row bound/constant and linear/quadratic
coefficient exactly. Two readers written separately agreeing is evidence that neither misreads
these files.
"""
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "bound-audit-verification"))
import osil  # previous verifier's reader
import qosil


def qnorm(terms):
    c = Counter()
    for a, b, v in terms:
        c[(min(a, b), max(a, b))] += v
    return {k: v for k, v in c.items() if v != 0}


for name in sys.argv[1:]:
    p = os.path.join(HERE, "data", name + ".osil")
    A, B = qosil.Model(p), osil.parse(p)
    assert A.n == B.n and A.m == B.m and A.name == B.vname and A.cname == B.cname
    assert A.lb == B.lb and A.ub == B.ub and A.type == B.vtype
    assert A.sense == B.sense and A.obj_const == B.obj_const and A.obj_lin == B.obj_lin
    assert qnorm(A.obj_Q) == qnorm(B.obj_quad)
    assert A.clb == B.clb and A.cub == B.cub and A.cconst == B.cconst
    for i in range(A.m):
        assert A.A[i] == B.lin[i], i
        assert qnorm(A.Q[i]) == qnorm(B.quad[i]), i
        assert B.nl[i] is None
    assert B.obj_nl is None
    print(f"{name}: identical ({A.n} variables, {A.m} rows, "
          f"{sum(len(r) for r in A.A)} linear and {sum(len(q) for q in A.Q) + len(A.obj_Q)} quadratic terms)")
