"""Section 4-5 checks of cutoff-propagation.md with the reviewer's propagator.

(1) Example 4.3 (x^2 - 2xy + y^2): pi_D on boxes vs -2a(b-a); diagonal points kept.
(2) D_i(y), L(y) from term gradients (sympy), linediag/rot/iso2 expanded.
(3) Cube losses (f(y) - pi_D(C))/r at r = 1e-3.
(4) Thin strips through the minimizer (iso2, rot0.1).
(5) Theorem 5.1 (CND vertex localization), linediag expanded, y on the optimal
    line, t in [0.2, 1.1]: random boxes around y; whenever the fixed point
    removes y, check d_i^C(y) < 2(m(y)+eps)/D0 for every i.
(6) Theorem 5.4 (face localization), iso2 and rot0.1 at the minimizer: whenever
    the fixed point removes x*, check min_i d_i^C(x*) < 2 eps / L0.
(7) Corollary 3.3 remark: h_{1/2} on s < 0 (term monotonicity; pi_D = min).
Run: python3 loss_check.py > logs/loss_check.log
"""
import math
import numpy as np
import sympy as sp
import inst as I
from ifbbt import DAG

rng = np.random.default_rng(3)


def term_grads(f, syms, y):
    poly = sp.Poly(sp.expand(f), *syms)
    G = []
    for mon, coef in poly.terms():
        if all(e == 0 for e in mon):
            continue
        t = float(coef) * sp.prod([s ** e for s, e in zip(syms, mon)])
        G.append([float(sp.diff(t, s).subs(dict(zip(syms, y)))) for s in syms])
    return np.array(G)


def DL(f, syms, y):
    G = np.abs(term_grads(f, syms, y))
    D = G.sum(0) - 2 * G.max(0)
    l1 = G.sum(1)
    return D, l1.sum() - 2 * l1.max()


def removed(dag, box, y, cut, R=40000):
    st, Z, r = dag.propagate(box, cut, max_rounds=R)
    if st == 'empty':
        return True, st
    xb = dag.xbox(Z)
    return any(not (lo - 1e-13 <= yi <= hi + 1e-13) for (lo, hi), yi in zip(xb, y)), st


if __name__ == '__main__':
    # (1) Example 4.3
    print('(1) Example 4.3: f = x^2 - 2xy + y^2 (monomials)')
    x, y = I.X[0], I.X[1]
    q = I.expanded(x ** 2 - 2 * x * y + y ** 2, [x, y])
    for box in ([(0.5, 1.5), (0.5, 1.5)], [(0.5, 2.0), (0.8, 1.5)], [(0.1, 3.0), (1.0, 1.2)],
                [(0.9, 1.1), (0.9, 1.1)]):
        a = max(box[0][0], box[1][0]); b = min(box[0][1], box[1][1])
        bound = -2 * a * (b - a)
        p = q.pi(box, hi=0.0)
        st, Z, _ = q.propagate(box, bound + 1e-9)
        xb = q.xbox(Z) if Z is not None else None
        ts = np.linspace(a, b, 7)
        kept = xb is not None and all(xb[0][0] - 1e-12 <= t <= xb[0][1] + 1e-12 and
                                      xb[1][0] - 1e-12 <= t <= xb[1][1] + 1e-12 for t in ts)
        fwd = q.forward_box(box)[-1][0]
        print(f'  box {box}: chord [{a},{b}], -2a(b-a) = {bound:+.4f}, pi_D(C) = {p:+.6f}, '
              f'forward LB = {fwd:+.4f}; all 7 diagonal points kept at c = bound: {kept}')

    # (2)-(3) loss constants and cube losses
    print('\n(2)-(3) D_i, L and cube loss (f(y) - pi_D(C))/r, r = 1e-3')
    cases = [('linediag', 'exp', [1.5, 0.5]), ('linediag', 'exp', [1.2, 0.2]),
             ('linediag', 'exp', [2.0, 1.0]), ('linediag', 'exp', [1.0, 0.0]),
             ('linediag', 'exp', [1.1, 0.1]), ('iso2', 'exp', [1.0, 1.0]),
             ('rot0.1', 'exp', [1.0, 0.0]), ('rot1', 'exp', [1.0, 0.0]),
             ('linediag', 's', [1.5, 0.5]), ('rot0.1', 'st', [1.0, 0.0])]
    for name, rep, yy in cases:
        d = I.make(name)
        dag = d['reps'][rep]
        r = 1e-3
        box = [(v - r, v + r) for v in yy]
        fy = dag.f(yy)
        p = dag.pi(box, hi=fy + 1e-12)
        if rep == 'exp':
            D, L = DL(d['f'], d['syms'], yy)
            head = f'D = {np.round(D, 4)}, L = {L:.4g}'
        else:
            head = 'lifted representation'
        print(f'  {name} {rep} y={yy}: {head}; cube loss = {(fy - p) / r:.3f}')

    # (4) strips
    print('\n(4) strips [x1* +- h] x [x2* - 0.5, x2* + 0.5]')
    for name in ('iso2', 'rot0.1'):
        d = I.make(name); dag = d['reps']['exp']; xs = d['xstar']
        for hh in (1e-2, 1e-3, 1e-4):
            box = [(xs[0] - hh, xs[0] + hh), (xs[1] - 0.5, xs[1] + 0.5)]
            p = dag.pi(box, hi=1e-12)
            print(f'  {name} h={hh:.0e}: pi_D = {p:+.4e}, -pi_D/h = {-p / hh:.3f}')

    # (5) Theorem 5.1 localization test
    print('\n(5) Theorem 5.1: linediag expanded, y = (t+1, t), t in [0.2, 1.1]')
    d = I.make('linediag'); dag = d['reps']['exp']
    D0 = 2.352
    for eps in (1e-4, 1e-5):
        r_loc = 2 * eps / D0
        n_rem = n_viol = n_tot = 0
        one_face = 0
        for trial in range(300):
            t = rng.uniform(0.2, 1.1)
            yv = [t + 1.0, t]
            # distances below/above y in each coordinate; mix of tiny and large
            dist = []
            for i in range(2):
                lo_d = rng.choice([rng.uniform(0, 3 * r_loc), rng.uniform(0, 0.3)])
                hi_d = rng.choice([rng.uniform(0, 3 * r_loc), rng.uniform(0, 0.3)])
                dist.append((lo_d, hi_d))
            box = [(yv[i] - dist[i][0], yv[i] + dist[i][1]) for i in range(2)]
            box = [(max(lo, B[0]), min(hi, B[1])) for (lo, hi), B in zip(box, d['box'])]
            dC = [min(yv[i] - box[i][0], box[i][1] - yv[i]) for i in range(2)]
            rem, st = removed(dag, box, yv, -eps)
            n_tot += 1
            if rem:
                n_rem += 1
                if not all(di < r_loc for di in dC):
                    n_viol += 1
                    print('   VIOLATION', t, box, dC, st)
                if sum(di < r_loc for di in dC) == 1:
                    one_face += 1
        print(f'  eps={eps:.0e}: {n_tot} boxes, y removed in {n_rem}; localization violated in {n_viol}')

    # (6) Theorem 5.4 face localization
    print('\n(6) Theorem 5.4: face localization at the minimizer, removed => min_i d_i < 2 eps / L0 (L0 ~ 8)')
    for name in ('iso2', 'rot0.1'):
        d = I.make(name); dag = d['reps']['exp']; xs = d['xstar']
        for eps in (1e-3, 1e-4):
            n_rem = n_viol = 0
            thr_obs = []
            for trial in range(150):
                near = rng.integers(0, 2)
                dist = []
                for i in range(2):
                    if i == near:
                        dist.append((rng.uniform(0, 0.4 * eps), rng.uniform(0.01, 0.5)))
                    else:
                        dist.append((rng.uniform(0.001, 0.5), rng.uniform(0.001, 0.5)))
                box = [(xs[i] - dist[i][0], xs[i] + dist[i][1]) for i in range(2)]
                dC = [min(xs[i] - box[i][0], box[i][1] - xs[i]) for i in range(2)]
                rem, st = removed(dag, box, xs, -eps)
                if rem:
                    n_rem += 1
                    if not min(dC) < 2 * eps / 8.0 * 1.01:
                        n_viol += 1
                        print('   VIOLATION', box, dC)
                    thr_obs.append(min(dC) / eps)
            mx = max(thr_obs) if thr_obs else float('nan')
            print(f'  {name} eps={eps:.0e}: 150 boxes, x* removed in {n_rem}; violations {n_viol}; '
                  f'largest removed min_i d_i / eps = {mx:.4f} (bound 0.25)')

    # (7) h_{1/2} on s < 0
    print('\n(7) h_{1/2}(s) = s^4 - 1.5 s^2 - s + 1.5 on s < 0: term monotonicity and pi_D')
    for lo, hi in ((-1.5, -0.2), (-0.9, -0.1), (-2.0, -1.0)):
        ss = np.linspace(lo, hi, 5)
        inc = {'s^4': np.all(np.diff(ss ** 4) > 0), '-1.5s^2': np.all(np.diff(-1.5 * ss ** 2) > 0),
               '-s': np.all(np.diff(-ss) > 0)}
        dh = I.make('h1')['reps']['exp']
        p = dh.pi([(lo, hi)], hi=dh.f([hi]))
        mn = min(dh.f([s]) for s in np.linspace(lo, hi, 20001))
        print(f'  [{lo},{hi}]: increasing terms {[k for k, v in inc.items() if v]}; '
              f'pi_D = {p:.8f}, min h = {mn:.8f}')
