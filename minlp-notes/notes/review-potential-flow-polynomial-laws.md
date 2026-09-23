# Independent review of fixed-degree potential-flow laws

Date: 2026-09-05. Reviewer: independent `spatial_sdp_review` agent.
Reviewed: `notes/potential-flow-polynomial-laws-investigation.md`, against
the existing bounded-block-rank, joint-resistance, exact arc-capacity,
and fixed-core/polyhedral-block results.

**Verdict: PASS under the stated C1, strict-monotonicity, zero-at-zero,
finite-piece, and fixed-degree assumptions.** The new analytic and
algebraic steps correctly extend the reviewed quadratic arguments.
No substantive gap was found. The examples need the minor qualification
that even signed integer powers require two pieces and hence `p>=2`;
the author was notified. This review does not make a novelty claim.

## Existence, coercivity, and continuity

On either unbounded outer interval, strict increase excludes a constant
polynomial piece. A nonconstant real polynomial that is increasing on
that outer interval diverges to the appropriate signed infinity. Thus
`f_e(x)` tends to positive infinity as `x` tends to positive infinity,
and to negative infinity in the opposite direction.

The primitive `H_e(x)=integral_0^x f_e(s) ds` is strictly convex because
its derivative is strictly increasing. It grows superlinearly in both
directions. Since `f_e(0)=0`, it is also nonnegative. Positive resistance
weights preserve strict convexity and coercivity of their sum. Every
balanced nomination has a nonempty affine conservation space on a
connected graph, for example by tree routing. The energy therefore
attains a unique minimizer there. Stationarity says that its gradient
belongs to the incidence transpose range, which gives precisely the
potential laws, with potentials unique up to one additive constant.

The physical positive-flow orientation is acyclic: every positive
flow follows a strictly decreasing potential because `f_e(0)=0` and
strict increase make the law sign equal to the flow sign. A finite
acyclic flow decomposes into source-to-sink paths. Hence every edge
flow magnitude is at most total positive injection, which is bounded
by the stated rational `B`, independently of resistance choices.

These bounds also apply to the smoothed laws. They give compactness
of flows and bounded normalized potentials uniformly over the compact
nomination/resistance uncertainty set and `rho` in a bounded interval.
For any convergent sequence of inputs and smoothing parameters, a
convergent subsequence of physical states satisfies the limiting laws
and conservation. Uniqueness identifies that limit. This proves
continuity in inputs and uniform convergence as `rho` tends to zero;
no uniform lower bound on the unsmoothed derivatives is required.

## Structural face arguments

A differentiable increasing function has nonnegative derivative at
every point. Therefore adding `rho x`, with `rho>0`, gives positive
electrical derivative resistance

```
R_e=beta_e(f'_e(x_e)+rho).
```

The smooth implicit system is locally invertible after one potential
reference is fixed, because the corresponding reduced weighted
Laplacian is positive definite. C1 laws are sufficient for this step;
second derivatives of the laws are not needed.

The reviewed maximum-principle and one-active-block arguments use this
positive electrical network and conservation, rather than the special
formula for a quadratic derivative. Their graph/interval face family
therefore stays valid. Likewise, the perturbed objective adds exactly
`delta` of adjoint source at every internal vertex of a maximal
degree-two path. The current increment remains `j_i-j_(i-1)=delta`,
so the same unimodal nomination patterns bound the number of free
coordinates by `O(r)`.

All normalized physical potentials are uniformly bounded. Consequently
the finite potential-sum objective perturbation vanishes uniformly as
`delta` tends to zero. Compactness, uniform smoothing convergence, and
selection of a subsequence lying in one of finitely many closed faces
justify the simultaneous limiting argument. The algorithm never needs
to select a numerical smoothing or perturbation scale.

For a joint optimum, holding its resistance vector fixed and applying
the fixed-resistance face theorem is valid. The face family depends
only on graph order and interval bounds, so it also contains a joint
optimizer. No resistance monotonicity or new joint KKT assumption is
being used.

## Fixed-dimensional algebraic representation

On a selected face, free nominations and fundamental circulations form
the same fixed-dimensional core as in the reviewed theorem. All edge
flows remain affine functions of that core by conservation alone.
Every rational constitutive breakpoint therefore gives an affine
hyperplane. There are at most `pm` such hyperplanes, with polynomial
coefficient encoding length. Their cells and lower-dimensional faces
are polynomially enumerable for fixed core dimension.

On each cell the constitutive expressions have degree at most `d`.
Adjacent polynomial formulas agree at their shared boundaries because
the law is continuous, so using closed cells introduces no false
physical states. Cycle equations and path-drop objectives are linear
in scalar resistance leaves, with fixed-degree polynomial core
coefficients. Resistance boxes are compact rational polyhedral leaves.
The number of cycle-linking equations is bounded by `r`. This is
exactly the required fixed-core/polyhedral-block format.

Nomination variables are bounded by their rational face bounds.
Fundamental circulation coordinates can be chosen as the non-tree
edge flows, so the physical bound `B` supplies finite rational core
bounds. All coefficients, bounds, and piece descriptions retain
polynomial bit length for fixed `r,d,p`. Thus the existing exact local
algebraic optimization theorem applies without introducing an
additional variable per constitutive piece or per edge law.

Inactive blocks have only their bounded number of circulation core
variables, together with resistance leaves. Their separately optimized
potential drops can be approximated and summed as rational intervals.
No common field across an unbounded number of independently algebraic
block values is required. This preserves the additive pressure
guarantee without asserting exact arbitrary pressure-span comparison.

## Exact edge-flow extrema, including nonodd laws

An objective edge's endpoints lie in the same block. The reviewed
aggregation therefore reduces its extremum to one block. At fixed
positive resistance,

```
x_e=f_e^(-1)((pi_u-pi_v)/beta_e)
```

is strictly increasing in its endpoint potential difference, because
the law is strictly increasing and onto. Its maximizing nominations
therefore coincide with those for the endpoint-potential objective.
This transfers an exact joint edge-flow optimum to the same bounded
nomination face family by holding the resistance vector fixed.

For a minimum, the reversed potential objective works even when the
law is not odd: `-f_e^(-1)(-D/beta_e)` is strictly increasing in
`D=pi_v-pi_u`. Oddness is not an implicit requirement.

On the fixed-dimensional core, the edge-flow objective is affine.
Exact local optimization and algebraic comparison over polynomially
many faces/cells therefore give exact signed extrema with polynomial
encoding length. There is no multi-block sum of optimal algebraic
values in this objective. Comparing these extrema with rational
capacities is the claimed exact robust decision. It correctly ranges
over the full uncertainty set, before any capacities are imposed.

## Explicit sensitivity bounds and rational recovery

The stated coefficient sums bound both `|f_e|` and `|f'_e|` on
`[-B,B]`; taking maxima over all pieces is conservative and valid.
Using `T=max(1,B)` handles powers and constant terms uniformly. Their
rational encoding lengths remain polynomial. A simple path sum of
the drop bounds gives the claimed finite potential bound.

For the ordinary unit-source/unit-sink adjoint, electrical potentials
lie between their source and sink values. Its effective resistance is
at most the sum of edge resistances along any specified terminal
path, by comparison with a unit path flow. Consequently nomination
sensitivity is bounded by

```
sum_{e in P} beta_upper_e(M_e+rho).
```

Integrating on a balanced nomination segment and letting `rho` tend
to zero gives exactly the candidate's `C_b` coefficient. This uses
the ordinary adjoint, rather than the separately perturbed adjoint
with many positive sources.

Differentiating the smoothed potential laws at fixed nominations
gives the resistance derivative

```
partial F_rho/partial beta_e
=j_h,e [f_e(x_e)+rho x_e].
```

The sign is positive with the stated orientation. The unit electrical
current is acyclic and decomposes into unit-total source-to-sink paths,
so `|j_h,e|<=1`. Therefore this derivative is bounded in absolute
value by `N_e+rho B`. Integration along the resistance-box segment and
the zero-smoothing limit prove inequality (1). Combining nomination
and resistance segments keeps every intermediate input admissible.

Refining local algebraic optimizer coordinates requires only
polynomially many precision bits: coefficient magnitudes and the
number of rounded coordinates have polynomial logarithmic size.
The rational nomination isolating box intersected with the original
box and exact balance equation is a nonempty rational polytope, so
rational LP returns an exactly balanced nearby nomination. Resistance
coordinates can be rounded independently within their intervals.
The unique physical state after rounding need not have the old
circulations; inequality (1) controls its pressure objective directly.
Off-path aggregation/disaggregation remains the reviewed exact
interval-sum operation.

## Supplementary checks and scope

Independent finite-difference checks used nonodd C1 piecewise cubics

```
f_e(x)=a_e x+b_e x^3+c_e max(x-1,0)^3,
```

with positive cubic coefficients, nonnegative linear coefficients
including zeros, and positive resistance values on a rank-two block.
For 12 physical states, five resistance directions and one balanced
nomination direction were checked against the smoothed electrical
adjoint formulas. All 72 comparisons passed; the maximum error was
`1.28e-10`. The checked unit adjoint currents also satisfied their
absolute-one bound. These checks support the changed constitutive-law
calculus, not the complete symbolic optimization algorithm.

The C1 condition must remain explicit: adding a positive linear term
does not remove a derivative jump. Arbitrary fractional-power laws
are not represented by this fixed-degree polynomial-cell argument.
No extra capacities or potential restrictions may be silently
included in the extremum subproblems. Finally, signed even integer
powers use two polynomial pieces; the displayed class includes them
when `p>=2`. These qualifications preserve the theorem's stated scope.

## Additional audit: degree and piece count may be input parameters

At the author's and parent's subsequent request, the stronger statement
was also checked: **only the maximum block cycle rank must be fixed**,
provided every univariate polynomial piece is densely encoded and the
finite list of pieces and rational breakpoints is explicit. This
strengthening passes. Let `D` be the maximum piece degree and `P_law`
the total number of pieces. Both are bounded by the dense input size.

The analytic and nomination-face arguments above do not use fixed
degree or fixed piece count. The breakpoint arrangement contains
`O(P_law)` affine hyperplanes in a dimension depending only on block
rank. Its cells and faces therefore remain polynomial in the input.
If the core dimension is `k`, expanding a degree-`D` univariate
polynomial after affine substitution produces at most
`C(D+k,k)=O(D^k)` monomials. Coefficient bit lengths grow polynomially
with the dense input, including the multinomial coefficients and
powers of the rational affine coefficients.

For these particular scalar resistance-box leaves, the support
construction is especially direct. With aggregate dimension `h`
fixed by the block cycle rank, put `W_e(z)` for the vector of cycle
and objective coefficients multiplying `beta_e`. The support of
the segment `W_e(z)[beta_lower_e,beta_upper_e]` selects an endpoint
according to the sign of

```
lambda^T W_e(z).
```

This is a polynomial of degree at most `D+1` in a fixed number of
core and support-direction variables. No core-dependent denominators
occur. Enumerating the realizable sign conditions selects all leaf
support endpoints simultaneously, and their support values sum to
polynomials with polynomial encoding length. The resulting feasibility
and optimality formulas have a fixed total number of variables.

The quantifier-elimination and algebraic-sampling bounds are polynomial
in polynomial count, degree, and coefficient bit length when total
dimension is fixed. Their degree dependence need not be treated as
a fixed constant. This was checked directly in
[Basu's survey, Theorem 2.18 and Theorem 3.6 with its sampling consequence](https://www.math.purdue.edu/~sbasu/raag_survey2011_final.pdf).
Section 2.5 of that source also states its dense representation
convention. Thus exact local values, a common local algebraic sample,
and the subsequent algebraic LP recovery retain polynomial encoding
and bit complexity with variable `D`.

The rational bounds `N_e,M_e` remain usable: their bit sizes grow by
at most polynomial terms involving `D log(max(1,B))`, coefficient
bits, and the explicitly listed number of pieces. Therefore the
pressure accuracy and rational-recovery budgets remain polynomial
in input size and requested precision bits. The multi-block sum
qualification is unchanged.

This is not a guarantee for sparse polynomials with binary-encoded
large exponents. There, `D` can be exponential in the input length;
the expansion, real-algebraic calls, and displayed numerical bounds
would not have the claimed dense-input polynomial complexity.

## Checking the law assumptions in the dense representation

The analytic assumptions may be retained as promises, but they are
also polynomial-time checkable in this representation. First verify
the explicit interval ordering and exact agreement of adjacent
polynomial values and derivatives at every rational breakpoint.
Evaluate the applicable piece at zero to check `f_e(0)=0`.

On each nonempty piece interval, univariate real-algebraic sign
determination checks that its derivative is nonnegative throughout
the interval, including unbounded outer intervals. Also require
that the derivative polynomial is not identically zero on any
nonempty piece. A nonzero polynomial has only finitely many roots,
so a nonnegative such derivative integrates to a strictly positive
increment over every nontrivial subinterval. Combined with boundary
continuity, these tests imply strict increase on the whole line.
Conversely a C1 strictly increasing piecewise polynomial passes
these tests. Empty or repeated-breakpoint pieces should be removed
or rejected before this check; they need no special law extension.

All tests use rational evaluation or fixed-dimensional, in fact
univariate, polynomial sign queries. Their bit complexity is
polynomial in the dense coefficients and explicit piece list.
