# Stage 2 author report

Scope: `sections/01-foundations.tex`, `sections/02-quadratic-finite.tex`, and their bibliography. This is the completed author pass for the current five-reviewer process. It does not constitute that review gate.

## Changes

1. Added a short proof roadmap before the quadratic-system law and an ordinary-subspace explanation of noncommutative rank. These identify the established algebraic input and the paper's contact-volume/precision-allocation connection before the technical proofs.
2. Made the square comparison with Beach, Hildebrand and Huchette (2022) precise. Their Proposition 1 represents the dyadic interpolant, whose graph alone does not retain the square graph. The displayed band `F_p-e_p <= w <= F_p` supplies graph containment with unchanged bit count, linear size, and error. The optimality claim concerns the new lower comparison against arbitrary convex integer lifts.
3. Added direct attribution of the dyadic folding identity to Yarotsky (2017), Proposition 2, and retained the later MIP/epigraph citations. Added its bibliography entry with the source-version locator.
4. Replaced the equal-coordinate Hessian argument for a product by a diagonal-congruence factorization valid at every positive point. The former illustrative argument did not cover positive boxes avoiding the equal-coordinate line. The new argument verifies the claimed coefficient on every positive full-dimensional compact box, without expanding the main theorem.
5. Updated Nicola's citation from the 2008 preprint to its published 2010 article, with precise printed pages 208–209. Added a sentence explaining how the established affine-fiber geometry supports the paper's polyhedral-cover count.
6. Explained the two roles of the finite covariance matrix and the relation between determinant loss and binary count. Added a short transition explaining why constant log-determinant accuracy suffices and how optimization, exact feasibility repair, and rational near-diagonalization fit together.

No theorem label, substantial result, main constant, hypothesis, or model restriction was removed. No new global priority claim was added.

## Complete proof audit

I read all 2,816 original lines of the two assigned files, including proofs, examples, unnumbered estimates and algorithm details. I reconstructed the following arguments rather than treating previous acceptance or finite tests as proof.

- Representation model: convexity under projection, witness averaging, nonmeasurable initial contacts and compact closures, integer parity versus binary sections, affine invariances, and finite disjunction including a common recession cone.
- Basic geometry/constructions: strong-curvature diameter and isodiametric constants; Taylor bands; exact binary products; residual McCormick and square errors; prefix endpoints/empty depths; exact square threshold; product area/width constants and four-point obstruction; fractional-cover LP and rational rounded demands.
- Scalar quadratics and one-sided lifts: maximal-simplex indefinite volume, principal minor existence, normalization and determinant constants; folding epigraph maximization; negative/positive inertia slices; exact product one-sided optimum; projected-facet face count. Dropping the square lower bound for hypographs does not drop input or binary-product bounds.
- Noncommutative rank: principal Hermitian compression over the free skew field, real descent of a maximizing shrunk subspace, orthogonal projection dimension identity, symmetric zero blocks and precision allocation. Recomputed covariance fourth moments, whitening volume bound, capacity determinant inequality and finite constants, alternative Hall/permanent proof, cross-product Hessians and SOS certificate.
- Smooth results: mixed-Hessian integration-by-parts kernel bound and Schur estimate, tensor evaluation, phase control on arbitrary compact contacts, principal slicing, global Taylor allocation, and polynomial bit-product expansion. The degree bound and real-coefficient scope remain explicit. Verified the rank-three polynomial example and PIT reduction. The positive-product example received the local repair above.
- Constant-rank and perspective results: partial Legendre transformation, Schur-complement zero Hessian, affine gradient fibers, transverse tubes in original coordinates, chart compactness at boundary points, and full-tube Taylor error. Verified positive perspective homogenization and exact binary-times-t encoding; no arbitrary-integer upper transfer is used.
- Finite covariance theory: feasible compact set/positive determinant, cap and energy scaling of contact covariance, shared symmetric monomial error, grid count and size, domain-volume variant, norm comparison, geodesic energy expansion, determinant certificate, commuting sign symmetrization, scalar water-filling, and dimension-gap example.
- Rational rank construction: base-field shrunk subspace, rational nonorthonormal bases in orthogonal spaces, interval normalization, coefficient/depth growth, integral capacity scaling `D_H^(-2r)`, rational box width products, and uniform lower remainder. Finding a principal compression by deletion preserves nc-rank.
- Rational spectral and finite algorithm: exact rational Jacobi rotations and denominator growth, matrix-function perturbation bounds without eigenvalue gaps, positive log-energy gradients, exact homogeneous penalty, polynomial-radius optimal covariance, inexact subgradient recurrence, local metric rounding, branch and gradient precision, scalar repair, rational grid sandwich, PSD-order energy monotonicity and final determinant/count loss. The iteration count is a theoretical polynomial guarantee, not an empirical performance statement.
- Output bodies: grouped PSD fourth-moment sum and shared-error control, rational unfactored grouped gradient in the correct frame, zero-energy groups; PSD Grothendieck rounding, correlation separation/weak optimization and rational repair; effective nonlinear output image, exact minima equivalence, oracle pullback/radii, symmetric ellipsoid rounding and dimensional loss.
- Input quotient: affine subtraction along fibers, rational common-kernel factorization, zonotope strong separator, rational LDL near-spherical map, contained cube and volume loss, exact original-domain lift. The active input rank remains distinct from nc-rank.
- PSD structure: unconditional domination, logdet allocation hypograph with explicit interior/outer balls, exact tangent separators and central-ball repair; block traces/determinants and shared grids; quotienting independent blocks; diagonal constants and scalar inexact solver; integer-feature minor volume and common kernel; exact forest volume, thin-domain obstruction and coefficient qualifications.
- Hardness: Max-Cut cube maximum/zero-count equivalence; exponential incompatible parity packing across polynomially many disjoint blocks; tolerance normalization; positive-optimum one-bit square appendage; polynomial replication for every fixed sublinear power. No claim is made about optimizing the generated formulation, recognizing general arbitrary convex lifts in coNP, or excluding every sublinear additive function.

I found no unresolved dependency or mathematical gap in the audited theorem proofs. The product illustration's limited proof domain is repaired. Rank-changing singularities, general varying vector null spaces, exact product constants, and stronger approximation-hardness thresholds are explicitly delimited research boundaries, not assumptions used to establish a claimed theorem.

## Source audit and priority scope

See `stage2-literature.md` and `stage2-retrievals.json` for versions, passages and retrieval evidence. Main algorithmic imports were independently reread in text freshly extracted from the cached original PDFs. The Nicola published original, Volcic v2 and Yarotsky v3 were additionally retrieved during this pass. The original Hörmander URL failed; Wolff's checked complete theorem and proof supply the same analytic estimate, whose local proof is also included in the manuscript.

Targeted online searches did not identify a prior statement of the paper's exact quadratic graph-count coefficient. This is limited search evidence, not proof of absence. Screened recent adjacent works concern MIQO optimization/convexification or algebraic determinant degree. Their stated models do not replace the arbitrary-lift graph-containment comparison. The introduction's existing qualified novelty statement is therefore preserved, with no stronger claim added.

## Validation

- Symbolic Hessian factorization and determinant identity checked for products in dimensions 2–7 using SymPy 1.14.0; results are in `stage2-focused-checks.json`. The proof for every dimension follows from the displayed diagonal congruence, not from these finite instances.
- `python verification/check_manuscript.py`: no duplicate labels, unresolved references, duplicate bibliography keys or unresolved citations; output in `stage2-reference-check.json`.
- Standard `latexmk` PDF build passed; output in `stage2-build.log`. The full manuscript has 87 pages at this author pass.
- I did not rerun all 45 baseline scripts: root's unchanged-core baseline already passed. No executable formulation algorithm was modified, and the only changed mathematical derivation received the focused symbolic check above.

## Integration notes for stage 4

No required abstract/introduction/theorem scope correction was identified. If the final references discussion mentions the square construction, preserve the distinction between a PWL interpolant and a graph-containing band, as now made explicit locally. Nicola now cites the 2010 published article despite the preserved key `nicola2008`. Author metadata, overall length/structure and whole-manuscript readability remain for the prescribed integration and complete review stages.
