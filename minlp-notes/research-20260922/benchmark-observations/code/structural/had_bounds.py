"""Certified dual and primal bounds for hadamard_6..9 (after had_model.py proves obj* = D01(n)).

Dual: with m = n + 1, D01(n) = Dpm(m) / 2^n (bijection between 0/1 matrices of order n and normalized
+-1 matrices of order m), and D01(n) is an integer. Classical bounds on Dpm(m), squared so that all
arithmetic is exact (integers / Fractions):
  Hadamard (all m):            Dpm^2 <= m^m
  Barba (m odd):               Dpm^2 <= (2m-1) (m-1)^(m-1)
  Ehlich-Wojtas (m = 2 mod 4): Dpm^2 <= (2m-2)^2 (m-2)^(m-2)
  Ehlich (m = 3 mod 4):        Dpm^2 <= (m-3)^(m-s) (m-3+4r)^u (m+1+4r)^v [1 - ur/(m-3+4r) - v(r+1)/(m+1+4r)],
                               s from Ehlich's table (m=7: s=5), r = floor(m/s), v = m - rs, u = s - v.
  D01(n) <= floor(sqrt(Dpm^2 / 4^n)) = isqrt(floor(Dpm^2 / 4^n)).
Primal: a 0/1 matrix found by local search; det computed exactly (sympy Bareiss), and the OSiL model
evaluated exactly (Fraction arithmetic) at (B, objvar = det B) with all constraints checked.
Exhaustive check (n = 6): max |det B| over all 0/1 6x6 matrices, independent of Ehlich's theorem.
Usage: python had_bounds.py            (writes certs/hadamard_n.json)
"""
import json
import os
import sys
from fractions import Fraction
from math import isqrt, comb
import itertools

import numpy as np
import sympy

from had_model import check as check_model, perm_sign

HERE = os.path.dirname(os.path.abspath(__file__))


class FracB:
    num = staticmethod(lambda s: Fraction(s) if isinstance(s, str) else s)


def ehlich_s(m):
    return {3: 3, 7: 5}[m]  # table in Ehlich (1964b); only the cases needed here


def pm_bounds_sq(m):
    """Dict name -> exact upper bound (int or Fraction) on Dpm(m)^2."""
    b = {"Hadamard": m ** m}
    if m % 2 == 1:
        b["Barba"] = (2 * m - 1) * (m - 1) ** (m - 1)
    if m % 4 == 2:
        b["Ehlich-Wojtas"] = (2 * m - 2) ** 2 * (m - 2) ** (m - 2)
    if m % 4 == 3:
        s = ehlich_s(m); r = m // s; v = m - r * s; u = s - v
        b["Ehlich"] = (Fraction((m - 3) ** (m - s) * (m - 3 + 4 * r) ** u * (m + 1 + 4 * r) ** v)
                       * (1 - Fraction(u * r, m - 3 + 4 * r) - Fraction(v * (r + 1), m + 1 + 4 * r)))
    return b


def d01_bound(n):
    out = {}
    for name, sq in pm_bounds_sq(n + 1).items():
        q = Fraction(sq) / 4 ** n  # bound on D01(n)^2
        out[name] = {"Dpm_sq": str(sq), "D01_real": float(q) ** 0.5,
                     "D01_int": isqrt(q.numerator // q.denominator)}
    return out


def local_search(n, target, seed=0, iters=200000):
    rng = np.random.default_rng(seed)
    while True:
        B = rng.integers(0, 2, (n, n))
        d = np.linalg.det(B)
        for _ in range(iters):
            i, j = rng.integers(0, n, 2)
            B[i, j] ^= 1
            d2 = np.linalg.det(B)
            if abs(d2) >= abs(d) - 1e-9 or rng.random() < 0.01:
                d = d2
            else:
                B[i, j] ^= 1
            if round(abs(d)) >= target:
                if d < 0:
                    B[[0, 1]] = B[[1, 0]]
                return B


def exact_primal(n, B, M):
    D = int(sympy.Matrix(B.tolist()).det(method="bareiss"))
    x = [Fraction(int(v)) for v in B.flatten()] + [Fraction(D)]
    v = M.check(x, FracB)
    assert v["bound"][0] == 0 and v["row"][0] == 0 and v["int"][0] == 0, v
    obj = M.objective(x, FracB)
    row = M.row_value(0, x, FracB)
    return D, obj, row


def exhaustive6():
    """max |det B| over all 0/1 6x6 B. WLOG (column permutation) row 1 = 1^w 0^(6-w), w = 1..6;
    rows 2..5 range over 4-subsets of the 63 nonzero rows (row order only changes the sign; repeated
    or zero rows give det 0); row 6 is optimized exactly: det is linear in row 6 with cofactor vector c,
    so max over 0/1 rows of |det| = max(sum of positive c_j, -sum of negative c_j). Cofactors are
    exact integer 5x5 Leibniz determinants."""
    n = 6
    rows = np.array([[(k >> (n - 1 - j)) & 1 for j in range(n)] for k in range(1, 2 ** n)], dtype=np.int64)
    perms5 = [(p, perm_sign(p)) for p in itertools.permutations(range(5))]
    quads = np.array(list(itertools.combinations(range(len(rows)), 4)))
    best = 0
    for w in range(1, n + 1):
        r1 = np.array([1] * w + [0] * (n - w), dtype=np.int64)
        for chunk in np.array_split(quads, 20):
            T = np.concatenate([np.broadcast_to(r1, (len(chunk), 1, n)), rows[chunk]], axis=1)  # (M,5,6)
            cof = np.zeros((len(chunk), n), dtype=np.int64)
            for j in range(n):
                S = np.delete(T, j, axis=2)  # (M,5,5)
                dj = np.zeros(len(chunk), dtype=np.int64)
                for p, sg in perms5:
                    prod = S[:, 0, p[0]] * S[:, 1, p[1]] * S[:, 2, p[2]] * S[:, 3, p[3]] * S[:, 4, p[4]]
                    dj += sg * prod
                cof[:, j] = (-1) ** (5 + j) * dj  # cofactor for entry (6, j+1)
            pos = np.where(cof > 0, cof, 0).sum(1); neg = -np.where(cof < 0, cof, 0).sum(1)
            best = max(best, int(pos.max()), int(neg.max()))
    return best


LISTED = {6: (9, 25), 7: (32, 721), 8: (56, "14267.56437"), 9: (144, None)}


def main():
    res = {}
    for n in (6, 7, 8, 9):
        M, _ = check_model(n)
        bnds = d01_bound(n)
        dual = min(v["D01_int"] for v in bnds.values())
        known = {6: 9, 7: 32, 8: 56, 9: 144}[n]
        B = local_search(n, known, seed=n)
        D, obj, row = exact_primal(n, B, M)
        rec = {"instance": f"hadamard_{n}", "n": n, "m_pm": n + 1, "bounds": bnds,
               "certified_dual_int": dual, "primal_matrix_rowmajor": B.flatten().tolist(),
               "primal_det_exact": D, "primal_objective_exact": str(obj), "row_e1_activity": str(row),
               "closed": D == dual}
        if n == 6:
            rec["exhaustive_max_abs_det"] = exhaustive6()
        json.dump(rec, open(os.path.join(HERE, "certs", f"hadamard_{n}.json"), "w"), indent=1)
        res[n] = rec
        print(f"hadamard_{n}: bounds " + ", ".join(f"{k} {v['D01_real']:.4f}->{v['D01_int']}" for k, v in bnds.items())
              + f" | dual {dual} primal {D} closed={D == dual}"
              + (f" | exhaustive max|det| {rec['exhaustive_max_abs_det']}" if n == 6 else ""), flush=True)
    return res


if __name__ == "__main__":
    main()
