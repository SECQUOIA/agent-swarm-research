# Independent review: Stage 07, round 01, reviewer 5

Reviewer: `paper_reviewer_5`. Date: 2026-09-07.

**Verdict: no major issue found; correct one minor numerical rounding statement.** The synthesis agrees with the accepted theorems. Both added trial asymptotics are justified, and the numerical evidence distinguishes discrete optimization, quadrature, and continuum claims appropriately. A separate complete-manuscript review remains required.

## Snapshot and independence

I verified every repository-relative file hash in snapshot `d383884b23d489bd685197e179c0e74be518161c6cf0575298800612eae383c0`. I read the author handoff, new introduction/numerics/discussion, numerical driver and its two imported solver/profile files, stored evidence, README, bibliography, literature audit, and the relevant accepted statements and proofs. I did not read other reviewer reports or the coordinator's numerical/check records, did not delegate, and did not edit manuscript source.

## Mathematics and scope of the synthesis

**Unrounded mean profile.** Let `Z_0=∫|sin s|^(−2/5)` and `Z_R=∫(|sin s|+R)^(−2/5)`. The unrounded and rounded unit-budget fields obey

`D_0/D_R=(Z_R/Z_0)[(|sin s|+R)/|sin s|]^(2/5)≥Z_R/Z_0→1`.

Form ordering therefore gives `J(D_0)≤(Z_0/Z_R)J(D_R)`. The unrestricted optimum is a lower bound for the unrounded trial. The accepted rounded equivalent squeezes its mean to the same sharp coefficient. The unrounded coefficient is integrable and has a positive compact-wall floor despite its unbounded fold values, so no inadmissible measure field is introduced.

**Distance-based critical profile.** Both normalizations have leading term `4log(1/R)`. On fixed-small fold neighborhoods the distance and sine denominators differ relatively by `O(r_*²)`, while their coefficients can be frozen on the retained root neighborhoods as in the accepted critical proof. The contribution outside those fixed fold neighborhoods has only order `a_R^(−2/5)`. The inner omitted annuli satisfy the accepted graded bounds. Sending M to zero before shrinking r_* proves the claimed sharp coefficient. This argument supports the critical asymptotic guide, but does not identify the third-moment graded trial with the supercritical minimum; the text correctly avoids that inference.

**Abstract, introduction, and discussion.** The moment table uses unrooted moments and correctly converts the uniform baseline to total budget. It distinguishes exact coefficients for the cosine family from generic order statements. The attained variational constants, exact-observation mean, finite-ratio crossover, separate coarse limit, and information-preserving physical transfer agree with the accepted results. The distinction between quenched channel variability and particle displacement statistics is maintained. The discussion states the nonzero-mean, fixed-bulk, affinity, wall-dimension, and stationarity requirements, and does not claim finite-budget optimality or manufacturing feasibility. The background/noise/cap exclusions match the actual admissible class.

## Independent numerical assessment

1. **Circle solver and resources.** I inspected the imported tridiagonal assembly. Its off-diagonal conductances, diagonal reaction plus adjoining conductances, zero endpoint flux, and factor `2h` in the full-circle response match the manuscript. The driver's common normalization makes `2h∑D_i=M` for uniform, graded, and observed fields. Its Gaussian integration coefficient is correct: reflection of the offset distribution gives `(1/2)∫_0^2`, and mapping each Gaussian interval contributes `(hi−lo)/4`. The stated subdivision widths, including the unrounded mean's quadrature-only width, match the code. The explicit observed branch and patch formulas also match their imported implementation.

2. **Independent full-resolution rerun.** Without writing the stored data, I reran the complete mean row at `M=10^(−3)`, 32768 half-wall cells, and 48 nodes per subdivision. Its trial value and trial/uniform ratio matched the saved row exactly in the current environment. I also recomputed the reported changes from every saved refinement row. The principal finite-budget ratios, third-moment reduction, critical scaled values, observed-branch quadrature change, and independent-grid/quadrature distinctions agree with those rows, apart from the minor percentage rounding below.

3. **Uncertain-center objective.** The face mass convention gives conductance `p_i/h³`, and differentiating `h 1ᵀH^(−1)1` gives the negative squared neighboring solution difference divided by `h²`. The exterior term is the exact averaged integral of `(x−z)^(−2)` outside `[-L,L]`; its displayed logarithmic formula and eta=0 limit are correct. It is independent of the mobility variables.

4. **Independent solver/gradient derivation.** I assembled the center matrix densely on a separate 19-cell problem with a nonuniform positive mass vector and eta=1.4. Dense and banded objective values agreed exactly at the printed precision; the maximum gradient discrepancy was `3.55×10^(−15)`. A centered finite difference in a mass-conserving direction differed from the analytical directional derivative by `1.15×10^(−10)`. This checks the derivative factors and matrix indexing through a separate formulation.

5. **Stored center values and tangent bounds.** I reconstructed feasible masses from every saved primary 400-cell profile and independently re-evaluated the objective and gradient. Value differences were at most `1.87×10^(−14)` and gap differences at most `7.55×10^(−15)`; all masses were nonnegative. Convexity yields exactly the stated lower value because minimizing the tangent over the unit simplex gives `min_i g_i`. The saved gaps support an interval for the same finite-dimensional, finite-quadrature problem, not for the continuum. The manuscript makes that restriction explicit and illustrates it with the eta=0 value below exact `C_pl`.

6. **Refinement limits.** The eta=32 fixed-spacing domain comparison is nested at the same grid spacing, and its value difference is indeed smaller than the optimization gaps. The text correctly describes it as a diagnostic rather than a rigorous domain error bound. The 24-node negative example has a small discrete gap but rises by 11.5703% under the independent 384-node evaluation. This is useful evidence against treating optimizer convergence as quadrature validation. The six-digit computed values are accompanied by their much larger optimization gaps, rather than presented as six-digit continuum optima.

7. **Figures and provenance.** I rendered and visually inspected both figure PDFs. Their axes, legends, asymptotic guides, and trial/discrete labels are readable. The moment panels correctly show budgets decreasing from left to right. The local-profile and continuum-bound panels do not imply a continuum certificate for the markers. The plots and generated tables use the saved quantities described by the manuscript. The README identifies the necessary repository solver dependencies, and compilation is independent of rerunning optimization.

## Literature check

I inspected the primary [2026 Alphonse–Kunštek–Vrdoljak preprint](https://arxiv.org/html/2602.19869v1), the [Buttazzo–Maestre preprint](https://arxiv.org/pdf/1002.2770), and the [Alexandre–Guérin–Dean primary record](https://arxiv.org/abs/2105.06212). The two stochastic-conductivity models have the positive-conductor/random-load setting described in the introduction; that restrictive comparison is not applied to the earlier degenerate mass-design literature. The generalized-dispersion attribution is also consistent with its cited scope. Previously inspected reinforcement, cooling-fin, and standard analytical sources remain appropriately attributed. The manuscript's positive, narrow contribution statements and explicit older-source access limits avoid asserting that a bounded search proves universal originality. I did not treat the audit's descriptions of uninspected full texts as independent theorem verification.

## Finding

### R5-01 — Minor: mean spatial-refinement percentage is rounded incorrectly

**Location:** `sections/07-numerics.tex`, the paragraph beginning “We refine space and offset quadrature separately”, which reports the mean-trial grid change as `0.0159%`.

**Reason:** The stored 65536-cell/48-node mean trial divided by the 32768-cell/48-node baseline, minus one, is `0.00015841231081359375`, or `0.015841231081359375%`. Rounded to four decimal places in percent, this is `0.0158%`. The discrepancy is immaterial to the stability conclusion, but the reported precision should match the data.

**Remedy:** Replace `0.0159%` by `0.0158%`, or use the conservative statement “less than 0.016%”. The other two displayed spatial-refinement percentages round consistently with the saved rows.

## Build

A fresh isolated build used `latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=<temporary directory> main.tex`. It exited with status 0, produced 54 pages, and left no warning, overfull-box, or underfull-box notice in the final log. This review inspected both figures, but does not replace the final required all-page and whole-manuscript audit.
