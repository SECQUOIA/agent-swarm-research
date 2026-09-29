# Exact strongly convex quartic optimization with a fixed integer block

Date: 2026-09-28. Status: the complete proof, unbounded integer-polyhedron
extension, and certificate-preserving hardness padding passed
[fresh independent adversarial review](fixed-integer-strong-quartic-independent-review.md).
The continuous observable comparison dependency also passed separate
fresh review. Publication priority is unestablished.

Let \(k\) be fixed, let \(n\) vary, and let
\(f\in\mathbb Q[Z_1,\ldots,Z_k,Y_1,\ldots,Y_n]\) have degree at
most four. The input includes a positive rational \(\mu\), with the
promise

\[
             \nabla^2 f(z,y)\succeq\mu I_{k+n}
             \quad\text{for every }(z,y)\in\mathbb R^{k+n}.
\tag{1}
\]

**Theorem.** There is a deterministic algorithm, polynomial in the explicit
binary input length for every fixed \(k\), using polynomially many PosSLP
queries, that returns an integer vector \(z_*\) satisfying

\[
 \min_y f(z_*,y)=\min\{f(z,y):z\in\mathbb Z^k, y\in\mathbb R^n\}.
\tag{2}
\]

The vector \(z_*\) has polynomial bit length. All exact order comparisons
of the optimum with a supplied rational threshold, including equality,
are in \(\mathsf P^{\mathrm{PosSLP}}\). The continuous optimizer can be
specified by its polynomial-size defining system
\(\nabla_y f(z_*,y)=0\), which has exactly one real solution. No expanded
algebraic coordinates or minimal polynomials are required or promised.

The result also holds when an explicitly given rational polyhedron
restricts the integer block; it need not be bounded. The algorithm
returns an optimum or reports that the polyhedron contains no integer
point. There are no additional
constraints on the continuous block.

These are polynomial-time **Turing** reductions. The proof does not give
one PosSLP instance for the whole mixed-integer problem, or a running time
\(a(k)L^C\) with \(C\) independent of \(k\). PosSLP-hardness already
holds for the continuous case, and for every fixed positive \(k\).
Section 8 gives the latter reduction even when the input supplies a
verifiable positive definite Hessian Gram on the full monomial basis.

## 1. What the result adds to the predecessors

The integer geometry comes from Oertel, Wagner, and Weismantel,
[*Integer convex minimization by mixed integer linear optimization*](https://orca.cardiff.ac.uk/id/eprint/86766/1/IntegerConvexMinRev4.pdf),
Theorem 1 and Sections 3--4. Their fixed-dimensional algorithm combines
integer central-point queries, cuts, and flatness recursion. We implement
its value comparisons and replace its approximate normalized-gradient
interface with a simpler cut valid specifically for lattice points.
The latter needs only ordinary polynomial absolute gradient precision.

The separate [continuous observable theorem](strong-convex-quartic-posslp-upper.md)
supplies exact comparison of two fiber minima by one PosSLP instance.
This is stronger than a minimum-versus-rational-threshold oracle; the
distinction is necessary for exact incumbent comparisons.

The [primary-source audit](fixed-integer-quartic-oracle-prior.md) compares
Khachiyan--Porkolab, Heinz/Hildebrand--Köppe, and separation-oracle methods.
Fixing the total semialgebraic dimension does not cover variable \(n\).
The projected objective is not generally a polynomial, and exact
membership alone does not provide a rational strong-separation oracle.
The present proof resolves these interface issues under (1). It does not
claim a new general integer-convex algorithm.

We give the geometric algorithm below, rather than invoke the 2014
theorem without qualification. Its printed difference-body formula in
Observation 2 is false; Section 6 gives a replacement flatness computation.
We also enumerate slice levels including both endpoints, avoiding an
off-by-one error in the printed Section 3 enumeration.

## 2. A polynomial-bit bound and the projected objective

Write \(x=(z,y)\) and \(a=\nabla f(0)\). Strong convexity gives

\[
 f(x)\ge f(0)+a^{\mathsf T}x+\frac\mu2\|x\|^2.
\tag{3}
\]

The mixed-integer domain is closed and nonempty, and \(f\) is coercive.
Consequently its minimum is attained and is at most \(f(0)\). Every
point with \(f(x)\le f(0)\) satisfies
\(\|x\|\le2\|a\|/\mu\). Thus the integer box

\[
 [-R,R]^k,
 \qquad R=1+\left\lceil\frac{2\|a\|_1}{\mu}\right\rceil
\tag{4}
\]

contains every mixed-integer minimizer. Its encoding length is polynomial
in that of \(f,\mu\).

If a rational polyhedron \(Q\) constrains the integer block, fixed-
dimensional integer linear programming first returns a polynomial-bit
\(z_0\in Q\cap\mathbb Z^k\), or certifies that none exists. This
holds for unbounded polyhedra as well: see Lenstra (1983), Section 1,
the bounded-witness reduction and the constructive algorithm. Put
\(C_0=f(z_0,0)\), \(A=\|a\|_1+|C_0-f(0)|+1\), and
\(R_Q=1+\lceil2A/\mu\rceil\). For \(r=\|x\|\ge R_Q\), (3)
implies

\[
 f(x)-C_0>
 -|C_0-f(0)|+(|C_0-f(0)|+1)r>0.
\]

Thus every point of objective at most \(C_0\) lies inside that radius.
Coercivity on the closed nonempty mixed-integer feasible set guarantees
attainment. Intersecting \(Q\) with \([-R_Q,R_Q]^k\) preserves an
optimum. All quantities have polynomial bit length. The rest of the
proof therefore only needs the bounded-polytope case.

For every real \(z\), the fiber has a unique minimizer \(y(z)\). Define

\[
                   g(z)=f(z,y(z))=\min_y f(z,y).
\tag{5}
\]

Applying (1) to \((u,y(u))\) and \((v,y(v))\), then dropping the
nonnegative squared distance between the continuous blocks, shows that
\(g\) is globally \(\mu\)-strongly convex. Since
\(\nabla^2_{yy}f\succeq\mu I\), the implicit function theorem applies
to \(\nabla_yf(z,y(z))=0\). Hence \(g\) is differentiable, with

\[
                       \nabla g(z)=\nabla_z f(z,y(z)).
\tag{6}
\]

For \(n=0\), these statements mean simply \(g=f\).

## 3. An integer cut from an approximate gradient

**Integer-cut lemma.** Suppose \(g:\mathbb R^d\to\mathbb R\) is
differentiable and globally \(\nu\)-strongly convex, \(z\in\mathbb Z^d\),
and \(q\in\mathbb Q^d\) satisfies

\[
                         \|q-\nabla g(z)\|_2\le\nu/4.
\tag{7}
\]

Then for every \(w\in\mathbb Z^d\setminus\{z\}\),

\[
       g(w)-g(z)\ge q^{\mathsf T}(w-z)
                         +\frac\nu4\|w-z\|_2^2.
\tag{8}
\]

Indeed put \(r=\|w-z\|_2\ge1\). The error in the gradient term
is at most \(\nu r/4\le\nu r^2/4\), which (1) absorbs. In particular,
if \(q=0\), then \(z\) is the unique integer minimizer. Otherwise

\[
                     q^{\mathsf T}(x-z)\le0
\tag{9}
\]

contains \(z\) and every integer point no worse than \(z\); each such
distinct point in fact satisfies \(q^{\mathsf T}(w-z)\le-\nu/4\).

This is a statement about integer points. The cut can exclude points of
the real sublevel set. We never supply it to an algorithm requiring
separation of that entire sublevel. The volume argument in Section 5
works for every nonzero rational normal through its integer query, so
no comparison of approximate and exact gradient directions is needed.

## 4. Implementing both required oracles

### 4.1 Polynomial-time absolute gradient approximation

Consider a current rational quartic \(F(u,y)\), with \(d\ge1\) integer
coordinates, a supplied curvature bound \(\nu>0\), and queries
\(u\in\mathbb Z^d\cap[-B,B]^d\), where \(B\ge1\) is an integer.
Let \(m=d+n\), and let \(C\ge1\) be the sum of the absolute values
of its rational coefficients, increased to at least one. Define

\[
 D=4mC(1+B)^3,\qquad
 S=1+B+D/\nu,\qquad K=1+12mCS^2.
\tag{10}
\]

The fiber gradient at zero has norm at most \(D\). Strong monotonicity
therefore gives \(\|y(u)\|\le D/\nu\). On the unit neighborhood of
this fiber minimizer, every coordinate of \((u,y)\) has absolute value
at most \(S\). Every second partial derivative has magnitude at most
\(12CS^2\), so the operator norm of the cross-Hessian is at most
\(12mCS^2<K\).

Put \(\tau=\nu/(4d)\), \(\eta=\min\{1,\tau/K\}\), and request a
rational approximate fiber minimizer \(\widehat y\) with objective
error at most \(\nu\eta^2/2\). Ordinary convex polynomial weak
optimization supplies this point in deterministic polynomial time.
For the precise bit-model statement see Slot--Steurer--Wiedmer,
[*Hesse's Redemption*](https://arxiv.org/html/2511.03440v1), Corollary 1.2,
as checked in the continuous comparison note. The fiber is unconstrained,
convex, and attains its minimum; the logarithm of the requested inverse
error is polynomial in the current input encoding.

Strong convexity implies \(\|\widehat y-y(u)\|\le\eta\). Consequently

\[
 q=\nabla_uF(u,\widehat y)\in\mathbb Q^d,\qquad
 \|q-\nabla \min_yF(u,y)\|_\infty\le K\eta\le\tau.
\tag{11}
\]

Its Euclidean error is at most \(\sqrt d\tau\le\nu/4\), as needed
in (7). The rational output and its computation have polynomial bit
complexity. If \(n=0\), compute the gradient exactly instead.

### 4.2 Exact comparisons, including ties

For two rational integer-block vectors \(u,v\), form

\[
 H(y,y')=F(u,y)+F(v,y'),\qquad
 h(y,y')=F(u,y)-F(v,y').
\tag{12}
\]

The polynomial \(H\) is globally \(\nu\)-strongly convex. At its
unique minimizer, \(h\) equals the difference between the two fiber
minima. The continuous observable theorem reduces any specified sign
comparison of that difference to one PosSLP instance in polynomial time.
The observable has degree at most four and its encoding is included in
the reduction's input. For \(n=0\), direct rational comparison suffices.

This argument uses supplied curvature. Even when the original \(F\)
has a positive definite Hessian Gram on its full basis, the separable
\(H\) need not have one on the larger full basis. We do not assume
closure of that certificate format under (12).

The algorithm keeps a rational integer vector as its incumbent and uses
(12) only to decide whether a new vector is better. Objective values
never become coefficients of a cut, linear program, or lattice basis.
After the best integer block is found, one more continuous comparison
decides its fiber minimum against a rational threshold.

## 5. The fixed-dimensional geometric algorithm

We describe the required specialization of the Oertel--Wagner--Weismantel
algorithm to an objective with oracle (7). A recursive subproblem consists
of a rational bounded polytope \(P\subseteq[-B,B]^d\), \(B\ge1\),
and a globally strongly convex projected objective. All feasible points
in this subproblem are the integer points of \(P\).

First use integer linear feasibility to detect \(P\cap\mathbb Z^d=
\varnothing\). If \(P\) has deficient affine dimension, use the
integer affine parametrization in Section 7 and recurse immediately.
For a zero-dimensional subproblem evaluate its sole candidate. Thus
assume \(P\) is full dimensional and has an integer point. Remove
redundant inequalities, write \(P=\{x:Ax\le b\}\), and compute
\(l_i=\min_{x\in P}a_i^{\mathsf T}x\). Each facet width \(b_i-l_i\)
is positive. Solve the rational MILP

\[
 \max\ \lambda\quad\text{subject to}\quad
 Ax+(b-l)\lambda\le b,\quad x\in\mathbb Z^d,\quad\lambda\ge0.
\tag{13}
\]

It is feasible, attains its optimum \((x_*,\lambda_*)\), and has
only \(d\) integer variables. Fix \(\Lambda=1/(4d)\).

If \(\lambda_*>\Lambda\), query the projected gradient at \(x_*\),
record \(x_*\) as an incumbent if appropriate, and stop this subproblem
if \(q=0\). Otherwise intersect \(P\) with (9).

This cut preserves every remaining integer point no worse than the new
candidate. It also reduces volume by a constant depending only on \(d\).
Indeed (13) implies

\[
                  x_*+\lambda_*(P-P)\subseteq P.
\tag{14}
\]

To check (14), bound each facet functional on \(P-P\) by \(b_i-l_i\).
The difference body is centrally symmetric; each halfspace through its
center contains half its volume. Brunn--Minkowski gives
\(\operatorname{vol}(P-P)\ge2^d\operatorname{vol}(P)\). Thus either
halfspace through \(x_*\) contains at least

\[
     c_d\operatorname{vol}(P),\qquad
     c_d=2^{d-1}\Lambda^d>0,
\tag{15}
\]

of \(P\)'s volume. The removed halfspace has that volume, regardless
of the direction of \(q\). The retained volume is at most
\((1-c_d)\operatorname{vol}(P)\).

If \(\lambda_*\le\Lambda\), the inset
\(P_\Lambda=\{x:Ax+(b-l)\Lambda\le b\}\) has no integer point in
its interior: such a point would permit a larger feasible \(\lambda\).
The flatness theorem bounds its lattice width by a constant \(\phi_d\)
depending only on \(d\). This inset is full dimensional. For completeness,
John's ellipsoid theorem provides \(a+E\subseteq P\subseteq a+dE\),
with \(E\) centered at zero. Since \(P-P\subseteq2dE\),

\[
 a+(1-2d\Lambda)E\subseteq P_\Lambda,\qquad
 P\subseteq a+\frac{d}{1-2d\Lambda}(P_\Lambda-a).
\tag{16}
\]

It follows that \(\operatorname{width}(P)\le2d\phi_d\). Compute a
minimum-width nonzero integer direction \(v\) as in Section 6. Recurse
on every nonempty integer slice

\[
 P\cap\{x:v^{\mathsf T}x=t\},\qquad
 \left\lceil\min_{x\in P}v^{\mathsf T}x\right\rceil
 \le t\le
 \left\lfloor\max_{x\in P}v^{\mathsf T}x\right\rfloor.
\tag{17}
\]

Both endpoints are included. There are at most \(2d\phi_d+1\) slices.

After \(O_d(\log B)\) cuts of type (9), (15) makes the volume smaller
than one even if the small-\(\lambda_*\) case has not occurred. A
bounded convex set of volume less than one has an integer-free translate:
the average number of lattice points in its translates over a unit
fundamental box equals its volume. Translation preserves lattice width,
so flatness bounds the current width by \(\phi_d\). Again branch using
(17), with at most \(\phi_d+1\) slices. An explicit iteration budget
can be obtained from (15) and the initial bound \((2B)^d\); no real
volume computation is required.

Every branch decreases dimension. Every cut either keeps a minimizer or
discards only points worse than a retained candidate. Taking the best of
all recorded candidates and all recursive outputs is therefore exact.
There are \(O_d(\log B)\) iterations at each node and a dimension-only
branching bound, with depth at most \(k\). The precise computational
bit bounds are supplied next.

## 6. Exact flatness computation without a false difference-body formula

For a full-dimensional rational polytope \(P\), enumerate its vertices
\(p_1,\ldots,p_s\). In fixed dimension this has polynomial output and
bit complexity. For each \(j=1,\ldots,d\), solve

\[
 \min t\quad\text{subject to}\quad
 t\ge v^{\mathsf T}(p_a-p_b)\ (1\le a,b\le s),
 \quad v\in\mathbb Z^d,\quad v_j\ge1.
\tag{18}
\]

For fixed \(v\), the least \(t\) is exactly the width of \(P\) in
direction \(v\). Every nonzero integer direction or its negative has a
positive coordinate. The best of the \(d\) MILPs therefore returns a
minimum-width direction. This optimum is attained: full dimensionality
makes width a norm on directions, so a bounded-width set of integer
directions is finite.

This replaces Observation 2's erroneous assertion that symmetrizing
facet inequalities gives \(P-P\). For example, for
\(P=\operatorname{conv}(0,e_1,e_2,e_3)\), the symmetrized facet
inequalities contain \((1,1,-1)\), whereas \(P-P\) does not. The
counterexample and (18) were independently checked in the prior audit.

## 7. Lattice recursion and uniform bit bounds

A rational affine subspace can be intersected with \(\mathbb Z^d\)
by clearing denominators and solving its integer linear equations.
Hermite or Smith normal form either detects emptiness or yields

\[
                         z=z_0+Tu,\qquad u\in\mathbb Z^e,
\tag{19}
\]

where \(z_0\) and \(T\) are integral, \(T\) has full column rank,
and (19) parametrizes all integer points in that affine subspace.
These data have polynomial bit length and are computable in polynomial
time. The recursive polytope is the full inverse image of the current
\(P\), so all inherited cuts are retained.

Substitute (19) in the current quartic \(F\), keeping the continuous
variables unchanged. Degree remains at most four, and coefficient
expansion has polynomial size. If \(e\ge1\), the transformed
polynomial has the valid rational curvature lower bound

\[
 \nu'=\nu\min\left\{1,
 \frac{\det(T^{\mathsf T}T)}
      {\operatorname{tr}(T^{\mathsf T}T)^{e-1}}\right\}>0.
\tag{20}
\]

Indeed its Hessian is a congruence by \(\operatorname{diag}(T,I_n)\),
and the determinant/trace expression bounds the least eigenvalue of
\(T^{\mathsf T}T\) from below. It has polynomial bit length.
The rational left inverse \((T^{\mathsf T}T)^{-1}T^{\mathsf T}\)
and the old coordinate bounds yield a new integer box \([-B',B']^e\)
of polynomial encoding length containing the transformed polytope.

Here is why repeated cutting does not silently cause an exponential
coefficient blowup. Fix one recursion node. Its polynomial, curvature
bound, coordinate box, and inherited facets are fixed input data for
that node. Every integer query has coordinates bounded by its fixed
\(B\). Equations (10)--(11) therefore impose the same polynomial bit
bound on every new \(q\), independent of the previously added cuts.
The right side \(q^{\mathsf T}x_*\) has the same kind of bound.
There are only \(O_d(\log B)\) new cuts. Rational LP, the fixed-integer-
dimension MILPs (13) and (18), vertex enumeration, and integer normal
form computations consequently all receive and return polynomial-size
data at this node. The node's output transformations have polynomial
size as well. Composing this bound at most \(k\) times remains
polynomial for fixed \(k\). Its exponent may depend on \(k\).

The primary algorithmic source is Lenstra,
[*Integer programming with a fixed number of variables*](https://pub.math.leidenuniv.nl/~lenstrahw/PUBLICATIONS/1983i/art.pdf):
Section 2 explicitly constructs the integral affine reduction using
Kannan--Bachem normal-form multipliers, and Section 5 treats fixed
integer-dimension MILP. The existence and polynomial computation of
these multiplier matrices is also stated in Kannan--Bachem,
[*Polynomial algorithms for computing the Smith and Hermite normal
forms of an integer matrix*](https://doi.org/10.1137/0208040).
In our MILPs the only additional
continuous variable is one scalar. No high-dimensional nonlinear
subproblem is being delegated to the MILP algorithm.

Together with Section 4, these bounds establish the theorem.

## 8. Preserving a verifiable curvature certificate in the hardness reduction

Suppose a rational quartic \(f(X)\), with \(X\in\mathbb R^n\), is
supplied with a rational full-basis Hessian Gram \(M\succeq\mu_0I\),
where \(\mu_0>0\) has polynomial bit length. Such a bound follows
from \(\det(M)/\operatorname{tr}(M)^{m-1}\), with \(m\) the matrix
size. For a fixed \(k\ge1\), introduce integer variables \(z\) and set

\[
 P(X,z)=f(X)+\|z\|^2+t\|z\|^4+\|z\|^2\|X\|^2,
 \qquad t=1+\frac{8nk}{\mu_0}.
\tag{21}
\]

The additional terms are nonnegative and vanish at \(z=0\), so the
mixed-integer minimum of \(P\) equals the continuous minimum of \(f\).
All coefficients have polynomial bit length. A full rational positive
definite Hessian Gram for \(P\) can be supplied explicitly.

Write a direction as \((v_X,v_z)\), and group the full basis into
\((v_X,X\otimes v_X)\), \(v_z\), \(z\otimes v_z\),
\(z\otimes v_X\), and \(X\otimes v_z\). Keep \(M\) on the first
block, put \(2I\) on the second and the last two blocks, and put
\(4tI+8t\operatorname{vec}(I_k)\operatorname{vec}(I_k)^{\mathsf T}\)
on the third. The remaining biform is
\(8(X^{\mathsf T}v_X)(z^{\mathsf T}v_z)\), represented by the
off-diagonal block
\(4\operatorname{vec}(I_n)\operatorname{vec}(I_k)^{\mathsf T}\)
between \(X\otimes v_X\) and \(z\otimes v_z\).

For arbitrary formal vectors in those two tensor blocks, put their
Euclidean norms equal to \(U,V\). The absolute cross term is at most

\[
 8\sqrt{nk}\,UV\le
 \frac{\mu_0}{2}U^2+\frac{32nk}{\mu_0}V^2.
\tag{22}
\]

Since \(4t-32nk/\mu_0=4\), the assembled Gram is bounded below by
\(\min\{\mu_0/2,2\}I\). This is positivity on the entire formal
Gram space, not just on tensors of the form \((X,z)\otimes v\).

Apply (21) to the reviewed
[unconstrained PosSLP reduction](unconstrained-quartic-posslp-reduction.md).
Exact order comparison is therefore PosSLP-hard for every fixed integer
dimension, even in this fully verifiable certificate format. Conversely,
the certificate yields (1), so the upper theorem applies to that format.
No matching equality hardness or many-one PosSLP upper reduction is
claimed. Merely adding \(\|z\|^2\) would preserve minima and strong
curvature, but would generally lose full Gram positive definiteness;
the mixed term in (21) supplies the missing tensor blocks.

## 9. The simpler one-integer corollary

For an unconstrained integer block with \(k=1\), let \((a,y_*)\) be the
unique fully continuous minimizer.
The function \(g\) is decreasing to \(a\) and increasing after \(a\).
An integer minimizer therefore lies among \(\lfloor a\rfloor\) and
\(\lfloor a\rfloor+1\). The bound (4), followed by binary search using
the continuous coordinate comparison theorem, recovers \(\lfloor a\rfloor\)
with \(O(\log R)\) PosSLP queries. One fiber comparison (12) chooses
an optimum. An integral \(a\), and a tie between the two neighbors,
are both handled by the exact comparisons. This elementary argument is
a useful special case, not the main contribution.

## 10. Interpretation, limits, and verification

The theorem permits an arbitrary continuous block while fixing only the
integer dimension. It separates the lattice search from the potentially
large algebraic degree of continuous optimizers: the search needs
polynomial-accuracy rational gradients and exact arithmetic comparisons,
without expanding those algebraic numbers. It gives a theoretical
oracle algorithm, not an implemented solver or a numerical speedup.

Supplied global strong curvature is used in three distinct places:
bounding an optimizer, obtaining gradient accuracy from ordinary convex
approximation, and the lattice margin (8). Removing that assumption,
adding general continuous constraints, or obtaining fixed-parameter
tractability in \(k\) requires additional arguments. PosSLP-hardness
does not imply NP-hardness, and this proof gives no such claim.

The [fresh review](fixed-integer-strong-quartic-independent-review.md)
independently reconstructed the proof, including the unbounded-polyhedron
extension and the padding in Section 8. The root independently read the
complete argument as well; the root also contributed the unbounded-
polyhedron reduction and discussed the integer-cut idea, so that read
is not a substitute for the fresh review.

Targeted command actually run:

```text
python research-20260927/check_fixed_integer_quartic_oracle.py
```

It passed 600 exact coupled quadratic-fiber lattice pairs, including
303 no-worse pairs; a concrete example where the valid lattice cut
excludes a better real point; an integral coordinate change requiring
a reduced curvature modulus; 48 exact central polygon cuts; and the
width-objective and inclusive-slice checks. The reviewer separately
checked 112 successive central cuts over 24 convex-quartic examples,
with gradient errors at the allowed boundary. These finite calculations
challenge the oracle and geometric steps; they do not prove the general
algorithm or its bit bound. No Lean formalization or project-wide
verification was performed.
