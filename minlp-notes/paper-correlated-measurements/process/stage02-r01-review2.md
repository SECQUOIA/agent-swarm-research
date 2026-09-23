# Stage 2 independent review 2

Verdict: **accept this stage; no major or minor correction identified**.

I read `sections/02-locality.tex` and `appendices/locality-scope.tex`, with the
accepted statistical model and macros as dependencies. I used `coverage.md`
to identify the intended boundary of this stage. I did not read other review
reports, edit the manuscript, run producers that overwrite historical data,
or examine the unrelated paper directory. Later optimization and computational
stages are intentionally outside this review gate.

## Findings

- **MAJOR:** none.
- **MINOR:** none.

The generic covariance theorem is conservative but correct under its stated
promises. Its proposed relationship to prior work is appropriately limited.
This assessment does not establish that every possible antecedent has been
located or that the constants are optimal; neither assertion is made by this
stage.

## Reconstructed mathematical audit

1. **Residual transfer and the row lemma.** The proof correctly uses the
   identical spectra of `BB^T` and `B^TB`, rather than placing reciprocal
   factors in the precision sandwich. Congruence and addition of a PSD prior
   preserve the stated factors. For the row lemma I reconstructed the near
   cancellation and the far double sum. The near exponent is `h+2d`, with
   lower limit `L+1-h`, and the stated geometric identity combines correctly
   with the additional far-history sum. Symmetric block-norm row sums give a
   dimension-free spectral norm bound even for unequal block sizes.

2. **General covariance decay (`thm:general-decay`, source lines 426–525).**
   The displayed choice of theta is strictly between rho and one and solves
   the weighted perturbation condition exactly. Both row and column sums are
   required because the weighted conjugate is not symmetric; the manuscript
   includes both, and the resulting norm bound is `m/2`. The Neumann inverse
   estimate has the correct factor order. The selected inverse-block example
   uses the correct direction of the weights. On a local past, multiplying
   the regression row by the increasing weights produces the bound `B_*`;
   dividing each block by its weight gives the desired theta decay. The old
   covariance estimate has the correct convolution and yields `K_*`.
   The Schur variational argument proves the innovation floor `mI` without an
   upper bound on diagonal blocks. Every constant in the final normalized
   error depends only on `C/m` and rho.

3. **Supplied metrics (`cor:decay-metric`).** The two-block PSD condition is
   equivalent to the whitened operator-norm bound for rectangular blocks as
   well as square ones. The residual-normalization transformation is block
   orthogonal, not an arbitrary congruence that could distort the norm.
   Therefore the conclusion really does return to the original residual
   norm and precision. Rational testing can use the original block LMIs and
   does not require rational square roots.

4. **Priority reductions (source lines 827–855).** Independent dummy blocks
   preserve the covariance hypotheses and leave selected conditionals
   unchanged at their original calendar positions. The resulting residual
   covariance is the asserted direct sum. The requirement that the older
   theorem be class-uniform is necessary and is expressly present.
   For diagonal normalization, `||R-D|| <= b_0`, `R >= mI`, and `D >= mI`
   yield both inequalities in the displayed spectral interval. The
   normalized off-diagonal amplitude is indeed `C/m`. These reductions
   properly prevent subset uniformity or large original diagonals alone
   from being presented as a new localization principle.

5. **Broad correctness checks.** The exact Markov path representation and
   forward/reverse telescoping agree with the two possible Schur evaluations.
   The singular-transition continuity argument keeps every covariance SPD.
   The stronger full-block far-pair argument does not require commutativity:
   it transports the cross covariance through an ordered product of
   contractions. The intrinsic partial-observation argument explicitly
   factors through covariance ranges and does not invert a possibly singular
   latent covariance. The spacing recurrence correctly separates the two
   sides of an anchor; this may overestimate a row but cannot underestimate
   it. The separate cooldown condition addresses the `g > L` case.

6. **Appendix.** The covariance-parameter Gaussian gap expression follows
   from conditional score orthogonality and the normal fourth-moment
   identity. The random-intercept example correctly telescopes its first
   `L` terms. The Gaussian KL identity implies the claimed eigenvalue-root
   sandwich; the repeated-pair example separates dimension-free spectral
   error from total KL, not the existence of a KL-to-Fisher implication.
   The explicit pivot precisions give the stated negative supermodularity
   slack. The manuscript distinguishes the thesis claim, the March 2026
   article, and the two pivot conventions.

## Independent checks

`verification/stage02-review2/check.py` constructs a covariance with packet
sizes `[1,3,2,1,2,3,1]`, noncommuting diagonal blocks, heterogeneous diagonal
scales, and off-diagonal blocks meeting an explicit exponential envelope.
It recomputes the genuine local regressions for all 127 nonempty subsets
and all seven windows: **889 cases**. It checks the final error bound,
innovation floors, coefficient bounds, residual/precision spectral identity,
ill-conditioned supplied-metric invariance, dummy-block padding, and the
diagonal-normalization spectrum. It also checks the finite geometric sums
using exact fractions.

All checks passed. The maximum actual-error/bound ratio was 0.062719.
Maximum discrepancies were approximately `1.03e-13` for the transfer spectrum,
`5.59e-11` for the metric-invariant norm, and `2.78e-17` for dummy padding.
These floating checks are independent implementation diagnostics, not a
replacement for the algebraic proof. Results are in
`verification/stage02-review2/results.json`.

An additional exact-fraction calculation confirms the printed illustrative
constants `46/55`, `11/6`, and `193/72`. The first windows below 0.05 and
0.01 are 49 and 58 respectively; the preceding windows have bounds
0.05351275429 and 0.01071698695.

## Primary-source comparison

I read the local literature instructions and checked the relevant source
passages rather than accepting the manuscript's comparison by itself.

- `krishtal2015-localization-of-matrix-factorizations` p.4–5 and p.12:
  Definition 2.2 imposes the GRS condition, and Corollary 5.1 uses the
  indicated inverse-closed algebra. A fixed positive exponential weight
  fails that condition. The manuscript's narrow claim about what that
  corollary alone establishes is correct; it does not deny classical
  exponential-decay results more generally. I also checked the open
  [author manuscript](https://math.ucdavis.edu/~strohmer/papers/2013/matrixfactorization.pdf)
  and [arXiv record](https://arxiv.org/abs/1305.1618).
- `schafer2021-sparse-cholesky-factorization-by-kullbackleibler` p.4 and
  p.9–11: Theorem 2.1 provides fixed-pattern KL minimization; Theorem 3.4
  uses Green's covariance/geometric hypotheses and a logarithmic radius
  involving the number of points; Section 4.1 uses a distinct added-noise
  construction. The exact Theorem 3.4 formula was independently extracted
  from the original PDF, since parts of the stored Markdown omit formulas.
- `benzi2000-orderings-for-factorized-sparse-approximate` Section 4:
  the inverse-factor decay comparison concerns the stated sparse/banded
  matrix setting. `rubensson2021-localized-inverse-factorization` Section 5
  concerns localized iterative inverse factorization. The stage does not
  incorrectly identify either computed factor with the local regression
  factor used here.
- `meyer2015-baxters-inequality-for-triangular-arrays` p.5–7 and
  `inoue2018-baxters-inequality-for-finite-predictor` p.1–3:
  the former uses stationary triangular arrays and spectral assumptions;
  the latter develops multivariate stationary predictor results including
  the FARIMA application. The stated comparison respects those hypotheses.

No correction is required before proceeding on the basis of this review.
