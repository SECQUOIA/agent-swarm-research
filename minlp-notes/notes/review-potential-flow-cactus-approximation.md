# Independent review: constructive multi-entry cactus MPD approximation

Date: 2026-09-05. Reviewer: `potential_flow_review`.

Reviewed candidate: [potential-flow-cactus-approximation-investigation.md](potential-flow-cactus-approximation-investigation.md).

**Verdict: PASS for the stated mathematical theorem.** The structural argument yields polynomially many nomination faces of dimension at most one. The ensuing fixed-dimensional algebraic computation, certified summation of the constant drops, and rational nomination rounding give the claimed polynomial bit-time additive approximation. This review is independent of the author but contributed the simpler Lipschitz estimate used for the final rounding step. A fresh review of that contribution is appropriate. Novelty and practical algorithm performance are separate questions.

## Aggregation and smooth sensitivity

Removing blocks off the objective-terminal block path leaves attached components with a single core attachment. Their original loads influence core conservation only through the sum within their attachment group. The Minkowski sum of independent real intervals is the interval whose endpoints are the sums of endpoints, and different attachment groups are disjoint. Thus every feasible balanced aggregate nomination can be disaggregated. With no flow or potential bounds, uniqueness of passive flow guarantees that these are exactly the attainable core nominations and objective values. This argument remains valid for the smoothed laws.

Use `rho>0` for the smoothing parameter, distinguishing it from the requested approximation tolerance. The smoothed law `phi_e(x)=beta_e(x|x|+rho x)` is continuously differentiable with strictly positive derivative. After fixing the potential gauge, conservation in inverse-potential coordinates has a positive-definite reduced Laplacian Jacobian. The inverse function theorem therefore gives continuously differentiable potentials as functions of balanced loads.

The objective derivative is `h^T d` in every balanced direction, where `h_t=0` and

```
B diag(1/[beta_e(2|x_e|+rho)]) B^T h = e_s-e_t.
```

This follows by differentiating the physical equations and using symmetry of the reduced Laplacian. The electrical source and sink in this equation are the **objective terminals**, even when the physical nomination has many entries and exits.

At a maximum over the balanced box, the directional first-order inequality holds against every other point of the box polytope, so the same nomination maximizes the linear functional `h^T b`. Linear-programming optimality supplies a balance multiplier `lambda` with the stated upper/lower saturation implications. No differentiability of the unsmoothed inverse law at zero and no nonlinear constraint qualification is assumed.

## Ordered thresholds and at most two free coordinates

The auxiliary electrical network has positive conductances. On its cactus core, unit electrical current traverses the blocks in series. A bridge has positive current. Both branches of a cycle have positive current because they connect the same distinct entrance and exit potentials and have positive total resistance. Thus `h` strictly decreases along each entrance-to-exit branch.

Block potential ranges have disjoint interiors in their natural series order. A multiplier in a block's interior range can coincide with at most one vertex per branch, hence at most two core vertices. Those two vertices, if present, are interior vertices of different branches of the same cycle. At an articulation value, the articulation is the only core vertex with that value. Values outside the full terminal range make every coordinate saturated at the same endpoint side. Fixed coordinates with equal lower and upper bounds cause no exception.

On a branch, the remaining possibilities are completely described by a threshold at a vertex or in an edge gap: preceding vertices are upper-saturated and succeeding vertices are lower-saturated; a vertex threshold may leave that one coordinate free. There are linearly many threshold locations per branch, so a cycle contributes quadratically many combinations. Shared entrance and exit labels must agree; inconsistent combinations can simply be discarded. Bridge thresholds, articulation thresholds, and fully saturated extremes add only linearly many cases. A cactus core has linear total block size, giving `O(n^2)` candidate faces.

Every such face is closed, being defined by fixed bound equalities and the original closed balanced box. The smoothing limits can be taken inside one fixed face because the family is finite. Consequently the original problem has an optimum in this polynomial family, with at most two free coordinates. A balance equation fixes the sum of the two; with fewer than two it fixes every coordinate. The feasible one-parameter interval has rational endpoints.

## Passing to zero smoothing

The draft's energy argument is valid. The feasible nomination polytope is compact, and tree routing bounds a comparison flow uniformly. Minimization of the positive cubic energy plus the nonnegative smoothed quadratic term gives a uniform bound on physical flows for `0<rho<=1`.

For convergent nominations and smoothing parameters tending to zero, every cluster point of their flows is feasible for the limit nomination. To prove its optimality, correct any fixed comparison flow for the limit nomination by a tree routing of the vanishing nomination difference. The corrected comparison flows converge, and passing the minimizing inequality to the limit shows that the cluster point minimizes the original energy. Strict convexity gives uniqueness. Summing edge drops along a fixed tree then proves convergence of normalized potentials.

This joint sequential continuity yields uniform convergence of the smoothed objective on the compact nomination domain. Hence cluster points of smoothed maximizers are original maximizers. Zero physical flows, vanishing unsmoothed conductances, and collapsed limiting electrical potential ranges do not invalidate the conclusion: the proof retains a fixed finite **nomination face**, not a limiting strictly positive conductance or strict sensitivity inequality.

The assumption that every interval contains zero is unnecessary for this reasoning. When all coordinates are forced to lower or upper bounds by an extreme multiplier, the candidate first/last block pattern still holds whenever that bound vector is balanced. The generalized theorem correctly needs only a nonempty finite balanced box.

## Fixed and variable blocks

On a two-pivot face, the variable cycle's total load is fixed, and every load outside it is fixed. The cut totals entering adjacent blocks therefore remain constant. Thus each other block has fixed effective nodal loads, and its flow and objective drop are independent of the nomination parameter. This is valid even when those fixed loads are nonzero at internal vertices of other cycles.

For such a fixed rational-load cycle, all flows are `c_e+sigma_e w` with rational `c_e` and `sigma_e` in `{−1,1}`. Its signed loop residual is strictly increasing in `w`: each summand is an increasing quadratic flow law composed with the same orientation sign twice. Its rational zero-flow breakpoints can be sorted and its signs there evaluated exactly. It has one global root. On the interval containing that root, the residual is quadratic or linear; a root at a breakpoint is rational. Consequently its flow and every path drop have algebraic degree at most two, with polynomial-size rational defining coefficients. Degenerate quadratic leading coefficients and repeated breakpoints are handled by these same cases.

Independent algebraic constant drops should be approximated separately and summed with certified rational intervals. Combining them into one primitive algebraic number, or deciding their exact sum against a rational threshold, is unnecessary and would discard the complexity advantage.

The active cycle has flows affine in two variables: the nomination parameter and one circulation. Its zero-flow lines form a planar arrangement with polynomially many cells, including boundary faces. On each cell closure, the loop law is a quadratic equality, all region restrictions are linear, and the objective is quadratic. Closure overlaps on zero-flow boundaries introduce no incorrect points because both signed polynomial pieces vanish there.

The compact box bound is valid: all passive physical flows are acyclic when oriented in their actual directions, and decompose into paths from positive to negative loads. Therefore each edge flow is bounded by total injection and hence by `B=sum max(|l_v|,|u_v|)`. A full-core spanning-tree routing obeys the same bound. A circulation coordinate, normalized by coefficients of absolute value one, is then bounded by `2B`. The path-drop objective is bounded in absolute value by `B^2 sum beta_e`.

## Algebraic subroutines and bit complexity

Two real variables, fixed polynomial degree, polynomially many constraints, and polynomial-bit rational coefficients suffice for exact semialgebraic feasibility in polynomial bit time. Rational objective bisection takes polynomially many calls in the input length and `log(1/epsilon)` because the objective bound itself has polynomial binary encoding length. Algebraic feasible-point sampling at a known feasible threshold also has polynomial bit complexity in this fixed-dimensional setting.

An independently checked source is Basu's [author survey](https://www.math.purdue.edu/~sbasu/raag_survey2011_final.pdf): Theorem 2.18 states quantifier-elimination operation and intermediate integer-size bounds; Theorem 3.6 and its following consequence give algebraic sample-point computation with corresponding bounds. At fixed variable count and degree these bounds are polynomial in the number of constraints and coefficient bit length. The [single-cycle booking paper](https://optimization-online.org/wp-content/uploads/2019/11/7472.pdf), Section 6, uses the same general approach, but the present proof does not require its particular nomination sign pattern or a constant number of constraints.

All graph-derived coefficients are rational sums and fixed-degree products of input numbers. Clearing their denominators requires only products of polynomially many polynomial-bit denominators, so output and intermediate encoding lengths remain polynomial. Approximating each fixed drop to inverse-polynomial fractions of the requested additive error likewise requires polynomially many bits.

If each face optimum is enclosed in an interval of width `w`, then the maximum lower endpoint and maximum upper endpoint enclose the global optimum with width at most `w`. Selecting the face with largest lower endpoint gives a face whose optimum is at most `w` below the global optimum. These two elementary interval facts validate the draft's selection step without exact radical-sum comparisons.

## Rational nomination output and quantitative continuity

The reviewer supplied the following simpler continuity bound. It holds on any connected passive quadratic network, not just cacti. Fix a simple objective-terminal path and let `R_path` be its sum of resistances. For the smoothed electrical sensitivity network, each edge resistance is `beta_e(2|x_e|+rho)`. The physical flow bound gives an effective electrical resistance at most `(2B+rho)R_path`, by testing unit flow along that path. The electrical maximum principle gives

```
0 <= h_v <= (2B+rho)R_path.
```

Integrating the objective derivative along the feasible segment between two balanced nominations gives

```
|F_rho(b')-F_rho(b)| <= (2B+rho)R_path ||b'-b||_1.
```

Passing to zero smoothing yields the rational, polynomial-bit Lipschitz constant `C=2B R_path`. When `B=0`, the only feasible nomination is zero and the problem is immediate.

On a two-pivot face, changing the nomination parameter by at most `eta` changes the full aggregate nomination in one-norm by at most `2eta`. Approximate an algebraic feasible parameter by a rational point within its **rational feasible interval**; projecting a rational approximation onto that interval preserves rationality and cannot increase its distance from the true parameter. Choosing `eta<=epsilon/(8C)` limits the objective loss to `epsilon/4`. The required precision has polynomial encoding length. Singleton feasible intervals are rational and need no approximation.

Disaggregate each rational core total into its original rational load intervals greedily. This gives an exactly feasible and balanced rational nomination, and aggregation preserves the objective. The three losses from choosing a face, choosing a sampled local point, and rational parameter approximation are each bounded by `epsilon/4`, so their sum is below `epsilon`.

The output claim concerns rational **nominations**, not a fully rational tuple of physical flows and potentials. Such a tuple need not exist for rational nominations, already in the independently reviewed square-root gadget. The current draft explicitly respects this distinction.

## Remaining checks outside this verdict

The algorithm is a theoretical construction using exact real algebraic computation; this review does not establish practical performance or supply an implementation of that subroutine. The proof should cite its standard subroutine explicitly and use different symbols for smoothing and output tolerance. A fresh independent review should check the Lipschitz contribution and the full argument. No substantive mathematical defect was found in the reviewed version.
