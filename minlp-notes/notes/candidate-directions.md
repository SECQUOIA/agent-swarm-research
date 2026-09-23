# Candidate research directions (brainstorm output, 2026-09-04)

Ranked lists produced by two brainstorming agents (convexification; algorithms/duality/complexity)
after calibration against the literature base and web checks. Kept for future selection.
Status annotations are maintained by this project.

**Current update:** this is a historical brainstorm. The positive-multilinear conjecture
now has an independently reviewed counterexample; CIA has counterexamples and a sharp
one-switch replacement; FBBT hardness and common-factor hull results are documented.
See `README.md` and `notes/log.md` for current results. Point-packing conjectures were
already resolved in Khajavirad (2024); graph-density order has classical Schur-multiplier
precedents. Older “not started” labels below describe the original session.

## Convexification / relaxation strength

1. **Degeneracy-dependent McCormick/hull gap bound.** For bilinear b on [0,1]^n with interaction graph G, mcgap ≤ 4√2·√d(G)·chgap (d = degeneracy), tight up to constants (Hadamard signs on K_{d+1}); constant ratio for planar/series-parallel graphs. Route: Boland et al. Cor. 1 (cut characterization) + polarization + Khintchine + degeneracy orientation. Status: in progress.
2. **Luedtke–Namazifar–Linderoth Conjecture 1** (positive-coefficient multilinear, term-by-term vs hull ratio uniformly bounded). Grid points {0,½,1}^n give ratio ≤ 2 easily; the question is off-grid. Plan: numerical search for large ratios (3-uniform hypergraphs, n ≤ 12), then proof or counterexample. Status: numerical exploration planned.
3. **Common-factor products with product bounds**: is conv{(x,y,w): w_j = x y_j, product bounds} the intersection of the Anstreicher–Burer–Park single-term hulls (after bound tightening)? Status: not started.
4. **Multi-attribute mixer with variable inlet compositions** (K ≥ 2 attributes, per-stream capacities): hull unknown. Status: not started.
5. **Quantitative strength of P-split relaxations vs P.** Status: not started.
6. **Product of simplices × polytope (Gupte's S̃)**: disaggregated extended hull of size Π m_l; original-space facets; extension-complexity lower bound. Status: not started.
7. **Single-pool pooling hull LP for fixed number of inputs** (Boland cells + Gupte RLT exactness + Cayley embedding). Status: not started.
8. **Exact recursive-McCormick vs hull ratio for trilinear terms on [ℓ,u]^3 as a function of u/ℓ.** Status: not started.
9. **Multilinear/hypergraph version of item 1.** Status: depends on 2.
10. **Exactness of pipe-hull relaxations of potential-based flow on meshed networks.** Status: not started (risky).
11. **Closed-form projected hulls for partial simplex × box product patterns and on/off bilinear with persistent compositions.** Status: not started.
12. **Series-parallel sharp constant (= 2) for item 1.** Status: fold into 1.

Rejected as known: bilinear term with product bounds (Anstreicher–Burer–Park 2021); single quadratic over a polytope (Santana–Dey 2020); pooling single-pool/output/attribute hull (Luedtke et al. 2020); simplex × polytope RLT exactness (Gupte et al. 2017); Boolean quadric/RLT+SDP exactness facts; MICP non-representability corollaries; Singh–Kekatos gas exactness on non-overlapping cycles; NP-hardness of optimal P-split partition (Tsay et al. 2021).

## Algorithms, duality, decomposition, complexity, optimal control

1. **Stagewise Shapley–Folkman bound for Lagrangian-cut SDDP / nested Benders with continuous aggregated states**: gap ≤ T(m+1)ρ̄ independent of the number of units; lower-bound family. Related: Dentcheva–Römisch 2004 (geographic decomposition gaps). Status: not started.
2. **Complexity of the greatest fixed point of FBBT with bilinear nodes** (NP-hard or polynomial?); geometric convergence rate. Status: not started.
3. **Information complexity of MI-convex optimization with bounded treewidth factor graphs.** Status: not started.
4. **Sager–Zeile Conjecture 1** (CIA with TV bound, n_ω > 2): computational settlement by MILP enumeration for small N, then proof. Status: planned.
5. **Perspective relaxation of on/off units with m coupling balances**: additive gap ≤ sum of m+1 largest nonconvexities; polynomial additive approximation for fixed m; tight family. Largely Aubin–Ekeland/Udell–Boyd specialization. Status: low priority.
6. **OA is information-optimal for convex MINLP** (matches Basu et al. lower bound); ECP/ESH may not be. Status: not started.
7. **Complexity of CIA with a total-variation budget**: XP algorithm for fixed n_ω; NP-hardness for n_ω in the input? Connection to Tijdeman's chairman assignment problem. Status: not started.
8. **Pooling with one quality and pool degree ≤ 2**: complexity classification. Status: not started.
9. **Finite termination of spatial B&B with nonlinear equalities** (Kirst–Füllner + Miranda test). Status: not started (check Füllner's thesis first).
10. **Growth of exact penalty parameters in regularized SDDP for MS-MINLP.** Status: low priority.
11. **Generalized surrogate duality gap vs number of aggregations.** Status: low priority.
12. **LP/NLP-B&B with inexact NLP subproblems.** Status: low priority.
13. **Geometric convergence rate of iterated OBBT.** Status: low priority.

Rejected as known: exponential OA iteration example (Hijazi–Bonami–Ouorou 2014); tight SUR/CIA bounds (Sager–Bock–Diehl; Kirches–Lenders–Manns; Zeile–Robuschi–Sager; Sager–Zeile n_ω = 2); FBBT linear fixed point via LP (Belotti et al.); SDDiP/SDDP complexity (Zhang–Sun; Lan); Dentcheva–Römisch gap ordering; one-pool bounded-input pooling (Boland et al.); potential-flow hardness results.

## Scaling disjunctions / integer multiplicity (own idea, novelty-checked)

The convex-case statement "aggregated perspective relaxation of n identical units is the hull; integrality of n is free" is Theorem 3 of Wu, Li, Lu, Deng, Fang, arXiv:2602.04123 (Feb 2026). Knueven–Ostrowski–Watson (2018) have the TU/integer-decomposition mechanism for aggregated identical generators; Shapley–Folkman consequences are classical (Starr; Aubin–Ekeland; Bertsekas et al. 1983; Henderson 2024 thesis). Still apparently unstated: the two-endpoint hull theorem for arbitrary scale sets Λ (discrete standard sizes) with shared intensive variables (bilinear n·T structure), the count-only cost separation, and the joint hull for several unit types over an integral count polytope. Deprioritized as incremental; see `notes/log.md`.
