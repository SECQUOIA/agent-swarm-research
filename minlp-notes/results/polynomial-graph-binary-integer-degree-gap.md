# A logarithmic binary-versus-integer gap for univariate polynomial graphs

Date: 2026-09-05. Status: independently reviewed result; two full proof audits passed.

Convexity is essential to a dimension-only comparison between binary and general
integer graph formulations. Even for one densely encoded rational polynomial
and fixed absolute tolerance, two general integer variables can suffice while
the minimum number of binary variables grows without bound. A matching finite
upper bound is logarithmic in the number of convexity intervals, hence in degree.

Here `p_conv` permits arbitrary convex lifts with general integer variables;
`p_bin` permits binary variables only, with convex continuous lifts. The upper
bounds below can in fact use finite MILPs. Both models contain the entire exact
graph and permit only the stated absolute output error.

## 1. An explicit polynomial family with a growing gap

For an integer `M>=2`, let `T_M:[0,1]->[0,1]` be the continuous triangular wave
with `M` periods, defined on every period by

```
t=Mx-j in [0,1],
T_M(x)=2t       when 0<=t<=1/2,
T_M(x)=2-2t     when 1/2<=t<=1,
j=0,...,M-1.
```

This function is `2M`-Lipschitz. Set `N=(32M)^2` and take its Bernstein polynomial

```
q_M(x)=sum_(k=0)^N T_M(k/N) binom(N,k) x^k(1-x)^(N-k).
```

All coefficients are rational. Its degree is at most `N`; both the Bernstein
representation and its dense monomial expansion have bit length polynomial in
`N` and `log M`. Thus the construction is a family of rational dense inputs,
not an elementary-function oracle.

If `X` is binomial with parameters `N,x`, the Bernstein identity gives
`q_M(x)=E T_M(X/N)`. Cauchy--Schwarz and the Lipschitz bound yield, uniformly,

```
|q_M(x)-T_M(x)|
 <=2M E|X/N-x|
 <=2M sqrt(x(1-x)/N)
 <=M/sqrt(N)=1/32.                                                 (1)
```

Fix `epsilon=1/4` for every member of the family.

### Two general integer variables suffice

Introduce an integer period variable `z in {0,...,M-1}`, a binary orientation
variable `b`, and continuous `t,y`. Impose `x=(z+t)/M`, and choose one of the
following two linear branches using `b`:

```
b=0: 0<=t<=1/2,   y=2t,
b=1: 1/2<=t<=1,   y=2-2t.
```

This finite two-branch disjunction has a constant-size big-M formulation with
rational coefficients and global bounds `0<=t,y<=1`. Its projection is exactly
the graph of `T_M`, including period boundaries and `x=1`. Add

```
y-1/32<=w<=y+1/32.
```

By (1), every graph point `(x,q_M(x))` is admitted. Conversely every admitted
point satisfies `|w-q_M(x)|<=1/16<epsilon`. Therefore

```
p_conv(q_M,epsilon)<=2.                                            (2)
```

The binary variable counts as one of the two general integer variables.

### Binary formulations need at least log M integers

At the `M` peaks `a_j=(j+1/2)/M`, inequality (1) gives
`q_M(a_j)>=31/32`. Between any two different peaks is a trough `b=k/M`,
where `q_M(b)<=1/32`.

If two exact peak graph points had feasible lifts with the same full binary
assignment, convexity of the corresponding continuous slice would admit their
entire graph chord. At the intervening trough's input coordinate, its output
would be at least `31/32`, producing an error at least `30/32>epsilon`.
This is impossible. Hence the `M` peaks require distinct binary assignments,
regardless of continuous lift size, and

```
p_bin(q_M,epsilon)>=ceil(log2 M).                                  (3)
```

The argument uses convexity for a fixed binary assignment, not a parity claim
for general integers. Period indices in (2) can differ by arbitrary integers;
that distinction is exactly what permits the gap.

Conversely, replacing the period index `z` in the explicit formulation by
`ceil(log2 M)` binary digits, with invalid codes excluded, gives

```
ceil(log2 M)<=p_bin(q_M,epsilon)<=ceil(log2 M)+1.                   (3a)
```

Thus the family's binary count is determined within one integer.

Equations (2)--(3) rule out any universal dimension-only additive upper bound
on `p_bin-p_conv` for nonconvex univariate polynomial graphs. Since the degree
is at most `1024M^2`, they also give a logarithmic lower bound in degree along
this family, up to an additive constant. No assertion about the exact degree
of every monomial expansion is needed. The degrees do tend to infinity:
the alternating near-zero troughs and near-one peaks force at least `2M`
distinct roots of `q_M-1/2` by the intermediate value theorem.

## 2. A finite upper bound using convexity intervals

Let a continuous function on a compact interval have a partition into `s`
intervals on each of which it is convex or concave. For any `epsilon>0`,

```
p_bin<=p_conv+ceil(log2(3s)).                                      (4)
```

This comparison allows real coefficients and unrestricted finite continuous
size. It is not a polynomial-time construction claim for arbitrary functions.

To prove it, restrict any admissible `p`-integer convex lift to one interval.
Negate the output if the function there is concave. The reviewed scalar parity
and refinement argument gives an `epsilon` chord partition on that interval
with at most `3*2^p` cells. Do this on all `s` intervals. Their combined finite
chord-band union has at most `3s*2^p` polyhedra, representable with
`ceil(log2(3s*2^p))=p+ceil(log2(3s))` binaries. Take `p=p_conv`.

A nonaffine polynomial of degree `D` has at most `D-2` distinct zeros of its
second derivative. Partitioning at these roots gives
`s<=max(1,D-1)` convex or concave intervals. Consequently,

```
p_bin<=p_conv+ceil(log2(3 max(1,D-1))).                             (5)
```

The boundaries may be irrational; real coefficients are allowed in this finite
comparison. Together with (2)--(3), this shows that logarithmic dependence on
degree is the correct worst-case order for this finite binary-versus-general-
integer comparison. The family proves a lower bound on the optimal counts,
not merely on a particular construction or determinant benchmark.

## 3. A compact rational upper bound for every dense polynomial

For any densely encoded rational polynomial of degree `D>=2`, without a
convexity assumption, a polynomial-time rational construction satisfies

```
p_out<=p_conv+12+ceil(log2 D).                                    (6)
```

Affine polynomials are exact linear graphs. This consequence uses the
[convex-polynomial hybrid theorem](../notes/compiled-convex-polynomial-hybrid-precision.md)
whose full proof and analytical dependencies have passed two independent audits.

Let `M_1=max(1,sum_(k=1)^D k|c_k|)` bound the absolute first derivative.
Isolate each distinct root of `f''` in `(0,1)` in a disjoint rational bracket
of width at most `min(1,epsilon/(32M_1))`. Together with the complementary
intervals these form at most `b<=2D` pieces. Roots at the domain endpoints
need no brackets. This requires polynomial time and polynomial endpoint
encoding by exact rational univariate root isolation.

On each complementary interval `f''` has a constant sign, so its graph is
convex or concave. Negate the output in the latter case and normalize its
rational interval. Restricting a global `p`-integer convex lift gives a local
one with at most `p` integers. The scalar hybrid therefore supplies a compact
local graph formulation with at most `p+11` binary variables, and a local
cell capacity at most `2^(p+11)`.

A bracket itself needs one chord band even if curvature changes sign inside.
For an arbitrary differentiable function with derivative bounded by `M_1`,
the absolute chord error on an interval of width `h` is at most `2M_1 h`.
Here this is at most `epsilon/16`. Exact rational endpoints and polynomial
values therefore give a single rational band containing its graph with
absolute admitted error at most `epsilon/8`.

Concatenate the local cell families. Their total count is at most

```
K<=b*2^(p+11)<=2D*2^(p+11).
```

The hybrid theorem's cumulative-index circuit identifies a piece and its local
cell, and excludes unused binary codes. It can return that cell's band offsets
as well as its endpoint data, so the reversed asymmetric bands on concave
pieces create no extra integer variables. Each piece has a polynomial-time
indexed description; there are only polynomially many pieces. Common rational
denominators of polynomial encoding length decode all input and output
coordinates. For outputs, include the denominators of the polynomially many
exact bracket endpoint values as well as the fixed denominators used by local
hybrid circuits. Taking their product preserves polynomial bit length. A
fixed integer offset makes every encoded numerator nonnegative, as in the
hybrid compiler.
Thus the whole union is a polynomial-size rational MILP using

```
ceil(log2 K)<=p+12+ceil(log2 D)
```

binaries. Take `p=p_conv` to obtain (6). The algorithm itself never needs `p`:
it computes the actual local cell counts and their cumulative sums.

Together with the explicit family in Section 1, this proves that logarithmic
degree overhead is both sufficient and necessary in worst-case order for a
compact binary construction compared with all convex general-integer lifts.
The lower bound already applies to unlimited-size binary convex formulations.

## Scope and source boundary

Bernstein approximation, periodic mixed-integer encodings, and convex slices
at fixed binary assignments are established tools. The conclusion established here is
their quantitative combination for polynomial graph-approximation counts,
paired with the finite convexity-interval upper bound. The bounded source review found no matching complete theorem, but does not
establish unrestricted publication priority.

The convex scalar and separable results are unaffected: the family here has
many curvature changes and is nonconvex. The bound concerns integer count,
not solver running time, ideality, or a lower bound on continuous variables.


## Verification and source review

* [First full proof audit](../notes/review-nonconvex-polynomial-binary-integer-gap.md).
* [Second full proof audit](../notes/review-nonconvex-polynomial-binary-integer-gap-second.md).
* [Focused literature review](../notes/nonconvex-polynomial-binary-integer-gap-novelty.md).

The [exact checker](../code/quadratic_rank/check_polynomial_binary_integer_gap.py)
passes 12 rational Bernstein-value checks at degrees 4096 and 9216, four
peak-chord violations, and 90 checks of the periodic MILP branches. The written
variance argument proves the uniform approximation; finite samples alone do
not do so.

General binary-versus-integer count gaps and bounded-variable binarization are
classical; see [Dash, Gunluk, and Hildebrand](https://optimization-online.org/wp-content/uploads/2018/01/6403.pdf).
The scope here is a single connected rational polynomial graph at fixed positive
tolerance, paired with degree-dependent finite and compact upper bounds.


The [polynomial-vector extension](polynomial-vector-compiled-integer-precision.md)
merges implicit scalar knot arrays and gives a compact logarithmic-total-degree
comparison for many polynomial outputs sharing one input.
