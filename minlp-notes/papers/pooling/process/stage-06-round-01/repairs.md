# Stage 6, round 1: accepted minor repairs

Implemented the root adjudication M1–M4 and the subsequently authorized packaging repair M5. No mathematical statement, numerical bound, or proof was changed beyond clarifying the specified conventions.

## Exact changes

- **M1:** In `sections/06-synthesis.tex`, replaced “compact convex singleton of dimension one” with “compact convex singleton in one scalar variable.”
- **M2:** Defined the entrywise unit ball as `U_1={E:sum_{i,j}|E_{ij}|<=1}`. Replaced “total SOC size” with “total second-order-cone dimension”; specified that scalar inequalities count as nonnegative cone factors or PSD blocks of order one, and that SDP size is the sum of block orders.
- **M3:** Added the direct Khademnia–Davarnia citation at the established compact network–simplex hull sentence. Both the sentence and new bibliography entry `s6:khademnia2024v2` identify arXiv:2302.14151v2, dated 26 February 2024; Appendix equation (25) refers to that version. The citation follows the version and original-PDF check recorded in the root adjudication. No journal metadata or page numbering was mixed into the preprint citation.
- **M4:** Added a real repository-root-relative result-file path to each of the twelve adjacent unpublished-note bibliography entries. Added the reader-facing locator explanation in Section 6 and `papers/pooling/source-index.md`, which maps all twelve citation keys and exact source titles to paths and SHA256 values. Source headings were checked directly. No authors or public URLs were inferred for these notes.
- **M5:** Replaced all seven conditional section inputs in `main.tex` with ordinary required inputs, as requested by root after the initial assignment. The preamble and all other driver content are unchanged.

The optional classical convex-order sentence was not needed for the accepted repairs and was not added.

## Validation and preservation

From `papers/pooling`, ran:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The build succeeded and produced a 91-page PDF. The full output is `repair-build.txt`. The final LaTeX log has no overfull boxes, unresolved references or citations, multiply defined labels, or pending rerun requests. It has eight underfull bibliography diagnostics. Bibliography PDF pages 88–91 were rendered and visually checked: all twelve note locators and the new primary citation are legible, stay within the text area, and have no overlap or clipping. The two BibTeX warnings are `empty year in s6:boveroux2026` and `empty year in s6:lrs-full`; these existing, explicitly undated source entries remain unchanged.

The first attempted build command used the repository root and failed before launching LaTeX because its log directory did not exist there. The successful build above used the documented manuscript directory.

Before editing, SHA256 values were recorded in `repair-protected-before.json`. The final comparison confirmed that all 211 protected result files, section files 00–05, frozen snapshots, and reviewer reports stayed byte-identical. Two other tracked baseline files changed as authorized: `main.tex` for M5, and `adjudication.md`, to which root independently added M5 during this repair. The repair agent did not edit the adjudication.

Compared every existing bibliography entry with the frozen Stage 6 bibliography: exactly twelve entries changed, each only by adding its note locator; the sole new key is `s6:khademnia2024v2`. All twelve locator targets exist and match the source-index hashes. Seven required section inputs were verified. Existing mathematical checks were not repeated because no mathematics changed.

`repair-validation.json` records these checks and final SHA256 values for all seven section files, `main.tex`, `bibliography.bib`, `source-index.md`, and `main.pdf`. The source index separately records the twelve original note hashes. Final Section 6 SHA256: `292bbf37694a33c79b53a0310426ca81846bbe4eef2a1bd42cf28a802a10c217`. Final PDF SHA256: `d08789cb9be2d8844bc57e6fba0148083c1440409ce1c9bce4cc68b2ab30f7f2`.
