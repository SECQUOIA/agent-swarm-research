# Stage 3 round 1 adjudication

Root read all fifteen complete reports, the entire frozen manuscript stage, its canonical sources and principal supporting developments. All reports identify the same seven-file snapshot. The round contains **0 major and 3 minor findings**, consolidated into two accepted actions. No finding is rejected. No mathematical proof or count constant needs replacement on the evidence reviewed.

## Accepted corrections

**A1 — Explicit rational computational inputs.** Reviewers 09 and 15, finding 1, identify the missing rational-tolerance qualifier in `thm:compiled-curvature`. Accept: the polynomial-time algorithm immediately invokes `lem:certified-curvature`, which requires rational tolerance, and performs rational arithmetic with that tolerance. State positive rational tolerance in the theorem. Root independently identified the same clarification needed in the constructive clauses of `thm:separable-scalar`: require rational polynomial data (including the affine terms) and positive rational tolerances. Preserve the finite continuous-convex, real-data clauses. This is a minor statement/input-model omission because the existing algorithm and proof already operate on finite rational data; there is no new mathematical hypothesis on the approximated shape or changed bound. A local qualifier is clearer than an implicit section-wide convention.

**A2 — Correct stale stage 2 status.** Reviewer 02, finding 1, identifies `coverage.md` under “Open boundaries and final obligations”: the rational nc-rank paragraph still ends “awaiting review.” Accept: stage 2 completed fifteen reviews and its correction gate. Replace the stale phrase with its accepted status while retaining the account of the proved rational construction. This is a documentation consistency issue, with no proof change.

## Other reports

Reviewers 01, 03–08, 10–14 reported no major, minor or unresolved question finding. Root read their complete reasoning and limits, including the independent proof reconstruction and finite exact/numerical checks. Their no-findings assessments are accepted as bounded review evidence, not as formal proof certification or a priority verdict. The report hashes and full-review acknowledgments are in `summary.json`.

## Correction scope and gate

A separate correction agent will implement A1–A2 only in `sections/03-scalar-nonlinear.tex` and `coverage.md`, write `verification/stage3-corrections.md`, and check the build and references. Preserve accepted sections 01/02, macros, main, bibliography, original research/literature and the frozen review archive. No new mathematical tests are needed for these input-qualifier and status edits. Root will inspect the complete patch and verify the preserved hashes before passing the gate. The gate is currently pending corrections. No accepted major finding requires another fifteen-reviewer stage round; the later whole-paper round remains mandatory.

## Final gate decision

Stage 3 gate passed. The separate correction agent completed A1–A2 and stopped editing. Root read the complete correction report and full diff, verified unchanged proof/count text and preserved accepted inputs/archive hashes, confirmed the build is up to date and the final TeX log clean, and reran the reference checker (198 labels, 32 bibliography entries). The corrected PDF has 63 pages. All fifteen report hashes remain unchanged. No accepted major or minor issue remains in this stage. The rational-input qualification and stale-status correction do not require another stage round; the mandatory whole-paper review will reread this corrected material.
