# Convex worst-case performance with a fixed number of flow measurements

Date: 2026-09-05. Status: verified by two independent full mathematical audits, with a completed bounded source assessment. This is a passive-network implementation of classical fixed-dimensional zonotope enumeration, with an additive physical-scenario guarantee.

## Theorem

Fix a positive integer k. Under the fixed-nomination quadratic cactus model, allow independent positive resistance intervals or explicitly listed finite sets. Let R be a rational k-by-m matrix of linear flow measurements, and let g be a densely encoded rational polynomial convex on a box containing the attainable measurements. Then, for rational epsilon>0, an epsilon-optimal rational resistance scenario maximizing g(Rx) can be found in polynomial bit time for fixed k, with polynomial dependence on requested accuracy bits.

The polynomial degree may be fixed, or included by dense encoding when k is fixed. No claim is made for sparse binary-exponent polynomial encoding. Convexity is a promise here; the candidate does not require a new convexity-validation algorithm.

In particular, a rational convex quadratic flow objective with fixed matrix rank admits such an additive worst-case algorithm, after adding one measurement for its affine term. This contrasts with the [coupled Max-Cut boundary](../notes/potential-flow-cactus-convex-performance-hardness.md), where the objective rank grows.

No exact maximizing scenario is promised when choosing among candidates requires comparing independent radical sums. The output is a rational resistance scenario with a certified theoretical additive guarantee; its physical flow and exact objective can be irrational.

## 1. A projected zonotope with rational directions

The [reviewed cactus flow-region theorem](../results/potential-flow-cactus-flow-region-and-optimization.md) gives the interval region, or the convex hull of the finite-scenario region, as

    x=x0+Zq,   l_C<=q_C<=u_C.

Here x0 and cycle vectors Z_C are rational, and each bound is a separately encoded quadratic algebraic number. Every circulation endpoint has an exactly computable rational endpoint resistance scenario.

Measurement vectors form the zonotope

    y=Rx0+sum_C a_C q_C,   a_C=RZ_C in Q^k.

Its generator lengths u_C-l_C may be algebraic. Their directions a_C are rational. Positive lengths do not affect the hyperplanes separating generic normal directions. A zero length only makes the corresponding endpoint choice irrelevant.

## 2. Enumerate endpoint scenarios from rational sign cones

Ignore zero vectors a_C. Enumerate every full-dimensional cone of the central arrangement

    h^T a_C=0

in R^k. At fixed k there are polynomially many cones. A direct rational implementation inserts the hyperplanes incrementally and keeps the sign patterns for which

    sigma_C h^T a_C>=1 for every inserted C

is feasible. Homogeneity makes this equivalent to a nonempty strict sign cone. Rational linear feasibility supplies a polynomial-bit representative h. The number of retained patterns is bounded by the fixed-dimensional arrangement bound; repeated and dependent hyperplanes do not increase it.

For each cone choose q_C=u_C when h^T a_C>0 and q_C=l_C when h^T a_C<0. Zero a_C can use either endpoint. Combine the corresponding precomputed rational endpoint resistance scenarios.

Every vertex of the actual projected zonotope occurs among these choices. Indeed, its normal cone contains a generic direction avoiding all the finitely many nonzero a_C hyperplanes. Such a direction uniquely chooses every positive-length segment endpoint. Spurious hyperplanes from zero-length generators only refine the normal fan and do not remove the vertex. This argument also covers a lower-dimensional projected zonotope and the point case.

Since g is convex, it has a maximum at a projected vertex. That vertex is attained by one of the enumerated original resistance scenarios. Hence the candidate list is complete even for finite resistance sets: all needed endpoint scenarios belong to the original sets, and all other finite states lie in their convex hull.

## 3. Bit-precision comparison without a common algebraic field

Let B=sum_v |b_v| and let

    T=B max_j sum_e |R_je|.

Every attainable measurement lies in [-T,T]^k. On the enlarged box [-T-1,T+1]^k, a rational upper bound L>=1 for every partial derivative of g is obtained by summing absolute monomial derivative coefficients times powers of T+1. If needed replace T+1 by max(1,T+1). For fixed k and dense degree input, the bound has polynomial bit length.

Write M=max_j sum_C |a_jC|. Enclose each selected circulation endpoint to rational error

    delta<=min(1/(1+M), epsilon/[8kL(1+M)]).

Then the measurement error is at most M delta in every coordinate, remains within the enlarged box, and polynomial evaluation differs from the true candidate value by at most kLM delta<=epsilon/8. Quadratic-root enclosure, rational measurement summation and dense polynomial evaluation are all polynomial in the input and accuracy bits.

Evaluate every candidate this way, keep the one with largest rational estimated value, and return its already constructed rational resistance vector. Two comparison errors cost at most epsilon/4, so the returned physical scenario is epsilon-optimal. Independent quadratic fields are never combined into one exact field. The number of candidates is N^{O(k)}, not a claimed fixed-parameter tractable bound.

If B=0 or all a_C vanish, the objective is constant across resistance scenarios and the choice is immediate. A polynomial g of degree zero is handled similarly.

## 4. Fixed-rank quadratic specialization

For f(x)=1/2 x^T Qx+d^T x+c with rational positive-semidefinite Q of fixed rank r, rational LDL decomposition expresses its quadratic part as a sum of r nonnegative rational multiples of squares of rational linear forms. Use these r forms and the additional form d^T x as at most r+1 measurements. The resulting g is a convex quadratic in fixed dimension. The preceding algorithm therefore applies to either finite or interval resistances on arbitrary cacti.

This is a maximization statement. Finite-resistance convex target matching is already NP-hard on one cycle even for one scalar target measurement, so the result cannot be reversed into a convex-minimization claim for finite sets.

## Attribution and verification

Fixed-dimensional zonotope enumeration is classical: [Onn and Rothblum, Convex Combinatorial Optimization](https://arxiv.org/pdf/math/0309083), Lemmas 2.1–2.3 on PDF page 4 and Theorem 2.6 in Section 2.2, reduce convex optimization to projected edge directions and vertex enumeration. Their PDF page 8 also discusses real data in a real-arithmetic model. The fixed-rank quadratic specialization has the direct predecessor [Ferrez, Fukuda, and Liebling (2005)](https://www.sciencedirect.com/science/article/pii/S0377221704003352), which studies fixed-rank positive-semidefinite binary quadratic maximization via zonotopes. No novelty is claimed for these geometric or optimization mechanisms.

The [paired source assessment](../notes/potential-flow-cactus-convex-performance-novelty.md) explains the narrower contribution: rational direction enumeration, separate algebraic cycle-root approximation, and recovery of an allowed rational original resistance scenario with a bit-precision guarantee. It found no equivalent passive-network statement in the inspected sources, without claiming exhaustive priority clearance.

Both [the first full audit](../notes/review-potential-flow-cactus-few-measurement-maximization.md) and [the second full audit](../notes/review-potential-flow-cactus-few-measurement-maximization-second.md) passed. They checked degenerate generators and normal cones, finite-scenario attainment, dense polynomial encoding, the rational LDL specialization, and the complete error budget.

## Reproducible checks

[`cactus_few_measurement_checks.py`](../code/potential_flow_mpd/cactus_few_measurement_checks.py) checked 18 projected convex quartic examples in one to three measurement dimensions. The best of 286 enumerated rational-direction sign cones matched exhaustive evaluation of 1,512 circulation endpoint scenarios at 70-digit precision. Cases included zero measurement generators, repeated generators and zero-length circulation intervals. Cone feasibility used numerical linear programming; the exact algorithm in the proof uses rational linear feasibility.
