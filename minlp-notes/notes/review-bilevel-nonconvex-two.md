# Second independent review of the exact nonconvex scalar solver

Date: 2026-09-07. Verdict: the mathematical specialization and revised implementation pass this review within their stated scope.

Reviewed sources:

- [Algorithm and proof](bilevel-nonconvex-scalar-algorithm.md).
- [Exact solver](../code/bilevel_nonconvex/scalar_solver.py), including the revised incremental envelope construction.
- [Conjugate and contact-set positioning](bilevel-nonconvex-source-positioning.md), for its mathematical identities and explicit example.

This is an independent proof and code review. The reviewer did not implement the solver. The review's [exact checker](../code/bilevel_nonconvex/review_two.py) is separate from the author checks and the other review.

## Corrections made during review

The original implementation used the arithmetic midpoint of adjacent algebraic partition cuts as an interior witness. Two quadratic cuts can belong to different quadratic fields, so their midpoint can have degree four. This does not invalidate optimality, but conflicts with the degree-at-most-two output claim. The author replaced these midpoints with exact rational interior samples, both for branch comparisons and for attained constant-objective witnesses. The resulting output claim is sound.

The original input guard rejected Python floats but accepted SymPy floating numbers through rational conversion. The author tightened it to rational text or values that are already exact rational numbers. The checker confirms rejection of both Python and SymPy floating values and of irrational algebraic input.

The operation-count discussion should treat algebraic signs and rational interior sampling as polynomial-bit primitives. Dyadic sampling can take a number of iterations depending on coefficient bit length. The polynomial bit-time conclusion remains valid; a bound only in `N` must not silently count the entire sampling loop as one scalar arithmetic operation.

## Proof audit

The fiber construction works for signed and zero aggregate weights and for fixed box coordinates. On every multiplier interval with positive aggregate slope, the inverse is rational affine. Zero-slope multiplier gaps omit no aggregate interval. The first and last event values give the extreme attainable aggregates; the one-point aggregate case is handled separately. Strict convexity on each fiber ensures uniqueness, including at shared piece boundaries.

The candidate list is complete. Positive-curvature pieces contribute their constrained stationary branch and endpoints. Negative-curvature pieces contribute endpoints. A zero-curvature piece contributes a full interval exactly at its flat tariff, if globally minimal. Thus the construction does not substitute follower stationarity for global optimality.

On an open leader cell, equal winning value polynomials have equal derivatives. Each derivative is `gamma*w(x)`, and `gamma!=0`, so all winners describe the same aggregate and, by fiber uniqueness, the same full response. This justifies using one open-cell response under both semantics.

The incremental envelope maintains the correct open-cell minimum by induction. Each insertion retains every relevant cost root, including tangencies that change no interval winner, and every branch-domain endpoint. Merging adjacent intervals with one winner does not remove retained contact points. A final isolated tie must arise at a retained domain boundary, envelope boundary, or contact with the earlier envelope; identical value polynomials give the same response on an open cell. All-branch point scans recover isolated candidates and all original flat response intervals. A candidate with a singleton tariff domain is therefore not lost when constructing open cells.

Within a cell, affine upper rows cut out an interval, possibly a singleton, and revenue is quadratic. Limiting endpoints, a feasible stationary point when concave, and a rational interior witness for a constant objective suffice. Inclusion is tested against the original open cell. At an isolated tariff, optimistic feasibility intersects each actual response interval with the upper rows; robust pessimistic feasibility tests every row at every interval endpoint. Worst revenue also occurs at an endpoint. These are exact because response reconstruction and all upper expressions are affine in the fiber coordinate.

The final comparison correctly prefers an attained candidate over an equally valued unattained limit. An unattained reported pair is only a limit of feasible cell responses. Optimistic attainment also follows independently from compactness and closedness of the true follower graph and upper constraints.

Intersection cuts have degree at most two. Row intersections inside cells are rational. At an algebraic point, response reconstruction remains in its quadratic field; a flat tariff is rational. Rational interior samples remove the earlier field-compositum problem. Comparisons between different quadratic fields have bounded degree at most four. Coefficient bit lengths and root-separation requirements are polynomial, establishing the stated bit-complexity conclusion with standard exact algebraic primitives.

## Independent exact checks

Run:

```bash
/home/sgusev/miniconda3/envs/minlp-notes/bin/python code/bilevel_nonconvex/review_two.py
```

Result:

```text
random_original_space_face_comparisons: 350
random_tied_cases: 1
atlas_point_and_cell_face_comparisons: 72
incremental_envelope_full_partition_comparisons: 30
explicit_edge_cases: 11
status: passed
```

The main independent reference enumerates stationary points on faces of the original box using the original dense Hessian `Diag(d)-h*u*u^T`. It does not use the scalar fiber reduction. Vertices and nonsingular stationary faces suffice for the global value: if a global minimum lies in the relative interior of a singular face, its restricted Hessian is positive semidefinite; a null direction preserves the objective and reaches a smaller face. Repeating ends at a face with nonsingular restricted Hessian or a vertex.

The random cases use rational data, both signs of `gamma`, signed and zero aggregate coefficients, fixed coordinates, and Hessians that need not be positive semidefinite. Atlas tests check actual returned point responses and cell winners against original-space face enumeration. A separate generic branch test compares incremental-envelope winners to a full pairwise-intersection partition. Explicit cases cover flat continua, an upper equality forcing an interior flat response, universal upper-row infeasibility, negative tariff coupling, fixed aggregate, a pessimistic unattained supremum, input exactness, rational sampling, isolated tangencies, and singleton candidate domains.

For the discontinuity check, `d=u=gamma=1`, `h=2`, `c=0`, `z in [0,1]`, and `x in [0,1]` give follower objective `-z^2/2+x*z`. Optimistic revenue attains `1/2` at the tie tariff; pessimistic revenue has supremum `1/2` approached from below and not attained. Both results are returned correctly.

## Contact identity and scope

The source-positioning identity `v(x)=-psi*(-gamma*x)` follows directly from conjugacy. Its contact-filtered argmin formula is correct: the affine function formed from the true minimum and tariff lies below `psi`, hence below its closed convex envelope. Consequently the original and convexified minimum values agree, and an original minimizer must be a contact point. The converse holds by equality of the values.

The stated one-coordinate false-feasibility example is also correct. Its untariffed function is `-z^2-z`, its convex envelope is `-2z`, and at tariff `2` the original minimizers are only `{0,1}` while the convexified model admits all of `[0,1]`. The checker confirms that the actual solver rejects the upper equality `z=1/2` for the entire allowed tariff range.

This review establishes correctness of the stated scalar, aligned-tariff, quadratic-aggregate specialization. It does not establish novelty of conjugation or envelope construction, solver superiority, or practical performance beyond the separately reported experiments. It does not extend the implementation to general polynomial aggregates or additional leader or aggregate dimensions.
