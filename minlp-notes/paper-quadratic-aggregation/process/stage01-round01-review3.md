# Stage 1, round 1: independent review 3

Date: 2026-09-22. Scope: inventory, setting and definitions, background
claims, corrected versus historical scope, and the standalone scaffold.
The later main proof and consequences were not reviewed as draft sections.
I did not read other stage-1 reviewer reports or edit manuscript sources.

## Verdict

**Major inventory revision required; no mathematical error found in the
current definitions or formulation of Conjecture 3.3.** The main issue is
new, directly relevant work that appeared concurrently in the shared
repository. This is a present completeness problem, not evidence that the
author overlooked a file available at the start of the stage.

The notation correctly distinguishes the ordinary hull from its closure,
strict systems from closed systems, the multiplier cone including zero
from nonzero certificates, and good aggregations from globally convex
quadratic functions. The corrected audit's existence-only interpretation
is preserved. The HHC definition, the elementary dimension condition for
HHC implying hidden convexity, and the equivalent nontriviality formulation
of Conjecture 3.3 are sound. The current manuscript makes no unsupported
claim that convex aggregations describe the whole hull or that the Shor
projection is always closed.

## Findings

### M1 — major: update the inventory and stage plan for concurrent relevant developments

`process/coverage.md` does not inventory
`notes/research-20260922-aggregation-frontier.md`. This note contains a
candidate resolution of BDS Conjecture 3.1, a general replicated-matrix
HHC construction, an exact good-multiplier cone, infinitely many uniquely
active multipliers, an explicit hull formula with a direct midpoint
derivation, a PDLC obstruction, and new literature comparisons. These
are directly relevant to the aggregation topic and to the paper's planned
boundary discussion of finite good-aggregation descriptions.

The coordinator confirmed that the note appeared concurrently, accepted
the completeness issue, and plans a separate author/review stage for it,
contingent on correctness and novelty checks. That is an appropriate fix.
Add the source and each substantive development to the coverage map and
revise PROCESS.md accordingly. Do not treat the candidate's favorable
derivations or symbolic checks as a substitute for the requested reviews.
Revisit the present coverage statement that finite good-aggregation
questions are outside the paper's results after the new stage concludes.

Also inventory the concurrent
`formal/topics/27-quadratic-aggregation/` package and its intended source
directory `formal/Formal/QuadraticAggregation/`. The README currently says
“in progress” and explicitly does not claim a completed Lean proof or
passed verification. Its scope is the main theorem and HHC specialization,
not all corollaries, SDP results, examples, or the new frontier note.
Record that bounded scope and defer any verification claim until the
actual completed declarations and targeted verification record have been
inspected. No Lean build was run for this review.

The frontier note additionally provides a published Blekherman–Dunbar
eprint link and pointers to Wang–Kılınç-Karzan matrix-programming results,
Dey–Han–Wang's different infinite-aggregation obstruction, and a thesis
search excerpt. Incorporate these as leads in the literature record;
independently inspect the needed primary sources before treating their
claims as established. In particular, the existing “publisher full text
was not obtained” statement is historical stage-1 access status, not a
reason to ignore the newly available eprint.

For inventory completeness, explicitly dispose of the older
`notes/research-20260912-algorithm-opportunities.md` and its linked
`notes/review-20260912-quadratic-conflict-example.md`. This is a closed
algorithmic exploration of repairing local proof multipliers to obtain
global convex aggregates, not another resolution of the proper-hull
question. Its elementary aggregate validity and repair LP should not be
promoted as novel or an implemented algorithm. A short exclusion as a
separate algorithmic topic is reasonable; it does not need to expand the
current paper's research program.

### m1 — minor: retain the dimension qualifier in the separable attribution

`sections/01-setting.tex:105–106` attributes the diagonal characterization
to BDS Theorem 2.12 without its stated `n >= 2` condition, whereas this
section starts with `n,m >= 1`. The cited arXiv-v2 theorem expressly assumes
`n >= 2`. The characterization in dimension one is elementary and does not
threaten the new theorem, but the attributed scope should be exact.

Fix: say “For `n >= 2`, their separable case …” or explicitly distinguish
the cited result from the elementary dimension-one extension.

### m2 — minor: identify the matrix blocks in the PDLC background sentence

`sections/01-setting.tex:126–130` describes the Dey–Muñoz–Serrano result
“under a positive definite linear combination assumption” and correctly
explains that signed coefficients are allowed. Specify that this is a
combination of the **homogenized matrices `Q_i`**. The paper will later
contrast PDLC of `A_i` and `Q_i`, so leaving the objects implicit here is
an avoidable ambiguity. It is also preferable to say “under additional
hypotheses including …” so the short contextual sentence cannot be read
as the full theorem statement.

## Checks and sources actually inspected

- Read PROCESS.md, the stage-1 author report, coverage.md, literature.md,
  main.tex, macros.tex, the full setting section, and references.bib.
- Read the canonical aggregation result, the aggregation portions of the
  corrective audit, and the historical aggregation review record.
- Searched topic phrases across `results`, `notes`, `code`, and README;
  read the frontier note and the relevant portions of the older algorithm
  opportunity note.
- Read the concurrent formal package README, claims inventory, and source
  inventory; listed its Lean source files. No formal certification was
  inferred from this inspection.
- Compared the current background claims with the already downloaded
  primary BDS arXiv-v2 extraction at Theorem 2.9, Theorem 2.12,
  Proposition 2.14, and Conjecture 3.3. No additional online novelty
  search was performed for this inventory-focused review.
- Ran `rg -n 'Warning|Overfull|Underfull|undefined'
  paper-quadratic-aggregation/build/main.log`: no matches in the existing
  final build log. This inspects the author's build; I did not independently
  rebuild or inspect the rendered PDF.
- Ran targeted `git status --short` for the frontier note and paper folder;
  both are untracked concurrent work. No project-wide verification, CI
  inspection, numerical experiments, or subagents were used.

The new candidate developments require their own mathematical and novelty
reviews. This report does not endorse their universal claims merely by
requiring them to be inventoried.
