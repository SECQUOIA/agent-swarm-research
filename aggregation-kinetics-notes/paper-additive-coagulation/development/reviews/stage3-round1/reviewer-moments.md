# Independent Stage 3 review: constants, envelopes, and exact observables

**Recommendation: accept Stage 3. MAJOR issues: 0. MINOR issues: 0. The reviewed mathematics is clean.**

I independently reviewed all new mathematics in `sections/last-event.tex`, `sections/daughter-comparison.tex`, `sections/critical-last-event.tex`, and `appendices/product.tex`, together with both supplement files and their dependence on accepted Stages 1 and 2. I did not consult other current Stage 3 reports, communicate with other reviewers, change manuscript files, or run a shared build. I checked the rational certificate and reproduced the saved supplement values without writing any generated file.

## Controlled last-event estimates and rare counts

The first-event construction uses a fragmentation-only path and a separate exponential threshold. This correctly describes the first future coagulation, without incorrectly identifying that path's integrated hazard with the full process's later compensator. Daughter mass conservation gives the factor `exp(-(F(s)-F(t)))`; multiplication by the count normalization cancels fragmentation activity and leaves `exp(-(Bc(s)-Bc(t)))`. Thus the expected first-event hazard is exactly `q u_{t,T}`.

Concavity yields the bound `1-exp(-q u_{t,T})`, and the subsequent fractional bounds and their controlled-clock coefficients are correct. They imply a finite last coagulation time in both cases: diverging total coagulation activity forces the affinity factor to zero, while finite total coagulation activity forces remaining activity to zero. Together with finite-horizon nonexplosion, this gives finite total coagulations. The no-fragmentation example attains the conditional bound. The scalar improvement `c_p` has the stated maximum and unique positive critical point.

The future-path coupling preserves each marginal after divergence by evaluating its daughter map at its own current state. On agreement up to the first coagulation, no distinction is needed between common uniform innovations and common realized fractions. The finite- and infinite-horizon total-variation bounds follow.

For constant rates, `chi_p=b a_p+sigma a_{1-p}` is correct. The exponential moment bound follows from the tail integral, including the possible atom at zero. The count window has mean `b ell`; dividing by the upper bound on its positive-event probability gives the stated conditional mean lower bound. Hölder gives exactly the coefficient and exponent in the higher-moment lower bound. The allowance of infinite higher moments and the conclusion of non-uniform integrability are justified.

The pure-coagulation Borel benchmark has the correct normalization and PGF equation. Substitution of `exp(-delta)` gives the displayed implicit tail equation. Its expansion yields `sqrt(2) exp(-bt/2)`, with no missing time factor.

## Daughter envelopes and sharpness

Both benchmark hazards have mean one for every `b>0` and `sigma>0`, even when their second moments are infinite. The reset benchmark has drift `d=sigma-b` and reset rate `sigma`; equal splitting has the same drift and rate `2 sigma`. The two benchmark equations have the correct drift, jump, and killing signs.

For the reset transform, the convex chord bounds the actual daughter term above by the benchmark term, so the killed-generator expression is nonpositive and the process is a supermartingale. For the equal-split transform, Jensen gives the reverse sign and a submartingale. Taking the terminal expectation gives exactly `w_eq <= w_t <= w_ext`. The limit step uses `E Y_s=q exp(-bs)` and does not require normalized size to be monotone or the competing daughter kernel to be stationary.

The positive epsilon-daughter approximation is valid. Its pre-reset hazard converges in `L^1` by domination by the integrable reset hazard. The expected remaining normalized state at the first small mark is exactly `q epsilon sigma/(b+sigma epsilon)`, which vanishes. This proves convergence of the complete hazard and hence the lower event-probability envelope without introducing an inadmissible zero daughter.

The overlap coefficient `1-w_ext(1)` follows from concavity and is attained in the limit by monodisperse initial data and epsilon daughters. The finite-support population construction correctly enforces the mean-one normalized-state constraint and provides finite second moments. It therefore makes the conditional extremizers accessible within the established solution class.

At criticality the reset hazard is mean-one exponential, and the equal-split hazard is the stated sum of independent exponentials with weights `2^{-k}`. Its mean, variance, recurrence, and Taylor coefficients are correct. The critical rational envelope, universal lower overlap coefficient `1/2`, and equal-split lower coefficient `c_*` follow. The two-atom construction for upper sharpness keeps mean one and yields `h/O -> 1`; it does not rely on an inadmissible atom at zero.

## Exact density, Laplace equation, and lower calendar-time bound

For equal splitting, applying the critical generator to `Psi` cancels the loss terms and leaves `b q E Psi(q+V)`. The pair integrand is bounded by one using the rational envelope. Total-variation continuity therefore supplies the continuous derivative of the tail, including its right derivative at zero, with no second size moment. The atom at zero and the density account for the complete law of the finite last time.

The size-Laplace equation has the correct sign: its coagulation term is `b(1-phi) partial_z phi`. At positive Laplace argument the required size-weighted exponential is bounded; at zero the first moment supplies the right derivative `-1`. The independent-exponential-sum mixture follows by Tonelli and gives the displayed density mixture.

For general critical daughters, the density argument conditions at actual coagulation stopping times on their post-event states. Its projected survival probability is then a measurable function of time, pre-event size, and partner, so the coagulation compensator applies. This establishes the density without differentiability of the time-dependent daughter kernel or conditioning at the non-stopping last time.

The envelopes imply `j(t) <= b h(t)`, hence the lower calendar-time tail. The proposed two-point mean-one law gives `h(0) ~ epsilon` and dissipation at least asymptotic to epsilon; the upper bound already proved gives the matching ratio. Thus the instantaneous coefficient `b` is sharp even for equal splitting. The critical exponential-moment bracket uses `chi_(1/2)=kappa b`, and the lower tail proves divergence also at the endpoint `r=b`. No exact long-time exponent is asserted in the unresolved interval.

## Scalar obstruction and product certificate

The scalar counterexample has strictly positive atoms, exact mean one, and finite positive moments for every fixed preparation. Its tail is asymptotic to epsilon, whereas the dissipation is bounded by the small atom plus `Psi(R_epsilon)`. The first `k` product factors give `Psi(R) <= 2^{k(k+1)/2} R^{-k}`. Choosing `k>alpha` proves the claimed obstruction for every fixed positive power, and derivative continuity extends a strict initial violation to a positive time interval. The conclusion is correctly limited to these uniform power-law bounds.

The large-argument product decomposition is algebraically correct, including the sign of the linear logarithmic term, the periodic polynomial term, and the positive remainder. Completing the finite sum removes precisely `sum_{r>=0} log(1+q^{-1}2^{-r})`. The two endpoint values of the periodic function agree. The bounds `2/q`, `2/q-2/(3q^2)`, and the additional upper term `8/(21q^3)` follow from the stated logarithm inequalities and geometric sums.

I independently executed the integer cross-multiplication check for `P_128(1)`. Both strict terminating-decimal endpoints for `c_*` pass. A read-only execution of the supplement's calculation reproduced the entire saved JSON exactly. Its Decimal rounding directions give outward bounds, and the floating-point two-point evaluations are clearly separated from the rational certificate and from the analytic asymptotic proof.

The normalization `S = I^(1/2)/2` and the cited product identity agree with [Bertoin–Biane–Yor, equations (1.3) and (1.6)](https://monge.univ-eiffel.fr/~biane/q_poisson.pdf). The ordered-generator citation to [Rüschendorf–Schnurr–Wolf](https://arxiv.org/abs/1505.02925) is contextual; the manuscript directly verifies the comparison it uses. The classical product is not presented as a newly discovered special function.

No corrective manuscript change is requested by this review.
