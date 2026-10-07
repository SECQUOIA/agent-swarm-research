# Expected exact sparse polynomial optimization with binary order variables

Date: 2026-10-02. Status: passed
[fresh independent review](../reviews/smoothed-mixed-order-review.md).
This note extends the [continuous order-polytope theorem](smoothed-sparse-order-polynomial.md).
No publication-priority or practical-performance claim is made.

Binary variables can be included in the order system without an integer-dimension
parameter. The main change is to keep endpoint groups fixed when transporting
conditional feasible points. A transported point gives a feasible upper support
for the conditional objective; it need not describe the whole fiber at an
endpoint. The exact-output certificate is applied only after pruning has fixed
every binary variable.

## 1. Statement and scope

Partition the coordinates into a continuous set `C` and a binary set `Z`, with
`N=|C|`, `s=|Z|`, and `n=N+s`. Let

```
X={x in [0,1]^n : x_i<=x_j for each specified edge i->j,
                   x_i in {0,1} for i in Z},
F_0=sum_B f_B,                 Hess F_0(x)<=H I on [0,1]^n.
```

The factors are explicit rational polynomials of fixed degree at most `d`,
`H>=1` is a supplied valid full Hessian bound, and a supplied tree decomposition
covers every factor scope and every order edge. Write `p` for its largest bag
size and `q` for the largest number of continuous coordinates in a bag. Cycles
are allowed. The zero vector is feasible. Let `I` contain the original input,
the decomposition, `H`, and a rational noise half-width `sigma>0`. If the proof
record must certify the curvature bound, include a verifiable certificate and
its verification cost in `I`, as in the continuous theorem.

There is a base-computable power of two `M`, with `log M=poly_d(I)`, such that
independent uniform coefficients on the single fixed rational grid

```
{-sigma+2sigma k/(M-1): k=0,...,M-1}
```

admit exact optimization of `F_gamma=F_0+gamma'x` over `X` on every draw, with
expected bit work

```
C_0^p q! (q+1) [2+3NH/(4sigma)]^q poly_d(I).                 (1)
```

Here `C_0` is absolute. The number of binary variables is unrestricted. For
fixed `p`, this is polynomial when `H/sigma` is polynomially bounded. It is
not an FPT bound in `q` or `p`. The usual exact output is a fixed binary
assignment and a rational description of a strongly convex continuous
order-polytope patch whose unique minimizer is a global optimizer. It supports
feasible rational point approximation and certified objective enclosures in
`poly_d(I+t)` bit work for `t` requested accuracy bits. The global pruning proof
trace has expected size and verification work bounded by (1), although its
size need not be polynomial on each draw. A rare same-draw algebraic branch
covers all ties and degeneracies; its work and output/evaluation costs have
polynomial expectations.

If `N=0`, ordinary finite-state tree dynamic programming solves the instance
exactly in `C_0^p poly_d(I)` work for any rational coefficients, without noise.
Below assume `N>=1`. Only binary integer variables are covered: transporting
arbitrary integer levels would require additional fixed knots and a different
count. The theorem solves the sampled objective, not the original objective.

## 2. Feasible rounding and the retained witness

Use the sparse cell lists, exact rational min-marginal dynamic program, and
nested bag whitelists of the [continuous theorem](smoothed-sparse-order-polynomial.md).
Assign order constraints and binary membership to containing bags. Continuous
coordinate cells have width `h_j=2^(-j)`. Initially a binary coordinate has the
single physical cell `{0,1}`, with two endpoint states. At every level `j>=1`
its cells are the singletons `{0}` and `{1}`. Binary singleton cells are never
refined further. There are at most `2^p` children per bag cell.

For a feasible point, common-threshold rounding of all coordinates by

```
Y_i=h_j(floor(x_i/h_j)+1{U<frac(x_i/h_j)}),   U uniform [0,1],
```

fixes every binary coordinate and preserves every order inequality. It stays
in each incident continuous cell containing the point, and in its binary
cell. Correlation is harmless because the supplied bound is a full Hessian
bound. Mean preservation gives

```
E F_gamma(Y)<=F_gamma(x)+E_j,       E_j=NHh_j^2/8.            (2)
```

Binary coordinates have zero variance. Let `m_j` be the grid minimum and
`U_j` the best feasible value. For a bag cell let `q_cell` be the least
min-marginal among its allowed corners, and retain it if
`q_cell-E_j<=U_j`. The fixed-cell rounding argument proves, without any
growth assumption, that all global optimizers survive and

```
f*<=U_j<=m_j<=f*+E_j.
```

Every retained cell has one globally feasible corner witness `y` with

```
F_gamma(y)=q_cell<=f*+2E_j.                                 (3)
```

No independent rounding of ordered coordinates is used. The common threshold
is an analysis device, not part of the sampled perturbation law.

## 3. Endpoint-preserving fiber transport

Fix a bag `B`, with `B_C=B intersect C`, containing `c` continuous and
`z` binary coordinates. Fix its binary
assignment `b`, and condition on all noise outside the continuous bag
coordinates. Define the original conditional value

```
V_b(v)=gamma_(B intersect Z)'b
       +min {F_0(v,b,u)+gamma_out'u : (v,b,u) in X}.
```

The fixed bag-binary noise contribution is included in `V_b`; it has no
effect on any directional comparison below. Compactness gives an attaining conditional
point at every feasible tuple.

Partition continuous bag tuples by the relative interiors of the faces of
the `c!` standard order simplices. Each face specifies equal-coordinate
groups, their order, and which groups are fixed at `0` or `1`. For a tuple
`v` in one such relative interior, take any attaining outside point `u`.
List its distinct continuous bag knots, together with `0` and `1`:

```
0=r_0<r_1<...<r_k<r_(k+1)=1.
```

For any `w` in the closed same face, let `s_l` be its corresponding group
values, with `s_0=0,s_(k+1)=1`. The nondecreasing piecewise-affine scalar map
`T_w` sends `r_l` to `s_l`. Apply it to every coordinate of `(v,b,u)`.
It maps the bag coordinates to `(w,b)`, preserves all order inequalities,
and fixes every binary coordinate because it fixes both endpoints. Thus it
gives a feasible full point `x(w)` for the original mixed domain.

For a fixed original coordinate in `[r_l,r_(l+1)]`, its image is
`(1-lambda)s_l+lambda s_(l+1)`, with a fixed `lambda in [0,1]`.
Consequently `x(w)` is affine in `w`. Each moving row has nonnegative
coefficients summing to at most one. There are at most `N` moving rows, so
the squared operator norm of this affine map is at most `N`.

The transported objective is a feasible upper support for `V_b`, equal to
`V_b` at `v`. Its Hessian is bounded above by `NH I`. In particular, for
any face direction `a` such that `v+ha` and `v-ha` belong to the closed face,

```
V_b(v+ha)+V_b(v-ha)-2V_b(v)<=NH h^2 ||a||^2.                (4)
```

This proof does not assert equality between a transported fiber and the
entire endpoint fiber. New binary assignments can become feasible at a
boundary. For example, under `v<=z`, `z` binary, minimizing `z` gives value
one for `v>0` and zero at `v=0`; transport of the interior winner still
provides a valid upper support at zero. Also, a group already fixed at zero
cannot be moved into the interior while preserving binary feasibility.
Faces keep these endpoint groups separate.

## 4. Expected count, with only continuous directions in the exponent

Consider feasible grid tuples with

```
V_b(v)+gamma_(B_C)'v<=f*+eta h^2,       h=1/r.
```

For a `k`-dimensional standard simplex face, its ordered zero-one vertices
have successive differences `a_1,...,a_k` with disjoint nonempty supports.
These supports contain only continuous bag coordinates, and
`||a_l||^2<=c`. At every relative-interior grid point, both `v+ha_l` and
`v-ha_l` lie in the closed face: all distinct knots and endpoint gaps have
length at least `h`. They are feasible by the transport construction,
even if the original feasible projection is not convex.

For these particular directions, the transport has a sharper bound than
its general operator norm: every entry of its derivative along `a_l` lies
in `[0,1]`, since a moving row has nonnegative coefficients of sum at most
one and `a_l` is a zero-one vector. Only `N` rows move. Thus the squared
norm of the transported direction is at most `N`, and the upper support's
second derivative along it is at most `NH`, independently of the group's
size. Comparison with the global optimum at the two points confines
`gamma_(B_C)'a_l` to a fixed interval of length at most

```
(NH+2eta)h.                                                (5)
```

The interval is determined by the conditioned noise and the fixed tuple,
not by the unconditioned continuous bag noise. Choose one noise coordinate
from each disjoint support and condition on all the others. Independence
gives a product of `k` scalar interval probabilities, each at most
`(NH+2eta)h/(2sigma)+1/M`.

A `k`-face has at most `binom(r-1,k)<=r^k/k!` relative-interior grid points.
There are `binom(c+1,k+1)` such faces per simplex and at most `2^z` bag binary
assignments. Consequently, with

```
A_h=(NH+2eta)/(2sigma)+1/(Mh),
```

the expected number of near-optimal bag tuples is at most

```
2^z c! sum_(k=0)^c binom(c+1,k+1) A_h^k/k!
   <=2^z c! (c+1)(1+A_h)^c.                               (6)
```

Infeasible tuples are simply omitted; no description or enumeration of
their mixed fibers is needed. Formula (6) also covers `c=0`, with its
natural value `2^z`. Using `eta=NH/4` from (3), and `Mh>=1`, gives

```
2^z c!(c+1)[2+3NH/(4sigma)]^c.                             (7)
```

Every corner belongs to at most `2^p` cells. The child and corner factors
are also at most `2^p`. Summing (7) over bags and levels gives (1), apart
from the polynomial factors established below. The probability calculation
uses original conditional fibers and deterministic full-grid tuples. It
does not condition on earlier pruning decisions.

## 5. Exact closure after fixing the binary assignment

Form coordinate hulls by intersecting projections of all retained incident
bags. They contain all original global optimizers. Do not apply a
continuous face certificate until every binary hull is a singleton.
Once that holds, fix the corresponding assignment `b`. The remaining
feasible set `P_b` is a continuous order polytope with endpoint fixings.
Propagate the fixed bounds, eliminate forced coordinates, and contract
cycles. All its vertices are zero-one; equivalently, it is a face of the
original continuous order polytope followed by coordinate projection.

The [continuous face certificate](order-polytope-face-closure.md) now applies
to this slice. For clarity, it may be implemented on the original `N`
continuous coordinates, retaining forced equalities. Let `c_j` be their hull
midpoint, `r_j` their largest half-width, and compute valid rational bounds

```
M_1>=max{1,max_(i in C) sum_(k in C) sup |partial_ik F_0|},
T>=max{1,max_(i in C) sum_(k,l in C) sup |partial_ikl F_0|}.
```

Set `g=grad_C F_gamma(c_j,b)` and `delta=M_1 r_j`. Compare `min_(P_b) g'x`
with the same linear program on the opposite zero-one face: for a proposed
order equality `x_i=x_l`, impose `x_i=0,x_l=1`; for a proposed bound, impose
the opposite endpoint. A gap greater than `N delta` certifies that equality
or bound at every original optimizer. Empty opposite faces give infinite
gaps. Edges incident to fixed binary variables become bounds or tautologies.

This is sound because every original optimizer minimizes the objective on
its now-fixed continuous slice. Its gradient exposes a zero-one face of
that slice. It need not expose a face containing an optimizer of a different
binary assignment; those assignments have already been excluded by valid
global pruning.

The order of these operations matters even under strong point growth.
For `0<=x<=z<=1`, binary `z`, the objective
`(x-1/2)^2+10z^2-11z` has mixed optimum `(1/2,1)` and growth modulus one.
Its full gradient there is `(0,9)`. Over the continuous relaxation, the
linear cost gap to the opposite vertex face for `x=z` is nine, which would
falsely certify that equality. Fixing `z=1` first gives the correct
continuous slice gradient zero and avoids this test.

After the certified substitutions, write `x_C=D y+b_C`, with disjoint
coordinate-copy columns in `D`. Intersect hull intervals, propagate bounds,
remove singletons and tautological rows, and contract remaining cycles.
Let `c_y,r_y` be the midpoint and largest half-width of the resulting box.
For a fixed positive rational `g_0`, the exact matrix test

```
Hess_y F_gamma(D c_y+b_C,b)-(NT r_y+g_0)I positive definite   (8)
```

certifies positive Hessian modulus `g_0` throughout the patch. The patch
contains all global optimizers, so its unique constrained minimizer is an
exact global optimizer. If no variable remains, return the verified rational
point. These tests are sound on every draw, independently of growth promises.

## 6. One finite law, binary identification, and closure tails

Let `g_*` denote the full Euclidean point-growth modulus on `X`, set to zero
on nonunique draws. The [finite-noise tail proof](polynomial-finite-noise-tails.md)
applies to this compact semialgebraic domain after adding the order atoms and
the binary equations `x_i(x_i-1)=0`. The number of quantified blocks remains
two, the degree remains fixed, and the number of atoms is polynomial in `I`.
Thus a base-computable `C_tail=2^{poly_d(I)}` satisfies

```
Pr{g_*<epsilon}<=n epsilon/sigma+2n C_tail/M.                (9)
```

For the active-face tail, union over at most `2^s` binary assignments and
apply the [continuous exposure-gap proof](order-polytope-face-closure.md)
on each slice. Put

```
D_0=max(1,d-1),
K=max{1,2^s (m+2n) 2^(m+2n) D_0^N}.
```

Then

```
Pr{g_*>0 and some active finite slice-exposure gap<=tau}
   <=K(tau/sigma+2/M).                                    (10)
```

Indeed a relevant optimizer is a nonsingular stationary root on the
relative interior of its slice's minimal face, by positive point growth.
There are at most `D_0^N` such roots per face. For an active order edge
between continuous coordinates, vary its two noise coefficients at fixed
sum. For an active bound, including one imposed by a binary neighbor, vary
its single continuous coefficient. Stationarity on the face is unchanged,
and the opposite-face gap varies with slope one. Counting finite-grid sum
fibers gives exactly the same `tau/sigma+2/M` bound. Binary coefficients may
be conditioned throughout; they add a constant on each fixed slice. The
union bound does not assume that every slice is globally optimal.

Suppose `g_*>=g_0` and every active finite gap exceeds `tau`. Set

```
A=2+NH/g_0.
```

By (3), the witness of every retained cell is within
`h_j sqrt(NH/g_0)/2` of the unique optimizer. For `j>=1`, binary cells are
singletons. In particular, if `h_j<=1/(4A)`, every retained binary label
equals the optimal label: a different label alone would give distance at
least one. Continuous hulls have radius at most `A h_j` and lie within that
distance of the optimizer. The continuous closure proof therefore applies
as soon as

```
h_j<=min{1/(4A), tau/(4N M_1 A), g_0/(4N T A)}.             (11)
```

It first identifies all active slice equalities and bounds; the restricted
Hessian at the optimizer is at least `2g_0 I`, so (8) succeeds. No positive
slack of an inactive primal order inequality is required.

The [canonical algebraic fallback](polynomial-exact-fallback.md), with the
same domain atoms, has a base budget `B=2^{poly_d(I)}` such that its exact
optimization, output and requested-accuracy evaluation costs are at most

```
B(I+log M+t+1)^c_d.                                       (12)
```

Choose before sampling

```
rho=1/(4B),       g_0=rho sigma/(2n),       tau=rho sigma/(2K).
```

Let `J>=1` be the first level satisfying (11). Choose the least power of two

```
M>=max{2,2^J,4n C_tail/rho,4K/rho}.                        (13)
```

These quantities have polynomial binary length. In particular `J` is
chosen before `M`; the sampling precision does not enter the exponential
fallback prefactor or the scalar-section count. Equations (9) and (10)
each contribute at most `rho` to failure. If closure has not succeeded by
level `J`, use (12) on the same draw. Its probability is at most `1/(2B)`,
which pays for its work and output. There is no resampling.

## 7. Arithmetic, feasible evaluation, and proof output

Every generated state, polynomial value, message, LP and matrix has
polynomial bit length for `j<=J`. There are polynomially many levels,
bags, and LP calls per level. Binary constraints add only exact feasibility
tests and two states per coordinate. The expected sparse table count in
(7), together with the expected fallback, proves (1).

The usual patch contains a fixed binary assignment and an explicitly
strongly convex polynomial on a continuous rational order polytope. Its
evaluation is exactly the [continuous order-patch procedure](smoothed-sparse-order-polynomial.md):
relative affine-hull reduction, rational interior-ball data, certified weak
convex optimization, and order-preserving repair. Its description is
polynomial in `I`; the accompanying global proof trace has the expected
bound (1). This does not promise short expanded algebraic coordinates.

For the fallback, first identify each binary coordinate of the exact
canonical optimizer by an approximation with certified error below `1/4`.
Round it to its unique binary value. Propagate these fixed endpoint bounds
through the order graph before repairing continuous approximants. Clip
continuous values to the propagated intervals and take predecessor maxima.
This preserves the identified binary labels and all order constraints, and
does not increase infinity-norm error relative to the exact feasible point.
Without the propagation step, a slightly positive approximation of a
continuous predecessor could incorrectly move a binary zero. Rational
gradient bounds and the exact-value enclosure provide a certified objective
gap. Euclidean accuracy requires only `O(log n)` additional coordinate bits.

The new ingredients here are the binary-preserving conditional comparison
and its composition with eventual binary identification. Sparse finite-state
dynamic programming, common-threshold order rounding, the continuous
face certificate, and the finite-noise algebraic fallback are reused. This
does not extend to arbitrary affine constraints, arbitrary integer ranges,
or a diagonal-curvature bound in place of `H`.

## 8. Verification

The author ran

```sh
python3 -B research-20261002/new-direction/check_mixed_order_transport.py
```

The [exact-fraction diagnostic](check_mixed_order_transport.py) uses
`0<=v<=w<=z<=1`, with `z` binary, and an indefinite quadratic whose full
Hessian is bounded above by `3I`. It passed 2,187 sampled triangle minima
over three mesh levels, from 729 distinct coefficient draws; 8,019
transported central-difference checks; 100 near-optimal noise-interval
tests; 2,433 near-optimal tuples; three complete-law expectation bounds;
138 common-threshold roundings; and an endpoint jump in the available
binary labels. The global minimum in this fixture is computed from its
analytically exhaustive triangle stationary-face list. The diagnostic does
not implement the full sparse dynamic program, sampler budget, algebraic
fallback, or convex evaluator.

The [independent review](../reviews/smoothed-mixed-order-review.md) read the
actual composition and supporting continuous results. It checked the
endpoint transport, sharper directional constant, conditioning, binary
identification before LP exposure, finite-law budgets, and output contract.
It requested the explicit bag-binary noise constant now present in section 3.
Its separate exact diagnostic passed 238 transports, 42 curvature checks,
40 binary-preserving repairs, the nonconvex projection example, and the
false-exposure example above. The reviewer did not rerun the author's
conditional-recourse diagnostic; the two scopes are distinct.

An inline Python command checked this note's local links, paired code
fences, and trailing whitespace. The topic-scoped `git diff --check`
passed. No external search, project-wide verification or CI inspection
was performed for this note.
