# Fixed global rank and weighted support: source assessment

Date: 2026-09-05. Candidate: [joint weighted optimization at fixed global rank and support](potential-flow-fixed-support-global-rank.md). This short note extends the [fixed-support tree source audit](potential-flow-fixed-support-weighted-tree-novelty.md). It is not a proof audit; the candidate is undergoing separate mathematical reviews.

No matching exact polynomial-bit theorem was located for **joint** balanced nomination-box and positive interval-resistance optimization, with both total cycle rank `r` and weighted potential support `p` fixed. The plausible contribution is this combined structural guarantee. Its perturbation and fixed-core machinery are inherited from earlier repository work; joint uncertainty, cycle coordinates, flow-sign arrangements, and fixed-dimensional algebraic optimization have established predecessors. The search supports qualified novelty, not an unqualified first-result claim.

## Primary antecedents

Aßmann, Liers, Stingl, and Vera, *Deciding Robust Feasibility and Infeasibility Using a Set Containment Approach: An Application to Stationary Passive Gas Network Operations* (2018), [primary preprint](https://arxiv.org/pdf/1808.10241), DOI 10.1137/17M112470X. Section 4.1.4 studies positive interval resistance uncertainty with fixed nominations. Proposition 4.7, PDF page 19, already bounds flow-sign regions by a hyperplane arrangement in the global-cycle-rank circulation space. Section 4.3.3 and Proposition 4.11 treat a single cycle through polynomial subproblems. The general computational approach uses SOS relaxations. The inspected source does not provide the candidate's sparse-objective nomination-face reduction or exact combined complexity theorem.

Aßmann, *Exact Methods for Two-Stage Robust Optimization with Applications in Gas Networks* (2019), [primary thesis](https://d-nb.info/1196351791/34). Equations (3.3)–(3.4), printed page 56 / PDF page 74, include balanced demand intervals and independent resistance intervals. Chapter 5, printed pages 108–110 / PDF pages 126–128, formulates joint worst-case potential-drop problems. Thus the joint uncertainty model is established. The earlier [joint uncertainty audit](potential-flow-joint-resistance-novelty.md) records the inspected passages and the unavailable final Networks article, DOI 10.1002/net.21871.

Labbé, Plein, Schmidt, and Thürauf, *Deciding feasibility of a booking in the European gas market on a cycle is in P for the case of passive networks* (2021), [publisher primary text](https://onlinelibrary.wiley.com/doi/full/10.1002/net.22003), DOI 10.1002/net.22003. The paper reduces fixed-law, pairwise nomination optimization on one cycle to polynomial systems of fixed dimension. Structural reduction followed by real algebraic optimization is therefore a direct passive-flow predecessor. The candidate changes the objective and uncertainty scope, and permits a fixed number of cycles rather than one cycle.

## Comparison with the repository's earlier results

| Result | Nominations | Resistance uncertainty | Objective | Graph parameter and output |
|---|---|---|---|---|
| Earlier fixed-nomination weighted companion | Fixed | Independent intervals | Arbitrary rational zero-sum weights | Fixed total cycle rank; exact algebraic optimization |
| Fixed-support tree candidate | Balanced rational box | Independent intervals or finite sets | Support at most `p` | Tree; exact rational optimization for fixed `p` |
| Earlier pairwise block-rank algorithm | Balanced rational box | Fixed resistances, with a separate interval extension | One prescribed pairwise difference | Fixed maximum rank per block; certified additive values and rational near-optimal scenario data |
| Current candidate | Balanced rational box | Independent positive intervals | Support at most `p` | Fixed **total** rank and `p`; exact algebraic values and optimizing scenario |

The first row leaves only circulations in the nonlinear core because nominations are fixed. The current candidate must also reduce the many nomination coordinates, which is the material new step. The second row exploits tree flow independence from resistances and does not extend its finite-resistance conclusion to cycles. The third row permits arbitrarily many cyclic blocks, so its topology scope is broader than a fixed total-rank bound; its pairwise objective and additive output are different restrictions. None of these statements should be conflated with the others.

Within the candidate proof, objective-free pendant pruning and degree counting leave `O(r+p)` marked vertices and suppressed paths. The positive-source objective perturbation then limits free nominations along each path, including returning paths. This extends the repository's reviewed perturbation argument to a weighted objective on the whole reduced graph. Exact optimization on the resulting faces is an application of the existing fixed-core/polyhedral-block theorem. It is best presented as one combined extension, not as several independent new algorithms.

## Limits on the claim

The exponent may depend on `r,p`; this is not a fixed-parameter tractable or strongly polynomial claim. Cyclic outputs can be algebraic, so the rational-output strengthening of the tree theorem is not inherited. No extra flow or potential restrictions may filter the scenario set.

Independent finite resistance choices are deliberately excluded: the repository's support-three, one-cycle weighted hardness result rules out that extension unless `P=NP`. Fixed support with only a bound on **each block's** rank is not settled by this proof. Multiple active blocks can exchange nomination totals, making intermediate block contributions algebraic functions of shared decisions rather than constants; summing fixed block values does not solve that optimization problem.

Recommended wording: “For passive quadratic networks, fixed total cycle rank and fixed support of a weighted potential objective permit exact polynomial-bit joint optimization over balanced nomination boxes and independent resistance intervals. This extends the fixed-nomination and two-terminal structural algorithms; no equivalent combined guarantee was found in the open primary sources inspected.” Use only after the mathematical reviews accept the full output and complexity claims.

Fresh searches combined potential-based flows, cycle rank, weighted objectives, nomination uncertainty, and uncertain friction with the primary anchors above. No matching theorem surfaced. General circuit-tolerance priority gaps and general fixed-core algorithm comparisons remain as recorded in the linked audits; this bounded extension does not resolve them. External page references are one-based positions in the linked PDFs, except where printed page numbers are explicitly identified.
