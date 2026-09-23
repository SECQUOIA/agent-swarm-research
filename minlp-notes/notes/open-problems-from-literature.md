# Open problems and conjectures mined from the literature base (2026-09-04)

Compiled by an agent sweep over all `fulltext.md`/`paper.md` files (139 fulltexts) for explicit
"open", "conjecture", "unknown", "future work" statements, then read in context. Page locators
refer to `p.N` markers in the corresponding `fulltext.md`. "Flag" = may have been resolved after
publication (unverified). Status column is maintained by this project.

| # | Source (slug) | Open question (condensed) | Feasibility | Status |
|---|---|---|---|---|
| 1 | dey2020-convexifications-of-rank-one-based p.9 | Conjecture: linear optimization over U^row ∩ U^col (rank-one, row and column sum bounds) is NP-hard | medium | **Resolved (strongly NP-hard): `results/rank-one-row-column-hardness.md`** |
| 2 | anstreicher2009-semidefinite-programming-versus-the-reformulation p.12–15 | Conjectures 4–5: exact RLT / SDP / RLT+SYM / +ORD bound values for the point-packing QCQP (RLT = 2, SDP = 1 + 1/(n−1), RLT+SYM = 1/2 for n ≥ 5, …) | medium | **Already resolved in Khajavirad (2024), arXiv:2404.03091; local formulas are a rediscovery, see `notes/audit-packing.md`** |
| 3 | wang2021-on-the-tightness-of-sdp p.30 | Sharpness of the thresholds k ≥ m+2 (hull), k ≥ m+1 (hull ∩ H), k ≥ m (value) for SDP exactness of QCQPs | medium | **Already resolved in Wang–Kılınç-Karzan (2024), arXiv:2403.04752, §4.1/Remark 5: full hull exactness holds at k ≥ m. Original Proposition 2 shows this common threshold is sharp. See `notes/qcqp-multiplicity-threshold-resolution.md`.** |
| 4 | vecchietti2003-modeling-of-discrete-continuous-optimization p.8–9 | Characterize when big-M relaxation = hull relaxation for disjunctions with intersecting disjuncts | easy–medium | open |
| 5 | kronqvist2026-p-split-formulations-a-class p.33 | Behaviour of P-split hierarchy under weak (interval-arithmetic) bounds; strict monotonicity; adaptive partition | easy–medium | open |
| 6 | sager2020-on-mixed-integer-optimal-control p.24–27 | Conjecture 1: exact worst-case CIA value with total-variation bound σ_max and n_ω > 2 controls equals the continuous lower bound + Δ̄/2 | medium | **Counterexamples, sharp continuous one-switch formula, and exact continuous two-switch formula for all n>=4 independently reviewed; see `results/cia-uniform-switching-obstruction.md` and `results/cia-exact-two-switch-worst-case.md`. No prior resolution found in targeted later-literature search; general switch budgets remain open here.** |
| 7 | geoffrion1972-generalized-benders-decomposition p.21 | Property (P) conjecture: first half implies second half without compactness of X | easy–medium | **Precise P-prime common-optimizer implication refuted without compactness, independently reviewed: `results/geoffrion-property-p-conjecture.md`. The informal computational Property P conjecture is NOT refuted.** |
| 8 | fullner2021-convergent-upper-bounds-in-global p.32–33; kirst2025 | Miranda-type feasibility test on parallelepipeds; inequality constraints; mixed-integer extension of RHS-restriction termination | easy–medium | open |
| 9 | gupte2017-relaxations-and-discretizations-for-the p.6 | Is checking triviality (z* = 0) of a pooling instance polynomial? | medium | **Affirmative for the stated upper-capacity acyclic generalized model: `results/pooling-triviality-polynomial.md`, independently reviewed. Explicit consequence of known destination-disaggregation machinery; no claim that the decomposition itself is new.** |
| 10 | basu2025-information-complexity-of-mixed-integer p.9 | Conjectures 1–3: transfer of constrained lower bounds to mixed-integer; binary-oracle complexity | medium–hard | open |
| 11 | bienstock2019-strong-np-hardness-of-ac p.6 | ε-approximate AC power flow feasibility is in NP | medium | open |
| 12 | bayraksan2024-bounds-for-multistage-mixed-integer | Monotonicity conditions for scenario-group bounds in multistage MI-DRO | medium | open |
| 13 | luedtke2012-some-results-on-the-strength p.22 | Conjecture 1: positive-coefficient multilinear, term-by-term vs hull gap ratio bounded by a universal constant (numerically ≤ 1.21 in dim 6) | medium–hard | **Resolved with sharp asymptotic replacement: worst ratio is asymptotic to ln d / ln ln d by degree, and ln n / ln ln n by dimension. Sparse unit-coefficient lower family and universal harmonic upper coupling independently reviewed. See `results/positive-multilinear-gap.md`; novelty search qualified.** |
| 14 | boland2017-bounding-the-gap-between-the | Exact growth constant of the McCormick/hull gap ratio (between √n/4 and 600√n); structural bounds | medium | **Strengthened to c* ≤ 4√ρ(G); graph-by-graph order already follows from Schur-multiplier theory. `results/mccormick-gap-degeneracy-bound.md`; sharp constant open.** |
| 15 | pia2024 / pia2021 (Del Pia–Khajavirad) | Characterize hypergraphs with MP_G = MP_G^{ERI} | hard | open |
| 16 | schutte2023-relaxation-strength-for-multilinear-optimization p.8 | Intersected recursive McCormick vs running-intersection strengthening | medium | open |
| 17 | belotti2025-convex-envelopes-of-bounded-monomials p.15, p.20 | Lower envelope for n > 2; n = 2 with negative exponents; hull of {x1^a1 x2^a2 ∈ [ℓ,u]} over a box | easy–medium | **Lower envelope for n > 2 on a wedge resolved by Yang–Zhang (IJOCTA 2026, local `zhang2026-flat-lower-envelopes-solve-bounded`): it is flat. Negative/mixed exponents and the box hull remain open (screen 2026-09-22, `notes/screen-monomial-envelopes.md`).** |
| 18 | khademnia2025-convexification-of-bilinear-terms-over | Original-space facet description for sparsely observed network-polytope × simplex products, m > 1 | medium–hard | **Scope corrected after reading source: a polynomial disaggregated extended hull is already standard; the original-space combinatorial description is the research direction. Investigation ongoing.** |
| 19 | hijazi2017-convex-quadratic-relaxations-for-mixed p.15 | Compact hull of on/off constraints with non-monotone functions | medium | open (flag) |
| 20 | gomez2021-strong-formulations-for-conic-quadratic p.25 | Hull of conic quadratic sets with indicators and bounded continuous variables | medium–hard | open (flag) |
| 21 | lodi2023-disjunctive-cuts-in-mixed-integer p.40; andersen2013 | Efficient conic cut separation; monoidal strengthening for conic; split closure structure | medium–hard | open |
| 22 | kuchlbauer2022; coey2020 p.8; lubin2018 p.20 | OA finite convergence beyond convexity / without conic well-posedness; guidance to avoid polyhedral-approximation failures | medium | open |
| 23 | eronen2017-method-for-solving-generalized-convex p.9 | No algorithm guaranteed to find a feasible point under f°-quasiconvex nonsmooth constraints | medium | open |
| 24 | boland2017-a-polynomially-solvable-case-of p.8; haugland2016-the-computational-complexity-of-the p.16; dey2015 p.111 | Pooling: one quality with in/out-degree ≤ 2; fixed pools with bounded inputs, outputs, or qualities; approximation better than n | medium | **Degree case resolved strongly NP-hard with all four degrees exactly two, unit capacities and constant costs; profit has no PTAS. Two reviews: `results/pooling-all-degrees-two.md`. Fixed-pool bounded-input and bounded-quality cases have reviewed polynomial bit algorithms: `results/fixed-core-block-polyhedral-optimization.md` (arbitrary bypasses excluded in the latter). Fixed-output case is NP-complete already with two pools and two outputs: `results/pooling-two-pools-two-outputs-hardness.md`, two reviews. Other approximation questions remain separate.** |
| 25 | gupte2017 p.19–23 | Inequality description of conv(S̃) (product of simplices × polytope) and Lagrangian hulls | medium–hard | open |
| 26 | azuma2023 p.21; kocuk2016 p.35 | Verifiable exactness conditions for SOCP/SDP relaxations beyond bipartite sparsity | medium–hard | open |
| 27 | zhang2022; fullner2022 p.25; fullner2025 | A priori regularization parameters σ_t; efficient Lagrangian duals in SDDiP/NC-NBD; deterministic stopping | medium–hard | open |
| 28 | nie2013-an-exact-jacobian-sdp-relaxation p.22; lasserre2001 p.21 | Singular minimizers; a priori relaxation order | hard | open |
| 29 | bomze2025-mixed-integer-bilevel-optimization-with p.16 | Separation of lower-level KKT points from the true reaction set | medium–hard | open |
| 30 | bonami2008 p.14; grossmann2002 p.9 | A priori criterion OA vs NLP-B&B | medium | open |
| 31 | he2024-mip-relaxations-in-factorable-programming; strahl2025 p.22 | Logarithmic ideal MIP relaxations for high-dimensional composites; PSD-cone d.c. underestimators | medium | open |
| 32 | modaresi2016 p.32; burer2017 p.31 | Non-concentric ellipsoid removal; multiple SOC/quadratics | medium–hard | open (flag) |
| 33 | lubin2022-mixed-integer-convex-representability p.33 | Sufficiency of the midpoint lemma; rationality; diameter assumption | hard | open (partly addressed in zadik2024) |
| 34 | koppe2012-on-the-complexity-of-nonlinear p.8, p.14 | Fixed integer dimension + varying continuous part; indefinite quadratics over integer points | hard | open (flag: planar case later solved) |
| 35 | furini2018-qplib p.20 | NP membership of quadratic feasibility over the reals | very hard | open |
| 36 | ogbe2019 p.4, p.10; ahmed2004 p.4 | Finite exact termination of decomposition with continuous first-stage variables | hard | open |
| 37 | gro2017-algorithmic-results-for-potential-based p.20 | Potential-based flows with switches: multiple sources/sinks; series–parallel; active networks | medium–hard | open (flag) |
| 38 | sager2009 p.14; sager2012 p.5, p.20 | Bang-bang results with control-dependent path constraints; Veliov's conjecture without differentiability | hard | open (flag) |
| 39 | r2012-a-strong-dual-for-conic | Subadditive dual function classes for conic MIP | hard | open |
| 40 | burer2009-on-the-copositive-representation-of | Copositive representation of more general quadratic constraints | hard | open |
| 41 | kronqvist2026-50-years-of-mixed-integer p.9 | No general tractable representation of conv(F ∩ X ∩ R^n × Z^l) for nonconvex MINLP (meta-limit) | — | framing |

| 42 | Haugland–Hendrix (2016), §4.5, journal p.607 / local PDF p.17 | With bypasses and only one mixing pool, is pooling polynomial when the number of qualities is fixed? | medium | **Negative: strong NP-completeness with one upper quality, exactly two pool feeds and two outlets, zero lower flows, bounded degrees and fixed physical-data alphabets. Two full audits: `results/pooling-constant-data-two-feed-np-completeness.md`. The later broad hardness assertion by Baltean-Lugojan–Misener (2018), Remark 4.6, is credited; the explicit reduction and combined restrictions are the candidate contribution.** |

Resolved within the corpus (do not pursue): mixed-sign bilinear McCormick ratio unbounded
(boland2017); one pool with bounded inputs polynomial (boland2017-a-poly); sparse SOS convergence
(lasserre2006); Ahmed's SDDP linear-in-T conjecture, qualified (zhang2022); no uniform generic
degree bound for Lasserre (nie2013-optimality); MICP-R of unions without common recession cone
(lubin2022).
