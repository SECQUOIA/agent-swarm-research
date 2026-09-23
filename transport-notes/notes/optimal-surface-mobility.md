# Optimal surface mobility and a finite-rate threshold

Research extension, 2026-09-06. This note develops a design consequence of [the verified surface-exchange crossover](result-surface-exchange.md): when lateral and axial surface diffusion have the same coefficient, some surface mobility can reduce band broadening, but a finite exchange-rate floor creates a threshold below which zero surface mobility is optimal. Convexity and the threshold have exact finite-bulk formulations. The local quadratic minimum gives a universal scaled onset law.

The convexity theorem, exact finite-bulk threshold, finite-floor constants, scaled optimizer and weak-flow zero-floor optimum have independent mathematical review in [the optimization review](review-optimal-surface-mobility.md). These results are verified within the stated model. Literature novelty remains under review throughout.

## Fixed assumptions and optimization variable

Use the same smooth channel, constant affinity K, rate kδ=δ+k₀ and fixed positive transverse bulk diffusivity D_b as in the main result. Assume isotropic surface diffusion, so a single coefficient D_s controls both transverse motion along the wall and molecular motion in the axial direction. Let u=εu₀, where ε is a dimensionless flow amplitude. Write

\[
 Z=A+KP,\quad p_s=KP/Z,\quad
 V_0=\frac1Z\int_\Omega u_0,\quad B_0=KV_0^2/Z.
\]

The mean axial drift is εV₀. At fixed ε, vary D_s while holding kδ, K, the bulk diffusivities and u₀ fixed. The objective is

\[
 D_{\rm eff}(D_s)=D_{\rm base}+p_sD_s
 +\varepsilon^2\mathscr D(D_s,\delta), \tag{1}
\]

where D_base=(A/Z)D_b^x is the fixed bulk axial Brownian term, and 𝒟 is the flow dispersion for u=u₀. Surface motion reduces the flow term but adds the explicit axial Brownian term p_sD_s. The parameter independence in this optimization is a modeling assumption: changing an experimental surface may change more than D_s.

## Exact convexity and threshold with finite bulk diffusion

The reversible transverse Dirichlet operator is affine in D_s. On the centered state space, write it as A(D_s)=A(0)+D_sS. Its quadratic inverse gives

\[
 \mathscr D(D_s,\delta)=\langle g_0,A(D_s)^{-1}g_0\rangle_\pi,
\]

where g₀ is the centered axial velocity. This function is decreasing and convex in D_s. If φ_{D_s} is its Poisson corrector and h_{D_s} its surface component, the envelope identity is

\[
 \mathscr D'(D_s,\delta)
 =-\frac KZ\int_\Gamma|h_{D_s}'|^2\,ds. \tag{2}
\]

The derivative is a right derivative at D_s=0. For δ>0 and the stated smooth fixed data, the zero-diffusion surface corrector has the required H¹ regularity. Form-resolvent differentiation or the variational principle justifies (2); an eigenfunction calculation is unnecessary.

At D_s=0, the exact full-bulk cell problem separates. Let f₀ be the mean-zero solution of

\[
 -D_b\Delta f_0=u_0-V_0,\qquad D_b\partial_nf_0=-KV_0.
\]

Then

\[
 h_0=f_0|_\Gamma-\frac{V_0}{k_\delta}.
\]

Define

\[
 M_\delta=\frac KZ\int_\Gamma
 \left|\left(f_0|_\Gamma-\frac{V_0}{k_\delta}\right)'\right|^2ds. \tag{3}
\]

If Mδ>0, the exact finite-bulk onset criterion is

\[
 \boxed{\displaystyle
 \varepsilon_c^2=\frac{p_s}{M_\delta}.} \tag{4}
\]

For ε²≤ε_c², D_s=0 minimizes (1). For ε²>ε_c², its minimum is at positive D_s. If Mδ=0, the flow corrector is annihilated by the surface-diffusion form, the flow term is independent of D_s, and zero mobility minimizes the total coefficient at every ε.

The full-bulk threshold involves the gradient of the **surface corrector**, not only the gradient of the reciprocal desorption rate. Omitting f₀Γ in (3) is generally incorrect at finite bulk diffusivity. In the well-mixed bulk model the bulk corrector is constant, so (4) becomes

\[
 \varepsilon_c^2=
 \frac{p_s}{B_0\int_\Gamma|(1/k_\delta)'|^2ds}. \tag{5}
\]

Convexity makes this a global criterion, not a local stability test. When Mδ>0, the flow term is strictly convex: its second derivative is the positive inverse-energy norm of Sφ, and it cannot vanish at an isolated D_s unless Sφ vanishes for every D_s. Its derivative approaches zero at large D_s because the flow term is nonnegative and decreasing. The total objective is coercive because p_s>0, so the positive minimizer above onset is unique.

## One quadratic minimum: universal finite-floor scaling

Now suppose V₀≠0 and k₀ has one nondegenerate zero, k₀(s₀+x)=ax²+o(x²), a>0. Let δ→0 and scale

\[
 r=\frac{aD_s}{\delta^2},\qquad
 \Lambda=\frac{\varepsilon^2B_0\sqrt a}{p_s\delta^{5/2}}.
\]

The leading variable part of (1), divided by p_sδ²/a, is

\[
 F_\Lambda(r)=r+\Lambda G(r),\qquad
 G(r)=r^{-1/4}\mathcal C(r^{-1/2}),\quad G(0)=\pi. \tag{6}
\]

Here C is the gamma-function crossover in the main result. Equivalently,

\[
 G(r)=\int_\mathbb R[-r\partial_y^2+(1+y^2)]^{-1}1\,dy.
\]

This representation makes G decreasing and convex. Formula (6) is a leading joint-limit law for the full-bulk system. Its exact bulk remainder is bounded, and ε²=O(δ^{5/2}); after division by δ², that remainder is O(δ^{1/2}) and vanishes. The same law is the direct local limit of the exact reduced-model objective.

The coefficient in the exact onset threshold has the asymptotic

\[
 M_\delta\sim B_0\sqrt a\,\delta^{-5/2}\frac\pi4. \tag{7}
\]

Indeed, ∫|(1/kδ)'|²∼√a δ^{-5/2}∫4y²/(1+y²)^4dy, and the dimensionless integral is π/4. The finite, rate-independent f₀Γ′ term and its cross term are lower order by Cauchy–Schwarz. Thus finite bulk diffusion changes the exact threshold (4), but not its leading singular coefficient.

## Onset and far-above-onset laws

At r=0, perturb the operator 1+y² by −r∂². Its first two inverse moments give

\[
 G(r)=\pi\left[1-\frac r4+\frac{21r^2}{32}+o(r^2)\right]. \tag{8}
\]

The first coefficient is −∫|[(1+y²)^{-1}]′|²=−π/4. The second is

\[
 \int_\mathbb R\frac{(6y^2-2)^2}{(1+y^2)^7}\,dy
 =\frac{21\pi}{32}.
\]

The inverse expansion can be justified by its positive spectral representation; the indicated derivative moments are finite. It is a small-r asymptotic, not an assertion of convergence of the infinite perturbation series.

Convexity and G′(0)=−π/4 imply the universal onset

\[
 \boxed{\Lambda_c=\frac4\pi.} \tag{9}
\]

For Λ≤4/π, the scaled optimum is r*=0. For Λ>4/π it is the unique positive solution of 1+ΛG′(r*)=0. Close above threshold,

\[
 r^*\sim\frac4{21}\left(\frac{\Lambda\pi}{4}-1\right). \tag{10}
\]

For Λ→∞,

\[
 r^*\sim\left(\frac{\Lambda\mathcal C(0)}4\right)^{4/5}. \tag{11}
\]

For fixed Λ away from Λc, the minimizer of the full finite-profile, finite-bulk problem approaches this scaled optimum as δ→0. Arbitrarily close to onset, the difference between the exact threshold (4) and its leading approximation (9) must be retained; the leading law alone does not specify a shrinking critical window.

## Exact zero: weak-flow fractional optimum

At δ=0, finitely many separated quadratic zeros give

\[
 \mathscr D(D_s,0)\sim A_0D_s^{-1/4},\qquad
 A_0=B_0\mathcal C(0)\sum_j a_j^{-3/4}.
\]

For ε→0, V₀≠0 and fixed p_s>0, every global optimum satisfies

\[
 \boxed{\displaystyle
 D_s^*\sim\left(\frac{A_0\varepsilon^2}{4p_s}\right)^{4/5},
 \qquad
 \min D_{\rm eff}-D_{\rm base}\sim5p_sD_s^*.} \tag{12}
\]

No differentiated asymptotic is needed. Set L=(A₀ε²/(4p_s))^{4/5} and x=D_s/L. The rescaled excess converges on compact positive x intervals to x+4x^{-1/4}, whose unique minimum is 5 at x=1. Nonnegativity of flow dispersion and a test value D_s=L bound minimizers from above by a constant times L. The divergent scalar integral excludes x→0. This localizes all global minimizers and proves (12). The independent reviewer checked this argument and its assumptions.

The finite floor becomes relevant when δ is of order √(aD_s*), equivalently when Λ is order one. Equations (9)–(12) describe how the positive optimum disappears as that floor increases.

## Analytic and numerical checks

For the dimensionless periodic profile kδ(s)=δ+2(1−cos s), −π≤s<π, the local curvature is a=1. Its reciprocal-rate-gradient integral can be evaluated exactly:

\[
 \int_{-\pi}^{\pi}|(1/k_\delta)'|^2ds
 =\frac{4\pi(\delta+2)}{[\delta(\delta+4)]^{5/2}}.
\]

One derivation starts from ∫(A−2cos s)^{-1}ds=2π/(A²−4)^{1/2}, differentiates with respect to A to obtain inverse powers, and writes 4sin²s=−(A²−4)+2Ak−k². Consequently the reduced-model threshold has the exact scaled expression

\[
 \Lambda_c(\delta)=\frac{(\delta+4)^{5/2}}{4\pi(\delta+2)}
 =\frac4\pi\left[1+\frac\delta8+O(\delta^2)\right]. \tag{13}
\]

This illustrates why the leading threshold cannot resolve arbitrarily small distances from onset at fixed δ. Direct quadrature at δ=0.001, 0.01, 0.1 and 1 matched the reciprocal-gradient formula to relative error below 5×10⁻¹⁴.

Independent high-precision evaluation of G and its derivative gave these limiting-objective minimizers. The onset parameter α means Λ=(4/π)(1+α).

| Parameter | Computed r* | Ratio to stated asymptotic |
|---|---:|---:|
| α=10⁻⁴ | 0.0000190500610 | 1.0001282 relative to (4/21)α |
| α=0.01 | 0.00192867091 | 1.0125522 relative to (4/21)α |
| Λ=10³ | 252.342549 | 0.8909734 relative to (ΛC(0)/4)^(4/5) |
| Λ=10⁶ | 70640.0257 | 0.9929448 relative to (ΛC(0)/4)^(4/5) |
| Λ=10⁹ | 17862081.1 | 0.9995541 relative to (ΛC(0)/4)^(4/5) |

These calculations used 35–45 decimal-digit arithmetic and bracketed derivative roots or a high-precision root solver. Direct integration separately recovered π/4 and 21π/32. They check the constants and limiting asymptotics; they do not replace verification of a full-bulk optimum for a particular material.

## Novelty, limits and next checks

An optimum that balances molecular spreading against kinetic or shear-induced dispersion is established transport reasoning. Classical chromatography and van Deemter-type relations are essential comparison literature; a generic statement that dispersion has an optimum is not a novelty claim. [Levesque et al. (2012)](https://arxiv.org/abs/1211.5224) also optimize adsorption/desorption parameters for dispersion in oscillatory flow. The candidate added content here is the fractional surface-mobility law for steady flow, the δ^{5/2} onset scale, the universal constant 4/π, and the exact finite-bulk surface-corrector threshold. Targeted searches for surface-diffusion optimization, heterogeneous adsorption and dispersion thresholds did not identify these particular formulas.

The assumptions deliberately hold affinity and rate profile fixed while varying D_s. A real material may not permit that independent change. Continuum surface diffusion must remain valid at the shrinking exchange length, and the channel coating is longitudinally invariant. The optimization is over dispersion at a specified flow, not over throughput, separation resolution per unit time, or cost.

The [independent review](review-optimal-surface-mobility.md) confirms the finite-floor onset coefficients, exact full-bulk threshold, scaled-minimizer argument, periodic benchmark and critical-window limitation. Its symbolic integrations and 50-digit numerical optimization were performed independently. This establishes mathematical confidence within the model, not novelty beyond the open-literature audit linked from the main result or validation of an experimental material.
