"""coreA verification: soundness of path certificates (grids.tex) in exact arithmetic.

For random small mixed-integer box QPs (n <= 3, nonconvex allowed):
  * OPT is computed exactly (enumerate integer values and faces of the
    continuous box; solve the stationarity system on each face).
  * Theorem thm:certificate: for a random nested sequence of subboxes with
    random grids (degenerate coordinates allowed), take the largest beta for
    which Definition def:cert holds (both alternatives of (C1)), and assert
    beta <= OPT.
  * Paragraph after the theorem and Prop prop:filter: a record produced by the
    filtering step (thresholds U_j = value of a feasible point), optionally
    followed by the integer-label filter on coordinates whose grid intervals all
    have length one, is a valid certificate with beta = beta_k; every exact
    minimizer stays in every stage box; U_j >= beta_j holds at every stage.
  * Prop prop:cellwise(c), node bound, at exact minimizers lying on nodes.
Usage: python3 coreA-verify-cert.py [seed] [count]
"""
import itertools
import random
import sys
from fractions import Fraction as Fr


def rand_instance(rng):
    n = rng.randint(1, 3)
    kinds = [rng.choice("CZ") for _ in range(n)]
    lo, hi = [], []
    for _ in kinds:
        a = rng.randint(-3, 1)
        lo.append(Fr(a))
        hi.append(Fr(a + rng.randint(1, 5)))
    H = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        H[i][i] = Fr(rng.randint(-4, 5))
        for j in range(i + 1, n):
            H[i][j] = H[j][i] = Fr(rng.randint(-4, 4), rng.randint(1, 2))
    b = [Fr(rng.randint(-6, 6), rng.randint(1, 3)) for _ in range(n)]
    L = [max(H[i][i], Fr(0)) for i in range(n)]
    return n, kinds, lo, hi, H, b, L


def F(H, b, x):
    n = len(x)
    return sum(Fr(1, 2) * H[i][j] * x[i] * x[j] for i in range(n) for j in range(n)) + sum(
        b[i] * x[i] for i in range(n)
    )


def solve(A, r):
    """Exact Gaussian elimination; returns None if A is singular."""
    m = len(A)
    M = [A[i][:] + [r[i]] for i in range(m)]
    for c in range(m):
        p = next((k for k in range(c, m) if M[k][c] != 0), None)
        if p is None:
            return None
        M[c], M[p] = M[p], M[c]
        for k in range(m):
            if k != c and M[k][c] != 0:
                f = M[k][c] / M[c][c]
                M[k] = [M[k][t] - f * M[c][t] for t in range(m + 1)]
    return [M[i][m] / M[i][i] for i in range(m)]


def exact_opt(n, kinds, lo, hi, H, b):
    """Exact minimum and all candidate minimizers (some minimizer is among them)."""
    C = [i for i in range(n) if kinds[i] == "C"]
    Z = [i for i in range(n) if kinds[i] == "Z"]
    best, arg = None, []
    for zv in itertools.product(*[range(int(lo[i]), int(hi[i]) + 1) for i in Z]):
        for face in itertools.product("lfu", repeat=len(C)):
            x = [Fr(0)] * n
            for i, v in zip(Z, zv):
                x[i] = Fr(v)
            free = []
            for i, f in zip(C, face):
                if f == "l":
                    x[i] = lo[i]
                elif f == "u":
                    x[i] = hi[i]
                else:
                    free.append(i)
            if free:
                A = [[H[i][j] for j in free] for i in free]
                r = [-(b[i] + sum(H[i][j] * x[j] for j in range(n) if j not in free)) for i in free]
                sol = solve(A, r)
                if sol is None:
                    continue
                ok = True
                for i, v in zip(free, sol):
                    if not (lo[i] <= v <= hi[i]):
                        ok = False
                    x[i] = v
                if not ok:
                    continue
            val = F(H, b, x)
            if best is None or val < best:
                best, arg = val, [tuple(x)]
            elif val == best:
                arg.append(tuple(x))
    return best, arg


def eff_width(kind, a, a2):
    return Fr(0) if (kind == "Z" and a2 - a == 1) else a2 - a


def intervals(Gi):
    return [(Gi[0], Gi[0])] if len(Gi) == 1 else [(Gi[k], Gi[k + 1]) for k in range(len(Gi) - 1)]


def stage(n, kinds, H, b, L, G):
    w = []
    for i in range(n):
        wi = {}
        for a, a2 in intervals(G[i]):
            e = eff_width(kinds[i], a, a2)
            for v in (a, a2):
                wi[v] = max(wi.get(v, Fr(0)), e)
        w.append(wi)
    d = [{v: L[i] * w[i][v] ** 2 / 8 for v in G[i]} for i in range(n)]
    Q = {y: F(H, b, y) - sum(d[i][y[i]] for i in range(n)) for y in itertools.product(*G)}
    beta = min(Q.values())
    m = [{v: min(q for y, q in Q.items() if y[i] == v) for v in G[i]} for i in range(n)]
    ystar = min(Q, key=Q.get)
    return d, Q, beta, m, ystar


def rand_grid(rng, kind, a, a2):
    """Grid for [a,a2] (integer points if kind == 'Z'); a == a2 allowed."""
    if a == a2:
        return [a]
    if kind == "Z":
        inner = [Fr(p) for p in range(int(a) + 1, int(a2)) if rng.random() < 0.5]
    else:
        inner = [a + (a2 - a) * Fr(rng.randint(1, 7), 8) for _ in range(rng.randint(0, 3))]
    return sorted(set([a, a2] + inner))


def rand_subinterval(rng, kind, a, a2):
    if a == a2:
        return a, a2
    if kind == "Z":
        pts = list(range(int(a), int(a2) + 1))
        x = rng.choice(pts)
        y = rng.choice([p for p in pts if p >= x])
        return Fr(x), Fr(y)
    x = a + (a2 - a) * Fr(rng.randint(0, 4), 8)
    y = a2 - (a2 - x) * Fr(rng.randint(0, 4), 8)
    return x, y


def best_beta(n, kinds, Gs, stages):
    """Largest beta for which (C1), (C2) of Definition def:cert hold."""
    k = len(Gs) - 1
    req = [min(stages[k][1].values())]
    for j in range(k):
        m = stages[j][3]
        for i in range(n):
            lo1, hi1 = Gs[j + 1][i][0], Gs[j + 1][i][-1]
            for a, a2 in intervals(Gs[j][i]):
                if lo1 <= a and a2 <= hi1:
                    continue
                alt1 = min(m[i][a], m[i][a2])
                alts = [alt1]
                if eff_width(kinds[i], a, a2) == 0:
                    outs = [v for v in {a, a2} if not (lo1 <= v <= hi1)]
                    alts.append(min(m[i][v] for v in outs))
                req.append(max(alts))
    return min(req)


def check_random_certificate(rng, inst, opt):
    n, kinds, lo, hi, H, b, L = inst
    k = rng.randint(0, 3)
    boxes = [list(zip(lo, hi))]
    for _ in range(k):
        boxes.append([rand_subinterval(rng, kinds[i], *boxes[-1][i]) for i in range(n)])
    Gs = [[rand_grid(rng, kinds[i], *box[i]) for i in range(n)] for box in boxes]
    stages = [stage(n, kinds, H, b, L, G) for G in Gs]
    beta = best_beta(n, kinds, Gs, stages)
    assert beta <= opt, ("certificate unsound", beta, opt)


def check_filter_record(rng, inst, opt, minimizers):
    n, kinds, lo, hi, H, b, L = inst
    P = [i for i in range(n) if L[i] > 0]
    box = list(zip(lo, hi))
    Gs, stages = [], []
    incumbent = None
    used_label = False
    for j in range(rng.randint(1, 4)):
        G = [rand_grid(rng, kinds[i], *box[i]) for i in range(n)]
        st = stage(n, kinds, H, b, L, G)
        d, Q, beta, m, ystar = st
        Gs.append(G)
        stages.append(st)
        # every exact minimizer lies in the current box; beta_j <= OPT
        for xs in minimizers:
            assert all(box[i][0] <= xs[i] <= box[i][1] for i in range(n))
            for i in range(n):
                if xs[i] in G[i]:
                    assert opt >= m[i][xs[i]] + d[i][xs[i]], "node bound"
        assert beta <= opt
        fy = F(H, b, ystar)
        incumbent = fy if incumbent is None else min(incumbent, fy)
        U = incumbent
        assert U >= beta  # Definition def:filter requires U >= beta
        new = []
        for i in range(n):
            if i in P:
                ret = [(a, a2) for a, a2 in intervals(G[i]) if min(m[i][a], m[i][a2]) <= U]
                assert ret
                lo1, hi1 = min(a for a, _ in ret), max(a2 for _, a2 in ret)
                assert lo1 <= ystar[i] <= hi1
            else:
                lo1, hi1 = G[i][0], G[i][-1]
            # integer-label filter (appendix-boundary lem:labelfilter(i))
            if kinds[i] == "Z" and all(a2 - a <= 1 for a, a2 in intervals(G[i])) and rng.random() < 0.7:
                keep = [v for v in G[i] if lo1 <= v <= hi1 and m[i][v] <= U]
                assert keep and ystar[i] in keep
                if (min(keep), max(keep)) != (lo1, hi1):
                    used_label = True
                lo1, hi1 = min(keep), max(keep)
            new.append((lo1, hi1))
        box = new
    beta_k = stages[-1][2]
    assert best_beta(n, kinds, Gs, stages) >= beta_k, "filtering record is not a valid certificate"
    assert beta_k <= opt
    return used_label


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    rng = random.Random(seed)
    labels = 0
    for _ in range(count):
        inst = rand_instance(rng)
        n, kinds, lo, hi, H, b, L = inst
        opt, minimizers = exact_opt(n, kinds, lo, hi, H, b)
        for _ in range(3):
            check_random_certificate(rng, inst, opt)
        labels += check_filter_record(rng, inst, opt, minimizers)
    print(f"seed {seed}: {count} instances, {3 * count} random certificates and "
          f"{count} filtering records passed ({labels} records used the label filter)")


if __name__ == "__main__":
    main()
