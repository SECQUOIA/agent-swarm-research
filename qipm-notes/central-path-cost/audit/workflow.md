# Authoring and independent review record

The user requested staged development, an author agent followed by five
independent reviewers for each stage, a separate repair agent for every valid
finding, and another five-reviewer round whenever a valid major issue occurs.
The final integrated manuscript receives the same full-review cycle.

The source map records scope and section ownership. Reviewers must not read
one another's reports before submitting their own. The root assesses each
finding rather than accepting a vote count. Optional preferences are
distinguished from errors or deficiencies in the stated publication standard.

## Stage 1: foundations and exact distance

- Author: `stage1_author`.
- Delivered: complete foundations and exact-distance sections; standalone
  build; source map; literature evidence. Eight-page interim PDF built cleanly.
- Review round 1: `reviewer1` through `reviewer5`, dispatched independently.
- Root assessment: all five independent reviews found no major issue.
  Accepted all distinct required minor findings: explicit barrier/radius
  hypotheses in the optimal-movement corollary; explicit nontrivial accuracy
  and radius ranges in the logarithmic-allocation corollary; definitions of
  Peirce spaces and a direct justification of the Jordan inversion derivative;
  and specification of the primal--dual metric in the Nesterov--Todd comparison.
  The intended statements and proof constants are unchanged. A short primitive
  idempotent definition was also accepted as a useful optional clarification.
- Repairs: separate agent `stage1_fixer` implemented every accepted finding.
  The Jordan calculation now differentiates `z circ z^{-1}=e`, states the
  positive eigenvalues of `L_z` on the Peirce spaces, and solves there directly;
  the vague power-series/scaling alternative was removed.
- Validation: `conda run -n qipm --live-stream make` succeeded. The corrected
  interim PDF has nine pages. Final `main.log` has no warnings, undefined
  references/citations, overfull boxes, or underfull boxes. The repair changes
  were inspected against the assessed findings.
- Stage complete after the minor repairs. No further five-reviewer round is
  required by the requested process because the independent review found no
  major issue. Later integration remains subject to the full-manuscript review.

## Later stages

2. Sharp standard-barrier centrality, accuracy comparison, weighted profiles,
   and finite-sequence separation.
3. Scalar, canonical, and coupled barrier dependence, including any verified
   new radial upper bounds.
4. Primal–dual completion and the directly relevant formulation/movement
   consequences.
5. Final synthesis, literature/novelty statements, figures and reproducible
   checks, publication metadata and full-manuscript review.

No review-completion claim is made for a pending stage.

## Stage 2: sharp centrality, distributions, and finite sequences

- Author: `stage2_author`. Completed standard-barrier sharp centrality,
  objective-distribution movement laws, finite dyadic sequences, and scalar
  rational certificates. New development strengthened the determinant
  certificate and resolved a uniform growing-tube proof using the same dyadic
  family throughout. Root feedback on the residual restriction and same-start
  unequal-scale comparison was incorporated before review. Exact certificate
  and numerical cross-check scripts passed in qipm; the integrated PDF had
  20 pages.
- Review round 1: `reviewer1` through `reviewer5`, dispatched independently;
  all five reports are recorded as `audit/stage2-review1.md` through
  `audit/stage2-review5.md`.
- Root assessment: no major issues. Accepted every distinct minor finding:
  the conic scheduling transfer requires the same unit-scale restricted
  barrier, objective, parameter, and Hessian metric; the pointwise distribution
  quotient requires positive eta; sampling and unequal-scale movement require
  explicit radius ranges; the minimization objective must identify its support
  direction; and the unequal-scale subsection must expressly replace the
  unit-scale barrier. Root also identified a minor endpoint-scope ambiguity:
  crossing a terminal label does not constrain an arbitrary final point to
  have the named endpoint distance.
- Repairs: separate agent `stage1_fixer` (not the Stage 2 author) applied all
  accepted findings. The conic paragraph now imposes equality of restricted
  barriers up to an additive constant and measures primal movement in that
  restricted Hessian metric. Pointwise and sampling parameter ranges are
  explicit, as are the support gap and the weighted barrier convention. The
  stronger unequal-scale crossing lower bound is retained; the same-endpoint
  comparison explicitly specializes to `z_N=x(0), s_N=0` and measures the
  shortest route from zero to that center.
- Validation: `conda run -n qipm --live-stream make` succeeded and produced a
  20-page PDF. The final log has no warnings, undefined references/citations,
  or overfull/underfull boxes. Repair passages were inspected against every
  accepted finding. No formulas changed, so the already-passing numerical
  and exact-certificate scripts were not repeated.
- Stage complete after minor repairs. No repeat five-reviewer round is
  required because the review identified no major issue. The integrated
  manuscript will still undergo its final full review.

## Stage 3: normalized, canonical, and coupled barriers

- Author: `stage3_author`. Completed normalized-profile comparison and its
  relaxed scalar envelope, the smooth nonmonotone construction, canonical
  cube barriers, spectral transfer, facet-collar lower bounds, exact coupled
  parameters, uniform radial upper bounds, and finite-sequence extensions.
  New radial developments progressed from the root's Stage 1 proposal to
  complete proofs and independent numerical checks; the source map retains
  that history and now records their completed review status.
- Review round 1: `reviewer1` through `reviewer5`, dispatched independently.
  All five reports appear in `audit/stage3-review1.md` through
  `audit/stage3-review5.md` and were assessed by the root. No valid major
  issue was found.
- Root assessment: accepted all distinct minor precision findings. The
  relaxed envelope class must explicitly require local absolute continuity,
  its positive-domain pointwise bounds, and almost-everywhere derivative
  bounds. The vertex-singular example requires `r>=2` and standalone wording.
  Only the objective weights and tolerance are claimed dyadic for arbitrary
  scalar profiles; the interval and analytic center need not be rational.
  Both new discrete consequences must state the Newton-decrement range
  `0<=beta<1/2`. Root also accepted a robust descriptive appendix reference
  in the scalar verification script's docstring as an optional improvement.
- Factual review correction: reviewer3 withdrew the allegation that the
  docstring's original “Appendix A” reference was currently stale; the scalar
  appendix is indeed first. Its replacement by “scalar-dilation appendix”
  avoids future numbering dependence and is not a repair of a present
  incorrect reference.
- Repairs: separate agent `stage1_fixer` applied every accepted item. The
  original smooth-envelope hypothesis already specifies `p` in `C^2`; the
  newly explicit relaxed class contains the constructed piecewise-smooth
  extremizers. No estimates or constants changed. The barrier-oracle
  qualification is retained, and fixed metric tubes remain unrestricted by
  the separate Newton-decrement radius bound.
- Validation: `conda run -n qipm --live-stream make` succeeded, producing a
  34-page PDF. The final log has no warnings, undefined references/citations,
  or overfull/underfull boxes. The repair passages were checked against the
  root's accepted findings. Numerical scripts were not repeated because no
  formulas or executable code changed; the script edit affects only its
  descriptive docstring.
- Stage complete after minor repairs. No repeat five-reviewer round is
  required because no major issue was identified. The integrated manuscript
  remains subject to final full review.

## Stage4 author handoff

- Author agent: `stage4_author`. Root's stage4 task and source-map determine scope; five independent stage4 reviewers are to be dispatched only after this handoff.
- Written and integrated primal–dual completion section, formulation section, complete concrete-formulation appendix, five primary bibliography entries and independent numerical diagnostic. No earlier-stage formulas changed. Main abstract/front matter remain explicitly reserved for stage5.
- Root inspected the evolving mathematics and requested precision repairs: redundant equality handling in Schur/progress proof; k=1 separate orthant case; parameter interval/round-radius/accuracy hypotheses; correct parameter cross-reference; small-error regime for matched chord counts; unambiguous bilinear Hessian notation and ordinary chain derivative. Author applied all of them before handoff.
- New development during author work: explicit feasible trial-direction proofs replace both informal root-Schur limiting arguments and establish the exact normtree parameter without a decoupling assumption.
- Independent numerical diagnostic passed:80 random full KKT solves, four dyadic ranks through256,80 arbitrary-fiber support/packing tests,1100 exact integer envelope cases, four tree shapes,100 root Schur inequalities. No packages installed.
- Author build:45pages; final log checked for undefined references/citations, LaTeX warnings, and overfull/underfull boxes. Root will assess five reviewer reports and assign a different fixing agent under the user's process. Stage4 is not yet certified complete.

## Stage 4 review and completion

- The preceding handoff records the state before review. Subsequently all
  five independent reviewers completed `audit/stage4-review1.md` through
  `audit/stage4-review5.md`; the root read and assessed every report.
- Root assessment: no major issue. Accepted both distinct minor findings:
  the equal-weight entropy specialization must retain the common positive
  objective weight, and the dimension theorem must define its affine lift
  and operational face reduction before imposing the factor dimension cap.
- Repairs: separate agent `stage1_fixer` corrected the specialization to
  `Delta_eff=lambda exp(-sum p_a log p_a)` for `lambda_a=lambda>0`.
  The dimension theorem now states `C=pi(K intersect L)`, with affine `L`
  and `pi`, and defines the smallest face containing the feasible lifted
  slice. Its factor faces are considered in their linear spans, with zero
  factors removed; the dimension cap explicitly applies to this reduced
  product cone. The general determinant scale, AM--GM argument, and
  dimension proof are unchanged.
- Validation: `conda run -n qipm --live-stream make` succeeded. The final
  45-page PDF log has no warnings, undefined references/citations, or
  overfull/underfull boxes. A direct qipm check of one source with weight
  two gives `Delta_eff=2` from both the general product definition and
  the corrected specialization. The unchanged numerical diagnostic was
  not repeated. The source map now records completion while retaining
  the earlier author-handoff history.
- Stage 4 complete after minor repairs. No repeat five-reviewer round is
  required because no major issue was identified. The final integrated
  manuscript remains subject to its full five-reviewer cycle.

## Stage 5 author handoff

The synthesis author read the whole mathematical draft, relevant
provenance and primary-literature ledgers, and additional online primary
sources. Completed final abstract, introduction, qualified contribution
statements, prior-work comparison and roadmap; moved the foundational
literature discussion into the introduction; added a final interpretation
section, author metadata, four finite-sequence references, two vector
scientific figures, reproducible dyadic data and generation script,
standalone README, and optional Makefile verification/figure targets.
Established theorem statements and proofs were preserved.

Root's concurrent reading identified two minor introduction precision
issues: an arbitrary admissible sequence has a lower Omega count while
the minimum has the matching Theta count, and the decrement neighborhood
requires radius beta<1/2. The author repaired both before handoff.

The figure script passed independent profile integration and derivative
checks. Its eight dyadic quadratures reported maximum relative error
estimate3.60e-12; these are numerical diagnostics, not rigorous enclosures.
The author inspected both figure pages and used embedded Type42 figure
fonts. The integrated manuscript builds as50pages, with no undefined
references/citations, overfull/underfull boxes or LaTeX warnings in the
final log. The submission sources contain no temporary stage markers.

Required next step: root dispatches five independent reviews of the
ENTIRE manuscript, assesses every finding, and assigns all accepted
repairs to a different agent. Any valid major issue requires a repeated
five-reviewer round; all remaining valid minor issues must be resolved.
This is both the stage5 review and the user's final manuscript review.

The author also built a fresh isolated copy containing only `main.tex`,
`macros.tex`, `bibliography.bib`, `Makefile`, `sections/` and `figures/`.
Latexmk generated all auxiliary files and the50-page PDF successfully;
the final isolated log had no warnings or undefined references/citations.
This verifies that other repository folders are not build dependencies.

## Stage 5 and full-manuscript review: completion

- The preceding author handoff records the pre-review state. Root dispatched
  five independent full-manuscript reviewers. Their completed reports are
  `audit/final-round1-review1.md`, `audit/final-round1-review2.md`,
  `audit/final-round1-review3.md`, `audit/final-round1-review4.md`, and
  `audit/final-round1-review5.md`. This round covers both Stage 5 synthesis
  and the user-required review of the entire integrated manuscript.
- Root assessed every report and found no valid major issue. All four
  distinct minor repairs were accepted: explicit standard-barrier scope
  for abstract/introductory exact geometry and allocation; integer-rounding
  qualification for introductory move counts; PDF title/author/keyword
  metadata; and the current STOC2026 trust-region prior-work comparison.
  Root independently identified the same count-rounding issue. No new
  mathematical gap or required theorem redevelopment was found.
- Separate repair agent `stage1_fixer` applied all four repairs. The current
  source is cited only for the precise abstract-supported wide/narrow
  neighborhood guarantees, with its distinct complexity resources explicit.
  Its bibliographic and primary-source evidence is recorded in the literature
  ledger. PDF metadata uses the existing manuscript title and author.
- Artifact hygiene: added `__pycache__/` to this folder's `.gitignore` and
  removed only generated `scripts/__pycache__` in this paper directory.
- Validation: `conda run -n qipm --live-stream make` succeeded, yielding
  49 pages. Final log is free of warnings, unresolved references/citations,
  and overfull/underfull boxes. The new citation is present in the generated
  bibliography; `pdfinfo` verifies populated title, author, keywords and
  subject. Existing mathematical diagnostics, figures and standalone-build
  dependencies did not change, so their prior successful checks were not
  repeated. Root's validation record now includes final resolutions.
- Stage 5 and the full-manuscript review cycle are complete after all minor
  repairs. No repeat five-reviewer round is required because no major issue
  was identified. Root will inspect the repaired passages and PDF before
  delivering the manuscript.

- Final root inspection complete: all repaired passages, primary-source
  scope, metadata and final log checked; all 49 reflowed PDF pages rendered
  and inspected. No further issue was identified. The manuscript and
  standalone source package are ready for delivery.
