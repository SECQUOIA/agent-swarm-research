# Pure relative graph accuracy can require infinite integer dimension

Date: 2026-09-05. Status: independently reviewed supporting consequence; see
`notes/review-relative-power-graph-integer-obstruction.md`. No priority claim.

The finite quadratic precision theorems use a strictly positive absolute
error allowance. This assumption cannot simply be replaced by a fixed
relative tolerance, even for a scalar square.

## Statement

Fix real `q>1` and finite `epsilon>=0`. There is no finite-dimensional
convex set `C` with finitely many integer coordinates whose mixed-integer
projection contains every point `(x,x^q)`, `0<x<=1`, while every admitted
point with `0<x<=1` satisfies

```
w <= (1+epsilon) x^q.
```

In particular, two-sided relative graph accuracy
`|w-x^q|<=epsilon x^q` is impossible with any finite integer dimension.
The statement permits arbitrary continuous auxiliary variables, unbounded
integer ranges, and nonclosed convex lifts. Including `x=0` in the domain
does not change the conclusion.

## Proof by integer residue classes

Choose an integer `M>=2` such that

```
M^(q-1) > 2^q (1+epsilon).
```

For every `k>=1`, choose an exact graph lift of `x_k=M^(-k)` and let
`z_k in Z^p` be its integer vector. The finite set of residue classes
modulo `M` contains two of these vectors in the same class. Denote their
inputs by `0<x<y`, so that `x/y<=1/M`. Take the convex combination with
weight `1/M` on the lift at `y` and weight `1-1/M` on the lift at `x`.
Its integer vector is

```
z_x + (z_y-z_x)/M in Z^p.
```

Its projected point `(u,v)` therefore must be admitted. But

```
0<u=y/M+(1-1/M)x <= 2y/M <= 1,
v=y^q/M+(1-1/M)x^q >= y^q/M,
v/u^q >= M^(q-1)/2^q > 1+epsilon,
```

contradicting the required upper bound. Only finitely many graph points
are needed for a given proposed `p`: any `M^p+1` points of this geometric
sequence suffice. No measurability or closure argument is involved.

## Scope and interpretation

An immediate application is the bilinear product graph on `[0,1]^2`.
Intersecting any proposed lift with the affine equation `x_1=x_2=t`
preserves its integer count and gives the square graph. Thus no finite
integer-dimensional convex lift can contain the entire product graph and
enforce `|w-x_1*x_2|<=epsilon*x_1*x_2` for any finite `epsilon`.
The same diagonal restriction applies to a product of any fixed number
`d>=2` of nonnegative factors. Fixed positive-scale slices of
quadratic-over-linear graphs likewise inherit the obstruction when the
admissible numerator slice approaches zero. Multiplying the output by
the fixed positive denominator preserves the relative tolerance. These are
direct restrictions of the proved power theorem, not additional
nonrepresentability methods.

For `q=2`, this excludes a pure relative-error version of the scalar
quadratic MILP construction on a domain approaching zero. The conclusion
is stronger than a lower bound growing with requested accuracy: every
finite relative tolerance already excludes every finite integer count.

The domain endpoint matters. On `[a,1]` with `a>0` and `epsilon>0`, any
absolute graph approximation with error at most `epsilon*a^q` gives the
relative guarantee. A strictly positive absolute error floor also removes
this particular obstruction. Neither statement applies to zero error.

The proof extends the familiar parity argument to residue classes modulo
an arbitrary integer; it is a supporting scope limitation rather than a
claimed new general lower-bound method. It does not concern epigraph-only
representations, which do not impose an upper bound on the output.

The relevant established method is the midpoint obstruction in
[Lubin, Vielma, and Zadik, Mixed-integer convex representability](https://arxiv.org/abs/1706.05135).
A bounded search on 2026-09-05 found that source and its graph
nonrepresentability consequences; it did not establish priority for this
relative-error consequence. The proof above states its own assumptions
and does not rely on rationality or closure restrictions from stronger
classification results in that paper.

## Concave powers have a sharp relative-error threshold

**Supporting proposition.** Let `0<q<1`. On `0<x<=1`, a convex lift
with finitely many integer coordinates cannot contain the entire graph
of `x^q` and satisfy two-sided relative error
`|w-x^q|<=epsilon x^q` when `0<=epsilon<1`. When `epsilon>=1`, a
continuous convex representation with no integer variables suffices.

**Proof of impossibility.** Put `c=1-epsilon>0`. Choose an integer
`M>=2` large enough that

```
M^(q-1)+M^(-q)<c.
```

For a putative formulation with `p` integer coordinates, choose graph
lifts of `M^p+1` points from the geometric sequence `x_k=M^(-2k)`.
Two integer vectors have the same residue modulo `M`. Label their
inputs `0<x<y`; then `x/y<=M^(-2)`. The convex combination with
weight `1/M` on the graph lift at `y` has integral auxiliary coordinates
and projected point

```
u=y/M+(1-1/M)x,
v=y^q/M+(1-1/M)x^q.
```

It obeys `0<u<=1`. Because `u>=y/M` and `x/y<=M^(-2)`,

```
v/u^q <= [y^q/M+x^q]/(y/M)^q
        <= M^(q-1)+M^(-q)
        < 1-epsilon.
```

This violates the required lower bound on the output. No closure,
bounded integer range, or measurability condition was used.

**Proof of attainability for larger tolerances.** The set

```
{(x,w):0<x<=1, 0<=w<=x^q}
```

is convex, since `x^q` is concave, and contains its whole graph. Its
relative error is at most one. Thus it suffices for every
`epsilon>=1` and uses no integers. If the endpoint `x=0` is included,
add `(0,0)`; the same conclusion holds. ∎

This proposition shows that the tolerance quantifier in the convex-power
result depends on the exponent. It does not extend the claim of
impossibility for every finite tolerance to concave powers.

## Relationship to the established midpoint method

Lubin, Vielma, and Zadik's *Mixed-integer convex representability*,
Lemma 4.1, uses parity classes and excluded midpoints to bound the
integer dimension; its proof is given on printed page 12 of the
[open manuscript](https://optimization-online.org/wp-content/uploads/2017/06/6082.pdf).
The residue argument here replaces the midpoint weight by `1/M`.
It is an elementary variation of that established mechanism, used to
record the behavior of relative graph error near a zero-valued endpoint.
The source defines representability with closed convex lifts, but its
finite convex-combination reasoning, as used explicitly here, does not
require closure. No new general integer-rank method is claimed.

## Truncating the zero endpoint gives double-logarithmic dimension

Fix `q>1` and `epsilon>0`. For a domain `[a,1]`, `0<a<1`, let
`p_conv(a)` and `p_bin(a)` be the least integer and binary dimensions
of whole-graph relaxations with two-sided relative error at most
epsilon. Then, as `a` decreases to zero,

```
p_conv(a)=Theta_(q,epsilon)(log log(1/a)),
p_bin(a)=Theta_(q,epsilon)(log log(1/a)).
```

The multiplicative constants in the lower and upper bounds need not
match. This is a supporting order bound, not an exact leading constant.

For the lower bound, fix the same integer M as in the q>1 proof and put
`N=floor(log_M(1/a))`. All `N+1` graph inputs
`1,M^(-1),...,M^(-N)` lie in `[a,1]`. No two of their chosen integer
lifts may have the same residue modulo M: the convex-combination
contradiction above would then give an admitted input between them,
and hence still inside `[a,1]`. Thus

```
M^p >= N+1,
p_conv(a) >= log_M(1+floor(log_M(1/a))).
```

For the upper bound, choose `rho=(1+epsilon)^(1/q)>1`. Divide `[a,1]`
into at most

```
K=max{1,ceil(log(1/a)/log rho)}
```

geometric intervals `[l,u]` satisfying `u/l<=rho`, truncating the last
interval at a. On each interval use the simple rectangle

```
l<=x<=u,       l^q<=w<=u^q.
```

It contains the interval's exact graph, and every point in it obeys

```
1/(1+epsilon)<=w/x^q<=1+epsilon.
```

Since `1-1/(1+epsilon)<=epsilon`, this gives the required two-sided
relative error. Encode the finite union of these bounded rectangles
with distinct binary codes and a convex-hull disjunctive lift. It uses
at most `ceil(log2 K)` binaries, so

```
p_bin(a)<=log2 log(1/a)+O_(q,epsilon)(1).
```

The lower bound applies to unrestricted integer ranges and arbitrary
convex lifts. The upper construction is elementary and may use
`O(log(1/a))` continuous variables and rows. Its real coefficients are
unrestricted, as in the rest of this note. The positive-tolerance
assumption matters: exact graph representation on any interval of
positive length is excluded by the usual strict-convexity midpoint
argument.
