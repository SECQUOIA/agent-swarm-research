# Stage 3 corrections

Date: 2026-09-13. Correction author: `/root/stage03_corrections`.

I read the coordinator's first-round assessment and the cited reports from
reviewers 1 and 4. Both accepted minor findings are corrected in
`appendices/approximation.tex`:

1. The predecessor reduction now explicitly assumes scalar observations and
   one parameter (`p=1`), with cardinality as its only constraint. It states
   that cardinalities below zero or above `n` are infeasible, returns the empty
   schedule for `k=0`, and handles identically zero sensitivities by choosing
   any feasible schedule. The nontrivial construction then assumes
   `1 <= k <= n` and at least one nonzero sensitivity. The upper bound makes
   the later cardinality padding explicit.
2. “Published theorem” is now “stated theorem,” consistent with the inspected
   and cited preprint version.

No other manuscript mathematics was changed. No original tracked source or
unrelated manuscript was edited.

Validation: ran
`latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex`
from the paper directory. The build succeeded and produced a 36-page PDF.
The final log contains no warnings, undefined references, or overfull or
underfull boxes. These wording and scope corrections do not require new
computational tests.
