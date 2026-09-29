# Independent review of the forest moment hull

Review date: 2026-09-27. Reviewed files:
[binary-separator-forest-hull.md](binary-separator-forest-hull.md) and
[binary-leaf-star-hull.md](binary-leaf-star-hull.md).

The forest theorem and its box-quadratic corollary pass this independent
analytic audit. I found no gap in the block incidence argument, conditional
gluing, projection argument, or diagonal replacement. A fresh subordinate
review of the complete star proof also found no gap. These reviews are
evidence of correctness, not formal verification or a determination of
priority.

## What the proof actually establishes

Let the retained coordinates be all first moments, the squares at vertices
in the stable set \(C\), and the products on forest edges. The theorem
establishes an exact convex hull in all these coordinates simultaneously.
It is stronger than equality of one selected objective value. It does not
preserve a given choice of auxiliary nonedge products or squares outside
\(C\).

There is a useful immediate strengthening. In the full SDP–RLT system,
the equalities \(X_{bb}=\mu_b\), \(b\notin C\), are optional for this
projection. Raising these diagonal entries to their first moments adds a
nonnegative diagonal matrix to the moment matrix. It preserves PSD and
every RLT inequality, and changes no retained coordinate. Thus the full
system and its binary-diagonal face have the same retained projection.

Furthermore, the mixed binary hull in the note equals

\[
\operatorname{conv}\left\{
\big((x_i)_{i\in V},(x_c^2)_{c\in C},(x_ix_j)_{ij\in E}\big):
x\in[0,1]^V\right\}.
\]

For any fixed continuous point, keep \(x_C\) fixed and replace each
\(x_b\), \(b\notin C\), by an independent Bernoulli variable of mean
\(x_b\). This preserves each retained first moment, square, and edge
product, including binary–binary edges. The reverse inclusion follows from
domain inclusion. This endpoint-rounding identity itself does not require
a forest; the SDP exactness does.

This observation does not extend the theorem to the full quadratic graph
hull retaining all vertex squares. In particular, endpoint rounding changes
an omitted square from \(x_b^2\) to \(x_b\). The positive-square epigraph
hull is obtained by adding nonnegative slack in the retained square
coordinates. Negative-loop hypograph coordinates can instead be introduced
as \(z_{bb}\leq\mu_b\); this uses endpoint rounding and downward slack,
not preservation of the original square coordinate.

## Audit of gluing and size

The incidence graph has precisely one node for each original binary vertex,
one star-bag node for each original continuous vertex, and one edge-bag node
for each binary–binary edge. Each continuous–binary edge becomes one
incidence edge. Each binary–binary edge becomes a path of length two.
Because \(C\) is stable, there is no other original edge type. Relabeling
continuous vertices and subdividing binary–binary edges therefore gives the
incidence graph exactly. No hidden cycle is introduced.

In a rooted incidence component, an unprocessed bag has only one already
processed binary vertex. Two such vertices would give two distinct paths
to the root and hence a cycle. The star theorem supplies a distribution
over every variable of that bag, even though it need not preserve its
leaf–leaf auxiliary moments. Its separator variable has the Bernoulli law
determined by the shared mean. Conditioning on that separator and drawing
the new variables therefore preserves the entire local law. Zero-probability
separator values need no compatibility condition. Isolated binary vertices,
isolated continuous vertices, and disconnected components are covered.

No PSD-completion theorem is being used. The global distribution constructs
a new full moment matrix, whose unretained entries can differ from any
input local or full-matrix auxiliary entries. This is sufficient for the
projection claim. Conversely, a point of the full SDP–RLT face restricts to
the required local blocks, so the local hull result implies the full-system
projection statement.

The size bound is valid. Writing \(d_c=\deg(c)\), stability gives
\(\sum_{c\in C}d_c\leq |E|\). Hence

\[
\sum_{c\in C}(d_c+1)^2
\leq |E|^2+2|E|+|C|=O(|V|^2).
\]

All local PSD matrices together have total order
\(\sum_c(d_c+2)\leq |E|+2|C|=O(|V|)\), although the number of scalar
matrix entries can be quadratic. The distribution obtained by direct
conditional multiplication can have many atoms. Carathéodory's theorem
gives a representation with at most \(|V|+|C|+|E|+1\) atoms in the retained
space, but this observation alone is not an efficient extraction algorithm.

The continuous box-objective corollary has the correct inequality direction:
raising diagonals at coefficients \(d_b\leq0\) cannot increase the
linearized objective. The modified point has a representing mixed binary
distribution, whose expectation is at least the full-box minimum. The
original relaxation point therefore also has value at least that minimum.

## Fresh check of the star dependency

The reviewer `/root/forest_hull_review/star_core_recheck` independently
checked both threshold corrections and the separation argument. In the
lower correction, \(\tau<1\) implies \(k_i'>e_i\), and every changed
hinge is active above \(\tau\). In the upper correction,
\(0\leq\gamma_i<e_i\) preserves the strict leaf inequalities and leaves
the lower-end condition intact. Boundary leaves, zero interactions,
\(a=0\), clipping equalities, and the empty star are all covered by the
stated branches. Compactness and exactness for every retained affine
functional justify the hull conclusion. This was an analytic review;
unchanged numerical suites were not repeated.

## A precise obstruction outside the forest class

The forest hypothesis cannot simply be deleted, even from the full
SDP–RLT projection theorem and even when \(C=\varnothing\). On a triangle
with three binary vertices, set every first moment to \(1/2\), every
diagonal to \(1/2\), and every off-diagonal product to \(1/8\). The full
moment matrix is

\[
Y=\begin{pmatrix}
1&1/2&1/2&1/2\\
1/2&1/2&1/8&1/8\\
1/2&1/8&1/2&1/8\\
1/2&1/8&1/8&1/2
\end{pmatrix}.
\]

Its eigenvalues are \(7/4,3/8,3/8,0\), and every RLT inequality holds.
But the binary-valid inequality

\[
1-\sum_{i=1}^3\mu_i+\sum_{1\leq i<j\leq3}X_{ij}\geq0
\]

has value \(-1/8\). At a binary point with \(k\) ones its left side is
\((k-1)(k-2)/2\geq0\). This is the familiar Boolean triangle inequality,
used here only as an explicit limitation. Global PSD does not by itself
repair cyclic incompatibility of local marginals.

## Literature and significance

I directly inspected Khajavirad's
[*Tight semidefinite programming relaxations for sparse box-constrained
quadratic programs*, v2](https://arxiv.org/html/2601.18545v2), Lemma 4,
Theorem 6, and Corollary 2. Its separator decomposition is established
prior work. Its stated polynomial-size SDP and SOC results impose
logarithmic positive-loop degree bounds; the relevant sets use one-sided
square coordinates. The present result removes that degree bound on
forests with stable positive-loop vertices for an SDP formulation. It does
not provide a polynomial-size SOC formulation or cover all of that paper's
bounded-treewidth graphs.

I also directly inspected Dey and Khajavirad's
[*A second-order cone representable class of nonconvex quadratic programs*,
v2](https://arxiv.org/html/2508.18435v2), Proposition 8 and its proof.
That result gives a polynomial-size SOC formulation for forests with stable
positive-loop vertices of logarithmic degree. The distinction claimed in
the forest note is accurate relative to this proposition.

The substantial candidate contribution is the arbitrary-size star hull
represented by the existing full SDP–RLT relaxation. The forest theorem is
a consequential application through standard separator gluing. Its exact
retained-coordinate hull can be used as a valid block relaxation inside a
larger MINLP, but arbitrary side constraints can destroy hull exactness.
Numerical performance, efficient atom extraction, and broader application
value remain unestablished. This review does not claim a new complexity
classification. Broader searches for equivalent mixed binary moment hulls
are still needed before claiming originality.

## Verification record

In addition to the analytic audits, I ran one targeted inline Python/SymPy
check, using `python - <<'PY'`, that constructed the rational triangle
matrix above, checked its exact eigenvalues and all McCormick bounds,
evaluated the displayed inequality, and enumerated its eight binary values.
It returned eigenvalues \(7/4,3/8,3/8,0\), relaxation value \(-1/8\), and
binary minimum zero. This checks the explicit obstruction only; it does
not verify the universal hull theorem. No project-wide verification or CI
inspection was performed.
