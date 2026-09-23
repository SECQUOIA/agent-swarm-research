# Repository-to-manuscript coverage audit

The manuscript is [main.tex](main.tex), compiled as [main.pdf](main.pdf). This audit uses stable LaTeX labels, which identify results even if section numbers change during final review. Original research notes are retained as development records; this paper supplies the current reservoir claims and qualifications.

## Relevant source material

| Repository source | Precise manuscript coverage | Current status |
|---|---|---|
| research/reservoir-support-classification.md | sections/framework.tex: exact law, heat-capacity convention, energy/full-state TV identity (lem:energy-tv), normalization, centered and secant calibrations. sections/thresholds.tex: thm:three-support, prop:two-atoms, thm:two-scale-necessity. | Complete. Weak-support iff covers arbitrary tuning and cutoff; no density/moment assumption. Unequal-scale necessity needs one nondegenerate phase and positive phase probabilities. |
| research/three-phase-physical-bath.md | thm:three-support, applied with extensive energy scale. | Entire three-phase theorem is subsumed by the stronger weak-support theorem. The two-energy-atom exception is explicit. |
| research/phase-decomposition-reservoir-criterion.md | thm:positive-sufficiency, cor:two-phase-iff; eq:phase-exponential-moment and eq:exceptional-general-rate. | Complete. Positive mixtures and amplified exceptional mass are distinguished from signed partition errors. |
| research/finite-bath-physical-extension.md, sections 1–5 | sections/thresholds.tex, subsec:density-tails; prop:density-sufficiency; cor:density-physical-iff. sections/boundary-and-smooth.tex, prop:smooth-necessity. | Complete. Density-tail sufficiency remains explicit; necessity is strengthened to a good-point curvature proof using weak Gaussian phases. |
| research/potts-physical-bath.md | sections/microscopic.tex: thm:mf-bath, complete minima and Hessians, eq:mf-phase-weights, eq:mf-variances, lem:mf-exponential, continuous envelope, eq:mf-canonical-occupancy through eq:mf-tv-cdf. | Complete and strengthened. Pure-spin mean-field model already has sufficient ordered-phase nondegeneracy; kinetic variables are optional. Exact continuous Gamma/Beta benchmark remains included. |
| research/short-range-potts-route.md | Main thm:sr-bath; Appendix app:short-range-proof: primary contour inputs and conventions, eq:sr-conditional-clt, variance positivity, lem:sr-restricted-derivatives, lem:sr-energy-transfer. | Earlier isolated-copy sufficiency gap is resolved. Full iff holds for every fixed spatial dimension d>=2 and sufficiently large fixed q. The old two-dimensional necessity-only record is superseded. |
| research/shared-bath-phase-correlations.md | sections/shared-baths.tex: thm:shared-selection; prop:shared-one-bit; cor:shared-joint-threshold; lem:shared-temperature-shift; subsec:shared-microscopic. appendices/shared-extensions.tex: prop:shared-count; thm:shared-linear; prop:shared-linear-tv; prop:shared-linear-information. | Complete. Full microscopic entropy limits have a separate KL proof. Fixed-copy/count extension, balancing, covariance, marginal/joint TV, and linear-capacity information included. Positive variances are required where the linear-boundary formulas need them. |
| research/scouting-ensembles.md | Appendix sec:gaussian-geometry: prop:scalar-gaussian and eq:gaussian-untuned-odds. sections/boundary-and-smooth.tex: smooth extension and thm:physical-boundary-optimum. Appendix sec:capillarity-diagnostics: histogram and fixed-energy barriers. | Complete. Exact Gaussian crossover retained; physical arbitrary-calibration crossover now also proved. |
| research/multiphase-reservoir-geometry.md | Appendix sec:gaussian-geometry: exact weights, affine invariants, thm:gaussian-geometry, thm:gaussian-phase-loss, eq:anisotropic-effective-metric. | Complete and strengthened. The previous optimal-loss upper bound is now equality for arbitrary fields, including escaping centers. Anisotropic finite-N metric and semidefinite degeneracies are corrected. |
| research/finite-bath-physical-extension.md, sections 6–8 | thm:physical-boundary, cor:physical-compensation, thm:physical-boundary-optimum, eq:physical-interior-exact (exact secant gain, now in the main boundary section), subsec:boundary-applications; Appendix prop:capillarity-ldp and cor:square-capillarity. | Complete within stated models. Physical boundary permits degenerate Gaussian measures and has actual UI. All fixed gamma covered in mean field and spatial d>2; sufficiently large gamma in short-range d=2. Capillarity remains an explicit rate model. |
| research/broad-scout-1.md and verification/learned-potential-geometry-review.md | cor:physical-compensation, eq:compensated-tv, eq:physical-optimum-cdf and its convex optimizer. | Relevant compensation/within-phase-error diagnostic developed directly with physical composite energy. Generic Hamiltonian uncertainty machinery excluded; it is a different control problem. |
| research/reservoir-coexistence-manuscript.md | Entire LaTeX paper, including sections/introduction.tex, numerics.tex, conclusions.tex. | Superseded. Earlier caveats about short-range sufficiency and pure-spin necessity are updated in current status notes. |
| research/verification/potts_finite_bath.py, check_potts_finite_bath.py, and saved results | code/potts_finite_bath.py, code/check_potts_finite_bath.py, data/potts-finite-bath-results.json, fig:potts-scaling. | Standalone copy with adapted CLI/output only. Archival data preserved; N=300 and independent small checks rerun. Large enumeration is reproducible but was not unnecessarily repeated. |
| Relevant ensemble, physical-reservoir, geometry and shared-bath prior-art audits | Introduction relation-to-work subsection, manuscript references, stage-5-author.md, coordinator source audit. | Established mechanisms credited; source limitations and internal-review status distinguished from priority. Historical reviewer reports are retained unchanged. |

## Improvements completed during manuscript development

The manuscript does more than consolidate notes:

- It removes the kinetic-sector requirement from the mean-field reservoir threshold by using nondegeneracy in the ordered phase.
- It proves the short-range phase-energy exponential moment through a positive contour construction and a physical-energy transfer, resolving the isolated-copy sufficiency question.
- It proves exact optimal Gaussian phase loss for every calibration sequence; finite-center analysis alone was previously insufficient.
- It proves the physical boundary law with the exact integrability assumptions required by exponential tilting, its microscopic range of applicability, phase-population compensation, and optimization over all composite energies.
- It provides explicit normal-CDF evaluation and a scalar-root characterization of the unequal-variance boundary optimum.
- It proves smooth-bath necessity by a robust strong-concavity chord argument.
- It gives an exact physical midpoint-barrier identity and the corresponding sharp absolute-error scale.

These developments completed the prescribed internal author/reviewer cycles. All five author stages and two whole-paper review rounds are now closed, with every accepted major and minor issue corrected. WORKFLOW.md records the complete process and final verification; no external acceptance is implied.

## Resolved limitations and assumptions that remain part of the theorem

The two-phase necessary condition alone does not imply sufficiency for arbitrary weak phase limits. The positive moment and exceptional-mass bounds are substantive assumptions, verified for the stated microscopic models. The short-range theorem requires sufficiently large fixed q and additive equilibrium coupling to the bath.

In spatial dimension two, all-gamma boundary behavior does not follow from the proved small exponential-moment window and surface bound. The manuscript therefore gives the explicit sufficient range, without claiming a microscopic small-gamma morphology.

The capillarity LDP and square-torus branches are specified models. At tied rate minima, subexponential factors can change limiting weights while preserving the rate; tie weights are not identifiable from that input. The exact Gaussian geometry is also a stated model, with common isotropic within-phase covariance for its scalar exponent classification. The anisotropic remark uses the correct effective metric and makes no unsupported classification for arbitrary matrix sequences.

The barrier statements concern ratios at specified energies. They neither locate moving stationary points nor infer a dynamical rate. Full microscopic mutual information uses explicit KL bounds, not continuity from TV on growing spaces.

## Deliberate exclusions

These separate repository directions do not supply a needed result for this reservoir paper:

- survival-conditioned thermodynamic integration;
- interfacial-response inverse problems;
- reactive capacity and finite-field nucleation response;
- confined channels and diffusion certificates;
- stabilized saddle and finite-record kinetics;
- generic multicomponent droplet stability and common-reservoir Schur complements;
- learned-potential fitting or uncertainty mixtures unrelated to physical reservoir calibration.

Their notes, negative results, and historical reviews remain in the repository. Excluding them does not remove a proof needed by the present manuscript.
