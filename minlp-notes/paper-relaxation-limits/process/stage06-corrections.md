# Stage 6 corrections

September 7, 2026. The separate correction agent read the complete round 1 reports 09 and 11, the coordinator adjudication, and the correction assignment before editing. All three accepted minor findings are repaired. Stage acceptance remains with the coordinator.

| Finding | Exact correction | Verification |
| --- | --- | --- |
| R09-1 | Proposition G.4 now states that the finite catalogue satisfies $\Lambda\subset[0,M]$, $\{0,s,M\}\subseteq\Lambda$, and $0<s<M=\max\Lambda$. Both the supporting-comparison row and the bounded-development row in `process/claim-coverage.md` state the same membership assumptions. | Read the proposition and its proof, including its zero and maximum slices and endpoint-only exception. The clarification gives the intended scope. Every proof block in `sections/appendix-scaling.tex` remains byte-identical to the reviewed snapshot. |
| R09-2 | The incidence coverage row now says “ownership of incoming high coordinates.” | Checked `sections/04-incidence-interiority.tex`: the proof partitions high variables into incoming and outgoing incidences, while the low coordinate is the anchor. The manuscript proof was already correct and was not edited. |
| R11-1 | Appendix J's opening LP comparison now begins “When the limiting box is nonempty” and cites Belotti et al., Theorem 4.1, directly after the LP claim. | Read original PDF pages 13–15 of `[[belotti2012-on-feasibility-based-bounds-tightening]]`, checked the matching `fulltext.md` p.14 marker, and rendered and visually inspected original page 14. Theorem 4.1 assumes a nonempty limit; Section 4.1 explicitly explains why the empty-limit case is excluded. Every proof block in `sections/appendix-fbbt.tex` remains byte-identical to the reviewed snapshot. |

The clean production build used `latexmk -C main.tex` followed by `python verification/build_and_check.py`. It returned compile exit 0, no warnings, no duplicate labels, and a matching printed cubic checker. The PDF remains 111 pages. Its SHA-256 is `912de166731f56368a8ee4db21294aa348b85364e85cd444e31265b29828d084`.

Comparing the complete pagewise layout extraction against the reviewed PDF identifies exactly pages 96 and 104 as changed. Both were rendered and visually inspected: the explicit catalogue membership and theorem citation are readable, with no clipping. All other pages have identical extracted text. The render files are in `verification/stage06-corrections-renders/`, alongside the original Belotti page 14 render.

The new `verification/stage06-corrections-validation.json` records current build, PDF, input, render, and primary-source hashes. All manuscript inputs other than the two named appendix files match the reviewed snapshot. Both frozen snapshot manifests were rechecked: all 81 build-manifest entries and all 9 review-context entries match. No snapshot, original literature, historical author or reviewer record, other paper directory, or unrelated accepted mathematics was edited. No unrelated mathematical test was rerun; the build script's printed-checker comparison is an input consistency check.

An initial optional page-comparison attempt found that the current Python environment lacked PyMuPDF. The completed comparison and rendering used the installed `pdftotext` and `pdftoppm` utilities, without adding a dependency.

The correction agent has finished validation and stopped edits. These checks establish the local repairs and production integrity; they do not replace coordinator acceptance or the separate whole-paper fifteen-reviewer loop.
