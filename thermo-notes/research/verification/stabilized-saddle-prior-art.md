# Prior-art audit: unstable growth from stabilized correlations

Date: 2026-09-06. Scope: the rank-one harmonic reconstruction and its information bounds in [stabilized-saddle-kinetics.md](../stabilized-saddle-kinetics.md). This is a bounded adversarial literature audit, separate from the mathematical review.

**Assessment:** the central reconstruction identity is an algebraic form of an established restrained-trajectory/Grote–Hynes workflow. It should be retained as a useful derivation, with explicit attribution, and not presented as a new way to obtain barrier kinetics without fitting friction. The finite-record bounds and the simultaneous sharpness of the two-summary bounds remain possible small contributions. This search does not establish their priority, and the available evidence does not justify making this direction the leading high-impact manuscript candidate.

## Exact close precedent, not merely related motivation

Christopher N. Rowley and Benoît Roux, *A computational study of barium blockades in the KcsA potassium channel based on multi-ion potential of mean force calculations and free energy perturbation*, Journal of General Physiology **142**, 451–463 (2013), DOI [10.1085/jgp.201311049](https://doi.org/10.1085/jgp.201311049). The [open publisher text](https://rupress.org/jgp/article/142/4/451/43350/A-computational-study-of-barium-blockades-in-the), section “Calculation of the transmission coefficient,” gives the relevant formulas.

They stabilize the barrier with a harmonic restraint, measure the velocity autocorrelation and equilibrium variances, numerically Laplace transform the autocorrelation, and solve the Grote–Hynes reactive-frequency equation. Equation (5) determines the frequency-dependent memory transform. No parametric friction fit is required. Their demonstration uses a 500 ps restrained trajectory and explicitly evaluates the reactive frequency. They attribute the correlation method to Straub, Borkovec, and Berne (1988).

The following elimination, performed here, makes the equivalence precise. Write the centered position autocorrelation as \(C_x(t)\), its value at zero as \(C_0\), the velocity autocorrelation as \(C_v(t)\), and \(v_0=C_v(0)=1/(\beta m)\). Their memory formula is

\[
\frac{\widehat M(s)}m=-s+
\frac{v_0}{\widehat C_v(s)}-\frac{v_0}{sC_0}.
\]

Combining it with the Grote–Hynes equation

\[
\omega_b^2-s^2=s\widehat M(s)/m
\]

gives

\[
\frac{\widehat C_v(s)}s=
\frac{v_0}{\omega_b^2+v_0/C_0}.
\]

For an exactly harmonic model with restraint stiffness \(k\), the restrained effective stiffness is \(1/(\beta C_0)\), while the unrestrained effective barrier curvature is \(-m\omega_b^2\). Hence

\[
k=m\omega_b^2+\frac1{\beta C_0}.
\]

Stationarity gives \(C_v(t)=-C_x''(t)\); time-reversal symmetry gives \(C_x'(0)=0\). Integration by parts therefore gives

\[
\widehat C_v(s)/s=C_0-s\widehat C_x(s),
\]

and the published workflow reduces exactly to

\[
\boxed{\beta k[C_0-s\widehat C_x(s)]=1.}
\]

The deduction uses the harmonic and unchanged-memory assumptions. It is not a claim that every molecular simulation in the prior paper is an exact harmonic model. It does show that replacing the intermediate memory calculation by the displayed scalar equation does not establish substantive novelty. For an inertial harmonic model the same algebra holds, although complete monotonicity of the position correlation generally fails; the overdamped bounds must not be transferred automatically.

## Earlier source inspected

John E. Straub, Michal Borkovec, and Bruce J. Berne, *Molecular dynamics study of an isomerizing diatomic in a Lennard-Jones fluid*, Journal of Chemical Physics **89**, 4833–4847 (1988), DOI [10.1063/1.455678](https://doi.org/10.1063/1.455678), [author-hosted PDF](https://people.bu.edu/straub/pdffiles/pubs/JCP.89.4833.1988.pdf).

Section IV.C, “Reaction coordinate friction,” introduces a harmonically confined coordinate around a chosen position, derives the complementary correlation/memory equation, and extracts barrier-top friction from confined fluctuations. Equations (4.5)–(4.6) and the subsequent comparison with Grote–Hynes rates are the relevant passage. The paper also discusses dependence on position and the expectation that sufficiently local harmonic confinement isolates the local friction. Thus both the computational idea and its sensitivity to the dynamical environment are longstanding.

The downloaded PDF is a scan. An OCR text was generated for searching; equations should be checked in the PDF, not trusted from OCR. Local files have stem *literature/straub-borkovec-berne-1988-friction*.

Related established work includes Thomas B. Woolf and Benoît Roux, *Conformational Flexibility of o-Phosphorylcholine and o-Phosphorylethanolamine: A Molecular Dynamics Study of Solvation Effects*, JACS **116**, 5916–5926 (1994), [DOI 10.1021/ja00092a048](https://doi.org/10.1021/ja00092a048). Its bibliographic record was verified; the primary publisher full text was not openly retrieved in this audit. Position-dependent diffusion from restrained correlations also has an extensive later literature. These references further rule out a broad claim that kinetic information has newly been extracted from harmonic umbrellas.

## What remains of the bounds

The note proves

\[
\frac{q-1}{\tau_{\rm int}}\leq\lambda
\leq(q-1)a_{\rm init},
\qquad q=\beta kC_0>1.
\]

These are Jensen bounds for a positive spectral measure, or arithmetic/harmonic-mean bounds for its Stieltjes transform. The more specific assertion is that neither endpoint can be improved even when both \(a_{\rm init}\) and \(\tau_{\rm int}\) are fixed. The two-atom construction is a useful explicit information limit. No exact matching statement for this saddle-reconstruction problem was found in the searches below. That absence is weak novelty evidence: generalized moment inequalities are a large literature, and elementary extremal two-point measures are standard.

The finite-time and finite-grid bounds in the note require only a nonnegative decreasing correlation, not its full complete monotonicity. They bound the Laplace transform of the positive measure \(-dC\) by moving interval masses to endpoints and bounding the remaining tail. This is an elementary integration bound. Turning those transform bounds into brackets for a reactive-frequency root is an application that may be useful, but should not be described as a new general theorem about completely monotone functions.

Two especially relevant primary sources are:

- Alessandro Ceccato and Diego Frezzato, *Inequalities for overdamped fluctuating systems*, Journal of Mathematical Chemistry **57**, 1822–1839 (2019), [DOI 10.1007/s10910-019-01040-1](https://doi.org/10.1007/s10910-019-01040-1), [institutional record](https://www.research.unipd.it/handle/11577/3309708). It derives a lower bound on correlation time from an initial correlation segment supplied by simulation, using complete monotonicity and convexity. The openly readable publisher appendix, equations (30)–(31), explicitly derives the positive exponential spectral representation for overdamped equilibrium correlations. The main bound itself was not openly accessible; the repository record has no attached manuscript. Therefore an exact formula-level exclusion is unresolved. The broad idea of bounding correlation integrals from finite records is definitely prior.
- Henry J. Brown and Yury Grabovsky, *On Feasibility of Extrapolation of Completely Monotone Functions*, SIAM Journal on Mathematical Analysis **56**, 7713–7747 (2024), [DOI 10.1137/24M1652325](https://doi.org/10.1137/24M1652325), [open preprint](https://arxiv.org/abs/2401.15178). It studies worst-case extrapolation under finite-precision interval information, gives explicit discrepancy exponents, and derives optimality conditions for local extremizers. Section 7 treats the local problem. This is a stronger mathematical treatment of noisy completely monotone data than the present elementary brackets, although its target is extrapolated function values rather than the saddle root. Local PDF/text stem: *literature/brown-grabovsky-2024-monotone*.

The determinant/resolvent step is also the standard rank-one Birman–Schwinger or Sherman–Morrison reduction. It supplies an especially short exact proof for finite-dimensional reversible dynamics; it does not provide an independent novelty argument.

## Relation to the new confined-nucleation paper

Lunna Li, Fabienne Bachtiger, Aaron R. Finney, Erik E. Santiso, and Matteo Salvalaglio, *Computing Nucleation Rates from Confined Equilibria: The Critical Cluster Equivalence Principle*, JACS, published August 31, 2026, [DOI 10.1021/jacs.6c09002](https://doi.org/10.1021/jacs.6c09002). The [primary full text](https://pubs.acs.org/jacsat/article/doi/10.1021/jacs.6c09002/5381258/Computing-Nucleation-Rates-from-Confined), especially section 2.3, was inspected.

The paper maps confined stable clusters to open critical clusters thermodynamically. It then extracts an attachment frequency from confined detachment residence times, invoking population detailed balance and a Poisson exchange model. It acknowledges finite-size kinetic and sampling limitations and compares with other kinetic estimates. Its kinetic observable is successful monomer exchange; it does not propose the harmonic autocorrelation root considered here.

The mathematical distinction is important. Equality of an equilibrium distribution or matching chemical potentials does not determine the absolute mobility: multiplying a reversible generator by a positive constant preserves its equilibrium law and changes every rate. Detailed balance constrains forward/reverse rate ratios, not their common scale. Consequently physical bath removal needs an additional dynamical argument or measurement before the same-mobility harmonic theorem applies. This observation identifies an assumption to test; it is not evidence that the JACS numerical results are wrong.

The present root determines a local unstable linear growth eigenvalue, whereas a full nucleation rate also needs thermodynamic factors and a justified relationship between local and global dynamics. A meaningful follow-up would establish quantitative transfer conditions for a specified reservoir model, or produce statistically valid uncertainty bounds that demonstrably improve practical kinetic estimates.

## Search coverage and disposition

Queries combined harmonic restraint, barrier stabilization, Grote–Hynes, velocity/position autocorrelation, Laplace transform, friction extraction, dynamic umbrella removal, completely monotone correlation bounds, finite records, and rank-one resolvents. Citation tracing reached the 1988 original and the explicit 2013 implementation. The search also located the 2019 correlation-time inequalities and 2024 sharp extrapolation study. Failure to find an exact root-bracketing duplicate is not a priority proof.

Recommended status:

1. Mark the reconstruction identity as an established consequence with an independent proof.
2. Preserve the two-summary sharpness construction and finite-record brackets as reviewed, potentially useful modest findings.
3. Do not claim certified inference from empirical correlations without statistical uncertainty control.
4. Compare the exact Ceccato–Frezzato bound before any publication claim focused on finite-record inequalities.
5. Pursue a stronger application or new transfer theorem before treating this as a leading manuscript direction.
