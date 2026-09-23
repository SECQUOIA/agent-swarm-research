"""Numerical cross-check of the one-quality pooling hardness reductions.

For random capacitated-orientation instances (multigraphs with edge weights and
vertex capacities) we build the two pooling instances of the result note
(out-degree version: private inputs, vertex outputs; in-degree version: vertex
inputs, private outputs), solve the P-formulation to global optimality with
Gurobi (NonConvex=2), and compare the optimal cost with -sum(w_e).  The claim is
that the optimum equals -sum(w_e) exactly when a feasible orientation exists,
which we check by brute force over all orientations.  Non-bipartite graphs are
first passed through the subdivision lemma, which is also checked directly.

Run: conda activate minlp-notes; python verify_reduction.py [seed] [trials]
"""
import itertools
import random
import sys

import gurobipy as gp
from gurobipy import GRB

TOL = 1e-6


def orientation_feasible(nv, edges, w, T):
    """Brute force: is there an orientation with in-load <= T at every vertex?"""
    for bits in itertools.product((0, 1), repeat=len(edges)):
        load = [0] * nv
        for k, ((u, v), b) in enumerate(zip(edges, bits)):
            load[v if b else u] += w[k]
        if all(load[i] <= T[i] for i in range(nv)):
            return True
    return False


def subdivide(nv, edges, w, T):
    """Bipartite subdivision: edge k=(u,v) -> u-m_k-v, both halves weight w_k, T(m_k)=w_k."""
    new_edges, new_w = [], []
    new_T = list(T)
    for k, (u, v) in enumerate(edges):
        m = nv + k
        new_T.append(w[k])
        new_edges += [(u, m), (m, v)]
        new_w += [w[k], w[k]]
    side = [0] * nv + [1] * len(edges)   # original vertices strict (0), midpoints lax (1)
    return nv + len(edges), new_edges, new_w, new_T, side


def solve_pooling(inputs, pools, outputs, arcs_in, arcs_out):
    """Generic P-formulation solved globally.

    inputs: dict i -> (lambda, capacity); pools: dict l -> capacity;
    outputs: dict j -> (mu, capacity); arcs_in: dict (i,l) -> cost;
    arcs_out: dict (l,j) -> cost.  Returns optimal cost (min)."""
    m = gp.Model()
    m.Params.OutputFlag = 0
    m.Params.NonConvex = 2
    m.Params.MIPGap = 0
    m.Params.FeasibilityTol = 1e-9
    m.Params.IntFeasTol = 1e-9
    m.Params.OptimalityTol = 1e-9
    x = {a: m.addVar(lb=0, obj=c) for a, c in arcs_in.items()}
    y = {a: m.addVar(lb=0, obj=c) for a, c in arcs_out.items()}
    lam_lo = min(v[0] for v in inputs.values())
    lam_hi = max(v[0] for v in inputs.values())
    p = {l: m.addVar(lb=lam_lo, ub=lam_hi) for l in pools}
    t = {l: m.addVar(lb=0, ub=cap) for l, cap in pools.items()}
    for l, cap in pools.items():
        ins = [a for a in arcs_in if a[1] == l]
        outs = [a for a in arcs_out if a[0] == l]
        m.addConstr(gp.quicksum(x[a] for a in ins) == t[l])
        m.addConstr(gp.quicksum(y[a] for a in outs) == t[l])
        m.addConstr(gp.quicksum(inputs[a[0]][0] * x[a] for a in ins) == p[l] * t[l])
    for i, (lam, cap) in inputs.items():
        m.addConstr(gp.quicksum(x[a] for a in arcs_in if a[0] == i) <= cap)
    for j, (mu, cap) in outputs.items():
        ins = [a for a in arcs_out if a[1] == j]
        m.addConstr(gp.quicksum(y[a] for a in ins) <= cap)
        m.addConstr(gp.quicksum(p[a[0]] * y[a] for a in ins) <= mu * gp.quicksum(y[a] for a in ins))
    m.ModelSense = GRB.MINIMIZE
    m.optimize()
    assert m.Status == GRB.OPTIMAL, m.Status
    return m.ObjVal


def build_outdegree_version(nv, edges, w, T, side):
    """Theorem 1: inputs private (out-degree 1), pools (2,2), outputs = vertices."""
    inputs, pools, outputs, arcs_in, arcs_out = {}, {}, {}, {}, {}
    for v in range(nv):
        outputs[('v', v)] = (0 if side[v] == 0 else 1, T[v])
    for k, (u, v) in enumerate(edges):
        assert side[u] != side[v]
        s, lax = (u, v) if side[u] == 0 else (v, u)
        inputs[('a', k)] = (0, w[k])
        inputs[('b', k)] = (1, w[k])
        pools[('l', k)] = w[k]
        arcs_in[(('a', k), ('l', k))] = 1
        arcs_in[(('b', k), ('l', k))] = 0
        arcs_out[(('l', k), ('v', s))] = -2
        arcs_out[(('l', k), ('v', lax))] = -1
    return inputs, pools, outputs, arcs_in, arcs_out


def build_indegree_version(nv, edges, w, T, side):
    """Theorem 2: inputs = vertices, pools (2,2), outputs private (in-degree 1)."""
    inputs, pools, outputs, arcs_in, arcs_out = {}, {}, {}, {}, {}
    for v in range(nv):
        inputs[('v', v)] = (0 if side[v] == 0 else 1, T[v])
    for k, (u, v) in enumerate(edges):
        assert side[u] != side[v]
        s, lax = (u, v) if side[u] == 0 else (v, u)
        pools[('l', k)] = w[k]
        outputs[('A', k)] = (0, w[k])
        outputs[('B', k)] = (1, w[k])
        arcs_in[(('v', s), ('l', k))] = 1
        arcs_in[(('v', lax), ('l', k))] = 0
        arcs_out[(('l', k), ('A', k))] = -2
        arcs_out[(('l', k), ('B', k))] = -1
    return inputs, pools, outputs, arcs_in, arcs_out


def random_instance(rng, bipartite):
    if bipartite:
        nu, nw = rng.randint(1, 3), rng.randint(1, 3)
        nv = nu + nw
        side = [0] * nu + [1] * nw
        ne = rng.randint(1, 5)
        edges = [(rng.randrange(nu), nu + rng.randrange(nw)) for _ in range(ne)]
    else:
        nv = rng.randint(2, 4)
        side = None
        ne = rng.randint(1, 4)
        edges = []
        for _ in range(ne):
            u, v = rng.sample(range(nv), 2)
            edges.append((u, v))
    w = [rng.randint(1, 3) for _ in edges]
    T = [rng.randint(0, 4) for _ in range(nv)]
    return nv, edges, w, T, side


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    rng = random.Random(seed)
    stats = {'yes': 0, 'no': 0, 'subdiv': 0}
    for trial in range(trials):
        bip = rng.random() < 0.5
        nv, edges, w, T, side = random_instance(rng, bip)
        feasible = orientation_feasible(nv, edges, w, T)
        if not bip:
            nv2, edges2, w2, T2, side = subdivide(nv, edges, w, T)
            feasible2 = orientation_feasible(nv2, edges2, w2, T2)
            assert feasible == feasible2, ('subdivision lemma violated', edges, w, T)
            stats['subdiv'] += 1
            nv, edges, w, T = nv2, edges2, w2, T2
        target = -sum(w)
        for builder in (build_outdegree_version, build_indegree_version):
            opt = solve_pooling(*builder(nv, edges, w, T, side))
            assert opt >= target - TOL, (builder.__name__, opt, target)
            reached = opt <= target + TOL
            assert reached == feasible, (builder.__name__, edges, w, T, opt, target, feasible)
        stats['yes' if feasible else 'no'] += 1
        print(f"trial {trial}: |V|={nv} |E|={len(edges)} w={w} T={T} feasible={feasible} ok")
    print('summary', stats)


if __name__ == '__main__':
    main()
