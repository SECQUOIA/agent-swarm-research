# Coordinator's independent Stage 03 checks

Date: 2026-09-07. Current stage only. The author is developing the section; none of the new sharp-limit claims is accepted until the required five independent reviews and correction cycle finish.

## Existing sharp lower certificates

Re-derived the moving-root derivative kernel rather than relying on the fixed-shape allocation. For local curvature a, normalized reference shape d, width ell=(Md/a)^(1/4), and field amplitude (Mda)^(-1/2), the squared derivative has prefactor M^(-3/2)d^(-3/2)a^(-1/2). Integration over the moving root adds ell times T. Weighting by z^(q-1), z=M^(-1/4)d^(-1/4)a^(-3/4), leaves

`M^(-1-q/4) rho d^(-1-q/4) a^(-3q/4) T`.

With rho=|sin r|/4 and d proportional to |sin r|^(-alpha_q), the spatial factor is constant. The supporting-plane prefactor q(2j)^q/(2Q) produces exactly `(qT/Q) 2^(q-3)j^q Z^(1+q/4)`, cancelling the extra constant term after the total budget is used. The derivative kernel counts both roots, whereas averaging a function of one symmetric root has the extra factor one-half. This distinction explains the normalization and was checked explicitly.

The moving-kernel change of variable has derivative `-(1+y ell')/ell`. Logarithmic coefficient derivatives are O(1/r), so compact test support produces a relative O(ell/r) error. At the critical retained radius M^b, b<1/7, the uniform ratio is at most `[M/(Z M^(7b))]^(1/4),` tending to zero even though Z grows logarithmically. Truncated arc-edge kernels are nonnegative and can only decrease the upper bound. No smoothness of the actual competitor is needed.

## Candidate supercritical local problem

Let J_mu(d) be the smooth compact-test response for derivative coefficient d and potential (x^2-mu)^2 on the real line. Put

`S_q = inf_{d>=0, integral d=1} integral_R J_mu(d)^q dmu`,

for q>8/5, and gamma=(3q-2)/7>0. A fixed bump and the entire unit budget give a positive lower bound for J_mu uniformly on |mu|<=1, hence S_q>0. A normalized graded density proportional to (1+|x|)^(-alpha), with 1<alpha<6-8/q, has integrable response tails: positive mu has exponent -(6-alpha)/8, negative mu has exponent -3/2. Compact parameters have finite response from a local mobility floor and reaction confinement. Thus S_q is finite.

Mass scaling is exact. From a unit-mass d form

`d_m(x)=m^(6/7)d(x/m^(1/7))`.

Then J_mu(d_m)=m^(-3/7)J_{mu/m^(2/7)}(d), and the moment integral is m^(-gamma) times the original value. Therefore the mass-m optimum is m^(-gamma)S_q.

For a dimensional local fold (b x^2-t)^2 with mobility mass m, ell=(m/b^2)^(1/7), the response factor is b^(-8/7)m^(-3/7) and parameter factor dt=b^(3/7)m^(2/7)dmu. Each fold with parameter density p thus contributes

`p b^((3-8q)/7)m^(-gamma)S_q`.

For the cosine family, p=1/4, b=1/2, and two equal masses m=M/2 give coefficient `2^((11q-12)/7)S_q`. At q=3 this multiplier is 8. Convexity and the pi-shift symmetry permit equal fold budgets before taking limits; equivalently strict convexity of m^(-gamma) minimizes the sum at equal division.

## Finite-measure relaxation: derivative flattening

I independently checked the proposed statement that a finite singular mobility measure does not change this smooth-test scalar response. Write nu=d dx+nu_s. For each fixed compact smooth test phi, choose a compact Lebesgue-null set K_n carrying all but o(1) of the relevant singular mass, and an open neighborhood U_n with both Lebesgue measure and integral_U_n d tending to zero. Choose smooth rho_n equal to zero near K_n and one outside U_n, between zero and one. Fix a compact smooth psi with integral one and define

`phi_n' = rho_n phi' - a_n psi`, where `a_n=integral rho_n phi'=O(|U_n|)`.

Integrate from minus infinity. The derivative has integral zero, so phi_n has support in a common compact interval and converges uniformly to phi. The absolutely continuous derivative energy converges to that of phi; the singular derivative energy tends to zero. The compact reaction and source integrals converge. Monotonicity in the measure and these reverse trials prove J_mu(nu)=J_mu(d) for every mu, including extended values. This does not assign a physical diffusion process to a measure.

The subprobability ball of finite positive measures is compact for vague convergence. For each compact smooth test, the response score is vague-continuous, so its supremum is lower semicontinuous; countable smooth tests also give joint measurability in mu. Fatou then gives lower semicontinuity of the integrated qth response. These facts are suitable for the localized circle liminf and for a direct existence proof for S_q.

If a minimizing measure limit has absolutely continuous mass m<1, singular ineffectiveness and exact scaling imply cost at least m^(-gamma)S_q>S_q. Mass m=0 has infinite response. Thus a minimizing limit must have absolutely continuous mass one: neither singular concentration nor escape of a positive mass fraction is compatible with a sharp minimum. This gives an L1 minimizer, without an explicit formula or uniqueness. It does not by itself prove that this minimizer is a closable physical coefficient; the manuscript's established positive-floor comparison handles physical values separately.

## Recovery and density of smooth trials

A near-minimizer can be combined with a small positive graded density and normalized to mass one with vanishing relative value cost. This provides the compact-domain coercivity and parameter-tail domination needed for recovery without pretending an arbitrary L1 profile has a smooth pointwise upper approximation.

On a fold half-cell, use x=2sin(s/2)/ell and w(ell x)=(1-ell^2 x^2/4)^(-1/2). The half-cell endpoints have |s|=pi/2, so 1<=w<=sqrt(2). Choosing physical D(s)=b^2 ell^6 w(ell x)d(x) makes its derivative energy canonical; reaction and source retain metric w. The total mass is m integral w^2 d on the expanding cell, tending to m by dominated convergence. Exact-budget renormalization therefore tends to one. Local weights converge to one.

The weak-limit domain needs a proof: local H1 convergence and finite weighted derivative energy alone do not invoke the Stage 01 minimal closure automatically. The author proposes the harmless narrower graded exponent 1<alpha<min(2,6-8/q). For a finite-energy limit, local Sobolev interpolation on a unit interval gives

`|v(x)|^2 <= C [|x|^(-4)+|x|^(alpha/2-2)] E[v]`

at large |x|, using quartic reaction and the graded derivative floor. Thus v is bounded. A large compact cutoff adds derivative cost bounded by `C||v||_infinity^2 R^(-2) integral_{R<|x|<2R}d`, which tends to zero; the reaction tail also vanishes. On a fixed compact, approximate the derivative in L2(d dx) by smooth functions, correct its total integral with a fixed smooth bump, and integrate. The compact lower floor controls ordinary derivative error and uniform function error. This proves membership in the smooth energy completion needed by the expanding-cell Neumann upper limit.

The graded floor supplies a global scaled-parameter majorant with positive-side power `mu^[-q(6-alpha)/8]` and negative-side power `|mu|^(-3q/2)`. Its positive exponent exceeds one precisely for the chosen alpha. Outside fixed physical fold windows, the normalized ordinary-root cost is of order `ell^[q(6-alpha)/4-2]`, tending to zero, and rootless costs are lower order. These observations support dominated convergence in the global recovery; the author's actual theorem must spell out the bounds and the order of the fixed-profile, small-background, and small-budget limits.

## Current literature check and limits

Additional targeted searches used combinations of optimal reinforcement, random potential, coalescing zeros, kinetic diffusivity and the threshold. Many broad queries were dominated by unrelated reinforcement-learning results and are weak evidence of absence. No new exact match was identified in those searches; this is not an exhaustive novelty finding. A fuller final-stage audit remains required.

I inspected Buttazzo–Oudet–Velichkov, *A free boundary problem arising in PDE optimization*, arXiv:1506.00141, introduction, Remark 2.1 and Section 4 Proposition 4.1 (printed pp.1–3 and 17). Its measure-valued reinforcement formulation already uses compact-test energies, weak-* semicontinuity and compactness to establish existence. The method must be attributed as established; the present folded-potential moment problem and sharp small-budget scaling are different claims. Open PDF: https://arxiv.org/pdf/1506.00141 .

I also verified the current arXiv record and introductory formulation of Alphonse–Kunštek–Vrdoljak, *Optimal design with uncertainties: a risk-averse approach*, arXiv:2602.19869v1, submitted 23 February 2026. It treats mixtures of two conducting materials and uncertain loading with generalized risk measures. The fact of risk-aware PDE design is not new. Open text: https://arxiv.org/html/2602.19869v1 . Buttazzo–Maestre, arXiv:1002.2770, likewise optimizes bounded conductivity under random loading. These boundaries will need precise final bibliography and positioning.

## Frozen-source check

Read the full authored Section03 after the final liminf-subsequence and subcritical-integral clarifications. The snapshot is 13abd3fbd62d1a6faf46617e4f678ed14ac22bacb42b8ff161f0ee27d67f0b00. Independently checked the signs and factors in the common-budget lower scaling and half-budget recovery scaling, the singular derivative flattening, strict mass-loss inequality, and rough-density completion argument. No substantive defect was found in this pass. Source whitespace scan is clean; snapshot hashes are unchanged. Visually inspected compiled page 22 (the measure and natural-endpoint arguments): readable equations, no overflow or clipping. This is a sampled layout check; final full-manuscript visual inspection remains required.
