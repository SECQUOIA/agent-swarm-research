"""Independent exact checks of affine-repair cancellation on state chains."""

from fractions import Fraction as Q
import json
from pathlib import Path
import random


rng = random.Random(20261002)
checked = 0
largest_repaired_drift_ratio = 0.0


def sample():
    return Q(rng.randrange(-8, 9), 8)


def simulate(s0, controls, a, b):
    states = [s0]
    for u in controls:
        states.append(a * states[-1] + b * u)
    return states


def objective(states, controls):
    return sum(s * s for s in states) + sum(u * u - u**4 / 4 for u in controls)


for horizon in [1, 2, 3, 7, 12]:
    for a, b in [(Q(1, 2), Q(1, 2)), (Q(-1, 2), Q(1, 4)), (Q(0), Q(1))]:
        for _ in range(20):
            cu = [sample() for _ in range(horizon)]
            cs = simulate(sample(), cu, a, b)
            z = [(sample(), sample()) for _ in range(horizon)]
            z = [(s, u, a * s + b * u) for s, u in z]
            xs = [z[0][0]] + [v[2] for v in z]
            xu = [v[1] for v in z]
            ys = simulate(xs[0], xu, a, b)
            assert all(abs(s) <= 1 for s in ys)
            mu = [Q(0)] * horizon
            mu[-1] = -2 * cs[-1]
            for t in range(horizon - 1, 0, -1):
                mu[t - 1] = a * mu[t] - 2 * cs[t]
            phi = Q(0)
            taylor = Q(0)
            errors = Q(0)
            ex = Q(0)
            ey = Q(0)
            for t, (s, u, snext) in enumerate(z):
                az = snext**2 + u**2 - u**4 / 4
                ay = ys[t + 1]**2 + u**2 - u**4 / 4
                linear = 2 * cs[t + 1] * (snext - ys[t + 1])
                if t == 0:
                    az += s**2
                    ay += ys[0]**2
                    linear += 2 * cs[0] * (s - ys[0])
                if t > 0:
                    slope = -a * mu[t]
                    phi += slope * (z[t - 1][2] - s)
                err = (1 - u**2) / 2
                phi += az - err
                errors += err
                taylor += az - ay - linear
                ex += (s - xs[t])**2 + (snext - xs[t + 1])**2
                ey += (s - ys[t])**2 + (snext - ys[t + 1])**2
            assert phi == objective(ys, xu) + taylor - errors
            residual_sq = sum((xs[t + 1] - a * xs[t] - b * xu[t])**2 for t in range(horizon))
            repair_sq = sum((x - y)**2 for x, y in zip(xs, ys))
            assert repair_sq <= residual_sq / (1 - abs(a))**2
            assert residual_sq <= (1 + a * a + b * b) * ex
            chi = float(1 + a * a + b * b)**0.5 / float(1 - abs(a))
            upper = (1 + 2**0.5 * chi)**2 * float(ex)
            assert float(ey) <= upper + 1e-12
            if upper:
                largest_repaired_drift_ratio = max(largest_repaired_drift_ratio, float(ey) / upper)
            checked += 1

# The author's fixed a=b=1/2 example remains nonconvex on its feasible set.
# Vary only the final control and state, with every earlier variable zero.
u = Q(15, 16)
reduced_curvature = 2 * (1 + Q(1, 2)**2) - 3 * u**2
assert reduced_curvature < 0

result = {
    "exact_configuration_identity_checks": checked,
    "repair_and_residual_bound_checks": checked,
    "maximum_repaired_drift_ratio": largest_repaired_drift_ratio,
    "reduced_objective_curvature_at_15_over_16": str(reduced_curvature),
    "status": "passed",
    "scope": "Exact rational cancellation checks and targeted repair inequalities; not a constrained DP implementation.",
}
destination = Path(__file__).with_suffix(".json")
destination.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
