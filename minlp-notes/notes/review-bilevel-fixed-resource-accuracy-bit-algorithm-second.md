# Second independent audit of fixed-resource accuracy-bit bilevel optimization

Date: 2026-09-05. Reviewer: fixed_resource_audit_second.

**Verdict: PASS for the stated positive-coefficient, fixed-resource theorem.**
The proof in [the candidate note](bilevel-fixed-resource-accuracy-bit-algorithm.md)
gives polynomial dependence on numerical degree and requested accuracy bits,
with an exactly feasible rational leader. I found no substantive mathematical
or bit-complexity correction. This review was conducted without reading the
first review. It checks correctness, not publication priority.

The audited scope fixes the leader dimension and the number of resource
inequalities; allows arbitrary signed rational resource coefficients that are
independent of the leader; and requires strictly increasing polynomial
marginals with nonnegative coefficients. The leader objective is affine in
leaders and responses, with arbitrary coefficient signs. Additional upper
constraints on the response are outside the result.

## Exact feasible leaders

The separation characterization is correct: the feasible resource right-hand
sides form `C[0,1]^N+R_+^k`, whose finite lower support functionals have
nonnegative coefficients. On each cone cut out by the column hyperplanes and
coordinate hyperplanes, that lower support function is linear.

Every cone is pointed because it is contained in the nonnegative orthant.
Every extreme ray is the nullspace of `k-1` independent active hyperplanes.
This remains true for lower-dimensional cones: their defining equalities
contribute to those active hyperplanes. Enumerating all independent subsets,
checking the two ray directions for nonnegativity, and retaining every valid
direction includes every needed ray. Extra nonnegative directions only impose
valid inequalities. Coordinate hyperplanes handle rank-deficient matrices and
zero columns. The separate `k=0` treatment and the empty-subset convention for
`k=1` are consistent.

For fixed `k`, ray enumeration and determinant encodings are polynomial. The
resulting explicit rational leader polytope is exact, including its boundary.

## Multipliers and the repair constant

The integer Gram-matrix argument works with real right-hand sides. A
nonnegative combination of finitely many normals can be reduced to linearly
independent normals by eliminating a coefficient along a linear dependence.
For that independent set, the Gram determinant is a positive integer.

With at most `N` rows and entries bounded by `M`, the claimed `V` dominates
every Gram cofactor. The inverse formula bounds a single coefficient by
`N^(3/2) M V ||v||_2` and their sum by
`N^(5/2) M V ||v||_2`; the displayed integer-power bounds are conservative.
For a gradient with infinity norm at most `Gbar`, these bounds give the
claimed multiplier box after multiplication by the common denominator `D`.
There is no hidden assumption that the optimal gradient or multiplier is
rational.

The polyhedral normal-cone formula applies at a lower-dimensional feasible
face without Slater's condition. It therefore supplies both stationarity and
complementarity for a multiplier in the common compact box.

For Euclidean projection of a box point `q`, the projection normal is also a
nonnegative combination of active normals. Active box rows have nonpositive
violation at `q`; active resource rows have violation at most `D delta` after
scaling. Taking the scalar product with `q-y` proves the stated bound
`||q-y||_infinity <= K delta`. The argument does not require computing the
projection. In the zero-distance case there is no division to perform.

The integers `D,M,V,K` can be exponentially large in value, but have
polynomial bit length. Only logarithms of their magnitudes enter the eventual
approximation precision.

## Response control

The box Lagrangian separates and has the claimed unique clipped-inverse
response. Weak duality has the sign used in the proof:

```
F_x(q)+lambda^T(Cq-b) <= F_x(z*).
```

After repairing `q` to a feasible `y`, the Lipschitz estimate gives an upper
objective gap of `L K delta+zeta`. The lower gap is nonnegative by follower
optimality.

The power Bregman inequality is valid in both directions. If `u>=v`, its
integrand is `(v+t)^j-v^j>=t^j`; if `u<v`, its integrand is
`v^j-(v-t)^j>=t^j` for `0<=t<=v-u`. Integrating gives
`|u-v|^(j+1)/(j+1)`. Since the distance is at most one and `j<=P`,
nonnegative coefficients then give the uniform exponent `P+1` and constant
`mu=min_i G_i/(P+1)`. The affine cost terms cancel in the Bregman divergence.
The first-order term at the constrained optimum is nonnegative.

The triangle inequality with the repair distance proves equation (8).
This is sufficient even when the marginal derivative vanishes at zero.

The continuity and attainment argument is also valid. Uniformly bounded
optimal multipliers have convergent subsequences. Continuity of the clipped
inverses, resource feasibility, and complementarity pass to the limit.
The limiting KKT point is the unique follower optimum. Thus the response and
upper objective are continuous on the compact exact feasible-leader polytope.

## Surrogates, algebraic optimization, and rational output

The reviewed positive-polynomial inverse construction supplies rational
breakpoints and branches, including a uniform guarantee at both ends of each
branch. After substituting affine targets, the arrangement has fixed dimension
`r+k` and polynomially many cells. Lower-dimensional cells and closed branch
boundaries do not invalidate the approximation guarantee.

Polynomial expansions remain polynomial in size because their number of
variables is fixed. A true leader optimum and one bounded optimal multiplier
belong to a nonempty surrogate set: approximation changes each resource
residual by at most `S eta` and complementarity by at most
`k Lambda S eta`.

Each surrogate set is compact. Fixed-variable real algebraic optimization
applies even though its polynomial inequalities are nonconvex. A minimizer
formula compares two points and uses `2(r+k)` variables; the follower count
does not enter that dimension. Exact algebraic sample and comparison degrees
remain polynomial in this fixed-dimensional setting. No common field for all
original follower inverse values is required.

A rational cell has polynomially many rational vertices with polynomial
encodings in fixed dimension. Caratheodory's theorem places the algebraic
minimizer in a simplex of at most `r+k+1` of these vertices. Enumerating such
simplices and testing barycentric feasibility is polynomial. Rounding the
nonnegative barycentric weights down and assigning the remainder to one
vertex preserves the cell exactly, including its affine equalities.

The coefficient-sum gradient bound is valid on the unit cube after the dual
normalization. It supplies polynomial-bit rounding accuracy for every
surrogate residual, complementarity polynomial, and objective. The rounded
point need not satisfy the original nonlinear surrogate constraints exactly;
the proof explicitly enlarges their residual allowances and accounts for the
enlargement. Exact leader feasibility is preserved by membership in the
rational cell.

## Error ledger

At the rounded point, the true box response obeys

```
delta=3 S eta,
zeta=3 k Lambda S eta.
```

The chosen `eta` gives `K delta<=tau/2` and
`((L K delta+zeta)/mu)^(1/(P+1))<=tau/2`. Thus its distance to the
true resource-constrained response is at most `tau`.

Since `eta<=tau=epsilon/[16(1+A_c)]`, replacing the true response by the
polynomial response changes the leader objective by at most `epsilon/8`.
The surrogate optimum contributes at most `epsilon/16`, and rational
rounding contributes at most `epsilon/8`. The final upper gap is at most
`5 epsilon/16`. The returned rational polynomial value is at most
`OPT+3 epsilon/16` and at least `OPT-epsilon/8`, as stated.

The factor `(tau/2)^(P+1)` costs `O(P log(1/tau))` bits. Consequently the
construction is polynomial in numerical degree, not in its logarithm for
sparse binary powers. The proof returns an exactly feasible rational leader
and a rational objective estimate; it does not claim an exact rational
follower response.

## Exact diagnostic

The independent standard-library
[Fraction checker](../code/bilevel_bounded_power/check_fixed_resource_second.py)
passed:

- 1,134 Bregman inequalities, covering both argument orders, degrees through
  12, and mixed coefficients ranging from `2^-30` to `2^20`.
- 216 residual-transfer cases with signed and rational resource matrices,
  duplicated equality rows, zero rows, box endpoints, and nearby as well as
  distant multiplier perturbations.
- 124 nonzero feasibility repairs; all 216 projected faces had dependent
  active constraints.

The projection check independently enumerates faces of a two-dimensional
bounded polygon. It verifies weak duality, the repair bound, the objective-gap
transfer using the actual repair distance, the constrained Bregman bound,
and equation (8) without floating-point roots. These finite checks supplement
the proof; they do not establish its arbitrary-dimensional statements.

Run:

```
python code/bilevel_bounded_power/check_fixed_resource_second.py
```

No change to the main theorem was needed. The empty-follower case, if allowed
by an implementation's input convention, is the immediate leader LP with
the affine feasibility inequalities `0<=b(x)`; the displayed conditioning
construction explicitly treats `N>=1`.

## Addendum: arbitrary signed polynomial marginals

**Verdict: PASS for Section 8 and the one-resource transfer.** This addendum
independently checks the new uniform-convexity argument and the use of the
general inverse interface. It relies on the separately twice-audited
[general inverse lemma](certified-monotone-polynomial-inverse-approximation.md)
for its analytic approximation construction; this review does not constitute
a third full audit of that analytic construction.

For a normalized increasing degree-`d` polynomial on `[0,1]`, interpolation
of `g-g(a)` at the equally spaced nodes of `[a,a+s]` is exact. Its node values
lie between zero and the marginal increment. Each numerator factor of a
Lagrange basis polynomial has magnitude at most one when evaluated at zero
or one. The denominator is exactly `(s/d)^d j!(d-j)!` in magnitude.
The sum of reciprocal factorial products is `2^d/d!<=2^d`.
Bounding both endpoint values and subtracting gives equation (14), including
its factor `1/2`. The zero-displacement case follows directly.

For either ordering of the two Bregman arguments, integrate over distances
between `s/2` and `s` from the base point. Every marginal difference there
contains an interval of length at least `s/2`; equation (14) bounds it below
by `G_i(s/(4d))^d/2`. Multiplication by the integration length `s/2` gives
`G_i s^(d+1)/[4(4d)^d]`. Since `d<=P` and `s<=1`, replacing this by
`G_i s^(P+1)/[4(4P)^P]` is valid. Thus the replacement constant
`mu=min_i G_i/[4(4P)^P]` has precisely the required property.

After shifting the marginal's constant term into the affine target, strict
increase implies `0<=g_i(z)<=G_i` on the follower box. The original gradient
bound and multiplier bound therefore remain valid despite coefficient
cancellation. The rational normalization by `G_i>0` and the new `mu` retain
polynomial bit length in dense input and numerical degree. The general
inverse lemma's polynomial branch count, degree, and coefficient bounds are
all that the fixed-dimensional construction uses; the sharper bounds of the
positive-coefficient lemma are unnecessary. Every residual and rounding
allowance in Sections 5–6 is unchanged after this substitution of `mu`.

I also read the original one-resource proof and checked its
[Section 9 transfer](../results/bilevel-one-resource-accuracy-bit-algorithm.md).
The endpoint multiplier bounds use only the clipping thresholds `0,G_i`.
The signed no-cancellation identity uses only monotonicity of the inverse;
zero weights still have no multiplier dependence. Exact leader feasibility,
continuity, the arrangement construction, relaxed balance, and rational
rounding consequently apply to arbitrary strictly increasing polynomial
marginals. That proof needs no Bregman or derivative lower bound. Replacing
its inverse approximation dependency leaves its error ledger intact; the
explicit positive-coefficient branch-count estimate is replaced by the
general polynomial bound, as its Section 9 states.

The exact checker adds 486 signed-polynomial cases. It uses normalized odd
shifted powers of degrees 3, 5, and 7 centered at `1/2` and `1/3`. These have
negative polynomial coefficients and a zero derivative at an interior point.
For both argument orders on a rational grid, all interpolation-modulus and
Bregman inequalities pass using exact fractions. These diagnostics test the
new scalar bounds, independently of the positive-coefficient cases.
