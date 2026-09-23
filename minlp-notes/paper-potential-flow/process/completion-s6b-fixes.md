# Stage 6b correction report

Status: all six consolidated minor findings and the additional lead certificate convention are corrected and validated. This report requests lead inspection; it does not accept S6b or replace the mandatory separate Stage 7 whole-manuscript review. No substantive scientific concern appeared.

## Repairs

1. **Main-model conventions:** `complexity/narrative/01-model.tex` now states coordinatewise `ell <= u` in the rational box data before the nonemptiness equivalence. Its maximum block rank is explicitly zero when there are no blocks. The weighted observable also states `c in Q^V` and balance separately, matching the corrected theorem wording.
2. **Positive per-block face bound:** `complexity/sections/00-introduction.tex` and `complexity/narrative/04-weighted.tex` use `r_0 >= 1` with `r_max <= r_0`, giving `O(r_0 p)` free coordinates and, where enumerated, `n^{O(r_0 p)}` faces. Total rank retains the symbol `r`. Figure 2 in `complexity/narrative/02-localization.tex` labels its selected block cyclic and states that bridge cases are handled directly. Its rendered page is readable and the longer label fits.
3. **Rational weighted input:** Theorem 5.1 in `complexity/narrative/04-weighted.tex` explicitly requires fixed positive rational asymmetric quadratic coefficients and states `c in Q^V` and `1^T c = 0` separately. The existing interval alternatives and output scopes remain intact.
4. **Sensitivity proof method:** `complexity/narrative/05-design.tex` describes Proposition I.8 as regularized electrical sensitivity and a limiting argument, retaining zero-flow and reversal coverage and the comparison with the weaker bound.
5. **Completed coverage:** `coverage.md` names the completed fixed-core applications in A03 (`lem:a-blk-boxlp`), A04 (`lem:a-law-dense`, `thm:a-law-polynomial`), and A06 (`thm:a-weight-global`), while excluding broader pooling applications. `process/completion-coverage.md` distinguishes the historical 18-section two-paper count from the current 308-file/13-included-section count and identifies A05 as included Appendix E. `verification/check_coverage.py` changes only its success wording to “included sections.”
6. **Dataset provenance:** `reproducibility/README.md` records the original INP header's Copyright 2018 KIOS Research and Innovation Center of Excellence, University of Cyprus notice and “Licensed under the EUPL,” with a direct source link. It preserves the synthetic transformation description and limits the notice to source data. The direct source returned HTTP 200 and SHA-256 `aa64abe37f578ab10feef59366d08e5e3a0b313ceb1ab34ff43ef4790e1802cd`, identical to the lead's original. No license version or repository-wide license was inferred; the original INP is excluded. The packaging script propagated the notice to the top-level archive README.
7. **Additional lead convention:** `complexity/narrative/06-certificates.tex` explicitly requires at least one edge before defining the minimum coefficient, retaining rational nominations and positive rational coefficients.

## Preservation and precise scope

The reviewed original manifest remains byte-identical with SHA-256 `a530e917bd4fee2ab9fd90af8f7c29ecddcbb64936abffab32b559f61c2dafb0`. Its 43 frozen files were verified before editing, and the lead's snapshot `/tmp/paper-a-s6b-before-fix.tar.gz` was used for the exact correction diff. Ten assigned source/documentation files changed; the three delivery files and Paper A build outputs were regenerated. Four new correction records are written. The lead separately appended the certificate convention to the adjudication during this work.

All 11 accepted technical sources, bibliography, original code/data, managed literature, Paper B nonbuild files, original S6b author/build/check/source/freeze records, retained exact/numerical evidence, and reviewer reports remain byte-identical. A pre-edit audit covered 3,613 nonbuild/nondist files; all 3,602 protected files compare identically after excluding the ten assigned edits and the lead-owned adjudication update. The A-only wrapper was used throughout; the two-paper build command was not invoked. No mathematical test or algorithm was changed.

The final manifest records current manuscript inputs, all archive payloads, the 308 inventoried research sources, and current delivery/process file hashes. It also records historical preservation and exact before/after hashes for each correction. Its self-hash is excluded to avoid circularity.

## Validation and evidence

- Repository Paper A build and a clean build from the final extracted archive both pass: zero errors, undefined references, undefined citations, duplicate labels, and overfull boxes. The corrected PDF has 216 pages, with 28 main-text pages.
- Coverage passes: `PASS: 308 inventory files and 13 included sections.`
- The final archive contains 63 hashed payloads plus its manifest. Every payload hash matches before and after extracted build, exact replay, and standalone repackaging. The extracted manuscript inputs match the final repository build inputs.
- All 18 exact replay commands pass from the final extracted archive using Python 3.12.14, including the existing `-S -O` checks. Their full commands and outputs are embedded in the new final-checks record. Original retained evidence files were not overwritten.
- Standalone repackaging succeeds from the extracted archive. All source/code/data/evidence payloads match; a fresh PDF may differ through build metadata.
- The earlier passing 28-command scientific suite is retained with its original SHA-256 and unchanged scientific source/data identities. It was not rerun for these prose-only changes. This is preserved evidence, not a claim of a new numerical run.
- Figure 2 on PDF page 11 was rendered and visually inspected. Extracted PDF text also confirms the changed model, face-bound, sensitivity, and certificate passages on pages 7, 18, 23, and 24.

Full machine-readable evidence is in `completion-s6b-final-build.json` and `completion-s6b-final-checks.json`; the correction freeze is `completion-s6b-final-manifest.json`. The lead will inspect preservation and delivery before deciding acceptance. Stage 7 remains required.

## Corrected delivery hashes

- PDF: `bda9cbb3407ac9e188574384f2efaf1739f00654c5ca83a7236c19e9dc612868`.
- Archive: `ccdb3657677749bba4e2aa3233ce159dfd90c0ddb3f8dbed21c0ad242a162978`.
