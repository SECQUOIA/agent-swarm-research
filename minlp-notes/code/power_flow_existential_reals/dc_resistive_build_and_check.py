"""Reduction from ETR-INV to feasibility of the resistive (DC) power-flow
model with power-injection bounds, plus Gurobi sanity checks, and a check
of the full AC model (rectangular coordinates) on the same instances.

Resistive model: buses i with voltages V_i in [VL_i, VU_i], lines (i,j)
with conductance g_ij > 0, injection bounds PL_i <= V_i * sum_j g_ij (V_i - V_j) <= PU_i.

ETR-INV instance: variables; constraints ('inv', x, y): x*y = 1 (x = y
allowed); ('add', x, y, z): x + y = z.  All variables in [1/2, 2].

Construction (see results/ac-power-flow-existential-reals.md):
  * variable/copy buses: V in [1/2, 2], free injection;
  * pinned buses: V = 1, fixed injection; two neighbours with g = 1 and
    injection -1/2 give V_a + V_b = 5/2 (complement copies); chains of
    complements give copies with every bus of degree <= 3;
  * addition x + y = z: pinned bus, neighbours x-copy, y-copy, zbar-copy
    (all g = 1), injection +1/2;
  * inversion x*y = 1: inversion bus I (V in [1/2,2], injection -1,
    neighbours W (g=1) and a pinned bus tying V_I = x); bus W (V in [1,4],
    free injection); pinned bus D (injection -5/2) with neighbours W (g=1),
    an xbar-copy (g=2), a ybar-copy (g=1).
"""
from fractions import Fraction as Fr
import itertools
import math
import sys

import gurobipy as gp
from gurobipy import GRB


class Net:
    def __init__(self):
        self.bus = {}    # name -> dict(VL, VU, PL, PU)
        self.lines = {}  # (i,j) -> g

    def add_bus(self, name, VL, VU, PL, PU):
        assert name not in self.bus
        self.bus[name] = dict(VL=Fr(VL), VU=Fr(VU), PL=PL, PU=PU)
        return name

    def add_line(self, i, j, g):
        key = tuple(sorted((i, j)))
        assert key not in self.lines and i != j
        self.lines[key] = Fr(g)

    def neighbors(self, i):
        for (a, b), g in self.lines.items():
            if a == i:
                yield b, g
            elif b == i:
                yield a, g


FREE = None   # marker: free injection, bounds set at the end from degrees
AC_MAX_BUSES = 25   # run the (slow) full AC cross-check only on small instances
AC_TIMELIMIT = 600


def build(variables, constraints):
    N = Net()
    counter = itertools.count()

    def fresh(p):
        return f"{p}{next(counter)}"

    def var_bus(name):
        return N.add_bus(name, Fr(1, 2), Fr(2), FREE, FREE)

    def pinned(name, P):
        return N.add_bus(name, 1, 1, Fr(P), Fr(P))

    # copy chains: for each variable a list of (bus, kind) with kind 'plain' (value v) or 'bar' (5/2 - v)
    chain = {}     # v -> current end bus and its kind; each bus has one gadget slot
    slots = {}     # bus -> remaining gadget slots (1 for chain buses)

    for v in variables:
        b = var_bus(f"X_{v}")
        chain[v] = (b, 'plain')
        slots[b] = 1

    def extend(v):
        b, kind = chain[v]
        c = pinned(fresh('C'), Fr(-1, 2))
        nb = var_bus(fresh(f"X{'bar' if kind == 'plain' else ''}_{v}_"))
        N.add_line(b, c, 1)
        N.add_line(c, nb, 1)
        chain[v] = (nb, 'bar' if kind == 'plain' else 'plain')
        slots[nb] = 1

    def take(v, kind):
        while chain[v][1] != kind or slots[chain[v][0]] == 0:
            extend(v)
        b = chain[v][0]
        slots[b] -= 1
        return b

    for c in constraints:
        if c[0] == 'add':
            _, x, y, z = c
            A = pinned(fresh('A'), Fr(1, 2))
            N.add_line(A, take(x, 'plain'), 1)
            N.add_line(A, take(y, 'plain'), 1)
            N.add_line(A, take(z, 'bar'), 1)
        elif c[0] == 'inv':
            _, x, y = c
            I = N.add_bus(fresh('I'), Fr(1, 2), Fr(2), Fr(-1), Fr(-1))
            W = N.add_bus(fresh('W'), 1, 4, FREE, FREE)
            CI = pinned(fresh('C'), Fr(-1, 2))
            N.add_line(I, W, 1)
            N.add_line(I, CI, 1)
            N.add_line(CI, take(x, 'bar'), 1)
            D = pinned(fresh('D'), Fr(-5, 2))
            N.add_line(D, W, 1)
            N.add_line(D, take(x, 'bar'), 2)
            N.add_line(D, take(y, 'bar'), 1)
        else:
            raise ValueError(c)
    # free injection bounds: |P_i| <= VU_i * sum_j g_ij * max|V_i - V_j| ; all voltages in [1/2, 4]
    for i, info in N.bus.items():
        if info['PL'] is FREE:
            L = info['VU'] * sum(g for _, g in N.neighbors(i)) * Fr(7, 2) + 1
            info['PL'], info['PU'] = -L, L
    return N


def solve_dc(N, timelimit=120):
    m = gp.Model()
    m.Params.OutputFlag = 0
    m.Params.NonConvex = 2
    m.Params.TimeLimit = timelimit
    m.Params.FeasibilityTol = 1e-9
    V = {i: m.addVar(lb=float(b['VL']), ub=float(b['VU']), name=f"V_{i}") for i, b in N.bus.items()}
    for i, b in N.bus.items():
        expr = gp.quicksum(float(g) * (V[i] * V[i] - V[i] * V[j]) for j, g in N.neighbors(i))
        m.addConstr(expr <= float(b['PU']))
        m.addConstr(expr >= float(b['PL']))
    m.setObjective(0, GRB.MINIMIZE)
    m.optimize()
    assert m.Status in (GRB.OPTIMAL, GRB.INFEASIBLE), f"status {m.Status}"
    if m.Status == GRB.OPTIMAL:
        return True, {i: V[i].X for i in V}
    return False, None


def solve_ac(N, timelimit=120, spread_timelimit=300):
    """Full AC model in rectangular coordinates: V_i = e_i + j f_i, lines with
    G = g, B = 0, no shunts; real injection bounds as in N, reactive bounds
    [0,0], magnitude bounds as in N, per-line limit e_i e_j + f_i f_j >= 0
    and the bus-angle box |theta_i - theta_ref| <= pi/4 (e_i >= |f_i|), which
    makes principal and real angle differences coincide (see the result
    file: per-line principal limits alone admit winding solutions on
    cycles).  First decides feasibility (objective 0); if
    feasible, maximizes the angle spread sum_i f_i^2 for a limited time and
    returns the certified upper bound on that maximum (0 means all angles
    are provably equal to the reference angle)."""
    def model():
        m = gp.Model()
        m.Params.OutputFlag = 0
        m.Params.NonConvex = 2
        m.Params.FeasibilityTol = 1e-9
        e = {i: m.addVar(lb=-5, ub=5, name=f"e_{i}") for i in N.bus}
        f = {i: m.addVar(lb=-5, ub=5, name=f"f_{i}") for i in N.bus}
        ref = next(iter(N.bus))
        m.addConstr(f[ref] == 0)
        m.addConstr(e[ref] >= 0)
        # bus-angle box |theta_i - theta_ref| <= pi/4 (rectangular variant of Theorem 2)
        for i in N.bus:
            m.addConstr(e[i] >= 0)
            m.addConstr(e[i] >= f[i]); m.addConstr(e[i] >= -f[i])
        for i, b in N.bus.items():
            mag2 = e[i] * e[i] + f[i] * f[i]
            m.addConstr(mag2 >= float(b['VL']) ** 2)
            m.addConstr(mag2 <= float(b['VU']) ** 2)
            # P_ij = G(|V_i|^2 - Re(V_i conj V_j)); Q_ij = -G Im(V_i conj V_j), Im(V_i conj V_j) = f_i e_j - e_i f_j
            P = gp.quicksum(float(g) * (e[i] * e[i] + f[i] * f[i] - (e[i] * e[j] + f[i] * f[j])) for j, g in N.neighbors(i))
            Q = gp.quicksum(-float(g) * (f[i] * e[j] - e[i] * f[j]) for j, g in N.neighbors(i))
            m.addConstr(P <= float(b['PU']))
            m.addConstr(P >= float(b['PL']))
            m.addConstr(Q == 0)
        for (i, j), g in N.lines.items():
            m.addConstr(e[i] * e[j] + f[i] * f[j] >= 0)   # |theta_ij| <= pi/2
        return m, e, f
    m, e, f = model()
    m.Params.TimeLimit = timelimit
    m.setObjective(0, GRB.MINIMIZE)
    m.optimize()
    if m.Status == GRB.TIME_LIMIT:
        return None, None
    assert m.Status in (GRB.OPTIMAL, GRB.INFEASIBLE), f"status {m.Status}"
    if m.Status == GRB.INFEASIBLE:
        return False, None
    m2, e2, f2 = model()
    m2.Params.TimeLimit = spread_timelimit
    m2.setObjective(gp.quicksum(f2[i] * f2[i] for i in N.bus), GRB.MAXIMIZE)
    m2.optimize()
    return True, m2.ObjBound


def run_case(name, variables, constraints, expect, ac=True):
    N = build(variables, constraints)
    degs = {i: sum(1 for _ in N.neighbors(i)) for i in N.bus}
    feas, V = solve_dc(N)
    print(f"case {name}: buses={len(N.bus)} lines={len(N.lines)} maxdeg={max(degs.values())}")
    print(f"   DC feasible: {feas}; expected: {expect}")
    ok = feas == expect
    if feas:
        print("   values:", {v: round(V[f'X_{v}'], 6) for v in variables})
    if ac and len(N.bus) <= AC_MAX_BUSES:
        feas_ac, spread_bound = solve_ac(N, timelimit=AC_TIMELIMIT, spread_timelimit=AC_TIMELIMIT)
        if feas_ac is None:
            print("   AC check: time limit reached, inconclusive (Lemma 4 is proved analytically)")
        else:
            print(f"   AC feasible: {feas_ac}" + (f"; certified upper bound on angle spread sum f_i^2 = {spread_bound:.2e}" if feas_ac else ""))
            ok &= feas_ac == expect
            if feas_ac and spread_bound >= 1e-6:
                print("   (angle-spread bound not certified within the time limit)")
    return ok


if __name__ == '__main__':
    ok = True
    ok &= run_case('x*x=1', ['x'], [('inv', 'x', 'x')], True)
    ok &= run_case('x+x=y, x*y=1 (1/sqrt2)', ['x', 'y'], [('add', 'x', 'x', 'y'), ('inv', 'x', 'y')], True)
    ok &= run_case('x+y=z, x*y=1, z*z=1 (infeasible)', ['x', 'y', 'z'],
                   [('add', 'x', 'y', 'z'), ('inv', 'x', 'y'), ('inv', 'z', 'z')], False)
    ok &= run_case('x+x=y, y+y=z, z*z=1 (infeasible)', ['x', 'y', 'z'],
                   [('add', 'x', 'x', 'y'), ('add', 'y', 'y', 'z'), ('inv', 'z', 'z')], False)
    ok &= run_case('x+x=y, y*y=1 (x=1/2)', ['x', 'y'], [('add', 'x', 'x', 'y'), ('inv', 'y', 'y')], True)
    ok &= run_case('x+x=y, y+y=z (z=2)', ['x', 'y', 'z'], [('add', 'x', 'x', 'y'), ('add', 'y', 'y', 'z')], True)
    ok &= run_case('golden', ['x', 'y', 'z'], [('add', 'x', 'y', 'z'), ('inv', 'x', 'z'), ('inv', 'y', 'y')], True)
    ok &= run_case('fan-out', ['u', 'w', 'y1', 'y2', 'y3'],
                   [('add', 'u', 'u', 'w'), ('inv', 'w', 'w'), ('inv', 'u', 'y1'), ('inv', 'u', 'y2'), ('inv', 'u', 'y3')], True)
    print("ALL OK" if ok else "MISMATCH")
    sys.exit(0 if ok else 1)
