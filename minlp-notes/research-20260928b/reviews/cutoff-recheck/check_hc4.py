"""Recheck of the HC4 paragraph after Lemma 1.1: fair runs of partial steps
(forward / backward / cutoff) converge to Z*, whatever the schedule.

(A) HC4 order against random orders of the partial steps: same empty/nonempty
    verdict and the same limit box (to 1e-7), on random boxes and cutoffs.
(B) 1D flat sums with non-monotone monomial terms: pi_D(C) from bisection on
    HC4 against min Phi(U') of Theorem 3.1(b) on a grid of sub-intervals
    (grid value >= true minimum, so HC4 value <= grid value up to resolution).
Run: python3 check_hc4.py > logs/check_hc4.log
"""
import random
import numpy as np
import iprop as P
import inst as I

rng = random.Random(7)


def part_a():
    insts = {'linediag/exp': I.linediag('exp'), 'linediag/s': I.linediag('s'),
             'rot0.1/exp': I.rot(0.1, 'exp'), 'rot1/st': I.rot(1.0, 'st'),
             'iso2/exp': I.iso2(), 'endpoint': I.endpoint(), 'nondeg1/u': I.nondeg1('u'),
             'line3/st': I.line3_st()}
    agree = verdict_diff = box_diff = skipped = 0
    worst = 0.0
    for name, J in insts.items():
        dag = J['dag']
        for _ in range(25):
            C = [(lo + rng.uniform(0, 0.45) * (hi - lo), hi - rng.uniform(0, 0.45) * (hi - lo))
                 for lo, hi in J['box']]
            Fl = P.z0(dag, C)[-1][0]
            c = Fl + rng.uniform(0.0, 1.0) * (min(P.evaluate(dag, [0.5 * (a + b) for a, b in C])[-1],
                                                  Fl + 5.0) - Fl)
            s1, Z1, _ = P.fixpoint(dag, C, c, max_rounds=50000, rtol=1e-15)
            s2, Z2, _ = P.fixpoint(dag, C, c, max_rounds=50000, rtol=1e-15, schedule='rand', rng=rng)
            if 'limit' in (s1, s2):
                skipped += 1
                continue
            if s1 != s2:
                verdict_diff += 1
                continue
            if s1 == 'empty':
                agree += 1
                continue
            d = max(max(abs(a[0] - b[0]), abs(a[1] - b[1])) for a, b in zip(Z1, Z2))
            worst = max(worst, d)
            if d > 1e-7:
                box_diff += 1
            else:
                agree += 1
    print(f'(A) HC4 vs random partial-step order: {agree} agree, {verdict_diff} different verdicts, '
          f'{box_diff} different limit boxes (> 1e-7), {skipped} unconverged skipped; '
          f'max lifted-box difference {worst:.1e}')


def part_b():
    n_ok = n_bad = 0
    worst = -np.inf
    for trial in range(40):
        J = rng.randint(2, 4)
        terms = [(rng.choice([-3, -2, -1, 1, 2, 3]) * rng.uniform(0.3, 1.0), rng.randint(1, 4))
                 for _ in range(J)]
        d = P.DAG(1)
        ch2, co2, tl = [], [], []
        used_var = False
        for a, k in terms:
            if k == 1 and used_var:
                continue                      # one bare-variable term at most
            ch2.append(0 if k == 1 else d.pow(0, k))   # fresh power node per term
            co2.append(a)
            tl.append((a, k))
            used_var = used_var or k == 1
        d.sum(ch2, co2)
        dag = d.nodes
        lo, hi = sorted([rng.uniform(-1.5, 1.5), rng.uniform(-1.5, 1.5)])
        if hi - lo < 0.2:
            continue
        g = np.linspace(lo, hi, 161)
        best = np.inf
        for i in range(len(g)):
            for j in range(i, len(g)):
                seg = g[i:j + 1]
                m = [np.min(a * seg ** k) for a, k in tl]
                h = [max(a * g[i] ** k, a * g[j] ** k) for a, k in tl]
                best = min(best, sum(m) + max(hh - mm for hh, mm in zip(h, m)))
        # bisection for pi_D(C)
        a_, b_ = P.z0(dag, [(lo, hi)])[-1][0] - 1e-9, best + 1.0
        for _ in range(45):
            mid = 0.5 * (a_ + b_)
            st, _, _ = P.fixpoint(dag, [(lo, hi)], mid, max_rounds=100000)
            if st == 'empty':
                a_ = mid
            else:
                b_ = mid
        pi = 0.5 * (a_ + b_)
        worst = max(worst, pi - best)
        if pi <= best + 1e-7:
            n_ok += 1
        else:
            n_bad += 1
    print(f'(B) 1D flat sums: HC4 pi_D <= grid min Phi in {n_ok} cases, > in {n_bad}; '
          f'max (pi_D - grid min Phi) = {worst:.2e} (should be <= 0 and close to 0)')


if __name__ == '__main__':
    part_a()
    part_b()
