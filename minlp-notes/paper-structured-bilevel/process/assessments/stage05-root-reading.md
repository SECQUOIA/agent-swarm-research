# Stage 5 root proof investigation

This is independent investigation during authorship, not stage acceptance.

## Dense scalar leader, constant gap

Root read the full scalar-leader SPD-box NP-completeness result. The ternary
leaders realize every Boolean vector with the displayed strict signs.
The upper triangular feedback bound is smaller than the own residual
margin, including the last coordinate. Auxiliary p and clause residuals
have exactly the stated conditional clipped optima; their feedback is
less than 4 eta and preserves all Boolean KKT signs. The full residual
matrix is square block lower triangular with invertible diagonal blocks,
so its weighted Gram matrix is SPD.

For any leader response, the upper objective is twice the sum of minority
amounts and clause shortfalls. Rounding at one half gives a false clause
whose literal sum is no larger than the total minority amount; distinct
clause variables are essential here and the preprocessing supplies them.
This proves the constant gap for every leader, with no extra upper row.
The exact NP certificate uses a guessed box face, a nonsingular principal
system and a rational leader interval. The ill-conditioned weights have
polynomial encoding and the joint-convex-square versus normalized-objective
distinction is correct. No substantive defect found.

## Conditioned additive approximation

Root read the full conditioned additive result, including its elementary
exact inner solver. Saturation thresholds follow from strict coordinate
derivative signs, with equality at each threshold included. On a closed
arrangement cell the unsaturated coordinates lie in cost slabs of width
R_i, while all others are fixed. The variational inequalities use the
same principal Hessian and give the correct cost-to-response estimate.

The maximum determinant row basis (after selecting independent columns)
gives barycentric coefficients at most one. Its selected cost intervals
have width at most K, regardless of large offsets or leader slopes.
Gridding only these coordinates and optimizing the direct leader cost
within each inverse image removes numerical b from the enumeration bound.
The response error with delta=epsilon/(Nr) is at most epsilon in the
required normalization. Coefficient magnitudes affect bit lengths only.

The elementary exact inner algorithm should be retained: rational
projected gradient has contraction at most 1-1/K; clearing Q and the sampled
linear term gives denominator bound B=N! H^N on every exact coordinate.
The proposed number of iterations puts the error below 1/(4B^2), including
K=1. Continued fractions then recover the unique bounded-denominator
coordinate, and exact KKT verifies the vector. Iterated rational bit lengths
grow polynomially in the allowed numerical K and input size. This closes
the exact-QP-oracle dependency within the manuscript's complexity bound.

Sent author boundary requests: N=0 and r=0 need direct treatments because
the inverse/norm/grid formulas otherwise use empty or zero quantities.
When A=0 the leader LP suffices for the objective, but a theorem promising
the exact follower vector still evaluates it at the selected leader.
Requested direct barycentric-spanner and closest box-path antecedent
attribution from the named source audits. No substantive defect found.

## Well-conditioned and arbitrarily near-identity hardness

Root read the full conditioned-hardness result and small-coupling addendum.
The feedforward ternary map stays in the unit interval on all three pieces,
its ReLU coordinates stay in [0,2], and every residual is in [0,2]. The
SAT score retains the exact zero-versus-two network gap for every leader.

The diagonal scaling makes B=S A S^{-1} small in both induced norms, so
Q=(I-B)'(I-B) has the required absolute eigenvalue bounds; its entries and
normalized linear coefficients are at most two. All scaling quantities
have polynomial rational encoding, despite tiny last-coordinate amplitudes.

The relative-coordinate calculation is valid without assuming a small
error in advance. The box KKT projection identity yields
e <= P e + U[(I+P)e+2*1], with
U=S^{-1}|B|'S=S^{-2}P'S^2. The nonnegative nilpotent inverse T=(I-P)^{-1}
has norm at most M; upper-triangular U has norm at most 2 C theta^2.
Thus the feedback norm is below one half and
||e|| <=8 M C theta^2 <=1/(16N). Multiplication by the bounded readout
delta ell' S^{-1} gives error at most delta/8 because ||ell||_1=2N.
This supplies the correct threshold separation, with log(1/delta)
polynomial, but no inverse-polynomial absolute gap.

Reducing theta to min(theta,eta/(10C)) preserves all estimates. The bound
2 eta/5+eta^2/25<eta controls both induced norms of Q-I and its spectral
norm. Strict diagonal dominance follows, while the same scaling further
shrinks the readout gap. Exactly diagonal and supplied fixed-rank positive
results remain distinct. No substantive defect found in the reduction.

## Small additional output-boundary development proposed to author

The already proved two-power binary-exponent output obstruction has a
one-power counterpart once upper polynomial data or a response constraint
are allowed. With z=x^(1/P), upper objective (z-1/2)^2 and tolerance 1/64
force 3/8<=z<=5/8, hence a positive rational x requires Omega(P) denominator
bits. Alternatively minimize affine z with row z>=1/2 at tolerance 1/8;
then 1/2<=z<=5/8 gives the same bound. The latter even has strict anchor
x=1 and convex reduced row 1/2-x^(1/P). These do not resolve the distinct
affine-objective, no-upper-row, same-power subclass. Author is independently
assessing the useful scope extension for the degree-boundary discussion.

## Growing leader dimension and leader-interaction paths

Root read the full diagonal leader-dimension note, its direct primary-source
audit, and the complete vertex-integrity result including both message
extensions. The mixed-radix table and half-grid formulas have the claimed
slopes, clipping domains and zero-versus-two continuous gap. Polynomial
duplication realizes bounded upper coefficients; the difference of TWO
scaled ReLUs is necessary to normalize a capped ramp's argument. Counts
O(k^2 n^2) and O(k^2 n^4) and parameter preservation are correct.

Root opened the actual Froese--Grillo--Hertrich--Stargalla arXiv v3 record
(September 3, 2026), Proposition 4.1 and its proof, and Corollary 5.5.
These support the direct existing parameterized/ETH boundary on bounded
boxes. The HTML piecewise spike display appears to contain a sign typo in
one left branch; its following ReLU expression is correct. The author was
alerted not to copy the typo. Our mixed-radix proof is independent.
https://arxiv.org/html/2509.22849v3

For bounded components after a fixed core, all relevant component vertices
arise from independent local threshold/bound rows with affine core RHS.
Feasible candidate evaluation is enough for soundness; the two successive
core arrangements capture every actual component minimum. Closing a cell
can omit newly feasible candidates, but it cannot invalidate the selected
leader; completeness uses the separately enumerated relative cell containing
an actual optimum. The method is XP for fixed core/component bounds, not FPT.

The path Subset Sum objective equals normalized distance to the subset sums
by telescoping and a cumulative-state witness. Its identity-Hessian ramp
realization preserves the leader path and bounded coefficients. The gap
1/W is a weak numerical reduction. Both elimination messages equal exact
distance-to-state-set functions. The varying-weight family has 2(2^n-1)
pieces; the identical-factor fixed-alphabet family has 2^(n+1)-1 including
its final increasing tail. The latter has a trivial zero optimum, so its
explicit-message output lower bound is not its NP-hardness.

## Follower-constraint paths, shadow and slab

Root read the full path obstruction and investigation, rank-one slab note
including padding, and diagonal follower bilevel note. The telescoping
identity cancels every intermediate square and makes F>=0, with zeros
exactly the original Klee--Minty endpoint vertices. Distinct terminal values
follow by backward decoding through disjoint endpoint ranges. The parabolic
exposure identity is exactly (u_n-v_n)^2 at other vertices.

The convex quadratic perturbation works on ALL feasible points by a vertex
decomposition, not just by comparing vertices. Score loss >=Delta*a and
norm-square change >=-2n*a give the positive gap with tau=Delta/(2n).
The same decomposition proves constant response intervals under
|h|<=Delta/4. Scaling to identity Hessian changes only the linear coefficients,
whose encodings remain polynomial. The weighted rounding error is <=1/8,
so the width-1/2 slab and F<=0 encode exact Subset Sum. Its NP certificate
is limited to this explicitly parameterized family. Deleting F<=0 makes
the slab feasible for all stated integer targets, by response continuity
from the zero vertex to the all-one-bit vertex. Thus the nonconvex upper
row (or nonconvex upper objective in the optimization version) is essential.

The original sparse-shadow primary paper was inspected directly: local
Gartner2013 fulltext Section 4, and original.pdf p.8 Definition 11 and
Lemma 12 visually confirm the geometric objective coefficients and signed
price witness. The original witness interval follows by a geometric series.
Backward elimination a_j=c_j-epsilon|a_(j+1)| gives linear arithmetic-time
support evaluation despite exponentially many pieces. The quantifier-free
epigraph lower bound is valid: the product of nonzero defining polynomials
must vanish on every open boundary segment, so every distinct supporting
line divides it. It only bounds total degree in the unextended variables.

## Developed fixed local-inequality alphabet for the bilevel path

Root proposed transferring the existing nonbilevel padding construction to
the diagonal/identity-Hessian bilevel theorem. Work in the FULL epsilon=1/4
cube of dimension N=n+(n-1)r, then restrict padding coordinates to <=1/2.
Each free bit pattern extends to an ORIGINAL full-cube vertex by lower
padding branches. The already proved strict convex vertex-response bound
holds for every point of the full cube, hence also its padded subset.
Use D=4^(N-1), Delta=D^-2 and tau=Delta/(2N). Every needed padded vertex
therefore remains a unique response at its parabolic exposing leader.
Conversely F<=0 forces an original endpoint vertex, and the padding bounds
force all padding branches low. The slab uses only free coordinates, so
the same Subset Sum equivalence holds. This gives fixed local inequality
coefficients and RHS while retaining large binary cost/slab data; it is
not strong hardness or a fixed alphabet for ALL coefficients. The author
is independently assessing this stronger stated bilevel corollary.

## Affine-strip projection and arithmetic boundaries

Root read the complete affine-strip path/tree/fixed-cycle-rank note. Equal
gains on both transition bounds are essential. After nonzero-gain scaling,
the bidirected tree has nonnegative two-edge excursions, so unique-path
lengths give the shortest distances. All lower-versus-upper distance tests
are necessary and sufficient; the minimum of shifted upper bounds recovers
a witness. Zero gains must be cut in their ORIGINAL orientation. A fixed
number of retained cycle-edge endpoints keeps the final dimension fixed.
Coefficient products and denominator clearing have polynomial degree/bit
growth. Dense eliminated-state objectives/aggregates and arbitrary 2VPI
polygons are excluded. Finite state bounds at a parameter do not themselves
imply global attainment.

Root read the convex-leaf arithmetic note and scalar theorem Section 6.
The singleton quadratic leaves and cubic follower responses both embed
Square-Root Sum. Cubic followers on [1,a_i+1] even have curvature >=2.
The prime-root field degree and sparse upper constraint x^(2^t)=2 concern
explicit algebraic output, not impossibility of succinct expressions or
NP-hardness. The distinct zero/negative local-curvature 3SAT examples must
state OPTIMISTIC feasibility; the same elementary clauses do not prove
pessimistic universal feasibility hard. Author was alerted.

For current arithmetic positioning root opened the primary SoCG2024
Eisenbrand--Haeberle--Singer record and abstract, DOI
10.4230/LIPIcs.SoCG.2024.54. It expressly treats polynomial-time exact
comparison as open and its improved separation constant as nonexplicit
and radicand-dependent. A primary July2026 IIT Madras seminar also retains
the unresolved status. No uniform polynomial-bit algorithm follows from
that improved bound. Author received the primary citation pointer.

## Completed draft reading before independent review

Root read the full boundary section and path appendix. The prime-root field
argument explicitly proves independent sign automorphisms and does not assume
the desired degree. The one-power output examples count rational denominator
bits and keep their upper-data restrictions distinct. The padded follower
reduction uses the full-cube strict response inequality by containment, so
additional vertices of the padded polytope do not invalidate it. The sparse
shadow edge cancellation has the claimed leading sign, and its explicit
message-size lower bounds correctly exclude compressed/extended descriptions.
The equal-gain forest proof uses original orientations for zero edges and
retains all endpoints of removed cycle edges. No additional mathematical
defect was found in this draft reading. This does not replace the forthcoming
five independent reviews of a frozen completed stage.

The author completion report was read in full before the review snapshot was
created. Root also read the focused diagnostic implementation. Its padded
vertex checks compare exact gradients against every vertex of the FULL cube,
which tests the intended restriction-by-containment argument rather than
merely evaluating selected padded vertices. Its inner-oracle checks compare
against separately enumerated rational active-face solutions. Root subsequently
reread the complete maximum-minor grid, gradient denominator recovery,
parameterized transfer, mixed-radix normalization, bounded-core closure proof,
and leader-path reduction in the completed frozen text. The exact numerical
condition/accuracy dependence, parameter dependence, and weak-gap caveats are
retained. Five independent reviews were dispatched only after author completion
and immutable snapshot creation (stage05-round01 manifest c25d5edb69e64647034e54fea863d4637e410b2a22461e8d3d378741d67fd6b5).
