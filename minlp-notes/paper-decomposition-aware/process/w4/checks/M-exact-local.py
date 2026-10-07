"""M-exact check 2: Section 6.5 and Appendix B.1 in exact arithmetic.

Own implementation (not experiments/, not w3 checks) of TRIAL with a common
mesh (Lemma lem:commonmesh): graded grids, corrections L_i w^2/8, brute-force
corrected minimum and min-marginals over the product grid (integer-scaled),
filtering with threshold U. At every stage that ends by filtering we build the
narrowed box of Prop prop:local, the face candidate of Def def:facecand, and
run the test. Checks:
  S1  y_j lies in the narrowed box (text before Def facecand);
  S2  soundness: whenever the test passes (with hypotheses x~ in X~, F(x~)<=U),
      the candidate is optimal -- on ALL instances (also several minimizers,
      also trials with 8 kappa theta^2 > 1);
  S3  Lemma lem:node(a): every grid point x of X^{(j)} ... (checked on the
      optimal points: x*_i in Z_i for integer i);
  C1  Cor cor:local at stages with h_j <= h* (unique minimizer, g certified by
      Lemma lem:growthcert(a)): X~_i = {x*_i} for integer i and i not in P,
      J_+ = J_0 cup A, J = J_0, candidate exists and equals x*, test passes;
  C2  first accepting stage <= least j with h_j <= h*  (stage count).
"""
import itertools
import math
import sys
from fractions import Fraction as Fr
from pathlib import Path
from random import Random

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'experiments'))
from oracle import exact_minimum  # noqa: E402


def val(H, b, c, x):
    n = len(x)
    return sum(H[i][j] * x[i] * x[j] for i in range(n) for j in range(n)) / 2 + \
        sum(b[i] * x[i] for i in range(n)) + c


def grad(H, b, x):
    n = len(x)
    return [sum(H[i][j] * x[j] for j in range(n)) + b[i] for i in range(n)]


def det(M):
    M = [list(r) for r in M]
    n = len(M)
    d = Fr(1)
    for k in range(n):
        p = next((i for i in range(k, n) if M[i][k] != 0), None)
        if p is None:
            return Fr(0)
        if p != k:
            M[k], M[p] = M[p], M[k]
            d = -d
        d *= M[k][k]
        for i in range(k + 1, n):
            f = M[i][k] / M[k][k]
            for j in range(k, n):
                M[i][j] -= f * M[k][j]
    return d


def is_psd(M):
    n = len(M)
    for k in range(1, n + 1):
        for S in itertools.combinations(range(n), k):
            if det([[M[i][j] for j in S] for i in S]) < 0:
                return False
    return True


def solve(M, r):
    n = len(M)
    rows = [list(M[i]) + [r[i]] for i in range(n)]
    for col in range(n):
        p = next((k for k in range(col, n) if rows[k][col] != 0), None)
        if p is None:
            return None
        rows[col], rows[p] = rows[p], rows[col]
        pv = rows[col][col]
        rows[col] = [v / pv for v in rows[col]]
        for k in range(n):
            if k != col and rows[k][col] != 0:
                f = rows[k][col]
                rows[k] = [a - f * bb for a, bb in zip(rows[k], rows[col])]
    return [rows[i][n] for i in range(n)]


def graded_grid(lo, hi, c, h, theta, integer):
    def step(t):
        if integer:
            return max(1, math.floor(h + theta * t))
        return h + theta * t
    nodes = {c}
    for side, end in ((1, hi - c), (-1, c - lo)):
        t = Fr(0)
        while t < end:
            t = min(t + step(t), end)
            nodes.add(c + side * t)
    return sorted(nodes)


def eff_widths(G, integer):
    w = {}
    for k, v in enumerate(G):
        best = Fr(0)
        for a, a2 in ((G[k - 1], v) if k > 0 else (None, None), (v, G[k + 1]) if k + 1 < len(G) else (None, None)):
            if a is None:
                continue
            L = a2 - a
            if integer and L == 1:
                L = Fr(0)
            best = max(best, L)
        w[v] = best
    return w


def lcm(a, b):
    return a * b // math.gcd(a, b)


def stage_tables(H, b, c, Ls, grids, ints):
    """Return beta, a minimizer y, min-marginals m[i][v] (Fractions)."""
    n = len(grids)
    D = 1
    for G in grids:
        for v in G:
            D = lcm(D, v.denominator)
    T = 1
    for i in range(n):
        for j in range(n):
            T = lcm(T, H[i][j].denominator)
        T = lcm(T, b[i].denominator)
        T = lcm(T, (Ls[i] / 4).denominator)
    T = lcm(T, c.denominator)
    S = 2 * T * D * D
    Hi = [[int(T * H[i][j]) for j in range(n)] for i in range(n)]
    bi = [int(2 * T * D * b[i]) for i in range(n)]
    ci = int(2 * T * D * D * c)
    Y = [[int(v * D) for v in G] for G in grids]
    widths = [eff_widths(G, i in ints) for i, G in enumerate(grids)]
    # unary part: H_ii Y^2 + b_i Y - corr
    unary = []
    for i, G in enumerate(grids):
        u = []
        for k, v in enumerate(G):
            Wd = int(widths[i][v] * D)
            corr = int(T * Ls[i] / 4) * Wd * Wd  # S*L w^2/8 = 2TD^2 L w^2/8 = T L/4 (wD)^2
            assert Fr(corr, S) == Ls[i] * widths[i][v] ** 2 / 8
            u.append(Hi[i][i] * Y[i][k] * Y[i][k] + bi[i] * Y[i][k] - corr)
        unary.append(u)
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    best = None
    arg = None
    mm = [[None] * len(G) for G in grids]
    for idx in itertools.product(*[range(len(G)) for G in grids]):
        q = ci
        for i in range(n):
            q += unary[i][idx[i]]
        for i, j in pairs:
            q += 2 * Hi[i][j] * Y[i][idx[i]] * Y[j][idx[j]]
        if best is None or q < best:
            best, arg = q, idx
        for i in range(n):
            cur = mm[i][idx[i]]
            if cur is None or q < cur:
                mm[i][idx[i]] = q
    beta = Fr(best, S)
    y = [grids[i][arg[i]] for i in range(n)]
    m = [{grids[i][k]: Fr(mm[i][k], S) for k in range(len(grids[i]))} for i in range(n)]
    return beta, y, m


def run_trial(inst, theta, cap, stages, on_stage):
    H, b, c, lo, hi, ints = inst
    n = len(b)
    Ls = [max(H[i][i], Fr(0)) for i in range(n)]
    P = [i for i in range(n) if Ls[i] > 0]
    s = max(hi[i] - lo[i] for i in range(n))
    box = [(lo[i], hi[i]) for i in range(n)]
    center = list(lo)
    U = val(H, b, c, lo)
    xhat = list(lo)
    for j in range(stages + 1):
        h = s / 2 ** j
        grids = []
        for i in range(n):
            if i in P:
                G = graded_grid(box[i][0], box[i][1], center[i], h, theta, i in ints)
                if len(G) > cap:
                    return 'abort', j
            else:
                G = [lo[i], hi[i]]
            grids.append(G)
        beta, y, m = stage_tables(H, b, c, Ls, grids, ints)
        fy = val(H, b, c, y)
        if fy < U:
            U, xhat = fy, list(y)
        if U - beta <= 0:
            return 'success', j
        newbox = []
        for i in range(n):
            if i in P:
                G = grids[i]
                keep = [(G[k], G[k + 1]) for k in range(len(G) - 1) if min(m[i][G[k]], m[i][G[k + 1]]) <= U]
                if len(G) == 1:
                    keep = [(G[0], G[0])]
                newbox.append((min(a for a, _ in keep), max(a2 for _, a2 in keep)))
            else:
                newbox.append(box[i])
        on_stage(j, h, grids, m, y, U, beta, box, newbox, Ls, P)
        box = newbox
        center = y
    return 'limit', stages


def narrowed_and_candidate(inst, grids, m, y, U, newbox, Ls, P):
    H, b, c, lo, hi, ints = inst
    n = len(b)
    Xt = []
    for i in range(n):
        G = grids[i]
        if i in ints and i in P:
            Z = set(v for v in G if m[i][v] <= U)
            for k in range(len(G) - 1):
                a, a2 = G[k], G[k + 1]
                if a2 - a >= 2 and min(m[i][a], m[i][a2]) <= U:
                    Z.update(Fr(z) for z in range(int(a) + 1, int(a2)))
            Z = [z for z in Z if newbox[i][0] <= z <= newbox[i][1]]
            Xt.append((min(Z), max(Z)) if Z else None)
        elif i not in P:
            a, a2 = G[0], G[1]
            if m[i][a] > U >= m[i][a2]:
                Xt.append((a2, a2))
            elif m[i][a2] > U >= m[i][a]:
                Xt.append((a, a))
            else:
                Xt.append((lo[i], hi[i]))
        else:
            Xt.append(newbox[i])
    if any(t is None for t in Xt):
        return Xt, None, None
    Jp = [i for i in range(n) if Xt[i][1] > Xt[i][0]]
    x = [None] * n
    free = []
    for i in range(n):
        if i in ints or i not in Jp:
            x[i] = y[i]
        else:
            if Xt[i][0] <= lo[i] <= Xt[i][1]:
                x[i] = lo[i]
            elif Xt[i][0] <= hi[i] <= Xt[i][1]:
                x[i] = hi[i]
            else:
                free.append(i)
    if free:
        fixed = [i for i in range(n) if i not in free]
        M = [[H[i][j] for j in free] for i in free]
        r = [-b[i] - sum(H[i][j] * x[j] for j in fixed) for i in free]
        sol = solve(M, r)
        if sol is None:
            return Xt, None, (Jp, free)
        for i, v in zip(free, sol):
            x[i] = v
    return Xt, x, (Jp, free)


def local_test(inst, Xt, x, U):
    H, b, c, lo, hi, ints = inst
    n = len(b)
    if any(not (Xt[i][0] <= x[i] <= Xt[i][1]) for i in range(n)):
        return False, 'not in box'
    if any(i in ints and x[i].denominator != 1 for i in range(n)):
        return False, 'not integer'
    if val(H, b, c, x) > U:
        return False, 'F>U'
    z = grad(H, b, x)
    Jp = [i for i in range(n) if Xt[i][1] > Xt[i][0]]
    mu = {}
    for i in Jp:
        al, al2 = Xt[i]
        if x[i] == al and z[i] >= 0:
            mu[i] = z[i] / (al2 - al)
        elif x[i] == al2 and z[i] <= 0:
            mu[i] = -z[i] / (al2 - al)
        elif al < x[i] < al2 and z[i] == 0:
            mu[i] = Fr(0)
        elif i in ints:
            mu[i] = -abs(z[i])
        else:
            return False, 'no case'
    N = [[H[i][j] + (2 * mu[i] if i == j else 0) for j in Jp] for i in Jp]
    return is_psd(N), 'psd' if is_psd(N) else 'not psd'


def growth_cert(H, b, x, lo, hi, ints):
    """Lemma growthcert(a): return rational g>0 or None."""
    n = len(b)
    z = grad(H, b, x)
    mu = []
    for i in range(n):
        if i not in ints and lo[i] < x[i] < hi[i]:
            if z[i] != 0:
                return None
            mu.append(Fr(0))
        elif x[i] == lo[i] and z[i] >= 0:
            mu.append(z[i] / (hi[i] - lo[i]))
        elif x[i] == hi[i] and z[i] <= 0:
            mu.append(-z[i] / (hi[i] - lo[i]))
        elif i in ints:
            mu.append(-abs(z[i]))
        else:
            return None
    M = [[H[i][j] + (2 * mu[i] if i == j else 0) for j in range(n)] for i in range(n)]
    lam = min(np.linalg.eigvalsh(np.array([[float(v) for v in r] for r in M])))
    if lam <= 1e-6:
        return None
    g = Fr(lam / 2 * 0.99).limit_denominator(10 ** 6)
    if g > lam / 2 * 0.995 or g <= 0:
        g = Fr(int(lam / 2 * 0.98 * 10 ** 6), 10 ** 6)
    Mg = [[M[i][j] - (2 * g if i == j else 0) for j in range(n)] for i in range(n)]
    if not is_psd(Mg):
        return None
    return g


def rnd(rng, a, b, dens=(1, 2)):
    return Fr(rng.randint(a, b), rng.choice(dens))


def random_instance(rng, n):
    H = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        H[i][i] = rnd(rng, -3, 8)
        for j in range(i + 1, n):
            H[i][j] = H[j][i] = rnd(rng, -3, 3)
    b = [rnd(rng, -6, 6) for _ in range(n)]
    c = Fr(0)
    ints = set(i for i in range(n) if rng.random() < 0.4)
    lo, hi = [], []
    for i in range(n):
        if i in ints:
            l = rng.randint(-2, 0)
            lo.append(Fr(l)); hi.append(Fr(l + rng.randint(1, 4)))
        else:
            l = rnd(rng, -2, 0)
            lo.append(l); hi.append(l + rnd(rng, 1, 4))
    return H, b, c, lo, hi, ints


def planted_instance(rng, n):
    """x* chosen first; b = zeta - H x*, zeta inward at bounds, 0 inside."""
    ints = set(i for i in range(n) if rng.random() < 0.45)
    lo, hi, xs, H = [], [], [], [[Fr(0)] * n for _ in range(n)]
    kinds = []
    for i in range(n):
        if i in ints:
            l = rng.randint(-3, 0)
            u = l + rng.randint(1, 7)
            lo.append(Fr(l)); hi.append(Fr(u))
            k = rng.choice(['lo', 'hi', 'in'])
            xs.append(Fr(l) if k == 'lo' else Fr(u) if k == 'hi' else Fr(rng.randint(l, u)))
        else:
            l = rnd(rng, -3, 0, (1, 2, 3))
            u = l + rnd(rng, 1, 5, (1, 2, 3))
            lo.append(l); hi.append(u)
            k = rng.choice(['lo', 'hi', 'in', 'in'])
            xs.append(l if k == 'lo' else u if k == 'hi' else l + (u - l) * Fr(rng.randint(1, 9), 10))
        kinds.append(k)
    for i in range(n):
        if i not in ints and kinds[i] == 'in':
            H[i][i] = rnd(rng, 1, 8)
        else:
            H[i][i] = rnd(rng, -3, 6)
        for j in range(i + 1, n):
            H[i][j] = H[j][i] = rnd(rng, -3, 3, (1, 2, 4))
    zeta = []
    for i in range(n):
        lam = rnd(rng, 1, 12, (1, 2, 4, 8, 16))
        if i not in ints and kinds[i] == 'in':
            zeta.append(Fr(0))
        elif xs[i] == lo[i]:
            zeta.append(lam)
        elif xs[i] == hi[i]:
            zeta.append(-lam)
        else:
            zeta.append(rnd(rng, -2, 2, (1, 2, 4)))
    b = [zeta[i] - sum(H[i][j] * xs[j] for j in range(n)) for i in range(n)]
    return H, b, Fr(0), lo, hi, ints


def main():
    rng = Random(4242)
    stats = dict(inst=0, unique=0, cor_checked=0, stages=0, accepted=0, sound_checked=0,
                 A=0, J0=0, IZP=0, notP=0, early=0, abort=0)
    fails = []
    first_acc_vs_jstar = []
    ninst = int(sys.argv[1]) if len(sys.argv) > 1 else 80
    while stats['inst'] < ninst:
        n = rng.choice([2, 2, 3, 3])
        inst = random_instance(rng, n) if rng.random() < 0.4 else planted_instance(rng, n)
        H, b, c, lo, hi, ints = inst
        opt, pts = exact_minimum(H, b, c, [(lo[i], hi[i]) for i in range(n)], ints)
        stats['inst'] += 1
        unique = len(pts) == 1
        g = growth_cert(H, b, pts[0], lo, hi, ints) if unique else None
        Ls = [max(H[i][i], Fr(0)) for i in range(n)]
        L = max(Ls)
        if g is not None:
            stats['unique'] += 1
            xs = pts[0]
            kappa = max(Fr(1), L / g)
            mu_ = 2
            while 4 ** mu_ < 8 * kappa:
                mu_ += 1
            if mu_ > 4:
                g = None  # keep grids small
        if g is None:
            mu_ = 2
            kappa = None
        theta = Fr(1, 2 ** mu_)
        cap = 8 * 2 ** mu_ * math.ceil(math.log2(n + 2))
        P = [i for i in range(n) if Ls[i] > 0]
        hstar = None
        if g is not None:
            z = grad(H, b, xs)
            J0 = [i for i in range(n) if i not in ints and lo[i] < xs[i] < hi[i]]
            A = [i for i in P if i not in ints and xs[i] in (lo[i], hi[i])]
            if any(z[i] == 0 for i in A):
                g = None
            else:
                cand = []
                if any(i in ints and i in P for i in range(n)):
                    cand.append(0.5)
                dX = [abs(xs[i] - e) for i in range(n) if (i not in ints or i not in P)
                      for e in (lo[i], hi[i]) if e != xs[i]]
                if dX:
                    cand.append(float(min(dX)) / 6)
                if A:
                    lamA = min(abs(z[i]) for i in A)
                    HAA = np.array([[float(H[i][j]) for j in A] for i in A])
                    nAA = np.linalg.norm(HAA, 2) * 1.001 + 1e-9
                    nJA = (np.linalg.norm(np.array([[float(H[i][j]) for j in A] for i in J0]), 2) * 1.001 + 1e-9) if J0 else 0.0
                    Gam = nAA + nJA ** 2 / (2 * float(g))
                    cand.append(float(lamA) / (5 * Gam))
                hstar = min(cand) / math.sqrt(n * float(kappa)) * 0.999
                stats['A'] += bool(A); stats['J0'] += bool(J0)
                stats['IZP'] += any(i in ints and i in P for i in range(n))
                stats['notP'] += any(i not in P for i in range(n))
        s = max(hi[i] - lo[i] for i in range(n))
        jstar = None
        if hstar is not None:
            jstar = 0
            while float(s) / 2 ** jstar > hstar:
                jstar += 1
        stages = (jstar + 2) if jstar is not None else 9
        stages = min(stages, 14)
        first_acc = [None]

        def on_stage(j, h, grids, m, y, U, beta, box, newbox, Ls_, P_):
            stats['stages'] += 1
            Xt, x, info = narrowed_and_candidate(inst, grids, m, y, U, newbox, Ls_, P_)
            # S1
            if any(t is None or not (t[0] <= y[i] <= t[1]) for i, t in enumerate(Xt)):
                fails.append(('S1 y not in narrowed box', stats['inst'], j))
                return
            # S3: optimal points lie in narrowed box after Lemma node(b) moves (unique case)
            if unique and any(not (Xt[i][0] <= pts[0][i] <= Xt[i][1]) for i in range(n)):
                fails.append(('S3 x* not in narrowed box', stats['inst'], j))
            passed = False
            if x is not None:
                passed, why = local_test(inst, Xt, x, U)
                if passed:
                    stats['accepted'] += 1
                    stats['sound_checked'] += 1
                    if val(H, b, c, x) != opt:
                        fails.append(('S2 UNSOUND', stats['inst'], j, x))
                    if first_acc[0] is None:
                        first_acc[0] = j
            if hstar is not None and float(h) <= hstar:
                stats['cor_checked'] += 1
                ok = True
                for i in range(n):
                    if (i in ints or i not in P) and Xt[i] != (xs[i], xs[i]):
                        ok = False; fails.append(('C1 narrowed', stats['inst'], j, i, Xt[i], xs[i]))
                Jp, free = info if info else (None, None)
                if Jp is not None and set(Jp) != set(J0) | set(A):
                    ok = False; fails.append(('C1 J+', stats['inst'], j, Jp, J0, A))
                if free is not None and set(free) != set(J0):
                    ok = False; fails.append(('C1 J', stats['inst'], j, free, J0))
                if x is None or list(x) != list(xs):
                    ok = False; fails.append(('C1 candidate', stats['inst'], j, x, xs))
                elif not passed:
                    ok = False; fails.append(('C1 test', stats['inst'], j))

        status, jend = run_trial(inst, theta, cap, stages, on_stage)
        if status == 'abort':
            stats['abort'] += 1
            if g is not None:
                fails.append(('abort with 8 kappa theta^2<=1', stats['inst']))
        if jstar is not None and first_acc[0] is not None:
            first_acc_vs_jstar.append((first_acc[0], jstar))
            if first_acc[0] < jstar:
                stats['early'] += 1
        if jstar is not None and first_acc[0] is None and status != 'success':
            fails.append(('C2 never accepted by j*+2', stats['inst'], jstar, status, jend))
    print(stats)
    print('first acceptance vs j*: max j* =', max((b for _, b in first_acc_vs_jstar), default=None),
          ' max first acc =', max((a for a, _ in first_acc_vs_jstar), default=None))
    print('FAILURES:', len(fails))
    for f in fails[:15]:
        print(f)
    print('ALL PASS' if not fails else 'SOME FAIL')


if __name__ == '__main__':
    main()
