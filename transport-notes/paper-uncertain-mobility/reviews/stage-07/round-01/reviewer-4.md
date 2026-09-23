# Stage 07 independent review — reviewer 4

Snapshot: `d383884b23d489bd685197e179c0e74be518161c6cf0575298800612eae383c0`.

## Verdict

No major issues identified. One minor wording issue should be corrected. The new trial asymptotic arguments, numerical formulations, and restrained interpretation of the numerical evidence are sound. This is a Stage 07 review, not the later whole-manuscript acceptance review.

I checked every file hash in the supplied snapshot manifest; all matched. I read the handoff, introduction, numerical section, discussion, numerical driver and its two imported repository modules, saved data, bibliography and literature audit, and the accepted mathematical dependencies needed for the new statements. I did not read other reviewers' reports or coordinator checks, delegate this review, or modify manuscript sources.

## Minor issue

1. **Name the saved aggregate quantities precisely.** Location: `sections/07-numerics.tex:88–89`, especially “unnormalized responses.” The JSON saves `uniform`, `trial`, and `adaptive_trial` as ensemble-averaged moments, alongside ratios and a scaled trial moment. It does not save the individual offset responses `J_c` or responses before the mobility-budget normalization. Since the preceding text discusses that normalization, “unnormalized responses” can imply either of those absent quantities. Remedy: replace the phrase with “unscaled ensemble moments,” or similarly explicit wording. There is no need to enlarge the data file: the script already reproduces the offset evaluations.

## Independent mathematical checks

### Unrounded mean trial

Write the unrounded and rounded normalizations as `Z_0` and `Z_R`. Their integrable weights obey `|sin s|^(-2/5) >= (|sin s|+R)^(-2/5)` and `Z_R/Z_0 -> 1`. Consequently the budget-M unrounded field dominates `(Z_R/Z_0)` times the rounded budget-M field. Monotonicity in mobility, together with the elementary comparison `J(tD) <= J(D)/t` for `0<t<=1`, gives the desired sharp upper coefficient. The accepted unrestricted lower theorem supplies the other direction. The fact that the unrounded coefficient is infinite at two measure-zero points is harmless for its L1 equivalence class. This verifies the argument at numerical-section lines 32–37 without assuming a pointwise asymptotic valid at the folds.

### Distance-based critical trial

Both normalizations are `4 log(1/R)+O(1)`, and the two positive coefficients have a ratio tending uniformly to one on a sufficiently small fixed fold neighborhood, up to `O(r_*^2)`. On retained annuli `R log(1/M) <= r <= r_*`, this controls the ordinary-root contributions. The remaining fixed outer region costs `O(a_R^(-2/5))`; the leading retained contribution has the additional large logarithm. The accepted inner-annulus and fold-core bounds apply because distance and sine are uniformly comparable there. Taking M to zero and then r_* to zero preserves the sharp critical coefficient. The q=3 computation correctly claims only order optimality and does not assign its coefficient to the attained variational optimum.

### Discrete response and objective certificate

For the circle, reflection, the factor `2h` in the integrated response, and the ensemble factor `(1/2) integral_0^2` are consistent. The quadrature weight `(hi-lo)/4` in the code includes that ensemble factor. Every compared field is normalized to the same explicitly defined discrete mass; the slight uniform-field difference from `M/(2 pi)` is disclosed and vanishes with refinement.

For the uncertain-center problem, face masses `p_i=h D_i` yield conductance `p_i/h^3`. Differentiating `h 1^T A(p)^{-1}1` gives precisely `-(h_{i+1}-h_i)^2/h^2`. The average exterior response is obtained by integrating `1/(x-z)^2` on both exterior half-lines and then over z, giving the stated logarithm and its continuous eta=0 value. No reciprocal tail is missing. Convexity gives the tangent lower bound because the minimum of a linear functional on the unit simplex is its smallest coordinate. This is a certificate for the discretized objective only; the manuscript makes that restriction explicit.

I additionally checked the gradient by a centered finite difference in a nonconstant mass-preserving direction (eta=2, 40 cells, 32 center nodes). The derivative values were `0.6413648989678222` and `0.6413648988353596`, differing by `1.33e-10`.

## Numerical and artifact checks

I independently reevaluated all nine stored center designs, including refinements and the deliberately underresolved example, using the saved mobility vectors. All vectors were nonnegative and had unit mass to floating-point accuracy. Recomputed objectives, tangent gaps, and validation quadrature values agreed with the saved quantities to roundoff (objective relative differences at most about `3e-15`). This checks the actual saved designs, not merely the optimizer's success flags.

I reran the full 32768-cell, 48-node-per-subinterval mean calculation at M=0.001. Its uniform, predetermined, and observed-trial costs reproduced exactly in this environment. I recalculated the circle refinement changes from the saved rows: approximately `1.5841e-4`, `-8.3927e-5`, and `1.1836e-3` relative for spatial doubling at the three smallest budgets. Quadrature-only changes for these predetermined trials were below `1e-8`. The decimal comparisons, tables, and plotted constants agree with the stored evidence. I did not rerun the entire lengthy optimization suite from scratch.

The exact-center computed value lying slightly below the continuum value is disclosed correctly. The larger eta=32 spatial error, the lack of a rigorous support-truncation certificate, and the underresolved quadrature example are all described without turning discrete lower or upper values into continuum bounds. The data do not purport to calculate either the full global crossover or the supercritical variational constant.

I built the manuscript with latexmk in private output directory `/tmp/stage07-r4-85uyV9`. It compiled to 54 pages, with no final undefined-reference, citation, overfull, underfull, or other warning lines. I rendered and inspected both figure PDFs; legends, labels, scales, and the distinction between trial data and continuum coefficients are readable. The README accurately identifies the two repository script dependencies; numerical reproduction is not falsely advertised as independent of the parent repository.

## Physical scope and literature

The introduction and discussion distinguish quenched ensemble moments from particle displacement moments, scalar variational admissibility from physical realizability, and exact observation from noiseless equal-bin observation. The stated transfer uses the accepted fixed-positive-bulk-diffusivity, constant-affinity, nonzero-mean-flow, connected-wall setting. Physical unit restoration is specified in the accepted model section. The generic-fold summary expressly retains an order theorem and does not transfer cosine constants to arbitrary families. No fabrication feasibility, general noisy-sensor theorem, uniqueness of the variational minimizers, or finite-budget optimality of the numerical trials is asserted.

I independently checked primary pages for [Levesque et al.](https://arxiv.org/abs/1211.5224), [Alexandre et al.](https://arxiv.org/abs/2105.06212), and [Buttazzo–Maestre](https://arxiv.org/abs/1002.2770). Their stated model classes and bibliographic identifiers support the introduction's comparisons. I also inspected the [full HTML of Alphonse–Kunštek–Vrdoljak](https://arxiv.org/html/2602.19869v1): its introduction explicitly sets `0<alpha<beta` and places uncertainty in the forcing. Thus the specific positive-conductivity distinction at introduction lines 156–164 is justified and is not incorrectly applied to the cited degenerate reinforcement literature. The [Yüksel–Linder primary record](https://arxiv.org/abs/1009.3824) supports the general observation-channel precedent. An attempted independent retrieval of the Saldi author PDF failed in this review; the manuscript makes only a general contextual claim there, not an unsupported theorem application. The broader source audit appropriately marks access limits and does not claim that its search proves absolute novelty.

## Workflow

The handoff treats this as an author-completed frozen stage awaiting the prescribed reviews and explicitly leaves the separate whole-manuscript review pending. That matches the user's requested sequence. No missing future-stage proof is being waived here; the new asymptotic trial consequences were checked as mathematics in this review. After the minor wording correction, I see no Stage 07 issue requiring another major-issue review cycle.
