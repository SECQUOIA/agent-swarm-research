# Stage 1, round 1 — independent review 3

## Verdict

**No major issues.** The frozen framework and threshold results are mathematically sound under their stated hypotheses. I found two minor wording/definition issues, listed below. I did not read another current review, edit the manuscript, or delegate this review.

Reviewed files: `main.tex`, `sections/framework.tex`, and `sections/thresholds.tex`. The principal emphasis was the positive-mixture argument, exceptional mass, uniform integrability, the sharp two-phase corollary, and the density-tail alternative. Later planned applications and literature sections were outside this stage's scope.

## Minor issues

1. **Define the secant weight at the cutoff explicitly.** In `sections/framework.tex`, immediately after `eq:secant-h` (line 170 in the reviewed version), the instruction is to set the exponential weight to zero “above the cutoff.” The displayed definition of the logarithm only covers energies strictly below the cutoff, so the value exactly at the cutoff is not explicitly assigned there. This matters formally for the discrete and mixed laws expressly admitted by the paper. The exact marginal and the later positive-sufficiency proof already use the correct convention. Change the phrase to “at and above the cutoff.” This is a local consistency issue, not a gap in the proof.

2. **State strict asymptotic growth accurately in the abstract.** The abstract says the exponent is “larger than the square of the energy scale” and that two-phase fluctuations “require an exponent larger than” the scale product. Mere inequality, or a fixed factor above these quantities, does not suffice. The theorems correctly require a diverging ratio. Replace these phrases with “growing faster than the square of the energy scale” and “growing faster than the product,” or give the corresponding `\gg` conditions. This is a wording correction; the formal statements are clear and correct.

## Independent verification

### Exact weights and calibration bounds

I rederived the physical marginal from the power-law surface density, checked boundedness of its energy likelihood on the entire feasible half-line, and checked the energy/full-state total-variation identity. The distinction between surface heat capacity `k_B c_N` and canonical heat capacity `k_B(c_N+1)` is internally consistent.

For the centered choice, `log(1-y) <= -y` establishes the global weight bound even for arbitrarily negative energies. For the secant choice, the two residual reservoir energies and their inverse temperatures have the displayed values. With `t = beta_N Delta_N/c_N -> 0`, the endpoint slopes are `O(Delta_N/c_N)`, and the curvature is uniformly `O(1/c_N)` between the centers. Subtracting the stated quadratic interpolation upper bound produces a convex function with zero endpoint values, hence a nonpositive function throughout that interval. The exterior bound follows from concavity. The fixed phase-window bound tends to zero because both `Delta_N s_N/c_N` and `s_N^2/c_N` tend to zero.

### Weak-support and two-scale necessity

I checked both exact three-point identities, including the assignment of the coefficient `theta`. The lower bound for `f_theta` is uniform in `theta`, including the regime in which one interpolation coefficient tends to zero. For three macroscopic support points, the selected good events have positive probability and the three log likelihoods tend to zero; no point mass or density is needed. The endpoint identity first forces `c_N q_N` to diverge, and the chord identity then forces `q_N -> 0` and `c_N q_N^2 -> 0`.

For the two-scale argument, `theta_N(1-theta_N)` is of order `s_N/Delta_N`. Combining this with the endpoint identity gives a chord lower bound of order `min(Delta_N s_N/c_N, s_N)`. Since `s_N -> infinity`, its convergence to zero implies the claimed strict scale separation. Positive weights transfer the unconditional good-set probability to each component even if component supports overlap. The exceptional component need not vanish for necessity. The exact two-atom exception also follows directly from the equal likelihood values.

### Positive decomposition, tails, and normalization

The exponential-moment assumption gives tightness of both phase laws on their stated fluctuation scale. The secant tangent estimate is global, not merely a local expansion. With `epsilon_N = O(Delta_N s_N/c_N) -> 0`, it yields `W_N <= exp(epsilon_N |E-e_i|/s_N)` and eventually `E_i W_N^2 <= M`. This proves uniform integrability for the triangular sequence of phase laws, so convergence in probability improves to `L^1` convergence. No local Gaussian limit or positive lower bound on either weight is required for this sufficient argument.

The exceptional contribution is bounded by `delta_N [1 + exp(C Delta_N^2/c_N)]`. The stated condition implies both that this quantity vanishes and that `delta_N -> 0`; neither an unstated moment bound nor a support restriction on the exceptional measure is used. Summing the positive components is legitimate even when they overlap. Normalization then follows from the explicitly proved normalization lemma.

For the sharp corollary, the moment bound implies concentration of the opposite phase on the smaller-than-gap scale. The additional nondegenerate weak phase limit supplies the necessity hypothesis. For sufficiency, `Delta_N^2/c_N = o(Delta_N/s_N)`, while `Delta_N/s_N -> infinity`, so the negative exceptional exponent dominates the positive amplification exponent. The more general sufficient condition with `t_N` is correct, and its lack of necessity is appropriately stated.

### Density-envelope alternative

The endpoint slope estimate follows from the zero secant integral and the curvature bound. On a fixed `R sqrt(N)` window the log weight tends uniformly to zero. In the interior away from those windows the gain is bounded by `C kappa_N N x`. Its ratios to the two density costs are bounded by `C lambda_N/R` and `C lambda_N N^(1/2-alpha)`, respectively, where `lambda_N = kappa_N N^(3/2) -> 0`. The second bound tends to zero throughout the stated interval `alpha in [1/2,1]`, including the boundary `alpha = 1/2`.

The split exponential tail bound is valid. The Gaussian contribution becomes a Gaussian tail after scaling; the remaining integral is finite for fixed positive `alpha` and has a prefactor `N^(-1/2)`. Exterior energies cannot be amplified because the residual weight is at most one there. The local density limits, with their weights summing to one, do imply tightness around the union of the two phase windows. Thus no exterior envelope or implicit global Gaussian approximation is needed.

Finally, midpoint conditioning really does give the positive phase decomposition used for necessity in the density corollary: compact-window convergence gives each half-line weight at least its limiting phase weight; the two limiting weights sum to one, so neither half-line can retain additional escaping mass. Normalizing the local laws gives the claimed conditional Gaussian weak limits. The physical reservoir satisfies the general curvature assumption when `c_N >> N^(3/2)`.

## Scope of the review

The checks above are analytic rederivations; no numerical test was needed to establish these inequalities. I made no claim to have completed a literature-priority audit at this stage. I found no hidden uniform-integrability assumption, missing tail hypothesis, unjustified signed-measure decomposition, or substantive gap in the statements reviewed.
