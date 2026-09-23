# Independent adversarial review of Stage 3

**MAJOR count: 0. MINOR count: 0. Recommendation: accept the Stage 3 mathematics as written.**

I independently read all of `sections/last-event.tex`, `sections/daughter-comparison.tex`, `sections/critical-last-event.tex`, `appendices/product.tex`, and the Python and JSON supplement. I checked their dependence on the accepted model, fractional-moment estimates, auxiliary-process construction, and logarithmic results. I also checked the coverage map and the relevant primary references. I did not read other current Stage 3 review reports, communicate with reviewers, edit manuscript files, or run shared builds. Unwritten later stages were excluded.

No theorem hypothesis, proof correction, or qualification is required by this review. The following records the concrete challenges and derivations behind that conclusion.

## 1. Controlled first-event and last-event estimates

**Location:** `sections/last-event.tex:22–113`, `thm:last-controlled` and `eq:scalar-tail-factor`.

The fragmentation-only path uses its own current parent size. Since it remains between zero and its finite starting size, compensation for its first moment is justified even with arbitrary measurable parent dependence. Its conditional first moment is `x exp(-(F(s)-F(t)))`. Multiplication by the known count normalization cancels the fragmentation clock and gives

\[
 \mathbb E\left[\frac{N(s)V_s}{m}\right]
 =q\exp[-(B_{\mathrm c}(s)-B_{\mathrm c}(t))].
\]

Consequently the expected hazard up to `T` is exactly `q u_(t,T)`. The proof correctly identifies this hazard with the first future event construction, not with the compensator along the full process after that event. Conditional on the entire fragmentation-only path, an independent exponential threshold gives survival `exp(-H)`. Jensen has the correct direction: concavity of `1-exp(-H)` supplies an upper event bound.

I checked both infinite-horizon cases separately. If total coagulation activity diverges, the fractional coagulation exponent forces the tail to zero. If it is finite, the remaining-activity factor tends to zero, irrespective of the fragmentation clock. If coagulation is identically zero after some time, the remaining-activity factor is exactly zero. If fragmentation vanishes after the restart, the hazard is deterministic and the conditional bound is an equality. These cases use only locally integrable controls and introduce no division by a vanishing rate.

The deduction from `h(t) -> 0` to finite last time is valid; finite-horizon nonexplosion then makes the total coagulation count finite. The scalar factor `c_p` is also correct: its ratio tends to zero at both endpoints, stays strictly below one, and its positive critical point is characterized by `z/(exp(z)-1)=p`. It is accurately described as a sharp scalar domination, not as a sharp temporal exponent.

## 2. Entire-future path coupling and rare window counts

**Location:** `sections/last-event.tex:115–188`, `cor:future-path-TV` and `cor:last-moments-counts`.

The coupling remains legal under parent dependence. The two processes use common fragmentation times and uniform innovations, but after their states differ each evaluates the daughter quantile at its own state. Thus both marginal dynamics are preserved. Agreement until the first future coagulation gives the claimed total variation bound on the entire finite or infinite future. The local Skorokhod space on the infinite interval does not require a positive limit at infinity, so paths approaching zero stay within the specified path-space framework.

The count identities are consistent with almost-sure disappearance. For a fixed window the compensator mean is exactly `b ell`, while finite last time makes the count eventually zero on each path. The event probability remains positive because its expectation is positive. Dividing by that probability yields the stated conditional lower mean; Hölder yields the higher-power lower bound with the correct power `d_p^(1-r)` and exponent `(r-1) chi_p`. Allowing infinite higher moments is essential and is stated. The argument does not infer uniform integrability from bounded first means or claim a distribution for bursts.

The exponential-moment estimate follows from the nonnegative tail integral and includes the atom at zero through the initial `1`. Its strict rate range is correct.

## 3. Classical Borel benchmark

**Location:** `sections/last-event.tex:190–220`, `eq:Borel-last-exact` and `eq:Borel-last-asymptotic`.

The rescaling gives `Q_t=delta X_t/x_0` with `delta=exp(-bt)` and Borel parameter `1-delta`. Pure-coagulation survival from the normalized state is `exp(-Q_t)`, so the Borel generating function gives exactly

\[
 -\log(1-h)=\delta+(1-\delta)h.
\]

Subtracting `h` produces `h^2/2+O(h^3)=delta(1-h)`. Since the tail is already known to vanish, division and taking the positive square root prove `h(t) ~ sqrt(2) exp(-bt/2)`. There is no use of a formal expansion away from its valid regime or an interchange with an infinite Borel mean. The benchmark's faster exponent does not contradict instantaneous sharpness of the fractional-moment inequality.

The underlying formula agrees with equation (3) in [Bertoin (2009)](https://www.numdam.org/article/AIHPC_2009__26_6_2073_0.pdf), checked during the preceding review. The manuscript clearly presents the new tail calculation as a deduction from that classical solution.

## 4. Daughter-law envelopes across all constant rates

**Location:** `sections/daughter-comparison.tex:13–150`, `thm:daughter-envelopes`.

I recomputed the normalized fragmentation-only dynamics: deterministic drift `dY=(sigma-b)Y`, fragmentation at rate `2 sigma`, conditional fraction mean one half, and killing rate `bY`. Its expected state is `q exp(-bs)`, so total expected hazard is `q` for every competing daughter kernel.

The extreme reset and equal-split benchmark hazards both have mean one for every finite `b>0` and `sigma>0`. This is sufficient for their transforms to be continuously differentiable at zero with derivative bound one. A second hazard moment is not available in every regime: for example, the extreme hazard has infinite second moment when `sigma >= 2b`. I specifically checked that the proof never needs that moment. Its small-time generator verification uses only a continuous first derivative and a deterministic finite-horizon state bound.

The benchmark equations have the correct drift, jump, and killing signs. Jensen provides the lower convex daughter average `w(q/2)` and the endpoint chord provides the upper average `(1+w(q))/2`. Combining them with the equations makes the extreme transformed process a supermartingale and the equal-split transformed process a submartingale. The terminal replacement is justified by the first-moment estimate

\[
 \mathbb E\left|e^{-H_s}w(Y_s)-e^{-H_s}\right|
 \le q e^{-bs},
\]

so the comparison does not require monotonicity of normalized size or almost-sure convergence proved elsewhere. It also does not require a stationary competing daughter law.

For the epsilon-daughter sharpness sequence, two independent rate-`sigma` clocks correctly represent the two daughter marks. The hazard before the first small mark converges under domination by the integrable extreme benchmark. The expected normalized size immediately after that mark is

\[
 \frac{q\varepsilon\sigma}{b+\sigma\varepsilon},
\]

which tends to zero. This controls the expected remaining hazard and proves convergence of the full hazard in `L^1`, including when `sigma>b` and normalization grows between jumps. The proof does not discard a potentially important post-reset tail. The reset to zero itself is explicitly excluded from the admissible model; all approximating daughters are strictly positive.

At `sigma=0`, the separately defined hazards equal one and the transforms both equal `exp(-q)`. Substitution into both benchmark equations gives zero. Thus no exponential random variable with zero rate is used, and the two envelopes really coincide for arbitrary inactive daughter laws.

## 5. Sharp overlap constants and accessible states

**Location:** `sections/daughter-comparison.tex:160–201` and `235–274`, `cor:overlap-all-rates` and `cor:critical-envelopes`.

The overlap is exactly `E min(1,Q)` under the paper's total variation convention. Concavity on `[0,1]` and monotonicity beyond one give the lower coefficient `1-w_ext(1)`. Monodisperse data attain normalized state one and overlap one; positive epsilon daughters approach the claimed optimal all-rate lower coefficient. Equal splitting attains its own critical lower coefficient at the same initial population.

The upper-sharpness two-point laws satisfy the mean-one constraint exactly. Their small contribution to the event probability is at most order `epsilon^2`, while the large state's event probability tends to one. Both overlap and future-event probability are therefore asymptotic to `epsilon`. No inadmissible atom at zero or infinite size is used.

The population realization map preserves count `N_0` and mass `m` and gives finite second moment for each finitely supported law. Thus all examples lie within the constructed existence class. An arbitrary positive conditional normalized state can also be included with positive probability using a second atom on the opposite side of one. The sharpness claims range over the allowed initial populations; they do not claim uniform moment bounds along the sharpness sequence. Diverging second moments across that sequence are therefore not a defect.

The constants compare probabilities at an instant over the full initial class. They are not promoted into an optimal large-time exponent for one fixed trajectory.

## 6. Critical product and exact equal-split density

**Location:** `sections/daughter-comparison.tex:203–233` and `sections/critical-last-event.tex:18–97`.

At criticality the holding-time computation produces `S=sum_(k>=1) 2^-k E_k`, including the factor one half from the rate-`2b` waiting time. Thus `E S=1`, `Var S=1/3`, the displayed recurrence, and the first three Taylor coefficients are correct. The finite positive exponential moments below parameter two justify the Taylor expansion and avoid a merely formal moment calculation.

The stated classical normalization is correct: `S` has the law of `I^(1/2)/2` in equations (1.3) and (1.6) of [Bertoin–Biane–Yor](https://monge.univ-eiffel.fr/~biane/q_poisson.pdf). The citation therefore supports the exact product used here, rather than just a similar product.

For the nonlinear generator, the recurrence cancels the direct coagulation loss and leaves `bq E Psi(q+V)`. The pair integrand is bounded by one using the rational envelope. Total variation continuity of the population law, with constant critical normalization, consequently gives a continuous density and a right derivative at zero without a second size moment. The atom at zero is exactly the probability of no coagulations at all, and finite last time ensures that the atom and density exhaust the distribution.

The size Laplace equation has the correct sign: the coagulation contribution is `b(1-phi) partial_z phi`. The first moment justifies the derivative at zero; positive Laplace parameters give bounded integrands and pointwise time differentiation. The mixture formulas follow from the independent exponential-functional variable and Tonelli. They do not close the evolution as a scalar equation in `h` alone.

## 7. General last-event marking, lower time tail, and optimal instantaneous coefficient

**Location:** `sections/critical-last-event.tex:107–204`, `thm:general-last-density` and `cor:critical-moment-bracket`.

The last-event indicator is not predictable, so direct compensation of that indicator would be invalid. The manuscript avoids this problem. It first conditions at each actual coagulation stopping time, replacing the future indicator by the survival probability at the post-event state. Only then does it compensate the function `w_t(q+v)` of time, predictable pre-event state, and partner mark. The finite expected number of jumps on a bounded interval and Tonelli justify the sum. Measurability of the restarted survival follows from the measurable finite-horizon construction and a monotone limit. This argument does not assume differentiability of `w_t` under a time-dependent daughter kernel.

The density formula therefore holds almost everywhere, and local absolute continuity suffices to integrate `h' >= -bh`. The bound uses exactly the critical rational upper survival envelope and lower event envelope. The exponential-moment divergence at `r=b` is justified because the initial event probability is strictly positive and the tail has a positive `exp(-bt)` lower bound. There is no unproved claim at the lower bracket endpoint or inside the unresolved interval.

For sharpness of the instantaneous coefficient, the law with small state `epsilon` and rare-state probability `epsilon^2` has mean one and finite support. Its event probability is asymptotic to `epsilon`; the pair of small states alone contributes asymptotically `epsilon` to the dissipation. The proved upper bound squeezes the ratio to one. The equal-split right derivative at zero then contradicts every smaller uniform coefficient. This is a valid initial-time sharpness argument, not evidence that the long-time tail actually has exponent `b`.

## 8. Scalar power-law obstruction

**Location:** `sections/critical-last-event.tex:213–279`, `prop:scalar-obstruction`.

The counterexample's two atoms are strictly positive, their weights sum to one, and the large atom enforces mean one exactly. Its small atom is smaller than every fixed positive power of `epsilon`. The event probability is asymptotic to `epsilon`, whereas splitting the first coordinate of the dissipation yields

\[
 \mathfrak d(\mu_\varepsilon)
 \le \delta_\varepsilon+\Psi(R_\varepsilon).
\]

For every fixed integer `k`, the first `k` product factors bound the second term by `2^(k(k+1)/2) R^-k`. Choosing `k>alpha` after fixing the proposed power proves the stated vanishing ratio for every `alpha>0`. The proof does not need a simultaneous estimate uniform in `k`, nor does it rely on the later refined product asymptotic.

Each initial measure has moments of every positive order because it has two finite positive atoms. Realization in the existence class makes the initial derivative a genuine solution derivative. Continuity makes a strict violation persist for a positive time interval, so interpreting a proposed differential inequality almost everywhere does not evade the counterexample. The final paragraph correctly limits the obstruction to fixed positive powers; it does not exclude all scalar inequalities.

## 9. Product asymptotic, rational certificate, and supplement

**Location:** `appendices/product.tex:11–127` and `supplement/last_coagulation_exact.py` / `.json`.

Splitting the product at `floor(log_2 q)` gives the displayed quadratic, linear, and periodic terms with the correct signs. Completing the finite sum removes exactly the stated remainder. The two periodic-function series converge uniformly on the closed unit interval, their combined endpoint values agree, and the polynomial part vanishes at those endpoints. Hence the bounded continuous periodic extension is justified, including the case `q=1` with an empty initial finite sum.

The remainder bounds follow from the first three alternating logarithm terms and the three geometric sums. The finite-product tail certificate has exponent `q 2^-k`, with no missing factor of two. The rational lower product bound is positive under the stated condition.

I independently checked, without running the supplement's output-writing step:

- The exact `Fraction` arithmetic at `k=128` satisfies both strict 30-decimal endpoint comparisons.
- The product decomposition and refined remainder bounds hold in direct numerical checks at `q=1, 1.2, 2, 3, 7.9, 8, 10, 100, 100000`; the largest floating residual in the identity was about `1.42e-14`.
- All saved two-point example values agree to relative tolerance `1e-12` with an independent 1024-factor product evaluation.

The decimal rounding proceeds outwards from exact rational endpoints, so it preserves the certificate directions. The fixed numerical examples stay above floating-point underflow in their small atom, and the script checks positivity. The supplement correctly distinguishes illustrative floating computations from certified rational arithmetic. Neither the scalar obstruction nor the asymptotic proof depends on those numerical examples.

## Optional improvements

None needed for acceptance. The current text already makes the crucial distinctions explicit: a restarted future hazard versus the full compensator, actual stopping times versus the last event, accessible finite-support preparations versus boundary benchmarks, and instantaneous sharpness versus an unresolved temporal exponent.

**Final MAJOR count: 0. Final MINOR count: 0. Clean recommendation: accept Stage 3.**
