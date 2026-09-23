# Stage 1 round 1 — reviewer 07

Primary lens: smooth maps, matrix evaluations, oscillatory estimates, and local versus global ranks.

Major findings: 0
Minor findings: 2

I found no major defect in the mathematical arguments reviewed. In particular, the smooth lower bound uses a valid oscillatory estimate on Cartesian powers, and both the smooth global-span upper bound and the constant-rank scalar upper bound retain the required domain and graph-containment conditions. This assessment is subject to the verification limits below; it is not a claim of formal verification or established publication priority.

## Snapshot and coverage

I checked the following SHA-256 values against `reviews/stage1-round1/snapshot.json`; all five matched:

| File | SHA-256 |
| --- | --- |
| `sections/01-foundations.tex` | `075e0e998e9cf3e9bdf0830fde1822876ac272bb336eec5d10374425ace92e03` |
| `references.bib` | `bc7fbcf1dad163b2e1064e787760f7f76b88ba649c3f6657d3a46d9432a433da` |
| `coverage.md` | `a5b675009a1c889bf93105e5b1121f2d5de5fac732d414c4b0b71563e1ce7727` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `cecaea518c089ff3beca3edf14ec879129f947f67ed01af7ef3602fb74ea571e` |

I read `PROCESS.md`, `reviews/PROTOCOL.md`, the stage task and lenses, the snapshot, the full 1,206-line stage, its bibliography, macros, main file, and coverage inventory. I independently followed all stage proof chains, including parity closure, finite disjunction, square/product constants, graph allocations, indefinite-volume and covariance estimates, symmetric shrinking, principal compression, one-sided constructions, smooth ranks, constant-rank fibers, and perspective transfer.

For source comparison I read the complete original smooth-map, constant-Hessian-rank, and perspective results, the relevant algebraic and construction sections of the original noncommutative-rank result, and the nonquadratic investigation note. I also inspected the second smooth audit and the constant-rank audit after checking the manuscript arguments independently. Those audits were not treated as proof.

Primary-source checks used the cached GGOW published text (Theorems 1.4 and 1.17, capacity discussion and Theorem 2.18), Wolff's Theorem A and proof on printed pages 50–51, and Nicola's Definition 1.1 and following paragraph. The latter two confirm the analytic hypotheses and constant-rank affine-fiber attribution used here. I did not independently retrieve Hörmander's original paper, recheck every bibliographic entry, audit all later-stage source files, or compile and visually inspect the PDF. The rational bit-complexity preview is explicitly deferred; I did not treat its unwritten stage-2 proof as a stage-1 omission.

## Findings

1. **MINOR — repeated malformed multiplication in the smooth upper proof.** Location: `sections/01-foundations.tex`, lines 974, 977, and 992, proof of `thm:smooth-ranks`. The text has `C_0,2^{-T}` and `2C_0,2^{-T}`. A literal comma is printed between the constant and the power, so the central error bound is malformed. The mathematical argument establishes the product `C_0 2^{-T}`: every nonzero Hessian term has coordinate-width product at most a fixed constant times `2^{-T}`. Replace these commas by spaces or `\,`. This is a typesetting defect, not a false estimate or proof gap.

2. **MINOR — the citation locator for the capacity equivalence omits the relevant part of GGOW.** Location: lines 529–541, especially the introductory citation to GGOW Theorems 1.4 and 1.17 preceding `eq:capacity`. Theorem 1.4 supplies the singularity/matrix-evaluation/shrinking equivalences; Theorem 1.17 supplies the rank/decomposability characterization. Neither displayed theorem states the positive-capacity equivalence. GGOW discusses that result separately as Gurvits' ingredient in Section 1.5 and develops capacity in Section 2. The original repository result includes Section 2 in its source pointer and explicitly credits the equivalence to Gurvits. Add a separate capacity citation to the appropriate discussion or original theorem, and retain that attribution. This is an inaccurate source locator, not an objection to the true equivalence or to the subsequent covariance argument. The direct Hall/permanent proof also independently supports the qualitative precision coefficient.

## Mathematical checks with emphasis on the primary lens

- At the repeated base point, the phase in `lem:smooth-volume` has mixed Hessian `-(1/2) sum_j B_j tensor Hess f_j(x_0)`, with the stated block ordering. Real matrix evaluations follow from nonvanishing of a real-coefficient determinant polynomial; symmetry of the evaluation matrices is unnecessary.
- The local oscillatory proof compares every mixed Hessian with one fixed invertible matrix before averaging along segments. This justifies the lower bound for the phase-difference gradient. Repeated integration by parts and Schur's test then give the stated `lambda^{-N/2}` norm, with constants independent of the contact set and accuracy.
- On `S^d times S^d`, the chosen frequency makes the real part of the exponential positive. The operator bound compares `v^{2d}` with `epsilon^{nd/2} v^d`; division and the `d`th root yield exactly `epsilon^{n/2}`. No regularity, convexity, or aspect-ratio condition on `S` is missing.
- For partial local rank, the principal compression yields an actual affine slice through an interior point, so the compact parity cover can be restricted to a positive-volume box on that slice.
- The general smooth upper proof intersects cells with the transformed original domain and puts each Taylor center in that intersection. Thus its Taylor segments stay where the Hessian zero pattern is known. For polynomials, vanishing of forbidden Hessian entries on an open set extends that structure to the larger box needed for the prefix construction.
- The polynomial compiler only multiplies existing bits with other bits and at most one bounded residual. Its continuous AND variables are forced to be binary-valued at integral input bits, so their exact bounded products require no new integer declarations.
- The constant-rank proof derives affine fibers in the original coordinates. Its Taylor bound holds on the whole tube, and the neighborhood assumption supplies uniform derivative bounds even for chart points outside the original box. The finite cover and intersection with the box preserve polyhedrality.
- The norm and quadratic-over-linear examples correctly distinguish local rank from global-span rank. The stated limitations do not claim a general characterization when those ranks differ.

Executed check: `python code/quadratic_rank/check_smooth_polynomial.py` passed. I inspected that script before running it. It checks the quartic example's rank-three Hessian, forbidden zero blocks, and all twelve Taylor-remainder terms having precision weight at least one. This supplements the proof and does not verify arbitrary smooth maps.

No manuscript, bibliography, original research, or other review report was edited.
