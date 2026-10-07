# Independent review: exact implicit convex-patch output

Date: 2026-10-02. Verdict: **PASS after correcting the output-size wording.**
The reviewer read the actual
[convex-patch theorem](../new-direction/implicit-convex-patch-certificate.md),
the [polynomial pruning extension](../new-direction/polynomial-pruned-grid-extension.md),
and the [precision obstruction](../new-direction/implicit-optimum-precision-obstruction.md).
This is a mathematical review of their composition, not an implementation
of the complete optimization algorithm or a claim of priority.

The conclusion is substantive but conditional: under physical point
quadratic growth and a comparable positive lower bound on the full
continuous Hessian at the optimizer, the construction returns a verified
strongly convex subproblem that defines the exact optimizer. Its size and
construction cost are `f(p,kappa) poly(I)`. It avoids expanded algebraic
coordinates and does not resolve the active set explicitly. The conditions
control termination; the returned certificate is sound without trusting them.

## 1. Global containment and integer recovery

The corrected-grid lower bounds and conditional min-marginals use the
verified upper-coordinate-curvature bound on the full box hull, including
fractional points between integer labels. Their polynomial extension is
valid by sequential semiconcavity; it does not require quadratic cross-term
cancellation. Exact Bellman tables and every pruning decision must be in
the successful trial's certificate. A check of the final restricted box
alone would not prove global optimality.

The extra integer rule repairs a real limitation of interval filtering.
When all current integer labels are grid nodes and all adjacent gaps are
one, each integer unary correction is zero. Fixing one such label and
rounding the other coordinates proves that its min-marginal is a lower
bound for every completion. Removing labels whose lower bound exceeds the
feasible incumbent is therefore sound. Taking the remaining hull cannot
remove a global optimizer or the corrected-grid minimizer.

The unit-grid timing uses the previous stage, not the current stage's
conclusion circularly. At stage `j`, the previous retained integer hull
has outward radius at most
`1+10 sqrt(n*kappa) h_j` from the current center. Once
`h_j <= 1/(10 sqrt(n*kappa))`, that radius is at most two; with
`theta <= 1/4` every generated integer step is one. The retained-label
witness then satisfies

\[
 \|z-a\|^2\le(22/15)\kappa n h_j^2\le22/1500<1.
\]

A native integer label different from the optimizer's label would already
contribute at least one to this distance. Thus the node filter leaves
exactly the optimal integer assignment. The stage-zero case is harmless:
an original width below one contains no nonfixed native integer interval.

The draft explicitly continues refinement even if an earlier objective-gap
test succeeds. Patch search must stop on the singleton/convexity certificate,
not on a different approximation stopping rule.

## 2. The Hessian certificate has the correct orientation

The row sum of absolute third-derivative bounds gives

\[
 \|H(x)-H(c)\|_2\le T\|x-c\|_\infty\le Tr
\]

on the continuous patch after integers are fixed. The proposed rational
test

\[
 H(c)-(Tr+\tau)I\succ0
\]

therefore proves uniform Hessian lower bound `tau I`, as claimed. Exact
rational LDL with positive pivots is a finite certificate; its verification
does not depend on numerical eigenvalue computation. Removing any fixed
continuous coordinates before the test is appropriate.

Conversely, if the unknown optimizer belongs to the patch and
`H(a) >= g I`, then `H(c) >= (g-Tr)I`. Radius `r <= g/(4T)` and
threshold `tau <= g/4` give a strict margin at least `g/4` in the test.
The two variation allowances are necessary and both occur in the proof.

The retained box contains every original global optimizer and is a subset
of the original feasible domain. Its strongly convex restriction has a
unique constrained minimizer. That point is consequently the unique
original global optimizer. No signs of active gradients over the whole
patch are needed. This remains true when the patch touches original bounds.

## 3. Unknown growth, bit depth, and size

With `K_mu=4^mu`, `theta=2^-mu`, and `tau_mu=L/(4K_mu)`, the first
trial satisfying `K_mu >= 8kappa` has `K_mu <= 32kappa`, including
the initial trial. The stated finite stage budget simultaneously ensures
the integer-label condition and

\[
 r\le5\sqrt{n\kappa}\,h_j\le L/(4TK_\mu)\le g/(4T).
\]

It therefore closes by that trial. The stage budget is
`poly(I)+O(mu)`: the third-derivative bound affects the number of bits
and refinement stages, rather than appearing numerically in the grid
state count. Caps are checked before allocating large DP tables. Capped
trial sums and the existing absorption of `(log n)^p` give the stated
parameterized complexity.

The fixed trial threshold is useful. Any earlier successful trial has
no larger `K_mu`, so the output obeys

\[
 \tau\ge L/(128\kappa),\qquad 2L/\tau\le256\kappa.
\]

Choosing an arbitrarily tiny stage-dependent threshold would not provide
this evaluation guarantee.

One wording correction was required and is now present in the actual
file. The grid denominator bound includes `mu*K_grid`, whose magnitude
can depend numerically on the conditioning. Thus the established output
length is `f(p,kappa) poly(I)`, polynomial in the input at fixed parameters,
not unconditionally `poly(I)`. The same qualification applies to the
coefficients of the KKT representation that encode patch endpoints.
No additional outward rounding step was added. This keeps the proved
algorithm and its claim aligned.

## 4. The implicit output has a useful computational meaning

The output does not merely rename the original optimization problem.
Its feasible integers are fixed, its remaining box is rational, its
polynomial degree is fixed, and uniform strong convexity is certified.
The separate pruning trace proves original global optimality. The box KKT
system defines a unique primal point; after fixed intervals are removed,
its multipliers are unique as well.

Strong convexity and the constrained first-order inequality give
`F_B(x)-F_B(a) >= (tau/2)||x-a||^2`, including boundary minimizers.
The polynomial approximation theorem can therefore be applied to the
patch with condition at most `256kappa`. Requesting certified value gap
at most

\[
 \min\{2^{-q},(\tau/2)2^{-2q}\}
\]

gives both the claimed Euclidean position error and value interval width.
Substituting the parameterized patch input length into that algorithm's
polynomial bound preserves `f(p,kappa) poly(I+q)`. No exact algebraic-number
oracle, sign determination at a tiny active multiplier, or trusted local
nonlinear solver is hidden in this step.

## 5. Scope checks

At a continuous interior optimum, two-sided directional point growth
implies `H_CC(a) >= 2g I`; the weaker hypothesis in the theorem is
automatic there. At boundary points, point growth does not imply full
positive definiteness. For example, a positive linear objective on a
bounded nonnegative interval has positive point growth and zero Hessian.
The quantitative full-Hessian hypothesis cannot be silently removed.

The draft's stronger precision example `G=F+y+x_n y^2` is correct.
Its point growth and upper diagonal curvature remain uniformly bounded,
while the additional Hessian eigenvalue at the optimizer is `2a_n`,
doubly exponentially small in the chain length. A rational positive
full-Hessian lower bound retaining that coordinate would require long
denominators. The example has the easy global elimination
`partial_y G >= 1`, so it limits this output contract rather than proving
hardness for every implicit representation. The actual note states that
qualification.

The fixed-degree explicit-polynomial input restriction and native-integer
spacing are also material. No general arithmetic-circuit evaluation
oracle, binary-exponent polynomial model, or metric-free rational-lattice
extension is claimed.

## 6. Targeted checks actually run

The reviewer ran

```sh
python research-20261002/reviews/check_implicit_convex_patch_review.py
```

The [persistent diagnostic](check_implicit_convex_patch_review.py) passed
three exact rational closed-patch certificates for the boundary quartic
chain in dimensions 5, 10, and 18. It constructs the Hessian and a verified
row sum of third-derivative bounds, then checks strict diagonal dominance
of `H(c)-(Tr+tau)I` with `tau=1/2`. Every patch uses endpoints with at most
12 denominator bits, includes the true optimizer, and also contains a
point where the active `y` derivative is negative. Thus these patches
certify strong convexity while the uniform active-sign test fails.

A separate mixed quadratic fixture verifies the integer-filter distinction:
ordinary interval retention keeps the hull of labels `0,1,2`, whereas
individual exact min-marginal filtering keeps only the optimal label `1`.
The checker does not implement the full global pruning algorithm. These
finite tests supplement the universal proof and do not establish it by
sampling. No project-wide checks or CI inspection were performed.
