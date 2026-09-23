# Stage 3 independent review 3

**Verdict: NO MAJOR ISSUES.** I checked all new barrier-dependence, coupled-barrier, scalar-envelope, nonmonotone-construction, and scalar-localization arguments. Their main claims follow from their stated hypotheses. One minor edit remains. No manuscript files were edited, no fellow reviews were read, and no reviewer communication occurred.

## Required minor corrections

1. **Limit the dyadic encoding statement to weights and tolerance.** `sections/04-barrier-dependence.tex:204–206` says “The data in this corollary are dyadic with the same encoding lengths as before.” An arbitrary fixed scalar barrier may live on an interval with irrational endpoints and have an irrational analytic center, so the entire optimization instance need not have dyadic data. Replace “The data” by “The objective weights and tolerance.” The subsequent sentence about an arbitrary barrier oracle is helpful, but does not by itself clarify the interval/initialization issue. The geometric corollary and its use of exactly the earlier dyadic weights are correct.

## Optional documentation preference

The script docstring at `scripts/verify_scalar_certificate.py:2` correctly refers to Appendix A: `main.tex` includes the scalar certificate before the barrier-profiles appendix. My original report incorrectly asserted the opposite order; this finding is withdrawn. Descriptive wording such as “the scalar-dilation appendix” would avoid dependence on future appendix ordering, but is optional and fixes no present error.

## Mathematical findings

### Normalized scalar profiles and general accuracy

- The inequality `v_f' >= v_f(1-v_f)` is correctly obtained from standard self-concordance and `(f')^2<=f''`. It implies monotonicity, limiting speed one, integrable positive tail, and the translated-step approximation needed for the exact fixed-profile supremum. The integrable negative tail follows from the metric coordinate at a finite interior point.
- Finiteness of the right endpoint follows from `x'(t)=e^{-t}v_f(t)^2`; surjectivity of the positive gradient identifies its limit with the original interval endpoint. The gap-tail identity and its factor-one upper/factor-one-quarter eventual lower bounds are consequently valid.
- The conditions on `p_f` are correct: `p_f'=sqrt(f'')`, `p_f''=f'''/(2f'')`, so `|p_f''|<=p_f'` and `p_f<=p_f'`. The closest accurate vector exists on the closed positive metric orthant. The perturbation argument excluding zero coordinates is valid and needs neither convexity of the transformed feasible set nor uniqueness of the allocation. Necessary equality-constrained multiplier conditions suffice, and their multiplier is positive. The text explicitly avoids the unjustified convexity/uniqueness claim.
- The scalar envelope is applied at `eta=lambda/log 2`, with the inequalities in the correct direction. Its lower comparison ensures the selected center is accurate, while its upper comparison bounds the radial norm of that center. Coordinate monotonicity then bounds the first accurate center.
- The fixed-profile discrete proof preserves the exact weights and tolerance, shifts the activation thresholds by a profile-dependent constant, and has the same endpoint-forcing and rounding estimates as the earlier theorem. Constants may depend on the fixed profile, as the statement says. The positive branch alone is enough because accuracy eventually forces the charged coordinates near the right endpoint.

### Relaxed envelope and smooth counterexample

- In the envelope proof, integrating the upper differential constraint gives the maximal future trajectory `min(1,(1+u)e^q-1)`. The integral comparison bounds the hitting time above, not below. Both solved branches decrease in u, agree to first order at the switch, and attain their envelope values with the stated relaxed trajectory.
- The maximum is strictly below two: the first-branch concavity argument and the positive cubic lower bound on the second branch are valid. Endpoint limits and an interior value above both limits establish attainment. On the first branch B is strictly convex; on the second the displayed exponential inequality implies B''<0. Thus `aB'-B` has one zero, proving uniqueness of the **relaxed-envelope** maximizer. This proof does not assume uniqueness of the different standard-barrier constant c_star.
- Reconstructing p from the piecewise admissible upsilon proves sharpness only in the relaxed almost-everywhere class, exactly as stated. The manuscript correctly does not promote this to a sharp smooth fixed-barrier arclength minimax.
- The globally smooth P_A construction gives a genuine barrier on a finite interval, positive Hessian, third-derivative ratio strictly below two, full gradient range, and parameter between A^2/9 and (A+1)^2. Its metric velocity exceeds one and returns to one, providing actual nonmonotonicity. The translated windows are disjoint after choosing fixed r, delta, B and sufficiently large A. Each window contributes the stated coordinate advance, and the endpoint upper bound gives the sqrt(r) supremum after taking the limits in the specified order. There is no contradiction with a fixed-parameter theorem.

### Canonical and spectral claims

- The universal cube barrier follows from the explicit orthant-simplex polar-volume calculation. The entropic log-partition factorization and inverse-Langevin coordinate are correct, including their continuous values at zero. The scalar entropic gradient norm tends to one, so Chewi's parameter upper bound is tight; products give exact parameter r.
- The general trace-separable Hessian formula follows by polynomial approximation of f'' and continuity of divided differences. It supplies spectral contraction and radial equality for the specified Hessian metrics. Positive Jordan objectives can be aligned and coordinates below the analytic center can be clamped without increasing distance. For even rectangular profiles, the dilation adds only an irrelevant constant when the rectangular dimensions differ.
- The manuscript correctly separates this metric transfer from standard self-concordance of an arbitrary spectral lift. It does not assert that scalar self-concordance automatically transfers to all Jordan/rectangular lifts. Thus the bounded-movement applications do not silently import an unproved property.

### Facet persistence and exact cube parameters

- The full-facet hypothesis is used correctly. Convexity controls the first partial derivative below the collar threshold while other coordinates are arbitrary, so sufficiently large first objective force enters the collar. This step would not follow from a small vertex neighborhood alone.
- The inverse quadratic-form lower bound restricted to a coordinate subset is valid even though G'' has off-diagonal terms. Bounded G' places active coordinates near their positive endpoints; bounded G'' then gives prefix speed arbitrarily close to sqrt(active count). The comparison path stays inside the collar after a fixed initial connector and pays only O(1) extra G length at fixed r. These facts give the Gamma_r limiting lower bound.
- Passing from the terminal-center ratio to the same-accuracy ratio is legitimate: strict objective increase along the central path makes the selected terminal point the first accurate center, and its distance upper-bounds distance to the whole target set.
- The dense Sherman–Morrison expression is correct. The estimates `|B|<=m`, `A<=m/2`, `|t|<r` give the stated 17m/32 correction and parameter at most r. Positive semidefinite quadratic curvature preserves standard self-concordance. Corner asymptotics prove the matching parameter lower bound.
- For radial coupling, the gradient/Hessian formulas are correct; the scalar numerator/denominator difference factors as displayed and is nonnegative for a<=1/2. The added term is a scaled Euclidean-ball barrier. Fixed-parameter corner asymptotics give the exact parameter r. The singular-at-vertices example has exact parameter r+1, and the almost-unused coordinate keeps its extra derivatives bounded along both the chosen path and comparison route, giving its Gamma_(r-1) lower bound.

### New uniform radial comparison

- The global metric estimate is valid: `x^T D^{-1}x<=t/2`, `S>=4lambda+t`, and `(t-4lambda)^2>=0` bound the two relative Hessian contributions by 1/4 and 1/8. These estimates hold for arbitrary cube points, including signed points, not only central points or fixed parameters.
- Differentiating radial stationarity gives the claimed a' equation. The inequality K<=t yields `0<=a'<=1/4` uniformly. The resulting logarithmic scalar-gradient derivatives lie in `[7/10,5/4]`, proving coordinate monotonicity. The scalar velocities are ordered by objective weights. The comparison with the classical prefix norm therefore gives exactly `sqrt(11/8)*(25/14)*Gamma_k` times the standard transformed chord, which is no greater than the full radial metric distance.
- The same-accuracy proof uses both sides of `(4/5)z_i<=q_i<=z_i` correctly. Advancing to `5 eta_U/4` makes the radial center accurate; `H(s+log a)<=aH(s)` bounds its coordinate norm. Applying the earlier standard target-allocation result and global metric domination gives the advertised constant without an extra unproved relation between radial central distance and radial target distance.
- The dyadic radial corollary is uniform when lambda and c vary with r. All profile shift, metric, velocity, and prefix constants used there are absolute. The initial tube controls initial clipped progress; actual accuracy plus scalar contraction forces the terminal label past the charged cutoff. The endpoint distance and path-independent lower bound remain those of the same dyadic tolerance. No coefficient growth depending on lambda or c enters the count.

## Independent verification

Used `/home/sgusev/miniconda3/envs/qipm/bin/python` throughout; installed nothing.

- `verify_barrier_dependence.py` passed: 96 independently solved centers, metric/parameter/a' and theta bounds, finite-difference tangents, three central-arc comparisons, and the numerical relaxed-envelope stationary point. Maximum reported relative tangent error was about 1.23e-9. The computed maximizer/value were 0.6501143834529713 and 1.831856422983876, supporting the expressly numerical decimals.
- `verify_scalar_certificate.py` passed the old c_star bound and all added rational logarithm, Y-series, and radical checks localizing **every** maximizer. The h_1/h_k monotonicity regions and the stationary equation were also checked analytically. No uniqueness of c_star's maximizer is assumed or inferred.
- Added an independent ephemeral numerical calculation at 200 signed random and near-corner points in dimensions 2, 3, 10, 40, with lambda ranging up to 10^6. Direct normalized Hessian eigenvalues obeyed `[1,11/8]`, and the direct inverse-Hessian gradient norm was at most r. The largest observed relative eigenvalue was approximately 1.2499895; the parameter ratio approached one at corners, as expected. This was a supporting check, not a new manuscript dependency.
- Inspected the current final build log; no Warning/Overfull/undefined matches. No shared-output build was run.

## Literature and novelty

Consulted the existing literature instructions and Stage 3 evidence ledger. Independently checked the primary [Lee–Yue author PDF](https://manchungyue.com/nSC.pdf), which explicitly states the universal n bound and cites NN1994 Proposition 2.3.6 for the cube lower bound. Read the relevant local Chewi Theorem 2 and Section 4 tensorization passages; they support the dimension-one entropic self-concordance and the product attribution. Also checked the local Castro–Cuesta section on diagonal parameter-preserving quadratic regularization. The manuscript's historical statements agree with those primary texts.

Opened the primary [Lévy et al. version cited](https://arxiv.org/html/2510.24187v3); its cube specialization is an appropriate citation for the explicit log-partition calculation. The present paper appropriately claims the proved centrality comparisons rather than invention of the universal/entropic constructions, scalar flattening, or parameter-preserving regularization in general.

The new radial matching upper bound is stated only for the explicit family and is not extrapolated to every optimal-parameter or facet-regular cube barrier. The general facet theorem supplies a lower bound only. The C_sc envelope has a narrowly stated relaxed sharpness claim, and c_star localization is distinguished from uniqueness. These are the important novelty/scope boundaries, and the current text preserves them. No targeted search or absence of a matching source should be treated as exhaustive priority certification; final synthesis still has its assigned broader review task.

Front matter, Stage 4, and later synthesis placeholders were excluded as instructed.
