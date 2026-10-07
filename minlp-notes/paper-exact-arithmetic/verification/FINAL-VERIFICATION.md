# Final manuscript verification

Snapshot: 2026-10-05 22:31 UTC. All manuscript, literature, internal review,
coverage, PDF layout and standalone package gates are closed. The anonymous
manuscript and its source archive are complete. No unresolved mathematical
objection remains in the completed review scopes.

## Deliverable and scope

The anonymous manuscript is *Exact Arithmetic in Polynomial Optimization:
Values, Optimizers, and Certificates*. It includes all 97 developments in the
repository inventory, together with the additional arguments needed to make
their statements and proofs complete. The source-to-result and proof map is
in `evidence/final-coverage.md`. All 97 entries are marked covered; none is
silently excluded. The paper has an abstract, introduction and related work,
explicit computational models, connected thematic chapters, full proofs in
Appendices A–L, and a discussion of uses and remaining research questions.

The manuscript does not depend on the repository notes, historical scripts,
or external data. Its bibliography contains 126 records and 120 cited works.
It has no author, affiliation or identifying PDF author metadata. The
standalone source package is specified in
`evidence/reviews/submission-package-r1.md` and `BUILD.txt`.

## Mathematical and editorial review

All eleven original main writing assignments used Opus. Separate Sol agents
reviewed the principal theorem families. Revisions received fresh bounded
reviews where the mathematics or its contract changed. The completed Opus
numerical review and the independent Sol numerical revision review passed.
When Claude rate limits stopped four late tasks, the user's authorized Sol
fallback completed the remaining writing scopes. After the user reported the
limits reset, a fresh Opus whole-paper review was completed. It found no
mathematical blocker and requested four presentation repairs. The abstract
now fixes both cone parameters; unsupported finite rank diagnostic references
were removed; the quartic recourse implication has a clear antecedent; and
the introduction explains the relation to unrestricted SOCP hardness. A
fresh Sol review and the completed Opus R3 pass those edits. R3 also
closed the height–Mahler source-record correction. Its remaining version-note
and title-case findings were repaired and passed the final Sol bibliography
recheck. All 27 TeX sources match the accepted R3 snapshot; only bibliography
metadata and title protection changed afterward. A failed review is not
counted as a completed review.

Completed internal review records include:

- `upper-r1.md`, `reductions-r2.md`, `heights-r2.md`;
- `points-constraints-r2.md`, `algebraic-r2.md`, `fields-r2.md`;
- `recourse-r2.md`, `contrast-r2.md`;
- `opus-numerical-r1.md`, `numerical-r2.md`;
- `nonconvex-r1.md`, `cones-r2.md`;
- `integration-r2.md`, `readability-r1.md`;
- `opus-wholepaper-r2.md`, `opus-final-scope-r3.md`;
- `final-scope-sol-r1.md`, `final-bibliography-r1.md`;
- `submission-package-r1.md`.

These reports are in `evidence/reviews/`. They distinguish the exact reviewed
scope and source snapshot from later document changes. Source-family reviews
and integration/readability reviews pass their scopes. They are internal
reviews, separate from journal peer review.

The large printed finite certificates were inspected and spot-checked
analytically. This task did not run a complete computer verification of
their matrix entries or minors. The review reports state their exact scope;
document checks are not substituted for mathematical verification.

Material development and repair included the rational radial SOS existence
proof; the fixed-selector and objective-gap interfaces; exact box-QP
admissibility and pivot arguments; ordered-limit/common-field proofs for
nonconvex finite infima and attained optimizers; and the algebraic-cone
projection, gap, rounding and witness arguments. Reviews corrected
representation charges, dimension ranges, zero-dimensional and empty cases,
certificate fields, source hypotheses, and summary scopes.

In particular, two preliminary transcriptions of the classical
Khachiyan–Porkolab witness bound were rejected analytically. The actual cone
proof was repaired to use fixed-block quantifier elimination first and only
the quantifier-free witness bound afterward. Fresh cone and interface reviews
passed the revised argument. No remaining theorem uses either rejected
transcription.

Research questions printed in the discussion are outside the proved claims.
Historical rank diagnostics are outside the proof dependencies; references
to unpublished finite rank computations were removed. Equality upper bounds
are distinguished from order-test hardness; expanded-output lower bounds are distinguished from bounds for
implicit representations and from unconditional computational hardness.

## Literature and novelty

Literature research and local literature additions used GPT Luna at max
reasoning with the local `$lit` workflow. The review record is
`evidence/literature-review.md`. It records theorem-level primary-source
contracts, version-specific comparisons, contribution boundaries, access
limits and local additions. The manuscript credits established optimization,
real-algebraic, circuit, integer, intersection-theoretic and SOS methods.
It does not claim broad priority for those methods or rely on a failed search
as evidence that a result is new.

Hesse comparisons use the inspected arXiv version 1. The 2026 proceedings
publication has separate metadata; its unretrieved text is not silently
equated with that version. The published Luo–Zhang metadata is distinguished
from the inspected 1997 report containing the required attainment corollary.
Other access limits and qualified comparisons are recorded in the literature
report. Final critical source-contract checks passed. The last source-only
repairs narrowed Cayley–Bacharach attribution to CB7, replaced unread specific
Harris book locators by the inspected Eisenbud–Harris 1987 classification and
ideal-generation statements, and removed a redundant exact Heintz locator.
The retained KPS source plus the printed componentwise projection argument
supplies the affine degree step. These changes preserve the mathematical
statements and proofs. OCR failures for original scans are distinguished from
primary page-image inspection. Bibliography rendering preserves the volume
part and proper names.

The final report consolidates the previously checked Grigoriev–Pasechnik
component-sampling and Dedieu–Malajovich–Shub isolated-root contracts.
Bombieri–Gubler is used for height conventions and the standard height–Mahler
identity. The final source row derives that identity from primitive-polynomial
Gauss norms and the product formula, while stating that the full textbook
chapter was not inspected. The quantitative height inequalities used later
are proved in Appendix J, and L's coefficient bound follows by expansion
over conjugates. Standard textbook imports and metadata-only or unretrieved
source text are identified explicitly.

The GP and DMS bibliography entries now print version notes for the inspected
preprints cs/0403008v3 and math/0312083v2 (19 July 2004). Their journal
publication metadata is retained; the two journal full texts are explicitly
listed as uninspected. The report has 13 identified in-scope access gaps,
separate from its textbook access notes. Protected numerals, proper names
and acronyms print correctly after the final bibliography-only recheck.

## Targeted commands actually run

Commands below were run from `paper-exact-arithmetic/` unless stated
otherwise. Builds were repeated only after actual manuscript or bibliography
changes. Early incomplete-draft diagnostics failed on then-missing sources,
labels or bibliography entries; those failures were resolved and are recorded
in `evidence/INTEGRATION.md`.

| Command or check | Actual result |
|---|---|
| `python verification/check_manuscript.py` | Pass: 27 TeX source files, 658 labels, 1768 cross-references, 120 cited works, zero errors. Checks source closure, labels, references, citation keys, unfinished text and repository-dependent paths; it is not a mathematical proof checker. |
| `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` | Pass after all source and bibliography changes: 322 pages. |
| `rg -n 'Warning\|Overfull\|Underfull\|undefined\|multiply defined' main.log main.blg` | No matches in the accepted typography build; exit code 1 means the search found no diagnostics. |
| `pdfinfo main.pdf` | Intended title, empty Author field, 322 pages, unencrypted PDF, no forms or JavaScript. |
| `pdftoppm -f N -l N -scale-to 1400 -png main.pdf ...`, followed by image inspection | Title, contents, result tables, large certificate matrices and minors, cone-proof pages and bibliography fit within margins and are legible. The changed final contents pages were checked again. After the final scope repairs, pages 1, 9, 13 and 101 were rendered at scale 1600 or 1200 and checked visually. Bibliography pages 316, 317, 319 and 321 were inspected after the version and capitalization repairs; the final accented-name page was checked again. |
| `pdftotext -layout main.pdf ...` | Used to locate the actual table/matrix/bibliography pages for visual inspection. |
| Targeted `rg`, `sed`, `nl`, source-hash and inclusion inspections | Supplied exact proof/source locators, reviewed snapshots and package closure. These were document inspections, not rerun mathematical experiments. |
| `sha256sum -c verification/SHA256SUMS`, invoked through a document-only Python wrapper | Pass: all 32 accepted source, PDF and archive files match the manifest. |
| `git status --short`, from the repository root | Only the new `paper-exact-arithmetic/` directory appears as changed/untracked at this snapshot. |

Authors also ran isolated chapter document builds. Those are identified in
their authoring reports; they are not counted as the root's full-manuscript
builds or as rerun mathematical experiments.

No computational experiments, historical mathematical scripts, CAS runs,
project-wide checks or CI checks were run. No journal submission, commit,
pull request or external message was made.

## Final archive and snapshot

`submission-source.zip` contains exactly 30 files: the 27 TeX files,
`references.bib`, `main.bbl` and `BUILD.txt`. Archive CRC checks, equality of
all archived bytes to the current source files, and included-source closure
passed. Internal evidence and verification records are excluded.

The archive was extracted to `/tmp/exact-paper-final-submission-cot9h0vp`.
The following targeted clean-package commands actually ran there:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
rg -n 'Warning|Overfull|Underfull|undefined|multiply defined' main.log main.blg
pdfinfo main.pdf
pdftotext -layout main.pdf /tmp/exact-paper-final-submission-layout.txt
```

The build passed with 322 pages; the diagnostic search found no matches; the
PDF author metadata remained empty. The final repository PDF was likewise
extracted with `pdftotext -layout`, and
`cmp /tmp/exact-paper-accepted-layout.txt /tmp/exact-paper-final-submission-layout.txt`
passed. Thus the clean archive build has identical extracted typeset text,
including pagination, to the current repository PDF. An initial comparison
used a text extraction made before the last bibliography capitalization
repair; regenerating the current repository extraction resolved that stale
comparison. It was not a source/package mismatch.

The clean-package check was refreshed after all four Opus R2 presentation
repairs, the earlier tilted-instance clarification and every final
bibliography version/capitalization repair. The refreshed archive
again passes integrity and byte-equality checks; its fresh build passes
with 322 pages and no warnings; extracted PDF text again matches the
repository build. These repairs change no theorem or proof.

A failed earlier Opus round later produced an interim working file through
automatic postterminal callbacks. That file is not a completed review. Root
checked its seven precision findings against the final source, made the
abstract clarification above, and stopped its later duplicate run. The
distinct fresh whole-paper R2 and bounded final R3 were completed. R3
passes the four presentation repairs; its bibliography-only findings passed
the separate final Sol recheck after repair.

Final accepted file hashes are in `verification/SHA256SUMS`: 30 packaged
files, the PDF and the archive. The manifest integrity check passes for all
32 files. Key reviewed snapshots are:

- Opus R3 report: `b186fe9caa83d2927827e217ea9506178b5a4e90f30b9a700592577fed582350`.
- Final Sol bibliography report: `f42975dbb49f79348dd6157e5a2ab9555988ed1d796fe12497c961ee07f1dc46`.
- Final literature report: `30b015fcfcef4e216d5fca14250dc9c298b43f4acc2950ff6677b212bd92b28b`.

All review findings are closed in their recorded scopes. The final package
is self-contained and anonymous. It has not been submitted to a journal.
