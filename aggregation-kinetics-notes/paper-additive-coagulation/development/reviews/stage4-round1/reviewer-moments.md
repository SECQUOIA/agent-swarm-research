# Independent Stage 4 review: moment balances and finite-population mathematics

**Recommendation: accept Stage 4. MAJOR issues: 0. MINOR issues: 0. The reviewed mathematics is clean.**

I independently reviewed all new mathematics in `sections/finite-population.tex`, `sections/observable-boundaries.tex`, `appendices/finite-count.tex`, and `appendices/unbounded-moments.tex`, and their compatibility with the accepted earlier results. I also read the new supplement source and reproduction instructions, inspected the supplied figure, and checked the archived numerical results. I did not read other current Stage 4 reports, communicate with reviewers, edit manuscript files, or run a shared build. The read-only verification and rational-counterexample scripts both passed.

## Entropy coefficient and complete unbounded balances

The strengthened entropy coefficient is correct. Dividing the established fractional pair inequality by `1-p` and taking `p` to one at fixed positive sizes gives

`(x+y) Delta(x log x)(x,y) >= 4(log 2)xy`.

The coagulation prefactor one half consequently produces at least `2 lambda m^2 log 2`. Jensen against the probability `b_{t,x}/2` bounds fragmentation below by `-b m log 2`. At criticality `b=lambda m`, their sum is the claimed `lambda m^2 log 2`. The scalar limit, sign, and factors are correct, and no limit is being passed through a population integral in this argument.

The appendix supplies the needed complete balances. Each tangent truncation differs from a bounded function by a multiple of the conserved mass test. Both the truncation and its removed tail are convex and vanish at zero; their superadditivity and daughter-loss inequalities give the claimed domination of complete increments. This argument remains valid for the negative part of `x log x` near zero. The second-moment coagulation majorant integrates to `4m M_2`, and the entropy majorant integrates using `2N M_2+2m^2`. The fragmentation bounds require no daughter logarithmic moments beyond the automatically controlled mass-weighted quantity. All time integrals are finite under the established locally bounded second moment.

Endpoint domination of the tests is valid, so the integrated identities and local absolute continuity follow. The argument for weighted-second-moment convergence at zero is also valid: total-variation convergence plus convergence of total second moments controls the tails after subtracting the bounded truncated moment. It makes the entropy vector field continuous for the equal-split monodisperse sharpness example. Both scalar inequalities attain equality there, so the instantaneous sharpness concerns actual solutions.

The second-moment balance gives exactly `3 lambda m M_2/2 <= M_2' <= 2 lambda m M_2`. Equal splitting attains the lower growth rate for the whole trajectory. Comparing it with the static model preserves the stated count, mass, and mean size, while the second-moment discrepancy grows without a uniform bound as lambda increases. No finite-time divergence is claimed for a fixed lambda.

## Physical count process and diffusion

Summing unordered additive pair rates gives `b(ell-1)`, while fragmentation gives `b ell`. The linear pure-birth domination proves nonexplosion and justifies the finite-horizon moment calculations. The count drift is `b`, its squared-count drift is `4b ell-b`, and its variance is exactly `b(2L_0-1)t+b^2t^2`.

The martingale bracket and the constants `8` and `10` in the maximal second-moment estimate are correct. The consequence on every horizon `T_n=o(n)` follows from the common upper bound on `c_n`. The manuscript appropriately distinguishes absolute count accuracy from relative accuracy when `c_n` can tend to zero.

After subtracting one, the count chain is critical linear branching with immigration at rate b. The one-family generating function and the immigration factor give the displayed PGF. Its Laplace scaling at time `n tau` gives `(1+b tau theta)^(-1) exp(-c theta/(1+b tau theta))`.

The scaled martingale has bracket rate `2b Z_n-b/n`. Compact containment follows from the nonnegative submartingale bound; stopping at a level gives the stated bound for increments between bounded stopping times. This verifies path tightness. The vanishing jump sizes and identified finite-dimensional laws yield the continuous limit in `J_1`. The two-dimensional Brownian squared-radius construction has drift b and diffusion coefficient `sqrt(2bZ)`, including the initial state c=0. Its transition transform, mean, and variance agree with the discrete limit. No initial mass-allocation or daughter-law parameter has been lost from a count law that depended on either of them.

## Mass-CDF obstruction and missing diagonal

The physical ceiling is `nm`, while the deterministic comparison begins from exactly the same empirical measure. The continuum fractional bound gives

`bar pi_t^n((0,nm]) <= (n c_n)^(1-p) exp(-b kappa_p t)`.

The limiting ratio `kappa_p/(1-p) -> log 2` permits a single fixed p whenever `C>1/(b log 2)`. Substitution of `C log n` gives the stated positive exponent eta and a discrepancy tending to one uniformly under the common count bound. The expectation version preserves the same ceiling. Simultaneous count accuracy follows because logarithmic time is sublinear in n. These arguments use neither a uniform second initial moment nor a prior continuum approximation theorem.

The relative-moment obstruction follows from the finite-system floor `m(nm)^(p-1)`. Its factors of mass cancel correctly against the continuum upper bound. The stated divergent ratio follows even when `c_n` tends to zero, and is not misrepresented as a nonvanishing absolute error.

The diagonal term included in the continuum drift is `lambda(2^p-2)n^(-2) sum x_i^(p+1)`. Removing it gives exactly `lambda(2-2^p)M_(p+1)/n`. At p=0 this is `b/n`, matching the autonomous normalized-count drift.

## Classification, rigidity, and power-kernel boundary

The monodisperse and two-atom preparations prove the complete count-neutral class `K(x,y)=x d(y)+y d(x)`, `S(x)=m d(x)`. Allowing count to vary at fixed mass is essential and is explicitly retained. The trajectory conclusion separately invokes mass conservation and integrability of the count balance.

For an additional fractional moment, the monodisperse vector field is at most `-kappa_p m^2 d(x)x^(p-1)`. For the second moment it is at least `3m^2 x d(x)/2`. These signs and constants force pointwise zero rates under universal vanishing.

For power kernels, count stationarity first forces `s=m`. The proposed positive jump-kernel rewriting has rate `q(x)=xD+2m x^alpha`, with integrated rate `3mD`. The weighted invariant probability makes the singular test integrable because its weighted integral is `D M_(1-alpha)+2mN`. Truncation against the invariant probability therefore legitimizes both gain and loss before subtraction; it does not silently assume a negative population moment.

The symmetrized coagulation loss bound `J<=alpha mN` follows from concavity of the alpha power and the sum of the two `(1+alpha)` powers on the unit interval. The fragmentation lower bound gives the strictly positive gap `2(2^alpha-1)-alpha`, establishing stationary exclusion throughout `0<alpha<=1`. The alpha=1 embedded-chain illustration has the correct probabilities one third and two thirds.

The atomic fractional-vector-field calculation and its coefficient `A_p` are correct. For `p>1-alpha`, its positive term grows without bound while its negative cross term remains bounded. At alpha=1, p=1/2, R=64, the explicit value is approximately `0.308281680671`, and the rational lower bound `151/500` is valid. The supplement passed both the direct-sum comparison and this rational certificate. The text correctly presents these as vector-field examples without claiming an unproved time-dependent solution theory.

I checked the equilibrium context against [Tran–Van, Proposition 4.3 and Remark 4.4](https://arxiv.org/html/1910.13424v3). Their kernel normalization maps as stated, and the identity for G yields the claimed `q^(2/3)` growth of the Bernstein transform. Its divergence implies infinite count, so these classical equilibria do not contradict the finite-count theorem.

## Numerical integration and reproducibility

The sampler's two-stage unordered-pair probabilities give the desired additive rates in real arithmetic. Uniform parent selection gives the fragmentation rate, and snapshots retain the existing event clock. I inspected the array/tree update logic, run wrapper, plot script, saved-data verifier, count diagnostic wrapper, and README. The described finite-precision limitations are relevant and do not overstate the mass checks as exact arithmetic.

The saved-data verifier confirmed all 90 snapshots, all nine declared paths, the count identities, normalizations, physical ceilings, moment floors, and 6,588,932 events. Independent arithmetic reproduced the continuum half bound `0.17983261947086074`, mean-log interval `[-13.862943611198906,-11.042975048153092]`, reported log-variance range, and table ranges. Optimizing the mass-CDF certificate gives `1.951420043080838e-5` for n=1000 and zero for the larger sizes, as stated. The figure distinguishes continuum references from particle paths, and the text does not promote the descriptive runs into proof of a continuum discrepancy or variance limit.

No corrective manuscript change is requested by this review.
