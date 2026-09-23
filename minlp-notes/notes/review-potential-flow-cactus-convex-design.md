# Independent audit: continuous convex flow design on a cactus

Date: 2026-09-05. Reviewer: `benders_property`.

**PASS.** I independently checked
[the convex-design candidate](potential-flow-cactus-convex-design.md).
The rational surrogate box, convex optimization step, exact resistance
interpolation, and total error bound are valid for an arbitrary number
of cactus cycles. The output is a rational resistance scenario whose
actual physical flow has the asserted additive performance guarantee.
No rational exact physical-flow vector or exact scalar optimum is
implicitly promised. The flow-region theorem is a reviewed import;
novelty of the combined algorithm remains a separate source question.

## Geometry and objective control

The inherited cactus representation has a rational particular flow and
independent signed cycle vectors with disjoint edge supports. Each
cycle-circulation endpoint has a separate degree-at-most-two encoding,
and a rational resistance profile attaining it is available. There is
no dependence on a fixed number of cycles in these statements.

Every physical flow is bounded by total positive nomination and hence
by `B=sum_v |b_v|`. On the expanded box of radius `B+1`, coordinate
gradients of the stated quadratic objective are bounded by
`|d_i|+(B+1)sum_j |Q_ij|`. The rational `L` therefore bounds the
gradient infinity norm. Integrating along the line segment between two
points in this convex expanded box proves
`|f(x)-f(y)|<=L||x-y||_1`. This bound permits arbitrary signs and
off-diagonal entries in the positive-semidefinite matrix.

An edgeless instance and zero nominations can be handled directly. A
tree also causes no difficulty: its circulation box has dimension zero
and its physical flow is rational and fixed by conservation.

## Rational inner intervals and freezing

The independently computed endpoint enclosures have polynomial bit size
at accuracy `eta=min(1,epsilon/(16mL))`. No comparison of an unbounded
sum of endpoint radicals is required. If `l^+<=u^-`, the retained
interval lies within the true one. Projecting any true feasible scalar
onto it moves that scalar by at most `eta`, since each displaced endpoint
is within its enclosure width of the true endpoint.

If `l^+>u^-`, then

```
u-l=(u-u^-)+(u^--l^+)+(l^+-l)<2eta.
```

Freezing the surrogate at `l^+` is safe, even if it lies outside the true
interval. Its distance from the true lower endpoint is at most `eta`.
The candidate's bound of `2eta` from every true point is conservative
and valid. A singleton irrational true interval is correctly treated
this way; the algorithm does not require a rational point inside it.

Disjoint cycle supports make each edge affected by at most one coordinate
change. Thus projection of a true feasible flow into the surrogate has
`l1` error at most `2m eta`. For any surrogate point, replace its frozen
coordinates by the true lower endpoints and keep every retained
coordinate unchanged. The result is a truly attainable flow by block
independence. The surrogate differs from it by at most `eta` on each
affected edge, and hence lies inside the expanded physical-flow box
of radius `B+1`.

These observations prove the one-sided optimum comparison
`min_surrogate f<=min_true f+2mL eta`. The surrogate need not be entirely
physically attainable before recovery; the proof only uses its explicit
proximity and the later exact recovery step.

## Convex optimization in unbounded cycle dimension

After freezing and deleting constant coordinates, affine rescaling maps
the rational box to a cube in its remaining dimension `k`. Its inner
Euclidean radius can be taken as one and its rational outer radius as
`k` for `k>=1`. A zero-dimensional box is evaluated separately.
Rational interval widths, including very small positive widths, have
polynomial bit length; this coordinate change preserves polynomial
encoding size.

The transformed objective is a rational convex quadratic. A rational
positive-semidefinite LDL decomposition can be computed in polynomial
bit time. Zero diagonal pivots are harmless: a zero diagonal in a
positive-semidefinite matrix has a zero row and column, so that direction
can be skipped. Positive pivots and their Schur complements give a sum
of squares of rational linear forms with nonnegative rational weights.
The affine part of the objective remains separate.

For each form `ell(y)`, an explicit rational bound on the cube is the
sum of absolute coefficients, with any affine offset included if used.
Replacing its scalar square outside `[-R,R]` by
`2R|t|-R^2` preserves convexity, matches value and derivative at the two
junctions, and gives a globally Lipschitz function agreeing with the
square throughout the required range. A zero form can be omitted.
The weighted sum and affine part are still globally convex and globally
Lipschitz. For example, a rational Euclidean Lipschitz upper bound is
the affine coefficient `l1` norm plus
`sum_j 2 gamma_j R_j ||ell_j||_1`.

Evaluation and subgradient queries are exact rational arithmetic on
polynomially many pieces. Their sizes are polynomial in the data and
query encodings. I checked
[Dadush's thesis, Theorem 2.5.9, printed page 48](https://homepages.cwi.nl/~dadush/papers/dadush-thesis.pdf)
directly. It supplies a rational feasible point and an additive objective
enclosure for a globally Lipschitz convex function over a centered body
with a weak-membership oracle. The thesis explicitly measures the
polynomial bound in input encoding lengths. The cube has a direct
membership oracle, and all required radii, Lipschitz bounds, and rational
value oracles are available here.

Thus the cited theorem gives the requested rational
`epsilon/2`-optimal surrogate point in polynomial input-and-accuracy-bit
time without fixing `k`. This use of a standard convex optimizer is
valid; it does not depend on a polynomial bound on the numerical size
of the objective coefficients.

## Exact rational resistance recovery

For a retained rational circulation, all its cycle-edge flows and signed
quadratic basis values are rational. Since it lies in the true interval,
`H_min(q)<=0<=H_max(q)`. Let `beta_min` and `beta_max` be the rational
endpoint profiles attaining these two values. If their values differ,
put

```
lambda=-H_min(q)/(H_max(q)-H_min(q)),
beta=(1-lambda)beta_min+lambda beta_max.
```

Then `0<=lambda<=1`, every edge resistance stays in its interval, and
linearity in resistance gives zero cycle pressure sum exactly. Thus
the desired rational flow is the actual physical cycle flow. A small
nonzero denominator in this formula creates no bit-complexity problem:
it is a rational number formed by polynomially many bounded-degree
rational operations, and inversion preserves polynomial encoding size.
If the two values agree, the bracketing inequalities force both to be
zero and either profile works.

For a frozen coordinate, use the stored rational endpoint scenario. Its
physical circulation is the exact algebraic lower endpoint, within
`eta` of the rational surrogate coordinate. Mixing the independently
recovered cycle profiles and arbitrary permitted bridge endpoints gives
a globally valid rational resistance scenario. This step uses continuous
resistance intervals; the interpolated values need not belong to a
finite resistance set.

No nonlocal compatibility condition is lost: conservation is built into
the cycle representation, and the independent cycle pressure equations
are precisely potential consistency. Physical uniqueness identifies the
state of the returned scenario with the recovered flows.

## Error budget and output arithmetic

Only frozen cycles move during recovery, so the additional `l1` flow
change is at most `m eta`, and objective increase at most `mL eta`.
The complete loss bound is therefore

```
2mL eta+epsilon/2+mL eta
<=3epsilon/16+epsilon/2
=11epsilon/16<epsilon.
```

The inequality remains true when the minimum defining `eta` selects
one, because that case implies `mL<=epsilon/16`. The returned physical
point and surrogate both lie in the expanded box used by the gradient
bound, validating every comparison.

Frozen cycles can have irrational physical flows despite rational
resistance scenarios. Separate quadratic root enclosures suffice for
approximate output values: approximate the flow coordinates rationally
and apply the same gradient bound before evaluating the quadratic.
Even when the objective couples different cycles, this uses ordinary
rational arithmetic and controlled approximation, not a common field
containing all independent roots. Exact added operating constraints are
correctly excluded because these perturbations need not preserve them.

I checked exact examples of a retained interval, singleton freezing,
the rational two-profile interpolation, and the numerical error-budget
fractions. All passed. These checks supplement the proof and do not
implement the full convex-optimization oracle. No substantive defect
remains in the stated additive rational-scenario theorem.
