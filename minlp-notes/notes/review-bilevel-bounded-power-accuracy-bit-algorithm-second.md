# Independent second audit: bounded-power bilevel approximation in accuracy bits

Date: 2026-09-05. Reviewer: `constant_rank_review`.

**Status: PASS.** I independently checked [the candidate](bilevel-bounded-power-accuracy-bit-algorithm.md), including every approximation budget, the fixed-dimensional algebraic optimization interface, rational leader recovery, and the growing-power output obstruction. For fixed leader dimension and fixed upper bound on the local powers, its running time and rational output length are polynomial in the original input encoding and the requested number of accuracy bits `B`. No exact sum-of-radicals comparison is needed. This audit does not certify literature novelty or practical efficiency.

## Follower response and approximation

Each follower term has derivative `z^p-ell(x)`, which is strictly increasing on `[0,1]`. Its clipped inverse is the stated unique response, including `p=1` and both clipping endpoints. The separable sum is strictly convex even though its Hessian need not be uniformly positive definite at zero. The theorem correctly does not claim strong convexity.

When `A=sum|c_i|` vanishes, the leader objective is an exact rational LP. Otherwise `eta=epsilon/(16 max(1,A))` has polynomial encoding; `m=ceil(log2(1/eta))` is polynomial in the input length and `B`. With `K=Pm`, every `p<=P` has `(2^-K)^(1/p)<=2^-m<=eta`. This includes arbitrarily negative affine arguments, where the exact response is already zero.

On each dyadic interval the normalization gives `|u|<=1/3`. For `alpha=1/p`, the binomial coefficient magnitudes are at most one. The absolute geometric tail after degree `q=m+1` is at most `3^-q/2`, which is at most `eta/4`; the truncated polynomial's magnitude is at most `3/2`. Approximating the scale root to `eta/4` therefore gives total error at most `3eta/8+eta/4<eta`. Both interval endpoints are included. The transition at the truncation threshold is also valid for either adjoining branch.

Ordinary rational bisection takes only `O(log(1/eta))` steps for each scale root. Raising a polynomial-bit rational to a fixed power has polynomial cost and encoding. Binomial coefficients, normalization factors, and dense polynomial expansion have polynomial encoding: factors involving the dyadic interval index and the polynomial degree contribute products of polynomially bounded bit lengths. Arbitrary signed upper weights are controlled by their absolute sum, so cancellation is not assumed.

## Cells, boundaries, and encoding

There are polynomially many rational threshold hyperplanes and polynomially many realizable sign cells in fixed leader dimension. One may enumerate them by incremental rational LP feasibility with a slack variable for strict inequalities, or by fixed-dimensional sign determination. The original polytope's inequalities remain imposed. Zero signs, constant affine arguments, lower-dimensional domains, and threshold-only cells must be retained, as the candidate states.

For a nonempty relative cell, replacing strict tests by weak tests gives its closure inside `X`. Given any point satisfying the weak tests, mixing it with a point satisfying the original strict tests stays in `X` and approaches it through the relative cell. Thus the closure operation introduces no spurious branch domain. Each selected polynomial is valid throughout that closure, even if an adjacent cell chooses a different approximant on their common boundary.

Substitution of rational affine arguments into degree-`q` polynomials creates only `binom(r+q,q)` monomials because the leader dimension is fixed. There is no expansion in the number of follower coordinates. All cell inequalities and resulting objective coefficients have polynomial encoding, including on very narrow cells. Uniform objective error on every cell is at most `A eta<=epsilon/16`.

## Exact polynomial minimization does not require exact radical sums

The algebraic optimization claim has the required fixed-variable bit complexity. An explicit interface is to apply quantifier elimination to

```
x in C and forall u: (u in C implies Q(x)<=Q(u)).
```

There are only `2r` scalar variables. Compactness and nonemptiness ensure that the resulting minimizer set is nonempty. Elimination followed by algebraic sampling returns a minimizer through a rational univariate representation of polynomial degree and coefficient bit length. I visually checked the relevant primary statements: Basu, Pollack and Roy, *Algorithms in Real Algebraic Geometry*, second edition, Theorem 14.16 on printed pages 560–561 includes intermediate and output coefficient bit bounds; Theorem 13.11 on page 525 gives the sampling representation degree and coefficient bounds. Algorithm 14.9, whose complexity analysis is on page 568, is the direct optimization alternative. The [primary book](https://www.math.purdue.edu/~sbasu/bpr-posted1.pdf) is also stored in the repository's literature folder.

The exact cell objective is a rational polynomial in fixed-dimensional leader variables. Consequently its algebraic minimizer and value have polynomial degree. Comparing two cell values is polynomial-degree algebraic comparison; selecting the least one does not require forming a common field for all cells. The winner can retain its own representation after each comparison. None of this represents or compares the sum of the actual follower radicals exactly.

## Rational feasible leader recovery

A bounded rational cell has rational vertices, and every vertex is obtained from an independent ambient-rank set of active rows. This remains true for a lower-dimensional cell: equality-defining active rows contribute to that rank. With fixed `r`, vertex enumeration and its rational encodings are polynomial.

Caratheodory's theorem supplies an affinely independent subset of at most `r+1` vertices containing the algebraic minimizer in its convex hull. Enumerating such subsets and checking consistency and nonnegative barycentric coordinates uses rational linear algebra and sign tests in the minimizer's polynomial-degree field. The barycentric coordinates are affine functions of that minimizer; this step does not create a field containing unrelated follower roots.

Flooring the first `s-1` barycentric weights to multiples of `1/R` and assigning the remaining mass to the last vertex preserves nonnegativity and total mass one. The total weight perturbation is less than `2(s-1)/R<=2r/R`, so the leader perturbation in infinity norm is at most `2r/R`, since all vertices lie in the unit cube. The new point is feasible in the same cell exactly. Coordinatewise rounding of the leader, which could violate a narrow cell, is never used.

The coefficient bound `L=max(1,sum|a_nu| |nu|)` bounds the sum of absolute partial derivatives of `Q` on the unit cube. Thus `R>=8 max(1,r)L/epsilon` limits polynomial objective deterioration to `epsilon/4`. The numerical value of `R` can be large, but its logarithm and its encoding are polynomial. Each floor is computed by `O(log R)` exact comparisons against rational thresholds; the output convex combination has polynomial rational length. Degenerate simplices can be skipped, and a singleton cell already has a rational leader.

Two objective approximation errors of `epsilon/16` plus the recovery error `epsilon/4` give true suboptimality at most `3epsilon/8`. At the rational leader, clipping decisions are exact rational comparisons. Independent root bisections with total weighted error at most `epsilon/4` give a rational value within `5epsilon/8` of the true optimum, hence within the requested `epsilon`. With signed weights, choose the appropriate endpoint of each root interval if a certified upper value is desired. No derivative bound on the true clipped-root objective is used during recovery.

## Exact arithmetic and growing powers

The constant-leader square-root construction is correct: argument `a_i/M^2` lies in the unit interval for `M>=max a_i`, and upper weight `M` restores `sqrt(a_i)`. Exact objective threshold testing therefore contains sum-of-square-roots comparison. The positive theorem makes only an additive approximation claim and does not assume a polynomial exact oracle for that problem.

For the separate growing-power example, the two response exponents are `1/p` and `2/p`, and the upper objective becomes `(s-1/2)^2-1/4`. Suboptimality at most `1/64` forces `3/8<=s<=5/8`, hence `0<x<=(5/8)^p`. A positive reduced rational `a/b` then has `b>=1/x>=(8/5)^p`, requiring `Omega(p)` explicit binary bits. Its sparse power input has only `O(log p)` bits and its accuracy is fixed. This is an unconditional output-length obstruction for the stated two-power extension. It does not establish a same-power obstruction, computational hardness for real or compressed outputs, or failure of the fixed-power theorem.

## Supporting verification and remaining scope

I reran [the exact rational approximation checker](../code/bilevel_bounded_power/check_dyadic_approximation.py):

```
PASS: 900 certified dyadic approximation values; truncation/tail bounds; output-barrier constants
```

It uses rational root enclosures to certify tested errors; it is not merely floating-point evidence. It does not implement the full algebraic optimization algorithm, whose proof and primary complexity interface are checked above.

The theorem requires fixed leader dimension, bounded local powers, an explicitly given rational nonempty polytope in the unit cube, and no additional response-dependent upper constraints. Polynomial time is in `B` itself, not in the binary length of the integer `B`. Arbitrarily large numerical coefficients and arbitrarily narrow rational cells are allowed through their encoding lengths. No unresolved proof or output-encoding issue remains within this scope.

## Addendum: explicit polynomial dependence on the numerical power bound

**PASS for the stronger complexity statement.** The same algorithm is polynomial in the original input bit length, `B`, and the numerical value `P=max_i p_i`, with only the leader dimension fixed. The fixed-`P` statement above is a special case. Consequently growing unary-encoded or explicitly dense powers also admit a polynomial-time accuracy-bit algorithm and polynomial-length rational leader output in their supplied encoding.

Here is the dependence that must be retained. The truncation depth is `K=Pm`, so the number of thresholds and their binary coefficient lengths are polynomial in `P` and `m`. The approximation degree remains `q=m+1`, independent of `P`. The exact binomial coefficient `binom(1/p,j)` has numerator and denominator lengths `O(j(log P+log(j+1)))`, as follows by writing its product with denominator `p^j j!`. A bisection point has `O(m)` bits; its exact `p`th power has `O(Pm)` bits. Comparing that power with a dyadic center adds at most `O(K)` bits. These operations take polynomial time in numerical `P`; no unit-cost operation on a huge exact power is assumed.

There are at most `P*K` scale-root approximations even if every possible power is processed, and processing only the powers present in the input also suffices. Their polynomial expansions have coefficient lengths polynomial in `K`, `q`, `log P`, and the original input. The number of cells is polynomial in `N(K+1)` for fixed `r`. The fixed-variable quantifier-elimination degree exponent depends only on `r`; increasing `P` increases explicit coefficient heights and cell counts, without introducing `P` quantified variables. Vertex enumeration, barycentric recovery precision, and final independent root bisections likewise stay polynomial in numerical `P`.

Thus no part of the proof uses an exponent in the running-time bound that grows with `P`. This extension still does not give polynomial time in `log P` for sparse binary-encoded powers. The candidate's `Omega(P)` rational-output obstruction is consistent with, and explains a limitation of, this explicit numerical-parameter dependence.
