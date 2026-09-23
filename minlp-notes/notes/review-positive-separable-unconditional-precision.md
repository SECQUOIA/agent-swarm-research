# Independent audit: positive separable precision under unconditional error bodies

Date: 2026-09-05. Reviewer: `graph_precision_second_review`.

**PASS.** I independently reviewed both [the unconditional-body precision extension](positive-separable-unconditional-error-precision.md) and [its rational log-product oracle](rational-log-product-convex-body-oracle.md). The finite constants, polynomial rational allocation, and final binary-count bounds are correct. No correction was needed.

## Unconditional domination and transformed Jensen bounds

A convex body invariant under coordinate sign changes contains the full coordinate box spanned by the sign changes of each of its points. Therefore coordinatewise absolute-value domination preserves membership. This is the exact property used in both halves of the precision theorem; central symmetry alone would not suffice.

For graph points whose lifts have the same integer parity, the Jensen vector belongs to the permitted error body and is nonnegative coordinatewise. The previously reviewed scalar power inequality bounds it below by the stated sums of squared transformed-coordinate differences. Compact closure preserves body membership because the body is closed and the Jensen map is continuous.

Uniform sampling is performed on each transformed support. Evaluating the original Jensen vector at inverse images is legitimate because the coordinate transformation is a homeomorphism. Its expectation belongs to the body by convexity and closedness. Twice the transformed covariance diagonal supplies a nonnegative vector dominated by that expectation. Thus the allocation `p_i=2 Sigma_ii/D_i^2` satisfies `Cp in K`. No original-coordinate measure or Jacobian is used. The Hadamard and transformed-volume argument therefore retains exactly the earlier finite lower constant.

For the upper bound, the true output and the permitted output both belong to the rational Taylor interval of width `(Cp)_j/2` in each coordinate. Their error is absolutely dominated by `Cp/2`, so it belongs to the unconditional body. The exact shared prefix-power construction is unchanged, and the final MILP needs only those rational interval bounds. It does not claim to describe an arbitrary curved body exactly by finitely many linear inequalities.

For diagonal PSD quadratics the expected Jensen vector is `C diag(Sigma)/4`: the quadratic Jensen discrepancy is one eighth of the Hessian-weighted squared difference, and expectation doubles covariance. This verifies the sharper quadratic allocation and constants. Shared square interpolation errors are dominated by `Cp/8`, giving the stated `p_conv+5r+1` construction after rational allocation.

## Log-product oracle: compact body and explicit radii

The supporting oracle lemma does not need nonnegative `C` or symmetric `K`. Its inner-ball assumption makes a small common positive allocation feasible even for arbitrary signed `C`. With `c=1+sum|C_ji|` and `delta r c<=rho_0/4`, the point `delta 1` is feasible, so the maximum product is at least `delta^r`. Since every allocation coordinate is at most one, every maximizer has every coordinate at least `delta^r`. Restricting coordinates below by `a=delta^r/4` therefore loses no maximizer.

The proposed log-product hypograph is convex and compact. Its maximum last coordinate equals `log D`. I checked all inner-ball constants:

- `a<=delta/4`, giving at least `delta/4` lower-coordinate margin at `p_0=(delta/2)1`; the upper margins are at least one half.
- `||Cp_0||<=rho_0/8`, and displacement within the proposed ball changes `Cp` by at most another `rho_0/8`.
- The log-product value at `p_0` exceeds `t_0` by at least two. Along the ball, coordinates remain at least `delta/4`, so gradient norm at most `4r/delta` bounds log-product variation by one quarter. The last-coordinate variation is at most one quarter as well.
- `t_0+B=b r(r-1)+r+2>=3`, preserving the lower last-coordinate bound.

Thus the closed radius-`sigma` ball is contained in the hypograph, with slack. The outer radius `2(B+r+1)` is conservative. All radii and the center are rational with polynomial encoding lengths, although the inner radius may be exponentially small in the input length. This is allowed because the oracle algorithm depends on its logarithmic encoding.

## Weak separation and its imported optimization guarantee

Coordinate or last-coordinate bound violations have exact rational separators. If `Cp` violates the original body, a strong separator pulls back through `C`. Its new normal cannot vanish because zero belongs to the original body and the queried point violates the inequality. Normalization by its infinity norm meets the cited source's lower bound of one on the Euclidean normal norm.

For a query passing these tests, the logarithmic interval has radius `eta/2`. If `t` exceeds its upper endpoint, the rational tangent based on that upper endpoint is valid for the entire hypograph by concavity and strictly separates the query. Its last-coordinate coefficient is one, so it already has the required normal norm. Otherwise lowering only the last coordinate by at most `eta` reaches the hypograph. This correction cannot cross the lower bound because every allowed allocation has log product at least `-r(rb+2)ln 2>-B`.

I previously checked, and apply here, the exact weak-optimization convention in [Grötschel, Lovász and Schrijver (1981), Definition (5) and Theorem (3.1)](https://ir.cwi.nl/pub/10046/10046D.pdf): the returned rational point is within the requested distance of the body, and its objective is within the requested additive error of the optimum over the original body. The source includes logarithmic accuracy dependence. The hypograph dimension is `r+1>=2`, matching its full-dimensional convex-body setup. Consequently the invoked weak optimizer has precisely the guarantees needed by the subsequent repair.

## Exact rational repair and bit bounds

Let a returned point be within distance `rho` of the hypograph, and let `z` be a nearest feasible point. The displayed repaired point is the convex combination of `z` and a point displaced from the known center by `(sigma/rho)(y-z)`. That displacement has norm at most `sigma`, so the second point belongs to the certified inner ball. Hence the repair is exactly feasible without nonlinear projection or an irrational coordinate computation.

The optimal last coordinate is at most zero and exceeds the feasible center's last coordinate by at most `B`. Therefore repair loses at most `rho+(rho/sigma)B`. Substituting `rho=nu sigma/[4(B+sigma+1)]` makes this less than `nu/4`, comfortably inside the claimed `nu` loss. The repaired allocation is positive and rational, and its log product is at least the repaired last coordinate. This proves the multiplicative product guarantee.

The lower allocation bound has logarithm `O(rb)`, so evaluating logarithms and reciprocal tangent entries needs only polynomial precision bits. The explicit center, radii, weak-optimization query sizes, and repair use polynomial rational encoding. The outer bounded hypograph makes an outer radius for the original body unnecessary in the supporting lemma. An arbitrary strong oracle remains an input assumption; the proof does not infer one from an unspecified body description.

Applying this allocation with `nu=1` adds at most `1/(2ln2)<1` to the earlier benchmark binary count. All polynomial-size prefix constructions remain valid for the stated dense polynomial encoding. Combining the unchanged finite constants gives `p_out<=p_conv+2 sum_i log2 D_i+4r+1`, and the sharper quadratic specialization gives `p_out<=p_conv+5r+1`.

This audit verifies the mathematics and oracle bit model. Attribution of convex optimization and interpolation ingredients, and novelty of the resulting whole-formulation precision guarantee, remain separate from correctness.
