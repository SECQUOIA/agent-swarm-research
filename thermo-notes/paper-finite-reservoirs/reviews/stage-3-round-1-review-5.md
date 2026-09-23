# Stage 3, round 1: independent review 5

**Verdict: no major issues identified. Two minor clarifications should be made.**

I independently reviewed all of `sections/shared-baths.tex`, checked its earlier theorem dependencies, and checked the cited prior phase-switching observation in the available primary-source text. I did not read other current-round reports, edit the manuscript, or delegate.

## Minor findings

### 1. Explain preservation of the positive contour decomposition under the balancing shift

**Location:** lines 327–332, following the balanced-temperature formula.

The bounded spin likelihood immediately preserves moment bounds on actual spin phase events. The short-range sufficient decomposition, however, was constructed from bond events on the Edwards–Sokal joint space. The text should say how it extends the change of measure to this space, so readers do not implicitly identify the two temperatures' conditional bond kernels.

This is a clarification with a direct proof, not an obstruction to the claimed persistence. One option is to keep the old conditional bond kernel as an auxiliary labeling kernel and multiply the old joint law by the spin likelihood. Its spin marginal is then the new canonical law and its positive decomposition inherits the bounds. Alternatively, use the actual Edwards–Sokal law at each temperature: its unnormalized change of measure is `exp[(lambda_N-lambda_c)|A|]`, with `lambda=log(exp(beta)-1)`. Since `|A| <= dN` and `lambda_N-lambda_c=O(1/N)`, the joint likelihood is uniformly bounded above and below. Conditioning therefore preserves the moment bounds and multiplying by the bounded joint likelihood preserves exceptional-event suppression.

**Fix:** Add one or two sentences specifying either construction. The actual Edwards–Sokal calculation also makes clear that its likelihood is a bond-count likelihood, whereas the spin marginal likelihood is an energy likelihood.

### 2. Describe the linear-capacity restriction by its actual hypothesis

**Location:** final paragraph, “outside the density-based linear-capacity statements above.”

The linear-capacity statements do not assume continuous microscopic densities; they are explicitly proved from weak conditional Gaussian limits and bounded microscopic likelihoods and apply to the discrete short-range spin model. Calling them “density-based” could obscure that distinction.

**Fix:** Replace this phrase with “outside the positive-variance linear-capacity statements above,” or equivalent wording referring to `v_->0` and `v_+>0`. The pure-spin mean-field exclusion itself is correct: the displayed density-ratio, crossing, and correlation formulas assume two positive variances. No extension to a zero variance is required to make the stated theorems valid.

## Mathematical checks and conclusions

### Intermediate reservoir window

- In opposite assignments, the centered total-energy deviation is tight on the `sqrt(N)` scale; in same-phase assignments it is `+/- Delta_N + O_P(sqrt(N))`. Because `c_N/N` diverges, the exact logarithmic expansion is justified in both cases. Its magnitude vanishes in the former case and diverges negatively in the latter when `c_N/N^2` vanishes.
- The global bound on the exact weight converts conditional convergence in probability into unconditional `L^1` convergence to the opposite-phase indicator without any hidden tail assumption. The positive limiting normalizer makes the normalization step valid.
- Conditioning the independent canonical pair on opposite phases gives exactly equal assignment probabilities even when the canonical phase weights are unequal. The two phase supports are disjoint, so both total-variation limits follow exactly from the conditioning limit and contraction under projection.
- The complete-state mutual-information proof separately evaluates joint and marginal relative entropies. Bounded likelihood ratios and continuity of `r log r` justify each limit, including at zero. Substitution into the finite-divergence chain rule gives `log 2`, with the phase-weight factors canceling. The conclusion does not infer entropy convergence from total variation alone.

### Joint accuracy and finitely many copies

- For fixed `m>=2`, independence implies convergence of the centered total energy to the `m`-fold convolution of the two-atom limit. It has `m+1` distinct atoms with positive mass, so the three-support theorem gives the claimed optimized quadratic threshold. This argument requires no conditional central limit theorem.
- The fixed-count argument applies also to `k=0` and `k=m`: the selected canonical count has a positive limiting probability because `m` is fixed, all same-count assignments have equal canonical probability, and the bounded-likelihood entropy proof extends continuously to zero marginal phase weights in the selected law.
- Subtracting the marginal divergences gives `m H(k/m)-log binom(m,k)`. At balanced reference weights this equals minus the logarithm of the canonical count probability; the endpoint counts have zero limiting total correlation. The explicit restriction to fixed `m` is necessary and correctly stated.

### Balancing and microscopic applicability

- The order-`1/N` temperature-change likelihood has the stated phase constants. The resulting phase-weight ratio and the negative sign in the balancing shift are correct. Within a phase, the normalized likelihood converges to one in `L^1`, so every weak fluctuation limit for the same measurable rescaling is retained.
- The mean-field ratio `3 r_*`, the short-range ratio `q`, and the respective latent-heat factors agree with the microscopic stage.
- For kinetic energies, direct evaluation gives relative entropy `aN[r-1-log r]`, with `r=beta_c/beta_N`, hence order `1/N`. The same expression applies to the full quadratic momentum law because its likelihood depends only on energy. The canonical Gamma moment bounds remain uniform for this nearby temperature sequence, and the center changes by only order one.
- Subject to minor clarification 1, the isolated thresholds persist under the balancing shift. The canonical-marginal result consistently targets the specified balanced temperature sequence rather than the original unbalanced canonical law.

### Linear capacity

- On compact opposite-phase fluctuation windows, the exact bath weight converges to `exp[-alpha(y_-+y_+)^2/2]`. On same-phase windows the centered bath argument tends to a nonzero constant. The separate negative-argument and positive-argument/cutoff estimates show suppression without using an invalid small-argument expansion, including when the limiting center lies at the cutoff.
- Tightness and boundedness justify the limiting normalizer `p_O/sqrt(1+alpha V)`. Inverting `D^{-1}+alpha 11^T` gives the displayed covariance, individual variances, and negative correlation. The result is correctly stated as weak convergence of standardized energies, not full-state convergence to a Gaussian measure.
- The proposed finite-size microscopic approximation retains the original reference and replaces only the bounded weight. Its full total-variation convergence follows from `L^1` convergence of those weights and their positive limiting normalizations.
- Integrating out the other copy gives the stated marginal kernel. Weak convergence plus uniform continuity on a compact set gives uniformity in the remaining energy variable, and the bound by one controls the other-copy tail. The globally bounded marginal likelihood then controls the remainder of the marginal total-variation integral.
- I rederived the marginal Gaussian density ratio and the crossing formula. At balance, the total-variation limit is one half of the sum of the two Gaussian distances, which gives exactly the displayed CDF expression. It is strictly positive for finite positive capacity coefficient and positive phase variances.
- The joint total-variation integral has the correct same-phase contribution and opposite-phase normalization. Integrating over the positive-likelihood region gives the displayed second expression with `t_gamma^2=-2 log(p_O A_gamma)/alpha`.
- I independently evaluated the joint and marginal relative-entropy limits. The Gaussian variance terms cancel in the chain rule, leaving `log 2 + (1/2) log[(1+alpha v_-)(1+alpha v_+)/(1+alpha V)]`. This proves the full microscopic mutual-information formula with no reliance on differential-entropy convergence. Its independence of the initial positive phase weights is correct.
- The specified centered calibration and positive-variance assumptions are retained throughout. There is no unsupported claim of optimized marginal accuracy at linear capacity, and the comparison as the fixed capacity coefficient increases is distinguished from a triangular-array limiting theorem.

## Sources and scope

The local primary-source text of Ramírez-Hernández, Larralde, and Leyvraz (2008) supports the introductory attribution: its abstract describes different final subsystem phases under thermal coupling, and the discussion describes finite-size switching of their phase assignments. The present text does not claim to originate that qualitative effect.

No numerical calculation was needed for this stage; the analytic Gaussian integrations, matrix inverse, likelihood normalizations, and information identities were rederived directly. Planned later synthesis or numerical material is outside this review's scope.
