# Stage 3 author report

The standalone exposition and anonymous delivery files are prepared for five
independent frozen-stage reviews. This author report does not accept the stage
or the complete revision. No external submission was made.

## Scope and preserved work

Read the Stage 3 brief, current STATUS, Stage 1/2 adjudications, active manuscript
sources and computational instructions, and the supplied global AGENTS.md rules.
The accepted mathematics and qualified prior-work position are preserved.

The manuscript changes are confined to `main.tex` metadata and nonmathematical
prose in `sections/08-computation.tex`. The computation section now describes the
reduced oracle, unreduced comparator, positive-state full LP, one-flow reduction,
and two general compressed formulations directly. It retains all current
quantitative results, negative runtime comparisons, synthetic/shared-host limits,
exact versus numerical distinctions, and the component-hull meaning of side rows.
The old-builder speed comparison and full-length archival-comparison discussion
were removed because they relied on omitted historical data; the current
512-gadget boundary-face loss remains explicit. The reproduction section points
to the accompanying supplement, with separate fresh-measurement and canonical-table
commands. It no longer requires a repository or development chronology.

The reduced inverse-basis sentence explicitly concerns recovery with three
observed labels, avoiding confusion with block cycle rank. No mathematics was
changed. All 66 theorem/lemma/proposition/corollary/proof environments are
byte-identical to accepted Stage 2. Sections 00–07 and 09 and the bibliography are
unchanged. All 31 selected production/verification/data/table input files match
the accepted snapshot. In particular, production code and the canonical raw
benchmark SHA-256 are unchanged. Evidence: `stage3-source.diff`,
`math-preservation.json`, and `production-preservation.json` in the evidence folder.

Active README and PROCESS now identify this revision, its anonymous artifacts,
and the remaining review protocol. September 7 archives, old manifests/reviews,
and unrelated research folders were not changed. The root maintains STATUS and
freeze tooling; this author did not edit those files.

## Delivery

`delivery/submission.pdf` is the current anonymous 50-page paper. The active
`main.pdf` is refreshed to identical bytes. Author/affiliation/date fields are
empty. PDF title, subject, and keywords describe the paper; the author value is
empty, creator is LaTeX, and dates/source-path/trailer identifiers are suppressed.

The two ZIP archives have separate top-level directories and payload manifests:

- `latex-source.zip`: 20 files including its manifest; all manuscript LaTeX,
  bibliography, five table/value files, TikZ figure, and build README.
- `computational-supplement.zip`: 40 files including its manifest; runnable code,
  tests, original independent checks, five selected additional exact checks,
  unreduced flat-chain source, canonical measurements, table generator and tables,
  interface guide, environment requirements, and complete command README.

The supplement preserves `code/` and `paper-network-simplex/verification/` so
imports work without installation. In particular, it includes the comparator
loaded as `network_simplex._stage06_unreduced` and the bounded-rank helper imported
by `stage04-recovery.py`. Package documentation replaces links to omitted research
notes and old archives. The canonical JSON itself is unchanged: its provenance
fields still identify historical measurements; the README explicitly distinguishes
those records from runnable reproduction instructions.

The selected additional checks are copied from the Stage 2 author and independent
review evidence: exact theta/circuit/Fibonacci checks, incidence elimination and
completion, actual Fibonacci facets, all exceptional three-label repairs and the
four-label example, and returned certificate contracts against enumerated integer
flows. Only the certificate check's package import/output paths and its opening
comment were adapted. Original review sources remain unchanged. The package does
not include internal reports, private build logs, unrelated research, external
literature PDFs, or obsolete research archives.

`delivery/build-packages.py` selects inputs explicitly, compiles in an external
temporary directory, writes sorted ZIP entries with fixed times/permissions, and
records SHA-256 input/payload/artifact hashes in `delivery/manifest.json`. It uses
a fixed source date and rejects LaTeX warnings and box diagnostics. Dependencies
for package validation are pinned separately from the historical measurement
versions; neither reproducible timing nor cross-toolchain byte identity is claimed.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `computational-supplement.zip` | 153,482 | `7ca8a25ec3e0f1baa20e91b92d9dd9aae7b0218f020f5f95dc3e5ba5845c01a6` |
| `latex-source.zip` | 80,117 | `ea41c75f1bdf46967f1b5958b8e732c64004f5c1159b3d9714396c8a7f8e4d7d` |
| `submission.pdf` | 613,974 | `21d09299cee1b7f9c6deece832a29aa6d96bb3402bcefdf9ca8e1c7d8aaff816` |

## Actual extraction and build validation

Evidence is under `stage3-author-evidence/`. `validate_extractions.py` extracts
both final archives into a fresh directory under `/tmp`, checks both payload
manifests, runs each documented check, builds the paper there, and records exact
commands, working directories, exit codes, and elapsed times in
`extraction-results.json`. All completed with exit status zero.

The extracted source build command was:

```sh
SOURCE_DATE_EPOCH=946684800 FORCE_SOURCE_DATE=1 latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

It used pdfTeX 1.40.25 / TeX Live 2023 Debian, latexmk 4.83, and BibTeX. The final
50-page log has no undefined references/citations, LaTeX/package warnings, or
underfull/overfull boxes. `clean-main.log`, `clean-main.blg`, `main.fls`, PDF text,
and `pdfinfo.txt` are retained. All explicit LaTeX input/bibliography references
resolve inside the archive. The extracted PDF is byte-identical to
`delivery/submission.pdf`.

The title/abstract page, computational pages and tables, reproduction instructions,
conclusion, and bibliography were visually inspected as rendered pages; a contact
sheet and individual page images are retained. PDF metadata has an empty author
and no creation/modification dates or private identifying paths. Archive text and
PDF text were scanned for private home paths and the workspace owner's identifier;
no matches were found. The manifest scans cover every packaged text input.

`check_final.py` rebuilds to a second external directory and compares all three
deliverables plus manifest.json byte-for-byte. All four match. It also refreshes
and checks active main.pdf, checks all formal environments against accepted Stage
2, and executes the API example from the extracted supplement. See
`determinism.json` and `api-example.json`.

## Actual computational validation

The extracted supplement used Python 3.13.11, NumPy 2.5.1, SciPy 1.18.0, and
SymPy 1.14.0. The package requirements record those library versions. The historical
paper measurements remain Python 3.12.14 / NumPy 2.5.2 / SciPy 1.18.1; no new
measurement replaces a reported value.

- Principal suite: all 23 tests passed. It checks both exact interfaces and the
  strengthened LP baselines, including side rows, zero weights, reconstruction,
  and solver-failure handling.
- Independent flat audit: 192 exact decompositions, 708 exact violated cuts,
  and 233 numerical path-hull comparisons passed. The old signed-subset basis
  helper remains an unreduced-system audit; reduced bases have separate tests.
- General compressed audit: 600 objective comparisons, 758 membership comparisons,
  476 exactly checked Farkas cuts, and six degenerate models passed. Global LP
  support checks are numerical, distinct from rational multiplier checks.
- Integration: exact recovered product ratios 2, 5, and 21 in both initial and
  observed-eliminated formulations.
- All six documented original independent checks passed. The recovery check
  includes a 225-point sharp K4 grid (116 witnesses, 109 negative-support checks);
  profile checks include 216 cases with 116 exact recoveries and 100 rejections;
  padding checks explicitly do not reimplement universality.
- All five selected additional checks passed. They include 1,180 cycle minors,
  1,408 observation/completion sets and 1,484 pivots; 8,360 theta recoveries;
  actual Fibonacci facets at q=3,4 with exact final certificates; all 512 and 27
  exceptional endpoint patterns; and 2,196 certificate queries on 219 models,
  with 17,584 exact vertex-cut checks, 1,117 zero-weight queries, and 498 queries
  with tiny positive weights. Finite tests supplement the proofs.
- The documented extracted benchmark smoke command passed with four flat cases,
  one membership case, and one optimization case, with warmups and one measured
  repetition. It successfully imported and ran the packaged unreduced comparator.
  Its raw data and log are retained as `smoke-benchmarks.json` and
  `benchmark-smoke.log`.
- The table generator passed and reproduced all five canonical table/value files
  byte-for-byte. A post-test manifest check confirms all original payload hashes,
  including the raw JSON hash
  `373ce70b3839c12a206b193e9952d856f585da400f902bda773a725a609f73ac`.

The root independently ran the complete five-repetition study from an isolated
copy of the accepted code: 16 flat, three membership, and three optimization
cases, each with one warmup. Its table generator passed. Comparing 5,754
non-timing leaves with canonical records found no input, side-row, status, count,
model-size, or audit-outcome differences; objectives were compared at absolute
tolerance 1e-7. This is root evidence, not a second full run by the package author:
see `stage3-root-evidence/full-study-validation.json`, full-study.json, and the
associated log. The author's actual extracted-package validation used the
meaningful smoke run above.

## Limits and handoff

No production defect was found and no production code change was needed. No
external submission occurred. The supplement validates exact finite certificates
and numerical comparisons without claiming an exact general LP optimizer, a
computational proof of universality, portable timings, industrial effectiveness,
or an exhaustive proof of software correctness. Deterministic artifacts require
the same source and toolchain; dependency installation uses available packages
and does not recreate the old host.

The author task is complete and reviewable. Five independent Stage 3 reviews and
root adjudication are required next, with a separate correction author for every
accepted finding. The complete manuscript still requires its own five-reviewer
cycle after Stage 3 acceptance.
