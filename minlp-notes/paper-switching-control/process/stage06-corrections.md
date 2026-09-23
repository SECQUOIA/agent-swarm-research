# Stage 6 notation correction

Read the primary adjudication and reviewer 02's finding, which consolidates
the same minor ambiguity reported by reviewers 01 and 05.

In `sections/12-computations.tex`, changed the deterministic input formula
from `1+((j+2)(i+3)+i^2\bmod 11)` to
`1+\bigl(((j+2)(i+3)+i^2)\bmod 11\bigr)`. The entire sum is explicitly
the operand of the modulo operation. No numerical data, algorithm, theorem,
or other prose was changed.

Validation:

- `python verification/stage06/render_results.py --check` passed. Generated
  tables and timing macros remain unchanged.
- A clean LaTeX rebuild with `latexmk -gg -pdf -interaction=nonstopmode
  -halt-on-error main.tex` passed. A subsequent final rebuild also passed.
  The manuscript has 56 pages; the final log has no warnings, undefined
  references, or overfull/underfull boxes.
- Inspected page 50. The formula wraps at a permitted arithmetic break,
  retains explicit grouping of the entire modulo operand, and fits the text
  area. A trial nonbreaking group caused overflow and was removed; the
  final source uses precisely the requested expression.
- All 161 frozen stage 6 round 1 file hashes remain unchanged. Archived
  numerical data and generated table/macro files match the frozen copies.

Evidence: `verification/stage06/corrections-generated-text.log`,
`corrections-build.log`, `corrections-final-build.log`, and
`corrections-page50.png`. No numerical experiments or broad mathematical
verification were repeated. No snapshot was edited.

The correction is complete. All writes have stopped. Ready for the primary
agent to freeze the manuscript for the full review.
