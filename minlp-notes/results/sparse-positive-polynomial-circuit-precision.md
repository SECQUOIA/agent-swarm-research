# Sparse positive-polynomial precision by compiled endpoint interpolation

Date: 2026-09-05. Status: independently reviewed theorem and construction.

The double-logarithmic degree precision theorem extends to sparse polynomials
whose exponents are supplied in binary. Compiling rounded endpoint evaluation
replaces the exact degree-by-degree power recurrences. The geometric lower
bound, dyadic layers, and integer count remain unchanged.

## Statement

Let

```
f_j(x)=l_j^T x+b_j+sum_i sum_(k in E_i) c_jik x_i^k,
x in [0,1]^r,       c_jik>=0,
```

where each finite exponent list `E_i` contains integers at least two, encoded
in binary. Zero coefficients may be omitted, and every coordinate is active.
Put `D_i=max E_i`, `C_ji=sum_(k in E_i)c_jik`, and let `K` be an unconditional
compact convex error body with the rational strong-oracle and radius assumptions
of the reviewed allocation theorem. Define

```
D_alloc=max{product_i p_i: 0<=p_i<=1, Cp in K},
Phi=-(1/2)log2 D_alloc,
J_i=ceil(log2 D_i),
S_i=ceil(log2(J_i+1)).
```

There is a deterministic polynomial-time construction of a rational MILP,
with polynomial size in the full sparse input and oracle encoding, whose
binary count satisfies

```
p_out<=Phi+r+sum_i S_i+1/(2ln2)
     <=p_conv+(9r/2)+sum_i S_i+1.                      (1)
```

In particular, running time and size are polynomial in the exponent bit lengths,
not in their numerical values. The arbitrary-convex-lift lower bound
`p_conv>=Phi-A_r`, `A_r<7r/2`, is exactly the reviewed
[supporting-scalarization lower bound](../results/positive-polynomial-loglog-degree-precision.md),
which is a mathematical finite-polynomial statement independent of encoding.

## Two previously audited ingredients

The [compiled rational knot lemma](../notes/compiled-rational-knot-formulations.md)
turns any deterministic polynomial-time indexed endpoint computation into a
rational MILP with only its input index bits declared integer. Every internal
Boolean gate is continuous but is forced to zero or one when its inputs are
Boolean. Its endpoint output bits can be multiplied exactly by a continuous
interpolation weight without declaring new integers. A polynomial-time
computation is compiled at its worst-case time bound, with flags or padding
for early termination.

That note also proves that a dyadic `x in [0,1]` can have its integer power
`x^k` evaluated downward to absolute error at most `eta` using
`O(log k)` fixed-precision multiplications. With `P` fractional bits,

```
0<=x^k-A<=k 2^(-P),
```

provided the original dyadic input is represented exactly. Taking
`P>=ceil(log2(k/eta))` and at least the input precision therefore suffices.
The number of bits is polynomial in `log k`, the input dyadic precision,
and `log(1/eta)`.

The reviewed dyadic-layer curvature estimate says that on each interval

```
[1-2^(-j),1-2^(-j-1)],          j=0,...,J_i-1,
[1-2^(-J_i),1],
```

every monomial `x^k`, `2<=k<=D_i`, has second derivative at most two in
the normalized local coordinate. It holds for each listed sparse exponent
without enumerating any unlisted powers.

## Exact dyadic input endpoints and computed monomial values

Use the rational allocation oracle to obtain a positive feasible `p` with
product at least `exp(-1)D_alloc`. For coordinate `i`, let

```
L_i=ceil[(1/2)log2(1/p_i)],
h_i=2^(-L_i),
eta_i=p_i/4.
```

The only integer inputs for this coordinate are an `S_i`-bit layer number
`j` and an `L_i`-bit local cell number `q`. Impose the single linear inequality
`j<=J_i` to exclude unused layer codes. If `L_i=0`, the sole cell number is
zero and requires no bit variables.

For the selected layer `[ell_j,ell_j+s_j]`, compute exactly the dyadic endpoints

```
a=ell_j+s_j q h_i,
b=ell_j+s_j(q+1)h_i.
```

A common output precision `B_i=J_i+L_i+1` represents both endpoints exactly.
The layer selection, dyadic shifts, and integer arithmetic have polynomial
cost in `J_i+L_i`, hence in the sparse exponent encoding and allocation encoding.
The algorithm may assign arbitrary outputs on the excluded unused layer codes.

For each distinct listed exponent `k in E_i`, compute downward approximations
`A_ik,B_ik` satisfying

```
0<=a^k-A_ik<=eta_i,
0<=b^k-B_ik<=eta_i,
0<=A_ik,B_ik<=1.
```

One common precision for the coordinate is

```
P_i>=max(B_i,ceil(log2(D_i/eta_i))).
```

This uses `O(J_i+L_i+log(1/p_i))` bits and `O(log k)` rounded multiplications
per listed monomial. Crucially, exact rational numerators of numerical-degree
powers are never formed. The output bit lengths and runtime are polynomial
in the sparse input. Endpoint zero and one cause no problem for downward
power evaluation; unlike inverse-root computation, no conditioning at zero
is needed here.

Compile all these endpoint computations jointly and introduce one continuous
interpolation weight `theta_i in [0,1]`. The output-bit product construction
imposes exactly

```
x_i=(1-theta_i)a+theta_i b,
z_ik=(1-theta_i)A_ik+theta_i B_ik.
```

The first equation uses exact input endpoints, so every original point is
covered by its layer and cell. All listed monomials use the same interpolation
weight and the same index bits. No independent integer variables are introduced
for internal gates or computed endpoint values.

## Error rectangle

Let `s_ik` be the true chord of `x^k` on `[a,b]`. The local cell width is `h_i`,
and its normalized second derivative is at most two. The elementary chord
bound therefore gives

```
0<=s_ik(x_i)-x_i^k<=h_i^2/4.
```

Downward endpoint rounding lowers that chord by a quantity in `[0,eta_i]`.
Hence every admitted interpolated monomial satisfies

```
-eta_i<=z_ik-x_i^k<=h_i^2/4.                           (2)
```

Define the linear approximate output

```
T_j=l_j^T x+b_j+sum_i sum_(k in E_i)c_jik z_ik.
```

Nonnegative coefficients and (2) imply

```
-sum_i C_ji eta_i<=T_j-f_j(x)<=sum_i C_ji h_i^2/4.
```

Impose the rational band

```
T_j-sum_i C_ji h_i^2/4 <=w_j<=T_j+sum_i C_ji eta_i.     (3)
```

It contains every exact graph point. Conversely, every admitted point obeys

```
|w_j-f_j(x)|<=sum_i C_ji(h_i^2/4+eta_i)<=(Cp)_j/2.
```

Since `Cp in K` and `K` is unconditional, this proves the full error-body
claim. The final MILP uses only the displayed rational bands; no exact linear
description of the body `K` is required.

The binary count is `sum_i(L_i+S_i)`, so the allocation product guarantee gives
the first inequality in (1). The degree-independent lower bound gives the
second. Rational coefficients, compilation, and oracle conditioning have all
been accounted for in the sparse encoding.

## Scope and attribution

The new scope relative to the dense theorem is sparse binary exponent input.
The geometric proof and integer-count constant do not change. The generic
computation compiler, exact interpolation of its Boolean outputs, and rounded
binary exponentiation are supporting tools credited in the compiled-knot note.
The [bounded source audit](../notes/sparse-positive-polynomial-circuit-precision-novelty.md)
records those predecessors and found no matching combined sparse-input
whole-formulation theorem. Publication priority remains unestablished.

The [first independent audit](../notes/review-sparse-positive-polynomial-circuit-precision.md)
and [second independent audit](../notes/review-sparse-positive-polynomial-circuit-precision-second.md)
both passed. The [checker](../code/quadratic_rank/check_sparse_positive_polynomial_circuits.py)
passed 56 exact rounded-power enclosures and 12 high-precision endpoint/band
cases through exponent `2^120+11`. The large-exponent cases are numerical
evidence; the proof supplies the uniform error certificate. The first
reviewer independently checked 3,720 exact monomial enclosures and 2,760
shared-output graph/band cases through degree 128.
