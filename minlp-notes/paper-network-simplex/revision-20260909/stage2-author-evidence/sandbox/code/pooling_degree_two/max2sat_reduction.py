"""Cross-check of the MAX-2-SAT reduction for one-quality pooling with ALL
degrees at most two (input out-degree, pool in- and out-degree, output
in-degree).

Two gadget families are checked (see results/pooling-all-degrees-two.md):

* cycle gadget: variable X with o_X literal occurrences becomes a cycle of
  t = 2 o_X pools and t inputs, qualities alternating 0/1, all capacities 1,
  pool k fed by inputs k and k+1 (mod t);
* path gadget: t = 2 o_X + 2 pools and t-1 inputs i_1..i_{t-1}; pool k is fed
  by i_k and i_{k+1} when they exist, so the two end pools have in-degree 1;
  the two end pools share one private output of capacity 1.

Every pool has a private output (mu = 1, capacity 1, arc cost -r); a clause
is an output with mu = 0 and capacity 1 fed by its two literal pools at arc
cost -(r+1), where r is the maximum number of occurrences of a variable.
Claim: the minimum cost equals -(r * base + MAX2SAT), where base is the total
saturating throughput of the gadgets (sum of t_X for cycles, sum of t_X - 1
for paths).  For random small instances both pooling instances are solved to
global optimality with Gurobi (NonConvex=2) and compared with brute force.
The flag --broken sets r = 0, which must produce discrepancies (harness
sanity check).

Run: conda activate minlp-notes; python max2sat_reduction.py [seed] [trials] [--broken]
"""
import itertools
import random
import sys

from verify_reduction import solve_pooling

TOL = 1e-6


def max2sat_brute(n, clauses):
    best = 0
    for bits in itertools.product((False, True), repeat=n):
        sat = sum(1 for c in clauses if any(bits[v] == s for v, s in c))
        best = max(best, sat)
    return best


def occurrences(n, clauses):
    occ = [[] for _ in range(n)]           # occ[v] = list of (clause index, sign)
    for ci, c in enumerate(clauses):
        for v, s in c:
            occ[v].append((ci, s))
    return occ


def build(n, clauses, gadget, r=None):
    """Return (inputs, pools, outputs, arcs_in, arcs_out, base)."""
    occ = occurrences(n, clauses)
    if r is None:
        r = max(len(o) for o in occ)
    inputs, pools, outputs, arcs_in, arcs_out = {}, {}, {}, {}, {}
    base = 0
    for ci in range(len(clauses)):
        outputs[('c', ci)] = (0, 1)
    for v in range(n):
        o = len(occ[v])
        if o == 0:
            continue
        pos = [ci for ci, s in occ[v] if s]
        neg = [ci for ci, s in occ[v] if not s]
        if gadget == 'cycle':
            t = 2 * o
            for k in range(t):
                inputs[(v, 'i', k)] = (k % 2, 1)
                pools[(v, 'l', k)] = 1
                arcs_in[((v, 'i', k), (v, 'l', k))] = 0
                arcs_in[((v, 'i', (k + 1) % t), (v, 'l', k))] = 0
                outputs[(v, 'p', k)] = (1, 1)
                arcs_out[((v, 'l', k), (v, 'p', k))] = -r
            even = [k for k in range(t) if k % 2 == 0]
            odd = [k for k in range(t) if k % 2 == 1]
            base += t
        else:
            t = 2 * o + 2
            for j in range(1, t):
                inputs[(v, 'i', j)] = (j % 2, 1)
            for k in range(t):
                pools[(v, 'l', k)] = 1
                if k >= 1:
                    arcs_in[((v, 'i', k), (v, 'l', k))] = 0
                if k + 1 <= t - 1:
                    arcs_in[((v, 'i', k + 1), (v, 'l', k))] = 0
            for k in range(1, t - 1):
                outputs[(v, 'p', k)] = (1, 1)
                arcs_out[((v, 'l', k), (v, 'p', k))] = -r
            outputs[(v, 'p', 'end')] = (1, 1)
            arcs_out[((v, 'l', 0), (v, 'p', 'end'))] = -r
            arcs_out[((v, 'l', t - 1), (v, 'p', 'end'))] = -r
            even = [k for k in range(2, t - 1, 2)]
            odd = [k for k in range(1, t - 2, 2)]
            base += t - 1
        assert len(pos) <= len(even) and len(neg) <= len(odd)
        for ci, k in zip(pos, even):
            arcs_out[((v, 'l', k), ('c', ci))] = -(r + 1)
        for ci, k in zip(neg, odd):
            arcs_out[((v, 'l', k), ('c', ci))] = -(r + 1)
    return inputs, pools, outputs, arcs_in, arcs_out, base, r


def check_degrees(inputs, pools, outputs, arcs_in, arcs_out):
    from collections import Counter
    out_i = Counter(a[0] for a in arcs_in)
    in_l = Counter(a[1] for a in arcs_in)
    out_l = Counter(a[0] for a in arcs_out)
    in_j = Counter(a[1] for a in arcs_out)
    assert all(out_i[i] <= 2 for i in inputs)
    assert all(in_l[l] <= 2 and out_l[l] <= 2 for l in pools)
    assert all(in_j[j] <= 2 for j in outputs)
    return max(out_i.values()), max(in_l.values()), max(out_l.values()), max(in_j.values())


def random_max2sat(rng):
    n = rng.randint(2, 4)
    m = rng.randint(1, 6)
    clauses = []
    for _ in range(m):
        u, v = rng.sample(range(n), 2)
        clauses.append(((u, rng.random() < 0.5), (v, rng.random() < 0.5)))
    return n, clauses


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    broken = '--broken' in sys.argv
    seed = int(args[0]) if len(args) > 0 else 0
    trials = int(args[1]) if len(args) > 1 else 40
    rng = random.Random(seed)
    bad = 0
    # Fixed instances first: all four sign patterns on two variables (MAX2SAT=3,
    # not satisfiable) and a satisfiable 3-variable instance.
    fixed = [
        (2, [((0, True), (1, True)), ((0, False), (1, True)),
             ((0, True), (1, False)), ((0, False), (1, False))]),
        (3, [((0, True), (1, False)), ((1, True), (2, False)), ((2, True), (0, False))]),
    ]
    for trial in range(-len(fixed), trials):
        n, clauses = fixed[trial] if trial < 0 else random_max2sat(rng)
        best = max2sat_brute(n, clauses)
        line = f"trial {trial}: n={n} m={len(clauses)} max2sat={best}"
        for gadget in ('cycle', 'path'):
            inst = build(n, clauses, gadget, r=0 if broken else None)
            inputs, pools, outputs, arcs_in, arcs_out, base, r = inst
            degs = check_degrees(inputs, pools, outputs, arcs_in, arcs_out)
            opt = solve_pooling(inputs, pools, outputs, arcs_in, arcs_out)
            target = -(r * base + best)
            ok = abs(opt - target) <= TOL
            bad += not ok
            line += f" | {gadget}: r={r} base={base} opt={opt:.6f} target={target} degs={degs} {'ok' if ok else 'MISMATCH'}"
        print(line)
    print('summary: trials', trials, 'mismatches', bad, '(expected > 0)' if broken else '(expected 0)')


if __name__ == '__main__':
    main()
