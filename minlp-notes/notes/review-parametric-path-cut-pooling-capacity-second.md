# Second review: common pool-capacity interval via path cuts

Date: 2026-09-05. Reviewer: `two_quality_sources`, independently of the
completion's author. **Verdict: PASS** for Sections 3–4 of
[the completed path-cut investigation](parametric-path-cut-clamp-investigation.md).
The reviewer previously supplied a source and direct proof for the
classical box-truncation identity; the physical application and its
complexity argument were reviewed separately here. This is not an
independent discovery of that identity.

The reviewed result is exact feasibility for one pool, scalar qualities,
exact individual source supplies and product demand/quality contracts,
bypass degree at most two, arbitrary individual arc intervals, and an
arbitrary common pool-throughput interval. The witness may have
polynomial algebraic degree. The earlier quadratic-degree guarantee does
not persist in the proof.

## Divergence polyhedron and physical objective

I checked the original transformation in
[the quality-scaled flow result](../results/pooling-quality-scaled-path-flow.md),
not merely its summary. With arcs oriented from input to output,
`div(w)_i=sum_j w_ij` at an input, including negative transformed
flows. Hence

```
sum_ij z_ij = sum_i div(w)_i/(C_i-q).
```

The exact total input supply `A` therefore makes pool throughput
`A-c(q).div(w)`. Both common lower and upper bounds translate with the
directions stated in equation (7). Positive individual feed and outlet
lower bounds are retained in the original node and arc intervals;
there is no use of the different two-source-value convex-QP argument.

The base-polyhedron proof is correct for finite signed arc bounds.
Writing the cut as a nonnegative directed cut with capacities `u-ell`
plus the modular divergence of `ell` proves submodularity. The usual
prescribed-divergence circulation criterion gives equality with `B(f)`.
After imposing node bounds, the proof of `D=B(g)` checks both singleton
upper bounds and complementary singleton lower bounds. Its normalization
uses the explicitly required nonempty `D`. No monotonicity or
nonnegativity of `f` or `g` is assumed.

The greedy formula applies to signed costs. Telescoping removes the
last cost term because every feasible divergence has total zero. Each
greedy prefix difference gives a feasible divergence vector, including
tied cost coordinates and disconnected components.

## Symbolic representation and common refinement

On each nonsingular quality interval, each effective arc bound is chosen
from constantly many quadratic candidates. Partitioning at their pairwise
comparison roots has polynomial size. Pure parameter restrictions and
connected-cut feasibility conditions remain in the model.

The order of input costs is fixed there: their differences have constant
numerators and products of nonzero affine denominators. Output costs
are zero. Thus the number of prefix sets requiring `g(S)` is linear
for each of the two objective orders.

For a fixed prefix, the formula for `g(S)` is a binary submodular cut
energy on the same path/cycle components. Its pairwise coefficients
are the nonnegative widths `u-ell`; its remaining terms are quadratic
unary costs. The separately audited clamp lemma therefore applies.
For cycles, conditioning on one label leaves a path with modified
endpoint unaries. Comparing the two branch values adds only roots of
quadratic polynomials within their current cells.

There is no multiplicative explosion in this application. The parameter
is one-dimensional, so a common refinement over all prefixes, branches,
and components is obtained by sorting the union of their polynomially
many breakpoints. Zero-dimensional cells are retained. On a final cell,
each rank value is one quadratic polynomial with polynomial coefficient
length. Adding component minima does not increase its degree.

The support expression introduces only the affine denominators
`C_i-q`. Their product has polynomial degree and coefficient length.
Clearing its known sign in the common-capacity inequalities is valid;
there are no vanished factors on these cells. Consequently all new
decision polynomials have polynomial degree and bit length. Standard
univariate root isolation and sign evaluation suffice, including an
isolated feasible root. The original rational fixed-quality LPs cover
all singular values and outer search endpoints.

## Interval overlap and exact witness recovery

At a retained quality, the transformed flow polytope is nonempty and
compact. Its scalar bypass-flow image is the full closed interval
between the support extrema. The two inequalities in equation (7) are
exactly the condition that it intersect `[A-U_P,A-L_P]`.

A selected feasible root has polynomial degree and isolating-data
length. Each greedy divergence coordinate is a difference of quadratic
rank values at that root. To realize it, subtract lower arc bounds;
the residual capacities are nonnegative and the prescribed residual
divergence sums to zero. The ordinary source/sink max-flow reduction
applies. Edmonds–Karp needs polynomially many augmentations regardless
of the numerical capacities, so it is suitable over the represented
ordered field.

The bit-length assertion can be seen directly: initial capacities and
imbalances are polynomial-size polynomial values at the common root.
Augmentations use comparisons, sums, and differences. Their coefficient
bit lengths grow at most linearly in the number of arithmetic operations
after common rational denominators are fixed. Root sign tests remain
polynomial. The final interpolation uses one nonzero field quotient,
followed by division by nonzero `C_i-q`; standard algebraic arithmetic
preserves polynomial representation length. If both support extrema
coincide, interpolation is correctly omitted.

Interpolating two realizing signed flows preserves every local bound and
node condition and gives a desired common-capacity value. Original flow
recovery then uses the already verified conservation identities. An
inactive pool remains covered because nonnegative physical pool flows
must all vanish when their total is zero.

## Independent exact checks

The new standard-library checker
[check_box_rank_support_second.py](../code/pooling_bypass_paths/check_box_rank_support_second.py)
enumerates vertices by exact rational Gaussian elimination in small
signed path, cycle, and disconnected networks. Feasible seed flows
generate finite arc/node intervals, including equalities and isolated
vertices. It independently compares all-subset rank values and greedy
support values against the enumerated flow vertices. It also checks
interval overlap and convex interpolation in the original arc variables.

Run: `python code/pooling_bypass_paths/check_box_rank_support_second.py`.
Result: **36 networks, 146 flow vertices, 672 subset-support comparisons,
288 signed objectives, and 864 exact interpolated witnesses passed**.
These finite checks test the new support and interval mechanism. They
do not implement the symbolic parameter algorithm or replace the proof
of algebraic complexity.

## Source comparison and limits

The exact box-rank formula and sorted-prefix greedy rule are prior;
their direct primary attribution is recorded in
[the box-truncation source note](parametric-path-cut-box-truncation-source.md).
The Section 1 clamp argument is an elementary specialized dynamic
program, with no claim to a new general submodular algorithm.

The checked pooling comparisons remain relevant. Boland–Kalinowski–
Rigterink exclude bypasses in their fixed-input one-pool theorem.
Baltean-Lugojan–Misener permit bypasses and fixed demands but drop feed
availability and pool capacity in their tractable model. Neither checked
statement yields this arbitrary common lower/upper capacity extension
with retained exact source and quality contracts. Their exact model
locations are documented in
[the contracted-pooling source assessment](pooling-quality-scaled-contracts-novelty.md)
and were checked during the same bounded review session. No matching
restricted theorem was located; this is not exhaustive priority clearance.

The result closes the previously unfinished common-capacity route. It
does not establish arbitrary source or product intervals, dense arc-cost
optimization, higher bypass degree, or a strongly polynomial arithmetic
algorithm. Earlier paragraphs of the investigation intentionally record
the unresolved stage; its final status and cross-links should identify
Sections 3–4 as the completed resolution.

## Promotion confirmation

The reviewer read the complete promoted
[common-capacity theorem](../results/pooling-contracted-common-capacity-algorithm.md)
on 2026-09-05. Its reordered Sections 2–3 retain the audited rank and
physical-capacity arguments. The unusable-pool branch explicitly rejects
a positive common lower bound after forcing all pool arcs to zero.
The affine-rank-one corollary uses the previously verified scalar
compression and leaves all physical throughput bounds unchanged.
The theorem continues to allow arbitrary scalar source values while
requiring exact external contracts and bypass degree at most two.
The polynomial algebraic witness bound and economic limitations are
unchanged. **Promotion confirmation: PASS.**

The author closed the equation-number gap left by removing the historical
outline. I checked the consecutive labels (1)–(6) and their updated
internal references. No additional tests were needed for this
reorganization.
