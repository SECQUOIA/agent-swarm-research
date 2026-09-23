# Stage 3, round 1, independent review 1

**Verdict: no major issues.** I found two minor presentation clarifications. The selection, optimized joint threshold, fixed-count, linear-capacity, and full microscopic entropy results are correct under their stated assumptions.

## Scope and independence

I read all of `sections/shared-baths.tex`, its integration in `main.tex`, the added bibliography entry, and the relevant earlier threshold and microscopic results. I did not read other Stage 3 round 1 reports, edit the manuscript, or delegate. I inspected the retained primary Ramírez-Hernández–Larralde–Leyvraz text concerning opposite subsystem phases and switching. The assessment below concerns correctness and source positioning, not an exhaustive novelty determination.

## Minor corrections

1. **Replace “density-based” in the final paragraph.** The last paragraph describes the positive-variance linear-capacity results as “density-based.” Their hypotheses require only weak Gaussian phase limits, and the proofs expressly permit discrete microscopic energy laws. The reason the pure-spin mean-field example is excluded from the displayed formulas is its zero disordered-phase limiting variance, not the absence of a density. Replace this wording with “positive-variance linear-capacity statements” or equivalent. This avoids contradicting the preceding explanation of how full microscopic total variation is obtained from bounded likelihood integrals.

2. **Make the auxiliary phase-label convention explicit when transferring moment bounds under the temperature shift.** In the balancing subsection, the paragraph asserting preservation of positive phase moments and exceptional mass is correct, but the short-range moment decomposition was constructed on the Edwards–Sokal extension, while the immediately preceding temperature-shift lemma is formulated for spin laws and spin phase events. A short sentence would make the transfer fully transparent: retain the conditional auxiliary bond law at `beta_c` and reweight the joint law by `exp[-(beta_N-beta_c) U_N]`. Its spin marginal is the desired new canonical law, and its joint likelihood is uniformly bounded above and below. Thus the old positive contour decomposition still supplies the required moment and exceptional-mass bounds. The necessity argument separately uses the actual midpoint spin events, whose conditional weak limits persist by the stated lemma. No assertion that the retained auxiliary conditional bond law is the natural Edwards–Sokal law at the new temperature is needed. This is an exposition clarification; the required positive decomposition exists and introduces no additional hypothesis.

## Independent checks

### Intermediate-window phase selection

For opposite labels, the total centered energy is tight on scale `sqrt(N)`, so the exact centered weight tends to one when `c_N/N -> infinity`. For equal labels, its total centered energy is `+/- Delta_N + O_P(sqrt(N))`. Since `Delta_N/c_N -> 0`, the logarithmic Taylor remainder is relatively small even when the leading quadratic term diverges. Thus the log weight tends to negative infinity when `c_N/N^2 -> 0`. The global bound `0<=W_N<=1` converts these conditional probability statements into unconditional mean convergence and handles every tail and cutoff event.

Normalizing gives full-state TV convergence to the product conditioned on opposite labels. Conditioning costs `1-p_O` in joint TV, while its marginal is exactly the equal mixture of the two disjoint phase-conditional microscopic laws. Therefore the stated joint and marginal limits follow, including canonical complete marginals only at balanced reference weights.

### Full microscopic mutual information

The proof does not infer relative-entropy convergence from TV. Instead `W log W` is uniformly bounded and approaches zero in the intermediate window, so the joint divergence converges to `-log p_O`. Marginal likelihoods are uniformly bounded by `1/z_N`; their mean convergence and uniform continuity of `r log r` give the marginal divergence limits. All finite-volume divergences needed for the chain rule are finite. The subtraction gives exactly `log 2`, independently of the positive initial phase weights. The statement that there is no additional limiting microscopic fluctuation information is consistent with the corresponding finite-label information limit.

### Optimized joint threshold

For a fixed number `m>=2` of independent identical copies, weak convergence of one centered energy to two distinct atoms gives weak convergence of their sum to the `m`-fold convolution. This has exactly `m+1` distinct positive-weight support points. The earlier weak-support theorem therefore proves the necessary and sufficient `c_N >> N^2` condition for arbitrary total-energy tuning. No phase central limit theorem, individual limit for each center divided by `N`, or special tuning enters the necessity argument.

### Fixed-count selection

The selected count has a square-root-volume energy deviation, and every other count differs by a nonzero fixed multiple of the extensive gap. Since the number of copies is fixed, the same bounded-weight proof applies. At fixed count, the assignments are uniform because the copies are identical and independent in the reference law. The marginal plus probability is exactly `k/m`. The resulting total correlation is

`-log[binom(m,k) w_+^k w_-^(m-k)] - m D(Bernoulli(k/m) || Bernoulli(w_+))`

which simplifies to `m H(k/m)-log binom(m,k)`. The endpoint counts are valid under the zero-term convention and give zero limiting correlation. The manuscript correctly makes no uniform claim for a growing number of copies.

### Temperature balancing

The canonical spin likelihood for a shift `delta/N+o(1/N)` is uniformly bounded when `U_N/N` is bounded. On each concentrating phase it tends to the constant `exp(-delta u_i)`. This proves both the weight-ratio formula and the conditional full-TV preservation; the sign of the balancing shift is correct. The new target is expressly the canonical law at `beta_N`, not the fixed-temperature unbalanced law.

For an independent kinetic sector, the displayed relative entropy has the correct rate ratio and shape factor. Its order is `N (beta_N-beta_c)^2 = O(1/N)`, giving full kinetic TV convergence. The kinetic phase-normalization factor cancels from the spin weight ratio. The change in mean kinetic energy is order one, so it does not change the square-root-volume weak fluctuation limit.

### Linear-capacity cutoff and limiting Gaussian tilt

Within an opposite assignment, the exact kernel converges uniformly on compact standardized windows to `exp[-alpha(y_-+y_+)^2/2]`. Tightness and boundedness are enough to pass its normalization and bounded integrals to the independent Gaussian limits.

For same-phase assignments the logarithm's argument tends to a nonzero constant, so the zero-centered Taylor expansion would not be justified. The manuscript correctly avoids it. At a negative limiting argument, `x+log(1-x)` is strictly negative. At a positive argument below the cutoff, it is bounded by `-x^2/2`; above the cutoff the weight vanishes. This also handles a center approaching the cutoff itself. Consequently both same-phase assignments disappear without an unproved local-density or tail assumption.

The normalizer is `p_O/sqrt(1+alpha V)`, and rank-one inversion of `D^(-1)+alpha 11^T` gives the stated covariance. The diagonal entries and squared correlation simplify to the displayed formulas, with negative cross covariance and strictly smaller positive marginal variances.

### Full microscopic TV at linear capacity

The finite-`N` approximation retains the actual microscopic reference and replaces only its bounded energy likelihood. Its unnormalized likelihood differs from the exact one in mean, proving full microscopic TV convergence even for discrete systems.

For a phase-`i` first-copy window, convolution with the other phase gives

`g_i(y) = (1+alpha v_j)^(-1/2) exp[-alpha y^2/(2(1+alpha v_j))]`.

The compact uniformity argument using a finite grid and tightness is sufficient. The identity `g_i/A_gamma = phi_(vhat_i)/phi_(v_i)` is exact. Since all marginal likelihoods remain uniformly bounded, weak Gaussian convergence and tightness control the full TV integral, not merely its compact restriction. The phase weights and factors of one half in the general and balanced TV formulas are correct. The Gaussian density crossing value has the stated logarithmic expression.

The joint-TV Gaussian expectation has the correct contribution `(1-p_O)/2` from the suppressed same-phase events. Integrating on the positive-likelihood set yields the stated equivalent normal-CDF expression; its threshold satisfies `exp(-alpha t_gamma^2/2)=p_O A_gamma`.

### Linear-capacity microscopic entropy

Again the proof evaluates bounded microscopic likelihood functions rather than differential entropies. The limiting joint divergence uses tilted sum variance `V/(1+alpha V)`. Each marginal divergence separates into its equal phase-weight contribution and one half the sum of the two Gaussian variance-change divergences. Subtracting the two marginal divergences cancels the initial phase weights and yields

`log 2 + (1/2) log[((1+alpha v_-)(1+alpha v_+))/(1+alpha V)]`.

This is identical to `log 2 - (1/2) log(1-rho_gamma^2)`. The additional term is strictly positive under the stated two positive variance assumptions. Its vanishing as `gamma` increases is a valid limit of the displayed formulas, and the text correctly distinguishes this from the separately proved varying-capacity intermediate regime.

## Source positioning and readability

The 2008 primary paper does show unequal subsystem magnetizations/energies and switching between the exchanged assignments; its figure and associated discussion support the opening attribution. The new section appropriately distinguishes that prior phenomenon from the present exact reservoir scaling and full microscopic distances. I found no unsupported novelty claim in this stage. The earlier proof dependencies are clear, and the distinction between weak Gaussian limits and microscopic TV/entropy statements is carefully maintained apart from the final “density-based” wording identified above.
