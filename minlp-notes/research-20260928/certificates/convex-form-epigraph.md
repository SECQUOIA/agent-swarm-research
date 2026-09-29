# Strictly curved polynomial norms have second-order cone epigraphs

Date: 2026-09-28. Status: proved as a consequence of existing representation
theorems and passed [independent adversarial review](convex-form-epigraph-review.md).
This is a useful representation result and a source correction, not a claim
of a new general representation theorem.

There are rational convex quartic forms that are not sums of polynomial
squares over the reals, but whose epigraphs have exact second-order cone
representations. An explicit example follows below. The representation is
existential: no bound on its size, rationality of its coefficients, or
polynomial-time construction is established here.

This distinction matters for MINLP reformulation. Failure of a polynomial
SOS certificate does not exclude an exact conic reformulation with auxiliary
variables. It also exposes a conflict with the unqualified claim in Theorem 3
of a set of 2025 lecture slides. The source comparison at the end identifies
the exact versions and what is contradicted.

## 1. Homogenizing a bounded lifted set

A second-order cone representable set is the projection of a finite system
of affine linear matrix inequalities with blocks of order at most two.
One-by-one blocks include ordinary affine inequalities.

**Lemma.** Let a bounded nonempty set \(K\subseteq\mathbb R^n\) have a
representation
\[
 K=\left\{x:\exists y,\quad
 A_0+\sum_i x_iA_i+\sum_j y_jB_j\succeq0\right\}.             \tag{1}
\]
The matrices may have a common block structure. Then the closed cone over
\(\{1\}\times K\), when \(K\) is closed, is represented by
\[
 u\ge0,\qquad
 uA_0+\sum_i x_iA_i+\sum_j y_jB_j\succeq0.                  \tag{2}
\]
The block sizes are unchanged, apart from the scalar block \(u\ge0\).

**Proof.** For \(u>0\), divide the matrix and the lift variables by \(u\).
This gives exactly \(x/u\in K\). At \(u=0\), suppose (2) holds with
some \(x\ne0\). Choose any feasible lift \((z,y^0)\) of a point
\(z\in K\). For every \(s\ge0\), the sum of its positive semidefinite
matrix and \(s\) times the matrix in (2) is a feasible lift of
\(z+sx\in K\), contradicting boundedness. Thus \(x=0\). Conversely,
\((u,x,y)=(0,0,0)\) is feasible. Finally, boundedness and closedness
show that the cone over \(\{1\}\times K\), with its origin added, is
closed. This proves the assertion without assuming that arbitrary
projections of closed cones are closed. \(\square\)

## 2. Passing from a polynomial norm ball to its epigraph

Let \(f\) be a homogeneous polynomial of even degree \(m\ge2\),
positive away from zero, and suppose that its unit sublevel set
\(K=\{x:f(x)\le1\}\) is convex. Its gauge is
\[
                         \gamma_K(x)=f(x)^{1/m}.          \tag{3}
\]
Indeed, \(x\in uK\) for \(u>0\) means exactly
\(f(x)\le u^m\). Positive definiteness makes \(K\) compact, so
Lemma 1 applies to any conic lift of \(K\).

If \(K\) is second-order cone representable, then so is
\(\operatorname{epi}\gamma_K\). Also, for an integer \(m\ge2\),
\(\{(u,t):u\ge0,\ t\ge u^m\}\) is second-order cone representable
as follows. Let \(k\) be a power of two with \(k\ge m\). Use a binary
geometric-mean tree on the \(k\) nonnegative leaves
\(t,1,\ldots,1,u,\ldots,u\), with \(m-1\) copies of one and
\(k-m\) copies of \(u\). Each parent \(s\ge0\) satisfies
\(s^2\le ab\) for its children \(a,b\), a rotated second-order cone
constraint, and the root is required to be at least \(u\). This is
equivalent to \(u^k\le t u^{k-m}\). For \(u>0\) cancellation gives
\(u^m\le t\); at \(u=0\) both descriptions allow exactly
\(t\ge0\). In the quartic case needed below, two simpler blocks are
\[
                    \begin{pmatrix}z&u\\u&1\end{pmatrix}\succeq0,
 \qquad
                    \begin{pmatrix}t&z\\z&1\end{pmatrix}\succeq0.
                                                               \tag{4}
\]
They give \(z\ge u^2\ge0\) and \(t\ge z^2\ge u^4\);
choosing \(z=u^2\) proves the converse.
Consequently
\[
 (x,t)\in\operatorname{epi}f
 \iff\exists u\ge0:\quad \gamma_K(x)\le u,\quad u^m\le t.
                                                               \tag{5}
\]
The implication uses monotonicity of the power on \([0,\infty)\).
Both the directions and the sign of \(u\) are essential.

**Theorem (consequence of prior representation theory).** Let \(f\) be a
positive definite convex form with positive definite Hessian at every
nonzero point. Its epigraph is second-order cone representable.

**Proof.** Euler's identity gives \(x\cdot\nabla f(x)=m\) on
\(f=1\), so that boundary is nonsingular. Its second fundamental
form is definite on every tangent space, because \(\nabla^2 f\) is
positive definite there. Thus \(K\) is compact, convex, and has smooth
boundary of strict positive curvature. Theorem 1.2 of Scheiderer,
[*Smooth hyperbolicity cones are second-order cone representable*,
arXiv:2509.17121v2](https://arxiv.org/pdf/2509.17121v2), gives a
second-order cone lift of \(K\). Lemma 1 and (5) finish the proof.
For degree four, use exactly (4). \(\square\)

The older Helton--Nie positive-curvature theorem already gives a
semidefinite version of this conclusion. The 2025 theorem sharpens the
allowed blocks to order two. Neither theorem, as used here, supplies a
small lift or rational lift data.

## 3. An explicit rational non-SOS quartic with such an epigraph

Use Saunderson's octonionic form in \(272=16\cdot17\) real variables:
\[
 q(x,y)=\|x\|^2\|y\|^2-
 \left|\sum_{i=1}^{17}\overline{x_i}y_i\right|^2
                +\tfrac14(\|x\|^2+\|y\|^2)^2,
 \qquad x,y\in\mathbb O^{17}.                              \tag{6}
\]
The standard octonion basis has integer multiplication constants, so
this is a rational quartic in real coordinates. Set
\[
 r^2=\|x\|^2+\|y\|^2,
 \qquad \boxed{f=q+\frac1{1016}r^4.}                       \tag{7}
\]

Saunderson's [Theorem 1.2 and Theorem 4.11](https://arxiv.org/pdf/2105.08432v2)
establish convexity of \(q\) and provide a symmetry-reduced SOS cone.
For its three evaluation points \(X_1,X_2,X_3\), the dual row
\(w=(252,3,-2)\) is nonnegative on that invariant SOS cone, and
\[
 (q(X_1),q(X_2),q(X_3))=(1/4,64,128),\quad
 (r^4(X_1),r^4(X_2),r^4(X_3))=(1,256,256).
\]
Both \(q\) and \(r^4\) are invariant under the same orthogonal group.
Thus an SOS for their sum would belong to that cone. But
\[
                          w(f)=-1+508/1016=-1/2<0.        \tag{8}
\]
Therefore \(f\) is not SOS even over \(\mathbb R\).
The exact matrix calculation supporting (8) is retained in the checker
linked below; it relies on the source's symmetry decomposition.

Since \(q\) is convex and
\[
 \nabla^2(r^4)=4r^2I+8XX^{\mathsf T},\qquad X=(x,y),
\]
we have
\[
                     \nabla^2f(X)\succeq\frac{r^2}{254}I
                         \quad(X\ne0).                  \tag{9}
\]
Moreover, (6) gives \(q\ge r^4/4\), by the octonionic
Cauchy--Schwarz inequality used in the source, so \(f\) is positive
definite. The theorem therefore applies: **the non-SOS rational
quartic (7) has an exact second-order cone representable epigraph.**
No rationality assertion about that lift follows from its rational
polynomial coefficients.

## 4. An unqualified statement in the slides cannot hold

The PDF of Scheiderer's talk *Spectrahedral shadows*, DDG 40,
6 August 2025, [printed slide 13](https://ddg40.sciencesconf.org/data/pages/Scheiderer_1.pdf),
states as Theorem 3 that the epigraph of every convex non-SOS form is
not a spectrahedral shadow. The author inspected both extracted text
and the rendered slide: the statement has no extra hypothesis or
visible qualification. The quartic (7), together with the proof above,
contradicts that universal assertion.

This is a conflict with the stated slide theorem. It is not a claim
that the published nonrepresentability results for general convex
semialgebraic sets are false, nor that all convex polynomial epigraphs
have conic representations. No associated proof of that slide theorem
was found or used. A missing hypothesis or an intended narrower
certificate format could explain the statement, but neither should be
silently supplied.

## 5. Verification and scope

The targeted command

~~~text
python research-20260928/certificates/check_convex_form_epigraph.py
~~~

checks the eight exact nonnegative entries obtained from Saunderson's
printed dual matrix, the negative perturbed evaluation, the scalar
power-lift identities, and the radial Hessian formula. It does not
verify the representation-theoretic decomposition or Scheiderer's
theorem; those are imported primary results. The homogenization and
curvature arguments are all-input mathematical proofs. No Lean,
project-wide verification, or CI inspection was used.

The [source directory](sources/) retains the three inspected PDFs,
with their hashes in [sources/README.md](sources/README.md). The independent
review reconstructed the homogenization and curvature arguments and
separately checked the invariant separation arithmetic. The author read
that review and rechecked the general integer-power construction it
recommended making explicit.

This observation identifies a possible exact conic capability for
homogeneous nonlinear constraints and clarifies a certificate boundary.
Turning the existence theorem into useful MINLP reformulations still
requires a constructive size bound and a practical method for finding
the lift. No computational solver advantage is claimed.
