# Stage 5 corrections

Completed 2026-09-14 by the correction agent, distinct from the author. Read
`stage05-adjudication.md` and `stage05-review4.md`. Addressed both accepted minor
findings. No mathematical statement, checker rule, numerical record, source
version, formal source, or acceptance status changed. Stage 6 was not begun.

## Finding-to-change map

1. **OA and SOS terminology.** The introduction now defines “outer approximation
   (OA)” when first introducing the method. The implementation contract now
   expands “special ordered set (SOS) constraints” on first use, avoiding
   ambiguity with the literature's sums-of-squares witnesses.
2. **Campaign-table reference metric.** The table caption now identifies `d` as
   the signed normalized difference from an unverified reference, links to the
   definition in the bound-quality subsection, and states that reference rows
   count only verified bounds. Added the stable subsection label
   `sec:reference-comparison`. Changed the caption in `experiments/analyze.py`
   and regenerated `tables/campaign-results.tex`, preserving every numerical
   row and column. The distributed generator/table copies are byte-identical
   to the current originals.

## Analysis and core validation

Regenerated the primary analysis into a new temporary directory. All seven
other data/TeX outputs are byte-identical to the prior versions. The campaign
results differ only in their caption. Refreshed `analysis-inputs.json` to
identify the edited generator while preserving all numeric input records.
Details: `stage05-corrections-table-comparison.json`.

Rebuilt the core with `experiments/package_evidence.py --phase core`, retaining
and explicitly labeling the previously verified bulk digest. The bulk archive
was not reread or rebuilt. The current core is **6,478,681 bytes**, SHA-256
`d2805b1cfead992904b840d4a63c913287d42aec309f1502b1d4e90e9d2e9f1b`.
Updated `supplement/archives.json`, the outer supplement README, the paper
README, and Appendix A's exact size. Prior dated reports remain unchanged as
provenance of their then-current artifacts.

Extracted the rebuilt core into a new directory, verified all **3,793** manifest
entries, and reran its portable analysis with no repository import path. Every
regenerated numerical/TeX output matches the paper copy; the only differing
analysis-input manifest fields identify the relocated script/input paths.
Generator and campaign-table bytes also match directly. Logs and details are
`stage05-corrections-core-packaging.log`,
`stage05-corrections-core-verify.log`,
`stage05-corrections-extracted-analysis.log`, and
`stage05-corrections-extracted-core.json`.

## Final paper and source archive

After all metadata updates, ran `scripts/build-paper.sh` to replace root
`main.pdf` and `main.bbl` from a fresh source directory. The PDF has **32 pages**;
the final log has no warnings, unresolved references/citations, or overfull/
underfull boxes. The caption's forward definition reference resolves.

Ran `scripts/package-source.py` to regenerate `PAPER-SHA256SUMS`, the source
archive, and its external index. The source archive contains **49 entries** and
is **476,986 bytes**, SHA-256
`eec96aede453c418800c357cd85190661ff6250e59b1ee2387e51c48f91bf756`.
A repeated invocation without source edits produces the same archive bytes.

Extracted the source archive to another fresh directory. All source-manifest
hashes and all thirteen formal-package hashes pass. Its documented build script
runs without the parent repository, produces no LaTeX diagnostics, and creates
bibliography bytes and extracted PDF text identical to the delivered root
build. Results and paths are in `stage05-corrections-source-extraction.json`;
source/formal hash checks and the clean build have separate matching-prefix
logs. Current root build logs and extracted text are under `build/`.

The preservation audit in `stage05-corrections-preserved-hashes.json` confirms
unchanged production modules, formal package files, generation/replay records,
original bulk manifest, and original complete bulk-readback record. No checker
test, solver run, full proof replay, or bulk readback was repeated for these
wording-only corrections. No additional issue was found; acceptance remains
the coordinator's decision.
