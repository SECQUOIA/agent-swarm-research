# Independent review: thermodynamics assembled from surviving trajectories

Date: 2026-09-06. Reviewer: nucleation scout, independently deriving the identities and the driven-protocol distinction. Scope: finite reversible Arrhenius networks, fixed conductance matrix, and energy-level controls. This is a mathematical and protocol review, not a determination of novelty.

## Verdict

The principal-eigenvalue derivative, endpoint/bulk distinction, and explicit endpoint curl are correct. The endpoint force integral need not be integrable. However, it must not be identified with the mean mechanical work of a trajectory conditioned to survive an entire quasistatic cycle: that ensemble has a different temporal-bulk law. In the stated fixed-conductance model, the latter law has an exact potential and its leading quasistatic cyclic work vanishes.

The parent's geometric-mean bound and weak-killing quadratic cancellation also check out, with spectral-gap assumptions stated below.

## Model and identities derived independently

Let A be a symmetric positive definite irreducible killed-network M-matrix, with nonpositive off-diagonal entries and A1≥0. Let W=diag(w_i), w_i=e^(−βE_i), and use the transient backward generator Q=−W⁻¹A. The absorbing transition rate from i is κ_i=(A1)_i/w_i. The principal eigenpair satisfies

\[
 Ah=\lambda Wh,\qquad h_i>0,\quad\lambda>0.
\]

The transient forward operator is Qᵀ=−AW⁻¹. Hence Wh is its positive right eigenvector, while h is the backward survival eigenfunction. For fixed parameters the long-time endpoint distribution conditional on survival is

\[
 \nu_i=\frac{w_ih_i}{\sum_jw_jh_j}.
\]

For an observation time well inside a much longer surviving trajectory, forward propagation supplies Wh and future survival supplies h. Their product gives

\[
 \eta_i=\frac{w_ih_i^2}{\sum_jw_jh_j^2}.
\]

This is also the invariant distribution of the corresponding Q-process. It is different from ν unless h is constant.

Differentiate Ah=λWh at fixed A and multiply by hᵀ. Symmetry cancels the eigenvector response, giving

\[
 \partial_{E_i}\lambda
 =-\lambda\frac{h^T(\partial_{E_i}W)h}{h^TWh}
 =\beta\lambda\eta_i.
\]

Therefore

\[
 \boxed{\sum_i\eta_i\,dE_i=\beta^{-1}d\log\lambda.}
\]

The logarithm can be written log(λ/λref) with a fixed reference rate to make its argument dimensionless. The canonical law π_i=w_i/Σw likewise gives Σπ_i dE_i=d[−β⁻¹logΣw]. Both one-forms are exact. If A depends on the controls, the additional term hᵀ(dA)h/(βλhᵀWh) must be included; the identity for the original energy forces alone then fails.

## Exact counterexample and minimal dimension

At β=1 and E=0, take

\[
 A=\begin{pmatrix}111/55&-1&0\\-1&2&-1\\0&-1&1\end{pmatrix}.
\]

Its off-diagonal graph is a three-state chain, with killing conductance 56/55 at state 1. Direct multiplication verifies

\[
 \lambda=1/5,\qquad h=(11/25,4/5,1)^T,
 \quad\nu=(11,20,25)/56,
 \quad\eta=(121,400,625)/1146.
\]

Independent symbolic differentiation, normalizing h3=1 while differentiating the generalized eigenproblem, gives the endpoint Jacobian J_ij=∂Ejν_i:

\[
 J=\begin{pmatrix}
 -11275/64176&275/4011&6875/64176\\
 4675/64176&-1975/8022&11125/64176\\
 275/2674&475/2674&-375/1337
 \end{pmatrix}.
\]

Both its row and column sums vanish, as required by common-energy-shift invariance and normalization. The curl is

\[
 \boxed{\partial_{E_2}\nu_1-\partial_{E_1}\nu_2=-275/64176\ne0.}
\]

For the conventional counterclockwise orientation in the (E1,E2) plane, the line integral Σν_i dE_i has the opposite positive area coefficient, 275/64176.

A two-state example with only energy controls cannot show this effect: common-shift invariance forces ν1=F(E1−E2), ν2=1−F, which makes the two-variable force form exact. Three transient states are therefore the minimal dimension under these controls.

## What a slow survival protocol actually measures

Let E(t)=E(s), s=t/T, be a smooth finite path with a uniform positive principal spectral separation along it. Assume the process is initialized in the endpoint QSD or is allowed a short initial relaxation. Distinguish three experiments.

1. **Separate fixed-parameter endpoint measurements.** At each E, run many replicas for long enough and retain those still alive. Their endpoint force is ν(E). Thermodynamic integration assembled from these separate experiments is ∫ν·dE and can depend on the chosen path. This is the unambiguous interpretation of the counterexample.
2. **A driven population, renormalized among current survivors at each time.** Its conditional endpoint law obeys the nonlinear normalized killed forward equation. In the adiabatic limit it follows ν(E(s)). Thus the integral of the *instantaneously renormalized mean force* tends to ∫ν·dE. It does not average work over a fixed set of trajectories: the ensemble used at time t depends on t.
3. **One driven experiment, retain only trajectories surviving the entire cycle.** If p_i(t) is the unnormalized forward live law and b_i(t)=Pr(τ>T|X_t=i) the backward remaining-survival factor, the conditional law at time t is exactly proportional to p_i(t)b_i(t). Away from endpoint relaxation layers, their adiabatic forms are Wh and h, respectively, yielding η. Therefore

\[
 \mathbb E\left[\int_0^T\dot E_{X_t}(t)dt\mid\tau>T\right]
 \longrightarrow\int\eta\cdot dE
 =\beta^{-1}\log\frac{\lambda(E_{\rm final})}{\lambda(E_{\rm initial})}.
\]

For a closed loop, this leading quasistatic mechanical work is zero. This limiting statement assumes finite state space, a smooth compact control path, a uniform spectral gap, and fixed A. It follows by the forward/backward adiabatic eigenvector expansion. Boundary layers contribute vanishing work because their physical duration stays finite while \dot E=O(T⁻¹). A complete uniform error theorem is not supplied here; direct numerical verification is below.

Mean work before absorption per *initial* replica is another observable:

\[
 \mathbb E\left[\int_0^{T\wedge\tau}\dot E_{X_t}(t)dt\right]
 =\int_0^T\Pr(\tau>t)\,\nu_t\cdot\dot E(t)dt.
\]

It includes survival weights and is not ∫ν·dE. For fixed positive killing along an increasingly slow cycle, survival becomes exponentially rare and this average tends to zero under bounded smooth driving.

Population replacement or cloning could maintain a fixed survivor population, but then resetting/selection is part of the physical operation and needs its own work, heat, and information accounting. The endpoint curl alone establishes neither extractable cyclic work nor an equilibrium-thermodynamics violation.

## Independent driven-network verification

`research/verification/check_survival_protocol.py` solves the normalized forward and backward equations for E1=0.3cos(2πs), E2=0.3sin(2πs), E3=0. It uses logarithmic probability ratios to enforce positivity and normalization, an implicit Radau integrator, and adaptive quadrature for work. This avoids underflow from exponentially small survival probabilities.

The separate fixed-parameter endpoint line integral is 0.00119602973; the corresponding η integral is zero to numerical precision. The driven results are:

| Cycle duration T | Instantaneously surviving ensemble integral | Mean mechanical work conditional on final survival |
|---:|---:|---:|
| 20 | 0.0168824622 | 0.0156444322 |
| 100 | 0.0046075462 | 0.0032055447 |
| 500 | 0.0018864011 | 0.0006403153 |
| 2000 | 0.0013689663 | 0.0001600021 |

The first column of integrals approaches the nonzero endpoint value; final-survival work decays approximately as 1/T. In the middle half of the T=2000 cycle, the maximum total-variation difference between the globally conditioned law and η was 1.11×10⁻⁴. These calculations support the protocol distinction; they do not prove the adiabatic limit for arbitrary networks.

## Verified midpoint and Hellinger bounds

Normalize Eπh=1, write h=1+δ, and v=Eπδ². Then ν=πh and η=πh²/(1+v). Exact subtraction gives

\[
 \nu_i-\frac{\pi_i+\eta_i}{2}
 =\pi_i\frac{v-\delta_i^2+2v\delta_i}{2(1+v)}.
\]

In particular the difference is second order in a uniformly small h−1. A sharper global estimate follows from the Bhattacharyya overlap

\[
 \mathcal B=\sum_i\sqrt{\pi_i\eta_i}=\frac1{\sqrt{1+v}},
 \quad \nu_i=\frac{\sqrt{\pi_i\eta_i}}{\mathcal B}.
\]

Let m=(π+η)/2. Pointwise,

\[
 m_i-\mathcal B\nu_i=\tfrac12(\sqrt{\pi_i}-\sqrt{\eta_i})^2\ge0.
\]

Thus m=\mathcal Bν+(1−\mathcal B)r for some probability law r (unless v=0, when all laws agree), and

\[
 \boxed{\operatorname{TV}(\nu,m)\le1-(1+v)^{-1/2}.}
\]

Since π and η have exact energy-force one-forms, for a closed smooth path at fixed A,

\[
 \boxed{\left|\oint\nu\cdot dE\right|
 \le\int_0^1\left[1-(1+v(s))^{-1/2}\right]
 \operatorname{osc}(E'(s))\,ds.}
\]

The oscillation max_i E′i−min_i E′i makes this bound invariant under a common shift of all energy levels. This controls endpoint-assembled force integrals, with the protocol restrictions just described. The geometric/arithmetic-mean inequality is familiar probability geometry; novelty of this application is unassessed.

## Spectral-gap control and weak killing

Write A=A0+diag(a), where A0 is the reflecting graph Laplacian and a≥0 the killing conductances. In the π-weighted inner product let H0=W⁻¹A0, let g>0 be its spectral gap on mean-zero functions, and let κ_i=a_i/w_i be the killing *rates*. The eigenproblem is (H0+κ)h=λh.

The elementary Poincaré argument gives

\[
 gv\le\langle h,H_0h\rangle_\pi
 =\lambda(1+v)-\langle\kappa h^2\rangle_\pi
 \le\lambda(1+v),
\]

hence v≤λ/(g−λ) if λ<g. This bound is valid but only first order in weak killing.

For a sharper estimate, let P project onto π-mean-zero functions. Projecting the exact eigenproblem and using h=1+δ gives

\[
 (H_0+P\kappa P-\lambda)\delta=-P\kappa.
\]

On the mean-zero space the operator on the left is bounded below by g+κmin−λ. Therefore

\[
 \boxed{v\le\frac{\operatorname{Var}_\pi\kappa}
 {(g+\kappa_{\min}-\lambda)^2}}
 \qquad\text{when }g+\kappa_{\min}>\lambda.
\]

Since λ≤Eπκ by the constant Rayleigh trial, one may replace λ in the denominator by Eπκ when that denominator stays positive. Uniform killing leaves h constant regardless of its magnitude. For κ=εκ0, a uniform positive reflecting gap and bounded coefficients along the control path imply v=O(ε²) and an endpoint cyclic-force integral O(ε²). The order claim assumes a fixed control-path length and uniform bounds; it is not uniform in paths that grow with 1/ε or approach a vanishing gap.

## Literature and novelty limits

The eigenfunction products and Hellmann–Feynman derivative are standard spectral facts; none is claimed new. The primary preprint *Generalization of Fluctuation-Dissipation Theorem to Systems with Absorbing States*, Padmanabha, Azaele, and Maritan (2022), <https://arxiv.org/abs/2204.02543>, is a close response-theory predecessor being audited by the originating scout. This review checked its bibliographic page, not its full derivation, and cannot exclude overlap.

Broad searches for quasistationary/quasistatic work and absorbing-state thermodynamics also surfaced existing geometric-work and nonequilibrium-force literature. The strongest currently justified result is a warning about mixing survival protocols, together with quantitative bounds on endpoint-assembled force nonintegrability in a specified model. A claim of a new quasistatic engine would be incorrect without a concrete operational protocol and complete accounting.

## Follow-up: verified Q-process response identity

The parent proposed an exact response formula for the spectral potential Fsurv=β⁻¹logλ. Let E(t)=E+tf with fixed vector f, and let \mathsf F=diag(f). Define the symmetric matrix G=W⁻¹/²AW⁻¹/², eigenpairs (λj,uj), and choose u0 positive and unit normalized. Then η_i=u0,i² and

\[
 G(t)=e^{\beta t\mathsf F/2}G e^{\beta t\mathsf F/2},
 \quad (G')_{j0}=\frac\beta2(\lambda_j+\lambda)\langle u_j,\mathsf Fu_0\rangle.
\]

Second-order eigenvalue perturbation, with the explicit G″ term retained, gives

\[
 (\log\lambda)''=-\beta^2\sum_{j>0}
 \frac{\lambda_j+\lambda}{\lambda_j-\lambda}
 |\langle u_j,\mathsf Fu_0\rangle|^2.
\]

The Q-process eigenfunctions uj/u0 are orthonormal in η and have relaxation rates λj−λ. Expanding its stationary autocovariance therefore verifies

\[
 \boxed{F_{\rm surv}''=-\beta\operatorname{Var}_\eta f
 -2\beta\lambda\int_0^\infty
 \operatorname{Cov}_\eta^Q(f(X_s),f(X_0))\,ds.}
\]

For this reversible process the integrated autocovariance is nonnegative, although individual trajectory products need not be. If gQ=λ1−λ>0,

\[
 -\beta(1+2\lambda/g_Q)\operatorname{Var}_\eta f
 \le F_{\rm surv}''\le-\beta\operatorname{Var}_\eta f.
\]

This confirms concavity and quantifies its departure from a bare canonical-looking fluctuation formula. The fixed-A and finite reversible network assumptions are essential. It is a standard spectral-perturbation derivation and needs comparison with the absorbing-state fluctuation-response literature before any novelty claim.

## Control-convention counterexample: first-order curl under variable conductances

Date of follow-up: 2026-09-07. The parent's proposed counterexample is correct. It shows that detailed balance and a long lifetime relative to intrabasin relaxation do not by themselves imply the O(ε²) endpoint cyclic-force cancellation proved above.

At β=1 use the same three-state chain, but vary its conductances with the energy controls:

\[
 c_{12}(E)=e^{-(E_1+E_2)/2},\qquad
 c_{23}(E)=e^{-(E_2+E_3)/2},\qquad
 a_1(E)=\varepsilon c\,e^{-E_1/2},\qquad c=56/55.
\]

Let A0(E) be the reflecting Laplacian of the two internal conductances, let Aε=A0+diag(a1,0,0), and keep W=diag(e^(−Ei)). The internal rates obey detailed balance with π∝e^(−E). At E=0 they coincide, for every ε, with the rates of the corresponding fixed-conductance chain. Their derivatives with respect to E do not coincide.

Write h=1+εu+O(ε²), with Σwiui=0. First-order perturbation of Aεh=λWh gives

\[
 A_0(E)u=\lambda_1(E)w-a(E),\qquad
 \lambda_1(E)=\frac{c e^{-E_1/2}}{\sum_i e^{-E_i}},
 \quad a(E)=c e^{-E_1/2}(1,0,0)^T.
\]

Here a excludes the explicit ε factor. At E=0,

\[
 u=c(-5,1,4)^T/9=(-56/99,56/495,224/495)^T.
\]

Since ν=π+επu+O(ε²), its first-order noncanonical correction is r=πu. Independent symbolic differentiation of the Poisson equation and its normalization gives

\[
 \left.\frac{\partial r_i}{\partial E_j}\right|_{E=0}
 =\begin{pmatrix}
 28/1485&-196/1485&28/1485\\
 -28/1485&-28/1485&28/495\\
 0&224/1485&-112/1485
 \end{pmatrix}.
\]

The canonical Jacobian has zero curl. Therefore

\[
 \boxed{\left.\left(\partial_{E_2}\nu_1-\partial_{E_1}\nu_2\right)\right|_{E=0}
 =-\frac{56}{495}\varepsilon+O(\varepsilon^2).}
\]

For sufficiently weak killing the reflecting relaxation gap remains O(1) while the decay rate is O(ε), so this is a counterexample even with strong timescale separation. The geometric-mean midpoint identity remains algebraically valid, but the η energy-force form is no longer exact when A varies. Its additional conductance-response term restores the correct eigenvalue differential. Consequently one cannot infer endpoint-force loop cancellation from closeness to the midpoint alone.

A common shift of all three *interior* energies is not a gauge symmetry of this particular control convention: internal rates remain unchanged, while killing rates scale as exp(shift/2). This is consistent with varying interior levels relative to an absorbing state whose reference energy is held fixed. It does not affect the two-control curl counterexample. The fixed-A assumption in the quadratic-protection result is therefore substantive, not just a choice of notation.
