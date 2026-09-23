# A local affine-pencil obstruction to excluding the \(H_3(\mathbb R)\) case

Status: Rigorous counterexample to a proposed proof route  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High

## Question

The symmetric-cone support-orbit theorem leaves one topological saturation
possibility besides spin factors: in contact-sphere dimension two, one
\(H_3(\mathbb R)_+\) factor can have support map
\(S^2\to\mathbb {RP}^2\).  Finite ray factors vanish on a suitable open
primal--polar rectangle by a Baire-category argument.  On that rectangle,
the rank-one side spans \(\mathbb S^3\), so the complementary rank-two
factor is the restriction of an affine symmetric \(3\times3\) pencil.

A proposed exclusion argued that determinant zero on a sphere patch made
this pencil globally singular and then invoked a common-kernel theorem.
That step is false.  The determinant can be the sphere quadric times a
nonzero linear factor, and the following pencil shows that every remaining
local requirement is compatible with this factorization.

## Explicit counterexample

For homogeneous coordinates \((t,x_1,x_2,x_3)\), define

\[
 L(t,x)=
 \begin{pmatrix}
 t+x_3&x_1&x_2\\
 x_1&t-x_3&0\\
 x_2&0&t-x_3
 \end{pmatrix}.                                           \tag{1}
\]

Direct expansion gives

\[
        \det L(t,x)
          =(t-x_3)\bigl(t^2-x_1^2-x_2^2-x_3^2\bigr).      \tag{2}
\]

Put \(t=1\) and take \(x\in S^2\) with \(x_3<1\).  The lower-right block
is \((1-x_3)I_2\succ0\), and its Schur complement is

\[
 1+x_3-\frac{x_1^2+x_2^2}{1-x_3}
 =1+x_3-\frac{1-x_3^2}{1-x_3}=0.                         \tag{3}
\]

Hence \(L(1,x)\succeq0\) has rank exactly two on the whole punctured sphere
\(S^2\setminus\{(0,0,1)\}\).  Its kernel line is

\[
 \ker L(1,x)=
 \operatorname{span}\left(
 1,-{x_1\over1-x_3},-{x_2\over1-x_3}\right).              \tag{4}
\]

The last two coordinates in (4) are stereographic coordinates.  Therefore
the projective kernel map is a local diffeomorphism at every point of the
punctured sphere, and in fact maps it diffeomorphically onto the affine
chart of \(\mathbb {RP}^2\) where the first homogeneous coordinate is
nonzero.  At the omitted north pole,

\[
                         L(1,0,0,1)=\operatorname{diag}(2,0,0), \tag{5}
\]

so the rank drops to one.

Thus an affine \(3\times3\) pencil can be PSD rank two on an arbitrary
open sphere patch, have locally invertible support/kernel map, and satisfy
\(\det L=\ell(t,x)(t^2-\|x\|^2)\), while failing constant rank only at a
point outside the patch.

## Why the Baire reduction remains local

Write the ray slack terms as \(a_j(x)b_j(z)\), and let
\(\gamma:P\to D\) be contact polarity.  Diagonal zero gives

\[
                         a_j(x)b_j(\gamma(x))=0.           \tag{6}
\]

For each of finitely many \(j\), the two closed zero sets in (6) cover the
contact sphere.  Iterating the Baire argument produces a nonempty open
patch \(U\) on which either \(a_j\) vanishes or
\(b_j\circ\gamma\) vanishes, separately for each \(j\).  Consequently all
ray terms vanish on \(U\times\gamma(U)\).

This does not make them vanish on \(U\times D\): for a given ray, the
second alternative may hold only on \(\gamma(U)\), while \(a_j\) remains
nonzero on \(U\).  The rank-two factor is therefore forced to be affine
only on the dual patch \(\gamma(U)\), not on the entire sphere.  Equations
(1)--(5) show exactly how the unavoidable rank drop can remain outside
that patch.

## Valid surviving conclusions

This counterexample does not construct a global \(H_3(\mathbb R)\)-plus-ray
slack factorization, so existence of the exceptional case remains open.
It only disproves the local affine-pencil/common-kernel exclusion.

Two stronger hypotheses do exclude the case:

- if every ray slack summand vanishes globally, the deck-related
  cross-contact has zero total slack, contradicting strict convexity;
- if all factor maps and contact polarity are real analytic, analytic
  unique continuation makes every ray summand vanish globally.

Under merely global \(C^1\) factors, the verified statement is instead that
the exception needs at least three active ray factors, by the Schwarz genus
of \(S^2\to\mathbb {RP}^2\).  These results are recorded in
[Saturated symmetric-cone factors induce idempotent-orbit
coverings](2026-09-04-symmetric-cone-support-orbit-rigidity.md).

