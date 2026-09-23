# Exact arc-flow extrema and robust capacity validation on bounded-rank blocks

Date: 2026-09-05. Status: passed the exact-flow addenda of [first independent review](../notes/review-potential-flow-joint-resistance.md) and [second independent review](../notes/review-potential-flow-joint-resistance-second.md). This is a corollary of the [joint nomination/resistance synthesis](potential-flow-joint-resistance.md), [bounded-rank nomination structure](potential-flow-bounded-block-rank.md), and [fixed-core/polyhedral-block theorem](fixed-core-block-polyhedral-optimization.md). The [joint-model novelty audit](../notes/potential-flow-joint-resistance-novelty.md) supplies literature context; the exact arc-capacity corollary has not had a separate exhaustive novelty search. No prior matching structural theorem was found in the inspected joint-uncertainty literature.

The exact guarantee here differs from pressure-span comparison across many blocks, which can encode Square-Root Sum.

## Theorem

Fix a bound `r` on the cycle rank of every biconnected block. Consider a connected passive quadratic network, rational finite nomination intervals with a nonempty balanced box, and independent positive rational resistance intervals. Then the exact maximum and minimum signed physical flow on any specified edge can be computed in polynomial bit time for fixed `r`, with real-algebraic values of polynomial encoding length.

Consequently, deciding whether **every** admissible nomination/resistance scenario satisfies all prescribed rational lower and upper arc-flow capacities is in polynomial time for fixed `r`. This is an exact equality-sensitive decision statement for flow capacities. It imposes no potential bounds and no controllable elements. The number of blocks and total number of cycles may be unbounded.

The fixed-resistance case follows by making each resistance interval a singleton.

## Proof

Let `e=(u,v)` be the objective edge and let `H` be its unique biconnected block, allowing a bridge as a block. The block-cut path between `u` and `v` consists of `H` alone. Aggregate every component outside `H` into its unique attachment vertex, adding nomination intervals. For every admissible scenario, the flow on `e` is determined by these aggregated nominations and resistances inside `H`; outside resistance choices do not affect it. Conversely every admissible aggregate nomination can be disaggregated, and all passive physical flows exist uniquely. Thus the edge-flow extremum is a single-block optimization problem.

Take a joint maximizer `(b*,beta*)` of `x_e`. At fixed `beta*`,

```
x_e=sign(pi_u-pi_v) sqrt(|pi_u-pi_v|/beta*_e)
```

is strictly increasing in `pi_u-pi_v`. Therefore its nomination maximizers coincide with the potential-difference nomination maximizers for terminals `u,v`. The reviewed bounded-rank theorem supplies one such maximizing nomination in a polynomially enumerable family with `O(r)` free coordinates, independent of the resistance values. Keeping `beta*` fixed transfers the joint edge-flow optimum to that family.

For each nomination face, parameterize its free nominations and at most `r` circulation variables by a fixed-dimensional core `z`. Every edge flow, including the objective flow, is affine in `z`. Within a sign cell, the physical cycle equations are

```
sum_f Z_if beta_f sign_f [x_f(z)]^2=0,
```

linear in the scalar resistance leaves `beta_f` with quadratic core coefficients. The objective `x_e(z)` is a linear **core-only** objective; leaf objective coefficients are zero. All core/leaf variables have finite rational bounds.

This is exactly the fixed-core/polyhedral-block model with fixed core dimension, scalar box leaves, and at most `r` aggregate equations. Its exact real-algebraic optimization theorem returns the local optimum value with polynomial encoding length. The number of faces and sign cells is polynomial for fixed `r`; comparisons of their algebraic objective values are polynomial in their encoding lengths. Taking the largest yields the global maximum. Apply the same argument to the reversed objective orientation `(v,u)` to obtain the minimum signed flow.

A bridge is simpler: its flow equals the signed total nomination on one side. It is independent of all resistances and its extrema follow from a rational linear optimization over the balanced box, or directly from interval sums.

For capacity validation, compute each edge's two extrema and compare exactly with the given rational bounds. Every scenario satisfies every capacity if and only if each maximum is at most its upper bound and each minimum is at least its lower bound. There are only twice as many optimizations as edges. Physical uniqueness means this is also equivalent to robust feasibility when the only extra operating constraints are these arc-flow capacities.

## Why the earlier arithmetic barrier does not apply

The exact single-entry cactus pressure-span reduction adds algebraic potential drops across an unbounded chain of blocks. An objective edge's endpoints belong to one block, so its extremum contains no such sum of independent block values. All relevant algebraic optimization takes place in one fixed-dimensional core after the nomination-face reduction. This is a structural explanation for the different guarantees, not a claim that arbitrary exact nonlinear network comparison is easy.

## Output and uncertainty caveats

The theorem claims exact algebraic **extremum values**, and optionally algebraic local optimizer data, with polynomial encoding length. It does not claim rational physical flows or potentials. If rational near-optimal nomination/resistance inputs are desired, round the algebraic **edge-flow** optimizer itself. Let `x,y` be its target-edge flow and the rounded scenario's target-edge flow, and let `D,D'` be their endpoint potential differences. The scalar inequality `|x|x-|y|y` in the direction of `x-y` has magnitude at least `|x-y|^2/2`, so

```
|x-y|^2 <= 2[|D-D'|+B^2|beta_e-gamma_e|]/beta_lower_e.
```

Combine this with the joint pressure Lipschitz bound for terminals `u,v`. Choosing polynomially many precision bits so the nomination/resistance l1 errors are proportional to the square of the desired flow error gives the guarantee. Rational box/balance recovery then proceeds as in the joint result. One must not substitute a pressure-maximizing resistance scenario for the edge-flow optimizer, because the two objectives need not have the same maximizers when the target-edge resistance varies.

Capacity validation concerns all scenarios in the original nomination/resistance uncertainty set. It does not optimize over only scenarios already satisfying some subset of capacities, and it does not incorporate node potential bounds. Those would alter the extremum problem.

## Verification

Both independent reviewers checked the monotone transfer at fixed resistance, single-block aggregation, core-only objective, polynomial algebraic comparison, and the optional rational-witness estimate. The latter must round an exact edge-flow optimizer rather than a pressure optimizer when resistance varies.

The [direct core/leaf mapping checker](../code/potential_flow_mpd/joint_core_mapping_checks.py) verifies the affine edge-flow objective under changes in LP-feasible resistance leaves. Forty exact rational cycle identities passed, and nonlinear physical recovery preserved edge flows and path objectives to maximum error `3.24e-12`. This supports the local encoding but is not an implementation of exact global algebraic optimization.
