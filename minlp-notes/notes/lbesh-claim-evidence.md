# LB-ESH claim and evidence register

This register separates mathematical statements, implementation contracts,
and numerical findings. It is a preparation aid for a manuscript, not a
manuscript or a claim of editorial acceptance. All declared experiment batches,
the final numerical audit, derived-table review, and fresh scientific review
are complete and accepted within the scope below.

| Permitted statement | Evidence and scope |
| --- | --- |
| A disjunct-level radial tangent produces a perspective OA inequality. | The identity and closed bounded-disjunct formulation are proved in [the theory note](lbesh-development-theory.md) and checked in [the independent review](lbesh-review-theory.md). This identifies an established cut family; it does not establish novelty. |
| Radial separation can be less sensitive than point tangents to equivalent constraint formulas. | The scalar construction, disk/ellipsoid diagnostic, and actual frozen oracle establish this for the stated transformations, anchors, and test grid. See [the diagnostic](lbesh-oracle-diagnostic.md) and [fresh review](lbesh-review-oracle-diagnostic.md). Finite-precision invariance is measured, not assumed universally. |
| Fewer radial cuts can require more function evaluations. | The diagnostic records real bisection evaluations and both policies' function/gradient calls. This is an oracle-cost observation, not a GDP runtime conclusion. |
| Neither policy's individual cuts uniformly dominate the other's. | Explicit off-center convex-set witnesses are proved and checked by support functions. Dominance depends on the anchor and candidate geometry. |
| Fixed-tolerance exact separation terminates under the stated compactness and bounded-gradient assumptions. | The packing proof has explicit strict-separation and cut-retention conditions. Floating-point root searches and a solver's status do not constitute an exact-arithmetic proof for a run. |
| A residual-calibrated fractional rule has a safe small-weight omission criterion. | The theory treats weighted residuals and a bound on the row over its compact domain. This is a proposed rule, not the fixed-cutoff implementation evaluated in the frozen study. |
| Approximate separate-disjunction hull feasibility admits a local geometric repair bound under the stated assumptions. | The proof concerns one disjunction. Intersecting repaired points with global constraints requires additional regularity; the counterexample rules out a general linear objective-error inference. |
| The implementation rejects documented unsupported GDP structures and revalidates numerical incumbents. | [Implementation scope](lbesh-development-implementation.md), [independent solver review](lbesh-review-solver.md), and targeted regression tests. Convexity remains an input assumption; this is not an automatic convexity recognizer. |
| The generated instances are reproducible, feasible, bounded, and convex in the specified domains. | [Instance construction](lbesh-development-instances.md) and [independent verification](lbesh-review-instances.md). The 51 instances have two principal structures, shared parameters, related sizes, and few seeds; they are not 51 independent applications. |
| The cone references use exact mathematical formulations of their supported models. | [Quadratic conic formulation](lbesh-development-conic.md), [general cone reference](lbesh-development-general-conic.md), and their independent reviews. Solver outputs are floating-point estimates. Unsupported inputs are refused. |
| The legacy collection supplies external numerical context with qualified mathematical scope. | [Fresh legacy scope audit](lbesh-legacy-scope-audit.md). Eight extracted models meet compact/smooth data assumptions, six need an epigraph argument, and thirteen are broader stress cases. This classification does not by itself verify every convergence-theorem assumption. |
| A run is numerically solved only when its original GDP witness passes and its usable global bound closes the declared gap. | [Frozen protocol](lbesh-study-protocol.md), [harness review](lbesh-review-harness.md), and final revalidation/contradiction audit. Consensus or a raw optimal status is insufficient. |

## Numerical claims supported by the completed study

The [results note](lbesh-study-results.md) supplies the exact cohorts,
denominators, and reproducible tables. These are descriptive results for
the specified instances and configurations.

| Permitted statement | Evidence and limit |
| --- | --- |
| Single-tree ESH has a modest, repeatable advantage in the generated held-out comparison. | All three runs solve 33/33 with each formulation, versus ECP's 32/33 hull and 31/33 big-M. Common-solved shifted wall means favor ESH by about 4–6%. Timing repeats use the same solver seed and related instances; they establish neither independent replication across applications nor uniform instance-level gains. |
| ESH trades fewer cuts and LP iterations for more expensive separation. | The paired work measurements and actual-oracle diagnostic support this observation. NLP and node reductions are arithmetic-mean effects concentrated in harder cases; some medians are tied or worse. This is not a causal decomposition of total runtime. |
| Formulation and tree policy have larger measured effects than the oracle choice in these controls. | The common-solved structure comparisons retain their exact memberships. They do not establish that hull or single-tree policies always win. |
| The exact quadratic conic baseline is substantially faster on its supported generated subset. | Nine of nine numerical solves, about 0.46-second shifted wall mean versus 2.28 seconds for ESH hull single-tree. This unfavorable result remains part of the study. |
| The legacy results show no ESH advantage in accepted solve counts. | Matched configurations have equal counts; common-solved timing differences are small and mixed. This external study is unrepeated, and its scope strata include nonsmooth and unbounded-auxiliary stress cases. |
| Integer-point NLP recovery is important to the tested prototype. | The NLP-disabled ablation solves 1/72 versus 69/72 matched primary runs. Fresh diagnosis distinguishes missing incumbents from open gaps and finds no false optimality/infeasibility claims. It does not establish a mathematical requirement for NLP solves. |
| Continuous conic roots and exhaustive small enumerations independently check the numerical targets. | Forty roots are reported optimal, two optimal inaccurate; precision claims distinguish these groups. All 174 optimal assignment witnesses revalidate. Cone outputs remain numerical estimates and do not supply a general mixed-integer runtime baseline. |
| Solver options and interface initialization affect numerical acceptance. | Separate, declared 9-run and 24-run follow-ups preserve original results and checker tolerances. They are not pooled into a best-of solver score. Missing exported bounds, invalid witnesses, and open gaps remain distinguishable outcomes. |

The matched ECP control shares ESH's interior initialization. These questions
compare cut-point policies within one implementation, not independently
optimized ESH and ECP solvers. Continuous cone roots are relaxation references,
not mixed-integer runtime baselines. Solver component times that overlap
must not be added. Repetitions use the same solver seed and assess timing
variation, not search-seed robustness.

## Claims excluded from the intended publication

The current work does not establish a new cut family, a stronger limiting
relaxation than perspective OA, universal oracle dominance, the convex hull
of the complete GDP from separate hull intersections, exact numerical
certification, or broad superiority over conic optimization. An absent trig
cone translation is not a proof of nonrepresentability. The scalar cut-count
example is not a GDP complexity separation. No general objective-error rate
is inferred from separate-disjunction geometric repair. Scientific priority
cannot be inferred from a literature search's failure to find a matching
title.

The completed evidence meets the narrower computational scope set out in the
[independent publication challenge](lbesh-publication-challenge.md).
The [final scientific review](lbesh-final-publication-review.md) accepts that
scope; the [readiness assessment](lbesh-publication-readiness.md) states the
resulting contribution and limits.
