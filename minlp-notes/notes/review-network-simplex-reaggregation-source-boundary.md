# Independent review: the boundary of common-matrix reaggregation

Date: 2026-09-07. Reviewer: independent subagent `literature/reaggregation_review`.

**Verdict: the proposed counterexample is correct.** A common constraint matrix and nonempty bounded disjuncts do not, by themselves, make right-hand-side aggregation an exact convex-hull formulation. This is an established limitation, not a new theorem of this repository.

The source examined is the local original PDF of Lee and Bernal Neira, *Mixed-Integer Reaggregated Hull Reformulation of Special Structured Generalized Linear Disjunctive Programs*, arXiv:2601.11782v1, January 2026. I read the model assumptions on p.2, the methodology on p.8–9, searched the full extracted paper for additional assumptions, and visually checked the original p.9. The stated structural restriction is a common left-hand-side matrix; the displayed theorem assumes nonempty disjuncts. I found no stated extra hypothesis that repairs the general claim. The proof refers readers to sufficient and necessary conditions in Jeroslow and Blair, without putting those conditions in the theorem statement. [[lee2025-mixed-integer-reaggregated-hull-reformulation]] p.2; [[lee2025-mixed-integer-reaggregated-hull-reformulation]] p.8-9. The [arXiv record](https://arxiv.org/abs/2601.11782) currently lists only v1; this review concerns that version, not an independently checked journal version.

Here is the exact arithmetic check. Set

\[
A=\begin{pmatrix}-1\\1\\2\end{pmatrix},\qquad
b^1=\begin{pmatrix}0\\1\\100\end{pmatrix},\qquad
b^2=\begin{pmatrix}0\\100\\2\end{pmatrix}.
\]

Both polyhedra \(P_j=\{x:Ax\le b^j\}\) equal \([0,1]\). Thus the convex hull of their union is \([0,1]\), and their Cayley hull is \([0,1]\times\Delta_2\). At \(\lambda_1=\lambda_2=1/2\), the intended reaggregated inequalities become

\[
-x\le0,\qquad x\le 101/2,\qquad 2x\le51.
\]

The point \(x=2\) satisfies all three inequalities, as well as valid global bounds \(0\le x\le100\), but belongs to neither hull. In fact, the reaggregated interval at this fixed selector is \([0,51/2]\). In the extended hull formulation, the first state's second row forces \(\widehat x_1\le1/2\), and the second state's third row forces \(\widehat x_2\le1/2\), so \(x=\widehat x_1+\widehat x_2\le1\).

This example uses redundant rows. That is permitted by the stated assumptions. Tightening the global upper bound to one repairs this particular example; therefore it should not be advertised as a counterexample robust to all preprocessing. Its role is to refute common-matrix structure as a sufficient condition, exactly as stated.

Theorem 2.2's literal display on p.9 is a separate issue: it has \(Ax-b^j\lambda_j\le0\) for every \(j\), without summing over the right-hand sides. The original PDF confirms this is not an extraction error. For the same example it even excludes \((x,\lambda)=(1,(1,0))\), which is a Cayley-hull point: the inactive state's rows imply \(x\le0\). The subsequent derivation and RHR display do use the sum. Consequently, the counterexample above targets the intended summed formulation, and does not rest on that apparent display error. [[lee2025-mixed-integer-reaggregated-hull-reformulation]] p.9.

The prior literature independently corroborates the distinction. Kis and Horváth, *Ideal, non-extended formulations for disjunctive constraints admitting a network representation*, §2, equation (7), explicitly discuss the common-matrix system with aggregated right-hand sides. They state that the union hull is contained in its projection, while the reverse inclusion can fail, and identify additional sufficient conditions due to Jeroslow and necessary/sufficient conditions due to Blair. This statement is directly available in the [open article](https://link.springer.com/article/10.1007/s10107-021-01652-z). This review did not independently read the original Jeroslow or Blair proofs.

The correct formulation-level statement is that aggregation always gives a valid relaxation; exactness requires proof of the reverse inclusion. At a fixed selector \(\lambda\), that is the Minkowski-sum equality

\[
\sum_j\lambda_j P_j
=\{x:Ax\le\sum_j\lambda_j b^j\}.
\]

For bounded nonempty \(P_j\), requiring this equality for every \(\lambda\in\Delta\) is equivalent to equality with the Cayley hull. Equality only after projecting away \(\lambda\) is a weaker assertion and should be distinguished from this condition. Any separately retained global constraints must also be accounted for in defining the disjuncts and the target hull.

The counterexample does **not** show that the paper's scheduling or strip-packing formulations are invalid, that their reported computations are wrong, or that aggregation cannot be effective. With binary unit-vector selectors the summed system still selects exactly one disjunct. The demonstrated failure is the unconditional LP-hull claim. Specific models may possess additional structure or valid inequalities that make aggregation exact; those models would need a separate audit.

For the network–simplex investigation, cite the established limitation and prove the appropriate reverse inclusion for each graph class. Do not use common coefficients alone as a shortcut, and do not frame this review as a new discovery of aggregation failure.
