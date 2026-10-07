# Expected exact sparse mixed-integer box QP under linear noise

Date: 2026-10-02. Status: complete theorem that passed two independent proof
reviews and targeted exact mixed DP checks. This extends the
[continuous sparse-cell theorem](sparse-bag-cell-smoothed-qp.md) to arbitrary
integer dimension. Publication priority and practical performance are not
established.

## 1. Statement and scope

Let

```
F_gamma(x)=x'Hx/2+b'x+c+gamma'x
```

be rational, on a product of bounded rational continuous intervals and bounded
integer intervals. Round integer bounds inward and substitute fixed
coordinates. Empty domains are detected immediately. Let `n_c,n_z` count the
remaining continuous and integer coordinates, `n=n_c+n_z>=1`, and

```
w_i=u_i-ell_i>0,      W=sum_i w_i,      w_max=max_i w_i.
```

Remaining integer endpoints and widths are integral. Supply a tree
decomposition of the interaction graph with largest bag size `p`, a rational
number `L>0` satisfying `H_ii<=L`, and rational noise half-width `sigma>0`.
Let `I` be the binary length of these base data. If all diagonal entries are
nonpositive, coordinate concavity already permits exact endpoint DP; the
theorem below does not require that special case.

There is a power of two `N`, computed from the base data with `log N`
polynomial in `I`, such that independent uniform draws

```
gamma_i in {-sigma+2sigma k/(N-1): k=0,...,N-1}                 (1)
```

admit an algorithm which returns an exact rational mixed global optimizer and
value on every draw, with expected bit work at most

```
C_0^p [4+(1+n/2)L w_max/(2sigma)]^p (I+1)^C,                  (2)
```

for absolute constants `C_0,C`. It requires no supplied growth constant,
uniqueness assumption, bound on variable occurrence, or bound on integer
dimension or negative inertia.

This is expected polynomial work for each fixed bag size when the numerical
ratio in (2) is polynomially bounded. It is not FPT in `p`, and it is not a
polynomial bound in the binary encoding of integer widths alone. The target
is the sampled objective under the particular base-chosen finite law (1).
Exceptional draws are solved exactly on the same sample, without resampling.

## 2. Nested mixed cells and certified sparse DP

Choose `s` as the least power-of-two integer at least
`max(1,w_max)`, and put `h_j=s 2^(-j)`. For continuous coordinates use
the original-endpoint clipped grid with spacing `h_j`. For integer
coordinates use the following partitions of their integer feasible set:

- While `h_j>=1`, use the same clipped grid. Its spacing and endpoints are
  integral; each cell is the integers in an adjacent-endpoint interval.
- At the first level with `h_j<1`, replace every retained unit interval
  by its two singleton endpoint cells. Thereafter integer point cells stay
  fixed while continuous cells refine.

These partitions are nested, and each old coordinate cell has at most two
children. At `h_j=1` every feasible integer value is already a grid node.
The following level changes the cells into points; it does not introduce any
new integer grid value. At level zero each bag has just its whole mixed box.

Use the same bag-cell whitelists, deduplicated corner row lists, and two-pass
separator-key DP as in Sections 2--3 of the continuous theorem. Binarize the
decomposition first, preserving bag size and using only linearly many copied
bags, so each bag has degree at most three. A full assignment is allowed
exactly when its tuple in every bag is an allowed corner row. All such
assignments are feasible for the original mixed domain. Let `D_j` denote
the physical mixed domain represented by all current candidate whitelists.

Every `x in D_j` can be rounded independently in its coordinates to cell
endpoints while preserving its mean. All integer endpoints are feasible.
Every coordinate already on a grid node is kept fixed, including every
integer coordinate once `h_j<=1`. The shared nested partitions imply that
every rounding outcome remains in every bag whitelist: a nongrid coordinate
has a unique containing interval, while a shared-boundary coordinate never
moves. This also holds when one specified bag cell must be preserved.

Off-diagonal errors cancel, and singleton integer coordinates contribute no
variance. Thus, with

```
E_j=n L h_j^2/8,                                               (3)
```

the expected rounded objective is at most `F_gamma(x)+E_j`.
Let `m_j` be the exact allowed-grid minimum, `U_j` the best feasible value
seen so far, and `m_B(v)` the exact bag-row min-marginal. Provided `D_j`
contains every original optimizer,

```
f* <= U_j <= m_j <= f*+E_j.                                    (4)
```

For each candidate bag cell `C`, set

```
q_C=min_{v a corner of C} m_B(v),       LB_C=q_C-E_j.            (5)
```

Retain exactly the cells with `LB_C<=U_j`, including ties. Rounding with
the specified cell preserved proves that `LB_C` bounds every feasible
point in that cell within `D_j`. Therefore all original optimizers remain
retained at every level. Every retained cell has a single globally
consistent feasible full-grid witness `y`, with `y_B` a corner of it, such
that

```
F_gamma(y)=q_C <= f*+2E_j.                                     (6)
```

The DP computes these quantities by minima keyed on separator tuples; it
does not take cross products of adjacent bags' row lists.

## 3. Expected cell counts with integer directions

Condition on all noise outside a bag `B`, and define

```
V_B(v)=min_{x_outside in their original mixed domain}
       [F_0(v,x_outside)+gamma_outside'x_outside].              (7)
```

Define this function also for real values of the bag's integer coordinates.
The outside feasible set is fixed independently of `v`, so subtracting
`L v_i^2/2` leaves a coordinatewise concave function. Thus `V_B` has upper
coordinate curvature `L`, even though the comparisons below use only
feasible mixed bag values. It is independent of every noise coefficient in
the bag.

For a retained-cell witness corner `v`, (6) implies

```
V_B(v)+gamma_B'v <= min_{v' in the original mixed bag domain}
                            [V_B(v')+gamma_B'v'] + 2E_j.       (8)
```

Let the comparison spacing for coordinate `i` be

```
a_i,j = h_j              if i is continuous,
a_i,j = max(1,h_j)       if i is integer.                       (9)
```

At a regular node, both neighbors at distance `a_i,j` are feasible mixed
values. Comparing (8) with those neighbors confines `gamma_i` to an
interval, independent of all other in-bag noise, of length at most

```
L a_i,j + 4E_j/a_i,j.
```

There are at most three exceptional coordinate nodes and at most
`w_i/a_i,j` regular nodes. At fine integer levels the two original endpoints
are the only exceptions. Independence and the finite-noise interval bound
`length/(2sigma)+1/N` give

```
E[number of full-grid bag tuples satisfying (8)]
 <= product_(i in B)
    [3 + Lw_i/(2sigma) (1+n h_j^2/(2a_i,j^2))
       + w_i/(N a_i,j)].                                     (10)
```

Since `a_i,j>=h_j`, for every `j<=J` and `N>=2^J` this is at most

```
H_B=product_(i in B) [4+(1+n/2)Lw_i/(2sigma)].                  (11)
```

Indeed, `w_i/(N a_i,j)<=s/(N h_j)=2^j/N<=1`. No separate lower bound
`N>=s` is needed. Only this counting argument uses the complete grid; the
algorithm generates sparse cell lists.

A corner belongs to at most `2^|B|` bag cells, including during the
integer singleton transition. Each retained cell has at most `2^|B|`
children with at most `2^|B|` corners. Consequently, expected cell and row
work per level is at most a constant to the power `p` times `sum_B H_B`,
with polynomial arithmetic and dictionary overhead. Bounded-degree
separator-key minima avoid products of random adjacent table sizes.

## 4. Exact mixed closure without a growth premise

Intersect the coordinate projection hulls of all retained bags containing
each coordinate. Their product `Q_j` contains every original optimizer.
Two distinct rules are used:

1. Fix an integer coordinate only when its intersected hull is a singleton,
   to that integer value. This value may be an interior integer.
2. For a continuous coordinate, compute its affine gradient range on
   `Q_j`. A strictly positive range forces its original lower endpoint;
   a strictly negative range forces its original upper endpoint, by the
   original mixed problem's first-order condition within its integer slice.

The gradient rule is not used for integer coordinates. Recorded equations
may be intersected into the hull for further tests because all original
optimizers satisfy them. As in the continuous algorithm, they need not be
inserted into the DP grids.

Invoke convex closure only after **all integer coordinates have been
fixed**, and only if the principal Hessian on the remaining continuous
coordinates is PSD. Solve that continuous convex box QP on the original
continuous face exactly. It contains every original optimizer at the
recorded integer assignment, so its solution is globally optimal for the
original mixed problem. With no remaining continuous coordinates, simply
evaluate the fixed point. PSD of the continuous block alone does not
justify closure while integer choices remain.

All these tests are sound on every draw. Their validity does not assume
the growth or margin events used next to bound the stopping time.

Suppose the draw has a unique mixed optimizer `x*`, point growth at least
`g_0>0` on the original mixed domain, and absolute gradient greater than
`tau>0` at each active continuous coordinate. Put

```
M=max(1,max_i sum_k |H_ik|),       A=2+nL/g_0.                   (12)
```

By (6), every witness is at distance at most
`h_j sqrt(nL/g_0)/2` from `x*`. At `h_j<1`, every integer cell is a
singleton; its value is the corresponding coordinate of its witness.
Every retained continuous cell and every coordinate hull is within
coordinatewise distance

```
h_j[1+sqrt(nL/g_0)/2] <= A h_j
```

of `x*`. In particular, if

```
h_j <= min{1/(4A), tau/(2MA)},                                 (13)
```

then `h_j<1` and each retained integer value is within `1/4` of the
optimal integer value. Hence every integer hull is its optimal singleton.
All gradients vary by at most `tau/2` on the hull, so all active continuous
coordinates are forced to their original endpoints. The free continuous
Hessian is positive definite: second-order optimality makes it PSD, and a
nonzero kernel direction would give distinct optima in that same integer
slice by exact quadratic expansion. Thus convex closure succeeds by (13).

## 5. Base-only cutoff, finite noise, and exact fallback

Define

```
B = 3^n_c product_(i integer) (w_i+1),
C_tail=8(B+1)^2,             K=max(1,n_c B),
rho=1/(4B),
g_0=rho sigma/(2W),         tau=rho sigma/(2K).                 (14)
```

Choose the least `J>=0` satisfying (13), with (12) and `h_J=s2^(-J)`.
Then choose the least power of two

```
N >= max{2, 2^J, 4n C_tail/rho, 2K/rho}.                       (15)
```

All quantities are computed from the base data before drawing noise.
Although `B` may be enormous, `log B`, `J`, and `log N` are polynomial
in the binary input length. Large integer ranges do not create an
exponential sampling precision.

The [finite-grid growth-tail theorem](proximal-growth-tail.md), Section 8,
already covers mixed boxes with the face count `B` in (14). It gives

```
Pr{g_*<g_0} <= g_0 W/sigma + 2n C_tail/N <= rho,                (16)
```

where `g_*=0` on draws with distinct optimizers.

For the continuous active-gradient event, fix an integer assignment and an
original continuous face with nonsingular free Hessian. Its stationary
free vector is affine in its free continuous noise. Every active
continuous gradient has the form

```
gradient_i = gamma_i + an affine function of the free noise.   (17)
```

Its own coefficient is exactly one. Fixed integer assignments contribute
only deterministic offsets; their linear noise is constant within the
slice. There are at most `n_c B<=K` such face-coordinate pairs, and each
has probability at most `tau/sigma+1/N` of absolute value at most `tau`.
Their union has probability at most `rho`. A unique optimizer has a
positive-definite free Hessian on its smallest continuous face, so the
relevant gradients occur in this union. With no continuous coordinates
the event is empty. It follows that closure succeeds by `J` except on an
event of probability at most `2rho=1/(2B)`.

If closure has not succeeded by `J`, enumerate all integer assignments
and original continuous faces on that same sampled input. For each face
whose free Hessian is positive definite, solve its rational stationary
equations and keep the feasible candidates, including vertices. There
is a global optimizer on a minimum-dimensional optimal continuous face
within an optimal integer slice. Its free Hessian is positive definite;
otherwise a null direction reaches a smaller optimal face at unchanged
objective. Thus the best enumerated candidate is globally optimal,
including on tied or degenerate draws. This fallback costs
`B poly(I+log N)` bit work.

## 6. Expected bit work and interpretation

The fallback contributes polynomial expected work because its probability
is at most `1/(2B)`. Summing (11) over the polynomial number of levels
and bags gives

```
C_0^p (I+1)^C sum_B H_B,
```

with an absolute polynomial exponent. Grid coordinates and sampled
coefficients have polynomial encoding length. Sparse-table sorting,
factor evaluation, message arithmetic, hull and gradient computations,
rational PSD tests, and exact continuous convex-QP closure have polynomial
bit cost. Even the logarithm of a complete level-grid table is polynomial
in `I+J`, so sorting sparse generated lists adds only a polynomial factor.
Absorbing the bag count and replacing individual widths by `w_max`
proves (2).

The integer dimension is unrestricted. Its ranges appear numerically in
the expected cell count, and logarithmically in the cutoff and rare-event
budget. This distinction is essential: the result does not turn binary
encoding of huge integer intervals into a range-independent running time.
The output solves the perturbed MIQP exactly; no approximation claim about
the unperturbed objective is made. The cell-pruning and closure history is
valid without trusting the probabilistic growth analysis.

## Review and verification

The [deterministic review](sparse-mixed-bag-cell-review.md) checks preservation
of every original optimizer, the unit-to-singleton transition, fixing of
interior integer values, and the requirement to fix all integers before
convex closure. The independent
[noise and bit review](sparse-mixed-bag-noise-review.md) checks the real
extension of mixed recourse, coordinate comparison intervals, finite atoms,
the base-only cutoff, and the rare-fallback budget.

The commands actually run were

```
python3 -B research-20261002/new-direction/check_sparse_mixed_bag_cells.py
python3 -B research-20261002/new-direction/check_sparse_bag_cells.py
```

The [mixed checker](check_sparse_mixed_bag_cells.py) passed four instances
and 19 stages. All 444 bag min-marginals matched exhaustive allowed-grid
assignments; 1,171 rounding atoms remained feasible; 151 retained witnesses
met the error bound; and 115 cells were removed while preserving the tested
optima. Six integer coordinates were fixed from singleton hulls, and three
instances reached exact closure. The
[recorded results](sparse-mixed-bag-cell-check-results.json) include an
interior integer optimum with positive derivative, a PSD instance with two
tied integer labels that correctly does not close, a nonconvex mixed
instance, and a purely integer instance.

The continuous regression also passed its five instances, 16 stages,
2,295 min-marginals, and shared-boundary fixture after the common checker
was extended to support integer coordinates. These tests verify finite
algorithmic steps. They do not implement the complete sampled solver with
its base-only cutoff and exceptional fallback, establish the asymptotic
expectation by experiment, or demonstrate practical speed. No project-wide
verification or CI inspection was performed.
