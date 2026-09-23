# Independent review: endpoint and facial pooling specifications

Date: 2026-09-05. Reviewer: `potential_flow_review`.

Reviewed candidate: [pooling-endpoint-quality-structure.md](pooling-endpoint-quality-structure.md), including the face-recognition LP and fixed-pool, fixed-quality face-enumeration algorithm.

**Verdict: PASS.** The endpoint disjunction, universal flow-integrality characterization, nonface counterexample, polynomial recognition, and face-enumeration algorithm are correct for the stated standard pooling model. This review does not establish novelty. The topology is input–pool–output with optional direct input–output arcs; no pool-to-pool arcs are included.

## Endpoint specifications

For a positive-throughput pool, each reconstructed quality is its nonnegative weighted input average. At a zero-bound output, the corresponding total quality mass is a sum of nonnegative terms and must equal zero. Thus a pool with positive outflow to any output strict in quality `k` must have zero pool quality in that coordinate. Since all positive input quality values have positive weights in the average, this is equivalent to zero total inflow from those input arcs. The unweighted quantity `D_lk` is therefore appropriate: it detects positive support, not the magnitude of quality mass.

The converse also holds simultaneously for multiple quality coordinates. Under `D_lk=0 OR S_lk=0`, any strict output receiving from the pool has `S_lk>0`, so all active intakes have zero value in that coordinate. Every reconstructed pool quality remains at most one. Compatible direct arcs have zero value in each strict output coordinate. All quality inequalities therefore hold. Inactive pools and outputs do not create exceptions because their quality masses and outflows vanish.

Fixing one side of each disjunction only forces specified arcs to zero. With ordinary flow conservation, finite arc bounds, and vertex-throughput bounds, the remaining problem is a standard network flow problem after node splitting. Positive lower bounds on a deleted arc simply make that branch infeasible; they are retained, not silently dropped. The at-most-`2^(pk)` branch count is correct. Each proposed binary inequality uses a valid pool-throughput upper bound because both `D_lk` and `S_lk` are sub-sums of that throughput.

## Integral flow and NP certificates

With integer flow bounds, node splitting gives integral network flow polytopes. Their projection onto original arc flows is also integral. Since the number of branches is finite and the flows are bounded, the pooling flow projection is a finite union of bounded integral polytopes. Its convex hull is the convex hull of finitely many integer vertices and is therefore integral. Every rational linear cost has an integral optimal flow whenever the model is feasible.

This establishes existence of an integral optimum; it does not require every feasible flow or every optimum to be integral. Pool qualities can remain fractional even at integral flows when multiple input units mix.

An integral flow certificate has polynomial encoding length because all flows are bounded by binary-encoded input bounds. The branch support disjunctions and ordinary flow constraints can be checked directly. The integer-bound endpoint family is consequently in NP, and the already reviewed unit-capacity hardness subfamily establishes strong NP-completeness. General pooling NP membership is not inferred.

## Facial sufficiency

Let `C=conv{lambda_i}` and `F_j=C intersect R_j`. At positive output throughput, the blended quality belongs to `F_j`. Every contributing pool quality and direct-input quality belongs to `C`. If `F_j` is a face, its defining segment property forces every positive-weight contributing quality into `F_j`. Applying that property again at each contributing pool forces every original input vector with positive intake into `F_j`.

Thus an intake arc and output arc through one pool are incompatible precisely when the intake's original quality vector is outside the receiving output face. Conversely, excluding all incompatible positive pairs suffices: each contributing pool averages only input vectors in every face to which it sends flow, and the final output blend remains in that convex face. Compatible direct arcs behave in the same way.

Here a compatible support means an **allowed set of arcs**; an actual flow's positive support may be any subset of it. Fixing such an allowed set leaves a closed ordinary network flow polytope, not a set requiring every retained arc to be strictly positive. The finite union over these allowed supports is exactly the pooling flow projection. The integral-optimum conclusion follows for arbitrary rational linear costs and integer bounds.

The interpretation of a general output polyhedron is its condition on positive-throughput blends. Equivalently, if `R_j={q:A_j q<=b_j}`, impose its homogenized inequalities on quality mass and throughput. At zero throughput the conditions reduce to zero inequalities. In particular, an empty `F_j` forces zero incoming flow; positive output lower bounds then correctly make the relevant network infeasible.

## Necessity and original input generators

The converse is sound for every nonempty nonface `F=C intersect R`. By failure of the face property, there are `x,y` in `C` and `0<theta<1` with an interior combination `q=theta x+(1-theta)y` in `F` and at least one endpoint, say `x`, outside `F`.

Express both endpoints using the **original** finite input generators. Every such expression of `x` must put positive mass on at least one generator outside `F`; otherwise convexity of `F` would place `x` in `F`. Combining the endpoint representations gives a representation of `q` by original inputs with positive total forbidden-input mass. The positive factor `theta` preserves that mass, and other nonnegative mixture weights cannot cancel it.

In the proposed one-pool, one-output network, that mixture at throughput one respects every unit arc and vertex upper bound and has strictly negative cost. Every integer feasible flow has throughput zero or one. Throughput one forces exactly one intake arc to carry one unit, so the output quality equals an original generator. Feasibility forces that generator into `F`, where its intake cost is zero. Hence every integer feasible flow has cost zero, and none is optimal in the presence of the negative-cost fractional mixture.

This argument correctly separates a universal guarantee over network topologies and costs from the behavior of any particular existing network. The counterexample itself has only one output arc and is a linear optimization problem after eliminating its quality variable; the characterization concerns integrality, not computational hardness.

## Rational witnesses and polynomial face recognition

The proposed LP both proves rationality constructively and recognizes the face condition without computing hull facets. Mark generator `i` forbidden when `lambda_i` is outside `R`; since every generator already belongs to `C`, this is equivalent to being outside `F`. Maximize total forbidden weight over the rational simplex intersected with the output inequalities.

If the LP is infeasible, `F` is empty. If `F` is a face, its property forces forbidden weight zero in every feasible mixture. Conversely, if the LP optimum is zero, a segment with an interior point in `F` cannot have an endpoint outside `F`: expanding that endpoint into original generators would produce a feasible mixture with positive forbidden mass. Thus optimum zero implies the face property.

For a nonface, the LP has strictly positive optimum. It is a bounded rational polytope, so it has a rational optimal vertex with polynomial encoding length. That vertex is an explicit rational strict-improvement mixture for the unit-capacity counterexample. No rationality assumption about the original geometric segment witness is needed. Generator membership tests, LP construction, and the rational certificate all have polynomial bit complexity.

## Fixed-pool, fixed-quality algorithm

Every active pool quality has a unique minimal face of `C`. Since it is an average of its input qualities, the face property places all positive-intake input generators in that minimal face. Every receiving output face contains the pool quality and therefore contains the entire minimal face. Consequently the original feasible flow survives the enumeration branch selecting each pool's minimal face.

Conversely, if all retained intake generators belong to the selected pool face and every retained receiving output face contains it, then every pool and output blend satisfies its specifications. Direct arcs are retained exactly when their original input quality belongs to the receiving output face. Inactive pools can receive arbitrary nonempty face states. The union of the resulting min-cost flow problems therefore gives exact optimization, including arbitrary direct arc graphs.

The finite-dimensional face count and construction are valid. Work in the rational affine hull of dimension `d<=k`. Every facet contains `d` affinely independent original input points, so candidate supporting hyperplanes can be enumerated from those subsets and checked against all generators. There are at most `m^d` candidates. For a nonempty proper face, take a basis among its active facet normals for the orthogonal complement of its affine hull. At most `d` normals suffice; the matching facet equalities then recover the face's entire affine hull, whose intersection with `C` is the face.

To realize the literal loose bound `m^(d^2)`, enumerate ordered tuples of exactly `d` candidate facets, allowing repetition to pad choices with fewer than `d` facets. Their intersections include every nonempty proper face; add `C` separately and discard empty intersections. Face membership and containment can be checked using the original generators lying in each face, which generate it. For `d=0`, the single nonempty face `C` is enough.

Thus at most `(1+m^(k^2))^p` min-cost flow solves suffice. Hull processing, face tests, and network solves have polynomial bit complexity for fixed `p,k`. Rational capacities are sufficient for exact optimization; integer capacities are additionally needed for the integral-output conclusion. The bound is an elementary upper bound and need not be sharp.

## Review scope

No numerical tests were needed: all claims reduce directly to exact support, convex-combination, face, and network-flow arguments. The note appropriately leaves novelty unclaimed. Its endpoint result does not cover interior quality bounds; the stated example with input qualities zero and one, output bound `delta` in `(0,1)`, and a reward on dirty input correctly has fractional optimum `-delta` and integral optimum zero.
