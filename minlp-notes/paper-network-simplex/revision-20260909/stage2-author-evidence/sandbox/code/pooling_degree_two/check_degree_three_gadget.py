"""Brute-force check of Lemma 2 (degree-three capacitated orientation).

For every small At-most-3-SAT(2L) formula (each literal at most twice, clauses
of size 1..3) we build the graph of Asahiro et al. with the special gadget
replaced by vertex-disjoint triangles of weight-2 edges, each triangle vertex
receiving at most one clause edge, weights: literal edges 2, triangle edges 2,
clause edges 1, capacity T=2 everywhere (in-load version).  We check that the
maximum degree is 3 and that an orientation with in-load <= 2 exists iff the
formula is satisfiable.  Run: conda activate minlp-notes; python check_degree_three_gadget.py
"""
import itertools
import random


def build(nvars, clauses):
    # vertices: ('lit', v, s) for literal v (s=0 positive, s=1 negative); ('cl', j); ('sp', j, i)
    V, E = [], []
    for v in range(nvars):
        V += [('lit', v, 0), ('lit', v, 1)]
        E.append((('lit', v, 0), ('lit', v, 1), 2))
    for j, cl in enumerate(clauses):
        V.append(('cl', j))
        for (v, s) in cl:
            E.append((('cl', j), ('lit', v, s), 1))
        pad = 3 - len(cl)
        if pad > 0:
            tri = [('sp', j, i) for i in range(3)]
            V += tri
            E += [(tri[0], tri[1], 2), (tri[1], tri[2], 2), (tri[2], tri[0], 2)]
            for i in range(pad):
                E.append((('cl', j), tri[i], 1))
    return V, E


def orientable(V, E, T=2):
    """Backtracking search for an orientation with in-load <= T everywhere."""
    idx = {v: i for i, v in enumerate(V)}
    load = [0] * len(V)
    order = sorted(range(len(E)), key=lambda k: -E[k][2])

    def rec(pos):
        if pos == len(order):
            return True
        u, v, w = E[order[pos]]
        for head in (idx[v], idx[u]):
            if load[head] + w <= T:
                load[head] += w
                if rec(pos + 1):
                    return True
                load[head] -= w
        return False

    return rec(0)


def satisfiable(nvars, clauses):
    for assign in itertools.product((0, 1), repeat=nvars):
        if all(any(assign[v] == (1 - s) for (v, s) in cl) for cl in clauses):
            return True
    return False


def random_formula(rng):
    nvars = rng.randint(1, 4)
    ncl = rng.randint(1, 6)
    count = {}
    clauses = []
    for _ in range(ncl):
        size = rng.randint(1, 3)
        lits = []
        tries = 0
        while len(lits) < size and tries < 20:
            tries += 1
            v, s = rng.randrange(nvars), rng.randint(0, 1)
            if (v, s) in lits or (v, 1 - s) in lits or count.get((v, s), 0) >= 2:
                continue
            lits.append((v, s))
            count[(v, s)] = count.get((v, s), 0) + 1
        if lits:
            clauses.append(lits)
    return nvars, clauses


def main():
    rng = random.Random(0)
    n_sat = n_unsat = 0
    fixed = [
        (1, [[(0, 0)], [(0, 1)]]),
        (2, [[(0, 0), (1, 0)], [(0, 1), (1, 0)], [(0, 0), (1, 1)], [(0, 1), (1, 1)]]),
        (2, [[(0, 0), (1, 0)], [(0, 1), (1, 0)], [(0, 0), (1, 1)]]),
        (3, [[(0, 0), (1, 0), (2, 0)], [(0, 1)], [(1, 1)], [(2, 1)]]),
        (3, [[(0, 0), (1, 0), (2, 0)], [(0, 1), (1, 1)], [(1, 0), (2, 1)], [(0, 0), (2, 1)], [(0, 1), (2, 0)]]),
    ]
    cases = fixed + [random_formula(rng) for _ in range(400)]
    for nvars, clauses in cases:
        V, E = build(nvars, clauses)
        deg = {}
        for u, v, w in E:
            deg[u] = deg.get(u, 0) + 1
            deg[v] = deg.get(v, 0) + 1
        assert max(deg.values()) <= 3, deg
        assert len({frozenset((u, v)) for u, v, w in E}) == len(E), "not simple"
        sat = satisfiable(nvars, clauses)
        ori = orientable(V, E)
        assert sat == ori, (nvars, clauses, sat, ori)
        n_sat += sat
        n_unsat += (not sat)
    print("degree-three gadget check passed:", n_sat, "satisfiable,", n_unsat, "unsatisfiable formulas")


if __name__ == '__main__':
    main()
