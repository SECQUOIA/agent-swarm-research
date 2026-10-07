# Decomposition chapter: source, proof, and scope record

Owned submission files:

- `sections/decomposition.tex`
- `appendices/decomposition-proofs.tex`

The chapter compares certificate representations under a fixed factorization and fixed local relaxation. It is not a generic decomposition algorithm or a runtime claim. There is no empirical discussion and no computational record needs archiving for this chapter.

## Main claims and reachable proofs

| Claim and label | Hypotheses and conclusion | Source mapping | Submission proof |
|---|---|---|---|
| `decomp:certificate`, `decomp:validity` | Continuous factors and continuous convex underestimators; rectangular bag leaves and separator cells, affine minorants, child/local tests. Upward induction proves minorants below exact subtree values and the root below `f_*`. Top-down substitution proves the chain inequality. | `research-20260929/theory-decomposition/decomposition-certificates.md`, Definition 1.2 and Lemmas 1.3–1.4; `AUDIT-BRANCHING.md`, Section 6. | Main chapter, complete proof of `decomp:validity`. |
| `decomp:unfolding` | One common slope on each separator; maximal bottom-up intercepts. The root is exactly the minimum of the copy-relaxed configuration value. | Source Lemma 1.5. | Appendix `app:decomp:existence`, complete recursive substitution proof. |
| `decomp:small-certificate` | Global growth `f-f_* >= c_g ||x-x*||²`, positive upper bound `H_a` for Lipschitz bag gradients, vertex-vanishing quadratic factor error, width `w`, variable occurrence `k`, child degree `Delta`, exact center and subtree-gradient slopes. Size at most `2M(4/theta)^(w+1)(J+1)` with explicit sufficient theta/h inequalities and truncated `J`. | Source Theorem 3.4, exact-center/exact-slope specialization; source Lemmas 3.1–3.2; `AUDIT-BRANCHING.md`, Section 6. | Appendix `app:decomp:existence`, full shell-grid, drift-operator, slope-cancellation, Taylor/Young/growth proof. |
| `decomp:path-separation` | Unperturbed quartic path, kappa=0.1 and b=0.8; convex unary factors exact and bilinear factors separately relaxed with alphaBB coefficient 0.4. Unique, nondegenerate interior optimum at zero; nonconvex objective. Spatial cover lower bound is the maximum of the accuracy-dependent integral bound and the exponential center-volume bound. Same-oracle path decomposition certificate has explicit `O(n log(n/epsilon))` size. | Source Sections 2.1 and 4, Corollary 2.1 and Theorem 4.1; specialized center-volume argument from `research-20260929/theory-face-exact/face-exact-exponential.md`, Theorem 1. Neither internal note is used as a manuscript citation or omitted proof. | Appendix `app:decomp:path`, full growth/Hessian facts, weighted arcsine integral, ellipsoid/determinant/Stirling bound, scalar center-volume inequality, constants, and two-regime uniform-ratio proof. |
| McCormick comparison | Same path factorization and termwise McCormick in both models. Center-volume spatial lower and certificate upper survive. Accuracy-dependent alphaBB integral and uniform-in-accuracy ratio are not transferred. | Source Theorem 4.1 variant and exact bilinear gap formulas; `AUDIT-BRANCHING.md`, Section 6. | Final paragraph of `app:decomp:path`, deriving both lower and upper McCormick gap inequalities. |
| `decomp:checking-count` | Number of local convex checks bounded by root leaves plus sum of own leaf/cell pair counts. A factor relaxation object is queried once per assigned factor/local leaf and reused. A minimization-only oracle may require a query per intersection. | Source Definition 1.2 checking remarks and Theorem 4.1 “What is counted”; `AUDIT-BRANCHING.md`, Section 6. | Main chapter, direct finite-count argument; bound `M(4/theta)^(2w+1)(J+1)^2`. |

The spatial cover bound applies separately to `N_cover`, `N_rect`, and `N_tree`; their minima are not identified. For binary spatial trees without additional reductions, terminal leaves give `2N-1` nodes. With reductions/probing the appropriate event accounting includes removed rectangular owners and virtual probe events. The appendix explicitly extends both path lower bounds to pointwise valid rectangular owners, avoiding the stale closed-frame lemma.

## Repairs and excluded interpretations

- The shell count is `J=max(0,ceil(log2(s0/h)))`; no potentially negative logarithmic count is used at large tolerance.
- The theorem explicitly takes integer `mu>=1`, needed for aligned shell-grid boundaries.
- A positive valid gradient-Lipschitz upper bound is chosen, avoiding a zero denominator in the h condition. Such a bound can be increased without changing the hypothesis.
- Continuous convex factor relaxations are assumed, so the local compact-box minima exist. The theorem does not silently invoke minimum attainment for arbitrary finite convex functions on closed boxes.
- Empty separators use the singleton in `R^0`, one cell, zero width/norm, and relative interiors. The shell lemma explicitly requires a positive side-length upper bound, so its logarithm is defined even for a zero-dimensional application.
- The exact-center result needs neither stationarity nor an interior minimizer. It does need a known global center and its gradient-defined slopes; construction without this information is outside the chapter.
- Width alone does not bound variable occurrence or conditioning. The dependence on `w`, `k`, `Delta`, `H_a/c_g`, and factor error is explicit.
- Conditional aligned checking counts are not asserted for the shell partitions. The unconditional unaligned bound has an extra logarithm. Neither convex-program counts nor factor-query counts are arithmetic/bit/runtime bounds.
- No arbitrary branching-tree localization is asserted. The October 2 counterexample in the source update disproves that unrestricted extension. GR’s separate path theorem requires stationarity and is not included.
- No later shared-coordinate-grid algorithms, recourse, bit-complexity theorems, or central contributions of `paper-decomposition-aware` are imported. Its certificates differ from the unaligned affine-cell format used here.
- No factorization-independent lower bound is claimed. Aggregation, new functional factors, and stronger relaxations/cuts can change the obstruction.
- The theorem uses `c=0` only. Root clarified that the requested amplitude distinction concerns specifically generated archived experiments, not a generic bound on linear perturbations. No mathematical or empirical conclusion about amplitude 0.3/0.2 appears in submission prose. In particular, no arbitrary `|c_i|<=0.2` interior-minimum claim is made.
- The exact exponential base is retained as `(2e/pi)^(n/2)`, never rounded upward. The uniform-ratio theorem uses an absolute unspecified positive constant, avoiding an unnecessary numerical minimization claim.

## Literature and contribution scope

Literature evidence was supplied by the Luna owner through root and the evolving `LITERATURE-KEYS.md`; no literature search or browsing was performed by this author.

- `marinescuDechter2009AndOrBranchAndBound`: discrete AND/OR branch-and-bound with reused/context-conditioned subproblems, used only as a structural precedent.
- `bienstockMunoz2018LpFormulations`: treewidth-based approximate formulations for polynomial optimization, used only for that narrower width/formulation precedent.
- The provisional Dechter–Mateescu article key was removed after root reported the source-edition mismatch. There is no article theorem locator derived from the dissertation copy.

The manuscript does not claim that exploiting decomposition or width is new. Its contribution in this chapter is the explicit comparison between spatial and local-cell certificate sizes with the factorization and termwise oracle held fixed, together with the audited existence proof and explicit size/query/checking distinctions. The specialized center-volume result is fully proved here because the geometry and face writers confirmed that they do not duplicate it.

## Audits and independent findings incorporated

Read the current `BRIEF.md`, `AUTHORING-CONVENTIONS.md`, `ARCHITECTURE-DECISION.md`, `INCOMING-AUDITS.md`, `ISSUES.md`, `AUDIT-BRANCHING.md` decomposition/scope portions, `AUDIT-SPATIAL.md` ownership portions, `ARCHITECTURE-BOUNDARY-NOTE.md`, and the relevant original model, lower, upper, separation, and scope updates. The `LITERATURE.md` file did not yet exist when checked; the current key map and root’s concrete primary-source directions determine citation scope.

A supporting independent proof checker verified the exact-center shell/drift/Taylor argument and the positive-gradient-bound/continuity details. The independent manuscript reviewer read both submitted TeX files and verified unfolding, copy cancellation, drift/growth constants, both spatial lower bounds, the scalar center inequality, and the uniform ratio. Its requested integer-mu, empty-separator, matrix-direction, positive-Lipschitz-bound, and width-wording corrections are incorporated. Root’s final separate review-resolution ledger owns the final review status.

## Targeted checks actually run

- `python3` inline exact-rational constant checks: PASS for `Q=159`, `H_0=610572/5`, theta inequalities, and safe rounding to the displayed path upper bound. This is a mathematical identity check, not an experiment or solver run.
- `python3` inline local-label/reference/proof-environment check: PASS for 39 local labels and all local references. The first checker invocation double-counted optional proof headings and failed its own assertion; the corrected checker passed without a corresponding manuscript defect.
- `git diff --check -- sections/decomposition.tex appendices/decomposition-proofs.tex`: no whitespace findings. The files were newly created, so this check was limited; standalone TeX compilation remains an integration check owned by root.

No experiments, project-wide checks, CI inspection, or edits outside the three assigned files were performed. No shared macros were added. The root already inputs both submission files. Remaining integration work: a targeted standalone TeX build and final global bibliography/review resolution.
