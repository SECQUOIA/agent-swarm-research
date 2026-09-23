# Exact arc capacities in continuous cactus resistance design

Date: 2026-09-05. Status: verified by two independent full mathematical audits. The inherited optimization mechanisms are credited, and direct publication priority remains subject to source comparison.

## Theorem

Fix rational balanced nominations on a connected simple cactus with quadratic passive laws and independent positive rational resistance intervals. Impose rational lower and upper bounds on every signed arc flow; absolute capacities are a special case. Then existence of a resistance design satisfying these bounds is decidable in polynomial bit time. If feasible, a rational resistance design satisfying all bounds exactly is computable in polynomial bit time.

For any rational positive-semidefinite quadratic objective of the entire flow vector and rational epsilon>0, a rational resistance scenario satisfying all bounds exactly and attaining objective at most epsilon above the constrained minimum is computable in polynomial time in input length and requested accuracy bits. There is no bound on the number of cactus cycles. The returned physical flow and potentials may be irrational.

No potential bounds or constraints coupling different cycle circulations are covered. More generally, the same theorem allows rational linear flow inequalities whose nonconstant part involves at most one cycle circulation. Such a constraint may also include fixed bridge flows.

## 1. Exact feasibility is interval intersection

The [reviewed flow-region theorem](../results/potential-flow-cactus-flow-region-and-optimization.md) writes

    x=x0+Zq,   l_C<=q_C<=u_C,

where x0 is rational, cycle supports are disjoint, and every l_C,u_C has a polynomial-size quadratic algebraic encoding. Both endpoints have computable rational resistance scenarios realizing them.

A bridge flow is fixed and rational, so its bounds can be checked directly. On a cycle, every signed flow is x_e=d_e+s_e q_C, with rational d_e and s_e in {-1,+1}. Its rational flow bounds yield rational lower and upper bounds on q_C. Intersect all such bounds, obtaining a rational interval [a_C,b_C], allowing infinite endpoints if some bounds are absent. A cycle-local linear inequality likewise reduces to a rational affine inequality in q_C; a zero coefficient is checked directly.

The constrained circulation interval is

    L_C=max(l_C,a_C),   U_C=min(u_C,b_C).

Comparing a quadratic algebraic number with a rational number, or comparing the two endpoint roots, is polynomial-time exact algebraic arithmetic. Thus emptiness, including strict separation versus equality, is decidable exactly. Global feasibility is equivalent to every cycle interval being nonempty and every bridge bound being satisfied.

## 2. Every new endpoint has a rational resistance witness

If L_C or U_C equals an original attainable endpoint l_C or u_C, use its existing rational endpoint resistance profile. Ties can be resolved this way.

Otherwise the new endpoint is the rational clipping value a_C or b_C. For any rational attainable circulation q, the scalar profiles from the [convex-design theorem](../results/potential-flow-cactus-convex-design.md) give rational values

    H_min(q)<=0<=H_max(q).

If the difference is positive, interpolate their resistance profiles with the rational coefficient

    lambda=-H_min(q)/(H_max(q)-H_min(q)).

The cycle equation is linear in the resistances at fixed q, so this realizes q exactly. If both profile values vanish, either realizes q. All output resistances remain inside their original intervals and have polynomial rational encoding length.

Choose one constrained endpoint per cycle and combine these independent profiles. This gives an exactly capacity-feasible rational resistance scenario, including singleton constrained intervals. Irrational singleton circulations cause no problem: if a rational clipping endpoint does not define them, they are original attainable endpoints with rational resistance witnesses.

## 3. Constrained convex optimization with exact capacity recovery

Run the [reviewed rational surrogate-box algorithm](../results/potential-flow-cactus-convex-design.md) on [L_C,U_C] instead of [l_C,u_C]. These endpoints still have polynomial-size degree-at-most-two algebraic encodings and rational resistance witnesses.

Retained rational inner intervals lie inside the constrained circulation interval. Rational circulation recovery therefore satisfies every flow bound exactly. A narrow interval is frozen at a rational upper enclosure of L_C only for the numerical surrogate; its final resistance scenario is the stored profile realizing the exact constrained endpoint L_C. Thus the final physical flow also satisfies every bound exactly, even when the frozen surrogate temporarily lies outside it.

The original proximity and error estimates are unchanged. With B=sum_v |b_v|, m edges,

    L=1+max_i (|d_i|+(B+1)sum_j |Q_ij|),
    eta=min(1,epsilon/(16mL)),

projection to the surrogate changes the flow by at most 2m eta in l1 norm, and final recovery changes it by at most m eta. Convex optimization on the rational surrogate box to epsilon/2 gives total loss at most

    3mL eta+epsilon/2<=11epsilon/16<epsilon.

The B=0 and edgeless cases are checked directly before dividing by m. Empty constrained intervals are rejected first. No capacity relaxation or feasibility margin is needed because final recovery uses the exact constrained intervals and their exact physical witnesses.

## Scope and significance

The earlier design theorem excluded arbitrary additional exact constraints; it did not prove that every such constraint creates an arithmetic obstruction. Individual flow bounds preserve the independent interval structure, which is the reason this extension works. A constraint coupling two or more cycles can instead compare independent algebraic quantities and is outside this proof. Potential bounds likewise do not generally become independent circulation intervals.

The [finite-resistance unit-capacity construction](../results/potential-flow-discrete-flow-realization.md) is NP-complete already on one cycle with fixed nominations. The theorem here gives a direct continuous-interval versus finite-choice separation for existence and convex performance design under exact capacities. Its mechanism is elementary interval clipping followed by the established cactus algorithm, so priority claims should remain modest and source-qualified.

## Verification and source scope

Both [the first full audit](../notes/review-potential-flow-cactus-capacitated-convex-design.md) and [the second full audit](../notes/review-potential-flow-cactus-capacitated-convex-design-second.md) passed. They checked exact interval clipping, rational endpoint witnesses, irrational singleton cases, and final exact capacity satisfaction after frozen-coordinate recovery.

The extension is interval clipping applied to the reviewed cactus design theorem. It is preserved as a useful exact-feasibility boundary, with no new general optimization mechanism claimed. The stronger [cycle-polytope theorem](potential-flow-cycle-polytope-resistance-design.md) also permits linear resistance correlations within each cycle.

## Exact recovery checks

[`cactus_capacity_recovery_checks.py`](../code/potential_flow_mpd/cactus_capacity_recovery_checks.py) passed 403 exact rational cases: 229 feasible clipped intervals and 174 infeasible ones. It checked 227 rational interior recoveries and two frozen endpoint recoveries, including an irrational singleton physical interval, a rational singleton imposed by capacities, and an interval of resistance width `2^-100`. Final capacity satisfaction was verified by exact signs of the strictly increasing cycle equation at each rational capacity boundary, without numerical evaluation of the irrational physical root. The coupled-objective optimization and error estimates are inherited from the separately checked design algorithm.
