# Compiled rational knots: investigation record

Date: 2026-09-05. The complete construction and proofs were promoted after
independent review to
[rational pure-power graphs with near-minimum integer counts](../results/rational-power-compiled-integer-precision.md).

The final theorem covers every rational exponent greater than one supplied
in binary, with a polynomial-size rational construction using at most
`p_conv+7r+1` integers. The sharper `p_conv+13r/2+1` bound holds when every
exponent is at least two. The promoted file retains the compiler, certified
integer inverse, rational-series inverse, scaled geometry, attribution, and
supporting verification.

Independent reviews:

- [First full proof audit](review-compiled-rational-knot-formulations.md).
- [Second full proof audit](review-compiled-rational-knot-formulations-second.md).
- [Additional integer-primitive bit audit](review-compiled-rational-knots-bit-conditioning.md).
- [Primary-source and novelty audit](compiled-rational-knot-formulations-novelty.md).

The earlier coupled-output target is now covered for dense polynomial
encoding by the [coupled separable vector theorem](../results/convex-separable-vector-oracle-curvature-rank-precision.md),
including arbitrary unconditional oracle error bodies. Its size guarantee
uses numerical degrees; it does not extend this note's binary-exponent
representation guarantee to every coupled mixture. Scalar sums and independent outputs are covered by the
[convex-polynomial construction](../results/convex-polynomial-compiled-integer-precision.md).
The coefficient-sum benchmark alone cannot attain that comparison, as shown in the
[allocation degree-gap example](positive-polynomial-allocation-degree-gap.md).
