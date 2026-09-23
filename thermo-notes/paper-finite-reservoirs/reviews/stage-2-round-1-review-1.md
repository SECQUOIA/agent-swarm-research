# Stage 2, round 1, independent review 1

**Verdict: no major issues.** I independently checked the new short-range sufficiency argument against the supplied primary sources. The cutoff-removal and differentiation argument closes the claimed gap for every fixed dimension at least two and sufficiently large fixed `q`. I found one minor source-scope and exposition issue, described below. The mean-field and finite-system developments are also mathematically consistent.

## Scope and independence

I reviewed `sections/microscopic.tex`, `main.tex`, `refs.bib`, the earlier mathematical dependencies, and the Stage 2 author record. I did not consult other current review reports, edit manuscript files, or delegate. Missing future sections are outside this stage's scope. I inspected the locally retained primary texts, rather than treating the author record's characterization of them as evidence.

## Required correction

### Minor: distinguish general matching-contour sums from the restricted scope of the random-cluster interpretation

**Location:** proof of Lemma `lem:sr-restricted-derivatives`, first paragraph, especially the sentence citing Section 3.8 of Borgs–Chayes–Helmuth–Perkins–Tetali (BCHPT).

**Issue:** BCHPT Section 3.8 explicitly cautions that general contour partition functions do not coincide with ordinary random-cluster partition functions because interfaces are excluded. Proposition 3.14 establishes its ordinary random-cluster interpretation under an embedding and simple-connectivity hypothesis. The manuscript's wording about positive sums with fixed geometric restrictions is defensible, and it separately cites the more general matching-label representation, so this does not invalidate the activity derivative bound. However, the Section 3.8 citation should not appear to supply an unrestricted representation for every torus contour interior.

**Correction:** Ground the estimate explicitly in BCT (6.13)–(6.14). For each admissible matching-contour family, its logarithmic weight is a sum of the two ground coefficients times their respective vertex counts, `-kappa` times the total internal contour size, and beta-independent powers of `q`. The two vertex counts sum to the interior volume. Compatibility and the bounded-degree contour embedding bound the total contour size in the interior by a dimension-dependent constant times the interior volume plus outer contour size. One may cite the geometry underlying BCHPT Section 3.7 and Lemma 3.13 for this last count. Thus each logarithmic summand has first and second beta derivatives bounded by `C (|Int gamma| + m_gamma)`. Apply the positive-sum differentiation formula already displayed in the proof. Restrict the Section 3.8 citation to cases where its embedding hypothesis holds, or omit that citation from this general step.

This is a clarification of an available elementary proof, not a request for an extra phase-stability assumption. In particular, no ordinary unrestricted random-cluster representation is needed to bound derivatives of positive matching-contour sums.

## Checks of the new short-range sufficiency proof

### Primary inputs

- **BCT printed pp. 21–23, Lemma 5.7:** its diameter definition gives `diam gamma <= L`, and its two asserted geometric inequalities give `diam gamma <= m_gamma/2` and `|Int gamma| <= m_gamma diam gamma/2`. Hence the volume is at most `m_gamma^2/4`, in every stated fixed dimension. The argument does not replace this bound with the generally different power from a sharp isoperimetric inequality.
- **BCT pp. 25–28, (6.1)–(6.5) and (6.13)–(6.22):** the ordered, disordered, and tunneling events are genuine positive, temperature-independent geometric events. The ordered multiplicity is `q`. The activity ratios and polymer partition forms in the draft have the correct direction and multiplicity.
- **BCT p. 39, (A.1):** the appendix expressly treats both sides of the transition whenever its low-temperature inequality holds. For sufficiently large fixed `q`, a fixed neighborhood of coexistence satisfies this input; the proof need not rely only on the main-text statement for the ordered side.
- **BCT p. 40, (A.3)–(A.8):** the cutoff is the minimum of an exact positive activity and a smooth exponential cap. The convergence estimates retain an exponential size margin. The thermodynamic limit and the exponentially small full-torus pressure error used in the manuscript are supplied there.
- **BCT p. 41, Lemma A.1(i):** the stated sufficient condition gives equality of the truncated and original activities, not just a smallness bound. This exact equality is the crucial input needed to differentiate original activities.
- **BCT p. 44, Lemma A.3; BCHPT Appendix B.1:** these support the stable-phase identification and its disordered-side version. BKMS Theorem 1 independently supplies the smooth stable free-energy branches for the same spin Hamiltonian.
- **BCHPT Lemma 2.1 and (19):** the anchored absolute cluster bound includes an exponential total-size factor. Summing it over the bounded-degree embedding gives the stated `C N` global bound. Its usefulness here is not limited to the unweighted convergence of the cluster series.

### Activity derivatives without circularity

Writing each positive interior partition sum as `S = sum exp(F_j)`, the bounds on individual logarithmic summands imply `|(log S)'| <= C V` and `|(log S)''| <= C(V+V^2)`, where `V = |Int gamma| + m_gamma`. Applying these bounds to the numerator and denominator of the activity and using `V = O(m_gamma^2)` gives

`|(log K)'| <= C m_gamma^2`, and `|K''| <= C m_gamma^4 K`.

The raw ratios may be large away from phase stability, but these relative derivative bounds remain valid. Therefore the proof does not first require the stability or the derivative estimates that it subsequently derives from truncation.

For the minimum-truncated activity, local absolute continuity follows because both positive branches are smooth. Almost everywhere the derivative is the derivative of an active branch. On the exact branch the preceding relative estimate applies, and on the cap branch its logarithmic derivative is only order `m_gamma`. Thus `|(K')_beta| <= C m_gamma^2 K'` almost everywhere, including without a differentiable switching temperature. The positive exponential cluster majorant absorbs the first-derivative polynomial and justifies integration of the differentiated series. It supplies a Lipschitz constant of order `N` for each finite-volume logarithmic partition function and a constant independent of volume for its pressure.

### Cutoff-free window and second derivatives

Uniform Lipschitz continuity passes to the infinite-volume truncated free energies. Their equality at coexistence then gives `a_i(beta) <= C |beta-beta_c|`. Combining this with `diam gamma <= L` removes all torus cutoffs on a fixed multiple of the interval of width `1/L`. This step uses the already established first-derivative control only; it does not assume twice differentiable truncated pressures.

On the resulting interval the activities are their original smooth positive functions. The second derivative of a cluster product is bounded by a constant times the fourth power of its total contour size times its original absolute weight. Since original and truncated weights coincide on this interval, the same exponential majorant absorbs this factor. The twice differentiated series is therefore uniformly summable and gives `|d^2 log Z_i/d beta^2| <= C N`. Differentiation never crosses an unresolved minimum cutoff.

### Correct centering and all fixed dimensions

The stable-side displacement used to identify the center is proportional to `1/sqrt(N)`, not `1/L`. Since `sqrt(N) = L^(d/2) >= L` for `d >= 2`, it lies in the cutoff-free window. Taylor's remainder contributes `O(sqrt(N))` to the first derivative; division of the finite-volume exponential error by this displacement is still negligible for every fixed `d`. Hence the claimed center `-N u_i + O(sqrt(N))` is sufficient for the subsequent exponential moment.

The final exceptional contribution is also dimensionally consistent: its logarithmic suppression is of order `L^(d-1)`, whereas the bath gain is `o(sqrt(N)) = o(L^(d/2))`. The inequality `d-1 >= d/2` is exactly what is required, including equality at `d=2`.

### Bond-to-spin transfer

The normalization `Z_RC = exp(-beta dN) Z_spin` is correct for the specified negative-monochromatic-bond Hamiltonian. In the parameter `lambda = log(exp(beta)-1)`, the restricted positive partition sum is a sum of `exp(lambda B) q^k`, so its first and second derivatives are the conditional bond mean and variance. Since `d beta/d lambda = p`, the predicted bond center is `-p N u_i`, with the signs in the manuscript correct.

Conditional on spins, the bond count is exactly Binomial(`M,p`) with `M=-U`. The Hoeffding logarithmic moment bound gives uniform square-root-volume exponential moments for `D=B-pM`. Conditioning this nonnegative exponential on either contour event costs only its inverse probability, which is bounded. Cauchy–Schwarz then transfers the bond moment to the spin-energy moment. No independence between the contour event and the binomial noise is assumed or needed.

The final positive-mixture theorem legitimately applies on the Edwards–Sokal extension: the reweighting is a function of the spin energy alone, and its projection is exactly the physical spin marginal. This use of auxiliary bond labels does not replace the subsystem Hamiltonian with occupied-bond count.

## Other mathematical checks

- BKMS's real-temperature partition formula gives the macroscopic two-atom energy law by bounded-variable Laplace transforms. The one-sided conditional-transform argument correctly recovers weak Gaussian limits by tilting and then using convergence of total phase masses to exclude escape of mass. No complex-temperature continuation is needed.
- The independent-vertex-set argument bounds the unconditional variance uniformly throughout a real temperature interval. Passing the resulting strong convexity through the stable thermodynamic branches, then taking the one-sided limit at coexistence, correctly proves positive phase variances. It does not confuse the order-`N^2` coexistence variance with an individual phase variance.
- In the mean-field model the scalar stationarity equation has precisely the listed three relevant roots; the intermediate one is unstable. The Hessian determinants, Stirling prefactors, phase probabilities, ordered tangent gradient, and ordered energy variance agree with direct calculation. The disordered spin-energy weak limit is allowed to be degenerate when `a=0`; the earlier necessity theorem needs nondegeneracy in only one phase, so the extension to pure spins is valid.
- The global occupation bound follows from nondegenerate minima and compactness; the boundary strip's exponential rate gap absorbs the missing Stirling prefactor. Summing the resulting shifted lattice Gaussians gives the uniform positive-phase moment with zero exceptional component.
- The kinetic smoothing, interior Gaussian envelope, exponent `A+c` in the integrated occupation law, and Beta parameter `c+1` are correct. The zero-kinetic case is explicitly handled without a shape-zero Gamma or Beta law. Strict concavity of the normalized likelihood justifies the interval-CDF expression for continuous total variation.

## Presentation and remaining scope

The stage explains why necessity and sufficiency use different positive phase partitions, and it separates local weak limits from the stronger moment estimate. Those distinctions are scientifically material and handled well. The only required correction from this review is the local source-scope clarification above. I found no reason to restrict the short-range conclusion to two dimensions, to add kinetic variables to either microscopic threshold theorem, or to reinstate the isolated short-range sufficiency gap.
