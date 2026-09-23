# Stage 3 independent review 5

Reviewed 2026-09-09. Frozen input: `stage3-round1/paper-network-simplex`, its sibling code, and the delivery artifacts. Comparison: `stage2-accepted`. I read the author report, change record, delivery documentation, builder, revised computational exposition, and relevant implementation interfaces. I followed `process/REVIEW_GUIDANCE.md`; I did not read other current review reports, coordinate judgments, edit frozen sources, or delegate work.

**Verdict: accept Stage 3. No major or minor finding requires correction.** The archives worked as standalone deliverables in the independent extraction and fresh environment described below. This verdict concerns Stage 3, not completion of the separate whole-manuscript review.

## Standalone use and dependency closure

I extracted both ZIP files under `/tmp/stage3 reviewer5 d5okk6d0/`, deliberately using a directory name containing spaces. Execution did not depend on the repository working directory or an inherited `PYTHONPATH`. The source archive has 20 entries and the supplement has 40; archive names have no absolute paths or parent-directory traversal. Both payload manifests passed.

I followed the supplement's environment instructions: created a fresh Python 3.13.11 virtual environment and installed `requirements.txt`. Installation succeeded with NumPy 2.5.1, SciPy 1.18.0, SymPy 1.14.0, and the resolved SymPy dependency mpmath 1.3.0. This checks actual dependency availability and installation, rather than merely relying on the workspace's existing libraries.

All 19 recorded test/check/smoke commands in `documented-results.json` completed with exit status zero. These include:

- The principal suite: **23 tests passed**.
- All three implementation audit commands: independent flat audit, compressed audit, and compressed integration.
- All six original mathematical-check commands and all five additional `checks/` commands.
- Canonical table regeneration and subsequent payload-hash verification.
- The documented one-repetition benchmark smoke run.

The dynamically loaded unreduced comparator and the bounded-rank helper were therefore exercised from the extracted package. Their dependency closure is supplied by the archive; no source copy from the repository was needed. The additional exact-contract checker is adapted to the supplement root and ran successfully there.

I also executed the verbatim Python example from `API.md` with the virtual environment interpreter's `-S` option, which disables site-package loading. It passed. This gives a direct check of the documented standard-library-only exact graph interface, separate from the dependency installation needed for LP comparisons.

## Full reproduction and retained measurements

After the documented smoke run, I ran the complete generator from the extracted supplement:

```sh
PYTHONPATH=code .venv/bin/python -m network_simplex_benchmarks.paper_stage06 --output rerun-benchmarks.json
```

It completed successfully with five repetitions, 16 flat cases, three membership cases, and three optimization cases. This was my own full extracted-package run, not reliance on the author's smoke run or the root's earlier study.

I independently compared 5,750 non-timing leaves of the flat, membership, and optimization records against the canonical data, omitting timing summaries and fields ending in `_seconds`. No differences were found; numerical leaves were compared with absolute tolerance `1e-7`. Thus the current generator reproduced the retained inputs, observations, objective data, method orders, statuses, model sizes, and audit outcomes within that stated numerical tolerance. This is not a claim of timing reproducibility or an exact proof of numerical LP optima.

I then followed the README's separate-extraction procedure for rerun tables: extracted another copy, replaced its canonical data file with the new complete-run JSON, and ran the table generator. It passed all complete-grid, method, status, rotation, and summary checks and produced the five table/value files. Earlier, regeneration from the untouched canonical data passed and left every original manifest hash valid. The canonical JSON retained its documented hash `373ce70b3839c12a206b193e9952d856f585da400f902bda773a725a609f73ac`.

The provenance fields in the canonical JSON do mention an earlier archive. The supplement README explicitly identifies those fields as historical provenance, supplies the necessary current sources, and gives working commands that do not require the old archive. I therefore do not regard those references as a broken reproduction dependency.

Evidence: `full-study-results.json`, `rerun-benchmarks.json`, `full-benchmark.log`, `documented-results.json`, and the per-command logs.

## Source build, anonymous metadata, and deterministic delivery

I ran the source archive's documented build command directly from its extraction:

```sh
SOURCE_DATE_EPOCH=946684800 FORCE_SOURCE_DATE=1 latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The build succeeded. The final log has no warning, overfull-box, or underfull-box diagnostics. The resulting 50-page PDF is byte-identical to the frozen `delivery/submission.pdf`, with SHA-256 `21d09299cee1b7f9c6deece832a29aa6d96bb3402bcefdf9ca8e1c7d8aaff816`. The frozen `main.pdf` also matches that artifact.

I separately ran the frozen delivery builder with `--output` directed into my evidence directory. It reproduced `submission.pdf`, both ZIP archives, and `manifest.json` byte-for-byte. The explicit source selection, temporary external LaTeX build, fixed ZIP metadata, and source-date controls work for this toolchain. The documentation correctly limits byte identity to the same inputs and toolchain rather than promising cross-version identity.

`pdfinfo` reports an empty Author field, Creator `LaTeX`, the intended scientific title/subject/keywords, and no creation or modification dates or metadata stream. Source and archive-text scans found no workspace-owner identifier, private home path, Codex/OpenAI attribution, or current review-report identifier. PDF text had no private-path or workspace-owner matches. The author/date fields in the manuscript are empty. Internal reports, external literature PDFs, and private build logs are absent from the archives.

I visually inspected the rendered first page and page 47, which contains reproduction instructions and the start of the conclusion. The title/abstract, commands, mathematical notation, and paragraph layout are readable and unclipped. The build diagnostics and extracted text supplement that limited visual check; I did not visually inspect every page.

Evidence: `source-build-results.json`, `source-build.log`, `main.log`, `pdfinfo.txt`, `paper-layout.txt`, `initial-checks.json`, `rebuild-results.json`, and the two rendered page images.

## Exposition, scope, and certificate claims

The revised `sections/08-computation.tex:264–293` explains the current comparators directly. Removing the old-builder narrative does not remove the unfavorable boundary-face result: the positive-state and one-flow LPs remain explicitly faster than the reduced exact oracle at the stated 512-gadget boundary query. The text also states where the general compressed formulations were not timed. The distinction between a two-observed-label workload and separate three-observed-label library setup remains clear.

The reproduction subsection (`sections/08-computation.tex:339–375`) correctly separates new measurements from regeneration of the published tables. Its relative paths work from the supplement root. The top-level supplement README distinguishes validation dependencies from the historical measurement environment and explains shared-host and synthetic-data limits.

The manuscript, supplement README, and `API.md` consistently distinguish:

- exact rational model assembly from numerical optimization;
- an exactly checked projected Farkas cut from an uncertified or numerical status;
- exact constructive recovery in the specialized interfaces from the general compressed interface, which does not return an exact feasible decomposition;
- production specialized interfaces from bounded-rank verification prototypes;
- an exact equality-flow component hull from its intersection with additional coupling rows.

The documented exception behavior and indexing conventions match the interfaces inspected. Compact defaults and materialized dense flows are distinguished. The supplement does not present finite computations as proofs of universality or arbitrary-size coefficient results.

An independent comparison found all **66 theorem/lemma/proposition/corollary/proof environments byte-identical** to accepted Stage 2. Only the computational section changed among the section files; the bibliography is unchanged. All 17 packaged files under `code/` match the accepted Stage 2 snapshot. The mathematical claims and qualifications previously reviewed are therefore preserved rather than silently changed during packaging. Evidence is in `preservation.json`.

## Enumerated findings

1. **Major findings:** none.
2. **Minor findings:** none.
3. **Unresolved standalone-use or anonymity defect requiring an author change:** none identified.

## Optional preferences and limits

No optional preference requires action.

Validation used one Linux/Python/TeX environment. I did not test Windows shells, different Python or TeX versions, offline installation, or cross-platform archive byte identity; the documentation does not promise those results. Anonymity checks cover explicit metadata, packaged text, and the inspected pages, not whether the scientific subject could allow an informed reader to infer authorship. The complete benchmark rerun and exact-check programs establish reproducibility and finite evidence on these inputs, not exhaustive software correctness or a universal performance ranking. I did not redo the full mathematical review or a new literature-priority search in Stage 3.
