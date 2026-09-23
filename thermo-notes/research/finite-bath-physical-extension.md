# Finite-bath accuracy with droplet and interfacial tails

Current complete treatment: [the LaTeX paper](../paper-finite-reservoirs/README.md). Its positive-contour proof resolves short-range sufficiency without requiring the pointwise density envelope used in this note. It proves the boundary law for all fixed gamma in mean field and spatial d>2, and sufficiently large gamma in short-range d=2. The capillarity model remains a stated model. Earlier missing-short-range statements below describe the development stage.

Date: 2026-09-06. Status: independently reviewed conditional theorems for continuous energy distributions, an exact physical-bath corollary, and a capillarity-model prediction. The assumptions are established for the separate [mean-field Potts-plus-kinetic benchmark](potts-physical-bath.md). The sufficient tail assumptions remain unproved for a short-range microscopic model. Literature novelty remains provisional; see [the closest-prior-art check](verification/ensemble-prior-art.md).

## Results

The \(N^{3/2}\) bath-capacity requirement survives when the canonical distribution has physically relevant droplet tails instead of the artificially deep valley of an exact Gaussian mixture. Under explicit local Gaussian and uniform droplet-tail bounds, there exists a constant-heat-capacity reservoir whose marginal converges in total variation to the two-phase canonical distribution **if and only if**

\[
 C_B/k_B\gg N^{3/2}.
\]

This holds for the stated tail class in dimensions \(d\ge2\). In \(d\ge3\), the boundary scale \(C_B/k_B\asymp N^{3/2}\) changes the distributions within each phase while leaving intermediate macroscopic states suppressed. In two dimensions, the same scale can instead make an interfacial state globally preferred. An isotropic square-torus capillarity model predicts an abrupt change from pure phases to an equal-volume slab at a calculable bath-capacity coefficient.

These results concern the complete equilibrium energy law. They do not assert equivalence of dynamics, predict a nucleation rate from an equilibrium barrier, or deny weaker equivalence for local observables.

## 1. Why a uniform droplet-tail assumption is needed

A canonical first-order distribution has peaks separated by \(O(N)\), each of width \(O(\sqrt N)\). That local description alone is insufficient for reservoir reweighting: the bath may amplify canonically rare intermediate states. Moreover, assuming an everywhere sub-Gaussian phase tail would exclude the droplet mechanism that matters in a short-range system.

The competition between a Gaussian excess cost \(x^2/N\) and a droplet surface cost \(x^{(d-1)/d}\) is established droplet physics. Their equality gives the mesoscopic crossover \(x\asymp N^{d/(d+1)}\). Biskup, Chayes and Kotecký develop this competition and prove results for the two-dimensional Ising lattice gas; their general-dimensional discussion is partly heuristic. [Primary paper](https://arxiv.org/abs/math-ph/0207012), [rigorous two-dimensional treatment](https://arxiv.org/abs/math/0212300).

We use that competition as an explicit **hypothesis on an energy density** below. The cited results concern specified models and observables and do not automatically establish this hypothesis for molecular energy histograms. The uniform bound is stronger than a local central limit theorem and stronger than an interfacial large-deviation statement at fixed phase fraction.

## 2. Precise canonical assumptions

Let \(p_N(E)\) be normalized continuous energy densities at a fixed reference inverse temperature \(\beta>0\). Let the two phase centers be \(E_{-,N}<E_{+,N}\), with

\[
 \Delta_N=E_{+,N}-E_{-,N},\qquad \Delta_N/N\longrightarrow\ell>0.
\]

Use fixed energy units. Let \(\phi_v\) denote a centered normal density of variance \(v\).

**Local phase limits.** For every fixed \(R<\infty\),

\[
 \sqrt N\,p_N(E_{i,N}+\sqrt N z)
 \longrightarrow w_i\phi_{v_i}(z)
 \quad\text{in }L^1([-R,R]),\qquad i\in\{-,+\},
\]

where \(w_i>0\), \(w_-+w_+=1\), and \(0<v_i<\infty\). These conditions imply that the original probability outside increasingly wide phase windows tends to zero, taking \(N\to\infty\) before \(R\to\infty\).

**Uniform interior tail bound.** For constants \(A,c>0\), independent of \(N\),

\[
 p_N(E)\le\frac{A}{\sqrt N}
 \exp\left[-c\min\left\{\frac{x^2}{N},x^\alpha\right\}\right],
 \qquad E\in[E_{-,N},E_{+,N}],
 \tag{2.1}
\]

where

\[
 x=\min\{E-E_{-,N},E_{+,N}-E\},\qquad
 \alpha=\frac{d-1}{d}\ge\frac12.
\]

This envelope permits droplet tails and an interfacial valley of cost \(O(N^\alpha)\). It does not impose an extensive Gaussian valley. Constants absorb units and model-dependent interfacial coefficients. No global Gaussian assumption is made outside the interval between the phases.

The proof below is stated for continuous densities. A lattice-energy version should be written separately with a local limit theorem and counting-measure tail bounds; it should not be inferred merely by replacing an integral symbol with a sum.

## 3. Smooth concave baths: sufficiency

Write the marginal as

\[
 q_N(E)=\frac{p_N(E)e^{h_N(E)}}{Z_N},\qquad
 Z_N=\int p_N(E)e^{h_N(E)}\,dE.
\]

The residual bath log-weight \(h_N\) includes the canonical factor already removed from the reference distribution. Assume it is concave and twice continuously differentiable on the interior of a convex feasible-energy domain, and set it to \(-\infty\) outside that domain. The domain must contain both phase centers and every fixed \(\sqrt N\)-neighborhood of them for sufficiently large \(N\).

Calibrate the linear term so that

\[
 h_N(E_{-,N})=h_N(E_{+,N})=0.
 \tag{3.1}
\]

For a prescribed concave log-weight \(g_N\), this amounts to subtracting its secant line between the phase centers. For a physical constant-heat-capacity bath, section 5 realizes the calibration by choosing the actual total energy.

Suppose that on the phase interval and every fixed-width phase neighborhood,

\[
 0\le-h_N''(E)\le K\kappa_N
 \tag{3.2}
\]

with an \(N\)-independent \(K\). Assume

\[
 \lambda_N:=\kappa_NN^{3/2}\longrightarrow0.
 \tag{3.3}
\]

**Theorem 1.** Under sections 2–3, \(Z_N\to1\) and
\(d_{\rm TV}(q_N,p_N)\to0\).

### Proof: local windows

The endpoint secant and the curvature bound imply

\[
 |h_N'(E_{i,N})|\le K\kappa_N\Delta_N.
\]

A Taylor bound then gives, uniformly for \(|z|\le R\),

\[
 |h_N(E_{i,N}+\sqrt N z)|
 \le K\kappa_N\Delta_N\sqrt N R
 +\frac K2\kappa_NNR^2\longrightarrow0.
 \tag{3.4}
\]

Hence reweighting is asymptotically constant on each fixed phase window.

### Proof: interior tails

The elementary interpolation-error bound for a concave function with bounded curvature gives

\[
 0\le h_N(E)\le\frac{K\kappa_N}{2}
 (E-E_{-,N})(E_{+,N}-E)
 \le C\kappa_NNx
 \tag{3.5}
\]

between the centers. For \(x\ge R\sqrt N\), the gain relative to the two possible canonical costs satisfies

\[
 \frac{h_N(E)}{x^2/N}\le\frac{C\lambda_N}{R},
 \qquad
 \frac{h_N(E)}{x^\alpha}\le C\lambda_NN^{1/2-\alpha}.
 \tag{3.6}
\]

Since \(\alpha\ge1/2\), both are small for large \(N\). Consequently the reweighted interior tail is bounded by

\[
 \frac{2A}{\sqrt N}\int_{R\sqrt N}^{\Delta_N/2}
 \exp\left[-\frac c2\min\left\{\frac{x^2}{N},x^\alpha\right\}\right]dx.
 \tag{3.7}
\]

Using \(e^{-a\min(u,v)}\le e^{-au}+e^{-av}\), the Gaussian term has an arbitrarily small limiting tail when \(R\to\infty\); the droplet term tends to zero already for fixed \(R>0\).

### Proof: exterior tails and normalization

Global concavity and (3.1) imply \(h_N(E)\le0\) outside the phase interval. The bath therefore cannot amplify exterior canonical tails. Their mass vanishes by the local phase limits and \(w_-+w_+=1\).

Combine this fact, (3.4) and (3.7), first at fixed \(R\), then let \(R\to\infty\). It follows that

\[
 \int p_N(E)|e^{h_N(E)}-1|\,dE\longrightarrow0.
\]

Thus \(Z_N\to1\), and division by \(Z_N\) proves the total-variation conclusion. No assumption about a Gaussian interfacial valley entered the proof.

## 4. A necessity theorem independent of valley details

For necessity, no tail envelope is needed. Retain the two positive local phase limits. Allow an arbitrary linear tilt and normalization, and suppose \(h_N\) is twice continuously differentiable and concave near and between the two phases, with

\[
 -h_N''(E)\ge k\kappa_N>0
 \quad\text{throughout }[E_{-,N},E_{+,N}].
 \tag{4.1}
\]

**Theorem 2.** If \(d_{\rm TV}(q_N,p_N)\to0\), then
\(\kappa_NN^{3/2}\to0\).

### Proof

Total-variation convergence is equivalent to

\[
 \mathbb E_{p_N}\left|e^{h_N(E)}/Z_N-1\right|\to0.
\]

In either rescaled phase window, the local normal limit is positive. Therefore

\[
 f_{i,N}(z)=h_N(E_{i,N}+\sqrt N z)-\log Z_N
 \longrightarrow0
\]

in Lebesgue measure on every fixed bounded interval. To see why the change from \(p_N\)-measure is allowed, restrict to a compact interval on which the limiting normal density has a positive minimum; local L1 convergence bounds the Lebesgue measure of exceptional sets.

Choose four points where \(f_{i,N}\) tends to zero, one in each interval \([-2,-3/2]\), \([-1,-1/2]\), \([1/2,1]\), and \([3/2,2]\). Such points exist by convergence in measure. Denote them by \(a_N,b_N,c_N,d_N\) in increasing order. Concavity bounds the central derivative by the right and left secant slopes:

\[
 \frac{f_{i,N}(d_N)-f_{i,N}(c_N)}{d_N-c_N}
 \le f_{i,N}^\prime(0)\le
 \frac{f_{i,N}(b_N)-f_{i,N}(a_N)}{b_N-a_N}.
\]

Both bounds tend to zero because their denominators stay bounded away from zero. Therefore

\[
 \sqrt N h_N'(E_{-,N})\to0,
 \qquad \sqrt N h_N'(E_{+,N})\to0.
\]

Their difference is at least

\[
 \sqrt N\int_{E_{-,N}}^{E_{+,N}}[-h_N''(E)]\,dE
 \ge k\kappa_N\Delta_N\sqrt N.
\]

As \(\Delta_N/N\to\ell>0\), the claimed necessity follows. Linear retuning cannot cancel the opposite local slopes produced by the integrated bath curvature.

## 5. An exact constant-heat-capacity reservoir

Take the reservoir density of states to be

\[
 \omega_B(U)=\text{constant}\times U^{c_B}\mathbf1_{U>0},\qquad c_B>0.
 \tag{5.1}
\]

Its dimensionless surface entropy is \(s_B(U)=c_B\log U+\text{constant}\). Thus its surface-entropy inverse temperature is \(c_B/U\), and its corresponding heat capacity is \(c_Bk_B\). Classical quadratic reservoir degrees of freedom give precisely such a power-law density; if there are \(f\) quadratic degrees of freedom, \(c_B=f/2-1\). This surface-entropy convention differs by one \(k_B\) from the canonical heat capacity of that finite quadratic reservoir. The convention is explicit and the asymptotic threshold is unchanged.

For a subsystem canonical density \(p_N(E)\propto\omega_S(E)e^{-\beta E}\), the exact isolated-composite marginal at total energy \(\mathcal E_N\) is

\[
 q_N(E)\propto p_N(E)
 e^{\beta E}(\mathcal E_N-E)^{c_B}
 \mathbf1_{E<\mathcal E_N}.
 \tag{5.2}
\]

Set

\[
 \boxed{\mathcal E_N=E_{-,N}
 +\frac{\Delta_N}{1-e^{-\beta\Delta_N/c_B}}.}
 \tag{5.3}
\]

The residual log-weight is exactly equal at the two phase centers. This is an operational choice of composite energy, not an extra artificial linear bias.

If \(c_B\gg N^{3/2}\), then uniformly over the latent-energy interval and fixed phase neighborhoods,

\[
 \mathcal E_N-E=\frac{c_B}{\beta}[1+o(1)],\qquad
 -h_N''(E)=\frac{c_B}{(\mathcal E_N-E)^2}
 =\frac{\beta^2}{c_B}[1+o(1)].
\]

Theorem 1 therefore gives sufficiency.

For necessity allow **any** total-energy sequence, not just (5.3). If its marginal converges in TV, the local-slope argument forces

\[
 \sqrt N\left[\beta-\frac{c_B}{\mathcal E_N-E_{i,N}}\right]\to0
 \quad(i=-,+).
\]

Both endpoint reservoir inverse temperatures consequently equal \(\beta+o(N^{-1/2})\). Subtracting their reciprocals gives

\[
 \frac{\Delta_N}{c_B}
 =\frac1{\beta_{B,-}}-\frac1{\beta_{B,+}}
 =o(N^{-1/2}),
\]

and hence \(c_B\gg N^{3/2}\).

**Corollary.** Under the canonical assumptions of section 2, a total-energy choice yielding TV convergence exists for the exact reservoir (5.1) iff \(c_B/N^{3/2}\to\infty\).

## 6. The boundary scale in three or more dimensions

Let \(d\ge3\), \(c_B/N^{3/2}\to\gamma\in(0,\infty)\), and use (5.3). Define

\[
 b=\frac{\beta^2\ell}{2\gamma},\qquad b_-=b,\quad b_+=-b.
\]

The residual log-weight on the two phase scales converges to

\[
 h_N(E_{i,N}+\sqrt N z)\longrightarrow b_i z.
\]

The local Gaussian fluctuations are therefore exponentially tilted. The two limiting phase contributions, in their separate \(z\) coordinates, are

\[
 q_i(z)=\frac{w_i\phi_{v_i}(z)e^{b_i z}}{Z_\gamma},\qquad
 Z_\gamma=\sum_i w_i e^{b^2v_i/2}.
 \tag{6.1}
\]

Thus phase \(i\) has limiting weight \(w_i e^{b^2v_i/2}/Z_\gamma\), rescaled mean \(b_iv_i\), and variance \(v_i\). Endpoint balancing need not preserve the integrated phase weights when their variances differ.

The proof that no intermediate probability is missed follows the tail argument above. At finite \(\lambda_N\), choose \(R\) large to control the Gaussian-cost ratio. The droplet-cost ratio now tends to zero because \(N^{1/2-\alpha}\to0\) for \(d\ge3\). Exterior tails are still not amplified. This proves both (6.1) and the full limiting distance

\[
 \lim d_{\rm TV}(q_N,p_N)
 =\frac12\sum_i\int_{\mathbb R}
 \left|w_i\phi_{v_i}(z)-q_i(z)\right|dz.
 \tag{6.2}
\]

For equal variances \(v_-=v_+=v\), the integrated phase weights remain unchanged and (6.2) reduces to

\[
 2\Phi\!\left(\frac{\beta^2\ell\sqrt v}{4\gamma}\right)-1.
\]

This extends the previously derived Gaussian-mixture crossover to the explicit droplet-tail class. It is not merely an expansion of the bath at a single mean energy.

## 7. Two dimensions: a bath can make an interface typical

At \(d=2\), the boundary scale is different because \(\alpha=1/2\). Suppose, in addition, that \(E_{i,N}/N\to e_i\) for both phases and that \(e=E/N\) satisfies a canonical large-deviation principle at speed \(\sqrt N\) on the coexistence interval, with continuous cost \(I(e)\), zero at the two phase endpoints and positive in between. Assume the compact-interval and exponential-tightness conditions needed for exponential tilting; these are an additional hypothesis.

For \(c_B\sim\gamma N^{3/2}\), the exact bath (5.1), calibrated by (5.3), has

\[
 \frac{h_N(Ne)}{\sqrt N}\longrightarrow
 J_\gamma(e):=\frac{\beta^2}{2\gamma}
 (e-e_-)(e_+-e)
\]

uniformly on the coexistence interval. More explicitly, writing \(E=E_{-,N}+\theta\Delta_N\), the endpoint-normalized exact bath satisfies

\[
 h_N(E)=\frac{\beta^2\Delta_N^2}{2c_B}\theta(1-\theta)
 +\frac{\beta^3\Delta_N^3}{6c_B^2}\theta(1-\theta)(2\theta-1)
 +O(\Delta_N^4/c_B^3),
\]

uniformly for \(0\le\theta\le1\) when \(\Delta_N/c_B\to0\). At the boundary scale the cubic term can be order one; it disappears only after division by \(\sqrt N\), and can still matter to weights at tied rate minima. Therefore the **normalized** tilted rate function is

\[
 I_\gamma(e)=I(e)-J_\gamma(e)
 -\min_u\{I(u)-J_\gamma(u)\}.
 \tag{7.1}
\]

The subtraction of the minimum is necessary. A negative unnormalized cost is evidence of a newly dominant state, not a negative rate function.

Define

\[
 \gamma_*:=\frac{\beta^2}{2}
 \sup_{e\in(e_-,e_+)}
 \frac{(e-e_-)(e_+-e)}{I(e)}.
 \tag{7.2}
\]

When this supremum is finite, \(\gamma>\gamma_*\) leaves the endpoints as the only leading-rate minima. For \(\gamma<\gamma_*\), at least one interior state has lower cost than both pure phases. Under the stated LDP, the bath law then concentrates away from the canonical endpoint phases, and TV tends to one. The boundary \(\gamma=\gamma_*\) requires subleading terms and prefactors to determine weights.

The LDP conclusion above does not, by itself, supply local peak weights or a TV formula for \(\gamma>\gamma_*\). Those would need the local and mesoscopic matching estimates as well.

## 8. A concrete capillarity prediction for an isotropic square torus

Consider the continuum capillarity approximation on a square of area \(N\) with periodic boundaries. Let \(\theta=(e-e_-)/\ell\) be the phase area fraction, ignoring subleading interface energy in that relation. Let \(\tau>0\) be the dimensionless line free energy per unit length in these units. The minimum-perimeter droplet, slab and bubble branches give the model cost

\[
 I(\theta)=\tau\min\{2\sqrt{\pi\theta},\ 2,\
 2\sqrt{\pi(1-\theta)}\},\qquad0\le\theta\le1.
 \tag{8.1}
\]

This assumes isotropy and the stated geometry. It is not the Wulff cost of a general anisotropic lattice. The familiar droplet-to-strip positions \(\theta=1/\pi\) and \(1-1/\pi\) also appear in primary Potts-model discussions; see [Kim, Keyes and Straub (2011)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3166335/).

The unnormalized bath cost becomes

\[
 F_\gamma(\theta)=I(\theta)-A\theta(1-\theta),\qquad
 A=\frac{\beta^2\ell^2}{2\gamma}.
\]

The inequality

\[
 I(\theta)\ge8\tau\theta(1-\theta)
 \tag{8.2}
\]

has equality only at \(\theta=0,1/2,1\). The slab branch satisfies it because \(\theta(1-\theta)\le1/4\). For the droplet branch, divide by \(\sqrt\theta\) and use

\[
 8\sqrt\theta(1-\theta)\le\frac{16}{3\sqrt3}
 <2\sqrt\pi,
\]

with the bubble branch obtained by reflection.

It follows that

\[
 \boxed{\gamma_* = \frac{\beta^2\ell^2}{16\tau}.}
 \tag{8.3}
\]

For \(\gamma>\gamma_*\), the two pure phases are the only leading-rate minima. For \(\gamma<\gamma_*\), the unique minimizing fraction is \(\theta=1/2\), a slab containing equal areas of the two phases. Indeed,

\[
 F_\gamma(\theta)-F_\gamma(1/2)
 \ge(A-8\tau)(\theta-1/2)^2>0
\]

away from the center when \(A>8\tau\). At equality there are three leading-rate minima; capillary translation/orientation factors and finite bath corrections determine the actual weights.

This is an explicit prediction of the capillarity-plus-reservoir model, with a discontinuous change of typical morphology at a finite coefficient of \(N^{3/2}\). It is not yet a proven microscopic transition or a cleared novelty claim.

## 9. Review, limits and next validation

Independent reviewer `review_physical_bath` checked the tail domination, the concavity necessity argument, the exact total-energy calibration, the arbitrary-total-energy constant-capacity necessity, and the two-dimensional capillarity threshold. The reviewer emphasized two restrictions now explicit above: the tilted LDP must subtract its minimum, and equality of leading-rate minima does not determine nonzero phase weights.

The substantive advance over the exact Gaussian note is the control of intermediate droplet/interfacial probability and the separation between three-dimensional local distortion and two-dimensional morphology selection. The finite-bath quadratic mechanism itself is established prior art. The 1990 Gaussian-ensemble review remains unavailable, and later finite-bath and constrained-coexistence papers need a targeted novelty check before any publication claim.

The largest remaining correctness-to-application gap is verifying (2.1), the local limits and the required LDP for an explicit microscopic example. This note proves implications of those assumptions, not the assumptions themselves. A useful next computation would compare exact density-of-states data from a first-order model under the physical power-law bath and check phase-window shifts, intermediate-state probability, and the predicted capacity scaling separately. The two-dimensional capillarity threshold offers a sharper test than fitting a single histogram distance.

Deterministic formula validation is available in `research/verification/verify-physical-bath.py`. It checks the capillarity inequality and both sides of the morphology threshold, then evaluates the exact power-law bath against its limiting interfacial tilt. At \(\beta=\ell=\tau=1\) and \(\gamma=0.1\), the uniform scaled-log-weight discrepancy falls from 0.1576 at \(N=100\) to 0.001604 at \(N=10^6\). This validates algebra and asymptotics, not a microscopic application.
