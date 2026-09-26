"""Exact-arithmetic stress check of the two-quality source-interval reduction.

Independent reproduction (2026-09-25) of the reviewer check described in
notes/review-pooling-two-source-qualities-source-intervals-independent.md,
section "Exact arithmetic stress checks"; the reviewer's script was not
archived. Standard library only; every quantity is a Fraction.

Each case builds a random physically feasible one-pool network with interior
pool quality q, two distinct source quality vectors, source supply intervals,
and bypass arcs. It then checks, exactly, against
results/pooling-two-source-qualities-convex-feasibility.md:
  * the vector-to-scalar normalization and every conserved component equation;
  * the lifted point (q, r, t, h, w) with r = q^2 + q(1-q)/4 satisfies the
    scaled source rows (9)-(11), the output identities (3)-(4), the
    strengthened output rows (6), and the strengthened common-capacity and
    signed resource rows (5a);
  * reverse recovery from the scaled variables alone returns a flow that
    satisfies every original bound and balance, and the pool quality balance
    follows from sum_i h_i = 0.
"""
from collections import Counter
from fractions import Fraction as F
from random import Random

SEED = 310905
CASES = 240


def rat(rng, lo, hi, den=12):
    """Random rational in [lo, hi] with small denominators."""
    return lo + (hi - lo) * F(rng.randint(0, den), den)


def make_case(rng, k):
    # pool quality q, including the extreme interior values 2^-80, 1-2^-80
    if k % 8 == 0:
        q = F(1, 2**80)
    elif k % 8 == 1:
        q = 1 - F(1, 2**80)
    else:
        q = F(rng.randint(1, 99), 100)
    inactive = rng.random() < 0.15
    n0, n1 = rng.randint(1, 4), rng.randint(1, 4)
    cls = [0] * n0 + [1] * n1
    nsrc, nprod = n0 + n1, rng.randint(2, 6)
    dim = rng.randint(1, 4)
    s0 = [rat(rng, -3, 3) for _ in range(dim)]
    s1 = list(s0)
    kstar = rng.randrange(dim)
    while s1[kstar] == s0[kstar]:
        s1 = [rat(rng, -3, 3) for _ in range(dim)]
    svec = [s0 if c == 0 else s1 for c in cls]
    zero_demand = {j for j in range(nprod) if rng.random() < 0.2}
    # pool intake with exact class-1 share q
    Y = F(0) if inactive else rat(rng, 1, 10)
    y = [F(0)] * nsrc
    for c, share in ((0, 1 - q), (1, q)):
        members = [i for i in range(nsrc) if cls[i] == c]
        weights = [F(rng.randint(1, 5)) for _ in members]
        for i, wt in zip(members, weights):
            y[i] = Y * share * wt / sum(weights)
    # outlet flows summing to Y (zero for zero-demand products)
    active = [j for j in range(nprod) if j not in zero_demand]
    v = [F(0)] * nprod
    if active and Y > 0:
        weights = {j: F(rng.randint(0, 4)) for j in active}
        if sum(weights.values()) == 0:
            weights[active[0]] = F(1)
        for j in active:
            v[j] = Y * weights[j] / sum(weights.values())
    elif Y > 0:          # every product has zero demand: pool must be idle
        Y, y = F(0), [F(0)] * nsrc
        inactive = True
    # bypass arcs: sparse or dense pattern
    density = rng.choice([0.2, 0.5, 1.0])
    arcs = [(i, j) for i in range(nsrc) for j in range(nprod) if rng.random() < density]
    z = {e: (F(0) if e[1] in zero_demand else rat(rng, 0, 3)) for e in arcs}
    # zero-demand check: nothing reaches these products
    b = [v[j] + sum(z[e] for e in arcs if e[1] == j) for j in range(nprod)]
    zero_demand |= {j for j in range(nprod) if b[j] == 0}
    pvec = [s0[d] + q * (s1[d] - s0[d]) for d in range(dim)]
    Bvec = []
    for j in range(nprod):
        if b[j] == 0:
            Bvec.append([rat(rng, -5, 5) for _ in range(dim)])  # immaterial
        else:
            Bvec.append([(v[j] * pvec[d] + sum(z[e] * svec[e[0]][d] for e in arcs if e[1] == j)) / b[j]
                         for d in range(dim)])
    A = [y[i] + sum(z[e] for e in arcs if e[0] == i) for i in range(nsrc)]
    # non-singleton bounds containing the flow; positive feed lower bounds
    supply = [(max(F(0), A[i] - rat(rng, 0, 2)), A[i] + rat(rng, F(1, 4), 2)) for i in range(nsrc)]
    feed = []
    for i in range(nsrc):
        lo = y[i] * rat(rng, F(1, 4), 1) if y[i] > 0 and rng.random() < 0.7 else F(0)
        feed.append((lo, y[i] + rat(rng, 0, 2)))
    zb = {e: (z[e] * rat(rng, 0, 1), z[e] + rat(rng, 0, 1)) for e in arcs}
    # outlet caps and resource rows chosen so the strengthened rows (r slack) hold
    ucap = [F(4, 3) * v[j] + rat(rng, 0, 1) for j in range(nprod)]
    rows = [([F(1)] * nprod, F(4, 3) * Y + rat(rng, 0, 1))]          # common capacity
    for _ in range(rng.randint(0, 3)):                                  # signed resource rows
        alpha = [F(rng.randint(-3, 3), rng.randint(1, 3)) for _ in range(nprod)]
        rows.append((alpha, max(F(0), F(4, 3) * sum(a * vv for a, vv in zip(alpha, v))) + rat(rng, 0, 1)))
    return dict(q=q, cls=cls, s0=s0, s1=s1, kstar=kstar, svec=svec, pvec=pvec, Bvec=Bvec,
                b=b, supply=supply, feed=feed, zb=zb, ucap=ucap, rows=rows, arcs=arcs,
                y=y, z=z, v=v, A=A, inactive=inactive, zero=zero_demand)


def check(c, cnt):
    q, cls, arcs, b = c['q'], c['cls'], c['arcs'], c['b']
    nsrc, nprod, dim = len(cls), len(b), len(c['s0'])
    s0, s1, ks = c['s0'], c['s1'], c['kstar']
    y, z, v, A = c['y'], c['z'], c['v'], c['A']
    assert 0 < q < 1

    # --- vector qualities: normalization and component equations
    B = []
    for j in range(nprod):
        if b[j] == 0:
            B.append(F(0))       # immaterial
            continue
        Bj = (c['Bvec'][j][ks] - s0[ks]) / (s1[ks] - s0[ks])
        assert 0 <= Bj <= 1
        for d in range(dim):     # product lies on the source line
            assert c['Bvec'][j][d] == s0[d] + Bj * (s1[d] - s0[d]); cnt['vector'] += 1
            assert (v[j] * c['pvec'][d] + sum(z[e] * c['svec'][e[0]][d] for e in arcs if e[1] == j)
                    == b[j] * c['Bvec'][j][d]); cnt['vector'] += 1
        B.append(Bj)
    for d in range(dim):         # pool component balance
        assert sum(y[i] * c['svec'][i][d] for i in range(nsrc)) == sum(y) * c['pvec'][d]; cnt['vector'] += 1

    # --- class totals (8)
    A0 = sum(b[j] * (1 - B[j]) for j in range(nprod))
    A1 = sum(b[j] * B[j] for j in range(nprod))
    assert sum(A[i] for i in range(nsrc) if cls[i] == 0) == A0
    assert sum(A[i] for i in range(nsrc) if cls[i] == 1) == A1

    # --- lifted point
    gamma = [-q if cls[i] == 0 else 1 - q for i in range(nsrc)]
    r = q * q + q * (1 - q) / 4
    assert q * q < r <= 1
    t = [gamma[i] * A[i] for i in range(nsrc)]
    h = [gamma[i] * y[i] for i in range(nsrc)]
    w = {e: gamma[e[0]] * z[e] for e in arcs}

    def between(x, u1, u2):
        return min(u1, u2) <= x <= max(u1, u2)

    # source rows (9)-(11)
    for i in range(nsrc):
        L, U = c['supply'][i]
        assert L < U
        assert between(t[i], gamma[i] * L, gamma[i] * U); cnt['source'] += 1
        assert between(h[i], gamma[i] * c['feed'][i][0], gamma[i] * c['feed'][i][1]); cnt['source'] += 1
        assert t[i] == h[i] + sum(w[e] for e in arcs if e[0] == i); cnt['source'] += 1
        cnt['feed_lb'] += c['feed'][i][0] > 0
    for e in arcs:
        assert between(w[e], gamma[e[0]] * c['zb'][e][0], gamma[e[0]] * c['zb'][e][1]); cnt['source'] += 1
    assert sum(t[i] for i in range(nsrc) if cls[i] == 0) == -q * A0; cnt['source'] += 1
    assert sum(t[i] for i in range(nsrc) if cls[i] == 1) == (1 - q) * A1; cnt['source'] += 1

    # output rows (3), (4), (6)
    W0 = [sum(w[e] for e in arcs if e[1] == j and cls[e[0]] == 0) for j in range(nprod)]
    W1 = [sum(w[e] for e in arcs if e[1] == j and cls[e[0]] == 1) for j in range(nprod)]
    for j in range(nprod):
        assert W0[j] + W1[j] == b[j] * (B[j] - q); cnt['output'] += 1
        assert W0[j] == q * b[j] * (B[j] - 1) + q * (1 - q) * v[j]; cnt['output'] += 1
        assert q * b[j] * (B[j] - 1) <= W0[j] <= q * b[j] * (B[j] - 1) + c['ucap'][j] * (q - r); cnt['output'] += 1

    # common-capacity and signed resource rows, strengthened (5a)
    for alpha, U in c['rows']:
        assert U >= 0
        assert sum(a * vv for a, vv in zip(alpha, v)) <= U
        assert (sum(a * W for a, W in zip(alpha, W0))
                <= q * sum(a * b[j] * (B[j] - 1) for j, a in enumerate(alpha)) + U * (q - r)); cnt['resource'] += 1

    # --- reverse recovery from the scaled variables only
    Ar = [t[i] / gamma[i] for i in range(nsrc)]
    yr = [h[i] / gamma[i] for i in range(nsrc)]
    zr = {e: w[e] / gamma[e[0]] for e in arcs}
    vr = [b[j] - sum(zr[e] for e in arcs if e[1] == j) for j in range(nprod)]
    for j in range(nprod):
        # (4) solved for v_j, and (6) with r > q^2 implies the original cap
        assert vr[j] == (W0[j] - q * b[j] * (B[j] - 1)) / (q * (1 - q)); cnt['output'] += 1
        assert 0 <= vr[j] <= c['ucap'][j]
        assert q * vr[j] + sum(zr[e] for e in arcs if e[1] == j and cls[e[0]] == 1) == b[j] * B[j]
    for i in range(nsrc):
        assert c['supply'][i][0] <= Ar[i] <= c['supply'][i][1]
        assert c['feed'][i][0] <= yr[i] <= c['feed'][i][1]
        assert Ar[i] == yr[i] + sum(zr[e] for e in arcs if e[0] == i)
    for e in arcs:
        assert c['zb'][e][0] <= zr[e] <= c['zb'][e][1]
    for alpha, U in c['rows']:
        assert sum(a * vv for a, vv in zip(alpha, vr)) <= U
    assert sum(h) == 0                                   # implies the pool quality balance
    assert sum(yr) == sum(vr)                            # pool mass
    assert sum(yr[i] for i in range(nsrc) if cls[i] == 1) == q * sum(yr)
    assert (Ar, yr, zr, vr) == (A, y, z, v)

    cnt['zero_demand'] += sum(1 for j in range(nprod) if b[j] == 0)
    cnt['inactive'] += sum(yr) == 0
    cnt['q_tiny'] += q == F(1, 2**80)
    cnt['q_near_one'] += q == 1 - F(1, 2**80)


def main():
    rng = Random(SEED)
    cnt = Counter()
    for k in range(CASES):
        check(make_case(rng, k), cnt)
        cnt['cases'] += 1
    print(f"seed={SEED}")
    for key in ('cases', 'q_tiny', 'q_near_one', 'source', 'output', 'resource', 'vector',
                'zero_demand', 'inactive', 'feed_lb'):
        print(f"{key}: {cnt[key]}")
    print("ALL PASSED")


if __name__ == '__main__':
    main()
