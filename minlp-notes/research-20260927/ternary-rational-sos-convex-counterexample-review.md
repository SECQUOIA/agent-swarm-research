# Independent review of the three-variable rational SOS obstruction

Date: 2026-09-28. Status: the algebraic obstruction, qualitative
strict-Hessian construction, and explicit rational Hessian certificate
pass independent review. This note does not establish literature priority.

The complete [main draft](ternary-rational-sos-convex-counterexample.md)
was read after its explicit certificate and coefficient-field discussion
were written; no blocking defect was found.

The proposed construction uses the positive real root \(a\) of
\(T^5-2\), the point

\[
 p=(a^{-1},a,a^{-3}),
\]

and five rational quadratics

\[
\begin{aligned}
 q_0&=1-xy,&q_1&=x^2-yz,&q_2&=y^2-2z,\\
 q_3&=z^2-x/2,&q_4&=xz-y/2.
\end{aligned}
\]

Let \(G\) be the three-variable specialization of the
[cyclic construction](cyclic-quartic-exponential-degree.md), or another
rational sum of squares of linear combinations of \(q_0,\ldots,q_3\)
with a rational positive definite Hessian Gram matrix on the full basis
\((v,(x,y,z)\otimes v)\). The candidate is

\[
 F=\lambda G-q_4^2
\]

for a sufficiently large positive rational \(\lambda\).

## The coordinate field and the complete vanishing space

Eisenstein's criterion at two proves \([\mathbb Q(a):\mathbb Q]=5\).
The coordinate \(y=a\) generates this field, so the joint coordinate
field of \(p\) also has degree five. In the basis
\((1,a,a^2,a^3,a^4)\), the ten quadratic monomials evaluate as follows:

| Monomial | Value at \(p\) |
| --- | --- |
| \(1\) | \(1\) |
| \(x\) | \(a^4/2\) |
| \(y\) | \(a\) |
| \(z\) | \(a^2/2\) |
| \(x^2\) | \(a^3/2\) |
| \(xy\) | \(1\) |
| \(xz\) | \(a/2\) |
| \(y^2\) | \(a^2\) |
| \(yz\) | \(a^3/2\) |
| \(z^2\) | \(a^4/4\) |

The evaluation map has rank five. Its kernel
\(I_2=\{q\in\mathbb Q[x,y,z]_{\leq2}:q(p)=0\}\) therefore has
dimension five. The displayed \(q_i\) vanish at \(p\) and are
linearly independent, proving that they form a basis. This checks the
whole vanishing space, not merely five convenient relations.

## A two-coefficient obstruction replaces Gram uniqueness

For a quartic \(P\), write \([m]P\) for its coefficient on the
monomial \(m\), and define

\[
 L(P)=2[z]P+4[y^2]P.
\]

Direct expansion gives

\[
 L(q_iq_j)=
 \begin{cases}1,&i=j=4,\\0,&\text{otherwise}.
 \end{cases}
\]

Indeed the only product besides \(q_4^2\) that contributes either
of these monomials is \(q_0q_2\), whose relevant part is
\(y^2-2z\), annihilated by \(L\). The \(y^2\) coefficient of
\(q_4^2\) is \(1/4\). Consequently

\[
 L\left(\left(\sum_{i=0}^4c_iq_i\right)^2\right)=c_4^2.
\]

Since \(G\) uses only the first four quadratics, \(L(G)=0\) and
\(L(F)=-1\). If \(F\) were rational SOS, every summand would
have degree at most two: the top homogeneous parts of real squares
cannot cancel. Evaluating at its real zero \(p\) then forces every
summand to belong to \(I_2\). The displayed identity would imply
\(L(F)\geq0\), a contradiction.

The functional is **not** nonnegative on all polynomial squares:
\(L((1-z)^2)=-4\). Its positivity applies only after rationality and
vanishing at \(p\) have restricted the summands to \(I_2\).
Thus this argument is consistent with the real SOS representation
obtained from the Hessian certificate.

An independent exact calculation also checked that the fifteen products
\(q_iq_j\), \(i\leq j\), are linearly independent. In the column
order induced by lexicographic order on \((i,j)\), the rows indexed by

\[
 1,x,y,z,x^2,xy,xz,y^2,yz,z^2,x^2y,x^2z,x^3,xz^2,x^2yz
\]

form a square coefficient matrix of determinant \(1/16\). Therefore
the alternative unique-Gram argument is also valid. Its extra matrix
calculation is unnecessary once the functional \(L\) is available.

## Independent check that the required baseline exists

The cyclic construction's exposing quadratic specializes to

\[
 E_*=q_0+a^2q_1+a^{-2}q_2+a^6q_3.
\]

Put \(X_0=1\), \(X_1=x/a^{-1}\), \(X_2=y/a\), and
\(X_3=z/a^{-3}\), with cyclic indices modulo four. Substitution gives

\[
 E_*=\frac12\sum_{i=0}^3(X_i-X_{i+1})^2.
\]

Thus \(E_*\) is a positive definite quadratic centered at \(p\).
The Jacobian rows of \(q_0,q_1,q_2\) have determinant
\(-10a^{-2}\) at \(p\), so the four residuals have full Jacobian
rank three there.

For sufficiently small positive rational \(\epsilon\), the quartic

\[
 E_*^2+\epsilon\sum_{i=0}^3q_i^2
\]

has a positive definite Gram matrix for its Hessian biform in centered
coordinates. To check the decisive point, write
\(E_*(p+u)=u^{\mathsf T}Hu\), \(H\succ0\), and let \(J\)
be the residual Jacobian. The Gram matrix on
\((v,u\otimes v)\) has constant block
\(2\epsilon J^{\mathsf T}J\), cross block \(O(\epsilon)\),
and lower block

\[
 8\operatorname{vec}(H)\operatorname{vec}(H)^{\mathsf T}
 +4H\otimes H+O(\epsilon).
\]

The lower block is positive definite for small \(\epsilon\); its
Schur complement is
\(2\epsilon J^{\mathsf T}J-O(\epsilon^2)\succ0\).
This verifies strict positivity on the full twelve-entry basis rather
than only pointwise positivity of the Hessian.

Approximate the coefficients of \(E_*\) by rational numbers within
\(\operatorname{span}(q_0,\ldots,q_3)\). For sufficiently close
approximation \(E\), the same strict Gram property persists and
\(E(p)=0\) remains exact. The resulting
\(G=E^2+\epsilon\sum_{i=0}^3q_i^2\) is rational SOS. Positive
rational weights can be absorbed into rational squares. Removing the
translation gives an invertible Gram congruence. The coefficient
equations for a Hessian Gram matrix of this rational polynomial form
a rational affine space. Rational points are dense in that affine
space, so it contains a rational positive definite Gram matrix.

This supplies a self-contained qualitative check of the imported cyclic
baseline. It does not certify any particular numerical coefficient choice.

## Perturbation, minimum, and certificate scope

The Hessian biform of \(q_4^2\) has some rational symmetric Gram
matrix \(N\) on the same full basis: every monomial of its biform is
a product of two basis entries. If \(M\succ0\) is a rational Hessian
Gram for \(G\), then \(\lambda M-N\succ0\) for sufficiently
large rational \(\lambda\). No positivity of \(N\) is needed.
The basis includes the direction coordinates \(v\), so this matrix
proves a global positive lower bound on \(\nabla^2F\).

Every \(q_i\) vanishes at \(p\). Thus \(F(p)=0\) and
\(\nabla F(p)=0\), independently of its negative square.
Strong convexity then gives
\(F(X)\geq\mu\|X-p\|^2/2\) for some \(\mu>0\).
In particular \(F\) has minimum zero and a unique real zero.
The strict Hessian certificate also supplies a real SOS by Taylor
integration at \(p\); it does not supply a rational SOS.

The argument proves existence in three affine variables and field degree
five. It does not prove a complexity lower bound. Combined with the
separately reviewed two-variable descent theorem, it would make three
the smallest affine dimension under these exact hypotheses. That final
comparison depends on Scheiderer's primary classification as recorded
in [the existing literature audit](rational-sos-convex-descent-prior.md),
not on the product-rank calculation here.

## Independent verification of the explicit integer polynomial

The author's explicit choice is considerably smaller than the qualitative
construction requires. Set \(r_i=2q_i\),

\[
 A=4r_0+5r_1+3r_2+9r_3,\qquad
 F=A^2+\sum_{i=0}^3r_i^2-r_4^2.
\]

The [targeted checker](check_ternary_rational_sos_convex_counterexample.py)
specifies a rational twelve-by-twelve Hessian Gram matrix \(M\) in the
coordinates \(u=(x,y,z)-(3/4,1,1/2)\). I reconstructed that matrix from
the coefficients of each shifted quadratic, without importing the
author's checker, and checked the fully differentiated polynomial
identity on \((v,u\otimes v)\).

Instead of repeating the author's positive-pivot factorization, I checked
Sylvester's criterion directly. The twelve exact leading principal
minors of \(M-I\), in order, are

\[
\begin{aligned}
&49,\quad 4357/2,\quad 530263/4,\quad 377023825/4,\\
&63225558167/4,\quad 24263050990949/4,\\
&4133378376865537/4,\quad205994934582134805/2,\\
&31940653902803489781/2,\quad9211556528250690277317/2,\\
&2186318040815874179080883/2,\quad
1202961604425506259443507567/4.
\end{aligned}
\]

All are positive. Hence \(M-I\succ0\) and
\(\nabla^2F\succeq I\) globally. The rational translation back to
the original monomial basis preserves a rational positive definite Gram
certificate by congruence; it need not preserve the particular matrix
lower bound \(M\succ I\). The global Hessian bound already follows
in the centered coordinates because the Gram vector includes \(v\).

Exact reduction modulo \(T^5-2\) also verified \(F(p)=0\),
\(\nabla F(p)=0\), and all five residual equations. On this scaled
basis, \(L(r_i r_j)=4\delta_{i4}\delta_{j4}\), and direct coefficient
extraction gives \(L(F)=-4\). The conditional coefficient argument
therefore proves that this particular small polynomial is not rational
SOS. No approximation or asymptotic choice remains in its certificate.

## Exact coefficient-field requirement

The same argument proves the following stronger statement for the explicit
polynomial: for every subfield \(E\subseteq\mathbb R\),

\[
 F\text{ is SOS in }E[x,y,z]
 \quad\Longleftrightarrow\quad a\in E.
\]

Here is an independent proof of both directions. If \(a\notin E\),
then \(T^5-2\) is irreducible over \(E\). Indeed, a proper monic
factor of degree \(r\in\{1,2,3,4\}\) would have constant term
\((-1)^ra^r\zeta_5^k\). This constant is real, so the fifth root
of unity \(\zeta_5^k\) must equal one. Hence \(a^r\in E\).
Since \(\gcd(r,5)=1\) and \(a^5=2\), an integer Bézout identity
would imply \(a\in E\), a contradiction. The evaluation table above
therefore has rank five over \(E\), and the same five \(r_i\) form
the entire \(E\)-space of quadratics vanishing at \(p\). The
coefficient obstruction applies unchanged, since squares of real
coefficients are nonnegative.

Conversely, suppose \(a\in E\). The positive definite rational
Hessian Gram matrix supplies a rational SOS of the Hessian biform by
rational elimination and four-square decompositions of its positive
rational pivots. Each squared expression, after substitution
\(X=p+tu\) and direction \(u\), is of the form
\(\ell(u)+tq(u)\), where \(\ell,q\in E[u]\). Its Taylor
integral has the explicit SOS identity

\[
 \int_0^1(1-t)(\ell+tq)^2\,dt
 =\frac12\left(\ell+\frac q3\right)^2
   +\left(\frac q6\right)^2.
\]

The coefficient \(1/2=(1/2)^2+(1/2)^2\) is a sum of rational
squares. Summing these identities, and translating back by \(p\in E^3\),
gives an SOS in \(E[x,y,z]\). This avoids assuming that every
positive element of \(E\) is a square or a sum of squares.

Thus \(\mathbb Q(a)\) is the smallest real coefficient field for a
polynomial SOS representation. Every finite such field has degree
divisible by five. The real-field assumption matters in the necessity
proof, both for the factor's constant term and for evaluating a sum of
squares at \(p\).

## Checks actually performed

An independent inline `python - <<'PY'` calculation with SymPy checked
the quadratic evaluations modulo \(T^5-2\), evaluation rank five,
product rank fifteen and the displayed determinant, and the rank twenty
of the first-jet evaluation map on the thirty-five quartic monomials.
It recovered and then directly verified the functional \(L\) on all
fifteen products. These are exact rational calculations. The field,
convexity, and rational-descent conclusions use the proofs above.
A second independent inline `python - <<'PY'` calculation rebuilt the
explicit Hessian Gram matrix from shifted coefficients, checked its exact
polynomial identity, computed the twelve principal minors above, and
rechecked algebraic vanishing and the coefficient obstruction. It passed.
A later targeted inline command executed the author's checker through
`runpy.run_path`, matched every listed principal minor of \(2(M-I)\),
and checked that the canonical Gram of the explicit baseline
\(G=A^2+\sum_{i=0}^3r_i^2\) is also positive definite. This last
check supports the main note's description of the negative-square
perturbation; the final polynomial's certificate was already verified
independently. A further exact symbolic check verified the Taylor integral
identity in the coefficient-field proof. Targeted Markdown checks passed.
No project-wide verification, CI inspection, or Lean check was run.
