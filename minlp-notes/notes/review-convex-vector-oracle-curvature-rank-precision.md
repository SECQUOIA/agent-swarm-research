# Independent audit of curvature-rank precision for oracle error bodies

Date: 2026-09-05. Reviewer: `binary_formulation_review`. Verdict: PASS on
[the main transfer theorem](convex-vector-oracle-curvature-rank-precision.md).

This report reviews the theorem independently of its author. I authored
the supporting rational-spanner lemma; its own independent audits are
therefore necessary and are not replaced by this report.

The endpoint-affine subtraction places every deviation and Jensen gap in
the nonlinear image. For polynomials, linear independence of `x^k-x`,
`k>=2`, identifies the span of that curve with the nonlinear coefficient
column span. The rational left inverse and both effective-body radii are
valid and have polynomial bit length. A violated pulled-back separator
cannot have zero normal, because zero belongs to the effective body.

Small positive coordinate-axis normals belong to the positive polar and
their projections span the effective coordinates. The selected normals
give convex scalarizations with nonnegative chord gaps. Consequently signed
barycentric coefficients still yield domination by the sum of basis gaps.
Unconditionality makes the positive-polar support identity exact on the
nonnegative vector of component gaps. This is the step that excludes the
earlier tilted-body counterexample.

Feasible effective-body basis columns and their negatives generate an inner
crosspolytope. Dividing their coefficient cube by `r` gives the inner
parallelotope; a coefficient bound `d` gives outer dilation `dr`.
The finite maximum-determinant bases have coefficient bound one. On each
parity hull the scalar sum gap is at most `2r`; refinement to `1/(2r)`
uses `8r^2-1` intervals and puts the vector gap inside half the inner
parallelotope. Its symmetric half-body chord band contains the graph and
admits errors in the full parallelotope, hence in the original budget.
The resulting pieces are polyhedra despite the nonpolyhedral original body.

For the constructive theorem, the supporting rational oracle supplies exact
feasibility and uniformly polynomial encoding for coefficient bound below
three. The safe value three for each basis gives gauge control `3g_Psi`
and outer dilation `3r`. At tolerance `1/(36r)`, scalar chord error is
`13/(576r)`. Multiplying by three and then by `3r` puts the vector gap in
`13P/64`. These constants have been checked independently.

Coordinate-polynomial rounding remains in the nonlinear image. The inverse
basis row-sum bound makes each rounding vector belong to `P_0/16`, so the
output center error belongs to `17P/64`. A symmetric `P/2` band both contains
the exact graph and admits only `49P/64` error. Common knots and the same
interpolation weight ensure simultaneous vector containment. Restoring the
affine output part exactly causes no additional error.

Every new map, coefficient evaluation, inverse, rounding depth, and band
equation has polynomial bit length under the fixed-denominator spanner
guarantee. All added variables are continuous except the scalar global index.
The conversion of a coordinate outer radius to the rational Euclidean bound
`mR` is safe. Direct refinement takes `144r^2-1` cells per parity hull;
the scalar factor `486` gives fewer than `69984r^2 2^p<2^17 r^2 2^p` cells.
This verifies `p_out<=p_conv+17+2ceil(log2 r)`.

The rank-zero branch, one-input restriction, oracle assumptions, and absence
of a claimed necessary rank overhead are explicit. No correction was needed.
