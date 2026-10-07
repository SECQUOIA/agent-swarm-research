# Final contribution-language review

Review date: 2026-10-02. This review read the actual current research README,
document README, claim map, and the report's main, screening, star, overlap,
integration, evidence, and literature sources. It also read the theory README,
overlap note, numerical contract, and screening note. It concerns attribution
and the scope of claimed contributions; the numerical review separately
checks proofs, code, and experimental arithmetic.

The document correctly presents the work as an integrated research
implementation. It does not assert a first simultaneous-convexification
method, new Bernstein theory, new box-forest tractability, general SDP
dominance, or certification of the whole solver run.

| Contribution | Final claim boundary assessed |
| --- | --- |
| Final-cut certification | The proved object is a concrete lower support bound for the stored expression, domain, and exported binary coefficients. Interval and Bernstein bounds need not be exact minima. Exact polygon/star support is distinguished from those bounds. |
| Separation screening | The normalized violation bound is attributed to standard convex-combination geometry and Hölder's inequality. It is a checkable skip condition, not a runtime prediction or a proof of original nonlinear feasibility. |
| Polygon quadratics | Stationary-point enumeration supplies exact rational support. Existing quadratic hull theory is attributed to Anstreicher and Burer. A bounded direction-search implementation is not claimed to compute the entire hull. |
| Constrained stars | Box-only support is identified as a specialization of Del Pia and Khajavirad's forest algorithm. Affine response pieces are related to classical parametric QP. The explicitly implemented extension allows center–leaf rows and all signs of leaf curvature; it excludes leaf–leaf coupling and carries no priority claim. |
| Gain from merging fixed pair directions | The report states the exact constant improvement for specified normals and its compatibility condition. It does not claim to choose the best normals automatically or predict solver speed. |
| Overlap obstruction | The witness concerns intersected exact pair hulls with matching first and second shared moments. The report explains that dense SDP plus the missing nonedge product also excludes it; no dominance over that stronger baseline is asserted. |
| Solver integration | Native nonlinear recognition and existing bilinear, RLT, and moment-minor cuts are credited. Source/native model checks, replay, and root-only cuts have explicit trust and applicability limits. |
| Native sampling | Microbenchmark gains are expressly separated from complete-solve performance and from a native SCIP nonlinear handler. |

Two wording corrections were sent to the responsible authors and then
confirmed in their actual revised files:

1. In the literature section, Anstreicher–Burer Theorem 7 concerns
   triangulated **polytopes**, not arbitrary unbounded polyhedra.
2. The research README's opening operation should certify **a lower bound
   on** the support value. Its general arithmetic paths do not compute exact
   support values in every case.

The saved [campaign results](../experiments/campaign-v1/results.md) report
19 numerically solved selected held-out models for baseline and control,
versus 18 for both cut modes, out of 24 selected. The research README
distinguishes 20 admitted models from four refusals and now explicitly
recommends leaving native SCIP as the default. This is the appropriate
interpretation: the bounded experiment has an unfavorable comparative
outcome, rather than merely leaving performance unexamined. Microbenchmark
improvements and exact diagnostic cuts do not reverse that interpretation.
Final report summaries should retain this explicit conclusion and the
short-run, shared-host, and numerical-solve qualifications. The numerical
review owns reconciliation of the detailed counts and timing records.

No additional literature search is needed to make these narrower claims.
The inspected latest source versions and access limits remain in
[the source manifest](sources/MANIFEST.md). The 23-entry bibliography was
already parsed successfully in the targeted literature checks. This final
review adds actual-document reading; it does not claim an additional
test run, project-wide verification, CI inspection, or formal proof review.
