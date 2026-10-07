# Targeted manuscript verification

The final anonymous manuscript has 181 pages, including seven proof
appendices and 47 bibliography entries. This report concerns this paper only.
No optimization experiment was rerun, no project-wide verification was run,
and no CI status or logs were inspected.

## Frozen sources and review coverage

The final source snapshot is `evidence/snapshots/final-submission-r4/`.
Its manifest SHA256 is
`0c48e0cda82b7a4f25be956980b536577311fa71d40220cc35c8d1a47d0af061`.
All 20 scientific TeX files are byte-identical to
`final-literature-integrated-r2/`, whose manifest is
`628f762d433e2b4cd82b309b88a1699a0d71bcb22dcc377d8f2963430b342515`.
Only six bibliography fields changed afterward: three optional companion
sort keys were removed, and three missing dates are displayed as `undated`.

The complete mathematical draft was reviewed by five specialist Sol
reviewers. Focused later reviews checked the parameter-envelope accounting,
scalar fiber calculation, rational resultant normalization, shared-root
conversion, new nonsingular-root proof, and explicit component-solver budget.
Their actual target snapshots and scope limits remain in the review reports.
The coverage amendment checks 69 exact-once inventory entries; this is a
coverage count, not a count of original results. The final sources retain all
410 labels and all 138 proof-environment signatures from that amendment.

The final editorial review independently checks the last source and PDF.
Its completed report, `evidence/reviews/final-editorial-sol-r2.md`, passes
the editorial, source-contract and PDF scope, with no unresolved blocker.
The report SHA256 is
`651190d254087c2a970a5903a5fb662ccfd889718e1bf0a65b7d96dc12a14b94`.
Classical and recent source contracts were audited by Luna. See
`evidence/source-audit-dispositions-final.md` for the mathematical changes
and remaining full-text access limits. The final literature audit records
the serialized source intake and KB check. No unavailable text is claimed
to have been read.

## Commands and observed results

Commands below were actually run. Paths are relative to this paper directory
unless an extraction path is given.

```sh
python3 verification/check_sources.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
pdftotext -layout main.pdf verification/main-final.txt
pdfinfo main.pdf
```

The source checker passed: 20 TeX files, 410 labels, and 47 cited entries.
It found no missing input, external source dependency, undefined label or
citation, unpaired environment, unfinished marker, or internal development
path. The 47 bibliography keys are distinct and exactly match the cited set.
The live build exited 0. Its final `main.log` contains no errors, warnings,
overfull boxes, or unresolved citations or references. `main.blg` has exactly
three expected `plainnat` sorting warnings for the anonymous companion
manuscripts, and no other warning. These entries supply their exact titles
and explicitly say they are undated and unpublished.

The final live build transcript is `build-final-submission-r4.stdout`.
Earlier build transcripts are historical and are not final verification
evidence.

The 23-file source ZIP was extracted into
`/tmp/smoothed-submission-r4-48uk9fps/smoothed-exact-global-optimization/`.
The following commands were then run there:

```sh
python3 /workspace/minlp-notes/paper-smoothed-global/verification/check_sources.py .
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
pdftotext -layout main.pdf main.txt
```

The extracted source check and build both passed. All 21 TeX/Bib source
hashes match the final manifest. The extracted PDF text matches the complete
live PDF text byte for byte. The extracted build has the same three known
sorting warnings and no TeX error, warning, overfull box, or unresolved
reference. The build transcript is `build-submission-archive-r4.stdout`.

Targeted inline Python checks using `pathlib`, `json`, `hashlib`, `re`,
`zipfile`, and `subprocess` performed these source, artifact, log, citation,
coverage-catalog and text comparisons. Their recorded outcomes are in
`final-delivery-check.json`; artifact hashes are in
`delivery/artifact-manifest.json`.

## PDF inspection

Root inspected rasterized title, contents, main-results table, the new
Appendix C proof, the explicit Appendix F ledger, and reference pages using
`pdftoppm` and the image viewer. The editorial reviewer independently checked
the final PDF and its internal link targets. The inspected pages are
legible; no clipping or page overflow was found. The corrected anonymous
references show each title once and have ordinary punctuation.

The PDF has an empty author field and no author names or date on its title
page. It is a letter-size pdfLaTeX document. Journal-specific style and author
details can be supplied for the selected venue without changing its content.

| Delivered artifact | SHA256 |
| --- | --- |
| `main.pdf` | `af378038034c845553eefc530d4f73ca6bfc72606e642b5401c7b0bdf84d38c4` |
| `delivery/smoothed-exact-global-optimization-source.zip` | `67203b9d23b6a5b1bd80aa8041541050ce2999e2e8de31135aa6454be6d687fc` |
| `main.bbl` | `fbd704008f1e818a739eafc91d262a2c93fbfacc6d0a517f1ef14e6fa2667eac` |

The source ZIP contains the manuscript, bibliography, generated bibliography
file, and portable build instructions. It excludes research notes, review
records, local paths, experiments, and unrelated papers.

## Literature handoff

Luna's final `evidence/literature-audit.md` was read in full by root and the
editorial reviewer. Its corrected SHA256 is
`24761a995eaf1ff4de06135b4b479874731a176d483025489846b37609ac622a`.
The archived run is
`literature/runs/2026-10-06-smoothed-global-literature-audit/run.md` at the
repository root. Four formal discovery rounds ended in an empty follow-up;
the two later numbered batches performed source closure and intake. They
are not six broad discovery rounds. The run preserves unsuccessful
retrievals, identity conflicts, metadata-only packages and unread supplemental
sources rather than treating them as read theorem support.

The sole serialized owner ran this targeted literature-KB integrity command:

```sh
/workspace/local-home/repo/skills/literature/scripts/lit.py check /workspace/minlp-notes/literature
```

The actual result was `KB_CHECK=ok`, `UNREAD=212`, `READ_UNCITED=749`. These
are global KB counters, not counts for this paper. The three pre-existing
thesis preview/excerpt warnings and their exact records are listed in the
archived run. Mehlhorn's package was reconciled to read before this check.
No main-source KB mutation followed the check; later corrections changed
only audit prose. The main paper's completed handoff does not depend on
subsequent serialized intake for other papers. Root did not duplicate the
owner's KB operation or inspect CI.
