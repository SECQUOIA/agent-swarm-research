# Independent review: rational PSD factorization and labels

Verdict: **PASS for the factorization and labeling layer.** The code produces
the rational factors it uses; it does not take a factorization certificate as
an additional input. Zero and singular PSD matrices are included. No proof
source changes were needed.

Reviewed files are `RationalSchur.lean`, `RationalFactorization.lean`,
`RationalFactorizationCast.lean`, and `LabeledFactors.lean` in
`formal/Formal/DAGSpectral/`. The separate
[normalization review](normalization.md) covers the subsequent geometric and
rational normalization layer.

## Producer and reconstruction

`rationalLDL` recursively decreases the matrix dimension. At each step it
tests the leading diagonal entry by exact rational equality. A zero pivot
removes that coordinate; a nonzero pivot emits its rational weight and
normalized rational column, then recurses on the explicit rational Schur
complement. There is no square root, pivot-selection oracle, or real-number
comparison in this producer.

Skipping a zero leading pivot is justified by `rationalPSD_zero_row` and
`rationalPSD_zero_col`. The row proof tests the PSD quadratic form on a
rational two-coordinate vector. If the off-diagonal entry were nonzero, an
explicit rational choice would make that form negative. This covers the
case where later diagonal entries are positive: the producer skips the zero
coordinate rather than treating the entire matrix as zero. This is a valid
implementation of the source elimination step even though it does not
permute a later positive pivot to the front.

In the nonzero branch, PSD implies a strictly positive pivot. The explicit
Schur embedding establishes PSD of the residual by congruence. Recursive
factors retain positive weights and nonzero columns under zero extension;
the newly emitted column has leading entry one. Thus `rationalLDL_factors`
establishes the required strict positivity and nonzero-vector conclusions.

`rationalLDL_reconstruct` proves exact entrywise reconstruction of the
original matrix by the emitted weighted rank-one sum. It handles both zero
rows/columns and the Schur identity, without assuming positive definiteness
or a positive lower bound on a nonzero pivot. `rationalLDL_length_le` bounds
the actual output length by the input dimension, and `rationalLDL_zero`
proves that the zero input emits no factors. Dimension zero is included.

`rationalPSD_of_realPSD` restricts the real quadratic-form condition to
rational test vectors and transfers symmetry through injective rational
casting. `rationalLDL_real_reconstruct` therefore applies directly to inputs
whose rational matrices are certified PSD after extension to the reals.
`exists_rational_rankOne_factors` uses the concrete output list for its
witnesses; it does not replace the producer by an abstract existence result.

## Owners and repeated labels

`FactorLabel A` is the dependent pair of an owner and a position in that
owner's actual LDL output. This preserves different factors of the same
owner and numerically equal factors of different owners. Neither equality of
columns nor equality of weights merges labels.

`factorLabel_owner_reconstruct` sums precisely the factors of a specified
owner. `factorLabel_selected_reconstruct` sums all factors whose owners lie
in a selected owner set. There is no one-factor-per-owner assumption.
`factorLabel_card_le` sums the actual per-owner length bounds, and
`factorLabel_prior_atoms_card_le` gives exactly `n*(m+1)` when the prior has
owner `none` and the `m` atoms have owners `some i`.

The selected-owner theorem uses a finite set of owners. Connecting this set
to a path's prior and edges requires the DAG layer's no-repeated-edge fact;
the theorem alone does not certify arbitrary lists with repeated owners.
Owner masks, incompatible owners, factor-span identification with the
information range, and full-trial coverage are outside this review.

## Targeted verification

The following targeted build passed from `formal`, with
`PATH="$HOME/.elan/bin:$PATH" LEAN_NUM_THREADS=1`:

```
lake build --wfail Formal.DAGSpectral.RationalSchur Formal.DAGSpectral.RationalFactorization Formal.DAGSpectral.RationalFactorizationCast Formal.DAGSpectral.LabeledFactors Formal.DAGSpectral.MaxVolume Formal.DAGSpectral.MaxVolumeTrials Formal.DAGSpectral.RatMatrix Formal.DAGSpectral.RangeNormalization Formal.DAGSpectral.NormalizationProducer Formal.DAGSpectral.NormalizationFloor
lake env lean -DwarningAsError=true topics/21-dag-spectral/verification/FactorizationReview.lean
```

The temporary client also passed. Its computational boundary checks used
`native_decide`: `diag(0,3)` emits the single factor `(3,(0,1))`;
`[[1,-2],[-2,4]]` emits `(1,(1,-2))`; zero inputs of dimensions zero and three
emit no factors. Two owners each contributing `diag(1,2)` give four distinct
labels, with two different labels sharing each owner. An initial attempt
using plain `decide` encountered opaque rational inverse reduction; switching
the client to native execution resolved it without source changes. These
are executable regression checks, not additional production proof axioms.

Selected production axiom checks covered `rationalPSD_zero_row`,
`rationalSchur_posSemidef`, `rationalLDL_factors`, `rationalLDL_reconstruct`,
`rationalLDL_real_reconstruct`, and `factorLabel_selected_reconstruct`. Every
declaration reported only `propext`, `Classical.choice`, and `Quot.sound`.
The full topic audit is separate. No project-wide check or CI inspection was
run, and this review makes no claim about polynomial bit work.

Reviewed SHA-256 digests:

```
772a3f1ea8c8b5ca1b1b216367e22c7bab7bae4806ea0f268a1dddac76438a50  RationalSchur.lean
65118c4619a4f579a556c94b6881324230db93dfb8155373fcf966e2501fc2b3  RationalFactorization.lean
280d09003538724ef841486624f0a8b05e88d151dcc1f6fd44dcaef138845bd9  RationalFactorizationCast.lean
da6efe4eb07d250021b2c75f107b70d58beb84398ed9c6d144edf5f10fe49b39  LabeledFactors.lean
```
