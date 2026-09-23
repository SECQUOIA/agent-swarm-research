# Independent review of invisible coagulation–fragmentation kinetics

Reviewer: `review_gauge`, 2026-09-06. This review independently checks the algebra and proofs in [the inverse-design note](../ideas/inverse-design.md) and [the invisible-kinetics extension](../results/invisible-kinetics-extension.md). It also proves the proposed extension to every fractional moment. Correctness findings below are conditional on the stated forward solution and observation assumptions. They do not establish novelty.

## 1. Assumptions that matter

- The coagulation kernel is symmetric. Every antisymmetric component is invisible in a quadratic count-rate observation, regardless of the number of preparations.
- Initial rates refer to the continuum population-balance model, with known preparation concentrations and unchanged kinetic coefficients between experiments.
- Full-time conclusions use mass conservation and valid weak balances. Initial count neutrality alone does not imply a constant full trajectory.
- A fixed-mass preparation class permits initial counts to vary. It differs from a class fixing both mass and count. The monodisperse rigidity arguments below require the former.
- For the moment estimates it suffices that the daughter measure is supported in `(0,x)`, has total measure two, and has first moment `x`. A realizable random binary split is sufficient but is not necessary for these estimates.

## 2. Initial-rate identification

Consider

$$r(c,p)=J+c\int b\,dp-\frac{c^2}{2}\iint K\,dp\,dp,$$

for all finitely supported probability measures `p` and positive known concentrations `c`.

With known `J`, equality of two models at one concentration is equivalent to

$$\Delta K(x,y)=a(x)+a(y),\qquad \Delta b(x)=ca(x).$$

Proof: monodisperse preparations give `Δb(x)=c ΔK(x,x)/2`. Equal mixtures of two point masses then give `ΔK(x,y)=[ΔK(x,x)+ΔK(y,y)]/2`. Conversely, substituting these expressions cancels the rate difference. No continuity is needed if pointwise finite coefficients and all finitely supported preparations are available. Two distinct concentrations remove this gauge.

With unknown `J`, two concentrations leave exactly

$$\Delta J=\delta,\qquad
\Delta b=-\delta(c_1^{-1}+c_2^{-1}),\qquad
\Delta K=-2\delta/(c_1c_2).$$

The resulting rate difference at another concentration is

$$\delta(1-c/c_1)(1-c/c_2).$$

A third distinct concentration therefore removes the gauge. Nonnegativity does not imply that a nontrivial admissible gauge always exists. For a baseline with `J,b,K≥0`, its exact admissible interval is

$$-J\le\delta\le
\min\left\{
\frac{\inf_x b(x)}{c_1^{-1}+c_2^{-1}},
\frac{c_1c_2}{2}\inf_{x,y}K(x,y)
\right\}.$$

This interval can be a singleton. In contrast, for known `J` at one concentration, every nonnegative function `a` gives another nonnegative model, absent additional constraints.

### Reconstruction and measurement count

Direct substitution independently verifies

$$K(x,y)=\frac{r(c,\delta_x)+r(c,\delta_y)-r(2c,(\delta_x+\delta_y)/2)-J}{c^2},$$

$$b(x)=\frac{4r(c,\delta_x)-r(2c,\delta_x)-3J}{2c}.$$

With exact `J` and absolute rate errors bounded by `ε`, the respective errors are at most `3ε/c²` and `5ε/(2c)`.

For `q` selectable states, the scheme uses `q+q(q+1)/2` scalar rates, exactly the number of unrestricted symmetric-kernel and linear-rate parameters. Fewer linear scalar observations cannot identify an open set of those parameters. This establishes the stated measurement-count optimality, not noise or finite-time experimental optimality. Unknown `J` requires one extra rate because

$$J=3r(c,\delta_x)-3r(2c,\delta_x)+r(3c,\delta_x).$$

The finite-time error estimate in the inverse-design note also checks: a count-difference error `η` and a valid bound `|N''|≤B` give rate error `η/t+Bt/2`, and its minimizing time is `sqrt(2η/B)` when admissible. This requires `B>0`; zero error or zero curvature cases should be interpreted directly from the original bound.

## 3. Complete shell classification

Let `C` have full row rank, `h≠0`, and suppose `{z>0:Cz=h}` is nonempty. For symmetric `K`, the quadratic rate

$$R(z)=s^Tz-\tfrac12z^TKz$$

vanishes on the shell exactly when

$$K=C^TA+A^TC,\qquad s=A^Th$$

for some matrix `A` of the indicated size.

The positive shell contains a relatively open subset of the affine space, so polynomial vanishing extends to that affine space. If

$$P=C^T(CC^T)^{-1}C,\qquad Q=I-P,$$

the vanishing Hessian on `ker C` gives `QKQ=0`. One explicit initial representation is

$$A=(CC^T)^{-1}CK(I-P/2).$$

It satisfies `CᵀA+AᵀC=K`. The residual is `s−Aᵀh=Cᵀγ`, with `γᵀh=0`. The skew matrix

$$B=\frac{h\gamma^T-\gamma h^T}{\|h\|^2}$$

satisfies `Bᵀh=γ`. Replacing `A` by `A+BC` corrects the residual without changing `K`. The converse follows by substitution. The rank bound `rank K≤2 rank C` follows, but is not a sufficient condition for invisibility. Nonnegativity of physical rates must be imposed separately.

## 4. Exact-time invisible families

For binary count production `S`, universal initial count neutrality at fixed mass `m>0` is equivalent to

$$K(x,y)=xd(y)+yd(x),\qquad S(x)=md(x).$$

The monodisperse preparations `(m/x)δx` give the diagonal relation, and the two-state preparations `(m/(2x))δx+(m/(2y))δy` give the cross relation. This verifies the complete continuum classification directly. Physical nonnegative selection forces `d≥0`.

The full count equation becomes

$$N'=(m-M_1)\int d\,dn.$$

Thus every mass-conserving trajectory at mass `m` retains its initial count. This implication explicitly uses the conserved mass.

The fixed-count family `K=a(x)+a(y), S=ca(x)` similarly gives `N'=(c−N)∫a dn`. The larger sufficient construction

$$K=a(x)+a(y)+xd(y)+yd(x),\qquad S=ca+md$$

gives `N'=(c−N)∫a dn+(m−M₁)∫d dn`. The finite-grid theorem proves completeness on feasible interior grids; it does not alone prove a continuum two-constraint converse.

For `d≡λ`, the additive kernel and constant selection are

$$K=\lambda(x+y),\qquad S=\lambda m.$$

When `M₂` is finite, coagulation contributes `2λmM₂`. Daughter count and mass imply

$$x^2/2\le\int z^2b_x(dz)\le x^2,$$

by Cauchy–Schwarz and `z²≤xz`. Consequently

$$\tfrac32\lambda mM_2\le M_2'\le2\lambda mM_2.$$

Equal splitting attains the lower exponent. This conclusion does not require a realizable pairwise split beyond the displayed daughter-measure conditions; an earlier restriction to actual binary splits was unnecessarily strong.

The entropy estimate `d/dt ∫x log x dn≥(1−log 2)λm²` also checks algebraically. Its use requires justification of the unbounded entropy test. The fractional-moment result below supplies nonstationarity without that extra assumption.

## 5. Sharp inequality for every fractional moment

**Verified theorem.** For `0<p<1` and `x,y>0`,

$$
(2-2^p)(xy^p+yx^p)
\le (x+y)[x^p+y^p-(x+y)^p]
\le xy^p+yx^p. \tag{A}
$$

The lower constant is sharp, with equality exactly at `x=y` in the positive quadrant. Both sides of the lower inequality also vanish on the boundary if zero sizes are allowed. The upper constant is the limiting ratio as one size divided by the other tends to zero.

### Independent calculus proof of the lower bound

Set `u=x/(x+y)`, `v=1−u`, and `A=2^p−1`. The lower bound is equivalent to

$$f(u):=A(u^p+v^p)+(1-A)(u^{p+1}+v^{p+1})\ge1.$$

By symmetry it suffices to take `0≤u≤1/2`. The endpoint values are `f(0)=f(1/2)=1`. For `0<u<1/2`, the sign of `f''(u)` is the sign of

$$ (1-A)(p+1)-A(1-p)R(u),$$

where

$$R(u)=\frac{u^{p-2}+v^{p-2}}{u^{p-1}+v^{p-1}}
=\frac{u^{2-p}+v^{2-p}}{uv(u^{1-p}+v^{1-p})}.$$

As `u` increases toward `1/2`, the numerator strictly decreases because `2−p>1`; both factors in the denominator strictly increase because `0<1−p<1`. Thus `R` strictly decreases from infinity. It follows that `f''` is initially negative and changes sign at most once, from negative to positive.

Also `f'(0+)=+∞` and `f'(1/2)=0`. The second derivative must become positive somewhere: otherwise `f'` would stay positive before the midpoint, contradicting the equal endpoint values of `f`. Therefore `f'` first strictly decreases and then strictly increases to zero. On its increasing portion it is negative; on its decreasing portion it has exactly one zero. Hence `f` first strictly increases and then strictly decreases to its original value. This proves `f(u)>1` for `0<u<1/2`, as required.

The upper bound in (A) follows from `(x+y)^{p+1}≥x^{p+1}+y^{p+1}`. The sharp lower constant follows by taking `x=y`.

The developing agent independently supplied a generalized-binomial proof: after `x=1+t,y=1−t`, the gap has coefficients

$$a_k={p\choose2k-1}\left[2-2^{p+1}+\frac{2^p(p+1)}{2k}\right].$$

I checked this algebra, absolute convergence at `t=1`, and the argument using the coefficients' single sign change and zero sum. It provides a second valid proof. The inequality may be established in the classical power-inequality literature; neither proof establishes novelty.

### Consequence for the dynamics

Under the mass-conserving weak-solution assumptions in the extension note, every `0<p<1` satisfies

$$M_p(t)\le M_p(0)e^{-\kappa_p\lambda mt},\qquad
\kappa_p=3-2^p-2^{1-p}>0. \tag{B}$$

Indeed, `M_p≤N^{1−p}m^p` by Hölder. The coagulation loss is at least `(2−2^p)λmM_p` by (A). Jensen's inequality against the probability measure `b_x/2` gives

$$\int z^p b_x(dz)\le2^{1-p}x^p,$$

so fragmentation gains at most `(2^{1−p}−1)λmM_p`. Their sum proves (B). Monodisperse initial data and equal splitting attain equality in the derivative at zero, so the coefficient is optimal in a uniform estimate with prefactor one.

The coefficient is symmetric under `p↦1−p` and is uniquely maximized at `p=1/2`, where it equals `3−2√2`. This identifies the fastest uniform fractional-moment decay coefficient; it does not assert that every particular observation-window bound is optimized by `p=1/2`.

For rigor, use bounded concave tests `f_R(x)=min{x^p,R}`. Their coagulation loss is nonnegative and at most `min{x^p,y^p}`, giving the common integrable majorant `λ(xy^p+yx^p)`. Since `f_R(z)/z` is nonincreasing, support and mass conservation imply a nonnegative daughter increment, bounded above by `2^{1−p}x^p`. Dominated convergence in the integrated weak equation establishes absolute continuity and the claimed differential inequality without additional moments. If bounded Lipschitz tests are required, first replace `x^p` by `(x+ε)^p−ε^p` and then let `ε` decrease to zero.

In particular,

$$n_t([\varepsilon,\infty))\le\varepsilon^{-p}M_p(0)e^{-\kappa_p\lambda mt},$$

$$\int_{(0,R]}x\,dn_t\le R^{1-p}M_p(0)e^{-\kappa_p\lambda mt}.$$

These imply absence of any stationary positive finite-mass, finite-count state on `(0,∞)`, weak convergence of number measures to `Nδ₀` on `[0,∞)`, and escape of mass probability measures to infinity. They are long-time statements and do not assert finite-time loss of mass or count.

## 6. Rigidity with an additional moment

Suppose both count and one fractional-moment derivative vanish for every finitely supported preparation of mass `m`, with physical nonnegative rates. The fixed-mass classification gives `K=xd(y)+yd(x), S=md(x), d≥0`. For the monodisperse preparation `(m/x)δx`, (A) and Jensen give

$$M_p'(0)\le-\kappa_p m^2d(x)x^{p-1}.$$

Thus `d=0` everywhere, so both physical rates vanish. The second-moment alternative also checks, with `M₂'(0)≥3m²xd(x)/2`.

These are universal preparation results, not recovery theorems from one trajectory. If count and mass are both fixed, only one monodisperse size is available and this proof cannot establish global rigidity.

## 7. Moving windows, entropy, and robustness

The moving-window corollary in the developing note checks. For every `0<v<λm log 2`, the number above `ε₀e^(−vt)` and mass below `R₀e^(vt)` tend to zero exponentially. The exponents in the two estimates are respectively `κ_pλm−pv` and `κ_pλm−(1−p)v`. The limits

$$\lim_{p\downarrow0}\frac{\kappa_p}{p}=\log2,
\qquad \lim_{p\uparrow1}\frac{\kappa_p}{1-p}=\log2$$

allow separate choices of `p` for the two bounds. The endpoint velocity is not covered and no matching front-speed claim follows.

Dividing the pair inequality by `1−p` and letting `p` increase to one proves

$$h(q)\ge4(\log2)q(1-q),\qquad
h(q)=-q\log q-(1-q)\log(1-q).$$

Therefore, when the entropy balance is valid, the earlier estimate improves to the sharp derivative bound

$$\frac{d}{dt}\int x\log x\,dn\ge\lambda m^2\log2.$$

Equal splitting and monodisperse initial data attain equality at time zero. The limiting algebra does not itself justify the unbounded entropy balance.

The proposed robust extension is also correct. Suppose

$$a(x+y)\le K(x,y)\le A(x+y),\qquad0\le S(x)\le\sigma,$$

with `0<a≤A<∞`, fixed conserved mass `m>0`, and the same daughter assumptions. Then

$$M_p'\le-\gamma_pM_p,\qquad
\gamma_p=am(2-2^p)-\sigma(2^{1-p}-1)
=(2^{1-p}-1)(am\,2^p-\sigma).$$

If `σ<2am`, a choice of `p` sufficiently close to one gives `γ_p>0`. This excludes a stationary finite-count, positive finite-mass state. Count conservation is not needed: `N(t)≤N(0)e^(σt)` and the upper kernel bound provide locally integrable majorants for the same truncation proof. A related necessary condition for any stationary state is

$$\int xS(x)\,dn(x)\ge2am^2.$$

Indeed, stationarity gives `∫Sx^p dn≥am 2^p M_p`; dominated convergence as `p` increases to one proves the claim. The argument makes no conclusion at the threshold `σ=2am`.

## 8. Proposed logarithmic number-law theorem: additional review, 2026-09-06

This subsection checks a later proposed theorem for equal splitting, `K=λ(x+y)`, `S=b=λm`, conserved mass `m`, and conserved count `N`. Let `ρ_t` be the number probability distribution of `Z=log x`, and suppose initially `∫|log x|dn<∞`.

The exact weak generator decomposition is

$$\partial_t\rho_t=2b(T_{-\log2}\rho_t-\rho_t)+R_t,$$

where `T` denotes translation and

$$R_t\varphi=\frac\lambda N\iint x[\varphi(\log(x+y))-\varphi(\log x)]\,dn_t(x)dn_t(y).$$

This follows by symmetrizing the additive coagulation kernel: its two linear loss terms combine with fragmentation's loss term to give `−2bρ_t`. The remainder is a finite signed measure of total mass zero, with total variation at most `2b`.

For a bounded 1-Lipschitz function on logarithmic size,

$$|R_t\varphi|\le\frac\lambda N\iint x\log(1+y/x)\,dn_t(x)dn_t(y)
\le\frac\lambda N M_{1/2}(t)^2,$$

because `log(1+r)≤√r`. This last inequality follows by writing `r=u²`: the derivative of `u−log(1+u²)` is `(u−1)²/(1+u²)≥0`.

**Technical qualification.** Under only the assumed logarithmic first moment, the positive and negative components defining `R_t` can have infinite first absolute logarithmic moments, since they involve `x|log x|`. It is not justified to treat `R_t` directly as an element of the usual space of signed measures with finite first absolute moment. The displayed Lipschitz bound is a bound on its compensated action, not a proof of that absolute-moment property.

The following workaround verifies the intended result without an additional moment assumption. Let `P_t` be the translation semigroup of `−(log 2)P_{2bt}`, where `P` is Poisson. First establish the backward-test identity for bounded Lipschitz `φ`:

$$\rho_t\varphi-(P_t\rho_0)\varphi
=\int_0^tR_s(P_{t-s}\varphi)\,ds.$$

The backward test is bounded, and the Poisson semigroup preserves its Lipschitz constant. Thus every displayed integral is well defined and the remainder bound is available.

Next establish finite first moments of `ρ_t` separately. For `φ_L(z)=min{(-z)_+,L}`, the remainder is nonpositive and the translation generator increases this test by at most `2b log 2`. Monotone convergence gives

$$\int(-z)_+\,d\rho_t\le\int(-z)_+\,d\rho_0+2bt\log2.$$

Also `∫z_+ dρ_t≤m/N`. The reference Poisson translation has a finite first moment as well. Therefore clipping arbitrary Lipschitz tests and passing to the limit supplies the full Wasserstein dual estimate

$$W_1\!\left(\rho_t,\operatorname{Law}(Z_0-(\log2)P_{2bt})\right)
\le\frac{M_{1/2}(0)^2}{2\kappa mN},\qquad\kappa=3-2\sqrt2,$$

where the reference Poisson variable is independent of `Z₀`. This checks the proposed constant. In particular the upper bound is at most `1/(2κ)` by Cauchy–Schwarz.

This estimate implies the logarithmic number-law speed `−2b log 2` in probability and in Wasserstein distance after division by `t`. It also implies

$$\frac{Z_t+2bt\log2}{\sqrt t}
\ \Longrightarrow\ \mathcal N(0,2b(\log2)^2),$$

with the perturbation from the scaled Poisson reference bounded by a constant times `t^(−1/2)` in `W₁`. The initial logarithmic variable contributes at most `E|Z₀|/√t`; no initial logarithmic second moment is needed. These statements concern distributions, without asserting that the physical deterministic population balance already supplies a particular tagged-particle path coupling.

There is also a useful ordering consequence. For bounded increasing tests, `R_tφ≥0`, and the Poisson semigroup preserves monotonicity. Hence `ρ_t` stochastically dominates the reference translated law. Since both have finite first moments, their `W₁` distance equals their mean difference. By clipped-test passage in the same identity, this difference equals the integrated positive logarithmic coagulation drift. It is nondecreasing in time and bounded by the preceding constant.

The generator algebra, bounded-test workaround, moment propagation, constants, and limiting-distribution implications have been independently checked here. A final theorem should specify the weak-solution class permitting bounded time-dependent tests, or derive that use from its integrated weak formulation. Novelty of this logarithmic law has not been assessed in this subsection.

## 9. Literature and remaining limits

I independently inspected [Laurençot (2019), Equation (1.8)](https://www.numdam.org/item/10.1016/j.anihpc.2019.06.003.pdf). It describes stationary solutions for an affine additive coagulation kernel with selection rate `a(x)=A₀x` and daughter density `2/y`, citing Dubovskii and Stewart (1996). This differs from the constant per-particle selection used above. Terminology such as “constant fragmentation” can refer to a constant binary fragmentation kernel whose integrated selection rate is linear; it must not be treated as synonymous with constant selection.

No novelty conclusion about the book section “Additive Coagulation and Constant Fragmentation” is based on an unauthorized mirror. Its title alone cannot establish its full scope. The general power inequality, polynomial shell algebra, and moment technique may have prior forms. A literature review of critical homogeneous coagulation–fragmentation dynamics remains necessary before publication claims.

The review found no algebraic counterexample to the stated results. It identified necessary symmetry, preparation-class, positivity, and weak-solution qualifications, and removed an unnecessary restriction on the daughter law. No forward existence theorem has been independently proved here.
