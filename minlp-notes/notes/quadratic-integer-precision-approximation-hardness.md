# Integer precision approximation hardness: investigation record

Date: 2026-09-05. The candidate passed two proof audits and a bounded
novelty review and was promoted to
[the result file](../results/quadratic-integer-precision-approximation-hardness.md).

Zero integer dimension for a convex Max-Cut graph quadratic is
coNP-complete to recognize. Polynomial replication, plus a one-integer
convex square baseline, gives a positive-optimum gap of `1` versus at
least `t+1`. Unless `P=NP`, no polynomial-time formulation construction
can guarantee additive or multiplicative `O(N^(1-delta))` approximation
for fixed `delta>0`, even at unit tolerances with positive optimum.

[First audit](review-quadratic-precision-approximation-hardness.md),
[second audit](review-quadratic-precision-approximation-hardness-second.md),
and [novelty assessment](quadratic-precision-approximation-hardness-novelty.md)
record the scope and checks. The result does not exclude `N/log N`
additive approximation.
