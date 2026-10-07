# Quadratic intersection-cut evidence companion

From the unpacked companion directory, check the package with Python 3.9 or later:

```sh
python3 check_manifest.py
```

This checks the wrapper hashes, retained original bytes, JSON and JSONL record
counts, and the primary multiround cohort. It runs no solver, experiment, or
mathematical certificate replay.

The top-level `manifest.json` describes the wrapper and points to
`archive/manifest.json`, which maps each selected original repository-relative
path to its submitted path and hash. `archive/source/` contains those unchanged
original files. `archive/README.md` explains evidence classes, corrections,
withdrawn timing claims, unresolved debug issues, and separate exact-verification
entry points. `archive/neutral-reference.json` records omitted source-context
hashes and the optional raw-fidelity archive checksums.
`archive/survey-labels.json` connects manuscript labels R1–R8 to saved numerical
coordinates and exact original record names and selectors.

`evidence-companion.tar.gz` contains the same evidence as the `archive/` tree;
`SHA256SUMS` records its compressed checksum. `verification.md` records the
targeted local checks. The selection and build script preserve packaging
provenance; rebuilding requires the original repository files.

The wrapper uses neutral metadata. Original-byte sources may contain names,
URLs, and absolute paths, so this package is not certified anonymized. No
redistribution license was added.

## Public export

This public copy contains privacy and redistribution edits. Current package hashes describe the exported files; `original_sha256` records identify the original committed bytes when an exported file changed. Historical experiment and review hashes remain provenance records. Scientific result values were retained, and the experiments were not rerun. Repository-level `THIRD_PARTY_NOTICES.md` records licenses for retained third-party material.

`build_archive.py` and `selected-sources.json` record the original packaging procedure and approved source hashes. They are historical provenance records. The current public export includes privacy edits, portable paths, and third-party notices; verify it with `check_manifest.py` and `inspect_archive.py`. The package inspectors check saved evidence and do not rerun optimization experiments.
