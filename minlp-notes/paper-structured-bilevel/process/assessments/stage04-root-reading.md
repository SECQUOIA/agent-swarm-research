# Stage 4 root proof investigation

This records independent investigation during authorship, not acceptance.
Root read all five canonical accuracy results and both full inverse notes:
bounded powers, one resource, fixed resources, convex aggregates,
response-dependent upper data; and the positive-coefficient and general
strictly monotone polynomial inverse constructions.

## Inverse and accuracy checks

For general monotone inverses, guards must include the real parts of ALL
complex critical values, not just real critical points. The three-variable
polynomial description supplies those guards. Padding the isolated values
controls the total discarded response variation by the interpolation
modulus. On each remaining panel the critical-value-free disk provides a
single analytic inverse branch. A rational response center makes its image
and Taylor coefficients rational. The Cauchy coefficient bounds and the
explicit denominator recurrence establish polynomial bit lengths, not just
arithmetic operation counts. Positive-coefficient marginals admit the
simpler relative Rouché disk and dyadic construction. Direct bounded-power
binomial panels are a useful explicit specialization.

The binary-growing-power obstruction uses TWO powers, p and p/2, with
response objective x^(2/p)-x^(1/p). It is an output-size obstruction at fixed
accuracy, not an NP-hardness claim or a same-power example.

The one-resource proof works for signed weights because all nonzero
weighted response changes have the same sign as the multiplier changes.
Thus the weighted absolute displacement equals the resource residual. Zero
weights and the all-zero row require their stated separate treatment.
Rechecked the source's 7 epsilon/32 objective and 5 epsilon/32 value-estimate
ledgers, including rational rounding and the minimum nonzero weight.

For fixed resources, support over the nonnegative orthant gives the exact
leader feasibility projection. Extreme rays of the central arrangement,
including coordinate hyperplanes, suffice even under rank deficiency.
The integer Gram-minor constant supplies both bounded KKT multipliers and
Hoffman repair without strict feasibility. The polynomial Bregman estimate
remains valid for signed coefficients of strictly increasing marginals;
positive coefficients improve its constant. All constants need polynomial
encoding, not polynomial numerical magnitude.

For nonlinear convex aggregates, the approximate frozen aggregate gives
the additional mismatch term D rho. Retaining displacement in that term
also gives the sharper rho^(1/P) estimate when resource errors vanish.
The algorithm rounds inside the rational base polytope, not inside the
nonlinear certificate set. Its transfer argument uses the TRUE clipped
inverse response at the rounded point. Complementarity transfer must use
a bound on potentially large negative inactive slacks. Rechecked the
source's 4 S eta, 5 k Lambda S eta and 4 A eta residual allowances and
7 epsilon/64 objective budget.

Polynomial upper data have complexity polynomial in their NUMERICAL
degree. Coefficient-sum Lipschitz constants must cover approximate response
values outside [0,1]. Outer solutions allow upper-row violation and do not
decide original feasibility. Inner solutions are exactly feasible but can
be empty when the original problem is feasible. Finite posterior value
brackets require an inner feasible candidate; convergence of inner values
requires a tightening modulus. A strict point alone does not supply it.
The isolated-optimum and irrational-only-feasibility examples check out.
No c=0 shortcut is valid when upper rows depend on the response. With zero
follower variables, polynomial upper data still need polynomial optimization,
not an automatic LP shortcut.

## Developed sharper leader-response regularity

Root proposed, and the author independently developed, an improvement from
the original leader-response exponent 1/(P+1) to the sharp exponent 1/P.
The resource matrix is leader-independent; its right-hand side is affine.
The leader feasibility set is convex, and the aggregate polynomial is convex
in its aggregate argument. Let mu be the existing Bregman constant, A_x and
A_z coefficient-sum gradient Lipschitz bounds, B_b the resource right-hand
side bound, and a=K B_b.

For two optima with the same active resource and box pattern, use an
independent active-row basis to solve the change in active right-hand sides
by a row-space vector d. Gram-minor bounds give ||d||_infty <= a Delta.
The difference e of the two responses minus d is tangent to all common
active rows. Both optimal gradients belong to their row span. Consequently,
with u=||e||_infty,

    2 mu u^(P+1) <= N(A_z u + A_x Delta) a Delta + N A_x Delta u.

If u >= a Delta, division gives
u^P <= N(A_z a+2 A_x) Delta/(2 mu). Otherwise the linear bound suffices
because Delta<=1. A rational uniform constant is
C0=a+max(1,N(A_z a+2 A_x)/(2 mu)). This argument uses no strong curvature
or constraint qualification. Continuity extends it to pattern limits.

It is NOT enough to count active patterns: a pattern could recur along a
leader segment. Bound the number of its connected components instead.
Each exact pattern is the projection of the polynomial KKT system in
(t,z,lambda), with bounded resource multipliers. At most 3N+4k+2 conditions
of degree d=max(P,deg(phi),2) suffice. Replace p>=0 by p-u^2=0 and p>0 by
p u^2-1=0, then sum squares. This gives a real algebraic hypersurface of
degree at most D*=2(d+2) in at most n*=8(N+k+1) variables. Projection cannot
increase the number of connected components. Across 3^N 2^k patterns,
Gamma=3^N 2^k D*(2D*-1)^n* is a safe component bound. Their endpoints divide
the parameter interval into at most 2 Gamma+1 pieces. Sum the same-pattern
bound on these pieces to obtain C_z=C0(2 Gamma+1) and exponent 1/P.

Only this INTEGER BOUND is computed; no high-dimensional decomposition is
part of the accuracy algorithm. Its encoding is polynomial despite its
large numerical magnitude. The independent marginal g(z)=z^P with
incentive x proves that no larger uniform exponent is possible in this
class. The sharper response estimate improves the convex-anchor tightening
exponent from P+1 to P. It does not imply that reduced upper constraints
are convex merely because the follower is convex.

Root read the complete new proposition in appendices/c-quantitative-bounds.tex
and checked its tangent identity, dimensions, degree bound, interval count,
and polynomial encoding. It will receive all five independent stage reviews.

## Primary-source verification

Root downloaded and visually inspected the ORIGINAL Milnor paper:
J. Milnor, On the Betti numbers of real varieties, Proc. Amer. Math. Soc.
15(2), 275--280 (1964), DOI 10.1090/S0002-9939-1964-0161339-9.
https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Milnor1.pdf
Printed p.275, Theorem 2, gives total Betti number at most
k(2k-1)^(m-1) for real affine varieties defined by polynomial equations
of degree at most k in R^m. There is no compactness assumption. Thus the
unbounded reciprocal-square auxiliary variables pose no problem. The
manuscript uses a weaker safe exponent and only the component consequence.

A bounded primary-literature search located related general stability and
quadratic-program sensitivity work but does not establish novelty of the
sharp exponent as a general regularity statement. Do not claim publication
priority for that general principle. The explicit proof and computable
constants provide the required development for this manuscript.

## Integrated draft reading during authorship

Root subsequently read the complete section 04 and both appendices, including
the nonlinear branch validity cover and every recovery and upper-row budget.
No substantive proof defect was found on that reading. The branch sets are
closed validity preimages, which may be disconnected; they are not claimed
to be closures of nonlinear sign cells. The rational recovery explicitly
stays only in Q0 and uses true inverse continuity when leaving a branch.

Two small boundary/metadata clarifications were sent while the author was
still editing: the anchor corollary should separately give exponent one
when N=0, and the reserve corollary should explicitly require a nonempty
follower-feasible incentive set. Also requested published metadata for the
Patriksson--Stromberg allocation paper, whose preprint was cited despite an
available journal version. The publisher search record identifies EJOR
243(3), 703--722 (2015); direct publisher access returned 403, so author
verification of the DOI/institutional metadata is requested.

## Root assessment of a reviewer progress finding

Reviewer04 flagged the substitution-degree sentence in section 04: it calls
d_p the degree of the inverse branches but then bounds the degree after
composition with nonlinear arguments by D_up max(1,d_p). Root confirms a
local accounting omission if inverse branches means the univariate branches.
For example, a quartic aggregate yields argument x-4w^3; composing a
nonconstant degree-q inverse approximant gives degree 3q, even for upper
objective H=z of degree one. This does not invalidate the polynomial-time
theorem: multiply by the polynomial argument degree, or explicitly define
d_p as the degree of the already-composed p_i(v) and bound it by the product.
This is a minor mathematical accounting correction, not a major theorem gap.
No edit is made before all five reviews are assessed and a separate fixer is
assigned. Review findings will be formally disposed of in the round assessment.
