"""Referee check (round 2 confirmation) of Lemma A.4 of robust-chains.md, written independently of chains/revision2_*.py.

Exact arithmetic only (Python fractions), except where marked:
  (1) own Sturm sequences: root counts of u' - 1, u' - b, u' - 2b on [-1, 1]; c bracketed by exact bisection.
  (2) the monotonicity steps of the proof of Lemma A.4(2), checked symbolically where possible (sympy) and by
      exact interval arithmetic on the leftover squares (natural interval extension over a uniform subdivision,
      with exact rational endpoints, so no rounding at all).
  (3) the split of Lemma A.4(4), built from scratch as shifts relative to the UNSPLIT base split (different route
      from the note), for n = 4..24; sum of factor minima vs. wall value for n symbolic.
  (4) the wall value at x^(j) against the sum of factor minima (mpmath 50 digits) for n = 4..12.
Usage: python3 d1_wall_exact.py
"""
from fractions import Fraction as Fr
import sympy as sp

UC = [Fr(0), Fr(1022, 1000), Fr(189, 1000), Fr(1774, 1000), Fr(1086, 1000)]
B = Fr(962, 1000)


def peval(cs, t):
    v = Fr(0)
    for cf in reversed(cs):
        v = v * t + cf
    return v


def pder(cs):
    return [i * cs[i] for i in range(1, len(cs))]


def ptrim(cs):
    cs = list(cs)
    while len(cs) > 1 and cs[-1] == 0:
        cs.pop()
    return cs


def pdivmod(a, b):
    a = ptrim(a); b = ptrim(b)
    q = [Fr(0)] * max(1, len(a) - len(b) + 1)
    r = list(a)
    while len(ptrim(r)) >= len(b) and any(r):
        r = ptrim(r)
        d = len(r) - len(b)
        f = r[-1] / b[-1]
        q[d] = f
        for i, cb in enumerate(b):
            r[i + d] -= f * cb
        r = ptrim(r)
        if len(r) < len(b) or (len(r) == 1 and r[0] == 0):
            break
    return q, ptrim(r)


def sturm_count(p, lo, hi):
    """number of distinct real roots of p in (lo, hi] (p squarefree, p(lo), p(hi) != 0 checked by caller)."""
    seq = [ptrim(p), ptrim(pder(p))]
    while len(seq[-1]) > 1 or seq[-1][0] != 0:
        _, r = pdivmod(seq[-2], seq[-1])
        r = [-v for v in r]
        if len(r) == 1 and r[0] == 0:
            break
        seq.append(r)

    def changes(x):
        vals = [peval(s, x) for s in seq]
        vals = [v for v in vals if v != 0]
        return sum(1 for i in range(len(vals) - 1) if (vals[i] > 0) != (vals[i + 1] > 0))
    return changes(lo) - changes(hi)


def u(t):
    return peval(UC, t)


du = pder(UC)


def main():
    one = Fr(1)
    for name, k in (("u' - 1", one), ("u' - b", B), ("u' - 2b", 2 * B)):
        p = list(du); p[0] -= k
        print(f"(1) {name}: values at -1, 0, 1: {peval(p, -one)}, {peval(p, Fr(0))}, {peval(p, one)}; "
              f"Sturm root count in (-1, 1]: {sturm_count(p, -one, one)}")
    # exact minimum of u' on [-1,1]: u'' is quadratic; check with sympy closed form
    t = sp.symbols("t")
    us = sum(sp.Rational(c.numerator, c.denominator) * t**i for i, c in enumerate(UC))
    d2 = sp.diff(us, t, 2)
    crit = [r for r in sp.solve(d2, t) if r.is_real and -1 <= r <= 1]
    vals = [sp.nsimplify(sp.diff(us, t).subs(t, r)) for r in crit] + [sp.diff(us, t).subs(t, -1), sp.diff(us, t).subs(t, 1)]
    print("    closed-form critical points of u' (roots of u''):", [sp.N(r, 15) for r in crit],
          "; min u' on [-1,1] =", sp.N(min(vals, key=lambda v: sp.N(v, 40)), 15))
    # c by exact bisection
    p2 = list(du); p2[0] -= 2 * B
    lo, hi = Fr(-1), Fr(1)
    for _ in range(110):
        mid = (lo + hi) / 2
        if peval(p2, mid) < 0:
            lo = mid
        else:
            hi = mid
    print(f"    c in [{float(lo):.17f}, {float(hi):.17f}] (width {float(hi - lo):.1e})")
    cr = hi

    def H(x, y):
        return u(x) + u(y) + B * x * y - B * (x + y)

    def twophi(x, y):
        return u(x) + u(y) + 2 * B * x * y
    Hup = H(Fr(-1), cr)       # >= H(-1, c) since c minimizes H(-1, .) = u(-1) + u(y) - 2by + b
    twomup = twophi(Fr(-1), cr)  # >= 2m since c minimizes 2phi(-1, .) = u(-1) + u(y) - 2by
    print(f"    rational upper bounds: H(-1,c) <= {float(Hup):.15f}, 2m <= {float(twomup):.15f}; "
          f"H(-1,c) - 2m - b (should be ~0): {float(Hup - twomup - B):.2e}")

    # (2) symbolic monotonicity steps
    x, y = sp.symbols("x y")
    bs = sp.Rational(481, 500)
    Hs = us.subs(t, x) + us.subs(t, y) + bs * x * y - bs * (x + y)
    Ps = us.subs(t, x) + us.subs(t, y) + 2 * bs * x * y
    print("(2) d_y H =", sp.expand(sp.diff(Hs, y)), "; = u'(y) + b(x - 1):",
          sp.expand(sp.diff(Hs, y) - (sp.diff(us, t).subs(t, y) + bs * (x - 1))) == 0)
    print("    d_y (2phi) - (u'(y) + 2bx) == 0:", sp.expand(sp.diff(Ps, y) - (sp.diff(us, t).subs(t, y) + 2 * bs * x)) == 0)
    print("    H(x,-1) - [u(x) - 2bx + u(-1) + b] == 0:",
          sp.expand(Hs.subs(y, -1) - (us.subs(t, x) - 2 * bs * x + us.subs(t, -1) + bs)) == 0)
    print("    2phi(x,-1) - [u(x) - 2bx + u(-1)] == 0:",
          sp.expand(Ps.subs(y, -1) - (us.subs(t, x) - 2 * bs * x + us.subs(t, -1))) == 0)
    print(f"    thresholds: 1 - 1/b = {1 - 1 / B} = {float(1 - 1 / B):.6f}; -1/(2b) = {-1 / (2 * B)} = {float(-1 / (2 * B)):.6f}; "
          f"c >= both: {cr > 1 - 1 / B and cr > -1 / (2 * B)}")

    # exact rational interval arithmetic on the leftover squares
    def imul(a, b_):
        ps = [a[0] * b_[0], a[0] * b_[1], a[1] * b_[0], a[1] * b_[1]]
        return (min(ps), max(ps))

    def iadd(a, b_):
        return (a[0] + b_[0], a[1] + b_[1])

    def ipow(a, k):
        lo_, hi_ = a
        if k % 2 == 1 or lo_ >= 0:
            return (lo_ ** k, hi_ ** k) if lo_ >= 0 or k % 2 == 1 else (hi_ ** k, lo_ ** k)
        if hi_ <= 0:
            return (hi_ ** k, lo_ ** k)
        return (Fr(0), max(lo_ ** k, hi_ ** k))

    def iu(a):
        # Horner-free monomial form with exact powers (tighter than naive products for even powers)
        v = (Fr(0), Fr(0))
        for i, cf in enumerate(UC):
            if cf == 0:
                continue
            pw = ipow(a, i) if i > 0 else (Fr(1), Fr(1))
            term = (cf * pw[0], cf * pw[1]) if cf >= 0 else (cf * pw[1], cf * pw[0])
            v = iadd(v, term)
        return v

    def lower_bound(fun, lo_, hi_, K):
        best = None
        for i in range(K):
            X = (lo_ + (hi_ - lo_) * Fr(i, K), lo_ + (hi_ - lo_) * Fr(i + 1, K))
            for j in range(K):
                Y = (lo_ + (hi_ - lo_) * Fr(j, K), lo_ + (hi_ - lo_) * Fr(j + 1, K))
                v = fun(X, Y)[0]
                best = v if best is None or v < best else best
        return best

    def iH(X, Y):
        xy = imul(X, Y)
        s = iadd(X, Y)
        return iadd(iadd(iu(X), iu(Y)), iadd((B * xy[0], B * xy[1]), (-B * s[1], -B * s[0])))

    def iP(X, Y):
        xy = imul(X, Y)
        return iadd(iadd(iu(X), iu(Y)), (2 * B * xy[0], 2 * B * xy[1]))
    for K in (16, 48):
        lbH = lower_bound(iH, Fr(-1), 1 - 1 / B, K)
        lbP = lower_bound(iP, Fr(-1), -1 / (2 * B), K)
        print(f"(2) exact interval bound, {K}x{K} boxes: H >= {float(lbH):.6f} on [-1, 1-1/b]^2 "
              f"(margin over H(-1,c): {float(lbH - Hup):.4f} > 0: {lbH > Hup}); "
              f"2phi >= {float(lbP):.6f} on [-1, -1/(2b)]^2 (margin over 2m: {float(lbP - twomup):.4f} > 0: {lbP > twomup})")

    # (3) split from shifts relative to the UNSPLIT base split, for n = 4..24 even
    ok = True
    for n in range(4, 25, 2):
        X = sp.symbols(f"z1:{n + 1}")
        U = lambda z: us.subs(t, z)
        # unsplit base: factor e (1-based, joins z_e, z_{e+1}) = u(z_e) + b z_e z_{e+1}; last factor also gets u(z_n)
        base = [U(X[e - 1]) + bs * X[e - 1] * X[e] for e in range(1, n)]
        base[-1] += U(X[-1])
        # target factors of Lemma A.4(4)
        tgt = []
        for e in range(1, n):
            xa, xb = X[e - 1], X[e]
            if e == 1:
                tgt.append(U(xa) + bs * xb * (xa + 1))
            elif e == n - 1:
                tgt.append(U(xb) + bs * xa * (xb + 1))
            elif e % 2 == 0:
                tgt.append(U(xa) + U(xb) + bs * xa * xb - bs * (xa + xb))
            else:
                tgt.append(bs * (xa + 1) * (xb + 1) - bs)
        # the differences tgt_e - base_e must be of the form r_{e+1}(z_{e+1}) - r_e(z_e) with univariate r_i in span{1, t, u}
        # solve recursively: r_1 = 0, r_{e+1}(z_{e+1}) = tgt_e - base_e + r_e(z_e); check univariate in z_{e+1}, and r_n = 0
        r = {1: sp.Integer(0)}
        for e in range(1, n):
            nxt = sp.expand(tgt[e - 1] - base[e - 1] + r[e])
            free = nxt.free_symbols - {X[e]}
            if free:
                ok = False
                break
            r[e + 1] = nxt
        ok = ok and sp.expand(r[n]) == 0 and sp.expand(sum(tgt) - sum(base)) == 0
        # each interior shift should lie in span{1, t, u}: r_i(t) - alpha u(t) - beta t - gamma == 0 for some constants
        if n == 8:
            for i in range(2, n):
                al, be, ga = sp.symbols("al be ga")
                expr = sp.expand(r[i].subs(X[i - 1], t) - al * us - be * t - ga)
                sol = sp.solve(sp.Poly(expr, t).all_coeffs(), [al, be, ga], dict=True)
                print(f"    n = 8, shift r_{i} (relative to the unsplit split) = alpha u + beta t + gamma with", sol)
    print(f"(3) the factors of Lemma A.4(4) are a split of f_n relative to the unsplit base (univariate shifts, r_1 = r_n = 0), "
          f"n = 4..24 even: {ok}")
    nn = sp.symbols("n")
    u1, uc, cc = sp.symbols("u1 uc cc")
    m = (u1 + uc) / 2 - bs * cc
    Hmin = u1 + uc - 2 * bs * cc + bs
    tot = 2 * u1 + (nn / 2 - 2) * (-bs) + (nn / 2 - 1) * Hmin
    wall = (nn - 2) * m + (u1 + bs) + u1
    print("    symbolic: sum of minima - wall value =", sp.simplify(tot - wall), "; H(-1,c) - (2m + b) =", sp.simplify(Hmin - 2 * m - bs))

    # (4) wall value at x^(j) vs sum of minima (50 digits)
    import mpmath as mp
    mp.mp.dps = 50
    cnum = mp.findroot(lambda z: sum(mp.mpf(str(float(c_))) * 0 for c_ in [0]) + mp.mpf(1022) / 1000 + 2 * mp.mpf(189) / 1000 * z
                       + 3 * mp.mpf(1774) / 1000 * z**2 + 4 * mp.mpf(1086) / 1000 * z**3 - 2 * mp.mpf(962) / 1000, 0.34)
    um = lambda z: mp.mpf(1022) / 1000 * z + mp.mpf(189) / 1000 * z**2 + mp.mpf(1774) / 1000 * z**3 + mp.mpf(1086) / 1000 * z**4
    bm = mp.mpf(962) / 1000
    mval = (um(-1) + um(cnum)) / 2 - bm * cnum
    Hm = um(-1) + um(cnum) - 2 * bm * cnum + bm
    worst = 0
    for n in range(4, 13, 2):
        for j in range(1, n // 2 + 1):
            xs = [cnum if ((i % 2 == 0 and i < 2 * j) or (i % 2 == 1 and i > 2 * j)) else mp.mpf(-1) for i in range(1, n + 1)]
            fv = sum(um(z) for z in xs) + bm * sum(xs[i] * xs[i + 1] for i in range(n - 1))
            mins = 2 * um(-1) - bm * (n // 2 - 2) + (n // 2 - 1) * Hm
            worst = max(worst, abs(fv - mins))
    print(f"(4) max |f_n(x^(j)) - sum of factor minima| over n = 4..12 even, all j: {mp.nstr(worst, 5)}; m = {mp.nstr(mval, 20)}")


if __name__ == "__main__":
    main()
