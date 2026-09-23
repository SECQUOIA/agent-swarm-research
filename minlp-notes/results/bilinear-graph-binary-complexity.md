# Integer dimension of simultaneous bilinear approximation

Date: 2026-09-05. Main theorem passed two independent proof reviews,
including its unrestricted-integer convex-lift extension. A dedicated
primary-literature audit found no matching graph precision theorem;
publication priority remains unestablished. The rational preprocessing
guarantee also passed the second reviewer's final read.

## Main statement

Let `G=(V,E)` be a finite simple graph, with `n=|V|`, and define

```
Q_G = {(x,w): x in [0,1]^V, w_ij=x_i x_j for ij in E}.
```

A mixed-integer convex relaxation has the form

```
R = {(x,w): there exist y in R^q, z in Z^p with (x,w,y,z) in C},
```

where `C` is any convex set and `Q_G subset R`. Neither the range of the
integer coordinates nor the dimension of the continuous lift is bounded.
Require componentwise vertical accuracy

```
|w_ij-x_i x_j| <= epsilon_ij
for every (x,w) in R with x in [0,1]^V and every ij in E.
```

Every `epsilon_ij` is strictly positive. Let `p_min(epsilon)` be the least
possible integer dimension, and `p_bin(epsilon)` the least binary count
among mixed-binary linear relaxations. For `C>0`, define the LP value

```
L_C(epsilon) = min sum_i s_i
  subject to s_i >= 0,
             s_i+s_j >= max{0, log2(1/(C epsilon_ij))}  (ij in E).
```

**Theorem 1 (finite accuracy bounds).**

```
ceil L_20(epsilon) <= p_min(epsilon) <= p_bin(epsilon)
                  <= sum_i ceil s_i <= L_4(epsilon)+n,
```

where `s` is any optimum of the LP defining `L_4`. The upper formulation
uses `O(n+|E|+sum_i degree(i) ceil(s_i))` continuous variables and linear
constraints, and uses the same binary expansion of each variable in every
incident product. Moreover, if

```
tau*(G) = min {sum_i a_i: a_i>=0, a_i+a_j>=1 for ij in E},
```

then `L_4 <= L_20 + tau*(G) log2(5)`. Thus the displayed construction uses
at most `n+tau*(G) log2(5)` more binaries than the integer dimension of any
admissible convex relaxation,
independently of the accuracy vector.

**Corollary 2 (sharp graph invariant).** For fixed nonempty `G`, with a
common accuracy `epsilon` tending to zero,

```
p_min(epsilon) = tau*(G) log2(1/epsilon) + O_G(1),
p_bin(epsilon) = tau*(G) log2(1/epsilon) + O_G(1).
```

The lower bound allows arbitrary continuous convex lifts, unrestricted
integer coordinates, and coupling constraints between different products.
It does not assume that a formulation comes from a coordinate grid.

## Proof of the lower bound

For each parity vector `b in {0,1}^p`, define

```
S_b = {x in [0,1]^V: there are y,z with z mod 2=b and
                    (x,(x_i x_j)_{ij in E},y,z) in C}.
```

These sets cover the unit cube. Take any two points `a,c` in one `S_b`,
with feasible lifts. Convexity of `C` makes their lifted midpoint feasible,
and its integer coordinates are integral because the endpoint integer
vectors have the same parity. Thus the midpoint of the two graph points
belongs to `R`. In component `ij`, its deviation from the graph at
`(a+c)/2` equals

```
(a_i-c_i)(a_j-c_j)/4.
```

Consequently `|(a_i-c_i)(a_j-c_j)| <= 4 epsilon_ij`. This inequality is
continuous in `a,c`, so it also holds on the closure `T_b` of `S_b` in
the unit cube. The sets `T_b` are compact and still cover the cube.
No measurability or closedness assumption on the original lifted set is
needed. This uses the established integer-parity midpoint argument from
mixed-integer convex representability; the precision bound below is its
quantitative geometric application.

We use the following elementary geometric fact. If compact `S subset R^2`
satisfies `|(a_1-b_1)(a_2-b_2)|<=delta` for every `a,b in S`, and its
coordinate widths are `d_1,d_2`, then `d_1 d_2 <= 5 delta`.
If `d_1=0`, this is immediate. Otherwise choose `a,b` attaining the minimum
and maximum first coordinate. Then `|a_2-b_2|<=delta/d_1`. Every `c in S`
is at first-coordinate distance at least `d_1/2` from one of these two
points, so its second coordinate is within `2 delta/d_1` of either `a_2`
or `b_2`. The union of these two intervals has total span at most
`5 delta/d_1`, proving the claim. This is the width part of Lemma 3 in
[the scalar binary-count note](mip-relaxation-binary-lower-bounds.md).

Let `d_i` be the coordinate widths of a nonempty `T_b`. Its two-coordinate
projections satisfy the preceding fact, giving

```
0<=d_i<=1,   d_i d_j<=20 epsilon_ij  (ij in E).
```

If any `d_i=0`, `T_b` has zero `n`-dimensional volume. Otherwise let
`s_i=-log2 d_i`. These values are feasible for the LP defining `L_20`.
Since `T_b` is contained in its coordinate box,

```
volume(T_b) <= product_i d_i = 2^(-sum_i s_i) <= 2^(-L_20).
```

Subadditivity of volume for the at most `2^p` closed parity-support sets gives
`1 <= 2^p 2^(-L_20)`, or `p>=L_20`. Integrality proves the lower bound.
The bound counts integer coordinates, even if their ranges are unbounded.
Restricting the same argument to individual assignments also shows that
at least `2^(L_20)` distinct assignments must occur in any formulation
whose total number of assignments is finite.

## A compact construction attaining the upper bound

Choose an optimum `s` of `L_4`, let `p_i=ceil(s_i)` and `h_i=2^(-p_i)`,
and introduce one shared expansion per vertex:

```
x_i = sum_{k=1}^{p_i} 2^(-k) beta_ik + r_i,
beta_ik in {0,1},   0<=r_i<=h_i.
```

Empty sums are zero. These expansions cover `[0,1]`, including its upper
endpoint. For each edge `ij`, orient it arbitrarily and write

```
w_ij = sum_{k=1}^{p_i} 2^(-k) u_ijk
     + sum_{l=1}^{p_j} 2^(-l) v_ijl + q_ij,
u_ijk = beta_ik x_j,
v_ijl = beta_jl r_i.
```

Each displayed binary-times-continuous equality has an exact four-row
linear description using the known continuous bounds. For example,
`u=beta x`, `0<=x<=U`, is exactly enforced at integral `beta` by
`0<=u<=U beta`, `u<=x`, and `u>=x-U(1-beta)`.
Constrain `q_ij` by the four McCormick inequalities for `r_i r_j` on
`[0,h_i] times [0,h_j]`. At integral binaries all terms except `q_ij`
are exact, so

```
|w_ij-x_i x_j| = |q_ij-r_i r_j| <= h_i h_j/4 <= epsilon_ij.
```

The last inequality follows from `p_i+p_j>=s_i+s_j` and the LP
constraints; when `epsilon_ij>=1/4` it follows from `h_i h_j<=1`.
All graph points have a lift with `q_ij=r_i r_j`. The number of binaries
is exactly `sum_i p_i`, and the formulation-size estimate follows by
counting these four-row product descriptions.

For the accuracy-independent comparison, choose an optimum `t` of `L_20`
and a minimum fractional vertex cover `a`. The vector
`t+log2(5) a` is feasible for `L_4`: each edge right-hand side increases
by at most `log2(5)`. Therefore
`L_4<=L_20+tau*(G) log2(5)`. With a common accuracy smaller than `1/20`,
`L_C=tau*(G) log2(1/(C epsilon))` for `C=4,20`, proving Corollary 2.

### Rational preprocessing

The real LP values in the theorem are exact mathematical benchmarks; their
logarithmic right-hand sides need not be rational. For rational input
tolerances, a polynomial bit algorithm can instead use integer demands

```
d_ij = max{0, ceil(log2(1/(4 epsilon_ij)))}.
```

Compute these demands by exact integer comparisons with powers of two.
Solve the rational LP `min sum s_i`, `s>=0`, `s_i+s_j>=d_ij`, and use
`p_i=ceil s_i` in the same construction. Rounding each demand up increases
it by at most one, so adding a minimum fractional vertex cover to an
optimum of `L_4` is feasible for this rational LP. Its value is at most
`L_4+tau*(G)`. The resulting binary count is at most

```
L_20 + n + tau*(G)(1+log2(5)).
```

Both preprocessing and the explicit formulation have polynomial bit size
in the graph and rational tolerance encoding. In particular, the demands
are bounded by that encoding length, and the dyadic coefficients have
polynomial encoding length. This constructive guarantee has a slightly
larger additive constant than the exact real-LP existence bound.

## Examples and implications

| Interaction graph | `tau*(G)` | Leading binary count |
|---|---:|---:|
| Star with any number of leaves | 1 | `log2(1/epsilon)` |
| Complete bipartite graph `K_(r,s)` | `min(r,s)` | `min(r,s) log2(1/epsilon)` |
| Matching of `m` edges | `m` | `m log2(1/epsilon)` |
| Odd cycle on `2k+1` vertices | `k+1/2` | `(k+1/2) log2(1/epsilon)` |
| Complete graph on `n>=2` vertices | `n/2` | `(n/2) log2(1/epsilon)` |

For bipartite graphs the fractional vertex-cover value equals the minimum
vertex-cover size. Odd cycles illustrate why choosing a set of variables
and discretizing each to full precision can waste a leading fraction of
the binary budget: splitting the required accuracy between both endpoints
can be asymptotically optimal. The lower theorem says arbitrary lifted
formulations cannot improve this leading rate.

In PSE, shared composition variables multiplied by many flow variables
create stars or bipartite graphs. The theorem describes the cost of a
uniform approximation of the unconstrained product block. Additional
physical equations can lower its effective dimension and invalidate an
application of the full-box lower bound. Likewise, a scalar weighted sum
of products can have cancellations; the theorem controls every lifted
product individually and does not assert the same bound for a scalar
objective or an epigraph.

Affine rescaling gives the corresponding statement on any nondegenerate
box: replace each accuracy by `epsilon_ij/((u_i-l_i)(u_j-l_j))` after
removing the affine terms from each product.

## Novelty and verification

The upper construction uses established binary expansion and McCormick
machinery. Fractional vertex cover, its half-integrality, and the parity
midpoint method for integer dimension lower bounds are classical.
The proposed contribution is the universal lower bound and matching
accuracy exponent for a whole interaction graph, together with the
finite LP guarantee for unequal product accuracies. It builds on the
scalar width argument already recorded locally; it is not independent
of that earlier observation.

The [source comparison](../notes/bilinear-graph-binary-complexity-novelty.md)
distinguishes the proposed theorem from known shared discretizations,
vertex-cover variable selection, geometric lower bounds for bilinear
triangulations, and MICP midpoint obstructions. The
[first proof audit](../notes/review-bilinear-graph-binary-complexity.md) and
[second proof audit](../notes/review-bilinear-graph-integer-complexity-second.md)
passed the main theorem and parity extension. The second audit also records
a four-point obstruction to a tempting improvement of the width constant.
The [verification script](../code/mip_relaxation_binaries/check_graph_precision.py)
passed 226 seeded weighted-allocation cases and 306 extrema computed from
explicit projected LP fibers. It checks coverage, simultaneous product
accuracy, sharp local error attainment, and the LP comparison constants.

Primary foundations and closest comparisons include:

- Lubin, Zadik, Vielma, *Mixed-integer convex representability*,
  [arXiv:1706.05135](https://arxiv.org/abs/1706.05135): the parity midpoint
  method is established. Consult the source-audit note for version-specific
  statement numbering.
- Beach, Burlacu, Bärmann, Hager, Hildebrand, *Enhancements of discretization
  approaches for non-convex mixed-integer quadratically constrained quadratic
  programming: Part II*, [arXiv:2302.01164](https://arxiv.org/abs/2302.01164):
  shared binary discretizations and their error formulas are established.
- Bärmann, Burlacu, Hager, Kleinert, *On piecewise linear approximations of
  bilinear terms: structural comparison of univariate and bivariate mixed
  integer programming formulations*,
  [DOI:10.1007/s10898-022-01243-y](https://doi.org/10.1007/s10898-022-01243-y):
  prior chord and triangulation-count bounds.
