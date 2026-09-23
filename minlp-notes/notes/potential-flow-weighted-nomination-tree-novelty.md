# Weighted nomination optimization on trees: bounded source audit

Date: 2026-09-05. Candidate: [weighted nomination tree hardness](potential-flow-weighted-nomination-tree-hardness.md). This is a source comparison, not a proof audit.

The underlying convex knapsack mechanism has a direct primary antecedent. The proposed result is best retained as a precise passive-flow consequence and a boundary on extending the repository's pairwise-pressure algorithms. No matching statement for a degree-three passive quadratic tree, fixed resistances, a balanced nomination box, and a growing-support potential objective with coefficients in `{−1,+1}` was located in the bounded search. This is a narrower assessment than a claim of a new hardness mechanism or the first hard potential-flow problem on trees.

## Direct convex knapsack predecessor

Retsef Levi, Georgia Perakis, and Gonzalo Romero, *A continuous knapsack problem with separable convex utilities: Approximation algorithms and applications*, Operations Research Letters 42, 367–373 (2014), DOI 10.1016/j.orl.2014.06.007, [open author-hosted publication](https://www-2.rotman.utoronto.ca/facbios/file/CKP%20ORL.pdf). Proposition 1, printed page 368 / PDF page 2, reduces Subset Sum using the objective `sum_i[x_i−x_i(u_i−x_i)]` over `0<=x_i<=u_i` and `sum_i x_i<=B`. Its upper bound `B` is attained exactly by endpoint choices forming a target subset. Section 2 uses extreme-point attainment for convex maximization. The paper credits Sahni's 1974 work as a predecessor to the proof method; that older paper was not independently inspected here.

Our comparison: the candidate uses the same endpoint-deficit principle, with the nonnegative increasing pure quadratic `sum_i y_i^2/w_i` and exact balance `sum_i y_i=K`. Its deficit is `sum_i y_i(w_i−y_i)/w_i`. The passive leaf laws realize these quadratic terms directly, while the weighted potential functional cancels backbone drops. This is a useful restricted network realization of known convex knapsack hardness, not a distinct combinatorial idea. Convex maximization, extreme-point attainment, and an at-most-one-interior-coordinate vertex are standard ingredients.

The candidate additionally records the absolute gap `1/2` for its chosen normalization and a direct rounding argument for near-optimal nominations. Those are elementary quantitative consequences of this construction. They support absolute-error-`1/8` hardness without additional resistance scaling. The objective range and integer nomination bounds grow with the input, so no relative-error, strong-hardness, or normalized-objective hardness claim follows. Existing relative-approximation results for convex knapsack are therefore compatible with this gap.

## Relevant potential-flow distinctions

Lars Schewe, Martin Schmidt, and Johannes Thürauf, *Computing technical capacities in the European entry-exit gas market is NP-hard*, DOI 10.1007/s10479-020-03725-2, [open primary PDF](https://d-nb.info/1219137715/34). Model (4), PDF page 6, maximizes a weighted sum of technical capacities, whose feasibility quantifies over all compliant nominations. Theorem 4.9, PDF page 23, proves NP-completeness on trees for nonlinear potential-based flows. Theorem 4.10 also treats linear potential-based flows. The weights apply to capacity decisions, and the robust feasibility condition includes physical potential bounds.

Our comparison: this is already tree hardness in the potential-flow setting. It is not the candidate's maximization of a potential functional over one fixed nomination box, with fixed resistances and no scenario-feasibility filtering. Cite it to prevent an overbroad “tree potential optimization is newly shown hard” claim. Optimizing the uncertainty set itself and evaluating a weighted objective over a given uncertainty set are different tasks.

Johannes Thürauf, *Deciding the feasibility of a booking in the European gas market is coNP-hard* (2022), DOI 10.1007/s10479-022-04732-1, [open publisher article](https://link.springer.com/article/10.1007/s10479-022-04732-1). Section 2, model (2), optimizes a single pairwise potential difference over bounded balanced nominations with fixed pressure-loss coefficients. The source proves general-graph hardness and explains the established polynomial tree and one-cycle cases. The objective has two distinguished terminals.

Our comparison: an arbitrary weighted sum of individually tractable pressure differences need not remain tractable, because the terms must use one common nomination. The candidate's `2n` supported vertices are therefore essential to its stated boundary. It does not refute fixed-pair results and does not resolve the separately investigated fixed-objective-support case. Fixed nominations on a tree remain a different easy setting: conservation determines all flows and weighted potential objectives become linear in multiplicative resistance coefficients.

## Recommended claim and remaining scope

Recommended wording: “A direct realization of classical convex knapsack hardness shows that growing-support weighted potential optimization over a balanced nomination box is NP-complete on a specified family of degree-three quadratic passive trees. The construction uses fixed positive resistances and objective coefficients of magnitude one, and gives a constant absolute gap. Thus bounded cycle rank alone cannot extend pairwise-pressure nomination algorithms to arbitrary weighted objectives.”

The result is a supporting complexity boundary rather than a high-impact standalone advance in convex knapsack theory. Its value increases if combined with a proved positive theorem for fixed objective support. Such a theorem would require its own source and proof review; none is inferred here.

The NP-membership argument in the candidate applies to its explicitly specified convex tree family and uses rational vertex nominations. This audit does not promote that argument to arbitrary weighted potential objectives on arbitrary trees, where the objective can have a different curvature pattern.

Searches combined weighted potential and pressure objectives, robust nomination optimization on trees, continuous convex knapsack, quadratic Subset Sum reductions, and technical-capacity complexity. Direct primary evidence supports the comparisons above. No equivalent restricted weighted-nomination flow statement was found, but this is not exhaustive novelty clearance. PDF page numbers refer to the linked files, not literature-package citations.
