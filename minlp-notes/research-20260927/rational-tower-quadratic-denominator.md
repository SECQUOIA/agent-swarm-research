# Short rational-function certificates for the exponential SOS-field tower

Date: 2026-09-28. Status: the complete constructive proof passed
[fresh adversarial review](rational-tower-quadratic-denominator-review.md)
and was independently reconstructed by the root. Publication priority
remains unestablished.

The [quintic-tower construction](exponential-least-sos-field.md) can be
scaled so that it has a polynomial-size rational-function SOS
certificate with an everywhere-positive quadratic common denominator.
At the same time, every polynomial SOS or PSD polynomial Gram
certificate over algebraic coefficients has an individual coefficient
of degree at least \(5^k\). The polynomial has \(3k\) variables,
degree four, rational coefficients of polynomial bit length, and a
polynomial-size rational positive definite Hessian Gram certificate.

The denominator is the fixed radial polynomial
\[
                         h(X)=1+\|X\|^2.
\]
Its degree two is the minimum possible common-denominator degree.
Both the multiplier certificate \(hF\in\Sigma\mathbb Q[X]^2\)
and a rational-function SOS for \(F\) can be constructed in
deterministic time polynomial in \(k\).

The construction below enlarges the scaling factor in the earlier
tower theorem. It does not assert that the earlier scaling prescription
already satisfies this additional certificate bound.

## A general multiplier lemma

The mechanism does not require convexity of the baseline.

**Lemma.** Let \(n,m\ge1\), let
\(q_1,\ldots,q_m\in\mathbb Q[X_1,\ldots,X_n]\)
have degree at most two, and let \(F_0=\sum_iq_i^2\). Suppose:

1. The rational span of the \(q_i\) contains a supplied quadratic
   \(G=X^{\mathsf T}HX+\ell^{\mathsf T}X+c\) with \(H\succ0\).
2. A homogeneous rational quadratic \(R\) belongs to the rational
   span of \(q_i\) and \(X_jq_i\).

Then \(h=1+\|X\|^2\) satisfies
\[
                 h(\lambda F_0-R^2)\in\Sigma\mathbb Q[X]^2
\]
for every sufficiently large rational \(\lambda>0\). A valid
integer threshold and a rational SOS certificate can be constructed
in deterministic polynomial time, with polynomial bit length in the
explicit rational input. The square factors have degree at most three.

The proof is exactly (5)--(14), with \(w=(X_jq_i)\) of length
\(m(n+1)\). Write \(R=a^{\mathsf T}w\), and let the columns
of \(U\) express \(X_jG\) in \(w\). The zero identity (8) and
the positivity estimates use no other property of the baseline.
The first, Hessian-related threshold in (12) is omitted for this
lemma. If the required span coordinates are not supplied, rational
linear algebra finds them in polynomial time and with polynomial
bit length. The unweighted rational-square conversion is given in
Section 4.

The tower has the needed quadratic \(G\) as a positive rational
multiple of \(q_0\), and (4) supplies the second span condition
explicitly. Its convexity is used for the additional optimization
and coefficient-field conclusions, not for this multiplier lemma.

## 1. The baseline and the relation to be subtracted

Use \(n=3k\), the root-tower point
\[
 p=(a_i,a_i^2,a_i^3)_{i=1}^k,\qquad a_i=2^{1/5^i},
\]
and the rational baseline from the tower theorem:
\[
 F_0=\sum_{i=0}^n q_i^2,\qquad
 q_0=\frac{G}{\tau\nu},\qquad
 q_i=\frac{r_i}{\nu}\quad(1\le i\le n).
                                                        \tag{1}
\]
Here \(\tau,\nu>0\) are rational, the \(r_i\) are the three
residuals per gate, and
\[
 G(X)=X^{\mathsf T}HX+\ell^{\mathsf T}X+c,\qquad H\succ0
                                                        \tag{2}
\]
is rational. The baseline's full rational Hessian Gram is \(M\succ0\).
All these objects are constructed in polynomial time with polynomial
bit length by the reviewed signed-root theorem.

Write \((x,y,z)=(x_k,y_k,z_k)\) for the last gate. Its first two
residuals are
\[
 r_{k,1}=x^2-y,\qquad r_{k,2}=xy-z.
\]
Set
\[
 R=y^2-xz=X^{\mathsf T}TX.
                                                        \tag{3}
\]
The identity
\[
                         R=xr_{k,2}-yr_{k,1}             \tag{4}
\]
will put \(R\) into the span of cubic factors already present in
\(hF_0\). The matrix \(T\) is rational and supported in the last
three coordinates. As in the tower theorem, its canonical Hessian
Gram for \(R^2\) has norm at most sixteen.

## 2. An exact zero identity enlarges the positive Gram space

Set \(X_0=1\). Let \(w\) be the full list
\[
                    w=(X_jq_i)_{\substack{0\le j\le n\\0\le i\le n}},
 \qquad d=(n+1)^2.
                                                        \tag{5}
\]
No linear-independence assumption on this list is needed. It gives
the identity
\[
                             hF_0=w^{\mathsf T}w.
                                                        \tag{6}
\]
By (4), there is an explicit rational \(a\in\mathbb Q^d\)
with
\[
 R=a^{\mathsf T}w.
\]
It has exactly two nonzero entries, \(\nu\) at
\(xq_{k,2}\) and \(-\nu\) at \(yq_{k,1}\).

Let \(U\in\mathbb Q^{d\times n}\) have its \(j\)-th column
represent \(X_jG\) in the list \(w\). Explicitly, that column
has entry \(\tau\nu\) at \(X_jq_0\) and is zero elsewhere.
Put
\[
 b=(X_1R,\ldots,X_nR)^{\mathsf T},\qquad
 C=\frac{a\ell^{\mathsf T}-UT}{2}.
                                                        \tag{7}
\]
The polynomial vector \(b\) has degree at most three. The key exact
identity is
\[
 \boxed{
 \begin{pmatrix}w\\b\end{pmatrix}^{\mathsf T}
 \begin{pmatrix}caa^{\mathsf T}&C\\C^{\mathsf T}&H\end{pmatrix}
 \begin{pmatrix}w\\b\end{pmatrix}=0.}
                                                        \tag{8}
\]
Indeed,
\[
 \sum_{j,l}T_{jl}(X_jG)(X_lR)
      =GR\sum_{j,l}T_{jl}X_jX_l=GR^2,
\]
while
\[
 b^{\mathsf T}Hb+R\ell^{\mathsf T}b+cR^2
       =R^2(X^{\mathsf T}HX+\ell^{\mathsf T}X+c)=GR^2.
\]
Subtracting these two equal expressions gives (8), including the
factor one half in its cross block.

For any positive rational \(\varepsilon\), equations (6)--(8)
therefore give a Gram representation of the same polynomial:
\[
 hF_0=
 \begin{pmatrix}w\\b\end{pmatrix}^{\mathsf T}
 Q_\varepsilon
 \begin{pmatrix}w\\b\end{pmatrix},\qquad
 Q_\varepsilon=
 \begin{pmatrix}
 I_d+\varepsilon caa^{\mathsf T}&\varepsilon C\\
 \varepsilon C^{\mathsf T}&\varepsilon H
 \end{pmatrix}.
                                                        \tag{9}
\]
The new lower block will be strictly positive. The old identity block
allows its cross terms to be absorbed by a Schur complement.

## 3. Explicit rational positivity and scaling bounds

Let
\[
 \eta=\frac{\det H}{(\operatorname{tr}H)^{n-1}}>0.
\]
As usual, \(\lambda_{\min}(H)\ge\eta\). Choose the rational
number
\[
 \varepsilon=\min\left\{
 1,\
 \frac{1}{2(1+|c|\|a\|^2)},\
 \frac{\eta}{4(1+\|C\|_F^2)}
 \right\}>0.
                                                        \tag{10}
\]
The top block \(A_\varepsilon=I_d+\varepsilon caa^{\mathsf T}\)
is at least \(I_d/2\), even when \(c<0\).
Consequently its inverse has norm at most two. The Schur complement
of \(A_\varepsilon\) in \(Q_\varepsilon\) is bounded below by
\[
\begin{aligned}
 \varepsilon H-\varepsilon^2C^{\mathsf T}
                  A_\varepsilon^{-1}C
 &\succeq
   \bigl(\varepsilon\eta-2\varepsilon^2\|C\|_F^2\bigr)I_n\\
 &\succeq \frac{\varepsilon\eta}{2}I_n.
\end{aligned}
\]
Thus \(Q_\varepsilon\succ0\). This statement concerns its
ordinary coefficient matrix. Redundancy in the polynomial list
\((w,b)\) does not obstruct a positive definite matrix representation
or the resulting polynomial SOS identity.

Put \(s=d+n\), and define
\[
 \delta=\frac{\det Q_\varepsilon}
                    {(\operatorname{tr}Q_\varepsilon)^{s-1}}>0,
 \qquad
 \mu=\frac{\det M}{(\operatorname{tr}M)^{n+n^2-1}}>0.
                                                        \tag{11}
\]
These bound the respective smallest eigenvalues from below.
Choose the integer
\[
 \widehat\lambda=
 \left\lceil
 \max\left\{\frac{17}{\mu},\
             \frac{2+\|a\|^2}{\delta}\right\}
 \right\rceil,\qquad
 F=\widehat\lambda F_0-R^2.
                                                        \tag{12}
\]
The original tower proof gives a rational full Hessian Gram at least
the identity, since the first threshold in (12) absorbs the Hessian
Gram of \(R^2\).

On the polynomial vector \((w,b)\), the polynomial \(hR^2\)
has the positive semidefinite Gram
\[
                   D_R=\operatorname{diag}(aa^{\mathsf T},I_n).
\]
Its norm is at most \(1+\|a\|^2\). The second threshold in
(12) therefore gives
\[
                 \widehat\lambda Q_\varepsilon-D_R\succeq I_s.
                                                        \tag{13}
\]
Together with (9), this is the promised explicit rational positive
definite Gram certificate:
\[
 \boxed{
 hF=
 \begin{pmatrix}w\\b\end{pmatrix}^{\mathsf T}
 (\widehat\lambda Q_\varepsilon-D_R)
 \begin{pmatrix}w\\b\end{pmatrix}.}
                                                        \tag{14}
\]

## 4. Polynomial construction and certificate size

All dimensions in (5)--(14) are \(O(n^2)\). All entries are rational
expressions obtained from the polynomial-size baseline by polynomially
many rational operations, powers with polynomial exponents, and
determinants of polynomial-dimensional matrices. Determinant bounds,
or exact elimination with standard bit bounds, show that numerators
and denominators have polynomial bit length. The minima in (10) and
the ceiling in (12) are exact rational comparisons. Consequently the
new scaling, the quartic, and the Gram certificate (14) are all
constructed in deterministic time polynomial in \(k\).

An unweighted rational SOS can also be constructed in polynomial time.
Rational LDL factorization of the positive definite matrix in (13)
gives positive rational weights with polynomial bit length and rational
polynomial factors of degree at most three. There is no need to assume
a polynomial-time algorithm for the integer four-square problem.
For a positive weight \(u/v\), with \(u,v\) positive integers,
write
\[
 \frac uv=\frac{uv}{v^2}.
\]
Expand the positive integer \(uv\) in binary. A term \(2^{2j}\)
is \((2^j)^2\), and a term \(2^{2j+1}\) is the sum of two
copies of that square. Dividing each resulting integer square by
\(v^2\) expresses \(u/v\) as \(O(\operatorname{bits}(uv))\)
rational squares. This expansion is deterministic and has polynomial
size. Absorbing these scalar squares gives
\[
                         hF=\sum_{\ell=1}^L f_\ell^2,
 \qquad f_\ell\in\mathbb Q[X],\quad\deg f_\ell\le3,
                                                        \tag{15}
\]
where \(L\), the dense factor lengths, and their coefficient bit
lengths are polynomial in \(k\).

Multiply (15) by \(h=1+\sum_jX_j^2\):
\[
 F=\sum_\ell(f_\ell/h)^2+
                \sum_{j,\ell}(X_jf_\ell/h)^2.
                                                        \tag{16}
\]
All numerators have degree at most four. The common polynomial
denominator has degree two and is at least one everywhere. The number
and total binary length of the rational-function factors remain
polynomial in \(k\).

## 5. The polynomial-certificate field obstruction remains intact

The tower's coefficient-field proof holds for every positive rational
scaling satisfying the original Hessian-Gram threshold. Necessity uses
a restricted Gram with the same negative direction, independently of
the positive scaling. Sufficiency uses the rational SOS Hessian
certificate, rather than strong convexity alone. Thus changing \(\lambda\) to
\(\widehat\lambda\) in (12) preserves all of the following:

- \(\nabla^2F\succeq I\), with an explicit rational positive
  definite full Hessian Gram of polynomial size;
- the unique zero and minimum at \(p\), with minimum value zero;
- polynomial SOS and PSD polynomial Gram certificates over a real
  field \(E\) exist exactly when \(2^{1/5^k}\in E\);
- by the [individual-coefficient lemma](exponential-sos-individual-coefficient-degree.md),
  every such certificate with algebraic coefficients has an individual
  coefficient of algebraic degree at least \(5^k\).

In particular, \(F\) is not rational polynomial SOS. The
[affine-denominator cancellation lemma](rational-denominator-certificate-frontier.md)
therefore excludes any rational-function SOS with a common polynomial
denominator of degree zero or one. Combined with (16), the minimum
possible common-denominator degree is exactly two. This does not
minimize the number of rational-function squares.

## 6. What the construction adds and what remains open

The general existence of rational-function SOS certificates is
classical, and the earlier
[regular-denominator deduction](rational-denominator-certificate-frontier.md)
already guarantees a denominator without real poles for these
quartics. The addition here is the explicit degree-two denominator,
a polynomial-time rational construction of its full certificate,
and its coexistence with the exponential individual coefficient-degree
requirement for polynomial SOS certificates.

Variable rational-function denominators are an established exact
certification strategy; see
[Kaltofen, Li, Yang, and Zhi](https://www.sciencedirect.com/science/article/pii/S0747717111001143).
The zero Gram identity and Schur-complement perturbation use elementary
linear algebra. No novelty is claimed for either technique in isolation.
Priority for this specific combined family remains unestablished.

The result distinguishes two exact certificate representations for the
same optimization problem. It does not prove that every algebraic
polynomial certificate has a long radical or circuit description.
It does not prove a numerical speedup, a decision-complexity lower
bound, or a uniform quadratic-denominator theorem for arbitrary rational
strongly SOS-convex quartics. The positive quadratic part of \(G\)
and the explicit relation (4) are substantive construction inputs.

No conflict arises with the
[unbounded fixed-radial-order family](rational-radial-exponent-obstruction.md).
That theorem scales one fixed polynomial. Here the signed-square
polynomial itself is selected using the additional multiplier threshold
in (12).

The proof establishes all identities and bounds for every \(k\).
The fresh review checked the zero identity, Schur constants,
determinant bit bounds, certificate conversion, general lemma, and
preservation of the field obstruction. It requested one scope
correction, now independently rechecked and incorporated: field
sufficiency uses the rational SOS Hessian certificate, not strong
convexity alone.

The reviewer ran the separate
[exact checker](check_tower_quadratic_denominator_review.py) with
a nonzero linear part and negative constant in \(G\):

~~~text
python research-20260927/check_tower_quadratic_denominator_review.py
~~~

It passed the exact span, zero-Gram, multiplier, and positive-matrix
identities. This check stresses the signs and indexing; it does not
establish the universal theorem. The author read that checker and
review without duplicating its executable calculation. No project-wide
verification, CI inspection, or Lean formalization was performed.

A targeted inline Python document check passed this note, its fresh
review, the radial-exponent note, and the tower's fresh review. It
checked nineteen local file links, balanced math delimiters, final
newlines, whitespace, and control characters. These document checks
are separate from the mathematical verification above.
