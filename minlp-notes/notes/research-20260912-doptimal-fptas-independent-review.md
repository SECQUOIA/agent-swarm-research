# Independent review of the fixed-dimension determinant approximation scheme

**The theorem passes fresh mathematical review.** The algorithm in [the candidate note](research-20260912-fixed-parameter-doptimal-fptas.md) is a deterministic FPTAS for maximizing the determinant of a sum of explicitly encoded rational PSD edge matrices and a rational PSD prior along a path in an explicit DAG, when the matrix dimension is fixed. The noisy full-block D-optimality corollary also follows under its stated fixed contraction and signal-to-noise promises. No proof correction was required.

This endorsement concerns correctness, including rational bit complexity. It does not establish priority or practical computational value. The full approximation scheme has not been implemented. Its degree in graph size and inverse accuracy depends strongly on the fixed information dimension. The result is not a fixed-parameter tractability claim with an exponent independent of that dimension. The prior-work qualifications in the author's note remain necessary.

The PSD factorization step is valid with singular matrices. If a rational PSD residual is nonzero, at least one diagonal entry is positive. Pivoting on that entry subtracts a positive rational multiple of a rational vector outer product and leaves a PSD Schur complement embedded in the original coordinates. The rank decreases. If every diagonal entry is zero, every off-diagonal entry is zero by the PSD two-by-two principal-minor inequalities. Thus each matrix admits at most \(p\) positive weighted rational factors, without square roots. Fixed-dimensional rational elimination has polynomial bit complexity.

The normalization argument also checks. On an optimal positive-determinant path, consider the finite collection of weighted real factors \(u_j=\sqrt{w_j}v_j\). A basis of maximum absolute determinant exists. Replacing one basis column by any factor proves that every factor's coordinate in that basis lies in \([-1,1]\). The algorithm need not compare irrational determinants: it enumerates all nonsingular label bases, which includes this proof basis. Even a direct comparison could use the rational squared volume \(\det(V_b)^2\prod_i w_{b_i}\).

For the enumerated proof basis, the rational map \(T=\operatorname{diag}(\tau_i)V_b^{-1}\) sends its weighted factor matrix to a diagonal matrix whose squared diagonal entries lie in \([1,4)\). Such dyadic \(\tau_i\) always exist. The exponent magnitude is bounded by the encoding length of the rational weight. Every transformed factor in the optimal path therefore has coordinate magnitude below 2. Because each edge matrix and the prior contains at most \(p\) factors, their transformed diagonal entries are at most \(4p\). Thus the filter preserves every edge of this path and its prior, and PSD bounds all retained matrix entries in absolute value by \(4p\).

Forcing the distinct edge owners of the basis factors is sufficient. Several factors can share an owner; traversing that edge includes all of them. Prior factors are already present and need no mask bit. The maximum-volume path satisfies the owner condition. Its information obeys \(A_*\succeq I\). Any accepted representative also contains the basis factors, although the approximation proof needs only the lower bound on \(A_*\). Edges of a DAG cannot be reused. The owner mask therefore records every required feature of the path prefix beyond the graph vertex and label sum.

The label argument correctly handles signed off-diagonal entries and paths of different lengths. Exact floor, including for negative inputs, gives a remainder in \([0,h)\) for each edge and matrix coordinate. The sum of remainders on any path lies in \([0,Nh)\). Two paths with the same integer label sum differ by less than \(Nh\) in every matrix coordinate, since the unrounded prior cancels. Their symmetric difference matrix has operator norm at most \(pNh=\eta/p\). Consequently

\[
A_{\rm rep}\succeq A_*-(\eta/p)I
\succeq (1-\eta/p)A_*.
\]

The final inequality uses \(A_*\succeq I\) with the correct direction. The determinant comparison and Bernoulli's inequality yield the factor \((1-\eta/p)^p\ge1-\eta\). Since the DAG is processed in topological order, replacing a prefix by another prefix at the same recorded state preserves all future reachable states and owner requirements. The proof does not require keeping the best true determinant at an intermediate state.

The zero-optimum fallback is sound. If any feasible path has positive determinant, its factors span the parameter space and provide the maximum-volume basis just analyzed. That basis must produce an accepted terminal representative. Therefore absence of a terminal representative for every enumerated basis implies that all feasible information matrices are singular. Any initially found path then satisfies the determinant guarantee. No lower bound on a positive optimum or on a prior eigenvalue is used.

The full Turing complexity claim follows from the stated explicit input model. There are at most \([p(|E|+1)]^p\) basis trials. For fixed \(p\), each trial has a constant-size owner mask and \(p(p+1)/2\) integer label coordinates, each in an interval of polynomial length in graph size and \(1/\eta\). The provided state bound is conservative and valid for signed coordinates. Rational factorizations, transformations, floors, path sums, and determinant comparisons have polynomial bit length. In particular, a path sum involves at most \(N\) input edge matrices, so a product of their denominators supplies a common denominator with polynomial encoding length. Very poor floating-point conditioning does not change this argument. Graph construction for arbitrary side constraints is outside the theorem; an exponentially large graph or a budget expanded from a binary-encoded number cannot be treated as polynomial input implicitly.

The noisy full-block composition preserves these conditions. Under the separately reviewed rational model promises, local conditional covariance matrices are positive definite and produce rational PSD information increments. Their dimensions and bit lengths are polynomial in the original input and memory length. A history length logarithmic in inverse accuracy gives an explicit graph of polynomial size when \(\rho_0\), \(B_0\), and \(p\) are fixed. The graph approximation has \(\eta=\epsilon/2\), while the memory comparison has \(\delta\le\epsilon/(4p)\), giving

\[
\det J(\widehat S)
\ge(1-\epsilon/2)
\left(\frac{1-\delta}{1+\delta}\right)^p
\det J(S_*)
\ge(1-\epsilon)\det J(S_*).
\]

Adding a fixed PSD prior preserves the Loewner comparison even if the prior is singular. At full history the exact value \(\delta=0\) applies. A zero optimal determinant needs no special approximation analysis, and a positive optimum remains positive through both comparisons. This is a multiplicative determinant guarantee and a corresponding determinant-root efficiency guarantee; it is not a multiplicative guarantee for a possibly negative log determinant. The block acquisition, rational-sensitivity, fixed-dimension, and fixed-contraction restrictions remain material.

The independent [stress-check script](../code/research_20260912/review_doptimal_fptas_theorem.py) was written for this review. It exhaustively identifies an optimum on small DAGs, obtains the proof's maximum-volume factor basis, and runs that basis's rounded-label dynamic program. This checks the decisive proof iteration without implementing enumeration of all bases. It includes rational rank deficiency, repeated factor owners, different path lengths, parallel edges, negative off-diagonal entries, actual state merging, and coordinate scalings as large as powers \(2^{60}\) and their reciprocals. [Saved results](../code/research_20260912/results/doptimal-fptas-theorem-independent-review.json) report:

- 270 exact PSD factorizations;
- 29 cases with positive optimal determinant and three singular-optimum fallbacks;
- 202 exhaustively enumerated paths, including 14 state merges and three cases with repeated basis owners;
- 678 signed-floor residual checks and 21 rational checks of the composed accuracy factor.

All checks passed. These are proof stress tests, not a performance benchmark or a replacement for the symbolic argument. No independent counterexample was found. Reproduction:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/review_doptimal_fptas_theorem.py
```
