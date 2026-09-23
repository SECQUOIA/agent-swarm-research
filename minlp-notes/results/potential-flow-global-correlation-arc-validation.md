# Exact cactus arc constraints under global parameter correlations

Date: 2026-09-05. Status: verified by two independent full mathematical audits, with a completed bounded source assessment. Established capacity linearization and convex Max-Cut mechanisms are credited; publication priority remains qualified.

## Model and conclusions

Fix rational balanced nominations on a connected simple cactus. Let one global parameter vector theta belong to a nonempty bounded rational polytope P. Every edge law g_e(x;theta) is continuous, strictly increasing, zero at x=0, and piecewise polynomial in flow with fixed rational breakpoints and densely encoded rational coefficients affine in theta. These passivity properties hold for every theta in P as promises. There may be arbitrary correlations between different cycles. Scalar quadratic resistances constrained by any bounded positive rational polytope are included.

Then exact feasibility of rational signed arc capacities is one rational linear feasibility problem. If feasible, it returns a rational original parameter scenario satisfying all capacities exactly. Robust satisfaction of all capacities over P is decided by rational linear optimization.

Every individual signed arc extremum is computable exactly, with a rational optimizing parameter scenario and an algebraic extremal flow, using the [reviewed monotone polynomial-root theorem](../notes/monotone-polynomial-root-polytope-optimization.md). This remains true when the parameter domain is restricted to scenarios satisfying any other specified rational arc capacities.

No independence between cycle parameters is needed. That independence was needed for an affine-box flow region and optimization of coupled performance functions. The present result does not claim those properties under global correlations. No additional potential bounds or uncertain nominations are included.

## 1. Convert all arc bounds to affine parameter inequalities

Fixed nominations determine every bridge flow and the effective nominations of each cycle. The existence, uniqueness, and uniform flow-bound arguments in the [polynomial-law application](../notes/potential-flow-correlated-polynomial-cycle-design.md) do not require independence of parameter coordinates: for every fixed theta the passive state exists and |x_e|<=B=sum_v |b_v|.

Orient each cycle consistently. Its edge flows are q_C+d_e with rational offsets; reversed input edges use the law -g_e(-x;theta). Its circulation is the unique zero of

    H_C(q,theta)=sum_(e in C) g_e(q+d_e;theta),

which is continuous and strictly increasing in q. Rational signed arc bounds become a rational interval a_C<=q_C<=b_C after accounting for orientation and offsets. Check bridge bounds directly and reject any interval with a_C>b_C. One may clip every interval to [-B,B] after choosing q_C to be a reference edge flow.

For every fixed theta, strict monotonicity gives the exact equivalence

    a_C<=q_C(theta)<=b_C
      iff H_C(a_C,theta)<=0 and H_C(b_C,theta)>=0.

At rational a_C,b_C, these two expressions are rational affine functions of theta. Thus all physical arc capacities define the rational polytope

    P_cap={theta in P:
           H_C(a_C,theta)<=0<=H_C(b_C,theta) for every cycle C}.

Feasibility and a rational feasible point are obtained by one LP. The inequalities are equivalent to the physical capacities, so the returned rational scenario is exactly feasible even when some physical circulations are irrational. No algebraic state certificate or separate cycle interpolation is needed.

The same argument covers a rational linear flow inequality whose nonconstant part involves at most one cycle. Multiple cycles may be coupled through P, but not through an additional flow inequality in this stated capacity formulation.

## 2. Robust validation

Robust capacity satisfaction over P is equivalent to

    max_(theta in P) H_C(a_C,theta)<=0,
    min_(theta in P) H_C(b_C,theta)>=0

for every cycle, together with the bridge checks. These are rational LPs. Strict violations and equality are distinguished exactly. A violating LP optimizer is a rational original parameter scenario; monotonicity certifies its physical violation without evaluating an irrational cycle root.

## 3. Exact individual arc optimization, including capacity filters

For a target cycle, H_C(q,theta) has a fixed rational piece partition after shifting edge breakpoints. Its coefficients are affine in the entire global theta vector and have polynomial encoding length. It is strictly increasing for every theta in P, and [-B,B] brackets its unique root. The abstract monotone-root theorem therefore computes both extremal roots over P exactly, returning rational optimizing vertices of P.

If other capacities filter scenarios, first construct P_cap. It is a bounded rational polytope, and the same passivity and root-bracket promises hold on it. Reject it if empty; otherwise apply the same theorem to P_cap. Every returned original parameter scenario satisfies all filtering capacities exactly. Signed target-flow shifts and reversed orientations are handled by rational affine transformations of q_C. Bridge extrema are fixed and rational.

Handle B=0 before invoking the nontrivial-bracket theorem: every physical flow is zero, so check the capacities directly and return any rational feasible point of P when they hold. An edgeless graph is handled in the same way. Polynomial bit complexity includes the number of coefficients, constraints, pieces, and the dense polynomial degree. The algorithm does not form a common algebraic field across cycles, because each target extremum is computed from only its scalar cycle equation.

## Limits and comparison

Global correlations can make the flow image nonconvex, as shown by the [two-cycle shared-resistance example](../notes/potential-flow-cross-cycle-correlation-obstruction.md). This does not obstruct the affine parameter description of individual capacity bounds. In contrast, a coupled objective involving flows from several cycles need not reduce to one scalar monotone equation or one LP.

The [global-correlation total-flow construction](../notes/potential-flow-global-correlation-total-flow-hardness.md) proves a strong hardness boundary for that coupled objective, even with the common quadratic law. Both mechanisms require source credit: capacity linearization follows directly from scalar monotonicity, while the hardness construction uses classical convex Max-Cut maximization.

## Verification

Both [the first full audit](../notes/review-potential-flow-global-correlation-arc-validation.md) and [the second full audit](../notes/review-potential-flow-global-correlation-arc-validation-second.md) passed. They checked all inequality directions, global correlations, exact capacity filters, the zero-flow case, and use of the dense piecewise root theorem. The [paired source assessment](../notes/potential-flow-global-correlation-novelty.md) explicitly identifies the prior quadratic capacity mechanism and distinguishes it from the exact optimizing-profile arithmetic.

## Direct source credit

[Aßmann, Liers, Stingl, and Vera](https://arxiv.org/pdf/1808.10241), Proposition 4.9 and Lemma 4.10 on printed pages 20–21, already give the quadratic single-cycle equation and express a circulation interval by two affine inequalities in pressure-loss coefficients. Proposition 4.11 explicitly preserves polyhedral uncertainty after those restrictions. These primary passages were read directly. Combining those constraints across cactus blocks gives the quadratic global-capacity LP as a straightforward extension. The broader dense polynomial-law scope and exact algebraic optimizing-profile output use the separate root theorem; the capacity linearization itself is not claimed as new.
