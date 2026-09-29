"""Reviewer checks (exact rational arithmetic) for two claims of relaxation-intrinsic-bounds.md.

Part 1. Proposition 5.2(b) says that under (C1) "simple variable branching attains [kappa] up to a
  factor of 2 in nodes".  Family: phi(z) = sum_i (z_i - a)^2 with a = 1/(2n), K = [0,1]^n,
  P = {0,1}^n, eps = 1/(8 n^2) < a^2.  We check exactly:
  - OPT = n a^2 = 1/(4n), attained only at z = 0;
  - (C1) at x° = 0: every wrong fixing z_i = 1 has bound (1-a)^2 >= OPT - eps;
  - kappa_tau(P) = 2: classes {0} and P cap {1.z >= 1}; min of phi over K cap {1.z >= 1} is
    attained at z = (1/n) 1 (KKT verified exactly) with value 1/(4n) = OPT >= tau; the root
    bound 0 < tau gives kappa >= 2;
  - the minimum number of leaves of a variable-branching eps-certificate is n + 1 (nodes 2n + 1),
    by exact DP over (number of variables fixed to 0, number fixed to 1); the node bound depends
    only on these counts.
Part 2. Summary sentence "The class number of a compact linear program is therefore always
  polynomial" versus Proposition 2.1(b).  The compact MILP
      min sum_i s_i  s.t.  s_i >= x_i - 1/2,  s_i >= 1/2 - x_i  (2n rows),  x in Z^n, s in R^n
  has projected relaxation phi(x) = ||x - (1/2) 1||_1, OPT = n/2, and all 2^n points of {0,1}^n
  pairwise midpoint-conflict for eps < 1/2 (midpoint value (n - d)/2).  Explicit 2^n halfspace
  classes H_sigma = {sum_i sigma_i (x_i - 1/2) >= n/2} (sigma in {-1,1}^n) cover Z^n and have
  phi >= OPT, so kappa_tau(Z^n) = 2^n exactly, with 2n constraint rows.
"""
from fractions import Fraction as F
from itertools import product, combinations
from functools import lru_cache


def part1():
    print("== Part 1: (C1) family phi = sum (z_i - 1/(2n))^2 on [0,1]^n ==")
    for n in range(2, 11):
        a = F(1, 2 * n)
        eps = F(1, 8 * n * n)
        OPT = n * a * a
        tau = OPT - eps
        # OPT over {0,1}^n: value = k1 (1-a)^2 + (n-k1) a^2, minimized at k1 = 0 uniquely
        vals = {k1: k1 * (1 - a) ** 2 + (n - k1) * a * a for k1 in range(n + 1)}
        assert min(vals.values()) == OPT and [k for k, v in vals.items() if v == OPT] == [0]
        # (C1): wrong fixing z_i = 1, others free in [0,1]: bound (1-a)^2
        c1 = (1 - a) ** 2 >= OPT - eps
        # class {1.z >= 1}: candidate minimizer z = (1/n) 1; KKT: grad_i = 2(1/n - a) = mu > 0,
        # constraint active, box constraints inactive (0 < 1/n <= 1/2 < 1)
        zc = F(1, n)
        grad = 2 * (zc - a)
        kkt = grad > 0 and n * zc == 1 and 0 < zc < 1
        val_class = n * (zc - a) ** 2
        class_ok = kkt and val_class >= tau
        root_bound = F(0)  # z = a 1 lies in K
        kappa = 2 if (class_ok and OPT >= tau and root_bound < tau) else None

        @lru_cache(maxsize=None)
        def T(n0, n1):
            bound = n0 * a * a + n1 * (1 - a) ** 2  # free variables sit at a
            if bound >= tau:
                return (1, 1)
            if n0 + n1 == n:
                raise RuntimeError("fully fixed node below tau")
            l0, m0 = T(n0 + 1, n1)
            l1, m1 = T(n0, n1 + 1)
            return (l0 + l1, 1 + m0 + m1)
        leaves, nodes = T(0, 0)
        print(f"n={n:2d}: OPT={OPT}, tau={tau}, (C1) holds: {c1}, class {{1.z>=1}} min = {val_class} (KKT ok: {kkt}), "
              f"kappa = {kappa}; min variable tree: leaves={leaves}, nodes={nodes}; nodes/kappa = {F(nodes, kappa)}")


def part2():
    print("== Part 2: compact MILP with phi = ||x - 1/2||_1 (2n rows) ==")
    for n in range(1, 11):
        half = F(1, 2)
        OPT = F(n, 2)
        eps = F(49, 100)
        cube = list(product((0, 1), repeat=n))
        # all pairs conflict: phi(mid) < OPT - eps
        allconf = all(sum(abs(F(p + q, 2) - half) for p, q in zip(u, v)) < OPT - eps
                      for u, v in combinations(cube, 2))
        # explicit halfspace classes: every integer point of [-2, 3]^n lies in some H_sigma, and phi >= OPT
        # on H_sigma because phi(x) >= sum_i sigma_i (x_i - 1/2) >= n/2 (triangle inequality)
        cover = "not checked" if n > 5 else True
        if n <= 5:
            for z in product(range(-2, 4), repeat=n):
                sigma = tuple(1 if zi >= 1 else -1 for zi in z)
                if sum(s * (F(zi) - half) for s, zi in zip(sigma, z)) < OPT:
                    cover = False
        print(f"n={n:2d}: rows=2n={2*n}, clique of size 2^n={2**n} pairwise conflicting: {allconf}; "
              f"2^n halfspace classes cover the integer points of [-2,3]^n: {cover}")


if __name__ == "__main__":
    part1()
    part2()
