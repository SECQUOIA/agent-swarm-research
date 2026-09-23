# Independent audit: positive-polynomial double-logarithmic degree overhead

Date: 2026-09-05. Reviewer: `graph_precision_second_review`.

**Status: PASS.** Reviewed [the candidate](positive-polynomial-loglog-degree-precision.md), including the supporting scalarization, degree-independent covariance lower bound, implied-integral layer selectors, exact power recurrences and all count constants. This is a proof audit, not a novelty certification.

## Scalarization and lower bound

A strictly positive common allocation with all coordinates strictly below one maps into the interior of `K`. The positive determinant optimum exists by compactness and is attained away from the zero-coordinate boundary. The normal-cone chain and sum rules therefore apply at the optimum, yielding the displayed multiplier relation with a nonnegative cap multiplier and the stated complementarity. This qualification does not require differentiability of the body or an interior optimum.

The nonnegativity adjustment of the body normal is valid. At a positive coordinate of `Cp*`, a small coordinate decrease stays in `K`, so the outward normal component is nonnegative. At a zero coordinate, nonnegative `C` and strictly positive `p*` force the whole corresponding row of `C` to vanish. Removing the associated normal component leaves both `C^T lambda` and `lambda^T Cp*` unchanged. For an unconditional body, its support function is invariant under componentwise absolute values and is monotone in those absolute values. Hence removal cannot increase support; since `Cp*` is still in `K`, support cannot fall below the unchanged contact value either. The modified vector remains a normal and is nonnegative.

The one-constraint determinant allocation has exactly the same optimum. The concave logarithm's tangent inequality, stationarity, and cap complementarity prove this globally for all positive feasible allocations; a zero coordinate gives product zero. This remains true when some coefficients `A_i` vanish: stationarity and complementarity force `p_i*=1` there. If the body multiplier itself is zero, all coordinates are one and the proposed lower bound is trivial. If it is nonzero, the body's interior implies its support value is positive. The proof does not require rational or computable optimal multipliers.

For each positive `A_i`, the normalized polynomial has nonnegative coefficients summing to one. Its square root is the Euclidean norm of nonnegative convex coordinate functions `sqrt(d_k)x^(k/2)`, and is therefore convex. This composition argument is valid for odd powers and at zero. It is also continuous and strictly increasing from zero to one. Zero-`A_i` coordinates use the identity map.

Squaring the midpoint convexity inequality gives the claimed Jensen estimate with constant `1/4`. Scalarizing a same-parity graph contact pair bounds its Jensen error by `h_K(lambda)=b`. After the coordinate homeomorphism, averaging independent uniform points gives `(1/2)sum A_i Sigma_ii<=b`. Thus `Sigma_ii/2` is a feasible allocation for the single-constraint problem; its cap follows from variance at most `1/4`. Equality of allocation optima, Hadamard, and the standard covariance-volume inequality give exactly the factor `2^(r/2) omega_r(r+2)^(r/2) sqrt(D_alloc)`.

Taking closures of parity supports before transformation is valid by continuity and closedness of `K`. The transformed compact supports cover the unit cube. Zero-volume supports require no estimate. Consequently the degree-independent lower bound `Phi-A_r` follows without a Jacobian or an assertion of volume preservation. For positive `r`, the previously reviewed Gaussian-volume estimate gives `A_r<7r/2`; the all-affine zero-dimensional case has an exact zero-integer formulation directly.

## Layer geometry and exact formulation

The stated intervals cover the unit interval, meeting only at shared endpoints. On the last interval, the normalized curvature is bounded by `D(D-1)/D^2<=1`. On the other intervals, `s<=1/2` and the upper endpoint is `1-s`. For `k>=3`, with `v=(k-2)s`, the estimate

```
k(k-1)s^2(1-s)^(k-2) <= (v+1)^2 exp(-v) <= 4/e < 2
```

is valid. The separate `k=2` estimate is also correct. Thus two is a uniform curvature bound for every monomial after normalizing its selected layer.

For integral layer-code bits, each unmatched selector is forced to zero by at least one mismatched bit inequality. At a valid code the remaining selector must be one by their sum constraint. At an unused code every selector would be zero, so that assignment is infeasible. This proves that the selectors are integral at every integer-feasible point despite being declared continuous. Their product hulls are therefore exact for the purpose of the final MILP; no integrality claim is needed at fractional code assignments.

The original coordinate equations imply, on the unique selected layer,

```
a=ell+s a_0,  rho=s eta,  x=ell+s(a_0+eta).
```

Because `a_0<=1-h` and `0<=eta<=h`, the entire segment from `a` to `x` stays in that layer. Conversely, every original coordinate is represented by a layer and a local prefix/residual pair, including the final endpoint. Depth `L=0` gives the exact special case `a_0=0`, `h=1`, with no prefix products.

For a bounded nonnegative variable `v`, the intermediate `a_0 v` is computed once using the prefix bits. Summing `ell_j theta_j v+s_j theta_j(a_0 v)` then gives `a v` exactly. The same construction works for both power and power-times-residual recurrences. Their bounds are valid inductively: `v_k=a^k` lies in `[0,1]` and `t_k=a^k rho` lies in `[0,h]`. This also supplies appropriate bounds for every intermediate product. Computing the intermediate prefix product once avoids an extra product of layer and prefix counts.

The stated per-coordinate size `O(D_i(L_i+J_i+1)+J_i S_i)` follows. All layer coefficients are dyadic with `O(log D_i)` bits; recurrence coefficients do not involve expansion into large binomial polynomials. The depth and allocation encoding are polynomial under the previously reviewed rational allocation oracle. The construction is polynomial in the numerical degree, as the dense input model requires.

## Error and count

Taylor's integral remainder on a selected layer, together with normalized curvature at most `2C_ji`, gives a nonnegative remainder at most `C_ji h_i^2`. Summing coordinates yields `0<=f_j-T_j<=(Cp)_j`. The proposed rectangle contains the exact graph. Any point of that rectangle has absolute error at most `Cp`, rather than twice `Cp`, because both the true value and admitted value lie in the same interval of that width. Unconditionality then gives the whole-body guarantee.

The ceiling estimate gives the finite binary upper bound `Phi+r+sum S_i`. The rational allocation oracle loses at most one in natural-log product, hence adds at most `1/(2 ln 2)` to this count. Combining with `A_r<7r/2` gives the advertised rational construction bound

```
p_out <= p_conv + 9r/2 + sum_i ceil(log2(ceil(log2 D_i)+1)) + 1.
```

No step needs an additive `sum log D_i` integer term. The result does retain numerical-degree dependence in continuous formulation size and construction time.

## Independent exact checks

A separate Python `Fraction` checker verified:

- **737** exact maximum-curvature inequalities at layer upper endpoints.
- **33,165** exact layered power-recursion and Taylor-remainder cases.
- **8** unused selector codes, which correctly admit no one-hot assignment.

The cases used degrees `2,3,4,7,16,31,64`, all layers, all prefix indices for depths zero through three, and residuals `0,h/3,h`. Every check passed. They supplement the symbolic proof and explicitly exercise zero-prefix depth, shared layer endpoints and the last interval.

No mathematical correction was needed in the reviewed candidate. Its scope remains nonnegative separable polynomial coefficients on the original nonnegative cube and an unconditional convex error body. The argument does not extend as written to signed coefficients, arbitrary nonseparable monomials, or polynomial time in the binary length of an unbounded sparse exponent.
