"""R9 referee lens: does the 'representation, not strength' message extend to stars?

Section 3.4 proves (via Burer-Natarajan-Willemsen, Thm 1, n <= 3) that on a
three-variable path the dense Shor relaxation with McCormick (RLT) inequalities
of all products is exact. The introduction and the conclusions state the
consequence generally ("the advantage of joint blocks over their pairs is one
of representation"). Here we test stars with k = 3 leaves (n = 4 variables),
built from the paper's own family (6): Phi = sum_i Phi_{A_i}(x_i, y) with
omega_i = (a_i2 - a_i1)^2, so the true minimum is min_y sum_i dist(y, A_i)^2.

For each instance we compute
  true  : exact minimum (enumerate nearest-point choices; rational),
  glued : pair hulls (3x3 moment matrix PSD + box RLT, exact for 2-D boxes by
          Anstreicher-Burer 2010) glued on (m_y, s_y),
  dense : moment matrix of (1, y, x_1..x_k) PSD + RLT of ALL pairs and squares
          (includes the McCormick inequalities of the leaf-leaf products).
SDPs are solved in floating point (Clarabel); a gap is reported only when it
exceeds 1e-5, far above solver accuracy. Read-only, single-threaded.
"""
import itertools
import os
import random
from fractions import Fraction

os.environ.setdefault("OMP_NUM_THREADS", "1")
import cvxpy as cp
import numpy as np


def true_min(sets, lo, hi):
    best = None
    for choice in itertools.product(*sets):
        mean = Fraction(sum(choice), len(choice))
        y = min(max(mean, lo), hi)
        val = sum((y - a) ** 2 for a in choice)
        best = val if best is None or val < best else best
    return best


def quad_coeffs(sets):
    """Phi = sum_i (y - a1 - d x_i)^2 + d^2 x_i (1 - x_i), d = a2 - a1.
    Return coefficients of monomials in (y, x_i): const, y, y^2, x_i, y x_i, x_i^2."""
    terms = {"c": 0.0, "y": 0.0, "yy": 0.0}
    leaf = []
    for (a1, a2) in sets:
        a1, a2 = float(a1), float(a2)
        d = a2 - a1
        # (y - a1)^2 - 2 d (y - a1) x + d^2 x^2 + d^2 x - d^2 x^2
        terms["c"] += a1 * a1
        terms["y"] += -2 * a1
        terms["yy"] += 1.0
        leaf.append({"x": 2 * d * a1 + d * d, "yx": -2 * d, "xx": 0.0})
    return terms, leaf


def rlt(M, idx_p, idx_q, lo_p, hi_p, lo_q, hi_q, cons):
    # M[0, p] = v_p, M[p, q] = v_p v_q ; McCormick / RLT for the product v_p v_q
    vp, vq, w = M[0, idx_p], M[0, idx_q], M[idx_p, idx_q]
    cons += [
        w - lo_q * vp - lo_p * vq + lo_p * lo_q >= 0,
        w - hi_q * vp - hi_p * vq + hi_p * hi_q >= 0,
        -w + hi_q * vp + lo_p * vq - lo_p * hi_q >= 0,
        -w + lo_q * vp + hi_p * vq - hi_p * lo_q >= 0,
    ]


def objective(M, terms, leaf, yidx, xidx):
    obj = terms["c"] + terms["y"] * M[0, yidx] + terms["yy"] * M[yidx, yidx]
    for i, c in enumerate(leaf):
        xi = xidx[i]
        obj += c["x"] * M[0, xi] + c["yx"] * M[yidx, xi] + c["xx"] * M[xi, xi]
    return obj


def dense_bound(sets, lo, hi):
    k = len(sets)
    n = k + 2
    M = cp.Variable((n, n), symmetric=True)
    cons = [M >> 0, M[0, 0] == 1]
    bounds = [(float(lo), float(hi))] + [(0.0, 1.0)] * k
    for p in range(1, n):
        for q in range(p, n):
            rlt(M, p, q, *bounds[p - 1], *bounds[q - 1], cons)
    terms, leaf = quad_coeffs(sets)
    prob = cp.Problem(cp.Minimize(objective(M, terms, leaf, 1, list(range(2, n)))), cons)
    prob.solve(solver=cp.CLARABEL)
    return prob.value


def glued_bound(sets, lo, hi):
    k = len(sets)
    Ms = [cp.Variable((3, 3), symmetric=True) for _ in range(k)]
    cons = []
    for M in Ms:
        cons += [M >> 0, M[0, 0] == 1]
        b = [(float(lo), float(hi)), (0.0, 1.0)]
        for p in range(1, 3):
            for q in range(p, 3):
                rlt(M, p, q, *b[p - 1], *b[q - 1], cons)
    for M in Ms[1:]:
        cons += [M[0, 1] == Ms[0][0, 1], M[1, 1] == Ms[0][1, 1]]
    terms, leaf = quad_coeffs(sets)
    obj = terms["c"] + terms["y"] * Ms[0][0, 1] + terms["yy"] * Ms[0][1, 1]
    for i, c in enumerate(leaf):
        obj += c["x"] * Ms[i][0, 2] + c["yx"] * Ms[i][1, 2] + c["xx"] * Ms[i][2, 2]
    prob = cp.Problem(cp.Minimize(obj), cons)
    prob.solve(solver=cp.CLARABEL)
    return prob.value


def report(name, sets, lo, hi):
    t = true_min(sets, lo, hi)
    g = glued_bound(sets, lo, hi)
    d = dense_bound(sets, lo, hi)
    flag = "GAP" if float(t) - d > 1e-5 else "exact"
    print(f"{name:34s} true={float(t):.6f} ({t})  glued={g:.6f}  dense+allRLT={d:.6f}  -> {flag}")
    return float(t) - d


F = Fraction
print("-- k = 2 (three-variable path; BNW predicts exact) --")
report("Prop 3.1 sets", [(F(1, 4), F(3, 4)), (F(0), F(5, 8))], F(0), F(1))
report("nested A={0,3}, C={1,2}", [(F(0), F(3)), (F(1), F(2))], F(0), F(3))

print("-- k = 3 (star with three leaves, n = 4) --")
report("A={0,1},{1,2},{0,2} on [0,2]", [(F(0), F(1)), (F(1), F(2)), (F(0), F(2))], F(0), F(2))

rng = random.Random(20261003)
gaps = []
n_inst = 60
for s in range(n_inst):
    sets = []
    for _ in range(3):
        a, b = rng.sample(range(0, 17), 2)
        sets.append((F(a, 16), F(b, 16)))
    gaps.append(report(f"random k=3 #{s}", sets, F(0), F(1)))
pos = [g for g in gaps if g > 1e-5]
print(f"\nrandom k=3: {len(pos)} of {n_inst} instances with dense+allRLT bound below the true minimum"
      f" (max gap {max(gaps):.6f})")
