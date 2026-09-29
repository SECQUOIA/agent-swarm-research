# Field degrees of zeros of rational SOS quartics

Date: 2026-09-28. Status: the degree bounds, weighted intersection
argument, residual-scheme argument, and example below have received
independent proof checks, including a
[fresh review of Sections 1–5](quartic-zero-degree-fresh-review.md).
The sharp bound in five variables is now established in a
[separately reviewed continuation](five-variable-positive-base-bound.md).
Sharp bounds from six variables onward and the extension beyond
rational SOS remain open in this investigation. No novelty claim is made.

## Results and exact assumptions

Let

\[
 F(x)=\sum_{j=1}^m q_j(x)^2,\qquad q_j\in\mathbb Q[x_1,\ldots,x_n],
 \qquad \deg q_j\leq2.
 \tag{1}
\]

Suppose that the real zero set of $F$ is the singleton $\{p\}$ and that
$\nabla^2F(p)$ is positive definite. Then $p$ is algebraic and

\[
 [\mathbb Q(p):\mathbb Q]\leq 2^n-1.
 \tag{2}
\]

If, in addition, $F$ is globally convex and $n\geq3$, then

\[
 [\mathbb Q(p):\mathbb Q]\leq2^n-3.
 \tag{3}
\]

In particular, the bound in three variables is five.

For $n\geq4$, the bound improves further to

\[
 [\mathbb Q(p):\mathbb Q]\leq2^n-5.
 \tag{3a}
\]

Thus the bounds in two, three, and four variables are respectively
three, five, and eleven. The separately developed
[cyclic family](cyclic-quartic-exponential-degree.md) attains these
degrees; its construction and verification are documented there.
In five variables the sharp bound is now twenty-one, by the
[finite residual obstruction](degree23-residual-obstruction.md)
and [positive-base argument](five-variable-positive-base-bound.md).
Their [combined root review](five-variable-degree-root-review.md)
checks the complete argument and its primary dependencies.

Global strong convexity implies the hypotheses of both statements. The
second statement only needs global convexity and a positive definite
Hessian at the zero. In the first statement the rational coefficients of
the **individual squares** are essential to the proof. A rational
polynomial that is SOS over the reals need not be SOS over the rationals.

The second statement uses classical Cayley–Bacharach, together with a
convexity argument that removes directions in which the quartic leading
part vanishes. Merely assuming positive curvature at the zero does not
give (3): Section 6 gives an exact degree-seven counterexample in three
variables.

## 1. The general rational SOS bound

Every $q_j(p)$ is zero. If $J(p)$ is the matrix with rows
$\nabla q_j(p)^{\mathsf T}$, then

\[
 \nabla^2F(p)=2J(p)^{\mathsf T}J(p).
\]

Consequently $J(p)$ has rank $n$. Choose $n$ rows with nonsingular
Jacobian. Their rational quadratic equations have an isolated simple
complex zero at $p$. An isolated point of a variety over $\mathbb Q$ has
algebraic coordinates, so $K=\mathbb Q(p)$ is a number field.

The $[K:\mathbb Q]$ conjugate points are distinct simple zeros of the
same selected equations: the nonzero Jacobian determinant remains
nonzero under every embedding. The isolated-point form of Bézout bounds
their number by the product of the degrees, at most $2^n$. This does
**not** require the selected equations to have no other components.
One can also obtain the bound by a generic small perturbation: each of
the finitely many simple points persists, and a generic system of the
same degrees has at most the product of the degrees many complex zeros.

Every real embedding of $K$ sends $p$ to a real common zero of the
$q_j$, hence to $p$ itself. Since the coordinates generate $K$, such an
embedding is the identity. Thus $K$ has exactly one real embedding and
its degree is odd. Since $2^n$ is even for $n\geq1$, (2) follows.

The argument bounds the degree of the **joint coordinate field**. It
does not multiply separate bounds for the individual coordinates.

## 2. Removing quartic-flat directions

This section applies to any rational globally convex polynomial of
degree at most four, independently of the SOS assumption. Write its
homogeneous parts as

\[
 F=F_4+F_3+F_2+F_1+F_0.
\]

The leading form $F_4$ is convex: it is the pointwise limit of the
convex functions $R^{-4}F(Rx)$ as $R\to\infty$. It is nonnegative and
even. Define

\[
 K_4=\{d\in\mathbb R^n:F_4(d)=0\}.
\]

If $d\in K_4$, then $F_4(x+td)=F_4(x)$ for all real $x,t$. Indeed,
for $0<\varepsilon<1$, convexity and homogeneity give

\[
 F_4(x+td)
 \leq (1-\varepsilon)
       F_4\left(\frac{x}{1-\varepsilon}\right)
       +\varepsilon F_4\left(\frac{td}{\varepsilon}\right)
 =(1-\varepsilon)^{-3}F_4(x).
\]

Let $\varepsilon\downarrow0$, then apply the same inequality in the
opposite direction. Therefore

\[
 K_4=\{d:D_dF_4\equiv0\}.
 \tag{4}
\]

The right side is the kernel of a rational matrix obtained by equating
polynomial coefficients. In particular, $K_4$ is a rational linear
subspace.

The cubic part is invariant in these directions as well. For fixed $d$
in $K_4$,

\[
 \nabla^2F(x+td)=\nabla^2F(x)+t\nabla^2(D_dF_3).
\]

The left side is positive semidefinite for every real $t$. Testing any
real vector against this matrix pencil shows that the coefficient of
$t$ is zero. Since $D_dF_3$ is homogeneous of degree two, its zero
Hessian means $D_dF_3=0$.

Choose rational coordinates $(y,t)$ that split off all of $K_4$.
Then

\[
 F(y,t)=G(y)+t^{\mathsf T}At+t^{\mathsf T}(By+c),
 \tag{5}
\]

where $A,B,c$ are rational. If $\nabla^2F(p)\succ0$, then $A\succ0$.
The fiber minimizer is the rational affine function

\[
 t_*(y)=-\tfrac12 A^{-1}(By+c).
\]

Substitution gives the rational convex polynomial

\[
 \widehat F(y)=F(y,t_*(y))
 =G(y)-\tfrac14(By+c)^{\mathsf T}A^{-1}(By+c).
 \tag{6}
\]

Its unique zero is the projection $\widehat p$ of $p$ and
$\mathbb Q(\widehat p)=\mathbb Q(p)$, after accounting for the rational
coordinate change. Its Hessian at $\widehat p$ is positive definite by
the Schur complement of $\nabla^2F(p)$. If the original polynomial is
globally strongly convex, so is $\widehat F$; alternatively this follows
by restricting $F$ to the rational affine graph of $t_*$.

If (1) holds, rational SOS is preserved directly:

\[
 \widehat F(y)=\sum_j q_j(y,t_*(y))^2.
\]

Every substituted polynomial still has degree at most two. The leading
quartic form of $\widehat F$ is positive at every nonzero real $y$.
If no variables remain, the zero is rational. Thus a nonzero real
direction at infinity can be removed without increasing the field
degree or losing the relevant assumptions.

## 3. A weighted degree count handles additional components

We use the following elementary consequence of projective Bézout. If
$Z\subseteq\mathbb P^n_{\mathbb C}$ is defined by $n$ quadrics and
contains $D$ distinct isolated points, then either $Z$ is
zero-dimensional or $D\leq2^n-2$.

To see this, begin with a list containing $\mathbb P^n$ and assign an
irreducible projective variety $X$ the weight

\[
 W(X)=2^{\dim X}\deg X.
\]

Intersect the listed varieties with the quadrics one at a time. When
a quadric contains a listed variety, retain that variety. Otherwise,
replace it by the irreducible components of its intersection with the
quadric. A positive-dimensional variety of degree $\delta$ then gives
components of dimension one less and total degree at most $2\delta$,
by proper variety–hypersurface Bézout. Their total weight is no larger
than the original weight. A zero-dimensional component either stays
or disappears.

We may keep a multiset of components: duplicates and components that
later lie inside other components only overcount the total weight.
Using reduced component degrees also causes no problem, since the
Bézout degree includes intersection multiplicities and therefore bounds
their sum from above. At every stage the union of the listed varieties
is exactly the intersection of the quadrics used so far. The initial
weight is $2^n$, and the weight never increases.

At the final stage, each distinct isolated point contributes at least
one to the weight. It cannot lie on a positive-dimensional listed
variety. If $Z$ has a positive-dimensional component, some listed
variety of positive dimension must cover it and contributes at least
two more. Thus $D+2\leq2^n$, proving the assertion. This count does
not assume that any partial intersection is proper.

Now suppose, for a contradiction to (3), that
$[K:\mathbb Q]=2^n-1$. If $K_4\neq0$, Section 2 reduces to at most
$n-1$ variables, where (2) gives degree at most $2^{n-1}-1$. We may
therefore suppose that $F_4$ is positive definite.

Choose $n$ of the $q_j$ with nonsingular Jacobian at $p$, and
homogenize them to degree two in $\mathbb P^n$. Their $2^n-1$
conjugate points are distinct isolated simple points. The weighted
degree count forces the projective intersection to be zero-dimensional.
It is therefore a proper quadratic complete intersection of length
$2^n$. The conjugates each have length one, so the residual subscheme
has length one. It is defined over $\mathbb Q$ and is consequently a
reduced rational point $b$ distinct from the conjugates. This also
proves that the complete intersection is reduced everywhere.

## 4. Cayley–Bacharach finishes the convex bound

The classical Cayley–Bacharach theorem says that, for a reduced
complete intersection of degrees $d_1,\ldots,d_n$ in $\mathbb P^n$,
a hypersurface of degree $\sum_i d_i-n-1$ through all but one of the
intersection points passes through the last one. For $n$ quadrics
this degree is $n-1$. The exact statement is given on printed page 196
of Eisenbud, Green, and Harris,
[*Higher Castelnuovo theory*](https://eisenbud.github.io/papers/pdfs/1993-002.pdf)
(1993).

Choose a rational linear form $L$ with $L(b)\neq0$. For each original
quadratic, multiply its degree-two homogenization by $L^{n-3}$. The
result has degree $n-1$ and vanishes on every conjugate, so
Cayley–Bacharach forces it through $b$. Therefore every homogenized
$q_j$ vanishes at $b$. If $b$ is affine, it is
a second real zero of $F$, contradicting uniqueness. If $b$ is at
infinity, write $b=[0:d]$ with a nonzero real vector $d$. The leading
quadratic parts of all the $q_j$ vanish at $d$, so $F_4(d)=0$,
contradicting positive definiteness of $F_4$.

Degree $2^n-1$ is impossible. Combining this with the odd-degree bound
(2) proves (3). When $n=3$, the conclusion is degree at most five.

## 5. A length-three residual gives the four-variable bound eleven

We now exclude $D=2^n-3$ for $n\geq4$. If the quartic-flat space is
nonzero, Section 2 reduces to at most $n-1$ variables and gives the
smaller bound $2^{n-1}-1$. We may again assume that $F_4$ is positive
definite.

Let $W\subseteq\mathbb P^n_{\mathbb C}$ be the common zero set of
**all** degree-two homogenizations of the $q_j$. Its only real point
is $p$: the affine assertion follows from the unique real zero of
$F$, and positive definiteness of $F_4$ excludes real points at
infinity. The point $p$ is isolated even over $\mathbb C$, by the
Jacobian rank. Consequently the positive-dimensional part of $W$ has
no real points.

Choose $n$ generic rational linear combinations $h_1,\ldots,h_n$ of
the original quadrics. We can require their Jacobian to be nonsingular
at every conjugate of $p$. We can also require their intersection $Z$
to have no positive-dimensional components outside $W$. Here is an
explicit genericity argument for the latter condition. On
$U=\mathbb P^n\setminus W$, the vector of quadratic evaluations is
nonzero. If there are $m$ original quadrics and $A$ is an $n\times m$
matrix of combination coefficients, then

\[
 \mathcal I=\{(x,A)\in U\times\mathbb A^{nm}:Aq(x)=0\}
\]

has dimension $nm$: each point $x$ imposes $n$ independent linear
conditions on $A$. The generic fiber of its projection to the
coefficient space is therefore zero-dimensional or empty. Intersect
this nonempty rational open condition with the nonvanishing Jacobian
condition. A rational choice exists because $\mathbb Q$ is infinite.

Apply the weighted component construction of Section 3 to these
quadrics. The final multiset is invariant under complex conjugation,
because all the cutting equations are rational. If any positive
component remains, its total contribution to the weight is at least
four. Indeed, every such component has weight at least two, and weight
strictly below four could only consist of a single projective line
of degree one. Conjugation would preserve that line, giving real
points on it. This is impossible: the chosen positive components lie
in $W$, whose positive part has no real points.

The $D=2^n-3$ simple isolated conjugates already contribute $D$ to
the weight. A positive component would give $D+4>2^n$, a
contradiction. Hence $Z$ is a proper quadratic complete intersection
of length $2^n$. Write $\Gamma$ for the reduced degree-$D$ orbit.
The residual subscheme $R$ has length three, is defined over
$\mathbb Q$, and is disjoint from $\Gamma$. Disjointness follows
because every point of $\Gamma$ has local intersection length one.
We do **not** assume that $R$ is reduced.

For a finite projective scheme $S$, let $H_S(t)$ be the dimension of
the image of degree-$t$ homogeneous polynomials in
$H^0(S,\mathcal O_S(t))$. We claim that $H_R(1)=3$. Otherwise the
linear equations of $R$ place it scheme-theoretically in a projective
linear space of dimension at most one. A reduced projective point
cannot contain a length-three subscheme, so $R$ is contained in a
projective line $L$. Every defining quadric of $Z$ then restricts to
a degree-two polynomial on $L$ vanishing on the length-three scheme
$R$. A nonzero degree-two section on a line has a zero scheme of
length two, counting multiplicity. Thus all the quadrics vanish
identically on $L$, contradicting the zero-dimensionality of $Z$.

It follows that $H_R(t)=3$ for every $t\geq1$. To check this even
when $R$ is nonreduced, choose a linear form nonzero on the finite
support of $R$. It trivializes the relevant line bundles on $R$;
multiplication by it carries surjectivity in degree $t$ to
surjectivity in degree $t+1$.

The modern Cayley–Bacharach identity, as stated on printed page 195
of [Eisenbud, Green, and Harris](https://eisenbud.github.io/papers/pdfs/1993-002.pdf),
applies to residual subschemes of a complete intersection. Here it gives

\[
 h^0(\mathbb P^n,\mathcal I_\Gamma(2))
 -h^0(\mathbb P^n,\mathcal I_Z(2))
 =h^1(\mathbb P^n,\mathcal I_R(n-3)).
 \tag{9}
\]

The degree on the right is $n-3$, because the quadratic complete
intersection has Cayley–Bacharach degree $n-1$ and we are testing
quadratic equations. Since $n\geq4$ and $H_R(n-3)=3$, the right
side is zero. The two spaces on the left are therefore equal. Every
original quadric, which vanishes on $\Gamma$, must vanish on all of
$Z$, including $R$.

Finally a finite scheme of odd length defined over $\mathbb R$ has a
real geometric point: its nonreal geometric points occur in conjugate
pairs with equal local lengths. Thus $R$ contains a real point. It
is distinct from $p$, since $R$ is disjoint from $\Gamma$. It cannot
be at infinity, since all original quadrics vanish there and $F_4$
is positive definite. Its affine location contradicts the unique real
zero of $F$. This excludes $D=2^n-3$; oddness and (3) prove (3a).

## 6. An exact failure under only local positive curvature

Let

\[
 q_1=z-x^2,\qquad q_2=yz-y^2-1,\qquad q_3=xz+y^2,
 \qquad F=q_1^2+q_2^2+q_3^2.
 \tag{7}
\]

Every common zero has $x\neq0$ and

\[
 z=x^2,\qquad y=\frac{1-x^3}{x^2},\qquad
 P(x)=x^7+x^6-2x^3+1=0.
 \tag{8}
\]

Conversely, every root of $P$ gives a common zero by (8). The polynomial
$P$ is irreducible modulo two: for $\bar P=x^7+x^6+1$, modular
exponentiation gives $x^{128}=x$ in $\mathbb F_2[x]/(\bar P)$ and
$\gcd(\bar P,x^2-x)=1$. The prime-degree finite-field criterion proves
irreducibility. Thus $P$ is irreducible over $\mathbb Q$.

For $x\geq0$,

\[
 P(x)=x^7+(x^3-1)^2>0.
\]

For $t>0$, the coefficient sequence of
$P(-t)=-t^7+t^6+2t^3+1$ has one sign change, so Descartes' rule
permits at most one negative root of $P$. A negative root exists since
$P(-2)<0<P(-1)$. Consequently (7) has exactly one real zero, and its
joint coordinate field has degree seven.

At every solution, the Jacobian determinant of $(q_1,q_2,q_3)$ is

\[
 \det J=-\frac{P'(x)}{x^2}\neq0.
\]

Hence $\nabla^2F=2J^{\mathsf T}J\succ0$ at its unique real zero.
Nevertheless, $F_{xx}(0,0,1)=-2$, so $F$ is not globally convex.
The homogenized quadrics have the real point $[0:0:0:1]$ at infinity.
This example explains why the infinity issue cannot be dismissed using
local nondegeneracy alone.

## 7. What remains unresolved

The proof does not establish (2), (3), or (3a) for a rational quartic lacking
a rational SOS representation. For a general rational quartic with a
nondegenerate real zero at its minimum, its cubic gradient equations
give the unconditional joint-field bound $3^n$ by the same
isolated-point Bézout argument. Uniqueness of the real zero still forces
one real embedding and odd degree. A separate
[node-bound audit](quartic-zero-degree-prior.md) develops the stronger
general bound $2\,3^{n-1}-1$, using the prescribed zero value and
intersection multiplicities; that proof is outside the present SOS
argument.

The distinction between rational SOS and real SOS is substantive:
Scheiderer constructs rational forms that are SOS over $\mathbb R$ but
not over $\mathbb Q$ in
[*Sums of squares of polynomials with rational coefficients*](https://arxiv.org/abs/1209.2976),
Theorem 2.1. Those examples do not themselves provide the strongly
convex singleton counterexample sought here.

One exploratory calculation used (8). The vector space of rational
quartics vanishing together with their first derivatives on its
degree-seven orbit has dimension seven: the exact coefficient matrix
has rank 28 on the 35 monomials of degree at most four. The products
of the three quadrics span a six-dimensional subspace. A numerical
SOS-Hessian feasibility test on the full seven-dimensional space was
reported infeasible by both CLARABEL and SCS. No exact separating
certificate was extracted. This is evidence about one attempted
construction, not a proof about all convex quartics or even an exact
infeasibility proof for that subspace.

For larger dimensions the convex bound $2^n-5$ may be far from
sharp. Generalized Cayley–Bacharach bounds could help, but require
careful control of positive-dimensional intersections and residual
schemes. The five-variable case is now resolved by the separate
continuation summarized below; higher-dimensional sharpness remains open.

A stronger classical comparison is available when a proper quadratic
complete intersection $Z$ containing the orbit has been established.
Eisenbud–Green–Harris, Theorems 1–2 on printed p. 197, prove their
generalized Cayley–Bacharach bound through projective dimension six.
For a quadric $q$ not containing $Z$, it gives

\[
 \operatorname{length}(Z\cap V(q))\leq 3\,2^{n-2},
 \qquad 3\leq n\leq6.
 \tag{10}
\]

In our setting at least one original quadric must fail to contain
$Z$: otherwise its odd-length residual to the simple odd-degree orbit
would have a real point, contradicting uniqueness and the positive
quartic leading form. Thus, **conditional on the existence of this
proper complete intersection**, (10) and oddness yield
$D\leq3\,2^{n-2}-1$. This is five, eleven, twenty-three, and
forty-seven for $n=3,4,5,6$. In particular, the four-variable upper
bound eleven is also a corollary of these older intersection results
once the component issue is settled. The present note does not claim
a new general Cayley–Bacharach theorem.

For $n=5$, the later continuation closes both remaining gaps.
The [finite residual proof](degree23-residual-obstruction.md)
excludes every odd orbit degree at least twenty-three in a proper
five-quadric complete intersection. Its Frobenius quotient and
real-parity argument includes nonreduced residuals. The
[positive-base proof](five-variable-positive-base-bound.md)
then shows that a real quadratic system with at least twenty-three
simple isolated points and no real points on its positive-dimensional
base must have finite base. A weighted degree count limits the
possible positive components; each has a quadratically generated
subbase whose generic residual count is at most twenty-two.
Perturbation transfers that count to the original simple points.
The rational flat-direction reduction handles zeros at infinity.
Thus the unconditional sharp bound in the stated convex rational-SOS
class is now $D\leq21$, attained by the cyclic family. This
supersedes the earlier unresolved five-variable status.

## 8. Sources and verification record

- Eisenbud, Green, and Harris (1993), printed pp. 195–197, were examined
  in the author's PDF, including a direct image check of the modern
  residual-scheme identity. A local PDF and OCR transcript are saved in
  [quartic-degree-sources](quartic-degree-sources/eisenbud-green-harris-1993.pdf).
  Their Theorem 2 proves the stated generalized cases. Its endpoint is
  $m\leq3$, and the projective-dimension endpoint is $n\leq6$;
  the OCR incorrectly rendered some weak inequalities as strict ones.
- Scheiderer's primary paper was examined at Theorem 2.1 and its
  construction. It prevents replacing rational SOS by real SOS without
  an additional argument; it is not a novelty comparison for (3).
- An independent child reviewer checked the three-variable component count, the
  rational flat-direction reduction, the field preservation, and the
  degree-seven example. The parent independently derived the
  simultaneous rational-kernel reduction and independently accepted the
  weighted component argument used for all $n\geq3$. The parent and
  this author independently derived the generic-combination argument,
  the weight-four obstruction, and the nonreduced length-three
  interpolation argument. The parent then checked the assembled
  residual-scheme proof. This is overlapping contributor/reviewer
  verification, not a claim of a wholly uninvolved fresh review.
  These checks are evidence,
  not a formal verification of the algebraic-geometry argument.
- The targeted command
  `python research-20260927/check_quartic_zero_degree.py` checks the
  exact identities, finite-field irreducibility certificate, rational
  inverse for $y$, Jacobian nondegeneracy, and nonconvexity certificate
  in Section 6; it passed. It does not verify Bézout or Cayley–Bacharach.
- A separate scoped check of Markdown whitespace, display delimiters,
  and local links passed.
- No project-wide checks or CI status checks were performed.
