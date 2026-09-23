"""Bounded-data variant of the ETR-INV -> pooling reduction.

Every forced pool has at most two arcs to non-slack terminals (M = 2, so
B = 7); copies of a variable value are produced along an alternating chain
P -> R -> P -> R -> ... (and Pbar -> Rbar -> ...) in which each pool spends
one emission on feeding the next pool of the chain and keeps one emission
for a gadget.  All capacities lie in {2, 5/2, 4, 7}, all bounds in
{0, 1, 1/14, 2/35}, qualities in {0,1}, costs in {0,-1,-2}; every node has
in-degree at most two and out-degree at most three.

See results/pooling-existential-theory-of-reals.md, Section 6 (bounded
data), and build_and_check.py for the unbounded-fan-out version.
"""
from fractions import Fraction as Fr
import itertools
import sys

from build_and_check import Pooling, solve

B = Fr(7)
MU_EMIT = Fr(1, 2 * B)      # 1/14
MU_GADGET = Fr(2, 5 * B)    # 2/35


def build_bounded(variables, constraints):
    P = Pooling()
    counter = itertools.count()

    def fresh(prefix):
        return f"{prefix}{next(counter)}"

    def forced_pool(name):
        p = P.pool(name, B, forced=True)
        d = P.source(fresh('d'), B, 0)
        P.arc(d, p)
        sl = P.term(fresh('slack'), B)
        P.arc(p, sl)
        return p

    def emission(pool, relay_quality):
        """Emission structure of Section 4.3 (+ quality flip if needed).
        Returns the source whose free arc carries the emitted value."""
        t = P.term(fresh('te'), Fr(2), forced=True, lo=MU_EMIT, up=MU_EMIT)
        P.arc(pool, t)
        pr = P.pool(fresh('pr'), Fr(2))
        P.arc(pr, t)
        sr = P.source(fresh('sr'), Fr(2), 0, forced=True)
        P.arc(sr, pr)
        if relay_quality == 0:
            return sr
        p2 = P.pool(fresh('pf'), Fr(2)); P.arc(sr, p2)
        t2 = P.term(fresh('tf'), Fr(2), forced=True); P.arc(p2, t2)
        pr2 = P.pool(fresh('pr'), Fr(2)); P.arc(pr2, t2)
        s2 = P.source(fresh('sr'), Fr(2), 1, forced=True); P.arc(s2, pr2)
        return s2

    # chain state per variable and per kind ('P' chain: P,R,P,R,...; 'Q' chain: Pbar,Rbar,...)
    chains = {}

    class Chain:
        def __init__(self, first_pool, first_kind):
            self.pool = first_pool      # current pool of the chain
            self.kind = first_kind      # 'P' (quality v/B), 'R' (1/v), 'Pb' (5/2-v), 'Rb' (1/(5/2-v))
            self.used = 0               # gadget-use arcs taken from current pool (0 or 1)

        def advance(self):
            # spend the chain emission of the current pool to feed the next pool
            nxt = {'P': 'R', 'R': 'P', 'Pb': 'Rb', 'Rb': 'Pb'}[self.kind]
            src = emission(self.pool, relay_quality=1)
            newp = forced_pool(fresh(nxt + '_'))
            P.arc(src, newp)
            self.pool, self.kind, self.used = newp, nxt, 0

        def take(self, kind):
            """Return a pool of the requested kind with a free gadget slot."""
            while self.kind != kind or self.used >= 1:
                self.advance()
            self.used += 1
            return self.pool

    for v in variables:
        s = P.source(f"s_{v}", Fr(5, 2), 1, forced=True)
        pv = forced_pool(f"P_{v}")
        pb = forced_pool(f"Pbar_{v}")
        P.arc(s, pv); P.arc(s, pb)
        chains[(v, 'P')] = Chain(pv, 'P')
        chains[(v, 'Q')] = Chain(pb, 'Pb')

    def take(v, kind):
        return chains[(v, 'P' if kind in ('P', 'R') else 'Q')].take(kind)

    for c in constraints:
        if c[0] == 'inv':
            _, x, y = c
            sr = emission(take(y, 'Rb'), relay_quality=0)      # delivers 5/2 - y at quality 0
            pc = P.pool(fresh('pc'), Fr(5, 2)); P.arc(sr, pc)
            t = P.term(fresh('tinv'), Fr(5, 2), forced=True, lo=MU_GADGET, up=MU_GADGET)
            P.arc(pc, t)
            P.arc(take(x, 'P'), t)
        elif c[0] == 'add':
            _, x, y, z = c
            padd = P.pool(fresh('padd'), Fr(4))
            for w in (x, y):
                sr = emission(take(w, 'R'), relay_quality=0)   # delivers w at quality 0
                P.arc(sr, padd)
            t = P.term(fresh('tadd'), Fr(5, 2), forced=True, lo=MU_GADGET, up=MU_GADGET)
            P.arc(padd, t)
            P.arc(take(z, 'Rb'), t)
        else:
            raise ValueError(c)
    # range enforcement: every variable needs at least one emission from a
    # P-type pool (gives v >= 1/2) and one from a Pbar-type pool (v <= 2);
    # advancing each chain once creates exactly such emissions.
    for v in variables:
        for key in ((v, 'P'), (v, 'Q')):
            ch = chains[key]
            if ch.kind in ('P', 'Pb') and ch.pool in (f"P_{v}", f"Pbar_{v}"):
                ch.advance()
    return P


def check_degrees_and_data(P):
    outdeg = {}; indeg = {}
    for (u, v) in P.arcs:
        outdeg[u] = outdeg.get(u, 0) + 1
        indeg[v] = indeg.get(v, 0) + 1
    caps = set(i['cap'] for d in (P.sources, P.pools, P.terms) for i in d.values())
    bounds = set()
    for i in P.terms.values():
        bounds.add(i['lo']); bounds.add(i['up'])
    quals = set(i['q'] for i in P.sources.values())
    costs = set(P.cost(u, v) for (u, v) in P.arcs)
    return dict(max_out=max(outdeg.values()), max_in=max(indeg.values()),
                caps=sorted(caps), bounds=sorted(bounds), quals=sorted(quals), costs=sorted(costs))


def run_case(name, variables, constraints, expect):
    P = build_bounded(variables, constraints)
    zeta = P.zeta()
    info = check_degrees_and_data(P)
    assert info['max_in'] <= 2 and info['max_out'] <= 3
    assert set(info['caps']) <= {Fr(2), Fr(5, 2), Fr(4), Fr(7)}
    assert set(info['bounds']) <= {Fr(0), Fr(1), Fr(1, 14), Fr(2, 35)}
    assert set(info['quals']) <= {Fr(0), Fr(1)} and set(info['costs']) <= {0, -1, -2}
    status, val, sol, bound = solve(P)
    feasible = val >= float(zeta) - 1e-6
    print(f"case {name}: |S|={len(P.sources)} |P|={len(P.pools)} |T|={len(P.terms)} |A|={len(P.arcs)} zeta={zeta}")
    print(f"   data: {info}")
    print(f"   best={val:.6f} bound={bound:.6f}; threshold reached: {feasible}; expected: {expect}")
    if feasible:
        print("   values:", {v: round(sol[(f's_{v}', f'P_{v}')], 6) for v in variables})
    return feasible == expect


if __name__ == '__main__':
    ok = True
    ok &= run_case('x*x=1', ['x'], [('inv', 'x', 'x')], True)
    ok &= run_case('x+x=y, x*y=1', ['x', 'y'], [('add', 'x', 'x', 'y'), ('inv', 'x', 'y')], True)
    ok &= run_case('x+y=z, x*y=1, z*z=1 (infeasible)', ['x', 'y', 'z'],
                   [('add', 'x', 'y', 'z'), ('inv', 'x', 'y'), ('inv', 'z', 'z')], False)
    ok &= run_case('x+x=y, y+y=z (z=2)', ['x', 'y', 'z'], [('add', 'x', 'x', 'y'), ('add', 'y', 'y', 'z')], True)
    ok &= run_case('golden', ['x', 'y', 'z'], [('add', 'x', 'y', 'z'), ('inv', 'x', 'z'), ('inv', 'y', 'y')], True)
    ok &= run_case('fan-out: u+u=w, w*w=1, u*y1=1, u*y2=1, u*y3=1', ['u', 'w', 'y1', 'y2', 'y3'],
                   [('add', 'u', 'u', 'w'), ('inv', 'w', 'w'), ('inv', 'u', 'y1'), ('inv', 'u', 'y2'), ('inv', 'u', 'y3')], True)
    ok &= run_case('fan-out infeasible: u+u=w, w*w=1, u*y1=1, y1+y1=y2, y2*y2=1', ['u', 'w', 'y1', 'y2'],
                   [('add', 'u', 'u', 'w'), ('inv', 'w', 'w'), ('inv', 'u', 'y1'), ('add', 'y1', 'y1', 'y2'), ('inv', 'y2', 'y2')], False)
    print("ALL OK" if ok else "MISMATCH")
    sys.exit(0 if ok else 1)
