# Companion verification record

Construction used the approved selection after its source count and size were
reported. The submitted payload preserves 1,393 original files totaling
80,680,117 bytes. Nine optional source notes and closeout documents were omitted;
their relative paths, sizes, and original hashes are in `neutral-reference.json`.

The archive is `evidence-companion.tar.gz`, 12,387,186 bytes. Its SHA-256 is
`f027b4f952f8ba25d3a291d59bb12c2bccf52702498145e87975c0bba0e9e0e6`.
`SHA256SUMS` provides the same detached checksum.

The following targeted commands ran from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 paper-quadratic-intersection-cuts/companion/build_archive.py
python3 paper-quadratic-intersection-cuts/companion/archive/check_manifest.py
python3 paper-quadratic-intersection-cuts/companion/inspect_archive.py
```

All exited 0. The manifest check verified 1,397 inventoried files totaling
80,710,667 bytes, including 1,393 unchanged originals. It parsed retained JSON and
JSONL record metadata and checked the 74 main/new trajectory files: 5,160 distinct
trajectories, 220 baseline instances, all recorded statuses `ok`, and exact
agreement with the cached numerical denominators. The size cohorts contain
60, 60, 50, and 50 baseline instances at 4×4, 6×8, 8×12, and 10×20.
The five completed closure-box records retain `status: complete` and empty queues.
These metadata checks do not verify mathematical certificate inequalities.

The compressed-archive check verified 1,398 regular members, neutral tar owner and
timestamp fields, safe relative member paths, all packaged file hashes, and
absence of the excluded benchmark, literature, cache, old-solver, and raw-fidelity
asset classes. It also matched the detached compressed-file checksum.

A scoped `rg -n 'https?://|/(home|Users)/'` check of the new wrapper files,
selection, and packaging tools found no matches (exit 1). Original-byte source
files were excluded from this wrapper scan. They may retain names, URLs, and
absolute paths, so the payload is not certified anonymized. No redistribution
license was added.

These are local companion checks. No experiment, solver, benchmark, certificate
generation, mathematical proof replay, literature search, project-wide check,
or CI inspection ran.

The final numerical-survey mapping adds `archive/survey-labels.json` and the
archive README table. Its eight labels refer to 12 original named survey rows;
the metadata checker compares the copied apex/ray coordinates and exact source
selectors to those retained rows. It does not execute coordinate constructors.
A read-only before/after manifest comparison confirmed that all 1,393 original
SHA-256 values match the pre-mapping snapshot. The build selection now pins those
hashes, and rebuilding leaves existing original payload files untouched.

The portable top-level entry point is also checked with:

```sh
python3 paper-quadratic-intersection-cuts/companion/check_manifest.py
```

It validates eight top-level wrapper files and the referenced payload-manifest
hash, then runs only the standalone record-metadata checker described above.

Read-only inline Python also parsed the three new wrapper scripts with
`ast.parse` and checked trailing whitespace in those scripts and the authored
README and verification record. The targeted checks passed.
