# S7 documentation correction report

The separate correction agent implemented all three repair groups in [the lead adjudication](completion-s7-adjudication.md), plus the precise related coverage repairs subsequently authorized by the lead. Final acceptance remains pending the lead's verification. The five current documents retain their existing stage status.

The actual diff and before/after hashes are recorded in [completion-s7-final-checks.json](completion-s7-final-checks.json), using `/tmp/paper-a-s7-before-fix.tar.gz` as the before-edit snapshot. The diff replaces 41 lines across five files: 34 in coverage.md, three in completion-coverage.md, one in README.md, two in PROCESS.md, and one in completion-plan.md. These counts describe changed physical Markdown lines, not separate findings.

| Repair | Actual changes |
| --- | --- |
| Capacity witness and operating constraints | coverage.md lines 57, 159 and 248 now list A09 as the principal destination and retain A07 for the separate related local-filter boundary. Each row explicitly distinguishes those roles while retaining its provenance description. The corresponding exact-check script rows, lines 302 and 345, now point to A09. completion-coverage.md line 50 uses A07/A09 instead of A07/S5. |
| Global correlation arc validation | The promoted, scientific-note and review-note rows at coverage.md lines 71, 141, 231 and 232 now point to A08. |
| Series-parallel arc characterization | The promoted, scientific-note and review-note rows at coverage.md lines 79, 165, 254 and 255 now point to A05. The related hull and obstruction check-script rows at lines 353 and 354 also point to A05. |
| Identical links | Removed one repeated identical included-section link from each of the nine rows at coverage.md lines 118, 153, 160, 161, 163, 249, 250, 348 and 351. Every distinct destination and provenance description remains. In line 118, the lead also authorized correcting the conclusion link label from A08 to A12 while preserving its target. |
| Current prose | Repaired joined words and numbers in all five documents, including stage and section names, counts, source years, theorem locators and the Zenodo identifier's introductory word. The corpus sentence now reads “all 308 inventoried sources match.” Existing paths, theorem labels, hash values, numerical claims and stage decisions remain unchanged. |

The corrected destinations were checked against the actual included definitions: `prop:a-corr-irrational`, `thm:a-corr-lipschitz` and `prop:a-corr-sharper` in A09; `thm:a-design-global-capacity` in A08; `thm:a-bound-characterization` in A05; and the separate `thm:a-wcac-capacities`/`ex:a-wcac-irrational` local-filter boundary in A07. The four additional check-script destinations were checked against their source scope: rank-two irrational resistance and pressure/perturbation examples belong to A09; adjacent-terminal arc sensitivity and the K4 arc obstruction belong to A05.

The correction checks passed:

- The read-only command `python paper-potential-flow/verification/check_coverage.py` returned exit 0: `PASS: 308 inventory files and 13 included sections.`
- All 353 included-section links have labels matching the inventory's actual source destinations. All 740 local links across the five current documents resolve. No included-section destination repeats within an inventory row. The nine deduplicated rows retain exactly the same sets of target paths.
- All 23 manuscript source inputs and all 308 research-corpus files match the frozen hashes. All 63 archive payloads match both the freeze and the archive's internal manifest; their 63 local source files also match. The archive contains no missing or extra payload.
- Of the 41 frozen stage files, 37 remain identical. Only coverage.md, process/completion-coverage.md, README.md and PROCESS.md differ, exactly as intended. completion-plan.md is outside that 41-file freeze and is separately checked against the before-edit snapshot.
- The distributed archive, distributed PDF and internal archive manifest retain their frozen hashes. The PDF remains the reviewed 216-page artifact with 28 main pages.

The historical S7 freeze remains unchanged, SHA-256 `996816b32ef7c78a5d66ddc0535845575d8e31c968387f97cd6add45b3b1e915`. The distributed archive remains `ccdb3657677749bba4e2aa3233ce159dfd90c0ddb3f8dbed21c0ad242a162978`; the PDF remains `bda9cbb3407ac9e188574384f2efaf1739f00654c5ca83a7236c19e9dc612868`.

The saved exact replay retains 18 passing commands and SHA-256 `8962705b4d8ab7419b57820da3ec5bd4568395b39b1ff5e1a89507808fcde197`. The saved numerical-mode replay retains 28 passing commands and SHA-256 `72d025016fa2cd0cfb0838687ec41408cb2ba006adca9f6c7857203385c99c9a`. These are preserved evidence, not new runs. No numerical run, exact replay, rebuild or repackaging was performed for these documentation-only corrections. No manuscript source, bibliography, code, data, managed literature, historical review/evidence/manifest, other paper, PDF or archive was edited. No commit was created.
