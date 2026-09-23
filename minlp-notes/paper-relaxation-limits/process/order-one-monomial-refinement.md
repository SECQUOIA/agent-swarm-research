# Candidate: order-one quadratic reformulations

Coordinator derivation during Stage 4 review, 2026-09-06. This is preparation
for Stage 5, not an accepted manuscript result. Its sole author and all15
reviewers must independently check it before promotion.

The canonical bounded-monomial transfer assumes r>=2 throughout, inherited
from its unlifted cubic objective. The lifted argument appears to need only
integer r>=1 and rD>=2, provided the stated lifted objective is available
through degree2r and its polynomial pullback is F. In particular, the
pair-plus-clause quadratic formulation has a linear objective and D=3,
so its lower bound should already hold at r=1.

## Lower transfer audit

Keep every original hypothesis: originals retained; signed nonempty supports
of size at most D; all character moments in {0,+1,-1}; original moments
through degree4rD, positive on squares of degree at most2rD; clause means
satisfy every equation; objective polynomial of lifted degree at most2r
with exact polynomial pullback F. The granted quadratic moment hull is of
the full lifted coordinate domain, not its feasible graph. Localizers of
arbitrary coupled quadratic inequalities are not granted.

For a witness-containing node, fix original variables in the union C of
restricted lifted supports, then pull back the monomial map. Every required
localizer becomes a nonnegative sum of parity-indicator times square terms.
Idempotence makes I P^2=(I P)^2 in the Boolean quotient; its degree is at
most2D(deg g+deg P)<=4rD. This uses r>=1, not r>=2. The lifted first/second
moment matrix is PSD using square degree D<=2rD, and signed characters give
its actual Boolean realization exactly as in the canonical lemma. Graph
identities vanish after literal pullback at every allowed degree.

An affected clause reduces to (1-sigma*x_S)/2 with |S|<=3. Positivity of
(1+x_S)^2 and (1-x_S)^2 requires original square degree3<=2rD, hence
the integer condition rD>=2 suffices. Its pseudo-cost lies in [0,1].
No other proof step uses r>=2. The same parity-rank/support-union count
therefore gives at least2^(m*T_*/(Delta*D)) regions.

For D=3,r=1 the imported source width condition is12<=a*n. The same
bounded-occurrence family, absolute1/16 or relative1/2 target, and N<=17n
then give at least2^(7n/3072) regions at lifted order one. The unlifted
cubic theorem still requires r>=2 because its objective must be available
at degree2r. Keep this distinction explicit.

## Order-one upper certificate for the pair-plus-clause model

The canonical order-two Bernstein certificate remains a distinct proof and
must be retained. A separate elementary argument appears to prove the same
M^n upper bound at order one for the quadratic reformulation when its exact
quadratic node-box hull is granted.

Partition original coordinates into M=ceil(3/epsilon) intervals, each of
width at most h=2/M<=2epsilon/3. Keep every pair/clause auxiliary in[-1,1].
In one resulting lifted box, let a be the lower original corner. A feasible
order-one functional has its first/second moments realized by an actual
distribution mu on this full lifted box. For each ordered clause(i,j,k),
write u=x_i*x_j and v=u*x_k for its graph equations, imposed on moments.
Thus L[u]=L[x_i*x_j] and L[v]=L[u*x_k]. The realizing distribution need
not satisfy either equation pointwise.

Since all original coordinates and u have magnitude at most one, pointwise
on the full box,

    |x_i*x_j-a_i*a_j| <= |x_j-a_j|+|a_j|*|x_i-a_i| <= 2h,
    |u*(x_k-a_k)| <= h.

Taking expectations and using only the two moment graph equations gives

    |L[v]-a_i*a_j*a_k|
    <= |L[u*x_k]-a_k*L[u]| + |a_k|*|L[u]-a_i*a_j|
    <= h+2h = 3h.

The clause-cost moment is consequently at least its value at corner a
minus3h/2, for either clause sign. After averaging all clauses, every
feasible node functional satisfies

    L[linear lifted objective] >= F(a)-3h/2 >= OPT-epsilon.

The node infimum has this bound, so M^n lifted boxes certify the original
feasible graph. At epsilon=1/16, M=48; OPT>=1/8 also makes this sufficient
for relative1/2. Hence order-one lower and upper region bounds match in
exponential order for the specified strong node oracle.

This argument uses an actual distribution only to represent moments through
degree two on the entire node box. It does not assume that distribution
lies on the graph or supplies higher moments. Coordinates in a clause are
distinct, but shared or repeated clauses do not affect the per-clause bound.
No claim is made about a computationally tractable exact-box-hull oracle.

## Review and scope

Verify every degree inequality and whether any hidden r>=2 hypothesis is
used by signed realization, full graph identities, arbitrary coordinate
sets, or the source input. Verify the new order-one upper bound without
silently replacing the full-box distribution by a graph-supported one.
The source's linear width and all lift/hull conventions remain unchanged.
This is a bounded completion of an existing proof, not a priority claim.

## Coordinator supplemental audit

`verification/check_order_one_upper.py` verifies a quadratic dual expression
on 3,375 selected boxes, including singleton coordinates (216,000 exact
vertex identities/inequalities). It also solves 250 moment LPs on full-box
vertices and reconstructs their weights and graph moment equations exactly.
Of these distributions, 242 have support outside the graph and 226 attain
below the true graph optimum on the node. All satisfy the proposed bound.
This tests the distinction the proof requires, without assuming pointwise
graph equations. It is finite evidence, not a universal theorem.

Writing clause sign b and graph equations e1=u-x_i*x_j, e2=v-u*x_k, the
universal degree-two certificate can be expressed as

    q = 3h/2-b/2*[u*(x_k-a_k)+a_k*(x_i*x_j-a_i*a_j)] >= 0,
    Phi_clause-F_clause(a)+3h/2 = q-b/2*(e2+a_k*e1).

The same bounds given above prove q nonnegative on the entire lifted node
box. Its quadratic moment inequality and the two equality moments prove
the order-one bound directly. Acceptance remains pending Stage 5 review.


## Accepted Stage5 completion

The sole author, coordinator and all fifteen independent reviewers verified both results in the written manuscript. Stage5 was accepted with no findings; see stage05-round01-adjudication.md. The preceding candidate history is retained as provenance.
