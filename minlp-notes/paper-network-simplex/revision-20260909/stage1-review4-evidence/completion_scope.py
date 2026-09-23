"""Exact witness that locally absent states are not uniquely reconstructed."""

from fractions import Fraction as F

# Directed three-cycle, all capacities one, zero balances, one observed
# coordinate (arc 0, label 1). Every displayed state is a constant circulation.
weights = (F(1, 2), F(1, 4), F(1, 4))
aggregate = (F(1, 2),) * 3
observed = F(1, 10)
lifts = (
    ((F(1, 4),) * 3, (F(1, 10),) * 3, (F(3, 20),) * 3),
    ((F(1, 5),) * 3, (F(1, 10),) * 3, (F(1, 5),) * 3),
)

for lift in lifts:
    for weight, state in zip(weights, lift):
        assert all(0 <= value <= weight for value in state)
        assert all(state[i - 1] == state[i] for i in range(3))
    assert tuple(sum(state[e] for state in lift) for e in range(3)) == aggregate
    assert lift[1][0] == observed

assert lifts[0][2] != lifts[1][2]
# For the only locally observed label, two unobserved edges form a tree.
rho_observed_label = 2 - 3 + 1
assert rho_observed_label == 0
print("PASS: rho=0 reconstructs label 1, while feasible label-2 products differ.")
