# Independent review of the Hessian-span error bound

Date: 2026-09-27. Reviewer: an agent separate from the proof author. Scope: the qualitative theorem and its stated exact-penalty consequence in [the candidate note](hessian-span-holder-geometry.md). This review does not establish novelty or an encoding bound for the constant.

## Assessment

The bounded-region error-bound theorem passes this review. Its induction counts only reductions that incur a square-root loss, and every such reduction kills a nonzero member of the current restricted Hessian span. No constraint qualification, rationality of the exposing affine space, or bound on the number of quadratic rows is used.

The initial wording of the exact-penalty consequence had a separate domain issue. An error bound for distance to the global feasible set does not automatically prove exactness when optimization is restricted to an arbitrary bounded subset. The repair must also be admissible for that optimization problem. This issue does not affect the distance theorem. It was reported to the author, who corrected the statement to optimization over a bounded polyhedron included in \(P\). The reviewer independently reread that corrected statement and verified the repair.

## Proof checks

1. **Quadratic minimizer set.** If a convex quadratic \(g\) attains its minimum at \(z\in P\), convex optimality gives \(b^T(x-z)\ge0\) on \(P\), where \(b=\nabla g(z)\). The identity
   \[
   g(x)-g(z)=\tfrac12(x-z)^TA(x-z)+b^T(x-z)
   \]
   therefore expresses the gap as a sum of two nonnegative terms. For \(A\succeq0\), their joint zero set is exactly \(A(x-z)=0,\ b^T(x-z)=0\). Thus the minimizer set is polyhedral even when its displayed coefficients are irrational.

2. **Repair to this set.** Hoffman's bound applies to the real linear system defining that minimizer set. For \(x\in P\), the original polyhedral inequalities have zero violation. The remaining residuals satisfy
   \[
   \|A(x-z)\|^2\le\|A\|(x-z)^TA(x-z)
       \le2\|A\|[g(x)-g(z)],
   \]
   and \(0\le b^T(x-z)\le g(x)-g(z)\). This establishes the claimed square-root-plus-linear repair estimate.

3. **Convex alternative.** The upper image
   \[
   U=\{(q_i(x))_i+r:x\in P,\ r\in\mathbb R^m_{++}\}
   \]
   is convex and open. Failure of a common strict feasible point makes it disjoint from the open negative orthant. Separation gives a nonzero normal \(\lambda\ge0\): a negative entry would contradict the unbounded positive-coordinate directions in \(U\). The supremum of \(\lambda^Ty\) over the negative orthant is zero, so \(\sum_i\lambda_iq_i(x)\ge0\) on \(P\), by sending \(r\) to zero. An existing feasible point forces equality there. Closedness of \(U\) is unnecessary.

4. **Nonzero exposing Hessian.** After restricted zero-Hessian rows have been incorporated into the polyhedron, every remaining Hessian is a nonzero positive semidefinite matrix. A nonzero nonnegative combination of these matrices cannot be zero; for example, its trace is positive. Normalizing the weights to sum to one also gives \(0\le g(x)\le v(x)\) on \(P\).

5. **Decrease of the induction parameter.** The affine hull of the minimizer set has all its directions in \(\ker A\). Restriction to this affine hull is a linear map on the current Hessian span and kills the nonzero member \(A\). Its image consequently has dimension at most \(h-1\). This argument does not assert that the whole span vanishes, and does not confuse matrix-span dimension with matrix rank.

6. **Transfer of residuals.** Projections of a bounded set onto any fixed nonempty closed convex set stay bounded. Quadratics are Lipschitz on a ball containing the points and their projections. Hence a displacement \(O(\sqrt\delta)\) changes each constraint value by \(O(\sqrt\delta)\). Applying the inductive exponent \(2^{-h'}\), with \(h'\le h-1\), gives a power \(2^{-(h'+1)}\ge2^{-h}\). The required comparison has the correct direction for \(0\le\delta\le1\). For \(\delta>1\), bounded distance to a fixed feasible point handles the remainder.

7. **Strict feasibility branch.** Mixing \(x\in P\) with a fixed strictly feasible point \(y\in P\), using weight \(\delta/(\sigma+\delta)\) on \(y\), gives a feasible point by convexity. On a bounded set the displacement is \(O(\delta)\). The strict point may lie outside the bounded set under consideration; the distance theorem only needs it to belong to \(P\).

8. **Sharpness.** In the power-chain example, backward induction forces every coordinate to zero at a feasible point. On the displayed curve the first \(h-1\) residuals are zero and the last is exactly \(t^{2^h}\), while distance to the feasible set is at least \(t\). Thus no larger uniform exponent is possible for a fixed value of \(h\).

## Affine preprocessing clarification

Incorporating zero-Hessian rows into the current polyhedron can shrink its affine hull. Some rows that were curved before that restriction can then become affine. The author corrected the proof to repeat preprocessing until every remaining restricted Hessian is nonzero, or no quadratic rows remain; the reviewer independently reread this correction. Each nontrivial repetition removes at least one remaining row, so the process terminates. Each projection has only a linear residual loss by Hoffman's bound; their finite composition therefore does not consume a square-root step or change the claimed exponent. This is a clarification of the proof, not a counterexample to it.

For example, the rows \(x\le0,-x\le0,x^2\le0\) over \(P=\mathbb R^2\) first restrict the polyhedron to \(x=0\). The final row is then identically zero and must be reclassified before applying the nonzero exposing-Hessian argument.

## Exact-penalty domain counterexample and repair

The initial statement required only that repairs lie in the objective's Lipschitz region. That is insufficient for exactness over an arbitrary bounded set \(K\).

Take \(P=\mathbb R^2\), the affine constraint \(q(x)=x_1\le0\), and
\[
 K=\{(t,10t):0\le t\le1\},\qquad f(x)=-x_2.
\]
Here \(h=0\), \(v(x)=(x_1)_+\), and
\(\operatorname{dist}(x,F)=v(x)\), so \(C=1\) is valid. The objective is globally \(1\)-Lipschitz. Nevertheless, with penalty coefficient \(2>1=L_fC\), the penalized value on \(K\) is \(-8t\), whose minimum occurs at the infeasible point \(t=1\). The only feasible point of \(K\) is \(t=0\). The global feasible projection of \((t,10t)\) is \((0,10t)\), which is outside \(K\) for \(t>0\).

A sufficient corrected statement is to include the bounded polyhedral optimization domain in \(P\), and use distance to its feasible subset. More generally, every repair used in the penalty proof must belong to the admissible domain. If \(f\) is Lipschitz along these repairs and \(\rho>L_fC\), then
\[
 f(x)+\rho v(x)^{2^{-h}}
 \ge f(x_F)+(\rho-L_fC)v(x)^{2^{-h}},
\]
which gives strict improvement by an admissible feasible repair whenever \(v(x)>0\).

## Verification and limits

This review checked the exact identities, separation argument, dimension decrease, exponent inequalities, and counterexample symbolically. A further independent agent was asked to challenge the same qualitative proof and independently identified the affine-preprocessing clarification and the penalty-domain issue. No numerical test or formal proof assistant was used: neither would replace the separation and induction arguments here. This review does not certify a computable constant, its bit complexity, a global unbounded-region bound, or priority relative to existing error-bound and facial-reduction results.

A targeted Python check of this review file passed for control characters, trailing whitespace, final newline, and balanced inline/display math delimiters. This was document validation only. No project-wide verification or CI inspection was performed.
