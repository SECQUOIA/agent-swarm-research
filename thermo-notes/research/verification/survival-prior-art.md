# Prior-art audit: survival-conditioned thermodynamic integration

Date: 2026-09-07. Bounded independent literature audit of [the survival note](../survival-conditioned-thermodynamics.md). This report assesses novelty, not the independent proof checks recorded in [the review](survival-thermodynamics-review.md).

## Assessment

The most defensible candidate is the **specific error theorem for integrating endpoint-survivor mean forces under fixed conductances**: an exact Hellinger-affinity bound relative to the midpoint of two force potentials, with a second-order weak-killing error despite first-order occupation bias. I did not find that theorem in the openly accessible primary sources inspected. This is provisional evidence, not a claim that no earlier theorem exists.

The ingredients have substantial prior art. The distinction between endpoint QSD and interior conditioned law is classical. Eigenvalue derivatives, Doob transforms, nonconservative statistical forces, and arithmetic/geometric distribution means are established. A manuscript should present their consequence for a precisely stated sampling and control protocol, rather than claim a new general theory of nonequilibrium free energy or absorbing-state response.

The proposed susceptibility formula is an attractive exact corollary. Its spectral and Green–Kubo machinery is standard, so it needs a physical application or a useful inference consequence to carry a strong independent novelty claim.

## Exact candidate being compared

Let \(A h=\lambda W h\), \(W_{ii}=e^{-\beta E_i}\), with a fixed symmetric grounded conductance Laplacian \(A\). The three laws are

\[
\pi_i\propto e^{-\beta E_i},\qquad
\nu_i\propto e^{-\beta E_i}h_i,\qquad
\eta_i\propto e^{-\beta E_i}h_i^2.
\]

The canonical law and the interior law have exact force potentials; the endpoint law generally does not. With \(B=\sum_i\sqrt{\pi_i\eta_i}\) and \(m=(\pi+\eta)/2\),

\[
\nu_i=\frac{\sqrt{\pi_i\eta_i}}B,\qquad
\|\nu-m\|_{\rm TV}\le 1-B.
\]

Consequently, the difference between an endpoint force integral and the corresponding change in the midpoint potential is bounded by

\[
\int (1-B(E(s)))\,\operatorname{osc}(E'(s))\,ds.
\]

For weak killing this is \(O(\epsilon^2)\), under the uniform gap and bounded-parameter assumptions in the main note. The theorem concerns separately sampled endpoint ensembles. It does not identify this integral with the quasistatic mechanical work of a single trajectory conditioned on surviving the entire driving protocol.

For \(E(t)=E+tf\), the additional proposed identity is

\[
\frac{d^2F_{\rm surv}}{dt^2}
=-\beta\operatorname{Var}_{\eta}(f)
-2\beta\lambda\int_0^\infty
\operatorname{Cov}^{Q}_{\eta}(f(X_s),f(X_0))\,ds.
\]

Here \(Q\) is the reversible Doob process at the specified parameter value. The covariance integral is nonnegative; for a nonconstant observable on a connected finite graph it is positive. This is an instantaneous static derivative of the family of interior laws, not the endpoint response function.

## Absorbing-state FDT: close, but a different observable and protocol

P. Padmanabha, S. Azaele and A. Maritan, *Generalization of Fluctuation-Dissipation Theorem to Systems with Absorbing States*, New Journal of Physics **25**, 113001 (2023), DOI 10.1088/1367-2630/ad0616. The original 2022 submission used the title *Linear Response Theory and Fluctuation Dissipation Theorem for Systems with Absorbing States*. [Open primary preprint, arXiv:2204.02543](https://arxiv.org/abs/2204.02543).

I retrieved the complete v3 manuscript, searched its full text, and read the main response derivation and relevant supplementary material. Equations (7)–(12) describe endpoint-survival averages and their response, including the change in survival normalization. Equation (12) uses a survival-indicator subtraction and a derivative of the logarithm of the endpoint eigenvector. Equations (15)–(16) address survival and first-passage response.

This is direct prior art against claiming the first response theory for QSDs. I did not locate the fixed-conductance interior force potential, the Hellinger midpoint work bound, or the weak-killing integrability cancellation there. The proposed interior susceptibility is not equation (12): it differentiates a different law and a restricted generator family.

## Endpoint versus interior conditioning is established

R. Chetrite and H. Touchette, *Nonequilibrium Markov processes conditioned on large deviations*, Annales Henri Poincaré **16**, 2005–2057 (2015), DOI 10.1007/s00023-014-0375-8. [Open primary preprint](https://arxiv.org/abs/1405.5157).

Equation (139) gives the driven invariant density as the product of left and right principal eigenvectors. Section VI.C, equations (185)–(186), explicitly distinguishes the endpoint QSD from the law deep inside a long surviving trajectory. Section V.E discusses reversibility; the squared-eigenfunction weighting in the reversible case is established. The endpoint/interior distinction and its order of limits must therefore be presented as prior foundations.

M. Bauer and F. Cornu, *Affinity and Fluctuations in a Mesoscopic Noria*, Journal of Statistical Physics **155**, 703–736 (2014). [Open primary preprint](https://arxiv.org/abs/1402.2422).

Sections 2.3–2.4 derive long-survival conditioning and show that it preserves cycle affinities. These are cycles in the **state graph**, not loops of externally controlled energies. Their result does not contradict nonzero curl of an endpoint-occupation force form in parameter space. It does rule out interpreting that curl as conditioning creating a nonzero steady state-graph affinity in an originally reversible process.

## Nonconservative statistical forces and second-order expansions

C. Maes and K. Netočný, *Nonequilibrium corrections to gradient flow*, Chaos **29**, 073109 (2019), DOI 10.1063/1.5098055. [Open author manuscript](https://fys.kuleuven.be/english/staff/christ/files/pdf/pub/finalnongrad.pdf).

Section V gives the equilibrium stiffness/Maxwell relation, its nonequilibrium correction, and an exterior-derivative expression for force curl. Equations (35)–(36) connect the antisymmetric stiffness to entropic and kinetic responses. Section VI develops weak-driving expansions through second order, using prior nonequilibrium statistical mechanics results.

Thus “nonequilibrium occupations can yield nonconservative mean forces” is established. This source does not identify the special geometric relation among \(\pi,\nu,\eta\), or establish the present fixed-conductance cancellation. The latter is a restricted protection result, not a generic statement about weakly driven media.

A. E. Allahverdyan and D. Martirosyan, *Free energy for non-equilibrium quasi-stationary states* (2017). [Open primary preprint](https://arxiv.org/abs/1705.07517).

This constructs a work potential for a two-temperature system with separated time scales and restricted controls. Its “quasi-stationary” state is not the endpoint QSD of an absorbing process. It is relevant to broad claims about restricted-control work potentials, but is not an identified duplicate.

## Hellinger ingredients are standard

F. Nielsen, *On the Jensen–Shannon Symmetrization of Distances Relying on Abstract Means*, Entropy **21**, 485 (2019), DOI 10.3390/e21050485. [Open primary article](https://pmc.ncbi.nlm.nih.gov/articles/PMC7514974/), [author PDF](https://franknielsen.github.io/papers/entropy-21-00485-v2.pdf).

Definitions around equations (44)–(46) describe normalized geometric mixtures. Equation (139) states the relation between Hellinger distance and the arithmetic/geometric mean difference. These directly precede the elementary inequality used here. The exact TV inequality is readily obtained by writing the arithmetic mixture as the normalized geometric mixture plus a nonnegative residual. It should not be advertised as a major new distribution inequality.

The potentially useful contribution is that the two endpoints of this geometric interpolation have **exact force potentials under the same physical control**, making the quadratic distribution discrepancy a quantitative integration-error certificate.

## Escape-rate corrections to thermodynamic identities already exist

M. Šiler et al., *Diffusing Up the Hill: Dynamics and Equipartition in Highly Unstable Systems*, Physical Review Letters **121**, 230601 (2018), DOI 10.1103/PhysRevLett.121.230601. [Open primary preprint](https://arxiv.org/abs/1803.07833).

The paper studies unstable Brownian motion and derives an escape-rate correction to equipartition. In the retrieved v2, equation (5) is

\[
\langle V\rangle_{\mathrm{st},+}
=k_BT/n+(\lambda_0\gamma/2n)\langle x^2\rangle_{\mathrm{st},+}.
\]

The average uses the positive-half-line part of the QSD for an odd unstable power-law potential. This is neither the interior law nor the proposed integrated-covariance susceptibility, but it is clear prior art for a thermodynamic identity corrected by escape rate. Broad claims to that effect would be inaccurate.

## Why the susceptibility should be positioned cautiously

For a reversible finite Doob process, its integrated covariance equals a reduced resolvent quadratic form:

\[
\int_0^\infty\operatorname{Cov}_{\eta}^{Q}(f_s,f_0)\,ds
=\langle f-\eta f,(-Q)^{-1}(f-\eta f)\rangle_\eta.
\]

This is standard spectral correlation theory. Combining it with second-order perturbation of \(Ah=\lambda Wh\) produces the proposed formula. Alternatively, the interior law is Gibbsian with effective energies \(E_i-2\beta^{-1}\log h_i\); differentiating those energies explains why the bare variance does not give the full susceptibility.

I found no exact occurrence of the displayed formula in the inspected sources. Its plausible distinctive content is the fixed-conductance coefficient \(2\lambda\), the definite sign, and their interpretation. It should be described as a specialized spectral susceptibility identity until further literature review or a useful application supports a stronger claim.

## Search limits and recommendation

Searches included combinations of QSD/quasi-stationary, thermodynamic integration, free energy, mean force, Maxwell relations, Hellinger distance, weak killing, susceptibility, and conditioned-process covariance, followed by primary-reference tracing. Exact phrase searches produced many unrelated uses of “quasi-stationary”; their failure is weak novelty evidence.

Retain the candidate and develop it. A useful next step is an application where endpoint survival is actually used to estimate metastable free energies, showing when the midpoint correction and its certificate improve an observable calculation. Keep the fixed-conductance restriction explicit. The current evidence supports an internally reviewed research candidate, not a verified claim of publication-level priority or high citation impact.

Retrieved primary PDFs and extracted texts are stored under research/sources with prefixes padmanabha-etal-2022-absorbing-response, maes-etal-nonequilibrium-gradient, allahverdyan-martirosyan-2017-quasi-freeenergy, chetrite-touchette-2014-conditioned, siler-etal-2018-equipartition, and bauer-cornu-2014-noria.
