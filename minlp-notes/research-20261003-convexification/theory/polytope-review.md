# Independent review of exact quadratic support on a bounded polytope

This review checks the active-face enumeration separately from the
implementation author. The algorithm is mathematically complete for a bounded
rational polytope. Source inspection and 40 independent diagnostics found no
correctness blocker in the reviewed version.

## Candidate completeness

Write the objective as

\[
q(x)=\tfrac12 x^T Hx+c^Tx+c_0,
\qquad P=\{x\in\mathbb R^d:Ax\le b\},
\]

where \(H\) is symmetric and \(P\) is bounded. The proposed enumeration considers
every subset \(S\) of at most \(d\) rows. For each nonsingular system

\[
\begin{pmatrix}H&A_S^T\\A_S&0\end{pmatrix}
\begin{pmatrix}x\\\lambda\end{pmatrix}
=\begin{pmatrix}-c\\b_S\end{pmatrix},
\]

it retains \(x\) if all inequalities defining \(P\) hold exactly. Multipliers in
this face-stationarity system are unrestricted. Filtering candidates by a
multiplier sign is unnecessary for the completeness argument.

If \(P\) is nonempty, compactness gives a global minimizer. Among all global
minimizers choose \(x_*\) whose minimal containing face \(F\) has the smallest
dimension. The point \(x_*\) lies in the relative interior of \(F\). Let \(T\)
be the tangent space of its affine hull. Relative first- and second-order
necessary conditions give

\[
v^T(Hx_*+c)=0,\qquad v^THv\ge0\quad (v\in T).
\]

If the restricted Hessian is singular and \(\dim F>0\), it has a nonzero null
direction \(v\in T\). Thus \(q(x_*+tv)=q(x_*)\) for every real \(t\). The line
meets the compact face in a bounded interval with \(x_*\) in its relative
interior. An endpoint belongs to a proper face of \(F\) and is another global
minimizer, contradicting the choice of \(F\). Therefore the restricted Hessian
is positive definite when the face has positive dimension. The zero-dimensional
case is a vertex.

Choose a linearly independent basis \(S\) of the rows active at \(x_*\). It has
at most \(d\) rows and \(\ker A_S=T\). The saddle matrix above is nonsingular:
in a homogeneous solution, multiplication of its first equation by \(x^T\)
gives \(x^THx=0\), while its second equation gives \(x\in T\). Positive
definiteness on \(T\) forces \(x=0\), and row independence forces
\(\lambda=0\). This also holds at a vertex, where \(T=\{0\}\).

Relative stationarity places \(Hx_*+c\) in the row span of \(A_S\), so this
nonsingular system returns \(x_*\). Hence the minimum over retained candidates
is the global minimum. If the candidate list is empty, the bounded polytope is
empty. This argument includes lower-dimensional polytopes, implicit equalities,
singular ambient Hessians, redundant constraints, and constant objectives.

Boundedness is essential to this proof. An API that accepts arbitrary rows must
also establish boundedness or require and enforce finite box bounds. A heuristic
cutoff in subset enumeration cannot return an exact optimum or infeasibility.

## Complexity and scope

There are at most \(\sum_{k=0}^{d}\binom{m}{k}\) subsets. Each system has order
at most \(2d\); checking a solution uses all \(m\) inequalities. A direct
implementation therefore uses
\(O(m^d(d^3+md))\) rational arithmetic operations for fixed \(d\), with the
usual harmless adjustments when \(m<d\). Exact Gaussian elimination or
determinant bounds give polynomial encoding length for each solution and for
the rational objective value. Thus the algorithm has polynomial bit complexity
for each fixed dimension. This is not a polynomial-time algorithm when the
dimension is part of the input.

For a graph with nonnegative edge weights, minimizing
\(-\sum_{\{i,j\}\in E} w_{ij}(x_i-x_j)^2\) on \([0,1]^d\) gives the negative
maximum cut weight. This concave quadratic attains a minimum at a box vertex,
where the expression counts crossing edges. This direct reduction explains why
unrestricted dimension is a computational boundary, even before general
nonlinear expressions are admitted. General quadratic-programming complexity
is also covered by [Vavasis (1990)](https://doi.org/10.1016/0020-0190(90)90100-C)
and [Pardalos and Vavasis (1991)](https://doi.org/10.1007/BF00120662).

## Prior work

Face enumeration for general quadratic programming is classical. The
author-hosted [Murty textbook, Internet edition (1997), Section 2.9,
pages 163–166](https://public.websites.umich.edu/~murty/books/linear_complementarity_webbook/lcp-complete.pdf)
describes recursive restriction to active faces and credits Murty's 1971
technical report 71-5 and Mueller's 1970 boundary result. Its treatment also
eliminates explicit and implicit equalities. The present construction gives a
direct rational implementation and replay contract for small graph-support
problems; the general face-enumeration principle is not a novelty claim.

## Implementation review

The implementation uses finite rational box bounds, so it enforces boundedness
without relying on a caller's claim about general linear rows. Bounds may be
reversed; in that case full enumeration correctly returns an empty domain. All
rank decisions, solves, feasibility comparisons, and objective evaluations use
`Fraction`. The Hessian doubles diagonal monomial coefficients and copies each
mixed coefficient symmetrically, matching the displayed objective convention.
Dependent row subsets are rejected through singularity of the full stationarity
system. Candidate deduplication retains one active set per exact point and does
not remove any objective value.

The work budget is checked against the complete subset count before enumeration.
Exceeding it raises `EnumerationLimitError`, rather than returning a truncated
minimum. Replay recomputes the full result using trusted bounds, rows, and
coefficients, and compares it with the supplied witness. This is independent of
the numerical direction search, but shares the exact enumeration implementation
with the producer. It is not a separately implemented or formally verified
mathematical checker.

The separate [diagnostic script](check_polytope_review.py) obtains expected
optima from analytic constructions and exhaustive Boolean MaxCut evaluation.
It does not duplicate active-face enumeration. Its 40 diagnostic cases cover:

- rank-deficient flat valleys and indefinite objectives constant on a line;
- skew equality domains with singular or indefinite ambient Hessians;
- a singleton defined by coupled equalities;
- invertible rational affine images of a simplex, with interior, proper-face,
  vertex, concave, and nonunique minima, plus duplicate and scaled rows;
- 12 weighted MaxCut examples in dimensions three and four;
- a width-zero feasible interval and inconsistent rows separated by
  \(2^{-200}\), a contradictory zero row, and reversed bounds;
- 12 witness corruptions, trusted-input changes, and the exact enumeration
  budget boundary.

Targeted command actually run:

```sh
code/minlp_solver_lab/.venv/bin/python research-20261003-convexification/theory/check_polytope_review.py
```

Result: all 40 diagnostics passed, exit code 0. No project-wide checks or CI
inspection were performed for this review. Reviewed source SHA-256:

```text
quadratic_polytope.py
4fffd2f5bb9b529e98b68ab1bd150083a24a9d5ee0c4fc122516bd82aab30a7b

check_polytope_review.py
36a1fc081a65e9e64b9c512f776e91a4c283f52aeaaa802584b08d93956e1908
```

These checks establish evidence for the stated bounded quadratic contract. They
do not establish numerical SCIP solve certificates, a practical speedup, or
complete separation over more general expression graphs.
