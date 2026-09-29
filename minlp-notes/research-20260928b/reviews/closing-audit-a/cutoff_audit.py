"""Closing audit A, item 1: cutoff-propagation.md, Section 11.2 changes.
Independent code; exact rationals.  Every propagation step below is a run step in
the note's sense (rho_E(Z) ⊆ rho(Z) ⊆ Z): forward/backward steps of HC4 whose
new bounds are rounded OUTWARD to the grid 2^-GRID and then intersected with the
current interval.  So every "long HC4" result is an outer approximation of Z*.

(E) Lemma 2.1(b): random branch-and-bound runs on random 2D DAGs (lin, abs, sqr,
    constants, shared subexpressions), several phases per node, 1-3 runs per phase,
    random schedules, cutoffs moving up and down, start boxes = Z0(x-box) ∩ random
    subsets of final lifted boxes of earlier runs at the node and its ancestors.
    Claim tested: for each frame piece S of a phase from B0 to Bf,
    Pi_x Z*(S, c_chain) ⊆ Bf, and Z*(B0, c_chain) = ∅ for emptying phases.
    Control: the phase-only minimum cutoff.
(W) Remark 4.1a on random 1D piecewise-linear DAGs with shared subexpressions:
    the exact-range witness box is hull-consistent (fixed by every exact
    forward/backward step and the cutoff), lies in Z0(C), and HC4 from Z0(C) at
    c = Phi_full(U') keeps U'.  Also Lemma 1.2(d) on the witness boxes and on exactly
    converged HC4 limits, and the constant-node counterexample.
(J) the joint-propagation counterexample of Section 2.
(R) round counts for (s-1)^2 and x^2 - 2x + 1 + r^4, r = x - 1 (Heuristic 3.8a evidence).
Run: python3 cutoff_audit.py [E W J R] > cutoff_audit.log
"""
import math
import random
import sys
from fractions import Fraction as Fr

GRID = 40


def rdown(x, g=None):
    g = GRID if g is None else g
    return Fr(math.floor(x * 2 ** g), 2 ** g)


def rup(x, g=None):
    g = GRID if g is None else g
    return Fr(math.ceil(x * 2 ** g), 2 ** g)


def sqrt_down(q, g=None):
    g = GRID if g is None else g
    if q <= 0:
        return Fr(0)
    return Fr(math.isqrt(math.floor(q * 2 ** (2 * g))), 2 ** g)


def sqrt_up(q, g=None):
    g = GRID if g is None else g
    if q <= 0:
        return Fr(0)
    X = math.ceil(q * 2 ** (2 * g))
    s = math.isqrt(X)
    if s * s < X:
        s += 1
    return Fr(s, 2 ** g)


def inter(A, B):
    if A is None or B is None:
        return None
    lo, hi = max(A[0], B[0]), min(A[1], B[1])
    return (lo, hi) if lo <= hi else None


def hull2(A, B):
    if A is None:
        return B
    if B is None:
        return A
    return (min(A[0], B[0]), max(A[1], B[1]))


def scale(a, I):
    return (a * I[0], a * I[1]) if a >= 0 else (a * I[1], a * I[0])


def add(I, J):
    return (I[0] + J[0], I[1] + J[1])


def sqr_img(I):
    lo, hi = I
    if lo >= 0:
        return (lo * lo, hi * hi)
    if hi <= 0:
        return (hi * hi, lo * lo)
    return (Fr(0), max(lo * lo, hi * hi))


def abs_img(I):
    lo, hi = I
    if lo >= 0:
        return (lo, hi)
    if hi <= 0:
        return (-hi, -lo)
    return (Fr(0), max(-lo, hi))


# DAG: list of nodes; ('var', i) | ('const', q) | ('lin', [children], [coefs]) | ('abs', ch) | ('sqr', ch)
def image(dag, k, Z):
    nd = dag[k]
    if nd[0] == 'lin':
        acc = (Fr(0), Fr(0))
        for ch, a in zip(nd[1], nd[2]):
            acc = add(acc, scale(a, Z[ch]))
        return acc
    if nd[0] == 'abs':
        return abs_img(Z[nd[1]])
    if nd[0] == 'sqr':
        return sqr_img(Z[nd[1]])
    raise ValueError


def Z0(dag, box):
    Z = []
    for k, nd in enumerate(dag):
        if nd[0] == 'var':
            Z.append(box[nd[1]])
        elif nd[0] == 'const':
            Z.append((nd[1], nd[1]))
        else:
            Z.append(image(dag, k, Z))
    return Z


def fwd(dag, k, Z, rnd):
    """forward step of node k (in place); returns False if empty."""
    img = image(dag, k, Z)
    if rnd:
        img = (rdown(img[0]), rup(img[1]))
    new = inter(Z[k], img)
    if new is None:
        return False
    Z[k] = new
    return True


def bwd(dag, k, Z, rnd):
    nd = dag[k]
    W = Z[k]
    if nd[0] == 'lin':
        chs, cs = nd[1], nd[2]
        for i, (ch, a) in enumerate(zip(chs, cs)):
            if dag[ch][0] == 'const':
                continue
            rest = (Fr(0), Fr(0))
            for j, (ch2, a2) in enumerate(zip(chs, cs)):
                if j != i:
                    rest = add(rest, scale(a2, Z[ch2]))
            cand = scale(1 / a, (W[0] - rest[1], W[1] - rest[0]))
            if rnd:
                cand = (rdown(cand[0]), rup(cand[1]))
            new = inter(Z[ch], cand)
            if new is None:
                return False
            Z[ch] = new
        return True
    ch = nd[1]
    Wp = inter(W, (Fr(0), max(W[1], Fr(0))))
    if Wp is None:
        return False
    if nd[0] == 'abs':
        rl, rh = Wp
    else:
        if rnd:
            rl, rh = sqrt_down(Wp[0]), sqrt_up(Wp[1])
        else:
            raise ValueError('exact sqrt not supported; exact mode is used only for PL DAGs')
    new = hull2(inter(Z[ch], (-rh, -rl)), inter(Z[ch], (rl, rh)))
    if new is None:
        return False
    Z[ch] = new
    return True


def cut(dag, Z, c):
    lo, hi = Z[-1]
    if lo > c:
        return False
    Z[-1] = (lo, min(hi, c))
    return True


def hc4_round(dag, Z, c, rnd=True):
    ops = [k for k, nd in enumerate(dag) if nd[0] not in ('var', 'const')]
    for k in ops:
        if not fwd(dag, k, Z, rnd):
            return False
    if not cut(dag, Z, c):
        return False
    for k in reversed(ops):
        if not bwd(dag, k, Z, rnd):
            return False
    return True


def hc4(dag, Z, c, rounds, rnd=True):
    """returns (Z or None, converged flag, rounds used)"""
    Z = list(Z)
    for r in range(rounds):
        old = list(Z)
        if not hc4_round(dag, Z, c, rnd):
            return None, True, r + 1
        if Z == old:
            return Z, True, r + 1
    return Z, False, rounds


def random_steps(dag, Z, c, nsteps, rng):
    ops = [k for k, nd in enumerate(dag) if nd[0] not in ('var', 'const')]
    Z = list(Z)
    for _ in range(nsteps):
        u = rng.random()
        if u < 0.15:
            ok = cut(dag, Z, c)
        elif u < 0.55:
            ok = fwd(dag, rng.choice(ops), Z, True)
        else:
            ok = bwd(dag, rng.choice(ops), Z, True)
        if not ok:
            return None
    # finish with one full round so the cutoff is certainly used
    return Z if hc4_round(dag, Z, c) else None


def proj(dag, Z):
    return [Z[k] for k, nd in enumerate(dag) if nd[0] == 'var']


# ---------------------------------------------------------------- random DAGs
COEFS = [Fr(-3), Fr(-2), Fr(-1), Fr(1), Fr(2), Fr(3), Fr(1, 2), Fr(-1, 2)]


def random_dag(rng, nvar=2, nops=7, ops=('lin', 'abs', 'sqr')):
    dag = [('var', i) for i in range(nvar)]
    for q in rng.sample([Fr(-1), Fr(1, 2), Fr(2), Fr(-1, 3)], 2):
        dag.append(('const', q))
    for _ in range(nops):
        t = rng.choice(ops)
        if t == 'lin':
            k = rng.randint(2, 3)
            chs = rng.sample(range(len(dag)), min(k, len(dag)))
            dag.append(('lin', chs, [rng.choice(COEFS) for _ in chs]))
        else:
            ch = rng.choice([i for i in range(len(dag)) if dag[i][0] != 'const'])
            dag.append((t, ch))
    cand = [i for i in range(len(dag)) if dag[i][0] != 'const']
    terms = rng.sample(cand, min(len(cand), rng.randint(3, 5)))
    dag.append(('lin', terms, [rng.choice(COEFS) for _ in terms]))
    return dag


def evaluate(dag, x):
    v = []
    for nd in dag:
        if nd[0] == 'var':
            v.append(x[nd[1]])
        elif nd[0] == 'const':
            v.append(nd[1])
        elif nd[0] == 'lin':
            v.append(sum(a * v[ch] for ch, a in zip(nd[1], nd[2])))
        elif nd[0] == 'abs':
            v.append(abs(v[nd[1]]))
        else:
            v.append(v[nd[1]] ** 2)
    return v


def frame(B0, Bf):
    n = len(B0)
    pieces = []
    for i in range(n):
        for side in (0, 1):
            S = []
            for j in range(n):
                if j < i:
                    S.append(Bf[j])
                elif j > i:
                    S.append(B0[j])
                else:
                    S.append((B0[i][0], Bf[i][0]) if side == 0 else (Bf[i][1], B0[i][1]))
            if all(lo < hi for lo, hi in S):
                pieces.append(S)
    return pieces


def excess(Pbox, B):
    return max(max(B[i][0] - Pbox[i][0], Pbox[i][1] - B[i][1], Fr(0)) for i in range(len(B)))


# ---------------------------------------------------------------- (E)
class Stats:
    def __init__(self):
        self.pieces = 0
        self.empties = 0
        self.res = {'chain': [0, 0, 0, 0], 'own': [0, 0, 0, 0]}  # violations, inconclusive, certified-empty, certified-contained
        self.max_ok_excess = Fr(0)
        # direct test of Pi_x D ⊆ Bf, D = Z*(B0, c): [phases, D empty, D nonempty and inside Bf, outside, inconclusive]
        self.D = {'chain': [0, 0, 0, 0, 0], 'own': [0, 0, 0, 0, 0]}


def check_cert(dag, S_box, c, Bf, st, tag, long_rounds, tol):
    Zs, conv, _ = hc4(dag, Z0(dag, S_box), c, long_rounds)
    if Zs is None:
        st.res[tag][2] += 1
        return
    ex = excess(proj(dag, Zs), Bf) if Bf is not None else Fr(1)
    if ex <= tol:
        st.res[tag][3] += 1
        st.max_ok_excess = max(st.max_ok_excess, ex) if tag == 'chain' else st.max_ok_excess
    elif conv:
        st.res[tag][0] += 1
    else:
        st.res[tag][1] += 1


CUT_LO, CUT_HI = Fr(-1, 10), Fr(2, 5)


def part_E(rng, ninst=400, long_rounds=400, tol=Fr(1, 10 ** 6)):
    print('== (E) Lemma 2.1(b) with the chain-minimum cutoff', flush=True)
    st = Stats()
    for inst in range(ninst):
        dag = random_dag(rng)
        X0 = [(Fr(-1), Fr(1)), (Fr(-1), Fr(1))]
        vals = [evaluate(dag, (Fr(i, 8), Fr(j, 8)))[-1] for i in range(-8, 9) for j in range(-8, 9)]
        fmin, fmax = min(vals), max(vals)
        span = fmax - fmin if fmax > fmin else Fr(1)
        phases = {}  # id -> c_chain
        counter = [0]

        def new_cut(prev):
            # cutoffs in the band [fmin + LO*span, fmin + HI*span], random walk up and down
            if prev is None:
                return fmin + span * Fr(rng.randint(int(100 * CUT_LO), int(100 * CUT_HI)), 100)
            step = span * Fr(rng.randint(-15, 15), 100)
            return max(fmin + CUT_LO * span, min(fmin + CUT_HI * span, prev + step))

        def process(box, avail, depth, cprev):
            nph = rng.randint(1, 2)
            for ph in range(nph):
                if ph > 0 and rng.random() < 0.4:  # another reduction (R-rel/R-inf) shrinks the box
                    i = rng.randrange(2)
                    lo, hi = box[i]
                    w = hi - lo
                    box = list(box)
                    box[i] = (lo + w * Fr(rng.randint(0, 20), 100), hi - w * Fr(rng.randint(0, 20), 100))
                counter[0] += 1
                pid = counter[0]
                B0 = list(box)
                cuts, entering = [], set()
                cur = list(box)
                emptied = False
                for r in range(rng.randint(1, 3)):
                    c = new_cut(cprev)
                    cprev = c
                    cuts.append(c)
                    Z = Z0(dag, cur)
                    for (qid, Y) in avail:
                        if rng.random() < 0.6:
                            if qid != pid:
                                entering.add(qid)
                            Z = [inter(a, b) for a, b in zip(Z, Y)]
                    if any(I is None for I in Z):
                        emptied = True
                        break
                    if rng.random() < 0.5:
                        Zf, _, _ = hc4(dag, Z, c, rng.randint(1, 3))
                    else:
                        Zf = random_steps(dag, Z, c, rng.randint(5, 40), rng)
                    if Zf is None:
                        emptied = True
                        break
                    avail = avail + [(pid, Zf)]
                    cur = proj(dag, Zf)
                c_own = min(cuts)
                c_chain = min([c_own] + [phases[q] for q in entering])
                phases[pid] = c_chain
                if emptied:
                    st.empties += 1
                    for tag, cc in (('chain', c_chain), ('own', c_own)):
                        check_cert(dag, B0, cc, None, st, tag, long_rounds, tol)
                    return
                Bf = cur
                for tag, cc in (('chain', c_chain), ('own', c_own)):
                    ZD, conv, _ = hc4(dag, Z0(dag, B0), cc, long_rounds)
                    st.D[tag][0] += 1
                    if ZD is None:
                        st.D[tag][1] += 1
                    elif excess(proj(dag, ZD), Bf) <= tol:
                        st.D[tag][2] += 1
                    elif conv:
                        st.D[tag][3] += 1
                    else:
                        st.D[tag][4] += 1
                for S in frame(B0, Bf):
                    st.pieces += 1
                    for tag, cc in (('chain', c_chain), ('own', c_own)):
                        check_cert(dag, S, cc, Bf, st, tag, long_rounds, tol)
                box = Bf
            if depth < 4:
                i = rng.randrange(2)
                lo, hi = box[i]
                if hi - lo > Fr(1, 2 ** 20):
                    s = lo + (hi - lo) * Fr(rng.randint(25, 75), 100)
                    s = rdown(s, 30) if lo < rdown(s, 30) < hi else s
                    for half in ((lo, s), (s, hi)):
                        b = list(box)
                        b[i] = half
                        process(b, list(avail), depth + 1, cprev)

        process(X0, [], 0, None)
        if (inst + 1) % 50 == 0:
            print(f'  after {inst + 1} instances: pieces {st.pieces}, emptying phases {st.empties}; '
                  f'chain [viol, inconcl, cert-empty, cert-contained] {st.res["chain"]}; own {st.res["own"]}', flush=True)
    print(f'  TOTAL: frame pieces {st.pieces}, emptying phases {st.empties}; '
          f'chain-minimum [violations, inconclusive, certified empty, certified nonempty-contained] = {st.res["chain"]}; '
          f'phase-only control = {st.res["own"]}; largest accepted excess {float(st.max_ok_excess):.2e}')
    print(f'  direct test Pi_x Z*(B0, c) ⊆ Bf over non-emptying phases [phases, D empty, D nonempty inside Bf, '
          f'outside Bf (converged), inconclusive]: chain {st.D["chain"]}; phase-only control {st.D["own"]}')


# ---------------------------------------------------------------- (W) PL witness, 1D
class PL:
    """continuous piecewise-linear function on [L, U] given by sorted breakpoints."""

    def __init__(self, pts):
        self.pts = pts  # list of (t, v)

    def at(self, t):
        P = self.pts
        for (t0, v0), (t1, v1) in zip(P, P[1:]):
            if t0 <= t <= t1:
                return v0 if t1 == t0 else v0 + (v1 - v0) * (t - t0) / (t1 - t0)
        raise ValueError

    def rng(self, s, t):
        vals = [self.at(s), self.at(t)] + [v for (x, v) in self.pts if s < x < t]
        return (min(vals), max(vals))


def pl_nodes(dag, L, U):
    fs = []
    for nd in dag:
        if nd[0] == 'var':
            fs.append(PL([(L, L), (U, U)]))
        elif nd[0] == 'const':
            fs.append(PL([(L, nd[1]), (U, nd[1])]))
        elif nd[0] == 'lin':
            ts = sorted({t for ch in nd[1] for t, _ in fs[ch].pts})
            fs.append(PL([(t, sum(a * fs[ch].at(t) for ch, a in zip(nd[1], nd[2]))) for t in ts]))
        elif nd[0] == 'abs':
            P = fs[nd[1]].pts
            out = []
            for (t0, v0), (t1, v1) in zip(P, P[1:]):
                out.append((t0, abs(v0)))
                if v0 * v1 < 0:
                    tz = t0 + (t1 - t0) * (-v0) / (v1 - v0)
                    out.append((tz, Fr(0)))
            out.append((P[-1][0], abs(P[-1][1])))
            fs.append(PL(out))
        else:
            raise ValueError
    return fs


def part_W(rng, ninst=300):
    print('== (W) Remark 4.1a (general DAG below a flat root sum), exact PL witness, 1D', flush=True)
    hc_bad = step_bad = z0_bad = keep_bad = d_bad = 0
    shared = 0
    tested = 0
    conv_lim = 0
    for inst in range(ninst):
        dag = random_dag(rng, nvar=1, nops=rng.randint(4, 9), ops=('lin', 'lin', 'abs'))
        # count shared (multiply used) non-root nodes
        uses = {}
        for nd in dag:
            if nd[0] == 'lin':
                for ch in nd[1]:
                    uses[ch] = uses.get(ch, 0) + 1
            elif nd[0] in ('abs',):
                uses[nd[1]] = uses.get(nd[1], 0) + 1
        shared += any(v > 1 for k, v in uses.items() if dag[k][0] not in ('var', 'const'))
        L, U = Fr(-rng.randint(1, 4), rng.randint(1, 3)), Fr(rng.randint(1, 4), rng.randint(1, 3))
        C = [(L, U)]
        fs = pl_nodes(dag, L, U)
        root = dag[-1]
        for _ in range(4):
            a = L + (U - L) * Fr(rng.randint(0, 90), 100)
            b = a + (U - a) * Fr(rng.randint(5, 100), 100)
            tested += 1
            # exact ranges; Phi_full from the root's term nodes
            rngs = [fs[k].rng(a, b) for k in range(len(dag))]
            tr = [scale(cf, rngs[ch]) for ch, cf in zip(root[1], root[2])]
            c = sum(t[0] for t in tr) + max(t[1] - t[0] for t in tr)
            W = [rngs[k] for k in range(len(dag) - 1)]
            W.append((sum(t[0] for t in tr), min(c, sum(t[1] for t in tr))))
            # hull consistency: every exact forward/backward step and the cutoff leave W unchanged
            ok = True
            for k, nd in enumerate(dag):
                if nd[0] in ('var', 'const'):
                    continue
                Z = list(W)
                if not fwd(dag, k, Z, False) or Z != W:
                    ok = False
                Z = list(W)
                if not bwd(dag, k, Z, False) or Z != W:
                    ok = False
            Z = list(W)
            if not cut(dag, Z, c) or Z != W:
                ok = False
            step_bad += not ok
            Z0C = Z0(dag, C)
            z0_bad += not all(z[0] <= w[0] and w[1] <= z[1] for z, w in zip(Z0C, W))
            # Lemma 1.2(d) on the witness: W ⊆ Z0(Pi_x W)
            Zp = Z0(dag, [W[0]])
            d_bad += not all(z[0] <= w[0] and w[1] <= z[1] for z, w in zip(Zp, W))
            # HC4 from Z0(C) at c keeps U' = [a, b]
            Zf, conv, _ = hc4(dag, Z0C, c, 300, rnd=False)
            if Zf is None or not (Zf[0][0] <= a and b <= Zf[0][1]):
                keep_bad += 1
            elif conv:
                conv_lim += 1
                Zp = Z0(dag, [Zf[0]])
                d_bad += not all(z[0] <= w[0] and w[1] <= z[1] for z, w in zip(Zp, Zf))
    print(f'  {ninst} DAGs ({shared} with a shared operation node), {tested} boxes U\': '
          f'witness not fixed by some step: {step_bad}; witness not in Z0(C): {z0_bad}; '
          f'HC4 at c = Phi_full(U\') removed part of U\': {keep_bad}; Lemma 1.2(d) failures on witnesses and '
          f'{conv_lim} exactly converged HC4 limits: {d_bad}')
    # constant-node remark: a widened constant breaks Z ⊆ Z0(Pi_x Z)
    dag = [('var', 0), ('const', Fr(0)), ('lin', [0, 1], [Fr(1), Fr(1)])]
    Z = [(Fr(0), Fr(0)), (Fr(0), Fr(1)), (Fr(0), Fr(1))]
    Y1, Y2 = list(Z), list(Z)
    fixed = fwd(dag, 2, Y1, False) and Y1 == Z and bwd(dag, 2, Y2, False) and Y2 == Z
    print(f'  constant widened to [0,1] under w = x + k, x = [0,0]: box fixed by both steps: {fixed}; '
          f'Z0(Pi_x Z) = {Z0(dag, [(Fr(0), Fr(0))])} does not contain Z = {Z}')


# ---------------------------------------------------------------- (J)
def part_J():
    print('== (J) joint propagation counterexample: -3x^2 + 2x^2 + 2x^2 on [-1,1], x >= 1/2', flush=True)
    dag = [('var', 0), ('sqr', 0), ('sqr', 0), ('sqr', 0), ('lin', [1, 2, 3], [Fr(-3), Fr(2), Fr(2)])]
    c = Fr(1, 4) - Fr(1, 1000)
    Zf, conv, r = hc4(dag, Z0(dag, [(Fr(1, 2), Fr(1))]), c, 2000)
    print(f'  HC4 on x in [1/2,1] (after the constraint) at c = f* - 1e-3: empty = {Zf is None} after {r} rounds')
    # witness at c = -1 on [-1, 1] (Theorem 3.1(b) box), checked by exact steps (sqrt of 0 and 1)
    W = [(Fr(-1), Fr(1)), (Fr(1), Fr(1)), (Fr(0), Fr(1)), (Fr(0), Fr(1)), (Fr(-3), Fr(-1))]
    ok = True
    for k in (1, 2, 3, 4):
        Y = list(W)
        ok &= fwd(dag, k, Y, True) and Y == W
        Y = list(W)
        ok &= bwd(dag, k, Y, True) and Y == W
    Y = list(W)
    ok &= cut(dag, Y, Fr(-1)) and Y == W
    print(f'  witness box with x = [-1,1] hull-consistent at c = -1 (so pi_D([-1,1], y) <= -1 for all y): {ok}')
    Zf, conv, r = hc4(dag, Z0(dag, [(Fr(-1), Fr(1))]), Fr(-1) - Fr(1, 1000), 2000)
    print(f'  HC4 on [-1,1] at c = -1.001: empty = {Zf is None} (so pi_D([-1,1]) = -1)')


# ---------------------------------------------------------------- (R)
def rounds_to_empty(dag, box, c, maxr=10 ** 6):
    global GRID
    Z = Z0(dag, box)
    for r in range(1, maxr):
        if not hc4_round(dag, Z, c):
            return r
    return None


def part_R():
    global GRID
    GRID = 70
    print('== (R) root rounds for (s-1)^2 = s^2 - 2s + 1 and x^2 - 2x + 1 + r^4 (r = x - 1) on [1/5, 11/5]', flush=True)
    q = [('var', 0), ('const', Fr(1)), ('sqr', 0), ('lin', [2, 0, 1], [Fr(1), Fr(-2), Fr(1)])]
    r4 = [('var', 0), ('const', Fr(1)), ('lin', [0, 1], [Fr(1), Fr(-1)]), ('sqr', 0), ('sqr', 2), ('sqr', 4),
          ('lin', [3, 0, 1, 5], [Fr(1), Fr(-2), Fr(1), Fr(1)])]
    for e in (2, 3, 4, 5, 6):
        eps = Fr(1, 10 ** e)
        a = rounds_to_empty(q, [(Fr(1, 5), Fr(11, 5))], -eps)
        b = rounds_to_empty(r4, [(Fr(1, 5), Fr(11, 5))], -eps)
        print(f'  eps=1e-{e}: (s-1)^2 {a} rounds ({a * math.sqrt(float(eps)):.3f}); with r^4: {b}', flush=True)
    GRID = 40


def main(parts):
    rng = random.Random(29092026)
    if 'J' in parts:
        part_J()
    if 'W' in parts:
        part_W(rng)
    if 'R' in parts:
        part_R()
    global CUT_LO, CUT_HI
    if 'E' in parts:
        part_E(rng)
    if 'E2' in parts:
        CUT_LO, CUT_HI = Fr(1, 5), Fr(7, 10)
        print('   (band for E2: cutoffs in [fmin + 0.2 span, fmin + 0.7 span])')
        part_E(rng)


if __name__ == '__main__':
    main(sys.argv[1:] or ['J', 'W', 'R', 'E'])
