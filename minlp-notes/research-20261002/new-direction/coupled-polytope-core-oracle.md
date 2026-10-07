# Selected optimal core coordinates on a coupled rational polytope

Date: 2026-10-02. Status: passed
[fresh actual-file review](../reviews/coupled-polytope-core-oracle-review.md).
Its explicit interfaces now have completed reviews of the
[value theorem](../reviews/coupled-polytope-core-value-review.md) and
[convex/fallback interface](../reviews/convex-polytope-value-interface-review.md).
This adapts the reviewed
[box-core Cauchy certificate](core-only-noise-core-oracle.md).
The changes are a compact-domain projected growth proof, feasible
in-cell witnesses, and rational LP repair on exact fallback.

## 1. Inherited input and precise output

Let `P` be a nonempty bounded rational polytope, with continuous
coordinates `(v,z)`, core `v in [0,1]^k`, `k>=1`, and a supplied rational
bounding box for the residual coordinates `z`.
Let `F_0` be an explicit rational polynomial of fixed degree `d`.
Supply a verified rational `alpha>=0` for which

```
F_0(v,z) + (alpha/2) ||v||_2^2 is convex on P.            (1)
```

The base length `I` includes all polynomial and polytope data, the
rational noise half-width `sigma>0`, and certificate data. As in the
value theorem, its parameterized bound presumes polynomial certificate
verification; otherwise charge actual verifier cost separately. Convexity
is only required on `P`, including its relative affine hull.

For independent uniform finite-grid core noise define
`F_gamma=F_0+gamma'v`. The projected core domain need not be the full
box, and no continuity assumption on a partially minimized value is used
below. Let `x_gamma^lex` be the global lexicographic optimizer with core
coordinates ordered first, and let `a_gamma` be its core.

Using the [coupled-polytope value theorem](coupled-polytope-core-value-oracle.md)
interfaces stated in Section 3, one base-computable finite noise law with
`log M=poly_d(I)` has the following property. On every draw, for every
`q>=0`, an evaluator returns a rational `x_q=(v_q,z_q) in P` and rational
`ell_q,U_q` with

```
ell_q <= min_P F_gamma <= U_q=F_gamma(x_q),
U_q-ell_q <= 2^(-q),
||v_q-a_gamma||_2 <= 2^(-q).                             (2)
```

Expected bit work and proof/output size are

```
f_d(k) (1+alpha/sigma)^k poly_d(I+q),                    (3)
```

with a polynomial exponent independent of `k,m`. A single random work
factor bounds every precision query simultaneously. Residual coordinates
are only required to be feasible and support the reported objective gap;
they need not approximate any selected exact residual optimizer.

## 2. Projected growth on a compact coupled domain

For a coefficient `gamma`, define `g` as the supremum of the constants
`t>=0` for which some `(a,z_0) in P` satisfies

```
F_gamma(v,z)-F_gamma(a,z_0) >= t ||v-a||_2^2
                                      for every (v,z) in P.    (4)
```

This definition permits residual ties. Distinct optimal core projections
force `g=0`. If the core projection is a singleton, use `g=+infinity`.
For any fixed positive `t`, compactness and continuity show that the set
of coefficients satisfying (4) is closed: take a convergent subsequence
of the witnessing points and pass every competitor inequality to the
limit. Thus the bad-growth event is measurable, even without continuity
of a projected value function.

The reviewed [proximal tail proof](proximal-growth-tail.md) applies with
one specific modification. For `epsilon>0` form the finite convex function
on coefficient space `R^k`

```
H_epsilon(c)=max_(v,z) in P
                  [c'v-F_0(v,z)+epsilon ||v||_2^2].       (5)
```

The maximum is attained because `P` is compact. Every maximizing core
projection is a subgradient, and all subgradients lie in `[0,1]^k`.
At a differentiability point of `H_epsilon`, all maximizing core
projections are therefore the same `a`; their residual coordinates may
still differ. Choosing any corresponding residual witness and setting
`gamma=-(c+2epsilon a)` gives (4) with `t=epsilon` for the convention
`F_gamma=F_0+gamma'v` used here. Equivalently, the coefficient of the
negative linear tilt is `c+2epsilon a`, as in the proximal proof.
Reflection does not change the symmetric uniform sampling law.
The proof requires uniqueness of this
subgradient/core, not uniqueness of the full maximizing point.

The proximal map consequently has the same bounded coordinate
displacements and the same divergence bound for the bad event.
Integrating its coordinate variations against independent uniform
densities on intervals of half-width `sigma` gives

```
Pr_cont(g<t) <= k t/sigma.                              (6)
```

All remaining steps of the reviewed proof concern the convex function
on coefficient space and are unchanged. This argument works more
generally for a continuous objective on any compact full-variable domain
whose core coordinates have widths at most one.

The exact good-event formula is (4), written with one existential
full-variable witness and one universally quantified competitor guarded
by membership in `P`. It has two quantified blocks, linear domain
predicates, and fixed-degree objective atoms. Fixed-block elimination
therefore gives a base-computable scalar-section constant
`C_g=2^(poly_d(I))`, uniformly over threshold values and coefficient
heights. Marginal replacement to the finite noise law gives

```
Pr(g<t) <= k t/sigma+C_g/M.                             (7)
```

No residual perturbation, interiority, or projected continuity enters
either (6) or its finite-law transfer.

## 3. The value theorem interfaces and hull certificate

Set `alpha_+=alpha+sigma>0`. Increasing the shift preserves (1) and
enlarges `1+alpha/sigma` only by a constant factor. On a dyadic core cell
`C=prod_i[l_i,u_i]` of side `h`, the value algorithm minimizes the
convex model

```
G_C(v,z)=F_gamma(v,z)
                 +(alpha_+/2) sum_i (v_i-l_i)(v_i-u_i)
```

over `P` intersected with the cell. Empty cells are certified and removed.
On this domain `0<=F_gamma-G_C<=e_h`, with
`e_h=alpha_+ k h^2/8`. The certified convex oracle gives a lower bound
`LB(C)` and a feasible witness in this cell whose true objective is at
most `LB(C)+2e_h`. These statements follow from the model error and an
oracle interval of width `e_h`.

The inherited algorithm uses the best true feasible objective `U` and
retains exactly cells with `LB(C)<=U` after its final incumbent update.
It proves the interval `[U-2e_h,U]` and a feasible witness of true gap at
most `4e_h` in every retained cell. Its all-scale count interface supplies
an extended random factor `W>=1` with

```
generated cells at every level <= c(k) W,   c(k)=4^k,
Pr(W>s) <= a_k/s+C_a/M,    s>=1,
a_k=(180 k^3)^k (1+alpha_+/sigma)^k,
log C_a=poly_d(I).                                      (8)
```

The all-draw fallback has cost `B_0 poly_d(I+b+q)` with
`B_0=2^(poly_d(I))`. The value theorem owns the proof of (8), the
cell-model oracle, and their bit bounds; they are explicit interfaces
of this addendum, not additional hypotheses on realized growth.

Every optimal core remains covered because a cell containing an optimal
full point has `LB(C)<=min_P F_gamma<=U`. A feasible incumbent need not
be a corner: when first inserted it lies in the cell that produced it.
If it remains best at later levels, a child containing its core is
nonempty because that same full point is feasible there. Every containing
cell has `LB(C)<=F_gamma(x_inc)=U`, so it survives the final pass.
An improved incumbent is handled at its own insertion. Thus the retained
coordinate hull contains both every optimal core and the current
incumbent core, exactly as in the box certificate.

Use the base choices

```
B>=max(2,B_0),   g_0=sigma/(2kB),
M=least power of two >=max(2,2B max(C_a,C_g)),
D=4k+k^2 alpha_+/g_0.                                   (9)
```

On `g>=g_0`, the retained feasible witness of gap `4e_h` lies within
`h sqrt(k alpha_+/(2g_0))` of the unique optimal core. It can be anywhere
in its cell; every other point in that cell is still within `h` in
each coordinate. Hence the retained hull's Euclidean diameter is at
most `Dh`, by the identical calculation in the box addendum.

At the first level `J` with `2e_J<=2^(-q)` and `D2^(-J)<=2^(-q)`,
test the actual squared hull diameter against `2^(-2q)`. Passing certifies
(2) for the current feasible incumbent, without trusting any growth
claim. Failing triggers the fixed-selector fallback. Failure at any
precision implies `g<g_0`, whose probability is at most `1/B` by (7).
This is one event across all future queries, not a level-wise union.

Keep the inherited pre-generation cell cap `c(k)B` and near-linear
list work. The only new ordinary work is the linear hull pass and
`J=poly_d(I)+O(q)` terminal depth. One uniform random work bound is

```
[f(k) min(B,W)+B_0 1_{W>B or g<g_0}] poly_d(I+q).        (10)
```

The weak-tail integral from (8) pays for the first term and its cap
fallback. The extra event contributes at most `B_0/B<=1`. This proves
(3), conditional on the stated value interfaces.

## 4. Fixed selector and exact feasibility on fallback

The [polytope fallback interface](convex-polytope-value-interface.md)
uses the same core-first lexicographic scalar singleton formulas as
the generic box fallback, replacing box membership by `P`. The selected
point is independent of requested precision; its coordinate and value
representations have the stated base-only exponential budget.

For error `epsilon=2^(-q)`, obtain a rational approximation `w` to that
exact selected point with max-norm error at most

```
delta=min(epsilon/(4(k+1)),epsilon/(4G)),
G>=max(1,sup_P ||grad F_gamma||_1).                     (11)
```

A rational coefficient bound on the supplied box gives
`log G=poly_d(I+b)`. Restore exact feasibility using the interface's
rational LP feasibility problem

```
find x in P with |x_i-w_i|<=delta for every coordinate.  (12)
```

The exact selected optimizer proves that this intersection is nonempty.
Any rational LP solution `x_q` therefore satisfies
`||x_q-x_gamma^lex||_infinity<=2delta`. This repair works when `P` is
lower-dimensional. Box clipping alone would not suffice.

The core distance is at most `2sqrt(k)delta<=epsilon`, and the objective
gap is at most `2Gdelta<=epsilon/2`, since the connecting segment lies
in `P`. Refining the exact global value to an interval of width
`epsilon/2` supplies the remaining half of (2). Rational LP work and
these extra precision bits preserve the base-separated fallback bound.

The ordinary hull outputs and this fallback thus approximate one fixed
globally optimal core on every draw, including tied-core atoms. No
efficient residual-coordinate extraction is implied.

## Verification status

The author read the actual coupled value theorem, polytope value/fallback
interface, and original proximal proof. The compact-domain modification is written
explicitly above; it does not apply the continuous-box value lemma to
an unverified projected function. The fresh review passed the composition;
the separate actual-file reviews now validate all its explicit value
interfaces. The composition review caught and reread a sign
clarification: the plus-noise convention requires
`gamma=-(c+2epsilon a)` in the proximal substitution. The symmetric-law
tail is unchanged. The value-theorem author's diagnostic
`python3 -B research-20261002/new-direction/check_coupled_polytope_cells.py`
includes 81 exact error-box repairs through 200-bit accuracy, checking
simultaneous core error and objective enclosure on coupled equality
fixtures. That author-owned run was not repeated for this addendum.
A targeted inline Python check passed this addendum's local links,
delimiters, fences, whitespace and control characters; a scoped
`git diff --check` also passed. No new count or probability fixtures,
index edits, project-wide tests, or CI checks were run for this addendum.
