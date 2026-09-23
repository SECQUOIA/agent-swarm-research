# Arbitrary polynomial-vector graphs from the implicit knot overlay

Date: 2026-09-05. Status: independently reviewed result; two full proof audits passed.

The [convex-vector implicit overlay](convex-vector-compiled-integer-precision.md)
also gives a polynomial rational construction for arbitrary dense polynomial
outputs, with a logarithmic total-degree penalty. Let the nonlinear outputs
`f_j:[0,1]->R`, `j=1,...,m`, have degrees `D_j>=2`, rational dense coefficients,
and positive rational componentwise tolerances. Affine outputs are retained
exactly without knot arrays. Then

```
p_out<=p_conv+12+ceil(log2(sum_j D_j)).                            (1)
```

The comparator allows every convex general-integer lift of the whole vector
graph, with unrestricted continuous size. The construction is polynomial in
the total dense input and tolerance encoding. If every output is affine, no
integers are needed. No arbitrary coupled error-body claim is made.

## 1. Scalar arrays and their metadata

The reviewed [scalar general-polynomial construction](../results/polynomial-graph-binary-integer-degree-gap.md)
provides an implicit array of cells obtained from rational convexity intervals
and narrow rational root brackets. On a convex or concave interval it uses the
[convex hybrid](../results/convex-polynomial-compiled-integer-precision.md),
negating concave outputs. Greedy knots are increasing, and the canonical
mass-quantile knots are nondecreasing by the search-tree argument in the
convex-vector note. Reverse indices on reflected pieces and concatenate pieces
in original-input order. This gives an ordered array

```
0=a_(j,0)<=...<=a_(j,K_j)=1.
```

Every index returns its rational knot and source-cell type: convex, concave,
or a narrow root bracket. The computation has polynomial bit complexity.

Projection of a vector lift onto output `j`, followed by interval restriction,
never adds integers. The scalar proof thus gives, with `p=p_conv`,

```
K_j<=4096 D_j*2^p.                                                (2)
```

A convex or concave source cell has absolute chord error at most
`13epsilon_j/16`. A bracket has width at most `epsilon_j/(32M_j)`, where the
known rational bound `M_j` is at least `max_[0,1]|f_j'|`. Its absolute chord
error on every subinterval is at most `epsilon_j/16`.

## 2. Merge and localize the source cells

Merge only the right endpoints `a_(j,1),...,a_(j,K_j)` from all arrays,
retaining multiplicity, and prepend one zero. Exactly

```
K=sum_j K_j
```

cells result. The convex-vector note proves that the `k`-th multiset endpoint
is computable exactly by nested index and numerator binary searches on a
common rational grid. Polynomially many rational piece-endpoint denominators
and the maximum local dyadic precision give a common denominator of polynomial
bit length. No cell enumeration or approximate ordering is needed.

Each positive-width merged cell `[a,b]` lies inside a source cell for every
output. Binary search finds the last source knot at most `a`; its successor
is at least `b`, since otherwise another merged knot would lie between them.
At a repeated merged endpoint use any source cell containing that input,
choosing the final source cell at the right domain endpoint if needed. This
also recovers the correct source-cell type for each output separately.

## 3. Bands for different curvature signs on the same cell

Evaluate `f_j` exactly at the two selected rational endpoints, then round with
error at most `epsilon_j/16`. Round downward for convex cells and brackets,
and upward for concave cells. Exact dense-polynomial evaluation and directed
dyadic rounding have polynomial bit complexity. The selected knots may come
from other outputs' arrays; this causes no change to the evaluation argument.

Let `y_j` interpolate the rounded values with one common continuous weight
`theta`. The following bands contain the exact graph:

```
y_j-13epsilon_j/16 <= w_j <= y_j+epsilon_j/8
    for convex cells and brackets,

y_j-epsilon_j/8 <= w_j <= y_j+13epsilon_j/16
    for concave cells.                                           (3)
```

Indeed, on a convex cell, `y_j-f_j(x)` lies in
`[-epsilon_j/16,13epsilon_j/16]`; on a concave cell it lies in
`[-13epsilon_j/16,epsilon_j/16]`. These bounds survive restriction of a convex
or concave source cell. On a bracket, the absolute chord error is at most
`epsilon_j/16`, so downward rounding gives
`y_j-f_j(x) in [-epsilon_j/8,epsilon_j/16]`. Each case in (3) admits absolute
error at most `15epsilon_j/16`. Zero-width cells satisfy the same bounds.

The index circuit computes the source-cell type for every output. Its Boolean
wires select the two rational offsets in (3) by linear equations, with no new
integer declarations. The same index and interpolation weight are used for
all outputs; this ensures simultaneous exact vector-graph containment.

## 4. Count and bit complexity

The indexed-knot compiler applies to the merged endpoints, directed polynomial
values, and source-cell flags. Only `ceil(log2 K)` input index bits are declared
integer. Internal gate variables and endpoint-bit products remain continuous
and are forced by those index bits. Fixed denominators and offsets decode
signed rational values. Invalid cell codes are excluded.

Each binary search has polynomially bounded depth, each scalar indexed oracle
runs in polynomial time, and there are only polynomially many outputs and
pieces. All denominators, count sums, and integer numerators have polynomial
bit length. Equation (2) gives

```
K<=4096(sum_j D_j)*2^p,
```

which proves (1). The algorithm knows the computed counts, not the unknown
optimal count `p`.

This is the same overlay mechanism as the convex-vector theorem; the added
work is source-cell sign metadata and a valid band on a bracket that may
contain an inflection. The logarithmic degree order is necessary already for
one output by the reviewed Bernstein triangular-wave family. No necessity of
an output-count penalty for globally convex vectors is asserted here.

## Supporting verification

The [exact checker](../code/quadratic_rank/check_implicit_knot_overlay.py)
passes 2,304 ordered-search comparisons, 60 multiset order statistics, 180
source-cell containments, eight large implicit-grid rank queries, and 99
convex/concave/bracket band checks. It does not implement the inherited
quadrature algorithm. Both independent proof audits passed, including the convex-overlay dependency.
The bounded literature review distinguishes the compact implicit representation
and integer-count comparison from prior finite overlays and selection algorithms.

The finite common-breakpoint construction and its single logarithmic index
have a direct predecessor in
[Lyu, Hicks, and Huchette, Section 3, Proposition 1](https://arxiv.org/abs/2304.14542).
They take the union of explicit breakpoints for several univariate outputs
and use shared SOS2 weights. The contribution considered here is its implicit
polynomial-bit realization and comparison with every convex integer lift;
merging breakpoints and sharing an index are not claimed as new.


* [First independent proof audit](../notes/review-compiled-polynomial-vector-overlay-precision.md).
* [Second independent proof audit](../notes/review-compiled-polynomial-vector-overlay-precision-second.md).
* [Focused source and novelty assessment](../notes/compiled-polynomial-vector-overlay-novelty.md).

The source assessment found no matching complete theorem in the checked
literature. This is a bounded assessment, not an exhaustive priority claim.
