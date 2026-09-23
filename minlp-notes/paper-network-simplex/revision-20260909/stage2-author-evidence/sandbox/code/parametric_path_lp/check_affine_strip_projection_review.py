"""Exact independent comparison for affine-strip path elimination.

Compares normalized all-pairs projection/recovery with forward reachable
interval propagation in the original coordinates. No floating-point LP is used.
"""

from fractions import Fraction as Q
import random


def intersect_retained(lower, upper, retained):
    lower, upper = lower[:], upper[:]
    for index, value in retained.items():
        lower[index] = max(lower[index], value)
        upper[index] = min(upper[index], value)
    return lower, upper


def forward_feasible(lower, upper, gains, offsets_low, offsets_high, retained):
    lower, upper = intersect_retained(lower, upper, retained)
    if any(l > u for l, u in zip(lower, upper)):
        return False
    lo, hi = lower[0], upper[0]
    for i, (a, b, c) in enumerate(zip(gains, offsets_low, offsets_high), 1):
        if b > c:
            return False
        image_lo, image_hi = sorted((a * lo, a * hi))
        lo, hi = max(lower[i], image_lo + b), min(upper[i], image_hi + c)
        if lo > hi:
            return False
    return True


def normalized_recover(lower, upper, gains, offsets_low, offsets_high, retained):
    lower, upper = intersect_retained(lower, upper, retained)
    starts = [0]
    for i, a in enumerate(gains, 1):
        if a == 0:
            lower[i] = max(lower[i], offsets_low[i - 1])
            upper[i] = min(upper[i], offsets_high[i - 1])
            starts.append(i)
    if any(l > u for l, u in zip(lower, upper)):
        return None
    starts.append(len(lower))
    answer = [None] * len(lower)
    for start, end in zip(starts, starts[1:]):
        count = end - start
        products = [Q(1)]
        alphas, betas = [Q(0)], [Q(0)]
        for i in range(start + 1, end):
            product = products[-1] * gains[i - 1]
            products.append(product)
            b, c = offsets_low[i - 1] / product, offsets_high[i - 1] / product
            alpha, beta = (b, c) if product > 0 else (c, b)
            if alpha > beta:
                return None
            alphas.append(alphas[-1] + alpha)
            betas.append(betas[-1] + beta)
        low, high = [], []
        for index, product in zip(range(start, end), products):
            l, u = lower[index] / product, upper[index] / product
            low.append(l if product > 0 else u)
            high.append(u if product > 0 else l)

        def distance(source, target):
            if source <= target:
                return betas[target] - betas[source]
            return alphas[target] - alphas[source]

        if any(low[i] > high[j] + distance(j, i)
               for i in range(count) for j in range(count)):
            return None
        for i in range(count):
            answer[start + i] = products[i] * min(
                high[j] + distance(j, i) for j in range(count)
            )
    return answer


rng = random.Random(2026090519)
gain_choices = [Q(-3, 2), Q(-1), Q(0), Q(1, 2), Q(2)]
feasible = infeasible = zero_cases = negative_cases = 0
for case in range(1200):
    edges = rng.randrange(1, 9)
    gains = [rng.choice(gain_choices) for _ in range(edges)]
    planted = [Q(rng.randrange(-12, 13), 3) for _ in range(edges + 1)]
    if case % 2 == 0:
        lower = [v - Q(rng.randrange(5), 2) for v in planted]
        upper = [v + Q(rng.randrange(5), 2) for v in planted]
        residuals = [planted[i + 1] - a * planted[i] for i, a in enumerate(gains)]
        offset_low = [v - Q(rng.randrange(5), 2) for v in residuals]
        offset_high = [v + Q(rng.randrange(5), 2) for v in residuals]
    else:
        lower = [Q(rng.randrange(-12, 4), 3) for _ in planted]
        upper = [l + Q(rng.randrange(10), 2) for l in lower]
        offset_low = [Q(rng.randrange(-8, 5), 3) for _ in gains]
        offset_high = [b + Q(rng.randrange(9), 2) for b in offset_low]
        if case % 11 == 1:
            upper[rng.randrange(edges + 1)] -= 10
        if case % 13 == 1:
            offset_high[rng.randrange(edges)] -= 10
    retained = {}
    mode = (case // 2) % 4
    if mode in (1, 3):
        retained[0] = planted[0]
    if mode in (2, 3):
        retained[edges] = planted[edges]
    reference = forward_feasible(lower, upper, gains, offset_low, offset_high, retained)
    witness = normalized_recover(lower, upper, gains, offset_low, offset_high, retained)
    assert reference == (witness is not None)
    if witness is None:
        infeasible += 1
    else:
        feasible += 1
        assert all(l <= v <= u for l, v, u in zip(lower, witness, upper))
        assert all(witness[index] == value for index, value in retained.items())
        assert all(b <= witness[i + 1] - a * witness[i] <= c
                   for i, (a, b, c) in enumerate(zip(gains, offset_low, offset_high)))
    zero_cases += 0 in gains
    negative_cases += any(a < 0 for a in gains)

print(f"PASS: 1200 exact projection comparisons ({feasible} feasible, "
      f"{infeasible} infeasible); all recovered witnesses verified; "
      f"{zero_cases} zero-gain and {negative_cases} negative-gain cases")
