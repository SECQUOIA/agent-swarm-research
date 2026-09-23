# Novelty audit: joint nomination and resistance uncertainty

Date: 2026-09-05. Scope: an independent, bounded primary-literature audit of [the candidate joint theorem](potential-flow-joint-resistance-investigation.md). This is a novelty assessment, not a proof review.

The proposed structural complexity conclusion remains a plausible research contribution. The underlying joint uncertainty model and worst-case potential-difference optimization problem are already in the literature. The defensible claim is a certified additive algorithm with polynomial bit complexity when the **maximum cycle rank of a biconnected block is fixed**, allowing arbitrarily many blocks, nominations, and uncertain resistances. No matching complexity theorem was found in the primary sources inspected below. This is evidence of a gap, not proof that no prior result exists.

## Closest primary sources

### Aßmann, Liers, and Stingl (2019)

[Decomposable robust two-stage optimization: An application to gas network operations under uncertainty](https://onlinelibrary.wiley.com/doi/abs/10.1002/net.21871), *Networks* 74(1), 40–61, DOI 10.1002/net.21871. The publisher abstract explicitly includes demand and pipe-parameter uncertainty, reduces a two-stage model using subproblem optimum values, and describes conservative computational approximations. Thus simultaneous uncertainty, worst-case subproblems, and decomposition are not new concepts here. The complete published article was not successfully retrieved: the publisher full-text request failed, and the institutional preprint page returned a bot challenge. No bypass was attempted.

A closely related open primary source is the author's [2019 thesis, *Exact Methods for Two-Stage Robust Optimization with Applications in Gas Networks*](https://d-nb.info/1196351791/34). It says Chapter 5 repeats and extends the Networks work (printed pp.103–104; PDF pp.121–122). Its equations (3.3)–(3.4), printed p.56/PDF p.74, already define independent positive resistance intervals and arbitrary real demand intervals intersected with balance. Equations (5.19), (5.30), and (5.33), printed pp.108–110/PDF pp.126–128, formulate joint demand/resistance worst-case potential-drop subproblems. Sections 5.2.2–5.2.3 solve relaxations through piecewise-linear MILPs. The inspected chapter supplies no bounded-block-cycle-rank polynomial bit-time guarantee. The thesis is a separate source; it should not be represented as verification of every detail of the final journal version.

### Aßmann, Liers, Stingl, and Vera (2018)

[Deciding Robust Feasibility and Infeasibility Using a Set Containment Approach: An Application to Stationary Passive Gas Network Operations](https://arxiv.org/pdf/1808.10241), arXiv:1808.10241; journal DOI 10.1137/17M112470X.

Section 4.1.4, PDF p.15, fixes nominations and considers uncertain positive pressure-loss coefficients. Proposition 4.7, PDF p.19, **already proves** that the number of feasible flow-sign regions is at most `sum_{i=0}^k binom(m,i)=O(m^k)` for global cycle rank `k`, using affine circulation coordinates and hyperplane arrangements. This mechanism must be credited. Section 4.2 treats trees using linear programming. Section 4.3.3 and Proposition 4.11, PDF pp.20–21, reduce a single cycle to linearly many polynomial subproblems using polyhedral uncertainty subsets. Section 5, PDF pp.22–23, uses semidefinite/SOS relaxations; a polynomial number of subproblems is not a polynomial-time solution guarantee for those subproblems. No contradictory bounded-block-rank complexity theorem was found. These statements concern the inspected arXiv version.

### Recent robust network design

[Adjustable robust nonlinear network design without controllable elements under load scenario uncertainties](https://link.springer.com/article/10.1007/s10107-025-02207-2), DOI 10.1007/s10107-025-02207-2, gives a robust-feasibility characterization through polynomially many nonlinear worst-case problems and an exact adversarial design algorithm. Its discussion of the worst-case potential-difference problem distinguishes trees from the general NP-hard case. This supplies an established application for an improved worst-case oracle; it does not itself give the candidate's structural oracle complexity. An oracle result should not be described as making the full mixed-integer design problem polynomial-time solvable.

### Current field overview

[Pfetsch, Schmidt, Skutella, and Thürauf, *Potential-Based Flows—An Overview*](https://optimization-online.org/wp-content/uploads/2026/01/ch_potential.pdf), inspected 2026 preprint, PDF pp.9–10, defines MPD, records general quadratic NP-hardness and tree/single-cycle tractability, and explicitly identifies nonlinear MPD complexity on cactus graphs as open. PDF pp.14–16 connect robust feasibility to worst-case potential differences and mention resistance uncertainty. This supports the relevance of the proposed graph parameter, but is contextual synthesis rather than the primary proof source for the cited earlier results. Its open-problem statement does not remove the distinction between additive approximation and exact threshold decision.

## What should be claimed and credited

The result under review should be framed as an algorithm for an established uncertainty model. Within the repository, its new step is the combination of the nomination-face reduction with the fixed-core/polyhedral-leaf method. The mathematical difficulty is that bounding cycle rank alone does not bound the number of free uncertain nominations or resistances. The nomination reduction proposes to leave only a bounded number of nomination coordinates; the fixed-core theorem then handles the remaining scalar resistance variables without making them nonlinear-core coordinates.

Three aspects are material to a precise contribution statement:

1. The topology parameter is the maximum rank of a block, rather than the total cycle rank. Total graph cycle rank can grow with the number of blocks.
2. The promised running time is polynomial in binary input size and requested precision bits for each fixed rank bound. A statement that only counts nonlinear subproblems is weaker. The exponent may depend on the rank; do not silently strengthen this to fixed-parameter tractability.
3. Output is a certified additive value interval and rational uncertain data satisfying their original bounds and balance exactly. Their induced physical state may be algebraic. Neither exact threshold comparison nor rational physical flows are part of the claim.

Suggested provisional wording:

> For passive quadratic potential networks, we give a certified additive algorithm for worst-case potential difference under balanced interval nomination uncertainty and independent positive interval resistance uncertainty. For each fixed bound on the cycle rank of every biconnected block, the algorithm runs in polynomial time in the input bit length and requested precision bits. The uncertainty model and worst-case formulation are established; the proposed contribution is the structural complexity guarantee and its nomination-face/fixed-core reduction. We found no equivalent guarantee in the open primary literature inspected.

Use that wording only after the separate proof review accepts every stated guarantee.

## Search scope and residual uncertainty

The audit used the two requested papers as anchors, the open Aßmann thesis for the joint formulation, recent robust-design work, and a 2026 field overview to check nearby developments. Targeted web searches combined `gas`, `potential-based`, `uncertain friction`, `uncertain resistances`, `maximum potential difference`, `cycle rank`, `biconnected`, and `polynomial`. No matching structural theorem appeared. Search snippets were used for discovery; the comparisons above rest on inspected primary full text or an explicitly identified publisher abstract. PDF page numbers above are one-based positions in the linked documents, not repository literature-package locators.

Remaining checks before a publication-level novelty assertion include a fuller forward-citation search from the two Aßmann papers, direct inspection of the final Networks article if an open copy becomes available, and comparison with general fixed-nonlinear-dimension/parametric-LP algorithms. The latter is especially relevant to the repository's fixed-core theorem and is not settled by this gas-network audit.
