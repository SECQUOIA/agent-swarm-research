# Geometry and lower-bound validation

The following targeted commands were run from `paper-exact-penalties/`:

```sh
python3 verification/check_lower_bound.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
pdftotext -layout main.pdf verification/main-text.txt
pdfinfo main.pdf
```

The exact arithmetic script passed 70 projected-envelope cases, 490
symmetric fixed-multiplier cases, and 81 scalar balanced-ratio identities,
plus accuracy thresholds, strict margins, chain values, numerator bit counts,
exponent arithmetic for the fractional-power example, and the source
example's continuous-branch completed-square identity. Its output is in
`verification/lower-bound-results.txt`. It independently maximizes finite
projected envelopes by enumerating line intersections rather than using
the manuscript's proposed multiplier alone.

The LaTeX build produced a six-page PDF. A targeted inspection of the final
log found no unresolved references or citations, TeX errors, or overfull
boxes. The initial build had three underfull bibliography boxes; the reviewed
revision has none. A source-line check found no trailing whitespace in the manuscript
and bibliography. Text extraction was checked for readability and equation
ordering. The author field is empty.

The general mathematical statements were checked against their proofs and
the primary source text; the finite script is not a proof for all dimensions.
No project-wide checks, CI inspection, or new formal verification were run.

After the independent review, the modified script and LaTeX build were rerun
successfully with the same numerical case counts. The symmetric count is now
computed by the script. The reviewed PDF remains six pages and the final log
has no underfull or overfull boxes, unresolved references or citations, or
TeX errors. A targeted source-path check confirmed that every explicit
Markdown, Python and Lean source path in the coverage map exists. The
changes and review judgments are recorded in `evidence/stage1-review.md`.
