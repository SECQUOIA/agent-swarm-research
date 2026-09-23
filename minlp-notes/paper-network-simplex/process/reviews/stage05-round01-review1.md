# Stage 5, round 1 — independent review 1

**Verdict: no major issues; accept after one minor terminology correction.**

I reviewed the complete frozen `stage05-round01` addition: Sections
`05-universality.tex`, `06-series-parallel.tex`, and
`07-fixed-state-chains.tex`, their integration, and the necessary accepted
dependencies. I independently reconstructed the new fixed-state proofs rather
than relying on author/root scripts or the older research notes. I did not
read other current-round reports, coordinate with other reviewers, or edit
manuscript sources.

## Enumerated findings

1. **S05R01-R1-F01 — minor: “coordinate plane” conflicts with its explicitly
   two-dimensional definition.**

   Location: `sections/05-universality.tex`, lines 21–24, theorem
   `thm:universality`; compare `sections/04-bounded-rank.tex`, lines 375–378.

   The prior section defines a coordinate plane as fixing every coordinate
   except **two**. The universality theorem uses that term for the subspace
   retaining an arbitrary number `p` of coordinates. The intended construction
   and proof are correct, but the defined terminology makes the statement
   inconsistent when `p != 2`.

   Replace this occurrence with “coordinate affine subspace” (or “coordinate
   section obtained by fixing ...”). No change to the mathematics is needed;
   the coefficient corollary appropriately returns to the two-dimensional case.

## Universality audit

I independently consulted the primary full text
`literature/papers/loera2006-all-linear-and-integer-programs/fulltext.md`.
Theorem 1.1 explicitly uses a coordinate-erasing bijection. Section 3.3,
printed page 816, gives the first-layer injection stated in the manuscript.
Section 3.1 preserves original coordinates in its coefficient-reduction
step. Theorem 1.2 and pages 807–808 support the manuscript's acknowledgment
of prior bitransportation/two-commodity universality.

The new transfer itself is sound. Nonnegative slack extension preserves
boundedness and the original retained coordinates. The one-row/one-column
padding forces zero cross cells and one in each new corner-layer entry,
preserving old coordinates while making all three layer totals positive.
The four-layer network's aggregate interior flows fix the two-dimensional
table margins; two observed boundary layers determine their row and column
margins, and subtraction determines the residual layer. Every nonnegative
state flow of value `D_k` on this acyclic network satisfies the uniform
scaled capacity `D_k`. Conversely, every feasible table supplies all three
state flows, including their boundary arcs. Thus the designated products are
an exact coordinate section, with no unsupported facet-projection argument.

The scaling to unit flow and unit capacities is invertible and scales the
entire free coordinate section uniformly. Applying it to `U+M V<=1`
preserves the ratio `M`. The two-dimensional section lemma therefore gives
an ambient coefficient requirement invariant under affine equations. The
input-size reasoning separates original nonlinear-model data from constants
fixing the section. The magnitude/bit-length distinction and absence of
separation-hardness claims are correct. The path/simplex-vertex argument
also correctly proves that these sparse hulls are 0/1 polytopes.

## Balanced incidence and Fibonacci audit

I rederived both sides of the balanced-incidence lemma. The observed row
totals and unobserved state capacity bounds give `K(w-a 1)>=-delta`;
positive balancing weights and fixed total profile yield the proposed
two-product inequality. In the converse, the cancellation
`-delta+tau=(-delta_r,R delta_r)` makes the displayed inverse-norm
neighborhood bound sufficient. The profile remains strictly between zero
and its state weight, the observations lie below every profile entry, and
the sole row reduction by `tau_s` is feasible. All gadget and bypass
aggregates match, including the zero residual state. Thus a full local
half-plane, not just necessary support, has been proved.

The small `N=4` matrix is invertible, has balancing weights `(2,1,1,1)`,
and yields the stated seven observations and section `2U+V>=3/32`.
The more general linear-ratio example has the correct graph/state/observation
counts. The scalar-composition counterexample is valid: each gadget can use
its own perturbed profile with the same total, while a common profile is
excluded by the positive weighted inequality.

For the Fibonacci matrix, I checked the row/column counts, recurrence-derived
kernel argument, positivity, and balancing equations. The weight sum is
`(q-1)F_{q+1}+1`; the complement preserves its positive balancing vector and
is invertible by the given rank-one argument. Using the complement makes
observations exactly the `5q-4` nonzero cells of the sparse matrix. The free
cells indeed have weights `F_q` and one. Counts, cycle rank, unit model data,
and `O(q log q)` encoding size agree with the construction. The exponential
ratio entails superpolynomial integer coefficient magnitudes but only linear
coefficient bit growth, as stated.

The simple maximum-degree-three transformation adds `N-1` connectors and
`N` subdivision vertices/arcs, giving `3N` vertices and `4N` arcs. It
preserves acyclicity and the two-terminal series-parallel construction.
Every old flow has a unique extension; new capacities are redundant for
unit acyclic source–sink flows and likewise for scaled state flows. Fixing
the new aggregate coordinates preserves the original two-product section.
The treewidth reasoning and the exclusion of claims about fixed state
count on arbitrary nested series-parallel graphs are appropriate.

## New reduced-profile and sharp-threshold audit

### Exact profile system and residual elimination

The gadget interval follows by fixing observed `a` entries, subtracting
observed `b` entries from their state profiles, and distributing the remaining
free mass. Nonnegativity of observed products is explicitly checked and is
essential for the doubly observed case. Reconstructed `b` and bypass entries
meet all state capacities and aggregate balances. Zero weights force zero
profiles and entries.

Since the residual label always lies in `U_i`, substituting
`w_0=t-sum_{j>=1}w_j` turns the upper endpoint into exactly
`1_{A_i union T_i}^T w <= t-R_i`. The remaining normals are precisely a
subset of the declared universe. Zero normals are retained as scalar tests.
Repeated-normal grouping is exact; its minimum is not a merger of distinct
state domains.

### General fixed-state theorem

Minimal positive dependences have at most `m+1` rows. Their cofactor
weights are bounded by the maximum 0/1 determinant after whole-row sign
changes. Farkas and the weighted sum-of-minima expansion prove a complete
original-coordinate description with the stated coefficient bound. The
normal and basis enumeration bounds are `2^{O(m^2)}`. A nonempty bounded
profile polyhedron, even if lower-dimensional, has a vertex with full-rank
active normals; hence finite inverse-basis recovery is complete. Greedy
filling and positive-weight normalization recover all state flows. Individual
integer determinants, affine right-hand sides, and resulting rational
numbers have polynomial encoding length despite the exponential library
cardinality.

### Two and three explicit states

The two-state five conditions are exactly interval nonemptiness and
intersection with the attainable sum interval. The explicit point selection
is feasible. I separately checked the product-occurrence argument; unit
circuit weights alone would not have been enough. Its restrictions on the
co-occurrence of normals exclude repeated same-sign product contributions.
The mandatory negative-full contribution offsets the potentially repeated
bypass coefficient in the singleton circuit.

For three states, I independently classified the circuits. Without the
negative full normal, minimality leaves one positive subset and its negative
singletons. With the negative full normal, a positive full row gives the
opposite pair; one negative singleton forces the two overlapping pairs
containing it; no negative singletons gives either a partition or the
three-pair cover with doubled negative-full weight. This yields exactly
`7+5+3+1` circuits. The only doubled weight carries no product coordinate.
The same two forbidden co-occurrence patterns prove unit product coefficients
for all row choices, not just the currently active branches.

Both bypass repairs are correct and do not create another coefficient of
magnitude two. In the singleton-partition exception, all three selected rows
are upper endpoints from distinct gadgets. A selected gadget contributes only
`-x_a`; adding its balance changes `(x_h,x_a,x_b)` from `(-2,-1,0)` to
`(-1,0,1)`. In the pair-triangle exception, all three rows are lower endpoints
from distinct gadgets. Subtracting one balance changes `(2,1,0)` to
`(1,0,-1)`. These are valid global representative changes on the retained
flow equations and preserve violation after the flow precheck. The two
numerical examples have the stated violations and satisfy their separate
McCormick bounds.

The `m=4` balanced-incidence example supplies a genuine ambient product-ratio
obstruction. Its two free products cannot be repaired by an affine equation,
unlike the shared bypass coordinate in the `m=3` proof. Thus the universal
unit-coefficient guarantee is sharp in explicit state count. Finally,
merging all wholly unobserved labels with the residual preserves exactness
and all flow/product bounds. One normalized merged flow plus the original
weights justifies the observed-label complexity and compact-output claim.

## Independent exact checks and build

I wrote `verification/reviewer1/stage05-round01/check.py` independently of
the production and author verification code. It passed:

- exact positive-circuit enumeration for `m=1,2,3`, with counts `1,5,16`;
- exact classification of the sixteen circuits into `7,5,3,1`;
- 4,336 product/local-flow occurrence checks over every gadget observation
  pattern for `m=2,3` and every circuit, allowing a zero contribution from
  rows supplied by other gadgets;
- exact arithmetic for both bypass-repair examples and their McCormick checks;
- Fibonacci balance, determinant, complement, and sparsity checks for
  `q=3,...,9`;
- 185 exact feasible witnesses for the `m=4` section and 176 grid points on
  the forbidden side of its necessary balanced inequality.

These finite checks supplement the general proofs. The product-occurrence
test does not stand in for the global bypass-repair proof, which was audited
separately above. A private snapshot copy compiled to 38 pages with no final
LaTeX warnings or overfull/underfull boxes.

## Limitations

This review did not reproduce the full transportation-universality algorithm
in code, but verified the required coordinate injection in the primary source
and checked its network transfer directly. It does not establish exhaustive
literature priority or validate later runtime experiments. No unresolved
mathematical issue was identified in this stage.
