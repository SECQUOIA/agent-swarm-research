# Independent review: bounded-block-cycle-rank original-space hull

Date: 2026-09-07.
Reviewer: independent `review_bounded_rank` agent.

Reviewed: `results/network-simplex-bounded-rank-hull.md`, SHA-256
`f7d40379af25942ff1b8822afc433d9cf77059cbcdfabde7ccaa1bbf932b966e`.
This identifies the candidate before any subsequent revisions.

**Verdict: the theorem and proof pass this review.** I found no mathematical
issue requiring a correction. The result establishes a finite original-variable
separation construction and an integer coefficient bound depending only on the
maximum block cycle rank. It does not establish a new general polynomial-time
separation result, computational superiority over extended formulations, or
sharpness of the coefficient bound at every rank.

## Proof checks

1. **Block coordinates and state merging.** Differences between feasible flows
   are circulations. Circulations split into the undirected biconnected blocks,
   including independent loop coordinates. Once a global reference flow with
   the required balances is fixed, independent block coordinate choices
   therefore preserve those balances. Each block can merge its unobserved
   labels: nonnegative homothetic copies of the same nonempty convex domain
   sum to the copy with total weight. Reconstruction splits the merged state
   proportionally to its original weights, using the same weights across
   blocks. The usual flow and simplex checks and fixed bridge observation
   equations are necessary parts of the description, as stated in the proof.

2. **Repeated normals and zero weights.** Taking the minimum over all parallel
   inequalities is exact. The matrix has both signs of every coordinate
   vector. Consequently a zero-weight state is forced to the zero cycle
   vector by its base bounds; nonzero observations then make that state
   infeasible. No division by a weight is used in the oracle.

3. **TU and feasibility certificates.** The tree/chord construction is a
   network matrix with appended identity rows. Signed and deduplicated rows
   remain totally unimodular. An extreme nonnegative dependency has minimally
   dependent support of size at most rank plus one; its primitive coefficients
   are all one by total unimodularity. If it uses opposite normals, minimality
   confines it to that pair. Thus the local certificate coefficient argument
   also covers repeated or canceling observations correctly.

4. **Edge directions of lower-dimensional slices.** At a relative interior
   point of an edge, the tight defining rows span a space of codimension one
   in the ambient cycle-coordinate space. Rows tight throughout the polytope
   provide the missing affine-hull equations. The cofactor construction
   therefore includes the edge direction even for lower-dimensional state
   slices. A point requires no edge directions.

5. **Arrangement refinement.** An objective inside an arrangement chamber is
   not perpendicular to any possible edge. Its maximizing face in any
   nonempty state polytope is therefore a vertex. The maximizer cannot change
   within the connected chamber without a nonunique maximum. Continuity
   extends the support formula to the closed chamber. Coordinate hyperplanes
   make the chamber pointed, so its extreme-ray inequalities imply the
   support inequality throughout it. This argument is valid for points,
   segments, and arbitrary lower-dimensional sums.

6. **Dual basis formulas.** The nonnegative dual system has full row rank and
   a nonempty feasible region because signed coordinate normals are present.
   It is pointed. Bounded nonempty primal states have an attained dual optimum
   at a basic solution. A smaller independent support extends to a full
   basis with zero additional coefficients. Primal degeneracy and lack of
   interior do not invalidate the minimum over dual bases.

7. **The transformed cofactor bound.** This is the substantive bound that a
   direct triangle inequality would miss. If `h` is primitive and orthogonal
   to the selected independent edge directions, then `B^{-T} h` is primitive
   because `B` is unimodular. It is orthogonal to the transformed directions
   `B d_i`. Their entries are in `{-1,0,1}`: each scalar product is a full
   minor of the original TU matrix. Their primitive cofactor vector therefore
   has entries at most `H_s`. Dividing cofactors by their common divisor can
   only improve the bound. The argument works for every nonsingular row
   basis, not just chord coordinates.

8. **Affine cuts and coefficient accounting.** Nonnegative multipliers make
   each branch expansion an affine upper bound on the support. Selecting an
   active branch and a minimizing dual basis preserves the violation at the
   queried point. Nonsingular row bases cannot use a normal and its negative,
   so an observed product contributes at most once in its state. Different
   labels have different product variables. Only the left side uses actual
   flow coordinates, with the ray coefficients. Local certificates and the
   original equations respect the claimed bound. It is essential to retain
   the stated convention: the flow/product coefficients are bounded in this
   representative, with rational simplex coefficients. Clearing all
   denominators would not preserve the same numerical bound.

9. **Complexity.** Both the signed-normal universe and direction universe have
   size `2^{O(s)}`. Enumerating subsets of size at most `s+1`, and the product
   of the ray and basis libraries, costs `2^{O(s^2)}`. The total number of
   observed block/label pairs is at most the observation count. Tree
   coordinate construction and endpoint updates respect the claimed
   parameter-dependent linear arithmetic bound. Rational additions can grow
   bit length, but only polynomially in total rational input length and the
   parameter-dependent library length. This is consistent with the explicit
   distinction between rational arithmetic counts and bit complexity.

## Independent computational checks

The retained script is `code/network_simplex_review/bounded_rank.py`; its output
is `code/network_simplex_review/bounded_rank_results.json`. Run:

```sh
python code/network_simplex_review/bounded_rank.py
```

It does not import the candidate separator. It constructs signed normals,
primitive cofactor directions, arrangement-ray candidates, and all nonsingular
row bases independently. All determinant and multiplier assertions use integer
arithmetic. The two matrices represent the star-tree coordinates of `K4` and
`K4` with one duplicated chord.

| Check | Rank 3 | Rank 4 |
| --- | ---: | ---: |
| Distinct signed normals | 12 | 14 |
| Exact square minors checked for TU | 454 | 3,059 |
| Primitive edge directions | 7 | 12 |
| Oriented support-ray candidates | 18 | 50 |
| Nonsingular row bases | 128 | 384 |
| Largest dual multiplier found | 2 | 2 |
| Theorem bound | 2 | 5 |
| Support comparisons against independent LP | 1,620 | 4,500 |
| Minkowski membership comparisons against full disaggregation | 90 | 90 |

All checks passed. Every transformed direction entry and every transformed ray
coordinate is checked against the claimed bound for every enumerated basis.
The LP comparisons include full-dimensional states, independent equality slices
of every intermediate dimension, point states, and zero-weight states. Sum
membership comparisons include constructed feasible points, guaranteed distant
infeasible points, and independent random candidates.

The LP comparisons use floating-point HiGHS and tolerance `1e-8`; they supplement
the mathematical proof and exact structural checks. The multiplier value two
on `K4` shows that this dual-basis library actually uses the rank-three bound.
It does **not** by itself show that every exact hull description needs a
coefficient of magnitude two: that would require a specific unavoidable facet
or a comparable argument modulo the hull's affine equations.

## Scope of this verdict

This review audits correctness and the stated complexity, not priority in the
literature. The candidate accurately identifies normal-fan refinement and
network-matrix total unimodularity as classical tools and disclaims new general
separation tractability. Its possible new contribution is their precise sparse,
blockwise specialization and the resulting original-variable coefficient bound.
A practical speed claim still requires the compressed extended baseline and
measurements on representative workloads.

## Follow-up review: sharp rank-three example and final theorem snapshot

Reviewed the complete updated result, including Sections 8 and 9, at SHA-256
`cf2b8364093afb03b92bd30570d27e65120222861a893241fe5d7f34b3831638`.

**Verdict: pass. The rank-three integer coefficient bound two is sharp.**
The new seven-observation example supplies the necessity argument that was
absent from the earlier library experiment. No correction is required.

For the stated arc order `(12,13,23,01,02,03)`, the displayed matrix satisfies
`A C = 0` under the usual incidence convention. Its first three rows are the
identity, so these are precisely the claimed chord coordinates. Unit capacities
and the reference flow `v = (1/2,...,1/2)` give `|C theta| <= 1/2`.
The aggregate flow displayed in the result equals `v + C (1/8,0,1/8)` and has
the required balances.

Each disaggregated state has weight `1/4`, reference part `v/4`, and cycle bounds
`|C theta^j| <= 1/8`. The seven observations imply:

- State one has its first two coordinates `p = U-1/8` and `q = V-1/8`.
  Its observed arc `02` fixes `-theta_1 + theta_3 = 0`, hence `(p,q,p)`.
- State two fixes `theta_1 = 0` and `-theta_2-theta_3 = 0`, hence
  `t(0,1,-1)` with `|t| <= 1/8`.
- State three fixes `theta_3 = 0` and `theta_1+theta_2 = 0`, hence
  `s(1,-1,0)` with `|s| <= 1/8`.

For `h=(1,1,1)`, residual arc bounds imply
`h theta* <= 1/8+1/8 = 1/4`. States two and three have zero `h` value, while
`h theta_bar = 1/4`. Therefore every point of the section satisfies
`2p+q >= 0`, which expands exactly to `2U+V >= 3/8`.

For `w=2p+q >= 0`, the proposed witness has
`theta^2=(0,-q/2,q/2)`, `theta^3=(q/2,-q/2,0)`, and
`theta*=(1/8-w/2,0,1/8-w/2)`. Its sum with `(p,q,p)` is exactly
`(1/8,0,1/8)`. In the stated open box `|p|,|q| < 1/32`, the first state's arc
values are `p,q,p,p+q,0,-p-q`, all within the state capacity bounds. The second
and third witnesses are strictly within their segment bounds. Finally
`0 <= w < 3/32` places each nonzero residual coordinate between `5/64` and
`1/8`, and its arc values are `a,0,a,a,0,-a`. Thus the converse works on the
entire asserted neighborhood, including `w=0`.

The inference from the section to ambient coefficient necessity is also valid.
The section has nonempty interior in its two free product coordinates, so every
ambient affine-hull equation restricts to the identity there. At an interior
point of the boundary segment, a finite inequality description must contain
at least one active inequality whose restriction is not an identity; otherwise
all nonconstant inequalities would be slack in a neighborhood and could not
produce the boundary. Such a supporting restriction has normal proportional to
`(2,1)`. Since every other original coordinate has been fixed, these are the
actual coefficients on `U,V` in that ambient inequality. The same reasoning
applies to any relative facet description. Adding ambient affine-hull equations
cannot change this ratio, because those equations have zero coefficients in
the two free coordinates after restriction. An integer coefficient description
with all product coefficients in `{-1,0,1}` is therefore impossible.

### Additional independent computation

Extended `code/network_simplex_review/bounded_rank.py` with a separate
`audit_sharp_k4()` check. It assembles the directed incidence matrix directly
from the six arcs, checks `A C = 0`, and builds the raw disaggregated model with
24 state/arc flow variables. This model uses four copies of the original flow
balances, scaled capacities, aggregate arc-flow equations, and the seven
observation equations; it does not use cycle-space separation formulas.

For every pair `p=a/256`, `q=b/256`, with integers `-7 <= a,b <= 7`, it checks
raw-state LP feasibility against the stated half-plane. All **225 comparisons
passed**. In addition:

- **116 feasible points** have their proposed four arc-flow vectors checked
  with exact rational arithmetic: capacities, all node balances, aggregate
  flows, and every observed product.
- **109 infeasible points** have a negative exact support certificate.
- **Seven boundary points** verify the equality case.

These checks include actual original graph flows and products, rather than only
abstract state polytopes. The rational witness checks are exact; the raw-state
LP cross-checks remain numerical. The complete updated theorem remains sound
under this review. The direct proof and this review establish correctness and
rank-three sharpness, while literature priority and computational advantage
remain separately assessed claims.
