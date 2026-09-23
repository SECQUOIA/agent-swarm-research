# Corrections: Stage 06, round 01

Fixer: `/root/paper_stage_fixer`, distinct from the Stage 06 author. Date: 2026-09-07.

Input reviewed snapshot: `fd49a0c7de991734f21f20428b8a74ba19e44a0ffa3204ed80a925056ab5fb2f`, preserved in [snapshot.json](snapshot.json). The [coordinator adjudication](adjudication.md) accepts one minor finding shared by R1-01, R3-01, R4-01, and R5-01; no major issue was identified.

Correction: in `sections/06-finite-precision.tex`, lines 444 and 448–450, named the corresponding fold site `s_j`, stated the exact coordinate `z=2 sin((s-s_j)/2)`, and replaced the incorrect `eq:fold-scaling` reference by the proof of `lem:cosine-uniform`. The cited proof in Section 2 contains that substitution (with its local coordinate named y) and the bounded metric factors. The local squared potential, every estimate, and all theorem statements are unchanged.

Verification:

- Forced the LaTeX/BibTeX build with `latexmk -pdf -g -interaction=nonstopmode -halt-on-error -file-line-error main.tex` in the manuscript folder. It exited with status 0 and produced the 45-page PDF.
- Scanned the final `main.log`: no warnings, undefined-reference notices, or overfull/underfull boxes. Confirmed that the corrected reference label exists in the Section 2 source and inspected its proof.
- Explicitly scanned every line and byte of the changed LaTeX source for trailing whitespace and control bytes other than newlines, and checked its final newline. These checks cover the untracked source directly and passed.
- Compared all sixteen manifest-listed file hashes. Only `sections/06-finite-precision.tex` differs. Reversing the coordinate/reference correction and its fold-site definition exactly reproduces the frozen section hash.
- Preserved the reviewed snapshot, reports, and handoff. The only authored file changes are the section above and this correction record; the build also regenerated its ordinary output artifacts. No later-stage file or historical source note was edited.

Corrected section SHA-256: `5e556d104eb9b6ce78b2c8ebce3378f0ee092999f91f91520e40e98b6f44baec`.

Editing is complete. No substantive issue emerged. The coordinator must verify the minor correction and separately record acceptance; this record does not accept Stage 06 or begin Stage 07.
