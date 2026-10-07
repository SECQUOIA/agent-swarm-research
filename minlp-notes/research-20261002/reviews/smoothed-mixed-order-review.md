# Independent review of the mixed order-polytope theorem

Date: 2026-10-02. Verdict: **pass** after the bag-binary noise constant
was made explicit. This review read the actual
[mixed theorem](../new-direction/smoothed-mixed-order-polynomial.md),
the reviewed [continuous theorem](../new-direction/smoothed-sparse-order-polynomial.md),
and its [count](../new-direction/order-polytope-cell-count.md) and
[face-closure](../new-direction/order-polytope-face-closure.md) interfaces.
The final stronger directional constant was checked independently.
No mathematical blocker remains under the stated full-Hessian premise.
This is an internal proof review, not a priority assessment.

## 1. Transport preserves the mixed domain

For a deterministic feasible bag tuple, fix its binary row and all noise
outside its continuous bag coordinates. A conditional minimizer exists
by compactness and can be chosen independently of the still-unconditioned
continuous bag noises. The original value must include the fixed binary
bag noise constant when it is compared with the full global optimum.
The revised definition does so. This constant then cancels from all
directional comparisons.

Take the minimal standard order-simplex face whose relative interior
contains the source tuple. Its endpoint groups and tied groups are fixed
as specified by that face. The piecewise-affine nondecreasing scalar map
that fixes zero and one and maps the source's interior knots to the target
knots preserves every order inequality. All binary coordinates, including
outside binary coordinates, are unchanged. The target may merge knots or
move an interior knot to an endpoint. No interpolation between different
binary assignments is used.

For a fixed source full point, the resulting full vector is affine in the
target bag tuple. Each continuous row has nonnegative coefficients of
sum at most one; binary rows have zero derivative. Hence the squared
operator norm is at most `N`, the number of continuous coordinates.
Applying the full Hessian upper bound to the same transported point for
both signs gives the asserted two-sided upper comparison. Neither
stationarity nor first-order optimality of the conditional minimizer is
needed for this argument.

The original projected mixed fiber need not be convex. For instance,
`v<=z<=w`, with binary `z`, projects to the union of `v=0` and `w=1`
inside the continuous order triangle. The two projected points `(0,0)`
and `(1,1)` are feasible while their midpoint is not. This does not
invalidate the proof: a feasible source in the relative interior of one
simplex face transports to that entire closed face. The algorithm need
not enumerate this union of faces.

Endpoint changes of the minimizing outside binary label also cause no
gap. Under `v<=z`, binary `z`, minimizing `z` gives value zero at `v=0`
and one at every `v>0`. Transporting the interior minimizer to zero gives
an upper support of value one, while the actual value is smaller. The
proof uses this inequality in the correct direction. It does not move
a source endpoint group into a larger face or identify a transported
fiber with the entire target fiber.

## 2. The sharper count and conditioning

For each standard face, the consecutive vertex differences have disjoint
nonempty supports and entries in `{0,1}`. If `J` is the preceding affine
transport Jacobian and `a` is such a direction, then

```
0 <= (Ja)_i <= 1 on continuous coordinates,
(Ja)_i = 0 on binary coordinates,
||Ja||² <= N.
```

Thus the relevant directional upper curvature is `NH`, independently of
the support size of `a`. Both neighbors use this same source transport,
including when a target knot merges with another knot or an endpoint.
The noise interval length is `(NH+2 eta)h`, improving the earlier
`(cNH+2 eta)h` estimate. At the retained-witness tolerance `eta=NH/4`,
the stated bracket `2+3NH/(4sigma)` follows when `Mh>=1`.

The interval endpoints depend only on the conditioned coefficients and
the deterministic source tuple. After one coordinate is selected from
each disjoint support, conditioning on the remaining bag noises leaves
independent scalar uniforms. Taking the product of the interval masses
is therefore valid. The global optimum appears only in the implication
from true near-optimality to these tests; its dependence on the sampled
coefficients does not make the resulting intervals random under this
conditioning.

The face point count `binom(r-1,k)<=r^k/k!`, the number of standard
simplex faces, and the sum over `2^z` fixed binary bag rows give formula
(6). Zero continuous bag dimension gives the correct value `2^z`.
Replacing bag quantities by their maxima and including cell incidences,
children and corners yields

```
C_0^p q! (q+1) [2+3NH/(4sigma)]^q poly_d(I).
```

These are counts of deterministic original-grid tuples, not a conditional
distribution given earlier pruning. A separate focused proof review
independently checked the transport, endpoint cases, conditioning, and
this improved directional bound.

## 3. Binary identification precedes continuous face exposure

Common-threshold rounding fixes every binary coordinate and preserves all
order inequalities. Only the `N` continuous coordinates contribute
variance, so `E=NHh²/8` is valid. The sparse min-marginal argument supplies
one consistent feasible witness of gap at most `2E` per retained cell.
Binary cells are singleton labels from level one onward. Under point
growth, a retained wrong label would itself contribute Euclidean distance
at least one, contradicting the witness radius at the stated cutoff.
This justifies eventual binary identification without enumerating all
binary assignments in the algorithm.

The prohibition on early continuous exposure tests is essential. Consider

```
0<=x<=z<=1, z binary,
F(x,z)=(x-1/2)²+10z²-11z.
```

The unique mixed optimum is `(1/2,1)`, of value `-1`, and the mixed
point-growth modulus is exactly one. Its full gradient is `(0,9)`.
On the continuous relaxation, the linear minimum is zero, while the
opposite vertex face for the proposed equality `x=z` has cost nine.
The relaxed exposure test would falsely force `x=z`. Once `z=1` is
fixed, the continuous slice gradient is zero and this false test does
not arise. The actual algorithm follows this latter order.

After all binary hulls are singleton, every original optimizer belongs
to the same continuous slice. That slice is convex with zero-one
vertices, even when some continuous coordinates are already fixed by
binary neighbors. First-order optimality and the continuous LP gap
certificate apply on precisely this slice. The `N delta` comparison is
sound. Bound propagation, cycle contraction, singleton removal and
retaining all other order inequalities preserve every original optimum.

The block substitution has squared norm at most `N`. The Hessian
variation bound `NT r_y` is therefore safe. Positive full-domain growth
gives restricted Hessian at least `2g_0 D'D`, hence at least `2g_0 I`,
on the minimal continuous face. The stated cutoff gives enough slack
for the rational positive-definite matrix test. No quantitative lower
bound on inactive primal slacks is used.

## 4. Tails, fixed noise law and exact output

Binary membership can be encoded by `x_i(x_i-1)=0`. Adding these and the
order atoms to the already reviewed growth and canonical-fallback
formulas preserves their fixed number of quantifier blocks and fixed
degree. Their format depends on the original input; the sampled
coefficient length enters only the polynomial height factor.

For exposure gaps, the analysis unions over the at most `2^s` binary
assignments. It does not condition the noise on the assignment selected
by the optimizer or by pruning. On any fixed slice, binary noises add
a constant and may be conditioned. Positive global growth makes each
relevant slice-face stationary root nonsingular. The isolated-root
count, followed by the two-coefficient fixed-sum count for an active
continuous order edge, gives the stated `K(tau/sigma+2/M)` bound.
Bound proposals use a single continuous coefficient. Empty opposite
faces are correctly excluded as infinite-gap events.

The thresholds and cutoff precede the choice of `M`. The growth and gap
events each cost at most `rho`; their sum pays the base-exponential
same-draw fallback cost. Thus the finite noise law does not change on
an exceptional draw, and no coefficient-height circularity is present.

The successful output is a fixed binary assignment and a rational
continuous convex patch. Its polynomial-size descriptor is correctly
distinguished from the pruning trace's expected-size bound. The
continuous order-patch evaluator already includes relative affine-hull
reduction, polynomial-bit ball data, and the near-feasible weak-oracle
cleanup. For fallback evaluation, binary labels are identified first.
Propagating their endpoint bounds before continuous clipping and
predecessor maxima prevents an approximate predecessor from changing a
binary zero. This repair preserves all identified labels and does not
increase infinity-norm error from the exact feasible point.

The all-binary case uses ordinary finite-state tree DP and needs none of
these smoothing or closure arguments. No claim for larger integer ranges
or arbitrary coupled linear constraints has been inferred.

## 5. Distinct targeted diagnostics

The command actually run for this review was

```text
python research-20261002/reviews/check_mixed_order_transport_review.py
```

The [checker](check_mixed_order_transport_review.py) and
[saved report](mixed-order-transport-review-results.json) passed 238
endpoint transports from 70 feasible sources on chain, fork and cyclic
mixed order systems, 42 two-sided directional curvature checks, and 40
binary-preserving feasibility repairs. All calculations used exact
fractions. The checker also verifies the nonconvex projection example
and the premature-exposure counterexample above, whose false gap is nine.
These are finite diagnostics, not a complexity experiment or a full
implementation of the stochastic algorithm.

The author's separate conditional-recourse and finite-noise-count
diagnostic was not rerun here. Targeted document checks covered this
review's local links, whitespace and paired delimiters, and the new
checker's Python syntax and saved JSON. No index, project-wide test, CI
inspection or external source search was performed.
