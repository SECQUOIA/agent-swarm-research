# Stage 4 author record

Date: 2026-09-07. Author agent: `paper_author`. Status: completed, awaiting
five independent reviews.

## Written scope

Added `sections/04-bounded-rank.tex` and integrated it in `main.tex`; added
two directly relevant edge-direction references and README instructions.
Earlier section files remain byte-identical to the Stage 3 accepted snapshot.

The section fully covers the accepted bounded-rank result and its independent
review: signed TU normal grouping, positive feasibility circuits, ternary
edge directions, complete arrangement support rays with degeneracies,
optimal dual bases, the transformed cofactor multiplier bound, coefficient
accounting, and exact arithmetic/encoding complexity. It also introduces a
reusable local coordinate-section facet-ratio lemma for later constructions.

## New developments

### Constructive recovery

The root's candidate recovery extension is now proved as `thm:rank-recovery`.
The remaining state intersection is described by the fixed row list
`M union (-R)`. Bounded nonempty intersections have vertices with a full
ambient-rank active basis even when lower-dimensional. Enumerating the fixed
inverse bases therefore constructs a state coordinate without an online LP.
The suffix-support invariant proves that the process ends at the exact
aggregate. Its bound is `2^{O(r^3)}` times sparse input size, separately from
the `2^{O(r^2)}` separation bound.

The proof addresses a potential encoding gap: every inverse has an integer
adjugate and a parameter-bounded determinant. A common denominator for the
remaining aggregate is multiplied by at most one such determinant per chosen
step. Its bit length therefore grows additively with the number of states,
while state bounds and fixed inverse matrices control numerator lengths.

### Fewer observations for sharpness

The root proposed replacing the former three-explicit-state, seven-product K4
example by a two-explicit-state, five-product example. I independently
recomputed its incidence balances, aggregate, observation restrictions,
support certificate, and every witness bound. The construction is sound:
`v_01=1/4` makes the residual support face in direction `(1,1,1)` an edge.
This allows one line state to replace the two line states in the old example.

The primary example now has balances `(-5/4,-3/4,1/2,3/2)`, all capacities
one, `y1=y2=1/3`, and a local free-product half-plane `2U+V>=1/2`.
The bound is sharp with five products, without claiming five is a minimum.
The old symmetric-reference seven-product example remains as
`rem:seven-product-k4`, including its data and complete local witness checks.
Both examples are explicitly multiple-supply, multiple-demand networks.

### Facet transfer

`lem:section-facet` treats a local half-plane in an actual coordinate section.
Two-dimensional local interior forces every ambient affine-hull equation to
have zero coefficients in the two free coordinates. A finite description
must then contain an active nonconstant restriction defining that boundary.
This proves the necessary coefficient ratio and its invariance under adding
valid equations, without confusing facets of projections with ambient facets.

## Proof scrutiny

- Positive dependence supports are shown minimally linearly dependent, not
  merely minimally positive; TU then forces unit primitive multipliers.
- Every edge of every state domain, including an affine slice, has `r-1`
  independent tight rows. No full-dimensionality assumption is introduced.
- Coordinate directions make every arrangement chamber pointed. Its support
  functions are linear throughout its closure, so extreme rays suffice.
- The dual optimum can be reduced to independent support by a zero-objective
  perturbation argument, then extended to a full basis with zero multipliers.
- The multiplier bound uses primitivity under a unimodular transformation;
  a direct norm bound on `B^{-T}h` would be weaker and is not substituted.
- A basis excludes opposite row normals, so products do not accumulate
  repeated coefficients in a support branch. Local circuit cancellation is
  addressed separately.
- Row scaling remains rational in simplex coefficients; no primitive-integer
  normalization claim is made.
- Both sharpness constructions verify every state arc bound and aggregate
  identity. The five-product example's residual `01` deviation lies in
  `(3/16,11/48)`, within its asymmetric interval `[-1/12,1/4]`.

## Literature

Read the full canonical bounded-rank note and its complete independent review,
including the sharpness follow-up. The existing Gritzmann–Sturmfels and
Onn–Rothblum citations cover the established support/zonotope mechanism.

Added Onn–Rozenblit (2014), *Convex Integer Optimization by Constantly Many
Linear Counterparts*, Linear Algebra and its Applications 447, 88–109;
verified the primary arXiv 1208.5639 record and its journal reference.
Added Onn–Rothblum–Tangir (2005), *Edge-Directions of Standard Polyhedra with
Applications to Network Flows*, Journal of Global Optimization 33, 109–122,
DOI `10.1007/s10898-004-4313-z`; verified the publisher's primary metadata
and scope. The DOI suffix is 2004, but the publication year is 2005.

The manuscript credits the classical ingredients and distinguishes the
Khademnia–Davarnia projection-cone multiplier-two example from a necessary
ratio on actual free product coordinates. No generic polynomial-separation
novelty or computational superiority is claimed.

## Verification executed

Existing author library check, rerun from the repository root:

```sh
python code/network-simplex-bounded-rank-verify.py
```

Passed 160 formula/numerical-LP classifications, 218 exact primal-vertex versus
dual-support comparisons, and the prior 81-point K4 grid with 43 exact
decompositions. Output: `verification/stage04-existing-library.json`.

Existing independent verifier, rerun:

```sh
python code/network_simplex_review/bounded_rank.py
```

Passed exact TU/ternary/multiplier checks at ranks 3 and 4; 6,120 numerical
support-LP comparisons; 180 numerical sum-membership comparisons; and the
prior K4 225-point raw-state-LP grid with 116 exact witnesses and 109 exact
negative support certificates. Output: `verification/stage04-existing-review.txt`.
The numerical comparisons remain labeled numerical.

New author check, from the manuscript directory:

```sh
python verification/stage04-recovery.py
```

It reuses the existing exact support-library builder but implements the new
inverse-basis recovery itself. It calls no LP. All 64 instances and 334 state
vectors passed exact original state bounds and aggregate identities.
Families are a cycle, theta, K4, and a rank-four box normal system. The last
is an algebraic rank-four test, not asserted to be a single cyclic graph
block. Tests include every slice dimension, zero weights, points, random
observations, and 25-state sequences. K4 has 18 recovery normals, 544
nonsingular inverse bases, and determinant magnitudes up to four.

The same script independently checks the new five-product K4 on a 225-point
grid: 116 exact original-flow witnesses and 109 exact negative support
certificates passed. These use a different grid from the root's independent
289-point full-state-LP check. Root evidence is retained separately as
`verification/stage04-root-k4-five.py/.json`.

The final full manuscript compiles cleanly to 27 pages with `latexmk -pdf
-interaction=nonstopmode -halt-on-error main.tex`. Build output and source
hashes appear in `verification/stage04-build.txt` and
`verification/stage04-validation.json`.

## Unresolved issues

No mathematical gap remains identified within the stated bounds. The recovery
factor is deliberately larger than the separation factor. Sharp coefficient
constants above rank three, minimum observation count for a ratio-two example,
and practical superiority of these finite libraries are not claimed.
Independent five-reviewer assessment is still required for the new and
rewritten statements before stage acceptance.
