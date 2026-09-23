# Independent audit: one-monomial envelope hardness on narrow boxes

Date: 2026-09-04. Reviewer: `review_common_factor`, independent of the author.

**Verdict: the reduction and NP-completeness statement pass the mathematical audit.** Reviewed result: [exact one-monomial envelope hardness](../results/positive-box-single-monomial-hardness.md). This establishes the stated complexity boundary; it does not establish publication novelty.

## Reduction and exact remainder bound

Doubling every positive PARTITION input preserves the answer and makes its total `A` even, including when the original total was odd. For any integer `K≥1`, the choice `ε=1/(16KA³)` gives positive rational widths and `εA≤1/16`. The physical midpoint becomes the vector of normalized Bernoulli means one half.

The function remains one unit-coefficient multiaffine monomial in the physical variables. Independent Bernoulli interpolation replaces any interior graph point by a distribution of corner graph points with the same coordinate means and function value. Thus the envelope is exactly a finite distribution LP; the proof does not assume that an optimizing distribution itself has independent coordinates.

For a binary vector, the degree-two expansion is exact because `z_i²=z_i`:

```
∏_i(1+εa_i z_i)
 =1+εS+(ε²/2)(S²−Σ_i a_i²z_i)+R(z).
```

All omitted terms are nonnegative. The elementary symmetric sum of order `k` is at most `A^k`, so the infinite geometric majorant is valid even though the original polynomial is finite. Consequently

```
0≤R(z)≤(εA)³/(1−εA)≤2ε³A³=ε²/(8K)≤ε²/8.
```

The constants and direction of every bound check. Empty higher-order tails for fewer than three variables cause no problem.

## YES and NO separation

Every feasible distribution has `ES=A/2` and `EΣa_i²Z_i=(1/2)Σa_i²`. Substitution gives precisely the draft's baseline

```
b=1+εA/2+ε²(A²/8−Σa_i²/4),
E m(X)=b+(ε²/2)Var(S)+ER.
```

For a YES instance, a partition subset and its complement each have total `A/2`. Their equal mixture gives every coordinate mean one half and zero variance. Its expected product is at most `b+ε²/8`.

For a NO instance, every binary total is an integer different from the integer `A/2`. Therefore every state has squared distance at least one and every feasible distribution has variance at least one. Since the remainder is nonnegative, its expected product is at least `b+ε²/2`. The proposed threshold `q=b+ε²/4` lies strictly between the two bounds. No limiting argument or numerical comparison is needed.

An equivalent explicit NO-instance dual certificate is the affine function

```
L(z)=1−ε²A²/8+ε²/2
     +Σ_i [εa_i+(ε²/2)(Aa_i−a_i²)]z_i.
```

At every binary vertex,

```
m(z)−L(z)=(ε²/2)[(S(z)−A/2)²−1]+R(z)≥0.
```

Multiaffinity extends this bound over the normalized box, and its midpoint value is `b+ε²/2`. This certificate is consistent with the variance proof and makes the NO separation directly checkable.

## Complexity and scope

`log A` is polynomial in the PARTITION input length. The widths and threshold use rational expressions with polynomial encoding length. Vertex product values also have polynomial bit length, since multiplying `n` rational input factors adds their encoding lengths up to a polynomial bound. Computing the reduction is therefore polynomial in binary input length, despite the small threshold gap.

For each fixed rational `η>0`, choosing a fixed integer `K` with `1/(16K)≤η` places all boxes in `[1,1+η]^n`. This makes the fixed-neighborhood hardness quantifier explicit. The theorem concerns varying coordinate upper bounds inside that box, not the common-aspect-ratio box with all upper bounds equal.

NP membership is valid. The feasible distribution polytope is nonempty and compact. An optimal basic feasible solution uses at most `n+1` binary states. Its probabilities are determined by a nonsingular zero-one basis with half-integer right-hand side; determinant bounds give polynomial-size rational probabilities. Listing those states and probabilities supplies a certificate whose normalization, means, and expected product threshold can all be checked with exact rational arithmetic. This proves NP-completeness of the decision problem, not merely NP-hardness of evaluation.

The PARTITION reduction does not establish strong NP-hardness. Its gap is of order `A^−6` and may be exponentially small in input bit length, so it does not establish hardness at fixed additive accuracy or a constant-factor approximation barrier. Calling it a PARTITION-based, ordinary NP-hardness result is accurate; no stronger hardness classification is inferred. With one factor, the termwise and scalar relaxations coincide: the difficulty is evaluating the individual envelope.

## Independent exact validation

I wrote and ran [an independent verifier](../code/audit_single_monomial_hardness.py), using exact rational arithmetic throughout. All 120 seeded instances passed: 28 YES and 92 NO cases. It checked the uniform remainder bound on 12,420 binary vertices, complementary-pair primal certificates for YES cases, and the affine lower certificate above for every vertex of each NO case. Several values of `K` and odd original totals are included. These finite checks supplement the proof and use no floating-point envelope solver.

The author is separately checking the primary literature. Broad hardness results for multilinear optimization alone do not settle novelty of this particular single-monomial, positive-box, midpoint restriction, and this audit makes no priority claim.

## Subsequent corollaries checked

The added scalar graph-hull membership corollary also passes. The equal mixture of the two extreme box corners attains the midpoint concave envelope. Its quadratic expansion gives `C−b≥ε²A²/8≥ε²/2`, strictly above the threshold offset. Hence the same reduced point lies in the scalar graph hull exactly in the YES case. NP membership follows from a basic rational convex combination of at most `n+2` corner graph points; the rational function-value row has polynomial encoding length, so determinant bounds still give polynomial-size probabilities.

The fixed-number-of-aspect-ratios qualification is correct. Within each ratio group, fixing the number of upper-bound coordinates fixes the product value. A dual separation objective then chooses the largest dual coefficients in that group. Sorted prefix sums and enumeration of at most `(n+1)^k` count tuples provide exact separation in `n^{O(k)}` time, with polynomial rational arithmetic cost for fixed `k`. The bounded-dual argument applies after bounding binary product values by their polynomial-bit endpoint product. Positive lower-bound scaling and substitution of fixed coordinates preserve the argument. This is appropriately described as an elementary classical consequence, without a novelty claim.

The subsequent connection to rank-one multimarginal optimal transport and the published logarithmic-precision question has a [separate independent source and mathematical audit](review-rank-one-mot-precision.md), including the input-padding and bit-complexity qualifications.
