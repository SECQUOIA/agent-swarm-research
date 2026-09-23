# S3 accepted corrections

Date: 2026-09-10. Applied by a correction agent distinct from the S3 author after reading `completion-s3-adjudication.md`.

## S3-C1

In `complexity/sections/05-boundaries.tex`, the equivalence in `thm:a-bound-arc-srs` now explicitly concerns weak lower comparison of the designated probe flow oriented from the unit source to the unit sink. The converse calls this the probe flow. These changes state the scope already proved; they change no construction or argument.

## S3-C2

Added `hasler1993-parameter-tolerances` to `complexity/references.bib` and cited it in the envelope-priority discussion. The entry records M. Hasler and C. Wang, *Parameter tolerances in non-linear resistive circuits: worst case analysis based on monotonicity*, International Symposium on Nonlinear Theory and its Applications, Hawaii, USA, 1993, pp. 841–846. The metadata were checked against reference 2 in the local primary manuscript `literature/papers/pastore2016-dc-tolerance-analysis-of-electronic/fulltext.md`, line 508. No DOI was added.

The discussion explicitly states that the 1993 full text has not been read and that no theorem-level priority conclusion is drawn from it. No literature index or read status changed.

## Verification

Called the existing `verification/build_and_check.py` API as `build('complexity')`, building Paper A only. The command `latexmk -g -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex` returned exit code 0 and produced the PDF. The final log has no errors, undefined references, undefined citations, duplicate labels, or overfull boxes. BibTeX reports no warnings. There are 19 underfull boxes, all in existing bibliography entries; none occurs in the revised section or the new Hasler–Wang entry.

Refreshed `completion-s3-build.json` with the build diagnostics and all 13 current input SHA-256 hashes. Only the section and bibliography input hashes changed from the reviewed S3 build. Checked all pre-existing non-build files under `paper-potential-flow` against a snapshot taken before these edits: only those two source files and the S3 build record changed during the correction pass. Accepted Sections 01–04, Paper B, and existing uncommitted work were preserved. A later, concurrent lead update to `completion-literature-screen.md` was also preserved.

No mathematical or numerical tests were rerun for these wording and citation corrections. `git diff --check` passed. No staging operation or commit was performed.
