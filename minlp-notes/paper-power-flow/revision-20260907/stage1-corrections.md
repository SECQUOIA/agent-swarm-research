# Stage 1 separate correction report

Read the root adjudication, all five Stage 1 review reports, the frozen introduction and bibliography, and the literature audit. Implemented every accepted minor correction group. No core theorem, proof, or mathematical scope changed.

## Changes

1. **Jeeninga locator (R1.1 / R4.2).** The introduction now cites Theorems 3.18 and 3.22 for convexity and the feasibility/interior alternatives.
2. **Network approximation scope (R2.1).** The Bienstock–Muñoz comparison now requires bounded treewidth and bounded numbers of local variables and constraints. Theorem 7 and Corollary 8 were directly checked in the primary local extraction; the version-specific locators remain correct.
3. **Rational-equivalence agreement (R2.2 / R3.1).** The introduction explicitly states that Dynamic Toolbox Definition 4 uses the same rational-coordinate notion, with forward and inverse maps defined on their respective sets. It identifies the broader-scope obstruction under that shared definition, without suggesting that denominators must stay nonzero everywhere in ambient space.
4. **Angular uniqueness (R4.1).** The Jafarpour comparison now qualifies uniqueness within each winding cell modulo a common rotation.
5. **Affine gadget explanation (R5.1).** The proof-strategy sentence now requires both prescribed voltage and prescribed injection.
6. **Ohmoto–Shiota publication metadata.** Converted the entry to a journal article: *Journal of Topology* 10(3), 765–775 (2017), DOI `10.1112/topo.12024`. Independently confirmed the metadata against the publisher and author records. Retained the inspected `arXiv:1505.03970v2` URL and added an explicit note that theorem and section numbering follows that version. Reread its Theorem 1.1 and Section 1.2 to verify the manuscript's locators. The journal full-text link returned an abstract page; no published numbering was inferred.
7. **Literature audit follow-up.** Added a clearly separated follow-up recording the additional checks. It resolves the JPT numbering question using the published CONICET PDF identified by reviewer 4. Downloaded and directly inspected journal page 242, which labels the relevant minimum bound Theorem 1.1; the numerical citation remains unchanged. Cached that primary PDF and text under `revision-20260907/sources/`. Original literature packages and historical reviewer/author reports remain untouched.

## Verification

- Built from `paper-power-flow` with `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex`. Successful output: `build/main.pdf`, 30 pages. Build transcript: `revision-20260907/stage1-corrections-build.log`.
- Checked the final LaTeX log and build transcript: no undefined references/citations, LaTeX warnings, or overfull/underfull box warnings.
- Compared the introduction and bibliography against `stage1-snapshot`: only the five accepted prose corrections and the Ohmoto–Shiota entry changed.
- Extracted the PDF text and visually inspected pages 2, 3, 4, and 30, covering all corrected introduction passages, the comparison table, and the amended bibliography entry. Layout and references are clean. Rendered pages are retained as `stage1-corrected-layout-*.png`.
- Unrelated manuscript edits were preserved. No subagents were dispatched and no new tests were added for these prose/bibliography changes.

All accepted Stage 1 corrections are complete. The scheduled later proof stages and final manuscript review remain necessary; this correction pass does not certify the unchanged core proofs.
