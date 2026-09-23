# Stage 1, round 2 — reviewer 13

**Verdict: MINOR.** No major mathematical or coverage defect found. One local notation definition should be added. The finite full-signing results and the accepted round-1 repairs withstand this review.

## Coverage

Read the assignment, `process/review-protocol.md`, `process/scope-proposal.md` (including all Stage 1 coverage rows), `process/stage01-round01-adjudication.md`, and `process/stage01-corrections.md`. No other round-2 report was read.

Reviewed all frozen manuscript text under `process/snapshots/stage01-round02/`: `main.tex`, `macros.tex`, `references.bib`, `sections/01-foundations.tex`, and `sections/appendix-finite-signings.tex`. Independently checked all manifest hashes. Inspected rendered PDF pages 11–12 for the printed enumeration program, witness table, and bibliography; they are readable and unclipped. This was not a new LaTeX build or a visual audit of every PDF page.

Read the canonical dependencies `results/mccormick-gap-degeneracy-bound.md`, `results/mccormick-hereditary-density-characterization.md`, and `results/positive-multilinear-degree-upper-bound.md`, with the latter's preliminary envelope, independence, and box-transfer arguments being the Stage 1 dependencies. The finite center constants, distinct direct degeneracy argument, and local-versus-global cut distinctions required by the Stage 1 coverage rows are present. Later-stage results are outside this review.

Read `literature/AGENTS.md` before using the collection. Checked relevant source statements and proofs in the local fulltexts, and extracted important formulas directly from originals:

- `[[luedtke2012-some-results-on-the-strength]]`: recursive product discussion in Section 2; vertex representation and common upper attainment, p.8-9; positive coloring bound, p.15. Original PDF pages 8–9 and 15 confirm the cited theorem numbers, formulas, and nonnegative-domain restriction.
- `[[boland2017-bounding-the-gap-between-the]]`: Theorems 2 and 4 and predecessor attribution, p.3; induced-cut identities and Corollary 1, p.4-6. Original PDF extraction confirms these constants and identities.
- `[[davidson2007-norms-of-schur-multipliers]]`: Theorem 1.2, p.4; weighted matrix Theorem 2.4 and row/column estimates, p.6-7; the associated proof passage. Original PDF pages 4–7 resolve formulas omitted by the Markdown extraction and confirm that the continuous weighted theorem supports the stated bound without integer rounding.
- `[[mccormick1976-computability-of-global-solutions-to]]`: introduction and algorithm discussion, p.1-4, supporting the manuscript's broad historical description.

Szarek's bibliographic metadata was confirmed on the [publisher's article page](https://www.impan.pl/en/publishing-house/journals-and-series/studia-mathematica/all/58/2/101277/on-the-best-constants-in-the-khinchin-inequality). The publisher download and EuDML access both returned HTTP 403. I therefore did not inspect Szarek's original proof; the sharp real Khinchin inequality is an explicitly retained external theorem dependency. I did not directly inspect the Misener–Smadbeck–Floudas predecessor; the manuscript accurately makes its attribution indirect through Boland et al.

## Findings

**R13-1 — MINOR: define the row-vector notation before the row estimates.**

Location: frozen `sections/01-foundations.tex`, lines 295–309, immediately before Lemma `lem:cut-row`; the same notation recurs through the proof of Theorem `thm:bilinear-upper`.

The text defines the symmetric weighted adjacency matrix `A`, but never explicitly defines `a_{i,T}` or `a_i`. These symbols first appear inside the lemma's principal inequalities. Their intended meaning is recoverable from the proof, so this does not compromise the mathematics, but it is a local omission in an otherwise careful notation setup. In particular, `a` previously denotes an edge coefficient vector, whereas `a_i` now denotes a full matrix row with nonedge entries zero.

Concrete repair: after defining `A`, add: “Write `a_{i,T}=(A_{ij})_{j\in T}` and `a_i=a_{i,W}`.” This also makes the treatment of nonedges and isolated vertices immediate. The canonical degeneracy note explicitly supplies this definition; the manuscript should do so too.

No other substantive finding. The theorem organization is workable: the upper theorem is announced first, followed by the exact induced-cut reduction, row estimates, fractional orientation, and its proof. The finite-signing subsection cleanly separates `M_n`, `F_n`, and the arbitrary-real-coefficient supremum.

## Independent verification

The following are analytic checks of the universal arguments, not inferences from numerical experiments.

1. **Envelope foundation.** Independent endpoint sampling puts every multiaffine graph point in the vertex graph hull. The finite vertex polytope gives attained envelope extrema and piecewise-affine boundary continuity. The circle construction for product lower envelopes works both below and above total failure mass one. Common-threshold rounding simultaneously attains all positive upper envelopes. After affine terms are discarded, subtracting the product lower envelope gives `t_e=min(u_e,S_e)` and the full gap is the maximum total deficiency. The two independence cases retain the stated constant, including boundary means. Nonnegative expansion gives the original-versus-expanded termwise inequality in the correct direction; it does not preserve arbitrary incidence structure.

2. **Induced-cut reduction.** At a face center, the symmetric two-point sign law preserves all means and gives `H=R_W/2`, while each active product gives `T=L_W/2`. Coordinates fixed to one introduce only affine terms. The cell-vertex argument accounts for fixed coordinates, odd complementation cycles, and free components, so all relevant vertices are half-integral. Since `T-cH` is convex on each cell for nonnegative `c`, the grid bound extends to the full cube. Orthogonality of distinct sign characters ensures `R_W>0` whenever `L_W>0`.

3. **Constants.** Polarization gives half the quadratic range exactly as the largest rectangular cut-block infinity-to-one norm. Khinchin gives the factor `1/sqrt(2)` for each side. A cut locally maximal for squared weights has at least half of every squared row weight crossing, yielding `R >= (1/4) sum_i ||a_i||_2`. Fractional orientation and weighted Cauchy–Schwarz count each absolute edge weight once and give `L <= 4 sqrt(rho_G) R`; counting full rows twice gives `L <= 2 sqrt(Delta_G) R`. The direct degeneracy coloring argument is valid and distinct. The signed four-cycle attains the bipartite constant.

4. **Worst coefficients and attribution transfer.** The random-sign exponential estimate uses `2^h` terms after global sign symmetry and both exponential signs; minimizing its bound gives `sqrt(2mh log 2)` without an independence assumption between configurations. Extending the signing outside a densest face preserves the witness. The center supremum proof zeroes exterior coefficients before taking the supremum and uses continuity only for the full-graph ratio. In the Schur transfer, symmetric adjacency has `beta=rho_G`, `<A,sign(A)>=2L`, and polarization bounds `||A||_{infinity->1}<=4R`, yielding exactly `4 K_G sqrt(rho_G)`. The stated Sidon comparisons use mean zero correctly.

5. **Exactness and conventions.** Equality `R=L` requires the positive and negative edge sets each to be cuts; the even-cycle intersection characterization supplies both necessity and sufficiency. Nonempty effective support is now explicit for factor-one assertions, with the zero function treated separately. Absolute tolerance is nonnegative, relative tolerance lies in `[0,1)`, and the best-incumbent relative normalization requires positive optimum. The target derivatives in the incumbent are respectively `1` and `1-theta`, so the claimed monotonicity is correct.

The finite computation is independently reproducible in `verification/reviewer13/round02/check.py`, with results in `verification/reviewer13/round02/results.json`. It uses direct quadratic evaluations by integer matrix multiplication, rather than the appendix's crossing-edge masks. Every dot product contains at most 21 signed unit terms, so its `int64` arithmetic is exact with ample overflow margin; all reported ratios use exact fractions.

- Normalized representative counts for `K_2` through `K_7`: `1, 2, 8, 64, 1024, 32768`.
- Minimum cut ranges: `1, 2, 4, 4, 5, 8`.
- For `K_7`, the complete range histogram is `{8: 3240, 10: 20664, 12: 8864}`.
- Every printed witness has the listed quadratic extrema. Direct evaluation on every induced face also confirms its all-face ratio.
- Extending the printed `K_6` witness gives extrema `(-9,11)`, center ratio `21/10`, and all-face ratio `3`.
- Extracting and executing the verbatim program from the frozen appendix returns `[1, 2, 4, 4, 5, 8]`.

Switching normalization is complete and unique because preserving the positive root star forces all switching signs equal. Complementation covers every cut with the root fixed. The initial search bound exceeds every possible range because differences of two cut weights involve at most all edges with unit coefficients. Thus the appendix establishes the specified finite minima, rather than only verifying witnesses. The analytic restriction-and-extension argument then gives `F_n=max_{2<=k<=n} M_k`; it does not identify these full-signing maxima with the arbitrary-real problem.

## Remaining limits

The original Szarek proof was inaccessible in this review, as described above. No new priority search or proof of the optimal general density constant was undertaken. Exact finite enumeration establishes only the listed finite signing claims; it does not prove a formula for larger complete graphs or the optimal arbitrary-real constants. These limits agree with the manuscript's stated scope and are not additional findings.
