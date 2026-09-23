"""Random one-quality pooling instances with ALL degrees at most two, solved to
global optimality with Gurobi (NonConvex=2), to test structural conjectures.

Instance generator: the input-pool graph and the pool-output graph are each a
random disjoint union of paths and cycles (every vertex of degree <= 2).
Data: input qualities lambda in {0, 1/4, 1/2, 3/4, 1}, output bounds mu in the
same set, capacities in {1, 2, 3}, input-arc costs in {0, 1, 2}, output-arc
costs in {-1, ..., -4}.

For each instance we record, for every pool with positive throughput at the
returned optimal point:
  (a) whether its quality equals one of its input qualities ("pure");
  (b) whether its quality equals an input quality or the bound mu of one of
      its outputs ("at a breakpoint");
and we also solve the "pure-pattern" restriction (each pool takes flow from at
most one input, enforced with binaries) and compare its optimum with the
global optimum.  Since Gurobi returns one optimal point, (a)/(b) failing at
the returned point does not by itself prove that no optimal point has the
property; we therefore also re-solve with the breakpoint restriction imposed
on every pool (quality restricted, per pool, to the finite set of its input
values and adjacent output bounds, via binaries) and compare optimal values.

Run: conda activate minlp-notes; python random_degree_two.py [seed] [trials]
"""
import random
import sys

import gurobipy as gp
from gurobipy import GRB

TOL = 1e-6
Q = [0, 0.25, 0.5, 0.75, 1]


def random_degree_two_bipartite(rng, left, right, edges_target):
    """Random bipartite graph on left x right with all degrees <= 2, connected
    components paths/cycles, about edges_target edges; returns a list of pairs."""
    deg_l = {u: 0 for u in left}
    deg_r = {v: 0 for v in right}
    edges = set()
    cand = [(u, v) for u in left for v in right]
    rng.shuffle(cand)
    for u, v in cand:
        if len(edges) >= edges_target:
            break
        if deg_l[u] < 2 and deg_r[v] < 2:
            edges.add((u, v))
            deg_l[u] += 1
            deg_r[v] += 1
    return sorted(edges)


def random_instance(rng):
    nl = rng.randint(2, 6)
    ni = rng.randint(2, nl + 1)
    nj = rng.randint(2, nl + 1)
    L = [('l', k) for k in range(nl)]
    I = [('i', k) for k in range(ni)]
    J = [('j', k) for k in range(nj)]
    ain = random_degree_two_bipartite(rng, I, L, rng.randint(nl, 2 * nl))
    aout = random_degree_two_bipartite(rng, L, J, rng.randint(nl, 2 * nl))
    inputs = {i: (rng.choice(Q), rng.randint(1, 3)) for i in I}
    pools = {l: rng.randint(1, 3) for l in L}
    outputs = {j: (rng.choice(Q), rng.randint(1, 3)) for j in J}
    arcs_in = {a: rng.randint(0, 2) for a in ain}
    arcs_out = {a: -rng.randint(1, 4) for a in aout}
    return inputs, pools, outputs, arcs_in, arcs_out


def solve(inputs, pools, outputs, arcs_in, arcs_out, mode='global'):
    """mode: 'global', 'pure' (each pool takes from <= 1 input), 'breakpoint'
    (each pool quality restricted to its input values and adjacent mu's)."""
    m = gp.Model()
    m.Params.OutputFlag = 0
    m.Params.NonConvex = 2
    m.Params.MIPGap = 0
    m.Params.FeasibilityTol = 1e-9
    m.Params.IntFeasTol = 1e-9
    m.Params.OptimalityTol = 1e-9
    x = {a: m.addVar(lb=0, obj=c) for a, c in arcs_in.items()}
    y = {a: m.addVar(lb=0, obj=c) for a, c in arcs_out.items()}
    p = {l: m.addVar(lb=0, ub=1) for l in pools}
    t = {l: m.addVar(lb=0, ub=cap) for l, cap in pools.items()}
    for l, cap in pools.items():
        ins = [a for a in arcs_in if a[1] == l]
        outs = [a for a in arcs_out if a[0] == l]
        m.addConstr(gp.quicksum(x[a] for a in ins) == t[l])
        m.addConstr(gp.quicksum(y[a] for a in outs) == t[l])
        m.addConstr(gp.quicksum(inputs[a[0]][0] * x[a] for a in ins) == p[l] * t[l])
        if mode == 'pure' and len(ins) >= 2:
            z = [m.addVar(vtype=GRB.BINARY) for _ in ins]
            m.addConstr(gp.quicksum(z) <= 1)
            for a, zz in zip(ins, z):
                m.addConstr(x[a] <= cap * zz)
        if mode == 'breakpoint' and len(ins) >= 2:
            vals = sorted({inputs[a[0]][0] for a in ins} | {outputs[a[1]][0] for a in outs})
            lo, hi = min(inputs[a[0]][0] for a in ins), max(inputs[a[0]][0] for a in ins)
            vals = [v for v in vals if lo <= v <= hi]
            z = [m.addVar(vtype=GRB.BINARY) for _ in vals]
            m.addConstr(gp.quicksum(z) == 1)
            m.addConstr(p[l] == gp.quicksum(v * zz for v, zz in zip(vals, z)))
    for i, (lam, cap) in inputs.items():
        m.addConstr(gp.quicksum(x[a] for a in arcs_in if a[0] == i) <= cap)
    for j, (mu, cap) in outputs.items():
        ins = [a for a in arcs_out if a[1] == j]
        m.addConstr(gp.quicksum(y[a] for a in ins) <= cap)
        m.addConstr(gp.quicksum(p[a[0]] * y[a] for a in ins) <= mu * gp.quicksum(y[a] for a in ins))
    m.ModelSense = GRB.MINIMIZE
    m.optimize()
    assert m.Status == GRB.OPTIMAL, m.Status
    return m.ObjVal, {l: (p[l].X, t[l].X) for l in pools}


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    rng = random.Random(seed)
    stats = dict(instances=0, nontrivial=0, active_pools=0, pure_pools=0, bp_pools=0,
                 pure_pattern_exact=0, breakpoint_exact=0, pure_gap_max=0.0, bp_gap_max=0.0)
    examples = []
    for trial in range(trials):
        inst = random_instance(rng)
        inputs, pools, outputs, arcs_in, arcs_out = inst
        opt, sol = solve(*inst)
        stats['instances'] += 1
        if opt > -TOL:
            continue
        stats['nontrivial'] += 1
        for l, (pv, tv) in sol.items():
            if tv <= 1e-7:
                continue
            ins = [inputs[a[0]][0] for a in arcs_in if a[1] == l]
            mus = [outputs[a[1]][0] for a in arcs_out if a[0] == l]
            stats['active_pools'] += 1
            pure = any(abs(pv - v) <= 1e-6 for v in ins)
            bp = pure or any(abs(pv - v) <= 1e-6 for v in mus)
            stats['pure_pools'] += pure
            stats['bp_pools'] += bp
        opt_pure, _ = solve(*inst, mode='pure')
        opt_bp, _ = solve(*inst, mode='breakpoint')
        assert opt_pure >= opt - 1e-6 and opt_bp >= opt - 1e-6
        gap_pure = opt_pure - opt
        gap_bp = opt_bp - opt
        stats['pure_pattern_exact'] += gap_pure <= 1e-6
        stats['breakpoint_exact'] += gap_bp <= 1e-6
        stats['pure_gap_max'] = max(stats['pure_gap_max'], gap_pure)
        stats['bp_gap_max'] = max(stats['bp_gap_max'], gap_bp)
        if gap_bp > 1e-6 and len(examples) < 3:
            examples.append((trial, opt, opt_pure, opt_bp, inst, sol))
        print(f"trial {trial}: |I|={len(inputs)} |L|={len(pools)} |J|={len(outputs)} "
              f"opt={opt:.4f} pure={opt_pure:.4f} breakpoint={opt_bp:.4f}")
    print('summary', stats)
    for ex in examples:
        trial, opt, opt_pure, opt_bp, inst, sol = ex
        print(f"\nexample trial {trial}: opt={opt:.6f} pure-pattern={opt_pure:.6f} breakpoint={opt_bp:.6f}")
        inputs, pools, outputs, arcs_in, arcs_out = inst
        print(' inputs', inputs)
        print(' pools', pools)
        print(' outputs', outputs)
        print(' arcs_in', arcs_in)
        print(' arcs_out', arcs_out)
        print(' optimal (p, t)', {l: (round(v[0], 6), round(v[1], 6)) for l, v in sol.items()})


if __name__ == '__main__':
    main()
