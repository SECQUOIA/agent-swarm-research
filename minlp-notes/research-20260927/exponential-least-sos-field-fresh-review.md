# Fresh review of the exponential least SOS coefficient field

Date: 2026-09-28. Verdict: the mathematical construction and the
coefficient-field characterization pass independent adversarial review.
No substantive gap was found. This review does not establish publication
priority.

The fully reviewed core manuscript has SHA-256
0ecae21340746b95d3e425a193e1eae89afded01cb40f6110d403c872bab725c.
The individual-coefficient supplement below was checked after that core
manuscript was frozen.

The [main theorem](exponential-least-sos-field.md) constructs rational
quartics in \(N=3k\) variables, with polynomial-size positive definite
rational Hessian Gram certificates and minimum zero, for which
\[
 F_k\in\Sigma E[X]^2
 \quad\Longleftrightarrow\quad
 2^{1/5^k}\in E
\]
for every subfield \(E\subseteq\mathbb R\). The same equivalence
holds for positive semidefinite Gram matrices over \(E\) on the
full monomial basis of degree at most two. Thus the least possible
coefficient field is the specified degree-\(5^k\) field.

I did not develop the construction. I independently reconstructed the
field, restriction, unique-Gram, convexity, and size arguments after
receiving the candidate. I also read the complete
[signed-root construction](signed-odd-root-circuit-quartic.md)
and its [existing independent review](signed-odd-root-circuit-review.md).
Their general construction is an explicit input to this theorem; I did
not rerun its exact checks for mixed-sign circuits.

## The inherited construction applies to every tower gate

Write \(a_i=2^{1/5^i}\). The boxes \([1,2]\) satisfy the
signed-root theorem's actual interval requirement: the first radicand
is \(2\), and each later radicand interval is \([1,2]\), contained
in \([1,32]\). All degrees are five, so their unary encoding has
size \(O(k)\), and there are exactly \(3k\) retained variables.
The normalization has sign \(+1\) and scale one. No root-separation
certificate with hidden exponential bit length is being assumed.

The residuals are
\[
 x_i^2-y_i,\qquad x_iy_i-z_i,\qquad y_iz_i-b_i,
 \qquad b_1=2,\quad b_i=x_{i-1}\ (i>1).
\]
Their common real zero is precisely
\(p=(a_i,a_i^2,a_i^3)_i\), since the first two equations enforce
powers and the last enforces the unique real fifth root.

The imported result supplies the stated rational \(G,t,\nu,F_0,M\)
in polynomial time and with polynomial bit length. In particular,
\(G(p)=0\), its homogeneous quadratic matrix is positive definite,
and \(M\succ0\) is a rational Hessian Gram on the uncentered full
vector \((v,X\otimes v)\). The last property, rather than strong
convexity alone, is needed for the perturbation argument.

## The perturbation preserves a strict rational Hessian certificate

For \(R=y_k^2-x_kz_k=X^{\mathsf T}TX\), the nonzero block of
\(T\) has eigenvalues \(1,1/2,-1/2\). Hence
\(\|T\|=1\) and \(\|\operatorname{vec}T\|^2=3/2\).
Direct differentiation gives the Hessian Gram block
\[
 B_Q=8\operatorname{vec}(T)\operatorname{vec}(T)^{\mathsf T}
       +4T\otimes T.
\]
The rank-one term has norm \(12\); the Kronecker term has norm
\(4\). Thus \(\|B\|\le16\), independently of the number of
earlier gates.

Let \(h=N+N^2\) and
\[
 \mu=\frac{\det M}{(\operatorname{tr}M)^{h-1}},
 \qquad \lambda=\lceil17/\mu\rceil.
\]
For each eigenvalue \(\eta_j>0\) of \(M\), all the other
eigenvalues are at most \(\operatorname{tr}M\), so
\(\eta_j\ge\mu>0\). It follows that
\[
 \lambda M-B\succeq
 (\lambda\mu-\|B\|)I\succeq I.
\]
This certifies \(\nabla^2F_k\succeq I\) for
\(F_k=\lambda F_0-R^2\). Both \(F_0\) and \(R^2\) have
value and gradient zero at \(p\). Strong convexity therefore proves
that the unique zero and minimizer is \(p\), and the minimum is
zero. Nonnegativity is established after the perturbation, rather than
inferred merely from its signed-square expression.

Exact determinant computation, rational powers of a trace, and the
ceiling operation have polynomial bit cost here. Clearing denominators
in an \(h\)-dimensional rational matrix of polynomial entry length
and applying determinant bounds gives polynomial numerator and
denominator lengths. Raising the trace to the exponent \(h-1\)
also has polynomial length. Consequently neither \(\mu\) nor
\(\lambda\) hides an exponential-length rational coefficient.

## The intermediate-field step is valid for arbitrary real fields

This is stronger than just applying quintic irreducibility once the
radicand has been adjoined. One must show that adjoining \(a^5\)
cannot already recover \(a\) when \(a\notin E\).

Set \(a=2^{1/5^k}\), and let the minimal polynomial of \(a\)
over \(E\subseteq\mathbb R\) have degree \(r\). It divides
\(T^{5^k}-2\). Its constant term is
\((-1)^r a^r\zeta^j\) for a \(5^k\)-th root of unity
\(\zeta^j\). Reality of the constant term forces
\(\zeta^j=1\), since an odd-order root of unity cannot be
\(-1\). Therefore \(a^r\in E\).

With \(g=\gcd(r,5^k)\), an integer Bézout identity gives
\(a^g\in E\). Negative exponents cause no problem because \(a\)
and \(2\) are nonzero. Thus the minimal degree satisfies
\(r\le g\le r\). Hence \(r=g=5^j\) for some \(0\le j\le k\),
and \(a^r\in E\). When \(a\notin E\), one has \(r\ge5\).
Now
\[
 [E(a^5):E]\le r/5,\qquad
 [E(a):E(a^5)]\le5.
\]
Their product is \(r\), so both inequalities are equalities.
This proves
\[
 [E(a):E(a^5)]=5.
\]
No number-field or finite-generation assumption on \(E\) has entered
this proof.

For \(L=E(a^5)\), every earlier \(a_i\) belongs to \(L\).
The polynomial \(T^5-a^5\) is irreducible over \(L\), so
\(1,a,a^2,a^3,a^4\) are linearly independent over \(L\).
This gives exactly the required setting for the last-gate slice.

## The quadratic space and its Gram map

Put \(b=a^5\). The degree-at-most-two evaluation map at
\((a,a^2,a^3)\) has rank five, using the monomials
\(1,x,y,z,xz\). Its five-dimensional kernel has basis
\[
 q=(x^2-y,\ xy-z,\ y^2-xz,\ yz-b,\ z^2-bx).
\]
These relations vanish by \(a^5=b\), and independence follows
from their distinct leading monomials
\(x^2,xy,y^2,yz,z^2\).

I checked product independence by explicit monomial reconstruction,
without relying on the retained checker's determinant. Write
\[
 s=(x^2,xy,y^2-xz,yz,z^2).
\]
Ten products immediately give the ten distinct monomials
\[
 x^4,\ x^3y,\ x^2yz,\ x^2z^2,\ x^2y^2,\ xy^2z,\
 xyz^2,\ y^2z^2,\ yz^3,\ z^4.
\]
The five missing quartic monomials follow from
\[
\begin{aligned}
 x^3z&=s_2^2-s_1s_3,&
 xy^3&=s_2s_3+s_1s_4,\\
 y^4&=s_3^2+2s_2s_4-s_1s_5,&
 y^3z&=s_3s_4+s_2s_5,\\
 xz^3&=s_4^2-s_3s_5.
\end{aligned}
\]
Thus the fifteen products span the fifteen-dimensional homogeneous
quartic space and are independent. Comparing highest homogeneous parts
then proves independence of the fifteen products \(q_iq_j\).
This argument works independently of the parameter \(b\).

Fixing all earlier variables at their coordinates in \(p\) leaves
\[
 H=\lambda\left(g^2+\nu^{-2}(q_1^2+q_2^2+q_4^2)\right)-q_3^2,
\]
where \(g\) is the restriction of \(G/(t\nu)\).
All its coefficients lie in \(L\), and \(g(a,a^2,a^3)=0\);
hence \(g=c^{\mathsf T}q\) with \(c\in L^5\).
The coefficient \(c_5=[z^2]g\) is positive, since it is a positive
diagonal entry of the quadratic matrix of \(G\), divided by
\(t\nu>0\).

The displayed Gram matrix has negative quadratic value
\(-c_5^2\) on
\[
 w=(0,0,c_5,0,-c_3).
\]
The vector annihilates \(c,e_1,e_2,e_4\), while its pairing with
\(e_3\) is \(c_5\). Product independence makes this Gram matrix
unique on the \(q\) basis. It therefore excludes every positive
semidefinite Gram on that basis, for every positive \(\lambda\).

## Polynomial SOS and PSD Gram necessity are separate arguments

An SOS over \(E\), after substitution of the earlier coordinates,
is an SOS over \(L\). Real squares of highest degree cannot cancel,
so all factors have degree at most two. The zero value at
\((a,a^2,a^3)\) forces every factor to vanish there. Each is an
\(L\)-linear combination of the \(q_i\), contradicting the
unique indefinite Gram.

For a PSD Gram matrix, no square factorization over \(E\) is
assumed. The substitution is a congruence over \(L\) and yields a
PSD matrix \(Q\) on the last three variables' monomial vector \(m\).
At the zero, \(m(p)^{\mathsf T}Qm(p)=0\), and real positive
semidefiniteness gives \(Qm(p)=0\). Thus each row of \(Q\)
is a vanishing quadratic over \(L\).

To make the descent to the five-dimensional basis explicit, write
\(q=Vm\), with \(V\in L^{5\times10}\) of full row rank.
Choose a right inverse \(S\in L^{10\times5}\), so \(VS=I\).
The row-space inclusion and symmetry give
\[
 Q=V^{\mathsf T}(S^{\mathsf T}QS)V.
\]
The middle matrix is PSD by congruence. It represents the same
polynomial on the \(q\) basis and contradicts the unique negative
direction above. This avoids the invalid general inference that a
PSD matrix over an arbitrary real field must factor as squares over
that same field.

## Sufficiency uses only rational scalar square decompositions

If \(a\in E\), then \(p\in E^N\). The rational positive
definite Hessian Gram factors into rational polynomial squares after
rational LDL and rational four-square decompositions of positive
rational weights. In Taylor's integral at \(p\), each such factor
becomes \(U+\tau V\), with polynomial coefficients in \(E\).
The exact identity
\[
 \int_0^1(1-\tau)(U+\tau V)^2\,d\tau
 =\frac12(U+V/3)^2+(V/6)^2
\]
gives squares over \(E\), since \(1/2=(1/2)^2+(1/2)^2\).
No square root of a possibly nonsquare positive element of \(E\)
is needed. The resulting SOS also gives a PSD Gram over \(E\).

Finally, Eisenstein's criterion at two gives
\([\mathbb Q(a):\mathbb Q]=5^k\). Every admissible real
coefficient field contains this field, and this field itself works.
For a number field carrying a certificate, its degree is consequently
divisible by \(5^k\). Positive rational scaling and its inverse
preserve SOS over every \(E\), and preserve PSD Grams directly,
so clearing coefficient denominators is harmless.

## Significance, prior results, and verification scope

The theorem first bounds the joint coefficient field of the
certificate. The separately reviewed supplement below strengthens this
to the degree of an individual algebraic coefficient. Both bounds are
exponential in the number \(N=3k\) of variables. Polynomial input
size in \(k\) does not by itself mean a lower bound
\(2^{\Omega(L)}\) in the full dense input length \(L\).
Neither bound lower-bounds radical circuits, field towers, or other
compact coefficient representations.

There is relevant stronger prior than mere failure of rational descent.
[Scheiderer's Corollary 2.11](https://ems.press/content/serial-article-files/32129),
printed page 1503, constructs a rational form of any even degree at
least four that is real SOS but not SOS over any prescribed real
number field. I directly checked that primary statement and its
construction scope. It excludes a fixed field; it does not state an
exact least field or a lower bound applying to all fields of bounded
degree. The strict convexity, polynomial-size quintic tower, and exact
containment characterization are additional assertions proved here.
Their priority still requires a broader literature audit.

The obstruction is specifically to polynomial SOS and polynomial Gram
certificates. The [prior-theory sphere corollary](rational-denominator-certificate-frontier.md)
applies to these quartics and supplies rational-function SOS
certificates over \(\mathbb Q\) with no real poles: a strict full
Hessian Gram gives a positive definite leading quartic form, and the
unique zero is nondegenerate. No degree-two denominator bound for the
whole tower has been established.

I read the new local checker and reconstructed the universal arguments
above. I did not rerun its determinant, Hessian identity, or Gram
direction calculations, which would duplicate its exact algebra.
The monomial reconstruction above is a separate proof of product
independence. No finite computation is being used to certify the
arbitrary-field lemma or the all-\(k\) size claim. No project-wide
verification, CI inspection, or Lean formalization was performed.

The targeted commands actually run were the core manuscript's
SHA-256 check and an inline Python document check. The latter passed
this review's four local links, math-delimiter balance, final newline,
trailing whitespace, and control-character checks. These document
checks do not establish the mathematical claims.

## Supplement: one algebraic coefficient must already have large degree

The following strengthening was proposed after the core construction.
It also passes independent review.

**Lemma.** Let \(m=5^k\), \(k\ge1\), and let
\(\beta_1,\ldots,\beta_s\) be finitely many algebraic numbers.
If
\[
 2^{1/m}\in\mathbb Q(\beta_1,\ldots,\beta_s),
\]
then some \(\beta_i\) has degree at least \(m\) over
\(\mathbb Q\).

**Proof.** Put \(a=2^{1/m}\),
\(C=\mathbb Q(\zeta_m)\), and
\(C^+=\mathbb Q(\zeta_m+\zeta_m^{-1})\). The last field is
totally real: all its embeddings send the generator to
\(2\cos(2\pi j/m)\). The real-field lemma already proved above
says that the minimal polynomial of \(a\) over \(C^+\) is
\(T^r-a^r\), where \(r\mid m\). If \(r<m\), then
\(a^r\in C^+\) has rational minimal polynomial \(T^{m/r}-2\)
by Eisenstein's criterion. That polynomial has nonreal roots.
This is impossible for an element of a totally real number field,
since every embedding of its generated subfield extends to the larger
number field. Therefore \([C^+(a):C^+]=m\).

The field \(C^+(a)\) lies in \(\mathbb R\), so it does not
contain \(\zeta_m\). The quadratic polynomial of \(\zeta_m\)
over \(C^+\) remains irreducible over \(C^+(a)\): one of its
roots would otherwise belong to that real field. Hence
\([C(a):C^+(a)]=2\). Comparing the two towers over \(C^+\)
gives \([C(a):C]=m\). Because \(C\) contains all \(m\)-th
roots of unity, \(S=C(a)\) is the splitting field of \(T^m-2\)
over \(\mathbb Q\), and its automorphism fixing \(C\) and
sending \(a\) to \(\zeta_m a\) has order \(m\).

Let \(d_i=[\mathbb Q(\beta_i):\mathbb Q]\), and let \(K_i\)
be the normal closure of \(\mathbb Q(\beta_i)\). Their compositum
\(K\) is finite Galois over \(\mathbb Q\), and restriction
embeds its Galois group into
\[
 \operatorname{Gal}(K/\mathbb Q)
 \hookrightarrow
 \prod_i\operatorname{Gal}(K_i/\mathbb Q)
 \hookrightarrow\prod_i\mathfrak S_{d_i}.
\]
The first map is injective because the \(K_i\) generate \(K\);
the second uses the faithful permutation action on each minimal
polynomial's roots.

Suppose all \(d_i<m\). An element of \(\mathfrak S_{d_i}\)
has order equal to the least common multiple of its cycle lengths.
Every such cycle length is below \(5^k\), so the largest power
of five dividing the permutation's order is at most \(5^{k-1}\).
The same holds for an element of the direct product, independently
of the number of factors.

On the other hand, \(a\in K\) by hypothesis. Normality forces
\(K\) to contain every conjugate of \(a\), hence \(S\subseteq K\).
The restriction map
\(\operatorname{Gal}(K/\mathbb Q)\to
\operatorname{Gal}(S/\mathbb Q)\) is surjective. A lift of the
order-\(m\) automorphism found above has order divisible by \(m\),
contradicting the preceding bound. Thus some \(d_i\ge m\).
\(\square\)

I first independently checked the order-\(m\) automorphism by another
route: two is unramified in the cyclotomic field \(C\), and
\(T^m-2\) is Eisenstein at a prime of \(C\) above two.
The root then supplied the elementary totally-real argument written
above. I checked its irreducibility and quadratic-extension steps
separately; it avoids the ramification input.

Applied to the finite list of algebraic coefficients in a polynomial
SOS certificate or a PSD Gram certificate for \(F_k\), the core
theorem supplies the lemma's containment assumption. At least one
individual coefficient therefore has algebraic degree at least
\(5^k\). Any representation that prints that coefficient's minimal
polynomial as a dense coefficient list needs at least \(5^k+1\)
positions. This is a certificate-output lower bound for that particular
encoding.

The algebraic-list hypothesis is substantive. The lemma makes no
assertion about arbitrary transcendental coefficient descriptions.
It also gives no lower bound for a sparse defining polynomial, a
radical expression, or a short root tower. The polynomial
\(T^{5^k}-2\) itself has only two nonzero terms, so degree alone
would not justify a sparse-list lower bound.
