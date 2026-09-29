# Review of exact witnesses at small common Hessian range

Date: 2026-09-28. Scope: the arithmetic lemma and algorithm in
[the exact witness note](common-range-witness-recovery.md), extending
[common-range feasibility](common-range-fpt-frontier.md).
The reviewer independently reconstructed the proof, read the local
genericity, elimination, and common-field recovery inputs, and inspected
the primary comparison below. This is a proof review, not a formalization
or a novelty determination. The completed author manuscript was then read
in full and compared with the reconstruction below. Earlier review feedback
contributed the inactive-box simplification and the primary-source shortcut;
those parts are overlapping proof contributions as well as checks.

**Finding.** No substantive gap was found. The proof gives the required arithmetic and
algorithmic bounds. The exponential number of projected rows enters the
height through its logarithm. The arithmetic lemma is also a close
corollary of an existing primary result, so it should not be presented as
a new elimination theorem. The candidate addition is the combination with
the implicit exact-feasibility oracle and recovery of eliminated variables.

## 1. The arithmetic statement needs one joint field

Let

\[
 U=\{u\in\mathbb R^r:P_i(u)\le0\quad(1\le i\le S)\}
\]

be nonempty, closed, and convex. Suppose the polynomials are rational,
have degree at most two, and have coefficient bit lengths at most
\(\tau\). Clear denominators separately in each row; this replaces
\(\tau\) by at most a polynomial in \(r\) times \(\tau+1\).
The unique minimum-norm point \(u^*\) exists even if \(U\) is unbounded.
The required conclusions are

\[
 [\mathbb Q(u_1^*,\ldots,u_r^*):\mathbb Q]\le 2^{O(r)},
 \qquad
 \operatorname{bits}(m_{u_j^*})
       \le (\tau+\log(S+1)+1)2^{O(r)}.                 \tag{1}
\]

Here the second expression means the maximum coefficient bit length of
the primitive integer minimal polynomial. Multiplying the separate
coordinate degrees would only give \(2^{O(r^2)}\), so it does not
establish the first bound.

The case \(r=0\) is rational linear feasibility and recovery. It should
be handled separately, without an artificial zero-dimensional invocation
of a radius or algebraic-recognition theorem.

## 2. Direct check of the local perturbation proof

The following uses the already reviewed generic quadratic lemma in
[the nonconvex note, Section 4](nonconvex-hessian-span-frontier.md#4-a-quantitative-genericity-lemma).
Introduce integer quadratic polynomials \(Q_0,Q_1,\ldots,Q_S\) and use

\[
 f_{i,\epsilon}(u)=P_i(u)+\epsilon^2Q_i(u)-\epsilon,
 \qquad
 g_\epsilon(u)=\|u\|_2^2+\epsilon Q_0(u).             \tag{2}
\]

Only subsets of at most \(r+1\) rows are needed. For subsets of at most
\(r\) rows, exclude gradient dependence and singular bordered KKT
matrices. For subsets of size \(r+1\), exclude common zeros. The latter
exclusion is essential: it ensures that no minimizer has more than
\(r\) active rows. The number of subsets is at most a polynomial in
\(r\) times \((S+1)^{r+1}\).

For each fixed nonzero \(\epsilon\), the selected perturbation
coefficients map surjectively onto arbitrary selected constraint and
objective quadratics. Therefore substituting (2) into a nonzero bad-locus
polynomial does not give the zero polynomial in the joint perturbation
coefficients and \(\epsilon\). Select one nonzero coefficient in its
expansion in \(\epsilon\). The product of these selected coefficient
polynomials has degree at most

\[
 (S+1)^{r+1}2^{\operatorname{poly}(r)}.                \tag{3}
\]

A nonzero polynomial of total degree \(D\) cannot vanish on the entire
integer grid \(\{0,\ldots,D\}^p\), regardless of the number \(p\)
of perturbation coefficients. Hence the \(Q_i\) can be chosen with
coefficient bits

\[
 O(r\log(S+1))+\operatorname{poly}(r).                \tag{4}
\]

Their total description is potentially exponential in the original input.
No algorithm constructs them. Only the size of each coefficient is used
in the existence proof. Counting the entire perturbation vector as part
of the elimination input would lose the needed bound.

Choose any auxiliary radius \(R>\|u^*\|_\infty+1\). Minimize
\(g_\epsilon\) subject to the rows in (2) and the hard box
\([-R,R]^r\). For all sufficiently small positive \(\epsilon\),
the point \(u^*\) is feasible, because there are finitely many fixed
values \(Q_i(u^*)\) and the negative linear term in \(\epsilon\)
dominates the quadratic term. Compactness gives minimizers.

Every sequence of these minimizers has a convergent subsequence. Its
limit belongs to \(U\), and comparison with \(u^*\) shows that its
norm is at most \(\|u^*\|_2\). Uniqueness therefore forces every
such limit to be \(u^*\). Since \(u^*\) lies strictly inside the
hard box, all box rows are inactive at every minimizer for sufficiently
small \(\epsilon\). Otherwise a subsequence of boundary minimizers
would have a boundary limit. Thus the unknown \(R\) never enters the
KKT coefficient bounds.

Fix an active set occurring along an infinite sequence approaching zero.
Its size is \(s\le r\); the selected gradients are independent and
the full KKT Jacobian is nonsingular. Use the full system in
\((u,\lambda)\), rather than eliminating \(u\) by a Hessian inverse.
It has \(r+s\le2r\) variables and equations, degree at most two in
those variables, and coefficient norm bits

\[
 (\tau+\log(S+1)+1)\operatorname{poly}(r).
\]

The [finite-quotient lemma](explicit-span-separation.md#2-an-elementary-elimination-lemma),
with \(a=2\), gives degree at most \(3^{r+s}\le9^r\) and height
as in (1) for the finite limit of each coordinate. It requires neither
bounded multipliers nor a finite full special fiber at \(\epsilon=0\).
Applying the same lemma to every rational linear form in \(u\) gives
the same degree bound, independent of the chosen linear-form coefficients.
After the coordinates are known to be algebraic, choose a primitive
rational linear form. This proves the joint-field bound. Passing from an
annihilator to a minimal-polynomial factor preserves the stated height
bound.

This reconstruction found no gap. Convexity is used for the uniqueness
and subsequent approximation argument, not for generic regularity of the
perturbed quadratics.

## 3. A stronger primary-source comparison

[Jeronimo--Perrucci--Tsigaridas](https://arxiv.org/pdf/1112.0544),
Proposition 10, explicitly bounds resultant coefficients using
\(\widetilde H=\max(H,2n+2m)\). Their Remark 11 applies the construction
to minimizer coordinates. Lemma 9 proves that the relevant deformed
projective KKT fiber is finite and avoids the hyperplane at infinity,
independently of the output polynomial. Replacing that polynomial by
\(T x_0-\ell(x)\) therefore also covers a rational linear form
\(\ell\), while retaining stationarity for the original norm objective.
For degree two the output-degree bound is
\(\binom{r}{s}2^s\le3^r\), and the coefficient formula gives the
height in (1). A primitive linear form gives the joint degree bound.
Their Theorem 12 treats noncompact components with a compact minimizer
set by adding an inactive auxiliary ball. For \(r=1\), one can pad
with a coordinate forced to zero, since their main setup assumes
\(n\ge2\).

Thus the arithmetic input has a direct classical route, with a better
degree constant than the local finite-quotient route. Neither route
implies an efficient algorithm for explicitly enumerating the projected
row family.

## 4. Approximating the same projected point

After a rational kernel coordinate change, the original rows have form
\(C_iv+p_i(u)\le0\), where \(C\) is constant and rational.
Farkas elimination gives the preceding description of \(U\), but the
algorithm asks feasibility questions in the original variables.

The norm query

\[
 \|u\|_2^2\le t
 \quad\Longleftrightarrow\quad
 \|(2u,t-1)\|_2\le t+1
\]

uses rational coefficients for rational \(t\ge0\). Its squared
Hessian vanishes on every eliminated \(v\) direction. It therefore
does not enlarge the common range dimension. This contrasts with adding
a norm bound on all original coordinates, which can enlarge that
dimension to the full ambient dimension.

Use an effective small-point radius to bound \(\|u^*\|\), then
bisect the norm threshold until its feasible upper value differs from
\(\|u^*\|^2\) by at most \(\varepsilon^2/16\). The projection
inequality

\[
 \|u-u^*\|^2\le\|u\|^2-\|u^*\|^2\qquad(u\in U)
\]

places every point in the retained norm sublevel within
\(\varepsilon/4\) of \(u^*\). Coordinate bisection retaining a
nonempty intersection then gives a rational approximation of the specified
tuple \(u^*\). Restart from the original coordinate box at each
accuracy request. A box retained from a previous approximation may fail
to contain \(u^*\).

The count and bit lengths of these queries are polynomial in input length,
the radius bits, and requested precision, with absolute exponents.
Substituting bounds \(2^{O(r)}N^C\) preserves that form. The implicit
family of projected rows is never generated or queried individually.

## 5. Recovering the eliminated variables without an algebraic LP oracle

For the now specified point \(u^*\), write its nonempty fiber as

\[
 F=\{v:Cv\le b\},\qquad b_i=-p_i(u^*),
 \qquad v^*=\operatorname*{argmin}_{v\in F}\|v\|^2.
\]

The normal-cone formula places \(v^*\) in the span of its active row
normals. Select independent active rows \(I\) spanning those normals.
Then

\[
 v^*=C_I^T(C_IC_I^T)^{-1}b_I.                         \tag{5}
\]

The empty active set gives \(v^*=0\). Formula (5) proves that
\(v^*\in\mathbb Q(u^*)\); it does not require knowing the correct
set \(I\) algorithmically. Rational minor bounds control its coefficient
bits by a polynomial in the explicit input. A common integer multiple
making every \(u_j^*\) integral, together with their conjugate bounds,
then bounds the heights of the quadratic values \(b_i\) and the rational
linear combinations (5). The full tuple has degree \(2^{O(r)}\) and
coordinate heights \(2^{O(r)}N^C\).

There is a computable \(H_C\le2^{N^C}\) satisfying the Hoffman bound
for this fixed rational matrix and every feasible right-hand side:

\[
 \operatorname{dist}(y,F)
       \le H_C\|(Cy-b)_+\|_\infty.                   \tag{6}
\]

For a direct check, let \(p\) be the projection of \(y\) onto
\(F\), and choose a representation
\(y-p=C_I^T\lambda\) with independent active row normals and
\(\lambda\ge0\). If the violation is at most \(\delta\),

\[
 \|y-p\|^2
 =\lambda^T(C_Iy-b_I)
 \le\delta\sqrt{|I|}\|\lambda\|
 \le\frac{\delta\sqrt{|I|}}{\sigma_{\min}(C_I)}\|y-p\|.
\]

Uniform rational minor bounds for all independent row subsets give the
stated effective \(H_C\). No enumeration of these subsets is needed.

Approximate \(b\) outward by rational \(b^\delta\) with
\(b\le b^\delta\le b+\delta\mathbf1\), and compute the exact
rational minimum-norm point \(v^\delta\) of
\(Cv\le b^\delta\). This is a rational convex quadratic program,
covered by the classical
[Kozlov--Tarasov--Khachiyan algorithm](https://doi.org/10.1016/0041-5553(80)90098-1).
It is always feasible and has an attained unique minimum.

Let \(M\ge\|v^*\|\) be an effective bound. Because the relaxed
polyhedron contains \(F\), \(\|v^\delta\|\le\|v^*\|\).
Equation (6) supplies \(w\in F\) with
\(\|w-v^\delta\|\le\eta=H_C\delta\). The minimum-norm
projection inequality gives

\[
 \|v^\delta-v^*\|
 \le \eta+\sqrt{2M\eta+\eta^2}.                    \tag{7}
\]

For \(0<\varepsilon\le1\), choosing
\(\eta\le\varepsilon^2/[16(M+1)]\) makes the right side less
than \(\varepsilon\). The required bit precision is
\(O(\log(1/\varepsilon)+\log(M+1)+\log(H_C+1))\).
The polynomial values \(b_i\) are approximated from the canonical
\(u^*\) oracle using a coefficient and radius bound on their gradients.
Thus this is a certified rational approximation oracle for one specified
tuple \((u^*,v^*)\), with the required FPT cost.

Finally apply the existing
[common-field recovery algorithm](constructive-common-field-recovery.md)
and the rational coordinate change back to the original variables.
The recovered original inequalities, including every squared SOC row's
affine sign condition, admit direct verification in the selected real
embedding. The returned point need not be the minimum-norm point in the
original coordinates; the two-stage choice is what the proof specifies.

## 6. Limits of the review

The argument depends on the exact common-range feasibility theorem and
classical exact rational convex QP and algebraic-recognition algorithms.
It does not give a practical numerical tolerance or establish novelty of
the combined algorithm. General semialgebraic convexity without the native
SOC or PSD representation would not provide the required feasibility
oracle. The proof does not use, or need, an algorithm constructing all
Farkas inequalities or choosing the existential perturbations.

The final manuscript comparison separately checked the absolute input
exponent after substituting the requested recognition precision. It also
checked that formula (5) preserves the field and bounds coefficient
heights: quadratic evaluation requires the square of a common denominator
for the \(u_j^*\), followed only by rational denominator clearing and
a field norm of degree at most the existing joint-field degree. Neither
step introduces a product of coordinate degrees.

In the native PSD-quadratic model, the norm query can be appended directly
as a PSD quadratic row. In the SOC model, use its rational cone
representation. Thus both stay within their respective decision models.

No broad tests or CI inspection were performed. Verification here consists
of independent proof reconstruction and primary-source inspection.
A targeted inline `python -` check passed for this review's local links,
whitespace, control characters, final newline, and paired math delimiters.
These document checks do not verify the mathematical proof. No numerical
experiment or Lean formalization is claimed.

## 7. Addendum: a rational matrix for the optimal-face completion

This separate check concerns the extension in
[the optimization note, Section 7](common-range-optimization.md#7-exact-continuous-optimizer-the-remaining-output-construction).
It does not change the feasible-witness theorem. Assume the finite value
\(\theta\) is attained, and the nonempty convex optimal set is under
consideration. Write the rational PSD objective as

\[
 q_0(x)=\tfrac12x^TQ_0x+a_0^Tx+c_0.
\]

Its gradient \(g=Q_0x+a_0\) is constant on that optimal set: along
the segment between any two optimizers the objective is constant, so
\((x-y)^TQ_0(x-y)=0\), and positive semidefiniteness gives
\(Q_0(x-y)=0\). Suppose the preceding recovery procedure has supplied
\(\theta,g,u^*\) in one real embedded number field \(K\), with
degree \(f(r)\) and coefficient heights \(f(r)N^C\), where
\(u^*\) lies in the projection of that optimal set.

Put \(b=g-a_0\). The system \(Q_0x=b\) is consistent. Rational
row reduction of the fixed matrix \(Q_0\) gives a rational solution
operator on its image, with polynomial coefficient bit lengths. Applying
it to \(b\) gives a particular point \(x_0\in K^n\). For every
solution \(x=x_0+d\), we have \(Q_0d=0\), and symmetry gives

\[
 x^TQ_0x=x_0^TQ_0x_0.
\]

Thus the objective level is expressed by the two affine conditions

\[
 Q_0x=b,\qquad
 a_0^Tx=\theta-c_0-\tfrac12x_0^TQ_0x_0.             \tag{8}
\]

Every normal in (8) is rational. Together with original feasibility and
\(u=u^*\), these equations are equivalent to membership in the optimal
set on that fiber. The particular \(x_0\) itself need not be feasible.
For \(Q_0=0\), take \(x_0=0\), so this also covers affine and
constant objectives. Positive semidefiniteness is needed for the common
gradient argument; the displayed quadratic identity only needs symmetry.

Substituting \(x=T_1u^*+T_0v\) leaves rational normals
\(Q_0T_0\) and \(a_0^TT_0\), in addition to the original rational
fiber normals. Equalities are represented by both signs. Their right-hand
sides are polynomials of degree at most two in the recovered tuple
\((\theta,g,u^*)\), with polynomial-bit rational coefficients.
If \(A\) makes every entry of this tuple integral, then \(A^2\)
handles its quadratic products. Clearing the remaining rational
denominators and bounding conjugates gives right-hand-side height
\(f(r)N^C\). All entries remain in the same field \(K\); no field
extension is introduced. The minimum-norm completion is a rational Gram
matrix combination of these right-hand sides and therefore also lies
in \(K\), with the same form of height bound.

Consequently Sections 5--6 apply with this enlarged rational matrix.
Its Hoffman constant still has polynomial bit length in the explicit
rational data, independently of the algebraic right-hand side. Outward
rational approximation, exact rational QP, and common-field recognition
recover an exact optimal completion with the stated FPT overhead. This
check is conditional on the preceding joint-field and approximation
bounds for \((\theta,g,u^*)\); it does not independently review those
optimization results.

An inline `python -` command used exact SymPy arithmetic to verify the
identity and the rational-normal objective level for the singular matrix
\(Q_0=(1,2,3)^T(1,2,3)/6\), with symbolic kernel directions. It also
checked the zero-Hessian case. Both checks passed. They verify those
examples; the general argument is the kernel calculation above.
