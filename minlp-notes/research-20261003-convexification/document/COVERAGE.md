# Claim, implementation, and evidence map

This map is maintained with the integrated report. Final source hashes and
actual checks belong in the independent review and verification records.
The prospective 282-job campaign and separate 75-job correction cohort are
complete, with original-model-bound replay and independent numerical and
metric checks. Semantic and mathematical reviews are recorded separately
from full-document consistency review; none is external peer review or
formal verification.

| Claim | Proof | Implementation | Evidence and boundary |
| --- | --- | --- | --- |
| Joint lower support gives valid graph-hull cuts | Support proposition in `foundations.tex` | Inherited certified kernel and current exact support APIs | Final coefficient and original-domain binding remain necessary. |
| Direct cuts preserve the original nonlinear formulation | Original-variable support proposition in `aggregation.tex` | [Integration](../solver/integration.py), [row certificate](../solver/row_certificate.py), [contract](../implementation/integration.md) | [Integration review](../reviews/integration-review.md) checks model/source reconstruction and actual SCIP rows. A bounded proposal search need not produce all useful cuts. |
| All direct support rows describe the projected joint graph relaxation | Closure theorem in `aggregation.tex` | Formulation theorem | This closure need not equal the convex hull of original feasible points. |
| Rounding after elimination preserves validity | Safe-export proposition in `aggregation.tex` | `solver/row_certificate.py` | Bounds used in the correction require independent model provenance; tiny separation can be lost. |
| Bounded rational-polytope quadratic support is exact | Complete finite support theorem in `polytope.tex` | [Exact oracle](../theory/quadratic_polytope.py), [contract](../theory/exact-support.md) | 34 targeted tests and [40 independent diagnostics](../theory/polytope-review.md). Fixed-dimension polynomial bit complexity; unrestricted dimension can be exponential. |
| Affine-constrained stars have polynomial exact support | Star theorem in `star.tex` | Inherited `quadratic_star.py` | No general leaf--leaf coupling in this specialized algorithm. The new polytope oracle covers bounded small unions. |
| Pair hulls need not compose, even with common first and second moments | Explicit `1/128` obstruction in `overlap.tex` | Inherited exact star diagnostic | Dense moment relaxations with nonedge products can exclude the same witness. |
| A finite complete positive-tolerance separator exists and has defined output semantics | `separation.tex`, [complete argument](../theory/separation.md) | [Separation API](../solver/separation.py) | 16 owner tests and [21 independent checks](../reviews/separation-review.md); theorem and implementation reviewed. Resource exhaustion differs from a near-hull certificate; costs can be exponential. |
| Source domains and native expressions remain bound to the admitted model | Source-domain projection identities and affine-bound proposition in `implementation.tex` | [Model builder](../solver/model.py), [bounds](../solver/bounds.py), [contract](../numerics/model-contract.md) | [Independent model review](../reviews/model-review.md), retained seven-model admission artifact. No claim about later SCIP transformations or whole-solve certification. |
| The frozen integration is evaluated prospectively on a new sample | `evidence.tex` | [282-run results](../experiments/campaign-v2/results.md), [raw summary](../experiments/campaign-v2/summary.json), [coverage](../experiments/campaign-v2/coverage.md) | Same 25 of 30 selected applications solved in every mode, with greater summed cut-mode time. All 123 recorded cuts replay; four worker errors retain unknown logs. All 271 incumbents pass numerical checks. Native SCIP remains the default. |
| Corrected sparse discovery and budget checks are validated separately | Defined discovery-incomplete contract in `implementation.tex`; correction history in `evidence.tex` | [Correction protocol](../experiments/repair-protocol.md), [fixed plan](../experiments/repair-plan.json), [75 matched results](../experiments/repair-discovery-v1/results.md), [replay](../experiments/repair-discovery-v1/replay.json) | Focused corrected-code suite passes 81 tests and three subtests. All 42 recorded repair cuts replay and all 67 returned incumbents pass numerical checks, with no errors or unknown logs. The former four crashing runs decline unfinished discovery and continue native SCIP. There are no extra solves. These selected correction runs do not replace the prospective sample. |
| Mathematical and computational frontiers are explicit | Explicit MaxCut reduction in `frontier.tex` and closure counterexample in `aggregation.tex` | Defined return statuses and resource guards | General support includes NP-hard problems; complete graph separation does not give the feasible-set hull; finite tests do not establish general speedup. |
| Attribution distinguishes established methods from this implementation | `literature.tex` | [New primary-source audit](../literature/README.md) and [aggregation audit](../literature/aggregation-prior.md) | No publication-priority claim; inspected source scope and inherited provenance are recorded. |

Across the two current campaigns, all **165 recorded cuts** passed replay
and all **338 returned incumbents** passed numerical checks. The four original
missing cut logs remain unknown and are outside successful replay coverage.
These are counts of records, not unique inequalities or unique instances.
The first continuation's 1,082 replayed cuts are separate historical evidence.

The [final contribution review](../literature/final-contribution-review.md),
[integration review](../reviews/integration-review.md), and
[experiment review](../reviews/experiment-review.md) state their actual
review scopes and source identities. The [verification record](VERIFICATION.md)
covers this report's build, references, and local evidence links.
