# Independent representation and recovery review

Date: 2026-09-22. This review covers the representation, restriction,
owner-marker, recovery, assembled cover, and original-input headline. It
does not certify the final combined bit-complexity theorem. The current
validation status is recorded below.

## Scope and outcome

The reviewer read `Representation.lean`, `RepresentationReduction.lean`,
`RepresentationExecution.lean`, `RepresentationCost.lean`,
`RepresentationBitCost.lean`, `Recovery.lean`, `ProfileLabels.lean`,
`ProfileProducer.lean`, `ProfileProducerOracle.lean`, and
`ProfileProducerBases.lean`, `ProfileCardinality.lean`, `TrialLabels.lean`,
`SpectralApproximation.lean`, `SpectralCover.lean`, `CoverProducer.lean`,
`CoverCardinality.lean`, and `Headline.lean` against claims
M01–M04, P01–P06, S02–S03, and C01 in [the frozen inventory](CLAIMS.md). The reviewer did
not author those modules. No semantic correctness defect was found in the
reviewed interfaces.

The reviewer authored `DeterminantProfiles.lean` and the new
`DeterminantProfileBounds.lean`; this review is **not** independent review
of those two modules. The assembled review must cover them separately.

## Findings

1. **Original bases have a precise meaning.** `IsColumnBase A B` requires
   independent original columns and cardinality `A.rank`. The determinant
   predicate `IsBase` instead uses the row count of its supplied matrix.
   These agree after preprocessing by
   `reducedRepresentation_isBase_iff`. It would be incorrect to apply the
   unreduced determinant predicate directly to a matrix with redundant
   rows; the theorem states the necessary reduction explicitly.
   `reducedRepresentation_mulVec_eq_zero_iff` preserves every column
   dependence, not only full-size determinants. The transposed row scan
   constructs an original column base, and
   `reducedRepresentation_bases_nonempty` proves existence without a
   nonempty-base assumption.

2. **Restriction never lowers the rank used by a support query.**
   `zeroColumns` has the same `Fin q` row index as the input. Its equality
   with `retainedRepresentation` connects the executable matrix to the
   support theorem for original `q`-element bases. Deletion changes only
   the retained columns. A rank-deficient retained set therefore has no
   positive target coefficient. `supportOracle_rejects_small_ground`
   separately proves rejection when fewer than `q` columns remain.

3. **Owner forcing is exact set inclusion.** The marker coefficient is
   the cardinality of `B ∩ forced`. Requiring `forced.card` is equivalent
   to `forced ⊆ B`. `markedProfileOracle_spec` additionally enforces
   `B ⊆ ground`; a removed owner cannot silently disappear from the
   condition. When `forced.card > q`, the executable oracle returns
   false and proves that no target can exist. Dependent forced sets are
   also infeasible because a target must be an actual base containing
   them. Owner sets are finite sets, so repeated factor owners are
   counted once. The creation of that owner set from factor labels is
   outside this review.

4. **No assumed profile oracle remains at the concrete interface.**
   `profileCoefficientOracle` uses executable tensor interpolation of
   rational determinant evaluations. `profileDeterminantValue_eq` and
   `profileCoefficientOracle_spec` connect those evaluations to the
   formal generating polynomial and its exact support. The generic
   recovery theorems accept an oracle specification, but
   `markedProfileOracle_spec` supplies it for the concrete computation.
   The field is the rationals throughout; neither a finite-field test nor
   floating-point positivity is substituted.

5. **One deletion pass returns an actual target base.** The scan preserves
   support, and each surviving processed column is indispensable.
   Monotonicity of support makes a previously rejected deletion remain
   impossible after later deletions. Since the scan covers the original
   ground, the final set equals a contained target member. It is not
   merely a larger set that contains a base. The concrete scan makes
   exactly `m` deletion calls; its rank-aware wrapper makes at most `m`.

6. **Rank-zero handling is guarded correctly.** The determinant of the
   empty matrix is one and the only rank-zero base is empty.
   `recoverBasisAtRank 0` returns the empty set without deletion calls.
   Its target theorem requires initial support. The producer performs
   the support test before calling recovery, so an impossible marked
   target does not become an accepted empty base. The full producer must
   still distinguish matroid rank zero from zero information with a
   potentially nonzero prior; that distinction lies beyond these modules.

7. **The marker does not increase the output grid dimension.** Candidate
   enumeration scans ordinary coordinates and fixes the marker at
   `forced.card`. Interpolation uses the additional marker variable and
   the safe uniform bound `max (q * W) q`. This bound is larger than
   necessary but remains polynomial at fixed information dimension.
   The new `determinantPolynomial_owner_degree` separately establishes
   the sharper marker bound `forced.card` required by P03.
   `optionalProfile_bound` establishes the optional coordinate bound
   `(q - forced.card) * W`. For optional rank zero,
   `base_eq_forced_of_optional_rank_zero` gives exact equality with the
   forced set; no strict zero-width remainder estimate is used.

8. **The row scan now has an executable refinement.**
   `selectRowsExecuted_correct` connects the scan using
   `Elimination.rationalDeterminant` to the semantic Gram-determinant
   scan. `rowSelectionRun` records the actual queried row sets and proves
   there are exactly `a` queries. The row-selection correctness argument
   does not enumerate row subsets or assume a row-basis oracle.

9. **The concrete profile producer discharges the generic interface.**
   `profileBases` supplies `markedProfileOracle` to candidate enumeration
   and deletion. `profileBases_sound` returns the exact base, ground, and
   owner guarantees. `profileBases_complete` explicitly requires that the
   supplied coordinate list covers every coordinate; it does not claim
   completeness for an incomplete list whose omitted entries default to
   zero. Deduplication is by attained ordinary profile and preserves one
   representative of each key. It cannot replace a profile by an unattained
   point. The empty-coordinate case and repeated coordinates cause no
   correctness problem, although the final complexity bound must use the
   actual coordinate-list length.

10. **The original-input bridge is assembled.** `representedSpectralCover`
    computes `rowReductionRepresentation A`, obtains PSD factors from
    `producedData`, and invokes the concrete spectral base producer.
    `columnBases_eq_reduced` connects its semantic domain to the original
    supplied matrix. `representedSpectralCover_sound` returns
    `IsColumnBase A B`, and `representedSpectralCover_nonempty` derives
    nonemptiness from a proved original base. No full-row-rank assumption
    is imposed on the input.

11. **All three zero-rank cases remain distinct.** The original matroid
    rank-zero branch returns `{∅}` even with a nonzero PSD prior. For
    positive matroid rank and zero information rank, `zeroBasisSet`
    requires zero prior and searches only zero-information elements using
    the unchanged original row count. Optional rank zero means that a
    feasible base is exactly its forced set. None of these cases accepts
    a smaller-rank restricted base or invokes a strict zero remainder.

12. **The final spectral and cardinality interfaces are discharged.**
    `spectralBasisSet_isRelativeCover` supplies both the zero-information
    representative and concrete positive-rank profile completeness to
    the generic spectral theorem. The latter invokes the already proved
    maximum-volume normalization result; it is not an assumed trial
    oracle. `representedSpectralCover_complete` states both PSD bounds
    for one actual original base and gives the same representative exact
    kernel and range when `0 < eta < 1`. The cardinality proof injects
    the deduplicated full profiles into optional profiles after removing
    the shared forced contribution. It obtains the stated optional-rank
    trial bound and the displayed sum of binomial trial counts. The
    extra marker contributes interpolation work, but no extra factor in
    the output count.

13. **Row-preprocessing arithmetic is linked to its execution.**
    `rowReductionRun` materializes Gram matrices and records determinant
    operations and operand pairs. `rowReductionRun_operands_length`
    equates trace length with the operation counter;
    `rowReductionRun_operands_bits` bounds all actual operands by a
    polynomial expression in variable dimensions and the input width.
    `rowReductionBitRun_work_le` bounds the schoolbook arithmetic observer
    plus its stated finite-storage/access overhead. The reduced matrix
    copies original entries, so their bit bound is unchanged. This is
    evidence for the stated execution model, not a Lean runtime or
    machine-instruction bound.

## Remaining review boundary

The mathematical original-input/base/spectral/cardinality integration gaps
identified in the intermediate review are closed by the assembled modules.
No semantic correctness defect was found in this final read. The reviewed
source snapshot passed a warning-free targeted build, and all 17 reviewed
source hashes remained unchanged across that check.

The combined cost of factor preprocessing, every trial, determinant
queries, interpolation, deletion, deduplication, storage, and final witness
production is a separate review obligation. This report does not infer
that whole-algorithm bound from the local row-preprocessing bound. The
independent review of the determinant-profile modules authored by this
reviewer also remains assigned to a different reviewer.

## Checks run

The final targeted command passed with warnings treated as errors:

```text
PATH="$HOME/.elan/bin:$PATH" LEAN_NUM_THREADS=1 lake build --wfail \
  Formal.MatroidSpectral.Headline \
  Formal.MatroidSpectral.RepresentationBitCost
```

[The source record](REVIEW-REPRESENTATION-SOURCES.json) gives SHA-256 hashes
for all 17 reviewed modules and records equality before and after the
successful check. Its scope exclusions are part of the review result.

Earlier intermediate checks covered determinant-profile bounds,
representation reduction, recovery, and the concrete oracle. During
concurrent development, later checks exposed a subtype coercion in a new
representation lemma and missing simplification/lint fixes in the headline.
The authors corrected those elaboration issues, and the final check above
passed. No semantic counterexample was found.

No project-wide check, CI inspection, axiom audit, or kernel replay was
performed as part of this review. The package's final verification must
record its separate axiom audit and module kernel replay.
