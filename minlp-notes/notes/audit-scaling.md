# Independent agent audit of scaling disjunction results

Date: 2026-09-04. This is an independent agent review of the preexisting result,
not external peer review. The corrected results are in
[`results/scaling-disjunctions-hull.md`](../results/scaling-disjunctions-hull.md).
A separate agent reviewed the replacement Theorems 4A and 4B in
[`notes/review-scaling-characterization.md`](review-scaling-characterization.md).

## Main correction

The original Theorem 4, which asserted independent convexification of count-only costs
and the shared-intensive feasible set, was false. Convexification may require a scale
mixture correlated with the intensive operating condition. An independently optimized
scale-cost envelope can use a different mixture and understate the cost.

A complete example uses the convex per-unit line `E={(ξ,T):ξ=T∈[0,1]}`, scales
`Λ={0,1,2}`, and costs `(f(0),f(1),f(2))=(1,0,1)`. The point `(λ,X,T)=(1,1,1/2)`
is in the base hull. Its true convexified scale cost is 1; the separately convexified
cost is 0. The proof in the result uses the exposed equality `X=2T` to show that the
only possible scale distribution has equal weight on 0 and 2. Multiplying the cost
by any positive number gives an arbitrarily large absolute error.

An independent obstruction occurs even with no intensive coordinate and a singleton
scale catalogue: `E={-1,1}`, `Λ={1}`, `g(λ,X)=|X|`. The lifted convexified cost at
`X=0` is 1, whereas evaluating the original convex cost at the convexified point gives 0.
Thus a nonconvex per-unit domain requires cost lifting before convexification. The
original example of joint convexity was also too broad: `λc(X/λ,T)` is not generally
jointly convex when `c` is convex, as `c=T²` shows.

## Replacement results and useful follow-up

Theorem 4A gives the correct extensive-only formula. For compact `E`, continuous
per-unit cost `c`, and finite nonnegative scales, first let `h` be the lower boundary of
`conv{(ξ,c(ξ)):ξ∈E}`. Then the exact convexified cost is
`λh(X/λ)+f̌(λ)` at positive scales, with the specified zero-scale slice. Size-biased
weights prove the lower bound; a product distribution over scale and per-unit atoms
attains it. The result covers nonconvex unit domains and additive multiplicity costs.
It is an elementary perspective result with no novelty claim.

Theorem 4B gives a sharper limitation. For a finite catalogue containing `0<s<M`,
**all scale-only costs separate if and only if `conv E` is the Cartesian product of
its extensive and intensive projections**. It suffices to test the single cost that
is zero at `s` and one at every other catalogue scale. Zero cost forces the base hull's
slice at `s` to coincide with the convexified original slice. Mixing the endpoint
slices then makes each intensive fibre invariant under contraction toward any point
in the intensive projection. Iterating and taking the limit proves rectangularity.
The separate review agent checked both directions and all boundary assumptions.

This identifies a structural obstruction rather than merely one failed example.
It can guide modelers deciding whether a count-cost epigraph may be relaxed separately.
The equivalence is a candidate observation; targeted searches did not find the exact
statement, but no publishable novelty is established. Arbitrary additional operating
costs are outside Theorem 4B. Affine scale costs always separate even for nonrectangular
models, and a catalogue with no interior scale is outside the necessity claim.

## Remaining original statements

- Theorems 1 and 2 are correct for nonempty compact sets. The proof of Theorem 1 now
  handles a singleton catalogue explicitly. Multiplicity `N=0` is separated from formulas
  involving division by `N`. Enlarging the off-state intensive domain requires replacing
  the corresponding block in the formulas.
- Theorem 3 is correct. Its zero-weight conic behavior now has an explicit proof:
  a homogeneous feasible direction projects to a recession direction of the compact
  represented set, so its original-variable component is zero. This also works for
  an unbounded auxiliary-variable lift when the projected set is compact.
- The bilinear corollary is correct for its reported parameters. The displayed global
  box requires nonnegative per-unit lower load; this is now an explicit assumption.
- Theorem 5 is correct. Its proof decomposes the count vector into integral vertices
  while keeping each type's per-unit convex point fixed. It needs an integral count
  polytope, not the integer-decomposition property. Totally unimodular matrices require
  integral right-hand sides for the stated integrality conclusion.
- Theorem 6's distance bound is classical and correct. The objective gap needs its
  Lipschitz constant. A relative `O(d/n)` bound additionally requires positive linear
  objective normalization. Extra aggregate constraints may invalidate rounded points;
  the distance bound alone gives no constrained objective guarantee. These qualifications
  replace the original unconditional relative-gap language.
- Local hull identities do not imply exactness after intersecting with process balances,
  nor do they justify removing intermediate scales from the original feasible model.

## Computational verification

Running `python code/scaling_disjunctions/bilinear_multiplicity_hull.py` reproduced nine
unique facets for the six-point hull, zero violations among 20,000 sampled feasible
points, and 13,499 of 100,000 sampled naive-relaxation points cut off. Sampling checks
support but do not replace the hull proof.

A separate six-variable LP over the endpoints of the three scale slices verified the
cost counterexample exactly to solver tolerance: minimum cost 1 and weights 1/2 at
`(0,0,0)` and `(2,2,1)`. An additional 100 LP comparisons checked Theorem 4A with
`E={-1,2}`, per-unit costs `{3,-2}`, `Λ={0,1,3}`, and scale costs `{1,-3,1}`. Using random
seed 481, the maximum discrepancy between the full lifted hull LP and the factorized
formula was `1.78e-15`. These computations were ephemeral checks; the mathematical
proofs are recorded in the result file.

## Literature checks and limits

The existing repository literature instructions were read. No literature package or
generated index was edited by this audit.

- The primary text of [Wu et al., Variable Aggregation-based Perspective Reformulation
  for Mixed-Integer Convex Optimization with Symmetry](https://arxiv.org/html/2602.04123v1#S4)
  was checked in Section 4.1. Lemma 3 states the Minkowski-sum convexification identity.
  Theorem 3 identifies the aggregated formulation's hull under its stated assumption.
  These are direct prior results for the extensive aggregation mechanism; they make
  a broad novelty claim for the elementary aggregation identities inappropriate.
- [Balas, Disjunctive Programming](https://onlinelibrary.wiley.com/doi/abs/10.1002/9780470400531.eorms0262)
  describes the established extended-formulation principle for unions of polyhedra.
  Theorem 3 in the local result is a two-slice specialization.
- The publisher record for [Jach, Michaels, and Weismantel, The Convex Envelope of
  (n–1)-Convex Functions](https://epubs.siam.org/doi/10.1137/07069359X) confirms related
  convex-envelope work. No assertion that its full theorem contains the exact set-valued
  scaling statement is based on its abstract. The old wording equating the mechanisms
  was weakened accordingly.
- Searches for combinations of scale costs, convex hulls, rectangularity, Cartesian
  products, perspectives, and shared intensive variables did not identify the exact
  Theorem 4B criterion. This limited negative search is not evidence that the result is
  absent from all literature. General disjunctive/perspective theory remains the most
  plausible prior-art route to investigate before claiming novelty.
