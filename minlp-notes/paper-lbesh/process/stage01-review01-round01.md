# Stage 1 independent review 01, round 01

Reviewer: `/root/reviewer01`. Date: 19 September 2026.

## Verdict

**No major issues found. Two minor corrections are required before closing this stage.** The contribution is defensible as a controlled computational comparison with mathematical contracts and diagnostics, rather than a new general algorithm or cut family. The existing prior-work boundaries are unusually explicit and appropriately limit the conclusions. This verdict concerns the completed Stage 1 scope; it does not certify proofs or numerical tables that have not yet been written.

I did not read any other current review report, edit manuscript sources, or spawn agents.

## Required corrections

1. **Minor — qualify the hull-specific implementation statements.** `sections/related-work.tex:12` says that “Our ECP and ESH variants choose different” tangent points in the displayed perspective inequality; line 17 then says that “The present implementation instead maintains disaggregated variables.” Both statements are accurate for the hull variants but unqualified for a study expressly including big-M (`sections/introduction.tex:6`). The big-M master uses original variables and a deactivated tangent inequality, not the displayed perspective inequality: see `code/minlp_solver_lab/lbesh/master.py:85` (copies only in the hull branch) and `:153` onward (`cut_expr_disjunct`, whose big-M branch returns the original-variable expression against `M * (1 - lam)`). Change these phrases to “Our hull ECP and ESH variants…” and “Our hull implementation…”; briefly identify the big-M alternative in the surrounding prose if helpful. This is a local scope ambiguity, not an invalid mathematical construction or a reason for more experiments.

2. **Minor — name the timing statistic in the introductory numerical claim.** `sections/introduction.tex:12` calls the 4–6% figures “Common-solved timing averages.” The underlying statistic is a one-second shifted geometric mean, not an unspecified average: `notes/lbesh-study-results.md:93`–`:104`, and the repetition table at `:154`. Say “common-solved shifted geometric mean times” (and specify wall time if space permits). The reported direction and approximate magnitudes agree with the notes. No recalculation or new study is required for this wording correction.

## Scientific and coverage assessment

- The perspective tangent displayed in `related-work.tex:9`–`:10` is correct. For any positive base weight and base copy equal to that weight times z, differentiating the perspective gives the stated x-gradient and lambda coefficient, with zero affine constant after cancellation. The wording correctly restricts direct perspective differentiation to positive weights.
- The CEHR constraints in `related-work.tex:24`–`:25` are consistent with the primary version-2 source and the bounded-domain perspective target. For positive lambda, eliminating t recovers the quadratic perspective row. At zero weight, scaled finite bounds force the copy to zero; t=0 is admissible. The later mathematical section should retain the coverage map's explicit empty-disjunct convention, but the Stage 1 summary does not contradict it.
- The manuscript correctly distinguishes separate-disjunction hull intersections from the full GDP hull, and does not infer finite termination of an objective-gap certificate from fixed-residual separation.
- The description of Kronqvist–Misener is faithful to the primary manuscript: fixed-normal termwise convex optimization, ESH integration, and no requirement to evaluate nonlinear perspectives directly. The paper does not wrongly claim that ESH plus disjunctions or avoiding perspective division is new.
- Serrano–Schwarz–Gleixner already supply the gauge/ESH explanation. The manuscript acknowledges that the representation diagnostic is a restricted executable illustration. No foundational novelty is claimed.
- The prominent limitations are proportionate: NLP assistance, common ECP interior initialization, related generated controls, unchanged solver seed, descriptive numerical acceptance, equal external solve counts, and a missing general conic OA comparison. There is no unsupported broad superiority or first-ever priority claim.
- Introduction cohort sizes, held-out accepted solve counts, external equality of accepted counts, and the 69/72 versus 1/72 ablation statement agree with the checked source notes. This review did not repeat the raw numerical audit.
- The coverage map accounts for the relevant theory, implementation, diagnostics, generators, references, failures, and followups. Reserved later sections are intentional and are not findings.
- Bibliography/scaffold/README are coherent for an interim anonymous manuscript. Publication metadata and accessibility will still need the planned final-stage treatment; their absence now is not a Stage 1 defect.

## Optional improvement, not a required fix or new research demand

A direct reference to Veinott's 1967 supporting-hyperplane paper could accompany `related-work.tex:15`, instead of reaching that history solely through Serrano et al. The current statement is accurately sourced through Serrano and makes no misleading priority attribution, so I do not classify this as a missing crucial precedent. No additional solver baseline, broad novelty claim, or independent implementation is required to support the stated Stage 1 scope.

## Checks actually performed

- Read all of `main.tex`, the two authored sections, `references.bib`, `README.md`, `process/stage01-author.md`, `evidence/coverage.md`, and `evidence/literature.md` using `nl -ba`/`sed`.
- Used targeted `rg` and `sed` reads of `notes/lbesh-study-results.md`, `notes/lbesh-publication-readiness.md`, `notes/lbesh-development-literature.md`, `notes/lbesh-development-theory.md`, and `code/minlp_solver_lab/lbesh/master.py`/`solver.py` to check numerical summaries, assumptions, and formulation distinctions.
- Ran a short Python bibliography/input check: 16 bibliography entries, 16 distinct keys, no missing cited keys, no uncited entries, and 13 section inputs. Passed.
- Inspected primary sources online: [Kronqvist–Misener author manuscript](https://optimization-online.org/wp-content/uploads/2020/08/7957.pdf), [Gusev–Bernal Neira version 2](https://arxiv.org/html/2508.16093v2), and [Serrano–Schwarz–Gleixner publisher article](https://link.springer.com/article/10.1007/s10898-020-00906-y). Checked the strengthening construction, CEHR formulation context, and supporting-hyperplane/gauge history respectively.
- Ran online related-work searches for `"logic-based" "extended supporting hyperplane"`, `"GDP" "ESH" "ECP" perspective comparison`, and `"extended supporting hyperplane" "perspective cuts" disjunctive`. No additional crucial omission was established; unsuccessful search results are not evidence of novelty. Technical conclusions above rely on primary sources, not third-party summaries.
- Did not rebuild TeX, run optimizer experiments, run project-wide verification, inspect CI, or rerun the raw-data audit. The author's recorded successful targeted build is not presented as my own execution.
