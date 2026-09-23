"""Independent brute-force check of the two degree-two hardness reductions.

For every tiny bipartite capacitated-orientation (CO) instance we

1. decide CO feasibility by enumerating all 2^|E| orientations;
2. build the Theorem 1 pooling instance (inputs out-degree 1) and the
   Theorem 2 pooling instance (outputs in-degree 1) exactly as in the
   result note's construction bullets;
3. solve each pooling instance to global optimality with Gurobi
   (NonConvex=2) and, independently, with an exact disjunctive LP
   enumeration (HiGHS): for a strict output with mu=0 and all lambda >= 0,
   constraint (7) forces every incoming term p*y to vanish, so each pool
   either sends nothing to its strict output or takes no dirty input; each
   of the 2^|L| branches is an LP;
4. check: opt == K  <=>  CO feasible, and opt >= K always.

It also brute-forces the bipartite subdivision lemma on small general
(non-bipartite, multi-edge) CO instances.

Run:  python independent_check.py
"""

import itertools
import sys

import gurobipy as gp
import numpy as np
from gurobipy import GRB
from scipy.optimize import linprog

TOL = 1e-6


# ---------------------------------------------------------------- CO ----------
def co_feasible(nv, edges, w, T):
    """edges: list of (u,v) pairs (multigraph allowed). Orientation into u or v."""
    m = len(edges)
    for bits in itertools.product((0, 1), repeat=m):
        load = [0] * nv
        for (u, v), b, we in zip(edges, bits, w):
            load[v if b else u] += we
        if all(load[i] <= T[i] for i in range(nv)):
            return True
    return False


def subdivide(nv, edges, w, T):
    edges2, w2, T2 = [], [], list(T)
    for (u, v), we in zip(edges, w):
        mid = len(T2)
        T2.append(we)
        edges2 += [(u, mid), (mid, v)]
        w2 += [we, we]
    return len(T2), edges2, w2, T2


# ------------------------------------------------------------ pooling ----------
# A pooling instance is a dict with
#   inputs: {name: (lambda, cap)}, pools: {name: cap}, outputs: {name: (mu, cap)}
#   arcs_in: {(input, pool): cost}, arcs_out: {(pool, output): cost}

def theorem1_instance(U, W, edges, w, T):
    """Inputs a_e (clean), b_e (dirty); pool l_e; outputs = vertices."""
    inst = dict(inputs={}, pools={}, outputs={}, arcs_in={}, arcs_out={})
    for v in U:
        inst["outputs"][("v", v)] = (0.0, T[v])
    for v in W:
        inst["outputs"][("v", v)] = (1.0, T[v])
    for k, ((u, wv), we) in enumerate(zip(edges, w)):
        assert u in U and wv in W
        inst["inputs"][("a", k)] = (0.0, we)
        inst["inputs"][("b", k)] = (1.0, we)
        inst["pools"][("l", k)] = we
        inst["arcs_in"][(("a", k), ("l", k))] = 1.0
        inst["arcs_in"][(("b", k), ("l", k))] = 0.0
        inst["arcs_out"][(("l", k), ("v", u))] = -2.0
        inst["arcs_out"][(("l", k), ("v", wv))] = -1.0
    return inst


def theorem2_instance(U, W, edges, w, T):
    """Inputs = vertices; pool l_e; outputs A_e (strict), B_e (lax)."""
    inst = dict(inputs={}, pools={}, outputs={}, arcs_in={}, arcs_out={})
    for v in U:
        inst["inputs"][("v", v)] = (0.0, T[v])
    for v in W:
        inst["inputs"][("v", v)] = (1.0, T[v])
    for k, ((u, wv), we) in enumerate(zip(edges, w)):
        assert u in U and wv in W
        inst["pools"][("l", k)] = we
        inst["outputs"][("A", k)] = (0.0, we)
        inst["outputs"][("B", k)] = (1.0, we)
        inst["arcs_in"][(("v", u), ("l", k))] = 1.0
        inst["arcs_in"][(("v", wv), ("l", k))] = 0.0
        inst["arcs_out"][(("l", k), ("A", k))] = -2.0
        inst["arcs_out"][(("l", k), ("B", k))] = -1.0
    return inst


_ENV = None


def solve_gurobi(inst):
    """Global optimum of the P-formulation (1)-(7) with one quality."""
    global _ENV
    if _ENV is None:
        _ENV = gp.Env(empty=True)
        _ENV.setParam("OutputFlag", 0)
        _ENV.start()
    md = gp.Model(env=_ENV)
    x = {a: md.addVar(lb=0.0, name=f"x{a}") for a in inst["arcs_in"]}
    y = {a: md.addVar(lb=0.0, name=f"y{a}") for a in inst["arcs_out"]}
    # p is free in the P-formulation; bound it loosely (any p works at t=0).
    p = {l: md.addVar(lb=-10.0, ub=10.0, name=f"p{l}") for l in inst["pools"]}
    lam = {i: inst["inputs"][i][0] for i in inst["inputs"]}
    for l, cap in inst["pools"].items():
        xin = [x[a] for a in x if a[1] == l]
        yout = [y[a] for a in y if a[0] == l]
        md.addConstr(gp.quicksum(xin) == gp.quicksum(yout))          # (1)
        md.addConstr(gp.quicksum(xin) <= cap)                         # (3)
        md.addConstr(gp.quicksum(lam[a[0]] * x[a] for a in x if a[1] == l)
                     == p[l] * gp.quicksum(xin))                      # (6)
    for i, (_, cap) in inst["inputs"].items():
        md.addConstr(gp.quicksum(x[a] for a in x if a[0] == i) <= cap)  # (2)
    for j, (mu, cap) in inst["outputs"].items():
        yin = [a for a in y if a[1] == j]
        md.addConstr(gp.quicksum(y[a] for a in yin) <= cap)              # (4)
        md.addConstr(gp.quicksum(p[a[0]] * y[a] for a in yin)
                     <= mu * gp.quicksum(y[a] for a in yin))             # (7)
    md.setObjective(gp.quicksum(c * x[a] for a, c in inst["arcs_in"].items())
                    + gp.quicksum(c * y[a] for a, c in inst["arcs_out"].items()),
                    GRB.MINIMIZE)
    md.Params.NonConvex = 2
    md.Params.MIPGap = 0.0
    md.Params.MIPGapAbs = 1e-7
    md.Params.FeasibilityTol = 1e-9
    md.Params.IntFeasTol = 1e-9
    md.optimize()
    assert md.Status == GRB.OPTIMAL, md.Status
    val = md.ObjVal
    md.dispose()
    return val


def solve_disjunctive_lp(inst):
    """Exact alternative: for each pool choose branch 0 (all outflow to
    mu=0 outputs is zero) or branch 1 (all intake with lambda>0 is zero).
    Correctness of the case split: at a mu=0 output, all incoming p*y terms
    are >= 0 (p in [0,1] whenever the pool has flow), so each must vanish;
    p*y = 0 with y>0 means p=0 means no dirty intake. In branch 1 p=0 and (7)
    is trivially satisfied wherever this pool sends flow; in branch 0 the
    pool only feeds mu=1 outputs where (7) holds since p<=1. Hence every
    remaining constraint is linear."""
    xin_keys = list(inst["arcs_in"])
    yout_keys = list(inst["arcs_out"])
    nx, ny = len(xin_keys), len(yout_keys)
    n = nx + ny
    c = np.array([inst["arcs_in"][a] for a in xin_keys]
                 + [inst["arcs_out"][a] for a in yout_keys])
    A_eq, b_eq, A_ub, b_ub = [], [], [], []
    for l, cap in inst["pools"].items():
        row = np.zeros(n)
        for k, a in enumerate(xin_keys):
            if a[1] == l:
                row[k] = 1
        for k, a in enumerate(yout_keys):
            if a[0] == l:
                row[nx + k] = -1
        A_eq.append(row)
        b_eq.append(0.0)
        row = np.zeros(n)
        for k, a in enumerate(xin_keys):
            if a[1] == l:
                row[k] = 1
        A_ub.append(row)
        b_ub.append(cap)
    for i, (_, cap) in inst["inputs"].items():
        row = np.zeros(n)
        for k, a in enumerate(xin_keys):
            if a[0] == i:
                row[k] = 1
        A_ub.append(row)
        b_ub.append(cap)
    for j, (_, cap) in inst["outputs"].items():
        row = np.zeros(n)
        for k, a in enumerate(yout_keys):
            if a[1] == j:
                row[nx + k] = 1
        A_ub.append(row)
        b_ub.append(cap)
    pools = list(inst["pools"])
    best = np.inf
    for branch in itertools.product((0, 1), repeat=len(pools)):
        ub = np.full(n, np.inf)
        for l, b in zip(pools, branch):
            if b == 0:
                for k, a in enumerate(yout_keys):
                    if a[0] == l and inst["outputs"][a[1]][0] == 0.0:
                        ub[nx + k] = 0.0
            else:
                for k, a in enumerate(xin_keys):
                    if a[1] == l and inst["inputs"][a[0]][0] > 0.0:
                        ub[k] = 0.0
        res = linprog(c, A_ub=np.array(A_ub), b_ub=b_ub, A_eq=np.array(A_eq),
                      b_eq=b_eq, bounds=list(zip(np.zeros(n), ub)),
                      method="highs")
        assert res.status == 0, res.message
        best = min(best, res.fun)
    return best


# ---------------------------------------------------------------- main ---------
def bipartite_instances(max_u=2, max_w=2, max_edges=3, weights=(1, 2),
                        caps=(0, 1, 2, 3)):
    for nu in range(1, max_u + 1):
        for nw in range(1, max_w + 1):
            U = list(range(nu))
            W = list(range(nu, nu + nw))
            pairs = [(u, wv) for u in U for wv in W]
            for m in range(1, max_edges + 1):
                if nu + nw == 4 and m == 3:
                    continue  # keep the Gurobi workload to a few minutes
                for edges in itertools.combinations_with_replacement(pairs, m):
                    for w in itertools.product(weights, repeat=m):
                        for T in itertools.product(caps, repeat=nu + nw):
                            yield U, W, list(edges), list(w), list(T)


def main():
    n_inst = n_yes = 0
    max_gap_no = np.inf
    failures = []
    for U, W, edges, w, T in bipartite_instances():
        n_inst += 1
        K = -sum(w)
        feas = co_feasible(len(T), edges, w, T)
        n_yes += feas
        for name, build in (("T1", theorem1_instance), ("T2", theorem2_instance)):
            inst = build(U, W, edges, w, T)
            g = solve_gurobi(inst)
            d = solve_disjunctive_lp(inst)
            ok = (abs(g - d) <= 1e-5) and (g >= K - TOL) and ((g <= K + TOL) == feas)
            if not feas:
                max_gap_no = min(max_gap_no, g - K)
            if not ok:
                failures.append((name, U, W, edges, w, T, K, feas, g, d))
        if n_inst % 200 == 0:
            print(f"  {n_inst} instances checked, {len(failures)} failures",
                  flush=True)
    print(f"bipartite CO instances: {n_inst} (feasible: {n_yes})")
    print(f"smallest opt-K over infeasible instances: {max_gap_no}")
    print(f"failures: {len(failures)}")
    for f in failures[:20]:
        print("  FAIL", f)

    # Subdivision lemma on general multigraphs (up to 3 vertices, 3 edges).
    n_sub = n_sub_fail = 0
    for nv in (2, 3):
        pairs = [(u, v) for u in range(nv) for v in range(u + 1, nv)]
        for m in range(1, 4):
            for edges in itertools.combinations_with_replacement(pairs, m):
                for w in itertools.product((1, 2), repeat=m):
                    for T in itertools.product((0, 1, 2, 3), repeat=nv):
                        n_sub += 1
                        a = co_feasible(nv, list(edges), list(w), list(T))
                        b = co_feasible(*subdivide(nv, list(edges), list(w), list(T)))
                        if a != b:
                            n_sub_fail += 1
                            print("  SUBDIVISION FAIL", edges, w, T, a, b)
    print(f"subdivision lemma: {n_sub} instances, {n_sub_fail} failures")
    return 0 if not failures and not n_sub_fail else 1


if __name__ == "__main__":
    sys.exit(main())
