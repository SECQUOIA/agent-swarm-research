# Convex nonlinear leaves already create an exact arithmetic barrier

Date: 2026-09-05. Status: checked deduction from the independent
[fractional-power review](review-potential-flow-fractional-power-arc.md),
also checked by the root agent. No standalone novelty claim is made.

The [fixed-core block theorem](../results/fixed-core-block-polyhedral-optimization.md)
requires polyhedral leaf fibers. Compact convex semialgebraic fibers of
fixed dimension and degree cannot replace them without an additional
exact-arithmetic qualification.

Given positive integers `a_i` and integer `K`, take scalar leaf sets

```
P_i={y_i: 0<=y_i<=max(1,a_i), y_i^2=a_i}.
```

Each is a compact convex singleton, given by rational quadratic data.
There is no nonlinear core. Impose one aggregate inequality
`sum_i y_i<=K`. Feasibility is precisely `sum_i sqrt(a_i)<=K`.
Thus an exact polynomial bit-time extension to these leaves would solve
Square-Root Sum in polynomial time. This is an arithmetic reduction,
not an NP-hardness result or a prohibition on additive approximation.

The obstruction is already present before core elimination: exact sums
of independently encoded algebraic leaf values can have growing field
degree. Polyhedral scalar fibers avoid this particular obstruction.
