# Independent review: correlated cycle resistance design

Date: 2026-09-05. Reviewer: `benders_property`. Status: mathematical PASS. The author applied the minor rational-root justification correction recorded below; I verified the final wording. No substantive theorem change was needed.

Reviewed [the full candidate](potential-flow-cycle-polytope-resistance-design.md), including its exact-recovery Section 6 and final exact scenario-optimization consequence. The previously reviewed continuous cactus geometry and rational convex surrogate-box algorithm are valid imports. Publication priority of this correlated formulation requires the separate source audit.

## Scalar LP oracle and exact capacity feasibility

For a cycle's consistently oriented offsets, H(q,beta) is strictly increasing in q for every allowed positive beta. Its unique root is continuous in beta. A nonempty compact polytope is connected, so the root image is exactly a closed interval. Correlation within a cycle does not affect these statements; independence between cycles is essential to their product use.

The LP signs are correct: `u>=q` is equivalent to `min H(q,beta)<=0`, and `l<=q` to `max H(q,beta)>=0`. Strict comparisons use strict signs, including at equality. At rational q, every LP coefficient is rational with polynomial encoding. Rational witness interpolation is valid because H is linear in beta and the polytope is convex.

After reducing capacities to a rational circulation interval [a,b], the two tests are exactly `u>=a` and `l<=b`. Together with a<=b, they characterize interval intersection. An arbitrary rational profile's quadratic root can be compared exactly with a and b. If outside the capacity interval, interpolation at the violated rational endpoint constructs an exact feasible profile. Singleton feasible intervals are covered: an irrational singleton already contains the stored root when feasible; otherwise a rational clipping target is recovered exactly. Bridge bounds are independent rational tests.

The reference circulation is an actual oriented edge flow, so the global nomination bound B applies. Intersecting with [-B,B] is valid even though the cycle can receive effective nominations through bridges and articulation blocks. Zero nominations and edgeless cases are correctly separated.

## Additive optimization with exact recovery

LP bisection encloses both interval endpoints to any polynomial-bit requested width. Maxima or minima with rational clipping endpoints preserve enclosure validity and width. For retained rational inner intervals, exact LP interpolation gives a profile in the original polytope. In a narrow interval, the stored capacity-feasible profile from Section 3 has circulation q0 in that same interval; a rational proxy within eta of q0 is therefore within 3 eta of every true feasible coordinate. Recovery changes it by at most eta and restores exact capacities.

Disjoint cycle supports give the claimed `3*m*eta` projection and `m*eta` recovery bounds. Every surrogate is within eta per edge of a feasible physical state formed by replacing only its frozen coordinates, so the magnitude bound B+1 and gradient bound L remain valid. The loss is at most `4*m*L*eta+epsilon/2<=3*epsilon/4`. All inputs to the imported convex optimizer are rational, and no common field of all cycle roots is needed.

## Exact optimal profiles: existence and height

At the largest attainable root u, H(u,beta) is nonnegative throughout P and vanishes somewhere. Its minimizing face therefore contains a vertex of P realizing u. The coefficients of this supporting functional may be algebraic; vertex existence still follows from elementary polytope geometry, and the vertex itself remains rational. Minimization of roots is symmetric.

Clearing denominators in the rational description gives an integer coefficient bound C of polynomial bit length. At any vertex, t independent active normals yield a common determinant denominator and Cramer numerators bounded by `Delta=t!*C^t`. This includes lower-dimensional polytopes. A common denominator R for offsets and the proposed H0 then bound all coefficients of the quadratic sign-piece polynomial of every vertex profile. All logarithms of these bounds are polynomial in the original input. Strict monotonicity excludes an identically zero polynomial on any nonempty sign interval. A root at a sign breakpoint is also a root of an adjacent closed sign piece.

For an irrational quadratic root, its primitive minimal polynomial is the sign-piece polynomial after removing content, so its height is at most H0. For a nonzero rational root, first remove any powers of q from that polynomial and then apply the rational-root theorem; numerator and denominator are bounded by coefficients of the remaining polynomial, still at most H0. A zero root has minimal polynomial q.

The draft's initial wording instead bounded a rational numerator by the *original* constant coefficient. That wording fails for the nonzero root 100 of `q*(q-100)`, whose original constant coefficient is zero. Dividing out zero-root factors corrects the proof without changing H0, the algorithm, or any claim. This correction was sent to the author.

## Separation and final LP-vertex extraction

For distinct minimal polynomials of degrees at most two, irreducibility makes the integer resultant nonzero. Its absolute value is at least one. Their roots, including complex roots, have magnitude at most 1+H0, so every other root difference is at most 4H0. There are at most three such factors, and the leading-coefficient factors contribute at most H0^4. Consequently the separation bound `1/(64*H0^7)` is valid. If the minimal polynomials coincide, two distinct real roots of their irreducible quadratic differ by `sqrt(discriminant)/abs(leading coefficient)>=1/H0`. Linear polynomials have no distinct roots. Repeated roots cause no exception because minimal polynomials in characteristic zero are square-free.

At a lower bracket endpoint v, LP gives a minimizing vertex with H(v,beta)<=0. Its physical root lies in [v,u]. Both roots are vertex roots with the common separation bound. Once u-v is strictly less than that bound, they must coincide. Computing the returned profile's ordinary scalar quadratic root then yields the exact extremal value. The minimum argument uses the upper bracket endpoint and a maximizing vertex. Initialization and boundary extrema at -B or B satisfy the needed invariants.

Lexicographic minimization over the rational LP optimal face uses at most t further LPs and finishes at an original P vertex. Intermediate faces remain faces of that optimal face, so their coordinate optima have the original vertex bit bounds; successive LPs do not cause exponential encoding growth. The required bisection depth is polynomial because log(1/sep) is polynomial. No enumeration of exponentially many vertices or parametric LP bases is used.

## Exact linear-objective scenario consequence

A rational linear flow objective becomes a rational constant plus one rational coefficient per independent cycle circulation. Its optimizing endpoint is determined by that coefficient's sign, without comparison of sums of radicals. Exact original endpoint profiles now come from Section 6; rational clipped endpoints come from interpolation. Combining these profiles therefore returns an exact optimizing rational resistance scenario in polynomial time, including exact capacities. The actual optimum scalar may be a sum of independent quadratic algebraic numbers, and the draft correctly keeps its exact rational-threshold comparison outside this claim.

Apart from the corrected rational-root sentence, no gap was found in the full candidate.

## Reproducible check

I independently reran `code/potential_flow_mpd/cycle_polytope_root_recovery_checks.py`. It passed 32 correlated polytopes, 254 vertices, and 6,314 exact rational threshold bisections; all returned vertices were optimal. The small-case oracle enumerates vertices for independent comparison, while the theorem uses LP and has no vertex enumeration step.

## Possible extension, not part of this approval

The same proof appears to cover any fixed positive integer power p: sign-piece root polynomials then have degree at most p, rational target cycle equations remain linear in resistances, and fixed-degree algebraic separation can replace the quadratic separation bound. Unary-encoded growing integer p may also work, but it requires explicit polynomial factor-height and root-isolation bounds. Noninteger rational exponents should not be included by analogy: sums of shifted radicals can have degrees growing exponentially with cycle size. This extension was sent to the author and needs its own complexity check before promotion.
