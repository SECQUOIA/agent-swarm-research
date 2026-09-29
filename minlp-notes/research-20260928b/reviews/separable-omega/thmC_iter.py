"""Does the ambiguity of Theorem C iterate?  (Review check; the note says it is open.)

Corner-node argument.  Call a node a *corner node* if each of its coordinate intervals contains
0 or 1 (it contains a corner of [0,1]^n).  Let S(v) be the set of coordinates cut on the path
to v.  For i not in S(v):
  (a) the node data (box, relaxation value, minimizer, germ of f at the minimizer, f near every
      corner of the box, incumbent) are identical in all A_i with i not in S(v);
  (b) v is invalid in A_i: value <= -n c + eps (1 + |S|/(2(n-1))) < 0.
So a deterministic rule follows one reference tree on all i-free nodes.  Cutting an uncut
coordinate gives two corner children; re-cutting gives one.  With N_i = number of corner nodes v
with i not in S(v) (all internal in A_i), T(A_i) >= 2 N_i + 1, and
  sum_i N_i >= sum_{d=0}^{n-1} 2^d (n - d) = 2^{n+1} - n - 2.
Hence max_i T(A_i) >= 2 G(n) + 1 with G(n) the min-max of N_i over reference trees, and every
randomized rule has E[T] >= 2 (2^{n+1} - n - 2)/n + 1 on some A_i (Yao, uniform i).

This script: (1) computes G(n) exactly by a Pareto DP; (2) checks (a) and (b) exactly on random
corner nodes; (3) simulates exact runs of explicit rules (omega, and a 'balanced' rule that
realizes G(n)) on all A_i for n = 2, 3, 4.
"""
import itertools
import random
from fractions import Fraction as Fr
from sepcore import PL
from thmC_check import lines, EPS

H2 = Fr(1, 2)


def pareto(vecs):
    vecs = sorted(set(vecs))
    out = []
    for v in vecs:
        if not any(all(a <= b for a, b in zip(w, v)) for w in out):
            out = [w for w in out if not all(a <= b for a, b in zip(v, w))] + [v]
    return out


def achievable(m, memo={}):
    """Pareto-minimal vectors (N_i) over reference corner trees with m uncut coordinates."""
    if m in memo:
        return memo[m]
    if m == 1:
        memo[1] = [(1,)]
        return memo[1]
    sub = achievable(m - 1)
    res = []
    for j in range(m):
        others = [k for k in range(m) if k != j]
        for Lv in sub:
            for Rv in sub:
                v = [0] * m
                v[j] = 1
                for pos, k in enumerate(others):
                    v[k] = 1 + Lv[pos] + Rv[pos]
                res.append(tuple(v))
    # close under permutations is automatic (j ranges over all, sub is perm-closed)
    memo[m] = pareto(res)
    return memo[m]


def value(n, r0, box, i):
    """relaxation value + eps of `box` in A_i (0-based i)."""
    LR, LN, _ = lines(n, EPS, r0)
    R, N = PL.from_lines(LR), PL.from_lines(LN)
    return sum((R if k == i else N).node(*box[k])[0] for k in range(n)) + EPS


def node_data(n, r0, box, i):
    LR, LN, _ = lines(n, EPS, r0)
    R, N = PL.from_lines(LR), PL.from_lines(LN)
    cs = [R if k == i else N for k in range(n)]
    d = [c.node(*iv) for c, iv in zip(cs, box)]
    y = tuple(x[1] for x in d)
    val = sum(x[0] for x in d)
    # germ at y: f on a small cube around y (sampled exactly on a 5^n grid of offsets)
    h = Fr(1, 10 ** 5)
    germ = tuple(sum(c.m(min(max(t + s * h, c.L), c.U)) for c, t, s in zip(cs, y, off))
                 for off in itertools.product(range(-2, 3), repeat=n))
    corners = tuple(sum(c.m(min(max(v + s * h, c.L), c.U)) for c, v, s in zip(cs, cn, off))
                    for cn in itertools.product(*[(l, u) for l, u in box])
                    for off in itertools.product((-1, 0, 1), repeat=n))
    return (box, val, y, germ, corners)


def check_corner_nodes(n, r0, trials, rng):
    """random corner nodes with cut set S != all; check (a) and (b)."""
    bad = 0
    worst = None
    for _ in range(trials):
        S = rng.sample(range(n), rng.randint(0, n - 1))
        box = []
        for k in range(n):
            if k in S:
                p = Fr(rng.randint(1, 999), 1000)
                box.append((Fr(0), p) if rng.random() < 0.5 else (p, Fr(1)))
            else:
                box.append((Fr(0), Fr(1)))
        box = tuple(box)
        free = [i for i in range(n) if i not in S]
        datas = {node_data(n, r0, box, i) for i in free}
        vals = [value(n, r0, box, i) for i in free]
        if len(datas) != 1 or max(vals) >= 0:
            bad += 1
        worst = max(vals) if worst is None else max(worst, max(vals))
    return bad, worst


def run_rule(n, r0, i, choose, cap=10 ** 5):
    """exact run on A_i of a rule splitting at the relaxation minimizer along choose(box, d)."""
    LR, LN, _ = lines(n, EPS, r0)
    R, N = PL.from_lines(LR), PL.from_lines(LN)
    cs = [R if k == i else N for k in range(n)]
    st = [tuple((c.L, c.U) for c in cs)]
    nodes = 0
    while st:
        box = st.pop()
        nodes += 1
        assert nodes < cap
        d = [c.node(*iv) for c, iv in zip(cs, box)]
        if sum(x[0] for x in d) + EPS >= 0:
            continue
        k = choose(box, d)
        l, u = box[k]
        y = d[k][1]
        if not (l < y < u):
            y = (l + u) / 2
        for iv in ((l, y), (y, u)):
            b = list(box); b[k] = iv
            st.append(tuple(b))
    return nodes


def omega_choose(box, d):
    return max(range(len(d)), key=lambda k: (d[k][2], -k))


def balanced_choose_factory(n):
    """reference strategy: at a corner node, cut an uncut coordinate chosen by a fixed map from
    the pattern of (cut coordinate, side); realizes G(n) for n <= 4 via the DP's witness."""
    # build witness tree: for each state (tuple of (coord, side) in order) choose coordinate
    wit = {}

    def best(U):
        # returns (vector over U as dict, plan) minimizing max; brute force over small U
        U = tuple(U)
        if len(U) == 1:
            return {U[0]: 1}, (U[0], None, None)
        bestv = None
        for j in U:
            rest = [k for k in U if k != j]
            opts = best_all(tuple(rest))
            for Lv, Lp in opts:
                for Rv, Rp in opts:
                    v = {j: 1}
                    for k in rest:
                        v[k] = 1 + Lv[k] + Rv[k]
                    key = max(v.values())
                    if bestv is None or key < bestv[0]:
                        bestv = (key, v, (j, Lp, Rp))
        return bestv[1], bestv[2]

    def best_all(U, memo={}):
        if U in memo:
            return memo[U]
        if len(U) == 1:
            memo[U] = [({U[0]: 1}, (U[0], None, None))]
            return memo[U]
        res = []
        for j in U:
            rest = tuple(k for k in U if k != j)
            for Lv, Lp in best_all(rest):
                for Rv, Rp in best_all(rest):
                    v = {j: 1}
                    for k in rest:
                        v[k] = 1 + Lv[k] + Rv[k]
                    res.append((v, (j, Lp, Rp)))
        # keep Pareto-minimal
        keep = []
        for v, p in sorted(res, key=lambda z: sorted(z[0].values())):
            vv = tuple(v[k] for k in U)
            if not any(all(a <= b for a, b in zip(tuple(w[k] for k in U), vv)) for w, _ in keep):
                keep.append((v, p))
        memo[U] = keep
        return keep

    vec, plan = best(range(n))

    def choose(box, d):
        # walk the plan along the cut history encoded in the box (corner nodes only)
        p = plan
        cut = {k for k in range(n) if box[k] != (Fr(0), Fr(1))}
        visited = []
        while p is not None:
            j, Lp, Rp = p
            if j not in cut:
                return j
            p = Lp if box[j][0] == 0 else Rp
        # non-corner or fully cut: fall back to omega
        return omega_choose(box, d)
    return vec, choose


if __name__ == "__main__":
    print("(1) G(n) = min over reference corner trees of max_i N_i; averaging bound (2^{n+1}-n-2)/n")
    for n in range(2, 6):
        A = achievable(n)
        G = min(max(v) for v in A)
        avg = Fr(2 ** (n + 1) - n - 2, n)
        print(f"  n={n}: G={G}  -> deterministic T >= {2 * G + 1}, ratio >= {Fr(2 * G + 1, 3)} = {float(Fr(2*G+1,3)):.3f}; "
              f"randomized E[T] >= {2 * avg + 1} ratio >= {float((2 * avg + 1) / 3):.3f}; "
              f"note: 7/3 and {float(Fr(7, 3) - Fr(4, 3 * n)):.3f}; |Pareto|={len(A)}")
    for n in (6, 8, 10, 16):
        avg = Fr(2 ** (n + 1) - n - 2, n)
        print(f"  n={n}: averaging bound only: deterministic ratio >= {float((2 * (avg.__ceil__()) + 1) / 3):.1f}, "
              f"randomized >= {float((2 * avg + 1) / 3):.1f}")
    rng = random.Random(7)
    print("(2) random corner nodes: identical data for all free i, and invalid in A_i")
    for n in (2, 3, 4):
        for r0 in (Fr(1, 4) - Fr(1, 5 * n),) + ((Fr(n - 1, 4 * n) + Fr(1, 50),) if n > 2 else ()):
            bad, worst = check_corner_nodes(n, r0, 150 if n < 4 else 60, rng)
            print(f"  n={n} r0={r0}: violations {bad}; max value+eps over free i = {worst}")
    print("(3) exact runs on all A_i (T = number of nodes)")
    for n in (2, 3, 4):
        r0 = Fr(1, 4) - Fr(1, 5 * n)
        om = [run_rule(n, r0, i, omega_choose) for i in range(n)]
        vec, ch = balanced_choose_factory(n)
        ba = [run_rule(n, r0, i, ch) for i in range(n)]
        print(f"  n={n}: omega (ties to lowest index) T on A_1..A_n = {om} (max {max(om)} = 2^(n+1)-1: {max(om) == 2 ** (n + 1) - 1}); "
              f"balanced rule T = {ba} (max {max(ba)}, predicted 2G+1 = {2 * max(vec.values()) + 1})")
    for n in (3, 4, 6):
        r0 = Fr(n - 1, 4 * n) + Fr(1, 50)
        om = [run_rule(n, r0, i, omega_choose) for i in range(n)]
        print(f"  author's r0, n={n}: omega T on A_1..A_n = {om}")
