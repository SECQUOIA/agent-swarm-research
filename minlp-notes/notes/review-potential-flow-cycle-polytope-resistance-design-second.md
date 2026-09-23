# Second independent audit of correlated cycle resistance design

Date: 2026-09-05. Reviewer: `spatial_sdp_review`.

**Verdict: PASS after a minor proof clarification already applied.** The [candidate](potential-flow-cycle-polytope-resistance-design.md) supports arbitrary rational resistance polytopes within each cactus cycle, independent between cycles. Exact capacity feasibility, rational feasible profiles, additive convex quadratic design, exact individual extrema, and exact rational profiles optimizing linear flow objectives all follow in polynomial bit time. Exact comparison of the resulting sum of independent algebraic values is correctly excluded.

## 1. LP threshold directions and realization

For a fixed positive resistance profile, `H(q,beta)` is continuous, strictly increasing, and unbounded in both directions. Its unique zero varies continuously with beta. A compact connected polytope therefore has a compact interval of root values. Positivity is uniform because explicit positive lower resistance bounds are part of the input.

The threshold directions are correct: a profile has root at least q exactly when its H value at q is nonpositive. Thus the largest root is at least q exactly when the minimum LP value is nonpositive. Likewise the smallest root is at most q exactly when the maximum LP value is nonnegative. Compactness gives attainment, so the corresponding strict comparisons are valid too.

At a rational test q, all LP coefficients are polynomial-bit rational numbers. A rational q belongs to the root interval precisely when these minimum and maximum values straddle zero. Interpolation between their rational optimal profiles stays in the polytope and sets H to zero. It also handles one or both LP values equal to zero. The interpolation coefficient has polynomial bit length.

Capacity feasibility is equivalent to `u>=a` and `l<=b`, together with `a<=b`; these are exactly the two displayed LP tests. The proposed witness construction also works at an irrational singleton: a rational initial profile whose root already lies in the capacity interval can be returned directly. If its root lies below a, H at a is positive and interpolation with an LP minimizer realizes a; the symmetric construction at b is correct. The comparisons require only the scalar root of a single rational profile, which is piecewise quadratic with polynomially many rational breakpoints.

## 2. Enclosures and additive convex design

Threshold bisection has valid initialization on `[-B,B]` and polynomial bit complexity. Taking maxima or minima with rational capacity endpoints cannot increase enclosure widths. A retained inner interval is exactly feasible. When the two inner enclosure endpoints cross, the true interval has width less than `2 eta`; a proxy within eta of any capacity-feasible physical root is within `3 eta` of every point in that interval.

Recovering a frozen coordinate uses its stored feasible rational profile, so exact capacity satisfaction does not depend on the proxy satisfying capacities. Recovering a retained rational coordinate uses LP interpolation. Independence between cycle polytopes makes all recovered coordinates jointly physical and keeps resistance correlations within each cycle satisfied.

Disjoint cycle supports give projection error at most `3m eta` and recovery error at most `m eta`. Every surrogate flow is within eta per edge of some actual feasible flow, hence has magnitude at most `B+1`. The displayed gradient bound applies on all comparison segments. Therefore the total loss is at most `4mL eta+epsilon/2<=3epsilon/4`. The polynomial-bit convex optimization step is exactly the one checked in the [earlier second audit](review-potential-flow-cactus-convex-design-second.md); rational LPs and scalar quadratic root enclosures add only polynomial work. Zero-dimensional cases require no optimization.

## 3. Exact recovery: vertices and height bounds

At the largest root u, every profile has `H(u,beta)>=0` and some profile has value zero. The minimizing face of this linear functional contains a vertex of P, whose root is therefore u. This is an existence argument over real coefficients; the algorithm does not need to solve an LP with those coefficients. The smallest root has the symmetric vertex argument.

For any vertex of the integer inequality system, choose t independent active normals. Cramer's rule gives a common denominator and all numerators bounded by `Delta=t! C^t`. This remains valid for lower-dimensional polytopes: a vertex lacking t independent active normals would admit a nonzero feasible local displacement in both directions. Clearing denominators in the input inequalities and in the rational offsets creates integers with polynomial bit lengths.

On a sign interval the vertex cycle equation, after multiplication by `D R^2`, is the displayed integer polynomial of degree at most two. Its quadratic, linear, and constant coefficients have magnitudes bounded respectively by `t Delta R^2`, `2t Delta R P0`, and `t Delta P0^2`, all within H0. Strict monotonicity rules out an identically zero polynomial on any nonempty open sign interval. A breakpoint root is also a root of either adjacent polynomial by continuity.

The minimal-polynomial height conclusion holds. For an irreducible quadratic it follows by removing content. For a nonzero rational root, first remove all factors q if the constant coefficient is zero; the remaining polynomial still has height at most H0 and nonzero constant term. The rational-root theorem then bounds both the reduced numerator and denominator by H0. Zero itself has minimal polynomial q. I independently requested this zero-constant clarification; the author confirmed that the first reviewer had requested it too, and it is now in the candidate. It changes no theorem or constant.

## 4. Separation and the final LP vertex

Take primitive minimal polynomials with a common sign convention. For different polynomials the resultant is a nonzero integer. Its root-product formula includes the selected difference, at most three other root differences bounded by `4H0`, and leading coefficient powers bounded by `H0^4`. Thus the selected nonzero difference is at least `1/(64H0^7)`. This remains a conservative valid bound when one or both degrees are one. Complex conjugate roots cause no problem because the Cauchy bound controls their absolute values too.

If the minimal polynomials coincide and the selected roots differ, they are the two roots of an irreducible quadratic. Their distance is the square root of its positive integer discriminant divided by the leading coefficient magnitude, and is at least `1/H0`. These cases establish the common separation bound.

The main recovery argument is valid. At a lower bracket v for the maximum root, an optimal vertex of the rational LP minimizing `H(v,beta)` has root in `[v,u]`. The global maximum u itself is a vertex root. Once the bracket width is strictly less than the separation bound, these two vertex roots must coincide. This also covers a boundary maximum and equality of the LP value to zero. For minimum recovery, the upper bracket and maximizing LP give the symmetric argument.

An optimal vertex of the LP is computable without vertex enumeration. Restrict to its rational optimal face, then minimize coordinates successively and retain each minimizing equality. After at most t further LPs every coordinate is fixed. The resulting point is a vertex of that face and hence of P. Its rational encoding, each intermediate equality, and all LP encodings have polynomial bit length by the usual rational LP bounds. Consequently the complete recovery procedure uses polynomially many polynomial-size rational LPs. Computing the selected profile's scalar quadratic root then gives an exact algebraic encoding of the extremum.

## 5. Linear optimization, boundaries, and diagnostics

Every weighted linear flow objective is a rational constant plus a sum of rational multiples of the independent cycle coordinates. The sign of each coefficient selects one constrained endpoint. Exact degree-two comparisons determine whether that endpoint comes from an original extremum or a rational capacity boundary. The previous constructions provide a rational profile in either case. Combining these profiles exactly optimizes the objective, even though comparing its scalar value with a rational threshold can involve a sum of many independent quadratic algebraic numbers.

The result requires independence between cycle polytopes, fixed nominations, positive compact resistance domains, and only cycle-local flow constraints. It makes no claim about finite resistance choices, inter-cycle correlations, or potential constraints. The exact recovery mechanism is an elementary combination of rational LP, Cramer's rule, and degree-two separation; this audit checks correctness, not literature priority.

Independently reran and inspected `code/potential_flow_mpd/cycle_polytope_root_recovery_checks.py`. It passed 32 correlated polytopes, 254 vertices, and 6,314 exact threshold bisections. The diagnostics enumerate small vertex sets only to check the oracle and recovery statement; the theorem's algorithm does not enumerate vertices. Its general polynomial-time conclusion follows from the proof, not this restricted diagnostic family.
