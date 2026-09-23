# Scout: global solution of nonconvex PSE problem classes (2026-09-12)

Status: literature and benchmark scout, no computation performed. Every
"not found" below is the result of a bounded web search and is not a proof of
novelty. Solver bound data quoted from MINLPLib are the library's recorded
runs (mixed solver versions and dates); the first task of any selected
candidate is to re-establish baselines with Gurobi 13, BARON 26, SCIP 10 and
ANTIGONE on the current machine.

## 1. Scope, method, and repository overlap

Goal: 5–8 candidate directions for global (or certifiably near-global)
solution of nonconvex MINLP classes from process and energy systems where the
current solvers demonstrably struggle and where a relaxation, decomposition,
reformulation, cut family or bound-tightening idea with a clear theoretical
justification can show an effect within days in Pyomo + Gurobi 13 + GAMS 54.

Method: web search of arXiv, Optimization Online, journal sites and MINLPLib
for each class; primary sources were opened where accessible (Mistry–Misener
2016 manuscript, Kim–Bagajewicz 2017, Tumbalam Gooty et al. 2020/2024,
Jalilian–Kocuk 2023, GALINI 2021, MINLPLib instance pages). Standard ideas
(piecewise McCormick / NMDT, generic OBBT, plain SDP relaxation, multivariate
partitioning, ML-guided partitioning) were discarded as required.

Repository overlap check (grep of `notes/`, `results/`, `papers/`, `code/`):

- Pooling: the repo's work is complexity theory (∃R-completeness, fixed-parameter
  algorithms, rank-one conic lower bounds; `papers/pooling/`). No practical
  relaxation or solver study exists. Directly reusable theory: the
  common-factor fixed-linking-row oracle
  (`results/common-factor-fixed-linking-optimization.md`, XP in the number of
  linking rows) and the reciprocal-anchor hulls
  (`results/common-factor-reciprocal-anchor-full-hull.md`).
- Network–simplex hulls (`paper-network-simplex/`): exact sparse hulls for
  flow × simplex products, with LP-level timings only; not tested inside any
  branch-and-bound on a real instance. Its own README says general simplex
  disaggregation and polynomial separation were already known.
- Potential flows (`paper-power-flow/`, `code/potential_flow_mpd/`): cactus
  theory, exact certificates; no design/topology solver.
- Energy storage: the 2026-09-12 scan
  (`notes/research-20260912-energy-opportunities.md`) already found the storage
  convexification direction covered by prior art (Bansal–Günlük, Morales 2025);
  storage sizing is therefore not re-proposed here.
- HENS, water networks, distillation, crude-oil scheduling: no repo work
  beyond the 2026-09-05 brainstorm entry on HENS minimum-number-of-matches
  approximability (`notes/candidate-directions-2026-09-05.md`, rank 7).

## 2. Solver landscape (September 2026)

- Gurobi 13.0 (November 2025): claims >2× faster on non-trivial MINLPs, new
  nonconvex NLP barrier for local solves; general nonlinear expression trees
  (pow, log, exp) handled by spatial B&B with dynamically refined outer
  approximations.
  [Release note](https://www.gurobi.com/news/gurobi-releases-version-13-0-with-improved-performance-and-new-solving-capabilities/),
  [changes](https://docs.gurobi.com/projects/optimizer/en/current/reference/releasenotes/changes.html).
- SCIP 10.0 (November 2025): stronger on nonlinear instances than 9.0; new
  NLP-solver interface including CONOPT.
  [arXiv:2511.18580](https://arxiv.org/abs/2511.18580).
- BARON: continuous 2025 updates in presolve, convexity detection, relaxation,
  separation and range reduction
  ([GAMS 2025 solver blog](https://www.gams.com/blog/2026/01/the-year-2025-for-gams-solvers/)).
- ANTIGONE: no substantive algorithmic update since 1.1; it is the weakest
  bounder on several MINLPLib water/HENS instances quoted below.
- Academic solvers with a clear pooling/PSE focus: GALINI (Pyomo-based,
  [arXiv:2105.01687](https://arxiv.org/abs/2105.01687)) and Alpine
  (multivariate partitioning; strong partitioning by Kannan–Nagarajan–Deka,
  [arXiv:2301.00306](https://arxiv.org/abs/2301.00306), IJOC 2025).

## 3. Class-by-class status: strongest recent results and what is open

Gaps below are (primal − best dual)/primal from the MINLPLib instance pages
unless stated otherwise.

| Class | Strongest recent global results | What remains open (concrete) |
|---|---|---|
| HENS, stage-wise SYNHEAT (isothermal mixing), LMTD/Chen | Mistry–Misener 2016: RecLMTD^β strictly convex (β>0); MILP-OA algorithm with nf4r piecewise McCormick, Gurobi 6 ([CACE 94:1–17](https://www.sciencedirect.com/science/article/pii/S0098135416302216), [manuscript PDF](https://spiral.imperial.ac.uk/bitstreams/73f1f43f-70a2-4142-84c7-54b3798583b5/download)). Kim–Bagajewicz 2017 bound contraction ([I&EC Res](https://pubs.acs.org/doi/10.1021/acs.iecr.6b04686), [PDF](https://www.ou.edu/class/che-design/pub-papers/Global%20Optimization%20of%20Stages-substages(kim%20and%20Bagajewicz)-17.pdf)): on a 10-stream and an 11+2-stream example, BARON 14.4 had 77% gap after 10 h and ANTIGONE 1.1 found no feasible point; their own method reached 1–6% gaps after 1–12 h. Bagajewicz's group now avoids MINLP altogether: enumeration + set trimming ("globally optimal", Oliva et al. 2024 [AIChE J](https://aiche.onlinelibrary.wiley.com/doi/10.1002/aic.18450); Chang et al. 2020 [AIChE J](https://aiche.onlinelibrary.wiley.com/doi/10.1002/aic.16267)). | MINLPLib `heatexch_gen1` (112 vars, 12 binaries): primal 154,896, best dual 107,976 (LINDO), BARON 100,552 → 30–35% gap, open since 2013 ([page](https://www.minlplib.org/heatexch_gen1.html)). `heatexch_gen2` (16 binaries): 1.3% (LINDO) / 8% (BARON) ([page](https://www.minlplib.org/heatexch_gen2.html)). `heatexch_gen3` (60 binaries): 13.6% for BARON, Gurobi and SCIP alike ([page](https://www.minlplib.org/heatexch_gen3.html)). No larger SYNHEAT instances (10SP1, 15SP, Escobar–Trierweiler set) are in any public library with certified bounds. |
| Standard pooling (many pools/qualities) | Luedtke–D'Ambrosio–Linderoth–Schweiger 2020 single-pool/single-output/single-attribute hull ([SIOPT 30:1582](https://epubs.siam.org/doi/10.1137/18M1174374), [arXiv](https://arxiv.org/abs/1803.02955)); Jalilian–Kocuk 2023 rank-one substructure (row/column-sum bounded nonnegative rank-one matrices), SOC-representable hull of exponential size, polyhedral OA + bound tightening, Gurobi 9.1.1 ([arXiv:2306.10810](https://arxiv.org/abs/2306.10810)); GALINI 2021: Luedtke cuts help sparse instances, hurt dense ones; Gurobi 9.1 gap degrades with size on Dey–Gupte dense instances ([arXiv:2105.01687](https://arxiv.org/abs/2105.01687)). Tawarmalani 2026 finite hierarchies for disjoint bilinear programs ([Math Prog](https://link.springer.com/article/10.1007/s10107-026-02326-4), [arXiv:2405.11068](https://arxiv.org/abs/2405.11068)) — theory only. | Alfaki–Haugland instances in MINLPLib: `pooling_sppc1pq` 12–16% gap (Gurobi/ANTIGONE dual) ([page](https://www.minlplib.org/pooling_sppc1pq.html)); `sppc0pq` 12%, `sppc3pq` 6.5%, `sppb0pq` 4.4%, `sppb2pq` 3.9%, `sppa0pq` 0.8%; `pooling_digabel16/18/19`, `pooling_epa2/3` open with <0.3% gaps. No published relaxation handles several attributes jointly at one pool. |
| Water-using / treatment networks (multi-contaminant, bilinear F·c) | Zhou–Liu–Du 2025 dynamic partition + adaptive bound contraction, "superior to commercial solvers on MIQCP" ([AIChE J](https://aiche.onlinelibrary.wiley.com/doi/10.1002/aic.18607)); Cheng–Li 2024 P*-formulation, provably at least as strong as P and SF formulations ([JOGO 89](https://link.springer.com/article/10.1007/s10898-023-01363-z)); Tristán–…–Grossmann–Bernal Neira 2024 QGDP water networks with energy recovery, Gurobi/BARON, 1 h limit ([arXiv:2407.19543](https://arxiv.org/html/2407.19543)); Bagajewicz-style bound contraction for reuse networks ([Water Sci Technol 2025](https://pubmed.ncbi.nlm.nih.gov/41468050/)). | MINLPLib (Castro–Teles 2013 and Karuppiah–Grossmann-type): `waterund32` ~10% (Gurobi dual), `waterund27` 7.7%, `waterund36` 8.3%, `wastewater11m2` 30%, `wastewater12m2` 26%, `wastewater13m2` 24%, `waterful2` 50% ([waterund32 page](https://www.minlplib.org/waterund32.html)). All bilinear QCPs of a few hundred variables. |
| Distillation with variable stages | Shortcut configurations: Tumbalam Gooty–Agrawal–Tawarmalani 2024, simultaneous hulls of fractions + RDLT + adaptive partitioning, 496 cases to 1% within 5 h; earlier BARON-based MINLPs could not scale to five components ([Oper Res 72:639](https://doi.org/10.1287/opre.2022.2340), [arXiv:2010.12113](https://arxiv.org/pdf/2010.12113)); extended to multicomponent products (Mathew et al. 2024, [CACE](https://www.sciencedirect.com/science/article/abs/pii/S0098135424000462)). Rigorous MESH with variable stages: only enumeration/set-trimming methods claim global optimality (Peccini et al. 2026 [AIChE J](https://aiche.onlinelibrary.wiley.com/doi/10.1002/aic.70406)); GDP with LD-SDA is local (Liñán/Bernal Neira, [CACE 2025](https://www.sciencedirect.com/science/article/abs/pii/S0098135424004113)). | Six-component and heat-integrated configurations; any global certificate for tray-by-tray GDP columns. No public open instance set. |
| Crude-oil / tank blending scheduling | Castro–Grossmann MDT-based global scheduling ([I&EC Res 2014](https://pubs.acs.org/doi/10.1021/ie503002k)); Ploussard et al. 2026 symmetric PWL MILP reformulations of "sequentially coupled bilinear programs" beating QP solvers on long horizons ([arXiv:2608.27312](https://arxiv.org/html/2608.27312)); Chen–Maravelias–Zhang 2022 tightened discretization MILPs for pooling ([arXiv:2207.03699](https://arxiv.org/abs/2207.03699)). | MINLPLib `crudeoil_li01/02/03/05/11/21` (Li–Misener–Floudas 2012 models) open with 0.05–1.2% gaps; `crudeoil_pooling_ct1/ct3/dt2` open, `ct1` closed by Gurobi alone (dual 210,537.26 vs primal 210,537.5) but BARON at 18% ([ct1 page](https://www.minlplib.org/crudeoil_pooling_ct1.html), [li05 page](https://www.minlplib.org/crudeoil_li05.html)). |
| Two-stage / multi-period nonconvex design | Cao–Zavala reduced-space B&B (JOGO 2019); Li–Grossmann GBD-based B&C with Lagrangean + Benders cuts ([JOGO 2019](https://link.springer.com/article/10.1007/s10898-019-00816-8)); Ogbe–Li joint decomposition ([JOGO 2019](https://link.springer.com/article/10.1007/s10898-019-00786-x)); Robertson–Cheng–Scott 2024 convergence order of value-function relaxations ([JOGO](https://link.springer.com/article/10.1007/s10898-024-01458-1)); Zhong–Cui–Nie polynomial lower approximation of recourse ([arXiv:2310.04243](https://arxiv.org/abs/2310.04243)). | No shared benchmark; papers use their own stochastic pooling / crude-selection sets. Progress is method-heavy; not a days-of-work target. |
| Potential-based networks (water distribution design, water supply operation, gas) | Okumusoglu–Kocuk 2025: SOC hull of pipe set, power-cone hull of compressor set, MISOCP framework beating BARON on GasLib ([arXiv:2503.15143](https://arxiv.org/abs/2503.15143), [JOGO 2026](https://link.springer.com/article/10.1007/s10898-026-01625-6)); Börner et al. 2025 polynomially separable cuts for potential-flow network design ([arXiv:2503.22327](https://arxiv.org/abs/2503.22327)); Humpola–Fügenschuh–Koch 2016 energy-based valid inequalities ([OR Spectrum](https://link.springer.com/article/10.1007/s00291-015-0390-2)). | MINLPLib `waternd_modena` 19%, `waternd_pescara` 14.5%, `waternd_fosspoly1` 92%, `waternd_hanoi` 4.9% (Bragalli et al. design instances, open since 2012); `waterno2_24` 85% (Gleixner–Held–Huang–Vigerske operative planning, [page](https://www.minlplib.org/waterno2_24.html)); `gasprod_sarawak16/81` open (0.2–0.4%). |

Contextual cross-class result worth knowing: Göß 2026 compares piecewise-linear
versus global parabolic relaxations (AC-OPF, trigonometric constraints) and
finds parabolic relaxations win at tight tolerances
([arXiv:2603.16505](https://arxiv.org/abs/2603.16505)); Dey–Han–Wang 2025
"extreme strong branching" for QCQPs outperforms commercial solvers on some
QCQP types ([arXiv:2510.20650](https://arxiv.org/abs/2510.20650)). Neither is
PSE-specific.

## 4. Candidates

Scores: I = importance, F = feasibility within days, N = confidence that the
specific combination is new (10 = certain).

### C1. SYNHEAT: homogeneity lift of the area constraint, common-factor hull, exact conic LMTD (I 8, F 8, N 6)

**Problem.** In SYNHEAT (isothermal mixing) all nonconvexity per match
(i,j,k) is the area constraint and the concave cost:

```
q_ijk ≤ U_ij · A_ijk · LMTD(dt_ijk, dt_ijk+1),      cost = c_f z_ijk + c A_ijk^β,  0<β<1,
```

with dt linear in stage temperatures and q coupled by linear energy balances.
LMTD (and the Chen approximation `(x·y·(x+y)/2)^{1/3}`) is concave and
positively homogeneous of degree 1 on the positive orthant; Mistry–Misener
prove LMTD^β concave for 0<β≤1 and RecLMTD^β strictly convex for β>0.

**Idea.** Use homogeneity to move the area into the LMTD argument:

```
A·LMTD(dt1, dt2) = LMTD(A·dt1, A·dt2).
```

Introduce `v1 = A·dt1`, `v2 = A·dt2` and replace the constraint by the
*convex* hypograph constraint `q ≤ U·LMTD(v1, v2)` (for Chen:
`q^3 ≤ U^3 · v1·v2·(v1+v2)/2`, a power-cone-representable constraint:
`t ≤ (v1 v2 s)^{1/3}`, `s=(v1+v2)/2`, `q ≤ U t`). The only remaining
nonconvexity is the pair of bilinears `v = A·dt` with a *common scalar factor*
A, whose leaves (dt1, dt2) lie in the polytope P defined by temperature bounds,
stage monotonicity and EMAT. For a scalar common factor the exact convex hull
is the Balas hull of the two endpoint slices:

```
conv{(A, dt, A·dt): A∈[A_L,A_U], dt∈P}
 = {(A, dt, v): dt = d¹ + d², v = A_L d¹ + A_U d², d¹ ∈ λP, d² ∈ (1−λ)P,
    A = λ A_L + (1−λ) A_U, λ ∈ [0,1]},
```

because `(A, dt, A dt) = λ(A_L, dt, A_L dt) + (1−λ)(A_U, dt, A_U dt)` with
`λ=(A_U−A)/(A_U−A_L)`. This is stronger than the product of McCormick
envelopes whenever P is not a box (it is exactly the RLT of P's inequalities
with `(A−A_L)` and `(A_U−A)`), and it is *exact when A is fixed*. Hence a
spatial B&B that branches **only on the areas A_ijk** (one variable per match)
has a relaxation error that vanishes with the width of the A-interval, with no
branching on temperatures, and the same branching simultaneously tightens the
secant of the concave cost `A^β`. The relaxation is a MISOCP/power-cone MIP
(exactly convex LMTD, no piecewise approximation of LMTD needed). Non-isothermal
mixing (heatexch_gen family) adds split-fraction × temperature products that
lie in the repo's flow × simplex hull class (`paper-network-simplex/`), a
natural extension.

**Bottleneck addressed.** Solvers relax `q·RecLMTD(dt)` or `A·LMTD(dt)`
as a bilinear product of a variable and a nonconvex-relaxed univariate/bivariate
term, then branch on temperatures and heat loads; the Mistry–Misener
tables show 35% (Model 1) and 7% (Model 2) solver root gaps on tiny instances
and MINLPLib still lists 30% / 13.6% gaps on `heatexch_gen1/gen3`.

**Closest prior work.** Mistry–Misener 2016 (convexity of RecLMTD^β,
outer approximation of RecLMTD, nf4r piecewise McCormick on q·RecLMTD; they do
not lift A into the LMTD argument and do not use the common-factor hull);
Björk–Westerlund 2002 signomial convexification with Paterson/Chen
([CACE 26:1581](https://www.sciencedirect.com/science/article/abs/pii/S0098135402001291));
Najman–Mitsos 2016 LMTD envelopes with quadratic convergence order
([ESCAPE 26](https://www.sciencedirect.com/science/chapter/bookseries/abs/pii/B9780444634283502721));
Kim–Bagajewicz 2015/2017 bound contraction using LMTD monotonicity; Escobar–Grossmann
2010 (LMTD moved to objective, source of `heatexch_gen*`). Manousiouthakis–Sourlas
1992 reformulate Chen/Paterson into quadratic constraints (cited in the
[2022 Frontiers survey](https://www.frontiersin.org/journals/sustainability/articles/10.3389/frsus.2022.976717/full)).
No source found uses degree-1 homogeneity to make the LMTD constraint convex
in lifted variables, and none uses the scalar-common-factor hull; the
Oh–Wiecek–Yang SIAM OP26 abstract on common-variable bilinear convexification
([abstract book](https://www.siam.org/media/r0be0xtr/op26_abstracts_v3.pdf))
is the main risk for the hull part, and the trick itself is simple enough that
it may be buried in the HENS literature (N 6, not higher).

**Effort.** 3–5 days: Pyomo SYNHEAT generator (Yee–Grossmann examples,
10SP1/15SP, Escobar–Trierweiler set, plus the three MINLPLib `heatexch_gen`
models), lifted formulation, root-relaxation gap comparison (original vs.
lifted) under Gurobi 13's own spatial B&B (a one-day experiment: pure
reformulation), then a custom A-only branching loop if the root gain is real.
Compare against BARON 26 / SCIP 10 / ANTIGONE on the same models.

### C2. Standard pooling with several qualities: joint few-attribute pool-output hull via the repo's fixed-linking-row oracle (I 7, F 6, N 5)

**Problem.** In the pq-formulation, for pool l and output j the flows
`w_ilj = q_il · y_lj` share the scalar factor `y_lj`, with linking rows
`Σ_i q_il = 1` and, per attribute a, `Σ_i λ_ia w_ilj − spec_ja y_lj ≤ s_ja`
(the slack `s_ja` absorbs other pools' contributions and is boxed). Luedtke et
al. 2020 characterised the hull for one attribute (non-polyhedral, three
parameter regimes) and observed limited effect on dense instances; Jalilian–Kocuk
2023 convexify the attribute-free rank-one block.

**Idea.** Treat the block with all W attributes jointly. The repo's theorem
(`results/common-factor-fixed-linking-optimization.md`; reviewed) gives an exact
linear-optimization oracle over the convex hull of

```
S = {(x, y, w): x∈[a,b], y∈box, w_i = x y_i, A y + B w ≤ c + d x}   (k linking rows)
```

by enumerating `C(n+k, k)` conditional LP bases and univariate sign intervals;
for n ≈ 5–10 inputs and k = 1+W ≤ 4 that is at most a few hundred bases per
block. Turn the oracle into a separator: for a relaxation point z, maximise
`π·z − h_S(π)` over `‖π‖≤1` by a bundle/level method (each evaluation is one
oracle call and yields a subgradient), yielding a most-violated cut for the
joint multi-attribute block. Add cuts at the root and at selected nodes on top
of Gurobi 13's or SCIP 10's relaxation (callback), compare with Luedtke cuts
and Jalilian–Kocuk polyhedral OA.

**Bottleneck.** The remaining 4–16% gaps on `sppb*/sppc*` instances come
from dense pools with several attributes, exactly where single-attribute hulls
lose. The joint hull is provably at least as strong and strictly stronger
whenever two attribute constraints are simultaneously active.

**Closest prior work.** Luedtke et al. 2020 (k = 2: simplex + one attribute);
Jalilian–Kocuk 2023 (no attributes in the hull); Dey–Kocuk–Santana 2020
rank-one convexifications ([JOGO](https://link.springer.com/article/10.1007/s10898-019-00844-4));
Gupte–Kalinowski–Rigterink–Waterer 2020 BQP-based hulls ([DO 36](https://arxiv.org/abs/1702.04813));
Khademnia–Davarnia 2025 bilinear terms over network polytopes ([MOR](https://arxiv.org/abs/2302.14151));
Tawarmalani 2026 finite hierarchies for disjoint bilinear programs (would
reach the same hull in ≤ m rounds, but no pooling computation reported);
Punnen–Sripratak–Karapetyan 2015 basis enumeration (credited in the repo's
literature audit). Oh–Wiecek–Yang (SIAM OP26) is again the main novelty risk.

**Effort.** 5–8 days; the theory and a verification script exist in the
repo (`code/common-factor-verify.py`), the new work is the separation loop,
pq-model generation for Alfaki–Haugland instances (MINLPLib `.gms`/`.nl` files
are available), and the solver callback. Risk: bundle-method separation may
be too slow per node; then root-only cuts must carry the result.

### C3. Multi-contaminant water networks: mixer-block hulls and concentration-only branching with LP certificates (I 7, F 7, N 4)

**Problem.** Water-using/treatment networks (Karuppiah–Grossmann, Castro–Teles,
Ahmetović–Grossmann superstructures) are bilinear QCP/MIQCPs in flows and
contaminant concentrations. MINLPLib `waterund*`, `wastewater*m2`, `waterful2`
show 8–50% gaps; Zhou et al. 2025 and Cheng–Li 2024 are the current frontier
(partitioning + bound contraction, formulation strengthening).

**Idea.** Two structural facts: (a) each splitter concentration `c_sw`
multiplies all outgoing flows `F_su` (common scalar factor; linking row
`Σ_u F_su = F_s`), and each mixer balance `F_u c_uw = Σ_s F_su c_sw` links the
W attribute products of the same flow — again a fixed-k common-factor block
(k = 1 + W), so the C2 oracle applies verbatim to every splitter–mixer block
with W ≤ 3 contaminants; (b) with all splitter concentrations fixed the
problem is an LP (or MILP with unit-existence binaries), so branching only on
the S·W concentrations gives a reduced-space B&B whose subproblems are LPs with
exact rational certificates. Combine: reduced-space B&B on concentrations,
block hulls at nodes, standard FBBT on flows. Bernal Neira's group already
models this class as (Q)GDP (Tristán et al. 2024) and has the GEHR/CEHR hull
reformulations for quadratic disjunctions
([Gusev–Bernal Neira 2025, arXiv:2508.16093](https://arxiv.org/abs/2508.16093)),
so the unit-existence disjunctions can be handled exactly in the relaxation.

**Bottleneck.** Solvers branch on both flows and concentrations; the strong
P*-formulation and RLT (Quesada–Grossmann 1995, Ruiz–Grossmann 2011) already
exploit the splitter identity, so the additional value must come from the
joint-attribute hull and from the LP-exact subproblems.

**Closest prior work.** Cheng–Li 2024 P*; Zhou et al. 2025 dynamic
partitioning; Castro–Teles 2013 comparison of MDT/PMC ([CACE](https://www.sciencedirect.com/science/article/pii/S0098135412003687));
Karuppiah–Grossmann 2006 Lagrangean cuts; Dey–Santana–Wang 2019 SOCP for
bipartite bilinear programs ([Opt Eng](https://link.springer.com/article/10.1007/s11081-018-9402-9));
Epperly–Pistikopoulos reduced-space B&B. Concentration-space branching per se
is known (MDT discretises concentrations), which is why N is 4; the
multi-attribute block hull is the new element.

**Effort.** 4–6 days on top of C2's separator (shared code). Even without
the hull, the reduced-space B&B with Gurobi LP subproblems is a one-day
baseline and gives immediate evidence on `waterund27/32/36`.

### C4. Crude-oil / tank-blending scheduling: time-chained flow × simplex hulls from the network–simplex paper (I 6, F 7, N 4)

**Problem.** Tank composition models use fractions `f_st` (share of crude s in
tank at period t, `Σ_s f_st = 1`) multiplying outflows and inventories; the
resulting bilinears are exactly "flow × simplex" products with sparse
observation patterns chained in time — the setting of
`paper-network-simplex/` (compressed exact extended hulls, cycle/theta cuts,
flat-chain oracles). MINLPLib `crudeoil_li*` instances are open with 0.05–1.2%
gaps after 13 years, `crudeoil_pooling_ct3/dt2` likewise.

**Idea.** Generate the compressed exact hull for each tank's time chain
(observed products are only those in the balances) and hand the strengthened
model to Gurobi 13 / SCIP 10; measure root gap closure and node counts on the
MINLPLib crude-oil instances versus the original MBQCP and versus Ploussard et
al.'s symmetric PWL MILPs.

**Closest prior work.** Alfaki–Haugland source-based (multi-commodity)
formulations for pooling ([JOGO 2013](https://link.springer.com/article/10.1007/s10898-016-0404-x));
Li–Misener–Floudas 2012 crude scheduling; Castro–Grossmann 2014; Ploussard et al.
2026; Khademnia–Davarnia 2025. The repo's paper itself states that general
simplex disaggregation was known; the contribution would be the demonstrated
effect on open scheduling instances.

**Effort.** 3–5 days (hull generator exists in `code/network_simplex*`; needs a
model parser for the `.gms`/`.nl` instances and a reformulation writer).

### C5. Potential-based network design and operation: cycle-space relaxations with energy duality (I 6, F 4, N 4)

**Problem.** `waternd_*` (Bragalli et al. 2012 pipe-diameter design,
[Opt Eng](https://link.springer.com/article/10.1007/s11081-011-9141-7)) carry
5–92% gaps, `waterno2_24` 85%. For fixed discrete choices the flow is the
unique minimiser of a strictly convex energy; relaxations ignore this.

**Idea.** Use the convex-duality (content/co-content) structure to derive
per-cycle valid inequalities in the lifted `(q_e, Δh_e)` space that bound the
dissipated energy of any feasible design from below by the relaxed design's
energy (Humpola–Fügenschuh–Koch type) and combine them with the exact
disjunctive hull of the per-pipe diameter-choice curves; certify with the
repo's exact potential-flow certificate pipeline (`code/potential_flow_mpd/`).

**Closest prior work.** Humpola–Fügenschuh–Koch 2016; Börner et al. 2025
(polynomial separation of a new cut class on real gas networks);
Okumusoglu–Kocuk 2025 (pipe/compressor hulls; MISOCP); Gleixner et al. 2012
(SCIP-based water supply operation). The direction is crowded and the cut
derivation is not a days-of-work item; kept as a lower-priority option because
the open gaps are the largest of all classes surveyed.

### C6. Distillation configurations and columns (I 7, F 3, N 5)

**Status.** Shortcut (Underwood) configuration MINLPs are solved to 1% for
≤ 5 components by Tumbalam Gooty et al. 2024 with simultaneous fraction hulls
and RDLT; six components, heat integration and non-CMO models remain open;
rigorous tray-by-tray GDP columns have no global method except enumeration
(Bagajewicz group). A theoretically justified idea would be monotone
(cascade) bounding of MESH stage compositions to build relaxations of the
stage-existence disjunctions; it is not realistic within days and no
benchmark set exists. Not recommended now, but it is the class most aligned
with Bernal Neira's GDP/LD-SDA work, so it should be revisited once C1–C3
tooling exists.

### C7. Two-stage / multi-period nonconvex design (I 7, F 4, N 4)

**Status.** Cao–Zavala, Li–Grossmann, Ogbe–Li and Robertson–Cheng–Scott cover
reduced-space B&B, Lagrangean/Benders cuts and their convergence order; the
scalar-common-factor hull (design variable × scenario variables) reduces to
McCormick across independent scenarios, so no cheap structural gain is
available. Not recommended.

## 5. Discarded as standard or already covered

- Piecewise McCormick / NMDT / adaptive partitioning (Castro, Zhou et al.
  2025, Alpine, strong partitioning), generic OBBT/FBBT, plain SDP or SOS
  hierarchies for pooling (Jalilian–Kocuk cite their scaling limits), ML-guided
  branching/partitioning.
- Storage sizing convexification: prior art recorded in
  `notes/research-20260912-energy-opportunities.md` (Bansal–Günlük;
  Morales 2025; Elgersma et al. 2024).
- HENS minimum-number-of-matches approximability: already listed in the
  2026-09-05 brainstorm (complexity, not solver work).

## 6. Recommendation

1. **C1 (SYNHEAT homogeneity lift + common-factor hull + conic LMTD).**
   Highest expected return per day: a pure reformulation test under Gurobi 13
   is one day, the MINLPLib `heatexch_gen1/gen3` gaps (30%, 13.6%) give an
   unambiguous target, the theory (degree-1 homogeneity, exactness of the
   Balas hull for a scalar factor, A-only branching) is short and checkable, and
   the class is central to Bernal Neira's PSE audience. Main risk: the trick
   may exist unnoticed in older HENS papers; check Björk–Westerlund 2002 and
   Escobar–Grossmann 2010 in full before writing.
2. **C2 (joint multi-attribute pool hull via the repo's fixed-linking oracle).**
   Reuses a reviewed repository theorem, targets open MINLPLib instances with
   4–16% gaps, and sits between two well-cited prior hulls (Luedtke et al.;
   Jalilian–Kocuk), which makes the comparison clean. Main risks: separator
   speed, and the Oh–Wiecek–Yang 2026 common-variable convexification.
3. **C3 (water networks: mixer-block hulls + concentration-only branching).**
   Shares C2's separator, adds an LP-certified reduced-space B&B, and connects
   to the group's own QGDP water models and exact hull reformulations. Its
   novelty is the lowest of the three, so it should be run as evidence-gathering
   alongside C2 rather than as a standalone paper.

C4 is a cheap add-on if the network–simplex hull code is easy to retarget;
C5–C7 are recorded for later.

## 7. Sources consulted

- Gurobi 13: https://www.gurobi.com/news/gurobi-releases-version-13-0-with-improved-performance-and-new-solving-capabilities/ ; https://docs.gurobi.com/projects/optimizer/en/current/reference/releasenotes/changes.html
- SCIP 10: https://arxiv.org/abs/2511.18580
- GAMS solver year 2025 (BARON updates): https://www.gams.com/blog/2026/01/the-year-2025-for-gams-solvers/
- Mistry & Misener 2016, CACE 94:1–17: https://www.sciencedirect.com/science/article/pii/S0098135416302216 ; manuscript https://spiral.imperial.ac.uk/bitstreams/73f1f43f-70a2-4142-84c7-54b3798583b5/download
- Najman & Mitsos 2016, ESCAPE 26: https://www.sciencedirect.com/science/chapter/bookseries/abs/pii/B9780444634283502721
- Björk & Westerlund 2002, CACE 26:1581: https://www.sciencedirect.com/science/article/abs/pii/S0098135402001291
- Kim & Bagajewicz 2017, I&EC Res: https://pubs.acs.org/doi/10.1021/acs.iecr.6b04686 ; PDF https://www.ou.edu/class/che-design/pub-papers/Global%20Optimization%20of%20Stages-substages(kim%20and%20Bagajewicz)-17.pdf
- Faria, Kim & Bagajewicz 2015, I&EC Res: https://pubs.acs.org/doi/10.1021/ie5032315
- Oliva et al. 2024, AIChE J: https://aiche.onlinelibrary.wiley.com/doi/10.1002/aic.18450 ; Chang et al. 2020: https://aiche.onlinelibrary.wiley.com/doi/10.1002/aic.16267
- HENS survey (Frontiers 2022): https://www.frontiersin.org/journals/sustainability/articles/10.3389/frsus.2022.976717/full
- MINLPLib pages: https://www.minlplib.org/heatexch_gen1.html , https://www.minlplib.org/heatexch_gen2.html , https://www.minlplib.org/heatexch_gen3.html , https://www.minlplib.org/synheat.html , https://www.minlplib.org/pooling_sppc1pq.html , https://www.minlplib.org/waterund32.html , https://www.minlplib.org/waterno2_24.html , https://www.minlplib.org/watersbp.html , https://www.minlplib.org/crudeoil_pooling_ct1.html , https://www.minlplib.org/crudeoil_li05.html , https://www.minlplib.org/gasnet.html , https://www.minlplib.org/instances.html
- Luedtke, D'Ambrosio, Linderoth, Schweiger 2020: https://epubs.siam.org/doi/10.1137/18M1174374 ; https://arxiv.org/abs/1803.02955
- Jalilian & Kocuk 2023: https://arxiv.org/abs/2306.10810
- GALINI (Ceccon, Misener et al. 2021): https://arxiv.org/abs/2105.01687
- Gupte, Kalinowski, Rigterink, Waterer 2020: https://arxiv.org/abs/1702.04813
- Dey, Kocuk, Santana 2020: https://link.springer.com/article/10.1007/s10898-019-00844-4
- Dey, Santana, Wang 2019: https://link.springer.com/article/10.1007/s11081-018-9402-9
- Khademnia & Davarnia 2025: https://arxiv.org/abs/2302.14151
- Tawarmalani 2026 finite hierarchies: https://arxiv.org/abs/2405.11068 ; https://link.springer.com/article/10.1007/s10107-026-02326-4
- Oh, Wiecek, Yang, SIAM OP26 abstract: https://www.siam.org/media/r0be0xtr/op26_abstracts_v3.pdf
- Kannan, Nagarajan, Deka 2025: https://arxiv.org/abs/2301.00306
- Dey, Han, Wang 2025: https://arxiv.org/abs/2510.20650
- Chen, Maravelias, Zhang 2022: https://arxiv.org/abs/2207.03699
- Alfaki & Haugland multi-commodity formulations: https://link.springer.com/article/10.1007/s10898-016-0404-x
- Zhou, Liu, Du 2025, AIChE J: https://aiche.onlinelibrary.wiley.com/doi/10.1002/aic.18607
- Cheng & Li 2024, JOGO: https://link.springer.com/article/10.1007/s10898-023-01363-z
- Castro & Teles 2013, CACE: https://www.sciencedirect.com/science/article/pii/S0098135412003687
- Barros Pedroza & Ravagnani 2025: https://pubmed.ncbi.nlm.nih.gov/41468050/
- Tristán, Fallanza, Ibáñez, Grossmann, Bernal Neira 2024: https://arxiv.org/html/2407.19543
- Gusev & Bernal Neira 2025 (exact hull reformulations for QCGDP): https://arxiv.org/abs/2508.16093
- Liñán & Bernal Neira, LD-SDA, CACE 2025: https://www.sciencedirect.com/science/article/abs/pii/S0098135424004113
- Tumbalam Gooty, Agrawal, Tawarmalani 2024, Oper Res: https://doi.org/10.1287/opre.2022.2340 ; https://arxiv.org/pdf/2010.12113
- Mathew et al. 2024, CACE: https://www.sciencedirect.com/science/article/abs/pii/S0098135424000462
- Peccini et al. 2026, AIChE J: https://aiche.onlinelibrary.wiley.com/doi/10.1002/aic.70406
- Castro & Grossmann 2014, I&EC Res: https://pubs.acs.org/doi/10.1021/ie503002k
- Ploussard et al. 2026: https://arxiv.org/html/2608.27312
- Li & Grossmann 2019, JOGO: https://link.springer.com/article/10.1007/s10898-019-00816-8 ; Ogbe & Li 2019: https://link.springer.com/article/10.1007/s10898-019-00786-x ; Robertson, Cheng, Scott 2024: https://link.springer.com/article/10.1007/s10898-024-01458-1 ; Zhong, Cui, Nie 2023: https://arxiv.org/abs/2310.04243
- Okumusoglu & Kocuk 2025/2026: https://arxiv.org/abs/2503.15143 ; https://link.springer.com/article/10.1007/s10898-026-01625-6
- Börner et al. 2025: https://arxiv.org/abs/2503.22327 ; Humpola, Fügenschuh, Koch 2016: https://link.springer.com/article/10.1007/s00291-015-0390-2
- Bragalli et al. 2012, Opt Eng: https://link.springer.com/article/10.1007/s11081-011-9141-7
- Göß 2026: https://arxiv.org/abs/2603.16505
- Repository: `results/common-factor-fixed-linking-optimization.md`, `notes/common-factor-literature-audit.md`, `paper-network-simplex/README.md`, `notes/research-20260912-energy-opportunities.md`, `notes/candidate-directions-2026-09-05.md`
