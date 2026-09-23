# Manuscript review ledger

The user requires one author followed by five independent reviewers, coordinator adjudication, and corrections by a different agent for each stage. A valid major issue triggers a fresh five-reviewer round after corrections. All valid minor issues must be corrected before acceptance. The [full plan](../PLAN.md) governs the process and the final complete-draft audit.

| Stage | Scope | Author | Current state | Review/correction record |
|---|---|---|---|---|
| 00 | Scaffold and scope | paper_stage0_author | Accepted after five reviews and separate minor corrections | [acceptance](stage-00/acceptance.md) |
| 01 | Model, forms, finite bulk | paper_stage1_author | Accepted after five reviews and separate minor corrections | [acceptance](stage-01/acceptance.md) |
| 02 | Local responses and uniform baseline | paper_stage2_author | Accepted after five reviews and separate minor correction | [acceptance](stage-02/acceptance.md) |
| 03 | Predetermined moments and sharp high-order investigation | paper_stage3_author | Accepted after five reviews and separate minor correction | [acceptance](stage-03/acceptance.md) |
| 04 | Generic folds | paper_stage4_author | Accepted after five reviews; no corrections required | [acceptance](stage-04/acceptance.md) |
| 05 | Exact observation and local placement | paper_stage5_author | Accepted after five reviews and separate minor corrections | [acceptance](stage-05/acceptance.md) |
| 06 | Finite precision and interior crossover | paper_stage6_author | Accepted after five reviews and separate minor correction | [acceptance](stage-06/acceptance.md) |
| 07 | Numerical/literature synthesis | paper_stage7_author | Accepted after five reviews and separate minor corrections | [acceptance](stage-07/acceptance.md) |
| Final | Complete manuscript | Five independent reviewers and separate fixer | Accepted after five whole-manuscript reviews and verified minor corrections | [acceptance](final/acceptance.md) |

For each stage create `stage-NN/`, with an author handoff and a directory for each review round. Each round contains five individual reports, an adjudication, and, when necessary, a correction record. Record a content snapshot identifier (a commit, file hashes, or an immutable patch reference) for what was reviewed; do not represent reports on different drafts as one five-reviewer round. Store final acceptance in `acceptance.md`, naming the accepted snapshot, last review round, remaining limitations in the theorem scope, and verification of the last minor fixes.

Review reports must record exact locations, severity, reasoning, and an actionable correction or counterexample where available. A reviewer may find no issue, but must describe what was checked. General approval without a mathematical check is insufficient. All five reviewers should independently assess correctness; distinct additional emphases are useful but must not reduce any review to copyediting alone.

Suggested additional emphases: (1) functional analysis and assumptions; (2) independent derivation of constants and asymptotics; (3) adversarial competitors, counterexamples, and uniform limits; (4) transport meaning, units, and evidence; (5) exposition, completeness, literature, and cross-section consistency. Reviewers submit before seeing others' reports. No report is accepted as independent solely because its agent name differs: it must contain the reviewer's own reasoning.

The templates below are guides, not completed records:

- [Independent review](templates/reviewer-report.md)
- [Coordinator adjudication](templates/adjudication.md)
- [Separate correction and verification](templates/corrections.md)

At delivery, `build-and-reproducibility.md` must record installed tool versions, exact commands, outputs, figure/data provenance, unresolved warnings if any, and the PDF inspection. It does not replace mathematical review.
