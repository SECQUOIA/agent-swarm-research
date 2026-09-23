# Independent second audit: degree-two bypass feasibility

Date: 2026-09-05. Reviewer: `pooling_all_two_review`.

Reviewed [the candidate proof](pooling-degree-two-boundary-projection.md).
The mathematical argument passes this audit. This is a feasibility result;
the proof does not optimize a dense cost over eliminated path interiors.
Priority of the polygon-composition lemma and pooling corollary remains a
separate literature question.

## Polygon composition

For compact planar convex relations `P(x,y)` and `Q(y,z)`, first restrict
the `y` range of `P` to the interval projection of `Q`. At every remaining
`x`, the feasible `y` values form the interval `[l(x),u(x)]`. Its minimum
achievable `z` is the minimum of the convex lower envelope `q` of `Q`
on this interval. If `[a,b]` minimizes `q`, this minimum equals
`max{L(l(x)),D(u(x))}`, with the monotone truncated branches defined in
the draft. The three cases (interval below, intersecting, or above
`[a,b]`) verify the identity directly.

The composition functions are convex: `L` is convex nondecreasing and
`l` convex; `D` is convex nonincreasing and `u` concave. On a univariate
convex or concave graph each level has at most two boundary crossings,
with a flat level interval counted by its two endpoints. Subdivision
at inner knots and preimages of outer knots therefore uses only a
constant times the sum of the input piece counts. A convex piecewise
affine function is the maximum of its affine segment extensions, so
taking the maximum of the two compositions creates no more pieces
than the total number of their affine pieces. Reflecting `z` gives the
upper boundary. The stated factor 16 is conservative and adequate.

Clipping adds only two inequalities. Point domains, vertical intervals,
horizontal segments, and singleton shared-coordinate domains admit the
separate interval operations stated in the draft. No argument requires
strict positivity of slice lengths or full dimensionality.

## Size, bit complexity, and reconstruction

At a balanced composition node, every candidate line coefficient is
obtained using a constant number of rational operations on its two
children's line coefficients. Boundary intersections and preimages have
the same property. Sorting and envelope construction select among these
candidate lines. Thus both the row-count recurrence and coefficient
bit-length recurrence have a constant multiplication factor per level.
The depth is logarithmic, so both are polynomial in the initial input
size. The same applies to all intermediate nodes together.

For reconstruction, the two child slices give intersecting intervals
for their shared coordinate. Their endpoints are rational affine
functions of the prescribed outer coordinates. A midpoint of the
intersection belongs to both children. Recursing lifts a feasible
endpoint pair to all original coordinates.

This last observation also settles algebraic encoding. Every recovered
coordinate is a rational affine combination of the fixed-dimensional
core sample. Divisions are by rational row coefficients; the procedure
does not repeatedly invert arbitrary algebraic elements or adjoin roots.
The common field degree stays polynomial, and balanced recursion keeps
the rational affine coefficients polynomially encoded. Order tests use
ordinary exact real-algebraic sign determination.

## Pooling mapping

The two feeding inputs and two receiving outputs have at most eight
incident bypass arcs when bypass degree is at most two. Retaining these
arcs, the four pool arcs, and one intake fraction gives at most thirteen
real variables. Feed-fraction consistency and output-quality constraints
have degree at most two. The quality dimension can grow because it
increases only the number of rows.

After deleting the four attachment nodes, all boundary-connected bypass
components are paths with at most two retained boundary flows. Each
internal capacity or quality row involves at most the two adjacent arc
flows. Exact endpoint projection therefore applies. One-boundary paths
reduce to interval projections; components with no boundary are rational
LP feasibility problems. An attachment-to-attachment bypass stays in
the core. A former cycle cut at an attachment becomes an ordinary path
whose two boundary flows may belong to the same attachment.

At zero pool throughput, nonnegative feed flows vanish, and any intake
fraction gives the same zero quality mass. Inconsistent positive lower
contracts are still detected by the retained linear rows. No composition
can hide such a contradiction.

Fixed-dimensional semialgebraic decision and sampling now applies to a
polynomial-size degree-two core system. The core and path lifts recover
an original feasible solution. This argument covers lower/upper flow
and quality bounds, finite rational arc bounds, and arbitrary many known
input qualities. It assumes the standard three-layer model and no dense
additional aggregate such as a profit threshold.

## Scope check against the fixed-alphabet obstruction

The independently checked quality-reset path has an exponential
one-price support curve even with input qualities `{0,1}` and no lower
flow bounds. This is compatible with polynomial endpoint feasibility:
the support curve retains the sum of costs throughout the path, which
is an additional dense coordinate. Neither result establishes the
complexity of one-pool profit maximization with degree-two bypasses.

## Immediate bounded-support optimization corollary

The same algorithm optimizes an objective supported on a fixed number
of designated actual arc flows. Retain these coordinates in the core and
split any affected bypass path at them. If a designated arc lies in a
detached cycle, cutting the cycle there leaves a path relation whose two
endpoint coordinates are constrained to equal that retained flow. The
core dimension stays fixed, and semialgebraic optimization replaces pure
feasibility. Exact algebraic attainment follows from finite bounds and
closed constraints.

The conclusion also allows a fixed-degree polynomial objective and
polynomially many fixed-degree constraints on that fixed set of retained
coordinates. A dense written objective is covered if an explicitly
available linear combination of the model's exact conservation or
contract equations reduces it to bounded support plus a constant. This
is a direct consequence of the proof, not an algorithm for unrestricted
dense bypass costs.

The final Section 5 wording in the promoted result was checked on
2026-09-05 and passes, including repeated endpoint coordinates for a cut
cycle, compactness, exact algebraic optimization, and checking a supplied
polynomial-bit equality reduction. The example based on a fixed number
of output-price changes correctly counts changes along the path, rather
than merely the number of distinct price values.
