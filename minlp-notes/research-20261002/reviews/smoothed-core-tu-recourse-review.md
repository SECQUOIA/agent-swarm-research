# Independent review: core-only smoothing over TU equalities

Date: 2026-10-02. Verdict: **passed** for the actual
[TU extension](../new-direction/smoothed-core-tu-recourse.md).
This review validates its new interfaces rather than inferring them from
the network theorem. No substantive correction was requested. The scope
is bounded native integer variables, fixed TU equalities or the explicitly
bounded inequality reduction reviewed below, separable convex costs, and
core dependence only in costs.

## 1. Interpolation gives the compact adjacent-slope dual

On a native integer grid cell, the piecewise-linear interpolation of the
separable costs is affine. Its feasible intersection with `Az=b` and
the cell bounds is a bounded integral polytope: appending signed unit
rows preserves TU, and every right-hand side is integral. This remains
true for lower-dimensional or degenerate cells. Every nonempty cell's
affine minimum is attained at an integer vertex. Since finitely many
cells cover the original box, the interpolant's real optimum equals the
integer optimum. Thus the particular returned integer optimum is also
a real interpolant optimum.

The interpolant has a finite LP epigraph description, even though that
description may be too large to build. LP duality supplies equality
multipliers and the usual subgradient/bound conditions at the optimum.
For an interior integer coordinate these conditions put `(A'lambda)_i`
between its two adjacent slopes. At a lower endpoint only the upper
slope inequality is required; at an upper endpoint only the lower one
is required. These are exactly the displayed inequalities (4). There is
no unjustified differentiability or relative-interior assumption.

Conversely, the inequalities make the selected native value minimize
each scalar adjusted cost `f_i-(A'lambda)_i t` over its integer interval.
The multiplier sum is constant on `Az=b`, so they certify the original
integer optimum directly. The algorithm solves this compact system of
at most `2r` inequalities; it need not construct the interpolation or
enumerate its cells.

TU is doing real work here. For example, with the non-TU equality
`z_1+2z_2=1`, bounds `[0,1]^2`, and objective `z_1`, the unique integer
optimum is `(1,0)`, but its proposed slope dual would require both
`lambda>=1` and `2lambda<=0`. The real interpolation optimum is cheaper.
The draft correctly does not claim the dual interface for general
integer matrices.

## 2. Preprocessing, pointedness, and a base-only multiplier box

Substituting fixed native coordinates preserves integral right-hand
sides and polynomial encoding length. Retaining an independent subset
of original equality rows preserves TU; checking right-hand-side
consistency before dropping rows is necessary and is included. The
remaining `A` has full row rank and each remaining native interval has
positive length.

Every column then contributes at least one signed-column inequality to
the dual. A line direction in its feasible polyhedron must be orthogonal
to all these columns, hence satisfy `A'h=0`; full row rank gives `h=0`.
The dual is nonempty and pointed, so it has a vertex, even if it is
lower-dimensional. At a vertex, `m` independent active normals are
signed columns of `A`. Their square matrix is a signed transpose minor,
with determinant `+-1` and inverse entries in `{0,+-1}`. The marginal
bound `V` therefore gives the coordinate bound `mV` by direct matrix
multiplication. Choosing `R=mV+1` supplies a nonempty bounded dual slice
with polynomial base encoding.

Lexicographic optimization over this bounded slice produces a vertex
of the original slice: any convex decomposition would preserve the
successive optimum coordinate values and hence every coordinate. An
independent active-row basis must be extracted from the original dual
and box constraints, as the draft specifies, rather than from the
temporary lexicographic equalities.

Adding signed unit rows to `A'` preserves TU. Thus every extracted
nonsingular basis still has inverse entries `0,+-1`. This covers bases
that use artificial multiplier-box rows, which can occur when a lexicographic
optimum lies at the end of an originally unbounded direction.

## 3. Symbolic charts and their genuine certification obligations

After fixing a native label and an active basis, its right-hand side
consists of native adjacent differences and base constants `+-R`.
The symbolic multiplier `C^{-1}h(v)` agrees with the computed dual at
the query. Its coefficient height is bounded using the base input,
the bounded native labels, and sums of at most `m` coefficients. The
queried core coordinates do not appear in those symbolic coefficients.
The query only selects one member of the finite family.

A unit difference in the native coordinate removes terms independent
of that coordinate. For a total-degree-`d` input polynomial, the remaining
core degree is at most `d-1`. The stated degree and height bounds for
the multipliers and adjusted marginal charts therefore hold. In the
bilinear model the charts are affine, including those involving box
rows. The ordered-basis count `(2r+2m)^m` is a safe overcount; after
including native labels and adjacent positions its logarithm remains
polynomial in the base input.

The artificial box serves only to select a bounded multiplier at the
query. Its inequalities need not remain valid elsewhere in the core.
An arbitrary real multiplier certifies scalar optimality when all the
original adjusted marginals have the required signs. Consequently only
those marginals belong in the uniform certificate; the draft correctly
does not impose unnecessary uniform box inequalities. Nor does it claim
that a chart is a feasible dual at every core point merely because it
is feasible at its query.

## 4. All optimal points and conformal TU proximity

Each adjusted scalar cost is convex, so its native minimizers form an
integer interval containing the returned coordinate. Over a feasible
point, subtracting `lambda'Az=lambda'b` changes the objective by a
constant. The gap is a sum of nonnegative scalar gaps. Equality holds
exactly when every coordinate is in its minimizing interval. Thus the
tightened TU system represents **all** optimal native points, not only
a subset or a selected label. Its interval endpoints can be found by
monotone adjacent-slope binary searches in the native bit length.

The circuit argument is also valid independently of graph topology.
Within the orthant of a nonzero kernel vector, choose a nonzero kernel
vector of smallest support. If the kernel restricted to its support
had dimension greater than one, a nonparallel kernel perturbation could
be followed to the orthant boundary while keeping a nonzero vector,
contradicting minimal support. It is therefore a circuit. Signed maximal
minors of its rank-deficient TU restriction give a primitive circuit
with unit nonzero entries. A zero column is covered by a one-coordinate
circuit. Repeatedly subtracting the largest conformal integer multiple
gives an integer decomposition and removes at least one nonzero
coordinate at each step.

For a nearest tightened point `bar z`, each circuit must have a coordinate
whose directed unit step exits its tightened interval; otherwise that
step preserves `Az=b`, remains in the tightened box, and decreases the
distance to `z`. Unit entries are essential. A blocking coordinate is
at an interval endpoint and the full difference toward `z` equals its
interval violation. Charging each circuit multiplicity to one blocker
is bounded by that violation, by conformality. Each circuit has at
most `r` nonzero entries. This proves the same `r`-proximity bound used
by the face certificate, without assuming incidence-matrix structure.

The inward-derivative argument survives unchanged for the precise reason
given in the draft: three tied consecutive integer values force affinity
of the convex adjusted scalar cost, so the original cost has zero second
derivative on the interval at the face point. One-sided inward differentiation
of the family of convex costs then gives a convex derivative cost.
Two-point intervals require interpolation, and singleton intervals are
substituted. These replacements agree on every feasible native label
and remain polynomial-time convex evaluation oracles. Their minimization
over the tightened TU equality system uses the established exact oracle.

## 5. Probability, arithmetic, and output transfer

The boundary-flow proof depends on topology only through the compact
dual charts, exact tightened-set recourse, and proximity estimate. The
preceding checks supply each replacement with the same type of degree,
height, query-length, and cost bounds. Symbolic multiplier terms cancel
on every feasible label because the right-hand side is fixed. The
uniform cost-gap and Taylor face-fixing inequalities therefore remain
valid, with no extra numerical factor beyond the same `r`.

Replacing the tree count by the basis count preserves polynomial
logarithmic chart size. The cross-label gradient-image argument,
normal-noise interval estimate, fixed-dimensional chart-value margin,
and projected-growth tail then choose the same form of base-only
finite law. The sampling height has no query-dependent feedback.
For general fixed-degree costs, its parameter-dependent precision is
charged to every exact LP, TU oracle, polynomial test, and fallback.
For bilinear coupling the affine-chart margin restores the sharper
polynomial sampling length and work expression.

All online new operations have fixed polynomial bit exponents:
compact rational LP solving, active-basis extraction, interval searches,
and the established separable-convex TU oracle. Circuits, interpolation
cells, labels, and bases are not enumerated in ordinary work. Label
enumeration remains confined to the rare same-draw fallback. Its output
keeps one winning label and the corresponding small-core representation,
so the inherited all-draw output and refinement bounds still apply.

The degenerate cases are accounted for: zero residual dimension gives
the small-core problem, rank zero gives independent scalar dual conditions,
and zero core dimension invokes the exact TU oracle. No arbitrary-matrix,
core-dependent feasibility, or unbounded-slack extension is inferred here.

## 6. Fresh review of the bounded-inequality addition

The subsequently added section 6 also **passes**. The displayed signed
endpoint sum is exactly the minimum of each row over the native box.
Consequently a negative `U_i=b_i-m_i` proves infeasibility, while every
feasible original point has its unique integral slack in `[0,U_i]`.
Conversely the equality with a nonnegative slack implies the original
inequality. This is a bijection, including zero-width slack intervals.

Appending identity columns preserves TU. The row sums and finite slack
bounds have polynomial encoding length in the original input even when
their numerical values are large. Existing fixed-coordinate preprocessing
therefore applies without changing the argument. Zero slack costs preserve
convexity, polynomial degree, all core derivatives, and the supplied `L`;
bilinear slack columns are zero. The added coordinates increase only the
polynomial input factor and the polynomial logarithm of the label count.
They introduce no new parameter or unbounded domain. Dropping them from
the exact output preserves the original optimizer and objective value.

Rounding a rational right-hand side down is valid because every row value
is integral. This audit does not extend to nonintegral variables or a
non-TU matrix. No additional numerical test was needed for this exact
reduction; I reread the actual saved addition and checked each implication.

## Verification record

This was an actual-file mathematical audit. I also inspected the complete
[author-side diagnostic](../new-direction/check_core_tu_recourse.py)
without rerunning it. Its separate run reports six cost systems and
24 rational queries; 495 exact TU-minor checks; preprocessing and an
inconsistent-row guard; 166 optimum-interval equalities; 1,188 proximity
checks with 1,158 conformal circuit steps; and 7,840 symbolic marginal
evaluations. It includes rank-zero and signed systems, endpoint-only
slope conditions, persistent ties, four selected box-active bases, and
charts deliberately infeasible away from their query. These are the
author's diagnostic results, not executions by this reviewer.

The checker enumerates small labels, bases, and circuits only as diagnostic
oracles. It is not a production implementation or a large-capacity
complexity experiment. No external search, index edit, project-wide
verification, or CI inspection was performed for this review.
