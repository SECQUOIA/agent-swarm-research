# Whole-paper round 1 — reviewer 02

Major findings: 0

Minor findings: 0

No correction request or unresolved mathematical question arose from this review. This is a bounded mathematical assessment, not formal certification, an exhaustive priority search, or a prediction of publication acceptance.

## Scope and snapshot

I read `WHOLE-TASK.md`, `WHOLE-LENSES.md`, `PROCESS.md`, `reviews/PROTOCOL.md`, and `literature/AGENTS.md`. I reread the complete manuscript source: abstract, introduction, all of sections 01–04, conclusion, main file, macros, bibliography, and coverage inventory. The review covers the entire 84-page manuscript, with additional depth on scalar quadratic rank, bilinear fractional covers, one-sided inertia, noncommutative rank, symmetric shrinking, and joint versus scalar rank. Earlier acceptance was not used as a proof.

All eleven snapshot hashes matched at the initial check and again after the mathematical review. The reviewed hashes are:

| File | SHA-256 |
| --- | --- |
| `abstract.tex` | `db2b95f525fdfc786c9c24b46f41693892131a8103f249d27dbc012d53e323a3` |
| `coverage.md` | `15093feb82f388506c4bf33a9596ee98f90df4fa0510d6b6ac6e71b7ea106fe9` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `ce1ba15da86b633469c308369f30e3e431340859986b36b5b2c46cc3f0bd59c5` |
| `references.bib` | `60fd73a2eec8fd2bc999cf2c407c6a571c590b087786c78647cc1bb7a59a1693` |
| `sections/00-introduction.tex` | `6940bf7c1017d82a8ea00af76575aa88da76f2ef26290b4b3872fd0bba152b16` |
| `sections/01-foundations.tex` | `3108dc02b31b4812fe7fffb444e637a2c846e00268d750262e363dfdb1ded37e` |
| `sections/02-quadratic-finite.tex` | `0a81bba6f3635323663fb347f74face34c2aadb2ba0993b8a1d6465e9f8fdbd3` |
| `sections/03-scalar-nonlinear.tex` | `8e271531b4c705a1333b49f170b20e987359ed5e7d1b05866030bccb69040803` |
| `sections/04-vector.tex` | `d9369569aa0711c3652dcf28929ea4be5884c534f18e371038fbdfc7edb6252d` |
| `sections/05-conclusion.tex` | `2bfb1f16aaa317e5b49dd171ccd9648c7a320343f23ec13acbf6a38b1955ad6e` |

## Full-paper assessment

The manuscript supplies the proof chain needed for its main synthesis. It keeps the minimum over arbitrary convex integer lifts separate from binary linear dimension and from the rational constructive count. The abstract and introduction do not promote fixed-data asymptotics into uniform bit bounds, or count guarantees into claims of easy optimization. The conclusion correctly leaves rank-changing smooth maps, general mixed-coordinate vector constructions, and the one-input convex-box constant-gap question unresolved.

The topology underlying the lower bounds is sound. A parity class is formed from all exact-graph witnesses, and only its visible support is closed. Continuity and the closed error body extend the midpoint inequality to that compact support. This does not require closing the original lift or selecting measurable witnesses. The compact supports cover the domain and therefore support the volume arguments. Residue arguments later in the paper use actual finite witness combinations; they do not impose a hidden bound on integer values.

### Quadratic asymptotics: detailed reconstruction

1. **Scalar rank and products (`thm:scalar-rank`, `thm:graph-cover`).** The maximal-simplex proof controls an indefinite quadratic form through its determinant, rather than through a false definite-curvature diameter bound. An invertible principal restriction of order equal to scalar rank supplies the full-dimensional lower-bound slice. Diagonalizing and normalizing the nonzero square coordinates gives the matching upper coefficient. For bilinear interaction graphs, the contact projection-width constraints yield the fractional-cover LP, and sharing coordinate prefixes implements the matching precision allocation. The constants 20 and 4, nonnegative truncated demands, ceilings, isolated vertices, and rational preprocessing have the stated roles. The product's finite constants do not claim a sharp optimum beyond what is proved.

2. **One-sided inertia (`thm:inertia`).** A negative eigenspace slice gives the epigraph lower bound with coefficient half the negative inertia. The upper construction assigns integer precision only to the concave square terms. Continuous folded epigraph descriptions handle the positive square terms; the positive-weight objective forces the fold variables in the required direction. Negation transfers the result to hypographs. The proof retains the complete epigraph or hypograph, including its unbounded output direction. Zero negative inertia gives zero integers at positive accuracy without claiming an exact polyhedral representation of every convex quadratic epigraph. The product's one-sided convex count and the qualification about the linear model are consistent.

3. **Principal compression and real shrinking (`sec:ncrank`).** Hermitian elimination over the free skew field uses an invertible diagonal pivot or an invertible two-by-two off-diagonal pivot, followed by the Schur complement. This produces an invertible principal submatrix of the required order; multiplication order is respected. The deficiency function is supermodular, and sums with conjugate subspaces yield a real maximizing subspace. With the resulting image space, the orthogonal intersections used for the shrinking decomposition have the required dimension difference. Symmetry forces each Hessian to map the zero-precision subspace into the full-precision subspace. The exponents 0, 1, and 1/2 therefore satisfy the required pairwise precision condition, and their sum is exactly half the nc-rank.

4. **Covariance, capacity, and volume (`lem:covariance`, `thm:ncrank`).** I reconstructed the fourth-moment expansion, including the nonnegative mean-square term that cannot be discarded with the wrong sign. Whitening and the second-moment ball inequality give the stated volume estimate. Positive capacity of the full-rank principal compression supplies an energy/determinant lower bound; combining it with the parity cover gives the claimed exponent. The alternative permanent argument uses the absence of a shrunk subspace to obtain a matching in every rotated support, then compactness of the orthogonal group for a positive uniform constant. It is a valid qualitative alternative, not an unstated effective capacity algorithm.

5. **Joint versus scalar ranks (`eq:sos-certificate` and the cross-product example).** The squared-Hessian identity gives an explicit full nc-rank certificate. Every nonzero scalar combination in the cross-product family has scalar rank four, while the joint six-input coefficient is three. Direct sums preserve the demonstrated gap. The graph-space identity with fractional vertex covers follows from the two independently proved precision laws. It is not obtained by substituting ordinary scalar rank for nc-rank.

6. **Uniform rational continuation (`thm:rational-ncrank`).** The rational shrunk-subspace algorithm has the stated field and encoding guarantees. Rational bases for the shrinking spaces need not be orthonormal: their orthogonal subspace relations are sufficient for the zero blocks. Coordinate bounds and Hessian denominator clearing have polynomial bit length. Capacity scales with the denominator to power twice the compressed dimension; the lower bound retains that exponent and the box-volume denominator. This supplies the promised uniform polynomial input-height overhead without changing the arbitrary-real fixed-data theorem.

The remaining smooth and perspective results also survive reconstruction. The tensor-phase mixed-Hessian estimate cancels the blow-up dimension after taking the appropriate root. The global-span upper bound uses a fixed shrinking decomposition and does not assert it is always exact. Partial Legendre coordinates yield affine gradient fibers, but the final tubes are polyhedral in the original coordinates; no nonlinear coordinate change is treated as a free formulation operation. Perspective row homogenization is exact because the scale is bounded away from zero and the integer coordinates being multiplied are binary. The PIT reduction and its circuit-input qualification are preserved.

### Finite quadratic theory

I checked both comparison directions for the covariance determinant, its dimension constants, attainment and positivity, the geodesic energy expressions, and the finite residual certificate. The rational Jacobi argument uses exactly orthogonal rational rotations and does not assume an eigenvalue gap. The matrix-function error estimates, bounded-radius geodesic iteration, near-active branch errors, final rational feasibility repair, and subsequent grid loss are compatible. They give polynomial complexity in encoded data and requested precision rather than a practical iteration claim.

The grouped-PSD and total-absolute-error extensions retain the correct homogeneous degree and positive-semidefinite energy structure. The correlation-SDP repair is exactly feasible with unit diagonal and its objective loss gives certified upper and lower values. The general-body reduction first restricts to the nonlinear output image, while the input quotient subtracts affine output terms before projecting. Both directions of the equality of formulation minima retain the real domain. The zonotope volume charge, block product-domain hypothesis, diagonal specialization, integer-feature minor bound, and exact forest volume have independent justification. The thin-domain example correctly rules out dropping those hypotheses. Max-Cut hardness distinguishes valid-formulation construction from solving a formulation, and the positive-optimum amplification does not claim to exclude every sublinear additive function.

### Scalar nonlinear theory

I reconstructed the chord refinement and packing argument, the truncated-curvature local remainder and telescoping potential, and both uses of the positive-power counterexample. Raw curvature mass at fixed tolerance and the coefficient-allocation gap at a different tolerance are kept separate. In certified integration, the positive-coefficient sector argument is not extended without proof to signed coefficients: the latter use the Taylor panel certificate, root separation, and polynomial bounds on failed panels. The inverse-modulus argument and the later mass-accurate knot routine have different purposes, and the latter does not require a density lower bound.

The compiler forces continuous Boolean wires from the declared index bits and uses common-denominator output decoding. Exact graph containment follows from coverage of the input path and the explicit bands, including duplicate or reversed knots. The hybrid absorbs curvature-piece counts only in the branch where its greedy abort proves the needed lower bound. The separable packing, positive supporting scalarization, degree layers, sparse rounded powers, and unconditional allocation consistently restore affine terms exactly and control the sum of local errors.

The Stieltjes construction is polynomial in numerical dense degree; the separate indexed inverse-power routine is polynomial in binary exponent length. The supplied positive-denominator certificate is a hypothesis of the general signed rational-function gadget. The relative-error obstruction handles unbounded integer witnesses and the concave threshold. In the root-encoding lower bound, freezing a possibly huge integer witness changes the right-hand-side numerator, but not the determinant denominator bound. The conic-value gadget excludes a nonzero recession value at zero weight, and the short conic formulation does not promise numerical tolerance stability.

### Vector theory and separations

I checked the finite refinements, ordered implicit overlay, common denominator, and containing-source-cell search, including endpoint multiplicities. Original-output spanners preserve the sign of convex chord gaps; arbitrary algebraic bases would not suffice. The rational polar construction supplies weak access and exact feasible repaired rows, with a fixed denominator controlling later exchanges. The final inner band lies in the effective image and is explicit linear data. No oracle remains as an optimization constraint.

The separable vector proof uses one concatenated basis across all coordinates, with the corresponding product packing and shared coordinate interpolation weights. The constants in the box, facet, and oracle rows follow from their local capacities and lattice-ball losses. I checked the positive-power thirds obstruction, cap-set reduction, repeated-convexification argument, and every integer section of the degree-32 three-box construction. The exact product counts do not purport to settle the one-input question. The Bernstein triangular-wave construction, signed overlay bands, tilted-body projection, and growing conditioning estimate preserve the distinctions among convexity, input dimension, and error geometry. The Helly/Radon discussion identifies limits of particular routes and does not assert a general impossibility theorem.

## Coverage and source assessment

I cross-checked every canonical and substantive-support row against the manuscript claim or proof component named in `coverage.md`, using the original source material read in this and the preceding review passes. The current round included fresh statement/scope comparisons for the foundational and finite quadratic source files and their supporting developments. The scalar and vector original-source readings were retained from my immediately preceding reviews and checked against the fresh full manuscript reread; I did not treat their audit status labels as evidence of validity. My source comparison is at the level of substantive results and proof mechanisms, not an assertion that every historical sentence or superseded numerical variant belongs in the paper.

The inventory has exactly 43 canonical links, 34 substantive-support links, and 196 dependency/audit links; all target files exist. I found manuscript locations for the distinct developments, including the indefinite simplex argument, the elementary permanent proof, one-sided face bound, PIT limitation, covariance certificate, signed curvature integration, raw-curvature and allocation obstructions, signed rational endpoint gadget, hinge/Bernstein stability, repeated thirds convexification, and conditioning comparisons. The pending whole-paper gate is appropriate for this snapshot. I did not freshly reread all 196 historical derivation, novelty, and review files in full.

For the algebraic imports I freshly checked GGOW's Theorems 1.4 and 1.17 and the capacity discussion in its primary text, and extracted the actual PDF pages 26–27 for Theorem 2.18. The latter gives the integral bound `cap(T) >= n^(-2n)` under rank nondecrease, exactly the bound needed here. I checked IQS's Theorem 1.5 and Lemma 5.3 for a rational maximal shrunk subspace, intermediate and final bit bounds, and invariance under field extension. The free-skew-field involution used in Hermitian compression is explicitly supplied by [Volčič's primary manuscript](https://arxiv.org/html/2101.02314), which fixes the free variables and conjugates scalars. These are imported algebraic facts, as the paper says.

My preceding direct primary-source checks also cover the quoted GLS weak-optimization interface, the spanner constructions and approximate-oracle predecessor, shared SOS2 breakpoints, proportional-fairness inequality, cap-set theorem, and mixed Helly statement; their use was reconsidered against the present proofs. I read every current bibliography entry and every citation context. This was not a fresh exhaustive search for priority, nor an independent proof of the classical imported theorems. No unsupported priority claim was identified in the synthesis.

## Executed checks and limits

In this whole-paper round I ran a new inline checker with seed `2026090502`:

- 185 graph cases: all labeled simple graphs on one through four vertices, plus 60, 35, and 15 sampled graphs on five, six, and seven vertices. Exhaustive half-integral cover allocations were compared with ranks of eight two-by-two matrix blow-ups per graph, computed exactly modulo the prime 1000003. Each best rank equaled four times the fractional-cover optimum. These are exact witnesses and finite checks; random evaluations are not used as a general rank algorithm or proof.
- 40 exact rational fourth-moment covariance identities for centered five-point distributions in three dimensions and signed symmetric Hessians.
- Symbolic verification that the cross-product scalar pencil has rank four and that its three squared Hessians sum to `2 I_6`.
- Reverification of all eleven frozen SHA-256 hashes, all inventory link targets, 258 unique LaTeX labels, and resolution of every extracted cross-reference and all 39 cited bibliography keys.

All checks passed. A first PDF-extraction attempt using the unavailable Python `fitz` module failed; `pdftotext` successfully supplied the required original capacity theorem and proof pages. This tooling failure did not leave that import unchecked. I did not run the shared LaTeX build, edit the manuscript or research sources, or spawn subagents. This review is primarily a source-level mathematical assessment, not a fresh page-by-page visual inspection of the PDF. I have not implemented the entire rational optimization/compiler pipeline; the algorithmic assessment rests on reconstructing its error and bit-length proofs, supplemented by the specified exact checks.
