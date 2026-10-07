"""R4: sanity checks of the multicolored-clique reduction of Appendix app:lbproduct.

(1) Brute force for k = 2 (one pair, the clique is one edge): Phi = 0 exactly at
    the encodings, Psi_w is integral, the minimizer is unique when the minimum
    edge weight is unique, OPT <= W0 - 1, every point with Phi >= 1 has
    Psi_w >= W0, and the growth constant 1/(n_v N^2) is valid.
(2) For random k = 3, 4 instances: the stated decomposition is a tree
    decomposition (every term in a bag, running intersection), its maximum bag
    size, and the diagonal-Hessian bound W0 (2 + 4 N^2 + 2k).
"""
from itertools import product, combinations
import random


def build(k, N, R, w):
    """Return variables (name, lo, hi), terms (list of (coef-dict-linear, const) squares),
    linear tie-break, and bags."""
    nR = sum(len(v) for v in R.values())
    W0 = 1 + (k * (k - 1) // 2) * 2 * nR
    var = {}
    for c in range(1, k + 1):
        var[("x", c)] = (1, N)
    squares = []  # (dict var->coef, const) meaning (sum coef*var + const)^2, times W0
    linear = {}
    bags = [frozenset(("x", c) for c in range(1, k + 1))]
    edges = []  # tree edges as (i, j) bag indices
    for (c, d), lst in R.items():
        m = len(lst)
        for l in range(1, m + 1):
            for nm in ("z", "S"):
                var[(nm, c, d, l)] = (0, 1)
            for nm in ("A", "B"):
                var[(nm, c, d, l)] = (0, N)
        def V(nm, l):
            return None if l == 0 else (nm, c, d, l)
        for l in range(1, m + 1):
            al, bl = lst[l - 1]
            for nm, coef in (("S", 1), ("A", al), ("B", bl)):
                t = {V(nm, l): 1, ("z", c, d, l): -coef}
                if l > 1:
                    t[V(nm, l - 1)] = t.get(V(nm, l - 1), 0) - 1
                squares.append((t, 0))
            linear[("z", c, d, l)] = w[(c, d, l)]
        if m >= 1:
            squares.append(({V("S", m): 1}, -1))
            squares.append(({V("A", m): 1, ("x", c): -1}, 0))
            squares.append(({V("B", m): 1, ("x", d): -1}, 0))
        else:
            squares.append(({}, -1))
            squares.append(({("x", c): -1}, 0))
            squares.append(({("x", d): -1}, 0))
        pb = frozenset([("x", c), ("x", d)] + ([V("S", m), V("A", m), V("B", m)] if m else []))
        bags.append(pb)
        edges.append((0, len(bags) - 1))
        prev = len(bags) - 1
        for l in range(m, 0, -1):
            b = set([("z", c, d, l), V("S", l), V("A", l), V("B", l)])
            if l > 1:
                b |= {V("S", l - 1), V("A", l - 1), V("B", l - 1)}
            bags.append(frozenset(b))
            edges.append((prev, len(bags) - 1))
            prev = len(bags) - 1
    return var, squares, linear, bags, edges, W0


def check_decomposition(var, squares, linear, bags, edges):
    for t, _ in squares:
        sc = set(t)
        assert any(sc <= b for b in bags), sc
    for v in linear:
        assert any(v in b for b in bags)
    adj = {i: set() for i in range(len(bags))}
    for i, j in edges:
        adj[i].add(j)
        adj[j].add(i)
    for v in var:
        nodes = {i for i, b in enumerate(bags) if v in b}
        assert nodes
        start = next(iter(nodes))
        seen, stack = {start}, [start]
        while stack:
            u = stack.pop()
            for x in adj[u]:
                if x in nodes and x not in seen:
                    seen.add(x)
                    stack.append(x)
        assert seen == nodes, v
    return max(len(b) for b in bags)


def diag_hessian(var, squares, W0):
    diag = {v: 0 for v in var}
    for t, _ in squares:
        for v, c in t.items():
            diag[v] += 2 * c * c * W0
    return max(diag.values())


def random_instance(k, N, p, rng):
    R = {}
    for c, d in combinations(range(1, k + 1), 2):
        R[(c, d)] = [(a, b) for a in range(1, N + 1) for b in range(1, N + 1) if rng.random() < p]
    nR = sum(len(v) for v in R.values())
    w = {(c, d, l): rng.randint(1, 2 * nR) for (c, d), lst in R.items() for l in range(1, len(lst) + 1)}
    return R, w


def brute_k2(rng):
    N = 2
    for trial in range(30):
        R, w = random_instance(2, N, 0.6, rng)
        lst = R[(1, 2)]
        if not lst or len(lst) > 3:
            continue
        var, squares, linear, bags, edges, W0 = build(2, N, R, w)
        names = list(var)
        ranges = [range(var[v][0], var[v][1] + 1) for v in names]
        vals = []
        for pt in product(*ranges):
            a = dict(zip(names, pt))
            Phi = sum((sum(c * a[v] for v, c in t.items()) + k0) ** 2 for t, k0 in squares)
            tie = sum(cw * a[v] for v, cw in linear.items())
            vals.append((W0 * Phi + tie, Phi, pt))
        vals.sort()
        OPT = vals[0][0]
        enc = [x for x in vals if x[1] == 0]
        assert len(enc) == len(lst)  # one encoding per edge (clique)
        for val, Phi, pt in vals:
            if Phi >= 1:
                assert val >= W0
        assert OPT <= W0 - 1
        wmin = min(w[(1, 2, l)] for l in range(1, len(lst) + 1))
        unique_w = sum(1 for l in range(1, len(lst) + 1) if w[(1, 2, l)] == wmin) == 1
        if unique_w:
            assert vals[1][0] > OPT
            nv = len(names)
            zs = vals[0][2]
            for val, Phi, pt in vals:
                d2 = sum((p - q) ** 2 for p, q in zip(pt, zs))
                assert (val - OPT) * nv * N * N >= d2
    print("k=2 brute force: encoding, integrality, W0 gap, uniqueness and growth OK")


if __name__ == "__main__":
    rng = random.Random(7)
    brute_k2(rng)
    for k in (3, 4, 8):
        for N in (2, 3):
            R, w = random_instance(k, N, 0.5, rng)
            var, squares, linear, bags, edges, W0 = build(k, N, R, w)
            p = check_decomposition(var, squares, linear, bags, edges)
            dh = diag_hessian(var, squares, W0)
            nv = len(var)
            assert p <= max(k, 7)
            assert dh <= W0 * (2 + 4 * N * N + 2 * k)
            assert nv <= k + 2 * k * k * N * N
            print(f"k={k} N={N}: decomposition valid, p={p} (<= max(k,7)), max diag={dh} <= {W0*(2+4*N*N+2*k)}, n_v={nv}")
