# Stage 3, round 1 — independent review 1

**Verdict: accept this stage. No major or minor defects found.**

Scope: the frozen `stage03-round01` manuscript, especially all of
`sections/03-structured-oracles.tex`, the new bibliography entries, and the
integration input. I independently rederived the main formulas and checked
their dependence on the accepted block theorem. I did not consult the other
current-round reports, coordinate judgments, or edit manuscript sources.

## Enumerated findings

1. **S03R01-R1-F00 — no actionable finding.** The claimed exact hulls,
   separation certificates, and compact recovery procedures are sound under
   the stated graph and arithmetic conventions.

## Proof audit

**Theta coordinates and state supports (lines 11–90).** The third-path sign
change correctly converts deviations `(s,t,-s-t)` into the coordinate forms
`s,t,h=s+t`. The tightened lower and upper endpoints enforce all observations,
including repeated observations with opposing arc orientations. At zero
weight, their base intervals force zero. The nonemptiness conditions exactly
test intersection of the attainable rectangle-sum interval with the prescribed
sum interval. Projecting that intersection onto either coordinate gives the
stated tight lower and upper supports, including their attainment. No
full-dimensionality assumption is needed.

**Minkowski sufficiency (lines 92–128).** I checked the dimension cases
separately. A nontrivial one-dimensional summand must be parallel to a boundary
line of one of the six defining inequalities. Every exposed edge of a
two-dimensional sum is a sum of maximizing faces in the same normal direction;
these faces can only be points or segments parallel to that edge. At least
one is nontrivial, so its direction already occurs in a summand. Therefore the
six normals include every required edge normal. If the whole sum is a segment,
all nonpoint summands are parallel, the perpendicular pair of supports fixes
the line, and a varying coordinate form fixes both endpoints. Points and the
empty sum are likewise correctly represented. The proof does not silently
apply a two-dimensional polygon argument to a segment.

**Original-coordinate linearization and separation (lines 137–205).** The
lower endpoints/supports are maxima of affine functions, and the upper ones
are minima. Every displayed condition therefore has the required convex
piecewise-affine form. Its active affine branch is globally valid, not merely
a tangent approximation to a nonconvex condition. I checked the product-index
counting in each type of local comparison and support formula: products from
different coordinate types and labels are distinct, and repeated selections
in same-type comparisons cancel. Representative flow coordinates are distinct
as well, so the unit coefficient statement is justified. The normalization
qualification is retained.

**Exact compact recovery (lines 207–255).** Suffix support sums describe the
entire remaining Minkowski sum by the preceding lemma. Reflecting and
translating it gives exactly the intersection intervals in the proof. The
stated point choice respects every bound: the chosen `s` is its tight lower
endpoint; `t=max(ell_t,ell_h-s)` is within its interval and makes the sum either
`ell_h` or `s+ell_t<=u_h`. Subtraction maintains the recovery invariant. The
same argument covers empty suffixes, singletons and segments. Divisions occur
only once positive weights have been identified; zero-weight defaults are
unused. One default coordinate vector per block and observed-label exceptions
indeed encode all global state flows without writing a dense state-by-arc
array. The arithmetic bound and the separate dense-output cost are consistent.

**Joint restriction example (lines 257–276).** The separate one-label
decompositions satisfy the scaled capacities and sum to the stated aggregate.
Jointly, the third-arc demand is excessive. The displayed inequality is the
residual state's valid first-two-arc upper bound, and its violation is exactly
`1/3`.

**General parallel-path theorem (lines 278–394).** I independently followed
both implications of the transportation reduction. The lower-endpoint shift
gives the displayed row targets, column targets and capacities. Complementary
subsets enforce nonnegative row targets; local conditions enforce nonnegative
column targets and capacities. The total targets agree because aggregate
deviations sum to zero. For fixed source-side row set, minimizing each column
side independently gives precisely the displayed minimum-cut formula. Adding
the selected lower endpoints converts the cut condition into the claimed
subset inequality without a missing sign or term. This proves sufficiency,
including zero total target. The branch-expansion coefficient argument and
the reduction to the six theta supports at `k=3` are correct.

**Flow separation and recovery (lines 396–457).** A negative shifted row
target yields a valid lower-bound cut. A deficient maximum flow yields a
violated subset after minimization over column sides. An active affine
majorant of the concave right side is globally valid and agrees at the
candidate, so the emitted linear cut separates strictly. The network has the
stated number of nodes and arcs. Shortest augmenting paths give a polynomial
algorithm independent of capacity magnitudes; clearing rational denominators
has polynomial encoding cost. Normalization of returned columns obeys the
same zero-weight and compact-output safeguards as the theta construction.
The scope is correctly restricted to actual parallel-path blocks rather than
all series-parallel networks.

## Independent exact checks

I wrote `verification/reviewer1/stage03-round01/check.py` without using the
repository separator implementation. It computes exact polygon vertices by
pairwise boundary-line intersection and exact convex hulls by orientation
tests. This supplies a second route to the support and Minkowski assertions.
The checks covered:

- all 216 ordered-interval patterns with endpoints in `{-1,0,1}`, checking
  nonemptiness, tight supports, and the point-choice formula;
- 41 distinct nonempty domains, including full-dimensional polygons, segments,
  and points;
- all 1,681 ordered pairs of these domains, comparing the actual convex hull
  of all vertex sums to the summed-six-support polygon;
- 8,360 exact recovery checks, at every resulting sum vertex and its rational
  centroid.

All checks passed. Results are recorded in `check-output.json`. The finite
checks supplement, rather than replace, the proof audit and do not establish
the general transportation theorem by experiment.

## Build, attribution, and limitations

A private snapshot copy compiled to 20 pages with the documented `latexmk`
command. The final log contains no LaTeX warnings or overfull/underfull boxes.
The added section uses the accepted definitions consistently.

I consulted the repository primary text of Kis–Horváth Section 5.7, whose
union-of-bounded-simplex network construction supports its identification as
a predecessor. The stage explicitly credits classical Minkowski support
geometry and transportation feasibility and does not claim that generic
polynomial separation is new. I did not independently audit every field in
the new classical bibliography entries or perform an exhaustive novelty
search. No experimental performance claims occur in this stage.
