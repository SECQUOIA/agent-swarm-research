# Stage 4 author report

The author pass covers all of `sections/04-vector.tex`, including every proof,
its scalar and quadratic dependencies, and integration through the abstract,
introduction, conclusion, bibliography and manuscript documentation. The earlier
stage records were read for scope; their acceptance was not treated as evidence
of mathematical correctness. This report completes the author pass, before the
required five independent reviews.

## Changes

- Added a short roadmap explaining why the vector analysis proceeds from output
  count to original-output curvature rank, then to positive-polar and effective
  error-body bases. Added the two-spanner explanation: the sum of polar directions
  and the inner polytope account for the two rank factors in the refinement count.
- Made the abstract and conclusion distinguish the finite two-bit scalar result
  from the eleven-bit polynomial rational dense-polynomial result. The abstract
  now states the input-dimension dependence for separable vectors and the explicit
  linear output of the strong-oracle construction. The introduction states the
  oracle bound `17 + 2 ceil(log2 r)` while retaining its qualified main novelty claim.
- Updated Plevrakis–Hazan to the published NeurIPS 2020 entry, with official
  proceedings metadata. Its relevant running-time discussion is Section 3.3 in
  that version, replacing the preprint's Section 3.2. Added exact preprint-version
  notes for the inspected Lyu, Ellenberg–Gijswijt and Averkov–Weismantel locators.
- Shortened the discussion of possible approaches to the one-input box question.
  It retains the proved lattice-free projection observation and the material
  Helly/Radon distinctions; it states explicitly that no proved comparison depends
  on that research question. Every theorem, proposition, example and label is
  preserved. The removed remarks about oscillatory substitutions were not used
  by any proof or claimed as a theorem.
- Marked the earlier fifteen-reviewer stage gates as historical without removing
  their records. README links to the current process. Added SUBMISSION-README.md
  for the eventual standalone source bundle. The author block remains blank as
  explicitly requested; no authorship, funding or declaration was invented.

## Mathematical audit

I reconstructed the complete argument, not only the altered text. The checks
included level refinement and finite cover trimming; deterministic monotone mass
queries and common-denominator sorted access; all directed output bands and hybrid
cell constants; finite and rational original-output spanners; maximum-product
allocation and its factor-seven support bound; effective-image radii and pulled-back
separators; fixed-grid oracle exchange, objective accuracy and central repair;
positive-polar weak separation; both error-body spanners and rounding inside the
exact nonlinear image; the shared separable basis and product-code packing; every
finite/compiled table constant; positive-power thirds and cap-set restrictions;
all integer sections of the degree-32 product construction and its exact counts;
Bernstein convexity and perturbation margins; the triangular-wave dense polynomial
family; arbitrary signed polynomial overlays; the tilted-body curvature and
conditioning estimates; and the simplex-band comparison.

Particular dependencies were checked directly in the accepted technical source:
the contact closures and finite-mixture lemma, scalar packing `N_tau <= 6P`,
Jensen superadditivity, hybrid counts `486 N_tau` and `1458 2^p`, the indexed
compiler and deterministic mass bisection, and the exactly feasible block logdet
oracle used by maximum-product allocation. All vector complexity claims use dense
polynomials, polynomial-length tolerances and the supplied rational oracle data;
they do not inherit a sparse huge-degree evaluation claim. The effective image
is essential: rounding original output coordinates would not justify the oracle
band. Unbounded integer labels and all mixtures within integer sections are
retained in the separation arguments.

No theorem required correction, narrowing or an additional unproved premise.
The open questions are scope boundaries, not gaps in the proved claims. No new
priority assertion was introduced: spanners, polar oracle equivalences, SOS2,
cap-set bounds and difference-of-convex decomposition remain attributed methods.

## Validation

`stage4-reference-check.json` passes with 258 labels and 44 bibliography entries,
without duplicate or unresolved labels/citations. `stage4-build.log` records a
successful 88-page build; the final `main.log` and `main.blg` contain no warnings
or overfull/underfull boxes. Root will perform the final whole-paper visual and
standalone-package checks after review.

No theorem, algorithm or numerical constant was changed. The 45 successful
baseline scripts were therefore not repeated and no implementation-mirroring
tests were added. The verification in this author stage is a complete mathematical
reading and a focused primary-source audit, not formal verification. No other
paper directory or generated literature metadata was edited.
