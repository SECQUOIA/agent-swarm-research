# Core-only smoothing with separable convex integer recourse over TU systems

Date: 2026-10-02. Status: passed a
[fresh independent review](../reviews/smoothed-core-tu-recourse-review.md),
including a separate review of the bounded-slack inequality corollary.
The flow theorem is separately reviewed. No index or publication-priority claim.

The [boundary-flow theorem](smoothed-boundary-core-flow.md) extends from
network incidence matrices to totally unimodular equality systems. Two
replacements are needed: a small rational dual linear program replaces
shortest paths, and conformal TU circuits replace directed cycles. Both
preserve the optimal-interval certificate and its base-only chart bounds.

## 1. Model and conclusions

Let `A` be an integer totally unimodular matrix, `b` integral, and

```
Y={z in Z^r:Az=b, ell<=z<=u}
```

nonempty, with finite integral bounds encoded in binary. Let

```
F_gamma(v,z)=phi(v)+sum_i f_i(v,z_i)+gamma'v,
v in [0,1]^k.
```

The polynomials are explicit and rational, of fixed degree at most `d>=1`.
Each `f_i(v,.)` is convex on its native real interval for every core point.
The core changes costs only. Supply a valid coordinate upper-curvature
bound `L>0`, and let the rational noise half-width be `sigma>0`. Include
these valid premises and any required verification data in the original
input length `I`. The preprocessing below has polynomial encoding length
in this original input. The TU hypothesis is a valid premise of the theorem.

The general conclusion is the [boundary theorem's](smoothed-boundary-core-flow.md)

```
expected work f_d(k)[3+(1+k/2)L/(2sigma)]^k poly_d(I),
sample length log M<=f_d(k) poly_d(I).                    (1)
```

One fixed finite rational law perturbs only the `k` core coefficients:
independently sample each from
`{-sigma+2sigma j/(M-1):j=0,...,M-1}`, with the base-chosen power of two `M`.
Every draw is solved exactly, including ties and arbitrary core boundary
optima, with a same-draw fallback. There is no parameter for residual
dimension, numerical interval widths or matrix rank. Exact common-root
output and `t`-bit refinement have bounds `f_d(k) poly_d(I)` and
`f_d(k) poly_d(I+t)` on every draw. Quadratic fixed-label core objectives
permit rational output.

For the more structured class

```
F_gamma(v,z)=phi(v)+sum_i psi_i(z_i)+v'Bz+gamma'v,          (2)
```

take the fixed degree bound at least two when `B` is nonzero. The sharper
[bilinear-flow bound](smoothed-bilinear-core-flow.md) transfers:

```
[8^k[3+(1+k/2)L/(2sigma)]^k+c_d^k] poly_d(I),
log M=poly_d(I),                                         (3)
```

where `L` only bounds the coordinate curvature of `phi`. Coupling magnitudes
and capacities enter through their binary lengths and the precision budget,
not through this curvature bound. The all-draw output and refinement bounds
in this case are `c_d^k poly_d(I)` and `c_d^k poly_d(I+t)`.

The exact separable-convex integer oracle for TU systems is the verified
Hochbaum--Shanthikumar interface in the
[recourse source audit](../prior-art/integer-convex-flow-recourse-prior.md).
Tightening integer coordinate bounds preserves the same matrix class.
After fixing the rational core, polynomial evaluations have polynomial bit
length. Tangent-line extensions outside the original intervals supply
globally convex costs if required by the oracle. This is the established
oracle, not a new integer optimization algorithm.

Substitute fixed native coordinates first. Discard dependent equality rows
after checking consistency of their right-hand sides; retain original rows,
so TU is preserved. Write `m=rank A<=r` for the remaining row count. The
remaining native intervals all have positive integer length. If `r=0`,
solve the small core directly. If `m=0`, the dual below has no variables
and the scalar intervals give the certificate directly. For `k=0`, use the
exact integer oracle.

## 2. A compact exact dual certificate at an integer optimum

At a rational core point `c`, let `z^0` be an exact integer optimum. For
each scalar convex cost, interpolate its values at consecutive integers
linearly. Extend past the two endpoints with the adjacent endpoint slopes.
The resulting function is convex and piecewise linear.

Minimizing this interpolant over the real polytope
`Az=b, ell<=z<=u` has the same value as the integer problem. On every
integer grid cell, the interpolant is affine and the feasible intersection
is an integral polytope: its constraint matrix consists of `A` and signed
unit rows, and all right-hand sides are integral. Thus an optimum in any
nonempty cell can be chosen at an integer vertex. There are finitely many
cells. In particular the given integer optimum is also a real interpolant
optimum.

Linear-program duality for this convex piecewise-linear problem supplies
`lambda in R^m` satisfying the following adjacent-slope inequalities:

```
f_i(c,z^0_i)-f_i(c,z^0_i-1) <= (A'lambda)_i
     if z^0_i>ell_i,
(A'lambda)_i <= f_i(c,z^0_i+1)-f_i(c,z^0_i)
     if z^0_i<u_i.                                      (4)
```

Equivalently, every scalar adjusted cost

```
g_i(c,t)=f_i(c,t)-(A'lambda)_i t
```

is minimized over its native integers at `z^0_i`. At an endpoint only the
available one-sided inequality is required. This dual system has at most
`2r` inequalities; the algorithm does not construct the piecewise-linear
epigraph over all native labels. Its nonemptiness follows from the preceding
interpolation argument and LP duality, including lower-dimensional feasible
sets. Conversely, any solution of (4) is an exact optimality certificate,
because `lambda'Az=lambda'b` is constant on feasible points.

## 3. A polynomial-bit dual vertex and its symbolic chart

The inequality normals in (4) are signed columns of `A`. Every column has
at least one inequality because fixed native coordinates were removed.
The dual polyhedron has no lines: a line direction would satisfy
`A'h=0`, and full row rank gives `h=0`. A nonempty pointed polyhedron has
a vertex. Each dual vertex is determined by `m` independent active rows.
The corresponding square submatrix is a signed transpose minor of `A`,
so its determinant is `+1` or `-1`, and every inverse entry is `0,+1,-1`.

Compute a base rational bound `V>=1` on the absolute value of every native
unit marginal throughout the core cube. Fixed degree and binary native
bounds give `log V=poly_d(I)`. Cramer's rule bounds every coordinate of
every dual vertex by `mV`. Hence (4) has a solution in the base box

```
[-R,R]^m,       R=mV+1.                                  (5)
```

Find a vertex of (4) intersected with (5) in polynomial bit time, for
example by successive exact lexicographic LP minimization. The final
point is a vertex of this original bounded polyhedron. Extract `m`
independent active rows from its original inequalities, not from the
extra equalities used during lexicographic minimization.

Their coefficient matrix `C` consists of signed rows of `A'` and unit rows.
It is a nonsingular TU matrix. Their right-hand side `h(c)` consists of
unit marginal values and constants `+R,-R`. Keep this same active basis
symbolically:

```
lambda_T(v)=C^(-1) h(v).                                 (6)
```

This vector agrees with the queried multiplier at `c`. Its coefficients
have polynomial base height and core degree at most `d-1`. No sampled
query coordinate enters those coefficient bounds. The artificial box may
supply some active rows; this causes no difficulty, since its bound `R`
was chosen before sampling.

For a fixed native label there are at most `(2r+2m)^m` such ordered basis
choices, a safe overcount. The family includes every structurally valid
nonsingular choice, whether or not it occurs at a query. For each such
basis and native adjacent pair, use the original adjusted marginal

```
f_i(v,t+1)-f_i(v,t)-(A'lambda_T(v))_i.                    (7)
```

These are exactly the polynomials needed by the optimal-interval
certificate. The artificial multiplier-box inequalities are not tested
uniformly on the core hull and are not required to stay valid there;
only (7) certifies scalar optimality. The base chart count is at most

```
R_Z(2r+2m)^m R_1,
R_Z=product_i(u_i-ell_i+1),
R_1=sum_i(u_i-ell_i+1).                                  (8)
```

Its logarithm and the chart coefficient heights are polynomial in `I`.
In model (2), all these charts are affine in the core.

## 4. Optimal intervals and TU proximity

Let `I_i` be the full interval of integer minimizers of `g_i(c,.)`.
As in the flow case, the whole optimum set at `c` is exactly

```
Y_0={z in Y:z_i in I_i for all i}.                        (9)
```

The intervals are found by binary search on monotone adjacent slopes.
The potential term is constant because `Az=b`. Uniform within-interval
identities and first outside adjusted marginals then give the same
separable cost lower bound as in the flow certificate.

The required proximity bound is also unchanged:

```
for every z in Y, some bar z in Y_0 satisfies
||z-bar z||_1<=r sum_i dist(z_i,I_i).                     (10)
```

Here is the TU replacement for the cycle proof. Every nonzero integer
vector `x in ker A` has a nonzero sign-compatible circuit whose entries
belong to `{0,+1,-1}`. To see this, choose a nonzero kernel vector of
minimal support in the orthant of `x`. If the kernel on its support had
dimension greater than one, a small two-sided perturbation followed to
the boundary of that orthant would reduce its support. Thus it is a
circuit. The primitive dependence coefficients of a TU circuit are signed
minors, hence `+1` or `-1` on the support. Subtract its largest possible
integer multiple conformally from `x`; this removes at least one nonzero
coordinate. Repetition gives a conformal integer circuit decomposition.
Every circuit has one-norm at most `r`.

Choose `bar z` closest to `z` in the finite nonempty set `Y_0` and decompose
`z-bar z` this way. Every circuit must have a coordinate whose directed
unit move from `bar z` leaves `I_i`; otherwise that circuit gives a feasible
point in `Y_0` with smaller distance. Since circuit entries are unit
integers, such a coordinate is at an interval endpoint and its full
difference toward `z_i` equals its interval violation. Charge each circuit
multiplicity to one blocking coordinate. Conformality bounds its total
charge by that violation, proving (10).

The inward-derivative argument does not depend on network structure. On
a tied interval with at least three integer points, the original convex
cost is affine at the face center, so its one-sided inward derivative is
convex there. On two points use linear interpolation; substitute singleton
intervals. The same exact TU oracle minimizes these costs over (9).
Together with (10), the same Hessian and mixed-derivative bounds prove
the deterministic face-fixing inequality without any new factor.

## 5. Transfer of the finite-law proof and output

Replace the flow tree count by (8) in the boundary theorem. Nothing else
in its probability argument uses network topology. Restricted chart zeros
have the same degree and height bounds; the cross-label free-gradient
images have the same fixed-dimensional format; the normal-noise margin
still minimizes over all labels in the same tightened feasible set.
The geometric and value-margin bounds therefore choose one finite law
with the precision and expected work in (1).

All online replacements are polynomial-bit exact operations: conditional
TU optimization, the compact dual LP, extraction of its active basis,
interval binary searches and restricted derivative-cost TU optimization.
There is no enumeration of cells in the piecewise-linear interpolation,
native labels, dual bases or circuits in the ordinary search. Those finite
families justify analysis bounds only. The same-draw fallback enumerates
native labels and solves their small continuous core, exactly as before.

For (2), charts and outside tests are affine and derivative recourse is
linear over the tightened TU polytope. The elementary affine margin restores
polynomial sampling length and yields (3), with one final constant-base
small-core solve. The original numerical curvature is still that of `phi`.

The proof above concerns equalities plus bounded native variables. It does
not cover arbitrary integer matrices: the compact
separable dual certificate and the unit conformal circuit proof use TU.
The interpolation, LP duality and circuit ingredients are classical;
the claim is their compatibility with the reviewed finite-noise core
search and boundary-face certificate.

The [focused TU prior audit](../prior-art/tu-equality-separable-convex-prior.md)
verifies the exact H&S oracle and distinguishes the classical interpolation,
dual and circuit ingredients from this finite-law composition. Its precise
primary locator for the classical circuit theorem remains under source
verification; the circuit and charging proof above is self-contained.

## 6. Bounded TU inequalities

The same conclusions apply to

```
Y={z in Z^r:Cz<=b, ell<=z<=u},
```

where `C` is TU, `b,ell,u` are integral and the native box is finite.
For each row compute exactly

```
m_i=min_(ell<=z<=u) C_i z
   =sum_(j:C_ij>=0) C_ij ell_j+sum_(j:C_ij<0) C_ij u_j,
U_i=b_i-m_i.
```

If some `U_i<0`, even the native box cannot satisfy that row, so the
original problem is infeasible. Otherwise add the integral slack
`s_i=b_i-C_i z` with the **finite explicit bound** `0<=s_i<=U_i` and impose

```
Cz+s=b.
```

The matrix `[C I]` is TU. Projection onto `z` is a bijection between the
new feasible integer points and the original set: each original feasible
point has exactly the displayed slack, and its upper bound follows from
the native-box minimum. Give every slack coordinate zero scalar cost and
zero core coupling. All objective values, core derivatives and the supplied
curvature bound remain unchanged.

The number and bit lengths of the added bounds are polynomial in the
original input; they do not require enumerating native labels. Fixed slack
coordinates are handled by the existing preprocessing. The degree remains
fixed, and enlarged residual dimension is not an exponential parameter in
either (1) or (3). Applying the equality theorem and then discarding the
slacks preserves its expected work, one-law construction and exact output
claims. Rational right-hand sides can first be rounded down because `Cz`
is integral. This corollary uses the displayed finite slack bounds; no
unbounded residual coordinate is introduced.

## Verification

The [fresh actual-file review](../reviews/smoothed-core-tu-recourse-review.md)
approved the new equality-system interfaces, including degenerate duals,
box-active bases, all optimal intervals, TU circuit charging and arithmetic
transfer. It inspected the author-side checker without rerunning it. Review
of the short bounded-slack addition also passed, including finite bound
encoding, the exact projection bijection and preservation of the core
curvature and output guarantees.

The author-side exact diagnostic was run with

```sh
python3 -B research-20261002/new-direction/check_core_tu_recourse.py
```

The [checker](check_core_tu_recourse.py) passed six cost systems and 24
rational recourse queries. Its matrices include a consecutive-ones matrix
with a three-entry column, a signed row/column variant and a rank-zero
case. It checked 495 TU minors, ten feasible-label correspondences after
fixed-column and redundant-row preprocessing, and one inconsistent-row
rejection. Exact basis enumeration found 130 original compact-dual vertices
and 166 boxed-dual vertices from 620 feasible nonsingular bases.

The 166 resulting optimal-interval sets agreed with exhaustive original
optima. All 1,188 nearest-tight-label distance checks passed, together with
1,158 conformal unit-circuit steps and 7,840 symbolic adjusted-marginal
evaluations. Cases include 84 endpoint-only slope systems, 12 tied queries,
four selected multiplier-box-active bases and 150 quadratic charts. The
checker also encountered 126 chart probes infeasible away from their own
query, confirming why uniform original-marginal tests remain necessary.

These are exhaustive small-instance checks, not a production convex TU
oracle, a general TU recognizer, native-interval binary search or a large
domain experiment. No index edits or project-wide checks were made.
