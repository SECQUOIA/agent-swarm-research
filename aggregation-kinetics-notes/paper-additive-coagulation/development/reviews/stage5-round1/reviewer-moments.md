# Independent Stage 5 review: Fourier constants and observation algebra

**Recommendation: accept after the minor correction below. MAJOR issues: 0. MINOR issues: 1.**

I independently read the complete new Fourier section, observation-design appendix, abstract/introduction, discussion, main file, added references, README, coverage map, and Stage 5 author handoff. I checked their mathematical dependence on the accepted stages. Every file listed in the frozen Stage 5 snapshot matched its recorded SHA-256 hash during this review. I did not read other current Stage 5 reports, communicate with reviewers, change shared sources or data, run a shared build, or repeat the accepted particle simulations.

## Actionable finding

### 1. MOM-S5-01 — MINOR: the daughter atom at one is not an identifiability obstruction under both stated daughter constraints

**Location:** `sections/fourier-identification.tex:211–215`, immediately after `thm:fourier-identification`. Related descriptions occur in `development/COVERAGE.md:55` and `development/stage5-author.md:21`.

The statement “Strictly smaller daughters are essential: a daughter atom at one would produce an invisible jump at zero” overstates the limitation. A zero log jump is invisible to an unrestricted compound-Poisson exponent, but this model also fixes both the daughter count and daughter mass. Those two constraints determine the missing atom.

To see this, allow `B` on `(0,1]` while retaining `B((0,1])=2` and `integral theta B(dtheta)=1`. Let `nu_-` denote the restriction of `sigma (log)_# B` to `(-infinity,0)`. The same one-sided uniqueness argument identifies `nu_-` from the exact local exponent. The daughter constraints then give

\[
\sigma=\int_{(-\infty,0)}(1-e^y)\,\nu_-(\mathrm dy),
\qquad
\nu(\{0\})=2\sigma-\nu_-(( -\infty,0)).
\]

Thus, when `sigma>0`, both the selection rate and the entire daughter measure, including its atom at one, remain uniquely determined. Equivalently, the very next manuscript identity `psi(-i)=-sigma` still holds when an atom at one is allowed, and recovers the selection rate before the missing atom is inferred from total daughter count.

For a concrete admissible expected-daughter example, take `B=(1/2)delta_1+(3/2)delta_(1/3)` and `sigma=2`. The visible measure is `nu_-=3 delta_(-log 3)`. It determines `sigma=3(1-1/3)=2`, then the missing jump mass `nu({0})=4-3=1`, and therefore `B({1})=1/2`. No ambiguity remains. This concerns the manuscript's expected-daughter class; an eventwise complementary positive binary split already excludes a daughter of the entire parent size for a separate physical reason.

**Suggested correction:** remove the claim that strict inequality is essential for identification. A concise replacement is: “The support assumption excludes zero log jumps. Such jumps are invisible directly in the exponent, but the two daughter constraints would determine their mass if daughters of the parent size were admitted.” The paper need not extend its forward theorems or change its current support assumptions. Align the coverage/handoff description with this narrower statement rather than presenting the endpoint as a proved nonidentifiability boundary.

This is minor because the formal identification theorem is correct on its stated open-support class; only the explanatory necessity claim is false.

## Fourier factorization and structural identification checked

The normalized bounded-test equation gives the fragmentation exponent `sigma integral(theta^(ik)-1)B` with the correct factor, and the coagulation forcing satisfies `|r_t(k)| <= |k|a_0 exp(-omega t)`. No separate absolute log moment is needed: the estimate is for the paired increment and uses the accepted half-moment bound.

Writing `d=-Re psi(k)`, the integrating-factor tail has exponent `delta=omega-d`, and its prefactor is exactly `D(k)=|k|a_0/delta`. Multiplication by the outer exponential gives physical error `D exp(-omega t)`. Both displayed estimates therefore have the correct signs and constants. On a compact neighborhood with positive lower bound for delta, the rescaled characteristic functions converge uniformly; this proves amplitude continuity and local nonvanishing from `C_infinity(0)=1` without an initial log moment. The text does not assume that this amplitude is an independent-shift characteristic function.

The quotient subtraction uses the rescaled denominator and yields exactly the factor

`[2D/|C_infinity|] exp(h Re psi) (1+exp(-delta h)) exp(-delta t)`.

The denominator condition is imposed before division. The uniform local result follows by compactness, and shrinking the interval so that the limiting quotient remains near one fixes the phase through the continuous logarithm anchored at zero. A pointwise arbitrary logarithm is not substituted for this branch.

The one-sided uniqueness proof uses the correct lower half-plane for negative log jumps. Finite measure mass supplies boundary continuity; damping supplies all derivatives strictly inside the half-plane. Subtracting total signed jump mass at zero changes equality of exponents into vanishing of a finite signed measure's transform. Schwarz reflection, the identity theorem, and finite-measure Fourier uniqueness then give the claimed result on the open negative half-line. There is no hidden moment assumption.

On the stated support class, structural recovery of `sigma` and `B`, the unused-daughter exception at zero selection, and recovery of `lambda=(sigma-r_N)/m` are all correct. Unknown initial data cancel through the amplitude; size-unit changes cancel through a common phase. The need for a continuum of exact frequencies and the distinction between expected daughter measures and event correlations are stated appropriately.

The complementary-atom instability example preserves both daughter constraints. Nearby distinct complementary pairs have exponent differences tending uniformly to zero on each bounded frequency interval, while their full signed variation distance stays four. This proves the stated lack of continuity into variation norm and makes no unsupported claim against stability in weaker metrics.

## Sampling constants, division, and observation-time balance checked

Hoeffding for a component in `[-1,1]` gives the two-sided bound `2 exp(-n a^2/2)`. Using `a=epsilon/sqrt(2)` and four components gives `8 exp(-n epsilon^2/4)`. Consequently `epsilon_n=2 sqrt(log(8/alpha)/n)` has exactly the claimed confidence level. Independence within each sample suffices; the extra independence between times is a valid stated observation model.

Both quotient identities in the proof are algebraically correct. The observable certificate uses the strict condition `|Uhat|>epsilon_n` to infer a nonzero exact denominator. The stronger signal condition instead gives `|Uhat| >= (c/4)exp(-dt)>0`; combined with `|R_t|<=1+K`, it yields the factor `4(2+K)/c` without an unnecessary second attenuation factor.

At `t_n=log(1/epsilon_n)/omega`, both the deterministic bias and the amplified sampling error are proportional to `epsilon_n^(delta/omega)`. Since delta is positive, this quantity tends to zero, verifies the signal condition eventually, and puts the observation time beyond the required finite `t_0`. At fixed confidence the exponent in n is `-delta/(2omega)`, and the time scale is `log(n)/(2omega)`. The zero-attenuation case remains valid. The paper correctly treats the schedule as sufficient and dependent on unknown class constants, rather than adaptive or statistically optimal. The sampling-to-finite-time ratio certificate is not confused with a full bias certificate or with an estimator from one interacting vessel.

## Preparation shell, gauges, and tomography checked

The shell's positive feasible point provides a relatively open subset of its affine space. Polynomial vanishing there gives the restricted Hessian identity `Q K Q=0`. The explicit `A_0` has symmetric product equal to K. The remaining linear term lies in the row space and has coefficient gamma perpendicular to h. The stated skew matrix satisfies `L^T h=gamma`; adding `L C` preserves K and supplies the required linear term. The hypotheses `h!=0` and full row rank are used, including at full-dimensional constraint rank. The rank bound is a necessary consequence and is not incorrectly used as a sufficient classification.

The continuum two-constraint family has count drift `(c-N)integral a dn+(m-M_1)integral d dn`. Under the stated bounded coefficients, valid count balance, and mass conservation, the scalar equation preserves count c. The manuscript does not infer an unproved continuum converse or forward existence theorem from the grid algebra.

The known-source fixed-concentration gauge, its removal at two concentrations, the unknown-source one-parameter family at two concentrations, and removal by a third concentration all follow from the diagonal and equal-mixture equations with the displayed signs. Physical nonnegativity and changing material loading are properly separated from the algebraic ambiguity.

Direct substitution verifies both reconstruction formulas, including repeated-size mixtures. The measurement count equals the unrestricted symmetric-kernel plus linear-rate parameter count, and the linear-map dimension argument justifies only the stated lower bound on scalar measurements. The source formula `3r(c)-3r(2c)+r(3c)` cancels the linear and quadratic terms exactly.

The deterministic noise constants `3/c^2`, `5/(2c)`, `1/c^2`, `3/(2c)`, and seven for the source reconstruction are correct. Reuse of observations does not invalidate these absolute-error bounds. Taylor's integral remainder gives `eta/t+Lt/2`; its positive-parameter minimizer and minimized kernel bound are `sqrt(2eta/L)` and `3 sqrt(2L eta)/c^2`. The allowed-time interval, zero-parameter cases, concentration dependence of curvature, finite-width preparations, and coefficient-preservation assumptions are all addressed.

## Integration and scientific attribution

The abstract, introduction, assumption table, and discussion accurately summarize the accepted results and distinguish instantaneous sharpness from exact long-time rates. They also distinguish the auxiliary number process, physical particle system, and independent continuum samples. The finite-population and logarithmic-limit qualifications are retained. No new theorem relies on solving the unresolved critical last-time exponent or stable noisy analytic continuation.

The new literature statements are narrow and do not import unverified hypotheses into proofs. I checked the direct quotient-and-logarithm antecedent in [Garnier, Section 2.2](https://arxiv.org/html/2405.10588v1), log-size sampling and Fourier regularization in [Hoang et al., Sections 3.1.1–3.1.4](https://www.math.univ-paris13.fr/~phamngoc/HoangPhamRivoirardTran.pdf), the stated inverse-fragmentation contexts in [Doumic–Escobedo–Tournus (2018)](https://arxiv.org/abs/1804.08945) and [their 2024 paper](https://www.numdam.org/articles/10.5802/ahl.207/), daughter-distribution inference in the [Mirzaev–Byrne–Bortz author preprint](https://arxiv.org/pdf/1510.01355), and the finite stochastic/mean-field context in [D'Orsogna–Lei–Chou](https://www.math.ucla.edu/~tchou/pdffiles/JCP_LEI.pdf). The [Brown–Donev–Bissett primary text](https://www.tandfonline.com/doi/pdf/10.1080/00401706.2014.947003) supports the limited quadratic-mixture context, rather than being presented as the source of the exact shell theorem.

Some older publisher pages, including the direct Patil/McCoy full-text requests, returned access errors during this review. I do not claim to have independently audited those inaccessible proofs, and no new proof depends on them. The author handoff explicitly limits the historical claim and records this access distinction. I found no additional actionable attribution issue.

## Optional preferences

None. The requested correction above concerns a mathematical claim of necessity, not a stylistic preference. The formal new theorems and their quantitative constants otherwise check out.
