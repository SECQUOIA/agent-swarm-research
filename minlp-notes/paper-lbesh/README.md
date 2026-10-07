# Radial and point separation for convex GDP

This directory supplies a complete anonymous research manuscript, its standalone source, compact data, and the frozen research supplement. The scientific contribution is a matched computational comparison of radial and point separation in an NLP-assisted convex GDP solver. The manuscript makes no priority claim for the established cut family or solver framework. Authorship, affiliations, funding declarations, and a public archival DOI have not been invented.

## Deliverables

- `main.pdf`: current manuscript, including complete proofs, model specifications and computational appendices.
- `dist/paper-lbesh.pdf`: submission copy, refreshed by the packaging script.
- `dist/paper-lbesh-source.tar.gz`: compact standalone source, bibliography, tables, figures, data and verification scripts. It excludes the large research archive and internal review records.
- `supplement/publication_bundle_v1.tar.gz`: public copy of frozen research sources, raw runs, witnesses, logs, analysis, environment declarations and model licenses.
- `SHA256SUMS`: hashes of the three delivery files, with paths relative to this directory.
- `dist/source-manifest.json`: hashes and sizes of every source-archive payload file. A copy is embedded as `source-manifest.json` inside the source archive.

The `dist/` files, `SHA256SUMS`, and the reviews described under "Verification performed" cover the 2026-09-19 version (commit `8e4dac61`). The manuscript sources were revised afterwards in commit `aee2afbf` (2026-09-24), which also rebuilt `main.pdf`, and in any 2026-09-25 audit follow-up edits. The packaging script was not rerun, so the `dist/` files and manifests do not contain the current sources, and no review of the later revisions is claimed. The study records and scientific outcomes remain frozen. Public package hashes describe privacy and portability edits; the historical review and timing records were not rerun.

The bibliography and generated graphics are local. The paper does not depend on repository notes or online references to supply a definition, proof or experimental result. `evidence/coverage.md` and `evidence/literature.md` document scope and sources consulted. Internal staged authorship, five-reviewer reports, dispositions and checks remain in `process/` in the repository, outside the submission archive.

## Build and regenerate the paper

Extract the source archive into a new directory, then run from its `paper-lbesh` directory:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

A standard TeX Live installation with latexmk, BibTeX and the packages declared in `main.tex` is sufficient. The prebuilt figures and tables require no Python, network or solver. The local `.bbl` is included as well as `references.bib`. `latexmk -c main.tex` removes intermediate build files while retaining the PDF.

To regenerate the numerical presentation:

```bash
python scripts/regenerate.py
python scripts/check_evidence.py
```

Python plus Matplotlib is needed for figure generation; the writing environment used Python 3.13.11 and Matplotlib 3.11.2. Use `python scripts/regenerate.py --no-figures` for standard-library-only table/CSV generation. The generator checks all immutable compact-input hashes, retains all 1,464 outcomes, and writes 17 tables, two PDF figures, `data/records.csv` and `data/table_values.json`. It does not reevaluate primal model expressions. The separate evidence checker independently reconstructs all 51 coefficient streams and checks secondary numerical claims. See `data/README.md` for schemas and numerical acceptance semantics.

## Extract and audit the research supplement

The large research archive is delivered separately. Place it at `supplement/publication_bundle_v1.tar.gz` in the extracted paper directory; its small manifest/checksum documents are already in the source package. Verify and safely extract it into a **new or empty** `research` directory:

```bash
python scripts/verify_supplement.py \
  supplement/publication_bundle_v1.tar.gz --extract research
python evidence/check_stage02.py --research-root research
```

The verifier checks the fixed archive hash, every payload hash and size, and the complete member inventory. It rejects links, special files, duplicates and unsafe paths. The second command performs the explicit analytic-example and frozen-source-default checks; its required argument prevents silently skipping source inspection. The full archive retains the original source freeze, all native logs and third-party model licenses. It includes no environments, solver binaries or downloaded literature PDFs.

For the full saved-result audit, use Python with the archived dependencies. For a fresh installation, enter `research/code/minlp_solver_lab` and run `uv sync --frozen`; optimization reruns additionally need native solvers and licenses described in `LBESH_RESEARCH.md`. Activate that environment, then run from the same directory:

```bash
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export PYTHONPATH="$PWD/instances/gdplib_src"
python lbesh_results_independent_audit.py \
  --fresh-validation \
  --compare-analysis results/lbesh_development/analysis_v1/analysis.json \
  --sensitivity results/lbesh_development/gurobi_trig_sensitivity_v1.jsonl \
  --legacy-initialization \
    results/lbesh_development/legacy_initialization_v1.jsonl \
  --out /tmp/lbesh-new-audit.json
```

The output path must not exist. Setting `PYTHONPATH` as shown selects the extracted GDPlib sources even when an existing Python environment has an editable installation pointing elsewhere. This audit checks all eight saved schedules and source metadata, freshly evaluates supplied original-model witnesses, and independently recomputes arithmetic for comparison with 6,122 analysis fields. It uses the original feasibility checker; it is not a second implementation of that checker. It verifies all 174 feasible enumeration witnesses and cross-witness bound/status consistency. No optimization performance run is launched.

The full experiment and continuous-cone schedules, exact options, historical software/hardware records and additional diagnostic commands are in the extracted `LBESH_RESEARCH.md` and archived plans. The conic-reference environment is separately locked under `lbesh_research/conic_reference_env`. Original outcomes, repeats and outcome-triggered follow-ups remain separate. Numerical solves require original-model feasibility, usable global bounds and the stated gap tolerance; they are not exact certificates.

## Refresh delivery after manuscript corrections

From the full paper directory, with the research archive present:

```bash
python scripts/package.py
sha256sum -c SHA256SUMS
```

Packaging first builds the current manuscript, writes a deterministic source archive (fixed member metadata and gzip time), copies the PDF and refreshes the manifests/checksums. It does not modify the frozen research archive. Run it again after any correction. The source archive excludes `process/`, temporary files, environments and recursive `dist/` contents.

## Verification performed

The five-stage author/review/correction process is complete: five independent agent reports per stage, including the final whole-manuscript review, with all valid findings corrected. No accepted finding was major. These 25 internal agent reviews are distinct from external journal peer review and do not guarantee acceptance. The final corrections narrow the PAR10 explanation to its single-tree comparisons and define the recorded row-separation timer consistently; no numerical evidence was changed.

The manuscript was built cleanly after relocation; all tables and figures regenerated identically. Local arithmetic/parameter checks, mandatory source/example checks against the extracted research source and the complete fresh saved-result audit passed. That portability check reused the existing pinned Python installation rather than installing a fresh environment. It did not rerun benchmark optimization timings. Targeted generator, cone and solver tests and detailed commands/results are retained in the repository review records. No project-wide checks or CI status/log inspection were used.
