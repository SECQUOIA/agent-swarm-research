# Independent adversarial review of Stage 2

I read all of `sections/auxiliary-process.tex` and `sections/log-limits.tex`, checked their dependencies against the current Stage 1 model, fractional-moment section, and existence appendix, and read the current bibliography and coverage map. I did not read other current Stage 2 review reports, contact reviewers, edit manuscript files, or run shared builds. Later stages are outside this review's scope.

**Assessment:** The central proof chain is sound. In particular, nonexplosion does not depend circularly on marginal identification; finite total coagulations are proved without taking expectations of uncontrolled random products; and exact transport does not subtract infinite means. I found two minor explanatory inaccuracies and no major defect.

## Findings

### S2-ADV-001 — MINOR: distinguish lattice support of the reference from atomic support of the nonlinear solution

**Location:** `sections/log-limits.tex:269–274`, the discussion following `thm:log-limits`.

The final sentence says that equal splitting can preserve a lattice in log size. In this location, the subject is the nonlinear law of `Z_t` in the standing constant-rate setting `lambda > 0`. Equal splitting does not preserve a global logarithmic lattice under additive coagulation, even from monodisperse data. The explanation should distinguish the reference from the nonlinear law.

For a concrete test, take `n_0 = delta_1`, equal splitting, and positive constant coagulation and fragmentation rates. At any positive time the zero-jump contribution gives positive probability at size `1`, a fragmentation-and-survival contribution gives positive probability at `1/2`, and fragmentation followed by coagulation with a size-one partner gives positive probability at `3/2`. The latter contribution has positive probability because the environment retains a positive atom at size one at every finite time. These three log sizes cannot all lie in a common lattice `a+h Z`: their differences include `log 2` and `log(3/2)`, whose ratio is irrational. Otherwise an integer power of `3` would equal an integer power of `2`.

There is nevertheless a valid obstruction to a density: dyadic rational sizes form a countable set closed under addition and halving, so monodisperse equal-split data keep the nonlinear size and log laws purely atomic. The independent equal-split reference does stay on its logarithmic lattice. The theorem and the warning that a weak CLT does not imply density convergence remain correct.

**Suggested fix:** Replace the final sentence with, for example: “For monodisperse initial data and equal splitting, the reference is lattice-valued in log size, while the coagulation–fragmentation law remains purely atomic.” Merely stating the latter atomic-support fact is also sufficient.

### S2-ADV-002 — MINOR: the statement about stationary reference increments needs the zero-rate exception

**Location:** `sections/log-limits.tex:27–30`, following `eq:poisson-reference`.

The claim that the increments are stationary “only when the intensity and mark law are constant” is too strong under the allowed nonnegative controls. If `sigma(t) = 0` for every `t`, then `bar Z_t-Z_0` is identically zero and has stationary increments even if `B_t` changes arbitrarily with time. For example, switch between `B_t = 2 delta_(1/2)` and `B_t = delta_(1/4)+delta_(3/4)`; both satisfy the daughter assumptions. Changes of `B_t` on null sets of times likewise cannot affect stationarity.

The relevant condition is time homogeneity of the effective jump-intensity measure `sigma(t) B_t(d theta) dt`, with equality understood almost everywhere. When its nonzero rate is constant, the fixed daughter count indeed forces `sigma` and `B_t` to be constant almost everywhere. The zero-intensity case leaves the mark law unrestricted. This does not affect any subsequent constant-rate theorem.

**Suggested fix:** The smallest correction is to state only the sufficient fact needed here: “The increments are stationary in the constant-rate, fixed-daughter-law setting below.” Alternatively, state the condition on the effective intensity measure directly.

## Detailed adversarial checks with no defect found

### 1. Number-process construction, nonexplosion, and identification

**Locations:** `auxiliary-process.tex:12–132`, `thm:number-process`.

I recomputed the normalization. Dividing the population equation by the count and differentiating the normalization cancels the extra additive coagulation loss and changes the fragmentation loss to `2 sigma`. The displayed number generator and its mean jump flux `2 sigma+b` are correct.

For the Lyapunov test `V(x)=x`, the fragmentation contribution is `-sigma x`, and the coagulation contribution is `lambda N x (m/N)=b x`. The proof first stops both jump number and state size. Before those stops the rates are bounded by an integrable function, while an overshooting coagulation mark has finite conditional first moment. Thus the stopped Dynkin calculation is valid with only the first size moment. The resulting bound controls the stopped count's compensator without knowing the process marginal. Removing the size stop by Fatou, followed by `k P(tau_k <= T) <= L_T`, rules out finite-time explosion. This argument also handles rates that are merely locally integrable, rates with zeros, and deterministic finite starting sizes.

The subsequent marginal argument is independent of a uniqueness claim for an unbounded forward generator. The prescribed probability curve has finite integrated gain and loss. The output restriction keeps the full incoming gain, including daughters from parents beyond the cutoff. The loss identity now has the explicit local multiplier bound required by the revised Stage 1 appendix. Positive successive substitutions give domination of each finite-jump partial sum; nonexplosion gives total mass one for their sum, forcing equality. Neither a second size moment nor continuity of the parent-dependent daughter kernel is used here.

I also checked the inverse-size calculation in `rem:inverse-size`. Both the eigenfunction identity and the transform have the stated coefficients, including the additional `b(t)` in the mass-tag coagulation rate. It is correctly presented as an algebraic identity, without claiming a mass-tag path construction under assumptions not proved here.

### 2. Finite correction and finite total coagulations

**Locations:** `auxiliary-process.tex:161–272`, `thm:controlled-path`.

The logarithmic sum is finite at finite times because every visited size is strictly positive and finite and the process is nonexplosive. Its increments are nonnegative. The elementary bound `log(1+r) <= sqrt(r)` and the Stage 1 half-moment estimate yield exactly

\[
 a(t)\leq\frac{H(0)^2}{mN_0}\,b(t)e^{-\kappa C(t)}.
\]

The use of the nonnegative compensator therefore needs no initial or daughter logarithmic moment. The integral tail tends to zero even when the coarser exponential upper bound does not, as the manuscript explicitly explains for finite total clock. This proves the asserted `L^1` convergence.

For parent-dependent daughters, the retained fraction has conditional mean one half in the full construction filtration. The product multiplied by `exp(F(t))` is consequently a local martingale; its deterministic finite-horizon bound makes it a true mean-one martingale on each finite interval. Applying the maximal inequality and then taking the horizon to infinity proves its almost-sure bounded supremum. No uniform integrability at infinite time is being assumed.

The factorization of `N(t)X_t` gives a finite all-time coagulation compensator pathwise. Its factors include `exp(A_infinity)`, but only their pathwise finiteness is used; no unproved exponential moment is needed. Stopping the continuous compensator at a level `L` and using compensation correctly turns finite all-time compensator into finite all-time count. The identity `E K_t = B_c(t)` is separately obtained from the identified marginals and Tonelli. Thus almost-sure finite count and infinite expected total count are compatible, and the proof does not exchange these claims.

The controlled dichotomy also follows: divergent `F` forces size to zero using the bounded martingale product; finite `F` gives finitely many fragmentation events, hence eventual constancy after the finitely many coagulations. No claim that the last coagulation is a stopping time or that subsequent fragmentation is independent of it is made.

### 3. Concrete heavy-tail tests

Take

\[
 n_0=\frac{6}{\pi^2}\sum_{k\geq1}\frac1{k^2}\delta_{e^{-k}}.
\]

This has finite positive count and mass and finite second size moment, but its number-weighted absolute logarithmic moment is infinite. It is therefore inside the constructed Stage 1 solution class and outside the ordinary first-log-moment class. The pathwise LLN and functional CLT still have no difficulty: `Z_0` is a finite random variable on each path, and dividing it by the diverging scale sends it to zero almost surely. The stated ordinary Wasserstein and finite-entropy results appropriately exclude this datum.

For an admissible daughter law with infinite mean log loss, let `K` have probabilities proportional to `k^-2`, let `V=e^-K`, and use the genuinely complementary split measure

\[
 B=\mathbb E[\delta_V+\delta_{1-V}].
\]

It has total count two and mean fraction one half, while the retained log fraction has infinite negative mean. The finite-time Poisson sum is still finite almost surely. The correction and extended transport statements still apply. The truncated strong-law argument gives `Z_t/t -> -infinity`, exactly as claimed, without applying an integrable-jump LLN illegally. The theorem does not assign an ordinary Gaussian limit or a finite geometric-mean prefactor to this example.

These examples can be combined. Neither the compensator bound nor clipped-test transport proof introduces their missing logarithmic moments indirectly.

### 4. Exact extended transport and the parent-dependence boundary

**Locations:** `log-limits.tex:6–106`, `thm:transport` and `rem:adaptive-marks`.

In the selfsimilar case the daughter quantile can be chosen as parent size times the quantile of `B_t/2`. Thus the retained fractions are marks of the stated Poisson random measure independent of the initial size and coagulation driver. The proof does not assert that they are independent of the nonlinear process or of `A_infinity`.

For the ordered coupling, clipped-test differences are nonnegative and increase to the paired difference. This is a valid lower bound on the cost of every coupling, including when separate means are infinite. Consequently the displayed equality is an exact extended cost, not merely an upper bound obtained from one coupling. Its monotone growth to `E A_infinity` and all constant-rate constants check out.

The signed remainder has mass zero, variation bounded by `2b`, and a Lipschitz paired-increment bound. The text expressly avoids extending that statement to separate absolute log moments of its gain and loss. General parent-dependent fractions keep their conditional mean, which is enough for the product martingale, but can depend on prior coagulation. The text correctly restricts the standalone Poisson reference and its limit conclusions to selfsimilar daughters.

### 5. Gaussian, ordinary transport, and general-scale limits

**Locations:** `log-limits.tex:162–328`, `thm:log-limits`, `cor:infinite-log-speed`, and `prop:general-scale-transfer`.

The reference centered unit increments have variance `r E Y^2`, including the count fluctuation. The within-unit total jump magnitude has finite second moment under the same assumption. The tail estimate `u^2 P(V_1>u) -> 0` and the union bound make the interpolation error vanish uniformly after division by `sqrt(T)`. This justifies transferring the iid invariance principle to the compound-Poisson path in `J_1`. The initial condition and nonlinear correction then vanish uniformly under the same scaling, with no moments beyond pathwise finiteness for the initial logarithm.

Ordinary one-time Wasserstein convergence is proved separately. The centered reference's bounded second moments give uniform integrability of its first absolute moments, and adding the initial log and correction costs only their first absolute moments divided by the scale. This avoids assuming a second initial log moment or a second correction moment. The first-moment-only speed proof correctly centers the truncated jump sum and controls the two truncation contributions by `2r E|Y-Y^(L)|`.

For infinite daughter log mean, the truncations are ordered in the needed direction and can be put on a common probability-one event. The Jensen bound tends to `log E Theta=-log 2`. The universal upper speed and the value `-infinity` are therefore justified.

The general-scale proposition is conditional on a reference limit and does not invent a stable domain of attraction. The uniform difference of the two centered paths is bounded by `A_infinity/d_T`; the identity time change then controls their `J_1` distance. No independence of the correction is required.

### 6. Mean log, entropy, and pure coagulation

**Locations:** `log-limits.tex:337–437`, `prop:log-means` and `cor:pure-coag`.

The logarithmic integrability assumptions justify expectations before the exact mean and entropy identities are taken. The number-to-mass Radon–Nikodym derivative is `m/(Nx)`, giving precisely the stated count correction `b-sigma`. The pure-coagulation convention sets the log drift to zero directly, so it does not multiply an infinite daughter log mean by a zero fragmentation rate. The geometric-mean prefactor and exponential error bound follow from the remaining correction, not from the increasing one-time transport cost.

With zero fragmentation, the process is increasing and eventually constant, and its finite limit remains inside the positive finite size space. The same clipped-test argument gives the exact transport cost between two times and to the limiting law even for the heavy initial log example above. Weak convergence of the size law does not require moment convergence.

The Borel formula has the correct additive-kernel clock. Its critical limit is a probability distribution, its `k^-3/2` tail gives infinite arithmetic mean and finite first logarithmic moment, and these facts do not contradict finite mean at each finite time. The manuscript correctly attributes this classical endpoint.

## Primary-source checks

The monodisperse formula matches equation (3) of [Bertoin (2009)](https://www.numdam.org/article/AIHPC_2009__26_6_2073_0.pdf), including the factor `exp(-t)` and parameter `1-exp(-t)`. The branching interpretation is present in Section 2.2 of [Deaconu–Tanré (2000)](https://www.numdam.org/article/ASNSP_2000_4_29_3_549_0.pdf). The contextual description of the mass-weighted LLN/CLT in [Bertoin (2003)](https://ems.press/content/serial-article-files/31511?nt=1) is consistent with its theorem and sampling convention. These are contextual citations, not substitutes for the manuscript's new auxiliary-process proofs.

## Optional improvements

The general-scale path statement could display `(Z_(Ts)-c_T(s))/d_T` and its reference explicitly. The intended rescaling is apparent from the preceding functional theorem, and the proof is valid; this is an optional clarity edit, not an additional issue.

**MAJOR count: 0. MINOR count: 2. Recommendation: accept Stage 2 after correcting S2-ADV-001 and S2-ADV-002. No additional theorem hypothesis or proof reconstruction is required.**
