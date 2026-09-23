# Stage 2 author report

Author: `/root/stage02_author`. Date: 2026-09-19. Status: authored and locally checked; independent Stage 2 review pending. All authored files are inside `paper-lbesh`. Frozen research sources and records were not changed. This author spawned no subagents.

## Completed scope

The four stable section files `model-and-cuts.tex`, `separation-theory.tex`, `algorithm-and-implementation.tex`, and the theoretical portion of `oracle-diagnostics.tex` now contain complete prose, equations and proofs. The empirical diagnostic is reserved for Stage 3. Abstract, computational study, discussion, conclusions and formulation/reproducibility appendices remain later-stage work.

The accepted Stage 1 framing is preserved: a controlled comparison of established perspective cut policies. No priority for the cut family, general cut dominance, stronger limiting GDP hull, finite exact gap closure or certified numerical convergence is claimed.

## Proof coverage

| Label | Complete developed result and necessary condition |
| --- | --- |
| `eq:gdp`, `eq:hull-affine` | Original integer variables separate from native indicators; global rows on the joint box, term rows on the original-variable box; sparse-copy extension. |
| `prop:perspective` | Bounded perspective convexity/continuity, differentiated coefficients, all-tangent equivalence, and distinction between an empty positive-weight lift and the intended inactive origin. |
| `prop:poly-hull` | Both inclusions for an individual disjunction hull, including grouping convex-combination terms; finite polyhedral and all-tangent continuous-term hull; no integer/full GDP hull claim. |
| `prop:epigraph` | Optimization-equivalent compact epigraph with differentiable convex objective and no independent auxiliary-variable role. Prototype limitation stated. |
| `lem:margin` | ECP/ESH margins, anchor inequality, original/transformed normal bounds, constant-row handling. |
| `thm:integral` | Finite fixed-residual rejection by rowwise compact packing at old-cut-feasible candidates, for hull or valid big-M. |
| `thm:fractional`, `eq:safe-skip`, `eq:fixed-cutoff` | Weighted residual continuity, finite residual-calibrated separation, safe omission and denominator floor, weaker actual fixed-cutoff guarantee. |
| `prop:repair`, `ex:intersection` | Local geometric repair and weighted bounds; square-root objective-error counterexample after intersection. |
| `prop:value` | Compactness plus vanishing residuals gives value convergence, without rate; integral variant explicitly optimizes relaxations of the GDP. |
| `thm:single-tree` | Conditional complete-solver theorem with old-lazy-cut/repetition requirements, finite fractional/refinement work, incumbent validation, and distinct gap conclusion. |
| `prop:arithmetic` | Certified coefficient-error relaxation, loss of 2E plus solver tolerance, and coordinatewise sufficient error bound; full approximate-root tangent constant. |
| `prop:invariance` | Same-anchor exact-root invariance, transformed ECP formula, and same-point weakening inequality. |
| `prop:scalar` | Actual scalar master recurrence, old-cut redundancy, transient lower bound, convergence, Newton identity and fixed-parameter local quadratic expansion. |
| `ex:nondominance` | Exact off-center disk boundary and opposite witnesses with rational enclosures; centered ellipsoid formula separately confined to that geometry. |

The proofs were reconstructed from the development/review notes and checked against their assumptions. The additional Newton interpretation, same-point ECP weakening inequality and centered ellipsoid formula are explanatory elementary derivations without novelty assertions.

## Source correspondence and qualifications

Read the mathematical development and independent review, implementation development and solver review, oracle diagnostic note, research README, and relevant `solver.py`, `master.py`, `structure.py`, and benchmark-constructor paths. The accepted Stage 1 literature review supplies external antecedents; no new priority claim required another source search in this stage.

The algorithm section describes the actual frozen routines, including these distinctions:

- LP/default separation skips `lambda <= 1e-6`; optional node cuts skip `lambda <= .05`. Neither implements the residual-calibrated theorem.
- Each violated row has its own boundary search. Its boundary point need not satisfy the full multirow term.
- Both policies share interior initialization. Artificial anchor-search boxes and the slack floor are search aids, not master/model bounds.
- The radial candidate check uses an untransformed numerical margin; fallback checks finite coefficients, not a certified transformed rejection margin.
- The prototype does not automatically upper-bound its artificial epigraph, enforce old-lazy-cut-feasible generating points externally, or cap the total optional user-cut count. Corresponding theorem hypotheses are conditional.
- Multi-tree explicitly adds accepted NLP-solution tangents; single-tree submits the heuristic point and relies on callbacks.
- Internal primal acceptance is absolute `1e-6`; internal gap tolerance is `abs_tol + rel_tol*abs(U)`, with a symmetric consistency check. Stage 3 will state the distinct independent benchmark formulas.
- Failed NLPs do not exclude assignments; disabling integer-point recovery retains interior NLP work; callback time components overlap.

No defect was found that invalidates this topic or requires changing the frozen solver for the scoped computational study. Stronger exact mathematical properties are carefully separated from actual numerical implementation behavior.

## Targeted verification actually run

From the repository root:

```sh
python paper-lbesh/evidence/check_stage02.py > paper-lbesh/evidence/stage02-checks.json
```

Passed. This standard-library checker corroborates the disk formula and opposite witnesses, approximate-root constant, tangent/Newton recurrence, monotonicity/lower-bound examples at a=2,4,10,100, local disk repair, and intersection error/residual ratios. Counts to geometric error 0.1 were 3,5,10,91. It also inspects the source AST for LP/default/node cutoff paths. These checks complement rather than replace the general proofs.

From `paper-lbesh`:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex > process/stage02-build.log 2>&1
pdftotext -layout main.pdf process/stage02-manuscript.txt
```

Passed. Combined interim PDF: 19 pages. Final build has no undefined references/citations, overfull/underfull boxes or LaTeX warnings. The extracted text was inspected for theorem/equation references and proof continuity. This intermediate stage manuscript is not the completed submission.

From the repository root:

```sh
rg -n 'Warning|Overfull|Underfull|undefined|Output written' paper-lbesh/main.log
pdfinfo paper-lbesh/main.pdf
git diff --check -- paper-lbesh
```

Only the successful PDF output line matched the log query. PDF metadata confirmed 19 pages. Git whitespace checking returned clean, but these files are untracked, so an additional inline Python assertion checked trailing whitespace in all four authored section files and wrote their hashes to `process/stage02-source.sha256`.

Several path-prefix mistakes were corrected during editing/report creation and build invocation; they made no relevant edit/build. The successful commands above are the final verification. The first build temporarily referenced the reserved experimental section; replacing that formal reference by plain forward prose removed the sole undefined reference. The final build is clean.

The lead separately ran all 25 targeted publication-contract and independent solver-review tests with Ipopt present and no skips; see `process/stage02-lead-verification.md`. This author did not duplicate those checks or rerun broad benchmarks. No project-wide verification or CI inspection occurred.
