# Quadratic aggregation paper: staged development

Scope: a standalone paper on the repository's quadratic aggregation
certificate theorem, weaker hypotheses, consequences and examples; the sharp
Gram HHC criterion and infinite-aggregation construction; exact hulls and
approximation; the strict PDLC four-bound; and the many-row span and local
certificate applications. All included mathematics receives the staged
review below. Internal agent review is distinct from journal peer review.

## Stages

1. Foundations: source inventory, primary-source literature review,
   mathematical setting, and standalone LaTeX scaffold.
2. Main certificate theorem resolving Conjecture 3.3 and complete proof,
   with critical investigation of the argument and its hypotheses.
3. Consequences, checkable hypotheses, boundary examples, and reproducible
   exact checks, including a concise application appendix on the proved
   conflict-repair LP and corrected exact example. Resolve or remove any
   unsupported ancillary statement; make no algorithm novelty or performance
   claim from the exploratory construction.
4. Sharp Gram completion and infinite aggregation: develop the sharp
   hyperplane-image construction, the infinite/uncountable necessity result,
   the arbitrary-quadratic-description obstruction, and the hull formulas;
   compare matrix-programming, spectral, and aggregation literature.
5. Quantitative approximation and objective-specific exactness: investigate
   the newly contributed approximation bounds and objective-dependent exact
   aggregation statements, with their precise domains and constants.
6. Four aggregations under strict PDLC: develop and audit the contributed
   theorem, sharpness example, and precise comparison with published bounds.
6b. Many constraints in a three-dimensional span: develop and assess the
   supporting material in `notes/research-20260922-span-three-many.md` and
   its independent review before synthesis. This bounded coverage stage
   requires its own author and five-reviewer process.
7. Full-paper synthesis: introduction, abstract, discussion, bibliographic
   consistency, standalone supplement and submission packaging.
8. Separate whole-manuscript review and final corrections.

Each stage is written by an author subagent, then reviewed independently by
five subagents. The coordinator assesses each finding. A separate correction
subagent addresses every accepted issue. A new five-reviewer round follows
any round with an accepted major issue. All accepted minor issues are fixed
before the next stage starts. Reports and assessments are saved in `process/`.

Only topic-specific checks are run. No project-wide checks or CI inspection.
The paper contains its own proofs and references; repository notes and the
local literature collection are not required to read or build it.

## Status

All stages are complete and accepted. Stages 1–7 completed the required
subagent authorship, five independent reviews, coordinator assessment, and
separate corrections; rounds with accepted major issues repeated the
five-reviewer cycle. Stage 7's two minor packaging/documentation issues were
corrected and the full portable proof verification was regenerated.

Stage 8 completed the separate whole-manuscript review with five independent
reviewers. All five final reports found no major or minor correction needed;
the coordinator accepted their findings after its own mathematical and
artifact checks. See `process/stage08-round01-assessment.md` and
`process/stage08-root-audit.md`.

Final deliverables are `paper.pdf` (42 pages), `formal-supplement.pdf`
(15 pages), and `dist/quadratic-aggregation-source.zip`, with hashes in
`artifacts.sha256`. The README gives reproduction commands and identifies
the author-supplied metadata required before submission. Internal review is
not external journal peer review, and no submission has been made.
