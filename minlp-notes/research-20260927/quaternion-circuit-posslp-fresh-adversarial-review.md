# Independent review of the rational quaternion sign reduction

Date: 2026-09-28. Reviewer: `quaternion_sign_fresh_audit`.

**Verdict: the stated circuit-sign theorem passes this review.** I found
no gap in the quaternion identities, micro-signal construction, uniform
error induction, treatment of cancellation, or polynomial-size
many-one reductions. This is a proof review, not a publication-priority
finding. The separate quartic realization is outside this review.

I did not develop the construction. I reviewed the frozen
[proof draft](quaternion-circuit-posslp-reduction.md) with SHA-256
`e9d0f6955777010090d4e1b1a9046c9d95b81470b1ba8a7bc8cb234e55bb42c5`.
Another reviewer was independently checking the same compiler. I
completed the mathematical checks below before receiving that
reviewer's conclusions.

## 1. Exact identities and orientation

The multiplication convention is internally consistent. Conjugation by
\(c=(1,1,1,1)/2\) maps vector coordinates to \((z,x,y)\),
so it sends \(e_1\) to \(e_2\), \(e_2\) to \(e_3\), and
\(e_3\) to \(e_1\). Thus the leading cross product used by
the multiplication macro has the required positive sign.

Expanding \(qT(q)\) gives vector coordinates
\((2wx,2xz,-2xy)\). Its scalar coordinate is
\(w^2-x^2+y^2+z^2=1-2x^2\) on the unit sphere.
The unit-norm hypothesis is essential for this last equality and is
satisfied at every circuit gate. In particular, the exact identity
\(P(q)=\mathbf 1\) when \(x=0\) is valid even if the transverse
coordinates are nonzero.

The commutator identity follows from
\[
(qr-rq)\bar q\bar r=[q,r]-\mathbf 1,
\qquad qr-rq=2(0,v\times u).
\]
Multiplicativity of the quaternion norm proves (7). For nonnegative
scalar parts,
\(\|q-\mathbf 1\|\le2\|v\|\), and similarly for \(r\).
Applying the triangle inequality to
\(\bar q\bar r-\mathbf 1\) proves the factor 4 in (8).
No asymptotic expansion is substituted for either exact identity.

A separate narrow symbolic audit by `quaternion_identity_check`
also verified these identities and the orientation. As an additional
check, for pure-axis unit inputs \(q=(w,x,0,0)\) and
\(r=(s,a,0,0)\), the exact selected coordinate is
\[
 M(q,r)_x=4wsxa(1-2x^2a^2).
\]
It has leading coefficient \(+4\), as required. This special-case
identity supplements, but does not replace, the uniform error proof.

## 2. The positive micro-signal

Under (10), the transverse bound gives
\[
2|yz|\le4096x^4,\qquad \|v\|\le2x.
\]
Consequently (8) gives
\[
 |U_x-2x^2|\le4096x^4+64x^3\le65x^3,
\]
because \(x\le2^{-16}\). The stated weaker bounds
\(x^2\le U_x\le3x^2\) follow. Equation (7) gives both
\(\|\operatorname{vec}U\|\le8x^2\) and
\(U_w\ge1-8x^2>1/2\).

Applying the exact projection formula therefore gives
\(x^2\le x'\le6x^2\). The transverse norm is at most
\(48x^4\le64(x')^2\). Also
\(P(U)_w=1-2U_x^2>0\) and \(6x^2\le x\), so all
parts of the induction hypothesis persist.

The fixed generator has selected coordinate
\[
x_0=\frac{2^{-19}}{1+2^{-40}}<2^{-19}
\]
and zero transverse coordinates. Iterating the upper recurrence proves
\[
0<x_j\le(6x_0)^{2^j}/6<2^{-16\cdot2^j}.
\]
The lower recurrence proves strict positivity at every finite stage.
Thus the construction does not merely produce a small approximation
whose sign would require a separate decision.

## 3. Uniform bounds and cancellation

I independently recovered the error coefficients in the draft:

| Operation | Error coefficient relative to the stated next order |
| --- | --- |
| \(P\) | \(2B+16B^2\le18B^2\) |
| \(A\) | \(4B+108B^2+32B^3\le144B^3\) |
| \(M\) | \(12B^2+128B^3+256B^4\le396B^4\) |

For addition, the scalar-part errors contribute at most
\(16B^3\delta^{3d}\), while the cross product contributes at
most \(4B^2\delta^{2d}\). Since \(d\ge1\), both can be
bounded using \(\delta^{d+1}\). Also
\(\|\operatorname{vec}(qr)\|\le5B\delta^d\); applying (9)
then gives the displayed addition bound.

For multiplication, the two inherited leading/error cross terms and
the error/error cross term together contribute at most
\(3B^2\delta^{a+b+1}\). The commutator remainder contributes at
most \(64B^3\delta^{a+b+1}\). Projection then adds at most
\(256B^4\delta^{2(a+b)}\), which is bounded using
\(\delta^{a+b+1}\) since \(a+b\ge2\).

All leading coefficients, including \(4CD\), and all displayed
errors fit \(B'=2^{20}B^4\) for \(B\ge1\).
These are absolute bounds. They neither divide by a leading coefficient
nor require it to be nonzero. An arithmetic gate whose exact value is
zero can therefore still be used as an input to subsequent gates.
Subtraction and arbitrarily severe cancellation do not invalidate the
induction.

Positivity of scalar parts is also justified without assuming the
conclusion. Write \(h=2B\delta\le2^{-29}\). For the product of
two input signals, its scalar part is at least \(1-3h^2>0\).
For a commutator, (7) gives scalar part at least
\(1-2h^2>0\). The vectors supplied to (9) are below \(1/2\),
and the final projection has scalar part \(1-2x^2>0\).
Inversion preserves the input scalar part.

## 4. Homogenization and the global scale

The numerator and denominator leading coefficients have the same
factor 4 at an integer multiplication gate. At an addition or
subtraction gate, the two multiplication macros give factor 4, and
the final addition gives factor 2. The denominator's extra projection
gives exactly the same factor 8. Thus
\[
C_i=D_iV_i,\qquad D_i\in\mathbb Z_{>0}
\]
is preserved. The two numerator terms have the same order, so addition
is invoked within its proved hypotheses.

With \(B_0=128\), the recurrence for \(b_j=\log_2B_j\) is
\(b_j=20+4b_{j-1}\), \(b_0=7\). Hence
\[
b_j=(41\cdot4^j-20)/3<14\cdot4^j.
\]
Choosing \(r=2T+2\) gives
\(16\cdot2^r=64\cdot4^T\), and
\[
64\cdot4^T>30+b_T
\]
for every \(T\ge0\). The chosen \(\delta\) therefore meets
the smallness hypothesis for every compiler operation. An earlier
signal may always be assigned a larger bound, so a shared circuit with
unequal branch depths causes no induction problem.

The final integer is \(W=2V-1\ne0\). Since its numerator
coefficient is the nonzero integer \(D W\), its absolute value is
at least one. The final error is below
\(\tfrac12\delta^d\), proving both the selected coordinate's
nonvanishing and its required sign.

## 5. Size, upper reduction, and scope

The compiler only needs its own topology and operation count \(T\)
before choosing the initial signal. It never needs the expanded values
of \(B_T\), \(C_i\), \(D_i\), \(\delta\), or any output
rational coordinate. The number of micro-signal iterations is linear
in \(T\); every macro contains a constant number of quaternion
operations. Reuse is permitted throughout. These facts give a
polynomial-size shared circuit over the stated fixed rational
generators.

For the upper reduction, a common positive denominator per quaternion
gate is sufficient. Products multiply positive denominators and use
integer bilinear numerator formulas. Inversion is conjugation because
the quaternion is unit; it negates three numerators and preserves the
positive denominator. Fixed generator integers have constant-size
straight-line programs over \(0,1,+,-,\times\). The selected
numerator therefore gives one PosSLP instance in polynomial time.

The resulting completeness statement is for coordinate positivity in
a shared circuit. The lower reduction produces nonzero selected
coordinates, so it also gives hardness under that promise. This does
not establish hardness of testing group identity, a lower bound for
explicitly expanded words, or rationality of a minimizer after an
objective perturbation. The quartic-coordinate application additionally
requires the separately reviewed realization theorem.

## 6. Verification record and remaining limits

This review reconstructs the estimates for arbitrary circuit size; a
finite numerical experiment is not the basis of the verdict. The narrow
symbolic audit checks exact identities only and does not establish the
global induction or complexity claims.

Targeted commands actually run by this reviewer:

- An inline `python3 -` check passed the recurrence formula, strict
  scale inequality, and exponent identity for every integer
  \(T=0,\ldots,256\). This is a finite arithmetic check; the
  general argument is in Section 4. The same command checked this
  review's two local links, paired math delimiters, final newline,
  whitespace, and control characters.
- `git diff --check -- research-20260927/quaternion-circuit-posslp-fresh-adversarial-review.md`
  returned no output. The direct text checks above also cover a newly
  created file before it is tracked by Git.

The narrow identity reviewer separately ran ephemeral Python/SymPy
expansions, reductions modulo the unit-norm equations, and a rational
parametrization limit. I inspected its reported identities and
independently derived the identities in Section 1; I did not rerun that
reviewer's command. No project-wide verification or CI inspection was
performed.

The existing [primary-source comparison](quaternion-circuit-posslp-prior.md)
identifies relevant matrix-circuit and Solovay--Kitaev work. I have not
independently completed that literature audit. This proof pass therefore
establishes neither novelty nor publishability, and it supplies no
practical solver speedup or polynomial bound on expanded rational
output lengths.
