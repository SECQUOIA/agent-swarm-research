# Unbounded rational radial order for strongly SOS-convex quartics

Date: 2026-09-28. Status: the full proof passed an
[independent adversarial review](rational-radial-exponent-review.md),
with a further fresh reader checking the cone and quantifiers.
Literature priority remains unestablished.

There is no uniform exponent for the fixed rational multiplier
\((1+\|x\|^2)^N\), even for three-variable quartics with a rational
positive definite Hessian Gram certificate, Hessian at least \(I\),
and attained minimum zero. This can happen while an everywhere-positive
quadratic multiplier with short rational coefficients always suffices.

The obstruction is arithmetic. Every member of the family below is
already SOS over the reals, without a multiplier. Their exact rational
certificates behave differently.

## 1. The fixed example and the scaling family

Let \(F\in\mathbb Z[x,y,z]\) be
\[
\begin{aligned}
r&=(2-2xy,\ 2x^2-2yz,\ 2y^2-4z,\ 2z^2-x,\ 2xz-y),\\
A&=4r_0+5r_1+3r_2+9r_3,\\
F&=A^2+\sum_{i=0}^3r_i^2-r_4^2.
\end{aligned}
\]
Its [reviewed construction](ternary-rational-sos-convex-counterexample-review.md)
and [quadratic multiplier certificate](rational-denominator-certificate-frontier.md)
establish the following facts:

1. \(\nabla^2F\succeq I\), and the Hessian has a rational positive
   definite Gram matrix on the full basis \((v,x\otimes v)\).
2. Its unique zero is \(p=(a^{-1},a,a^{-3})\), where \(a^5=2\)
   and \(a>0\). The coordinate field has degree five.
3. The rational quadratic vanishing space at \(p\) is
   \(I_2(p)=\operatorname{span}_{\mathbb Q}\{r_0,\ldots,r_4\}\).
   The rational coefficient functional
   \[
   L(P)=2[z]P+4[y^2]P
   \]
   satisfies
   \[
   L\!\left(\left(\sum_{i=0}^4c_i r_i\right)^2\right)=4c_4^2,
   \qquad L(F)=-4.                                      \tag{1}
   \]
   The identity holds for arbitrary **real** coefficients \(c_i\).
4. For \(R=1+x^2+y^2+z^2\), there is a rational positive definite
   fifteen-by-fifteen matrix \(G\) and a rational cubic vector \(b\)
   with \(RF=b^{\mathsf T}Gb\). The matrix \(G\) is fixed,
   with entries having denominators at most eight.

For every positive integer \(t\), define
\[
f_t(X)=t^{-2}F(tX),\qquad X=(X_1,X_2,X_3).                 \tag{2}
\]

**Theorem.** The family (2) has all the following properties.

- Each \(f_t\) is a rational quartic in three variables with
  \(\nabla^2f_t\succeq I\), a rational positive definite full Hessian
  Gram certificate, and unique minimum zero at \(p/t\).
- For every fixed integer \(N\ge0\), all sufficiently large integers
  \(t\) satisfy
  \[
  (1+\|X\|^2)^Nf_t(X)\notin\Sigma\mathbb Q[X]^2.           \tag{3}
  \]
- In contrast,
  \[
  R_t(X)=1+t^2\|X\|^2
  \quad\text{satisfies}\quad
  R_t f_t\in\Sigma\mathbb Q[X]^2.                         \tag{4}
  \]
  It gives a rational-function SOS with common denominator \(R_t\),
  and this common-denominator degree two is minimal.
- The coefficients of \(f_t\), \(R_t\), and the certificate in (4)
  have bit length \(O(1+\log t)\). The Hessian at the minimizer
  is the same matrix \(\nabla^2F(p)\) for every \(t\).

The constants in the bit bound depend only on the displayed fixed
example and its fixed certificate.

## 2. A closed cone that retains the rational zero constraints

For any integer \(d\ge2\), define
\[
I_d(p)=\{q\in\mathbb Q[x,y,z]:\deg q\le d,\ q(p)=0\},
\qquad
V_d=\operatorname{span}_{\mathbb R}I_d(p).
\]
The space \(V_d\) is generally smaller than the space of all real
polynomials of degree at most \(d\) vanishing at \(p\).
It retains the equations at all algebraic conjugates of \(p\).
Replacing it with that larger space would destroy the argument.

Write
\[
C_d=\left\{\sum_j q_j^2:q_j\in V_d\right\}.
\]

**Lemma 1.** The cone \(C_d\) is closed in the coefficient space of
polynomials of degree at most \(2d\).

**Proof.** Choose a linearly independent real basis \(b_1,\ldots,b_s\)
of \(V_d\), and a closed Euclidean ball \(B\) with nonempty interior.
The moment matrix
\[
T=\int_B b(x)b(x)^{\mathsf T}\,dx
\]
is positive definite: a nonzero polynomial has positive integral of
its square over \(B\). Every element of \(C_d\) has the form
\(b^{\mathsf T}Qb\) with \(Q\succeq0\).

Suppose \(b^{\mathsf T}Q_kb\) converges coefficientwise.
The integrals \(\operatorname{tr}(Q_kT)\) are bounded. If
\(\lambda>0\) is the smallest eigenvalue of \(T\), then
\[
0\le\lambda\operatorname{tr}(Q_k)
 \le\operatorname{tr}(Q_kT).
\]
Thus the positive semidefinite matrices \(Q_k\) are bounded.
A convergent subsequence has a positive semidefinite limit, representing
the limiting polynomial. \(\square\)

This proof supplies the needed closedness. An arbitrary linear image
of a positive semidefinite cone need not be closed.

**Lemma 2.** \(F\notin C_d\) for every \(d\ge2\).

**Proof.** Suppose \(F=\sum_jq_j^2\) with \(q_j\in V_d\).
Because \(F\) has degree four, each \(q_j\) has degree at most two:
the highest-degree homogeneous real squares cannot cancel.

The finite-dimensional intersection identity
\[
V_d\cap\mathbb R[x,y,z]_{\le2}
=\operatorname{span}_{\mathbb R}I_2(p)                    \tag{5}
\]
follows from rational linear algebra. More explicitly, evaluating a
rational polynomial at \(p\) and expanding in the basis
\(1,a,\ldots,a^4\) defines a rational matrix. Its kernel is
\(I_d(p)\). Restricting its columns to degree at most two and
extending the coefficient field to \(\mathbb R\) commute.
By (5), each \(q_j\) is a real linear combination of the five
\(r_i\). Equation (1) gives \(L(F)\ge0\), contradicting
\(L(F)=-4\). \(\square\)

Merely knowing that \(F\) is not rational SOS would not suffice for
Lemma 2. The explicit functional obstruction on the real span of its
rational vanishing space is essential.

## 3. Proof of the radial lower bound

Fix \(N\ge0\) and set \(d=N+2\). As \(\varepsilon\downarrow0\),
\[
P_\varepsilon(x)=(1+\varepsilon\|x\|^2)^N F(x)
\longrightarrow F(x)
\]
coefficientwise. By Lemmas 1 and 2, the complement of \(C_d\)
contains a neighborhood of \(F\). Hence
\[
P_\varepsilon\notin C_d
\quad\text{for all sufficiently small positive }\varepsilon.       \tag{6}
\]

If \(P_\varepsilon\) were a rational polynomial SOS, its summands
would have degree at most \(N+2\). Its value at \(p\) is zero,
so every summand would vanish at \(p\). The summands would therefore
lie in \(I_d(p)\), contradicting (6).

Take \(\varepsilon=t^{-2}\). A rational SOS identity for the left
side of (3), followed by the rational substitution \(X=x/t\) and
multiplication by the rational square \(t^2\), would give a rational
SOS for \(P_{t^{-2}}\). This is impossible for all sufficiently large
integers \(t\), proving (3).

Failure at order \(N\) also implies failure at every smaller order,
because multiplication by \(R^{N-M}\), a rational SOS, preserves
rational SOS. Thus no fixed finite initial segment of the radial
hierarchy certifies every member of the family.

This closed-cone proof alone gives no explicit rate relating the
necessary order to \(\log t\), or an explicit threshold in (3).
A [subsequent recursive separator and height analysis](rational-radial-height-lower-bound.md)
does obtain
\(\nu(t)=\Omega(\log\log t/\log\log\log t)\) for all sufficiently
large integer \(t\). That quantitative conclusion uses additional
arguments, not closedness alone.

## 4. Strict convexity and short adaptive certificates survive

Differentiating (2) gives
\[
\nabla^2f_t(X)=\nabla^2F(tX)\succeq I,\qquad
\nabla^2f_t(p/t)=\nabla^2F(p).
\]
The rational change from the Hessian Gram vector
\((v,X\otimes v)\) to \((v,tX\otimes v)\) is invertible.
Congruence therefore preserves the positive definite rational Gram
certificate. Uniqueness of the minimum and the degree-five coordinate
field are preserved by the nonzero rational scaling.

The adaptive multiplier identity is explicit:
\[
R_t(X)f_t(X)
=\bigl(b(tX)/t\bigr)^{\mathsf T}G\bigl(b(tX)/t\bigr).       \tag{7}
\]
Its matrix is unchanged, and its polynomial vector still has degree at
most three. All coefficients in (7) have \(O(1+\log t)\) bit
length. There are a fixed number of coefficients; choosing any one
rational square-factor expansion of the fixed matrix \(G\) gives
the same total certificate-length bound. Conversely,
\([X_1^4]f_t=104t^2\), so the input length itself is
\(\Omega(1+\log t)\).
Multiplying (7) by \(R_t\) and dividing by \(R_t^2\)
gives rational-function squares with common denominator \(R_t\).
The numerator degrees are at most four. The denominator is at least
one everywhere.

No \(f_t\) is rational polynomial SOS, because substituting \(X=x/t\)
would make \(F\) rational SOS. The
[affine-denominator cancellation lemma](rational-denominator-certificate-frontier.md)
therefore rules out a common denominator of degree zero or one.

The [rational sphere corollary](rational-denominator-certificate-frontier.md)
also proves that each individual \(f_t\) has some finite fixed-radial
order: the leading form is positive definite and its sole zero is
nondegenerate. Thus the least such order is finite for each \(t\)
and tends to infinity as \(t\) runs through the positive integers.
The adaptive certificate (7) alone would not justify this finiteness
claim; it uses the separate prior-theory corollary.

## 5. Finite fixed menus and practical meaning

The same proof gives a slightly broader consequence. Let
\(h_1,\ldots,h_s\in\mathbb Q[X]\) be a fixed finite list with
\(h_j(0)>0\). Then, for all sufficiently large integers \(t\),
none of \(h_jf_t\) is rational SOS.

For one \(h_j\), change variables back and let \(t\to\infty\):
\[
h_j(x/t)F(x)\longrightarrow h_j(0)F(x).
\]
Choose a single degree bound covering these products. Their rational
SOS summands, if they existed, would belong to the corresponding
\(I_d(p)\). The limiting positive multiple of \(F\) is outside
the closed cone \(C_d\). A finite list allows taking the maximum
of the individual thresholds. In particular this applies to any
finite predetermined menu of everywhere-positive rational
polynomial multipliers.

This establishes a capability separation for exact certification.
Choosing a denominator adapted to the coordinates can keep both its
degree and the size of the certificate bounded by a constant times the
input length. Insisting on bounded powers of one fixed radial
polynomial cannot do so for this family. The argument does not show
that numerical real-SOS optimization needs high order: the real SOS
problem is feasible already at order zero. It also does not show
that finding the adaptive denominator is difficult; the scaling
parameter makes it explicit here.

The constant Hessian at the minimizer rules out explaining this
particular order obstruction by worsening local Hessian conditioning.
It does not supply a global upper Hessian bound or prove numerical
stability of a certificate-search implementation.

## 6. Prior results, verification, and remaining questions

The scaling-and-closedness method is classical.
Reznick's Theorem 1 scales a putative universal multiplier toward a
monomial and uses closedness and linear-factor cancellation to
contradict a real polynomial SOS obstruction.
His Corollary 2 excludes a finite menu for general nonnegative forms.
[Primary paper, Section 3](https://arxiv.org/pdf/math/0306163).
The degree-one cancellation used in the companion note is also
explicitly discussed there and credited to earlier work.

Those results do not directly establish the theorem here: every
\(f_t\) is real SOS and globally strongly SOS-convex.
The additional ingredient is the closed cone built from the
**rational** vanishing space of an algebraic minimizer, together with
the coefficient functional (1). It makes the same kind of limiting
argument detect a rational certificate obstruction that disappears
over the reals. The simultaneous small adaptive certificate and
unchanged local Hessian follow from the explicit example.

Variable SOS denominators and the resulting reductions in certificate
size are already advocated by Kaltofen, Li, Yang, and Zhi.
[Primary algorithm paper](https://www.sciencedirect.com/science/article/pii/S0747717111001143).
The present theorem supplies a strong convex arithmetic example with an
unbounded fixed-radial order and a degree-two adaptive denominator.
No search result establishes priority for that combination.

The original polynomial, its strict Hessian certificate, its vanishing
space, and its adaptive Gram certificate have exact independent checks.
This note's universal scaling argument is a proof using
finite-dimensional closedness; a finite numerical experiment cannot
verify its quantifier over every \(N\). The separate height note
proves an explicit order lower bound in terms of input length.
No Lean proof, project-wide test, or CI result is claimed here.

A targeted inline Python document check, run as
\(\texttt{python3 -}\), passed for this note, the denominator
frontier, and their two fresh reviews: balanced math delimiters,
trailing whitespace, control characters, final newlines, and all
fourteen local file links. This checks document integrity, not the
mathematical theorem.

The main remaining quantitative question is to sharpen the lower bound
on the least radial order and obtain useful upper bounds in terms of
coefficient height and the relevant arithmetic separation margin.
A separate algorithmic question is how
to select short adaptive positive denominators without knowing the
change of coordinates in advance.
