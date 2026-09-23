# A surface-diffusion crossover for channels with nearly inactive exchange points

Candidate theoretical result, 2026-09-06, verified within the stated mathematical model. The central prediction is a singular dependence of axial dispersion on weak lateral surface diffusion, even when equilibrium adsorption and mean tracer speed are unchanged. Independent agents have checked the cell formula, crossover constant, finite-bulk bound and localization for general rate profiles. A targeted literature audit has not located this particular transport crossover; publication novelty is still under review.

The derivation and initial calculations are in [the exploration note](exploration-interfaces.md), independent verification in [the cell-problem review](review-singular-exchange.md) and [the localization review](review-localization.md), and the closest literature in [the prior-art audit](singular-exchange-prior-art.md).

## Model and assumptions

Let Ω be a fixed bounded connected smooth two-dimensional channel cross-section, with area A and boundary Γ of perimeter P. The longitudinal velocity is u(y), independent of the axial coordinate, and u∈L²(Ω). The bulk transverse diffusivity D_b>0 is fixed. Adsorbed particles have zero longitudinal advective velocity and diffuse along the transverse wall coordinate s with diffusivity D_s>0.

The desorption rate and adsorption coefficient are

\[
 k_\delta(s)=\delta+k_0(s),\qquad k_a(s)=Kk_\delta(s),\qquad K>0.
\]

Thus K is a constant equilibrium affinity with dimensions length. Assume k₀ is a fixed nonnegative C² function on Γ, with a nonempty finite set of isolated zeros s_j, each a nondegenerate minimum:

\[
 k_0(s_j+r)=a_jr^2+o(r^2),\qquad a_j>0.
\]

There are no other zeros. The minimum rate δ is nonnegative. These assumptions exclude a finite wall interval with zero exchange. Several disconnected boundary components are allowed if each satisfies these conditions or has a strictly positive k₀.

The invariant bulk and wall measures are dy/Z and Kds/Z, where

\[
 Z=A+KP,\qquad V=\frac1Z\int_\Omega u(y)\,dy.
\]

Neither equilibrium adsorption nor the mean tracer speed V depends on D_s or δ. Both adsorption and desorption slow together near s_j; the heterogeneity is kinetic.

Let D_flow be the flow-induced part of the long-time axial diffusivity, with Var X(t)∼2D_eff t. Independent axial molecular diffusivities add their stationary average to D_flow and do not alter the result below.

## Finite-bulk theorem and crossover

Define

\[
 H_{D_s,\delta}=-D_s\partial_s^2+k_\delta(s),\qquad
 I(D_s,\delta)=\int_\Gamma H_{D_s,\delta}^{-1}1\,ds,
 \qquad B=\frac{KV^2}{Z}.
\]

There is a constant C, depending on the fixed geometry, rates, u, K and D_b, such that

\[
 \boxed{D_{\rm flow}=B I(D_s,\delta)+R(D_s,\delta),
 \qquad 0\le R(D_s,\delta)\le C.} \tag{1}
\]

The bound is uniform for sufficiently small D_s>0 and all δ≥0. It is not uniform as D_b→0. In fact, the regular correction has the limit

\[
 R(D_s,\delta)\longrightarrow R_0
 =\frac{D_b}{Z}\int_\Omega|\nabla f_0|^2, \tag{1a}
\]

uniformly over δ≥0, where f₀ is the mean-zero solution of

\[
 -D_b\Delta f_0=u-V,\qquad D_b\partial_n f_0=-KV.
\]

Thus the limiting regular bulk correction is independent of the heterogeneous rate profile.

In the joint limit D_s→0 and δ→0, with each

\[
 \zeta_j=\frac{\delta}{\sqrt{a_jD_s}}
\]

remaining in a bounded interval, the scalar surface problem gives

\[
 \boxed{\displaystyle
 I(D_s,\delta)\sim D_s^{-1/4}
 \sum_j a_j^{-3/4}\mathcal C(\zeta_j),
 \qquad
 \mathcal C(\zeta)=\frac\pi2
 \frac{\Gamma((\zeta+1)/4)}{\Gamma((\zeta+3)/4)}.} \tag{2}
\]

Equations (1) and (2) establish the same leading crossover at every fixed positive bulk diffusivity. If V≠0, D_flow diverges as D_s^{-1/4} at δ=0. If V=0, B=0 and this singular contribution is absent. The scalar approximation (2) has error o(D_s^{-1/4}); C² regularity alone does not make that error O(1). The bounded and convergent bulk correction in (1)–(1a) is defined by subtracting the **exact** scalar integral I.

At an exact zero, C(0)=4.647476009400967…. For large ζ, C(ζ)∼π/√ζ. The latter matches the immobile-wall integral π/√(a_jδ) when δ also tends to zero. For fixed positive δ, the limiting answer depends on the full function kδ, and replacing it by only its local quadratic minimum is generally incorrect.

## Why the bulk contribution stays bounded

The reversible transverse process has unnormalized dissipation

\[
 E(f,h)=D_b\int_\Omega|\nabla f|^2
 +KD_s\int_\Gamma|h'|^2
 +K\int_\Gamma k_\delta(h-f_\Gamma)^2.
\]

Here fΓ is the trace of f. Its centered velocity forcing is

\[
 F(f,h)=\int_\Omega(u-V)f-KV\int_\Gamma h.
\]

The cell variational principle is ZD_flow=sup(2F−E). Writing q=H^{-1}1 and maximizing exactly over h yields

\[
 ZD_{\rm flow}=KV^2I+
 \sup_{\int_\Omega f=0}\left[2L(f)-D_b\|\nabla f\|_2^2-KQ(f_\Gamma)\right], \tag{3}
\]

\[
 L(f)=\int_\Omega(u-V)f-KV\int_\Gamma k_\delta q f_\Gamma,
\]

\[
 Q(v)=\inf_h\left[D_s\int_\Gamma|h'|^2+
 \int_\Gamma k_\delta(h-v)^2\right]\ge0.
\]

The gauge in (3) is legitimate because ∫Γkδq=P and ∫Ω(u−V)=KPV. Choosing f=0 proves R≥0.

A partition of unity around the quadratic minima, together with the harmonic-oscillator inequality, gives

\[
 \lambda_{\min}(H)\ge\delta+c\sqrt{D_s}.
\]

The partition derivative error is O(D_s), smaller than the local √D_s bound. Multiplying Hq=1 by kδq and integrating gives the exact identity

\[
 \|k_\delta q\|_2^2+D_s\int_\Gamma k_\delta|q'|^2
 =P+\frac{D_s}{2}\int_\Gamma k_0''q^2. \tag{4}
\]

The spectral bound makes D_s‖q‖² uniformly bounded, so (4) bounds ‖kδq‖₂ uniformly. Trace and Poincaré inequalities imply |L(f)|≤M‖∇f‖₂, uniformly. Dropping the nonnegative Q in (3) and maximizing 2Mx−D_bx² proves R≤M²/(ZD_b). This establishes (1) without assuming the bulk is well mixed.

For (1a), first obtain I=O(D_s^{-1/4}) by splitting ∫q into intervals of width D_s^{1/4} around the zeros and their complement. Cauchy–Schwarz, the spectral lower bound, and ∫kδq²≤I bound both pieces by a constant times √I D_s^{-1/8}. Hence D_s‖q‖²≤D_sI/λ_min=O(D_s^{1/4}). Equation (4) and ∫kδq=P then give ‖kδq−1‖²=O(D_s^{1/4}). Therefore L converges to L₀(f)=∫Ω(u−V)f−KV∫Γf in the bulk energy dual norm. Since Q≥0, dropping Q gives the upper limit of (3). For its lower limit, insert any fixed smooth f and use Q(fΓ)≤D_s∫Γ|fΓ′|²→0, then use density. The limiting variational problem is exactly the Neumann problem for f₀. This proof does not require subtracting a local approximation from I.

## Why a harmonic oscillator appears

Near s_j, the surface diffusion length and relaxation rate are

\[
 \ell_j=(D_s/a_j)^{1/4},\qquad
 \lambda_j=\sqrt{a_jD_s}.
\]

The change s−s_j=ℓ_jy converts H locally to λ_j(−∂²_y+y²+ζ_j). Its integrated inverse contributes ℓ_j/λ_j=D_s^{-1/4}a_j^{-3/4} times the dimensionless crossover.

This localization follows by splitting the wall into disjoint fixed neighborhoods of the minima and the remaining region. Dirichlet conditions at the artificial cuts restrict the resolvent variational space and give a lower bound; allowing independent Neumann pieces enlarges it and gives an upper bound. On each small neighborhood, (a_j−η)r²≤k₀≤(a_j+η)r². On the remaining region k₀ is bounded below, so its integrated resolvent is O(1). Rescaled local intervals expand to the real line. Their oscillator energies uniformly control ∫(1+y²)|q|², including with free endpoints. Weighted Cauchy–Schwarz then bounds integrated absolute tails beyond |y|=L by O(L^{-1/2}). Compactness and these tails show that the Dirichlet and Neumann integrated inverses have the same whole-line limit. First taking D_s→0 and then η→0 gives (2), uniformly for bounded ζ_j. The [localization review](review-localization.md) supplies the full proof, including uniformity and the energy-space treatment of the constant source on the real line.

The whole-line value is explicit because the double-integrated Mehler kernel is

\[
 \int_{\mathbb R^2}e^{-t(-\partial_y^2+y^2)}(y,z)\,dy\,dz
 =\sqrt{\frac{2\pi}{\sinh2t}}.
\]

Thus C(ζ)=∫₀∞e^{-ζt}√(2π/sinh2t)dt. Substituting r=e^{-4t} evaluates this as the gamma ratio in (2). Harmonic-oscillator killing is established mathematics; the candidate contribution is its controlled connection to finite-bulk axial transport with heterogeneous surface kinetics.

## Physical prediction and checks

A rate minimum δ is regularized by surface motion once

\[
 \delta\lesssim\sqrt{a_jD_s}.
\]

The relevant length is the local exchange layer ℓ_j, not the whole wall perimeter. Within this regime, decreasing surface mobility can strongly increase axial band broadening without changing mean retention or equilibrium surface coverage. A candidate experiment would compare coatings with the same equilibrium affinity and measured rate-curvature a_j while varying surface mobility or the minimum exchange rate. A nonzero rate floor produces the crossover in (2), avoiding reliance on physically exact zero rates.

The model requires a regime in which lateral surface diffusion remains an appropriate continuum description at scale ℓ_j. It also requires longitudinally uniform coating properties and fixed positive bulk transverse diffusivity. Molecular discreteness, axial coating variation, and simultaneous loss of bulk mixing are outside this theorem.

Independent finite-difference calculations of k(s)=2(1−cos s)+δ recover C(0) and its ζ dependence. A separate finite-volume bulk–surface calculation confirms a bounded bulk correction. The reproducible checks are in [the script](../scripts/check_surface_exchange.py) and [its recorded results](../results/surface-exchange-checks.json); the [independent review](review-singular-exchange.md) records additional fresh checks and their limits.

## Corollary: optimal isotropic surface mobility at weak flow

Suppose surface diffusion is isotropic: the same D_s controls transverse wall motion and axial molecular diffusion of the adsorbed tracer. Take δ=0 and u=εu₀, with a dimensionless flow amplitude ε→0 and V₀=(∫Ωu₀)/Z≠0. Define

\[
 p_s=KP/Z,\qquad
 A_0=\frac{KV_0^2}{Z}\mathcal C(0)\sum_j a_j^{-3/4}.
\]

With fixed bulk axial diffusivity D_b^x, the total coefficient is

\[
 D_{\rm eff}=\frac A ZD_b^x+p_sD_s
 +\varepsilon^2\left[A_0D_s^{-1/4}(1+o(1))+O(1)\right].
\]

At specified weak flow, the globally minimizing surface diffusivity therefore satisfies

\[
 \boxed{\displaystyle
 D_s^*\sim\left(\frac{A_0\varepsilon^2}{4p_s}\right)^{4/5},
 \qquad
 \min_{D_s>0}D_{\rm eff}-\frac A ZD_b^x
 \sim5p_sD_s^*.} \tag{5}
\]

This is a consequence of the singular transport law, not a separate claim that optimizing diffusion is new. Surface motion reduces kinetic band broadening but adds axial Brownian spreading; their balance gives the fractional weak-flow exponent 8/5.

For verification without differentiating an asymptotic expansion, set L=(A₀ε²/(4p_s))^{4/5} and x=D_s/L. The excess diffusivity divided by p_sL converges on compact x intervals to x+4x^{-1/4}, whose unique minimizer is x=1 and minimum is 5. Nonnegativity of flow dispersion and a test value D_s=L bound any global minimizer from above by a constant times L. The divergent scalar integral excludes x→0. These bounds localize the global minimizer and justify (5). The independent reviewer checked this argument.

A positive rate floor changes the optimum once it is comparable to √(a_jD_s^*). Formula (5) requires an exact zero or a floor asymptotically smaller than that scale. It also assumes that changing D_s leaves k₀, K and bulk diffusivity fixed.

The [surface-mobility optimization note](optimal-surface-mobility.md) develops the finite-floor transition, including an exact finite-bulk threshold, the universal scaled onset 4/π, and an independently reviewed optimizer law.

## Novelty and verification boundary

Reversible-adsorption Taylor dispersion is established in [Levesque et al. (2012)](https://arxiv.org/abs/1211.5224), and surface transport was already included in Dill and Brenner's generalized Taylor-dispersion theory. The zero-surface-diffusion model reduces to established multirate mass transfer. Heavy-tailed trapping, anomalous variance, and equilibrium-versus-injected initialization effects are not new claims here. In particular, the factor-of-two variance difference for a quadratic zero agrees with established renewal results in [Akimoto, Cherstvy and Metzler (2018)](https://arxiv.org/abs/1803.07232).

The candidate result is the **explicit weak-surface-diffusion crossover for spatially resolved kinetic minima, together with the uniform separation of finite bulk mixing in (1)**. Searches so far have not found this formula in the open literature. The [prior-art audit](exchange-prior-art.md) includes adjacent quadratic-killing and adsorption literature and should be consulted before claiming novelty.

The bound (1), regular limit (1a), general-profile localization, exact oscillator coefficient, and reduced-model formulas have independent review. This supports the static result as verified within the stated mathematical model. The separate transient results in the exploration note are exact or asymptotic for the reduced well-mixed model. The static finite-bulk theorem does not by itself transfer their full time-dependent prefactors to finite bulk diffusion.
