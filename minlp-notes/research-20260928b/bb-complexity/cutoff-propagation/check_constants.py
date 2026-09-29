"""Constants for the transfer theorems (Section 5 of the note), and a test of
face-localization on thin strips.

(a) linediag, expanded monomial representation: coordinatewise no-dominant-term
    constant D_i(y) along the optimal line y = (t+1, t); second-derivative
    constant K on coordinate segments; transfer constant alpha_F = D0/(2 n s0);
    smallness threshold D0^2/(4K); resulting covering lower bound (Theorem 5.2
    with Theorem 4.6 of the constrained note, eta = 0) against the node counts
    of logs/sweep.jsonl.
(b) iso2 and rot0.1, expanded representation: pi_D on thin strips
    [x*_1 - h, x*_1 + h] x [x*_2 - 0.5, x*_2 + 0.5] (long in x_2): the loss is
    first order in the thin width h only, so propagation can prune long thin
    boxes through a minimizer (face-, not vertex-localization).
Run: python3 check_constants.py > logs/check_constants.log
"""
import json
import math
import numpy as np
import instances as I
from check_loss import term_grads, pi_bisect
from fbbt import evaluate


def second_partials(inst, y):
    """|d_ii g_j(y)| for each term j and coordinate i."""
    terms, _ = I.poly_terms(inst['f'], inst['syms'])
    H = np.zeros((len(terms), len(y)))
    for j, (coef, exps) in enumerate(terms):
        for i, e in exps.items():
            if e < 2:
                continue
            v = coef * e * (e - 1) * y[i] ** (e - 2)
            for k, e2 in exps.items():
                if k != i:
                    v *= y[k] ** e2
            H[j, i] = abs(v)
    return H


def part_a():
    inst = I.make('linediag')
    n, s0, alpha = 2, 4.2, inst['alpha']
    print('(a) linediag, expanded representation, optimal line y = (t+1, t)')
    for t in (-0.8, -0.5, -0.2, 0.0, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0, 1.1):
        y = np.array([t + 1.0, t])
        G = term_grads(inst, y)
        D = [np.abs(G[:, i]).sum() - 2 * np.abs(G[:, i]).max() for i in range(n)]
        print(f'   t={t:+.2f}  D_1={D[0]:+.3f}  D_2={D[1]:+.3f}')
    t1, t2 = 0.2, 1.1
    ts = np.linspace(t1, t2, 181)
    D0 = min(min(np.abs(term_grads(inst, np.array([t + 1, t]))[:, i]).sum()
                 - 2 * np.abs(term_grads(inst, np.array([t + 1, t]))[:, i]).max() for i in range(n))
             for t in ts)
    # K over coordinate segments of half-length 1 around the sub-segment (upper bound)
    Hmax = None
    for t in ts:
        for i in range(n):
            for s in np.linspace(-1, 1, 41):
                y = np.array([t + 1.0, t]); y[i] += s
                Hs = second_partials(inst, y)[:, i]
                Hmax = Hs if Hmax is None else np.maximum(Hmax, Hs)
    K = Hmax.sum() / 2 + Hmax.max()
    rho = D0 / (2 * K)
    alphaF = D0 / (2 * n * s0)
    aeff = min(alpha, alphaF)
    thr = D0 ** 2 / (4 * K)
    print(f'   sub-segment t in [{t1}, {t2}]: D0={D0:.4f}, K={K:.2f} (segments |s|<=1, '
          f'so rho=D0/(2K)={rho:.4f} <= 1), alpha_F=D0/(2 n s0)={alphaF:.4f}, '
          f'alpha={alpha}, alpha_eff={aeff:.4f}, threshold eps+eta < D0^2/(4K)={thr:.2e}')
    rows = [json.loads(l) for l in open('logs/sweep.jsonl')]
    ell = t2 - t1
    for eps in (1e-3, 1e-4, 1e-5, 1e-6):
        if eps >= thr:
            continue
        delta = 2 * math.sqrt(eps / aeff)
        bound = 2 ** (-n) * math.ceil(ell / delta)
        nodes = {r['mode']: r['nodes'] for r in rows
                 if r['inst'] == 'linediag' and r['eps'] == eps and r['rep'] in ('exp', '-')}
        print(f'   eps={eps:.0e}: covering lower bound on |P| (hybrid, any tree, any FBBT) '
              f'= {bound}; nodes >= |P|/(2n+1) = {bound / (2 * n + 1):.1f}; '
              f'observed nodes off/fix/10 = {nodes.get("off")}/{nodes.get("fix")}/{nodes.get("10")}')


def part_b():
    print('(b) thin strips through the minimizer, expanded representation')
    for name in ('iso2', 'rot0.1'):
        inst = I.make(name)
        dag = inst['reps']['exp']
        xs = inst['xstar']
        for h in (0.1, 0.01, 0.001, 0.0001):
            box = [(xs[0] - h, xs[0] + h), (xs[1] - 0.5, xs[1] + 0.5)]
            p = pi_bisect(dag, box, evaluate(dag, xs))
            print(f'   {name}: strip half-width h={h:<7} long side 1.0: pi_D={p:+.4e}  -pi/h={-p / h:.3f}')


if __name__ == '__main__':
    part_a()
    part_b()
