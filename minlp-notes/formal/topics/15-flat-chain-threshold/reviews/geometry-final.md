# Independent final review: circuits, coefficients, and obstructions

The reviewed mathematical results have no unresolved soundness or scope finding.
This review covers FC10–18 and the mathematical parts of FC38–53. It does not
certify the execution or complexity claims within FC44, which are reviewed in
the algorithm lane. It does not mark the whole topic complete.

The reviewer independently read the proof statements and substantive proof bodies,
compared them with Section 7 and the required Section 6 construction, and ran the
targeted commands below. The reviewer did not author or change any proof module
in this review. Earlier review reports were used to identify possible gaps; their
conclusions were checked against the current code.

## General circuits and finite descriptions

- `ThresholdFarkas.farkas_inequalities` proves feasibility for arbitrary finite
  real row systems. Its Fourier–Motzkin induction keeps zero-coefficient rows,
  forms nonnegative combinations of positive and negative rows, and reconstructs
  a variable from compatible finite lower and upper bounds. Either bound family
  may be empty. Neither boundedness nor full dimension nor prior feasibility is
  assumed. The zero-dimensional case checks every scalar row.
- `ThresholdPositive` derives a positive circuit from an actual nonzero
  nonnegative cancellation using an affinely independent convex representation.
  The support bound and unique kernel ray are conclusions. `ThresholdCone`
  proves pointedness, finite positive circuit decomposition by strict support
  descent, both directions of the extreme-ray characterization, and equivalence
  with support-minimal nonnegative dependencies. It also excludes signed
  dependencies on a proper subset. The cone-generation claim is therefore
  stronger than a rank or support-size calculation alone.
- `ThresholdCircuitWeights` selects a genuinely nonsingular coordinate minor
  from independent rows. Its signed cofactor vector is nonzero and proportional
  to the positive real relation. Absolute values, followed by gcd division,
  produce positive primitive integer weights. `ThresholdCircuitInteger`
  transfers these weights back to the original circuit and proves the exact
  positive scaling relation. It does not assume the circuit weights are rational.
- `ThresholdDeterminant.delta01` is the finite maximum over Boolean square
  matrices of every order from zero through `m`. Whole-row sign changes justify
  using this bound for the actual normal minors. The values at 1, 2, and 3 are
  kernel-checked. `ThresholdHadamard` proves the real-exponent upper bound,
  including the empty matrix and `m=0` cases.
- `ThresholdPreprocessCriterion.feasible_iff_compiledPartialTests` restricts to
  the subtype of present normals before using the full library. Missing rows
  are not replaced by constraints in the emitted family. In the separate
  three-label proof, `ThresholdPartial` uses artificial large right-hand sides
  only inside a feasibility proof; `ThresholdSourceGrouping` ultimately selects
  only attaining original rows. This distinction prevents the earlier redundant
  box rows from invalidating the coefficient argument.
- FC16 has an explicit identity: `weighted_groupMinimum_eq_minimum` in
  `ThresholdCoefficientBound`, supported by independently attained minima and
  the nonnegative weighted comparison. Its row fibers are nonempty finite types;
  absent directions are handled separately by the partial-library results.
  `weighted_groupMinimum_nonneg_iff` proves the exact branch expansion.
- `ThresholdGeneralSourceDescription` indexes finitely many actual source-row
  choices and bounded natural weights. Cancellation is checked, and the resulting
  tests are equivalent to a real profile and then actual graph-hull membership.
  The family also catches zero-normal rows. Its coefficient bound uses the
  coefficients of the literal affine expressions, rather than an abstract
  placeholder for a unit row.
- `ThresholdBoundedDescription` combines those branches, original-domain rows,
  and both signs of the simplex equality into one fixed finite family. The
  expression and cancellation transfers depend only on the observation pattern;
  the family is exact for every query with that pattern. All flow and observed
  product coefficients satisfy `(m+1)*delta01 m`. Simplex-coordinate coefficients
  and constants are deliberately outside that bound.
- `exists_violated_valid_branch` fixes the attaining row choices at the rejected
  query and proves validity at every feasible point without recomputing them.
  `ThresholdCircuitOracle.groupedCircuitOracle_separates` provides the analogous
  result for the actual stored row identifiers, including original-row provenance.

The finite-description wrappers evaluate `ReductionData` on its balance affine
space, where `xb = 1 - xh - xa`. This parameterization is explicit in their types.
To view them as an ambient original-coordinate description, adjoin the actual
unit-coefficient gadget balance equations. They do not assert that the cuts
alone impose conservation on independently varying `xb` coordinates.

## Three-label classification and repairs

`ThresholdClassification.supportMinimal_classification` covers all real
support-minimal positive dependencies, without bounding candidate integer
weights in advance. It proves positive proportionality to a listed circuit and
unique support. The checked sixteen-entry table has the source's seven subset,
five partition, three overlap, and one pair-triangle forms. The occurrence
lemmas establish the forbidden pairs and identify the unique doubled weight on
the pair triangle's negative-total normal.

`ThresholdProductCoefficients` derives the occurrence pattern from each actual
row expression and observation class before applying the finite occurrence
lemma. In particular, doubly observed `b` products do not enter the endpoint
residual through an assumed extra term. The negative-total row contains no
observed products. The conclusions cover every actual branch.

`ThresholdFlowRepair.bypass_cases` isolates exactly coefficients `-2` and `+2`
as the exceptional cases. `ThresholdFlowWitness` proves that each exception
comes from three distinct actual gadgets and identifies the chosen gadget's
flow coefficient. The repairs add or subtract that gadget's actual balance
equation. `ThresholdBalanceRepair` proves unchanged evaluation on the entire
balance domain and unchanged product coefficients; `ThresholdFlowRepresentative`
and `ThresholdUnitDescription` assemble a unit representative for every branch
and a fixed finite exact unit description. No replacement of a selected
endpoint by an artificial pair box is used.

The two numerical examples are checked as actual `ReductionData` instances.
`ThresholdRepairData` verifies the original domain and every selected scalar
McCormick inequality. `ThresholdRepairExamples` proves values `-1/5` and `-1/20`,
bypass coefficients `-2` and `+2`, and unit repaired expressions with the same
values. `ThresholdRepairSeparation` also proves nonmembership and global validity
of each fixed repaired expression for its observation pattern.

## Actual-coordinate obstructions

- The section lemma produces an active nonconstant inequality in every finite
  description, then proves positive proportionality of its two free
  coefficients. `ThresholdArbitrarySection` removes sign restrictions on the
  section normal, including either component being zero. Valid affine equations
  vanish on both free coordinates.
- The balanced-incidence construction uses the exact displayed neighborhood
  `a / (16*(1+R)*(1+inverseSize K))`. `inverseSize` is the operator norm induced
  by the coordinate sup norm. The inverse equation, perturbation bound, and
  zero perturbation sum are derived from invertibility and column balancing.
  The profile proof covers the boundary of the feasible half-plane. The separate
  initial-entry and single-row-correction lemmas verify the stated construction.
- `sectionPoint_eq_productSlice` proves that only two distinct individual
  observed products vary. Their coefficients are preserved without coordinate
  rescaling. `ThresholdFace` connects the sum-one section to the original
  simplex inequality domain by deriving that the residual state flow is zero.
- The four-label instance has the source's flows, weights, seven observations,
  and exact inequality `2U+V >= 3/32`. The graph counts concern the actual graph;
  its cycle rank is the dimension of the incidence kernel. The obstruction
  theorem means coefficients in the discrete set `{-1,0,1}`, not merely absolute
  value at most one. It permits arbitrary additional affine equations and even
  arbitrary inequality index types. The unused-label extension preserves the
  actual free products and derives zero flow in added zero-weight states.
- `ThresholdStarObstruction` instantiates every balanced-incidence hypothesis
  with the explicit star family. Its unavoidable ratio is `k-1`, and the terminal
  unboundedness theorem quantifies over descriptions of the actual original hull.
  The positive denominator is proved. Its observation count is connected to the
  actual observed-product subtype; graph dimensions and cycle rank match the
  paper after substituting `M=k-1`.

## Targeted verification actually run

From `formal/`, all these commands passed with warnings treated as errors:

```sh
lake build Formal.NetworkSimplex.ThresholdGeneralSourceDescription Formal.NetworkSimplex.ThresholdHadamard Formal.NetworkSimplex.ThresholdCone Formal.NetworkSimplex.ThresholdUnitDescription Formal.NetworkSimplex.ThresholdRepairExamples Formal.NetworkSimplex.ThresholdArbitrarySection Formal.NetworkSimplex.ThresholdOriginalObstruction Formal.NetworkSimplex.ThresholdUnusedObstruction Formal.NetworkSimplex.ThresholdStarObstruction --wfail
lake build Formal.NetworkSimplex.ThresholdRepairSeparation --wfail
lake build Formal.NetworkSimplex.ThresholdBoundedDescription --wfail
lake env lean -DwarningAsError=true /tmp/threshold-geometry-final-review.lean
```

The temporary review file printed the transitive axioms of 21 terminal results,
including Farkas, Hadamard, cone generation and extremality, primitive weights,
source-family exactness and coefficients, classification, both repair witnesses,
the full unit description, both repaired-example validity results, arbitrary
section normals, the balanced section, affine-equation invariance, four-label
and unused-label unit impossibility, and star-family unboundedness. Every result
used only `propext`, `Classical.choice`, and `Quot.sound`. The topic's final audit
and source manifest remain the durable whole-topic evidence.

No project-wide verification was run, and no CI status or logs were inspected.

## Follow-up review: zero through two labels and ambient coordinates

The final frozen `ThresholdSmallClassification`, `ThresholdOneUnit`,
`ThresholdSmallSource`, `ThresholdSmallDescription`, and
`ThresholdAmbientDescription` were independently reviewed after the first
review. No proof changes were made by this reviewer.

`ThresholdSmallClassification` closes the distinction between counting listed
supports and counting all primitive integer circuits. In each dimension, its
`PrimitiveCircuit` predicate requires real support minimality and gcd one, with
no prior bound on the integer entries. Real classification gives a positive
scalar multiple of a listed row. A proved weight-one pivot identifies the
scalar as an integer entry; gcd one forces that entry to be one. The exact
finite-image equalities, injectivity, and cardinalities therefore establish
`1,5,16` for all primitive circuits. Separate maximum theorems prove both upper
bounds and attainment of `1,1,2`. The normal counts are `2,6,11`. The actual
five two-label supports and their checked occurrence restrictions match the
three opposite pairs and two triples in FC33.

The direct one-label coefficient proof checks the signs of actual positive and
negative source-row coefficients. This is necessary because the negative total
and negative singleton normals coincide in one dimension. It does not borrow a
false assumption that these are distinct directions. Product signs oppose,
negative-normal gadget-flow coefficients vanish, and bypass signs also oppose,
so the literal two-row sum is unit. The source-only partial-library argument
then supplies exactness. The one- and two-label terminal finite descriptions
discharge every hypothesis of the generic assembly theorem using these actual
branch results, include zero rows and domain rows, and fix the observation
pattern across queries. Their correctness is not an assumed premise in the
terminal theorem.

The zero-label finite description has no circuit branches. FC27's stronger
simplification to the original flow polytope follows from
`NetworkSimplex.original_hull_no_observations` in `ThresholdMergeObserved`:
its conclusion is exactly original flow feasibility and original simplex
feasibility, with no profile tests. With `m=0`, the observation type is empty
and the explicit simplex condition is vacuous. The scalar-source description
alone should not be cited as the proof that these extra scalar checks are
redundant.

`ThresholdAmbientDescription` makes the earlier balance-space qualification
explicit. `oppositeFlow_eq_of_balance` proves equality to the derived b-flows
from the supplied original gadget equations. `boundedDescription_ambient` and
`exists_unit_ambient_description` then evaluate the literal rows at arbitrary
supplied b-flows satisfying those equations. The equations themselves have
unit coefficients. This is the appropriate bridge to original-coordinate
representatives; it does not silently assume that independently supplied
b-flows already equal the derived values.

`ThresholdSignedUniverse` was also checked for FC28. It proves the full
all-dimensional signed-subset library criterion, primitive determinant bounds,
packed cofactor preprocessing coverage, and the exponential candidate bound.
Its `signed_compiled_coefficient_bound` is explicitly a generic expansion lemma:
it assumes the supplied row-coefficient vector is unit. The final source-adapter
review below checks the additional bridge to literal unreduced chain rows and
closes this distinction for FC28.

The following additional targeted build passed:

```sh
lake build Formal.NetworkSimplex.ThresholdSmallClassification Formal.NetworkSimplex.ThresholdSmallDescription Formal.NetworkSimplex.ThresholdAmbientDescription Formal.NetworkSimplex.ThresholdSignedUniverse --wfail
```

A second temporary probe, run with
`lake env lean -DwarningAsError=true /tmp/threshold-small-geometry-review.lean`,
printed the axioms of 12 additional results covering these counts, maxima,
small-label descriptions, ambient wrappers, the no-observations theorem, and
signed-library results. All used only the same three standard axioms. The first
probe attempt preceded completion of the ambient module build and reported a
missing object file; the sequential rerun after the successful build passed.

## Final FC28 source-adapter review

The frozen `ThresholdUnreducedLift`, `ThresholdUnreducedRows`, and relevant
`ThresholdPreprocessOperands` declarations were independently inspected. The
previous distinction between a generic unit-coefficient premise and actual
unreduced source expressions is closed. No unresolved finding remains.

- `unreducedData` retains every one of the original `d=m+1` states as an explicit
  coordinate and inserts one new unobserved state of weight zero.
  `unreducedData_full_cons_iff` and `unreducedData_reduced_iff` prove the exact
  profile correspondence. The proof derives the full-profile sum from both
  total rows; it does not assume the desired profile conclusion or that the
  original state zero is unobserved.
- `unreducedKey` and `unreducedExpression` use the literal unreduced upper
  endpoint `-w(B∪N) <= -R`. `unreduced_endpoint_iff` proves equivalence to the
  reused endpoint only after deriving the total-profile equality. The lower
  endpoint and local rows retain their actual original meanings. This avoids
  incorrectly presenting the residual-eliminated positive endpoint as the
  unreduced negative subset row.
- `unreducedRows_iff_fullProfile` proves both directions for every supplied
  profile vector. `unreduced_normal_mem_or_zero` includes zero rows explicitly,
  and `fullProfile_iff_unreduced_tests` uses the bounded integer-certificate
  criterion on the actual finite source-row set. In particular, contradictory
  scalar rows cannot disappear from the feasibility test.
- `unreducedExpression_eval` identifies the expressions with the actual source
  right-hand sides. Their flow and product variables correspond to every
  original state; the added bookkeeping weight is fixed to zero. Fixing that
  weight introduces no change to flow or product coefficients.
  `unreduced_coefficient_unit` proves the unit bound directly from these
  expressions, including the negated residual endpoint. The terminal
  `unreduced_compiled_coefficient_bound` obtains `(d+1)*delta01 d` for actual
  branches without a caller-supplied unit-coefficient assumption.
- `unreduced_compiled_branch_valid` requires selected source keys to match the
  stored circuit support and proves validity on every feasible full profile.
  The coefficient-bound theorem does not need that matching premise because
  its magnitude estimate holds for arbitrary selected source rows. Together
  with exact source grouping and the existing signed-library criterion, these
  results supply the source claim without a duplicate unreduced oracle.
- `ThresholdPreprocessOperands` bounds the actual cached cofactors, gcd-fold
  inputs and intermediate Euclidean divisions, normalized weights, validation
  products, and arbitrary partial validation sums. Rejected candidates are
  included. The signed-universe arithmetic and bit-work bounds specialize the
  actual cofactor compiler's declared cost model to `2^(d+1)` packed normals.
  They are `2^(8*(d+2)^2)` and `2^(14*(d+2)^2)`, respectively. As elsewhere in
  this topic, the bit-work bound is for the declared arithmetic model, not a
  theorem about a compiled runtime or a machine-integer implementation.

The final targeted build passed:

```sh
lake build Formal.NetworkSimplex.ThresholdUnreducedRows Formal.NetworkSimplex.ThresholdPreprocessOperands --wfail
```

The warning-free probe
`lake env lean -DwarningAsError=true /tmp/threshold-unreduced-source-review.lean`
printed the transitive axioms of the eight source-adapter results listed above
and four operand/work results. All 12 used only `propext`, `Classical.choice`,
and `Quot.sound`. No project-wide verification or CI inspection was performed.
