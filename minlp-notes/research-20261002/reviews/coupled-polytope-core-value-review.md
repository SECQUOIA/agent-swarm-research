# Independent review of coupled-polytope core value evaluation

Date: 2026-10-02. Verdict: **passed**. This is a fresh actual-file
review of the [coupled-polytope theorem](../new-direction/coupled-polytope-core-value-oracle.md)
and its full [convex-value and fallback interface](../new-direction/convex-polytope-value-interface.md).
I also read the separate interface review and saved diagnostic results.
No substantive mathematical correction is requested. The prior
[all-scale review](all-scale-core-value-oracle-review.md) supplies the
independent audit of the geometric and finite-law ingredients reused here.

## 1. The convex cell oracle handles actual coupled feasibility

The corrected cell objective is the supplied convexification plus an
affine function. On the cell its difference from the original objective
is nonnegative and at most `e=alpha k h^2/8`. Convexity is required on
the feasible polytope, not on an ambient box. The premise and its
verification are explicitly charged; integer feasibility is not silently
included in this oracle.

The companion interface resolves lower-dimensional cells correctly.
Exact row-slack LPs find the universally tight inequalities. Averaging
positive-slack witnesses makes every other row strict simultaneously,
which proves that the tight equations define the entire affine hull.
The rational nullspace basis can use original free coordinates as its
parameters, so their supplied widths bound the reduced domain. Positive
reduced slacks give the rational relative inner radius. All these
quantities have polynomial encoding length in the cell input, including
its dyadic level. Small physical widths affect bit lengths rather than
the number of cells. A zero-dimensional cell is evaluated directly.

The relative epigraph's claimed inner and outer balls are valid.
Checking linear domain inequalities before the tangent separator avoids
using convexity outside the feasible polytope. The cited GLS contract is
the reviewed near-feasible/eroded-body contract, rather than an unsupported
exact-feasible promise.

Its rational error-box feasibility repair is sound. A nearby true
epigraph point proves that the LP intersects the reduced polytope. Every
returned point is at infinity distance at most `2 epsilon` from that
nearby feasible point. The gradient one-norm bound therefore gives the
stated `1+2G` objective correction with no missing dimension factor.
This step preserves coupled equalities; coordinate clipping would not.

The final tangent certificate also checks independently. For constraints
`Ax<=b`, the dual signs `lambda>=0`, `A'lambda=-g` give the lower linear
value `-b'lambda`. Exact primal-dual equality proves the tangent LP
optimum, including on lower-dimensional polytopes. The segment to its
minimizer lies in the feasible set, so the stated Taylor estimate converts
a sufficiently accurate feasible value approximation to the required
tangent gap. The certificate can be checked without reproducing the
ellipsoid computation.

## 2. Lower bounds, witnesses and coverage have the correct errors

A convex cell answer of gap `e` gives original objective upper error
at most `2e`. A cell containing an optimizer is never discarded, hence
the final level incumbent satisfies `U-f*<=2e`. Conversely every queried
nonempty cell has lower bound at least `U-2e`. Earlier removed cells
had bounds above their earlier, no-smaller incumbents. Along with the
empty-cell LP certificates, this proves coverage and the interval
`[U-2e,U]` globally.

Filtering against the final incumbent is important and is explicit.
Each retained cell's own feasible witness has true gap at most `4e`.
No feasible corner or coordinate-rounding assumption enters these
inequalities. The entire cell can contain infeasible points; only its
intersection is used by the optimization oracle.

## 3. Whole-cell packing removes the projection regularity issue

The projected near-optimal set is compact because it is the projection
of a compact joint sublevel set. This avoids assuming continuity of
a partial value function on the projected domain. Conjugacy can likewise
be defined directly by maximizing over the compact joint polytope.
Its subgradients lie in the unit core box even when the projection is
lower-dimensional.

Every retained full cell lies within infinity distance `h` of the core
component of its near-optimal witness. It is therefore contained in
`conv(S_h)+[-h,h]^k`. The distinct full cells have disjoint interiors;
their volumes may be counted even though they are not feasible subsets.
The maximum-simplex volume bound yields `2^k A` retained cells and
`4^k W` generated children. Padding handles even a singleton projection.

The changed padding constant was independently recalculated. Its norm
is at most `sqrt(k)h`. The three Fenchel-residual contributions are
`(1/2+1+1/2) alpha k h^2=2 alpha k h^2`. Strong convexity puts the
inverse gradient within `2 sqrt(k) alpha h`, strictly inside the retained
open radius `4k alpha h`. Thus the predecessor's local mass bound and
all-scale weak first-moment constant apply unchanged. No full-dimensional
projection or differentiable value function has been inserted into this
transfer.

## 4. The finite law and fallback keep their bit separation

The strict determinant event uses feasible joint witnesses in the
existential block and one shared universally quantified competitor in
the original polytope. Linear membership constraints do not add a block.
The saved QR and product-chain representation keeps explicit polynomial
size and degree at most `max(d,2)`. The uniform scalar-section bound
therefore applies under mixed continuous/discrete conditioning, including
exceptional atoms and arbitrary threshold values.

The fallback explicitly replaces box membership by rational polytope
membership in the canonical scalar two-block formulas. Compactness
preserves the common lexicographic optimizer used to identify coordinates.
Refining those coordinates and intersecting the original polytope with
their rational error box supplies an exactly feasible rational point.
The true optimizer witnesses nonemptiness. The gradient bound then gives
the stated objective precision. The reviewed base-only exponential
factor remains separated from sampled coefficient height and requested
accuracy; the extra rational LP only enlarges fixed polynomial factors.

The cap is checked before child generation, including potentially empty
cells whose feasibility tests still cost work. Any cap at any precision
implies the same event `W>B`. Integrating the weak tail pays for both
the truncated ordinary count and the same-draw exact fallback. All LP
and polynomial operations at level `j` have input length polynomial in
`I+j`. The finite law is chosen before sampling and does not depend on
future query precision. The single pathwise random work factor therefore
has the stated expectation uniformly over all queries.

## 5. Scope and verification

The result supplies an exact value Cauchy name and feasible objective-gap
points, not optimizer-coordinate convergence. It broadens feasibility
relative to the product theorem but uses the supplied convexifier
`alpha`, which can be much larger than original coordinate curvature.
For example, `F(v,z)=(v^2+z^2)/2+M v z` has core upper curvature one
and residual modulus one, while its core-only quadratic convexifier
requires `alpha>=M^2-1` when `M>1`.

The interpretation using sums of nonnegative weighted fourth powers
and a convex quadratic provides a direct verifiable nonlinear family.
The equality lifting and normalization also check: after a factor
coordinate is written as an offset plus width times a unit coordinate,
`alpha max_i width_i^2` leaves a positive-semidefinite diagonal correction
and an affine translation term. Widths and noise directions must change
as stated. This does not establish a width-free or parameter-preserving
equivalence to every low-rank nonconvex problem.

I read the saved diagnostic JSON: it reports 108 levels, 391 generated
cells, 337 tangent dual certificates, 246 noncorner points, 108 global
intervals and 81 feasibility repairs, including lower-dimensional and
101-bit thin domains. These are the author's separately executed checks;
I did not rerun them or claim they implement the general GLS/QE oracle.
My verification here is the independent actual-file proof audit and a
targeted local check of this review's links, whitespace and control
characters. No project-wide test, CI inspection or index edit was made.
