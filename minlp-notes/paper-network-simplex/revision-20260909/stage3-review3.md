# Stage 3 independent review 3

Reviewed on 2026-09-09. Frozen inputs: `stage3-round1/paper-network-simplex` and its sibling `code` directory. Comparison: `stage2-accepted/paper-network-simplex`. I followed the active review guidance, read the Stage 3 author report and relevant evidence, and did not read other current-round reports or coordinate judgments. All extraction, building, and testing used private locations; the frozen snapshot was not changed.

**Verdict: accept Stage 3. No major or minor issue found.** The source archive builds independently, the supplement runs its documented checks without repository dependencies, and the delivery artifacts reproduce byte-for-byte under the available documented toolchain. The revised computation prose is self-contained and preserves the quantitative results and limitations.

## Enumerated findings

1. **S3-R3-F0 — No actionable finding.** No major or minor correction is requested. The checks below support this verdict within their stated limits.

## Archive integrity, closure, and reproducibility

I extracted both frozen archives into the fresh directory recorded in `stage3-review3-evidence/extraction-root.txt`, under `/tmp`. I checked ZIP member uniqueness, safe relative paths, absence of symlink entries, and exact agreement between ZIP members and the delivery manifest. Both archives have the advertised single top-level directory. All entries use timestamp `2000-01-01 00:00:00` and mode `100644`.

The source contains 20 files including its manifest; the supplement contains 40. Every payload hash agrees with both its own `MANIFEST.sha256` and the delivery `manifest.json`. The own-manifest file list covers every payload file except itself, with no omitted or unexpected listed file. All 55 delivery input hashes agree with the frozen input files. Artifact byte counts and hashes agree with the recorded values, and frozen `main.pdf` equals `delivery/submission.pdf`. Evidence: `stage3-review3-evidence/archive-audit.json`.

From the extracted source root I ran exactly the documented build command:

```sh
SOURCE_DATE_EPOCH=946684800 FORCE_SOURCE_DATE=1 latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The build succeeds at 50 pages. Its final log has no undefined-reference/citation messages, LaTeX or package warnings, overfull boxes, or underfull boxes. I checked every actual `INPUT` record in `main.fls`: external inputs are exclusively system TeX files, with no repository or author-workspace dependency. The resulting PDF equals the frozen delivery PDF byte-for-byte. The private log, bibliography log, and recorder file are retained as `main.log`, `main.blg`, and `main.fls` in my evidence directory.

I also ran the frozen `delivery/build-packages.py` with `--output` directed to my private evidence directory. The rebuilt PDF, both ZIP archives, and `manifest.json` are each byte-identical to the frozen delivery files. This independently verifies the builder's current deterministic-output claim rather than relying on the author comparison. The explicit file selection includes the otherwise easy-to-miss unreduced comparator and bounded-rank helper. Evidence: `rebuild-output.json`, `reproduction-audit.json`, and `rebuilt/`.

After all checks and canonical table regeneration, both extracted payload manifests still pass in full. This confirms that the documented commands produce reports without silently modifying packaged code or canonical data, and that all five regenerated table/value files exactly match their archived bytes. Evidence: `post-run-audit.json` and the two `*-post-manifest.log` files.

## Anonymous delivery

The source has empty author and date fields. `pdfinfo` reports the intended paper title, subject, and keywords, an empty author, creator `LaTeX`, and producer `pdfTeX-1.40.25`. Creation/modification dates and an XMP metadata stream are absent. `pdfdetach -list` reports zero embedded files. I scanned the manifest-covered archive text and extracted PDF text for the workspace owner's identifier, private home paths, and obvious assistant/service identifiers; no matches were found. The ZIP inventories contain no private logs, reviewer reports, literature PDFs, or unrelated research directories.

The privacy checks apply to the actual distributable payloads. Private author/reviewer evidence naturally contains local command paths and is not part of either archive. Evidence: `pdfinfo.txt`, `submission.txt`, `archive-audit.json`, and `post-run-audit.json`.

## README, API, and executed commands

I read the delivery guide, both packaged README templates, `API.md`, requirements, the builder, and the affected manuscript reproduction instructions. I compared API statements with the packaged constructors, result objects, `flow` methods, numerical optimizer, and exact certificate routine. The explicit/residual label indexing, incoming-minus-outgoing convention, normalized positive-state flows, compact versus dense output, supported graph classes, and certificate status distinctions are consistent. The README correctly distinguishes the validation dependency versions from the historical timing environment. The packaged API example executes unchanged and returns its asserted exact violation.

All execution below occurred from the extracted supplement root with its packaged `code` directory, not from the repository. The environment is Python 3.13.11, NumPy 2.5.1, SciPy 1.18.0, and SymPy 1.14.0, matching the package validation documentation.

| Documented check | Independent result |
|---|---|
| Principal `unittest` command | All 23 tests pass |
| Independent flat implementation audit | Pass |
| General compressed verification | Pass |
| General compressed integration | Pass |
| Six original mathematical-check commands | All pass |
| Five additional `checks/` commands | All pass |
| `API.md` Python example | Pass unchanged |
| Canonical table generator | Pass; all five output files remain manifest-identical |
| Quick benchmark with one repetition | Pass: four flat cases, one membership case, one optimization case |

The smoke run successfully imports and executes the packaged unreduced comparator, so that dynamic-file dependency is exercised rather than merely present in the ZIP. The bounded-rank recovery check also runs with the packaged helper. The exact-versus-numerical qualifications in the README match what these programs do. The additional Fibonacci program uses LP only to propose rows and then verifies the resulting certificates exactly; the documentation says so.

Exact commands, return codes, and logs are retained in `additional-execution.json`, `independent-execution.json`, `tests.log`, the individual audit/check logs, and `smoke.log`. The independent smoke measurements are retained as `smoke-benchmarks.json`; they do not replace any published timing.

## Manuscript and scope preservation

My comparison with accepted Stage 2 finds changes only in `main.tex` and `sections/08-computation.tex`. All 66 formal theorem/lemma/proposition/corollary/proof environments are unchanged. The metadata change supplies anonymous descriptive PDF metadata and suppresses variable identifiers. The computation edits remove dependence on omitted development history while retaining the loss to elementary LP baselines, synthetic/shared-host qualifications, exact-versus-numerical distinctions, and the component-hull meaning of additional side constraints.

The new reproduction instructions correctly separate a fresh benchmark run from regeneration of the published tables. They state the extracted working directory and required layout, preserve canonical measurements, and direct fresh output to a separate file. The source archive includes every manuscript input, so the paper can be built without any computational package. I visually inspected rendered page 47 containing the reproduction commands; its commands and prose are legible and fit the page. The corresponding image is retained as `reproduction-47.png`.

## Limitations

- I used the already installed matching Python dependencies and TeX toolchain; I did not test fresh dependency installation from an external package index or a different operating system. The documentation does not promise cross-toolchain PDF or ZIP identity.
- I ran the documented meaningful smoke benchmark, not a second complete five-repetition timing study. I did not treat the author's or root's full-study claims as my own execution. Canonical table regeneration and the complete listed test/check commands were executed independently.
- Anonymous metadata and payload scans are not a guarantee against every possible inference of authorship from research content. They found no concrete identifying disclosure.
- I checked the altered exposition, formal-environment preservation, delivered artifacts, package interfaces, and execution closure. This is not a new proof audit of all unchanged mathematics or an exhaustive software-correctness proof.
- Visual inspection was targeted to the reproduction page, not every rendered page. Both builds' diagnostic logs are clean.

## Optional preferences

None. No additional packaging or exposition change is needed for acceptance from this review.

**Final verdict: accept Stage 3, with no major or minor findings.**
