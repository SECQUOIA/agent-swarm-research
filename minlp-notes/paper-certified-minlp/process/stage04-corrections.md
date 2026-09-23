# Stage 4 corrections

Completed 2026-09-14 by the correction agent, distinct from the author. Read the
adjudication and all five independent reviews. All five accepted minor findings
are addressed. No frozen production module, mathematical rule, protocol,
campaign count, formal source, or acceptance status was changed.

## Finding-to-change map

1. **R1: saved-solver flag.** Section 6 now specifies the exact one-sided
   criterion `s*(B-r_solver) > 10^-6*max(1,abs(B))` and included saved model-status
   codes `{1,2,8}`. The count remains eighteen investigation candidates. The
   library-reference metric retains its separate reference-based denominator.
2. **R2: historical restoration.** Kept the complete V1/V2/V3 frozen source
   directories and original manifests unchanged. Added a separate
   `evidence/source-snapshots/shared-data/` directory containing the thirteen
   common test-fixture/helper and quadratic-example files, with a supplemental
   manifest of their sizes and SHA-256 hashes. Its files match the default core;
   existing V2/V3 fixtures are identical. The quadratic README retains its
   archival/portable-workflow notice. The snapshot README now gives explicit
   commands to replace versioned `certify`/`lbesh` code in a separate evidence
   copy and then restore shared data. The main core README points to those
   commands and states all three expected test counts. The original source
   manifests are not retroactively extended to claim these were frozen files.
3. **R3: rational length.** Section 6 now says “a rational bound with a
   4,326-digit numerator,” correctly identifying the component triggering the
   report-construction conversion limit.
4. **R4: reference rounding.** Section 6 describes the small `risk2bpb`
   discrepancy as consistent with rounding at the displayed reference precision.
   It no longer asserts this as an established cause or establishes feasibility
   or provenance from proximity.
5. **R5: core contents.** Section 6 and the outer supplement README now specify
   pinned dependency specifications and all 289 campaign models. Installed
   dependency binaries and excluded models are not claimed as bundled.

## Packaging change and bulk preservation

Rebuilt the small core using `experiments/package_evidence.py --phase core`.
The packager previously recomputed the bulk digest even in core-only mode.
A bounded edit now retains the existing bulk index record after checking the
recorded file size; `archives.json` explicitly labels that digest as reused.
This is not fresh hash verification. If no matching prior index exists, the
core phase computes the digest normally, preserving the initial bulk-then-core
workflow. Other phases still hash newly built bulk archives. A miniature isolated
archive exercise passed bulk-only creation, initial core creation without an
index, and repeated core creation with explicitly labeled digest reuse; see
`stage04-corrections-packager-phases.log`. No general cache or new production/checking behavior was introduced.
The portable packager copy in the core reflects this change.

The rebuilt core has 3,793 manifest entries, and its archive is **6,478,558
bytes**, SHA-256
`80ef5d50faefc97e01832f06b1f730a3a906b7d5b2ca9d8609453df9561f1fc6`.
The outer README and machine-readable index match these values. The new core
archive digest was independently recomputed after packaging.

The bulk remains **30,664,561,063 bytes**, with retained SHA-256
`88c23497c2d20c76b3ac25cfc2c60a529aecb35da98e8de00213f4513ed314d4`.
The original bulk manifest and `stage04-bulk-readback.json` are byte-identical
before and after this correction. The three original versioned source manifests
also remain byte-identical. Their preservation hashes are recorded in
`stage04-corrections-preserved-hashes.json`. No large archive was reread or
rewritten, and no numerical campaign or large-proof replay was repeated.

## Restored-version validation

Extracted the newly rebuilt core into a fresh temporary directory. Used the
existing isolated Python 3.13 checker/test environment, with `PYTHONPATH` unset,
`PATH=/usr/bin:/bin`, and bytecode writing disabled. All 3,793 core manifest
entries passed before and after validation. After the final packager-only
adjustment, a newly extracted final archive passed all entries again. Its source
and shared-data files are unchanged from the tested restored versions.

For each version, made a separate copy of the extracted tree, removed the
default module directories, copied in the frozen version, and restored the
shared data exactly as documented. Checked every original versioned source
hash and every supplemental shared-data hash in each restored tree.

| Restored version | Tests | Representative entry point |
|---|---:|---|
| V1 primary | 152 passed | Passed |
| V2 producer repair | 153 passed | Passed |
| V3 reporting repair | 161 passed | Passed |

Each representative entry-point run was the complete `reproduce.py small`
command: four full certificate bundles, exact source/primal audits including
optimum 6545, and all fifteen local failed-step extracts. This includes the
quadratic bundle previously lost during restoration. Reports went to separate
new output directories. The unchanged default V3 suite was not redundantly run
in addition to the restored V3 suite.

Results and temporary locations are recorded in
`stage04-corrections-restoration-validation.json`. Per-version test and small
logs, extracted-manifest logs, and the core-packaging log use the
`stage04-corrections-` prefix in this process directory.

## Manuscript validation

A fresh isolated copy of the LaTeX sources, bibliography, and generated tables
was built in `build/stage04-corrections/` with
`latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`. The build
returned zero and produced a 28-page PDF. The final log has no warnings,
undefined references/citations, or overfull/underfull boxes. PDF text extraction
succeeded. The build transcript is `stage04-corrections-build.log`.

No additional issue was found. Stage acceptance remains the coordinator's
responsibility.
