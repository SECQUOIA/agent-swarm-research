"""Exact identification of the MINLPLib hadamard_n models as  max det(B)  over 0/1 matrices B.

Checks from the OSiL file (via the independent parser osil_eval.Model):
  * variables b1..b_{n^2} binary in [0, 1], objvar continuous and free; objective max objvar;
  * one row  e1:  poly(b) - objvar >= 0  (no other terms, constant 0);
  * poly is a sum of products of variables with coefficients +-1, and its coefficient dictionary
    (monomial = set of variable indices) equals, term by term, the Leibniz expansion
    det(B) = sum_pi sgn(pi) prod_i B[i, pi(i)]  with  B[i, j] = b_{i*n + j + 1}  (row-major).
    Each product has n distinct variables, so the identity is an identity of real polynomials
    (no reduction b^2 = b is used). Equality of coefficient dictionaries is an exact proof.
Hence the optimal value of hadamard_n equals D01(n) = max { det B : B in {0,1}^{n x n} }.
Usage: python had_model.py [n ...]
"""
import itertools
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from osil_eval import Model, _t  # noqa: E402

OS = os.path.expanduser("~/.cache/minlplib/minlplib/osil/")


def perm_sign(p):
    s, seen = 1, [False] * len(p)
    for i in range(len(p)):
        if not seen[i]:
            j, L = i, 0
            while not seen[j]:
                seen[j] = True; j = p[j]; L += 1
            if L % 2 == 0:
                s = -s
    return s


def leibniz(n):
    return {frozenset(i * n + p[i] for i in range(n)): perm_sign(p) for p in itertools.permutations(range(n))}


def extract_poly(root):
    assert _t(root) == "sum"
    poly = defaultdict(int)
    for term in root:
        assert _t(term) == "product", _t(term)
        coef, idx = 1, []
        for v in term:
            assert _t(v) == "variable"
            c = v.get("coef", "1")
            assert c in ("1", "-1"), c
            coef *= int(c)
            idx.append(int(v.get("idx")))
        key = frozenset(idx)
        assert len(key) == len(idx), "repeated variable in a product"
        poly[key] += coef
    return {k: c for k, c in poly.items() if c != 0}, len(root)


def check(n):
    M = Model(OS + f"hadamard_{n}.osil")
    nb = n * n
    assert M.n == nb + 1
    for j in range(nb):
        assert M.vtype[j] == "B" and M.vlb[j] == "0" and M.vub[j] == "1", j
    assert M.vtype[nb] == "C" and M.vlb[nb] == "-INF" and M.vub[nb] == "INF"
    assert M.objsense == "max" and M.objlin == {nb: "1"} and M.objconst == "0"
    assert M.m == 1 and M.clb[0] == "0" and M.cub[0] == "INF" and M.cconst[0] == "0"
    assert M.lin[0] == {nb: "-1"} and not any(M.quad.values()) and set(M.nl) == {0}
    poly, nterms = extract_poly(M.nl[0])
    assert all(max(k) < nb for k in poly)
    det = leibniz(n)
    assert poly == det, "polynomial differs from det(B)"
    return M, nterms


if __name__ == "__main__":
    for n in [int(a) for a in sys.argv[1:]] or [6, 7, 8, 9]:
        M, nterms = check(n)
        print(f"hadamard_{n}: {nterms} product terms; polynomial == det(B) (row-major, {len(leibniz(n))} Leibniz terms) VERIFIED")
