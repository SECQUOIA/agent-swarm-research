# Stage 4, round 1 — independent review 1

**Verdict: no major issues; accept after one minor wording correction.**

Reviewed the frozen `stage04-round01` manuscript, all of
`sections/04-bounded-rank.tex`, integration, and relevant accepted dependencies.
I independently checked the new recovery theorem and five-product example;
the earlier seven-product audit was not treated as evidence for either new
result. I did not read other current-round reviews, coordinate judgments, or
edit manuscript sources.

## Enumerated findings

1. **S04R01-R1-F01 — minor: the final comparison attributes a geometric change
   to the reference flow without mentioning the changed balances.**

   Location: `sections/04-bounded-rank.tex`, lines 512–514, the end of
   Remark `rem:seven-product-k4`.

   The sentence says that changing the reference on `01` makes the residual
   support face an edge rather than a point. A change of reference for a fixed
   balance vector translates cycle coordinates and cannot change a support
   face's dimension. In these two examples, changing that coordinate of `v`
   also changes `b=Av`; hence the actual flow domain changes. The preceding
   displayed data are correct, but the explanatory sentence can mislead a
   reader into interpreting the improvement as a choice of representation of
   the same instance.

   Suggested correction: say that changing the reference value **and the
   induced balance vector** changes the flow domain so that the residual
   supporting face is an edge, permitting one fewer line state. This is minor:
   it requires no alteration to the examples, proofs, bounds, or conclusions.

## Core mathematical audit

### Feasibility and finite support separation

The signed cycle-normal matrix (lines 18–58) preserves total unimodularity
under sign duplication and includes both coordinate signs. The minimum
right-hand sides correctly combine repeated arc normals and enforce both
sides of every observed equality. Zero-weight states are points or infeasible;
no hidden full-dimensional assumption enters.

The local positive-circuit proof (lines 67–103) is sound. Extreme nonnegative
dependences have minimally dependent support, at most `s+1` rows. TU cofactors
give primitive coefficients one. Farkas therefore reduces feasibility to the
enumerated tests. An observation can occur twice in a circuit only when its
two opposite normals constitute that entire circuit; the selected contributions
then either cancel or use distinct product coordinates. This verifies the
unit local-cut claim.

For the edge-direction lemma (lines 110–135), an edge's active normals have
rank `s-1` in ambient coordinates even when the polytope lies in a proper affine
subspace: inactive inequalities remain slack under sufficiently small nullspace
motions. TU gives both ternary direction vectors and ternary products `Md`.
This latter property is essential to the later multiplier bound and is proved,
not merely assumed.

The chamber argument (lines 137–176) covers lower-dimensional states and sums.
An interior chamber objective cannot maximize along an edge, so each summand's
maximizer is unique and constant within the chamber. Supports extend linearly
to its closure. The coordinate hyperplanes make closed chambers pointed, and
the enumerated primitive rays include all their extreme rays. Thus finite ray
tests imply every support inequality. This also handles the zero singleton
used for an empty suffix in recovery.

The dual-basis lemma (lines 194–228) remains valid for degenerate primals.
Reducing an optimal dual's dependent positive support preserves its objective
and eventually yields independent supporting rows, which can be completed to
a full basis with zero added multipliers. For the stronger coefficient bound,
`B^{-T}h` is primitive and orthogonal to the independent ternary vectors
`Bd_i`. Its cofactor characterization therefore gives `H_s`, avoiding the
larger bound that a naive triangle inequality would give.

I checked the description/separation theorem (lines 230–291) row by row:
nonnegative basis multipliers preserve concavity of endpoint minima, active
branches yield globally valid affine majorants, and a basis cannot contain
opposite normals. Distinct state/product indices prevent unintended coefficient
addition. The `2^{O(r^2)}` enumeration counts, per-state work, and sparse bound
`sum_B a_B <= |O|` are consistent. The integer flow/product bound is properly
qualified by rational row scaling rather than primitive whole-row integrality.

### New finite-basis exact recovery

I checked all parts of lines 298–372 independently.

- For each step, the finite-support lemma describes the entire suffix sum,
  so the additional inequalities are exactly the reflection/translation
  required for `Q_i intersect (t - suffix)`. They do not provide only an outer
  approximation.
- This intersection is nonempty by the maintained aggregate invariant and
  bounded because it is inside `Q_i`. At any vertex, active normals have full
  ambient rank; otherwise sufficiently small positive and negative nullspace
  motions would contradict extremality. This justifies enumerating full
  bases even for segments and singleton intersections.
- All normals are fixed before observing the candidate. If their count is
  `2^{O(s^2)}`, enumeration of `s`-row bases and checking every row for every
  candidate gives `2^{O(s^3)}` per state, including inverses. The sum over local
  states retains the sparse-input factor. The theorem does not quietly claim
  the cheaper separation parameter dependence for recovery.
- The bit-growth argument is valid. Choose a common denominator for initial
  endpoints, supports and aggregate. A remaining aggregate denominator can be
  maintained as that initial denominator times the determinants selected at
  preceding steps. Each chosen basis multiplies it by only one new fixed
  determinant, so its bit length increases additively per state. Rejected
  candidates are evaluated from the current right-hand sides independently;
  their denominators do not accumulate over all rejected bases. Finite state
  bounds and parameter-bounded inverse matrices control numerator lengths.
  Final division by an input rational positive weight also has polynomial
  encoding cost.
- Normalization, the merged default, and local exceptions correctly recover
  one global graph point per positive simplex weight. Zero weights and dense
  output costs are separately handled. Storing a block coordinate vector of
  length `s` fits the parameter-dependent sparse bound.

### New five-product sharpness and section transfer

The coordinate-section lemma (lines 380–409) is correct. Two-dimensional local
interior forces every valid affine equation to have zero coefficients on the
two free coordinates. A finite restricted description must contain an active
nonconstant inequality at the boundary; feasibility in both tangent directions
forces its normal to agree, up to positive scaling, with the section normal.
This establishes the claimed invariance under affine-equation modifications
of facet representatives.

I recalculated the K4 incidence balances, aggregate flow, and every observed
equality in lines 411–473. The five products force exactly
`theta^1=(p,q,p)` and `theta^2=s(1,-1,0)`. The residual's `12` upper bound and
`03` lower bound imply support at most `1/3` in direction `(1,1,1)`, proving
necessity of `2p+q>=0`. The displayed witness has the correct sum and every
residual arc value is as printed. For the stated neighborhood,
`0<=w<1/32`; the critical residual `01` deviation lies strictly between
`3/16` and `11/48`, inside its asymmetric scaled interval. All other bounds
also hold. Thus the argument genuinely gives a full local half-plane in two
actual product coordinates, not just a supporting inequality or dual weight.
The rank-three sharpness corollary follows.

I also recalculated the seven-product variant's state sums and bounds. Its
residual support face is a point, whereas the five-product instance's face
is an edge. Those statements are correct; only their attribution to a
reference change alone needs the minor clarification above.

## Exact evidence and build

I wrote `verification/reviewer1/stage04-round01/check.py` using rational
arithmetic and direct three-dimensional determinant formulas, independently
of the repository's separator implementation. It constructs the K4 normal,
edge and support-ray libraries, computes state supports by primal vertex
enumeration, and then tests the new recovery method against those supports.

All checks passed:

- 12 signed normal rows, 7 primitive edge directions, 18 support rays;
- 544 nonsingular recovery bases on the deduplicated normal list;
- 64 exact sequential recovery steps, with state dimensions 0, 1, 2 and 3
  and explicit zero-weight states;
- 185 exact feasible witnesses in the new five-product local section and
  176 exact exclusions using the residual-support certificate.

Results are in `check-output.json`. These finite checks supplement the general
proof review and are not claimed to exhaust all ranks or observation patterns.

A private snapshot copy compiled to 27 pages. Its final log has no LaTeX
warnings or overfull/underfull boxes. The integration introduces no broken
references or inconsistency with accepted foundations.

## Limitations

This round did not independently recheck every new bibliographic field or
establish literature priority. The proof audit does establish the stated
mathematical implications without relying on earlier code reviews. No claimed
practical runtime advantage needs validation in this section: it explicitly
presents the large finite libraries as structural bounds.
