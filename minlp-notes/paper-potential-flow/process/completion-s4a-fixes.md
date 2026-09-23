# S4a correction record

The separate correction agent applied the two minor findings accepted in
`completion-s4a-adjudication.md`. The only manuscript file changed was
`complexity/sections/06-weighted.tex`.

1. The Brandenberg–Stursberg comparison now states both quantifier levels:
   each differential-flow polytope fixes its positive elasticity vector,
   while the universal nondegeneracy characterization quantifies over all
   positive elasticity vectors and all nomination/capacity bounds.
2. The universal hull theorem now specifies rational nominations and
   objective coefficients and strictly positive rational resistances, all
   of polynomial encoding length. The quadratic convex-region theorem
   specifies rational nominations and strictly positive rational
   resistances, with the same polynomial encoding qualification. The
   nonlinear-power extension specifies existence of rational nominations
   and strictly positive rational resistances and retains its explicit
   absence of a uniform encoding bound or algorithmic claim. The
   positive-width extension retains its existence-only qualification.

These wording changes preserve the mathematical statements, constructions,
proofs, and encoding distinctions. Earlier accepted sections, Paper B, and
the literature store were not edited. Existing uncommitted changes were
preserved. Unchanged mathematics regression tests were not repeated.

Validation imported `verification/build_and_check.py` and called only
`build('complexity')`; its CLI was not invoked. The refreshed
`completion-s4a-build.json` records all 13 source hashes and confirms a
successful build, an existing PDF, zero errors, zero unresolved references,
zero unresolved citations, zero duplicate labels, and zero overfull boxes.
All 12 other source hashes match the pre-correction build record.

The corrected Section 6 SHA-256 is
`20030371746b874b82e7704767b33e18e05216373d02dd755d79927a08d47904`.

Authored or refreshed files:

- `complexity/sections/06-weighted.tex`
- `process/completion-s4a-fixes.md`
- `process/completion-s4a-build.json`

The build also refreshed generated outputs under `complexity/build/`.
