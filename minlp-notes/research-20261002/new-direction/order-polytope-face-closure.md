# Certified face identification and convex closure on order polytopes

Date: 2026-10-02. Status: a closure lemma and a finite-noise margin
bound. This note does not by itself establish the complete expected
optimization algorithm.

A small rational hull can identify the optimizer's active order
equalities by polynomially many linear programs. The certificates compare
linear objective gaps with a verified gradient error. Under independent
linear noise, these gaps are bounded away from zero outside an explicitly
bounded exceptional event. Once the active equalities are identified,
point quadratic growth supplies a positive Hessian on their affine hull.
The remaining order inequalities stay in the final convex patch, so no
probability bound on their primal slacks is needed.

This supplies the constrained closure ingredient left open in
[the order-polytope counting note](order-polytope-cell-count.md). The
mechanism replaces the coordinate gradient-sign tests in
[the polynomial box theorem](smoothed-sparse-polynomial.md).

## 1. Model and the linear gap certificates

Let

```text
P = {x in [0,1]^n : x_i <= x_j for each of m specified edges i -> j},
F_gamma(x) = F_0(x) + gamma'x,
```

where `F_0` is a rational polynomial of fixed degree at most `d`.
Directed cycles are allowed. They impose equalities that can be removed
in preprocessing or certified by the tests below. All variables are
continuous. The certificates do not require a bound on graph treewidth.

Every vertex of `P` is a zero-one vector. One direct proof is to group
coordinates connected by tight order equalities. If a group has a common
value strictly between zero and one, it can be moved slightly in both
directions, since every order inequality to another group has positive
slack. Such a point is not a vertex. Fixing coordinates to zero or one
selects a face, so the resulting nonempty polytope also has only zero-one
vertices.

Suppose a rational coordinate hull

```text
Q = product_i [ell_i,u_i] subseteq [0,1]^n
```

contains every original global optimizer. Let `c` be its midpoint and
`r=max_i (u_i-ell_i)/2`. Compute a rational bound

```text
M_1 >= max{1, max_i sum_j sup_[0,1]^n |partial_ij F_0|}.
```

With

```text
g = gradient F_gamma(c),       delta = M_1 r,                (1)
```

every `a in Q` satisfies
`||gradient F_gamma(a)-g||_infinity <= delta`.
Termwise monomial bounds give such an `M_1` with polynomial encoding
length for fixed degree. Its numerical magnitude need not be polynomial.

For an edge `e=(i,j)`, define its violating vertex face

```text
P_e^- = P intersect {x_i=0, x_j=1}.
```

For a proposed lower-bound equality `x_i=0`, use
`P_e^-=P intersect {x_i=1}`. For a proposed upper-bound equality
`x_i=1`, use `P_e^-=P intersect {x_i=0}`. In all cases define

```text
Delta_e(v) = min_(x in P_e^-) v'x - min_(x in P) v'x.         (2)
```

If `P_e^-` is empty, the proposed equality already holds throughout
`P`. Otherwise, both minima in (2) are rational linear programs when
`v=g`. Force the proposed equality whenever

```text
Delta_e(g) > n delta.                                       (3)
```

There are `m+2n` proposed equalities. One common unconstrained LP and
one constrained LP for each proposal suffice. Rational primal and dual
solutions provide exact certificates for the gaps and their comparison
with the rational threshold.

### Soundness of each fixing

Let `a in Q` be any original global optimizer, and write
`h=gradient F_gamma(a)`. Since `P` is convex, first-order optimality
gives

```text
h'(x-a) >= 0 for every x in P.                              (4)
```

Thus `a` minimizes the linear objective `h'x` on `P`. If `a`
violates a proposed equality, express it as a convex combination of
vertices in this linear optimal face. At least one of those vertices,
say `v`, belongs to `P_e^-`: for an edge this means `v_i=0,v_j=1`;
the bound cases are the corresponding single-coordinate statement.

Let `w` be a vertex minimizing `g'x` on `P`. Since `v` is
`h`-optimal and both vertices are zero-one,

```text
Delta_e(g) <= g'(v-w)
           = h'(v-w) + (g-h)'(v-w)
           <= n delta.                                    (5)
```

This contradicts (3). Therefore every certified equality holds at every
original global optimizer. No growth, uniqueness, or probabilistic
assumption is used in this argument.

For every nonempty `P_e^-`, the gap also satisfies

```text
|Delta_e(v)-Delta_e(w)| <= n ||v-w||_infinity.                (6)
```

For example, take a violating vertex minimizing the first objective
under `w`, and a vertex minimizing the unrestricted objective under
`v`; subtracting their costs proves one direction, and interchanging
`v,w` proves the other. Consequently, a true gap
`Delta_e(h)>tau` is detected whenever `delta<=tau/(2n)`.

## 2. A finite-noise bound for small active gaps

Let each `gamma_i` be independent and uniform on the same `M>=2`
equally spaced values in `[-sigma,sigma]`, with rational `sigma>0`
included in the input encoding. Their spacing is

```text
eta = 2 sigma/(M-1).
```

Let `g_*` be the global point-growth modulus, set to zero on draws
without a unique optimizer. Thus `g_*>0` means that the unique optimizer
`a` satisfies

```text
F_gamma(x)-F_gamma(a) >= g_* ||x-a||^2 for every x in P.
```

Set

```text
q = m+2n,
D = max(1,d-1),
K = q 2^q D^n.                                             (7)
```

For every `tau>=0`,

```text
Pr{g_*>0 and some equality active at a has
   nonempty P_e^- and Delta_e(gradient F_gamma(a)) <= tau}
    <= K (tau/sigma + 2/M).                                 (8)
```

For independent continuous uniform noise on the same interval, the
corresponding bound is `K tau/sigma`. These are unconditional
intersection bounds; the noise is not conditioned on positive growth.
In particular, the continuous law has positive gaps for all active
constraints almost surely on the event `g_*>0`.

### Faces and stationary roots

There are at most `2^q` faces of `P`, since each face is determined by
the subset of the displayed `q` inequalities that hold identically on
it. This crude bound is used only in the analysis.

Fix a face `F` of dimension `k`, and choose rational affine coordinates
`x=b+Bz` for its affine hull, with `B` of full column rank. If the
optimizer has minimal face `F`, it belongs to the relative interior of
`F`. The restricted stationary equations are

```text
B' [gradient F_0(b+Bz)+gamma] = 0.                          (9)
```

Positive point growth gives

```text
B' Hess F_0(a) B >= 2 g_* B'B,                              (10)
```

by two-sided Taylor expansion in every direction parallel to `F`.
Hence this stationary root is nonsingular. For fixed coefficients, the
system (9) has at most `D^k<=D^n` nonsingular complex roots, by the
isolated-root Bezout bound. Other singular components do not affect
this count. A zero-dimensional face contributes one candidate.

### An order equality: two noise coordinates on each grid fiber

Fix an edge `e=(i,j)` active on `F`, and a zero-one vertex `w` of
`F`. Hold all noise coordinates other than `i,j` fixed. Parameterize
the remaining pair by

```text
s = gamma_i+gamma_j,       t = gamma_i,
gamma_j = s-t.
```

For fixed `s`, varying `t` changes the noise in direction
`e_i-e_j`, which is orthogonal to the affine hull of `F`. Therefore
the restricted stationary system (9), including its nonsingular roots,
does not change along this fiber.

Fix one of these real roots `a` in the relative interior of `F`.
Its gradient has the form
`h(t)=h(0)+t(e_i-e_j)`. Whenever this root is an actual optimizer with
minimal face `F`, equation (4) and stationarity on `F` imply

```text
min_(x in P) h(t)'x = h(t)'w.
```

Every vertex `v` of `P_e^-` has `v_i=0,v_j=1`, whereas
`w_i=w_j`. Thus

```text
(e_i-e_j)'(v-w) = -1.
```

It follows, on every parameter value where this root satisfies the
required optimality conditions, that

```text
Delta_e(h(t)) = beta - t,                                   (11)
```

where `beta=min_(v in P_e^-) h(0)'(v-w)` is independent of `t`.
The event `0<=Delta_e(h(t))<=tau` is therefore contained in an
interval of length `tau`. The identity is needed only on the
optimality-valid parameter values, which may form a smaller set.

For the finite law there are `2M-1` possible sums `s`. On each fiber,
the allowed `t` values are spaced by `eta`. An interval of length
`tau` contains at most `tau/eta+1` of them. Summing over the at most
`D^n` roots on each fiber and dividing by the `M^2` equally likely
pairs bounds the contribution for this face and edge by

```text
D^n (2M-1)(tau/eta+1)/M^2
    <= D^n (tau/sigma + 2/M).                               (12)
```

This counting argument does not assert a uniform conditional density
after fixing the sum. Such a density can be large on short fibers.
For continuous noise, the transformation to `(s,t)` has Jacobian one;
the sum ranges over an interval of length `4 sigma`. Integrating
fiber lengths against density `1/(4 sigma^2)` gives `D^n tau/sigma`.

### An active coordinate bound

If `x_i` is fixed to zero or one on `F`, varying only `gamma_i`
leaves (9) unchanged. For each stationary root, the difference
`h(t)'(v-w)` for a violating vertex has slope `+1` or `-1`.
The same interval argument gives the smaller finite bound
`D^n(tau/(2 sigma)+1/M)`. The bound in (12) therefore covers all
three kinds of proposal. Union over at most `q` proposals and
`2^q` faces proves (8).

The algorithm never enumerates these faces or roots. Their counts affect
only the chosen margin and the number of random bits.

## 3. Restriction to a certified convex patch

Intersect all certified equalities with the retained hull. Order
equalities merge coordinates into blocks; active bounds fix entire
blocks to zero or one. Substitute these relations as

```text
x = b+Bz,
```

where each column of `B` is the zero-one indicator of one unfixed
block. The supports of these columns are disjoint, and

```text
D_B = B'B
```

is a positive diagonal integer matrix. For each unfixed block, intersect
the original coordinate intervals to obtain its rational interval.
Substitute any resulting singleton intervals as well. Let `C` be the
product of the remaining block intervals, intersected with every
remaining original order inequality. This rational polytope still
contains all original optimizers after substitution. No inactive order
inequality is dropped.

Take the midpoint of the block interval product and map it to the full
point `c`. It need not satisfy the remaining order inequalities, but it
lies in the original box. Let `r` be the largest half-width of these
block intervals. Every full point in the patch is within infinity-norm
distance `r` of `c`. A rational bound

```text
T >= max{1, max_i sum_jk sup_[0,1]^n |partial_ijk F_0|}
```

gives `||Hess F_0(x)-Hess F_0(c)||_2<=T r` throughout the block
interval product. For a positive rational trial modulus `g_0`, test
exactly whether

```text
B' Hess F_0(c) B - (T r+g_0) D_B is positive definite.       (13)
```

A rational LDL decomposition, or an equivalent rational matrix test,
certifies this condition. It implies

```text
Hess_z F_gamma(b+Bz) >= g_0 D_B throughout C.                (14)
```

Therefore the restricted polynomial has a unique minimizer on the
convex patch `C`. Since the patch contains every original global
optimizer, that minimizer is the original global optimizer. If all
blocks are fixed, return the resulting feasible point instead.

The exact output can be the rational patch, the restricted polynomial,
the positive modulus, and the rational matrix certificate, together with
the pruning and fixing record. Its unique constrained minimizer is an
unambiguous exact implicit representation. A KKT system with the retained
linear inequalities gives an equivalent implicit primal description;
the multipliers need not be unique. This does not promise short expanded
minimal polynomials for the optimizer's coordinates.

### Why closure eventually succeeds on the margin event

For this stopping argument only, suppose `g_*>=g_0`, and every active
equality with nonempty violating face has true gap greater than `tau`.
If the initial hull radius satisfies

```text
r <= min{tau/(4n M_1), g_0/(4T)},                           (15)
```

then (6) and (3) identify all active equalities. Equalities with empty
violating faces are already imposed. The resulting affine hull is that
of the optimizer's minimal face, apart from any additional valid
singleton substitutions. The restricted Hessian at the optimizer is
at least `2g_0 D_B`, by (10).

Block intersection can only reduce the hull radius. Thus the matrix in
(13) is at least

```text
(g_0-2T r) D_B >= (g_0/2) D_B,
```

so the test succeeds. The inequalities that are inactive at the optimizer
need only be strictly slack for the infinitesimal argument establishing
(10). Their slacks do not occur in (15), and they remain constraints of
the convex patch.

## 4. Bit complexity and convex evaluation

For fixed degree, `M_1`, `T`, and all polynomial evaluations have
polynomial encoding length in the rational input and hull description.
The `q+1` linear programs used for identification have rational
coefficients of that length. Block substitution, the gap comparisons,
and the matrix test also use polynomial bit work. In particular,

```text
log K <= log q + q + n log D
```

is polynomial in the base input. Choosing a dyadic margin
`tau=2^-p(I)` and `M=2^s(I)` for polynomially bounded nonnegative
integers `p(I),s(I)` therefore requires only polynomially many random
bits and coefficient bits. The precise
budget must be combined with the independent growth tail, hull-shrinkage
bound, and exact-fallback cost of a complete algorithm.

The successful patch also supports polynomial-bit weak convex
optimization and evaluation, by the same epigraph argument used in
[the convex-patch evaluation lemma](convex-patch-evaluation.md). The
extra order constraints do not require a supplied primal-slack bound:

1. Compute the affine hull of `C` by rational linear programming and
   linear algebra. A displayed inequality is an equality throughout
   `C` exactly when its maximum slack is zero. Eliminate these universal
   equalities in rational affine coordinates.
2. For each remaining inequality, find a rational point of `C` with
   positive slack by an LP. Averaging these points gives a rational
   relative-interior point with positive slack in every remaining row.
   Rational LP bounds and the usual determinant bound show that these
   points, the affine coordinates, and the average have polynomial
   encoding length. Thus the least positive slack, divided by one plus
   the largest row one-norm, is a rational inner radius at least
   `2^-poly(I_patch)` in the reduced coordinates. This gives an inner
   ball of polynomial logarithmic
   radius. The outer radius has the same encoding bound. A
   zero-dimensional patch is evaluated directly.
3. Compute a rational bound `V>=max_C |F_gamma|`. The convex epigraph
   truncated above at `V+2` contains a ball about the relative-interior
   point at height `V+1`, with radius the smaller of the preceding inner
   radius and `1/2`. Check the linear inequalities first. At a point
   with feasible spatial coordinates, rational objective and gradient
   evaluation supply the epigraph separating plane. Rational ellipsoid
   weak optimization therefore computes
   value approximations in work polynomial in the patch input and the
   requested number of accuracy bits.

### Rational feasibility repair and the weak-optimization gap

The weak-optimization oracle used in the linked evaluation lemma returns
a point near the epigraph and compares it against the eroded epigraph.
Both errors must be accounted for here as well. The following order
repair replaces coordinatewise box clipping.

Write the block patch as interval bounds `ell_i<=z_i<=u_i` and
order inequalities, and include each vertex as its own predecessor and
successor. Propagate the bounds by reachability:

```text
L_i = max_(k reaches i) ell_k,
U_i = min_(i reaches k) u_k.
```

Nonemptiness gives `L_i<=U_i`; these propagated bounds describe the
same patch. For an arbitrary rational vector `z`, first clip its
coordinates to these intervals, obtaining `v`, and then set

```text
y_i = max_(k reaches i) v_k.                               (16)
```

This rational vector is feasible. In particular, propagated upper
bounds are nondecreasing along the order, so every predecessor value
used in (16) is at most `U_i`. If `bar z` is any feasible vector,
clipping does not increase its coordinatewise error, and order
feasibility of `bar z` gives

```text
||y-bar z||_infinity <= ||z-bar z||_infinity.                (17)
```

Indeed, `y_i>=v_i>=bar z_i-epsilon`, while every predecessor term is
at most `bar z_k+epsilon<=bar z_i+epsilon` when the error on the
right is `epsilon`.

Let `r_K` be the rational inner radius of the epigraph in the reduced
affine coordinates. Let `E` be the rational matrix mapping those
coordinates back to block coordinates, and take a rational
`L>=max{1,max_i sum_j |E_ij|}`. Also bound the restricted objective's
gradient one-norm on `C` by a rational `G`. Define

```text
A = 1+(2V+1)/r_K,
C_eval = G L+2+(2V+1)/r_K,
epsilon = min{r_K/2, eta/C_eval},                           (18)
```

where `eta>0` is the requested objective interval width. The inner-ball
convex-combination argument in the linked evaluation lemma shows that
the eroded epigraph is nonempty and that the oracle's returned height
satisfies `t<=f*+A epsilon`, where `f*` is the patch optimum. Its
near-feasibility guarantee supplies an epigraph point
`(bar z,bar t)` with block-coordinate infinity error at most
`L epsilon` and height error at most `epsilon`.

Apply (16) to the returned block vector. By (17) and the gradient bound,
the exactly feasible rational point `y` satisfies

```text
U := F_gamma(b+B y) <= t+(G L+1) epsilon.
```

Thus

```text
[t-A epsilon, U]                                           (19)
```

contains the exact optimum and has width at most `eta`. Every constant
and every operation in this repair has polynomial bit complexity.
This supplies exactly feasible rational evaluation points and certified
objective intervals, rather than assuming exact feasibility of the weak
oracle's output. The same repair is used in Section 7 of
[the sparse order-polytope composition](smoothed-sparse-order-polynomial.md).

For the patch optimizer `z*`, constrained first-order optimality and
(14) give, for every feasible `y`,

```text
F_gamma(b+B y)-f* >= (g_0/2) ||B(y-z*)||^2.                 (20)
```

Consequently, taking `eta<=g_0 epsilon_x^2/2` in (18) gives an
exactly feasible rational point within Euclidean distance `epsilon_x`
of the optimizer in the original coordinates. The required precision
still has polynomial bit length. These are evaluation guarantees for
the exact implicit patch output, not expanded algebraic
coordinate-output guarantees.

## 5. Scope

Point growth and a small hull alone do not force ambient Hessian
positivity or finite active-face identification. The positive linear
gaps are the missing condition. This note proves their sound use and an
explicit finite-noise tail, without choosing or requiring unique KKT
multipliers.

To obtain a complete expected sparse optimization theorem, one must
separately justify feasible rounding, sparse pruning with true feasible
witnesses, expected table counts, a fixed finite-noise growth tail, and a
rare exact fallback for this constrained domain. The face-closure work
is polynomial per invocation and does not add a graph-width requirement.

The argument was checked analytically. No executable tests, project-wide
verification, CI inspection, or literature search were performed.
