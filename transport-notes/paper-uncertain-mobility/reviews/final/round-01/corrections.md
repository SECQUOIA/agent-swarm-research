# Corrections: final whole-manuscript review, round 01

Fixer: `/root/paper_stage_fixer`, distinct from the substantive-stage authors. Date: 2026-09-07.

Input reviewed snapshot: `e5a8cd3e390d1b7afa16481b35bcd01944a8111bce55e2ffaf1570f40ebc899d`, preserved in [snapshot.json](snapshot.json). I read the [coordinator adjudication](adjudication.md), which accepts the minor finding groups below and no major issue. No reviewer report or historical handoff, acceptance record, or manifest was edited.

| Accepted finding | Corrected locations | Correction and verification |
|---|---|---|
| Reviewer 1 R1-F-1; reviewer 4 status item; reviewer 5 M1 | Manuscript `README.md`, `PLAN.md`, `claims-map.md` including N1, and `notation.md` | Removed stale pending-Stage-07 and pending-whole-manuscript-review statements. The live documents record completed development and the performed staged and five-reviewer whole-manuscript audits, linking the review ledger and final adjudication for coordinator decisions and accepted snapshots. N1 links the existing Stage 07 acceptance. This wording does not itself accept the corrected manuscript. |
| Reviewer 2 M1 | `sections/00-introduction.tex`, paragraph following `eq:intro-response` | Qualified the physical summary: for physically admissible designs with finite response, flow-induced dispersion equals χJ plus a nonnegative bulk correction. The information-preserving uniform-background construction remains unchanged. This matches the actual Schur theorem and leaves the larger scalar class intact. |
| Coordinator: local κ collision | `sections/03-predetermined.tex`, shell-test width; `sections/04-generic-folds.tex`, corresponding generic shell-test width; `notation.md` | Renamed only the local bump-width factor to δ_*. Made the generic proof's two small constants c_* and δ_* explicit. Added separate ledger entries for this factor and the integrated-rate anchor κ. Reversing these local substitutions, wording, and the positive-mass case-label clarification below exactly reproduces the two frozen section hashes. The model's rate-anchor κ and all quantitative estimates are unchanged. |
| Coordinator: positive-mass case label | `sections/03-predetermined.tex`, same shell paragraph | Changed the case label to `0<m≤c_1r⁷` before choosing a positive test width. The zero-mass case is already handled explicitly below; no proof or bound changes. |
| Coordinator: additional-constraint scope | `sections/08-discussion.tex`, admissible-design paragraph | Replaced the suggestion of a common scale obstruction from caps, backgrounds, and fabrication lengths by the precise statement that optimal values under additional pointwise, background, or fabrication constraints are not established. No new constrained-design claim or investigation was added. |

Delivery navigation: added one link in the repository-root `README.md` to the LaTeX manuscript workspace. It explains that the paper's new sharp supercritical coefficient and finite-ratio crossover proofs supersede the historical notes' open-status statements for those limits. Historical notes remain unchanged.

Build and scope checks:

- Removed prior build artifacts with `latexmk -C main.tex`, then ran `latexmk -g -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex` from the manuscript folder. The clean LaTeX/BibTeX build succeeded and produced 54 pages.
- Scanned the final `main.log`: no warnings, unresolved references/citations, or overfull/underfull boxes. Appended the command, toolchain, and PDF hash to `reviews/build-and-reproducibility.md` without altering its historical entries.
- Directly scanned all 17 manuscript `.tex`, `.bib`, and `.py` source files for non-whitespace control bytes, trailing whitespace, and missing final newlines. Scanned the edited Markdown files directly as well. These checks include untracked source files and do not rely on a Git diff.
- Compared every file in the 28-file final-review manifest. Exactly the eight manuscript source/document files listed below differ; mathematical Sections 01, 02, 05, and 06, numerical Section 07, numerical code/data/figures, bibliography, and historical manifest-listed review files retain their frozen hashes. The changes in Sections 03 and 04 are exactly the local symbol, explanatory wording, and positive-mass case-label corrections above.
- Confirmed the rate-anchor formula remains unchanged, the stale status phrases are absent, and the relative links in the changed navigation documents resolve. No substantive mathematical issue emerged or theorem changed.

Corrected file hashes (repository-relative paths):

| File | SHA-256 |
|---|---|
| `README.md` | `1ca94ec1d3ea8e9188b8581bc7f57d1f77d2e644d9dba9d685433eee81a2996d` |
| `paper-uncertain-mobility/README.md` | `47dd0518f0b39ed2e0711f5ba56fe5661d0515a345b88939e4f54f78d198b335` |
| `paper-uncertain-mobility/PLAN.md` | `3a3c6ddc06bb08e93dc68312d5dd19151e2e30525417f70307d129700cac5f14` |
| `paper-uncertain-mobility/claims-map.md` | `91cbac8f94878dce8df3153c52a090ee446c0c6492e75283b2b91557fd846e23` |
| `paper-uncertain-mobility/notation.md` | `baffc5365b69bf1737bf35bbd311f89a7e8a9050d7e183161b6e0890e00ce526` |
| `paper-uncertain-mobility/sections/00-introduction.tex` | `8b859f66cc4ed170d18002259a994e6f2f7ef5d43f13dd2442162795ff62033a` |
| `paper-uncertain-mobility/sections/03-predetermined.tex` | `88b7df21572e5cf39eec3d4898050a1b84ddeefbb421317e462733de6219ca20` |
| `paper-uncertain-mobility/sections/04-generic-folds.tex` | `87d7d4e4bdf10a71bc5e7bc50505006466db1a630e68fda814ee62523f0ebfa1` |
| `paper-uncertain-mobility/sections/08-discussion.tex` | `f4bc9ac735ae9b45d5001c9845bb7e9e3f2ddf5b2717d6d669ffbd171fc394d6` |
| `paper-uncertain-mobility/reviews/build-and-reproducibility.md` | `6afdfd9e6a6ded56d57563133e2968a69c87813f04d14759065424eac9b8417a` |

The only additional authored file is this correction record. Build output artifacts were regenerated; the PDF SHA-256 is `260be943f47f06955b4b78c6baa158ebbe44394009b008ea3c4c96cb0eef2dd3`.

Editing is complete. The coordinator must verify all corrections, inspect the affected PDF pages, update the ledger, and record the final accepted snapshot. This record is not the final acceptance decision.
