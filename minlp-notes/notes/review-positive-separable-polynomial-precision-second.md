# Second audit: positive separable polynomial precision

Date: 2026-09-05. Reviewer: `constant_rank_review`.
Reviewed candidate:
`notes/positive-separable-polynomial-integer-precision.md`.

## Verdict

**PASS.** The finite allocation law, its lower-bound constants, the
rational Taylor-band formulation, and the polynomial-time guarantee
`p_out<=p_conv+2sum_i log2 D_i+4r+1` are correct.

The nonlinear power map is used only on proof support sets. It is
neither imposed in the MILP nor assumed to preserve volume or convexity.
The exact power recurrence needs no added integers and has polynomial
size for dense polynomial input, including growing degrees. No substantive
correction was needed.

This audit does not establish novelty. Positivity of all nonlinear
coefficients, separability, the nonnegative cube, and the dense degree
encoding are material hypotheses.

## Active coordinates and the allocation

Subtracting the affine output map and projecting to the active coordinates
preserves both integer minima. As usual, the original cube can first be
imposed explicitly without integer overhead. Conversely, the inactive
coordinates remain continuous and their affine contributions are restored
by linear equations. The active domain is exactly a unit cube.

Every row coefficient `C_ji` is nonnegative. A sufficiently small common
positive allocation is feasible because all tolerances are positive.
The feasible allocation set is compact; its product maximum is positive
and hence attained with all coordinates positive. Thus the logarithmic
benchmark is finite. Zero rows impose no restriction, and the fully
affine case is handled separately by an exact LP.

## Scalar Jensen inequality

For `k>=2`, the function `u^(k/2)` is convex and nonnegative.
Applying Jensen and then squaring yields

```
((a+b)/2)^k <=((a^(k/2)+b^(k/2))/2)^2.
```

Subtracting from the endpoint average gives
`J_k(a,b)>=(a^(k/2)-b^(k/2))^2/4`. The function
`u^(D/k)` is Lipschitz with constant `D/k` on the unit interval,
because its exponent is at least one. Applying this to the two
half-powers gives

```
|a^(k/2)-b^(k/2)| >=(k/D)|a^(D/2)-b^(D/2)|.
```

Finally `k^2/4>=1`, proving the stated coefficient `1/D^2`.
This includes odd degrees and endpoint zero; no differentiability of
an inverse power at zero is required.

For exact graph lifts in one integer parity class, their midpoint is
admitted. The Jensen gaps of all nonnegative monomials sum to a
nonnegative vertical error at most the prescribed tolerance. Summing
the preceding scalar bound therefore gives the candidate's inequality
with coefficient `C_ji/D_i^2`. Affine terms cancel exactly.

## Transformed supports and covariance constants

Take compact closures of the original parity supports inside the active
cube. Continuity preserves every pairwise Jensen bound. The coordinate
map `t_i=x_i^(D_i/2)` is a continuous bijection with continuous inverse
on the unit cube. It sends these supports to compact sets still covering
the entire unit cube.

The proof subsequently places uniform probability measures directly on
the transformed supports. It does not transport a uniform measure from
the original support, apply a Jacobian formula, or treat transformed
midpoints as midpoints of original graph lifts. All required pairwise
inequalities have already been established before introducing these
new probability measures. Convexity of transformed supports is unnecessary.

For independent uniform transformed points, averaging squared coordinate
differences gives twice the corresponding variance. Thus

```
sum_i (C_ji/D_i^2) Sigma_ii <=epsilon_j/2.
```

The allocation `p_i=2Sigma_ii/D_i^2` satisfies every row budget.
Its cap follows from `Sigma_ii<=1/4` and `D_i>=2`; in fact,
`p_i<=1/8`. Positive-volume support ensures positive variances.
Zero-volume supports contribute nothing to the covering argument.

Hadamard's determinant inequality and the volume-covariance bound yield

```
vol(S)<=omega_r(r+2)^(r/2)
        product_i(D_i/sqrt(2)) sqrt(D_alloc).
```

The factor for coordinate `i` is exactly `D_i/sqrt(2)` because
`Sigma_ii=(D_i^2/2)p_i`. Summing over at most `2^p` transformed
supports covering unit volume gives precisely
`p_conv>=Phi-A`, with the displayed definition of `A`.
Arbitrary continuous lift dimensions and unbounded general integer
coordinates are covered by the parity argument.

## Original-coordinate Taylor bands

The depth choice makes `h_i<=sqrt(p_i)/D_i`. Binary prefixes have
`0<=a_i<=1-h_i`, so the full Taylor segment from `a_i` to
`a_i+r_i=x_i` lies inside the unit interval for every admitted
residual `0<=r_i<=h_i`. Every original input coordinate, including
its upper endpoint, has such a representation.

The second derivative of an output's univariate nonlinear part is
nonnegative and bounded by `D_i^2 C_ji` on this interval. The
integral Taylor remainder is therefore between zero and
`(1/2)D_i^2 C_ji r_i^2`. Summing and using the allocation gives

```
0<=f_j(x)-T_j<=epsilon_j/2.
```

Both the true output and every admitted output from the band lie in
the same interval `[T_j,T_j+epsilon_j/2]`. Consequently graph
containment holds and the absolute error is at most `epsilon_j/2`,
safely within the requested tolerance. Arbitrary signs of the original
affine coefficients do not change the remainder.

## Exact reused-bit powers

For each fixed integer assignment of prefix bits, the bounded binary
product inequalities force every product variable to its exact value.
Starting from `v_0=1` and `t_0=r`, the recursive equations therefore
give inductively

```
v_k=a v_(k-1)=a^k,
t_k=a t_(k-1)=a^k r.
```

The bounds `0<=v_k<=1` and `0<=t_k<=h` hold because
`0<=a<=1` and `0<=r<=h`. These are valid bounds for each use
of the four-row binary product formulation. The recursion is ordered
by degree and introduces no circular dependence.

All levels reuse the original prefix bits. The other variables are
continuous and become exact through the product constraints; they
need not be declared binary. Generating powers through `D_i` and
residual powers through `D_i-1` requires only `O(D_i L_i)`
rows and continuous variables. Sharing them across outputs leaves
only the supplied coefficient-weighted output expressions to assemble.

This construction is materially different from expanding all products
of prefix bits into distinct monomials, which would produce an
unnecessary combinatorial increase with degree. The written recurrence
has the stated polynomial size.

## Rational construction, degree encoding, and final constant

The scalar allocation algorithm applies with row coefficients `C_ji`:
its proof needs only their nonnegativity and positive rational budgets,
not a quadratic interpretation. Its already reviewed guarantee gives
a rational feasible allocation with product at least
`exp(-1)D_alloc`.

Thus the grid count is at most
`Phi+sum_i log2 D_i+r+1/(2ln2)`. The Gaussian bound gives

```
A <=sum_i log2 D_i
    +(r/2)log2[2pi e(1+2/r)]-r/2
  <sum_i log2 D_i+3r.
```

Combining this with `Phi<=p_conv+A` and
`1/(2ln2)<1` proves the claimed
`p_conv+2sum_i log2 D_i+4r+1` bound. It is uniform in coefficient
magnitudes, tolerances, and number of outputs.

Rational row sums have polynomial encoding length. The allocation
algorithm's common feasible dyadic point and final repair bound its
negative log product by a polynomial in the original input length.
Consequently all individual positive-allocation logarithms, binary
depths, and dyadic coefficient lengths are polynomially bounded.
Depth selection compares the rational quantities
`2^(2L_i)` and `D_i^2/p_i` exactly.

Under dense input encoding, every `D_i` is bounded by the length
of its coefficient list, and the number of recurrences
`sum_i O(D_i L_i)` is polynomial in the total input size.
Integer factors `k` in the Taylor expressions add only
`O(log D_i)` coefficient bits. No irrational breakpoints, inverse
power maps, or algebraic coefficients appear in the produced MILP.

A polynomial-size claim for sparsely encoded enormous exponents would
not follow from this construction. The note explicitly excludes it,
while correctly retaining the finite mathematical bounds for arbitrary
integer degrees.
