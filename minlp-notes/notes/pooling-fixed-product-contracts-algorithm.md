# Conserved-product-mass pooling algorithm: promoted result

Date: 2026-09-05. The complete, twice-reviewed proof is maintained in
[the result file](../results/pooling-fixed-product-contracts-algorithm.md).

The theorem permits one pool, a fixed number of pool outlets, arbitrarily
many feeds and qualities, and degree-two bypass paths. All inputs have
exact supplies; nonreceiving products have exact demand and exact quality.
Global mass and attribute conservation then eliminate the dense pool
balances. Feasibility and standard input-cost/output-revenue optimization
are polynomial in rational bit time. Arbitrary dense arc costs remain
outside the theorem.

Both [independent](review-pooling-fixed-product-contracts.md)
[audits](review-pooling-fixed-product-contracts-second.md) pass. The
retained code passes 90 original/substituted fixed-split fiber comparisons
and an exact-quality-assumption negative control. The result file states
the exact scope of these numerical checks and the qualified source
comparison.
