# Independent review of the constrained filtered-grid theorem

Date: 2026-10-02. Scope: the completed mathematical text of
[tu-filtered-grid.md](../tu-filtered-grid.md), read together with the earlier
TU rounding lemma and box filtered-grid theorem. This review does not cover
an implementation of tree dynamic programming or a general certificate checker.

The integral-data theorems withstand the checks below. Two clarifications
were requested: a qualifying endpoint must be distinguished from the other
endpoint of a retained interval, and the rational-data extension must use
an enlarged rational-height bound for exact output. Neither changes the
integral-data result. The requested changes were sent to the author before
this record was written. Both corrected passages were then reread and
accepted; no unresolved mathematical finding remains from this review.

## Feasibility and filtering

Fixing the explicit integer labels is sufficient. The columns multiplying
those labels need not be TU: their integral values change only the integral
right side. For a cell of side `h=2^-j`, substitution gives the TU system
`At <= 2^j(b-Bz)-Ak`, with integral right side and unit bounds. Its vertices
are feasible zero-one corners. Taking a convex decomposition preserves the
continuous mean and gives summed coordinate variance at most `n_c h²/4`.
No independence of the rounded coordinates is needed.

The full-Hessian upper bound gives the stated expectation inequality even
when the objective is nonconvex. The segments used for Taylor's inequality
are in the original box, where the bound is assumed. Filtering keeps grid
aligned interval endpoints, so the same argument applies after every
restriction. This includes coordinates fixed to a current grid node.

For a given continuous interval, every rounding outcome has one of its two
endpoints in that coordinate. Therefore its least endpoint min-marginal is
at most the rounded expectation. Subtracting the global error proves the
conditional lower bound used by filtering. A fixed discrete label has the
same argument without changing that label. Simultaneous filtering is safe
because every optimizer survives each coordinate decision; taking interval
hulls weakens filtering but does not invalidate it.

The incumbent survives as well: its coordinates remain on finer dyadic
grids, and its min-marginals are at most its attained objective. Consequently
the current grid contains the old incumbent and updating it makes `U=v_j`.
The objective interval has width exactly `E_j` under this convention. No
growth assumption is used for any of these assertions. Initial infeasibility
is decidable by the first grid because every nonempty integral TU fiber has
a feasible integer corner.

A certificate must include the restriction history. Checking the final
restricted grid alone would not justify a bound on the original domain.
The proposed history is sufficient: points actually excluded at a stage
have objective strictly above that stage's incumbent, hence above the final
incumbent. The last bound applies to points that remain. TU and the curvature
certificate must also be checked; the note explicitly requires both.

## State counts and complexity

For each retained interval there is **at least one qualifying endpoint**
whose min-marginal has a feasible witness with objective at most `U+E_j`.
Growth puts that endpoint within `sqrt(n_c L/(4g)) h` of the optimizer.
The opposite endpoint can be another distance `h` away. This proves the
stated hull bound and the next-level count
`5+2 sqrt(n_c L/g)`. Discrete labels are always explicitly enumerated and
have at most `d` states. The global dimension factor remains, so this is an
XP guarantee in width, not the box theorem's FPT guarantee.

The initial grid enumerates every integer node between each pair of integral
bounds. Its cost is correctly recorded as pseudopolynomial in capacities.
It cannot be absorbed into polynomial bit complexity. The subsequent number
of levels depends logarithmically on `n_c L` and linearly on requested
accuracy bits. Rational arithmetic has polynomial bit length: nodes have
one shared dyadic denominator per level; factor outputs have the required
polynomial length; a message sums at most the input number of factors.
The assumption on exact factor evaluation is necessary for the general
objective statement.

Two-pass min-sum dynamic programming can compute every min-marginal within
the stated table bound. Summing incoming messages and excluding the recipient
avoids a product in the number of children. Infeasible local assignments
must be represented with flags or infeasible counts so exclusion never
subtracts infinities. This review checks the algorithmic argument, not code
implementing that bookkeeping.

## Exact quadratic output

The constrained KKT height argument is valid for the integral model. Fix an
optimal integer assignment and choose an optimal point whose minimal face
has least dimension among optimal points. At its relative interior, the
quadratic is stationary on the face tangent space and its Hessian is positive
semidefinite there. A nonzero tangent null direction would keep the exact
quadratic constant until reaching a smaller face, contradicting that choice.
Thus the tangent restriction is positive definite. Independent active TU
rows and coordinate bounds have entries in `{0,±1}`. Their KKT saddle matrix
is nonsingular, has dimension at most `2n_c`, and has entries bounded by
`2C`. Its integral right side may be large, but that affects numerators,
not the determinant denominator bound. Cramer's rule gives the claimed
common denominator bound `R`; the value denominator is at most `D R²`.

For a unique optimizer, filtering preserves the denominator-bounded point.
Growth shrinks each continuous hull and eventually leaves only its integer
labels. Rational reconstruction in these hulls and in the objective interval
therefore has an existing unique candidate. Exact feasibility and objective
checks certify acceptance without a growth estimate. The number of levels
is `poly(I)+O(log kappa)` as claimed.

The qualitative growth claim for unique QP optima also holds. If the growth
ratio tended to zero, compactness and uniqueness would force the points
toward the optimizer, so their finite integer labels would eventually agree.
Normalize continuous displacements and take a limiting unit direction in
the closed polyhedral tangent cone. First-order optimality makes the linear
term nonnegative. Dividing the quadratic expansion by squared displacement
shows that the limit has zero linear term and nonpositive quadratic term.
Second-order optimality on its feasible short ray makes that quadratic term
nonnegative, hence zero. The entire short ray has the same quadratic value,
contradicting uniqueness. This proves existence of growth, not good numerical
conditioning.

## Corrections incorporated after review

1. The original sentence beginning “For a retained endpoint or discrete
   label” overstates what the retention rule proves. For `F(x)=x²` on
   `[0,1]`, `L=2`, and the initial grid, `E=1/4` and `U=0` retain the
   interval `[0,1]`, although its endpoint `1` has min-marginal `1>U+E`.
   Say “For an endpoint satisfying `M_i(t)-E_j<=U`, or a retained discrete
   label” instead. The subsequent proof already includes the extra interval
   length and needs no numerical change.

2. The section on rational data must not reuse the integral-data height
   bounds unchanged. The equality `x=1/17` with objective `x²` has
   `n_c=C=D=1`, hence the displayed integral-data formula gives `R=16`,
   while the optimizer has denominator 17 and its value denominator 289
   exceeds `V=256`. If `D_0` clears all rational right sides, continuous
   bounds, and integer-column data after preprocessing, the unchanged TU
   KKT matrix has right-side denominators dividing `D_0`. Coordinate height
   `R'=D_0 R` and value height `V'=D(R')²` suffice. Alternatively, explicitly
   restrict the rational-data paragraph to certified approximation. The
   dyadically refined mesh must start at `1/D_0`, as already stated.

## Targeted finite checks

An independent exact-rational enumerator was run with:

```sh
python research-20261002-decomposition/constraints/reviews/check_review_examples.py > research-20261002-decomposition/constraints/reviews/check_review_examples-results.json
```

The [script](check_review_examples.py) and [results](check_review_examples-results.json)
cover eight levels of `x+y=2z`, `0<=x,y<=2`, `z in {0,1}`, with unique
non-grid optimizer `(2/3,4/3,1)`. The continuous matrix is TU while the full
matrix including the integer column is not. All objective brackets,
optimizer and incumbent retention checks, and next-level state bounds
passed. There were 212 checks of conditional bounds at rational feasible
sample points. Separate exact examples check the necessity of full curvature,
the nonqualifying retained endpoint, and the rational-right-side height issue.

These finite checks do not prove the theorems, test tree DP, implement
rational reconstruction, or establish competitive solver performance.
The mathematical arguments above carry the general claims. No project-wide
verification, CI status inspection, or CI log inspection was performed.

A subsequent limited reading of the author's two-bag prototype found that
its `row_cost` loops over neighbors for each outgoing message. This suffices
for its diagnostic fixtures, but would introduce an extra degree factor on
general branching trees. The theorem's sum/exclusion implementation is not
the code path used by that prototype. This distinction was sent to the author;
it does not affect the theorem or the reported two-bag finite checks.

## Follow-up review: equality-tangent curvature

The subsequently added equality-tangent alternative is sound. For an
original equality `Cx+Ez=a`, every feasible rounding displacement at fixed
`z` satisfies `C(Y-x)=0`. Its entire Taylor segment has that same displacement
direction. Thus the proof needs a Hessian upper bound only on `ker C`, and
the Euclidean variance estimate and all later bounds remain unchanged.
The equality must be imposed throughout the original feasible set; a merely
active inequality at an unknown optimizer does not supply this argument.

For a rational kernel basis `Z`, the correct check is positive
semidefiniteness of `Z^T(LI-Hess_xx F)Z`, as written. An arbitrary kernel
basis need not be orthonormal, so a bound on `Z^T Hess_xx F Z` without its
Gram matrix would not suffice. The note avoids that error. For a constant
quadratic Hessian, the rational orthogonal projector
`P=I-C^T(CC^T)^(-1)C`, after removing dependent rows, gives a symmetric matrix
`P Hess_xx F P`. Its maximum absolute row sum bounds its spectral radius
and hence supplies a valid tangent upper bound. Rational elimination and
matrix arithmetic have polynomial bit cost. Neither operation substitutes
variables into objective factors, so it does not change the decomposition.

Adding `rho ||Cx+Ez-a||²` changes no feasible objective value. Its continuous
Hessian is `2rho C^T C`, which projects to zero. With the same tangent bound,
rounding allowances and all decisions at a given filtering level therefore
remain unchanged. This does not make the stated exact solver's stopping
level invariant: its coefficient-based denominator bounds can grow with
`rho`. That limitation and the corrected introductory description were
requested, incorporated, and reread. The addition is accepted with no
unresolved mathematical finding.

The reviewer script was rerun after adding exact projector checks for
`C=(1,1)` and four penalty coefficients, including a large integer and a
nonintegral rational. All four projected Hessians equal the same matrix;
eight feasible-point penalty checks also passed. These are finite
diagnostics of the algebra, separate from the proof above. The command
remains the one recorded in the preceding verification section.

## Follow-up review: supplied common-unit mesh

The positive rational initial mesh extension is also accepted. Its alignment
test is sufficient for every independent label choice because

```text
(b-Bz)/delta = (b-Bz0)/delta - sum_i B_i(z_i-z0_i)/delta.
```

The reference vector and each listed individual increment are integral by
the test; no Cartesian enumeration is needed. Bound alignment puts every
initial interval endpoint on the mesh. At level `j`, multiplying these
integer quantities by `2^j` supplies the same integral right side required
by the TU cell argument. Retained endpoints remain aligned at the next
level. The rounding error is `n_c L delta² 4^-j/8`, while the ratio of a
filtered hull width to the next mesh is unchanged, proving the same later
state count. The initial count is correctly `W/delta+1`.

The supplied rational mesh contributes its encoding length to the input;
it adds `O(log_+ delta)` to the accuracy-level bound and a common rational
denominator to grid nodes. Both fit the stated polynomial bit overhead.
Original constraints and coordinates are unchanged, so the existing KKT
height bound does not acquire a scaling factor just from choosing this
mesh. Large unaligned capacities still have the stated limitation. This
acceptance is an analytic check of the extension; the author's separate
large-capacity diagnostic was not rerun by this reviewer.
