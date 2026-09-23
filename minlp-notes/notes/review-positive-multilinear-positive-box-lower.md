# Independent audit: linear positive-box aspect-ratio lower bound

Date: 2026-09-04. Reviewer: `fbbt`, independently of the `multilinear` reviewer. Target: [the positive-box lower theorem](../results/positive-multilinear-positive-box-lower.md).

**Verdict: the complete written lower-bound proof is correct.** The termwise gap is exact, the softened-coverage identity is valid, both hull-gap bounds have the asserted leading term, and the actual ratio tends to `rho` for every fixed `rho>1`. Scaling gives `C_box(rho)>=max(2,rho)`. The separate upper theorem is not re-audited here; if its stated `O(rho)` bound holds, the linear-order conclusion follows.

## Model, normalization, and local minimum

Put `epsilon=1/rho` and `eta=1-epsilon`. A physical endpoint coordinate with normalized success bit X equals `epsilon+eta X`. For every term its physical product is `epsilon^R_total`, where `R_total` counts failed coordinates, including the anchor.

A level-j term has `k=m/b^j` leaves and anchor success mean `u_j=b^-j`. Therefore its expected total number of failures is `(1-u_j)+k/m=1`. The function `r -> epsilon^r` is convex for `0<epsilon<1`, so Jensen gives an expected product at least `epsilon` for every admissible local vertex law.

The bound is attained exactly: choose one failed coordinate, selecting the anchor with probability `1-u_j` and each leaf with probability `1/m`. These probabilities sum to one and give every required marginal. The resulting product is always `epsilon`. Thus the original, unexpanded monomial's convex-envelope value is exactly `epsilon`; this is not a claim about separately convexifying its normalized submonomials.

Using vertex laws is legitimate on the positive box. A multiaffine function equals the expectation of its endpoint values under independent rounding of each normalized coordinate, so its graph hull equals the convex hull of its endpoint graph.

## Local maximum and exact termwise sum

Positive products admit the common-threshold success coupling as a simultaneous concave-envelope optimizer. One way to justify this directly is to expand each product in normalized bits: all coefficients are nonnegative, and a common threshold maximizes every subproduct's intersection probability at once.

The anchor's success interval has length `u_j`, the leaves' common success interval has length `1-1/m`, and `u_j<=1-1/m`. The three resulting cases give

`C_term=u_j+epsilon(1-1/m-u_j)+epsilon^(k+1)/m`.

Subtracting the exact minimum `epsilon` yields `eta u_j-(epsilon/m)(1-epsilon^k)`. There are `b^j` terms at level j, so the first contribution sums to `eta` at each level. Reindexing `t=L-j` gives exactly

`T_L=eta L-D_L`, and `D_L=epsilon sum_(t=0)^(L-1) (1-epsilon^(b^t))/b^t`.

The geometric bound `0<=D_L<=epsilon b/(b-1)` is correct and uniform in L. Since `b=L^2>=4`, it is in particular bounded by `4epsilon/3`. Every normalized mean is strictly between zero and one, so all physical evaluation coordinates are strictly inside `[epsilon,1]`.

## Independent derivation of the full hull identity

Let `R_B` count failed leaves in B and set `s_B=1-epsilon^(R_B)`. Each term equals

`(epsilon+eta A_j)(1-s_B)`.

There are `b^j` copies of the same anchor at level j and its mean is `b^-j`; hence the expected sum of anchor bits over all terms is L. The complete concave-envelope value is `epsilon*(number of terms)+eta L-D_L`. Subtracting the expected polynomial gives

`epsilon E sum_(j,B) s_B + eta E sum_j A_j sum_B s_B - D_L`.

Taking the maximum over all common endpoint laws proves equation (4) exactly. In particular the correction `D_L` appears once with a minus sign; it is neither multiplied by epsilon again nor absorbed into the random maximum.

## Upper hull bound

Since `s_B<=1[R_B>0]`, the anchor-weighted term is at most `eta` times the maximum of `E sum_j A_j N_j` under the same normalized marginals. This is precisely the unit-box variable-radix hull objective. Its reviewed upper bound is `1+(L-1)/b` when `b>=L`, which holds for `b=L^2`.

The exact attaining law from that older result is stronger than this proof requires: only its elementary upper bound is used. No assumption that a single law simultaneously maximizes the two parts of equation (4) is made or needed. Bounding each part separately is a valid upper bound on their common-law maximum.

For the other term, `1-epsilon^r=eta sum_(h=0)^(r-1) epsilon^h<=eta r` for every nonnegative integer r. The level partitions imply `sum_B R_B=R`, and the total failure mean is one. Thus `E sum_(j,B) s_B<=eta L`. Multiplying by epsilon and combining gives

`H_L<=epsilon eta L+eta[1+(L-1)/b]-D_L`.

This verifies all constants and signs in the upper estimate.

## Lower hull bound and positivity

Choose exactly one uniformly random failed leaf. Each leaf then has failure probability `1/m`. At every level exactly one block has a failure, so `sum_B s_B=eta` deterministically. Give the anchors their prescribed marginals; independence from the leaf and from each other is a valid explicit choice, though the deterministic level sums make that independence unnecessary for this expectation.

The unweighted part is `epsilon eta L`, and the anchor-weighted part is `eta^2 sum_j b^-j`. This produces exactly the stated lower bound

`H_L>=epsilon eta L+eta^2 sum_j b^-j-D_L`.

For explicit positivity at every finite L, apply the same geometric inequality with `r=b^t`. Each summand of `D_L` is at most `epsilon eta`, so `D_L<=epsilon eta L`. Therefore this lower bound implies

`H_L>=eta^2 sum_j b^-j>0`.

Thus the constructed ratios are admissible even before passing to a sufficiently large L. This useful observation was sent to the author; eventual positivity already follows from the asymptotic squeeze.

## Limits and scaling

For fixed `epsilon in (0,1)`, `D_L=O(1)`, `sum_j b^-j<=1/(b-1)`, and `1+(L-1)/b=1+O(1/L)` with `b=L^2`. Dividing both hull bounds by L therefore yields `H_L/L -> epsilon eta`. The exact termwise formula gives `T_L/L -> eta`. Because `epsilon eta>0`, division is legitimate and the actual ratio tends to `1/epsilon=rho`.

This limit keeps rho fixed. Establishing a separate sequence for every fixed rho is sufficient to prove the pointwise supremum bound `C_box(rho)>=rho`; no uniformity in rho or exchange of two limits is required.

Under the coordinate map `x=rho*a`, each degree-d original term becomes `rho^-d` times the corresponding monomial in x. All coefficients stay positive, and the graph transformation preserves both envelope gaps exactly. The degree-dependent coefficients are allowed by the definition of `C_box`; no unit-coefficient claim on `[1,rho]` is required. If rho is rational, all finite-instance data remain rational.

For the other lower bound, the complete positive bilinear graph at normalized center has ratio `2(n-1)/n` for even n, tending to two. Affine expansion on the common interval `[1,rho]` changes each quadratic part by the same positive factor `(rho-1)^2` and adds affine terms. Both termwise and full gaps scale by that factor, so the ratio is preserved. Hence `C_box(rho)>=2` for every `rho>1`.

Combining the two separate families gives the stated maximum. Together with an independently established `O(rho)` upper bound it proves `Theta(rho)` **as rho tends to infinity**. It does not establish leading constant one, an exact formula for `C_box`, or unboundedness at a fixed positive-box aspect ratio.

## Exact small-instance checks

An independent check used the six-variable radix instance `L=2,b=2,m=4` as a small test of the general algebra. This is a toy radix value satisfying `b>=L`, not the selected asymptotic sequence `b=L^2`. All 64 endpoint vertices were enumerated. The individual term minima and maxima and the complete polynomial's two envelope values were solved as LPs. Floating-point solutions were converted to rational primal and dual candidates; every equality, nonnegativity constraint, dual inequality, and primal-dual objective equality was then verified exactly.

| epsilon | Exact termwise gap T | Exact hull gap H | Certified lower bound on H | Certified upper bound on H |
|---|---:|---:|---:|---:|
| 1/5 | 168/125 | 128/125 | 68/125 | 158/125 |
| 1/2 | 9/16 | 7/16 | 1/4 | 13/16 |
| 2/3 | 7/27 | 11/54 | 13/108 | 29/54 |
| 9/10 | 49/2000 | 39/2000 | 3/250 | 309/2000 |

Every local minimum was exactly epsilon, the summed local gap agreed with equation (2), and both global hull bounds held. These checks support the proof and are not assumptions behind the asymptotic result.

## Novelty boundary

This audit verifies a new use of the repository's variable-radix family on a fixed strictly positive box; it does not establish literature novelty. The local product envelopes, vertex-distribution representation, and common-threshold upper optimizer are established ingredients. Priority for the aspect-ratio conclusion should be assessed together with the separate upper theorem and its literature review.
