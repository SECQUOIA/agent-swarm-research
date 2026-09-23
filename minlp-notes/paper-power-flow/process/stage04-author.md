# Stage 4 author report

The complete 28-page manuscript is ready for five independent stage-4 reviews.
No new mathematical gap was found during integration. This report does not
declare stage 4 accepted or substitute for the required whole-paper review.

## Changes

- Replaced the long abstract with a concise overview led by simultaneous
  connected planar bipartite degree-three, unit-conductance, fixed-girth
  existential-real completeness. It retains the rational coefficient field
  in the universality claim and uses the explicit cosine interval (-1,1].
- Added `sections/00-introduction.tex`: problem motivation, theorem overview,
  proof strategy, model restrictions, and checked primary-source comparisons.
  The reader is told which AC statements use real bus angles, principal line
  angles, and reference-fixed boxes, and which numerical result is a gap
  promise. The fixed-data versus size-dependent cosine distinction is explicit.
- Added `sections/07-conclusion.tex`, collecting only proved results and
  explaining their exact/approximate and real/principal-angle scopes.
- Added `appendices/verification.tex`: all four deterministic standard-library
  suites and their actual counts, a table and derivations resolving all eight
  legacy source examples, the rerun legacy winding check, and a precise
  statement of historical AC solver evidence. The four old AC instances had
  15, 19, 23, and 25 buses and reported bounds on the sum of squared imaginary
  voltages; the licensed solver was not rerun and no floating point bound is
  used as a formal certificate.
- Completed bibliography metadata and source-version attribution. The only
  change to the accepted mathematical sections is the Bienstock–Verma
  approximation citation in section 06, now pointing to its explicit arXiv
  version. All other accepted section, arithmetic-appendix, checker, and macro
  files are byte-identical to `process/snapshots/stage03-accepted/`.
- Rewrote the README with final scope and reproducible commands; completed
  the source coverage map, including the identical other-worktree audit and
  explicit duplicate/out-of-scope dispositions. Snapshot locations are correctly
  given as `process/snapshots/`, and execution logs as `verification/`.
- Updated `.gitignore` to exclude reviewer build directories and rendered
  diagnostic images while retaining review reports, checker code, manifests,
  and useful text logs. Root/reviewer4 separately handled relocation of its
  earlier task-owned artifacts.
- Kept the anonymous article format, set the PDF title metadata, and used a
  smaller bibliography font so all 15 entries fit on one page without a
  nearly empty final page. No author identity, submission, or journal template
  was invented.

## Literature verification and decisions

I read the relevant primary full text in the repository and cached PDFs,
along with the accepted dependency audits and root integration cautions.

- Gan–Low's primary PDF explicitly distinguishes physical DC networks from
  linear DC approximations and gives conditional SOCP exactness regimes. The
  introduction attributes those scoped conclusions, not unconditional exactness.
- Jeeninga–De Persis–van der Schaft Part I, cached Theorem 3.22, characterizes
  both exact and interior fixed-source constant-power-demand feasibility.
  The introduction preserves both claims and does not infer exact Turing P
  from a matrix-inequality alternative. Part II supplies no additional result
  required for the comparison.
- Lehmann–Grastien–Van Hentenryck's primary full text fixes unit magnitudes
  and proves hardness by a star construction. Bienstock–Verma's primary text
  uses the lossless fixed-magnitude model with unconstrained reactive power.
  Neither is presented as the same physical subclass as the present transfer.
- Bienstock–Muñoz's primary Theorem 7 and Corollary 8 concern scaled feasibility
  and optimality tolerance, as stated in the introduction. Their exact versus
  approximate distinction is preserved.
- Lavaei–Low's cached Appendix B, Case 2, was checked for the zero-reactive
  connection. It is credited without adopting the unrestricted discrete-phase
  conclusion. Dörfler–Chertkov–Bullo is used only for the sine-coupling
  framework already checked in stage 2, not a global torus uniqueness theorem.
- The compendium's primary introduction and class discussion supply context;
  no search-absence or priority conclusion is asserted.
- The Dynamic Toolbox correction and the self-contained conjunction-only
  proof remain intact. The introduction keeps rational basic-closed
  universality over Q separate from arbitrary semialgebraic topology.
- The algebraic, crossover, triangulation, and polynomial-minimum citations
  retain the versions and locators verified during accepted stages 1–3.

Additional primary online metadata checks:

- [Bienstock–Verma arXiv v2](https://arxiv.org/abs/1512.07315v2) states a
  revision date of 9 April 2019. The new separate preprint entry therefore
  uses 2019 and explicitly identifies v2. Its Section 1.3 is not attributed
  to the differently organized journal version.
- The [University of Copenhagen STOC record](https://researchprofiles.ku.dk/en/publications/the-art-gallery-problem-is-%E2%84%9D-complete/)
  confirms pages 65–73 and DOI 10.1145/3188745.3188868. The bibliography no
  longer uses “locally archived” wording; the text qualifies the full-version
  theorem numbering.
- The [SIAM publisher record](https://epubs.siam.org/doi/pdf/10.1137/15M1054079)
  and [author publication list](https://gonzalomunoz.org/publications/)
  corroborate the Bienstock–Muñoz metadata.
- The [Caltech publication feed](https://feeds.library.caltech.edu/people/Low-S-H/article.html)
  and [Lavaei publication list](https://lavaei.ieor.berkeley.edu/Publication.html)
  corroborate the Lavaei–Low volume, issue, pages, year, and DOI.

## Actual validation

All four commands completed with exit code zero:

| Check | Execution log | Scope confirmed |
|---|---|---|
| Resistive | `verification/stage04-resistive.log` | 12,751 profiles; 606 solutions |
| AC | `verification/stage04-ac.log` | 2,112 pairs; 14,784 cosine checks; 177,168 cycles; 648 sign cases |
| Developments | `verification/stage04-developments.log` | Generalized gadgets, three subdivision scales, 360 perturbations, k=0,...,10 recurrence, 100 quantitative profiles |
| Arithmetic | `verification/stage04-arithmetic.log` | 1,681 composed profiles; full 332-variable/330-equation circuit; dyadic and simplex profiles |

The final `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build
main.tex` completed with exit code zero. `build/main.log` has no warnings,
undefined references/citations, overfull boxes, or underfull boxes. The PDF is
28 pages. The command log is `verification/stage04-build.log`.

`verification/stage04-accepted-content-check.json` records unchanged accepted
content, the sole version-specific citation change, unique labels, resolved
cross-reference uses, and the clean build result. The complete extracted
layout is in `verification/stage04-layout.txt`. I visually inspected rendered
pages 1, 27, and 28, including the abstract, eight-example table, and final
bibliography; the table and references are legible and fit their pages.

The process status file was not edited, and no review snapshot was frozen
by the author. Only `paper-power-flow/` was edited.
