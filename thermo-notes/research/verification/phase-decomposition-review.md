# Independent review: positive phase decomposition and the short-range route

Reviewer: `capacity_review`. Date: 2026-09-06. Reviewed `research/phase-decomposition-reservoir-criterion.md` and the current `research/short-range-potts-route.md`.

**Verdict on the lemma:** the proposed sufficient condition is correct. A single fixed exponential moment per positive phase law suffices; neither a local central limit theorem nor a density is needed. The stated scaling with exceptional mass is sufficient, with the advertised conservatism.

**Verdict on the short-range model:** the conditional weak-CLT extraction from the stated real-temperature partition asymptotics is mathematically valid. This does not close sufficiency for the actual two-dimensional Potts model. The positive phase-specific inward exponential-moment estimate for the physical spin energy remains a substantive missing result. No full short-range iff theorem is verified by this report.

## 1. Positive-mixture lemma

Let the mixture and moment assumptions be those in the criterion note. Endpoint calibration gives `h(E_-)=h(E_+)=0` after subtracting a constant. Since `Delta_N=O(N)` and `c_N >> N^(3/2)`, the exact endpoint derivative formulas imply

\[
|h_N'(E_{i,N})|\le C N/c_N,
\qquad
\sup_E h_N(E)\le C N^2/c_N.
\]

The maximum lies between the endpoints; concavity gives `h_N<=0` outside that interval. Both bounds concern the full feasible energy domain, with `exp(h_N)=0` beyond the bath cutoff. The cutoff lies far beyond every fixed standardized neighborhood of the high-energy endpoint.

For each phase, the tangent inequality gives

\[
\exp[h_N(E)]\le
\exp\left(\epsilon_N|E-E_{i,N}|/\sqrt N\right),
\qquad \epsilon_N=O(N^{3/2}/c_N)\to0.
\]

The assumed exponential moment implies tightness of `(E-E_i)/sqrt N`. Uniform convergence `h_N -> 0` on every fixed standardized window then implies `exp(h_N)->1` in phase probability. For all sufficiently large `N`, `2 epsilon_N<=eta`, so

\[
\sup_{N\text{ large}}\mathbb E_{P_{i,N}}e^{2h_N}\le M.
\]

This is a genuine uniform-integrability bound. It gives `E_phase |exp(h_N)-1| -> 0` without any Gaussian approximation. There is no need to control a local density or to assume equal phase variances.

For the exceptional positive measure,

\[
\delta_N\mathbb E_{R_N}|e^{h_N}-1|
\le\delta_N[1+\exp(CN^2/c_N)]\to0.
\]

Mixture weights need not converge or stay positive for this sufficient-condition proof. Their nonnegativity and sum equal to one are enough. Summing the three terms gives `E_P |exp(h_N)-1| -> 0`; normalization then gives total-variation convergence.

If the phase decomposition is defined on an enlarged positive spin–bond space, the same proof applies there because the likelihood is still the physical-energy function. Projection gives the desired spin or subsystem conclusion. A signed expansion into metastable partition terms does not meet this requirement.

## 2. Scaling and limits

If `delta_N<=exp(-s_N)` with `s_N -> infinity`, the condition

\[
c_N\gg\max\{N^{3/2},N^2/s_N\}
\]

implies `CN^2/c_N=o(s_N)` and therefore the required exceptional-mass estimate. For `s_N>=b sqrt N`, `c_N >> N^(3/2)` alone suffices. The conversions to `N=L^d` and surface-order exceptional probabilities in the note are correct.

This is a sufficient criterion based on the global possible reservoir amplification. It is not a necessary condition on the exceptional-mass exponent: an exceptional component situated near a phase center may receive much less amplification. The note states that limitation correctly.

The moment assumption must concern the energy actually exchanged with the bath. Replacing spin energy by occupied-bond count without controlling their relationship would invalidate its use here. Independent kinetic smoothing affects regularity and local variance; it does not establish a missing moment estimate for the spin phase.

## 3. A weaker premise already suffices for necessity

The criterion note refers to local Gaussian density limits as a way to recover the known necessary condition. They are sufficient, but stronger than needed for the concavity argument.

Suppose the positive phase weights have positive limiting values and

\[
(E-E_{i,N})/\sqrt N\ \big|\ \text{phase }i
\Rightarrow\mathcal N(0,v_i),\qquad v_i>0.
\]

If the bath-reweighted law converges in TV, its likelihood ratio `r_N=exp(h_N)/Z_N` tends to one in probability under each phase law: each conditional probability is bounded by the corresponding unconditional probability divided by its positive mixture weight.

Choose four fixed separated standardized intervals, two on either side of zero. Weak convergence to a positive-variance normal gives positive limiting probability to each interval. Probability convergence of `log r_N` to zero then guarantees at least one point in each interval at which `log r_N` tends to zero. The two outer secants bound the center derivative, and the chord/continued-secant argument bounds the center value. Thus

\[
\sqrt N h_N'(E_{i,N})\to0,
\qquad h_N(E_{i,N})-\log Z_N\to0.
\]

The reciprocal-temperature argument then proves `c_N >> N^(3/2)`. This works for discrete energies; no transfer to Lebesgue measure is needed. A cutoff cannot obstruct selecting the good points because it would force the likelihood ratio to zero on a positive-probability interval.

Consequently, verified conditional weak Gaussian limits with positive variances already supply necessity. Kinetic smoothing is still a useful way to guarantee positive variance if a spin phase has a degenerate limit, and to obtain a continuous benchmark, but its local density limit is not a logical prerequisite for necessity itself.

## 4. Conditional CLTs from one-sided real-temperature asymptotics

This section verifies the deduction **assuming** the uniform real-temperature expansion (A) in the route note, with its stated metastable free-energy smoothness and positive latent heat. It does not independently re-audit the source theorem's normalization or uniformity range.

Evaluating partition ratios at `beta_c+t/N` gives the Laplace transforms of the bounded energy density `U_N/N`. Taylor expansion of the two metastable terms therefore yields the two-point limiting law with weights `q/(q+1)` and `1/(q+1)`. The fixed midpoint energy events have those limiting probabilities because their boundary lies strictly between the limiting atoms.

At `beta_c+s/sqrt N`, `s>0`, the ordered term dominates. After centering at `Nu_o`, its first-order exponential cancels and the second-order term gives `w_o exp(sigma_o^2 s^2/2)`. The expansion's error is exponentially small relative to that dominant term, provided its asserted uniform form holds. The contribution from the opposite midpoint event is bounded by `exp[-s(u_d-u_o)sqrt N/2]`. Thus the ordered **positive subprobability measure** has the stated Laplace limit for every `s>0`. The disordered statement follows at the opposite temperature displacement and opposite Laplace sign.

A one-sided Laplace limit is enough here because the total phase mass is also known. To show this rigorously, let `mu_N` be the ordered subprobability law and

\[
L_N(s)=\int e^{-sx}\,d\mu_N(x)
\longrightarrow w e^{vs^2/2},\qquad s>0.
\]

Fix `s_0>0` and normalize the tilted measures

\[
d\widetilde\mu_N(x)=e^{-s_0x}d\mu_N(x)/L_N(s_0).
\]

Their moment-generating functions at `|t|<s_0` are `L_N(s_0-t)/L_N(s_0)` and converge to

\[
\exp(-v s_0t+vt^2/2),
\]

the MGF of a normal law with mean `-v s_0` and variance `v`. The ordinary MGF convergence theorem therefore gives weak convergence of the tilted probability measures. Untilting against compactly supported continuous functions yields vague convergence of `mu_N` to `w Normal(0,v)`. Because `mu_N(R)->w`, the limit has the full limiting mass; vague convergence is therefore weak convergence, with no mass escape.

The nonnegativity of `v` follows independently from convexity of `log L_N(s)` on the positive half-line and its quadratic limit. Zero variance is allowed in this step. This derivation uses no complex-temperature extension and does not pretend that a metastable exponential term is itself a probability law.

The deduction is sound. It should remain explicitly conditional on checking that the cited partition theorem gives (A), uniformly at real displacements of order `N^(-1/2)`, with the route's Hamiltonian and dimensionless-free-energy conventions.

## 5. Kinetic convolution

The standardized Gamma kinetic density converges uniformly to a bounded continuous Gaussian density. Convolving it with the conditional weak spin-energy limit gives pointwise convergence of the total standardized energy density to the appropriate Gaussian convolution. Both are probability densities, so Scheffé's lemma also yields global L1 convergence; one can alternatively use the tightness argument in the route note.

Contributions from the other phase do not spoil the local limit. Their centers are separated by order `sqrt N` in standardized coordinates, and global L1 convergence of each component implies that its mass in a bounded window centered on the other phase tends to zero. The added kinetic variance `a/beta_c^2` is strictly positive for the stated fixed `a>0`.

Thus this smoothing argument is correct once the conditional weak spin CLTs are established. It does not generate uniform exponential moments for the inward spin-energy tail.

## 6. Separate proof-gap verdict for the actual two-dimensional model

The route note currently distinguishes the completed reductions from the missing microscopic estimate correctly. The remaining gap is substantive:

1. A positive contour decomposition and an exponentially small tunneling probability are not yet a uniform exponential-moment bound for the actual spin energy within each phase.
2. Differentiating a bond-restricted random-cluster partition function also differentiates the temperature-dependent spin–bond kernel. It cannot be equated with the conditional physical-spin-energy transform without another argument.
3. The real-temperature partition expansion gives the **outward** conditional Laplace transforms needed for the weak CLTs. The reservoir amplifies **inward** phase fluctuations. The former do not bound the latter by themselves.
4. Interface or Peierls costs require a controlled volume-versus-boundary argument, treatment of nested interiors, and centering of energy fluctuations to establish the required fixed small exponential moment. Calling this a standard phase-decomposition consequence would leave the main sufficiency step unproved.

The positive-decomposition criterion is therefore verified as an abstract theorem. The proposed conditional weak-CLT route is verified as a deduction from (A). These are useful advances, but they do not justify promoting the current notes to a full short-range Potts reservoir iff theorem. Once (A)'s source hypotheses are checked, necessity can be asserted for the kinetically smoothed model; sufficiency still requires the physical-energy moment estimate or a comparably strong positive-measure bound.

## Final spin-only upgrade check, 2026-09-07

The added Section 3.1 of `short-range-potts-route.md` correctly proves `sigma_o^2,sigma_d^2>0` without auxiliary kinetic energy. The square torus has degree at most four and an independent set of size at least `N/5`. Conditional on its complement, site energies are independent; for `q>4` their neighbor-color counts include a zero and a positive value. The stated lower bound on every color probability therefore gives conditional variance at least `q^(-2)exp(-8 beta_max)` per selected site, uniformly on a compact temperature interval.

The resulting inequality `N^(-1) Var_beta(U_N)>=v_*` means `N^(-1)log Z_N-v_* beta^2/2` is convex. Its pointwise limit is convex. On each stable side, the limit equals the corresponding smooth pressure branch minus that quadratic term, giving `-psi_i''>=v_*`; continuity extends the lower bound to the coexistence endpoint. These are precisely the variance coefficients identified by the already reviewed weak CLTs. No convergence of conditional second moments has been assumed.

The source audit now records the required uniform real-temperature expansion and Hamiltonian normalization. Conditional on that audited primary theorem, the mathematical deduction is complete for spin-only necessity. The unresolved physical-energy inward exponential-moment estimate still prevents promotion to an isolated short-range iff theorem, and the current route note retains that restriction.
