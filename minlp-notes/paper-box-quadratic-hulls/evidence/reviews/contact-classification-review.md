# Independent review: edge-contact classification

Reviewed files:

- `sections/05b-contact-classification.tex`
- `appendices/E-contact-classification.tex`

Verdict: the theorem is mathematically sound under its stated hypotheses. I found no material gap or counterexample. The classification concerns extreme rays with strictly positive square coefficients, positive mixed-coefficient product, all three negative two-variable principal determinants, and no vertex zeros. It does not establish the unrestricted completeness conjecture.

## Proof audit

1. **Normalization and location of zeros.** A positive mixed-coefficient product permits coordinate complementation to make all three mixed coefficients positive. These transformations preserve extremality, the square coefficients, the three principal determinants, and vertex positivity. An interior face zero would require its two-dimensional Hessian restriction to be positive semidefinite; an interior cube zero would require the full Hessian to be positive semidefinite. The determinant assumptions exclude both. Strict positive edge curvature gives at most one zero on an edge.

2. **Strict inward derivatives.** At an edge zero, if one inward derivative vanished, a displacement in that inward coordinate combined with the minimizing displacement along the edge would have value `t^2 (Q_jj - Q_ij^2/Q_ii) < 0`. The edge root lies strictly inside its edge, so the displacement remains feasible for sufficiently small positive `t`. This proves strict positivity of both inward derivatives.

3. **Two-sided perturbations.** The value and tangency equations at each edge zero are sufficient local constraints. Completing the square in the edge displacement and shrinking the neighborhood absorbs the cross terms into positive edge curvature and the strictly positive inward linear terms. This gives `q >= delta (u^2+s+t)` and `|p| <= M (u^2+s+t)`. Finitely many neighborhoods and positivity on their compact complement then give a uniform permissible perturbation. Thus fewer than five edge zeros give a solution space of dimension at least two and contradict extremality. The proof does not require independent contact equations.

4. **Incident edges.** The face identity at two incident contact edges is determined by their endpoint square roots and edge curvatures. Evaluating at half of both edge roots gives the necessary reflected mixed coefficient at least `2 d_i d_j`; the negative determinant makes this inequality strict. Therefore the two directions must both increase, or both decrease, the Hamming weight. Three incident contacts give an affine square plus strictly positive multiples of three coordinate products, a nontrivial decomposition into nonnegative quadratics. Consequently the graph has degree at most two, and each connected component remains between a fixed pair of adjacent weight levels.

5. **Opposite edges.** The displayed two-variable identity follows by completing the square. The affine minimizer remains in the unit interval for every value of the other coordinate. Therefore its remainder coefficient is nonnegative. Positive mixed coefficient orders the two roots and gives the strict direction inequality used in cases (iii) and (iv).

6. **Graph enumeration.** The five case types in the appendix exhaust the local graph restrictions. I independently enumerated all `2^12 = 4096` edge subsets of the cube, retained subsets with at least five edges and the necessary degree/Hamming-direction restrictions, and obtained exactly 31 graphs. Their counts by `(min(a,b),max(a,b),m_0)` are `(0,0,5): 6`, `(0,0,6): 1`, `(0,1,4): 6`, `(1,1,3): 6`, `(1,2,2): 6`, and `(2,2,1): 6`. They form six orbits under coordinate permutations and simultaneous complementation; the additional orbit is the distinction between five and six central edges, both covered by case (i). This is a finite combinatorial check, not a rerun of the archived experiments.

7. **Central cycle.** The alternating sum of the edge-length equations forces the sixth contact from five contacts. The six vertex values imply a common scalar `h` and show that the difference from the affine square is `A r`, where `r` is the sum of the two opposite vertex weights. On a central edge, the square has zero gradient and the two inward derivatives of `r` are strictly positive. Nonnegativity forces `A >= 0`. If `A > 0`, the square and `A r` give a nontrivial nonnegative decomposition because only the square has positive square coefficients. If `A = 0`, the principal determinants vanish. Both possibilities contradict the hypotheses and extremality.

8. **Excluded outer-star cases.** Case (iii) gives opposite strict inequalities on `d_1,d_3`. In case (iv), completing the square across the two parallel faces produces a nonnegative remainder, and the upper contact edge then has a strictly positive square value plus nonnegative terms. In case (v), the completed-square minimizer in the first variable is strictly inside the interval at three square vertices; positivity of both corresponding mixed coefficients puts its fourth vertex value between the extreme two values. The minimizer is therefore feasible everywhere, so the remainder is nonnegative everywhere. It cannot cancel the strictly positive square on the proposed lower contact edge. These contradictions are valid, including the weak remainder case.

9. **Family recovery.** The remaining graph is a four-edge path plus an isolated edge. It is cube-equivalent to the listed family graph. The first two contacts determine the constant and two linear coefficients. The two next contacts determine vertical-root values. Writing the fifth root as `(D+k)/d_3`, the three vertical tangency equations and the value at `110` determine every remaining coefficient exactly as stated. The bottom contact's strictly positive inward derivative gives `k > 0`; the three vertical roots and two bottom roots give precisely the strict family parameter range.

10. **Converse.** The earlier five-contact theorem supplies exposedness in the full nonnegative quadratic cone. Seven vertices are endpoints of contact edges, with strictly positive values because every contact root is interior; the remaining vertex has the explicitly positive value in the appendix. The coefficient formulas make all three principal determinants strictly negative and the mixed-coefficient product positive.

## Minor clarity recommendations

The author addressed all three recommendations below during the review; they did not change the mathematical claim.

- Replace plain `D_3` by the established `\mathcal D_3` in both files.
- Use strict inward derivative positivity to conclude `k > 0` directly in the recovery argument. The current weaker `k >= 0` followed by exclusion of the affine-square case is correct under the standing determinant assumptions, but this shorter argument makes the reason explicit.
- An explicit symmetry for case (ii) would help readers check the graph correspondence. For the representative consisting of the isolated edge `000--100` and central path `110--010--011--001--101`, swap coordinates 1 and 3, then complement coordinates 1 and 2. Its image is the family graph printed in the appendix.

No literature research, numerical optimization, archived experiment reruns, or project-wide checks were performed for this review. The only fresh executable check was the finite graph enumeration described above.
