# Joint convexification: completion of the solver study

This continuation addresses the five remaining deliverables recorded in
[PROGRAM.md](PROGRAM.md): preserving native model structure, broader safe model
admission, complete positive-tolerance separation, support beyond pairs and
stars, and a new prospective evaluation. The earlier study and its unfavorable
experiment remain unchanged in
[research-20261002-convexification](../research-20261002-convexification/README.md).

The integrated [report](document/main.pdf) develops the mathematical results
and their implementation together. Its [claim map](document/COVERAGE.md)
distinguishes proofs, implemented algorithms, numerical experiments, and the
limits of each claim. Internal independent review means review by another
research agent, not external peer review or formal verification.

The main results are:

- **Cuts directly from original rows.** Joint lower support and nonnegative
  row multipliers produce certified linear inequalities in original variables.
  Native nonlinear rows and presolve remain in place. All such inequalities
  describe the projected joint-graph relaxation; this relaxation need not be
  the convex hull of the original nonlinear feasible set.
- **Exact support on general small polytopes.** Finite rational face enumeration
  minimizes any quadratic on a bounded rational polytope, including singular
  and lower-dimensional cases. Fixed dimension gives polynomial bit complexity.
  Unrestricted dimension includes MaxCut and is NP-hard.
- **Complete separation at positive tolerance.** The standalone polynomial
  graph separator returns a rational separating cut or a certified L1 distance
  bound. Its finite exhaustive fallback can be expensive. Bounded mode can
  return `unresolved`; the practical SCIP callback uses its own fixed budget.
- **Broader source-model preservation.** Exact consequences of original affine
  rows justify bounds and domains. Exact domain witnesses preserve restrictions
  hidden by cancellation. Positive-base variable powers and explicit expression
  DAGs avoid earlier importer failures. All seven historical refusals now
  import; this does not imply that every expression supports a certified cut.
- **Replay of the final solver row.** Certificates bind the original source,
  domain premises, support inequality, coefficient-rounding correction, and
  actual SCIP row. SCIP's full numerical solve is outside this certificate.

The 282-run prospective campaign is complete. All three modes solved the same
25 of 30 new holdout models. All 123 recorded cuts replayed successfully, and
all 271 returned incumbents passed the original-model numerical checks. Four
historical diagnostic runs failed during discovery and retain unknown cut logs.

The campaign exposed large-model discovery and budget-enforcement defects.
Those are repaired and independently reviewed. A separately frozen, matched
75-run validation completed without worker errors or missing cut logs. All
42 recorded cuts passed replay and all 67 returned incumbents passed their
checks. Every mode solved the same 4 of 8 affected holdout models and 4 of 7
historical cases. The cohorts remain separate; original outcomes are unchanged.
Neither comparison established additional solves from enabling cuts. Native
SCIP remains the default recommendation.

The [completion record](CLOSEOUT.md) maps each required deliverable to its
evidence. [VERIFICATION.md](VERIFICATION.md) records the actual targeted checks.

| Material | Entry point |
| --- | --- |
| Integrated report and claim map | [document/README.md](document/README.md) |
| Original-row validity and closure theorem | [theory/row-aggregation.md](theory/row-aggregation.md) |
| General quadratic support and hardness boundary | [theory/exact-support.md](theory/exact-support.md) |
| Complete separation proof and API | [theory/separation.md](theory/separation.md) |
| Model, expression, and domain contract | [numerics/model-contract.md](numerics/model-contract.md) |
| Native SCIP integration | [implementation/integration.md](implementation/integration.md) |
| Prospective evaluation and reproduction | [experiments/README.md](experiments/README.md) |
| Primary-source comparison | [literature/README.md](literature/README.md) |
| Independent review record | [reviews/PLAN.md](reviews/PLAN.md) |

The supported results do not settle arbitrary nonlinear hull construction,
efficient separation for large blocks, or exact certification of a complete
SCIP solve. The report gives explicit counterexamples and complexity boundaries
where a stronger interpretation would be false or unsupported. Completion is
assessed against the five stated deliverables, not against every possible future
research question.
