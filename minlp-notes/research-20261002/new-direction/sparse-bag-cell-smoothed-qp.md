# Expected exact sparse box QP under independent linear noise

Date: 2026-10-02. Status: complete theorem that passed two independent
proof reviews and targeted exact checks. The algorithm uses sparse tables of retained bag
cells; it does not construct complete continuous Bellman messages.
Publication priority and practical performance are not established.

## 1. Result

Consider the rational continuous-box quadratic

```
F_gamma(x)=F_0(x)+gamma'x,
F_0(x)=x'Hx/2+b'x+c,
X=product_i [ell_i,u_i].
```

Substitute fixed coordinates out. Assume `n>=1`, all remaining widths
`w_i=u_i-ell_i` are positive, and a supplied tree decomposition has
largest bag size `p`. Let

```
s=max_i w_i,           W=sum_i w_i,
L>0 rational, with H_ii<=L for all i.
```

Here `L` is a bound for the summed objective, not a sum of absolute
factor Hessian norms. If every diagonal is nonpositive, endpoint DP
already solves the problem exactly; that case may be handled separately.
Let `I` be the rational base input length, including `L`, the decomposition,
and a rational noise half-width `sigma>0`. When a positive diagonal exists,
one can choose its largest value as `L` directly from the input.

There is a power-of-two grid size `N`, computed from the base data and
having polynomial binary length, such that independent uniform draws

```
gamma_i in {-sigma+2sigma k/(N-1): k=0,...,N-1}          (1)
```

admit an algorithm with the following guarantees:

- It returns an exact rational global optimizer and value on every draw.
- Its expected bit work is at most

  ```
  C_0^p [4+(1+n/2)Ls/(2sigma)]^p (I+1)^C,              (2)
  ```

  for absolute constants `C_0,C`.
- It requires no supplied growth constant, uniqueness assumption,
  variable-occurrence bound, or bound on negative inertia.

Thus work is expected polynomial for each fixed bag size when the
displayed numerical curvature/width/noise ratio is polynomially bounded.
The powers of `n` prevent an FPT conclusion in `p` and a dimension-free
noise ratio. The target is the perturbed objective under the particular
base-chosen finite law (1), not an arbitrary coarser atomic law.

An exact active-face fallback handles exceptional draws of the same
sampled input. It does not reject or resample them. All pruning and
closure tests are valid independently of the probabilistic analysis.

## 2. Common nested grids and sparse bag tables

First replace the decomposition by a rooted tree of maximum degree three
using copies of existing bags. This preserves bag size and needs only
linear additional bags. Assign each quadratic monomial and linear term
to one containing bag, without duplicating its contribution.

At level `j`, set `h_j=s 2^(-j)`. Coordinate `i` has the deterministic
partition with nodes

```
ell_i, ell_i+h_j, ell_i+2h_j, ..., u_i,
```

where only points below `u_i` are included before the final endpoint.
These partitions are nested. Every interval has width at most `h_j`,
and an old interval splits into at most two new intervals. Very short
coordinate intervals may stay unrefined for several levels.

A bag cell is a product of adjacent coordinate intervals. Each bag
stores a whitelist of such cells. Initially each bag has its original
box as its only cell. At each later level, its candidate cells are all
children of the preceding retained cells. Let `D_j` be the physical set

```
D_j={x in X: x_B lies in some candidate cell of every bag B}.       (3)
```

This set is used only in the correctness proof. The algorithm stores
the bag cells and their corners, not a list of all global cells.

The allowed row list of bag `B` is the union of its candidate-cell
corners, with duplicate tuples removed. A full grid assignment is allowed
when every bag tuple belongs to that bag's row list. This is precisely
the set of global level-grid nodes in `D_j`: a grid node belonging to
an adjacent-interval cell must be one of that cell's corners.

Ordinary two-pass tree DP computes the exact grid minimum `m_j`, an
attaining full assignment, and every bag-row min-marginal

```
m_B(v)=min{F_gamma(y): y is an allowed full grid assignment, y_B=v}.
                                                               (4)
```

Each directed message stores a minimum keyed by the separator tuple.
For each row, look up the incoming minima on its separator keys, add
the local factor value, and update the outgoing key. Missing keys have
value infinity. The second pass gives all min-marginals. No pairwise
cross product of adjacent bags' row lists is needed. Bounded degree
makes the row work linear up to polynomial arithmetic, sorting, and
key-handling factors. This is standard finite-state DP on sparse row
lists, with the same running-intersection requirement as dense tables.

## 3. Rounding and certified cell pruning

Put

```
E_j=nLh_j^2/8.                                                    (5)
```

For a point `x in D_j`, independently round each coordinate to the two
endpoints of its containing grid interval, preserving its mean. If a
coordinate is already a grid node, keep it fixed. Every outcome remains
in `D_j`. Indeed, in each bag choose any candidate cell containing
`x_B`. A nongrid coordinate has a unique containing interval, so its
rounded values lie in that cell. A boundary coordinate stays fixed,
so different bags' choices of containing cells cause no conflict.
This also preserves membership in any specified bag cell containing
`x_B`.

Independence cancels off-diagonal quadratic errors. Each coordinate
variance is at most `h_j^2/4`, so

```
E[F_gamma(round(x))] <= F_gamma(x)+E_j.                            (6)
```

In particular, if `D_j` contains the original optimal set, then
`m_j<=f*+E_j`. Maintain a monotone incumbent `U_j` by taking the
best feasible grid value seen so far. Thus

```
f*<=U_j<=m_j<=f*+E_j.                                             (7)
```

For a candidate cell `C` of bag `B`, compute

```
q_C=min_{v a corner of C} m_B(v),       LB_C=q_C-E_j.               (8)
```

Equation (6), with bag `B` constrained to `C`, proves that `LB_C`
is a lower bound for every point of `D_j` whose bag coordinates lie
in `C`. Retain `C` exactly when `LB_C<=U_j`; ties are retained.
Every cell containing an original optimizer is retained. Replacing
the whitelists by the retained lists and refining them therefore
preserves all original optimizers at every level.

For each retained cell there is an actual allowed full grid assignment
`y` attaining `q_C`, with a corner of `C` as its bag tuple, and

```
F_gamma(y)<=U_j+E_j<=f*+2E_j.                                    (9)
```

This is a single globally consistent feasible assignment supplied by
DP, not a collection of unrelated per-bag choices. Infeasible rows
have infinite min-marginals and cannot supply this witness.

Storing the discarded-cell lower bounds and DP records gives a
pruning history for the original domain. The later exact closure uses
the resulting invariant that every original optimizer is retained.

## 4. Expected bag counts from local coefficient comparisons

Fix a bag `B` and condition on the noise outside it. Define the
original-domain conditional value

```
V_B(v)=min_{x_(outside B) in their original box}
       [F_0(x)+sum_(i outside B) gamma_i x_i].                    (10)
```

This function is independent of every `gamma_i` in the bag. It has
upper coordinate curvature `L`: after subtracting `L v_i^2/2`,
each coordinate restriction is an infimum of concave functions.
The bag-dependent feasible set used by the algorithm is not used in
this conditional value or probability argument.

Every bag corner supplied by (9) satisfies

```
V_B(v)+gamma_B'v <= min(V_B+gamma_B'v)+2E_j.                       (11)
```

At a regular coordinate grid node, both `v_i-h_j` and `v_i+h_j`
are feasible. Comparing (11) with those two neighbors confines
`gamma_i` to an interval of length at most

```
Lh_j+4E_j/h_j = (1+n/2)Lh_j.                                    (12)
```

The interval endpoints depend only on `v` and the noise outside `B`.
The other in-bag linear coefficients cancel. Thus independence can be
used jointly for all regular coordinates of this fixed bag tuple.

There are at most three exceptional nodes in each coordinate: the
left endpoint, the last full-step node, and the clipped right endpoint.
All other nodes have both regular neighbors. The number of regular
nodes is at most `w_i/h_j`. A uniform `N`-point noise grid assigns
an interval of length `a` probability at most `a/(2sigma)+1/N`.
Summing the product bounds over the complete deterministic bag grid
therefore gives

```
E[# bag grid tuples satisfying (11)]
 <= product_(i in B) [3+(1+n/2)Lw_i/(2sigma)+w_i/(N h_j)].         (13)
```

Only the counting proof uses the full deterministic grid. The
algorithm generates corners of sparse candidate lists.

If levels stop at `J` and `N>=2^J`, then `w_i<=s` implies
`w_i/(N h_j)<=1` for every `j<=J`. Define

```
H_B=product_(i in B) [4+(1+n/2)Lw_i/(2sigma)].                    (14)
```

The bound (13) is at most `H_B`, independently of the refinement level.
Each full-grid bag corner belongs to at most `2^|B|` bag cells.
By (9), the expected number of retained cells is at most
`2^|B| H_B`. Each has at most `2^|B|` children, each child has at
most `2^|B|` corners, and duplicates are removed. Thus expected
candidate-list and table work per level is bounded by a constant to
the power `p` times the sum of the bag bounds (14), with polynomial
factor-evaluation and arithmetic overhead.

For independent continuous noise with density bounds `phi_i`, the
same argument gives `product_i[3+(1+n/2)Lw_i phi_i]` without an
atomic term. The finite-law version above is what is used for exact
rational output.

## 5. Exact closure by original-bound KKT signs and convexity

After pruning, compute the coordinate projection hull of each bag's
retained cells. For each coordinate, intersect these intervals over
all bags containing it. Call the product of the resulting intervals
`Q_j`. It contains every original global optimizer, although it need
not contain every retained cell projection.

Each gradient component is affine. Compute its exact interval range
on `Q_j`. If the lower end is strictly positive, record the equation
`x_i=ell_i`; if its upper end is strictly negative, record `x_i=u_i`.
These are the **original** box endpoints. Every original global
optimizer satisfies each recorded equation, by first-order optimality
on the original box. This reasoning needs neither a growth estimate
nor a feasible monotone path through the retained cell unions.

Let `A_j` be the original box face defined by all recorded equations.
If the principal Hessian on its unfixed coordinates is PSD, solve the
resulting convex box QP exactly and stop. Every original optimizer
lies in `A_j`, so this convex solve returns the original global
optimum. A PSD test, the gradient-sign bounds, the pruning history,
and convex-QP KKT multipliers are independently checkable.

The recorded equations need not be inserted into the grid DP during
the search. Continuing with the original grids avoids changing the
counting argument; the equations are used for the closure test only.
They may also be intersected with `Q_j` for further gradient-sign tests,
because every original optimizer already satisfies them.
On arbitrary draws they may be insufficient to trigger closure.

Suppose a draw has a unique optimizer `x*`, point growth at least
`g_0>0`, and every active coordinate has gradient magnitude greater
than `tau>0` at `x*`. Let

```
M=max(1,max_i sum_k |H_ik|),        A=2+nL/g_0.                   (15)
```

The witnesses in (9) are within Euclidean distance
`h_j sqrt(nL/g_0)/2` of `x*`. Every retained cell is therefore
within coordinatewise distance

```
r_j=h_j[1+sqrt(nL/g_0)/2] <= A h_j                              (16)
```

of `x*`, and the same holds for `Q_j`. If

```
h_j <= tau/(2 M A),                                              (17)
```

every gradient differs from its value at `x*` by at most `tau/2`
on `Q_j`. All active coordinates are then recorded at their correct
endpoints. The Hessian on the remaining, interior coordinates is
positive definite: it is PSD by second-order optimality, while a
nonzero kernel direction would give other optima by exact quadratic
expansion. Thus the PSD closure test has succeeded by this level.
When no free coordinate remains, the PSD test is vacuous.

This is an analysis of when sound closure succeeds. The algorithm
does not test or trust `g_0` or strict complementarity.

## 6. A base-only level cap and one fixed finite noise law

Put

```
B=3^n,         C_tail=8(B+1)^2,        K=nB,
rho=1/(4B),
g_0=rho sigma/(2W),                  tau=rho sigma/(2K).          (18)
```

Use (15) and choose the least integer `J>=0` satisfying (17) with
`h_J=s2^(-J)`. These quantities depend only on the base input, and
`J` is polynomial in its binary length.

Choose the least power of two `N` such that

```
N >= max{2, 2^J, 4n C_tail/rho, 2K/rho}.                         (19)
```

Then sample (1) once. The grid has polynomial-bit coordinates because
`log N` is polynomial in the base input. Crucially, (19) is not a
condition involving an exact-recovery precision that itself depends
on the sampled denominators.

The [finite-grid growth-tail theorem](proximal-growth-tail.md),
Section 8, gives

```
Pr{g_*<g_0} <= g_0 W/sigma + 2n C_tail/N <= rho.                  (20)
```

Here `g_*` is the point-growth modulus, defined to be zero on draws
with distinct optimizers. Thus the complement of this bad event has
a unique optimizer.

For the active-gradient margin, consider any original box face with
nonsingular free Hessian. Its stationary free vector is affine in
`gamma_J`, and an active gradient component has the form

```
gradient_i = gamma_i + an affine function of gamma_J,
                      i not in J.                               (21)
```

The coefficient of its own noise is exactly one. Conditional on all
other noise, the event `|gradient_i|<=tau` has probability at most
`tau/sigma+1/N`. There are at most `K=n3^n` face-coordinate pairs,
so the union has probability at most

```
K(tau/sigma+1/N) <= rho.                                         (22)
```

Faces and their hyperplanes are counted only in the analysis, not
enumerated by the search. On a unique-optimum draw, the free Hessian
of the optimizer's smallest face is positive definite, so its active
gradients are among (21). Combining (20)--(22), the hypotheses for
closure by level `J` hold except on an event of probability at most
`2rho=1/(2B)`.

Run the sparse cell algorithm through level `J`. If it has not closed,
run exact active-face enumeration on that same draw. Enumeration takes
`B poly(I+log N)` bit work: on each face with positive-definite free
Hessian, solve its rational stationary equations and retain feasible
solutions, including vertices. Some global optimizer belongs to a
minimum-dimensional optimal face whose free Hessian is positive
definite; a null direction would otherwise move to a smaller optimal
face. Taking the best retained candidate is exact even on tied or
degenerate draws. No optimization oracle with unknown complexity is
being used in this fallback.

## 7. Expected bit work and scope

The expected fallback contribution is at most a polynomial because
its probability is at most `1/(2B)`. For the search, sum (14) over
the `J+1` levels and the bags. Generation of candidate cells is
charged to retained cells at the preceding level. Maximum degree
three and separator-key minima prevent products of random table
sizes in the DP work.

Every generated grid coordinate has polynomial encoding length in
`I+j`. Sampled coefficients add `O(log N)` bits. Quadratic
evaluation, message addition, exact comparison, interval gradient
evaluation, rational PSD tests, and exact convex QP closure have
polynomial bit cost. Sorting and dictionary keys add at most a
polynomial factor: even the full level grid has logarithmic size
`O(p(J+I))`. Therefore the total expected bit work is bounded by

```
C_0^p (I+1)^C sum_B H_B,
```

with an absolute exponent after absorbing the polynomial number of
bags and levels. Replacing all widths by `s` gives (2), with a
possibly larger absolute constant `C`.

The result permits arbitrary positive and negative curvature, arbitrary
negative inertia, and unbounded variable occurrence. The numerical
factor still uses upper coordinate curvature `L`, not only `nu`.
It does not resolve the open deterministic sparse `nu/g` target.
The expected bound concerns one specified fine rational noise law;
it does not extend automatically to arbitrary atomic perturbations.
The current endpoint-forcing closure proof is continuous and should
not be applied to integer variables without a separate argument.

## Review and verification

The [algorithm review](sparse-bag-cell-review.md) checks rounding through
overlapping cell whitelists, consistent DP witnesses, sparse joins,
optimizer-preserving pruning, and exact face closure. A separate
[noise review](sparse-bag-cell-noise-review.md) checks the independent-noise
counts and finite-law schedule.

The [hardness sanity check](sparse-smoothed-hardness-sanity.md) reads the
bounded-coefficient width-two reduction of Del Pia--Khajavirad. An
explicit NO family has exponentially small positive decision gap;
inverse-polynomial independent linear noise crosses its original
threshold with substantial probability. This explains compatibility
with that reduction, without excluding other possible robust reductions.

The commands actually run were

```
python3 -B research-20261002/new-direction/check_sparse_bag_cells.py
python3 -B research-20261002/new-direction/check_sparse_bag_noise.py
```

The [sparse DP checker](check_sparse_bag_cells.py) passed five instances
and 16 stages: 2,295 exact min-marginals matched exhaustive assignments,
2,807 rounding atoms preserved the whitelists, and 392 retained-cell
witnesses satisfied the objective bound. It removed 951 cells while
preserving the tested optima and reached three exact PSD-face closures.
A separate shared-boundary fixture passed, including four infeasible
bag rows. The [recorded results](sparse-bag-cell-check-results.json)
give the full counts and scope.

The [finite-noise diagnostic](check_sparse_bag_noise.py) passed eight
clipped-grid cases and 238 bag tuples, checking all 64 in-bag draws
for each tuple and two conditioned private coefficients. It also
covered 45 empty comparison intervals.

These are exact checks of the sparse DP, rounding, closure, and local
probability inequalities. They do not implement the complete sampled
solver with its base-only cutoff and rare fallback, establish the
asymptotic expectation by experiment, or demonstrate practical speed.
They are separate from the literature-priority audit.
No project-wide verification or CI inspection is part of this work.
