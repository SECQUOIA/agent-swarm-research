# Scout report: (A) MIP / piecewise-linear relaxations of MINLP, (B) symmetry handling with continuous variables

Date: 2026-09-22. Sources: local knowledge base, in-house `results/`, web search, and arXiv PDFs fetched to `/tmp/scout/`. Quotes were checked against PDF text I extracted myself; a web-summarizer "quote" attributed to the unified framework paper was fabricated and is not used. A failed search does not prove that a problem is open.

---

## Part A. MIP relaxations and piecewise-linear (PWL) relaxations

### A1. Sawtooth, separable, and NMDT relaxations for quadratic terms

**State of the art.**
- Beach, Hildebrand, Huchette, "Compact mixed-integer programming formulations in quadratic optimization", JOGO 84(4):869–912 (2022), arXiv 2011.08823. This paper introduced the Yarotsky sawtooth formulation for `y=x^2`. Error is `2^{-2L-2}` with O(L) binaries, rows, and auxiliary variables. The reflected Gray-code version is sharp and **hereditarily sharp**. The sawtooth *epigraph* relaxation (lower side) needs no binaries. KB: `beach2022-compact-...`.
- Beach, Burlacu, Bärmann, Hager, Hildebrand, "Enhancements of discretization approaches for non-convex MIQCQP", Part I: COAP 87:835–891 (2024), arXiv 2211.00876. It covers sawtooth, tightened sawtooth (TSR), Bin2/Bin3, and HybS. HybS needs `nL` binaries, against about `(n²+n)L/2` for Bin2/Bin3. HybS has a tighter LP relaxation than Bin2/Bin3, but its MIP relaxation is not always tighter. Part II: arXiv 2302.01164 introduces D-NMDT (doubly discretized NMDT), which reaches the same error as NMDT with fewer binaries and has a better LP relaxation.
- Bärmann, Burlacu, Hager, Kleinert, JOGO 85(4):789–819 (2022). For small ε, univariate reformulations of `xy` use fewer simplices than bivariate triangulations. Lemma 8 gives a simplex lower bound of `⌈area/(2√5 ε)⌉` for bivariate triangulations. The projection of every sharp bivariate formulation is exactly McCormick.
- NMDT/MDT: Teles, Castro, Matos (2013); Castro (2015, tightened piecewise McCormick); Castro, I&EC Res. 62(28):11053–11066 (2023, base-2 NMDT with OBBT in spatial B&B).
- Göß, Burlacu, Martin, JOGO (2026), arXiv 2407.06143: MIP-computed paraboloid estimators for Lipschitz functions.

**Stated open problems and future work.**
- Beach et al. 2022 (§7, App. C), on higher-order monomials: "a comparable approximation for x³ seem[s] to require a relatively large number of basis functions … interesting future work to observe if this seeming obstruction is fundamental, or if compact methods for higher-order monomials can be derived". They also leave "an implementation that iteratively refines the approximation to guarantee a pre-specified approximation error" as future work.
- Part II conclusion: "Two of the most promising directions … are employing adaptivity and adding MIQCQP-specific cuts that are valid but not recognized by the MIP solvers. This is the subject of future work."

**Already addressed in-house.**
- `results/mip-relaxation-binary-lower-bounds.md`: every MIP relaxation of `x²` with `p` binaries has error at least `2^{-2p-2}`, so sawtooth is exactly optimal. For `xy`, `p_min(ε)=log2(1/ε)+O(1)`, with the additive constant known only up to an interval of length 2.
- `bilinear-graph-binary-complexity.md`: graph-LP bounds for simultaneous bilinear terms.
- `quadratic-rank-integer-complexity.md`: integer dimension is half the Hessian rank.
- Pure powers, positive polynomials, and smooth maps: `positive-pure-power-linear-dimension-precision.md`, `rational-power-compiled-integer-precision.md`, `positive-polynomial-loglog-degree-precision.md`, `polynomial-graph-binary-integer-degree-gap.md`, `smooth-map-local-rank-integer-complexity.md`, and related files.

These in-house results largely settle the **binary-count** part of Beach et al.'s x³ question. For positive powers, O(log 1/ε) integers suffice, within an additive constant of optimal. They do **not** settle whether a formulation can be both count-optimal and sharp or hereditarily sharp for x³ or `xy`.

**Where theory is missing.**
1. **Count and LP strength together.** Is there a formulation of `xy` on `[0,1]²` with `log2(1/ε)+O(1)` binaries that is sharp, meaning its LP projection is McCormick? The same question applies to hereditary sharpness, and to x³ with the convex-hull LP. The in-house lower bounds ignore LP strength. Part I shows that LP and MIP tightness can disagree (HybS vs Bin2). Confidence open: **medium-high**. I found no theorem on the minimum binaries for a sharp ε-relaxation of `xy`.
2. **Exact constant for `xy`.** The in-house gap of 2 on the additive constant is open in-house.
3. **Constraint and auxiliary-variable counts** for a fixed binary budget. The in-house bounds let rows be unlimited.

### A2. Logarithmic and ideal formulations of PWL functions and combinatorial disjunctive constraints (CDCs)

**State of the art.**
- Vielma and Nemhauser, Math. Prog. 128:49–72 (2011): logarithmic formulations.
- Vielma, SIAM Review survey (2015).
- Huchette and Vielma, "Nonconvex piecewise linear functions: advanced formulations and simple modeling tools", OR 71(5):1835–1856 (2023), arXiv 1708.00050. Zig-zag ZZI/ZZB formulations are ideal and logarithmic and branch in a more balanced way. For bivariate grids, independent-branching depth is `⌈log d1⌉+⌈log d2⌉+6`. Implemented in PiecewiseLinearOpt.jl.
- Lyu, Hicks, Huchette, Math. Prog. 204:385–413 (2023), arXiv 2205.06916: junction-tree CDCs and an ideal SOS_k formulation. **Minimum biclique cover remains hard.**
- Lyu, Hicks, Huchette, OR 74(1):484–499 (2026), arXiv 2304.14542: shared SOS2 encodings for PWL lower and upper bounds, plus generalized nD-ordered CDCs.
- Related 2025 work: Dobrovoczki and Kis, arXiv 2503.10405 (triangulation heuristics and compact MILPs). Ploussard, Li, Pavičević, arXiv 2508.09395 (tightening DC-based continuous PWL MILPs).

**Stated open problems.**
- Vielma and Nemhauser 2011, concluding section: necessary conditions for logarithmic formulations are open. This is recorded in the in-house note `mip-relaxation-binary-lower-bounds.md`.
- Lyu et al. 2026, §8: "Could we design computationally more efficient formulations for generalized 1D-ordered CDCs? What are the computational performances of different approaches for piecewise linear relaxations with more than one variable? Could we design an efficient procedure to find a piecewise linear relaxation of a given multivariate nonlinear function such that it can be modeled by generalized nD-ordered CDCs?"

**Where theory is missing.** There is no theory relating branching balance (Huchette and Vielma's metrics) to B&B tree size. There are also no lower bounds on the constraint count of ideal logarithmic formulations for general CDCs.

### A3. Optimal triangulations

**State of the art.** Pottmann et al. (2000) found optimal interpolating triangulations and conjectured they are optimal among all approximations. Atariah, Rote, Wintraecken (2018) refuted that conjecture. Bärmann, Burlacu, Hager, Kutzer, JOTA 199(2):569–599 (2023), give a constant-factor "crossing swords" triangulation for `xy`. **Burlacu, Hager, Hildebrand, arXiv 2604.04026 (Apr 2026)** give the global optimum for discontinuous ε-approximations of `xy` on the plane: density `3√3/(32ε)`. They also give one-sided density `3√3/(16ε)` and prove optimality among parallelogram tilings for continuous approximations: density `√3/(8ε)`, with constant deviation `ε/3`.

**Stated open problems (verbatim, §7).** "Several directions remain open for future work. First, proving or disproving Conjecture 6.1— that the parallelogram tiling optimum extends to all continuous triangulations… Second, extending these results to higher dimensions— optimal simplicial approximations in R^n… Third, the bounded domain case, where boundary effects may permit lower densities." Bärmann et al. 2022 add: "Finding a bivariate ε-optimal triangulation for the approximation of F over a rectangular domain is still an open problem."

### A4. Adaptive partitioning (Alpine / AMP) and piecewise polyhedral relaxations (PPR)

**State of the art.**
- Nagarajan, Lu, Yamangil, Bent (CP 2016), arXiv 1606.05806. Nagarajan, Lu, Wang, Bent, Sundar, JOGO 74(4):639–675 (2019), arXiv 1707.02514 (AMP in Alpine.jl). The method refines partitions sparsely around the incumbent and runs OBBT. Convergence is proved only asymptotically, through exhaustive refinement. At iteration k there are at most `3+2(k−1)` partitions per variable.
- Sundar, Nagarajan, Linderoth, Wang, Bent, ORL 49:144–149 (2021), arXiv 2001.00514: an SOS2-based PPR for one multilinear term. It is locally sharp, but the recursive R-PPR depends on how terms are grouped.
- **Kim, Richard, Tawarmalani, SIOPT 34(4):3167–3193 (2024).** Linking constraints across overlapping multilinear terms on regular partitions give about 10× speedups in Alpine. The paper also gives the first locally ideal polynomial-size formulation for non-regular (decision-tree) partitions. Regular partitions can have exponentially more cells than non-regular ones. The linking system is not the full convex hull in general.
- He and Tawarmalani, SIOPT 34(3):2856–2882 (2024), arXiv 2310.07168: ideal MIP relaxations of discretized composites. They close about 60–70% of the McCormick gap.
- Kannan, Nagarajan, Deka, IJOC (2025), arXiv 2301.00306, "strong partitioning": a max–min problem that chooses partition points. An ML approximation gives 2–4.5× speedups in Alpine.

**Adaptive refinement with convergence guarantees.** Burlacu, Geißler, Schewe, OMS 35(1):37–64 (2020), classify refinement rules that guarantee convergence. They also show that earlier schemes may fail to terminate. Schmidt, Sirvent, Wollner, Math. Prog. (2019), and Optim. Lett. 16:1355–1372 (2022), treat Lipschitz nonlinearities and prove a **worst-case iteration bound** in the oracle setting.

**Stated open problems.**
- Kannan et al. §7 raise optimal allocation of partition points under a budget, which leads to a max–min problem with binary outer variables that "necessitates new techniques".

**Where theory is missing.** I found **no convergence-rate or iteration-complexity theory for AMP/Alpine-style adaptive partitioning of explicit polynomial terms**. Existing results give asymptotic convergence only, apart from the Lipschitz-oracle bounds, which are exponential in dimension. Open questions:
- How many AMP iterations, or how many total binaries, are needed for ε-optimality, compared with uniform or dyadic partitioning?
- Is adaptivity ever provably better than a uniform logarithmic (sawtooth/NMDT) discretization?
- What is the complexity of the strong-partitioning max–min problem?

The in-house spatial-B&B lower bounds do not cover AMP.

### A5. Solvers
- **Gurobi 11–13**: general nonlinear constraints. Gurobi documentation says function constraints were approximated by static PWL before Gurobi 11, and that since Gurobi 12 the default is spatial B&B with dynamically refined outer approximations. Static PWL (`FuncNonlinear=0`, `FuncPieces`/`FuncPieceError`) remains an option. Source: Gurobi 13 manual (KB `optimization2026-nonlinear-constraints-gurobi-optimizer-13`).
- **Alpine.jl** (AMP/PPR) and **PiecewiseLinearOpt.jl** (logarithmic and zig-zag formulations).
- **SCIP and BARON** use spatial B&B, not MIP-relaxation-based schemes.
- Ploussard et al., arXiv 2608.27312 (2026): Square/Triangle/DC PWL MILPs can beat QP solvers on long-horizon sequentially coupled bilinear programs.

---

## Part B. Symmetry handling in MINLP with continuous variables

### B1. Detection

**State of the art.**
- Liberti, "Reformulations in mathematical programming: automatic symmetry detection and exploitation", Math. Prog. 131:273–304 (2012): formulation groups found through expression-DAG automorphisms, plus static symmetry-breaking constraints. Applied to MINLPLib/GlobalLib with Couenne.
- Kouyialis, Wang, Misener, arXiv 1712.05222 (Processes 2019): binary layered graphs for QCQP symmetry detection.
- **SCIP 8** (arXiv 2112.08872) added detection of permutation symmetries through expression graphs, plus "complementary" symmetries for quadratic problems (attributed to Wegscheider's work).
- **SCIP 9 and Hojny, MPC (2025), arXiv 2405.08379**: symmetry detection graphs (SDGs) for signed permutations and reflections, with gadgets for sums, `(x_i−x_j)²`, bilinear terms, and even functions. The paper states that detecting general MINLP symmetries is undecidable, and that detection is NP-hard even for binary LPs.
- Wiese (MOSEK), "Symmetry detection in mixed-integer conic programming", MPC (2025/26).

**Stated open problems (Hojny 2025, §7.4, verbatim).** "It might be promising to develop alternative approaches for detecting row and column symmetries that depend less on the structure of generators. Ideally, one would use an exact mechanism … but detecting such symmetries is as hard as the graph isomorphism problem." Also, "it could be interesting to investigate means to benefit from handling symmetries in branch-and-bound, while removing the symmetry-based restrictions in heuristics." Reflection symmetries appear in only 6/486 MINLPLib instances.

### B2. Handling with binary variables: polyhedral and propagation methods

**State of the art.**
- Orbitopes and orbitopal fixing (Kaibel, Peinhardt, Pfetsch).
- Hojny and Pfetsch, "Polytopes associated with symmetry handling", Math. Prog. (2019): symretopes, symresacks, and almost-linear-time separation of symresack cover inequalities.
- Hojny, "Packing, partitioning, and covering symresacks", DAM (2020).
- Bendotti, Fouilhoux, Rottner, Math. Prog. (2021): orbitopal fixing for full (sub-)orbitopes, with an application to unit commitment.
- Schreier–Sims (SST) cuts: Liberti and Ostrowski, "Stabilizer-based symmetry breaking constraints for mathematical programs", JOGO 60:183–194 (2014), and Salvagnin (2018).
- **van Doornmalen and Hojny, IJOC 36(3):868–883 (2024), arXiv 2203.00992**: complete propagation for cyclic groups, under the assumption that generators are monotone and ordered.

**Stated open problems (verbatim).**
- van Doornmalen and Hojny 2024, intro: "It has been an open problem for at least ten years to gain further insights into the structure of lexicographically maximal points for cyclic groups." Conclusion: "since completeness of Algorithm 3 is only guaranteed for monotone and ordered permutations γ, it would be helpful to derive methods that achieve completeness even if one of the assumptions on γ are dropped."
- Deciding lexicographic maximality in an orbit is coNP-complete for generator-given groups.

### B3. General (continuous) variables: unified framework, fundamental domains, rotations

**State of the art.**
- **van Doornmalen and Hojny, "A unified framework for symmetry handling", Math. Prog. 212:217–271 (2025), arXiv 2211.01295.** Symmetry-handling constraints (SHCs) with node-dependent lexicographic orders unify orbital fixing, LexFix, orbitopal fixing, and isomorphism pruning. The paper generalizes them to arbitrary domains as *lexicographic reduction*, *orbitopal reduction*, and *orbital reduction*. These methods are implemented in SCIP 9/10.
  - Theorem 8 guarantees exactly one representative per orbit in finite B&B trees whose branchings partition the feasible region.
  - Remark 14, verbatim: "For spatial branch-and-bound algorithms, two subtleties arise … there might not exist a finite branch-and-bound tree … branching decisions do not necessarily partition the feasible region. In this case, (2) can still be used to handle symmetries. However, in the depth-pruned tree there might exist more than one leaf containing a symmetric copy of a feasible solution."
  - Remark 15: the theorem survives for some infinite groups, such as rotations.
  - §6 future work: "As the framework also supports other types of symmetries such as rotational and reflection symmetries, further research could involve devising symmetry handling methods for such symmetries," plus separation routines for SHCs, packing/partitioning structure, and "overlapping orbitopal subgroups within a component."
- **Verschae, Villagra, von Niederhäusern, "On the geometry of symmetry breaking inequalities", Math. Prog. (2023), IPCO 2021, arXiv 2011.09641.** A *fundamental domain* is a minimal closed symmetry-breaking polyhedron for a finite orthogonal group acting on Rⁿ. The paper introduces generalized Dirichlet domains (GDDs).
  - Every permutation group has a fundamental domain with at most n−1 facets.
  - The closure of the lexicographically-maximal set equals the SST cuts.
  - SST cuts can over-represent a binary orbit by `2^{Ω(n)}` points, while a GDD with O(n) facets can give unique binary representatives.
  - Only reflection groups admit fundamental domains with a unique representative for every orbit in Rⁿ.
  - §6, verbatim: "**Q1:** Does our GDD construction exhaust all possible fundamental domains for a group of isometries …? **Q2:** Does every group of isometries admit a fundamental domain with a single representative of each binary orbit, and with a polynomial number of facets?" The authors also propose variants based on extension complexity or separation complexity, and characterizing the groups with O(1) representatives per orbit in Rⁿ.
- **Hojny and Liberti, "A computational comparison of handling distance constraints in MINLP", arXiv 2605.02305 (2026).** On rotations: "for rotation symmetries arising in applications like the kissing number problem or packing spheres into a bigger sphere, only simple techniques have been developed". They prove the simple fixings `X_{i,j}=0 (j>i)`, `X_{1,j}≥0` are "the strongest possible ones for the class of Givens rotations".
- **SCIP 10** (arXiv 2511.18580) extends SST cuts and orbitopes to reflections and adds a heuristic for double-lex block matrices (disk packing).
- **Other solvers.** Berthold, Kamp, Mexi, Pokutta, Pólik (FICO), arXiv 2605.04850 (2026), footnote: symmetry handling "has not been added to nonlinear solvers" because such symmetry is rarer and harder to detect. SCIP is the documented exception. I found no documentation of symmetry handling for nonlinear constraints in Gurobi or BARON; this is uncertain.

### B4. Symmetry, relaxation strength, and reformulation in continuous nonconvex problems

- Costa, Hansen, Liberti, DAM 161(1):96–106 (2013): symmetry-breaking constraints in spatial B&B for circle packing.
- **Khajavirad, ORL 57:107197 (2024), arXiv 2404.03091**: compares LP, RLT, and SDP relaxations with symmetry-breaking constraints for circle packing. It proves Anstreicher's conjectures, which also appear in-house in `point-packing-relaxations-anstreicher-conjecture-4.md` as known results.
- **Qu, Lu, Wu, Li, Deng, Fang, JOTA 209:71 (2026)**: exact variable-aggregation reformulations of separable (MI)QPs with symmetric variable groups. In the convex case the optimum has equal components. In the concave case all but one component sit at a bound. In the indefinite case the reformulation keeps first and second aggregate moments. Gurobi gains more from aggregation than from symmetry-breaking inequalities.
- **Timofte (2003) and Riener, arXiv 1001.4464 (JPAA 2012)**: the (half-)degree principle. Timofte's form: a symmetric degree-d polynomial is nonnegative on Rⁿ if and only if it is nonnegative on points with at most `max(⌊d/2⌋,2)` distinct coordinates. Riener derives this from a more general statement about symmetric optimization problems. Moustrou, Riener, and coauthors extend this to reflection groups. As far as I found, this is **not used in any MINLP solver**.
- Faenza et al., arXiv 2511.07766 (IPCO 2026): under (k+1)-transitive symmetry, level k of Sherali–Adams, Lovász–Schrijver, and lift-and-project are equally strong; whether the same holds for SoS is left open.
- **In-house link.** The spatial-B&B exponential lower bounds (`spatial-bb-*-exponential-lower-bound.md`) explicitly exclude symmetry handling: "Symmetry-breaking constraints, general branching disjunctions, and stronger moment hierarchies require separate analysis." `separable-vertex-binarization.md` records that SCIP solves the *symmetric* family `P_30` in 11 nodes through symmetry handling, and times out when `misc/usesymmetry = 0`. No theorem explains this.

---

## Candidate open theoretical questions (ranked)

1. **Continuous optimal triangulation of `xy` (Burlacu–Hager–Hildebrand Conjecture 6.1)**, plus bounded-domain and n≥3 versions. The conjecture is explicit and recent (Apr 2026), so it is very likely unsolved. Candidate optimum: `√3/(8ε)`.
2. **Fundamental domains with unique binary representatives and polynomially many facets (Verschae et al. Q2)**, and whether GDDs exhaust all fundamental domains (Q1). The questions are explicit (2021/2023), and I found no follow-up.
3. **Size and strength trade-off for MIP relaxations of `xy` and x^k.** What is the minimum number of binaries for a *sharp* or *hereditarily sharp* ε-relaxation, compared with the in-house count-only optimum? Also, what is the exact additive constant for `xy`? Not stated verbatim in the literature; no theorem found; extends in-house results.
4. **Iteration and binary complexity of adaptive partitioning (AMP/Alpine, Burlacu-type refinement).** Rates, lower bounds, and a comparison with uniform logarithmic discretization. There is no theory beyond asymptotic convergence and exponential Lipschitz-oracle bounds.
5. **Spatial B&B with symmetry handling for continuous variables.**
   - (a) Node-count theory: can lexicographic or orbitopal reduction make spatial B&B polynomial on S_n-symmetric nonconvex separable families (the in-house `P_n`)? What happens under group-preserving perturbations?
   - (b) Symmetry handling for rotation × permutation groups (point configurations) that are compatible with spatial branching (unified framework Remark 14 and §6; Hojny–Liberti 2026).
   - (c) Automatic use of the degree principle or orbit-space aggregation (Riener; Qu et al.) for non-separable invariant QCQPs.
6. Structure of lexicographically maximal binary points under cyclic groups. Described as open "for at least ten years".
7. Necessary conditions and constraint-count lower bounds for logarithmic ideal formulations (Vielma–Nemhauser 2011; Lyu et al.).
