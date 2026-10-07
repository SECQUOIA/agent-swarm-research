# Exact support for coupled quadratic blocks

The implemented extension is exact rational support for two-variable quadratic
graphs over affine row domains, and for quadratic stars whose rows each involve
the center and at most one leaf. The star extension joins overlapping pairs in
one support problem. It does not assume their separate hulls compose exactly.

The finite stationary-point argument, low-dimensional quadratic hulls, and
box-star elimination have prior foundations. Anstreicher and Burer's 2010
paper gives exact quadratic graph formulations on triangulated polytopes in
dimension at most three. Del Pia and Khajavirad's September 2026 paper solves
the more general forest **box** quadratic program in quadratic time. Our box
star routine is an attributed specialization. The constrained-star argument
below handles additional center–leaf affine rows; the
[literature audit](../literature/star-overlap.md) distinguishes that extension
from the box theorem. No priority claim is made for the constrained extension.

## 1. Quadratic graphs over a polygon

Let

\[
P=\{(x,y):\ell\le(x,y)\le u,\ A(x,y)^T\le b\}
\]

be bounded with finite rational bounds and rows. Let

\[
\Phi(x,y)=(x,y,x^2,xy,y^2),\qquad H_P=\operatorname{conv}\Phi(P).
\]

Any finite vector of quadratic expressions in two variables is an affine
image of this graph. To obtain a valid linear inequality in that vector, it
suffices to minimize the scalar quadratic given by the chosen normal.

**Proposition 1.** For rational

\[
q(x,y)=c_0+c_1x+c_2y+c_3x^2+c_4xy+c_5y^2,
\]

the minimum over a nonempty rational polygon is attained at one of the
following rational candidates:

1. A polygon vertex.
2. The interior minimum of the restriction to a polygon edge, when that
   restriction has positive quadratic coefficient.
3. The feasible stationary point of a positive-definite quadratic, if the
   polygon has two-dimensional interior.

The code uses coefficient order `(constant, x, y, xx, xy, yy)`.

**Proof.** A boundary minimizer lies on an edge or at a vertex. On an edge
parametrized by `v+t(w-v)`, `0<=t<=1`, the restriction is `a t²+b t+d`.
Its minimum occurs at an endpoint, or at `t=-b/(2a)` when `a>0` and the
stationary point lies inside the edge. These candidates are rational.

An interior minimizer satisfies `gradient q=0`, with positive-semidefinite
Hessian `Q=[[2c_3,c_4],[c_4,2c_5]]`. If `Q` is positive definite, the
unique solution is rational and is the listed candidate. If `Q` is singular,
take a nonzero null vector `v`. Along the line through the minimizer in
direction `v`, both the linear derivative and the quadratic coefficient
vanish. The value is constant until this line reaches the boundary of the
bounded polygon. Thus a boundary minimizer exists. The same edge argument
covers a line segment; a singleton requires only its point. ∎

The implementation enumerates all intersections of independent pairs of
original rows, including the four bounds, keeps feasible intersections, and
constructs their exact convex hull. Every nonempty bounded polyhedron in two
dimensions, including a segment or singleton, has a vertex with two
independent active normals. Thus an empty list certifies emptiness. With `m`
input rows this takes `O((m+4)^3)` rational operations, followed by linear
candidate work in the number of vertices. Bit complexity is polynomial in
the rational input length. The algorithm does not cover unbounded domains.

## 2. A constrained star with arbitrarily many leaves

Use one center variable `y` and leaves `x_1,...,x_k`, all in finite rational
intervals. Each additional rational affine row may involve `y` and at most
one leaf; rows involving only the center or one leaf are allowed. Consider

\[
q(y,x)=q_0(y)+\sum_{i=1}^k
       [a_i x_i^2+(b_i y+d_i)x_i],
\tag{1}
\]

where `q_0` is quadratic. Coefficients may have either sign. There are no
leaf–leaf products. This objective is the general rational linear support
direction for the vector containing all center and leaf coordinates, their
squares, and all center–leaf products. Any supported vector of quadratic
expressions is again an affine image.

**Theorem 2.** The exact minimum of (1) over the constrained star is rational
and can be computed with a finite rational partition of the center interval.
The provided implementation uses `O((k+m+1)^3)` rational operations as a
conservative bound, where `m` is the number of additional rows. For a box
without rows it uses `O((k+1)^2)` operations. The algorithm also certifies
empty feasible sets and handles fixed variables.

**Proof.** Associate with each leaf the polygon in `(y,x_i)` defined by the
center and leaf bounds and its rows. Its projection onto `y` is a closed
rational interval, computable by Proposition 1's vertex construction. The
star is feasible precisely when all these intervals and the center-only rows
have a common point: for such a center, leaves can be selected independently.
Their intersection is a rational interval `I`, possibly a singleton.

For `y in I`, the feasible interval of leaf `i` has the form

\[
L_i(y)\le x_i\le U_i(y),\qquad
L_i=\max_j(\alpha_{ij}+\beta_{ij}y),\quad
U_i=\min_j(\gamma_{ij}+\delta_{ij}y).
\tag{2}
\]

These finite envelopes include the original leaf bounds. All intersections
of their defining lines are rational, and partition `I` into intervals on
which the active lower and upper bounds are affine. Infeasibility cannot
occur inside `I` because each polygon projects onto an interval.

When `a_i>0`, the conditional minimizer is

\[
x_i^*(y)=\operatorname{clip}_{[L_i(y),U_i(y)]}
              \left(-\frac{b_i y+d_i}{2a_i}\right).
\tag{3}
\]

Inside an interval of fixed envelopes, it changes formula only at the
intersection of two affine functions, hence at rational points. When
`a_i<=0`, a minimum occurs at an interval endpoint. The difference between
the two endpoint values factors as

\[
[U_i(y)-L_i(y)]
 [a_i(U_i(y)+L_i(y))+b_i y+d_i].
\tag{4}
\]

The first factor is nonnegative throughout `I`. On each envelope interval,
the second factor is affine. Thus endpoint selection has at most one
additional rational switch there. A zero interval width or an identically
zero difference permits either endpoint.

Collect all envelope intersections and regime switches of all leaves.
On every resulting center interval, one affine choice
`x_i^*(y)=p_i+r_i y` is optimal for each leaf, so substitution into (1) gives
one rational quadratic in `y`. Its minimum is an endpoint or an interior
stationary point with positive quadratic coefficient. Both are rational.
The conditional minimum is continuous; formulas valid in an open interval
remain valid at its endpoints, even when multiple minimizers coexist.
For a singleton `I`, optimize every leaf only at that fixed center. These
cases cover all feasible points and prove the minimum claim.

For complexity, let `s_i` be the number of defining affine bound functions
of leaf `i`, including its two box bounds, and write `S=sum_i s_i`.
Pairwise line intersections give `O(s_i²)` intervals, active-envelope
selection takes `O(s_i)` work on each, and regime switches add only a
constant number per interval. The union has `O(sum_i s_i²)` intervals.
Evaluating all leaves and constructing the quadratic on each costs `O(S)`,
giving `O(S³)` operations including polygon projection. Center-only rows
are processed linearly. With box bounds only, each leaf has at most two
regime switches, the union has `O(k)` pieces, and direct reevaluation of all
leaves costs `O(k²)`. All operations have polynomial rational bit complexity:
breakpoints solve affine equations, and the final candidates solve linear
stationarity equations of quadratics. ∎

The row condition is essential to this proof. An arbitrary row involving two
leaves destroys conditional independence. The implementation rejects it;
it does not discard the row or assume the result remains exact. Integer
restrictions are not enforced by these continuous support oracles, though
their cuts remain valid for integer subsets.

## 3. Sharp improvement from merging fixed pair directions

Suppose a proposed aggregation uses pair polynomials `q_i(y,x_i)` over
center–leaf polygons `P_i`. The assembled domain consists exactly of points
with `(y,x_i) in P_i` for every leaf; any additional center restriction must
be included in these polygons. Assume this domain is nonempty. Write

\[
\beta_i=\min_{(y,x_i)\in P_i}q_i(y,x_i),\qquad
\beta_* = \min_{(y,x)\text{ in the star}}\sum_iq_i(y,x_i),\qquad
\Delta=\beta_*-\sum_i\beta_i.
\tag{5}
\]

**Corollary 3.** `Delta>=0` is the largest uniform improvement of the constant
in the sum of these fixed pair inequalities. It is computable exactly by
Propositions 1 and Theorem 2. It is positive if and only if the center
coordinates of the individual minimizing sets have no common point.

**Proof.** Every pair term is at least `beta_i`. Equality in their sum occurs
exactly when every pair term attains its minimum at the same center. The
polygons are compact and the objectives continuous, so all minima are
attained. If their projected minimizing sets have a common center, select
its leaf minimizers independently; the assembled feasible point attains
`sum beta_i`. Otherwise no assembled point can attain that sum; compactness
makes the minimum strictly larger. The value `beta_*` is attained, so no
larger constant is valid in the same summed direction. ∎

This is an exact diagnostic for a **specified** aggregation of normals. It
does not predict the benefit of every other direction or prove that the
extra work improves solver runtime. Selecting arbitrary normal vectors is
still a separate algorithmic task.

Two concrete strictness witnesses are useful for interpreting the extension:

- **A coupling row adds strength beyond the entire unconstrained block
  hull.** On `x,y>=0, x+y<=1`, the inequality
  `x²+2xy+y²<=x+y` is valid. Half mass at `(0,0)` and half at `(1,1)` is a
  valid point of the full quadratic graph hull over the unit box, and its
  means satisfy `x+y<=1`, but its lifted moments violate the inequality by
  one. Thus convexifying the row domain beats even the exact joint box hull
  intersected with the row. It also gives `xy<=1/4`, whereas the full box
  hull intersected with the row permits `xy=1/2`.
- **Merged pairs can add strength when shared first and second moments
  agree.** The [overlap note](overlap-review.md) proves that
  `D=(y-1/4-x/2)²+(y-5z/8)²+x(1-x)+z(1-z)` has minimum `1/128` on the unit
  cube, whereas the intersection of the two exact pair graph hulls admits
  value zero. These are full pair hulls, so this is stronger than a comparison
  with scalar McCormick or separate-square relaxations. The star routine
  returns `1/128` and `(y,x,z)=(11/16,1,1)` exactly. In (5), the two displayed
  nonnegative pair terms each have minimum zero and `Delta=1/128`.

The second witness does not prove dominance over dense SDP/RLT relaxations.
Its two pair covariances saturate the PSD Cauchy inequalities. A common PSD
completion therefore forces `Cov(x,z)=1/5`, hence `E[xz]=3/5`, which violates
the nonedge McCormick bound `E[xz]<=E[x]=1/2`. Thus a dense relaxation with
the additional `xz` product also excludes the point. The star support cut
provides the strengthening in the existing sparse coordinates.

The overlap note also gives a reduced version using only the shared square
`y²`, a constrained obstruction surviving separate block interval
propagation, and a positive tree-gluing theorem when full separator measures
agree. Matching finitely many shared moments alone is insufficient.

## 4. Implementation and proof boundary

[quadratic_polygon.py](quadratic_polygon.py) exports:

```
support_quadratic(bounds, rows, coefficients)
replay_quadratic(bounds, rows, coefficients, certificate)
```

Bounds are two `(lower,upper)` pairs, rows are `(a_x,a_y,rhs)`, and
coefficients are `(constant,x,y,xx,xy,yy)`. Equality rows are supplied in both
directions. Certificates include the original inputs, polygon vertices, all
minimizing candidates, and the attained rational bound.

[quadratic_star.py](quadratic_star.py) exports:

```
support_star(bounds, rows, coefficients, center=0)
replay_star(bounds, rows, coefficients, center, certificate)
```

Here rows are `(coefficient_vector,rhs)` and coefficients map exponent tuples
to rational values. Certificates include the original inputs and center
index, the complete center partition, affine leaf minimizers, interval
quadratics, and the attained rational bound.

All coefficients are converted to `fractions.Fraction`. A finite float means
its exact binary rational value; a decimal string means that exact decimal
value. NaN, infinities, invalid degrees and unsupported coupling are rejected.
The row and polynomial inputs supplied to replay must come from the trusted
original model. Replaying checks a complete canonical reconstruction and
rejects changed inputs, missing intervals, or changed constants. The producer
and checker share exact geometric code; this is not a formally verified or
independently implemented checker. The surrounding solver must also bind
the emitted floating-point row to its exact coefficients and bound.

Binding concerns normalized mathematical inputs: equivalent representations
such as `"1/2"` and `Fraction(1,2)` have the same rational value, and zero
polynomial terms do not alter the problem. It is not a claim to preserve a
model file's lexical spelling. Original model-variable and expression
identities must additionally be bound by the surrounding integration.

Exact support for a selected rational normal certifies its inequality.
It does **not** establish completeness of the bounded-budget floating-point
normal search, nor certify the nonlinear solver's final global bound.

## 5. Targeted verification

Executed from the repository root:

```
python -m pytest -q research-20261002-convexification/theory/test_quadratic_polygon.py research-20261002-convexification/theory/test_quadratic_star.py
python -m compileall -q research-20261002-convexification/theory/quadratic_polygon.py research-20261002-convexification/theory/quadratic_star.py
```

Result: **30 tests passed**. The tests include 120 independently formulated
one-leaf star versus polygon comparisons, 40 nonconvex stars compared with
exhaustive leaf endpoint enumeration, 30 constructed convex stars with known
exact minimizers, rational degeneracy and empty-domain cases, the strict
pair-hull obstruction, and certificate/input tampering. These are targeted
local checks; the compilation check also passed. No project-wide checks or
CI results are asserted.

An [independent audit](star-audit.md) additionally compares constrained-star
support with exact full-space KKT face enumeration; its saved script and
outputs distinguish those checks from the producer's test suite.
The executed command was
`python research-20261002-convexification/theory/check_star_audit.py`.
It passed 155 random cases (76 feasible and 79 empty), checked 298 returned
pieces, confirmed a separate four-variable mixed-curvature example with
seven pieces, and rejected seven certificate or input mutations. The saved
[output](star-audit-results.txt) records the counts and exact example values.
