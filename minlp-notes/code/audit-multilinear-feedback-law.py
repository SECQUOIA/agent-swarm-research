"""Exact small-grid audit of the universal feedback-variable marginal law."""

from fractions import Fraction as F
from itertools import product


def joint_mass(feedback_means, outside_mean, state, outside_state):
    total = F(0)
    f = len(feedback_means)
    for orientation in product((0, 1), repeat=f):
        lo, hi = (F(0), outside_mean) if outside_state else (outside_mean, F(1))
        for mean, bit, right in zip(feedback_means, state, orientation):
            if not right:
                a, b = (F(0), mean) if bit else (mean, F(1))
            else:
                a, b = (1 - mean, F(1)) if bit else (F(0), 1 - mean)
            lo, hi = max(lo, a), min(hi, b)
        total += max(F(0), hi - lo)
    return total / (2 ** f)


if __name__ == "__main__":
    grid = [F(k, 4) for k in range(5)]
    for f in range(4):
        states = list(product((0, 1), repeat=f))
        count = 0
        for means in product(grid, repeat=f + 1):
            feedback, outside = means[:-1], means[-1]
            law = {(s, b): joint_mass(feedback, outside, s, b)
                   for s in states for b in (0, 1)}
            assert sum(law.values()) == 1
            assert sum(law[s, 1] for s in states) == outside
            for j in range(f):
                assert sum(mass for (s, b), mass in law.items() if s[j]) == feedback[j]
            for s in states:
                literal_probs = [mean if bit else 1 - mean for mean, bit in zip(feedback, s)]
                q_f = sum(law[s, b] for b in (0, 1))
                assert q_f >= min(literal_probs, default=F(1)) / (2 ** f)
                for b in (0, 1):
                    bound = min(literal_probs + [outside if b else 1 - outside])
                    assert law[s, b] >= bound / (2 ** f)
            count += 1
        print(f"f={f}: {count} mean vectors passed normalization, margins, and all domination bounds")
