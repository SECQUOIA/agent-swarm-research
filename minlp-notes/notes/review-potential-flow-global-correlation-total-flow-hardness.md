# Independent review: total-flow hardness under global resistance correlation

Date: 2026-09-05. Reviewer: `benders_property`. Status: PASS.

Reviewed [the full reduction](potential-flow-global-correlation-total-flow-hardness.md), including the actual-edge resistance polytope, strong numerical bounds, restricted NP/coNP membership, and rational near-optimal scenario output. The Max-Cut and convex-maximization mechanisms are classical; this review verifies the passive-network scope and exact reduction.

## Triangle physics and scalar constants

For a triangle with each of its two path edges having resistance r and its direct edge resistance two, the unit-through-flow equation is `2*r*f^2=2*(1-f)^2`. Its unique positive split is `f=1/(1+sqrt(r))`. The total of its three positive edge flows is 1+f. Thus the paired construction has exactly the stated dependence on delta, with no missing factor from the two path resistances.

The displayed second derivative of f is correct and positive for r>0. Hence psi is convex and even. At binary theta, the uncut and cut values are respectively `A=2*sqrt(2)-2` and `B=sqrt(3)/2`. The rational square bounds establish `kappa=B-A>7/200>1/32`. All long-path and direct flows are strictly positive throughout the whole parameter cube, not merely at its vertices.

## Graph and actual resistance encoding

The 2m disjoint triangles have 6m vertices and 6m edges. Joining successive exits and entrances adds 2m-1 edges without identifying vertices. Adding n bridge edges before the first entrance adds n new vertices. Thus the proposed totals `6m+n` vertices, `8m-1+n` edges, and cycle rank 2m are correct. Entrance and exit vertices have degree at most three; other vertices have degree at most two. The graph is connected, simple, cactus, and admits the displayed directed acyclic orientation.

The only nonzero nominations are +1 at the first source and -1 at the final sink. Every bridge then carries one, and every triangle carries unit through-flow. The added n bridges change only the additive objective constant and provide actual resistance coordinates `r_i=1+theta_i`. Their presence makes the parameterization injective. All remaining uncertain resistances are affine expressions `2+r_i-r_j` or `2-r_i+r_j` in these actual edge coordinates. The resulting polytope is exactly an injective affine image of the cube; its vertices correspond to binary theta. Bounds [1,3], fixed resistance two, and bounded integer correlation coefficients hold as stated.

Summing all edge flows gives `4*m-1+n+sum psi`. The bridge resistances do not affect those bridge flows or the unit demand seen by each triangle. Since all arc flows are positive, this objective also equals the sum of their absolute values with unit coefficient on every edge.

## Optimization and threshold gap

Convexity of each psi composed with theta_i-theta_j makes the total a convex function on the cube. Expressing a cube point as a convex combination of its vertices shows that some binary point is at least as good. At a binary point the value is exactly `C+kappa*cut_size`. This proves the exact optimum identity; there is no approximation in the reduction's physical or combinatorial part.

For 1<=K<=m, the coefficients of A and B in Q are nonnegative, sum to m, and are O(m). If each square root is approximated within `w=1/[8192*(m+1)]`, the induced errors in A and B are at most 2w and w/2. Therefore Q's error is at most 2mw, substantially below 1/512. Choose the dyadic denominator by rounding up the required bit precision; it is at most `16384*(m+1)`, so it is O(m). After the fixed half factors, the threshold denominator remains O(m), and its numerator is polynomial in m+n.

The half-cut gap is greater than 1/64. Subtracting the allowed threshold error gives a strict gap greater than 7/512 on both sides. Thus weak attainment `OPT>=tau` encodes the yes answer and robust satisfaction `T<=tau` encodes the no answer, with no equality ambiguity in the reduction. All numerical data have polynomial unary encoding length: edge data and correlation coefficients are constant, while the threshold numerator and denominator are polynomially bounded. This establishes the asserted strong hardness.

## Membership and output semantics

On this restricted family a maximizing scenario may be chosen at binary theta, giving integer resistances and an n-bit certificate. Its objective depends only on its integer cut size and lies in the fixed field Q(sqrt(2),sqrt(3)), of degree at most four. Exact comparison with any rational threshold is polynomial. This proves NP membership for weak attainment and NP membership for the complement of robust upper satisfaction. The resulting NP/coNP completeness claims are correctly restricted to this family; arbitrary sums of roots on general correlated cacti are not covered by this certificate argument.

Absolute value error at most 1/256 is smaller than the reduction gap, so it decides the source after comparison with tau. For a rational near-optimal scenario, the yes case remains above tau+5/512 after its performance loss, while every no-case scenario stays below tau-7/512. Separate quadratic-root approximations totaling error at most 1/512 preserve the distinction. A polynomial-time rational-output algorithm has polynomial output bit length, which suffices for this evaluation. No exact comparison of its arbitrary radical sum is needed.

The statement properly avoids fixed relative-error or objective-normalized hardness. Its constant absolute gap uses neither nomination scaling nor large resistance or objective coefficients.

## Independent checks

I independently checked four symbolic identities: the triangle pressure equation, f's second derivative, and the two expressions for A and B. A separate graph construction checked 35 combinations with 2<=n<=6 and 1<=m<=n(n-1)/2, verifying the vertex/edge counts, connectedness, acyclicity, maximum degree, cycle rank, and cactus blocks. Exact rational arithmetic checked the square bounds and threshold-gap constants. All checks passed.

No correction was required.
