# Fresh source and proof review of the singly exponential interior Gram bound

Date: 2026-09-28. Status: the complete statement passed independent
source and construction review. No mathematical correction was required
in the frozen note.

I checked the exact primary theorem, the rational-center reduction,
the explicit Gram formula, positive definiteness, and total certificate
length in
[the upper-bound note](interior-gram-single-exponential-upper.md).
The argument proves the stated size bound with the supplied positive
definite full Hessian Gram. It does not establish that bound for general
SOS-interior polynomials.

## Primary source and its exact scope

I read Theorem 4.1.2 and its proof directly in Basu, Pollack, and Roy,
*On the Combinatorial and Algebraic Complexity of Quantifier
Elimination*, Journal of the ACM 43(6), 1996, printed pages 1031--1032.
The repository's
[primary PDF](../literature/papers/basu1996-on-the-combinatorial-and-algebraic/original.pdf#page=30)
contains these on PDF pages 30--31. I inspected both extracted text
and rendered page images to check the strict inequality and the exponent.

The theorem concerns a nonempty set defined by strict inequalities
\(P(X)>0\), for integer polynomials in \(n\) variables of degree
at most \(d\), with integer coefficient bit length at most \(\tau\).
It gives a rational point in each semialgebraically connected component,
whose coordinate numerators and denominators have bit length
\(\tau d^{O(n)}\). Thus it is the required rational-point result,
not merely an algebraic sampling result or a bound on coordinate
magnitude. The proof explains rational approximation of its univariate
representations while preserving the strict signs.

The application has one strict inequality, degree at most six, and
integer coefficient bound \(\tau=\operatorname{poly}(L)\).
Its hypotheses therefore match exactly. No equality constraint,
convexity of the open set, or rationality of the minimizer is needed.
The existence theorem alone suffices for the stated certificate-size
conclusion; the note makes no polynomial-time claim in \(L\) alone.

The targeted source-reading commands were:

~~~text
pdftotext -f 30 -l 31 -layout literature/papers/basu1996-on-the-combinatorial-and-algebraic/original.pdf -
pdftoppm -f 30 -l 31 -scale-to 1600 -png literature/papers/basu1996-on-the-combinatorial-and-algebraic/original.pdf /tmp/interior_bpr_review
~~~

## The rational center condition

The determinant-to-trace quantity
\(\mu=\det A/(\operatorname{tr}A)^{h-1}\) is positive and
satisfies \(A\succeq\mu I\). Since the full Hessian vector
contains its constant block, this implies
\(\nabla^2f(X)\succeq\mu I\). Hence \(f\) is coercive,
has a unique minimizer \(p\), and has positive attained minimum.

The polynomial
\[
 c(X)=f(X)-\frac{\|\nabla f(X)\|^2}{2\mu}
\]
has degree at most six and is positive at \(p\). Its positive set
is therefore nonempty and open. The gradient-square term introduces
only polynomially many coefficients because its degree is fixed.
Determinant bounds, the trace power with polynomial exponent, and
positive common-denominator clearing give integer coefficients of
bit length polynomial in the expanded input length \(L\).

The primary theorem consequently gives a rational \(q\) with
\(c(q)>0\) and coordinate bit bound
\(\operatorname{poly}(L)6^{O(n)}\). The subsequent proof needs
only this inequality. It does not assume an additional, unquantified
distance bound between \(q\) and the minimizer.

## The explicit positive definite Gram

With \(d=X-q\) and \(g=\nabla f(q)\), the matrix
\[
 \bar A=A-\mu\operatorname{diag}(I_n,0)
 \succeq\mu\operatorname{diag}(0,I_{n^2})
\]
is rational and PSD. The Taylor vector is exactly
\[
 (d,(q+td)\otimes d)=(d,q\otimes d)+t(0,d\otimes d).
\]
Thus its dependence on \(t\) is affine. Integrating against
\(1-t\) gives coefficients \(1/2\), \(1/6\), and \(1/12\)
for the constant, cross, and quadratic terms. Completing that quadratic
expression yields the \(1/2\) and \(1/36\) terms in (12).
All factors and signs in (11)--(13) are correct.

The remaining affine completion is
\[
 f(q)+g^{\mathsf T}d+\frac\mu2\|d\|^2
 =\frac\mu2\|d+g/\mu\|^2+c(q).
\]
It accounts for the exact same center condition used by the sampling
step. Therefore equation (13) represents \(f\) without an
approximation or coefficient projection.

Every term in that matrix is PSD. Its second term dominates the
coefficient Gram of
\(\mu\sum_{i,j}(d_id_j)^2/36\). These quadratic factors, the
completed affine factors, and the positive constant span the entire
degree-at-most-two polynomial space. Their Gram is positive definite.
Equivalently, any coefficient vector in the kernel would annihilate
the constant, every affine polynomial, and every quadratic monomial
in \(d\), and hence would be zero. Rational translation between
the \(d\) and \(X\) bases is invertible.

This proves positive definiteness of the displayed ordinary Gram,
not only existence of some SOS representation.

## Bit growth and unweighted squares

Let \(B\) bound the numerator and denominator lengths of the
coordinates of \(q\). The bit argument is not based solely on
counting arithmetic operations. Evaluation has fixed degree, and the
explicit matrix formulas have bounded algebraic depth and polynomial
dimensions. In particular, \(f(q)\) has degree four in the center,
\(g\) has degree three, and \(c(q)\) has degree at most six.
The coefficient matrices of \(U\) and \(V\) involve only products
of at most two center coordinates. The completed affine terms involve
\(g/\mu\), with \(\mu\) already of polynomial input bit length.

Thus the displayed Gram entries are fixed-degree expressions in
\(q\), with rational coefficients controlled by the input, and
polynomially many terms. Rational evaluation and summation give
\(\operatorname{poly}(L,n,B)\) bit length for the total matrix.
Cancellation can reduce a numerator but cannot defeat this upper
bound. No lower numerical bound on \(c(q)\) is required.

Substitution of \(B=\operatorname{poly}(L)6^{O(n)}\) gives
\(\operatorname{poly}(L)2^{O(n)}\). A fixed polynomial in a
singly exponential bit bound is still singly exponential; it is not
an iteration of exponentials.

Exact rational LDL factorization of this positive definite matrix
has polynomial bit complexity in its dimension and entry length.
It produces positive rational weights and rational linear forms in
\(z\), which are quadratic polynomial factors in \(X\).
The binary expansion of a positive weight \(a/b\), using
\(a/b=ab/b^2\), gives polynomially many rational squares in the
weight's bit length. Counting all factors and all their coefficients
still gives a polynomial in the Gram encoding length, and therefore
the same singly exponential form of bound. No integer factorization
or efficient four-square algorithm is assumed.

## Comparison and verification limits

The separately reviewed lower family has polynomial-size input and
requires \(\Omega(n2^{n/2})\) denominator bits in every positive
definite rational ordinary Gram. It satisfies the supplied-Hessian
hypothesis here. Together the two results show that exponential
dependence on dimension is qualitatively necessary and sufficient in
this class. They do not match exponent constants or polynomial factors.
The lower family retains its short singular PSD and SOS certificates.

No new numerical experiment was needed for this review. The source
was checked directly, and the matrix identities and size estimates
were checked algebraically. A targeted inline Python document check
passed the review's local links, math delimiters, whitespace, control
characters, and final newline; the frozen theorem-note hash was
unchanged. No project-wide verification, CI inspection, or Lean
formalization was performed. Publication priority remains unestablished.
