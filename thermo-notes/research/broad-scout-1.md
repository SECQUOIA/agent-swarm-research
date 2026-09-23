# Broader scout: learned-potential uncertainty at phase coexistence

Date: 2026-09-06. Scope: uncertainty in an interatomic Hamiltonian, not reservoir size. Status: a bounded asymptotic result and a useful negative novelty finding. Independent mathematical review is recorded in [the reviewer report](verification/learned-potential-geometry-review.md). The result is not yet a strong publication candidate: its ingredients are exponential tilting, conditional central limit theory, and established coexistence response identities.

## Assessment

The most useful question found in this cycle is whether fitting a potential to phase free energies also controls its finite-system phase probabilities and within-phase fluctuation laws. It does not generally do both. A precise local limit separates parameter perturbations normal and tangent to a coexistence manifold, and gives an explicit second-order correction to phase probabilities.

The physical subject is active and relevant to molecular thermodynamics, but several broad ideas are already occupied. Thermodynamic fitting of potential parameters dates at least to Hamiltonian Gibbs–Duhem integration, and recent work explicitly differentiates phase free energies with respect to learned-potential parameters. Generic reweighting, free-energy sensitivity, or training against transition temperatures would not be novel contributions.

The bounded result below is worth keeping as an uncertainty diagnostic and possible component of a stronger future method. I would not replace the reviewed physical-reservoir manuscript with this result alone. A useful next advance would have to supply a practical and independently validated certificate or sampling strategy, beyond the limit calculation itself.

## 1. Closest primary literature read early

**Potential fitting along coexistence is established.** Sturgeon and Laird, *Adjusting the melting point of a model system via Gibbs-Duhem integration: application to a model of Aluminum* (2000), derive a generalized coexistence equation including arbitrary potential parameters and use it to change a melting point while retaining fitted mechanical properties. Their Section II makes clear that parameter sensitivity is not restricted to pair potentials. [Open primary full text](https://arxiv.org/html/cond-mat/0006390v1).

**Propagation of learned-potential uncertainty through sampling is established.** Imbalzano et al., *Uncertainty estimation for molecular dynamics and sampling* (2021), use exact committee reweighting and a Gaussian cumulant/linear-response approximation. Their equations (20)–(24) and discussion explicitly distinguish the exact formula from the approximation and discuss deteriorating reweighting efficiency with system size. Appendix B gives functional uncertainty propagation. The present diagnostic must not be described as discovering that uncertain potentials change thermodynamic averages. [Open primary full text](https://arxiv.org/html/2011.08828v2).

**Differentiable phase thermodynamics is already a current research direction.** Swinburne, Lapointe and Marinica, *Score matching the descriptor density of states for model-agnostic free energy estimation*, published online December 2025, express a broad class of potentials as linear functions of extensive descriptors and learn an entropy representation for phase free energies. They demonstrate parameter uncertainty propagation and phase-boundary fitting. [Open primary article](https://www.nature.com/articles/s41467-025-66938-8).

Fuchs and Zavadlav, *Refining machine learning potentials through thermodynamic theory of phase transitions* (June 2026), introduce differentiable transition-temperature correction by matching phase free-energy differences. This directly occupies the broad proposal to improve a learned potential using thermodynamic coexistence constraints. [Open primary article](https://www.nature.com/articles/s41524-026-02195-7), [open preprint](https://arxiv.org/abs/2512.03974).

**Bulk validation and interface validation are already recognized as different.** Fazel et al., *Improving the reliability of machine learned potentials for modeling inhomogeneous liquids* (2024), train on inhomogeneous configurations and examine density response, surface tension, and cavitation free energies. Thus a general warning that bulk-trained potentials may fail for nucleation is not a new result. [Primary article](https://doi.org/10.1002/jcc.27353). The paper's abstract and accessible article text were inspected; no quantitative theorem from it is used below.

## 2. A local limit for uncertain Hamiltonian parameters

Fix inverse temperature \(\beta>0\). Let a reference canonical state law \(P_N\) have a fixed measurable phase partition \(A_{1,N},\ldots,A_{k,N}\) of its entire state space. The partition does not depend on the perturbed parameters. Assume

\[
P_N(A_{i,N})\to w_i>0,\qquad \sum_iw_i=1.
\tag{1}
\]

A linear Hamiltonian perturbation is

\[
\delta U_N(x)=\delta\theta_N\cdot S_N(x),\qquad S_N\in\mathbb R^p.
\tag{2}
\]

For a generalized linear learned potential, \(S_N\) is the sum of local descriptors. No learned-potential architecture is needed in the theorem. The reference potential may already contain other terms.

Within phase \(i\), assume

\[
X_{i,N}:=\frac{S_N-Nm_i}{\sqrt N}
\Longrightarrow Z_i\sim\mathcal N(0,\Sigma_i).
\tag{3}
\]

Covariance matrices may be singular. In addition to this weak limit, require enough exponential integrability for the intended tilts: a simple sufficient hypothesis for fixed \(h,g\) is

\[
\sup_{N,i}\mathbb E_{P_N(\cdot\mid A_{i,N})}
\exp(K\|X_{i,N}\|)<\infty
\tag{4}
\]

for some \(K>\beta\|h\|\). For sufficiently large \(N\), this also controls the small \(g/\sqrt N\) correction. The stronger margin in (4) gives uniform integrability of the reweighting factors. A phase CLT by itself does not give this control; exponentially rare descriptor tails could otherwise invalidate the conclusion.

Define the tangent subspace

\[
\mathcal T=\{h:\ h\cdot(m_i-m_1)=0\text{ for all }i\}.
\tag{5}
\]

Take fixed \(h\in\mathcal T\), \(g\in\mathbb R^p\), and

\[
\delta\theta_N=\frac h{\sqrt N}+\frac gN.
\tag{6}
\]

The perturbed canonical law is exactly

\[
\frac{dQ_N}{dP_N}(x)
=\frac{e^{-\beta\delta\theta_N\cdot S_N(x)}}
{\mathbb E_{P_N}e^{-\beta\delta\theta_N\cdot S_N}}.
\tag{7}
\]

**Conditional theorem.** Under (1)–(6), put

\[
a_i=-\beta g\cdot m_i+\frac{\beta^2}{2}h^T\Sigma_i h,
\qquad Z=\sum_iw_i e^{a_i}.
\tag{8}
\]

Then

\[
Q_N(A_{i,N})\longrightarrow\widetilde w_i
=\frac{w_i e^{a_i}}{Z},
\tag{9}
\]

and, conditional on phase \(i\), the standardized descriptors converge weakly under \(Q_N\) to

\[
\mathcal N(-\beta\Sigma_i h,\Sigma_i).
\tag{10}
\]

The exact full-state TV distance has limit

\[
\boxed{
\|Q_N-P_N\|_{\rm TV}\longrightarrow
\frac12\sum_iw_i
\mathbb E\left|
\frac{e^{-\beta g\cdot m_i-\beta h\cdot Z_i}}Z-1
\right|.}
\tag{11}
\]

Equation (10) is weak convergence; a conditional CLT does not establish TV convergence of descriptor distributions. Equation (11) nevertheless follows because TV between the original state laws is the expectation of their exact likelihood ratio, not a claim that the discrete or continuous descriptors have become normal in TV.

### Proof

For \(x\in A_{i,N}\), expand the exponent exactly:

\[
-\beta\delta\theta_N\cdot S_N
=-\beta\sqrt N\,h\cdot m_i
-\beta g\cdot m_i
-\beta h\cdot X_{i,N}
-\frac\beta{\sqrt N}g\cdot X_{i,N}.
\tag{12}
\]

The first term is independent of \(i\) by (5) and cancels in normalization. The remaining random exponent converges in distribution to \(-\beta g\cdot m_i-\beta h\cdot Z_i\). Condition (4) supplies uniform integrability, so its exponential mean converges to \(e^{a_i}\). This proves (9). Multiplication by a bounded continuous test function and the same argument give the tilted Gaussian law (10). Finally, apply uniform integrability to the absolute difference of the normalized likelihood from one to obtain (11).

This proof is an application of standard exponential tilting and the logic of local asymptotic likelihood theory. The finite phase label makes the limiting experiment a mixture rather than a single Gaussian shift. Calling it a new general statistical principle would be unjustified.

## 3. What the scales mean, and what they do not mean

A parameter displacement \(g/N\) can change phase probabilities by a finite amount while barely changing the standardized fluctuations inside a phase. It acts on the extensive descriptor contrasts \(N(m_i-m_j)\).

A displacement \(h/\sqrt N\) tangent to coexistence cancels those leading phase contrasts, but acts at order one on within-phase descriptor fluctuations. Different phase covariances then produce different normalization factors in (8). Tangency at first order does not preserve phase probabilities at second order.

These are scales for **nontrivial finite distortion**, not scales guaranteeing convergence in TV to the original law. In (11) the limiting TV vanishes exactly when the limiting likelihood is one almost surely. For positive phase weights this requires

\[
h^T\Sigma_i h=0\quad\text{for every }i,
\qquad g\cdot(m_i-m_j)=0\quad\text{for every }i,j.
\tag{13}
\]

In particular, a nonzero tangent direction with nonzero phase variance still changes the full law. If all relevant tangent covariances are positive definite, perturbations must be smaller than \(N^{-1/2}\) tangentially and \(N^{-1}\) normally for vanishing distortion within this local regime. Null directions and gauge parameters are exceptions. No universal training-set-size requirement follows without specifying how parameter uncertainty shrinks with training data.

Full-system TV can be an unnecessarily strict target for some applications. Convergence of a transition temperature or a local structural observable need not require these parameter scales. The theorem is useful only when preserving finite-system phase probabilities and fluctuation events is the stated objective.

## 4. Second-order coexistence compensation is established geometry

The limiting phase probabilities are preserved when all \(a_i\) are equal. Thus the required normal correction satisfies

\[
g\cdot(m_i-m_1)
=\frac\beta2h^T(\Sigma_i-\Sigma_1)h.
\tag{14}
\]

For two distinct descriptor means, one can always solve this one scalar equation for an unrestricted \(g\). Several phases give a linear system; any affine dependency of the \(m_i\) must also annihilate the corresponding variance contrasts.

When (14) is satisfied, the limiting full-state error simplifies to

\[
\lim_N\|Q_N-P_N\|_{\rm TV}
=\sum_iw_i\left[2\Phi\!\left(\frac\beta2\sqrt{h^T\Sigma_i h}\right)-1\right].
\]

This follows by comparing the one-dimensional Gaussian likelihood in the direction \(h\) within each phase. It gives the fluctuation error remaining after the phase probabilities have been corrected.

The origin of (14) should prevent an inflated novelty claim. If the restricted phase free energies per particle \(f_i(\theta)\) are twice differentiable and thermodynamic limits commute with these derivatives, their standard derivatives are

\[
\nabla f_i=m_i,\qquad \nabla^2f_i=-\beta\Sigma_i.
\]

Expanding \(f_i-f_1\) along
\(\theta(t)=\theta_0+th+t^2g\) gives

\[
f_i(\theta(t))-f_1(\theta(t))
=t\,h\cdot(m_i-m_1)
+t^2\left[g\cdot(m_i-m_1)
-\frac\beta2h^T(\Sigma_i-\Sigma_1)h\right]+o(t^2).
\]

Equation (14) is precisely the second derivative condition for following coexistence. Its content belongs to generalized Clapeyron/Hamiltonian Gibbs–Duhem geometry. The potentially useful refinement is its consequence for the complete finite-size likelihood and its irreducible within-phase error, not the curvature equation itself.

## 5. Exact diagnostic example

An exactly solvable labeled Gaussian reference illustrates the distinction without claiming to be a microscopic fluid. Take \(\beta=1\), two phase weights \(w_1=w_2=1/2\), descriptor means

\[
m_1=(-1,0),\quad m_2=(1,0),\quad
\Sigma_1=\operatorname{diag}(1,1),\quad
\Sigma_2=\operatorname{diag}(1,4),
\]

and let \(S_N\mid i\sim\mathcal N(Nm_i,N\Sigma_i)\) exactly. Choose \(h=(0,1)\).

With \(g=0\), the perturbation has the same zero mean in each phase. A first-order response calculation for the phase indicator gives zero because its covariance with the perturbation is zero. Yet exact reweighting yields

\[
Q_N(A_2)=\frac{e^2}{e^{1/2}+e^2}
=0.817574476\ldots
\]

for every \(N\), and the full-state TV is \(0.640770523\ldots\). The per-particle perturbation tends to zero while a finite phase-probability discrepancy remains. This is a counterexample to applying a linear approximation without checking its smallness condition, not a refutation of the explicitly conditional approximation in Imbalzano et al.

Taking \(g=(3/4,0)\) solves (14) and restores the phase weights exactly. Within-phase laws still move. The full-state TV tends to

\[
\Phi(1/2)+\Phi(1)-1=0.532807207\ldots,
\]

where \(\Phi\) is the standard normal CDF. Direct finite-Gaussian evaluation gives 0.535452431 at \(N=25\), 0.533471447 at \(N=100\), and 0.532813860 at \(N=10000\).

For reproducibility, if the original component weight is \(w_i\), the reweighted weight is \(q_i\), and the displacement has Mahalanobis length
\(d_i=\beta\sqrt{N\delta\theta_N^T\Sigma_i\delta\theta_N}\), its contribution to the positive part of the likelihood difference is

\[
q_i\Phi\!\left(\frac{\log(q_i/w_i)}{d_i}+\frac{d_i}2\right)
-w_i\Phi\!\left(\frac{\log(q_i/w_i)}{d_i}-\frac{d_i}2\right).
\]

For \(d_i=0\), use \((q_i-w_i)_+\) instead. Summing gives the full labeled-state TV. The numerical values above were evaluated with SciPy's normal CDF and independently reproduced by the reviewer; the analytic limits independently determine their interpretation.

## 6. A tempting second direction rejected on prior art

A global free-energy cumulant expansion near coexistence can have a parameter radius of convergence proportional to \(1/N\). This initially looked like a possible explanation for failing learned-potential uncertainty propagation. It is already a direct consequence of established first-order partition-function zero theory.

For the elementary two-branch approximation

\[
M_N(\lambda)=w_1e^{-\beta N\lambda d_1}
+w_2e^{-\beta N\lambda d_2},
\qquad d_1\ne d_2,
\]

the zeros satisfy

\[
\lambda_k=
\frac{\log(w_2/w_1)-i(2k+1)\pi}
{\beta N(d_2-d_1)}.
\]

The logarithm's Taylor series about zero therefore has radius

\[
R_N=
\frac{\sqrt{\log^2(w_2/w_1)+\pi^2}}
{\beta N|d_2-d_1|}.
\]

Biskup, Borgs, Chayes, Kleinwaks and Kotecký give a much stronger rigorous theory for first-order lattice models, including asymmetric phase weights and complex phase boundaries. Their phase-sum representation and zero-location equations already subsume this mechanism. [Open primary analysis](https://arxiv.org/abs/math-ph/0304007), [author-hosted full paper](https://www.math.ucla.edu/~biskup/PDFs/papers/bigZeros-final.pdf), [microscopic Pirogov–Sinai verification](https://arxiv.org/abs/math-ph/0312041).

Rephrasing those zeros as an MLIP cumulant-expansion problem may be pedagogically useful, but is not an adequate new theoretical result. Phase-conditional expansion followed by exact recombination avoids this particular cancellation; it does not by itself solve sampling overlap or establish a new estimator.

## 7. Research decision

Retain (8)–(14) as a checked local uncertainty result, with novelty unresolved and likely modest. It supplies a concrete finite-size diagnostic that separates phase-weight errors from within-phase errors, and identifies when a first-order tangent correction misses an order-one effect. Its assumptions are explicit, and its proof does not rely on an uncontrolled global Gaussian replacement.

Reject three broad publication claims: new thermodynamic potential fitting, a new generalized Clapeyron equation, and a new \(1/N\) cumulant-convergence mechanism. Primary work already establishes them. The current result also resembles the reservoir notes at the mathematical level—phase-dependent exponential normalization—although the uncertain-Hamiltonian control problem is physically different.

The exact linear perturbation assumption matters. For a nonlinear parameterized potential, its parameter Hessian can be extensive; at a parameter displacement of order \(N^{-1/2}\), the quadratic Hamiltonian term is order one and can alter the phase scores. Such terms must be retained before applying the formulas to general neural-network fine-tuning. The present result directly covers generalized linear models and frozen-feature readout parameters.

A stronger future contribution would need either a nonasymptotic, computable uncertainty bound validated on an atomistic phase boundary, or an active-learning method that reduces a specified thermodynamic uncertainty more efficiently than existing free-energy-targeted training. The present scout does not establish such a method, and no claim of higher impact than the current reservoir results is justified.
