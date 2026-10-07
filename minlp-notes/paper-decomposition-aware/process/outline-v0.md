# Working outline (v0, before verification results)

Title: Decomposition-aware global optimization: certified coordinate grids,
conditional recourse, and structural limits

Story: small treewidth alone does not make nonconvex mixed-integer
optimization tractable (box QP is strongly NP-hard at treewidth two). Two
quantitative properties make tree decompositions useful for certified global
optimization: an upper bound L on coordinate curvature (gives valid continuous
lower bounds from finite DP) and quadratic growth g at a unique optimizer
(gives accuracy-independent grid sizes). Exact conditional recourse lowers the
curvature that must be discretized or removes residual problems from
discretization. Explicit examples mark where each ingredient stops working.

1. Introduction (motivation, informal main results, related work, contributions)
2. Setting (model, decompositions, curvature, growth, encoding)
3. Corrected coordinate grids (interpolation lemma, DP and min-marginals,
   filtering, certificate)
4. Accuracy-independent grids under growth (graded grids, contraction,
   localization, state bound, unknown growth, main theorem, expanding-box
   chain example: exact messages exponential, grids polynomial)
5. Exact output (rational height, exact MIQP theorem, candidate acceptance,
   finite recovery without uniqueness, polynomial factors)
6. Conditional recourse (partial minimization preserves curvature/growth;
   convex responses and value factors; min-cut residual oracles; the
   conditional interface and why bag-local corrections fail)
7. Coupled constraints (TU fibers; XP not FPT)
8. Nonunique optima (endpoint full-set identity; diagonal certificates)
9. Structural limits (hardness vs conditioning, ETH and width, complete
   messages, local corrections, local moments, product domains, set growth,
   polynomial outputs)
10. Implementation and computational illustration
11. Conclusions and open problems
Appendices: deferred proofs

Candidate motivating example: the chain G(S,z) with S_t in [0,2^t-1]
(unique optimum, width 3, g = 1/8, L <= 10) has terminal Bellman messages
with 2^(m-1) quadratic pieces, while the corrected-grid method needs
O(sqrt(kappa) log n) labels per coordinate and O(m + log(1/eps)) stages.
