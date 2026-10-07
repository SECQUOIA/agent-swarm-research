# Front matter review, round 1

The structure and attribution boundaries are sound. Resolve the following scope overstatements during integration; these do not invalidate the technical results.

1. Abstract: 'finite agreement ... not the strength ... determines the rate' is too universal. The sharp examples show a persistent obstruction even with exact local measures; they do not characterize the rate for every sparse problem. State that finite separator information can limit the rate even with exact local measures.
2. Introduction first paragraph: compactness alone does not guarantee convergence of every ordinary quadratic-module hierarchy. State standard Archimedean assumptions, or restrict the initial convergence claim to the box hierarchies actually studied.
3. Introduction mechanism and Discussion: Lipschitz derivatives give an inverse-square approximation upper bound, not a universal exact order. Smooth or polynomial functions can approximate much faster. State upper bounds and sharp examples separately.
4. Discussion: 'a convex corner appears exactly when ... becomes active' is false. An affine private constraint can become active without a corner: min y^2 subject to y>=x, y>=0 has value x_+^2. Use 'can create a convex corner' and identify the multiplier discontinuity in the sharp example; no equivalence is proved.
5. Introduction table: the regular-multiplier row references the whole Holder theorem while reporting r^-2. Specify weighted Chebyshev regularity or coordinatewise Lipschitz (beta=1); put the general beta rate in prose/table footnote.
6. Introduction ordinary-module paragraph: 'product kernels are not available' is too broad; products of globally SOS kernels are available. The normalized interval-positive Jackson product does not generally have the required ordinary-module representation. Clarify this precise obstruction.
7. Introduction grid baseline: 'The same holds ... in the recourse setting' follows an explicit r^-2 sentence and could imply inverse-square affine recourse generally. State that grid/QP dynamic programming reaches the corresponding regime-dependent exponents; r^-1 is the general affine case.
8. Abstract 'far fewer' blocks applies to larger bags; use exact v+1 versus up to 2^v in the body, simple 'fewer' or omit in abstract.
9. Avoid unsupported 'all constants are explicit' if regularity statements use approximation constants whose numerical values are not supplied. Say finite-order bounds display the relevant parameter dependence.
10. Constrained lift comparison and named prior results remain provisional pending Luna source verification. Avoid broad negative literature claims until ledger finalized.

No experiments run. This review concerns the authored front matter and its correspondence to the audited theorem contracts, not a new literature search.

11. The grid baseline can also yield a certified lower bound by subtracting a proved discretization error from its grid optimum. Avoid suggesting that providing any lower bound is unique to the SOS result. The specific contribution is quantitative control of the stated sparse SDP and its feasible moment points, together with its algebraic certificate cone.
