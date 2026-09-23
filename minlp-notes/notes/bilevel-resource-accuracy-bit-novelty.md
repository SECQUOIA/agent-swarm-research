# Source assessment: resource-coupled bilevel optimization in accuracy bits

Date: 2026-09-05. This is a focused primary-source comparison for the
[one-resource result](bilevel-one-resource-accuracy-bit-algorithm.md) and
[fixed-resource extension](bilevel-fixed-resource-accuracy-bit-algorithm.md).
No matching theorem was identified in the sources checked. This is bounded evidence, not an exhaustive priority certificate. Mathematical audits are recorded separately.

## Scope of the candidate contribution

There are arbitrarily many box-bounded follower variables with separable strictly convex polynomial local costs. A fixed number of rational resource rows couples them; the row coefficients are independent of the leader. The leader dimension is fixed, its domain is a rational polytope, and its objective is an arbitrary signed affine function of the leader and unique follower response. No upper constraint depends on the response. The output is an exactly feasible rational leader with additive error `2^(-B)` and a rational optimum estimate, in time polynomial in input bits, numerical polynomial degree, and `B`.

The one-equality proof uses a particularly sharp identity: the absolute resource residual equals the weighted one-norm response error along its scalar dual-response curve. With several rows, a classical linear feasibility error bound and a polynomial uniform-convexity estimate replace that identity. Neither scalar multiplier search nor approximate convex follower solution is the proposed novelty. The candidate distinction is global optimization of the generally nonconvex induced upper objective within an accuracy-bit budget.

## Resource allocation and accuracy bits are established

Hochbaum and Shanthikumar, *Convex Separable Optimization Is Not Much Harder than Linear Optimization*, JACM 37(4), 843–862 (1990), explicitly give logarithmic dependence on inverse accuracy for continuous separable convex optimization. Their Theorem 1.1 has a subdeterminant-dependent size term; Section 5 discusses finite-precision function evaluation. Thus it would be incorrect to claim that logarithmic accuracy dependence for resource allocation itself is new. Their optimization variable is the resource allocation vector and their objective is its separable convex cost. They do not optimize an independently signed objective of the allocation response over leader parameters. [Primary author PDF](https://hochbaum.ieor.berkeley.edu/html/pub/Hochbaum-Shanthi-JACM90.pdf).

Patriksson and Strömberg, *Algorithms for the continuous nonlinear resource allocation problem—new implementations and numerical studies*, present inverse-marginal formulas, breakpoint methods, and scalar dual balance algorithms. Their equation (17) is explicitly a clipped inverse response. Section 6 and Remark 9 distinguish dual residual or multiplier error from primal response error. The current scalar residual identity is an elementary consequence of the same monotonicity and linear resource structure; it should not be advertised as a new dual-decomposition principle. The paper studies solution of the resource allocation problem, rather than a global signed bilevel objective. [Primary manuscript](https://arxiv.org/html/1501.07035).

Hoffman's 1952 theorem bounds distance to a nonempty linear inequality system by its positive violations. The fixed-row proof uses precisely this established error-bound principle; its projection and integer-minor calculation merely supply a self-contained coarse constant whose encoding is polynomial. The derivation does not establish a new Hoffman theorem. [Original NBS paper, pp. 263–265](https://nvlpubs.nist.gov/nistpubs/jres/049/4/V49.N04.A05.pdf).

## Closest algebraic-sum optimization predecessor

Vigneron's *Geometric Optimization and Sums of Algebraic Functions* gives approximation schemes for sums of bounded nonnegative algebraic terms over fixed-description semialgebraic domains. The manuscript's Theorems 6 and 9 and Section 2.3 include polynomial dependence on inverse accuracy and explicitly discuss the bit model. It supplies an important earlier way to avoid exact sum-of-roots comparison. The present response family is more restricted, permits signed upper coefficients, and seeks polynomial dependence on accuracy bits together with exact rational leader feasibility. Converting signed terms to nonnegative ones does not convert a general inverse-accuracy scheme into an accuracy-bit algorithm. [Author manuscript](https://antoinevigneron.github.io/manuscripts/rational.pdf); [the prior detailed local comparison](bilevel-bounded-power-accuracy-bit-novelty.md).

## Fixed dimensions in bilevel optimization

Ketkov and Prokopyev, *On the Complexity of Bilevel Linear and Quadratic Programs in Fixed Dimensions*, arXiv:2511.15592v2, revised June 10, 2026, prove fixed-follower-dimension and fixed-follower-constraint-count results for linear and quadratic bilevel models. Their Table 2 and Theorems 4–6 distinguish convex quadratic optimistic and pessimistic settings. The proof of Theorem 4 uses conic Caratheodory to retain a bounded number of active follower normals. That is an antecedent for active-normal compression, not a new ingredient of the present proof. Here the follower dimension and its box-constraint count grow, while leader dimension and the additional resource-row count are fixed; separability and strict convexity are material. The new result does not settle their general open case of an optimistic convex quadratic follower with fixed total follower constraints. [Primary v2 manuscript](https://arxiv.org/html/2511.15592v2).

The fixed-variable polynomial optimization and sampling tools are also classical. The current argument uses polynomially many rational inverse-approximation cells in the fixed combined leader/multiplier dimension and preserves only their rational polyhedral constraints when recovering a rational leader. The audited [bounded-power algorithm](../results/bilevel-bounded-power-accuracy-bit-algorithm.md) records the precise real-algebraic interface. This is a composition theorem, not a new quantifier-elimination method.

## Limits of this comparison

Searches included combinations of “bilevel,” “separable convex,” “resource allocation,” “fixed dimension,” “fixed coupling constraints,” “algebraic functions,” and “logarithmic accuracy.” Primary resource-allocation, algebraic-sum, linear error-bound, and recent fixed-dimension bilevel sources were checked directly. The checked sources did not contain the combined global bilevel theorem stated above. Related terminology is broad, and an unindexed or differently phrased theorem could still exist.

The claimed running time is a bit-complexity existence result with exponents depending on the fixed dimensions. It is not an implemented efficient global solver. The sparse binary-degree output obstruction, arbitrary dense follower coupling, and exact algebraic-sum comparison remain distinct boundaries. Independent agent audits establish additional confidence in the proof; they are not peer review or publication-priority verification.
