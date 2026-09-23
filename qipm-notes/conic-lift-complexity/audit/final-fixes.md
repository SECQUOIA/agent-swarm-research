# Final manuscript corrections

Applied all three minor corrections accepted in `final-assessment.md`.

1. Added the standing sentence “Throughout, cone-dimension and matrix-order
   caps are integers.” immediately after the section heading in
   `sections/01-foundations.tex`. This also covers the implicit cap
   conventions in Sections 05 and 06 without repeating the qualification.
2. Changed the opening of `cor:tree-cap-parameter` in
   `sections/07-concrete-barriers.tex` to “Fix an integer Lorentz dimension
   cap”.
3. Changed the several-independent-search construction in
   `sections/12d-query-output.tex` to require “an integer cap” before
   its displayed range `3 <= d < s+1`.

These edits only make the intended discrete cap hypotheses explicit.
No proof, formula, bibliography entry, or unrelated prose was changed.
Historical review reports and the root assessment were preserved.

## Verification

Ran `conda run -n qipm --live-stream make clean`, followed by
`conda run -n qipm --live-stream make`; both exited successfully.
The clean and full build outputs are retained in `final-clean.log` and
`final-build.log`. The resulting `main.pdf` has 183 pages.

A separate validation with the qipm Python interpreter confirmed that
all 35 section files are included, all 499 labels are unique, all
references resolve, and all 87 bibliography entries are cited and appear
in the generated bibliography. There are no duplicate bibliography keys,
missing citation entries, or uncited entries. The final LaTeX log contains
no warnings, undefined references, multiply defined labels, or overfull
or underfull boxes. Counts and validation results are retained in
`final-validation.json`.

The PDF and build artifacts remain available for root inspection.
