# Stage 2, round 1 — independent review 4

## Verdict

**No major mathematical issues found.** The mean-field theorem, including the pure-spin case, follows from the stated arguments. The new short-range sufficiency proof supplies the previously missing positive-phase moment bound; I did not find a gap in its derivative, cutoff-removal, or bond-to-spin transfer chain. One source-convention clarification should be corrected before this stage closes.

I reviewed the frozen `sections/microscopic.tex`, its dependencies in the framework and threshold sections, and `refs.bib`. I consulted primary-source text in `sources/`, especially BCT 2012, BKMS 1991, BCHPT 2022, and the two mean-field papers. I did not consult other new reports, delegate, or edit the manuscript.

## Issue

### R4.1 — Distinguish the two contour exterior conventions

- **Severity:** minor source and notation clarification. The proof can consistently use the original BCT convention without changing its result.
- **Location:** The paragraph following equation `eq:sr-positive-contour-decomposition`, saying that the “exact event definitions” are also recorded in BCHPT 2022, and the citation to its Section 3.8 in the proof of Lemma `lem:sr-restricted-derivatives`.
- **Evidence:** BCHPT 2022 explicitly states after Definition 5 in Section 3.4 that its definition of exterior differs from BCT 2012. Its interior is selected by component size. Its Lemma 3.9 consequently explains why the BCT geometric estimates still hold for the smaller interior. Therefore the event formulas look the same but are not literally the same definitions for every contour configuration. In this manuscript, the geometric estimate, cutoff criterion, truncated free energies, and partition-function remainder all come from the original BCT construction.
- **Correction:** State explicitly that the paper uses BCT's exterior convention throughout. Cite BCT equations (6.1)–(6.5) for the exact positive events and their multiplicity. Describe the 2022 construction as a related formulation with a modified exterior convention, rather than an identical definition. The derivative proof already cites BCT's matching-label sums (6.13)–(6.14), which suffice for its positive finite-sum estimates; retain those as the direct justification and qualify the 2022 random-cluster interpretation as a related representation. Alternatively prove equivalence of the particular quantities used, but that adds unnecessary work.

## Mean-field verification

### Complete minimum classification

The boundary exclusion uses the correct entropy sign. Equality of `log p_j - b p_j` yields at most two distinct coordinate values. If two entries take the larger value, the exchange direction has negative second variation because `b > 1/x`. The remaining scalar stationary equation has at most three roots by Rolle's theorem, and the three listed roots are correct. The middle root is a saddle; the uniform and ordered candidates have equal potential. This establishes completeness, rather than merely identifying locally stable candidates.

I recomputed the Hessian determinant and ordered energy variance. At `b=4 log 2`:

- `det H_o = 2.2018491675995744`, versus `3(3-b)(6-b) = 2.2018491675995757`.
- For `J=1`, `(H_o^{-1})_11/4 = 0.7328865494630357`, versus `1/[6(3-b)] = 0.7328865494630352`.
- The Gaussian prefactors give ordered total weight `0.5296771135094822`.

The Stirling prefactor, rescaled lattice density, and factor of three for ordered minima are consistent. The disordered energy gradient vanishes, while the ordered gradient does not. Consequently pure spins have one nondegenerate square-root-size phase even though the disordered fluctuation limit on that scale is a point mass. This is exactly enough for the asymmetric two-scale necessity theorem; adding kinetic variables is unnecessary for the exponent.

### Uniform positive-cell moments

The global quadratic rate lower bound follows from compactness, isolated complete minima, and positive local Hessians. On the boundary strip the positive rate gap absorbs the missing Stirling factor `1/N`. The resulting global occupation bound controls the Gaussian Riemann sums and supplies the phase probability lower bounds, so the later conditioning argument is not circular. Lipschitz energy control and completion of the square give the required exponential moment. Independent Gamma energy adds the same bound for any fixed sufficiently small transform argument. The decomposition has no exceptional mass, so the pure-spin and kinetic threshold proofs both apply directly.

### Gamma smoothing and interior envelope

Uniform standardized Gamma density convergence follows from its local asymptotics and unimodality. Convolution with the tight phase-conditioned spin-energy laws yields the local density limits, including the disordered point-mass spin limit. The Gamma log-curvature bound has the correct direction on the bounded kinetic-energy interval; its mode differs from the kinetic mean by a constant. The inequality combining occupation distance and kinetic mismatch is a valid Lipschitz estimate. The lattice sum cancels the occupation prefactor and gives the claimed full interior envelope. This does not assume a Gaussian mixture outside controlled neighborhoods.

### Exact physical finite-system formulas

Direct integration gives the occupation exponent `A+c_N`, not `A+c_N+1`, and the conditional Beta parameters are correctly `A` and `c_N+1`. Infeasible occupations have zero reservoir probability and are excluded from the conditional CDF sum. The shape-zero case is treated separately and correctly. Strict log-likelihood concavity yields an interval of positive normalized likelihood, and support-exterior root locations cause no problem for the CDF expression.

I independently evaluated a small system with `N=8`, `J=1`, `a=1/2`, `beta=4 log 2`, `A=4`, `c=20`, and secant total energy. The likelihood roots were approximately `-1.4190447712586993` and `0.8614119142543658`. The exact Gamma/Beta CDF formula gave total variation `0.11775323281926137`. Direct quadrature of the positive energy likelihood difference gave `0.11775323281926509`, an absolute difference of about `3.7e-15`. This check independently exercises the normalization, exponent, Beta parameter, roots, and CDF support conventions.

## Short-range verification

1. **Source normalization:** The spin Hamiltonian agrees with BKMS equation (6) at unit coupling. Direct expansion gives `Z_RC=e^{-beta dN} Z_spin`. Hence the branch relation `f_i^tr=psi_i+d beta` on the stable side has the correct sign. BKMS Theorem 1 provides the smooth real branches used by the proof; no analyticity or differentiation of a signed error is needed.
2. **Weak conditional limits:** The `1/N` real-temperature shift identifies the two macro-energy masses. The signed `1/sqrt(N)` shifts suppress the opposite midpoint event. Exponential tilting supplies a genuine moment-generating-function neighborhood; untilting gives vague convergence, and the known total masses upgrade it to weak convergence. This avoids an unjustified inference from a one-sided transform alone.
3. **Strict phase variances:** Conditional independence on a vertex independent set bounds the total canonical variance below by a positive multiple of `N`. Passing this strong convexity through stable thermodynamic branches and then to coexistence is valid. The proof correctly avoids treating the large coexistence variance as a conditional phase variance.
4. **Positive interior derivatives:** BCT equations (6.13)–(6.14) represent each interior partition function by positive finite sums with fixed geometric restrictions. The first log derivative is bounded by its involved volume, and the second includes a variance bounded by the volume squared. BCT Lemma 5.7 gives interior volume `O(m_gamma^2)`, so the displayed activity derivative estimates are adequate in every fixed dimension.
5. **Cluster derivative control:** BCT equations (A.5)–(A.6) have convergence slack for sufficiently large fixed `q`. Retaining an exponential cluster-size factor absorbs the polynomial factors introduced by one or two temperature derivatives. The minimum cutoff is used only at the absolutely-continuous, first-derivative level before establishing Lipschitz limiting free energies. This is legitimate and does not suppose that the minimum is twice differentiable.
6. **Cutoff removal:** Lipschitz branch differences vanish at coexistence. The original BCT Lemma A.1(i), combined with diameter at most `L`, therefore removes every finite-torus cutoff on a common interval of width proportional to `1/L`. On that interval the original positive activities are smooth and the second cluster derivative is bounded by `CN`.
7. **Center estimate:** The stable-side finite difference uses a shift of order `1/sqrt(N)`, inside the `1/L` interval for every `d>=2`. The exponentially small finite-volume error survives division by that shift. The resulting `O(sqrt(N))` mean-center error is sufficient for a fixed exponential moment; an unproved smaller error is not needed.
8. **Bond-to-spin transfer:** The fugacity derivative correctly produces occupied bond count, with `d beta/d lambda=p`. Conditional on spins, the bond count is Binomial with number of trials equal to the monochromatic-bond count. Its centered noise has a uniform exponential moment on the square-root scale. Conditioning on a positive-probability contour phase and Cauchy–Schwarz are enough; no independence after phase conditioning is assumed.
9. **Exceptional mass:** The tunneling probability decays as `exp[-b L^(d-1)]`. At `c_N >> N^(3/2)`, the largest reservoir gain is `exp[o(L^(d/2))]`, so the product vanishes for every fixed `d>=2`, including the borderline dimension two. The resulting spin--bond reweighting depends only on the spin Hamiltonian and projects to precisely the physical spin marginal.

The short-range proof thus supplies the inward physical-energy control needed by the positive-decomposition theorem. It does not substitute bond energy for spin energy, a signed partition-function remainder for a positive measure, or a weak local limit for a uniform moment bound.

## Scope

This report verifies the mathematics and the cited inputs inspected above. It does not certify that the resulting reservoir theorem is absent from all prior literature. Later manuscript sections and their final connections remain outside this stage review.
