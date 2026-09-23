# Stage 3, round 1 — independent review 3

## Verdict

**No major issues.** The microscopic mutual-information limits, fixed-count endpoint cases, and linear-capacity likelihood arguments are correct. In particular, the manuscript does not infer entropy convergence from total variation or covariance convergence from a central limit theorem. I found one minor clarification concerning the temperature shift of the auxiliary spin–bond measure.

I reviewed all claims in `sections/shared-baths.tex`, checked their stage-1 and microscopic dependencies, and consulted the saved Ramírez-Hernández–Larralde–Leyvraz primary-source text for the introductory attribution. I did not read another current-round review, modify the manuscript, or delegate.

## Minor issue and remedy

**Make the bounded temperature-shift likelihood explicit for the short-range contour phase events.** In the balancing subsection, the paragraph after `eq:shared-balanced-temperature` says the positive phase moment bounds and exceptional-event bound persist because the new conditional likelihood is uniformly bounded. The preceding lemma establishes this directly for spin measures. In the short-range proof, however, these positive phase events are bond events in the Edwards–Sokal extension, whose bond conditional law also changes when the temperature changes.

The claimed preservation is correct, but deserves one explicit sentence to prevent the reader from assuming that the spin likelihood alone reweights that joint measure. If `B=|A|` and `lambda(beta)=log(exp(beta)-1)`, the two Edwards–Sokal joint laws have a likelihood proportional to `exp[(lambda(beta_N)-lambda(beta_c)) B]`. Its support, given by bond/spin compatibility, is unchanged. Since `B <= dN` and the lambda increment is `O(N^(-1))`, this likelihood and its normalized version are bounded above and below uniformly. This supplies the stated moment and exceptional-probability comparison for the original contour events. Adding that explanation resolves the minor presentation gap without changing the conclusion.

## Verification details

### Opposite-phase and fixed-count selection

For opposite phases, tightness puts the total centered energy on the `sqrt(N)` scale, so its squared fluctuation divided by `c_N` tends to zero in the intermediate window. For identical phases its deviation is `+/- Delta_N + O_P(sqrt(N))`; `c_N/N -> infinity` permits the local logarithmic expansion while `N^2/c_N -> infinity` forces suppression. The global bound by one turns conditional convergence into unconditional `L^1` convergence. No interfacial tail estimate is needed.

The limiting opposite-assignment probability is positive for every fixed positive pair of phase weights. Normalization therefore preserves `L^1` convergence. The joint total-variation limit is one minus the original opposite-assignment probability. The conditional product measure has exactly equal one-copy phase weights, even when the original canonical weights are unequal, because the two assignments have identical probability. Disjoint phase supports make the marginal total-variation calculation exact.

For fixed `m`, the same argument works for every count, including `k=0` and `k=m`. The conditioning probability stays positive because `m` and the weights are fixed. The count-conditioned phase assignments are uniform, each one-copy plus probability is `k/m`, and the microscopic phase-conditional reference laws are unchanged. There is no hidden assertion uniform in increasing `m`.

### Finite microscopic KL and the one-bit limit

The proof uses bounded likelihoods relative to the original canonical product, not the differential entropy of either state law. Because `W_N` lies in `[0,1]` and tends to an indicator, bounded continuity of `x log x` gives the joint relative-entropy limit directly. The normalizers stay bounded away from zero, so all marginal likelihoods lie in a common compact interval of `[0,infinity)`. Convergence in `L^1` to their finite-size conditional counterparts therefore also controls their `r log r` integrals, including points at which a likelihood vanishes.

All reference relative entropies are finite: a bounded nonnegative likelihood has integrable `r log r`, including its negative part. The relative-entropy decomposition against a product reference then gives a finite mutual information and the exact chain-rule subtraction used in the paper. This avoids an `infinity-minus-infinity` argument. Substituting the phase weights cancels their dependence and leaves `log 2`.

For the fixed-count extension, the same calculation gives total correlation

`-log p_k - m[f log(f/w_+) + (1-f) log((1-f)/w_-)]`

`= m H(f) - log binom(m,k)`.

At either endpoint this is zero. The marginal likelihood has a zero branch there, but continuity of `r log r` at zero makes the entropy proof valid. When `f=w_+`, the marginal reference divergences vanish and the limiting total correlation is exactly `-log p_k`.

### Optimized joint threshold and balancing

The independent sum of a fixed number of two-atom weak limits has `m+1` distinct support points of positive weight. The stage-1 weak-support theorem therefore establishes both sufficiency and necessity of `c_N >> N^2`, including arbitrary total-energy tuning. No phase Gaussian assumption is used for that statement.

The bounded-spin temperature shift multiplies the lower/upper phase weight ratio by `exp(delta ell)`, giving the displayed negative shift for balance. Within a spin phase, the normalized likelihood tends to one in `L^1`, so the same centered weak fluctuation limits persist. The Gamma/kinetic relative entropy is also correctly oriented: against the old rate it equals `aN[r-1-log r]`, with `r=beta_c/beta_N`, and is `O(N^(-1))`. Thus the complete kinetic laws approach each other in total variation and their fluctuation center changes only by `O(1)`. The only clarity issue is the separate joint spin–bond likelihood noted above.

### Linear capacity: suppression and Gaussian limits

At linear capacity the same-phase reservoir argument tends to a nonzero constant, so a small-argument Taylor expansion would be invalid there. The proof correctly uses the strict inequality for negative arguments and the cutoff or the one-sided quadratic bound for positive arguments. Suppression also holds when a limiting center lands exactly on the cutoff. All discarded canonical tails are controlled by tightness and the weight bound by one.

On opposite phases the exact weight tends uniformly on compact standardized windows to `exp[-alpha(y_-+y_+)^2/2]`. Independence supplies the Gaussian product limit before reweighting. The normalization is `p_O/sqrt(1+alpha V)`. Adding the rank-one precision matrix and inverting it gives

`Sigma = D - alpha v v^T/(1+alpha V)`.

The resulting diagonal terms and squared correlation coefficient in the manuscript agree with this inverse. The statement refers to covariance of the limiting Gaussian; it does not assert convergence of finite-size second moments under only weak hypotheses.

The finite-size microscopic approximation using the original reference and the limiting bounded kernel does converge to the exact reweighted law in full total variation. The `L^1` error follows by restricting to compact phase windows and controlling the complement by tightness. This is stronger than merely writing a Gaussian weak limit, without incorrectly comparing discrete microscopic laws to continuous Gaussian laws in total variation.

### Linear-capacity marginal TV and information

Integrating over the other copy gives

`g_i(y)=(1+alpha v_j)^(-1/2) exp[-alpha y^2/(2(1+alpha v_j))]`.

The identity `g_i/A_gamma = phi_hat_v_i/phi_v_i` is exact. The compact-uniform integration argument uses a finite grid and tightness, so it remains valid for discrete conditional energy laws converging weakly to Gaussians. Global marginal likelihood bounds then control the tails of both the absolute-value and `r log r` integrals. Thus the stated full microscopic marginal TV limit does not need local density convergence.

For balanced weights, each component contributes half its Gaussian total-variation distance. Solving the two density crossing equations gives the displayed `x_i^2`; the formula has the correct factor of two after summing the two phase contributions. The full joint TV expression likewise follows by separating the vanished same-phase sector and the opposite-phase Gaussian sum. Its positive-likelihood threshold and alternative CDF expression are consistent.

For entropy, the joint Gaussian tilt gives the penalty `-alpha V/[2(1+alpha V)]`. The marginal Gaussian divergences have the displayed orientation. Writing `r_i=hat_v_i/v_i`, their variance terms satisfy

`r_- + r_+ - 2 = -alpha V/(1+alpha V)`.

They therefore cancel the joint variance penalty in the chain rule. The remaining fluctuation information is

`(1/2) log[(1+alpha v_-)(1+alpha v_+)/(1+alpha V)]`,

which equals `-(1/2) log(1-rho_gamma^2)`. It is strictly positive because both variances and alpha are positive. The phase-weight terms leave exactly `log 2`. This verifies the full microscopic information limit without relying on differential-entropy continuity.

## Scope and evidence

The introductory historical statement agrees with the saved 2008 source, which describes distinct subsystem phases and switching assignments in thermally coupled negative-specific-heat systems. The new theorem is not attributed to that source. All other checks here were analytic; no finite numerical experiment was used in place of an asymptotic proof. Apart from the explicit joint-measure temperature-shift clarification, I found no unsupported assumption, entropy gap, incorrect endpoint case, or integration inconsistency.
