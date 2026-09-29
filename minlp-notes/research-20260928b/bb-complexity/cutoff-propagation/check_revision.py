"""Checks for the revision after review (Section 11 of the note).

(A) Endpoint example x^2 = -3x^2 + 2x^2 + 2x^2 (three power nodes) on [-1,1]:
    pi_D by bisection against the endpoint formula of Theorem 3.1 and the
    rejected full-range formula; and a restart: the forward box of the
    contracted x-box is larger than the lifted box at the end of the run.
(B) Lemma 2.1(b) as revised: a propagation phase made of several runs, each
    restarted from the forward box of the current x-box (or from inherited
    lifted bounds).  For every frame piece S of B0 \\ int Bf, the fixed point
    Z*(S, c) must project into Bf.  Also: a child started from the parent's
    final lifted box ends with a box containing Pi_x Z*(child, c).
(C) h_{1/2} (expanded) on intervals inside s < 0: pi_D(C) = min_C h.
(D) Two-sided localization (Proposition 5.1a) on expanded linediag: whenever
    y is removed from C, both faces of C are within 4(m(y)+eps)/D'_0 in every
    coordinate, D'_0 = min_i (D_i(y) - |d_i f(y)|).
Run: python3 check_revision.py > logs/check_revision.log
"""
import math
import numpy as np
from fbbt import Builder, hc4, init_intervals, evaluate
from check_loss import pi_bisect, term_grads
import instances as I

rng = np.random.default_rng(11)


def part_a():
    b = Builder(1)
    p = [b.pow(0, 2) for _ in range(3)]
    b.lin(p, [-3.0, 2.0, 2.0], 0.0)
    dag = b.dag()
    coef = [-3.0, 2.0, 2.0]
    G = 801
    xs = np.linspace(-1, 1, G)
    best_end, best_full = np.inf, np.inf
    for i in range(G):
        for j in range(i, G, 4):
            seg = xs[i:j + 1]
            m = [min(a * seg ** 2) for a in coef]
            e = [max(a * xs[i] ** 2, a * xs[j] ** 2) for a in coef]
            M = [max(a * seg ** 2) for a in coef]
            best_end = min(best_end, sum(m) + max(ei - mi for ei, mi in zip(e, m)))
            best_full = min(best_full, sum(m) + max(Mi - mi for Mi, mi in zip(M, m)))
    print('(A) -3x^2 + 2x^2 + 2x^2 on [-1,1]:')
    print(f'    min Phi (endpoint formula) = {best_end:+.4f}; min Phi (full-range formula) = {best_full:+.4f}')
    for box in ([(-1.0, 1.0)], [(-0.1, 0.1)], [(-0.1, 0.3)]):
        print(f'    pi_D({box[0]}) by bisection = {pi_bisect(dag, box, 0.0):+.5f}')
    st, vb, r, iv = hc4(dag, [(-1.0, 1.0)], -0.01, lifted=True)
    z0 = init_intervals(dag, vb)
    print(f'    run at c=-0.01: status={st}, x-box={vb[0]}, first square node {iv[1]} '
          f'but forward box of the x-box gives {z0[1]} (restart is not a step rho(Z) ⊆ Z)')


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
            if all(hi - lo > 1e-12 for lo, hi in S):
                pieces.append(S)
    return pieces


def inside(A, B, tol=1e-10):
    return all(a[0] >= b[0] - tol and a[1] <= b[1] + tol for a, b in zip(A, B))


def part_b():
    cases = [('linediag', 'exp'), ('linediag', 's'), ('iso2', 'exp'), ('rot0.1', 'exp'),
             ('h1', 'exp'), ('nondeg1s', 'exp')]
    pieces_tested = viol = child_tests = child_viol = 0
    for name, rep in cases:
        inst = I.make(name)
        dag = inst['reps'][rep]
        n = len(inst['box'])
        for _ in range(60):
            if inst['xstar'] is not None:
                c0 = inst['xstar']
            else:  # linediag: a random point of the optimal line
                t = rng.uniform(0.2, 1.0); c0 = [t + 1, t]
            B0 = [(max(lo, ci - rng.uniform(0.01, 0.4)), min(hi, ci + rng.uniform(0.01, 0.4)))
                  for (lo, hi), ci in zip(inst['box'], c0)]
            c = -1e-3 if rng.random() < 0.5 else rng.uniform(-1e-3, 0.3)
            # phase: run 1 from Z0(B0), then restart from Z0 of the contracted box
            st, B1, _ = hc4(dag, B0, c, max_rounds=int(rng.integers(1, 4)))
            if st == 'empty':
                continue
            st, Bf, _, ivf = hc4(dag, B1, c, max_rounds=int(rng.integers(1, 4)), lifted=True)
            if st == 'empty':
                continue
            for S in frame(B0, Bf):
                pieces_tested += 1
                st2, vS, _ = hc4(dag, S, c, max_rounds=200000)
                if st2 != 'empty' and not inside(vS, Bf):
                    viol += 1
            # child started from the parent's final lifted box
            i = int(np.argmax([hi - lo for lo, hi in Bf]))
            mid = 0.5 * (Bf[i][0] + Bf[i][1])
            child = list(Bf); child[i] = (Bf[i][0], mid)
            st3, vc, _ = hc4(dag, child, c, max_rounds=int(rng.integers(1, 4)), start=ivf)
            st4, vstar, _ = hc4(dag, child, c, max_rounds=200000)
            child_tests += 1
            if st4 != 'empty' and (st3 == 'empty' or not inside(vstar, vc)):
                child_viol += 1
    print(f'(B) merged phases with restarts: {pieces_tested} frame pieces, {viol} with '
          f'Pi_x Z*(S,c) not inside Bf; {child_tests} children started from inherited '
          f'lifted bounds, {child_viol} losing part of Pi_x Z*(child,c)')


def part_e():
    """Gap B (recheck): cutoffs that move up and down.  A parent phase with
    cutoff c_p; a child phase of 1-3 runs with its own cutoffs, the first run
    started from the parent's final lifted box, later runs restarted from
    Z0(B_i) intersected with the previous lifted box.  Frame pieces of the
    child's phase are certified with the chain minimum c = min(c_p, child
    cutoffs); control: the child's own minimum only."""
    cases = [('linediag', 'exp'), ('linediag', 's'), ('iso2', 'exp'), ('rot0.1', 'exp'),
             ('rot0.1', 'st'), ('h1', 'exp'), ('nondeg1s', 'exp'), ('nd2', 'mono')]
    pieces = viol_chain = viol_own = 0
    for name, rep in cases:
        inst = I.make(name)
        dag = inst['reps'][rep]
        for _ in range(80):
            c0 = inst['xstar'] if inst['xstar'] is not None else [rng.uniform(1.2, 2.0)] * 1
            if inst['xstar'] is None:
                t = rng.uniform(0.2, 1.0); c0 = [t + 1, t]
            Bp = [(max(lo, ci - rng.uniform(0.05, 0.5)), min(hi, ci + rng.uniform(0.05, 0.5)))
                  for (lo, hi), ci in zip(inst['box'], c0)]
            cp = rng.uniform(-1e-3, 0.3)
            st, Bpf, _, Yp = hc4(dag, Bp, cp, max_rounds=int(rng.integers(1, 5)), lifted=True)
            if st == 'empty':
                continue
            i = int(np.argmax([hi - lo for lo, hi in Bpf]))
            mid = 0.5 * (Bpf[i][0] + Bpf[i][1])
            B0 = list(Bpf)
            B0[i] = (Bpf[i][0], mid) if rng.random() < 0.5 else (mid, Bpf[i][1])
            cuts = [rng.uniform(-1e-3, 0.3) for _ in range(int(rng.integers(1, 4)))]
            start, B, empty = Yp, B0, False
            for c in cuts:
                st, B, _, L = hc4(dag, B, c, max_rounds=int(rng.integers(1, 4)), start=start, lifted=True)
                if st == 'empty':
                    empty = True; break
                start = L
            if empty:
                continue
            c_chain, c_own = min([cp] + cuts), min(cuts)
            for S in frame(B0, B):
                pieces += 1
                for cc, tag in ((c_chain, 'chain'), (c_own, 'own')):
                    st2, vS, _ = hc4(dag, S, cc, max_rounds=200000)
                    if st2 != 'empty' and not inside(vS, B):
                        if tag == 'chain':
                            viol_chain += 1
                        else:
                            viol_own += 1
    print(f'(E) cutoffs moving up and down, inherited starts: {pieces} frame pieces; not certified '
          f'with the chain-minimum cutoff: {viol_chain}; with the phase-only minimum (control): {viol_own}')


def part_c():
    inst = I.make('h1')
    dag = inst['reps']['exp']
    F = I.lambdas(inst)[0]
    print('(C) h_{1/2} expanded on intervals in s < 0 (only (c-2)s^2 increases):')
    for box in ([(-2.0, -0.5)], [(-1.5, -0.1)], [(-0.8, -0.3)]):
        g = np.linspace(box[0][0], box[0][1], 20001)
        mn = float(np.min(F(g)))
        p = pi_bisect(dag, box, mn)
        print(f'    C={box[0]}: min_C h = {mn:.6f}, pi_D(C) = {p:.6f}')


def part_d():
    inst = I.make('linediag')
    dag = inst['reps']['exp']
    F, Gf, _ = I.lambdas(inst)
    removals = 0; worst = 0.0; tried = 0
    for _ in range(600):
        t = rng.uniform(0.3, 1.1); u = rng.uniform(-0.01, 0.01)
        y = np.array([t + 1 + u, t])
        eps = 10 ** rng.uniform(-6, -3)
        m = float(F(*y))
        TG = term_grads(inst, y)
        df = np.array(Gf(*y), dtype=float)
        D = [np.abs(TG[:, i]).sum() - 2 * np.abs(TG[:, i]).max() for i in range(2)]
        Dp = min(D[i] - abs(df[i]) for i in range(2))
        if Dp <= 0:
            continue
        r = 4 * (m + eps) / Dp
        box = []
        for i in range(2):
            lo = y[i] - r * 10 ** rng.uniform(-3, 0.5)
            hi = y[i] + r * 10 ** rng.uniform(-3, 0.5)
            box.append((lo, hi))
        tried += 1
        st, vb, _ = hc4(dag, box, -eps, max_rounds=200000)
        removed = st == 'empty' or not all(vb[i][0] - 1e-13 <= y[i] <= vb[i][1] + 1e-13 for i in range(2))
        if removed:
            removals += 1
            ratio = max(max(y[i] - box[i][0], box[i][1] - y[i]) for i in range(2)) / r
            worst = max(worst, ratio)
    print(f'(D) two-sided localization, linediag expanded: {tried} boxes, {removals} removals of y; '
          f'max over removals of (farthest face distance)/(4(m+eps)/D\'_0) = {worst:.3f} (claim: < 1)')


if __name__ == '__main__':
    part_a()
    part_b()
    part_c()
    part_d()
    part_e()
