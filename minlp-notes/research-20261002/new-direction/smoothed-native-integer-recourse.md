# Expected exact optimization with native integer recourse

Date: 2026-10-02. Status: passed
[fresh independent review](../reviews/smoothed-native-integer-recourse-review.md).
The constant-base algebraic completion and output improvement has a
separate [scoped transfer review](../reviews/constant-base-core-transfer-review.md).
The concrete convex-flow oracle has been checked against its primary source.

A small continuous core can be coupled to arbitrarily many native integer
variables when the conditional integer problem has an exact polynomial-time
oracle stable under coordinate bounds. A competing-label certificate identifies
one residual label containing a global optimizer. Exact algebraic optimization
of that label's small continuous core then finishes the original problem.
No gradient fixing or local Hessian test is needed. This extends the
[box-stable recourse framework](smoothed-box-stable-recourse.md) to constrained
integer recourse and fixed-degree nonlinear objectives.

## 1. Model, oracle, and theorem

Let

```
X=[0,1]^k times Y,
Y={z in Z^r: Dz<=e, l<=z<=u},
F_gamma(v,z)=F_0(v,z)+gamma_C'v+gamma_R'z,
```

where all displayed input data are rational, the integer bounds are rounded
inward and encoded in binary, and `F_0` is an explicit rational polynomial of
fixed degree at most `d>=1`. Equalities may be represented directly or by two
inequalities. The residual feasible set is fixed: the continuous core changes
costs, not feasibility, supplies, or right-hand sides. Substitute fixed residual
coordinates and reject empty integer intervals. The initial oracle call detects an empty
`Y`; assume below that `Y` is nonempty.

Supply `L>0` with

```
partial_ii F_0(v,z)<=L,   i in C, (v,z) in [0,1]^k times Y.  (1)
```

A bound valid on the full real bounding box suffices. Its size and any
required verification record are part of the input length `I`, together with
a rational noise half-width `sigma>0` and the original instance.

The oracle assumption is precise: for every rational core vector in
`[0,1]^k`, rational
linear cost perturbation, and tightened integer coordinate bounds on `z`,
an algorithm returns an exact rational optimal value and an attaining integer
point, or reports infeasibility, in polynomial bit time in the query length.
The exponent is independent of `k`. Exact values are rational because the
core is rational and every residual point is integral. A proof record can
verify oracle calls by this same polynomial algorithm; a separate compact
optimality certificate is sufficient but not required.

There is one base-computable power of two `M`, with `log M=poly_d(I)`, such
that independent uniform coefficients on

```
{-sigma+2sigma j/(M-1): j=0,...,M-1}                         (2)
```

admit exact global optimization over `X` on every draw, with expected bit work
and expected proof-record size

```
[8^k [3+(1+k/2)L/(2sigma)]^k+c_d^k] poly_d(I),              (3)
```

Here `c_d` is a fixed effective constant from the
[deterministic polynomial box solver](polynomial-component-primitive-limit.md).
It depends only on the fixed degree and exact-arithmetic implementation.
An explicit conservative [implementation budget](strong-field-component-polynomial.md#7-an-effective-component-budget-constant)
is available; it does not require a new promise on the instance.

Thus the result is expected FPT in the core dimension and numerical ratio
`L/sigma`. Residual dimension, graph width, and the numerical cardinalities
of the native integer intervals do not enter the exponential factor. They
enter the polynomial input factor and the logarithms of the precision
budgets below. The polynomial factor includes the exact recourse cost.

The output is an exact integer residual point and an exact real-algebraic
core optimizer and value. The coordinates are rational polynomial maps of
one isolated real root, so they belong to the same deterministically selected
optimum. Separate nonzero integer defining polynomials and rational isolating
intervals for each coordinate and the value can also be computed within the
same bound. Their total encoding length is at most `c_d^k poly_d(I)` on every draw,
and they support `t`-bit refinement in `c_d^k poly_d(I+t)` bit work. A rare
same-draw fallback covers every tie and degeneracy; its search and proof trace
can be large, but their expectations obey (3). For a quadratic objective,
both branches can instead return exact rational optimizers and values.

An [optional implicit-output variant](native-integer-recourse-implicit-closure.md)
removes the additional `c_d^k` processing term and gives polynomial-time
evaluation of the usual compact convex-patch descriptor. It uses additional
active-gradient and local Hessian tests. Those tests are not needed for the
expanded-output theorem proved here.

If `k=0`, call the exact integer oracle directly; no noise is needed. If a
valid core curvature bound is nonpositive, coordinatewise endpoint
interpolation gives an exact solution using at most `2^k` recourse calls,
also without noise. Below `k>=1` and `L>0`. No growth or label-gap promise
is supplied, and the theorem concerns the sampled objective.

## 2. Core search and expected state count

Condition on residual noise and write

```
V(v)=min_(z in Y) F_gamma(v,z).
```

The fixed feasible set is essential. Its finite lower envelope, after
subtracting `gamma_C'v`, has upper coordinate curvature `L`, including at
nonsmooth label changes. Each rational query gives an exact value and a
feasible completion.

Use the nested dyadic core search of the
[exact recourse theorem](smoothed-box-stable-recourse.md), with side length
`h_j=2^(-j)` and correction

```
e_j=kLh_j^2/8.
```

Retain a generated cell when its least corner value minus `e_j` is at most
the current best queried value `U_j`. All original optimizer cells survive,
`U_j-f*<=e_j`, and each retained cell has a corner of value at most
`f*+2e_j`. Let `D_j` be the coordinate hull of the retained cells, and let
`(c_j,z_j)` be a best queried core corner and its exact completion. In
particular `c_j` belongs to `D_j`.

For each near-optimal interior grid tuple, its two coordinate neighbors
confine the corresponding core noise coefficient to an interval of length

```
Lh_j+4e_j/h_j=Lh_j(1+k/2).
```

All interval endpoints depend on the deterministic tuple and conditioned
residual noise, not on the core noise. Independent scalar probabilities,
the two endpoint positions per coordinate, and `Mh_j>=1` give expected
near-optimal tuple count at most

```
[3+(1+k/2)L/(2sigma)]^k.                                   (4)
```

Cell incidence, children, and queried corners contribute at most `8^k`
per level. Only retained lists are generated; the full fine grid is not
materialized. This proof is unchanged by the number or geometry of the
integer feasible labels.

## 3. A competing-label certificate valid on every draw

Compute a rational base bound

```
G>=max{1, sup_(v,z) sum_(i in C) |partial_i F_gamma(v,z)|},   (5)
```

uniform for all noises in `[-sigma,sigma]^(k+r)` and for the real bounding
box of `X`. Monomial bounds give `G` of polynomial bit length. Every
conditional optimum over a fixed subset of residual labels is
`G`-Lipschitz in core infinity distance.

At a best queried corner `c`, with exact integer completion `z`, use at
most `2r` further oracle calls: for every coordinate `i`, impose either

```
z'_i<=z_i-1,          or          z'_i>=z_i+1,               (6)
```

together with the original residual constraints and bounds. Empty calls
have value `+infinity`. Their union is exactly `Y` minus the single label
`z`, regardless of how strongly the residual coordinates are coupled.
Let `V_other(c)` be the least of their exact optimal values. If there are
no other labels, it is `+infinity`.

For `D=D_j` let `w=max_i width_i(D)`. The test

```
V_other(c)-V(c)>2Gw                                       (7)
```

certifies that `z` is the unique conditional winner at every `v in D`.
Indeed the best other-label value there is at least `V_other(c)-Gw`,
whereas the feasible same-label value is at most `V(c)+Gw`. Thus every
original global optimizer lies in `D times {z}`.

The restrictions in (6) are closed integer restrictions with a full unit
gap. No continuous derivative test is applied to an integer variable, and
no enumeration of labels is used on this branch. Feasible upper values
for the excluded problems would not suffice: (7) needs their certified
global lower values, supplied here by exact recourse.

## 4. Exact algebraic completion in the small core

Once (7) passes, the slice `[0,1]^k times {z}` contains an original global
optimizer and is a subset of the original feasible domain. Consequently

```
min_(v in [0,1]^k) F_gamma(v,z)=f*.
```

Thus solve this entire core box exactly. The core polynomial need not be
convex, its minimizer need not be unique, and no stationarity or Hessian
promise is used. The reviewed
[joint critical-limit construction](polynomial-component-primitive-limit.md)
returns an exact optimizer for every rational polynomial on such a closed
box. Its deterministic candidate order chooses one attaining point;
lexicographic minimality among all global optimizers is not required.

After substituting `z`, combine coefficients into at most `binom(k+d,d)`
monomials. Their binary heights are polynomial in `I+log M`: native labels
have input-bounded bit length, and degree is fixed. The solver enumerates
the `3^k` continuous faces and uses a monic pure-power deformation of each
stationary system. Characteristic-polynomial coefficient derivatives recover
all coordinates of a finite critical limit from one common scalar root.
This gives complete candidates even for nonradical or positive-dimensional
original stationary sets. Feasible extra candidates are harmless. Its exact
work and coefficient-height exponents are polynomial in the new rational
input bits, with a constant-base exponential only in `k`.

The resulting exact construction and `t`-bit evaluation cost is

```
c_d^k poly_d(I+log M+t).                                   (8)
```

The output is one isolated root `alpha` and coordinate polynomials `r_i`
with `v_i=r_i(alpha)`. A univariate resultant for any `r_i(alpha)` or the
objective value supplies its separate defining polynomial, if requested.
Squarefree root isolation and matching preserve the same bound, after
fixing a sufficiently conservative effective `c_d`. These operations use
one common root rather than a compositum of independent coordinate fields.
No separation from values at other residual labels is needed in the final
representation. Construction occurs once after a successful label test,
which explains the additive `c_d^k` term in (3).

For stopping analysis only, suppose full Euclidean point growth holds on
`X` at its unique optimizer `a=(a_C,a_R)` with constant at least `g_0>0`.
Set `A_0=2+kL/g_0`. Retained witnesses imply that every point of `D_j` lies
within `A_0h_j` of `a_C` in infinity norm, and
`||(c_j,z_j)-a||^2<=e_j/g_0`. If

```
h_j<=min{1/(4A_0), g_0/(16GA_0)},                           (9)
```

then `e_j<=g_0/8` and `z_j=a_R`, since distinct integer labels have
Euclidean distance at least one. Every other label at `c_j` has objective
at least `f*+g_0`, whence

```
V_other(c_j)-V(c_j)>=g_0-e_j>=7g_0/8,
2G max_i width_i(D_j)<=4GA_0h_j<=g_0/4.                    (10)
```

The sound label test passes. This forces exact completion by a base-only
cutoff; growth is used only for this rate argument. On any draw where (7)
passes, algebraic completion is sound even when core minimizers are tied
or form a positive-dimensional set.

## 5. One finite law and a same-draw label-enumeration fallback

Let

```
n=k+r,     R_Z=product_i(u_i-l_i+1),
S=k+sum_i(u_i-l_i).
```

These numbers can be exponentially large, but their binary lengths are
polynomial in `I`. The [finite-noise growth proof](polynomial-finite-noise-tails.md)
extends to `X` and gives a base-computable `C_tail=2^{poly_d(I)}` with

```
Pr{g_*<epsilon}<=S epsilon/sigma+2n C_tail/M.                (11)
```

Here `g_*` is the full point-growth modulus, set to zero on nonunique
draws. The continuous-noise estimate uses only compactness, the coordinate
widths, and the linear perturbation, not product feasibility.

The scalar-section format does not hide a double exponential in a large
integer range. Describe each integer coordinate by the disjunction
`z_i=l_i or ... or z_i=u_i`, and include the residual linear inequalities.
The number of atoms is bounded by
`s_0=O(I+sum_i(u_i-l_i+1))`, hence `log s_0=poly(I)`.
The good-growth predicate is still one existential point block followed by
one universal competitor block, with one free noise scalar and fixed degree
`max(d,2)`. The reviewed fixed-block elimination bound is
`(s_0 max(d,2))^{O((n+1)^2)}`. Its logarithm is polynomial in `I`.
The sampler computes this format bound in binary; it does not materialize
the label disjunction or perform this elimination on each draw.

For a completely correct fallback, enumerate the `R_Z` candidate labels,
reject infeasible ones, and use the exact small-core solver of section 4
for every remaining label. Compare their algebraic optimum values exactly
and keep an attaining point for a least one. Each compared value has degree
at most `c_d^k` and coefficient height at most
`c_d^k poly_d(I+log M)`, after fixing the constant conservatively. Stream
through the labels and keep the current least value. Pairwise comparisons
use univariate gcds and isolation of the squarefree product of the two value
polynomials. Their work is polynomial in those degrees and heights, hence
still has a constant base in `k`; it is included in `c_d^k` by the component
solver's mixed-label bound. No compositum of all compared values is formed.
Thus a base-computable budget
`B=2^{poly_d(I)}>=2` bounds this search and its proof record by

```
B(I+log M+1)^e_d.                                          (12)
```

For example, `B` may be chosen as `R_Z` times a sufficiently large
effective parameter-only multiple of `c_d^k`; `e_d` is a fixed polynomial
exponent. Substituting a native label creates
only polynomial-length coefficients because degree is fixed. The fallback
returns one winning label and its small-core representations, not the
collection of all tested labels. Re-isolating the selected roots of their
own polynomials, if necessary, gives the all-draw output size and refinement
bounds in section 1. A tiny gap between different labels can increase search
work, but not this final representation size.

For quadratic objectives, enumerate the at most `3^k` core stationary faces
per label, as in the [quadratic recourse fallback](smoothed-box-stable-recourse.md).
A global minimizer on a smallest core face has either no free variable or
a nonsingular free Hessian: otherwise a flat stationary direction reaches
a smaller face. All candidates are rational with polynomial coordinate bit
length. This gives exact rational outputs on both the regular and fallback
branches, including degenerate optima.

Choose, before sampling,

```
rho=1/(4B),       g_0=rho sigma/(2S),       A_0=2+kL/g_0.
```

Let `J>=0` be the first level satisfying (9), and choose the least power of
two

```
M>=max{2,2^J,4n C_tail/rho}.                                (13)
```

All quantities preceding `M` are base-only; `J,log M=poly_d(I)`.
Equation (11) gives failure probability at most `rho=1/(4B)`. If the label
certificate has not succeeded by level `J`, invoke (12) on the same draw.
Expected fallback work and proof-record size are polynomial. Every atom
remains correct; no draw is rejected or resampled. Only the growth tail is
used: no active-gradient, reduced-cost, Hessian, or label-isolation margin
is assumed as input or charged as a separate failure event.

## 6. Bit work, evaluation, and the constrained recourse scope

At each level, every rational core corner and every tightened bound has
polynomial encoding length. Exact oracle outputs are bounded integer labels
and rational polynomial values, also of polynomial bit length. The at most
`2r` competing-label calls and list operations per level cost polynomial work
apart from the actual number of core corner queries. Sum (4) through `J`,
add the one-time exact core solve (8), and add the expected fallback to
obtain (3).

The output fixes the integer residual label exactly. Refine its core
algebraic coordinates and clip rational approximants to `[0,1]^k`; clipping
does not increase their distance from the exact feasible point. This gives
an exactly feasible mixed rational point. A rational gradient bound and the
separate exact-value representation give a certified objective enclosure
and gap. Euclidean accuracy requires only `O(log k)` additional coordinate
precision bits. Refinement of the stored small-core representations costs
`c_d^k poly_d(I+t)` on every draw, independently of how many labels the
fallback examined.

There is a concrete network-flow corollary. Let `Y` be the integer flows
on a fixed directed network with integer supplies and binary-encoded integer
arc bounds, and let the costs have the form

```
F_0(v,z)=phi(v)+sum_a f_a(v,z_a).
```

For every core vector, each univariate cost must be convex on its native
interval. This is a valid supplied premise; when a verifiable proof record
is required, supply a checkable convexity certificate and count its size and
verification cost in `I`. Core fixing, linear noise and tightened integer
bounds preserve that property and the residual feasibility class. The simpler family
`phi(v)+sum_a psi_a(z_a)+v'Bz`, with each `psi_a` convex, permits arbitrary
core-to-arc coupling magnitude without charging that bilinear magnitude to
the core curvature `L`. Convexity of each fixed-degree univariate `psi_a`
on its interval can be checked in polynomial bit time by univariate sign
determination; standard convex quadratic or quartic choices need no such
general check.

Hochbaum and Shanthikumar's [1990 primary paper](../../literature/papers/hochbaum1990-convex-separable-optimization-is-not/original.pdf),
Theorem 4.3 and Algorithm 4.2, printed page 858, give an exact optimal integer
solution for separable convex minimization over a bounded totally unimodular
system. Their scaling construction uses a logarithmic number of stages in
the numerical right-hand-side bound and polynomially many function evaluations
on prescribed grids; each stage is a polynomial-size rational linear program
whose optimal extreme point is integral. A network incidence matrix with
arc-bound unit rows is totally unimodular. At a rational core vector, all
fixed-degree cost evaluations have polynomial bit length. If an internal
grid queries outside an arc's original interval, extend its cost by the
endpoint tangent on each side. This preserves convexity, has rational
polynomial-time evaluations, and changes no feasible objective value.
Thus the algorithm
is an exact polynomial-bit oracle here, with logarithmic capacity dependence.
Changing the integer arc bounds in (6) preserves the premise. This verifies
the oracle required in section 1, so (3) applies to these constrained flows.

The same established oracle also supplies a corollary for a fixed bounded
totally unimodular residual system with integral right-hand side and separable
convex costs. The network case additionally has the short certificate below.
Neither statement covers core-dependent balances, arbitrary nonseparable
integer convex minimization, or a general mixed-integer convex oracle with
unbounded integer dimension.

For a network flow, oracle optimality has a short classical certificate.
At a feasible integer flow `z`, give each available forward residual arc
the unit marginal cost `f_a(v,z_a+1)-f_a(v,z_a)`, including its linear
perturbation. Give each available reverse arc the cost
`f_a(v,z_a-1)-f_a(v,z_a)`. Supply rational node potentials for which every
residual arc has nonnegative reduced cost.

To verify sufficiency, let `z'` be any other feasible integer flow. Its
positive and negative arc differences form a nonnegative integral residual
circulation. Discrete convexity bounds the actual cost difference below by
this circulation's cost at the displayed unit marginals. Summing reduced
costs gives a nonnegative value because potential terms cancel on a
circulation. Thus the supplied flow is globally optimal. Conversely, a
negative residual cycle admits an improving one-unit augmentation, so an
optimal flow has none. Shortest-path distances from an added zero-cost
source then provide the required potentials, of polynomial bit length.
This proves exact value certificates for unrestricted and bound-restricted
calls. It is an optimality test, not a claim that repeated unit augmentation
has polynomial running time.

The [focused prior comparison](../prior-art/integer-convex-flow-recourse-prior.md)
attributes the integer convex oracle, capacity scaling and discrete
optimality mechanisms to established work. It also compares geometric
branching on a small continuous core, smoothed discrete winner gaps, and
the project's separable mixed-recourse result. The additional statement here
is their particular composition into a fixed finite-law expected exact bound
with coupled integer recourse and expanded algebraic output. No publication-
priority claim follows from that focused search.

## 7. Verification

The author ran

```sh
python3 -B research-20261002/new-direction/check_native_integer_recourse.py
```

The [exact-fraction diagnostic](check_native_integer_recourse.py) implements
the common one-dimensional core refinement and competing-label test, followed
by the [optional implicit variant's](native-integer-recourse-implicit-closure.md)
nonlinear Hessian closure, for a two-parallel-arc flow. The objective has a
nonconvex quartic core and convex quadratic arc costs. Its conditional integer
winner changes with the core, and the final core optimizer is an interior
root of a cubic. The fixture oracle uses the exact nearest-integer solution
of its convex scalar flow problem; it does not enumerate capacities or
implement the general Hochbaum--Shanthikumar algorithm.

For capacity `7`, closure occurred at level 11 after 53 generated cells and
118 exact recourse calls. For capacity `2^80+7`, closure occurred at level
86 after 409 generated cells and 849 calls. Both runs retained at most four
cells at any level. All 967 calls passed exact residual-network potential
checks; both tied-label guards correctly prevented premature exclusion.
The final patches were checked against the fixture's separate analytical
description of its conditional winner regions and unique global minimum.
The checker also verifies explicit core and value root representations,
`4v^2-2v-1=0` and `256t^2-176t-1=0`, with isolating intervals; and a separate
flat-core example where the label test passes but no positive-Hessian closure
is possible. Whole-core algebraic completion correctly handles that example.
These are deterministic mechanism checks, not implementations of general
quantifier elimination, the full finite perturbation law, or the fallback.

The [independent review](../reviews/smoothed-native-integer-recourse-review.md)
read the revised primary theorem and optional companion, checked the
whole-core completion and parameter-only algebraic format, and independently
verified the source-backed flow oracle and marginal-potential certificate.
Its separate diagnostic passed 1,215 competing-label tests, 2,430 restricted
solves, 5,040 endpoint comparisons for 420 accepted labels, strict-gap and
excluded-upper-value failure guards, and precision budgets with a 200-bit
native range. It also checked cubic coordinate/value refinements at 8, 32
and 96 bits. The reviewer did not rerun the author's flow refinement test.

Scoped local-link, code-fence, whitespace and Python-syntax checks passed,
as did topic-scoped `git diff --check`. No index edit, project-wide
verification or CI inspection is part of this note.
