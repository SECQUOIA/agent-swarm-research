# Independent review: compiled knots with binary-encoded power exponents

Date: 2026-09-05. Reviewer: `potential_flow_review`.

**Verdict: PASS**, including Section 6's strengthening to rational exponents `alpha>=2` and Section 7's extension to every rational `alpha>1`. I reviewed [the full candidate](compiled-rational-knot-formulations.md), the earlier degree-independent lower bound, and the construction's integer-count and bit-complexity claims. The Boolean compiler and output interpolation are classical supporting tools; this is a proof audit, not a claim of priority for those mechanisms.

The final scope is one pure coordinate power per active coordinate, shared across outputs through nonnegative rational coefficients, plus arbitrary rational affine terms. Exponents may be rational numbers strictly greater than one, supplied in binary. The unconditional error body must satisfy the stated allocation-oracle assumptions. The comparison is with arbitrary convex mixed-integer lifts under the same whole-graph error definition. The stronger constant for exponents at least two remains a valid separate corollary.

## 1. The compiler uses only the declared index integers

A deterministic computation of polynomial bounded length can be unrolled into a polynomial-size acyclic Boolean circuit. The rational instance data and precision are constants in this circuit; only the cell-index bits are inputs. Data-dependent branches can be compiled through flags and selection gates, so early termination does not create a variable-length formulation. This is a uniform construction, not a separate nonuniform circuit-existence assumption.

The given AND inequalities and NOT equality force their output to the correct Boolean value when their inputs are Boolean. Induction in circuit order therefore forces every internal and output wire to zero or one once the declared index inputs are integral. Their continuous declarations do not weaken the integer-feasible set.

For such a forced Boolean wire `v`, the four inequalities for `t=theta*v` are exact: if `v=0` they force `t=0`, and if `v=1` they force `t=theta`. The wire itself needs no separate integrality declaration. Applying this to all output bits gives exactly the interpolated rational coordinates. A dyadic coordinate equal to one needs an integer-place output bit in addition to its fractional bits; this changes the circuit size by a constant and not the declared binary count.

Only the `L` index inputs are declared binary. Computing `k+1`, including the endpoint `2^L`, uses internal bits and does not require a new integer. The formulation is not claimed ideal when the input integrality restrictions are relaxed.

## 2. Integer exponents: certified rounded powering

Downward fixed-point multiplication on `[0,1]` preserves the lower-bound property. If powers of exponents `a,b` have errors bounded by `(a-1)2^(-P)` and `(b-1)2^(-P)`, their rounded product has error at most `(a+b-1)2^(-P)`. This remains valid for squaring because it simply uses the same error bound twice. The initial accumulator one is exact; multiplication by it introduces no rounding error on the existing fixed-point grid.

Exponentiation by squaring consequently gives

```
0<=s^D-A<=(D-1)2^(-P)<=tau
```

using `O(log D)` multiplications of `O(P)`-bit fixed-point integers. The base is exact because every tested bisection point has no more fractional bits than the prescribed precision. This avoids constructing the exact numerator or denominator of `s^D`, which could have exponentially many bits.

The two decisive comparison cases safely update the root bracket. In the remaining case, both `u` and `s^D` belong to `[A,A+tau]`, so `|s^D-u|<=tau`. Since an interior grid index has `u>=2^(-2L)` and `tau=delta*2^(-2L)/16`, the power remains at least `u/2` between the tested point and the root. On that segment,

```
D*z^(D-1)>=z^D>=u/2.
```

The inverse-error bound `|s-u^(1/D)|<=2tau/u<=delta/8` follows. Thus an unresolved exact comparison is a safe stopping event, not an oracle requirement or possible infinite loop. If it never occurs, the prescribed number of bisections gives the required small bracket. Endpoints are handled exactly and every output has one common dyadic precision after padding.

The precision is `P=O(log D+L+log(1/delta))`. The loop count, each multiplication, rational comparisons, and the compiled circuit size are polynomial in the binary degree encoding and other inputs. In the gadget, `delta=p/(16D)` adds only `O(log D)` precision bits. A numerically huge exponent is therefore compatible with polynomial construction size.

## 3. Approximate knot order is unnecessary

For exact inverse-power knots, the selected chord lies above the convex power graph. The first interval has error `h^2(theta-theta^D)<=h^2`. On later intervals, the candidate's input-length and curvature estimates combine to

```
[(D-1)/(2D)]*((a+h)/a)^(2-4/D)*h^2<=2h^2.
```

Here `a>=h`, so the ratio is at most two, and the exponent is in `[0,2)`. The stated bound `4h^2` is conservative. These estimates include `D=2`.

Replacing the two exact inverse knots by approximations of error at most `delta` changes their interpolated input by at most `delta`. Since both inputs remain in `[0,1]`, the `D`-Lipschitz bound gives

```
-D*delta<=y-x^D<=4h^2+D*delta.
```

The proposed output band therefore admits the exact graph value at every represented input and bounds every admitted graph error by `4h^2+2D*delta`.

The represented inputs cover the entire unit interval even if adjacent approximate knots are reversed or equal. The deterministic knot procedure returns the same dyadic result whenever a shared index is requested, so the consecutive segments form one continuous path from input zero to input one. The intermediate value theorem gives coverage. Every point on every segment obeys the same error estimate, so folds introduce no invalid distant graph points.

With the specified `L` and `delta`, `4h^2<=p/4` and `2D*delta=p/8`. Thus the bound `3p/8` is correct. None of this reasoning assumes an ideal LP relaxation or a monotone approximate knot sequence.

## 4. Rational exponents: all arithmetic has polynomial bit length

For interior `t=k/2^L`, the integer normalization `v=2^e t in [1,2)` uses `1<=e<=L`. In the logarithm series, `z=(v-1)/(v+1)` lies in `[0,1/3)`, and the comparison series at two has `z=1/3`. Integrating the geometric series gives the logarithm identity. Bounding its positive tail yields the stated loose error `3*9^(-N)`.

The truncated series increases with its argument. Consequently

```
A=beta*(H_N(v)-e*H_N(2)) in [-L,0],
a=beta*log t in [-L,0],
|A-a|<=delta/8.
```

These bounds also hold when `beta=2/alpha` is very small. Multiplication by `beta<=1` can only improve the error estimate.

The power-of-two scaling integer `M` satisfies `2L<=M<4L`, so `q=A/M in [-1/2,0]`. For odd `J`, the Taylor polynomial is a positive lower approximation to `exp(q)`. Its value is at least `1+q>=1/2`, because the subsequent even/odd pairs are nonnegative. The alternating-series remainder is at most `2^(-(J+1))`. Raising the approximation to the `M`th power multiplies this error by at most `M`, giving `delta/16`. The exponential is one-Lipschitz on the nonpositive axis, so the logarithm approximation adds at most `delta/8`. Final downward dyadic rounding contributes at most `delta/4`, for total `7delta/16`.

The exact rational arithmetic here stays polynomial. The logarithm and exponential series have only `O(log(L+1)+log(1/delta))` terms. Numerator and denominator lengths for their exact finite sums are polynomial in this term count, the rational argument size, and the exponent encoding. The final integer power is only `M<4L`, rather than the potentially huge numerator of `alpha`, so it multiplies the rational bit lengths by only a polynomial factor. A common output precision and exact endpoint handling make this algorithm suitable for the same circuit compiler.

For `x^alpha` with real `alpha>=2`, the chord proof and Lipschitz estimate hold with `D` replaced by `alpha`; the second derivative exists with the required endpoint behavior. Therefore the rational inverse-knot algorithm gives the same graph band and binary count for binary-encoded rational exponents.

## 5. Whole-system containment and the count

For a feasible allocation `p`, each coordinate error has magnitude at most `3p_i/8`. Nonnegative output coefficients imply

```
|w-f(x)|<=C*p
```

coordinatewise. A convex unconditional body contains the coordinate box below any of its nonnegative points, so `C*p in K` proves the whole-output error guarantee. Conversely each exact coordinate graph value can be selected in its own band; this admits every exact whole-graph point. Affine terms contribute no approximation error.

Using the allocation guarantee `product p_i>=exp(-1)D_alloc` gives

```
sum_i L_i<=Phi+3r+1/(2 ln 2).
```

The previously reviewed lower bound also extends to real exponents at least two. Its key scalar step uses only convexity of `x^(alpha/2)`:

```
(a^alpha+b^alpha)/2-((a+b)/2)^alpha
 >=(a^(alpha/2)-b^(alpha/2))^2/4.
```

The coordinate map `x_i -> x_i^(alpha_i/2)` is a cube homeomorphism. The transformed-support covariance and volume argument has no polynomial encoding or exponent integrality requirement. Thus `p_conv>=Phi-A_r` with the same `A_r<7r/2` applies, yielding

```
p_out<=p_conv+(13r/2)+1.
```

The dimension-zero case can be handled as an entirely affine system with no binaries. For positive active dimension, all allocation and radius assumptions remain those of the imported oracle theorem. The current result does not extend this bound to arbitrary mixtures of several powers on one coordinate.

## 6. The extension to every rational exponent greater than one

For `1<alpha<2`, put `s=alpha-1`. On `[a,b]` with `b>0`, the second derivative has lower bound `alpha*s*b^(alpha-2)`. Strong convexity therefore gives a midpoint Jensen gap of at least `alpha*s*b^(alpha-2)*(b-a)^2/8`, extending to `a=0` by continuity. Since `u^(alpha/2)>=u` on `[0,1]`,

```
b^(alpha/2)-a^(alpha/2)<=b^(alpha/2-1)*(b-a).
```

These statements imply the proposed `s/8` transformed-square lower bound. For exponents at least two, the earlier `1/4` bound is stronger. Hence `s=min(1,alpha-1)` gives a common valid inequality for all exponents greater than one.

The scaled coefficient matrix is correctly `C_eff,ji=c_ji*s_i`. For two independent support points, expectation of a squared coordinate difference is twice its variance. The new Jensen factor `1/8` therefore makes `diag(Sigma)/4` a feasible allocation. Hadamard and the same covariance-volume bound produce the factor `2^r`, giving `A'_r=A_r+r/2<4r`. The coordinate change needs only to be a homeomorphism in this volume argument; its concavity for exponents below two creates no gap.

The scaled chord upper bound is also correct. On the first cell,

```
theta-theta^alpha<=s*theta*(-log theta)<=s/e.
```

On later cells the inverse map is convex, so its input interval length is at most `(2/alpha)*b^(2/alpha-1)*h`. The maximum power curvature is at the lower input endpoint. Combining them yields

```
[s/(2alpha)]*(b/a)^(4/alpha-2)*h^2<=2s*h^2,
```

because `b/a<=2` and `0<4/alpha-2<2`. The safe bound `4s*h^2` follows.

Using `delta=s*p/(16alpha)` then gives graph error at most `3s*p/8`. The rational series algorithm extends exactly as claimed: `beta=2/alpha<2` doubles the logarithm error and range bounds; taking `4L<=M<8L` retains `A/M in [-1/2,0]`. All subsequent exponential, rounding, and bit-complexity estimates are unchanged. In particular, when `alpha` approaches one, `s` may be small but its reciprocal requires only polynomially many bits in the rational exponent encoding. No operation is repeated a number of times proportional to `1/s`.

Applying the same allocation and count proof to `C_eff` gives

```
p_out<=Phi_eff+3r+1/(2 ln2)<=p_conv+7r+1.
```

This confirms Section 7's final scope and constant. Affine powers may be treated outside the active list. The proof does not cover concave exponents below one or arbitrary mixtures of different powers on one coordinate.

## Independent checks and conclusion

I independently implemented the two inverse-knot procedures with exact rational/fixed-point arithmetic and compared their outputs with 180-digit reference powers. All 50 integer tests passed, including `D=2^128+7`, and all 40 rational-exponent tests passed, including `alpha=(2^40+1)/3`. The tests included both exact endpoints, the smallest positive index, a middle index, and the last interior index, with dyadic resolutions two and seven and tolerance `1/(256*exponent)`. These are numerical checks of the proof's observable approximation claim, not substitutes for its certified error bounds.

I also reran the author's updated checker after Section 7 was added; it includes exact rounded-power checks, inverse approximations, and scaled Jensen/chord checks for exponents below two and very close to one.

No mathematical correction is required. The circuit construction removes the dense-degree restriction while retaining only the original cell-index integers. Both rational-exponent extensions are sound. The generic compiler, Boolean-output interpolation, rounded arithmetic, and elementary series should retain their classical attribution; the whole-formulation comparison and its scope require their own qualified source assessment.
