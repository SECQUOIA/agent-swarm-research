# Attainment for rational convex quadratic mixed-integer programs

Date: 2026-09-27. Independent adversarial investigation of the unbounded
mixed-integer extension. Both attainment and closedness of rational linear
images are already consequences of Bank–Mandel (1987). The self-contained
quadratic proof below is retained for its explicit elimination argument.
See the [prior audit](mixed-integer-attainment-prior.md).

## Statement

Write \(w=(z,x)\in\mathbb Z^k\times\mathbb R^{n-k}\), and let

\[
q_i(w)=\tfrac12w^TQ_iw+a_i^Tw+b_i,\qquad i=0,\ldots,m,
\]

have rational coefficients and \(Q_i\succeq0\). Affine inequalities and
equalities can be included as rows with zero Hessian. If

\[
F=\{w\in\mathbb Z^k\times\mathbb R^{n-k}:q_i(w)\le0,
\ i=1,\ldots,m\}
\]

is nonempty and \(\inf_Fq_0> -\infty\), then \(q_0\) attains its infimum on
\(F\). No box, Slater condition, rational feasible point, or fixed dimension
is required for this qualitative statement.

## Recession and dimension reduction

For a nonempty continuous feasible set

\[
C=\{w:q_i(w)\le0, i=1,\ldots,m\},
\]

its recession cone is

\[
\operatorname{rec}C
=\{d:Q_id=0, a_i^Td\le0, i=1,\ldots,m\}.       \tag{1}
\]

Indeed, substituting \(w+td\) and letting \(t\to\infty\) first forces
\(d^TQ_id=0\), hence \(Q_id=0\) by positive semidefiniteness, and then
\(a_i^Td\le0\). The converse follows directly by substitution. Thus this
cone is rational polyhedral, even when the feasible set has an irrational
affine hull.

Suppose \(d\ne0\) is rational, \(d\in\operatorname{rec}C\), and

\[
Q_0d=0,\qquad a_0^Td=0.                         \tag{2}
\]

There is a rational invertible change of variables preserving the mixed
lattice that turns \(d\) into one coordinate direction.

- If \(d_z=0\), extend \(d_x\) to a rational basis of the continuous space.
  The coordinate \(t\) in direction \(d\) is continuous.
- If \(d_z\ne0\), rescale \(d\) so its integer part is a primitive integer
  vector \(p\). Extend \(p\) to a unimodular matrix \(U\). Set
  \(z=U(t,\widehat z)\) and \(x=\widehat x+d_xt\). Here \(t\in\mathbb Z\),
  \(\widehat z\in\mathbb Z^{k-1}\), and \(\widehat x\) is unrestricted
  continuous. This map is a bijection of the mixed lattice.

In either case, write the remaining coordinates as \(y\). Since every
\(Q_id=0\), every transformed row has the form

\[
q_i(y,t)=r_i(y)+\alpha_it,\qquad \alpha_i\le0,
\]

with rational convex quadratic \(r_i\). The objective is independent of
\(t\), by (2). Projection of the feasible mixed-integer set onto \(y\) is
exactly

\[
\{y:r_i(y)\le0\text{ for all }i\text{ with }\alpha_i=0\}.       \tag{3}
\]

For the reverse inclusion, choose \(t\) at least
\(\max_{\alpha_i<0}r_i(y)/(-\alpha_i)\), rounding upward if \(t\) is
integer. There are only finitely many rows, so this is a finite choice.
Rows with negative slope impose no condition on the projection. Consequently
dimension reduction preserves the entire set of achieved objective values.

## Attainment proof

Induct on \(n\). The zero-dimensional assertion is immediate. Choose a
minimizing sequence \(w_j\in F\), with objective values bounded above by
some real \(c\). A bounded subsequence converges, after passage to a further
subsequence, to a point of \(F\): the mixed lattice and each weak inequality
are closed. Continuity then gives an optimum.

Otherwise pass to an unbounded subsequence with

\[
\|w_j\|\longrightarrow\infty,
\qquad w_j/\|w_j\|\longrightarrow d,\quad\|d\|=1.
\]

Dividing the inequalities by \(\|w_j\|^2\) gives \(d^TQ_id=0\) for every
row and the objective. Dividing by \(\|w_j\|\), and using the nonnegative
quadratic terms before taking the limit, gives \(a_i^Td\le0\). Therefore
the following rational polyhedral cone contains a nonzero vector:

\[
K=\{d:Q_id=0, a_i^Td\le0, i=0,\ldots,m\}.       \tag{4}
\]

If \(K\) contained a vector with \(a_0^Td<0\), it would contain a rational
such vector, because the defining inequalities are rational. Scale it so
its integer coordinates are integers. From any point \(w\in F\), the
points \(w+\ell d\), \(\ell\in\mathbb Z_+\), are feasible and have
objective tending to \(-\infty\). This contradicts the finite infimum.
Hence \(a_0^Td=0\) for every \(d\in K\).

Since a nonzero rational polyhedral cone contains a nonzero rational
vector, choose such a vector in \(K\), and apply (3). The reduced problem
has dimension \(n-1\), rational PSD data, and the same nonempty set of
objective values. Its finite infimum is attained by induction. The finite
lift described after (3) attains the same value in the original problem.

This completes the proof.

## Closed rational linear images

The same argument proves that \(A(F)\) is closed for every rational matrix
\(A\). Let \(Aw_j\to b\). If a subsequence of \(w_j\) is bounded, its limit
lies in \(F\) and maps to \(b\). Otherwise a normalized unbounded subsequence
gives a nonzero vector in the rational polyhedral cone

\[
\{d:Q_id=0, a_i^Td\le0, i=1,\ldots,m, Ad=0\}.
\]

Choose a nonzero rational vector in this cone, and apply the same exact
projection (3). The map \(A\) is independent of the deleted coordinate, so
the desired conclusion follows by induction on dimension. The reduced map
remains rational. This establishes closedness of rational linear images of
this particular mixed-integer class, not of arbitrary mixed-integer convex
sets. This corollary is already implied by the older result discussed below.

## Coordinate choices for an effective extension

The parent investigator observed a useful refinement of the elimination
step, which was checked independently here. If \(d_z=0\), choose a
continuous coordinate \(x_j\) with \(d_j\ne0\). Every line parallel to \(d\)
has a representative on \(x_j=0\). Since retained rows and the objective
are invariant along \(d\), their reduced expressions are their literal
restrictions to \(x_j=0\). This just deletes coefficients; there is no
coefficient growth in these purely continuous eliminations. The rational
change of coordinates is needed only for the proof and later lift.

Integer-direction eliminations require a unimodular coordinate change but
occur at most \(k\) times. Standard rational polyhedral and lattice bounds
provide polynomial-size directions and unimodular completions at each
such step. For fixed \(k\), a composition of these polynomial bounds stays
polynomial in the original input size. The span dimension of the
continuous Hessian blocks cannot increase: pure continuous deletion takes
principal submatrices, and the integer-coordinate step leaves the
continuous Hessian blocks unchanged before any row deletion.

This controls the transformed problem's encoding. A bound for the
eventual optimizer and for the back-substitution still needs a separate
argument; it does not follow solely from attainment.

## Boundaries of the statement

Rationality cannot simply be discarded. Minimize

\[
(z_1-\sqrt2z_2)^2
\quad\text{over }(z_1,z_2)\in\mathbb Z^2,\ z_2\ge1.
\]

Continued-fraction approximants to \(\sqrt2\) give infimum zero, while
irrationality prevents attainment. The objective is globally convex
quadratic but its coefficients are irrational.

Convexity of the feasible set does not replace global PSD Hessians of its
native quadratic rows. The rational problem

\[
\inf x\quad\text{subject to }z\in\mathbb Z,\ z\ge1,
\quad x\ge0,\quad zx\ge1
\]

has value zero and no optimizer. Its continuous feasible set is convex and
has a rational second-order-cone representation, but the polynomial row
\(1-zx\le0\) has indefinite Hessian. The failure already occurs with one
integer and one continuous variable.

The induction does not establish a polynomial encoding bound for an
optimal integer assignment. It is qualitative: repeated coordinate changes,
the reduced optimizer, and the final lift need separate effective bounds.
It also does not produce rational continuous coordinates; some rational
PSD systems have only irrational feasible points. The separate
[complexity note](mixed-integer-attainment-frontier.md) develops effective
optimal-witness bounds beyond this qualitative argument.

## Literature examined

1. Bank and Mandel, “Nonlinear parametric integer programming,” in
   *Parametric Optimization and Related Topics* (1987), 16–48,
   [primary-source preview](https://api.pageplace.de/preview/DT0400.9783112720936_A50662169/preview-9783112720936_A50662169.pdf).
   Theorem 7(ii), printed page 34, proves closedness of the mixed-integer
   right-hand-side feasibility domain under a recession-generator condition
   for the stable subsystem. Theorem 3(iii), printed page 24, makes this
   condition automatic for rational quasiconvex polynomial data, including
   that subsystem. Appending the objective as a row gives finite attainment.
   Appending opposite affine rows encoding a rational linear map gives
   closedness of its image. Thus both qualitative conclusions above are
   covered, in a broader polynomial class. The relevant statements were
   inspected directly; the [prior audit](mixed-integer-attainment-prior.md)
   records the definitions and application.
2. Bertsekas and Tseng, *Set intersection theorems and existence of optimal
   solutions*, Mathematical Programming 110 (2007), 287–314,
   [author-hosted full text](https://www.mit.edu/~dimitrib/Set_Intersections.pdf).
   The discussion before Proposition 11, on printed page 309, cites
   Bank and Mandel, *Parametric Integer Optimization* (1988), Theorem 7.4,
   for quasiconvex polynomial problems with finitely generated common
   recession directions and some integer variables. This citation led to
   the older primary source above. The exact book theorem has not been
   inspected; it is no longer needed to establish the prior scope.
3. Bank and Mandel, *Parametric Integer Optimization*, Akademie-Verlag
   (1988), [publisher record](https://doi.org/10.1515/9783112472668).
   The openly accessible contents locate Section 7.3, “Some Special
   Mixed-Integer Optimization Problems,” at page 111. The available preview
   does not include that section.
4. Bank and Mandel, “(Mixed-) integer solutions of quasiconvex polynomial
   inequalities,” in *Advances in Mathematical Optimization*, Mathematical
   Research 45 (1988), 20–34. The
   [publisher preview](https://api.pageplace.de/preview/DT0400.9783112479926_A46396805/preview-9783112479926_A46396805.pdf)
   includes the article's introduction and identifies existence and stability
   of mixed-integer solutions as its subject, but does not expose all
   relevant theorems.
5. Bank, Heintz, Krick, Mandel, and Solernó, “Une borne optimale pour la
   programmation entière quasi-convexe,” BSMF 121 (1993), 299–314,
   [open full text](https://www.numdam.org/item/BSMF_1993__121_2_299_0.pdf).
   Its abstract gives a singly exponential binary-size bound for feasible
   integer points of rational quasiconvex polynomial systems, and a related
   optimization bound. It concerns pure integer variables; applying it to
   arbitrary-dimensional continuous projections requires further work.
6. The continuous convex-polynomial attainment theorem is already classical:
   Belousov and Klatte, “A Frank–Wolfe type theorem for convex polynomial
   programs,” Computational Optimization and Applications 22 (2002), 37–48,
   as discussed by Bertsekas and Tseng. No continuous attainment novelty is
   suggested here.

Searches used the terms “mixed-integer attainment convex,” “Frank–Wolfe
mixed integer quadratic constraints,” “convex polynomial bounded below,”
and the exact Bank–Mandel titles. The 1987 primary source resolves the
initial uncertainty about whether these qualitative conclusions were old.

## Verification record

The proof was developed independently in response to a counterexample
request. The parent investigator independently checked the rational
mixed-lattice change of variables and projection step before this note was
written. No numerical experiment or formal proof checker is used: the
argument consists of exact quadratic identities, rational polyhedral facts,
unimodular completion, and induction. The older theorem comparison was
checked against the 1987 primary source and independently audited.
A targeted Python check of this file's trailing whitespace,
control characters, and final newline passed. No project-wide checks or CI
inspection were performed.
