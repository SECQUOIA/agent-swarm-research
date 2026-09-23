# Coverage and dependency inventory

This inventory covers the integer-dimension / nonlinear-graph approximation program, not unrelated algorithmic precision results (for example rank-one optimal transport). Canonical result files were found by content search, supplemented by named hidden files and explicit local dependencies. Result names alone were not used as a scope test.

## Stage gates

1. Foundations and precision exponents: verified in `sections/01-foundations.tex`; stage review gate passed (15 reviewers, accepted corrections completed).
2. Finite-accuracy quadratic theory: verified in `sections/02-quadratic-finite.tex`; stage review gate passed (15 reviewers, five accepted correction actions completed).
3. Scalar and separable nonlinear theory, compilation and encoding: verified in `sections/03-scalar-nonlinear.tex`; stage review gate passed (15 reviewers, two accepted correction actions completed).
4. Vector theory, exact separations and synthesis: verified in `sections/04-vector.tex`; stage review gate passed (15 reviewers, one root layout correction completed).
5. Whole-paper proof, coverage, citation, compilation and presentation review: passed after fifteen full-paper reviews, with zero major/minor findings and no accepted outstanding issue.

Coverage alone is not a validity verdict. The mathematical stages and final whole-paper review independently checked the included proofs. Superseded bounds are retained only when their proof, algorithm, constants, hypotheses, or counterexamples contribute distinct information.

## Canonical results (43 files)

| Stage | Source | Development and relation to stronger results | Manuscript location/status |
| --- | --- | --- | --- |
| 1 | [bilinear-graph-binary-complexity](../results/bilinear-graph-binary-complexity.md) | Unequal-edge LP bounds, fractional-cover exponent, shared prefixes, rational preprocessing and constant obstruction. | thm:graph-cover |
| 1 | [constant-hessian-rank-smooth-precision](../results/constant-hessian-rank-smooth-precision.md) | Constant scalar rank via partial Legendre affine fibers and polyhedral tubes; rotating-kernel counterexamples. | thm:constant-rank |
| 1 | [mip-relaxation-binary-lower-bounds](../results/mip-relaxation-binary-lower-bounds.md) | Exact square optimum; product finite constants; strong-curvature volume bounds and matching C² box rate; sawtooth comparison. | thm:square; eq:strong-lower; cor:c2-strong; eq:product-finite |
| 1 | [perspective-integer-precision](../results/perspective-integer-precision.md) | Exact row homogenization and slice transfer, quadratic-over-linear rates and compactness. | prop:perspective |
| 1 | [quadratic-inertia-one-sided-integer-complexity](../results/quadratic-inertia-one-sided-integer-complexity.md) | Epigraph/hypograph inertia, exact product one-sided convex count, linear threshold qualification. | thm:inertia; eq:product-one-sided |
| 1 | [quadratic-rank-integer-complexity](../results/quadratic-rank-integer-complexity.md) | Signed scalar rank law, explicit indefinite determinant bound and compact upper. | thm:scalar-rank |
| 1 | [quadratic-system-covariance-lower-bounds](../results/quadratic-system-covariance-lower-bounds.md) | Covariance identity, squared-Hessian certificate, cross-product counterexample and direct sums. General characterization superseded by nc-rank, explicit certificate retained. | lem:covariance; eq:sos-certificate |
| 1 | [quadratic-system-noncommutative-rank-complexity](../results/quadratic-system-noncommutative-rank-complexity.md) | Exact nc-rank coefficient; principal compression, real descent, symmetric shrinking, capacity and elementary permanent proofs, shared compact upper. | thm:ncrank |
| 1 | [smooth-map-local-rank-integer-complexity](../results/smooth-map-local-rank-integer-complexity.md) | Local oscillatory lower, global-span upper, fixed-degree prefix compiler, rank examples. | thm:smooth-ranks |
| 2 | [block-psd-quadratic-precision](../results/block-psd-quadratic-precision.md) | Block allocation; block-size overhead, rank reductions and required domain structure. | thm:block-psd; eq:block-psd-law; eq:block-rank-count |
| 2 | [block-psd-unconditional-error-precision](../results/block-psd-unconditional-error-precision.md) | Block PSD allocation with unconditional error bodies and certified logdet oracle. | thm:block-psd; lem:block-logdet-oracle |
| 2 | [diagonal-psd-quadratic-linear-dimension-precision](../results/diagonal-psd-quadratic-linear-dimension-precision.md) | Diagonal covariance reduction and linear active-dimension overhead. | cor:diagonal-psd; eq:diagonal-count; scalar log-coordinate algorithm |
| 2 | [forest-laplacian-quadratic-precision](../results/forest-laplacian-quadratic-precision.md) | Forest differences, independent edge coordinates, rational reconstruction and linear rank overhead. | cor:forest-precision; eq:forest-volume |
| 2 | [independent-integer-feature-quadratic-precision](../results/independent-integer-feature-quadratic-precision.md) | Independent primitive integer feature maps without disjoint blocks; finite dimension bounds and limitations. | thm:integer-features; eq:feature-count |
| 2 | [quadratic-ellipsoidal-output-precision](../results/quadratic-ellipsoidal-output-precision.md) | Correlated, Euclidean and overlapping PSD error budgets, including singular unmeasured directions. | thm:grouped-covariance; eq:shared-ellipsoidal-error |
| 2 | [quadratic-general-norm-output-precision](../results/quadratic-general-norm-output-precision.md) | Effective nonlinear output image and strongly separated symmetric oracle bodies; explicit rational output bands. | thm:general-quadratic-body; eq:output-image-equivalence |
| 2 | [quadratic-integer-precision-approximation-hardness](../results/quadratic-integer-precision-approximation-hardness.md) | Zero-dimension Max-Cut equivalence; positive-optimum additive/multiplicative hardness and unit-tolerance amplification. | lem:zero-count-maxcut; thm:count-hardness |
| 2 | [quadratic-l1-output-precision](../results/quadratic-l1-output-precision.md) | PSD Grothendieck correlation SDP and rational feasible-oracle repair for total absolute error. | thm:l1-covariance; eq:correlation-repair |
| 2 | [quadratic-ncrank-rational-construction](../results/quadratic-ncrank-rational-construction.md) | Uniform rational nc-rank construction and lower bounds with polynomial input-height overhead. Stage 1 states the exact scope; stage 2 proves the bit bounds. | thm:rational-ncrank; eq:rational-ncrank-lower-explicit (full proof) |
| 2 | [quadratic-nonlinear-input-rank-precision](../results/quadratic-nonlinear-input-rank-precision.md) | Common Hessian-kernel quotient, zonotope domain, rank-based additive overhead and hardness transfer. | thm:input-quotient; eq:quotient-domain-volume |
| 2 | [quadratic-weighted-covariance-precision](../results/quadratic-weighted-covariance-precision.md) | Finite unequal-tolerance determinant characterization and dimension-only constants; covariance-benchmark gap. | thm:finite-covariance; prop:commuting-covariance; ex:covariance-gap |
| 2 | [quadratic-weighted-precision-polynomial-construction](../results/quadratic-weighted-precision-polynomial-construction.md) | Deterministic rational geodesic optimization, certified matrix functions and rational grid; additive O(n log n). | thm:rational-finite; lem:rational-jacobi; eq:inexact-recurrence |
| 3 | [accuracy-dependent-curvature-precision](../results/accuracy-dependent-curvature-precision.md) | Truncated curvature mass versus chord count and true integer minimum; raw curvature arclength obstruction. | thm:curvature-mass; eq:mass-local-remainder; ex:positive-degree-gap (accepted at stage 3 gate) |
| 3 | [compiled-curvature-quantile-precision](../results/compiled-curvature-quantile-precision.md) | Certified cumulative integration, mass quantiles, random access and positive scalar p_conv+7 compiler. | lem:certified-curvature; thm:compiled-curvature; eq:mass-knot-certificate (accepted at stage 3 gate) |
| 3 | [convex-polynomial-compiled-integer-precision](../results/convex-polynomial-compiled-integer-precision.md) | Arbitrary dense convex polynomial compiler p_conv+11; signed monotone integration, inflection neighborhoods, hybrid greedy/quantile selection. | thm:convex-hybrid; eq:hybrid-total-cells; thm:separable-scalar (accepted at stage 3 gate) |
| 3 | [positive-polynomial-loglog-degree-precision](../results/positive-polynomial-loglog-degree-precision.md) | Supporting scalarization removes degree from lower bound; dyadic endpoint layers give loglog-degree upper overhead and allocation gap examples. | thm:positive-loglog; eq:allocation-supporting-normal; eq:layer-curvature; ex:positive-degree-gap (accepted at stage 3 gate) |
| 3 | [positive-pure-power-linear-dimension-precision](../results/positive-pure-power-linear-dimension-precision.md) | Positive Stieltjes rational inverse approximation and reciprocal MILP gadget with no new bits; dense-degree complexity. | prop:pure-power-finite; lem:stieltjes-power; thm:reciprocal-powers (accepted at stage 3 gate) |
| 3 | [positive-separable-polynomial-integer-precision](../results/positive-separable-polynomial-integer-precision.md) | Coefficient-sum allocation and O(sum log degree) bounds; baseline superseded quantitatively by loglog theorem but retain feature-curve proof. | prop:positive-baseline; eq:exact-prefix-powers; eq:feature-jensen (accepted at stage 3 gate) |
| 3 | [positive-separable-unconditional-error-precision](../results/positive-separable-unconditional-error-precision.md) | Unconditional-body extension of allocation; superseded quantitatively by loglog theorem but oracle reduction retained. | prop:positive-baseline; eq:positive-allocation-oracle; eq:unconditional-diagonal-sharp (accepted at stage 3 gate) |
| 3 | [rational-power-compiled-integer-precision](../results/rational-power-compiled-integer-precision.md) | Binary rational exponents greater than one, inverse-power endpoint compiler and 7r+1 overhead. | lem:inverse-power-index; thm:rational-powers; eq:scaled-power-jensen (accepted at stage 3 gate) |
| 3 | [separable-convex-graph-linear-dimension-precision](../results/separable-convex-graph-linear-dimension-precision.md) | Scalar sums and independent outputs; Jensen superadditivity and product packing give linear dimension, degree-independent overhead. | lem:jensen-superadditivity; thm:separable-scalar; eq:separable-product-packing (accepted at stage 3 gate) |
| 3 | [small-exponent-milp-soc-encoding-separation](../results/small-exponent-milp-soc-encoding-separation.md) | Root-power rational MILP encoding barrier and matching four-bit MILP; primal-dual conic-value gadget yields short MISOCP with same count. | thm:root-encoding; lem:conic-value; thm:root-conic-separation (accepted at stage 3 gate) |
| 3 | [sparse-positive-polynomial-circuit-precision](../results/sparse-positive-polynomial-circuit-precision.md) | Sparse binary exponents; rounded endpoint evaluation circuit; polynomial exponent-bit complexity. | lem:binary-power-evaluation; sparse proof of thm:positive-loglog; eq:sparse-polynomial-band (accepted at stage 3 gate) |
| 4 | [convex-polynomial-box-error-exact-integer-gap](../results/convex-polynomial-box-error-exact-integer-gap.md) | Exact n versus ceil(n log2 3) counts for fixed-degree componentwise convex product curves; rational upper constructions. | thm:exact-box-gap; eq:exact-box-counts; affine monotonicity shear and precursor stability after the theorem |
| 4 | [convex-separable-vector-curvature-rank-precision](../results/convex-separable-vector-curvature-rank-precision.md) | One common concatenated curvature basis across inputs, product packing, n log r+17n compiled box guarantee. | lem:vector-product-packing; thm:separable-vector-rank (box and facet rows) |
| 4 | [convex-separable-vector-oracle-curvature-rank-precision](../results/convex-separable-vector-oracle-curvature-rank-precision.md) | Separable multivariate vector extension to unconditional oracle bodies; effective rank and shared packing. | thm:separable-vector-rank (finite and compiled oracle row); shared effective image and explicit band |
| 4 | [convex-vector-compiled-integer-precision](../results/convex-vector-compiled-integer-precision.md) | Sorted implicit knot overlay, duplicate handling and polynomial order-statistic merge; p_conv+11+ceil(log m). | lem:implicit-overlay; thm:convex-vector-overlay; deterministic monotone quantile proof |
| 4 | [convex-vector-curvature-rank-precision](../results/convex-vector-curvature-rank-precision.md) | Curvature quotient, original-output barycentric spanners, scalar refinement; finite and compiled logarithmic-rank overhead. | lem:curvature-spanner; thm:vector-rank; eq:vector-box-rank |
| 4 | [convex-vector-facet-curvature-rank-precision](../results/convex-vector-facet-curvature-rank-precision.md) | Nonnegative facet scalarization, facet curvature rank, coupled half-body bands and weighted-l1 specialization. | thm:vector-rank; eq:vector-facet-rank; eq:facet-linear-band; weighted l1 specialization |
| 4 | [convex-vector-oracle-curvature-rank-precision](../results/convex-vector-oracle-curvature-rank-precision.md) | Unconditional strong oracle, effective body, positive polar spanner, explicit rational parallelotope; finite O(log r) and compiled guarantees. | lem:rational-spanner; thm:vector-oracle-rank; eq:inner-image-band |
| 4 | [convex-vector-unconditional-compiled-precision](../results/convex-vector-unconditional-compiled-precision.md) | Unconditional log-product allocation plus overlay. Retain its direct construction and comparisons even where rank bounds strengthen dimensions. | prop:vector-log-product; eq:product-support; eq:approximate-product-support |
| 4 | [polynomial-graph-binary-integer-degree-gap](../results/polynomial-graph-binary-integer-degree-gap.md) | Nonconvex scalar polynomial family: two general integers versus growing binary count; Bernstein triangular waves and convexity-piece upper. | thm:nonconvex-gap; eq:convexity-piece-bound; scalar case of thm:arbitrary-vector-overlay |
| 4 | [polynomial-vector-compiled-integer-precision](../results/polynomial-vector-compiled-integer-precision.md) | Arbitrary polynomial vectors with degree/output-dependent implicit overlays and convexity pieces. | thm:arbitrary-vector-overlay; eq:signed-overlay-bands; metadata and duplicate handling |

## Substantive supporting developments that must not be lost

| Stage | Supporting source | Distinct content |
| --- | --- | --- |
| 1 | [mip-binary-lower-bound-extensions](../notes/mip-binary-lower-bound-extensions.md) | Parity extension, logarithmic epigraph LP face-count bound, four-point width obstruction; all drafted. |
| 1 | [nonquadratic-integer-precision-investigation](../notes/nonquadratic-integer-precision-investigation.md) | Global-span norm counterexample and circuit polynomial-identity-testing reduction; both drafted. |
| 1 | [quadratic-noncommutative-rank-novelty](../notes/quadratic-noncommutative-rank-novelty.md) | Source and priority comparison for the matrix-space precision law. |
| 1 | [quadratic-rank-integer-investigation](../notes/quadratic-rank-integer-investigation.md) | Scalar indefinite approximation source comparison and candidate derivation. |
| 2 | [block-psd-domain-correlation-obstruction](../notes/block-psd-domain-correlation-obstruction.md) | Correlated input domains invalidate naive independent-block transfer. Drafted: ex:thin-domain. |
| 2 | [commuting-quadratic-covariance-reduction](../notes/commuting-quadratic-covariance-reduction.md) | Commuting quadratic simultaneous diagonalization and its scope. Drafted: prop:commuting-covariance and water-filling formula. |
| 2 | [covariance-benchmark-dimension-gap](../notes/covariance-benchmark-dimension-gap.md) | Dimension-dependence example for covariance benchmark, independent of computational hardness. Drafted: ex:covariance-gap. |
| 2 | [rational-block-logdet-convex-body-oracle](../notes/rational-block-logdet-convex-body-oracle.md) | Block allocation oracle bit-complexity dependency. Drafted with scalar special case: lem:block-logdet-oracle; eq:central-ball-repair. |
| 2 | [covariance-determinant-optimality-certificates](../notes/covariance-determinant-optimality-certificates.md) | Geodesic Lagrangian residual gives certified finite determinant gaps, rational residual evaluation and convex multiplier refinement. Drafted: prop:covariance-certificate. |
| 2 | [rational-jacobi-matrix-functions](../notes/rational-jacobi-matrix-functions.md) | Certified rational matrix functions and coordinate approximations used by geodesic algorithm. Drafted: lem:rational-jacobi; eq:matrix-function-bounds; eq:relative-metric-bound. |
| 3 | [certified-monotone-polynomial-curvature-quantiles](../notes/certified-monotone-polynomial-curvature-quantiles.md) | Signed-coefficient monotone-curvature integral extension. Drafted: lem:certified-curvature; eq:taylor-panel-certificate; eq:quantile-inverse-modulus. |
| 3 | [certified-positive-polynomial-curvature-quantiles](../notes/certified-positive-polynomial-curvature-quantiles.md) | Polynomial-bit integral oracle with explicit certified approximation and complexity. Drafted: lem:certified-curvature, including separate positive-sector panels and input-accurate quantiles. |
| 3 | [compiled-rational-knot-formulations](../notes/compiled-rational-knot-formulations.md) | Generic circuit-to-MILP compilation; only external index bits need be integral. Drafted: lem:indexed-compiler; lem:inverse-power-index. |
| 3 | [curvature-arclength-precision-obstruction](../notes/curvature-arclength-precision-obstruction.md) | Counterexample to raw curvature mass as a finite-accuracy invariant. Drafted: ex:positive-degree-gap; eq:raw-curvature-obstruction. |
| 3 | [positive-polynomial-allocation-degree-gap](../notes/positive-polynomial-allocation-degree-gap.md) | Coefficient-sum allocation can miss shape; retain sharp loglog degree gap. Drafted: ex:positive-degree-gap; eq:degree-allocation-obstruction. |
| 3 | [positive-polynomial-feature-curve-geometry](../notes/positive-polynomial-feature-curve-geometry.md) | Independent feature-curve geometric lower argument, not just a historical allocation theorem. Drafted: lem:jensen-superadditivity; eq:feature-jensen. |
| 3 | [positive-rational-stieltjes-power-approximation](../notes/positive-rational-stieltjes-power-approximation.md) | Full certified positive quadrature, truncation and rational normalization proof. Drafted: lem:stieltjes-power; eq:gauss-weight-conditioning. |
| 3 | [pure-power-degree-independent-count-novelty](../notes/pure-power-degree-independent-count-novelty.md) | Primary source comparison for the pure-power count guarantee. Drafted: prop:pure-power-finite; finite versus compact construction distinction; Bonito/Avis/Adams source credit. |
| 3 | [rational-log-product-convex-body-oracle](../notes/rational-log-product-convex-body-oracle.md) | Strong oracle optimization and rational allocation feasibility repair. Drafted: eq:positive-allocation-oracle, explicitly specializing accepted lem:block-logdet-oracle and eq:central-ball-repair. |
| 3 | [relative-power-graph-integer-obstruction](../notes/relative-power-graph-integer-obstruction.md) | Infinite dimension for pure relative error near zero, concave threshold, truncated-domain loglog law. Drafted: prop:relative-power; eq:relative-truncated-law. |
| 3 | [scalar-convex-graph-two-bit-gap](../notes/scalar-convex-graph-two-bit-gap.md) | Continuous convex scalar finite two-bit comparison and three-piece refinement; essential primitive beyond polynomial cases. Drafted: lem:scalar-chords; eq:scalar-two-bit. |
| 3 | [small-exponent-rational-formulation-barrier](../notes/small-exponent-rational-formulation-barrier.md) | Uniform LP determinant denominator lower bound with unrestricted integer witnesses; total encoding Theta(D), four-bit upper. Drafted: thm:root-encoding, including total row-bit determinant bound and matching four-bit upper. |
| 4 | [componentwise-convex-fixed-condition-integer-gap](../notes/componentwise-convex-fixed-condition-integer-gap.md) | Conditioning comparisons for tilted symmetric bodies, unconditional dimension-only bounds and sharper simplex bands. Drafted: prop:conditioning; eq:simplex-conditioning; eq:simplex-band; normalization to an inner crosspolytope and the nonsymmetric extension. |
| 4 | [convex-separable-vector-finite-rank-precision](../notes/convex-separable-vector-finite-rank-precision.md) | Continuous convex separable finite companion: n ceil(log2 r)+7n box and +8n facet-body overhead, no polynomial representation assumed. Drafted: thm:separable-vector-rank, finite box +7n and facet +8n rows, with continuous summands. |
| 4 | [convex-vector-box-gap-lattice-investigation](../notes/convex-vector-box-gap-lattice-investigation.md) | Remaining one-input constant-gap question, strict violation sets, and failed Helly/Radon amplification routes. Drafted: subsec:one-input-open; strict violation sets, Helly/Radon and amplification limits. |
| 4 | [convex-vector-one-bit-box-gap-investigation](../notes/convex-vector-one-bit-box-gap-investigation.md) | One-bit gap precursor and exact three-section geometry; compare with tensorized exact result. Drafted: thm:exact-box-gap; hinge precursor and Bernstein stability argument after it; earlier numerical polynomial variants are superseded by the exact degree-32 family. |
| 4 | [convex-vector-tilted-error-integer-gap](../notes/convex-vector-tilted-error-integer-gap.md) | Tilted error-body examples and common-section restrictions; separate convex components from effective scalar nonconvexity. Drafted: prop:tilted-gap; explicit common-direction band, scalar projection and growing conditioning proof. |
| 4 | [nonconvex-polynomial-binary-integer-gap](../notes/nonconvex-polynomial-binary-integer-gap.md) | Precursor construction; retain only distinct construction facts not superseded by the canonical polynomial-gap theorem. Drafted: thm:nonconvex-gap; promoted pointer has no additional theorem. |
| 4 | [positive-polynomial-vector-refinement-novelty](../notes/positive-polynomial-vector-refinement-novelty.md) | Primary source comparison for the vector-power obstruction. Drafted: prop:vector-power-obstruction and its quantified scalarization discussion; classical parity/chord/disjunction source credit. |
| 4 | [positive-polynomial-vector-refinement-obstruction](../notes/positive-polynomial-vector-refinement-obstruction.md) | Positive-power vector family defeats all fixed scalarizations and uniform midpoint refinement; output-dependent finite upper. Drafted: prop:vector-power-obstruction; prop:finite-vector-overlay; output/facet finite upper bounds. |
| 4 | [positive-vector-capset-integer-lower-bound](../notes/positive-vector-capset-integer-lower-bound.md) | Residues modulo three form cap sets; stronger quantitative integer bound and failed ternary construction. Drafted: prop:cap-set; eq:cap-count; Ellenberg–Gijswijt attribution and open-gap limitation. |
| 4 | [positive-vector-three-witness-integer-obstruction](../notes/positive-vector-three-witness-integer-obstruction.md) | Three positive-power outputs already exclude one integer; non-midpoint geometry. Drafted: direct arbitrary-label and repeated-convexification argument following prop:cap-set. |
| 4 | [rational-polar-spanner-oracle](../notes/rational-polar-spanner-oracle.md) | Positive polar support, rational approximate barycentric spanner and explicit body-band certificates. Drafted: lem:rational-spanner; eq:fixed-spanner-grid; eq:spanner-repair; eq:feasible-support; positive-polar separator and effective-body seeds. |
| 3 | [shared-prefix-rational-interpolation-gadget](../notes/shared-prefix-rational-interpolation-gadget.md) | General signed P/Q endpoint products with supplied positive denominator certificate, zero-bit case and clipped nonmonotone path. Drafted: lem:rational-endpoint-products. |

## Dependency and audit index

196 supporting note files are indexed below. Multiple stages mean the note is shared. These include earlier derivations, mathematical audits and bounded novelty searches; none substitutes for a proof or establishes external priority.

| Stages | Supporting note |
| --- | --- |
| 3 | [accuracy-dependent-curvature-precision-novelty.md](../notes/accuracy-dependent-curvature-precision-novelty.md) |
| 3 | [accuracy-dependent-curvature-precision.md](../notes/accuracy-dependent-curvature-precision.md) |
| 1 | [bilinear-graph-binary-complexity-novelty.md](../notes/bilinear-graph-binary-complexity-novelty.md) |
| 2 | [block-psd-domain-correlation-obstruction.md](../notes/block-psd-domain-correlation-obstruction.md) |
| 2 | [block-psd-quadratic-precision-novelty.md](../notes/block-psd-quadratic-precision-novelty.md) |
| 2 | [block-psd-quadratic-precision.md](../notes/block-psd-quadratic-precision.md) |
| 2 | [block-psd-unconditional-error-novelty.md](../notes/block-psd-unconditional-error-novelty.md) |
| 2 | [block-psd-unconditional-error-precision.md](../notes/block-psd-unconditional-error-precision.md) |
| 3 | [certified-monotone-polynomial-curvature-quantiles.md](../notes/certified-monotone-polynomial-curvature-quantiles.md) |
| 3 | [certified-positive-polynomial-curvature-quantiles.md](../notes/certified-positive-polynomial-curvature-quantiles.md) |
| 2 | [commuting-quadratic-covariance-reduction.md](../notes/commuting-quadratic-covariance-reduction.md) |
| 3 | [compact-pure-power-reciprocal-interpolation-novelty.md](../notes/compact-pure-power-reciprocal-interpolation-novelty.md) |
| 3 | [compact-pure-power-reciprocal-interpolation.md](../notes/compact-pure-power-reciprocal-interpolation.md) |
| 3 | [compiled-convex-polynomial-hybrid-novelty.md](../notes/compiled-convex-polynomial-hybrid-novelty.md) |
| 3, 4 | [compiled-convex-polynomial-hybrid-precision.md](../notes/compiled-convex-polynomial-hybrid-precision.md) |
| 4 | [compiled-convex-vector-knot-overlay.md](../notes/compiled-convex-vector-knot-overlay.md) |
| 3 | [compiled-curvature-quantile-precision-novelty.md](../notes/compiled-curvature-quantile-precision-novelty.md) |
| 3 | [compiled-curvature-quantile-precision.md](../notes/compiled-curvature-quantile-precision.md) |
| 4 | [compiled-polynomial-vector-overlay-novelty.md](../notes/compiled-polynomial-vector-overlay-novelty.md) |
| 4 | [compiled-polynomial-vector-overlay-precision.md](../notes/compiled-polynomial-vector-overlay-precision.md) |
| 3 | [compiled-rational-knot-formulations-novelty.md](../notes/compiled-rational-knot-formulations-novelty.md) |
| 3 | [compiled-rational-knot-formulations.md](../notes/compiled-rational-knot-formulations.md) |
| 4 | [componentwise-convex-fixed-condition-integer-gap.md](../notes/componentwise-convex-fixed-condition-integer-gap.md) |
| 4 | [convex-polynomial-box-gap-exact-counts-novelty.md](../notes/convex-polynomial-box-gap-exact-counts-novelty.md) |
| 4 | [convex-separable-vector-curvature-rank-novelty.md](../notes/convex-separable-vector-curvature-rank-novelty.md) |
| 4 | [convex-separable-vector-curvature-rank-precision.md](../notes/convex-separable-vector-curvature-rank-precision.md) |
| 4 | [convex-separable-vector-finite-rank-precision.md](../notes/convex-separable-vector-finite-rank-precision.md) |
| 4 | [convex-separable-vector-oracle-curvature-rank-novelty.md](../notes/convex-separable-vector-oracle-curvature-rank-novelty.md) |
| 4 | [convex-separable-vector-oracle-curvature-rank-precision.md](../notes/convex-separable-vector-oracle-curvature-rank-precision.md) |
| 4 | [convex-vector-box-gap-lattice-investigation.md](../notes/convex-vector-box-gap-lattice-investigation.md) |
| 4 | [convex-vector-curvature-rank-novelty.md](../notes/convex-vector-curvature-rank-novelty.md) |
| 4 | [convex-vector-curvature-rank-precision.md](../notes/convex-vector-curvature-rank-precision.md) |
| 4 | [convex-vector-facet-curvature-rank-precision.md](../notes/convex-vector-facet-curvature-rank-precision.md) |
| 4 | [convex-vector-gap-and-overlay-source-audit.md](../notes/convex-vector-gap-and-overlay-source-audit.md) |
| 4 | [convex-vector-one-bit-box-gap-investigation.md](../notes/convex-vector-one-bit-box-gap-investigation.md) |
| 4 | [convex-vector-oracle-curvature-rank-novelty.md](../notes/convex-vector-oracle-curvature-rank-novelty.md) |
| 4 | [convex-vector-oracle-curvature-rank-precision.md](../notes/convex-vector-oracle-curvature-rank-precision.md) |
| 4 | [convex-vector-tilted-error-integer-gap.md](../notes/convex-vector-tilted-error-integer-gap.md) |
| 4 | [convex-vector-unconditional-log-product-precision.md](../notes/convex-vector-unconditional-log-product-precision.md) |
| 2 | [covariance-benchmark-dimension-gap.md](../notes/covariance-benchmark-dimension-gap.md) |
| 3 | [curvature-arclength-precision-obstruction.md](../notes/curvature-arclength-precision-obstruction.md) |
| 2 | [diagonal-psd-quadratic-linear-dimension-precision.md](../notes/diagonal-psd-quadratic-linear-dimension-precision.md) |
| 2 | [diagonal-psd-quadratic-precision-novelty.md](../notes/diagonal-psd-quadratic-precision-novelty.md) |
| 2 | [forest-laplacian-quadratic-precision-novelty.md](../notes/forest-laplacian-quadratic-precision-novelty.md) |
| 2 | [forest-laplacian-quadratic-precision.md](../notes/forest-laplacian-quadratic-precision.md) |
| 2 | [independent-integer-feature-precision-novelty.md](../notes/independent-integer-feature-precision-novelty.md) |
| 2 | [independent-integer-feature-quadratic-precision.md](../notes/independent-integer-feature-quadratic-precision.md) |
| 1 | [mip-binary-lower-bound-extensions.md](../notes/mip-binary-lower-bound-extensions.md) |
| 4 | [nonconvex-polynomial-binary-integer-gap-novelty.md](../notes/nonconvex-polynomial-binary-integer-gap-novelty.md) |
| 4 | [nonconvex-polynomial-binary-integer-gap.md](../notes/nonconvex-polynomial-binary-integer-gap.md) |
| 1 | [nonquadratic-integer-precision-investigation.md](../notes/nonquadratic-integer-precision-investigation.md) |
| 1 | [perspective-integer-precision-investigation.md](../notes/perspective-integer-precision-investigation.md) |
| 3 | [positive-polynomial-allocation-degree-gap.md](../notes/positive-polynomial-allocation-degree-gap.md) |
| 3 | [positive-polynomial-feature-curve-geometry.md](../notes/positive-polynomial-feature-curve-geometry.md) |
| 3 | [positive-polynomial-linear-dimension-shape-precision.md](../notes/positive-polynomial-linear-dimension-shape-precision.md) |
| 3 | [positive-polynomial-linear-shape-precision-novelty.md](../notes/positive-polynomial-linear-shape-precision-novelty.md) |
| 3 | [positive-polynomial-loglog-degree-novelty.md](../notes/positive-polynomial-loglog-degree-novelty.md) |
| 3 | [positive-polynomial-loglog-degree-precision.md](../notes/positive-polynomial-loglog-degree-precision.md) |
| 4 | [positive-polynomial-vector-refinement-novelty.md](../notes/positive-polynomial-vector-refinement-novelty.md) |
| 4 | [positive-polynomial-vector-refinement-obstruction.md](../notes/positive-polynomial-vector-refinement-obstruction.md) |
| 3 | [positive-rational-stieltjes-power-approximation.md](../notes/positive-rational-stieltjes-power-approximation.md) |
| 3 | [positive-separable-polynomial-integer-precision.md](../notes/positive-separable-polynomial-integer-precision.md) |
| 3 | [positive-separable-polynomial-precision-novelty.md](../notes/positive-separable-polynomial-precision-novelty.md) |
| 3 | [positive-separable-unconditional-error-novelty.md](../notes/positive-separable-unconditional-error-novelty.md) |
| 3 | [positive-separable-unconditional-error-precision.md](../notes/positive-separable-unconditional-error-precision.md) |
| 4 | [positive-vector-capset-integer-lower-bound.md](../notes/positive-vector-capset-integer-lower-bound.md) |
| 4 | [positive-vector-three-witness-integer-obstruction.md](../notes/positive-vector-three-witness-integer-obstruction.md) |
| 3 | [pure-power-degree-independent-count-novelty.md](../notes/pure-power-degree-independent-count-novelty.md) |
| 3 | [pure-power-degree-independent-integer-count.md](../notes/pure-power-degree-independent-integer-count.md) |
| 2 | [covariance-determinant-optimality-certificates.md](../notes/covariance-determinant-optimality-certificates.md) |
| 2 | [review-covariance-optimality-certificate-root.md](../notes/review-covariance-optimality-certificate-root.md) |
| 2 | [quadratic-ellipsoidal-output-precision.md](../notes/quadratic-ellipsoidal-output-precision.md) |
| 2 | [quadratic-general-norm-output-precision.md](../notes/quadratic-general-norm-output-precision.md) |
| 2 | [quadratic-general-norm-precision-novelty.md](../notes/quadratic-general-norm-precision-novelty.md) |
| 1 | [quadratic-inertia-one-sided-investigation.md](../notes/quadratic-inertia-one-sided-investigation.md) |
| 2 | [quadratic-integer-precision-approximation-hardness.md](../notes/quadratic-integer-precision-approximation-hardness.md) |
| 2 | [quadratic-l1-output-precision.md](../notes/quadratic-l1-output-precision.md) |
| 2 | [quadratic-ncrank-rational-construction.md](../notes/quadratic-ncrank-rational-construction.md) |
| 1 | [quadratic-noncommutative-rank-novelty.md](../notes/quadratic-noncommutative-rank-novelty.md) |
| 2 | [quadratic-nonlinear-input-rank-precision-novelty.md](../notes/quadratic-nonlinear-input-rank-precision-novelty.md) |
| 2 | [quadratic-nonlinear-input-rank-precision.md](../notes/quadratic-nonlinear-input-rank-precision.md) |
| 2 | [quadratic-precision-approximation-hardness-novelty.md](../notes/quadratic-precision-approximation-hardness-novelty.md) |
| 1 | [quadratic-rank-integer-investigation.md](../notes/quadratic-rank-integer-investigation.md) |
| 1 | [quadratic-system-integer-complexity-investigation.md](../notes/quadratic-system-integer-complexity-investigation.md) |
| 2 | [quadratic-weighted-covariance-algorithm.md](../notes/quadratic-weighted-covariance-algorithm.md) |
| 2 | [quadratic-weighted-covariance-precision.md](../notes/quadratic-weighted-covariance-precision.md) |
| 2 | [quadratic-weighted-precision-algorithm-novelty.md](../notes/quadratic-weighted-precision-algorithm-novelty.md) |
| 2 | [rational-block-logdet-convex-body-oracle.md](../notes/rational-block-logdet-convex-body-oracle.md) |
| 2 | [rational-jacobi-matrix-functions.md](../notes/rational-jacobi-matrix-functions.md) |
| 2, 3, 4 | [rational-log-product-convex-body-oracle.md](../notes/rational-log-product-convex-body-oracle.md) |
| 4 | [rational-polar-spanner-oracle.md](../notes/rational-polar-spanner-oracle.md) |
| 3 | [relative-power-graph-integer-obstruction.md](../notes/relative-power-graph-integer-obstruction.md) |
| 3 | [review-accuracy-dependent-curvature-precision-second.md](../notes/review-accuracy-dependent-curvature-precision-second.md) |
| 3 | [review-accuracy-dependent-curvature-precision.md](../notes/review-accuracy-dependent-curvature-precision.md) |
| 1 | [review-bilinear-graph-binary-complexity.md](../notes/review-bilinear-graph-binary-complexity.md) |
| 1 | [review-bilinear-graph-integer-complexity-second.md](../notes/review-bilinear-graph-integer-complexity-second.md) |
| 2 | [review-block-psd-quadratic-precision-second.md](../notes/review-block-psd-quadratic-precision-second.md) |
| 2 | [review-block-psd-quadratic-precision.md](../notes/review-block-psd-quadratic-precision.md) |
| 2 | [review-block-psd-unconditional-precision-second.md](../notes/review-block-psd-unconditional-precision-second.md) |
| 2 | [review-block-psd-unconditional-precision.md](../notes/review-block-psd-unconditional-precision.md) |
| 2 | [review-commuting-quadratic-covariance-reduction.md](../notes/review-commuting-quadratic-covariance-reduction.md) |
| 3 | [review-compact-pure-power-interpolation-second.md](../notes/review-compact-pure-power-interpolation-second.md) |
| 3 | [review-compact-pure-power-interpolation.md](../notes/review-compact-pure-power-interpolation.md) |
| 3 | [review-compiled-convex-polynomial-hybrid-precision-second.md](../notes/review-compiled-convex-polynomial-hybrid-precision-second.md) |
| 3 | [review-compiled-convex-polynomial-hybrid-precision.md](../notes/review-compiled-convex-polynomial-hybrid-precision.md) |
| 4 | [review-compiled-convex-vector-knot-overlay.md](../notes/review-compiled-convex-vector-knot-overlay.md) |
| 3 | [review-compiled-curvature-quantile-precision-second.md](../notes/review-compiled-curvature-quantile-precision-second.md) |
| 3 | [review-compiled-curvature-quantile-precision.md](../notes/review-compiled-curvature-quantile-precision.md) |
| 4 | [review-compiled-polynomial-vector-overlay-precision-second.md](../notes/review-compiled-polynomial-vector-overlay-precision-second.md) |
| 4 | [review-compiled-polynomial-vector-overlay-precision.md](../notes/review-compiled-polynomial-vector-overlay-precision.md) |
| 3 | [review-compiled-rational-knot-formulations-second.md](../notes/review-compiled-rational-knot-formulations-second.md) |
| 3 | [review-compiled-rational-knot-formulations.md](../notes/review-compiled-rational-knot-formulations.md) |
| 3 | [review-compiled-rational-knots-bit-conditioning.md](../notes/review-compiled-rational-knots-bit-conditioning.md) |
| 4 | [review-componentwise-convex-fixed-condition-integer-gap-root.md](../notes/review-componentwise-convex-fixed-condition-integer-gap-root.md) |
| 1 | [review-constant-hessian-rank-smooth-precision.md](../notes/review-constant-hessian-rank-smooth-precision.md) |
| 4 | [review-convex-separable-vector-curvature-rank-precision-second.md](../notes/review-convex-separable-vector-curvature-rank-precision-second.md) |
| 4 | [review-convex-separable-vector-curvature-rank-precision.md](../notes/review-convex-separable-vector-curvature-rank-precision.md) |
| 4 | [review-convex-separable-vector-oracle-curvature-rank-precision-second.md](../notes/review-convex-separable-vector-oracle-curvature-rank-precision-second.md) |
| 4 | [review-convex-separable-vector-oracle-curvature-rank-precision.md](../notes/review-convex-separable-vector-oracle-curvature-rank-precision.md) |
| 4 | [review-convex-vector-box-gap-root.md](../notes/review-convex-vector-box-gap-root.md) |
| 4 | [review-convex-vector-curvature-rank-precision-second.md](../notes/review-convex-vector-curvature-rank-precision-second.md) |
| 4 | [review-convex-vector-curvature-rank-precision.md](../notes/review-convex-vector-curvature-rank-precision.md) |
| 4 | [review-convex-vector-facet-curvature-rank-precision-second.md](../notes/review-convex-vector-facet-curvature-rank-precision-second.md) |
| 4 | [review-convex-vector-facet-curvature-rank-precision.md](../notes/review-convex-vector-facet-curvature-rank-precision.md) |
| 4 | [review-convex-vector-one-bit-box-gap.md](../notes/review-convex-vector-one-bit-box-gap.md) |
| 4 | [review-convex-vector-oracle-curvature-rank-precision-second.md](../notes/review-convex-vector-oracle-curvature-rank-precision-second.md) |
| 4 | [review-convex-vector-oracle-curvature-rank-precision-third.md](../notes/review-convex-vector-oracle-curvature-rank-precision-third.md) |
| 4 | [review-convex-vector-oracle-curvature-rank-precision.md](../notes/review-convex-vector-oracle-curvature-rank-precision.md) |
| 4 | [review-convex-vector-tilted-error-integer-gap-second.md](../notes/review-convex-vector-tilted-error-integer-gap-second.md) |
| 4 | [review-convex-vector-tilted-error-integer-gap.md](../notes/review-convex-vector-tilted-error-integer-gap.md) |
| 4 | [review-convex-vector-unconditional-log-product-precision-second.md](../notes/review-convex-vector-unconditional-log-product-precision-second.md) |
| 4 | [review-convex-vector-unconditional-log-product-precision.md](../notes/review-convex-vector-unconditional-log-product-precision.md) |
| 2 | [review-covariance-benchmark-dimension-gap.md](../notes/review-covariance-benchmark-dimension-gap.md) |
| 2 | [review-diagonal-psd-quadratic-precision-second.md](../notes/review-diagonal-psd-quadratic-precision-second.md) |
| 2 | [review-diagonal-psd-quadratic-precision.md](../notes/review-diagonal-psd-quadratic-precision.md) |
| 2 | [review-forest-laplacian-quadratic-precision-second.md](../notes/review-forest-laplacian-quadratic-precision-second.md) |
| 2 | [review-forest-laplacian-quadratic-precision.md](../notes/review-forest-laplacian-quadratic-precision.md) |
| 2 | [review-independent-integer-feature-precision-second.md](../notes/review-independent-integer-feature-precision-second.md) |
| 2 | [review-independent-integer-feature-precision.md](../notes/review-independent-integer-feature-precision.md) |
| 1 | [review-mip-relaxation-binary-lower-bounds.md](../notes/review-mip-relaxation-binary-lower-bounds.md) |
| 4 | [review-nonconvex-polynomial-binary-integer-gap-second.md](../notes/review-nonconvex-polynomial-binary-integer-gap-second.md) |
| 4 | [review-nonconvex-polynomial-binary-integer-gap.md](../notes/review-nonconvex-polynomial-binary-integer-gap.md) |
| 1 | [review-nonquadratic-integer-precision-second.md](../notes/review-nonquadratic-integer-precision-second.md) |
| 1 | [review-nonquadratic-integer-precision.md](../notes/review-nonquadratic-integer-precision.md) |
| 1 | [review-perspective-integer-precision.md](../notes/review-perspective-integer-precision.md) |
| 3 | [review-positive-polynomial-allocation-degree-gap-second.md](../notes/review-positive-polynomial-allocation-degree-gap-second.md) |
| 3 | [review-positive-polynomial-allocation-degree-gap.md](../notes/review-positive-polynomial-allocation-degree-gap.md) |
| 3 | [review-positive-polynomial-linear-shape-precision-second.md](../notes/review-positive-polynomial-linear-shape-precision-second.md) |
| 3 | [review-positive-polynomial-linear-shape-precision.md](../notes/review-positive-polynomial-linear-shape-precision.md) |
| 3 | [review-positive-polynomial-loglog-precision-second.md](../notes/review-positive-polynomial-loglog-precision-second.md) |
| 3 | [review-positive-polynomial-loglog-precision.md](../notes/review-positive-polynomial-loglog-precision.md) |
| 4 | [review-positive-polynomial-vector-refinement-obstruction.md](../notes/review-positive-polynomial-vector-refinement-obstruction.md) |
| 4 | [review-positive-polynomial-vector-refinement-second.md](../notes/review-positive-polynomial-vector-refinement-second.md) |
| 3 | [review-positive-separable-polynomial-precision-second.md](../notes/review-positive-separable-polynomial-precision-second.md) |
| 3 | [review-positive-separable-polynomial-precision.md](../notes/review-positive-separable-polynomial-precision.md) |
| 3 | [review-positive-separable-unconditional-precision-second.md](../notes/review-positive-separable-unconditional-precision-second.md) |
| 3 | [review-positive-separable-unconditional-precision.md](../notes/review-positive-separable-unconditional-precision.md) |
| 4 | [review-positive-vector-capset-integer-lower-bound.md](../notes/review-positive-vector-capset-integer-lower-bound.md) |
| 4 | [review-positive-vector-three-witness-integer-obstruction.md](../notes/review-positive-vector-three-witness-integer-obstruction.md) |
| 3 | [review-pure-power-degree-independent-count-second.md](../notes/review-pure-power-degree-independent-count-second.md) |
| 3 | [review-pure-power-degree-independent-count.md](../notes/review-pure-power-degree-independent-count.md) |
| 2 | [review-quadratic-ellipsoidal-output-precision.md](../notes/review-quadratic-ellipsoidal-output-precision.md) |
| 2 | [review-quadratic-general-norm-output-precision-second.md](../notes/review-quadratic-general-norm-output-precision-second.md) |
| 2 | [review-quadratic-general-norm-output-precision.md](../notes/review-quadratic-general-norm-output-precision.md) |
| 1 | [review-quadratic-inertia-one-sided.md](../notes/review-quadratic-inertia-one-sided.md) |
| 2 | [review-quadratic-l1-output-precision.md](../notes/review-quadratic-l1-output-precision.md) |
| 2 | [review-quadratic-ncrank-rational-construction.md](../notes/review-quadratic-ncrank-rational-construction.md) |
| 1 | [review-quadratic-noncommutative-rank-second.md](../notes/review-quadratic-noncommutative-rank-second.md) |
| 1 | [review-quadratic-noncommutative-rank.md](../notes/review-quadratic-noncommutative-rank.md) |
| 2 | [review-quadratic-nonlinear-input-rank-precision-second.md](../notes/review-quadratic-nonlinear-input-rank-precision-second.md) |
| 2 | [review-quadratic-nonlinear-input-rank-precision.md](../notes/review-quadratic-nonlinear-input-rank-precision.md) |
| 2 | [review-quadratic-precision-approximation-hardness-second.md](../notes/review-quadratic-precision-approximation-hardness-second.md) |
| 2 | [review-quadratic-precision-approximation-hardness.md](../notes/review-quadratic-precision-approximation-hardness.md) |
| 1 | [review-quadratic-rank-integer-complexity.md](../notes/review-quadratic-rank-integer-complexity.md) |
| 1 | [review-quadratic-vector-cross-product.md](../notes/review-quadratic-vector-cross-product.md) |
| 2 | [review-quadratic-weighted-covariance-precision-second.md](../notes/review-quadratic-weighted-covariance-precision-second.md) |
| 2 | [review-quadratic-weighted-covariance-precision.md](../notes/review-quadratic-weighted-covariance-precision.md) |
| 2 | [review-quadratic-weighted-precision-algorithm-second.md](../notes/review-quadratic-weighted-precision-algorithm-second.md) |
| 2 | [review-quadratic-weighted-precision-algorithm.md](../notes/review-quadratic-weighted-precision-algorithm.md) |
| 4 | [review-rational-polar-spanner-oracle-second.md](../notes/review-rational-polar-spanner-oracle-second.md) |
| 4 | [review-rational-polar-spanner-oracle.md](../notes/review-rational-polar-spanner-oracle.md) |
| 3 | [review-relative-power-graph-integer-obstruction.md](../notes/review-relative-power-graph-integer-obstruction.md) |
| 3 | [review-small-exponent-rational-formulation-barrier-second.md](../notes/review-small-exponent-rational-formulation-barrier-second.md) |
| 3 | [review-small-exponent-rational-formulation-barrier.md](../notes/review-small-exponent-rational-formulation-barrier.md) |
| 3 | [review-small-exponent-soc-formulation-separation-second.md](../notes/review-small-exponent-soc-formulation-separation-second.md) |
| 3 | [review-small-exponent-soc-formulation-separation.md](../notes/review-small-exponent-soc-formulation-separation.md) |
| 3 | [review-sparse-positive-polynomial-circuit-precision-second.md](../notes/review-sparse-positive-polynomial-circuit-precision-second.md) |
| 3 | [review-sparse-positive-polynomial-circuit-precision.md](../notes/review-sparse-positive-polynomial-circuit-precision.md) |
| 3 | [scalar-convex-graph-two-bit-gap.md](../notes/scalar-convex-graph-two-bit-gap.md) |
| 3 | [shared-prefix-rational-interpolation-gadget.md](../notes/shared-prefix-rational-interpolation-gadget.md) |
| 3 | [small-exponent-rational-formulation-barrier-novelty.md](../notes/small-exponent-rational-formulation-barrier-novelty.md) |
| 3 | [small-exponent-rational-formulation-barrier.md](../notes/small-exponent-rational-formulation-barrier.md) |
| 3 | [small-exponent-soc-formulation-separation-novelty.md](../notes/small-exponent-soc-formulation-separation-novelty.md) |
| 3 | [small-exponent-soc-formulation-separation.md](../notes/small-exponent-soc-formulation-separation.md) |
| 3 | [sparse-positive-polynomial-circuit-precision-novelty.md](../notes/sparse-positive-polynomial-circuit-precision-novelty.md) |
| 3 | [sparse-positive-polynomial-circuit-precision.md](../notes/sparse-positive-polynomial-circuit-precision.md) |

## Open boundaries and scope

- Stage 1 leaves rank-changing smooth scalar maps and vector maps with unequal local/global ranks uncharacterized; the manuscript states this explicitly. It proves constant-rank scalar and positive-perspective cases.
- Stage 2 supplies the complete polynomial-bit proof of equation `eq:rational-rate-preview` in thm:rational-ncrank, including the exact input-denominator lower bound and the imported rational algorithm/capacity constants; accepted at the stage 2 gate after fifteen reviews and a separate correction pass.
- Preserve distinctions among real-coefficient existence, polynomial continuous size, rational encoding size, construction time and MILP solution time. Some source notes use `p_bin` for arbitrary convex binary lifts; the manuscript uses binary linear lifts and must explicitly state when a lower bound holds for the larger binary class.
- The error-body definition in stage 1 is a compact convex full-dimensional body symmetric about the origin. Stage 2 explicitly extends the convention for grouped-PSD budgets with unmeasured directions in sec:quadratic-bodies; stage 4 prop:conditioning explicitly extends its finite inner/outer-ball comparison to nonsymmetric compact convex permitted-error sets. The symmetric compact-body definition remains the default elsewhere.
- Do not flatten shape-adapted scalar guarantees into the earlier coefficient-sum allocation benchmark; their gap example is a distinct development.
- The necessity of all logarithmic output/curvature-rank overheads is not established merely by the available upper bounds. Keep the exact convex polynomial separation and the nonconvex polynomial separation with their different hypotheses.
- A source comparison should credit parity, disjunctive formulations, McCormick/sawtooth constructions, matrix-space rank/capacity, oscillatory analysis, affine fibers, geometric optimization, barycentric spanners and circuit compilation as established ingredients. Literature priority remains subject to a bounded source audit.
- Final coverage was cross-checked against the manuscript statements, proofs and source content during the stage and whole-paper reviews. All 273 links and 119 explicit theorem/equation/section mappings checked by the root audit resolve. The gate-status update changes no mathematical mapping.

## Vector coverage

All ten canonical stage 4 results and all eleven explicit supporting developments are drafted in `sections/04-vector.tex`. The introduction, abstract and conclusion synthesize the accepted stages with this new material. Stage 4 passed its fifteen-reviewer gate with no reviewer findings and one separately corrected root layout finding. Coverage and review remain bounded evidence, not a correctness certificate. The finite one-input constant-gap question, rank-changing smooth boundary, and mixed-coordinate vector extension remain explicitly unresolved. The stage 4 source index contains promoted pointers and predecessor variants; substantive hinge geometry and Bernstein stability are retained, while alternate numerical constants for the same degree-32 argument are superseded by the exact product-count theorem. Primary method credit includes shared SOS2 overlays, barycentric spanners and their approximate-oracle predecessors, GLS anti-blocker access, proportional-fair allocation, cap-set estimates, difference-of-convex geometry and mixed Helly scope.
