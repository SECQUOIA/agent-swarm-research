# Independent review: globally correlated cactus arc constraints

Date: 2026-09-05. Reviewer: `benders_property`. Status: PASS. The author added the requested explicit zero-flow and edgeless cases, and I verified the final wording.

Reviewed [the full candidate](potential-flow-global-correlation-arc-validation.md). The passive-state existence, orientation reversal, shifted-piece construction, and dense-degree abstract root algorithm were separately reviewed in the preceding application audits. This note checks what changes under one globally correlated parameter polytope.

For fixed nominations, bridge flows and effective cycle nominations are determined by conservation. This conclusion does not require independent parameter coordinates. The unique cycle circulation is determined by its own strictly increasing scalar balance H_C at the given global parameter vector. Thus, for rational a<=b,

    a<=q_C(theta)<=b  iff H_C(a,theta)<=0 and H_C(b,theta)>=0.

Both directions and equality cases are correct. Signed original arc orientations yield rational interval bounds after the already checked reversal and shift. Bridge bounds and inconsistent circulation intervals are direct checks. Clipping to [-B,B] is valid when q_C is a reference-edge flow.

Each displayed balance value is affine in the original global theta, including any parameter-independent constant. Intersecting all these inequalities with P therefore gives a rational polytope whose points are exactly the capacity-feasible physical scenarios. A rational LP feasible point is consequently an exact original scenario witness, even if its physical flow is irrational. There is no requirement to realize the cycles independently, because the same global theta satisfies all their equations by their unique-root definitions.

The robust signs are also correct: the lower capacity requires `max_P H_C(a)<=0`, and the upper capacity requires `min_P H_C(b)>=0`. A strictly wrong sign at a rational LP optimizer certifies a strictly violating scenario. No algebraic root evaluation is needed. Empty capacity intersections are infeasible; robust validation over the promised nonempty P fails if their corresponding constraints are impossible.

For a target arc, the scalar cycle balance remains piecewise polynomial with fixed rational breakpoints and affine coefficients in all coordinates of theta. The abstract root theorem allows unrestricted polytope dimension and arbitrary correlations. Restricting to P_cap changes only rational inequalities. It remains bounded, and the passivity and root-bracket promises hold on it. After testing nonemptiness, exact scalar extrema and rational optimizing vertices therefore follow with polynomial degree and bit bounds. Bridge extrema are fixed constants. No common algebraic field across cycles appears.

I requested one explicit edge-case sentence: if B=0, do not call the abstract theorem on the degenerate bracket [0,0]. All physical flows are zero; check capacities directly and return any rational feasible P point when needed. An edgeless connected graph is handled directly as well. This is already implicit in the imported application but should be visible in this standalone statement.

The permitted cycle-local linear-flow constraints also reduce to individual circulation intervals. General flow inequalities involving several circulations and coupled performance objectives do not follow from the displayed LP description. The note correctly keeps these separate from arbitrary correlation in parameter space.

No substantive defect was found. The capacity description itself is elementary scalar monotonicity and needs the planned comparison with prior coefficient-space formulations; this review makes no new priority claim.
