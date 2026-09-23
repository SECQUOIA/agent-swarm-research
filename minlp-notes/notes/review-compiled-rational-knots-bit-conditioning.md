# Independent audit: compiled rational knots and binary exponent conditioning

Date: 2026-09-05. Reviewer: `quadratic_weighted_precision`.
Status: PASS for the complete candidate at
[compiled rational knot formulations](compiled-rational-knot-formulations.md).
This audit particularly checks the coefficient and bit-complexity boundary
requested by root; it also reads the complete graph and integer-count proof.

## Binary exponent arithmetic

The downward-rounded power evaluation has the stated bound. If two approximate
powers have absolute errors bounded by `(a-1)2^-P` and `(b-1)2^-P`, their product
has error at most the sum of those errors, because all exact and approximate
factors lie in `[0,1]`. One further downward rounding adds at most `2^-P`.
This gives `(a+b-1)2^-P`. Squaring may reuse the same approximate factor,
but the same deterministic inequality remains valid; independence is irrelevant.
An initial exact accumulator equal to one causes no extra error. The base
bisection points are represented exactly because `P>=R+1`.

Thus `D2^-P<=tau` is certified with only
`P=O(log D+L+log(1/delta))` bits. Although the error bound contains numerical
`D`, the precision needed contains only `log D`; no exact rational numerator
of the huge power is ever formed. Exponentiation uses `O(log D)` rounded
multiplications of `P`-bit fixed-point values. Intermediate multiplication
before truncation has at most `2P` fractional bits.

For an interior knot, `u>=2^-2L`. The uncertain-comparison case implies that
both `s^D` and `u` are at least `u-tau>=u/2`. Throughout the root segment,
`D z^(D-1)>=z^D>=u/2`. Hence the mean-value distance bound
`2tau/u<=delta/8` is correct and does not depend on a very small derivative
at zero. The endpoint with target zero is handled separately, which is
necessary for this argument. Strict above/below branch tests maintain the
root bracket. If all comparisons are strict, the prescribed number of
bisections gives a bracket of width at most `delta/2`.

All outputs use a common fixed dyadic precision by padding shorter outputs.
The endpoint one requires its integer bit in addition to fractional bits,
which is a harmless constant addition to the representation. Early termination
can be represented by a Boolean flag in a fixed worst-case running time.
The computational claims therefore have polynomial dependence on the sparse
binary exponent length, not the numerical exponent.

## Circuit and interpolation integrality

An acyclic AND/NOT circuit with its primary index bits fixed to zero or one
forces every continuous gate wire to its unique Boolean value. The displayed
AND inequalities are exact on Boolean inputs, and NOT is exact by equality.
The product of a resulting output bit and the continuous interpolation weight
is likewise exact. No additional integrality declarations are needed for those
wires or products. This is a statement about integer-feasible points, and the
candidate correctly avoids asserting an ideal continuous relaxation.

A deterministic polynomial-time bounded computation has a uniformly constructible
Boolean circuit of polynomial size. Each dyadic output is a linear combination
of its computed bits. The coefficient bit lengths grow with output precision,
which was already bounded polynomially. Computing the two endpoints at index
`k` and `k+1` uses a carry operation inside the circuit, rather than another
integer input. The two calls share the same specified deterministic knot routine,
so adjacent cell segments join at exactly the same rational value.

## Whole graph and count

The approximate knot sequence need not be monotone: the continuous polygonal
path joining its endpoint values zero and one still covers the input interval.
Every computed endpoint is in `[0,1]`; interpolation preserves that bound.
The comparison interpolation of exact inverse knots differs by at most `delta`,
so the uniform chord and Lipschitz arguments from the reviewed pure-power theorem
apply. The two-sided rational band contains every exact graph point and admits
only error at most `3p/8`.

With `delta=p/(16D)`, both its input bit length and `log(1/delta)` are polynomial
in the bit lengths of `p` and `D`. The allocation oracle supplies `p` with
polynomial bit length independently of the exponents. Thus each compiled gadget
has polynomial size in sparse input length and still uses only the prescribed
cell-index bits. The count `p_out<=p_conv+13r/2+1` follows with the same reviewed
finite lower bound. No unresolved coefficient, conditioning, graph-containment,
or count issue was found.

The generic computation compiler and interpolation method require the attribution
already identified in the candidate. This proof audit does not establish novelty
or practical runtime of the resulting formulation.
