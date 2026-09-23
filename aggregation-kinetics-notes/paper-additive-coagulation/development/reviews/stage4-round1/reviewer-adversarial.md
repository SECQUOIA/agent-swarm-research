# Independent adversarial review of Stage 4

**MAJOR count: 0. MINOR count: 0. Recommendation: accept Stage 4.**

I read all of `sections/finite-population.tex`, `sections/observable-boundaries.tex`, `appendices/finite-count.tex`, and `appendices/unbounded-moments.tex`, and checked their use of the accepted earlier framework. I inspected the particle simulator, runner, saved CSV and JSON, plot code and figure, verification wrappers, power-counterexample script, and supplement documentation. I did not read other current Stage 4 review reports, contact reviewers, change manuscript or shared data files, or run a shared build. All executable checks and regenerated artifacts used a temporary copy. Stage 5 omissions were excluded.

No mathematical or evidence-related defect was found. The detailed checks below explain why the requested adversarial cases do not invalidate the results.

## 1. Finite process, autonomous count, and normalization

**Location:** `sections/finite-population.tex:13–92`, `prop:finite-count`.

I recomputed the unordered pair sum. Each mass occurs in exactly `ell-1` pairs, so total coagulation rate is `b(ell-1)` when physical mass is `nm`. Total fragmentation rate is `b ell`; at count one the death rate is zero. The distinction between an actual complementary split and an arbitrary expected daughter measure is necessary and is explicitly imposed here.

The event-count pure-birth domination has rates larger than those of the actual process, has divergent reciprocal-rate sum, and controls all fixed count moments on bounded intervals. It therefore justifies nonexplosion and the stopped-to-unstopped generator calculations. All particle masses remain positive and finite at finite times, and the total physical mass stays `nm` pathwise.

The count generator applied to `ell` and `ell^2` gives `b` and `4b ell-b`. Hence

\[
 \mathbb E L=L_0+bt,\qquad
 \operatorname{Var}L=b(2L_0-1)t+b^2t^2.
\]

The quadratic-variation and Doob calculations give exactly the displayed concentration constants. A common upper bound on `c_n=L_0^n/n` is enough for absolute concentration on every `o(n)` horizon.

I explicitly challenged the case `L_0^n=1`, so `c_n=1/n -> 0`. At logarithmic time the expected count is `1+bC log n`, and relative accuracy against the continuum count can fail badly, while the normalized absolute error still tends to zero. The manuscript states precisely this distinction rather than claiming relative concentration or order-`n` populations under the weaker assumption.

## 2. Mass discrepancy without a uniform initial second moment

**Location:** `sections/finite-population.tex:103–174`, `thm:finite-discrepancy` and `eq:finite-diagonal`.

For each `n`, the empirical initial measure has finite support, so the accepted existence theorem supplies its own continuum solution. The proof never uses a uniform initial second-moment bound across `n`. Its uniform fractional estimate is instead

\[
 M_p(v_t^n)\le c_n^{1-p}m^p e^{-b\kappa_p t},
\]

which follows from count, mass, and the earlier moment theorem.

Comparing both mass laws at the deterministic physical ceiling `nm` gives the displayed lower discrepancy. The factors of `m` cancel correctly; the continuum mass below the ceiling is at most `(n c_n)^(1-p) exp(-b kappa_p t)`. The limit of `kappa_p/(1-p)` at one permits a single fixed `p` for every specified strict coefficient `C>1/(b log 2)`. The result is uniform in the initial configurations with bounded `c_n` and in the allowed split laws because neither the ceiling nor this fractional estimate depends on their additional details.

In the difficult example `L_0^n=1`, the initial continuum second moment is `n m^2`, which diverges. The ceiling estimate still simplifies to `exp(-b kappa_p t)`, so the theorem remains valid. This provides a concrete check that an unspoken uniform second moment has not entered the proof.

The same deterministic ceiling holds after taking expectation of the finite mass law. No Jensen interchange for a nonlinear distance is needed. The relative fractional-moment lower bound also has the correct direction and diverges under the common upper count bound. It is correctly distinguished from a nonvanishing absolute moment error.

The finite-generator correction has the correct sign and factor. The continuum diagonal is `lambda(2^p-2)n^-2 sum_i x_i^(p+1)` and must be subtracted. At `p=0` this gives exactly `b/n`, consistent with the independent count calculation. Fragmentation is already linear and needs no diagonal correction. The text does not claim that the factor `1/n` makes this correction uniformly small when the accompanying higher moment grows.

## 3. Count PGF, diffusion scaling, and the boundary initial state

**Location:** `appendices/finite-count.tex:11–116`, `prop:count-diffusion`.

Shifting the count by one gives critical per-individual birth and death rates `b` and immigration rate `b`. The single-family generating function solves `partial_t u=b(u-1)^2`. Multiplying its initial-family contribution by the Poisson immigration factor gives the stated PGF, including the denominator and the count shift.

Substituting the count scale `t=n tau` and Laplace argument `exp(-theta/n)` gives the stated limit transform uniformly over bounded scaled starting counts. The conditional transform argument supplies the finite-dimensional distributions. Compact containment follows from the nonnegative submartingale bound. The stopped martingale bracket controls stopping-time increments by `2bR delta`, and the deterministic drift adds at most `b delta`. Thus the path tightness argument works in `J_1`; vanishing jump sizes force continuous limits.

The two-dimensional squared Brownian construction has drift `b` and variance coefficient `2bZ`, with exactly the stated initial radius. Its Laplace transform, mean, and variance agree with the count-scale limits. The zero-initial-state case `c=0` is covered: at positive time the limiting law is exponential with mean `b tau`, as also follows directly from the PGF for the shifted process started at zero. No positive lower bound on `c_n` is being used to identify or construct this limit.

The later count scale is not substituted for the earlier mass-discrepancy scale. The text correctly explains that mass-CDF failure need not wait for count collapse.

## 4. Count-neutral classification and rigidity

**Location:** `sections/observable-boundaries.tex:13–84`, `thm:neutral-class` and `prop:observable-rigidity`.

Monodisperse preparations force `S(x)=mK(x,x)/(2x)`. Equal-mass two-point preparations then force the off-diagonal expression `K(x,y)=x d(y)+y d(x)` with `d=S/m`. Conversely, direct integration gives the claimed neutral count vector field. The classification requires only finite-support initial rates; it does not smuggle in an existence theorem for general kernels.

The full-trajectory conclusion separately requires mass conservation and integrable event rates, which are the conditions needed to integrate the count identity. The fixed-mass preparation class allows the count to vary, as required for the monodisperse tests.

For an additional fractional moment, the monodisperse vector field is bounded above by the strictly negative coefficient `-kappa_p m^2 d(x)x^(p-1)` whenever `d(x)>0`. For the second moment, the coagulation contribution is `2m^2 x d(x)`, while the fragmentation contribution is at least `-m^2 x d(x)/2`; the lower coefficient `3/2` is correct. Nonnegative rates then force `d=0` under universal vanishing. These are statements about all preparations, not identification from one trajectory.

## 5. Tangent truncation, second moment, and entropy

**Location:** `appendices/unbounded-moments.tex:11–85` and `sections/observable-boundaries.tex:88–162`, `prop:broadening-entropy`.

The tangent truncation is an effective way to obtain admissible tests here. For both `x^2` and `x log x`, subtracting the tangent slope times `x` leaves a bounded function. The bounded weak equation and conserved first-moment identity therefore give the full truncated balance without assuming the desired unbounded test in advance.

Both the truncated function and the removed tail are convex, vanish continuously at zero, and have nondecreasing quotient by `x`. This proves the displayed coagulation and fragmentation increment dominations even for `x log x`, which is negative below one. The argument does not incorrectly assume that convexity requires a nonnegative function.

The second-moment coagulation majorant integrates to `4mM_2`; the entropy majorant integrates to a constant times `2NM_2+2m^2`. The fragmentation majorants are `x^2` and `x log 2`. All are time-integrable under locally bounded second moment and locally integrable controls. Endpoint domination is also valid, including the negative entropy part near zero. Hence the complete balances and local absolute continuity follow without an additional logarithmic moment or a third size moment.

The second-moment production interval is exactly `[3lambda m M_2/2, 2lambda m M_2]`, and equal splitting gives the lower endpoint at all times. Dividing the earlier pair inequality by `1-p` and letting `p` increase to one gives the entropy pair constant `4 log 2`; coagulation therefore contributes at least `2lambda m^2 log 2`, and fragmentation subtracts at most `lambda m^2 log 2`. The stated net entropy constant is correct.

For initial-time sharpness, continuity of the total second moment together with total variation convergence indeed yields weighted variation convergence with weight `1+x^2`. The explicit truncated-second-moment remainder controls the tail beyond `sqrt(2)R`, so no unsupported uniform-integrability inference is needed. This makes the entropy integrand continuous at the monodisperse initial state and proves the claimed right derivative for an actual solution.

The comparison with the static model uses the same initial measure, count, mass, and mean. Increasing a fixed positive rate across models produces arbitrarily large second-moment differences at a chosen positive time, while each individual model retains finite second moments at finite times. This establishes the stated inability of those three bulk outputs to give a uniform second-moment bound; it makes no finite-time gelation claim.

## 6. Singular stationary test for power kernels

**Location:** `sections/observable-boundaries.tex:166–275`, `thm:power-no-equilibrium`.

For `0<alpha<=1`, finite count and mass imply `0<M_alpha<infinity`. The total event flux is therefore finite, and the bounded count test forces `s=m`. I recomputed the integrated generator representation at that value: its loss is exactly `xD+2m x^alpha`, including the second copy of the fragmentation-weighted loss. The embedded transition kernel and the rate-weighted probability are consequently normalized correctly.

The inverse-power test is not applied directly under the population measure. It is integrable under the rate-weighted probability because

\[
 3mD\int x^{-\alpha}\,d\zeta
 =D M_{1-\alpha}+2mN<\infty.
\]

Testing the invariant probability identity with bounded truncations and using monotone convergence establishes finiteness of the corresponding gain before subtraction. This remains valid when the original daughter inverse moments are infinite: the hypothetical stationarity forces their integrated contribution to be finite. Thus there is no hidden negative-moment assumption and no illegal cancellation of infinities.

Jensen gives the stated positive fragmentation contribution. The symmetrized coagulation integrand and the tangent bound for the concave power yield `J<=alpha mN`, with the factors of two correct. The net coefficient is strictly positive throughout the stated interval, including `alpha=1`. At that endpoint the rate-weighted probability is the mass law, and the simpler inverse-size contradiction is consistent with the general proof.

The proof requires only stationary bounded-test identities; it neither relies on a time-dependent solution for the power kernel nor constructs an unproved auxiliary process in that model.

## 7. Power-kernel counterexamples and known infinite-count equilibria

**Location:** `sections/observable-boundaries.tex:277–335` and `supplement/count_neutral_power.py`.

The two-point preparation has mass exactly two. I checked the two diagonal coagulation terms, the cross term, and the fragmentation term independently; they give the displayed formula. Its positive term diverges when `p>1-alpha`, while the negative term stays bounded. The half-moment example at `alpha=1, R=64` has drift

\[
 27\sqrt2+2\sqrt{65}-54\approx0.308281680671>151/500.
\]

The rational square-root lower bounds certify the strict inequality. The supplement agrees with the atomic sum. Its other finite-radius examples are merely formula checks and are not all positive; the manuscript does not incorrectly claim they are.

The preparations have finite support and all positive moments. The manuscript explicitly describes them as vector-field counterexamples and does not assert an unproved local solution or initial derivative for the separate power-kernel evolution.

I checked Proposition 4.3 and Remark 4.4 of the cited [Tran–Van preprint](https://arxiv.org/pdf/1910.13424v3). The original kernel and fragmentation convention match the stated conversion. The scaling `n_t=m c_(2mt)` changes them to `K=2xy`, `S=mx`. The stationary transform identity gives the claimed derivative and integrated asymptotic, so monotone convergence yields infinite particle count. Thus the known stationary examples do not contradict the finite-count exclusion. The manuscript appropriately limits its power-kernel conclusion to nonstationarity and does not transfer the additive path or moment theorems.

## 8. Simulator, saved data, and figure audit

**Locations:** `supplement/critical_additive_particles.cpp`, the particle Python scripts, saved CSV/JSON and figures, and `sections/finite-population.tex:176–275`.

The simulator's event sampler matches the physical model. Total rate is `2L-1`; fragmentation selects a uniform parent; the coagulation sampler chooses one mass-weighted particle and one different uniform particle. Summing the two orderings gives the intended unordered pair rate. Count one cannot enter the coagulation branch. Snapshot processing keeps the already sampled event time across output times, so snapshots do not reset clocks.

I inspected the dense-array and Fenwick updates, including capacity growth and moving the last mass into a removed slot. Sorting merge indices prevents the kept particle from being overwritten during removal. The output statistics use the stated denominators: actual count for number statistics and log moments, initial physical mass for mass fractions, and `n` for the empirical half moment. CDF thresholds are inclusive.

All execution took place in `/tmp/stage4-adversarial-vwlwwh4s`, leaving the shared source and data untouched. The checks were:

- Ran the saved-data verification and power-counterexample script in the temporary copy.
- Recompiled and reran all nine declared trajectories, then reran verification. All 90 regenerated CSV records matched the archived records exactly. The total remained 6,588,932 events.
- Regenerated the six-panel figure. Its PNG was byte-for-byte identical to the archived PNG, which I also inspected visually. All declared trajectories and continuum references are present.
- Reran the separate 2,000-seed count diagnostic. It reproduced mean `60.473`, unbiased variance `1098.2614017008505`, minimum count one, and mean error `0.6407120465587508` theoretical standard errors, agreeing with the documentation.
- Wrote and ran an independent temporary C++ harness with 20,000 randomized append, replace, remove, split, and merge operations. After every operation it compared the array with a separate reference vector, checked the direct mass sum against the tree, and tested each active cumulative-mass interval. It passed under address and undefined-behavior sanitizers with no runtime diagnostics.

The mathematical sampler is exact in real arithmetic. The implementation uses finite random numbers and floating-point masses, as the manuscript says. It does not claim that printed conservation certifies unlimited dynamic range or arbitrary time horizons. The acknowledged risk of losing tiny cumulative weights is real, and the stated limitation is appropriate. The archived claims do not require stronger accuracy than the evidence establishes.

I independently recomputed the data assertions. All nine final log means lie in the stated interval `[-13.862943611198906,-11.042975048153092]`. Their log variances range from `11.962426785404078` to `14.56583446770551`. At `n=100000`, the mass fractions below 100 are between `1.050539%` and `1.249908%`, and the largest count deviation from its continuum value is `3.228%`. These agree with the printed rounded descriptions and table.

The continuum certificate optimization has the correct stationary equation for its optimizing fractional power and is clipped at the endpoint for the two larger sizes. Its small value at `n=1000` and zero values for the larger sizes are consistent with the explicit warning that these runs do not demonstrate nearly maximal continuum discrepancy. No numerical PDE solution, propagation-of-chaos conclusion, confidence interval, or variance-convergence claim is inferred from the figure.

## References and scope

The count diffusion is supported by a self-contained PGF, tightness, and Brownian construction. The contextual citation to [Giorno–Nobile](https://www.mdpi.com/2227-7390/9/16/1879) accurately identifies birth–death processes with immigration as sources of Feller-type diffusion approximations; it is not being used to bypass the specialization's proof.

The Stage 4 additions preserve the earlier distinctions between number and mass sampling, physical particles and the auxiliary number process, finite first/second size moments and logarithmic assumptions, and instantaneous versus trajectory-level claims. The future Fourier application and remaining Stage 5 material are outside this review.

## Optional improvements

None required. The mathematical caveats and numerical limitations needed for the current claims are already present.

**Final MAJOR count: 0. Final MINOR count: 0. Clean recommendation: accept Stage 4.**
