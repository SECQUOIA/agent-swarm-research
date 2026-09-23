# Stage 1, round 1 — reviewer 04

Primary lens: bilinear graphs, contact geometry, fractional-cover LPs, covariance-volume reasoning, and rational precision.

Major findings: 0

Minor findings: 2

## Snapshot and coverage

I checked the following actual SHA-256 values against `reviews/stage1-round1/snapshot.json`; all match.

| File | SHA-256 |
| --- | --- |
| `coverage.md` | `a5b675009a1c889bf93105e5b1121f2d5de5fac732d414c4b0b71563e1ce7727` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `cecaea518c089ff3beca3edf14ec879129f947f67ed01af7ef3602fb74ea571e` |
| `references.bib` | `bc7fbcf1dad163b2e1064e787760f7f76b88ba649c3f6657d3a46d9432a433da` |
| `sections/01-foundations.tex` | `075e0e998e9cf3e9bdf0830fde1822876ac272bb336eec5d10374425ace92e03` |

I read all 1,206 lines of the stage, the process and review protocol, bibliography, macros, main file, and coverage inventory. I checked every displayed proof chain, with deeper reconstruction of the product-width bound, weighted graph allocation, rational demand rounding, covariance identity, determinant constants, and Hall/permanent argument. Source comparisons included the complete bilinear graph and covariance result files, relevant portions of the noncommutative-rank, rational construction, smooth-map, constant-rank, one-sided inertia, and perspective results, the supporting binary-lower-bound extension note, and the two bilinear review notes. I did not treat their review verdicts as proof.

After reading `literature/AGENTS.md`, I checked primary-source passages in the local Lubin–Vielma–Zadik and Beach full texts and the cached GGOW text. I also checked Theorem 1.5 and Lemma 5.3 directly in the [2018 IQS manuscript](https://arxiv.org/html/1512.03531): they supply the asserted rational output/intermediate-data bounds and field-extension invariance. I have not audited every bibliography entry against its original PDF, performed an exhaustive novelty search, verified every item in the later-stage inventory, or compiled/visually inspected the PDF. The explicitly deferred stage-2 bit-bound proof is outside this stage's proof obligations.

## Assessment

I found no major mathematical defect in this stage. In particular, the bilinear theorem establishes its lower bound for arbitrary convex lifts and unrestricted integer ranges, and its upper formulation uses genuinely shared input bits. The rational construction correctly avoids the need to compute LPs with exact logarithmic right-hand sides. The covariance and permanent arguments also check out, including their constants and their application to nonconvex compact contacts. This is an assessment within the stated verification limits, not a claim of certainty or external peer review.

## Findings

1. **MINOR — malformed multiplication in the smooth upper proof.** Location: `sections/01-foundations.tex`, lines 974, 977, and 992, proof of `thm:smooth-ranks`. The expressions `C_0,2^{-T}` and `2C_0,2^{-T}` contain literal commas. The intended Taylor bound and error-budget condition are products, `C_0 2^{-T}` and `2C_0 2^{-T} <= epsilon`. This is a notation/transcription defect, not a false estimate: the next sentence bounds each contributing Hessian product by a constant times `2^{-T}`, and the original smooth-map result has the correct multiplication. Replace the three commas by `\,` or ordinary multiplication spacing. It would also be helpful to give the explicit choice `T=max{0,log_2(2C_0/epsilon)}` when `C_0>0`, as in the source proof.

2. **MINOR — the capacity equivalence needs its own accurate source locator.** Location: lines 529–541, especially the collective citation to GGOW Theorems 1.4 and 1.17 preceding `eq:capacity`. Those theorem statements support matrix evaluations and rank/shrinking (Theorem 1.17 through its zero-block characterization), but neither states positivity of capacity. The capacity claim itself is correct and supported elsewhere in the same primary paper: the discussion at the end of Section 1.5, published p. 237, explicitly attributes positive capacity for noncommutatively nonsingular pencils to Gurvits, and Section 2 develops capacity. Thus this is a citation-locator/credit issue, not a missing mathematical hypothesis or a failure of the main theorem. Split the citation: retain Theorems 1.4 and 1.17 for the algebraic characterizations, and cite the capacity discussion/Section 2 separately, identifying the Gurvits origin. The original repository nc-rank result already makes this distinction. Primary evidence: cached `build/source-cache/ggow2020.txt`, lines 235–267, 509–521, and 740–750; [published GGOW paper](https://www.math.ias.edu/~avi/PUBLICATIONS/GargGOW20.pdf), pp. 227, 232, and 237.

## Checks supporting the assessment

- The product condition on a parity contact is `|Delta x_i Delta x_j| <= 4 epsilon_ij`; multiplying by the valid width constant five gives the theorem's `20 epsilon_ij`. Positive widths yield feasible nonnegative logarithmic LP coordinates. Zero widths give zero full-dimensional volume, so no logarithm of zero is taken.
- The upper identity `y_i y_j=A_i y_j+rho_i A_j+rho_i rho_j` is exact before relaxing the final product. Each relaxed residual incurs at most `h_i h_j/4`; exact residual products provide simultaneous witnesses for all outputs. The endpoint `y_i=1` and depth zero are covered.
- The clipped demand increase between `L_20` and `L_4` is at most `log_2(5)`. Adding that multiple of a fractional cover proves the stated comparison, including edges whose demands cross zero. Integer demand rounding costs at most one more fractional-cover value. Isolated vertices can receive zero depth.
- For rational `epsilon=a/b`, the rounded demand is the least nonnegative integer `d` satisfying `4a 2^d >= b`. Its magnitude is bounded by the tolerance encoding length. If `D` is the maximum demand, setting all coordinates to `D` is feasible, so an optimal nonnegative allocation has every coordinate at most `nD`. Consequently the dyadic depths, output row count, and coefficient lengths really are polynomially bounded; this does not follow merely from writing down a rational LP.
- Independently expanding the centered fourth moment gives exactly the displayed covariance identity. Whitening and the centered-ball rearrangement give the stated volume constant. The capacity/AM–GM combination yields the printed finite nc-rank constant. The Hall argument produces a positive permanent for each orthogonal basis; its continuous minimum on the compact orthogonal group is positive, which supplies the required uniform constant.
- The remaining stage checks covered the parity closures and finite disjunction, square and scalar-rank constants, one-sided signed-square construction and LP facet count, principal compression and real shrinking, oscillatory contact argument, polynomial prefix compiler, Legendre tubes, PIT example, and perspective row division. I found no additional concrete issue in those checks.

Executed verification:

- `python code/mip_relaxation_binaries/check_graph_precision.py`: **PASS**, 226 weighted allocation cases and 306 projected LP extrema. This is an existing numerical checker, not an independent proof.
- Independent inline SymPy/Fraction checks: **PASS**, all six exact products in the four-point width obstruction and 3,200 exact rational-demand cases, including minimality and a bit-length bound.
- Snapshot hash comparison: **PASS**, all five files.

No manuscript, bibliography, original result, or other reviewer report was edited. No subagents were used.
