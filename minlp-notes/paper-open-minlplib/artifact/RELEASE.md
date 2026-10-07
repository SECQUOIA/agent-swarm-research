# Release identification

The first section identifies the historical upstream release. The public
repository rebuild is identified separately below.

This file identifies the two PDF files of the release. `check_claims.py`
validates the sources and the evidence (hashes of inputs, code and outputs,
paths and labels); it does not identify the PDF files. The PDFs are identified
only by the SHA-256 hashes below, computed after the final build. This file is
not hashed in `claims.json`, because it is written after the index is
validated.

| field | value |
| --- | --- |
| build date | 2026-10-05, final `make` from an empty `build/` (02:39:25 to 02:39:46, −04:00) |
| `paper-open-minlplib/build/main.pdf`, SHA-256 | `4b183b233cc4d2eded6c7381a7057b9ecf26ca83952c38eb83d2daff43166784` (56 pages) |
| `paper-open-minlplib/build/supplement.pdf`, SHA-256 | `f8547c05fb3135a37e73bb0ea6b9eb5650d33676b93593e4b9dd5831ef8595ab` (131 pages) |
| validator result on the final sources | `PASS: 65 claims; 5632 SHA-256 references; 1918 distinct files; all paths, LaTeX labels, displayed values, status labels and register rows valid` (`logs/check_claims.log`, after the final build) |

## Validation results of this release

Two kinds of check apply, and they establish different things:

- **Source and evidence validation** (`check_claims.py`, standard library only):
  the PASS line above. It recomputes the SHA-256 of every file that the index
  names and checks paths, LaTeX labels, displayed values, status labels per
  instance and the agreement of the claim register (Section S7.3) with
  `RUNS.md`. It establishes packaging consistency, not a mathematical claim, and
  it says nothing about the PDF files.
- **PDF identification:** the two SHA-256 hashes above, and nothing else.

Other checks run on the final sources (2026-10-05, two CPU cores):

- `data/make_tables.py`: 851 checks, 0 failed; `make_campaign_table.py` (115
  checks) and `make_points_table.py` (108 checks) pass all their checks; every
  generated table is reproduced byte for byte, and the figure scripts reproduce
  the figures pixel for pixel.
- The 15 short checks of `run_short_checks.py`, run from a fresh copy of the
  runner on the sources of the previous build of the same day: all pass, with
  every stored field reproduced except elapsed time and CPU affinity. The last
  changes before this build (wording in the paper, `RUNS.md`, `README.md` and
  `build_claims.py`, and the rebuilt `claims.json`) touch none of their
  inputs. The recipe of Section S7.1, whose commands did not change, was
  last run as written on a stand-in archive of the sources of an earlier
  build (`logs/recipe-test.log`, `logs/short-checks.json`); the guarded KAN
  replay commands of `README.md` were tested as recorded in
  `logs/kan-guard-recipe-test.log`.
- The build: no LaTeX error, no undefined or multiply defined reference or
  citation, no overfull box; the only printed placeholders are the four
  `[TODO: …]` items of the declarations (licence, AI-use confirmation, competing
  interests, funding) and four `[archive DOI]`.

To check a copy, run in `paper-open-minlplib/`:

```bash
sha256sum build/main.pdf build/supplement.pdf
```

and compare the output with the table. A rebuild from the same sources need not
give the same bytes (the PDF files contain build dates); the sources are
validated by `check_claims.py` instead.

## Public repository rebuild: 2026-10-06

The PDFs linked from the repository README were compiled from the current
public manuscript sources with `make`. They are provided alongside the sources
as [the paper](../main.pdf) and [the supplement](../supplement.pdf). Keep these
two files together: their cross-document links use these relative file names.

| File | Pages | SHA-256 |
| --- | --- | --- |
| `main.pdf` | 56 | `84debcddd0b878839a9a6475efcd4e6685f8d68aea0d99109faa36f75a0ccf2a` |
| `supplement.pdf` | 131 | `949dd8f369b3731da4114cb5c6598d7c5ffb3c7eadb853981713c1c7294feb08` |

This rebuild has no LaTeX errors, undefined or multiply defined references or
citations, or overfull boxes. The PDF text contains no unresolved `??`
references. Minor underfull-box warnings remain. The four author declaration
TODOs and four archive DOI placeholders are unchanged; these are draft PDFs.
The float checker flags no pages and finds all 31 closure names; visual
inspection of the sideways and long tables found no clipping.
No new scientific replay or external peer review is claimed. The missing-input
caveat and validation scope in [the artifact documentation](README.md#public-export-index)
still apply.

To rebuild and refresh the published copies from `paper-open-minlplib/`:

```sh
make
python3 development/check_floats.py
cp build/main.pdf main.pdf
cp build/supplement.pdf supplement.pdf
sha256sum main.pdf supplement.pdf
```

A rebuild can change PDF bytes because the files contain build dates. Update
the public rebuild hashes above whenever the published copies change.
