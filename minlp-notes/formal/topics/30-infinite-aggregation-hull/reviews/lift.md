# Independent semantic review of the finite lift

Reviewed `LiftSmall` and `Lift` in namespace `InfiniteAggregation`.
Machine verification is recorded separately; this review did not repeat
the author's targeted builds.

`hullLift` is the actual affine matrix on `Fin 2 ⊕ Fin r`: its leading
block is `[[1,sigma],[sigma,1]]`, its next two rows contain `u` and `v`,
the transpose block contains the corresponding columns, and its lower
block is the identity. `lift_schur` proves that eliminating this identity
gives the stated two-by-two slack matrix. Thus the lift is a faithful
reindexing of source formula (9), with no extra decision variables except
the scalar `sigma`.

`gramMatrix_posSemidef_iff` includes both nonnegative diagonal conditions
and the determinant inequality. Its converse explicitly treats a zero
first diagonal, which forces the off-diagonal to vanish. The positive
definite counterpart proves both positive diagonals and strict determinant
inequality, then tests every nonzero vector, including vectors with zero
second coordinate. These are genuine matrix PSD/PD properties.

The PSD Schur criterion uses the proved library block theorem with the
identity positive definite. The PD criterion is proved through a completed
square and the corresponding Hermitian equivalence. Its forward direction
chooses the lower coordinates to cancel the square; its reverse direction
handles separately whether the upper coordinates vanish. No nonzero
vector or singular-boundary case is dropped.

For the weak scalar projection, the constructive witness is
`sigma=d+sqrt(p*q)`, which satisfies the weak lower bound and the PSD
determinant equality. This remains valid when `p*q=0`. For the strict
projection, `sigma` is chosen strictly between `max(h,d)` and
`d+sqrt(p*q)`. Positive slacks make this interval nonempty, and the choice
gives both `sigma>h` and the strict determinant condition. In the intended
application `h=1/2`; the implementation therefore proves the exact strict
scalar requirement and does not settle for `sigma≥1/2`.

`mem_closedRegion_iff_lift` and `mem_hullRegion_iff_lift` are unconditional
equalities for the candidate scalar regions. Combining them with the
independently established hull equalities discharges H03–H05. The affine
identity and PSD/PD addition arguments also prove convexity of both
candidate regions, including zero convex weights.

No mathematical defect, missing boundary case, or source mismatch was
found. These are exact representation theorems, not verified numerical
solver or computational complexity claims.
