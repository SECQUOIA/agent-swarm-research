# Power-flow manuscript process

Scope: resistive and AC power-flow feasibility, existential-real completeness,
algebraic witnesses, angle semantics, and rigorously established extensions.
All relevant repository developments and their dependencies must be accounted
for. Other manuscript folders and research files are read-only for this task.

The user requires one author per stage, then five independent reviews, root
adjudication, and a different correction agent for all accepted findings.
A round with any accepted major finding requires another five-reviewer round.
Every accepted minor finding must be corrected before the stage closes.
The full manuscript receives the same five-reviewer process after all stages.
Internal reviews are not external peer review or proof-assistant certification.

## Stages

1. Foundations and resistive completeness: manuscript scaffold, exact input
   model, source problem, gadgets, both reduction directions, degree/data
   bounds, and exact reproducible checks.
2. AC feasibility and angle semantics: AC model, existential-real encoding,
   winding obstruction, resistive transfer, rectangular variant, and justified
   extensions of angle bounds or physical line parameters.
3. Algebraic and numerical boundaries: self-contained algebraic-degree
   consequences; investigate quantitative residual transfer, finite-precision
   certificates, and plausible structural restrictions. Retain proved results
   and precisely justified limitations, without assuming unresolved research.
4. Integration and publication preparation: introduction, related literature,
   complete scope comparison, verification supplement, conclusion, bibliography,
   layout, and complete source coverage. Resolve any material gaps discovered.
5. Whole-paper review: five independent full-manuscript reviews, corrections
   by another agent, repeated review whenever a major finding is accepted.

## Status

- Stage 1: accepted after five independent reviews (round1), no major findings;
  all two required minor findings and one accepted typography suggestion fixed
  by a separate agent and checked by root. Six-page draft builds cleanly.
- Stage 2: accepted after five independent reviews (round1), no major or minor
  findings. Root rechecked proofs, exact checks, and clean ten-page build.
- Stage 3: accepted after two rounds of five independent reviews. The major
  source universality error found in round1 was repaired with a self-contained
  arithmetic proof and sharp scope characterization. Round2 found no major
  issues; its minor coefficient-field qualifier was corrected separately and
  checked by root. All four exact checkers and the 24-page build pass.
- Stage 4: accepted after five independent reviews with no major issue. All
  five accepted minor fixes were applied by a separate agent and verified by
  root. The complete 28-page draft builds cleanly; source coverage is closed.
- Stage 5: complete. Five independent whole-paper reviews found no major
  issue and one minor singleton/connectedness omission. A separate agent
  corrected it; root verified the proof, exact boundary checks, unchanged
  checker code, clean 28-page build, and rendered page. No accepted issue
  remains. All stages and all 30 independent reviews are closed.

Evidence: author reports, independent reviews, root assessments, correction
reports, immutable review snapshots, and actual check logs live in this folder.
No submission or external communication is authorized by this process.
