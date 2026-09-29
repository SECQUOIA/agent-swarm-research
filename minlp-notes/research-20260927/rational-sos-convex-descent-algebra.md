# Strict SOS-convexity does not force rational sums of squares

Date: 2026-09-28. Status: algebraic construction and exact dimension
checks completed; an independent algebra review is recorded below.
Publication priority has not been assessed in this note.

The [integrated result](rational-sos-convex-descent.md) combines this
algebraic proof with the explicit certificate, the literature comparison,
and the distinction between exact and strictly suboptimal SOS bounds.

There exists a rational quartic in four variables with all of the
following properties:

- Its Hessian has a positive definite rational Gram matrix on the full
  monomial vector \((v,x\otimes v)\).
- It is globally strongly convex and has minimum zero at one point.
- It is a sum of squares over the reals.
- It is **not** a sum of squares of polynomials over the rationals.

The obstruction is a coefficient of one mixed monomial. Thus rational
SOS-convexity, even with an interior Hessian certificate and rational
optimal value, does not by itself justify rational SOS descent.

## The algebraic point and its rational quadratic equations

Write

\[
 \alpha=\sqrt[3]{2},\qquad \beta=\sqrt[3]{5},\qquad
 p=(\alpha,\alpha^2,\beta,\beta^2),
\]

and use variables \((x,y,z,w)\). Define

\[
 \begin{array}{lll}
 q_1=x^2-y,&q_2=xy-2,&q_3=y^2-2x,\\
 q_4=z^2-w,&q_5=zw-5,&q_6=w^2-5z.
 \end{array}                                                   \tag{1}
\]

The field \(\mathbb Q(\alpha,\beta)\) has degree nine. Here is an
elementary proof that does not require a ramification argument. Suppose
\(\beta=a+b\alpha+c\alpha^2\) belongs to
\(K=\mathbb Q(\alpha)\), with rational \(a,b,c\). Since \(\beta\)
has degree three, it generates \(K\). Therefore its trace and the trace
of its square are zero. The first equality gives \(a=0\); the second
gives \(12bc=0\). If \(c=0\), then \(b^3=5/2\), and if \(b=0\),
then \(c^3=5/4\). Neither number is a rational cube. Thus
\(\beta\notin K\). If \(T^3-5\) were reducible over the real field
\(K\), it would have a root in \(K\), necessarily its unique real root
\(\beta\). It is consequently irreducible over \(K\), proving degree
nine.

The nine numbers

\[
 \alpha^i\beta^j\quad(0\leq i,j\leq2)
                                                               \tag{2}
\]

are a rational basis of this field. Evaluating polynomials of total
degree at most two at \(p\) maps onto that basis: the four mixed basis
members are represented by \(xz,xw,yz,yw\), and the other five by
\(1,x,y,z,w\). There are fifteen monomials of total degree at most two.
Hence the rational vector space

\[
 I_2=\{q\in\mathbb Q[x,y,z,w]:\deg q\leq2,\ q(p)=0\}
\]

has dimension six. The six polynomials (1) are linearly independent,
so they form a basis of \(I_2\).

Let \(W\) be the rational span of all products of two members of
\(I_2\). Every member of \(W\) has coefficient zero on \(yz^3\).
Indeed, products of two quadratics from the same block are independent
of the other block. Products from different blocks have degree at most
two in \((x,y)\) and at most two in \((z,w)\). Neither type contains
\(yz^3\).

## A rational perturbation outside the required SOS space

Set

\[
 g(z,w)=z^3+\frac{w^3}{5}-3zw+5,
 \qquad h(x,y,z,w)=y\,g(z,w).                         \tag{3}
\]

At \((z,w)=(\beta,\beta^2)\),

\[
 g=0,\qquad g_z=3z^2-3w=0,\qquad
 g_w=\frac35(w^2-5z)=0.
\]

Consequently \(h(p)=0\) and \(\nabla h(p)=0\). But the coefficient
of \(yz^3\) in \(h\) is one, so \(h\notin W\).

This does not contradict membership in the ordinary square of the
vanishing ideal. In fact,

\[
 q_4q_6-q_5^2=-5g,
 \qquad h=-\frac y5(q_4q_6-q_5^2).                  \tag{4}
\]

Equation (4) uses products whose individual factors exceed the degree
bound required for quartic SOS summands. The cancellation of their
degree-five terms leaves a quartic outside \(W\).

For any rational \(c>0\), the same cubic identity is

\[
 c\left(z^3+\frac{w^3}{c}-3zw+c\right)
   =(zw-c)^2-(z^2-w)(w^2-cz).
\]

For \(c=2\), twice the cubic is the polynomial
\(2z^3+w^3-6zw+4\) in the prior Bienstock--Del Pia--Hildebrand
example discussed in
[the publication assessment](convex-quartic-publication-assessment.md).
Thus that cubic itself is not new. Here it is multiplied by a coordinate
from an independent cubic block to obtain the rational SOS obstruction.

## The general perturbation principle

The mechanism can be stated independently of the example. Fix a real
point \(a\), and let \(I_2(a)\) be the rational polynomials of degree
at most two that vanish at \(a\). Let \(W(a)\) be the rational span
of products of pairs of members of \(I_2(a)\). Suppose:

1. A rational SOS quartic \(G\) vanishes at \(a\) and has a positive
   definite rational Hessian Gram matrix on the full basis
   \((v,X\otimes v)\).
2. A rational polynomial \(h\) of degree at most four satisfies
   \(h(a)=0\), \(\nabla h(a)=0\), and \(h\notin W(a)\).

Then \(\lambda G+h\), for every sufficiently large rational
\(\lambda>0\), is globally strongly convex, has unique minimum zero
at \(a\), has a positive definite rational Hessian Gram matrix, and
is real SOS but not rational SOS.

The proof is given below for the explicit example and uses only the
two displayed assumptions. Positive definite Hessian Gram matrices
form an open cone; every rational quartic perturbation has some rational
Hessian Gram matrix; and rational SOS at \(a\) would force membership
in \(W(a)\). These facts explain why strict SOS-convexity can coexist
with a rational SOS obstruction.

## A rational baseline with an interior Hessian Gram matrix

We next construct a rational SOS quartic \(G\) such that \(G(p)=0\)
and the Hessian of \(G\) has a positive definite Gram matrix on the full
basis \((v,(x,y,z,w)\otimes v)\), where \(v\in\mathbb R^4\).
The direct sum of two block quartics would not automatically give this
interior property. Instead, combine their exposing quadratics before
squaring.

For a positive real number \(r\), put

\[
 E_r(X,Y)=r^2(X^2-Y)-r(XY-r^3)+(Y^2-r^3X).
\]

Writing \(X=r+u\) and \(Y=r^2+t\) gives

\[
 E_r(r+u,r^2+t)=r^2u^2-rut+t^2.
                                                               \tag{5}
\]

The associated symmetric matrix has positive determinant
\(3r^2/4\) and positive diagonal entries. Thus

\[
 E_*=E_\alpha(x,y)+E_\beta(z,w)
\]

is a positive definite quadratic in coordinates centered at \(p\),
and is a real linear combination of (1). Write this centered expression
as \(u^{\mathsf T}Hu\), with \(H\succ0\).

Let \(J\) be the matrix whose rows are \(\nabla q_i(p)^{\mathsf T}\).
It has rank four: in each block the first two equations have Jacobian
determinant \(3r^2\ne0\). For a sufficiently large positive integer
\(N_0\), put \(\varepsilon=N_0^{-2}\) and consider the real-coefficient
polynomial

\[
 G_*=E_*^2+\varepsilon\sum_{i=1}^6q_i^2.
                                                               \tag{6}
\]

The exact centered Hessian Gram formula in
[the quartic Hessian construction](sos-convex-quartic-realization.md)
has constant block \(2\varepsilon J^{\mathsf T}J\), cross block of
order \(\varepsilon\), and quadratic block

\[
 8\operatorname{vec}(H)\operatorname{vec}(H)^{\mathsf T}
       +4H\otimes H+O(\varepsilon).
\]

The quadratic block is positive definite for sufficiently small
\(\varepsilon\). Its Schur complement is
\(2\varepsilon J^{\mathsf T}J-O(\varepsilon^2)\), also positive
definite for sufficiently small \(\varepsilon\). This proves that
the full Gram matrix is positive definite.

Fix such a rational \(\varepsilon>0\). Approximate the six real
coefficients expressing \(E_*\) in the basis (1) by rational numbers,
obtaining a rational quadratic \(E\). It still satisfies \(E(p)=0\).
For sufficiently close approximation the same centered Gram formula
remains positive definite by continuity. Hence

\[
 G=E^2+\varepsilon\sum_{i=1}^6q_i^2                 \tag{7}
\]

is rational, vanishes at \(p\), and has a real positive definite
Hessian Gram matrix. It is explicitly rational SOS because
\(\varepsilon q_i^2=(q_i/N_0)^2\).

The change from centered to original variables is an invertible
congruence, so the Hessian has a positive definite Gram matrix on the
specified original full basis as well. The coefficient equations for
that Gram matrix are rational affine equations. A consistent rational
linear system has a rational solution and a rational basis for its
homogeneous solution space. Rational points are therefore dense in its
real affine solution space. Positive definiteness is open, so a rational
positive definite Gram matrix \(M\) exists. This is an existence proof
with effective choices available from the quantitative construction
cited above; no polynomial coefficient-size claim is needed here.

## The counterexample

The Hessian biform of any rational quartic, including \(h\), has some
symmetric rational Gram matrix \(N\) on the same full basis. To see
surjectivity directly, its monomials have degree two in \(v\) and degree
at most two in \((x,y,z,w)\); each is a product of two entries of that
basis. Splitting coefficients between symmetric entries gives \(N\).
No positivity is asserted for \(N\).

Choose a sufficiently large positive rational \(\lambda\) so that
\(\lambda M+N\succ0\), and set

\[
 F=\lambda G+h.                                    \tag{8}
\]

This is a rational quartic with a positive definite rational Hessian
Gram matrix. If \(\mu=\lambda_{\min}(\lambda M+N)>0\), then

\[
 v^{\mathsf T}\nabla^2F(x,y,z,w)v\geq\mu\|v\|^2
\]

everywhere, because the full basis contains \(v\) as its first block.
Also \(F(p)=0\) and \(\nabla F(p)=0\), so integration along the
segment from \(p\) gives

\[
 F(X)\geq\frac\mu2\|X-p\|^2.
\]

Thus \(F\) is globally strongly convex and its unique zero is \(p\).
Taylor integration of its SOS Hessian at \(p\) gives a real SOS
representation of \(F\). More explicitly, substituting
\(X=p+t(X-p)\) into the Hessian Gram identity and integrating with
weight \(1-t\) gives a positive semidefinite Gram matrix for a vector
of real quadratics in \(X\). This argument gives real coefficients,
not rational ones.

Suppose instead that \(F=\sum_j f_j^2\), with rational polynomials
\(f_j\). Every \(f_j\) has degree at most two: the highest homogeneous
parts of squares cannot cancel. Since \(F(p)=0\) and \(p\) is real,
every \(f_j(p)=0\). Hence every \(f_j\in I_2\) and \(F\in W\).
But \(G\in W\), while the coefficient of \(yz^3\) in \(h\) is one.
Therefore the coefficient of \(yz^3\) in \(F\) is one, contradicting
\(F\in W\). This proves the asserted failure of rational SOS descent.

The argument also excludes positive rational weighted SOS
representations of quadratic polynomials, since they too belong to
\(W\).

## One concrete rational polynomial

The following choices remove the existential approximation and scaling
steps. Put \(D=2^{31}\) and

\[
 \begin{array}{ll}
 S_2=2705659852/D,&R_2=3408917801/D,\\
 S_5=3672145383/D,&R_5=6279280279/D,
 \end{array}
\]

and, using the quadratics (1), set

\[
 \begin{aligned}
 E&=R_2q_1-S_2q_2+q_3+R_5q_4-S_5q_5+q_6,\\
 F&=2^{40}\left[E^2+2^{-26}
                   (q_1^2+q_2^2+q_4^2+q_5^2)\right]+h.
 \end{aligned}                                                   \tag{9}
\]

The [exact checker](check_rational_sos_convex_descent.py) builds a
\(20\times20\) rational Hessian Gram matrix at the rational center
\((S_2,R_2,S_5,R_5)\). It verifies its polynomial coefficient identity
and an exact rational \(LDL^{\mathsf T}\) factorization with all
twenty diagonal pivots positive. The rational change from this center
to the original variables gives the required original-basis certificate
by congruence. It also verifies the zero, first derivatives, quadratic
vanishing-space basis, and the coefficient obstruction. These checks
establish the claimed properties of this particular polynomial without
depending on estimates for the approximation errors or for the required
scaling factor.

## Verification and limits

An exact SymPy calculation formed the evaluation matrix for all fifteen
quadratic monomials over the basis (2), the first-jet evaluation matrix
for all seventy quartic monomials, and the coefficient matrix of all
products of a basis of \(I_2\). It returned

\[
 \dim I_2=6,\qquad \dim W=21,\qquad
 \dim\{f:\deg f\leq4,\ f(p)=\nabla f(p)=0\}=25.
\]

The computation supplied (3); the proof above independently replaces
its crucial membership tests with a field-basis argument and the
single coefficient \(yz^3\). A separate algebra reviewer independently
checked the field-degree proof, the full-basis Hessian construction,
and the explicit perturbation. That reviewer commissioned a fresh
further review, which also found no gap. Their initial symbolic checks
used the equivalent second radicand three; the author reran the checks
with the radicand five used here.

The targeted command

```bash
python research-20260927/check_rational_sos_convex_descent.py
```

passed. A separate author-side `python - <<'PY'` calculation checked
the radicand-five identities, all three matrix ranks above, the exposing
identity (5), and this note's local links, paired mathematical display
delimiters, trailing whitespace, and final newline. Those checks passed.
No Lean proof, project-wide verification, or CI inspection was used.

This is a counterexample construction, not a solver hardness result.
It does not contradict the rational SOS certificates in the existing
quartic constructions, which explicitly square rational quadratics.
It does show that their rational SOS hypothesis cannot be replaced by
a rational positive definite Hessian Gram hypothesis merely by invoking
Taylor's formula. The previously known general failure of rational SOS
descent is discussed in
[the quartic degree audit](quartic-zero-degree-adversarial.md); the
additional convex assumptions in the present construction require a
separate literature comparison before any novelty claim.
