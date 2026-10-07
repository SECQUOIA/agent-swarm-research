# Core-only smoothing with exact integer-flow recourse and interior core optima

Date: 2026-10-02. Status: complete argument with a
[fresh full review](../reviews/smoothed-interior-core-flow-review.md)
finding no substantive gap, plus distinct exact diagnostics. The fixed-core
algebraic and tube interfaces used below have separate reviews.
The constant-base completion and sign-test improvement has a
[separate scoped review](../reviews/constant-base-core-transfer-review.md).

Only the small continuous core needs perturbation when all its global
optimizers are interior. A residual-network certificate allows several integer
flows to remain tied: one selected flow must be optimal throughout a retained
core hull, but need not be its unique optimizer. Base-only algebraic chart
boundaries and a finite-grid tube estimate give the stopping bound. The
[boundary obstruction](core-only-flow-boundary-obstruction.md) explains why
interiority is a substantive restriction of this result.

## 1. Model and conclusion

Let `v in [0,1]^k` be a continuous core, and let `Y` be the nonempty set of
integer flows on a fixed directed network with `r` arcs, `s` nodes, integral
supplies, and bounded integral arc intervals `[l_a,u_a]`. The bounds are
encoded in binary. The core appears only in costs. Let

```
F_0(v,z)=phi(v)+sum_a f_a(v,z_a),
F_gamma(v,z)=F_0(v,z)+gamma'v.                              (1)
```

All displayed functions are explicit rational polynomials of fixed degree
at most `d`. For every core point, each arc cost is convex on its native
interval. Supply a valid core-coordinate upper curvature bound
`partial_ii F_0<=L`, with `L>0`, on the original domain. Uniform conditional
convexity and the curvature bound are valid premises; include any required
verification certificates and their costs in the base input length `I`.
The [exact convex-flow oracle](smoothed-native-integer-recourse.md#6-bit-work-evaluation-and-the-constrained-recourse-scope)
then has polynomial bit cost at every rational core point, including for
binary-encoded capacities. No residual dimension or graph-width restriction
is imposed.

Fix rational `sigma>0`. The additional hypothesis is:

> For every `gamma in [-sigma,sigma]^k`, every globally optimal core point
> of (1) belongs to `(0,1)^k`.

This may be supplied through a checkable sufficient condition. For example,
for some rational `tau>0`, require on every original core face and every
feasible integer flow

```
partial_i F_0(v,z)<=-sigma-tau when v_i=0,
partial_i F_0(v,z)>= sigma+tau when v_i=1.                  (2)
```

Moving inward at a boundary point then improves every attaining fixed-flow
slice. The theorem does not assume a numerical distance of the optimizers
from the boundary, and no reciprocal of `tau` occurs in its state count.
The hypothesis concerns all possible noises in the cube, rather than an
uncertified property of the selected draw.

There is one base-computable power of two `M`, with `log M=poly_d(I)`, such
that independent uniform core coefficients on

```
{-sigma+2sigma j/(M-1):j=0,...,M-1}
```

admit exact global optimization on every draw in expected bit work

```
[8^k [3+(1+k/2)L/(2sigma)]^k+c_d^k] poly_d(I),              (3)
```

Here `c_d` is the fixed effective constant of the reviewed
[polynomial box solver](polynomial-component-primitive-limit.md), including
its exact sign comparisons and refinement. This computational constant is
distinct from the analysis-only elimination bound in Section 4.

The residual costs receive no random perturbation. Arbitrarily many optimal
integer flows may persist on every draw. Output consists of an exact integer
flow and an exact common-root representation of the core coordinates and
value, with separate univariate defining polynomials and isolating intervals
available if desired. Total length is `c_d^k poly_d(I)` on every draw, with
`c_d^k poly_d(I+t)`-time refinement
to `t` bits. The proof trace has the expected bound (3). A same-draw exact
fallback handles every exceptional atom. For quadratic objectives, ordinary
rational outputs are available.

Handle `k=0` by the exact integer oracle directly. The algorithm remains
correct through its exact certificates and fallback even without (2); the
expected bound here requires the stated interiority hypothesis. This is not
a theorem for arbitrary core-boundary optima or for core-dependent flow
balances.

## 2. Search and a non-strict uniform-flow certificate

Let `V_0(v)=min_(z in Y) F_0(v,z)` and `V_gamma=V_0+gamma'v`.
Use the exact core search of the [native-integer theorem](smoothed-native-integer-recourse.md):
dyadic cells of side `h_j`, corner recourse, correction `e_j=kLh_j^2/8`,
and sparse retention. Every original optimal core survives; the best queried
corner has gap at most `e_j`, and each retained cell has a corner of gap
at most `2e_j`. The expected near-optimal grid count is

```
[3+(1+k/2)L/(2sigma)]^k                                    (4)
```

when `Mh_j>=1`. Its proof uses only the independent core noises and the
fixed residual feasible set, so no residual perturbation is needed.

Let `D_j` be the retained core hull. At a best queried corner `c in D_j`,
take an exact optimal integer flow `z`. Form its residual directed graph.
For an available forward arc use the marginal polynomial
`f_a(v,z_a+1)-f_a(v,z_a)`; for a reverse arc use
`f_a(v,z_a-1)-f_a(v,z_a)`. The core-only linear term cancels from these
costs. Add a new source with zero-cost arcs to every original node.

At `c`, optimality gives no negative residual cycle. Compute rational shortest
path distances from the added source. Choose a spanning arborescence of the
tight-edge graph, for example by graph search in that graph. This avoids
cyclic predecessor choices when zero-cost cycles exist. Its source-to-node
paths give polynomial potentials `pi_T(v)` by summing the corresponding
marginal polynomials. They equal the shortest-path distances at `c`.

For every augmented residual arc `e`, form

```
r_e(v)=c_e(v)+pi_tail(v)-pi_head(v).                        (5)
```

These are degree-at-most-`d` polynomials with polynomial-length rational
coefficients. At `c`, every `r_e(c)>=0`. Test exactly that

```
r_e(v)>=0 for every v in D_j, for every augmented arc e.    (6)
```

There are at most `2r+s` tests. Each is a fixed-degree polynomial sign
decision on a rational `k`-box; the [small-core algebraic interface](smoothed-native-integer-recourse.md#4-exact-algebraic-completion-in-the-small-core)
performs it in `c_d^k poly_d(I+j)` bit work: minimize `r_e` exactly on the
rational closed box `D_j` and compare its algebraic optimal value with zero.
Substitute any fixed hull coordinates first. Each test uses one ordinary
univariate value representation; it does not compare a sum of unrelated
algebraic values. Identically zero polynomials pass without a strictness
requirement.

The marginal-potential certificate proves that `z` is optimal for every
core point of `D_j`. Since this hull contains an original optimal core, the
slice `[0,1]^k times {z}` contains an original global optimizer. Solve its
entire small core exactly and return a deterministic optimizer and value. This
completion is valid even with a continuum of core minimizers. It needs
neither integer label uniqueness nor local positive Hessian curvature.

All steps so far are sound on every draw. The remaining argument only shows
that the certificate passes at polynomial precision with high probability.

## 3. A base-only finite collection of flow charts

For analysis, consider every feasible integer flow `z`, every augmented
residual arborescence `T`, and every corresponding polynomial (5). Discard
identically zero polynomials and let `S` be the union of the zero sets of
the remaining polynomials, restricted to `[0,1]^k`. Nonzero constant
polynomials contribute the empty set.

Each tree path uses at most `s` arcs. Marginal evaluations at bounded native
labels and sums of these paths give coefficient heights polynomial in the
base input, independently of sampling precision. The number of labels is
at most

```
R_Z=product_a(u_a-l_a+1).
```

There are at most `(2r+s)^s` augmented arborescences per label and at most
`2r+s` reduced-cost polynomials per tree. Hence the finite collection has
at most `R_Z(2r+s)^(s+1)` members, with polynomial logarithmic length.
No part of the ordinary algorithm enumerates this collection.

The set `S` is compact semialgebraic with dimension at most `k-1`, or empty.
If a connected core box avoids `S`, all nonzero reduced polynomials of a
selected tree have constant signs on that box. At a queried point they are
nonnegative and not zero, hence positive. All identically zero polynomials
remain zero. Thus (6) passes whenever `D_j` avoids `S`.

The ignored identities include persistent ties, such as zero-cost residual
cycles present throughout an open core region. Discarding their zero sets
from `S` does not discard an optimality condition: their exact sign test in
(6) is satisfied everywhere.

## 4. Interior stationarity and the exceptional noise image

For each feasible label `w`, define the smooth polynomial slice
`F_w(v)=F_0(v,w)`, and set

```
E=union_(w in Y) [-grad F_w](S).                            (7)
```

This is compact semialgebraic of dimension at most `k-1`. Polynomial maps
do not increase semialgebraic dimension, and only a finite union is used.
The gradient label `w` need not equal the label defining a chart in `S`;
all cross-label pairs are included.

Let `a` be any globally optimal core point, and choose any integer flow
`w` attaining `V_0(a)`. The slice `F_w(v)+gamma'v` is bounded below by
`V_gamma(v)`, and both values agree at `a`. Hence `a` is a global minimizer
of this smooth slice. By the interiority hypothesis,

```
gamma=-grad F_w(a).                                       (8)
```

No differentiability of the lower envelope `V_0` is assumed. Compute a
base rational bound `H_2>=1` on the spectral norm of every core Hessian
`Hess F_w` throughout the unit core box; a monomial row-sum bound over the
native real bounding box suffices. Compactness gives

```
dist(gamma,E)<=H_2 dist(a,S).                              (9)
```

When `S` is empty, there is no proximity event and the chart tests already
hold throughout the core. Formula (9) is used only when `S` is nonempty.

There is a base-computable nonzero polynomial whose zero set contains `E`,
of degree `D=2^{poly_d(I)}`. Here is the format argument. For a fixed
chart polynomial `r_(z,T,e)` and a separate label `w`, the image piece has
the one-block formula

```
exists x in [0,1]^k:
   r_(z,T,e)(x)=0,    beta+grad F_w(x)=0.                  (10)
```

It has `k` quantified and `k` free variables, `O(k)` atoms, and degree
at most `max(d,2)`. Fixed-block elimination bounds its output format and
degree by the analysis-only parameter quantity
`E_d(k)=(k+1)^{O_d(k^2)}`, after fixing effective constants in that bound.
Coefficient heights do not enter it. The constant-base optimization solver
does not replace this multivariate quantifier-elimination format estimate.

Each piece has empty interior. Multiply all nonzero nonconstant polynomials
in its quantifier-free description. Their zero set contains that piece:
otherwise all signs would be locally constant at an image point, forcing
an open subset of the image. If no such atom remains, the piece is empty
and its product is one. Each product is nonzero, of degree at most
`E_d(k)^3`. Multiplying over the cross-label collection gives the safe bound

```
D=max{1,R_Z^2(2r+s)^(s+1) E_d(k)^3}.                       (11)
```

In particular `log D=poly_d(I)`. This is an analysis-only enclosure. The
algorithm computes the bound (11), not its exponentially large product or
the list of labels and trees.

## 5. A finite-grid tube bound including exceptional atoms

Use the [reviewed algebraic tube interface](core-noise-active-stratum-tube.md#5-algebraic-tube-input-and-the-finite-grid-reduction),
based on Basu--Lerario's singular-algebraic-set tube theorem. For a nonzero
polynomial of degree at most `D` in `k` variables, a valid integer coefficient
is

```
C_tube=16 k^(k+1) D (4D+2)^(k-1).
```

Its logarithm is polynomial in the base input. For the independent endpoint-
inclusive `M`-point uniform grid on `[-sigma,sigma]^k`, that interface gives

```
Pr{dist(gamma,E)<=eta}
   <=min{1,C_tube(eta/sigma+sqrt(k)/M)}.                   (12)
```

This includes atoms exactly on `E`. The proof adds independent uniform
jitter cubes around the grid points; these cubes tile a slightly enlarged
noise cube. It therefore needs no conditional-density claim and no sampling-
precision-dependent geometric separation. Both `E` and its degree bound
are base-only. In particular, they do not depend on a flow chosen after the
noise is observed.

The projected core-growth tail also remains valid under core-only noise.
Write `g_C` for the point-growth modulus of `V_gamma` on the unit core box,
set to zero on nonunique optimal core points. There is a base bound
`C_growth=2^{poly_d(I)}` such that

```
Pr{g_C<epsilon}<=k epsilon/sigma+2k C_growth/M.              (13)
```

To check its finite-grid format, write the good event as

```
exists (v,z) in X, for all (u,w) in X:
 F_gamma(u,w)>=F_gamma(v,z)+epsilon||u-v||^2.
```

Only the core distance appears. Native integrality uses finite coordinate
disjunctions with exponentially many atoms but polynomial logarithmic
length, as in the [native-recourse tail argument](smoothed-native-integer-recourse.md#5-one-finite-law-and-a-same-draw-label-enumeration-fallback).
There are two quantified blocks and fixed degree, so the section bound is
singly exponential in a polynomial of the base input. Persistent residual
ties do not force `g_C` to zero. The continuous-noise starting bound is applied
to the continuous function `V_0` on its `k`-dimensional compact box.

## 6. Cutoff, one law, and exact fallback

Use the label-enumeration fallback of the native-integer theorem, with a
base budget `B=2^{poly_d(I)}>=2`. Its cost is
`B(I+log M+1)^{e_d}`, with fixed polynomial exponent `e_d`, while it returns
a single winning small-core algebraic
representation. Define, before sampling,

```
rho=1/(4B),
g_0=rho sigma/(2k),        A_0=2+kL/g_0,
delta=rho sigma/(4 C_tube H_2).
```

Let `J>=0` be the least level satisfying

```
h_J<=delta/(2k A_0),                                      (14)
```

and choose the least power of two

```
M>=max{2,2^J,4k C_growth/rho,4k C_tube/rho}.                (15)
```

All bounds are base-only; `J,log M=poly_d(I)`. Equation (13) contributes at
most `rho` to failure. Equation (12) at `eta=H_2 delta` contributes at most
`rho/2`, using `sqrt(k)<=k`. Their sum is less than `2rho=1/(2B)`.

On the complementary event, the core optimizer `a` is unique, growth is
at least `g_0`, and (9) implies `dist(a,S)>delta`. The retained core hull
lies within infinity distance `A_0h_j` of `a`. By (14), every point in it
is within Euclidean distance at most `kA_0h_j<=delta/2`. Hence the hull
avoids `S`, and its selected tree certificate (6) passes. Exact whole-core
completion then succeeds.

If no chart certificate has passed by level `J`, use the exact fallback on
the same draw. Its expected work and proof-record cost are polynomial. No
residual coefficient is perturbed, and no draw is resampled or ignored.

## 7. Bit work, output, and scope

All queried core coordinates, exact integer flows, marginal values and
polynomial tree coefficients have polynomial bit length through level `J`.
Each level has one set of at most `2r+s` exact sign tests, costing
`c_d^k poly_d(I)` in total. Shortest paths, tree selection and ordinary
integer recourse have polynomial bit cost. Summing (4), adding these tests,
one exact small-core completion and the expected fallback, proves (3).

The output and refinement argument is the same as in the expanded-output
native-integer theorem. Even a fallback returns one feasible integer flow
and its core coordinate/value representations. Their degrees and heights
depend on the small core, not the number of labels inspected. Refinement
and clipping preserve mixed feasibility because the residual flow set is
independent of the core.

This result removes residual noise under an explicit core-interiority
hypothesis. It does not remove the hypothesis for general boundary optima:
the [two-arc boundary example](core-only-flow-boundary-obstruction.md) has
constant projected conditioning but no uniformly optimal flow in any retained
origin box, on a fixed positive-probability noise event. It also does not
extend the flow certificate to arbitrary nonseparable integer recourse or
core-dependent constraints.

The exact flow oracle, marginal potentials, fixed-block elimination and
algebraic tube estimate are established ingredients. The composition with
the sparse core search and non-strict polynomial flow certificate is the
claim of this note. The [focused prior audit](../prior-art/smoothed-interior-core-flow-prior.md)
compares exact convex-flow algorithms, parametric-envelope methods,
few-continuous-variable search and discrete smoothed optimization. No
publication-priority claim is made.

## Verification

A focused independent check approved the cross-label image format, its
base-only degree bound, the constant coefficient-height exponent, and the
fixed-core sign-test cost. The [completed-file review](../reviews/smoothed-interior-core-flow-review.md)
approved the chart certificate, exceptional-image argument, finite law,
same-draw fallback, and output contract.

The author ran

```sh
python3 -B research-20261002/new-direction/check_interior_core_flow.py
```

The [exact-fraction diagnostic](check_interior_core_flow.py) tests all eight
atoms of a small core-noise law on networks with one and 80 serial two-arc
stages. The latter has `2^80` feasible flows and `2^79` persistently tied
conditional winners. The joint objective is cubic, with quadratic
core-dependent arc costs. The checks passed 480 oracle queries, 10,535
whole-interval polynomial sign tests, and 10,363 identically zero reduced
costs. Regular draws closed by level three with at most four retained cells.
Each network also had an endpoint atom with two optimal core points;
uniform-flow closure correctly failed there. Analytic comparison of its two
cost classes checked the fallback value. The diagnostic does not implement
general flow optimization, general algebraic sign tests, the full base-law
budget, or enumeration of all feasible flows.

The reviewer independently ran a [cyclic-network diagnostic](../reviews/check_interior_core_flow_charts.py):
205 charts, 104 interval certificates, 1,768 competing-label comparisons,
683 zero reduced costs, and 33 tied query optima. That check includes
forward and reverse arcs and tight zero-cost cycles. These reviewer results
are distinct from the author's tests. No index edits, project-wide
verification or CI inspection were performed.
