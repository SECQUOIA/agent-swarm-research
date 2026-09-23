# Stage 3 independent review 5

**No supported major or minor finding.** I read the entire frozen `reviews/revision-stage3-round1/source/sections/03-scalar-nonlinear.tex` (1,593 lines), including every proof, example, implementation argument and unnumbered estimate. I compared the section and bibliography with the frozen stage 2 versions and read the author and literature records. I checked the dependencies on the representation definition, parity, finite disjunction, covariance volume bound and allocation machinery reviewed in stage 2. I did not consult other stage 3 reviewer reports or edit manuscript sources.

The stage passes this review. This is a substantive review, not a guarantee against every possible future criticism.

## Mathematical coverage and critical checks

The full reading covered scalar chord partitions and packing; truncated curvature mass and the high-degree example; indexed endpoint circuits, certified integration and mass inversion; the seven-bit and eleven-bit compilers; Jensen superadditivity, feature curves and separable budgets; positive-polynomial allocation and dense/sparse construction; convex powers, positive rational approximants and binary-exponent evaluation; relative-error obstructions; and the root-graph MILP–MISOCP encoding separation.

I checked particularly:

- The distinction between a real-coefficient existence result and a polynomial-size rational compiler. Internal circuit wires are forced only after fixing input bits; weighted endpoint products introduce no additional integer variables. Common denominators and endpoint rounding are accounted for.
- The truncated-mass estimates at the endpoint, including `E <= m^2 + 3m/2` and the reverse bound, and the use of mass accuracy rather than coordinate accuracy for approximate inverse knots. Slightly out-of-range target masses and nonmonotone neighboring computed knots do not break graph coverage or the local error bound.
- Polynomial subdivision depth and panel count in certified integration, including repeated roots, square-free preprocessing, and Gaussian-node/weight precision. The hybrid construction's rounded/coalesced partition and the stopping alternative give the stated `1458 * 2^p < 2048 * 2^p` segment comparison.
- The separable packing volume constants and positive-allocation supporting weights; the degree normalization in the covariance transformation; binary rational exponents near one; and the explicit distinction between polynomial dependence on numerical degree in the Stieltjes construction and polynomial dependence on exponent bit length in the separate evaluator.
- The MILP denominator argument after freezing an arbitrary integer witness: witness size affects right-hand sides, while the determinant bound uses the fixed continuous coefficient matrix. In the conic value gadget, the zero-weight case is justified. The repeated-square primal/dual certificate cancels correctly, and its long witness coordinates are not counted as formulation coefficients. The concluding separation explicitly requires exact cone feasibility and makes no numerical stability claim.

These checks did not reveal a gap or a count/encoding inconsistency.

## Primary-source and attribution checks

I followed `literature/AGENTS.md`; author records supplied leads, not the evidence for conclusions.

- **LinA (2025):** inspected the published local text, Proposition 1/Corollary 1, Remark 3, Section 4.1 and Lemma 4. The revised comparison correctly credits greedy optimal segmentation and continuity for convex corridors, and scopes logarithmic oracle cost to one maximal segment. It does not portray continuity or greedy splitting as new. Local passages: [[codsi2025-lina-a-faster-approach-to]] p.7-8, p.10-12, p.17-18.
- **Sagraloff–Mehlhorn:** checked Theorem 36 in cached `build/source-cache/sagraloff2015.txt`, printed p.41, against the explicit [arXiv v2 record](https://arxiv.org/abs/1308.4088v2). The square-free integer-polynomial refinement theorem supports the imported polynomial precision bound. Published volume/pages/DOI were cross-checked with [the author's institutional publication listing](https://www.mpi-inf.mpg.de/people/mehlhorn/). Direct publisher full-text access failed, but the manuscript accurately identifies the preprint as the theorem-number basis rather than implying identical journal numbering.
- **Adams–Henry:** inspected the cached SAND2012-0505P manuscript, Section 2, and the [publisher record](https://pubsonline.informs.org/doi/10.1287/opre.1120.1106). The 2012 journal metadata and explicit author-manuscript locator are correct. Discrete-function encoding and multiplication by a nonnegative continuous weight are established antecedents.
- **Circuit and numerical antecedents:** inspected Avis et al., Section 3/Lemma 1, for unique fixed-input circuit extensions; DLMF Section 3.5(v) for Gaussian quadrature; and Bonito–Pasciak, Section 3.3/equation (37)/Lemma 3.4, for positive resolvent quadrature. The manuscript proves its additional endpoint, precision and formulation claims locally and does not attribute those stronger claims to these sources.
- **Conic antecedents:** inspected [Boyd–Vandenberghe](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf), Section 5.9, printed pp.264–267; O'Donnell's local Section 2 discussion of long SOS solution encodings; and Wang's Section 4, Theorem 18/Corollary 21, on short geometric-mean cone descriptions. These support the closing attribution. The fixed-error, same-binary-count graph separation is stated as the particular result proved here, without claiming that conic power lifts or long feasible encodings are themselves new.

The new opening and endpoint explanations improve standalone readability. The section's contribution statements remain scoped to its proved comparisons and constructions; no broader priority assertion is introduced. No additional required editorial correction or optional preference arose from this review.
