# Stage 1, round 1 — independent reviewer 4

Reviewed snapshot: `process/snapshots/stage01-round01`.

## Verdict

**Accept this stage: no major or minor defects identified.** The foundations
are mathematically complete within the assigned scope, and their attribution
does not overstate novelty. This verdict does not cover the intentionally
unwritten compression, separation, coefficient, or computational results.

## Enumerated findings

1. **R4-S01-01 — No actionable finding.** I found no invalid assertion, essential
   missing argument, or material omission within the current-stage scope.

## Mathematical checks

- **Model and disaggregation, Section 2.** I checked both directions of
  Proposition 2.1 directly. The linear lifted system contains each graph point;
  conversely, positive state weights yield normalized feasible flows and
  simplex-vertex graph points. The observation identity holds separately at
  positive and zero weights. Since at least one weight is positive, an empty
  flow polytope cannot acquire a spurious feasible lift. The finite capacity
  assumption is precisely what makes every zero-weight state flow zero.
  The stated bound of at most `m+1` graph points is valid even when normalized
  state flows are not vertices of the flow polytope: membership in the graph,
  not extremality, is sufficient.
- **Degeneracies.** I traced the assertions for `m=0`, no observations, no cyclic
  blocks, isolated vertices, zero capacities, self-loops, parallel arcs, and
  disconnected networks. Component balance is checked before choosing the
  reference vector. The empty product convention correctly handles a feasible
  forest, whose flow polytope is a singleton. Ambient rank is explicitly
  distinguished from capacity-induced affine dimension.
- **Reference vector and block factorization, Section 3.1.** The fundamental
  cut construction yields `Av=b` without any unstated capacity feasibility.
  Rational component sums have polynomial encoding length; a tree traversal
  computes all such sums in linear arithmetic work. Cancelling nonforest
  coordinates against fundamental cycles leaves a forest-supported circulation,
  which is zero. Each cycle is in one cyclic block, so the resulting block
  restrictions are circulations even at articulation vertices. Conversely,
  zero extensions of block circulations have zero incidence separately. Thus
  the asserted affine Cartesian product, including its bridge obstruction,
  follows without an unmentioned articulation coupling condition.
- **Local mergers, Section 3.2.** The theorem assumes nonempty `P`, which
  supplies nonempty `K_B` and makes its scalar-set notation legitimate.
  Each block may merge a different set of global labels: proportional
  refinement preserves the same global weights and each block's domain, so
  the independent block circulations combine into each global state flow.
  When a merged weight is zero, all its constituent weights are zero and its
  local vector is zero. A structurally observed label of zero candidate weight
  is retained and constrained correctly. The linear version of the scaled
  domain remains exact when the reference vector lies outside the capacity box.
- **Counterexample and limitation.** In Example 3.3, both original intervals
  really equal `[0,1]`; the aggregated interval contains `2`, since its upper
  bounds are `50.5` and `25.5`. This demonstrates the stated common-matrix
  boundary. The final side-constraint paragraph correctly limits the hull
  exactness claim and avoids importing that property into arbitrary coupled
  models.
- **Coefficient and complexity wording.** No current-stage claim confuses
  numerical coefficient magnitude with bit length, or linear arithmetic work
  with bit complexity. Generic polynomial optimization/separation follows from
  the explicit polynomial-size rational LP and is correctly described as known.
  The ratio sentence asserts only scaling invariance and does not yet claim
  uniqueness of ambient facet coefficients modulo affine equations.

## Scope and source checks

I compared the relevant proof and scope material in
`notes/network-simplex-reopened-compressed-hull.md`,
`notes/network-simplex-reopened-literature.md`, and
`notes/network-simplex-reaggregation-source-boundary.md`. The block and merger
arguments retain the material assumptions from those notes and expand their
proofs enough to read independently. Path suppression and rank elimination are
properly deferred to later stages rather than silently asserted here.

I independently located Proposition 2.6 in the
[2016 Davarnia dissertation](https://ufdcimages.uflib.ufl.edu/UF/E0/05/02/79/00001/DAVARNIA_D.pdf),
printed pages 28–29: it concerns Cartesian component domains sharing one
simplex. The manuscript correctly distinguishes that locator from the 2017
journal article. I checked the 2017 article's bibliographic identity against
the [publisher entry](https://epubs.siam.org/doi/pdf/10.1137/16M1066166?download=true)
and the author's publication list. I also checked equation (7) and its following
paragraph in [Kis–Horváth](https://link.springer.com/article/10.1007/s10107-021-01652-z);
they explicitly say common-matrix right-hand-side aggregation need not give
the union hull. That supports the manuscript's limited attribution.

## Build and limitations

A private copy in `verification/reviewer4/stage01-round01/build` compiled with
`latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`, producing seven
pages. The final log contains no undefined-reference, citation, overfull,
underfull, or other warning matches. An initial tool invocation attempted to
use the private build directory before it existed; after creating the
directory, the actual build succeeded. This was a review harness error, not a
manuscript defect.

I did not run numerical tests: the retained foundational statements are
elementary exact identities and were checked symbolically. I did not independently
re-audit every future-facing literature comparison or every bibliography DOI;
those are limitations, not adverse findings. I read no other current-round
review, edited no manuscript source, and spawned no agents.
