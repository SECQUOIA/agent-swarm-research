# Integrated contribution and proof-scope review

Review date: 2026-10-03. The core proof and attribution review and the
limited final reading of both the 282-job prospective campaign and the
separate 75-job matched repair validation are complete. No unresolved
contribution, mathematical-scope, or attribution finding remains.

I read the report's `main`, `foundations`, `aggregation`, `polytope`,
`star`, `overlap`, `separation`, `implementation`, `evidence`, `literature`,
and `frontier` TeX sources and its claim map. I compared the new arguments
with the companion theory notes and the inspected primary-source ledger.
This review concerns mathematical reasoning, attribution, and stated scope.
It is not another code audit, experiment replay, or verification of SCIP's
internal numerical computation.

## Core findings

No unresolved proof or attribution issue was found in the reviewed core.

| Claim | Review finding |
| --- | --- |
| Joint support and safe cuts | The support argument, exact Bernstein bound, domain-cover premise, curvature lower bound, and final-coefficient contract are correctly distinguished. A successful cut is not an exact support optimum in every arithmetic path. |
| Original-variable aggregation | The signs, source-row constants, inequality multipliers, equality multipliers, and objective epigraph/hypograph orientations are correct. The formula is attributed to weak Lagrangian duality. |
| Closure of every aggregate direction | Compactness of the joint graph and addition of a closed coordinate cone justify closed convex separation. The closure is precisely the projected graph relaxation. The equality functions are now explicitly continuous. The `x^2 = 1/4` example correctly proves that this is not in general the original feasible-set hull. |
| Final row rounding | The bound correction has the correct sign. Its sufficient one-sided mathematical condition is distinguished from the current exporter's conservative requirement for two finite bounds when a coefficient changes. Exact coefficients can remain on unbounded variables. |
| General bounded-polytope quadratic support | The minimal-dimensional minimizing face has a positive-definite restricted Hessian, or zero tangent space. Its independent active-row basis gives a nonsingular bordered system. Complete enumeration therefore handles singular ambient Hessians, implicit equalities, flat minima, and empty domains. Feasible extra stationary candidates cannot invalidate the minimum. |
| Complexity | The face-subset count and rational encoding bounds justify polynomial bit complexity for fixed dimension. The report does not claim polynomial dependence on unrestricted dimension. A partial candidate list is not used as a lower support bound. |
| Constrained stars and overlaps | The inherited leaf-response argument retains its center–leaf constraint assumption and permits all curvature signs. The pair-hull witness and its `1/128` gap remain correct. Dense SDP with the missing product is expressly allowed to remove the same witness. |
| Complete positive-tolerance separation | The distance identity uses the appropriate dual normal box, with nonnegative normals on cone coordinates. The normal-grid error, rational feasible domain net, polynomial derivative bound, and separate support errors justify the claimed tolerance. Lower-dimensional domains cause no interior-grid assumption. |
| Separation scope | Complete finite enumeration, the bounded standalone API, and the deployed bounded callback are distinguished. Exhaustion returns unresolved. Distances for direct-row separation are in feature/slack coordinates, rather than automatically distances in original model variables. Rational separation and preservation of a numerical separation margin are distinct. |
| Source domains | The report identifies the submitted exact-binary expression DAG as its boundary and excludes later SCIP transformations. Exact existential guards preserve strict or nonzero domains in projection. Variable exponents require a proved positive base; cancellation does not authorize loss of original domains. Support on a polynomial extension is not a closeness certificate for a partial original graph. |
| Frontier | The explicit multilinear box quadratic reduction gives the negative weighted MaxCut optimum. This justifies the stated NP-hard boundary. It does not assert that all special classes or useful extensions are exhausted. |

Two small clarifications were requested and verified in revised text:

1. The equality extension of the closure theorem explicitly assumes
   continuity of the additional equality features on the compact domain.
2. The rounding discussion separates the broader one-sided mathematical
   condition from the exporter's actual conservative admission rule.

The direct Murty face-enumeration precedent was also added to the report
and bibliography after inspecting the author's chapter PDF, Section 2.9,
pp. 163–166. The bibliography now has 34 unique entries and passes a
standalone BibTeX parse. The author catalog and Internet-edition cover
distinguish the original 1988 book from the 1997 online edition.

## Attribution and evidence boundary

The report credits simultaneous graph support, composite/vector
convexification, Bernstein bounds, forest quadratic programming, parametric
quadratic responses, Lagrangian aggregation, safe numerical rows, and
optimization/separation duality to established literature. It does not
claim first-method status, general SDP dominance, or a new tractability
result for arbitrary quadratic programs. The finite-net construction is
not presented as a polynomial-time replacement for the classical
weak-oracle equivalence.

The main contribution language concerns the explicit admitted classes,
complete return contracts, mathematical proofs, source and final-row
binding, replay, and measured effects of a specified implementation.
Inherited source-access limitations remain recorded. In particular, the
Vavasis reference is checked at publisher abstract/metadata level; the
present finite-face proof is supplied directly rather than represented as
a full audit of that paper.

## Limited reading of the completed prospective campaign

I read the updated abstract, completion standard, evidence section,
attribution, frontier, research README, and CLOSEOUT against the reported
independent reconciliation. The primary application comparison states the
same 25 of 30 selected models solved in each mode, with greater summed
time for the cut modes. The synthetic root improvement is identified as
a local mechanism, not a new application solve. The deployment
recommendation remains native SCIP by default.

The claim that 123 recorded cuts replayed excludes the four worker-error
records with unknown logs. The 271 checked incumbents are described as
passing numerical original-model checks, rather than exact feasible or
optimal certificates. The earlier unfavorable 316-job campaign is retained.

The original frozen implementation and results are distinguished from
later discovery and budget-enforcement repairs. The 75-job repair cohort
was selected from observed failure and overrun groups, includes matched
modes, and is explicitly a regression validation rather than another
prospective holdout. The text does not replace original failures or splice
repair outcomes into the 30-model table. These qualifications are sound.

## Final repair results and deployment conclusion

I read the completed repair table, updated abstract, operational
recommendation, research README, and CLOSEOUT. I compared the repaired
counts with the saved `repair-discovery-v1/results.md` and replay summary.
This is a claim-consistency check, not a second execution of the
independent replay or metric audit.

The 75 repaired jobs are accounted for separately: no worker errors or
missing logs; 42 recorded cuts replayed; 67 returned incumbents passed
their numerical checks. The matched full application cohort solves four
of eight models per mode, and the historical cohort four of seven per
mode. Neither cut mode adds a solve. The report's 165-cut total is the
sum of 123 prospective and 42 repair cuts; the four original unknown logs
remain explicitly outside the claim.

Incomplete discovery on large repaired models is described as a safe
stop followed by native SCIP, rather than successful exhaustive analysis
of the discarded blocks. Measured soft-deadline excesses are retained,
and the report does not turn them into a hard real-time guarantee.

The final recommendation to retain native SCIP by default follows the
observed absence of a solve gain, greater primary summed time, and
unfavorable or tied matched bounds. Positive synthetic root evidence and
reusable exact-support or separation APIs are retained without being
promoted to a general solver improvement. The closeout limits completion
to the declared proved, implemented, and evaluated contracts; the
unrestricted hull, complexity, and whole-solver certification boundaries
remain intact.

No project-wide verification or CI inspection was performed for this
review. The separate mathematical row review, implementation reviews,
certificate replay, and experiment reconciliation retain their own
evidence and responsibility.
