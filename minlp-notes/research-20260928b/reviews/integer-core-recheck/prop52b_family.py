"""Recheck of the corrected Proposition 5.2(b) family, exact arithmetic.

phi(z) = sum_i (z_i - a)^2,  a = 1/(2n),  K = [0,1]^n,  P = {0,1}^n,  eps = 1/(8 n^2).

- OPT, uniqueness of the optimum, (C1) with x = 0 (exact node bounds).
- kappa = 2: the two classes are admissible (exact minimum over the hull, which for
  {1.z >= 1} cap {0,1}^n is the polytope [0,1]^n cap {1.z >= 1}), and P itself is not
  admissible.  For n = 2, 3, 4 also by exact subset DP over all partitions of P.
- Minimum variable-branching certificates: exact DP over fixings (symmetric DP by
  counts for n <= 12; full DP over {free,0,1}^n states for n <= 6 as a cross-check);
  reports the minimum number of leaves and of nodes.
- The ratio nodes/kappa = (2n+1)/2 against the note's "factor about n".
"""
import functools
import itertools
from fractions import Fraction as Fr

from exact import bad_masks, admissible_table, min_cover, box_min, hull_min


def setup(n):
    a = Fr(1, 2 * n)
    OPT = n * a * a
    eps = Fr(1, 8 * n * n)
    return a, OPT, eps, OPT - eps


def node_bound(n, a, s0, s1):
    # free coordinates sit at a in (0,1)
    return s0 * a * a + s1 * (1 - a) ** 2


def sym_dp(n, a, tau):
    @functools.lru_cache(maxsize=None)
    def f(s0, s1):
        if node_bound(n, a, s0, s1) >= tau:
            return 1
        if s0 + s1 == n:
            return None  # an unprunable leaf: impossible in a certificate
        return f(s0 + 1, s1) + f(s0, s1 + 1)
    return f(0, 0)


def full_dp(n, a, tau):
    A = [[Fr(int(i == j)) for j in range(n)] for i in range(n)]
    y = [a] * n

    @functools.lru_cache(maxsize=None)
    def bound(state):
        lo = [0 if v == -1 else v for v in state]
        hi = [1 if v == -1 else v for v in state]
        return box_min(A, y, lo, hi)

    @functools.lru_cache(maxsize=None)
    def f(state):
        if bound(state) >= tau:
            return 1
        best = None
        for i, v in enumerate(state):
            if v == -1:
                c = f(state[:i] + (0,) + state[i + 1:]) + f(state[:i] + (1,) + state[i + 1:])
                best = c if best is None else min(best, c)
        return best
    return f((-1,) * n)


def main():
    print("Proposition 5.2(b) family: phi = sum (z_i - 1/(2n))^2 on [0,1]^n, eps = 1/(8n^2)")
    for n in range(2, 13):
        a, OPT, eps, tau = setup(n)
        pts = list(itertools.product((0, 1), repeat=n)) if n <= 10 else None
        if pts:
            vals = sorted(sum((Fr(zi) - a) ** 2 for zi in z) for z in pts)
            uniq = vals[0] == OPT and vals[1] > OPT
        else:
            uniq = 'n/a'
        # (C1) with x = 0: r(box cap {x_i >= 1}) = (1-a)^2 >= UB - eps = tau (UB = OPT)
        c1 = node_bound(n, a, 0, 1) >= tau
        # class {0}: phi(0) = OPT >= tau; class {1.z >= 1}: min over [0,1]^n cap {1.z >= 1}
        # is attained at z = (1/n)1 (projection of a1, inside the box); KKT exact:
        z = [Fr(1, n)] * n
        grad = [2 * (zi - a) for zi in z]  # = 2(1/n - a) 1 = mu * 1 with mu > 0
        mu = grad[0]
        kkt = all(g == mu for g in grad) and mu > 0 and sum(z) == 1 and all(0 <= zi <= 1 for zi in z)
        m1 = sum((zi - a) ** 2 for zi in z)
        adm2 = m1 >= tau and OPT >= tau
        root = n * 0  # phi(a1) = 0 < tau, a1 in conv P
        kappa_ge2 = root < tau
        # leaves: s0 fixings to 0 alone never prune unless s0 = n
        prune_s0 = [s0 for s0 in range(n + 1) if node_bound(n, a, s0, 0) >= tau]
        L = sym_dp(n, a, tau)
        line = (f"   n={n:2d}: OPT={OPT} unique={uniq}; (C1) {c1}; class {{1.z>=1}} min = {m1} (KKT {kkt}) >= tau: {adm2}; "
                f"P not admissible: {kappa_ge2}; s0-only prunable iff s0 in {prune_s0}; "
                f"min leaves {L} (n+1={n + 1}), nodes {2 * L - 1} (2n+1={2 * n + 1}); nodes/kappa = {Fr(2 * L - 1, 2)}")
        if n <= 6:
            Lf = full_dp(n, a, tau)
            line += f"; full DP leaves {Lf}"
        if n <= 4:
            A = [[Fr(int(i == j)) for j in range(n)] for i in range(n)]
            y = [a] * n
            P = [tuple(map(Fr, p)) for p in pts]
            ok = admissible_table(len(P), bad_masks(A, y, P, tau))
            f = min_cover(len(P), ok)
            line += f"; exact kappa by subset DP = {f[-1]}"
        print(line)
    # the split tree {1.z <= 0} v {1.z >= 1} is a 3-node certificate (kappa + 1 nodes)
    for n in (3, 6, 10):
        a, OPT, eps, tau = setup(n)
        A = [[Fr(int(i == j)) for j in range(n)] for i in range(n)]
        # child {1.z <= 0} cap [0,1]^n = {0}: bound OPT; child {1.z >= 1}: bound 1/(4n) = OPT
        print(f"   split tree n={n}: child bounds {OPT} and {n * (Fr(1, n) - a) ** 2} vs tau {tau}: 3 nodes")


if __name__ == "__main__":
    main()
