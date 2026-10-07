"""coreA checks for Section 4 (grids.tex) after the W3 revision.

Exact arithmetic (fractions) on random small nonconvex mixed-integer box QPs.
Checks, for grids that may contain single-node (degenerate) coordinates:
  Prop cellwise (b): beta = min over cells of the cell bound;
  Prop cellwise (c): formula for beta_i(J) and the inequality >= min m_i;
  Prop cellwise (c), node bound: F(x) >= m_i(v) + d_i(v) whenever x_i = v;
  Prop cellwise (a): F(x) >= beta(C) at random points of random cells;
  family form: the same (b), (c) and node bound when grid intervals are
    replaced by a family of intervals with endpoints in G_i covering all nodes;
  randomized rounding: E Q(Y) <= F(x) (exact expectation by enumeration);
  Def filter / Prop filter: every point of X' outside X'' has F > U, and the
    minimizer of Q lies in X'' (U >= beta).
Usage: python3 coreA-cellwise.py [seed] [count]
"""
import itertools
import random
import sys
from fractions import Fraction as Fr


def rand_instance(rng):
    n = rng.randint(1, 3)
    kinds = [rng.choice("CZ") for _ in range(n)]
    lo, hi = [], []
    for k in kinds:
        a = rng.randint(-3, 1)
        b = a + rng.randint(1, 5)
        lo.append(Fr(a))
        hi.append(Fr(b))
    H = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        H[i][i] = Fr(rng.randint(-4, 4))
        for j in range(i + 1, n):
            v = Fr(rng.randint(-4, 4), rng.randint(1, 2))
            H[i][j] = H[j][i] = v
    b = [Fr(rng.randint(-5, 5), rng.randint(1, 3)) for _ in range(n)]
    L = [max(H[i][i], Fr(0)) for i in range(n)]
    return n, kinds, lo, hi, H, b, L


def F(H, b, x):
    n = len(x)
    return sum(Fr(1, 2) * H[i][j] * x[i] * x[j] for i in range(n) for j in range(n)) + sum(
        b[i] * x[i] for i in range(n)
    )


def rand_subbox_grid(rng, n, kinds, lo, hi):
    """Random subbox X' (possibly degenerate coordinates) and a grid for it."""
    G = []
    for i in range(n):
        if kinds[i] == "Z":
            pts = list(range(int(lo[i]), int(hi[i]) + 1))
            a = rng.choice(pts)
            bb = rng.choice([p for p in pts if p >= a])
            if rng.random() < 0.2:
                bb = a
            inner = [p for p in range(a + 1, bb)]
            sel = sorted(set([a, bb] + [p for p in inner if rng.random() < 0.5]))
            G.append([Fr(p) for p in sel])
        else:
            a = lo[i] + Fr(rng.randint(0, 2), 2)
            bb = hi[i] - Fr(rng.randint(0, 2), 2)
            if bb < a:
                a, bb = bb, a
            if rng.random() < 0.15:
                bb = a
            inner = sorted(set(a + (bb - a) * Fr(rng.randint(1, 7), 8) for _ in range(rng.randint(0, 3))))
            sel = sorted(set([a, bb] + [p for p in inner if a < p < bb]))
            G.append(sel)
    return G


def grid_intervals(Gi):
    if len(Gi) == 1:
        return [(Gi[0], Gi[0])]
    return [(Gi[k], Gi[k + 1]) for k in range(len(Gi) - 1)]


def eff_width(kind, J):
    a, a2 = J
    if kind == "Z" and a2 - a == 1:
        return Fr(0)
    return a2 - a


def setup(n, kinds, H, b, L, G, fam):
    """fam[i]: list of intervals (a,a') for coordinate i; every node is an endpoint."""
    w = []
    for i in range(n):
        wi = {}
        for v in G[i]:
            ws = [eff_width(kinds[i], J) for J in fam[i] if v in J]
            assert ws, "node not covered"
            wi[v] = max(ws)
        w.append(wi)
    d = [{v: L[i] * w[i][v] ** 2 / 8 for v in G[i]} for i in range(n)]
    Q = {}
    for y in itertools.product(*G):
        Q[y] = F(H, b, y) - sum(d[i][y[i]] for i in range(n))
    beta = min(Q.values())
    m = [{v: min(q for y, q in Q.items() if y[i] == v) for v in G[i]} for i in range(n)]
    return w, d, Q, beta, m


def cell_bound(n, kinds, H, b, L, C):
    verts = itertools.product(*[sorted(set(J)) for J in C])
    return min(F(H, b, v) for v in verts) - sum(L[i] * eff_width(kinds[i], C[i]) ** 2 / 8 for i in range(n))


def rand_point_in(rng, kind, J):
    a, a2 = J
    if kind == "Z":
        return Fr(rng.randint(int(a), int(a2)))
    return a + (a2 - a) * Fr(rng.randint(0, 12), 12)


def check_one(rng, inst, fam_mode):
    n, kinds, lo, hi, H, b, L = inst
    G = rand_subbox_grid(rng, n, kinds, lo, hi)
    fam = []
    for i in range(n):
        gi = grid_intervals(G[i])
        if fam_mode and len(G[i]) >= 3:
            # random family: intervals between (not necessarily consecutive) nodes,
            # every node an endpoint of some member
            Gi = G[i]
            members = set()
            for v in Gi:
                u = rng.choice([x for x in Gi if x != v])
                members.add((min(u, v), max(u, v)))
            for _ in range(rng.randint(0, 2)):
                u, v = rng.sample(Gi, 2)
                members.add((min(u, v), max(u, v)))
            fam.append(sorted(members))
        else:
            fam.append(gi)
    w, d, Q, beta, m = setup(n, kinds, H, b, L, G, fam)
    cells = list(itertools.product(*fam))
    # (b)
    bc = {C: cell_bound(n, kinds, H, b, L, C) for C in cells}
    assert min(bc.values()) == beta, ("(b) fails", min(bc.values()), beta)
    # (c)
    for i in range(n):
        for J in fam[i]:
            bi = min(v for C, v in bc.items() if C[i] == J)
            ends = sorted(set(J))
            formula = min(m[i][v] + d[i][v] for v in ends) - L[i] * eff_width(kinds[i], J) ** 2 / 8
            assert bi == formula, ("(c) formula", bi, formula)
            assert bi >= min(m[i][v] for v in ends)
    # (a) and node bound at random points
    for _ in range(30):
        C = rng.choice(cells)
        x = [rand_point_in(rng, kinds[i], C[i]) for i in range(n)]
        fx = F(H, b, x)
        assert fx >= bc[C], ("(a)", fx, bc[C])
        for i in range(n):
            if x[i] in G[i]:
                v = x[i]
                assert fx >= m[i][v] + d[i][v], ("node bound", fx, m[i][v] + d[i][v])
        # randomized rounding, exact expectation
        probs = []
        for i in range(n):
            a, a2 = C[i]
            if a2 == a:
                probs.append([(a, Fr(1))])
            else:
                p = (x[i] - a) / (a2 - a)
                probs.append([(a, 1 - p), (a2, p)])
        EQ = Fr(0)
        for combo in itertools.product(*probs):
            y = tuple(c[0] for c in combo)
            pr = Fr(1)
            for c in combo:
                pr *= c[1]
            if pr:
                EQ += pr * Q[y]
        assert EQ <= fx, ("rounding", EQ, fx)
    # filtering (grid-interval form only)
    if not fam_mode:
        P = [i for i in range(n) if L[i] > 0]
        U = beta + Fr(rng.randint(0, 6), 2)
        ystar = min(Q, key=Q.get)
        newbox = []
        for i in range(n):
            if i in P:
                ret = [J for J in fam[i] if min(m[i][J[0]], m[i][J[1]]) <= U]
                assert ret
                newbox.append((min(J[0] for J in ret), max(J[1] for J in ret)))
            else:
                newbox.append((G[i][0], G[i][-1]))
            assert newbox[i][0] <= ystar[i] <= newbox[i][1]
        for _ in range(40):
            x = [rand_point_in(rng, kinds[i], (G[i][0], G[i][-1])) for i in range(n)]
            inside = all(newbox[i][0] <= x[i] <= newbox[i][1] for i in range(n))
            if not inside:
                assert F(H, b, x) > U, "filter removed a point with F <= U"
    return True


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    rng = random.Random(seed)
    k = 0
    for t in range(count):
        inst = rand_instance(rng)
        check_one(rng, inst, fam_mode=False)
        check_one(rng, inst, fam_mode=True)
        k += 2
    print(f"seed {seed}: {k} grid/family checks passed")


if __name__ == "__main__":
    main()
