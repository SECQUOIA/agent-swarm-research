# Independent review: three modes, five unit intervals, two switches

Date: 2026-09-07. Reviewer: `review_small_grid` subagent. Scope: the exact universal bound in [the small-grid note](cia-reopened-small-grid-boundary.md), including chamber coverage, boundary profiles, and the lower example. The separate literature review owns correspondence with the published statements.

**Verdict: the exact value is 1.** The upper bound has a complete finite integer-arithmetic proof once the prefix-flow integrality argument below is included. The independent checker does not import the author's code, use an optimization solver, or read its output as a certificate.

## Independent implementation and result

Run:

```bash
python code/cia_reopened/check_small_grid_review.py
```

The [checker](../code/cia_reopened/check_small_grid_review.py) enumerates all 14,400 candidate floor histories directly. This differs from the author's recursive pruning: each complete history is evaluated using precomputed integer bit masks over all 243 words of length five.

The resulting partition is:

| Candidate histories | Count |
|---|---:|
| No compatible integral word | 8,082 |
| Compatible words, but no strict chamber interior | 5,922 |
| Nonempty strict chambers | 396 |
| Total | 14,400 |

Among the 396 strict chambers, the minimum compatible word switch counts are 0 in three chambers, 1 in 138 chambers, and 2 in 255 chambers. Thus every strict chamber has a compatible word with at most two switches. A separate direct cumulative-error check of all 99 words with at most two switches gives minimum error exactly 1 against the pure word `(0,1,0,1,0)`.

## Why the enumeration covers every generic profile

Let `a[i,k] >= 0` be the relaxed allocation of mode `i` on unit cell `k`, with each column summing to one, and let `A_i(k)` be its cumulative allocation. First suppose all fifteen `A_i(k)`, for `i=0,1,2` and `k=1,...,5`, are nonintegers. Put `b_i(k)=floor(A_i(k))`.

At time `k`, the three fractional parts lie strictly between zero and one and sum to an integer. Their sum is therefore 1 or 2. Consequently `sum_i b_i(k)` is `k-1` or `k-2`, and each floor is nonnegative. There are exactly `k²` such triples: the numbers of weak compositions of `k-1` and `k-2` into three parts sum to `k²` (the second term is empty at `k=1`). Hence there are exactly `(1·2·3·4·5)²=14,400` candidate histories. No assumption about monotonicity of floors or realizability is needed to form this superset.

For a fixed history, consider the closed polytope of relaxed allocations satisfying

\[
b_i(k)\le A_i(k)\le b_i(k)+1
\]

for every coordinate and time. This polytope is integral. One explicit flow model has:

- a source sending exactly one unit to a separate node for each cell `k`;
- arcs from cell `k` to nodes `(i,k)`, carrying `a[i,k]`;
- a chain `(i,1) -> (i,2) -> ... -> (i,5) -> sink` for each mode;
- lower and upper capacities `b_i(k)` and `b_i(k)+1` on the chain arc leaving `(i,k)`.

Conservation makes that chain-arc flow exactly `A_i(k)`. All capacities and source/sink demands are integers. The flow conservation matrix is a directed incidence matrix. Its subdeterminants are 0 or ±1: a square submatrix with a column having at most one nonzero expands inductively, while a submatrix with two nonzeros in every column has dependent rows. Adding bound rows preserves this property. Integer right-hand sides therefore make every vertex integral.

Each integral allocation has one unit in exactly one mode per cell, so it is precisely one of the 243 enumerated words. Conversely every enumerated word respecting the bounds is a point of this polytope. The polytope is bounded and every point is a convex combination of its integral vertices.

This justifies both pruning criteria. An empty set of compatible words means an empty polytope. If all compatible words take only one of the two integer endpoints in some prefix coordinate, every point of the polytope takes that endpoint, so no point has all prefix coordinates strictly between their bounds. Conversely, if every coordinate attains both endpoints among the compatible words, the average of **all** those words is a valid relaxed allocation strictly between every pair of bounds. Thus the surviving 396 histories are exactly the nonempty strict chambers, not a sampled subset.

If `W_i(k)` is the cumulative integer allocation of a compatible word, then `W_i(k)` is either `b_i(k)` or `b_i(k)+1`. It follows that `|W_i(k)-A_i(k)|<1` throughout the strict chamber. The independent code also checks the maximum distance from each selected word's prefix count to **both** endpoints of the closed coordinate interval; it never relies merely on evaluating one representative profile.

For grid-constant relaxed controls, cumulative discrepancies are affine on every cell and their absolute maximum occurs at an endpoint. The same conclusion holds for arbitrary measurable simplex-valued relaxed controls: with an integer mode fixed on that cell, its discrepancy derivative has one sign and every other mode's discrepancy derivative has the opposite sign. Each coordinate is monotone. Thus replacing the relaxed control by its cell averages preserves the objective for every grid word, and the universal bound also covers arbitrary measurable relaxed profiles.

## Boundary profiles and lower bound

Generic profiles are dense. A concrete proof mixes any profile with the constant profile `q=(1/7,2/7,4/7)`. Every prefix `k q_i` for `k=1,...,5` is noninteger. Each equation asserting an integer prefix for the mixture excludes at most one mixing parameter; there are only finitely many relevant equations. Mixing parameters tending to zero can therefore be chosen so that all prefix coordinates are noninteger.

The minimum error over the finite collection of 99 schedules with at most two switches is continuous in the allocation matrix: each individual error is a maximum of finitely many absolute affine functions, and a finite minimum preserves continuity. The strict-profile bound thus extends to error at most 1 at every boundary profile.

A minor proof issue identified during review was the suggestion to perturb toward the uniform profile. At `k=3`, a prefix equal to 1 remains equal to 1 under that perturbation, so uniform mixing alone does not establish generic density. The author was notified; the nonuniform rational profile above repairs the argument without changing the theorem.

For the lower bound, use the pure allocation word `(0,1,0,1,0)`. Its discrepancy against any integer word is an integer at every grid endpoint. Error below 1 would therefore force every prefix count to agree exactly, which forces the same word and its four switches. Every allowed schedule consequently has error at least 1. The independent enumeration confirms some allowed schedule attains 1. Together with the universal upper bound, this proves the exact minimax value.

## Scope

This is a finite computer-assisted proof for the exact parameter triple `(n,N,s)=(3,5,2)` with unit cell lengths, a free initial mode, and at most two changes of mode. Arbitrary measurable relaxed profiles are covered by their cell averages. Scaling all five cell lengths by `h` scales the result to `h`. The checker does not prove analogous formulas for larger dimensions, longer grids, nonuniform grids, dwell constraints, or prescribed initial modes. It supplies the exact universal upper needed to evaluate the literature discrepancy; an input with small error alone would not have supplied that upper bound.
