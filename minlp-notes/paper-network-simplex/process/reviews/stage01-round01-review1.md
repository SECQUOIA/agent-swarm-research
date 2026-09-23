# Stage 1, round 1 — independent review 1

**Verdict: accept this stage. No major or minor defects found.**

Reviewed the frozen snapshot `process/snapshots/stage01-round01`, including
`main.tex`, all of `sections/01-foundations.tex`, bibliography, and supporting
README. I did not read the other current-round reports or modify manuscript
sources. Future substantive sections are outside this stage and their absence
is not a defect.

## Enumerated findings

1. **S01R01-R1-F00 — no actionable finding.** The foundational mathematical
   assertions and their edge-case qualifications are correct as written.

## Mathematical checks

- **Exact disaggregation, lines 106–142.** I independently checked both
  implications. Lifting a graph point by `f^k=lambda_k x` and taking a convex
  projection proves the forward implication. Conversely, finite capacities
  force every zero-weight flow to zero, and each positive-weight flow divided
  by its weight belongs to `P`. The same at-most-`m+1` reconstruction matches
  every retained coordinate. This argument also handles `P` empty: a feasible
  lift would have at least one positive state, contradicting emptiness. The
  special definition `P(0)={0}` therefore does not accidentally admit a hull
  point when `P` is empty. With `m=0`, the only state has weight one and the
  formulation reduces exactly to `P`.
- **Residual state, lines 144–155.** The residual capacity bounds follow from
  eliminating `f^0`, and the warning against discarding them is necessary. For
  example, one free unit-capacity loop with one label permits `x=1,y=1,z=0`
  after dropping residual capacity bounds, whereas the actual hull requires
  `z=x` at `y=1`.
- **Reference flow, lines 173–190.** Componentwise zero balance is both
  necessary and sufficient for solving the unrestricted incidence equations.
  Fundamental-cut sums yield the asserted arithmetic and encoding bounds.
  The reference flow need not be capacity feasible; using translated
  circulation domains rather than assuming their origin feasible is correct.
- **Block factorization, lines 192–231.** The fundamental-cycle basis proof
  is sound for arbitrary orientations, disconnected graphs, parallel pairs,
  and loops. Every undirected simple cycle lies within a cyclic block; hence
  restricting a global circulation to a block preserves zero divergence even
  at an articulation vertex. Conversely, extension by zero preserves all
  incidence equations. Edge-disjointness supplies the direct sum and affine
  bijection. Fixed bridge values, empty block domains, and the empty family
  convention correctly cover forests and isolated vertices. Rank is rightly
  kept distinct from capacity-restricted affine dimension.
- **Homothetic merger, lines 233–259.** The stated identity uses a nonempty
  convex set, explicitly handles total weight zero, and never equates a
  Minkowski sum of unrelated right-hand-side slices with their aggregation.
  Keeping observed labels structurally present at zero candidate weight is
  correct.
- **Exact local-to-global recovery, lines 261–323.** Proportional refinement
  assigns an unobserved state a member of precisely `lambda_k K_B`; local
  weights sum to the corresponding global weights. This remains true when
  the merged weight is zero. Different mergers in different blocks do not
  conflict because the refined deviations are independent circulations and
  use one common global state index. Adding `lambda_k v` gives correct
  balances and capacity bounds on blocks and bridges. Observed coordinates
  survive because their labels were not merged. Thus recovery invokes the
  disaggregation proposition without an unproved gluing assumption.
- **Boundary example and side-constraint warning, lines 330 onward.** Both
  original one-dimensional domains equal `[0,1]`; averaged rows permit
  `q=2` (indeed up to `51/2`). This is a valid counterexample to the stronger
  common-matrix claim. The final warning concerning intersection with extra
  constraints is mathematically appropriate.

## Attribution and presentation checks

The manuscript treats disaggregation and shared-simplex gluing as established
results, rather than presenting elementary specializations as new general
principles. I independently consulted:

- The original [Davarnia dissertation](https://ufdcimages.uflib.ufl.edu/UF/E0/05/02/79/00001/DAVARNIA_D.pdf),
  Proposition 2.6 (printed pages 28–29), confirming the Cartesian-component
  shared-simplex convexification locator and its applicability here.
- The repository's primary full text of Kis–Horváth, Section 2, confirming
  the distinction between the common-matrix aggregation relaxation and exact
  disjunctive convexification.
- The [published Almoghrabi–Skutella–Warode article](https://link.springer.com/article/10.1007/s10107-026-02392-8),
  Remark 1, confirming that the cited numbered remark distinguishes aggregate
  arc-flow decompositions from individual-commodity vector decompositions.
  The online publication date and authors match the bibliography.

I also read the relevant discussion in the repository's primary
Davarnia–Richard–Tawarmalani full text. I did not independently verify every
bibliographic field or the precise Khademnia–Davarnia Appendix locator: the
NSF PDF endpoint failed during this review. That access failure is not evidence
of an error, and no stage theorem depends on trusting that locator instead of
the supplied direct proof.

The distinction between arithmetic operations and encoding length, the
scope of graph assumptions after modeling transformations, and the
separation definition are clear. No unjustified claim of novelty or
computational speedup occurs in this stage.

## Build and limitations

A private copy compiled successfully with the documented `latexmk` invocation:
seven PDF pages, no remaining LaTeX warnings or overfull/underfull boxes in the
final log. Artifacts are under
`verification/reviewer1/stage01-round01/`; no production build was edited.

This review is a direct proof audit, with symbolic edge-case checks and a
private compilation. I did not run numerical experiments, inspect later
sections, or claim an exhaustive literature search. Those are unnecessary for
accepting the foundational assertions established explicitly in this stage.
