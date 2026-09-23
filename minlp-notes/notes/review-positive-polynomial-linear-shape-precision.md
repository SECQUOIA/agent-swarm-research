# Independent audit: linear-dimensional shape-adapted precision

Date: 2026-09-05. Reviewer: `graph_precision_second_review`.

**Status: PASS for the final revised theorem.** Reviewed [the shape-adapted precision note](positive-polynomial-linear-dimension-shape-precision.md), including its revised Jensen-superadditivity proof and general continuous-convex corollary. The final claims are:

- Polynomial rational construction for dense positive polynomials: additive `12r` for a scalar sum and `9r` for independent outputs.
- Finite real-coefficient comparison for arbitrary continuous convex summands: additive `7r` for a scalar sum and `4r` for independent outputs.

The earlier `14r` scalar construction was valid but was superseded by the stronger proof. This audit covers the improved final constants. It also checks the separately retained [feature-curve identities](positive-polynomial-feature-curve-geometry.md). Literature novelty is not certified here.

## Maximal scalar packing and actual grid count

Uniform continuity of a scalar function makes the midpoint gap at most `tau` whenever the two inputs are sufficiently close. Hence a set with all pairwise gaps strictly above `tau` has a uniform positive input separation and bounded finite cardinality. Starting with one point and adding another whenever possible must terminate after finitely many additions. This proves existence of a finite maximal packing; a maximum-cardinality packing or a computable selection procedure is unnecessary.

For a fixed selected point, its compatibility set is a closed interval containing that point. The derivative signs displayed in the note are correct for smooth convex functions. They extend to continuous convex functions by convex piecewise-linear approximation or smoothing. Monotonicity of the gap under interval enlargement rules out disconnected components of this compatibility set.

Maximality implies that the compatibility intervals cover the entire domain: a point outside them would have gap greater than `tau` from every selected point and could be added. Splitting each interval at its anchor gives at most `2P` intervals whose endpoint midpoint gaps are at most `tau`. Concavity of chord error bounds its full maximum by twice the midpoint value. Degenerate pieces can be discarded, and the finite interval cover can be trimmed to a partition without increasing the number of pieces or chord errors. Thus `N_(2tau)<=2P` is justified.

The previously audited curvature inequalities then give `M_tau<=2M_(2tau)<=48N_(2tau)<=96P`. For the actual scalar compiler, `U<=M_tau+1/256`. If its computed depth is positive, `2^L<=5U<=480P+5/256<=481P`. For zero depth, `2^L=1<=481P` since the packing is nonempty. This bounds the actual computed binary count, not just the minimum scalar count. The compiler is independent of the packing, which remains solely a lower-bound witness.

## Independent outputs

The full Cartesian product of the coordinate packings is pairwise midpoint-incompatible: two distinct product points differ in some coordinate, and that coordinate's corresponding output exceeds its own error tolerance at the graph midpoint. Arbitrary affine terms, including affine dependence on other coordinates, cancel in this Jensen gap.

Choosing a lift of each exact graph point and applying the integer-parity argument gives `2^p_conv>=product P_i`. Composing the scalar constructions restores every exact graph point and respects each output tolerance. Summing `L_i<=log2 P_i+log2 481` and using `481<512` proves the `9r` bound. No restriction on the number or type of continuous variables in the competing convex lift is used.

## Jensen superadditivity and strict code thresholds

The smooth midpoint-gap identity has the correct factor one half:

```
J_phi(a,b)=(1/2) integral_a^b min(t-a,b-t) phi''(t) dt.
```

For a point in any subinterval, both distances to the global endpoints dominate the corresponding distances to the local endpoints. Thus the global tent dominates each local tent. Their interiors are disjoint, so nonnegative curvature proves `J_phi(a,b)>=sum J_phi(x_j,x_(j+1))`.

For continuous convex functions, convex piecewise-linear interpolants converge uniformly on the compact interval. Each interpolant has a representation as an affine function plus nonnegative hinges, and a hinge's midpoint gap is exactly one half of the tent at its kink. The same inequality therefore holds for each interpolant and passes to the uniform limit. This avoids any endpoint differentiability or curvature-monotonicity assumption in the finite corollary.

Adjacent packing gaps are strictly greater than `tau`. Summing them gives gap strictly greater than `tau*h` at index separation `h>0`. In a scalar sum, coordinate Jensen gaps add without cancellation, so distinct product points have total gap strictly above `tau` times their index `ell_1` distance. With `tau=epsilon/r`, distance greater than `r` suffices for strict violation of the scalar tolerance. In fact distance exactly `r` would also violate it; the chosen deletion rule is safely conservative.

The lattice-ball estimate is correct. Each point in the radius-`r` ball has weight `2^-norm` at least `2^-r`; the total weight over the lattice is `(1+2 sum_(k>=1)2^-k)^r=3^r`. Hence the ball has at most `6^r` points. A greedy selection deletes at most that many product points per selected point, and the finite product boundary only reduces the deleted count. The selected code has at least `product P_i/6^r` points, separated by distance greater than `r`.

Every selected product pair therefore violates the midpoint tolerance. Parity gives `2^p_conv>=product P_i/6^r`, even when the right side is below one. Neither enumerating this product nor constructing the code is part of the claimed polynomial-time algorithm.

## Construction and revised constants

Each coordinate compiler is run at tolerance `epsilon/r`, and its actual error is at most `15epsilon/(16r)`. Summing its scalar outputs therefore admits every exact scalar-sum graph point and has absolute total error at most `15epsilon/16`. Restoring affine terms uses only exact linear equations.

Replacing the tolerance by `epsilon/r` adds only `O(log r)` encoding bits. The sum of the coordinate construction costs and sizes is polynomial in the complete dense input. The feature coefficients and packing points used in lower-bound proofs never enter the rational formulation.

The code lower bound and the actual coordinate cell counts give

```
p_out<=p_conv+r log2(6*481)<p_conv+12r,
```

since `6*481=2886<4096`. This proves the final scalar-sum claim. The independent-output calculation uses `481<512` and proves the stated `9r`. The same reasoning covers local packings of size one and coordinate compilers with zero depth.

## Finite general continuous-convex corollary

The separately audited three-piece refinement gives `N_tau<=3N_(2tau)`. Combining with the maximal-packing cover gives `N_tau<=6P`. Logarithmic finite encoding of the chord bands uses depth `ceil(log2 N_tau)`, so its number of binary assignments is at most `2N_tau<=12P`, also when `N_tau=1`.

For independent outputs, the full product packing gives additive `r log2 12<4r`. For a scalar sum, use local tolerance `epsilon/r` and the same radius-`r` code to get additive `r log2(6*12)<7r`. Summing local error bounds gives the required total tolerance. These are valid finite real-coefficient results for arbitrary continuous convex summands; they do not claim rational knots, efficient access to a partition, or polynomial construction time from a function oracle.

## Retained feature identities

The feature comparison from the earlier proof remains correct. Convexity of `x^(k/2)` gives the lower coefficient `1/4`. Arithmetic-geometric mean gives the upper coefficient `1/2`. Nonnegative coordinate coefficients preserve both after summation. On an ordered input sequence, feature increments are coordinatewise nonnegative, so all cross inner products in the square of their sum are nonnegative; squared distance is superadditive. These identities are useful independently, but they are weaker than the direct Jensen argument for the final count.

## Independent exact checks and scope

Independent rational checks passed **144 feature comparisons** and **84 ordered-packing inequalities**. After the improved proof was added, a separate check verified **84 exact Jensen-superadditivity and strict-distance cases** and **1,978 radius-`r` product-code midpoint incompatibilities** in dimensions one through four. The lattice-ball counts in those dimensions obeyed `6^r`. The coordinate examples included mixed positive powers through degree eight and rational squared input grids, allowing exact checks even for the half-power features.

These finite checks supplement the symbolic arguments. No mathematical correction was required in the final revision. The constructive claim remains limited to densely encoded positive polynomials and the two stated output structures. It does not assert the same result for arbitrary coupled output bodies, sparse huge degrees, or arbitrary efficiently evaluated convex summands. Affine-only coordinates can be retained exactly or removed from the active count; the all-affine case uses no integers directly.
