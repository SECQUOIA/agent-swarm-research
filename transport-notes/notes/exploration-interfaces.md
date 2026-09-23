# Slow exchange points and the singular effect of surface diffusion

Research note, 2026-09-06. This is an original derivation under active verification, not a claim that publication novelty is established. The most promising candidate is the explicit crossover law linking a nearly inactive exchange point to dispersion. Ordinary reversible-adsorption Taylor dispersion and multirate trapping are established background.

## Physical question

Can surface mobility that appears negligible control dispersion in an otherwise ordinary finite channel? Yes, in this model: a smooth quadratic minimum in adsorption and desorption rates, at **constant equilibrium affinity**, makes the effect of small surface diffusion singular. The mean tracer speed and equilibrium surface coverage remain unchanged. The dispersion enhancement scales as the negative quarter power of surface diffusivity. A finite minimum rate competes with surface diffusion through a calculable gamma-function crossover.

Constant affinity matters: both rates become small together. This models a kinetic exchange barrier, not a divergent binding energy. An exact zero is an idealized limit. The finite minimum-rate crossover is the physically usable prediction.

## Exact reduced model

Consider a translationally invariant channel, with cross-sectional area A and perimeter P. The mobile phase is well mixed transversely and has longitudinal velocity U. Its internal state is one state b. The adsorbed state is indexed by arclength s on a periodic perimeter Γ and has zero longitudinal advective velocity. Its transverse surface diffusivity is D_s. Independent longitudinal Brownian diffusivities may be added afterward.

The desorption rate is k(s), with dimensions 1/time. The adsorption coefficient is K k(s), where the constant equilibrium affinity K has dimensions length. From b, adsorption into ds occurs at rate K k(s) ds/A. Desorption from s into b occurs at rate k(s). These transitions and surface diffusion obey detailed balance with

\[
 Z=A+KP,\qquad \pi_b=A/Z,\qquad \pi_s(ds)=K\,ds/Z.
\]

The generator acts as

\[
 (Lf)_b=\frac KA\int_\Gamma k(s)[f_s(s)-f_b]ds,
 \qquad (Lf)_s=D_s f_s''+k(s)(f_b-f_s).
\]

The mean velocity is V=UA/Z, independent of k and D_s. This is an exact Markov model. Its interpretation as the leading channel reduction requires transverse bulk equilibration faster than the kinetic times being studied.

Define the positive self-adjoint surface operator and its integrated resolvent

\[
 H=-D_s\partial_s^2+k(s),\qquad
 I(z)=\int_\Gamma [(z+H)^{-1}1](s)\,ds.
\]

For stationary internal initial conditions, let C(t) be the covariance of the longitudinal velocity. Its **exact** Laplace transform is

\[
 \widetilde C(z)=\frac{V^2 K I(z)}{Z-KzI(z)}. \tag{1}
\]

To derive (1), solve (z-L)φ=g with g_b=U−V and g_s=−V. If h_z=(z+H)^{-1}1, the identity (z+H)1=z+k gives

\[
 \phi_s=\phi_b-(V+z\phi_b)h_z,
 \qquad \phi_b=\frac{VK I(z)}{Z-KzI(z)}.
\]

Stationary centering gives ⟨φ⟩=0 and ⟨g,φ⟩=Vφ_b. No assumption of independently sampled adsorption sites is used once D_s is present.

When I(0) is finite, the flow-induced contribution to the long-time diffusivity is

\[
 D_{\rm flow}=\frac{V^2K}{Z}\int_\Gamma H^{-1}1\,ds. \tag{2}
\]

The convention is Var X(t)∼2D_eff t. If the longitudinal molecular diffusivities are D_b^x and D_s^x, add (A D_b^x+KP D_s^x)/Z to (2). These molecular terms do not affect the singular result.

## Quadratic minimum: explicit crossover

Suppose k has one isolated minimum s=0, positive away from that point, with

\[
 k(s)=\delta+a s^2+o(s^2),\qquad a>0,
\]

where a has dimensions 1/(time length²). Let

\[
 \ell=(D_s/a)^{1/4},\qquad
 \lambda=\sqrt{aD_s},\qquad \zeta=\delta/\lambda.
\]

As D_s→0 with fixed nonnegative ζ, rescaling s=ℓy gives H≈λ(−∂_y²+y²+ζ). Hence

\[
 I(0)\sim D_s^{-1/4}a^{-3/4}\,\mathcal C(\zeta), \tag{3}
\]

\[
 \boxed{\displaystyle
 \mathcal C(\zeta)=\frac\pi2
 \frac{\Gamma((\zeta+1)/4)}{\Gamma((\zeta+3)/4)}}. \tag{4}
\]

The dimensions of I are length×time; D_s^{-1/4}a^{-3/4} has precisely these dimensions. Formula (2) therefore has dimensions length²/time.

For (4), Mehler's kernel for H₀=−∂²+y² gives

\[
 \langle1,e^{-tH_0}1\rangle_{\mathbb R}
 =\sqrt{\frac{2\pi}{\sinh 2t}}.
\]

Integrating against e^{-ζt}, followed by r=e^{-4t}, gives (√π/2)B((ζ+1)/4,1/2), which is (4).

At an exact zero,

\[
 \mathcal C(0)=4.647476009400967\ldots,
 \qquad D_{\rm flow}\sim
 \frac{V^2K}{Z}\,4.6474760094\,D_s^{-1/4}a^{-3/4}.
\]

At ζ≫1, C(ζ)∼π/√ζ; (3) becomes π/√(aδ), the immobile-wall local integral ∫ds/(δ+as²). This extension requires δ→0 as well: for fixed positive δ the whole wall, not only its quadratic neighborhood, determines the finite limiting integral. Thus the regularization changes at **δ∼√(aD_s)**, not δ∼D_s/P².

Multiple well-separated quadratic minima contribute their local expressions additively at leading order. If their layer widths become comparable to their separation, independent-minimum asymptotics no longer apply.

## Stationary anomalous dispersion and time crossover

When D_s=δ=0, I(z)∼π/(√a√z), and zI(z)→0. Equation (1), together with the positive spectral representation of C, gives

\[
 C(t)\sim B\sqrt{\pi/a}\,t^{-1/2},\qquad
 B=V^2K/Z,
\]

\[
 \operatorname{Var}_{\rm stat}X(t)
 \sim\frac83 B\sqrt{\pi/a}\,t^{3/2}. \tag{5}
\]

The stationary distribution is finite even though the Taylor coefficient diverges. The exchange rate vanishes only on a set of zero equilibrium measure. States exactly at a zero can be absorbing when D_s=0, so the statement assumes the specified absolutely continuous stationary distribution and excludes initial atoms at such points.

For small D_s>0, time t=T/λ with fixed T>0, the bulk feedback in the denominator of (1) is smaller by order Kℓ/Z. The leading covariance is

\[
 C(t)\sim B\ell\,e^{-\zeta T}
 \sqrt{\frac{2\pi}{\sinh 2T}},\qquad T=\lambda t. \tag{6}
\]

Accordingly,

\[
 \operatorname{Var}_{\rm stat}X(t)
 \sim 2B D_s^{-3/4}a^{-5/4}
 \int_0^T (T-r)e^{-\zeta r}
 \sqrt{\frac{2\pi}{\sinh 2r}}\,dr. \tag{7}
\]

This recovers (5) at small T and 2D_flow t at large T. Formula (6) is a scaling-limit statement, not a uniform-in-time exact correlation formula; bulk-feedback corrections can shift the ultimate exponential tail at fixed nonzero D_s.

## Initialization is a material distinction

An independent reviewer derived a different leading coefficient for injection entirely into the mobile state. At D_s=δ=0,

\[
 \mathbb E_b X(t)=Vt+2V\frac KZ\sqrt{\pi/a}\,t^{1/2}+o(t^{1/2}),
\]

\[
 \operatorname{Var}_b X(t)\sim
 \frac43 B\sqrt{\pi/a}\,t^{3/2}. \tag{8}
\]

Thus the injected variance is one half the stationary variance. The physical reason is the residual residence-time bias in an equilibrium adsorbed population. The variance must be centered around the actual time-dependent mean. Equations (5) and (8) must not be interchanged in comparisons with pulse-injection experiments.

## Full transverse bulk diffusion

For a bounded smooth cross-section Ω with longitudinal velocity u(y), bulk transverse diffusivity D_b>0 and the same wall kinetics, the invariant distribution is again uniform in the bulk and K times that density on the wall. Set V=(∫Ωu dy)/Z. The unnormalized Dirichlet form is

\[
 E(f,h)=D_b\int_\Omega|\nabla f|^2
 +K D_s\int_\Gamma|h'|^2
 +K\int_\Gamma k(h-f_\Gamma)^2.
\]

The flow dispersion is Z^{-1}sup[2F−E], where

\[
 F(f,h)=\int_\Omega(u-V)f-KV\int_\Gamma h.
\]

Eliminating h gives the **exact Schur-complement identity**

\[
 D_{\rm flow}=B I(0)+\frac1Z
 \sup_{\int_\Omega f=0}\{2L_{D_s}(f)-E_{D_s}(f)\}, \tag{9}
\]

\[
 L_{D_s}(f)=\int_\Omega(u-V)f
 -KV\int_\Gamma[kH^{-1}1]f_\Gamma,
\]

\[
 E_{D_s}(f)=D_b\int_\Omega|\nabla f|^2
 +K\left(\int_\Gamma k f_\Gamma^2
 -\langle kf_\Gamma,H^{-1}kf_\Gamma\rangle\right).
\]

The last parenthesis is nonnegative. Therefore the extra contribution in (9) is nonnegative. If kH^{-1}1 is bounded uniformly as D_s,δ→0, the trace theorem and Poincaré inequality make that extra contribution O(1), proving that (3)–(4) survive arbitrary finite D_b and arbitrary bounded u.

Here is a global supersolution proof of the required uniform bound. Work in fixed dimensionless units, write k=δ+k₀, and assume k₀∈C²(Γ), with finitely many nondegenerate quadratic zeros and no other zeros. Keep δ/√D_s in a bounded interval. Choose a constant b>0 and set r=δ+b√D_s and Q=1/(r+k₀). Direct differentiation gives

\[
 HQ=\frac{\delta+k_0}{r+k_0}
 +D_s\left[\frac{k_0''}{(r+k_0)^2}
 -\frac{2(k_0')^2}{(r+k_0)^3}\right]. \tag{10}
\]

In a fixed neighborhood of each minimum, k₀″≥c₀>0 and (k₀′)²≤C₀k₀. Split that neighborhood at k₀/r=y₀, with y₀>0 sufficiently small. When k₀/r≤y₀, the numerator k₀″(r+k₀)−2(k₀′)² is at least c₀r/2. Its contribution to (10) is therefore bounded below by a positive constant times D_s/r²; this has a strictly positive lower bound because δ/√D_s is bounded and b is fixed. When k₀/r≥y₀, the first term in (10) is at least y₀/(1+y₀). The potentially negative derivative contribution is bounded in magnitude by a constant times D_s/r²≤constant/b², so choosing b large preserves a positive lower bound. Outside these fixed neighborhoods k₀ is bounded below, and the derivative correction is O(D_s).

Thus HQ≥c>0 uniformly for small D_s. Positivity of H^{-1} implies

\[
 H^{-1}1\le Q/c,\qquad
 0\le kH^{-1}1\le\frac{\delta+k_0}{c(r+k_0)}\le1/c.
\]

The trace and Poincaré bounds applied to (9) now give the full-bulk result

\[
 \boxed{D_{\rm flow}=B I(0)+O(1)}, \tag{11}
\]

uniformly for bounded δ/√D_s, with D_b fixed positive. The separate reviewer verified a shorter proof using an L² bound on kH^{-1}1, valid uniformly for all δ≥0, and also proved that the regular remainder converges to the rate-independent D_s=0 bulk energy. Those stronger reviewed statements appear in [the standalone result](result-surface-exchange.md) and [the review](review-singular-exchange.md). Neither proof claims a uniform bound if D_b simultaneously vanishes.

At D_s=0, full-bulk separation is exact without a small-diffusion estimate: the surface corrector satisfies h−fΓ=−V/k, and the bulk corrector satisfies D_b ∂ₙf=−KV. Thus the bulk corrector is independent of k and

\[
 D_{\rm flow}=\frac{D_b}{Z}\int_\Omega|\nabla f|^2
 +\frac{KV^2}{Z}\int_\Gamma\frac{ds}{k(s)}.
\]

## General vanishing orders: secondary result

For a one-dimensional wall coordinate with k(s)∼a|s|^m, m>1, local balance gives ℓ=(D_s/a)^{1/(m+2)} and λ=a^{2/(m+2)}D_s^{m/(m+2)}. Therefore I(0) scales as ℓ/λ, namely

\[
 I(0)\asymp a^{-3/(m+2)}D_s^{-(m-1)/(m+2)}.
\]

The dimensionless coefficient is ∫ℝ(−∂²+|y|^m)^{-1}1 dy and is finite for m>1. With D_s=0, C(t) scales as t^{-1/m}, so stationary variance scales as t^{2−1/m}. These exponent statements follow from the same resolvent structure but the quadratic case has the clean closed crossover and describes generic smooth nonnegative minima. For higher-dimensional internal adsorption manifolds, replace 1 by the codimension p of the zero set: the singular power becomes −(m−p)/(m+2) when m>p. A physical three-dimensional translationally invariant channel has a one-dimensional transverse wall, so p=1 is the direct channel application.

## Numerical check

A periodic finite-difference solve used k(s)=2(1−cos s)+ζ√D_s on −π≤s<π, for which a=1. With N=32768 equally spaced wall nodes, the dimensionless quantity D_s^{1/4}∫H^{-1}1 approaches the predicted C(ζ):

| ζ | D_s | Computed scaled integral | Prediction |
|---:|---:|---:|---:|
| 0 | 10⁻² | 4.6597041122 | 4.6474760094 |
| 0 | 10⁻⁴ | 4.6486252707 | 4.6474760094 |
| 0 | 10⁻⁶ | 4.6475943511 | 4.6474760094 |
| 1 | 10⁻⁴ | 2.7808625714 | 2.7841639984 |
| 1 | 10⁻⁶ | 2.7838335075 | 2.7841639984 |
| 10 | 10⁻⁶ | 0.9897994559 | 0.9910358607 |
| 10 | 10⁻⁸ | 0.9909120302 | 0.9910358607 |

This confirms the predicted law for a globally smooth periodic rate. It is not yet a mesh-refinement study or an independent time-domain test. At the smallest D_s, the finite mesh starts to affect the last digits. The parent agent subsequently added an independent full-bulk finite-volume check in `scripts/check_surface_exchange.py` and recorded results in `results/surface-exchange-checks.json`: for a periodic strip with D_b=1, height 1, K=0.7 and k=2(1−cos s), the difference D_flow−B I approached a finite value near 0.0333 as D_s decreased to 10⁻⁶. This supports the bounded remainder in (11); consult those artifacts for their discretization details.

## Literature audit and novelty boundary

Open searches on 2026-09-06 used combinations of Taylor dispersion, heterogeneous adsorption/desorption, surface diffusion, vanishing reaction rate, singular diffusivity, multirate mass transfer, and anomalous sorption. This is a targeted initial search, not a complete novelty review.

- [Levesque, Bénichou, Voituriez and Rotenberg, *Taylor Dispersion with Adsorption and Desorption*, PRE 86, 036316 (2012), open full text](https://arxiv.org/html/1211.5224) treats stationary and oscillatory flow with adsorption/desorption and develops a stochastic formulation. Its explicit canonical formulas use uniform kinetic coefficients. The general Green–Kubo approach and additive steady adsorption contribution are prior work, not discoveries here.
- [Dill and Brenner, *A general theory of Taylor dispersion phenomena: III. Surface transport*, JCIS 85, 101–117 (1982)](https://doi.org/10.1016/0021-9797(82)90239-9) already incorporates adsorption, surface diffusion and surface convection in generalized Taylor dispersion. Only its openly visible abstract was consulted, so exclusion of overlap at the detailed formula level remains incomplete.
- [Haggerty and Gorelick, *Multiple-rate mass transfer for modeling diffusion and surface reactions in media with pore-scale heterogeneity*, WRR 31, 2383–2400 (1995), author-posted text](https://www.researchgate.net/profile/Steven-Gorelick/publication/262380391_haggerty_95WR10583/links/0c96053798e5f5e28a000000/haggerty-95WR10583.pdf) establishes multirate exchange and its relation to diffusion-controlled immobile domains. The D_s=0 reduced model here is a continuous multirate model. Anomalous transport from broad residence times is therefore not a defensible broad novelty claim.
- [Alexandre, Guérin, Mangeat and Dean, *How stickiness can speed up diffusion in confined systems*, open author manuscript](https://www.mangeatm.fr/papers/alexandre_mangeat_2021_stickiness.pdf) treats diffusion changes produced by reversible adsorption and surface diffusion. Its existence rules out claiming that surface mobility can generally have a surprising sign as new.
- [*Non-Markovian Diffusion and Adsorption–Desorption Dynamics: Analytical and Numerical Results* (2024)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11048754/) has closely related subject matter. Search-accessible abstract indicates prescribed non-Markovian bulk/surface dynamics; the direct open request encountered a browser challenge. The full paper has not been inspected, and no detailed exclusion claim is made.

The candidate contribution is narrower: **spatially resolved, constant-affinity kinetic minima plus weak lateral surface diffusion produce an explicit universal gamma-function crossover, with a finite-bulk variational separation and a directly testable transition at δ∼√(aD_s)**. No matching formula was found in this initial open search. This is evidence of a promising gap, not proof of novelty.

## Independent review record

The child reviewer `verify_degenerate_adsorption` independently confirmed the Poisson formula, the exact covariance resolvent, the Mehler-kernel gamma constant, the stationary anomalous coefficient, the finite-time crossover, and the exact D_s=0 finite-bulk decomposition. It identified the initialization correction in (8). The separate reviewer `review_singular_exchange` also independently confirmed the oscillator constant and the injection correction, and identified the need to require δ→0 when extending the large-ζ asymptotic. It subsequently verified the full-bulk bounded-remainder theorem and convergence of that remainder through an L² spectral argument. Complete literature novelty remains an open check.

## Preserved negative directions

1. A general claim that adsorption adds kinetic Taylor dispersion is already established.
2. A general claim that slow trapping gives anomalous transport is already established by multirate and continuous-time-random-walk literature.
3. Small surface mobility alone is not novel; the spatial degeneracy, its regularization exponent, and the explicit crossover must carry the contribution.
4. Equilibrium retention or mean drift cannot detect this kinetic defect in the constant-affinity model. This is a prediction of the model, not a general identifiability theorem for arbitrary adsorption physics.
5. A stationary covariance calculation cannot be used unmodified for an initially mobile injected pulse: it overpredicts the leading anomalous variance by a factor of two in the quadratic case.
