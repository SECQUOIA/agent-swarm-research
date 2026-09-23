# Stage 6 author report: integration and standalone package

The integrated scientific manuscript is complete at this author stage. It is
ready for the required five independent integration reviews, followed later by
the separate whole-manuscript review gate. Those review gates are not claimed
complete here. No new theorem, empirical value, or unqualified priority claim
was introduced during synthesis.

## Manuscript integration

- Added `sections/00-introduction.tex`: standalone abstract and keywords;
  measurement/resource-allocation motivation; selected-covariance and certificate
  target; concise synthesis of correlated-design, locality, and approximation
  predecessors; a readable five-row contribution-comparison table; a theorem and
  assumptions roadmap. The abstract explicitly restricts spectral covers to
  additive rational PSD atoms, explicit acyclic graphs and rationally represented
  matroids. FPTAS and PSD are expanded on first introduction use.
- Added `sections/06-discussion.tex`: interpretation of the source reanalysis;
  distinct continuous optimization, locality, arithmetic and mixture gaps;
  practical significance and exact limits of all-split separation; nested-anchor
  strength/cost tradeoff; full-packet and physical-grid negative evidence;
  finite-scenario and local-information scope; scientific conclusion; accompanying
  data/code availability without an invented permanent public URL.
- Updated `main.tex` to include the two sections and an anonymous author block.
  No authorship, affiliation, funding, or publication metadata was invented.
- All five accepted technical sections, all four appendix files, `macros.tex`,
  and `references.bib` remain byte-identical to the Stage 5 accepted snapshot.
  No coherence error requiring an accepted proof or numerical change was found.

The novelty statements remain restricted to the combined all-target two-sided
relative PSD cover with exact singular ranges and polynomial accuracy dependence
under the specified explicit representations, and the particular nested
changing-anchor hierarchy. Explicit locality constants and their certified
consequences are developed results, while selected covariance, Kantorovich,
Vecchia, exact noiseless Markov hulls, virtual-noise equivalence, Schur/subsystem
criteria, profile interpolation, and generic mixture/support machinery remain
credited. Matroid atoms are additive only. No computational test is presented
as a large spectral-set FPTAS implementation.

## Documentation and packaging

- Replaced stale Stage 1 `README.md` with the complete deliverable, standalone
  source/build instructions, supplement validation/reproduction guide, source
  provenance, and distinction between scientific attachments and development
  records. Its source instructions need no repository-relative inputs.
- Reconciled `process/coverage.md` to actual final labels and dispositions.
  Removed stale pending-stage and attempted D/A ranking language, linked the
  now-exact rankings, preserved supersession and exclusions, corrected the stale
  RTS-versus-reverse-adjoint summary, and added the integrated package map.
  Live review status remains in root-owned `PROCESS.md`.
- Added the actual Stage 6 source-reading/metadata record to
  `process/literature.md`; inspected primary versions and access limits remain
  explicit. All 57 existing bibliography entries remain cited, so no reference
  additions or speculative metadata updates were needed.
- At root's author-phase request, moved the entire three-file smoke-test directory
  `supplement/results/reproduced/block4/` into
  `verification/stage06/reproduction-smoke-block4/`. A before/after SHA-256 map
  in `verification/stage06/reproduction-smoke-move.json` proves preservation.
  The empty `supplement/results/reproduced/` parent was removed so the documented
  default reproduction destination is initially available. No frozen evidence
  or scientific timing was deleted or relabeled.
- Changed both identical source-kinetics README copies,
  `supplement/source_kinetics/README.md` and
  `verification/stage05-root/source_kinetics/README.md`, to use explicit new
  rerun outputs instead of defaults that overwrite frozen timed records.
  Refreshed only that README's entry in `supplement/archive-manifest.json`.
  The README hash is
  `43c665f016c41a55d4926f3f2cefe3645b85a279e7d03c7783d56ec90e8fa4fe`.
  No producer, checker, frozen numerical array, or certificate changed.

## Verification

Forced complete LaTeX/BibTeX regeneration succeeded with

```sh
latexmk -g -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

The final PDF has **65 pages** (729,504 bytes at this build). The final log
contains no warnings, overfull/underfull boxes, undefined references or citation
errors. The build transcript is `verification/stage06/build.txt`.

`verification/stage06/integration-checks.json` records:

- 57 bibliography entries, all cited, with no missing or duplicate keys;
- 204 unique labels and 209 resolved cross-references;
- no scientific placeholder or stale incomplete-stage wording;
- byte identity of all 11 accepted technical/macro/bibliography files;
- absent default reproduction destinations.

Both supplement manifests were verified after the documentation update:
**159 archived files and 11 new-source files passed**. The smoke-test move and
safe README examples are packaging/documentation changes; broad scientific
reruns were not repeated without a new mathematical or executable change.

Rendered title/abstract, contribution table, introduction-to-foundations
transition, and discussion pages were visually inspected. The table fits the
text width, is readable, and has clean row wrapping. The PDF and extracted text
have no incomplete section flow or unresolved source labels. The visual and
text artifacts are under `verification/stage06/` and are not required by the
scientific source package.

No original tracked repository files, literature package, unrelated paper,
root-owned process tracker, accepted snapshot, or frozen scientific data was
modified. Final distributable ZIP files remain root's responsibility after the
required final review gates.
