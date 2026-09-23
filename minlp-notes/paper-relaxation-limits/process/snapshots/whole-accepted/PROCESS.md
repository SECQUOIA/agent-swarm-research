# Manuscript preparation and verification

## Current status

**Complete: all six authoring stages and the separate whole-paper review are accepted.** There are **135 completed reports across nine review rounds**. The final fifteen reports are all PASS, with no major or minor manuscript findings. No accepted issue remains unresolved.

The final deliverables are `main.pdf` (111 pages), `main.tex`, and `FINAL-REPORT.md`. The source-to-label ledger is `process/claim-coverage.md`. The final clean build and equivalence checks are in `verification/build-report.json` and `verification/final-build-validation.json`. All 31 manuscript inputs match the reviewed snapshot; extracted PDF text is identical, and PDF bytes differ only in build dates and trailer ID. The final PDF SHA-256 is `cffbee231ca40ea9a3e9ca461a788b805512b44ce4c19331ce4a988c874c447b`.

The scope is topic 3: convex-relaxation gaps and spatial certificate limits, with the assigned supporting comparisons. Other paper directories, canonical repository results and the literature collection are outside the authoring write scope. Existing research notes and PASS labels are evidence to inspect; they are not substitutes for proofs.

## Required workflow

1. Inventory claims, dependencies, corrections, superseded versions and open ideas.
2. Assign each writing stage to one author.
3. Freeze its complete text and have fifteen independent reviewers read the full assigned stage and shared dependencies. Additional focus areas do not narrow the review obligation.
4. The coordinator reads and adjudicates every finding on substance. A separate fixer implements accepted corrections, followed by coordinator verification.
5. Any accepted major issue requires another complete fifteen-reviewer round. A stage may advance only after no major or other accepted issue remains unresolved.
6. After integration and its stage gate, conduct the separate whole-paper fifteen-review/fix loop until no accepted findings remain. Any accepted finding in this final loop, including a minor one, requires fixes and another complete fifteen-reviewer round.
7. Compile, inspect layout and references, preserve reproducibility evidence, and report actual remaining limits.

A major issue affects theorem truth, proof completeness, required hypotheses, scope coverage, principal attribution or a reader's ability to verify a central argument. Minor issues concern local notation, wording or layout without those effects. Findings are not decided by majority vote. Internal review, finite computation and compilation establish neither external peer review, publication priority, journal suitability nor formal proof-assistant certification.

## Chronological stage accounting

| Stage and round | Completed reports | Outcome and correction | Gate |
| --- | ---: | --- | --- |
| 1, round 1 | 15 | One major finite-signing coverage omission and five minor correction groups accepted. Separate fixer restored switching-complete enumeration, exact witnesses and all qualifications. | Another full round required. |
| 1, round 2 | 15 | Fourteen PASS, one MINOR. Separate row-notation fix checked by coordinator. | Stage 1 accepted; 30 reports. |
| 2, round 1 | 15 | Twelve PASS, two MINOR, one MAJOR coverage omission. Separate fixer restored exact small two-level cubic members and completed the within-family threshold; notation, wording and checker layout repaired. | Another full round required. |
| 2, round 2 | 15 | Fourteen PASS, one MINOR spacing issue. Separate spacing fix preserved the printed executable exactly; coordinator inspected the result. | Stage 2 accepted; cumulative 60 reports. |
| 3, round 1 | 15 | Nine PASS, six MINOR verdicts, consolidated into four correction groups. Separate fixer clarified asymmetric definitions, retained zero-weight scopes, m>=2 for the exact width example, and the distinct open partition target. | Stage 3 accepted; cumulative 75 reports. |
| 4, round 1 | 15 | All PASS, no findings; no repair required. The degree-loss-free coordinatewise graph-lift theorem and relative transfer accepted. | Stage 4 accepted; cumulative 90 reports. |
| 5, round 1 | 15 | All PASS, no findings; no repair required. Bounded-monomial order-one lower transfer and independent order-one quadratic upper certificate accepted. | Stage 5 accepted; cumulative 105 reports. |
| 6, round 1 | 15 | Thirteen PASS and two MINOR; three local corrections accepted, no major issue. | All three separately fixed and verified; Stage 6 accepted, cumulative 120 reports. |
| Separate whole-paper round 1 | 15 | All PASS, zero major or minor manuscript findings. Coordinator read all complete reports; no repair required. | Final review accepted; cumulative 135 reports. |

Stages 1–3 were completed on September 5, 2026. Stage 4 resumed on September 6 after a usage-limit interruption: four section drafts had been saved, and a replacement sole author checked and completed them before any stage acceptance. It then received the complete fifteen-reviewer gate. Stage 5 was accepted on September 6; Stage 6 was accepted after its review and separate repairs on September 7. The separate whole-paper round was accepted on September 7 after all fifteen reports, including three interrupted reviewers, were completed. The interruption did not waive an authoring, source, coverage or review requirement.

Accepted snapshot lengths are 12, 33, 62, 80, 91 and 111 pages for Stages 1–6. These are historical build identifiers, not quality metrics. Frozen inputs and manifests are preserved under `process/snapshots/`; authors do not modify them.

## Audit trail

For each round, the complete reports remain under `process/reviews/` or the round-specific review directories recorded by its assignment and adjudication. Author records are `process/stage-01-author.md` through `process/stage-06-author.md`. Round decisions are `process/stage01-round01-adjudication.md`, `stage01-round02-adjudication.md`, `stage02-round01-adjudication.md`, `stage02-round02-adjudication.md`, `stage03-round01-adjudication.md`, `stage04-round01-adjudication.md` `stage05-round01-adjudication.md`, `stage06-round01-adjudication.md` and `whole-round01-adjudication.md`. These historical records describe their then-current drafts; the current-status paragraph and table above supersede their old present-tense gate statements.

Separate correction records and coordinator reading logs remain alongside those adjudications. `process/development-summary.md` and `process/claim-coverage.md` identify bounded completions and genuine open questions. Primary-source records under `verification/` retain exact version locators and access limits. `verification/repository-checks/` retains prior selected replay metadata and logs; later exact paper-local checks are recorded separately. Numerical or finite checks supplement general proofs and are not silently promoted to universal claims.
