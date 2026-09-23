# Independent audit: quadratic precision in independent integer features

Date: 2026-09-05. Reviewer: `graph_precision_second_review`.

**PASS.** I independently reviewed [the independent integer-feature candidate](independent-integer-feature-quadratic-precision.md). Its normalized-volume bound, exact quotient, nonlinear rank, and rational construction give the stated `p_conv+5r+sum_i log2 w_i+1` guarantee. No correction was needed.

## Normalization and volume

For row `T_i`, the minimum and maximum over the unit cube are `ell_i` and `ell_i+w_i`. Full row rank ensures every row is nonzero, so the positive integer width `w_i` is at least one. The normalized image therefore lies in the unit `r`-cube and is full-dimensional, compact, and convex.

A nonsingular `r`-column minor exists. Fixing all other coordinates to zero leaves a parallelotope inside the normalized image, including the translation by `-diag(w)^{-1}ell`. Translation does not affect its volume, which is `|det T_I|/product_i w_i`. The nonzero determinant is an integer, giving the claimed lower bound. The parallelotope's containment also verifies that this ratio cannot exceed one. No computation of the full zonotope volume is required, and rational elimination finds a suitable minor in polynomial time.

The sharper actual-minor ratio is valid and invariant under positive row scaling when numerator and widths are both transformed. The coarser bound by the product of integer row lengths is the place where integrality enters.

## Diagonal output and exact rank

Substitution `T_i x=w_i u_i+ell_i` gives Hessian diagonal `C_ji=a_ji w_i^2` in the normalized coordinates. The additional terms are affine. There are no cross-feature quadratic terms because the supplied representation is a positive weighted sum of the individual squared forms.

The common original Hessian kernel equals `ker T`. If all output quadratic forms vanish on a vector, their nonnegative weighted square sums force every active feature to vanish. Conversely a vector annihilated by `T` belongs to every Hessian kernel. Since every feature is active and `T` has full row rank, the common nonlinear input rank is exactly `r`.

The affine-fiber quotient is exact for both formulation minima: restrict the original formulation to its cube, subtract its affine output, and project to normalized feature coordinates. For the reverse direction retain the original continuous variables, their cube, and the rational feature equations, then restore the affine output. Errors are preserved even when affine values vary along fibers. Neither direction adds integers.

## Precision constants and rational encoding

The already reviewed diagonal trace covariance proof applies on the normalized convex subdomain with unchanged support-volume constant. Covering volume `V` gives the lower term `Phi-A_r+log2 V`. The containing-cube square grid gives the upper count `Phi+r`; restricting it through the exact original-variable lift retains all original graph points. Coordinatewise error domination by `Cp/8` and unconditionality certify the whole output body.

The rational log-product oracle gives a feasible allocation with product at least `exp(-1)D`. Thus the constructed count is at most `Phi+r+1/(2ln2)`. Substituting the lower bound and `V>=1/product_i w_i` yields the first and second inequalities in (2), using `A_r<4r` and `1/(2ln2)<1`. Bounded row lengths therefore give the claimed linear-in-rank overhead with the explicit coefficient `5+log2 s`.

All row widths, offsets, squared widths, and transformed coefficients have polynomial encoding length, even if their numeric magnitudes are large. The scalar allocation and grid routines depend on these bit lengths rather than the magnitudes themselves. No new optimization import is needed.

The feature decomposition is explicitly supplied; the proof does not find it from an arbitrary collection of Hessians. For rational features, clearing a row's denominators multiplies its feature by a positive integer and divides its square coefficient by that integer squared. Dividing the resulting integer row by its greatest common divisor makes the reverse coefficient adjustment. These operations preserve the map, nonnegativity, and polynomial encoding, but may leave large primitive row lengths. The stated limitation for ill-conditioned rational features is consequently appropriate.

## Verification and scope

I ran `code/quadratic_rank/check_integer_feature_precision.py`. All 30 exact checks of normalized ranges, minor bounds, nonlinear ranks, quotient identities, and rational rescaling passed. The general volume proof requires only one integer minor and does not assume total unimodularity or disjoint row supports.

A forest incidence matrix has every active row width two and hence recovers the `6r+1` bound. Its separately proved exact volume can improve the component-sensitive estimate. The broader feature theorem allows overlapping supports and noncommuting original Hessians while requiring independent supplied features. It correctly makes no linear-overhead claim for arbitrary feature transformations without the row-length control. Novelty review remains separate from this correctness audit.
