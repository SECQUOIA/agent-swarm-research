# Second review: sparse positive-polynomial circuit precision

Date: 2026-09-05. Reviewer: `constant_rank_review`.
Reviewed candidate: `notes/sparse-positive-polynomial-circuit-precision.md`.
Relevant compiler and rounded-power dependency:
`notes/compiled-rational-knot-formulations.md`, Sections 1--2.
Verdict: **PASS** for the sparse integer-exponent scope, full graph
containment, stated binary count, and polynomial rational construction.

This audit does not establish publication priority for the compiler,
rounded arithmetic, or their formulation application. The inverse-power
and rational-exponent extensions elsewhere in the compiler note are not
needed for this sparse-polynomial theorem.

## Sparse encoding and exact endpoint computation

The supporting scalarization lower bound is a finite mathematical statement
about nonnegative polynomial coefficients. Its proof places no requirement
on how the finite exponent list is encoded. It therefore gives the same
degree-independent `p_conv>=Phi-A_r` lower bound for sparse input.

For each coordinate, `J_i=ceil(log2 D_i)` is at most the exponent bit
length, and the layer list has only `J_i+1` members. The `S_i` layer bits
and `L_i` local cell bits encode integers by their usual linear binary
expansions. The inequality `j<=J_i` excludes unused layer strings. No
separately declared integer variable for `j` or `q` is needed.

On an earlier layer, `s_j=2^(-j-1)`, and on the final layer
`s_J=2^(-J)`. The exact cell endpoints consequently have dyadic precision
at most `J_i+L_i`; the proposed `B_i=J_i+L_i+1` is safe. The value one
is represented exactly as well, using the usual leading bit in a fixed
point representation. Computing `q+1` uses at most `L_i+1` integer bits.
Variable dyadic shifts are bounded by `J_i+L_i`, so none requires time
proportional to the numerical degree or number of cells.

When `L_i=0`, the only cell is the full selected layer, with the same
endpoint formulas and no precision-index bits. Invalid layer codes can
return prescribed dummy outputs before evaluation and are excluded by
the model. The circuit has a known polynomial worst-case running time
on its entire input bit cube, not just on valid codes.

## Downward exponentiation is polynomial in exponent bit length

Fix an exact dyadic base in `[0,1]` represented with at most `P`
fractional bits. Every approximate power stays in `[0,1]` and below
its exact value. If powers with positive exponents `a,b` have errors
at most `(a-1)2^(-P)` and `(b-1)2^(-P)`, their rounded product has error
at most

```
[(a-1)+(b-1)+1]2^(-P)=(a+b-1)2^(-P).
```

The product error before rounding is at most the sum of the two input
errors, since exact and approximate factors lie in `[0,1]`. One floor
rounding adds at most `2^(-P)`. The initial accumulator one is exact,
and multiplication by it needs no rounding error. This proves the stated
`k 2^(-P)` bound along the repeated-squaring computation, even though
its error estimate involves numerical `k`.

There are only `O(log k)` multiplications. Each multiplies two fixed-point
integers with `O(P)` bits and then discards the extra fractional bits.
Choosing `P>=ceil(log2(D_i/eta_i))` makes the final error at most `eta_i`
for every listed exponent. The additional condition `P>=B_i` keeps
the original endpoint exact. Thus

```
P=O(J_i+L_i+log(1/p_i))
```

suffices with `eta_i=p_i/4`. The numerical degree can be exponentially
large without requiring exponentially many precision bits or arithmetic
steps. Endpoints zero and one are handled exactly by this same arithmetic.
No exact high-degree rational numerator is formed.

## Compiled gates and interpolation introduce no additional integers

A deterministic polynomial-time indexed endpoint algorithm can be unrolled
to a polynomial-size acyclic Boolean circuit, with instance data fixed
as constants. AND and NOT constraints force every continuous gate wire
to its exact Boolean value when the input index bits are Boolean. This
is a direct induction in circuit order and does not require the polytope
to have an ideal continuous relaxation.

I checked the cited primary antecedent,
[Avis, Bremner, Tiwary and Watanabe, Section 3, Lemma 1](https://arxiv.org/pdf/1408.0807).
It gives this input-Boolean propagation property for the circuit polytope
and credits the earlier construction. The candidate properly treats this
as a supporting established tool.

For a computed output bit `v`, its product with `theta_i in [0,1]` is
exactly imposed by the four binary-times-continuous inequalities, because
`v` is already forced to zero or one at integer-feasible points. Linear
combinations of output bits and these products give the stated endpoint
interpolations exactly. Neither gate wires, computed value bits, product
variables, nor interpolation weights require an integrality declaration.

All listed monomials use one common `theta_i` and the same selected exact
input endpoints. Every original input point belongs to some layer and
cell and has its corresponding interpolation parameter in `[0,1]`.
This proves coverage in the original input coordinate; it does not rely
on an approximate inverse map. Layer and cell boundary choices are harmless.

## Chord, rounding, and band signs

Each monomial's normalized layer curvature is between zero and two.
On a local cell of normalized width `h_i`, its true chord therefore has
nonnegative error at most `2h_i^2/8=h_i^2/4`. Downward endpoint rounding
subtracts from that chord a convex combination of two errors in
`[0,eta_i]`. Hence the interpolated value satisfies precisely

```
-eta_i<=z_ik-x_i^k<=h_i^2/4.
```

The coefficients are nonnegative, so the approximate output has error
between `-L_j` and `U_j`, where

```
L_j=sum_i C_ji eta_i,
U_j=sum_i C_ji h_i^2/4.
```

The band `T_j-U_j<=w_j<=T_j+L_j` has the correct signs: it contains
the exact output for every chosen input cell, and every admitted output
has error in `[-(L_j+U_j),L_j+U_j]`. Since `h_i^2<=p_i` and
`eta_i=p_i/4`, its absolute error is at most `(Cp)_j/2`.

Exact graph containment does not require the internal `z_ik` variables
to equal the powers. Their certified errors and the final band suffice
to admit `w=f(x)` simultaneously for all outputs. The exact affine terms
cause no additional error. Because `Cp in K`, unconditional convexity
puts the admitted vector error in `K`. No finite exact linear description
of the curved body is assumed.

## Total count, runtime, and verification

The only declared integers are the `sum_i(L_i+S_i)` index bits.
The reviewed rational allocation oracle gives a positive feasible rational
allocation with product at least `exp(-1)D_alloc`. Therefore

```
p_out<=Phi+r+sum_i S_i+1/(2 ln 2)
     <=p_conv+(9r/2)+sum_i S_i+1.
```

The precision parameters have polynomial magnitude in the sparse input
and allocation encoding. The endpoint evaluator visits only listed
exponents, and every exponentiation uses their bit lengths. Unrolling
its known polynomial time bound produces polynomially many gates; adding
their constant-size linear constraints and output-bit products preserves
polynomial total size. Dyadic coefficients have polynomial encoding, and
the rational polynomial coefficients and band sums retain polynomial
length. There is no hidden dependence on the numerical degree in this
complexity argument. It is a formulation construction theorem, not a
polynomial-time algorithm for solving the resulting MILP.

I inspected and reran
`code/quadratic_rank/check_sparse_positive_polynomial_circuits.py`.
All 56 exact rounded-power enclosures and 12 endpoint/band cases through
exponent `2^120+11` passed. The large-exponent checks use 120-digit
references and are explicitly numerical evidence; the uniform proofs
above supply their certificates. The checker does not generate the
entire compiled MILP. No unresolved mathematical or encoding defect
was found.
