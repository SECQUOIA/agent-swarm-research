# Manuscript development and review workflow

The user requested sequential stages. For each stage, one author completes the draft before five independent agents review it. The coordinating agent assesses every finding. A different agent corrects all accepted issues, including minor ones. Any accepted major issue triggers another round of five independent reviews after correction. Remaining accepted minor issues are fixed before the next stage. The full manuscript receives the same five-reviewer process after all stages.

Reviewers do not read one another's reports during a round. Manuscript sources are frozen during each review round, and source hashes are recorded with the reports. Reports distinguish mathematical defects, insufficient justification, scope or attribution errors, and optional preferences. The coordinator records accepted and rejected findings with reasons.

## Stages

| Stage | Scope | Status |
|---|---|---|
| 1 | Scaffold, model, solution framework, existence and uniqueness, sharp fractional moments and separation | Accepted: five independent reviews, zero major issues; all accepted minor corrections checked |
| 2 | Auxiliary number process, finite log correction, transport coupling, scaling limits and related identities | Accepted: five reviews, zero major; all minor corrections checked |
| 3 | Last-event tails, sharp daughter-law extrema, exact critical formulas and scalar-closure counterexamples | Accepted: five independent reviews, zero major; all minor corrections checked |
| 4 | Finite-population theory and numerical evidence; count-neutral and power-kernel boundary results | Accepted: five independent reviews, zero major and zero minor issues |
| 5 | Fourier identification application, sampling bounds, introduction, literature positioning, discussion, and full coverage integration | Accepted: five independent reviews, zero major; all minor corrections verified |
| Full draft | Independent assessment of all mathematics, structure, consistency, coverage, sources, figures, and readability | Accepted: five fresh independent whole-manuscript reviews, zero major and zero minor issues |

The claim-level scope is recorded in [COVERAGE.md](COVERAGE.md). Unrelated extinction and coarse-graining investigations are excluded. Research limitations are not silently converted into claims; any gap required by a theorem must be resolved or the theorem must be stated with justified assumptions.

## Stage 1

Author: `paper_stage1_author`. Author report: [stage1-author.md](stage1-author.md).

Round 1 snapshot and reports: [reviews/stage1-round1](reviews/stage1-round1).

Reviewers: `stage1_r1_measure`, `stage1_r2_moments`, `stage1_r3_adversarial`, `stage1_r4_sources`, and `stage1_r5_readability`. Each reviews the complete current mathematical draft; the names indicate additional areas of attention, not exclusive assignments.

The [assessment](reviews/stage1-round1/assessment.md) accepted four groups of minor corrections and several short reader aids. The separate `paper_revision_agent` implemented them in [stage1-revision.md](stage1-revision.md). The coordinator inspected every changed statement, the comparison hypothesis, the sharpness justification, and the clean final build log. No accepted issue remains. The accepted source hashes are in `stage1-accepted-snapshot.json`. Stage 1 is closed; no second review round was required because no major issue was identified.

## Stage 2

Author: `paper_stage2_author`. The draft completed five independent reviews and coordinator verification. See [stage2-author.md](stage2-author.md) for proof decisions and validation. The accepted stage 1 mathematical sources are unchanged. No reviewer or later-stage author was dispatched by this author.

Round 1 is complete in [reviews/stage2-round1](reviews/stage2-round1): five independent reports, zero major issues, two distinct minor issues. The coordinator accepted both wording corrections and several reader aids in the assessment. The separate `paper_revision_agent` implemented them, including correction of the repeated lattice claim in the original research note. Stage 3 began after acceptance.

Stage 2 accepted by the coordinator after inspection of every correction and the final clean build log. All accepted issues and reader aids are implemented. The source-note lattice correction is also verified. Accepted hashes: `stage2-accepted-snapshot.json`. No second review round was required because there were no major issues.

## Stage 3

Sole author: `paper_stage3_author`. Assignment began only after Stage 2 acceptance. The scope is the complete existing last-event and sharp-daughter package, including all-rate overlap coefficients, critical exact identities and limitations, and the classical pure-coagulation benchmark. Independent coordinator checks during authorship are recorded in `stage3-coordinator-checks.md`. The five manuscript reviewers completed their reviews after the author finished.

The author completed the assigned stage and its checks; see [stage3-author.md](stage3-author.md). At the author handoff, all Stage 3 coverage rows had destinations and the accepted Stage 1 and 2 mathematical source hashes were unchanged. No reviewer or later-stage author was dispatched by the Stage 3 author.

Round 1 is complete in [reviews/stage3-round1](reviews/stage3-round1): five independent reports and zero major issues. The separate `paper_revision_agent` implemented both accepted minor corrections, including the coagulation-event qualification in the earlier auxiliary-process discussion. The revision and clean build are recorded in [stage3-revision.md](stage3-revision.md). Coordinator verification and acceptance followed, as recorded below.

Stage 3 accepted by the coordinator after reading both corrected passages, reconciling the status records, and checking the clean final logs. No accepted issue remains. Accepted source hashes are in `stage3-accepted-snapshot.json`. No second review round was required because no major issue was identified.

## Stage 4

Sole author: `paper_stage4_author`. The finite-population and observable-boundary sections, two supporting appendices, and self-contained numerical supplement are authored. Proof decisions, source checks, and validation are recorded in [stage4-author.md](stage4-author.md). The accepted Stage 1–3 mathematical sources remain unchanged. Five independent reviewers completed the frozen-source review after the author handoff; each reported zero major and zero minor issues. The coordinator read and assessed all reports and verified the unchanged source hashes. Stage 4 is accepted without revisions; see `reviews/stage4-round1/assessment.md` and `stage4-accepted-snapshot.json`.

## Stage 5

Sole author: `paper_stage5_author`. All remaining content and paper-wide integration are authored; see [stage5-author.md](stage5-author.md). The new Fourier section and observation-design appendix include complete proofs and explicit statistical and preparation assumptions. The abstract, introduction, literature synthesis, assumptions roadmap, discussion, references, and coverage destinations are complete. Accepted Stage 1–4 mathematical and supplement files remain unchanged. Five independent reviews are complete with zero major issues. The separate `paper_revision_agent` implemented both accepted minor corrections; see [stage5-revision.md](stage5-revision.md). Coordinator verification and Stage 5 acceptance are complete; the full-draft review follows. No reviewer or additional author was dispatched by the Stage 5 author.

Stage 5 accepted by the coordinator after reading the revised endpoint formulas, abstract, source-note qualification, and dated record amendments, and inspecting the clean final logs. Only the two required section corrections and current status documents changed among frozen files. No accepted issue remains. Accepted hashes: `stage5-accepted-snapshot.json`. No second stage round is required because all issues were minor. The separate full-manuscript review followed.

## Full manuscript

The integrated draft is frozen in `reviews/full-round1/snapshot.json`. Five fresh reviewer agents independently assessed all sections, appendices, claims, sources, coverage, and presentation. They did not read prior manuscript review reports or each other's current findings. The required correction and repeat-review procedure remained in force; this final round found no issue requiring it.

Final acceptance: all five fresh whole-manuscript reports are complete, with zero major and zero minor findings. The coordinator read and assessed every report, verified the unchanged frozen sources, and accepted the paper. Optional presentation preferences were assessed as nonblocking. See `reviews/full-round1/assessment.md`, `FINAL-REPORT.md`, and `final-accepted-snapshot.json`. All stages and the full draft are complete; no further research is active.
