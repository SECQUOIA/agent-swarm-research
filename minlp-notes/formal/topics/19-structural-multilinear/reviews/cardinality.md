# Independent review of cardinality envelope foundations

Reviewed 2026-09-20 against C01 and C02 in [CLAIMS.md](../CLAIMS.md), and the
cardinality-envelope lemma in `paper-relaxation-limits/sections/05-feedback-frequency.tex`.
The reviewer did not author or change the three reviewed proof modules.

**Result: C01 and C02 are proved as stated in the inventory. No mathematical
or statement-scope defect was found. This result does not discharge C03 or
W03.**

## Reviewed statements

- `StructuralCardinality.lean`: `ConvexCountTable`, finite-table extension,
  `cardinalityLower_le_expect`, `exists_cardinalityLower_law`, and
  `cardinality_minimum`.
- `StructuralInterpolation.lean`: the actual tensor-product interpolant,
  separate affinity, vertex agreement, identification with independent
  Bernoulli expectation, and `cardinalityFactor_minimum`.
- `StructuralCardinalityUpper.lean`: finite slope ordering, threshold-law
  support and peeling lemmas, `convex_cardinality_common_upper`,
  `cardinality_maximum`, and `convex_cardinality_sum_common_upper`.

The lower-law argument was traced into `exists_adjacentLaw` and
`convex_count_expect_lower` in `PhysicalEnvelope.lean`. The envelope bridge
was checked in `CubicGap/Envelope.lean` and `CubicGap/Hull.lean`.

## Scope and boundary checks

1. **Finite convexity is sufficient.** `ConvexCountTable φ d` compares slopes
   only when `k + 2 ≤ d`. The continuation copies the last slope. For `d=0`
   it is constant, and for `d=1` it imposes no unintended convexity condition.
   All actual random counts are at most `d`, so the artificial tail does not
   change any expected value.
2. **The upper interpolation endpoint is valid.** At mean count `d`, the
   floor equals `d` and `countFrac=0`. The proof explicitly cancels the value
   at `d+1`; it does not assume convexity or any specified original value
   there. Means zero, one, and interior integer counts are included.
3. **Signed and decreasing tables are covered.** Neither the lower nor the
   upper proof assumes nonnegative table values or slopes. The upper proof
   adds the same final-slope term to both expectations, even when that term
   is negative. Nonnegative coefficients are required only when weighting
   and summing factors.
4. **The continuous factor is the right function.** `cardinalityFactor` is
   the multiaffine interpolation of binary count values. It is not the
   generally different composition of a continuous function with the mean
   sum. Separate affinity and agreement at every binary vertex are proved.
   The abstract endpoint theorems also apply to any separately affine
   function with those same binary values.
5. **Actual graph hulls are used.** `minimum_from_laws` and
   `maximum_from_laws` invoke the proved equivalence between the continuous
   cube graph hull and finite binary laws. The lower endpoint has an actual
   law attaining it; the upper endpoint is attained by `thresholdLaw x`.
   These are not numerical bounds with attainability assumed.
6. **All ambient means are preserved.** The adjacent-count construction
   starts with the Bernoulli law and resamples individual coordinates while
   preserving other means. Coordinates outside the support remain covered
   by `HasMeans`. Empty supports, an empty ambient coordinate type, singleton
   supports, tied means and unused coordinates require no additional
   nonemptiness or strict-interiority assumptions.
7. **The upper argument terminates.** It uses strong induction on a finite
   support, removing a minimum-mean coordinate at each step. Positive-weight
   threshold atoms containing that coordinate contain the entire support;
   zero-weight atoms are handled separately. No uncrossing procedure,
   unstated termination hypothesis, or existence of an optimizing law is
   assumed.
8. **Simultaneous upper attainment is sound.** Every factor uses the same
   threshold law on the full ambient coordinate space. The weighted-sum
   inequality allows overlapping or repeated scopes and an empty term set.

The manuscript's additional explicit sorted-means formula for the upper
value is not a named theorem in these modules. The proved peeling recurrence
contains its mathematical induction step, and the exact upper value is
already specified as a threshold expectation. Do not describe the displayed
sorted formula as separately checked by Lean without adding that corollary.
A uniqueness theorem for multiaffine interpolation is likewise not separately
stated; existence and the endpoint claims needed by C01/C02 are proved.

## Targeted verification

From `formal/`, the following passed:

```sh
PATH=$HOME/.elan/bin:$PATH LEAN_NUM_THREADS=1 lake build Formal.MultilinearGap.StructuralCardinality Formal.MultilinearGap.StructuralInterpolation Formal.MultilinearGap.StructuralCardinalityUpper
PATH=$HOME/.elan/bin:$PATH LEAN_NUM_THREADS=1 lake env lean /tmp/topic19-cardinality-review.lean
```

The temporary review file checked the axioms of `cardinalityFactor_minimum`,
`cardinality_maximum`, `convex_cardinality_common_upper`, and
`convex_cardinality_sum_common_upper`. Each depended only on `propext`,
`Classical.choice`, and `Quot.sound`; no `sorryAx` appeared. It also checked
an empty ambient dimension, the top interpolation endpoint, and a negative,
decreasing, strictly convex finite table with an arbitrarily nonconvex tail.
An initial review-file run had an omitted type annotation for its empty
support; the annotation was corrected and the final run passed. No proof
module was changed for this review. No project-wide check or CI inspection
was run.

Reviewed SHA-256 values:

```text
81344b22d979ed87d6a8b77e1f87d4fc66d120e49d177e18a1e2ce2012bd8895  StructuralCardinality.lean
a01ffd1a827dc0aadca6e904f83e081791bb79b820324e24936a66ee5126cf3d  StructuralInterpolation.lean
9e9f0dd6d95ea55447fab2338c1a26bbc9d6464ffdc489fa3c6c3cd153bd8ee4  StructuralCardinalityUpper.lean
```

## Remaining aggregate envelope work

The following lists the mathematical connections still needed beyond the
reviewed modules. It does not assume that any graph supplies a cycle
decomposition, a TU partition, or the required laws.

For **C03**:

- Turn a finite law over points in the prescribed degree slab, with mean
  `x`, into the equality between the average `cardinalityLower` and its
  value at `x`. Handle coincident floor/ceiling bounds at integer sums.
- Prove the corresponding concavity inequality for each exact upper value,
  hence that the average sum of local gaps is at most its value at `x`.
- At an actual fractional-cycle row, identify its integral-one count `m`
  and two half-valued coordinates. Derive lower value `φ(m+1)`, upper value
  `(φ(m)+φ(m+2))/2`, and their nonnegative curvature difference.
- Establish the joint count probabilities of matching/complement rounding:
  zero and two selected fractional edges each have probability `1/(2L)`.
  Coverage probability alone does not supply the expected cost for an
  arbitrary cardinality table. Add the integral ones, obtaining cost equal
  to the local lower value plus the local gap divided by `L`.
- Assemble the conditional rounding laws into a global prescribed-mean law,
  prove the aggregate expected-cost bound, and connect that witness and the
  common upper endpoint to the continuous hull of the sum. For bipartite
  slabs, assemble simultaneous exact lower attainment instead. Deduce the
  odd-girth factor and handle zero total gaps without dividing by them.

For **W03**:

- From each class's actual integral slab decomposition, construct a binary
  law with all ambient means and the allowed adjacent counts on every row
  in that class. The single-factor adjacent law does not establish
  simultaneous attainment across the class.
- Prove that each such class law attains every class lower envelope, using
  the affine formula on its allowed interval. Prove that other factors'
  expected deficiencies from their upper values are nonnegative.
- Mix the two laws equally and sum weighted deficiencies. Supply the common
  upper endpoint of the actual separately affine sum, then convert the
  witness to `T ≤ 2H`. Include empty classes, constants, signed table values,
  zero coefficients and zero gaps.
- Separately discharge the structural input: integral class decompositions
  must follow from a proved TU partition and integrality theorem. Assuming
  those objects only yields a conditional envelope lemma, not W03's
  treewidth theorem.

Existing generic envelope and mixture lemmas may shorten these steps, but
their premises must be checked for the actual cardinality factors and laws.
