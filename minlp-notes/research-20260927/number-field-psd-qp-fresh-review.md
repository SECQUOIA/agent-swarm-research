# Fresh review of convex QP recovery over a supplied number field

Date: 2026-09-28. Status: independent proof review of
[the number-field QP construction](number-field-psd-qp-review.md).
No unresolved gap was found in its classification, approximation,
recognition, or bit-complexity arguments under the stated dense common-field
input model. This review is separate from the earlier
[nonnegative-curvature field audit](nonnegative-curvature-field-audit.md).
The construction supplies an algorithm that the existential chart argument
alone did not supply. No novelty claim is made.

The reviewed input is
\[
 \min_{Cx\le b}\ \tfrac12x^TQx+c^Tx,
 \qquad Q\succeq0,\quad Q,C\text{ rational},\quad b,c\in K,
 \qquad K=\mathbb Q(\alpha)\subset\mathbb R.
 \tag{1}
\]
The input specifies one dense field representation and its real embedding.
The number of variables is unrestricted. The desired output is the
least-Euclidean-norm optimizer, expressed in the input power basis. This
scope does not cover independently encoded algebraic coefficients whose
joint field degree is uncontrolled.

The chart identity in Section 2 of the construction is valid for this
selector. It uses a basis of all active row normals and the rational
Moore--Penrose inverse of a constant KKT matrix. Basis multipliers may be
signed. That identity is distinct from the nonnegative KKT multipliers used
in an optimality certificate. The chart therefore expresses each selected
coordinate as a rational linear combination of the entries of \(b,c\),
with uniformly polynomial coefficient length. This proves membership in
\(K\), a polynomial power-basis bound, and a polynomial-bit containing
box without enumerating charts. Adding that box preserves both the optimum
and its least-norm optimizer.

Both Hoffman bounds used in Section 3 are justified. For completeness,
let \(z\) be the projection of \(y\) onto a nonempty polyhedron
\(Mx\le r\). Its displacement has a representation
\(y-z=M_I^T\lambda\), with \(\lambda\ge0\) and independent
active row normals. Taking the inner product with \(y-z\) gives
\[
 \|y-z\|^2
 \le\|\lambda\|_1\|(My-r)_+\|_\infty
 \le\frac{\sqrt{|I|}}{\sigma_{\min}(M_I)}
       \|y-z\|\|(My-r)_+\|_\infty.
 \tag{2}
\]
Thus the displayed independent-row bound in the construction applies to
all right-hand sides. Redundant rows, zero rows, and equalities represented
by both signs cause no problem.

Here is an explicit check of the number-field determinant estimate. Choose
an integer \(S\ge1\), of polynomial bit length, such that every
\(SM_{ij}\) is an algebraic integer. Such an \(S\) is obtained by
multiplying a common denominator of all rational power-basis coefficients
by \(a^{D-1}\), where \(a\) is the absolute leading coefficient of
the degree-\(D\) polynomial of \(\alpha\). Indeed, \(a\alpha\)
is integral. Cauchy's root bound gives a computable integer \(V\ge1\),
of polynomial bit length, bounding every conjugate of every entry of
\(M\).

For any nonzero \(r\)-by-\(r\) minor \(\Delta\),
\(S^r\Delta\) is integral. Its nonzero norm is an integer, whereas
every conjugate of \(\Delta\) has magnitude at most \(r!V^r\).
Therefore, in the selected embedding,
\[
 |\Delta|\ge
 S^{-rD}(r!V^r)^{-(D-1)}.
 \tag{3}
\]
For an independent row submatrix, take one nonsingular square column
minor. The smallest singular value of the row submatrix is at least that
of this square matrix. Its determinant and operator-norm bounds give the
needed inverse-polynomial-bit lower bound. For example, for a matrix with
\(n\ge1\) columns, a conservative uniform Hoffman upper bound is
\[
 n\,S^{nD}(n!V^n)^{D-1}(nV)^{n-1},
 \tag{4}
\]
increased to at least 1 if necessary. Its logarithm is polynomial in the
dense input length. This makes clear why no enumeration of independent
row subsets and no computation of the best Hoffman constant are needed.

In the construction the second matrix is
\(M=(A^T,Q^T,-Q^T,c,-c)^T\), where \(A\) includes the box rows.
It is known before the optimizer is recovered. Although the right-hand
sides defining the optimal set are unknown, they do not enter (2)--(4).
The optimal set in the box is exactly
\[
 O=\{x:Ax\le d, Qx=Qx_*,\ c^Tx=c^Tx_*\}.
 \tag{5}
\]
The midpoint identity makes \(Qx\) constant on the convex optimal
set; its quadratic value is then constant, and optimality fixes its linear
value. These facts prove both directions of (5).

The objective-gap estimate used for this second Hoffman bound also holds
at singular \(Q\). If \(z\) is feasible in the box and
\(\gamma=f(z)-f(x_*)\), the variational inequality at \(x_*\)
gives
\[
 \tfrac12(z-x_*)^TQ(z-x_*)\le\gamma,
 \qquad
 \|Q(z-x_*)\|\le\sqrt{2\|Q\|_2\gamma}.
 \tag{6}
\]
The difference of the quadratic values is
\(\tfrac12(z+x_*)^TQ(z-x_*)\). Since both points have norm at most
\(U\), the linear-value residual is at most
\(\gamma+U\sqrt{2q\gamma}\), where \(q\ge\|Q\|_2\).
This proves the stated distance bound \(T\sqrt\gamma\) for
\(0\le\gamma\le1\). All constants may be replaced by rational
upper bounds of polynomial bit length.

The approximation proof in Section 4 selects the same point at every
precision. Outward rounding of \(b\), with exact box rows, preserves
the true boxed feasible set. Approximation of \(c\) changes any
objective comparison in the box by at most \(2U\varepsilon\).
The first Hoffman bound repairs the rounded optimizer within
\(H_A\varepsilon\) to the true boxed feasible set. Its objective
changes by at most \(LH_A\varepsilon\). These observations give
both inequalities in the construction's (9), with
\(W=2U+LH_A\).

The second Hoffman bound then supplies distance at most
\(e=H_A\varepsilon+T\sqrt\Gamma\) to \(O\), where
\(\Gamma=W\varepsilon+\delta U^2/2\). The norm penalty controls
the selected point within that set. If \(w\) is the projection of the
rounded optimizer \(y\) onto \(O\), then
\[
 \|w-x_*\|^2\le\|w\|^2-\|x_*\|^2
 \le 2W\varepsilon/\delta+2Ue.
 \tag{7}
\]
The factor \(2U\) is justified because both \(w\) and \(y\)
belong to the fixed box. Keeping the box in the repaired feasible set and
in \(O\) is therefore a substantive part of this proof.

I independently checked the precision choice in (11) of the construction.
It gives
\[
 \Gamma\le E^2/(8T^2),\qquad
 e\le E(1/2+1/\sqrt8)\le E,\qquad
 2W\varepsilon/\delta\le\tau^2/16.
\]
Together with \(E=\tau^2/[16(U+1)]\), these imply error at most
\(\tau/16+\sqrt3\tau/4<\tau\). The logarithms of the required
rational precisions are \(O(p)+N^{O(1)}\) when \(\tau=2^{-p}\).
No parameter is required to be polynomial in the reciprocal target error.
The exact rational QP has a positive definite regularized Hessian, so its
unique output is the required rational approximation.

The reconstruction step uses the existing common-field theorem correctly.
The tuple \((\alpha,x_*)\) generates exactly \(K\), rather than an
unknown compositum, and every coordinate has a polynomial height bound.
The certified approximation procedure refers to this one tuple. If its
primitive generator changes to \(\beta\), the recovered expression
\(\alpha=a(\beta)\) makes
\(1,a(\beta),\ldots,a(\beta)^{D-1}\) a rational basis.
Polynomial-size rational basis inversion converts every coordinate back
to the input power basis. Thus coordinate degrees are never multiplied
across the ambient variables.

Section 6 also passes review. A rational-matrix affine system with
algebraic right-hand side has a conditional polynomial-bit box containing
its least-norm feasible point. On that box the common-violation LP has an
optimal vertex: its optimal face is nonempty and compact, because the
\(x\) variables are boxed and the optimal \(t\) is fixed. Vertex
determinants give a polynomial-size element of \(K\). If the original
system is infeasible, its positive optimal violation has the computable
lower bound supplied by the same norm argument as (3). An outward rounding
smaller than that bound cannot change infeasibility. This proves the
proposed exact rational LP test; merely sending the rounding error to zero
would not prove a finite algorithm.

For a nonempty feasible set, the boundedness test
\(Qv+C^T\lambda=-c,\ \lambda\ge0\) is exact. Feasibility gives
a lower bound by completing the square. Otherwise separation from the
closed polyhedral cone
\(\operatorname{range}Q+\operatorname{cone}(C^T)\) gives
\(Qh=0\), \(Ch\le0\), \(c^Th<0\), hence an unbounded
feasible ray. This reduces classification to the affine routine, without
assuming an algebraic QP algorithm.

The exact rational QP import was checked independently in the primary
Russian text of
[Kozlov--Tarasov--Khachiyan](https://www.mathnet.ru/php/getFT.phtml?jrnid=zvmmf&option_lang=eng&paperid=5189&what=fullt).
Printed page 1320 defines exact solution to include feasibility,
boundedness, rational optimal value, and an attaining point, and states
deterministic polynomial Turing complexity. Section 6 on page 1323
recovers an optimal point. Clearing rational denominators preserves
polynomial input length and PSD curvature. The review also inspected
[Hoffman's original theorem](https://nvlpubs.nist.gov/nistpubs/jres/049/4/V49.N04.A05.pdf);
the quantitative estimate needed here was checked directly in (2)--(4).
The existing constructive common-field and recognition notes were read
as the stated reconstruction dependencies.

Verification was a fresh mathematical and primary-source review, followed
by a targeted integrity check of this new review file. The author's scalar
symbolic tests were not rerun. No project-wide verification, CI inspection,
or solver implementation was performed.
