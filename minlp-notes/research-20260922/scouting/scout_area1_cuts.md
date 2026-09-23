# Scout report, Area 1: convexification and cutting planes for nonconvex quadratic and polynomial MINLP

Date: 2026-09-22. Scope: 2021-2026 work, with older anchors where needed.
Sources: the local KB (`/home/sgusev/repo/minlp-notes/literature/papers/<slug>/paper.md`, cited as `[KB:slug]`) plus web and arXiv (cited by arXiv id or DOI). Quotes come from full texts: the KB `fulltext.md` or the arXiv PDFs saved under `/tmp/scout1/*.txt`. "Not found" means I searched for the item and did not find it. It does not mean the item is proven absent.

---

## 1. Intersection cuts and maximal quadratic-free sets

**State of the art**
- Muñoz & Serrano, "Maximal quadratic-free sets", IPCO 2020 and Math. Prog. 2022 (doi 10.1007/s10107-021-01738-8, arXiv 1911.12341). This was the first construction of maximal S-free sets for S = {x : q(x) <= 0} with q a general quadratic. The construction runs through a homogenization to the set {||x|| <= ||y||}.
- Chmiela, Muñoz & Serrano, "On the implementation and strengthening of intersection cuts for QCQPs", IPCO 2021 (LNCS 12707) and Math. Prog. 197:549-586 (2023) (doi 10.1007/s10107-022-01808-5). They give closed-form cut formulas, add Glover-style strengthening, and implement both in SCIP.
- Chmiela, Muñoz & Serrano, "Monoidal strengthening and unique lifting in MIQCPs", IPCO 2023 and Math. Prog. B 210:189-222 (2025) (doi 10.1007/s10107-024-02112-0). They show unique lifting, so monoidal strengthening gives the best possible coefficients for the integer variables.
- Muñoz, Paat & Serrano: "Towards a characterization of maximal quadratic-free sets" (IPCO 2023), then "A characterization of maximal homogeneous-quadratic-free sets" (Math. Prog. 2024, doi 10.1007/s10107-024-02092-1, arXiv 2211.05185), then "A characterization of maximal inhomogeneous-quadratic-free sets" (arXiv 2605.30602, May 2026). Together these give a **complete characterization** of full-dimensional maximal quadratic-free sets through non-expansive maps Γ. The 2026 paper: "our work completes a characterization of all maximal quadratic-free sets."
- Related constructions:
  - Bienstock, Chen & Muñoz, outer-product-free sets and oracle-based cuts, Math. Prog. 183 (2020) [KB:bienstock2020-outer-product-free-sets-for].
  - Serrano, intersection cuts for factorable MINLP via concave underestimators, IPCO 2019, arXiv 1812.03073.
  - Modaresi, Kılınç & Vielma, intersection cuts for nonlinear integer programming [KB:modaresi2016-intersection-cuts-for-nonlinear-integer].
  - Xu & Liberti, submodular maximization through an intersection-cut lens, Math. Prog. 2024 (arXiv 2302.14020).
  - Xu & Pokutta, "Joint-range inequalities for nonconvex QCQPs", arXiv 2608.03318 [KB:xu2026-joint-range-inequalities-for-nonconvex]. They project two valid inequalities onto a 2-D joint range, convexify there, and lift back. The result is sparse cuts and a four-ray intersection cut.

**Solvers**
- SCIP 8 has quadratic intersection cuts in `nlhdlr_quadratic`, but they are **off by default**. SCIP 8's reason: "Since intersection cuts can be rather dense, it is not clear yet how to decide when it will be beneficial to generate such cuts. Their separation is therefore currently disabled by default" [KB:bestuzheva2025-global-optimization-of-mixed-integer].
- SCIP 9 (arXiv 2402.17702) added monoidal strengthening and cut sparsification. Intersection cuts are still "currently disabled by default". SCIP 9 notes that "the strengthened intersection cuts significantly outperform the pure intersection cuts whenever monoidal strengthening can be applied."
- I found no evidence that Gurobi, BARON or Xpress implement quadratic-free intersection cuts.

**Stated open problems**
- Muñoz & Serrano (1911.12341): "The empirical performance of these intersection cuts remains to be seen". They also list "a theoretical and empirical comparison with the method proposed by Bienstock et al." and "devising new methods for producing other families of quadratic-free sets". Their 3-D conjecture was later settled by the Muñoz-Paat-Serrano full paper.
- Muñoz, Paat & Serrano (2211.05185, §8): "finding a characterization of when a set of points in D^m can be used to define a maximal Q-free polyhedron is an important follow-up question". The polyhedral case and the choice of Γ remain open.
- Serrano (1812.03073): "It remains to be seen the practical performance of these intersection cuts … the strengthening procedures … might be too expensive to be of practical use."
- Xu & Pokutta (2608.03318): "A primary direction for future research is to automate … selecting two effective base inequalities." Their mixed cuts exclude the punctured Δ=0 cases.

**Missing theory**
- The characterization tells us which S-free sets are maximal. It says nothing about which maximal set yields the strongest or deepest cut for a given LP vertex and cone. With a whole family of Γ available, choosing Γ is an optimization problem that nobody has studied.
- I found no closure result, meaning no statement on whether the intersection-cut closure over all quadratic-free sets, or over the monoidally strengthened cuts, is polyhedral.
- I found no rank or convergence result for iterated quadratic intersection cuts. The only finite-convergence scheme I found is the oracle-based one of Bienstock, Chen & Muñoz, which uses a different set family.
- Every construction handles **one** quadratic at a time. Maximal S-free sets for intersections of two or more quadratics are open, apart from the 2-D projected case of Xu & Pokutta.
- I found no dimension-free density or sparsity guarantee, although density is the stated reason the cuts are disabled in SCIP.

## 2. Convex hulls of one or a few quadratics: aggregation, rank-one sets, hidden convexity

**State of the art**
- Santana & Dey, SIOPT 30(4) (2020), arXiv 1812.10160 [KB:santana2020-the-convex-hull-of-a]. The convex hull of one quadratic equality intersected with a bounded polytope is SOC-representable, with no sign or rank assumptions. The construction can be exponential in size.
- Modaresi & Vielma, Math. Prog. 164 (2017) [KB:modaresi2017-convex-hull-of-two-quadratic]: two quadratics, or one conic quadratic and one quadratic.
- Burer & Kılınç-Karzan, Math. Prog. 162 (2017) [KB:burer2017-how-to-convexify-the-intersection]: SOC cone intersected with one nonconvex quadratic.
- Dey, Muñoz & Serrano, SIOPT 32(2) (2022), arXiv 2106.12629 [KB:dey2022-on-obtaining-the-convex-hull]. Under PDLC, aggregations give the hull of three quadratics, but possibly through infinitely many aggregations.
- Blekherman, Dey & Sun, SIOPT 34(1) (2024), arXiv 2210.01722 [KB:blekherman2024-aggregations-of-quadratic-inequalities-and]: hidden hyperplane convexity (HHC) is sufficient for any number of quadratics.
- Blekherman & Dunbar, arXiv 2405.18282 (2024). Under PDLC, no points at infinity and nonempty interior, **at most 4** good aggregations suffice for three quadratics. This is a partial answer to the finiteness question.
- Exactness of the SDP relaxation in the convex-hull sense:
  - Wang & Kılınç-Karzan, Math. Prog. 193 (2022) [KB:wang2021-on-the-tightness-of-sdp].
  - Kılınç-Karzan & Wang, arXiv 2107.06885.
  - Wang & Kılınç-Karzan, ORL 2024 (arXiv 2403.04752).
  - Kojima, Kim & Arima, arXiv 2504.03204 and 2604.02968 (separable QCQPs).
- Rank-one based sets:
  - Dey, Kocuk & Santana, JOGO 77 (2020) [KB:dey2020-convexifications-of-rank-one-based].
  - Anstreicher, Burer & Park, bounded products, JOGO 80 (2021) [KB:anstreicher2021-convex-hull-representations-for-bounded].
  - Choi, Cepeda, Gómez & Han, rank-one convexification with step penalties, arXiv 2504.16330.
- Hidden convexity with bilinear terms: Gorissen, den Hertog & Reusken, OR 2026 [KB:gorissen2026-hidden-convexity-in-a-class]. Topological view: Chandrasekaran, Duff, Rodriguez & Shu, arXiv 2510.06112.

**Stated open problems**
- Dey, Muñoz & Serrano: "An important open question is to determine if we actually require an infinite number of aggregations to obtain the convex hull". They also ask how to relax the "no low-dimensional components" condition and the PDLC condition.
- Blekherman, Dey & Sun, Conjecture 3.1: "even with hidden hyperplane convexity there exist sets S … where infinitely many good aggregations are needed". Conjecture 3.2 claims that examples needing more than four good aggregations exist. Conjecture 3.3 states that "aggregations always provide certificates when conv(S)=R^n." Blekherman & Dunbar 2024 prove r <= 4 under extra assumptions and "leave open the case of more defining inequalities or a nonempty variety". So Conjecture 3.2 remains open for the strict or general setting.
- Dey, Kocuk & Santana: "We conjecture that optimizing a linear function on U^row ∩ U^col is NP-hard." I found no resolution.
- Kılınç-Karzan & Wang (2107.06885): "We additionally conjecture that V(G^⊥) = V(G^4) even without the facially exposed assumption." Wang & Kılınç-Karzan 2022: "establishing exactness conditions for strengthened SDP relaxations of QCQPs [e.g., SDP+RLT] is clearly of great interest."
- Burer & Kılınç-Karzan 2017: "The theoretical and practical strength of this technique is of interest for future research."
- Resolved example: Burer's conjecture that the lifted ball-QCQP relaxation dominates Kronecker RLT was proved by Kılınç-Karzan & Sun [KB:sun2025-on-the-strength-of-burers].

**Missing theory**
- Santana-Dey is an existence result. I found no separation-complexity result for conv{x ∈ P : quadratic} with P given by inequalities, and no compact (polynomial-size) version except in special cases.
- I found no bound on the number of aggregations as a function of n and m.

## 3. RLT, SDP/eigenvector cuts and sparse cuts

**State of the art**
- RLT separation in solvers: Bestuzheva, Gleixner & Achterberg, Math. Prog. 210 (2025), arXiv 2211.13545 [KB:bestuzheva2025-efficient-separation-of-rlt-cuts]. They detect implicit products, apply row marking, and report results in both SCIP and Gurobi.
- Sparse eigenvector cuts: Dey, Kazachkov, Lodi & Muñoz, "Cutting plane generation through sparse principal component analysis", SIOPT 32(2) (2022) [KB:dey2022-cutting-plane-generation-through-sparse]. Separating a k-sparse eigen-cut is NP-hard (it is sparse PCA). Hybrid sparse+dense cuts work best in practice.
- Quality of k-PSD closures:
  - Blekherman, Dey, Molinaro & Sun, "Sparse PSD approximation of the PSD cone", Math. Prog. 2022 (arXiv 2002.02988).
  - Bhardwaj, Kothari & Narayanan, arXiv 2105.11920.
  - Bhardwaj, Narayanan & Pathapati, arXiv 2405.01208.
- **Eigen-CG cuts**: Dey, Jiang, Kazachkov, Lodi & Muñoz, arXiv 2604.00932 (Apr 2026). They apply CG rounding to eigenvector inequalities and transfer the result to continuous variables through Burer-Letchford.
  - The conic closure of two of their subfamilies equals the Boros-Hammer (BH) closure.
  - They prove that dense Eigen-CG cuts are ineffective on top of SDP+McCormick.
  - BH / Eigen-CG capture only 3,676 of the 116,764 facets of BQP_6.
- Outer-product-free and oracle cuts: [KB:bienstock2020-outer-product-free-sets-for].
- Recent strengthening schemes for nonconvex QP:
  - Qu et al., DNN cutting planes, arXiv 2510.02948.
  - Lambert & Porumbel, convex quadratic cuts that converge to Shor+RLT, JOGO 2025/26 (doi 10.1007/s10898-025-01513-5).
  - Strahl, Raghunathan, Sahinidis & Gounaris, tight quadratic relaxations II (d.c.), arXiv 2408.13058.
  - González-Rodríguez et al., RLT branch-and-bound with SOCP/SDP constraints, JOTA 2025 [KB:rodriguez2025-polynomial-optimization-tightening-rlt-based].
- Exact and inexact RLT: Qiu & Yıldırım, JOGO 2024 and Math. Prog. 2025 [KB:qiu2024-on-exact-and-inexact-rlt; KB:qiu2025-polyhedral-properties-of-rlt-relaxations].
- Bipartite bilinear programs:
  - Dey, Santana & Wang, SOCP relaxation for bipartite bilinear programs, Optim. Eng. 2019 [KB:dey2019-new-socp-relaxation-and-branching].
  - Gu, Dey & Richard, lifting convex inequalities (arXiv 2106.12625) and lifted bilinear cover cuts (arXiv 2208.00345).

**Stated open problems**
- Eigen-CG, **Conjecture 1**: "For any (v0, v), the inequality defined by E-CG(v0, v) is implied by a nonnegative combination of BH inequalities. To date, every computational test we have devised suggests that this conjecture is true, but we have not been able to find a proof."
- Blekherman et al. (2002.02988): "Improving these bounds as a function of this ratio [k/n] is an important open question."
- Gu, Dey & Richard (2208.00345): "We conjecture that the separation problem is NP-hard although proving this result appears nontrivial." They also leave open whether the cuts help inside QCQP relaxations.
- Qu et al. (2510.02948): "it is not known whether the above GMC method converges in a finite number of iterations for indefinite QP … A rigorous convergence analysis is left for future work."
- Tawarmalani (2026) [KB:tawarmalani2026-new-finite-relaxation-hierarchies-for]: RLT "is not known to terminate with the convex hull in finite steps" for disjoint bilinear programs, in contrast with the new disjunctive-decomposition hierarchy.

**Missing theory**
- I found no approximation guarantee for sparse eigen-cut closures relative to the full SDP bound with McCormick/RLT included. Blekherman et al. bound only the distance from the PSD cone alone.
- I found no complexity result for separating Boros-Hammer inequalities in the continuous BoxQP setting beyond the known results for the BQP polytope.

## 4. Boolean quadric polytope and BoxQP

**State of the art**
- Burer & Letchford, SIOPT 20(2):1073-1089 (2009). The projection of QP_n = conv{(x, xx^T): x ∈ [0,1]^n} onto (x, off-diagonal X) is the Boolean quadric polytope (BQP) (Padberg 1989 [KB:padberg1989-the-boolean-quadric-polytope-some]). So every BQP inequality is valid for BoxQP.
- Bonami, Günlük & Linderoth, MPC 10:333-382 (2018) (doi 10.1007/s12532-018-0133-x). BQP cuts plus integrality-based preprocessing in spatial branch-and-cut make an LP-based solver competitive with SDP solvers on small and sparse BoxQP.
- Anstreicher & Burer 2010 [KB:anstreicher2010-computable-representations-for-convex-hulls]: PSD+RLT is exact for QP_n only when n=2.
- Recent structure-based exact formulations:
  - Dey & Khajavirad, "A second-order cone representable class of nonconvex QPs", arXiv 2508.18435 / Math. Prog. 2026 (doi 10.1007/s10107-026-02364-y) [KB:dey2025-a-second-order-cone-representable].
  - Khajavirad, "Tight SDP relaxations for sparse box-constrained QPs", arXiv 2601.18545 (2026). An RLT-SDP relaxation that exploits sparsity, with an exact extended formulation under tree-decomposition conditions.
- Submodular BoxQP:
  - Burer, Natarajan & Willemsen, arXiv 2504.03996 [KB:burer2025-on-the-semidefinite-representability-of]: an SDP with RLT is exact for n <= 3 and has a counterexample at n=4.
  - Zhang & Wang, arXiv 2609.03617 (Sep 2026): for n >= 4, **no finite family of instance-independent linear cuts** closes the SDP gap. With BQP-valid cuts the gap is Ω(n); with m arbitrary cuts it is Ω(n/m²).
- Other: Xia, Vera & Zuluaga, INFORMS JoC (arXiv 1511.02423); Fix-and-Bound for BoxQP, MPC 2024 (arXiv 2211.08911).

**Stated open problems**
- Dey & Khajavirad (2508.18435) and Khajavirad (2601.18545): "to date, obtaining an explicit algebraic description for QP_3 remains an open question."
- Khajavirad (2601.18545): "For a complete graph with three nodes and three plus loops, we leave it as an open question whether our proposed SDP relaxation gives an extended formulation for QP(G)." "We leave it as an open question whether a similar result can be obtained for |V+| > 2." "The authors of [18] leave open the question of whether a tree decomposition … satisfying conditions (I)-(III) can be constructed in polynomial time."
- Dey & Khajavirad: "we pose an open question whether the stable set assumption on the nodes with plus loops is necessary for SOC-representability of QP(G)." They also leave open "the complexity of checking conditions (C1)-(C3)".
- Burer, Natarajan & Willemsen: "The complexity of minimizing a submodular quadratic over [0,1]^n for n >= 4 remains open." Zhang & Wang (2609.03617): "how to systematically design non-BQP-valid cuts to reduce the relaxation gap remains an interesting topic for future research". In one construction they write "the problem still remains open".
- Gupte et al. [KB:gupte2020-extended-formulations-for-convex-hulls]: "We conjecture that this observation extends to any wheel W_{n-1} with n >= 6, n even". Halin graphs are posed as an open question.
- Xia, Vera & Zuluaga (1511.02423): "obtaining general and effectively computable bounds of this type is an interesting open question."

## 5. Multilinear polytope (Del Pia, Khajavirad and others)

**State of the art**
- Acyclicity ladder:
  - Berge-acyclic: the standard linearization is exact.
  - γ-acyclic: flower inequalities.
  - Kite-free β-acyclic: running-intersection inequalities (MOR 2021) [KB:pia2021-the-running-intersection-relaxation-of].
  - β-acyclic: polynomial-size extended formulation (Math. Prog. 2024) [KB:pia2024-a-polynomial-size-extended-formulation].
  - α-acyclic: the complete edge relaxation (CER) is exact **iff** G is α-acyclic, with size 2^r|E_max| (Math. Prog. 2026, arXiv 2507.12831) [KB:pia2026-the-complete-edge-relaxation-for].
- Overview with a characterization of the acyclic hypergraphs that admit a polynomial-time-constructible polynomial-size extended formulation: Del Pia & Khajavirad, arXiv 2501.04805 (2025).
- Pseudo-Boolean polytope and limits of tractability [KB:pia2024-the-pseudo-boolean-polytope-and; KB:pia2025-beyond-hypergraph-acyclicity-limits-of].
- Knowledge compilation: Capelli, Del Pia & Di Gregorio [KB:capelli2026-a-knowledge-compilation-take-on].
- Simple odd β-cycle inequalities with strongly polynomial separation: Del Pia & Walter [KB:pia2023-simple-odd-cycle-inequalities-for].
- Recursive McCormick versus flower:
  - Khajavirad, ORL 2023 [KB:khajavirad2023-on-the-strength-of-recursive].
  - Schutte & Walter [KB:schutte2023-relaxation-strength-for-multilinear-optimization].
  - Raghunathan et al., arXiv 2207.08955.
- Decision-diagram cut generation: Cooper & Castro, arXiv 2607.28511 [KB:cooper2026-beyond-hand-derived-inequalities-decision]. Davarnia's graphical framework: arXiv 2409.19794.
- Continuous multilinear relaxations: piecewise polyhedral relaxations [KB:kim2024-piecewise-polyhedral-relaxations-of-multilinear]; symmetric multilinear polynomials [KB:xu2021-polyhedral-analysis-of-symmetric-multilinear].

**Solvers**
- BARON: running-intersection cuts gave about a 50% average time reduction on random multilinear/polynomial instances (Del Pia, Khajavirad & Sahinidis, MPC 12:165-191, 2020).
- SCIP 10 (arXiv 2511.18580) [KB:hojny2025-the-scip-optimization-suite-10] added `sepa_flower`, which separates k-flower inequalities for k=1,2 over AND constraints and products. Extending it to products of continuous variables caused "a performance loss, which is why this is disabled by default."

**Stated open problems**
- Characterize the hypergraphs with MP = MP^RI (2021) and with MP = MP^ERI (2024). The 2024 paper's Example 5 shows the extended running-intersection (ERI) inequalities are not enough for all β-acyclic hypergraphs.
- 2501.04805: "obtaining an explicit description for the multilinear polytope of β-acyclic hypergraphs in the original space remains an open question" (the authors doubt it would matter in practice).
- CER (2507.12831): "how to generalize inequalities (40) for α-cycles of any length … The next step is to understand the complexity of separation over these inequalities … and characterize the class of hypergraphs for which the new relaxation coincides with the multilinear polytope."
- Beyond acyclicity (2410.23045): "the complexity of checking whether the nest-set gap of a hypergraph is bounded is an open question". The complexity of constructing an elimination ordering with nsw_N(G) <= k is also open. The paper states two extension-complexity statements "we do not know if they are true or false".
- Pseudo-Boolean polytope (2309.08693): "a complete characterization of such signed hypergraphs remains an open question."
- Del Pia & Walter, Conjecture 12: redundancy of non-simple odd closed walks.
- Schutte & Walter: "We leave it as an open problem to investigate how this strengthening of intersected recursive linearizations compares to … running intersection inequalities."
- Cooper & Castro: "it remains open whether β-acyclic hypergraph classes admit polynomial-size compact DDs."
- Rank-one Boolean tensor factorization (2202.07053): "obtaining recovery guarantees for the complete LP is an interesting open question."

## 6. Bilinear, trilinear and edge-concave/vertex-polyhedral envelopes

**State of the art**
- Classical:
  - Rikun 1997 [KB:rikun1997-a-convex-envelope-formula-for].
  - Sherali 1997 [KB:sherali1997-convex-envelopes-of-multilinear-functions].
  - Meyer & Floudas, trilinear facets and edge-concave envelopes (Math. Prog. 2005).
  - Tardella, vertex-polyhedral envelopes.
  - Tawarmalani, Richard & Xiong, envelopes via polyhedral subdivisions, Math. Prog. 138 (2013) [KB:tawarmalani2013-convex-envelopes-of-products-of].
  - Bao et al., multiterm polyhedral relaxations [KB:bao2009-multiterm-polyhedral-relaxations-for-nonconvex].
- Edge-concave cuts: Misener & Floudas (GloMIQO / GloMIQO 2, JOGO 2012-2013). Available in SCIP since 3.2, but "not shown to be particularly useful for general MINLP, this separator is disabled for now" [KB:bestuzheva2025-global-optimization-of-mixed-integer].
- Recent results:
  - Belotti, envelopes of bounded monomials on two-variable cones, Math. Prog. 211 (2025) [KB:belotti2025-convex-envelopes-of-bounded-monomials].
  - Makhoul & Speakman, volume of the trilinear hull over general boxes, IJOO 2026 (arXiv 2512.13964) [KB:makhoul2026-volume-formulae-for-the-convex].
  - Khademnia & Davarnia, bilinear terms over network polytopes, MOR 2024 (arXiv 2302.14151).
  - Davarnia & Rahimian, arXiv 2510.15861.
  - Dey, Han & Wang, aggregation of bipartite bilinear equalities, JOGO 94 (2026) [KB:dey2026-aggregation-of-bilinear-bipartite-equality].
  - Locatelli, envelopes of quadratics on the simplex [KB:locatelli2015-convex-envelopes-of-some-quadratic].
  - Karmarkar & Lucet, envelope of bivariate piecewise linear-quadratic functions in linear time, arXiv 2609.19343.
  - He & Tawarmalani, MIP relaxations of composite functions, SIOPT 2024 [KB:he2024-mip-relaxations-in-factorable-programming].

**Stated open problems**
- Belotti: "The lower envelope for W_ij is an open problem for n > 2."
- Makhoul & Speakman: closed-form volumes for the alternative McCormick relaxations P1-P3 over general boxes "remain an open question". They also ask whether the tightness ranking known for nonnegative bounds persists when bounds have mixed signs.
- Dey, Han & Wang: "we might conjecture that the intersection of the convex hull of finitely many aggregated sets may represent the convex hull for a more general case of n1 and n2."
- Xu, Adams & Gupte: "The convex envelope of a supermodular function is not known in general and is NP-hard to separate over." An explicit hull for symmetric multilinear polynomials in general is also missing.

**Missing theory**
- I found no guarantee that relates edge-concave decomposition choices to the resulting bound; the decomposition is chosen heuristically.
- I found no volume or strength ranking for vertex-polyhedral cuts beyond trilinear monomials.

## 7. Solver implementations (summary)

| Solver | Quadratic/polynomial convexification and cuts |
|---|---|
| SCIP 8 (JOGO 91, 2025; arXiv 2301.00587) | Expression DAG with nonlinear handlers (quadratic, bilinear, SOC, convex/concave, perspective, quotient). McCormick, RLT (implicit and explicit products), 2x2 SDP minor cuts. Intersection cuts and edge-concave cuts implemented but **off by default**. |
| SCIP 9 (arXiv 2402.17702) | Monoidal strengthening of intersection cuts (still off by default), signomial handler with DC cuts (off by default), sparsification. MINLP about 4% faster and 13% fewer nodes than SCIP 8. |
| SCIP 10 (arXiv 2511.18580) | `sepa_flower` (1- and 2-flower inequalities). Handling of continuous products is off by default. MINLP gains exceed MILP gains. |
| Gurobi 9.0 (2019-20) | Nonconvex quadratics become bilinear terms. McCormick with local bounds, spatial branching. **RLT cuts** and **BQP cuts** (only triangle inequalities at that point). The 9.0 slides state PSD cuts were "not yet implemented". |
| Gurobi 9.5+ | `PSDCuts` parameter; also `BQPCuts` and `RLTCuts` parameters. |
| Gurobi 11-13 | General MINLP through outer approximation and spatial B&B (11). Nonlinear expressions (12). NL barrier local solver and "over 2x faster" MINLP (13). Cut internals are not published. |
| BARON | Multiterm polyhedral relaxations, running-intersection cuts (MPC 2020), tight quadratic relaxations (Strahl et al. 2024). |

## 8. Computational evidence on which cuts help

- Gurobi 9.0 webinar ablation, 444 models (values read from a slide, so treat them as approximate): timeouts were 21 by default, 110 without RLT cuts, 20 without BQP cuts, 165 without RLT+BQP, and 187 with no cuts. **RLT cuts carry most of the gain; triangle-only BQP cuts add little.**
- Bestuzheva, Gleixner & Achterberg: explicit RLT cuts solved 4,434 → 4,557 instances, with time ratio 0.85 and node ratio 0.81 on MINLP. Row marking cut RLT separation time share from 16.7% to 2.6% (MINLP) and from 54.6% to 2.8% (MILP).
- Bonami, Günlük & Linderoth: BQP cuts are highly effective on BoxQP.
- Dey et al. 2022: sparse cuts are cheaper but weaker at n=200-250 (75% vs 85% gap closed); the hybrid is the best compromise.
- Eigen-CG 2026: density "quickly degrades effectiveness", while sparse cuts beyond triangles help.
- Intersection cuts: useful when monoidal strengthening applies (SCIP 9), but density prevents default use.
- Bienstock, Chen & Muñoz: oracle cuts complement SDP+OA; neither dominates.
- Running-intersection cuts: about 50% time cut in BARON on random polynomial instances. Simple odd β-cycle cuts: separation "often prohibitively expensive" [KB:pia2023-simple-odd-cycle-inequalities-for].
- Perspective cuts: convex ones give consistent gains; nonconvex ones help root bounds but can hurt hard instances [KB:bestuzheva2023-a-computational-study-of-perspective].
- Cross-cutting gap: I found **no published cross-solver ablation** that isolates each cut family (RLT, BQP, PSD, intersection, edge-concave, flower) on QPLIB or MINLPLib under a common protocol. Evidence is solver-internal and version-specific.

## 9. Where theory is missing (cross-cutting)

1. **Cut selection theory for nonlinear cut families.** Density-versus-depth tradeoffs are the stated reason cuts are disabled (SCIP 8/9), yet no guarantee exists. The Eigen-CG "dense cuts are ineffective" theorem is the first such result.
2. **Closures.** I found closure results only for Eigen-CG (via BH) and for flower/RMC relaxations. I found none for quadratic intersection cuts, monoidally strengthened cuts, sparse eigen-cuts with McCormick, or joint-range cuts.
3. **Separation complexity.** Most separation problems are open or only conjectured hard: BH in the continuous setting, lifted bilinear cover cuts (conjectured NP-hard), α-cycle inequalities, and SOC conditions (C1)-(C3). Sparse eigen-cut separation is known to be NP-hard.
4. **Multiple-constraint S-free sets.** Only single-quadratic and 2-D joint-range results exist.
5. **Finite-convergence and rank results** for iterative quadratic/DNN cutting schemes: open, per Qu et al. and Tawarmalani.

## 10. Ranked shortlist of open questions (for the summary)

1. Explicit description of QP_3 (BoxQP hull, n=3) and more generally SDP/SOC-representability boundaries for QP(G). Stated in 2508.18435 and 2601.18545.
2. Eigen-CG Conjecture 1 (Eigen-CG closure = Boros-Hammer closure) (2604.00932).
3. Complexity of submodular BoxQP for n >= 4, combined with the Ω(n) cut-gap result (Burer et al. 2504.03996; Zhang-Wang 2609.03617).
4. Finiteness of aggregations for three or more quadratics (Dey-Muñoz-Serrano; Blekherman-Dey-Sun Conjectures 3.1-3.3; partial answer by Blekherman-Dunbar 2405.18282).
5. Quadratic-free intersection cuts: characterizing maximal *polyhedral* Q-free sets, choosing Γ for the strongest cut, closure and density theory, and extension to several quadratics (Muñoz-Paat-Serrano 2211.05185 §8; SCIP 8/9 default-off rationale).
6. Multilinear polytope: exactness classes for RI/ERI relaxations, α-cycle inequalities and their separation complexity, and recognition of a bounded nest-set gap (Del Pia-Khajavirad 2021-2026).
