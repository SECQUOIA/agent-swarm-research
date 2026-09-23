# Whole-paper round 01 — independent review 13

**Verdict: PASS.** No major or minor finding requiring repair. The additional coverage/development focus did not narrow this review to selected chapters.

## Coverage

Reviewed the frozen target `process/snapshots/whole-round01/main.pdf`, 111 pages, SHA-256 `912de166731f56368a8ee4db21294aa348b85364e85cd444e31265b29828d084`. Read the complete mathematical source, every proof and appendix, introduction, abstract, synthesis, macros and bibliography. Specifically:

- `main.tex`, `macros.tex`, `references.bib`;
- `sections/01-foundations.tex`, `02-universal-positive.tex`, `03-cubic-equal-means.tex`, `04-incidence-interiority.tex`, `05-feedback-frequency.tex`, `06-treewidth-two.tex`, `07-positive-boxes.tex`, `08-exact-complexity.tex`;
- `sections/09-cardinality-spatial.tex`, `10-cardinality-preordering.tex`, `11-coordinate-domains-lifts.tex`, `12-relative-blocks-cuts.tex`, `13-xor-quadratic-hulls.tex`, `14-monomial-reformulations.tex`, `15-finite-certificates-affine.tex`, `16-supporting-comparisons.tex`, `17-synthesis.tex`;
- `sections/appendix-finite-signings.tex`, `appendix-positive-couplings.tex`, `appendix-cubic-certificates.tex`, `appendix-structural-auxiliary.tex`, `appendix-positive-box-predecessors.tex`, `appendix-point-packing.tex`, `appendix-scaling.tex`, `appendix-p-split.tex`, `appendix-rank-one.tex`, `appendix-fbbt.tex`, `appendix-integer-comparison.tex`.

Read the frozen `process/review-protocol.md`, `whole-paper-review-assignment.md`, `scope-proposal.md`, `claim-coverage.md`, `stage-06-author.md`, `stage06-corrections.md`, `stage06-reviewer-focus.json`, and frozen `README.md` and `PROCESS.md`. Also read the paper-local development summary and the coordinatewise-lift/order-one refinement records. Historical acceptance labels were not treated as mathematical premises. No report from this final round was read; no delegation was used.

For the coverage focus, compared every required scope row with the coverage ledger and the actual manuscript arguments. Read the repository research closeout, continued-research closeout and open-thread audit, plus these development notes in full: `multilinear-second-order-investigation.md`, `multilinear-treewidth-three-investigation.md`, `positive-box-rho-plus-two-proof.md`, `review-positive-box-balanced-orientation-closure.md`, and `multilinear-frequency-two-positive-box-investigation.md`. These comparisons check that completed results are present and that exploratory or superseded statements are not presented as established conclusions. This was not a fresh line-by-line rereading of every historical repository file, nor an attempt to incorporate unrelated repository topics.

Read `literature/AGENTS.md` before consulting originals. Targeted primary-source checks included:

| Source | Passage inspected and use |
| --- | --- |
| Luedtke–Namazifar–Linderoth, local original and extracted text | Author-manuscript Conjecture 1, PDF p.22; common-upper Theorems 4–5 and coloring Theorem 8 in extracted text. The conjecture has the positive-coefficient/nonnegative-box scope used here. |
| Davidson–Donsig, local original | PDF pp.3–7: Theorems 1.1–1.2 and 2.3–2.4, real Grothendieck convention, continuous weighted density parameter and the `2M` upper bound. |
| Cornuéjols, saved author original | Fresh direct extraction of Theorems 6.5 and 6.13 and surrounding arguments. Eulerian-submatrix TU and mixed unit-right-hand-side balanced integrality are different statements, as the manuscript says. |
| Hassin–Tamir, saved original | PDF pp.3–4, printed pp.381–382, visually inspected because text extraction returned no usable content. Theorem 3.1 gives the block characterization; the subsequent paragraphs define two-terminal series/parallel construction. |
| Schoenebeck, saved full original | Fresh direct extraction of Definition 10, Theorems 11–12, Lemma 13 and its full character-vector proof, PDF pp.7–11. Checked density eight, positive width constant, resolution closure and width-to-square-degree accounting. |
| Altschuler–Boix-Adserà, local full text | PDF page marker p.55, Section 7.2, Theorem 7.4 and the following open question, plus the input-model paragraph. The manuscript correctly limits its negative accuracy result to rational bit complexity. |
| Kronqvist–Misener–Tsay, local published original | PDF pp.15–16, Definition 4, Theorem 6 and complete proof; minimal-sharing Assumption 3/Remark 1 in extracted text. The retained-domain counterexample addresses the actual universal statement. |
| Fawzi–Parrilo, local original | PDF p.3, Theorem 1 and Lorentz-cone decomposition: verified the fixed-block constants and the counted SOC resource. |
| Lee–Raghavendra–Steurer, local original | PDF p.23, Theorem 3.8/equation (3.11), and pp.32–34, Theorems 5.3–5.4 and displayed proofs. Verified the pseudo-density normalization, quantitative rank expression and the distinct shifted-slack consequence used here. |
| Belotti et al., local original | PDF p.14, Theorem 4.1 and the following infeasibility discussion. The frozen correction now includes its nonempty-limit qualification. |

These are direct source checks of the relevant statements, not claims to have audited every proof in every cited paper. Other classical dependencies, including sharp Khinchin, polynomial matching/optimization–separation, and the contextual source comparisons, were checked for consistency with the manuscript argument but not independently reproved from their entire primary literature. The manuscript's stated Coniglio-version and broader priority limits remain limits of this review as well.

## Findings

None. No repair is requested.

The complete scope comparison supports the current organization. The following boundaries are particularly important and are handled correctly:

1. The arbitrary-real-coefficient graph supremum, full-signing center value and induced-face signing optimum are distinct. The finite complete-graph computation is retained, including the nonmonotonic center optimum at seven vertices.
2. The exact dyadic cutoff, arbitrary-partition surrogate, general-radix cutoff and simpler large-radix formula are all present with their own assumptions and attainment arguments. Fixed-radix limitations do not become a universal second-order lower theorem.
3. The cubic lower endpoint is consistently the certified supremum bound `1610000/743033`; the upper bound is `31/12`. The actual convergence result for the two-level family is distinguished from the analytic family's lower certificates. The exact small-family threshold and all explicit finite witnesses are retained.
4. The fixed-ambient balanced law, its deterministic-coordinate restrictions and the coefficient-regularity consequence are completed proofs. Fixed-mixture optimality does not claim the exact physical-box optimum.
5. The full width-two active/blocking proof and TU consequence are retained. The stronger chordal-bipartite question and the width-three searches remain open or finite evidence. The `K_(3,m)` obstruction is correctly restricted to the all-cycle coloring mechanism.
6. The later unequal-aspect bipartite family approaching `3/2`, bipartite upper two and signed forest gluing are included. Common-aspect exactness is not silently transferred to unequal aspects.
7. The coordinatewise graph-lift result uses order `r` and affine endpoint interpolation, with full-graph objective agreement. The multivariable signed-monomial transfer instead uses source degree `4rD` and parity rank. The order-one extension and its separate upper certificate are present without weakening those assumptions.
8. Scaling cost separation uses the repaired catalogue membership and rectangularity hypothesis. The completed P-split ball and exact-image arguments are included; they are not left as proposed follow-ups.
9. Global lift size, integer precision, primitive propagation and spatial region counts remain different resources. Excluding the rest of the integer-dimension, pooling, Benders and process-network programs is consistent with the selected scope.

## Independent verification

All new files and copied-input build products are under `verification/reviewer13/whole-round01/`; only this report is outside that directory. No production manuscript or frozen input was edited.

### Proof reconstruction and attempted falsification

Reconstructed the vertex-law and deficiency argument, induced-cut localization, polarization constants, fractional orientation and random-sign lower bound. Checked zero effective support and fixed coordinates separately. For the harmonic law, checked normalization, inactive-mass loss, convex-tangent mixing, the Lambert correction and integer-parameter interpolation. For structural results, traced the ownership directions, repaired conditional local laws, fractional odd-cycle rank argument, baseline retention, series/parallel terminal cases and TU slab use. The scalar matching reductions keep signed dual costs and polynomial encoding bounds.

For the spatial results, checked the endpoint-avoidance cover count and strict below-target inequalities; the complete fractional-cardinality Gram identity and homogeneous reduction; assignment indicators with repeated slacks and possible zero weights; tensor positivity with total degree; and both kinds of graph substitution. In the XOR proof, deterministically fixing coordinates is not conditional pseudoexpectation. The `0,±1` Gram classes provide an actual quadratic realization; the lifted realization need not satisfy graph identities pointwise. The basis-row support union proves `|C|<=D rank(A_R)`, including repeated supports. Checked the positive-target endpoint, the order-one available objective, the degree-six clause-cost squares and all displayed dimension/exponent conversions.

For the supporting appendices, recomputed the point-packing pair categories and covariance bounds, the scale-cost counterexample and fibre iteration, the P-split retained-box witness and capsule distance calculation, the rank-one exposure/stability accounting, the shifted PSD slack and prefactor exponent, the FBBT detector/amplifier and contractor invariant, and the parity-class width/area/volume arguments. No attempted boundary example contradicted the stated hypotheses or conclusions.

### Exact finite checks

`check13.py` uses standard-library rational arithmetic and direct interval integration, independently of the finite-spreading induction. It checked 1,703 sorted marginal/support cases, 11,981 coefficient inequalities, with ambient dimensions 2–7, every support size in that ambient dimension, and means in `{0,1/4,1/2,3/4,1}`. It enumerates restrictions of the original ambient balanced subset, so deterministic deletion and smaller supports retain the correct correlated law. All coefficients were nonnegative.

The same checker verified 446 general-radix cutoff cases for bases 2–12 and levels 2–40, including all admissible adjacent cutoffs. It checked exact mean-one mixture weights, equality of the affine certificate at every stratum/profile and the exact objective `s+(L-s)b^(-s)`.

Extracted the executable text directly from the two finite-certificate appendices into private files and ran it. The complete normalized-signing enumeration returned `[1,2,4,4,5,8]` for dimensions 2–7. All three-group cubic integer minorants, rational primal means/values, smaller two-level certificates and the m=16 count certificate passed. This is a fresh replay of the printed proof, separate from the independently written coefficient/radix checks.

A fresh ledger check found 313 distinct referenced labels, all present among 341 unique manuscript labels. All 65 explicitly named repository file paths matched existing files. Presence alone does not verify coverage; the manual scope-to-proof comparison described above supplies the substantive check.

Results are in `check13.json`, `check13.log`, `printed_signings.log` and `printed_cubic.log`. These are exact finite checks; they do not prove the corresponding universal theorems without the arguments read and reconstructed above. No floating-point mathematical experiment was used in this review.

### Build and PDF

Copied only frozen TeX inputs and bibliography into the private `build/` directory and ran `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` with that directory explicitly set as the working directory. The build succeeded with 111 pages. There were no unresolved citations/references or overfull boxes. The raw TeX log has three underfull-box notices; these are not mathematical or readability defects in the inspected output.

Fresh `pdftotext -layout` extraction of all 111 frozen pages agrees exactly, page for page, with extraction of the private rebuild. The rebuilt PDF has a different byte hash, as expected for a fresh build with metadata; the target reviewed remains the frozen hash above. `build_check.json` records the comparison.

Rendered and visually inspected frozen PDF pages 1, 24, 49, 73, 85, 96, 103, 104, 109 and 111. These cover the abstract/navigation, finite cubic formulas, precision/open-question comparison, lifted degree accounting, certificate table, repaired catalogue hypothesis, PSD transfer, FBBT correction and bibliography. They are readable and unclipped. This is sampled visual inspection, not a claim that every page received a raster-level audit. The complete mathematical reading was from the source, with full-PDF text/build correspondence checked separately.

## Remaining limits

The exact cubic constant, matching second-order lower asymptotics, finite-aspect optimum, higher-width and stronger partition targets, unequal-aspect frequency-two optimum, and unrestricted affine-branching constant-gap question remain open. None is used as a premise of a theorem in this manuscript.

This review does not certify publication priority, remote-link permanence, identity of uninspected source versions, every exploratory solver experiment, practical efficiency of the granted exact quadratic hull oracle, or formal proof-assistant correctness. These limits do not produce a defect in the properly scoped statements reviewed here.
