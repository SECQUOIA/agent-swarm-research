# Stage 4 author report

Status: complete author draft and standalone delivery, frozen for the required five independent Stage 4 reviewers. This is not final manuscript acceptance. No subagents were used by this author. Changes are confined to `paper-lbesh/`; frozen research sources, plans, benchmark outcomes and prior literature files are unchanged.

## Complete narrative and organization

Authored the abstract/keywords, discussion, conclusion, and reproducibility appendix. The scientific claim remains a matched empirical comparison in this NLP-assisted GDP implementation, with a modest 4–6% conditional single-tree timing benefit, substantially greater cut-generation work, equal external accepted counts, faster supported cone alternatives in aggregate, and the negative integer-point NLP recovery ablation. No new cut-family, general framework, universal superiority, exact certificate or unsupported priority claim was added. The accepted related-work section and literature ledger supply attribution; no new historical or literature claim required an additional source search in this integration stage.

Added `sections/guarantees-overview.tex` to make the main implications of the accepted theory accessible before the algorithm and study. Moved the complete, unmodified separation-theory and representation/oracle-diagnostic sections into appendices. The study starts on page 13 instead of around page 20; results start on page 15. Full proofs, model/cone specifications, all 17 tables, both figures and every material qualification remain. The full manuscript is 42 pages, including references and appendices; the conclusion ends on page 22. There are no reserved scientific sections, TODOs, unresolved citations or unresolved cross-references.

The main model and algorithm remain in the article because their differences define the experimental intervention. The concise overview explicitly points to full assumptions and proofs. New prose avoids interpreting the approximate numerical code as an implementation of the certified arithmetic or residual-calibrated algorithm. The lead's two pre-handoff suggestions were incorporated: convexity is stated for the row re-expression that weakens ECP, and the abstract qualifies conic superiority as a common-solved mean-time comparison.

Anonymous authorship is retained. No authors, affiliations, funding, conflicts, public archive DOI or journal acceptance were fabricated. Third-party sources retain their archived attribution and licenses. The paper is scientifically standalone; repository research/review notes are provenance rather than substitutes for definitions or proofs.

## Packaging and portable commands

- `scripts/package.py` first builds the current PDF and creates the deterministic `dist/paper-lbesh-source.tar.gz`, `dist/paper-lbesh.pdf`, `dist/source-manifest.json` and root `SHA256SUMS`. The source archive contains 62 payload files plus its embedded manifest, currently about 920 KiB compressed. It includes TeX, bibliography and `.bbl`, generated tables/figures, compact data, scripts, selected evidence and supplement metadata. It excludes review/process records, environments, temporary logs, recursive dist contents and the large research archive.
- `supplement/publication_bundle_v1.tar.gz` is copied byte-for-byte: SHA-256 `f0399194ca1c9c57421965e236302c62e10eb72846ab807f936f18d9927d4b26`, 38,086,636 bytes. Original manifest, checksum and verification JSON are copied unchanged beside it. The archive has 9,076 payload files plus its embedded manifest; all source licenses remain intact.
- `scripts/verify_supplement.py` checks the fixed archive hash, all member names, payload sizes and hashes. It rejects duplicate names, links, special files and unsafe relative paths. Optional extraction requires a new or empty directory.
- `evidence/check_stage02.py` now requires `--research-root`, locating its checked solver source in the extracted research tree. It never silently skips source/default validation.
- `README.md`, `supplement/README.md` and the reproducibility appendix explain delivery, extraction, ordinary and fresh-install environments, numerical acceptance, regeneration versus fresh primal audit versus optimization reruns, and exact commands. The extracted audit command explicitly sets `PYTHONPATH="$PWD/instances/gdplib_src"` so that a reused editable install does not import models from another checkout.
- The coverage ledger now records completed accepted Stages 1–3 and the integrated manuscript, with final review still pending.

## Checks actually performed

The complete details and exact executable paths are in `stage04-relocation-checks.json`, `stage04-final-delivery-checks.json`, their logs, and `stage04-import-origins.log`.

From the repository root:

```bash
python paper-lbesh/scripts/package.py
pdftotext -layout paper-lbesh/main.pdf paper-lbesh/process/stage04-rendered.txt
```

From `paper-lbesh`:

```bash
python scripts/package.py
sha256sum -c SHA256SUMS
```

Packaging was repeated with unchanged inputs; source archives were byte-identical. All three delivery hashes passed. The current stage archive hash is recorded in `stage04-final-delivery-checks.json`; corrections must refresh it with the packaging script.

Initial source extraction was into `/tmp/lbesh-paper-stage04-fue1r0qb/paper-lbesh`. Every source file was compared with the embedded manifest before execution. From that extracted directory:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
/path/to/existing/.venv/bin/python scripts/regenerate.py
/path/to/existing/.venv/bin/python scripts/check_evidence.py
/path/to/existing/.venv/bin/python scripts/verify_supplement.py \
  supplement/publication_bundle_v1.tar.gz --extract research
/path/to/existing/.venv/bin/python evidence/check_stage02.py \
  --research-root research
```

All commands passed. All 21 regenerated outputs (17 tables, two figures, CSV and displayed-values JSON) were byte-identical to the delivered files. All 9,077 research archive members passed verification and safe extraction. The source/example check passed against the extracted source. From its extracted research `code/minlp_solver_lab` directory, with the original venv executable path intact, one BLAS/OpenMP thread and `PYTHONPATH` pointing to the extracted `instances/gdplib_src`:

```bash
/path/to/existing/.venv/bin/python lbesh_results_independent_audit.py \
  --fresh-validation \
  --compare-analysis results/lbesh_development/analysis_v1/analysis.json \
  --sensitivity results/lbesh_development/gurobi_trig_sensitivity_v1.jsonl \
  --legacy-initialization \
    results/lbesh_development/legacy_initialization_v1.jsonl \
  --out /tmp/lbesh-paper-stage04-fue1r0qb/fresh-audit-extracted-models.json
```

This passed: all 1,464 saved benchmark records and 6,122 analysis fields reconcile, all 174 feasible enumeration witnesses validate, and no cross-witness bound/status contradiction is found. The 42 roots and 378 assignment calls remain accounted for separately. The result is copied to `evidence/stage04-relocated-audit.json`. An explicit import-origin probe verified `gdplib`, `gdp_instances` and `lbesh_research.validation` inside the extracted research tree.

A final source package, after the import-path documentation fix, was extracted freshly into `/tmp/lbesh-paper-stage04-final-lrixab5c`. All 62 payload hashes/sizes passed; a clean TeX build passed and produced exactly the same extracted PDF text as the authoritative PDF. There are no overfull boxes, undefined citations/references or multiply-defined labels. One inherited underfull bibliography URL is harmless. No benchmark timings were rerun and no clean Python installation is claimed: relocation reused the existing pinned installation. No project-wide checks or CI inspection were performed.

## Issues caught and resolved during authoring

The first draft of the reproducibility appendix produced three overfull filename lines; breakable `\path` formatting resolved all three. The first relocation driver used `Path.resolve()` on the venv Python executable, which followed its symlink into the base environment. Regenerated figures then differed only in Matplotlib's embedded version string (3.11.1 versus the intended 3.11.2), and the explicit byte-identity assertion failed. The driver was corrected to preserve the venv executable path, and all 21 outputs then matched exactly. No original figure or frozen result was changed to hide the discrepancy.

A subsequent import inspection found that the reused venv's editable GDPlib installation could still load the original checkout despite running the audit in the extracted directory. The explicit extracted-source `PYTHONPATH` fixed this; the full fresh audit was rerun to a new output path after verifying import origins. Both README and paper appendix document the requirement. The initial otherwise passing audit was not treated as the final portable-source check.

## Visual inspection

Rendered and inspected pages 1, 16, 17, 31, 41 and 42 (abstract/title, primary tables, work table and cost figure, oracle figure/diagnostic, and artifact/command appendices). Text, equations, table labels and plot annotations are legible and unclipped. All 17 tables and two figures remain in the output. The final additional import-path line was then included in the clean final build, which retains 42 pages and no overfull boxes.

## Review handoff

The source fingerprint is `stage04-author-source-sha256.json`. Reviewers should assess the abstract/discussion scope, consistency of the concise theorem overview with the full appendices, reader flow after moving proofs, portable instructions and archive contents, and delivery/source consistency. All accepted scientific sections and raw research evidence remain unchanged. Independent Stage 4 acceptance and the full-manuscript Stage 5 cycle are still required.
