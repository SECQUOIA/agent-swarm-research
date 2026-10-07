#!/usr/bin/env python3
"""Round-2 math lens: independent checks that complement R9_math_checks.py.

  K  Appendix C.1 (lower bounds for Theorem 3.2(ii)): the polynomials p of the
     separated and nested cases satisfy dist(y,A)^2 - p >= kA and dist(y,C)^2 + p >= kC
     on R with kA + kC = delta^2/2 (exact, random rational instances).
  L  Theorem 3.2(ii) by LP: the minimum over pairs of grid measures with equal first two
     moments of int dist_A^2 + int dist_C^2 is 0 (interleaving or touching) or delta^2/2.
  M  Theorem 3.3 by LP: for random finite disjoint A, C, measures on A and on C with equal
     moments 1..kappa exist iff alt(A, C) >= kappa + 1.
  N  Section 8.5, Part C4: independent computation of bound (ii) as the Lagrangian dual
     max_mu sum_i min_y (phi_i(y) + mu y) - mu c (exact rationals, rigorous bracket),
     comparison with experiments/v4/c4-references.json and the claims "equal on 13 of 20"
     and "at most 6.5e-4 below"; feasibility and value of the archived optimal y; and an
     independent exact branch and bound (Lagrangian bounds, branching on arc choices) that
     certifies the archived optimum to 1e-20.
  O  Section 8.5: whole-row cuts give sum_i min phi_i; count instances where this is below
     the SCIP default root bound of Table 12 (claim: half).

Run: OMP_NUM_THREADS=1 .venv/bin/python R9_math_indep.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import itertools  # noqa: E402
import json  # noqa: E402
import random  # noqa: E402
from fractions import Fraction as Q  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
from scipy.optimize import linprog  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
V4 = ROOT / "experiments" / "v4"
RESULTS = []


def check(name, cond, info=""):
    RESULTS.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + (f"  [{info}]" if info else ""))


def dist2(y, S):
    return min((y - s) ** 2 for s in S)


def quad_min(a2, a1, a0):
    """min over R of a2 y^2 + a1 y + a0 (a2 > 0), exact."""
    assert a2 > 0
    return a0 - a1 * a1 / (4 * a2)


# ---------------------------------------------------------------- K
def part_K():
    rng = random.Random(7)
    ok_sep = ok_nest = True
    for _ in range(400):
        pts = sorted(rng.sample(range(0, 97), 4))
        pts = [Q(p, 32) for p in pts]
        # separated: A = two smallest, C = two largest
        A, C = pts[:2], pts[2:]
        a0, c0 = max(A), min(C)
        d = c0 - a0
        t0 = (a0 + c0) / 2
        # p(y) = d (y - t0) = d y - d t0
        kA = min(quad_min(Q(1), -2 * s - d, s * s + d * t0) for s in A)
        kC = min(quad_min(Q(1), -2 * t + d, t * t - d * t0) for t in C)
        ok_sep &= kA >= d * d / 4 and kC >= d * d / 4 and kA + kC >= d * d / 2
        # nested: A = outer pair, C = inner pair
        A, C = [pts[0], pts[3]], [pts[1], pts[2]]
        delta = min(abs(s - t) for s in A for t in C)
        t0 = (min(C) + max(C)) / 2
        h = (max(C) - min(C)) / 2
        rho = delta + h
        g = (rho - h) / (rho + h)
        # p(y) = -g (y - t0)^2
        kA = min(quad_min(1 + g, -2 * s - 2 * g * t0, s * s + g * t0 * t0) for s in A)
        kC = min(quad_min(1 - g, -2 * t + 2 * g * t0, t * t - g * t0 * t0) for t in C)
        ok_nest &= kA + kC >= delta * delta / 2
    check("K: App. C.1 separated-case polynomial gives kA + kC >= delta^2/2 (400 exact cases)", ok_sep)
    check("K: App. C.1 nested-case polynomial gives kA + kC >= delta^2/2 (400 exact cases)", ok_nest)


# ---------------------------------------------------------------- L
def glued_lp(A, C, grid):
    """min sum_g muA_g dA(g) + muC_g dC(g) s.t. both probability, equal 1st, 2nd moments."""
    G = len(grid)
    cost = [float(dist2(g, A)) for g in grid] + [float(dist2(g, C)) for g in grid]
    Aeq = []
    beq = []
    Aeq.append([1.0] * G + [0.0] * G)
    beq.append(1.0)
    Aeq.append([0.0] * G + [1.0] * G)
    beq.append(1.0)
    for k in (1, 2):
        Aeq.append([float(g ** k) for g in grid] + [-float(g ** k) for g in grid])
        beq.append(0.0)
    r = linprog(cost, A_eq=np.array(Aeq), b_eq=np.array(beq), bounds=(0, None), method="highs")
    return r.fun


def part_L():
    rng = random.Random(11)
    grid = [Q(k, 128) for k in range(129)]  # contains all midpoints of 1/64 points
    worst = 0.0
    counts = {"interleave": 0, "touch": 0, "separated": 0, "nested": 0}
    for _ in range(120):
        vals = [Q(k, 64) for k in rng.sample(range(65), 4)]
        kind = rng.choice(["random", "touch"])
        if kind == "touch":
            A = (vals[0], vals[1])
            C = (vals[1], vals[2])
        else:
            A, C = (vals[0], vals[1]), (vals[2], vals[3])
        delta = min(abs(s - t) for s in A for t in C)
        if set(A) & set(C):
            label, expected = "touch", 0
        else:
            srt = sorted([(v, "A") for v in A] + [(v, "C") for v in C])
            labs = [l for _, l in srt]
            inter = all(labs[i] != labs[i + 1] for i in range(3))
            if inter:
                label, expected = "interleave", 0
            elif labs in (["A", "A", "C", "C"], ["C", "C", "A", "A"]):
                label, expected = "separated", delta * delta / 2
            else:
                label, expected = "nested", delta * delta / 2
        counts[label] += 1
        v = glued_lp(A, C, grid)
        worst = max(worst, abs(v - float(expected)))
    check("L: Theorem 3.2(ii) glued minimum = 0 or delta^2/2 (LP on 1/128 grid, 120 cases)",
          worst < 1e-9, f"max |LP - claim| = {worst:.1e}; {counts}")


# ---------------------------------------------------------------- M
def alt(A, C):
    pts = sorted([(a, 0) for a in A] + [(c, 1) for c in C])
    runs = 1
    for (_, l1), (_, l2) in zip(pts, pts[1:]):
        runs += l1 != l2
    return runs - 1


def moments_match(A, C, kappa):
    nA, nC = len(A), len(C)
    Aeq = [[1.0] * nA + [0.0] * nC, [0.0] * nA + [1.0] * nC]
    beq = [1.0, 1.0]
    for k in range(1, kappa + 1):
        Aeq.append([float(a) ** k for a in A] + [-float(c) ** k for c in C])
        beq.append(0.0)
    r = linprog(np.zeros(nA + nC), A_eq=np.array(Aeq), b_eq=np.array(beq), bounds=(0, None),
                method="highs")
    return r.status == 0


def part_M():
    rng = random.Random(5)
    bad = 0
    tested = 0
    for _ in range(300):
        size = rng.randint(2, 7)
        pts = [Q(k, 8) for k in rng.sample(range(0, 25), size)]
        labels = [rng.randint(0, 1) for _ in pts]
        A = [p for p, l in zip(pts, labels) if l == 0]
        C = [p for p, l in zip(pts, labels) if l == 1]
        if not A or not C:
            continue
        r = alt(A, C)
        for kappa in range(1, 6):
            tested += 1
            if moments_match(A, C, kappa) != (r >= kappa + 1):
                bad += 1
    check("M: Theorem 3.3 criterion alt >= kappa+1 (LP, random finite sets)", bad == 0,
          f"{tested} (A,C,kappa) cases, {bad} mismatches")


# ---------------------------------------------------------------- N
def load_mech():
    sys.path.insert(0, str(V4))
    import mechanism  # noqa: E402
    return mechanism


def arcs_of(A, C):
    return [((s + t) / 2, (s - t) ** 2 / 2) for s in A for t in C]


def arc_value(m, e, mu):
    y = min(max(m - mu / 4, Q(0)), Q(1))
    return 2 * (y - m) ** 2 + e + mu * y, y


def g_copy(arcs, mu):
    vals = [arc_value(m, e, mu) for m, e in arcs]
    best = min(v for v, _ in vals)
    ys = [y for v, y in vals if v == best]
    return best, min(ys), max(ys)


def h_and_super(arcs_all, cap, mu):
    tot, lo, hi = Q(0), Q(0), Q(0)
    for arcs in arcs_all:
        v, a, b = g_copy(arcs, mu)
        tot += v
        lo += a
        hi += b
    return tot - mu * cap, lo - cap, hi - cap


def lagrangian_bracket(arcs_all, cap, steps=110):
    """Rigorous [lower, upper] bracket for max_{mu>=0} h(mu); h concave."""
    lo, hi = Q(0), Q(4)
    hl, gl_lo, gl_hi = h_and_super(arcs_all, cap, lo)
    if gl_hi <= 0:  # maximum at mu = 0
        return hl, hl, lo
    for _ in range(steps):
        mid = (lo + hi) / 2
        hm, glo, ghi = h_and_super(arcs_all, cap, mid)
        if glo > 0:
            lo = mid
        elif ghi < 0:
            hi = mid
        else:
            return hm, hm, mid
    # candidate rational kinks (interior-interior arc swaps) inside the bracket
    best, best_mu = None, None
    cands = {lo, hi}
    for arcs in arcs_all:
        for (m1, e1), (m2, e2) in itertools.combinations(arcs, 2):
            if m1 != m2:
                mu = (e2 - e1) / (m1 - m2)
                if lo <= mu <= hi:
                    cands.add(mu)
    for mu in cands:
        v = h_and_super(arcs_all, cap, mu)[0]
        if best is None or v > best:
            best, best_mu = v, mu
    hl, gl, _ = h_and_super(arcs_all, cap, lo)   # gl > 0 is a supergradient at lo
    hh, _, gh = h_and_super(arcs_all, cap, hi)   # gh < 0 is a supergradient at hi
    # tangent lines hl + gl (mu - lo) and hh + gh (mu - hi); intersection bounds the max
    mu_x = (hh - hl + gl * lo - gh * hi) / (gl - gh)
    upper = hl + gl * (mu_x - lo)
    return best, upper, best_mu


def phi_val(arcs, y):
    return min(2 * (y - m) ** 2 + e for m, e in arcs)


def bnb_certify(arcs_all, cap, opt, tol=Q(1, 10 ** 20), max_nodes=2000):
    """Certify min sum phi_i(y_i) s.t. sum y <= cap, y in [0,1] is >= opt - tol."""
    stack = [tuple(tuple(a) for a in arcs_all)]
    nodes = 0
    while stack:
        node = stack.pop()
        nodes += 1
        if nodes > max_nodes:
            return False, nodes
        lower, _, mu = lagrangian_bracket(list(node), cap, steps=90)
        if lower >= opt - tol:
            continue
        # branch on a copy whose arc choice is ambiguous near mu (largest y-spread)
        eps = Q(1, 10 ** 12)
        branch, spread = None, Q(-1)
        for i, arcs in enumerate(node):
            if len(arcs) == 1:
                continue
            ys = sorted(arc_value(m, e, mu)[1] for m, e in arcs
                        if arc_value(m, e, mu)[0] <= g_copy(arcs, mu)[0] + eps)
            sp_ = ys[-1] - ys[0] if ys else Q(0)
            if len(ys) > 1 and sp_ > spread:
                branch, spread = i, sp_
        if branch is None:
            # no ambiguity: pick any copy with >1 arcs
            cand = [i for i, a in enumerate(node) if len(a) > 1]
            if not cand:
                return False, nodes  # convex problem with lower < opt: opt not a lower bound
            branch = cand[0]
        for arc in node[branch]:
            child = list(node)
            child[branch] = (arc,)
            stack.append(tuple(child))
    return True, nodes


def part_N(mech):
    refs = json.loads((V4 / "c4-references.json").read_text())["instances"]
    eq = 0
    max_gap = Q(0)
    agree = True
    feas = True
    certified = 0
    total_nodes = 0
    table = []
    for r in refs:
        n, seed = r["n"], r["seed"]
        cap = Q(r["coupling"]["c"])
        opt = Q(r["optimum_exact"])
        arcs_all = [arcs_of(A, C) for A, C in mech.draw_triples(n, seed)]
        lower, upper, _ = lagrangian_bracket(arcs_all, cap)
        if lower > opt:
            agree = False
        # equality: opt lies in the rigorous bracket [lower, upper] of max h, and h at the
        # archived exact multiplier equals opt
        mu_arch = Q(r["multiplier_exact"])
        h_arch = h_and_super(arcs_all, cap, mu_arch)[0]
        is_eq = lower <= opt <= upper and h_arch == opt
        eq += is_eq
        gap_hi = opt - lower
        max_gap = max(max_gap, gap_hi)
        ref_val = Q(r["bound_ii"]["lower_exact"])
        agree &= abs(ref_val - lower) <= upper - lower + Q(1, 10 ** 25)
        # archived optimal y
        ys = [Q(v) for v in r["y_exact"]]
        feas &= sum(ys) <= cap and all(0 <= y <= 1 for y in ys)
        feas &= sum(phi_val(a, y) for a, y in zip(arcs_all, ys)) == opt
        ok, nodes = bnb_certify(arcs_all, cap, opt)
        certified += ok
        total_nodes += nodes
        table.append((n, seed, float(opt - lower), float(upper - lower), ok, nodes))
        if cap < 1:
            agree = False
    for row in table:
        print("     n=%-3d s=%d  opt-(ii)=%.4g  bracket=%.1e  bnb=%s nodes=%d" % row)
    check("N: independent bound (ii) agrees with c4-references.json", agree)
    check("N: (ii) = optimum on 13 of 20 instances", eq == 13, f"{eq} of {len(refs)}")
    check("N: max optimum-(ii) <= 6.5e-4", max_gap <= Q(65, 100000), f"{float(max_gap):.4g}")
    check("N: archived optimal y feasible and attains optimum (exact)", feas)
    check("N: independent exact B&B certifies archived optimum to 1e-20", certified == len(refs),
          f"{certified} of {len(refs)}, {total_nodes} nodes")
    check("N: c >= 1 so proven bounds do not shrink the block box", all(Q(r["coupling"]["c"]) >= 1 for r in refs))


# ---------------------------------------------------------------- O
TABLE12_C4_BASE = {  # (n, seed): SCIP default root bound, Table 12 Part C4 (as typeset)
    (10, 5): -0.02472, (10, 6): 0.2214, (10, 7): -0.0234, (10, 8): -0.1117, (10, 9): -0.009054,
    (20, 5): 0.09005, (20, 6): -0.0242, (20, 7): 0.01972, (20, 8): 0.2429, (20, 9): 0.1314,
    (40, 5): 0.0889, (40, 6): -0.001551, (40, 7): 0.187, (40, 8): 0.205, (40, 9): -0.2923,
    (80, 5): 0.7687, (80, 6): 0.2171, (80, 7): -0.1272, (80, 8): -0.1146, (80, 9): 0.6497,
}


def part_O(mech):
    below = 0
    for (n, seed), zb in TABLE12_C4_BASE.items():
        s = sum(min(e for _, e in arcs_of(A, C)) for A, C in mech.draw_triples(n, seed))
        below += float(s) < zb
    check("O: sum_i min phi_i below SCIP's C4 root bound on half of the instances", below == 10,
          f"{below} of 20")


if __name__ == "__main__":
    part_K()
    part_L()
    part_M()
    mech = load_mech()
    part_N(mech)
    part_O(mech)
    bad = [n for n, ok in RESULTS if not ok]
    print(f"\n{len(RESULTS) - len(bad)} of {len(RESULTS)} checks passed")
    if bad:
        print("FAILED:", bad)
        sys.exit(1)
