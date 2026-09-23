# Stage 2 corrections

Correction agent: `correction_agent`, distinct from the stage author and all
five reviewers. Date: 2026-09-07. Authority:
`process/assessments/stage02-round01.md`. All three accepted issues are fixed;
no accepted issue remains unresolved. Stage acceptance remains the root's
decision.

## Changes and evidence

| Issue | Change | Verification |
| --- | --- | --- |
| S2-1 | Added `GritzmannSturmfels1993` in `references.bib:74–78`. The attribution paragraph at `appendices/a-fixed-core.tex:268–275` cites Algorithm 2.3.6, Theorem 2.3.7, and Corollary 2.3.10 for shared support-direction arrangements and compatible summand vertices. It distinguishes the manuscript's uniform enumeration over the varying core, exact optimization, and common-field reconstruction. | Read the primary extracted text, `[[gritzmann1993-minkowski-addition-of-polytopes-computational]] p.13-14`, and visually checked both original PDF pages, printed pages 258–259. The algorithm enumerates arrangement cells; the theorem's proof selects maximizing summand vertices in each sampled direction; the corollary states polynomial binary complexity in fixed dimension. Checked title, authors, journal, volume, issue, pages, and year against the primary title page and the local package's DOI metadata. No varying-core theorem or reconstruction claim is attributed to that source, and no novelty claim was added. |
| S2-2 | Removed only the redundant author-PDF URL from `AdlerBeling1994` in `references.bib:69–73`; retained all existing metadata and DOI `10.1007/BF01188714`. | The compiled Adler–Beling entry is complete on PDF page 17 and has no split author URL. Its original access remains documented in the stage 2 author and review provenance; that provenance was not changed. |
| S2-3 | Wrapped the short substitution-lemma statement in the standard LaTeX `samepage` environment, `sections/01-foundations.tex:268–283`. | The complete Lemma 1.1 statement now appears on PDF page 5. A byte comparison after removing the two wrapper lines reproduces the accepted foundations source exactly. No mathematical text, proof, package, or hard page break was added or changed. |

I followed `../literature/AGENTS.md` for the primary-source consultation. The
user-supplied Gritzmann–Sturmfels original remains in the literature collection;
temporary page previews were outside the manuscript folder. No literature
package or original was changed or copied into this paper. The direct primary
citation suffices; no optional Fukuda citation was added.

## Build, layout, and source integrity

Before editing, all seven live source files and their frozen counterparts
matched `process/snapshots/stage02-round01/SHA256.json`. Its SHA-256 was and
remains `b4c7f91913054ca4da83eac32ccaae2ac52412e605c468a63278172846d1f849`.
After editing, all frozen file hashes still match. I inspected the complete
diff: the only changes to manifest-listed sources are the citation paragraph,
the bibliography corrections, and the `samepage` wrapper. In particular,
`sections/02-exact-responses.tex`, `main.tex`, `README.md`, and
`process/coverage.md` are unchanged from the accepted review source.

The live clean build succeeded with:

```sh
latexmk -gg -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

The resulting `build/main.pdf` has 18 pages. Its final log has no warnings,
undefined references or citations, overfull or underfull boxes, or fatal
errors. I checked the rendered attribution text and visually inspected PDF
pages 5 and 17, confirming the intact lemma statement, complete Adler–Beling
entry, and correctly displayed Gritzmann–Sturmfels entry. No clipping or
overlap appeared on the inspected pages. Final integrated pagination remains
part of the planned manuscript-wide pass.

Evidence is retained in `verification/correction-agent/stage02/`:

- `build-command.log` and `final-main.log`: full rebuild transcript and final log.
- `source.diff` and `checks.json`: exact source changes, hash checks, unchanged
  mathematical content, and final diagnostics.
- `rendered.txt`, `lemma-page5.png`, and `references-page17.png`: PDF text and
  inspected layout.

Remaining accepted issues: **none**. Root status, assessments, and frozen
snapshots were not edited. Stage 3 was not started, and no work was delegated.
