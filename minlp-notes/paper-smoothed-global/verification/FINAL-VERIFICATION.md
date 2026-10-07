# Targeted manuscript verification

The final anonymous manuscript has 182 pages, seven proof appendices and
47 references. This report concerns this paper only. No optimization
experiment, project-wide verification or CI inspection was performed.

## Frozen sources and independent reviews

The final source snapshot is `evidence/snapshots/submission-addendum-r2/`.
Its manifest SHA256 is `0f1ff4db085a5d732b4e476309deafd2a2793225103a7a0773ae3ae84c2c2d94`.
All 21 source entries match the live files and extracted submission archive.
The snapshot's creation-time status is preserved; subsequent review closure
is recorded here and in `evidence/STATUS.md`.

The predecessor R4 release is preserved in
`evidence/release-history/final-submission-r4/`. Nine source files changed
from R4 to addendum R1. The changes include companion attribution, an
explicit row-scaled lattice law, a corrected original-domain regret bound
and the affine-margin proof repair. The other 137 proof blocks, all 410
labels, all 249 displayed equations and the bibliography remain unchanged.
From R1 to final R2, only two introduction clauses changed. All 329
mathematical blocks, including 138 proofs, remain byte-identical to R1.
The source comparisons are `addendum-source-comparison.json` and
`addendum-r2-source-comparison.json`; the exact diffs are in `evidence/`.

Earlier complete specialist Sol reviews and focused follow-up reviews keep
their actual target snapshots and limits. The changed arguments were
independently reviewed against the actual repaired source. Final Opus R1
passes the addendum; fresh Opus R2 passes the two final prose refinements
and verifies unchanged content by identity. Sol's final report independently
checks the mathematical repairs, attribution, source identity and final PDF,
including an explicit R2 follow-up. Both final reports give scoped PASS,
with no remaining defect or requested repair in their stated scopes. These
are not guarantees of absolute priority or journal acceptance.

| Final review receipt | SHA256 |
| --- | --- |
| `evidence/reviews/post-addendum-final-opus-r2.md` | `47bbe6f0c0f7680c5d22210b71674298d4001dc6c3ea8d9681757c62d284f763` |
| `evidence/reviews/post-addendum-final-sol-r1.md` | `13a843695242da1f92f4a793d4ff6ab6ce4c8376cea76d4342c63b2cd8a15530` |
| `evidence/reviews/late-opus-math-disposition-sol-r1.md` | `abede7bbdc92c0ad83694fed7102ecbd56ea1acccf65f75f824f356707740e91` |

The final coverage index links all 69 inventory entries to current source
labels. This is a coverage count, not a claim of 69 original results.

## Commands and observed results

These targeted commands were actually run from this paper directory:

```sh
python3 verification/check_sources.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
pdftotext -layout main.pdf verification/main-final.txt
pdfinfo main.pdf
```

The source checker passed: 20 TeX files, 410 labels and 47 cited entries.
The 47 distinct bibliography keys exactly match the cited set. There is no
missing input, undefined label or citation, unpaired environment, unfinished
marker or external manuscript-source dependency. The final live build
exited 0; its transcript is `build-submission-addendum-r2.stdout`.
The final TeX log has no error, warning, overfull box or unresolved reference.
A few cosmetic underfull-hbox notes occur in tables and the bibliography.
BibTeX has exactly three expected sorting warnings for anonymous, undated
companion manuscripts, whose citations and displayed titles resolve.

The 23-file ZIP was freshly extracted into
`/tmp/smoothed-submission-addendum-r2-_foxylb7/smoothed-exact-global-optimization`.
The following commands were run there:

```sh
python3 /workspace/minlp-notes/paper-smoothed-global/verification/check_sources.py .
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
pdftotext -layout main.pdf main.txt
```

The extracted source check and build passed; the build exited 0. Its
transcript is `build-submission-archive-addendum-r2.stdout`. All 21 TeX/Bib
hashes match the final manifest. The generated bibliography bytes and the
complete extracted PDF text match the live build byte for byte. Its logs
have the same three BibTeX warnings and no TeX error, warning, overfull box
or unresolved reference. ZIP integrity passed. Its 23 files comprise the
21 sources, `main.bbl` and portable `README.txt`; review records,
experiments and unrelated papers are excluded.

Targeted inline Python checks with `pathlib`, `json`, `hashlib`, `re` and
`zipfile` verified the source, archive, artifact, log and text comparisons.
Their outcomes are in `final-delivery-check.json`. These checks do not
substitute for proof review.

## PDF inspection and delivered artifacts

Root inspected addendum R1 pages 11, 14, 70, 73 and 169, then final R2
pages 11 and 12 using `pdftoppm` and the image viewer. Sol independently
inspected 17 affected R1 pages and final R2 pages 11–12; Opus checked the
changed R2 page. Verified unchanged source content supports transfer of the
remaining R1 review, rather than a claim that every R2 page was visually
inspected. No clipping or unresolved reference was found on inspected pages.
Sol confirmed that all 1,505 internal links resolve; external link targets
were not rechecked by that reviewer. Full PDF text has no unresolved markers.
The PDF has an empty author field and letter-size pages.

| Delivered artifact | SHA256 |
| --- | --- |
| `main.pdf` | `72dfac22092c60dcebd8f0b081b6baa27d37e35fde0a113e107b9437b2659e9b` |
| `delivery/smoothed-exact-global-optimization-source.zip` | `eb8c179a665ac172a7b8cdfdf62b9a8e5f0c8fcc1cd17b1d3adfc333fe632b94` |
| `main.bbl` | `fbd704008f1e818a739eafc91d262a2c93fbfacc6d0a517f1ef14e6fa2667eac` |

## Literature handoff

All literature research was assigned to Luna at maximum reasoning. The
unchanged main audit, `evidence/literature-audit.md`, has SHA256
`24761a995eaf1ff4de06135b4b479874731a176d483025489846b37609ac622a`.
Its source-access qualifications and historical target remain explicit.
The archived run is
`literature/runs/2026-10-06-smoothed-global-literature-audit/run.md` at the
repository root. Four formal discovery rounds ended in an empty follow-up;
two later batches closed source contracts and intake. Metadata-only and
unread records are not claimed as read theorem support.

The sole serialized owner previously ran:

```sh
/workspace/local-home/repo/skills/literature/scripts/lit.py check /workspace/minlp-notes/literature
```

Its recorded result was `KB_CHECK=ok`, `UNREAD=212`, `READ_UNCITED=749`.
The counters are global KB counts. Three pre-existing thesis preview warnings
are recorded in that run. Root did not duplicate this operation.

The late local-companion audit is
`evidence/companion-overlap-addendum-luna.md`, SHA256
`fbd34b464a1b4f3272fa667498510bc1e6aadb8c64786c963f53eaa64ce01d5a`.
Its dated follow-up supersedes the initial family-B statement: the paper's
positive-definite example is exactly the companion's second family at mesh
1/4. The manuscript directly credits both star families and the inherited
deterministic tools. The addendum needed no new citation key, source intake
or KB mutation. Subsequent intake for other authorized papers is separate
and remains under the shared serialized owner.
