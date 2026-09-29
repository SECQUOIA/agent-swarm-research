# Short rational certificates after retaining the root variables

Date: 2026-09-28. Status: companion consequence passed
[fresh independent review](tower-auxiliary-and-encoding-review.md).
The Taylor SOS principle used here is established prior
theory; this note makes its size and degree consequences explicit for
the [quintic-tower family](exponential-least-sos-field.md).

That family requires an individual coefficient of algebraic degree at
least \(5^k\) in every algebraic polynomial SOS certificate. Yet its
nonnegativity has a polynomial-size rational SOS certificate modulo
quadratic equations in \(3k\) auxiliary variables. The auxiliary
equations have a real solution by the elementary odd-root recursion.
This is a separation between specified certificate representations,
not a lower bound for all exact proof systems.

## The explicit certificate

Use the notation of the tower theorem, with \(N=3k\), original
variables \(X\), and a second copy \(Y\). Write
\[
 F(X)=\sum_{j=0}^{N+1}w_jq_j(X)^2,
 \qquad q=(G,r_1,\ldots,r_N,R),
 \tag{1}
\]
where the rational weights are \(\lambda/(t\nu)^2\) on
\(G\), \(\lambda/\nu^2\) on every root residual, and
\(-1\) on \(R\). Let \(M\succ0\) be the rational
Hessian Gram for the final \(F\), on \((v,X\otimes v)\).
This is the final matrix \(\lambda M_0-B\) from the tower
construction, not its baseline Gram \(M_0\).

Set \(u=X-Y\) and define polynomial vectors
\[
 A=(u,Y\otimes u),\qquad B=(0,u\otimes u).
\]
Then the rational polynomial
\[
 s(X,Y)=\frac12(A+B/3)^{\mathsf T}M(A+B/3)
                       +\frac1{36}B^{\mathsf T}MB
 \tag{2}
\]
is SOS over \(\mathbb Q\), has degree at most four, and has
a rational PSD Gram of polynomial size. Direct Taylor integration gives
\[
 s(X,Y)=F(X)-F(Y)-\nabla F(Y)^{\mathsf T}(X-Y).
 \tag{3}
\]
Indeed the Hessian basis along \(Y+\tau u\) is
\(A+\tau B\). Integrating its Gram quadratic form against
\(1-\tau\) gives coefficients \(1/2,1/3,1/12\) on
\(A^{\mathsf T}MA,A^{\mathsf T}MB,B^{\mathsf T}MB\),
respectively, which agrees with (2).

Differentiate the signed-square expression (1), and put
\[
 H_j(X,Y)=w_j\bigl(q_j(Y)+2\nabla q_j(Y)^{\mathsf T}(X-Y)\bigr).
 \tag{4}
\]
Equations (1)--(3) now give the rational polynomial identity
\[
                  F(X)=s(X,Y)+\sum_{j=0}^{N+1}H_j(X,Y)q_j(Y).
 \tag{5}
\]
Every \(H_j\) has degree at most two. Thus (5) has certificate
degree at most four. All data, including the Gram matrix for \(s\),
are constructed in deterministic polynomial time and have polynomial
bit length. Checking the coefficient identity and rational PSD matrix
is also polynomial time in the printed certificate size.

## The auxiliary equations really have a solution

The \(N\) root residuals in gate \(i\) are
\[
 r_{i,1}=x_i^2-y_i,\quad r_{i,2}=x_iy_i-z_i,\quad
 r_{i,3}=y_iz_i-b_i,
 \quad b_1=2,\quad b_i=x_{i-1}\ (i>1).
\]
They have the unique real solution
\(p=(a_i,a_i^2,a_i^3)_i\), with
\(a_i=2^{1/5^i}\in[1,2]\). Existence and uniqueness follow
successively from the unique real fifth root of a positive number.
No expansion of its degree-\(5^k\) defining polynomial is needed.

The additional equations \(G(Y)=0\) and \(R(Y)=0\) are
redundant, with small explicit ideal-membership certificates. At one
gate, suppress its index and put
\[
 R_i=y^2-xz=-y r_1+x r_2,\qquad
 S_i=z^2-bx=-z r_2+x r_3.
 \tag{6}
\]
The exposing construction expresses \(G\) as a rational linear
combination of \(r_{i,1},r_{i,2},r_{i,3},R_i,S_i\). For degree
five these are all the moment relations needed in that construction:
among local quadratic monomials, only weights two, three, and four
give nonzero moment differences. Equation (6) therefore gives
\[
                    G=\sum_{i,j}A_{i,j}r_{i,j}
 \tag{7}
\]
with rational affine coefficients \(A_{i,j}\). The removed
relation \(R\) is \(R_k\) and has the same property. This
also verifies their redundancy without evaluating any algebraic number.

One may substitute (6)--(7) into (5) to retain only the \(N\)
root residuals. The resulting multipliers have degree at most three,
so this alternative certificate has degree at most five. Keeping the
two redundant equations gives the simpler degree-four version.

For every fixed \(X\), set \(Y=p\) in (5). The ideal terms
vanish and the SOS term is nonnegative. This proves \(F(X)\geq0\).
The existence argument is essential: an identity modulo an inconsistent
auxiliary system would not prove unrestricted nonnegativity.

## Rational size, prior theory, and scope

The vectors \(A,B\) contain only linear and quadratic polynomials
with small integer coefficients. Formula (2) is a rational matrix
congruence of two positive rational multiples of \(M\). Its
dimension and entry sizes are polynomial in the original data. Rational
LDL decomposition can also turn it into positively weighted rational
polynomial squares. Actual rational square factors of polynomial total
size can be produced deterministically: for a positive weight \(a/b\),
write the positive integer \(ab\) in binary, replace every odd
power of two by twice the preceding even power, and divide all square
bases by \(b\). This uses at most twice the bit length of \(ab\)
squares. No integer factorization or algorithm for a four-square
decomposition is required.

The central SOS fact is prior theory. Ahmadi and Parrilo,
[A Complete Characterization of the Gap between Convexity and SOS-Convexity](https://web.mit.edu/~a_a_a/Public/Publications/sos_convexity_tables.pdf),
Theorem 3.1, proves that the first-order convexity difference (3) is
SOS exactly when the Hessian is an SOS matrix. The present rational
formula is its elementary quartic Taylor construction. SOS certificates
modulo equality ideals are also a standard format; no new proof system
is proposed here.

The new tower theorem supplies the contrast: direct polynomial SOS
coefficients require exponential algebraic degree, while retaining the
small defining root system gives a polynomial-size rational certificate
of fixed degree. This observation does not establish novelty for an
auxiliary-variable separation in general. For this family, rational
functions and other compact exact certificates can also avoid the
coefficient-field obstruction. The result supplies no hardness claim
for deciding nonnegativity or computing an approximation.

The focused checker is

```text
python research-20260927/check_tower_auxiliary_certificate.py
```

It checks the local ideal identities, the coupled two-gate derivative
and Taylor identities, the degree bounds, and the binary rational-square
conversion. The all-\(k\) size and existence arguments require the
proof above. No project-wide checks or CI inspection are used.
