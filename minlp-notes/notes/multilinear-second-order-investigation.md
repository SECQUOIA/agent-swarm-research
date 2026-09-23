# Optimizing the harmonic mixture beyond leading order

Date: 2026-09-04.

The complete theorem is in [the second-order upper-bound result](../results/positive-multilinear-second-order-upper.md). It preserves the harmonic coupling and improves its mixture with threshold coupling. Independent review is in [the second-order audit](review-multilinear-second-order.md).

The final bound also tunes the harmonic cutoff. Choosing N=1+ln(d−1) and M=(d−1)N gives the stronger bound

    R(d)≤N/[ln N−ln ln N+o(1)]+2/(1−e^−1).

The finite certificate uses L=1+ln M, ρ=(d−1)/M, and w=W(L exp(−ρ)):

    R(d)≤L/[w−1/(2w)]+2/(1−e^−1)   whenever w≥1.

The derivation below records the simpler initial cutoff M=d−1. The final theorem leads with the general cutoff and the best explicit tuned corollary, and retains that initial case as an illustration.

## What changed

The previous proof split hard monomials into two classes according to their largest failure marginal. That loses part of the harmonic integral. Retaining the whole integral gives the two simultaneous deficiency bounds

    threshold/T ≥ z,
    harmonic/T ≥ J_L(z),
    J_L(z)=∫_z^1 [1−exp(−(1−v)/(Lv))]dv,

where z=min(p_max/T,1) and L=1+ln(d−1).

Convexity shows that the best common mixture based on these bounds is obtained at the unique fixed point J_L(z_L)=z_L. Its hard-term guarantee is exactly z_L. Combining it with independence gives

    R(d)≤1/z_L+2/(1−e^−1).

This bound is constructive: solve one scalar equation depending only on maximum degree, then sample one of the three explicit common-marginal couplings.

The fixed point satisfies

    L z_L=ln L−ln ln L−1+o(1).

With w=W(L/e), the finite certificate

    L z_L≥w−1/(2w)       for w≥1

is accurate through its first reciprocal correction:

    L z_L=w−1/(2w)+O(w^−2).

This proves an upper bound only. It does not establish that the second-order loss is necessary for the actual optimal convex-hull gap.

## Numerical check

[The verification script](../code/verify_multilinear_second_order.py) solves the fixed-point equation in logarithmic integration coordinates to avoid small endpoints. It checks both explicit lower certificates. Its output on 2026-09-04 included:

| ln L | L z_L | W(L/e) | L z_L−(ln L−ln ln L−1) |
|---:|---:|---:|---:|
| 4 | 2.12380691 | 2.20794003 | 0.51010127 |
| 10 | 6.98676546 | 7.04734855 | 0.28935055 |
| 50 | 45.17835532 | 45.18914314 | 0.09037833 |
| 200 | 193.73095097 | 193.73351641 | 0.02926834 |
| 500 | 492.79888458 | 492.79989680 | 0.01349268 |

The numerical checks supplement the analytic proof; they are not rigorous floating-point certificates.

## Barrier for changing the radix of the lower construction

The root investigation proposed checking nested radix-b partitions, with b an integer at least two. Use m=b^ell leaves, ell anchors with means b^−j, and b^j disjoint blocks at level j. The quantile intervals where exactly the first l anchors are selected have probabilities

    w_l=(b−1)b^(−l−1)   for l<ell,
    w_ell=b^−ell.

For the concave resource-allocation surrogate, the total capacity having marginal slope at least s is

    B_s=[(ell−s)(b−1)+b]/b^s.

To verify this, at quantile level l≥s the relevant capacity is b^(l−s+1), including the first segment of slope l when l=s. Summing w_l times this capacity for l=s,...,ell gives the displayed formula.

The fixed-radix transition B_s≈1 occurs at s=log_b ell+O_b(1), so the hull gap remains log_b ell+O_b(1). Since ln m=ell ln b, this produces the same leading order as the dyadic construction. Merely taking b to grow does not visibly produce the negative ln ln ln term needed to match the new upper denominator: the transition itself includes ln(b−1), and multiplying the additive hull terms by ln b incurs a further cost. This is a barrier for this direct radix modification, not a universal impossibility theorem about all non-dyadic or weighted constructions.

## Open questions

- Is the second-order denominator ln ln d−ln ln ln d+o(1) achievable by a different positive polynomial?
- Can a better common-marginal coupling eliminate the ln ln ln d loss in the universal bound?
- Are weighted or overlapping block families able to separate those possibilities?

The known scalar-curve mixture optimum only restricts mixtures assessed through the two displayed guarantees. It does not restrict mixtures using additional structural information, and it does not show either guarantee is simultaneously tight for a polynomial family.
