"""M-core: scalar constants of Sections 3-5 and Appendix A, and an exhaustive
check of Lemma lem:graded (a),(b),(c) for small rational/integer parameters.
Exact arithmetic (fractions) where the claim is exact; floats with margins
for transcendental constants."""
from fractions import Fraction as Fr
import math, itertools, sys

ok = True
def check(cond, msg):
    global ok
    if not cond:
        ok = False
        print("FAIL:", msg)

# ---- Lemma inv: exact algebra of (iii), (iv), (v) at the extreme k=1/gamma
for kgam in [Fr(1), Fr(3, 2), Fr(10)]:   # k*gamma >= 1
    g = Fr(1); k = kgam / g  # gamma=1 wlog scaling of a
    a = Fr(1)
    # gamma Y <= a/4 + gamma/16 (Y + 4 k a)  ->  Y <= 16/15 (a/(4 gamma) + k a /4)
    Y = Fr(16, 15) * (a / (4 * g) + k * a / 4)
    check(Y <= Fr(8, 15) * k * a, "inv(iii)")
    th2 = 1 / (8 * k)
    D = a / 4 + th2 / 2 * (k * a + 4 * k * a)
    check(D <= Fr(9, 16) * a, "inv(iv)")
    Z = Fr(16, 15) * (Fr(13, 16) * a / g + k * a / 4)
    check(Z <= Fr(17, 15) * k * a, "inv(v)")
# commonmesh: same with a=Lnh^2, L<=kappa g
Y = Fr(16, 15) * (Fr(1, 4) + Fr(1, 4))
check(Y == Fr(8, 15), "G2 Y")
D = Fr(1, 4) + Fr(1, 16) * (Fr(8, 15) + 4)
check(D == Fr(8, 15) and D <= Fr(9, 16), "G3")
Z = Fr(16, 15) * (Fr(13, 16) + Fr(4, 16))
check(Z == Fr(17, 15), "G2 Z")

r = math.sqrt(17 / 15)
c_states = 3 + 2 * r + (2 + r) / math.sqrt(2)
check(c_states < 7.3, "states 7.3: %r" % c_states)
check(2 * (1 + r) < 8, "states integer")
c_g4 = (2 + r) * (1 + 1 / math.sqrt(8))
check(c_g4 < 4.15, "G4 4.15: %r" % c_g4)
check(8.4 / math.sqrt(8) < 3, "G5 8.4/sqrt8")
check(16 / math.sqrt(8) <= 4 * math.sqrt(2) + 1e-12, "states 16/sqrt8")

phi = lambda m: 0.75 + 8 * math.log(1.25 + 4 * math.sqrt(2 * m))
psi = lambda m: 0.75 + 8 * math.log(1.25 + 3 * math.sqrt(m))
print("phi(1)=%.4f phi(2)=%.4f psi(1)=%.4f psi(2)=%.4f" % (phi(1), phi(2), psi(1), psi(2)))
check(phi(1) < 16.3 and phi(2) < 18.6 and psi(1) < 12.4 and psi(2) < 14.4, "phi/psi values")
for m in list(range(1, 5000)) + [10**k for k in range(4, 13)]:
    check(phi(m) <= 10 * math.ceil(math.log2(m + 2)), "phi(%d)" % m)
    check(psi(m) <= 8 * math.ceil(math.log2(m + 2)), "psi(%d)" % m)
    # actual node bound before the 3<=3/(4 theta) step, for theta=1/4 (worst)
    for th in [0.25, 0.125, 2**-6]:
        cnt = 1 + 2 * math.ceil(4 / th * math.log(1.25 + 4 * math.sqrt(2 * m)))
        check(cnt <= 10 / th * math.ceil(math.log2(m + 2)), "K cap m=%d th=%g" % (m, th))
        cnt = 1 + 2 * math.ceil(4 / th * math.log(1.25 + 3 * math.sqrt(m)))
        check(cnt <= 8 / th * math.ceil(math.log2(m + 2)), "G5 cap m=%d th=%g" % (m, th))

# eq:logabsorb
for p in range(1, 40):
    for n in list(range(1, 3000)) + [10**k for k in range(4, 15)]:
        x = math.ceil(math.log2(n + 2))
        if x ** p > 2 * p ** p * (n + 2):
            check(False, "logabsorb p=%d n=%d" % (p, n))
# mu*: 2^mu* <= 6 sqrt(kb), mu* <= 3(1+log2 kb), 8 kb 4^-mu* <= 1
for kb in [1, 1.01, 1.5, 2, 2.0001, 3, 7.9, 8, 8.01, 31.99, 32, 33, 100, 1e4, 1e9]:
    mu = max(2, math.ceil(math.log(8 * kb, 4) - 1e-15))
    check(8 * kb * 4.0 ** (-mu) <= 1 + 1e-12, "mu* grading %g" % kb)
    check(2 ** mu <= 6 * math.sqrt(kb) + 1e-9, "mu* 6sqrt %g" % kb)
    check(mu <= 3 * (1 + math.log2(kb)), "mu* log %g" % kb)
# ln(1+x) >= 23/24 x on [0,1/12]; 72/23 <= 4
for i in range(0, 1001):
    x = i / 12000
    check(math.log1p(x) >= 23 / 24 * x - 1e-15, "ln bound")
check(Fr(72, 23) <= 4, "72/23")

# ---- Lemma graded exhaustive
def graded(lo, hi, c, h, th, integer):
    nodes = {c}
    for sgn, end in [(1, hi - c), (-1, c - lo)]:
        t = Fr(0)
        while t < end:
            step = h + th * t
            if integer:
                step = max(1, math.floor(step))
            t = min(t + step, end)
            nodes.add(c + sgn * t)
    return sorted(nodes)

def eff(a, b, integer):
    return 0 if (integer and b - a == 1) else b - a

cnt = 0
for integer in [True, False]:
    hs = [Fr(1, 4), Fr(1, 2), Fr(1), Fr(3, 2), Fr(2), Fr(5), Fr(8)] if integer else [Fr(1, 8), Fr(1, 3), Fr(1), Fr(5, 2)]
    for th in [Fr(1, 4), Fr(1, 8), Fr(1, 16), Fr(3, 13)]:
        for h in hs:
            for lo, hi in ([(0, w) for w in range(0, 70)] if integer else [(Fr(0), Fr(w, 3)) for w in range(0, 40)]):
                cs = range(lo, hi + 1) if integer else [lo + (hi - lo) * Fr(k, 6) for k in range(7)]
                for c in cs:
                    G = graded(Fr(lo), Fr(hi), Fr(c), h, th, integer)
                    cnt += 1
                    check(G[0] == lo and G[-1] == hi, "span")
                    w = {v: 0 for v in G}
                    for a, b in zip(G, G[1:]):
                        e = eff(a, b, integer)
                        w[a] = max(w[a], e); w[b] = max(w[b], e)
                    for v in G:
                        check(w[v] <= h + th * abs(v - c), "graded(a) %s" % ((lo, hi, c, h, th, integer),))
                    hhat = max(h, 1) if integer else h
                    for R, side in [(hi - c, [v for v in G if v > c]), (c - lo, [v for v in G if v < c])]:
                        if R > 0:
                            bnd = math.ceil(4 / float(th) * math.log(1 + float(th) * float(R) / float(hhat)))
                            check(len(side) <= bnd, "graded(b) %s" % ((lo, hi, c, h, th, integer, len(side), bnd),))
                    if h >= hi - lo:
                        check(len(G) <= 3, "graded(c)")
print("graded grids checked:", cnt)
print("ALL OK" if ok else "SOME FAILURES")
sys.exit(0 if ok else 1)
