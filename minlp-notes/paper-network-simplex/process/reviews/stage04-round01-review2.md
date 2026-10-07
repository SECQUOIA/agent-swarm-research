# Stage 4, round 1 — independent review 2

**Verdict: accept this stage. No major or minor defects identified.**

I reviewed the frozen `process/snapshots/stage04-round01` snapshot, including all
claims in `sections/04-bounded-rank.tex` and the earlier results used by them.
The principal emphasis was the new five-product K4 construction, its relation
to actual graph coordinates, and the new recovery theorem. I did not read other
current-round reports, coordinate reviews, edit manuscript sources, or spawn
agents.

## Enumerated findings

1. **No major findings.** I found the new five-product example correct, the
   coefficient-ratio transfer valid even modulo affine equations, and the rank
   library and recovery proofs complete within their stated scope.
2. **No minor findings.** I have no required local correction.

## Mathematical assessment

### R2-S4-C1 — normal matrix and local feasibility (verified)

At `sections/04-bounded-rank.tex:18–103`, each original cyclic-block arc has a
nonzero row in the fundamental-cycle matrix. Repeated rows and opposite
orientations are correctly combined into upper-bound normals. The observation
minimum includes both signs of each equality, retaining consistency conditions
and forcing zero-weight states to zero when feasible.

The positive-circuit proof is valid: an extreme positive dependence has a
one-dimensional dependence space and no dependent proper support. Cofactors
of the corresponding TU submatrix give primitive coefficients of magnitude one.
A repeated product can occur in both signed normals only when the circuit is
that opposite pair, in which case it cancels if both branches select it.
The affine branch is an upper bound on the circuit expression, so its
nonnegativity is indeed a globally valid inequality.

### R2-S4-C2 — edge directions, chambers, and support multipliers (verified)

At lines 105–228, the cofactor construction gives primitive ternary edge
vectors and ternary `Md`. Tight-row rank at the relative interior of an edge
is correctly justified in ambient dimension even for a lower-dimensional
state polytope. Coordinate directions are included, making each objective
chamber pointed.

Within a chamber, changing the maximizing vertex would require an objective
perpendicular to an edge direction. This proves linearity of each support
function on the chamber closure, so checking all chamber rays suffices for
all objectives. The argument includes point states, lower-dimensional sums,
and the empty sum.

The multiplier bound uses more than integrality of the inverse basis: the
unimodular change of coordinates preserves primitivity, and the transformed
edge vectors `Bd_i` remain ternary. Thus the cofactor/Hadamard bound applies to
`B^{-T}h` itself. This validates the sharper bound by `H_s`, rather than an
unjustified multiple of that bound. Rank one is treated separately.

The basis support formula includes optima supported on fewer than `s` rows:
extending an independent support to a basis adds zero multipliers. It therefore
does not assume a nondegenerate or full-dimensional state domain.

### R2-S4-C3 — complete description, coefficients, and complexity (verified)

At lines 230–291, the local feasibility tests precede use of the support formula.
Nonnegative dual multipliers preserve the concave minimum-of-affine form.
Selecting an active basis and active endpoint branch gives a valid affine
majorant that agrees at the violating candidate.

A nonsingular basis cannot contain both signs of a row, so one observation is
used at most once per state. Different states have distinct original product
coordinates, and aggregate cycle coordinates are distinct chord arc flows.
This proves the stated flow/product coefficient bound in the specified row
scaling. The number of normal subsets, edge-direction subsets, rays, and row
bases is `2^{O(s^2)}`; their finite products keep that order. The sparse state
count then yields the input-linear factor. The text correctly avoids claiming
that this large parameter factor is computationally attractive.

### R2-S4-C4 — recovery without an online LP (verified)

At lines 293–372, the suffix-support polytope equals the next state intersected
with the reflected suffix sum. The induction supplies nonemptiness, and state
boundedness supplies a vertex. At any vertex, the active normals have full
ambient rank even in a lower-dimensional polytope: a nonzero null direction
would otherwise allow small feasible motions of both signs.

The normal list is fixed by the block, and enumerating its nonsingular bases
with precomputed inverses is therefore a genuine arithmetic recovery algorithm,
not an online optimization oracle hidden in notation. Its basis enumeration
and per-candidate checks fit the stated `2^{O(s^3)}` bound. The last suffix
forces the remaining aggregate to zero.

The denominator argument explicitly handles repeated divisions: each chosen
step adds only the encoding length of one parameter-bounded determinant to a
common denominator. There are only as many steps as local states. Rejected
candidates use those same bounded right-hand sides and fixed matrices. Hence
there is no exponential bit-length growth in the number of states. The sparse
normalization/default construction and separate dense output cost are also
consistent with the earlier recovery results.

### R2-S4-C5 — new five-product K4 construction (verified)

At lines 411–487, I independently formed the incidence matrix from the stated
arc order and checked `AC=0`. The nonuniform reference vector has exactly the
reported balance vector, with two supplies and two demands, and the aggregate
flow equals `v+C theta_bar` and satisfies all unit capacities.

The fixed observation on 02 in state 1 gives `theta^1_3=theta^1_1`; the two
fixed state-2 observations give `theta^2_3=0` and
`theta^2_1+theta^2_2=0`. Thus the displayed state vectors follow from actual
observed products and balances, not from extra hidden constraints.

For each state, only arc 01 has the changed deviation interval
`[-1/12,1/4]`; the other five intervals are `[-1/6,1/6]`. The residual
support bound follows from its 12 upper bound and 03 lower bound. Since the
second state contributes zero in direction `(1,1,1)`, the section inequality
is exactly `2p+q>=0`, or `2U+V>=1/2`.

The witness in the manuscript has the correct sum and all five observations.
Its six residual arc deviations agree with the displayed formula. For the
strict neighborhood `|p|,|q|<1/96`, the fourth deviation lies strictly between
`3/16` and `11/48`; all other deviations have the claimed bounds. The first
and sixth deviations may attain their limits on the boundary, which is
correctly allowed. Thus the entire nearby feasible side, including its
boundary, is established.

As an additional independent check, the same balances imply the globally valid
original-coordinate inequality

\[
2z_{12,1}+z_{13,1}+z_{02,1}+z_{23,2}+z_{01,2}
\ge x_{12}+x_{13}+x_{23}-\frac52+3y_1+\frac74y_2.
\]

Substituting the section constants gives exactly `2U+V>=1/2`. This is supporting
verification, not a required manuscript change or a claim that this particular
global inequality is itself facet-defining.

### R2-S4-C6 — section-to-facet transfer and old variant (verified)

At lines 374–409, a local two-dimensional interior of the coordinate section
forces every valid affine equation to restrict identically to that plane.
Consequently its two free-coordinate coefficients vanish. At the local boundary,
a nonconstant active inequality must exist in every finite description, and
feasibility in both tangent directions forces its normal to be proportional to
the displayed half-plane normal. The interior side fixes the sign. Applying
this argument to a relative facet description proves the actual facet-ratio
claim and its invariance under adding affine equations.

At lines 489–515, the older seven-product construction is also correct. The
line states have zero support in direction `(1,1,1)`, the stated witness sums
to the aggregate vector, and its residual scalar satisfies
`5/64<a<=1/8` throughout the stated neighborhood. The final explanation is
geometrically consistent: the symmetric residual support face is a point,
whereas the modified 01 bound makes it an edge and allows the extra line
state to be omitted.

## Independent executable evidence

Two standalone checks were written in `verification/reviewer2/stage04-round01/`.
Neither imports repository hull or oracle implementations.

1. `check_k4.py` constructs the graph incidence matrix and verifies all balances,
   scaled capacities, state sums, and observed products for 185 rational local
   witnesses in **each** K4 variant. It verifies the exact residual-support
   contradiction for 176 points on the infeasible side in each variant. It
   also symbolically checks the section reduction of the independent global
   inequality above. Results: `result.json`, all passed.
2. `check_rank_recovery.py` independently builds the rank-three normal,
   edge-direction, support-ray, dual-basis, and recovery-basis libraries. It finds
   12 signed normals, 7 primitive edge directions, 18 support rays, and 544
   recovery bases; every nonnegative dual multiplier is at most 2. It performs
   36 exact state recoveries, including families consisting entirely of
   singleton states. Results: `rank-result.json`, all passed.

Commands actually run:

```sh
/workspace/local-home/miniconda3/envs/minlp-notes/bin/python paper-network-simplex/verification/reviewer2/stage04-round01/check_k4.py
/workspace/local-home/miniconda3/envs/minlp-notes/bin/python paper-network-simplex/verification/reviewer2/stage04-round01/check_rank_recovery.py
```

## Review limitations

The general-rank arguments were checked mathematically; executable library
checks cover rank three, not every parameter value. The rational K4 grids
supplement the direct neighborhood proof and are not offered in place of it.
I did not independently certify novelty, retrieve every cited historical source,
or compile a private PDF. Later unwritten sections are outside this review.
