# Second independent review: uncertain piecewise polynomial flow laws

Date: 2026-09-05. Reviewer: `potential_flow_review`.

**Verdict: PASS for the strongest scope stated below.** This is a fresh proof audit of [the affine-law candidate](potential-flow-affine-law-uncertainty-investigation.md), including its continuous-law addendum, and [the polynomial-law candidate](potential-flow-polynomial-laws-investigation.md). It is independent of [the first affine-law review](review-potential-flow-affine-law-uncertainty.md). The earlier quadratic-flow review alone would not establish these extensions.

Only the maximum cycle rank of a biconnected block is fixed. The degrees, number of pieces, number of basis functions, and number of uncertain coefficients may grow in the **dense rational input encoding**. Each edge law has the form

```
g_e(x,theta_e) = f_e0(x) + sum_j theta_ej f_ej(x).
```

The basis functions are continuous piecewise polynomials on the whole real line, with fixed rational breakpoints, and vanish at zero. Each coefficient has its own finite rational interval. Every complete law throughout this independent coefficient box must be strictly increasing. Nomination intervals are finite rational intervals with a nonempty balanced intersection; they need not contain zero. Under these assumptions the candidate supports polynomial-bit additive optimization of terminal potential differences, rational near-optimal nomination/coefficient inputs, exact algebraic signed-edge-flow extrema, and exact comparison of those extrema with rational capacities.

These conclusions concern extrema over the unrestricted physical states induced by the input boxes. They do not add flow-capacity or pressure constraints to the optimization domain. They do not claim exact comparison of arbitrary sums of independently algebraic block pressure optima. Shared uncertain coefficients across blocks, uncertain breakpoints, and sparse binary exponents are outside this audit.

## 1. Physical existence, boundedness, and limits

A continuous strictly increasing finite-piece polynomial law on the whole real line tends to opposite infinities at the two ends. Its outer polynomials cannot be constant, because that would create constant intervals. Its primitive is strictly convex and coercive on feasible flows. The standard energy argument therefore gives a unique physical flow for every balanced nomination. Potentials are unique after one normalization.

The assumption `g_e(0)=0` ensures that a nonzero flow goes from higher to lower potential. The directed support of the physical flow has no directed cycle. Consequently each edge flow has absolute value at most

```
B = sum_v max(abs(lower_v), abs(upper_v)).
```

This bound is uniform over the coefficient box. It is also sufficient to avoid an unnecessary uniform-coercivity assumption: bounded flow and bounded constitutive-law values give uniformly bounded normalized potentials. For converging nominations and coefficients, any subsequential state limit solves the limiting equations, and uniqueness identifies it. Thus the physical state depends continuously on the inputs and the required joint maxima are attained.

The same compactness argument applies to constitutive-law approximations that converge uniformly on the relevant bounded interval. It is valid even when a limiting derivative vanishes. A uniform positive lower derivative bound for the original law family is not required.

## 2. Continuous laws and the nomination-face argument

For a smooth nonnegative kernel of integral one supported on `[-1,1]`, the centered operator

```
S_rho f(x) = integral eta(t) f(x-rho*t) dt
            - integral eta(t) f(-rho*t) dt
```

is linear in `f` and gives zero at zero. Convolution preserves increase. Therefore

```
g_rho(x,theta) = S_rho g(x,theta) + rho*x
```

is smooth and has derivative at least `rho`. The centering is necessary for retaining the zero-flow/zero-drop normalization and its acyclic-flow bound. Nonmonotone individual basis functions cause no problem: monotonicity is required for each complete law, and the smoothing is applied linearly to that law.

A continuous finite-piece polynomial is locally Lipschitz. For `rho<=1`, piecewise derivative bounds on `[-B-1,B+1]` give uniform convergence on `[-B,B]`, uniformly over the bounded coefficient box. Continuity at a breakpoint ensures that the distributional derivative has no point mass; hence convolution derivatives are bounded by the essential supremum of the ordinary piece derivatives. This justifies both the smoothing argument and the later sensitivity bounds for laws with corners.

The smoothed physical states converge uniformly by compactness and uniqueness. Thus the previously reviewed nomination-face proof transfers in full: first identify the single active block; within that block use the perturbed electrical adjoint and its degree-two paths; then pass to a limit through the finite family of closed nomination faces. The proof uses only positive smoothed derivatives and graph structure, not quadratic constitutive laws. The topology bounds and the number of free nomination/circulation coordinates remain functions of the fixed block cycle rank.

At a joint optimum, fix its coefficient vector and replace its nomination by a maximizer in this graph-only face family. This preserves a joint optimum. Because coefficient intervals are independent across blocks, the remaining block objectives separate once effective nominations are fixed. This independence is a real hypothesis, rather than a convenience of the proof.

The smoothing need not be represented by polynomials or computed. It proves the existence of an optimizer on a finite family of faces. The algorithm optimizes the original continuous piecewise polynomials on those faces. No numerical smoothing parameter or effective convergence rate enters the algorithm.

## 3. Dense degrees and many coefficient variables

On a selected face, physical flows are affine in a core `z` whose dimension is bounded in terms of the block cycle rank. The common refinement of the basis breakpoints gives polynomially many affine hyperplanes in this fixed-dimensional core. Their arrangement, including its lower-dimensional cells, has polynomial complexity. On each cell all basis evaluations are rational polynomials in `z`.

Substituting an affine form into a densely encoded univariate polynomial of degree `D` produces at most `binomial(D+k,k)` monomials in `k` fixed core variables. Their coefficient lengths are polynomial in the input length. Dense encoding is essential: it makes `D` at most the input length. Refining the pieces across many basis functions takes their union of breakpoints, rather than a Cartesian product of pieces.

There is a particularly direct verification of the many-leaf step here. Include the local objective as one extra coordinate alongside the cycle equations. For coefficient leaf `theta_j`, let `W_j(z)` be its vector of coefficients in these equations and the objective. The attainable linking/objective vectors at fixed `z` form the translate of the zonotope

```
sum_j [lower_j, upper_j] W_j(z).
```

Membership in this compact convex set is equivalent to all of its support inequalities. For a support direction `lambda`, the support contribution of leaf `j` is

```
max(lower_j * lambda^T W_j(z),
    upper_j * lambda^T W_j(z)).
```

The signs of the polynomials `lambda^T W_j(z)` choose all maximizing endpoints. Enumerating their realizable sign conditions takes polynomial time because the combined dimension of `z` and `lambda` is fixed. For each sign condition the complete support inequality is a single rational polynomial inequality. Ties cause no difficulty because both endpoints give the same support value. Universal quantification over `lambda` gives an exact fixed-dimensional formula for membership, and hence for the local optimization problem.

In this interval-leaf setting **there are no denominators to clear**. Polynomial degrees grow with the dense input degree, but the number of real variables stays fixed. Fixed-dimensional real algebraic algorithms are polynomial in the number of polynomials, their degrees, and their coefficient lengths. This dependence follows from the quantitative bounds in [Basu's survey, particularly Theorem 2.18](https://www.math.purdue.edu/~sbasu/raag_survey2011_final.pdf); the degree need not be treated as a fixed constant here.

Exact sampling yields the local core, objective value, and a common algebraic extension of polynomial degree and encoding length. Recovering the possibly many coefficient leaves is then a linear feasibility problem over that same field. The applicable complexity bound is polynomial in the common extension degree, as stated by [Adler and Beling](https://adler.ieor.berkeley.edu/ilans_pubs/lp_algebraic_1994.pdf). This does not form an uncontrolled compositum of separately represented roots. With input degrees growing, the field degree is polynomially bounded; it is not asserted to be constant.

The more general fixed-core theorem's denominator argument also survives dense degrees: fixed-size minors have degree `O(D)`, and polynomially many denominator factors have polynomial total degree. Expansion stays polynomial in a fixed number of variables. The direct support proof above is sufficient for the present coefficient boxes.

## 4. Pressure accuracy, rational inputs, and exact flow extrema

For a smooth law let `R` be the diagonal matrix of positive constitutive derivatives, and let `j_h` be the electrical flow for a unit source at the objective's first terminal and unit sink at its second terminal. Differentiating physical conservation and the potential equations gives

```
dF = h^T db + sum_ej j_h,e f_ej(x_e) dtheta_ej.
```

Every edge of this unit electrical flow has absolute current at most one. Its potential range is the effective resistance, which is at most the sum of edge resistances on any fixed terminal path. For the centered smoothing, the basis term becomes `S_rho f_ej`, whose absolute value is at most `2N_ej`, where `N_ej` bounds the original basis on the enlarged interval. The derivative bounds likewise hold uniformly there. Integrating along a segment in the nomination/coefficient boxes and taking the smoothing limit proves

```
|F(b,theta)-F(c,eta)|
 <= C_b ||b-c||_1 + 2 sum_ej N_ej |theta_ej-eta_ej|.
```

The original C1 note's uncentered smoothing gives its sharper factor-one coefficient bound. Both are valid in their stated settings. All constants have polynomial encoding length even when the dense degrees grow: coefficient-sum bounds involve powers whose exponents are at most the input degree.

Algebraic coordinates can therefore be isolated to rational boxes at polynomial precision. Intersect the nomination box with the exact balance equation and use rational linear programming to recover balanced rational nominations. Round each coefficient within its own rational interval. Allocate the error across all nomination and coefficient coordinates, including the input-dependent number of coefficients. This gives a rational input with the stated pressure loss. Its physical state need not be rational; the result does not claim otherwise.

For a single edge, strict increase of its complete law implies that at fixed coefficients its signed flow and its endpoint potential difference have exactly the same maximizers. Fixing a joint maximizing coefficient vector therefore transfers the nomination-face theorem to the flow objective. The objective flow is affine in the local core, and the endpoints of the edge lie in one block. Exact local algebraic optimization and pairwise algebraic comparison establish the flow-extremum and rational-capacity claims without summing independent algebraic block values. Minimizing signed flow reverses the objective terminals; no oddness assumption is needed.

For a general terminal pressure difference, independently algebraic block optima are approximated separately and their rational enclosing intervals are added. The method does not decide arbitrary exact equality of their sum with a rational threshold.

## 5. Polynomial validation of the complete coefficient box

The proposed validation is necessary and sufficient and is polynomial in the dense input model.

First verify rational breakpoint matching and zero at zero. For the C0 result only function values must match; derivative matching is unnecessary. On a common open polynomial piece, the minimum complete derivative over the independent coefficient intervals is

```
f_e0'(x) + sum_j min(lower_j f_ej'(x), upper_j f_ej'(x)).
```

Partition this piece at the real roots of the nonzero basis derivative polynomials. Identically zero derivative polynomials must be omitted from their product. The product has polynomial degree and coefficient length in the dense input, and provides a common root-isolation representation. On each resulting interval the minimizing endpoint for each coefficient is fixed, so exact univariate sign tests decide nonnegativity of the complete envelope. Unbounded outer intervals are included. The one-sided derivatives on the original pieces and continuity of the law suffice at original breakpoints.

After establishing nonnegative derivatives for every coefficient vector, strict increase fails exactly when some allowed complete law is constant on a nonempty interval. Such an interval contains an open subinterval of one common original polynomial piece. Its derivative polynomial then vanishes identically on that entire piece. Matching all derivative coefficients to zero is a rational linear system in the uncertain coefficients. Testing its intersection with the coefficient box is an ordinary LP. Conversely a feasible LP supplies an allowed law flat on that nonempty piece, so strict increase fails. Empty pieces are omitted.

This correctly permits isolated zero derivatives and rejects flat intervals. It applies to signed coefficient intervals and nonmonotone basis functions because the derivative envelope concerns complete laws throughout the full box.

## Review scope and presentation

No mathematical correction was required. The candidate files' opening status and C1-only scope are now stale relative to their proved C0 addendum and the two completed independent audits; promotion should consolidate those statements and retain the encoding and independence hypotheses above. This review establishes correctness of the mechanism, not a separate exhaustive novelty search.

The numerical checks recorded by the author are useful supporting evidence for cycle identities and derivatives. This second review independently checked the proofs and complexity bounds; it does not report a new numerical rerun.
