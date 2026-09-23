# Second audit: hardness of approximating integer precision

Date: 2026-09-05. Reviewer: `constant_rank_review`.
Reviewed draft: `notes/quadratic-integer-precision-approximation-hardness.md`,
including its positive-optimum extension.

## Verdict

**PASS.** The zero-dimension characterization, restricted-family
coNP-completeness, multiplicative obstruction at zero, replicated additive
obstruction, and positive-optimum additive and multiplicative obstructions
are correct. No substantive mathematical correction was needed.

The claims concern polynomial-time construction of valid formulations
with a guaranteed integer count. They do not require optimizing a produced
formulation or efficiently checking its validity. Their input-dimension
bounds are uniform, with a fixed approximation constant and exponent
across all inputs. The amplification uses vector-valued graphs with a
growing number of disjoint convex quadratic outputs; the single-output
claim is the zero-dimension and unrestricted finite-factor obstruction.

This review does not establish novelty. I inspected the linked primary
Garey--Johnson--Stockmeyer paper: its abstract explicitly identifies
Simple Max Cut, with all edge weights one, as NP-complete.
[Primary paper](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/JohnsonDavid2.pdf).

## Zero integer dimension

The Hessian of `f_G=sum_edges(x_i-x_j)^2` is twice the graph Laplacian
and is positive semidefinite. Coordinatewise convexity lets one move
successively to cube endpoints without reducing the objective. Therefore
its maximum over the continuous cube is exactly the maximum cut size.
The function is nonnegative, is invariant under complementing every
coordinate, and vanishes at the cube center.

When `M(G)<=epsilon`, the proposed LP band
`0<=x<=1, 0<=w<=epsilon` contains the entire graph. Any admitted
output and the true output belong to the same interval of length
`epsilon`, giving the required uniform absolute graph error. Thus
both integer minima are zero.

Conversely, the complement of a Boolean maximum-cut vector has the
same output. In any zero-integer convex lift, choose feasible lifts of
these two exact graph points. Their midpoint has visible input equal
to the cube center and visible output equal to `M(G)`. Its error is
therefore `M(G)`. Continuous auxiliary variables cannot alter this
visible midpoint, and convexity suffices without closedness. This proves
the stated equivalence for both minima.

For integer target `k>=1`, the tolerance `k-1/2` is positive and has
polynomial rational encoding length. The zero case is exactly
`M(G)<k`. Its complement has a Boolean cut of size at least `k` as
a polynomial certificate. Thus the zero-decision language restricted
to this explicitly described graph-quadratic family is coNP-complete.
No general complexity-class membership for arbitrary convex-lift
minimization follows or is claimed.

## Finite multiplicative approximation at zero

A finite multiplicative guarantee forces zero output count whenever the
minimum is zero. In the positive case, any valid formulation must have
at least one integer coordinate. Reading the declared count therefore
distinguishes the two Max-Cut cases.

The argument permits the approximation factor to depend on the instance
or its dimension, provided it is finite and the guaranteed output count
is a pure multiplicative bound. It does not cover a guarantee with an
additional additive term. Validity is part of the hypothetical algorithm's
contract; the reduction never attempts to certify an arbitrary supplied
formulation.

## Replication and parity

In the high-Max-Cut case, choose a maximizing Boolean vector and its
complement independently in each of `t` blocks. This gives `2^t`
distinct exact graph points. Two distinct choices differ in at least
one block, where their midpoint input is the center but their midpoint
output remains `M(G)>k-1/2`. Hence every pair has an incompatible
midpoint in at least one output.

Choose one feasible lift for each point. If two integer vectors have
the same parity, their midpoint is integral in every coordinate.
Convexity would admit the incompatible midpoint, a contradiction.
At most `2^p` parity classes are available, so `p>=t`. The argument
applies equally to binary and unrestricted general integer variables.
The exponentially large point family is only a mathematical packing
witness; the reduction does not enumerate or compute it.

In the low case, the product of the displayed LP bands gives zero
integer dimension. Thus replication produces the gap `0` versus
at least `t` using `N=tn` input coordinates and `t` outputs.

## Approximation constants and reduction size

Fix the proposed exponent `delta>0` and its uniform finite constant
`C`. For `0<delta<=1`, choose a fixed integer `q>1/delta` and
set `t=n^q`. Then

```
C(tn)^(1-delta)/t
 =C n^(1-delta-q delta) -> 0.
```

Consequently the low-case output count is below `t` for every
sufficiently large graph, whereas every high-case valid count is at
least `t`. The exponent and threshold may depend on the hypothesized
algorithm's fixed guarantee; they remain constants in this reduction.
Small input dimensions can be solved by enumerating their constantly
many cuts, with ordinary polynomial-time comparison against the encoded
target. Alternatively, isolated-vertex padding preserves maximum cut.

For `delta>1`, the guarantee is no weaker than a constant additive
guarantee, so the `delta=1` obstruction suffices. The same observation
handles the positive-optimum multiplicative claim below.

Replication is polynomial in the original input encoding because `q`
is fixed. This remains true with dense matrix encoding: writing `t`
matrices of dimension `tn` still takes only a fixed polynomial number
of entries. Tolerances and all repeated coefficients have polynomial
bit length. The construction algorithm's polynomial output-time bound
also makes the returned integer count readable in polynomial time.

The proof excludes every fixed sublinear power bound in input dimension.
It does not exclude a bound such as `N/log N`, which need not be
smaller than `t` under this fixed polynomial replication. The draft
correctly records that limitation.

## Fixing every tolerance to one

Scaling each output by the positive rational `1/(k-1/2)` preserves
convexity, rationality, and polynomial encoding length. The low-case
range lies within `[0,1]`, while every high-case incompatible midpoint
has error `M(G)/(k-1/2)>1`. Thus the same reduction has unit tolerances
throughout. The scaled coefficients need not be integers; the draft
correctly calls them rational.

## Positive-optimum amplification

For the additional scalar output `8z^2` on `[0,1]` with tolerance
one, the graph endpoints have midpoint `(1/2,4)`, whose graph error
is two. At least one integer coordinate is necessary.

The displayed one-binary construction is exact in its prefix products:

```
z=(beta+r)/2,
8z^2=2(beta+2 beta r+r^2).
```

The exact bounded binary product enforces `v=beta r`. On
`0<=r<=1`, the three inequalities for `s` contain `r^2` and
have maximum absolute deviation `1/4`: above the graph the error is
at most `r-r^2`, and below it at most
`r^2-max(0,2r-1)`. Multiplication by two gives output error at most
`1/2`, safely within the unit tolerance. Every `z` admits a prefix
representation, including both endpoints. Hence this scalar's two
integer minima are exactly one.

Appending it to the replicated graph gives low optimum exactly one:
the product construction is an upper bound, and fixing other inputs
leaves the scalar midpoint obstruction. In the high case, independently
choosing the scalar endpoints doubles the pairwise-incompatible packing.
If two points differ only in the scalar choice, its midpoint error is
two; if they differ in a graph block, that block already provides an
error exceeding one. Thus there are `2^(t+1)` incompatible points and
the lower bound is `p>=t+1`.

The total input dimension is `N=tn+1`. Since `tn+1<=2tn`, the same
fixed-polynomial replication makes `C N^(1-delta)<t` eventually.
Under an additive guarantee, the low count is at most
`1+C N^(1-delta)<t+1`. Under a multiplicative guarantee it is at
most `C N^(1-delta)<t+1`, because the low optimum is exactly one.
Every high-case count is at least `t+1`. Therefore both claimed
barriers survive the promise of a positive optimum, with all tolerances
fixed at one. This strengthening avoids relying solely on the convention
for multiplicative approximation at a zero optimum.

