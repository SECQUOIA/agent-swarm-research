# Independent audit: positive separable polynomial integer precision

Date: 2026-09-05. Reviewer: `graph_precision_second_review`.

**PASS.** I independently reviewed [the positive separable polynomial candidate](positive-separable-polynomial-integer-precision.md). Its finite allocation bounds, arbitrary-convex-lift lower bound, exact shared prefix-power formulation, and polynomial rational construction are correct. This includes growing degrees under the explicitly stated dense input representation. No correction was needed.

## Scalar inequality and transformed parity supports

For `2<=k<=D`, convexity of `u^(k/2)` and nonnegativity of its values give

```
((a+b)/2)^k <= ((a^(k/2)+b^(k/2))/2)^2.
```

Subtracting this upper bound from the average of `a^k` and `b^k` yields one quarter of the squared difference of the half powers. The map `v -> v^(D/k)` is `D/k`-Lipschitz on `[0,1]`, so the half-power difference for degree `k` dominates `k/D` times that for degree `D`. Since `k^2/4>=1`, the claimed `D^(-2)` Jensen lower bound follows. This reasoning applies to odd degrees as well; no polynomial identity for the intermediate half power is assumed.

The midpoint of two graph lifts in the same integer parity class is integer-feasible. Its output discrepancy is the sum of the nonnegative univariate Jensen discrepancies, with affine terms canceling. Therefore it bounds the stated weighted sum of squared transformed-coordinate differences by each output tolerance. Taking compact closures preserves the inequality by continuity.

The coordinate map `t_i=x_i^(D_i/2)` is a homeomorphism of the active cube onto itself. The transformed compact supports cover that entire cube. Volume and uniform covariance are then defined on the transformed sets themselves. Their measure need not agree with the original sets' measure; the proof never uses such an agreement or a Jacobian formula. No convexity of a parity support or of its image is required.

Averaging squared differences gives twice the corresponding diagonal covariance. Thus `p_i=2 Sigma_ii/D_i^2` is feasible for the allocation problem, and the cube variance cap ensures its coordinate bounds. Hadamard's inequality produces the volume factor `product_i(D_i/sqrt(2))`, exactly as stated. The finite parity cover gives the lower constant `A` with the correct sign of `-r/2`.

The affine and inactive-coordinate reduction is exact: subtract the affine output map, restrict inactive input coordinates to a fixed value for one direction, and reintroduce them as free continuous cube coordinates for the other. Both integer minima are preserved. If no active coordinate remains, the graph is affine.

## Taylor formulation and exact prefix powers

The upper construction stays in the original coordinates. Every chosen grid cell has prefix `a_i` and residual `r_i` with `0<=a_i<=1-h_i` and `0<=r_i<=h_i`, so the entire Taylor segment lies in `[0,1]`. The univariate second derivative is between zero and `D_i^2 C_ji`. Integral Taylor remainder therefore lies between zero and `epsilon_j/2` after applying the allocation inequalities and grid-width choices.

Both the exact output and every admitted output belong to the interval `[T_j,T_j+epsilon_j/2]`. This proves graph inclusion and the claimed error bound. The proof does not confuse a one-sided Taylor underestimate with an equality to the original function.

For each coordinate, the recurrences for `v_k` and `t_k` are exact by induction. At an integer-feasible point every binary-continuous product is forced to its true value by the stated four inequalities. Summing the products multiplies the preceding power by the common prefix. Thus `v_k=a^k` and `t_k=a^k r` for every generated degree. The bounds `0<=v_k<=1` and `0<=t_k<=h` are valid throughout. The construction is acyclic and uses only the existing prefix bits.

Generating both sequences through the necessary degrees takes `O(D_i L_i)` continuous variables and rows. Sharing them across outputs is valid, since the underlying powers are identical. Substitution into every Taylor expression is linear. The depth sum is at most `Phi(p)+sum_i log2 D_i+r`, proving the finite upper bound.

## Rational complexity and constants

The coefficient sums `C_ji` are rational, nonnegative, and have polynomial encoding length. The previously reviewed scalar allocation algorithm uses only these facts. It therefore returns a feasible rational allocation with product at least `exp(-1)D_alloc`, independently of the polynomial degrees.

Grid depths are computed by comparing rational numbers with `2^(2L_i)`, and their sum is polynomial in the coefficient, tolerance, and degree encoding under the dense input model. Each recurrence uses rational powers of two, integer degree factors, and supplied coefficients; it never computes an irrational inverse-power breakpoint or expands a product into exponentially many monomials. The total number of recurrences is polynomial because the dense input explicitly includes the degree ranges. This does not extend to exponentially large exponents supplied only in binary; the note correctly excludes that representation.

The rational allocation increases the benchmark count by at most `1/(2 ln 2)<1`. The Gaussian volume estimate gives `log2[omega_r(r+2)^(r/2)]<3r`, and in fact the additional `-r/2` leaves further slack. Hence `A<sum_i log2 D_i+3r`. Combining the lower bound, grid upper bound, and rational allocation loss yields exactly

```
p_out <= p_conv+2 sum_i log2 D_i+4r+1.
```

The fixed-degree overhead is consequently linear in active dimension, uniformly over coefficient magnitudes, positive tolerances, and output counts.

## Exact checks and scope

I ran 4,750 exact rational Jensen-inequality checks with degrees two through twenty. Inputs were squares of rational numbers, so both sides could be evaluated exactly even for odd degree half powers. The cases included zero, one, coinciding points, unequal points near endpoints, and all lower degrees `k<=D`. Every inequality passed. The analytic proof above covers all real inputs in the interval and all permitted degrees.

Nonnegative coefficients and the nonnegative original box are essential to the lower and upper arguments. The result does not cover cancellation among signed monomials or nonseparable polynomials. This audit verifies the mathematics and encoding claim; novelty assessment remains separate.
