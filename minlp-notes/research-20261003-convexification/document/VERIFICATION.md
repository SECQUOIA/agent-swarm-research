# Targeted document verification

Only the current joint-convexification report is checked here. No
project-wide verification or CI inspection was performed.

The final report built successfully from the repository root with:

```sh
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error \
  research-20261003-convexification/document/main.tex
```

The parent agent ran this final build on 2026-10-03 at 05:17:30 UTC; it
exited with status 0. The final `main.log` contained no undefined citations
or references, no LaTeX warnings, and no overfull or underfull boxes.
`pdfinfo` reported 25 pages and 407,497 bytes. This PDF includes the final
prospective campaign, matched repair cohort, and negative recommendation
on default cut activation.

Targeted inline Python checks parsed the 11 TeX source files and the
bibliography: all 43 labels are unique, every reference and citation
resolves, and the bibliography contains 34 entries. Every local artifact
path in TeX and every local Markdown link in this directory's README,
claim map, and verification record resolves. The first path-check attempt
mistook the `\\pathref` macro's `#1` argument for a literal path; excluding
macro parameters corrected that checker without changing the document.

The final build log and document status wording were also inspected with
`rg`. PDF text extraction confirmed that the final repair table and its
counts appear in the built artifact. The parent agent inspected the title
and result pages, and the independent document reviewer inspected rendered
pages 20 and 21: the tables and surrounding text are readable.

The separation reviewer independently checked the proof in `separation.tex`:
support-distance duality with coordinate cones, normal-grid coverage,
rational barycentric domain coverage, support approximation error, and the
distinction between rational and binary64 separation. The implementation
owner confirmed that the proof and four mathematical return statuses match
the implemented API. The cardinality budgets are explicitly distinguished
from wall-clock and per-oracle face-enumeration limits.

The independent internal review also checked the aggregation theorem,
singular-face quadratic proof, constrained-star and overlap results,
source-model contract, completion boundaries, and numerical claims against
the archived experiment records. The final reviews are recorded in
[integration-review.md](../reviews/integration-review.md),
[experiment-review.md](../reviews/experiment-review.md), and
[final-contribution-review.md](../literature/final-contribution-review.md).
These are internal research checks, not external peer review or formal
verification. Software test commands and results are recorded separately
in the topic's [VERIFICATION.md](../VERIFICATION.md).
