# Stage 2 independent review 5

Reviewer date: 2026-09-13. Scope: `sections/02-locality.tex`,
`appendices/locality-scope.tex`, accepted foundations/macros, and the Stage 2
coverage obligations. I did not read another Stage 2 reviewer report or change
the manuscript. I treated the planned absence of Stages 3–6 as out of scope.

## Verdict and findings

**No MAJOR findings. No MINOR corrections requested. Accept this stage.**

The consolidated arguments are mathematically coherent. The stronger complete-
block far bound and the singular-state partial-observation proof are adequately
developed. The manuscript distinguishes inherited factorization/hull machinery
from its explicit constants and intended certification use. I did not find a
false theorem, missing hypothesis needed for a displayed conclusion, source
misattribution, or coverage omission within this stage.

This is a scoped scientific review, not a formal verification or a claim that
future referees cannot identify further issues.

## Mathematical assessment

1. **Residual transfer and common row argument** (`02-locality.tex:116–195`).
   The precision sandwich has the correct factors `1 ± delta`; reciprocal
   factors would be an error here. The square invertible residual map makes
   the two normalized Gram matrices isospectral. PSD prior terms preserve the
   sandwich without a positive prior eigenvalue. In the near-pair argument,
   the surviving history is precisely `j < t-L`, so the lower distance
   `L+1-h` and both geometric sums are correct. The block-norm row argument
   does not introduce a hidden packet-dimension factor.

2. **Scalar and complete-block bounds** (`02-locality.tex:218–347`). The fresh
   filter must restart with unconditional covariance, as explicitly stated.
   For a far pair the earlier residual is correlated with the state at its
   own time by the earlier local prediction covariance. All updates in the
   later fresh history occur strictly later, and fresh noises are independent
   of that earlier residual. Consequently the exact scalar transport and
   the ordered full-block transport are valid. After noise whitening, each
   full-observation gain and its complement are symmetric contractions;
   matrix commutativity is not needed. The stationary near factor correctly
   uses a lower bound on the first gain, while the general result uses only
   the upper gain bound. No stationary factor is incorrectly assigned to the
   general-block or far-pair terms.

3. **Spacing and graph** (`02-locality.tex:355–424,740–792`). The innovation
   floor counts observations before the target, including the final prediction
   gap. Replacing gaps by their minimum and adding updates up to `floor(L/g)`
   decreases variance, so the stated floor has the correct direction. The
   finite-row recurrence solves a separated-distance support problem even
   when the weights are not monotone. It is used as an upper bound, without
   asserting joint attainability of pairwise majorants. The mask count and
   the cooldown requirement for `L < g-1` address the main feasibility edge
   case. The flow statement appropriately limits arbitrary linking constraints
   to integer exactness.

4. **General covariance decay** (`02-locality.tex:426–563`). The weighted
   similarity perturbation has both row and column bounds, which are needed
   because it is not generally symmetric. The Neumann bound is therefore
   justified. Applying the weighted inverse to the actual regression row gives
   its coefficient bound; the excluded-old-observation bound uses the correct
   ordering of all surviving local indices. The lower Schur-complement floor
   follows from minimization of the covariance quadratic form. Supplied block
   metrics preserve the residual norm by block orthogonal congruence, rather
   than by an incorrect assertion of invariance under arbitrary congruence.

5. **Singular partial observations** (`02-locality.tex:595–728`). The crucial
   contraction follows from `Xi_t >= (1-gamma^2) P_t >=
   (1-gamma^2) Pi_t^-`. The update covariance inequality propagates that
   contraction across skipped and selected times. Both endpoint estimates
   follow from the spectrum of `M`, including zero eigenvalues. The stated
   range factorization is enough to transport a cross covariance from the
   earlier residual's fresh filter through the later filter initialized at
   unconditional `P_s`; it does not silently identify their prediction
   covariances. No inverse of singular latent covariance is required. The
   far coefficient `kappa`, old coefficient `sqrt(kappa*s)`, and regression
   coefficient `kappa` combine to the displayed near coefficient.

6. **Appendix calculations** (`locality-scope.tex:25–61,63–241`). The general
   Gaussian gap Fisher formula differentiates the conditional mean while
   holding the conditioning observation fixed; its transition-derivative
   term and covariance-derivative term are correct. The nonstationary and
   random-intercept examples have the stated covariance/information values.
   Gaussian KL indeed implies relative precision through its nonnegative
   eigenvalue terms. The paired example distinguishes total divergence from
   uniform spectral error without claiming KL cannot bound Fisher information.
   The pivot witness has positive leading minors, the displayed four precision
   matrices and determinant ratios are correct, and the distinction between
   the fixed-order greedy contradiction and convention-independent failed
   supermodularity is essential and correctly stated.

## Independent checks and source scope

The independent script `verification/stage02-review5/check.py` imports no author
or historical implementation. Its results are in the adjacent `results.json`.
It constructs dense covariances directly and recomputes actual selected-history
regressions. A deterministic collection of 18 variable-rank, rotated state
models checked:

| Diagnostic | Passed cases |
|---|---:|
| Complete-block relative residual bound | 216 |
| Improved complete-block far-pair bound | 1,188 |
| Singular partial-packet relative residual bound | 216 |
| Nonuniform observation-coordinate invariance | 216 |

Maximum observed error/bound ratios were 0.2381 for complete blocks and 0.4315
for partial packets. Maximum coordinate-change discrepancy was below `5.6e-15`.
These floating calculations are diagnostics, not rigorous certificates or
substitutes for the proofs. Independently constructed exact rational regressions
also recovered `exp(2 KL) = (25/7,16/7,16/7,1)` and the supermodularity ratio
`175/256`.

I inspected local primary-source text for the following particular boundaries:

- `[[vecchia1988-estimation-and-model-identification-for]] p.4–5`: Section 3.1
  supplies the earlier local-conditional likelihood construction, including
  measurement error. The manuscript credits this rather than inventing a new
  factorization claim.
- `[[atamturk2026-convexification-of-multi-period-quadratic]] p.7–11`: block
  factorization and the principal-inverse polyhedral representation support
  the explicitly inherited Markov hull mapping. The manuscript supplies the
  sensitivity image and handles singular transition limits itself.
- `[[kozdoba2019-on-line-learning-of-linear]] p.7–8`: covariance-norm
  process-noise contraction and forecast approximation after burn-in support
  the qualified comparison at `02-locality.tex:730–738`.
- `[[kaminetz2026-everything-is-vecchia-unifying-low]] p.2`: Definition 1.1
  uses the arithmetic mean raised to rank, consistent with the unnormalized
  Kaporin calculation. The source also credits earlier positive-definite
  fixed-pattern optimality.
- `[[kaminetz2025-everything-is-vecchia-unifying-column]] p.13–14`: I also
  checked the original PDF's Theorem 4.3 and equation (4.10), rather than only
  extracted formulas. The theorem's fixed-order sparsity and claimed
  supermodularity support the precise target of the rational counterexample.
  The manuscript does not transfer that criticism to the distinct 2026 paper.

No third-party source excerpt is retained in the review scratch directory.

## Completeness and presentation

The actual-label map in `process/coverage.md:134–162` is consistent with the
manuscript. All this stage's substantive model families, refinements, prior
reductions, and negative boundary examples are present. The deferred complexity,
approximation-set, certificate-arithmetic, robust, separator, and computational
claims are clearly assigned to later stages. The proofs are self-contained
and use source citations for attribution rather than outsourcing their key
arguments to repository notes.
