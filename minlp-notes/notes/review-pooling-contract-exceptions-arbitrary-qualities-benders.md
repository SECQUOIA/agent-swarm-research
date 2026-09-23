# Independent audit: removing the quality-rank restriction

Date: 2026-09-05. Reviewer: `benders_review`.

**Verdict: PASS after the recorded clarifications.** I independently
checked the full theorem in
[the arbitrary-quality draft](pooling-contract-exceptions-arbitrary-qualities.md).
The fixed quality-rank assumption can be removed for the stated
bounded-exception, degree-two-bypass model. The proof uses two sound
branches with different fixed-dimensional representations. It retains
exact ordinary contracts, standard node economics, finite individual
arc bounds, and redundant common pool bounds.

During review the author explicitly added: initial unusable-pool
preprocessing; membership tests for singular source qualities in a
restricted affine-space branch; and retention of exceptional-input
supply bounds and all retained arc bounds in the exceptional-only
branch. I checked these additions in the final draft.

## Restricted quality spaces with arbitrary ambient dimension

Let `q=q_0+D eta`, where `D` has a fixed number of independent columns.
The source vectors need not lie in this affine space. The full vector
quality equations and their scalar projections remain valid algebraic
identities for arbitrary source and product vectors. The previous
fixed-rank cut proof therefore applies once its chart coverage and
encoding bounds are checked in the ambient dimension.

For each fixed `q` unequal to every source vector, the polynomial
`sum_h k^(h-1)(C_ih-q_h)` is nonzero and has degree at most `K-1`.
At most `|I|(K-1)` integers are forbidden across all sources. The
listed family contains one more integer, so some direction makes every
scaling factor nonzero. Its number of directions is polynomial even
when `K` grows. Every entry `k^(h-1)` has polynomial bit length, bounded
by `O(K log(|I|K+1))`. Storing and using all directions therefore still
costs polynomial space and bit operations. For `K=1` the same argument
gives a single direction; with no quality coordinates the model is an
LP.

The singular full source vectors are rational. In the restricted-class
lemma their LPs must be included only if the source vector belongs to
the chosen affine space and quality box. The added membership tests
make that lemma exact. Every nonsource vector belongs to at least one
valid chart, so no additional singular set is omitted.

After substituting the affine parametrization, scaling factors and the
coefficients `a_h` remain affine in fixed-dimensional `eta`. Direct
expansion shows that the bracket multiplied by `gamma_1` in `f_h` is
affine, hence `f_h` is quadratic. Neither cancellation uses source
membership in the selected space. All ambient quality coordinates
remain as constraints; they add polynomially many rows and candidates,
not parameter variables.

The sign arrangement has polynomial size for fixed parameter dimension,
including lower-dimensional cells. Zero `a_h` requires `f_h=0`; nonzero
`a_h` yields an exact rational arc equality. Connected residual cuts
cross at most two internal edges, so even polynomial-size candidate
lists give polynomially many combinations. Clearing only the selected
one or two affine denominators retains fixed degree and polynomial
coefficient length. Full exceptional constraints and all global quality
equations are still quadratic in at most `d+5s` core coordinates.

The checked fixed-rank algorithm's open-cell attained-value procedure
and common-field reconstruction therefore apply to this restricted
space without any bound on ambient quality rank.

## An active ordinary product supplies a suitable space

At an ordinary product receiving positive pool flow, dividing its exact
mass and vector-quality equations by that positive outlet flow gives
an affine combination of its product vector and its bypass source
vectors. The coefficients sum to one, although some are negative;
an affine span, rather than a convex hull, is the correct conclusion.
Bypass degree at most two bounds the span dimension by two. Positive
pool inflow also implies positive exact demand, so the enumerated
positive-demand products contain every possible witness to this case.

There are polynomially many candidate spaces. Their rational bases
have polynomial encoding length. To bound the parameter coordinates,
choose independent rows of `D` and solve for `eta` from those coordinates
of `q`. The fixed-dimensional inverse is rational of polynomial bit
length. The feed-coordinate quality box therefore yields finite
polynomial-bit bounds for `eta`; retaining all other quality-box rows
gives the exact intersection. Empty and zero-dimensional intersections
are correctly handled.

It is sound to omit the positive-outlet inequality from each resulting
branch. Every branch still enforces the complete physical constraints,
so inactive points it additionally finds are feasible original flows.
Conversely every original flow with an active ordinary outlet belongs
to at least one candidate space. No positivity division is used when
recovering a solution from such a branch.

## The exceptional-only branch

Force ordinary pool outlets to zero and reject incompatible individual
lower bounds. If no exceptional outlet is allowed, mass conservation
forces all pool arcs to zero and the remaining model is a rational LP.
Initial no-feed/no-outlet preprocessing also avoids an undefined feed
quality box.

Otherwise, the retained variables are exceptional input feeds, bypass
arcs incident to exceptional nodes, exceptional outlet flows, and
their output fractions. The count is at most
`3|E_I|+4|E_J|`. Exceptional supply bounds and retained arc bounds are
explicitly preserved. Ordinary intakes are eliminated by fixed input
contracts, including zero for an absent inlet. Ordinary products now
have bypass-only exact mass and all exact quality rows, involving at
most two bypass variables each. These rows have fixed rational
coefficients and no hidden quality parameter.

Removing exceptional nodes gives the previously reviewed static
compact two-variable path projection problem. All boundary flows are
retained; detached cycles and paths are independently checked for
feasibility, and isolated-node relations are retained. Polynomial
endpoint descriptions and rational affine lifting apply to the full
collection of mass, quality, and arc-bound rows. The number of quality
rows may grow without increasing the local variable count.

I independently checked the two aggregate identities. Total bypass
mass is the sum of fixed ordinary demands plus the retained bypass
flows into exceptional outputs. Total bypass quality mass is the sum
of fixed ordinary delivered masses plus the retained bypass quality
masses into exceptional outputs. Subtracting these quantities from
total actual input throughput and quality mass gives exactly summed
pool intakes and their quality mass. Thus the stated `T,Q` are affine
core expressions for every valid local reconstruction. They are not
additional dense aggregate constraints on forgotten path variables.

Imposing nonnegative fractions summing to one and `v_j=theta_j*T`
gives actual pool mass conservation. If `T>0`, the recovered quality
is `Q/T` and each outlet receives quality mass `theta_j*Q`, as used
in all exceptional product bounds. If `T=0`, nonnegative reconstructed
intakes imply every intake is zero, hence `Q=0` in every coordinate.
Fractions can then be any simplex point and do not impose a spurious
quality requirement. Positive individual outlet lower bounds are still
checked. Conversely every original flow supplies these coordinates,
with its actual output fractions when active.

The resulting core is closed and bounded: original retained arc bounds
are finite, and the fractions lie in a simplex. All remaining rows
are quadratic regardless of ambient quality count. Standard economics
is constant on ordinary throughputs and affine on exceptional core
throughputs. Fixed-dimensional exact optimization and static path
lifting consequently apply.

## Union, recovery, and scope

The two cases cover every feasible physical flow. Each branch is
sound, and their number is polynomial. Quality-chart branches retain
strict chart conditions and use their attained-value sets; the
exceptional-only branch is compact directly. The complete original
model with a closed bounded quality box is compact, so the union has
an attained optimal value. There is no optimization of an invalid
closure at a vanishing denominator.

An optimal core and value admit a common polynomial-degree algebraic
representation. Incidence recovery or static affine endpoint lifting
stays in that field. All divisions used in active chart recovery are
by nonzero scalings. In the exceptional-only branch, reporting active
quality uses `Q/T`; for an inactive pool a rational feed-quality vector
can be used. All original flows have polynomial common-field encoding.
No degree-two witness bound follows from the fixed-dimensional method.

The result does not cover restrictive common pool bounds or arbitrary
dense arc costs. Redundancy can be certified by the minimum of the
three separately valid total-input, total-feed-capacity, and total-
outlet-capacity bounds. The key retained restriction is the fixed
number of exceptions to exact external contracts, not the number of
quality coordinates. This is a fresh mathematical audit of the new
geometry and conservation arguments; existing dependency tests were
not repeated. Publication priority requires the separate source audit.

The audited proof is now promoted as
[pooling with bounded contract exceptions](../results/pooling-contract-exceptions-algorithm.md),
with its independent review links and source qualifications retained.
