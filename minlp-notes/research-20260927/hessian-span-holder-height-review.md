# Hessian-span Hölder bounds with controlled constants

Date: 2026-09-27. Status: co-developed theorem argument; a separate
[independent adversarial review](hessian-span-holder-height-adversary.md)
found no unresolved proof gap after an active-row correction. Publication
priority remains unestablished. The argument below supplies an encoding
bound for the constant in
[the qualitative Hölder theorem](hessian-span-holder-geometry.md).
It depends on the common-field degree and coordinate-height theorem in
[the algebraic-witness note](algebraic-witness-recovery.md) and on the
coefficient-sensitive quantifier-elimination theorem already used in
[the Hessian-span value proof](hessian-span-reduction.md). This is an
additional theorem argument, not an independent verification of those
dependencies.

A subsequently completed [direct number-field precision
argument](algebraic-coefficient-span-precision.md), with its own
[independent review](algebraic-coefficient-span-review.md), improves the
constant bound to
\(\log_2\max(1,C)\le N^{O(h+1)}\). It replaces only the terminal
margin estimate in Section 5; the common-field reductions and Hoffman
bounds below already have this sharper size. Sections 4--6 retain the
earlier quantifier-elimination route and its conservative
\(N^{O((h+1)^2)}\) bound as a separately checked proof.

## Quantitative theorem

Let all input data be rational, let the explicit binary input length be
\(N\ge2\), and let

\[
 F=\{x\in P:q_i(x)\le0\ (1\le i\le m)\}\ne\varnothing,
 \qquad q_i(x)=\tfrac12x^TQ_ix+a_i^Tx+c_i,
\]

where every \(Q_i\succeq0\). The rational polyhedron \(P\) includes an
explicit rational box, so it is compact. Set

\[
 h=\dim_{\mathbb Q}\operatorname{span}\{Q_i\},\qquad
 v(x)=\max(0,q_1(x),\ldots,q_m(x)).
\]

The proposed quantitative conclusion is that an effectively bounded
constant satisfies

\[
 \operatorname{dist}(x,F)\le C v(x)^{2^{-h}}\quad(x\in P),
 \qquad \log_2\max(1,C)\le N^{O((h+1)^2)}.            \tag{1}
\]

The exponent in the encoding bound is deliberately conservative. This
note does not provide numerical values for the universal constants in
the quantifier-elimination theorem. It proves existence of a uniform
effective bound; it does not implement a repair algorithm.

## 1. Fix one number field for all facial reductions

Choose the unique minimum-norm point \(x^*\in F\). The algebraic-witness
theorem gives

\[
 K=\mathbb Q(x_1^*,\ldots,x_n^*),\qquad
 D=[K:\mathbb Q]\le N^{O(h+1)}.                       \tag{2}
\]

Every coordinate has a primitive integer minimal polynomial whose degree
and coefficient bit length are bounded by \(N^{O(h+1)}\). In particular,
its absolute logarithmic Weil height is bounded by the same expression.
The joint-field statement (2) is essential: separate coordinate degree
bounds would not suffice.

Write \(H(\beta)\) for absolute logarithmic Weil height, to distinguish
it from the parameter \(h\). We use natural logarithms in intermediate
height estimates; conversion to bit lengths changes only constants.
The defining local-height formula and product formula give

\[
 H(\beta\gamma)\le H(\beta)+H(\gamma),\quad
 H(\beta^{-1})=H(\beta),\quad
 H(\beta+\gamma)\le H(\beta)+H(\gamma)+\log2.
                                                               \tag{3}
\]

For \(0\ne\beta\in K\), at the intended real embedding,

\[
 e^{-D H(\beta)}\le |\beta|\le e^{D H(\beta)}.        \tag{4}
\]

The lower bound is the upper bound applied to \(\beta^{-1}\). These
inequalities also control every conjugate. The normalized height is
unchanged after passing to a normal closure; no degree of that closure
enters (3).

A useful determinant estimate is the following. If an \(r\times r\)
matrix has entries of height at most \(B\), then

\[
 H(\det M)\le r^3B+\log(r!).                         \tag{5}
\]

At a non-archimedean place the determinant is bounded by the \(r\)-th
power of the largest entry magnitude, with that maximum replaced by
its maximum with one. At an archimedean place multiply this bound by
\(r!\). Sum the local inequalities, and bound the local maximum height
by the sum of the \(r^2\) entry heights. This proves (5) directly and
avoids summing the heights of \(r!\) determinant terms separately.

## 2. Keep the reductions in the original coordinates

There is no need to introduce a new orthonormal chart at every stage.
Maintain a polyhedron \(P_j\) in the original ambient space, with
\(F\subseteq P_j\subseteq P\), and use the same point \(x^*\) throughout.
All its coefficients will lie in \(K\).

If a native quadratic has zero Hessian after restriction to
\(L_j=\operatorname{aff}P_j\), replace that row on \(P_j\) by its affine
tangent at \(x^*\):

\[
 \ell_i(x)=q_i(x^*)+\nabla q_i(x^*)^T(x-x^*).         \tag{6}
\]

For every \(x\in L_j\), the quadratic Taylor identity and the vanishing
restricted Hessian give \(q_i(x)=\ell_i(x)\). Add \(\ell_i\le0\) to
the polyhedron and remove that native row from further curved-row
processing. Its coefficients always have height \(N^{O(h+1)}\), because
they are fixed expressions in the original rational data and \(x^*\).
They do not inherit the size of a changing affine chart.

Each native row is moved at most once. Thus even allowing one affine
preprocessing projection per row gives only \(m\le N\) such steps.
Alternatively, batch all currently affine rows. Whenever a later batch
contains a newly affine row, the intervening restriction has killed a
nonzero Hessian and lowered the restricted span dimension. Neither
description requires an uncontrolled number of arithmetic rounds.

Now suppose the remaining curved rows have no common strict point in
\(P_j\). The qualitative alternative supplies a normalized nonnegative
combination \(g=\sum_i\lambda_iq_i\), with
\(\sum_i\lambda_i=1\), attaining its minimum zero over \(P_j\) at
\(x^*\). Define
\(I_q=\{i:i\text{ is a remaining curved row and }q_i(x^*)=0\}\).
Because \(g(x^*)=0\) and each \(q_i(x^*)\le0\), every positive
weight of this exposing combination belongs to \(I_q\). Restrict the
multiplier variables to this set. Polyhedral first-order optimality
then gives

\[
 \sum_{i\in I_q}\lambda_i\nabla q_i(x^*)+A_{j,I}^T\mu=0,
 \qquad \lambda\ge0,\quad\mu\ge0,\quad
 \sum_{i\in I_q}\lambda_i=1,                         \tag{7}
\]

where \(I\) uses only polyhedral rows active at \(x^*\), and every
unlisted native multiplier is fixed to zero. Encode
equalities as their two opposite inequalities. The coefficients of (7)
belong to \(K\), and the right-hand side is rational.

Choose a basic feasible solution of this nonempty standard-form linear
system. At most \(n+1\) entries are nonzero. A nonsingular subsystem
and Cramer's rule show that all its coordinates belong to \(K\), with
height at most

\[
 N^{O(1)}(B_j+B_*+1),                                \tag{8}
\]

where \(B_j\) bounds current polyhedral coefficient heights and
\(B_*=N^{O(h+1)}\) bounds the fixed expressions in (6) and (7). A
basic solution exists because a nonempty linear system with nonnegative
variables has a feasible solution with linearly independent positive
support. Normalization in (7) prevents all native multipliers from
vanishing. For these newly chosen basic multipliers, activity gives
\(g(x^*)=0\), and (7) is the first-order optimality condition for
the convex function \(g=\sum_{i\in I_q}\lambda_iq_i\) over \(P_j\).
Thus this basic combination also satisfies \(g\ge0\) on \(P_j\).
Restricting the native multipliers to active rows is necessary for this
conclusion; stationarity and normalization alone would not suffice. For
example, on \([-1,1]^2\), the rows \(q_1(x,y)=y^2\) and
\(q_2(x,y)=x^2-1\) have feasible set \([-1,1]\times\{0\}\) and
minimum-norm point zero. Both gradients vanish there. The invalid choice
\(\lambda_2=1\) would satisfy unrestricted stationarity but would
discard feasible points by forcing \(x=0\) in (9). It is excluded by
\(I_q\).

Set

\[
 A=\sum_{i\in I_q}\lambda_iQ_i,\qquad
 b=\sum_{i\in I_q}\lambda_i\nabla q_i(x^*).
\]

The next polyhedron is

\[
 P_{j+1}=P_j\cap\{x:A(x-x^*)=0,\ b^T(x-x^*)=0\}.     \tag{9}
\]

Its new coefficients lie in \(K\) and satisfy the same bound as (8),
with a different absolute polynomial. The restricted Hessian
\(A|_{L_j}\) is nonzero: it is a nonnegative combination with positive
total weight of nonzero positive semidefinite restricted Hessians.
Restriction to (9) kills it. Thus there are at most \(h\) such curved
steps.

It follows from (8) that **all** polyhedral coefficients used in the
entire reduction satisfy

\[
 B_j\le N^{O(h+1)}.                                  \tag{10}
\]

The number of rows stays polynomial in \(N\): at most the original
rows, the \(m\) tangent rows, and \(h(n+1)\) facial equations. The
field remains the single field \(K\). Repeated choices of unrelated
algebraic exposing points would not justify either conclusion.

## 3. Quantitative Hoffman constants

Consider any of these polyhedral systems, written as \(Mx\le d\),
with opposite rows for equalities. Let \(p\) be the Euclidean projection
of an arbitrary \(x\) onto its nonempty feasible set. Its normal-cone
representation can be reduced to linearly independent active rows:

\[
 x-p=M_J^T\nu,\qquad \nu\ge0,\qquad |J|\le n.
\]

Write \(r=\|(Mx-d)_+\|_\infty\). Since the rows in \(J\) are active,

\[
 \|x-p\|_2^2
 =\nu^T(M_Jx-d_J)
 \le\sqrt n\,\|\nu\|_2r,
\quad
 \|x-p\|_2\ge\sigma_{\min}(M_J)\|\nu\|_2.
\]

Thus a Hoffman constant is at most
\(\sqrt n\max_J\sigma_{\min}(M_J)^{-1}\), over independent row
subsets. Choose a nonsingular square column minor \(T\) of \(M_J\).
Then \(M_JM_J^T\succeq TT^T\), and so
\(\sigma_{\min}(M_J)^{-1}\le\|T^{-1}\|_2\).

By (4), (5), and the adjugate formula, uniformly over all these minors,

\[
 \log\max(1,\|T^{-1}\|_2)
 \le D N^{O(1)}(B_j+1)=N^{O(h+1)}.                  \tag{11}
\]

No enumeration of the minors is required for this existence bound.
Consequently every affine projection in the proof can use a Hoffman
constant whose logarithm is \(N^{O(h+1)}\).

The curved-step estimate in the qualitative note additionally contains
\(\|A\|^{1/2}\). Equations (4) and (10) bound its logarithm by the
same expression. The original quadratic Lipschitz constants and the
diameter of the input box have polynomial logarithms in \(N\). All
projection points remain in \(P\), so there is no growing-region issue.

## 4. A common-field encoding lemma

The following supplies the missing bridge from heights to rational
quantifier elimination. The algebraic-witness note constructs a
primitive generator \(\alpha\) of \(K\) as a rational linear
combination of \(x^*\), with degree and minimal-polynomial coefficient
bits \(N^{O(h+1)}\). In particular \(H(\alpha)\le N^{O(h+1)}\).

For any \(\beta\in K\) with \(H(\beta)\le B\), write uniquely

\[
 \beta=\sum_{r=0}^{D-1}c_r\alpha^r,\qquad c_r\in\mathbb Q.
\]

Let \(\sigma_1,\ldots,\sigma_D\) be the embeddings of \(K\) into a
normal closure. The equations

\[
 \sigma_j(\beta)=\sum_r c_r\sigma_j(\alpha)^r
\]

form a nonsingular Vandermonde system, because \(\alpha\) is primitive
and characteristic zero is separable. Every entry has absolute height
at most \(D H(\alpha)+B\). Cramer's rule and (5), now applied in the
normal closure, give

\[
 H(c_r)\le D^{O(1)}(H(\alpha)+B+1).                 \tag{12}
\]

The bound is independent of the normal-closure degree. Since \(c_r\)
is rational, its numerator and denominator have bit lengths bounded
by the right-hand side of (12), up to an absolute factor. Thus every
face coefficient has a rational polynomial-in-\(\alpha\) description
of total length \(N^{O(h+1)}\).

The intended real root of the primitive polynomial is selected by a
rational isolating interval of polynomial bit length in its degree and
coefficient bit length, using the elementary discriminant root-separation
bound in the algebraic-witness note. Replacing all field coefficients by
their polynomial expressions and introducing **one** root variable
therefore gives rational formulas of degree and coefficient bit length
\(N^{O(h+1)}\). Other conjugates need not preserve convexity: the
isolating interval excludes them.

This is an existence and size argument. It does not require a
number-field factorization algorithm, nor assert that coordinatewise
minimal polynomials alone permit efficient multivariate sign evaluation.

## 5. Terminal strict-feasibility margin

At the terminal polyhedron \(P_t\), either no curved rows remain, or
they admit a common strict point. In the latter case define

\[
 \theta=\min_{x\in P_t}\max_i q_i(x)<0.
\]

An epigraph variable gives a convex quadratic program with objective
\(s\), constraints \(q_i(x)-s\le0\), and an explicit rational bound
on \(|s|\) from the original box. Its native Hessian-span dimension
is at most \(h\). Its affine coefficients lie in \(K\) and have
height bounded by (10).

The active-affine restriction, polynomial dependence of active
quadratics, regularized KKT system, and multiplier support reduction
from the Hessian-span value proof all work over the ordered field
\(K\). Their affine charts require only bounded-size linear algebra
over \(K\), so (5) preserves polynomial height. The regularization
and compact-ball argument use only the intended real embedding.

After the encoding in Section 4, the scalar singleton limit formula
has two quantifier blocks with \(O(h+1)\) variables, one additional
variable selecting \(\alpha\), and rational polynomials with degree
and coefficient bits \(N^{O(h+1)}\). Coefficient-sensitive block
quantifier elimination then gives a nonzero integer annihilator for
\(\theta\), with degree and coefficient bit length
\(N^{O((h+1)^2)}\). A reciprocal Cauchy bound yields

\[
 |\theta|\ge 2^{-N^{O((h+1)^2)}}.                    \tag{13}
\]

Choose an attained minimizer \(y\in P_t\). It satisfies every
remaining row at most \(\theta\), so \(\sigma=|\theta|\) is a
strict-feasibility margin. The terminal convex-combination repair has
constant at most \(\operatorname{diam}(P)/\sigma\). Its logarithm
is bounded by (13). A separate
[terminal-margin audit](algebraic-slater-margin-review.md) expands this
coefficient extension and checks that ordinary quantifier elimination
over all original variables would be insufficient.

## 6. Assemble the constants without losing the exponent

For original residual \(0\le\delta\le1\), let \(r\) be the number
of curved reductions already performed. Inductively bound the current
native residual by \(K_j\delta^{2^{-r}}\). Affine projections multiply
\(K_j\) by a constant whose logarithm is bounded by (11). At a curved
step the distance estimate has the form

\[
 a_j\bigl(\sqrt{v_j}+v_j\bigr).
\]

Even if the intermediate residual \(v_j\) exceeds one, the induction
remains valid: since \(\delta\le1\), both terms are at most
\((\sqrt{K_j}+K_j)\delta^{2^{-(r+1)}}\). Taking all \(K_j\ge1\)
and using \(\sqrt{K_j}+K_j\le2K_j\), each step multiplies the
constant by a controlled factor. There are at most \(m+h\) steps.
The sum of their displacement estimates and the terminal repair therefore
has logarithm bounded by \(N^{O((h+1)^2)}\), and at most \(h\)
square-root steps occur. This proves (1) for \(\delta\le1\).
For \(\delta>1\), use the input-box diameter and enlarge \(C\).

If the residual also includes violations of the original affine rows,
first project onto \(P\). The original rational Hoffman bound and
quadratic Lipschitz bounds on the box give the same encoding conclusion.
This version is stated for trial points in that box, and includes the
box itself in the exact affine system.

## Sources and verification limits

The arithmetic normalization was checked against Joseph H. Silverman's
[2024 Arizona Winter School notes, Section 4, pp. 13–14](https://swc-math.github.io/aws/2024/2024SilvermanNotes.pdf),
which define absolute logarithmic height and prove independence of the
ambient number field. Equations (3)–(5) and the Vandermonde estimate are
derived here from those definitions; they are not asserted as new
number-theoretic results.

The local copy of Hoffman's 1952 paper, *On Approximate Solutions of
Systems of Linear Inequalities*, pp. 263–264, was inspected, along with
[Wang and Lin, Appendix B](https://www.csie.ntu.edu.tw/~cjlin/papers/cdlinear.pdf),
which gives the active-row and conic-support proof used in Section 3.
The determinant conversion of that estimate into a common-field height
bound is supplied above.

The argument controls irrational affine faces and repeated affine
preprocessing without enlarging the number field. The relevant
safeguards are to keep one canonical feasible point, use its joint field,
keep tangent rows in original coordinates, and include one isolated
primitive root in the compressed formula. Without these steps, an
unsupported assertion of polynomially encoded facial reductions would
remain a gap.

No numerical computation establishes the universal bound. No Lean
formalization, project-wide verification, or CI inspection was performed.
The complete argument passed a separate independent adversarial review.
That review required the explicit restriction to active native rows in
system (7); the saved correction was independently rechecked. The author independently read the saved terminal-margin audit
after its completion and found no gap in its common-field encoding,
bounded-radius argument, or additional-root-variable construction.

Targeted verification run: an inline Python check read only this file
and `algebraic-slater-margin-review.md`, checking final newlines, trailing
whitespace, control characters, paired inline/display math delimiters,
and existence of their five relative Markdown links. All checks passed.
These checks validate document integrity, not the mathematical theorem.
