# Global resistance correlations make total cactus flow strongly hard

Date: 2026-09-05. Status: verified by two independent full mathematical audits, with a completed bounded source assessment. Established capacity linearization and convex Max-Cut mechanisms are credited; publication priority remains qualified.

## Theorem

For fixed unit source/sink nominations on a connected simple cactus with the common quadratic law, maximizing the sum of all arc flows over a globally correlated rational resistance polytope is strongly NP-hard. The graph has maximum degree three and a directed acyclic orientation; every physical arc flow is strictly positive. Thus the objective also equals the sum of absolute flows, with coefficient one on every edge.

Every resistance lies in [1,3], fixed resistances equal two, and the global correlation constraints have bounded integer coefficients. An explicit restricted family has NP-complete weak-threshold attainment and coNP-complete robust upper-threshold satisfaction. Absolute-error 1/256 value approximation is NP-hard on this bounded-data family.

The exact-capacity and individual-arc tasks under the same global polytope model remain polynomial by the [separate arc theorem](../notes/potential-flow-global-correlation-arc-validation.md). The hardness concerns a coupled objective over many cycles, not capacity feasibility or a single arc extremum.

## 1. Paired triangles encode one comparison edge

Take an unweighted Max-Cut instance H with n vertices, m>=1 edges, and target integer 1<=K<=m. Trivial source cases are preprocessed; fixed outputs in the same family can use a one-edge comparison graph with K=1 for yes and a comparison triangle with K=3 for no. Introduce theta_i in [0,1] for each vertex. For each comparison edge ij make two unit-through-flow triangles, indexed by the signs + and -. Write delta=theta_i-theta_j.

In the plus triangle, a two-edge source-to-sink path has resistance 2+delta on each edge. In the minus triangle, the corresponding two edges each have resistance 2-delta. Each triangle's alternate single edge has fixed resistance two. All resistances lie in [1,3]. Let f_+ and f_- be the two-edge path flows. Conservation and equal path drops give

    f_+=f(2+delta),   f_-=f(2-delta),
    f(r)=1/(1+sqrt(r)).

Both path flows and both alternate flows 1-f_+,1-f_- are strictly positive for every allowed parameter. The total of all three edge flows in a triangle is 1+f_+ or 1+f_-.

The scalar f is strictly convex for r>0 because

    f''(r)=(1+3sqrt(r))/[4r^(3/2)(1+sqrt(r))^3]>0.

Consequently the pair contribution psi(delta)=f(2+delta)+f(2-delta) is convex and even on [-1,1]. At binary theta, its value is

    A=2/(1+sqrt(2))=2sqrt(2)-2   if theta_i=theta_j,
    B=1/2+1/(1+sqrt(3))=sqrt(3)/2   otherwise.

Their difference kappa=B-A is a positive absolute constant. In fact sqrt(3)>173/100 and sqrt(2)<283/200, by exact squaring, give

    kappa>7/200>1/32.

## 2. One actual-edge resistance polytope and the full graph

Join the 2m triangles in a chain using 2m-1 bridges of fixed resistance two. Triangle vertices are otherwise distinct, and bridges connect an exit terminal to the next entrance terminal. Put a further path of n bridges before the first triangle. Its edge i has resistance r_i in [1,2], and define theta_i=r_i-1.

These extra bridge resistances make the uncertainty set an explicitly described polytope in the vector of actual physical edge resistances, without relying on a projected parameter representation. For comparison edge ij impose the linear equalities

    beta_plus,path1=beta_plus,path2=2+r_i-r_j,
    beta_minus,path1=beta_minus,path2=2-r_i+r_j.

All other triangle and joining-bridge resistances are fixed at two. The correlation coefficients and right-hand sides are in a fixed integer alphabet, and every resistance remains in [1,3]. The polytope is the injective affine image of [0,1]^n through the bridge coordinates; its vertices correspond exactly to binary theta.

Put nomination +1 at the beginning of the extra bridge path, -1 at the final triangle exit, and zero elsewhere. Every bridge carries flow one, and every triangle carries unit through-flow. Orient all paths from source to sink. The physical graph is simple and acyclic as a directed graph, with maximum degree three. It has

    |V|=6m+n,   |E|=8m-1+n,   cycle rank=2m.

All arc flows are strictly positive, including the bridges.

## 3. Exact relation to maximum cut

The sum of all physical arc flows is

    T(theta)=4m-1+n+sum_(ij in E(H)) psi(theta_i-theta_j).

It is a convex function of theta on its cube, so a maximizing cube vertex exists. At a binary theta, it equals

    T(theta)=C+kappa * cut(theta),
    C=4m-1+n+mA.

Thus OPT=C+kappa * MaxCut(H). No loss or asymptotic approximation enters this identity. The global correlations transfer the comparison graph H into the objective despite the physical cactus topology and unit objective coefficients.

## 4. Rational thresholds, strong hardness, and membership

Let Q=C+kappa(K-1/2). Compute a rational threshold tau with |tau-Q|<=1/512. This is possible with polynomially bounded numerator and denominator: enclose sqrt(2),sqrt(3) by dyadics to width at most 1/(8192(m+1)), and substitute into

    Q=4m-1+n+(m-K+1/2)A+(K-1/2)B.

The coefficients have magnitude O(m), so these enclosures more than suffice. Their dyadic denominators are O(m+1), and tau has numerator polynomial in m+n. Consequently all numerical data, including the rational threshold, have polynomial unary encoding length.

If MaxCut(H)>=K, then OPT>=C+kappa K>tau+7/512. If MaxCut(H)<=K-1, then OPT<=C+kappa(K-1)<tau-7/512. Hence the source answer is equivalent to OPT>=tau, with a strict constant gap. Robust satisfaction T<=tau encodes the complementary source answer. This proves strong NP-hardness and coNP-hardness, respectively.

On this explicit family, membership is also immediate. A maximizing scenario can be chosen at binary theta, giving integer resistances. Its value is C+kappa k for an integer cut size k, in the fixed degree-at-most-four field Q(sqrt(2),sqrt(3)). Comparing it with a rational threshold is polynomial-time exact algebraic arithmetic. Therefore weak-threshold attainment is NP-complete and robust upper-threshold satisfaction is coNP-complete on the stated family. This membership argument is not asserted for arbitrary coupled objectives over arbitrary globally correlated cacti.

An additive value estimate with error at most 1/256 decides the source by comparison with tau, since 1/256<7/512. Thus fixed absolute-error approximation is hard without scaling nominations, resistances, or objective coefficients. No fixed relative-error or objective-normalized constant-error claim follows from this statement.

## 5. Near-optimal scenario output

A polynomial-time algorithm returning a rational admissible resistance scenario with total flow at least OPT-1/256 would also decide the source. In a no instance every scenario is below tau-7/512. In a yes instance the returned scenario is above tau+5/512. Its value can be approximated to absolute error 1/512 by separately enclosing the quadratic triangle roots and summing them; the required precision has polynomial bit length in the output scenario and the graph size. The two cases remain separated by tau.

This does not require the algorithm to return a binary scenario or require exact comparison of an arbitrary sum of radicals. A polynomial-time rational-output algorithm necessarily returns a scenario with polynomial bit length, which suffices for the additive evaluation step.

## Attribution and verification

The mechanism uses classical convex Max-Cut maximization. The [completed source assessment](../notes/potential-flow-global-correlation-novelty.md) found no matching restricted theorem for the sum of every positive arc flow under the stated bounded-data cactus model, while crediting broad circuit-tolerance hardness and the established combinatorial mechanism. This is a bounded comparison, not exhaustive priority clearance.

Both [the first full audit](../notes/review-potential-flow-global-correlation-total-flow-hardness.md) and [the second full audit](../notes/review-potential-flow-global-correlation-total-flow-hardness-second.md) passed. They checked the actual-resistance polytope, every graph count and flow sign, the rational threshold and strong encoding bounds, restricted NP/coNP membership, and the near-optimal scenario-output reduction.

The independent [exact second checker](../code/potential_flow_mpd/global_correlation_total_flow_second_review.py) passed 71 complete cactus structures, 1,068 exact binary physical states in Q(sqrt(2),sqrt(3)), and 205 rational thresholds. It checked conservation and pressure balance on every physical edge, not only the scalar objective formula.

## Reproducible full-state checks

[`global_correlation_total_flow_checks.py`](../code/potential_flow_mpd/global_correlation_total_flow_checks.py) passed 1,197 complete positive-flow states over all 63 nonempty comparison graphs on four vertices, including all binary profiles and additional fractional profiles. It verified cactus counts, maximum degree, DAG orientation, actual resistance bounds, conservation, quadratic path consistency, the cut-value identity, and domination of tested fractional scenarios by the endpoint optimum. At 90-digit precision the largest physical residual was below `4.91e-91`. It also checked 192 rational threshold constructions, their strict yes/no gaps, and polynomial numerator/denominator bounds. The threshold arithmetic is exact rational arithmetic; the physical-state evaluations are high-precision numerical checks.
