"""Recheck of Proposition 3.9 and of the restated round-count criterion.

(A) Proposition 3.9: (s-a)^2 as s^2 - 2as + a^2, HC4 rounds (forward, cutoff
    -eps, backward) from [a - y0, a + x0], x0, y0 <= a/4, eps <= a^2/16.
    The box must stay nonempty for at least
      B = (a/(4 sqrt eps)) (arctan(z0/sqrt eps) - arctan(4 sqrt(eps)/a)) - 1
    rounds, z0 = min(x0, y0). Also: rounds for a random partial-step order.
(B) Criterion "every term strictly monotone at the minimizer" (slow) versus
    "some term stationary there / minimizer at the end of a lifted range"
    (few rounds). Root round counts at cutoff f* - eps = -eps.
Run: python3 check_rounds.py > logs/check_rounds.log
"""
import math
import random
import iprop as P
import inst as I

rng = random.Random(39)


def rounds_to_empty(dag, box, c, maxr=400000, schedule='hc4'):
    st, _, r = P.fixpoint(dag, box, c, max_rounds=maxr, rtol=0.0, schedule=schedule, rng=rng)
    return r if st == 'empty' else None


def part_a():
    print('(A) Proposition 3.9 (HC4 as in the note):')
    ok = bad = 0
    rows = []
    for a in (0.5, 1.0, 2.0):
        for x0f, y0f in ((0.25, 0.25), (0.25, 0.05), (0.02, 0.25), (0.1, 0.1)):
            x0, y0 = x0f * a, y0f * a
            for k in range(2, 9):
                eps = 10.0 ** (-k)
                if eps > a * a / 16:
                    continue
                R = rounds_to_empty(I.quad(a), [(a - y0, a + x0)], -eps)
                z0 = min(x0, y0)
                se = math.sqrt(eps)
                B = (a / (4 * se)) * (math.atan(z0 / se) - math.atan(4 * se / a)) - 1
                good = R is not None and R - 1 >= B
                ok += good
                bad += not good
                rows.append((a, x0f, y0f, eps, R, B))
    print(f'    {ok + bad} runs (a in 0.5,1,2; 4 start boxes; eps 1e-2..1e-8): '
          f'nonempty for >= B rounds in {ok}, violated in {bad}')
    worst = min(((R - 1) / B, a, x0f, y0f, eps) for a, x0f, y0f, eps, R, B in rows if B > 0)
    print(f'    smallest (rounds before emptying)/B = {worst[0]:.2f} '
          f'(a={worst[1]}, x0={worst[2]}a, y0={worst[3]}a, eps={worst[4]:.0e})')
    for a in (1.0,):
        line = []
        for k in (2, 4, 6, 8):
            eps = 10.0 ** (-k)
            R = rounds_to_empty(I.quad(a), [(0.2, 2.2)], -eps)
            line.append(f'{R * math.sqrt(eps) / a:.3f}')
        print(f'    box [0.2, 2.2], a = 1: rounds*sqrt(eps)/a at eps=1e-2,-4,-6,-8: {", ".join(line)} '
              f'(note: -> pi)')
    line = []
    for k in (2, 4, 6):
        eps = 10.0 ** (-k)
        R = rounds_to_empty(I.quad(1.0), [(0.2, 2.2)], -eps, schedule='rand')
        line.append(f'{R * math.sqrt(eps):.2f}')
    print(f'    random partial-step order, same box: rounds*sqrt(eps) = {", ".join(line)}')


def part_b():
    print('(B) root round counts at cutoff -eps (f* = 0), eps = 1e-2, 1e-4, 1e-6, 1e-8:')
    cases = [
        ('(s-1)^2 as s^2 - 2s + 1, [0.2,2.2]', I.quad(1.0), [(0.2, 2.2)],
         'all terms strictly monotone'),
        ('t^2 - 2t^4 monomial, [-1/3,2/3]', I.nondeg1('mono')['dag'], [(-1 / 3, 2 / 3)],
         'all terms stationary'),
        ('t^2 - 2t^4 as u - 2u^2, [-1/3,2/3]', I.nondeg1('u')['dag'], [(-1 / 3, 2 / 3)],
         'lifted endpoint u = 0'),
        ('x^2 - 2x + 1 + (x-1)^4, [0.2,2.2]', I.quad_plus_quartic(), [(0.2, 2.2)],
         'term (x-1)^4 stationary, at end of its range'),
        ('rot1 / st (root box)', I.rot(1.0, 'st')['dag'], I.rot(1.0, 'st')['box'],
         'term (x+y-1)^2 stationary, at end of its range'),
        ('rot1 / st, [0.9,1.1]x[-0.1,0.1]', I.rot(1.0, 'st')['dag'], [(0.9, 1.1), (-0.1, 0.1)],
         'same'),
        ('line3 / st (root box)', I.line3_st()['dag'], I.line3_st()['box'],
         'term (x1+x2-1)^2 stationary, at end of its range'),
    ]
    for label, dag, box, why in cases:
        out = []
        for k in (2, 4, 6, 8):
            eps = 10.0 ** (-k)
            R = rounds_to_empty(dag, box, -eps)
            out.append((R, R * math.sqrt(eps) if R else None))
        cnt = ', '.join(str(R) for R, _ in out)
        sc = ', '.join(f'{v:.2f}' for _, v in out)
        print(f'    {label:36s} [{why}]: rounds {cnt}; rounds*sqrt(eps) {sc}')


if __name__ == '__main__':
    part_a()
    part_b()
