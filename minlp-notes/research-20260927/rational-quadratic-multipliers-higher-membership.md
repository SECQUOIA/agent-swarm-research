# Multiplier order from the degree of quadratic ideal membership

Date: 2026-09-28. Status: complete proof passed
[fresh adversarial review](rational-quadratic-multipliers-higher-membership-review.md)
after one input-length clarification. Publication priority is unestablished.

This theorem extends the
[affine-membership multiplier theorem](rational-quadratic-perturbation-multipliers.md).
The target polynomials remain quadratic. The new parameter is the
degree of their coefficient polynomials in an ideal representation.

## Theorem

Let \(n,m,s,d\ge1\). Let \(q_1,\ldots,q_m\in\mathbb Q[X]\)
have degree at most two, and put \(F_0=\sum_iq_i^2\). A supplied
rational polynomial in their constant linear span is
\[
 G=X^{\mathsf T}HX+\ell^{\mathsf T}X+c,\qquad H\succ0.
                                                        \tag{1}
\]
Let \(R_1,\ldots,R_s\in\mathbb Q[X]\) have degree at most two,
with ideal representations
\[
 R_a=\sum_{i=1}^m u_{ai}(X)q_i(X),\qquad \deg u_{ai}\le d.
                                                        \tag{2}
\]
Let \(J\) be any supplied rational symmetric \(s\)-by-\(s\)
matrix. Write \(h=1+\|X\|^2\).

**Conclusion.** An explicit integer \(\lambda_*\) can
be constructed so that, for every rational \(\lambda\ge\lambda_*\),
\[
                       h^d(\lambda F_0-R^{\mathsf T}JR)
                              \in\Sigma\mathbb Q[X]^2.
                                                        \tag{3}
\]
The rational square factors have degree at most \(d+2\).
The construction and its output size are polynomial in the input
coefficient length and the explicitly expanded monomial count
\[
                         B=\binom{n+d}{d},
                                                        \tag{4}
\]
together with \(n,m,s,d\). No polynomial bound in binary-encoded
\(d\), or in \(n\) alone, is claimed.
The stated output bound uses the constructed scale \(\lambda_*\).
If a larger rational \(\lambda\) is prescribed externally, its bit
length is also counted as part of the input.

The representations (2) may be supplied or found by coefficient
matching through degree \(d+2\), within this expanded-size bound.
The polynomial \(G\), not merely the promise that it exists, is
supplied. Its constant span coordinates can also be recovered by
rational linear algebra.

## The initial Gram and the new polynomial entries

For \(\alpha\in\mathbb Z_{\ge0}^n\) with \(|\alpha|\le d\),
define
\[
 \kappa_\alpha=
       \frac{d!}{(d-|\alpha|)!\alpha_1!\cdots\alpha_n!}.
                                                        \tag{5}
\]
These are positive integers, and
\[
              h^d=\sum_{|\alpha|\le d}\kappa_\alpha X^{2\alpha}.
\]
The initial polynomial list is
\[
                    w=(X^\alpha q_i)_{|\alpha|\le d,\ 1\le i\le m}.
                                                        \tag{6}
\]
It has a positive diagonal Gram \(D_0\), with entries
\(\kappa_\alpha\), representing \(h^dF_0\). In particular,
\(D_0\succeq I\). No independence of the list is assumed.

Introduce a new \(n\)-entry block for every target \(a\) and
every monomial \(X^\alpha\) with \(|\alpha|\le d-1\):
\[
              b_{a,\alpha}=X^\alpha XR_a.
                                                        \tag{7}
\]
Its entries have level \(|\alpha|+1\). Initial entries have level
zero. Let \(v\) be the concatenation of \(w\) and all these blocks.
The total dimension is
\[
 t=m\binom{n+d}{d}
       +sn\binom{n+d-1}{d-1}.
                                                        \tag{8}
\]
This count permits repeated polynomial entries and even zero entries.

For \(\alpha=0\), the parent polynomial \(R_a\) has a known
coordinate vector in \(w\) by (2). For \(|\alpha|=e\ge1\),
choose any \(j\) with \(\alpha_j>0\). The parent
\(X^\alpha R_a\) is exactly the \(j\)-th entry of the earlier
block \(b_{a,\alpha-e_j}\), at level \(e\).
Thus every parent is represented either in the initial block or by
a single entry of the preceding level.

The polynomials \(X^\alpha G\) and \(X^\alpha X_jG\) are
represented entirely in \(w\), because
\(|\alpha|+1\le d\) and \(G\) is a constant linear combination
of the \(q_i\).

## Zero identities at every level

Write
\[
                  R_a=X^{\mathsf T}T_aX+r_a^{\mathsf T}X+s_a
                                                        \tag{9}
\]
with \(T_a\) symmetric. Fix \((a,\alpha)\), put
\(u=X^\alpha\), and abbreviate
\[
 p=uR_a,\quad g=uG,\quad z=uXR_a,\quad V=uXG.
\]
The following polynomial identity is exact:
\[
 z^{\mathsf T}Hz+p\ell^{\mathsf T}z+cp^2
                  -V^{\mathsf T}T_az-g r_a^{\mathsf T}z-s_agp=0.
                                                        \tag{10}
\]
Its first three terms equal \(u^2GR_a^2\), and its last three
terms equal their negative.

Using the representations just described, let \(Z_{a,\alpha}\)
be the symmetric rational matrix on \(v\) for the left side of
(10). Cross terms are split equally between the two transpose
blocks. Its block on the newly introduced entries
\(b_{a,\alpha}=z\) is exactly \(H\). Put
\[
             E_{a,\alpha}=Z_{a,\alpha}
                   -\operatorname{embed}_{b_{a,\alpha}}(H).
                                                        \tag{11}
\]
All entries of \(E_{a,\alpha}\) lie in the following pairs
of levels, where \(e=|\alpha|\):

| Term | Levels |
| --- | --- |
| \(cp^2\) | \((e,e)\) |
| \(-s_agp\) | \((0,e)\) and its transpose |
| \(p\ell^{\mathsf T}z\) | \((e,e+1)\) and its transpose |
| \(-V^{\mathsf T}T_az-gr_a^{\mathsf T}z\) | \((0,e+1)\) and its transpose |

For \(e=0\), the parent coordinate vector can have many entries,
but they all have level zero. Thus the same table remains valid.

Every matrix in (11) is explicitly rational. Let
\[
 K=\sum_{a,\alpha}\ \sum_{i,j}|(E_{a,\alpha})_{ij}|,
 \qquad
 \eta_0=\min\left\{1,\frac{\det H}{(\operatorname{tr}H)^{n-1}}\right\}.
                                                        \tag{12}
\]
Here \(\eta_0>0\), and both \(I\) and \(H\) are at least
\(\eta_0 I\). Define the rational number
\[
                         \rho=\frac{\eta_0}{2(1+K)}.
                                                        \tag{13}
\]
It satisfies \(0<\rho\le1/2\).

## A single positive Gram perturbation

Extend \(D_0\) by zeros on all new entries, and set
\[
 Q=D_0\oplus0+
       \sum_{a,\alpha}\rho^{2(|\alpha|+1)}Z_{a,\alpha}.
                                                        \tag{14}
\]
Every added term represents zero, so
\[
                            v^{\mathsf T}Qv=h^dF_0.
                                                        \tag{15}
\]
Let \(S\) be diagonal, with entry \(\rho^{-l}\) on every
coordinate of level \(l\). This is a rational invertible matrix.
The positive principal parts of \(SQS\) are the initial block
\(D_0\) and one copy of \(H\) on every new block.

The remaining entries come from the matrices \(E_{a,\alpha}\).
An entry joining levels \(l,l'\), contributed at step \(e\), is
multiplied by
\[
                             \rho^{2(e+1)-l-l'}.
\]
The four rows of the level table give exponents respectively
\[
                         2,\qquad e+2,\qquad1,\qquad e+1.
\]
All are at least one. Therefore the total absolute-entry norm of
the transformed correction is at most \(K\rho<\eta_0/2\).
This bounds its operator norm as well. Consequently
\[
                         SQS\succeq\frac{\eta_0}{2}I.
                                                        \tag{16}
\]
The largest level is \(d\), so undoing the congruence gives the
explicit rational bound
\[
                        Q\succeq
                    \frac{\eta_0\rho^{2d}}2 I.
                                                        \tag{17}
\]
This avoids successively applying determinant bounds to intermediate
Gram matrices, which could unnecessarily inflate the coefficient
heights.

## The target Gram and the final scale

For every monomial \(X^\beta\), \(|\beta|\le d\), let
\(V_\beta\) be an \(s\)-by-\(t\) rational matrix expressing
the vector \(X^\beta R\) in \(v\). For \(\beta=0\), use the
input membership coordinates in \(w\). For \(\beta\ne0\), choose
one occurrence of each target in (7), exactly as for the parents.

Then the rational symmetric matrix
\[
                    D_J=\sum_{|\beta|\le d}
                          \kappa_\beta V_\beta^{\mathsf T}JV_\beta
                                                        \tag{18}
\]
represents \(h^dR^{\mathsf T}JR\). Put
\[
 B_J=\max_i\sum_j|(D_J)_{ij}|,\qquad
 \lambda_*=\left\lceil
          \frac{2(B_J+1)}{\eta_0\rho^{2d}}
                            \right\rceil.
                                                        \tag{19}
\]
For every rational \(\lambda\ge\lambda_*\), symmetry and
(17) imply
\[
 \lambda Q-D_J\succeq I,\qquad
 h^d(\lambda F_0-R^{\mathsf T}JR)
                      =v^{\mathsf T}(\lambda Q-D_J)v.
                                                        \tag{20}
\]
This proves the SOS conclusion.

Because the final matrix is positive definite and \(v\) includes all
the \(q_i\), (20) also shows that the real zero set of
\(\lambda F_0-R^{\mathsf T}JR\) is exactly the common real zero
set of the \(q_i\). The converse uses (2), which makes all targets
vanish whenever the baseline factors vanish. No convexity assumption
is needed for this zero-set statement.

## Complexity and denominator conversion

The matrices in (10)--(14) can be formed by rational coefficient
operations in dimension (8), polynomial in the expanded count (4).
Each exponent in (14) is at most \(2d\). The rational number
\(\rho\) has polynomial bit length because \(K\) is the sum of
polynomially many explicitly bounded rational entries and the only
determinant in (12) has size \(n\). Thus \(\rho^{2d}\), all
entries of \(Q,D_J\), and the integer threshold (19) have
polynomial bit length in the stated expanded input model.

The multinomial coefficients (5) have bit length
\(O(d\log(n+1))\). Exact coefficient matching through degree
\(d+2\) has
\(\binom{n+d+2}{d+2}\le(n+d+2)^2B\) rows, so finding the
membership coordinates retains the same expanded polynomial bound.
Rational LDL and binary expansion of positive rational weights then
produce actual unweighted rational squares in polynomial time and
size, as in the affine-membership theorem.

If \(d\) is even, the SOS in (3) gives a rational-function SOS
with common denominator \(h^{d/2}\). If \(d\) is odd, first
multiply the SOS by \(h\), and use common denominator
\(h^{(d+1)/2}\). In both cases the denominator has no real zeros
and has degree \(2\lceil d/2\rceil\). Numerator degrees are at
most \(2\lceil d/2\rceil+2\). No minimal-denominator claim is made.

For \(d=0\), the targets lie in the constant span of the \(q_i\).
Direct domination of their fixed coefficient Gram gives
\(\lambda F_0-R^{\mathsf T}JR\) rational SOS without any
multiplier. That simpler case is separate from the positive-level
construction above.

If a rational positive definite full Hessian Gram for \(F_0\)
is additionally supplied, one can impose the independent Hessian
threshold from the affine-membership note and retain strict
SOS-convexity. This affects only the scale, not the multiplier degree.

## A relation requiring coefficient degree two

Higher-degree membership is not automatically affine under the
theorem's hypotheses. In \(\mathbb Q[x,y,z]\), take
\[
 q_1=G=x^2+y^2+z^2-1,\quad q_2=x^2,\quad
 q_3=xy-z,\quad q_4=yz-1,\qquad R=1.
\]
The required leading matrix is \(H=I_3\). Direct expansion gives
\[
\begin{aligned}
1={}&xq_1+(-x+y^2-1)q_2\\
   &+(-xy+xz-y)q_3+(-x^2-x-1)q_4.
\end{aligned}
\]
Thus coefficient degree two suffices.

For a polynomial \(P\) of degree at most three, let \([m]P\)
denote its coefficient of the monomial \(m\). Define
\[
 L(P)=[1]P+[x]P+[yz]P+[z^2]P+[xy^2]P+[xyz]P.
\]
This functional annihilates all sixteen products
\(mq_i\), with \(m\in\{1,x,y,z\}\), but \(L(1)=1\).
For example, the nontrivial cancellations include
\(L(q_1)=L(z^2-1)=0\),
\(L(xq_1)=L(xy^2-x)=0\),
\(L(yq_3)=L(xy^2-yz)=0\), and
\(L(zq_3)=L(xyz-z^2)=0\).
The remaining products either have both listed coefficients cancel
or contain no monomial seen by \(L\). Hence no affine ideal
representation of \(1\) exists, and the minimum coefficient degree
is exactly two.

This example has no common complex zero: \(x^2=0\) forces \(x=0\),
then \(xy-z=0\) forces \(z=0\), contradicting \(yz-1=0\).
A common zero is not assumed in the multiplier theorem.
The example proves a strict extension of its algebraic input class.
It does not prove that multiplier exponent two, or any positive
denominator degree, is necessary for the resulting penalty.

## Limits and verification status

The degree parameter is a degree bound for ideal-membership
coefficients in (2), not the degree of a general target polynomial.
Higher-degree negative squares would destroy nonnegativity at infinity
in general. The proof also requires a supplied positive definite
quadratic part in the constant factor span.

The construction uses only rational polynomial algebra and matrix
perturbation, without expanding a field of common zeros. The
[primary-source comparison and scope examples](rational-quadratic-multiplier-prior.md)
relate it to established order-unit and effective denominator
theorems; that comparison does not establish priority. Qualitative
domination for a sufficiently large scale is already elementary
under the hypotheses. The contribution here is the prescribed
multiplier order and explicit rational certificate construction.
The general ideal-membership problem, finding a suitable \(G\),
and numerical usefulness of the scale are outside its algorithmic claim.

Fresh review independently checked the complete proof, all level
exponents, coefficient heights, zero-set claim, and denominator
conversion. It required one clarification: if a larger scale is
prescribed externally, its bit length must count as input. The author
independently rechecked the correction, complete review, and checker.

The reviewer's targeted command was:

~~~text
python3 research-20260927/check_higher_membership_multiplier_review.py
~~~

It passed exact cases at membership degrees two and three, with Gram
dimensions thirty and fifty-four, nonhomogeneous targets, an
off-diagonal positive \(H\), negative constant \(c\), and indefinite
cross-target matrix \(J\). Every zero identity, the assembled scaled
error bound, two independent exact LDL positivity checks, and the
final polynomial identity passed. The supplied degrees were
deliberately nonminimal; these checks test valid high-degree
representations, not sharpness of the degree bound.

The author read the checker without rerunning the same computation.
Finite checks do not prove the universal theorem, its complexity,
or priority. No project-wide verification, CI inspection, or Lean
formalization was performed.

For the genuine degree-two example, a separate author-run inline
Python/SymPy coefficient-matching calculation found ranks
\(4,16,34\) at coefficient degrees zero, one, and two, with augmented
ranks \(5,17,34\). It produced the displayed identity and functional.
The fresh reviewer independently expanded the identity and checked
all sixteen functional cancellations by hand and exact arithmetic.
The identity and separating functional prove minimum degree two;
the exploratory rank calculation is additional finite evidence.

A final targeted inline Python document check passed for the two
multiplier notes, this theorem's review, and the prior comparison:
four Markdown files and eleven local links, with valid math
delimiters, whitespace, control characters, and final newlines.
