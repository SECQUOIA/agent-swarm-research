# Independent review: path integration and finite-memory transfer

Date: 2026-09-20. Reviewed `PathMatrix.lean`, `TrialApproximation.lean`,
and `Transfer.lean`. Verdict: **PASS** for the normalized-trial integration
and the exact transfer factors. This review does not independently review
`Graph` or the profile-DP modules, which this reviewer authored. It checks
how the separately reviewed DP contract is used by the root-authored
matrix integration. The complete basis-trial producer and its normalization
hypotheses remain separate obligations.

## Signed labels and a common actual representative

`rationalUpperLabels` computes integer floors of rational quotients at the
actual upper-triangular coordinates. Its index conversion uses the concrete
`upperCoordEquiv`, not the noncomputable `upperCoordIndex`. The correctness
lemma connects these executable rational labels to the real floor labels
used in the error proof. Negative entries use mathematical floor, not
truncation toward zero. A client checked a negative off-diagonal entry
`-1/4` at mesh `1/2`, whose integer label is `-1`.

`pathMatrix` includes the prior exactly once and does not round it.
`pathMatrix_entry_close` permits different path lengths, including empty
paths; only the common positive upper bound `N` is required. Equal integer
sums give a difference below `N*h`, rather than `2*N*h`, because each
individual floor residual lies in `[0,N*h)`. No entrywise nonnegativity
assumption is introduced. The common prior cancels algebraically. Symmetry
extends the upper-triangular estimates to the lower triangle with the
correct reversed indices.

`pathMatrix_relativeSandwich` uses `r*N*h=eta` and the quadratic-form
perturbation bound. Its only lower spectral-floor hypothesis is on the
target normalized matrix. This is sufficient for both inequalities: the
absolute perturbation is bounded above and below by `eta*I`, which is then
bounded by `eta` times the target. It does not assume the representative
has a spectral floor as a premise of this step.

`trial_output_relative` obtains one actual path `fs` from `output_complete`,
then obtains its allowed-edge and required-owner properties from
`output_sound`. The same `fs` is used in both PSD inequalities. Equality of
the state-key profile produces equality of every upper-triangular integer
sum. Both path-length bounds come from the actual DAG path predicates.
The rational mesh equals the real mesh after scalar extension. The theorem
therefore connects the concrete DP output to the normalized relative matrix
sandwich; it is not an existential representative unrelated to the output.

The integration assumes positive rank, the target identity lower bound,
and Hermitian transformed matrices. It does not itself prove that some
basis trial supplies those premises, reconstruct the original matrices, or
handle the rank-zero trial. Those are normalization and producer obligations.
Its lack of an `eta<1` premise is mathematically harmless for the sandwich
it proves; downstream kernel preservation and the stated approximation
scheme must still impose `eta<1`.

## Transfer and singular boundaries

`relative_cover_transfer` composes all three supplied sandwiches, using
nonnegative scalar multiplication and transitivity. Division is only by
`1+delta` and `1-delta`, whose positivity follows from `0<=delta<1`.
It gives the exact lower and upper factors

```text
(1-eta)(1-delta)/(1+delta),
(1+eta)(1+delta)/(1-delta).
```

No matrix inverse, determinant, positive eigenvalue, or nonsingularity
assumption is used. This makes the statement valid for singular and zero
matrices as well. The upstream graph sandwich remains an explicit
hypothesis; the theorem does not assert a finite-memory construction for
an arbitrary stochastic model.

`transfer_factors_accuracy` includes the non-strict boundary
`delta=epsilon/8`, with `eta=epsilon/4` and `0<epsilon<1`. It verifies the
source's lower deficit `epsilon/2` and upper excess `17*epsilon/28`.
`relative_cover_transfer_accuracy` then uses PSD scalar monotonicity of the
target to obtain the final `epsilon` sandwich. A client checked the maximal
allowed error boundary and the all-zero matrix transfer. There is no hidden
positive-definiteness assumption in the latter theorem.

## Targeted checks actually run

From `formal/`, with the Elan toolchain on `PATH` and
`LEAN_NUM_THREADS=1`:

```text
lake build --wfail Formal.DAGSpectral.PathMatrix Formal.DAGSpectral.TrialApproximation Formal.DAGSpectral.Transfer
lake env lean topics/21-dag-spectral/verification/PathTransferReview.lean
```

Both final checks passed. The client checked rational negative floor,
common-prior cancellation for unequal lists, the target-only floor contract,
zero-matrix transfer, and the boundary `delta=epsilon/8`. Its initial attempt
to close the rational-floor example by plain `decide` did not reduce the
rational arithmetic; `norm_num` with the definitions established the same
statement. No proof source was changed for this review.

Axiom checks for the entrywise estimate, normalized sandwich, rational-label
bridge, actual output integration, and all three transfer theorems listed
only `propext`, `Classical.choice`, and `Quot.sound`. No project-wide build
or CI inspection was performed. Source hashes were unchanged during review:

```text
PathMatrix         d69f402929361a178a87931764b6b687c505a86a1a98457fbbf767fc43365894
TrialApproximation 74f30e49d37a7941526b5f1be766f36ef584bd8a83a7fc292e1f1e3c5ed65266
Transfer           50a8a1c6a8c6e12579375c29275ccb50b26531ab2b24447c9be380ee26e6f62c
```
