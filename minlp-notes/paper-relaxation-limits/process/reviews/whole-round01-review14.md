# Independent whole-paper review 14

**Verdict: PASS.** No major or minor finding. This is an independent review of the complete frozen manuscript, with additional attention to primary literature and attribution. It is not an endorsement based on earlier review labels.

The reviewed target is `process/snapshots/whole-round01/main.pdf`, 111 pages, SHA-256 `912de166731f56368a8ee4db21294aa348b85364e85cd444e31265b29828d084`. The final hash check matched. All 82 entries in its build manifest and all 10 entries in its review-context manifest matched their recorded hashes.

## Coverage

I read the entire manuscript in its frozen TeX sources, including every proof, appendix, displayed certificate, printed program, and bibliography entry. The exact files were `main.tex`, `macros.tex`, `references.bib`, and these files under `sections/`:

- `01-foundations.tex`, including the signed-bilinear arguments; `02-universal-positive.tex`; `03-cubic-equal-means.tex`.
- `04-incidence-interiority.tex`; `05-feedback-frequency.tex`; `06-treewidth-two.tex`.
- `07-positive-boxes.tex`; `08-exact-complexity.tex`.
- `09-cardinality-spatial.tex`; `10-cardinality-preordering.tex`; `11-coordinate-domains-lifts.tex`; `12-relative-blocks-cuts.tex`.
- `13-xor-quadratic-hulls.tex`; `14-monomial-reformulations.tex`; `15-finite-certificates-affine.tex`; `16-supporting-comparisons.tex`; `17-synthesis.tex`.
- `appendix-finite-signings.tex`; `appendix-positive-couplings.tex`; `appendix-cubic-certificates.tex`; `appendix-structural-auxiliary.tex`; `appendix-positive-box-predecessors.tex`; `appendix-point-packing.tex`; `appendix-scaling.tex`; `appendix-p-split.tex`; `appendix-rank-one.tex`; `appendix-fbbt.tex`; `appendix-integer-comparison.tex`.

I also read the frozen `README.md`, `PROCESS.md`, `process/review-protocol.md`, `process/whole-paper-review-assignment.md`, `process/scope-proposal.md`, `process/claim-coverage.md`, `process/stage-06-author.md`, `process/stage06-corrections.md`, and the assigned focus. I checked coverage against the actual arguments, including retained bounded developments and explicit exclusions. I read `../literature/AGENTS.md` before examining originals. I did not read another report from this final round, delegate work, or change manuscript, snapshot, or literature files.

Primary-source checking concentrated on the exact external statements used, their hypotheses, and version-dependent numbering. It was not a complete rereading of every external paper. The following records distinguish this work from the complete manuscript reading:

| Source | Primary material examined and relevance |
| --- | --- |
| Luedtke–Namazifar–Linderoth | Relevant envelope and gap statements in the author manuscript; Conjecture 1 on original PDF p. 22. The unit-box question and the distinction between positive and signed coefficients are represented correctly. |
| Boland et al. | Original PDF pp. 2–6: Theorems 1–4, Lemma 1 and its primal/dual proof, and Corollary 1. The manuscript correctly treats the half-integral cut characterization and square-root growth as established background. |
| Davidson–Donsig | Original PDF pp. 3–7, including Theorems 1.2 and 2.3–2.4. I checked the real Grothendieck comparison and the continuous weighted rectangular-density statement, rather than substituting the rounded integer-pattern bound. |
| Sherali | Original PDF pp. 8–9, including equation (13) and Theorem 3. The symmetric/equal-mean envelope is attributed as classical. |
| Del Pia–Khajavirad | Relevant Berge-acyclicity definitions and Theorem 7, checked against original PDF p. 9. This supports the stated relationship to exact standard linearization, without identifying all acyclicity notions. |
| Hassin–Tamir | Original scanned PDF pp. 2–3, read visually because text extraction was empty. Theorem 3.1 and the series-parallel definitions support the block decomposition used in the width-two argument. |
| Cornuéjols | Theorem 6.5 (Camion) and Theorem 6.13 in the July 2000 author manuscript. The paper keeps total unimodularity and the balanced-matrix slab theorem distinct. |
| Adams–Gupte–Xu | Original PDF pp. 22–23, especially Proposition 4.1 and its constant-ratio envelope formulas. The manuscript does not infer an unequal-aspect formula by an invalid coordinate replacement. |
| Altschuler–Boix-Adserà | Original PDF pp. 55–56, Theorem 7.4, Corollary 7.5, and the intervening accuracy discussion; the arithmetic/accuracy convention was also checked. Polynomial dependence on inverse accuracy does not contradict the manuscript's exact rational complexity result. |
| Potechin / Grigoriev attribution | Potechin's Theorem 1, Example 18, and Theorem 44 and its proof, including the falling-factorial moments and attribution to Grigoriev. I did not independently read the complete original Grigoriev paper. |
| Schoenebeck | Author full version: Definition 10, Theorems 11–12, Lemma 13 and the signed-character argument; Theorem 21 and Proposition 22 with the width proof. I checked the strict parameter ranges needed at constant density and the distinction between width closure and mere small-support consistency. |
| Jarre | Author preprint, Sections 2–3 and the binary-knapsack/max-cut SDP comparison. Its branching and oracle restrictions support the manuscript's carefully limited precedent statement. |
| Kronqvist–Misener–Tsay | Published original, assumptions and additive bounds, Definition 4, and Theorem 6 with its proof on PDF pp. 15–16. The retained-domain counterexample addresses the universal assertion actually printed there. |
| Fawzi–Parrilo | Original PDF p. 3, Theorem 1 and the Lorentz-cone decomposition discussion. The fixed-block and SOC conclusions use the correct resource. |
| Lee–Raghavendra–Steurer | Author full version, PDF p. 23, Theorem 3.8 and equation (3.11), and pp. 32–34, Theorems 5.3–5.4. The explicit dependence on the pseudo-density parameters is sufficient for the shifted-slack calculation in Appendix I. I did not reprove the complete external PSD-rank theorem. |
| Braun et al. | July 2013 author version, PDF p. 18, hard-pair construction and Theorem 6(i). The fixed-dilation LP comparison is used at the stated scale. |
| Belotti et al. | Original PDF pp. 13–15, especially Theorem 4.1 and the following empty-limit discussion. The repaired opening of Appendix J now has the necessary nonempty-limit hypothesis. |
| Etessami–Yannakakis | Author version, PDF pp. 26–28, Theorem 5.2 and its PosSLP construction. PosSLP hardness is not relabeled as NP hardness. |
| Stewart–Etessami–Yannakakis | Original PDF pp. 21–22, Section 4.1 and equation (18). The manuscript's primitive-update result is distinguished from the source's Newton iteration discussion. Esparza et al.'s Section 7/Theorem 7.1 was also located and its comparison read, without a complete external proof audit. |
| Lubin–Vielma–Zadik | Original PDF p. 12, Lemma 4.1 and its parity proof. The manuscript's midpoint argument respects the integer-coordinate count. |
| Beach et al. | Combined 2022 original, PDF p. 21, Section 5.1.1. The bibliography explicitly distinguishes this numbering from published Part I. |
| Wu et al. | Original-source text, Section 4.1, Assumption 1, Lemma 3, and Theorem 3. The manuscript gives its own disaggregation proof and identifies the source's additional assumption. |
| Ahmadi et al. | Version 1 source text, relevant fixed-degree discussion and Section 6, including Algorithms 2–3 and their positive-tolerance termination statements. The paper does not turn termination into a polynomial region bound. |

Additional primary web checks confirmed Anstreicher's four conjectured point-packing values in [Conjecture 4 of the May 2007 author manuscript](https://optimization-online.org/wp-content/uploads/2007/05/1655.pdf), and the corresponding established results in [Khajavirad, Propositions 1(i–ii) and 3, version 1](https://arxiv.org/html/2404.03091v1). I checked the convex degree-cost matching construction in [Deza–Onn, Theorem 1.2 and Section 3](https://arxiv.org/html/1908.09278). The integer-negation convention and Tseitin comparison match [Beame et al., Section 1 and Theorem 1](https://arxiv.org/html/1710.03219v3); the finite-field and coefficient-restricted statements match [Fleming et al., Theorems 1.3–1.4](https://arxiv.org/html/2102.05019v2).

The Coniglio comparison could not be independently source-checked: both the forum and the linked anonymous PDF returned an OpenReview browser-verification page. I did not circumvent it. The manuscript identifies the precise review version and explicitly leaves identity with the published version unverified. This is a limit on this review's verification of a contextual comparison, not an assumption in the manuscript's proofs.

## Findings

None. I found no demonstrable defect requiring a repair. The source-access and verification limits below should not be read as claims of additional results or as invented findings.

## Independent verification

### Proof reconstruction and falsification attempts

For signed bilinear widths, I reconstructed the half-integral reduction, the polarization identity, and the cut-range normalization. The local maximal-cut argument uses squared coefficients before the row-norm estimate. The induced density parameter and the continuous weighted Schur estimate have compatible normalization. Zero terms and empty supports do not require division by a zero width. The random-sign lower bound concerns growth, and the small exact signings are finite statements.

For positive unit-box polynomials, I traced the dyadic construction through the affine cap, cutoff ties, resource normalization, and the bit-reversal attaining laws. The inactive mass and the independent/common-threshold mixtures are retained when the active support changes. The harmonic normalization and tangent optimization yield the stated Lambert-W bound. Cloning integer weights preserves the limiting ratio because both envelopes have a uniform vertex-error estimate. In the cubic section, the coefficient 31/12 is an upper bound from the displayed mixture and is not claimed to be the exact universal cubic constant. The five rational Bernstein identities give a strictly positive slack; the resulting limiting lower ratio and the finite certificates are compatible.

For structural improvements, I checked the ownership of incoming high coordinates, conditional gluing in a feedback deletion, preservation of the independent baseline, and the fractional odd-cycle structure in the degree-slab argument. I reconstructed the convex degree-cost matching gadget and the rational optimization/separation use. The width-two proof maintains its terminal information through both series and parallel composition; its TU step invokes Camion separately from the balanced-matrix result. The radix counterexamples do not imply a bound depending only on degree-independent treewidth.

For positive boxes, I checked the global minimum/maximum aspect reduction while retaining common ambient random choices. Expanding a positive monomial into square-free terms changes the termwise relaxation in the required direction. Endpoint and empty-factor cases agree with the formulas. In the exact-complexity reduction, the rational perturbation parameter has polynomial encoding length, the NO case uses an integer partition imbalance, and the YES case uses a complementary endpoint law. This establishes the stated weak exact hardness and small rational certificates; it does not establish fixed-accuracy hardness or strong NP hardness.

For spatial cardinality bounds, I reconstructed the homogeneous Gram expansion, the conditioning identities for literal products, the permissible endpoint ranges, and positivity for globally coupled squares by a tensor-product principal-submatrix argument. The coordinatewise graph lifts preserve polynomial order because every lifted coordinate becomes affine on the two selected endpoints. The objective and equality checks require agreement only on the selected graph atoms. The count applies to every certified region covering a witness, hence to a finite cover, without assuming disjoint leaves.

For the XOR section, I checked the use of width closure to obtain a consistent signed Gram matrix, the 4r and 4rD degree budgets, deterministic substitution under coordinate fixing, bounded-occurrence deletion, and the constant-density gap. Fixing is not silently replaced by probabilistic conditioning. The quadratic-hull comparison permits actual second moments in the full domain without forcing an auxiliary point back onto its graph. The parity-rank support estimate uses a basis of queried supports. The order-one strengthening and the affine-halfspace examples prove the advertised distinctions and limitations of the counting method, rather than an unrestricted affine-branch lower bound.

For the supporting appendices, I checked the packing covariances and adjusted secants; the scale-hull disaggregation, zero-scale slice, and rectangularity criterion with {0, s, M} ⊆ Λ; and the P-split retained-box example. In the latter, the union already contains all box vertices, while coordinatewise strict Jensen inequalities need not hold if the selected points share a coordinate, and an outward perturbation need not stay in the retained domain. The directional repair adds the conditions that avoid these failures. I reconstructed the rank-one correlation face and the stability transfer, including the shifted slack's coefficient norm and the explicit LRS parameter dependence. I also checked the FBBT least-fixed-point invariant and the restriction to primitive affine/product contractors, and the integer-precision midpoint, scalar-square, product-width, and area arguments. These do not exchange lift size, propagation updates, integer coordinates, and spatial regions.

### Exact computational checks

Artifacts are under `verification/reviewer14/whole-round01/`. I extracted and ran the printed programs from the frozen finite-signing and cubic-certificate appendices. Both completed successfully. The signing output gives the six reported finite values; the cubic program checks all listed count states, rational dual inequalities, primal laws, and claimed ratios. These runs validate those finite certificates, not their discovery or any asymptotic optimality claim.

I separately wrote and ran `independent_check.py`; `independent_check.json` records:

- 729 coefficient patterns on K₄, checking the polarization identity exactly.
- 107 radix cutoff cases for bases 2 through 8 and depths 2 through 15, including ties, checking normalization and the attained affine cap exactly.
- 70 symbolic homogeneous-Gram entry identities for degrees 1 through 4 and several admissible dimensions.
- All five rational Bernstein identities and the minimum coefficient 901/120000.
- Two scalar certificate polynomial identities.
- 61 rational points checking the retained-box P-split link inequalities, supplemented by the analytic box-vertex argument.
- 2,300 small parity-support triples, checking the support-union/rank inequality exactly.

These are integer, rational, and symbolic computations. I did not use floating-point LP/SDP output as proof, and did not run numerical solver experiments. Finite identity checks supplement the universal arguments; they do not establish them by enumeration.

### Build and visual checks

I copied the 31 frozen TeX/bibliography inputs into `verification/reviewer14/whole-round01/build/`, verified that they match, and ran `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` with that directory explicitly set as the working directory. The build succeeded and produced 111 pages. Its page-layout text extraction is byte-identical to the frozen PDF's extraction. The final log contains three underfull-hbox diagnostics in bibliography material, with no overfull-hbox, unresolved-reference, or duplicate-label diagnostics. The underfull lines are readable and are not a finding.

I rendered every frozen PDF page and inspected all 111 pages in overview sheets for missing material, clipping, page breaks, and gross layout. I additionally inspected full-page renders of pages 22, 84, 86, 87, 96, 104, 109, and 111, covering the positivity table, finite certificates and code, the repaired scale and FBBT passages, and bibliography/version notes. These detailed pages are readable. I also inspected source-page renders for Davidson–Donsig, Kronqvist et al., LRS, Schoenebeck, and the two scanned Hassin–Tamir pages. `verification-record.json` records build, manifest, exact-check, and visual coverage evidence.

## Remaining limits

This review is not a formal verification of the manuscript or a complete independent proof of every classical external theorem. Standard dependencies such as real Khinchin constants, perfect matching algorithms, rational LP optimization/separation, PARTITION hardness, disjunctive hulls, and Shapley–Folkman are used as established mathematics; I checked their application in the manuscript without rereading every original proof. In particular, I did not separately audit all of Szarek, Edmonds, GLS, Karp, Balas, Starr, Barrus, Padberg, and McCormick. The complete Grigoriev and LRS external proofs were not reconstructed. Primary-source table entries describe the actual passages checked, not whole external papers read.

The overview render check is not a glyph-by-glyph visual review of all 111 pages. Mathematical reading was from the complete TeX sources; detailed PDF inspection was selective. The build comparison establishes matching extracted content, not identical PDF bytes or a proof that every PDF link destination was tested.

I did not verify every journal metadata field against publishers, nor establish identity between each author version and its eventual publication. The manuscript generally identifies the exact version when numbering matters. OpenReview prevented the independent Coniglio check described above. No new assertion about that source's published version is made here.

The paper expressly leaves sharper universal constants and unrestricted affine-branch conclusions open. Its lower bounds are for the stated domains, node oracles, tolerances, encodings, and resources. I found no place where those stated limits were used as if they proved the broader open claims.
