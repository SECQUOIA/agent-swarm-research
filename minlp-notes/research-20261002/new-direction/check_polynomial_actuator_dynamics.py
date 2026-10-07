"""Exact checks of adjoint reduction and feasible trajectory evaluation."""

from fractions import Fraction as F
from itertools import product
from random import Random


def polynomial(coefficients, value):
    answer = F(0)
    for coefficient in reversed(coefficients):
        answer = answer * value + coefficient
    return answer


def forward(initial, controls, transitions, actuators):
    states = [initial]
    for control, a, coefficients in zip(controls, transitions, actuators):
        states.append(a * states[-1] + polynomial(coefficients, control))
    return states


def adjoints(costs, state_noise, transitions):
    result = [F(0)] * len(costs)
    result[-1] = costs[-1] + state_noise[-1]
    for t in range(len(costs) - 2, -1, -1):
        result[t] = costs[t] + state_noise[t] + transitions[t + 1] * result[t + 1]
    return result


def free_cost(initial, controls):
    """Quartic coupled factors on a path, including its initial endpoint."""
    answer = initial**2 / 7 + initial * controls[0] / 16
    for u in controls:
        answer += u**4 / 16 - u**2 / 8
    answer += sum((u * v / 32 for u, v in zip(controls, controls[1:])), F(0))
    return answer


def values(initial, controls, transitions, actuators, costs, state_noise, free_noise):
    states = forward(initial, controls, transitions, actuators)
    lam = adjoints(costs, state_noise, transitions)
    linear_free = free_noise[0] * initial + sum(
        (noise * u for noise, u in zip(free_noise[1:], controls)), F(0)
    )
    original = free_cost(initial, controls) + linear_free + sum(
        ((c + noise) * state for c, noise, state in zip(costs, state_noise, states[1:])),
        F(0),
    )
    reduced = (
        free_cost(initial, controls)
        + linear_free
        + transitions[0] * lam[0] * initial
        + sum(
            (multiplier * polynomial(g, u) for multiplier, g, u in zip(lam, actuators, controls)),
            F(0),
        )
    )
    return original, reduced, states, lam


def fixture(horizon, rng):
    transitions = [F(rng.choice((-1, 1)), 4) for _ in range(horizon)]
    actuators = [
        [F(0), F(1, 4), F(rng.choice((-1, 1)), 8), F(1, 32), F(-1, 64)]
        for _ in range(horizon)
    ]
    costs = [F(rng.randrange(-6, 7), 5) for _ in range(horizon)]
    # One common endpoint-inclusive eight-point grid, with sigma=1/4.
    noise_grid = [F(-1, 4) + F(j, 14) for j in range(8)]
    state_noise = [rng.choice(noise_grid) for _ in range(horizon)]
    free_noise = [rng.choice(noise_grid) for _ in range(horizon + 1)]
    return transitions, actuators, costs, state_noise, free_noise


def main():
    rng = Random(20261002)
    identities = 0
    lipschitz = 0
    bit_bounds = 0
    for horizon in (1, 2, 4, 8, 16, 32):
        for _ in range(12):
            data = fixture(horizon, rng)
            initial = F(rng.randrange(-32, 33), 32)
            controls = [F(rng.randrange(-32, 33), 32) for _ in range(horizon)]
            original, reduced, states, lam = values(initial, controls, *data)
            assert original == reduced
            assert all(-1 <= state <= 1 for state in states)
            bound = (max(abs(c) for c in data[2]) + F(1, 4)) / F(3, 4)
            assert all(abs(multiplier) <= bound for multiplier in lam)
            identities += 1

            other_initial = F(rng.randrange(-32, 33), 32)
            other_controls = [F(rng.randrange(-32, 33), 32) for _ in range(horizon)]
            other_states = forward(other_initial, other_controls, data[0], data[1])
            free_squared = (initial - other_initial) ** 2 + sum(
                ((u - v) ** 2 for u, v in zip(controls, other_controls)), F(0)
            )
            full_squared = sum(
                ((s - t) ** 2 for s, t in zip(states, other_states)), F(0)
            ) + sum(((u - v) ** 2 for u, v in zip(controls, other_controls)), F(0))
            # |g'| <= 1/4+1/4+3/32+4/64 = 21/32 on [-1,1].
            trajectory_bound = 1 + (1 + F(21, 32)) / F(3, 4)
            assert full_squared <= trajectory_bound**2 * free_squared
            lipschitz += 1

            denominator_bound = initial.denominator.bit_length()
            for state, a, g, u in zip(states[1:], data[0], data[1], controls):
                value = polynomial(g, u)
                denominator_bound += a.denominator.bit_length() + value.denominator.bit_length()
                assert state.denominator.bit_length() <= denominator_bound
                bit_bounds += 1

    mixed_assignments = 0
    gap_transfers = 0
    # Fixed rational initial state and native integer controls. Exhaustive
    # optimization is used only for these tiny diagnostic fixtures.
    for horizon in (1, 2, 3, 4):
        data = fixture(horizon, rng)
        initial = F(1, 3)
        rows = []
        for controls in product((F(-1), F(0), F(1)), repeat=horizon):
            original, reduced, states, _ = values(initial, controls, *data)
            assert original == reduced
            assert all(-1 <= state <= 1 for state in states)
            rows.append((controls, original, reduced))
            mixed_assignments += 1
        original_min = min(row[1] for row in rows)
        reduced_min = min(row[2] for row in rows)
        assert original_min == reduced_min
        assert {row[0] for row in rows if row[1] == original_min} == {
            row[0] for row in rows if row[2] == reduced_min
        }
        for _, original, reduced in rows:
            assert original - original_min == reduced - reduced_min
            gap_transfers += 1

    print(
        f"PASS: {identities} rational adjoint identities and invariant trajectories, "
        f"{lipschitz} trajectory Lipschitz comparisons, "
        f"{bit_bounds} denominator-growth checks, "
        f"{mixed_assignments} native-integer assignments and "
        f"{gap_transfers} exact objective-gap transfers."
    )


if __name__ == "__main__":
    main()
