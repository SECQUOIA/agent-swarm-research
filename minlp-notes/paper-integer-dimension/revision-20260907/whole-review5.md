# Independent whole-manuscript review 5

Reviewed the frozen manuscript in `reviews/revision-whole-round1/source` on September 7, 2026. No manuscript edits were made. No reviewer reports, adjudications, or acceptance records were read.

**Major findings: none. Minor findings requiring correction: none.** I found no supported mathematical, scientific-integration, attribution, or standalone-completeness defect. No required revision is identified by this review.

## Complete manuscript coverage

I read all nine TeX files and the complete bibliography: 6,646 source lines, including the abstract, introduction, all six section files, conclusion, main document, macros, and all 44 bibliography entries. No manuscript source scope remains unread. The section files contain multiple numbered sections; the review covered every theorem, lemma, proposition, example, proof, and intervening discussion, rather than only the six file boundaries.

The mathematical audit followed these full dependency chains:

- Arbitrary convex lifts, projected sections, closed parity contacts, residue combinations, finite disjunctions, shared prefixes, square/product constants, fractional covers, scalar rank and one-sided inertia.
- Principal compression over the involutive division ring, real symmetric shrinking, covariance fourth moments, determinant/volume estimates, the noncommutative-rank law and cross-product example, rational rank certificates, smooth oscillatory lower bounds, constant-rank tubes, and perspectives.
- Finite covariance bounds, geodesic convexity, residual certificates, rational Jacobi rotations, matrix-function conditioning, actual-iterate convergence and rounding, feasibility repair, grouped and absolute-sum budgets, effective output and input reductions, positive blocks/diagonals/features/forests, domain-volume restrictions, and Max-Cut amplification.
- Scalar chord refinement and packing, truncated curvature mass, signed-polynomial integration panels and quantile computation, Boolean endpoint compilation, the eleven-bit hybrid, separable packing, positive allocation scalarization, sparse powers, rational exponents, relative-error residues, root encoding, and homogeneous primal-dual conic gadgets.
- Ordered implicit overlays, original-output curvature bases, fixed-grid feasible spanners and positive-polar access, explicit effective-image bands, common separable bases, scalarization and cap-set obstructions, exact product counts, nonconvex polynomial and tilted-body separations, conditioning bounds, and the remaining one-input question.

In particular, I checked that the construction proofs retain the whole exact graph, that implied Boolean wires need no extra integrality declarations, that common-denominator bounds survive implicit indexing, and that error-body restrictions and dense/sparse/binary-exponent models match each invocation. The different meanings of noncommutative rank, common nonlinear input rank, and curvature rank are stated and used consistently. The introduction and conclusion accurately reflect the theorem hypotheses and limitations.

An independent source audit found 258 distinct labels, no duplicate labels, no missing cross-references, no missing citation keys, and no uncited bibliography entries. Text extraction of `build/main.pdf` found 87 pages and no unresolved `??` markers. This was a complete source review, not a complete visual inspection of all rendered PDF pages.

## Primary evidence and novelty assessment

I independently inspected the relevant original PDF passages, rather than relying on author or literature-summary conclusions:

- Lubin–Vielma–Zadik, Definition 4.3 and Lemma 4.1: the paper correctly acknowledges existing MICP rank and its parity obstruction while distinguishing minimization over graph relaxations and nonclosed lifts. [[lubin2022-mixed-integer-convex-representability]] p.11-12.
- Ivanyos–Qiao–Subrahmanyam, Theorem 1.5 and Lemma 5.3: rational polynomial-bit shrunk-subspace output and field-extension invariance support the stated algorithmic import. [[ivanyos2018-constructive-non-commutative-rank-computation]] p.7, p.16.
- GGOW, published PDF `build/source-cache/ggow2020.pdf`, Theorems 1.17 and 2.18, PDF pages 10 and 29: the rank characterization and integral capacity bound support the quadratic proof, including the denominator scaling exponent.
- GLS, original PDF and text in `build/source-cache/gls1981.*`, Definition (5), weak-separation convention, and Theorem (3.1); DPV, `dpv2011.pdf`, Theorem B.5, PDF page 39; Zhang–Sra, `zhang-sra2016.pdf`, Corollary 8, PDF page 8. These support the weak-optimization guarantees, rounding factor, and geodesic recurrence actually used.
- Sagraloff–Mehlhorn, `sagraloff2015.pdf`, Theorem 36, PDF page 41; Awerbuch–Kleinberg, `awerbuch2004.pdf`, Propositions 2.2 and 2.4, PDF page 4; Del Pia, `delpia2026.pdf`, Theorem 2. The manuscript presents these as established ingredients and supplies its own application-specific precision accounting.
- Beach–Hildebrand–Huchette, Section 2.1 and Proposition 1, original PDF pages 4–5; Lyu–Hicks–Huchette, Proposition 1, original PDF page 7; Codsi–Ngueveu–Gendron, Proposition 1, Section 4.1 and Remark 3, original PDF pages 7, 9–10. These support the acknowledged square formulation, common SOS2 interpolation, maximal segmentation, and continuity antecedents.

The distinction from prior work is substantive: the main assertion compares the minimum integer count over every admissible convex lift with a matching binary linear construction. Existing matrix-space algorithms, PWL encodings, greedy partitions, and spanners are not presented as inventions of this manuscript. The novelty claim is properly concentrated on the joint quadratic coefficient and the precise finite comparison/encoding theorems.

Targeted online searches for the joint noncommutative-rank/graph-approximation claim and convex integer-dimension approximation did not identify an earlier matching characterization. This is evidence from a bounded search, not proof that no earlier result exists. Current primary records also support the recent bibliography versions: [Schade–Sinha–Weltge](https://link.springer.com/article/10.1007/s10107-025-02234-z) has the stated 2026 volume/pages despite 2025 online publication; [Lyu–Hicks–Huchette](https://pubsonline.informs.org/doi/10.1287/opre.2023.0187) appears in the January–February 2026 issue, with 2025 online publication; [Del Pia](https://arxiv.org/abs/2607.29386) was submitted July 31, 2026. The manuscript explicitly pins preprint theorem numbering where needed.

All bibliography entries were read, but not every cited original was read in full or independently revalidated. The primary checks above concentrate on the closest work and the external mathematical/algorithmic imports. I did not execute the proposed algorithms or claim a formal machine verification of the proofs.

## Preferences, separate from findings

The breadth and 87-page length may affect journal placement, but I do not regard length alone as a scientific defect or a reason to split the requested standalone paper. The existing overview, prior-work table, scope statements, and local notation make its structure navigable. No cosmetic preference is promoted to a required change. Blank author and date fields are intentional and were not treated as defects.
