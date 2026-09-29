# Independent review of the rational SOS-convex descent counterexample

Date: 2026-09-28. Status: the algebraic obstruction, convexity construction,
concrete certificate, and positive-constant perturbation consequence pass
independent adversarial review. Publication priority is not assessed here.

The [integrated result](rational-sos-convex-descent.md) proves that a
rational quartic can have a positive definite
rational Hessian Gram matrix, a unique minimum of zero, and a real SOS
representation, while having no SOS representation by rational
polynomials. The [concrete verification script](check_rational_sos_convex_descent.py)
uses the point

\[
 a=(\alpha,\alpha^2,\beta,\beta^2),\qquad
 \alpha^3=2,\quad\beta^3=5,
\]

with real cube roots. The
[algebraic construction](rational-sos-convex-descent-algebra.md), the
integrated note, and the concrete checker consistently use this point.
The final integrated proof was read in full.

## Field degree and the rational quadratic vanishing space

The degree-nine claim has a short exact proof. Suppose
\(\beta=A+B\alpha+C\alpha^2\) belongs to \(K=\mathbb Q(\alpha)\).
Because \(\beta\) has degree three, it generates \(K\). Thus its trace
and the trace of its square over \(\mathbb Q\) are zero. Since
\(\operatorname{Tr}(\alpha)=\operatorname{Tr}(\alpha^2)=0\), the first
equation gives \(A=0\). Expanding the square then gives
\(\operatorname{Tr}(\beta^2)=12BC\), so \(BC=0\). The remaining
possibilities require \(B^3=5/2\) or \(C^3=5/4\), neither a rational
cube. Hence \(\beta\notin K\). A reducible cubic over the real field
\(K\) would have a root in \(K\); for \(T^3-5\), that root would have
to be its unique real root. Therefore it is irreducible over \(K\),
and \([\mathbb Q(\alpha,\beta):\mathbb Q]=9\).

The nine products
\(\alpha^i\beta^j\), \(0\leq i,j\leq2\), consequently form a basis.
The evaluation of quadratics spans all nine: use

\[
                1,x,y,z,w,xz,xw,yz,yw.
\]

The rational space \(I_2\) of polynomials of degree at most two vanishing
at \(a\) therefore has dimension \(15-9=6\). A basis is

\[
\begin{array}{lll}
q_1=x^2-y,&q_2=xy-2,&q_3=y^2-2x,\\
q_4=z^2-w,&q_5=zw-5,&q_6=w^2-5z.
\end{array}
\]

Their independent quadratic leading monomials verify linear
independence directly. This step is essential: without the field-degree
argument, an evaluation in a nine-dimensional quotient algebra alone
would not establish the dimension of the vanishing space at the chosen
real point.

## The explicit obstruction and the preliminary dimension count

Let \(W\) be the rational span of all products \(q_iq_j\). Products from
different blocks have degree at most two in each block. Products from
the same block are independent of the other block. Thus the coefficient
functional

\[
                         f\longmapsto [yz^3]f
\]

vanishes on all of \(W\). Set

\[
 C(z,w)=z^3+w^3/5-3zw+5,\qquad h=yC(z,w).
\]

At \((\beta,\beta^2)\), \(C=0\), and

\[
 C_z=3z^2-3w=0,\qquad C_w=3w^2/5-3z=0.
\]

Hence \(h(a)=0\) and \(\nabla h(a)=0\), while \([yz^3]h=1\).
This proves \(h\notin W\) without relying on a computed nullspace.

The original dimension argument also passes. Rational quartics have
dimension 70. Evaluation of the value and four derivatives at \(a\)
gives at most \(5\cdot9=45\) rational linear equations, so their common
kernel has dimension at least 25. Meanwhile \(\dim W\leq21\), since
\(\dim I_2=6\). Independent exact calculations gave the sharp values
25 and 21. The explicit coefficient argument is stronger evidence for
the particular perturbation than these dimension counts alone.

There is no contradiction with membership in the square of the full
vanishing ideal. Indeed,

\[
       q_4q_6-q_5^2=-5C,\qquad
       h=-\frac y5(q_4q_6-q_5^2).
\]

The latter identity involves factors beyond the quadratic degree bound.
It does not place \(h\) in \(W\).

## Why a full positive definite Hessian Gram baseline exists

The proposed aggregation of exposing quadratics is valid. For a positive
real \(r\), the quadratic

\[
 E_r(X,Y)=r^2(X^2-Y)-r(XY-r^3)+(Y^2-r^3X)
\]

vanishes with zero gradient at \((r,r^2)\). In centered coordinates its
matrix is

\[
 \begin{pmatrix}r^2&-r/2\\-r/2&1\end{pmatrix}\succ0.
\]

Adding the two exposing quadratics gives a positive definite quadratic
part on all four coordinates. Rational approximations to their
coefficients preserve exact vanishing, because the rational quadrics
\(q_i\) themselves vanish. The resulting gradient at \(a\) can be made
arbitrarily small.

The four residuals \(q_1,q_2,q_4,q_5\) suffice for a nonsingular Jacobian:
each two-dimensional block has determinant \(3r^2\ne0\). Using all six
residuals also works. The full Hessian Gram construction from the
previously reviewed quartic lemma now applies in dimension four. At
the exact exposing quadratic, its constant block is of order
\(\varepsilon J^{\mathsf T}J\succ0\), its cross block is of order
\(\varepsilon\), and its quadratic block tends to a positive definite
matrix. The Schur complement is positive for small positive
\(\varepsilon\). After fixing that parameter, sufficiently close
rational approximation preserves positive definiteness.

This argument produces a rational SOS quartic \(G\in W\) vanishing at
\(a\), with a positive definite Hessian Gram matrix on the full basis
\((v,x\otimes v)\). Rational Gram matrices can be obtained by density
in the rational affine space of coefficient equations. Merely adding
separate block quartics would not justify this full-basis property;
adding the exposing quadratics before squaring is the relevant step.

Every rational quartic Hessian has some symmetric rational Gram matrix
on that basis, without a positivity requirement. Each biform monomial
is a product of two basis entries. Therefore, if \(M\succ0\) is a
rational Hessian Gram matrix for \(G\), and \(B\) represents the Hessian
of \(h\), then \(\lambda M+B\succ0\) for a sufficiently large rational
\(\lambda\). The polynomial \(F=\lambda G+h\) is strongly convex.
Since \(F(a)=0\) and \(\nabla F(a)=0\), it has unique global minimum
zero. Stationarity, rather than a pointwise domination estimate for
\(h\), is what makes this perturbation argument work.

## Review of the concrete certificate

The script removes the need to leave the last construction existential.
With denominator \(d=2^{31}\), it uses rational floors of the cube
roots of \(2,4,5,25\). The resulting approximants are

\[
 \frac{676414963}{536870912},\
 \frac{3408917801}{2147483648},\
 \frac{3672145383}{2147483648},\
 \frac{6279280279}{2147483648}.
\]

Writing these as \(a_1,b_1,a_2,b_2\), define

\[
 A=b_1q_1-a_1q_2+q_3+b_2q_4-a_2q_5+q_6.
\]

The concrete polynomial is

\[
 F=2^{40}\left(A^2+2^{-26}
                  (q_1^2+q_2^2+q_4^2+q_5^2)\right)+h.
\]

I inspected the complete script and reran it independently. The
following details were checked in the code:

- At its rational center, a quadratic is written as
  \(d_0+b^{\mathsf T}u+u^{\mathsf T}Tu\). The constant Hessian Gram
  block correctly includes \(4d_0T\), in addition to
  \(2bb^{\mathsf T}\).
- The tensor ordering in the cross and quadratic blocks agrees with
  the stated basis.
- The perturbation Gram construction groups all ordered matrix entries
  yielding the same monomial. Dividing by the group size accounts for
  off-diagonal entries correctly.
- An exact rational \(LDL^{\mathsf T}\) identity has all 20 diagonal
  pivots positive. A separate differentiated polynomial identity proves
  that the matrix actually represents the Hessian.
- The rational shift of the basis is invertible, so its positive
  definiteness is equivalent to a positive definite rational Gram
  matrix on the original full basis.

These checks passed. Positivity is proved by exact rational arithmetic,
not approximate eigenvalues or Hessian sampling.
An additional exact calculation verified the integrated note's metadata:
the largest numerator bit length is 103, the largest denominator bit
length is 86, and all 20 pivots are greater than one. A pivot bound alone
does not bound the smallest eigenvalue by one.

## Exclusion of rational SOS and existence of real SOS

Suppose \(F=\sum_j f_j^2\) with \(f_j\in\mathbb Q[x,y,z,w]\).
Every \(f_j\) has degree at most two: otherwise the nonzero highest
homogeneous squares could not cancel over the reals. Evaluating at the
real point \(a\) gives \(\sum_j f_j(a)^2=0\), so every \(f_j(a)=0\).
Thus every \(f_j\in I_2\), and \(F\in W\). But its \(yz^3\)
coefficient is one. This contradiction excludes all rational SOS
representations, including ones with more summands or positive rational
weights. It does not assume a particular Gram basis for the proposed
rational representation.

For completeness, the positive definite Hessian Gram proves a stronger
real SOS statement. Put \(u=x-a\) and let

\[
 \phi(u)=(u_i,\ u_i u_j:1\leq i\leq j\leq4),
\]

which has 14 entries. Taylor's formula gives

\[
 F(a+u)=\int_0^1(1-t)\,
              u^{\mathsf T}\nabla^2F(a+tu)u\,dt.
\]

Substitution in the Hessian Gram identity expresses its integrand as
\(\phi(u)^{\mathsf T}L_t^{\mathsf T}ML_t\phi(u)\), where \(L_t\)
maps the formal coordinates of \(\phi\) to
\((u,(a+tu)\otimes u)\). For every \(t\ne0\), this map is injective:
its first four coordinates recover the linear part, and then its
remaining coordinates recover all symmetric quadratic coordinates.
Consequently

\[
 R=\int_0^1(1-t)L_t^{\mathsf T}ML_t\,dt\succ0.
\]

Thus \(F(a+u)=\phi(u)^{\mathsf T}R\phi(u)\) is a real SOS. Its
irrational translation is precisely why this proof does not imply a
rational SOS.

## Every positive rational constant restores rational SOS

The preceding argument proves the additional claim requested for
review. It applies to any rational quartic having a positive definite
full Hessian Gram matrix and minimum zero at a point \(a\).
For every rational \(\eta>0\), the polynomial \(F+\eta\) has Gram
matrix \(\operatorname{diag}(\eta,R)\succ0\) on
\((1,\phi(x-a))\). Translation gives an invertible change to the full
ordinary monomial basis of degree at most two, so \(F+\eta\) has a
positive definite real Gram matrix there.

Its coefficient equations are rational affine equations. They have a
rational particular solution and a rational basis for their homogeneous
solution space. Rational points are dense in their real solution space,
and positive definiteness is open. Hence there is a positive definite
rational Gram matrix for \(F+\eta\). Rational \(LDL^{\mathsf T}\)
decomposition and a rational sum-of-squares decomposition of each
positive rational weight yield an SOS by rational polynomials.

The integrated note gives an equivalent direct proof by subtracting
\(\mu I\) from the translated positive definite Hessian Gram matrix.
Its Taylor contributions are
\(\mu\|u\|^2/2+\mu\|u\|^4/12\); both constants are correct.
The latter quartic supplies positive diagonal Gram entries for every
quadratic monomial, including each mixed monomial \(u_i u_j\).

For the displayed counterexample, rational SOS lower bounds therefore
have supremum zero, since every negative rational bound is feasible.
The bound zero is not attained over rational SOS certificates, and no
positive bound is possible because \(F(a)=0\). Real SOS certificates
do attain zero. This is an exact distinction between the two coefficient
fields; it asserts no complexity lower bound.

## Verification record and limits

Command actually run:

    python research-20260927/check_rational_sos_convex_descent.py

Result: passed. A separate inline Python calculation built the evaluation
and first-jet matrices independently, without importing the author's
script. It returned quadratic evaluation rank 9, \(\dim I_2=6\),
\(\dim W=21\), first-jet rank 45, and kernel dimension 25. It also
checked all five zero-jet identities for \(h\), the coefficient
obstruction, and the increase to rank 22 upon adjoining \(h\) to \(W\).
These checks passed.
Another inline Python command loaded the checker and verified the exact
coefficient-bit and pivot bounds reported above.
A standard-library document check passed final-newline, whitespace,
control-character, math-delimiter, and three local-link checks.

The field-degree proof is needed in addition to those quotient-algebra
computations. The existence argument for rational Gram matrices uses
ordinary exact linear algebra and openness; no polynomial bit bound for
the certificates of \(F+\eta\) is asserted. No Lean proof, project-wide
tests, or CI inspection was performed. The result's originality requires
a separate literature comparison.
