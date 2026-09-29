# Bounded-region error bounds from the span of convex quadratic Hessians

Date: 2026-09-27. Status: qualitative proof independently reviewed. The [later conic comparison](hessian-span-holder-hu-li-comparison.md) derives the exponent from established facial-reduction results and a short span argument, so its contribution is a modest structural corollary. The [quantitative facial argument](hessian-span-holder-height-review.md), sharpened by [direct number-field arithmetic](algebraic-coefficient-span-precision.md) and its [independent review](algebraic-coefficient-span-review.md), gives \(\log C\le N^{O(h+1)}\) for rational boxed data. Publication priority for that arithmetic bound remains unestablished.

## Result and scope

Let
\[
 F=\{x\in P:q_i(x)\le0,\ i=1,\ldots,m\}\ne\varnothing,
 \qquad q_i(x)=\tfrac12x^TQ_ix+a_i^Tx+b_i,
\]
where \(P\subseteq\mathbb R^n\) is a nonempty polyhedron and every \(Q_i\succeq0\). Data may be real. Write
\[
 h=\dim\operatorname{span}\{Q_1,\ldots,Q_m\},\qquad
 v(x)=\max(0,q_1(x),\ldots,q_m(x)).
\]
For every bounded set \(K\subseteq P\), there is a finite constant \(C\) such that
\[
 \operatorname{dist}(x,F)\le C v(x)^{2^{-h}}
 \qquad(x\in K).                                      \tag{1}
\]
The exponent is uniformly sharp as a function of \(h\). No Slater condition, rational affine-hull assumption, or bound on the number of rows is required. The count can be reduced to the dimension of the Hessian span after restriction to \(\operatorname{aff}P\).

For a bounded set of arbitrary points, include positive affine-inequality violations and absolute affine-equality violations in the maximum residual. The same exponent then holds. In particular, an explicit input box can be part of the affine system, or can specify the bounded region on which the bound is wanted.

A consequence is a distance guarantee for an approximate feasible point: a residual at most \(\varepsilon\) implies distance at most \(C\varepsilon^{2^{-h}}\). If the optimization domain itself is a bounded polyhedron \(P\), an objective with Lipschitz constant \(L_f\) on \(P\) admits an exact penalty \(f+\rho v^{2^{-h}}\) for every \(\rho>L_fC\). Here exactness means equality of the full minimizer sets over \(P\) and over \(F\). Indeed, projecting an infeasible point onto the closed convex set \(F\subseteq P\) supplies an admissible repair that strictly improves the penalized objective. Merely restricting the estimate to an arbitrary bounded set \(K\subseteq P\) would not ensure that repairs lie in \(K\), and does not imply this optimization claim over \(K\). The coefficient assertion is existential; it does not give a procedure to compute \(C\).

## A quadratic minimizer set is polyhedral

We first record an elementary lemma. Let \(g(x)=\tfrac12x^TAx+c^Tx+d\), \(A\succeq0\), attain its minimum \(\gamma\) over a polyhedron \(P\). Choose a minimizer \(z\), and put \(b=\nabla g(z)\). Optimality gives
\[
 b^T(x-z)\ge0\qquad(x\in P).
\]
Consequently
\[
 g(x)-\gamma=\tfrac12(x-z)^TA(x-z)+b^T(x-z),
\]
and both terms on the right are nonnegative on \(P\). Thus its minimizer set is the polyhedron
\[
 S=P\cap\{x:A(x-z)=0,\ b^T(x-z)=0\}.                 \tag{2}
\]
[Hoffman's bound](https://nvlpubs.nist.gov/nistpubs/jres/049/4/V49.N04.A05.pdf), applied to this fixed real linear system, yields
\[
 \operatorname{dist}(x,S)
 \le H\bigl(\|A(x-z)\|+|b^T(x-z)|\bigr)
 \le H\bigl(\sqrt{2\|A\|\,[g(x)-\gamma]}+g(x)-\gamma\bigr)
 \quad(x\in P).                                    \tag{3}
\]
No rationality is asserted for the coefficients of (2). Hoffman's theorem applies to real matrices. If \(A=0\), the square-root term is absent.

## A facial reduction that consumes one Hessian dimension

Work in the affine hull of the current polyhedron, using orthonormal coordinates. Any row whose restricted Hessian is zero is affine and can be put into the polyhedron. Suppose at least one curved row remains and there is no point of this polyhedron at which every remaining curved row is strictly negative.

The usual convex alternative gives nonnegative weights \(\lambda_i\), not all zero, with
\[
 g(x)=\sum_i\lambda_iq_i(x)\ge0\qquad(x\in P).
                                                               \tag{4}
\]
For completeness, separate the convex upper image
\(\{(q_i(x))_i+r:x\in P,\ r\in\mathbb R^m_{++}\}\)
from the negative orthant. Their disjointness follows from failure of strict feasibility. A separating normal has nonnegative entries. Since a feasible point exists, the separating level is zero. This is a finite-dimensional separating-hyperplane argument; closedness of the upper image is unnecessary when the other set is open.

Every original feasible point has \(g=0\); hence \(g\) attains its minimum zero on \(P\). Normalize \(\sum_i\lambda_i=1\). Its Hessian
\[
 A=\sum_i\lambda_iQ_i
\]
is nonzero, since all the remaining \(Q_i\) are nonzero positive semidefinite matrices. Let \(S=\operatorname{argmin}_P g\), the polyhedron in (2). By (3),
\[
 \operatorname{dist}(x,S)\le C_0(\sqrt{v(x)}+v(x))
 \qquad(x\in P).                                  \tag{5}
\]

Every direction of \(\operatorname{aff}S\) lies in \(\ker A\). Therefore restriction to \(\operatorname{aff}S\) kills the nonzero member \(A\) of the current Hessian span. The image of that span has dimension at most \(h-1\). Positive semidefiniteness also shows that it kills every \(Q_i\) with \(\lambda_i>0\): a zero value of a nonnegative weighted sum of quadratic forms forces each positive-weight form to vanish. The feasible set is unchanged when \(P\) is replaced by \(S\), because \(F\subseteq S\).

This dimension decrease counts curved reductions only. Restricting to an affine face created by affine rows cannot increase the Hessian span and incurs only a Lipschitz projection estimate.

## Proof of the bound

We prove (1) by induction on the dimension of the restricted Hessian span. Throughout the proof, all projection points range over bounded sets: if \(z_0\) is any fixed point in a nonempty closed convex set \(S\), then
\[
 \|\Pi_S(x)\|\le \|z_0\|+2\|x-z_0\|.
\]
Thus every quadratic used below has a finite Lipschitz constant on a common bounded ball containing the points in that step.

First move all zero-Hessian rows into the polyhedron. If a point \(x\in K\) violates these affine rows, project it onto the resulting nonempty polyhedron \(P'\). Hoffman's bound gives \(\|x-x'\|\le H v(x)\), and the remaining quadratic residual at \(x'\) is at most \(C_1v(x)\) on the bounded region under consideration. Proving the assertion over \(P'\) therefore suffices; for \(0\le v\le1\), a linear term is at most the claimed fractional power. Repeat this preprocessing after any change in the affine hull: a formerly curved row may become affine on the smaller polyhedron. Each nontrivial repetition removes at least one remaining row and uses only a linear Hoffman repair. Their finite composition still has a linear residual loss. We may consequently assume that every remaining row has nonzero Hessian after restriction to the current affine hull.

If no rows remain, the feasible set is the current polyhedron and the claim is already supplied by the affine projection. This includes the base case \(h=0\).

If there is a point \(y\in P\) with every remaining \(q_i(y)<0\), choose \(\sigma>0\) such that \(q_i(y)\le-\sigma\) for all these rows. For \(x\in P\), let \(\delta=v(x)\). The convex combination
\[
 x_F=\frac{\sigma}{\sigma+\delta}x+
     \frac{\delta}{\sigma+\delta}y
\]
is feasible, and on a bounded set
\[
 \operatorname{dist}(x,F)\le\|x-x_F\|
 \le\frac{\sup_{x\in K}\|x-y\|}{\sigma}\,\delta.
\]
This is stronger than (1) when \(0\le\delta\le1\).

Otherwise perform the reduction (4)–(5), and put \(x'=\Pi_S(x)\). For \(0\le\delta=v(x)\le1\), (5) gives
\[
 \|x-x'\|\le C_2\sqrt\delta,
 \qquad v(x')\le\delta+L\|x-x'\|
                    \le C_3\sqrt\delta.             \tag{6}
\]
The restricted Hessian span has dimension \(h'\le h-1\), so induction on the bounded set of projection points gives
\[
 \operatorname{dist}(x',F)
 \le C_4v(x')^{2^{-h'}}
 \le C_5\delta^{2^{-(h'+1)}}
 \le C_5\delta^{2^{-h}}.
\]
The triangle inequality and \(\sqrt\delta\le\delta^{2^{-h}}\) finish the proof for \(\delta\le1\). For \(\delta>1\), distance is bounded on \(K\) by distance to any fixed feasible point, so enlarging \(C\) finishes the result. The same preliminary Hoffman projection proves the version including all affine violations.

The induction does not require that the dimensions of the affine hulls or the number of affine reductions be bounded by \(h\). Only the steps that take square roots are charged to the decreasing Hessian-span dimension.

## Sharpness

For \(h\ge1\), take
\[
 q_i(x)=x_i^2-x_{i+1}\quad(1\le i<h),\qquad
 q_h(x)=x_h^2.
\]
The feasible set is \(\{0\}\), and the Hessians are independent diagonal matrices, so their span has dimension exactly \(h\). On the curve
\[
 x(t)=(t,t^2,t^4,\ldots,t^{2^{h-1}}),\qquad0<t\le1,
\]
all rows except the last vanish, while
\[
 v(x(t))=t^{2^h},\qquad\operatorname{dist}(x(t),F)\ge t.
\]
An exponent \(\alpha>2^{-h}\) would require
\(t\le C t^{2^h\alpha}\) for all sufficiently small \(t>0\), which is impossible. This power-chain obstruction is classical; it is not claimed as a new example.

## What the result does not yet establish

1. It proves a bounded-region estimate. A global estimate of the form \(C(v+v^{2^{-h}})\), without a bounded region, is not proved here.
2. This qualitative induction alone does not bound the encoding of \(C\): its separating multipliers and affine offsets may be irrational. The [separate quantitative proof](hessian-span-holder-height-review.md) fixes one algebraic feasible point and controls all reductions in its common number field. The [reviewed arithmetic refinement](algebraic-coefficient-span-precision.md) obtains \(\log C\le N^{O(h+1)}\) for rational boxed data by working directly over that field. The earlier primitive-element quantifier-elimination proof remains a valid conservative route. The value-height theorem alone would not establish the error-constant conclusion.
3. It does not give an efficiently computed repair map: the proof uses a sequence of existential reductions and projections.
4. [The first prior review](hessian-span-holder-prior.md) compares the result to Wang–Pang's singularity-degree bound and subsequent facial-reduction results. The [original-source follow-up](hessian-span-holder-original-source-audit.md) obtained the full Luo–Sturm quadratic-systems chapter. More decisively, the [full Shor derivation](hessian-span-holder-hu-li-comparison.md) combines existing partial-polyhedral facial reduction and conic error bounds with a short Hessian-span decrease argument to obtain the qualitative theorem. Thus the exponent should be presented as a modest structural corollary of established theory. Neither that derivation nor the inspected sources supplies the separate coefficient bound with its dependence on \(h\). Priority remains unresolved; the original Wang–Pang proof and a different Luo–Sturm Handbook chapter were not fully inspected.

## Verification

The proof uses exact identities, convex separation, and Hoffman's linear error bound. No numerical experiment or formal proof assistant verification is asserted. The sharpness calculation is symbolic and holds for every positive integer \(h\). [Independent adversarial review](hessian-span-holder-review.md) checked the separation argument, affine-only preprocessing, and decrease of the restricted Hessian span. It identified an exact-penalty domain issue in the first draft, which was corrected and rechecked, and requested the explicit iteration of affine preprocessing now included above. A further independent reviewer concurred with the qualitative proof. The reviews do not establish novelty or a coefficient-height bound.
