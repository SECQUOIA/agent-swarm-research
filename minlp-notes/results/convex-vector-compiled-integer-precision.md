# Compact convex-vector graph formulations by merging implicit knot arrays

Date: 2026-09-05. Status: independently reviewed supporting construction.
The [first independent full audit](../notes/review-compiled-convex-vector-knot-overlay.md)
and [second audit](../notes/review-compiled-polynomial-vector-overlay-precision-second.md)
passed.

Let `F=(f_1,...,f_m)` consist of densely encoded rational polynomials convex
on `[0,1]`, and let the positive rational component tolerances be
`epsilon_1,...,epsilon_m`. A deterministic polynomial-time rational MILP
construction contains the entire vector graph and admits only errors
`|w_j-f_j(x)|<=epsilon_j`. Its binary count satisfies

```
p_out<=p_conv+11+ceil(log2 m).                                  (1)
```

The benchmark permits all convex lifts with unrestricted integer variables
and continuous size. Construction time and total encoding are polynomial in
the full dense vector input and tolerance encoding. If all outputs are
affine, the graph is linear and uses no integers. This does not establish an
output-independent additive bound.

The construction merges sorted rational knot arrays supplied by the
[reviewed scalar hybrid theorem](../results/convex-polynomial-compiled-integer-precision.md).
The arrays can have exponentially many entries but admit polynomial-time
indexed evaluation. Standard implicit order-statistic search performs the
merge without enumerating the entries.

## 1. The existing quantile algorithm returns ordered knots

The [compiled curvature-quantile algorithm](../results/compiled-curvature-quantile-precision.md)
computes an interior knot for target `t=qU/N` by a fixed-depth bisection.
At a node with midpoint `x`, it uses one deterministic approximation
`Fhat(x)` at a fixed error `zeta`, independent of the target. It proceeds
left if `t<Fhat(x)-zeta`, returns `x` if the target is between those two
thresholds, and proceeds right if `t>Fhat(x)+zeta`.

This output is nondecreasing in the target. To prove it, consider the common
binary search tree. At any node, the target ranges for the left subtree,
returned midpoint, and right subtree are ordered. Every possible output of
the left subtree lies at or below the node midpoint; every right-subtree
output lies at or above it. Induction from the common final depth proves
the claim, even if the approximation values at different nodes are not
monotone in `x`. Early returns and final-depth midpoints preserve the same
ordering. Forcing the endpoint knots to be zero and one also preserves it.

Here the oracle must be evaluated canonically with the same accuracy and
deterministic algorithm at a given node for every target. This is available
in the cited construction and entails no new numerical accuracy requirement.
Padding dyadic outputs to one precision does not change their values.

The scalar hybrid's enumerated greedy knots are already increasing. Its
monotone-curvature pieces therefore also have nondecreasing knots. On a
reflected piece, reverse the local index order when mapping back to original
input coordinates. Concatenating the consecutive pieces gives, for output
`j`, a nondecreasing implicit array

```
0=a_(j,0)<=a_(j,1)<=...<=a_(j,K_j)=1.
```

Its endpoint evaluations take polynomial time, all rational knots share a
polynomial-bit denominator, and every cell's exact chord error is at most
`13epsilon_j/16`. The scalar cell-count proof gives

```
K_j<1458*2^(p_conv)                                              (2)
```

for nonaffine outputs. Indeed, projection of a vector lift is a scalar lift
at tolerance `epsilon_j`, so its minimum scalar integer count is no larger
than `p_conv`. An affine output may use `K_j=1`, which also satisfies (2).

## 2. Polynomial-time order statistics of all right endpoints

Take the multiset consisting of the right endpoints
`a_(j,1),...,a_(j,K_j)` for every `j`. Its total multiplicity is

```
K=sum_j K_j.
```

Write its sorted values as `b_1<=...<=b_K`, retaining duplicates, and put
`b_0=0`. Every original knot occurs in this list except the redundant initial
zero. The final value is one. Thus the consecutive cells `[b_k,b_(k+1)]`
cover `[0,1]`, and any positive-length cell is contained in one cell of each
original array. Duplicate endpoints merely give zero-length cells.

Fix a positive common denominator `H` for all input knots. The product of
the polynomially many piece-endpoint denominators, multiplied by a sufficiently
large power of two for all local dyadic precisions, suffices. Its bit length
is polynomial in the total input. Every knot is exactly an integer divided
by `H`.

For a candidate numerator `v in {0,...,H}`, count the number of right
endpoints at most `v/H`. Each array's count is found by binary search in its
index, using its monotone polynomial-time indexed evaluator. Sum these
counts over the `m` arrays. For `k>=1`, the numerator of `b_k` is the least
`v` for which the sum is at least `k`; binary search over the numerator
range finds it exactly. This requires at most `ceil(log2(H+1))` count
queries, each using `O(sum_j log(K_j+1))` indexed evaluations.

All bit lengths and iteration counts are polynomial. No enumeration of the
`K` knots, distinct-knot count, exact real root, or approximate tie decision
is needed. Repeated knots are handled by multiplicity in the comparison.

## 3. Compiling the merged cells and their graph bands

Given a cell index, compute its two merged endpoints. At each endpoint,
evaluate each dense polynomial exactly as a rational number and then round
down to a fixed dyadic precision with error at most `epsilon_j/8`. These
operations have polynomial bit complexity. Use a fixed rational offset if
needed to encode signed values with nonnegative binary output numerators.

The standard indexed-knot circuit construction uses only
`ceil(log2 K)` declared binary input variables. Continuous gate variables
are forced to their Boolean values by those inputs. Products of the common
continuous interpolation weight and computed output bits have exact linear
formulations. Exclude cell-index codes at least `K`.

Let `y_j` interpolate the rounded values on the selected merged cell. Impose

```
y_j-13epsilon_j/16<=w_j<=y_j+epsilon_j/8.                         (3)
```

On a positive-length merged cell, restriction of a convex chord interval
cannot increase its chord error. Thus its exact chord gap remains between
zero and `13epsilon_j/16`. Rounding introduces only a downward interpolation
error between zero and `epsilon_j/8`. Band (3) therefore contains the whole
graph on that cell and admits absolute error at most `15epsilon_j/16`.
At a repeated knot the exact chord gap is zero and the same argument applies.

Every input belongs to a merged cell, so all exact vector graph points are
admitted simultaneously. No independent cell-selection bits are added for
the different outputs.

Finally, (2) gives `K<1458m*2^(p_conv)`, hence

```
ceil(log2 K)<=p_conv+11+ceil(log2 m),
```

which proves (1). The algorithm computes each actual `K_j` and their sum;
it does not need to know `p_conv`.

## Scope and attribution

This compact result complements the
[finite vector bound](../notes/positive-polynomial-vector-refinement-obstruction.md),
whose box-error overhead is only `ceil(log2(2m+1))` but whose arbitrary real
knots and unrestricted finite size need not give a polynomial rational
construction. Neither theorem says that logarithmic dependence on `m` is
necessary relative to the unrestricted-integer minimum.

Merging explicit breakpoint lists and sharing one SOS2 or binary index
across several same-input piecewise-linear functions are already described
by [Lyu, Hicks and Huchette, Section 3](https://arxiv.org/html/2304.14542).
Binary search, order statistics of sorted arrays, and Boolean-circuit-to-LP
compilation are also established tools. The application here combines their
implicit versions with the reviewed scalar graph count and error bounds.
The monotonicity argument concerns the specific deterministic quantile
algorithm, not arbitrary approximate inverse oracles. No sparse huge-degree
claim is made: exact endpoint polynomial evaluation uses dense encoding.

The [independent exact checker](../code/quadratic_rank/check_implicit_knot_overlay.py)
passes 2,304 ordered-search comparisons, 60 exact merged order statistics,
180 source-cell containments, eight rank queries on arrays with `2^40`
cells, and 99 directed-band checks. These checks supplement the proofs;
the search tests deliberately include nonmonotone approximate oracle values.

The [bounded primary-source assessment](../notes/compiled-polynomial-vector-overlay-novelty.md) covers this theorem and its arbitrary-polynomial extension, including the explicit finite-overlay predecessor.
An [additional independent source audit](../notes/convex-vector-gap-and-overlay-source-audit.md)
confirms the same finite-overlay attribution and the scope of the implicit
polynomial-bit construction.
