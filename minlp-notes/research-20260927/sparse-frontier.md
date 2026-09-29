# Sparse quadratic frontier: budgeted low-rank gain

Date: 2026-09-27. This is a direction assessment and a map to the detailed
result. It does not establish priority.

## Current outcome

The useful result from this exploration is a deterministic approximation
scheme for **budgeted quadratic gain** with a supplied positive low-rank
update:

\[
 Q=D+UU^T,\qquad
 \max_{S:\,\sum_{i\in S}c_i\le C} b_S^TQ_{SS}^{-1}b_S,
\]

where `D` is positive rational diagonal, `U` has a fixed number of columns,
`b` is arbitrary rational, and costs and budget are nonnegative rationals.
The candidate construction preserves the budget exactly and obtains a
`1-epsilon` fraction of optimal gain in time polynomial in input bit length
and `1/epsilon`, with an exponent depending on the coupling rank. There is
no numerical condition-number assumption. Cardinality restrictions can be
recorded separately. The supplied factorization is part of the input.

The [detailed note](positive-update-spectral-approximation.md) contains the
proof, related penalized and ridge formulations, assumptions, and limitations.
The [adversarial review](sparse-psd-review.md) and
[literature audit](sparse-psd-prior.md) are separate records.

The main matrix mechanism was already developed in the repository's
[September 12 PSD path approximation theorem](../notes/research-20260912-dag-psd-approximation-set.md).
It constructs a two-sided relative Loewner approximation set without an
eigenvalue lower bound. Replacing an arbitrary representative at each
rounded dynamic-programming state by the representative with minimum exact
additive cost preserves this matrix guarantee and a single exact budget.
The gain is a Schur complement of an `(r+1)`-dimensional PSD sum. This is an
application and modest extension of that earlier theory, not a new discovery
of its normalization argument. In particular, this exploration has not yet
produced a substantially new general matrix approximation principle.

The budget is binary encoded and need not be expanded into a state-space
coordinate. This distinction matters: the original PSD path note explicitly
requires a polynomial-size DAG, while a budget-expanded DAG can be
pseudopolynomial. The exact-cost representative rule itself has established
one-exact Pareto antecedents, identified in the literature audit.

## Why this is more useful than the first additive formulation

For a penalized indicator objective, fixed-support minimization gives
`c(S)-g(S)`. The same construction gives error at most
`epsilon*g(S*)`, and hence at most `epsilon*sum_i b_i^2/d_i`. This is only
an additive guarantee, since positive costs can nearly cancel the gain.
Under a budget, maximizing the nonnegative gain has a genuine relative
approximation guarantee. It therefore addresses a familiar subset-selection
criterion without relaxing the resource constraint.

Das and Kempe's 2008 work already gives approximation schemes for regression
subset selection under structural assumptions on a covariance graph. Its
bandwidth guarantee includes a condition-number assumption. A dense
`D+UU^T` matrix need not have bounded bandwidth, and the present guarantee
allows arbitrary numerical conditioning. These are different tractable
classes, rather than a claim that either dominates the other in general.
See their [primary manuscript](https://david-kempe.com/publications/regression.pdf).

The polynomial exponent is large. No implementation speedup, favorable
empirical performance, or feasibility for high factor rank has been shown.
A practical algorithm would need much more efficient state compression or
problem-specific structure. A complete external novelty assessment remains
necessary before treating the consequence as a publishable advance.

## Directions screened out

1. **Negative low-rank update.** The apparently promising exact algorithm
   for `Q=D-UU^T` was already documented in the
   [September 25 low-dimensional-coupling note](../research-20260925/integer-structure-exploration.md),
   including oracle matroid constraints and comparisons with Gao--Li and
   Del Pia--Dey--Weismantel. Repeating it would not advance the frontier.
2. **Arbitrary linear signs for Stieltjes matrices.** This is already
   addressed by Gómez and Han,
   [*Convex Submodular Minimization with Indicator Variables*, arXiv:2209.13161v2](https://arxiv.org/html/2209.13161v2),
   Theorem 2 and Section 4.2. Their lattice lift permits arbitrary linear
   signs and activation bounds. The same-sign qualifications in the earlier
   Stieltjes convex-hull literature must not be mistaken for a current
   optimization-complexity barrier. This does not remove the separate
   universal convex-hull obstructions in the local sparse quadratic paper.
3. **Naive random ambiguity components.** Fixing an indicator active does
   not remove its continuous variable. Consequently, disconnected ambiguous
   vertices in the induced ambiguity graph need not be independent. For a
   star with an always-active center, eliminating that center changes the
   leaf quadratic to `D-ww^T/a`. Every pair of leaves becomes coupled when
   its two center-edge weights are nonzero. Thus a percolation argument
   using only the induced graph of undecided indicators is invalid. No
   general smoothed polynomial algorithm for unbounded-treewidth sparse
   matrices was established by this exploration.

## Verification and attribution limits

The important algebra is exact: the Schur-complement identity, the
cost-preserving dynamic-programming argument, and the Loewner-order transfer.
The independent review records finite rational checks and their limits.
Those checks exercise actual state collisions and large coefficient scales;
they do not prove asymptotic bit complexity, establish novelty, or measure
solver performance. No project-wide verification or CI inspection was run.
A targeted inline `python3` check of this note, the detailed result, the
source audit, and the independent review passed all relative-link,
math-delimiter, and trailing-whitespace checks. This is document hygiene
only.

This file records the assessment rather than adding a new independent
mathematical claim beyond the linked note. The immediate next question is
whether the budgeted low-rank consequence and its certified-surrogate
extension warrant a focused theorem after comparison with the strongest
subset-selection and experimental-design literature. The broader search
for a more substantial contribution should continue.
