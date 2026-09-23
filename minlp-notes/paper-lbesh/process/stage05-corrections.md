# Stage 5 final corrections and delivery freeze

Author: /root/stage05_corrections. Date: 19 September 2026.

Read all five final reports and the lead disposition, including the LP-counter clarification. Both accepted minor groups are closed. No theorem, frozen observation, outcome, cohort, formula or numerical table entry changed. No subagents were spawned.

## Itemized closure

1. PAR10 scope: the opening results paragraph confines the much larger differences to the single-tree pairs and their one/two additional ECP failures. It states that multi-tree accepted counts are equal and their PAR10 differences reflect timing alone. Direct arithmetic reconfirmed counts 33/32, 30/30, 33/31, 29/29 and PAR10 ratios 0.119339, 0.994405, 0.114240, 0.990858.
2. Recorded row-separation time: inspected _esh_cuts, _separate_point, _initial_cuts and _cuts_at_solution. AST inspection confirmed time_cuts writes only at initialization (line 40) and accumulation (line 345). Algorithm and compact-data documentation define cumulative elapsed time in completed _esh_cuts calls: row checks, radial searches when used, and linearization/coefficient work. They exclude initial tangents, NLP-solution tangents, outside normalization/transformation and master/callback installation. They distinguish the broader cut-count scope. Abstract, introduction, results, caption, conclusion, generated figure title, table header and coverage statement use consistent terminology. Overlapping-timer and non-per-cut qualifications remain. Paired mean-time ratios remain 6.632235, 6.505443, 6.128555, 5.479943.
3. LP-counter clarification within group 2: inspected solver.py around line 738. Algorithm and compact-data documentation now define lp_iters as initial LP separation-phase iterations, not simplex/barrier iterations or all node LP solves. They state that one phase iteration can include a second solve with dual reductions disabled. No counter or value changed.
4. Administrative closeout: README and coverage record all five author/review/correction stages, 25 agent reports, all valid findings corrected, and no accepted major finding. They distinguish internal agent review from journal peer review and do not guarantee acceptance. No pending status remains in delivered documentation. Authorship stays anonymous; no administrative facts or DOI were invented. Lead acceptance is a separate decision.

## Checks actually executed

Working directory: paper-lbesh.

- ../code/minlp_solver_lab/.venv/bin/python scripts/regenerate.py
- python scripts/check_evidence.py > process/stage05-correction-evidence.log

Used the original venv path without resolving its symlink. An inline standard-library check compared the saved pre-correction ledger: all 17 table rows are unchanged; the only changed heading is the last work-table column. It ran the same regeneration command again and verified byte-identical hashes for all 21 outputs. Immutable compact inputs, provenance, CSV and full research archive match their pre-correction review hashes. The generation check is recorded in stage05-correction-generation-checks.json. The evidence checker passed narrative arithmetic and all 51 independent parameter reconstructions; it did not freshly evaluate model witnesses.

Clean build and packaging:

- latexmk -C main.tex > process/stage05-clean.log
- python scripts/package.py > process/stage05-package.log 2>&1

After the additional LP-counter clarification:

- python scripts/package.py > process/stage05-final-package.log 2>&1
- sha256sum -c SHA256SUMS
- pdfinfo main.pdf
- pdftotext -layout main.pdf process/stage05-final-rendered.txt

Both package runs passed. First-pass undefined citations/references in the clean multi-pass transcript resolved normally. Final main.log has no undefined references/citations, multiply defined labels or overfull boxes; only the inherited bibliography underfull line (badness 6300). The manuscript has 42 pages and all three delivery checksums pass.

An inline standard-library final check verified all 62 source-archive payloads against current files and their declared hashes/sizes, matching embedded/external manifests, absence of process records in the archive, and identical main/submission PDFs. It checked 83 unique labels, 62 reference targets and all 27 citation keys; no missing targets, unresolved rendered question marks, scientific placeholders or pending delivered status remain. It independently recomputed the four paired counts and timing ratios. Results are in stage05-final-checks.json. The 68-path stage05-final-source-sha256.json fingerprints the reviewed source/delivery set.

Visual checks used pdftoppm -f N -l N -scale-to 1600 -png -singlefile main.pdf /tmp/lbesh-stage05-corrections-pageN. Viewed pages 1 and 17 after the clean build, and pages 10, 12, 16, 17 after the LP refresh. Page 1 content is unaffected by that refresh. Abstract, definitions, PAR10 prose, figure title and table heading/caption are readable and unclipped; all numerical bar annotations remain.

One tool invocation to write this report initially had a JavaScript syntax error before shell execution; it made no change and was corrected. No scientific check failed. No optimizer campaign, full witness audit, project-wide/CI check, new environment installation or literature search was repeated. Earlier audit and relocation checks remain documented in their original stage records, not claimed as new checks here. No research source/data/supplement was modified. All changes are confined to paper-lbesh.

## Frozen delivery identifiers

- dist/paper-lbesh.pdf: 559,792 bytes; SHA-256 0a2249a00dee9621015331663244b0f7a43ba22961d6f5c08359d9c6167acf53.
- dist/paper-lbesh-source.tar.gz: 942,239 bytes; SHA-256 0188c56ef9c98189a2b330977f9cc08432176b082030e4a2d791776be51d28f8.
- supplement/publication_bundle_v1.tar.gz: 38,086,636 bytes; SHA-256 f0399194ca1c9c57421965e236302c62e10eb72846ab807f936f18d9927d4b26.

Source and delivery are frozen for final lead inspection. No further edits are planned.
