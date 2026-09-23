# Preparation and review record

Completed on 2026-09-13. This is the preparing agent's local review, not a
new independent review or external peer review.

The note was written as a self-contained account of the original conjecture,
the sparse counterexample, its exact gap, and the matching leading degree
and dimension asymptotics. It includes its own definitions, probability-law
lemmas, finite certificate, attaining law, harmonic upper proof, box
transfer, and bibliography. No parent-paper section or external result note
is required to follow a proof.

The mathematical and specification review checked:

- The conjecture's positive-coefficient, nonnegative-box, uniform-constant
  scope and its published/author-manuscript numbering.
- The construction's distinct supports, interior means, exact termwise gap,
  global upper attainment, and positive hull gap.
- The shifted-cap inequality for arbitrary anchor selections and its
  telescoping sum, without assuming a special dependence between anchors.
- The exact cutoff law's full coordinate means, power-of-two failure counts,
  simultaneous block hits, equality cases, and attained lower envelope.
- The shared nature of the upper couplings, boundary marginals, easy cases,
  measurable harmonic densities, active-mass bound, nonempty integration
  window, rational union estimate, and nonnegative mixture contributions.
- The original-term inequality under box expansion, including fixed
  coordinates and repeated expanded supports.
- The leading constant and lower witnesses at every sufficiently large
  integer allowance, with unused-coordinate padding preserving both gaps.
- The correspondence of the coverage table's declaration names to the
  bundled source files, and explicit separation of written elementary
  calculations from formal endpoints.

All 11 PDF pages were rendered and inspected. The theorem statements,
displayed formulas, exact-value table, bibliography, and source-link table
were readable without clipping. A missing backslash in a harmonic-law
subscript was corrected during visual inspection; that page was rebuilt
and inspected again. The final LaTeX log has no warnings, overfull boxes,
unresolved references/citations, or duplicate labels. qpdf's structural
check also passed. Actual PDF link annotations and Markdown links are
checked by `scripts/check_bundle.py`.

The paper rebuilt outside the repository with identical extracted text.
The independent directory also compiled all 41 project proof modules from
an empty project build cache, using copies of the pinned standard
dependency caches. Import coverage, the 733-declaration axiom audit, and
kernel replay of the whole bundled project passed. See
[the formal record](../formal/VERIFICATION.md) and
[the paper build report](paper-build.json).

The general monomial lower-envelope identity, exact total support and
occurrence counts, sparsity asymptotics, and finite example table are
identified as written calculations rather than separate Lean endpoints.
The disproof, exact hull formula with attainment, explicit finite upper
bound used here, and sharp all-box limits are formalized. The note makes
no second-order, coefficient-removal, or publication-priority claim.
