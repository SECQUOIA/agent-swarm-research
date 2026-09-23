"""Exact structural check of the MINLPLib elec instances (Thomson problem).

Asserts, from the OSiL file, that the model is exactly
    min  sum_{a<b} 1 / sqrt( sum_{c=0..2} (x[a + cN] - x[b + cN])^2 )
    s.t. x[i]^2 + x[i+N]^2 + x[i+2N]^2 = 1   (i = 0..N-1),  x free continuous,
with each unordered pair {a, b} appearing exactly once. Returns N.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from osil_eval import Model, _t  # noqa: E402

OS = os.path.expanduser("~/.cache/minlplib/minlplib/osil/")


def _diff_pair(e):
    """e must be sum(variable a, variable b coef=-1) (either order); return (a, b) with a the +1 term."""
    assert _t(e) == "sum", _t(e)
    ch = list(e)
    assert len(ch) == 2 and all(_t(c) == "variable" for c in ch)
    coefs = [c.get("coef", "1") for c in ch]
    idx = [int(c.get("idx")) for c in ch]
    assert sorted(coefs) == ["-1", "1"], coefs
    return (idx[0], idx[1]) if coefs[0] == "1" else (idx[1], idx[0])


def check(name):
    M = Model(OS + name + ".osil")
    assert M.n % 3 == 0
    N = M.n // 3
    assert M.m == N
    assert all(t == "C" for t in M.vtype)
    assert all(lb == "-INF" for lb in M.vlb) and all(ub == "INF" for ub in M.vub)
    # constraints: ||p_i||^2 = 1 exactly
    for r in range(M.m):
        assert M.clb[r] == "1" and M.cub[r] == "1" and M.cconst[r] == "0", r
        assert not M.lin[r] and r not in M.nl
        assert sorted(M.quad[r]) == sorted([(i, i, "1") for i in (r, r + N, r + 2 * N)]), r
    assert set(M.quad) == set(range(M.m))  # no quadratic objective terms
    # objective
    assert M.objsense == "min" and not M.objlin and M.objconst == "0"
    assert set(M.nl) == {-1}
    root = M.nl[-1]
    assert _t(root) == "sum"
    pairs = set()
    for term in root:
        assert _t(term) == "divide"
        num, den = list(term)
        assert _t(num) == "number" and num.get("value") == "1" and num.get("type") in (None, "real")
        assert _t(den) == "sqrt"
        (inner,) = list(den)
        assert _t(inner) == "sum"
        sq = list(inner)
        assert len(sq) == 3 and all(_t(s) == "square" for s in sq)
        ab = [_diff_pair(list(s)[0]) for s in sq]
        a, b = ab[0]
        assert 0 <= a < N and 0 <= b < N and a != b
        # one squared difference per coordinate c, between the coordinates of points a and b
        # (orientation is irrelevant because the difference is squared)
        assert {frozenset(p) for p in ab} == {frozenset((a + c * N, b + c * N)) for c in range(3)}
        key = (min(a, b), max(a, b))
        assert key not in pairs
        pairs.add(key)
    assert len(pairs) == N * (N - 1) // 2
    return N


if __name__ == "__main__":
    for nm in sys.argv[1:] or ["elec25", "elec50", "elec100", "elec200"]:
        print(nm, "N =", check(nm), "structure verified")
