# Second independent audit: compiled rational knots

Date: 2026-09-05. Reviewer: `graph_precision_second_review`.

**Status: PASS, including Sections 6 and 7 on binary-encoded rational exponents.** Reviewed [the promoted result](../results/rational-power-compiled-integer-precision.md). Its rational MILP construction is polynomial in the bit encoding of every rational exponent `alpha_i>1`, with `p_out<=p_conv+7r+1`. The sharper `p_out<=p_conv+13r/2+1` remains valid when all exponents are at least two. The integer-exponent, rational-exponent and scaled-curvature proofs were checked separately.

## Circuit compilation and integer count

A deterministic computation with an explicit polynomial time bound can be unrolled uniformly into a polynomial-size Boolean circuit. Here the instance data, precision and loop bounds are fixed constants; only the cell-index bits vary. Early stopping can be represented by a state flag through the remaining bounded steps. Exact arithmetic on polynomial-bit words and their comparisons have polynomial circuit size. This does not enumerate all possible indices.

The gate constraints have the claimed property. A NOT gate is fixed by its input, and an AND gate is uniquely zero or one at each pair of Boolean inputs. Acyclic induction therefore fixes every internal and output wire to its correct Boolean value once the `L` cell bits are fixed. These wires need only continuous declarations. A product of a wire with the interpolation parameter is then exact under its four displayed inequalities, because that wire is already forced to zero or one at every integer-feasible point. No auxiliary integrality declaration is hidden in the construction.

All endpoint coordinates can share the same index bits and interpolation parameter. A common dyadic precision can be chosen as the largest required precision among the computed coordinates, padding shorter outputs with zeros. The endpoint value one uses the usual additional integer-position output bit. This changes neither the polynomial size nor the declared integer count. The general compiler also handles `L=0`, when all circuit input data are constants; the power application uses `L>=2`.

The proof makes no ideal-relaxation claim, which is essential. With fractional input bits the gate inequalities can admit fractional internal wires; the result concerns the integer-feasible set.

The source attribution is appropriate. [Avis, Bremner, Tiwary and Watanabe, Lemma 1](https://arxiv.org/pdf/1408.0807) explicitly establishes the input-0/1 property of the continuous circuit polytope and credits that lemma to Valiant. [Filos-Ratsikas, Hansen, Høgh and Hollender, Section 3.4](https://arxiv.org/pdf/2312.01237) treats Boolean-circuit representations of piecewise-linear interpolation and multiplication by output bits. These are direct antecedents of the supporting machinery. This audit does not certify novelty of the pure-power consequence.

## Integer-exponent inverse knots

The rounded-power estimate is valid even though an exponentiation-by-squaring computation reuses intermediate values. A stored approximation to exponent `a` has absolute error at most `(a-1)2^-P` and lies below the exact value in `[0,1]`. Multiplying approximations to exponents `a,b` adds at most their two errors plus one rounding unit, giving `(a+b-1)2^-P`. Squaring is the case `a=b`; its repeated input contributes twice, as required. The initial exact accumulator one can be handled without rounding loss. No multiplication requires an exact rational number with bit length proportional to the numerical exponent.

Every bisection test point is representable exactly at precision `P`, because `P>=R+1`. Fixed-point products have at most twice the stored bit length before truncation. Thus `[A,A+tau]` is a certified enclosure and is computed using `O(log D)` polynomial-bit multiplications.

The two strict comparison branches maintain a true root bracket. In the uncertain branch, both `s^D` and `u` lie in the same interval of width `tau`, so `|s^D-u|<=tau`. Since `u>=2^-2L` and `tau=delta*2^-2L/16`, both power values are at least `u/2`. On the interval between the test point and the true root, the derivative obeys `D z^(D-1)>=z^D>=u/2`. Hence the point error is at most `2tau/u<=delta/8`. This proves safe termination without any exact-equality test.

If there is no uncertain comparison, `R=ceil(log2(2/delta))` bisections give bracket width at most `delta/2`; the final midpoint is valid. Earlier termination values and the final midpoint can all be padded to `R+1` fractional bits. Both original endpoints are treated exactly. All branch decisions and required integer ceilings can be computed by exact rational and dyadic comparisons.

The precision bound `P=O(log D+L+log(1/delta))` is correct, with rational input encoding lengths included. The resulting time and output size are polynomial in the binary exponent length, rather than in its numerical value.

## Graph containment and error

The chord estimate is valid on the first transformed grid interval and on all remaining intervals. On the first it is exactly `h^2(theta-theta^D)<=h^2`. On a later interval, concavity of the inverse power bounds its input length by `(2/D)a^(2/D-1)h`; multiplying its square by the maximum forward-power curvature gives the displayed bound at most `2h^2`. The stated `4h^2` is therefore safe.

The compiled endpoint approximations may be nonmonotone or repeated. This does not invalidate either claim. Each segment stays in `[0,1]`, and its comparison with the exact endpoint segment gives the same uniform error estimate. The deterministic knot algorithm returns the same rational number whenever a shared endpoint is requested, so the consecutive segments form a continuous path from zero to one. The intermediate value theorem proves input coverage. A vertical segment at a repeated input knot is allowed and still satisfies the error estimate.

With the shared interpolation parameter, `|x-x_0|<=delta`, and the forward power is `D`-Lipschitz on the unit interval. The stated band consequently contains the exact graph and permits absolute error at most `4h^2+2D delta<=3p/8`. There is no factor lost by having both endpoint and band error: the two-sided interval calculation gives precisely that sum.

The feasible rational allocation supplies product at least `exp(-1)D_alloc`. Summing cell depths gives `Phi+3r+1/(2 ln 2)` binaries. Shared scalar power approximations across outputs give absolute error bounded by `(3/8)Cp`, which belongs to the unconditional error body by domination. The previously reviewed parity-volume lower bound applies to all finite exponents without an input-encoding condition, giving the final additive `13r/2+1` comparison.

## Rational-exponent extension

For an interior knot, an integer `1<=e<=L` gives `v=2^e t` in `[1,2)`. The atanh series in the note has positive terms and a geometric tail at most `3*9^-N`. Its choice of `N` therefore gives the claimed error in

```
A=(2/alpha)[H_N(v)-e H_N(2)].
```

Because `H_N(v)<=H_N(2)<log 2<1` and `e>=1`, both `A` and the exact logarithmic exponent lie in `[-L,0]`. Their difference is at most `delta/8`. These bounds do not depend on the numerical magnitude of the rational exponent.

The power of two `M` satisfying `2L<=M<4L` gives `q=A/M` in `[-1/2,0]`. An odd Taylor truncation for the exponential lies below the exponential. Grouping its even/odd pairs after `1+q` shows it is at least `1/2`. The next-term remainder is at most `2^-(J+1)`, so the stated `J` gives approximation error at most `delta/(16M)`.

Raising this rational Taylor value to the power `M` incurs error at most `delta/16`, by the Lipschitz bound for that power on `[0,1]`. The exponential perturbation contributes at most `delta/8`, and final downward dyadic rounding at most `delta/4`. Their sum is `7delta/16<delta`. The output remains in `[0,1]` with both endpoints set exactly.

The rational series have polynomially many terms and polynomial numerator and denominator lengths. Crucially, the final exact power has exponent `M<4L`, so its rational bit lengths grow by only a polynomial factor. The original exponent `alpha` appears only in rational arithmetic and the requested error precision; neither its numerator nor its denominator is used as a numerically large exact-power exponent. This closes the sparse rational input bit-complexity claim without an elementary-function oracle.

The geometric proof and lower bound both extend to every real `alpha>=2`: the forward power is twice continuously differentiable on the nonnegative unit interval, the inverse-power chord calculation uses only the displayed real exponent inequalities, and `x^(alpha/2)` is a convex increasing homeomorphism. For rational binary input, the newly proved series algorithm supplies the required uniform computation. The same integer-count constant therefore applies to the stated rational-exponent extension.

## Independent verification

The reproducible [second-review checker](../code/quadratic_rank/check_compiled_knots_second.py) uses a separate implementation of both knot algorithms. It passed:

- **65 exact rational root-enclosure checks** for integer exponents through 64.
- **75 exact rational rounded-power error checks**.
- **8 numerical checks at 300-digit precision** for integer exponents as large as `2^200+51`.
- **40 numerical checks at 300-digit precision** for rational exponents, including large numerators and denominators and `alpha=1+2^-90`.

The numerical cases supplement the symbolic proof; they do not certify a uniform approximation bound. The exact checks exercise endpoints, interior indices and multiple grid depths. No mathematical correction was required in the reviewed candidate.

## Limits

This is a polynomial-size existence and construction theorem, not a claim of practically small circuit formulations. The whole-system class retains one common power per coordinate across outputs, nonnegative coefficients and the stated unconditional error body with its oracle assumptions. The theorem does not yet remove degree overhead for arbitrary positive mixtures of several powers on a coordinate, and it does not claim an ideal continuous relaxation.

## Final scope update: exponents strictly above one

Section 7 was independently read after the initial review, and it also passes. For `1<alpha<2`, the lower curvature bound on `[a,b]` is `alpha(alpha-1)b^(alpha-2)`. Subtracting its quadratic proves the stated strong-convexity Jensen estimate, including `a=0` by continuity. Because `u^(alpha/2)>=u` for `u in [0,1]`, the resulting bound dominates `(s/8)(b^(alpha/2)-a^(alpha/2))^2`, where `s=alpha-1`. The earlier convex-square argument covers `alpha>=2` with `s=1`.

Expected same-parity Jensen errors therefore make `diag(Sigma)/4` feasible for the scaled allocation with `C_eff,ji=c_ji min(1,alpha_i-1)`. Its variance caps hold, and the determinant-volume calculation gives precisely `A'_r=r+log2[omega_r(r+2)^(r/2)]<4r`. The coordinate map remains an increasing homeomorphism even where its convexity is lost; the separate curvature argument supplies the needed Jensen inequality.

For `1<alpha<2`, the first grid interval has error `h^2(theta-theta^alpha)<=s h^2/e`. On later intervals the inverse power is convex, so its interval length is bounded using its derivative at the right endpoint. Forward-power curvature is bounded at the left endpoint. Their product gives exactly `[s/(2alpha)](b/a)^(4/alpha-2)h^2<=2s h^2`, since `b/a<=2` and the exponent lies in `(0,2)`. Thus the uniform `4s h^2` estimate is valid.

The inverse exponent `beta=2/alpha` is below two. Multiplying the logarithm truncation allowance by two gives `|A-beta log t|<=delta/8`, now with `A in [-2L,0]`. Choosing a power of two `4L<=M<8L` restores `A/M in [-1/2,0]`; every remaining series and bit-size estimate remains valid. The small rational scale `s` has polynomial bit encoding even as the exponent approaches one. Accordingly `delta=s p/(16alpha)` requires only polynomial additional precision.

The scaled output band contains the graph and has absolute error at most `3s p/8`. Summing depths and comparing with the scaled lower bound gives the claimed `7r+1` additive overhead. The updated independent checker also passed fifteen added rational-exponent cases below two, including values within `2^-90` of one. Affine powers can be removed separately. Concave powers below one and arbitrary mixtures on one coordinate remain outside this result.
