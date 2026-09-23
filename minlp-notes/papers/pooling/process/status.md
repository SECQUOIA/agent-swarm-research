# Pooling manuscript: work and review record

Requested: a comprehensive LaTeX paper on the repository's pooling research, with mathematical development and verification, sequential author/review/repair stages, 15 reviewers per round, repeated review after major issues, a final whole-paper review, and a compiled PDF.

## Review protocol

Each stage is authored by one assigned agent. Once its draft is complete, 15 agents review the entire stage with complementary areas of emphasis. Root assesses each finding rather than treating votes as proof. A different agent repairs accepted findings. Any accepted major issue requires another 15-reviewer round after repair. Stages advance only with no unresolved major findings. Minor accepted findings are repaired and checked. The complete manuscript receives the same process; accepted remaining findings must be resolved before completion.

Reviews are internal research checks, not external peer review or formal proof certification. Numerical and exact finite checks supplement mathematical proofs. Unresolved mathematical questions must remain explicitly unresolved; no novelty or completeness claim is inferred from unsuccessful searches.

## Stages

1. Models, arithmetic conventions, profitable-flow and hull tools, facial integrality. **Complete: two rounds of 15 reviews, accepted repairs checked, clean PDF build.**
2. Existential-real completeness, bounded-data variants, one-pool universality, and algebraic witnesses. **Complete: 15 full reviews, two minor corrections repaired and checked, clean PDF build.**
3. Sparse and small-network hardness, constant physical data, approximation and feasibility boundaries. **Complete: two rounds of 15 reviews, accepted repairs checked, clean PDF build.**
4. Fixed nonlinear core, certificate tools, quality rank, and structured bypass algorithms. **Complete: 15 full reviews, accepted minor repairs checked, clean PDF build.**
5. Degree-two paths, product contracts, exceptions, common throughput capacity, and two source-quality vectors. **Complete: 15 full reviews, accepted minor repair checked, clean PDF build.**
6. Related work, pooling-specific rank-one connections, unresolved routes, contribution map, introduction, and synthesis. **Complete: 15 full reviews, accepted minor repairs checked, successful PDF build.**
7. Whole-paper review, corrections, reproducibility checks, PDF compilation and visual inspection. **Complete: two rounds of 15 full-paper reviews, all accepted repairs checked, final source-only build and full PDF layout inspection passed.**

The detailed coverage inventory maps retained results, superseded arguments, and open directions to the manuscript. The review and correction files in this directory preserve the evidence for advancing each stage.

## Initial environment

The original working tree was clean. A TeX distribution, latexmk, and BibTeX are installed. Existing repository literature is read-only for this task; the manuscript will have its own bibliography and will not redistribute imported papers.

## Stage 1, round 1

Author: `/root/writer`. Reviewers: `/root/review01` through `/root/review15`. The frozen draft is `process/snapshots/stage-01-round-01.tex`, SHA-256 `dd43ffb4322012e5402cfa1f2480477b3b4e5adedf4820821c1ae37f5a9de23b`. The first draft compiled successfully to 11 pages. The final revised stage will be compiled again after review corrections. Stage 2 has not started.

All 15 first-round reports arrived. Root accepted one major missing hypothesis and six consolidated minor corrections. The separate `/root/s01_fixer` implemented them and compiled the corrected 11-page PDF without final warnings. Adjudication and repairs are saved in the round-1 directory.

## Stage 1, round 2

Fifteen fresh reviewers `/root/s01r02_01` through `/root/s01r02_15` are reviewing the full corrected stage, with complementary emphases. Snapshot `process/snapshots/stage-01-round-02.tex` has SHA-256 `999fa47848161c0c3b75611ce69389fc8ce36eb144d7bdb6b9609ee7388e1db2`. No reviewer is assigned only the previous correction. The endpoint regression check passes 55 exact physical/disjunctive comparisons and reproduces the rejected lower-quality-bound counterexample. Stage 2 remains pending the round's disposition.

All 15 second-round reports arrived: 13 with no findings, two with minor findings only. Root accepted the two clarifications. Separate agent `/root/s01_minor_fixer` made them and compiled without final warnings. Root inspected the exact two changes and the repair record, found no remaining accepted issue, and closed stage 1. In total this stage received 30 full agent reviews and two separate repair passes. This closure permits stage 2 to begin; it is not a claim of formal or external certification.

## Stage 2, round 1

Author `/root/stage02_author` froze the complete section after self-check and primary-source diagram verification. Snapshot `process/snapshots/stage-02-round-01.tex`, SHA-256 `4c00bbd3842c5605465727cc2b318b50f98f855601e81dd963314148c4157e77`. Fifteen independent full-stage reviews are being dispatched. Root read the whole draft and ran the independent physical one-pool checks and exact source-identity verifier. The author audit and root source-proof investigation are retained; no later stage has begun.

All 15 stage-2 round-1 reports arrived and were read by root: 13 with no findings, two with minor findings only. Root accepted the bibliography-rendering/version clarification and the weak-inequality terminology correction; no mathematical change was requested. A separate repair agent will implement them, and root will inspect the changes before advancing.

Separate `/root/s02_minor_fixer` implemented the exact minor repairs and produced a clean 22-page build. Root inspected both diffs and the rendered bibliography entries, verified foundations retain their accepted hash, and closed stage 2 with no unresolved accepted issue. Final section SHA-256 `8abd1d862cc58d23ee4671f2610c02ca04c27390353ba023b442325565514e67`. Stage 2 received 15 full reviews and one separate repair pass. This closure permits stage 3 to begin.

## Stage 3, round 1

Sole author `/root/stage03_author` completed all 19 assigned coverage entries. Root read the complete draft, checked primary sources, and ran independent exact and physical-network checks. The initial build has 40 pages and no final warnings. Frozen section SHA-256 `2d8f3082b7fce0a5da15fac5a3f4d20e44bafbe6b3cf209831e25a0c4b7f44a3` is saved in `process/snapshots/stage-03-round-01.tex`. Fifteen independent full reviewers `/root/s03r01_01` through `/root/s03r01_15` are reviewing it. Stage 4 has not begun.

All 15 reports arrived and were read fully by root. Ten report no findings, four minor findings, and one a major finding. Root accepted the missing upper-only quality hypothesis as major and four consolidated minor corrections. A separate repair agent is assigned; a second full 15-reviewer round is required after the repair. Detailed reasoning is in `stage-03-round-01/adjudication.md`.

Separate `/root/s03_fixer` implemented all accepted corrections. Root inspected the full source diff and unchanged stage-1/stage-2/bibliography hashes; the 40-page build has no final warnings. The corrected stage is frozen at SHA-256 `b8201a4bc6a61d4304f888649afe97bfc4aeefd9234d314a8cae3b805b3fad40` in `snapshots/stage-03-round-02.tex`.

## Stage 3, round 2

Fifteen fresh reviewers `/root/s03r02_01` through `/root/s03r02_15` are assigned the entire corrected stage under `stage-03-round-02-instructions.md`. Previous repairs are included in scope, but no reviewer is assigned only those changes. Stage 4 remains pending this review round and any required repairs.

All 15 second-round reports arrived and were read fully by root. Every report has no findings. Root closed stage 3 with no unresolved accepted issue; no second-round repair was needed. Stage 3 received 30 full reviews and one separate repair pass. Its accepted source retains SHA-256 `b8201a4bc6a61d4304f888649afe97bfc4aeefd9234d314a8cae3b805b3fad40`. The full adjudication is in `stage-03-round-02/adjudication.md`. This closure permits stage 4 to begin.

## Stage 4, round 1

Sole author `/root/stage04_author` completed the full stage and all six coverage entries. Root read the full draft, checked primary sources, and independently ran the support, ownership, and polygon-composition checks. The initial build has 54 pages with no final warnings. Frozen section SHA-256 `1ac2f2edead7ed519c97dec65e299412b7c10eb6709e1978ebdf2d2611c6bbe7` is saved in `snapshots/stage-04-round-01.tex`. Fifteen independent reviewers `/root/s04r01_01` through `/root/s04r01_15` assess the entire stage under `stage-04-round-01-instructions.md`. Stage 5 remains pending the review outcome and any necessary repairs.

All 15 stage-4 reports arrived and were read fully by root: fourteen no findings, one minor finding only. Root accepted the interval-validation repair and two optional local clarifications. No major finding was accepted. A separate repair agent is assigned; stage5 remains pending checked repairs and a clean build. Detailed reasoning is in `stage-04-round-01/adjudication.md`.

Separate `/root/s04_minor_fixer` implemented all three accepted minor corrections. Root inspected the full exact diffs in sections01/04, checked the bound counterexample is rejected without changing quality semantics, verified unchanged02/03/bibliography hashes, and checked the clean54-page build. Stage4 closes with no unresolved accepted issue after15fullreviews and one separate repair pass. Its final SHA-256 is `88b1c181cde7f72b48535054de702a2ff4688a470633eb56e528c519974189de`. The minor global flow-interval clarification gives section01 SHA-256 `e023daa9d8ceb445d931e193dce9d47ae1934e17ac13b54d4591710e3f8f76ae`; its prior accepted snapshot is preserved. This closure permits stage5 to begin.

## Stage 5, round 1

Sole author `/root/stage05_author` completed the entire stage and all 16 coverage rows. Root read the full draft, checked primary sources, and ran nine distinct contract/path verification scripts. The draft builds to 73 pages with no final warnings. Frozen section SHA-256 `b7930df8e95ebcd597051e24357aaa62f9ee11083642ae1a826c142ecc91aa62` is saved in `snapshots/stage-05-round-01.tex`. Fifteen independent reviewers `/root/s05r01_01` through `/root/s05r01_15` assess the entire stage under `stage-05-round-01-instructions.md`. The new exact throughput optimization corollary is included in their scope. Stage 6 remains pending review and any necessary repairs.

All 15 reports arrived and were read fully by root. Fourteen have no findings; review07 has one minor indexing/constraint-preservation clarification. Root accepted it and assigned a separate repair agent. No major finding was accepted. Detailed reasoning is in `stage-05-round-01/adjudication.md`; stage 6 remains pending checked repairs and a clean build.

Separate `/root/s05_minor_fixer` implemented the accepted correction. Root inspected the exact diff and repair record, verified the review's bypass-only product is rejected, confirmed preserved earlier sections and bibliography, and checked the clean 73-page build. Stage 5 closes with no unresolved accepted issue after 15 full reviews and one separate repair pass. Its accepted section SHA-256 is `ccb69faa00989209af3be2b152ca721e51deedf3c2139ea8c3ec0fe87ff02aa5`. This brings the completed full-stage review count to 105 and permits stage 6 to begin.

## Stage 6, round 1

After a usage-limit interruption, root verified that the sole author had completed and frozen the introduction and Section 6, including the requested primary citations and table spacing. Accepted sections 01–05 retain their hashes. The introduction hash is 5449b1254d6eb682f3238465e01f93b5b493ebdcb068c66edb1d7d8583c928f1; Section 6 hash is 3c2752d7d04769b796fed4e48cb05259fa313dcd5da006830a3e945db859867c. Snapshots preserve both and the bibliography. Fifteen full-stage reviewers are assigned under stage-06-round-01-instructions.md. Whole-paper review remains pending this stage's closure.

All 15 stage-6 reports arrived and were read fully by root. Eleven report no findings; four report minor findings. Root accepted four consolidated local corrections (singleton dimension, conic conventions, primary disaggregation citation, and research-note locators). No major finding was accepted. A separate agent is assigned repairs; stage 7 remains pending checked closure. See stage-06-round-01/adjudication.md.

Stage 6 closes after the separate repair and root checks. All five local repairs are complete; the 91-page manuscript has no unresolved references or overfull boxes. There are 120 completed full-stage reviews in total.

## Stage 7, whole-paper round 1

The complete manuscript, bibliography, driver and source index are frozen under `snapshots/whole-round-01/`, with a SHA-256 manifest. Fifteen independent reviewers assess every section and the introduction, with complementary emphases. The final round repeats after any accepted finding, including minor findings, until no accepted issue remains. Root separately checks source coverage, reproducibility, the build and final PDF layout.

All fifteen whole-round-1 reports arrived and were read fully. Root accepted one minor related-result coverage omission from review13 and no other finding. There are 135 completed full reviews. A separate repair agent will add the zero-lower/unit-upper general-cost margin-block refinement and its real source locator. Every proof remains subject to a fresh full-paper round after that repair.

Separate `/root/whole01_fixer` completed the accepted local repair. Root read the exact diff and validation, checked preservation and a successful 91-page build, and froze the corrected ten-file bundle under `snapshots/whole-round-02/`. Fifteen fresh full-paper reviewers are assigned under `whole-round-02-instructions.md`; every section and proof remains in scope.

## Final closure

All fifteen whole-round-2 reports arrived and were read fully by root. Every report has no findings; no accepted issue remains. The final source and PDF retain their verified hashes. The process is complete with 150 full reviews across ten rounds and eight separate repair passes. The final 91-page PDF builds from the supplied source bundle independently of the literature archive. All pages were visually inspected. See `whole-round-02/adjudication.md` and `../FINAL-REPORT.md` for the complete outcome and verification limits.
