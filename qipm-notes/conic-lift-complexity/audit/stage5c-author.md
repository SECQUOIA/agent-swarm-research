# Stage 5C author integration

Date: 2026-09-20. Status: authored and frozen for five independent Stage 5C
reviews. This record does not close that cycle or the separate mandatory
five-reviewer whole-manuscript cycle. No reviewer was dispatched by this author.

## Authored changes

- Replaced the Stage 1 abstract with a full-paper abstract in `main.tex`.
  It identifies the symmetric dictionary and s≥2 rank scope, fixed unit tree
  objective, feasible PSD allocation hypothesis, remaining intervals, and
  conditional computational conclusions.
- Added `sections/00-introduction.tex`: principal results with exact model
  qualifications, three displayed headline formulas, seven-row model table,
  primary-literature comparison, explicit qualified novelty statement,
  notation/convention guide, and six-part roadmap.
- Consolidated the old 56-line introduction and literature sketch into that
  introduction. `01-foundations.tex` now starts with “Exact lifts and local
  conventions”; all subsequent definitions, proofs, statements and labels
  are retained. All other previously reviewed mathematical section files
  are unchanged by this stage.
- Organized the existing proof order into six thematic parts, with linked
  contents through subsections. Retained all four appendices and added a
  contents entry for references. There are 32 main sections, four appendices,
  and 35 section source files (the foundations file contains two sections).
- Added `sections/13-synthesis.tex`, distinguishing exact formulas from
  intervals and integer lower ledgers, summarizing the weighted tree and
  feasible quotient results, and retaining the access/output boundaries.
- Added title, subject, and keywords to PDF metadata. The author field and
  date remain intentionally empty for anonymous review.
- Rewrote `README.md` around the actual complete draft, source files,
  reproducible qipm build, anonymous metadata, audit roles, and pending
  review cycles. It makes no claim of journal acceptance.

The support-fiber minimax is explicitly selection-free; product certificate
existence is not relabeled as a minimum aggregate-fiber rank theorem.
Global selection, fixed-domain intrinsic barrier optimization, and a
displayed metric each retain their distinct scopes. The bounded narrow-cap
interval `eq:unsettled-range` and nonsymmetric intervals are explicitly
unresolved. The headline tree formula fixes a unit objective and the target
gap; the PSD transfer fixes the projected point and exact feasible source
allocations. The notation guide permits paths in the stated metric domain,
so it does not impose unstated affine constraints on intermediate
primal–dual paths. Root's author-stage precision comments were incorporated
before freezing; these comments were not a formal review round.

## Literature verification and helper inspection

Two bounded helper authors were used, as authorized. Neither acted as a
formal reviewer. Both finished before this freeze; their complete reports
and edits were inspected.

`stage5c-literature-helper.md` records independent primary-source metadata
checks for Scheiderer 2025, the Fawzi–Gouveia–Parrilo–Saunderson–Thomas 2022
survey, Averkov 2019, Saunderson 2020, Kummer 2016, Hildebrand 2022,
Cardoso–Vieira 2006, and Mohammadisiahroudi et al. 2026. All eight entries
are cited in the introduction. The verified ENS-hosted original Adams scan
replaces the incorrect course-notes URL. The full root preparation and
literature audits were read, including their original-text theorem checks
and the superseding dynamic-source disposition.

The introduction distinguishes SOC existence from factor/rank frontiers,
neighborliness and extension degree from local contact curvature, direct
LMIs from projected lifts, and ambient optimality from exact restrictions.
It attributes Jordan and topological tools, norm trees, self-concordant
barriers, NT/NN metric geometry, query primitives, and sparse elimination.
The unpublished central-path companion is named and compared explicitly;
its shared results remain proved here. The 2026 iterative-refinement
comparison avoids an outdated universal inverse-accuracy claim. The new
claims are qualified at the exact invariant/formulation level; negative
literature search is not offered as priority evidence.

## Coverage and packaging

The source-ledger helper replaced the stale controlling status with a final
routing map while retaining the historical plan and every authored stage
appendix. Its independent before/after check preserved the 42,637-byte
appendix suffix exactly; the hash is in `stage5c-ledger-helper.md`.
The final source partition is 136 included, six comparator-only, 56 excluded,
and three navigation notes. This is inventory classification, not a count
of new theorems. The helper report lists every comparator-only and excluded
source and the ledger retains their complete paths and titles.

The dynamic PSD source is explicitly included in full through
`newt:dynamic-scale`, `newt:scale-service`, and `newt:fixed-scale`; its fresh
batches are not identified with a fixed optimization trajectory. The
relative-entropy compiler and direct-ball comparator promotions are also
explicit. The author independently repeated the inventory and link checks:
all 201 current workbench paths appear exactly once, no current or stale
path is missing, and all 204 local ledger links resolve.

Removed unused `scripts/map_sources.py` without executing it. Its initial
overwrite behavior could erase the authored ledger appendices; neither the
build nor any proof uses it. The manuscript build has no workbench,
literature-archive, companion-file, network, or Python dependency. No package
was installed. Existing user work outside this manuscript folder was not
modified.

## Build, references and rendered checks

Executed `conda run -n qipm --live-stream make clean`, then
`conda run -n qipm --live-stream make`, after the final manuscript edits.
The clean build succeeds: **183 PDF pages**, with no LaTeX warnings,
undefined references or citations, duplicate labels, or overfull/underfull
boxes. BibTeX reports 87 entries and zero warnings. Build and clean records
are `stage5c-build.log` and `stage5c-clean.log`; the final `main.log` and
`main.blg` give the TeX/BibTeX checks.

A separate source scan found 499 unique labels, no missing references,
87 unique bibliography keys, no missing or unused citations, and no
scientific TODO/TBD/FIXME/placeholder text. Its output and the repeated
ledger verification are in `stage5c-validation.json`.

Used installed `pdfinfo`, `pdftotext`, and `pdftoppm` to check the PDF.
Visually inspected the final title/abstract (page 1), contents (page 2),
main-results table (page 9), notation table and roadmap (page 11), weighted
tree theorem/proof (page 123), and feasible quotient theorem/proof
(page 135). These pages have readable text, resolved links, and unclipped
math and tables. Representative renders are `stage5c-front-*.png`,
`stage5c-guide-*.png`, `stage5c-tree-123.png`, and
`stage5c-quotient-135.png`; `stage5c-rendered.txt` is the extracted final PDF.
`pdfinfo` confirms the correct title/keywords and empty author metadata.
An initial optional attempt to use PyMuPDF found it unavailable; no
installation was attempted, and the installed Poppler tools completed the
rendered checks.

No new mathematical theorem or unreviewed proof replacement was introduced
in this integration stage. The entire authored stage is now frozen for the
root's five independent reviews, before assessment, a separate fixer if
needed, and the later separate full-manuscript review cycle.
