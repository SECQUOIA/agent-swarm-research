# Final manuscript corrections and delivery

Correction agent: `stage08_corrections`, separate from the author and all five
whole-manuscript reviewers. Authority: `assessments/stage08-round01.md`, including
root's additional minor literature finding S8-3. Date: September 9, 2026.
All three accepted minor findings are corrected. Root verification and final
acceptance remain pending; this report does not mark acceptance.

## Corrections

| Finding | Completed change | Evidence |
| --- | --- | --- |
| S8-1: export dependency closure | Created separate standalone LaTeX and computational ZIPs. The supplement preserves the common parent of `paper-structured-bilevel/` and the nine relevant sibling code directories, includes historical comparison data, original diagnostic outputs and harness-failure records, and maps all 11 recorded inputs to supplied measured files. | Both actual archives were extracted outside the repository; all documented non-timing commands passed. |
| S8-2: sparse-power objective sign | Example `ex:sparse-power-output` now explicitly states `z_2-z_1=x^{2/p}-x^{1/p}`. | The existing completed square and all subsequent bounds are unchanged. The corrected example renders clearly on page 28. |
| S8-3: pessimistic coupling constraints | Added the concise Henke--Lefebvre--Schmidt--Thürauf comparison after Ketkov--Prokopyev and the verified JOTA reference. | Independently inspected the primary manuscript's standing assumptions, universal-feasibility model and Theorem 3.3. The comparison restricts its conclusion to that displayed reformulation, which adds the follower-sized vector to the leader. No general impossibility claim is made. |

For S8-3, the primary manuscript is [On Coupling Constraints in Pessimistic
Linear Bilevel Optimization](https://optimization-online.org/wp-content/uploads/2025/02/pessimistic-w-wo-coupling.pdf),
with [published DOI](https://doi.org/10.1007/s10957-026-03026-x). Root separately
verified the publisher metadata and full published article. The new entry is
JOTA volume 210, article 25 (2026). No theorem, proof or novelty claim changed.

## Exact scope

Among the 31 reviewed files, exactly four changed:

- `sections/01-foundations.tex`: the additional related-work paragraph.
- `sections/04-accuracy.tex`: the explicit signed objective.
- `references.bib`: the additional citation.
- `README.md`: final artifact locations, standalone build and reproduction
  instructions, with root acceptance explicitly pending.

The other 27 reviewed files are byte-identical, including every appendix,
all other sections, `main.tex`, all scientific code, raw data, tables, figures
and the coverage record. The reviewed snapshot manifest retains SHA-256
`d487e138b70585e03d5affa52a23e03631a30a45165651ddbe9d286162643231`.
The complete difference is `verification/stage08-corrections/changes.diff`.
No surrounding repository source, historical record, status, assessment or
snapshot was modified.

New delivery files are `paper.pdf`, the two ZIPs, and the following files under
`delivery/`: `README-source.md`, `README-supplement.md`, `build_archives.py`,
`verify_archive.py`, `measurement-provenance.json`, and `archive-manifest.json`.
Verification scripts, command records, logs, extracted PDF text, three page
images and manifests are under `verification/stage08-corrections/`.
These internal verification records are excluded from both submission ZIPs.

## Delivered artifacts

| Artifact | Contents | SHA-256 |
| --- | --- | --- |
| `paper.pdf` | 78-page manuscript, blank author field, built from the actual exported source | `0bfddf160785d5b900b4ea6c35f15e68815002edc49065ccc34c96eb1bebf4ee` |
| `structured-bilevel-latex-source.zip` | 17 scientific inputs, standalone README and hash manifest; 19 files | `e701924cf71aed88365743e157604494099c0d8eb75c3b76c836a8368649d538` |
| `structured-bilevel-computational-supplement.zip` | Standalone computational dependency closure, provenance and documentation; 135 files | `bc14cd60de36e01a34e75f6019d53922313d4e70e6b0990d0c9427f8ebb8c32f` |

Each archive contains its own `SHA256.json`. The supplement additionally has
`verify_archive.py`, `requirements.txt` and `measurement-provenance.json`.
`delivery/archive-manifest.json` records the archive identities and every
exported file hash. Repeating the archive builder gave byte-identical ZIPs.
No user literature originals, internal manuscript reviews, source notes,
build intermediates or unrelated repository material are exported.
Computational scripts with historical names containing `review` are exact
checks, not manuscript reviewer reports.

The supplement includes the exact measured solver, experiment driver and
full-task helper at their preserved archival paths. All 11 input hashes in
the raw record match their mapped exported files. Removing the single
`constraints = tuple(constraints)` line from the current solver reproduces
the measured solver byte for byte. The README explains that the iterator
correction was not timed and that recorded calls used lists or tuples.
The raw timing record is unchanged, with SHA-256
`29d0bf7b85001b96f50fcd220164bd019238a2132ea866daba73d5863bc8af7f`.
No new timing campaign was run and no timing was replaced or relabeled.

## Verification on actual exported inputs

The reproducible validator is
`verification/stage08-corrections/validate_exports.py`. It created the independent
workspace `/tmp/structured-bilevel-export-kt9mt75c`, extracted each ZIP into its
own directory, removed `PYTHONPATH` and put the selected Python interpreter
first on `PATH`. No symbolic link or import from the original repository was
used. The tested Python and package versions match the recorded environment;
Matplotlib 3.11.1 was additionally used for figure generation.

From the extracted source directory, this command succeeded:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

The final log has no warnings, undefined references or citations, overfull or
underfull boxes, or errors. The resulting PDF has 78 pages and an empty author
metadata field. I visually inspected the new comparison on page 3, the signed
example on page 28 and the bibliography entry on page 76; all are readable
and fit the established layout.

From the extracted supplement root, every documented non-timing command
completed successfully:

```sh
python verify_archive.py
python paper-structured-bilevel/code/summarize_experiments.py
python paper-structured-bilevel/code/run_diagnostics.py
python paper-structured-bilevel/verification/stage02-author/check_support_recovery.py
python code/bilevel_reopened/nearoptimal_second_review.py
python code/bilevel_reopened/screening_review_checks.py
python paper-structured-bilevel/verification/stage04-author/check_sharp_modulus.py
python paper-structured-bilevel/verification/stage05-author/run_checks.py
python paper-structured-bilevel/verification/stage05-author/check_padding_and_recovery.py
python paper-structured-bilevel/code/plot_contacts.py
```

The integrity check passed for all 134 manifest-listed supplement files and
all 11 measured input mappings. The complete implementation driver passed all
five families, including the 18 original-coordinate/compressed upper-task
comparisons and iterator assertions under both semantics. The boundary driver
passed all eight constituent scripts. Support recovery, the modulus, robust
and screening checks, padding/recovery and figure generation also passed.
The table generator reproduced all three TeX inputs byte for byte and retained
the raw-record hash. Figure generation ran only in the extracted copy, so the
original figure and its recorded hash remain unchanged.

All 13 recorded commands, including PDF metadata/text extraction, have exit
code zero in `commands.json`. `computational-validation.json` records the
five child-family outcomes and table hashes. `manifest.json` records the
changed files, preserved inputs, final artifacts and build result. The
standalone supplement reproduces the documented finite computations; it does
not claim to implement the general quantifier-elimination algorithms or
reproduce machine-dependent timings exactly.

Remaining accepted issues: none. No new major issue was found. No further
agents were dispatched. Root acceptance and the accepted snapshot are reserved
for the parent agent.
