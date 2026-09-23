# Polynomial additive optimization under joint nomination and resistance uncertainty

Date: 2026-09-05. Status: passed [first independent mathematical review](../notes/review-potential-flow-joint-resistance.md) and [second independent mathematical review](../notes/review-potential-flow-joint-resistance-second.md), including the exact arc-flow corollary. A [separate bounded novelty audit](../notes/potential-flow-joint-resistance-novelty.md) found no matching structural complexity theorem in the inspected open primary literature. These are internal research checks, not external peer review, and novelty remains provisional.

This theorem combines the [bounded-block-cycle-rank nomination structure](potential-flow-bounded-block-rank.md) with [fixed-core/polyhedral-block optimization](fixed-core-block-polyhedral-optimization.md). The simultaneous nomination/resistance uncertainty model is established; the contribution is the polynomial bit-complexity guarantee for fixed maximum block cycle rank.

## Theorem

Fix a bound `r` on the cycle rank of every biconnected block. Consider a connected network with the quadratic passive law

```
pi_u-pi_v=beta_e x_e|x_e|,
0<beta_lower_e<=beta_e<=beta_upper_e,
l_v<=b_v<=u_v,    sum_v b_v=0.
```

All bounds are rational, finite, and independent except for nomination balance. Assume the balanced nomination box is nonempty. The original nomination intervals may be arbitrarily shifted; they need not contain zero.

Optimize `pi_s-pi_t` jointly over nominations and resistances, for any distinct objective vertices `s,t`. The conclusion is a certified rational optimal-value interval of width at most `epsilon` and feasible rational nomination/resistance vectors within additive `epsilon` of the optimum, in time polynomial in input bit length and requested precision bits, for fixed `r`.

Feasibility of the output refers to the exact nomination bounds, nomination balance, and resistance boxes. Its unique physical flows and potentials need not be rational. No additional flow capacities, potential bounds, compressors, valves, or binary decisions are present in this MPD subproblem. Exact threshold decision is not claimed.

## 1. A fixed-resistance optimal-face theorem transfers directly

Let `(b*,beta*)` be a joint global maximizer. It exists: the joint box/balance domain is compact, the resistance lower bounds are positive, and the unique energy-minimizing physical flow and its normalized potentials depend continuously on nominations and resistances.

At the fixed resistance vector `beta*`, the reviewed bounded-block-rank nomination theorem supplies a nomination `b~` in its enumerated face family such that

```
F(b~,beta*)=max_b F(b,beta*)=joint_OPT.
```

The last equality follows because `(b*,beta*)` is already a joint maximizer. The entire enumerated family depends only on graph path orders and nomination interval bounds, not on resistance values. Thus `(b~,beta*)` is a joint global maximizer on one of the same faces. This immediately transfers both the one-active-block saturation and its bounded-free-coordinate refinement. It does not require a new joint perturbation argument or any resistance first-order condition.

The selected active block has at most `8r-2` free nominations. All preceding core nominations are fixed at upper bounds, all following ones at lower bounds, and the selected block's total is fixed by balance. Original nomination intervals may be shifted without changing this reasoning.

## 2. After fixing a nomination face, resistance optimization separates by block

Every selected-block face fixes all outside nominations and fixes the selected block's total nomination by balance. Consequently every inactive block has fixed effective nominations, even while the active block's individual nominations vary. Conservation and uniqueness imply that its physical flow depends only on these fixed effective nominations and its own edge resistances.

Independent resistance boxes therefore separate the total potential difference into independently optimizable block drops. The maximum on the selected face is the sum of the inactive blocks' resistance-only optimum values and the selected block's joint nomination/resistance optimum. Off-path blocks do not affect the core objective and need not be optimized.

## 3. Each local problem has a fixed nonlinear core and scalar resistance leaves

For a non-bridge active block, eliminate one free nomination using balance and add its at most `r` circulation variables. Denote this nonlinear core by `z`. Its dimension is at most `9r-3`. For an inactive block, `z` consists only of its at most `r` circulations. Bridge and zero-free-coordinate cases are handled without applying negative dimension formulas. On an inactive bridge, its fixed flow is constant and the best resistance endpoint follows the sign of `x|x|`. On an active bridge, first take the largest feasible flow, since every positive-resistance law is increasing, then take the upper resistance endpoint for nonnegative flow and the lower endpoint for negative flow.

Every physical edge flow is affine in `z`:

```
x_e(z)=c_e+d_e^T z.
```

Use a fundamental cycle basis `Z`. On a fixed sign cell of these affine edge flows, define the quadratic polynomial

```
f_e(z)=sign_e [x_e(z)]^2.
```

The local physical equations are precisely the cycle equations

```
sum_e Z_ie beta_e f_e(z)=0,   i=1,...,r_H.  (1)
```

Conservation is already built into the affine flow representation. For any fixed oriented path between the block's objective terminals, the local potential drop is

```
g(z,beta)=sum_e p_e beta_e f_e(z),           (2)
```

where `p_e` is its signed path-incidence vector.

Equations (1) and objective (2) are linear in every resistance coordinate. They fit the fixed-core/polyhedral-block theorem exactly:

- nonlinear core: `z`, of fixed dimension;
- leaf `e`: the single scalar `beta_e` in its rational interval;
- aggregate constraints: the at most `r` cycle equations;
- coefficients in the core: degree at most two;
- objective: a sum of leaf-linear terms with quadratic core coefficients.

The zero-flow hyperplanes have polynomially many cells for fixed core dimension. Intersect each cell closure with the nomination bounds and rational circulation bounds. In a fundamental cycle basis, a circulation coordinate equals a chord flow and is bounded by total possible injection. The same global injection bound applies to a block: its effective loads are sums over disjoint original vertex groups, so their total positive load cannot exceed the global bound. Hence the core set is compact and rational semialgebraic, with polynomial input size.

The [fixed-core theorem](fixed-core-block-polyhedral-optimization.md), applied to every cell and with objective sign reversed if needed, gives exact local global optimization and an algebraic local optimizer with polynomial encoding length. There are arbitrarily many resistance variables, but this does not increase the nonlinear core or aggregate dimension. The theorem's box-leaf case has constant vertex denominators, so its support-polynomial construction does not introduce an unbounded product of core-dependent denominators.

Keep each block optimizer in its own algebraic representation. Do not construct a common algebraic field across all blocks, whose degree could be exponential. Interval approximation and coordinatewise rational rounding never require merging these fields. Only the nomination coordinates of the one active block need a common local representation.

For value approximation, polynomial algebraic encoding length suffices: each local optimum can be enclosed to prescribed accuracy in polynomial bit time. Sum block intervals and take the maximum over selected blocks and nomination faces. Exact comparison of an unbounded sum of algebraic local values is not required.

## 4. Rational recovery uses a uniform joint Lipschitz estimate

Let `B=sum_v max(|l_v|,|u_v|)` on the aggregated core and fix any simple `s-t` path `P`. Define

```
C_b=2B sum_{e in P} beta_upper_e.
```

The fixed-resistance nomination estimate is uniform over the resistance box. For resistance sensitivity, differentiate the smoothed physical equations with the nomination held fixed. If `h` is the ordinary unit-source/unit-sink adjoint for `pi_s-pi_t`, then

```
partial F_rho / partial beta_e
  = j_h,e [x_e|x_e|+rho x_e],
j_h,e=(h_u-h_v)/[beta_e(2|x_e|+rho)].         (3)
```

Electrical currents for a unit source and unit sink are acyclic and have absolute value at most one. Since `|x_e|<=B`, (3) gives `|partial F_rho/partial beta_e|<=B^2+rho B`. Integrating along box segments and passing to zero smoothing yields

```
|F(b,beta)-F(c,gamma)|
  <= C_b ||b-c||_1+B^2 ||beta-gamma||_1.    (4)
```

The bound is valid on every connected graph and has rational constants of polynomial bit length. It does not rely on resistance monotonicity.

If `B=0`, every aggregate core nomination is zero, the objective is identically zero, and rational disaggregation plus arbitrary rational resistance choices gives the output directly. Otherwise use the following rounding argument.

The algebraic optimizer has only `O(r)` free nomination coordinates, but it may have polynomially many non-bound resistance coordinates. Refine all coordinate isolating intervals to precision allowing their total l1 errors in (4) to consume at most `epsilon/4`; the extra factor from the number of resistances costs only logarithmically many precision bits. Intersect the nomination isolating boxes with the original rational nomination box and exact balance equation, and solve a rational LP. Choose each resistance rationally inside its intersected rational interval. This produces rational nominations/resistances satisfying their original constraints exactly. The original algebraic circulation need not survive rounding: the rounded nomination/resistance pair has its own unique physical solution, and (4) controls its objective change.

Approximate local values finely enough to select a face/block combination within `epsilon/4` of the global optimum, recover local optimizers or sufficiently close algebraic feasible points, and use (4) for a further error below `epsilon/4`. Rational off-path nomination disaggregation and arbitrary rational off-path resistances complete a globally feasible output. A standard budget leaves total loss below `epsilon`.

## Relationship to the earlier resistance sign-pattern route

An earlier exploratory proof tried to leave only `O(r)` resistance coordinates free using resistance KKT conditions and a bounded number of physical flow-sign changes. That required nomination intervals containing zero. The fixed-core theorem eliminates the need for that step and removes the sign restriction. The [older derivative and zero-flow examples](../notes/potential-flow-joint-resistance-sign-patterns.md) remain useful checks, but they are not the structural basis of this theorem.

The simpler proof also avoids relying on unchanged adjoints after moving a zero-flow resistance to a bound. Such a move preserves the physical solution but may change the adjoint; the old note handled this by recomputing KKT data. No such move is used here.

## Evidence and literature scope

[`code/potential_flow_mpd/joint_resistance_checks.py`](../code/potential_flow_mpd/joint_resistance_checks.py) passed 48 nonlinear finite-difference checks of the resistance derivative (maximum error `7.87e-10`) and a zero-flow example showing that resistance changes can preserve the physical solution while changing its adjoint. Its 2,000 exact long-path sign tests concern the older route and are not needed for this proof. The bounded-rank topology/adjoint checks and the fixed-core theorem's independent tests supply evidence for the two main ingredients.

The bounded novelty audit compares the established uncertainty formulations of Aßmann, Liers, and Stingl (2019) and Aßmann, Liers, Stingl, and Vera (2018 preprint). The latter's Proposition 4.7 already uses affine circulation coordinates and hyperplane arrangements to bound flow-sign regions by `O(m^k)` for fixed total cycle rank `k`; this ingredient is not new. [Primary preprint](https://arxiv.org/abs/1808.10241). Aßmann's [2019 thesis](https://d-nb.info/1196351791/34), equations (3.3)–(3.4) and Chapter 5, explicitly treats the joint interval model. The present theorem bounds the nonlinear nomination dimension through block-rank structure and handles the remaining resistance coordinates as scalar polyhedral leaves. It does not make the surrounding mixed-integer network-design problem polynomial-time solvable.

## Exact local flow-capacity corollary

The separately stated [corollary](potential-flow-exact-arc-capacity.md) gives exact edge-flow extrema and exact robust arc-capacity validation. An edge's endpoints belong to one block, so off-block aggregation removes the sum of independent algebraic values. At fixed resistances, maximizing edge flow is equivalent to maximizing its endpoint potential difference; the same nomination faces therefore apply. The edge-flow objective is affine in the fixed-dimensional core, which fits the fixed-core theorem exactly. Both independent synthesis reviews accepted the exact corollary and its rational-witness refinement. Its exact guarantee concerns arc-flow capacities, without node potential bounds.

The direct fixed-core mapping has a separate checker, [`joint_core_mapping_checks.py`](../code/potential_flow_mpd/joint_core_mapping_checks.py). It constructs 40 exact rational physical states on subdivided theta/K4 blocks, verifies every scalar-leaf cycle identity exactly with fractions, solves the resistance LP at that fixed nonlinear core, and independently recovers the same physical flows and path/edge objectives. The maximum numerical recovery error was `3.24e-12`. Run with `/home/sgusev/miniconda3/envs/minlp-notes/bin/python code/potential_flow_mpd/joint_core_mapping_checks.py`.
