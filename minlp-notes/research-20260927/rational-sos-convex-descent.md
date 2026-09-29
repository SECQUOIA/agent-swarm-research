# A strongly SOS-convex rational quartic without a rational SOS decomposition

Date: 2026-09-28. Status: explicit construction, exact certificate, and
integrated proofs passed independent adversarial review. Literature
priority is not established.

The later [three-variable construction](ternary-rational-sos-convex-counterexample.md)
reduces the dimension, uses small integer coefficients, and determines
the coefficient fields admitting SOS or PSD Gram certificates. The
four-variable example below remains useful because its obstruction is
failure of membership in the span of products of rational vanishing
quadratics, rather than failure of positivity within that span.

Rational SOS-convexity does **not** make an attained rational minimum
certifiable by a rational SOS decomposition of the objective minus its
minimum. This remains false with a positive definite rational Hessian
Gram matrix, global strong convexity, and just four variables.

The quartic below has minimum zero at

\[
 a=(\sqrt[3]2,\sqrt[3]4,\sqrt[3]5,\sqrt[3]{25}).
\]

It is SOS over the reals and has a rational positive definite Hessian
Gram certificate, but it is not SOS over the rationals. For every
positive rational \(\eta\), the polynomial \(F+\eta\) is rational
SOS. Thus the real SOS optimization problem attains its exact lower
bound, while rational SOS lower bounds approach that bound without
attaining it. This is an arithmetic obstruction, not nonattainment of
the real semidefinite program or a complexity lower bound.

## The explicit polynomial

Set

\[
\begin{aligned}
 s_2&=\frac{676414963}{536870912},&
 t_2&=\frac{3408917801}{2147483648},\\
 s_5&=\frac{3672145383}{2147483648},&
 t_5&=\frac{6279280279}{2147483648},
\end{aligned}
\]

and define the rational quadratic

\[
\begin{aligned}
 A={}&y^2-2x+t_2(x^2-y)-s_2(xy-2)\\
     &+w^2-5z+t_5(z^2-w)-s_5(zw-5).
\end{aligned}
\]

The counterexample is

\[
\boxed{\begin{aligned}
 F(x,y,z,w)={}&2^{40}\left(A^2+2^{-26}\left[
  (x^2-y)^2+(xy-2)^2+(z^2-w)^2+(zw-5)^2\right]\right)\\
 &+y\left(z^3+\frac{w^3}{5}-3zw+5\right).
\end{aligned}} \tag{1}
\]

The constants \(s_c,t_c\) are the downward approximations of
\(c^{1/3},c^{2/3}\) to denominator \(2^{31}\), reduced as
fractions. Approximations only select rational coefficients. No rounded
algebraic equality is used: every quadratic inside the first line of
(1) vanishes exactly at \(a\).

Write

\[
 h=yC(z,w),\qquad C=z^3+w^3/5-3zw+5.
\]

At \((z,w)=(\beta,\beta^2)\), with \(\beta^3=5\), one has

\[
 C=0,\qquad C_z=3z^2-3w=0,\qquad C_w=3w^2/5-3z=0.
\]

Therefore \(F(a)=0\) and \(\nabla F(a)=0\). The Hessian
certificate below makes \(F\) globally strongly convex. It follows
that \(a\) is its unique global minimizer and its unique real zero.

## An exact rational Hessian certificate

The [targeted checker](check_rational_sos_convex_descent.py) constructs
the certificate by the following rational formulas. They specify the
matrix without a large table of fractions.

Put \(c=(s_2,t_2,s_5,t_5)\), \(u=(x,y,z,w)-c\), and let \(v\)
be an arbitrary direction. For each rational quadratic \(q\), write

\[
 q(c+u)=d+b^{\mathsf T}u+u^{\mathsf T}Tu.
\]

On the 20-entry monomial vector
\(Z=(v,u\otimes v)\), the directional Hessian of \(q^2\) has
the symmetric rational Gram matrix

\[
 \mathcal M(q)=\begin{pmatrix}C&D\\D^{\mathsf T}&Q\end{pmatrix},
\]

where, indexing the tensor coordinates by \((k,j)\),

\[
\begin{aligned}
 C&=2bb^{\mathsf T}+4dT,\\
 D_{i,(k,j)}&=2b_kT_{ij}+4b_iT_{kj},\\
 Q&=8\operatorname{vec}(T)\operatorname{vec}(T)^{\mathsf T}
       +4T\otimes T.
\end{aligned} \tag{2}
\]

The term \(4dT\) is essential because the center \(c\) is rational,
not the exact zero. Formula (2) follows by differentiating the square.

Let \(B\) be the rational Gram matrix of
\(v^{\mathsf T}\nabla^2h(c+u)v\) obtained as follows. For each
monomial, distribute its coefficient equally among all ordered entries
\((i,j)\) for which \(Z_iZ_j\) is that monomial. This gives a
symmetric matrix and counts off-diagonal entries twice, as required.
Every monomial in this Hessian biform occurs in such a product.

For \(r_1=x^2-y,r_2=xy-2,r_3=z^2-w,r_4=zw-5\), set

\[
 M=2^{40}\left(\mathcal M(A)+2^{-26}\sum_{j=1}^4
          \mathcal M(r_j)\right)+B. \tag{3}
\]

Exact rational computation verifies

\[
 v^{\mathsf T}\nabla^2F(c+u)v=Z^{\mathsf T}MZ,
 \qquad M=LDL^{\mathsf T},\qquad D_{ii}>0\ (1\le i\le20).
 \tag{4}
\]

The checker expands the differentiated identity and verifies the exact
factorization. Each entry of \(M\) has numerator and denominator bit
length at most 103. Every diagonal pivot is in fact greater than one;
this observation does not assert a corresponding lower bound for the
smallest eigenvalue of \(M\).

Since \(M\succ0\) and \(\|Z\|^2\ge\|v\|^2\), (4) proves
\(\nabla^2F\succeq\lambda_{\min}(M)I\succ0\) globally. The
rational change from \((v,u\otimes v)\) to
\((v,(x,y,z,w)\otimes v)\) is invertible. Congruence therefore also
gives a rational positive definite Gram matrix on the requested original
monomial vector. Its rational positive pivots supply a rational SOS
certificate for the Hessian biform; positive rational weights can be
expanded into rational squares.

No numerical semidefinite solution is used to establish (4). The exact
checker is a finite certificate verification, not a formal proof of the
Python interpreter or the symbolic algebra library. A separate
[algebraic construction](rational-sos-convex-descent-algebra.md) explains
why a sufficiently large multiplier must work, independently of the
chosen numerical constants.

## Why no rational SOS decomposition exists

Let \(\alpha^3=2\) and \(\beta^3=5\) denote the real roots.
The field \(K=\mathbb Q(\alpha,\beta)\) has degree nine. Here is
an elementary proof. If \(T^3-5\) were reducible over the real cubic
field \(\mathbb Q(\alpha)\), it would have a root there, necessarily
\(\beta\). Write \(\beta=b_0+b_1\alpha+b_2\alpha^2\).
The equality of the two cubic fields would give
\(\operatorname{Tr}(\beta)=\operatorname{Tr}(\beta^2)=0\).
Taking traces gives \(b_0=0\) and \(12b_1b_2=0\). Thus either
\(b_1^3=5/2\) or \(b_2^3=5/4\), impossible for rational
\(b_1,b_2\). This proves the degree claim.

Let \(I_2\) be the vector space of rational polynomials of degree at
most two vanishing at \(a\). There are 15 monomials of degree at
most two. Their evaluations span \(K\), because they include all nine
basis elements \(\alpha^i\beta^j\), \(0\le i,j\le2\).
Therefore \(\dim_{\mathbb Q}I_2=6\). Its basis is

\[
 x^2-y,\quad xy-2,\quad y^2-2x,\quad
 z^2-w,\quad zw-5,\quad w^2-5z. \tag{5}
\]

Every product of two polynomials in (5) has coefficient zero on
\(yz^3\). Products within a block involve only that block; products
from different blocks have degree at most two in each block. Thus the
same is true for every element of

\[
 W=\operatorname{span}_{\mathbb Q}\{qr:q,r\in I_2\}.
\]

The squared part of (1) lies in \(W\), but \(h\) has coefficient
one on \(yz^3\). Hence \(F\notin W\).

If \(F=\sum_j q_j^2\) with rational polynomial \(q_j\), the
degree bound on \(F\) forces every \(q_j\) to have degree at most
two: highest-degree real squares cannot cancel. Since \(F(a)=0\),
each \(q_j(a)=0\), so \(q_j\in I_2\). This would put \(F\)
in \(W\), a contradiction. The same obstruction excludes rational
positive semidefinite Gram matrices for \(F\), and positive rational
weighted SOS representations.

## Arbitrarily close rational SOS certificates

The following statement explains the boundary behavior and does not
depend on the particular counterexample.

**Lemma.** Suppose a rational quartic \(P\) has a positive definite
Hessian Gram matrix on \((v,x\otimes v)\), and its minimum is zero.
For every positive rational \(\eta\), \(P+\eta\) has a rational
positive definite polynomial Gram matrix, hence a rational SOS
decomposition.

**Proof.** Let \(a\) be the minimizer and translate the Hessian
certificate to \(u=x-a\). The translated real Gram matrix is positive
definite. For some \(\mu>0\), subtracting \(\mu I\) leaves a
positive semidefinite matrix. Taylor's formula at the stationary zero is

\[
 P(a+u)=\int_0^1(1-t)u^{\mathsf T}\nabla^2P(a+tu)u\,dt.
\]

Substituting the translated Gram identity and integrating shows that

\[
 P(a+u)-\frac\mu2\|u\|^2-\frac\mu{12}\|u\|^4
\]

is a real SOS of polynomials of degree at most two. Integration of its
Gram matrix preserves positive semidefiniteness. The displayed positive
quadratic and quartic terms have a diagonal positive definite Gram
matrix on all nonconstant monomials of degree at most two:
\(\|u\|^4=\sum_i u_i^4+2\sum_{i<j}u_i^2u_j^2\).
Adding \(\eta\) makes the Gram matrix positive definite on the full
monomial basis, including the constant. Translating back preserves this
property. The affine equations for a Gram matrix of the rational
polynomial \(P+\eta\) are rational. Rational points are dense in
that affine space, and positive definiteness is open, so it contains a
rational positive definite Gram matrix. Rational \(LDL^{\mathsf T}\)
and the four-square theorem turn this into rational polynomial squares.
\(\square\)

In particular \(F\) itself is real SOS, by the same Taylor formula,
but

\[
 \sup\{\gamma\in\mathbb Q:F-\gamma\text{ is rational SOS}\}=0
\]

is not attained. Every negative rational \(\gamma\) is feasible;
zero is excluded by (5); positive \(\gamma\) is excluded by evaluating
at \(a\). The lemma makes no polynomial bit-size or uniform algorithmic
claim about these certificates as \(\eta\downarrow0\).

## Comparison with prior results and significance

The [primary-literature audit](rational-sos-convex-descent-prior.md)
records the sources and comparisons in detail. Scheiderer established
that rational real-SOS polynomials need not be rational SOS. His
ternary-quartic classification also rules out this phenomenon for a
bivariate nonnegative quartic with a unique nondegenerate real zero of
odd field degree. [Published primary text, Theorem 4.1](https://ems.press/content/serial-article-files/32129).

Odd degree does not restore polynomial SOS descent: a quartic attributed
to Capco, Laplagne, and Scheiderer is SOS over
\(\mathbb Q(\sqrt[3]2)\) but not over \(\mathbb Q\). Laplagne
reproduces it and proves this property, and also constructs strictly
positive real-SOS forms with no rational SOS decomposition. Those
displayed examples are nonconvex, as checked in the audit.
[Primary text, Proposition 3.1 and Theorem 3.4](https://arxiv.org/pdf/2312.16801).

The combination established here is the simultaneous presence of
global strong convexity, a rational positive definite Hessian Gram
certificate, a unique irrational zero with rational objective value,
and failure of rational polynomial SOS descent. The general existence
of irrational SOS certificates, rational approximation inside the SOS
cone, and real SOS consequences of SOS-convexity are prior results.
No priority claim follows from the unsuccessful search for this exact
combination of hypotheses.

The cubic used in the perturbation also has close prior: the identity
\(5C=(zw-5)^2-(z^2-w)(w^2-5z)\) generalizes the cubic
\(2z^3+w^3-6zw+4\) in Bienstock--Del Pia--Hildebrand's Example 1.
The present obstruction couples that cubic to an independent block and
preserves a strict global Hessian certificate.
[Primary paper, Example 1](https://optimization-online.org/wp-content/uploads/2020/11/8105.pdf).

Arithmetic nonattainment with a rational optimum and Slater feasibility
is also a broader prior phenomenon: any old rational real-SOS form
without rational SOS gives it by minimizing \(t\ge0\) subject to
\(p+t\sum m_i^2\) being SOS, where the \(m_i\) are the full
degree-half monomial basis. Positive \(t\) creates an interior Gram
matrix. The distinction here is the ordinary constant lower-bound
perturbation \(F+\eta\) for a globally strongly convex quartic with
a strict rational Hessian certificate; the audit spells out this
comparison.

For exact optimization this separates two tasks: certifying convexity
with rational data and certifying the exact optimum by rational SOS.
The former does not guarantee the latter, even when the Hessian
certificate is strictly positive definite. Real or algebraic SOS
certificates remain available. The example does not imply NP-hardness,
failure of approximate optimization, or a lower bound for arbitrary
certificate systems. It blocks extending the repository's field-degree
bounds for rational SOS quartics merely by asserting automatic rational
descent from SOS-convexity. Its degree nine does not itself violate those
bounds in four variables.

## Verification and remaining questions

Command actually run:

```text
python research-20260927/check_rational_sos_convex_descent.py
```

It passed exact differentiation, rational Gram construction, rational
positive-pivot factorization, algebraic zero and stationarity,
quadratic evaluation rank, the six-dimensional vanishing-space basis,
and the forbidden-coefficient check. An initial run reached the positive
Gram check but stopped at a polynomial-domain mismatch; setting the
reduction domain to \(\mathbb Q\) fixed the checker, and the full
rerun passed. No numerical solver, project-wide tests, CI inspection,
or Lean verification was used.

The [fresh adversarial review](rational-sos-convex-descent-review.md)
checks the field argument, the perturbation construction, the explicit
certificate, the no-SOS argument, and the positive-constant lemma.
Independent finite calculations support the identities; the field and
convexity conclusions use the proofs above. The prior audit derives an
affirmative answer in two affine variables from Scheiderer's published
classification. The later three-variable construction closes this
dimension gap within the full positive definite Hessian Gram class.
Broader degree bounds without rational SOS remain separate questions.
