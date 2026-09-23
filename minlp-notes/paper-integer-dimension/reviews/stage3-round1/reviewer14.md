# Stage 3, round 1 — reviewer 14

Major findings: 0

Minor findings: 0

No concrete defect requiring correction was identified in this review. This is a bounded mathematical and source assessment, not a correctness guarantee or a finding of publication priority.

## Scope and snapshot

I read the entire `sections/03-scalar-nonlinear.tex` (lines 1–1564), the task and lens instructions, process and protocol, bibliography, and coverage inventory. I independently reconstructed the arguments throughout the stage. I reread the accepted foundation interfaces for parity contacts, finite disjunctions, binary products and covariance volume, and the accepted block log-determinant allocation proof, including its scalar specialization and exact central-ball feasibility repair. Earlier stages had also been reviewed in full in my preceding assignments.

I compared the eleven stage-3 canonical result statements and their distinct development requirements with the manuscript, and checked the thirteen explicitly substantive supporting developments. These comparisons used the original result/note texts, not merely the coverage labels. Primary-source checks used the extracted primary texts in the source cache and local literature, after reading `literature/AGENTS.md`, and the official DLMF page. The root source audit was a lead to relevant passages, not evidence that a mathematical step was correct.

All seven frozen-file SHA-256 hashes matched the snapshot, both initially and immediately before this report:

| File | SHA-256 |
| --- | --- |
| `coverage.md` | `19ccd1e2bea4439da83da8959d8d1bb59d172efa6e4160b40d80722def385ec5` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `e662d0747e850fe23c3625c0cd6e9fe39d1bc370223f2f8c4b2659095cbea599` |
| `references.bib` | `d1c9428ba522987e3709b9d902163ae99ee940d8ec6fb781bf04255f3d23aa80` |
| `sections/01-foundations.tex` | `3108dc02b31b4812fe7fffb444e637a2c846e00268d750262e363dfdb1ded37e` |
| `sections/02-quadratic-finite.tex` | `0a81bba6f3635323663fb347f74face34c2aadb2ba0993b8a1d6465e9f8fdbd3` |
| `sections/03-scalar-nonlinear.tex` | `dbd488d7fa1d3e377f57bea9f48f8391e5b153b827e4d4caf62e9aa0c3bc66be` |

## Mathematical checks

1. **Scalar geometry and curvature.** Reconstructed the three-way refinement of a concave chord gap, the passage from parity-support spans to chord covers, and the finite maximal incompatible packing. These establish the two-bit comparison for binary *linear* lifts. Checked the truncated mass estimate, its local Taylor-remainder bound, and the potential argument yielding the factor 24. The positive-polynomial example separately demonstrates the raw-arclength failure at fixed accuracy and the allocation gap at accuracy depending on the family parameter. Its quantifiers do not conflict with fixed-function high-accuracy interpolation asymptotics.

2. **Certified integration and compilation.** Checked cutoff and branch-root losses, the signed-coefficient Taylor-panel certificate, and why root separation bounds refinement depth without requiring an exponentially large uniform mesh. The count of failed panels at each depth uses proximity to a polynomial root, rather than the smallest root distance as a global mesh width. Checked the analytic quadrature remainder, positive-weight rational approximation, and the explicit inverse modulus. For mass-accurate compilation, checked targets slightly beyond the actual total mass, common dyadic output precision, exact endpoint overrides, and reversed or duplicate knots. The continuous endpoint path still covers the domain. The chord and rounding slack gives the claimed graph containment and admitted-error bound. The Boolean compiler forces internal wires only after the declared input bits are fixed; it does not require those wires to be separately integral.

3. **Arbitrary convex polynomials and separable comparisons.** Reconstructed the rounding comparison with an optimal finer partition, the exact chord-error decision and greedy dominance argument, and the implication from failure to finish within the cell cutoff to a sufficiently large true chord count. Checked the accounting for derivative-root brackets and reflected monotone-curvature pieces in the hybrid branch. Reconstructed Jensen-gap superadditivity and the product-packing deletion bound used for scalar sums; independent outputs have their separate product lower bound. The dense positive and arbitrary dense convex cases keep their stated different constants.

4. **Positive mixtures and allocation.** Checked the coefficient-sum baseline and the stronger supporting scalarization. A small positive allocation supplies the required constraint qualification; coordinate-cap normals explain the inactive-cap terms. Zero scalarized coordinates are handled, and the homeomorphisms are used on the whole cube, without an inappropriate Jacobian-volume transfer. Unconditional domination turns the coordinate bounds into valid output bands. The accepted scalar allocation oracle gives exact rational feasibility with the stated product loss. Checked the endpoint layers, common selectors, exact prefix powers, and the sparse replacement by rounded binary exponentiation. Numerical-degree and exponent-bit complexity are distinguished.

5. **Pure powers and rational inverse constructions.** Checked the finite power-coordinate lower and upper bounds, including the curvature scale for exponents between one and two. Reconstructed the Stieltjes tails, uniform complex-panel estimate, positive rationalization and normalization at one. Its size bound depends polynomially on numerical degree. Checked the general signed-numerator rational endpoint recurrence with a supplied positive denominator certificate, including zero weight and zero index bits. The reciprocal construction reuses existing bits and bounds all reciprocal variables. The integer inverse-power bisection has a justified uncertainty exit; the rational-exponent logarithm/exponential implementation uses polynomial precision in exponent encoding. Endpoint perturbation and interpolation errors fit the stated unconditional bands.

6. **Relative error and encoding separation.** Reconstructed the modulus-residue arguments for convex and concave powers, their distinct tolerance thresholds, and the doubly logarithmic truncated-domain count. For the root-graph MILP barrier, fixing an unbounded integer witness alters only the right-hand side; the basis denominator remains controlled by the original coefficient encoding. Checked why minimizing the input under the additional output threshold has a positive attained optimum. Reconstructed the conic-value gadget at both positive and zero weight, and the explicit repeated-squaring primal/dual certificates. The short MISOCP is an exact-feasibility representation; no conclusion about stable numerical extraction is silently used.

## Coverage comparison

All eleven canonical stage-3 developments are present:

| Canonical development | Manuscript evidence |
| --- | --- |
| Accuracy-dependent curvature precision | `thm:curvature-mass`, local remainder, positive-degree example |
| Compiled curvature quantiles | `lem:certified-curvature`, `thm:compiled-curvature` |
| General dense convex polynomial compiler | `thm:convex-hybrid`, large-grid and monotone-piece proof |
| Positive-polynomial double-logarithmic degree bound | `thm:positive-loglog`, supporting normal and layer curvature |
| Positive pure-power compact linear construction | `prop:pure-power-finite`, `lem:stieltjes-power`, `thm:reciprocal-powers` |
| Positive separable polynomial baseline | `prop:positive-baseline`, exact prefix powers and feature Jensen bound |
| Unconditional positive-separable allocation | Positive allocation oracle and unconditional lower/upper arguments |
| Binary rational exponents | `lem:inverse-power-index`, `thm:rational-powers`, scaled power geometry |
| Scalar sums and independent convex outputs | `lem:jensen-superadditivity`, `thm:separable-scalar`, product packing |
| Small-exponent MILP/MISOCP encoding separation | `thm:root-encoding`, `lem:conic-value`, `thm:root-conic-separation` |
| Sparse positive-polynomial compiler | Rounded evaluation lemma and sparse proof of `thm:positive-loglog` |

The supporting-content comparison also located both positive and signed monotone integration algorithms; the general indexed-knot compiler; raw-curvature and allocation obstructions; feature-curve geometry; the full rational Stieltjes argument; the finite pure-power/source distinction; the rational log-product oracle in accepted stage 2; relative-power obstructions; the scalar two-bit lemma; the small-exponent rational encoding barrier; and the general shared-prefix signed rational interpolation gadget. Superseded baseline bounds retain their distinct mechanisms. The source-assessment note is represented by appropriately bounded predecessor credit, rather than imported as a priority theorem. Later coupled-vector and exact-gap developments are explicitly outside this stage and were not marked missing.

## Primary-source scrutiny

- **Sagraloff–Mehlhorn:** inspected the primary preprint's Theorem 36 and its surrounding input model in `build/source-cache/sagraloff2015.txt`. It supplies polynomial bit complexity for isolating/refining integer-polynomial real roots. Denominator clearing and square-free preprocessing reconcile the manuscript's rational polynomial applications with that input model. The manuscript separately proves the analytic-panel and arithmetic-precision work that root isolation alone does not supply.
- **DLMF:** directly checked positive Gaussian weights and degree `2n-1` exactness in [NIST DLMF §3.5(v)](https://dlmf.nist.gov/3.5#v), equations 3.5.18–3.5.20_1. These are precisely the classical quadrature facts used. Certified rational node/weight precision is justified in the manuscript instead of being inferred from a numerical quadrature table.
- **Simchowitz et al.:** checked Lemma 2.1 in `simchowitz2018.txt`; its convex-function midpoint-versus-maximum secant-gap inequalities match the limited credit at manuscript lines 66–70. It is not presented as the source of the new whole-lift count comparison.
- **Avis et al.:** checked Section 3 and Lemma 1 in the local primary full text. Boolean circuit inputs uniquely force Boolean gate outputs under the displayed linear inequalities. The manuscript's conditional-wire compiler is consistent with this antecedent and proves its additional endpoint/interpolation interface.
- **Adams–Henry:** checked Section 2 in `adams2012.txt`, including the binary-code convex-combination observation and discrete-function representation. The manuscript accurately credits base-2 discrete-function/product representations and does not attribute its polynomial random-access compiler size bound to an explicitly enumerated table construction.
- **Codsi–Ngueveu–Gendron:** checked the primary report's greedy maximum-segment and dichotomic constructions. Its cautions about general continuous piecewise-linear greedy schemes do not invalidate the manuscript's more restricted convex-chord argument, which is proved locally. The cited report number, authors and title match the primary document.
- **Teles–Castro–Matos:** checked the primary article's metadata and stated power-based/disaggregation mechanism. The 2013 journal volume 55, pages 227–251 and DOI match; its earlier online date does not create a bibliography discrepancy. The manuscript gives predecessor credit for the established mechanism without assigning it the present arbitrary-convex-lift lower comparison.
- **Bonito–Pasciak:** inspected Section 3.3, equation (37), Lemma 3.4 and its uniform positive spectral-parameter hypothesis in `bonito2015.txt`. Substitution `lambda=1/t` gives positive resolvent sums for positive `t`; both target and approximants extend by zero at `t=0`. The citation supports the stated precedent. The manuscript supplies its own rational coefficients, endpoint normalization and degree-dependent bounds.
- **Conic context:** inspected the local O'Donnell and Wang primary texts for the short-conic/long-solution and rational-power SOC contexts. Their uses at the end of the stage are contextual, not imported assertions of the present fixed-error four-binary separation. The explicit conic-value and squaring-chain proofs carry the mathematical obligation.

No unsupported claim that these numerical, interpolation, disaggregation or conic tools are newly invented was found. The distinction between an established ingredient and the resulting whole-graph integer-count guarantee is maintained.

## Findings and limits

There are no numbered correction findings or unresolved questions from this review. I did not independently rerun the supplementary numerical scripts, rebuild or visually inspect the PDF, formally verify the proofs, or perform an exhaustive external novelty search. The source comparison is limited to the consequential cited passages and the stated predecessor relationships. The original canonical and supporting notes were compared for statements and distinct content; the independent full proof reconstruction was of the manuscript, rather than a reread of every historical audit. These limits do not convert the no-findings assessment into a priority or publication-readiness claim.
