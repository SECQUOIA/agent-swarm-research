# Independent review: canonical selector comparison

Date: 2026-10-02. Verdict: the actual
[canonical-selector note](canonical-selector-radical-comparison.md) passes.

The added term is nonnegative and vanishes at the unique base optimizer
with `y=1`. Consequently every optimum has the same base coordinates,
and its last coordinate is free exactly when the distinguished base
coordinate is zero. Minimizing the Euclidean norm therefore gives the
claimed zero-versus-one jump. The Hessian square identity retains
`I/32` on the base coordinates and is valid at zero; global convexity
does not depend on an unjustified positive-curvature assumption in the
new coordinate. The new two-variable bag preserves maximum bag size
three. The threshold at `1/2` correctly separates rational outputs
within distance `1/4` of the canonical point.

The distinction between outputs is material. A nearby point to some
optimizer is easy for this family by always choosing `y=1` and using
the strongly convex base evaluator. Canonical selection and exact
optimal-affine-hull dimension contain the radical comparison. This
does not by itself give the stronger statement about any optimizer;
the separate [paired construction](convex-point-radical-comparison.md)
addresses that question.

I independently read the actual proof and checked these identities and
scope statements. The source author's symbolic and optimizer-set
diagnostics are recorded in its note and were not rerun. No broader
test or CI claim is made, and no publication-priority claim is assessed.
