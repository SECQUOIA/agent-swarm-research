# Corrections: Stage 03, round 01

Fixer: `/root/paper_stage_fixer`, distinct from the Stage 03 author. Date: 2026-09-07.

Input reviewed snapshot: `13abd3fbd62d1a6faf46617e4f678ed14ac22bacb42b8ff161f0ee27d67f0b00`, preserved in [snapshot.json](snapshot.json). I read the [coordinator adjudication](adjudication.md) and reviewer 5's R5-01. The adjudication accepts this single minor finding and identifies no major issue.

**R5-01:** In `sections/03-predetermined.tex`, lines 294, 295, and 298, changed the local subcritical normalization from `Z` to `Z_q` in the definition of `d_q`, the normalization integral, and the following displayed evaluation. The equilibrium normalization `Z=A+KP` remains unchanged. This is solely a consistent symbol replacement: the density, integral, coefficient, and mathematical argument are unchanged.

Verification:

- Forced the full LaTeX/BibTeX build with `latexmk -pdf -g -interaction=nonstopmode -halt-on-error -file-line-error main.tex` in the manuscript folder. It exited with status 0 and produced the 25-page PDF.
- Scanned the final `main.log`; no warnings, undefined-reference notices, or overfull/underfull boxes were present.
- Explicitly scanned the changed LaTeX file for trailing whitespace and tab characters and checked its final newline. These checks cover the untracked source directly and passed.
- Compared all twelve manifest-listed file hashes. Only the intended section changed. Reversing precisely the three requested substitutions reproduced its frozen hash, verifying that no other source edits occurred.
- Preserved the reviewed manifest, reports, and author handoff. No later-stage file or historical source note was edited.

Corrected section SHA-256: `8fd907c3c5d755ad7c4da1561e3379158a79e17790032119031158463cf5d15d`.

Editing is complete. No substantive issue emerged. The coordinator must verify this minor correction and separately record acceptance; this record does not accept Stage 03 or start the next stage.
