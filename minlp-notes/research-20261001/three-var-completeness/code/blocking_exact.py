"""Exact (rational) blocking test and enumeration of minimal blocking zero
configurations at the origin, including configurations with one zero
segment inside a facet.

Zero types
  point:   ('P', s)            s in {0,1,-1}^3, -1 = generic free coordinate
  segment: ('S', j, c, A, B)   segment in facet x_j = c joining generic
                               points of the boundary faces A and B of that
                               facet (A, B are statuses with s_j = c).
Generic coordinates are random rationals; the blocking test is exact for
those values (two independent draws must both block).

Blocking (note.md, Lemma 2.4): for every Fr subset of {0,1,2},
pi_Fr(0) lies in the affine hull of pi_Fr(Z cap S_Fr), with
S_Fr = {x : x_j != 1 for j not in Fr}.
"""
import sys
from fractions import Fraction
from itertools import combinations, permutations, product
import random

POINT_FACES = [s for s in product((0, 1, -1), repeat=3) if s != (-1, -1, -1)]


def facet_anchors(j, c):
    out = []
    for s in product((0, 1, -1), repeat=3):
        if s[j] != c:
            continue
        if s.count(-1) == 2:
            continue  # the facet itself
        out.append(s)
    return out  # 4 edges + 4 vertices of the facet


def same_edge(a, b, j):
    # anchors a, b of facet j lie on a common edge of that facet
    free_a = [i for i in range(3) if a[i] == -1]
    free_b = [i for i in range(3) if b[i] == -1]
    if a == b:
        return True
    # edge contains vertex?
    for e, v in ((a, b), (b, a)):
        if e.count(-1) == 1 and v.count(-1) == 0:
            if all(e[i] == v[i] for i in range(3) if e[i] != -1):
                return True
    # two vertices on a common edge of the facet
    if a.count(-1) == 0 and b.count(-1) == 0:
        diff = [i for i in range(3) if a[i] != b[i]]
        if len(diff) == 1:
            return True
    return False


SEGMENTS = []
for j in range(3):
    for c in (0, 1):
        anc = facet_anchors(j, c)
        for a, b in combinations(anc, 2):
            if not same_edge(a, b, j):
                SEGMENTS.append(('S', j, c, a, b))
POINTS = [('P', s) for s in POINT_FACES]


def rand_point(s, rnd):
    return [Fraction(rnd.randint(5, 95), 100) if v == -1 else Fraction(v) for v in s]


def sample(config, rnd):
    """List of (point, status) samples representing the zero set.
    A segment is represented by its two endpoints and an interior point."""
    pts = []
    for z in config:
        if z[0] == 'P':
            pts.append((rand_point(z[1], rnd), z[1]))
        else:
            _, j, c, a, b = z
            pa, pb = rand_point(a, rnd), rand_point(b, rnd)
            t = Fraction(rnd.randint(20, 80), 100)
            mid = [pa[i] * t + pb[i] * (1 - t) for i in range(3)]
            st = tuple(c if i == j else -1 for i in range(3))
            pts += [(pa, a), (pb, b), (mid, st)]
    return pts


def rank(rows):
    M = [list(r) for r in rows]
    r = 0
    ncol = len(M[0]) if M else 0
    for col in range(ncol):
        piv = None
        for i in range(r, len(M)):
            if M[i][col] != 0:
                piv = i
                break
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        for i in range(len(M)):
            if i != r and M[i][col] != 0:
                f = M[i][col] / M[r][col]
                M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        r += 1
    return r


def in_aff(points, target):
    if not points:
        return False
    if len(target) == 0:
        return True
    base = points[0]
    D = [[p[i] - base[i] for i in range(len(target))] for p in points[1:]]
    t = [target[i] - base[i] for i in range(len(target))]
    if not D:
        return all(x == 0 for x in t)
    return rank(D) == rank(D + [t])


def blocked(config, seed=0, draws=2):
    rnd = random.Random(seed)
    for _ in range(draws):
        pts = sample(config, rnd)
        for k in range(4):
            for Fr in combinations(range(3), k):
                vis = [p for p, s in pts if all(s[j] != 1 for j in range(3) if j not in Fr)]
                proj = [[p[i] for i in Fr] for p in vis]
                if not in_aff(proj, [Fraction(0)] * len(Fr)):
                    return False
    return True


def statuses_of(z):
    if z[0] == 'P':
        return [z[1]]
    _, j, c, a, b = z
    return [a, b, tuple(c if i == j else -1 for i in range(3))]


def realizable(config):
    """Necessary conditions (positive square coefficients, p(0) > 0,
    generic positions).  See note.md Section 2.4."""
    sts = []
    for z in config:
        sts += statuses_of(z)
    if (0, 0, 0) in sts:
        return False
    # two distinct zeros on a common axis-parallel line (fixed coords equal on 2 indices)
    pts = []
    for z in config:
        if z[0] == 'P':
            pts.append(z[1])
        else:
            pts += [z[3], z[4]]
    for a, b in combinations(pts, 2):
        if a == b:
            continue
        if len([j for j in range(3) if a[j] != -1 and a[j] == b[j]]) >= 2:
            return False
    for z in config:
        if z[0] == 'P' and z[1].count(-1) == 2:
            j = [i for i in range(3) if z[1][i] != -1][0]
            others = [w for w in config if w is not z and any(s[j] == z[1][j] for s in statuses_of(w))]
            if len(others) >= 2:
                return False
        if z[0] == 'S':
            _, j, c, a, b = z
            others = [w for w in config if w is not z and any(s[j] == c for s in statuses_of(w))]
            if others:
                return False
    segs = [z for z in config if z[0] == 'S']
    return len(segs) <= 1


def act_zero(z, perm):
    def a(s):
        return tuple(s[perm[i]] for i in range(3))
    if z[0] == 'P':
        return ('P', a(z[1]))
    _, j, c, s1, s2 = z
    jn = [i for i in range(3) if perm[i] == j][0]
    s1n, s2n = sorted([a(s1), a(s2)])
    return ('S', jn, c, s1n, s2n)


def canon(config):
    best = None
    for perm in permutations(range(3)):
        img = tuple(sorted((act_zero(z, perm) for z in config), key=repr))
        if best is None or repr(img) < repr(best):
            best = img
    return best


def conditions(config):
    n = 0
    for z in config:
        if z[0] == 'P':
            n += 1 + z[1].count(-1)
        else:
            n += 5
    return n


if __name__ == '__main__':
    maxpts = int(sys.argv[1])
    minimal = []
    seen = set()

    def consider(config):
        if not realizable(config):
            return
        key = canon(config)
        r = repr(key)
        if r in seen:
            return
        seen.add(r)
        ks = set(map(repr, key))
        if any(set(map(repr, m)) <= ks for m in minimal):
            return
        if not blocked(key):
            return
        minimal.append(key)
        print(len(key), conditions(key), key, flush=True)

    for k in range(1, maxpts + 1):
        for config in combinations(POINTS, k):
            consider(config)
    npts = len(minimal)
    if len(sys.argv) > 2 and sys.argv[2] == 'seg':
        for k in range(0, maxpts):
            for seg in SEGMENTS:
                for rest in combinations(POINTS, k):
                    consider((seg,) + rest)
    print('minimal blocking configurations: points only', npts, 'with one segment', len(minimal) - npts)
