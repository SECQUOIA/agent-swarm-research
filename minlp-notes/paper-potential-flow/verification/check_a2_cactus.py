#!/usr/bin/env python3
"""Deterministic A2 regression checks using only the standard library.

Fraction pairs represent u+v*sqrt(d) for exact identities. Encoders never
compute radicals. Each decision uses its exact Fraction gap when available,
otherwise 100-digit Decimal evaluation separated from zero by more than
1e-70 times its absolute term sum (at least one). Compare whenever both
decisions are known; withhold the comparison otherwise. Small numerical
gaps are never rounded to equality. Perfect-square gaps use integer square
roots and Fractions. Face optimization is numerical
sampling plus local refinement, not the certified algebraic algorithm.
The A1 whole-graph solver independently checks its passive residuals.
"""

from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction as F
import importlib.util
from itertools import product
from math import isqrt, prod
from pathlib import Path
import random
import sys

sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location(
    'a1', Path(__file__).with_name('check_a1_preliminaries.py'))
a1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a1)
CHECKS = 0
DECIDED = 0
INCONCLUSIVE = 0
EXACT_TIES = 0
MARGIN = Decimal('1e-70')
FACE_TOL = Decimal('2e-7')


def check(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise AssertionError(message)


def close(a, b, message, tolerance=Decimal('1e-9')):
    check(abs(a1.dec(a) - a1.dec(b)) <= tolerance, message)


def mul(x, y, d):
    return (x[0]*y[0] + d*x[1]*y[1], x[0]*y[1] + x[1]*y[0])


def inverse(x, d):
    norm = x[0]**2 - d*x[1]**2
    check(norm != 0, 'singular formal radical inverse')
    return x[0]/norm, -x[1]/norm


def scale(x, a):
    return x[0]*a, x[1]*a


def rational_sqrt(q):
    q = F(q)
    a, b = isqrt(q.numerator), isqrt(q.denominator)
    return F(a, b) if a*a == q.numerator and b*b == q.denominator else None


def parallel(a, b):
    a, b = a1.dec(a), a1.dec(b)
    return a*b/(a.sqrt() + b.sqrt())**2


def identities(rng):
    for d in [2, 3, 4, 5, 9, 16, 31, 101]:
        a, b = F((d-1)**2), F((d-1)**2, d)
        x = inverse((F(1), F(1)), d)
        y = mul((F(0), F(1)), x, d)
        check((x[0]+y[0], x[1]+y[1]) == (1, 0), 'gadget balance')
        drop = scale(mul(x, x, d), a)
        check(drop == scale(mul(y, y, d), b), 'gadget equal drops')
        check(drop == (d+1, -2), 'gadget radical identity')
    for _ in range(100):
        a, b = F(rng.randint(1, 30), rng.randint(1, 12)), F(rng.randint(1, 30), rng.randint(1, 12))
        if a == b:
            b += 1
        d = a*b
        raw = scale(inverse((a+b, F(2)), d), a*b)
        rationalized = (a*b*(a+b)/(a-b)**2, -2*a*b/(a-b)**2)
        check(raw == rationalized, 'parallel rationalization in Q(sqrt(AB))')
        check(mul(raw, (a+b, F(2)), d) == (a*b, 0), 'parallel denominator identity')
        # x_A = (B+sqrt(AB))/(A+B+2sqrt(AB)).
        xa = mul((b, F(1)), inverse((a+b, F(2)), d), d)
        xb = (1-xa[0], -xa[1])
        check(scale(mul(xa, xa, d), a) == raw, 'parallel physical A drop')
        check(scale(mul(xb, xb, d), b) == raw, 'parallel physical B drop')
        close(parallel(a, a), a/4, 'equal branch numerical formula')


@dataclass
class Instance:
    n: int
    edges: list
    s: int
    t: int
    threshold: F


def fixed_mpd(yes):
    return Instance(2, [(0, 1, F(1))], 0, 1, F(1 if yes else 2))


def srs_to_mpd(radicands, threshold):
    """Exact many-one encoder, including nonpositive-threshold branches."""
    check(all(isinstance(a, int) and a >= 0 for a in radicands), 'encoder radicand domain')
    check(isinstance(threshold, int), 'encoder threshold domain')
    threshold -= radicands.count(1)
    radicands = [a for a in radicands if a > 1]
    if not radicands:
        return fixed_mpd(threshold >= 0)
    if threshold <= 0:
        return fixed_mpd(False)
    constant = sum(a+1 for a in radicands) + len(radicands)-1
    gamma = constant-2*threshold
    if gamma <= 0:
        return fixed_mpd(True)
    scale_factor = 2*prod(radicands)
    edges = []
    for i, a in enumerate(radicands):
        u, mid, v = 3*i, 3*i+1, 3*i+2
        half = F((a-1)**2, 2*a)
        edges.extend([(u, v, F((a-1)**2)), (u, mid, half), (mid, v, half)])
        if i:
            edges.append((u-1, u, F(1)))
    return Instance(3*len(radicands), [(u, v, r*scale_factor) for u, v, r in edges],
                    0, 3*len(radicands)-1, F(scale_factor*gamma))


def block_chain(n, edges, s, t):
    blocks = a1.blocks(n, edges)
    incidence = [[] for _ in range(n+len(blocks))]
    for i, block in enumerate(blocks):
        for v in {v for e in block for v in edges[e][:2]}:
            incidence[v].append((n+i, i, 1))
            incidence[n+i].append((v, i, -1))
    walk = a1.path(incidence, s, t)
    return [(blocks[walk[i][1]-n], walk[i][0], walk[i+1][1])
            for i in range(0, len(walk), 2)]


def branches(n, edges, block, entrance, exit):
    adj = a1.adjacency(n, edges, block)
    paths = []

    def walk(v, vertices, edge_path):
        if v == exit:
            paths.append((vertices, edge_path))
            return
        for w, e, _ in adj[v]:
            if w not in vertices:
                walk(w, vertices+[w], edge_path+[e])
    walk(entrance, [entrance], [])
    check(len(paths) == (1 if len(block) == 1 else 2), 'not a cactus block')
    return paths


def block_totals(inst):
    pairs, bridge = [], F(0)
    for block, entrance, exit in block_chain(inst.n, inst.edges, inst.s, inst.t):
        if len(block) == 1:
            bridge += inst.edges[block[0]][2]
        else:
            pairs.append(tuple(sum((inst.edges[e][2] for e in es), F(0))
                               for _, es in branches(inst.n, inst.edges, block, entrance, exit)))
    return pairs, bridge


def mpd_to_srs(inst):
    """Exact encoder for arbitrary single-source/sink cacti."""
    pairs, rational = block_totals(inst)
    radicals = []
    for a, b in pairs:
        if a == b:
            rational += a/4
        else:
            rational += a*b*(a+b)/(a-b)**2
            radicals.append(4*a**3*b**3/(a-b)**4)
    threshold = rational-inst.threshold
    if not radicals:
        return ([1], 1) if threshold >= 0 else ([4], 1)
    if threshold <= 0:
        return [4], 1
    denominator = threshold.denominator*prod(r.denominator for r in radicals)
    integers = [denominator**2*r for r in radicals]
    k = denominator*threshold
    check(all(x.denominator == 1 and x > 0 for x in integers), 'SRS radicand integrality')
    check(k.denominator == 1 and k > 0, 'SRS positive threshold')
    return [x.numerator for x in integers], k.numerator


def srs_gap(radicands, threshold):
    terms = [Decimal(a).sqrt() for a in radicands]
    gap = a1.dec(threshold)-sum(terms, Decimal(0))
    size = max(Decimal(1), abs(a1.dec(threshold))+sum(terms, Decimal(0)))
    roots = [isqrt(a) for a in radicands]
    exact = F(threshold-sum(roots)) if all(r*r == a for r, a in zip(roots, radicands)) else None
    return gap, size, exact


def mpd_gap(inst):
    pairs, bridge = block_totals(inst)
    terms = [parallel(a, b) for a, b in pairs]
    value = a1.dec(bridge)+sum(terms, Decimal(0))
    size = max(Decimal(1), abs(a1.dec(inst.threshold))+abs(value))
    exact = bridge-inst.threshold
    for a, b in pairs:
        root = rational_sqrt(a*b)
        if root is None:
            exact = None
            break
        exact += a*b/(a+b+2*root)
    return value-a1.dec(inst.threshold), size, exact


def compare_decisions(left, right):
    global DECIDED, INCONCLUSIVE, EXACT_TIES

    def decide(side):
        gap, size, exact = side
        if exact is not None:
            return exact >= 0
        if abs(gap) > MARGIN*size:
            return gap > 0
        return None

    left_decision, right_decision = decide(left), decide(right)
    if left_decision is not None and right_decision is not None:
        check(left_decision == right_decision, 'independent decision mismatch')
        DECIDED += 1
        EXACT_TIES += int(left[2] == 0 or right[2] == 0)
    else:
        INCONCLUSIVE += 1


def reductions(rng):
    # A separated irrational no must disagree with an exact rational yes,
    # even when the latter's gap is zero. The old joint-gap rule missed this.
    try:
        compare_decisions(srs_gap([2], 1), mpd_gap(fixed_mpd(True)))
    except AssertionError as error:
        check(str(error) == 'independent decision mismatch', 'wrong regression failure')
    else:
        raise AssertionError('deliberately wrong encoder pairing was not detected')
    cases = [([], 0), ([0, 1, 1], 2), ([1, 1], 1), ([2], 0),
             ([2], 2), ([4, 9], 5), ([0, 1, 4, 9], 6), ([16], 4)]
    cases += [([rng.randrange(26) for _ in range(rng.randrange(1, 7))], rng.randrange(-2, 27))
              for _ in range(100)]
    for aa, k in cases:
        inst = srs_to_mpd(aa, k)
        check(len({tuple(sorted((u, v))) for u, v, _ in inst.edges}) == len(inst.edges), 'hardness simplicity')
        check(max(map(len, a1.adjacency(inst.n, inst.edges))) <= 3, 'hardness maximum degree')
        check(all(r > 0 and r.denominator == 1 for _, _, r in inst.edges), 'integer resistances')
        check(all(len(block) in (1, 3) for block in a1.blocks(inst.n, inst.edges)), 'triangle cactus')
        original, encoded = srs_gap(aa, k), mpd_gap(inst)
        compare_decisions(original, encoded)
        compare_decisions(encoded, srs_gap(*mpd_to_srs(inst)))
        # Independent nonlinear state evaluation on the actual encoded graph.
        b = [F(0)]*inst.n
        b[inst.s], b[inst.t] = F(1), F(-1)
        _, pi = a1.solve(inst.n, inst.edges, b)
        close((pi[inst.s]-pi[inst.t])-a1.dec(inst.threshold), encoded[0], 'encoded graph passive value')
    # Random reverse inputs have bridges, off-path blocks, unequal and equal
    # branches, and arbitrary terminal pairs; they are not only gadget graphs.
    off_path_cases = 0
    for trial in range(45):
        n, edges = random_cactus(rng, 4)
        s, t = rng.sample(range(n), 2)
        inst = Instance(n, edges, s, t, F(rng.randrange(-5, 40), rng.randrange(1, 5)))
        compare_decisions(mpd_gap(inst), srs_gap(*mpd_to_srs(inst)))
        core_edges = {e for block, _, _ in block_chain(n, edges, s, t) for e in block}
        off_path_cases += int(len(core_edges) < len(edges))
        b = [F(0)]*n
        b[s], b[t] = F(1), F(-1)
        x, pi = a1.solve(n, edges, b)
        pairs, rational = block_totals(inst)
        radicals = []
        for a, branch_b in pairs:
            if a == branch_b:
                rational += a/4
            else:
                rational += a*branch_b*(a+branch_b)/(a-branch_b)**2
                radicals.append(4*a**3*branch_b**3/(a-branch_b)**4)
        radical_drop = a1.dec(rational)-sum((a1.dec(r).sqrt() for r in radicals), Decimal(0))
        close(pi[s]-pi[t], radical_drop, 'reverse whole-graph radical value', Decimal('1e-20'))
        for e in set(range(len(edges)))-core_edges:
            close(x[e], 0, 'off-path unit-flow state', Decimal('1e-20'))
    check(off_path_cases >= 20, 'insufficient reverse off-path coverage')
    print(f'  reverse encoders: 45 whole-graph solves, {off_path_cases} with off-path blocks.', flush=True)
    # Exact ties include unequal branches with rational square-root product.
    for a, b in [(4, 4), (1, 4), (9, 16), (F(1, 4), F(9, 4))]:
        a, b = F(a), F(b)
        root = rational_sqrt(a*b)
        value = a*b/(a+b+2*root)
        for delta in [F(0), F(1, 100), F(-1, 100)]:
            inst = Instance(3, [(0, 2, a), (0, 1, b/2), (1, 2, b/2)], 0, 2, value+delta)
            compare_decisions(mpd_gap(inst), srs_gap(*mpd_to_srs(inst)))
    for gamma in [F(6), F(7)]:  # Q=6: T=0 and T<0 must map to positive-K no.
        inst = Instance(3, [(0, 2, F(1)), (0, 1, F(1)), (1, 2, F(1))], 0, 2, gamma)
        check(mpd_to_srs(inst) == ([4], 1), 'T<=0 fixed no convention')
    check(DECIDED >= 180 and EXACT_TIES >= 8, 'insufficient reduction decision coverage')


def random_cactus(rng, count):
    n, edges = 1, []
    for _ in range(count):
        anchor = rng.randrange(n)
        length = rng.choice([1, 2, 3, 4, 5])
        if length == 1:
            pairs = [(anchor, n)]
            n += 1
        else:
            vertices = [anchor]+list(range(n, n+length-1))
            n += length-1
            pairs = list(zip(vertices, vertices[1:]+vertices[:1]))
        for u, v in pairs:
            if rng.randrange(2):
                u, v = v, u
            edges.append((u, v, F(rng.randrange(1, 10), rng.randrange(1, 5))))
    return n, edges


def aggregate(n, edges, lo, hi, s, t):
    core_edges = {e for block, _, _ in block_chain(n, edges, s, t) for e in block}
    core_vertices = sorted({v for e in core_edges for v in edges[e][:2]})
    index = {v: i for i, v in enumerate(core_vertices)}
    groups = [sorted(a1.component(n, edges, core_edges, v)) for v in core_vertices]
    check(sum(map(len, groups)) == n and len(set().union(*map(set, groups))) == n, 'aggregation partition')
    check(all(set(g).intersection(core_vertices) == {v} for g, v in zip(groups, core_vertices)), 'unique attachment')
    core = [(index[edges[e][0]], index[edges[e][1]], edges[e][2]) for e in sorted(core_edges)]
    return (len(core_vertices), core,
            [sum((lo[v] for v in g), F(0)) for g in groups],
            [sum((hi[v] for v in g), F(0)) for g in groups],
            index[s], index[t], groups)


def disaggregate(groups, totals, lo, hi):
    b = list(lo)
    for group, total in zip(groups, totals):
        remainder = total-sum((lo[v] for v in group), F(0))
        for v in group:
            take = min(remainder, hi[v]-lo[v])
            b[v] += take
            remainder -= take
        check(remainder == 0, 'disaggregation remainder')
    check(sum(b) == 0 and all(l <= x <= u for l, x, u in zip(lo, b, hi)), 'exact disaggregation feasibility')
    return b


@dataclass(frozen=True)
class Face:
    fixed: tuple
    pivots: tuple
    lo: F
    hi: F
    total: F

    def loads(self, z=None):
        z = self.lo if z is None else z
        b = list(self.fixed)
        if self.pivots:
            b[self.pivots[0]] = z
        if len(self.pivots) == 2:
            b[self.pivots[1]] = self.total-z
        return b


def nomination_faces(n, edges, lower, upper, s, t):
    """Exact bound/vertex/gap enumeration on an already aggregated core."""
    seen, patterns = set(), 0

    def retain(pattern):
        nonlocal patterns
        patterns += 1
        pivots = tuple(v for v in range(n) if pattern[v] == 'F' and lower[v] != upper[v])
        check(len(pivots) <= 2, 'more than two pivots')
        fixed = tuple(F(0) if v in pivots else upper[v] if pattern[v] == 'U' else lower[v]
                      for v in range(n))
        total = -sum(fixed)
        if not pivots:
            if total != 0:
                return
            lo = hi = F(0)
        elif len(pivots) == 1:
            lo = hi = total
            if not lower[pivots[0]] <= lo <= upper[pivots[0]]:
                return
        else:
            p, q = pivots
            lo, hi = max(lower[p], total-upper[q]), min(upper[p], total-lower[q])
            if lo > hi:
                return
        seen.add(Face(fixed, pivots, lo, hi, total))

    retain(['L']*n)
    retain(['U']*n)
    before = set()
    for block, entrance, exit in block_chain(n, edges, s, t):
        vertices = {v for e in block for v in edges[e][:2]}
        base = ['U' if v in before else 'L' for v in range(n)]
        for pivot, state in [(entrance, 'L'), (exit, 'U')]:
            pattern = list(base)
            for v in vertices:
                pattern[v] = state
            pattern[pivot] = 'F'
            retain(pattern)
        if len(block) == 1:
            pattern = list(base)
            pattern[entrance], pattern[exit] = 'U', 'L'
            retain(pattern)
        else:
            paths = branches(n, edges, block, entrance, exit)

            def options(vertices):
                inner = vertices[1:-1]
                for gap in range(len(inner)+1):
                    yield {v: 'U' if j < gap else 'L' for j, v in enumerate(inner)}
                for pivot in range(len(inner)):
                    yield {v: 'U' if j < pivot else 'L' if j > pivot else 'F'
                           for j, v in enumerate(inner)}
            for left, right in product(options(paths[0][0]), options(paths[1][0])):
                pattern = list(base)
                pattern[entrance], pattern[exit] = 'U', 'L'
                for v, state in {**left, **right}.items():
                    pattern[v] = state
                retain(pattern)
        before.update(vertices)
    check(patterns <= 8*n*n, 'quadratic enumeration bound')
    return sorted(seen, key=lambda f: (f.fixed, f.pivots, f.lo, f.hi, f.total))


def feasible_random(lo, hi, rng):
    """Random sequential allocations, with exact residual feasibility."""
    order = list(range(len(lo)))
    rng.shuffle(order)
    b, remaining = list(lo), F(0)
    for i, v in enumerate(order):
        rest = order[i+1:]
        low = max(lo[v], remaining-sum((hi[w] for w in rest), F(0)))
        high = min(hi[v], remaining-sum((lo[w] for w in rest), F(0)))
        check(low <= high, 'random allocation feasibility')
        b[v] = low+(high-low)*F(rng.randrange(17), 16)
        remaining -= b[v]
    check(sum(b) == 0, 'random nomination balance')
    return b


def maximize_face(face, objective):
    if face.lo == face.hi:
        return objective(face.loads())
    grid = [face.lo+(face.hi-face.lo)*F(i, 48) for i in range(49)]
    values = [objective(face.loads(z)) for z in grid]
    best = max(values)
    for j in range(1, len(grid)-1):
        if values[j] >= max(values[j-1], values[j+1]):
            left, right = grid[j-1], grid[j+1]
            # Refine each sampled local maximum, not only the largest one.
            for _ in range(22):
                a, b = (2*left+right)/3, (left+2*right)/3
                va, vb = objective(face.loads(a)), objective(face.loads(b))
                best = max(best, va, vb)
                if va < vb:
                    left = a
                else:
                    right = b
    return best


def exchange_line_search(lo, hi, objective, rng):
    """Multi-restart full-box search, without structural face information."""
    movable = [v for v in range(len(lo)) if lo[v] < hi[v]]
    best = Decimal('-Infinity')
    for _ in range(5):
        b = feasible_random(lo, hi, rng)
        value = objective(b)
        for _ in range(16):
            p, q = rng.sample(movable, 2)
            left = max(lo[p]-b[p], b[q]-hi[q])
            right = min(hi[p]-b[p], b[q]-lo[q])

            def evaluate(step):
                candidate = list(b)
                candidate[p] += step
                candidate[q] -= step
                return objective(candidate), candidate

            grid = [left+(right-left)*F(i, 8) for i in range(9)]
            samples = [evaluate(step) for step in grid]
            candidates = list(samples)
            for j in range(1, 8):
                if samples[j][0] >= max(samples[j-1][0], samples[j+1][0]):
                    low, high = grid[j-1], grid[j+1]
                    for _ in range(12):
                        a, c = (2*low+high)/3, (low+2*high)/3
                        va, vc = evaluate(a), evaluate(c)
                        candidates.extend((va, vc))
                        if va[0] < vc[0]:
                            low = a
                        else:
                            high = c
            candidate_value, candidate_b = max(candidates, key=lambda item: item[0])
            if candidate_value > value:
                value, b = candidate_value, candidate_b
        best = max(best, value)
    return best


def face_checks(rng):
    total_faces = variable_faces = attached = 0
    six_cycle_pivot_faces = grid_cases = 0
    smallest_margin = Decimal('Infinity')
    cases = []
    # Opposite interior branch pivots, shifted boxes, and nontrivial exact
    # rational parameter intervals are guaranteed, rather than left to chance.
    for trial in range(6):
        edges = [(0, 1, F(rng.randrange(1, 8))), (1, 2, F(rng.randrange(1, 8))),
                 (0, 3, F(rng.randrange(1, 8))), (3, 2, F(rng.randrange(1, 8)))]
        shift = F(trial-2, 3)
        lo = [F(2), shift-1, F(-2), -shift-1]
        hi = [F(2), shift+1, F(-2), -shift+1]
        cases.append((4, edges, lo, hi, 0, 2))
    # An active diamond followed by a fixed triangle tests changing one block
    # while another contributes a constant irrational drop.
    cases.append((7, [(0, 1, F(2)), (1, 2, F(3)), (0, 3, F(4)),
                      (3, 2, F(1)), (2, 4, F(1)), (4, 6, F(1)),
                      (4, 5, F(1)), (5, 6, F(1))],
                  [F(2), F(-1), F(0), F(-1), F(0), F(0), F(-2)],
                  [F(2), F(1), F(0), F(1), F(0), F(0), F(-2)], 0, 6))
    for trial in range(12):
        n, edges = random_cactus(rng, 4)
        center = [F(rng.randrange(-6, 7), 3) for _ in range(n-1)]
        center.append(-sum(center))
        lo = [c-F(rng.randrange(4), 2) for c in center]
        hi = [c+F(rng.randrange(4), 2) for c in center]
        if trial == 0:
            lo = list(center)  # all-lower is the only balanced point
        elif trial == 1:
            hi = list(center)  # all-upper is the only balanced point
        elif trial == 2:
            lo = hi = list(center)
        s, t = rng.sample(range(n), 2)
        cases.append((n, edges, lo, hi, s, t))
    # Terminal/articulation pivots on a tree, zero box, and parallel cycle.
    for lo, hi in [([F(-1), F(-1), F(-1)], [F(2), F(1), F(0)]),
                   ([F(0)]*3, [F(0)]*3)]:
        cases.append((3, [(0, 1, F(1)), (1, 2, F(2))], lo, hi, 0, 2))
    cases.append((2, [(0, 1, F(1)), (1, 0, F(2))], [F(0), F(-1)], [F(1), F(0)], 0, 1))
    six_cycle_start = len(cases)
    for _ in range(6):
        edges = [(v, (v+1) % 6, F(rng.randrange(1, 10), rng.randrange(1, 5)))
                 for v in range(6)]
        shifts = [F(rng.randrange(-3, 4), 3) for _ in range(3)]
        shifts.append(-sum(shifts))
        lo, hi = [F(0)]*6, [F(0)]*6
        lo[0] = hi[0] = F(2)
        lo[3] = hi[3] = F(-2)
        for v, shift in zip([1, 2, 4, 5], shifts):
            lo[v], hi[v] = shift-1, shift+1
        cases.append((6, edges, lo, hi, 0, 3))
    for trial, (original_n, original_edges, original_lo, original_hi, os, ot) in enumerate(cases):
        n, edges, lo, hi, s, t, groups = aggregate(original_n, original_edges, original_lo, original_hi, os, ot)
        attached += int(n < original_n)
        faces = nomination_faces(n, edges, lo, hi, s, t)
        check(bool(faces), 'no feasible faces')
        total_faces += len(faces)
        variable_faces += sum(f.lo < f.hi for f in faces)
        if trial >= six_cycle_start:
            count = sum(len(f.pivots) == 2 and f.lo < f.hi for f in faces)
            check(count >= 2, 'six-cycle missing two-pivot variable faces')
            six_cycle_pivot_faces += count
        cache = {}

        def objective(b):
            key = tuple(b)
            check(sum(b) == 0 and all(l <= x <= u for l, x, u in zip(lo, b, hi)), 'sample exactly feasible')
            if key not in cache:
                _, pi = a1.solve(n, edges, b)
                cache[key] = pi[s]-pi[t]
            return cache[key]
        best = max(maximize_face(face, objective) for face in faces)
        full = []
        for _ in range(65):
            b = feasible_random(lo, hi, rng)
            full.append((objective(b), b))
        # A randomized exchange search over the full box adds local boundary
        # exploration independently of the structural face enumeration.
        for _ in range(3):
            b = feasible_random(lo, hi, rng)
            value = objective(b)
            for _ in range(14):
                p, q = rng.sample(range(n), 2)
                left = max(lo[p]-b[p], b[q]-hi[q])
                right = min(hi[p]-b[p], b[q]-lo[q])
                next_b = b
                for d in [left, (left+right)/2, right]:
                    candidate = list(b)
                    candidate[p] += d
                    candidate[q] -= d
                    v = objective(candidate)
                    if v > value:
                        value, next_b = v, candidate
                b = next_b
            full.append((value, b))
        search_best = max(v for v, _ in full)
        if trial >= six_cycle_start:
            search_best = max(search_best, exchange_line_search(lo, hi, objective, rng))
        # An exhaustive rational grid over all but one coordinate supplies a
        # separate, deterministic full-box comparison on three tiny cacti.
        if trial in (0, 1, 2):
            axes = [[lo[v]+(hi[v]-lo[v])*F(i, 8) for i in range(9)]
                    if lo[v] < hi[v] else [lo[v]] for v in range(n-1)]
            grid_values = []
            for prefix in product(*axes):
                last = -sum(prefix)
                if lo[-1] <= last <= hi[-1]:
                    grid_values.append(objective(list(prefix)+[last]))
            check(bool(grid_values), 'empty brute-force grid')
            check(best >= max(grid_values)-FACE_TOL, 'face maximum below brute-force grid')
            grid_cases += 1
        margin = best-search_best
        smallest_margin = min(smallest_margin, margin)
        check(margin >= -FACE_TOL, f'face search below full search in trial {trial}: {margin}')
        path = a1.path(a1.adjacency(n, edges), s, t)
        bound = sum(max(abs(l), abs(u)) for l, u in zip(lo, hi))
        constant = 2*bound*sum((edges[e][2] for _, _, e, _ in path), F(0))
        for _ in range(10):
            (_, b), (_, c) = rng.sample(full, 2)
            distance = sum((abs(x-y) for x, y in zip(b, c)), F(0))
            check(abs(objective(b)-objective(c)) <= a1.dec(constant*distance)+Decimal('1e-9'), 'Lipschitz inequality')
        # Check both directions of aggregation with exact totals and original
        # whole-graph states, independent of the reduced solver calls.
        for b in [faces[0].loads(), faces[-1].loads(), feasible_random(lo, hi, rng)]:
            original_b = disaggregate(groups, b, original_lo, original_hi)
            _, pi = a1.solve(original_n, original_edges, original_b)
            close(pi[os]-pi[ot], objective(b), 'disaggregated objective invariance')
        original_b = feasible_random(original_lo, original_hi, rng)
        b = [sum((original_b[v] for v in g), F(0)) for g in groups]
        _, pi = a1.solve(original_n, original_edges, original_b)
        close(pi[os]-pi[ot], objective(b), 'original-to-core objective invariance')
        print(f'  face case {trial+1}/{len(cases)}: {len(faces)} faces, margin {margin:.2E}', flush=True)
    check(variable_faces >= 6 and attached >= 4, 'insufficient variable/attached face coverage')
    check(six_cycle_pivot_faces >= 12 and grid_cases == 3, 'insufficient new search coverage')
    print(f'  six-cycles: {six_cycle_pivot_faces} two-pivot variable faces; '
          f'{grid_cases} tiny-cactus brute-force grids.', flush=True)
    return len(cases), total_faces, variable_faces, attached, smallest_margin


def split_checks(rng):
    for _ in range(100):
        n, edges = random_cactus(rng, 3)
        if n >= 3:
            # Also exercise noncactus graphs: the ETR statement is general.
            edges.append((0, n-1, F(2)))
        flows = [F(rng.randrange(-20, 21), rng.randrange(1, 10)) for _ in edges]
        flows[0] = F(0)
        original_div, split_div = [F(0)]*n, [F(0)]*n
        for (u, v, beta), x in zip(edges, flows):
            p, negative = max(x, F(0)), max(-x, F(0))
            check(p >= 0 and negative >= 0 and p*negative == 0, 'split complementarity')
            check(p-negative == x, 'split reconstructs flow')
            check(p*p-negative*negative == x*abs(x), 'split exact signed quadratic')
            check(beta*(p*p-negative*negative) == beta*x*abs(x), 'split exact edge drop')
            original_div[u] += x
            original_div[v] -= x
            split_div[u] += p-negative
            split_div[v] -= p-negative
        check(original_div == split_div and sum(split_div) == 0, 'split conserves nominations')
    # Positive p and n without complementarity would be an incorrect encoding.
    check(F(2)**2-F(1)**2 != (F(2)-F(1))*abs(F(2)-F(1)), 'complementarity is necessary')


def main():
    rng = random.Random(2026090702)
    with localcontext() as ctx:
        ctx.prec = 100
        identities(rng)
        reductions(rng)
        print(f'Exact identities/encoders passed: {DECIDED} known decision comparisons, '
              f'{EXACT_TIES} involving exact ties, {INCONCLUSIVE} comparisons withheld.', flush=True)
        summary = face_checks(rng)
        split_checks(rng)
    print(f'PASS: {CHECKS} A2 assertions; {summary[0]} cactus cases, {summary[1]} faces, '
          f'{summary[2]} variable faces, {summary[3]} off-core cases; min face margin {summary[4]:.3E}.')
    print(f'A1 solver/decomposition assertions: {a1.CHECKS}; maximum residual {a1.MAX_ERROR:.3E}.')
    print('Numerical face searches supplement the proofs; they are not certified global optimization.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
