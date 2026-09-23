# Paper preparation and verification report

The paper is **Convex relaxation gaps and spatial certificates in nonlinear optimization**. Its source is [main.tex](main.tex), and its compiled manuscript is [main.pdf](main.pdf).

**Completed September 7, 2026.** All six authoring stages and the separate whole-paper review are accepted. The final PDF has **111 pages**. The process produced **135 completed review reports across nine rounds**, with all fifteen final reports PASS and no unresolved accepted finding.

## Coverage

The paper treats the selected third repository topic: limits of convex relaxations and spatial certificates. It contains the signed bilinear density comparison; universal, cubic, structural and physical-box multilinear laws; exact scalar-envelope complexity; cardinality and XOR spatial lower bounds; coordinate and monomial reformulations; and finite upper certificates. Supporting appendices cover point packing, scaling disjunctions, P-split coordinate effects, correlation-face conic lift bounds, primitive FBBT, and a short integer-precision comparison.

The [claim-coverage ledger](process/claim-coverage.md) maps the assigned repository developments to actual theorem, equation and appendix labels. It includes distinct predecessor proofs and finite certificates, identifies superseded claims, and separates inherited literature results from the paper's proof work. Unrelated repository topics and the other paper directories remain outside this paper's scope.

## Authoring and review stages

Each stage had one author, a frozen manuscript, and fifteen independent reviewers. Each reviewer had to read the complete assigned text and its dependencies; additional focus areas did not excuse partial reading. The coordinator read the complete reports and decided findings on substance. Separate correction agents implemented accepted repairs. An accepted major issue required another complete fifteen-reviewer round before proceeding.

| Stage | Content | Review rounds | Completed reports | Resolution |
| --- | --- | ---: | ---: | --- |
| 1 | Foundations and signed bilinear comparison | 2 | 30 | Restored omitted complete-signing finite results, witnesses and executable enumeration; repaired conventions, attribution and notation. |
| 2 | Universal positive laws, cubics and equal means | 2 | 30 | Restored omitted exact small cubic members and completed the family crossing threshold; repaired local wording and checker layout. |
| 3 | Incidence, feedback, frequency, treewidth, boxes and scalar complexity | 1 | 15 | Corrected four local groups concerning asymmetric definitions, retained scopes, an endpoint parameter and an open partition question. |
| 4 | Cardinality spatial, moment, coordinate-lift and relative certificates | 1 | 15 | All PASS, no findings. |
| 5 | XOR, monomial reformulations and finite certificates | 1 | 15 | All PASS, no findings. |
| 6 | Full integration, supporting proofs, literature and coverage | 1 | 15 | Thirteen PASS and two MINOR; three accepted local repairs separately implemented and verified. |

The two major findings were coverage omissions in Stages 1 and 2. Each triggered the required second round on the entire corrected stage. Stage 6's final repairs made the scaling catalogue membership explicit, corrected one coverage-ledger word, and qualified the cited linear-FBBT LP result to nonempty limiting boxes. No accepted stage finding remains unresolved.

Usage-limit interruptions did not waive a gate. An interrupted Stage 4 draft was completed by a replacement sole author before review. The later interrupted stage and integration work were completed and accepted before starting the separate whole-paper review. In that final round, reviewers 9, 12 and 14 resumed their saved independent work after the usage-limit errors. Reviewer 15 used a completed prior-stage thread because the platform rejected one more new thread; all fifteen reviewers in the round are distinct agents. Dispatch records preserve these details.

## Separate whole-paper review and final build

After all stage corrections were accepted, fifteen independent reviewers read the corrected complete paper, every proof and appendix, the bibliography and the coverage record. All fifteen returned PASS without a requested manuscript repair. The coordinator read every report in full and independently assessed its substance. No further correction or review round was necessary under the agreed stopping rule. The [final adjudication](process/whole-round01-adjudication.md), [complete reading log](process/whole-round01-root-reading.md), and [report hashes](process/whole-round01-report-hashes.json) preserve the decision.

Fourteen reviewers independently compiled their own copied inputs. Several inspected all 111 PDF pages at overview scale, with selected enlarged pages for dense formulas, code, tables and corrected passages. The fifteenth reviewer explicitly performed fresh full reading, exact printed-certificate replay and all-page visual inspection without an additional build. Minor inaccuracies in a few review descriptions were checked against the actual manuscript and recorded; they did not require manuscript changes.

After acceptance, the coordinator cleaned and compiled the deliverable with:

```sh
cd paper-relaxation-limits
latexmk -C main.tex
python verification/build_and_check.py
```

The build succeeded with no unresolved references or citations, duplicate labels, overfull boxes or tracked warnings. The three underfull bibliography lines in the raw log were readable in the visual audit. All 31 manuscript inputs are byte-identical to the reviewed inputs. All 111 pages' extracted layout text matches. The rebuilt PDF itself is identical after removing only creation/modification dates and the trailer ID; no mathematical or visual content changed after review.

Final PDF SHA-256:

```text
cffbee231ca40ea9a3e9ca461a788b805512b44ce4c19331ce4a988c874c447b
```

See [final-build-validation.json](verification/final-build-validation.json) for the exact checks and reviewed-versus-final hashes. The final accepted artifact is preserved under `process/snapshots/whole-accepted/`; earlier snapshots remain unchanged.

## Developments completed while writing

The work went beyond transcription. Bounded completions include:

- Exact small two-level cubic values and the precise threshold at which that specified family exceeds a ratio of two.
- The general-radix cutoff and attaining construction beyond the simpler large-radix regime.
- The coefficient-regularity cardinality bound improved from `L+3` to `L+1+beta_N`, with its hypotheses and common-law proof.
- A degree-loss-free transfer for coordinatewise graph lifts, including everywhere-finite nonpolynomial coordinate functions, and its globally coupled relative extension.
- The bounded signed-monomial lower transfer at order one under `rD >= 2`, plus a separate order-one upper certificate for the quadratic formulation.

Full proofs, finite witnesses, localizer degree checks, tensor positivity, exact midpoint-tree counts and the feasibility-tolerance range make these developments independently assessable. See [development-summary.md](process/development-summary.md) and the coverage ledger for exact scope; these are not independent publication-priority claims.

## Verification and reproducibility

The verification combined proof reconstruction, targeted inspection of primary originals, exact rational and integer certificates, independent finite falsification attempts, selected numerical experiments, isolated LaTeX builds, extracted-PDF comparisons and visual inspection. These provide different evidence: numerical checks and finite tests do not prove universal theorems.

The two printed executable certificate appendices were repeatedly extracted and run. Independent checks also exercised common-law marginals, coefficient inequalities, graph colorings, matching gadgets, cardinality Gram and assignment identities, coupled tensor localizers, signed moment realizations, P-split projections, packing moment matrices, scaling hulls, rank-one face bounds and FBBT contractors. Reports identify their exact or numerical character and their limits.

[README.md](README.md) gives build and replay commands. [verification/environment.json](verification/environment.json) records the actual software environment. [PROCESS.md](PROCESS.md), the complete reports under `process/reviews/`, round adjudications, correction records, source audits and immutable snapshots preserve the audit trail. Local literature originals were read without redistributing the user-supplied PDFs.

## Remaining boundaries

The paper explicitly leaves the exact cubic constant, matching second-order lower asymptotics, exact finite-aspect constants, higher-width structural constants, unequal-aspect frequency-two sharpness and unrestricted affine-branching bounds open. It also states the domain, representation, oracle, degree and encoding hypotheses of every lower bound.

Deep classical results remain attributed external inputs. Source records identify inaccessible originals, inspected author versions and unresolved contextual bibliographic identity; these limits are not presented as fresh proofs or exhaustive priority clearance. Internal agent reviews are not external peer review or proof-assistant certification. A journal's assessment, authorship information and any eventual venue-specific formatting remain separate from the mathematical preparation requested here.
