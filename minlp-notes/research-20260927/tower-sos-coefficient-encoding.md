# Dense algebraic output versus a shared root circuit

Date: 2026-09-28. Status: companion consequence passed
[fresh independent review](tower-auxiliary-and-encoding-review.md).
This is an encoding clarification for the
[quintic-tower theorem](exponential-least-sos-field.md), not a claim of
hardness for every exact representation.

The theorem's quartics have a constructive separation between two
representations of polynomial SOS certificates. Dense defining
polynomials for individual algebraic coefficients require exponential
length. A shared root circuit for the coefficients has polynomial
length and can be constructed in polynomial time.

## The two bounds

Let \(F_k\) be the rational quartic in \(N=3k\) variables.
Its rational positive definite Hessian Gram is part of the constructed
data. Then:

1. Every polynomial SOS certificate with algebraic coefficients has
   at least one coefficient of degree at least \(5^k\). Any dense
   rational annihilating-polynomial list for that coefficient has at
   least \(5^k+1\) positions.
2. A polynomial SOS certificate can be constructed with polynomially
   many square factors, each quadratic in the original variables, whose
   coefficients are represented by a shared arithmetic circuit of
   polynomial size. Its only nonrational operations are the \(k\)
   positive fifth-root gates
   \[
      a_1=\sqrt[5]{2},\qquad a_i=\sqrt[5]{a_{i-1}}.
   \]
   All other gates use rational constants and addition, subtraction,
   and multiplication.

The first assertion is the
[reviewed individual-coefficient degree consequence](exponential-sos-individual-coefficient-degree.md).
Here is an explicit construction for the second.

## Constructing the square factors

Factor the rational positive definite Hessian Gram by rational LDL.
Every resulting positive rational weight \(a/b\) can be written
as a sum of rational squares in deterministic polynomial time: expand
\(ab\) in binary, replace each term \(2^{2j+1}\) by two
copies of \((2^j)^2\), and divide each square base by \(b\).
The number and bit lengths of the terms are polynomial in the weight's
bit length. Thus the Hessian biform has a rational SOS representation
\[
             v^{\mathsf T}\nabla^2F_k(Z)v=\sum_j L_j(Z,v)^2,
\]
of polynomial total size. Each \(L_j\) is linear in \(v\)
and affine in \(Z\).

Let \(p=(a_i,a_i^2,a_i^3)_i\) and \(u=X-p\).
Substitution along \(Z=p+\tau u\), \(v=u\), gives
\[
 L_j(p+\tau u,u)=U_j(X,p)+\tau V_j(X,p).
\]
Both \(U_j\) and \(V_j\) have total degree at most two
in \((X,p)\), and their rational coefficients have polynomial bit
length. At the zero \(p\), the value and gradient of \(F_k\)
vanish. Taylor integration therefore gives
\[
 F_k(X)=\sum_j\left[
       2\left(\frac{U_j+V_j/3}{2}\right)^2
                      +\left(\frac{V_j}{6}\right)^2\right].
\]
Interpreting the factor two as two identical squares gives actual square
factors with no extra root gates. Their coefficients are rational
polynomials of degree at most two in the coordinates of \(p\).

The \(k\) root gates produce all \(a_i\), after which two
multiplications per gate produce \(a_i^2,a_i^3\). Each required
coefficient is then evaluated by a polynomial-size arithmetic circuit
on these shared outputs. Rational matrix factorization, binary square
splitting, and these coefficient operations all have polynomial cost in
the tower construction's output size, which is polynomial in \(k\).
No degree-\(5^k\) minimal polynomial is expanded.

## What the comparison establishes

The lower and upper bounds concern the same quartics and exact
polynomial SOS certificates. Thus the coefficient-field obstruction is
a substantial restriction on dense algebraic output, while this family
admits compact shared root descriptions. The statement does not give
an efficient method for checking arbitrary SOS identities whose
coefficients are supplied as arbitrary root circuits. These particular
identities can instead be justified by their rational Hessian Gram,
the root relations, and the displayed Taylor formula; the
[auxiliary-variable certificate](tower-rational-auxiliary-certificate.md)
makes that rational proof explicit.

The upper bound is an elementary consequence of Taylor SOS and the
compact root data already retained by the construction. It is recorded
to state the representation boundary accurately, not as an additional
novelty claim. The exponential lower bound is in \(k\) or \(N\),
and gives a superpolynomial bound relative to the constructed dense
input size; it is not asserted to be exponential in that entire bit
length.
