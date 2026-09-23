# Structured bilevel manuscript development

User request: a comprehensive LaTeX paper, with active mathematical development,
seven sequential author/review stages, and a final whole-manuscript review.

## Required process

Each stage has one author followed by five independent reviewers. The root agent
evaluates every finding and records its disposition. A separate correction agent
addresses every accepted issue, including minor issues. Any accepted major issue
requires another five-reviewer round after correction. All accepted minor issues
must also be closed before advancing. The same process applies to the completed
manuscript. Earlier repository audits supplement this process; they do not count
as the five reviews requested here.

## Stage plan

1. Foundations, related work, complete source coverage, and build scaffold.
2. Exact scalar and block response compression, moving normals, pessimism,
   attainment, and arithmetic output boundaries.
3. Near-optimal follower robustness and certified dense-model screening.
4. Polynomial inverse approximation, power and resource results, nonlinear
   aggregates, response-dependent upper data, and rational recovery.
5. Dense and conditioned hardness, conditioned approximation, growing-leader
   structure, and follower-path response boundaries.
6. Exact convex and nonconvex algorithms, computational development, and
   reproducible experiments.
7. Full synthesis, abstract, exposition, figures, and completeness integration.
8. Whole-manuscript five-reviewer cycles, correction, and final verification.

## Completion

All eight stages are accepted as of September 9, 2026. The interrupted stage 7
was completed by a fresh author, reviewed by five independent agents, corrected
by a separate agent and accepted before stage 8 began. Five fresh reviewers then
read the entire manuscript. Root adjudicated all findings and verified the
separate final corrections. No major issue or unresolved accepted minor issue
remains. The final artifacts are the 78-page `paper.pdf`, the standalone LaTeX
source ZIP and the computational supplement ZIP, with blank authors and 54
references. Both exports were tested outside the repository. The full record is
`process/assessments/stage08-round01.md`; final hashes are in
`delivery/final-artifacts.json`.

Accepted final snapshot: `process/snapshots/stage08-accepted`, 39 files, manifest
SHA-256 `22466375e8acb78cd06879ba48b5051efbe9bdef2939e668c715252431cc5327`.
It includes the delivered PDF and the manifests identifying both ZIP archives.

## Stage history

- Stage 1 accepted after five independent reviews and separate correction of
  all five unique minor issues. No major issue required a repeat round.
- Accepted snapshot: `process/snapshots/stage01-accepted`.
- Assessment: `process/assessments/stage01-round01.md`; correction record:
  `process/stage01-corrections.md`.
- Stage 2 accepted after five independent reviews and separate correction of
  three minor attribution/layout issues. No major issue required re-review.
  Accepted snapshot: `process/snapshots/stage02-accepted`; assessment:
  `process/assessments/stage02-round01.md`.
- Stage 3 accepted after five independent reviews and separate correction of
  two minor bibliography/layout issues. No major issue required re-review.
  Accepted snapshot: `process/snapshots/stage03-accepted`; assessment:
  `process/assessments/stage03-round01.md`. Clean draft has 27 pages.
- Stage 4 author completed accuracy algorithms, full inverse/quantitative
  appendices, upper-data guarantees, and a new sharp 1/P response modulus.
  Nine distinct diagnostics passed; clean combined draft has 45 pages.
  Five independent reviews completed on `stage04-round01` (11 files,
  manifest SHA256 `4ef85d87d33a7c0860e735f7daa7311f1bc61f20b3ae6a36585f05ffe268befe`).
  Root accepted four minor corrections and no major issue; the separate
  correction agent fixed them and root verified the complete diff and clean
  46-page live build. Stage 4 accepted; snapshot `stage04-accepted`.
  Assessment: `stage04-round01.md`.
- Stage 5 author completed the boundary section and path-geometry appendix,
  including padded identity-Hessian hardness and one-power output obstructions.
  Eight existing exact diagnostics plus focused padding/recovery checks passed;
  clean combined draft has 63 pages. Five independent reviews completed
  on `stage05-round01` (13 files, manifest SHA256
  `c25d5edb69e64647034e54fea863d4637e410b2a22461e8d3d378741d67fd6b5`).
  Root accepted three minor corrections and no major issue. A separate agent
  fixed all three; root checked the complete diff, frozen hashes and clean live
  63-page build. Stage 5 accepted; snapshot `stage05-accepted`.
  Assessment: `stage05-round01.md`.
- Stage 6 author completed complete executable scalar algorithms, contact proofs,
  new independent full-task baseline and 60 successful fresh workers. The clean
  draft has 73 pages. Five independent reviews completed on `stage06-round01`
  (30 files; manifest SHA256
  `b9c28c41440e7ea2e660731eac9023d900279ad1ebae7bf99866f32ffb3d4bc8`).
  Root accepted two minor corrections and no major issue. A separate agent
  fixed iterator handling and stale README text; root checked the complete diff,
  hashes and new regression. All 18 cases and the clean 73-page build passed;
  measured provenance is preserved. Stage 6 accepted, snapshot `stage06-accepted`.
  Assessment: `stage06-round01.md`.
- Stage 7 was interrupted before authored text or an author report existed.
  On 2026-09-09 root verified accepted stages 1–6 and a clean working tree,
  then assigned a fresh sole author to finish synthesis and the strengthened
  standalone/novelty brief. Root and author are checking complementary primary
  literature; stage 7 has not yet passed review.
- Stage 7 author completed the 77-page standalone draft and isolated 17-input
  build. Root read the complete author report and new prose, checked the source
  comparisons, and froze `stage07-round01` (31 files; manifest SHA256
  `8291e480da66a12a69a046e702818c268420be847c4af81b324baca6868ce1b6`).
  All five independent synthesis reviews completed. Root read every report,
  accepted three minor attribution/terminology corrections and no major issue,
  and assigned a separate correction agent. Stage 8 has not begun.
- Root verified all three stage7 corrections, complete diff/source preservation
  and successful78-page build. Stage7 is accepted. The independent whole-paper
  stage8 review is the next required gate.
- Accepted stage 7 snapshot and stage08-round01 each contain 31 files with manifest
  SHA256 `d487e138b70585e03d5affa52a23e03631a30a45165651ddbe9d286162643231`.
  Five fresh independent reviewers completed the entire 78-page manuscript,
  including every section, appendix and proof. Root read all five reports and
  accepted two minor findings: the computational export's dependency closure
  and an explicit sign clarification in the sparse-power example. Root also
  followed up a reviewer literature lead, read the primary publication and
  accepted one additional minor attribution to Henke et al. (2026). No major
  issue was identified. A separate correction agent is completing all three
  corrections and creating the submission archives. Root verification and final
  acceptance remain pending. Assessment: `stage08-round01.md`.
- Stage 8 correction and final verification are complete. Root read the entire
  correction report and exact changes, checked the additional primary source,
  independently built the exported source without warnings, compared its text
  against the delivered PDF, verified the actual supplement and all 11 measured
  inputs, reran all five diagnostic families and regenerated all three tables
  byte for byte. The correction agent additionally ran every documented exact
  check and figure-generation command from its own extracted copy. Raw timings
  and all proofs are preserved. Root accepts stage 8 and the complete paper.
  No major issue required another five-reviewer round.
- Existing unrelated working-tree changes are being preserved.

## Evidence conventions

Review files identify the source snapshot/hash they inspected. Reviewers do not
edit the manuscript. Separate verification directories prevent output conflicts.
Root assessments distinguish accepted major issues, accepted minor issues,
rejected findings with reasons, and later-stage dependencies. A stage is accepted
only after its required corrections and repeat reviews are complete.

Literature sources support manuscript claims directly; internal notes and agent
reviews are provenance and verification records, not publication-priority proof.
