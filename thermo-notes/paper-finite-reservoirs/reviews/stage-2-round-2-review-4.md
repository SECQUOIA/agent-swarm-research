# Stage 2, round 2 — independent review 4

## Verdict

**No major or minor issues identified in the revised stage.** The contour-convention problem has been resolved by consistently using the original BCT construction. The expanded matching-label and stable-pressure arguments justify the needed estimates without identifying different finite-volume contour models.

I independently read the full revised `sections/microscopic.tex`, checked its theorem dependencies, and compared the revised source claims against the primary text of BCT 2012 and BKMS 1991. I did not read any other round-2 report, edit the manuscript, or delegate.

## Revised short-range argument

### Original contour convention

The manuscript now reproduces BCT Definition 4.4 correctly: a compatible interface selects the exterior when available; otherwise component size and a fixed tie rule do so. The events are the original BCT events (6.1)–(6.5). The later BCHPT convention is explicitly distinguished and no estimate is imported by asserting equality of its finite-volume phase events. The same original convention is used for contour geometry, activities, cutoffs, and limiting free energies.

### Matching-label derivatives

I checked the explicit summand against BCT equations (6.13)–(6.14). The vertex-count terms, contour-size term, ordered-component factor, and constant removal of one ordered color multiplicity are correct. Their geometry and indexing are independent of inverse temperature.

The bound on total internal contour size is sufficient and valid. A lattice edge can have only a bounded number of intersections with the compatible internal contours in the half-unit-cube construction. An edge meeting the interior either has an interior endpoint or crosses the bounding contour; thus the number of such edges is bounded by a constant times the interior vertex count plus the bounding contour size. This argument also covers an interior that wraps around the torus. Consequently, the first summand derivative is bounded by this effective volume, and the second log derivative of a positive sum is bounded by the volume plus its square. BCT Lemma 5.7 gives effective volume of order at most the contour size squared. The activity derivative bounds stated in the manuscript follow.

### Cluster differentiation and cutoff removal

BCT estimates (A.5)–(A.6) allow positive exponential slack for sufficiently large fixed `q`. That slack absorbs the degree-two and degree-four factors arising from first and second cluster derivatives. The first derivative of a minimum of the two smooth positive activity branches is used only almost everywhere. Integrating the majorized first derivatives establishes uniform Lipschitz free energies without differentiating a cutoff twice.

The activity cutoff is the original BCT cap with decay exponent `beta/8-beta/20+1`. After the Lipschitz estimate, BCT Lemma A.1(i) removes all torus cutoffs on a common interval of width proportional to `1/L`. Only then does the proof differentiate the smooth original activities twice. There is no circular use of a second derivative to prove the Lipschitz estimate or to establish cutoff inactivity.

### Stable sides and pressure identification

I checked BCT Lemma A.3 directly. Its two implications identify positive spontaneous magnetization with zero ordered excess free energy under the Appendix A hypotheses. Below coexistence this makes the disordered branch minimizing; above coexistence it makes the ordered branch minimizing. Continuity gives equality at coexistence.

The revised physical-pressure identification also holds in the original construction. BCT Lemma A.1(ii) gives a full-torus upper bound by the minimum truncated free energy, and (A.9) gives the matching lower bound in a minimizing phase. The derivation of (6.26)–(6.27) for interface networks uses the contour/interior bounds and large-`q` counting, not the separate assertion that the ordered phase minimizes. Its stated extra inequality on `q` holds in a sufficiently small fixed neighborhood of coexistence, using the source's `beta_c=(log q)/d+O(q^{-1/d})`. This identifies the limiting random-cluster pressure on both sides. The normalization shift `d beta` and the stable-side identity with `psi_i` have the correct signs.

### Physical spin-energy moment

The finite difference on the stable side stays within the cutoff-free interval because `1/sqrt(N) <= 1/L` for fixed `d>=2`. Its error gives a center discrepancy of order `sqrt(N)`, sufficient for a fixed standardized exponential moment. The corrected text now explicitly differentiates the logarithm of the fugacity partition function. Its first and second fugacity derivatives are indeed conditional bond-count mean and variance.

Conditional on spins, the occupied bond count is binomial with number of trials equal to the monochromatic-bond count. The standardized centered noise estimate remains bounded after conditioning on either positive-probability contour phase. Cauchy–Schwarz transfers the bond moment to the actual spin energy without assuming independence after phase conditioning. Finally, the tunneling decay beats the maximal reservoir amplification also in dimension two. The exact spin-energy likelihood projects from the joint spin–bond measure to the claimed physical subsystem law.

### Necessity

The real-temperature partition ratios, one-sided phase transforms, exponential tilting, and restoration of total mass give the two conditional weak Gaussian energy limits. The independent-vertex-set variance bound passes through the stable thermodynamic branches to give strictly positive phase variances. This verifies the hypotheses of the earlier two-scale necessity theorem and does not confuse the total coexistence variance with the phase variances.

## Mean-field and finite-system regression review

I rechecked the complete minimum classification, the two Hessians, the prefactors producing the phase weights, and the ordered energy variance. The pure-spin ordered phase still provides the one nondegenerate `sqrt(N)` fluctuation law required by the necessity theorem. The global occupation estimate and positive Voronoi decomposition still provide sufficiency without an exceptional component or kinetic smoothing.

The Gamma convolution and interior envelope remain consistent. The finite-system occupation exponent is `A+c_N`; the Beta parameters are `A,c_N+1`. The discrete `a=0` case is handled separately. The Gamma/Beta CDFs respect infeasible occupation states and support-exterior interval endpoints. The strictly concave normalized log likelihood gives the correct positive-difference interval used for total variation. No changes have invalidated the independent round-1 direct-quadrature check of these formulas, so I did not duplicate that numerical calculation.

## Scope

The revised stage establishes the two stated microscopic reservoir thresholds under the written fixed-parameter and sufficiently-large-`q` hypotheses. This is an assessment of the mathematical argument and the inspected source inputs, not a certification of bibliographic priority.
