# Correlated polynomial edge laws on independent cactus cycles

Date: 2026-09-05. Status: verified by two independent full mathematical audits. The supporting arithmetic and convex-optimization mechanisms are credited; this verification does not establish publication priority.

## Model and results

Fix rational balanced nominations on a connected simple cactus. For each cycle C, let theta_C range over a nonempty bounded rational polytope P_C given by linear inequalities. The parameter polytopes are independent across cycles. Every edge e of C has a law

    pi_u-pi_v=g_e(x_e;theta_C)

that is continuous and piecewise polynomial in x_e, with fixed rational breakpoints and dense rational polynomial coefficients affine in theta_C. Polynomial degrees and piece counts may grow with the input. Assume that for every theta_C in P_C each edge law is strictly increasing on the real line and satisfies g_e(0;theta_C)=0. These are promises, not properties asserted to be verified by this algorithm. Bridges have fixed rationally encoded laws of the same passive type; allowing independent bridge parameters does not affect flows and is optional.

Then the following hold in polynomial bit time, with no bound on cycle size or count:

- Every signed arc-flow extremum has an exact real-algebraic encoding, of degree at most the largest edge-law degree, and an optimizing rational parameter scenario can be recovered.
- With rational signed arc capacities, feasibility is decidable exactly and a rational parameter scenario satisfying them exactly can be recovered. The same holds for rational linear flow constraints whose nonconstant part involves only one cycle circulation.
- Every rational linear flow objective has an exactly optimizing rational parameter scenario, including under those capacities. Its scalar value can be approximated to any additive precision; exact comparison of a sum across cycles is not claimed polynomial.
- A rational positive-semidefinite quadratic objective of all flows can be minimized to additive error epsilon with a rational parameter scenario satisfying capacities exactly, in time polynomial in the input and requested accuracy bits.

All outputs concern original admissible edge-law parameters. Physical flows and potentials may be irrational. Correlations between different cycles, uncertain nominations, moving breakpoints, and arbitrary potential constraints are not covered.

## 1. Existence, flow bounds, and scalar cycle equations

For fixed parameters, integrating each continuous strictly increasing law gives a strictly convex primitive. It is coercive: with c=min(g_e(1),-g_e(-1))>0, its value for |x|>=1 is at least c(|x|-1). Thus total energy has a unique minimizer on the nonempty affine conservation space. Its stationarity gives potentials modulo a constant and the passive edge equations.

Orient the physical positive flows from higher to lower potential. This orientation has no directed cycle, so flow decomposition gives |x_e|<=B=sum_v |b_v|. The bound is uniform in the parameters. The B=0 case is immediate.

Fixed nominations determine bridge flows and the effective nomination of each cycle, independently of the other cycle parameters. After consistent cycle orientation, write x_e=q+d_e with rational d_e and choose one reference edge with offset zero. If this reverses an input orientation, replace its law by x -> -g_e(-x;theta_C), which preserves all promises and polynomial encoding properties.

Cycle pressure consistency is exactly

    H_C(q,theta_C)=sum_(e in C) g_e(q+d_e;theta_C)=0.

For every admissible theta_C this is continuous and strictly increasing in q. Its unique root lies in [-B,B]. At a rational q, H_C is a rational affine function of theta_C. The shifted breakpoints are the input edge breakpoints minus d_e; their total count and encoding length are polynomial. On each common interval, H_C is a densely encoded univariate polynomial of degree at most D, affine in theta_C. Rational translation of a dense degree-D polynomial has polynomial coefficient bit growth and cost. No product of edge polynomials is formed.

## 2. Exact local optimization by the monotone-root lemma

Apply the piecewise version of the [reviewed monotone polynomial-root theorem](../notes/monotone-polynomial-root-polytope-optimization.md) to H_C on [-B,B]. It gives exact extreme roots l_C,u_C and rational parameter vertices attaining them. It permits growing dense degree and fixed rational breakpoints, including roots at breakpoints, without assuming a derivative lower bound.

The root image of each compact connected P_C is the interval [l_C,u_C]. Continuity follows, for example, from the uniform strict sign inequalities on either side of any root and continuity of H_C in its arguments. The complete cactus flow region is therefore the independent affine box x=x0+Zq with these intervals.

The lemma's exact recovery is important: an approximate value oracle alone would not automatically identify the correct algebraic endpoint or an exactly optimizing original scenario. Here the LP vertex root-separation argument supplies both.

## 3. Rational target realization and exact capacities

A rational target circulation q is attainable precisely when

    min_(theta in P_C) H_C(q,theta)<=0
      <=max_(theta in P_C) H_C(q,theta).

Both extrema are rational LPs. Their rational optimizing parameter vectors can be interpolated to force H_C(q,theta)=0 exactly. The interpolation remains in P_C, so every constituent law stays within the promised passive family. An affine constant in H_C does not affect this argument because affine functions preserve convex combinations.

Every rational arc bound or permitted cycle-local inequality clips [l_C,u_C] by a rational interval. Exact algebraic comparisons decide emptiness. Each clipped endpoint is either an original extreme root with its rational vertex witness or a rational clipping value with the LP-interpolation witness. These facts include singleton feasible intervals and roots of degree larger than two. Directly check the rational bridge flows against their capacities.

Combining one feasible endpoint witness per cycle gives an exactly capacity-feasible rational global scenario. Choosing the correct endpoint for each rational linear-objective coefficient gives an exactly optimizing rational scenario. The corresponding exact objective may sum independent algebraic values from many cycles, so that separate scalar comparison task is not included.

## 4. Coupled convex quadratic design

Use the [reviewed rational surrogate-box proof](../results/potential-flow-cactus-capacitated-convex-design.md) with the new algebraic circulation endpoints. Exact root isolation gives rational endpoint enclosures of any requested width in polynomial bit time under dense encoding. The proof only uses that property and rational endpoint witnesses; it does not require degree two.

Retained inner intervals are rational and are recovered by the LP interpolation above. Narrow intervals use their stored exact endpoint scenario after numerical surrogate optimization. The passive flow bound B and the objective gradient bound remain unchanged. Consequently the same error budget yields a rational original parameter scenario that satisfies all capacities exactly and is epsilon-optimal for the convex quadratic objective.

This argument needs no constitutive derivative or inverse-flow continuity bound: approximation occurs directly in the independent flow coordinates, and every final coordinate is realized exactly or through an exactly feasible stored endpoint scenario.

## Convex polynomial objectives

The separately [reviewed convex polynomial objective extension](potential-flow-convex-polynomial-design.md) replaces the PSD quadratic performance by any rational densely encoded polynomial promised convex on the expanded flow box |x_e|<=B+1. Its perspective construction supplies the required polynomial-bit convex oracle, while the present parameter recovery and exact capacities remain unchanged. The second application/objective reviewer checked this composition explicitly.

## Attribution and verification

Both [the first full audit](../notes/review-potential-flow-correlated-polynomial-cycle-design.md) and [the second full audit](../notes/review-potential-flow-correlated-polynomial-cycle-design-second.md) passed. They checked passive existence, orientation reversal, shifted partitions, growing dense degree and coefficient size, affine parameter interpolation, exact capacity clipping, and the inherited surrogate algorithm.

The scalar monotonicity, LP interpolation, polynomial root arithmetic, and convex optimization are established ingredients or separately reviewed results. The [root-method source assessment](../notes/monotone-polynomial-root-polytope-novelty.md) treats the exact vertex recovery as a supporting arithmetic refinement of classical quasilinear optimization. The [cactus source assessment](../notes/potential-flow-cactus-flow-region-and-optimization-novelty.md) records related uncertainty geometry and unresolved older circuit sources. This application combines the mechanisms for correlated polynomial laws within independent cycles; a complete direct-priority comparison remains open.

## Exact diagnostics

[`correlated_polynomial_cycle_checks.py`](../code/potential_flow_mpd/correlated_polynomial_cycle_checks.py) passed 72 exact root brackets, 216 zero-at-zero and breakpoint monotonicity controls, and 215 exact rational target-profile recoveries. The examples use a two-parameter triangular polytope shared across each cycle's edges, heterogeneous polynomial degrees from one to seven, and centered piecewise-linear hinges. Thus they include nonodd laws with continuous but nondifferentiable breakpoints. All interpolated profiles remained inside the original correlated polytope and satisfied cycle pressure balance exactly. The general algebraic separation argument is audited in the abstract root theorem.
