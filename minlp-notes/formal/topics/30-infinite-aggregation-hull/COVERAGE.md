# Exact hull and SDP coverage

All eight frozen claims have implemented declarations and independent
semantic review. Names below are in namespace `InfiniteAggregation`.
The targeted machine verification record is separate evidence.

| Claim | Required interface | Evidence |
|---|---|---|
| H01 | Actual original systems, formulas, affine lift | `HullModel.hullRegion`, `closedRegion`, `weakFeasible`, `mem_weakFeasible_iff`; `Lift.liftRows`, `hullLift`, `liftSlack`, `lift_schur`, `hullLift_affine` |
| H02 | Ordinary convex hull equals strict formula, all `r≥2` | `HullCone.convexHull_subset_hullRegion`; `HullCoreRoots.two_roots_weights`; `HullCore.two_point_decomposition_of_strict_hull_inequalities`, `hullRegion_subset_convexHull`; `Hull.convexHull_feasible_eq_hullRegion` |
| H03 | Ordinary convex hull equals strict PD projection | `LiftSmall.gramMatrix_posDef_iff`; `Lift.fromBlocks_one_posDef_iff`, `hullLift_posDef_schur`, `hullLift_posDef_iff`, `exists_gramPD_iff`, `mem_hullRegion_iff_lift`; `HullRepresentations.mem_convexHull_iff_strict_lift` |
| H04 | Weak formula equals PSD projection, including singular slacks | `LiftSmall.gramMatrix_posSemidef_iff`; `Lift.hullLift_posSemidef_schur`, `hullLift_posSemidef_iff`, `exists_gramPSD_iff`, `mem_closedRegion_iff_lift` |
| H05 | Closure of ordinary hull equals weak formula and PSD projection | `HullClosure.isClosed_closedRegion`, `smul_mem_hullRegion`, `closure_hullRegion_eq_closedRegion`; `HullClosedConsequences.closure_convexHull_feasible_eq_closedRegion`; `HullRepresentations.mem_closedHull_iff_lift` |
| H06 | Hull of original weak system equals closed hull | `HullClosure.isCompact_weakFeasible`, `weakSegments`, `isCompact_weakSegments`, `weakSegments_subset_convexHull`; `HullClosedConsequences.hullRegion_subset_weakSegments`, `closedRegion_subset_weakSegments`, `convexHull_weakFeasible_eq_closedRegion`, `convexHull_weakFeasible_eq_closure_convexHull_feasible`; `HullRepresentations.mem_weakHull_iff_lift` |
| H07 | Ordinary hull equals all strict source-good aggregations | `HullCone.strict_cone_tests`, `goodCone_strict_intersection_subset_hullRegion`; `Hull.convexHull_eq_all_good_strict`, using topic 29's `good_iff_goodCone` |
| H08 | Closed hull equals all weak source-good aggregations | `HullCone.weak_cone_tests`, `goodCone_weak_intersection_subset_closedRegion`; `HullRepresentations.closedHull_eq_all_good_weak`, using topic 29's `good_closedHull_valid` and `good_iff_goodCone` |

Each `Module.declaration` entry identifies the module file and the declaration
in the common namespace; it is not an additional Lean namespace. The ten
owned modules are `HullModel`, `HullCoreRoots`, `HullCore`, `HullCone`,
`Hull`, `LiftSmall`, `Lift`, `HullClosure`, `HullClosedConsequences`, and
`HullRepresentations`, all under `Formal/InfiniteAggregation`.

The exact obligations and exclusions are in [CLAIMS.md](CLAIMS.md).
The [independent reviews](REVIEW.md) explain the strict/weak distinctions,
the dimension-two decomposition, actual lift, and singular boundaries.
Compilation, axiom audits, and kernel replays are separate verification
evidence and are not implied by the declaration inventory.
