# Whole-manuscript editorial review, round 1

Status: **PASS for whole-manuscript editorial coherence, claim scope, proof reachability, and sampled readability**, for the frozen source scope below. No editorial corrections remain requested. This report is review evidence, not a submission source.

## Scope and method

Read BRIEF.md, AUTHORING-CONVENTIONS.md, ARCHITECTURE-DECISION.md, ISSUES.md, LITERATURE-KEYS.md, main.tex, macros.tex, references.bib, every main section, every appendix, and all three table sources. The regression appendix was read after its arrival. The initial pass occurred while authors were active; the frozen-version comparison and exact read scope are recorded below.

No literature research, experiment rerun, project-wide verification, CI inspection, or manuscript edit was performed. A read-only Python Fraction calculation checked the displayed eleven-node branching example. A preliminary read-only reference scan identified missing inputs and keys while authors were still active; it is not a final build check.

## Findings sent immediately to root

1. **Bibliography TeX escapes.** The McCoy--Tropp journal field had a doubled backslash before `&`; the Hug--Schneider field had an unescaped `&`. Both need ordinary TeX `\&`.
2. **Missing bibliography identities.** The then-current bibliography lacked cited Rikun, Kaibel--Weltge, and Dong--Chen--Linderoth keys. The final Luna integration must resolve source identity and claim scope rather than preserve provisional entries automatically.
3. **Regression source corruption.** Several align rows ended with one backslash, the dual formula printed `lambda^{-1}`, and the exactness equivalence printed `quad` without its backslash. These are concrete source defects, not requests to change the mathematics.
4. **Branching tight-point error.** The eleven-node example states that its middle piece is tight at 13/16, which lies outside that piece. Exact Fraction substitution gives the actual tight middle point 1/2. Its first piece is tight at 3/16; the value at 13/16 in the last piece is positive, 1210319/446560000.
5. **Propagation variable definition.** The fast-round proposition must identify U_0 as the upper bound on u=t^2. Its recurrence uses that meaning, but the statement merely says "initial upper bound."
6. **Empirical McCormick cross-reference.** The aligned McCormick explanation in experiments points to sec:face-exact, whose positive separable-gap theorem is a different oracle. It should point to the McCormick material in sec:geometry.
7. **External lattice inputs.** The maximal lattice-free polyhedron theorem and Siegel mean-value theorem are explicitly external non-elementary inputs but lacked bibliography citations. Request verified sources and theorem locators through Luna. The parity/Jeroslow precedent should also receive verified attribution.
8. **Internal status wording.** Replace the introduction's "A completed induction" with a mathematical description such as "The sharp-coordinate theorem." Completion history does not help the reader.
9. **Gaussian matrix concentration input.** The regression appendix states the rectangular Gaussian singular-value inequalities at `regression:singular-tail` as an external standard fact but supplies neither proof nor citation. Request a verified primary source and theorem locator through Luna.
10. **Kaibel--Weltge comparison scope.** The final literature ledger distinguishes hiding-set formulation complexity from B&B tree-size bounds. The introduction and lattice chapter group this source with Dey et al. under B&B lower-bound mechanisms. Split the attribution: Dey et al. for B&B midpoint/leaf-capacity bounds; Kaibel--Weltge for the related formulation obstruction.
11. **Schichl exclusion scope.** The final ledger states that the source's validated exclusion regions identify critical points and do not themselves enforce an objective cutoff. The introduction and propagation opening attribute cutoff exclusion/propagation to that source. Attribute interval overestimation and validated exclusion to the source, then identify the manuscript's objective-cutoff model separately.

Saved-version inspection confirms resolution of findings 1--11. Finding 4 was repaired using simpler breakpoints 2/5 and 3/5, with side minima 209/160000 and middle minimum zero at 1/2. All TeX inputs and cited keys are now present, with no duplicate/undefined labels or placeholder/process markers. The newly added `app:branching-dimension` proof has arrived and was read in full. Findings 10 and 11 were repaired in the introduction, lattice, and propagation openings; the saved sentences and their rendered pages were reread. Dey and Kaibel--Weltge now receive separate attributions, and Schichl's established exclusion tools are distinguished from this paper's cutoff model.

The external lattice inputs now cite Basu--Conforti--Cornuéjols--Zambelli, Theorem 2, and Skenderi, Theorem 3.2 and Remark 3.3. The probability inputs cite Laurent--Massart, Lemma 1, and Davidson--Szarek, Theorem II.13, together with the required 2003 corrigendum. The appendix explicitly maps the matrix normalization and requires a nonnegative lower bound before squaring. The alphaBB paragraph attributes the established underestimator to Adjiman et al., while leaving the paper's box-face characterization separate. These saved passages agree with the final literature ledger. The unread Jeroslow original is excluded from theorem attribution and the retained bibliography; the quadratic example is proved in full and carries no priority claim.

The final framing reread requested one further small hypothesis qualifier: the discussion's summary of the BLS hard law should specify divergent sublinear SNR. This is now saved in both the statistical summary and the open question, agreeing with the abstract and introduction. The visible author field and PDF author metadata are both blank in main.tex.

## Integrated PDF inspection

Root supplied a 125-page integrated PDF and reported a clean build with no undefined references/citations, errors, or overfull boxes, and three underfull hboxes. This reviewer did not run a build. Directly inspected root-rendered pages 6, 20, 26, 32, 58, 64, and 124. Text, theorem statements, displayed equations/cases, margins, and bibliography are readable, with no clipping or collision on these pages. Figure page 64 has readable four-panel axes, legends, rate guides, termination markers, and caption. This is sampled visual inspection, not a claim that all 125 pages were inspected.

The first bibliography rendering lowercased proper names/acronyms under plainnat (MIMO, Gibbs, AND/OR, Boolean). Protective title braces now preserve the verified names and acronyms. The rebuilt bibliography pages confirm the repair, including Banach, CSP, Poisson, LP, Lasso, and Steiner.

PDF/render scope at inspection:

| Artifact | SHA-256 |
|---|---|
| `main.pdf` | `d2f4fd490347c67d2e19e678a9939626423b4539e8c55ef71a426db00bd37207` |
| `delivery/preview-page-6.png` | `66b57745ee419b23c4b70fa1dbbf254811b42035498ac10840141acf40ba027d` |
| `delivery/preview-page-20.png` | `ce2daf6a220a3fca91f5f844366929835964cfc01893adb9864693a5eb0aa972` |
| `delivery/preview-page-26.png` | `ea1929ad7e9745eb9bdf25b18149c19b6646e27a91ab13c78c1159e64bd65b92` |
| `delivery/preview-page-32.png` | `470f32cb991faa92ca5a2f8e54a8c40d4873265f0007bd0263c081465a78ba6b` |
| `delivery/preview-page-58.png` | `33647a4bb29612c85fc1fe6a11e71d7f36a7a883907018396bd01abe744fe418` |
| `delivery/preview-page-64.png` | `31118387d391e1102757f6ef9020b8565d6ab05a493166caef497f934c6b65ef` |
| `delivery/preview-page-124.png` | `65380ed49efb4025db9456333c9a03b73784e82c6d70cd53c3bb34c2b4b9f75d` |

## Editorial assessment

The certificate viewpoint supplies a coherent organizing question across the continuous, decomposition, integer, and statistical chapters. Definitions distinguish covers, rectangular partitions, permitted split trees, and semantic convex-piece trees. Incumbent assumptions, oracle changes, removed-piece accounting, virtual probes, local checking, and propagation rounds are generally stated where readers need them.

The abstract, introduction, and discussion agree on the principal continuous rates and on the separation of the three BLS events: integer recovery, C1 at every wrong fixing, and root box inactivity. They explicitly avoid inferring large trees from C1 failure. Sparse-regression negative claims are framed against the planted value until planted optimality is available, and the easy and hard signal regimes are distinguished. The fixed-dimensional PWE comparison is narrow and preserves the underlying formulation and deterministic condition.

The manuscript explains why the results matter: a certificate obstruction cannot be removed merely by selecting different cuts; changing the relaxation or proof representation may remove it; a short certificate can still be expensive to find or check. It supplies no unsupported production-solver speedup claim. Archived observations are presented with their numerical and selection limits. Long proof appendices support the main narrative without requiring a shorter paper.

The final `evidence/LITERATURE.md` has been read completely, with its last revised PWE sentence reconciled after the stability notice. Its SHA-256 is `028cc65ed65d141c5b71f03591b51cc99cbc1616f02976f0cbcb7c6ccbc3afe8`; the final `evidence/LITERATURE-KEYS.md`, also read, has SHA-256 `41878dcb04073dbd87d230bb58ffe6547d34699fdc9e574ef62fd1d345c48b6e`. The last key-map-only correction now correctly states the McCoy--Tropp law for a standard Gaussian vector and fixed cone; its saved row was reread. Analytic sublevel inputs, bilinear envelope formulas, Gaussian cone laws, and the Gaussian regression Student density are described as established. The finite NNLS tail and its simultaneous B&B use are identified as the relevant paper-specific ingredient. After findings 10 and 11 were repaired, the framing agrees with the ledger's model, normalization, resource, and unread-source limits. In particular, it makes no universal priority claim, does not treat unavailable sources as evidence of novelty, and describes the PWE contradiction only under the printed per-entry-noise normalization.

## Final disposition and limits

No editorial blocker remains in the frozen manuscript. It gives a complete narrative across the reviewed development scope, motivates the results for optimization readers, states the substantive operation and relaxation restrictions, and makes its nonstandard proofs reachable in the main text or appendices. The abstract and summaries retain the key distinctions and avoid solver-speedup or universal-priority claims. The prose is suitable for expert journal submission within that scope, with blank authors as requested.

This is an editorial and coherence verdict, supported by the independent chapter reviews for mathematical correctness. It is not an exhaustive literature/priority clearance or a journal acceptance prediction. Visual inspection is sampled and identified by artifact below. Root performed the standalone builds and package checks; this reviewer performed source reads, targeted read-only reference/key inspection, exact Fraction substitution for the branching example, SHA-256 comparisons, and inspection of supplied images. No experiment, solver, CI, project-wide verification, or independent literature search was run. Shared-KB archive bookkeeping lies outside this review and does not alter the frozen manuscript claims.

## Frozen source scope

The root froze this snapshot at `2026-10-06T04:25:39.101419+00:00` in `delivery/source-freeze.json` (SHA-256 `a35ab77448d835494cab523d69baf93062497a2047278d3c1183c94665c6c786`). A final read-only comparison found that all 29 local submission inputs match the manifest. All sections, appendices, table sources, bibliography, and build instructions have been read. Relative to the earlier complete read, the saved changes were in the lattice and regression appendices, discussion, face and lattice sections, and bibliography; these versions have been reread. The last attribution edits in the introduction, lattice, and propagation opening were then reread directly. The figure is included for artifact identity. Root confirms mathematical review hashes match all 22 final chapter/empirical entries in `delivery/review-hash-check.json`.

The bibliography-stage PDF had SHA-256 `dd67815aa84b3e659c9fa3ce1d1dce9fe68d0f8bf4bde4422376d9ce8ee66f82`. Direct inspection of its regenerated bibliography pages 124 and 125 confirms readable layout and corrected proper names/acronyms. Their PNG hashes are `c823e4dae63856ab57178cec36714ebd8ba457b39b28d0afc2ee692620407732` and `8d8082a996aacf361b8daae04e91d591530267ced5ffd6ee62677dc20dc8c625`. Earlier sampled body/figure inspection remains scoped to the earlier PDF and hashes above.

The final 125-page PDF has SHA-256 `42ac972a51686afdc97fb39d00afab08d4ca33381c288dfcf0d9a0521ed298fe`. Its repaired-prose pages 9, 33, and 43 were directly inspected: text, citations, theorem statements, and displays are readable without clipping or collision. The PNG hashes are respectively `a378272be940f218d884724e9df060417946425848b596bf6dc385be97f5b3dc`, `45ffdb3175b311571247173a1285c201eb18fd28bda079df86b91fe0399f3b18`, and `645c51ac3d35456d6bcd5c16c1572b38492d545a182edc1807386332734a238c`. Root reports a successful relocated clean build of the matching portable package, all 30 checksums and 29 local-input comparisons passing, byte-exact PDF text agreement, and no blocking warnings. This reviewer did not execute that build.

| Source | SHA-256 |
|---|---|
| `BUILD.txt` | `0cbbe4b1de7234ae4b8157def41c02609eb52b54533936bc2d758df219247422` |
| `appendices/bls-proofs.tex` | `8fb602516aba588cceee13ced87b89d2799ca05db1498cc1400c55405ffe8e6c` |
| `appendices/branching-proofs.tex` | `413818bddd4560ee9525e3297a8629496b44a9a00d58e641b489e27655743b70` |
| `appendices/decomposition-proofs.tex` | `f41d4ef325560234d563aee7752b895fbdd27d07a100248a4a1a50306e6d6b1c` |
| `appendices/face-proofs.tex` | `f10db89fc908a85a3e93d60f78558ba5050e9256e7f46fc6bfc5068ed350630e` |
| `appendices/geometry-proofs.tex` | `8cd3da2e1ef4c8b6babf6e6cb734afd36f563f5fda7f36ef93a5cdddb48c3349` |
| `appendices/lattice-proofs.tex` | `8e3ffdb2e4c16eca503e950c4ff22e45c8068fb9b20c597dc9a47dd6a7ae7221` |
| `appendices/propagation-proofs.tex` | `5c8d4254c6d78f33c43aadb07ecaea1d434f49ba15a79d32c0cf8586049645ca` |
| `appendices/regression-proofs.tex` | `759760aff46a9376db68a325f9207a642bd0c3d02b0957d404c2db59fc8274a9` |
| `figures/node-scaling.pdf` | `3eb3c03c8d569768896811073ebe53ab7adc9cefc57ec0e5619b51dece2dd54b` |
| `macros.tex` | `10731fd28908919532a33e8601f6011bb54e23aba46148b283837c984b09913d` |
| `main.tex` | `210e17b7e1193f329bffb16fed02e47ce3dd45ec8df05f2a6333d3f819f6e770` |
| `references.bib` | `9409dbc80bc83a5888806b2a7e6efb014f47af1623bb930ec4d5e2c7fc2c9d32` |
| `sections/abstract.tex` | `ef5d8464f1c0df6662d7476a9afad3a770a0a963959310b5e8d908ed5a95e269` |
| `sections/binary-least-squares.tex` | `bd256b308009b27da0bf3bd01b6fff6bb4ac645b978bdfd54054aec1b3ed7043` |
| `sections/branching.tex` | `a746e77d893c12c0ae9ea31bd10c220e0ce23e63fa107ecee10cbde2d1c7e39d` |
| `sections/certificates.tex` | `645cf2ab6f39d05b7749add31c7bbf50f5e75b370531b326cfb78d00fd8777d4` |
| `sections/decomposition.tex` | `947940025b0531535457c203c1c2ebb0e420f190631036675bf8c73c85e71ed4` |
| `sections/discussion.tex` | `c10cd87846eadc96b5407cbb34fa933c78bffc2c1124051455712f9d9ffd59a0` |
| `sections/experiments.tex` | `455ef17d3c7ec4042e93d2b3d01f8e283813e6db9942c13debbdea17a5c47350` |
| `sections/face-exact.tex` | `780273b271ef15582a3e865053642c81fe6c7efdd496e66382ea568003881109` |
| `sections/geometry.tex` | `0d9b8b10d5a9f8b84578abbf7c8b372854534ce924c2fc5d6803b20c820d2506` |
| `sections/introduction.tex` | `babc03bcd1f337123b36d793dbc37b8319ad5dfb5156c3e5cbee93342693254a` |
| `sections/lattice.tex` | `6f2a698fc11be69addf3d526f3b8c15976a6384ae23778bdff686a1cd68c667c` |
| `sections/propagation.tex` | `1125781a1465c9a5f2f490bab596a73c9c9c1eb1bc3da780815b4b9c058f029d` |
| `sections/regression.tex` | `abb0dd9920afe7fcfe466c766d4c38e2982bb4ff4dadcaa3c9776e047d600d09` |
| `tables/empirical-branching.tex` | `d10dc8b4294c1683a114c00d7b6dd266bdd52b62c22851951d62fe0cff09e4bd` |
| `tables/empirical-finite-c1.tex` | `3eb71cec88973722abf01ece4a5463fa8152250c8f26df858447ef8cc4027fc8` |
| `tables/empirical-protocols.tex` | `48b157ed6fae62f5c6733450341ae995af1b6546c07c5aa51a03665f04fabcd7` |
