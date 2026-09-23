# Stage 1 correction report

All eight corrections accepted in `stage1-adjudication.md` are implemented.

1. The LinA comparison acknowledges continuity for convex corridors and
   states both the continuously differentiable boundary assumptions and
   the per-maximal-segment function/derivative oracle cost.
2. The eleven-bit compiler summary specifies `[0,1]`, dense rational
   polynomial data, and a positive rational tolerance included in input
   length.
3. Both introductory mentions of binary union encodings are qualified by
   boundedness. The precise Vielma citation adds rationality and separately
   points to our elementary real-coefficient version.
4. The curvature-rank summary states the logarithmic overhead plus an
   absolute constant for positive rank and the zero-bit affine case.
5. The main quadratic statement defines the input dimension through
   `B` contained in `R^n` before using the shrinking formula.
6. The shrinking explanation identifies coefficients in `{0,1/2,1}` as
   summing to half the noncommutative rank, avoiding the incorrect reading
   that the discretization depths themselves have that sum.
7. The IQS entry preserves the exact published “non-commutative” title and
   links the inspected arXiv v6 used for theorem locators.
8. A short mixed-integer extension-complexity paragraph credits Cevallos,
   Weltge, Zenklusen and Schade, Sinha, Weltge. It distinguishes their
   inequality counts and projected mixed-integer hulls from our rational
   bit counts and graph-band containment with unrestricted convex lifts.

`stage1-correction-literature.md` records independently inspected primary
models, theorem statements, source versions and locators, metadata, and
limits. No technical sections, historical reports, literature packages,
or other papers were modified. No additional mathematical claim or
priority assertion was introduced.

Validation: `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build
main.tex` succeeded and produced an 86-page PDF. The final `build/main.log`
contains no warnings, overfull boxes, or underfull boxes.
`verification/check_manuscript.py` reports 9 TeX files, 258 labels, and
44 bibliography entries, with no duplicate labels/keys or unresolved
references/citations. Logs are `stage1-correction-build.log` and
`stage1-correction-reference-check.json`. This is correction validation;
it does not substitute for the scheduled technical and whole-paper audits.
