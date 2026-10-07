# Targeted manuscript verification

This record concerns this paper and its portable packages. No project-wide
verification was run, CI was not inspected, and no computational experiment
or solver run was repeated.

## Integrated source and build checks

Commands actually run from `paper-bb-complexity`:

```sh
python3 verification/check_sources.py --json delivery/source-check.json
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex > delivery/build.log 2>&1
pdftotext -layout main.pdf delivery/manuscript-text.txt
pdfinfo main.pdf
python3 verification/package_sources.py
```

The integrated build passes and produces a 125-page PDF. The source check
passes with 28 reachable files, 432 labels, and 57 citation uses. The final log has no undefined references, undefined citations,
errors, or overfull boxes. Three underfull boxes occur in narrow table
columns; the inspected pages remain readable.

Initial build failures exposed an unused `algorithm` package dependency,
an incompatible `split` display with multiple alignment pairs, array rows
whose initial brackets were parsed as optional spacing, and an unbraced
operator inside a square root. These were corrected. The two remaining
overfull boxes were removed by changing display breaks; independent
reviewers checked that their mathematics was unchanged and refreshed the
reviewed file hashes.

The source checker originally mistook mathematical sets such as
`x:\nabla\phi(x)>0` for Windows paths. Text scanning now recognizes private
home-directory paths and file URIs, while dependency arguments separately
reject all absolute drive paths. A targeted temporary fixture passed six
mathematical expressions, six private paths, and two absolute dependencies.
Static checks do not replace compilation or manual review.

## PDF inspection

The following page-render command was run for pages
1, 6, 20, 26, 32, 58, 63, 66, 90, and 124:

```sh
pdftoppm -f PAGE -l PAGE -r 110 -singlefile -png main.pdf delivery/preview-page-PAGE
```

Page 64, containing the full figure and caption, was rendered at 130 dpi.
Root and the independent editorial reviewer inspected these images. The
selected pages include the title and abstract, theorem statements, tables,
the figure, long proof displays, and bibliography. No clipping, collisions,
or unreadable labels were found. Bibliography pages 124 and 125 were
rendered again after the final proper-name protection. The independent
editorial reviewer confirmed readable layout and correct capitalization.

## Reviewed source versions

All 22 chapter, proof, table, and figure hash rows in the seven accepted
mathematical and empirical review reports match the saved files. The
read-only reconciliation is recorded in
[review-hash-check.json](../delivery/review-hash-check.json). The six other
reachable files (entry point, macros, bibliography, abstract, introduction,
and discussion) belong to integrated editorial and literature review.

[source-freeze.json](../delivery/source-freeze.json) records the SHA256 hashes
of all 29 local submission inputs, including `BUILD.txt`, at
2026-10-06T04:25:39.101419+00:00.

## Portable submission sources

The current source archive has 31 members: 29 local submission inputs,
`dependencies.json`, and `SHA256SUMS`. A Python standard-library `ZipFile`
extraction into `/tmp/bb-complexity-source-check-v092o6fy` preceded these
commands, actually run from that clean directory:

```sh
sha256sum --quiet -c SHA256SUMS
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
pdfinfo main.pdf
pdftotext -layout main.pdf clean-manuscript-text.txt
```

All 30 manifest hashes passed. All 29 extracted submission inputs match the
local frozen inputs. The clean build passed, produced 125 pages, and had no
errors, undefined references or citations, or overfull boxes. Its three
underfull table cells are the same harmless warnings seen locally. Extracted
PDF text matches the local PDF text byte for byte. PDF file hashes differ
because separate builds contain their own timestamps and PDF identifiers;
no byte-identical PDF-build claim is made.

The source ZIP SHA256 is
`ecddcd206310a509f7a90de158f193e00386bad1f1cf841c2782e74b3baded6d`.
[source-package-check.json](../delivery/source-package-check.json) records
checks, commands, hashes, and the actual clean build directory. The package
contains no internal reviews, computational outputs, or downloaded
literature. It builds without the research notes, repository, network
access, or solver software.

An earlier portable build also passed. The check was repeated after the
bibliography's capitalization, unused-entry changes, and final prior-work
attribution corrections so that the tested archive matches the final source
snapshot. The attribution corrections changed no mathematical statement or
proof and passed independent narrow review.

## Evidence archive

The evidence ZIP was extracted into a fresh temporary directory and its
read-only `verify_archive.py` executed there. All 218 manifest entries
matched; the retained computational records and fit groups reconciled. The
ZIP has 219 members and preserves 209 original files byte for byte.
[evidence-package-check.json](../delivery/evidence-package-check.json)
records the actual archive hash and verification results.

## Final manuscript reviews

All selected mathematical and empirical chapters passed independent review.
The integrated editorial review also passes for the final frozen source
manifest and PDF; all eleven concrete editorial findings are resolved.
The final source review includes the repaired prior-work passages and sampled
PDF pages 9, 33, and 43. The editorial report distinguishes its own source
and visual inspection from root's actual build commands.

The final read-only Luna literature audit passes for the manuscript's bounded
claims. All 32 unique citation keys occur in the bibliography and claim map.
Fourteen source-content/access gaps are stated explicitly and limited or
excluded; the audit makes no universal priority or exhaustive-search claim.
The final ledger SHA256 is
`028cc65ed65d141c5b71f03591b51cc99cbc1616f02976f0cbcb7c6ccbc3afe8`;
the corrected key-map SHA256 is
`41878dcb04073dbd87d230bb58ffe6547d34699fdc9e574ef62fd1d345c48b6e`.

## Shared literature workflow closure

The user directed all shared KB mutations and checks through the reusable
Luna lead under the smoothed-paper parent. BB ceased those operations on
receipt of the coordination notice. Its historical pre-notice check passed
with `UNREAD=171` and `READ_UNCITED=752`.

The shared owner archived all three completed BB discovery rounds intact in
`literature/runs/2026-10-06-bb-complexity-literature/`, including a `run.md`
account. At 2026-10-06 04:43 UTC, after binary-separation released ownership
and the first two serialized sparse-SOS batches completed, the shared owner
ran:

```sh
/workspace/local-home/repo/skills/literature/scripts/lit.py check /workspace/minlp-notes/literature
```

It exited 0 with `KB_CHECK=ok`, `UNREAD=213`, and `READ_UNCITED=752`.
This check covers the already-ingested BB records. Three unrelated existing
short-preview warnings are documented in
[KB-HANDOFF.md](KB-HANDOFF.md); there is no BB-specific issue or pending
source addition. No independent BB KB check was resumed.

## Delivery

A final read-only delivery guard compared all 29 frozen submission inputs and
all three delivery artifacts with their recorded SHA256 hashes; every match
passed. [release-check.json](../delivery/release-check.json) records the
actual comparison. It also records hashes of the two initially modified
tracked files. The repository README changed during concurrent work outside
this task; this task did not edit or restore it. The adaptive-OBBT README
still matches the initial baseline.

The PDF, standalone source ZIP, and portable computational-evidence ZIP are
complete. [ARTIFACTS.json](../delivery/ARTIFACTS.json) records their final byte
sizes and SHA256 hashes. The final claim/proof and issue ledgers are
[COVERAGE-FINAL.md](COVERAGE-FINAL.md) and
[REVIEW-RESOLUTION.md](REVIEW-RESOLUTION.md). No selected manuscript claim or
submission check remains unresolved. These records do not claim exhaustive
publication priority, journal acceptance, or a CI result.
