# Independent review: a microscopic Potts model with kinetic energy

Date: 2026-09-06. Reviewer: independent subagent `review_physical_bath`.

## Verdict and scope

The proposed route proves the local phase-density limits and a uniform interior energy-tail bound for the mean-field three-state Potts model supplemented by independent quadratic kinetic degrees of freedom. The boundary-of-simplex issue and the kinetic density near zero can both be controlled uniformly. This gives a concrete microscopic realization of the hypotheses in [the physical finite-bath extension](../finite-bath-physical-extension.md).

This is a mean-field example. Its extensive valley is consistent with that model and does not establish the droplet-tail assumptions for short-range systems. This review verifies the inference from the stated Potts rate-function structure; it does not independently clear novelty or the literature provenance of that established structure.

Take fixed \(J,a>0\), \(\beta J=4\log2\), and

\[
U_N(n)=-\frac{J}{2N}\sum_{j=1}^3n_j^2,
\qquad \sum_jn_j=N,
\qquad K_N\sim\operatorname{Gamma}(aN,\text{rate }\beta),
\]

with canonical independence of \(U_N\) and \(K_N\). For a literal quadratic kinetic Hamiltonian, choose the number of quadratic degrees of freedom to be \(2aN\) along an admissible integer sequence. The arguments concern sufficiently large \(N\), so the eventual condition \(aN>1\) causes no issue.

The rate function on the simplex is

\[
I(p)=\sum_jp_j\log p_j-\frac{\beta J}{2}\sum_jp_j^2.
\]

The input used below is that its global minima are exactly the disordered point \((1/3,1/3,1/3)\) and the three permutations of \((2/3,1/6,1/6)\), all interior with positive definite Hessian on the simplex. Their potential-energy densities are \(-J/6\) and \(-J/4\), respectively. Adding \(a/\beta\) gives the two total-energy centers, with gap \(NJ/12\).

## 1. A uniform occupancy bound, including the boundary

Let \(M\) denote the four minima. Local positive definite Hessians, compactness of the simplex, and continuity of \(I\), including at its boundary, imply

\[
I(p)-I_{\min}\ge c_0\operatorname{dist}(p,M)^2
\]

globally. Away from fixed neighborhoods of the minima there is also a strictly positive rate gap.

Write \(Z_N^{\rm occ}\) for the unnormalized occupancy partition sum. Stirling's formula on an interior \(N^{-1/2}\)-neighborhood of one minimum gives

\[
Z_N^{\rm occ}\ge c_1e^{-NI_{\min}}.
\]

There are order \(N\) lattice points in this two-dimensional neighborhood, and each has unnormalized weight bounded below by a constant times \(N^{-1}e^{-NI_{\min}}\). This explains why no extra polynomial normalization factor is missing.

On any fixed interior subset of the simplex, uniform Stirling bounds consequently give

\[
\Pr(n)\le\frac{C}{N}e^{-N[I(p)-I_{\min}]},\qquad p=n/N.
\]

For the boundary strip, use the global multinomial type bound

\[
\frac{N!}{n_1!n_2!n_3!}\le e^{N[-\sum_jp_j\log p_j]}.
\]

It remains valid when coordinates vanish. Thus \(\Pr(n)\le Ce^{-N[I(p)-I_{\min}]}\) globally. Choose a fixed boundary strip disjoint from \(M\), with rate gap at least \(\eta>0\). Splitting the exponent into two halves gives

\[
e^{-N[I(p)-I_{\min}]}
\le e^{-N\eta/2}
e^{-(c_0/2)N\operatorname{dist}(p,M)^2}.
\]

Since \(Ne^{-N\eta/2}\) is bounded, the missing factor \(N^{-1}\) is recovered. Combining the interior and boundary regions proves the desired global estimate

\[
\boxed{\Pr(n)\le\frac{C}{N}
e^{-cN\operatorname{dist}(p,M)^2}.}
\]

This argument is stronger and cleaner than keeping unspecified boundary polynomial prefactors.

## 2. Uniform kinetic density control near zero

Let \(g_N(K)\) be the gamma density and \(k_0=a/\beta\). For any fixed finite upper bound \(k_{\max}>k_0\), sufficiently large \(N\) satisfy

\[
\frac{d^2}{dK^2}\log g_N(K)
=-\frac{aN-1}{K^2}\le-\frac{c}{N},
\qquad 0<K\le Nk_{\max}.
\]

Its mode is \(K_{\rm mode}=Nk_0-1/\beta\), and Stirling's formula gives \(g_N(K_{\rm mode})\le C/\sqrt N\). Taylor's inequality around the mode, followed by its bounded displacement from \(Nk_0\), therefore yields

\[
\boxed{g_N(Nk)\le\frac{C}{\sqrt N}
e^{-cN(k-k_0)^2},\qquad 0<k\le k_{\max}.}
\]

Set the density to zero at nonpositive kinetic energies. This proof handles arbitrarily small positive \(k\) without incorrectly treating the Stirling prefactor \(1/k\) as bounded. For total-energy density \(e\) in the fixed coexistence interval, boundedness of \(u(p)=-J\sum_jp_j^2/2\) supplies the required \(k_{\max}\).

## 3. The total-energy envelope

Partition the simplex by a nearest minimum \(p_i\), resolving ties arbitrarily, and put \(e_i=u(p_i)+k_0\). The function \(u\) is Lipschitz on the simplex. Hence

\[
|e-e_i|\le|e-u(p)-k_0|+L|p-p_i|,
\]

which implies, with fixed positive constants,

\[
c_1|p-p_i|^2+c_2|e-u(p)-k_0|^2
\ge c_3\bigl(|p-p_i|^2+|e-e_i|^2\bigr).
\]

Multiplying the occupancy and kinetic estimates and summing each partition gives

\[
p_N(Ne)\le\frac{C}{N\sqrt N}
\sum_i e^{-cN(e-e_i)^2}
\sum_{n_1,n_2}e^{-cN|n/N-p_i|^2}.
\]

The last lattice Gaussian sum is at most \(CN\), uniformly in the location of its center. Therefore

\[
\boxed{p_N(E)\le\frac{C}{\sqrt N}
\sum_i\exp\left[-c\frac{(E-Ne_i)^2}{N}\right]}
\]

throughout the coexistence interval. The three ordered minima have the same energy center and can be combined into one term. This is stronger than the interior tail envelope required by the physical-bath theorem, for any of its stated exponents \(\alpha\).

## 4. Local density limits follow by kinetic smoothing

A full occupancy local limit theorem is unnecessary. Discrete Laplace asymptotics around the four nondegenerate interior minima give positive limiting phase weights and a conditional central limit theorem for \(\sqrt N(p-p_i)\). The first-order delta method then gives a weak Gaussian limit for

\[
X_{i,N}=\frac{U_N-Nu(p_i)}{\sqrt N}
\]

conditioned on a fixed small neighborhood of phase \(i\).

At the disordered minimum the tangent gradient of \(u\) vanishes, so this limit is the point mass at zero. That is harmless: the kinetic contribution has strictly positive variance \(a/\beta^2\). At each ordered minimum the potential-energy contribution has a nonnegative finite Gaussian variance, equal for all three ordered phases by symmetry.

The standardized gamma variable \((K_N-Nk_0)/\sqrt N\) has densities converging uniformly to \(\phi_{a/\beta^2}\), with a uniform density bound. This follows directly from Stirling's formula near its mode and its vanishing density tails. Convolving with the conditional weak limit of \(X_{i,N}\) gives pointwise convergence of the standardized total-energy density to a Gaussian of variance

\[
v_i=\frac{a}{\beta^2}+v_i^{\rm pot}>0.
\]

The uniform kinetic density bound permits dominated convergence on every bounded standardized energy interval, yielding precisely the local L1 convergence required by the physical-bath theorem. Other occupancy phases do not contaminate this limit: the bound in section 3 suppresses their contribution at an energy separation of order \(N\). Occupancies outside fixed neighborhoods of all minima have exponentially small probability and bounded conditional kinetic densities, so their density contribution is negligible as well.

The three ordered phases combine into one positive low-energy weight; the disordered phase supplies the positive high-energy weight. Their limiting weights sum to one. Finite-size shifts of their centers by order one do not change the asserted \(\sqrt N\)-scale limits.

## Consequence and limitations

With the stated rate-function input, this model satisfies both canonical hypotheses needed for the physical finite-bath iff criterion. A constant-heat-capacity reservoir can reproduce its full canonical total-energy density in TV exactly in the asymptotic regime \(c_B/N^{3/2}\to\infty\), with the total-energy calibration specified in the physical-bath note. The stronger extensive-tail bound also supports the finite-error local crossover at a finite capacity coefficient.

The proof should retain fixed positive \(a\): taking the kinetic shape per particle to zero could remove the continuous smoothing and the disordered phase's \(\sqrt N\)-scale energy variance. No conclusion here establishes short-range interfacial morphology selection, dynamics, nucleation rates, or novelty of the resulting mean-field example.
