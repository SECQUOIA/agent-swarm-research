"""Independent reproduction of the reviewer checks for the spatial B&B lower bound.

Reproduces the "Numerical checks performed for this review" list in
notes/review-spatial-bb-lower-bound.md (reviewer scripts /tmp/review/check.py
and /tmp/review/check2.py, never archived) for the result note
results/spatial-bb-exponential-lower-bound.md.  Written 2026-09-25 from the
review text only.  It does not reuse the committed checker's code; the
committed check_lower_bound.py is imported only at the end, as an object under
test, to compare its Remark 7 leaf counts with the counts built here.

Chord-LP bounds are computed two ways: exactly, with a rational greedy solver
for "minimize a separable linear function subject to one equality and box
bounds", and with HiGHS through scipy (as the reviewer did).

Run: /home/sgusev/miniconda3/envs/minlp-notes/bin/python review_lower_bound_repro.py
"""
from fractions import Fraction as Fr
from itertools import product
from math import comb, isclose, log2, sqrt

import numpy as np
from scipy.optimize import linprog

HALF = Fr(1, 2)
QUARTER = Fr(1, 4)


def chord_terms(box):
    """Chord of x(1-x) on [a,b] is a*b + (1-a-b)*x; return (constant, slopes)."""
    return sum(a * b for a, b in box), [1 - a - b for a, b in box]


def lb_exact(box, total):
    """Exact min of the chord sum over box ∩ {sum x = total}; None if empty."""
    lo = sum(a for a, _ in box)
    hi = sum(b for _, b in box)
    if not lo <= total <= hi:
        return None
    const, slopes = chord_terms(box)
    value = const + sum(s * a for s, (a, _) in zip(slopes, box))
    rest = total - lo
    for s, (a, b) in sorted(zip(slopes, box), key=lambda t: t[0]):
        step = min(rest, b - a)
        value += s * step
        rest -= step
        if rest == 0:
            break
    return value


def lb_highs(box, total):
    box = [(float(a), float(b)) for a, b in box]
    const, slopes = chord_terms(box)
    res = linprog(slopes, A_eq=np.ones((1, len(box))), b_eq=[float(total)],
                  bounds=box, method="highs")
    if res.status == 2:
        return None
    assert res.status == 0, res.message
    return res.fun + const


def pruned_both(box, total, target):
    """Check a box is target-pruned by the exact and the HiGHS chord LP."""
    ex = lb_exact(box, total)
    hs = lb_highs(box, total)
    assert (ex is None) == (hs is None), (box, ex, hs)
    ok = ex is None or ex >= target
    assert ok == (hs is None or hs >= float(target) - 1e-9), (box, ex, hs)
    return ok, ex


def lemma1(nmax=7):
    """Enumerate vertices of F: n-1 coordinates at 0/1, one determined by the equality."""
    total_vertices = 0
    for n in range(2, nmax + 1):
        for k in range(1, n):
            S = k + HALF
            verts = set()
            for free in range(n):
                for bits in product((0, 1), repeat=n - 1):
                    v = S - sum(bits)
                    if 0 <= v <= 1:
                        x = list(bits[:free]) + [v] + list(bits[free:])
                        verts.add(tuple(x))
            values = {sum(xi * (1 - xi) for xi in x) for x in verts}
            assert values == {QUARTER}, (n, k, values)
            assert len(verts) == n * comb(n - 1, k), (n, k, len(verts))
            total_vertices += len(verts)
    print(f"[Lemma 1] n=2..{nmax}, all k: every vertex of F has value exactly 1/4 "
          f"({total_vertices} vertices); OPT = 1/4")


def exact_psd(M):
    """Exact PSD test by symmetric Gaussian elimination on a rational matrix."""
    A = [row[:] for row in M]
    n = len(A)
    for p in range(n):
        if A[p][p] < 0:
            return False
        if A[p][p] == 0:
            if any(A[p][j] != 0 for j in range(p, n)):
                return False
            continue
        for i in range(p + 1, n):
            f = A[i][p] / A[p][p]
            for j in range(p, n):
                A[i][j] -= f * A[p][j]
    return True


def remark3(nmax=12):
    fail_constraint, fail_justification, hold_justification = [], [], []
    for n in range(2, nmax + 1):
        for k in range(1, n):
            c = Fr(2 * k + 1, 2 * n)
            d = (k - HALF) * c / (n - 1)
            assert d == (k - HALF) * (k + HALF) / (n * (n - 1))
            assert 0 <= d <= c
            # 1/n <= d  iff  n <= k^2 + 3/4 (review, Issue 3)
            assert (Fr(1, n) <= d) == (n <= k * k + Fr(3, 4))
            if not d >= 2 * c - 1:
                fail_constraint.append((n, k))
            if n >= 2 * k:
                (hold_justification if Fr(1, n) <= d else fail_justification).append((n, k))
            # PSD of [[1, x^T], [x, X]] and the RLT row sums, exactly
            x = [c] * n
            X = [[c if i == j else d for j in range(n)] for i in range(n)]
            assert all(sum(X[i]) == (k + HALF) * x[i] for i in range(n))
            M = [[Fr(1)] + x] + [[x[i]] + X[i] for i in range(n)]
            assert exact_psd(M), (n, k)
    ge2k_fail = [p for p in fail_constraint if p[0] >= 2 * p[1]]
    stated = [(n, k) for n in range(2, nmax + 1) for k in range(1, n)
              if n >= 2 * k + 1 or (n == 2 * k and k >= 2)]
    assert not set(stated) & set(fail_constraint)
    print(f"[Remark 3] exact, 1<=k<n<={nmax}: 0<=d<=c, RLT row sums and PSD hold for all "
          f"{nmax * (nmax - 1) // 2} pairs")
    print(f"  d >= 2c-1 fails at {len(fail_constraint)} pairs, exactly k=n-1: "
          f"{fail_constraint == [(n, n - 1) for n in range(2, nmax + 1)]}; "
          f"among n>=2k it fails only at {ge2k_fail}")
    print(f"  justification 1/n<=d among n>=2k: fails at {len(fail_justification)} pairs, "
          f"holds at {len(hold_justification)} pairs {hold_justification}")
    return fail_justification, hold_justification


def cover_counterexample():
    for n in (2, 3, 4):
        k = n - 1
        # feasibility-based tightening at the root: x_i >= k+1/2-(n-1) = 1/2
        assert k + HALF - (n - 1) == HALF
        box = [(HALF, Fr(1))] * n
        ok, ex = pruned_both(box, k + HALF, QUARTER)
        assert ok and ex == QUARTER, (n, ex)
        assert isclose(lb_highs(box, k + HALF), 0.25, abs_tol=1e-9)
        # max form with m=1, z=0 asks for n^(1/4-eps) > 1 boxes for eps < 1/4
    print("[cover counterexample] k=n-1, n=2,3,4: LB([1/2,1]^n) = 1/4 exactly and by HiGHS; "
          "max form requires n^(1/4-eps) > 1 boxes (e.g. eps=0: "
          + ", ".join(f"{n}^(1/4)={n ** 0.25:.3f}" for n in (2, 3, 4)) + ")")


def remark7_tree(n, k):
    """Branch each coordinate at 1/2 in order; prune when c=k+1 highs or d=n-k lows."""
    nodes, leaves = 0, []
    stack = [()]
    while stack:
        prefix = stack.pop()
        nodes += 1
        c = sum(1 for side in prefix if side)
        d = len(prefix) - c
        if c >= k + 1 or d >= n - k:
            leaves.append(prefix)
            continue
        assert len(prefix) < n, "unpruned node at depth n"
        stack.append(prefix + (0,))
        stack.append(prefix + (1,))
    return nodes, leaves


def remark7_leaf_count(n, k):
    """Leaf count by path counting: first reach c=k+1 (last step high) or d=n-k (last low)."""
    high = sum(comb(k + j, j) for j in range(n - k))      # c=k+1 reached with d=j<n-k
    low = sum(comb(n - k - 1 + j, j) for j in range(k + 1))  # d=n-k reached with c=j<=k
    return high + low


def check_remark7_trees():
    configs = [(n, k) for n in range(2, 9) for k in (1, 2) if k < n] + [(50, 1), (40, 39)]
    total = 0
    for n, k in configs:
        nodes, leaves = remark7_tree(n, k)
        assert len(leaves) == remark7_leaf_count(n, k)
        if k == 1:
            assert nodes == n * n + n - 1 and len(leaves) == n * (n + 1) // 2, (n, nodes)
        for prefix in leaves:
            box = [((HALF, Fr(1)) if s else (Fr(0), HALF)) for s in prefix]
            box += [(Fr(0), Fr(1))] * (n - len(prefix))
            ok, _ = pruned_both(box, k + HALF, QUARTER)
            assert ok, (n, k, prefix)
        total += len(leaves)
    print(f"[Remark 7 trees] all leaves pruned at eps=0 (exact + HiGHS), {total} leaves over "
          f"{len(configs)} (n,k): n=2..8 with k=1,2; (50,1): {remark7_tree(50, 1)[0]} nodes, "
          f"{len(remark7_tree(50, 1)[1])} leaves; (40,39): {len(remark7_tree(40, 39)[1])} leaves")


def bound_log2(n, k, m, z, eps, form):
    h = m * (0.5 - 2 * eps)
    terms = [h / 2 * log2(n / (n - k)), h / 2 * log2(n / (n - z))]
    return (max if form == "max" else min)(terms)


def leaf_counts_vs_forms():
    eps = 0.01
    print(f"[k=1 tree vs Theorem 1 forms] eps={eps}, m+z=n-1 with m,z = floor/ceil((n-1)/2)")
    for n in (50, 100, 200, 400):
        leaves = n * (n + 1) // 2
        rows = []
        for m in sorted({(n - 1) // 2, n - 1 - (n - 1) // 2}):
            z = n - 1 - m
            mx, mn = 2 ** bound_log2(n, 1, m, z, eps, "max"), 2 ** bound_log2(n, 1, m, z, eps, "min")
            assert mn <= leaves
            rows.append(f"(m,z)=({m},{z}) max={mx:.3g} min={mn:.4g}")
        # the largest min bound over all m still stays below the leaf count
        best = max(2 ** bound_log2(n, 1, m, n - 1 - m, eps, "min") for m in range(1, n))
        assert best <= leaves
        print(f"  n={n}: leaves={leaves}; " + "; ".join(rows) + f"; max_m min-form={best:.4g}")


def min_form_vs_tree_k_third():
    print("[k=n/3] Theorem 1 min form (maximised over m, z=n-k-m) vs leaf counts")
    for n in (30, 60, 90):
        k = n // 3
        leaves7 = remark7_leaf_count(n, k)
        leaves2 = 2 ** (n + 1) - 1  # Proposition 2 tree
        parts = []
        for eps in (0.01, 0.125):
            best = max(bound_log2(n, k, m, n - k - m, eps, "min") for m in range(1, n - k + 1))
            assert best <= log2(leaves7) and best <= log2(leaves2)
            parts.append(f"eps={eps}: log2 bound={best:.2f}")
        print(f"  n={n}, k={k}: log2 Remark7 leaves={log2(leaves7):.2f}, "
              f"log2 Prop2 leaves={log2(leaves2):.2f}; " + "; ".join(parts))


def proposition2(nmax=7, eps=0.125):
    alpha = (1 - sqrt(1 - 4 * (0.25 - eps))) / 2
    target = 0.25 - eps
    lo, hi, mid = (0.0, alpha), (1 - alpha, 1.0), (alpha, 1 - alpha)
    middle_min, total_lp = None, 0
    for n in range(2, nmax + 1):
        # build the tree: at coordinate i split at alpha, then split the upper child at 1-alpha
        nodes, leaves = 1, []
        frontier = [()]
        for i in range(n):
            nxt = []
            for pre in frontier:
                nodes += 4  # low, upper, middle, high
                leaves.append((pre + (mid,), True))
                nxt += [pre + (lo,), pre + (hi,)]
            frontier = nxt
        leaves += [(pre, False) for pre in frontier]
        assert nodes == 2 ** (n + 2) - 3 and len(leaves) == 2 ** (n + 1) - 1, (n, nodes)
        for k in range(1, n):
            for pre, is_middle in leaves:
                box = list(pre) + [(0.0, 1.0)] * (n - len(pre))
                val = lb_highs(box, k + 0.5)
                total_lp += 1
                assert val is None or val >= target - 1e-9, (n, k, pre, val)
                if is_middle and val is not None:
                    middle_min = val if middle_min is None else min(middle_min, val)
    assert abs(middle_min - target) < 1e-9
    print(f"[Proposition 2] n=2..{nmax}, all k, eps={eps}: nodes 2^(n+2)-3 and leaves "
          f"2^(n+1)-1 confirmed; {total_lp} leaf LPs pruned; smallest middle-child LB "
          f"= {middle_min!r} (1/4-eps = {target})")


def committed_object_under_test():
    import check_lower_bound as author
    pairs = [(6, 1), (8, 1), (10, 2), (12, 3), (20, 1), (9, 3), (12, 4)]
    for n, k in pairs:
        assert len(author.remark7_tree_leaves(n, k)) == remark7_leaf_count(n, k), (n, k)
    print(f"[committed check_lower_bound.remark7_tree_leaves] leaf counts agree on {pairs}")


def main():
    # exact PSD test sanity: rejects indefinite and zero-pivot-indefinite matrices
    assert not exact_psd([[Fr(1), Fr(2)], [Fr(2), Fr(1)]]) and not exact_psd([[Fr(0), Fr(1)], [Fr(1), Fr(0)]])
    assert exact_psd([[Fr(1), Fr(1)], [Fr(1), Fr(1)]])
    lemma1()
    remark3()
    cover_counterexample()
    check_remark7_trees()
    leaf_counts_vs_forms()
    min_form_vs_tree_k_third()
    proposition2()
    committed_object_under_test()
    print("all reproduction checks completed")


if __name__ == "__main__":
    main()
