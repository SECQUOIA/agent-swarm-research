# A value-height bound for a compact intersection of few quadrics

Date: 2026-09-27. Status: a proved reduction using established algebraic
results, independently reviewed during the present research session. It is a
supporting lemma for the proposed Hessian-span result, not a claim of a new
general algorithm for optimization over few quadrics.

## Statement

Let rational quadratic polynomials \(g_1,\ldots,g_h,q\) and a positive
rational \(R^2\) describe

\[
 K=\{u\in\mathbb R^n:g_i(u)=0\ (1\le i\le h),\ \|u\|^2\le R^2\}.
\]

Suppose \(K\) is nonempty. Let \(L\ge2\) be its explicit binary input
length. No convexity or constraint qualification is needed for this lemma.
Then \(\alpha=\min_Kq\) is a root of a nonzero integer polynomial whose
degree and coefficient **bitsizes** are \(L^{O(h+1)}\). Thus, when
\(\alpha\ne0\),

\[
 |\alpha|\ge 2^{-L^{O(h+1)}}.
\]

The coefficient bound concerns logarithmic height, not the absolute
magnitudes of coefficients. The latter can be exponential in the displayed
bound. All hidden constants are absolute.

## Primary results used

1. Grigoriev and Pasechnik, *Polynomial-time computing over quadratic maps I:
   Sampling in real algebraic sets*, Computational Complexity 14 (2005),
   20–52, [inspected preprint v3](https://arxiv.org/pdf/cs/0403008v3).
   Lemma 5.2, pp. 28–29 of the PDF, gives the Hessian-pencil perturbation
   property below, including a statement for every sufficiently small
   **real** positive perturbation. Theorem 1.2 bounds sampling degrees and
   coefficient bitsizes. Theorem 1.5 announces an exact optimization bound
   but defers its proof; the argument here does not rely on that announcement.

2. Basu, Pollack and Roy, *Algorithms in Real Algebraic Geometry*, second
   edition, Theorem 14.16; also Basu, *Algorithms in real algebraic geometry:
   A survey*, [author version](https://www.math.purdue.edu/~sbasu/raag_survey2011_final-sep4-2014.pdf),
   Theorem 2.27. We use block quantifier elimination with one universal
   variable, \(O(h+1)\) existential variables and one free variable, including
   its coefficient-bitsize conclusion.

3. Kamminga and Rudolph, [arXiv:2411.03096v2](https://arxiv.org/pdf/2411.03096v2),
   Sections 6.2–6.3, Theorem 6.2, Remark 6.4, and equations (93), (98), give
   closely related reduced formulas. Their Section 7.1 optimizes through an
   additional quantified formula. We instead use the boundary of the
   attainable-value set. The derivation below is explicit and uses only the
   perturbation lemma from item 1 and quantifier elimination from item 2.

## Direct reduction to few variables

Introduce a real slack \(s\), put \(X=(u,s)\in\mathbb R^d\), where
\(d=n+1\), and use the quadratic outputs

\[
 Q_i(X)=g_i(u)\quad(1\le i\le h),\qquad
 Q_b(X)=\|X\|^2-R^2,\qquad Q_o(X)=q(u).
\]

There are \(k=h+2\) outputs. For a free real parameter \(a\), define

\[
 p_a(Y)=\sum_{i=1}^hY_i^2+Y_b^2+(Y_o-a)^2.
\]

The equation \(p_a(Q(X))=0\) is feasible exactly when \(a\in q(K)\).
Rational coefficient denominators may be retained until the final
polynomial formulas are cleared; this preserves the normalization of
\(Q_b\) and the meaning of \(a\). The total denominator bitsize remains
polynomial in \(L\).

Write
\(Q_j(X)=\tfrac12X^TH_jX+c_j^TX+d_j\). Fix any enumeration
\(j=1,\ldots,k\) of the outputs, and set

\[
 D_j=\operatorname{diag}(1^{j-1},\ldots,d^{j-1}),\qquad
 \widetilde Q_j(X,\varepsilon)
 =Q_j(X)+\frac{\varepsilon}{2}X^TD_jX.
\]

GP Lemma 5.2 states that there exists \(\varepsilon_0>0\) such that,
for every real \(0<\varepsilon<\varepsilon_0\) and every
\(w\in\mathbb R^k\setminus\{0\}\),

\[
 \operatorname{rank}\left(\sum_jw_j(H_j+\varepsilon D_j)\right)
 \ge d-k+1.
\]

After deleting one row, the justified lower bound is \(d-k\).
This distinction matters: the corresponding row-deleted claim in KR
Lemma 6.5 is off by one as written. GP's introductory explanation already
uses the appropriate bound \(d-k\).

Assume first \(d>k\), and put \(r=d-k\). Consider a nonempty compact
smooth level set

\[
 F_{a,\varepsilon}(X):=p_a(\widetilde Q(X,\varepsilon))=\zeta>0.
\]

The first coordinate attains a minimum on this level set. At such a point
the derivatives of \(F\) in coordinates \(2,\ldots,d\) vanish. With
\(Y=\widetilde Q(X,\varepsilon)\) and
\(w=\nabla p_a(Y)\), these equations are

\[
 \Phi(Y,\varepsilon,a)X=b(Y,a),
\]

where \(\Phi\) is the last \(d-1\) rows of
\(\sum_jw_j(H_j+\varepsilon D_j)\), and \(b\) is the last
\(d-1\) coordinates of \(-\sum_jw_jc_j\). Since
\(p_a(Y)=\zeta>0\), we have \(w\ne0\), and hence
\(\operatorname{rank}\Phi\ge r\).

Enumerate all row sets \(U\subseteq\{2,\ldots,d\}\) and column sets
\(W\subseteq\{1,\ldots,d\}\) with \(|U|=|W|=r\).
There are at most \(d^{2k-1}\) such choices. For each choice put

\[
 \Omega=\det\Phi_{UW},\qquad T=X_{W^c},\qquad
 X_W=\frac{\operatorname{adj}(\Phi_{UW})
              (b_U-\Phi_{U,W^c}T)}{\Omega}.
\]

Here \(T\) has exactly \(k\) coordinates. Define a piece formula
\(P_{UW}(a,\varepsilon,\zeta,Y,T)\) by imposing:

- \(\Omega\ne0\) and \(p_a(Y)=\zeta\);
- the remaining \(k-1\) row equations \(\Phi X=b\), after multiplying
  by \(\Omega\);
- the \(k\) equations \(Y_j=\widetilde Q_j(X,\varepsilon)\), after
  multiplying by \(\Omega^2\).

Every witness reconstructs a genuine point of the level set. Conversely,
at least one piece contains the coordinates of a critical point whenever
the stated compactness, smoothness and small-perturbation assumptions hold.
The selected minor need not have maximum size: remaining row consistency
is imposed explicitly. No rank-maximality minors are required.

## Compactness and the limit formula

The sphere output supplies a uniform bound. Since its added diagonal is
positive semidefinite, for \(\varepsilon>0\),

\[
 F_{a,\varepsilon}(X)=\zeta
 \quad\Longrightarrow\quad
 \|X\|^2\le R^2+\sqrt\zeta.
\]

It also makes \(F_{a,\varepsilon}\) coercive. These facts hold for every
real \(a\), with the same radius bound.

For each piece define

\[
 \Xi_{UW}(a):\quad
 \forall\gamma\;\Bigl[\gamma\le0\ \lor\
 \exists\varepsilon,\zeta,Y,T:
 0<\varepsilon<\gamma,\quad0<\zeta<\min\{1,\gamma\},\quad
 P_{UW}(a,\varepsilon,\zeta,Y,T)\Bigr].
\]

Then

\[
 a\in q(K)\quad\Longleftrightarrow\quad
 \bigvee_{U,W}\Xi_{UW}(a).
\]

To prove the forward implication, fix an original root \(X^*\). For any
small positive \(\gamma\), choose a sufficiently small generic
\(\varepsilon<\gamma\) with
\(F_{a,\varepsilon}(X^*)<\min\{1,\gamma\}\).
Choose \(\zeta\) between that value and \(\min\{1,\gamma\}\), avoiding
the finitely many critical values of \(F_{a,\varepsilon}\).
Coercivity and the intermediate value theorem, with \(\varepsilon\)
held fixed, give a nonempty level. The level is compact and smooth and
therefore yields a piece witness. Apply this construction with
\(\gamma=1,1/2,1/3,\ldots\). One of the finitely many pieces occurs
infinitely often. Its witnesses have both perturbations arbitrarily close
to zero, which is exactly \(\Xi_{UW}(a)\).

For the reverse implication, choose witnesses with \(\gamma\downarrow0\)
and reconstruct their \(X\) coordinates. The uniform radius bound gives
a convergent subsequence. Its limit satisfies \(p_a(Q(X))=0\) by
continuity. The reduced coordinates \(Y,T\) need not be bounded separately
for this argument, and \(\Omega\) is allowed to approach zero.

This also justifies exchanging an arbitrarily changing piece with a fixed
piece in the finite disjunction. No uniform lower bound on a determinant
and no uniform parameter threshold in \(a\) is needed.

## Degrees and coefficient bitsizes

Let \(\tau\) bound input coefficient bitsizes after a common positive
denominator is cleared. The diagonal entries have bitsize
\(O(k\log(d+1))\). Entries of \(\Phi\) have degree at most two in
\((Y,\varepsilon,a)\) and coefficient bitsize
\(O(\tau+k\log(d+1)+\log(k+1))\).

Expanding an \(r\)-row determinant bounds its degree by \(2r\) and
its coefficient bitsize by

\[
 O\bigl(r(\tau+k\log(d+1)+\log(k+1)+\log(r+1))\bigr).
\]

The adjugate has the same kind of bound. The reconstruction numerator,
row-consistency equations and quadratic substitution equations therefore
have degree \(O(d+1)\) and coefficient bitsize polynomial in \(L\).
Multiplication by \(\Omega\) or \(\Omega^2\) clears variable
denominators exactly under \(\Omega\ne0\). Rational input denominators
can subsequently be cleared with polynomial bitsize. This is an explicit
coefficient calculation, not an inference from arithmetic operation count.

Each \(\Xi_{UW}\) has one universal variable, \(2k+2\) existential
variables, one free variable and \(O(k)\) polynomial conditions. Block
quantifier elimination therefore yields output degrees and coefficient
bitsizes \(L^{O(k)}\). If \(d\le k\), apply existential elimination
directly to \(p_a(Q(X))=0\); the same bound follows.

Collect the output polynomials for all pieces, removing identically zero
polynomials. The union of the formulas defines the compact nonempty set
\(q(K)\). Its minimum \(\alpha\) must be a root of one collected
polynomial: otherwise every sign, and thus every formula, would be
constant on a neighborhood of \(\alpha\), contradicting its being the
minimum. Taking a union does not change the degree or height of an
individual polynomial; one must not multiply all output polynomials.

If \(\alpha\ne0\), divide its vanishing polynomial by the largest power
of the indeterminate that divides it. The reciprocal polynomial and the
Cauchy root bound give the stated positive separation bound.

## Verification and limitations

Two agents independently checked the compactness and subsequence
argument, the finite-piece step, the boundary argument, and the
coefficient calculation. A reviewer found the row-deletion rank correction;
it was independently rechecked against GP's original statement and
introductory explanation. The direct coercive-level argument also avoids
using KR Theorem 6.8's parameter-varying intermediate-value proof.

No computational test or Lean proof was run: the claims are symbolic
reductions, and small numerical examples would not verify the required
degree and height estimates. No project-wide checks or CI inspection were
performed. This note establishes the supporting value-height lemma; it
does not independently establish the broader exact-penalty application or
its novelty.
