# Prior art for expected semiconcave grid-cell counts

Date: 2026-10-02. This is a focused comparison for the reviewed result in
[`smoothed-semiconcave-cells.md`](../new-direction/smoothed-semiconcave-cells.md).
It records close prior art and the comparison boundary; it is not a
completeness or novelty claim.

## Candidate result

The candidate studies a fixed continuous box and a continuous objective with
an upper coordinate-curvature bound. Independent random linear coefficients
are added, with a density bound for each coordinate. At any mesh level, a
local comparison with the two adjacent grid points puts each coefficient into
a deterministic interval whose length is at most the curvature term
`alpha h_i` plus the near-optimality tolerance divided by `h_i`. Multiplying
the coordinate probability bounds and summing over the tensor grid gives a
bound on the expected number of near-optimal grid points. A corrected-corner
branch-and-bound procedure processes only cells with a surviving lower bound;
the resulting expected number of processed cells per level stays bounded as
the mesh is refined. The arithmetic-oracle algorithm therefore has expected
logarithmic dependence on target accuracy at fixed dimension. The result does
not assume quadratic growth, convexity, differentiability, or a unique
minimizer.

The separate recourse application uses independent random tilts in a supplied
low-dimensional factor coordinate. It produces correlated, lower-dimensional
perturbations in the original decision variables, and its convex-QP oracle
cost must be counted in addition to the cell work. The candidate does not
claim exact optimization under one fixed finite perturbation distribution at
arbitrarily fine accuracy.

## Closest comparison: smoothed Pareto counts on finite non-integral sets

Röglin and Rösner, [“The Smoothed Number of Pareto-optimal Solutions in
Non-integer Bicriteria Optimization”](https://roeglin.org/publications/TAMC17.pdf),
TAMC 2017, LNCS 10185, pp. 543–555, Theorem 2, study a finite set
`S` contained in `[0,1]^n`. One criterion is an arbitrary ranking on `S`; the
other is a linear profit with independently perturbed coefficients of bounded
density. Under their `(k, delta)` structural property, they bound the expected
number of Pareto-optimal solutions by
`O(n^2 delta^{-1} sum_i k_i phi_i)`, where `k_i` is the size of the
coordinate anchor set and `phi_i` bounds the corresponding density. This is
the closest comparison because it handles real-valued coordinates and uses
random linear coefficients to bound an expected count over a finite feasible
set.

The differences matter here. Their feasible set is finite; “non-integer”
means a finite set of real-valued vectors, not a continuous box. Their count is
of exact Pareto-optimal solutions, not grid nodes within an additive
objective tolerance. Their structural parameter also includes a coordinate
separation `delta`; for increasingly fine full tensor grids, both the number
of coordinate values and the inverse separation deteriorate with the mesh.
The theorem therefore does not give a mesh-uniform bound for the candidate's
near-optimal nodes or retained cells. The candidate's local adjacent-point
comparison instead yields a count uniform over successively finer grids.

## Other smoothed global-optimization comparison

Kelner and Nikolova, [“On the Hardness and Smoothed Complexity of
Quasi-Concave Minimization”](https://doi.org/10.1109/FOCS.2007.4389517),
FOCS 2007, Theorem 2.9 and Lemma 2.10, analyze a constant-rank
quasi-concave objective over an integral polytope whose vertex coordinates
are bounded. Their perturbation randomly rotates the low-rank subspace of
the objective. They bound the expected number of vertices in the projected
shadow, giving an expected polynomial-time smoothed algorithm for fixed rank.
This is a strong comparator for smoothed global optimization with a
low-dimensional objective structure. Its perturbation is a random rotation,
and its count is projected-polytope vertices; it does not bound near-optimal
grid cells under independent additive linear tilts of a semiconcave value
function.

Classical spatial branch-and-bound supplies deterministic underestimators
and convergence frameworks, but the sources checked do not provide this
expected cell-count bound. That methodological background does not itself
close the gap between worst-case cell counts and the candidate's
mesh-independent expected count.

## Assessment and search boundary

The focused search included smoothed Pareto counts for finite non-integral
sets, near-optimal solution counts under random linear objectives, smoothed
spatial branch-and-bound, and low-rank smoothed global optimization. The
closest prior is the finite non-integral Pareto-count theorem of Röglin and
Rösner; the closest general global-optimization algorithm is
Kelner–Nikolova. Neither states the candidate's expected count of
additively near-optimal nodes and branch-and-bound cells on a continuous
semiconcave box, uniform across nested mesh levels.

This is a scoped comparison only. It does not establish that the combination
is new, and it does not assess related results under formulations outside
these search terms.

## Sources checked

- Röglin and Rösner (2017), author-hosted full paper, pp. 5–7, Definition 1
  and Theorem 2; this is a finite subset of `[0,1]^n` with the stated
  `(k, delta)` condition. The complete local author PDF was read.
- Kelner and Nikolova (2007), local full-text extraction and the original
  Theorem 2.9/Lemma 2.10; the result uses a random rotation of a fixed
  low-rank objective subspace over an integral polytope.
- [`smoothed-semiconcave-cells.md`](../new-direction/smoothed-semiconcave-cells.md),
  including its separate direct proof and exact-rational verification record.

The Röglin–Rösner paper has been routed to the literature-ingest agent for
the normal metadata/full-text workflow. No literature knowledge-base files
were edited for this audit.
