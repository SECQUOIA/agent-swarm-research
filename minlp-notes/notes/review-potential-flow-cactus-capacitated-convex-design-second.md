# Second independent audit of exact capacities in cactus convex design

Date: 2026-09-05. Reviewer: `spatial_sdp_review`.

**Verdict: PASS.** The [candidate](potential-flow-cactus-capacitated-convex-design.md) correctly extends continuous interval resistance design to exact signed arc capacities and rational linear constraints involving at most one cycle circulation. The conclusion includes polynomial-bit rational resistance output, additive convex quadratic minimization, and exact final capacity satisfaction at arbitrary cactus rank.

## Exact feasible intervals and witnesses

The reviewed flow-region representation has independent cycle coordinates and disjoint cycle supports. A rational signed arc bound therefore gives a rational scalar bound on its cycle coordinate. A cycle-local linear inequality gives the same after summing its rational coefficients; if the resulting coefficient is zero, its constant inequality must be checked directly. Bridge flows are fixed rational numbers. These reductions preserve weak inequalities, including equality cases.

Intersecting the original attainable interval with the resulting rational interval gives exactly `[max(l,a),min(u,b)]`. Its endpoints have degree at most two and polynomial-size algebraic encodings. Exact comparison of a bounded number of quadratic algebraic numbers is polynomial-time, even when the two original endpoint profiles generate different quadratic fields. No sum across all cycles is needed.

Every constrained endpoint has a rational resistance witness. An endpoint equal to an original attainable endpoint uses the previously computed profile. Otherwise it is a rational clipping value q. At fixed q, the cycle equation is rational and linear in resistance, so the displayed interpolation between profiles with values `H_min(q)<=0<=H_max(q)` realizes q exactly. The coefficient is in `[0,1]`; a zero denominator means both values vanish. Rational arithmetic and output sizes are polynomial in the encoded data. In particular, small interpolation denominators affect numerical conditioning but not polynomial bit size.

The singleton case does not introduce an arithmetic gap. A singleton defined by a rational clipping value is rational and uses interpolation. An irrational singleton must be an original endpoint and uses its rational endpoint profile. Independence of cycles permits combining all these witnesses. Conservation and cycle consistency then give the physical state globally.

## Convex minimization and exact capacities

The [previous second audit](review-potential-flow-cactus-convex-design-second.md) establishes the surrogate-box optimizer and its polynomial-bit convex optimization hypotheses. Replacing the original interval endpoints by the constrained endpoints preserves all properties used there: degree at most two, polynomial-bit enclosures, independent coordinates, and rational endpoint resistance witnesses.

A retained interval is contained in the exact constrained interval, so every recovered retained rational coordinate satisfies its capacities. A frozen surrogate need not satisfy capacities itself. Its final profile realizes the exact constrained lower endpoint, which does satisfy them. The proof correctly makes the guarantee about the returned physical state.

The original proximity bounds remain valid: projection from a true feasible flow to the surrogate costs at most `2m eta` in l1 norm, and recovery costs at most `m eta`. Each surrogate flow is within eta on each affected edge of a jointly physical flow, so its magnitude is at most `B+1`. The displayed gradient bound therefore controls both comparisons, including cross-cycle quadratic objective terms. The final error is at most `3mL eta+epsilon/2<=11epsilon/16`. This holds for both branches of the minimum defining eta. Empty intervals and constant-flow cases are handled before optimization.

The theorem does not cover constraints coupling different cycle coordinates or potential bounds. The older exclusion of arbitrary exact constraints is consistent with this new structured extension.

## Verification

Independently reran `code/potential_flow_mpd/cactus_capacity_recovery_checks.py` with the project Python interpreter. It passed 403 exact cases: 229 feasible, 174 infeasible, 227 retained rational recoveries, and two frozen endpoint recoveries. These include rational and irrational singletons and a very narrow resistance interval. The full algorithmic guarantee rests on the proof above and the previously reviewed convex optimizer, not on finite diagnostics.

No correction to the candidate is required.
