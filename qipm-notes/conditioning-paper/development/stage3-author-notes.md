# Stage 3 author record

Author: `stage3_examples_author`. Status: five independent reviews completed
with no major issues. The distinct agent `stage1_fixer` corrected both accepted
minor findings; see `stage3-corrections.md` for the terminology audit and
additional source comparison.

## Delivered sections

- `sections/05-classifications.tex`: error-bound and attained-diameter dictionary
  for every fixed barrier; elementary polytope classification including
  degenerate vertices; explicit curved 2-by-2 spectrahedron; a uniform
  near-optimal-edge simplex plateau and its exact iterated limit.
- `sections/06-lp-limits.tex`: the classical positive scaled-Hessian limit at
  a unique LP optimum, its active-set formula and quantitative bounds, an
  explicit compact degenerate example, and the repository's exact unbounded
  degenerate witness with compact objective sublevels.
- `sections/07-fractional-sdp.tex`: the classical trace-normalized Sturm
  construction; sharp diameter proofs for it and its block-diagonal section;
  exact minimal two-step facial reduction for both optimality systems;
  failure of strict complementarity despite primal and dual strict
  feasibility; the exact central path and four reduced log-Hessian
  eigenvalue constants; the two-eigenvalue restricted calculation; and
  all-barrier transfer at equal gap.
- `main.tex` includes the three sections. The bibliography adds
  Drusvyatskiy–Wolkowicz 2017 and Wei–Wolkowicz 2010.

The original paper, workbench, literature corpus, and unrelated
`central-path-cost/` directory were not changed. The author did not delegate.
The remaining front matter, solver sections, numerical section and final
synthesis belong to later authorized stages.

## Mathematical decisions and independent verification

1. The general law retains `D(g)` even if no power-law asymptotic exists.
   The examples are not an exhaustive classification of all convex sets.
   For compact LPs, however, the only asymptotic condition exponents are
   zero (singleton optimum) and two (positive-dimensional optimal face).
   A finite-range intermediate slope is explicitly distinguished from a
   fractional asymptotic LP rate.
2. The upper error bound is not used as a lower conditioning bound. Matching
   conditioning exponents require matching sublevel diameters. Uniform
   approximate-center statements explicitly require a fixed residual bound
   strictly less than one.
3. The simplex's instance constants are uniform: fixed interior ball,
   objective range one, and projected objective squared norm in `[1/2,2/3]`.
   This removes the canonical-tail assumptions required by the original
   paper's weaker upper-bound theorem. The exact `4/3` plateau statement
   is an iterated limit, distinct from the uniform joint estimate.
4. The unique-LP limiting Hessian is an immediate consequence of the
   classical centered dual endpoint and exact complementarity. Uniqueness
   makes `A_B` full column rank and `R_N W` injective even when `|B|<m`.
   No primal nondegeneracy assumption is introduced. Every active-set
   eigenvalue and condition inequality follows from the displayed Loewner
   sandwich, with no change of external metric.
5. The compact LP example's explicit nonorthonormal basis `T` has Gram
   matrix `[[14/9,1],[1,6]]`. Its generalized eigenvalues equal those from
   an independently constructed orthonormal nullspace basis.
6. The fractional SDP's four coordinates split orthogonally into `(b,g)`
   and `(X13,X23)` blocks. For the latter, the Frobenius metric cancels
   the factor two in the log-det second derivative. For the former,
   the Gram matrix is `[[4,1],[1,2]]`. Its large generalized eigenvalue
   constant is `4/7`; its determinant gives the smaller constant one.
   The resulting ordered constants are `(sqrt(2),1,sqrt(2),4/7)` at
   exponents `(1/2,1,3/2,2)`. The condition constant is `2sqrt(2)/7`
   in μ and `3sqrt(3)/7` in gap. The block-diagonal problem retains
   the middle-coordinate block with condition constants `4/7` in μ
   and `6/7` in gap.
7. The singularity degree is explicitly that of the optimality system,
   including `X22=0`. Both original feasible systems are strictly
   feasible and have degree zero. In both optimality systems every
   first-step PSD equality combination is a multiple of `E22`; it
   cannot expose the final rank-one face. The displayed two-step chain
   is therefore minimal. Adding `X13=X23=0` retains degree two but
   changes the diameter and conditioning exponents, rigorously showing
   that degree alone does not determine them.

## Source inspection and novelty status

- Read the current original conditioning section, the relevant spectrum
  discussion, the active degenerate-LP workbench note, the Stage 1 scope
  audit, the Stage 2 sources and author/correction record, and the root's
  mathematical leads. Leads were independently derived in the manuscript;
  their numerical values were not used as proofs.
- Adler–Monteiro 1991 local full text: Theorem 3.3 and its discussion give
  the dual centered endpoint (printed page 41 in the extracted source);
  Theorem 5.1 and printed pages 44–45 give endpoint derivative behavior
  and explicitly note full column rank at a unique primal optimum.
  The manuscript uses the precise centered-limit theorem and proves the
  compressed-Hessian corollary. It does not advertise this classical
  consequence as novel.
- Drusvyatskiy–Wolkowicz 2017 local full text: Definition 4.2.1,
  Theorem 4.5.1, Example 4.5.2, and Section 4.7 establish the facial
  reduction definition, compact-set Hölder bound, nested worst-case
  construction, and attribution to Sturm. Publisher DOI metadata was
  independently checked online at https://doi.org/10.1561/2400000011;
  volume 3(2), pages 77–170, publication year 2017. Some older preprint
  metadata says 2016 and numbers the example differently; those are not
  used for the journal citation.
- Sturm 2000 local text: Example 2, printed page 1244, and the preceding
  discussion were inspected. Its extracted displayed equations are
  incomplete. Root separately checked the original PDF equation; the
  Drusvyatskiy–Wolkowicz primary full text independently spells out the
  same chain constraints and attributes it to Sturm. The manuscript
  credits the construction and quarter-power geometry as classical.
- The Stage 1 detailed Alizadeh–Haeberly–Overton comparison was read:
  their Section 4 addresses a Schur matrix in the strict-complementarity
  setting, not the reduced primal log-det Hessian used here. The text
  makes the matrix, scaling, metric, and regularity distinctions explicit.
- Targeted online searches for Sturm, central-path Hessians, quarter-power
  spectra, four eigenvalues, and the explicit constants did not identify
  a statement of these four constants. This is not an exhaustive priority
  proof. The qualified novelty sentence names only the exact reduced
  spectrum for the trace-normalized classical construction, followed by
  the all-barrier transfer. It claims neither a first fractional SDP
  example nor first SDP spectral clustering.
- Wei–Wolkowicz 2010 was screened after search results surfaced it. Its
  local extraction has broken font encoding, so no theorem-level claim
  relies on that text. The primary author-submitted abstract at
  https://optimization-online.org/2006/01/1291/ confirms the generator
  for non-strictly-complementary SDP instances and empirical difficulty
  measures. Only that broad, accurate relationship is cited. Journal
  metadata in the existing local package is consistent with DOI
  10.1007/s10107-008-0256-3. The temporary full-text extraction was removed.

## Verification commands and results

From `conditioning-paper/`:

```sh
/workspace/local-home/miniconda3/envs/qipm/bin/python development/stage3_verify.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The verification script is retained in `development/` as an author audit,
not as the final Stage 5 numerical package. It uses Python `decimal` at
70 digits plus NumPy/SciPy, with no added dependencies. It verifies PSD
feasibility of the explicit diameter witnesses, centrality of the exact
matrix center, and full Hessian trace products against the analytic block
formulas. At gaps `1e-2`, `1e-4`, and `1e-6`, maximum relative eigenvalue
discrepancy between the independently assembled float64 matrix and stable
Decimal formulas was less than `7e-16`; the scaled tangent centrality
residual was less than `1e-16`.

At gap `1e-24`, scaled ordered eigenvalues were approximately
`(1.4142135623749321, 1.0000000000010103, 1.4142135623741157,
0.5714285714289014)`, and `kappa*mu^(3/2)` was
`0.40406101782059267`. The compact LP computation gave eigenvalues
`(0.24888159957939374,1.1428906151565694)` and condition number
`4.592105712467446`, agreeing between orthonormal and generalized
coordinate formulations.

The integrated manuscript builds to 20 pages at this stage. Final build
log contains no undefined references/citations, overfull boxes, or other
LaTeX warnings. Root identified and the author corrected three minor
draft issues before submission to reviewers: the uniform residual wording,
three lost TeX backslashes, and wording that wrongly described the scalar
diameter as retaining directional information.
