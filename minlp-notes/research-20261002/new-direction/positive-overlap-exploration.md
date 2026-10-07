# Positive overlap removes dyadic copy drift, but not affine shell error

Date: 2026-10-02. Status: a proved geometric improvement, a remaining
counterexample for isotropic affine models, and a scoped anisotropic
estimate. This note concerns continuous optimization on a product box.
It does not prove the requested occurrence-free FPT theorem. No external
search or knowledge-base material was used.

The starting definitions are the configuration DP and shell partition in
the [original certificate note](../../research-20260929/theory-decomposition/decomposition-certificates.md),
the [regridded contraction proof](../regridded-certificates/note.md), and
its [rational QP specialization](../geometric-dp/regridded-qp-bit.md).
The earlier [drifting fan example](weighted-drift-exploration.md) explains
why both kinds of touching incidence must be removed.

## 1. What the overlap change proves

At a fixed stage, use the same center `c`, base width `h`, and dyadic
grading ratio `theta` for every bag and separator. Retain a bag/separator
incidence only when their projections have positive overlap in every
separator coordinate. Apply this test in both places:

- the local pair consisting of a bag leaf and its own separator cell;
- the pair consisting of a parent bag leaf and a child separator cell.

Keep the boxes and the local optimization domains closed. The strict
test determines which pairs are eligible; it does not remove endpoints
from an eligible intersection. Empty separators pass the test
vacuously. Substitute fixed coordinates out before applying it.

**Geometric conclusion.** In every configuration of this modified DP,
all selected intervals for a coordinate `i`, including both bag and
separator intervals, lie inside one selected interval `J_i`. If
`w_i=width(J_i)`, then

```
max_t z_i^t - min_t z_i^t <= w_i
                         = max width of a selected interval for i.    (1)
```

In particular, for the usual consistent reconstruction
`x_i=z_i^{top(i)}`, every copy satisfies `|z_i^t-x_i|<=w_i`.
There is no occurrence or path-length factor in this coordinatewise
bound. The interval `J_i` need not belong to the top bag and need not
contain `c_i`. Different coordinates can have maximal intervals from
different selected boxes.

### Why the scalar intervals are laminar

Before clipping, every scalar shell interval has the form

```
[c_i + m 2^r h, c_i + (m+1) 2^r h]
```

for integers `m,r`. The central intervals have length `h`; shell lengths
are `theta 2^(j-1)h`, also powers of two times `h`. The shell-grid anchor
differs from `c_i` by an integral multiple of its grid spacing. Thus all
occurrences of coordinate `i` use one nested dyadic hierarchy.

Two intervals from that hierarchy with positive-length overlap are
nested. Intersecting every interval with the same coordinate domain
`[l_i,u_i]` preserves nesting. It can create equal clipped intervals,
which are treated as the same set. It cannot create positive overlap
between originally disjoint interiors. Therefore the retained,
nondegenerate clipped intervals form a laminar family under
positive-length overlap.

Having dyadic rational endpoints alone is insufficient. For example,
`[0,1/2]` and `[1/4,3/4]` overlap positively without being nested.
Common alignment at every scale is the property used here.

### Connected laminar families have one maximal member

Take any finite family of intervals whose positive-overlap graph is
connected and whose positively overlapping members are nested. Choose
a member `J` of maximum length. Every neighbor of `J` is contained in
`J`. Suppose a path from `J` first reaches an interval `K` not contained
in `J`, after an interval `L` contained in `J`. Positive overlap makes
`K` and `L` nested. Since `L` lies in both `K` and `J` and has positive
length, `K` and `J` positively overlap as well. They must be nested;
`K` not contained in `J` would strictly contain it, contrary to maximal
length. Thus every member lies in `J`. The union is exactly `J`, proving
that its diameter is the maximum selected width.

For a coordinate `i`, take one vertex for each selected bag interval
and one for each selected separator interval containing `i`. On each
edge of its occurrence subtree, the selected separator interval has
positive overlap with both endpoint bag intervals by the two eligibility
rules. This expanded graph is connected by running intersection. The
preceding argument proves (1).

Omitting only one class of touching pairs does not give this proof: the
other edge of the bag--separator--bag connection can still be a
boundary-only contact.

## 2. The modified lower bound is globally sound and attained

For a parent bag leaf `B`, let `E(u,B)` be the child separator cells with
positive overlap with `B_{S_u}`. For a cell `D` of the current separator,
let `E(t,D)` be the bag leaves with positive overlap with `D`. Define

```
psi_(u,B)(s) = lambda_u^T s + min_(D' in E(u,B)) beta_(u,D'),

beta_(t,D) = min_(B in E(t,D))
            min_(z in B, z_St in D)
            [ell_(t,B)(z) + sum_u psi_(u,B)(z_Su)
                           - lambda_t^T z_St].                       (2)
```

The root minimizes the analogous expression over all root leaves.
Every eligible local intersection is nonempty and compact. Finite
nondegenerate box partitions ensure that all the required eligibility
lists are nonempty. With continuous affine models, all minima in (2)
are attained, and exact minimizers can be chosen at corners of the closed
intersection, including corners on its boundary. The usual storing of
minimizing choices and backtracking therefore gives an attained
configuration minimum. Replacing both incidence lists in the unfolding
proof gives exactly

```
LB = min_config Phi,
Phi = sum_t ell_(t,B_t)(z^t)
      + sum_(t != root) lambda_t^T(z^parent(t)_St-z^t_St).              (3)
```

Here a configuration must pass both positive-overlap tests and still
has `z^t in B_t`, `z^t_St in D_t`. Its actual points may be endpoints.

**Completeness at boundaries.** Every point `x` of the original product
box has a consistent configuration in (3). To see this, choose points
`x^(m)` from the interior of the product box converging to `x` and
avoiding every bag and separator boundary. There are finitely many
such boundaries, each a coordinate hyperplane. Select the unique
interior bag leaf and separator cell containing each projection of
`x^(m)`. Every relevant pair has positive overlap, because a common
point lies in both interiors. Along a subsequence all selected boxes
are the same, since there are finitely many choices. Their closures
contain the corresponding projections of `x`. Use these boxes with
`z^t=x_{V_t}`. They remain eligible, and their slope terms cancel.
Since each local model is valid on its entire closed box,

```
LB <= Phi <= F(x),             hence LB <= min_X F.                  (4)
```

This also gives a direct explanation using half-open cells: assign a
boundary point to the cell reached by a common sufficiently small
coordinatewise inward perturbation, then use that cell's closure for
optimization. At a domain upper endpoint the perturbation points
inward. A coordinatewise half-open convention is valid only when it
produces these consistent owners across all partitions. The
subsequence argument avoids imposing an implementation convention.

One can instead prove (4) first for generic interior points and extend
it by continuity of `F`. The closed-configuration construction is
stronger: it explicitly provides a consistent feasible configuration
at a boundary minimizer.

This is a modified certificate contract. Its intercepts need not satisfy
the old inequalities for omitted touching pairs, and its root value can
exceed the old all-touching configuration minimum. Equation (4), rather
than equality with the old minimum, is the required soundness statement.

It would be incorrect to optimize on genuinely half-open intersections
while claiming an attaining corner oracle. An affine objective can have
an unattained infimum there. Closed intersections plus strict pair
eligibility preserve both the geometric lemma and attainment.

The proof uses the unrestricted product box. With an additional equality
or another feasible set confined to cell boundaries, the generic inward
perturbations may be infeasible. A constrained extension would need a
separate soundness and feasibility argument.

## 3. Isotropic affine shells still have an occurrence obstruction

The copy-range improvement does not control the total affine relaxation
error. The following example has no disagreement between copies at all.

Choose `n=4^r`, `beta=1/4`, `a=beta/sqrt(n)`, and

```
X = [0,1] x [-1,1]^n,
F(u,v) = u^2/2 + sum_i v_i^2/2 + a u sum_i v_i.                       (5)
```

All data are rational. The Hessian has eigenvalues `1-beta`, `1+beta`,
and `1` on the remaining subspace, so

```
||H||_2=5/4,       F(u,v)>=3||(u,v)||_2^2/8.                          (6)
```

The unique optimizer is zero. Use the star-shaped decomposition with
bags `{u,v_i}`; make bag 1 the root, assign `u^2/2` only to that bag,
and assign `v_i^2/2+a u v_i` to bag `i`. Each Hessian coefficient is
assigned exactly once. All slopes prescribed at center `c=0` vanish.

Take a dyadic `theta<=1/2`, `R=1/2`, and `w=theta R`. At any sufficiently
fine stage with `R` a shell radius, select

```
B_i = [R,R+w] x [0,w],      D_i=[R,R+w]  (i>1),
z^i=(R,0).                                                        (7)
```

These are genuine bag and separator cells in the shell from radius `R`
to `2R`, with positive widths after domain clipping. The `u` coordinate
puts each bag cell outside the inner shell cube. Every own and parent
incidence overlaps over the whole separator interval. Every hub copy
is exactly `R`; the reconstructed point is `(R,0,...,0)`.

Use the existing affine midpoint model, with `p=2` and the valid common
bag Hessian bound `M=5/4`:

```
ell_i(z) = a_i(m_i)+grad a_i(m_i)^T(z-m_i)-M p w^2/8.                 (8)
```

For a nonroot bag, the midpoint displacement at (7) is
`(-w/2,-w/2)`. Exact quadratic Taylor expansion gives

```
ell_i(R,0) = -w^2/8-a w^2/4-M w^2/4 <= -3w^2/8.
```

For the root it gives

```
ell_1(R,0) = R^2/2-w^2/4-a w^2/4-M w^2/4
           <= R^2/2-w^2/2.
```

Thus this legal, zero-drift configuration proves

```
LB <= Phi <= R^2/2-3n w^2/8
          = R^2(1/2-3n theta^2/8).                                 (9)
```

For fixed `theta`, this is negative when `n theta^2>4/3`, at every
finer base mesh for which the same radius-`R` shell occurs. For example,
`n theta^2>=4` gives `LB<=-1/4` with `R=1/2`, even though the incumbent
at center zero already has optimal value zero.

The issue persists if the scalar `M p w^2/8` correction is replaced
by the sharper entrywise anisotropic correction
`w_Vi^T |H_i| w_Vi/8`, while keeping these isotropic cells. The nonroot
model then has value `-(1+2a)w^2/4`, and the same argument gives
`LB<=R^2/2-nw^2/4`. Tightening that constant does not solve the problem.

This is a counterexample to a uniform vanishing fixed-center gap for
these isotropic affine models. It is not a hardness result, a failure
of lower-bound soundness, or a proof that the actual moving-center
iteration never terminates. It also does not cover models that retain
useful convex quadratic terms exactly. The star QP itself is easy.

## 4. What coordinatewise grading does repair

There is an occurrence-free aggregate estimate if every selected
scalar interval, in bags and separators, obeys

```
width(I_i) <= h + theta dist(I_i,c_i).                               (10)
```

Assume the common dyadic hierarchy and both positive-overlap rules.
Let `w_i` be the maximal selected width from Section 1. Since the
maximal interval contains the reconstructed `x_i`, (10) implies

```
w_i <= h + theta |x_i-c_i|,
||w||_2 <= sqrt(n)h + theta ||x-c||_2.                              (11)
```

Allocate every entry of the global symmetric Hessian `H` to exactly
one bag, obtaining local `H_t`. An off-diagonal symmetric pair is
allocated together. Allocate affine coefficients once as well. This
allocation is important: arbitrary cancelling bag quadratics are not
covered by the estimate below.

For a bag with side-width vector `b_t`, use

```
ell_(t,B)(z) = a_t(m_B)+grad a_t(m_B)^T(z-m_B)
              -b_t^T |H_t| b_t/8,                                 (12)
```

where the absolute value is entrywise. Exact Taylor expansion shows

```
0 <= a_t(z)-ell_(t,B)(z) <= b_t^T |H_t| b_t/4.
```

Put `d_t=z^t-x_Vt` and `r=|x-c|` coordinatewise. The geometry gives
`|d_t|<=w_Vt`, and every side of `B_t` is at most the corresponding
entry of `w`. Use subtree-gradient slopes at the current center,
`lambda_(t,i)(c)=sum_(s in sub(t), i in V_s) partial_i a_s(c_Vs)`.
With these slopes, the telescoping identity at `c` is still exact:

```
Phi = F(x)+sum_t [d_t^T H_t (x-c)_Vt + d_t^T H_t d_t/2]
             -sum_t err_t.
```

Canonical allocation and entrywise nonnegativity therefore give

```
sum_t err_t <= w^T |H| w/4,
sum_t |d_t^T H_t (x-c)_Vt| <= w^T |H| r,
sum_t |d_t^T H_t d_t|/2 <= w^T |H| w/2.
```

Consequently, with `K=|| |H| ||_2` and `R=||x-c||_2`,

```
F(x)-Phi <= K [R ||w||_2 + 3||w||_2^2/4].                         (13)
```

No occurrence count enters. If the interaction graph has treewidth at
most `p-1`, then

```
K <= (1+2 sqrt(p-1)) ||H||_2.                                     (14)
```

For completeness, orient the off-diagonal graph with outdegree at most
`p-1`, and write `H=diag(H)+B+B^T`. Rowwise Cauchy--Schwarz gives
`|| |B| ||_2 <= sqrt(p-1)||H||_2`, because each column's sum of squared
assigned entries is at most that of the corresponding column of `H`.
The triangle inequality proves (14).

Equations (11)--(13) recover the needed contraction inequality. For
example, take `eta=g/20`, `theta<=min(1/2,eta/(4K))`, and `K>0`. Then
Young's inequality yields

```
F(x)-Phi <= eta ||x-c||_2^2 + C n h^2,
C = 3K/4 + 49K^2/(32 eta).                                       (15)
```

Indeed, substituting (11) into (13) bounds the mixed term by
`(7K/4)sqrt(n)h R` and the quadratic coefficient by
`(11K theta/8)R^2`; half of the `eta R^2` allowance handles the mixed
term, and the displayed restriction on `theta` handles the latter.
The existing quadratic-growth recurrence now applies, with constants
depending on `p` and `||H||/g`, and with `n h^2` as the mesh term.
If `K=0`, the objective is affine and can be solved directly.

This proves the aggregate error estimate. It does not yet give the
required FPT partition count.

## 5. A counting barrier for this anisotropic repair

A direct implementation of (10) takes a one-dimensional graded grid
for each coordinate and their Cartesian products inside each bag.
Its per-bag count is `O((theta^-1 log(1/h))^p)` after normalizing the
domain size. The power of the accuracy-bit count depends on `p`.

This is unavoidable for any explicit rectangular cover that imposes
(10) separately on every coordinate. Consider `X=[0,1]^p`, center
zero, and a box `B=product_i[a_i,b_i]`. If
`b_i-a_i<=h+theta a_i`, then

```
integral_(a_i)^(b_i) dx/(h+theta x)
    <= (b_i-a_i)/(h+theta a_i) <= 1.
```

The weighted volume of `B` under the product density
`product_i(h+theta x_i)^(-1)` is at most one. The weighted volume of
the whole domain is

```
[theta^-1 log(1+theta/h)]^p.
```

Every cover therefore needs at least that many boxes. This argument
does not even need disjoint interiors. At `h=2^-j` with fixed positive
`theta`, it gives `Omega(j^p)` boxes. An explicit cover of this kind
cannot have a bound `f(p,theta^-1) poly(j)` with an absolute polynomial
exponent.

Thus positive overlap supplies the missing occurrence-free scalar
geometry, and coordinatewise grading supplies a compatible aggregate
QP error bound. Combining those two steps by an explicit coordinatewise
graded rectangular cover loses the sought FPT dependence on input and
accuracy bits. A general result needs another ingredient, such as a
stronger local model or a representation that does not enumerate this
cover. No such ingredient is established here.

## Verification

A delegated independent geometry audit checked the laminar-family
argument, boundary completeness, and the distinction between pair
eligibility and closed optimization domains. It also checked the star
counterexample and the rectangular-cover counting argument. A final
focused pass found no flaw in the global soundness proof, the three
entrywise aggregate estimates, the spectral bound (14), or the constants
in (15). The exact checks actually run used `python3 - <<'PY'` with
`fractions.Fraction`. They verified:

- 80 clipped dyadic intervals and all 696 positive-overlap ordered pairs;
- 4,478 connected components from 1,000 sampled interval families,
  each contained in a maximum-width member;
- 120 exact star shell cases, including 60 negative cases satisfying
  the threshold in (9), and the entrywise-correction variant.

A separate targeted inline Python check verified all four local Markdown
links and balanced code fences in this note.

The checks support the displayed finite constructions; the proofs give
the general claims. No complete DP implementation, project-wide
verification, CI inspection, external search, or knowledge-base access
was performed for this note.
