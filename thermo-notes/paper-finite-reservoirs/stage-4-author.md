# Stage 4 author handoff

Status: complete author draft, awaiting the five independent reviewers required by the workflow. No claim of independent acceptance is made here.

## Files and coverage

Added and integrated:

- sections/gaussian-geometry.tex: exact scalar Gaussian reweighting; necessary and sufficient calibrated scale; balanced and optimized finite crossover; specified untuned canonical-mean calibration; arbitrary finite multivariate phase geometry; affine invariants; sphere versus nonsphere classification; exact optimized phase loss; correct finite-N anisotropic effective metric.
- sections/boundary-and-smooth.tex: smooth curvature necessity and the already proved density converse; physical finite-capacity boundary under explicit positive-phase integrability and exceptional-mass conditions; finite calibration corrections; direct physical phase-population compensation; optimization over every admissible composite energy; computable convex normal-CDF objective and its scalar root; microscopic mean-field and short-range applicability.
- sections/capillarity-diagnostics.tex: exact physical interior gain and cubic correction; surface-cost dimensional comparison; explicit compact-support capillarity LDP and normalized variational law; square-torus rate minimizers; histogram L2 versus TV; exact physical fixed-midpoint barrier lowering and separate absolute/relative accuracy scales.
- code/check_stage4.py: quadrature checks of the CDF objective, optimizer, actual power-law compensation, and square-model inequalities.

main.tex integrates these sections. refs.bib adds two verified primary references. Stages 1–3 mathematical files were not edited.

Coverage against repository notes:

| Original material | Treatment |
|---|---|
| research/scouting-ensembles.md | All scalar exact Gaussian, crossover, tuning, smooth-bath, histogram, and barrier developments included. The physical optimized crossover is now proved too. |
| research/multiphase-reservoir-geometry.md | Three-scalar-phase classification is subsumed by the general theorem; three-point missing-outer-phase formula stated. Multivariate classification and anisotropic observations included with corrections. Original open optimal-loss equality completed. |
| research/finite-bath-physical-extension.md, sections 3 and 6–8 | Smooth sufficiency cross-referenced to Stage 1, with simpler weak-limit necessity. Boundary law strengthened to positive phase mixtures and microscopic models. Capillarity model and square-torus minimizers proved with explicit scope. |
| research/broad-scout-1.md and independent review | Compensation versus fluctuation diagnostic derived directly for the physical reservoir. Generic learned-Hamiltonian fitting, descriptor geometry, and uncertainty ensembles excluded because they change the Hamiltonian rather than the reservoir and add no required reservoir proof. Their established mechanisms are not claimed as new. |

## Developments beyond transcription

1. **Exact multivariate optimal phase loss.** Old notes supplied an upper bound without equality in general. The proof now covers arbitrary fields, including unbounded fields and diverging sphere centers. Fields bounded away from zero push surviving phases beyond a supporting hyperplane, giving TV one. Fields tending to zero preserve macroscopic phase locations; the positive limiting weight support solves approximate finite nearest-sphere equations. Farkas' lemma converts approximate feasibility into finite-center feasibility, supplying the missing lower bound. The parent independently developed and checked this proof in reviews/stage-4-coordinator-investigation.md.

2. **Weak-limit physical boundary theorem.** Exact secant derivatives, a phasewise concavity tangent bound, and an exponential moment strictly beyond the required tilt give actual uniform integrability. Full microscopic TV follows from the exact likelihood expectation, not a false TV Gaussian approximation. Variance-zero phases are included as Gaussian probability measures. Moment bounds need hold only for sufficiently large N; this matters for Gamma sectors at large fixed tilt.

3. **Optimization over all composite energies.** Positive overlap with both target phases forces any calibration beating abandonment to lie within order sqrt(N) of the secant energy. The exact two-good-point likelihood identity proves compactness. Finite corrections have the derived boundary limit; phase-centered calibrations attain abandonment. The complete optimum is a one-dimensional convex minimization or abandonment. Both positive variances give a unique scalar root; equal variances simplify the result even for unequal weights.

4. **Physical phase-population compensation.** An explicit order-sqrt(N) composite-energy correction offsets unequal integrated fluctuation factors without changing local tilt slopes. Original phase weights are restored asymptotically while phase fluctuations retain the stated TV error. The sign and coefficient were independently checked by the parent.

5. **Microscopic boundary applications.** Mean-field Gaussian occupation bounds and Gamma transforms give all fixed standardized moments for sufficiently large N. In short-range dimension d>2, every fixed displacement at scale 1/sqrt(N) eventually fits the Stage 2 cutoff-free 1/L window. Its derivative and center bounds give every fixed moment, transferred to actual spin energy by the established conditional binomial estimate. The surface exceptional cost dominates bath gain. In dimension two, only sufficiently large fixed gamma is justified, with both sufficient inequalities explicit.

6. **Smooth curvature necessity.** Strong concavity at three good likelihood points inside the phase interval gives necessity from weak Gaussian phase limits. This avoids differentiating likelihood limits and handles a convex feasible cutoff interval.

7. **Exact physical barrier diagnostic.** The midpoint gain is exactly c log cosh(beta Delta/(2c)). Vanishing absolute error is equivalent to c much larger than Delta squared without first assuming a quadratic approximation. Peak relocation and dynamic rates are not inferred.

## Corrections and scope

- The old semidefinite-cylinder remark was too broad. The metric is B(I+NB)^(-1), with a transformed field. A linear nullspace component can produce a paraboloid with possible flat directions; a positive-radius cylinder requires the linear coefficient in the positive-rank singular metric range. Zero radius gives an affine subspace, while rank zero gives a hyperplane, the whole space, or an empty locus according to the linear coefficient and level constant.
- Exact Gaussian models do not replace microscopic interfacial tails.
- Gaussian density subscripts consistently denote variance.
- Generic smooth-bath converse assumes endpoint calibration exists; varying composite energy need not achieve it for arbitrary entropy.
- Boundary exponential moments must extend beyond the required tilt, and reweighted exceptional mass must vanish.
- Pure-spin mean-field disordered variance is zero. Measure-form boundary formulas cover it; positive-density formulas are qualified.
- Two-dimensional short-range boundary claims apply to sufficiently large gamma, with no claim about microscopic small-gamma morphology.
- Capillarity is an explicitly assumed compact-support rate model. Isotropic square-torus branches are prescribed, not a lattice Potts Wulff theorem.
- At a capillarity tie, subexponential factors preserve the rate and change weights or select a minimum. Leading rates therefore cannot identify tied weights; this is a resolved nonidentifiability statement.
- Endpoint-minimizing LDPs do not establish phase-local TV.
- Histogram norms and specified-energy barriers are distinct diagnostics. No dynamics theorem is claimed.

## Source verification

No new literature theorem is assumed beyond accepted Stage 2 primary inputs. Established mechanisms are cited narrowly; priority synthesis remains Stage 5.

- Challa and Hetherington, Gaussian Ensemble as an Interpolating Ensemble, Physical Review Letters 60, 77–80 (1988), DOI 10.1103/PhysRevLett.60.77. Primary full text retained at research/sources/challa-hetherington-1988-interpolating.pdf and .txt; first-page metadata checked. Added key ChallaHetherington1988PRL.
- Challa, Landau and Binder, Finite-Size Effects at Temperature-Driven First-Order Transitions, Physical Review B 34, 1841–1852 (1986), DOI 10.1103/PhysRevB.34.1841. Primary publisher page and abstract inspected 2026-09-07: https://journals.aps.org/prb/abstract/10.1103/PhysRevB.34.1841 . The abstract explicitly describes weighted Gaussian energy peaks. Added key ChallaLandauBinder1986.
- Stage 2 Borgs–Kotecky–Miracle-Sole, Borgs–Chayes–Tetali, and Borgs–Chayes–Helmuth–Perkins–Tetali inputs are reused through precise manuscript references. The new moment deduction uses only the previously proved finite-window derivative estimates.
- Consulted prior-art and review records include ensemble-prior-art.md, physical-reservoir-novelty-audit.md, multiphase-reservoir-review.md, and learned-potential-geometry-review.md. They do not establish priority for broad Gaussian-ensemble, response, or compensation mechanisms; no such claim is made.

## Validation

- python code/check_stage4.py passes. Three weighted-normal examples compare the CDF objective to independent absolute-density quadrature (approximately 1e-10 agreement); the equal-variance optimizer matches the target weight. Actual power-law quadrature with unequal variances converges to the compensation weights and TV as N increases. A fine grid also checks the square-model lower inequality. These checks supplement, not replace, the proofs.
- latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex succeeds. Draft: 39 pages before Stage 5 synthesis. Final log has no undefined references, citation warnings, overfull boxes, or bookmark warnings.
- Parent independently checked phase-loss proof, physical optimization, compensation, moment extension, capillarity minimizers and barrier identity. The five formal independent reviewers remain required.

No known unresolved author issue remains in the stated claims. Unsupported breadth was excluded or converted into a precise limitation.
