# Candidate research directions (brainstorm, 2026-09-05)

Output of a brainstorming agent asked for directions outside the existing
clusters (integer-precision laws, pooling dichotomies, potential flows,
spatial B&B lower bounds, bilevel, multilinear gaps, CIA, rank-one hulls,
FBBT). Scores are the agent's: impact I, feasibility F, novelty confidence N.
Every "not aware of" is a memory-based judgment and needs a literature pass
before investment. Kept for future selection; status annotations are
maintained by this project.

| Rank | Direction | I | F | N |
|---|---|---|---|---|
| 1 | Complexity and parameterization of the Grossmann flexibility index for linear models: NP-hardness of the flexibility test (RHS uncertainty, `{0,±1}` recourse), polynomial for fixed `n_θ` (classical) or fixed `n_z` (LP value function with `O(m^{n_z})` pieces), ETH lower bound `2^{o(n_θ)}`; approximability open. Known: Zhang–Grossmann–Lima 2016 identify the test with adjustable robust feasibility; Ben-Tal et al. 2004 NP-hardness of ARC. | 7 | 8 | 6 |
| 2 | Two-way exponential separation between NLP-B&B and linearization methods (OA/ECP/ESH/LP-NLP-B&B) on convex MIQCPs: family A where NLP-B&B needs `O(n)` nodes but any linearization master needs `2^{Ω(n)}` rounds (ball shifted so one integer point is feasible, objective favouring `Θ(2^n/√n)` outside points; spherical-cap counting), family B the reverse. Answers open problem #30 (a priori OA vs B&B criterion) negatively. Known: Hijazi–Bonami–Ouorou 2014 ball example is not a separation. | 7 | 7 | 6 |
| 3 | Proximity theorem for mixed-integer separable convex programs with subdeterminants `≤ Δ`: `‖x*−x̄‖_∞ ≤ nΔ` in the integer part. Known: Cook et al. 1986 (MILP), Hochbaum–Shanthikumar 1990 (pure integer separable convex), Paat–Weismantel–Weltge 2020 (mixed linear). Risk: the exchange step with real multipliers. | 6 | 7 | 5 |
| 4 | LP-bound invariance for continuous-time (event-based) STN/RTN scheduling MILPs: LP value independent of the number of event points; discrete-time bound strictly increases with `T`. | 6 | 6 | 5 |
| 5 | Integrality gap of Mišić's split-based tree-ensemble MILP as a function of the number of trees and depth; APX-hardness for depth-2 ensembles (MAX-CUT). Risk: may reduce to Boolean quadric polytope facts. | 6 | 6 | 5 |
| 6 | NP-hardness of membership in the convex hull of a ReLU layer `conv{(x, ReLU(Wx+b)) : x ∈ box}` when the number of neurons grows; polynomial separability for fixed `k`. Known: Anderson et al. 2020 single-neuron ideal formulation. | 7 | 5 | 5 |
| 7 | HEN minimum-number-of-matches approximability. Updated by the 2026-09-05 status check: single interval is APX-hard with a `6/5+ε` approximation (Chen–Li–Liang, arXiv:2504.18037; TAMC 2026) and W[1]-hard in the number of hot streams (Fertin et al., TCS 2024, as maximum zero-sum partition); the multi-interval constant-factor question and the exact single-interval threshold in `[c, 6/5]` are open; the HENS, fixed-charge-transportation, and zero-sum-partition literatures are mutually unaware. | 6 | 5 | 6 |
| 8 | Hausdorff convergence order of big-M versus hull relaxations of convex on/off sets under bound tightening (order 1 versus infinite), with a cluster-type node blow-up consequence. | 5 | 6 | 4 |
| 9 | GDP basic steps: NP-hardness of choosing a bound-improving basic step; Shapley–Folkman-type bound on the improvement in terms of coupling rank. Check Papageorgiou 2025 first. | 5 | 5 | 5 |
| 10 | Basu–Jiang–Kerger–Molinaro Conjectures 1 and 3 (constrained transfer; upper-bound transfer). Updated: Basu–Kerger–Molinaro arXiv:2511.02082 give `Ω(2^n d^2 log(R/ρ))` for feasibility under bit and inner-product oracles (partial Conjecture 2); Conjectures 1 and 3 untouched. High risk. | 8 | 3 | 7 |
| 11 | Lagrangian-cut tightness for general-integer states in SDDiP: closure equals the convex envelope over the lattice; `Ω(U)` gap for `n = 1`; exactness under integrally convex structure. | 6 | 4 | 5 |
| 12 | Closure of intersection cuts from maximal quadratic-free sets for `w = xy` on a box (equals McCormick?) and for the `2×2` minor set (weaker than SOC?). | 5 | 4 | 5 |

Direction actually taken on 2026-09-05: existential-theory-of-the-reals
completeness of the pooling problem (not in the list above; the root's own
idea), recorded in `results/pooling-existential-theory-of-reals.md` and
`results/pooling-one-pool-bypass-existential-reals.md`.
