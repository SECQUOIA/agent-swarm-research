# Independent review: exact capacities in continuous cactus design

Date: 2026-09-05. Reviewer: `benders_property`. Status: PASS for the stated arc-capacity and cycle-local linear-constraint scope.

Reviewed [the extension candidate](potential-flow-cactus-capacitated-convex-design.md) against the promoted [continuous convex-design theorem](../results/potential-flow-cactus-convex-design.md), which I previously audited in full. This review checks the new exact-feasibility claims and the changes needed in that algorithm. It does not assign publication priority to interval clipping or convex quadratic optimization.

## Exact feasibility and endpoint representation

In the cactus representation `x=x0+Zq`, each nonbridge edge has coefficient +1 or -1 in exactly one cycle coordinate. Thus each signed arc bound becomes a rational lower or upper bound on that coordinate, with the inequality reversed when appropriate. A bridge bound is a rational constant test. A rational linear constraint involving only one nonconstant cycle coordinate has precisely the same reduction; a zero coefficient is checked as a constant condition.

Each constrained interval is the intersection of the original attainable interval with these rational bounds. All its finite endpoints are either rational clipping values or the original degree-at-most-two algebraic roots. Exact comparisons are polynomial in their rational coefficient encodings; comparing two independently encoded quadratic roots does not require a field containing every cycle root. Equality is handled exactly. Independence of cycle coordinates makes the conjunction of these interval tests sufficient for global feasibility.

## Rational physical witnesses, including singletons

An original endpoint has the rational resistance profile supplied by the scalar envelope construction. A new endpoint is rational. At such a target q, every signed edge flow is rational, so both cycle-envelope values and their difference are rational of polynomial bit length. The signs `H_min(q)<=0<=H_max(q)` follow from attainability. The displayed interpolation coefficient belongs to [0,1] and enforces cycle balance exactly. Its arithmetic has polynomial bit complexity; no numerical residual is accepted as a feasibility certificate. If the difference vanishes, both envelope values vanish and an endpoint profile works directly.

For a rational singleton introduced by clipping, the same interpolation supplies an exact witness. An irrational singleton cannot be introduced solely by rational clipping: its coincident constrained endpoints must equal original attainable endpoints, for which the stored rational profiles suffice. In particular, rational resistance output never requires rational physical flow. This resolves the narrow-boundary case without a feasibility margin.

Combining independently selected cycle profiles and arbitrary admissible bridge resistances gives a physical network state satisfying all capacities. The usual cycle-space characterization of potential consistency suffices; cycles sharing an articulation vertex introduce no additional equation.

## Constrained optimization and recovery

Replacing the original interval endpoints by the clipped endpoints preserves every input property of the reviewed surrogate-box algorithm: compact independent intervals, polynomial-size quadratic endpoint encodings, and polynomial-size rational resistance witnesses at their endpoints.

Retained inner intervals are contained in the constrained intervals, so rational interpolation realizes their targets with exact capacity satisfaction. A frozen surrogate coordinate may temporarily violate capacity, but its final recovered physical coordinate is the exact constrained lower endpoint. It therefore satisfies all original bounds. That final endpoint is within eta of its rational surrogate, including irrational singleton intervals.

Projection of a feasible physical flow to the rational surrogate incurs at most `2*m*eta` in l1 distance; recovery adds at most `m*eta`. Every surrogate flow is within eta per edge of a feasible flow obtained by substituting the frozen endpoints, and consequently lies in the expanded magnitude box B+1. The same rational gradient bound L applies. The total objective loss is

    2*m*L*eta + epsilon/2 + m*L*eta <= 11*epsilon/16 < epsilon.

Rational convex optimization is on the surrogate box only. It requires no exact feasible rational circulation in an irrational singleton and no common algebraic field for all cycles. The imported polynomial-bit optimizer and rational interpolation retain polynomial dependence on the input encoding and requested accuracy bits. Empty intersections, fixed coordinates, zero nominations, and edgeless graphs are correctly handled separately.

The extension does not cover general constraints coupling distinct cycles, potential bounds, or finite resistance sets. No inference of polynomial exact scalar objective comparison is made.

## Reproducible check

I independently reran `code/potential_flow_mpd/cactus_capacity_recovery_checks.py`. It passed 403 exact cases: 229 feasible clipped intervals, 174 infeasible ones, 227 retained rational recoveries, and two frozen endpoint recoveries. The test checks capacity satisfaction through exact cycle-equation signs, including rational and irrational singleton cases. The correctness of general coupled convex optimization continues to rest on the reviewed proof, not these recovery checks.

No substantive or editorial correction was required.
