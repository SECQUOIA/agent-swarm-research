# Finite integer precision for positive separable polynomials

Date: 2026-09-05. Status: independently reviewed theorem.

Positive separable polynomials admit a finite allocation law with an
additive error controlled by their active dimension and degrees. For
fixed degree this is `O(r)`, uniformly in all coefficients, tolerances,
and output counts. The formulation is rational and has polynomial size
for dense polynomial input, even when the degrees grow.

## Statement

On `[0,1]^n`, let

```
f_j(x)=a_j^T x+b_j+sum_i sum_(k=2)^(D_i) c_jik x_i^k,
c_jik>=0,       j=1,...,m,
```

and require separate errors `|w_j-f_j(x)|<=epsilon_j`, with
`epsilon_j>0`. Affine coefficients may have either sign. Retain only
coordinates with some positive nonlinear coefficient, and let their
number be `r`. For each retained coordinate choose `D_i>=2` at least
its largest nonzero exponent. Set

```
C_ji=sum_(k=2)^(D_i) c_jik,
D_alloc=max{product_i p_i:
              0<=p_i<=1, sum_i C_ji p_i<=epsilon_j for every j},
Phi=-(1/2)log2 D_alloc,
A=log2[omega_r(r+2)^(r/2)]+sum_i log2 D_i-r/2,
B=sum_i log2 D_i+r.
```

If `r=0`, the exact graph is a linear formulation. Otherwise the
arbitrary-convex-lift and binary-LP minima satisfy

```
max(0,Phi-A)<=p_conv<=p_bin<=Phi+B.                      (1)
```

For rational coefficients and positive rational tolerances, a
deterministic polynomial-time algorithm constructs a rational MILP with

```
p_out<=p_conv+2sum_i log2 D_i+4r+1.                     (2)
```

The input is a dense coefficient representation: computation and model
size are polynomial in the full coefficient list, including its degrees
and bit lengths. The bound does not claim polynomial complexity for
binary-encoded enormous exponents given sparsely or through a circuit.
For a fixed maximum degree, (2) is an additive `O(r)` guarantee. With
growing degree `D=max_i D_i`, it is `O(r log(D+1))`.

## A scalar Jensen inequality supplies the lower bound

For `a,b in [0,1]` and integers `2<=k<=D`, define

```
J_k(a,b)=(a^k+b^k)/2-((a+b)/2)^k.
```

Convexity of `u^(k/2)` gives

```
((a+b)/2)^k <=[(a^(k/2)+b^(k/2))/2]^2,
J_k(a,b)>=(1/4)(a^(k/2)-b^(k/2))^2.
```

The function `u^(D/k)` is `D/k`-Lipschitz on `[0,1]`. Consequently

```
|a^(k/2)-b^(k/2)| >=(k/D)|a^(D/2)-b^(D/2)|,
J_k(a,b)>=(1/D^2)|a^(D/2)-b^(D/2)|^2.                  (3)
```

Now take any exact-graph parity support of a valid convex lift. Its
original graph midpoint is admitted, so positivity of the coefficients
and (3) imply, for every pair `x,y` in that support,

```
sum_i (C_ji/D_i^2)
       (x_i^(D_i/2)-y_i^(D_i/2))^2 <=epsilon_j.         (4)
```

Affine terms cancel. Continuity preserves this inequality on compact
closures, exactly as in the reviewed quadratic lower bound.

Map each support coordinatewise by

```
t_i=x_i^(D_i/2).
```

This is a homeomorphism of the active cube onto itself. The transformed
compact supports still cover a unit-volume cube, and (4) is now a
quadratic pairwise bound in `t`. No transformed support needs to be
convex, and no Jacobian or volume-preservation assertion is used: all
following volumes and covariances are taken directly in the `t` cube.

For a positive-volume transformed support with uniform covariance
`Sigma`, averaging (4) over two independent points gives

```
sum_i (C_ji/D_i^2) Sigma_ii<=epsilon_j/2.
```

Thus `p_i=2Sigma_ii/D_i^2` is feasible for `D_alloc`; the bound
`Sigma_ii<=1/4` ensures `p_i<=1`. Hadamard's determinant inequality and
the reviewed volume-covariance inequality imply

```
vol(support)
 <=omega_r(r+2)^(r/2) sqrt(det Sigma)
 <=omega_r(r+2)^(r/2) [product_i (D_i/sqrt(2))]
      sqrt(D_alloc).
```

The at-most-`2^p` parity cover of the transformed cube proves the lower
bound in (1). Inactive affine coordinates are removed exactly by affine
output subtraction and projection onto the active cube, without adding
integers, as in the diagonal quadratic theorem.

## Original-coordinate grids need only a Taylor band

For any feasible positive allocation `p`, choose dyadic widths

```
L_i=ceil[log2(D_i/sqrt(p_i))],
h_i=2^(-L_i)<=sqrt(p_i)/D_i.
```

Write each active coordinate as `x_i=a_i+r_i`, where `a_i` has `L_i`
binary prefix digits and `0<=r_i<=h_i`. In particular, `0<=a_i<=1-h_i`.
For output `j`, define its affine Taylor expression on the selected box

```
T_j=a_j^T x+b_j+
       sum_i sum_(k=2)^(D_i) c_jik
                [a_i^k+k a_i^(k-1)r_i].
```

Every univariate nonlinear part has second derivative between zero and
`D_i^2 C_ji` on `[0,1]`. Taylor's integral remainder therefore gives

```
0<=f_j(x)-T_j<=(1/2)sum_i D_i^2 C_ji h_i^2
                    <=epsilon_j/2.
```

The two linear inequalities

```
T_j<=w_j<=T_j+epsilon_j/2                               (5)
```

contain every exact graph point. Every admitted `w_j` and the true
`f_j(x)` lie in the same interval of length `epsilon_j/2`, so (5) has
absolute error at most `epsilon_j/2`. The remaining task is to express
all powers in `T_j` with linear constraints and the existing prefix bits.

## Exact shared prefix powers require no additional integers

Suppress the coordinate index. If

```
a=sum_(l=1)^L 2^(-l) z_l,       z_l binary,
```

introduce `v_k=a^k` and `t_k=a^k r`, starting with `v_0=1`, `t_0=r`.
Generate them recursively by

```
v_k=sum_l 2^(-l) (z_l v_(k-1)),
t_k=sum_l 2^(-l) (z_l t_(k-1)).                          (6)
```

Each parenthesized product is represented exactly by the four usual
linear inequalities for a binary times bounded continuous variable.
Valid bounds are `0<=v_k<=1` and `0<=t_k<=h`. For example, for
`b in {0,1}` and `0<=u<=M`, the product variable `s=bu` is enforced by

```
0<=s<=M b,       s<=u,       s>=u-M(1-b).
```

Induction proves that (6) gives exactly the claimed powers on every
integer-feasible solution. They are shared across all outputs. It
suffices to generate `v_k` through degree `D_i` and `t_k` through
`D_i-1`, requiring `O(D_i L_i)` rows and continuous variables for
coordinate `i`. There are no new binaries. Substituting these variables
into `T_j` makes (5) linear with rational coefficients whenever the
original data are rational.

The total binary count is

```
sum_i L_i<=Phi(p)+sum_i log2 D_i+r,
Phi(p)=-(1/2)log2 product_i p_i.
```

An exact optimal allocation proves the upper bound in (1). The model
size is polynomial in the dense degree representation, the full input
bit length, and the constructed binary count. This construction does
not need an inverse power grid or any irrational breakpoints.

## Rational polynomial construction

Apply the reviewed scalar allocation algorithm from the
[diagonal PSD theorem](../results/diagonal-psd-quadratic-linear-dimension-precision.md)
with row coefficients `C_ji` and tolerances `epsilon_j`. Its dyadic
initial point, Euclidean log-coordinate iterations, and exact rational
scaling repair give a feasible positive rational allocation satisfying

```
product_i p_i>=exp(-1)D_alloc.
```

Only nonnegativity of the row coefficients is used by that algorithm;
it is independent of the polynomial degrees. Therefore the grid count
is at most `Phi+B+1/(2ln2)`. All depth choices use exact rational
comparisons of `2^(2L_i)` with `D_i^2/p_i`.

The Gaussian volume bound yields

```
A<sum_i log2 D_i+3r.
```

Combining this with (1) and the rational count bound proves (2).
The prefix-power equations use only rational coefficients `2^(-l)`
and the supplied polynomial coefficients and integer exponents.
Even with growing dense degrees, the number of generated recurrences
and every coefficient encoding length remain polynomial in the input.

## Scope and novelty boundary

Nonnegative nonlinear coefficients and the nonnegative box are explicit
assumptions. The theorem does not cover cancellation between signed
monomials or arbitrary nonseparable polynomials. Its lower bound uses a
power transformation only as a proof device; the actual MILP remains
in the original rational coordinates.

Shared interpolation encodings, Taylor estimates, binary-continuous
product linearization, and convex scalar allocation are established
methods. The proposed conclusion is the finite, coefficient- and
accuracy-uniform integer-count law against arbitrary convex lifts,
with a compact rational construction for growing dense degrees.
In particular, the 2013 work of Teles, Castro and Matos already develops
radix-plus-residual MILP approximations for polynomial powers; no separate
priority claim is made for the prefix recurrence here. The proposed new
bridge is the power-transformed parity-support lower bound and its finite
comparison with the construction. The [source and novelty assessment](../notes/positive-separable-polynomial-precision-novelty.md)
records this prior work and found no matching whole-formulation theorem
in its bounded search. Publication priority remains unestablished.

The [first proof audit](../notes/review-positive-separable-polynomial-precision.md)
and [second proof audit](../notes/review-positive-separable-polynomial-precision-second.md)
both passed. The reproducible checker
`code/quadratic_rank/check_positive_separable_polynomials.py` passed 792
exact scalar Jensen bounds, 192 recursive-prefix Taylor bands, and 12
transformed-covariance allocation checks. The first independent reviewer
also checked 4,750 exact scalar inequalities through degree 20.

The [unconditional-error-body extension](positive-separable-unconditional-error-precision.md)
retains these dimension bounds for whole monotone norm budgets, using
`Cp in K` directly in the allocation and rational output rectangles.

For the subclass with one power per coordinate shared by every output,
the [compact inverse-power construction](positive-pure-power-linear-dimension-precision.md)
removes degree dependence from the additive integer count: it gives
`p_out<=p_conv+6.5r+1` with polynomial rational size for dense degree input.

The [supporting-scalarization and dyadic-layer refinement](positive-polynomial-loglog-degree-precision.md)
strengthens the degree dependence for this entire positive-polynomial
family. It gives a degree-independent lower allocation bound and a compact
rational construction with overhead `O(r+sum_i log log(D_i+2))`.
