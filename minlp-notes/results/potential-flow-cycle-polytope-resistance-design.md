# Correlated resistances within cactus cycles: LP thresholds and convex design

Date: 2026-09-05. Status: verified by two independent full mathematical audits. The inherited optimization mechanisms are credited, and direct publication priority remains subject to source comparison.

## Model and results

Fix rational balanced nominations on a connected simple cactus with quadratic laws. For each cycle C, its entire resistance vector belongs to a nonempty rational polytope P_C given by linear inequalities. Include explicit rational bounds 0<beta_lower<=beta<=beta_upper, so these polytopes are compact and uniformly positive. Different cycles have independent polytopes; arbitrary correlations among resistance coordinates of one cycle are permitted. Bridges may have independent positive intervals.

Impose rational signed arc-flow bounds, or more generally rational linear flow constraints whose nonconstant part involves only one cycle. Then:

1. Capacity feasibility is decidable in polynomial bit time, and every feasible instance has a polynomial-time computable rational resistance witness satisfying every capacity exactly.
2. Every individual arc extremum can be compared with a rational threshold exactly in polynomial time. A rational resistance scenario within any requested additive error of an arc extremum is computable in polynomial bit time.
3. A rational resistance scenario satisfying all capacities exactly and minimizing any rational positive-semidefinite quadratic flow objective to additive error epsilon is computable in polynomial time in input length and accuracy bits.

There is no bound on cycle size or the number of cycles. No correlation between different cycle polytopes, variable nominations, or additional potential constraints is included. Section 6 additionally proves exact single-cycle algebraic extrema and rational optimizing-profile recovery, using an explicit separation bound. Exact sums of independent cycle values remain a separate arithmetic question.

## 1. A scalar monotone equation with an LP threshold oracle

Orient a cycle consistently and choose its reference circulation q to equal one selected oriented edge flow. Conservation writes every cycle flow as q+d_e, with rational offsets and the selected offset zero. Let B=sum_v |b_v|. Passive flow acyclicity gives |q|<=B for every scenario.

For beta in P_C define

    H(q,beta)=sum_e beta_e(q+d_e)|q+d_e|.

For fixed beta this is continuous and strictly increasing, has a unique root q(beta), and depends continuously on beta. Its root image over the connected compact polytope P_C is therefore a compact interval [l_C,u_C]. At rational q, H(q,beta) is a rational linear function of beta.

Consequently

    u_C>=q  iff  min_{beta in P_C} H(q,beta)<=0,
    l_C<=q  iff  max_{beta in P_C} H(q,beta)>=0.

Each right-hand side is a rational LP decision, including equality. The corresponding strict inequalities are decided by changing the final comparison with zero. Nonemptiness of P_C itself is checked first by LP.

This also proves exact weak/strict rational threshold tests for all signed cycle-edge extrema, after shifting by d_e and reversing orientation when necessary. Bridge flows are fixed and rational.

The original physical cycle roots need not be computed for these threshold tests. LP coefficients have polynomial bit length at every polynomial-bit rational test point.

## 2. Rational realization at a rational target

A rational circulation q is attainable exactly when

    min_P H(q,beta)<=0<=max_P H(q,beta).

LP supplies rational minimizer beta^- and maximizer beta^+. If their values differ, interpolate them with coefficient

    lambda=-H(q,beta^-)/(H(q,beta^+)-H(q,beta^-)).

This rational convex combination lies in P and has H(q,beta)=0. If both values are zero, either LP solution realizes q. Rational LP solutions, interpolation coefficients, and returned resistances have polynomial bit length.

## 3. Exact capacities and a rational feasible scenario

Cycle-local flow bounds reduce to a rational circulation interval [a,b]. Intersect it with [-B,B] first; this does not remove any physical scenario. If a>b reject. The intersection with [l_C,u_C] is nonempty exactly when

    min_P H(a,beta)<=0,  max_P H(b,beta)>=0.

Thus feasibility requires two LP value comparisons per cycle, plus direct bridge checks.

To construct a witness, obtain any rational beta0 in P by LP. Its scalar physical root q0 has a degree-at-most-two algebraic encoding: sort the rational sign breakpoints -d_e and solve the appropriate strictly increasing quadratic or linear segment. Test exactly whether a<=q0<=b. If so, beta0 is already a witness.

If q0<a, then H(a,beta0)>0, whereas the feasibility test supplies a rational beta^- with H(a,beta^-)<=0. A rational interpolation between these two profiles makes H(a,beta)=0, yielding the exactly capacity-feasible circulation a. If q0>b, use the rational maximizer at b and interpolate to H(b,beta)=0. No algebraic endpoint of [l_C,u_C] is needed.

Combine the independent cycle witnesses. The result is an exactly capacity-feasible rational resistance scenario. This argument covers singleton feasible intervals and irrational q0; only its comparison with rational capacity bounds is used.

## 4. Polynomial root enclosures and endpoint approximation

Binary search on [-B,B], using the LP comparisons in Section 1, encloses l_C and u_C to any rational width eta in polynomial bit time. If B=0, all flows vanish and the remaining bounds/objective are checked directly. Intersect these enclosures with [a,b] by taking endpointwise maxima/minima. This produces valid rational enclosures for the constrained endpoints

    L_C=max(l_C,a),  U_C=min(u_C,b)

of width at most eta.

For unconstrained additive arc maximization, retain at every feasible lower test q an LP profile with H(q,beta)<=0. Its true root is at least q and at most u_C. Once the enclosing interval has width eta, this rational profile is eta-optimal. Minimization is symmetric. Initial boundary tests at -B or B provide a profile when an extremum equals the boundary. The physical value can be separately approximated from the returned rational profile's scalar quadratic root.

## 5. Convex design over a rational surrogate box

Let f(x)=x^TQx/2+d^Tx+c with rational Q positive semidefinite. Let m be the number of edges and define

    L=1+max_i(|d_i|+(B+1)sum_j |Q_ij|),
    eta=min(1/2,epsilon/(16mL)).

Handle an edgeless graph directly. Enclose each constrained endpoint with width at most eta. If the upper enclosure L_C^+ is at most the lower enclosure U_C^-, retain the rational inner interval [L_C^+,U_C^-]. Every true feasible circulation projects to it within eta. Every rational circulation in it has an exact rational resistance witness from Section 2 and satisfies all capacities exactly.

Otherwise the true constrained interval has width less than 2eta. Take the exactly capacity-feasible rational resistance scenario from Section 3, with physical circulation q0. Enclose this single quadratic root and choose a rational proxy t within eta of q0. Freeze the surrogate coordinate at t, storing that scenario for final recovery. Every true constrained circulation differs from t by at most 3eta. Returning the stored profile changes the proxy by at most eta and satisfies all capacities exactly.

Cycle supports are disjoint, so every true feasible flow maps to the surrogate box within 3m eta in l1 norm, while final recovery changes any surrogate flow by at most m eta. Every surrogate flow has magnitude at most B+eta<=B+1. The displayed L therefore bounds objective differences on all relevant segments.

Optimize the rational convex quadratic on this surrogate box to additive error epsilon/2 by the established polynomial-bit convex method in the [reviewed cactus design theorem](../results/potential-flow-cactus-convex-design.md). Recover retained rational circulations by LP interpolation and frozen ones by their stored scenarios. The returned profile lies in every original cycle polytope and satisfies every capacity exactly. Its total objective loss is at most

    3mL eta+epsilon/2+mL eta
      <=epsilon/4+epsilon/2<epsilon.

No joint algebraic field is formed across cycles. All exact arithmetic outside single-profile cycle-root comparisons is rational LP, interpolation, and polynomial evaluation.

## 6. Exact extremal roots and rational optimizing profiles

The threshold oracle also permits exact recovery of the extremal circulation and an optimizing rational resistance profile. The following argument upgrades additive recovery to exact optimization without enumerating polytope vertices.

First, an extremal root is attained at a vertex of P. For example, at u=max_P q(beta), every H(u,beta)>=0 and at least one is zero. Minimizing this linear function over P gives a vertex with value zero, hence physical root u. The analogous statement holds at l using maximization.

Here is a computable common height bound for the physical roots of every vertex of P. Let t be its number of resistance coordinates. Clear all denominators in the rational inequality description, giving an integer system whose coefficient and right-hand-side magnitudes are at most C>=1. Put

    Delta=t! C^t.

Every vertex has coordinates N_e/D with a common nonzero integer denominator D and numerators N_e bounded in absolute value by Delta, by Cramer's rule and the determinant bound. Lower-dimensional polytopes cause no exception: a vertex has t linearly independent active constraint normals.

Write all rational cycle offsets as d_e=p_e/R using one positive integer denominator R, and let P0=max_e |p_e|. On every nonempty sign interval, multiplying H(q,beta) by D R^2 gives the integer polynomial

    sum_e N_e s_e (Rq+p_e)^2,

of degree at most two and coefficient height at most

    H0=max(1,2t Delta (R+P0)^2).

At a sign breakpoint use an adjacent nonempty interval and its closed endpoint. Strict monotonicity ensures this polynomial is not identically zero. Thus every vertex root is an algebraic number of degree at most two with a nonzero integer polynomial of height at most H0. Its primitive minimal polynomial has height at most H0: the irreducible quadratic case only removes content, and for a nonzero rational root first divide out any powers of q, then apply the rational-root theorem to the remaining polynomial. Its nonzero constant and leading coefficients still have magnitude at most H0. A zero root has minimal polynomial q. The bit lengths of Delta, R, P0 and H0 are polynomial in the input.

Any two distinct real algebraic numbers alpha,gamma with degree at most two and minimal-polynomial height at most H0 are separated by at least

    sep=1/(64 H0^7).

Indeed, if their minimal polynomials differ, their nonzero integer resultant has magnitude at least one. Its root-product expression includes alpha-gamma, at most three other root differences of magnitude at most 2(1+H0)<=4H0 by the elementary Cauchy bound, and leading-coefficient factors of magnitude at most H0^4. Rearrangement proves the bound. If their minimal polynomials agree, they are the two real roots of one irreducible quadratic and their difference is sqrt(discriminant)/|leading coefficient|>=1/H0. Linear minimal polynomials cannot have distinct common roots.

Bisect the maximum-root threshold oracle until its enclosing interval [v,w] has width strictly less than sep. The lower endpoint v always satisfies min_P H(v,beta)<=0. Solve this LP and obtain an optimal vertex beta_v. A vertex can be recovered in polynomial time by lexicographic coordinate minimization over the rational optimal face, using at most t additional LPs. Its physical root lies in [v,u], because H(v,beta_v)<=0 and u is the global largest root. Both that root and u are roots of vertex profiles, so their distance is either zero or at least sep. Since u-v<sep, they are equal.

The rational profile beta_v is therefore exactly optimal. Compute its unique scalar quadratic root exactly to obtain an algebraic encoding of u. Minimization is symmetric, taking an upper endpoint w with max_P H(w,beta)>=0 and a maximizing vertex. Boundary cases u=-B or l=B satisfy the same invariant; initialization at [-B,B] is valid for all profiles. The number of bisection and LP steps is polynomial in input size because log(1/sep) is polynomial.

This avoids enumerating vertices of P, following all parametric LP bases, or reconstructing an algebraic number by integer relations. The separation bound is used only to guarantee that the final rational LP vertex is exactly optimizing.

## 7. Consequences and limits

Independence is required between cycle polytopes, not between edges within one cycle. A polytope coupling different cycles destroys the product argument and is outside this result. The exact local recovery in Section 6 also supplies exact endpoint profiles for the convex-design surrogate argument, so the sharper earlier freezing scheme is also available.

For any rational linear objective of all cactus flows, block independence makes it affine and separable in the cycle circulations. Choose each cycle's exactly optimizing endpoint profile according to its rational objective coefficient. With capacities, a constrained endpoint is either an original extremum from Section 6 or a rational clipping value realized by Section 2; exact degree-two comparisons identify which case holds. This returns an exactly optimizing rational resistance scenario in polynomial time. Its scalar value can be approximated in polynomial bit time, while exact comparison of a sum of independent cycle values still inherits the square-root-sum barrier already present for fixed resistances. The result does not claim exact polynomial-time comparison of that sum.

## Verification and source scope

Both [the first full audit](../notes/review-potential-flow-cycle-polytope-resistance-design.md) and [the second full audit](../notes/review-potential-flow-cycle-polytope-resistance-design-second.md) passed. They checked the LP threshold directions, exact capacity witnesses, surrogate error budget, common Cramer denominator, degree-two root height and separation, and exact final vertex recovery. Review identified a minor rational-root explanation gap when the polynomial constant vanishes; the proof now explicitly removes powers of q before applying the rational-root theorem.

Linear programming for a fixed rational flow, determinant bounds, root separation, and convex quadratic minimization are established ingredients. The theorem combines them for correlated resistances within each independent cycle, including original rational scenarios and exact capacity guarantees. The [abstract root-method source assessment](../notes/monotone-polynomial-root-polytope-novelty.md) identifies classical quasilinear optimization as the general antecedent and treats exact rational vertex recovery as a supporting arithmetic refinement. A focused comparison with earlier uncertain-resistance single-cycle methods remains needed before assigning publication priority. The [cactus geometry source assessment](../notes/potential-flow-cactus-flow-region-and-optimization-novelty.md) records relevant antecedents and unresolved circuit sources.

The [shared-parameter two-cycle example](../notes/potential-flow-cross-cycle-correlation-obstruction.md), with its [independent check](../notes/review-potential-flow-cross-cycle-correlation-obstruction.md), shows that correlations between cycles can make a cactus flow region nonconvex. It is a geometric scope boundary, not a complexity hardness theorem.

## Exact algebraic-recovery diagnostics

[`cycle_polytope_root_recovery_checks.py`](../code/potential_flow_mpd/cycle_polytope_root_recovery_checks.py) passed 32 correlated resistance polytopes defined by boxes and a weighted-sum equality. It checked 254 vertices and 6,314 exact rational threshold-bisection steps. Each final LP-oracle vertex had an exactly maximal root, verified by separately isolating all vertex roots and applying the proved separation bound. Common-denominator and polynomial-height bounds were checked exactly for every vertex and every sign pattern. These small diagnostics enumerate vertices to implement an independent exact oracle; the theorem instead uses polynomial-time rational LP and does not enumerate them.
