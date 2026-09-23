# Independent review: maximum-volume bases and rational normalization

Verdict: **PASS for the reviewed normalization layer.** The maximum-volume
basis is proved to exist among the actual finite family labels, and its
coordinate estimate applies to the actual rational Gram-inverse normalizer.
The rational normalization producer agrees exactly with that algebraic
construction. The review does not assert complete path-trial coverage.

Reviewed files in `formal/Formal/DAGSpectral/` are `MaxVolume.lean`,
`MaxVolumeTrials.lean`, `RatMatrix.lean`, `RangeNormalization.lean`,
`NormalizationProducer.lean`, and `NormalizationFloor.lean`. I also read the
`rationalMatrixInverse` definition and its equality with the algebraic
inverse in `RationalMatrixArithmetic.lean`; the bit-complexity part of that
dependency was not independently audited here.

## Actual finite-family maximum volume

`max_volume_basis_of_span` first extracts a labeled basis of a spanning
family. Relative to that reference basis, it maximizes the absolute
determinant over all label tuples of the required length. The search domain
is finite and nonempty; the reference tuple has determinant one. The
maximizer therefore has nonzero determinant and is a basis with distinct
labels. Replacing one label by any family label and applying the determinant
coordinate identity proves that every basis coordinate has absolute value
at most one. The maximizing tuple and its coordinate bounds are derived,
not supplied as hypotheses.

`max_volume_basis` applies this argument inside `familySpan`, the actual
span of the family. Thus the dimension is the factor family's true rank,
not the ambient dimension. The argument includes an empty family and a
zero-dimensional span. A determinant relative to any fixed reference basis
differs from Euclidean volume by a common positive factor, so this supplies
the source's maximum-volume coordinate argument in a proper subspace.

`max_volume_scaled_basis` applies it to the weighted family and proves that
removing the nonzero weights preserves independence and the exact span.
`exists_max_volume_rational_trial` uses weights `sqrt(w_j)` only in this
geometric existence proof. From that basis it derives rational-column
injectivity, equality of the selected raw span with the full family span,
and the strict transformed-coordinate bound `<2` whenever
`tau_i^2 w_(b_i)<4`. There is no maximum-volume or square-root oracle in the
rational normalizer.

The bound follows from the exact coordinate identity
`(T(sqrt(w_j)v_j))_i = tau_i sqrt(w_(b_i)) c_ij` and `|c_ij|<=1`.
`reindex_labeled_basis` preserves the basis and coordinate bounds under any
injective enumeration of the same labels, which permits later use of a
deterministically ordered subset. These files do not themselves prove
membership of the selected subset in the actual trial enumerator.

## Rational maps, reconstruction, and exact ranges

For a full-column-rank rational matrix `V`, `gram_isUnit` proves invertibility
of `V^T V` using the rational sum-of-squares quadratic form. The code then
proves `LV=I`, symmetry and idempotence of `Pi=VL`, `TK=I`, and `KT=Pi` for
the stated Gram inverse and nonzero diagonal scales. The rational-to-real
cast lemmas preserve products, transposes, diagonal maps, and multiplication
by vectors. Rational and real column injectivity are proved equivalent.

`reconstruct_retained` uses the actual test `Pi Q=Q`. Symmetry of `Q` and
`Pi` gives `Q Pi=Q`, and direct multiplication proves
`K(TQT^T)K^T=Q`. The input can be singular and the congruence rectangular.
The test is essential: no claim is made for a matrix with information
outside the selected span.

`retained_range_of_normalized_floor` strengthens mere containment to equality
of the actual real linear-map ranges. Its premise that the normalized matrix
dominates the identity gives positive definiteness in the rank-dimensional
space. `TK=I` and the inverse of that middle matrix explicitly yield the
reverse range inclusion. Invertible diagonal scaling then identifies the
range of `K` with that of `V`. The original information matrix need not be
positive definite in the ambient space; the rank-zero case is valid too.

`NormalizationProducer` supplies computable rational definitions. Its inverse
uses the explicit determinant and adjugate expression, and its equality
lemmas connect all four maps and the transformed matrix to the algebraic
definitions. The identities are not merely stated for an unspecified pair
of left-inverse maps. This review does not establish their operation or bit
complexity.

## Forced-label floor

`normalization_forced_floor` proves the actual normalized weighted sum is at
least the identity. An injective tuple of selected labels defines a subset
of all included labels. Nonnegative rank-one summands let the full sum
dominate the selected sub-sum; the concrete normalizer maps its selected raw
columns to the scaled coordinate vectors. The sub-sum therefore becomes
the diagonal matrix with masses `tau_i^2 w_(b_i)>=1`.

Distinct labels are required to avoid counting a single rank-one summand
twice. Distinct owners are not required: multiple selected factors may come
from one owner, and all remain legitimate separate summands. The caller must
connect a complete owner mask to inclusion of these actual basis labels.
This is not assumed proved merely by the abstract finite-set subset premise.

## Targeted verification and limits

The ten-module targeted `lake build --wfail` and the temporary boundary
client both passed; the exact commands and factorization checks are recorded
in [factorization.md](factorization.md). The client's native execution also
checked a proper-subspace example with `V=(2,0)^T`, `tau=2`: the producer gives
`T=(1,0)`, `K=(1,0)^T`, transforms `diag(3,0)` to `[3]`, and reconstructs it
exactly. `diag(0,1)` fails its actual rational range test, as required.

Selected production axiom checks covered `max_volume_scaled_basis`,
`exists_max_volume_rational_trial`, `reindex_labeled_basis`,
`normalizationProducer_reconstruct`, `retained_range_of_normalized_floor`,
and `normalization_forced_floor`. All reported only `propext`,
`Classical.choice`, and `Quot.sound`. No proof sources were edited and no
project-wide checks or CI inspection were run.

Remaining integration includes dyadic-scale production, exact rank tests,
trial enumeration, per-atom magnitude filters, owner-mask execution,
identification of a target's factor span with its information range, and
survival/coverage of every actual target path. Those claims require their
own producer connections; this review does not discharge them conditionally
by assuming a successful trial.

Reviewed SHA-256 digests:

```
f3a6241996e0848b49ec2b71b4b3430aab17891d11cc50b8ca35e2d6ce006e19  MaxVolume.lean
015290bda79b35f5c5f3addfa50e431cd379131664a107bc94f7376222225ffa  MaxVolumeTrials.lean
5c44d90e6333687b185dc93ed7989469efd1979bcd12117cc6da47d1c6f02ff9  RatMatrix.lean
777fc275e3e70d99f2345f66b26cc6efa837b61e83452b1ad2766813c5928232  RangeNormalization.lean
4b6af708594b1d55342dca3ee4d4c2b7a0ffca20aaa70914f0924c7f1fdca2a2  NormalizationProducer.lean
d5de60d624c141bfa202afd938b6f6de8d9bec4fd6cd41762942942851d88cf9  NormalizationFloor.lean
3a335a68ccd2d20075c0769daa07d518d6a5b6fd0568dd810d157ea0f19fb6da  RationalMatrixArithmetic.lean (inverse definition/equality only)
```
