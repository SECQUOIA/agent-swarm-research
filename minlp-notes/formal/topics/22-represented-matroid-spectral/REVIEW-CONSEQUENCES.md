# Independent consequences and subclass review

Date: 2026-09-22. The reviewer did not author the modules reviewed here.
The graphic representation modules, which the reviewer authored, are
excluded and require a separate review.

## Scope and result

Reviewed `UniformRepresentation.lean`, `PartitionRepresentation.lean`,
`Boundaries.lean`, `Criteria.lean`, `CriteriaSelection.lean`,
`CriteriaExecution.lean`, `CriteriaContrastExecution.lean`,
`CriteriaControl.lean`, `CriteriaBitWork.lean`, `Headline.lean`, and
`HeadlineCriteria.lean` against U01–U02, B01–B03, and O01–O06 in
[the frozen claims](CLAIMS.md). The relevant reused DAG criterion,
selector, singular-cost, and arithmetic-trace interfaces were also read.
The explicit fixed-dimension cardinality estimate in
`CoverPolynomialSize.lean` received a separate light review. No semantic
correctness defect was found. The final headline now connects the
computed selectors to the actual original-input cover. This review does
not certify the separate whole-producer bit-complexity theorem. Exact
source hashes for all twelve reviewed modules are recorded in
[the stable-source record](REVIEW-CONSEQUENCES-SOURCES.json).

## Representation checks

- The uniform matrix is an actual rational Vandermonde matrix with distinct
  positive integer evaluation points. `uniform_isBase_iff` proves the
  determinant base predicate exactly when the selected cardinality is
  `q`. `uniform_has_base` supplies a base under the necessary `q <= m`
  condition. Rank is not fixed. The proved entry bound
  `(m+1)(q+1)+1` is polynomial in both dimensions; no numerical magnitude
  is mistaken for its encoding length.
- The partition construction keeps group identities in a sigma type,
  then flattens rows and columns through finite equivalences. Its
  injectivity and selected-index equivalence are proved. Thus the direct
  sum argument reaches the supplied finite matrix, not only an abstract
  direct sum of vector spaces.
- `partition_arbitrary_isBase_iff` applies to every selected finite column
  set. `partitionSelection_groups` proves that the grouped selections
  exhaust these sets. Independent columns force each group cardinality
  to be at most its row quota; equality of total cardinalities then forces
  every quota exactly. The converse uses independent Vandermonde blocks.
- `partition_has_base` requires every quota to fit its group and constructs
  such a selection. Zero quotas and empty groups are covered by the same
  statements. A quota larger than its group is not silently truncated.
  `partitionRepresentation_bits` includes the zero blocks and gives a
  polynomial entry bound when quotas and group sizes grow. These are
  representation-size results, not a traced runtime claim for the
  noncomputable finite-equivalence indexing operation.

## Criterion checks

- `HomogeneousCriterion` includes positive degree, nonnegativity on PSD
  matrices, Loewner monotonicity, and homogeneity for nonnegative scales.
  No concavity is assumed. The generic homogeneous selection theorem
  proves a finite maximum and its ratio; it does not claim an algorithm
  for an arbitrary real-valued objective without a comparison method.
- D-optimality uses `eta = epsilon/p`, determinant-root selection uses the
  dimension-positive hypothesis, and E-optimality uses `eta = epsilon`.
  The E selector imports the proved exact characteristic-polynomial and
  bisection comparator. No eigenvalue separation or distinct-eigenvalue
  hypothesis has been introduced. The all-singular E conclusion is zero.
- Conventional A-cost is an extended nonnegative real and is infinite
  for singular information. The actual rational selector tests the
  determinant before comparing inverse traces. The transfer inequality
  has factor `1+epsilon` at `eta = epsilon/(1+epsilon)` and does not divide
  by an infinite or zero optimum. Positive-definite feasibility is
  preserved by the cover.
- The Moore–Penrose bounds use the proved relative sandwich and PSD
  information. Estimability is checked on the actual range. Contrast
  and weighted contrast statements use extended costs and therefore
  preserve zero variance and non-estimable cases. Executable contrast
  selectors require rational contrasts and weights; weighted correctness
  additionally requires nonnegative weights.
- Adding a common PSD prior requires nonnegative tolerance. Rectangular
  congruence preserves the same candidate cover without a nonsingularity
  hypothesis. Neither operation asserts that an earlier selected optimum
  remains optimal for the changed criterion.
- `selectSetsRun_result` identifies the executed selector with the
  mathematical selector. Matrix-sum construction is included in its
  arithmetic events. D, E, A, contrast, and weighted-contrast selection
  each have an instantiated trace bound. Weighted-contrast bounds keep
  the number of supplied contrasts variable and include their encoded
  coordinates and weights.
- `materializeSetRun` implements the increasing identifier scan and
  charges membership comparisons and copies. It is proved equal to the
  sorted finite-set list used by the semantic selector.
  `selectSetsBitRun_value` proves that the counted scan returns the same
  candidate. The bounds in `CriteriaBitWork.lean` include materialization
  and finite scan control, closing the earlier uncounted-sort concern
  within selector execution. The model retains immutable candidate
  references rather than copying an information matrix at each branch.
  Determinant and inverse constants may be large functions of `p`; this
  is legitimate here because only information dimension is fixed.

## Boundary witnesses

The mixed-determinant witness has two common feasible singleton bases
but determinant zero; the squared single-representation determinant is
positive. The finite-field witness changes an actually nonzero rational
determinant to zero modulo two. These statements justify the rational
characteristic-zero assumptions without claiming that every algorithm
for a broader model is impossible.

The scalar projected values are exactly 1 and 3, while their integer
midpoint 2 is unattained. The three diagonal profiles are actual singleton
bases, and the middle profile strictly improves determinant and minimum
eigenvalue over both endpoint profiles. Dominance deletion and distinct
singular-range witnesses preserve the two-sided-cover limitation.

## Final headline integration

The earlier criterion integration findings are closed by
`HeadlineCriteria.lean`:

- `representedCover_list_nonempty` derives nonemptiness from the actual
  original-input cover. `bestBy_exists_of_nonempty` then proves that the
  computed finite selector returns `some B`. No successful-result or
  spectral-cover certificate is assumed from the caller.
- Every selector theorem supplies the cover from
  `representedSpectralCover_isRelativeCover`, whose information matrices
  are the supplied prior plus selected element matrices. The produced
  factor data and row-reduced representation are connected to these
  original inputs by the headline. Output membership is transported to
  `IsColumnBase A B`, and the approximation inequality quantifies over
  every original column base.
- The remaining list premise identifies an enumeration of the computed
  finite cover. It permits any ordering and duplicates; it is not an
  assumption about approximation or successful selection. Runtime bounds
  depend on the actual list length, so the whole implementation must use
  its proved bounded producer list rather than an arbitrarily repeated
  enumeration.
- D uses positive rational `epsilon` with `epsilon <= 1` and positive
  information dimension. E additionally uses the explicit nonzero
  dimension instance. The endpoint `epsilon=1` is valid: the cover
  theorem holds for every positive tolerance, and these lower objective
  guarantees become zero. Neither theorem asserts exact kernel
  preservation at tolerance one. Zero tolerance is not admitted.
- A uses positive `epsilon`, so `epsilon/(1+epsilon)` lies strictly
  between zero and one. Contrast and weighted-contrast headlines retain
  the explicit strict tolerance interval; the latter also requires
  nonnegative encoded rational weights. Their extended-cost statements
  preserve singular, non-estimable, zero-variance, and zero-weight cases.

The previously reviewed execution additions also close the contrast and
weighted arithmetic and finite-set materialization gaps. Composition of
selector costs with candidate construction and storage belongs to the
separate whole-producer complexity review.

## Polynomial cardinality check

`CoverPolynomialSize.lean` correctly bounds each rank contribution by
replacing the binomial coefficient with `(M+1)^p`, the profile-grid base
with `8 p^2 q^2 ceil(1/eta)+1`, and its exponent with `p(p+1)/2`. There
are exactly `p` positive-rank terms. The initial one for the zero branch
is retained.

The original-input corollary substitutes the proved factor-label bound
`M <= p(m+1)` and then the actual matrix-rank bound `rank(A) <= m`. Its
result is polynomial in ground-set size and inverse tolerance at fixed
information dimension. It does not fix matroid rank, rely on a condition
number, or mistake cardinality for total runtime. The empty-rank and
zero-dimension cases also satisfy the stated inequality.

## Checks run

This targeted command passed with warnings treated as errors:

```text
PATH="$HOME/.elan/bin:$PATH" LEAN_NUM_THREADS=1 lake build --wfail \
  Formal.MatroidSpectral.UniformRepresentation \
  Formal.MatroidSpectral.PartitionRepresentation \
  Formal.MatroidSpectral.Boundaries \
  Formal.MatroidSpectral.CriteriaExecution
```

A subsequent targeted `lake build --wfail
Formal.MatroidSpectral.CriteriaBitWork` also passed, covering the added
contrast, weighted, materialization, and full selector-cost modules.

The final targeted command also passed:

```text
PATH="$HOME/.elan/bin:$PATH" LEAN_NUM_THREADS=1 lake build --wfail \
  Formal.MatroidSpectral.HeadlineCriteria \
  Formal.MatroidSpectral.CoverPolynomialSize
```

All twelve recorded source hashes were unchanged during that final check.
No project-wide verification, CI inspection, axiom audit, or kernel replay
was performed for this review. The package audit and replay are separate
checks.
