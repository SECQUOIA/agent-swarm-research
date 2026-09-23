# Independent review: correlated polynomial laws on cactus cycles

Date: 2026-09-05. Reviewer: `benders_property`. Status: PASS.

Reviewed [the full application candidate](potential-flow-correlated-polynomial-cycle-design.md), including the now-integrated fixed-breakpoint Section 6 of the [abstract root theorem](monotone-polynomial-root-polytope-optimization.md). I previously audited the abstract theorem, correlated quadratic-cycle construction, and exact-capacity surrogate method. This review checks the broader constitutive laws and every application dependency; it does not establish publication priority.

## Passive state and block decomposition

For each fixed admissible parameter vector, continuity and strict increase of g make its primitive continuously differentiable and strictly convex. The zero-at-zero promise makes the primitive nonnegative. The displayed lower bound outside [-1,1] is correct on both sides: integrate a positive lower bound on g for x>=1 and a negative upper bound on g for x<=-1, reversing the integration direction in the latter case. The positive constant may depend on the fixed scenario; that suffices for coercivity and existence on the closed affine conservation space. Strict convexity supplies uniqueness. Equality-constrained stationarity supplies a potential vector even though the incidence matrix has one redundant row.

Strict passivity forces each nonzero flow to follow a strict potential decrease. There is no directed cycle of positive flow, so standard flow decomposition bounds each edge by total positive nomination, and hence by the stated B. This uniform bound does not require a uniform derivative, a uniform energy constant over the parameter polytope, or differentiability of the laws at breakpoints.

Bridge flows and the effective nominations entering each cactus cycle are fixed by conservation. Distinct cycles have independent circulation coordinates, including when they share an articulation vertex. Consistently orienting a cycle gives rational offsets and one reference-edge flow q. Reversing an original edge requires `-g(-x;theta)`, exactly as written. This is essential for nonodd laws; it preserves strict increase, continuity, zero-at-zero, fixed rational breakpoints, and affine coefficient dependence. The cycle equation is then a sum of increasing functions of q.

## Representation and abstract root theorem

For a fixed cycle, take the union of all rational breakpoints after translation by its rational offsets and intersect it with [-B,B]. This is a scalar partition with polynomially many pieces, not a product of the individual edge partitions. On each piece, summing translated polynomials preserves affine dependence on theta and degree at most the maximum edge degree D. Expanding a dense translated degree-D polynomial uses polynomial arithmetic and polynomial coefficient bit growth in D and the input encoding; binomial coefficients have O(D) bits. Forming the common partition and all its coefficients remains polynomial even when the polytope dimension, number of edges, degrees, and piece counts grow.

The B=0 case is correctly handled separately. Otherwise [-B,B] is a nonempty rational bracket. The physical state proves that every profile has its cycle root there; global strict increase gives the endpoint signs. These verify all promises needed by the abstract piecewise theorem. A root at a shifted breakpoint belongs to an adjacent closed polynomial piece, and the recovered vertex root has degree at most D. Shifting or reversing it to describe an original signed arc flow preserves that algebraic degree and polynomial encoding length.

The exact root and rational optimizing parameter vertex therefore follow from the reviewed height, separation, and LP recovery theorem. Fixed breakpoints are essential to this application. Nothing here validates the passive-family promises or covers moving breakpoints.

## Parameter interpolation and exact capacities

At any rational target q, every edge-law evaluation and the cycle sum are rational affine functions of the original parameter vector. The two LP sign tests characterize attainability. Their optimizing rational vectors can be combined to make the affine cycle sum zero, because an affine function preserves convex combinations just as a linear function does. The combination stays in the original polytope; consequently every constituent edge law remains in the promised family. The output is an admissible original parameter scenario, not a collection of independently modified edge coefficients.

Continuity of the unique root map follows from strict scalar sign inequalities around a root and continuity in the parameters. Compactness and connectedness of each cycle polytope give an attained interval image. Independence between cycles gives the entire affine product region. These facts justify clipping each circulation interval by rational capacities or cycle-local linear inequalities.

Exact comparison of the degree-at-most-D endpoint encodings is polynomial in their degree and coefficient bit length. It does not require a field containing every cycle root. A clipped endpoint is either an original algebraic endpoint with a rational vertex witness or a rational boundary with the LP-interpolation witness. This covers rational and irrational singleton intervals. Bridge capacities are direct rational comparisons. Selecting one endpoint per cycle gives a feasible global scenario; selecting according to the rational coefficient of a separable linear objective gives an exactly optimizing scenario without comparing a sum of algebraic numbers.

## Coupled convex quadratic objective

The earlier exact-capacity surrogate proof requires only polynomial-bit endpoint enclosures and exact rational endpoint parameter witnesses. Both are now supplied by the abstract theorem and interpolation; degree two was never needed in the approximation or recovery argument. Retained rational coordinates are exactly realized by LP interpolation. Frozen coordinates return their stored exact feasible endpoint scenarios, so every original capacity holds exactly after recovery.

The independent circulation structure, disjoint edge supports, flow bound B, and rational objective gradient bound are unchanged. Hence the original projection and recovery errors and the epsilon-optimality estimate apply verbatim. Polynomial root isolation and refinement in growing dense degree supply the requested enclosures in polynomial input and accuracy bits. No constitutive derivative bound, inverse-law condition number, or common algebraic field across cycles is used.

The theorem correctly limits exact scalar output: a rational optimizing parameter scenario is available for a linear objective, while exact comparison of the resulting sum of independent algebraic quantities is a separate task. Arbitrary potential constraints and globally coupled performance geometry are outside the stated proof.

## Verification

I independently reran `code/potential_flow_mpd/correlated_polynomial_cycle_checks.py`. It passed 72 exact root brackets, 216 zero-at-zero and hinge controls, and 215 exact rational parameter recoveries, with degrees one through seven. These tests include nonodd continuous laws with nondifferentiable hinges, which exercise the broadened orientation and interpolation assumptions. They supplement the proof; they do not replace the abstract algebraic separation audit.

I also reread the abstract theorem's final integrated piecewise section and verified that its handling of breakpoints, nonzero piece polynomials, common height bounds, and final root identification matches the extension approved in the earlier review.

No correction was required.
