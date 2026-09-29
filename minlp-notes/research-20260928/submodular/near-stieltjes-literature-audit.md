# Exact near-Stieltjes indicator optimization: literature boundary

Date: 2026-09-28. Status: literature audit and a small exact counterexample.
This note establishes no new tractability or hardness theorem. In particular,
failure to find a theorem is not evidence that the question is open in the
literature.

The target model is

\[
 \min\{x^TQx-2b^Tx+c^Tz:0\le x_i\le u_i z_i,
          \ z\in\{0,1\}^n\},\qquad Q\succ0,
\]

without additional indicator constraints. Infinite upper bounds mean that an
inactive coordinate is zero and an active coordinate is nonnegative. The
parameters of interest are the number of positive off-diagonal pairs, or the
minimum number of coordinates meeting every such pair.

## Strongest directly relevant baseline

[Han and Gómez, *Convex Submodular Minimization with Indicator Variables*,
arXiv:2209.13161v2](https://arxiv.org/html/2209.13161v2), Theorems 1–3,
provides the main baseline. Its indicator reduction covers convex submodular
objectives and general coordinate activation intervals. Its quadratic
extension applies when diagonal sign switching makes every off-diagonal
coefficient nonpositive. The graphical criterion contracts negative-edge
components and requires the resulting positive-edge graph to be bipartite.
Positive edges whose endpoints contract together must remain as loops and
must obstruct bipartiteness. The latest inspected version is dated
2025-07-08; arXiv:2507.00442 is superseded by this canonical submission.

For exactly one positive pair \(\{a,b\}\), the sign criterion has a simple
equivalent form: \(a,b\) lie in different connected components of the
negative-edge graph. To see this directly, signs must agree along every
negative edge and must disagree across the positive edge. These requirements
are consistent exactly when no negative-edge path connects its endpoints.
Thus the unsolved boundary **in this investigation** is one positive edge
whose endpoints are connected by a negative-edge path. It is essential to
exclude the already solved sign-switchable case from any novelty claim.

## Nearby results and why they do not settle the target

| Source examined | Relevant conclusion | Boundary of comparison |
| --- | --- | --- |
| [Ganian, Ramanujan, and Szeider, *Backdoors to Tractable Valued CSP*, CP 2016](https://arxiv.org/abs/1612.05733) | Fixed-parameter tractability by the size of a strong backdoor into tractable valued constraint languages of finite arity and finite domain. | Fixing exceptional **continuous** coordinates is not finite-domain enumeration. The result does not turn a small continuous separator into an exact algorithm. |
| [Kawahara, Iyer, and Bilmes, *On Approximate Non-submodular Minimization via Tree-Structured Supermodularity*, AISTATS 2015](https://proceedings.mlr.press/v38/kawahara15.html) | A binary submodular function plus tree-structured pairwise supermodularity is NP-hard in general; the paper develops approximation methods and bounds. | A tree can have arbitrarily many positive pairs. For a fixed number of binary exceptional variables, direct assignment enumeration applies. This is not one-positive-edge continuous-indicator hardness. |
| [Gómez, He, and Pang, *Linear-step solvability of some folded concave and singly-parametric sparse optimization problems*](https://par.nsf.gov/servlets/purl/10334383) | Polynomial algorithms under Z-type assumptions find directional stationary points for folded-concave sparsity; related parameter paths concern weighted \(\ell_1\) models and suitable hidden Z conditions. | Stationarity for a sparsity surrogate is not global exact \(\ell_0\) optimization. The parameter-path theorem cannot be used without its sign and weight assumptions. |
| [He, Han, Gómez, Cui, and Pang, *Comparing solution paths of sparse quadratic minimization with a Stieltjes matrix*](https://doi.org/10.1007/s10107-023-01966-0) | Studies exact sparsity, convex sparsity, and capped-sparsity parameter paths, with distinct global and local guarantees. | A path parameter multiplying the sparsity penalty is not a positive-interaction parameter or an exceptional continuous coordinate. |
| [Gómez, Han, and Lozano, *Real-time solution of quadratic optimization problems with banded matrices and indicator variables*](https://arxiv.org/abs/2405.03051), also in the local literature folder | Decision diagrams exploit banded matrices; truncation gives approximation guarantees under fixed bandwidth and conditioning. | Bandwidth is a different parameter. The inspected local record does not supply an exact algorithm for arbitrary dense negative interactions plus one positive pair. |
| [Allman, Lo, and McCormick, *Complexity of Source-Sink Monotone 2-Parameter Min Cut*](https://arxiv.org/abs/2107.09743) | Two monotone parameters can expose exponentially many distinct minimum cuts. | This is an obstruction to an automatic small path dictionary, not a hardness theorem for the target. The local September 27 audit already records the large encoding size of the construction. |

The last two rows were checked against local material and the authors' primary
records. The other rows were checked on the linked primary pages or accessible
manuscripts. No surveyed result supplies an exact fixed-parameter algorithm
for the target simply from a fixed number of exceptional coordinates.

## Why branching on exceptional indicators is insufficient

The following example is an independent elementary calculation, included to
rule out a tempting proof step. It does not rule out other algorithms.

Let

\[
 Q=\begin{pmatrix}
 3&1&-1\\
 1&3&-1/10\\
 -1&-1/10&3
 \end{pmatrix},\qquad b=(3,2,0)^T,
 \qquad c=0,\qquad u_i=+\infty.
\]

The leading principal minors are \(3,8,2117/100\), so \(Q\succ0\).
There is exactly one positive pair, \(\{1,2\}\), and \(\{1\}\) covers
every positive pair. Fix \(z_1=1\), but optimize \(x_1\) continuously.
For \(S\subseteq\{2,3\}\), let \(v(S)\) be the minimum with only
coordinates \(\{1\}\cup S\) available. Exact unconstrained minimizers
on all four fibers are nonnegative, and the values are

| \(S\) | Nonzero-coordinate minimizer | \(v(S)\) |
| --- | --- | --- |
| \(\varnothing\) | \(x_1=1\) | \(-3\) |
| \(\{2\}\) | \((x_1,x_2)=(7/8,3/8)\) | \(-27/8\) |
| \(\{3\}\) | \((x_1,x_3)=(9/8,3/8)\) | \(-27/8\) |
| \(\{2,3\}\) | \((x_1,x_2,x_3)=(1,10/29,10/29)\) | \(-107/29\) |

Consequently,

\[
 v(\{2\})+v(\{3\})-v(\varnothing)-v(\{2,3\})
 =-\frac7{116}<0,
\]

which violates submodularity. Algebraically, eliminating coordinate 1 creates
the Schur-complement coefficient

\[
 Q_{23}-Q_{21}Q_{13}/Q_{11}=-1/10+1/3=7/30>0.
\]

The reduced Hessian on coordinates 2 and 3 is
\(\left(\begin{smallmatrix}8/3&7/30\\7/30&8/3\end{smallmatrix}\right)\),
and the reduced linear vector is \((1,1)\). The nonnegative constraint on
coordinate 1 does not interfere with the displayed minimizing points.

This example disproves only the claim that fixing the positive-edge-cover
**indicators** restores a submodular value function on the other indicators.
Fixing the corresponding **continuous values** does remove every positive
interaction in the remaining continuous variables. Exact optimization over
those continuous values is the additional difficulty.

## Search record and research consequence

Searches included combinations of: indicator quadratic positive NP-hard
Stieltjes; one positive edge; few positive off-diagonal entries;
non-submodular variables; continuous submodular backdoor; parameterized
indicator quadratic; sparse quadratic solution paths; and parametric
minimum cut with nonmonotone parameters. Generic indefinite-QP hardness,
fixed-charge network-flow hardness with coupling constraints, and
pseudo-Boolean roof-duality results were not treated as answers to the
specific target.

The exact one-edge question remains worthwhile as a clean boundary question,
but an algorithm for it would need more than the existing scalar AM–GM
majorant identity or fixed-dimensional gridding. Both are already recorded in
[the September 27 note](../../research-20260927/free-frontier.md). Conversely,
many optimal parameter supports alone would not prove hardness. A substantial
result should supply either a bit-polynomial exact algorithm or a reduction
that respects positive definiteness, one positive pair, nonnegative
coordinate boxes, and the absence of coupling constraints.

## Verification

The four quadratic fiber minima, the leading principal minors, and the
submodularity defect were recomputed using exact SymPy rational arithmetic.
The command actually run was a targeted `python` heredoc importing SymPy,
forming the displayed rational matrix, and evaluating
`Q.extract(A,A).inv()*b.extract(A,[0])` and the resulting objective for
`A=(0,)`, `(0,1)`, `(0,2)`, `(0,1,2)`. It returned exactly the values above.
This computation checks the arithmetic of the counterexample. The
positive-definiteness argument and the inference from the four values are
mathematical, not a numerical tolerance test. No project-wide verification or
CI inspection was performed. The fresh reviewer `/root/close_scope_audit`
subsequently checked the three principal minors, all four stationarity
equations, nonnegative minimizers, objective values, and defect by hand,
finding no error. The coordinating author independently rechecked the full
three-coordinate stationarity equations, determinant, and defect. The
[closure audit](../closure-audit.md) records the review's narrow scope.
This completes verification of this supporting example, without resolving
the broader one-positive-edge complexity question.
