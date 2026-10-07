# Independent review of the convex cubic polytope extension

Date: 2026-10-02. Result: passed the complete actual
[polytope addendum](../new-direction/convex-cubic-polytope-point-oracle.md),
including its affine-branch error constant and original-coordinate
minimum-norm output. Read all sections after the draft was saved and
reread the two subsequent completeness clarifications. No substantive
mathematical or bit-complexity gap remains.

The scope is explicit rational degree-at-most-three objectives promised
convex on a nonempty bounded rational polytope given by rational linear
inequalities. The result does not recognize convexity or cover general
nonlinear feasible sets. It uses the separately reviewed
[box error-bound argument](convex-cubic-point-oracle-review.md) and
classical rational linear and weak convex optimization.

## 1. The actual affine hull is found in polynomial bit work

Maximizing each inequality's slack correctly distinguishes rows that
are equalities everywhere from rows merely tight on some face. Exact
rational LP values permit the required zero test. An independent
subset of the universally tight rows implies all the remaining
universally tight equations because the system is consistent.

For each non-universally-tight row, a feasible strict-slack witness
exists. Their average is strict for every such row. This gives a
relative neighborhood in the selected affine solution space and
proves that this space is exactly the affine hull. The revised wording
correctly excludes redundant universally tight rows from the strict
witness construction.

Rational elimination supplies `x=x_0+Vu` with polynomial-bit entries,
full-column-rank `V`, and the stated identity submatrix. If its column
count is zero, the unique feasible point is rational and can be
returned directly. Otherwise the transformed feasible set is bounded
and full-dimensional. Substitution in an explicit cubic causes only
polynomial growth in monomial count and coefficient length. It is
correct to delay the positive-semidefinite Hessian argument until this
reduction: convexity on a lower-dimensional original set does not
imply an ambient Hessian condition there.

The inball LP uses the rational one-norm of each nonzero row, which
dominates its Euclidean norm. A positive solution therefore certifies
the stated Euclidean ball. Full dimension ensures a positive optimum;
boundedness and `0<=rho<=1` make the feasible LP region compact.
Exact rational LP returns the center and radius with polynomial bit
length. Coordinate LP bounds give the stated rational outer radius.
No small numerical tolerance is used to infer dimension or strict
feasibility.

## 2. Reflection and the error constant

The reflected point lies in the certified ball. The affine Hessian
therefore expresses its center value as a positive weighted average
of the two endpoint Hessians. Rearrangement gives exactly
`H(u)<=(1+R/rho)H_c`. This proves the common-kernel statement and the
uniform Hessian norm bound, including boundary points where an
individual Hessian can have a larger kernel.

The cubic Taylor and third-derivative identities require only feasible
segments. Using the deliberately loose bounds `||d||<=2R`,
`||c-v||<=2R`, and `||H||<=2M` reproduces the box estimate with
`sqrt(n)` replaced by `2R`. Thus the denominator `384 M R^2` is
valid. The sharper bound actually available on these quantities is
not needed. The optimizer-set affine-slice characterization and the
extra gradient-row residual estimate follow as in the box proof.

For the generalized Hoffman estimate, projection onto the equality
slice gives equality rows plus active inequality normals. Selecting
original rows and eliminating dependent normals modulo the equality
row space leaves at most `s` independent integer rows, each bounded
by `C_*`. Their Gram determinant is at least one and their operator
norm at most `s C_*`. The resulting singular-value bound is therefore
valid. Active inequality normals have nonpositive inner product with
the feasible displacement, leaving only the equality residual. This
proves the displayed constant uniformly in the possibly irrational
right-hand side and without assuming a full-dimensional slice.

All transformed inequality rows are included in the integer height
bound. Clearing their denominators together with the Hessian and
gradient preserves polynomial bit length. The positive-principal-minor
argument gives the stated `lambda_0`; using the larger global `M`
instead of the center norm only weakens this lower bound. The values
`R_0`, `Gamma_u` and `Gamma_P` are rational, computable in polynomial
time, and have polynomial binary length. The norm bound on `V` correctly
transfers reduced-coordinate distance to original-coordinate distance.

The affine branch also now supplies the promised error constant.
Its equality matrix has just the cleared-gradient row, so its residual
is `D E`. Hoffman gives a linear-in-gap distance bound, which implies
the required fourth-root bound for gaps at most one. A constant
objective has zero distance to its optimizer set and permits constant
one. This fills the degenerate case without dividing by a nonexistent
positive Hessian eigenvalue.

## 3. Weak optimization is repaired to exact polytope feasibility

The reduced polytope has known rational inner and outer radii. The
capped epigraph is consequently a full-dimensional convex body with
polynomial-bit geometric data. A violated linear row separates an
outside query; a polynomial tangent is used only for a query whose
core point is inside the feasible polytope. Thus convexity is needed
only on the supplied domain.

The rational repair
`u_hat=(rho u+delta c)/(rho+delta)` is exact. Each row violation at a
point within `delta` of the polytope is at most `delta||a_i||`, while
the center has slack at least `rho||a_i||`. The two terms cancel in
that convex combination. For a nearby feasible point, the displacement
bound is the stated `delta(1+R/rho)`. Both points used for the gradient
estimate are feasible, so no convexity outside the polytope is assumed.

The value tolerance can be made explicit. Let
`r_K=min(rho/2,1/2)` and let `G` bound the gradient norm. Put

\[
 A_0=1+(2F_{\max}+1)/r_K,\qquad
 C_0=A_0+1+G(1+R/\rho),\qquad
 \delta=\min\{r_K/2,\eta/C_0\}.
\]

The usual inner-set comparison gives `t<=f*+A_0 delta`, and the
repair gives `phi(u_hat)<=t+[1+G(1+R/rho)]delta`. Therefore
`[t-A_0 delta,phi(u_hat)]` is a certified interval of width at most
`eta`. Every quantity has polynomial binary length. This supplies
the concrete tolerance accounting behind the draft's weak-output
argument and avoids assuming an exact-feasible weak optimizer.

If a tangent certificate is wanted, its linear minimum is an ordinary
rational LP over the reduced polytope. The existing smoothness argument
controls its gap after polynomially many extra accuracy bits. The
distance algorithm only needs the certified value interval and the
already computed error constant.

## 4. Minimum norm uses the original metric

The reduced objective is regularized by `||x_0+Vu||^2`, not by `||u||^2`.
The regularization convergence proof uses only convexity, compactness,
the original-coordinate error constant and a radius bound, so the box
corollary applies with the displayed parameters. The affine error
constant makes this argument available on that branch as well.

For feasible original points, convexity plus the exact quadratic norm
identity gives a regularized objective gap at least
`tau||x-x_tau||^2`. Constrained first-order optimality suffices even
on a lower-dimensional polytope. Hence the value tolerance converts
directly to original Euclidean distance, and a smallest-singular-value
estimate for `V` is unnecessary. Combining this accuracy with the
regularization bias proves approximation to the fixed minimum-norm
optimizer with only `poly(I)+O(q)` bits of additional precision.

## Verification scope

This was a fresh complete-file mathematical and bit-complexity review.
Read the final affine-constant and affine-hull wording changes, and also
checked the analogous affine-constant addition to the box theorem.
The final explicit weak-optimization tolerance and interval paragraph
was separately read after the author added it.
A targeted inline Python check of the addendum and this review passed
local links, paired fences and display delimiters, and trailing
whitespace. No optimization diagnostic was run, and no new agent,
external research, index edit, project-wide verification or CI
inspection was used.
