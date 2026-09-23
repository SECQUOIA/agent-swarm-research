"""Reduction from ETR-INV to the Pooling Problem (Haugland 2016 model) and
numerical sanity checks with Gurobi.

ETR-INV instance: variables (names), constraints of the forms
  ('add', x, y, z)  meaning x + y = z
  ('inv', x, y)     meaning x * y = 1
with all variables implicitly bounded to [1/2, 2].

Pooling model (no source-terminal arcs, node capacities, one quality
attribute with source qualities in {0,1}, lower and upper terminal quality
bounds, arc costs; decision: profit >= zeta).

The build follows results/pooling-existential-theory-of-reals.md.
"""
from fractions import Fraction as Fr
import itertools
import sys

import gurobipy as gp
from gurobipy import GRB


class Pooling:
    def __init__(self):
        self.sources = {}   # name -> dict(cap, quality, forced)
        self.pools = {}     # name -> dict(cap, forced)
        self.terms = {}     # name -> dict(cap, forced, lo, up)
        self.arcs = set()   # (u, v)

    def source(self, name, cap, quality, forced=False):
        assert name not in self.sources
        self.sources[name] = dict(cap=Fr(cap), q=Fr(quality), forced=forced)
        return name

    def pool(self, name, cap, forced=False):
        assert name not in self.pools
        self.pools[name] = dict(cap=Fr(cap), forced=forced)
        return name

    def term(self, name, cap, forced=False, lo=Fr(0), up=Fr(1)):
        assert name not in self.terms
        self.terms[name] = dict(cap=Fr(cap), forced=forced, lo=Fr(lo), up=Fr(up))
        return name

    def arc(self, u, v):
        assert (u in self.sources and v in self.pools) or (u in self.pools and v in self.terms), (u, v)
        assert (u, v) not in self.arcs
        self.arcs.add((u, v))

    def zeta(self):
        z = Fr(0)
        for d in (self.sources, self.pools, self.terms):
            for n, info in d.items():
                if info['forced']:
                    z += info['cap']
        return z

    def cost(self, u, v):
        """cost coefficient = -(number of forced groups containing the arc)."""
        c = 0
        if u in self.sources and self.sources[u]['forced']:
            c += 1
        if u in self.pools and self.pools[u]['forced']:
            c += 1
        if v in self.terms and self.terms[v]['forced']:
            c += 1
        return -c


def build(variables, constraints, B=None):
    """Build the pooling instance. Returns (Pooling, info)."""
    # count emissions needed per pool type to choose B
    need = {v: dict(P=0, Pbar=0, R=0, Rbar=0) for v in variables}
    for c in constraints:
        if c[0] == 'inv':
            _, x, y = c
            need[x]['P'] += 1        # pinned emission from P_x
            need[y]['Rbar'] += 1     # copy of 5/2 - y
        elif c[0] == 'add':
            _, x, y, z = c
            need[x]['R'] += 1        # copy of x
            need[y]['R'] += 1        # copy of y
            need[z]['Rbar'] += 1     # emission of 5/2 - z at the addition terminal
        else:
            raise ValueError(c)
    for v in variables:
        # each R_v / Rbar_v needs one feeding emission from P_v / Pbar_v;
        # ensure at least one emission from P_v and Pbar_v (range enforcement)
        need[v]['P'] += 1       # emission feeding R_v (always created)
        need[v]['Pbar'] += 1    # emission feeding Rbar_v (always created)
    M = max(max(d.values()) for d in need.values())
    if B is None:
        B = 2 * M + 3
    B = Fr(B)
    P = Pooling()
    BIG = B   # diluent sources and slack terminals have capacity B
    counter = itertools.count()

    def fresh(prefix):
        return f"{prefix}{next(counter)}"

    def emission(pool, mu_value, cap=Fr(2), relay_quality=0):
        """Forced terminal t (cap) with inflow from `pool` pinned to value e by
        mass = mu * cap, plus a quality-0 relay pool p' carrying cap - e, fed
        by a forced quality-0 source s' (cap) whose other arc delivers e as a
        quality-0 source arc.  If relay_quality == 1, a second relay stage
        (vacuous terminal) converts the delivered arc to a quality-1 source
        arc.  Returns the source name whose free arc carries e; the caller
        attaches that arc."""
        t = P.term(fresh('te'), cap, forced=True, lo=mu_value, up=mu_value)
        P.arc(pool, t)
        pr = P.pool(fresh('pr'), cap)
        P.arc(pr, t)
        sr = P.source(fresh('sr'), cap, 0, forced=True)
        P.arc(sr, pr)
        if relay_quality == 0:
            return sr
        # quality flip: sr -> p2 -> t2 (forced, vacuous bounds) <- pr2 <- s2 (quality 1)
        p2 = P.pool(fresh('pf'), cap)
        P.arc(sr, p2)
        t2 = P.term(fresh('tf'), cap, forced=True)
        P.arc(p2, t2)
        pr2 = P.pool(fresh('pr'), cap)
        P.arc(pr2, t2)
        s2 = P.source(fresh('sr'), cap, 1, forced=True)
        P.arc(s2, pr2)
        return s2

    # per-variable structure
    S = {}
    Pz, Pbar, R, Rbar = {}, {}, {}, {}
    slack = {}
    for v in variables:
        S[v] = P.source(f"s_{v}", Fr(5, 2), 1, forced=True)
        Pz[v] = P.pool(f"P_{v}", B, forced=True)
        Pbar[v] = P.pool(f"Pbar_{v}", B, forced=True)
        P.arc(S[v], Pz[v]); P.arc(S[v], Pbar[v])
        for p in (Pz[v], Pbar[v]):
            d = P.source(fresh('d'), BIG, 0)
            P.arc(d, p)
            sl = P.term(fresh('slack'), BIG)
            P.arc(p, sl)
        # inverse pools (always created, as in the text): R_v gets a copy of
        # 1/v as a quality-1 source arc and emits copies of v
        if True:
            R[v] = P.pool(f"R_{v}", B, forced=True)
            sr = emission(Pz[v], Fr(1, 2 * B), relay_quality=1)   # e = 1/v
            P.arc(sr, R[v])
            d = P.source(fresh('d'), BIG, 0); P.arc(d, R[v])
            sl = P.term(fresh('slack'), BIG); P.arc(R[v], sl)
        if True:
            Rbar[v] = P.pool(f"Rbar_{v}", B, forced=True)
            sr = emission(Pbar[v], Fr(1, 2 * B), relay_quality=1)  # e = 1/(5/2 - v)
            P.arc(sr, Rbar[v])
            d = P.source(fresh('d'), BIG, 0); P.arc(d, Rbar[v])
            sl = P.term(fresh('slack'), BIG); P.arc(Rbar[v], sl)
    # constraints
    for c in constraints:
        if c[0] == 'inv':
            _, x, y = c
            # copy of 5/2 - y as a quality-0 source arc
            sr = emission(Rbar[y], Fr(1, 2 * B), relay_quality=0)   # e = 5/2 - y (mass (1/((5/2-y)B)) e = 1/B)
            pr = P.pool(fresh('pc'), Fr(5, 2))
            P.arc(sr, pr)
            t = P.term(fresh('tinv'), Fr(5, 2), forced=True, lo=Fr(2, 5 * B), up=Fr(2, 5 * B))
            P.arc(pr, t)
            P.arc(Pz[x], t)
        else:
            _, x, y, z = c
            padd = P.pool(fresh('padd'), Fr(4))
            for w in (x, y):
                sr = emission(R[w], Fr(1, 2 * B), relay_quality=0)   # e = w
                P.arc(sr, padd)
            t = P.term(fresh('tadd'), Fr(5, 2), forced=True, lo=Fr(2, 5 * B), up=Fr(2, 5 * B))
            P.arc(padd, t)
            P.arc(Rbar[z], t)   # emitted 5/2 - z, pinned by mass with padd as diluent
    return P, dict(B=B, S=S, Pz=Pz, Pbar=Pbar, R=R, Rbar=Rbar)


def solve(P, verbose=False, timelimit=60):
    m = gp.Model()
    m.Params.OutputFlag = 1 if verbose else 0
    m.Params.NonConvex = 2
    m.Params.TimeLimit = timelimit
    m.Params.FeasibilityTol = 1e-9
    m.Params.IntFeasTol = 1e-9
    m.Params.OptimalityTol = 1e-9
    x = {a: m.addVar(lb=0, name=f"x_{a[0]}_{a[1]}") for a in P.arcs}
    w = {p: m.addVar(lb=0, ub=1, name=f"w_{p}") for p in P.pools}
    outs = {n: [a for a in P.arcs if a[0] == n] for n in list(P.sources) + list(P.pools)}
    ins = {n: [a for a in P.arcs if a[1] == n] for n in list(P.pools) + list(P.terms)}
    for s, info in P.sources.items():
        m.addConstr(gp.quicksum(x[a] for a in outs[s]) <= float(info['cap']))
    for p, info in P.pools.items():
        X = gp.quicksum(x[a] for a in outs[p])
        m.addConstr(gp.quicksum(x[a] for a in ins[p]) == X)
        m.addConstr(X <= float(info['cap']))
        m.addConstr(w[p] * X == gp.quicksum(float(P.sources[a[0]]['q']) * x[a] for a in ins[p]))
    for t, info in P.terms.items():
        X = gp.quicksum(x[a] for a in ins[t])
        m.addConstr(X <= float(info['cap']))
        mass = gp.quicksum(w[a[0]] * x[a] for a in ins[t])
        m.addConstr(mass <= float(info['up']) * X)
        m.addConstr(mass >= float(info['lo']) * X)
    profit = gp.quicksum(-P.cost(*a) * x[a] for a in P.arcs)
    m.setObjective(profit, GRB.MAXIMIZE)
    m.optimize()
    assert m.Status == GRB.OPTIMAL, f"Gurobi status {m.Status}: verdict not certified"
    val = m.ObjVal
    sol = {a: x[a].X for a in P.arcs}
    return m.Status, val, sol, m.ObjBound


def run_case(name, variables, constraints, expect_feasible):
    P, info = build(variables, constraints)
    zeta = P.zeta()
    status, val, sol, bound = solve(P)
    print(f"case {name}: |S|={len(P.sources)} |P|={len(P.pools)} |T|={len(P.terms)} |A|={len(P.arcs)} B={info['B']} zeta={zeta}")
    print(f"   gurobi status={status} best={val} bound={bound}")
    if sol is not None:
        vals = {v: sol[(info['S'][v], info['Pz'][v])] for v in variables}
        print("   variable values:", {v: round(t, 6) for v, t in vals.items()})
    feasible = val is not None and val >= float(zeta) - 1e-6
    print(f"   threshold reached: {feasible}; expected feasible: {expect_feasible}")
    return feasible == expect_feasible


if __name__ == '__main__':
    ok = True
    ok &= run_case('x*x=1', ['x'], [('inv', 'x', 'x')], True)
    ok &= run_case('x+x=y, x*y=1 (x=1/sqrt2)', ['x', 'y'], [('add', 'x', 'x', 'y'), ('inv', 'x', 'y')], True)
    ok &= run_case('x+y=z, x*y=1, z*z=1 (infeasible)', ['x', 'y', 'z'],
                   [('add', 'x', 'y', 'z'), ('inv', 'x', 'y'), ('inv', 'z', 'z')], False)
    ok &= run_case('x+x=y, y+y=z, z*z=1 (infeasible: z=1 forces x=1/4)', ['x', 'y', 'z'],
                   [('add', 'x', 'x', 'y'), ('add', 'y', 'y', 'z'), ('inv', 'z', 'z')], False)
    ok &= run_case('x+x=y, y*y=1 (x=1/2 boundary)', ['x', 'y'],
                   [('add', 'x', 'x', 'y'), ('inv', 'y', 'y')], True)
    ok &= run_case('x+x=y, y+y=z (x=1/2,y=1,z=2 boundary)', ['x', 'y', 'z'],
                   [('add', 'x', 'x', 'y'), ('add', 'y', 'y', 'z')], True)
    ok &= run_case('x+y=z, x*z=1, y*y=1 (x+1=z, x z=1 -> x=(sqrt5-1)/2)', ['x', 'y', 'z'],
                   [('add', 'x', 'y', 'z'), ('inv', 'x', 'z'), ('inv', 'y', 'y')], True)
    print("ALL OK" if ok else "MISMATCH")
    sys.exit(0 if ok else 1)
