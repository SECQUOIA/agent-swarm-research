# One-input vector powers defeat scalarization and midpoint refinement

Date: 2026-09-05. Status: independently reviewed supporting boundary. The
[first audit](review-positive-polynomial-vector-refinement-obstruction.md) and
[second audit](review-positive-polynomial-vector-refinement-second.md) both passed.
Both audits also passed the finite upper bounds below.
This does not settle whether a polynomial rational construction can
stay within additive `O(1)` of the true convex-lift integer minimum for
arbitrary positive polynomial vector outputs.

The example below isolates two failures of scalar proof mechanisms. All
pairwise graph midpoints satisfy the requested error bound, and every fixed
linear scalarization needs at most one binary variable. Nevertheless the
vector graph requires an unbounded number of integer coordinates. Its
interval chord-cover count also has no constant-factor stability when the
error is halved.

## Family and claims

For `M>=1`, define

```
D_j=128*1024^(j-1)=2^(10j-3),
F_j(x)=(7/4)x^(D_j),    j=1,...,M,
0<=x<=1,
K=[-1,1]^M.
```

These are positive rational polynomial outputs of one input. The instance
is also meaningful in dense encoding, although binary sparse encoding is
much shorter. Let `p_conv` be the minimum number of unrestricted integer
coordinates in a convex lift containing the exact vector graph with error
in `K`. Let `p_bin` impose binary coordinates instead. No formulation-size
restriction or rational-coefficient restriction is imposed in these finite
counts. Then

```
ceil(log_3 M)<=p_conv<=p_bin,
ceil(log2 M)<=p_bin<=ceil(log2(M+1)).               (1)
```

Moreover:

- Every pair of exact graph points has midpoint error strictly below
  `7/8` in every output component.
- For every real `lambda` with `sum_j |lambda_j|=1`, the scalar graph
  `g_lambda=lambda^T F`, at its natural scalar error tolerance one, has
  a finite binary linear formulation with at most one binary variable.
- If `N_F(epsilon)` denotes the minimum number of input intervals whose
  vector chord errors are at most `epsilon` in the infinity norm, then
  `N_F(2)=1` while `N_F(1)>=M`.

Thus neither the strongest fixed linear scalarization nor pairwise midpoint
compatibility characterizes the vector integer count up to an additive
constant, even for this one-input positive-power family.

## Midpoint compatibility everywhere

For any convex differentiable scalar function `f`, its midpoint Jensen gap

```
J_f(a,b)=[f(a)+f(b)]/2-f((a+b)/2),    a<=b,
```

is nonincreasing in `a` and nondecreasing in `b`: its partial derivatives
are `(f'(a)-f'((a+b)/2))/2` and
`(f'(b)-f'((a+b)/2))/2`. Hence, for every component in this family,

```
0<=J_(F_j)(a,b)<=J_(F_j)(0,1)
 =7/8-(7/4)2^(-D_j)<7/8<1.                       (2)
```

Every midpoint test is therefore compatible, including tests involving
arbitrary input points rather than just the selected witnesses below.

## A non-midpoint obstruction and integer lower bounds

Choose `M` rational inputs

```
x_j=1-64/D_j in [1/2,1).
```

For `j<ell`, the ratio `D_ell/D_j` is at least 1024. Bernoulli's inequality
gives

```
x_ell^(D_j) >=1-64D_j/D_ell>=15/16.               (3)
```

Set `xi=(x_j+2x_ell)/3`. Then

```
xi=1-64/(3D_j)-128/(3D_ell)
   <=1-64/(3D_j).
```

Using `1-u<=exp(-u)` and `exp(v)>=1+v`,

```
xi^(D_j)<=exp(-64/3)<=3/67.                       (4)
```

The two-thirds chord error in output `j` is consequently at least

```
[F_j(x_j)+2F_j(x_ell)]/3-F_j(xi)
 >=(7/4)[(2/3)(15/16)-3/67]
 =2177/2144>1.                                   (5)
```

Select an integer lift of every exact graph point at `x_j`. If two selected
integer vectors agree coordinatewise modulo three, their weighted average
with coefficients `1/3,2/3` is integral. Convexity of the lifted set then
admits the projected point in (5), contradicting the error guarantee.
Thus there must be at least `M` distinct residue vectors in `{0,1,2}^p`,
which proves `3^p>=M` for arbitrary integer lifts.

For binary lifts, two exact graph witnesses with the same binary vector
may be combined with any real convex weight while retaining that vector.
Equation (5) therefore requires distinct binary vectors for all `M`
witnesses, proving `2^p>=M`. These arguments need only finitely many
witnesses; closedness, bounded integer ranges, and measurability are not
assumed.

## Finite upper bound and failure of vector refinement

Each output increases continuously from zero to `7/4`. Its half-height
point is `a_j=2^(-1/D_j)`, where `F_j(a_j)=7/8`. Sort these points together
with zero and one. They partition the input interval into `M+1` subintervals.
On each such interval, each component stays entirely below or entirely above
its own half-height point. Its range on that interval therefore has length
at most `7/8`.

The product rectangle consisting of the input interval and the component
output ranges contains every graph point on that interval and admits only
component errors of magnitude at most `7/8`. A finite union of these
bounded rectangles has a linear formulation with
`ceil(log2(M+1))` binary selectors, using standard binary codes. The
endpoint constants may be real algebraic numbers; this is a finite count
statement, not yet a polynomial rational construction claim.

For the chord-cover statement, every full-domain component chord and every
component graph value lie in `[0,7/4]`. Convexity therefore gives full-domain
chord error at most `7/4<2`, so `N_F(2)=1`.

An input interval containing two of the points `x_j,x_ell` cannot have vector
chord error at most one. The chord over that containing interval lies above
the chord joining the two selected graph points, componentwise: it lies above
the convex function at both selected endpoints, and the difference of the
two chords is affine. At `xi`, (5) therefore remains a strict obstruction.
Every admissible interval contains at most one selected point, and covering
all of them requires at least `M` intervals. In particular, the scalar
three-piece error-halving argument cannot have a vector analogue with a
constant number of pieces independent of output count.

## All fixed linear scalarizations remain easy

Fix `lambda` with `sum_j |lambda_j|=1`. Define the increasing reference
function

```
Psi(x)=sum_j |lambda_j|F_j(x).
```

It increases continuously from zero to `7/4`. For `a<=b`,

```
|g_lambda(b)-g_lambda(a)|<=Psi(b)-Psi(a).           (6)
```

Partition at the unique point where `Psi=7/8`. On either resulting compact
interval, (6) bounds the full range of `g_lambda` by `7/8`. Use an input-output
rectangle with its actual minimum and maximum on that interval. The two
rectangles contain the scalar graph and admit only error at most `7/8`.
Their union needs one binary variable. This argument allows negative
scalarization coefficients; scalar convexity is not assumed.

The unit scalar tolerance is the correct one induced by `K`, since
`h_K(lambda)=sum_j |lambda_j|=1`. Consequently the separation is not
produced by scaling the scalarized error incorrectly.

## What remains open

The example proves that the vector problem needs additional information
beyond all fixed scalarizations and midpoint-compatible intervals. It
does not prove an unbounded difference `p_bin-p_conv`: the bounds in (1)
leave a factor between `log_3 M` and `log2 M` in the unrestricted-integer
count. It therefore does not rule out a construction within additive
`O(1)` of `p_conv` using unrestricted integer variables, or a sharper
argument showing the binary count is already nearly optimal here.

The modulo-three argument is the same elementary convex-combination
principle used by the repository's relative-power obstruction, extending
the familiar parity argument. The literature antecedent for that general
style of obstruction is
[Lubin–Vielma–Zadik, *Mixed-integer convex representability*](https://arxiv.org/abs/1706.05135).
Fixed-knot interpolation and finite binary disjunctions are established
tools. A bounded search of simultaneous convex interpolation and mixed-integer
graph approximation did not locate this combined family and conclusion;
this is a supporting boundary, with no claim of established publication
priority.

## Finite upper bounds with output-dependent overhead

The failure of a dimension-independent refinement factor still permits a
general logarithmic output-count bound. Let `F:[a,b]->R^m` be continuous and
componentwise convex, and let the error body be a box
`K=prod_j[-epsilon_j,epsilon_j]` with every `epsilon_j>0`. For finite
real-coefficient formulations, with no size restriction,

```
p_bin<=p_conv+ceil(log2(2m+1)).                    (7)
```

Here `p_bin` may be taken over binary linear lifts and `p_conv` over convex
lifts with unrestricted integer coordinates. Thus the assertion is stronger
than merely permitting nonlinear convex constraints on both sides.

To prove it, take a convex lift with `p` integer coordinates. For each
parity vector, collect the input points of exact graph witnesses with that
parity and take their closure. The nonempty closures have interval hulls
covering `[a,b]`. If `[u,v]` is one such hull, the endpoint midpoint Jensen
vector belongs to `K`, by taking limits of pairs of original witnesses.
For each output, its chord gap `g_j` on `[u,v]` is nonnegative and concave,
vanishes at the endpoints, and satisfies

```
max g_j<=2g_j((u+v)/2)<=2epsilon_j.               (8)
```

For a scalar concave gap between zero and `2epsilon`, cut at the two
crossings of level `epsilon` if its maximum exceeds that level. On the two
outside intervals its gap is at most `epsilon`; subtracting the affine
interpolation of its endpoint gaps cannot increase that bound. On the
middle interval the endpoint gaps both equal `epsilon`, so its local gap
is `g-epsilon<=epsilon`. Thus at most two cuts make every local scalar
chord error at most `epsilon`. If the original maximum is already at most
`epsilon`, no cut is needed.

Overlay these cuts for all `m` outputs. There are at most `2m` cut points,
hence at most `2m+1` intervals. Restricting an interval does not increase
the local chord error of a convex function, so each resulting interval
has every output chord error at most its `epsilon_j`.

On one resulting interval, let `T_j(x)` be its affine component chords.
The polyhedral band `T_j(x)-epsilon_j<=w_j<=T_j(x)` contains the exact
vector graph and admits only errors in `K`. There are at most
`(2m+1)2^p` such bands. A finite binary disjunction uses at most
`p+ceil(log2(2m+1))` bits, proving (7). Singleton parity hulls are represented
as degenerate intervals with their exact output values.

### Unconditional polytopes with nonnegative facet normals

A safe related statement holds for

```
K={e in R^m: A|e|<=b},
A>=0,    b>0,
```

where `A` has `q` rows and `K` is compact. Then

```
p_bin<=p_conv+ceil(log2(8q+1)).                    (9)
```

On each parity hull the vector chord gap is bounded componentwise by twice
its midpoint gap, hence `A g(x)<=2b`. Each scalarized function given by a
row of `A F` is convex. Apply the preceding scalar refinement twice to
that row: first from `2b_k` to `b_k`, then from `b_k` to `b_k/2`. This
uses at most nine scalar intervals, or eight cuts, for that row. Overlay
the cuts for all rows to get at most `8q+1` intervals satisfying
`A g(x)<=b/2`. Because `g>=0`, this means `g(x) in K/2`.

For each interval use the polyhedral band

```
w-T(x) in K/2.
```

It contains the exact graph since `F-T=-g in K/2`. Every permitted error
satisfies `w-F=(w-T)+g in K`, by convexity and symmetry. The same binary
disjunction count proves (9). Absolute values in the description of `K`
can be represented using continuous linear auxiliaries.

The extra factor in (9) has a purpose. Merely knowing the chord gap belongs
to `K` does not justify subtracting another arbitrary vector of `K` while
retaining error in `K`; in general their difference lies only in `2K`.
For example, in the two-dimensional unit `l_1` ball both `(1,0)` and
`(0,1)` belong to its nonnegative part, but their difference has `l_1`
norm two. A chord gap equal to the first vector and a downward band shift
equal to the second therefore produce an inadmissible error.
The box band used in (7) exploits coordinatewise bounds, which need not
preserve a coupled unconditional body. The half-body construction avoids
that unsupported step.

Neither (7) nor (9) asserts polynomial construction time, rational knot
encoding, or that its logarithmic overhead is necessary relative to the
true minimum. The family above proves the lack of constant-factor
error-halving for simultaneous chords, not a matching lower bound on
`p_bin-p_conv`.
