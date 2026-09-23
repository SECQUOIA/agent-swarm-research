# Stage 3 author report

Status: complete author draft, ready for the required five independent reviewers. This is not independent acceptance or completion of Stage 4. All changes are within `paper-lbesh/`; frozen solver, generator, raw results and repository notes are unchanged.

## Authored scope

- `sections/experimental-design.tex`: complete generated and external populations, pilot/held-out chronology, correlated designs, all methods/settings, actual hardware evidence, numerical acceptance formulas, independent audit boundaries and timing metrics.
- `sections/results.tex`: primary, pilot and repeated results; family/size and formulation/tree contrasts; paired work and medians; all cone evidence; external scope; no-integer-NLP and user-cut ablations; both outcome-triggered follow-ups.
- `sections/appendix-formulations.tex`: complete models and random draw order, convexity/domain/finite-epigraph/feasibility arguments, explicit SOC/exponential perspectives, inactive-origin reasoning, exact quadratic adapter and legacy input classifications.
- `sections/appendix-computational.tex`: detailed secondary tables, included by the formulations appendix. No main-file edit was necessary.
- `sections/oracle-diagnostics.tex`: empirical subsection appended below the Stage 2 ownership marker. Accepted preceding theory is preserved.
- `references.bib`: nine primary software/source references, with access/source checks recorded in the evidence literature ledger. No new priority claim.
- `scripts/regenerate.py`, `scripts/check_evidence.py`, `data/`, `tables/`, `figures/`: local standalone table/figure regeneration and all individual outcomes. Seventeen table fragments, two PDF figures and compact frozen extracts (~3.1 MB).

## Scientific development and numerical reconciliation

The model appendix now permits reconstruction without opening repository notes. In addition to the original arguments, it explicitly explains that zero-weight individual epigraph cones may permit positive auxiliary values, while positive cost coefficients and the zero copied cost budget force all such auxiliaries to zero. It also separates preservation of minimum epigraph costs from preservation of redundant unbounded epigraph values, and describes the standard/efficient tradeoff without falsely claiming both cost curves must cross within their common feasible interval.

The 51 coefficient streams are independently reconstructed from the appendix's specified order and compared exactly with each stored parameter digest. Existing targeted generator/conic tests were performed independently by the lead (31 passes; see `stage03-lead-verification.md`), so the stage author did not duplicate them. All computational claims use numerical evidence with stated scope; there is no claim of certified cone duals, universal dominance or successful separation-only implementation.

The paper takes per-record arithmetic over prior narrative rounding. Three small printed discrepancies with `notes/lbesh-study-results.md` were corrected:

1. Held-out quadratic ESH hull-single shifted mean is 2.282471871767047, printed 2.282 (the note prints 2.283).
2. Third-run ECP hull-single PAR10 is 50.62952244700026, printed 50.630 (the note prints 50.629).
3. Primary ECP hull-single wall time on `lbesh.log.large.s130363` is 120.87457759700192, printed 120.87 (the note prints 120.88).

These are rounding/transcription differences only; no underlying record, accepted classification or scientific conclusion changed. There was no defect invalidating this topic.

## Targeted verification actually performed

From `code/minlp_solver_lab`:

```bash
.venv/bin/python lbesh_results_independent_audit.py --help
.venv/bin/python lbesh_results_independent_audit.py \
  --fresh-validation \
  --compare-analysis results/lbesh_development/analysis_v1/analysis.json \
  --sensitivity results/lbesh_development/gurobi_trig_sensitivity_v1.jsonl \
  --legacy-initialization results/lbesh_development/legacy_initialization_v1.jsonl \
  --out ../../paper-lbesh/evidence/stage03-independent-audit.json \
  > ../../paper-lbesh/process/stage03-audit.log 2>&1
.venv/bin/python lbesh_oracle_diagnostic.py \
  --output ../../paper-lbesh/evidence/stage03-oracle-replay.json \
  > ../../paper-lbesh/process/stage03-oracle-replay.log 2>&1
```

The independent full-study audit completed successfully, with 1,464 records, 6,122 compared analysis fields, zero bound/status contradictions, 42 roots, 14 enumerations, and all 174 feasible assignment witnesses revalidated. It independently implements arithmetic and cohort matching but reuses the reviewed original-model validator; the manuscript says so. The oracle replay passed all internal analytic/recurrence/support/non-dominance checks. Its 14 scalar and 896 quadratic trials reproduce the saved summary and all executable hashes exactly. Replay timings remain separate and do not replace frozen diagnostic timing data.

From the repository root:

```bash
code/minlp_solver_lab/.venv/bin/python paper-lbesh/scripts/regenerate.py
python paper-lbesh/scripts/check_evidence.py
pdftoppm -f 34 -singlefile -scale-to 1600 -png \
  paper-lbesh/main.pdf paper-lbesh/evidence/stage03-page34
```

Regeneration derived all 17 tables, two figures and the 1,464-record CSV. SHA-256 comparison before and after a second regeneration verified identical bytes in all 21 outputs (17 tables, two figures, CSV and table-values JSON); recorded hashes are in `evidence/stage03-regeneration-before.json`. The narrative check independently verifies all 51 parameter streams and records all non-table secondary arithmetic in `evidence/stage03-claims.json`. Visual inspection of the rendered detailed-table page found readable text with no clipping; the lead separately inspected both figures and reported them legible.

Initial development assertions caught an incorrect local scope-key name (`norm_objective_stress` instead of `nonsmooth_norm_objectives`) and an incorrect local category label (`timeout` instead of `wall_timeout`); both scripts were corrected before successful execution. Several draft file-edit commands were initially invoked from the wrong working directory and returned `No such file or directory`; corrected commands wrote the intended paper paths. These were authoring-command errors, not solver/model failures or changes to the frozen data.

From `paper-lbesh`:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex \
  > process/stage03-build.log 2>&1
pdftotext -layout main.pdf process/stage03-rendered.txt
```

The complete current document builds to 36 pages with resolved cross-references and citations and no overfull boxes. A bibliography URL produces one harmless underfull-box diagnostic; it has no clipped or missing content. The initial long inaccurate-status token that caused an overfull line was rewritten as ordinary prose. The abstract/discussion/conclusion and full reproducibility appendix remain Stage 4 responsibilities, so the complete submission is not yet declared finished.

No project-wide checks, CI status checks or CI log inspection were performed. No additional optimization performance runs were launched; the fresh oracle replay is solver-free.

## Data and provenance

`data/provenance.json` links compact extracts to the final frozen `analysis_v1/analysis.json`, all eight benchmark JSONL inputs, both reference inputs, the generator source and relevant plans/manifests. Original-model acceptance was checked freshly before the compact snapshot was used for authoring. The snapshot keeps all failures and all runs separate; neither repeat nor follow-up pooling occurs. `data/records.csv` provides full individual results across all methods, and `data/instance_parameters.json` supplies the complete coefficients and metadata for all 51 controls.

The compact extracts regenerate manuscript tables/figures without repository imports, solver licenses or network access. They are not substitutes for raw witnesses/logs. Stage 4 should bundle/relocate the existing complete `publication_bundle_v1.tar.gz`, add final instructions and administrative sections, and verify the standalone submission package. The full frozen research bundle has not been copied by this author, to leave that packaging decision with Stage 4.

## Review focus

Review the generated-table denominators, interpretation of small descriptive timing differences, distinction between fixed numerical cutoffs and the theoretical residual-calibrated rule, positive/zero-scale conic equivalence, exact original-model acceptance, and expression-based external scope. The manuscript retains the negative conic comparison, unrepeated external results, same-seed repetitions, shared ECP interior initialization, lack of complete candidate/cut histories, outcome-triggered follow-ups, missing exported batch bound, and uncertified inaccurate references.
