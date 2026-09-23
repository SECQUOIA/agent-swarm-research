# Stage 2, round 1: independent review 5

**Verdict: no major issues identified; correct the three minor issues below.**

I reviewed `sections/microscopic.tex`, `main.tex`, `refs.bib`, and the Stage 1 theorem dependencies. I did not consult other current reviews, delegate, or edit the manuscript. The proposed short-range sufficiency argument survives my independent mathematical and source checks. In particular, I did not find a circular use of smoothness of the truncated free energies.

## Minor issues

### 1. Derivatives of the logarithm are required

**Location:** `sections/microscopic.tex`, lines 647–651, proof of the bond-to-spin transfer lemma.

The text introduces the partition function `exp(d beta N) Z_{i,L}` and then says its first and second derivatives in the fugacity parameter are the conditional mean and variance of the bond count. These are derivatives of its **logarithm**. The subsequent argument uses log partition ratios correctly, so this is a local wording error rather than a gap in the theorem.

**Fix:** Say explicitly that the first and second derivatives of `F_{i,L} = log[exp(d beta N) Z_{i,L}]` with respect to `lambda` are the mean and variance.

### 2. Qualify the cited random-cluster interpretation for contour interiors

**Location:** `sections/microscopic.tex`, lines 538–547, especially the sentence referring to Section 3.8 of Borgs–Chayes–Helmuth–Perkins–Tetali.

That source explicitly says at the beginning of Section 3.8 that general contour partition functions do not coincide with ordinary random-cluster partition functions because interfaces are excluded. Its explicit identities are then supplied for suitable interiors embedded in the infinite lattice, with simply connected sets in Proposition 3.14. The manuscript's phrase “the exact random-cluster interpretations are given” can be read as attributing the general torus-interior assertion to this proposition.

The derivative bounds nevertheless have a direct, sufficient justification from the positive matching-label sums (6.13)–(6.14) in Borgs–Chayes–Tetali, which the manuscript already cites. Each term has a logarithm consisting of the two volume terms, the total contour-size term, and a beta-independent power of `q`; its first two derivatives have the required geometric bounds. This route does not need every interior to admit an unrestricted infinite-lattice random-cluster interpretation.

**Fix:** Make the matching-label representation the general justification. Qualify the Section 3.8 reference as an additional exact interpretation for the specified embeddable interiors, or remove that reference from this proof. Retain the explicit geometric explanation that the total number of local contour elements in a configuration is bounded by a constant times the interior volume plus boundary size.

### 3. Add a short geometric explanation of the positive phase events

**Location:** the paragraphs introducing `O_L`, `D_L`, and `T_L` before the positive contour decomposition.

The source locations are accurate, but the manuscript currently supplies almost no description of what the positive events mean. A theoretical-thermodynamics reader can follow the subsequent energy-transfer argument more easily if the geometric labels are explained before the polymer formulas.

**Fix:** Add a compact explanation that the contour construction assigns ordered or disordered labels to regions separated by boundaries of the occupied-bond geometry, that the phase event is determined by the exterior label when there are no interfaces, and that the tunneling event consists of configurations with interfaces. State that exact geometric definitions and compatibility conventions are those of the cited construction. No reproduction of the complete contour machinery is needed.

## Independent mathematical verification

### Mean-field model

- Recomputed the stationary equation, the classification of its relevant roots, both Hessian determinants, the phase prefactor ratio, and the ordered spin-energy variance. They agree with the manuscript.
- The boundary argument excludes boundary minima. Strict concavity of `log x - b x` limits the stationary coordinate values to two. The exchange direction excludes configurations with two equal large coordinates. The one-dimensional stationarity equation has at most three roots by the stated derivative count, and the listed roots exhaust them.
- The global quadratic rate lower bound follows from isolated nondegenerate minima on a compact simplex. The boundary-strip rate gap absorbs the missing Stirling factor, giving the stated lattice-Gaussian upper bound. This provides both the Laplace-sum tail justification and the conditional energy exponential moment.
- The no-momenta extension is valid: only one phase needs a nondegenerate weak fluctuation limit for the Stage 1 necessity result. The ordered phase has it. The degenerate disordered spin-energy limit does not undermine the positive-phase sufficiency theorem.
- The Gamma convolution, bounded-interval logarithmic-curvature estimate, and lattice sum yield the stated continuous local density limits and interior density envelope for fixed positive `a`. The upper bound on the relevant kinetic energy is of order `N`; its mode may be included by enlarging that fixed bound, preserving the curvature argument.
- Direct integration yields occupation exponent `A+c_N` and conditional Beta parameters `(A,c_N+1)`. The finite-sum CDFs and the positive-likelihood interval formula for total variation are correct. The pure-spin case is handled separately and never invokes a Gamma distribution of zero shape.

### Weak short-range energy limits

- The real-temperature expansion from Borgs–Kotecký–Miracle-Solé, applied first at shifts of order `1/N`, gives the stated two-atom macroscopic energy law.
- At a one-sided shift of order `1/sqrt(N)`, the appropriate stable branch dominates and the opposite midpoint event contributes an exponentially vanishing term. The normalized tilt has moment-generating functions converging on a neighborhood of zero. Undoing the tilt against compactly supported functions gives vague convergence; convergence of the known total phase masses then gives weak convergence. This establishes the conditional Gaussian limits without analyticity at complex temperature and without converting a signed partition remainder into a positive phase measure.
- The independent-set variance argument is correct. Conditional on exterior spins, site contributions have uniformly positive variance when `q>2d`; the independent-set density gives the displayed constant. Passing strong convexity to the thermodynamic limit on each stable side, then using continuity at coexistence, proves positivity of the two branch variances. It does not confuse total coexistence variance with within-phase variance.

### New short-range sufficiency argument

The proof has the following noncircular order:

1. Positive finite interior sums and the geometric volume bound imply polynomial bounds on activity derivatives, without phase stability assumptions.
2. Uniform convergence of the *truncated* polymer expansion, with spare exponential decay, absorbs those polynomial factors. First derivatives of the minimum are needed only almost everywhere, giving uniformly Lipschitz finite-volume free energies and therefore Lipschitz limiting truncated free energies.
3. The phase free-energy difference is zero at coexistence and thus of order the temperature displacement. The published inactive-cutoff criterion, together with contour diameter at most `L`, removes all finite-torus cutoffs in a window of width proportional to `1/L`.
4. Only after this removal does the proof differentiate twice. The original activities are smooth, and the exponential cluster majorant absorbs the fourth-degree cluster-size factor, giving a second log-partition derivative of order `N`.
5. Stable-side finite differences at displacement of order `1/sqrt(N)` identify the restricted first derivative to error `O(sqrt(N))`. This displacement lies in the cutoff-free window for every fixed dimension at least two. The finite-volume exponential error remains negligible after division by this displacement.
6. Log partition ratios in the bond fugacity give the conditional exponential bond-count moment. The Edwards–Sokal conditional binomial fluctuation estimate remains bounded after conditioning on a phase event of probability bounded below. Cauchy–Schwarz therefore transfers the moment to the actual spin Hamiltonian.
7. The positive tunneling mass decays as `exp[-b L^(d-1)]`. At `c_N >> N^(3/2)`, the bath amplification exponent is `o(L^(d/2))`. Since `d-1 >= d/2`, the exceptional contribution vanishes, including in dimension two.

All these scale comparisons and signs check out. The use of two different positive phase partitions is legitimate because the necessity and sufficiency theorems do not require the same partition. The final projection of the energy-only reweighted joint spin–bond law is exactly the physical spin marginal.

## Primary-source checks performed

- **Borgs–Kotecký–Miracle-Solé (1991):** equation (6), equation (8), and Theorem 1. Checked the Hamiltonian normalization, fixed-real-temperature expansion, differentiability, stable-side identification, and positive latent heat.
- **Borgs–Chayes–Tetali (2012):** Lemma 5.7; equations (6.13)–(6.22); Lemma 6.1; Appendix A assumptions; equations (A.3)–(A.8); Lemma A.1; and the phase identification discussion in Appendix A.4. Checked the diameter and interior-volume bounds, positive partition representations, exact minimum cutoff, inactive-cutoff criterion, finite-volume approximation, and tunneling suppression.
- **Borgs–Chayes–Helmuth–Perkins–Tetali (2022 preprint):** equations (44)–(46), polymer discussion and Lemma 3.13, Section 3.8 and Proposition 3.14, Lemma 4.1, and Appendix B.1. Checked the phase multiplicity, finite embedding bounds, the scope qualification described in minor issue 2, and applicability on the disordered side.

I used the local primary-source texts, whose content was available, and did not perform additional web searches or numerical calculations. The mathematical findings above do not rely on declarations in previous repository notes. Future planned manuscript sections are outside this verdict.
