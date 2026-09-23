# Independent HHC review

Status: source and statement review complete; no defects found. Targeted build,
axiom audit, and kernel replay results are recorded separately by the coordinator.

Reviewer scope is frozen claim I03: the actual homogeneous map in `Model.lean`
must have a convex image on every homogeneous hyperplane for every `r ≥ 2`.
This review does not weaken that claim to a conditional Gram realization theorem.

## Reviewed components

- `Model.lean` defines the homogeneous map as
  `(u·u − t², v·v − t², t²/2 − u·v)` and quantifies HHC over kernels of all
  nonzero real linear functionals on `(R^r × R^r) × R`.
- `GramFrame.lean` constructs an orthonormal pair containing the coefficient
  vectors in its span. It treats a zero first vector and a zero residual
  explicitly. The perpendicular-vector construction needs only `r ≥ 2`, so
  there is no hidden `r ≥ 3` assumption.
- `GramSupport.lean` constructs every scalar value allowed by the claimed
  Gram-fiber support bound. It first solves the circle functional equation,
  including the zero functional, then rotates a Gram factor. The `a = 0`
  branch forces `c = 0` and handles the remaining vector separately. The
  positive-`a` branch permits zero determinant. The final frame lift gives
  actual vectors, not merely a Gram matrix or a formal support inequality.
- `GramConcavity.lean` proves determinant-square-root superadditivity and
  nonnegative homogeneity from elementary two-by-two PSD inequalities. Their
  combination proves concavity, including singular matrices and zero
  coefficients. Convexity of the four-coordinate domain follows without
  assuming a positive determinant or a nonzero hyperplane scalar coefficient.
- `GramBound.lean` proves the two-frame upper bound by separating
  projections from residual vectors and comparing their Gram determinants.
  The residual terms make this valid in dimensions larger than two. Its
  `gram_support_upper` then applies this estimate to `P • u + Q • v` and
  `R • v`. The squared norms give the trace term, and the determinant is
  exactly the product of the coefficient and variable Gram determinants.
  Together with `gram_support_attained`, this proves both directions of the
  full support-interval claim.
- `Hyperplane.lean` represents every linear functional by two vector
  coefficients and a scalar. Its output linear map applied to actual Gram
  coordinates agrees definitionally with `Model.homEval`.

- `HyperplaneConvexity.lean` proves the exact equality
  `homGram_image_kernel`. The forward inclusion uses the proved support upper
  bound and the actual hyperplane equation. For the reverse inclusion it
  chooses `t = sqrt(T)` and realizes the scalar `−s t` on the prescribed Gram
  fiber. The assumptions permit `T = 0`, `s = 0`, singular coefficient Gram
  matrices, and singular variable Gram matrices. There is no division by
  any of these quantities.
- Its final theorem `hhc` has the sole hypothesis `2 ≤ r` and concludes
  `Model.HHC r`. Every linear functional is covered; no convenient
  hyperplane parametrization or additional range assumption is imposed.
  The last step identifies the actual homogeneous image with the linear
  image of the proved convex coordinate domain.

Frozen claim I03 is fully covered by the reviewed declarations. In particular,
the construction works at `r = 2` using explicit circle coordinates, without
assuming connectedness of the full orthogonal group. No mathematical or
statement-fidelity defect remains.

## Verification responsibility

This is a source and statement review. No builds were run by this reviewer;
the coordinator records the targeted build, axiom audit, and kernel replay.
