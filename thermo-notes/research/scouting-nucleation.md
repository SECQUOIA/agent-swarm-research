# Nucleation scouting: finite perturbations and reactive susceptibility

Date: 2026-09-06. Status: candidate results derived below; novelty remains provisional. This note does **not** claim a publishable discovery. Independent mathematical review is complete; see [the report](verification/nucleation-independent-review.md). No literature packages were altered.

## Research choice and intended contribution

A concrete direction is to bound the change of a reversible nucleation rate when a thermodynamic field or interaction potential changes, using the committor at just one reference state. The useful possible contribution is a finite perturbation interval, a sharp two-sided curvature bound, and a clear distinction between series bottlenecks and parallel mechanisms. The first derivative itself is established prior work, and the variational machinery is classical.

The application fits Corti's interests in nucleation, constrained metastability, finite systems, and the interpretation of measured nucleation slopes. Its potential impact would depend on turning the bounds into a usable uncertainty/extrapolation method; an elementary inequality without a persuasive application is unlikely to be a major advance.

## Setting and precise observable

Let A and B be fixed disjoint sets in a fixed state space. In the intervening domain Ω, consider a reversible diffusion with generator

\[
 L_\lambda f=w_\lambda^{-1}\nabla\cdot(w_\lambda D\nabla f),
 \qquad w_\lambda(x)=w_0(x)e^{\lambda Q(x)}.
\]

Here w is an **unnormalized** equilibrium density, D is a fixed symmetric positive definite diffusion tensor, λQ is dimensionless, and Q is a fixed observable. Assume sufficient regularity, integrability, and ellipticity for the Dirichlet and Thomson principles and differentiation. Outer boundaries are reflecting. The committor qλ is zero on A and one on B. Set

\[
 C_\lambda=\min_{f|_A=0,f|_B=1}\int_\Omega
 w_\lambda\nabla f\cdot D\nabla f\,dx,
 \quad
 \nu_\lambda(dx)=\frac{w_\lambda\nabla q_\lambda\cdot D\nabla q_\lambda}{C_\lambda}\,dx.
\]

ν is a probability measure weighted by local Dirichlet dissipation. It is **not** the usual transition-path occupation measure proportional to ρq(1−q).

If Zλ is the total partition integral, the equilibrium frequency of A→B reactive events is Cλ/Zλ. Define separately the capacity rate

\[
 k_\lambda^{\rm cap}=C_\lambda/Z_{A,\lambda},\qquad
 Z_{A,\lambda}=\int_Aw_\lambda dx.
\]

This equals reactive-event frequency divided by the fraction of time physically spent in A. It is not identically the inverse mean first-passage time for arbitrary initial ensembles. It is also not the conventional TPT rate normalized by the *last-visited-A* population, whose unnormalized mass is ∫wλ(1−qλ) and has an extra committor response. In a well-separated metastable regime these distinctions can become small; that approximation must be tested for a physical application.

## Candidate 1: finite perturbation sandwich

For any λ such that the two moments exist,

\[
 \boxed{\frac{1}{\mathbb E_{\nu_0}e^{-\lambda Q}}
 \leq\frac{C_\lambda}{C_0}
 \leq\mathbb E_{\nu_0}e^{\lambda Q}.}\tag{1}
\]

**Proof of the upper bound.** Insert the old committor q0 into the new Dirichlet variational problem. Its energy is C0 Eν0 exp(λQ).

**Proof of the lower bound.** The old unit current is j0=w0D∇q0/C0 (orientation is immaterial). It remains divergence free and carries unit current between the fixed boundaries. The new Thomson resistance evaluated on j0 is

\[
 \int j_0\cdot(w_\lambda D)^{-1}j_0\,dx
 =C_0^{-1}\mathbb E_{\nu_0}e^{-\lambda Q}.
\]

The minimum resistance is 1/Cλ, which proves the bound.

Writing Mν(λ)=Eν0 exp(λQ) and MA(λ)=EA,0 exp(λQ), the capacity-rate version is

\[
 \boxed{\frac{1}{M_\nu(-\lambda)M_A(\lambda)}
 \leq \frac{k_\lambda^{\rm cap}}{k_0^{\rm cap}}
 \leq\frac{M_\nu(\lambda)}{M_A(\lambda)}.}\tag{2}
\]

For the equilibrium event frequency, replace MA by the full equilibrium moment. Both variants remove the otherwise unphysical dependence on adding a constant to Q. The logarithmic width of either interval is

\[
 \log M_\nu(\lambda)+\log M_\nu(-\lambda).
\]

For nonzero λ it vanishes exactly when Q is constant ν0-almost everywhere, and is λ²Varν0(Q)+O(λ⁴) when the necessary cumulants exist. Thus fluctuations of the perturbing observable specifically in the reference dissipation measure control the width; equilibrium fluctuations over the entire basin are a different quantity.

For Q∈[a,b], Hoeffding's lemma gives

\[
 \left|\log(C_\lambda/C_0)-\lambda\mathbb E_{\nu_0}Q\right|
 \leq\lambda^2(b-a)^2/8.
\]

This is a finite-range corollary, not a claim that a local variance alone controls finite perturbations.

## Candidate 2: sharp reactive susceptibility bound

Tangency of the upper and lower bounds at zero gives the known first-order sensitivity

\[
 \partial_\lambda\log C_\lambda=\mathbb E_{\nu_\lambda}Q.
\]

Their second derivatives give

\[
 \boxed{-\operatorname{Var}_{\nu_\lambda}(Q)
 \leq\partial_\lambda^2\log C_\lambda
 \leq\operatorname{Var}_{\nu_\lambda}(Q).}\tag{3}
\]

With several fields wθ=w0 exp(θ·Q), the same directional argument yields the Loewner-order bound

\[
 -\operatorname{Cov}_{\nu_\theta}(Q)
 \preceq\nabla_\theta^2\log C_\theta
 \preceq\operatorname{Cov}_{\nu_\theta}(Q).
\]

Consequently

\[
 -\operatorname{Cov}_{\nu_\theta}(Q)-\operatorname{Cov}_{A,\theta}(Q)
 \preceq\nabla_\theta^2\log k_\theta^{\rm cap}
 \preceq\operatorname{Cov}_{\nu_\theta}(Q)-\operatorname{Cov}_{A,\theta}(Q).
\]

Unlike equilibrium log partition functions, log capacities need not be convex. Inferring a positive structural variance directly from the curvature of log nucleation rate is therefore invalid in this general setting.

### Exact decomposition of the curvature

Let h=∂λqλ at a fixed λ and use the energy inner product E(u,v)=∫wλ∇u·D∇v. Then h vanishes on A and B and solves

\[
 E(h,v)=-\int w_\lambda Q\nabla q_\lambda\cdot D\nabla v\,dx
 \quad\text{for every zero-boundary }v.
\]

Differentiating the minimum energy twice gives

\[
 \partial_\lambda^2\log C_\lambda
 =\operatorname{Var}_{\nu_\lambda}(Q)-2E(h,h)/C_\lambda.\tag{4}
\]

The response correction is nonnegative. Since E(q,v)=0, Q may be centered in the forcing. Cauchy–Schwarz then gives

\[
 E(h,h)\leq C_\lambda\operatorname{Var}_{\nu_\lambda}(Q),
\]

which proves both sides of (3) independently of differentiating (1). For multiple fields the response correction is the Gram matrix 2E(hi,hj)/C.

### Sharp examples

The same proof works for a finite network with positive undirected conductances c_e(λ)=c_e(0)e^{λQ_e}, energy Σe c_e(Δeq)², and dissipation probabilities νe=c_e(Δeq)²/C. An edge is counted once.

- **Parallel channels:** All edges connect A directly to B. Then Cλ/C0=Σνe exp(λQe), so the upper finite bound is exact and curvature is +Varν(Q). Different channels can be favored by different fields even though each has a fixed exponent.
- **Series bottlenecks:** A chain connects A to B. Then Cλ/C0=[Σνe exp(−λQe)]⁻¹, so the lower finite bound is exact and curvature is −Varν(Q). The dissipation probabilities are normalized resistances.

Therefore neither coefficient in (3) can be improved for general reversible networks. Equal dissipation statistics at one reference state do not fix finite-field rate changes: series and parallel networks can share those statistics and realize the two opposite extremes. Continuum thin-channel limits provide analogous examples, though exact attainment in a connected smooth multidimensional domain requires separate conditions.

## What the thermodynamic interpretation requires

For Fλ=F0−λQ/β with fixed D, this is an exact potential perturbation theorem. Setting λ=βΔμ and Q equal to particle excess requires a state space and dynamics in which that field really couples linearly to the free energy and D remains unchanged. It is not automatic for cluster-size projections.

In particular, a particle-conserving simulation has constant total N: adding −μN changes no dynamics. A meaningful grand-canonical chemical-potential response requires an open system, nonconserved density dynamics, or a carefully derived effective landscape and kinetic model. In a jump process detailed balance fixes conductance symmetry, but it does not fix its chemical-potential dependence; Q_e is an **edge conductance score**, which need not equal the particle number at either endpoint.

The common nucleation identification of slope with a critical size is recovered only when ν concentrates around a single saddle, its relevant Q is the desired excess, and basin subtraction and mobility terms are treated. The exact dissipation-weighted mean generally covers multiple saddles and bottlenecks.

## Field-dependent mobility and limitations

If Dλ=e^{aλ}D0 globally, then log Cλ gains aλ. The naive thermodynamic slope is off by a even though equilibrium measures are identical; an arbitrary time rescaling cannot be learned from equilibrium fluctuations. With Dλ=e^{bλ²/2}D0, curvature gains b, which can violate (3) by any amount. These are simple counterexamples to a mobility-free universal rate theorem.

A safe extension for general tensor Kλ=wλDλ is the direct trial pair

\[
 C_\lambda\leq\int\nabla q_0\cdot K_\lambda\nabla q_0,
 \qquad
 C_\lambda\geq\left[\int j_0\cdot K_\lambda^{-1}j_0\right]^{-1}.
\]

For scalar Dλ=dλ(x)D0, equation (1) holds with exp(λQ) replaced by rλ=(wλ/w0)dλ; a linear field identity requires log rλ to be linear. Arbitrary tensor perturbations need this matrix form.

Other limitations: boundaries must remain fixed; underdamped and irreversible dynamics do not obey this symmetric Dirichlet/Thomson construction; exact inequalities require exact fields or separately certified trial functions and flows; finite-sample moment estimates can miss rare tails and are not automatically rigorous confidence bounds.

## Prior art audit and negative findings

1. **The first derivative is not new.** Gu, Lin, and Zhou, *Sensitivity Analysis and Optimization of Reaction Rate*, Communications in Mathematical Sciences 15 (2017), 1507–1525, derive potential sensitivities of reactive flux and TPT rate (Theorem 3.1, printed pp.1511–1512). Their equation (3.7) is the normalized version of the first derivative above. They explicitly distinguish event frequency from the rate normalized by ∫ρ(1−q), a distinction preserved here. Open primary PDF: <https://personal.cityu.edu.hk/xizhou/cmsv-207-xiangzhou.pdf>. Downloaded and inspected full-text definitions, theorem, proof, and discussion; not ingested into literature.
2. **An exact kinetic nucleation theorem is not new.** Ford, *Nucleation theorems, the statistical mechanics of molecular clusters, and a revision of classical nucleation theory*, Phys. Rev. E 56 (1997), 5615–5629, derives a size average from the exact Becker–Döring rate (equations 30–31, printed p.5621). Open author PDF: <https://www.homepages.ucl.ac.uk/~ucapijf/pubs/papers/PRE05615.pdf>. The exact slope-average idea therefore cannot be claimed as a new nucleation theorem merely by replacing a sharp critical size with an average. Search-result full-text excerpt inspected; full article still needs detailed audit.
3. **The principles behind (1) are classical.** Den Hollander and Jansen, *Berman–Konsowa principle for reversible Markov jump processes* (2013 preprint; published 2016), place Dirichlet/Thomson and stronger path-flow principles in this setting. Open primary source: <https://arxiv.org/abs/1309.1305>, published record <https://math-mprf.org/journal/articles/id1429/>. The harmonic/arithmetic structure also resembles classical Wiener/Voigt–Reuss bounds for conductivity. This is a serious novelty risk: reference-field comparison inequalities may already contain (1) verbatim in another notation.
4. **Rate reweighting and force-field uncertainty are active work.** Moracchini et al., *Girsanov Reweighting for Uncertainty Propagation in Rare-Event Kinetics* (July 2026), <https://arxiv.org/abs/2607.13757>, uses path reweighting for committor uncertainty and rate bounds under basin assumptions. Only abstract inspected. Distinction to investigate: present bounds use static dissipation weights and two variational principles, not trajectory likelihood ratios.
5. **Finite reservoir equilibrium/critical-cluster correspondence has fresh prior art.** *Computing Nucleation Rates from Confined Equilibria: The Critical Cluster Equivalence Principle*, JACS, DOI <https://doi.org/10.1021/jacs.6c09002>, was returned by the search as very recent. Its accessible text derives reservoir-depletion curvature changes and the stability reversal between confined and open critical clusters. This weakens an alternative proposal based only on finite-reservoir Hessian corrections, which is therefore not pursued here. Verify bibliographic timing against the publisher before citation in a manuscript.

Searches on 2026-09-06 included “committor rate sensitivity,” “capacity nucleation theorem,” “nucleation theorem kinetic exact,” “effective conductance second derivative,” “conductance moment generating perturbation,” and reaction-rate/Thomson perturbation combinations. No exact match to the covariance sandwich or its paired finite-field nucleation application was found in these searches. Absence from these searches is not evidence of absence from the literature.

## Next research gates

1. Independently audit equations (1)–(4), normalization, and sharp examples, including a random-network numerical check.
2. Read Ford 1997 and search conductivity/effective-resistance sensitivity literature before assigning novelty.
3. Test a two-channel nucleation network with physical state energies and explicit detailed-balance rates; distinguish state thermodynamic scores from edge kinetic scores.
4. Explore whether a stronger Berman–Konsowa path bound makes finite perturbation prediction practical where the moment sandwich is broad.
5. Connect to certified approximate committor/current methods; merely substituting an approximate committor in ν loses the lower guarantee.


## Numerical verification

`research/code/check_reactive_susceptibility.py` (NumPy, seed 772951) solves 100 random finite networks directly. It checks 1,200 finite perturbations against both moment bounds, compares the first and second derivatives to centered finite differences, and verifies the exact series/parallel examples. On 2026-09-06, the largest bound violation was 1.33×10⁻¹⁵ (roundoff), maximum slope error 2.44×10⁻⁸, and maximum curvature error 6.05×10⁻⁸. Curvature/variance ranged from −1 to 0.99294. This supports the algebra; it is not physical validation or a substitute for the variational proof.

## Further extension: resolve the perturbation along the reference committor

This subsection was added after the initial equations were sent for independent review. It is a derived extension requiring a separate review. It uses the same classical variational tools.

In the diffusion setting, the pushforward of ν0 under q0 is uniform on [0,1]. Indeed, flux conservation gives ∫δ(q0−u)w0∇q0·D∇q0 dx=C0 for almost every u. Define mλ(u)=Eν0[exp(λQ)|q0=u]. Minimizing the new Dirichlet energy over all trial functions g(q0), rather than only q0, gives

\[
 \frac{C_\lambda}{C_0}\leq
 \left[\int_0^1\frac{du}{m_\lambda(u)}\right]^{-1}
 \leq \mathbb E_{\nu_0}e^{\lambda Q}.\tag{5}
\]

The minimizing derivative is g′(u) proportional to 1/mλ(u). This is simply an optimized reaction-coordinate upper bound specialized to finite potential changes, not a new variational principle.

When Q=Q(q0), the result is exact:

\[
 \frac{C_\lambda}{C_0}=\left[\int_0^1e^{-\lambda Q(u)}du\right]^{-1},
 \qquad
 q_\lambda(x)=\frac{\int_0^{q_0(x)}e^{-\lambda Q(u)}du}
 {\int_0^1e^{-\lambda Q(u)}du}.
\]

Substitution into the PDE verifies this directly. Such a perturbation changes the committor values but preserves its level sets and current lines. The physical relevance depends on whether an available field approximates a function of q0.

For finite networks a stronger lower bound follows from the classical Berman–Konsowa principle. Orient each edge from smaller to larger q0, define unit harmonic flow φe=c_eΔeq0/C0, and sample an A→B path by splitting outgoing probability in proportion to φ. Choose the starting vertex in A with probability equal to its total outgoing unit flow, and omit zero-flow edges. For a path γ, let

\[
 S_\gamma(\lambda)=\sum_{e\in\gamma}(\Delta_eq_0)e^{-\lambda Q_e}.
\]

Every sampled path has Σe∈γΔeq0=1. The Berman–Konsowa trial-flow bound gives

\[
 \frac{C_\lambda}{C_0}\geq
 \mathbb E_{\gamma\sim\phi}\frac{1}{S_\gamma(\lambda)}
 \geq\frac{1}{\mathbb E_{\nu_0}e^{-\lambda Q}}.\tag{6}
\]

The second inequality is Jensen plus the fact that edge visitation probability is φe. This stronger lower bound retains correlations of the perturbation along reference current paths, and is exact for both pure series and pure parallel networks. It requires only the reference flow; it does not require simulating the changed network. The formula is a specialization of an existing theorem. Its usefulness for uncertainty propagation is a possible application, with novelty yet to be established.

## Independent review outcome

The independent review in `research/review-scouting-nucleation.md` confirmed equations (1)–(4), normalization, and network sharpness. It caught the λ=0 exception in the interval-width statement; that wording is corrected above. It also strengthened continuum sharpness: an angular perturbation Q in a radial annulus has ∇Q·D∇q0=0 and saturates the upper bound exactly, while Q=F(q0) saturates the lower bound by the committor transformation just derived. Thus smooth connected-domain examples are available, not only thin-channel limits. The review does not establish novelty.

The extension review also confirmed equations (5)–(6). It supplied the precise starting distribution for multiple-source A and a direct pathwise Cauchy–Schwarz proof of (6), recorded in the review file. These clarifications are incorporated.
