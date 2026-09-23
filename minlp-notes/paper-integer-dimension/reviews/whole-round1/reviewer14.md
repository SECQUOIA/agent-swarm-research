# Reviewer 14 — whole-paper round 1

Major findings: 0
Minor findings: 0

No numbered correction finding or unresolved question is raised. I found no concrete mathematical failure, missing substantive development, or materially inaccurate attribution in the reviewed manuscript. This is a bounded independent review, not a formal correctness certificate, an exhaustive priority search, or a prediction of publication acceptance.

I read the entire current manuscript source: main, macros, abstract, introduction, all four mathematical files, conclusion, bibliography and coverage inventory. I also read WHOLE-TASK.md, WHOLE-LENSES.md, PROCESS.md, PROTOCOL.md and literature/AGENTS.md. I reconstructed the mathematical chain below rather than treating earlier stage acceptance as proof. Source-result comparisons included the actual original statements and relevant supporting arguments; I did not infer coverage merely from file names or review-status labels. The extra focus of this report is complete substantive coverage and the hypotheses and credit of primary imports.

## Independent full-paper assessment

### Model and foundations

The graph sandwich, finite but unrestricted continuous dimension, arbitrary convex lift, real-coefficient finite existence model, and binary **linear** comparison are consistent throughout. Exact graph witnesses are the lower-bound inputs. Parity contact sets need not be convex or measurable: their compact closures inherit midpoint inequalities by continuity and cover the domain. The arguments do not close the entire lift or assert that its projection is closed. Higher rational convex weights are used only when the corresponding integer-label arithmetic warrants them.

I reconstructed the square count including zero bits, strong-curvature diameter/volume estimate, product area bound and four-point obstruction, and the unequal-edge LP lower and shared-prefix upper. The scalar indefinite maximal-simplex determinant argument handles null directions without importing strong convexity. Signed-square decomposition and the fold underestimator give the graph rank law and the separate epigraph/hypograph inertia laws; the one-sided unbounded recession direction is preserved. The finite-union formulation accounts for common recession cones and does not require bounded continuous auxiliaries in the perspective homogenization.

For the system law, I checked the Hermitian principal-pivot induction over a division ring, descent of a maximal shrinking subspace to the reals, the symmetric shrinking decomposition, capacity-to-covariance energy inequality, and the volume estimate. The coordinate precision exponents sum to half the noncommutative rank. The independent compact-group/permanent argument is actually retained, not silently replaced by a capacity citation. The cross-product Hessians satisfy the squared-Hessian certificate while every nonzero scalar combination has rank four. This distinguishes scalar rank from the joint invariant.

For smooth maps, I reconstructed the local mixed-Hessian oscillatory estimate and its application to Cartesian powers of contacts. The evaluation dimension cancels upon taking the root. Global Hessian-span shrinking supports anisotropic Taylor cells; fixed numerical polynomial degree supports the stated prefix-product size, but an arbitrary smooth map has no claimed logarithmic-size formulation. The partial Legendre chart gives affine gradient fibers under constant scalar rank and produces local polyhedral tubes. Compactness supplies finitely many charts. Positive perspective transfer divides by a strictly positive scale; it does not claim the same bounded-product gadget works for an unbounded general integer.

### Finite quadratic accuracy and rational algorithms

I checked both directions of the covariance determinant comparison, the constants from the covariance cap and rotated grid, geodesic energy convexity despite indefinite Hessians, commuting reduction by successive geometric means, and the explicit covariance-benchmark gap. The latter concerns this benchmark; it is not used to rule out every sharper invariant. The residual certificate is sufficient for a global determinant bound and does not claim necessity of multipliers.

The rational nc-rank construction uses a rational maximal shrunk subspace with polynomial intermediate bit length, not just a polynomial number of arithmetic operations. Clearing Hessian denominators scales capacity by the determinant power D_H^(-2r); rational input-box widths contribute the original denominator product to the lower estimate. The dependence on the full accuracy input is retained.

I reconstructed rational Jacobi residual contraction, exact orthogonality, denominator accumulation, and the square-root/log/exp error bounds. The geodesic algorithm applies its recurrence to the actual rational iterates, budgets objective and metric errors, and repairs the final covariance by an exactly computable scale. The matrix-curvature import has the stated affine-invariant normalization. Polynomial iteration and precision bounds are conservative theoretical guarantees, not practical runtime claims.

The grouped-PSD extension works through Gram energies and does not require computing an irrational factorization. Its explicit convention permits unmeasured output directions. The l1 extension uses the PSD Grothendieck bound and a rational correlation-matrix feasibility repair, with low output dimensions handled separately. General symmetric bodies are restricted to the nonlinear output image before rounding; intersection with that image precedes projection, preserving graph containment and both minima. The input quotient retains the actual zonotope with a rational linear lift and incorporates domain volume loss.

For block PSD, diagonal, integer-feature and forest cases I checked the expectation of the nonnegative Jensen vector, block determinant inequality, the exact allocation oracle interface, active kernels, integer-minor volume lower bound and forest image volume. Shared or transformed blocks do not remove input-domain correlation for free; the thin-domain example demonstrates the loss explicitly. Max-Cut zero-dimension equivalence, replication, positive-optimum offset and unit-tolerance scaling support the stated additive and multiplicative barriers. The paper does not claim general coNP membership or an algorithm for optimizing the output MILP.

### Scalar shape, compilation and encoding

I reconstructed three-piece scalar refinement, chord/packing comparison, truncated-curvature local remainder and global mass bound. Signed monotone-curvature integration uses certified root separation and panel control; the positive-sector alternative and the input-accurate inverse modulus remain present. The compiled quantile bound allows clipped or reversed local paths and gives both graph coverage and a bound for every admitted output. The dense convex hybrid either finishes a polynomial-size greedy partition or uses a lower bound on the optimum count to absorb curvature splitting. Numerical dense degree, sparse binary degree and binary rational exponent are kept separate.

The compiler forces continuous Boolean wires by integral external index bits, decodes fixed-denominator endpoints and uses a common interpolation parameter. The signed rational P/Q endpoint gadget retains a positive denominator certificate and its zero-bit case. Endpoint values and interpolation products are not assumed exact merely because a circuit computes their index. Common denominators, output rounding, invalid codes and polynomial evaluation complexity are supplied where needed.

I checked Jensen superadditivity, product packing, feature-curve comparisons, support-allocation multipliers, endpoint layers and the sparse rounded-power algorithm. The coefficient-allocation and raw-curvature counterexamples remain distinct finite-accuracy statements. For pure powers, finite degree-independent comparisons are separated from dense-degree Stieltjes construction and binary rational-exponent inverse evaluation. Positive quadrature weights, tail bounds and rational normalization provide the reciprocal approximation used by the linear gadget.

The relative-error obstruction handles unbounded integer labels through a modulus argument and treats convex/concave exponents and the tolerance threshold separately. The truncated-domain law does not contradict the endpoint impossibility. For the root encoding separation, fixing an integer witness changes right-hand sides but not the coefficient denominators controlling an LP basic solution; the lower bound therefore survives unrestricted witness magnitudes. The four-bit upper count, total linear encoding order, and short conic construction are distinct claims. The conic value gadget includes its zero-weight case and both primal and dual constraints; repeated squaring provides the required exact values without long rational coefficients.

### Vector theory, separations and synthesis

I checked arbitrary level refinement, sorted random-access overlay including duplicates, and the deterministic common-grid monotonicity argument. Every vector component shares the input cell and interpolation weight. Selecting original convex outputs or nonnegative polar scalarizations is essential: arbitrary algebraic bases need not preserve nonnegative gaps. The finite maximum-determinant and rational determinant-exchange spanners have the stated coefficient factors.

The maximum-product transfer uses a feasible box and the correct approximate support inequality. For oracle rank, the positive polar is accessed weakly from the original strong oracle with known balls. Fixed-grid rounding and central repair make returned spanner rows exactly feasible and prevent denominator growth across exchanges. The second spanner produces an explicit inner parallelotope in the nonlinear image. Rounding effective coordinates keeps errors in that image. The final band contains the exact graph and bounds all admitted errors; no oracle constraint remains in the MILP.

For separable vectors, one concatenated basis is shared across all input coordinates. Product packing and the integer l1-ball estimate produce the displayed finite and compiled overheads; coordinatewise tolerances and rounding sum within the final body. General mixed-coordinate polynomials are explicitly outside this argument.

I reconstructed the separated-power thirds inequalities, cap-set reduction and independent one-integer repeated-convexification obstruction. Their statements do not confuse a growing lower bound on both minima with a growing difference. The fixed-degree product example checks the entire middle integer section, not only initially labeled graph segments, and gives exact n versus ceil(n log2 3) counts. The hinge/Bernstein stability mechanism is retained separately. The triangular-wave Bernstein polynomial yields two general integers and logarithmically growing binary dimension with numerical degree growing; convexification by a common quadratic transfers the obstruction only to tilted, increasingly ill-conditioned bodies. The inner/outer-ball and simplex-band comparisons, including the nonsymmetric extension, use exactly their stated body inclusions.

The abstract, introduction, result map and conclusion match these hypotheses. They keep the one-input box constant-gap question, rank-changing smooth boundary and mixed-coordinate vector extension open. None of the introduction's contribution statements converts finite existence into polynomial encoding, or a short integer list into ideality or easy optimization.

## Coverage cross-check

The 43 canonical rows break into 9 foundational, 13 finite-quadratic, 11 scalar and 10 vector results. The following locations were checked against the source developments and the manuscript proofs. Some statements improve or generalize an earlier numerical bound; their distinct proofs, constructions and counterexamples remain covered.

| Original result file | Manuscript location |
| --- | --- |
| `bilinear-graph-binary-complexity.md` | thm:graph-cover |
| `constant-hessian-rank-smooth-precision.md` | thm:constant-rank |
| `mip-relaxation-binary-lower-bounds.md` | thm:square; eq:strong-lower; cor:c2-strong; eq:product-finite |
| `perspective-integer-precision.md` | prop:perspective |
| `quadratic-inertia-one-sided-integer-complexity.md` | thm:inertia; eq:product-one-sided |
| `quadratic-rank-integer-complexity.md` | thm:scalar-rank |
| `quadratic-system-covariance-lower-bounds.md` | lem:covariance; eq:sos-certificate |
| `quadratic-system-noncommutative-rank-complexity.md` | thm:ncrank |
| `smooth-map-local-rank-integer-complexity.md` | thm:smooth-ranks |
| `block-psd-quadratic-precision.md` | thm:block-psd; eq:block-psd-law; eq:block-rank-count |
| `block-psd-unconditional-error-precision.md` | thm:block-psd; lem:block-logdet-oracle |
| `diagonal-psd-quadratic-linear-dimension-precision.md` | cor:diagonal-psd; eq:diagonal-count; scalar log-coordinate algorithm |
| `forest-laplacian-quadratic-precision.md` | cor:forest-precision; eq:forest-volume |
| `independent-integer-feature-quadratic-precision.md` | thm:integer-features; eq:feature-count |
| `quadratic-ellipsoidal-output-precision.md` | thm:grouped-covariance; eq:shared-ellipsoidal-error |
| `quadratic-general-norm-output-precision.md` | thm:general-quadratic-body; eq:output-image-equivalence |
| `quadratic-integer-precision-approximation-hardness.md` | lem:zero-count-maxcut; thm:count-hardness |
| `quadratic-l1-output-precision.md` | thm:l1-covariance; eq:correlation-repair |
| `quadratic-ncrank-rational-construction.md` | thm:rational-ncrank; eq:rational-ncrank-lower-explicit (full proof) |
| `quadratic-nonlinear-input-rank-precision.md` | thm:input-quotient; eq:quotient-domain-volume |
| `quadratic-weighted-covariance-precision.md` | thm:finite-covariance; prop:commuting-covariance; ex:covariance-gap |
| `quadratic-weighted-precision-polynomial-construction.md` | thm:rational-finite; lem:rational-jacobi; eq:inexact-recurrence |
| `accuracy-dependent-curvature-precision.md` | thm:curvature-mass; eq:mass-local-remainder; ex:positive-degree-gap (accepted at stage 3 gate) |
| `compiled-curvature-quantile-precision.md` | lem:certified-curvature; thm:compiled-curvature; eq:mass-knot-certificate (accepted at stage 3 gate) |
| `convex-polynomial-compiled-integer-precision.md` | thm:convex-hybrid; eq:hybrid-total-cells; thm:separable-scalar (accepted at stage 3 gate) |
| `positive-polynomial-loglog-degree-precision.md` | thm:positive-loglog; eq:allocation-supporting-normal; eq:layer-curvature; ex:positive-degree-gap (accepted at stage 3 gate) |
| `positive-pure-power-linear-dimension-precision.md` | prop:pure-power-finite; lem:stieltjes-power; thm:reciprocal-powers (accepted at stage 3 gate) |
| `positive-separable-polynomial-integer-precision.md` | prop:positive-baseline; eq:exact-prefix-powers; eq:feature-jensen (accepted at stage 3 gate) |
| `positive-separable-unconditional-error-precision.md` | prop:positive-baseline; eq:positive-allocation-oracle; eq:unconditional-diagonal-sharp (accepted at stage 3 gate) |
| `rational-power-compiled-integer-precision.md` | lem:inverse-power-index; thm:rational-powers; eq:scaled-power-jensen (accepted at stage 3 gate) |
| `separable-convex-graph-linear-dimension-precision.md` | lem:jensen-superadditivity; thm:separable-scalar; eq:separable-product-packing (accepted at stage 3 gate) |
| `small-exponent-milp-soc-encoding-separation.md` | thm:root-encoding; lem:conic-value; thm:root-conic-separation (accepted at stage 3 gate) |
| `sparse-positive-polynomial-circuit-precision.md` | lem:binary-power-evaluation; sparse proof of thm:positive-loglog; eq:sparse-polynomial-band (accepted at stage 3 gate) |
| `convex-polynomial-box-error-exact-integer-gap.md` | thm:exact-box-gap; eq:exact-box-counts; affine monotonicity shear and precursor stability after the theorem |
| `convex-separable-vector-curvature-rank-precision.md` | lem:vector-product-packing; thm:separable-vector-rank (box and facet rows) |
| `convex-separable-vector-oracle-curvature-rank-precision.md` | thm:separable-vector-rank (finite and compiled oracle row); shared effective image and explicit band |
| `convex-vector-compiled-integer-precision.md` | lem:implicit-overlay; thm:convex-vector-overlay; deterministic monotone quantile proof |
| `convex-vector-curvature-rank-precision.md` | lem:curvature-spanner; thm:vector-rank; eq:vector-box-rank |
| `convex-vector-facet-curvature-rank-precision.md` | thm:vector-rank; eq:vector-facet-rank; eq:facet-linear-band; weighted l1 specialization |
| `convex-vector-oracle-curvature-rank-precision.md` | lem:rational-spanner; thm:vector-oracle-rank; eq:inner-image-band |
| `convex-vector-unconditional-compiled-precision.md` | prop:vector-log-product; eq:product-support; eq:approximate-product-support |
| `polynomial-graph-binary-integer-degree-gap.md` | thm:nonconvex-gap; eq:convexity-piece-bound; scalar case of thm:arbitrary-vector-overlay |
| `polynomial-vector-compiled-integer-precision.md` | thm:arbitrary-vector-overlay; eq:signed-overlay-bands; metadata and duplicate handling |

All 34 explicit supporting developments are also represented. My substantive checks covered the following additional content, including items superseded in count but not in method:

- Foundation supports (4): unrestricted-integer parity and LP epigraph face count; four-point width obstruction; the norm/global-span and circuit-PIT boundaries; source positioning for the scalar indefinite and nc-rank laws.
- Finite quadratic supports (6): thin correlated domains; commuting geometric-mean reduction and water filling; the n log n benchmark gap; block logdet weak optimization with explicit interior ball and rational repair; determinant residual certificates; rational Jacobi and matrix-function precision.
- Scalar supports (13): both signed-monotone and positive-sector certified integration; generic indexed circuit compilation; raw-curvature obstruction; coefficient-allocation degree gap; feature-curve geometry; certified positive Stieltjes quadrature; pure-power source comparison; scalar log-product specialization; relative-power obstruction; continuous scalar two-bit theorem; total rational MILP denominator barrier; signed shared-prefix P/Q interpolation including zero-bit and nonmonotone-path cases.
- Vector supports (11): conditioning/simplex comparisons; continuous separable finite companions; the one-input lattice/Helly/Radon investigation; hinge and polynomial stability precursor; tilted-body transfer; nonconvex promoted precursor (no additional theorem to duplicate); source comparison and mathematical positive-power refinement obstruction; cap-set strengthening; three-witness repeated convexification; rational positive-polar spanner interface.

The 196-note dependency/audit index includes repeated reviews, promoted pointers and novelty searches. I checked the listed distinct developments and their original mathematical content; I did not read every line of every historical audit or treat an audit's approval as evidence that a proof is correct. The executable check also confirms that all inventory links exist and all named manuscript locations resolve. It is only a structural supplement to the content comparison above.

## Primary-source scrutiny and credit

Primary passages were read directly from open original manuscripts/published copies and their local extractions, rather than from the repository's audit conclusions. Some passages were first read during the immediately preceding staged reviews in this continuous session and compared again with their unchanged current applications. This is not a claim to have read every page of all 39 cited publications. The consequential checks include:

- Lubin–Vielma–Zadik, Lemma 4.1 and its proof: integer parity and unrestricted integer labels. Their representation definition is closed-convex; the paper supplies its own closure-free contact argument rather than silently importing the broader convention. Vielma, Proposition 1/Corollary 1 and their assumptions: binary embeddings of rational polyhedral unions and common recession. The manuscript proves its real-coefficient version directly and does not import ideality into the complexity comparisons.
- GGOW, Theorems 1.4, 1.17 and 2.18, and positive-capacity discussion: complex-field rank/evaluation/shrinking, Gurvits' capacity equivalence, and integral square Kraus operators for the quantitative capacity bound. IQS, full-manuscript Theorem 1.5 and Lemma 5.3: rational intermediate/final bit bounds and field-extension invariance. The lower proof uses the exact denominator scaling required by these hypotheses.
- Volčič, Section 2.1: the involution conjugates scalars and fixes the free variables, with product order reversed. This is explicitly present in the [published primary text](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/hilberts-17th-problem-in-free-skew-fields/1DC74DC3E0E011210C826FF4DCA24DE1), inspected during this whole round. The manuscript's Hermitian-pencil use is legitimate.
- Wolff, Theorem A, pp. 50–51: the compactly supported smooth amplitude and nondegenerate mixed Hessian yield the required L2 decay; the manuscript also proves the local estimate. Nicola, Definition 1.1 and the following paragraph: constant Hessian rank gives affine gradient fibers. The paper supplies the partial Legendre proof and does not claim the foliation itself as new.
- Zhang–Sra, Corollary 8: the projected one-step inequality on a lower-curvature-bounded manifold; Criscitiello–Boumal, Proposition I.1: curvature at least -1/2 under the exact affine-invariant metric used. Dadush–Peikert–Vempala, Theorem B.5: strong separation, an outer bound, and the small-volume alternative; the manuscript's known inner ball excludes that alternative at the chosen threshold. GLS, Definition (5), Theorem (3.1), and Corollaries (3.4)–(3.5): weak objective comparison with the body, polar/anti-blocker access, and the distinction between approximate and exact feasibility. The dimension-one embedding is explicit.
- Sagraloff–Mehlhorn, Theorem 36 in the cited revised full version: root isolation/refinement with coefficient and separation-dependent bit bounds. Simchowitz et al., Lemma 2.1, and Codsi et al., Sections 3–5: midpoint/chord and adaptive segmentation precedents. Avis et al., Section 3/Lemma 1, and Adams–Henry, Section 2: continuous circuit constraints and products with discrete values. These do not alone supply implicit endpoint random access; that interface is proved here.
- DLMF Section 3.5(v), and Bonito–Pasciak Section 3.3, equation (37)/Lemma 3.4: positive exact Gaussian quadrature and positive-resolvent fractional-power approximation. The manuscript proves its own scalar uniform truncation, rational coefficient and normalization guarantees. Wang's power-cone representations and O'Donnell's encoding discussion are contextual precedents, not imported four-bit graph-separation theorems.
- Awerbuch–Kleinberg, Section 2.3, Propositions 2.2/2.4; Plevrakis–Hazan, Section 3.2; Lyu–Hicks–Huchette, Section 3/Proposition 1; Kelly–Maulloo–Tan, Section 2: barycentric spanners, approximate-oracle exchanges, shared same-input SOS2 partitions and proportional-fair maximum-product allocation. The manuscript credits those established methods and proves the fixed-denominator, exact-feasibility and implicit-list interfaces needed here.
- Ellenberg–Gijswijt, Theorem 4: the F3 specialization and monomial bound match the cap-set application; the optimized exponential base is derived locally. Hartman's difference-of-convex framework and Averkov–Weismantel's Theorem 1.1 are used with accurate, limited scope. Mixed Helly is not presented as an error-preserving interval-cover result.

I read the entire bibliography and matched the application-specific version/numbering conventions. In particular the 2018 IQS full version, 2015 Sagraloff–Mehlhorn revision, 2011 DPV full manuscript, and appendix-bearing Criscitiello–Boumal version are identified. The Lyu publication's 2026 issue year is consistent with its earlier online/preprint availability. Classical methods are credited in both the local discussion and the introduction; the paper's claimed contributions are its graph-error/count comparisons, rational interfaces and explicit examples. I found no unsupported assertion of exhaustive priority. This audit does not prove no closer external paper exists.

## Executed checks and limits

- Independently recomputed every SHA-256 below for both the live file and the archived `whole-round1/source` copy; all 22 comparisons match the 11-entry snapshot.
- Parsed all manuscript labels, references and citation keys: 258 unique labels, no unresolved reference, 39 bibliography keys all cited, no missing citation key. Checked 43 canonical and 34 substantive-support entries and their links/locations.
- Inspected the existing 84-page PDF with `pdfinfo`, extracted its text with `pdftotext`, and found no `??` unresolved-reference marker. Rendered and visually inspected pages 1, 41, 64 and 84 with `pdftoppm`. No clipping or material layout defect appeared on these sampled pages. I did not run a shared or isolated LaTeX build, and this is not an exhaustive page-by-page typographic audit.
- The structural checker passed before an optional PyMuPDF rendering attempt failed because `fitz` is unavailable. Rendering was then completed successfully with Poppler. No package was installed and no manuscript/build file was changed.
- Mathematical checks above are independent proof reconstructions and explicit constant/error accounting, not machine-checked formal proofs. I did not implement every polynomial-time oracle or use prior script success as a substitute for its proof.

Existing PDF SHA-256: `e42d609f20db16339487d130913bc463d7397fff3d5aa9904251e0dfbd456e4b`. The PDF is not one of the eleven snapshot entries; its source provenance is the frozen manuscript and existing build, not a new build made by this reviewer.

## Reviewed source hashes

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
