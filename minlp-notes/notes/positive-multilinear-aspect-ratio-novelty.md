# Novelty screen for sharp gap growth in positive-box aspect ratio

Date: 2026-09-04. Independent bounded primary-literature screen. The parent investigation reports independent mathematical audits of both bounds; some draft headers still say that reviews are pending. This note evaluates prior overlap and does not replace those audits.

## Assessment

No exact prior theorem was found for either the uniform positive-box bound over unrestricted dimensions and degrees or its sharp leading asymptotic

`C_box(rho) ~ rho` as `rho -> infinity`.

Here `C_box(rho)` is the worst pointwise ratio of the sum of exact individual-monomial envelope gaps to the envelope gap of their positive sum, over strictly positive boxes with maximum coordinate aspect ratio at most rho. The proposed results are [the sharp upper bound](../results/positive-multilinear-positive-box-sharp.md), [the matching lower family](../results/positive-multilinear-positive-box-lower.md), and [the earlier finite bound](../results/positive-multilinear-positive-box.md).

The closest prior theory explicitly provides the single-product envelopes on these boxes. The new comparison uses these classical envelopes but requires a common distribution for all overlapping products. The direct predecessor in the MINLP literature discusses numerical evidence on `[1,2]^5` and conjectures a universal constant over nonnegative boxes; the inspected statements do not give an aspect-dependent replacement.

Thus the candidate contribution is a dimension- and degree-independent quantitative theorem for arbitrary positive sums, with sharp linear growth in aspect ratio. This is a potentially substantial refinement of the original gap question. The evidence remains a bounded novelty screen, not proof that the theorem is unknown under every equivalent formulation.

## Closest exact envelope antecedents

Adams, Gupte, and Xu, *Error bounds for monomial convexification in polynomial optimization*, Proposition 4.1 in Section 4.1, explicitly records both envelopes for the product on `[1,r]^d`, attributing them to Benson 2004 and Tawarmalani--Richard--Xiong 2013. Their Theorem 1.3 and Section 4 analyze maximum absolute monomial-envelope errors. Their comparisons of convex and concave errors concern maxima for one monomial, and are not pointwise ratios for an arbitrary positive sum. [Primary manuscript, Proposition 4.1 and Section 4](https://www.pure.ed.ac.uk/ws/files/137020380/1704.00424.pdf).

Tawarmalani, Richard, and Xiong, *Explicit convex and concave envelopes through polyhedral subdivisions*, Theorem 4.6 of the June 2010 manuscript, gives the convex envelope for vertex data of the form `f(sum_i y_i)+a^T y` with convex f. Taking `f(s)=rho^s` directly supplies the piecewise-linear cardinality envelope used by the local proof. Their supermodular-envelope framework also supplies the classical common-threshold concave side. This primary manuscript was inspected directly, in addition to the attribution above. [Primary manuscript, Theorem 4.6](https://optimization-online.org/wp-content/uploads/2010/06/2640.pdf).

Specifically, for `x_i=1+(rho-1)u_i`, a product vertex has value `rho^(sum_i Y_i)`. Its convex envelope at the prescribed means is the linear interpolation of `rho^k` at `sum_i u_i`. No new claim should attach to this formula, the cardinality-slab integrality behind it, or common-threshold attainment of the concave envelope.

Nguyen, Richard, and Tawarmalani, *Deriving the convex hull of a polynomial partitioning set through lifting and projection*, develops exact hulls for bounded bivariate monomial relations and their packing/covering counterparts. These strengthen individual factorable relations; their inspected statements do not compare arbitrary sums of positive monomials. [Primary manuscript](https://optimization-online.org/wp-content/uploads/2014/02/4260.pdf).

Knowing each individual envelope is necessary here but insufficient: separate envelope optima can require incompatible joint distributions on their shared variables. Likewise, an upper bound on an absolute error does not provide a lower bound on the aggregate hull gap required in the denominator. A single monomial always has termwise/hull ratio one where its gap is positive, regardless of its absolute envelope errors.

## Direct relation to the original multilinear-gap question

Luedtke, Namazifar, and Linderoth, *Some Results on the Strength of Relaxations of Multilinear Functions*, Section 4, compares termwise and full-hull gaps for a positive polynomial on `[1,2]^5`. The discussion immediately before Conjecture 1 states that the observed closeness lacks an accompanying general theory. Conjecture 1 then proposes a uniform constant over positive-coefficient multilinear functions on nonnegative boxes. The same paper identifies the exact concave-envelope behavior for positive sums. [Primary author manuscript, Section 4 and Conjecture 1](https://jlinderoth.github.io/papers/Luedtke-Namazifar-Linderoth-12-TR.pdf).

The aspect theorem gives a qualified positive resolution when the coordinate endpoint ratios are uniformly bounded. The lower family proves that the allowable constant must increase at least linearly as that bound grows, even though every individual box stays strictly positive. This is stronger than perturbing a zero-box counterexample by an unspecified small positive amount: for each fixed rho, the family has actual ratios tending to rho as its dimension increases.

The finite-rho optimum remains undetermined. The current audited bounds give `C_box(rho)>=max{2,rho}` for every rho greater than one and an upper bound `rho+3 sqrt(rho)+O(1)` as rho grows. The lower bound two is the classical positive complete-bilinear-graph example transported by an affine scaling. It should not be presented as part of the new lower construction.

## Correlation and dependence comparisons

Let `C_e` be the exact concave value and `V_e` the exact convex value of physical monomial e at the given point. With positive weights c, write

`A=sum_e c_e(C_e-V_e)`,

`H=sum_e c_e C_e - min_Q E_Q[sum_e c_e m_e(X)]`,

where Q preserves every coordinate mean and is supported on the box vertices. The target ratio is `A/H`. The numerator permits a separate minimizing law for each term, while H requires one law. Standard correlation gaps instead compare an expected function value under optimal dependence with its expectation under independence. Bounds on such absolute values do not automatically survive subtraction from the concave value.

Agrawal, Ding, Saberi, and Ye, *Price of Correlations in Stochastic Optimization*, develops the standard fixed-marginal dependence-versus-independence comparison, with bounded-gap classes based on cost sharing and contrasting supermodular examples. The ratio and hypotheses differ from the positive-sum envelope comparison above. [Primary author manuscript](https://web.stanford.edu/~yyye/priceofcorrelation.pdf).

### Independence cannot give even a uniform fixed-box guarantee

Fix any rho greater than one. On `[1,rho]^2`, take one bilinear product and normalized endpoint-success means `(epsilon,1-epsilon)`, where `0<epsilon<=1/2`. Put `t=rho-1`. After removing its constant and affine terms, this product is `t^2 Y_1Y_2`. Its exact termwise and hull gaps are both

`T=t^2 epsilon`.

The deficiency of independent rounding relative to its concave envelope is

`D_I=t^2[epsilon-epsilon(1-epsilon)]=t^2 epsilon^2`.

Thus `T/D_I=1/epsilon` is unbounded while rho stays fixed. The actual termwise/hull ratio is one. This directly prevents a proof of fixed-rho finiteness using only independent deficiency as the common feasible witness. It explains the role of the additional correlated law in the proposed upper proof. The example does not exclude other deductions inspired by correlation-gap theory.

Nor does the earlier marginal-floor theorem immediately supply this result. A physical coordinate on `[1,rho]` is positive, but its endpoint-success marginal `(x_i-1)/(rho-1)` can approach zero. Envelopes on `[1,rho]^n` differ from envelopes on an enlarged zero-lower-bound box. Confusing these domains would incorrectly substitute a physical value bound for a Bernoulli-marginal bound.

## Candidate mechanisms and scope

The upper proof combines independence with random endpoint orientations, both preserving every mean and applying to all terms. The asymmetric split identifies the high means near one; estimates within the two groups and across them control the exact original-monomial gaps. The classical product-envelope formula is retained throughout. Positive affine expansion transfers the result from a common aspect ratio to smaller, unequal ratios while bounding the original termwise gap in the correct direction.

The lower proof adapts the local nested-block family to `[1/rho,1]`, where a failed leaf reduces a term by a factor rather than annihilating it. Its softened-coverage calculation shows that the termwise gap and actual hull gap have different linear-in-levels limits with ratio rho. The support family itself predates this extension within the repository; the fixed-positive-box calculation and matching upper asymptotic are the additional claims.

Searches covered positive and strictly positive boxes, constant-ratio product envelopes, aspect ratios in multilinear relaxation, original termwise-gap terminology, dependence and correlation gaps for products and supermodular functions, and curvature-based related terminology. No inspected primary theorem matches the aggregate aspect-ratio statement. Several queries produced irrelevant results, so search misses alone provide weak evidence. A publication should cite the exact envelope antecedents and the original gap conjecture, retain the distinction from absolute errors, and describe novelty as provisional until broader citation tracking is complete.
