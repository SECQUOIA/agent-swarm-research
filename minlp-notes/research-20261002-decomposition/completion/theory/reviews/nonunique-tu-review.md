# Independent review of nonunique TU exact output

Date: 2026-10-03. Reviewed
[the completed proof](../nonunique-tu-exact.md), the parent
[TU filtered-grid theorem](../../../constraints/tu-filtered-grid.md), and
the complete [polytope recovery argument](../../../../research-20261002/new-direction/proximal-polytope-recovery.md).

**Verdict: the stated theorems are supported by the proof.** No mathematical
gap requiring a theorem restriction was found. The exact-output argument
allows arbitrary optimal sets; the accuracy-independent table-size bound
requires finite continuous coordinate projections. Neither assertion is a
width-FPT result or a method to predict the growth constant.

## Proof checks

1. **Disconnected retained domains.** Every retained interval endpoint is
   on the previous mesh and therefore on the refined mesh. A feasible point
   has a surrounding cell inside its own retained coordinate components.
   An isolated coordinate node is fixed. After these fixed coordinates and
   the integer labels are held constant, the scaled right-hand side is
   integral and the remaining constraint matrix is a TU column submatrix.
   Appending coordinate bounds preserves TU. Thus feasible mean-preserving
   corner rounding stays inside the disconnected domain. It does not need
   a convex hull of that domain.

2. **Preservation and original-domain certification.** On a continuous
   cell, every feasible corner has one of its two endpoint labels, so the
   smaller endpoint marginal minus the rounding allowance bounds the
   objective of every feasible point in the cell. Singleton and discrete
   tests use the one corresponding marginal. Consequently every optimizer
   survives each simultaneous coordinate restriction. The grid incumbent
   also survives and remains available on every refined grid. Removed
   points have objective strictly above the then-current incumbent and
   hence above the final incumbent. This establishes the certificate for
   the original domain when its entire restriction history is replayed.

3. **State-count constants.** A passing endpoint has a grid witness with
   objective at most `f* + 2 E_j`, giving projection distance at most
   `a_j = sqrt(n_c L/(4g)) h_j`. A retained cell adds at most `h_j` to this
   distance. Each resulting interval has length `2 a_j + 2 h_j`, so its
   next mesh has at most `5 + ceil(2 sqrt(n_c L/g))` nodes. Summing over at
   most `r` distinct projected optimal values gives the claimed bound.
   Different coordinates may use different optimizers; no unjustified
   joint assignment or component enumeration enters this argument.

4. **Recovery and omitted integer labels.** The imported recovery proof
   uses a bounded stationary polytope in the original coordinate space,
   not vertices of the possibly unbounded multiplier formulation. Its
   integer nullspace basis gives a uniform denominator bound, and its
   summed-slack argument snaps extra nearly active rows simultaneously.
   Both gradients are orthogonal to the selected face directions, so
   every feasible recovery output has the same quadratic value. Replacing
   an explicit integer list by its bounding interval is sound only in
   this analysis construction: recovery fixes the actual allowed label
   of the feasible grid incumbent. Every point then belongs to the same
   allowed slice. A diagnostic below checks a case where the omitted
   intermediate integer label would otherwise give a strictly better
   objective.

5. **Growth-independent acceptance and finite termination.** Once the
   unconditional interval has width less than `1/(4 V^2)`, it contains
   exactly one rational with denominator at most `V`, namely the optimum.
   A returned feasible point is accepted only when its rational objective
   equals that isolated value. Thus an early, invalid face guess cannot
   produce a false certificate. The classical set-growth bound is used
   only to prove that a grid incumbent eventually satisfies the imported
   recovery distance threshold. On an optimal integer slice, distance to
   the full optimal set is no larger than distance to that slice's optimal
   set. Every other nonempty slice has a positive gap and bounded distance
   to the global set. Finitely many slices therefore give some common
   positive growth constant, also with holes in the integer lists.

6. **Arithmetic and complexity.** Dyadic coordinates and fixed rational
   objective coefficients give polynomial-length finite DP values and
   marginals. Infeasibility remains a flag. The height, slack, and distance
   thresholds have polynomial binary length in the original input. Only
   selected row indices and fixed integer labels enter the final linear
   system; the incumbent's long continuous denominators do not enter its
   coefficients. A rational feasible solution of the lifted linear system
   has polynomial encoding length despite multiplier lineality. The level
   count is `poly(I) + O(log kappa)`; general optimal continua can still
   cause unbounded growth of the intermediate grid sizes.

7. **Example and scope.** The three-variable example has exactly the two
   stated optimizers. On each half of its `z` range, comparison to the
   corresponding optimizer proves growth `g=1/6`; the Hessian maximum
   absolute row sum is `12`. Independent copies preserve these constants.
   The hull keeps all intermediate `z` nodes, whereas the union eventually
   discards the middle. This demonstrates the representation issue on an
   easy instance and does not establish general empirical superiority.
   Exact optimization of arbitrary rational quadratic programs, TU
   rounding, tree DP, rational reconstruction, qualitative set growth,
   and the imported recovery lemma are not claimed as new ingredients.

The author applied the one minor clarity suggestion: define `W` explicitly
over the continuous coordinates. The already separate `n_c=0` branch
needs no width parameter. This clarification does not affect the proof.

## Targeted checks actually run

`python research-20261002-decomposition/completion/theory/reviews/check_nonunique_tu_review.py`

Passed nine exact-rational union-grid levels on the coupled two-optimum
example. The check uses exhaustive feasible assignments independently of
the author's tree DP. It verified preservation, passing-endpoint
projection bounds, incumbent persistence, and next-grid state counts.
There were at most 17 states in a coordinate, five levels with a
disconnected retained `z` domain, and 97 passing-endpoint checks. It also
solved the stationary recovery systems on both allowed slices of a
`{0,2}` integer domain whose omitted label `1` would lower the optimum.

`python research-20261002/new-direction/check_polytope_recovery_review.py`

Passed the eight imported recovery cases: thirteen stationary-polytope
vertices, ten recovery vertices, and four extra facet snaps. These include
redundant and zero rows, lower-dimensional domains, disconnected optimal
faces, rational coupled constraints, integer assignments, and negative
curvature normal to the feasible affine hull.

These finite diagnostics support the review; they do not replace the
proof. No project-wide tests, CI checks, or external literature search
were run in this review. The primary theorem statement for qualitative
growth was supplied in the repository's source note and was not
independently re-fetched.
