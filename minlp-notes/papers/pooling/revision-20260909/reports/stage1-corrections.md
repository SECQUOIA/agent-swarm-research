# Stage 1 accepted minor corrections

Completed all three changes accepted in `stage1-round1-adjudication.md`. No theorem statement, proof scope, or mathematical argument was changed. No delegation was used.

## Changes

1. Added a two-panel physical-network schematic, `figures/emission-conversion.tex`, and its local reference immediately after the conversion argument in Section 2. The diagram is native TikZ; `main.tex` loads TikZ and its standard `arrows.meta` library. It shows input, pool, and product columns, capacity and quality labels, every local gadget flow, and the precise marked nodes. Dashed arrows distinguish the physical source-to-pool arcs assigned by the caller. The caption expressly identifies the omitted storage feeds, diluent, slack, and other uses, and leaves caller-owned receiving pools' markings unspecified.
2. Added `Section 4.3` to the existing Boland–Kalinowski–Rigterink citation in the cyclic-formulation discussion of Section 1.
3. Added the Dey–Gupte electronic-companion Appendix A citation after the established Haugland Theorem 2 attribution in the one-pool/no-bypass certificate proof. The new sentence attributes the earlier MILP representation with both quality directions; it does not attribute the manuscript's broader flow-contract statement to that source or make a novelty claim for the certificate.

## Mathematical and source checks

The emission panel has exactly the marked nodes `Q`, `r`, and `t`. Its product inflows are `1/a` and `2-1/a`; its marked source splits into `2-1/a` and the caller delivery `1/a`. Thus both marked totals equal two and the product quality mass is `(a/B)(1/a)=1/B`, as required by exact quality `1/(2B)` at total two. The relay `H` is unmarked.

The conversion panel marks exactly `r1` and `t0`. The caller's quality-zero source sends `d` to `H0`, while the new quality-one source splits into `2-d` through `H1` and `d` to the receiving pool. The product total is two, and its specification is the vacuous interval `[0,1]`. No relay is marked. Every displayed arrow has type input-to-pool or pool-to-product. These checks use the current emission lemma and equation `s2:flip`; neither diagram introduces a pool-to-pool arc or a new constraint.

For Boland et al., read the local article's Section 4.3, **Equivalence of formulations**, beginning on printed p.10 and continuing on p.11: `literature/papers/boland2016-new-multi-commodity-flow-formulations/fulltext.md`. That is the discussion of cyclic formulation equivalence already cited by the paper. The current manuscript's qualification about singular circulations remains intact.

For Dey–Gupte, opened and retrieved the [open author manuscript](https://optimization-online.org/wp-content/uploads/2013/04/3849.pdf). Its electronic companion begins on PDF p.32, printed ec1, with Appendix A, **MILP representability of the single pool case**. The discussion and rows (EC.1a)–(EC.1f) give the one-pool representation, including both quality bounds and product-selection binaries. The manuscript explicitly identifies the structure as all source flows mixing at a single pool before reaching products. A copy of this open source and a fresh layout extraction of ec1 are saved in the check directory below. The repository's existing Dey–Gupte package contains a slide artifact; its metadata and generated literature files were not changed or used for article pagination.

## Build and visual inspection

Copied `main.tex`, `bibliography.bib`, all sections, and the figure directory into the isolated directory `revision-20260909/checks/stage1-corrections-build/`. Built there with `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`; exit status was zero. The final PDF has 92 pages. The final LaTeX log contains no warning, undefined reference/citation, overfull box, or error. Checked that the four changed manuscript source files match their isolated copies byte for byte.

Output PDF: `revision-20260909/checks/stage1-corrections-build/main.pdf`.

Build transcript: `revision-20260909/checks/stage1-corrections-build/build.log`.

Rendered figure: `revision-20260909/checks/stage1-corrections-build/emission-conversion-page.png` (PDF p.17, rendered with `pdftoppm`). Visually inspected at 1800-pixel page height: arrows, dashed caller connections, formulas, markings, and caption are legible, with no clipping or overlaps. Root independently inspected the same page and accepted the schematic. The caption's final refinement says that the caller supplies the connecting arc's **other** endpoint; that final source was rebuilt successfully and the render refreshed.

Source evidence: `revision-20260909/checks/stage1-corrections-build/dey-gupte-open-manuscript.pdf` and `dey-gupte-appendix-a.txt`.

This correction pass verifies the accepted local changes and their build. It is not a new proof audit of Sections 3–6 or a claim of formal verification. No accepted issue remains unresolved.
