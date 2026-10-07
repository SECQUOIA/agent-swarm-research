"""Second verifier pass for group limits (W3): exact checks of statements
not covered by the other limits-*.py scripts.

1. Prop. lim:prop:messages: part 2 (Psi_m >= (|xi|^2+|z|^2)/8 on the box) at
   random rational points, including points with z binary and rho = 0;
   part 3 (Hessian diagonal 10/4/7/4 and Hess + 1/4 sum_t e_zt e_zt^T PSD).
2. Prop. prop:oraclebarrier: derivative formulas, the factorization
   1-(1-rho)^3-rho = rho(1-rho)(2-rho), d_ii f <= 1 on the ball, set growth
   with g_S = w^2/(6n), and the subcube count M (symbolic + random points).
3. Prop. prop:lbwidth, all graphs on n <= 4 vertices: unique binary
   minimizer, floor decoding for every approximation within 1/2, growth
   1/(2n) of Psi and 1/n of Psi_0 at random rational points, kappa-bar = 2.
4. Padding after Cor. lim:cor:nopolylog: adding t_j^2 on [0,1] keeps L = 4
   and the growth constant g of Prop. lim:prop:unique (g <= 1).
"""
import itertools
import random
from fractions import Fraction as Fr

import sympy as sp

random.seed(31)


def rnd(lo, hi, den=97):
    return lo + (hi - lo) * Fr(random.randint(0, den), den)


# ---------------------------------------------------------------- 1. messages
def psi_m(xi, z):
    m = len(xi)
    val = xi[-1] ** 2
    prev = Fr(0)
    for t in range(m):
        rho = xi[t] - 2 * prev - z[t]
        val += rho ** 2 + Fr(1, 8) * z[t] * (1 - z[t])
        prev = xi[t]
    return val


def check_messages():
    for m in range(2, 8):
        for trial in range(400):
            if trial % 4 == 0:  # exact chains: rho = 0, z binary
                z = [Fr(random.randint(0, 1)) for _ in range(m)]
                xi, prev = [], Fr(0)
                for t in range(m):
                    prev = 2 * prev + z[t]
                    xi.append(prev)
            else:
                xi = [rnd(0, 2 ** (t + 1) - 1) for t in range(m)]
                z = [rnd(0, 1) for _ in range(m)]
                if trial % 4 == 1:  # small perturbations of the origin
                    xi = [x / 1000 for x in xi]
                    z = [w / 1000 for w in z]
            lhs = psi_m(xi, z)
            rhs = Fr(1, 8) * (sum(x * x for x in xi) + sum(w * w for w in z))
            assert lhs >= rhs, (m, xi, z)
        # Hessian (constant): variables xi_1..xi_m, z_1..z_m
        xs = sp.symbols(f"x1:{m+1}")
        zs = sp.symbols(f"z1:{m+1}")
        expr = xs[-1] ** 2
        prev = 0
        for t in range(m):
            expr += (xs[t] - 2 * prev - zs[t]) ** 2 + sp.Rational(1, 8) * zs[t] * (1 - zs[t])
            prev = xs[t]
        H = sp.hessian(expr, list(xs) + list(zs))
        diag = [H[i, i] for i in range(2 * m)]
        assert diag[: m - 1] == [10] * (m - 1) and diag[m - 1] == 4
        assert diag[m:] == [sp.Rational(7, 4)] * m
        Hs = H + sp.diag(*([0] * m + [sp.Rational(1, 4)] * m))
        assert Hs.is_positive_semidefinite is True, m  # exact (rational) test
        # kappa: L = 10, g = 1/8
        assert sp.Rational(10) / sp.Rational(1, 8) == 80
    print("messages: part 2 at random/exact points, part 3 Hessian: PASS")


# ----------------------------------------------------------- 2. oraclebarrier
def check_oraclebarrier():
    w = sp.symbols("w", positive=True)
    for n in (1, 2, 3):
        x = sp.symbols(f"x1:{n+1}")
        c = sp.symbols(f"c1:{n+1}")
        r2 = sum((x[i] - c[i]) ** 2 for i in range(n))
        f = -w ** 2 / 6 * (1 - r2 / w ** 2) ** 3
        z = [(x[i] - c[i]) / w for i in range(n)]
        rho = sum(zi ** 2 for zi in z)
        for i in range(n):
            gi = sp.diff(f, x[i])
            assert sp.simplify(gi - w * z[i] * (1 - rho) ** 2) == 0
            for j in range(n):
                hij = sp.diff(f, x[i], x[j])
                target = (1 if i == j else 0) * (1 - rho) ** 2 - 4 * z[i] * z[j] * (1 - rho)
                assert sp.simplify(hij - target) == 0
    r = sp.symbols("r")
    assert sp.expand(1 - (1 - r) ** 3 - r - r * (1 - r) * (2 - r)) == 0
    # d_ii f = (1-rho)(1-rho-4 z_i^2) <= 1 for rho in [0,1], z_i^2 <= rho
    for _ in range(2000):
        rho_v = rnd(0, 1, 499)
        zi2 = rho_v * rnd(0, 1, 499)
        assert (1 - rho_v) * (1 - rho_v - 4 * zi2) <= 1
        # growth inside: (w^2/6)(1-(1-rho)^3) >= (w^2/6) rho
        assert 1 - (1 - rho_v) ** 3 >= rho_v
    # subcube count: Q < (B-1)^n - 1 with B = 1/(2 sqrt(6 eps)) gives
    # M = floor((Q+1)^(1/n)) + 1 with M^n > Q+1 and M < B (B rational here)
    for n in (1, 2, 3, 4):
        for B in (Fr(3), Fr(7, 2), Fr(10), Fr(41, 3)):
            bound = (B - 1) ** n - 1
            Q = 0
            while Q < bound:
                root = sp.integer_nthroot(Q + 1, n)[0]
                M = root + 1
                assert M ** n > Q + 1 and M < B, (n, B, Q, M)
                Q += 1
    print("oraclebarrier: derivatives, factorization, d_ii f <= 1, subcube count: PASS")


# ------------------------------------------------------------------ 3. lbwidth
def all_graphs(n):
    pairs = list(itertools.combinations(range(n), 2))
    for mask in range(1 << len(pairs)):
        yield [pairs[k] for k in range(len(pairs)) if mask >> k & 1]


def alpha(n, E):
    best = 0
    for S in range(1 << n):
        if all(not (S >> i & 1 and S >> j & 1) for i, j in E):
            best = max(best, bin(S).count("1"))
    return best


def check_lbwidth():
    count = 0
    for n in range(1, 5):
        for E in all_graphs(n):
            def psi0(x):
                phi = -sum(x) + 2 * sum(x[i] * x[j] for i, j in E)
                chi = sum(2 ** i * x[i] for i in range(n))
                return 2 ** n * phi + chi

            def psi(x):
                return psi0(x) + Fr(1, 2 * n) * sum(xi * xi - xi for xi in x)

            verts = list(itertools.product((Fr(0), Fr(1)), repeat=n))
            vals = sorted((psi(v), v) for v in verts)
            assert vals[0][0] < vals[1][0]
            xs, ps = vals[0][1], vals[0][0]
            a = alpha(n, E)
            assert xs != tuple([Fr(0)] * n)
            for d in (Fr(-1, 2), Fr(-1, 3), Fr(0), Fr(1, 3), Fr(1, 2)):
                q = ps + d
                assert (q / 2 ** n).__floor__() == -a, (n, E, d)
            for _ in range(60):
                x = [rnd(0, 1, 37) for _ in range(n)]
                dist2 = sum((x[i] - xs[i]) ** 2 for i in range(n))
                assert psi(x) - ps >= Fr(1, 2 * n) * dist2
                assert psi0(x) - ps >= Fr(1, n) * dist2
                # weighted norm with L_i = 1/n: Psi - Psi* >= (1/2) ||.||_L^2
                assert psi(x) - ps >= Fr(1, 2) * Fr(1, n) * dist2
            count += 1
    print(f"lbwidth: {count} graphs (n<=4) exhaustive: PASS")


# ------------------------------------------------------------------ 4. padding
def check_padding():
    # Prop. lim:prop:unique: L = 4, g = lambda/(m(1+2(m-1)|a|^2)) < 1.
    for m in range(2, 7):
        lam = Fr(1, m * 2 ** (m + 1))
        for a2 in (1, 5, 50):
            g = lam / (m * (1 + 2 * (m - 1) * a2))
            assert g <= 1
            kappa_before = max(Fr(1), Fr(4) / g)
            # padded: extra coordinates t_j with curvature 2 and growth 1
            kappa_after = max(Fr(1), max(Fr(4), Fr(2)) / min(g, Fr(1)))
            assert kappa_before == kappa_after
    print("padding: kappa unchanged: PASS")


if __name__ == "__main__":
    check_messages()
    check_oraclebarrier()
    check_lbwidth()
    check_padding()
    print("ALL PASS")
