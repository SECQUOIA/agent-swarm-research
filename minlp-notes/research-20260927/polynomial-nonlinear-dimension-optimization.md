# Exact convex polynomial optimization with few nonlinear directions

Date: 2026-09-28. Status: complete proof with a
[fresh full adversarial review](polynomial-nonlinear-dimension-optimization-review.md)
that found no remaining gap, conditional on the separately reviewed
dependencies below. The selected-point degree and height argument has a separate
[bounds audit](polynomial-nonlinear-dimension-witness-review.md). This note
uses the reviewed [polynomial feasibility theorem](polynomial-nonlinear-dimension-frontier.md)
and [general convex semialgebraic value theorem](unbounded-misocp-multiple-integer-frontier.md#22-general-convex-semialgebraic-value-theorem).
Novelty and practical usefulness remain to be established.

## 1. Model and result

Consider

\[
 \begin{split}
 \min\quad &q_0(z,u,v)=C_0v+p_0(z,u),\\
 \text{subject to}\quad &C_iv+p_i(z,u)\le0\quad(1\le i\le m),\\
 &z\in\mathbb Z^k,\qquad u\in\mathbb R^r,
       \qquad v\in\mathbb R^n.                         \tag{1}
 \end{split}
\]

Every \(p_i\), including \(p_0\), is a rational polynomial globally
convex in the joint variables \((z,u)\), of degree at most \(d\).
The row vectors \(C_i\) are rational and constant. Affine inequalities
and equalities are allowed; each equality is represented by two affine
weak inequalities. Coefficients and monomials are explicitly encoded.
Let \(N\ge2\) be total binary input length and \(D=\max(2,d)\).

The objective's nonlinear continuous directions are included in the same
\(r\)-dimensional core as the constraints. The remaining continuous
dimension \(n\), the row count, and their linear coefficients are
unrestricted parts of the input. Convexity is an assumption on the supplied
polynomials; the algorithm need not recognize it.

**Theorem.** There is an algorithm with bit cost

\[
                          f(k,r,d)N^C,                    \tag{2}
\]

where \(f\) is computable and \(C\) is an absolute constant, that
classifies (1) as infeasible, unbounded below, or having a finite attained
minimum. In the finite case it returns the exact minimum \(\theta\),
an optimal integer vector \(z^*\), and an exact algebraic continuous
optimizer \((u^*,v^*)\).

The tuple \((\theta,u^*,v^*)\) can be returned in one number field of
degree at most \(g(r,d)\), using a primitive integer irreducible
polynomial, a rational isolating interval, and rational coordinate
polynomials. Its total output length, and the bit length of \(z^*\),
are at most \(f(k,r,d)N^C\). No variable bounds, strict feasible point,
or rational continuous feasible point need be supplied.
The integer dimension affects the time and height bounds, but not this
field-degree bound. If \(r=0\), the returned value and continuous
optimizer can be rational.

Finite attainment is a classical fact for this class, not an additional
claim of originality. The candidate addition to the feasibility result is
full exact optimization and algebraic output with the same parameter set
and an absolute input-size exponent. The proof obtains a uniform optimizer
box; it does not enumerate the potentially exponential projected row family.

### 1.1 Intrinsic form and an application family

For an original convex polynomial formulation in \((z,x)\), compute
the common kernel of all polynomial Hessians on continuous directions,
**including the objective Hessian**. The coefficient identities and rational
coordinate change in Section 1.1 of the feasibility note produce (1) in
\(f(k,r,d)N^{O(1)}\) time. For globally convex polynomials, the continuous
Hessian blocks suffice: a vector of zero quadratic form for a positive
semidefinite Hessian belongs to its full kernel. This rules out variable
coefficients on the eliminated linear variables.

One model covered by (1) combines many linear flow or allocation variables
\(v\), a small integer design vector \(z\), and aggregate features
\(u=Fv+Gz\). Convex higher-moment bounds can take the form

\[
 \sum_s w_{is}(a_{is}^Tz+b_{is}^Tu+c_{is})^{2e_i}
                         +c_i^Tv\le\tau_i,
       \qquad w_{is}\ge0,\quad 2e_i\le d.               \tag{3}
\]

The objective may have the same form plus linear cost. Each even power of
an affine function is globally convex. Expanding these sums into explicit
monomials costs \(f(k,r,d)N^{O(1)}\), because only \(k+r\) variables
occur nonlinearly. The theorem therefore permits the linear model and
scenario count to grow while these parameters stay fixed. It could support
exact certification for such models. It does not establish that real
applications have small parameters, that the constants are practical, or
that an implementation would improve current solvers.

## 2. Quantitative and qualitative ingredients

We use three previously established inputs, keeping their roles separate.

1. **Exact rational feasibility.** The linked polynomial feasibility theorem
   decides systems (1) in \(f(k,r,d)N^{C_0}\) time and returns a feasible
   original integer vector. Appending a rational objective threshold,
   coordinate boxes, or \(\|u\|^2\le a\) preserves its form, with degree
   at most \(D\). Its proof supplies an absolute exponent for coefficient
   bits, including after lattice restrictions. This coefficient-sensitive
   property is essential here.
2. **Convex semialgebraic values.** Section 2.2 of the linked value theorem
   bounds a finite mixed-integer infimum for any upward-closed convex
   epigraph in \((z,t)\). If its quantifier-free atomic degrees are at
   most \(a\) and individual coefficient bits at most \(H\), the finite
   value has degree \(a^{G(k)}\) and coefficient bits
   \((H+1)a^{G(k)}\). Some optimal integer vector has the latter bit
   bound when the value is attained. These bounds do not depend on the
   number of atoms. The theorem is used for bounds, not to construct that
   description or execute an algorithm on it.
3. **Finite attainment.** Bank--Mandel's 1987 Theorems 3(iii) and 7(ii)
   imply that the right-hand-side feasibility domain of a rational,
   globally quasiconvex polynomial mixed-integer system is closed. Append
   the rational convex objective as one more row and let its right-hand
   side decrease to a finite infimum. Closedness gives an optimizer.
   Rationality supplies the integer-generated recession condition for the
   stable subsystem. The relevant primary statements and definitions were
   inspected in the [publisher preview](https://api.pageplace.de/preview/DT0400.9783112720936_A50662169/preview-9783112720936_A50662169.pdf),
   printed pages 20, 24, and 34; the deduction is detailed in the
   [attainment prior audit](mixed-integer-attainment-prior.md).

The third input is valid without fixing \(k,r,d\). It removes a
nonattainment branch for (1). The general value theorem is stronger than
needed in that respect, but remains useful for its effective arithmetic
bounds. Its geometric argument, and the feasibility oracle itself, retain
their separate independent reviews.

We also use coefficient-sensitive real quantifier elimination. In a fixed
number of free and quantified variables, individual output polynomial
degrees depend on the input degree and block sizes, and individual output
coefficient bits are linear in the input coefficient bits up to such a
factor. They do not depend on the number of input predicates; output count
and running time do. See [Basu's survey, Theorem 2.27](https://arxiv.org/abs/1409.1534),
and the primary framework cited there. Only these arithmetic bounds are
used on exponential descriptions. The independent bounds auditor inspected
the full displayed integer-coefficient statement.

## 3. The value and an optimal integer assignment have FPT encoding bounds

Introduce a real threshold \(t\), and eliminate \(v\) from

\[
 C_iv+p_i(z,u)\le0\ (1\le i\le m),\qquad
                   C_0v+p_0(z,u)\le t.                  \tag{4}
\]

Its matrix on \(v\) is constant and rational. Normalize the nonnegative
Farkas multipliers by requiring their sum to be one. Its extreme points
give an exact finite family

\[
                P_j(z,u,t)\le0\quad(1\le j\le S).       \tag{5}
\]

If the normalized dual polytope is empty, the family is vacuous. Every
projected row is a nonnegative combination of rows in (4), so it is convex.
Rational minor bounds give

\[
 \deg P_j\le D,\qquad
 \operatorname{bits}(P_j)\le N^{C_1},\qquad
                         \log(S+1)\le N^{C_1}.           \tag{6}
\]

Clear denominators separately in each row by a positive multiplier. No
common denominator over all \(S\) rows is required. Exactly as in the
feasibility proof, adding \(L\)-bit rational data changes the individual
coefficient bound by a fixed polynomial in structural size times \(L+1\).

Quantify the \(r\) variables \(u\) in (5). This describes the convex,
upward-closed epigraph

\[
 E=\{(z,t):\exists u,v\ ((z,u,v)\text{ is feasible},
                                        q_0(z,u,v)\le t)\}. \tag{7}
\]

Quantifier elimination gives an equivalent formula in \(k+1\) free
variables with atomic degrees at most \(f(k,r,d)\) and individual
coefficient bits at most \(f(k,r,d)N^{C_1}\). This is an existence and
height statement; no formula is constructed. Applying the general value
theorem yields computable bounds

\[
 \deg M_\theta\le A:=g(r,d),\qquad
 \operatorname{bits}(M_\theta)\le L:=f(k,r,d)N^{C_2}.       \tag{8}
\]

Here \(M_\theta\) is the primitive integer minimal polynomial of any
finite optimum. The general theorem first bounds its degree by
\(f(k,r,d)\). To obtain the stronger degree in (8), fix any optimal
integer \(z\), which exists by classical attainment. Substitute it
into (5). The remaining epigraph has variables \((u,t)\) and degree
at most \(D\). Quantifier elimination over the \(r\) variables
\(u\) leaves univariate atoms of degree at most \(g(r,d)\), regardless
of the integer vector's size. Its finite endpoint \(\theta\) must
annihilate a nonzero output polynomial, since otherwise all atom signs
would be constant near that endpoint. This proves the degree refinement;
the uniform height bound still comes from the general value theorem.
For \(r=0\), this fiber is a rational linear program, so its finite
value is rational.

The same general value theorem gives a uniform integer \(B_z\ge1\)
with

\[
 \operatorname{bit}B_z\le f(k,r,d)N^{C_2},\qquad
 \text{some optimal }z\text{ lies in }[-B_z,B_z]^k.        \tag{9}
\]

The optimum exists by the classical attainment result. Alternatively, the
integer-vector bound follows by selecting \(\theta\) with (8) and a
short rational isolating interval, then applying Khachiyan--Porkolab's
integer witness bound to its convex optimal projection. The isolating
interval has at most \(f(k,r,d)N^{C_2}\) bits by root separation. This
argument is not an algorithm on an exponentially large formula.

The factor multiplying \(N^{C_2}\) may grow rapidly with the parameters.
The point is that \(C_2\) is absolute: quantifier elimination and the
general value theorem multiply coefficient lengths by parameter factors;
they do not raise those lengths to parameter-dependent powers.

## 4. Status and exact value use only rational feasibility queries

First test feasibility by the existing oracle. Suppose the answer is yes.
The root bound applied to (8) gives a computable integer \(M\ge1\),
with \(\operatorname{bit}M\le f(k,r,d)N^{C_3}\), such that every
finite optimum obeys \(|\theta|<M\).

Ask whether the original, unbounded model has a point with

\[
                         q_0\le -M-1.                    \tag{10}
\]

If yes, the optimum cannot be finite, so the objective is unbounded below.
If no, feasibility and the definition of infimum imply a finite optimum.
This query uses the original model; imposing a box known to contain some
finite optimizer would not justify an unboundedness test.

For a finite optimum, bisect \([-M,M]\). At rational \(a\), the query
\(q_0\le a\) is a convex polynomial row using the same nonlinear core.
It answers whether \(\theta\le a\), because finite attainment holds.
Even without that fact, keeping the lower endpoint after a negative answer
would still produce valid shrinking intervals around an infimum.

Use (8) and certified Kannan--Lenstra--Lovasz algebraic recognition to
recover the exact \(\theta\). Degree and height bounds require only
\(f(k,r,d)N^{C_4}\) approximation bits, queries, and total bit operations
after increasing the absolute constant. Return the minimal polynomial and
a rational isolating interval. This is certified recognition with proved
bounds, rather than a heuristic integer-relation computation. The imported
recognition method and its exact arithmetic conventions are recorded in
[common-field recovery](constructive-common-field-recovery.md).

The same procedure is a **value subroutine** for any rational instance
obtained by appending a fixed-size template of rational boxes, affine
integer restrictions, and at most one norm row \(\|u\|^2\le a\).
Its degree remains at most \(D\), and its nonlinear core is unchanged.
If the appended numbers use at most \(p\) bits, its bit cost is

\[
                    f(k,r,d)(N+p+1)^{C_5}.                \tag{11}
\]

Here the number of box rows is allowed to be linear in the number of
original coordinates. Their bits are part of the input; no exponent
depends on that dimension or on the parameters.

## 5. A uniform box contains canonical optimal points

We now prove a stronger form of the box needed for recovery. For every
optimal integer \(z\) in (9), there is a specified optimal continuous
pair \((u^*,v^*)\) with the bounds below, uniform over those \(z\).
Neither the definition nor the arithmetic proof enumerates the integers.

Fix such a \(z\). Write \(Q(u,s)\) for the Farkas description (5)
after substituting \(z\), with threshold variable \(s\). Then

\[
 U_\theta=\{u:Q(u,\theta)\}
     =\{u:\exists v\ ((z,u,v)\text{ feasible},\ q_0\le\theta)\}
                                                               \tag{12}
\]

is nonempty, closed, and convex. Closedness follows from its finite weak
polynomial description, using the constant eliminated matrix. It is not
inferred from the false general assertion that projections of closed
convex sets are closed. Thus it has a unique minimum-norm point

\[
                         u^*=\arg\min_{u\in U_\theta}\|u\|^2.
                                                               \tag{13}
\]

Let the rational interval \((a,b)\) isolate \(\theta\) as a root of
\(M_\theta\). For a free scalar \(t\), the formula

\[
 \begin{split}
 \exists s\,\exists u\;[&M_\theta(s)=0\ \wedge\ a<s<b
       \ \wedge\ t=u_i\ \wedge\ Q(u,s)\\
 &\wedge\ \forall w\bigl(Q(w,s)
           \Longrightarrow \|u\|^2\le\|w\|^2\bigr)]       \tag{14}
 \end{split}
\]

defines exactly the singleton \(\{u_i^*\}\). Its quantified block
sizes are \(r+1\) and \(r\). Its degrees are bounded by \(g(r,d)\),
and its individual coefficient lengths are
\(f(k,r,d)N^{C_6}\), including the substituted integer and the value
isolator. Quantifier elimination gives a nonzero univariate polynomial
vanishing at \(u_i^*\) with bounds of the same form. Otherwise all
nonconstant signs in the output would be constant in a neighborhood,
contradicting the singleton property. Passing to a minimal-polynomial
factor preserves these bounds.

Therefore every \(u_i^*\) has degree at most \(g(r,d)\) and
minimal-polynomial coefficient bits at most \(f(k,r,d)N^{C_6}\).
Include the value in the common field:

\[
                    K=\mathbb Q(\theta,u_1^*,\ldots,u_r^*).
                                                               \tag{15}
\]

The product of the \(r+1\) individual degree bounds still depends only
on \((r,d)\), giving \([K:\mathbb Q]\le g(r,d)\). We do not
multiply degrees over the \(n\) eliminated coordinates.

At \(u=u^*\), the original rows and the objective upper row form a
nonempty polyhedron

\[
 Av\le b^*,\qquad
 A=\begin{pmatrix}C\\C_0\end{pmatrix},\qquad
 b^*=\begin{pmatrix}-p(z,u^*)\\\theta-p_0(z,u^*)\end{pmatrix}.
                                                               \tag{16}
\]

Let \(v^*\) be its unique minimum-norm point. The normal-cone condition
and conic Caratheodory give a linearly independent set of active rows
\(I\) for which

\[
                  v^*=A_I^T(A_IA_I^T)^{-1}b_I^*.           \tag{17}
\]

For \(v^*=0\), use the empty set. The rational matrix in (17) has
polynomial coefficient bits by minors. Thus every coordinate of \(v^*\)
is in the existing field \(K\).

For the height bound, let \(D_0\) be the product of leading coefficients
of the minimal polynomials of \(\theta\) and all \(u_i^*\).
Multiplication by \(D_0\) makes these numbers algebraic integers.
Polynomial evaluation of degree at most \(d\) and the objective's linear
\(\theta\) term are cleared by \(D_0^D\). Clear also the rational
denominators of the polynomial coefficients and the matrix in (17).
Coordinate root bounds control every conjugate, not
just the chosen real embedding. A field norm then gives an integer
annihilator for each \(v_j^*\), of degree at most \([K:\mathbb Q]\)
and coefficient bits \(f(k,r,d)N^{C_7}\). Products of polynomially many
rational denominators add their bit lengths; they do not multiply the
degrees of the algebraic coordinates.

Cauchy root bounds now give a uniform rational \(R\ge2\) with

\[
 \operatorname{bit}R\le f(k,r,d)N^{C_8},\qquad
                \|(u^*,v^*)\|_\infty<R                 \tag{18}
\]

for every optimal \(z\) in (9). The bounds used above are uniform in
its bits, so \(R\) is computable without locating a particular integer
optimizer or continuous point. When \(r=0\), (14) is unnecessary;
the field in (15) is \(\mathbb Q(\theta)=\mathbb Q\), so (17) is
rational. When \(n=0\),
the affine fiber step is empty.

## 6. Choose an optimal integer assignment inside one compact box

Fix, once and for all, the original rows and the box

\[
             |z_j|\le B_z,\qquad |u_i|\le R,\qquad |v_j|\le R.
                                                               \tag{19}
\]

Its mixed-integer feasible set is compact and contains an optimizer of
the original model. For any additional rational closed constraints
\(G\) of the allowed form,

\[
 \begin{split}
 &\text{the optimal set in (19) meets }G\\
 &\quad\Longleftrightarrow\quad
 \text{the model (19) with }G\text{ is nonempty and its minimum is }\theta.
                                                               \tag{20}
 \end{split}
\]

Compactness and continuity prove the reverse implication. Test the right
side with the rational value subroutine and exact comparison of real
algebraic numbers. No row with an algebraic right-hand side is sent to
the feasibility oracle. The fixed box is retained throughout these
queries; comparing an arbitrary unboxed infimum to \(\theta\) would
need a separate attainment justification.

Bisect the integer interval for each \(z_j\). Test its lower half by
(20). Retain that half if it contains an optimizer, and the upper half
otherwise. Use the complementary integer endpoints \(a\) and \(a+1\)
at each split. Keep only the current coordinate intervals. After
\(O(k\log(B_z+1))\) queries, one optimal integer vector \(z^*\)
remains. This does not enumerate its box.

The stronger uniformity in Section 5 ensures that the canonical pair for
this chosen \(z^*\) also lies in (19). It is not enough merely to know
that the original mixed-integer model has some small optimizer if one
later chooses another integer assignment.

## 7. Approximate and recognize the continuous optimizer

Fix the recovered \(z^*\). All optimal-face queries below use (20),
the same box (19), and rational additional rows. By (18), the projection
of the boxed optimal set contains the unboxed minimum-norm point (13).
Its own minimum-norm point is therefore exactly the same \(u^*\).

Let \(\nu=\|u^*\|^2\). Query (20) with \(\|u\|^2\le t\),
and bisect \(\nu\) between \(0\) and \(rR^2\). For a requested
coordinate accuracy \(\eta=2^{-p}\), find an upper endpoint
\(t\) with

\[
                         \nu\le t\le\nu+\eta^2/16.       \tag{21}
\]

Every \(y\) in that norm sublevel of the optimal projection satisfies
the projection inequality

\[
                   \|y-u^*\|^2\le\|y\|^2-\|u^*\|^2
                                      \le\eta^2/16.       \tag{22}
\]

Starting from \([-R,R]^r\), bisect one coordinate interval at a time,
retaining a half exactly when (20), together with the norm row and all
current intervals, remains true. Each retained compact optimal slice is
nonempty. Stop when all intervals have width below \(\eta/2\).
Their rational midpoint approximates \(u^*\) within \(\eta\) in
each coordinate by (22). Restart from the original box for each new
precision request: a box containing a nearby optimal point need not contain
\(u^*\) itself. When \(r=0\), this procedure is empty.

Now approximate the particular \(v^*\) in (17). Its fiber (16) has a
constant rational matrix \(A\). Using the univariate representation of
\(\theta\) and the preceding \(u^*\) oracle, construct a rational
vector \(\widetilde b\) with
\(\|\widetilde b-b^*\|_\infty\le\delta\). Set

\[
 \widehat b=\widetilde b+\delta\mathbf1,
 \qquad b^*\le\widehat b\le b^*+2\delta\mathbf1,
 \qquad
 v_\delta=\arg\min\{\|v\|^2:Av\le\widehat b\}.          \tag{23}
\]

This is a rational convex quadratic program, solvable exactly in polynomial
time. Its minimizer is rational. Because its feasible set contains (16),
\(\|v_\delta\|\le\|v^*\|\). A rational-matrix Hoffman constant
\(H_A\le2^{N^{O(1)}}\), computable conservatively from minors, gives
a true fiber point \(w\) within \(\zeta=2H_A\delta\) of
\(v_\delta\). With a uniform bound \(V\ge\|v^*\|\), the
projection inequality at \(v^*\) yields

\[
 \|v_\delta-v^*\|
                \le\zeta+\sqrt{2V\zeta+\zeta^2}.         \tag{24}
\]

Thus \(\zeta\le\eta^2/[16(V+1)]\), for \(0<\eta\le1\),
suffices to approximate \(v^*\) within \(\eta\). The detailed
rational QP and Hoffman argument, including its exact symbolic tests, is
in [common-range witness recovery, Section 5](common-range-witness-recovery.md#5-recover-the-affine-fiber-through-rational-quadratic-programs).
The same proof applies here because only the evaluated right-hand side
changes. Degree-\(d\) evaluation on the known coordinate box needs
\(f(k,r,d)(N+\log R+\log(1/\delta)+1)^{O(1)}\) accuracy bits;
the factor involving \(d\) is a parameter factor.

The tuple \((\theta,u^*,v^*)\) has the joint degree bound from (15),
the height bounds from Section 5, and a certified approximation oracle
from (21)--(24). Apply the reviewed common-field recognition algorithm.
Its overhead is polynomial in tuple length, degree, coefficient heights,
and requested precision, with an absolute exponent. It returns one
primitive element and coordinate polynomials in the desired bit bound.
We include \(\theta\) in this tuple because it appears in the affine
fiber's right-hand side. The proof does not require a separate argument
that it already belongs to \(\mathbb Q(u^*)\).

Finally substitute the returned coordinates into every original polynomial
row and the objective. Exact univariate sign determination verifies
feasibility and \(q_0(z^*,u^*,v^*)=\theta\). This verifies the returned
point and its value against the original explicit input. The global
optimality conclusion also uses the exact value algorithm; substitution
alone does not prove it.

## 8. Why the complete algorithm remains FPT

The existence proofs give value degree \(g(r,d)\), value and integer
encoding bounds \(f(k,r,d)N^C\), and an optimizer box with that many
bits. These proofs may use exponentially many implicit rows, but the
algorithm calls only the already established feasibility oracle on the
explicit original model with additional rational rows.

For an approximation request of \(p\) bits, all retained endpoints,
thresholds, and norm bounds have at most
\(f(k,r,d)(N+p+1)^C\) bits. Only current coordinate intervals are
retained; bisection history does not become a growing constraint list.
The number of feasibility or boxed-value queries has the same form. The
value subroutine (11) has an absolute input exponent, and it calls
feasibility and algebraic recognition, not optimizer recovery. Therefore
the nesting depth of the subroutines is fixed; integer-coordinate
bisection does not recursively apply optimizer recovery \(k\) times.

Certified recognition needs precision polynomial in the degree and height
bounds, hence \(p\le f(k,r,d)N^C\). Composition of this fixed number
of polynomial-cost stages preserves (2), after increasing its absolute
constant. Bounds which were merely \(N^{g(k,r,d)}\), or unspecified
polynomial recurrences iterated a parameter-dependent number of times,
would not prove this conclusion.

## 9. Prior comparison, limits, and verification

The [feasibility prior audit](polynomial-nonlinear-dimension-prior.md)
compares Hildebrand--Koppe's fixed-dimensional polynomial integer method,
Toledo's implicit polynomial separation framework, Norton--Plotkin--Tardos,
Khachiyan--Porkolab, and the recent convex-polynomial objective work of
Slot--Steurer--Wiedmer. Each is substantial prior art. The associated
feasibility theorem, including its implicit-family adaptation, is an input
to this note, not a new algorithm developed again here.

The additional methods are established as well: coefficient-sensitive real
quantifier elimination, exact rational convex QP, Hoffman's linear error
bound, algebraic recognition, and classical finite attainment. The
candidate contribution is their combination with the reviewed convex
epigraph arithmetic theorem to obtain full exact optimization for an
arbitrarily large linear continuous extension of a small nonlinear
polynomial core. The [optimization prior audit](polynomial-nonlinear-dimension-optimization-prior.md)
also records a published mixed-integer FPT folklore statement by
Gavenciak--Knop--Koutecky, and Toledo's explicit-row arithmetic bound whose
logarithmic powers are compatible with FPT. Neither should be omitted from
a novelty comparison. The inspected sources did not supply this exact
large-linear-extension output theorem; that does not establish priority.

The model requires rational coefficients, global joint convexity of every
polynomial row and the objective, and constant coefficients on the
eliminated variables. Convexity of the feasible set alone is insufficient
for the feasibility oracle. A separately reviewed
[quasiconvex extension](quasiconvex-polynomial-nonlinear-dimension-frontier.md)
supplies the different separation algorithm required for globally
quasiconvex rows; the present convex-gradient oracle does not automatically
apply. The degree parameter
belongs to the claim. General polynomial circuits
with unbounded expansion are not included by the explicit input model.

Even feasibility need not admit a rational point: the independently reviewed
[strongly convex quartic example](convex-quartic-irrational-zero.md) has a
singleton irrational zero sublevel in two variables. Thus recovering an
algebraic point can be necessary before any objective is considered.

The theorem proves a parameterized exact bit bound and a common algebraic
output bound. It does not supply practically sized constants, improved
floating-point conditioning, a numerical implementation, or experimental
solver performance. These remain necessary to realize practical value.

As an exact higher-degree example, consider

\[
 \min_{z\in\mathbb Z,\ u,v\in\mathbb R}
                  z^2-z+\tfrac14+v-2u
       \quad\text{subject to}\quad u^4\le v.             \tag{25}
\]

Let \(a=2^{-1/3}\). Its two optimal integer assignments are \(z=0,1\),
both with \(u=a\), \(v=a/2\), and
\(\theta=1/4-3a/2\). The global certificate is the identity

\[
 q_0-\theta=z(z-1)+(v-u^4)
                +(u-a)^2\bigl((u+a)^2+2a^2\bigr).        \tag{26}
\]

Every term is nonnegative on the mixed-integer feasible set. The value's
minimal polynomial is \(64T^3-48T^2+12T+107\), while the nonlinear and
linear coordinates satisfy \(2T^3-1\) and \(16T^3-1\), respectively.
All three generate the same cubic field. This example checks the need for
algebraic output beyond quadratic inputs; it is not a complexity lower bound.

There is also an elementary exponential lower bound on field degree as
\(r\) grows. For \(r\ge1\), use \(r\) nonlinear coordinates
\(u_0,\ldots,u_{r-1}\) and one linear coordinate \(v=u_r\):

\[
 \min\ v-2^{r+1}u_0
       \quad\text{subject to}\quad
           u_i^2\le u_{i+1}\quad(0\le i<r).               \tag{27}
\]

These are globally convex quadratic rows, their common nonlinear dimension
is exactly \(r\), and the objective is affine. For fixed \(u_0=a\),
the smallest feasible \(v\) is \(a^{2^r}\); all intervening powers
are attained by equality. After the first square the coordinates are
nonnegative, so increasing an intervening coordinate cannot lower the
final one. Minimizing \(a^{2^r}-2^{r+1}a\) gives the unique positive
root

\[
 a^{2^r-1}=2,\qquad u_i=a^{2^i},\qquad
                    \theta=-2(2^r-1)a.                   \tag{28}
\]

The polynomial \(T^{2^r-1}-2\) is Eisenstein at 2. Both \(a\) and
\(\theta\) therefore have degree exactly \(2^r-1\). The input
coefficients require only \(O(r)\) bits each, and the complete input
has polynomial length in \(r\). Thus a field-degree bound independent
of \(r\), or polynomial in \(r\), is impossible even in this
continuous quadratic subclass. This uses standard repeated squaring and
Eisenstein's criterion; no novelty is claimed for the example.

The independent bounds audit read the complete draft and checked Sections
3--8 in detail: the singleton formula, individual and joint degree bounds,
all eliminated coordinates staying in one field, degree-\(d\) denominator
clearing, the uniform box over all selected optimal integer assignments,
compact optimal-face queries, and the fixed-depth complexity composition.
A fresh full adversarial review independently checked these interfaces,
the sharpened degree bound, the repeated-squaring boundary, and the primary
Bank--Mandel and quantifier-elimination statements. Its own fresh subreview
checked status, scalar recognition, and complexity composition. These reviews
treat the previously reviewed feasibility oracle and general convex value
theorem as separate inputs; they do not establish priority or constitute a
formal verification.

The targeted command
`python research-20260927/check_polynomial_nonlinear_optimization.py`
passed the quartic gap identity, 41 integer gap checks, both optimal integer
assignments, the exact Farkas projection, and three irreducible cubic
encodings in one field. It also checked eight instances of (27), including
the stationary equation, value identity, common nonlinear dimension, and
Eisenstein coefficient conditions. These checks verify the examples; they
do not implement the algorithm or verify the general arithmetic and
complexity bounds.

A targeted inline `python -` check passed for this manuscript, its three
review and prior-audit notes, and the exact example checker: local Markdown
links, paired math delimiters, whitespace, control characters, and final
newlines. These are document checks, not mathematical verification.
No project-wide verification, CI inspection, or Lean formalization is
claimed.
