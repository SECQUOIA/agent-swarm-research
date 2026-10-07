# Manuscript coverage and development map

This map records the scope of the paper. The manuscript contains the statements
and proofs; this file is not a substitute for them. The original studies and
experimental source bytes are preserved in the companion.

| Original result or topic | Manuscript location | Treatment |
| --- | --- | --- |
| September Lemma 1: validity and monotonicity | `foundations.tex`, `lem:order` | Whole-family hypotheses and support attainment explicit. |
| September Propositions 2–3: scalar contraction | `local-rates.tex`, `prop:sharp-growth`, `prop:quadratic-growth` | Full proofs; sufficient thresholds distinguished from necessary conditions. |
| September Theorem 4 and Corollary 5: tangent contraction | `local-rates.tex`, `ass:tangent`, `thm:tangent-contraction`, `cor:tangent-rate` | Shape map and comparison factor defined; cutoff enclosure and local-entry assumptions stated. |
| September Theorem 6: stalling | `local-rates.tex`, `thm:local-stall`, `cor:face-test` | Strict face witnesses required when the expansion has a remainder; tests not presented as an exhaustive classification. |
| September Proposition 7: two-variable quadratic | `local-rates.tex`, `prop:two-variable-rate` and following propositions | Exact symmetric rate, rectangular maps, eigenboxes, cutoff limit, and arbitrary interior-box geometric rate; no unsupported successive-ratio limit. |
| September Proposition 8: row stall | `local-rates.tex`, `prop:quadratic-rows` and examples | Full proof; signed and diagonally dominant strongly convex examples; exact complete-graph cube criterion. |
| September Corollary 9: relaxation gap after tightening | `local-rates.tex`, `cor:local-gap` | Full proof under the contraction hypotheses. |
| September Lemma 10: original sublevel hull | `foundations.tex`, `lem:sublevel-hull` | Hull and protected box independently lie inside the iteration limit. |
| September Proposition 11: boundary minimum | `local-rates.tex`, `thm:boundary`; `local-proofs.tex` | Repaired terminal case; geometric upper enclosure rather than contraction of each actual free gauge. |
| September Theorem 12: factorable expansion | `local-rates.tex`, `thm:composite-expansion`; `local-proofs.tex` | Complete coefficient recursion and proof, including degenerate intervals, clipping, and critical scalar factors. |
| Jacobi, directional, and selective schedules | `foundations.tex` | Round sandwich and fair-schedule intersection; fixedness needs additional continuity. |
| October current-round screens and protected boxes | `certificates.tex` | Finite witnesses, rebuilt-row check, operation scope, objective ceilings, exact fixed-box completeness, and discovery limitations. |
| Cutoff mixing and cached frontiers | `cutoff.tex` | Complete proofs, pair-mixture candidates, precise reuse conditions and cutoff response. |
| Remaining movement from a residual | `residual.tex` | Ordered-pair majorant on an invariant region; checked supersolution; valid upper-residual after-round ceiling; least majorant without unnecessary spectral premise. |
| Coupled constraints and dual information | `constraints.tex` | Fixed-matrix dual envelopes and basis regions; rebuilt-row limitations and residual correction. |
| Uniform matrix across active regimes | `constraints.tex`, `parametric-proofs.tex` | Complete region coverage and an exact finite strict-violation test, with possible combinatorial cost stated. |
| Nonlinear feasible repair | `constraints.tex` | Full conditional transfer theorem; explicit graph example with improved proved rate bound. |
| Exact finite closure implementation | `algorithms.tex` | Exact primal–dual verification, committed-round contract, statuses, certificate persistence, and archived fixtures. |
| Numerical integrated policy | `algorithms.tex`, `numerical-validation.tex` | Frozen relaxation, current-round screening, row/dual validation, incumbent contract and heuristic selection. Strong future-round certificates are not implemented by this policy. |
| Effort and baseline comparison | `effort.tex`, `scheduling.tex` | Serial admission accounting, independent-baseline limits and scheduling guarantees; established mathematical ingredients credited. |
| September external presolve study | `experiments.tex`, `precursor-study.tex` | Separate precursor; corrected solve counts and precise saved-trajectory classifications; original descriptive timing conventions identified. |
| October 120-run comparison | `experiments.tex` | Frozen protocol, all runs, numerical incumbent validation, LP/callback cost decomposition and qualified negative finding. |

Additional analytic developments include sharp same-box cutoff thresholds,
finite rational face-certificate completeness, exact positive complete-graph
cube rates, a robust signed three-variable stall, a complete basis-cover test,
and an improved nonlinear graph estimate. A critical scalar example shows
sublinear contraction and a cubic-root cutoff floor at the borderline
comparison factor one. These additions are derived analytically; no numerical
experiment was rerun.

The literature audit distinguishes original OBBT formulations and explicit
model-specific results from classical monotonicity, convex-hull, contraction,
error-bound, and parametric-LP arguments. The measured policy tests its own
scheduling and costs, rather than the computational value of the stronger
certificates.
