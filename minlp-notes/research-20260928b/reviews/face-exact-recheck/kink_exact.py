"""Recheck of Propositions 5.4 and 5.5 (kink family) in exact rational arithmetic.

Own code; nothing is imported from the note's directory or from the first review.

Kink family: f = L|x-a| + c(x-a)(y-b) on [0,1]^2, termwise McCormick on c*x*y, f* = 0.

[A] Exact node LP (lifted, vertex enumeration over (x, y, w, t)) on random rational boxes:
    - straddling boxes: LB = -|c| w_y (a-l_x)(u_x-a)/w_x, every optimal vertex has x = a and
      y at relative position rho (c < 0) or 1 - rho (c > 0);
    - non-straddling boxes: LB >= 0 (valid at eps = 0).
    The simulator below uses these closed forms only after they are checked here.
[B] Prop 5.4(b),(d): LP(1,0) and INC take 3 nodes for many a (widest side, ties to x).
[C] Prop 5.4(c): eps-independent bound 1 + 4 beta^-(k0+1)/(1-beta) against exact counts
    (eps = 0 tree where affordable, else small eps), for many a and several beta.
[D] Prop 5.5(ii): a = 1/6, beta = 1/5 counts for the rules of the note's table, and the bound
    0.0745 eps^-1/2.  Also the scout's a = 1/3 rows for SCIPdef.
[E] Prop 5.5(i): Cantor set survivors, measure (2 beta)^k, period-2 point beta/(1+beta).
[F] Points of K_beta with a long run of left steps: nodes*sqrt(eps) is not bounded below
    uniformly on K_beta (the eps^-1/2 rate is specific to orbits like that of 1/6).
[G] Incumbent-branching model: tie-breaking and "incumbent in subdomain" vs "coordinate in interval".
"""
from fractions import Fraction as Fr
import itertools
import math
import random
import sys

sys.setrecursionlimit(10000)


# ----------------------------------------------------------------------------------------------
# exact linear algebra and the lifted node LP
# ----------------------------------------------------------------------------------------------
def solve_lin(A, b):
    n = len(A)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for col in range(n):
        piv = next((r for r in range(col, n) if M[r][col] != 0), None)
        if piv is None:
            return None
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        for r in range(n):
            if r != col and M[r][col] != 0:
                f = M[r][col] / pv
                M[r] = [M[r][k] - f * M[col][k] for k in range(n + 1)]
    return [M[i][n] / M[i][i] for i in range(n)]


def kink_lp(box, a, b, L, c):
    """min L t + c w - c b x - c a y + c a b over McCormick(w = xy), t >= |x - a|, box.
    Returns (value, list of optimal vertices (x, y, w, t))."""
    lx, ux, ly, uy = box
    G, h = [], []

    def add(row, rhs):
        G.append(row); h.append(rhs)
    add([1, 0, 0, 0], lx); add([-1, 0, 0, 0], -ux); add([0, 1, 0, 0], ly); add([0, -1, 0, 0], -uy)
    add([-ly, -lx, 1, 0], -lx * ly)          # w >= ly x + lx y - lx ly
    add([-uy, -ux, 1, 0], -ux * uy)          # w >= uy x + ux y - ux uy
    add([uy, lx, -1, 0], lx * uy)            # w <= uy x + lx y - lx uy
    add([ly, ux, -1, 0], ux * ly)            # w <= ly x + ux y - ux ly
    add([-1, 0, 0, 1], -a); add([1, 0, 0, 1], a)   # t >= |x - a|
    obj = [-c * b, -c * a, c, L]
    best, arg = None, []
    for S in itertools.combinations(range(len(G)), 4):
        sol = solve_lin([G[i] for i in S], [h[i] for i in S])
        if sol is None:
            continue
        if all(sum(G[i][k] * sol[k] for k in range(4)) >= h[i] for i in range(len(G))):
            val = sum(obj[k] * sol[k] for k in range(4)) + c * a * b
            if best is None or val < best:
                best, arg = val, [tuple(sol)]
            elif val == best and tuple(sol) not in arg:
                arg.append(tuple(sol))
    return best, arg


def rand_frac(rng, den=97):
    return Fr(rng.randint(0, den), den)


def part_A():
    print("[A] exact node LP vs closed form (random rational boxes)")
    rng = random.Random(20260929)
    cases = [(Fr(2), Fr(-1), Fr(41, 99)), (Fr(2), Fr(1), Fr(41, 99)), (Fr(1), Fr(-3, 2), Fr(1, 2)),
             (Fr(3, 4), Fr(1, 2), Fr(1, 3))]
    for (L, c, b) in cases:
        assert L > abs(c) * max(b, 1 - b)
        nstr = nnon = 0
        bad = 0
        for trial in range(120):
            a = Fr(rng.randint(1, 96), 97)
            lx, ux = sorted([rand_frac(rng), rand_frac(rng)])
            ly, uy = sorted([rand_frac(rng), rand_frac(rng)])
            if trial % 3 == 0:   # force straddling
                lx, ux = a - Fr(rng.randint(1, 40), 97), a + Fr(rng.randint(1, 40), 97)
                lx, ux = max(lx, Fr(0)), min(ux, Fr(1))
            if lx == ux or ly == uy:
                continue
            val, arg = kink_lp((lx, ux, ly, uy), a, b, L, c)
            if lx < a < ux:
                nstr += 1
                wx, wy = ux - lx, uy - ly
                rho = (a - lx) / wx
                pred = -abs(c) * wy * (a - lx) * (ux - a) / wx
                ry = rho if c < 0 else 1 - rho
                ok = (val == pred and all(v[0] == a for v in arg)
                      and all(v[1] == ly + ry * wy for v in arg))
            else:
                nnon += 1
                ok = val >= 0
            bad += (not ok)
        print(f"    L={L}, c={c}, b={b}: straddling {nstr}, non-straddling {nnon}, mismatches {bad}")


# ----------------------------------------------------------------------------------------------
# exact kink branch-and-bound simulator (closed forms checked in [A])
# ----------------------------------------------------------------------------------------------
def clamp(p, lo, hi):
    return min(max(p, lo), hi)


def simulate(a, eps, point, select="wx", c=Fr(-1), cap=10**6, inc=None, inc_model="coord",
             want_levels=False):
    """Processed nodes (root + all children of non-pruned nodes).  Non-straddling boxes are valid
    (checked in [A]); a straddling box is pruned iff |c| w_y (a-l)(u-a)/w_x <= eps.
    point: ('LP', beta) | ('bis',) | ('SCIP',) | ('INC',)
    select: 'wx' widest, ties to x; 'wy' widest, ties to y; 'x' always x."""
    stack = [(Fr(0), Fr(1), Fr(0), Fr(1))]
    nodes = 0
    while stack:
        lx, ux, ly, uy = stack.pop()
        nodes += 1
        if nodes > cap:
            return None
        if not (lx < a < ux):
            continue
        wx, wy = ux - lx, uy - ly
        if abs(c) * wy * (a - lx) * (ux - a) / wx <= eps:
            continue
        rho = (a - lx) / wx
        ry = rho if c < 0 else 1 - rho
        if select == "wx":
            var = "y" if wy > wx else "x"
        elif select == "wy":
            var = "x" if wx > wy else "y"
        else:
            var = "x"
        lo, hi, xh = (lx, ux, a) if var == "x" else (ly, uy, ly + ry * wy)
        w = hi - lo
        mid = (lo + hi) / 2
        kind = point[0]
        if kind == "LP":
            beta = point[1]
            p = clamp(xh, lo + beta * w, hi - beta * w)
        elif kind == "bis":
            p = mid
        elif kind == "SCIP":
            r = w            # relative width (root is the unit square)
            mp = Fr(3, 4) if r >= Fr(1, 2) else Fr(3, 4) * r
            p = clamp(mp * mid + (1 - mp) * xh, lo + Fr(1, 5) * w, hi - Fr(1, 5) * w)
        elif kind == "INC":
            xs, ys = inc
            s = xs if var == "x" else ys
            inside = lo < s < hi
            if inc_model == "box":
                inside = inside and (lx <= xs <= ux) and (ly <= ys <= uy)
            p = s if inside else mid
        else:
            raise ValueError(kind)
        if not (lo < p < hi):
            p = mid
        if var == "x":
            stack.append((lx, p, ly, uy)); stack.append((p, ux, ly, uy))
        else:
            stack.append((lx, ux, ly, p)); stack.append((lx, ux, p, uy))
    return nodes


def k0_of(a, beta, kmax=200):
    rho = a
    for k in range(kmax):
        if beta <= rho <= 1 - beta:
            return k
        rho = rho / beta if rho < beta else (rho - 1 + beta) / beta
    return None


def bound_c(k0, beta):
    return 1 + 4 * beta ** (-(k0 + 1)) / (1 - beta)


EPS = [Fr(1, 10 ** k) for k in range(2, 9)]


def part_B():
    print("[B] Prop 5.4(b),(d): LP(1,0) and INC (incumbent (a, 1/2)), widest side ties to x")
    rng = random.Random(7)
    avals = [Fr(1, 3), Fr(1, 6), Fr(1, 5), Fr(199, 1000), Fr(1, 2)] + \
        [Fr(rng.randint(1, 9999), 10000) for _ in range(60)]
    worst = {}
    for rule, pt in [("LP(1,0)", ("LP", Fr(0))), ("INC", ("INC",))]:
        counts = set()
        for a in avals:
            for eps in (Fr(1, 100), Fr(1, 10 ** 6), Fr(0)):
                n = simulate(a, eps, pt, "wx", inc=(a, Fr(1, 2)))
                counts.add(n)
        worst[rule] = counts
        print(f"    {rule:8s}: distinct node counts over {len(avals)} values of a and eps in "
              f"{{1e-2, 1e-6, 0}}: {sorted(counts)}")


def part_C():
    print("[C] Prop 5.4(c): exact counts vs 1 + 4 beta^-(k0+1)/(1-beta)")
    rng = random.Random(11)
    for beta in (Fr(1, 5), Fr(1, 10), Fr(3, 10), Fr(9, 20)):
        avals = [beta - Fr(1, 10 ** j) for j in range(1, 7)] + [1 - beta + Fr(1, 10 ** j) for j in range(1, 7)]
        avals += [Fr(rng.randint(1, 99999), 100000) for _ in range(40)]
        avals = [a for a in avals if 0 < a < 1]
        worst_ratio, viol, rows = Fr(0), 0, []
        for a in avals:
            k0 = k0_of(a, beta)
            B = bound_c(k0, beta)
            eps = Fr(0) if B < 3 * 10 ** 5 else Fr(1, 10 ** 8)
            n = simulate(a, eps, ("LP", beta), "wx", cap=400000)
            if n is None:
                rows.append((a, k0, None, B)); continue
            viol += n > B
            worst_ratio = max(worst_ratio, Fr(n) / B)
            rows.append((a, k0, n, B, eps))
        print(f"    beta={beta}: {len(avals)} values of a, violations {viol}, max count/bound "
              f"{float(worst_ratio):.3f}")
        for r in rows[:12]:
            if r[2] is None:
                print(f"       a={float(r[0]):.7f} k0={r[1]} count>cap bound={float(r[3]):.0f}")
            else:
                print(f"       a={float(r[0]):.7f} k0={r[1]:2d} nodes={r[2]:7d} (eps={r[4]}) "
                      f"bound={float(r[3]):.0f}")
    print("    note's example a = 0.1999, beta = 1/5 (k0 = 5): nodes at eps = 1e-4, 1e-6, 1e-8, 0:",
          [simulate(Fr(1999, 10000), e, ("LP", Fr(1, 5)), "wx") for e in
           (Fr(1, 10 ** 4), Fr(1, 10 ** 6), Fr(1, 10 ** 8), Fr(0))],
          " k0 =", k0_of(Fr(1999, 10000), Fr(1, 5)), " bound =", float(bound_c(5, Fr(1, 5))))


def part_D():
    print("[D] Prop 5.5(ii): a = 1/6, beta = 1/5, c = -1 (counts at eps = 1e-2 .. 1e-8)")
    a = Fr(1, 6)
    rules = [("LP(1,.2) w", ("LP", Fr(1, 5)), "wx"), ("LP(1,.2) x", ("LP", Fr(1, 5)), "x"),
             ("SCIPdef w", ("SCIP",), "wx"), ("bisect", ("bis",), "wx"),
             ("LP(1,0) w", ("LP", Fr(0)), "wx"), ("LP(1,.1) w", ("LP", Fr(1, 10)), "wx"),
             ("INC w", ("INC",), "wx")]
    for name, pt, sel in rules:
        row = [simulate(a, e, pt, sel, inc=(a, Fr(1, 2))) for e in EPS]
        print(f"    {name:11s} {row}")
    lb = [0.2 * (7.2 * float(e)) ** -0.5 for e in EPS]
    row = [simulate(a, e, ("LP", Fr(1, 5)), "wx") for e in EPS]
    print("    proved bound 0.0745 eps^-1/2:", [f"{0.0745 * float(e) ** -0.5:.1f}" for e in EPS])
    print("    (1/5)(7.2 eps)^-1/2        :", [f"{v:.1f}" for v in lb])
    print("    LP(1,.2)w / bound          :", [f"{n / (0.0745 * float(e) ** -0.5):.1f}" for n, e in zip(row, EPS)])
    # proof step 6: the level-k count 5^k with k = max{k : 5^(-2k) >= 7.2 eps}
    ks = []
    for e in EPS:
        k = 0
        while Fr(1, 5 ** (2 * (k + 1))) >= Fr(36, 5) * e:
            k += 1
        ks.append((k, 5 ** k))
    print("    (k, 5^k) of the proof      :", ks)
    print("    scout's a = 1/3: SCIPdef w", [simulate(Fr(1, 3), e, ("SCIP",), "wx") for e in EPS[:5]],
          " SCIPdef x", [simulate(Fr(1, 3), e, ("SCIP",), "x") for e in EPS[:5]],
          " bisect", [simulate(Fr(1, 3), e, ("bis",), "wx") for e in EPS[:5]],
          " LP(1,.2)w", [simulate(Fr(1, 3), e, ("LP", Fr(1, 5)), "wx") for e in EPS[:5]])


def part_E():
    print("[E] Prop 5.5(i): Cantor set K_beta")
    for beta in (Fr(1, 5), Fr(1, 10), Fr(1, 3), Fr(9, 20)):
        ivs = [(Fr(0), Fr(1))]
        for k in range(1, 9):
            new = []
            for (l, u) in ivs:
                w = u - l
                new += [(l, l + beta * w), (u - beta * w, u)]
            ivs = new
            meas = sum(u - l for l, u in ivs)
            assert meas == (2 * beta) ** k and len(ivs) == 2 ** k
        p = beta / (1 + beta)
        T = lambda r: r / beta if r < beta else (r - 1 + beta) / beta
        q = T(p)
        print(f"    beta={beta}: 2^k survivor intervals of total length (2 beta)^k for k<=8: ok; "
              f"beta/(1+beta)={p} -> {q} -> {T(q)}; outer both times: {p < beta and q > 1 - beta}; "
              f"dim = log2/log(1/beta) = {math.log(2) / math.log(1 / float(beta)):.4f}")


def part_F():
    print("[F] K_beta points with a run of m left steps (beta = 1/5, LP(1,.2), widest side)")
    beta = Fr(1, 5)
    eps_list = [Fr(1, 10 ** k) for k in range(2, 11)]
    for m in (0, 4, 8):
        r = beta ** m / 6                      # m left steps lead to 1/6 (period 2)
        a = beta * (1 - beta + beta * r)       # prefix: left, then right
        assert k0_of(a, beta, 400) is None
        row = [simulate(a, e, ("LP", beta), "wx", cap=300000) for e in eps_list]
        sc = [f"{n * float(e) ** 0.5:.4f}" if n else "cap" for n, e in zip(row, eps_list)]
        print(f"    m={m}: a={float(a):.12f}  nodes={row}")
        print(f"           nodes*sqrt(eps)={sc}")


def part_G():
    print("[G] incumbent branching model on the kink, a = 1/3 (counts at eps = 1e-2 .. 1e-6)")
    a = Fr(1, 3)
    E = EPS[:5]
    cases = [("ties x, inc (a,1/2), coord", "wx", (a, Fr(1, 2)), "coord"),
             ("ties x, inc (a,0),   box  ", "wx", (a, Fr(0)), "box"),
             ("ties y, inc (a,1/2), coord", "wy", (a, Fr(1, 2)), "coord"),
             ("ties y, inc (a,1/2), box  ", "wy", (a, Fr(1, 2)), "box"),
             ("ties y, inc (a,0),   coord", "wy", (a, Fr(0)), "coord"),
             ("ties y, inc (a,0),   box  ", "wy", (a, Fr(0)), "box")]
    for name, sel, inc, model in cases:
        print(f"    {name}: {[simulate(a, e, ('INC',), sel, inc=inc, inc_model=model) for e in E]}")
    print("    bisection ties y         :", [simulate(a, e, ("bis",), "wy") for e in E])




def simulate_float(a, eps, beta, cap=10**6):
    """Same rule as simulate(..., ('LP', beta), 'wx') but in binary floating point, to test whether
    the small differences from the note's LP(1,.2)w counts come from floating-point width ties."""
    stack = [(0.0, 1.0, 0.0, 1.0)]
    nodes = ties = 0
    while stack:
        lx, ux, ly, uy = stack.pop()
        nodes += 1
        if not (lx < a < ux):
            continue
        wx, wy = ux - lx, uy - ly
        if wy * (a - lx) * (ux - a) / wx <= eps:
            continue
        rho = (a - lx) / wx
        ties += abs(wy - wx) <= 1e-12 * wx and wy != wx
        var = "y" if wy > wx else "x"
        lo, hi, xh = (lx, ux, a) if var == "x" else (ly, uy, ly + rho * wy)
        w = hi - lo
        p = min(max(xh, lo + beta * w), hi - beta * w)
        if var == "x":
            stack.append((lx, p, ly, uy)); stack.append((p, ux, ly, uy))
        else:
            stack.append((lx, ux, ly, p)); stack.append((lx, ux, p, uy))
    return nodes, ties


def part_H():
    print("[H] floating-point replay of LP(1,.2)w at a = 1/6 (float widths, ties broken by rounding)")
    row = [simulate_float(1 / 6, 10.0 ** -k, 0.2) for k in range(2, 9)]
    print("    float nodes :", [n for n, _ in row])
    print("    near-ties with wy != wx in floats:", [t for _, t in row])
    print("    exact nodes :", [simulate(Fr(1, 6), e, ("LP", Fr(1, 5)), "wx") for e in EPS])
    print("    a = 0.1999 float at 1e-8:", simulate_float(0.1999, 1e-8, 0.2)[0],
          " exact:", simulate(Fr(1999, 10000), Fr(1, 10 ** 8), ("LP", Fr(1, 5)), "wx"))


if __name__ == "__main__":
    parts = sys.argv[1:] or ["A", "B", "C", "D", "E", "F", "G", "H"]
    for p in parts:
        {"A": part_A, "B": part_B, "C": part_C, "D": part_D, "E": part_E, "F": part_F, "G": part_G,
         "H": part_H}[p]()
        sys.stdout.flush()
