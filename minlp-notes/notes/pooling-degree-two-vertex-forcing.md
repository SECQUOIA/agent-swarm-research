# A degree-two pooling network with exponentially many isolated global optima

Date: 2026-09-05. Status: two independent physical-model audits passed;
written reviews and test records appear below. This is a geometric
obstruction, not a complexity classification.

The telescoping Klee–Minty certificate can be realized by an actual
one-pool network with two feeds, two pool outlets, and input/output degrees
at most two. Every vertex of its blending-path component extends to a
global optimizer, and these are all its optimizers. The separate weighted
slab needed for the subset-sum reduction is not realized here. Thus the
degree-two pooling complexity question remains open.

## 1. The physical path

Fix `n>=2`, `epsilon=1/4`, and `s_j=4^(j-n)`. Use the
[reviewed physical blending path](pooling-degree-two-bypass-investigation.md):
input `j` has quality `C_j=n-j`, exact supply `s_j`, and only two arcs,
to outputs `j-1` and `j`. Write their flows as `s_j-t_j` and `t_j`.
Each arc has upper capacity `s_j`. Output 0 has upper capacity `s_1`
and redundant upper quality `C_1`. For `j=2,...,n`, output `j-1`
has upper capacity `s_j` and upper quality `(C_(j-1)+C_j)/2`.
Consequently its constraints are

```
t_(j-1) <= t_j <= s_j-t_(j-1).
```

The normalized coordinates `x_j=t_j/s_j` therefore form the
Klee–Minty polytope. In particular, `t_n=x_n`; denote this value by `t`.
The former terminal output `n` is modified as follows.

## 2. A two-feed pool attached to the endpoint

Add a pool `P`, inputs `A,B,Z`, and outputs `W,V`.
The only new arcs are

```
A -> n,  A -> P,
B -> P,  B -> W,
P -> W,  P -> V,
Z -> V.
```

Inputs `A` and `B` have qualities 1 and 2 and exact supplies 1.
Input `Z` has quality 0 and upper supply 1. Every new arc has upper
capacity 1. Pool `P` has exact throughput 1. Output `n` has exact
demand 1 and upper quality 1; this replaces its old quality bound 0.
Output `W` has exact demand 1 and upper quality 2. Output `V` has
upper capacity 2 and upper quality 1. There are no other lower bounds
besides the explicitly stated exact supplies, demands and pool throughput.

The endpoint demand and source `A` conservation force its bypass flow
to be `1-t` and its pool intake to be `t`. Pool throughput then forces
the intake from `B` to be `1-t`. Source `B` conservation makes its
bypass flow `t`; output `W` demand consequently forces pool waste
flow `1-t`. The remaining pool outlet to `V` is exactly `t`.

The pool always has positive throughput and quality `q=2-t`. Write
`z` for the clean input flow from `Z`. The only nonredundant new quality
condition, at output `V`, is

```
(2-t)t <= t+z,   equivalently z >= t-t^2.
```

All other new quality rows are redundant. Since `0<=t-t^2<=1/4`,
every path point extends to a feasible full network, and its least
feasible clean flow is `z=t-t^2`. Every input and output has total
degree at most two; the pool has exactly two intakes and two outlets.
The bypass graph remains a collection of paths. The underlying full
undirected network is connected and has exactly one cycle.

## 3. Ordinary nonnegative production costs and output revenues

Give path input `j` production cost `s_j`. Give `A` and `B` cost 1
and clean input `Z` cost 2. Give path output `j`, for `j=0,...,n-1`,
unit revenue `s_(j+1)`, and give outputs `n,W,V` unit revenue 1.
These are nonnegative costs at most 2 and revenues at most 1.

To verify the economics, subtract 1 from every input unit cost and every
output unit revenue. Global mass conservation makes this change cancel
exactly. All new outputs and inputs `A,B` then have zero price, while
`Z` costs 1. On the path, put `R_j=s_(j+1)-1` for `j<n` and
`R_n=0`. The cost at input `j` is `R_(j-1)=s_j-1`.
Its revenue minus cost is

```
R_(j-1)(s_j-t_j) + R_j t_j - R_(j-1)s_j
 = (R_j-R_(j-1))t_j.
```

Here the terminal output's additional inflow causes no extra term,
because `R_n=0`. For `j<n` the coefficient is `3s_j`; for `j=n`
it is zero. Total original profit is therefore exactly

```
sum_(j<n) 3s_j t_j-z
 = sum_(j<n) c_j x_j-z,
c_j=3s_j^2=(1-epsilon)epsilon^(2(n-j)-1).
```

## 4. Exact global optimizers

The [reviewed telescoping identity](klee-minty-rank-one-slab-hardness.md)
states

```
F(x)=x_n-sum_(j<n)c_j x_j-x_n^2 >= 0
```

throughout the path polytope, with equality exactly at its `2^n`
vertices. Hence every feasible full-network profit satisfies

```
profit <= sum_(j<n)c_j x_j-(t-t^2) = -F(x) <= 0.
```

Every path vertex achieves zero profit by taking `z=t-t^2`. Conversely,
zero profit forces both `F=0` and that unique value of `z`. All other
new flows and the pool quality were uniquely determined by `t`.
The full network therefore has exactly `2^n` global optimizers in physical
arc flows and the active pool quality, all isolated. Redundant variables
introduced by alternative formulations are not counted. The projection
of its set of global optimizers onto the path
coordinates is precisely the Klee–Minty vertex set.

All quality values and upper specifications may be divided by
`max(n-1,2)` to lie in `[0,1]`, without changing the feasible flows.
All flow upper capacities are at most 2, and all rational data have
polynomial bit length. Exact flow contracts are part of this statement;
their removal is not claimed here.

The certificate also has a simple expression directly in physical flows:

```
t_n-t_n^2-sum_(j<n)(s_(j+1)-s_j)t_j
 = sum_(j=1)^n (t_j-t_(j-1))(s_j-t_(j-1)-t_j),  t_0=0.
```

Expanding each product cancels consecutive square terms. Thus the same
construction works for any rational supplies satisfying `s_n=1`, `s_1>0`
and `s_(j+1)>2s_j`, with the same input costs `s_j` and output revenues
`s_(j+1)`. Every local endpoint interval then has positive length, and
the lower and upper endpoint ranges are disjoint, so there are again
`2^n` distinct endpoint patterns and terminal values. In these physical
coordinates the lower affine hull function is
`sum_(j<n)(s_(j+1)-s_j)t_j`. The geometric sequence is a convenient
explicit polynomially encoded instance, not an essential algebraic choice.
Both reviewers independently approved this extension in written addenda.

### 4.1 Distinct strict local optima after a small price perturbation

The exponential multiplicity need not consist of tied global optima.
For the geometric supplies, increase the revenue of output `V` and
the unit cost of clean input `Z` by `delta=4^(-n)`. Their net added
profit is `delta[(t+z)-z]=delta*t`. Thus, after choosing the least
clean flow, the perturbed objective on the path is

```
H(x)=-F(x)+delta*x_n.
```

At the vertex with terminal value `t`, its value is `delta*t`.
These values are distinct. Consider any edge from that vertex to a
neighboring vertex with terminal value `t'`. Along the segment with
parameter `a in [0,1]`, the telescoping identity gives

```
F((1-a)x+a x')=a(1-a)(t'-t)^2.
```

The outward directional derivative of `H` is therefore
`-(t'-t)^2+delta*(t'-t)`. It is strictly negative. Indeed every
terminal value has denominator dividing `4^(n-1)`, so every nonzero
difference has absolute value at least `4^(-(n-1))>delta`.
The tangent cone of a polytope at a vertex is generated by its incident
edge rays; strict negativity on these finitely many rays implies that
the vertex is a strict local maximizer. In the physical set, extra
clean flow strictly decreases profit, so the same strict local property
holds in physical arc flows and the active pool quality.

The network now has at least `2^n` strict local optima with distinct
values, of which exactly one is globally optimal: every feasible profit
is at most `delta*t<=delta`, and equality requires the unique path
vertex with `t=1` and least clean flow. The other `2^n-1` constructed
local optima are suboptimal. The construction does not assert that
there are no additional local optima.

The perturbation has polynomial binary length, and all prices remain
nonnegative and at most 3. Its magnitude decreases with dimension.
No fixed perturbation tolerance, attraction-basin bound or local-solver
runtime lower bound follows. Both independent reviewers approved this
subsection in written addenda.

## 5. Integer dimension of an exact convex lift of the optimal set

For the original unperturbed economics, let `S` be the set of optimal
physical flows, optionally retaining the
active pool quality. For distinct optimizers whose path coordinates are
`x,x'`, the endpoint values `t,t'` are distinct and

```
F((x+x')/2) = (t-t')^2/4 > 0.
```

Thus their midpoint is not in `S`. This pairwise midpoint exclusion,
rather than isolatedness alone, gives an exact integer-dimension bound.
Suppose `S` is the projection onto its physical coordinates of a convex
set with arbitrary continuous auxiliaries and `k` integer coordinates.
Choose one lift of each of its `2^n` points. If `k<n`, two integer
lifts have the same parity. Their midpoint remains in the convex set
and has integer values in those coordinates, so its physical midpoint would
belong to `S`, a contradiction. Therefore `k>=n`, even if the integer
variables are unbounded and the convex lift is not polyhedral.

The bound is attained as an integer-dimension statement: associate every
optimizer `s(u)` with its endpoint pattern `u in {0,1}^n` and take the
convex hull of the finitely many points `(s(u),u)`. Requiring the last
`n` coordinates to be integer selects precisely those original points.
This upper construction may have exponentially many vertices and makes
no polynomial formulation-size claim. Consequently the minimum number
of integer coordinates in an exact convex lift of this optimal set is
exactly `n`.

This is an application of the established midpoint/parity argument of
[Lubin, Vielma and Zadik](https://arxiv.org/abs/1706.05135), not a new
general representability principle. It applies to the complete optimal
set. Representing just the optimal value or one chosen optimizer is a
different requirement. Both reviewers independently approved the
corollary in written addenda.

## 6. An explicit convex hull and polynomial linear optimization

There is a useful contrast to the optimal-set representation bound.
Every linear objective over the full physical feasible set is solvable
by a polynomial-size linear program. In normalized path coordinates,
the full feasible set is affinely equivalent to

```
T = { (x,z) : x in P_epsilon, x_n-x_n^2 <= z <= 1 }.
```

Every other arc flow and the active pool quality is affine in `(x,z)`.
Put `c^T x=sum_(j<n)c_j x_j`. Its exact convex hull is

```
conv(T) = { (x,z) : x in P_epsilon, c^T x <= z <= 1 }.       (2)
```

The telescoping identity proves `x_n-x_n^2>=c^T x`, so the right
side contains `T`. Conversely, decompose any `x` into path vertices
`x=sum_u lambda_u v(u)`. At those vertices,
`v_n(u)-v_n(u)^2=c^T v(u)`. Thus `(x,c^T x)` is a convex combination
of points of `T`. The point `(x,1)` itself belongs to `T`. Every
intermediate `(x,z)` in (2) is on the segment between these two points,
which proves the reverse inclusion.

Moreover, every vertex of (2) is physically feasible. A vertex must
have `z=c^T x` or `z=1`; an interior `z` permits a vertical
perturbation. On either boundary, a nonvertex `x` permits a convex
decomposition along that affine boundary. Hence `x` must be a path
vertex, where both boundary choices are feasible for `T`. The two
boundaries never meet, since `c^T x<=1/4` on the path polytope.
Solving the LP and returning an optimal basic feasible solution
therefore supplies an exact physical optimizer for any linear cost.
Both the formulation size and its rational encoding length are
polynomial. A point in the optimal LP face chosen without a vertex
requirement need not be physically feasible.

This also explains a failed hardness route. A concave quadratic
`a^T x-b x_n^2`, with `b>=0`, over the bare path polytope has the same
minimum as the linear objective `a^T x-b L(x)`: a concave objective
attains its minimum at a vertex, and `x_n^2=L(x)` at every vertex.
The dense slab creates new vertices and destroys this linearization.
Thus the slab cannot be omitted from the abstract hardness proof.

The exact convex hull supports optimization; it is not an exact
representation of the original nonconvex feasible set or its finite
optimal set. The integer-dimension statement in Section 5 concerns
those exact sets, not their convex hull. Both independent reviewers
approved this convex-hull corollary in written addenda.

## 7. Verification and unresolved questions

- [First physical audit](review-pooling-degree-two-vertex-forcing.md)
  verifies conservation, quality, standard economics, exact optimizer
  count, and graph restrictions.
- [Second physical audit](review-pooling-degree-two-vertex-forcing-second.md)
  independently verified the same proof and ran
  252 original-network vertex slices with fixed pool quality and 18
  interior terminal slices.
- [Author checker](../code/pooling_bypass_paths/check_vertex_forcing.py)
  passed 65 original-network optimization runs: free global problems,
  all terminal vertex slices through dimension five, and an interior
  negative control. The solver receives only original node, arc, pool,
  quality and economic constraints.
  Its exact rational extension also checked 18,432 outward edge slopes
  for the price perturbation through dimension ten.

The exact pool-throughput contract cannot simply be deleted. A concrete
negative control takes `x_1=...=x_(n-2)=0`, `x_(n-1)=1`, `x_n=1/4`,
uses pool intake `1/4` solely from `A`, routes all of `B` directly to
`W`, and sets clean flow and pool waste flow to zero. Every other
contract and capacity remains satisfied, the pool quality is 1, and
profit is `c_(n-1)=3/16>0`. Thus retaining only the pool upper capacity
changes the claimed optimum. Standard production costs and output
revenues also cannot directly distinguish different amounts of internal
flow around `B-P-W` when all external throughputs are fixed.

This physical construction realizes the nonlinear vertex certificate
without a dense nonphysical constraint or arc-specific profit. It does
not realize the additional aggregate slab used in the subset-sum
reduction. Maximizing a linear function over the selected path vertices
alone is still a linear program over their convex hull. Exponentially
many isolated optimizers therefore do not imply NP-hardness.

The remaining task is to impose the aggregate using conservation or
quality identities while preserving degree two, or to prove an algorithm
that exploits the restricted physical coupling. No extension from the
abstract rank-one/slab reduction is assumed. Separate priority of this
geometric family has not been established by a complete literature audit.

Many local optima in pooling are established prior phenomena. For example,
[Grothey and McKinnon (2020), Section 3](https://arxiv.org/pdf/2002.10899)
give a two-quality, three-pool geometric example with several symmetric
global solutions and many additional local solutions. That primary section
was inspected directly; it does not state the one-pool, degree-two,
asymptotic `2^n` family or its explicit LP hull developed here. This is a
bounded comparison, not proof that no earlier matching construction exists.
