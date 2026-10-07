# Exact support for general small quadratic blocks

The new oracle computes the exact minimum of any rational quadratic over a
bounded rational polytope. This extends the preceding implementation from
two-variable blocks and constrained stars to general small blocks, including
cycles, constraints that couple several leaves, and lower-dimensional domains.
The integration attempts this algorithm in dimension at most four and only
when its complete enumeration fits a fixed work budget.

This is an implementation and certification extension. Face enumeration for
quadratic programming is classical: [Murty's textbook, Section 2.9,
pages 163–166](https://public.websites.umich.edu/~murty/books/linear_complementarity_webbook/lcp-complete.pdf)
describes total face enumeration and credits earlier work. The rational
certificate structure of quadratic programming also appears in
[Vavasis (1990)](https://doi.org/10.1016/0020-0190(90)90100-C). The proof below
is included to make the precise degeneracy and replay contracts self-contained;
no priority claim is made for general quadratic optimization by active faces.

## Problem and result

Let

\[
P=\{x\in\mathbb R^d: \ell\le x\le u,\;Ax\le b\},\qquad
q(x)=c_0+c^Tx+\tfrac12x^THx,
\]

where all data are rational, all box endpoints are finite, and \(H\) is
symmetric. The box guarantees boundedness. Reversed box bounds, inconsistent
rows, duplicate rows, zero rows, explicit equalities, and implicit equalities
are allowed. An equality is represented by two opposite inequalities.

**Theorem.** There is a finite algorithm using exact rational arithmetic that
returns either:

- an attained minimum \(q_*\in\mathbb Q\) and minimizer \(x_*\in P\cap\mathbb Q^d\); or
- the conclusion that \(P\) is empty.

For each fixed dimension, the algorithm has polynomial bit complexity in the
rational input size. No positive-definiteness, full-dimensionality, unique
minimizer, or constraint qualification assumption is required.

If graph features \(f_1,\ldots,f_p\) are quadratic polynomials and a rational
direction \(a\) is supplied, apply the theorem to
\(q(x)=\sum_j a_jf_j(x)\). The result is the exact valid support inequality

\[
\sum_j a_j y_j\ge q_*,\qquad
(x,y)\in\operatorname{conv}\{(x,f(x)):x\in P\}.
\]

Linear terms in \(x\) may be included among the features. The oracle computes
support for a supplied direction. Finding a useful separating direction is a
separate task, handled by the new separation code.

## Algorithm

Append the box inequalities to \(Ax\le b\), producing \(\bar A x\le\bar b\)
with \(m\) rows. For every subset \(S\) of at most \(d\) rows, form

\[
K_S=
\begin{pmatrix}
H&\bar A_S^T\\
\bar A_S&0
\end{pmatrix}.
\]

If \(K_S\) is nonsingular, solve exactly

\[
K_S
\begin{pmatrix}x\\\lambda\end{pmatrix}
=
\begin{pmatrix}-c\\\bar b_S\end{pmatrix}.
\]

Retain \(x\) if every inequality \(\bar A x\le\bar b\) holds exactly.
Finally, evaluate \(q\) at every retained point and choose its smallest value.
An empty candidate set certifies that the bounded polytope is empty.

The multipliers are unrestricted because these systems express stationarity on
an affine face. The algorithm does not filter on multiplier signs. It also
does not need to test the restricted Hessian for positive definiteness: extra
feasible saddle points or maxima cannot reduce the minimum below the true
minimum. Singular systems are skipped in their entirety; completeness follows
from the next argument, not from choosing an arbitrary solution of a singular
system.

## Why every minimum is covered by some candidate

Suppose \(P\) is nonempty. Compactness gives a global minimizer. Choose a
global minimizer \(x_*\) whose smallest containing face \(F\) has minimum
dimension among all global minimizers. The point lies in the relative interior
of \(F\). Write \(T\) for the tangent space of \(\operatorname{aff}F\).
Relative first- and second-order conditions give

\[
v^T(Hx_*+c)=0,\qquad v^THv\ge0\quad(v\in T).
\]

If the restricted Hessian were singular on a positive-dimensional \(T\),
there would be a nonzero \(v\in T\) with \(v^THv=0\). Expanding the
quadratic along that line yields

\[
q(x_*+tv)=q(x_*)+t\,v^T(Hx_*+c)+\tfrac12t^2v^THv=q(x_*).
\]

The intersection of this line with the compact face is a nontrivial closed
segment. Its endpoints belong to proper faces of \(F\), and are also global
minimizers. This contradicts the choice of \(F\). Thus the restricted Hessian
is positive definite, except at a vertex where the tangent space is zero.

Choose independent active row normals spanning the orthogonal complement of
\(T\); they form an enumerated subset \(S\), of size at most \(d\), with
\(\ker\bar A_S=T\). Relative stationarity gives a multiplier solving the
displayed system. To prove that the system is nonsingular, suppose

\[
Hv+\bar A_S^T\mu=0,\qquad\bar A_Sv=0.
\]

Then \(v\in T\) and multiplication of the first equation by \(v^T\)
gives \(v^THv=0\). Positive definiteness on \(T\), or \(T=\{0\}\), gives
\(v=0\); row independence gives \(\mu=0\). The enumerated nonsingular system
therefore returns \(x_*\).

Every retained candidate is feasible and at least one is a global minimizer,
so their minimum is exact. This also proves that a nonempty bounded domain
cannot produce an empty candidate list. Constant objectives and flat valleys
eventually reach vertices or smaller faces in this proof. Singular ambient
Hessians and lower-dimensional feasible sets require no separate numerical
rank tolerance.

## Complexity and the dimension boundary

The number of row subsets is

\[
N(m,d)=\sum_{k=0}^{d}\binom{m}{k}.
\]

Each linear system has order at most \(2d\). Exact Gaussian elimination,
feasibility checking, and objective evaluation use
\(O(d^3+md)\) rational arithmetic operations per subset. The resulting bound
is \(O(N(m,d)(d^3+md))\). In fixed dimension this is polynomial in the input
size. Determinant bounds control the bit length of the rational solutions and
objective values by a polynomial in the rational input length and \(d\), so
this is a bit-complexity claim, not merely a count of unit-cost real operations.
The dependence on the dimension remains combinatorial.

There is a direct hardness boundary even for multilinear quadratic objectives
over a box, without extra affine rows. For a graph \(G=(V,E)\) with
nonnegative rational edge weights, minimize

\[
q(x)=-\sum_{\{i,j\}\in E}w_{ij}(x_i+x_j-2x_ix_j),
\qquad x\in[0,1]^{|V|}.
\]

Fixing all other coordinates makes this objective affine in each coordinate.
Moving one coordinate at a time to a minimizing endpoint never increases the
objective, so some global minimizer is Boolean. At a Boolean point the
parenthesized expression is one exactly when the edge crosses the associated
cut. Therefore \(\min q\) is the negative maximum cut weight. Since Max-Cut
is NP-hard, a polynomial-time exact oracle for arbitrary block dimension would
imply \(\mathrm P=\mathrm{NP}\). The small-dimension algorithm and the earlier
structured-star algorithm provide useful tractable restrictions; they cannot
justify a universal polynomial-time promise for arbitrary overlapping blocks.
This is consistent with the classical hardness literature, including
[Pardalos and Vavasis (1991)](https://doi.org/10.1007/BF00120662).

## API, work limits, and replay

[quadratic_polytope.py](quadratic_polytope.py) exports:

- `support_quadratic(bounds, rows, coefficients, max_faces=None)`;
- `replay_quadratic(bounds, rows, coefficients, certificate, max_faces=None)`;
- `polytope_vertices(bounds, rows=(), max_faces=None)`;
- `enumeration_size(dimension, row_count)` and `coefficient_pairs(dimension)`.

The keyword-only arguments are shown without a `*` here for readability.
Coefficients are ordered as the constant, all linear terms, and then quadratic
terms \((i,j)\), \(0\le i\le j<d\), in lexicographic order. Rows contain
\(d\) coefficients followed by the right-hand side. Python floats denote
their exact binary rational values. Vertex enumeration returns exact
`Fraction` coordinates, including segment endpoints and singleton domains.

`max_faces` checks the complete subset count **before** enumeration. If the
budget is too small, the producer raises `EnumerationLimitError` and returns
no support claim. A minimum over only some feasible candidates would be an
upper bound on the true minimum and would be unsafe as a support cut. The
implementation never uses such a partial list as a lower bound.

A complete witness records the original rational problem, enumeration counts,
all distinct feasible stationary candidates, one defining active subset per
candidate, the attained minimum, and a minimizing point. Replay uses trusted
caller-supplied bounds, rows, and coefficients to repeat **all** subsets, then
compares the entire reconstructed witness. Omitting a candidate, changing a
row, or replacing the objective is rejected. The checker shares the exact
enumeration primitives with the producer. It is independent of numerical
direction search, but is neither a second implementation nor a formally
verified proof checker.

[The solver wrapper](../solver/support.py) reuses the preceding typed
expression binding, validates every original polynomial tree before combining
features, converts proposed direction coefficients to their actual binary64
values, and then performs rational support. Its default admission limits are
dimension four and 5,000 subsets. If enumeration is refused, it tries the
existing supported kernels; these may return `unsupported` or `incomplete`.
The wrapper rounds the support intercept downward and tests any requested
separation target against that **exported** intercept. An unmet target returns
no cut, while keeping the exact minimizer in diagnostic statistics for use by
the direction search. Replay checks the typed binding, complete exact support,
and exported intercept against the original model supplied by its caller.

These cut certificates do not certify SCIP's full numerical solve, its
presolve transformations, or the correctness of arbitrary expression imports.
Native-model binding and final elimination/rounding of exported rows are
additional integration contracts.

## Verification performed

The targeted command

```sh
PYTHONPATH=research-20261003-convexification \
  code/minlp_solver_lab/.venv/bin/python -m pytest -q \
  research-20261003-convexification/theory/test_quadratic_polytope.py \
  research-20261003-convexification/solver/test_support.py
```

passed all 34 tests. These cover known exact minima in dimensions one to four,
coupled simplex faces, singular flat valleys, lower-dimensional and empty
domains, random comparison with the separate two-dimensional geometric
oracle, a non-star multilinear block, exact binary input semantics, tiny
curvature, duplicate rows, work-budget boundaries, certificate mutation,
expression/row binding, target rounding, and legacy fallback behavior.

An [independent review](polytope-review.md) also passed 40 separate
analytic and adversarial diagnostics, including affine simplex images, skew
equality domains, exhaustive Boolean Max-Cut controls, and witness corruption.
The review records source hashes and its exact command. These are targeted
local checks; no project-wide verification or CI status inspection was used.
