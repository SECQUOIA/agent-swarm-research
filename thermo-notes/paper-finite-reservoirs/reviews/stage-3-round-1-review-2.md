# Stage 3, round 1: independent review 2

Verdict: **no major issues**. All shared-reservoir limit formulas and their microscopic information arguments check out. One minor clarification is needed in the transfer of the short-range positive-contour estimates under the balancing temperature shift.

I read `sections/shared-baths.tex`, `main.tex`, `refs.bib`, the relevant Stage 1–2 dependencies, and the stage author record. For the added attribution I read the retained primary text `research/sources/ramirez-etal-2008-zeroth.txt`, especially the discussion of Figure 3. I did not consult other current-round reviews, edit the manuscript, or delegate work.

## Minor issue

### R2.1 — Identify the augmented measure used when shifting contour-phase estimates

**Location:** Section `subsec:shared-balancing`, paragraph following the balanced-temperature formula: “Their positive phase moment bounds are preserved as well: the new conditional likelihood is uniformly bounded, and any positive exceptional-event bound is multiplied by at most a constant.”

**Reason:** For mean-field Voronoi phases and short-range midpoint events, these are events of the physical spin state, and the displayed spin likelihood immediately proves the assertion. The positive short-range moment and tunneling estimates used for isolated-copy sufficiency, however, were obtained using contour events of the Edwards–Sokal spin–bond space. If the bond kernel is also changed to its natural value at the new temperature, the joint likelihood is not the displayed spin-energy likelihood. The assertion is true, but the augmented measure must be specified so that the argument does not silently equate spin and spin–bond changes of measure.

**Exact remedy, either option:**

1. Explicitly keep the conditional bond kernel at `beta_c` while changing the spin marginal to its canonical law at `beta_N`. This is a legitimate auxiliary positive decomposition for the physical spin law. Its full augmented likelihood is then exactly the bounded spin likelihood already proved, so the contour moment and exceptional-mass estimates persist without further work.

2. If using the natural Edwards–Sokal measure at both temperatures, display its unnormalized likelihood `exp[(lambda_N-lambda_c) B]`, where `lambda=log(exp(beta)-1)` and `0<=B<=dN`. Since `lambda_N-lambda_c=O(N^-1)`, this likelihood is uniformly bounded above and below, as is its normalization. The same conditional moment and exceptional-mass transfer follows.

Either explanation is sufficient. No change to the threshold, balancing formula, phase weights, or subsequent shared-reservoir conclusion is needed.

## Checks of phase selection and microscopic information

- On opposite assignments in the intermediate window, the total centered energy is tight on scale `sqrt N`, so the log weight converges to zero. On equal assignments its leading term is `-beta^2 Delta_N^2/(2c_N)`, which diverges negatively. The expansion is justified there because `c_N/N -> infinity`; the global bound by one controls every discarded tail. Normalization converges to `2w_-w_+ > 0`.

- The conditional product law has an exact half-and-half mixture of the two positive conditional state laws in each marginal. Since the phase events are disjoint, the stated joint and marginal total-variation limits follow with the correct factors. These are complete microscopic distributions, not just their energy laws.

- The full mutual-information proof separately controls relative entropy. `W log W` is bounded and converges to zero in probability, while marginal likelihoods are bounded by `1/z_N`. Uniform continuity of `r log r` on a common bounded interval justifies the marginal divergence limits even though the underlying spaces and phase events vary with `N`. The finite-divergence chain rule yields exactly `log 2` for any positive limiting phase weights.

- The phase-label mutual information tends to `log 2` because its alphabet is fixed and its limiting assignments are uniform and opposite. Thus subtracting the label information from the full information leaves no positive limiting amount of additional information in the intermediate window; the text's interpretation is supported by the two results together.

- For any fixed number of copies, the energy convolution has `m+1` distinct atoms of positive weight after centering. The Stage 1 support theorem therefore gives the optimized `c_N >> N^2` joint threshold. It does not require an unproved individual limit for the absolute phase centers or a fluctuation CLT.

- Fixed-count conditioning selects all assignments of that count uniformly. The marginal weights, joint TV error, and total correlation reduce to the stated binomial and Bernoulli entropy expressions. The continuity at zero used for counts `0` and `m` is valid; those limits have zero total correlation. No growing-copy-count assertion is made.

## Temperature shifts and microscopic applicability

The balancing sign is correct: a positive change in inverse temperature favors the lower energy, so excess lower-phase weight must be removed with a negative shift. On a bounded spin Hamiltonian, the `delta/N + o(N^-1)` shift gives a bounded likelihood with a phase-constant limit. This proves both the limiting ratio and conditional TV convergence, which preserves any conditional fluctuation limit under the same varying centering and scaling maps.

For short-range midpoint phases, the ratio is `q`; for the combined mean-field ordered phases it is `3r_*`. These agree with Stage 2. The midpoint and Voronoi events provide the actual disjoint state-space phase partitions required by this stage. The different positive contour decomposition is needed only when transferring the isolated-copy sufficient criterion, as addressed in the minor issue above.

The kinetic relative entropy has the correct direction and value: for Gamma shape `aN` and rates `beta_N` and `beta_c`, it is `aN[r-1-log r]` with `r=beta_c/beta_N`, hence `O(N^-1)`. The same value follows from the `2aN` Gaussian coordinates. Its TV consequence applies to the complete kinetic law, because the temperature likelihood depends only on total kinetic energy. The mean changes by `O(1)` and the standardized fluctuation limit persists. No bounded-likelihood claim is made for the unbounded kinetic variables.

The plain short-range model has two strictly positive limiting phase variances, and the balancing shift preserves them. The mean-field model has two positive variances only when kinetic smoothing is present. The explicit exclusion of pure-spin mean-field from the nondegenerate linear-boundary formulas is correct; its inclusion in the tightness-based phase-selection results is also correct.

## Linear-capacity calculations

I independently checked the full chain of formulas.

1. On opposite assignments, the compact-window limiting likelihood is `exp[-alpha(y_-+y_+)^2/2]`. On equal assignments the logarithm's argument need not vanish. The exact inequality and cutoff provide suppression for positive arguments, including a center at the cutoff; strict negativity of `x+log(1-x)` handles the negative argument. Boundedness and tightness justify passing to the normalizer `p_O/sqrt(1+alpha V)`.

2. Adding `alpha 11^T` to the product Gaussian precision and inverting gives the stated covariance, reduced marginal variances, and negative correlation. The text correctly asserts weak convergence to that Gaussian, not convergence of arbitrary second moments or microscopic TV convergence to a Gaussian density.

3. Replacing the exact weight by the opposite-phase Gaussian kernel evaluated on the actual finite-system energies gives a valid full-state TV approximation: both weights are bounded, agree asymptotically on compact windows, and have positive limiting normalization. This statement requires no local density limit.

4. Integration against the partner energy gives the stated `g_i`. The identity `g_i/A_gamma = phi_hat/phi_original` is correct. A finite-grid argument plus tightness gives the compact uniform convergence needed to evaluate full marginal TV by weak energy convergence. The resulting integral has the correct weights and factor one-half.

5. At balanced weights, the full marginal distance is one-half the sum of the two centered-Gaussian TV distances. Their crossings obey the displayed `x_i^2` equation, and integration gives the stated sum of Gaussian CDF differences, without an omitted factor of two.

6. The scalar joint-TV expectation includes the same-phase contribution `(1-p_O)/2`. Its equivalent CDF formula follows from the positive-likelihood interval with `t_gamma^2=-2 log(p_O A_gamma)/alpha`. Under the tilted law the sum variance is `V/(1+alpha V)`, giving the first CDF argument; the reference positive-set probability carries the factor `p_O`.

7. The joint KL limit is `-log p_O + (log(1+alpha V))/2 - alpha V/[2(1+alpha V)]`. Each marginal KL is its phase-weight divergence plus the half-weighted Gaussian variance divergences. In the chain rule the phase terms leave `log 2`, the trace terms cancel, and the log determinants leave `0.5 log[(1+alpha v_-)(1+alpha v_+)/(1+alpha V)]`. This is precisely `-0.5 log(1-rho_gamma^2)`, positive for the assumed positive variances and independent of the original phase weights.

All entropy limits are justified through bounded microscopic likelihood integrals. None relies on differential-entropy continuity or on weak Gaussian convergence alone.

## Attribution and review limits

The opening citation to Ramírez-Hernández, Larralde, and Leyvraz is accurate and appropriately narrow. Their original Figure 3 discussion describes the coupled systems exchanging the two phase assignments; it does not establish the present bath-exponent, full-state TV, or microscopic-information results. The manuscript does not attribute those new statements to that work or claim that opposite-phase behavior itself is unprecedented.

This was an analytic and primary-source review, with no new numerical computation or comprehensive new priority search. The absent later synthesis is not a defect of this stage.
