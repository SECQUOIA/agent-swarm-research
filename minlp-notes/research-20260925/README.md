# Research batch started 2026-09-25

This batch and its publication preparation are finished. The
[publication handoff](publication-readiness.md) identifies three candidate
packages, their exact claim boundaries, the completed reviews, and the
supporting material. The [reproduction index](publication-reproduction.md)
records commands, dependencies, formal coverage, and retained sources.
The work is ready for manuscript preparation within that scope; no paper
has been written and no publication priority is guaranteed.

Research remains paused at the user's request to finish the current ideas
without starting new ones. Unresolved extensions below are open questions,
not active tasks. Independent review means review by another research agent,
not journal peer review. No unsuccessful literature search is treated as
proof of originality.

## Three-variable quadratic cuts

[The exact counterexample](three-positive-disjoint-counterexample.md) is
nonnegative on the cube, but a rational point satisfying all 27 matrices
of the inspected disjoint-support SDP gives value `-1/40`. The same point
satisfies the earlier extended-triangle SOC strengthening. The comparison
and strict gap have independent proof, source, and exact-arithmetic checks.

The example belongs to a family of exposed extreme rays of nonnegative
cube quadratics. [The entire valid parameter family](three-positive-family-sdp.md)
has an exact lift using one PSD block of order five and six nonnegative
auxiliaries, without higher moment coordinates. This gives a selective
strengthening of the inspected relaxations. Its [priority review](three-positive-family-priority-review.md)
compares the classical exact tetrahedral lift and earlier named cuts.
The family does not establish new three-variable SDP representability,
and completeness of all its symmetry copies remains unresolved.

## Exact penalty encoding and calibration

- [Encoding obstruction](parametric-exploration.md): a bounded convex
  quadratic model with one binary variable requires least exact norm
  penalty `2^(2^n-1)`, even after optimizing its equality multiplier.
  The construction and exact dual formulas have
  [targeted Lean coverage](formal/penalty-encoding-coverage.md).
- [Upper bounds](penalty-upper-bound.md): under the stated slice Slater
  assumptions, sufficient penalties have `(N+1) 2^{O(n)}` bits. With at
  most `k` nonlinear native quadratic inequalities per slice, the bound
  improves to `N^{O(k+1)}`. The [fixed-count review](penalty-fixed-quadratic-count-review.md)
  checks degeneracy, coefficient heights and multiplier reconstruction.
  These are encoding existence results derived using established theory.
- [Calibration inapproximability](minimum-penalty-hardness.md): even with
  a native binary box, linear objective and one equality, approximating
  the smallest exact penalty within any polynomial factor is impossible
  unless P = NP. A simple conservative sufficient penalty is available.
  Generic penalty hardness is prior work; the
  [comparison](minimum-penalty-novelty.md) identifies the narrower addition.
- [Rational RHS perturbations](smoothed-penalty.md): a supplied penalty
  has polynomial encoding. With high probability, the sampled problem is
  either infeasible or exact at this coefficient. Conditional guarantees
  need the stated additional feasibility assumptions. Perturbation need
  not preserve the original optimum.

[Penalty geometry](penalty-geometry.md) supplies supporting dual formulas
and distinguishes exact dual values from multiplier attainment. The
[significance review](penalty-significance-review.md) treats the initial
penalty results as a focused contribution, not a solver-speedup theorem.

## Quantitative limits of subset moment consistency on stars

[The accuracy theorem](star-subset-accuracy-lower.md) constructs rational
indicator-quadratic stars with `I/39 < Q < 12I`, polynomial encoding,
bounded means and bounded positive hull costs. Checking exact compatibility
of every group of at most `k` leaves still leaves an additive gap at least
`1/(466560 k^2)` and a relative gap at least `1/(56920320 k^2)`.
The [independent review](star-subset-accuracy-review.md) covers both real
and rational constructions and the original-variable separating inequality.

The scheme shares only center and singleton moments across groups.
The theorem does not cover stronger overlap consistency, unrestricted
conic lifts, or optimization complexity. The
[literature assessment](tree-indicator-novelty-assessment.md) identifies
the established quantum compatibility theory underlying the construction.

## Supporting findings and limits

- [Treewidth correction](treewidth-elimination-review.md): an elimination
  lemma in two inspected preprints fails; a corrected bound and growing
  examples explain the affected proof step. In the August revision, the
  affected claim is Corollary 1; its main theorem instead assumes torso
  width directly. This is not a lower bound against every possible
  algorithm or extended formulation.
- [Continuous sparse moments](disjunctive-exploration.md) and
  [five-variable star gap](star-hull-proof-exploration.md) record exact
  counterexamples, with classical copositive antecedents.
- [Four-variable star analysis](four-star-analytic.md) gives reviewed
  sufficient conditions. The unrestricted exactness question remains open
  here; the saved numerical search is not an exactness certificate.
- [Pooling literature](pooling-hull-literature.md) identifies the proposed
  edge reduction as classical; its SOC conversion is a supporting result.
- [Integer structure](integer-structure-exploration.md) records fixed-rank
  extensions and a weak-hardness construction with close prior results.
- [Direction audit](direction-audit.md) records the initial opportunity
  assessment. Later result notes supersede preliminary conjectures.

The [root verification record](root-research-log.md) lists targeted checks
actually run and distinguishes them from other agents' checks and Lean
coverage. No project-wide verification or CI inspection was performed.
