# Cardinality review

The determinant implementation agent independently reviewed
`ProfileCardinality.lean`, `TrialLabels.lean`, and `CoverCardinality.lean`.
No mathematical or statement-fidelity defect was found.

The checks covered these points:

- `trialWeights_profile_iff` uses equal base cardinalities to cancel the common
  shift. Both lower and upper signed-label bounds are proved from accepted
  normalized entries and positive mesh width.
- `optionalProfile_injective` translates full profiles by the fixed forced-set
  profile. This is injective on the returned family because every member
  contains that same forced set. The owner-marker interpolation coordinate
  therefore does not enlarge the output-cardinality exponent.
- `profileFamily_card_le` counts optional profiles in a finite box. The identity
  `|B \ F| = q - |F|` follows from actual forced-set inclusion and actual base
  cardinality; it is not an assumption about arbitrary subsets.
- `trialBasisSet_card_optional` obtains profile injectivity from the recovered
  key list's proved absence of duplicates, and obtains base validity and forced
  inclusion from the producer's soundness theorem. Its bound retains the
  optional rank before the simpler rank-based bound is applied.
- `zeroBasisSet_card` returns at most one zero-information representative.
  `spectralBasisSet_card` treats the zero matroid rank separately and sums the
  actual independent factor-label trials for every possible information rank.
  Overlap between trials can only reduce the finite-set cardinality.

The reviewer subsequently authored `CoverPolynomialSize.lean`; that module is
not included in this independent approval. It proves an explicit fixed-
information-dimension polynomial bound, then replaces the factor count by
`p (m + 1)` and optionally replaces matrix rank by `m`. It uses the ceiling of
`1 / η`, not the numerical value of a rational input denominator.

Targeted author validation passed with `lake build --wfail
Formal.MatroidSpectral.CoverPolynomialSize`. Project-wide checks and CI were not
run as part of this review.
