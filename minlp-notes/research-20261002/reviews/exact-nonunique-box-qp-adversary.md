# Independent arithmetic review of exact nonunique box QP

Date: 2026-10-02.

Reviewed [the exact nonunique corollary](../geometric-dp/exact-nonunique-box-qp.md), the height and reconstruction arguments in [exact box QP](../geometric-dp/exact-box-qp.md), and the algorithm and parameter definitions in [projection anchors](../new-direction/projection-anchors.md). The source-grid recurrence in the original geometric-grid theorem was also checked. This review concerns the arithmetic transfer; the projection progress theorem has a separate review.

**Verdict:** No substantive error found in the arithmetic transfer. Conditional on the coordinate-anchor theorem's lower-bound validity, finite-projection progress bound, and table-operation bound, the stated exact terminating algorithm and fixed-width polynomial bit bound follow. The arithmetic extension was checked directly rather than assumed from the earlier single-center theorem. No claim about novelty or practical performance is established by this review.

## Height and qualitative growth

The height argument applies to every isolated optimizer. Fix that optimizer's integer assignment and its active continuous bounds. On the remaining free continuous face, first-order stationarity and positive semidefiniteness hold. A singular free Hessian gives a nonzero feasible short line with exactly constant quadratic objective, contradicting isolation. Thus the free block is invertible and Cramer's rule gives a common coordinate denominator dividing `D det(2H_SS)`, at most `R`. The empty free block has determinant one. Arbitrary integer values in their bounded domains contribute integral right-hand-side data and do not require enumeration.

The stronger existence statement used for certification also holds without finite `S`: choose an optimal point on a continuous face of minimum dimension within one optimal integer slice. A singular free Hessian would allow movement to a smaller face. Consequently the optimum value always has reduced denominator at most `V`, even if other optimizers form a continuum.

The finite-set growth proof is sound. Compactness and vanishing objective gaps imply distance to the optimal set tends to zero. After fixing a nearest optimizer along a subsequence, the points converge to it and their integer assignments eventually coincide. In that slice, each displacement has nonnegative first-order objective change. The limiting unit direction has zero first-order change and nonpositive quadratic change; its feasible short ray forces the latter to be zero. This produces infinitely many global optimizers and is the required contradiction. No numerical lower bound on `g` is obtained or needed here.

## Recovery and certificate validity

For an admissible trial, the two accuracy inequalities give

```
dist(y,S)^2 <= eps_theta/g <= 1/(64R^4) < rho^2.
```

Choosing one nearest optimizer makes every coordinate reconstruction refer to the same optimal vector. This is essential: coordinatewise membership in optimal projections alone would not suffice. The uniform height bound applies to this nearest optimizer, including when different DP solves approach different optima. The integer coordinates already coincide because their distance is less than one. All integer variables must remain in the metric, as the statement explicitly requires.

The value interval has width at most `1/(4V^2)` and hence isolates the optimum value. Coordinate intervals have width `1/(2R^2)` and contain at most one rational with denominator at most `R`. Feasibility and exact objective equality make acceptance sound even for an inadmissible trial. That argument uses the unconditional optimum-value height bound, not a promise that an arbitrary candidate has denominator at most `V`.

## Denominator closure and bit costs

For continuous source grids the recurrence is exactly

```
t_(k+1) = (1+theta)t_k+h,  t_0=0.
```

With fixed `h=s 2^-J`, dyadic `theta=2^-r`, and `k<=K`, every unclipped offset has denominator dividing `D 2^(J+rK)`. The same `K=O(2^r(J+1))` bounds every source grid because every anchor stays in the original box. Clipping returns an original endpoint. Inductively, adding any number of anchors preserves the fixed denominator `Qgrid=D 2^E`, where `E=J+rK`. It does not require a denominator bound on the number of additions. Integer grids use their own floored recurrence; their coordinates are integers, so the same divisibility conclusion holds without treating their offsets as continuous offsets.

A quadratic monomial with coefficient denominator dividing `D` has value denominator dividing `D Qgrid^2=D^3 2^(2E)`. Every adjacent union-grid length has denominator dividing `Qgrid`. Since the denominator of `L` divides `D`, a correction `L ell^2/8` has denominator dividing `8D^3 2^(2E)`. Therefore the displayed `W` is valid for supplied factors, corrections, their sums, and DP messages. Minimization selects a value and introduces no division. Reduced rational arithmetic keeps retained denominators within this bound; temporary arithmetic products still have polynomial bit length.

Coordinates remain in the input box. Factor and correction magnitudes have polynomial bit bounds, and summing the assigned factors and corrections adds only polynomially many magnitude bits. Integer trial-step arithmetic uses rational `h` and `theta` with polynomial bit length. Thus comparison, grid generation, sorting, DP, and reconstruction all have polynomial bit costs in `I` and `E`. At a near-threshold admissible trial, `E` is polynomial in `I,kappa`; union-grid cardinalities introduce the stated polynomial dependence on `A` at fixed width.

## Unknown parameters and presentation

The bounded-run schedule does not need `A` or `g`. If admissible trial `m*` takes `P` bit operations, a round of index at most a constant plus `max(m*,ceil(log2 P))` suffices. Summing all trial budgets through this round costs `O(q* 2^q*)`, which is polynomial because `P` is polynomial in `I,A,kappa` and `2^m*=O(sqrt(kappa))`. Enforcing budgets at the bit-operation level, including preprocessing and rational operations, avoids charging a huge arithmetic operation as one unit. The note explicitly makes this requirement.

One optional clarification: specify a single initial endpoint anchor per coordinate, for example `C_i={a_i}`. Then the literal `T+1` anchor count agrees with the initialization. If both endpoints are initially anchors, use `T+2`; this changes no asymptotic result. Both endpoints are already included in every source grid regardless of which initialization is chosen.

## Targeted verification actually run

Ran one inline `python3 - <<'PY' ... PY` exact-`Fraction` check, without creating a test file. It varied `D` over `6,10,30`, `J` over `1,...,4`, and `r` over `1,...,3`, retained union grids through seven anchor rounds, and checked the fixed coordinate denominator and `W` divisibility of quadratic factor values, unary corrections, and accumulated message-like sums. All 252 anchor rounds and 3,183 node checks passed.

The same command checked zero objective, height bounds, and reconstruction neighborhoods at both distinct optimizers `(0,1/3)` and `(1,2/3)` of `x(1-x)+(y-(x+1)/3)^2` on the unit square; both passed. These examples corroborate arithmetic identities and recovery geometry. They do not substitute for the general proofs or exercise a complete nonunique DP implementation.

No project-wide checks were run. CI status and logs were not inspected.
