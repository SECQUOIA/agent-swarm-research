# Second independent audit: conditioned-box additive bilevel algorithm

Date: 2026-09-05. Reviewer: `noncommutative_rank_review`.

**Verdict: PASS.** The [candidate algorithm](bilevel-conditioned-box-additive-algorithm.md) achieves its stated normalized additive guarantee in time polynomial in input bit length, `K`, and `1/epsilon` for fixed leader dimension. No mathematical correction is required. This audit does not resolve novelty.

## Saturation and cells

The two saturation implications hold at their thresholds. Positive definiteness gives `Q_ii>0`. If the cost is at least `-m_i^-`, then at a point with `z_i>0` the derivative is bounded below by `Q_ii z_i>0`; a small decrease improves the objective. If the cost is at most `-m_i^+`, then at `z_i<1` the derivative is bounded above by `Q_ii(z_i-1)<0`; a small increase improves it. These arguments are coordinatewise and allow arbitrary off-diagonal signs.

The slab width is exactly the absolute row sum of `Q`. The two thresholds of one coordinate cannot coincide. Threshold equalities therefore freeze the coordinate unambiguously. A coordinate strictly inside its slab in a sign cell may reach saturation in that cell's closure, which is harmless: it remains in the reduced problem. Zero rows of `D` inside their slabs must remain eligible to vary through coupling, as the candidate correctly states.

The sign-cell enumeration is valid for lower-dimensional `X`, coincident hyperplanes, and cells consisting of a point. For a realizable strict/equality pattern, mixing a weakly feasible point with a point satisfying the strict signs proves the asserted closure equality. There is no need for a full-dimensional interior point.

One explicit polynomial enumeration is incremental: start with `X`, add each threshold test, branch each retained sign pattern into its three possible signs, and discard infeasible patterns. Test strict feasibility by maximizing a common slack `sigma`, constrained by `0<=sigma<=1`, with each strict signed affine test at least `sigma`. Positive optimum is equivalent to feasibility of all the strict signs. Patterns without strict signs use ordinary LP. The number of realized patterns at each stage is bounded by the total face count of a hyperplane arrangement in dimension at most `r`, hence polynomial for fixed `r`. Restricting to convex `X` cannot split one pattern into disconnected components. The explicit inequality count of `X` enters LP input size, not the grid exponent.

## Sensitivity and rational row basis

For symmetric `Q`, spectral radius is bounded by induced infinity norm, so `mu=1/||Q^{-1}||_infinity<=lambda_min(Q)`. Every principal submatrix has smallest eigenvalue at least that of `Q`. Subtracting the reduced follower variational inequalities thus proves the stated response bound without a dependence on the frozen cost magnitudes.

The maximum-minor row argument is correct. Fix independent columns `S`, choose rows `I` maximizing the nonzero determinant magnitude, and let `M=E[I,S]`. For any row, the coefficients `E[i,S] M^{-1}` have absolute value at most one by determinant replacement. Since columns `S` span the column space, these coefficients represent the whole row `E[i,:]`, not just its entries in `S`. Hence a basis-coordinate change at most `delta` gives each normalized cost change at most `q delta` and response change at most `sqrt(N) q delta`.

Each selected row belongs to an unsaturated coordinate and has a scalar range of width `R_i/mu<=K`. The offset may be numerically large but has polynomial rational bit length. This is the step that removes numerical `c,D` magnitudes from the enumeration bound. Rank zero is handled exactly; its response is constant on the entire cell. The case of leader dimension zero is also an immediate single-response evaluation.

## Leader LP and additive guarantee

Each inverse-image rectangle intersected with its closed cell is a compact rational polytope. Exact LP produces a rational minimizer of `b^T x`, including when the intersection is lower-dimensional or a singleton. On the rectangle containing a global optimizer, the retained leader has no larger direct leader cost. Therefore the magnitude or sign of `b` cannot amplify the follower approximation error.

The follower contribution changes by at most

```
||a||_2 sqrt(N) q delta
<= ||a||_1 sqrt(N) r epsilon/(N r)
<= epsilon ||a||_1.
```

The follower map is continuous by strong convexity and the fixed compact box, so the global optimizer used in this comparison exists. Closed grids cover all boundaries. The eventual output is the best evaluated candidate, which only improves the guarantee. If `a=0`, exact leader LP is sufficient.

## Exact responses and bit complexity

At a rational leader, the follower optimizer is rational: on its minimal box face, free coordinates satisfy a nonsingular principal system, while the remaining coordinates are zero or one. Rational determinant bounds give polynomial bit length. This representation fact alone would not prove polynomial-time discovery of the face, but the candidate separately invokes the classical polynomial-time convex-QP algorithm, which supplies that missing computational ingredient.

The primary journal archive for Kozlov, Tarasov and Khachiyan, *The polynomial solvability of convex quadratic programming* (1980), explicitly states in its Russian abstract that the algorithm is exact and polynomial in binary input length. I checked that abstract directly; I did not independently reread the full historical proof. [Primary archive and abstract](https://www.mathnet.ru/php/archive.phtml?jrnid=zvmmf&option_lang=rus&paperid=5189&wshow=paper).

The row selection enumerates at most `N^r` minors. Grid indices have bit length polynomial in `log K` and `log(1/epsilon)`. Matrix inversion, grid offsets, LP vertices, and exact follower responses have polynomial encoding length. The count

```
N^{O(r)} (2+K N r/epsilon)^r
```

therefore gives the claimed bit-time bound after multiplying by polynomial per-candidate work. Since each infinity norm is at most `sqrt(N)` times the spectral norm for a symmetric matrix, `K<=N kappa_2(Q)` also holds. The stated distinctions between inverse tolerance and precision bits, and between normalized and absolute error, are necessary and correctly retained. There is no promise for exact follower-dependent upper feasibility constraints.

## Independent exact checks

Added [a reproducible exact checker](../code/bilevel_response/check_conditioned_additive_second.py). It enumerates all follower box active patterns for small scalar-leader cases, obtains the complete exact piecewise-affine response and global benchmark, and separately runs the saturation/basis grid with the direct leader LP rule.

All seven rational examples passed: 25 affine response pieces and 299 retained grid candidates. They include coefficients of magnitude `2^80`, opposite large cost slopes, a zero direct slope with coupling, rank-zero response, a singleton leader polytope, and a case with strictly positive approximation error `1/120`. A further 60 exact rank-one through rank-three matrix cases passed the maximum-minor full-row representation and coefficient bounds. These checks supplement the proof and do not replace its general complexity argument.
