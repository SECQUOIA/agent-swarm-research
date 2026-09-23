| Source claim | Formal proof |
|---|---|
| Exact inverse-moment interval (C) | `Moments.lean`: finite positive measures, weighted Cauchy–Schwarz, secant bound, explicit three-atom attainment of every admissible value, including zero mass |
| Allocate the reciprocal moment between the two leaf endpoints | `Allocation.lean`: all boundary cases, with total inverse moment exactly t |
| Actual original graph and convex hull | `Model.lean`, `Representation.lean`: real graph points and finite convex combinations |
| Exact one-leaf hull using two rotated SOC constraints | `Hull.mem_hull_iff_conicBounds` (namespace `ReciprocalAnchor`): all real 0<a<b; necessity and constructive sufficiency |
| Equivalent 3×3 PSD formulation (A) | `PSD.lean`, `mem_hull_iff_psd`: actual `Matrix.PosSemidef`, including zero denominators |
| Fixed-anchor case a=b | `Degenerate.lean`: exact linear hull description |
| Individual rational examples lie in the exact hulls | `Joint.first_leaf_in_hull`, `second_leaf_in_hull`: explicit original-graph convex combinations |
| Joint separating inequality (D) | `Separator.joint_cut_pointwise`, `Joint.joint_cut_valid`: exact coefficients and correction 1/400, valid pointwise for all X>0 and on the stated convex hull |
| Individual hull intersection is insufficient | `individual_hulls_not_joint`: two individual memberships and joint nonmembership |

File prefixes in this table locate the modules; all declarations are in the
`ReciprocalAnchor` namespace.

The obstruction is proved using the explicit separating cut. The separate
Cauchy–Schwarz equality/support argument in the note is not needed or separately
formalized. Likewise, the cut proof uses rational quadratic certificates rather
than separately proving the four displayed radical identities or their strict
bounds. The proved bound is sufficient for exactly the claimed strengthened cut.

Not formalized here: congruence to an earlier moment-cut matrix, affine
normalization of a general leaf box, extensions with product bounds or linking
constraints, arbitrary-many-leaf hulls from the separate later note, or any
novelty or algorithmic-complexity claim. The exact hull statements concern the
original graph's convex hull; they do not assume a representing distribution.

Later coverage: the completed [many-leaf package](../13-many-leaf-reciprocal/COVERAGE.md)
proves the equality-support argument (MR46), affine leaf-box normalization
(MR27–MR28), and the arbitrary-many-leaf hull. These are additions in that
package; the exclusions above describe the scope of this one-leaf stage.
