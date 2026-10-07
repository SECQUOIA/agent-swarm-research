# Claim, proof, implementation, and evidence

This map covers the authorized continuation of automatic joint convexification.
The integrated report is [main.tex](main.tex), built as [main.pdf](main.pdf).
The components below form a supported solver implementation; they do not
establish a general-purpose solver speedup or a certificate for the whole solve.

| Claim | Mathematical argument | Implementation | Evidence and boundary |
| --- | --- | --- | --- |
| Every accepted support row is valid on its supplied graph domain | Report Proposition “Support and complete hull description”; validity is preserved by convex combinations | [certified.py](../solver/certified.py) | Numerical direction search is outside the validity calculation. A finite cut collection need not describe the hull. |
| The final binary64 row, including its coefficients, has the proved interpretation | Report Proposition “Final floating-point row”; lower-bound rounding after coefficient conversion | [certified.py](../solver/certified.py), [numerical contract](../numerics/contract.md) | [kernel tests](../solver/test_certified.py) and [numerical review](../reviews/numerical-review.md). No claim about SCIP's later internal row transformations or complete dual bound. |
| Polynomial certificates cover the complete domain | Bernstein enclosure and complete partition propositions; strict affine-row exclusion | [certified.py](../solver/certified.py) | Exact rational arithmetic; replay rejects omitted branches, altered bounds, false exclusions, and changed models. One- and two-variable fallback, capped degree and tensor size. |
| Supported elementary functions retain every required endpoint and domain cell | Outward interval evaluation and optional rigorous curvature correction | [certified.py](../solver/certified.py), [numerical contract](../numerics/contract.md) | Kernel tests include tiny invalid slivers, singular derivative endpoints, zero-weight invalid features, and retained reciprocal cancellation. Requires Arb and the stored expression; cannot recover a domain already erased upstream. |
| A small certified residual rules out large normalized support violations | Report Theorem “Normalized violation screening”, from a verified convex combination and Hölder's inequality | [screening.py](../solver/screening.py), [screening note](../implementation/screening.md) | [screening tests](../solver/test_screening.py). Norm and coefficient normalization must match. Positive tolerance proves neither hull membership nor original feasibility; integration screens only source polynomials. |
| A rational quadratic vector over a rational polygon has exact rational support | Report Theorem “Finite rational support candidates”; boundary minima and singular-Hessian reduction | [quadratic_polygon.py](../theory/quadratic_polygon.py) | [pair tests](../theory/test_quadratic_polygon.py). Includes empty, segment, and singleton domains. Exact support does not imply complete numerical direction search. |
| Affine center–leaf rows preserve exact quadratic-star support | Report Theorem “Exact rational star support”; piecewise affine leaf minimizers and quadratic value pieces | [quadratic_star.py](../theory/quadratic_star.py) | [star tests](../theory/test_quadratic_star.py), [theory note](../theory/README.md). Arbitrary leaf–leaf rows and products are outside this class. Box-only tractability is prior forest-QP work. |
| Merging specified pair directions gives an exact, sharp constant improvement | Report Corollary “Sharp gain for specified pair directions”; equality iff projected minimizing sets intersect | Pair and star exact support APIs | The exact diagnostic is meaningful for the specified normals. It neither chooses all useful normals nor predicts runtime benefit. |
| Exact pair hulls can remain weaker than their assembled sparse quadratic hull | Report Proposition “A strict pair-hull gap”; rational two-measure witness and sharp minimum 1/128 | [overlap note](../theory/overlap-review.md), star oracle | [Exact replayed mechanism](../experiments/star-mechanism.json). The witness satisfies full pair hulls, not only scalar relaxations. Dense PSD plus nonedge RLT can also exclude it; no general dominance claim. |
| Full separator distributions permit tree gluing | Conditional-measure construction under running intersection | Mathematical comparison in [overlap note](../theory/overlap-review.md) | Established measure-consistency theory. Finite first and second moments do not imply the premise for a continuous separator. |
| Automatic separation preserves native nonlinear enforcement | Root-global cuts, original finite boxes, source-tree auxiliary definitions, retained native constraints | [integration.py](../solver/integration.py) | Common reformulation control and original-model checks distinguish representation effects. Automatic activation is a bounded heuristic, not a universal dominance rule. |
| Source expressions and actual inserted native rows are checked at the declared trust boundary | Source-domain restrictions proved on the declared box; exact algebraic comparison of stored binary coefficients; exact column, side, constant, and locality comparison before insertion | [model_binding.py](../solver/model_binding.py), [integration.py](../solver/integration.py) | [model-binding tests](../solver/test_model_binding.py), [source-model review tests](../reviews/test_source_model_review.py). All modes reject unproved source domains or unequal whole-row imports; individual auxiliary and rewritten-row rejections preserve original native expressions. This can exclude valid models with broad declared bounds or ordinary decimal-coefficient folding and does not certify later presolve. |
| A C component accelerates appropriate repeated polynomial sampling | Shared-power evaluation; both outputs are only numerical proposals | [native_sampling.py](../solver/native_sampling.py), [native_sampling.c](../solver/native_sampling.c) | [retained benchmark](../implementation/native-kernel-benchmark.json), [native note](../implementation/native-kernel.md), [tests](../solver/test_native_sampling.py). Low-degree and small-array losses are retained. This is not a native SCIP handler or a solver-speed theorem. |
| Computational comparisons separate new cuts from reformulation and retain unfavorable outcomes | Frozen baseline/control/all/auto protocol and independent original-model residual checks | [campaign runner](../experiments/run_campaign.py), [worker](../experiments/worker.py), [case evaluator](../experiments/cases.py) | [protocol](../experiments/protocol.md), [held-out selection](../experiments/holdout-selection.json). Short shared-host runs cannot establish a broad population effect; numerical residual checks are not exact feasibility certificates. |
| Attribution reflects relevant prior results | Inspected primary texts with theorem/version locators | [literature audit](../literature/README.md), [composition audit](../literature/composition-audit.md), [star audit](../literature/star-overlap.md) | [source manifest](../literature/sources/MANIFEST.md), [bibliography](../literature/references.bib). Limited retrieval and source-inspection scope are explicit; no publication-priority claim. |

The proofs justify universal claims under their stated assumptions. Finite tests
provide distinct implementation evidence, including alternative formulations
and tampering cases; they do not replace those proofs. Internal research-agent
review is distinguished from formal verification and journal peer review.

Two additional star audits use different checks: [full-space stationary-face
enumeration](../theory/star-audit.md) compares 155 cases, while
[whole-interval conditional-rule checking](../reviews/star-review.md) compares
88 cases and 786 complete center intervals. Their scripts and saved outputs
are linked from those records. These complement the implementation's targeted
tests rather than repeating its support algorithm as an oracle.

The report incorporates the [316-run summary](../experiments/campaign-v1/summary.json),
[raw records](../experiments/campaign-v1/records.jsonl), and
[fresh-process replay](../experiments/campaign-v1/replay.json). All 1,082 recorded
cuts pass; eight worker errors lack model/cut logs and retain unknown logged
cut counts. The negative held-out outcome is explicit: 19 solved by native
baseline/control versus 18 by either cut mode among 20 admitted models from
24 selected. Three common domain refusals and one unsupported variable-exponent
model are importer limitations, not native SCIP failures. Default activation
is not supported by this experiment. Historical experiments remain separate
and are not relabeled as certified results of the new kernel.

The [experiment interpretation and reproduction record](../experiments/README.md)
explains the import refusals, adverse solver outcomes, timing coverage, and
combined reuse-policy ablation. The [independent metrics audit](../experiments/experiment-audit.md)
and its [saved checks](../experiments/campaign-v1/experiment-audit-results.json)
verify the selected/admitted denominators and recorded totals. The
[final document review](../reviews/document-review.md) and
[its direct evidence checks](../reviews/document-evidence-checks.json) assess
the manuscript against raw records. The
[final contribution review](../literature/final-contribution-review.md) checks
attribution and novelty boundaries against the actual report.
