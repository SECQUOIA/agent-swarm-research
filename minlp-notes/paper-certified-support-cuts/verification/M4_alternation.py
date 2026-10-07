"""M4: exact checks for the k-moment gluing theorem.

  (G1) divided-difference weights 1/omega'(t_i) annihilate t^0..t^k on k+2
       nodes and strictly alternate in sign;
  (G2) binomial witness: on t_i = i (i = 0..k+1), the even and odd parts of
       Binomial(k+1) weights, each normalized by 2^k, are probability
       measures with equal moments of orders 0..k (and different order k+1);
  (G3) alternation theorem, checked exhaustively on random finite point
       sets: measures on A and C with equal moments 1..k exist iff
       alt(A,C) >= k+1.  'If' by an explicit measure, 'only if' by an
       explicit separating polynomial of degree alt(A,C) <= k;
  (G4) the r-leaf subset-sum construction: D_L is multilinear in the leaves,
       min over leaves equals dist(y,A)^2, and for k = 2^(r+1)-2 the lifted
       point built from the binomial witness has lifted D = 0 while the
       global minimum is 1/2.
Run: .venv/bin/python M4_alternation.py
"""
from fractions import Fraction as F
from math import comb
import itertools
import random
import sympy as sp


def dd_weights(t):
    w = []
    for i, ti in enumerate(t):
        prod = F(1)
        for j, tj in enumerate(t):
            if j != i:
                prod *= ti - tj
        w.append(1 / prod)
    return w


# ---- (G1) ------------------------------------------------------------------
random.seed(7)
for trial in range(300):
    k = random.randint(0, 8)
    t = sorted(set(F(random.randint(-50, 50), random.randint(1, 9)) for _ in range(3 * (k + 2))))[: k + 2]
    if len(t) < k + 2:
        continue
    w = dd_weights(t)
    for j in range(k + 1):
        assert sum(wi * ti**j for wi, ti in zip(w, t)) == 0
    assert sum(wi * ti ** (k + 1) for wi, ti in zip(w, t)) == 1   # leading coeff
    for i in range(k + 2):
        assert (w[i] > 0) == ((k + 1 - i) % 2 == 0)

# ---- (G2) ------------------------------------------------------------------
for k in range(0, 16):
    n = k + 1
    alpha = {i: F(comb(n, i), 2**k) for i in range(0, n + 1) if i % 2 == 0}
    gamma = {i: F(comb(n, i), 2**k) for i in range(0, n + 1) if i % 2 == 1}
    assert sum(alpha.values()) == 1 and sum(gamma.values()) == 1
    for j in range(0, k + 1):
        assert sum(p * i**j for i, p in alpha.items()) == sum(p * i**j for i, p in gamma.items())
    assert sum(p * i ** (k + 1) for i, p in alpha.items()) != sum(p * i ** (k + 1) for i, p in gamma.items())


# ---- (G3) ------------------------------------------------------------------
def alternation_chain(points, label):
    """Greedy maximal alternating chain of the sorted labelled points."""
    pts = sorted(points)
    chain = [pts[0]]
    for t in pts[1:]:
        if label[t] != label[chain[-1]]:
            chain.append(t)
    return chain


def runs(points, label):
    pts = sorted(points)
    out = [[pts[0]]]
    for t in pts[1:]:
        if label[t] == label[out[-1][-1]]:
            out[-1].append(t)
        else:
            out.append([t])
    return out


def separating_poly(points, label):
    """p of degree (#runs - 1) with sign(p) = label on all points."""
    rs = runs(points, label)
    cuts = [(rs[i][-1] + rs[i + 1][0]) / 2 for i in range(len(rs) - 1)]
    s0 = label[rs[0][0]]

    def p(t):
        val = F(s0)
        for rho in cuts:
            val *= (rho - t)
        return val
    return p, len(cuts)


def measures_from_chain(chain, label, k):
    t = chain[: k + 2]
    w = dd_weights(t)
    # orient: positive on A (label +1)
    if (w[0] > 0) != (label[t[0]] == 1):
        w = [-wi for wi in w]
    S = sum(wi for wi in w if wi > 0)
    alpha = {ti: wi / S for ti, wi in zip(t, w) if wi > 0}
    gamma = {ti: -wi / S for ti, wi in zip(t, w) if wi < 0}
    return alpha, gamma


checked = 0
for trial in range(1500):
    N = random.randint(2, 8)
    pts = sorted(set(F(random.randint(-30, 30), random.randint(1, 5)) for _ in range(N)))
    if len(pts) < 2:
        continue
    lab = {t: random.choice((1, -1)) for t in pts}
    if len(set(lab.values())) < 2:
        continue
    A = [t for t in pts if lab[t] == 1]
    C = [t for t in pts if lab[t] == -1]
    chain = alternation_chain(pts, lab)
    alt = len(chain) - 1
    p, deg = separating_poly(pts, lab)
    assert deg == alt
    for k in range(0, len(pts) + 1):
        if alt >= k + 1:
            alpha, gamma = measures_from_chain(chain, lab, k)
            assert all(t in A for t in alpha) and all(t in C for t in gamma)
            assert sum(alpha.values()) == 1 and sum(gamma.values()) == 1
            assert all(v > 0 for v in alpha.values()) and all(v > 0 for v in gamma.values())
            for j in range(1, k + 1):
                assert sum(q * t**j for t, q in alpha.items()) == sum(q * t**j for t, q in gamma.items())
        else:
            # degree alt <= k polynomial strictly separates: no matching measures
            assert all(p(t) > 0 for t in A) and all(p(t) < 0 for t in C)
        checked += 1
    # finite special case |A|+|C| = k+2: alternation <=> fully alternating labels
    k = len(pts) - 2
    fully = all(lab[pts[i]] != lab[pts[i + 1]] for i in range(len(pts) - 1))
    assert (alt >= k + 1) == fully

# ---- (G4) subset-sum leaf construction ---------------------------------------
y = sp.Symbol("y")
for r in (1, 2, 3):
    xs = sp.symbols("x0:%d" % r)
    zs = sp.symbols("z0:%d" % r)
    bj = [2 ** (j + 1) for j in range(r)]
    a0, c0 = 0, 1
    DL = sp.expand((y - a0 - sum(bb * xx for bb, xx in zip(bj, xs))) ** 2
                   + sum(bb**2 * xx * (1 - xx) for bb, xx in zip(bj, xs)))
    DR = sp.expand((y - c0 - sum(bb * zz for bb, zz in zip(bj, zs))) ** 2
                   + sum(bb**2 * zz * (1 - zz) for bb, zz in zip(bj, zs)))
    PL = sp.Poly(DL, *xs)
    assert all(max(m) <= 1 for m in PL.monoms())          # multilinear in leaves
    A = sorted({a0 + sum(bb for bb, e in zip(bj, S) if e) for S in itertools.product((0, 1), repeat=r)})
    C = sorted({c0 + sum(bb for bb, e in zip(bj, S) if e) for S in itertools.product((0, 1), repeat=r)})
    top = 2 ** (r + 1) - 1
    assert A == list(range(0, top, 2)) and C == list(range(1, top + 1, 2))
    # min over the leaf box = min over vertices (multilinear) = dist(y,A)^2
    for yv in [sp.Rational(i, 3) for i in range(-3, 3 * top + 4)]:
        vals = [DL.subs({**{y: yv}, **dict(zip(xs, S))}) for S in itertools.product((0, 1), repeat=r)]
        assert min(vals) == min((yv - s) ** 2 for s in A)
    # global min over y of dist_A^2 + dist_C^2 is 1/2 (delta = 1, midpoints in [0, top])
    assert min(F(1, 2) * (s - t) ** 2 for s in A for t in C) == F(1, 2)
    k = 2 ** (r + 1) - 2
    n = k + 1
    alpha = {i: F(comb(n, i), 2**k) for i in range(0, n + 1) if i % 2 == 0}
    gamma = {i: F(comb(n, i), 2**k) for i in range(0, n + 1) if i % 2 == 1}

    def bits(m):
        return [(m >> j) & 1 for j in range(r)]
    # local measures on the zero sets: left atom (bits(i/2), i), right atom (i, bits((i-1)/2))
    left = [(p_, dict(zip(xs, bits(i // 2))), i) for i, p_ in alpha.items()]
    right = [(p_, dict(zip(zs, bits((i - 1) // 2))), i) for i, p_ in gamma.items()]
    for p_, xv, i in left:
        assert DL.subs({**xv, y: i}) == 0
    for p_, zv, i in right:
        assert DR.subs({**zv, y: i}) == 0
    # shared separator moments 1..k agree
    for j in range(1, k + 1):
        assert sum(p_ * i**j for p_, _, i in left) == sum(p_ * i**j for p_, _, i in right)
    # lifted D = E_left D_L + E_right D_R = 0
    assert sum(p_ * DL.subs({**xv, y: i}) for p_, xv, i in left) == 0
    print("r=%d leaves per side: A=%s C=%s, k=%d shared moments, lifted min 0 < global min 1/2"
          % (r, A, C, k))

print("M4_alternation: all exact checks passed (%d labelled (A,C,k) cases)." % checked)
