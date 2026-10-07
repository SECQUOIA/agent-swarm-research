"""coreB checks for Section 5 / Appendix A (W3 revision).

1. Constants (60-digit mpmath):
   - per-coordinate radius constant of Lemma lem:states (< 7.3 < 8);
   - common-mesh radius constant of Lemma lem:commonmesh (G4) (< 4.2);
   - phi(m) = 3/4 + 8 ln(5/4 + 4 sqrt(2m)) <= 10 ceil(log2(m+2)) for all m >= 1,
     and <= 10 log2(m+2) for m >= 2 (fails at m = 1 without the ceiling);
   - psi(m) = 3/4 + 8 ln(5/4 + 3 sqrt(m)) <= 8 ceil(log2(m+2)) for all m >= 1,
     and <= 8 log2(m+2) for m >= 2;
   - 8.4/sqrt(8) < 3;
   - exact algebra of Lemma lem:inv / lem:commonmesh: 8/15, 9/16, 17/15.
2. Brute-force simulation of TRIAL with the common mesh h_j = s 2^{-j}
   (exact Fractions, full grid enumeration), on planted mixed-integer box QPs
   with an exactly certified point-growth constant g (H + 2M - 2gI PSD).
   At every stage it asserts (G1)-(G5) of Lemma lem:commonmesh with
   kappa = max{1, L/g} and theta = 2^{-mu}, 8 kappa theta^2 <= 1.
3. Rescaled expanding-box chain: L = 4^{m+1}, G = 20 delta^2 on the sigma_1 ray,
   and G >= (1/8)||(sigma,z)||^2 at random points.
"""
import itertools
import math
import random
import sys
from fractions import Fraction as Fr

import mpmath as mp

mp.mp.dps = 60


def constants():
    s1715 = mp.sqrt(mp.mpf(17) / 15)
    per = 3 + 2 * s1715 + (2 + s1715) / mp.sqrt(2)
    com = (2 + s1715) * (1 + 1 / mp.sqrt(8))
    print("per-coordinate radius constant", mp.nstr(per, 8))
    print("common-mesh radius constant   ", mp.nstr(com, 8))
    assert per < 7.3 and com < 4.2
    assert 8.4 / mp.sqrt(8) < 3
    phi = lambda m: mp.mpf(3) / 4 + 8 * mp.log(mp.mpf(5) / 4 + 4 * mp.sqrt(2 * m))
    psi = lambda m: mp.mpf(3) / 4 + 8 * mp.log(mp.mpf(5) / 4 + 3 * mp.sqrt(m))
    print("phi(1), phi(2)", mp.nstr(phi(1), 6), mp.nstr(phi(2), 6),
          " 10 log2 3 =", mp.nstr(10 * mp.log(3, 2), 6))
    print("psi(1), psi(2)", mp.nstr(psi(1), 6), mp.nstr(psi(2), 6))
    assert phi(1) > 10 * mp.log(3, 2)  # the claim without ceiling fails at m=1
    for m in list(range(1, 5000)) + [10**k for k in range(4, 16)]:
        c = math.ceil(math.log2(m + 2))
        assert phi(m) <= 10 * c and psi(m) <= 8 * c, m
        if m >= 2:
            assert phi(m) <= 10 * mp.log(m + 2, 2) and psi(m) <= 8 * mp.log(m + 2, 2), m
    # derivative comparisons for m >= 2 (closed forms)
    for m in [2, 3, 5, 10, 100, 10**6]:
        m = mp.mpf(m)
        dphi = 8 * (4 * mp.sqrt(2) / (2 * mp.sqrt(m))) / (mp.mpf(5) / 4 + 4 * mp.sqrt(2 * m))
        dpsi = 8 * (3 / (2 * mp.sqrt(m))) / (mp.mpf(5) / 4 + 3 * mp.sqrt(m))
        assert dphi <= 4 / m and dpsi <= 4 / m
        assert 10 / ((m + 2) * mp.log(2)) >= mp.mpf(7.2) / m
        assert 8 / ((m + 2) * mp.log(2)) >= mp.mpf(5.7) / m
    # exact algebra (kappa=1 normalisation, a = L n h^2, g = L/kappa worst case)
    Y = Fr(16, 15) * (Fr(1, 4) + Fr(1, 4))          # (15/16) g Y <= a/4 + g k a /4 ... /g k a
    assert Y == Fr(8, 15)
    D = Fr(1, 4) + Fr(1, 16) * (Y + 4)
    assert D <= Fr(9, 16) and Fr(1, 4) + Fr(1, 16) * 5 == Fr(9, 16)
    Z = Fr(16, 15) * (Fr(13, 16) + Fr(4, 16))
    assert Z == Fr(17, 15)
    assert Fr(8, 15) * 4 <= 4  # c bound at next stage: (8/15) k a_{j-1} = (32/15) k a_j
    print("constants ok")


def ldl_psd(A):
    A = [row[:] for row in A]
    n = len(A)
    for k in range(n):
        if A[k][k] < 0:
            return False
        if A[k][k] == 0:
            if any(A[k][j] != 0 for j in range(k + 1, n)):
                return False
            continue
        for i in range(k + 1, n):
            f = A[i][k] / A[k][k]
            for j in range(k + 1, n):
                A[i][j] -= f * A[k][j]
    return True


def make_instance(n, magmax):
    while True:
        types = [random.choice("CZ") for _ in range(n)]
        lo, hi = [], []
        for t in types:
            if t == "Z":
                a = random.randint(-6, 0)
                lo.append(Fr(a)); hi.append(Fr(a + random.randint(3, 12)))
            else:
                a = Fr(random.randint(-8, 0), random.choice([1, 2, 3]))
                lo.append(a); hi.append(a + Fr(random.randint(2, 15), random.choice([1, 2, 4])))
        xs = []
        for i in range(n):
            kind = random.choice(["lo", "hi", "in", "in"])
            if kind == "lo":
                xs.append(lo[i])
            elif kind == "hi":
                xs.append(hi[i])
            elif types[i] == "Z":
                xs.append(Fr(random.randint(int(lo[i]), int(hi[i]))))
            else:
                xs.append(lo[i] + (hi[i] - lo[i]) * Fr(random.randint(1, 9), 10))
        H = [[Fr(0)] * n for _ in range(n)]
        for i in range(n):
            H[i][i] = Fr(random.randint(-2, 12), random.choice([1, 2]))
            for j in range(i):
                H[i][j] = H[j][i] = Fr(random.randint(-8, 8), random.choice([1, 2]))
        zeta, mu = [Fr(0)] * n, [Fr(0)] * n
        for i in range(n):
            if lo[i] < xs[i] < hi[i]:
                continue
            mag = Fr(random.randint(1, magmax), random.choice([1, 2, 4]))
            zeta[i] = mag if xs[i] == lo[i] else -mag
            mu[i] = mag / (hi[i] - lo[i])
        L = [max(H[i][i], Fr(0)) for i in range(n)]
        if not any(L):
            continue
        g = None
        for e in range(0, 16):
            gg = Fr(1, 2**e)
            A = [[H[i][j] + (2 * mu[i] - 2 * gg if i == j else 0) for j in range(n)] for i in range(n)]
            if ldl_psd(A):
                g = gg
                break
        if g is None:
            continue
        b = [zeta[i] - sum(H[i][j] * xs[j] for j in range(n)) for i in range(n)]
        return dict(n=n, types=types, lo=lo, hi=hi, xs=xs, H=H, b=b, L=L, g=g)


def F(inst, x):
    H, b, n = inst["H"], inst["b"], inst["n"]
    return (sum(Fr(1, 2) * H[i][j] * x[i] * x[j] for i in range(n) for j in range(n))
            + sum(b[i] * x[i] for i in range(n)))


def graded(lo, hi, c, h, th, integer):
    def sig(t):
        return max(Fr(1), Fr(math.floor(h + th * t))) if integer else h + th * t
    nodes = {c}
    for side, R in ((1, hi - c), (-1, c - lo)):
        t = Fr(0)
        while t < R:
            t = min(t + sig(t), R)
            nodes.add(c + side * t)
    return sorted(nodes)


def eff(a, b, integer):
    return Fr(0) if (integer and b - a == 1) else b - a


def sq(d):
    return sum(x * x for x in d)


def run_common(inst, mu_exp, stages=11):
    n, types, L = inst["n"], inst["types"], inst["L"]
    lo, hi, xs, g = inst["lo"], inst["hi"], inst["xs"], inst["g"]
    P = [i for i in range(n) if L[i] > 0]
    Lmax = max(L)
    th = Fr(1, 2**mu_exp)
    kap = max(Fr(1), Lmax / g)
    assert 8 * kap * th * th <= 1
    OPT = F(inst, xs)
    s = max(hi[i] - lo[i] for i in range(n))
    cap = 8 * 2**mu_exp * math.ceil(math.log2(n + 2))
    box = [(lo[i], hi[i]) for i in range(n)]
    c = list(lo)
    U = F(inst, lo)
    maxnodes = 0
    for j in range(stages):
        h = s / 2**j
        G = [graded(box[i][0], box[i][1], c[i], h, th, types[i] == "Z") if i in P
             else [lo[i], hi[i]] for i in range(n)]
        maxnodes = max(maxnodes, max(len(gr) for gr in G))
        assert all(len(gr) <= cap for gr in G), "(G5) cap"
        w = []
        for i in range(n):
            gr, wi = G[i], {}
            for k, v in enumerate(gr):
                cand = [Fr(0)]
                if k > 0:
                    cand.append(eff(gr[k - 1], v, types[i] == "Z"))
                if k + 1 < len(gr):
                    cand.append(eff(v, gr[k + 1], types[i] == "Z"))
                wi[v] = max(cand)
            w.append(wi)
        Qv, Fv, Dv = {}, {}, {}
        for y in itertools.product(*G):
            fy = F(inst, y)
            dy = sum(L[i] * w[i][y[i]] ** 2 / 8 for i in range(n))
            Fv[y], Dv[y], Qv[y] = fy, dy, fy - dy
        beta = min(Qv.values())
        y = min(k for k in Qv if Qv[k] == beta)
        m = [{v: min(Qv[k] for k in Qv if k[i] == v) for v in G[i]} for i in range(n)]
        U = min(U, Fv[y])
        a = Lmax * n * h * h
        assert all(box[i][0] <= xs[i] <= box[i][1] for i in range(n)) and beta <= OPT
        cx = sq([c[i] - xs[i] for i in range(n)])
        for z in Qv:  # (G1)
            assert Dv[z] <= a / 4 + Lmax * th * th / 2 * (sq([z[i] - xs[i] for i in range(n)]) + cx), "(G1)"
        assert cx <= 4 * kap * n * h * h, "(G2) center"
        assert sq([y[i] - xs[i] for i in range(n)]) <= Fr(8, 15) * kap * n * h * h, "(G2) y"
        for z, qz in Qv.items():
            if qz <= U:
                assert sq([z[i] - xs[i] for i in range(n)]) <= Fr(17, 15) * kap * n * h * h, "(G2) z"
        assert U - OPT <= Fv[y] - OPT <= Fv[y] - beta == Dv[y] <= Fr(9, 16) * a, "(G3)"
        if U - beta <= Fr(1, 10**7):
            return ("success", j, maxnodes, cap)
        newbox = list(box)
        rho = math.sqrt(float(n * kap))
        for i in P:
            gr = G[i]
            kept = [(p, q) for p, q in zip(gr[:-1], gr[1:]) if min(m[i][p], m[i][q]) <= U]
            nb = (min(k[0] for k in kept), max(k[1] for k in kept))
            R = Fr(4.2 * rho) * h + (1 if types[i] == "Z" else 0)
            assert y[i] - R <= nb[0] and nb[1] <= y[i] + R, "(G4)"
            # sharper: constant 4.148
            newbox[i] = nb
        box = newbox
        c = list(y)
    return ("stages", j, maxnodes, cap)


def chain_check():
    for m in range(2, 9):
        # variables sigma_1..sigma_m, z_1..z_m; xi_t = 2^t sigma_t
        def G(sig, z):
            xi = [Fr(0)] + [Fr(2) ** t * sig[t - 1] for t in range(1, m + 1)]
            val = xi[m] ** 2
            for t in range(1, m + 1):
                r = xi[t] - 2 * xi[t - 1] - z[t - 1]
                val += r * r + Fr(1, 8) * z[t - 1] * (1 - z[t - 1])
            return val
        # curvatures: G is quadratic; second difference along each coordinate
        curv = []
        zero = [Fr(0)] * m
        for t in range(m):
            e = [Fr(0)] * m; e[t] = Fr(1)
            curv.append(G(e, zero) + G([-x for x in e], zero) - 2 * G(zero, zero))
        for t in range(m):
            e = [Fr(0)] * m; e[t] = Fr(1)
            curv.append(G(zero, e) + G(zero, [-x for x in e]) - 2 * G(zero, zero))
        assert max(curv) == Fr(4) ** (m + 1), (m, curv)
        d = Fr(1, 3)
        assert G([d] + [Fr(0)] * (m - 1), zero) == 20 * d * d
        for _ in range(300):
            sig = [Fr(random.randint(0, 2**t - 1), 2**t) * Fr(random.randint(0, 100), 100) for t in range(1, m + 1)]
            z = [Fr(random.randint(0, 100), 100) for _ in range(m)]
            assert G(sig, z) >= Fr(1, 8) * (sq(sig) + sq(z))
    print("rescaled chain ok (L = 4^{m+1}, ray 20 delta^2, growth 1/8), m = 2..8")


if __name__ == "__main__":
    random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    magmax = int(sys.argv[3]) if len(sys.argv) > 3 else 40
    constants()
    chain_check()
    done = 0
    while done < count:
        n = random.choice([2, 2, 3])
        inst = make_instance(n, magmax)
        kap = max(Fr(1), max(inst["L"]) / inst["g"])
        if kap > 400:
            continue
        mu = 2
        while 8 * kap * Fr(1, 4**mu) > 1:
            mu += 1
        res = run_common(inst, mu)
        done += 1
        print(done, n, inst["types"], "kappa<=", kap, "mu=", mu, res, flush=True)
    print("common-mesh invariants (G1)-(G5) held on", done, "instances")
