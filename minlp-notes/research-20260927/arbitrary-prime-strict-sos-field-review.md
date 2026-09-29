# Independent review of the arbitrary-prime SOS field construction

Date: 2026-09-28. Status: fresh adversarial proof review complete. No
unresolved gap was found in
[the construction](arbitrary-prime-strict-sos-field.md), its universal
quantitative estimates, or the exact SOS and polynomial-Gram field
characterization. The reviewer did not develop the construction. The
retained exact checker was inspected and rerun successfully. Publication
priority is not established by this review.

The result holds as stated for every prime \(p=2s+1\ge5\), in
\(n=s+1\) variables. Its arithmetic conclusion applies to every
subfield \(E\subseteq\mathbb R\), including fields with
transcendental elements. The Hessian Gram is integer and positive definite;
the polynomial has a stationary zero at
\(b=(a^s,\ldots,a^{2s})\), with \(a=2^{1/p}\), and its
Hessian is globally at least the identity. The construction and coefficient
bounds are polynomial in \(p\), as distinguished from polynomial in
the binary length of \(p\).

The coefficient obstruction is valid. A degree-at-most-two monomial at
\(b\) has exponent zero, an exponent in \([s,2s]\), or an exponent
in \([2s,4s]\). After reduction by \(a^{2s+1}=2\), the
coefficient of \(a^{2s}\) receives contributions only from \(x_s\)
and \(x_0^2\). Products whose exponents exceed \(2s\) reduce to
exponents at most \(2s-1\). Hence a vanishing quadratic over a field
where \(T^p-2\) is irreducible satisfies
\(v_s+h_{00}=0\). Direct multiplication gives
\[
 \Lambda(q^2)=v_0^2+2d(v_s+h_{00})=v_0^2.
 \tag{1}
\]
Every baseline factor has \(v_0=0\). The omitted factor
\(r=x_1x_s-2x_0\) vanishes at \(b\) and has \(v_0=-2\),
so subtracting \(r^2\) makes \(\Lambda(F)=-4\) exactly.
This argument does not require a basis of the entire vanishing space.

Irreducibility over arbitrary real \(E\) also holds. A proper monic
factor of \(T^p-2\), of degree \(1\le j<p\), has constant
coefficient \((-1)^j a^j\zeta_p^k\). Its reality forces
\(\zeta_p^k=1\), since an odd-order root of unity can be real only
when it is one. Thus \(a^j\in E\). Primality gives integers
\(u,v\) with \(uj+vp=1\), and then
\(a=(a^j)^u2^v\in E\). Therefore absence of \(a\) implies
irreducibility. No normality assumption on \(E\), or assumption that
it is algebraic over \(\mathbb Q\), is needed.

For SOS necessity, highest-degree real squares cannot cancel, and evaluation
at the zero forces every quadratic square factor to vanish there. Equation
(1) contradicts \(\Lambda(F)=-4\). Gram necessity is correctly
proved separately: positivity and \(F(b)=0\) imply \(Qm(b)=0\).
The constant-index row of \(Q\) is a vanishing quadratic, so
\[
 Q_{1,x_s}+Q_{1,x_0^2}=0,
 \qquad
 \Lambda(F)=Q_{x_0,x_0}\ge0.
 \tag{2}
\]
This excludes every PSD Gram rank over \(E\), without assuming that
a PSD matrix factors into squares over its coefficient field.

The positive definite exposing quadratic was checked by expanding its
tridiagonal factorization in general dimension. The diagonal coefficients
of \(L^{\mathsf T}GL\) are
\(2a\) on \(x_0^2\), \(a^2\) on \(x_s^2\), and
\(a^{2s-2i+2}\) on \(x_i^2\) for \(1\le i<s\).
Adjacent cross terms cancel except for \(-2x_0x_1\). The remaining
quadratic cross terms and the linear terms are exactly those in (8) of
the construction. The curve identity (11) can alternatively be checked
without this expansion: on \((t^s,\ldots,t^{2s})\), only
\(P_1\) and \(P_2\) survive, giving the displayed factorization
by \(t^p-2\).

The conditioning estimates follow from explicit matrices. In
\(G=D_aTD_a\), the diagonal entries of \(D_a\) lie in
\([1,\sqrt2)\), and the least eigenvalue of \(T\) is
\(1-\cos(\pi/(n+1))\ge2/(n+1)^2\). This gives
\(G\succeq I/(2n^2)\) and \(G\preceq4I\). The finite
geometric series for \((-aI+U)^{-1}\) has operator norm less than
\(n\), while \(\|-aI+U\|<3\). Consequently the stated
\(I/(2n^4)\) lower bound and \(36I\) upper bound for the
centered quadratic matrix are valid.

The residual equations have the claimed unique real zero. Their first
product equation ensures \(x_0\ne0\); the recurrence then gives
\(x_i=x_0t^i\), and the remaining equations give
\(x_0=t^s\) and \(t^{2s+1}=2\). The displayed inverse of the
normalized Jacobian was checked directly. Its first two coefficient norms
are at most \(1\) and \(1/\sqrt s\), respectively. Thus
\[
 |h_i|\le(1+2\sqrt s)\|\rho\|,
 \qquad \|h\|\le3n\|\rho\|.
\]
The row normalization divides by numbers at least one, and
\(\|u\|\le2\|h\|\), yielding
\(\sigma_{\min}(J)\ge1/(6n)\). The choice
\(\nu=1/(8n)\) is conservative. Each residual quadratic matrix has
norm at most one, including \(R_2=x_0x_2-x_1^2\); each gradient
has norm below eight. The condition \(s\ge2\) correctly prevents
the linear term of \(P_1\) from involving \(x_0\).

The rounding and full-Gram constants also check out. There are \(n+1\)
exposing weights. Rounding on the \(D^{-1}\) grid changes the
gradient by at most
\(8(n+1)/D=\varepsilon/8\), and the quadratic matrix by at most
\((n+1)/D=\varepsilon/64\). These errors preserve
\(H\succeq mI\), with \(m=1/(4n^4)\), and
\(\|H\|\le40\).

Using \(40+8n\le24n\), the most restrictive square-Gram condition
has right-hand side at least
\(1/(21233664n^{13})\). This exceeds
\(\varepsilon=1/(2^{40}n^{16})\) for every \(n\ge3\).
The other two conditions are immediate from the same choice. The
[imported Gram proof](sos-convex-quartic-realization.md) therefore gives
a quadratic block at least \(qI\), with \(q=2m^2\), and a Schur
complement at least \(\sigma I\), with
\(\sigma=3\varepsilon/(128n^2)\). Here \(q\ge\sigma\).
The bound on the cross block divided by \(q\) is at most
\(1152n^{10}\varepsilon<1\). Completing the block square gives
\[
 M_0\succeq\frac{\sigma}{4}I
       =\frac{3\varepsilon}{512n^2}I
       \succeq\frac{\varepsilon}{256n^2}I.
 \tag{3}
\]
Thus the lower bound concerns the entire Gram matrix, including directions
that are not tensor evaluation vectors.

For the omitted square, its centered gradient has squared norm less than
12, its quadratic matrix has operator norm \(1/2\), and its squared
Frobenius norm is \(1/2\). The block estimates
\(32\), \(12\sqrt n\), and \(5\) therefore suffice. The
whole-matrix bound \(37+24\sqrt n\le64n\) is valid. Finally,
\[
 D^2\frac{\varepsilon}{256n^2}
 =\frac{16(n+1)^2N^2}{n^2}>64n+1.
 \tag{4}
\]
This proves the centered full Hessian Gram is greater than the identity.
Since its evaluation vector includes \(v\), the global Hessian is at
least the identity. Vanishing and stationarity at \(b\) then prove
that zero is the unique global minimum.

The exact translation covariance was checked at the matrix-entry level,
not inferred from equality of polynomial evaluations. With
\(A_c=c\otimes I\), multiplication gives
\(A_c^{\mathsf T}Q(T)=D(2Tc,T)\) and the other two block identities
in (24). Congruence by
\(\left(\begin{smallmatrix}I&0\\-A_c&I\end{smallmatrix}\right)\)
therefore gives the canonical formula for the translated quadratic itself.
This applies to negative as well as positive linear combinations of
quadratic squares. Hence the positive definite centered Gram becomes
exactly the canonical Gram computed from the integer factors at zero.

To verify integrality explicitly, put \(W=2T\) for an integer
quadratic. The blocks then have entries
\[
 C=2bb^{\mathsf T}+2dW,\qquad
 D_{i,(k,j)}=b_kW_{ij}+2b_iW_{kj},\qquad
 Q=2\operatorname{vec}(W)\operatorname{vec}(W)^{\mathsf T}
                                      +W\otimes W.
 \tag{5}
\]
All are integers. The original-coordinate matrix remains positive
definite by congruence. Its lower bound need not remain the identity;
the global Hessian lower bound was already established using the centered
certificate. The checker proves the stronger original-coordinate
\(M-I\succ0\) only for its two tested outputs, which is sufficient
for those finite checks and is not needed for the universal claim.

The size and construction claims are consistent. The scales \(N,D\)
have polynomial magnitude in \(n\), and the rounded integer weights
are bounded by \(4D\). The quadratic \(A\) has \(O(n)\)
monomials; squaring it produces \(O(n^2)\), and the residual squares
add only \(O(n)\). Their integer coefficients have polynomial
magnitude. The canonical Gram has \(O(n^4)\) entries, each computed
from quadratic expressions in integer factor coefficients and the stated
integer weights, so its entries also have \(O(\log n)\) bits.
Computing each grid floor by comparison of
\(z^p\) with \(2^kD^p\) uses \(O(p\log n)\)-bit integers
and polynomially many bit operations. The representation
\(2a=a^{p+1}\) justifies the largest exponent in this comparison.

SOS sufficiency over \(K=\mathbb Q(a)\) is valid. Rational LDL
factorization of the positive definite integer Hessian Gram, followed by
rational square decompositions of its positive rational weights, gives a
rational Hessian SOS. Taylor integration at \(b\) uses only
\(K\)-coefficients. The integral identity in (25) has coefficients
\(1/2\), \(1/3\), and \(1/12\) after expansion, as required;
its first displayed term represents two identical squares. It introduces
no square-root extension. Combining this with (1)--(2) proves the exact
field characterization for both certificate types.

The cited primary statement of Scheiderer's Corollary 2.11 was also
inspected: it excludes any prescribed real number field using rational
real-SOS forms, including ternary quartics.
[Primary source, p. 1503](https://ems.press/content/serial-article-files/32129).
That prior statement and the present all-real-fields characterization have
different quantifiers. This check verifies the cited comparison only; it
does not establish publication priority for the new family or audit the
separate tower construction.

The targeted command actually run was

```text
python research-20260927/check_arbitrary_prime_strict_sos_field.py
```

It passed the generic two-variable covariance check, the stated scalar
inequalities for \(3\le n\le80\), and the exact \(p=5,7\)
construction, stationarity, coefficient obstruction, polynomial Hessian
identity, integer-entry, and positive-LDL checks. The metadata matched
the construction note: 31 and 50 monomials, coefficient bounds of 152 and
165 bits, and Gram-entry bounds of 153 and 167 bits. These finite tests
support the universal proof; they do not prove the arbitrary-prime theorem
by enumeration. A separate targeted integrity check of this new review
file passed. No project-wide verification or CI inspection was performed.
