# Pure powers have degree-independent finite integer counts

Date: 2026-09-05. Status: independently reviewed finite theorem.

For positive sums of pure coordinate powers, the minimum integer count
can be characterized with an additive linear-dimension error independent
of the degrees. The construction proving the finite upper bound can have
exponentially many rows in the desired accuracy encoding. The existing
polynomial-size construction still has an additional degree-dependent
term. Keeping these two claims distinct identifies an open compactness
question. A compact rational inverse-power interpolation approach is
now under separate investigation; no conclusion about its feasibility
is drawn here.

## Finite statement

Consider

```
f_j(x)=l_j^T x+b_j+sum_(i=1)^r c_ji x_i^(D_i),
x in [0,1]^r,        c_ji>=0,        integers D_i>=2.
```

Each coordinate is active. Additional coordinates occurring only affinely
may be retained continuously without changing the minimum integer count.
Let `K subset R^m` be a compact convex unconditional body with zero in its
interior, and define the whole-graph approximation minima as in the
[positive polynomial theorem](../results/positive-separable-unconditional-error-precision.md).
Put

```
C=(c_ji),
D_alloc=max{product_i p_i: 0<=p_i<=1, Cp in K},
Phi=-(1/2)log2 D_alloc,
A_r=(r/2)+log2[omega_r(r+2)^(r/2)]<7r/2.
```

For real-coefficient convex and binary linear lifts of unrestricted size,

```
max(0,Phi-A_r)<=p_conv<=p_bin<=Phi+2r.                  (1)
```

Thus the finite comparison `p_bin<=p_conv+11r/2` is independent of all
`D_i`. No polynomial bound on the size of the finite upper construction
is included in (1).

For rational dense input and an unconditional body with the previously
stated rational strong-oracle and radius assumptions, the existing compact
original-coordinate Taylor construction yields instead

```
p_out<=Phi+sum_i log2 D_i+r+1/(2ln2)
     <=p_conv+sum_i log2 D_i+(9r/2)+1.                  (2)
```

This construction has polynomial size and polynomial construction time.
The stronger finite lower bound here improves the comparison for this
pure-power subclass, but does not prove a compact algorithm attaining (1).

## A common power transform strengthens the lower bound

For every integer `D>=2` and `a,b in [0,1]`, convexity of `x^(D/2)` gives

```
(a^D+b^D)/2-((a+b)/2)^D
 >=(1/4)(a^(D/2)-b^(D/2))^2.                           (3)
```

The map `t_i=x_i^(D_i/2)` is a homeomorphism of the cube onto itself.
For two graph points in a parity support, their nonnegative Jensen error
vector belongs to `K`. After mapping the support into the `t` cube, (3)
gives

```
0<=(1/4)sum_i c_ji(t_i-s_i)^2<=J_j.
```

For independent uniform points in a positive-volume transformed support,
with covariance `Sigma`, taking expectation gives
`(1/2)C diag(Sigma)<=EJ` coordinatewise. Since `EJ in K`, unconditionality
implies that `p_i=Sigma_ii/2` is feasible for `D_alloc`. Its cap follows
from `Sigma_ii<=1/4`. Hadamard's determinant inequality gives

```
vol(transformed support)
 <=omega_r(r+2)^(r/2) product_i sqrt(Sigma_ii)
 <=2^(r/2)omega_r(r+2)^(r/2) sqrt(D_alloc).
```

The transformed supports cover the whole unit cube. This proves the lower
bound in (1). No preservation of the original support volume is needed.
The Gaussian volume bound gives `A_r<7r/2`, including `r=1`.

## Uniform chord error in power coordinates

Let `f(x)=x^D`, `D>=2`, and let `s_[a,b]` be its chord on `[a,b]`, where
`0<=a<b<=1`. Set `A=a^(D/2)`, `B=b^(D/2)`, and `Delta=B-A`. Then

```
0<=s_[a,b](x)-x^D<=4Delta^2 for all x in [a,b].          (4)
```

If `A<=B/2`, the chord is at most `B^2`, which is at most `4Delta^2`.
If `A>B/2`, then `a>0`. The standard twice-differentiable chord bound and
the mean-value lower bound for `x^(D/2)` give

```
s_[a,b](x)-x^D
 <=[D(D-1)b^(D-2)/8](b-a)^2,
b-a <=(2/D)a^(1-D/2)Delta.
```

Combining them gives a bound of

```
[(D-1)/(2D)](b/a)^(D-2)Delta^2 <=2Delta^2,
```

because `(b/a)^(D/2)=B/A<2`. This proves (4), including `D=2`.

## Finite binary encoding of the nonuniform grid

Take any positive feasible allocation `p`. For coordinate `i`, let

```
L_i=ceil[(1/2)log2(1/p_i)]+1,
h_i=2^(-L_i),
a_ik=(k h_i)^(2/D_i),        k=0,...,2^(L_i).
```

These knots divide the coordinate interval into exactly `2^(L_i)` cells.
On each cell, (4) bounds the chord error by `4h_i^2<=p_i`. Introduce a
shared scalar approximation `z_i` and, on the selected cell, impose

```
a_ik<=x_i<=a_i,k+1,
s_cell(x_i)-4h_i^2<=z_i<=s_cell(x_i).
```

This band contains the exact power graph and implies
`|z_i-x_i^(D_i)|<=4h_i^2`. Define the final outputs exactly by
`w_j=l_j^T x+b_j+sum_i c_ji z_i`. Every original exact graph point is
admitted, and every admitted error satisfies `|w-f(x)|<=Cp`, hence belongs
to `K` by unconditionality.

A finite union of the cell bands can be encoded with `L_i` binary variables:
assign the `2^(L_i)` cells all binary strings of length `L_i`, and relax
each cell's inequalities by a sufficiently large multiple of its Hamming
distance from the chosen binary string. Bound `x_i` and `z_i` globally so
finite valid constants exist. For each binary assignment exactly one cell
has zero distance, so its complete band is imposed. Conversely, a point
in that band is admitted with its assigned string after choosing the
constants to make every other cell's inequalities redundant. This is a
linear mixed-binary formulation with real coefficients and no additional
integers.

The count satisfies

```
sum_i L_i<=-(1/2)log2 product_i p_i+2r.
```

At an optimal allocation this proves the upper bound in (1). Its row count
is on the order of `sum_i 2^(L_i)`; the number of nonzero coefficients
also includes a factor proportional to each cell's bit count. Neither
bound is polynomial in the accuracy encoding in general. The generally
irrational knot locations are also why (1) is explicitly a real-coefficient
finite statement. Rational approximation of knots can retain a similar
finite count with extra constant slack, but that variant is not needed
for the stated result and is not used to infer bit complexity.

For the compact rational claim (2), apply the already reviewed original
coordinate prefix-power construction and log-product allocation oracle.
Its binary count is `Phi+sum_i log2 D_i+r+1/(2ln2)`. Combining it with the
stronger lower bound above yields (2).

## Scope and novelty boundary

Each coordinate has one power shared across all outputs. When several
powers of the same coordinate occur, their separate square-root transforms
do not automatically give this same degree-independent lower benchmark.
The general positive-polynomial theorem remains the applicable result.

Nonuniform interpolation, logarithmic encoding of finite disjunctions,
and power transformations are established ideas. No standalone novelty
claim is made for those ingredients. The proposed observation is the
finite whole-formulation count with constants uniform in the degrees,
and its distinction from polynomial-size rational construction. The [bounded source audit](pure-power-degree-independent-count-novelty.md)
records adaptive interpolation and logarithmic disjunction predecessors,
while finding no matching whole-formulation bound. Publication priority
remains unestablished.

The [first independent audit](review-pure-power-degree-independent-count.md)
and [second independent audit](review-pure-power-degree-independent-count-second.md)
both passed. The [exact checker](../code/quadratic_rank/check_pure_power_reciprocal_interpolation.py)
passed 3,348 uniform chord inequalities and 60 reciprocal interpolation
identities; the first reviewer additionally checked 8,316 exact cases.

The [compact reciprocal candidate](compact-pure-power-reciprocal-interpolation.md)
uses a separate rational inverse-power approximation lemma to seek the same
degree-independent order with polynomial size. Its status is stated there;
this finite theorem does not depend on that candidate.
