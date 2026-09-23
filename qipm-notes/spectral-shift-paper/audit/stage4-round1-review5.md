# Stage 4, round 1 — independent review 5

**Result: 0 major findings, 0 minor findings.** The new presentation agrees with the reviewed mathematics, the source ledger accounts for the relevant research notes, and the submission archive builds and reproduces independently. No repair is requested.

Reviewed the new abstract, introduction, conclusion, reproducibility appendix, overview script and figure, README, Makefile, packaging script, bibliography, final source ledger, and author audit. I did not read peer reports or change manuscript files or stored artifacts. All execution used the qipm environment; archive tests ran in `/tmp/stage4-review5-dsv5eu67`.

## Presentation and mathematical consistency

The abstract and introduction correctly distinguish the fixed-accuracy staircase, its two coarse cases, the even threshold plateau, the concrete matched parity comparison, the odd logarithmic factor, and the uniform high-accuracy regime. The intermediate-regime summary retains the margin factor and does not claim an optimal multiplicative law. The degree-six witness is consistently an upper bound on `F_3`, not its exact value.

The access model is stated before the results, including arbitrary input completions and repeated oracle cost when the conversion circuit is reused. The LP overview preserves the dual-state target, counted right-side access, separate matrix-only compiler contract, zero-query coarse exception, and digital-access bypass. The conclusion identifies genuine remaining problems without weakening or overstating the proved claims.

The overview figure is mathematically consistent. Its left panel puts threshold equality on the cheaper tier; the displayed terminal segment stops before the next threshold. The right panel uses a range where `G_1<K<G_0` and where the positive degree-six witness proves the even index is three below `1/24`. Overlapping even and unrestricted curves above that value are shown without changing their exponents. The caption states the coarse and odd logarithmic qualifications. I visually inspected the regenerated figure.

The related-work framing separates standard synthesis, sign approximation, polynomial query methods, factor access, and amplitude estimation from the manuscript's claims. The descriptions of the especially close recent works agree with primary sources: [Dong et al.](https://arxiv.org/abs/2608.30937), [Laneve](https://quantum-journal.org/papers/q-2026-03-13-2025/), [Somma–de Wolf](https://arxiv.org/abs/2608.24493), and [Sarkar–Yoder](https://arxiv.org/abs/2111.07182). The qualified originality statement concerns the specific results and makes no universal priority guarantee.

## Repository-note coverage

The eight-note final ledger agrees with the source developments independently checked in my earlier stages. It records the substantive corrections: approximation-aware pairwise constants, the degenerate high-band exception, integer rounding, stronger even/odd parity results, explicit growing-degree constants, exact fixed-error state orders, and the LP's zero-query coarse branch.

I repeated searches across the workbench and neighboring manuscript sources for normalized shift/complement, plain-H, spectral-shift, and exact-subnormalization language. Additional workbench matches concerned cone complementarity or cohomological normalization, not omitted shift results. The frontier note routes its shift developments to the eight listed notes. The broad paper's Section 4 contains the motivating open question; Section 16 repeats that question without an additional theorem. The scalar-Newton coherent-access discussion explicitly treats normalized complement access as a separate assumption. These agree with the ledger's scope distinctions. No substantive source development is missing from the standalone manuscript.

I checked the ledger's explicit theorem numbers against the extracted build's auxiliary labels; no mismatch was found. There are 100 distinct manuscript labels, all references resolve, and all 18 bibliography entries are cited with no undefined citation keys.

## Standalone package and reproduction

The ZIP passes its CRC check and contains 18 files. Every archived file matches the frozen workspace. Its allowlist includes all referenced sections, macros, bibliography database and generated bibliography, the required PDF figure, three scripts, README, and Makefile. It excludes audit files, local literature, previews, and intermediate products. No repository-relative dependency is needed to read or build the paper.

In the extracted directory I ran the ordinary build, figure regeneration, rebuild and source packaging. All succeeded. The generated 31-page PDF has text identical to the workspace PDF; the final full-build log is clean. Both overview outputs checked as data/image—the CSV and PNG—and both supplementary CSVs reproduce byte-for-byte. The observed Python and library versions match the README.

I also exercised `make clean`: it retains the supplied bibliography and required figure, and the documented two-pass direct pdfLaTeX build succeeds afterward. The normal Makefile build does not invoke Python. Figure scripts import their shared solver and locate output directories correctly in the extracted tree. Packaging the extracted source produces the expected portable archive again.

The appendix and README appropriately describe the plots as deterministic floating-point illustrations, not mesh-based certificates. The paper remains standalone apart from its explicitly cited standard results. This presentation/package review does not replace the planned fresh full-proof review.
