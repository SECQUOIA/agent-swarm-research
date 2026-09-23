# Stage 4, round 1, independent review 5

Reviewer: `/root/stage04_review5`.

Scope: the complete `sections/04-certification.tex` and `appendices/certification.tex`, their accepted locality/graph/spectral-cover dependencies, the coverage map, selected original literature, and the repository's descriptions of the two dense-oracle failures. No other review report was read. No manuscript, historical result, or unrelated paper was modified. Later computation and synthesis stages were not treated as missing deliverables in this stage.

## Verdict

**MAJOR: none.** The certificate inequalities, diagonal-family separation argument, robust normalization directions and approximation factor, and changing-representation Schur proof withstand this review.

**MINOR: two explicit-domain/arithmetic clarifications below.** Neither changes a theorem's intended mathematics or requires a new result.

### MINOR 1: state the cube restriction on the continuous relaxation

Locator: `sections/04-certification.tex:151–156`, inherited by the fixed-point split comparison at lines 188–192.

The definition says only that `mathcal Z` is a specified compact convex relaxation of the feasible indicators. Explicitly require `mathcal Z subseteq [0,1]^n` (and containment of the indicator hull). The virtual-noise map was defined and proved concave on that cube. A compact convex set containing the feasible indicators need not lie in the cube, and the displayed continuous maximum can otherwise be undefined. For example, with a single candidate, `R=a=J0=F=1`, the map is `log(1+z)`; `[-2,1]` is compact, convex, and contains the sole size-one indicator but is not an admissible domain for that maximum.

Recommended fix: write “Let `conv{1_S:S in F} subseteq mathcal Z subseteq [0,1]^n` be a specified compact convex relaxation.” This also makes the later nonnegative `h_i` assumption explicit.

### MINOR 2: distinguish rational model inputs from rational certificate witnesses

Locator: `sections/04-certification.tex:70–78`, together with `appendices/certification.tex:4–11`.

The sentence beginning “For rational model data” says that `N^{-1}` can be recomputed by rational elimination, although the theorem permits any real SPD `N`, and a locality constant may involve an irrational square root even for rational model matrices. Rational model data alone do not make those supplied witness quantities rational. The surrounding discussion clearly intends an exact rational reconstruction, but its arithmetic contract should say so directly.

Recommended fix: state that the exact implementation chooses rational symmetric `N` (or rational `W=N^{-1}`), verifies SPD, and uses a verified rational upper bound `bar delta<1` in place of any nonrational analytic error bound. Alternatively describe certified algebraic/interval evaluation for that bound. The theorem remains valid for arbitrary real witnesses; only the rational checker needs this additional representation statement. Analogous rational choices for `G`, split references, and simplex weights are already described well elsewhere.

## Mathematical review

- The prior-aware local upper matrix follows in the correct direction from the accepted residual sandwich. The tangent constant subtracts `p` and adds the uninflated prior trace correctly. Pricing all feasible paths, including cooldown when its memory exceeds the statistical window, is necessary and explicitly retained.
- The resolvent derivative is correct for nonsymmetric intermediate products and yields the stated symmetric information derivative. The PSD split boundary follows by continuous approximation. Zero weights do not require an inverse of the selection diagonal, and gradients at zero need not vanish.
- Fixed-point split convexity is correctly proved even for indefinite symmetric Hessian directions: the Kronecker difference is PSD. The dual domination `w^T a <= tr(RY)` has the right direction. The common fractional point proves both the pointwise split bound and survival under the specified upper-support cuts, without a minimax exchange. The two-candidate example's information, derivative, trace terms, and log gap are correct.
- The robust certificate prices a single common path. The use of upper standardizer bounds for the incumbent and lower standardizer bounds for the optimum is correct. The zero clipping is valid. The fixed-scenario result uses one block-diagonal spectral representative and legitimately loses two efficiency factors for its same-set estimated normalizers. The sharp tie example and common-mixture example check arithmetically.
- The separator construction treats anchors as nuisance variables with a prior, not observations. The appendix retains the nonzero prior cross terms when anchors are removed. Its change of minimized coordinates, Woodbury calculation, and successive Schur minimization establish the exact identity. Concavity then yields the claimed order `U_A <= U_B`, rather than its opposite. The proof does not confuse a smaller matrix with a principal block.
- Arbitrary rationally rounded nuisance `G` remains valid in the separator support inequality. Count pricing operates on complete schedules; the caution against replacing their hull with expected-count block mixtures is appropriate. The singleton-level comparison uses its actual residual diagonal, including the unanchored last time.
- Signed bridge loadings, covariance, transitions, and endpoint interpretations are correct. The zero-variance anchor reset avoids invalid division. The anchor-prior score is the usual signed gap-transition factorization.
- The logarithm remainder and negative power-of-two endpoint reversal are correct. Signed interval multiplication and clamping before division handle indefinite weight matrices safely. The paper distinguishes arithmetic interval error from the statistical locality error.

## Dense-oracle review

The tridiagonal equations agree with the literal covariance resolvent. Their field-operation count includes the small parameter-information factorization and all gradient quadratics. The covariance innovations and reverse derivative sweep are also exact, including negative correlation and zero weights. The proof of `a/q_i <= 1` uses the original observation residual variance plus nonnegative virtual noise and is valid for admissible splits exceeding the nugget.

The repository notes `research-20260912-structured-dense-oracle.md` and `research-20260912-covariance-dense-oracle.md` confirm that the text is referring to two distinct recorded implementation failures: ill-conditioned latent precision near unit correlation, and cancellation in the first RTS mean-subtraction implementation at large latent-to-nugget ratios. The manuscript properly does not infer a general floating-point error theorem from the repaired formulas. Its parenthesized process-variance product also reflects the recorded left-to-right overflow problem for negative correlation. The Stage 5 performance comparison should retain the repaired implementation and the promised setup/full-cost reporting, as already recorded in coverage; that is a handoff, not a Stage 4 defect.

## Independent exact checks

New code: `verification/stage04-review5/check.py`; result: `verification/stage04-review5/result.json`.

Executed with the existing Python/SymPy environment. The script was written directly from the formulas and imports no manuscript-author or historical audit helpers. It checks:

1. **243 rational dense queries** for signed and zero correlations, every vector in `{0,1/3,1}^4`, a non-diagonal positive prior, and an admissible split exceeding the nugget. Direct resolvent information and every residual row equal the covariance-filter/reverse-adjoint outputs exactly; the bounded scale factor is checked too.
2. **1,296 cross-representation Schur identities**, covering every selected set and all nested anchor pairs in a four-time nonstationary chain with signed transitions and unequal process variances. Prior cross terms are formed from independent covariance calculations.
3. **81 mixture Loewner comparisons** for those nested anchor pairs, using exact principal-minor PSD tests.

All checks passed. These finite checks supplement the proof review; they do not replace a general proof or establish floating-point stability.

## Primary-source checks and novelty scope

After reading `literature/AGENTS.md`, I inspected original PDF text for Kim–Kim (2006), Lemma 1/proof, and Sagnol–Harman (2015), PDF pp. 11–13, Theorem 4.3's subsystem construction; also Levine–How (2013), original PDF p. 8, Section 7/Proposition 7. The local Särkkä–Svensson second-edition text has the cited Kalman and RTS theorem numbers. These support the manuscript's explicit attribution of logdet convexity, subsystem design, and latent-augmentation ideas to prior work.

I also inspected the primary Rybicki–Press preprint, including its tridiagonal inverse and diagonal-noise treatment: [arXiv:comp-gas/9405004](https://arxiv.org/pdf/comp-gas/9405004). This is relevant prior work, as the manuscript states.

A supplementary primary search found [“Nested performance bounds and approximate solutions for the sensor placement problem,” APSIPA 2014](https://doi.org/10.1017/ATSIP.2014.3). Its Section IV, especially definition (44) and Theorems 2–3, develops nested bounds by retaining coordinate sensors while relaxing the other measurements to linear combinations, evaluated through matrix pencils. That is a different representation and criterion from the present Markov-anchor hull. It does not invalidate the manuscript's specifically qualified claim. I do not request another citation merely because both works use the word “nested”; avoid broadening the manuscript claim to all nested sensor-selection bounds during synthesis.

The stage's novelty wording is appropriately narrow. I found no basis here for asserting a first virtual-noise relaxation, a new filter, a new Schur criterion, or a first generic design-support algorithm; the manuscript does not make those claims.
