# Exact SOS certificates can require an exponentially large coefficient field

Date: 2026-09-28. Status: quantitative theorem passed
[fresh adversarial review](exponential-least-sos-field-fresh-review.md)
and an [independent root audit](exponential-least-sos-field-root-audit.md).
Publication priority is unestablished.

For every \(k\geq1\), a polynomial-size rational strongly
SOS-convex quartic can have rational minimum zero while every real
coefficient field admitting an exact SOS certificate must contain
\(2^{1/5^k}\). The required field degree is exponential in the
number of variables, although a rational positive definite Hessian
Gram certificate has polynomial size.

The distinction is between coefficient fields, not between all possible
encodings. A [matching constructive upper bound](tower-sos-coefficient-encoding.md)
gives a polynomial-size SOS certificate when the coefficients share the
original root circuit. The result therefore does not say that every
circuit or tower representation is long, nor does it prove a
decision-complexity lower bound.
The [individual-coefficient strengthening](exponential-sos-individual-coefficient-degree.md)
shows that every algebraic certificate has at least one coefficient of
degree at least \(5^k\), so the obstruction also applies when dense
minimal polynomials are output separately for each coefficient.

## The theorem

**Theorem.** For each integer \(k\geq1\), one can construct in
deterministic time polynomial in \(k\) a rational quartic \(F_k\)
in \(N=3k\) variables and a rational positive definite Hessian
Gram matrix on \((v,X\otimes v)\), all of polynomial bit length,
such that:

1. \(\nabla^2F_k\succeq I\) everywhere, and its minimum is zero.
2. Its unique zero is
   \[
      p=(a_i,a_i^2,a_i^3)_{i=1}^k,
            \qquad a_i=2^{1/5^i}.
   \]
3. For every subfield \(E\subseteq\mathbb R\), the following are
   equivalent: \(a_k\in E\); \(F_k\) is a sum of polynomial
   squares over \(E\); and \(F_k\) has a positive semidefinite
   polynomial Gram matrix over \(E\) on the monomial basis of degree
   at most two.

Thus the smallest possible real coefficient field is exactly
\(\mathbb Q(2^{1/5^k})\), of degree \(5^k=5^{N/3}\).
One may clear denominators to obtain integer quartics with polynomial
coefficient bit length and the same statements. No assertion of a
minimal number of variables is made. Exponential growth is measured in
\(k\) or \(N\), not in the full dense input bit length; polynomial
output size in \(k\) gives a superpolynomial field-degree requirement
relative to that encoding, without asserting a \(2^{\Omega(\text{input bits})}\) bound.

## A polynomial-size baseline

Consider the root circuit

\[
 a_1^5=2,\qquad a_i^5=a_{i-1}\quad(2\leq i\leq k).
 \tag{1}
\]

Every gate has the rational box \([1,2]\). The first radicand is
two, and every later radicand interval is \([1,2]\), contained in
\([1,2^5]\). Hence the input condition of the
[reviewed signed odd-root construction](signed-odd-root-circuit-quartic.md)
is satisfied with degree five at every gate. No sign or scale change
is needed. Use local variables \((x_i,y_i,z_i)\), and set

\[
 b_1=2,\qquad b_i=x_{i-1}\ (i>1),
 \quad r_{i,1}=x_i^2-y_i,
 \quad r_{i,2}=x_iy_i-z_i,
 \quad r_{i,3}=y_iz_i-b_i.
 \tag{2}
\]

That construction returns positive rational \(t,\nu\), a rational
quadratic \(G\), and the quartic

\[
 F_0=\left(\frac{G}{t\nu}\right)^2+
                         \sum_{i=1}^k\sum_{j=1}^3
                                  \left(\frac{r_{i,j}}\nu\right)^2.
 \tag{3}
\]

The polynomial \(G\) vanishes at \(p\), and its homogeneous
quadratic matrix is positive definite. The baseline has a positive
definite rational Hessian Gram matrix \(M\) on the full basis
\((v,X\otimes v)\). The theorem supplies \(F_0,G,M,t,\nu\)
with polynomial bit length and polynomial construction time. This is
an explicit algorithmic dependency, not an assumption that the
degree-\(5^k\) minimal polynomial is expanded.

Let

\[
                     R=y_k^2-x_kz_k.
 \tag{4}
\]

This rational quadratic vanishes at \(p\). The counterexample will
be a sufficiently large positive rational multiple of \(F_0\),
minus \(R^2\).

## Exact convexity and the size of the multiplier

Let \(h=N+N^2\) be the Hessian Gram dimension. Define

\[
 \mu=\frac{\det M}{(\operatorname{tr}M)^{h-1}}>0,
 \qquad \lambda=\left\lceil\frac{17}{\mu}\right\rceil,
 \qquad F_k=\lambda F_0-R^2.
 \tag{5}
\]

If the eigenvalues of \(M\) are positive, each is at most its
trace. Their product consequently gives
\(\lambda_{\min}(M)\geq\mu\).

For the homogeneous quadratic \(R=X^{\mathsf T}TX\), the matrix
\(T\) is supported on the last three coordinates and has eigenvalues
\(1,1/2,-1/2\) there. Thus
\(\|T\|=1\) and \(\|T\|_F^2=3/2\). The Hessian biform
of \(R^2\) has the rational Gram matrix \(B\) with zero constant
and cross blocks and quadratic block

\[
 B_Q=8\operatorname{vec}(T)\operatorname{vec}(T)^{\mathsf T}
                       +4T\otimes T.
 \tag{6}
\]

It satisfies \(\|B\|\leq8(3/2)+4=16\). Therefore

\[
                  \lambda M-B\succeq I.
 \tag{7}
\]

This is a rational positive definite Hessian Gram matrix for \(F_k\).
Its first basis block is \(v\), so (7) proves
\(\nabla^2F_k\succeq I\) globally. Both terms in (5) have value
and gradient zero at \(p\). Thus \(p\) is the unique minimizer
and zero, with value zero.

The determinant, trace, and ceiling in (5) use rational arithmetic on
a polynomial-dimensional matrix of polynomial bit length. Their
outputs also have polynomial bit length. Hence \(\lambda\), the
quartic coefficients, and the final certificate have polynomial size
and are computed in polynomial time. Clearing a common positive
denominator preserves the field characterization below; positive
rational scaling and its inverse are sums of rational squares.

## A real-field lemma for a prime-power radical

Let \(a=2^{1/5^k}\), and let \(E\subseteq\mathbb R\) be an
arbitrary subfield. If \(a\notin E\), then

\[
                   [E(a):E(a^5)]=5.
 \tag{8}
\]

Here is a proof that also handles transcendental coefficient fields.
Let the minimal polynomial of \(a\) over \(E\) have degree
\(r\). It divides \(T^{5^k}-2\), so its roots are a subset
of the numbers \(a\zeta^{j}\), where \(\zeta\) is a primitive
\(5^k\)-th root of unity. Its constant term is
\((-1)^r a^r\zeta^j\) and belongs to the real field \(E\).
An odd-order root of unity is real only when it is one. Thus
\(a^r\in E\).

Let \(g=\gcd(r,5^k)\). An integer Bézout identity and
\(a^{5^k}=2\) give \(a^g\in E\). Minimality then gives
\(r\leq g\leq r\), because \(T^g-a^g\) is an annihilating
polynomial. Hence \(r=g=5^j\) for some \(j\), and the minimal
polynomial is \(T^r-a^r\). If \(a\notin E\), then \(r\geq5\).
The element \(a^5\) has degree at most \(r/5\) over \(E\),
while \(a\) has degree at most five over \(E(a^5)\). The tower
degree identity forces equality in both bounds and proves (8).

Put \(L=E(a^5)\). Every earlier tower coordinate belongs to \(L\),
since \(a_i=a^{5^{k-i}}\) for \(i<k\). Equation (8) says that
\(T^5-b\), with \(b=a^5\in L\), is irreducible over \(L\).

## The five quadratic relations in the last slice

For any real field \(L\), suppose \(T^5-b\) is irreducible
over \(L\), with real root \(a\), and consider
\((x,y,z)=(a,a^2,a^3)\). The quadratics

\[
 \begin{aligned}
 q_1&=x^2-y,&q_2&=xy-z,&q_3&=y^2-xz,\\
 q_4&=yz-b,&q_5&=z^2-bx
 \end{aligned}
 \tag{9}
\]

form a basis over \(L\) of all degree-at-most-two polynomials
vanishing at this point. Indeed the ten quadratic monomials evaluate
onto the degree-five field, using \(1,x,y,z,xz\) for powers zero
through four. The five displayed independent relations therefore
span the kernel.

Their fifteen pair products are linearly independent over \(L\).
It suffices to use their highest homogeneous parts

\[
                  x^2,\quad xy,\quad y^2-xz,\quad yz,\quad z^2.
 \tag{10}
\]

The fifteen pair products in (10) form a basis of homogeneous ternary
quartics. One can eliminate coefficients successively using their
monomials; equivalently, their integer coefficient matrix has determinant
\(-1\) in the order used in the retained checker. Thus every
polynomial in the span of the products in (9) has a unique symmetric
Gram matrix in that basis, with off-diagonal entries counted twice.

## Why every exact certificate must contain the full tower

Suppose \(E\subseteq\mathbb R\) does not contain \(a=a_k\),
and set \(L=E(a^5)\). Fix all earlier blocks of \(F_k\) to
their coordinates in \(p\), which belong to \(L\). The last
three variables remain \((x,y,z)\), and their parameter is
\(b=a^5\). In this slice, all earlier residuals in (3) are zero.
Writing \(g\) for the restriction of \(G/(t\nu)\), one obtains

\[
 (F_k)_{\mathrm{slice}}
   =\lambda\left(g^2+\nu^{-2}(q_1^2+q_2^2+q_4^2)\right)-q_3^2.
 \tag{11}
\]

The quadratic \(g\) lies in the \(L\)-span of (9), because it
vanishes at \((a,a^2,a^3)\). Its coefficient on \(z^2\) is
strictly positive: the quadratic matrix of \(G\) is positive
definite, and restriction to a coordinate slice preserves its last
diagonal entry. Scaling by \(t\nu>0\) preserves its sign.

Write \(g=\sum_{j=1}^5 c_jq_j\). Only \(q_5\) has a
\(z^2\) term, so \(c_5>0\). In the five-dimensional coefficient
space use the nonzero vector

\[
                         w=(0,0,c_5,0,-c_3).
 \tag{12}
\]

It is orthogonal to the coefficient vectors of \(g,q_1,q_2,q_4\).
The symmetric Gram matrix exhibited by (11) consequently has
quadratic value \(-c_5^2<0\) on \(w\). By product independence,
it is the unique Gram matrix on the space (9). It is not positive
semidefinite, for every value of \(\lambda>0\).

If \(F_k\) were SOS over \(E\), substituting the earlier
coordinates would give an SOS over \(L\) in the last three variables.
Every factor would have degree at most two and would vanish at
\((a,a^2,a^3)\), since the slice has value zero there. It would
therefore lie in the span (9), producing a positive semidefinite Gram
matrix in contradiction to (12). Hence \(F_k\) is not SOS over
any such \(E\).

The same argument rules out a positive semidefinite polynomial Gram
matrix over \(E\), without assuming it factors over \(E\).
Substitution of the earlier coordinates is a matrix congruence that
preserves positive semidefiniteness and places entries in \(L\).
At the real zero, \(m(p)^{\mathsf T}Qm(p)=0\) for its monomial
vector implies \(Qm(p)=0\). Each row of \(Q\) consequently
represents a vanishing quadratic over \(L\). Expressing its row and
column spaces in the basis (9) gives a positive semidefinite Gram
matrix on that basis, again contradicting uniqueness and (12).

## Sufficiency of the tower field

If \(a_k\in E\), all coordinates of \(p\) lie in \(E\).
The rational positive definite Hessian Gram certificate can be written
as a rational SOS biform. At the stationary zero, Taylor integration
then expresses \(F_k\) as SOS over \(E\). Explicitly, each
substituted biform square has the form \((U+tV)^2\), with
coefficients in \(E\), and

\[
 \int_0^1(1-t)(U+tV)^2\,dt
       =\tfrac12(U+V/3)^2+(V/6)^2.
\]

The positive rational weights are sums of rational squares, so no extra
square roots of field elements are introduced. The resulting square
factors provide a positive semidefinite polynomial Gram matrix over
the same field. This proves all equivalences in the theorem.

Finally \(T^{5^k}-2\) is irreducible over \(\mathbb Q\) by
Eisenstein's criterion. Thus the necessary contained field has degree
exactly \(5^k\), and that field itself suffices. Any real number
field carrying either certificate has degree divisible by \(5^k\).

## Verification, comparison, and limits

The [exact local checker](check_exponential_least_sos_field.py) verifies
the integer determinant for the fifteen leading products, the
vanishing relations, the symbolic negative Gram direction, and the
perturbation Hessian Gram identity and norm bound. The command is

```text
python research-20260927/check_exponential_least_sos_field.py
```

The baseline construction has its own independent proof and mixed-sign
exact checks. The new field lemma, restriction argument, and polynomial
multiplier bound passed the linked fresh review and root audit. These
reviews reconstruct the universal arguments; the finite symbolic checks
do not establish their universal quantifiers. No project-wide or CI
checks are part of this verification.

The [fixed-quintic example](ternary-rational-sos-convex-counterexample.md)
already requires \(\mathbb Q(2^{1/5})\) for its exact certificate.
This theorem uses a compact root tower to make the least coefficient
field exponential while retaining rational strong-convexity certificates
of polynomial size. Existing failures of rational SOS descent remain
essential prior; their general existence is not claimed new. A scoped
literature audit of the exponential least-field conclusion is still
needed, and no priority claim follows from the present construction.

The obstruction concerns polynomial squares and polynomial Gram
matrices. It does not extend to rational-function SOS certificates:
the [prior-theory regular-denominator corollary](rational-denominator-certificate-frontier.md#3-the-general-regular-denominator-existence-result-is-prior-theory)
applies here. Indeed the strict full Hessian Gram gives a positive
definite leading quartic form, and the real zero is unique and
nondegenerate. A rational-function SOS with no real poles therefore
exists over \(\mathbb Q\). This theorem gives no useful uniform bound
on its denominator degree; the quadratic denominator found for the
earlier fixed ternary example is not asserted for this tower.

A [subsequent reviewed construction](rational-tower-quadratic-denominator.md)
does obtain a quadratic common denominator for this tower family by
choosing a possibly larger polynomial-bit multiplier than (5). That
choice preserves every field and individual-degree conclusion above.
It is a stronger selectable construction, not a claim that the specific
multiplier in (5) already satisfies the additional denominator bound.

The consequence for exact optimization is an arithmetic certificate
boundary. Even a strictly positive definite rational certificate of
convexity does not ensure a rational certificate of the exact optimum,
or one over a real number field of polynomial degree. Shared root-circuit
SOS descriptions and [rational auxiliary certificates](tower-rational-auxiliary-certificate.md)
are nevertheless polynomial in size. The theorem does
not show NP-hardness, obstruct approximate optimization, or bound all
possible proof systems.
