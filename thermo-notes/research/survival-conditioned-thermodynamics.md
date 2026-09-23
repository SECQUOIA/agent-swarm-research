# Survival conditioning and thermodynamic integration

Date: 2026-09-06; extended 2026-09-07. Status: candidate sampling-protocol result, with [independent mathematical and protocol review](verification/survival-thermodynamics-review.md). The eigenvalue and conditioned-process ingredients are established. The most specific candidate is the second-order bound on the path dependence of endpoint-conditioned force integration. A [focused prior-art audit](verification/survival-prior-art.md) found no exact duplicate in the sources examined; novelty remains unconfirmed.

## Why the sampling protocol matters

A simulation may estimate metastable properties by discarding trajectories that escape a basin. Sampling the surviving trajectories at their final time gives a different distribution from sampling well inside trajectories that survive for a much longer time. Even for a reversible underlying network, the two prescriptions need not give the same integrability of mean forces.

The calculation below distinguishes three measures: the canonical distribution with reflecting basin boundaries, the endpoint quasi-stationary distribution, and the stationary distribution of the process conditioned never to escape. It proves an exact force potential for the last measure under a specified energy-control protocol, gives a counterexample for endpoint conditioning, and bounds the latter's path dependence in a weak-killing regime.

An integral of separately measured endpoint-conditioned forces is **not** automatically the mean mechanical work of a single driven trajectory conditioned to survive the entire protocol. In a slow, globally surviving trajectory, the temporal bulk is instead biased by both past and future survival. The distinction is essential to the physical interpretation; no equilibrium work-extraction claim is made.

## Reversible killed network and allowed controls

Let the finite transient-state network be connected, with positive weights w_i=exp(-βE_i), W=diag(w), and a symmetric reflecting conductance Laplacian A_0. Add nonnegative killing conductances d_i, at least one positive, and write

\[
 A=A_0+\operatorname{diag}(d_i).
\]

The backward killed generator is -W^(-1)A. Transition rates are c_ij/w_i, and killing rates are r_i=d_i/w_i. Its principal generalized eigenpair satisfies

\[
 Ah=\lambda Wh,\qquad \lambda>0,\quad h_i>0.\tag{1}
\]

During the control variations, β and **all conductances A are held fixed**; only well energies E_i vary. This is a fixed transition-state-conductance Arrhenius model. It preserves detailed balance between transient states. Holding transition rates or attempt frequencies fixed is a different model, and a general change of molecular energy can also change the conductances.

Define Z=Σ_i w_i and

\[
 \pi_i=\frac{w_i}{Z},\qquad
 \nu_i=\frac{w_ih_i}{\sum_jw_jh_j},\qquad
 \eta_i=\frac{w_ih_i^2}{\sum_jw_jh_j^2}.\tag{2}
\]

Here π is the reflecting canonical law. The endpoint law ν is the long-time distribution conditional on no escape before observation. The law η is the stationary distribution of the Doob-transformed process conditioned never to escape; it is also the limit in the interior of a long surviving trajectory. These are standard quasi-stationary and conditioned-process facts.

## An exact potential for interior-survivor mean forces

Differentiating (1), using symmetry and holding A fixed, gives

\[
 \partial_{E_i}\lambda
 =-\lambda\frac{h^T(\partial_{E_i}W)h}{h^TWh}
 =\beta\lambda\eta_i.
\]

Consequently

\[
 \boxed{\quad \sum_i\eta_i\,dE_i
 =d\left[\beta^{-1}\log(\lambda/\lambda_{\rm ref})\right].\quad}\tag{3}
\]

The fixed positive reference rate λ_ref makes the logarithm dimensionless and does not affect its derivative. By comparison Σ_iπ_i dE_i=dF_can, with F_can=-β^(-1)log Z. The potential in (3) is a spectral escape-rate potential for this control family, not automatically an ordinary Helmholtz free energy with all of its thermodynamic interpretations.

Equation (3) is a Hellmann–Feynman response identity. The principal eigenvalue, its derivative, and the Doob process are established machinery. The question is what they imply for force integration under the two survival sampling protocols.

## Endpoint-conditioned forces need not be integrable

At β=1 take

\[
 A=\begin{pmatrix}
 111/55&-1&0\\
 -1&2&-1\\
 0&-1&1
 \end{pmatrix}.
\]

This is a three-state chain with unit internal conductances and a killing conductance 56/55 at state 1. At E=(0,0,0),

\[
 \lambda=1/5,\qquad h=(11/25,4/5,1),
 \qquad\nu=(11,20,25)/56,
 \qquad\eta=(121,400,625)/1146.
\]

Differentiating the generalized eigenproblem yields the nonzero curl

\[
 \boxed{\quad
 \partial_{E_2}\nu_1-\partial_{E_1}\nu_2
 =-\frac{275}{64176}.\quad}\tag{4}
\]

Thus there is no local scalar potential whose well-energy derivatives are all the endpoint occupations. Integrating forces from separately equilibrated survivor endpoints can give different values along different paths between the same energies.

At least three transient states are required for this effect with unrestricted well-energy controls and fixed A. For two states, a common shift of both energies leaves ν unchanged; ν_1 depends only on E_1-E_2 and ν_2=1-ν_1. These facts force the two-dimensional curl to vanish. This observation concerns this control family, not all two-state nonequilibrium models.

## Second-order protection near the reflecting equilibrium

The lack of an exact endpoint potential does not imply a first-order error in weakly escaping systems. Normalize h so E_πh=1 and let v=Var_π(h). Then

\[
 \nu_i=\pi_ih_i,\qquad
 \eta_i=\frac{\pi_ih_i^2}{1+v}.
\]

The endpoint law is exactly the normalized geometric mean of the two laws with integrable forces:

\[
 B=\sum_i\sqrt{\pi_i\eta_i}=\frac1{\sqrt{1+v}},\qquad
 \nu_i=\frac{\sqrt{\pi_i\eta_i}}{B}.\tag{5}
\]

Set m=(π+η)/2. Pointwise,

\[
 m_i-B\nu_i=\tfrac12(\sqrt{\pi_i}-\sqrt{\eta_i})^2\ge0.
\]

The right side sums to 1-B, so m=Bν+(1-B)ρ for a probability law ρ when B<1. It follows that

\[
 \boxed{\quad
 \|\nu-m\|_{\rm TV}\le1-B
 =1-(1+v)^{-1/2}\le v/2.\quad}\tag{6}
\]

Both terms of m have exact force potentials. Therefore for any piecewise smooth closed energy path Γ along which A is fixed,

\[
 \boxed{\quad
 \left|\oint_\Gamma\sum_i\nu_i\,dE_i\right|
 \le\int_0^1[1-B(E(s))]\,
 \left[\max_i E_i'(s)-\min_i E_i'(s)\right]ds.
 \quad}\tag{7}
\]

To prove (7), subtract m from ν inside the closed integral and use the probability inequality |(ν-m)·f|≤TV(ν,m) osc(f). The oscillation removes common energy shifts automatically.

The corresponding approximate endpoint potential is

\[
 F_{\rm mid}=\tfrac12\left[F_{\rm can}
 +\beta^{-1}\log(\lambda/\lambda_{\rm ref})\right].\tag{8}
\]

For an open path, the difference between its endpoint-force integral and ΔF_mid obeys the same right side as (7). Equations (6)–(8) bound force integrals without differentiating an eigenvector with respect to controls. A bound on local curl would additionally require control of those derivatives.

## A computable spectral-gap criterion

Let L_0=W^(-1)A_0 be the positive reflecting generator, g>0 its spectral gap in L²(π), and r_i=d_i/w_i its killing-rate function. Let r_min=min_i r_i and σ_r²=Var_π(r). If

\[
 g+r_{\min}-\lambda>0,
\]

then

\[
 \boxed{\quad
 v\le\frac{\sigma_r^2}{(g+r_{\min}-\lambda)^2}.\quad}\tag{9}
\]

Write h=1+δ, E_πδ=0. From (L_0+r)h=λh, take the inner product with δ:

\[
 \langle\delta,L_0\delta\rangle_\pi
 +\langle(r-\lambda)\delta^2\rangle_\pi
 =-\langle\delta,r-\mathbb E_\pi r\rangle_\pi.
\]

Poincaré's inequality and Cauchy–Schwarz give (g+r_min-λ)v≤σ_r√v, proving (9). The Rayleigh trial h=1 gives λ≤E_πr, so replacing λ by E_πr produces a weaker bound using only reflecting equilibrium data whenever its denominator is positive.

For killing conductances εd_i on a fixed compact energy-control region, with reflecting gap uniformly bounded below, σ_r=O(ε) and λ=O(ε). Hence v=O(ε²), and the path-dependence bound (7) is O(ε²) for a fixed path. Endpoint occupations themselves generally differ from π by O(ε). Their first-order discrepancy is nevertheless integrable, because ν=(π+η)/2+O(ε²). Uniform killing rates give h constant and exact agreement of all three laws.

This is a conditional finite-network statement. A vanishing reflecting gap, a moving basin, changing transition-state conductances, or a singular low-temperature limit can destroy the uniform estimate. Those are material questions for a molecular application.

## Exact response of the interior-survivor law

There is also a useful fluctuation-response identity for the same fixed-conductance controls. Let E(t)=E+tf for a fixed state function f, and let C_f^Q(s) denote its centered stationary autocovariance in the Doob process with invariant law η. Then

\[
 \boxed{\quad
 \frac{d^2}{dt^2}\left[\beta^{-1}\log\lambda(E+tf)\right]_{t=0}
 =-\beta\operatorname{Var}_\eta(f)
 -2\beta\lambda\int_0^\infty C_f^Q(s)\,ds.
 \quad}\tag{10}
\]

For a direct proof, put G=W^(-1/2)AW^(-1/2), with orthonormal eigenvectors u_j and eigenvalues λ=λ_0<λ_1≤..., and write f_j0=u_j^T diag(f)u_0. Under the control, G(t)=exp(βt diag(f)/2)G exp(βt diag(f)/2). Symmetric eigenvalue perturbation gives

\[
 (\log\lambda)''=-\beta^2\sum_{j>0}
 \frac{\lambda_j+\lambda}{\lambda_j-\lambda}|f_{j0}|^2.
\]

The Doob generator has decay rates λ_j-λ and eigenfunctions u_j/u_0 in L²(η). Thus Var_η(f)=Σ_(j>0)|f_j0|² and the covariance integral is Σ_(j>0)|f_j0|²/(λ_j-λ), proving (10).

If g_Q=λ_1-λ, reversibility gives

\[
 -\beta(1+2\lambda/g_Q)\operatorname{Var}_\eta(f)
 \le F_{\rm surv}''\le-\beta\operatorname{Var}_\eta(f).
\tag{11}
\]

The spectral potential is concave, and this force response has a larger magnitude than the variance term alone. The added term is controlled by the escape rate relative to relaxation within the conditioned process. This is not a general equilibrium susceptibility formula for a physical potential with changing barriers; absorbing-state fluctuation-response theory is close prior art requiring explicit comparison.

## Scope, related work, and verification

General response theory for absorbing processes already exists; for example Padmanabha, Azaele, and Maritan, *Generalization of Fluctuation-Dissipation Theorem to Systems with Absorbing States*, New Journal of Physics **25**, 113001 (2023), [open manuscript, originally posted in 2022](https://arxiv.org/abs/2204.02543). Quasi-stationary laws, Doob transforms, and principal-eigenvalue occupation derivatives are not proposed as new. The [audit](verification/survival-prior-art.md) also records established endpoint/interior distinctions, nonequilibrium force curls, and escape-rate corrections to equilibrium identities. Equation (10) is best treated as a specialized spectral response corollary, not a new general fluctuation-dissipation theorem.

The current candidate is the joint statement that endpoint force integration can fail to be path independent while interior-survivor forces have a spectral potential, together with the geometric-mean bound showing second-order protection near equilibrium. A dedicated prior-art audit must determine whether this combination is already known.

For a physical interpretation, one must specify the observation protocol and which microscopic quantities remain fixed as the control changes. Equations (4) and (7) concern force data assembled from separate endpoint-conditioned ensembles. They do not prove nonzero quasistatic cyclic work for a single trajectory conditioned on surviving the whole cycle. Additional energetic costs of reinjection, replication, or feedback must be included if such a mechanism is used to maintain a population. The present note makes no claim to calculate those costs.

For general varying conductances the exact differential instead reads

\[
 dF_{\rm surv}=\sum_i\eta_i\,dE_i
 +\frac{h^T(dA)h}{\beta\lambda h^TWh}.
\]

Dropping its second term would incorrectly extend the integrability statement beyond the authorized control family.

### The quadratic cancellation can fail for another reversible control family

This limitation is quantitative. In the same three-state chain, choose energy-dependent conductances

\[
 c_{12}(E)=e^{-(E_1+E_2)/2},\quad
 c_{23}(E)=e^{-(E_2+E_3)/2},\quad
 d_1(E)=\epsilon\frac{56}{55}e^{-E_1/2},\quad d_2=d_3=0
\]

at β=1. Internal transitions still obey detailed balance. At E=0 the entire killed generator and its conditioned measures agree with the fixed-conductance example at the same ε. Their responses to changes in well energy differ. Independent weak-killing perturbation gives

\[
 \partial_{E_2}\nu_1-\partial_{E_1}\nu_2
 =-\frac{56}{495}\epsilon+O(\epsilon^2).
\tag{12}
\]

Thus detailed balance and a separation between mixing and escape times do not alone imply the second-order cancellation. How the controls change transition barriers matters even when all rates and stationary observations agree at the reference point. Equation (12) is derived in the independent review. It concerns two control derivatives at a fixed absorbing reference, so no common-energy-shift invariance is assumed for this alternative family.

### Numerical checks

The reproducible [network checker](verification/check_survival_thermodynamics.py) tests 150 random networks. It verifies the potential derivative, endpoint response, Hellinger and gap bounds, and the covariance form of (10); endpoint derivatives agree with centered numerical differences to maximum absolute error 9.05×10^(-11). In the three-state example, a square of side 0.5 in (E_1,E_2), with E_3=0, gives endpoint-force integral 0.00100070. Both canonical and interior-survivor integrals vanish to numerical precision. Scaling the killing conductance by ε gives integrals proportional to ε²: the integral divided by ε² is 0.003576 at ε=0.01 and 0.003602 at ε=0.003. The general bound (7) holds but is conservative in this example. See [results](verification/survival-thermodynamics-results.json).

An [independent driven calculation](verification/check_survival_protocol.py) solves forward and backward survival equations around a smooth loop. The endpoint-assembled force integral stays nonzero; the mechanical work conditional on survival through the whole cycle decreases toward zero as the cycle duration grows. This checks the protocol distinction rather than suggesting an extraction mechanism. All numerical results are floating-point checks, not rigorous numerical enclosures; the algebraic statements have separate proofs.
