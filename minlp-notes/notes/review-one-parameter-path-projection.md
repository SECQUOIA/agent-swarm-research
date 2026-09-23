# Independent review: one-parameter polygon-path projection

Date: 2026-09-05. Reviewer: `pooling_degree_two`. Verdict: **PASS** for
[the quasipolynomial projection theorem](one-parameter-path-projection-investigation.md)
under its bounded-coordinate, explicitly encoded, fixed initial degree,
and single-parameter assumptions. This audit does not settle the
unbounded-attachment pooling problem or establish literature priority.

## Local elimination and stable row selection

On a cell where the signs of all coefficients of the eliminated variable
are fixed, one-variable Fourier–Motzkin elimination produces at most a
quadratic number of candidate rows. Its positive multipliers are selected
using those signs. Symbolically each row uses only two products and an
addition. Pairs within either child are needed for endpoint domain
restrictions and are correctly included.

Include permanent endpoint box inequalities. The signs of augmented
row minors of orders one, two, and three determine the following:
which two row normals are independent; whether their boundary intersection
satisfies every candidate inequality; and the sign of any constant-only
row. Identically zero minors are handled without creating roots. Thus
candidate-vertex feasibility is invariant inside an open sign cell.

Choose at one sample a small subset that describes the exact projected
polygon, retaining the box. To verify this same subset throughout the
cell, consider every intersection of two selected independent boundaries.
Its membership in the selected bounded polyhedron and its satisfaction
of every omitted row are invariant. Every nonempty bounded polyhedron
in the plane has a vertex of this form, including a point or segment.
Every selected vertex therefore satisfies every omitted row throughout
the cell, proving equivalence by convexity. Emptiness is also invariant:
no independent row-pair intersection can become a feasible vertex
without changing one of the recorded signs.

The pointwise additive projection bound controls the size of the selected
subset. A full-dimensional projected polygon has an original candidate
row supporting each facet. A segment needs its affine-hull equality and
two endpoint bounds; an irredundant point description uses at most four
rows. These degeneracies introduce only a fixed additive overhead.

## Recursion, algebraic exceptional points, and bit size

In one parameter, the common refinement of two partitions has at most
a constant times the sum of their cell counts. At each balanced node,
its polynomial-size candidate row list generates polynomially many
minor roots per common child cell. Hence the stated recurrence
`L_parent<=N^c(L_left+L_right)` and logarithmic depth give
`N^(O(log(h+1)))` total cells.

No selected row coefficient depends on the numerical sample used to
select it. Rows remain integer polynomials obtained from the symbolic
Fourier–Motzkin combinations. Therefore the maximum degree at most
doubles per balanced level, giving `O(dh)`, and the coefficient-height
recurrence also remains polynomial after accounting for polynomial
convolution. Cross-cell root comparisons only involve explicitly encoded
univariate polynomials of polynomial degree and height.

At an isolated root, the draft correctly performs elimination and pruning
in that root's represented real-algebraic field, but retains the selected
symbolic row expressions. This avoids carrying the entire unpruned
quadratic list at every later level. It also avoids adjoining a new field
for every operation: all evaluated rows belong to the field of the same
parameter value. Root isolation and separation bounds give polynomial
bit encodings for isolated endpoints and samples on open cells.

The theorem controls the endpoint relation. A later algebraic lift at a
fixed parameter may use divisions by nonzero evaluated coefficients;
this stays in that parameter field together with any supplied endpoint
field. The draft does not claim a separate uniform polynomial-size
encoding for arbitrary externally supplied endpoint fields, and no such
claim is needed for its cell-count conclusion.

## Scope and checks

The conclusion excludes an exponential-in-full-input-length number of
necessary cells in the stated explicit representation. It does not prove
a polynomial bound, a matching quasipolynomial lower bound, or a bound for
several parameters. It also does not retain dense pool mass or attribute
aggregates, so applying it to local pooling-node projections alone does
not solve global pooling feasibility.

This is a complete symbolic proof audit. No new numerical test is claimed:
the endpoint facet bound already has independent exact polygon checks,
while the new conclusions concern sign-invariant redundancy, symbolic
height recurrences, and root-count asymptotics.
