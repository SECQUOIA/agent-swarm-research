# Literature lane L4: Lagrangian and aggregation cuts, block decomposition, constraint aggregation, bound tightening from aggregated rows

Date: 2026-10-03. Lane focus: contribution C-AGG and novelty claim N3
(closure of original-variable aggregation cuts and its gap to the feasible
hull), with side findings for N4 (safe export after elimination) and N2.

## 1. Main findings

1. **The cut itself (Proposition "aggregated support cut") is classical.**
   It is weak Lagrangian duality (Boyd and Vandenberghe 2004, §5.1.3,
   p. 216, eq. (5.2)). In MINLP it appears as:
   - Nowak's *Lagrangian cut* for a block of an extended block-separable
     reformulation (Nowak 2004/2005, §7.1.3, eq. (7.9));
   - Tawarmalani and Sahinidis' Lagrangian cut on constraint values for
     range reduction (2004, Theorem 4.1);
   - Karuppiah and Grossmann's Lagrangean cuts (2008);
   - Domes and Neumaier's aggregated redundant constraint built from
     approximate multipliers (2016, §3.1).

   Our cut is the Nowak Lagrangian cut for the block
   {(x,y): x∈D, y≥g(x)}. The auxiliaries y are eliminated by one
   Fourier–Motzkin step against the source rows y ≤ b−Lz.

2. **The closure theorem (N3, first half) is anticipated in substance.**
   The values agree with the classical identity "Lagrangian dual =
   convexified problem":
   - Falk 1969; Magnanti–Shapiro–Wagner 1976; Geoffrion 1974 (linear and
     integer case);
   - Feltenmark–Kiwiel 2000, reproduced as Nowak's Lemma 3.5;
   - Lemaréchal–Renaud 2001, who convexify "in the product of the three
     spaces containing respectively the variables, the objective and the
     constraints". This is exactly our K = conv{(u,g(u))} with the
     variables kept.

   The *set-level* closure, proved by the same separation argument as
   ours, is Chen and Luedtke 2022, Theorem 3. Their proof includes the
   sign argument "v ≥ 0, since the min is −∞ if v < 0"; their setting is
   two-stage stochastic integer programs with polyhedral conv(K^s).

   What remains ours is narrow:
   - the specialization to compact continuous graphs with dualized
     *nonlinear* rows, affine remainders, and free equality multipliers;
   - the observation that the set statement needs no constraint
     qualification;
   - the identification of P as the projection of the lifted
     joint-graph relaxation.

   The paper must present the theorem as a recorded adaptation with
   these citations, not as a new result.

3. **The gap example x²=1/4 (N3, second half) is an instance of a known
   gap.** It is the standard Lagrangian duality gap: Geoffrion's conv(X)∩{Ax≤b}
   versus conv(X∩{Ax≤b}), and Nowak Lemma 3.3. More precisely, it is a
   **surrogate-versus-Lagrangian gap**: the surrogate dual is never
   weaker than the Lagrangian dual (Müller et al. 2022, p. 91, citing
   Greenberg–Pierskalla 1970 and Karwan–Rardin).

   The *aggregation closure* of Dey–Muñoz–Serrano 2022 and Dey–Han–Wang
   2026 closes this example with two aggregations. It convexifies each
   aggregated *set*, not the Lagrangian *function*. I checked this
   inline:
   - every sampled Lagrangian cut accepts x=1/4 (maximum violation 0);
   - for ν=+1, conv(S_ν)=[0,1/2]; for ν=−1, conv(S_ν)=[1/2,1];
   - the intersection is {1/2}.

   Nowak's and Decogo's convex hull relaxations would also close it,
   because they keep the row as a local block constraint. The example is
   a useful illustration but carries no novelty.

4. **"Avoiding auxiliary variables" is a representation choice with
   precedent.**
   - Nowak's extended reformulation (§2.5) introduces exactly the
     auxiliaries t ≥ h(x) that C-AGG eliminates.
   - Lemma 3.2 there shows that this lifting does not change the dual.
   - Zhu, He and Tawarmalani 2026 (p. 6) project out auxiliaries when
     the functions do not occur elsewhere.
   - Muts–Nowak–Hendrix 2020 and Wu et al. 2025 use copy constraints
     instead.

   The Decogo convex hull relaxation keeps the nonlinear rows and the
   variable bounds inside blocks. It can therefore be *strictly
   stronger* than P. The draft sentence "working in the original
   variables costs nothing" is true only relative to the lifted
   joint-graph relaxation with free auxiliaries and dualized rows. It
   should say so.

5. **Safe export after elimination (part of N4) is anticipated.** It is
   the bound-corrected rounding of:
   - Neumaier and Shcherbina 2004, §3, pp. 286–288. They also advise
     choosing cuts in floating point and then repeating the derivation
     rigorously (p. 294), and applying corrections to the raw data, not
     the presolved data (p. 289);
   - Cook et al. 2009;
   - Eifler and Gleixner 2024, Lemma 1 (p. 7) and Corollary 2 (p. 8).

   What I did not find in the lane sources is the whole contract
   combined: a whole-domain *nonlinear* support certificate, then exact
   elimination, then bound-corrected binary64 export, then replay
   against the source model.

6. **Bound tightening from aggregated rows is well established.**
   - LP rows: Tawarmalani–Sahinidis 2004 §4.4.1; Belotti 2013 (pairs of
     rows); Gleixner et al. 2017 (Lagrangian variable bounds).
   - Nonlinear rows: Domes–Neumaier 2016, with rigorous interval
     multipliers.
   - Certified, MIP: Borst et al. 2024.

   C-AGG with a=±e_j would give nonlinear Lagrangian variable bounds.
   The paper does not claim this, and should not without citing these
   works.

7. **The quadratic aggregation-hull literature studies a different
   object.** Yildiran 2009, Modaresi–Vielma 2017, Burer–Kılınç-Karzan
   2017, Dey–Muñoz–Serrano 2022, Blekherman–Dey–Sun 2024 and
   Dey–Han–Wang 2026 ask when intersections of (possibly nonconvex)
   aggregated *sets* give conv(S). It must be cited and distinguished.
   Our closure lies in the hierarchy
   conv(S) ⊆ aggregation closure ⊆ P, and both inclusions can be strict
   (strictness of the second shown by x²=1/4).

## 2. Scope and reading method

Local knowledge base (read only, `literature/papers/*/fulltext.md`).

**Read in full or in the cited passages:**
- Wu–Muts–Nowak–Hendrix 2025 (full);
- Muts–Nowak–Hendrix 2020 (§§1–3);
- Gleixner et al. 2017 (ZIB report, §§1–2);
- Tawarmalani–Sahinidis 2004 (preprint, §4);
- Müller et al. 2022 (§§1–2, definitions, theorem statements);
- Dey–Muñoz–Serrano 2022 (§§1–2 and theorem list);
- Blekherman–Dey–Sun 2024 (preprint abstract and introduction);
- Modaresi–Vielma 2017 (manuscript abstract, introduction, theorem
  list);
- Burer–Kılınç-Karzan 2017 (abstract, p. 2, Theorem 1);
- Chen–Luedtke 2022 (arXiv §§2–3);
- Neumaier–Shcherbina 2004 (§§3–4, 7);
- Eifler–Gleixner 2024 (arXiv §§2.2–2.3);
- Karuppiah–Grossmann 2006 (cut passage);
- Kerdreux et al. 2023 (§2.2);
- Udell–Boyd 2016 (pp. 1–4);
- Dey–Han–Wang 2026 (abstract, introduction, theorem statements);
- Füllner–Rebennack 2022 and Zhang–Sun 2022 (introductions);
- Zhu–He–Tawarmalani 2026 (p. 6);
- Puranik–Sahinidis 2017 (p. 8).

**Summaries only (KB):** Tawarmalani–Sahinidis 2005, Bao et al. 2009,
Li–Grossmann 2019, Allman–Zhang 2021, Borst et al. 2024.

**Online.** Full texts downloaded to a scratch directory, not added to the
KB:
- Nowak's HU Berlin habilitation (2004), which has the same title and
  content as the 2005 Birkhäuser book. Read: §§2.2.5, 2.5, 3.1–3.5,
  4.2 (part), 7.1, 7.3–7.4;
- Domes–Neumaier 2016 accepted manuscript (§§1–3.2);
- Boyd–Vandenberghe author PDF (§§5.1–5.3).

Abstracts or metadata only: Lemaréchal–Renaud 2001, Feltenmark–Kiwiel
2000, Geoffrion 1974, Falk 1969, Magnanti–Shapiro–Wagner 1976,
Karuppiah–Grossmann 2008, Misener–Floudas 2012, Kronqvist–Lundell–Westerlund
2018, Belotti 2013, Yildiran 2009, Balas 2005, Dey–Meunier–Morán 2025,
Muts–Nowak–Hendrix 2021, Nowak et al. 2018. All DOIs were checked
through Crossref.

Page locators are given only where I read the passage. Nowak locators
refer to the habilitation PDF pagination, which may differ from the
book. Recheck them against the book before printing page numbers.

## 3. Detailed findings by topic

### 3.1 The cut principle: weak duality and Lagrangian cuts

**Boyd and Vandenberghe 2004** (full text of §§5.1–5.3 read).
- §5.1.3, p. 216, eq. (5.2): g(λ,ν) ≤ p* for every λ ⪰ 0 and every ν,
  with no convexity assumption.
- §5.2.2, p. 225, eq. (5.23): weak duality "holds even if the original
  problem is not convex".
- §5.3.1, p. 232, eqs. (5.36)–(5.37): the value set
  G = {(f₁(x),…,h(x),f₀(x)) : x∈D} and the set
  A = G + (R^m_+ × {0} × R_+). The dual function is a nonvertical
  support of G or A (p. 234, eq. (5.38)).

*Relation:* our U = K + ({0}×R^m_+) is the convex hull of BV's A,
augmented with the variable coordinates x. Proposition "aggregate" is
(5.2) applied to the objective a^T x − λ^T ℓ(v). Fully anticipated as a
principle; Report B already says so.

**Nowak 2004/2005**, *Relaxation and Decomposition Methods for MINLP*
(habilitation text read).
- §2.2.5 (p. 16): block-separability.
- §2.5 (p. 22): the "extended block-separable reformulation". Each
  constraint Σ_k h_{i,k}(x_{J_k}) ≤ 0 is rewritten as Σ_k t_{i,k} ≤ 0
  with h_{i,k}(x_{J_k}) − t_{i,k} ≤ 0. The auxiliaries t_{i,k} get
  bounds from convex underestimators. All nonlinear constraints become
  local to blocks; the coupling is linear.
- §3.3 (p. 29): Lagrangian relaxation of min f s.t. g ≤ 0, x∈G, and
  weak duality (Observation 3.3).
- §3.4: dual-equivalent convex relaxations.
  - Lemma 3.2 (p. 30): the dual of the original and of the extended
    reformulation coincide.
  - Lemma 3.3 (p. 31): under a constraint qualification, the dual of the
    extended reformulation equals min{c^T x : x ∈ conv(G), Ax+b ≤ 0},
    where G contains the local nonlinear constraints. A nonzero gap
    means the Lagrangian solution is infeasible.
  - Lemma 3.4 (p. 32): dual relaxations are at least as strong as
    convex-underestimating relaxations (envelope of each function
    separately).
  - Problem (3.14) and Lemma 3.5 (pp. 32–33), credited to Feltenmark and
    Kiwiel 2000: the dual equals the convex program over n+1 convex
    combinations of (f(w_j), g(w_j)) with Σ z_j g(w_j) ≤ 0. This is
    exactly "impose the constraints on the averaged graph coordinates",
    the mechanism of our x²=1/4 example.
- §3.5 (p. 34): Lemma 3.6 (adding valid cuts can only reduce the
  duality gap) and Remark 3.2.
- §7.1.3 (p. 93): Lagrangian cut a_k(μ)^T x_{J_k} ≥ D_k(μ) =
  min_{x∈G_k} L_k(x;μ).
- §7.1.4 (p. 93): "deeper cuts" from super-blocks.
- Observation 7.3 (p. 97): LP bounds with Lagrangian cuts recover the
  dual bound.
- §7.4 (p. 98): box reduction from these relaxations.

*Relation:* the C-AGG cut is Nowak's Lagrangian cut for the block
{(x,t): x∈D, g(x) ≤ t} with t eliminated through the coupling rows.
Nowak's closure statement is value-level and needs a constraint
qualification. Our Theorem is the set-level form for the block with
free auxiliaries. Nowak's G_k keeps local nonlinear constraints and
t-bounds, so his convex hull relaxation can be strictly tighter than P.
**Anticipates the C-AGG principle fully and the N3 closure in
substance.**

**Tawarmalani and Sahinidis 2004** (preprint, §4 read).
- §4.1 (pp. 15–17): a homogenized Lagrangian subproblem
  inf_x {y₀f(x) + y·g(x)} over the "easy" set X, and a range-reduction
  master in the space of perturbations (u₀,u). Algorithm SimpleReduce
  reduces to the Lagrangian lower bound for (a₀,a) = (1,0).
- Theorem 4.1 (p. 18): for a dual vector y ≤ 0 with y_i ≠ 0, the cut
  g_i(x) ≥ (b₀ − inf_x l(x,y))/y_i does not cut off any optimal
  solution. Marginals-based range reduction, Ryoo–Sahinidis Theorems 2–3
  and Zamora–Grossmann's contraction are derived as corollaries
  (pp. 18–19).
- §4.3.2 (p. 19): feasibility-based range reduction is "a rather simple
  application of Fourier–Motzkin elimination".
- §4.4.1 (pp. 20–21): FBBT on *surrogate constraints* ΠAx ≤ Πb, with
  stored dual-feasible multipliers.

*Relation:* direct precedent for Lagrangian-dual valid inequalities on
nonlinear constraint functions, for row aggregation in bound tightening,
and for the Fourier–Motzkin view. Its cuts are optimality-based (they
use an incumbent bound b₀); ours are feasibility cuts. Partial
anticipation of C-AGG; cite.

**Karuppiah and Grossmann 2008** (abstract only). Lagrangean
decomposition of decomposable nonconvex MINLPs. Cuts derived from the
global optima of the decomposed subproblems are added to the convex
relaxation. Same principle (support of a block, with multipliers) in
nonconvex MINLP. Cite as a Lagrangian-cut precedent in nonconvex MINLP.

**Karuppiah and Grossmann 2006** (KB PDF p. 8, the passage on
"Non-redundant bound strengthening cuts"; the equation did not extract).
Overall contaminant balances, which are linear, are added as "deep
cuts" because the relaxation of the bilinear mixer balances violates
the overall balance. This is the special case of aggregation in which
the nonlinear parts cancel and the support is exact. An optional
illustration.

**Domes and Neumaier 2016** (accepted manuscript read, §§1–3.2).
- Example 1 (pp. 3–4): aggregating the objective cutoff and the
  constraints with KKT multipliers ν=1, y=(−0.5,0) gives
  0.5(x₁+x₂)² ≤ 0. This new constraint lets propagation contract the box
  to the optimum.
- §3.1 (pp. 13–14): the aggregator y ≠ 0 defines the aggregated
  constraint u^T F(x) ∈ y^T b, with u ∈ B^T y as interval coefficients,
  eqs. (31)–(34). Interval coefficients make the approximate multipliers
  rigorous. The aggregated constraint is then filtered.
- §3.2: a "singly-quadratic" constraint-satisfaction problem (one
  quadratic plus linear constraints) handled by a directed Cholesky
  factorization.

*Relation:* the closest precedent for *rigorous aggregation of original
nonlinear rows with numerically computed multipliers*. It differs from
C-AGG in two ways: it keeps the aggregated constraint nonlinear and
uses it for bound reduction, not for certified linear support cuts; and
it has no whole-domain support certificate or binary64 export contract.
Partial anticipation of C-AGG and N4; **must cite.**

### 3.2 Closure: Lagrangian dual = convexified problem; set version

**Lemaréchal and Renaud 2001** (abstract only). Formulate a convex
problem with the same dual as a nonconvex one, by "a convexification in
the product of the three spaces containing respectively the variables,
the objective and the constraints". Applied to Lagrangean decomposition
and operator splitting.

Kerdreux et al. 2023 (KB, read) quote this paper's Theorem 2.11 as their
Theorem 2.3 (p. 4): the dual function of (P) equals that of the
convexified problem; strong duality holds under a relative-interior
condition.

*Relation:* value-level version of our closure theorem, *including* the
variable coordinates. **Anticipates N3 (closure) in substance.**

**Feltenmark and Kiwiel 2000** (not accessed; content via Nowak's
Lemma 3.5 and problem (3.14)). Dual-equivalent convex relaxation
through n+1 convex combinations of graph points.

**Geoffrion 1974** (not accessed; standard result, also discussed by
Dey–Meunier–Morán 2025). For X finite or the integer points of a
rational polyhedron, the Lagrangian bound equals
min{cx : Ax ≤ b, x ∈ conv X}. Dey–Meunier–Morán (arXiv:2510.10966,
abstract and statement summary only) show that the equality can fail
without finiteness or rationality, through non-closed conv X, and give
sufficient conditions. For our theorem this supports keeping the
compactness and continuity assumptions explicit: closedness of U is
what makes the set equality hold.

**Falk 1969; Magnanti, Shapiro and Wagner 1976; Aubin and Ekeland 1976**
(metadata only). Classical sources for "dual = convexified (separable)
problem" and for duality-gap estimates. Udell–Boyd 2016 (p. 4) state
that the convexified separable problem is the dual of the Lagrangian
dual. Kerdreux et al. 2023 and Dey–Xu 2026 bound the gap with the
Shapley–Folkman lemma. These are optional context for "how large can
the closure–hull gap be".

**Chen and Luedtke 2022** (arXiv version read, §§2–3, pp. 4–7).
- Proposition 2 (p. 6): any normalization neighborhood of the cut
  coefficients gives the same Lagrangian-cut closure.
- Theorem 3 (pp. 6–7): z_LC = z_D. The proof shows that
  U^s = proj{(x,y,θ): θ ≥ q^T y, (x,y) ∈ conv(K^s)} equals the set cut
  out by all Lagrangian cuts. It uses strict separation, with
  "v ≥ 0 … since the min is −∞ if v < 0".
- Theorem 1 (p. 5) is Carøe–Schultz.

*Relation:* the same theorem *and proof* as our closure theorem, in the
polyhedral setting of two-stage stochastic integer programs. Our version
replaces conv(K^s) with the compact convex hull of a continuous graph
and adds a cone for inequality rows. **Strongest set-level anticipation
of N3; must cite.**

**Wu, Muts, Nowak and Hendrix 2025** (full text read). "Overlapping
convex hull relaxation" (CHR): replace each local nonlinear block set
X_k by conv(X_k) (§2.2, p. 418); X_k contains the nonlinear constraints
and small-support linear rows. Proposition 1 (p. 419): adding an
aggregated block B_k = B_ℓ ∪ B_s that contains a coupling row (for
example a copy constraint) never increases the gap, and strictly
reduces it if the CHR solution is unique and lies outside conv(X_k).

Other parts:
- §3.2 (pp. 420–421) illustrates this with copy constraints;
- §4.1 (p. 422) gives the resource-constrained reformulation;
- §4.3 (p. 423) column generation: pricing problems are MINLPs over X_k
  with direction (1,μ);
- DESSlib results: gaps reduced but nonzero (Tables 2–3, p. 431).

*Relation:* (i) P is a CHR for the block {(x,y): x∈D, y≥g(x)} with
dualized rows. Decogo's CHR keeps rows in blocks and is never weaker.
(ii) Wu et al. Proposition 1 is the qualitative statement that block
hulls glued by copy constraints are weaker than the hull of the merged
block. This is the same phenomenon as N2, but without an explicit
witness or quantification (the N2 lane should note this). (iii) The
draft's "two rows sharing one variable" example is the same phenomenon.

**Muts, Nowak and Hendrix 2020 (DECOA)** (§§1–3 read). Convex
block-separable MINLP, with local nonlinear constraints and global
linear coupling (§2, pp. 77–78). States (p. 78) that a general sparse
MINLP can be made block-separable "by adding new variables and
copy-constraints". Its supporting hyperplanes come from projection and
line-search subproblems. Relevant to the "auxiliary or copy variable
versus original variable" distinction. DECOA itself is for convex
MINLP. Low anticipation.

**Further Decogo and decomposition works** (abstracts only):
- Nowak, Breitfeld, Hendrix and Njacheun-Njanzoua 2018:
  decomposition-based inner and outer refinement;
- Muts, Nowak and Hendrix 2021: multiobjective-based column and
  disjunctive cut generation in the resource-constrained reformulation;
- Nowak and Vigerske 2008: LaGO;
- Allman and Zhang 2021 (KB summary): branch-and-price for nonconvex
  MINLP with linear complicating constraints.

Cite one or two as context for block convex-hull relaxations computed
by column generation.

### 3.3 Gap to the feasible hull; surrogate and aggregation closures

**Müller, Muñoz, Gasse, Gleixner, Lodi and Serrano 2022**
(read §§1–2 and statements).
- Definition 1 (p. 90): surrogate relaxation min{c^T x : x∈X,
  λ^T g(x) ≤ λ^T b}.
- Definition 2 (p. 91): surrogate dual. It "always results in a bound
  that is at least as good" as the Lagrangian dual (citing
  Greenberg–Pierskalla 1970 and Karwan–Rardin).
- §2 (p. 93): history (Glover 1968; Greenberg–Pierskalla 1970;
  Glover 1975).
- §§4–5: the K-surrogate dual with several simultaneous aggregations,
  Theorem 2 (p. 98ff.).

*Relation:* surrogate relaxations aggregate the *original nonlinear
rows* and keep the aggregate as a constraint. C-AGG instead takes the
linear support of the Lagrangian of the aggregate. The x²=1/4 gap is
exactly a surrogate-versus-Lagrangian gap. **Must cite** next to the
gap example.

**Dey, Muñoz and Serrano 2022** (§§1–2 read). Aggregation hull results
for quadratic constraints:
- the closed convex hull is the best aggregations can give (p. 660);
- Theorem 2.4 (pp. 662–663): three strict quadratics under PDLC and a
  nontrivial-hull condition give conv(S) as an intersection of
  aggregations;
- Proposition 2.5 (p. 665): this fails for four quadratics;
- Proposition 2.6 (p. 666): it fails without PDLC;
- Theorem 2.7 (p. 667): the closed case, which cannot be applied to sets
  with empty interior, such as those with equalities (p. 668).

They define S_λ as the aggregated set, not its convexification.

**Blekherman, Dey and Sun 2024** (preprint abstract and introduction).
Hidden hyperplane convexity is sufficient for "special aggregations" to
describe the convex hull. With PDLC, finitely many aggregations suffice;
six aggregations suffice for three quadratics. There is also a
closed-inequality result without topological assumptions.

**Yildiran 2009** (via DMS and Modaresi–Vielma). Two strict quadratics:
the hull is the intersection of two aggregations, with an LMI
representation.

**Modaresi and Vielma 2017** (manuscript abstract and theorem list).
Theorem 2, which is Yildiran's Theorem 1, gives conv(S) for two strict
quadratic sets. Extensions cover a conic quadratic plus a quadratic, and
the closed case under topological assumptions.

**Burer and Kılınç-Karzan 2017** (abstract, p. 2, Theorem 1).
Aggregation with nonnegative weights for an SOC intersected with a
nonconvex quadratic. The aggregated function only needs to be convex on
the cone; Theorem 1 gives the hull under Conditions 1–5.

**Dey, Han and Wang 2026** (KB; abstract, introduction, Theorems 1–3
read). Aggregation closure ∩_λ conv(S_λ) for two bounded bilinear
bipartite *equalities*:
- Theorem 1: three aggregations suffice when n₁=n₂=1;
- Theorem 2: infinitely many aggregations can be needed;
- Theorem 3: the aggregation closure can differ from conv(S).

*Relation for the aggregation-hull literature:* these papers study
∩_λ conv(S_λ), the convex hull of each aggregated *set*. For fixed λ,
C-AGG cuts describe conv(S_λ) only when the affine remainder λ^T L z
ranges over all of R. When the row has no free remainder, as in
x²=1/4, C-AGG gives the weaker level set {x : (λ^T g)**(x) ≤ λ^T b}.
Hence the hierarchy

  conv(S) ⊆ ∩_λ conv(S_λ) ⊆ P.

The second inclusion is strict for x²=1/4, and the first is strict by
DHW Theorem 3 and DMS Propositions 2.5–2.6. None of these papers
anticipates the C-AGG cut family or its closure, but a referee will
expect the hierarchy to be stated. **Must cite DMS, BDS and Yildiran or
Modaresi–Vielma; DHW 2026 is recommended because it treats equalities
and convexifies aggregations.**

### 3.4 Grouping terms, separability, and lifting versus projection

**Misener and Floudas 2012** (abstract). Facets of low-dimensional
(n ≤ 3) *edge-concave aggregations*, which dominate the termwise
relaxation, are added at every node. Also **ANTIGONE**, Misener and
Floudas 2014 (metadata only). Grouping of *terms within* quadratic rows
rather than nonnegative aggregation of *rows*. Cite and distinguish.

**Bao, Sahinidis and Tawarmalani 2009** (KB summary). Multiterm
envelopes of the bilinear part of one quadratic row over a box;
Theorem 2.4 characterizes facets through vertex LPs. Precedent for
joint convexification of several terms of a *single* row. C-AGG does
the analog across rows through λ.

**Tawarmalani and Sahinidis 2005** (KB summary and theorem statements).
Lifting each term of a composition separately gives tighter polyhedral
outer approximations (Theorem 1, Propositions 3–5). Precedent for the
trade-off between lifting and projection.

**Kronqvist, Lundell and Westerlund 2018** (abstract). Lifted polyhedral
approximations of "almost additively separable" convex functions,
obtained by reformulation with auxiliary variables, are provably
tighter. A contrast for C-AGG: there, lifting helps polyhedral outer
approximation of convex functions. In C-AGG the exact support of the
aggregate is already as strong as the lifted joint graph, so no lifting
is needed for strength. Cite briefly.

**Zhu, He and Tawarmalani 2026** (arXiv, p. 6 read). In their
Proposition 2 setting, "when the functions f_i(·) do not appear
elsewhere … the auxiliary variables t_i can be projected out". Precedent
for avoiding auxiliaries by projection; Report B already cites this
paper.

**Mitsos, Chachuat and Barton 2009** (KB, not reread). McCormick
relaxations in the original variable space without auxiliaries. This
optional citation belongs to another lane. It is relevant if the paper
discusses "original variables versus auxiliary variable method".

### 3.5 Bound tightening from aggregated rows

**Gleixner, Berthold, Müller and Weltge 2017** (ZIB Report 15-16,
§§1–2 read).
- Theorem 1 (report p. 5): aggregating LP rows with optimal OBBT duals
  plus the cutoff gives a valid "Lagrangian variable bound"
  x_k ≥ r̃^T x + λ̃^T b + μ̃U, tight at x̃.
- Validity "also follows from a special instantiation of the (PU-PR)
  range reduction framework" of Tawarmalani–Sahinidis 2004.
- Remark 3 (report p. 7): LVBs are redundant for the LP and are used
  for propagation.
- Gleixner and Weltge 2013 (CPAIOR) is the earlier version.

Report B's characterization is correct.

**Belotti 2013** (abstract, plus the Puranik–Sahinidis survey p. 8).
Bound reduction from convex combinations of *pairs* of LP rows, with an
O(m²n²) procedure in Couenne and in SCIP's tworowbnd presolver.

**Puranik and Sahinidis 2017** (arXiv p. 8 read). Survey placing
Belotti 2013 and Domes–Neumaier 2016 as multi-constraint (aggregation)
reductions.

**Borst, Eifler and Gleixner 2024** (KB summary). Certified constraint
propagation and dual proof analysis in exact MIP: safe aggregation of
dual rows with directed rounding, and VIPR certificates. This is the
certified-aggregation analog in MIP.

**Nowak 2004/2005 §7.4** (p. 98) and **Caprara and Locatelli 2010**
(KB summary). Box reduction from relaxations and its fixed-point
properties. Optional.

*Relation:* if the paper mentions using C-AGG directions a=±e_j for
bound tightening, it should cite TS2004, Gleixner et al. 2017, Belotti
2013 and Domes–Neumaier 2016. Otherwise one sentence suffices.

### 3.6 Lagrangian and value-function cuts in decomposition

- **Carøe and Schultz 1999** (via Chen–Luedtke Theorem 1).
- **Rahmaniani et al. 2020.**
- **Zou, Ahmed and Sun 2019.** Füllner–Rebennack (p. 3) summarize that
  SDDiP Lagrangian cuts "reproduce the lower convex envelope of the
  value function".
- **Füllner and Rebennack 2022** (introduction): Lagrangian cuts inside
  nonconvex nested Benders.
- **Zhang and Sun 2022** (introduction, p. 3): generalized conjugacy
  cuts for multistage stochastic MINLP.
- **Li and Grossmann 2019** (KB summary): Lagrangian cuts from
  nonanticipativity in nonconvex two-stage MINLP.

*Relation:* the closure "Lagrangian cuts give the convex envelope or
convex hull" is folklore in decomposition. It confirms that N3's
closure statement is not new. Cite Chen–Luedtke, and optionally
Zou–Ahmed–Sun, for the set version.

### 3.7 Safe export after elimination (N4, C-AGG part)

**Neumaier and Shcherbina 2004** (§§3–4 and 7 read).
- §3, pp. 286–288: a rigorous lower bound from an approximate dual
  multiplier λ. The residual r = A^T λ − c is enclosed by directed
  rounding and bounded with variable bounds; finite bounds are needed.
- p. 289: rigorous corrections must be applied to the raw LP, not to a
  presolved version with rounded substitutions.
- p. 294: "decide upon the cuts … using ordinary floating-point
  arithmetic, and then … repeat the arguments … with rigorous rounding
  error control. … the bounds are valid for the s actually used,
  independent of its construction."

This is the direct ancestor of Proposition "Safe export", of the
"numerical direction, a-posteriori certificate" pattern of C-SUP and N4,
and of the replay-against-the-source-model principle of N6.
**Must cite.**

**Eifler and Gleixner 2024** (arXiv §§2.2–2.3 read).
- Lemma 1 (p. 7): a rational row is relaxed to an F-representable row
  by transforming to nonnegative variable space, rounding, and
  correcting with the bounds, "the essential technique from [11]",
  that is, Cook et al. 2009 (p. 8).
- Corollary 2 (p. 8): safe aggregation with approximate multipliers.

**Cook, Dash, Fukasawa and Goycoolea 2009** (metadata). Numerically safe
Gomory mixed-integer cuts.

*Relation:* Proposition "Safe export" is the ≥-form of these
corrections with one-sided bound requirements. Anticipated; Report B
already attributes it.

### 3.8 Projection and Fourier–Motzkin views

The C-AGG cut is the projection of the lifted support cut
a^T x + λ^T y ≥ β onto (x,z), using λ ≥ 0 times the rows y + Lz ≤ b. For
a fixed λ this is one Fourier–Motzkin step. The closure theorem is a
projection theorem: in the polyhedral case the multipliers λ range over
Balas's projection cone. In our compact convex case, support functions
replace the projection cone.

Sources: **Balas 2005** (metadata, survey of projection and the
projection cone); TS2004 p. 19 (FBBT as Fourier–Motzkin); BV §5.3
(supporting hyperplanes of the value set). Cite Balas 2005 if the paper
uses the word "projection" for Theorem "closure".

### 3.9 Not relevant or not found

- Kallrath: nothing relevant to aggregation or closure.
- Rebennack: relevant only through Füllner–Rebennack 2022 (Lagrangian
  cuts).
- Davarnia, Kiaghadi and Qiu 2024 (arXiv:2409.19794, abstract only):
  decision-diagram convexification of MINLP constraints with cutting
  planes. From the abstract, it is unclear whether it convexifies
  several rows jointly; low priority.
- Bodur, Del Pia, Dey, Molinaro and Pokutta 2018: aggregation closure
  for packing and covering integer programs. A MILP analog, optional.
- No source found that states the *complete contract* of C-AGG: certified
  nonlinear support over D, exact elimination into the original
  variables, bound-corrected binary64 export, and replay of the stored
  SCIP row.

## 4. Novelty assessment for the lane

| Claim | Verdict | Evidence |
| --- | --- | --- |
| C-AGG cut principle (aggregated support cut in original variables) | Anticipated (principle) | BV §5.1.3; Nowak §7.1.3 Lagrangian cuts with §2.5 auxiliaries; TS2004 Thm 4.1; Domes–Neumaier 2016 §3.1; Karuppiah–Grossmann 2008 |
| N3a: closure of all aggregate cuts = projected joint-graph relaxation | Anticipated in substance; set form follows routinely | Value form: Lemaréchal–Renaud 2001 (Th. 2.11 via Kerdreux et al. 2023 Thm 2.3); Feltenmark–Kiwiel 2000 / Nowak Lemma 3.5; Nowak Lemma 3.3; Geoffrion 1974 (linear/integer). Set form with identical proof: Chen–Luedtke 2022 Thm 3. Remaining: compact nonlinear graph with dualized nonlinear rows, affine remainders, free equality multipliers; no constraint qualification needed for the set statement. |
| N3b: x²=1/4 shows the closure is strictly weaker than the feasible hull | Known phenomenon; example elementary | Lagrangian duality gap (Geoffrion; Nowak Lemma 3.3); surrogate ≥ Lagrangian (Müller et al. 2022 p. 91; Greenberg–Pierskalla 1970). Aggregation closure (DMS 2022; DHW 2026) and Decogo-type CHR (Wu et al. 2025) close this instance (checked: conv S_{+1}=[0,1/2], conv S_{−1}=[1/2,1]). |
| "Avoids auxiliary variables at no loss" | True only relative to the lifted joint graph with free auxiliaries and dualized rows | Nowak Lemma 3.2 (lifting does not change the dual); Zhu–He–Tawarmalani 2026 p. 6 (project out auxiliaries); block CHR keeping rows and bounds (Nowak Lemma 3.3; Wu et al. 2025) can be strictly stronger. |
| N4 (lane part): safe binary64 export after elimination; numerical choice then rigorous certificate | Partially anticipated | Neumaier–Shcherbina 2004 §3 and p. 294; Cook et al. 2009; Eifler–Gleixner 2024 Lemma 1, Cor. 2; Borst et al. 2024. The combination with whole-domain nonlinear support certificates and replay of the stored row was not found. |
| N2 (side finding): pair hulls glued on shared moments are not the joint hull | Qualitatively anticipated; quantification not found | Wu et al. 2025 Prop. 1 and §3.2 (aggregated blocks strictly tighten the glued CHR); Nowak §7.1.4 (super-block cuts). Neither gives an explicit witness, a 1/128 gap, or a δ²/2 family. Pass to the N2 lane. |
| N1, N5, N6 | Outside lane; no anticipating source found here | Neumaier–Shcherbina p. 289 (apply corrections to raw rather than presolved data) is a precursor in spirit of N6's source-faithfulness, not of its exact domain witnesses. |

## 5. Suggested changes to `sections/04-original-variables.tex`

These are suggestions for the section owner; I did not edit the file.

1. After Proposition `prop:aggregate`, cite the cut as weak duality (BV)
   *and* as a Lagrangian cut for the extended block reformulation
   (Nowak 2005 §§2.5 and 7.1.3), with the auxiliaries eliminated by the
   source rows. Also cite TS2004 Thm 4.1 and Domes–Neumaier 2016 for
   aggregating nonlinear rows with multipliers.
2. Before Theorem `thm:closure`, add a sentence of this kind: "This is
   the set version of the classical fact that the Lagrangian dual of a
   nonconvex program equals the dual of its convexification in the
   product of the variable, objective and constraint spaces
   [Lemaréchal–Renaud 2001; Feltenmark–Kiwiel 2000; Nowak 2005]. The
   separation argument below is the one Chen and Luedtke [2022, Thm 3]
   use for Lagrangian cuts; we record it because our functions are
   nonlinear, the dualized rows carry affine remainders, and no
   constraint qualification is needed for the set statement."
3. Qualify "costs nothing relative to the lifted joint-graph
   relaxation". Convex hull relaxations that keep nonlinear rows and
   remainder bounds inside the block (Nowak 2005 Lemma 3.3; Wu et al.
   2025) can be strictly stronger. Example `ex:quarter` is such a case.
4. In Example `ex:quarter`, name the phenomenon: a Lagrangian duality
   gap, equivalently a surrogate-versus-Lagrangian gap (Müller et al.
   2022). Note that the aggregation closure ∩_λ conv(S_λ) (Dey–Muñoz–Serrano
   2022; Dey–Han–Wang 2026) equals {1/2} here, using two aggregations.
   State the hierarchy conv(S) ⊆ ∩_λ conv(S_λ) ⊆ P.
5. Example `ex:two-rows` (joint versus separate one-row envelopes): cite
   Nowak Lemma 3.4 (dual relaxations dominate separate convex
   underestimators) and Bao et al. 2009 or Misener–Floudas 2012 for term
   grouping within rows.
6. In §`sec:export`, add Neumaier–Shcherbina 2004 (§3; p. 294 for "choose
   numerically, certify rigorously") ahead of Cook et al. 2009 and
   Eifler–Gleixner 2024.

## 6. Must-cite list for C-AGG and N3

- BoydVandenberghe2004 (already in Report B bib)
- Nowak2005 (book; locators from the habilitation text)
- LemarechalRenaud2001
- ChenLuedtke2022
- Geoffrion1974
- TawarmalaniSahinidis2004
- GleixnerEtAl2017 (already in bib)
- DomesNeumaier2016
- MullerEtAl2022Surrogate
- DeyMunozSerrano2022 and BlekhermanDeySun2024 (already in bib)
- Yildiran2009 or ModaresiVielma2017
- WuMutsNowakHendrix2025 (Decogo convex hull relaxation)
- NeumaierShcherbina2004
- EiflerGleixner2024 and CookEtAl2009SafeCuts (already in bib)
- MisenerFloudas2012 (already in bib)

Recommended:
- FeltenmarkKiwiel2000, KaruppiahGrossmann2008, DeyHanWang2026,
  MutsNowakHendrix2020, KronqvistLundellWesterlund2018,
  BaoSahinidisTawarmalani2009, Belotti2013, GreenbergPierskalla1970.

Optional:
- Falk1969, MagnantiShapiroWagner1976, AubinEkeland1976, UdellBoyd2016,
  KerdreuxEtAl2023, DeyMeunierMoran2025, Balas2005, BurerKilincKarzan2017,
  TawarmalaniSahinidis2005, ZhuHeTawarmalani2026 (already in bib),
  ZouAhmedSun2019, CaroeSchultz1999, RahmanianiEtAl2020,
  FullnerRebennack2022, ZhangSun2022, LiGrossmann2019, AllmanZhang2021,
  NowakVigerske2008, MutsNowakHendrix2021, NowakEtAl2018,
  GleixnerWeltge2013, BorstEiflerGleixner2024, PuranikSahinidis2017,
  KaruppiahGrossmann2006, Glover1968, MisenerFloudas2014,
  BodurEtAl2018.

## 7. Full citations (BibTeX-ready)

DOIs were checked against Crossref on 2026-10-03 unless marked. Entries
already in `research-20261003-convexification/literature/references.bib`
are marked [in bib].

```bibtex
@book{Nowak2005,
  author = {Ivo Nowak},
  title = {Relaxation and Decomposition Methods for Mixed Integer Nonlinear Programming},
  series = {International Series of Numerical Mathematics},
  volume = {152},
  publisher = {Birkh{\"a}user},
  address = {Basel},
  year = {2005},
  doi = {10.1007/3-7643-7374-1},
  isbn = {978-3-7643-7238-5},
  note = {Content read in the author's Habilitationsschrift of the same title, Humboldt-Universit{\"a}t zu Berlin, 2004, https://edoc.hu-berlin.de/bitstreams/5c143f18-f9de-4d5b-82b6-7c99aac8010c/download; locators refer to that text}
}

@article{LemarechalRenaud2001,
  author = {Claude Lemar{\'e}chal and Arnaud Renaud},
  title = {A geometric study of duality gaps, with applications},
  journal = {Mathematical Programming},
  volume = {90},
  number = {3},
  pages = {399--427},
  year = {2001},
  doi = {10.1007/PL00011429}
}

@article{FeltenmarkKiwiel2000,
  author = {Stefan Feltenmark and Krzysztof C. Kiwiel},
  title = {Dual Applications of Proximal Bundle Methods, Including {L}agrangian Relaxation of Nonconvex Problems},
  journal = {SIAM Journal on Optimization},
  volume = {10},
  number = {3},
  pages = {697--721},
  year = {2000},
  doi = {10.1137/S1052623498332336}
}

@incollection{Geoffrion1974,
  author = {Arthur M. Geoffrion},
  title = {Lagrangean relaxation for integer programming},
  booktitle = {Approaches to Integer Programming},
  series = {Mathematical Programming Studies},
  volume = {2},
  pages = {82--114},
  year = {1974},
  doi = {10.1007/BFb0120690}
}

@article{Falk1969,
  author = {James E. Falk},
  title = {Lagrange Multipliers and Nonconvex Programs},
  journal = {SIAM Journal on Control},
  volume = {7},
  number = {4},
  pages = {534--545},
  year = {1969},
  doi = {10.1137/0307039}
}

@article{MagnantiShapiroWagner1976,
  author = {Thomas L. Magnanti and Jeremy F. Shapiro and Michael H. Wagner},
  title = {Generalized Linear Programming Solves the Dual},
  journal = {Management Science},
  volume = {22},
  number = {11},
  pages = {1195--1203},
  year = {1976},
  doi = {10.1287/mnsc.22.11.1195}
}

@article{AubinEkeland1976,
  author = {Jean-Pierre Aubin and Ivar Ekeland},
  title = {Estimates of the Duality Gap in Nonconvex Optimization},
  journal = {Mathematics of Operations Research},
  volume = {1},
  number = {3},
  pages = {225--245},
  year = {1976},
  doi = {10.1287/moor.1.3.225}
}

@article{ChenLuedtke2022,
  author = {Rui Chen and James Luedtke},
  title = {On Generating {L}agrangian Cuts for Two-Stage Stochastic Integer Programs},
  journal = {INFORMS Journal on Computing},
  volume = {34},
  number = {4},
  pages = {2332--2349},
  year = {2022},
  doi = {10.1287/ijoc.2022.1185},
  eprint = {2106.04023},
  archivePrefix = {arXiv},
  note = {Theorem/page locators refer to the arXiv version}
}

@article{TawarmalaniSahinidis2004,
  author = {Mohit Tawarmalani and Nikolaos V. Sahinidis},
  title = {Global optimization of mixed-integer nonlinear programs: A theoretical and computational study},
  journal = {Mathematical Programming},
  volume = {99},
  number = {3},
  pages = {563--591},
  year = {2004},
  doi = {10.1007/s10107-003-0467-6},
  note = {Page locators refer to the 35-page preprint, https://arnold-neumaier.at/glopt/mss/TawS03.pdf}
}

@article{TawarmalaniSahinidis2005,
  author = {Mohit Tawarmalani and Nikolaos V. Sahinidis},
  title = {A polyhedral branch-and-cut approach to global optimization},
  journal = {Mathematical Programming},
  volume = {103},
  number = {2},
  pages = {225--249},
  year = {2005},
  doi = {10.1007/s10107-005-0581-8}
}

@article{DomesNeumaier2016,
  author = {Ferenc Domes and Arnold Neumaier},
  title = {Constraint aggregation for rigorous global optimization},
  journal = {Mathematical Programming},
  volume = {155},
  pages = {375--401},
  year = {2016},
  doi = {10.1007/s10107-014-0851-4},
  note = {Locators refer to the accepted manuscript, https://arnold-neumaier.at/ms/Aggregate.pdf}
}

@article{MullerEtAl2022Surrogate,
  author = {Benjamin M{\"u}ller and Gonzalo Mu{\~n}oz and Maxime Gasse and Ambros Gleixner and Andrea Lodi and Felipe Serrano},
  title = {On generalized surrogate duality in mixed-integer nonlinear programming},
  journal = {Mathematical Programming},
  volume = {192},
  pages = {89--118},
  year = {2022},
  doi = {10.1007/s10107-021-01691-6}
}

@article{GreenbergPierskalla1970,
  author = {Harvey J. Greenberg and William P. Pierskalla},
  title = {Surrogate Mathematical Programming},
  journal = {Operations Research},
  volume = {18},
  number = {5},
  pages = {924--939},
  year = {1970},
  doi = {10.1287/opre.18.5.924}
}

@article{Glover1968,
  author = {Fred Glover},
  title = {Surrogate Constraints},
  journal = {Operations Research},
  volume = {16},
  number = {4},
  pages = {741--749},
  year = {1968},
  doi = {10.1287/opre.16.4.741}
}

@article{Yildiran2009,
  author = {U{\u{g}}ur Y{\i}ld{\i}ran},
  title = {Convex hull of two quadratic constraints is an {LMI} set},
  journal = {IMA Journal of Mathematical Control and Information},
  volume = {26},
  number = {4},
  pages = {417--450},
  year = {2009},
  doi = {10.1093/imamci/dnp023}
}

@article{ModaresiVielma2017,
  author = {Sina Modaresi and Juan Pablo Vielma},
  title = {Convex hull of two quadratic or a conic quadratic and a quadratic inequality},
  journal = {Mathematical Programming},
  volume = {164},
  number = {1--2},
  pages = {383--409},
  year = {2017},
  doi = {10.1007/s10107-016-1084-5}
}

@article{BurerKilincKarzan2017,
  author = {Samuel Burer and Fatma K{\i}l{\i}n{\c{c}}-Karzan},
  title = {How to convexify the intersection of a second order cone and a nonconvex quadratic},
  journal = {Mathematical Programming},
  volume = {162},
  number = {1--2},
  pages = {393--429},
  year = {2017},
  doi = {10.1007/s10107-016-1045-z}
}

@article{DeyHanWang2026,
  author = {Santanu S. Dey and Dahye Han and Yang Wang},
  title = {Aggregation of bilinear bipartite equality constraints and its application to structural model updating problem},
  journal = {Journal of Global Optimization},
  volume = {94},
  number = {4},
  pages = {1099--1135},
  year = {2026},
  doi = {10.1007/s10898-026-01607-8},
  eprint = {2410.14163},
  archivePrefix = {arXiv},
  note = {Venue and DOI from KB metadata; theorem numbers from the KB full text}
}

@article{WuMutsNowakHendrix2025,
  author = {Ouyang Wu and Pavlo Muts and Ivo Nowak and Eligius M. T. Hendrix},
  title = {On the use of overlapping convex hull relaxations to solve nonconvex {MINLPs}},
  journal = {Journal of Global Optimization},
  volume = {91},
  pages = {415--436},
  year = {2025},
  doi = {10.1007/s10898-024-01376-2}
}

@article{MutsNowakHendrix2020,
  author = {Pavlo Muts and Ivo Nowak and Eligius M. T. Hendrix},
  title = {The decomposition-based outer approximation algorithm for convex mixed-integer nonlinear programming},
  journal = {Journal of Global Optimization},
  volume = {77},
  number = {1},
  pages = {75--96},
  year = {2020},
  doi = {10.1007/s10898-020-00888-x}
}

@article{MutsNowakHendrix2021,
  author = {Pavlo Muts and Ivo Nowak and Eligius M. T. Hendrix},
  title = {On decomposition and multiobjective-based column and disjunctive cut generation for {MINLP}},
  journal = {Optimization and Engineering},
  volume = {22},
  number = {3},
  pages = {1389--1418},
  year = {2021},
  doi = {10.1007/s11081-020-09576-x}
}

@article{NowakEtAl2018,
  author = {Ivo Nowak and Norman Breitfeld and Eligius M. T. Hendrix and Gr{\'e}goire Njacheun-Njanzoua},
  title = {Decomposition-based Inner- and Outer-Refinement Algorithms for Global Optimization},
  journal = {Journal of Global Optimization},
  volume = {72},
  number = {2},
  pages = {305--321},
  year = {2018},
  doi = {10.1007/s10898-018-0633-2}
}

@article{NowakVigerske2008,
  author = {Ivo Nowak and Stefan Vigerske},
  title = {{LaGO}: a (heuristic) Branch and Cut algorithm for nonconvex {MINLPs}},
  journal = {Central European Journal of Operations Research},
  volume = {16},
  number = {2},
  pages = {127--138},
  year = {2008},
  doi = {10.1007/s10100-007-0051-x}
}

@article{KaruppiahGrossmann2008,
  author = {Ramkumar Karuppiah and Ignacio E. Grossmann},
  title = {A {L}agrangean based branch-and-cut algorithm for global optimization of nonconvex mixed-integer nonlinear programs with decomposable structures},
  journal = {Journal of Global Optimization},
  volume = {41},
  number = {2},
  pages = {163--186},
  year = {2008},
  doi = {10.1007/s10898-007-9203-8}
}

@article{KaruppiahGrossmann2006,
  author = {Ramkumar Karuppiah and Ignacio E. Grossmann},
  title = {Global optimization for the synthesis of integrated water systems in chemical processes},
  journal = {Computers \& Chemical Engineering},
  volume = {30},
  number = {4},
  pages = {650--673},
  year = {2006},
  doi = {10.1016/j.compchemeng.2005.11.005}
}

@article{MisenerFloudas2014,
  author = {Ruth Misener and Christodoulos A. Floudas},
  title = {{ANTIGONE}: Algorithms for co{NT}inuous / Integer Global Optimization of Nonlinear Equations},
  journal = {Journal of Global Optimization},
  volume = {59},
  number = {2--3},
  pages = {503--526},
  year = {2014},
  doi = {10.1007/s10898-014-0166-2}
}

@article{BaoSahinidisTawarmalani2009,
  author = {Xiaowei Bao and Nikolaos V. Sahinidis and Mohit Tawarmalani},
  title = {Multiterm polyhedral relaxations for nonconvex, quadratically constrained quadratic programs},
  journal = {Optimization Methods and Software},
  volume = {24},
  number = {4--5},
  pages = {485--504},
  year = {2009},
  doi = {10.1080/10556780902883184}
}

@article{KronqvistLundellWesterlund2018,
  author = {Jan Kronqvist and Andreas Lundell and Tapio Westerlund},
  title = {Reformulations for utilizing separability when solving convex {MINLP} problems},
  journal = {Journal of Global Optimization},
  volume = {71},
  number = {3},
  pages = {571--592},
  year = {2018},
  doi = {10.1007/s10898-018-0616-3}
}

@inproceedings{GleixnerWeltge2013,
  author = {Ambros M. Gleixner and Stefan Weltge},
  title = {Learning and Propagating {L}agrangian Variable Bounds for Mixed-Integer Nonlinear Programming},
  booktitle = {Integration of AI and OR Techniques in Constraint Programming for Combinatorial Optimization Problems (CPAIOR 2013)},
  series = {Lecture Notes in Computer Science},
  volume = {7874},
  pages = {355--361},
  year = {2013},
  doi = {10.1007/978-3-642-38171-3_26}
}

@article{Belotti2013,
  author = {Pietro Belotti},
  title = {Bound reduction using pairs of linear inequalities},
  journal = {Journal of Global Optimization},
  volume = {56},
  number = {3},
  pages = {787--819},
  year = {2013},
  doi = {10.1007/s10898-012-9848-9}
}

@article{PuranikSahinidis2017,
  author = {Yash Puranik and Nikolaos V. Sahinidis},
  title = {Domain reduction techniques for global {NLP} and {MINLP} optimization},
  journal = {Constraints},
  volume = {22},
  number = {3},
  pages = {338--376},
  year = {2017},
  doi = {10.1007/s10601-016-9267-5}
}

@article{NeumaierShcherbina2004,
  author = {Arnold Neumaier and Oleg Shcherbina},
  title = {Safe bounds in linear and mixed-integer linear programming},
  journal = {Mathematical Programming},
  volume = {99},
  number = {2},
  pages = {283--296},
  year = {2004},
  doi = {10.1007/s10107-003-0433-3}
}

@misc{BorstEiflerGleixner2024,
  author = {Sander Borst and Leon Eifler and Ambros Gleixner},
  title = {Certified Constraint Propagation and Dual Proof Analysis in a Numerically Exact {MIP} Solver},
  year = {2024},
  eprint = {2403.13567},
  archivePrefix = {arXiv}
}

@article{Balas2005,
  author = {Egon Balas},
  title = {Projection, Lifting and Extended Formulation in Integer and Combinatorial Optimization},
  journal = {Annals of Operations Research},
  volume = {140},
  number = {1},
  pages = {125--161},
  year = {2005},
  doi = {10.1007/s10479-005-3969-1}
}

@article{UdellBoyd2016,
  author = {Madeleine Udell and Stephen Boyd},
  title = {Bounding duality gap for separable problems with linear constraints},
  journal = {Computational Optimization and Applications},
  volume = {64},
  number = {2},
  pages = {355--378},
  year = {2016},
  doi = {10.1007/s10589-015-9819-4}
}

@article{KerdreuxEtAl2023,
  author = {Thomas Kerdreux and Igor Colin and Alexandre d'Aspremont},
  title = {Stable Bounds on the Duality Gap of Separable Nonconvex Optimization Problems},
  journal = {Mathematics of Operations Research},
  volume = {48},
  number = {2},
  pages = {1044--1065},
  year = {2023},
  doi = {10.1287/moor.2022.1291}
}

@misc{DeyMeunierMoran2025,
  author = {Santanu S. Dey and Fr{\'e}d{\'e}ric Meunier and Diego Mor{\'a}n Ram{\'i}rez},
  title = {Geoffrion's theorem beyond finiteness and rationality},
  year = {2025},
  eprint = {2510.10966},
  archivePrefix = {arXiv}
}

@article{CaroeSchultz1999,
  author = {Claus C. Car{\o}e and R{\"u}diger Schultz},
  title = {Dual decomposition in stochastic integer programming},
  journal = {Operations Research Letters},
  volume = {24},
  number = {1--2},
  pages = {37--45},
  year = {1999},
  doi = {10.1016/S0167-6377(98)00050-9}
}

@article{RahmanianiEtAl2020,
  author = {Ragheb Rahmaniani and Shabbir Ahmed and Teodor Gabriel Crainic and Michel Gendreau and Walter Rei},
  title = {The {B}enders Dual Decomposition Method},
  journal = {Operations Research},
  volume = {68},
  number = {3},
  pages = {878--895},
  year = {2020},
  doi = {10.1287/opre.2019.1892}
}

@article{ZouAhmedSun2019,
  author = {Jikai Zou and Shabbir Ahmed and Xu Andy Sun},
  title = {Stochastic dual dynamic integer programming},
  journal = {Mathematical Programming},
  volume = {175},
  number = {1--2},
  pages = {461--502},
  year = {2019},
  doi = {10.1007/s10107-018-1249-5}
}

@article{FullnerRebennack2022,
  author = {Christian F{\"u}llner and Steffen Rebennack},
  title = {Non-convex nested {B}enders decomposition},
  journal = {Mathematical Programming},
  volume = {196},
  number = {1--2},
  pages = {987--1024},
  year = {2022},
  doi = {10.1007/s10107-021-01740-0}
}

@article{ZhangSun2022,
  author = {Shixuan Zhang and Xu Andy Sun},
  title = {Stochastic dual dynamic programming for multistage stochastic mixed-integer nonlinear optimization},
  journal = {Mathematical Programming},
  volume = {196},
  number = {1--2},
  pages = {935--985},
  year = {2022},
  doi = {10.1007/s10107-022-01875-8}
}

@article{LiGrossmann2019,
  author = {Can Li and Ignacio E. Grossmann},
  title = {A generalized {B}enders decomposition-based branch and cut algorithm for two-stage stochastic programs with nonconvex constraints and mixed-binary first and second stage variables},
  journal = {Journal of Global Optimization},
  volume = {75},
  number = {2},
  pages = {247--272},
  year = {2019},
  doi = {10.1007/s10898-019-00816-8}
}

@article{AllmanZhang2021,
  author = {Andrew Allman and Qi Zhang},
  title = {Branch-and-price for a class of nonconvex mixed-integer nonlinear programs},
  journal = {Journal of Global Optimization},
  volume = {81},
  number = {4},
  pages = {861--880},
  year = {2021},
  doi = {10.1007/s10898-021-01027-w}
}

@article{BodurEtAl2018,
  author = {Merve Bodur and Alberto Del Pia and Santanu S. Dey and Marco Molinaro and Sebastian Pokutta},
  title = {Aggregation-based cutting-planes for packing and covering integer programs},
  journal = {Mathematical Programming},
  volume = {171},
  number = {1--2},
  pages = {331--359},
  year = {2018},
  doi = {10.1007/s10107-017-1192-x}
}
```

Entries already in the Report B bibliography (reuse their keys):
- `BoydVandenberghe2004`: author PDF, §5.1.3 p. 216, §5.2.2 p. 225 and
  §5.3.1 p. 232 confirmed here;
- `GleixnerEtAl2017`;
- `DeyMunozSerrano2022`;
- `BlekhermanDeySun2024`;
- `MisenerFloudas2012`, Math. Program. 136:155–182,
  doi:10.1007/s10107-012-0555-6;
- `CookEtAl2009SafeCuts`;
- `EiflerGleixner2024`;
- `ZhuHeTawarmalani2026`.

All DOIs, volumes and pages in the BibTeX block above were checked
against Crossref on 2026-10-03. The exceptions are `DeyHanWang2026`
(taken from KB metadata) and the two arXiv-only entries.

## 8. Read-scope ledger

| Work | Scope actually read | Source |
| --- | --- | --- |
| Nowak 2004 habilitation (= 2005 book content) | §§2.2.5, 2.3 intro, 2.5, 3.1–3.5, 4.2 (Example 4.1 context), 7.1, 7.3–7.4 | edoc.hu-berlin.de PDF |
| Wu, Muts, Nowak, Hendrix 2025 | Full text | KB `wu2025-on-the-use-of-overlapping` |
| Muts, Nowak, Hendrix 2020 | §§1–3, references | KB `muts2020-...` |
| Gleixner et al. 2017 | §§1–2.2, Thm 1, Remarks 1–3 (ZIB report) | KB `gleixner2017-...` |
| Tawarmalani–Sahinidis 2004 | §4 (pp. 15–21 preprint) | KB `tawarmalani2004-...` |
| Müller et al. 2022 | §§1–2, Defs 1–2, theorem statements | KB `muller2022-...` |
| Dey–Muñoz–Serrano 2022 | §§1–2, theorem and proposition statements | KB `dey2022-...` |
| Blekherman–Dey–Sun 2024 | Abstract and §1 (preprint 2022-10-05) | KB `blekherman2024-...` |
| Modaresi–Vielma 2017 | Abstract, §§1–2, theorem list (manuscript) | KB `modaresi2017-...` |
| Burer–Kılınç-Karzan 2017 | Abstract, p. 2, Theorem 1 statement | KB `burer2017-...` |
| Dey–Han–Wang 2026 | Abstract, §1, Theorems 1–3 statements | KB `dey2026-aggregation-...` |
| Chen–Luedtke 2022 | §§2–3 (arXiv pp. 4–7) | KB `chen2022-...` |
| Neumaier–Shcherbina 2004 | §§3–4, 7 (pp. 286–289, 294) | KB `neumaier2004-safe-...` |
| Eifler–Gleixner 2024 | §§2.2–2.3 (arXiv pp. 7–8) | KB `eifler2024-...` |
| Domes–Neumaier 2016 | §§1–3.2 (accepted manuscript) | arnold-neumaier.at PDF |
| Boyd–Vandenberghe 2004 | §§5.1–5.3 (pp. 215–234) | author PDF |
| Kerdreux et al. 2023 | §2.2 (pp. 3–4) | KB |
| Udell–Boyd 2016 | pp. 1–4 | KB |
| Karuppiah–Grossmann 2006 | p. 8 passage | KB |
| Puranik–Sahinidis 2017 | p. 8 passage | KB (arXiv) |
| Füllner–Rebennack 2022; Zhang–Sun 2022 | Introductions (pp. 2–3) | KB |
| Zhu–He–Tawarmalani 2026 | p. 6 passage | KB |
| Tawarmalani–Sahinidis 2005; Bao et al. 2009; Li–Grossmann 2019; Allman–Zhang 2021; Borst et al. 2024; Caprara–Locatelli 2010 | KB summaries and theorem lists only | KB |
| Lemaréchal–Renaud 2001; Feltenmark–Kiwiel 2000; Geoffrion 1974; Falk 1969; Magnanti–Shapiro–Wagner 1976; Aubin–Ekeland 1976; Karuppiah–Grossmann 2008; Misener–Floudas 2012, 2014; Kronqvist–Lundell–Westerlund 2018; Belotti 2013; Yildiran 2009; Balas 2005; Dey–Meunier–Morán 2025; Muts–Nowak–Hendrix 2021; Nowak et al. 2018; Nowak–Vigerske 2008; Glover 1968; Greenberg–Pierskalla 1970; Carøe–Schultz 1999; Rahmaniani et al. 2020; Zou–Ahmed–Sun 2019; Bodur et al. 2018 | Abstract, publisher metadata, or secondary statement only | Crossref, publisher or abstract pages, citing papers |

## 9. Checks run in this lane

- Inline Python (numpy, project venv; no file written). The x²=1/4
  example: every sampled Lagrangian cut over (a,ν) ∈ [−5,5]² accepts
  x=1/4, with maximum violation 0.0. The surrogate sets give
  conv(S_{+1}) = [0,1/2] and conv(S_{−1}) = [1/2,1], whose intersection
  is {1/2}.
- Crossref lookups for the DOIs listed as checked.
- No solver runs, no project-wide tests, no CI inspection. Nothing was
  written under `literature/` or `research-2026100*-convexification/`.
  Downloaded PDFs were kept in a scratch directory outside the
  repository.
