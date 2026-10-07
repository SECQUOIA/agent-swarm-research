# An all-scale count removes the two-dimensional value-oracle restriction

Date: 2026-10-02. Status: passed a
[fresh independent actual-file review](../reviews/all-scale-core-value-oracle-review.md).
This note extends the reviewed
[core-only value oracle](core-only-noise-value-oracle.md) to any number
of core coordinates. The new step is a weak first-moment bound on one
random factor controlling every grid scale. It uses neither a product
of directional growth constants nor a volume quantifier-elimination
claim. No publication-priority claim is made.

## 1. Statement and inherited interfaces

Use the input of the predecessor with arbitrary `k>=1`: an explicit
fixed-degree rational polynomial `F_0(v,z)` on
`[0,1]^k x [0,1]^m`, convex in `z` for every `v`, with verified
`partial_ii F_0<=L` for all core coordinates on the full product box.
Certificate data and polynomial verification work are included in the
base length `I`. A verifier with a different cost is charged separately.
Let `sigma>0` be rational. Put

```
f(v)=min_z F_0(v,z),
F_c(v,z)=F_0(v,z)-c'v.
```

The sign of the independent uniform core noise is immaterial. There is
one base-computable power-of-two grid size `M`, with
`log M=poly_d(I)`, such that the independent endpoint-inclusive uniform
`M`-point noise in `[-sigma,sigma]^k` has the following property.
For every query `q>=0`, the same sampled objective admits a feasible
rational point and a certified rational optimal-value interval of width
at most `2^(-q)`. Every draw is handled correctly. Expected bit work and
proof/output size per query are at most

```
f_d(k) (1+L/sigma)^k poly_d(I+q),                         (1)
```

where the polynomial exponent does not depend on `k` or `m`.
More strongly, one random work factor of that expected size controls
all query precisions simultaneously. There is no residual perturbation,
residual strong-convexity assumption, optimizer-coordinate oracle, or
expanded polynomial-size algebraic-output claim.

The proof uses the predecessor's three deterministic interfaces:

- certified convex residual value evaluation and a rational feasible
  witness in polynomial bit work, without a residual growth modulus;
- dyadic core-cell refinement with corner uncertainty
  `eta=e_h=kLh^2/8`, globally valid lower bounds, and incumbent gap
  at most `2e_h`;
- an all-draw exact fallback costing
  `B_0 poly_d(I+b+q)`, where `B_0=2^(poly_d(I))` is base-computable
  and independent of sampled coefficient length `b` and query `q`.

For each retained cell, one corner has true projected objective at most
`f_c^*+4e_h`. There are at most `2^k` incident cells per corner and
`2^k` children per parent. The analysis below bounds these witnesses
simultaneously for every real scale `0<h<=1`. It does not change the
cell algorithm or require computing a conjugate.

## 2. A geometric factor controlling every scale

Assume `L>0`. For `c in R^k` and `0<h<=1`, define

```
epsilon_h=k L h^2/2,
S_h(c)={x in [0,1]^k: f(x)-c'x <= min_v(f(v)-c'v)+epsilon_h},
K_h(c)=conv(S_h(c))+[-h/4,h/4]^k.                         (2)
```

Continuity and compactness make `S_h` nonempty and compact. The padded
convex body `K_h` is full-dimensional. Let

```
D_h(c)=max_{y_0,...,y_k in K_h(c)}
                     |det(y_1-y_0,...,y_k-y_0)|,
A(c)=sup_{0<h<=1} D_h(c)/h^k,
W(c)=max(1,A(c)).                                        (3)
```

Allow `A=+infinity`. The event `A>T` has the finite semialgebraic
description proved in Section 5, so these extended quantities are
measurable.

Two elementary volume comparisons will be used. For a compact convex
body `K`, with maximum simplex determinant `D(K)`,

```
D(K)/k! <= Vol(K) <= 2^k D(K).                          (4)
```

The first inequality uses the maximizing simplex. For the second,
fix maximizing vertices `y_0,...,y_k`. Every point of `K` has all its
barycentric coordinates of absolute value at most one: replacing a
vertex with that point multiplies the determinant by the corresponding
coordinate. In particular the `k` coefficients relative to the edge
basis lie in `[-1,1]^k`. The associated parallelepiped has volume
`2^k D(K)` and contains `K`.

Suppose `N_h` distinct grid nodes of side `h` belong to `S_h(c)`.
Their cubes of side `h/2`, centered at the nodes, have disjoint interiors
and lie in `K_h(c)`. They need not lie in the feasible core box; the
padding was introduced for this reason. Thus

```
N_h (h/2)^k <= Vol(K_h) <= 2^k D_h,
N_h <= 4^k A(c).                                        (5)
```

Each retained cell has a node counted by `N_h`. Therefore the number
of generated cells at the next level is at most `4^k N_h`, hence

```
generated cells at every level <= 16^k W(c).             (6)
```

This bound includes the initial cell. It holds for every permitted
choice of approximate residual oracle answers and incumbents, since
the true near-optimal witness property is deterministic.

## 3. A locally finite measure from convex conjugacy

Extend the convex conjugate to all coefficient space:

```
b(c)=max_{x in [0,1]^k}(c'x-f(x)),
H(c)=b(c)+||c||^2/(2L).                                 (7)
```

The finite convex function `b` has every subgradient in `[0,1]^k`.
The function `H` is `1/L`-strongly convex on all of `R^k`.
Consequently `H*` is finite, continuously differentiable, with
`L`-Lipschitz gradient, and

```
y in partial H(c)  iff  grad H*(y)=c.                   (8)
```

Define a Borel measure by pushing ordinary Lebesgue measure through
this continuous map:

```
mu(E)=Leb({y: grad H*(y) in E}).                         (9)
```

This avoids an assumption that `b` is smooth or that a Hessian
determinant exists everywhere. If a bounded set `E` lies in a coordinate
box `[a,b]^k`, its inverse image in (9) lies in
`[0,1]^k+[a,b]^k/L`, by (8). Hence `mu` is locally finite.

Fix `x in S_h(c)` and put `y_0=x+c/L`. The near-optimality inequality
implies, for every `t in R^k`,

```
b(t)>=b(c)+x'(t-c)-epsilon_h.
```

For the convex nonnegative Fenchel residual

```
r_c(y)=H(c)+H*(y)-c'y,
```

this gives `r_c(y_0)<=epsilon_h`. Strong convexity of `H` also gives

```
||grad H*(y_0)-c|| <= sqrt(2L epsilon_h).
```

For `u in [-h/4,h/4]^k`, the smooth upper bound on `H*` yields

```
r_c(y_0+u)
 <= epsilon_h+sqrt(2L epsilon_h)||u||+(L/2)||u||^2
 <= (25/32) k L h^2
 <= k L h^2.                                            (10)
```

The sublevel set of `r_c` is convex. Taking the convex hull over `x`
therefore shows that every `y in K_h(c)+c/L` satisfies (10).
For any such `y`, strong convexity again gives

```
||grad H*(y)-c|| <= sqrt(2k) L h < 4k L h.
```

Translation invariance of volume and (9) now imply

```
Vol(K_h(c)) <= mu(B(c,4k L h)),                         (11)
```

where `B` is an open Euclidean ball. The deliberately larger radius
avoids any issue concerning measure on the boundary of a ball.

## 4. Continuous noise: an all-scale weak first-moment bound

Let `Q=[-sigma,sigma]^k` and `R=4kL`. Every ball in (11) centered in
`Q`, with `h<=1`, lies in `Q_R=[-sigma-R,sigma+R]^k`. Thus

```
mu(Q_R) <= (1+2sigma/L+8k)^k.                           (12)
```

If `A(c)>T`, some `h in (0,1]` satisfies `D_h>T h^k`.
Equations (4) and (11) give a ball of radius `r=R h` with

```
mu(B(c,r)) > T r^k/(k! R^k).                           (13)
```

The elementary `5r` covering lemma selects countably many disjoint
balls from this bounded-radius family whose fivefold enlargements cover
all its centers. The selected original balls lie in `Q_R`. Summing
their measures, and then the volumes of their enlarged balls, proves

```
Leb({c in Q:A(c)>T})
 <= 5^k v_k k! R^k mu(Q_R)/T,                           (14)
```

where `v_k` is the volume of the unit Euclidean ball. No differentiation
or absolute continuity of `mu` is required. Dividing by `(2sigma)^k`,
using `v_k<=2^k`, and enlarging constants gives the explicit bound

```
P_cont{A>T} <= a_k/T,
a_k=(180 k^3)^k (1+L/sigma)^k.                          (15)
```

The factor is intentionally conservative. The substantive point is the
power `T^-1` in every dimension, rather than `T^(-2/k)` obtained by
bounding a whole near-optimal set with the weakest point-growth constant.

## 5. The all-scale event has a finite-law section bound

For each fixed real `T>0`, the event `A(c)>T` is equivalent to a formula
with two quantified blocks of polynomial size in `I`.

The existential block selects `0<h<=1`, `k+1` points `y_i` of `K_h`,
and a Caratheodory representation for each:

```
y_i=sum_{j=0}^k lambda_ij x_ij+u_i,
lambda_ij>=0,  sum_j lambda_ij=1,
|u_i,l|<=h/4.                                           (16)
```

It also selects feasible residual witnesses `z_ij`. Require

```
F_c(x_ij,z_ij) <= F_c(v,z)+k L h^2/2
                 for every (v,z) in the original box,   (17)
```

for every pair `(i,j)`. This is exactly `x_ij in S_h(c)`:
attainment supplies a residual witness in one direction, and minimizing
the right side supplies the other. All conditions (17) use the same
single universal block `(v,z)`. Finally require

```
|det(y_1-y_0,...,y_k-y_0)| > T h^k.                     (18)
```

For polynomial-size explicit encoding, do not expand a symbolic
determinant into `k!` monomials. Instead add existential real matrices
`Q,R` with `Q'Q=I`, `R` upper triangular with positive diagonal, and
`(y_1-y_0,...,y_k-y_0)=QR`. Add scalar product chains for the diagonal
product of `R` and for `h^k`, and compare the former with `T` times the
latter. The strict threshold in (18) forces nonsingularity; every
nonsingular real matrix has such a QR factorization, and its diagonal
product is the absolute determinant. Conversely these equations imply
that same determinant value. All new equations have degree at most two,
use polynomially many explicitly encoded monomials, and stay in the
existential block. These are analysis witnesses, not numerical matrix
factorizations performed by the algorithm.

Caratheodory's theorem is applicable because `S_h` is compact; there is
no relaxation from its convex hull to a different near-optimal set.
The strict supremum event in (3) is equivalent to the existence of such
an `h`; no attainment at `h=0` is asserted.

There are `O(k^2(k+m)+k^2)` variables, polynomially many atoms and
polynomial-size explicitly encoded polynomials, of degree bounded by
`max(d,2)`. When one coefficient `c_l` is free, all other coefficients
and `T` may be arbitrary fixed reals. The same fixed-block real
quantifier-elimination bound used in
[the finite-noise tail interface](polynomial-finite-noise-tails.md)
therefore gives a base-computable scalar-section component bound

```
C_sec=2^(poly_d(I)),                                    (19)
```

uniform in those fixed values. Only the number, degrees and variable
blocks determine this bound, not coefficient heights or the size of `T`.
No quantifier for a volume or an integral has been used.

Replacing the `k` noise marginals one at a time, including arbitrary
mixed continuous/discrete conditioning measures, bounds the discrepancy
between uniform continuous noise and the endpoint-inclusive grid by
`2k C_sec/M`. Let `C_0>=max(1,2k C_sec)` be a base-computable integer.
Then, for all `s>=1`, one finite law satisfies

```
P{W>s} <= a_k/s+beta,   beta=C_0/M.                     (20)
```

In particular `P{W=+infinity}<=beta`. The section argument handles
arbitrary tied or singular atoms; they are not silently removed from
the sampling law.

## 6. One cap and one rational law work at every accuracy

Choose before sampling a base-computable integer `B>=max(2,B_0)` with
`log B=poly_d(I)`, and choose `M` to be the least power of two at least
`max(2,C_0 B)`. Thus `beta B<=1` and sampled coefficient lengths are
polynomial in the base input, independent of query accuracy.

Use exactly the predecessor's dyadic refinement and two-pass filtering,
but cap the number of generated cells at

```
T_cells=16^k B.                                         (21)
```

Check the number of children before constructing or querying an
oversized level. If the cap would be exceeded, use the all-draw exact
fallback on this same objective. List processing remains linear in the
generated count. The `2^k` corner calls per cell are absorbed into the
explicit parameter factor, not treated as a dimension-independent
constant.

By (6), hitting the cap at any scale or any query precision implies
`W>B`. Without a cap, accuracy `2^(-q)` needs only `O(I+q)` levels,
with polynomial bit work per corner. With the cap, the entire work and
record length, simultaneously for every query, are bounded by

```
[f(k) min(B,W)+B_0 1_{W>B}] poly_d(I+q).                (22)
```

Integrating (20) gives

```
E min(B,W) <= 1+a_k log B+beta B,
B P{W>B} <= a_k+beta B.                                (23)
```

The logarithm and base bit lengths are polynomial in `I`; (22)--(23)
prove (1). This is one uniform random work factor, with no union over
levels or future queries. Neither the cutoff nor the finite noise law
depends on `q`. In particular the proof has no condition `M h>=1`.

If `L=0`, independent endpoint rounding shows that the optimum is the
minimum of the `2^k` convex residual vertex values. Their certified
evaluation directly gives deterministic `2^k poly_d(I+q)` work.

## 7. Scope, comparison and verification

The stronger conclusion is a value Cauchy oracle for one fixed sampled
objective in arbitrary core dimension. It remains compatible with the
known obstacles to efficiently extracting a selected residual optimizer.
It does not replace the exact optimizer output of the special bilinear
flow/TU theorems, and does not perturb or solve the unperturbed instance.
The separate [continuous-noise oracle](continuous-core-noise-value-oracle.md)
obtains arbitrary-dimensional expected work more directly from counts at
each scale and an infinite random-bit stream. The present result instead
returns one rational sampled objective, with a finite law fixed before
all accuracy queries; its all-scale proxy and rare exact fallback are
what permit that stronger sampling interface.

The conjugacy and covering tools are classical. The
[focused prior audit](../prior-art/all-scale-core-value-oracle-prior.md)
identifies the weak `1/T` estimate as an instance of the classical
weak-(1,1) centered maximal inequality for a locally finite measure,
here restricted to the expanded noise cube. The proposed advance over
the local predecessor is their use to construct a semialgebraic,
all-scale count proxy with a weak first-moment tail. This permits one
finite-law cap/fallback argument in every dimension. The audit records
the specific source-access boundaries; no novelty conclusion follows
from this derivation or the prior search.

The fresh review independently checked the geometry, finite-law formula,
constants and arithmetic. It caught the original determinant-format
shortcut; Section 5 now contains the reviewed quadratic QR encoding.
The distinct exact diagnostic
`python3 -B research-20261002/new-direction/check_all_scale_core_geometry.py`
passed four fixtures, 1,030 near-optimal grid nodes, 7,770 padded Fenchel
residual and inverse-gradient inequalities, 15 maximum-simplex node
bounds, two signed rational QR witnesses, and a singular pushforward
measure fixture. The examples combine diagonal quadratics and quartic
double wells, including tied finite-noise atoms and a three-dimensional
case. All arithmetic is rational. This diagnostic checks the new geometry;
it is not a general recourse implementation, a quantifier-elimination
implementation, or a probability simulation. No root indices,
project-wide tests or CI checks are part of this work.
