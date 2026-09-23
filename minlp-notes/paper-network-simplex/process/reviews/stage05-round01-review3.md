# Stage 5, round 1 — independent review 3

Reviewed frozen snapshot `process/snapshots/stage05-round01`, including all
three new sections 05–07 and their disaggregation, block-merger, and
coordinate-section dependencies. No other current-round review was consulted;
no manuscript edits, subagents, or coordinated checks were used.

## Verdict and enumerated findings

**No major issues. Accept after one minor terminology correction.** In
particular, the new few-observed-label results, the three-label coefficient
repairs, and sharpness at four labels pass independent mathematical scrutiny.

1. **S05-R1-R3-01 — Minor: distinguish a general coordinate subspace from
   the previously defined coordinate plane.** In
   `sections/05-universality.tex:22–24`, the transfer theorem calls a section
   with arbitrary `p` free coordinates a “coordinate plane.” Section 04,
   immediately before Lemma `lem:section-facet` (line 376), explicitly defines
   a coordinate plane to have exactly two free coordinates. Use “coordinate
   affine subspace” or “coordinate p-plane” in the general transfer theorem,
   reserving the previously defined term for its two-coordinate application.
   The transfer and its coefficient corollary are mathematically correct;
   this is only an inconsistent use of a defined term.

No other required correction was identified. The limitations about nested
series–parallel graphs, coefficient bit lengths, and dense decomposition
output are appropriate boundaries, not unfinished proofs in this stage.

## Section 07: independent mathematical examination

### Exact profile system and the reduced normal universe

I derived the gadget interval directly from its state entries. An only-`a`
state fixes its `a` entry; an only-`b` state contributes `w_j-v_ij`; a doubly
observed state fixes the profile to `u_ij+v_ij`; an unobserved state contributes
any value in `[0,w_j]`. Nonnegativity of observations is needed and is included
in the prechecks. The resulting interval is exactly the displayed endpoint
system. Setting `b` entries and bypass entries then gives all state balances,
capacities, aggregates, and observations, including zero weights.

Eliminating `w_0` changes the upper endpoint into the positive subset normal
on `A_i union T_i`. Because the residual is always in `U_i`, no missing
negative nonsingleton subset appears. Apart from the negative full normal,
the only negative normals are singleton normals. The universe bound
`2^m+m`, the separate scalar-zero-row checks, and the individual right-hand
side coefficient assertion follow. In particular, the smaller universe is a
real structural reduction from the earlier full signed-subset library.

### Determinant bound, circuits, and recovery complexity

Extreme positive dependences have minimally dependent support of size at most
`m+1`. The cofactor construction uses square minors of order at most `m`;
whole-row sign changes turn each such matrix into a 0/1 matrix, so the
improved bound by `Delta_m^{01}` is valid. Positivity makes the weighted
minimum expansion exact. All branch inequalities are globally valid, even
when active rows change at another point.

The enumeration bounds are `2^{O(m^2)}` because subsets of at most `m+1`
normals are selected from an exponential-size fixed universe. The profile
polyhedron is bounded by the explicit state weights. At any vertex, including
in a lower-dimensional profile region, the active rows span the ambient
`m`-space. Thus inverse-basis enumeration recovers a feasible profile. The
greedy construction fills precisely the remaining unobserved `a`-entry sum,
which lies between zero and the available total capacity; it preserves all
observations and gives the required state flows.

The rational bit argument is sufficient. The grouped right-hand sides are
input-derived affine values, basis determinants and cofactors have
`O(m log m)` bit bounds, and there is one profile inversion rather than an
uncontrolled sequence of inversions across gadgets. Greedy filling adds and
subtracts numbers with a common polynomial-length denominator. Dividing by
positive input state weights also preserves polynomial length. The bit-mask
implementation qualification avoids copying a full normal for each cell row;
the stated `O(mL+|O|+m)` arithmetic construction cost is attainable. None of
these bounds is presented as a unit-bit-cost runtime claim.

### Two-label unit coefficients

The five tests are exactly feasibility of the two singleton intervals and
their attainable sum interval. The explicit recovery formulas satisfy each
bound. I separately checked the repeated-product issue: for an only-`a`
product, the two possible negative occurrences have incompatible circuit
normals; for a doubly observed `a` product, its two positive occurrences
either share a normal group or cannot coexist in a circuit. The only-`b`
case has the analogous exclusion. Doubly observed `b` products and bypass
products only have opposite local singleton occurrences. Hence circuit
weights of one really yield unit product coefficients.

For the common bypass flow, the possible two negative contributions from
the positive singleton rows are offset by the compulsory positive contribution
from the negative full row. The other circuits are immediately bounded. This
verifies the flow coefficient claim as well as the product claim.

### Three-label classification and both flow-equation repairs

I independently classified the positive circuits. Without the negative full
normal, minimality leaves one positive subset and its negative singletons.
With the negative full normal, an opposite full row gives the two-row circuit;
one negative singleton forces the two pairs containing its coordinate; without
negative singletons the minimal positive cover is a partition or the triangle
of all three pairs. This yields exactly the four displayed types, with counts
`7,5,3,1`. Only the negative full row in the pair triangle has weight two.

The two normal-exclusion properties used in the occurrence argument hold for
all four types. Every product coefficient therefore stays unit. The doubled
negative-full weight has no product in its right-hand side. Individual gadget
flow coefficients have only two opposite-signed endpoint occurrences, each
with weight one.

The bypass analysis identifies all exceptions. Coefficient `-2` requires the
three-singleton partition and three upper endpoint branches. They come from
distinct gadgets, and the selected gadget's `x_a` coefficient is exactly
`-1`, so adding its flow equation changes the affected coefficients to
`(-1,0,1)` on `(x_h,x_a,x_b)`. Coefficient `+2` requires the three-pair circuit
and three lower endpoint branches from distinct gadgets. Subtracting one
gadget equation changes them to `(1,0,-1)`. There is no hidden second
contribution from the chosen gadget in either exceptional case. Validity and
query violation are preserved on the checked original flow domain.

Both example certificates have the stated negative value and satisfy the
independent McCormick inequalities. The four-label obstruction is the valid
`N=4` balanced-incidence construction, whose ratio two is invariant under
affine-equation additions. Thus the threshold is sharp for the claimed
unit-flow/product coefficient property.

Finally, global observation-label merging is exact because every retained
label shares the same original flow domain. The merged weight is
`1-sum_{j in J} y_j`, independently of the number of omitted labels.
The same normalized merged flow recovers all omitted states, with only their
weights requiring additional bookkeeping. The corollary correctly distinguishes
compact recovery from writing every dense global flow.

## Sections 05–06 and integration

The transportation transfer is valid: slack introduction preserves boundedness;
the cited coordinate-erasing construction preserves the designated original
coordinates; padding adds three fixed corner entries and forces all old/new
cross entries to zero. The two observed boundary layers, their aggregate, and
the residual layer enforce every table margin. Conversely table layers give
flows of their prescribed values, and acyclicity makes every arc flow at most
the layer value, proving the homogeneous capacity bounds. Fixing all aggregate
flows and observing only designated interior products yields the claimed
coordinate section directly. Uniform scaling preserves coefficient ratios.
The section constants are correctly distinguished from original nonlinear
model data when establishing the unit-data input-length claim.

For balanced incidence, the necessary inequality follows by multiplying the
row residual capacities by the positive balancing vector. The inverse formula
has zero total profile change. With the usual induced infinity matrix norm,
the stated neighborhood bounds both the profile perturbation and the row
surplus. Reducing a single allowed entry in the selected row supplies a valid
state-flow decomposition on the entire local feasible side. The chosen
observed entries remain below their profiles and strictly positive. The
section-facet lemma is therefore applicable.

I checked the Fibonacci column counts, recurrence, kernel proof, sum of the
balancing weights, and invertibility of the complement. The complement makes
the observed entries exactly the sparse ones of the original incidence
matrix. The graph rank, treewidth, and sparse bit counts match. The simple
degree-three modification adds the stated numbers of vertices/arcs and gives
a unique flow extension; fixing the new aggregate coordinates preserves the
same two-product coordinate section. The claim concerns numerical coefficient
magnitudes, not superpolynomial bit lengths or separation hardness.

The scalar-composition failure is consistent with the shared-profile theorem:
one gadget can transfer a sufficiently small amount of profile mass, while
other gadgets use the nominal profile, but the resulting collection has no
common profile. The positive small-state results and the growing-state
coefficient obstruction therefore fit together without contradiction.

## Independent executable evidence and build

The scripts in `verification/reviewer3/stage05-round01/` import no repository
hull or author verification implementation:

- `check_chain_circuits.py` independently enumerates the reduced circuit counts
  **1, 5, 16**, verifies the complete listed three-label classification and the
  full signed-subset counts **1, 5, 41**, and checks primitive weights.
  It tests **8, 320, and 6,144** per-product coefficient bounds across all
  one-gadget observation-class patterns for one, two, and three labels. Each
  normal independently chooses a row, including a zero contribution from
  other gadgets, so these checks address repeated-product branch accumulation.
  It also verifies both repaired example inequalities at all path/simplex
  vertices, for **72 exact validity and equivalence checks**.
- `check_balanced_sections.py` checks the four-label matrix and Fibonacci
  matrices for `q=3,...,9`, including their exact balancing identities and
  complements. It verifies **106 rational feasible state-flow witnesses** and
  **94 negative balancing certificates** in their local sections.

The finite checks supplement the proofs rather than replacing them. Their
JSON results are retained. A private full-snapshot `latexmk` build succeeded;
the final 38-page log has no warnings or overfull/underfull boxes.

## Primary-source audit and limits

I opened the [published De Loera–Onn article](https://www.math.ucdavis.edu/~deloera/researchsummary/universalitytransportation.pdf)
and checked Theorems 1.1–1.2, the coordinate-erasing definition on printed
p.807, and the Section 3.3 first-layer injection on printed p.816. The explicit
injection is exactly the one cited. The two-commodity interpretation on
pp.807–808 is already known, as the manuscript acknowledges. The further
sparse bilinear section transfer does not misattribute transportation or
multicommodity universality.

The [Alon–Vu primary manuscript](https://web.math.princeton.edu/~nalon/PDFS/av1.pdf)
contains the ill-conditioned matrix and related 0/1 simplex geometry
background, including Section 3.2. The manuscript uses it for that classical
phenomenon, not for the restricted network construction. The
[Almoghrabi–Skutella–Warode primary article](https://link.springer.com/article/10.1007/s10107-026-02392-8),
Remark 1, explicitly distinguishes aggregate flow decomposition from a
decomposition of the full commodity vector. The comparison remains accurate.
The previous published/preprint author-list bibliography correction is present.

This is a bounded primary-source audit, not an exhaustive priority search for
the new small-state theorem. I did not implement the full general
transportation-universality compiler or perform new industrial performance
experiments. Those are not prerequisites for the mathematical assertions
reviewed here. No current-round reviewer report or author/root check was used
as evidence for correctness.
