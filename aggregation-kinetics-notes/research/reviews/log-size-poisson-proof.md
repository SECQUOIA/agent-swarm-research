# Independent proof review: logarithmic compound-Poisson approximation

Reviewer: `review_gauge`, 2026-09-06. Reviewed the full [log-size theorem](../results/log-size-poisson-limit.md), including its generalized self-similar daughter law, stochastic-order refinement, and weak limits without an initial logarithmic moment. The developing team then proposed the stronger moment-free transport statement. Its complete independent verification is recorded below so that the result does not rely on review of a superseded version.

**Verdict.** The generator decomposition, uniform transport estimate, exact transport identity, limiting-distribution transfer, Gaussian variance, and integrable-case mean and entropy identities are correct under the stated global mass-conserving weak-solution assumptions. The transport theorem requires neither an initial logarithmic moment nor a logarithmic moment of the daughter fractions, provided transport is defined as an infimum of expected distances on arbitrary probability laws. The ordinary space of probability measures with finite first moment must be distinguished from this extended transport-cost formulation.

## 1. Model and normalization

The kernel is `K(x,y)=λ(x+y)`, the fragmentation selection rate is `b=λm`, and initial count and mass are finite positive `N,m`. The count balance gives `N'=−λmN+bN=0`. The daughter measure is self-similar: it is the image of a fixed measure `B` on `(0,1)` under `θ↦xθ`, with

$$B((0,1))=2,\qquad\int\theta B(d\theta)=1.$$

No joint realization as two daughter fractions is needed for the proof. Let `Y=log Θ`, where `Θ` has probability law `B/2`. Then `Y` is a finite negative random variable almost surely, even when its absolute mean is infinite.

Write `ρ_t=(log)#n_t/N`. Let `W_t` be the compound-Poisson process with rate `2b` and jump law `Y`, and set

$$\bar\rho_t=\operatorname{Law}(Z_0+W_t),\qquad Z_0\sim\rho_0,$$

with independence in this reference construction. Since the number of jumps on a finite interval is finite almost surely, this law exists without a jump-moment assumption.

## 2. Exact generator decomposition

For a bounded continuous test `φ` on the logarithmic axis, symmetry gives the coagulation contribution to its normalized expectation as

$$\frac\lambda N\iint x[\varphi(\log(x+y))-\varphi(\log x)-\varphi(\log y)]\,dn_t(x)dn_t(y).$$

The last term is `−b〈φ,ρ_t〉`. Adding fragmentation gives

$$\frac d{dt}\langle\varphi,\rho_t\rangle
=2b\langle\mathbb E[\varphi(\cdot+Y)-\varphi(\cdot)],\rho_t\rangle+R_t\varphi,$$

where

$$R_t\varphi=\frac\lambda N\iint x[\varphi(\log(x+y))-\varphi(\log x)]\,dn_t(x)dn_t(y). \tag{R}$$

Thus the reference jump rate is `2b`, not `b`. The remainder is a finite signed measure of mass zero and total variation at most `2b`.

For every bounded 1-Lipschitz test,

$$|R_t\varphi|\le a(t):=\frac\lambda N\iint x\log(1+y/x)\,dn_t(x)dn_t(y)
\le\frac\lambda N H(t)^2,$$

where `H(t)=∫√x dn_t`. The last inequality uses `log(1+r)≤√r`; after writing `r=u²`, its proof is that the derivative of `u−log(1+u²)` is `(u−1)²/(1+u²)≥0`.

The independently verified fractional-moment result applies to this expected daughter measure by Jensen's inequality, giving

$$H(t)\le H_0e^{-\kappa bt},\qquad\kappa=3-2\sqrt2.$$

Consequently

$$\int_0^t a(s)\,ds
\le A_0(1-e^{-2\kappa bt}),\qquad
A_0=\frac{H_0^2}{2\kappa mN}\le\frac1{2\kappa}. \tag{A}$$

The constants and all factors of two check.

## 3. Weak variation of constants and the signed-moment issue

Let `P_tφ(z)=Eφ(z+W_t)`. It preserves sup norms, Lipschitz constants, and monotonicity. Its generator is bounded on bounded continuous functions. The integrated weak equation therefore permits the backward test `P_{t-s}φ`, giving

$$\langle\varphi,\rho_t\rangle-\langle\varphi,\bar\rho_t\rangle
=\int_0^t R_s(P_{t-s}\varphi)\,ds. \tag{D}$$

This bounded-test identity is sufficient for every argument below. It avoids imposing a first absolute moment on the signed remainder. Such a moment does not follow from a first logarithmic moment of the number law: the two components of `R_s` carry an additional factor `x`, and can have infinite `x|log x|` moment.

A finite-total-variation interpretation of (D) is also available, but should be justified rather than confused with a finite-first-moment interpretation. Total event rates bound the weak derivative of `n_t` in total variation, so its integrated weak equation gives total-variation Lipschitz continuity. Truncating the weight `x` in (R) gives total-variation continuous remainder approximants. Finite mass makes them converge pointwise in total variation to `R_t`. The uniform bound `2b` then supplies a measurable integrable remainder. Either this argument or the bounded-test route repairs the relevant functional-analytic detail.

## 4. Stochastic order and an exact transport identity without moments

Every coagulation shift in (R) is upward. Thus `R_sφ≥0` for bounded increasing `φ`. Applying (D) and preservation of monotonicity shows that `ρ_t` stochastically dominates `barρ_t`. Bounded increasing Lipschitz tests already suffice to establish this order; discontinuous tests need not be inserted into a weak equation whose test class excludes them.

Let `Q_t(U)` and `barQ_t(U)` be the quantile coupling with `U` uniform on `(0,1)`. Stochastic order gives

$$Q_t(U)\ge\bar Q_t(U)\quad\text{almost surely}.$$

Define `c_L(z)=max{−L,min{z,L}}`. These bounded increasing 1-Lipschitz tests give

$$\mathbb E[c_L(Q_t(U))-c_L(\bar Q_t(U))]
=\int_0^t R_s(P_{t-s}c_L)\,ds.$$

For any ordered finite real numbers `z₂≥z₁`, the difference `c_L(z₂)−c_L(z₁)` is the length of the interval `[z₁,z₂]` inside `[−L,L]`. It increases to `z₂−z₁` as `L` increases. The same property holds after applying any common finite random shift `W_{t-s}`. Therefore monotone convergence applies on both sides, including all the time, size, and shift integrals, and yields

$$\mathbb E[Q_t(U)-\bar Q_t(U)]=\int_0^t a(s)\,ds. \tag{E}$$

No expectation of either quantile separately is used. In particular, this is valid even when both have infinite absolute first moments or `E|Y|=∞`.

Define the transport cost on arbitrary probability laws by

$$\mathcal W_1(\alpha,\beta)=\inf\mathbb E|X-X'|,$$

where the infimum is over their couplings and may be infinite. The ordered quantile coupling attains the right side of (E). It is optimal: for any competing coupling, the difference of expectations of `c_L` is at most its expected absolute displacement; pass to the limit in these bounded-test lower bounds. Hence

$$\mathcal W_1(\rho_t,\bar\rho_t)
=\int_0^t a(s)\,ds
\le A_0(1-e^{-2\kappa bt}). \tag{T}$$

This verifies the moment-free main theorem and its exact identity. The cost is nondecreasing in time and has a finite limiting offset. Finite transport cost between these two laws does not imply that either belongs to the usual space `P₁` of laws with finite first absolute moment.

## 5. Distributional limits and assumptions

For arbitrary deterministic centerings `c_t` and scales `a_t>0` increasing to infinity, the same coupling gives

$$\mathbb E\left|\frac{Q_t(U)-c_t}{a_t}-\frac{\bar Q_t(U)-c_t}{a_t}\right|\le A_0/a_t.$$

Consequently any weak scaling limit of the reference law transfers to the population law. This is a statement about one-time distributions and does not assert a tagged-particle process or pathwise approximation. It also does not require an initial logarithmic moment: `Z₀/a_t` tends to zero in probability because `Z₀` is finite almost surely.

If `E|Y|<∞`, put `μ=EY<0`. The compound-Poisson law of large numbers and the preceding coupling give

$$Z_t/t\longrightarrow2b\mu$$

in probability. If additionally `ν₂=E(Y²)<∞`, then

$$\frac{Z_t-2b\mu t}{\sqrt t}\Longrightarrow\mathcal N(0,2b\nu_2).$$

The variance contains the second raw jump moment `E(Y²)`, not merely `Var(Y)`, because the jump count is Poisson. Expansion of the centered compound-Poisson characteristic exponent gives `−bu²ν₂`, as stated in the theorem.

The jump law's second moment is not needed merely to state a conditional transfer of a non-Gaussian limit: whenever the compound-Poisson reference has a specified stable or other weak limit under known centering and diverging scaling, (T) transfers that same limit. An unconditional claim identifying a stable-law domain of attraction would need separate hypotheses and a proof or appropriate primary reference.

If `E|Z₀|<∞` and `E|Y|<∞`, both comparison laws belong to `P₁`, as verified below. Under the jump second-moment assumption, the Gaussian convergence then also holds in ordinary `W₁`. The centered compound-Poisson variables have bounded second moments, which gives uniform integrability of their first absolute moments. The initial variable divided by `√t` tends to zero in `W₁`, and the transport perturbation contributes at most `A₀/√t`.

The explicit speed bound also checks:

$$W_1(\operatorname{Law}(Z_t/t),\delta_{2b\mu})
\le\frac{A_0+\mathbb E|Z_0|}{t}+\sqrt{\frac{2b\nu_2}{t}}.$$

Weak convergence without an initial log moment must not be upgraded to `P₁-W₁` convergence. In that case the first absolute moments may remain infinite.

## 6. Integrable logarithmic observables

Assume `E|Z₀|<∞` and `E|Y|<∞`. The positive log moment is bounded by `m/N`. For `φ_L(z)=min{(-z)_+,L}`, the remainder is nonpositive and each downward reference jump increases the test by at most `|Y|`. The integrated equation and monotone convergence give

$$\int(-z)_+\,d\rho_t\le\int(-z)_+\,d\rho_0+2bt\mathbb E|Y|.$$

This proves membership in `P₁` without assuming its propagation in advance. Clipped identity tests, using the same paired-displacement bounds, give

$$\mathbb E Z_t=\mathbb E Z_0+2b\mu t+\int_0^t a(s)\,ds.$$

Hence the mean log size after subtraction of its deterministic drift has a finite limit. The corresponding geometric mean has a finite positive limiting prefactor multiplying `exp(2bμt)`.

For raw number and mass probabilities `η_t=n_t/N` and `π_t=xn_t/m`, the Radon–Nikodym derivative is `dη_t/dπ_t=m/(Nx)` on positive sizes. Therefore

$$D_{\mathrm{KL}}(\eta_t\Vert\pi_t)=\log(m/N)-\mathbb E Z_t.$$

This checks the direction and sign of the relative entropy. It grows at rate `−2bμ`, with the finite correction specified by the mean identity. Without the logarithmic integrability assumptions this divergence can be infinite and the finite asymptotic correction statement is unavailable.

For equal splitting, the drift and variance rates are `−2b log 2` and `2b(log 2)²`. For a deterministic unequal split `r,1−r`, they are `b log(r(1−r))` and `b[(log r)²+(log(1−r))²]`. Both examples check.

## 7. Scope and final audit

- The half-moment estimate is independent of daughter-log moments and remains valid for the self-similar expected daughter measure assumed here.
- Translation invariance of the reference requires a parent-independent daughter-fraction measure. The proof does not identify a fixed compound-Poisson reference for a general parent-dependent daughter law.
- The uniform bound is in log-size transport, so it does not control raw-size exponential moments or the mass carried by extreme tails. There is no conflict with conserved arithmetic mean or persistent nonlinear coagulation.
- Neither a local central limit theorem nor a density approximation follows. With monodisperse initial data and equal splitting, the pure-fragmentation reference retains a logarithmic lattice; the full nonlinear law remains atomic on positive dyadic rational multiples of the initial size, but coagulation need not preserve a log lattice. **Amendment, 2026-09-07:** Stage 2 manuscript review identified that the original sentence did not distinguish these two support properties. This correction preserves the no-density conclusion.
- The assumed global weak-solution theory and finite-time conservation are not proved by this review.
- Novelty has not been certified. Compound-Poisson limits, transport duality, stochastic order, and fragmentation limit theorems have established precedents; the separate literature audit must assess the specific nonlinear displacement result.

No mathematical counterexample was found. The principal correction was to avoid assuming a finite absolute first moment for the signed remainder. The bounded-test and ordered-coupling proofs above resolve that issue and yield the stronger moment-free transport theorem.
