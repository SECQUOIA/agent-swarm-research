# Root audit of the strongly convex quartic with an irrational zero

Date: 2026-09-28. This is an additional mathematical check of the compact
construction in [the main note](convex-quartic-irrational-zero.md).
The root contributed a different, larger three-square construction during
development, then independently reconstructed the compact example and its
global Hessian bound. This record supplements the separately staffed fresh
review; it is not a claim of independent authorship or publication priority.

## The polynomial

Put

\[
 q_1=x^2-y,\qquad q_2=y^2-2x,
\]

\[
 A=12599x^2-10000xy+7937y^2-15874x-12599y+20000,
 \qquad F=A^2+10000(q_1^2+q_2^2).
\]

Then \(F\in\mathbb Z[x,y]\) has degree four and is nonnegative.
For \(a=\sqrt[3]{2}\), its value at \(p=(a,a^2)\) is zero. One way
to check this is to set

\[
 q_3=(x-y)^2-2x-y+4,
 \qquad A=7599q_1+2937q_2+5000q_3.
\]

All three \(q_i\) vanish at \(p\). Conversely, \(F=0\) forces
\(q_1=q_2=0\), hence \(y=x^2\) and \(x(x^3-2)=0\).
The alternative \((x,y)=(0,0)\) has \(A=20000\ne0\).
Thus the zero set is exactly \(\{(a,a^2)\}\), with no rational point.

## A bound valid everywhere

Let \(c_1=7599/5000\), \(c_2=2937/5000\), and
\(\epsilon=1/2500\). Write \(u=(u_1,u_2)= (x,y)-p\) and

\[
 H=\begin{pmatrix}c_1+1&-1\\-1&c_2+1\end{pmatrix},
 \quad g_1=(2a,-1)^T,\quad g_2=(-2,2a^2)^T,
\]

\[
 e_1=c_1-(2a-1),\quad e_2=c_2-(a^2-1),
 \qquad \ell=e_1g_1+e_2g_2.
\]

The translated polynomial \(f=F/5000^2\) has homogeneous parts

\[
 f_2=(\ell^Tu)^2+\epsilon[(g_1^Tu)^2+(g_2^Tu)^2],
\]

\[
 f_3=2(\ell^Tu)(u^THu)
       +2\epsilon[(g_1^Tu)u_1^2+(g_2^Tu)u_2^2],
\]

\[
 f_4=(u^THu)^2+\epsilon(u_1^4+u_2^4).
\]

There are no constant or linear terms. The following estimates use only
the rational isolator \(1.259921<a<1.259922\), whose cubed endpoints
lie strictly on either side of 2:

- \(H\succeq\tfrac12I\) and \(\|H\|_2<5\), by its row sums
  and diagonal dominance.
- \(\|g_1\|_2<3\), \(\|g_2\|_2<4\), and the matrix
  \(G=[g_1\ g_2]\) has determinant 6 and squared Frobenius norm
  less than 25. Hence \(GG^T\succeq I\): its smaller eigenvalue
  is at least \(36/25>1\).
- The isolator gives \(|e_1|\le44/10^6\) and
  \(|e_2|<4/10^6\). Consequently
  \(\|\ell\|_2\le3|e_1|+4|e_2|<1/5000\).

It follows that \(\nabla^2 f_2\succeq2\epsilon I\).
For a symmetric matrix \(B\) and vector \(b\), direct differentiation
gives

\[
 \bigl\|\nabla^2[2(b^Tu)(u^TBu)]\bigr\|_2
       \le12\|b\|_2\|B\|_2\|u\|_2.
\]

Applying this to the three cubic terms, and conservatively bounding both
\(\|g_i\|_2\) by 4, gives

\[
 \|\nabla^2 f_3\|_2
 \le\left(\frac{60}{5000}+\frac{96}{2500}\right)\|u\|_2
 =\frac{63}{1250}\|u\|_2.
\]

Finally,

\[
 \nabla^2(u^THu)^2
 =8(Hu)(Hu)^T+4(u^THu)H\succeq\|u\|_2^2I.
\]

The other quartic terms are convex. Completing the scalar square in
\(r=\|u\|_2\) proves

\[
 \nabla^2f\succeq
 \left[\frac2{2500}-\frac{63}{1250}r+r^2\right]I
 \succeq\frac{1031}{6250000}I.
\]

Multiplication by \(5000^2\) gives the claimed global bound

\[
                         \nabla^2F(x,y)\succeq4124I.
\]

No bounded-domain restriction or numerical sampling is used in this
convexity proof. Strong convexity also independently guarantees uniqueness
of the zero already identified above.

## Source and verification checks

The root directly read Table 1 and Appendix C of
[Slot--Steurer--Wiedmer, *Hesse's Redemption*, November 5, 2025 version](https://arxiv.org/pdf/2511.03440).
Their exact decision problem asks whether \(f\le0\) on a rational
polyhedron. Table 1 marks existence of a compact rational witness for
convex quartics as unknown. Appendix C gives a univariate convex sextic
with an irrational zero and proves rationality of a univariate convex
quartic minimizer when its minimum is rational. The example here has two
variables and rational minimum zero, so it does not conflict with that
univariate theorem. It refutes the general rational-witness possibility
stated in that version. It does not prove any complexity lower bound for
exact decision or exclude algebraic certificates.

An inline `python -` command using `fractions.Fraction` and SymPy checked
the isolator by exact cubing, all displayed numerical inequalities, the
integer identity for \(A\), the zero and gradient modulo \(a^3-2\), the
full translated homogeneous decomposition, \(\det G=6\), and the exact
square-completion constant. All checks passed. The first run used a strict
endpoint comparison where the rational upper bound equals \(44/10^6\);
changing that comparison to `<=` fixed the checker. The proof and its
strict interior-root estimate were unchanged.

The calculation establishes the identities and rational inequalities used
by the proof. The differentiation and matrix-norm arguments above supply
the universal quantifiers; finite examples alone would not prove global
convexity. No project-wide check or CI inspection was performed. Later
literature and equivalent examples remain part of the separate novelty
audit.

## A second exact certificate and formal coverage

A different investigator subsequently found a
[rational SOS certificate](convex-quartic-rational-sos.md) proving
\(\nabla^2F\succeq4096I\), a slightly weaker bound. It uses a rational
translation and scaling, a six-dimensional integer Gram matrix, and a
strictly diagonally dominant rational congruence. It contains no algebraic
root in its coefficients.

The root independently checked its Gram identity using only Python's
fractions.Fraction. The directional Hessian was derived directly from
the three squared polynomials, independently of the author's symbolic
differentiator. The identity was checked on the Cartesian grid
\(X,Y\in\{-1,0,1\}\) for directions \((1,0),(0,1),(1,1)\), giving
27 exact equalities. This is an interpolation certificate, rather than
numerical sampling: each coefficient of the directional quadratic has
degree at most two in each of \(X,Y\), so the grid determines it
uniquely, and the three directions determine a symmetric two-by-two
quadratic form. Independent rational elimination also found all six Schur
pivots of the Gram matrix positive. Thus the root's check proves the
global matrix identity and positivity without SymPy, a numerical solver,
or a cube-root approximation. The author's separate check verifies the
more concise 21-square diagonal-dominance identity as well.

The [Lean file](../formal/ConvexQuarticIrrationalZero.lean) now verifies
the polynomial's nonnegativity, exact real zero and nonpositive sets,
existence and uniqueness of the zero, and the absence of rational
nonpositive points. The root read its declarations and proofs against the
mathematical formula. A separate
[correspondence review](convex-quartic-lean-correspondence-review.md)
checked the same mapping and successful-build source hash.
The [verification record](convex-quartic-lean-verification.md) lists the
targeted command and reported axioms. The subsequent Lean extension also
verifies the rational 21-square identity and the lower bound \(4096I\)
for the actual second directional derivative of \(F\). The root read
the formal first- and second-derivative chain and the SOS identity; the
certificate author separately checked all coefficients and the source
hash. A final extension verifies the functional ConvexOn predicate on
\(\mathbb R^2\), using differentiability along each affine line and
Mathlib's nonnegative-second-derivative criterion. The root read that
bridge and its endpoint interpolation independently; the correspondence
review checks the frozen final source. The analytic constant \(4124\)
and named strong-convexity packaging remain outside formal coverage.
