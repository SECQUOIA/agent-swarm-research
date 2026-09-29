# Field and projection audit for nonnegative shared curvature

Date: 2026-09-28. Status: independent structural and field audit. The
proposed extension to nonnegative curvature multipliers passes the checks
below, provided its selector and recession classification are changed as
specified. This audit does not establish the separate exact QP algorithm
over a supplied real number field or reprove the imported mixed-value
theorem. No novelty claim is made.

The starting model is the one in
[the positive-multiplier note](common-range-shared-curvature-fractional.md),
with rational multipliers \(\lambda_j\ge0\). Retain every denominator
direction before eliminating continuous variables. In the resulting
coordinates \(x=T_1u+T_0v\), let \(p=(z,u,t)\) and write the lifted
linear fiber and objective as

\[
 P_p=\{y:\widehat C y\le\widehat b(p)\},\qquad
 y=(v,\eta),\qquad
 \Phi_p(y)=B(z,T_1u+T_0v)-\eta.
 \tag{1}
\]

Here \(\widehat C\) is constant rational, \(\widehat b\) has
degree at most two, and the new rows have normals
\((a_{j,v},\lambda_j)\). The denominators depend only on \((z,u)\).
The lifted threshold is exactly \(y\in P_p\), \(\Phi_p(y)\le0\):
the reverse implication uses \(\lambda_j\ge0\), and the forward
implication takes \(\eta=B\). A zero multiplier causes no problem
for this equivalence. It does mean that \(P_p\) can be empty even
when the native fiber is nonempty.

The structural recession test is

\[
 \widehat C(h,\sigma)\le0,\qquad Q_{vv}h=0,\qquad \sigma>0.
 \tag{2}
\]

This test is independent of \(p\). Full positive semidefiniteness of
\(Q\) implies that \(Q_{vv}h=0\) annihilates every quadratic cross
block involving \(h\). Consequently

\[
 \Phi_p(y+s(h,\sigma))=\Phi_p(y)-s\sigma
 \quad\text{for all real }s.
 \tag{3}
\]

The condition on the full matrix is material; a condition on the
eliminated diagonal block alone would not remove parameter-dependent
linear terms along the ray. Homogeneity lets (2) be normalized to
\(\sigma=1\). If it is feasible, rational linear programming supplies
a rational normalized direction of polynomial bit length. Fix its choice
from the input before defining a canonical output.

If (2) is infeasible, every nonempty \(P_p\) has a finite attained
minimum of \(\Phi_p\), including for irrational parameter values.
This is exactly the constant-matrix convex QP dichotomy used in
[the quadratic optimization proof](common-range-optimization.md).
The objective Hessian on \(y\) is
\(\operatorname{diag}(Q_{vv},0)\), and its only possible negative
linear coefficient on a null-curvature recession direction is
\(-\sigma\). Thus absence of (2) is the correct hypothesis for that
lemma.

Use the unique least-norm QP minimizer in each such fiber. The
[active-set chart lemma](common-range-optimizer-witness.md#2-constant-matrix-quadratic-programming-charts)
provides rational polynomial charts \(y_I(p)\) of degree at most two.
It remains essential to take a basis of all active row normals, including
zero-multiplier rows. Define

\[
 D_I=\{p:\widehat C y_I(p)\le\widehat b(p)\},\qquad
 q_I(p)=\Phi_p(y_I(p)).
 \tag{4}
\]

The \(D_I\) have quadratic atoms and the \(q_I\) are quartic. The
projection of the lifted threshold onto \(p\) is exactly

\[
 T=\bigcup_I\{p\in D_I:q_I(p)\le0\}.
 \tag{5}
\]

A feasible threshold point has a QP minimizer with no larger
\(\Phi_p\). Conversely, every retained chart point is an actual
threshold lift. No multiplier-sign guard is needed. The finite union in
(5) is closed; in particular, fixing \(z\) and \(t\) gives a closed
projection onto \(u\).

If (2) is feasible, fix \(d=(h,1)\). In this branch the threshold
projection is simply

\[
 T=\{p:P_p\ne\varnothing\}.
 \tag{6}
\]

Indeed, any \(y\in P_p\) can be shifted by
\(\max(0,\Phi_p(y))d\) to satisfy \(\Phi_p\le0\), without
violating a linear row. For polynomial charts, take the unique least-norm
point \(y_0(p)\) of the polyhedron \(P_p\), rather than minimizing
the unbounded objective \(\Phi_p\). Its active-set charts \(y_I(p)\)
have degree at most two. They give

\[
 T=\bigcup_I D_I.
 \tag{7}
\]

This is a finite union of closed sets with quadratic atoms, so closedness
does not rely on the general projection of a closed convex set being
closed. That general assertion would be false.

For a chart representing \(y_0(p)\), set \(q_I=\Phi_p(y_I)\).
The corrected selector is represented by the two closed charts

\[
 \begin{array}{lll}
 p\in D_I,\ q_I(p)\le0:& \widetilde y_I(p)=y_I(p),\\
 p\in D_I,\ q_I(p)\ge0:&
 \widetilde y_I(p)=y_I(p)+q_I(p)d.
 \end{array}
 \tag{8}
\]

The outputs agree at \(q_I=0\). Their degree is at most four, and
(3) verifies feasibility directly. Substituting a quartic output into a
quadratic would give a superficial degree-eight expression; that
substitution is unnecessary, because (3) reduces its objective value to
\(q_I-\max(0,q_I)\). Polynomial coefficient lengths stay polynomial.
All-zero multipliers are included: then \((h,\sigma)=(0,1)\) is
always a recession direction and the original threshold is entirely
linear in the eliminated variables.

A negative ray does not establish global unboundedness. For example,
\(\max\{x^2-v,1\}\) on \(\mathbb R^2\) has minimum 1. With
\(B=x^2\), its lifted linear rows are \(\eta-v\le t\) and
\(1\le t\), and \((h_x,h_v,\sigma)=(0,1,1)\) satisfies (2).
The zero-curvature row keeps the global value finite. Unboundedness must
therefore remain part of the global threshold/value procedure in both
branches.

For either branch, fix an integer assignment and an attained finite
global value \(\theta\). The projected optimal set in \(u\) is
closed by (5) or (7), and is convex because each original threshold row
has PSD Hessian \(\lambda_jQ\). Its minimum-norm point \(u_*\)
therefore exists and is unique. Choose one chart set containing \(u_*\)
and contained in that projected set. Then \(u_*\) is also the unique
minimum-norm point of that single basic closed set.

In the branch without a negative ray, this set has degree at most four;
in the negative-ray branch the set in (7) has degree at most two. The
same low-dimensional singleton formula as in
[the reviewed field proof](common-range-shared-curvature-fractional-field-review.md)
bounds the common field \(\mathbb Q(\theta,u_*)\) using only the
retained dimension and the degree of \(\theta\). Its per-polynomial
degree and height estimates do not multiply across the ambient
coordinates or the number of charts.

At \((z,u_*,\theta)\), choose the least-norm QP minimizer when no
negative ray exists. When a negative ray exists, choose the least-norm
polyhedral point and apply the fixed correction in (8). In either case
all selected eliminated coordinates belong to
\(\mathbb Q(\theta,u_*)\); the correction in (8) adds no field
extension. The rational polynomial maps have degree at most four and
polynomial coefficient length, so the established polynomial height and
conditional box argument remains applicable.

These selectors must not be described as the least-norm original
optimizer. The example

\[
 \min_v\max\{(v-2)^2,2\}=2
 \tag{9}
\]

has original minimum-norm optimizer \(2-\sqrt2\), despite having
no retained coordinates and rational value. Its lifted QP at \(t=2\)
minimizes \(v^2-\eta\) subject to \(\eta-4v+4\le2\). Its
unique minimizer is \((v,\eta)=(2,6)\), with \(\Phi=-2\).
The revised selector gives a rational original optimizer. This example
also disproves the identities \(\Phi=0\) and \(\eta=B\) at every
optimal lift, and the old common-gradient output argument cannot be
carried into the extension. The separate number-field QP recovery must
replace that argument.

An inline `python -` command using exact SymPy arithmetic checked (9),
the finite-value negative-ray example, and a quadratic chart whose
correction has degree four. It also checked the objective and linear-row
identities under that correction. All assertions passed. These are
targeted algebraic checks, not a verification of the universal theorem.
No project-wide verification or CI inspection was performed.
