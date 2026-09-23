# Stage 3 corrections

Completed 2026-09-13 by the correction agent, distinct from the author. Read
`stage03-adjudication.md` and `stage03-review4.md`. Addressed the one accepted
minor finding: direct attribution of Lean and mathlib.

## Changes and verified sources

- Added a direct Lean 4 citation at its first substantive mention in
  `sections/05-formalization.tex`. The new `demoura2021-lean4` bibliography
  record credits Leonardo de Moura and Sebastian Ullrich, *The Lean 4 Theorem
  Prover and Programming Language*, CADE 28, LNCS 12699, 625–635 (2021), DOI
  [10.1007/978-3-030-79876-5_37](https://link.springer.com/chapter/10.1007/978-3-030-79876-5_37).
  The primary Springer record was opened and its authors, title, year, volume,
  page range, and DOI verified.
- Added a direct mathlib citation at its first substantive mention in the
  section's build paragraph. The new `mathlib2020` record follows the current
  [official mathlib4 citation guidance](https://raw.githubusercontent.com/leanprover-community/mathlib4/master/CITATION.md):
  The mathlib Community, *The Lean Mathematical Library*, CPP 2020, DOI
  [10.1145/3372885.3373824](https://doi.org/10.1145/3372885.3373824).
  The page range 367–381 was checked against the project's
  [mathlib3 citation record](https://github.com/leanprover-community/mathlib3/blob/master/CITATION.md).
  The primary [community-hosted paper](https://leanprover-community.github.io/papers/mathlib-paper.pdf)
  independently confirms the title, collective authorship, venue, year, and DOI.
  The ACM page returned HTTP 403; no access was bypassed. The 2020 paper is the
  project's recommended attribution, while the separately stated version pin
  identifies the actual modern dependency.

The Lean 4.33.1 and mathlib 4.33.1 version pins remain unchanged. No formal
source, prior manuscript section, or acceptance status was changed. The only
substantive edited files are Section 5 and the paper bibliography.

## Validation

Built a fresh isolated source copy in `build/stage03-corrections/` using
`latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`. The build
returned zero and produced a 23-page PDF. The transcript is
`process/stage03-corrections-build.log`. The final LaTeX log has no warnings,
undefined references/citations, or overfull/underfull boxes. Both new keys occur
in the generated bibliography, and PDF text extraction succeeded.

Ran `sha256sum -c verification/SHA256SUMS` in the formal directory: all 13
source/configuration/documentation files match the recorded hashes. No Lean
compilation was repeated for this citation-only correction. No new issue was
found; stage acceptance remains the coordinator's decision.
