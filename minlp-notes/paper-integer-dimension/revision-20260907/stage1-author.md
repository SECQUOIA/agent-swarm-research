# Stage 1 author report

Author work complete, pending the required five independent reviews.

## Changes

Rewrote `sections/00-introduction.tex` around three principal developments: (1) the exact nc-rank quadratic precision law; (2) the uniform finite covariance benchmark and polynomial rational construction; (3) scalar/vector integer-count comparisons with explicit description models. The opening explains why integer count, general integer ranges, continuous size, and rational description length differ. It now credits Lubin et al.'s minimum MICP rank at first use, specifies same-input graph containment, full-box domain and absolute error, explains the nc-rank shrinking characterization, and distinguishes finite two-bit scalar existence from the dense rational eleven-bit theorem.

Replaced the result-location catalogue with a compact prior-result/development comparison table, retained theorem links for all major extensions, and expanded source-specific discussion. Added Beach–Hildebrand–Huchette 2022 and Rebennack–Kallrath 2015 as important omitted predecessors. Added the published LinA 2025 article while retaining the older report key for the untouched scalar section. Updated IQS to published journal metadata with manuscript theorem-version note, and completed Lubin's issue/pages.

Only one explicit qualified priority assertion remains: the identification of nc-rank/2 with the quadratic minimum precision coefficient. It is limited to the exact stated model and supported by a concrete comparison to the inspected closest sources. Integer dimension, parity, logarithmic encodings, compact quadratic approximation, adaptive knots, chord estimates, greedy segmentation, shared SOS2, and algebraic/oracle primitives are credited as prior work.

`stage1-literature.md` records actual inspected passages, original-PDF spot checks, primary URLs, version and locator boundaries, searches, and access/scope limitations. No literature packages or historical reports were changed.

## Mathematical framing checks

Read the principal quadratic-system theorem and proof, symmetric shrinking lemma and proof, covariance lemma and finite covariance theorem, rational theorem statement/algorithm opening, scalar chord lemma and proof, and vector curvature-rank theorem statement/proof opening. The introduction's nc-rank, finite determinant, scalar two-bit, dense eleven-bit, and curvature-rank descriptions match those statements. No new proof defect was identified in this bounded framing audit. This does not replace the full technical stages.

The rank characterization is explicitly real for symmetric Hessian spaces, with a pointer to the manuscript's complex-to-real argument. It describes deficiency as the maximum loss and rank as its complement. Sparse encoding is attributed only to the positive separable polynomial result; the vector compiler is explicitly dense. No stronger efficiency guarantee is inferred from an existence count or oracle count.

## Validation

`latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex` completed successfully after bibliography updates; build log is `stage1-build.log`. `python verification/check_manuscript.py` reports no duplicate labels, unresolved references, duplicate bibliography keys, or unresolved citations (9 TeX files, 258 labels, 42 entries). Final source rerun and layout check are recorded below. The root separately reports 45 baseline technical checks passed; those are baseline confidence, not mathematical proof verification of this revision.

## Boundaries for later stages

The full finite-accuracy rational algorithm, scalar compact compiler, vector oracle interface, and all separation proofs still require their scheduled technical audits. Section 3 still cites the valid older LinA report; its author can decide whether the journal article should replace that exact source after checking locators. Existing technical imports outside the headline comparisons were not all reread in this framing stage. The open universal additive vector gap is retained as a nondependency research question, not represented as a solved result. No submission or authorship metadata was supplied.

Final rerun: 86-page PDF; no LaTeX overfull/underfull boxes, warnings, or undefined references in `build/main.log`. The final machine-readable reference result is `stage1-reference-check.json`. Visually inspected rendered pages 5 and 6 (`stage1-page5.png`, `stage1-page6.png`), including the contribution formulas and comparison table; text and table fit within the page without clipping. This is a focused changed-page inspection, not the scheduled whole-paper layout audit.
