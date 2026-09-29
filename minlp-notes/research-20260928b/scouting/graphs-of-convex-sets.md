# Scout report: graphs of convex sets (`graphs-of-convex-sets`)

Date: 2026-09-28. Scratch code, downloaded sources and outputs:
`research-20260928b/scouting/graphs-of-convex-sets/` (sources under `src/`).

## Summary

- **What is proved in the literature.** The shortest-path problem (SPP) in a graph of
  convex sets (GCS) is NP-hard even for interval sets, for acyclic graphs, and for
  disjoint sets with homogeneous lengths. The perspective mixed-integer convex program
  (MICP) of Marcucci–Umenberger–Parrilo–Tedrake is exact. Its relaxation is exact when
  all sets are points and can be arbitrarily loose in general. Beyond that, the
  literature contains no a priori bound on the integrality gap and no approximation
  guarantee for rounding. Every tightness claim in 2022–2026 GCS papers is empirical.
- **First-pass result (new as far as this search could establish).** Consider the
  relaxation strengthened with the vertex-local convex hull that Marcucci et al. already
  describe (their eq. (7.4)); call it `REL_H`. On acyclic graphs without edge
  constraints, its integrality gap is at most a flow-weighted sum of **Jensen
  (concave-envelope) defects** of the edge lengths. A Markov-chain rounding driven by
  the hull's edge-pair variables attains the bound in expectation, and a second-order
  line-graph shortest path attains it deterministically. For norm lengths this gives
  `OPT ≤ sec(θ_max)·REL_H`, where `θ_max` is the largest half-angle of the cone of
  feasible edge displacements. The gap is therefore second order in the ratio of set
  size to separation. Other consequences:
  - The relaxation is exact for affine lengths with the hull, and exact in 1D with
    disjoint intervals even without it.
  - Squared lengths obey a Kantorovich-type bound. This explains why Euclidean-length
    relaxations are "almost always exact" while squared-length ones are not.
  - The basic relaxation (without the hull) is only first-order tight. An explicit
    family has `OPT/REL − 1 = Θ(1/R)`, while `OPT/REL_H − 1 = Θ(1/R²)`.
- **Negative findings.**
  - With overlapping sets there is no a priori bound. A 6-vertex 1D acyclic instance
    with Euclidean lengths has `REL = δ` and `OPT = 2 − δ`.
  - In a motion-planning (order-1, polygonal) formulation, gaps are not caused by
    obstacles alone. Simply connected corridors covered by overlapping boxes gave gaps in
    35/35 instances (mean 5.7%, max 16%), even with lifted two-cycle cuts.
  - A "door" (line-graph) reformulation removes the gap around a single obstacle
    (29% to 0%). It does not help in corridors, where the relaxation teleports positions
    through fractional cycles among overlapping sets.
- **Complexity map.** Euclidean-length GCS SPP is polynomial in 1D (breakpoint dynamic
  program) and NP-hard in 2D (a direct consequence of Dror–Efrat–Lubiw–Mitchell polygon
  touring). The `ℓ1`-length problem with boxes is polynomial in any fixed dimension. The
  squared-length problem is `n^{1−ε}`-inapproximable via longest path.
- **Recommendation.** The best question is an a priori gap theory for the practical
  formulations (edge constraints, overlapping covers), with Theorem 1 below as the base.
  It is clean and feasible, but its depth is moderate and the hardest part (the overlap
  regime) is open. Score **5/10**.

## 1. Frontier map

### 1.1 Problem and formulations (Marcucci et al., SIOPT 2024; local `marcucci2024-shortest-paths-in-graphs-of`)

The data are a digraph `G=(V,E)`, compact convex sets `X_v ⊂ R^n`, and proper closed
convex lengths `ℓ_e(x_u,x_v) ≥ 0`, possibly `+∞` outside an edge set `X_e`. The SPP
in GCS minimises `Σ_{e∈p} ℓ_e(x_u,x_v)` over `s–t` paths `p` and points `x_v ∈ X_v`.

- **MICP (5.5).** Take the network-flow LP with degree constraints. For each edge add
  perspective copies `(z_e, y_e) ∈ X̃_u` and `(z'_e, y_e) ∈ X̃_v`, conserve positions via
  `Σ_{in(v)} z'_e = Σ_{out(v)} z_f`, and use the objective `Σ ℓ̃_e(z_e,z'_e,y_e)`.
  Theorem 5.7: with `y` binary, this is exact. Its size is `O(|E|)` binaries and
  `O(n|E|)` continuous variables. The relaxation of (5.5) is called `REL` below.
- **Set-based bilinear relaxation (Sec. 7).** Relaxation (5.5) is the first-level
  reformulation–linearization technique (RLT) / Lovász–Schrijver-type relaxation of
  `Z_v = x_v y_v^T`. It is exact at the extreme points of `Y_v` (Lemma 7.4), but it is
  not `conv S_v` in general (Prop. 8.1 of the thesis, `X = Y = [−1,1]²`). It is the
  convex hull when `Y` is an interval (thesis Prop. 8.2).
- **Vertex-local convex hull (7.4).** This is the disjunctive description with one copy
  per extreme point of `Y_v`, i.e. per (in-edge, out-edge) pair. Its size is
  `Σ_v |in(v)||out(v)|`. Marcucci reports it is stronger but slower. With it added, the
  relaxation is called `REL_H` below.
- **Dual (thesis Sec. 9.4.2).** The dual of the relaxation, for acyclic graphs and
  without degree constraints, maximises `p_s − p_t` over **affine potentials**
  `r_v^T x + p_v` that satisfy the edge inequalities on `X_u × X_v`. So `REL` is the best
  lower bound certifiable with affine cost-to-go functions. Morozov et al. (arXiv
  2409.19543) note this and replace affine with convex-quadratic potentials via
  semidefinite programming (SDP).

### 1.2 Complexity results

| Result | Assumptions | Statement | Source |
|---|---|---|---|
| Thm 3.1 SIOPT / Thm 9.2 thesis | cyclic digraph; `X_s={0}`, `X_t={1}`, `X_v=[0,1]`; squared Euclidean lengths | NP-hard (Hamiltonian path; a path with `K` edges costs exactly `1/K`) | local fulltext p.4–5 |
| Thm 3.2 SIOPT | acyclic, disjoint sets, positively homogeneous lengths | NP-hard; proof omitted, adapted from Canny–Reif 3D Euclidean shortest path (dimension not stated) | local fulltext p.5 |
| Thm 9.1 thesis | acyclic layered graph, sets `{x∈[0,1]^n : x_k = a}`, zero costs plus edge constraint `x_u=x_v`; or norm lengths with no edge constraints | NP-hard; with norm lengths, "`OPT = 0` iff the 3SAT instance is satisfiable" | thesis p.91–92 |
| Thm 9.3 thesis | disjoint rectangles in 2D, squared lengths, cyclic | NP-hard | thesis p.93 |
| Bipartite matching in GCS | any | polynomial; the MICP relaxation is exact (Prop. 2) | arXiv 2510.20184 §6.5, App. A |
| Shortest walk in GCS | — | NP-hard (thesis reduction) | arXiv 2507.10878 §II |

### 1.3 Exactness and tightness results known

- Singletons: the relaxation equals the flow LP and is exact (SIOPT Remark 5.8).
- Relaxation (5.5) is exact at binary `y` (Theorem 5.7; Lemma 7.4 generalises an RLT
  result of Adams–Sherali).
- Degree constraints are needed. Example 5.10 (cyclic, squared lengths) has
  relaxation 1 and true value 2 without them.
- Section 9.4 (SIOPT) gives a symmetric 5-vertex acyclic example with a 5% gap and a
  variant with a 100% gap (relaxation 0 versus 2). The variant uses zero-length source
  edges.
- The empirical record is consistent:
  - SIOPT §9.2: maximum gaps of 28.9% (n=20) and 32.9% (|E|=500) with squared lengths;
    the relaxation is "almost always exact" with Euclidean lengths.
  - Science Robotics (arXiv 2205.04422): certified gaps up to 27.1%, usually under 4–7%.
  - Multi-query (2409.19543): affine lower bounds are poor compared with quadratic ones.
  - Unified method (2510.20184): SPP and minimum spanning arborescence (MSAP) are tight.
- **No a priori gap bound, rounding guarantee or approximation ratio was found in any
  GCS paper examined** (§1.6).

### 1.4 Rounding and algorithms

- **Randomized depth-first rounding** (thesis §9.5). Sample out-edges with probability
  `y_f/y_v` and solve the fixed-path convex restriction. It is guaranteed feasible when
  every restriction is feasible. There is no cost guarantee. Thesis Remark 9.3 explains
  why greedy deterministic rounding is bad.
- **Search methods.**
  - A*-GCS (2407.17413): bounds from a relaxation restricted to explored vertices.
  - GCS* (2407.08848): forward search with domination checks; complete and optimal.
  - IxG (2410.08909): implicit graph search.
  - Multi-query SDP cost-to-go (2409.19543).
  - Shortest walks with piecewise-quadratic SDP lower bounds (2507.10878).
- **Traveling-salesman lines.**
  - GHOST (2511.06471): best-first search; optimal and bounded-suboptimal.
  - Augmented GCS (2604.06406): Held–Karp states.
  - Steiner TSP branch and bound (2608.21319): `ε`-certificates.
  - Moving-target TSP (2403.04917).
  - All guarantees are search optimality or `ε`-suboptimality certificates, not
    relaxation-gap theory.
- **Stronger relaxations.**
  - Logic-network-flow Fourier–Motzkin elimination (2509.24235): "provably tighter" than
    logic-tree formulations, but no gap bound.
  - Contact-rich SDP (2402.10312).
  - Occupation-measure GCS for hybrid control (Buehrle et al., 2507.19210): measures are
    conserved at vertices, with a moment hierarchy.

### 1.5 Relation to classical results

- Flow-LP integrality (network matrices). With singletons, GCS is the classical SPP.
- Perspective reformulation: Ceria–Soares disjunctive hull, Frangioni–Gentile,
  Günlük–Linderoth. Each edge is an on/off indicator of a convex cost. The GCS twist is
  that indicators share continuous vertex variables through conservation of first
  moments.
- RLT / Lovász–Schrijver: `REL` is level one; the vertex hull is the disjunctive hull of
  one vertex.
- Touring polygons (Dror–Efrat–Lubiw–Mitchell, STOC 2003). Convex polygons in fixed
  order are polynomial under `L2`. The problem is NP-hard for nonconvex polygons, "or
  even if each `P_i` consists of a pair of segments with a shared endpoint". I confirmed
  this wording via the introduction of arXiv 2605.07882; I did not open the original.
  Under `L1` with orthogonal polygons it is polynomial (2605.07882).
- Euclidean shortest paths: polynomial in 2D, NP-hard in 3D (Canny–Reif), with a
  Papadimitriou-type approximation. TSP with neighborhoods (Arkin–Hassin, and others,
  cited in SIOPT) is related but was not rechecked here.
- Extended formulations of dynamic programming (Martin–Rardin–Campbell 1990, recalled,
  not rechecked). The pair-variable rounding below resembles DP extended formulations.
  This is a novelty risk for Corollary A.

### 1.6 Sources examined

- **Local.**
  - `literature/papers/marcucci2024-shortest-paths-in-graphs-of/{paper.md,fulltext.md}`:
    read in full (Thms 3.1–3.2, 5.7; Lemmas 5.4, 7.4; Prop. 7.1; eq. (7.4); Examples
    5.10 and 9.4).
  - GCS mentions in `research-20260928/solver/branching-curvature-prior.md` and in
    citations in the `tawarmalani2026`, `atamturk2026` and `shoja2025` full texts
    (reference lists only).
- **Marcucci thesis** (MIT 2024,
  `groups.csail.mit.edu/robotics-center/public_papers/Marcucci24a.pdf`,
  `src/marcucci-thesis.txt`): Ch. 8 (Thm 8.1, Props 8.1–8.2, Lemmas 8.1–8.2), Ch. 9
  (Thms 9.1–9.3, §9.4 dual, §9.5 rounding), Ch. 12 conclusions.
- **arXiv full texts** (in `src/`):
  - 2510.20184 (unified GCS method; Props 1–2, Section 3, conclusions)
  - 2205.04422 (Science Robotics; §8.2, App. A.1–A.2)
  - 2409.19543 (multi-query; Lemma 1, affine versus quadratic bounds)
  - 2507.10878 (shortest walks)
  - 2407.17413 (A*-GCS; Thms 1–2)
  - 2509.24235 (logic network flow; Thms 4–5)
  - 2507.19210 (measure relaxations)
  - 2511.06471 (GHOST; Thms 1, 3, 4)
  - 2604.06406 (augmented GCS TSP)
  - 2608.21319 (Steiner TSP; Thm 1)
  - 2605.07882 (touring orthogonal polygons; hardness statements)
- **arXiv API listing** of all 41 abstracts matching "graph(s) of convex sets"
  (`src/arxiv_gcs.json`), scanned for tightness, gap, approximation and complexity
  claims. None proves a gap bound.
- **Web searches** (about 12 queries) covered tightness, integrality gaps, approximation,
  complexity in fixed dimension, SDP potentials, GCS*, TSP and facility location.
- **Recalled, not re-fetched:** Björklund–Husfeldt–Khanna, ICALP 2004 (directed longest
  path not approximable within `n^{1−ε}` unless P=NP). I could not re-verify it because
  Springer and dblp blocked fetches.
- **Novelty caution.** The session-wide web-search budget ran out mid-scout, so later
  checks used only arXiv API queries and direct fetches. An unsuccessful search does not
  establish novelty. The Jensen/perspective ingredients are standard, and results
  similar to Corollary A may exist in the dynamic-programming extended-formulation or
  disjunctive-programming literature.

## 2. Open questions

**Q1 (best). An a priori integrality-gap theory for the GCS perspective relaxation in
terms of geometry.** Find computable geometric parameters `κ` such that `OPT ≤ κ·REL`
(or an additive analogue) holds for the formulations used in practice. Specifically:

- (a) the basic relaxation `REL` versus the vertex hull `REL_H`;
- (b) formulations with edge constraints (Bézier continuity, derivative matching, PWA
  dynamics);
- (c) the overlapping-cover regime of motion planning, where all separation-based
  parameters are infinite.

Evidence that it is open: none of the sources in §1.6 states such a bound. The SIOPT
paper and the thesis present only the 100%-gap example and empirical statistics. §3
settles (a) for acyclic graphs without edge constraints and gives evidence for (c); (b)
and (c) remain open.

**Q2. Approximability threshold versus aperture.** For Euclidean-length GCS whose edges
have displacement cones of half-angle at most `θ`, Theorem 1 gives a deterministic
polynomial `sec θ = 1 + θ²/2 + O(θ⁴)` approximation. Is the SPP NP-hard to approximate
within `1 + cθ²` for some `c > 0`?

- Without separation, no finite ratio is possible in variable dimension (thesis
  Thm 9.1: the zero test is NP-hard).
- A layered 3SAT embedding with layer spacing `L` gives only `1 + θ²/poly(n,m)`
  hardness, because deviations can be spread over many steps.
- I found no source addressing this.

**Q3. Low-dimensional complexity.**

- (i) Squared Euclidean lengths, 1D intervals, acyclic graph: in P or NP-hard? The
  Hamiltonian reduction needs cycles; the breakpoint argument of Prop. 6(a) fails
  because optimal positions are not at breakpoints.
- (ii) Euclidean lengths in 2D with pairwise-disjoint convex sets on an acyclic graph.
  The 2D hardness via polygon touring uses segments that share an endpoint.
- (iii) Is there a `(1+ε)` scheme in fixed dimension `n ≥ 2`? Grid discretisation looks
  routine when `s` and `t` are distinct points.

**Q4 (lower priority; overlaps repository topics).** `REL` is the first-moment
truncation of a measure-valued flow linear program (LP) that is exact on acyclic graphs:
edge measures on `X_u×X_v` with vertex marginals conserved. Its dual uses affine
potentials; quadratic potentials give Morozov-type SDPs. What are the convergence rates
of moment or edge-pair liftings, and when is convergence finite? This overlaps the
repository's Lasserre/Putinar work, so it is not recommended.

## 3. Best question (Q1): first-pass mathematics

### 3.1 Setting

- `G` is a digraph; `s` has no in-edges and `t` has no out-edges.
- `X_v` is compact convex; `ℓ_e` is convex and finite on `K_e := X_u × X_v`; there are
  no edge constraints. Vertex costs could be added and charged per pair point.
- `REL` is (5.5).
- `REL_H` adds, for each `v ∉ {s,t}` and each pair `e ∈ in(v)`, `f ∈ out(v)`, variables
  `λ_{ef} ≥ 0` and `w_{ef}` with `(w_{ef}, λ_{ef}) ∈ X̃_v`,
  `Σ_f λ_{ef} = y_e`, `Σ_e λ_{ef} = y_f`, `Σ_f w_{ef} = z'_e` and `Σ_e w_{ef} = z_f`.
  This is the projection of eq. (7.4).
- `REL ≤ REL_H ≤ OPT`. Notation: `z̄ = z/y` and `w̄ = w/λ`.

### 3.2 Theorem 1 (Jensen-defect rounding)

Let `G` be acyclic and let `(y,z,z',λ,w)` be feasible for `REL_H`. Let `cav_e` denote
the concave envelope of `ℓ_e` over `K_e`. Then

`OPT ≤ Σ_e y_e · cav_e(z̄_e, z̄'_e)`, and hence
`OPT − REL_H ≤ Σ_e y_e · (cav_e − ℓ_e)(z̄_e, z̄'_e) ≤ Σ_e y_e · Δ_e`,

where `Δ_e = max_{K_e}(cav_e − ℓ_e)`.

The same holds on arbitrary digraphs, without the degree constraints, if
`ℓ_e(x,x') = g(x'−x)` for a single sublinear `g ≥ 0`.

*Proof.*

1. **Markov chain.** Choose the first edge `f ∈ out(s)` with probability `y_f`. At
   `v ∉ {s,t}`, entered through `e`, choose `f` with probability `λ_{ef}/y_e`.
2. **Positions.** Place each visited `v` at `x_v := w̄_{ef} ∈ X_v`. Place `s` at the
   tail point `z̄_f` of the first edge and `t` at the head point `z̄'_e` of the last edge.
3. **Edge marginals.** By topological induction, `P(f used) = Σ_e y_e·λ_{ef}/y_e = y_f`,
   and `P(d, e consecutive) = λ_{de}`.
4. **Conditional means.** Given that `e=(u,v)` is used,
   `E[x_v | e] = Σ_f (λ_{ef}/y_e) w̄_{ef} = z̄'_e` and
   `E[x_u | e] = Σ_d (λ_{de}/y_e) w̄_{de} = z̄_e`.
5. **Jensen step.** `(x_u, x_v) ∈ K_e`, so `E[ℓ_e(x_u,x_v) | e] ≤ cav_e(E[(x_u,x_v) | e])`.
   Summing with weights `y_e` bounds the expected cost of a feasible path, so `OPT` is
   at most that bound.
6. **Derandomization.** A shortest path over states = edges with positive `y`, with
   transitions `λ_{ef} > 0` and costs that depend on consecutive edge triples
   `(d,e,f)`, finds a path no worse than the expectation, in polynomial time.
7. **Cyclic case.** The chain has no closed class reachable from `s`. A closed class has
   zero inflow by conservation of `λ`. So the chain is absorbed at `t` almost surely and
   the expected number of traversals of `f` equals `y_f`. Revisits are shortcut: if the
   walk is at `v` at times `i < j`, replace the closed subwalk by one step from `p_i`.
   Subadditivity gives `g(p_{j+1}−p_i) ≤ g(p_{j+1}−p_j) + Σ_{k=i}^{j−1} g(p_{k+1}−p_k)`,
   so the cost does not increase. ∎

**Corollary A (affine lengths).** If every `ℓ_e` is affine on `K_e` and `G` is acyclic,
then `REL_H = OPT`. The problem is then polynomial: on the line graph, the cost of
passing through `v` from `e` to `f` is a support-function value of `X_v`.

`REL` alone can fail. In Exp 14 (a square vertex with two in-edges and two out-edges and
crossing linear costs), `REL = −4` while `REL_H = OPT = −2`.

**Corollary B (norms and aperture).** Let `ℓ_e = g_e(x'−x)` with `g_e` sublinear and
define

`κ_e := inf{κ : ∃a, a^T w ≤ g_e(w) ∀w, and g_e(w) ≤ κ·a^T w ∀w ∈ X_v−X_u}`.

Then `OPT ≤ Σ_e κ_e ℓ̃_e(z_e,z'_e,y_e) ≤ max_e κ_e · REL_H`. The proof uses
`E g(W) ≤ κ·a^T E W ≤ κ·g(E W)`.

- For the Euclidean norm, `κ_e = sec θ_e`, where `θ_e` is the half-angle of the
  narrowest circular cone containing `X_v − X_u`. This is finite iff `X_u ∩ X_v = ∅`.
- For balls, `sin θ_e = (r_u+r_v)/‖c_v−c_u‖`.
- So the relative gap is at most `sec θ_max − 1 ≈ θ_max²/2`. It is second order in the
  ratio of set size to separation.
- For `ℓ1`, `κ_e = 1` whenever `X_v − X_u` lies in one closed orthant, so `REL_H` is
  exact for sign-monotone `ℓ1` instances.

**Corollary C (squared norms).** With `m_e, M_e` the smallest and largest `‖w‖` over
`X_v − X_u`,

`κ_e^sq ≤ sec²θ_e · (M_e+m_e)²/(4M_e m_e)`.

The proof combines `‖E W‖ ≥ cos θ·E‖W‖` with the Kantorovich inequality. The factor
does not tend to 1 when directions agree but step lengths vary.

This is a first mechanism-level explanation of the empirical difference:

- Sublinear lengths lose only through **directional** dispersion of fractional
  displacements.
- Squared lengths also lose through **length** dispersion. Mixing paths with different
  numbers of steps is exactly the Hamiltonian-reduction effect, and it grows with graph
  density and dimension, as SIOPT §9.2 observed.

### 3.3 Basic versus hull relaxation

**Proposition 2.** A feasible point of `REL` extends to `REL_H` at vertex `v` if either:

- (i) `v` has in-degree ≤ 1 or out-degree ≤ 1 in `supp(y)`: take `w_{ef} = z_f`
  (respectively `z'_e`); or
- (ii) `X_v` is a simplex.

*Proof of (ii).* On a simplex, every measure with barycentre `m` is dominated in convex
order by the unique vertex measure with barycentre `m`. Couple the arrival labels and
the departure labels to that vertex measure (Strassen) and glue them conditionally
independently. The pair points `E[X | e,f]` have the required row and column means. ∎

- Hence in 1D, `REL = REL_H`.
- With Corollary B, every acyclic 1D instance with disjoint intervals on every edge and
  lengths `α w⁺ + β w⁻` has `REL = OPT`.
- Numerical check (Exp 5): on 80 random acyclic 1D instances, `max(OPT − REL) = 6e−8`
  and `|REL_H − REL| ≤ 1.1e−7`.
- Triangles (Exp 13): `max(REL_H − REL) = 1.2e−7` on 30 instances.

**Proposition 3 (repair).** For any feasible point of `REL`, let `μ_v^in` and `μ_v^out`
be the flow-weighted arrival and departure point measures at `v`, and let `L` be the
Lipschitz constant of the lengths in the tail argument. Then

`REL_H ≤ REL + L·Σ_v y_v·W1(μ_v^in, μ_v^out)`.

*Proof.* Move the departure points to `b'_f = Σ_e π(e,f) a_e / y_f`, where `π` is an
optimal coupling. The result is hull-feasible at `v`, and vertices do not interact. ∎

With Corollary B this gives `OPT ≤ κ_max·(REL + L·Σ_v y_v W1_v)`.

**Separation (Exp 3).** Take `v = [−1,1]²`. In-neighbours are points at distance `R`
along `±(1,1)` and out-neighbours along `±(1,−1)`. `REL` realises a "diagonal
crossing": arrivals at `(1,1)` and `(−1,−1)`, departures at `(1,−1)` and `(−1,1)`. The
means are equal, but the configuration is not hull-feasible.

| R | OPT/REL − 1 | OPT/REL_H − 1 | sec θ − 1 |
|---|---|---|---|
| 5 | 7.2e−2 | 5.1e−3 | 4.3e−2 |
| 20 | 1.5e−2 | 2.7e−4 | 2.5e−3 |
| 80 | 3.7e−3 | 1.6e−5 | 1.6e−4 |

`OPT − REL ≈ 1.43` is constant while `OPT ≈ 4.8R`. So `REL` has a first-order gap and
`REL_H` a second-order one. No bound of the form `OPT ≤ κ·REL` holds for the basic
relaxation.

**Sharpness (Exp 4).** A symmetric fork–merge gadget with disjoint balls reaches
`(OPT/REL_H − 1)/(sec θ − 1) ≈ 0.499` under local search. So Corollary B is tight up to
about a factor 2 in the excess. Only the edges entering a fork and leaving a merge lose.

### 3.4 Limits: overlapping sets and motion planning

**Proposition 5 (no a priori bound with overlap).** The 1D acyclic instance
`s={0} → A=[−1,1] → {P={1} | M={−1}} → B=[−1,1] → t={δ}` with lengths `|x_v−x_u|` has
`REL = REL_H = δ` and `OPT = 2−δ` (Exp 1).

The relaxation forks at `A` and merges at `B` with arrival and departure means that
match. The instance is polynomial by Prop. 6(a), so the gap is a formulation artifact,
not a hardness phenomenon.

**Motion planning, order 1.** Regions are overlapping boxes. The vertex variable is a
segment in the box, with continuity at doors enforced in perspective form. The two-cycle
cuts follow Science Robotics App. A.1 and Lemma 5.4. Code: `mp.py`, Exps 8, 9, 11, 12.

| Instance class | Result |
|---|---|
| Ring around a square obstacle | gap 29.2% symmetric, 27.7% and 22.8% when perturbed (`ε` = 0.05, 0.2); robust to asymmetry |
| Random box unions | simply connected: 0/25 gaps; with holes: 2/25 |
| Adversarial simply connected zigzag corridors with overlapping parallel lanes | gaps in 35/35 (mean 5.7%, max 16.0%); still 34/35 with lifted two-cycle cuts |
| Same corridors with region-level vertex hull and no immediate backtracking | mean 5.7% → 4.9% |
| Ring with vertex hull | unchanged |

- **Door (line-graph) formulation.**
  - Vertices are the intersections `X_u ∩ X_v`, plus `s` and `t`.
  - Edges join two vertices that lie in a common region, with length `‖x'−x‖` and no
    edge constraints. Theorem 1 therefore applies, but `κ` is finite only when the doors
    of each region are pairwise disjoint.
  - On the ring it is **exact** (29% → 0%): the only forks and merges are at the
    singletons `s` and `t`.
  - On the corridors it is no better. The rounding-certified mean gap is ≤ 5.6% and
    `REL_door` is 5.6% below `OPT_region`.
- **Inspection of a 4-box corridor (Exp 16).** The support contains fractional cycles
  through long, mutually overlapping doors. A door is entered near both of its ends and
  left from its middle, with matching means. This "teleportation" is invisible to
  separation parameters (`κ = ∞`).
- **Conclusion.** Topology (holes) is neither necessary nor sufficient for gaps.
  Separation explains exactness in the separated regime. The overlap regime needs a new
  quantity.

### 3.5 Complexity additions

**Proposition 6.**

- (a) **1D, norm lengths, any digraph: polynomial.** For a fixed path, the LP has an
  optimal solution at interval endpoints. Run Dijkstra on (vertex, breakpoint) pairs and
  shortcut walks with the triangle inequality. Exp 15: 60 cyclic instances, maximum
  difference from enumeration `4e−8`.
- (b) **`ℓ1` lengths with axis-aligned boxes in fixed dimension `d`: polynomial.** The
  coordinates separate for a fixed path, so the breakpoint grid has size `O(|V|^d)`.
  This is consistent with the `L1` orthogonal-touring results in 2605.07882.
- (c) **Euclidean lengths in 2D on layered acyclic graphs with segment sets: NP-hard.**
  In the polygon-touring hardness, each `P_i` is a pair of segments sharing an endpoint.
  This maps to a layer of two segment-vertices, with consecutive layers fully connected
  and a target box containing everything. With (a), the dimension threshold for
  Euclidean lengths is 1 versus 2.
- (d) **Variable dimension: no finite approximation ratio** for norm lengths on acyclic
  graphs with boxes (thesis Thm 9.1). Additive hardness is 1/2 on `[0,1]^n`: rounding
  shows that an unsatisfiable instance forces a total movement of at least 1/2.
- (e) **Squared Euclidean lengths, 1D intervals, cyclic: not approximable within
  `n^{1−ε}`** unless P=NP. Add a super-source and super-sink to the Hamiltonian-path
  GCS; a path with `K` edges costs exactly `1/K`. Then apply the Björklund–Husfeldt–
  Khanna longest-path hardness (recalled, see §1.6).

### 3.6 Attack plan for the rest of Q1

1. Write Theorem 1 with its corollaries, Props 2–3 and the separations. This is done in
   draft form here and needs a careful proof audit.
2. **Edge constraints (Q1b).** Pair points must satisfy the constraint pointwise, not
   just in mean.
   - For "matching" equalities (continuity at doors), try triple variables
     `(d,e,f)`, which put an edge hull on `K_e` intersected with the constraint set.
   - Alternatively, reduce to door-type formulations with vertex state
     `(position, derivatives)` and sublinear-in-difference costs.
   - Test on Bézier order 2–3 with time scaling.
3. **Overlap regime (Q1c).** Look for an a priori bound on the transport defect
   `Σ_v y_v W1(μ_v^in, μ_v^out)`.
   - Candidate parameter: the "teleport capacity" of a cover, i.e. how far the mean of a
     fractional cycle can shift inside a set.
   - Candidate cheap cuts that kill fractional cycles through a single set: lifted
     subtour cuts restricted to cycles inside one vertex's neighbourhood.
   - Test first on the corridor family (`exp9_corridor.py`).
4. **Q2 hardness.** Look for a gap-amplifying reduction in which unsatisfiable instances
   force `Ω(1)` angular deviation on a constant fraction of edges, e.g. via label cover
   with geometric gadgets.

**Difficulty and risk.**

- Step 1 is low risk; the main risk is lack of novelty (dynamic-programming extended
  formulations, perspective literature).
- Step 2 is medium risk.
- Step 3 is high risk: no mechanism is identified yet, and the corridor evidence shows
  gaps persist under the natural fixes.
- Step 4 is high risk and of theoretical interest only.

## 4. Significance

- **Proved in this pass.** These are first-pass proofs; they need an audit before being
  cited.
  - The first a priori integrality-gap bounds for GCS relaxations: Theorem 1 and
    Corollaries A–C. The multiplicative constant is `sec θ_max` for norm lengths and a
    Kantorovich factor for squared lengths.
  - A polynomial rounding algorithm matching the bound.
  - Exactness classes: affine lengths with the hull; 1D with disjoint intervals without
    it; sign-monotone `ℓ1`.
  - Strict separations: `REL` is first-order and `REL_H` second-order; the basic
    relaxation is inexact even for linear costs.
  - Infinite gap under overlap even in 1D.
  - Complexity items 6(a) and 6(b). Items (c)–(e) are corollaries of cited reductions.
- **Plausible benefits for solvers.**
  - A geometry-only certificate, computable before solving, telling when the relaxation
    plus rounding is provably within `x%`, so branch and bound can be skipped.
  - Principled placement of vertex-hull constraints: only at non-simplex vertices where
    both in- and out-flows split, which is detectable from `REL`'s solution by a small
    convex feasibility problem.
  - Guidance on formulation: door formulations remove region-level fork/merge loss (ring
    example).
  - A mechanism-level explanation, useful to modelers, of why squared-length and
    dense-graph instances are loose.
- **Speculative.**
  - An approximability threshold `1+Θ(θ²)`.
  - A theory of the overlap regime that explains motion-planning tightness. This is the
    most application-relevant part and the least understood. The experiments here show
    the practical formulations do have 2–16% gaps on simple corridors, so "empirical
    near-tightness" is itself regime-dependent.
- **Still needed for practical value.**
  - Extension to Bézier/time-scaling formulations with edge constraints.
  - Tests on real configuration-space covers from IRIS or clique covers in 7–14
    dimensions.
  - Measurement of the cost of hull constraints against the gap closed.

## 5. Recommendation

GCS is an active, application-driven MICP area with a clean open theoretical gap: there
is no a priori theory of when its perspective relaxation is tight. This scout produced a
correct-looking and fairly general first result. The gap of the vertex-hull relaxation
is bounded by Jensen defects of the edge lengths and attained by a line-graph rounding.
This yields `sec θ` bounds for separated sets, exactness classes, the Euclidean versus
squared explanation, and a first-order versus second-order separation between the basic
and hull relaxations. The scout also mapped where the theory stops. Overlapping covers,
which is the motion-planning regime, have gaps that neither topology, the vertex hull
nor a door reformulation removes. The easy half is feasible and probably publishable as
a solid note. Its MINLP depth is moderate, and its originality carries a real
rediscovery risk: dynamic-programming extended formulations and the perspective
literature, with the search budget exhausted before a full check. The hard half (edge
constraints, overlap regime, approximability threshold) is where solver impact would
come from, and it has no identified mechanism yet. **Score: 5/10**
(significance 5, feasibility 7 for the easy half and 3 for the hard half, originality
5).

## Reproduction (targeted commands actually run)

All commands were run in `research-20260928b/scouting/graphs-of-convex-sets/` with
cvxpy 1.9.3 and Clarabel; SCIP was used only for a mixed-integer check. No
project-wide checks were run.

| Command | Purpose |
|---|---|
| `python3 exp1_forkmerge.py` | 1D infinite gap |
| `python3 exp2_aperture.py 0` | random separated balls; bound never violated |
| `python3 exp3_crossing.py` | first- versus second-order separation |
| `python3 exp4_forkgadget.py` | sharpness ≈ 0.5 |
| `python3 exp5_1d.py` | 1D exactness; `REL = REL_H` |
| `python3 exp6_rounding.py` | chain `OPT ≤ E[round] ≤ Σκ ≤ κ_max·REL_H`, 0 violations |
| `python3 exp7_squared.py` | Kantorovich bound, 0 violations |
| `python3 exp8_mp.py` | ring and random unions |
| `python3 exp9_corridor.py 0 [two]` | corridor gaps |
| `python3 exp11_mp_hull.py` | region vertex hull |
| `python3 -u exp12_door.py` | door formulation; output in `exp12_door.out` |
| `python3 exp13_linear_simplex.py` | linear exactness with the hull; simplex `REL = REL_H` |
| `python3 exp14_linear_crossing.py` | linear-cost crossing: `REL = −4`, `REL_H = OPT = −2` |
| `python3 exp15_1d_dp.py` | 1D breakpoint dynamic program |
| `python3 exp16_inspect_door.py` | cycle teleportation in the door formulation |
