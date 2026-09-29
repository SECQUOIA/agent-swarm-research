"""Recheck of Theorem 1.7(b),(c) and Lemma 1.7a (hemispace chain), exact arithmetic.

Part A  The first review's caterpillar counterexample; the chain on it (all orders).
Part B  Random open-E instances (phi = ||Ax - y||^2 on R^d, d = 2, 3): exact kappa,
        every minimum partition (capped) and every ordering (capped).  For each:
          - gradient halfspaces G_j = {g_j.(x - xh_j) >= 0} (Theorem 1.7(c)(iii)):
            I_j in G_j and exact min_{G_j} phi >= tau;
          - the chain N_0 = R^d, N_j = {g_i.x < c_i, i <= j}: covering condition of
            Definition 1.1 at EVERY internal node, for every P-point;
          - Theorem 1.7(c)(i): every node set S replaced by conv(S cap P): covering at
            every internal node (exact point-in-hull) and exact leaf bounds;
          - for contrast, the old caterpillar on the same (partition, ordering).
Part C  A non-open E where no closed (or open) halfspace can serve as a leaf, so a
        genuine hemispace is needed; hemispaces built by the recursion of Lemma 1.7a,
        convexity of G and of its complement tested, chain checked, and (c)(i) checked.
"""
import itertools
import random
import sys
from fractions import Fraction as Fr

from exact import (F, dot, phi, hull_min, bad_masks, admissible_table, min_cover,
                   all_min_partitions, halfspace_min, grad)

I2 = [[Fr(1), Fr(0)], [Fr(0), Fr(1)]]


def in_hull_slow(p, S):
    """exact: p in conv(S)  <=>  min ||x - p||^2 over conv(S) is 0"""
    d = len(p)
    Id = [[Fr(int(i == j)) for j in range(d)] for i in range(d)]
    return hull_min(Id, list(p), [list(s) for s in S])[0] == 0


def _cross3(u, v):
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def in_hull(p, S):
    """exact point-in-convex-hull.  2-D: orientation tests on the hull; 3-D, full
    dimensional S: all planes through three points of S that support S; otherwise the
    slow exact quadratic test."""
    p = tuple(p)
    S = [tuple(s) for s in S]
    if p in S:
        return True
    if len(S) == 1:
        return False
    d = len(p)
    if d == 2:
        H = convex_hull(S)
        if len(H) >= 3:
            for i in range(len(H)):
                a, b = H[i], H[(i + 1) % len(H)]
                if (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]) < 0:
                    return False
            return True
        return in_hull_slow(p, S)
    if d == 3:
        sub = lambda u, v: tuple(a - b for a, b in zip(u, v))
        full = False
        cons = []
        for a, b, c in itertools.combinations(S, 3):
            nrm = _cross3(sub(b, a), sub(c, a))
            if nrm == (0, 0, 0):
                continue
            vals = [dot(nrm, sub(s, a)) for s in S]
            if any(v != 0 for v in vals):
                full = True
            if all(v >= 0 for v in vals):
                cons.append((nrm, a, 1))
            elif all(v <= 0 for v in vals):
                cons.append((nrm, a, -1))
        if full:
            return all(sg * dot(nrm, sub(p, a)) >= 0 for nrm, a, sg in cons)
        return in_hull_slow(p, S)
    return in_hull_slow(p, S)


# ------------------------------------------------------------------ chain checks
def gradient_halfspaces(A, y, P, parts, tau, kappa):
    """per class: (g, c) with G = {g.x >= c}; checks I in G and min_G phi >= tau"""
    Gs, ok = [], True
    for mask in parts:
        I = [P[i] for i in range(len(P)) if mask >> i & 1]
        val, xh = hull_min(A, y, I)
        g = grad(A, y, xh)
        if all(v == 0 for v in g):
            ok &= kappa == 1
            Gs.append(None)
            continue
        c = dot(g, xh)
        ok &= all(dot(g, q) >= c for q in I)
        ok &= halfspace_min(A, y, g, c) >= tau
        Gs.append((g, c))
    return Gs, ok


def chain_covering_ok(P, Gs, order):
    """Definition 1.1 covering at every internal node of the chain with leaves
    G_{order[0]}, ..., and internal nodes N_j = complement of the first j leaves."""
    k = len(order)
    inG = lambda j, p: dot(Gs[j][0], p) >= Gs[j][1]
    inN = lambda j, p: all(not inG(order[i], p) for i in range(j))  # N_j
    if k == 1:
        return all(inG(order[0], p) for p in P)
    for j in range(1, k - 1):  # internal node N_{j-1}, children G_{order[j-1]}, N_j
        for p in P:
            if inN(j - 1, p) and not (inG(order[j - 1], p) or inN(j, p)):
                return False
    for p in P:  # last internal node N_{k-2}, children the last two leaves
        if inN(k - 2, p) and not (inG(order[k - 2], p) or inG(order[k - 1], p)):
            return False
    return True


def polytope_version_ok(A, y, P, Gs, order, tau):
    """Theorem 1.7(c)(i): replace every node set S by conv(S cap P)."""
    k = len(order)
    inG = lambda j, p: dot(Gs[j][0], p) >= Gs[j][1]
    inN = lambda j, p: all(not inG(order[i], p) for i in range(j))
    leafsets = [[p for p in P if inG(order[j], p)] for j in range(k)]
    nodesets = [[p for p in P if inN(j, p)] for j in range(k - 1)]
    # leaf bounds: effective set is inside conv(G cap P)
    for L in leafsets:
        if L and hull_min(A, y, L)[0] < tau:
            return False
    # covering: P-points of conv(N_{j-1} cap P) lie in the children's polytopes
    for j in range(1, k):
        S = nodesets[j - 1]
        if not S:
            continue
        inside = [p for p in P if in_hull(p, S)]
        if sorted(inside) != sorted(S):  # conv(S cap P) cap P = S cap P
            return False
        kids = [leafsets[j - 1], nodesets[j] if j <= k - 2 else leafsets[k - 1]]
        for p in inside:
            if not any(K and in_hull(p, K) for K in kids):
                return False
    return True


def caterpillar_ok(P, parts, order):
    """old construction: node conv(I_j u ... u I_k), children conv I_j and the rest"""
    k = len(order)
    cls = [[P[i] for i in range(len(P)) if parts[o] >> i & 1] for o in order]
    for j in range(k - 1):
        node = sum(cls[j:], [])
        rest = sum(cls[j + 1:], [])
        for p in P:
            if in_hull(p, node) and not (in_hull(p, cls[j]) or in_hull(p, rest)):
                return False
    return True


def run_instance(A, y, P, eps, max_parts, max_orders, rng, poly_orders=2, cater=True):
    OPT = min(phi(A, y, p) for p in P)
    tau = OPT - eps
    bad = bad_masks(A, y, P, tau)
    ok = admissible_table(len(P), bad)
    f = min_cover(len(P), ok)
    kappa = f[(1 << len(P)) - 1]
    parts_list = all_min_partitions(len(P), ok, f, limit=max_parts)
    stats = dict(kappa=kappa, parts=len(parts_list), pairs=0, chain_ok=0, grad_ok=0,
                 poly_checked=0, poly_ok=0, cat_checked=0, cat_fail=0)
    for parts in parts_list:
        Gs, gok = gradient_halfspaces(A, y, P, parts, tau, kappa)
        orders = list(itertools.permutations(range(kappa)))
        if len(orders) > max_orders:
            orders = rng.sample(orders, max_orders)
        for oi, order in enumerate(orders):
            stats['pairs'] += 1
            stats['grad_ok'] += gok
            if kappa == 1:
                stats['chain_ok'] += gok
                continue
            stats['chain_ok'] += gok and chain_covering_ok(P, Gs, order)
            if oi < poly_orders:
                stats['poly_checked'] += 1
                stats['poly_ok'] += polytope_version_ok(A, y, P, Gs, order, tau)
            if cater and oi < poly_orders:
                stats['cat_checked'] += 1
                stats['cat_fail'] += not caterpillar_ok(P, parts, order)
    return stats


def partA():
    print("== Part A: the first review's caterpillar counterexample ==")
    A = [[Fr(-2), Fr(1)], [Fr(3), Fr(3)]]
    y = [Fr(-3, 5), Fr(18, 7)]
    P = [(Fr(i), Fr(j)) for i in range(4) for j in range(3)]
    OPT = min(phi(A, y, p) for p in P)
    tau = OPT - Fr(1, 20)
    I1 = [(0, 1), (0, 2), (1, 1), (1, 2), (2, 1), (3, 1), (3, 2)]
    I2c = [(0, 0)]
    I3 = [(1, 0), (2, 0), (2, 2), (3, 0)]
    idx = {p: i for i, p in enumerate(P)}
    parts = [sum(1 << idx[(Fr(a), Fr(b))] for a, b in I) for I in (I1, I2c, I3)]
    bad = bad_masks(A, y, P, tau)
    ok = admissible_table(len(P), bad)
    f = min_cover(len(P), ok)
    print(f"   OPT = {OPT}, tau = {tau}, exact kappa = {f[-1]}; classes admissible: {[ok[m] for m in parts]}")
    p11 = (Fr(1), Fr(1))
    print(f"   (1,1) in conv(I2 u I3): {in_hull(p11, [P[idx[(Fr(a), Fr(b))]] for a, b in I2c + I3])}, "
          f"in conv I2: {in_hull(p11, [(Fr(0), Fr(0))])}, in conv I3: {in_hull(p11, [(Fr(a), Fr(b)) for a, b in I3])}")
    Gs, gok = gradient_halfspaces(A, y, P, parts, tau, 3)
    res = []
    for order in itertools.permutations(range(3)):
        res.append((order, caterpillar_ok(P, parts, order), gok and chain_covering_ok(P, Gs, order),
                    polytope_version_ok(A, y, P, Gs, order, tau)))
    for order, cat, ch, po in res:
        print(f"   order {tuple(o + 1 for o in order)}: caterpillar valid {cat}; hemispace(halfspace) chain valid {ch}; polytope version valid {po}")


def rand_instance(rng, d, P):
    """A random integer (invertible), target y = A c + noise with c inside conv P, so
    that the continuous minimizer sits among the P-points (larger kappa)."""
    from exact import solve
    while True:
        A = [[Fr(rng.randint(-3, 3)) for _ in range(d)] for _ in range(d)]
        if solve(A, [Fr(0)] * d) is not None:
            break
    hi = [max(p[k] for p in P) for k in range(d)]
    c = [Fr(rng.randint(1, 8 * int(h) - 1), 8) for h in hi]
    y = [sum(A[i][j] * c[j] for j in range(d)) + Fr(rng.randint(-3, 3), 10) for i in range(d)]
    return A, y


def partB(n2=60, n3=40, seed=20260929):
    print("== Part B: random open-E instances (exact) ==")
    rng = random.Random(seed)
    for d, trials, P in ((2, n2, [(Fr(i), Fr(j)) for i in range(4) for j in range(3)]),
                         (3, n3, [(Fr(i), Fr(j), Fr(k)) for i in range(2) for j in range(2) for k in range(3)])):
        tot = dict(pairs=0, chain_ok=0, grad_ok=0, poly_checked=0, poly_ok=0, cat_checked=0, cat_fail=0)
        kd = {}
        for t in range(trials):
            A, y = rand_instance(rng, d, P)
            OPT0 = min(phi(A, y, p) for p in P)
            eps = rng.choice([Fr(0), OPT0 / 100, OPT0 / 10, OPT0 / 3])
            st = run_instance(A, y, P, eps, max_parts=30 if d == 2 else 12,
                              max_orders=24 if d == 2 else 6, rng=rng,
                              poly_orders=2 if d == 2 else 1, cater=True)
            kd[st['kappa']] = kd.get(st['kappa'], 0) + 1
            for k in tot:
                tot[k] += st[k]
        print(f"   d={d}: {trials} instances, kappa distribution {dict(sorted(kd.items()))}")
        print(f"      (partition, ordering) pairs: {tot['pairs']}; gradient halfspaces valid: {tot['grad_ok']}; "
              f"chain covering valid at every internal node: {tot['chain_ok']}")
        print(f"      polytope version (c)(i) checked {tot['poly_checked']}, valid {tot['poly_ok']}; "
              f"old caterpillar checked {tot['cat_checked']}, invalid {tot['cat_fail']}")


# ------------------------------------------------------------------ Part C: non-open E
# Q = [0,1] x [-1,1];  phi = -1 on int Q;  phi(0, s) = (s+1)(s+1/2) on the left edge;
# +inf elsewhere.  phi is convex (h >= -1/16 >= -1 on the edge), not lsc.
# tau = 0:  E = {phi < 0} = int Q  u  {0} x (-1, -1/2).   P = {-1,0,1}^2.
def h_edge(s):
    return (s + 1) * (s + Fr(1, 2))


def phiC(x):
    x1, x2 = x
    if 0 < x1 < 1 and -1 < x2 < 1:
        return Fr(-1)
    if x1 == 0 and -1 <= x2 <= 1:
        return h_edge(x2)
    return None  # +inf


def in_E(x):
    v = phiC(x)
    return v is not None and v < 0


def conv_meets_E(S):
    """exact: conv(S) cap E != empty (S finite in Q^2)."""
    S = [tuple(map(F, s)) for s in S]
    # (1) conv(S) cap int Q: clip conv(S) by Q; nonempty clip meets int Q iff the
    #     average of the clipped vertices lies in int Q (a relative-interior point).
    poly = convex_hull(S)
    for (a, b, c) in ((1, 0, 0), (-1, 0, -1), (0, 1, -1), (0, -1, -1)):  # a x1 + b x2 >= c
        poly = clip(poly, a, b, c)
        if not poly:
            break
    if poly:
        cx = sum(p[0] for p in poly) / len(poly)
        cy = sum(p[1] for p in poly) / len(poly)
        if 0 < cx < 1 and -1 < cy < 1:
            return True
    # (2) conv(S) cap ({0} x (-1,-1/2)): interval of conv(S) on the line x1 = 0
    iv = line_interval(S)
    if iv is not None:
        lo, hi = iv
        if lo < Fr(-1, 2) and hi > -1:
            return True
    return False


def convex_hull(S):
    pts = sorted(set(S))
    if len(pts) <= 2:
        return pts
    cross = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def clip(poly, a, b, c):
    """Sutherland-Hodgman clip of a convex polygon (or segment/point) by a x1 + b x2 >= c."""
    if not poly:
        return []
    val = lambda p: a * p[0] + b * p[1] - c
    if len(poly) == 1:
        return poly if val(poly[0]) >= 0 else []
    out = []
    m = len(poly)
    edges = [(poly[i], poly[(i + 1) % m]) for i in range(m)] if m > 2 else [(poly[0], poly[1]), (poly[1], poly[0])]
    for p, q in edges:
        vp, vq = val(p), val(q)
        if vp >= 0:
            out.append(p)
        if (vp > 0 > vq) or (vp < 0 < vq):
            t = vp / (vp - vq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    res = []
    for p in out:
        if p not in res:
            res.append(p)
    return convex_hull(res) if len(res) > 2 else res


def line_interval(S, g=(Fr(1), Fr(0)), alpha=Fr(0), h=(Fr(0), Fr(1))):
    """conv(S) cap {g.x = alpha}, as an interval of h.x (None if empty)."""
    vals = []
    for p in S:
        if dot(g, p) == alpha:
            vals.append(dot(h, p))
    for p, q in itertools.combinations(S, 2):
        gp, gq = dot(g, p) - alpha, dot(g, q) - alpha
        if (gp < 0 < gq) or (gq < 0 < gp):
            t = gp / (gp - gq)
            x = (p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1]))
            vals.append(dot(h, x))
    if not vals:
        return None
    return min(vals), max(vals)


QV = [(Fr(0), Fr(-1)), (Fr(1), Fr(-1)), (Fr(1), Fr(1)), (Fr(0), Fr(1))]  # vertices of cl E = Q


def E_on_line(g, alpha, h):
    """E cap {g.x = alpha} as an interval of t = h.x: (lo, lo_open, hi, hi_open) or None.
    E = int Q u L.  int Q cap line is an open interval; L = {0} x (-1,-1/2)."""
    pieces = []
    iv = line_interval(QV, g, alpha, h)   # cl Q cap line
    if iv is not None and iv[0] < iv[1]:
        # line meets int Q iff the midpoint of the chord is in int Q
        lo, hi = iv
        # recover midpoint point: solve g.x = alpha, h.x = (lo+hi)/2
        det = g[0] * h[1] - g[1] * h[0]
        tm = (lo + hi) / 2
        x = ((alpha * h[1] - g[1] * tm) / det, (g[0] * tm - alpha * h[0]) / det)
        if 0 < x[0] < 1 and -1 < x[1] < 1:
            pieces.append((lo, True, hi, True))
    # L cap line
    Lend = [(Fr(0), Fr(-1)), (Fr(0), Fr(-1, 2))]
    ga, gb = dot(g, Lend[0]) - alpha, dot(g, Lend[1]) - alpha
    if ga == 0 and gb == 0:
        ta, tb = dot(h, Lend[0]), dot(h, Lend[1])
        pieces.append((min(ta, tb), True, max(ta, tb), True))
    elif (ga < 0 < gb) or (gb < 0 < ga):
        t = ga / (ga - gb)
        x = (Lend[0][0] + t * (Lend[1][0] - Lend[0][0]), Lend[0][1] + t * (Lend[1][1] - Lend[0][1]))
        pieces.append((dot(h, x), False, dot(h, x), False))
    if not pieces:
        return None
    # union of intervals (E cap line is convex, so the union is an interval)
    lo = min(p[0] for p in pieces)
    lo_open = all(p[1] for p in pieces if p[0] == lo)
    hi = max(p[2] for p in pieces)
    hi_open = all(p[3] for p in pieces if p[2] == hi)
    return lo, lo_open, hi, hi_open


def lemma17a_hemispace(S, gchoice=0, alpha_choice='low'):
    """Build a hemispace G containing conv(S) and missing E, following the proof of
    Lemma 1.7a: weak separation in R^2, then recursion on the line, then on a point.
    Returns a membership function, a description, or None if no separator candidate."""
    S = [tuple(map(F, s)) for s in S]
    # weak separation of conv S and E (equivalently cl E = Q): g >= alpha on S, g <= alpha on Q
    cands = []
    pts = S + QV
    for p, q in itertools.combinations(pts, 2):
        d = (q[0] - p[0], q[1] - p[1])
        for g in ((-d[1], d[0]), (d[1], -d[0])):
            if g != (0, 0):
                cands.append(g)
    cands += [(Fr(1), Fr(0)), (Fr(-1), Fr(0)), (Fr(0), Fr(1)), (Fr(0), Fr(-1))]
    seps = []
    for g in cands:
        mq = max(dot(g, v) for v in QV)
        ms = min(dot(g, s) for s in S)
        if ms >= mq:
            seps.append((g, mq, ms))
    if not seps:
        return None
    g, mq, ms = seps[gchoice % len(seps)]
    alpha = mq if alpha_choice == 'low' else ms
    h = (-g[1], g[0])
    # recursion on the line H = {g.x = alpha}: A' = conv S cap H, B' = E cap H (intervals in t = h.x)
    Ai = line_interval(S, g, alpha, h)
    Bi = E_on_line(g, alpha, h)
    if Ai is None:
        line_part = ('empty',)
    elif Bi is None:
        line_part = ('all',)
    else:
        a_lo, a_hi = Ai
        b_lo, b_lo_open, b_hi, b_hi_open = Bi
        # 1-D separation of disjoint intervals; A' to the right or to the left of B'
        if a_lo >= b_hi:
            s, beta = 1, b_hi       # G' = {t > beta} u ({t = beta} if in A')
        elif a_hi <= b_lo:
            s, beta = -1, -b_lo     # G' = {-t > beta} u ...
        else:
            raise AssertionError("A' and B' overlap")
        include = (a_lo <= s * beta <= a_hi) if s == 1 else (a_lo <= -beta <= a_hi)
        line_part = ('half', s, beta, include)

    def member(x):
        x = tuple(map(F, x))
        gx = dot(g, x)
        if gx > alpha:
            return True
        if gx < alpha:
            return False
        if line_part[0] == 'empty':
            return False
        if line_part[0] == 'all':
            return True
        _, s, beta, include = line_part
        t = s * dot(h, x)
        return t > beta or (t == beta and include)
    return member, (g, alpha, line_part)


def check_G_disjoint_E(member, desc):
    """exact: G cap E = empty, using the structure of G."""
    g, alpha, line_part = desc
    if max(dot(g, v) for v in QV) > alpha:
        return False  # some point of int Q would have g.x > alpha (Q is the closure of E)
    Bi = E_on_line(g, alpha, (-g[1], g[0]))
    if Bi is None or line_part[0] == 'empty':
        return True
    if line_part[0] == 'all':
        return False
    _, s, beta, include = line_part
    lo, lo_open, hi, hi_open = Bi
    # E cap H is the interval (lo, hi) with flags; in t' = s t it must satisfy t' < beta,
    # or t' == beta excluded or not in G'
    if s == 1:
        top, top_open = hi, hi_open
    else:
        top, top_open = -lo, lo_open
    if top > beta:
        return False
    if top == beta and not top_open and include:
        return False
    return True


def convexity_test(member, desc, rng, trials=4000):
    """randomized exact test that G and its complement are convex.  Points: a rational
    grid, plus points on the separating line H = {g.x = alpha} (including the special
    point t = beta of the line recursion)."""
    g, alpha, line_part = desc
    h = (-g[1], g[0])
    gg = dot(g, g)
    hh = dot(h, h)
    xH = (alpha * g[0] / gg, alpha * g[1] / gg)
    ts = [Fr(k, 4) for k in range(-12, 13)]
    if line_part[0] == 'half':
        _, s, beta, include = line_part
        ts.append(s * beta / hh)
    online = [(xH[0] + t * h[0], xH[1] + t * h[1]) for t in ts]
    assert all(dot(g, p) == alpha for p in online)
    grid = [Fr(k, 4) for k in range(-8, 9)]
    pts = [(a, b) for a in grid for b in grid] + online * 6
    for _ in range(trials):
        p, q = rng.choice(pts), rng.choice(pts)
        lam = Fr(rng.randint(1, 7), 8)
        m = (lam * p[0] + (1 - lam) * q[0], lam * p[1] + (1 - lam) * q[1])
        if member(p) and member(q) and not member(m):
            return False
        if not member(p) and not member(q) and member(m):
            return False
    return True


def partC(seed=7):
    print("== Part C: non-open E, genuine hemispaces (exact) ==")
    rng = random.Random(seed)
    P = [(Fr(a), Fr(b)) for a in (-1, 0, 1) for b in (-1, 0, 1)]
    print(f"   phi on P: {[(tuple(map(int, p)), str(phiC(p)) if phiC(p) is not None else 'inf') for p in P]}")
    print(f"   no P-point in E: {not any(in_E(p) for p in P)}")
    nP = len(P)
    ok = [False] * (1 << nP)
    ok[0] = True
    for m in range(1, 1 << nP):
        S = [P[i] for i in range(nP) if m >> i & 1]
        ok[m] = not conv_meets_E(S)
    # heredity sanity
    her = all(ok[m ^ (m & -m)] or not ok[m] for m in range(1, 1 << nP))
    f = min_cover(nP, ok)
    kappa = f[-1]
    parts_list = all_min_partitions(nP, ok, f)
    print(f"   exact kappa_0(P) = {kappa}; heredity holds: {her}; minimum partitions: {len(parts_list)}")
    # (i) classes containing (0,0): no closed halfspace and no open halfspace works
    o = P.index((Fr(0), Fr(0)))
    need_hemi = 0
    halfspace_possible = 0
    for parts in parts_list:
        for mask in parts:
            if mask >> o & 1:
                S = [P[i] for i in range(nP) if mask >> i & 1]
                # a closed halfspace {g.x >= c} containing (0,0) and missing int Q must
                # support Q at (0,0), i.e. be {x1 <= 0}; test that candidate exactly:
                closed_ok = all(s[0] <= 0 for s in S) and not in_E((Fr(0), Fr(-3, 4)))
                halfspace_possible += closed_ok
                need_hemi += 1
    print(f"   classes containing (0,0) over all minimum partitions: {need_hemi}; "
          f"of these, served by the only candidate closed halfspace {{x1 <= 0}}: {halfspace_possible} "
          f"((0,-3/4) in E: {in_E((Fr(0), Fr(-3, 4)))})")
    # (ii) Lemma 1.7a hemispaces and the chain, every partition, every ordering,
    #      several separator choices
    total = valid = conv_ok = poly_ok = poly_tot = 0
    not_halfspace = 0
    for parts in parts_list:
        for gchoice in range(3):
            for ach in ('low', 'high'):
                Gs = []
                good = True
                for mask in parts:
                    S = [P[i] for i in range(nP) if mask >> i & 1]
                    res = lemma17a_hemispace(S, gchoice, ach)
                    if res is None:
                        good = False
                        break
                    member, desc = res
                    good &= all(member(s) for s in S) and check_G_disjoint_E(member, desc)
                    conv_ok_here = convexity_test(member, desc, rng, 600)
                    conv_ok += conv_ok_here
                    good &= conv_ok_here
                    not_halfspace += desc[2][0] == 'half'
                    Gs.append(member)
                for order in itertools.permutations(range(kappa)):
                    total += 1
                    if not good:
                        continue
                    k = kappa
                    inN = lambda j, p: all(not Gs[order[i]](p) for i in range(j))
                    cov = True
                    for j in range(1, k - 1):
                        for p in P:
                            if inN(j - 1, p) and not (Gs[order[j - 1]](p) or inN(j, p)):
                                cov = False
                    for p in P:
                        if k >= 2 and inN(k - 2, p) and not (Gs[order[k - 2]](p) or Gs[order[k - 1]](p)):
                            cov = False
                    valid += cov
                    # (c)(i): polytope version: leaves conv(G cap P) must miss E
                    if gchoice == 0 and ach == 'low':
                        poly_tot += 1
                        leaves = [[p for p in P if Gs[order[j]](p)] for j in range(k)]
                        poly_ok += all(not conv_meets_E(L) for L in leaves if L)
    print(f"   Lemma 1.7a hemispaces: {conv_ok} built/tested convex (G and complement); "
          f"{not_halfspace} of them use the line recursion (not a plain open/closed halfspace)")
    print(f"   chains (partition x separator choice x ordering): {total}; covering valid at every internal node: {valid}")
    print(f"   polytope version (c)(i): {poly_ok} of {poly_tot} valid (leaf polytopes conv(G cap P) miss E)")


# ------------------------------------------------------------------ Part D: open, non-smooth E
def partD():
    """Theorem 1.7(c)(ii) without gradients: phi = ||x - (1/2)1||_1 on R^2 (Example 2.1a,
    n = 2), E = open l1 ball.  Closed halfspaces {g.x >= c} with c = min_{I_j} g.x are
    found among finitely many normals; min of phi over a closed halfspace is
    (c - g.center)_+ / ||g||_inf (exact LP duality)."""
    from ex21a_compact_milp import conv_min_l1_2d, phi as phi1
    print("== Part D: open non-smooth E (l1 ball), closed separating halfspaces (exact) ==")
    P = [(Fr(a), Fr(b)) for a in range(-1, 3) for b in range(-1, 3)]
    nP = len(P)
    cen = (Fr(1, 2), Fr(1, 2))
    OPT = min(phi1(p) for p in P)
    for eps in (Fr(0), Fr(1, 4)):
        tau = OPT - eps
        bad = []
        for k in (1, 2, 3):
            for T in itertools.combinations(range(nP), k):
                if conv_min_l1_2d([P[i] for i in T]) < tau:
                    bad.append(sum(1 << i for i in T))
        ok = admissible_table(nP, bad)
        f = min_cover(nP, ok)
        kappa = f[-1]
        parts_list = all_min_partitions(nP, ok, f, limit=60)
        normals = set()
        for p, q in itertools.combinations(P, 2):
            d = (q[0] - p[0], q[1] - p[1])
            normals.add((-d[1], d[0]))
            normals.add((d[1], -d[0]))
        normals |= {(Fr(s1), Fr(s2)) for s1 in (-1, 1) for s2 in (-1, 1)}
        normals.discard((0, 0))
        normals = sorted(normals)
        pairs = valid = 0
        found_all = True
        for parts in parts_list:
            Gs = []
            for mask in parts:
                I = [P[i] for i in range(nP) if mask >> i & 1]
                best = None
                for g in normals:
                    c = min(dot(g, q) for q in I)
                    val = max(Fr(0), c - dot(g, cen)) / max(abs(g[0]), abs(g[1]))
                    if val >= tau:
                        best = (list(g), c)
                        break
                if best is None:
                    found_all = False
                Gs.append(best)
            if any(G is None for G in Gs):
                continue
            for order in itertools.permutations(range(kappa)):
                pairs += 1
                valid += chain_covering_ok(P, Gs, order)
        print(f"   eps={eps}: exact kappa = {kappa}; minimum partitions tested {len(parts_list)}; "
              f"closed separating halfspace found for every class: {found_all}; chains {pairs}, covering valid at every internal node: {valid}")


if __name__ == "__main__":
    parts = sys.argv[1] if len(sys.argv) > 1 else "ABCD"
    if "A" in parts:
        partA()
    if "B" in parts:
        partB()
    if "C" in parts:
        partC()
    if "D" in parts:
        partD()
