# Algebraic optimization bounds from the common Hessian range

Date: 2026-09-28. Status: the quadratic programming charts, low-dimensional
quantifier-elimination consequence, and canonical projected-coordinate
addendum passed independent review. No algorithm or novelty claim is made
here.

The Hessian of a convex quadratic objective need not be included in the
common range parameter when bounding the algebraic size of finite optimal
values and attained optimizers. Directions that occur only linearly in the
constraints can be eliminated through quadratic programming charts. Each
chart leaves a quartic objective in the nonlinear coordinates. The number of
charts can be exponential, but each has small coefficients; the proof uses
one chart and does not enumerate them.

## 1. Statement and scope

Let

\[
 S=\{x\in\mathbb R^n:q_i(x)\le0\ (1\le i\le m)\}
\]

be a rational quadratic system, including any affine rows. Equalities can be
represented by both signs. Convexity of the constraint polynomials is not
needed for this note. Set

\[
 K=\bigcap_i\ker\nabla^2q_i,\qquad r=n-\dim K.
\]

Let \(f\) be a rational quadratic objective whose Hessian is positive
semidefinite on \(K\). In particular, every convex quadratic objective is
allowed, regardless of its rank. Its Hessian is excluded from \(r\).
Let \(N\ge2\) be the total explicit rational input length.

**Proposition.** There are an effectively computable function \(F\) and an
absolute constant \(C\) with the following properties.

1. If \(S\ne\varnothing\) and \(\theta=\inf_S f\) is finite, then
   \(\theta\) has an integer annihilator of degree at most \(F(r)\)
   and coefficient bit length at most \(F(r)N^C\).
2. If the infimum is attained, some global optimizer has a common algebraic
   field of degree at most \(F(r)\) and a rational univariate
   representation of total length at most \(F(r)N^C\).
3. Consequently a rational box of radius with bit length at most
   \(F(r)N^C\) contains some optimizer whenever the infimum is attained.

These are encoding bounds. They do not by themselves give a fixed-parameter
algorithm, a tractability result for nonconvex systems, or a certificate of
global optimality. In particular, generating every chart is not a proposed
algorithm. The proposition bounds some optimizer; it does not identify the
minimum-norm point of a general objective sublevel set.

The case \(r=0\) is ordinary quadratic optimization over a rational
polyhedron. Its finite minimum is attained, and the chart argument below
gives a rational optimizer of polynomial bit length directly.

## 2. Constant-matrix quadratic programming charts

A rational basis of \(K\) and a rational complement give an invertible
coordinate change \(x=T_1u+T_0v\), with \(u\in\mathbb R^r\).
Rational minor bounds keep the transformed coefficients polynomial in
\(N\). The constraints and objective become

\[
 Cv+p(u)\le0,\qquad
 f(u,v)=\tfrac12v^THv+(Bu+b)^Tv+a(u),                 \tag{1}
\]

where \(C,H,B,b\) are rational, \(H\succeq0\), and every entry of
\(p\) and \(a\) has degree at most two.

For each row subset \(I\) whose rows in \(C_I\) are linearly
independent, including the empty subset, form

\[
 M_I=\begin{pmatrix}H&C_I^T\\ C_I&0\end{pmatrix},\qquad
 \binom{v_I(u)}{\lambda_I(u)}
 =M_I^+\binom{-Bu-b}{-p_I(u)}.                       \tag{2}
\]

Here \(M_I^+\) is the Moore--Penrose inverse of this constant rational
matrix. It is rational with polynomial coefficient bit lengths. Explicitly,
choose a rational basis matrix \(Z\) of \(\ker M_I\), and put
\(A=M_I+ZZ^T\). This matrix is invertible and
\(M_I^+=A^{-1}M_IA^{-1}\), by restricting to the kernel and its
orthogonal complement. Rational basis and minor bounds control its bits.
Consequently \(v_I\) is a rational polynomial map of degree at most two
and polynomial coefficient bit length. This definition is made even at
values of \(u\) where the displayed linear system is inconsistent.

**Chart lemma.** Fix \(u\) such that its feasible fiber is nonempty and
the objective is bounded below on that fiber. The minimum-norm optimizer
\(v^*\) of the fiber equals \(v_I(u)\) for some \(I\).

To prove this, a convex quadratic bounded below on a nonempty polyhedron
attains its minimum by the classical Frank--Wolfe theorem; see the
introduction of [Martinez-Legaz, Noll and Sosa](https://www.math.univ-toulouse.fr/~noll/PAPERS/frank_and_wolfe.pdf).
The optimal set is closed and nonempty, so it has a
minimum-norm point. Choose \(I\) to be a basis of **all** constraint
row normals active at \(v^*\). For any \(d\in\ker C_I\), both
\(v^*+td\) and \(v^*-td\) are feasible for all sufficiently small
positive \(t\). Indeed, all active equations stay fixed, and the finitely
many inactive inequalities have strict slack. First-order optimality gives

\[
 Hv^*+Bu+b\in\operatorname{range}C_I^T.
\]

Thus some, possibly signed, \(\lambda\) makes \((v^*,\lambda)\)
a solution of the linear system in (2). No sign condition on these basis
multipliers is required.

Its kernel is exactly

\[
 \ker M_I=(\ker H\cap\ker C_I)\times\{0\}.          \tag{3}
\]

In fact, if \(Hd+C_I^T\mu=0\) and \(C_Id=0\), multiplication by
\(d^T\) gives \(d^THd=0\). Positive semidefiniteness gives \(Hd=0\);
independence of the rows of \(C_I\) then gives \(\mu=0\).

For every \(d\in\ker H\cap\ker C_I\), the small feasible motions
just described preserve the objective exactly. Minimum norm therefore gives
\(v^*\perp d\). By (3), \((v^*,\lambda)\) is orthogonal to
the kernel of the symmetric matrix \(M_I\). It is the unique least-norm
solution, which is exactly its Moore--Penrose solution. This proves the
lemma, including singular \(H\) and singular \(M_I\).

Using only a positive-multiplier support would be insufficient. For example,
minimizing \(v_1^2\) subject to \(v_2\ge1\) has minimum-norm optimizer
\((0,1)\), although its only active inequality has multiplier zero.
The full active-row basis is what supplies the needed constraint.

## 3. Reduce values and attained optima to one small-dimensional chart

Define the closed sets and polynomial objectives

\[
 D_I=\{u:Cv_I(u)+p(u)\le0\},\qquad
 g_I(u)=f(u,v_I(u)).                                  \tag{4}
\]

Every defining row of \(D_I\) has degree at most two, and \(g_I\)
has degree at most four. Each coefficient has polynomial bit length, and
each chart has only the original number of rows. There are at most \(2^m\)
charts. No consistency or multiplier sign guard is necessary in (4): every
point retained by (4) is an original feasible point, whether or not its
pseudoinverse happened to solve the full stationarity system.

Suppose the global infimum is finite. Every nonempty fiber is then bounded
below. The chart lemma represents one optimizer in every such fiber, while
every point of every chart is feasible. Consequently

\[
 \inf_S f=\min_{I:D_I\ne\varnothing}\inf_{u\in D_I}g_I(u).       \tag{5}
\]

This equality need not hold for a problem with an unbounded-below fiber:
for \(v\ge0\) and objective \(-v\), the displayed pseudoinverse
charts only produce \(v=0\). This is why (5) is used under the finite
infimum assumption, not as an unboundedness test.

If the original minimum is attained, take any original optimizer, keep its
\(u\), and replace its \(v\) by the minimum-norm optimizer of that
fiber. One chart therefore attains the same global value. It remains to
control optimization of a quartic in \(r\) variables on its quadratic
basic closed set. The next section supplies the required bound with the
dependence on the number of inequalities stated explicitly.

## 4. A direct classical quantifier-elimination bound

We use the coefficient-sensitive quantifier-elimination theorem of Basu,
Pollack and Roy. The primary paper, [*On the combinatorial and algebraic
complexity of quantifier elimination*](https://doi.org/10.1145/235809.235813),
Theorem 1.3.1 and the preceding
“well-behaved” bit-complexity definition, separates the degree and coefficient
bounds from the number of input polynomials. The explicit statement also
appears as Theorem 2.27 in
[Basu's author survey](https://www.math.purdue.edu/~sbasu/raag_survey2011_final-sep4-2014.pdf).
Both local source texts were inspected.

The inspected copies are the
[1996 paper text](../papers/pooling/revision-20260909/checks/whole-review4/basu1996-on-the-combinatorial-and-algebraic.txt),
Section 1.3, pages 1004--1005, and the
[2014 survey text](../research-20260925/publication-sources/basu-2014-author-survey.txt),
Section 2.5.2, page 16.

For bounded polynomial degree, one scalar free variable, and quantifier
blocks whose dimensions depend only on \(d\), each polynomial in the
resulting quantifier-free formula has degree at most \(F(d)\) and coefficient
bit length at most \(F(d)\tau\). Crucially, **these two bounds do not depend
on the number of predicates or the formula length**. The number of output
polynomials and the cost of constructing the formula do depend on those
quantities. We use only the per-polynomial bounds, not the algorithm's
running time.

Each input polynomial is cleared of denominators separately. With bounded
degree and \(O(d)\) variables, this multiplies \(\tau\) by a function of
\(d\); it does not collect denominators from all rows.

### 4.1 Finite values, including unattained infima

Let \(D\subseteq\mathbb R^d\) be a nonempty basic closed set defined by
polynomials of degree at most four, and let \(g\) be quartic. The formula

\[
 E(t)\quad\Longleftrightarrow\quad
       \exists u\,[u\in D\ \wedge\ g(u)\le t]               \tag{6}
\]

has one quantified block of dimension \(d\) and one scalar free variable.
If \(\gamma=\inf_Dg\) is finite, its realization is either
\([\gamma,\infty)\) or \((\gamma,\infty)\).

After quantifier elimination, at least one nonzero output polynomial must
vanish at \(\gamma\). Otherwise all its nonzero predicates have locally
constant signs, so the whole Boolean formula is constant in a neighborhood
of \(\gamma\), contradicting that \(\gamma\) is an endpoint.
Identically zero output polynomials may simply be discarded. The theorem's
per-polynomial bounds give an integer annihilator of degree \(F(d)\) and
coefficient bits \(F(d)\tau\), with no attainment assumption.

### 4.2 Some small algebraic optimizer

Suppose the infimum is attained. Its optimizer set is nonempty and closed,
so it has a nonempty compact set of minimum-norm points. Select the
lexicographically least point of that compact set, denoted \(u^*\).
Sequential coordinate minimization on compact sets proves that this point
exists and is unique; convexity is unnecessary.

The selected point is described by the following polynomial formula:

\[
\begin{split}
 u\in D,\qquad
 &\forall v\,[v\in D\Rightarrow g(u)\le g(v)],\\
 &\forall w\,[(w\in D\ \wedge\ g(w)=g(u))
                       \Rightarrow\|u\|^2\le\|w\|^2],\\
 &\forall y\,[(y\in D\ \wedge\ g(y)=g(u)
               \ \wedge\ \|y\|^2=\|u\|^2)
                       \Rightarrow u\le_{\mathrm{lex}}y].
                                                               \tag{7}
\end{split}
\]

The lexicographic relation is a Boolean combination of linear equalities
and inequalities. For coordinate \(j\), append \(t=u_j\), quantify
\(u\) existentially, and combine the three universal blocks. The resulting
formula has one scalar free variable, blocks of dimensions \(d\) and
\(3d\), and bounded polynomial degree. It defines the singleton
\(\{u_j^*\}\). Some nonzero output polynomial therefore vanishes at that
coordinate, by the same local-sign argument as above.

Each coordinate degree is bounded by \(F(d)\), and its coefficient bits
by \(F(d)\tau\). The common field degree is at most the product of these
\(d\) degree bounds, which is still a function of \(d\). A bounded
integer linear combination of the coordinates separates its finitely many
embeddings. Trace linear algebra then expresses every coordinate in the
resulting power basis, with total rational-univariate-representation length
at most \(F(d)(\tau+1)\), after increasing \(F\). There are only \(d\)
coordinates in this product, not the original ambient number of variables.

The earlier [ordered-perturbation proof](common-range-lowdim-perturbation.md)
is retained as an alternate check. It is unnecessary for this consequence
of established quantifier elimination.

## 5. Finish the original encoding bound

Apply Section 4 to a chart attaining the minimum in (5), or to one whose
infimum equals it. Its dimension is \(r\), degrees are at most four,
row count is at most the original count, and coefficient bits are \(N^C\)
for an absolute \(C\). The endpoint argument gives the claimed value bound.

In the attained case, choose the chart optimizer supplied by Section 4.2.
Every component of \(v_I(u)\), and hence every original coordinate
\(x=T_1u+T_0v_I(u)\), belongs to the common field \(\mathbb Q(u)\).
There is no multiplication of degree bounds across the original \(n\)
coordinates. Evaluating degree-two rational maps with polynomial coefficient
bit lengths in this field keeps total representation length within
\(F(r)N^C\). Cauchy's root bound for coordinate annihilators then supplies
the optimizer box in the proposition.

## 6. Canonical projected coordinates and the objective gradient

Suppose now that the original feasible set is convex, the objective is
convex, and its finite optimum is attained. This covers both native convex
quadratic systems and convex sets described by squared SOC rows with the
right-hand-side sign conditions retained.

Let \(U^*\) be the projection of the original optimal set onto the nonlinear
coordinates \(u\). The chart lemma gives the exact identity

\[
 U^*=\bigcup_I\{u\in D_I:g_I(u)=\theta\}.              \tag{8}
\]

It is therefore closed, because this is a finite union of closed sets.
It is convex because it is a linear projection of the original convex
optimal set. Thus \(U^*\) has a unique point \(\bar u\) of minimum norm.
This conclusion uses (8); closedness of a general convex projection alone
would be false.

Set \(H(u,t)=\bigvee_I[u\in D_I\ \wedge\ g_I(u)=t]\). The pair
\((\bar u,\theta)\) is uniquely described by

\[
\begin{split}
 H(u,t)\quad\wedge\quad
 &\forall v\bigwedge_I[v\in D_I\Rightarrow t\le g_I(v)]\\
 {}\wedge\quad
 &\forall w\bigwedge_I[(w\in D_I\ \wedge\ g_I(w)=t)
                                      \Rightarrow\|u\|^2\le\|w\|^2].
                                                               \tag{9}
\end{split}
\]

For each coordinate, add its scalar output equation and existentially
quantify \((u,t)\). This has
blocks of dimensions \(r+1\) and \(2r\), with degree at most four.
Although the number of chart predicates can be exponential, their coefficient
bits are polynomial in \(N\). The same classical theorem therefore gives
coordinate and common-field bounds \(F(r)N^C\) for \((\bar u,\theta)\).

If \(f(x)=\tfrac12x^TQx+a^Tx+c\), its gradient \(Qx+a\) is constant
on the original optimal set. Indeed, for any two optimizers \(x,y\), their
segment is optimal, hence \((x-y)^TQ(x-y)=0\). Since \(Q\succeq0\),
this gives \(Q(x-y)=0\). The gradient of any algebraic chart optimizer
from Section 5 therefore equals this common gradient \(g^*\).

That optimizer places every coordinate of \(g^*\), and \(\theta\), in
one field of degree \(F(r)\) and coefficient bits \(F(r)N^C\). Taking
the compositum with the field of \(\bar u\) multiplies two bounds depending
only on \(r\), and thus still gives degree \(F(r)\) and total encoding
\(F(r)N^C\) for \((\bar u,g^*,\theta)\). This is an existence bound;
constructing the canonical coordinates or the gradient from threshold
queries requires a separate recovery argument.

## 7. Literature and significance

The reduction uses classical parametric quadratic programming: solving a
constant linear KKT system makes optimizers affine in its right-hand side.
Here the right-hand side is quadratic in the retained nonlinear coordinates,
and the full active face handles singular systems and zero multipliers.
Neither this observation nor finite-dimensional algebraic elimination is
presented as a new general technique.

A direct prior treatment is Spjøtvold, Tøndel and Johansen,
[*Unique Polyhedral Representations of Continuous Selections for Convex
Multiparametric Quadratic Programs*](https://skoge.folk.ntnu.no/prost/proceedings/acc05/PDFs/Papers/0149_WeB08_6.pdf),
ACC 2005. Their model has affine parameters in the linear objective term
and constraint right-hand sides. Theorem 1 gives finitely many affine
optimizer pieces; Section IV explicitly permits singular positive
semidefinite Hessians, including zero, and Lemma 3 selects minimum-norm
optimizers by a secondary quadratic program. Substituting a parameter vector
consisting of \(u\) and its quadratic monomials yields precisely the
degree-two optimizer and degree-four value mechanism used here.

Their presentation assumes a full-dimensional parameter domain, and
Section IV, Remark 1 sets aside lower-dimensional regions. Our direct basis
proof retains every feasible parameter, including such regions, and records
rational bit bounds. Those details support the later encoding argument;
they do not make piecewise-affine parametric quadratic optimization a new
mechanism. The model, Theorem 1, Section IV, and Lemma 3 were inspected
directly in the primary paper.

[Jeronimo, Perrucci and Tsigaridas](https://arxiv.org/abs/1112.0544),
Theorem 1, already give degree and separation bounds for polynomial minima
on compact connected components. Their degree bound is independent of the
number of inequalities, and their coefficient-sensitive expression uses
\(\max(H,2n+2m)\), so the number of inequalities enters logarithmically
after taking logarithms. Their Theorems 14 and 15 extend selected conclusions
to attained minima on noncompact sets. The local source text was inspected.
Classical coefficient-sensitive quantifier elimination already supplies the
finite-infimum and simultaneous-coordinate bounds used here, including
possibly unattained values. The alternate perturbation proof does not
establish a new low-dimensional algebraic bound.

The [common-range feasibility note](common-range-fpt-frontier.md) establishes
why this representation can be useful algorithmically: the many linear
directions can be handled by linear or mixed-integer linear optimization,
while the nonlinear coordinate dimension controls exact precision. The
present proposition removes one apparent obstacle to exact optimization:
an arbitrary-rank convex quadratic objective does not itself force large
algebraic output on this class. A full algorithm still needs exact threshold
decisions with an absolute input-size exponent, a treatment of unboundedness
and attainment, and a recovery procedure. Those conclusions are not proved
by chart enumeration or by the encoding bounds alone.

The charts also explain a limitation of a different proposed route. A
minimum-norm point of an objective sublevel set can have large algebraic
degree even when the original constraints are affine. Such a point need not
be an optimizer of the original objective. The proposition bounds original
optimizers and does not justify controlling arbitrary sublevel projection
points by \(r\).

## 8. Verification record

The [independent chart review](common-range-optimizer-chart-review.md)
checks the singular linear algebra, full active-face selection, coefficient
bounds, and boundary examples. A separately staffed reviewer checked the
linear-algebra argument again. Five exact SymPy examples and the rational
Moore--Penrose identity passed in that review; these finite checks do not
prove the general statement.

The [independent algebraic-bound review](common-range-lowdim-review.md)
checks the exact quantifier-elimination statement, denominator clearing,
finite endpoints, selection of one optimizer for all coordinate formulas,
common-field conversion, and Section 6. It confirms that classical
quantifier elimination supplies these supporting bounds; it does not review
an optimization algorithm.

The author ran a targeted inline Python document check on this note and
the alternate perturbation note. Both passed final-newline, trailing-space,
control-character, and paired math-delimiter checks; all eight local links
resolved in the final check. A scoped `git diff --check` for those two
paths produced no errors. The files were new and untracked, so the direct
Python checks provide the actual whitespace check of their full contents.
No project-wide checks, CI inspection, or Lean formalization were run.
