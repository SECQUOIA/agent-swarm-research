# Second independent audit of correlated polynomial cycle design

Date: 2026-09-05. Reviewer: `spatial_sdp_review`.

**Verdict: PASS.** The [candidate](potential-flow-correlated-polynomial-cycle-design.md) correctly applies the reviewed fixed-breakpoint monotone-root lemma and the exact-capacity cactus design proof to continuous piecewise-polynomial laws affine in independent cycle parameter polytopes. Dense degree and piece count may grow with the input. Exact local extrema, rational realizing parameters, exact capacity feasibility, exact linear-objective scenario optimization, and additive convex quadratic design follow within the stated scope.

## 1. Passive states and scalar representation

For fixed parameters, the primitive `G_e(x)=integral_0^x g_e(s) ds` is continuously differentiable and strictly convex. Since the law is strictly increasing and vanishes at zero, G is nonnegative. With `c=min(g(1),-g(-1))>0`, integrating on the appropriate side gives `G(x)>=c(|x|-1)` for `|x|>=1`. The sum is therefore coercive in the finite-dimensional flow space. The conservation space is a nonempty closed affine space for a connected graph and balanced nominations, so the strictly convex energy has a unique minimizer. Equality-constrained stationarity identifies its gradient with incidence-transpose potentials, giving exactly the physical equations.

The derivative of g itself is unnecessary. Continuous nondifferentiable breakpoints and vanishing constitutive derivatives therefore cause no problem. The energy primitive remains differentiable.

A nonzero physical flow always points from higher to lower potential because g has the sign of its argument. These positive-flow directions form a directed acyclic graph. Source-to-sink path decomposition bounds every flow magnitude by total positive nomination and hence by the displayed B, uniformly over parameters. Zero nominations give zero flow directly; in that case arbitrary rational feasible parameter points can be obtained from their nonempty rational polytopes.

On a cactus, fixed conservation determines bridge flows and independent cycle offsets rationally. A consistent cycle orientation writes its flows as `q+d_e` with one zero reference offset. Reversing an input edge replaces its law by `-g_e(-x;theta)`, which preserves continuity, strict increase, zero at zero, parameter affinity, and rational fixed-breakpoint encoding. Summing the oriented drops gives exactly H. Independent cycle consistency together with conservation is sufficient for global physical consistency.

## 2. Encoding and exact root optimization

The common partition of q is the union of shifted rational breakpoints from the edge laws. Its size is at most their total supplied count. No combination of edge pieces must be enumerated beyond these intervals. Expanding `(q+d)^j` introduces only degree-j binomial coefficients and powers of the polynomial-bit rational offset. Hence translating a densely encoded polynomial, summing its coefficients, and sorting the breakpoints all have polynomial bit cost in numerical degree and total input length. Degrees do not increase under translation or summation.

H is continuous and strictly increasing for every admissible parameter point. Its physical reference flow lies in `[-B,B]`, so its endpoint signs meet the abstract lemma's bracket promises. For B positive, this is a nontrivial bracket. Fixed breakpoints and affine parameter dependence satisfy the other hypotheses exactly.

The [second abstract audit](review-monotone-polynomial-root-polytope-optimization-second.md), including its fixed-breakpoint addendum, verifies polynomial-time exact endpoint roots and rational optimizing vertices, even when derivatives vanish, roots are repeated, or a root lies at a breakpoint. The output degree is at most the maximum input law degree. Coefficient bit lengths are polynomial, not necessarily coefficient magnitudes.

The root depends continuously on theta. At an interior root, strict signs at two nearby points trap roots for all sufficiently nearby parameters by joint continuity; boundary roots use the corresponding one-sided trap inside the common bracket. Compact connected parameter polytopes therefore have compact interval root images. Since parameter blocks are independent across cycles, their entire product is attainable, giving the stated affine box flow region.

## 3. Rational realization, capacities, and linear performance

At rational q every edge piece can be selected by rational comparisons, and every selected polynomial evaluates to a polynomial-bit rational affine function of theta. Continuity makes a breakpoint evaluation independent of the chosen adjacent representation on the admissible polytope.

The root is at least q exactly when H is nonpositive there, and at most q exactly when H is nonnegative. Thus rational target attainability is precisely the pair of LP value inequalities displayed in the candidate. A rational convex combination of their optimizing parameter vectors sets H to zero. Affine constant terms preserve this identity. The combination stays in the original polytope, so all coupled laws remain in the promised passive family. A zero LP-value difference means both profiles already realize the target.

Signed capacities and permitted linear flow constraints reduce to rational bounds on a single circulation. Empty intersections can be decided by exact comparison of algebraic endpoints and rational bounds. Comparing two degree-D algebraic numbers represented by polynomial-size polynomials and isolating intervals is polynomial-time; only local pairs are compared, and no field containing all cycles is formed.

A clipped endpoint is either an original extremum with its rational vertex witness or a rational boundary with its LP-interpolation witness. Ties can use the original witness. This covers irrational singleton intervals as well as rational singletons. Bridge bounds involve fixed rational flows. Combining endpoint witnesses gives an exactly feasible global rational scenario.

A rational linear objective becomes a constant plus one rational coefficient per cycle circulation. Its coefficient sign selects an exactly optimizing constrained endpoint in each block. Returning these parameter profiles does not require deciding the sign of a sum of independent algebraic roots. The candidate correctly distinguishes this exact scenario optimization from exact scalar threshold comparison. Additive evaluation of the scalar objective can refine separate root enclosures according to its rational coefficients.

## 4. Inheriting additive quadratic design

The [second exact-capacity design audit](review-potential-flow-cactus-capacitated-convex-design-second.md) used three endpoint properties: polynomial-bit enclosures at requested precision, rational admissible endpoint witnesses, and independence of cycle coordinates. None depended on degree two. All three properties hold here under dense encoding; standard algebraic root refinement is polynomial in degree, coefficient bit length, and requested accuracy bits.

A retained rational inner interval is physically feasible, and LP interpolation recovers its optimized rational circulation exactly. A frozen proxy is replaced by its stored exact endpoint parameter scenario, which satisfies capacities exactly even if the proxy itself did not. Cycle supports remain disjoint, so the same projection and recovery errors hold in the full flow l1 norm. The same uniform B and quadratic gradient bound control objective perturbation. All convex optimization arithmetic occurs on a rational surrogate box.

The resulting parameter output is rational with polynomial bit length. Its physical state may be algebraic and need not be produced in a common algebraic field. Neither a derivative lower bound nor a continuity modulus for inverse constitutive laws is needed because numerical approximation occurs directly in flow coordinates.

## 5. Diagnostics and limitations

Independently inspected and reran `code/potential_flow_mpd/correlated_polynomial_cycle_checks.py`. It passed 72 exact root brackets, 216 zero/hinge controls, and 215 rational target-profile recoveries, with degrees one through seven. Its triangular shared-parameter examples include nonodd continuous laws with nondifferentiable hinges. These diagnostics check concrete realizations; the general variable-degree exact recovery rests on the abstract proof audit.

Strict increase and zero at zero throughout each parameter polytope remain promises. Inter-cycle parameter correlations, moving breakpoints, uncertain nominations, and potential constraints are excluded. This audit establishes mathematical correctness of the application, not literature priority. No correction is required.
