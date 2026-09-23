# Convex flow-performance design on a cactus with continuous resistance intervals

Date: 2026-09-05. Status: verified by two full mathematical audits. The standard optimization mechanisms are credited below; mathematical verification does not establish publication priority.

## Theorem

Fix rational balanced nominations on a connected simple cactus with quadratic passive laws and independent positive rational resistance intervals. Let

    f(x)=1/2 x^T Qx+d^T x+k,

where Q is rational positive semidefinite and all other coefficients are rational. For every rational epsilon>0, a rational resistance scenario whose physical flow has objective within epsilon of the minimum can be computed in polynomial time in the input length and requested accuracy bits. The cactus may have arbitrarily many cycles.

No extra exact flow or potential feasibility constraints are imposed. The statement is an additive performance guarantee, not an exact scalar threshold or exact boundary-feasibility algorithm. Physical flows in the returned rational scenario may be irrational. In contrast, minimizing a convex deviation or maximum-load objective over finite resistance choices is NP-hard already on one cycle, as recorded in the [inverse-design boundary](../notes/potential-flow-discrete-flow-realization.md).

## 1. Independent cycle intervals

Use the [cactus flow-region construction](../notes/potential-flow-cactus-flow-region-and-optimization.md). The attainable flow set under continuous resistance intervals is

    x=x0+Zq,   l_C<=q_C<=u_C,

where x0 is rational, cycle vectors have disjoint edge supports and entries in {0,+1,-1}, and each endpoint l_C,u_C has a polynomial-size quadratic algebraic encoding. An endpoint resistance vector realizing either bound is computable exactly.

Write B=sum_v |b_v|. Every physical flow has magnitude at most B. Handle an edgeless graph or B=0 directly. Let m be the number of edges and choose the rational gradient bound

    L=1+max_i (|d_i|+(B+1)sum_j |Q_ij|).

Then |f(x)-f(y)|<=L||x-y||_1 on the expanded flow box with |x_e|,|y_e|<=B+1.

## 2. A rational surrogate box with controlled recovery error

Let eta=min(1,epsilon/(16mL)). Compute rational enclosures

    l_C^-<=l_C<=l_C^+,   u_C^-<=u_C<=u_C^+

of width at most eta. If l_C^+<=u_C^-, retain the rational inner interval [l_C^+,u_C^-]. Call this a retained coordinate. Every true feasible coordinate projects to this interval with error at most eta.

Otherwise freeze its surrogate coordinate at the rational number l_C^+. The true interval then has width less than 2eta. Any point of that interval differs from the frozen surrogate by at most 2eta. Store the rational resistance scenario realizing the exact lower endpoint l_C for later recovery; its physical circulation differs from the frozen surrogate by at most eta.

The resulting surrogate flow box is rational. Every true feasible flow maps into it with l1 error at most 2m eta. Each surrogate flow has magnitude at most B+1: retained coordinates are physically attainable and frozen coordinates differ from an attainable endpoint by at most eta. Thus its optimum is no larger than the true optimum plus 2mL eta.

## 3. Polynomial-bit convex optimization on the surrogate box

The function f(x0+Zq) is a rational convex quadratic on a rational box. Compute a rational point within epsilon/2 of its minimum using standard polynomial-bit convex optimization. One fully explicit route using the already-read [Dadush thesis](https://homepages.cwi.nl/~dadush/papers/dadush-thesis.pdf), Theorem 2.5.9, is as follows.

Discard fixed coordinates and affinely transform every remaining interval to [-1,1]. Rational LDL decomposition writes the positive-semidefinite quadratic term as a sum of nonnegative rational multiples of squares of rational linear forms. Bound each form on the cube by a rational number R. Replace its square outside [-R,R] by its tangent-affine continuation. This produces a globally convex, globally Lipschitz, piecewise-quadratic function that agrees with the objective throughout the cube. Its exact rational value and subgradient oracle, rational Lipschitz upper bound, and encoding lengths are polynomial. The cited bounded convex-optimization theorem therefore gives a rational epsilon/2-optimal point in polynomial bit time. A zero-dimensional box is evaluated directly.

This step uses established convex optimization. No fixed number of cycle variables is required.

## 4. Exact rational resistance recovery

For a retained coordinate q_C, all cycle-edge flows q_C+d_e are rational and belong to the true attainable interval. Form the endpoint profiles attaining H_min(q_C) and H_max(q_C), as in the scalar cycle construction. Their values satisfy

    H_min(q_C)<=0<=H_max(q_C).

If their difference is positive, let

    lambda=-H_min(q_C)/(H_max(q_C)-H_min(q_C)).

Interpolate the two endpoint resistance vectors with this rational lambda. Cycle pressure balance is linear in the resistances for the fixed target flow, so the interpolated vector realizes q_C exactly. It lies in every resistance interval and has polynomial rational bit size. If both values are zero, either endpoint profile realizes q_C.

For a frozen coordinate, use its stored endpoint scenario. Use arbitrary allowed endpoints on bridges. Block independence gives a globally valid rational resistance scenario. Only frozen cycles differ from their surrogate flows, by at most eta per edge, so physical recovery adds at most mL eta to the objective.

The total performance loss is at most

    2mL eta + epsilon/2 + mL eta
      <=3epsilon/16+epsilon/2<epsilon.

One can also approximate the returned physical objective by separately enclosing its quadratic cycle roots and evaluating f with the same explicit gradient bound. A common algebraic field across cycles is unnecessary.

## Why this is a separate design statement

The actual finite resistance scenario set can have holes inside this convex flow region. The exact target-realization counterexample has an interval-feasible unit target but no finite scenario attaining it. Continuous interpolation in Section 4 is therefore essential and is not valid for finite sets.

Exact added operating constraints are excluded. A constraint supported only at an irrational boundary can reintroduce exact radical comparisons or obstruct a rational surrogate feasible point. Such constraints would require a separate feasibility-margin or arithmetic analysis, not the additive argument above.

## Verification and source scope

Both [the first full audit](../notes/review-potential-flow-cactus-convex-design.md) and [the second full audit](../notes/review-potential-flow-cactus-convex-design-second.md) passed. They checked narrow and singleton intervals, the rational surrogate bounds, the cited convex-optimization theorem and its bit model, exact resistance recovery, and the full error budget.

Convex quadratic minimization is established, and the geometry is the independent-cycle product. The combined statement supplies rational original resistance scenarios despite independent algebraic interval bounds. The [cactus geometry source assessment](../notes/potential-flow-cactus-flow-region-and-optimization-novelty.md) records antecedents and unresolved older circuit sources. A focused direct-priority comparison for this design formulation remains open.

## Reproducible recovery checks

[`cactus_convex_design_checks.py`](../code/potential_flow_mpd/cactus_convex_design_checks.py) passed 12 coupled convex quadratic examples with one to four cycle coordinates. It used exact rational root brackets and resistance interpolation, verified 24 rational target-cycle recoveries exactly, and exercised six narrow cycles with resistance widths `2^-80`. All recovered resistances satisfied their original intervals exactly. The largest observed objective loss against a numerical convex reference was below `1.61e-6` for requested error `1e-3`; the largest returned numerator-plus-denominator encoding was 172 bits. These reference comparisons are numerical evidence, while the interval and interpolation identities are exact checks. The script is not a certified implementation of the general convex-optimization oracle theorem.
