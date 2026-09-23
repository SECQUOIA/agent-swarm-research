# Stage07 independent review — reviewer 1

Snapshot: `d383884b23d489bd685197e179c0e74be518161c6cf0575298800612eae383c0`.

I checked all 27 files against the SHA-256 values in `snapshot.json`; every hash matched. I read the author handoff, all three new sections, the numerical driver and its imported circle/graded-design routines, saved data and refinements, figures, bibliography, literature audit, and the mathematical dependencies used by the new claims. I did not read other reviewers' reports or coordinator checks and did not change manuscript or numerical files.

**Verdict: no major issues found. One minor clarification should be made before accepting this stage.** The numerical results are illustrative computations with correctly delimited discrete certificates. The two additional asymptotic trial claims follow from the existing variational estimates, for the reasons below; I did not treat the earlier acceptance labels as evidence.

## Finding

### R1-07-1 — Minor: distinguish optimizer uncertainty from the small mesh-refinement changes

**Location:** `sections/07-numerics.tex`, the paragraph beginning “Increasing the grid from 200 to 400 cells” (approximately lines 218–227).

The quoted changes in returned objective values are correct. However, the changes at eta = 0 and eta = 2 are smaller than the available optimization gaps. At eta = 0, the 200-to-400 change is approximately 0.000511, while the two tangent gaps are approximately 0.000667 and 0.001684. At eta = 2, the change is approximately 0.000901, while the gaps are approximately 0.000194 and 0.002195. Thus these two comparisons do not separately resolve the effect of the spatial mesh on the optimized discrete value. The paragraph makes this qualification explicitly for the domain comparison but leaves the same limitation implicit for the first two spatial comparisons. This matters in a section whose stated purpose is to separate error sources.

**Remedy:** Add a short sentence saying that the eta = 0 and eta = 2 spatial changes also lie below the remaining optimization uncertainty and therefore indicate stability of the returned values, rather than a separately resolved spatial error. No new optimization is needed if the claim remains at this level. Alternatively, tighten both optimization gaps below the corresponding refinement changes before interpreting those differences as spatial effects. This is a presentation limitation, not an incorrect computed number or a threat to a continuum theorem.

## Mathematical checks

### The unrounded mean trial

Write the normalized rounded mean design as

`D_R = M (|sin s| + R)^(-2/5) / Z_R`

and the unrounded design as

`D_u = M |sin s|^(-2/5) / Z_0`.

Integrability gives `Z_R -> Z_0`, and, almost everywhere,

`D_u / D_R = (Z_R/Z_0) ((|sin s|+R)/|sin s|)^(2/5) >= Z_R/Z_0`.

The scalar supremum is decreasing in the derivative coefficient. For `0 < t <= 1`, the nonnegative reaction term additionally gives `J(tD) <= t^(-1) J(D)` directly by rescaling the variational test. Hence the mean of the unrounded field is bounded above by `(Z_0/Z_R)` times the rounded mean. It is bounded below by the unrestricted optimal mean at the same mass. The accepted sharp mean equivalent therefore squeezes its coefficient to `K_1`. This comparison is valid for the integrable singular coefficient: it does not require bounded diffusivity or pointwise values at the two fold sites. The trial also has a positive lower bound away from its harmless upward singularities for each fixed positive mass.

### The distance-rounded critical trial

The leading critical normalizing integral is `4 log(1/R) + O(1)` for both the distance and sine forms. On a fixed small fold neighborhood, `sin r = r(1 + O(r_*^2))`, and the same relative comparison holds after adding the common positive cutoff `R`. This supplies the energy comparison needed on the retained annuli. The region outside those neighborhoods contributes `O(a_R^(-2/5))`, whereas the critical total contains an additional logarithm. The inner omitted annuli can be estimated using the same two-root/fold bounds because both local coefficients are uniformly comparable there. Taking the small-budget limit first and the fixed neighborhood radius to zero second gives the identical critical coefficient. The passage does not require the distance formula to approximate sine uniformly over the entire circle. It also does not make the q = 3 trial a sharp optimizer; the text correctly avoids that conclusion.

### Synthesis and physical interpretation

I checked the exponents and regime boundaries in the abstract, introduction and table against their underlying scalings. Uniform quadratic-root contributions have the q/4 power and become nonintegrable at q = 4/3; optimized moving-root allocation has exponent `(6q-4)/(q+4)` and reaches the spatial-integrability boundary at q = 8/5. The critical optimized power and logarithm, supercritical `(2-3q)/7` power, oracle mean `M^(-1/5)`, and information scale `Delta/M^(1/5)` are consistent. The introduction does not assign the cosine constants to generic folds. The information law is stated for the actual equal-bin experiment, rather than arbitrary noisy channels.

The bulk transfer is described at the level established by the comparison: same information, exactly the same budget, fixed positive bulk diffusivity, and an asymptotically negligible uniform addition paid for by reducing the original field. The statements do not presume that an arbitrary pathological coefficient itself defines a physical diffusion or that a finite-grid scalar computation solves the coupled physical problem. The discussion appropriately separates quenched disorder moments from moments of tracer displacement and identifies mobility caps and fabrication lengths as outside the proved class.

## Independent numerical checks

1. **Circle ensemble and budget factors.** Reflection reduces the response to twice the half-wall integral. Combining offset symmetry with the uniform density on `[-2,2]` gives `(1/2) integral_0^2 J_c^q dc`; the mapped Gauss weights in the implementation have exactly this factor. Every sampled profile is normalized to `2h sum D_i = M`. The slight finite-grid change to nominal uniform diffusivity is therefore intentional and converges away under refinement. The known-root trial radius uses mass `M/2` per reflected root. Its replacement by a finite patch near a fold is explicitly an evaluated policy, not the oracle construction used in the theorem.

2. **Independent sparse assembly.** I independently formed the uncertain-center matrices using sparse diagonal assembly and `spsolve`, rather than the driver's banded solver, and reevaluated the saved four main coefficient vectors and the deliberately underresolved vector. The main objective values agreed to relative discrepancies at most about `8.2e-15`; recomputed tangent gaps agreed to absolute discrepancies at most about `2.6e-14`. Saved vectors were nonnegative and had unit mass to floating-point precision.

3. **Derivative and certificate.** Differentiating `h 1^T A(p)^(-1) 1` with a face conductance `p_i/h^3` gives precisely the negative squared finite-difference gradient in the text; no extra cell-width factor is missing. I also checked this with a centered finite difference along a zero-sum simplex direction on an independent small grid: the analytic directional derivative was `32.56209664445731`; a step of `1e-6` gave `32.56209665636`. Convexity implies `F(r) >= F(p) + g dot (r-p)`, whose minimum over the unit simplex is the reported `F(p) - [g dot p - min g]`. This is a global statement for the finite quadrature problem only. The text states that scope and the floating-point limitation correctly.

4. **Exterior contribution.** With zero mobility outside `[-L,L]`, the response there is the reciprocal potential. Integrating its two tails gives `1/(L-z) + 1/(L+z)`. Averaging over the center interval yields exactly `(2/eta) log[(L+eta/2)/(L-eta/2)]`, with limit `2/L`. This adds the response tail exactly but does not remove the restriction on the support of mobility; the manuscript makes the distinction.

5. **Reproduction and saved values.** I reran the complete main circle calculation for q = 1 and M = `1e-9`; its uniform, predetermined, observed-trial, ratio, and scaled-trial outputs matched the saved values. I independently recalculated the percentages and ratios quoted from the saved main/refinement data. I did not rerun the entire SLSQP campaign, so the independent check of those runs is evaluation of their saved feasible fields and certificates, not a claim of independent rediscovery of each optimizer.

6. **Quadrature failure example.** The saved eta = 32 field optimized with 24 center nodes has the reported small finite-quadrature gap, yet its 384-node reevaluation increases the cost from about 10.84053 to 12.09482. The approximately 11.6% discrepancy is real. The text correctly uses it to demonstrate that optimization residuals alone do not control integration over uncertain parameters. The main 400-cell vectors are reevaluated on a finer center quadrature without reoptimizing; this is the appropriate independent check of those particular fields.

7. **Figures and interpretation.** I rendered and visually inspected both PDF figures. Labels, legends, comparison constants, budget direction, and captions are consistent with the data. The critical data are still far from their limiting constant, and the text reports that fact. The eta = 0 finite-grid objective falls below the exact continuum coefficient, providing a useful explicit reason not to present the discrete markers or tangent intervals as continuum bounds. No value of the supercritical variational constant or the full global crossover is inferred numerically.

## Literature and readability checks

I read the bibliography and literature audit and independently inspected the primary 2026 uncertain-design preprint, the primary records/open material for Buttazzo–Maestre, generalized Taylor dispersion, and observation-channel optimization. In particular, the directly inspected [Alphonse–Kunštek–Vrdoljak preprint](https://arxiv.org/html/2602.19869v1) uses two strictly positive conductors and random forcing; the manuscript's narrow comparison with that framework is supported. The [generalized Taylor-dispersion paper](https://arxiv.org/abs/2105.06212) supports the positive attribution of variable diffusion and wall interactions, and the [observation-channel paper](https://arxiv.org/abs/1009.3824) supports the attribution of the general information framework. The paper does not claim to invent those frameworks or the elementary gradient-saturation method.

I also ran additional targeted searches for uncertain optimal diffusion with reaction, random surface-diffusion dispersion optimization, and the proposed moment threshold. They did not identify a direct match to the specific combined theorem package. That bounded search is not proof of global originality. The introduction is appropriately framed around the positive results established here and explicit differences in the admissible class, rather than an unsupported claim that no predecessor exists. The source-access limitations recorded in the audit are acceptable because no detailed exclusion claim is based on an unavailable full text.

The new introductory and discussion material is coherent for a transport audience, and the numerical section explains why each comparison is being made. Apart from R1-07-1, I found no valid minor or major issue requiring correction in this stage. I did not perform a new full LaTeX build during this review; final whole-manuscript review remains separate.
