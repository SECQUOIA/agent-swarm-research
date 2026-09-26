"""One-pool reduction from ETR-INV to pooling with bypass (source-terminal)
arcs and many quality attributes, plus Gurobi sanity checks.

ETR-INV instance: variable names; constraints ('add', x, y, z): x+y=z and
('inv', x, y): x*y = 1 (x = y allowed); all variables in [1/2, 2].

Construction (see results/pooling-one-pool-bypass-existential-reals.md):
  * one pool p, forced throughput B = 4 * n_s where n_s is the number of
    non-filler sources; a filler source f of quality 0 (capacity B);
  * one source s_v (capacity 2, unforced, quality-1 in attribute A_v) per
    ETR variable v, no direct arcs;
  * one auxiliary source s_t (capacity 2, forced) per pinned terminal t,
    with arcs (s_t, p) and the bypass (s_t, t); attribute A_t;
  * addition attributes A_{x+y} with quality 1 at s_x and s_y;
  * every pinned terminal t has capacity 2 and is forced; its pinned
    attributes carry equal lower/upper bounds; all other bounds are [0,1];
  * a slack terminal absorbs the remaining pool outflow.
In a saturated flow lambda_s = x_{s p} / B, y_t = B lambda_{s_t} and the
pinned attribute A at t satisfies w_A * y_t = kappa_A * 2.
"""
from fractions import Fraction as Fr
import itertools
import sys

import gurobipy as gp
from gurobipy import GRB


def build(variables, constraints):
    # Normalize: every variable must be on the attribute side of at least
    # one pinned product with an auxiliary (gives the lower bound 1/2).
    sources = []            # (name, forced, cap, direct_terminal or None)
    attributes = {}         # attr name -> dict source -> quality
    terminals = []          # (name, cap, forced, {attr: (lo, up)})
    aux_count = itertools.count()
    need_lower = set(variables)

    for v in variables:
        sources.append((f"s_{v}", False, Fr(2), None))
        attributes[f"A_{v}"] = {f"s_{v}": Fr(1)}

    def new_aux():
        k = next(aux_count)
        s = f"aux{k}"
        t = f"t{k}"
        sources.append((s, True, Fr(2), t))
        attributes[f"A_{s}"] = {s: Fr(1)}
        return s, t

    # Normalization: an addition with a repeated summand x + x = y is replaced
    # by x*u = 1, u*x' = 1, x + x' = y (so all attribute qualities are 0/1).
    norm = []
    dup = itertools.count()
    for c in constraints:
        if c[0] == 'add' and c[1] == c[2]:
            _, x, _, y = c
            k = next(dup)
            u, xc = f"u{k}", f"{x}copy{k}"
            for nv in (u, xc):
                variables = list(variables) + [nv]
                sources.append((f"s_{nv}", False, Fr(2), None))
                attributes[f"A_{nv}"] = {f"s_{nv}": Fr(1)}
                need_lower.add(nv)
            norm += [('inv', x, u), ('inv', u, xc), ('add', x, xc, y)]
        else:
            norm.append(c)
    constraints = norm
    pins = []   # (terminal, attribute, kind)
    for c in constraints:
        if c[0] == 'inv':
            _, x, y = c
            s1, t1 = new_aux()      # tau1 with x * tau1 = 1
            s2, t2 = new_aux()      # tau2 with tau1 * tau2 = 1 and y * tau2 = 1
            pins.append((t1, f"A_{x}", 'inv'))
            pins.append((t2, f"A_{s1}", 'inv'))
            pins.append((t2, f"A_{y}", 'inv'))
            need_lower.discard(x); need_lower.discard(y)
        elif c[0] == 'add':
            _, x, y, z = c
            a = f"A_{x}+{y}"
            attributes.setdefault(a, {})
            assert x != y
            attributes[a][f"s_{x}"] = Fr(1)
            attributes[a][f"s_{y}"] = Fr(1)
            s1, t1 = new_aux()
            pins.append((t1, f"A_{z}", 'add'))
            pins.append((t1, a, 'add'))
        else:
            raise ValueError(c)
    for v in sorted(need_lower):
        s1, t1 = new_aux()
        pins.append((t1, f"A_{v}", 'inv'))
    n_s = len(sources)
    B = Fr(4 * n_s)
    kappa = {'inv': Fr(1, 2 * B), 'add': Fr(1, B)}
    # terminals
    term_bounds = {}
    for (t, a, kind) in pins:
        term_bounds.setdefault(t, {})[a] = (kappa[kind], kappa[kind])
    for (s, forced, cap, t) in sources:
        if t is not None:
            terminals.append((t, Fr(2), True, term_bounds.get(t, {})))
    terminals.append(("slack", B, False, {}))
    sources.append(("filler", False, B, None))
    assert all(q in (Fr(0), Fr(1)) for qual in attributes.values() for q in qual.values())
    return dict(sources=sources, attributes=attributes, terminals=terminals, B=B, pins=pins)


def solve(inst, verbose=False, timelimit=120):
    S = inst['sources']; A = inst['attributes']; T = inst['terminals']; B = inst['B']
    m = gp.Model()
    m.Params.OutputFlag = 1 if verbose else 0
    m.Params.NonConvex = 2
    m.Params.TimeLimit = timelimit
    m.Params.FeasibilityTol = 1e-9
    m.Params.OptimalityTol = 1e-9
    xp = {s: m.addVar(lb=0, name=f"x_{s}_p") for (s, _, _, _) in S}
    xd = {s: m.addVar(lb=0, name=f"x_{s}_{t}") for (s, _, _, t) in S if t is not None}
    y = {t: m.addVar(lb=0, name=f"y_{t}") for (t, _, _, _) in T}
    w = {a: m.addVar(lb=0, ub=1, name=f"w_{a}") for a in A}
    forced_groups = []
    # sources
    for (s, forced, cap, t) in S:
        tot = xp[s] + (xd[s] if t is not None else 0)
        m.addConstr(tot <= float(cap))
        if forced:
            forced_groups.append((tot, cap))
    # pool
    X = gp.quicksum(xp.values())
    Y = gp.quicksum(y.values())
    m.addConstr(X == Y)
    m.addConstr(Y <= float(B))
    forced_groups.append((Y, B))
    for a, qual in A.items():
        m.addConstr(w[a] * Y == gp.quicksum(float(q) * xp[s] for s, q in qual.items()))
    # terminals
    direct_into = {}
    for (s, forced, cap, t) in S:
        if t is not None:
            direct_into.setdefault(t, []).append(s)
    for (t, cap, forced, bounds) in T:
        inflow = y[t] + gp.quicksum(xd[s] for s in direct_into.get(t, []))
        m.addConstr(inflow <= float(cap))
        if forced:
            forced_groups.append((inflow, cap))
        for a, qual in A.items():
            mass = w[a] * y[t] + gp.quicksum(float(qual.get(s, 0)) * xd[s] for s in direct_into.get(t, []))
            lo, up = bounds.get(a, (Fr(0), Fr(1)))
            m.addConstr(mass <= float(up) * inflow)
            m.addConstr(mass >= float(lo) * inflow)
    zeta = sum(c for _, c in forced_groups)
    m.setObjective(gp.quicksum(g for g, _ in forced_groups), GRB.MAXIMIZE)
    m.optimize()
    val = m.ObjVal if m.SolCount > 0 else None
    sol = {s: xp[s].X for s in xp} if m.SolCount > 0 else None
    try:
        bound = m.ObjBound
    except gp.GurobiError:
        bound = None
    return zeta, val, sol, bound, m.Status


STATUS_NAMES = {GRB.OPTIMAL: 'OPTIMAL', GRB.INFEASIBLE: 'INFEASIBLE',
                GRB.TIME_LIMIT: 'TIME_LIMIT', GRB.INF_OR_UNBD: 'INF_OR_UNBD',
                GRB.UNBOUNDED: 'UNBOUNDED', GRB.SUBOPTIMAL: 'SUBOPTIMAL',
                GRB.NUMERIC: 'NUMERIC', GRB.INTERRUPTED: 'INTERRUPTED'}


def classify(zeta, val, bound, status, tol=1e-6):
    """YES: incumbent meets the threshold. NO: INFEASIBLE status, or the
    maximization bound ObjBound is below the threshold by more than tol.
    OPTIMAL alone is not enough: it only certifies the default relative
    MIPGap (1e-4), which is far looser than tol. Otherwise INCONCLUSIVE."""
    if val is not None and val >= float(zeta) - tol:
        return 'YES'
    if status == GRB.INFEASIBLE:
        return 'NO'
    if bound is not None and bound < float(zeta) - tol:
        return 'NO'
    return 'INCONCLUSIVE'


def run_case(name, variables, constraints, expect):
    inst = build(variables, constraints)
    zeta, val, sol, bound, status = solve(inst)
    B = inst['B']
    print(f"case {name}: sources={len(inst['sources'])} attrs={len(inst['attributes'])} terms={len(inst['terminals'])} B={B} zeta={zeta}")
    print(f"   status={STATUS_NAMES.get(status, status)} best={val} bound={bound} threshold={float(zeta)}")
    if sol is not None:
        print("   values:", {v: round(sol[f's_{v}'], 6) for v in variables})
    verdict = classify(zeta, val, bound, status)
    print(f"   verdict: {verdict}; expected: {'YES' if expect else 'NO'}")
    return verdict == ('YES' if expect else 'NO')


if __name__ == '__main__':
    ok = True
    ok &= run_case('x*x=1', ['x'], [('inv', 'x', 'x')], True)
    ok &= run_case('x+x=y, x*y=1', ['x', 'y'], [('add', 'x', 'x', 'y'), ('inv', 'x', 'y')], True)
    ok &= run_case('x+y=z, x*y=1, z*z=1 (infeasible)', ['x', 'y', 'z'],
                   [('add', 'x', 'y', 'z'), ('inv', 'x', 'y'), ('inv', 'z', 'z')], False)
    ok &= run_case('x+x=y, y+y=z, z*z=1 (infeasible)', ['x', 'y', 'z'],
                   [('add', 'x', 'x', 'y'), ('add', 'y', 'y', 'z'), ('inv', 'z', 'z')], False)
    ok &= run_case('x+x=y, y*y=1 (x=1/2)', ['x', 'y'], [('add', 'x', 'x', 'y'), ('inv', 'y', 'y')], True)
    ok &= run_case('x+x=y, y+y=z (z=2)', ['x', 'y', 'z'], [('add', 'x', 'x', 'y'), ('add', 'y', 'y', 'z')], True)
    ok &= run_case('x+y=z, x*z=1, y*y=1 (golden)', ['x', 'y', 'z'],
                   [('add', 'x', 'y', 'z'), ('inv', 'x', 'z'), ('inv', 'y', 'y')], True)
    ok &= run_case('x*y=1, x*z=1, y+y+... y=z? (y=z forced: y+w=z,w*w... )', ['x', 'y', 'z', 'w'],
                   [('inv', 'x', 'y'), ('inv', 'x', 'z'), ('add', 'y', 'w', 'z'), ('inv', 'w', 'w')], False)
    print("ALL OK" if ok else "MISMATCH")
    sys.exit(0 if ok else 1)
