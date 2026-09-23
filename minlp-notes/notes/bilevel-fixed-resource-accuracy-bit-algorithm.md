# Fixed-resource bilevel optimization in accuracy bits

The completed theorem is now in
[the result file](../results/bilevel-fixed-resource-accuracy-bit-algorithm.md).
For fixed leader dimension and resource-row count, it gives an exactly feasible rational leader and additive `2^(-B)` optimum estimate in time polynomial in input length, numerical degree, and `B`. It covers arbitrary dense strictly convex univariate polynomial local follower costs, including signed coefficients.

Both [the first independent audit](review-bilevel-fixed-resource-accuracy-bit-algorithm.md) and [the second](review-bilevel-fixed-resource-accuracy-bit-algorithm-second.md) passed the complete positive-coefficient proof and the signed-marginal extension. The general inverse dependency has its own two full audits.

The [source assessment](bilevel-resource-accuracy-bit-novelty.md) records established ingredients and qualified novelty status. Extra response-dependent upper constraints, leader-dependent resource matrices, arbitrary resource-row counts, and sparse binary-degree guarantees remain outside the theorem.
