# Independent audit: sparse positive-polynomial circuit precision

Date: 2026-09-05. Reviewer: `graph_precision_second_review`.

**Status: PASS.** Reviewed [the sparse polynomial candidate](sparse-positive-polynomial-circuit-precision.md). Its stated rational polynomial-size construction and binary count are valid in the full sparse input encoding. The supporting [compiled-knot proof](review-compiled-rational-knot-formulations-second.md) and [degree-independent lower bound and layers](review-positive-polynomial-loglog-precision.md) were independently audited before this combined extension.

## Sparse input and computation size

The layer count `J_i=ceil(log2 D_i)` is at most the bit length of the largest supplied exponent. Constructing or selecting all `J_i+1` dyadic layers therefore costs polynomial time in the sparse input. It does not enumerate the unlisted powers. The number of distinct listed exponents across outputs is also polynomial in that input.

The `S_i` layer bits represent an integer `j`; the single weighted linear inequality `j<=J_i` excludes every unused layer code. The local index needs exactly `L_i` bits. At `L_i=0`, it is the constant zero and no index bits or associated operations are required. The endpoint computation can return arbitrary fixed outputs for an excluded layer code, keeping its circuit defined on all input strings.

For a selected layer, both input endpoints are dyadic. The stated common precision `B_i=J_i+L_i+1` is sufficient: even the finest layer and cell have denominator dividing `2^(J_i+L_i)`. The endpoint value one uses the ordinary integer-position bit. Layer selection, shifts, multiplication of the bounded integer index and addition all have polynomial bit cost.

At precision `P_i>=max(B_i,ceil(log2(D_i/eta_i)))`, the input endpoints are represented exactly and downward binary exponentiation gives error at most `k*2^-P_i<=eta_i` for every listed exponent. There are `O(log k)` rounded multiplications, each on polynomial-bit words. A temporary exact fixed-point product has only twice the stored length before truncation; the numerical exponent never multiplies the denominator length. Endpoint zero and one satisfy the same algorithm and bounds.

A common output precision can pad endpoint and monomial output words without changing their values. Compiling these computations jointly costs polynomial size in the input and required precision. Only the `S_i+L_i` input bits are declared integer: acyclic gate constraints force all internal and output wires to their Boolean values at integer-feasible points, and multiplying each such output bit by the single interpolation parameter is exact under the standard four inequalities. The body oracle is not implicitly compiled. It is used first to produce the rational allocation; the subsequent endpoint computation uses only ordinary rational and integer arithmetic on those fixed data.

## Domain coverage and error signs

The exact input endpoint equation gives `x_i=(1-theta_i)a+theta_i b`. Each selected interval is contained in its layer, and the layers and local cells cover the unit interval, including their shared and final endpoints. Thus every original input point has a feasible index and interpolation parameter. All monomials and all outputs for that coordinate share this same parameter.

The previously reviewed layer curvature bound is at most two in the normalized layer coordinate. A local cell of width `h_i` therefore has monomial chord error between zero and `h_i^2/4`. Downward rounding of each endpoint by an amount in `[0,eta_i]` lowers the chord by a convex combination of those two errors, also in `[0,eta_i]`. Consequently

```
-eta_i <= z_ik-x_i^k <= h_i^2/4.
```

The signs in both the approximate-output inequality and the final band are correct. Write `E_j=sum_i C_ji eta_i` and `U_j=sum_i C_ji h_i^2/4`. Then `T_j-f_j` lies in `[-E_j,U_j]`, so the band `[T_j-U_j,T_j+E_j]` contains the exact output. Every admitted output error lies in `[-E_j-U_j,E_j+U_j]`.

Since `eta_i=p_i/4` and `h_i^2<=p_i`, this last absolute error is at most `(Cp)_j/2`. Convex unconditionality implies membership in the required body. The explicit rational output bands suffice; no linear representation of that body is assumed or needed. Shared monomial variables and nonnegative coefficients are essential to this error summation, and both are imposed in the candidate.

## Lower bound and integer comparison

The supporting-scalarization lower proof applies to the finite polynomial functions independent of how their exponents are encoded. It uses the same coefficient sums `C_ji` and therefore the same determinant allocation optimum. No degree-by-degree computation is hidden in this purely geometric lower bound.

The allocation oracle provides a positive exactly feasible rational allocation with product at least `exp(-1)D_alloc`. The ceiling bound for local depths gives

```
sum_i(L_i+S_i) <= Phi+r+sum_i S_i+1/(2 ln 2).
```

Combining this with `p_conv>=Phi-A_r`, `A_r<7r/2`, proves the stated `p_conv+9r/2+sum_i S_i+1` upper comparison. Internal gate variables do not change that count. The full rational formulation has polynomial total encoding length in the sparse coefficients, exponent bit lengths, allocation output and oracle input assumptions.

## Independent exact checks

A separate Python `Fraction` checker passed **3,720 exact monomial interpolation enclosures** and **2,760 exact shared-output graph and band checks**. It used degrees `2,3,7,31,128`, all layers, all local cells at depths zero through three, and interpolation weights `0,1/3,1/2,1`. Two different nonnegative coefficient vectors tested shared monomial values, including zero coefficients. The checks verified both graph containment and the absolute error at both extreme admitted output values. They supplement the symbolic argument, including the separate polynomial bit-complexity proof for arbitrarily large binary exponents.

No mathematical correction was needed. The result retains nonnegative separable polynomial terms with integer exponents at least two, the original nonnegative cube, and the stated unconditional error-body and oracle assumptions. It establishes theoretical polynomial size; it makes no claim of an ideal relaxation or a practically small compiled circuit. Literature novelty is outside this proof audit.
