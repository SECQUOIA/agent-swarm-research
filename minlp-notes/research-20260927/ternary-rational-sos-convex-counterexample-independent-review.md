# Fresh review of the ternary SOS counterexample and its coefficient field

Date: 2026-09-28. Status: the field argument, rational SOS obstruction,
qualitative construction, explicit Hessian certificate, and exact
coefficient-field classification pass independent adversarial review. No novelty
claim is established by this review.
The final integrated mathematical argument, including the strengthened
SOS and PSD Gram field equivalences, was read and checked.

The [main note](ternary-rational-sos-convex-counterexample.md) and its
[explicit checker](check_ternary_rational_sos_convex_counterexample.py)
use the positive root \(a^5=2\), the point
\(p=(a^{-1},a,a^{-3})\), and integer quadrics

\[
\begin{aligned}
r_0&=2-2xy,&r_1&=2x^2-2yz,&r_2&=2y^2-4z,\\
r_3&=2z^2-x,&r_4&=2xz-y.
\end{aligned}
\]

Set \(E=4r_0+5r_1+3r_2+9r_3\). The verified polynomial is

\[
                  F=E^2+\sum_{i=0}^3r_i^2-r_4^2.       \tag{1}
\]

The negative square is compatible with global strong convexity. It
prevents a rational SOS representation only because of the arithmetic
restrictions on quadratic polynomials vanishing at \(p\).

## The complete quadratic vanishing space

Eisenstein at two proves that \(K=\mathbb Q(a)\) has degree five.
All coordinates of \(p\) are in \(K\), and its second coordinate is
\(a\), so its coordinate field is exactly \(K\). Write \(q_i=r_i/2\).
All five \(q_i\) vanish at \(p\). In the basis
\((1,a,a^2,a^3,a^4)\), the ten quadratic monomials evaluate to

| Monomial | Evaluation |
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

The evaluation map has rank five. Its kernel \(I_2\) over
\(\mathbb Q\) therefore has dimension five. The independent quadratic
coefficients of \(q_0,\ldots,q_4\) prove that these quadrics form a
basis. Having five displayed vanishing equations alone would not have
sufficed; surjectivity and dimension establish the entire kernel.

## Two independent forms of the SOS obstruction

The fifteen products \(q_iq_j\), \(i\leq j\), are independent.
I checked this by exact rational linear algebra with an independently
chosen minor. In the column order given by lexicographic \((i,j)\),
the rows

\[
\begin{gathered}
1,z,y,x,z^2,yz,y^2,xz,xy,x^2,\\
yz^2,y^2z,y^3,xyz,y^2z^2
\end{gathered}
\]

have determinant \(-1/128\). This certifies injectivity of the Gram
coefficient map on the five-dimensional vanishing space. The checker
uses a different nonzero minor obtained by setting \(x=0\), so these
are independent exact witnesses to the same claim.

In the integer basis \(r=(r_0,\ldots,r_4)\), the unique symmetric Gram
matrix for (1) is

\[
 ww^{\mathsf T}+\operatorname{diag}(1,1,1,1,-1),
 \qquad w=(4,5,3,9,0)^{\mathsf T}.
\]

Its last diagonal entry is \(-1\), so it is not positive semidefinite.
This excludes a rational SOS once every rational square factor is
known to belong to \(I_2\).

There is also a simpler dual check. Define the rational linear
functional on quartics

\[
                   \ell(P)=2[z]P+4[y^2]P.
\]

Direct expansion gives

\[
 \ell(r_ir_j)=4\,\mathbf 1_{\{i=j=4\}},\qquad
 \ell\!\left(\left(\sum_i c_ir_i\right)^2\right)=4c_4^2.
\]

But \(\ell(F)=-4\). If \(F=\sum_j f_j^2\) with rational
polynomials \(f_j\), every factor has degree at most two: highest
homogeneous parts of real squares cannot cancel. Since \(p\) is real
and \(F(p)=0\), every \(f_j(p)=0\). The basis result forces each
factor into \(I_2\), where the functional is nonnegative on squares,
contradicting \(\ell(F)=-4\).

The restriction to \(I_2\) is essential. For example,
\(\ell((1-z)^2)=-4\). This is not a positive functional on all
quadratic squares and does not rule out a real SOS. Also, unlike the
earlier four-variable perturbation, this \(F\) belongs to
\(\operatorname{span}_{\mathbb Q}\{qr:q,r\in I_2\}\). Membership in
that linear space alone is therefore not sufficient for rational SOS.

## Existence of a suitable strictly positive Hessian Gram baseline

The imported [cyclic construction](cyclic-quartic-exponential-degree.md)
does apply to this exact point and these first four quadrics. Its
exposing quadratic is

\[
 Q_*=q_0+a^2q_1+a^{-2}q_2+a^6q_3.
\]

With \(X_0=1,X_1=ax,X_2=y/a,X_3=a^3z\), it satisfies

\[
             Q_*=\frac12\sum_{i=0}^3(X_i-X_{i+1})^2,
             \qquad X_4=X_0.
\]

This is a positive definite quadratic centered at \(p\). The Jacobian
of \(q_0,q_1,q_2\) has determinant \(-10a^{-2}\) at \(p\), so
the first four residuals have full Jacobian rank three.

The existing Gram regularization proof consequently gives a rational
baseline \(G\), formed from squares of combinations of the first four
quadrics, with a positive definite Hessian Gram matrix on the full
twelve-entry basis \((v,x\otimes v)\). One can also check the decisive
step directly: the centered constant block is of order
\(\epsilon J^{\mathsf T}J\succ0\), the cross block is of order
\(\epsilon\), and the quadratic block tends to
\[
 8\operatorname{vec}(H)\operatorname{vec}(H)^{\mathsf T}
                         +4H\otimes H\succ0.
\]
For small \(\epsilon>0\), the Schur complement is positive. Rational
approximation of the exposing weights preserves the exact zero and,
with enough precision, the strict Gram inequality.

If \(M\succ0\) represents the Hessian of this \(G\), and \(N\)
represents that of \(q_4^2\), then \(\lambda M-N\succ0\) for
sufficiently large rational \(\lambda\). This establishes the
qualitative perturbation argument. Since all quadrics vanish at \(p\),
both the value and gradient of \(\lambda G-q_4^2\) vanish there.
Strong convexity then makes this its unique global zero and minimizer.

## The explicit small integer example is separately certified

The concrete choice (1) does not rely on an unspecified approximation
or sufficiently large multiplier. I inspected and reran the entire
checker. It constructs a rational \(12\times12\) Hessian Gram matrix
\(M\) on \((v,u\otimes v)\), centered at
\[
                  (3/4,1,1/2),\qquad u=x-(3/4,1,1/2).
\]
It proves the differentiated identity exactly and verifies by rational
\(LDL^{\mathsf T}\) factorization that \(M-I\succ0\). The square
Gram formula includes the constant term \(4dT\) at this rational
center; omitting that term would have been an error.

I also checked the twelve leading principal determinants of \(M-I\)
with a separate exact determinant calculation. They are all positive.
Thus \(M-I\succ0\) also follows from Sylvester's criterion.
The matrix \(2M\) is integral, and its entries have numerator and
denominator bit length at most 12. The polynomial has 31 monomials
and maximum absolute integer coefficient 448. These metadata checks
passed as well. I also checked every listed leading principal minor
of \(2(M-I)\) against the corresponding integer in the main note.
An additional exact LDL calculation verified that the concrete SOS
baseline \(E^2+\sum_{i=0}^3r_i^2\) itself has a positive definite
Hessian Gram matrix; this does not follow merely by adding the
indefinite Gram representation of \(r_4^2\) to \(M\).

Because the basis contains \(v\), the certificate gives
\[
 v^{\mathsf T}\nabla^2F(x)v\geq\|v\|^2
\]
globally. Rational translation of the full basis is an invertible
congruence, so a rational positive definite Hessian Gram matrix also
exists in the original coordinates. Exact evaluation modulo \(a^5-2\)
checks \(F(p)=0\) and \(\nabla F(p)=0\). Therefore \(F\geq0\),
with unique zero \(p\). The negative square causes no unresolved
nonnegativity issue.

## Exactly which real fields contain SOS or PSD Gram certificates

The stronger classification holds for every subfield \(E\subseteq
\mathbb R\), including fields that are not algebraic over \(\mathbb Q\):
the polynomial has an SOS over \(E\), or a positive semidefinite Gram
matrix with entries in \(E\), if and only if \(a\in E\).

First, if \(a\notin E\), then \(T^5-2\) is irreducible over \(E\).
Indeed, a proper monic factor of degree \(r\), with \(1\leq r\leq4\),
would have constant coefficient
\[
              (-1)^r a^r\zeta_5^k\in E
\]
for some integer \(k\). This coefficient is real. The only real fifth
root of unity is one, so \(a^r\in E\). Since \(\gcd(r,5)=1\),
integers \(u,v\) satisfy \(ru+5v=1\); consequently
\(a=(a^r)^u2^v\in E\), a contradiction. The prime exponent and the
real embedding are both used in this argument.

Thus the five powers of \(a\) remain independent over \(E\), and the
kernel of quadratic evaluation at \(p\) over \(E\) is exactly
\(\operatorname{span}_E(r_0,\ldots,r_4)\). An SOS over \(E\)
would have quadratic factors vanishing at \(p\). The functional
identity would give \(\ell(F)\geq0\), since \(4c_4^2\geq0\) in
the specified real embedding. This contradicts \(\ell(F)=-4\).

The PSD Gram claim needs a separate argument: over a general real
field, a PSD Gram matrix need not factor into squares over that field.
Let \(m\) be the ten-entry monomial vector of degree at most two, and
suppose \(F=m^{\mathsf T}Qm\), where \(Q\in\operatorname{Sym}_{10}(E)\)
is positive semidefinite in the given real embedding. From
\[
                m(p)^{\mathsf T}Qm(p)=F(p)=0
\]
one obtains \(Qm(p)=0\). Hence each row of \(Q\) is the coefficient
vector of a quadratic in the evaluation kernel. Let \(B\) be the
rational \(10\times5\) matrix whose columns are the coefficients of
the \(r_i\). Symmetry gives \(\operatorname{im}Q\subseteq
\operatorname{im}B\). Choose a rational left inverse \(C\) of \(B\).
Then
\[
 S=CQC^{\mathsf T}\succeq0,\qquad Q=BSB^{\mathsf T}.
\]
The second identity follows from \(BCQ=Q\) and its transpose. Therefore
\[
                \ell(F)=\ell(r^{\mathsf T}Sr)=4S_{44}\geq0,
\]
again a contradiction. This covers all ranks, rather than only maximal
Gram matrices.

Conversely, \(K=\mathbb Q(a)\) itself supports an SOS decomposition.
Factor the rational positive definite Hessian Gram matrix by rational
\(LDL^{\mathsf T}\); represent each positive rational diagonal
weight as at most four rational squares. This writes its biform as
at most \(12\cdot4=48\) rational polynomial squares.
After substituting \(x=p+tu\) and direction \(u\), each factor is
\(A(u)+tB(u)\), with coefficients in \(K\) and degree at most two
in \(u\). Taylor integration uses the exact identity

\[
\begin{aligned}
\int_0^1(1-t)(A+tB)^2\,dt
 &=\frac12A^2+\frac13AB+\frac1{12}B^2\\
 &=2\left(\frac{A+B/3}{2}\right)^2+\left(\frac B6\right)^2.
\end{aligned}
\]

Thus each Hessian square contributes three \(K\)-squares, without
adjoining square roots of the rational integration weights. Translating
\(u=x-p\) retains coefficients in \(K\). There is consequently an
SOS over \(K\) with at most 144 squares. No minimal-length claim is
made.

If \(a\in E\), this same SOS is defined over \(E\), and its coefficient
vectors give a PSD Gram matrix over \(E\). This proves both directions
of the stated classification. In particular, every real coefficient
field of either certificate must actually contain \(K\); a mere
divisibility condition on its degree would be weaker.

The minimum degree of a real algebraic coefficient field is therefore
exactly five. In particular an SOS cannot have all coefficients
constructible: finitely many constructible real numbers lie in one
number field of power-of-two degree. The qualification “real” is
essential; over a field containing \(i\), sums of squares do not have
the positivity meaning used here.

## Minimal affine dimension: precise scope

I checked [Scheiderer's published Theorem 4.1](https://ems.press/content/serial-article-files/32129).
It classifies nonnegative rational ternary quartic forms that are not
rational SOS as products of four complex lines in general position.
The repository's two-variable consequence is valid: a positive
definite full Hessian Gram makes the leading quartic strictly positive
away from zero, so homogenization has no zeros at infinity. Strong
convexity permits one affine zero. The exceptional classification would
instead give two distinct real projective zeros, one from each
conjugate pair of lines. Real lines are excluded by nonnegativity.

Thus no two-variable counterexample has all the stated strict Gram
hypotheses. In one variable a stationary zero of a rational quartic
has minimal polynomial of degree at most two, since its square divides
the quartic. An irrational quadratic root would supply two distinct
real zeros, contrary to strong convexity. The minimizer is rational,
and Taylor integration gives rational SOS.

Three is therefore the minimum affine dimension within this
positive-definite-full-Hessian-Gram class. This review does not extend
that minimality claim to hypotheses that merely say “strongly convex”
or “SOS-convex” without the full-basis positive definiteness condition.

The claim that \(F+\eta\) is rational SOS for every rational
\(\eta>0\) follows from the separately
[reviewed positive-constant lemma](rational-sos-convex-descent-review.md).
The present full positive definite Hessian Gram certificate meets all
its assumptions. Consequently the rational SOS lower-bound supremum
is zero and is unattained, while the real SOS bound is attained.

## Verification scope

Command actually run:

    python research-20260927/check_ternary_rational_sos_convex_counterexample.py

Result: passed. Independent inline SymPy calculations checked the
evaluation rank, the five-dimensional quadratic kernel, product
injectivity and the displayed \(-1/128\) minor, the residual Jacobian,
the two-coefficient functional, all Sylvester determinants of \(M-I\),
the portable integer minors, the concrete SOS baseline certificate,
and the three-square integral identity. These checks passed.
An initial Jacobian assertion omitted reduction by \(a^5-2\);
after applying that necessary relation, the corrected check passed.
The updated checker, including its explicit baseline positivity check,
was rerun and passed. A standard-library document check passed final
newline, whitespace, control-character, math-delimiter, and four
local-link checks for this review.

The exact calculations certify identities and finite matrix inequalities.
The field-degree lower bound, coefficient-field sufficiency, and
dimension conclusion use the arguments above. No Lean verification,
project-wide tests, or CI inspection was performed. The prior literature
comparison beyond the stated classification is outside this proof review.
