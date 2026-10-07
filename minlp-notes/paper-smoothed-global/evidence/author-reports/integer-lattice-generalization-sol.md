# Native-integer lattice extension beyond quartic unaries

Date: 2026-10-05. Author: Sol. This is supplementary mathematical
development for the authorized smoothed-exact manuscript. It preserves
the original brief and the conclusions of prewrite-lowrank-sol.md and
prewrite-two-inertia-sol.md. No literature research, experiment rerun,
historical-note edit, or author-owned TeX edit was performed.

## Conclusion

The no-fallback lattice proof extends to every fixed-degree rational
convex unary polynomial. It also extends to explicitly listed polynomial
pieces of fixed degree, with rational coefficients and rational
breakpoints, defining a globally convex continuous unary function.
The quartic degree is used only for exact polynomial-time scalar
evaluation in the historical note. Neither the objective lattice, the
semiconcave auxiliary envelope, nor the sampling/mesh compatibility uses
the number four.

More precisely, the proof needs nondecreasing forward differences on each
integer interval, exact polynomial-time unary evaluation, polynomial-height
integer values, and one polynomial-bit common denominator for those unary
values. Real convexity and continuity of the listed piecewise function
are sufficient input conditions. They are stronger than what the pure
integer proof intrinsically requires.

This is a simple extension of the supplied proof, not a researched
novelty or priority claim. The native-integer domain, separable recourse,
and aligned finite perturbation law remain material restrictions.

## 1. Precise theorem

Fix a degree bound d_* independent of input length. Let

    X = product_(j=1)^n {L_j,L_j+1,...,U_j},
    L_j,U_j in Z, L_j <= U_j,

with binary-encoded endpoints. For each coordinate, a function phi_j
on [L_j,U_j] is given by an explicit finite list of polynomial pieces
of degree at most d_* in ordinary monomial form. All polynomial
coefficients and listed breakpoints are rational. The pieces cover the
entire interval and define a continuous globally convex function there.
One polynomial is an allowed one-piece representation. Singleton
integer intervals can be evaluated directly and require no convexity
search. At shared breakpoints the listed values agree, as required by
continuity; no smoothness or equality of one-sided derivatives is assumed.

Let alpha>0 be rational, let T be any supplied rational r-by-n matrix,
and put

    G(x) = sum_j phi_j(x_j),
    F(x) = G(x)-alpha||Tx||^2/2.

No norm, rank, smallest-singular-value, or kernel promise on T is needed.
Rows may be dependent, constant on X, or zero. There is no restriction
on the number of integer coordinates. The domain is a product box;
coupled constraints are excluded.

For r=0, the objective separates and is solved deterministically by the
scalar method below. Assume r>=1 in the remaining statement. Let each
sigma_i>0 be rational and perturb the original objective to

    F_d(x)=F(x)+d^T Tx.

This is independent coefficient noise in the supplied r auxiliary
coordinates. The perturbation of the original n linear coefficients
is T^T d and is generally correlated and supported on a subspace.

Let I denote the expanded rational input length, including every listed
piece and breakpoint, all endpoints, alpha, T, and the sigma_i. If
pieces are initially supplied in shifted or factored fixed-degree form,
expand them first in polynomial time, and define the denominator budget
from those expanded coefficients. Clearing denominators from an
unexpanded expression only once may fail to clear its powered shifts.

Compute row ranges over the integer box by endpoint choices:

    l_i=min_X(Tx)_i, u_i=max_X(Tx)_i,
    A=product_i [l_i-sigma_i/alpha,u_i+sigma_i/alpha],
    w_i=u_i-l_i+2sigma_i/alpha > 0,
    s=max_i w_i.

Let Q be the product of the positive denominators of all expanded base
rational data. It may include breakpoint denominators; these are not
needed for the original value lattice but do not invalidate the budget.
Put

    D_0=2Q^3,
    M=the least power of two >= max(2,r alpha s^2 D_0),
    J=log_2 M.

Independently sample K_i uniformly from {0,...,M-1} and set

    d_i = sigma_i[2K_i-(M-1)]/(M-1).                  (1)

All budgets are computed from the base input before sampling. Each index
uses exactly J fair bits. There is an algorithm returning an exact
integer optimizer and exact rational optimum value of F_d for every
draw, including ties, without resampling or an exact fallback. Its
expected bit work is at most

    8^r H_rat P_(d_*)(I),
    H_rat=product_i [3+(1+2r)alpha w_i/(2sigma_i)],      (2)

where P_(d_*) has an absolute polynomial degree independent of r, n,
the integer interval cardinalities, and the number of pieces. Constants
can depend on the fixed degree bound. Both the integer optimizer and
its rational value have polynomial encoding length on every draw.

Thus fixed r with numerically polynomial bounds on alpha w_i/sigma_i
gives expected polynomial work. If the numerical ratios have a common
bound R, (2) has form f(r,R) poly(I) with an absolute input exponent.
Binary encoding alone does not bound the numerical ratios. The target
is the one sampled objective; the theorem does not recover the exact
unperturbed optimizer.

## 2. Exact scalar recourse, including crossings between listed pieces

For a rational auxiliary a define

    W(a)=alpha||a||^2/2
                     +min_(x in X) [G(x)-alpha a^T Tx].

The inner problem separates. In coordinate j set

    lambda_j=alpha(T^T a)_j,
    psi_j(z)=phi_j(z)-lambda_j z,
    Delta_j(z)=psi_j(z+1)-psi_j(z),
    z in {L_j,...,U_j-1}.

Global real convexity gives midpoint convexity at consecutive integers,
so the forward differences of phi_j, and therefore those of psi_j,
are nondecreasing. This remains true when z and z+1 lie in different
listed pieces. Evaluate both values using their applicable pieces;
there is no assumption that one polynomial formula covers the pair.

Binary search for the first z with Delta_j(z)>=0 returns an exact
integer minimizer. If no such z exists, choose U_j. The first
nonnegative difference satisfies Delta_j(z-1)<0 when the previous
neighbor exists; if a zero-difference interval creates a tie, the
returned first point is still a minimizer. If the whole function is
affine at the queried slope, the search returns L_j. A singleton
interval is direct.

The two available neighbor inequalities

    Delta_j(z-1)<=0 when z>L_j,
    Delta_j(z)>=0 when z<U_j

certify global optimality: summing forward differences on either side
of z shows psi_j(t)>=psi_j(z) for every feasible t. The method takes
O(1+log(U_j-L_j+1)) comparisons, rather than enumerating labels.

For each integer argument, locate the appropriate rational piece by
ordered-breakpoint comparisons and evaluate its fixed-degree polynomial
by rational Horner arithmetic. Piece lookup is polynomial in the
explicit list length, or logarithmic in that length with ordinary
binary lookup. Comparison at a breakpoint is unambiguous because the
function is continuous. The list is part of I, so neither piece lookup
nor evaluating across different pieces introduces an exponential factor.

Consequently each rational query a returns an exact value W(a) and
an attaining original integer vector x(a) in polynomial bit work in
I and the query-coordinate bit length. No general integer convex
optimization oracle is invoked. Arbitrarily many integer coordinates
cost a polynomial number of independent scalar searches.

## 3. Square completion and the original feasible gap

The recourse identity is unchanged:

    W(a)=min_X [F(x)+alpha||a-Tx||^2/2].

There are finitely many original integer points, so the minimum is
attained. W is continuous as a finite minimum of continuous functions.
Also W(a)-alpha||a||^2/2 is a minimum of affine functions and hence
concave. Thus W has upper coordinate curvature alpha on A, regardless
of the degree or size of the unaries. This envelope property does not
require derivatives of phi_j or a smooth recourse response.

Set Z_d(a)=W(a)+d^T a and C_d=||d||^2/(2alpha). Then

    Z_d(a)=min_X [F_d(x)
                 +alpha||a-Tx+d/alpha||^2/2]-C_d.      (3)

Since |d_i|<=sigma_i, all points Tx-d/alpha belong to the fixed box A.
It follows that

    min_A Z_d=min_R^r Z_d=F_d*-C_d.                   (4)

For every attaining recourse witness x(a), (3) also gives

    F_d(x(a))<=Z_d(a)+C_d.                            (5)

Therefore an auxiliary certificate L<=min_A Z_d<=U=Z_d(a) transfers to

    L+C_d<=F_d*<=F_d(x(a))<=U+C_d.                    (6)

The original feasible gap is no larger than U-L. The same C_d cancels
in that gap. Neither uniqueness of the inner witness nor a lattice for
auxiliary values is needed. All returned witnesses are original native
integer labels.

## 4. Nested cells and their deterministic certificates

At level j set h_j=s 2^(-j). In coordinate i use the smallest power
of two m_ij making h_ij=w_i/m_ij<=h_j. The subdivisions are equal
over the whole interval. They are nested; each m_ij either stays
unchanged or doubles at the next level, and m_ij<=2^j. If m_ij>=2,

    h_j/2<h_ij<=h_j.                                 (7)

An unrefined coordinate has only two endpoints and no interior grid
node. Its possibly small width needs no inverse-width estimate.

Every level-j cell has the common correction

    B_j=alpha sum_i h_ij^2/8
       <= r alpha s^2 4^(-j)/8.                       (8)

For any point in a cell, round each coordinate independently to its
two endpoints with matching mean. Coordinate semiconcavity gives
Z_d(point)>=the mean corner value minus alpha times the sum of the
coordinate variances divided by two. Each variance is at most h_ij^2/4.
Thus

    L(C)=min_corner Z_d(v)-B_j<=min_C Z_d.             (9)

Process the initial one cell and then the children of retained cells.
Query all corners exactly and keep the least auxiliary value U_j seen
so far with its recourse witness. After processing the entire level,
retain exactly the cells with L(C)<=U_j. An optimal cell always survives,
including equality on ties. With L_j the least retained lower bound,

    L_j<=min_A Z_d<=U_j, U_j-L_j<=B_j.                (10)

For the last inequality, each evaluated corner value is at least the
global incumbent U_j, so each processed L(C)>=U_j-B_j. The optimal
cell's rounding bound also gives U_j-min_A Z_d<=B_j. Consequently
each retained cell has at least one corner satisfying

    Z_d(v)-min_A Z_d<=2B_j.                           (11)

Old discarded cells stay irrelevant because the incumbent only
decreases. The stored witness associated with U_j has original gap at
most B_j by (6) and (10). This is the witness used for exact termination.
Maintaining an additional least original witness value is optional and
can only improve this guarantee.

## 5. Expected local counts under one fixed atomic law

Fix one node v of the entire deterministic level-j grid. If it is
within 2B_j of the auxiliary optimum, then in every interior coordinate
it satisfies both neighboring comparisons with tolerance 2B_j:

    W(v)+d^T v <= W(v +/- h_ij e_i)
                           +d^T(v +/- h_ij e_i)+2B_j.

The other d coordinates cancel. The two comparisons confine d_i to
an interval depending only on W and the deterministic node. Its length
is at most

    alpha h_ij+4B_j/h_ij.

For a refined coordinate, (7) gives

    4B_j/h_ij=(alpha/2) sum_l h_lj^2/h_ij
              <=2r alpha h_ij,

so the length is at most (1+2r)alpha h_ij. An unrefined coordinate
has no interior comparison and contributes at most one per endpoint.

Under (1), a scalar interval of length ell has probability at most

    ell/(2sigma_i)+1/M.

Independence multiplies these necessary-event probabilities over
interior coordinates. Summing over the entire tensor grid gives an
expected 2B_j-near-optimal node count at most

    product_i [2+(m_ij-1){(1+2r)alpha h_ij/(2sigma_i)+1/M}]
    <= product_i [2+(1+2r)alpha w_i/(2sigma_i)
                                                  +(m_ij-1)/M].

Because M=2^J and m_ij<=2^j, every j<=J obeys m_ij<=M. The bound
is therefore at most H_rat in (2), uniformly over all levels actually
used. In particular, ties at atoms are not removed from the law and
do not require a favorable growth event.

By (11), each retained cell has a near-optimal corner. A corner belongs
to at most 2^r cells, so the expected number of retained cells at each
level is at most 2^r H_rat. A retained parent generates at most 2^r
children, each with at most 2^r corner queries. Hence the expected
number of recourse evaluations through level J, without corner caching,
is at most

    2^r+8^r H_rat J.                                 (12)

The count uses the full deterministic level grid only as a proof device.
The algorithm visits its adaptive subset. No independence of retained
cells or of their selected corners is assumed. Polynomial piece degree
and the number of integer coordinates never enter this exponential
count; they affect only the polynomial cost of an exact query.

## 6. Original objective lattice and termination without fallback

Every expanded polynomial coefficient has denominator dividing Q.
At an integer argument, every monomial is an integer. Regardless of
which piece applies,

    phi_j(x_j) in Q^(-1) Z,
    G(x) in Q^(-1) Z.                                (13)

Rational breakpoints determine piece selection; they introduce no new
denominator into an integer value. If adjacent pieces agree at an
integer breakpoint, either evaluation obeys (13).

Since alpha and every entry of T have denominator dividing Q,

    alpha||Tx||^2/2 in (2Q^3)^(-1) Z.                 (14)

The perturbation term is

    d^T Tx=sum_(i,j) sigma_i[2K_i-(M-1)]T_ij x_j/(M-1),

and belongs to [Q^2(M-1)]^(-1)Z. Combining (13)--(14) gives

    F_d(x) in [D_0(M-1)]^(-1) Z for every x in X,
    D_0=2Q^3.                                        (15)

The same M in all noise coordinates is essential to this particular
simple denominator bound. The finite optimum F_d* is one of these
values and lies in the same lattice.

The base-only selection of M gives at the predetermined level J

    B_J <= r alpha s^2/(8M^2)
         <=1/(8D_0 M)<1/[D_0(M-1)].                  (16)

Return the stored integer witness x_inc associated with U_J. Equations
(6), (10), and (16) imply

    0<=F_d(x_inc)-F_d*<=B_J<1/[D_0(M-1)].

Both values are on (15), so they are equal. The algorithm terminates
at J on every draw. It never needs an exceptional-event fallback, a
global growth modulus, or a unique optimum.

The auxiliary corner values and the constant C_d may have much finer
denominators, including a factor (M-1)^2. Those values establish the
real inequality (6) and are not used for exact lattice recovery. Using
an auxiliary-value lattice in place of (15) would introduce a false
precision obstacle. The degree of an integer unary introduces no
additional sampling denominator.

## 7. Uniform bit-height and work bounds

The bit length of the product Q is at most the sum of the expanded
input denominator lengths, hence log D_0=O(I). Row extrema are sums
of rational entries of T times binary integers, with polynomial bit
length. Dividing sigma_i by the nonzero rational alpha and taking a
largest width preserve polynomial bit length. Thus the positive
rational r alpha s^2 D_0 has polynomial logarithmic magnitude, and

    J=log_2 M=poly(I).

The algorithm computes the least sufficient power of two by rational
comparison; it does not enumerate M support points. Sampling uses rJ
fair bits, and the rational perturbation coordinates have polynomial
length in I+J.

Every feasible integer label has input-bounded binary length. For an
integer z of B bits and degree at most d_*, its powers z^t have at
most tB+O(1) bits. A rational piece evaluation has polynomial numerator
and denominator length in I+B, with constants depending on d_*.
The number of scalar binary-search comparisons is polynomial in I,
because log(U_j-L_j+1) is at most a constant times the endpoint bit
length. Rational breakpoint comparisons use ordinary exact integer
products of polynomial length. These statements also cover negative
integer arguments, constants, affine pieces, and knots.

At any j<=J, a mesh corner is an auxiliary endpoint plus an integer
index times w_i/m_ij. Its coordinates have polynomial length in I+j.
The quantities alpha(T^T a)_j, every recourse comparison, W(a), Z_d(a),
the correction B_j, and the original objective at the stored witness
therefore have uniformly polynomial length. Sums involve only a
polynomial number of rationals per query. No denominator products
accumulate across unrelated oracle calls: incumbents are selected by
comparison, and new corner instances use base data and the current
mesh directly.

All addresses and tree indices have length O(rJ). Even a draw retaining
exponentially many cells has polynomial bit cost per cell; the expected
number of cells is controlled by (12). Multiply (12) by the polynomial
query and bookkeeping cost, and absorb J, sampling, and initialization
into P_(d_*)(I). This proves (2) with an absolute input-polynomial
degree independent of r. The output integer vector has input-bounded
length, and (13)--(15) plus the fixed-degree evaluation bound give a
polynomial-height exact rational output value.

The same predetermined M has two roles: it makes (m_ij-1)/M bounded
through J and makes the final original gap smaller than its objective
lattice spacing. The value lattice is linear in M-1 while B_J is
quadratic in 1/M. This is why the proof has no sampling/termination
precision circle and needs no rare-draw solver.

## 8. Assumptions actually used and manuscript boundaries

The theorem can be stated abstractly for unary functions on consecutive
integer labels if the input supplies:

1. Nondecreasing forward differences on each interval, or a promise
   implying them.
2. An exact polynomial-bit evaluation method at binary integer labels.
3. A computable common unary-value denominator of polynomial bit length,
   with uniformly polynomial numerator height.

In such an abstract version, include the supplied common unary-value
denominator in Q, together with the rational quadratic/noise data.
The listed convex fixed-degree piecewise-polynomial model supplies all
three. Continuity at rational breakpoints makes the represented function
unambiguous; global real convexity supplies discrete convexity. The
proof does not use a derivative at a knot, fixed positive curvature,
quartic parity, nonnegative polynomial coefficients, or a full-rank
factor.

The degree restriction is not algebraically needed for (15). It ensures
the elementary evaluation/height premise for the stated input model.
Other encodings can also satisfy that premise, but a succinct binary
exponent or arithmetic-circuit encoding does not automatically do so:
even evaluating z^(2^b) at z=2 produces an exponentially long integer.
Do not extend the polynomial bit claim to such representations merely
because coefficients are rational. No new theorem about arbitrary
succinctly represented unary functions is asserted here.

The current task assumes convexity. Checking that an arbitrary supplied
piece list is globally convex is a separate input-validation question;
the optimization theorem can state a convexity promise. If validation
is included, it must verify continuity, convexity on every piece, and
ordered one-sided derivatives at knots. Testing only each piece's
curvature would miss downward derivative jumps between individually
convex pieces.

Pure native-integer feasibility is essential to exact recovery in this
argument. Continuous polynomial coordinates can have irrational minima
and do not satisfy (15). Coupled constraints prevent the separable
binary-search oracle. Noise is aligned to the supplied factor; no
independent ambient Gaussian theorem follows from this extension.
Arbitrarily finer refinement under an externally imposed coarse noise
grid is also not covered by the expected-count proof.

The unperturbed problem can remain hard or have an unfavorable numerical
ratio. This theorem is for its sampled objective under (1), and makes
no worst-case tractability, practical performance, or priority claim.
Binary and explicitly listed-label fixed-rank baselines discussed in
the original note continue to apply: increasing the unary degree does
not alter their easy-case boundary. The useful contract still permits
long binary-encoded intervals without enumerating their labels, under
the numerical dependence in (2).

## 9. Targeted verification record

I read smoothed-integer-low-rank.md and both original independent reviews.
I re-derived the scalar crossing-piece oracle, objective denominator,
mesh/noise compatibility, primal gap transfer, and levelwise expectation
analytically. The only filesystem changes are this authorized report and
its destination directory. No computational experiment or original
diagnostic was rerun. No literature research, project-wide verification,
CI inspection, or author-owned manuscript edit was performed.

A scoped `python -` read this report alone and checked its final newline,
absence of trailing whitespace, paired code fences, and the denominator,
mesh, no-fallback, and cross-piece theorem markers. It passed before this
verification paragraph and the abstract denominator clarification were
appended. No solver or arithmetic diagnostic was executed.
