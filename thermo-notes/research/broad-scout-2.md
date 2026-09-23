# Broader thermodynamics scout: survival sampling, potential validation, and interfacial inference

Date: 2026-09-06. Status: bounded initial scout, with one concrete candidate developed. The first direction was subsequently developed and independently verified in [survival-conditioned thermodynamics](survival-conditioned-thermodynamics.md); that note supersedes this initial scout. No result here is declared novel or publishable.

The strongest lead in this cycle is a distinction between two ways of sampling surviving metastable trajectories. A solvable reversible network shows that thermodynamic integration from their endpoint samples can depend on the integration path, while the corresponding averages deep inside long surviving trajectories have an exact potential under a specified Arrhenius control convention. This gives a physical sampling consequence rather than another stability-matrix reformulation.

## 1. Can survival-selected samples define a thermodynamic potential?

Metastable simulations commonly discard trajectories that leave a basin. Two limiting protocols are different:

1. Observe the endpoint at a large time t, conditional on survival until t. The limit is the quasi-stationary distribution, denoted ν.
2. Observe a time well away from both ends of a trajectory conditioned to survive until a much later time T, or average over such a long surviving trajectory. The limit is the quasi-ergodic distribution, denoted η; it is also the stationary distribution of the Q-process.

The distinction itself is established probability theory. The proposed question is whether these two sampling protocols have different thermodynamic integrability properties, and how large the resulting thermodynamic-integration bias can be.

### Exactly specified model

Consider n transient states with energies E_i at fixed inverse temperature β. Let w_i=exp(−βE_i), W=diag(w_i), and let c_ij=c_ji≥0 be fixed transition-state conductances on a connected graph. Let c_i0≥0 be conductances to an absorbing exit, with at least one nonzero. The transition rates are

\[
k_{ij}=c_{ij}/w_i,\qquad k_{i0}=c_{i0}/w_i.
\]

These are Arrhenius rates with transition-state energies and prefactors held fixed while well energies are changed. Internal transitions satisfy detailed balance with the restricted Boltzmann law π_i=w_i/Z. The absorbing process describes stopping an underlying reversible system at its first exit, rather than claiming the physical exit state has no possible return.

Define the symmetric grounded graph Laplacian

\[
A_{ij}=-c_{ij}\ (i\ne j),\qquad
A_{ii}=\sum_{j\ne i}c_{ij}+c_{i0}.
\]

It is positive definite. The backward killed generator is −W^{-1}A. Its principal eigenpair satisfies

\[
Ah=\lambda Wh,\qquad \lambda>0,\quad h_i>0.
\]

The two standard conditioned laws are

\[
\nu_i=\frac{w_i h_i}{\sum_jw_jh_j},
\qquad
\eta_i=\frac{w_i h_i^2}{\sum_jw_jh_j^2}.
\tag{1}
\]

### An exact potential for interior-of-trajectory averages

Differentiating the generalized eigenproblem at fixed A gives

\[
\partial_{E_i}\lambda
=\beta\lambda\frac{w_i h_i^2}{h^TWh}.
\]

Therefore

\[
\boxed{\eta_i=\partial_{E_i}\Phi,\qquad
\Phi(E)=\beta^{-1}\log[\lambda(E)/\lambda_{\rm ref}].}
\tag{2}
\]

Here λ_ref is an arbitrary fixed rate needed to make the logarithm dimensionless. Since the mechanical work differential for changing well energies is Σ_i occupation_i dE_i, the η-based mean-force field is exactly integrable.

This is a Hellmann–Feynman consequence, not a newly discovered spectral principle. Its possible contribution is the sampling interpretation and a quantitative comparison with endpoint averages. Changing barriers or prefactors with the controls adds

\[
d\Phi=\sum_i\eta_i\,dE_i+
\frac{h^T(dA)h}{\beta\lambda h^TWh}.
\tag{3}
\]

Thus the fixed-A convention is essential. It must not silently be replaced by rates proportional to exp[−β(E_j−E_i)/2], which describe a different control protocol.

There is also an elementary concavity property: the Rayleigh principle gives

\[
\Phi(E)=\beta^{-1}\inf_{h\ne0}
\left[\log(h^TAh)-\log\sum_i e^{-\beta E_i}h_i^2\right]
-\beta^{-1}\log\lambda_{\rm ref}.
\]

Each function minimized is concave in E; their infimum is concave. Hence its Hessian is negative semidefinite wherever differentiable. This provides a consistency condition for η-based occupation susceptibilities.

### Exact counterexample for endpoint samples

Set β=1 and

\[
A=\begin{pmatrix}
111/55&-1&0\\
-1&2&-1\\
0&-1&1
\end{pmatrix}.
\]

This is a three-state chain with unit internal conductances and exit conductance 56/55 from state 1. At E_1=E_2=E_3=0,

\[
\lambda=\frac15,\quad
h=\left(\frac{11}{25},\frac45,1\right)^T,\quad
\nu=\frac1{56}(11,20,25),\quad
\eta=\frac1{1146}(121,400,625).
\]

All entries of h are positive, so this is the principal eigenpair. Implicit differentiation of the generalized eigenproblem, with A fixed, gives

\[
\boxed{\partial_{E_2}\nu_1-\partial_{E_1}\nu_2
=-\frac{275}{64176}\ne0.}
\tag{4}
\]

For reproducibility, the full occupation Jacobian J_ij=∂_{E_j}ν_i at this point is

\[
J=\frac1{64176}
\begin{pmatrix}
-11275&4400&6875\\
4675&-15800&11125\\
6600&11400&-18000
\end{pmatrix}.
\]

Both row and column sums vanish, as required by invariance under a uniform energy shift and probability normalization. The rational calculation was performed using SymPy by fixing h_3=1, differentiating Ah=λWh, inserting ∂_iλ=λη_i, and differentiating ν=Wh/(1^TWh). The subsequent [independent review](verification/survival-thermodynamics-review.md) verified this calculation and its protocol limits.

The defensible physical statement is that **thermodynamic integration assembled from separate fixed-parameter endpoint-QSD samples can be path-dependent**. This is not a claim of free work extraction from a single heat bath. A globally survival-conditioned driven protocol may sample a different forward/backward weighting; it has not been derived here. Selection costs, sample rejection, and boundary layers cannot be omitted from a thermodynamic engine interpretation.

### First-order protection in the metastable limit

The parent agent independently identified the useful extension. Scale the exit conductances by ε, while keeping internal conductances fixed. At fixed finite n and a nonzero internal mixing gap, normalize h so ⟨h⟩_π=1. Perturbation theory gives h=1+εg+O(ε²), with ⟨g⟩_π=0. Equation (1) yields

\[
\nu=\pi+\epsilon\pi g+O(\epsilon^2),\qquad
\eta=\pi+2\epsilon\pi g+O(\epsilon^2).
\]

Consequently

\[
\boxed{\nu=\tfrac12(\pi+\eta)+O(\epsilon^2).}\tag{5}
\]

Both π·dE and η·dE are exact differentials. Endpoint-QSD thermodynamic integration is therefore integrable through first order in weak killing, even though its occupations already differ from restricted equilibrium at first order. A Maxwell-relation defect first appears at second order, provided the expansion is uniform with the required control derivatives.

The exact geometric-mean identity behind this cancellation is

\[
\nu_i=\frac{\sqrt{\pi_i\eta_i}}{\sum_j\sqrt{\pi_j\eta_j}}.
\tag{6}
\]

Equation (5), a uniform spectral-gap error bound, and a physically justified sampling protocol appear more substantial than the isolated counterexample. A small measured Maxwell defect need not imply equally small error in metastable averages.

### Closest primary literature and novelty limits

- Padmanabha, Azaele, and Maritan, *Linear Response Theory and Fluctuation Dissipation Theorem for Systems with Absorbing States* (2022), [arXiv:2204.02543](https://arxiv.org/abs/2204.02543). This already develops response of survival-conditioned observables and the associated modified fluctuation–dissipation theorem. Main text and supplement were retrieved. It prevents a broad claim that response theory for survival-selected states is new. Its displayed spectral derivatives are close ingredients; an exact match to (2), (4), or the weak-killing cancellation was not identified in the inspected material.
- Maes and Netočný, *Nonequilibrium corrections to gradient flow*, Chaos **29**, 073109 (2019), [DOI 10.1063/1.5098055](https://doi.org/10.1063/1.5098055), [author PDF](https://fys.kuleuven.be/english/staff/christ/files/pdf/pub/finalnongrad.pdf). Sections V–VI explicitly derive violations of Maxwell symmetry for statistical forces and discuss second-order corrections. Their medium is maintained in a nonequilibrium steady state; their small parameter is driving amplitude, not killing in a reversible basin. The general curl idea is established; its survival-specific cancellation requires a narrower comparison.
- Allahverdyan and Martirosyan, *Free energy for non-equilibrium quasi-stationary states* (2017), [arXiv:1705.07517](https://arxiv.org/abs/1705.07517). It proves work-potential existence for a two-bath slow/fast system under partial control and effective detailed balance. Its use of “quasi-stationary” is a separation-of-time-scales steady-state construction, not the endpoint-conditioned killed-process law above. It is relevant prior for the general integrability question, not an identified duplicate.
- Champagnat and Villemonais, *General criteria for the study of quasi-stationarity*, [arXiv:1712.08092](https://arxiv.org/abs/1712.08092), supplies the established QSD/Q-process framework. The standard distinction between endpoint and trajectory-interior distributions must be attributed to this broader literature.

Searches specifically combining survival conditioning, quasi-stationary/quasi-ergodic distributions, Hellmann–Feynman derivatives, geometric means, Maxwell relations, and second-order protection did not reveal an exact duplicate. This is provisional evidence only; a manuscript requires a closer spectral-thermodynamic-formalism search.

## 2. Can potential-validation errors certify phase weights?

This is highly relevant to molecular simulation but already crowded. A tractable theorem would separate the data needed to control intraphase structure from the data needed to control relative phase normalization. For example, at two-phase coexistence, a phase-specific energy bias δf per particle changes phase log-odds by βNδf; force errors within either basin can remain small. A useful advance would be a sharp, feasible validation protocol with a guarantee that remains informative as N grows, rather than another demonstration that small force error does not guarantee correct phase behavior.

Two recent primary papers already make the broad issue explicit:

- *Deep Coarse-grained Potentials via Relative Entropy Minimization* (2022), [arXiv:2208.10330](https://arxiv.org/abs/2208.10330), identifies sensitivity of force-matched free-energy surfaces to undersampled transition regions and develops relative-entropy training.
- *Refining machine learning potentials through thermodynamic theory of phase transitions*, npj Computational Materials (2026), [DOI 10.1038/s41524-026-02195-7](https://doi.org/10.1038/s41524-026-02195-7), directly trains coexistence constraints. It explicitly explains how phase energy offsets can alter phase stability while changing forces mainly in rarely visited transition states.

**Negative result:** the simple force-error/phase-weight no-go is not a new direction. A globally phase-flat perturbation is also often nonlocal, so it does not by itself establish failure for the finite-range atomistic architectures used in practice. A stronger candidate would prove a locality-aware sample-complexity or certification theorem and compare it with thermodynamic training methods. This is deferred rather than promoted.

## 3. What bulk information is sufficient to bound a nucleation barrier?

Bulk equations of state do not generally determine interfacial costs. A possible high-impact target is a quantitative identifiability theorem: specify which bulk measurements, interaction-range assumptions, and inhomogeneous observations suffice to bound surface tension or a nucleation barrier. This would directly inform potential validation and extrapolation to metastable states.

An elementary negative construction is already classical. For a square-gradient functional

\[
F_\kappa[\rho]=\int\left[f(\rho)+\frac{\kappa}{2}|\nabla\rho|^2\right]dx,
\]

all homogeneous free energies are independent of κ, whereas planar tension is proportional to √κ and a capillary nucleation barrier in d dimensions scales as κ^{d/2} at fixed bulk driving. The formulas are standard and should not be claimed as a new nonidentifiability theorem.

Kac models provide a microscopic version of the same issue. Alberti, Bellettini, Cassandro, and Presutti, *Surface Tension in Ising Systems with Kac Potentials*, Journal of Statistical Physics **82**, 743–796 (1996), [DOI 10.1007/BF02179792](https://doi.org/10.1007/BF02179792), derives the interfacial limit through Γ-convergence. A primary later discussion by Carlen and colleagues explains the distinction between bulk mean-field limits and interfacial continuum limits in [this author-hosted paper](https://cmsr.rutgers.edu/images/people/lebowitz_joel/publications/jll.pub_488.pdf).

**Negative result:** another example with identical bulk f and freely adjustable κ is too elementary. The tractable next question would constrain κ through actual bulk finite-wavevector structure factors and bound the error made when predicting curved interfaces. This requires explicit control of nonlocal kernels and higher-gradient terms; knowing only the small-wavevector coefficient may still leave the critical nucleus unconstrained. No such theorem was completed in this cycle.

## Disposition

Continue direction 1 through independent review, stronger weak-killing bounds, and a careful observation protocol. Preserve directions 2–3 as useful problem statements and negative novelty findings. They should be revisited only with a concrete constraint or measurement that makes the desired guarantee nontrivial.
