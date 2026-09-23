# Stage 1 author report

This stage writes `main.tex`, `macros.tex`, `bibliography.bib`, `Makefile`, and Sections 2–4. It is a mathematical core for the later joint-accuracy, LP-access, and literature-synthesis stages, not yet the complete requested paper.

## Sources read and incorporated

Read in full:

- `workbench/active/2026-09-04-exact-two-cluster-shift.md`.
- `workbench/active/2026-09-04-two-cluster-interval-shift-upper.md`.
- `workbench/active/2026-09-04-adaptive-normalized-shift-hierarchy.md`.
- `workbench/active/2026-09-04-normalized-shift-staircase.md`.

Verified the real-polynomial QSVT implementation against the local Gilyén–Su–Low–Wiebe full text, Corollary 18. The bibliography metadata for that source and Orsucci–Dunjko comes from the local literature database; Motlagh–Wiebe's arXiv abstract/version was checked online. Root handles the broader literature audit and novelty positioning in later stages.

## Results and proof checks

- Exact quadratic interpolation includes its contractivity hypothesis and factorized clustered-support error. The two-query claim uses real-polynomial QSVT with coherent conjugate averaging, not the stronger single complex-sequence completion condition.
- A direct hybrid proof establishes a conservative explicit two-scalar approximate lower bound. It accounts for allowed output-amplitude error instead of quoting the notes' error-free complementary amplitudes.
- Exact interval impossibility is proved by analyticity and strengthened to every normalization strictly below two.
- The model includes arbitrary oracle completions, controlled calls and inverses, reusable coherent output, worst-case query count, and deferred finite measurements. It excludes free postselection and does not claim expected-stopping-time lower bounds.
- GQSP implementation is reduced explicitly to a Hermitianized arbitrary block encoding and a two-dimensional walk. The centered Laurent polynomial has ordinary degree at most 2d; undoing its centering uses another d walk calls. Hermitianization costs only a constant query factor.
- All-circuit lower bounds use the scalar trigonometric polynomial and a compactness limit of the rescaled Taylor polynomial. Only the limiting polynomial is globally nonnegative.
- The Chebyshev threshold formula includes global nonnegativity, the negative-lobe estimate, unique maximizer, strict decrease (including a separate check from G0 to G1), and large-index asymptotics.
- The pinned gate proof now gives explicit polynomiality, local slack domination, and all-domain tail bounds. Its global contractivity proof covers the region containing positive and negative pins. This proves exact threshold inequalities, not merely `(G_r+o(1))*delta` errors.
- The logarithmic lower bound is proved by elementary interpolation on a fixed circle arc; no unstated Remez theorem is required.
- Full definite-parity lower hierarchy, explicit affine threshold, Fejér-kernel square-root upper, and the GQSP versus a single definite-parity QSVT separation are included.
- The ratio-two sign-selector construction and the unpinned strict-threshold construction are superseded by more general proved constructions. Their mathematical conclusions are covered; duplicating their alternative formulas would add no distinct theorem.

## Corrections to the notes

1. The coarse tier is logarithmic only if `0<c<1`. If `c=1`, the fixed upper band is one known point and a degree-four polynomial gives constant query complexity, including equality `K=G0`. A zero-query indistinguishability argument supplies the matching lower bound.
2. The claimed `o(1)` precision for the integer-valued inversion of the threshold index is replaced by `O(1)`, explicitly including rounding. The resulting query-exponent asymptotic is unchanged.
3. The exact differentiated normalization-slack inequality is only a formal necessary condition near normalization one: exact interval conversion is already impossible whenever `nu<2`. The paper states this explicitly and does not present that inequality as an attainable exact tradeoff. Approximate normalization-slack complexity is not claimed.
4. The scalar-pair explicit constant is derived afresh with the error tolerance included. It remains an absolute positive multiple of `delta^(-1/2)`.
5. Query complexity is explicitly separated from gate synthesis and phase-computation time. Fixed-K asymptotics are not asserted uniform in joint vanishing K and delta.

## Validation and pending scope

`conda run -n qipm --live-stream make -C spectral-shift-paper` completed successfully. Final LaTeX log has no undefined references/citations or overfull/underfull box warnings. Independent five-reviewer review is still required by the user's process; this author pass is not a substitute.

No known unresolved mathematical gap remains in the stage's stated theorems. Later sections and the full prior-work/novelty discussion remain intentionally outside this stage. The manuscript currently has a temporary abstract and no comprehensive introduction; these are scaffolding for Stage 4.
