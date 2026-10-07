# Sparse smoothed polynomial optimization on products of simplices

Date: 2026-10-02. Status: complete theorem, with independent geometry/count
and closure/bit reviews and targeted exact checks. This is a constrained
extension of the sparse box method. This note makes no priority claim and
does not edit an index.

The extension permits resource constraints inside disjoint
blocks while retaining original-coordinate linear noise. It does not cover
overlapping resource constraints. Its mechanism is feasible block rounding
and face-stratified counting, rather than a change to box coordinates.

## 1. Model and conclusion

Partition the continuous coordinates into blocks with feasible sets

```
Delta_b={x in R^b: x_i>=0, sum_i x_i<=1}.
```

Additional native-integer coordinates have bounded integer intervals.
Fixed coordinates and empty integer intervals are handled first. For the
continuous part, the initial statement uses unit simplices; arbitrary
affine images and intersecting local polytopes are not included.
If no variable remains, evaluate the fixed point and any sampled additive
constant directly; the formulas involving `W`, `n`, and growth below apply
only to the nontrivial remaining domain.

The objective is an explicit rational polynomial of fixed degree, given
as factors on a supplied tree decomposition. Every bag contains whole
simplex blocks whenever it contains any of their coordinates. Let `p` be
the largest total scalar dimension of a bag, including its integer
coordinates, and let `n` be the total scalar dimension. Factors may couple
different blocks. Let `I` count all base input, including a rational noise
half-width `sigma>0` and a verified `L>0` such that

```
H_BB F_0 <= L I    for every simplex block B,
partial_ii F_0 <= L    for every integer coordinate i.       (1)
```

These bounds hold on the full continuous hull of the domain. Rational
monomial and matrix row-sum bounds are a concrete polynomial-time verifier.
A sharper supplied proof needs a polynomial-time verifier with its encoding
included in `I`; otherwise add that verifier's actual cost to (2).
Condition (1) is a block matrix bound, stronger than a bound on its
diagonal entries alone. Correlated block rounding requires this distinction.

As in the [reviewed box theorem](smoothed-sparse-polynomial.md), there is
one base-chosen rational grid of `M` equally spaced points in
`[-sigma,sigma]`, with `log M=poly_d(I)`, and an algorithm that returns an
exact global optimizer on every draw of independent ambient linear noise
from that grid. Its expected bit work is at most

```
C_0^p [4+(2+n/2)L max(1,w_max)/(2sigma)]^p poly_d(I),        (2)
```

where `w_max` is the largest integer interval width, or one if none occur.
The output is a certified convex local polytope defining an exact optimizer,
or an exact algebraic optimizer on a rare same-draw fallback. The target
is expected polynomial bit work for fixed width and polynomial numerical
ratios, not FPT in width. No global growth or strict-complementarity promise
is supplied; those are good-event conditions for stopping analysis.

## 2. Feasible clipped-cube rounding

For `h=1/m`, with `m` a power of two, intersect a dyadic cube with a
simplex:

```
C=Delta_b intersection product_i [h k_i,h(k_i+1)].           (3)
```

After translation and scaling, its nonempty part is

```
{z in [0,1]^b: sum_i z_i<=m-sum_i k_i}.                     (4)
```

The right-hand side is an integer. Every vertex of (4) is a cube corner:
if two coordinates were fractional, a small opposite displacement would
preserve the budget and violate extremality; if exactly one were fractional,
an active integer budget would force it to be integral, while an inactive
budget permits a one-coordinate displacement. Therefore `C` is the convex
hull of its feasible grid corners.

Every point of `C` admits a distribution over those corners with its own
mean. Coordinates already on grid boundaries stay fixed. Each variance is
at most `h^2/4`, so the trace covariance is at most `b h^2/4`. The proof
only needs this convex-combination distribution. There are at most `2^b` corners, children, and
incident cells per grid point. The cells are nested under dyadic refinement.
No triangulation or factorial incidence bound is needed.

Use these cells in each continuous block and the predecessor's cells in
integer intervals, with singleton integer cells below unit resolution.
Before the common physical mesh reaches one, keep each simplex as one cell
with its `b+1` vertices. Afterwards (3) applies. Each bag cell is a product
of whole-block cells. Shared grids and fixed boundary coordinates imply
that correlated rounding within a block preserves every bag whitelist
containing that block, including one specified bag cell.

Round blocks sequentially, independently between blocks. For fixed outside
coordinates, (1) gives

```
E F_gamma(Y)<=F_gamma(x)+(L/2) E||Y_B-x_B||^2.
```

Thus the global error remains `E_j=n L h_j^2/8`. The original pruning rule
retains every optimizer, and every retained bag cell has one consistent
global grid witness of gap at most `2E_j`. Separate block witnesses would
not establish the probability argument below.

## 3. Expected counts by original simplex faces

Condition on the noise outside a bag. Minimizing outside blocks leaves a
conditional value function `V` on that bag's product domain. The outside
feasible set is fixed. Subtracting `L||x_B||^2/2` in any simplex block makes
each outside-restricted function concave in that block; its infimum is
concave too. Hence `V` has the same block upper curvature and is independent
of all bag noise.

Every retained witness tuple `v` satisfies

```
V(v)+gamma'v <= min_original_bag [V+gamma'x]+2E_j.            (5)
```

Classify a simplex grid node by its smallest original face. If its positive
support is `S` and its budget is slack, the relative face dimension is
`r=|S|`. Both neighbors `v+-h e_i` are feasible for each `i in S`:
positive coordinates and nonzero budget slack are integer multiples of `h`.
If its budget is tight, choose the least index `j in S` as anchor. The face
dimension is `r=|S|-1`, and both neighbors
`v+-h(e_i-e_j)` are feasible for every other `i in S`.

For a direction `d`, comparison in (5) confines `gamma'd` to an interval
of length at most

```
L h ||d||^2 + 4E_j/h <= Lh(2+n/2).                         (6)
```

For tight budgets, condition also on the anchor coefficient. The remaining
coefficients are still independent; intervals for `gamma_i-gamma_j` become
intervals for the distinct `gamma_i`. All interval endpoints depend on the
fixed grid tuple and the outside value function, not other remaining bag
noise. Treat all blocks jointly and condition their anchors at once.

An `r`-dimensional original face contains
`binom(m-1,r)<=m^r` relative-interior grid nodes. A simplex has
`binom(b+1,r+1)` such faces. Under an `M`-point ambient noise grid, each
comparison has probability at most its interval length divided by
`2sigma`, plus `1/M`. Thus a face contributes at most

```
[L(2+n/2)/(2sigma)+1/(Mh)]^r.                              (7)
```

Choose `M>=2^J`, as in the predecessor, for the base cutoff level `J`.
The atom term in (7) is at most one. Summing over faces bounds one block
by `C^b [1+(2+n/2)L/(2sigma)]^b`. The zero-dimensional faces contribute
their vertices directly. The initial levels above unit mesh have only
`b+1` nodes and satisfy the same coarse bound. Combining the independent
remaining bag coefficients across blocks and the prior integer-coordinate
count proves the state factor in (2), up to an absolute constant to the
power `p`.

Clipped cells have the same constant-to-the-dimension incidence and child
counts as boxes. Sparse separator-key DP therefore generates only a
constant-to-the-`p` multiple of retained rows. It need not enumerate the
full simplex grid. This is an expected count for joint bag min-marginals,
not a product of expectations for separately filtered blocks.

## 4. Exact original-face tests

Let a rational coordinate hull contain every original optimizer. Verify
rational bounds `M_1>=max{1,max_i sum_k sup|partial_ik F_0|}` and
`T>=max{1,max_i sum_jk sup|partial_ijk F_0|}` on the entire enclosing
coordinate box, not only the product of simplices. A coordinate-hull
midpoint can lie outside a simplex. Monomial bounds on this larger box
suffice; their magnitudes affect only the cutoff logarithm. Derivative
intervals on a hull are then obtained from its midpoint and `M_1`.
For each simplex block, the following tests are sound:

- If `partial_j F>0` throughout the hull, force `x_j=0`.
- If `partial_j F<0` throughout the hull for some `j`, force `sum x_i=1`.
- If `partial_i F-partial_j F>0` throughout the hull for distinct `i,j`,
  force `x_i=0`.

The first test decreases a positive coordinate; the second increases a
coordinate when the budget is slack; the third transfers a small positive
amount from coordinate `i` to `j`. Each direction is feasible in the
original simplex whenever the forced equality is absent. These arguments
use original feasibility, not the artificial coordinate hull as an
optimization domain. Integer coordinates are fixed only by singleton hulls.

At a simplex optimum, write KKT stationarity as

```
partial_i F + lambda_budget - lambda_i=0,
lambda_budget>=0,    lambda_i>=0.                           (8)
```

The active original normals are linearly independent. If the budget is
slack, a zero coordinate with multiplier at least `tau` has positive
gradient. If the budget is tight, at least one coordinate `j` is positive,
and its gradient is `-lambda_budget`. A positive budget multiplier forces
the budget equality by the second test. Every zero coordinate with positive
multiplier satisfies `partial_i F-partial_j F=lambda_i`, so the third test
forces it. No lower bound on the positive coordinate's magnitude is needed.

Under point growth `g_0` and active multipliers greater than `tau`, the
retained witness argument bounds coordinate radii by `A h_j`, with
`A=2+nL/g_0`. A derivative-difference enclosure differs from its value at
the optimizer by at most `4M_1 A h_j`; therefore
`h_j<=tau/(8M_1 A)` suffices for all tests. Below unit mesh, the usual
`h_j<=1/(4A)` identifies every integer coordinate.

After these equalities, form the intersection of the retained hull with
the original simplex faces. It still contains all original optimizers.
Its affine tangent basis `Z` uses columns `e_i` for a slack-budget face
and `e_i-e_j` for a tight-budget face. It is rational and has
`Z'Z>=I`. A rational point `c` of each clipped face can be found by filling
from its lower bounds; degenerate coordinates are substituted.

Let `r` bound the maximum coordinate distance from `c` throughout this
polytope, and let `T` bound the full third-derivative row sum. The exact
matrix test

```
Z' H(c) Z - (Tr+g_0) Z'Z  is positive definite              (9)
```

certifies strong convexity on the remaining affine face. At the good
optimizer, point growth gives `Z'H(a)Z>=2g_0 Z'Z`. Since both `c` and
the optimizer lie within the retained hull, `r<=2A h_j`; consequently
`h_j<=g_0/(8TA)` makes (9) pass. With no tangent coordinates, the point is
already exact. All face and matrix tests are valid independently of the
probabilistic event used to bound their stopping level.

## 5. Finite-noise active-multiplier margin

Fix integer labels and an original product face. Parameterize it using
the basis just described. For every tight simplex face with positive
support `S` and anchor `j`, change noise coordinates to

```
eta_i=gamma_i-gamma_j (i in S except j),
zeta_budget=gamma_j,
zeta_i=gamma_i (i outside S).                               (10)
```

For slack faces, keep the positive-support coefficients as tangent noise
and the zero-coordinate coefficients as normal noise. This is a unimodular
linear transformation. The free stationarity equations depend only on
the tangent noise. On a positive-growth draw, the relevant tangential
Hessian is nonsingular, so the isolated-root bound is at most `D^k`,
where `D=max(1,d-1)` and `k` is free dimension.

For fixed tangent noise and all but one normal coefficient, every active
multiplier is affine with slope `1` or `-1` in a suitable remaining normal
coefficient. In particular, a budget multiplier is
`-partial_j F_0-gamma_j`, and a zero-coordinate multiplier at a tight
budget is `partial_i F_0-partial_j F_0+gamma_i-gamma_j`.

The transformed finite-grid variables need not be independent. Do not
assume they are. Instead, each tangent difference has at most `2M-1`
possible labels, while each unchanged coefficient has `M`. Counting
transformed tuples and then the at most
`tau(M-1)/sigma+1` labels in a multiplier slab gives, for one face and
one active multiplier,

```
Pr{positive growth and |lambda|<=tau}
 <= 2^k D^k (tau/sigma+1/M).                                (11)
```

There are at most `3^{n_c}` product-simplex faces, at most `2n_c` original
continuous facets, and `R_Z` integer assignments. Thus a safe union factor is

```
K=max{1,2n_c R_Z 3^{n_c}(2D)^{n_c}}.                        (12)
```

Its logarithm is polynomial in base input. The degree-one and
zero-dimensional-face cases use the same empty-system convention as the
box tail proof. Point-growth failure is handled separately; (11) is not
obtained by conditioning the distribution on positive growth.

## 6. Remaining bit and certificate interfaces

The point-growth tail applies to this compact mixed domain. Its two-block
finite-grid formula replaces box membership by the linear simplex
inequalities and integer-label disjunctions. The scalar-section degree and
count bounds remain `exp(poly_d(I))`. Likewise the
[scalar exact fallback](polynomial-exact-fallback.md) applies after this
replacement: compactness, not box geometry, supplies the canonical
lexicographic optimizer. These are direct formula adaptations that require
explicit review; no new quantifier-elimination theorem is proposed.

Let `B=exp(poly_d(I))` be an effective base budget for that exact fallback
and its subsequent algebraic refinement. Let `C_tail=exp(poly_d(I))`
be the finite-grid scalar-section bound, and put

```
W=n_c+sum_integer widths,       rho=1/(4B),
g_0=rho sigma/(2W),             tau=rho sigma/(2K).
A=2+nL/g_0.
```

Choose `s` as the least power of two at least `max(1,w_max)`, and take
the least `J` for which `h_J=s2^(-J)` satisfies

```
h_J<=min{1/(4A),tau/(8M_1 A),g_0/(8TA)}.                   (13)
```

Before drawing noise, choose the least power of two

```
M>=max{2,2^J,4n C_tail/rho,2K/rho}.                        (14)
```

The global point-growth failure and the positive-growth multiplier-margin
failure each have probability at most `rho`. Outside their union, the
original-face tests and (9) succeed by level `J`. Every draw is treated
soundly; if closure has not succeeded, invoke the exact fallback on that
same draw. Its expected work is polynomial. All logarithms in (13)--(14)
are polynomial in the base input. Sampled coefficient length appears only
in the polynomial factor of the base-chosen fallback budget.

All grid vertices, evaluations, derivative intervals, and face matrix
tests have polynomial rational encoding length. The sparse generation
bound in Section 3 proves (2) after summing polynomially many levels. The
remaining output evaluation is explicit below; it does not use a numerical
condition-number iteration bound.

### 6.1 Rational affine hull and interior ball

After integer and face fixing, a block patch has bounds `l<=x<=u` and
either `sum x<=beta` or `sum x=beta`. Fixed coordinates have already been
substituted into the rational `beta`. If `sum l=beta`, feasibility forces
the unique point `l`. For an equality, `sum u=beta` similarly forces `u`.
Substitute these points and zero-width coordinates. All remaining blocks
have positive coordinate widths and `sum l<beta`; equality blocks also
have `beta<sum u`.

For an equality block choose

```
lambda=(beta-sum l)/sum(u-l),       c=l+lambda(u-l).
```

For an inequality block choose

```
lambda=min{1/2,(beta-sum l)/(2sum(u-l))},
c=l+lambda(u-l).
```

Every remaining bound has strictly positive slack at `c`; the inequality
budget has positive slack too. These are rational points with polynomial
encoding length. Thus the only remaining affine equations are the recorded
block sums. No strict original-coordinate slack at the unknown optimizer
is being assumed.

Use coordinates `t_i=x_i` in inequality blocks. In an equality block drop
one anchor coordinate and substitute `x_j=beta-sum_(i!=j)t_i`.
The resulting full-dimensional rational domain `P` is a product of boxes
with an upper total-sum bound or a lower and upper total-sum bound. All
nonconstant inequalities are strict at the displayed reduced center.
For its rational inequality description `a_s't<=b_s`, the positive number

```
r_P=min_s (b_s-a_s'c)/(1+||a_s||_1)
```

is a valid Euclidean interior-ball radius. The logarithm of its inverse
is polynomial in the patch encoding. An outer radius follows from its
coordinate bounds. The reduced polynomial is explicit and still fixed
degree; substitution increases its size by at most a polynomial whose
exponent depends on the fixed degree. The tangent basis satisfies
`I<=Z'Z<=nI`, so (9) gives reduced Hessian at least `g_0 I` on `P`.

### 6.2 Exactly feasible projection and GLS evaluation

Projection of a rational vector `v` onto one reduced block
`l<=t<=u, a<=sum t<=b` is rational and computable in polynomial bit time.
First clip `v` to its box. If its sum belongs to the slab, this is the
projection. Otherwise the active sum equals the violated endpoint `q`,
and the projection has coordinates

```
t_i=clip(v_i-alpha,l_i,u_i),       sum_i t_i=q.
```

Sort the rational breakpoints `v_i-u_i` and `v_i-l_i`. On each interval
the sum is affine in `alpha`; solving its one linear equation gives a
rational threshold. Endpoint plateaus give an endpoint vector directly.
This proves the formula's exact rational and polynomial-bit implementation.
Blocks project independently, and Euclidean projection is nonexpansive.

Apply the [reviewed GLS epigraph construction](convex-patch-evaluation.md)
to the reduced polynomial on `P`. Let `V>=max{1,sup_P|f|}` and
`G>=max{1,sup_P||grad f||_2}` be rational monomial bounds. The capped
epigraph has inner center `(c,V+1)` and radius `r=min{r_P,1/2}`;
translate by this center for the origin-centered outer-radius convention.
Linear inequalities, the top cap, and polynomial tangent planes supply
exact rational strong separation with polynomial output length.

GLS weak optimization returns an `epsilon`-near-feasible epigraph point
`(t,v)` and compares with the `epsilon` erosion. Its homothety toward the
known center proves

```
v<=f*+epsilon[1+(2V+1)/r].
```

Project `t` rationally onto `P`. Its feasible value `U` is at most
`v+(G+1)epsilon`, by nonexpansiveness and the gradient bound. Therefore

```
[v-epsilon(1+(2V+1)/r), U]
```

is a valid objective interval, of width at most
`epsilon[G+2+(2V+1)/r]`. Choose the weak tolerance at most `r/2` and
the desired gap divided by this last factor. This accounts explicitly for
both approximate feasibility and comparison with the eroded body.

For physical-coordinate accuracy `2^-q`, use an objective gap at most
`min{2^-q,(g_0/(2n))2^(-2q)}`. Strong convexity gives the reduced-coordinate
error, and `||Z||_2^2<=n` gives the stated physical error. Every required
tolerance has `poly_d(I+q)` bits. This proves polynomial-bit evaluation of
the compact successful descriptor, including boundary optimizers.

The fallback's feasible rational approximation also extends: refine each
continuous coordinate and project each block onto its original simplex;
use its selected integer labels exactly. Nonexpansiveness and a polynomial-
bit gradient bound control the objective error. The refinement precision
grows by only `poly_d(I+log M)` bits. Thus the same base budget pays for
the rare fallback's arbitrary-precision evaluation. A full global DP trace
has only the expected size bound; the compact local descriptor has
polynomial encoding length.

## 7. Probability-simplex equality blocks

Some original blocks may instead be probability simplices
`{x>=0:sum x=1}`, with independent noise on those original coordinates.
Record this equality at initialization. A one-coordinate equality block
is a fixed point and is substituted; any sampled coefficient on that fixed
coordinate contributes only an additive value constant.

Intersect grid cubes with the equality. The scaled equation has an integer
right-hand side, so its vertices remain cube corners and the same
mean-preserving rounding proof applies. Every original face is now a
positive-support face with tight sum. Its dimension and lattice-node count
are `|S|-1` and `binom(m-1,|S|-1)`, respectively. All counting uses the
anchor differences already analyzed in Section 3; no independent-noise
assumption is imposed on a reduced coordinate system.

For these blocks, **omit both absolute-gradient tests** in Section 4.
Decreasing one coordinate alone violates the original equality, so a
positive partial derivative does not force that coordinate to zero.
Only a strict derivative difference `partial_i F-partial_j F>0`
forces `x_i=0` by a feasible transfer. A positive-support anchor at an
optimum has the common tangent gradient, and every strictly positive
zero-coordinate multiplier is its gradient gap, so these tests remain
complete without a positive-coordinate slack bound.

The equality's unrestricted normal multiplier has no required margin.
The good event requires positive point growth and positive margins only
for active zero-coordinate inequalities, together with the earlier margins
on inequality-simplex blocks. The transformed-noise root and slab counts
are unchanged for these zero-coordinate gaps. There are fewer original
faces and margin events, so (12) remains a safe bound. The initial equality
is included in the scalar membership formula and the affine tangent basis;
the fallback and relative-polytope evaluator therefore apply unchanged.
Thus the extension covers lower-dimensional feasible domains as well as
full-dimensional resource simplices.

## 8. Scope and significance check

These constraints are not eliminated by an affine box substitution. A
stick-breaking map from a box to a simplex makes original ambient linear
noise nonlinear, so the reviewed box theorem does not apply directly.
The geometric and probabilistic extensions above address that difference.

The product structure is essential: it makes the outside feasible set
independent of bag values. An overlapping resource constraint can destroy
this property. The note therefore offers a concrete first constrained
class, not a theorem for arbitrary sparse linear constraints or arbitrary
local convex factors.

Whole-block bags are also essential to this proof. If the scalar primal
graph includes each simplex constraint as a clique, expanding every bag to
contain all coordinates of its intersecting blocks increases scalar bag
size by at most the maximum block size. Thus fixed original width remains
fixed width, but the parameter increase must be stated. A single resource
constraint over all variables has a large block and provides no fixed-width
advantage.

Feasible dependent rounding, simplex KKT conditions, rational convex
optimization, and scalar elimination are established ingredients. The
potential new capability is their composition with sparse expected cell
counts and an every-draw exact output contract under finite ambient noise.
The [literature comparison](../prior-art/simplex-block-smoothed-prior.md)
does not establish publication priority.

## 9. Review and targeted checks

The independent [geometry and noise audit](simplex-block-noise-review.md)
checks clipped-cell rounding, joint bag counts, original-face forcing, and
the transformed-tuple multiplier bound. A separate
[completed-text review](../reviews/simplex-block-closure-review.md)
checks the final closure, equality-block rules, and relative-polytope
evaluator. The root reviewer also independently read the full proof and
checked its constants. The reviews record the required ambient-box
derivative bound, the restricted equality-block rules, and the precise
GLS approximate-feasibility repair.

The targeted command

```
python3 -B research-20261002/new-direction/check_simplex_sparse_dp.py
```

passed eight levels on two two-dimensional simplices coupled through a
binary coordinate: 513 exact DP min-marginals matched exhaustive compatible
bag-row pairs over 9,242 assignments. It checked 140 retained witnesses,
267 removals, 20 feasible mean-preserving rounding atoms, and 336 point-
growth probes. At level seven it fixed the integer, one tight budget,
and a zero coordinate in the other simplex, then verified the tangent
matrix test despite negative curvature in an ambient normal direction.
The result is saved in
[simplex-sparse-dp-results.json](simplex-sparse-dp-results.json).
These are finite exact diagnostics, not a performance or probability test.
The independent count audit records its own distinct finite-law checks.
The closure review's separate checker passed 668 finite-noise draws,
154 per-face multiplier probability bounds, 75 zero-multiplier incidences,
three rational interior balls, and 27 projection/KKT checks, including a
200-bit thin equality patch. Those checks were run by that reviewer, not
rerun here. The scoped main-document check covers formatting and local links.
No project-wide verification, CI inspection, or index edit was performed.
