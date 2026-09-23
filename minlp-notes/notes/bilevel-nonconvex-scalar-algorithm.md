# An exact scalar-tariff algorithm with a nonconvex aggregate follower

Date: 2026-09-07. Status: exact specialization and implementation independently
reviewed twice, with review corrections incorporated.

Independent audits: [first proof and code review](review-bilevel-nonconvex-one.md)
and [second proof and code review](review-bilevel-nonconvex-two.md). They include
86 adversarial exact checks, 350 independent original-space global comparisons,
72 atlas cell/point comparisons, 30 comparisons against a separate all-pair
envelope construction, and 11 further edge-case groups. These checks support
the proof audit within the stated scope; they are not a novelty certification.

This is an implementable specialization of the existing
[fixed-aggregate response theorem](../results/bilevel-fixed-aggregate-response-algorithm.md).
It supplies explicit global response comparisons for a genuinely nonconvex
follower. It does not claim a new general complexity boundary. Resource-allocation
multiplier sweeps, parametric quadratic programming, and lower-envelope
comparisons are classical ingredients. Source positioning belongs with the
repository's [source positioning](bilevel-nonconvex-source-positioning.md); this
note makes no priority claim for their combination. Univariate nonconvex
piecewise-quadratic convex envelopes and conjugates already have established
algorithms, including Gardiner–Lucet (2010) and Moehle et al. (2021), Appendix B.

Implementation: [scalar_solver.py](../code/bilevel_nonconvex/scalar_solver.py).
All accepted inputs are rational; binary floating-point inputs are rejected.
The code uses SymPy exact arithmetic and comparisons, without numerical root
selection or optimization tolerances.

## 1. Model and algorithmic statement

For rational data, let the scalar tariff satisfy `x in [L,U]`. The follower solves

```
min  sum_i (d_i*z_i^2/2 + c_i*z_i) - h*(u^T z)^2/2 + gamma*x*(u^T z)
s.t. lower_i <= z_i <= upper_i,
```

where `d_i>0`, `h>=0`, and `gamma!=0`. The aggregate weights `u_i` may have
both signs or be zero; box intervals may be singletons. The follower's Hessian
`Diag(d)-h*u*u^T` need not be positive semidefinite. The dimension of the
follower, the rational bit lengths, and the number of upper constraints may grow.
The leader maximizes tariff revenue `x*w`, where `w=u^T z`, subject to finitely
many affine rows `a_j*x+b_j^T*z<=rhs_j`.

We use the following explicit conventions:

- **Optimistic:** the leader chooses a global follower minimizer satisfying
  the upper rows and maximizes its revenue.
- **Robust pessimistic:** every global follower minimizer must satisfy the
  upper rows, and the leader maximizes the least revenue among those responses.
  This is a specified robust feasibility convention, not an assertion that all
  definitions of pessimistic bilevel constraints agree with it.

**Specialization.** Both problems admit an explicit polynomial rational-bit
algorithm. It constructs every global follower response; it decides infeasibility;
otherwise it returns the exact revenue supremum and decides attainment. If
attained, it supplies a tariff and follower response. All reported algebraic
coordinates and values have degree at most two over the rationals. In the
pessimistic case the supplied response realizes the worst revenue at the returned
tariff. An unattained supremum instead includes a one-sided limit pair, explicitly
not presented as a feasible optimizer.

The optimistic problem, when feasible, attains its maximum because its feasible
response graph is closed in a compact box. The explicit attainment machinery is
needed for the robust pessimistic problem and serves as a consistency check for
the optimistic implementation.

## 2. Exact resource-allocation compression

Define

```
C(w) = min { sum_i(d_i*z_i^2/2+c_i*z_i) : box bounds, u^T z=w }.
```

Every nonempty fiber has a unique minimizing point, by strict convexity of the
local objective. Moreover every global follower minimizer must be this point on
its fiber. Thus the original problem is equivalent to minimizing
`psi(w)+gamma*x*w` over its aggregate interval, with `psi=C-h*w^2/2`.

For a resource multiplier `lambda`, the unique minimizer of the strictly convex
local objective minus `lambda*u^T*z` is

```
z_i(lambda)=clip((lambda*u_i-c_i)/d_i,lower_i,upper_i).
```

For each varying coordinate with `u_i!=0`, its two clipping events are
`(d_i*lower_i+c_i)/u_i` and `(d_i*upper_i+c_i)/u_i`. Sort these events, combining
ties. Between adjacent events, write `z(lambda)=a+b*lambda` and
`w(lambda)=w0+S*lambda`, where

```
S = sum_{free i} u_i^2/d_i >= 0.
```

When `S>0`, invert this expression. It yields a rational affine fiber solution
`z(w)=alpha+beta*w` on a closed rational aggregate interval and a rational
quadratic expression `psi(w)=A*w^2+B*w+D`. When `S=0`, the aggregate is constant;
there is no missing positive-length aggregate interval. Such points are included
by neighboring positive-slope pieces. Coordinates with `u_i=0` stay at their
independent local minimum. Fixed coordinates are also retained.

The map `w(lambda)` is continuous and nondecreasing, runs from the minimum to
the maximum attainable aggregate, and has at most `2N-1` positive-length pieces.
Hence these pieces cover the entire aggregate interval. Their fiber solutions
agree at shared endpoints by uniqueness. The degenerate case of a single
attainable aggregate is represented by one singleton piece.

This is the classical continuous quadratic resource-allocation reduction; its
use here is to retain the global nonconvex scalar minimization after compression.
It does not conclude that local follower KKT conditions imply global optimality.

## 3. Finite candidates and flat response intervals

On each piece `[p,q]`, the reduced objective is

```
A*w^2+(B+gamma*x)*w+D.
```

Include the following candidates:

1. Every distinct fiber-piece endpoint, valid for the entire leader interval.
2. For `A>0`, the stationary point
   `w(x)=-(B+gamma*x)/(2A)`, on exactly the rational tariff interval where
   `p<=w(x)<=q`.
3. For `A=0`, the entire interval `[p,q]` at the single tariff
   `x=-B/gamma`, but only if its common value equals the global minimum.

If `A<0`, every piece minimum is at an endpoint. If `A=0` away from its flat
tariff, every piece minimum is also at an endpoint. Consequently this list
contains all global follower minimizers, not merely one selected minimizer.
Endpoint costs are affine in the tariff; stationary-branch costs are quadratic
with rational coefficients. Flat intervals are tested by their endpoint costs.

Partition `[L,U]` at candidate-domain boundaries, at every real pairwise cost
intersection lying in both candidates' domains, and at flat tariffs. Each
partition point is rational or a root of a rational polynomial of degree two.
On each resulting open cell, candidate validity and relative cost ordering are
constant. Exact comparison at a rational interior sample therefore identifies its global winners.
At every partition point, compare all valid candidates again and add every
flat interval passing the global cost comparison.

Every open cell has a unique aggregate response, although duplicate candidates
can describe it. To see this, if two distinct candidate branches both win
throughout a cell, their value polynomials agree identically. The derivative of
each value polynomial is `gamma*w(x)` (direct differentiation for endpoints and
stationary branches). Since `gamma!=0`, their aggregate responses are identical.
Strict fiber convexity then makes their complete follower responses identical.
The nonzero-tariff-coupling hypothesis is used at precisely this step.

## 4. Exact leader optimization and ties

On each open tariff cell, `w(x)` and `z(x)` are rational affine functions.
Every upper row is consequently a rational affine inequality in `x`; their
intersection with that cell is an interval, possibly empty or a singleton.
Revenue `x*w(x)` is quadratic. Its supremum over the feasible interval is found
from its two limiting endpoints, its interior stationary point when concave,
and one rational interior sample to certify attainment for a constant objective. Endpoint
inclusion is tracked explicitly; a limiting endpoint excluded by the open cell
is not declared an optimizer.

At a partition point, each global response is either a singleton or a fiber
interval on which `z(w)` is affine. Under optimistic semantics, intersect each
such interval with the affine upper rows and maximize the linear function `x*w`
there. Under robust pessimistic semantics, test every row at both endpoints of
every minimizing interval, then minimize `x*w` over those endpoints. Affinity
makes these endpoint checks necessary and sufficient, including a continuum of
tied follower responses. Comparing all cell suprema and feasible point values
returns the global supremum. It is attained if and only if some maximizing
candidate is included in its domain.

For an unattained supremum, the reported cell limit can be approached by
feasible interior tariffs from the corresponding interval. It is not a claim
that the follower response at the limit tariff preserves the same robust
feasibility or pessimistic revenue.

## 5. Complexity and exact arithmetic

There are `O(N)` fiber pieces and candidate branches, and `O(N^2)` candidate
intersection points. Straightforward all-candidate comparisons on every cell
and point take `O(N^3)` branch-processing steps, excluding the bit-dependent
work inside exact sign and rational interior-sample routines. Constructing and
storing all fiber response coefficients uses `O(N^2)` arithmetic/storage. With
`m` affine upper rows, the deliberately simple implementation uses at most
`O(m*N^3+N^3)` further scalar operations, and can retain `O(N^2)` partition data.
These are generous combinatorial processing bounds, not optimized implementation
claims or bounds independent of coefficient bit length for the arithmetic helpers.

All rational coefficients have polynomial bit length. Intersection points have
degree at most two; sorting two such points uses algebraic numbers of bounded degree (at most
four); comparing branch values at rational interior samples is rational arithmetic.
A dyadic interior sample is found by doubling its denominator until it lies
strictly between the bounds; polynomial separation bounds for bounded-degree
algebraic numbers imply polynomial sample bit length and polynomial iterations. Exact signs
and equality are therefore decidable in polynomial bit time. Leader row
intersections inside cells are rational. At a fixed algebraic tariff, affine
row intersections in a flat fiber have degree at most two (in fact the flat
tariff itself is rational). Revenue evaluations and returned follower vectors
stay in the quadratic field of the selected endpoint, or are rational. These
facts give the stated polynomial-bit bound and degree-two output claim.

The implementation constructs the envelope by inserting candidate branches one
at a time. It starts with an endpoint branch valid on the whole tariff interval.
For each current open winner interval, it inserts the new branch's domain
boundaries and its cost intersections with the current winning branch, samples
the resulting subintervals exactly, and keeps the lower branch. Adjacent intervals
with the same winner are merged. Every insertion contact and every branch-domain
endpoint is retained separately, even if merging removes it from the open-cell
representation. Flat tariffs are also retained. At the end, all candidates are
compared afresh at every retained point. This avoids crossings strictly above
the envelope while preserving isolated contacts and all final global ties.

Induction proves the open-cell representation is the current candidate minimum.
To verify contact completeness, take a final tie and consider insertion of the
later tied candidate. At that tariff the earlier tied candidate already attains
the final minimum; no previously inserted candidate can have a smaller value.
Thus the new candidate meets the current envelope there. Such a meeting is an
explicit intersection with an adjacent winning branch, a candidate-domain or
existing envelope boundary, or identity with that branch on an open interval.
The first three cases are retained points. In the identity case their derivative
values give the same aggregate response, so no distinct response is lost.
A flat fiber interval is separately included at its flat tariff.

The polynomial bounds above remain valid: there are at most two distinct roots
per pair of nonidentical quadratic candidate costs and `O(N)` domain boundaries.
Insertion performs at most `O(N^3)` interval-processing steps, retains `O(N^2)`
distinct contacts, and final point scans take `O(N^3)` further branch comparisons.
Each exact sign or rational-sample operation has a further polynomial bit cost. This is a
simple exact reference implementation, not an optimal envelope implementation.
Incremental rational coefficient updates and specialized envelope data structures
remain opportunities for engineering improvements.

## 6. What this adds and what it does not establish

The general fixed-aggregate theorem already implies exact polynomial-time
solvability of this family. This specialization replaces its general algebraic
elimination step with explicit clipped-price fiber pieces, quadratic equations,
and interval optimization. It handles an indefinite follower Hessian, genuinely
nonconvex reduced fiber costs, global phase transitions, ties, response-dependent
upper constraints, and pessimistic nonattainment in executable code.

It does not cover a general nonconvex polynomial aggregate, moving box bounds,
multiple aggregate rows, multiple leader coordinates, integer followers, or
nonlinear upper rows. Generalizing the scalar aggregate polynomial would require
higher-degree branch equations and algebraic comparisons; it is not a cosmetic
change to this implementation. No solver-superiority or application-validation
claim follows from exact solvability. Timing evidence must distinguish this
actual global algorithm from the earlier convex tariff sweep.

## 7. Small exact examples that distinguish the semantics

The [example checker](../code/bilevel_nonconvex/check_scalar_examples.py) records
these exact calculations.

For `d=(1,1)`, `c=(-1,-1/2)`, `u=(1,1)`, box `[0,1]^2`, `h=3/5`,
`gamma=1`, and tariff interval `[0,1]`, the fiber cost has positive-curvature
outer pieces and a negative-curvature middle piece. At tariff `17/20`, its
only globally minimizing aggregates are `3/8` and `13/8`. With the upper
capacity row `w<=1`, optimistic revenue has maximum `51/160`, attained at
`x=17/20,w=3/8`. Robust pessimistic revenue has the same supremum but does not
attain it: tariffs approach `17/20` from above; at the limit tariff the other
global response violates the capacity. This example exercises actual global
nonconvex comparisons and response-dependent upper feasibility.

A second example explains why simply replacing the reduced follower by its
convex envelope is insufficient for bilevel feasibility. Let `N=1`, `d=u=1`,
`c=-1`, `h=3`, `gamma=1`, box `[0,1]`, and tariffs `[1,3]`. The original follower
objective is `-w^2+(x-1)*w`. At `x=2`, its global minimizers are exactly `{0,1}`.
The convexified follower has every `w in [0,1]` as a minimizer at that tariff.
Consequently an upper equality `w=1/2` makes the original bilevel problem
infeasible, while the convexified-response formulation falsely declares it
feasible. Convex-envelope methods can still supply the value and supporting
slopes, but exact bilevel response reconstruction must retain contact with the
original objective. The reference implementation compares original candidate
costs and preserves precisely those contacts.
