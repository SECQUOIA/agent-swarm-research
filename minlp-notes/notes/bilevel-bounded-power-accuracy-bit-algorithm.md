# Additive optimization in accuracy bits for bounded-power box followers

Date: 2026-09-05. Status: reviewed predecessor of the
[promoted theorem](../results/bilevel-bounded-power-accuracy-bit-algorithm.md). The construction uses classical
polynomial approximation and fixed-dimensional real-algebraic optimization.
Its proposed contribution is their explicit combination for many algebraic
follower responses, including feasible rational leader recovery.

## 1. Model and candidate theorem

Fix leader dimension `r`. Let the positive integer local powers be input
data and put `P=max_i p_i`. The leader belongs to
a nonempty rational polytope `X subset [0,1]^r`, given explicitly. For each
follower coordinate choose an integer `1<=p_i<=P` and a rational affine
function `ell_i(x)`. The follower minimizes

```
sum_i [z_i^(p_i+1)/(p_i+1)-ell_i(x)z_i],
z in [0,1]^N.
```

It is strictly convex and has the unique response

```
z_i(x)=g_(p_i)(ell_i(x)),
g_p(t)=0 if t<=0; t^(1/p) if 0<=t<=1; 1 if t>=1.
```

The leader minimizes

```
H(x)=d_0+d^T x+sum_i c_i z_i(x),
```

with arbitrary signed rational `c_i` and rational `d_0,d`. No additional
upper constraints involve the response. All numerical magnitudes are
unrestricted; their rational encoding lengths count toward the input.

**Candidate theorem.** Given an integer accuracy count `B>=1`, one can
return a rational `xhat in X` satisfying

```
H(xhat)<=min_(x in X)H(x)+2^(-B)
```

in time polynomial in the original input bit length, `B`, and the
numerical maximum power `P`, for fixed `r`. A rational approximation to the optimal value with absolute error
at most `2^(-B)` can also be returned. The rational leader has polynomial
bit length. Exact representation of the optimum or all follower coordinates
in a common algebraic field is not asserted.

The usual same-power case is obtained by taking every `p_i=p`. For fixed
`P`, or unary/dense power encodings with `P` bounded polynomially by the
input length, the running time is polynomial in input length and accuracy
bits alone. Polynomial dependence on numerical `P` is distinct from
polynomial dependence on its sparse binary encoding.
The theorem counts the number of requested accuracy bits, not merely the
binary encoding length of the integer `B`.

## 2. Rational polynomials on dyadic root intervals

Write `epsilon=2^(-B)` and `A=sum_i |c_i|`. If `A=0`, solve the rational
leader LP exactly. Otherwise put

```
eta=epsilon/[16 max{1,A}],
m=ceil(log2(1/eta)),   K=P*m.
```

These integers can be computed by rational comparisons. For every
`p<=P`, setting the response approximation to zero whenever `t<=2^(-K)`
has error at most `eta`, because
`(2^(-K))^(1/p)<=2^(-m)<=eta`. The exact response is one for `t>=1`.

For `k=0,...,K-1`, consider

```
2^(-(k+1))<=t<=2^(-k),
b_k=3*2^(-(k+2)),   u=t/b_k-1 in [-1/3,1/3].
```

Set `alpha=1/p` and `q=m+1`. The binomial coefficients are rational and
satisfy `|binom(alpha,j)|<=1` for every `j>=0`: after the first coefficient,
the absolute recurrence ratio is at most one for `0<alpha<=1`. Therefore

```
T_q(u)=sum_(j=0)^q binom(alpha,j)u^j,
|T_q(u)|<=3/2,
|(1+u)^alpha-T_q(u)|<=3^(-q)/2<=eta/4.             (1)
```

Compute a rational `sigma_(k,p)` within `eta/4` of `b_k^(1/p)` by ordinary
bisection on `[0,1]`, comparing rational `p`th powers to `b_k`. Define

```
P_(k,p)(t)=sigma_(k,p) T_q(t/b_k-1).
```

Since `b_k^(1/p)<=1`, (1) proves

```
|P_(k,p)(t)-t^(1/p)|<=3eta/8+eta/4<eta.             (2)
```

The degree is `q=O(m)`. The construction uses `O(m)` bisections per root,
with rational comparisons of bit length polynomial in numerical `P`
and `m,K`. Raising an `O(m)`-bit rational to power `p` uses numbers of
`O(Pm)` bits; dyadic targets add `O(K)` bits. Binomial coefficient lengths
are `O(q(log P+log q))`, while normalization contributes `O(qK)` bits. All binomial coefficients, dyadic scalings, and expanded polynomial
coefficients have bit lengths polynomial in `m,K` and the original input.

## 3. A polynomial number of rational leader cells

Arrange the affine hyperplanes

```
ell_i(x)=2^(-k),   i=1,...,N,   k=0,...,K,
```

inside `X`. There are `N(K+1)` hyperplanes in a fixed-dimensional space,
so their realizable sign cells can be enumerated in polynomial time.
Include zero signs, constant tests, and lower-dimensional cells. Replace
each relative cell by its closure inside `X`; these rational compact
polytopes cover `X`. Weakening its strict affine tests gives that closure,
as follows by mixing any boundary point with a point of the relative cell.

On a cell choose, for each response, either zero below the truncation
threshold, one above the upper threshold, or the dyadic polynomial from
(2). At a cell contained in a threshold hyperplane choose any adjacent
valid branch. Each selected branch remains valid on the cell closure,
including its boundary. Thus the rational polynomial

```
H_C(x)=d_0+d^T x+sum_i c_i P_(i,C)(ell_i(x))
```

has degree at most `q` and satisfies throughout that closed cell

```
|H_C(x)-H(x)|<=A*eta<=epsilon/16.                  (3)
```

The notation `P_(i,C)` includes the constant branches zero and one.
Because `r` is fixed, expanding these substituted polynomials produces
only `binom(r+q,q)` monomials per polynomial. Their coefficient bit lengths
are polynomial in the input length and `B`. There is no expansion in the
unbounded number of follower variables.

Neighboring polynomials need not agree exactly at their common boundary.
This causes no problem: each one has the uniform guarantee (3) on its own
closed cell, and the finite family of closed cells covers the true domain.

## 4. Polynomial optimization and rational leader recovery

Minimize every `H_C` over its rational compact cell using a fixed-dimensional
real-algebraic algorithm. Fixed-variable quantifier elimination and algebraic
sampling have polynomial bit complexity when polynomial degrees and the
number of constraints grow explicitly. They return an exact algebraic
minimizer and value of polynomial encoding length. One explicit interface
eliminates `u` from `x in C` and `not exists u in C: H_C(u)<H_C(x)`, then
samples the resulting minimizer set. The number of variables remains fixed,
and the sampled coordinates share one polynomial-degree algebraic field.
Exact comparison selects
a cell with the least polynomial optimum. Denote its minimizer by `xstar`
and its polynomial by `Q`.

If `xopt` is a true global minimizer, applying (3) in a cell containing it
gives

```
Q(xstar)<=H(xopt)+epsilon/16.                      (4)
```

We now produce a nearby *rational* feasible leader without assuming that
algebraic outputs can simply be rounded coordinatewise.

Enumerate the rational vertices of the selected cell by its independent
active-row systems. Since `r` is fixed, there are polynomially many.
Every vertex has polynomial rational bit length. Caratheodory's theorem
places `xstar` in a simplex of at most `r+1` of these vertices. Enumerating
these small subsets and solving their affine systems finds a representation

```
xstar=sum_(j=1)^s lambda_j v_j,
lambda_j>=0,  sum_j lambda_j=1,  s<=r+1.
```

All tests and coefficients can be handled in the same polynomial-degree
algebraic field as `xstar`. Lower-dimensional cells and singleton cells
are included. For a singleton the exact leader is already rational.

Write `Q(x)=sum_nu a_nu x^nu` and compute the positive rational bound

```
L=max{1, sum_nu |a_nu|*|nu|}.
```

On the unit cube, the sum of the absolute partial derivatives of `Q` is
at most `L`. Its binary logarithm is polynomial in the constructed input
length. Choose an integer

```
R>=8 max{1,r} L/epsilon.
```

For `j<s`, replace `lambda_j` by `floor(R lambda_j)/R`; define the last
weight to make their sum one. Every new weight is nonnegative. Exact
algebraic comparisons compute the floors in polynomial time using
`O(log R)` comparisons per weight. The rational convex combination `xhat`
remains inside the selected cell and satisfies

```
||xhat-xstar||_infinity<=2r/R,
Q(xhat)<=Q(xstar)+epsilon/4.                       (5)
```

The second inequality follows from the derivative bound along the segment
inside the unit cube. All rational output bit lengths are polynomial.
Combining (3)--(5) yields

```
H(xhat)<=H(xopt)+epsilon/8+epsilon/4< H(xopt)+epsilon.
```

In fact the displayed budget gives suboptimality at most `3epsilon/8`.
Evaluate the finitely many roots at this rational leader by bisection to
make the final upper-value error at most `epsilon/4`. The resulting
rational value estimate differs from the true optimum by less than
`epsilon`. If desired, each follower coordinate can also be returned as
an individual root expression or isolating interval; no common-field
exact representation for their sum is required.

## 5. Why this does not solve exact root-sum arithmetic

Even with no effective leader choice, square-root followers can encode
an arbitrary sum of square roots. Given positive integers `a_i`, choose
an integer `M>=max_i a_i`, use constant affine arguments `a_i/M^2`, and
set the upper coefficients to `M`. The fixed follower output value is
`sum_i sqrt(a_i)`. Exact threshold comparison therefore includes the
sum-of-square-roots decision problem. The algorithm above approximates
values; it does not import an unproved polynomial exact arithmetic oracle.

The candidate also does not preserve additional response-dependent upper
constraints exactly. Uniform objective approximation is sufficient for
its stated optimization task, but does not establish exact feasibility
for such extra constraints.

## 6. A separate obstruction when binary-encoded powers grow

The numerical dependence on local powers cannot simply be replaced by
dependence on their sparse binary lengths for this rational leader output
guarantee. Let `p>=2` be even and binary encoded. Use one
leader `x in [0,1]` and two unit-box followers with costs

```
z_1^(p+1)/(p+1)-x z_1,
z_2^(p/2+1)/(p/2+1)-x z_2.
```

Their responses are `z_1=x^(1/p)` and `z_2=x^(2/p)`. The affine upper
objective is `z_2-z_1`. Writing `s=x^(1/p)`, it equals
`(s-1/2)^2-1/4` and has minimum `-1/4` at `x=2^(-p)`.
Any leader with suboptimality at most `1/64` must satisfy

```
3/8<=s<=5/8,
0<x<= (5/8)^p.
```

A positive rational such `x=a/b` in reduced form requires
`b>=(8/5)^p`, so its explicit binary encoding needs `Omega(p)` bits.
The original sparse power encoding has only `O(log p)` bits, while the
requested accuracy is constant. Thus polynomial rational output length
is impossible for this extension. The example uses *two distinct* growing
local powers; it does not establish the same barrier when every local
power must be identical. This is a supporting output-encoding obstruction,
not a new hardness assumption or a strong-convexity statement.

## 7. Scope and source status

The proof uses dyadic truncation, binomial polynomial approximation,
fixed-dimensional hyperplane arrangements and polynomial optimization,
and rational convex combinations. These are established ingredients. The
real-algebraic imports are described in
[Basu's primary-author survey, Theorems 2.15 and 2.18](https://www.math.purdue.edu/~sbasu/raag_survey2011_final.pdf);
the independent audits check the degree, coefficient-bit, and common-field
sampling requirements.
The [bounded source comparison](bilevel-bounded-power-accuracy-bit-novelty.md)
found no exact matching theorem, without claiming exhaustive priority.
The closest general predecessor is
[Vigneron, *Geometric Optimization and Sums of Algebraic Functions*, Theorems 6 and 9](https://antoinevigneron.github.io/manuscripts/rational.pdf).
It treats more general nonnegative algebraic sums in fixed dimension, with
polynomial dependence on inverse relative error. Section 2.3 explicitly
also discusses bit complexity. Thus neither algebraic-sum approximation
nor its bit-model implementation is new. The distinction investigated
here is polynomial dependence on accuracy bits for the specific clipped-
root family, with signed objectives and rational feasible leader recovery.
The full primary manuscript was retrieved and its relevant statements
checked; shifting signed terms to be nonnegative would not change an
inverse-error runtime into an accuracy-bit runtime.
The main algorithm avoids stationarity root isolation, exact signs of sums
of radicals, and derivative conditioning near the clipping threshold.
The growing-power obstruction and exact arithmetic limitation are retained
separately from the positive fixed-power theorem.

## 8. Exact approximation diagnostics

[The exact checker](../code/bilevel_bounded_power/check_dyadic_approximation.py)
passed 900 certified rational evaluations of the dyadic approximants for
powers one through five, several accuracy levels, and coefficient weights
from `2^(-10)` to `2^20`. Reference roots are enclosed by exact rational
bisection, so these are interval certificates rather than floating-point
comparisons. The checks also verify the truncation, tail, and growing-power
output-obstruction constants. They supplement the general proof and do
not implement the fixed-dimensional real-algebraic optimizer.
