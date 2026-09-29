# Attractive indicator quadratics: prior art and remaining question

Date: 2026-09-27. Status: literature scout; the broad tractability route is
occupied. The small obstruction below is an auxiliary observation, not a
proposed main contribution.

Consider

\[
\min\{x^TQx+c^Tx+\lambda^Tz:
       x_i(1-z_i)=0,\quad z\in\{0,1\}^n\},\qquad Q\succ0.
\]

## Prior results directly covering the initial ideas

- Atamtürk and Gómez, [*Strong formulations for quadratic optimization with
  M-matrices and semi-continuous variables*, 2018 manuscript, Proposition 3](https://optimization-online.org/wp-content/uploads/2018/02/6445.pdf).
  For a positive definite M-matrix and a one-sign continuous linear term,
  optimization reduces to minimizing the submodular support function
  \(\lambda(S)-c_S^TQ_{SS}^{-1}c_S/4\). The proof uses entrywise
  supermodularity of embedded inverses of principal submatrices. Thus the
  direct same-sign support theorem is already established.
- Gómez and Han, [*Convex Submodular Minimization with Indicator Variables*,
  arXiv:2209.13161v2, 8 July 2025](https://arxiv.org/html/2209.13161v2),
  Theorems 1–3 and Section 4. Their general lattice reformulation handles
  arbitrary continuous linear terms and signed, possibly infinite activation
  bounds, with a convex submodular objective. When variables can cross zero,
  additional binary variables encode the two signs. Consequently, failure of
  submodularity of the original support function does not imply intractability.
  Their quadratic result also covers every matrix made Stieltjes by diagonal
  sign changes. The graph formulation contracts negative edges and requires
  the resulting graph to be bipartite; positive loops must be retained as
  obstructions. The stated strongly polynomial conclusion depends on the
  corresponding continuous oracle. Sections 5–6 additionally develop and
  evaluate a parametric extreme-base method.
- Liu, Atamtürk, Gómez and Küçükyavuz, [*Polyhedral analysis of quadratic
  optimization problems with Stieltjes matrices and indicators*, published
  online 27 August 2025](https://link.springer.com/article/10.1007/s10107-025-02272-7).
  This is the closest convexification comparison: it studies an inverse-matrix
  polyhedral relaxation and its exactness under a same-sign continuous linear
  objective. It is not a blanket assertion that the entire indicator epigraph
  hull has an easy explicit formulation.

The one-sign extension and the balanced signed-Hessian extension should
therefore be rejected as research contributions. The 2025 version of Gómez–Han
is materially stronger than its older same-sign antecedents and must be used
when stating the frontier.

## A possible question beyond the occupied class

After an optimal or supplied diagonal sign change, suppose only \(k\)
off-diagonal entries remain positive. Is there an exact algorithm with
parameter dependence isolated in \(k\), or is there hardness for fixed \(k\)?
Neither answer was located in this limited search. This is a question, not a
novelty or open-problem claim. The local
[bandwidth-two hardness](../results/indicator-quadratic-treewidth-two-hardness.md)
uses a chain of frustrated triangles and does not settle bounded \(k\).

One must not transfer the familiar binary-energy enumeration argument without
accounting for the continuous variables. Fixing indicators of exceptional
vertices to one leaves their continuous values free. Eliminating those values
can produce new sign conflicts.

Here is an exact example. Set \(a=1/10\) and

\[
Q=\begin{pmatrix}
1&a&-a&-a\\
a&1&-2a^2&0\\
-a&-2a^2&1&0\\
-a&0&0&1
\end{pmatrix}.
\]

The matrix is symmetric and strictly diagonally dominant with positive
diagonal, so it is positive definite. It has exactly one positive
off-diagonal edge. Removing coordinate zero leaves a Stieltjes matrix.
Eliminating coordinate zero, however, gives the Schur complement

\[
R=\begin{pmatrix}
99/100&-1/100&1/100\\
-1/100&99/100&-1/100\\
1/100&-1/100&99/100
\end{pmatrix}.
\]

The product of its three edge signs is positive. Diagonal sign changes
preserve this product, whereas three negative edges have negative product.
Thus \(R\) is not sign-switchable to Stieltjes. This disproves the proposed
closure property, without establishing hardness.

A separate elementary observation is that a single cycle graph is tractable:
either every indicator is one, giving one convex QP, or some chosen vertex is
inactive, leaving a forest. Enumerating the inactive vertex and using an
existing forest algorithm gives a polynomial algorithm. This limited case is
too elementary to serve as the main research advance, and its priority was
not established.

## Search and verification record

Primary full texts inspected: Atamtürk–Gómez Section 3.1;
Gómez–Han Sections 1, 2 and 4–5; Liu et al. introduction and exactness
discussion. Local files inspected included the bandwidth-two hardness result,
the 2026-09-22 frontier scout, and the 2026-09-25 integer-structure exploration.
Queries included `quadratic optimization indicator variables M-matrix
submodular minimization`, `Stieltjes matrix indicator quadratic optimization
submodular`, `quadratic indicator frustration`, `quadratic indicator variables
cycle graph`, `convex quadratic indicators feedback`, and `Stieltjes
parameterized`. Search results on discrete MRF frustration supplied no
continuous-indicator parameter theorem. An unsuccessful search is not evidence
of novelty.

Targeted verification: a Python/SymPy exact-rational calculation constructed
the displayed matrix, checked its four leading principal minors, and asserted
the three Schur-complement off-diagonals. The minors were
\(1,99/100,49/50,242501/250000\); the triangle product was \(1/10^6\).
This verifies the arithmetic of the counterexample. The sign-invariance
argument is proved above. No project-wide checks or CI inspection were run.
