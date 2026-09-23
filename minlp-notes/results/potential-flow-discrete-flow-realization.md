# Exact flow realization and existential capacity design with finite resistances

Date: 2026-09-05. Status: verified by two full mathematical audits. The standard optimization mechanisms are credited below; mathematical verification does not establish publication priority.

## Results

Under common quadratic passive laws, deciding whether an explicitly specified rational flow can be realized by independent finite resistance choices is NP-complete. Hardness holds on a single simple cycle of maximum degree two, with fixed source/sink nominations (2,-2), prescribed flow one on every arc of a directed acyclic orientation, positive integer resistances, and only two options on each uncertain edge.

The same construction proves NP-completeness of existential resistance selection satisfying unit arc capacities on the fixed-nomination single-cycle class. In contrast, robust capacity validation on this class is polynomial by the reviewed finite-resistance single-arc algorithm. These are different quantifiers: existence of a feasible design versus capacity satisfaction for every scenario.

For independent continuous resistance intervals and any graph, realization of a specified rational flow is rational linear feasibility and is polynomial. Cactus flow-box geometry describes the interval region and the convex hull of finite scenarios; it does not imply finite-scenario membership tractability.

## 1. Linear feasibility when the target flow is fixed

Given rational target flow x_bar, first check A x_bar=b. Its quadratic drop coefficient t_e=x_bar_e|x_bar_e| is rational. With resistance intervals, physical realization asks for

    A^T pi=diag(t) beta,
    beta_lower<=beta<=beta_upper.

Fix one potential reference in each connected component. These are rational linear equalities and inequalities, so feasibility is decidable in polynomial bit time. No cycle-rank bound is required. Zero target flows simply impose zero potential difference on their edges.

For finite resistance sets, guess one input option index per edge. Once selected, the edge drops are rational and checking whether they are potential differences is rational linear algebra. Thus finite-set realization belongs to NP on arbitrary graphs. The certificate contains resistance choices; no irrational physical-state certificate is needed because the prescribed flow is rational.

## 2. A one-cycle Subset-Sum construction

Take positive integers a_1,...,a_n,K, let S=sum a_i, and preprocess trivial cases and n<2. Build two directed source-to-sink paths: a long path of n edges and one direct arc. This is a directed acyclic orientation of a simple cycle when n>=2. Set source nomination 2, sink nomination -2, and all other nominations zero.

Prescribe flow one on every arc. Long-path edge i has the options

    beta_i in {1,1+a_i},

and the direct arc has fixed resistance D=n+K. The target flow is conserved. Its long-path pressure drop is

    theta=n+sum_i a_i sigma_i,

while the direct drop is D. The target is physical exactly when theta=D, equivalently when a subset sums to K.

All resistances are positive integers. The graph has n+1 vertices, n+1 edges, global cycle rank one, and maximum degree two. Only the two fixed nominations are nonzero, and the target flow is the all-one vector. Fixed preprocessing outputs can use a two-edge long path and a direct arc: options {1,2} on both long edges and direct resistance 3 give a yes instance; options {1,3} and direct resistance 3 give a no instance. They retain the same simple triangle, target flow, and nominations.

This proves NP-hardness, and the preceding certificate proves NP-completeness.

## 3. Unit capacities force the same target flow

For any positive resistance choice in this graph, let p be the long-path flow and z the direct flow. All internal nominations vanish, so every long edge carries p. Conservation gives p+z=2. Both are strictly positive: the source-to-sink potential difference is common to both passive paths, and their common direction must carry the positive total demand.

Give every arc capacity one. Then p<=1 and z<=1 force p=z=1. Conversely the target flow satisfies all capacities. Thus existence of a capacity-feasible resistance choice is exactly the target-realization problem. The same conclusion holds for absolute capacities |x_e|<=1 because every physical flow is positive in this construction.

Membership for the broader fixed-nomination single-cycle capacity-design class follows by guessing resistance options and evaluating its scalar piecewise-quadratic cycle root exactly, then comparing each flow with its rational capacity. Hence the restricted existential design problem is NP-complete. This is not a claim about NP membership of arbitrary-rank nonlinear capacity design.

## 4. A precision gap and convex target matching

The physical long-path flow is

    p=2sqrt(D)/(sqrt(theta)+sqrt(D)),   z=2-p.

Consequently

    |p-1|=|D-theta|/(sqrt(D)+sqrt(theta))^2.

If no exact target subset exists, the numerator is at least one. With M=n+S+K, both D and theta are at most M, so

    |p-1|>=1/(4M).

Thus the minimum attainable maximum arc load is one in yes instances and at least 1+1/(4M) in no instances. The same gap holds for minimizing the maximum deviation from the all-one target, whose yes optimum is zero. These are convex functions of the flow vector, but their minimization over the finite scenario set is NP-hard. Polynomial dependence on input size and requested accuracy bits would decide Subset-Sum.

This is a weak, precision-dependent obstruction with fixed small nominations and unit target/capacities. No strong hardness, fixed relative-error hardness, or fixed absolute-error hardness under these normalizations is inferred.

## 5. Why convex-hull replacement changes existential questions

After replacing the long-edge sets by intervals [1,1+a_i], their total resistance ranges over [n,n+S]. Whenever 0<=K<=S, the direct resistance n+K lies in this interval. Thus every nontrivial source instance has an interval-resistance design realizing the target, including no Subset-Sum instances.

The target consequently belongs to the interval flow region and to the finite-scenario convex hull, while it may belong to no original finite scenario. There is no contradiction with endpoint worst-case theorems: containment of every scenario in a convex capacity set is preserved by convexification, whereas intersection with that set is not.

The [cactus flow-region investigation](../notes/potential-flow-cactus-flow-region-and-optimization.md) must therefore label its polynomial membership claim as interval-region or finite-convex-hull membership. Exact finite-scenario membership is a separate inverse-design task.

## Verification and source scope

Both [the first full audit](../notes/review-potential-flow-discrete-flow-realization.md) and [the second full audit](../notes/review-potential-flow-discrete-flow-realization-second.md) passed. They checked the rational certificate, simple-cycle construction, capacity quantifiers, precision gap, and interval relaxation. The first reviewer originated the finite-membership observation during an earlier geometry audit; the second review independently checked the resulting proof.

The reduction uses the classical Subset-Sum mechanism of discrete linear feasibility. Its role is the exact output-task and quantifier boundary beside the positive cactus geometry. A focused comparison with prescribed-flow inverse design and discrete pipe sizing remains open; no broad priority claim is made.

## Reproducible checks

[`discrete_flow_realization_checks.py`](../code/potential_flow_mpd/discrete_flow_realization_checks.py) passed 1,300 resistance scenarios over 34 instances at 80-digit precision. It checked cycle/DAG topology, exact all-one target conservation, exact subset/drop consistency, physical positive path flows, the deviation identity and gap, and unit-capacity forcing. It included 44 exact target choices and seven instances whose interval relaxation is feasible although no finite scenario realizes the target.
