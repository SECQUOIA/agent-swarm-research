# One exact SOS coefficient must have exponentially large algebraic degree

Date: 2026-09-28. Status: root-contributed strengthening of the
[quintic-tower theorem](exponential-least-sos-field.md), independently
reconstructed by its author and checked by the theorem's fresh reviewer.
The argument uses standard Galois theory; no novelty claim is made for
the abstract field lemma.

The tower theorem forces every real coefficient field of a polynomial
SOS or positive semidefinite polynomial Gram certificate to contain
\(2^{1/5^k}\). This note strengthens that joint-field statement:
if the certificate has algebraic coefficients, at least one coefficient
already has degree at least \(5^k\). Splitting the coefficient field
among many separately represented algebraic numbers cannot avoid the
degree bound.

## A field-generation lemma

**Lemma.** Let \(D=5^k\), where \(k\geq1\), and let
\(\beta_1,\ldots,\beta_s\) be a finite list of algebraic numbers.
If
\[
 2^{1/D}\in\mathbb Q(\beta_1,\ldots,\beta_s),
\]
then
\[
 \max_i[\mathbb Q(\beta_i):\mathbb Q]\geq D.
\]
The numbers in this abstract lemma need not be real.

**Proof.** Write \(a=2^{1/D}\), let \(\zeta\) be a primitive
\(D\)-th root of unity, and put
\[
 Z=\mathbb Q(\zeta),\qquad Z^+=\mathbb Q(\zeta+\zeta^{-1}).
\]
Every conjugate of \(\zeta+\zeta^{-1}\) is a sum of a root
of unity and its inverse and is real. Thus \(Z^+\) is totally
real. The element \(\zeta\) satisfies a quadratic over
\(Z^+\), and it is not real, so \([Z:Z^+]=2\).

The real-field lemma in the tower theorem, applied to \(Z^+\),
says that the minimal polynomial of \(a\) over \(Z^+\) is
\(T^r-a^r\), with \(r\mid D\) and \(a^r\in Z^+\).
If \(r<D\), then \(a^r=2^{1/(D/r)}\) has rational minimal
polynomial
\[
 T^{D/r}-2.
\]
This is irreducible by Eisenstein at two and has nonreal conjugates,
since \(D/r\) is odd and greater than one. It cannot be an
element of a totally real field. Hence \(r=D\).

The field \(Z^+(a)\) is real. Adjoining the nonreal element
\(\zeta\) to it gives degree two, because \(\zeta\) still
satisfies the same quadratic. The tower identity therefore gives
\[
 [Z(a):Z]
 =\frac{[Z(a):Z^+(a)]\,[Z^+(a):Z^+]}{[Z:Z^+]}
 =D.
\]
Consequently the splitting field \(S=Z(a)\) of \(T^D-2\)
has an automorphism \(\sigma\) fixing \(Z\) and sending
\(a\) to \(\zeta a\). Its order is exactly \(D\).

Let \(d_i=[\mathbb Q(\beta_i):\mathbb Q]\), let \(K_i\)
be the normal closure of \(\mathbb Q(\beta_i)\), and let
\(K\) be the compositum of the finitely many \(K_i\). The
restriction actions on the minimal polynomials' roots give faithful
embeddings
\[
 \operatorname{Gal}(K/\mathbb Q)
 \hookrightarrow \prod_i\operatorname{Gal}(K_i/\mathbb Q)
 \hookrightarrow \prod_i\mathfrak S_{d_i}.
\]
The first map is injective because the \(K_i\) generate \(K\).

Suppose every \(d_i<D\). The order of a permutation is the least
common multiple of its cycle lengths. Its largest power-of-five divisor
is at most \(5^{k-1}\) when all cycles have length below
\(5^k\). The same bound holds for the order of every element of
the displayed product, regardless of the number of factors.

The hypothesis gives \(a\in K\). Normality of \(K/\mathbb Q\)
then gives \(S\subseteq K\). Restriction onto
\(\operatorname{Gal}(S/\mathbb Q)\) is surjective, so
\(\sigma\) has a lift to \(\operatorname{Gal}(K/\mathbb Q)\).
The order of that lift is divisible by the order \(5^k\) of
\(\sigma\), a contradiction. This proves the lemma. \(\square\)

The same proof works with five replaced by any odd prime. Only the
quintic case is needed for the quartic construction.

## Consequence for exact convex optimization certificates

Let \(F_k\) be the rational strongly SOS-convex quartic from the
tower theorem, in \(N=3k\) variables. List all coefficients of
any polynomial SOS certificate for \(F_k\), or all entries of
any positive semidefinite polynomial Gram certificate on the full
monomial basis of degree at most two. If these numbers are algebraic,
their generated real field contains \(a=2^{1/5^k}\), by that
theorem. The lemma proves that at least one individual entry has degree
at least
\[
                         5^k=5^{N/3}.
\]
Thus an output format that lists a dense rational minimal polynomial
for each coefficient must use at least \(5^k+1\) coefficient
positions for one entry alone. This conclusion holds even if different
entries use different defining fields. A dense list of any annihilating
polynomial is no shorter, since its degree is at least the minimal
polynomial degree.

The input quartic and its rational positive definite Hessian Gram have
polynomial size in \(k\). The resulting dense-output lower bound is
superpolynomial relative to that input size. It is exponential in the
number of variables, not asserted to be exponential in the full dense
input bit length.

## Verification and limits

The parent proposed the individual-degree strengthening and the
totally-real cyclotomic proof above. The tower author independently
reconstructed both. The
[fresh adversarial review](exponential-least-sos-field-fresh-review.md#supplement-one-algebraic-coefficient-must-already-have-large-degree)
checks the permutation-group argument and also records a separate check
of the order-\(5^k\) automorphism using Eisenstein at a prime above
two in the cyclotomic field. These are mathematical checks; no finite
computation establishes the all-\(k\) assertion.

This is a statement about finite lists of algebraic coefficients and a
specified dense representation. It gives no output lower bound for
transcendental descriptions, sparse polynomials, radicals, root towers,
or arithmetic circuits. In particular, \(T^{5^k}-2\) has only
two nonzero terms, and the tower itself has a short root-circuit
description. It also gives no decision-complexity or approximate
optimization lower bound. Rational-function SOS certificates with no
real poles remain available over \(\mathbb Q\), as explained in
the main theorem.
