# Stage 3, round 1 — independent review 4

## Verdict

**No major or minor issues identified.** The shared-reservoir selection, full-state total-variation limits, entropy limits, fixed-count extension, balancing shifts, and linear-capacity formulas follow from the stated hypotheses. The manuscript correctly distinguishes weak Gaussian fluctuation limits from microscopic total-variation and entropy conclusions.

I read the frozen `sections/shared-baths.tex`, `main.tex`, the relevant threshold and microscopic dependencies, and the new bibliography entry. I independently checked the cited prior phenomenon in the primary text `research/sources/ramirez-etal-2008-zeroth.txt`. I did not consult other current-round reports, delegate, or edit the manuscript.

## Independent mathematical checks

### Intermediate-capacity selection

For opposite assignments the centered sum fluctuates on scale `sqrt(N)`, while for same-phase assignments its center differs by `+/- Delta_N`. The exact centered reservoir weight is globally between zero and one. In the window `N << c_N << N^2`, its limits are consequently one and zero, respectively. Bounded convergence supplies full microscopic `L1` convergence of the weights, including arbitrary canonical tails, and the normalization tends to the positive probability of opposite assignments.

Conditioning on opposite assignments gives each subsystem a half-and-half mixture of its original conditional phase laws. Their disjoint phase supports give the stated marginal distance exactly. The joint distance is one minus the canonical probability of the conditioning event. Both conclusions are full-state statements, not merely statements about the two phase probabilities or energy averages.

### Entropy and one-bit limit

The entropy argument is separate from total-variation convergence, as required on growing or continuous state spaces. Bounded continuity of `W log W` and the positive limiting normalization establish the joint relative-entropy limit. The marginal likelihoods are uniformly bounded, and their `L1` approximation by the exact conditional marginal ratios makes `r log r` uniformly integrable. Subtracting the two marginal divergences yields exactly `log 2`, with all original phase-weight terms canceling. The finite-divergence chain rule is applicable. No convergence of differential entropies or unbounded moments is assumed.

### Optimized joint threshold and fixed count

The sum of a fixed number `m>=2` of independent two-atom macro-energy limits has `m+1` distinct positive-weight atoms. The earlier weak-support theorem therefore gives the optimized `N^2` joint threshold, including necessity for arbitrary total-energy tuning. It requires neither a phase CLT nor fixed limits of the individual uncentered energy centers.

For fixed-count selection, the identical-copy product reference makes all assignments with the chosen count equally likely. The bounded-weight argument applies separately to each of finitely many counts. The relative-entropy calculation gives

`-log p_k - m[f log(f/w_+) + (1-f) log((1-f)/w_-)] = m H(f) - log binom(m,k)`.

This includes the endpoint counts, where the marginal likelihood vanishes on one phase and continuity at zero is essential. The stated exclusion of increasing `m` is appropriate.

### Temperature balancing

The bounded spin-energy-per-particle hypothesis makes the likelihood for a `delta/N+o(1/N)` temperature shift uniformly bounded above and below. Conditional concentration yields the displayed weight-ratio shift with the correct sign. Conditional total variation preserves the weak fluctuation limits, and bounded likelihoods preserve the positive-phase moment and exceptional-mass estimates.

For optional momenta, the Gamma or Gaussian relative-entropy formula is correct for the direction comparing the new rate against the old one. A temperature difference of order `1/N` makes that divergence `O(1/N)`, so Pinsker applies to the full kinetic law. The reference temperature in the reservoir calibration is consistently the shifted temperature. No bounded-likelihood claim is made for the unbounded kinetic energy.

### Linear-capacity covariance and selection

On opposite assignments, direct expansion of the exact physical weight gives the Gaussian kernel `exp[-alpha(y_-+y_+)^2/2]`. The same-phase suppression does not incorrectly use a small-argument expansion: the proof treats negative limiting arguments, positive feasible arguments, and cutoff contact separately. The same-phase assignments disappear even when the limiting upper center meets the reservoir cutoff.

The limiting opposite-assignment Gaussian has precision `D^{-1}+alpha 11^T`. Direct inversion gives the stated rank-one covariance correction. Its marginal variances and squared correlation are correct, with strictly negative correlation and strictly reduced positive variances. The theorem describes the covariance of the limiting Gaussian; it does not infer convergence of finite-system covariance from weak convergence alone.

### Linear marginal and joint total variation

Integrating the Gaussian kernel against the other phase gives

`g_i(y)=(1+alpha v_j)^(-1/2) exp[-alpha y^2/(2(1+alpha v_j))]`.

Its ratio to `A_gamma` equals the ratio of centered Gaussian densities with variances `vhat_i` and `v_i`. The exact microscopic marginal likelihood converges on compact standardized windows to this bounded continuous function divided by `2w_i`. Tightness and a common likelihood bound justify passing to the full TV integral. This works for discrete microscopic phase laws as well.

For balanced weights, the crossing equation gives exactly the printed `x_i^2`. Each individual Gaussian TV is twice the difference of the two normal CDFs at the positive crossing, and the phase weights supply the extra half, giving the printed sum.

For the joint error, the positive-likelihood set contains only opposite assignments and satisfies `|G|<t_gamma`. Integrating its probability under the normalized tilted sum law and subtracting its canonical probability gives the printed CDF expression. The prefactor `p_O` and both square-root variance factors are correct. Its limit as `alpha` decreases to zero is `1-p_O`, consistent with the intermediate-capacity result.

### Linear relative entropy and mutual information

The joint log likelihood is the Gaussian quadratic tilt minus the logarithm of `p_O A_gamma`; its expectation gives the stated joint divergence. Each complete marginal divergence splits into the phase-weight term and the equally weighted Gaussian divergence terms. All limits are justified through bounded microscopic likelihood functions. The Gaussian terms simplify to

`log 2 + (1/2) log[(1+alpha v_-)(1+alpha v_+)/(1+alpha(v_-+v_+))]`.

Equivalently this is `log 2 - (1/2) log(1-rho_gamma^2)`. The extra term is positive and independent of the original phase probabilities. This result concerns the specified centered calibration; the manuscript does not assert an unproved optimization over total-energy choices.

## Distinct numerical checks

I checked the new closed forms independently with `v_-=1.3`, `v_+=0.4`, and `alpha=1.7`:

- The product of the printed covariance and the independently formed precision matrix differed from the identity by at most `2.3e-16`.
- For weights `0.3,0.7`, direct integration of the joint absolute likelihood difference gave `0.6650638561791604`; the CDF formula gave `0.6650638561791602`.
- At balance, direct integration of the two marginal Gaussian density differences gave `0.1233452593485582`; the crossing/CDF formula gave `0.12334525934855822`.
- A two-dimensional, 100-point-per-axis Gauss–Hermite integration of the limiting microscopic likelihood-ratio expression for mutual information gave `0.8564749670233138`, the same as the closed form at printed precision. I evaluated the log ratios directly to avoid numerical underflow in extreme quadrature nodes.
- For `m=5,k=2`, explicit enumeration of the conditional phase assignments gave total correlation `1.0624732420522365`, compared with `1.0624732420522367` from `mH(k/m)-log binom(m,k)`.

These numerical checks supplement the independent derivations; they are not substitutes for the compact-window and bounded-likelihood convergence arguments.

## Scope and source positioning

The 2008 primary paper describes two coupled negative-specific-heat systems taking different phases and exchanging their assignments through finite-size switching. The manuscript accurately credits that phenomenon and restricts its contribution to the exact reservoir-size and full-law/information statements established here. The linear-capacity results explicitly require two positive phase variances; the pure-spin mean-field case is correctly excluded there while remaining included in the intermediate-capacity selection results. No priority claim beyond the inspected comparison is certified by this review.
