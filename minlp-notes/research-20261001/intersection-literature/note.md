# Priority and context audit for the optimal intersection-cut results

Workstream note, research-20261001, stream `intersection-literature`.
Date: 2026-10-01. This audit replaces Section 10 of
[`../../research-20260928b/sfree/optimal-intersection-cuts.md`](../../research-20260928b/sfree/optimal-intersection-cuts.md)
(called "the sfree note" below), which was written without web search.
Theorem numbers such as "Theorem 1" or "Proposition 16" refer to the sfree note
unless stated otherwise. Sources are in [`sources/`](sources/) with a
[manifest](sources/MANIFEST.md); search records are in [`logs/`](logs/); scripts
are in [`code/`](code/). Program files were included in repository commits made outside this program
(e.g. `d91d8d98b`, `f785387a8`, `b59ed1b83`); the program itself makes no commits.
Final status (2026-10-04): reviewed in three rounds;
[round 3](reviews/review-r3.md) verified the revision; not refereed.
"Reviewed" in this
program means checked by another research agent. Review round 1
([`reviews/review-r1.md`](reviews/review-r1.md)) found three major and four
minor issues; the revision of 2026-10-02 fixed them (Section 11). Review
round 2 ([`reviews/review-r2.md`](reviews/review-r2.md)) confirmed those fixes
and found two minor issues; this version fixes them (Section 12). The version
after round 2 was verified in [round 3](reviews/review-r3.md).

## Summary

**Main answer.** I found no work, up to 2026-10-01, that chooses among maximal
quadratic-free (or other S-free) sets to get the best intersection cut for a
quadratic constraint, or that computes the best single intersection cut for
QCQPs. Every paper that cites the six papers listed in Section 2.1, according to
Semantic Scholar, OpenAlex and OpenCitations, works on something else (Section 2).
This is an unsuccessful search. It does not establish novelty.

The search did change the context of three results:

1. **Theorem 1 and Proposition 2 are closer to known results than the old
   audit said.** The cut-generating-function literature already contains:
   - exact dominance of every valid cut by a single S-free cut when
     `S − x̄ ⊆ cone(R)` (Cornuéjols–Wolsey–Yıldız, Math. Program. 152, 2015,
     Thm. 1.1; reproved by Kılınç-Karzan–Steffy, Math. Program. 159, 2016,
     Prop. 5) or when `cone(R)` is the whole space (Conforti–Cornuéjols–
     Daniilidis–Lemaréchal–Malick, MOR 40, 2015, Thm. 6.3);
   - dominance of every valid cut by a *relaxed* cut-generating function
     (a support function that may take the value `+∞`), with no assumptions
     (Kılınç-Karzan–Steffy 2016, Cor. 2 and the discussion after it). This is
     close to Theorem 1(5);
   - the failure mechanism of Proposition 2(a) (CCDLM, §6, the "more
     nonlinear" variant of Example 6.1; Kılınç-Karzan–Yang Example 4.5);
   - sufficient and nearly necessary conditions when `S − x̄ ⊄ cone(R)`
     (Kılınç-Karzan–Yang, author draft revised Oct. 2017, Prop. 3.11,
     Cor. 3.12, Prop. 4.3, Cor. 4.4), and **examples showing that their strict
     conditions cannot be dropped** (their Examples 4.3 and 4.5) and that, in
     the equality case, attainment depends on whether the outside points
     approach the limit point transversally (Example 4.2: attained) or
     tangentially (Example 4.3: not attained).

   **Proposition 2(b) is KY Example 4.3 with the coordinates swapped**, with a
   quadratic sublevel set in place of their discrete sequence. It must be
   cited as such.

   KY Cor. 3.12 is false as printed (two counterexamples, checked exactly in
   Section 4.4). A corrected form, which is what KY's proof gives, requires
   the ray of each `D_2` point to avoid `cl(B_2)`. From the corrected form one
   can derive Theorem 1(2) (Remark 4.4). What remains of Theorem 1 is part (4),
   as a **general sufficient condition** (transversality at every corner
   minimizer, for `S = {q ≤ 0}` with any `q ∈ C^1`). It formalizes the
   transversal/tangential distinction that KY illustrate by Examples 4.2 and
   4.3 (the mechanism; their discrete Example 4.2 is not itself covered). It
   decides cases that KY's corrected sufficient condition and their
   necessary conditions leave open. The Theorem 14 corner is such a case
   (exact check, Section 4.4).
2. **New (known-result) consequence, Proposition A.** If the projected rays
   positively span `R^k`, the polytope `conv{s̄, s̄ + (z_K/w_j) p_j}` is already
   S-free and attains `z_K` for every `w ≥ 0`. This is CCDLM Thm. 6.3
   specialized to the sfree setting. It is not new and has no direct solver
   relevance: the projected rays span `R^3` in **0 of the 120** McCormick LP
   corners of the sfree note (LP-based, tolerance `10^-9`; Section 4.3). For
   bilinear `S` the second hypothesis of Proposition A (`S_k − s̄ ⊆ cone(P)`)
   is equivalent to the first, so Proposition A applies to none of these
   corners. For LP corners the relevant attainment criterion stays Theorem
   1(4).
3. **The orbit parametrization extends a known one-parameter family.** In
   Bienstock–Chen–Muñoz (Math. Program. 183, 2020; arXiv v7 Lemma 22,
   Thm. 23(iv)) the maximal outer-product-free sets (14a) for a 2×2 minor are
   exactly the orbit sets `{sym(F^T M) ⪰ 0}` with `F` a rotation, and no other
   orbit set with `det F > 0` is a (14a) or (14b) set (Proposition B; proved in
   general, identities checked exactly). The sfree note's orbit
   `{sym(F^T M) ⪰ 0 : det F > 0}` is the three-parameter extension under
   `SL_2 × SL_2`. I did not find it stated. BCM also posed the selection
   question explicitly: their choice of `λ` is "'best' in a violation sense, and may not translate to
   finding the deepest cut" (arXiv v7, p. 24). The note must cite this.

**Classical deeper-cut literature.** Glover 1973, Konno 1975/76, Porembski
1996–2008, Eckstein–Nediak 2003/05 and Balas–Margot 2013 all order cuts by step
lengths (coefficient-wise dominance) and seek deeper cuts in special settings.
Eckstein–Nediak formulate a "deepest cut generation problem" over S-free sets
for MIP. That is the closest precedent for "best cut selection", but it uses
distance-based depth, a finite set `Y` of integer points, and restricted
parametrizations. None of these works treats maximal quadratic-free sets, the
corner-bound criterion, the inertia bound, or the orbit results.

**Solver baseline.** Quadratic intersection cuts have been off by default since
SCIP 8.0 and still are in SCIP 10.0.3 (`DEFAULT_USEINTERCUTS FALSE`). The
SCIP 8 leaves these dense cuts disabled because their net benefit is unclear.
(SCIP 8 MINLP paper, §2.3.5). The only published evaluation I could read is a
root-node experiment: Chmiela–Muñoz–Serrano, ZIB-Report 20-29, §5, 587
MINLPLib instances, mean gap closed 0.56 with default SCIP and 0.62 with the
best cut setting. It ran in a development SCIP with CPLEX 12.10, and
branch-and-bound effects are given only as LP-speed remarks. SCIP 9 says
monoidal strengthening makes the cuts "significantly outperform the pure
intersection cuts whenever monoidal strengthening can be applied", citing the
monoidal paper. I could not access the computations of the monoidal paper or
the Math. Program. 197 version of Chmiela et al. So the accurate statement is:
no branch-and-bound comparison appears **in the sources I could read**.

**Revised novelty verdicts** (Section 7):

| Result | Verdict |
|---|---|
| Thm 1(1)–(3), (5) | Known or derivable from published/preprint results (CWY 2015 and Kılınç-Karzan–Steffy 2016 under a cone condition; Kılınç-Karzan–Steffy 2016 Cor. 2 for relaxed CGFs; corrected Kılınç-Karzan–Yang Cor. 3.12 in general); keep as background with citations |
| Thm 1(4) attainment criterion | General sufficient condition not found; KY Examples 4.2/4.3 already show by example that transversal versus tangential approach decides attainment in the equality case; modest |
| Prop 2 | (a) same mechanism as CCDLM §6 variant of Example 6.1; (b) a quadratic version of KY Example 4.3 (coordinates swapped); cite both |
| Lemma 3 | Classical (basic solutions) |
| Thm 4 (inertia bound) | No prior statement found; standard technique |
| Thm 5 | Polynomial part routine; hardness a standard Motzkin–Straus reduction; the statement for best intersection cuts not found |
| Prop 6, Remark 7 | Quantitative statements not found; qualitative precedents (MS 2022 §6, BCM 2020 p. 24, Chmiela Remark 3) |
| Thm 8 | No prior statement found; short consequence of MPS 2025/2026 plus Möbius 2-transitivity |
| Prop 9 | Elementary example of a well-known phenomenon (one round is not enough) |
| Orbit `{sym(F^T M) ⪰ 0}`, Lemma 10, Prop 12, Thm 11, Lemma 13, Thm 14, Prop 16 | No prior statement found; the rotation subfamily is BCM's (14a) |

---

## 1. Scope and method

Four kinds of search were used:

- **Citation lists.** Semantic Scholar (the API is rate-limited from this
  machine, so it was fetched through WebFetch; `logs/s2_citations_via_webfetch.md`),
  OpenAlex (`code/openalex_citers.py`, `logs/openalex_citers.jsonl`), and
  OpenCitations (`logs/opencitations.log`). Google Scholar was not used, because
  it requires CAPTCHAs.
- **Keyword search.** 28 WebSearch queries, most in "extended" mode, plus 2 in
  revision round 1
  (`logs/web_searches.md`), and arXiv API queries (`code/arxiv_search.py`,
  `logs/arxiv_*.log`).
- **Metadata.** Crossref, OpenAlex and zbMATH Open (`logs/crossref_*.log`,
  `logs/openalex_abstracts.log`, `logs/zbmath_lookup.log`).
- **Full texts** of open copies (manifest). Springer pages are behind a
  bot-check and paywall. They were not bypassed, and Springer-only papers were
  not read.

The comparisons below use only text I read. Each claim about a source has a
locator (section, theorem, page of the copy in `sources/`). Where only an
abstract, a title or a secondary description was available, I say so.

## 2. Recent and concurrent work (2024–2026)

### 2.1 Citing papers

Union of the citation lists for: Muñoz–Serrano (Math. Program. 192, 2022,
arXiv:1911.12341); Chmiela–Muñoz–Serrano (Math. Program. 197, 2023);
Muñoz–Paat–Serrano (Math. Program. 210, 2025, arXiv:2211.05185; IPCO 2023);
Muñoz–Paat–Serrano (arXiv:2605.30602, May 2026); Chmiela–Muñoz–Serrano,
monoidal strengthening (Math. Program. B 210, 2025; IPCO 2023); and
Bienstock–Chen–Muñoz (Math. Program. 183, 2020).

| Citing work (year) | What it does | Relevance to set choice / best cut |
|---|---|---|
| MPS, inhomogeneous case, arXiv:2605.30602 (2026) | Characterizes all maximal `Q_g`-free sets | p. 2: "Prior work has implemented intersection cuts using only one family of such sets"; no selection |
| MPS, homogeneous case (2025) | Characterization via non-expansive `Γ` | §8 (arXiv v2, p. 26): open question on polyhedral sets; no selection |
| Chmiela–Muñoz–Serrano, monoidal (2025) | Lifting for integer nonbasic variables | Abstract only (ZIB OPUS 8959; file access "not granted"); not about the choice of S-free set |
| SCIP 8 MINLP (JOGO 2023), SCIP 9 report (2024) | Solver descriptions | Off by default (Section 6) |
| Xu–Liberti, submodular maximization through an intersection-cut lens (Math. Program. 2024) | Hypograph-free sets | Unique-maximal-set settings; no selection among quadratic-free sets |
| Xu–D'Ambrosio–Liberti–Haddad-Vanier, signomial cuts (SIOPT 2025) | Signomial-free sets | No |
| Dey–Kazachkov–Lodi–Muñoz, sparse PCA cuts (SIOPT 2022) | Sparse cut generation | No |
| Dey–Muñoz–Serrano, aggregations (SIOPT 2022); Gu–Dey–Richard (Math. Program. 2022); Dash–Günlük–Lee (Math. Program. 2021); Behrends–Schöbel (JOTA 2020); Del Pia (SIOPT 2025) | Hulls, lifting, closures, complexity | No |
| Turner et al., cut selection with analytic centers (2022) | MILP cut selection in SCIP | Cut selection, not set selection |
| Rahimian–Mehrotra, disjunctive cuts for bilinear programs (SIOPT 2024) | Finite disjunctive cutting-plane algorithm | Abstract only (Crossref); not intersection-cut set choice |
| Dey–Jiang–Kazachkov–Lodi–Muñoz, Eigen-CG (arXiv:2604.00932, 2026) | CG rounding of eigenvector cuts | Abstract: no intersection cuts |
| Pathy–Rahimian (arXiv:2609.33946, Sep. 2026) | S-free sets for chance constraints | Different `S`; no quadratic-free sets |
| Xu–Pokutta (arXiv:2608.03318, Aug. 2026) | Two-row joint-range hulls for QCQP | Computes the hull of a projected 2-D set; Remark 4 identifies some cuts as intersection cuts; no selection among maximal sets |
| Duguet et al. (arXiv:2506.02520) | Intersection cuts for Nash equilibria | Different `S` |
| Kuznetsov–Sahinidis survey (Optimization Online 2024) | Euclidean-norm problems | Cites MS 2022; title/abstract only |
| Others citing BCM (energy markets, optimal control, KAN convexification, bilevel) | Applications | No |

Counts: the Semantic Scholar list for arXiv:1911.12341 now has 17 entries (the
sfree note found 16 in September; the new one is the Kuznetsov–Sahinidis
survey). The MPS 2025 paper is cited only by MPS 2026. MPS 2026 has no citing
papers, and arXiv shows only its v1 (28 May 2026).

### 2.2 Keyword searches

Searches combined quadratic-free, S-free, best, strongest, deepest, optimal
intersection cut, corner relaxation, Lorentz, Möbius, bilinear-free,
outer-product-free and 2024–2026. They found no paper on choosing among maximal
quadratic-free sets for cut strength (`logs/web_searches.md`, rows 1–4 and
22–27). The arXiv API phrase queries `abs:"quadratic-free"` and
`abs:"intersection cut" AND abs:quadratic` return only the MS/MPS papers,
Modaresi–Kılınç–Vielma and Duguet et al. (`logs/arxiv_searches.log`).

**Assessment.** As of 2026-10-01 I found no concurrent work. The risk remains
real. MPS 2026 (p. 2) calls the full characterization "a new avenue to
strengthen cutting-plane methods", and the same group controls SCIP's
implementation.

## 3. Classical literature on deeper cuts

| Source (copy read) | Exact locators | What it contains | Relation to the sfree results |
|---|---|---|---|
| Tuy, "Concave programming under linear constraints", Doklady 1964 (Soviet Math. 5, 1437–1440) | Not accessed | Origin of concavity (γ-valid) cuts, per Glover 1973 ref. 14 and Note 1 (p. 133), Eckstein–Nediak §1, Towle–Luedtke §1 | For reverse-convex `S` the complement closure is the unique maximal S-free set (sfree §3, first corollary) |
| Glover, "Convexity cuts and cut search", Oper. Res. 21 (1973) 123–134 (author-hosted scan) | Convexity-Cut Lemma p. 124; Remark 1 pp. 124–125; Remark 11 p. 127; speculation 3 p. 128; Note 1 p. 133 | Cut from any convex `R` with `B_0 ∈ int R`, `int R ∩ S = ∅` and step lengths `t_j*`. Remark 1: when the constraints imply the cone, every valid halfspace minimized at the vertex over the cone is a convexity cut. Remark 11: the cut gets stronger as the `t_j*` grow. Cut search can give stronger cuts | Remark 1 is the trivial case of exact attainment when `S` lies in the cone (the halfspace itself is S-free). This is the precursor of CWY and of Proposition A. No set-selection criterion |
| Konno, "A cutting plane algorithm for solving bilinear programs", IIASA RM-75-061 (Dec. 1975), published as Math. Program. 11 (1976) 14–27; also WP-74-075 | §3: Lemma 3.1, Theorem 3.3, Definition 3.1 ("deeper cut"), "Iterative Improvement Procedure" | For disjoint bilinear programs, at a local maximum pair, each step length `θ_ℓ` is the largest `θ` with `max_{y_2 ∈ Y_2} φ ≤ φ_max + ε` along the ray (an LP). A cut is deeper if all its step lengths are larger. Shrinking `Y_2` by the other cut and iterating gives deeper cuts | Same coefficient-wise strength order as the sfree note. The convex region is fixed by the problem structure, so there is no choice among S-free sets. Not about `{w ≤ xy}`-free sets for one bilinear term |
| Sherali–Shetty, "A finitely convergent algorithm for bilinear programming problems using polar cuts and disjunctive face cuts", Math. Program. 19 (1980) 14–31 | Not accessed (title and metadata) | Per its title and the citing literature: polar cuts with negative edge extensions and disjunctive face cuts | Negative edge extension is the strengthening family behind SCIP's `usestrengthening` (SCIP 8 report §4.3.3 cites Glover 1974). It concerns infinite step lengths, not the choice of set |
| Porembski, thesis (Marburg 1996); "How to extend the concept of convexity cuts to derive deeper cutting planes", JOGO 15 (1999) 371–404; "Finitely convergent cutting planes for concave minimization", JOGO 20 (2001); "Cone adaptation strategies ...", JOGO 24 (2002) 89–107; "Cutting planes for low-rank-like concave minimization problems", Oper. Res. 52 (2004) 942–953; "On the hierarchy of γ-valid cuts", NRL 55 (2008) 1–15 | Full texts not accessed. zbMATH reviews/summaries: thesis Ch. 3; 2001 (Zbl 1701641); 2008 summary; 2004 abstract (Crossref) | Thesis Ch. 3: transforms a convex set `K` with polyhedral closure into `K*` whose convexity cut removes a "largest possible" part of `P ∩ int K`. 1999: decomposition cuts, which beat convexity cuts in experiments. 2001: the cut is taken relative to a modified cone (vertex and base pulled along `−c`). 2008: dominance of decomposition cuts over concavity cuts, the degenerate case, finite convergence | Deeper cuts for concave minimization by changing the set (thesis) or the cone (2001, 2002). No quadratic-free sets, no corner-bound optimality theorem, no complexity result. Thesis Ch. 3 is the closest in spirit to "choose the set to maximize depth", for reverse-convex sets |
| Eckstein–Nediak, "Depth-optimized convexity cuts", RUTCOR RRR 23-2003 (rev. Nov. 2003), published as Ann. Oper. Res. 139 (2005) 95–129 | §2: Prop. 2.7 (strength order: same edges, larger step lengths), Prop. 2.9 (monotone in the set), Prop. 2.10 / Cor. 2.11 (strongest cuts come from sets `X(d) = {x : d(y)^T x ≤ d(y)^T y ∀y ∈ Y}`); §4: "deepest cut generation problem" (25)–(29) and (40)–(42), restricted to pairs of coordinates in (48)–(54); §5: MIPLIB tests | General treatment of convexity cuts. The strongest cuts come from sets built from separating hyperplanes at points of `Y`. For MIP (finite `Y`) the deepest cut (largest norm distance) is an optimization over these sets. It has `p·2^p` parameters, so they restrict to two coordinates and get an LP | **Closest precedent for "best intersection cut over all S-free sets".** Differences: distance-based depth instead of the bound `z_C(w)`; finite `Y` (integer points) instead of a quadric; no exactness theorem like Theorem 1 and no complexity results like Theorem 5. Must be cited |
| Balas–Margot, "Generalized intersection cuts and a new cut generating paradigm", Math. Program. 137 (2013) 19–35 | Primary not accessed. Secondary: Kazachkov–Nadarajah–Balas–Margot, arXiv:1703.02221 v2, §1–2 (Theorem 4 of Balas–Margot; PRLP) | Fix the S-free set; replace the basis cone by a tighter relaxation `C` (activate more hyperplanes); collect intersection points and rays; choose the cut by the LP (PRLP) over the point-ray collection, for an objective direction | The complementary axis: fix `S`-free set and vary the relaxation (GICs), versus fix the cone and vary the S-free set (sfree note). The PRLP with an objective direction is analogous to the bound-optimal choice. Must be cited |
| Conforti–Cornuéjols–Daniilidis–Lemaréchal–Malick, "Cut-generating functions and S-free sets", MOR 40 (2015) 276–301 (HAL v1 and UAB preprint 05/2013 read) | Thm. 4.3 (Zorn; preprint p. 11); Example 6.1 (HAL p. 24); Prop. 6.2 and the "more nonlinear" variant (HAL p. 25, Fig. 12; preprint pp. 20–21, Fig. 9); Thm. 6.3 (HAL p. 25; preprint p. 21) | Cut-generating functions correspond to S-free neighbourhoods. Ex. 6.1: not all cuts come from cgf's. The variant (`S` the curve `ψ = −1/|φ|`, cut `c = (0, 1)`): a zero coefficient on a ray that `S` approaches asymptotically from outside the cone cannot be generated. Thm. 6.3: if `cone(R) = R^q`, every cut `c ≥ 0` is generated, with the S-free set `conv{r_j/c_j : c_j > 0} + cone{r_j : c_j = 0}` | Prop. 2(a) of the sfree note is the same mechanism as the variant (there `X = ∅`, here `X` is a point). Thm. 6.3 gives Proposition A (Section 4) |
| Cornuéjols–Wolsey–Yıldız, "Sufficiency of cut-generating functions", Math. Program. 152 (2015) 643–651 (read as Ch. 4 of Yıldız's CMU thesis, 2016) | Thm. 1.1 = thesis Thm. 4.1 (p. 66); Prop. 4.5 (p. 69); proof via `h_c(r) = min{c^T s : Rs = r, s ≥ 0}` and the extension `h'_c`, Cor. 4.10 (p. 72) | If `S ⊆ cone(R)`, every valid cut `c^T s ≥ 1` is dominated by a single S-intersection cut | Exact single-cut attainment of `z_K` for every `w ≥ 0` under `S − x̄ ⊆ cone(P)`. Theorem 1(2)–(4) concern the case where this fails (Section 4) |
| Kılınç-Karzan–Steffy, "On sublinear inequalities for mixed integer conic programs", Math. Program. 159 (2016) 585–605 (author draft, rev. Jul. 2015, read) | Prop. 3 (p. 8: `R^n_+`-sublinear inequalities suffice, no assumptions); Def. 3 and Prop. 4 (p. 9: relaxed CGFs = support functions, possibly `+∞`); Cor. 2 (p. 10); discussion pp. 10–11 ("without any further technical assumptions, the relaxed CGFs are always sufficient"); Prop. 5 (p. 11: if `B ⊆ cone(A)`, `σ_{D_{c,ρ}}` is a finite CGF; "recovers the main result, Theorem 1.1, of [CWY]") | Every valid cut separating the origin is dominated by a relaxed CGF cut, with no assumptions; under `B ⊆ cone(A)` by a genuine CGF (second proof of CWY) | Refereed counterpart of the KY draft. Cor. 2 is close to Theorem 1(5): it gives exact domination by relaxed CGFs, whose level sets need not contain 0 in their interior; Theorem 1(5) uses genuine S-free sets and obtains the closure by the approximation in Theorem 1(2). Prop. 5 is a second source for the cone case of Theorem 1(2) |
| Kılınç-Karzan–Yang, "Sufficient conditions and necessary conditions for the sufficiency of cut-generating functions", author draft (Dec. 2015, rev. Oct. 2017); no journal version found | §3: partition (3) `B_1 = B ∩ cone(A)`, `B_2 = B \ B_1`; Prop. 3.6 (`B_2` compact); Prop. 3.8, Cor. 3.9 (`cl(R_{++}(B_2)) ∩ cone(A) ⊆ {0}`); Prop. 3.11 (p. 15), Cor. 3.12 (pp. 17–18; strict conditions (iii)); §4: Prop. 4.1, 4.3, Cor. 4.4 (necessary conditions); **Examples 4.2–4.5 (pp. 21–23, Fig. 4–5)** | Sufficiency of cgf's when `B ⊄ cone(A)`, under strict conditions at limit points and limit directions of `B_2` inside `cone(A)`; near-matching necessary conditions. Ex. 4.2 (`B_2 = {(1, −1/n)}`, transversal approach to `e_1`): `c = (1, 1)` is generated although `σ = 1`. Ex. 4.3 (`B_2 = {(1 − 1/√n, −1/n)}`, tangential approach): `c = (1, 1)` is not generated. Ex. 4.4/4.5: the same pair for `σ = 0` along a limit direction | Cor. 3.12 is false as printed; the corrected form (ray of each `D_2` point avoids `cl(B_2)`) implies Theorem 1(2) for `w > 0` (Section 4.4). Ex. 4.3 is Proposition 2(b) with coordinates swapped. Ex. 4.2/4.3 illustrate by example the distinction that Theorem 1(4) states as a general sufficient condition |

**What the old Section 10 got wrong about this literature.**

- Glover 1973, Konno and Eckstein–Nediak do treat "which convex set, which cut".
  Eckstein–Nediak even pose the deepest-cut problem over all S-free sets. The
  old audit called these works precedents only "in special cases". That is fair
  for Glover and Konno, but too weak for Eckstein–Nediak.
- Theorem 1 was described as "the finite-ray, closed-S form of the sufficiency
  of S-free sets ... and folklore". In fact CWY is a single-cut dominance
  theorem, not only a closure theorem. Under its cone hypothesis it already
  gives exact attainment. The precise relation is in Section 4.

## 4. Theorem 1 and the sufficiency of cut-generating functions

Notation as in the sfree note, §1. Work in the projected space: closed
`S_k ⊆ R^k`, `s̄ ∉ S_k`, projected rays `P = [p_1, …, p_N]`, `w ≥ 0`,
`X = {λ ≥ 0 : s̄ + Pλ ∈ S_k}` and `z = z_K(w)`. For a closed convex
`V ⊆ R^k` with `s̄ ∈ int V` and `int V ∩ S_k = ∅`, the step lengths are
`α_j(V)` and the cut bound is `z_V(w) = min_{α_j < ∞} w_j α_j`. Lifting to
`R^d` uses `C = {x : s̄ + E(x − x̄) ∈ V}`. Since `E` is a surjective linear map,
`int C = E^{-1}(int V)`, so `C` is S-free with the same step lengths. Only
full-dimensional sets are used.

### 4.1 Dictionary

The CCDLM/CWY model is `X(R, S_0) = {s ∈ R^k_+ : Rs ∈ S_0}`. It matches the
sfree setting with `S_0 = S_k − s̄` and `R = P`. A cut-generating function
(cgf) is a finite sublinear `ρ`, and `V = {r : ρ(r) ≤ 1}` is an `S_0`-free
neighbourhood of 0. The gauge of `V` is `γ_V = max(ρ, 0)`, because `ρ` is
positively homogeneous. So if `ρ(p_j) ≤ c_j` and `c ≥ 0`, then
`1/α_j(V) = γ_V(p_j) ≤ c_j`. With `c = w/z` this gives `α_j ≥ z/w_j` and
`z_V(w) ≥ z`. "A valid cut `c` is dominated by a cgf cut" therefore implies
"`z_K` is attained by a single intersection cut".

### 4.2 Proposition A (attainment when the rays span)

**Proposition A** (proved; a specialization of CCDLM Thm. 6.3, and of CWY
Thm. 1.1 for (ii)). Let `S_k` be closed, `s̄ ∉ S_k`, `w ∈ R^N_{≥0}` and
`0 < z = z_K(w) < ∞`.

1. If `cone(P) = R^k`, then `V = s̄ + P·{λ ≥ 0 : w^T λ ≤ z}` is closed,
   convex and S-free, with `s̄ ∈ int V` and `z_V(w) = z`. The step lengths
   satisfy `α_j(V) ≥ z/w_j`, with `α_j = ∞` when `w_j = 0`.
2. If `S_k − s̄ ⊆ cone(P)`, some S-free `V` attains `z_V(w) = z`.

In both cases the supremum of Theorem 1(2) is attained for every `w ≥ 0`. This
holds also when `w` has zero entries and without the regularity hypothesis of
Theorem 1(4).

*Proof.* (1) `V` is the image of a polyhedron under an affine map, so it is a
polyhedron. Since `cone(P) = R^k`, each `±e_i` equals `Pμ_i^±` with
`μ_i^± ≥ 0`. For `u ∈ R^k`, write `u = Σ_i (u_i^+ Pμ_i^+ + u_i^- Pμ_i^-)`; its
cost is at most `‖u‖_1 max w^T μ_i^±`, which is `≤ z` for small `‖u‖`. Hence a
ball around `s̄` lies in `V`.

`V` is S-free: let `s ∈ int V`. Then `s̄ + (1 + ε)(s − s̄) ∈ V` for some
`ε > 0`, that is, `(1 + ε)(s − s̄) = Pλ` with `λ ≥ 0` and `w^T λ ≤ z`. Put
`λ' = λ/(1 + ε)`. Then `s = s̄ + Pλ'` and `w^T λ' < z`. If `s ∈ S_k`, then
`λ' ∈ X`, which contradicts `z = inf_X w^T λ`.

Step lengths: `s̄ + t p_j = s̄ + P(t e_j) ∈ V` whenever `t w_j ≤ z`. So
`z_V(w) ≥ z`, and `≤` is validity.

(2) Apply CWY Thm. 1.1 to the valid cut `c = w/z` (`c^T λ ≥ 1` on `X`). Then
use the dictionary of §4.1. ∎

Part (1) is exactly the construction in the proof of CCDLM Thm. 6.3. Nothing
in Proposition A is new. Its use here is to locate the sfree attainment
question: Theorem 1(4) and Proposition 2 matter only when `cone(P) ≠ R^k` and
`S_k − s̄ ⊄ cone(P)`.

### 4.3 How often does `cone(P) = R^3` hold on LP corners? (computed)

`code/cone_span_mccormick.py` replays the generator of the sfree note's §9.2
with the same seeds and filters, including the SCIP bound `z_1 > 10^-6`. It
reproduces the instance counts 47 and 73. For each corner it tests
`{y : P^T y ≤ 0} = {0}` with six HiGHS LPs (tolerance `10^-9`). This is part
(1) of Proposition A.

| Generator | Corners | `cone(P) = R^3` |
|---|---|---|
| 4 vars, 4 products, seed 11 | 47 | 0 |
| 6 vars, 8 products, seed 12 | 73 | 0 |

(LP-based, numerical tolerance `10^-9`; `logs/cone_span_mccormick_11.log`,
`logs/cone_span_mccormick_12.log`.) *Heuristic explanation, not checked
instance by instance:* at these vertices some tight constraint (a bound on
`x_i` or `x_j`, or a McCormick row of the violated product) involves only the
three projected coordinates. That puts the projected cone in a halfspace. The
Theorem 14 and Proposition 16 corners have `N = 3 = k` rays, so `cone(P) ≠ R^3`
there as well (exactly).

*Part (2) of Proposition A* (added after review round 1; proved). Part (1) is a
special case of part (2), since `cone(P) = R^k` implies `S_k − s̄ ⊆ cone(P)`.
For the sets of these corners the converse also holds. Here `S_k` is
`{w ≤ xy}` or `{w ≥ xy}` in the projected coordinates `(x_i, x_j, w_ij)`. A
convex cone other than `R^3` lies in a closed halfspace `{y : a^T y ≥ 0}` with
`a ≠ 0`. But `{w ≤ xy}` lies in no closed halfspace `{a^T(x, y, w) ≥ β}`:

- if `a_w > 0`, fix `x, y` and let `w → −∞`;
- if `a_w < 0`, take `x = y = t`, `w = t^2` and let `t → ∞`;
- if `a_w = 0`, take `(x, y) = −s(a_x, a_y)`, `w = xy`, and let `s → ∞`.

In each case `a^T(x, y, w) → −∞`. Translation by `s̄` does not change this, and
the linear bijection `(x, y, w) ↦ (−x, y, −w)` maps `{w ≥ xy}` onto `{w ≤ xy}`.
So `S_k − s̄ ⊆ cone(P)` holds iff `cone(P) = R^3`. Therefore Proposition A
(both parts) applies to none of the 120 corners (subject to the LP tolerance)
and to neither the Theorem 14 nor the Proposition 16 corner (exactly).

### 4.4 Theorem 1(2) and (4) against Kılınç-Karzan–Yang

This subsection was rewritten after review round 1 (issues M1, M2).

KY's setting is `S(A, R^n_+, B)` with `B` partitioned as `B_1 = B ∩ cone(A)`,
`B_2 = B \ B_1` (their (3)). For `d ∈ cone(A)` and `c ≥ 0`,
`σ_{D_c}(d) = max{λ^T d : A^T λ ≤ c} = min{c^T μ : Aμ = d, μ ≥ 0}` by LP
duality. In the sfree setting `B = S_k − s̄` (closed, `0 ∉ B`) and `A = P`.

**KY Cor. 3.12 as printed (draft pp. 17–18).** Let `c^T x ≥ 1` be valid and
separate the origin. Suppose there are sets
`D_1 ⊆ cl(B_2) ∩ cone(A)` and
`D_2 ⊆ (cl(R_{++}(B_2)) \ cl(B_2)) ∩ cone(A)` with

- (i) `R_{++}(D_1 ∪ D_2) ∪ {0} ⊇ cl(R_{++}(B_2)) ∩ cone(A)`;
- (ii) `td ∉ cl(B_2) ∩ cone(A)` for `d ∈ D_1` and `0 ≤ t < 1`;
- (iii) `σ_{D_c}(d) > 1` on `D_1` and `σ_{D_c}(d) > 0` on `D_2`.

Then a CGF generates `c^T x ≥ 1` or a cut that dominates it.

**Claim 4.4a (refuted as printed; computed exactly,
`code/check_ky_cor312_counterexample.py`).** The printed Cor. 3.12 is false.
Both counterexamples have `A = I` (2×2) and `c = (1, 1)`. They use one fact:
for `A = I` in `R^2`, every nonzero point `y` of `cl(R_{++}(B_2)) ∩ R^2_+`
lies on a coordinate axis. Indeed, write `y = lim t_n b_n` with `t_n > 0` and
`b_n ∉ R^2_+`. Along a subsequence, either all `b_{n,1} < 0` or all
`b_{n,2} < 0`, so `y_1 ≤ 0` or `y_2 ≤ 0`. Since `y ≥ 0`, one coordinate is 0.

1. *KY's own Example 4.3* (p. 22): `B_2 = {(1 − 1/√n, −1/n)}`, and
   `cl(B_2) = B_2 ∪ {(1, 0)}`. KY state that
   `cl(R_{++}(B_2)) ∩ cone(A) = cone(e_1)`. Take `D_1 = ∅` and
   `D_2 = {(1/2, 0)}`. The point `(1/2, 0)` is not in `cl(B_2)`: its distance
   to every point of `B_2` is at least `1/8` (for `n ≤ 8` the second
   coordinates differ by `1/n ≥ 1/8`; for `n ≥ 9` the first coordinates differ
   by `1/2 − 1/√n ≥ 1/6`), and its distance to `(1, 0)` is `1/2`. Then (i) holds,
   (ii) is vacuous, and `σ((1/2, 0)) = 1/2 > 0`. The printed corollary says
   that `c` is generated. KY prove in the same example that it is not.
2. *sfree Proposition 2(b)*: `B = {q ≤ 0}` with
   `q(λ) = λ_1 − λ_1^2 + (1 − λ_2)^2`. Take `D_1 = ∅` and
   `D_2 = {(1/2, 0), (0, 1/2)}`. Here `q(1/2, 0) = 5/4` and `q(0, 1/2) = 1/4`,
   so neither point lies in `B ⊇ cl(B_2)`. By the fact above, (i) holds, and
   `σ = 1/2 > 0` on `D_2`. A CGF `ρ` generating `c` gives `ρ(e_j) ≤ 1` and
   `ρ ≥ 1` on `B`, so by §4.1 the set `{ρ ≤ 1}` is S-free and attains
   `z_K = 1`. Proposition 2(b) shows that no S-free set attains it.

*Where KY's proof breaks.* KY prove Cor. 3.12 by applying Prop. 3.11 to
`D_1 ∪ D_3`, where `D_3` rescales each `d ∈ D_2 \ R_{++}(D_1)`. The extracted
formula is garbled; the reading consistent with Prop. 3.11(iii) is
`d ↦ 2d/σ_{D_c}(d)`, which has `σ = 2 > 1`. Prop. 3.11(ii) then requires the
segment `[0, 2d/σ(d))` to avoid `cl(B_2)`. In Example 4.3, `2d/σ(d) = (2, 0)`,
and the segment contains `(1, 0) ∈ cl(B_2)`.

**Corrected form (Cor. 3.12').** Replace the condition on `D_2` by
`D_2 ⊆ {d ∈ cl(R_{++}(B_2)) ∩ cone(A) : td ∉ cl(B_2) for all t > 0}`, that is,
the ray of each `D_2` point avoids `cl(B_2)`. Then each rescaled point
`2d/σ(d)` satisfies Prop. 3.11(ii) and (iii), `R_{++}(D_1 ∪ D_3) =
R_{++}(D_1 ∪ D_2)`, and KY's one-line proof goes through. *Status:* proved,
given KY Prop. 3.11 (p. 15). I read the statement of Prop. 3.11 and the
proofs of Props. 3.6 and 3.8, but not every step of the proof of Prop. 3.11.
Both counterexamples above violate the corrected hypothesis, as they must. All
uses of Cor. 3.12 below are uses of Cor. 3.12'.

**Remark 4.4 (Theorem 1(2) from Cor. 3.12').** Let `w > 0`, `z < ∞`,
`ε ∈ (0, 1)` and `c = w/((1 − ε)z)`. The cut `c` is valid.

- *Choice of `D_1`, `D_2`.* For each ray `ℓ = R_{++}d` of
  `cl(R_{++}(B_2)) ∩ cone(A)`:
  - if `ℓ` meets `cl(B_2)`, put the point `t_0 d` with the smallest such
    `t_0 > 0` into `D_1` (it exists because `cl(B_2)` is closed and avoids 0);
  - otherwise put `d` into `D_2`.

  This gives (i) and (ii). Every `D_2` point lies on a ray that avoids
  `cl(B_2)`, which is the hypothesis of Cor. 3.12'.
- *Condition (iii) on `D_1`.* A point `d ∈ D_1` lies in
  `cl(B_2) ∩ cone(A) ⊆ B ∩ cone(A)`. Every `μ ≥ 0` with `Aμ = d` lies in `X`,
  so `σ_{D_c}(d) = min{c^T μ : Aμ = d, μ ≥ 0} ≥ 1/(1 − ε) > 1`.
- *Condition (iii) on `D_2`.* For `d ∈ D_2 \ {0}` in `cone(A)`, the minimum
  is positive, because `c > 0` and `μ ≠ 0`.

Cor. 3.12' then gives a cgf `ρ` with `ρ(p_j) ≤ c_j` and `ρ ≥ 1` on `B`. By §4.1,
`z_V(w) ≥ (1 − ε)z`. Letting `ε → 0` gives Theorem 1(2).

*Infinite case.* If `z_K = ∞`, then `X = ∅`, so `B ∩ cone(A) = ∅`. Hence
`B_1 = ∅`, `cl(B_2) = B` misses `cone(A)`, `D_1 = ∅`, and every ray goes into
`D_2`. Every `c` is valid, since `X = ∅`. The same argument with `c = w/M`,
for any `M > 0`, gives a cgf `ρ` with `ρ(p_j) ≤ w_j/M`, so `α_j ≥ M/w_j` by
§4.1 and `z_V(w) ≥ M`. Since `M` is arbitrary, `sup_V z_V(w) = ∞ = z_K`.
(Before review round 2 this paragraph used `c = Mw`, which gives only
`z_V(w) ≥ 1/M`.) This assumes that KY's results allow `S(A, R^n_+, B) = ∅`. I found no
exclusion in the draft, and in any case the sfree note's direct proof covers
this case.

The sfree note's three-line proof (`T_ε + δB`) is simpler and self-contained.
I would keep it and cite CWY, Kılınç-Karzan–Steffy Prop. 5 (cone case) and
Kılınç-Karzan–Yang.

**The equality case.** For a closed `S` and `c ≥ 0`, the necessary conditions
of KY Prop. 4.3 are vacuous:

- a point `d ∈ cl(B_2) ∩ cone(A)` lies in `B_1`, so `σ_{D_c}(d) ≥ 1`;
- `σ_{D_c} ≥ 0` on `cone(A)`.

Their sufficient condition (Cor. 3.12') needs strict inequalities: `σ > 1` at
the first points of `cl(B_2)` on rays in `cone(A)`, and `σ > 0` on the other
limit directions. With `c = w/z_K` exactly, two kinds of equality case can
occur:

- `σ_{D_c}(d) = 1` at a limit point `d` that is a corner minimizer;
- `σ = 0` along a direction with `w_j = 0`.

KY already treat this gap by examples (draft pp. 21–23). Their Examples 4.3
and 4.5 show that the strict inequalities cannot be dropped, and Examples 4.2
and 4.4 show that they are not necessary either. KY write: "The main
difference in these examples is in the way the sequence of points in `B_2`
approach to a point in `cone(A)`" (p. 21). The sfree results relate to this as
follows.

- **Prop. 2(b)** (non-attainment, `w > 0`). The minimizer `(0, 1)` is a limit
  of the points `(−s², 1 − s)` of `S` outside `R^2_+`, which approach it
  tangentially to the ray `e_2`, and `σ = 1` there. This is **KY Example 4.3
  with the coordinates swapped** (their points `(1 − s, −s^2)`, `s = 1/√n`,
  accumulate at `e_1`). The sfree version replaces the discrete sequence by a
  quadratic sublevel set with interior. It adds nothing in substance to KY's
  example.
- **Prop. 2(a)** (`w_1 = 0`). `S` approaches the ray `e_1` from outside the cone
  along the zero-cost direction (`σ = 0`). This is the mechanism of the CCDLM
  variant of Ex. 6.1 and of KY Example 4.5 (`B_2 = {(n, −1/n)}`, `c = (0, 1)`).
  Here `X = ∅`; KY Ex. 4.5 has `X ≠ ∅`.
- **Theorem 1(4)** (attainment for `S = {q ≤ 0}` with any `q ∈ C^1`, when
  every minimizer satisfies `∇q(t*)^T(x̄ − t*) > 0`). This is a general
  sufficient condition in the equality case `σ = 1`. It formalizes the
  transversal approach of KY Example 4.2. In Prop. 2(b) the approach is
  genuinely tangential: at `t* = (0, 1)`, `∇q(t*) = (1, 0)` and
  `∇q(t*)^T(x̄ − t*) = 0` (in `λ`-coordinates, `x̄ ↔ 0`). For the discrete KY
  Examples 4.2 and 4.3 the hypothesis is not informative, because any `C^1`
  description has `∇q(t*) = 0` (next sentences). I found no general statement of this kind in KY or
  elsewhere; KY give only the pair of examples. Theorem 1(4) does not cover
  KY Example 4.2 literally: if a discrete closed set equals `{q ≤ 0}` near an
  accumulation point `t*`, with `q ∈ C^1`, then `q = 0` on the set and `q > 0`
  off it near `t*`, so `t*` is a local minimizer of `q`, `∇q(t*) = 0`, and the
  transversality hypothesis fails. The analogy is in the mechanism, not in
  the hypotheses.

  *Exact check* (`code/check_ky_gap_thm14.py`, `logs/check_ky_gap_thm14.log`).
  At the Theorem 14 corner, `t* − s̄ = P(1/2, 1/2, 0)` lies in `cone(P)` with
  cost exactly `z_K = 1`. Along the outward normal `n = (−18, −60, −18)` of
  the face `cone{p_1, p_2}`, `q(t* + εn) = 18ε(−60ε − 11) < 0`, so points of
  `int S` outside the cone accumulate at `t*`; thus `t* − s̄ ∈ cl(B_2)`. On the
  segment, `q(s̄ + τ(t* − s̄)) = 3(1 − τ)/2 > 0` for `τ < 1`, so `t* − s̄` is
  the first point of `cl(B_2)` on its ray. Under Cor. 3.12' this ray cannot
  carry a `D_2` point, and by (ii) its only admissible `D_1` point is
  `t* − s̄`, where `σ = 1`. So Cor. 3.12' does not apply, and KY's necessary
  conditions are vacuous. Yet `∇q(t*)^T(s̄ − t*) = 3/2 > 0`, and `t*` is the
  unique minimizer, so Theorem 1(4) gives attainment (by a set outside both
  orbit families, Theorem 14). This inference needs the corrected reading:
  under the printed reading one could put `(t* − s̄)/2` into `D_2`.

**Revised status of Theorem 1.**

- (1), (3): standard (CCDLM Thm. 4.3).
- (5): close to Kılınç-Karzan–Steffy Cor. 2 (relaxed CGFs, no assumptions);
  with genuine S-free sets it follows from (2). Folklore.
- (2): derivable from Cor. 3.12' (the corrected form of an unpublished draft's
  corollary, resting on its Prop. 3.11), and known in the cone case (CWY;
  Kılınç-Karzan–Steffy Prop. 5). The sfree proof is self-contained.
- (4): a general sufficient condition for attainment in the equality case,
  for `S = {q ≤ 0}` with any `q ∈ C^1`. KY Examples 4.2 and 4.3 already show,
  by example, that the manner of approach decides attainment. No general
  statement found. It is elementary.

## 5. Bienstock–Chen–Muñoz and the orbit parametrization

### 5.1 What BCM prove (arXiv:1610.04604 v7)

| Locator (v7) | Statement | Note |
|---|---|---|
| Thm. 15, Cor. 16, Cor. 18 (§4.2) | Full-dimensional maximal outer-product-free (OPF) sets are convex cones | Scout's "Thm 4.3" (KB numbering) |
| Thm. 19 (p. 20) | The halfspace `⟨A, X⟩ ≥ 0` is maximal OPF iff `A` is NSD | Scout's "Thm 4.7" |
| Lemma 22, Thm. 23 (pp. 21–22) | For a 2×2 submatrix `[[a, b], [c, d]]` and unit `λ`, (14a) `λ_1(a + d) + λ_2(b − c) ≥ ‖(b + c, a − d)‖` and (14b) are OPF. Thm. 23 lists maximal cases; (iv)/(viii): all `λ` when no entry is diagonal | The non-symmetric-minor case is the determinant set `ad = bc` |
| Lemma 24 and Remark (pp. 23–24) | `λ = (ā + d̄, b̄ − c̄)/‖·‖` puts `X̄` in the interior; "the λ choices are ... the best possible ... in a violation sense, and may not translate to finding the deepest cut" | The point rule of MS/SCIP, flagged as possibly suboptimal for depth |
| Cor. 25, Lemma 26, Thm. 27 (pp. 24–25) | `S^{n×n}_+` is maximal OPF iff `n ≤ 2`; in `S^{2×2}` the maximal OPF sets are the PSD cone and halfspaces with NSD normal | Scout's "Thm 4.10, 4.15" |
| §5.1–5.3 (pp. 25–28) | "How to select appropriate outer-product-free sets": oracle ball, halfspaces ("best possible cut from this maximal halfspace is ..."), 2×2 cones with the Lemma 24 `λ` | The only "best cut" statements concern halfspaces, where the cut is the reversed halfspace |
| §7 (p. 37) | Conclusions | No selection theory |
| Chmiela et al., ZIB 20-29, §3.1 (p. 14) | For implied minors with distinct indices, the `C_λ`-based set "is exactly one of the maximal outer-product-free sets constructed by Bienstock et al." | — |

**Optimality results for OPF sets.** BCM prove maximality and the 2×2
classification. Their only cut-optimality claims are for halfspace sets. For
the 2×2 cone family they choose `λ` by violation and say explicitly that this
may not give the deepest cut. I found no later result on optimal OPF cuts.
The papers citing BCM (§2.1) do not address it.

### 5.2 Proposition B (BCM's family is the rotation part of the orbit)

**Proposition B** (proved; the identities in the proof are checked exactly by
`code/check_bcm_orbit.py`). For `M = [[a, b], [c, d]]` write
`C_F = {M : sym(F^T M) ⪰ 0}` (sfree Lemma 10), and let
`G_t = [[cos t, sin t], [−sin t, cos t]]`.

1. `sym(G_t M) ⪰ 0` holds iff
   `cos t (a + d) − sin t (b − c) ≥ ‖(b + c, a − d)‖`. This is BCM's (14a) with
   `λ = (cos t, −sin t)`. So the (14a) sets are exactly the orbit sets `C_F`
   with `F^T = G_t ∈ SO(2)`.
2. Let `F` be invertible and not a scalar multiple of a rotation. Then `C_F` is
   not a (14a) set for any unit `λ`.
3. If `det F > 0`, then `C_F` is not contained in any (14b) set; in particular
   it is not a (14b) set.

*Proof.* (1) A symmetric 2×2 matrix is PSD iff its trace is at least the norm
of (difference of diagonal entries, twice the off-diagonal entry).

- `tr sym(G_t M) = cos t (a + d) + sin t (c − b)`.
- The traceless part has squared norm
  `(cos t (a − d) + sin t (b + c))² + (cos t (b + c) − sin t (a − d))² = (a − d)² + (b + c)²`.

(2) Put `A = F^T`, so `C_F = C'_A := {M : sym(AM) ⪰ 0}`, and let
`J = [[0, 1], [−1, 0]]`. The lineality space of the closed convex cone `C'_A`
is `C'_A ∩ (−C'_A) = {M : sym(AM) = 0} = {M : AM ∈ span(J)} = span(A^{-1}J)`,
a line. By (1), each (14a) set is `C'_G` for a rotation `G`, with lineality
space `span(G^{-1}J)`. If `C'_A = C'_G`, the lineality spaces agree, so
`A^{-1}J = μ G^{-1}J` for some `μ ≠ 0`. Since `J` is invertible,
`A = μ^{-1} G`, and `F = μ^{-1} G^T` is a scalar multiple of a rotation, a
contradiction. (For 2×2 matrices `−G_t = G_{t+π}`, so "scalar multiple" and
"positive multiple" of a rotation mean the same.)

(3) The map `M ↦ sym(AM)` is a linear surjection onto the symmetric 2×2
matrices: its 3×3 minors are `±(entry of A)·det(A)/2`, not all zero. So
`int C'_A = {M : sym(AM) ≻ 0}`, which contains `A^{-1}` and is nonempty. For
any `N ∈ R^{2×2}` write `N = sym(N) + kJ`; then
`det N = det sym(N) + k^2`. Hence `sym(AM) ≻ 0` implies `det(AM) > 0`, and
`det M = det(AM)/det A > 0` when `det F > 0`. So
`int C_F ⊆ {ad − bc > 0}`. BCM's proof of Lemma 22 (v7 p. 21) shows that
every (14b) set lies in `{‖(b + c, a − d)‖ ≥ ‖(a + d, b − c)‖} = {ad ≤ bc}`.
Hence `C_F` is contained in no (14b) set. ∎

*Example.* `F^T = diag(2, 1/2)` illustrates (2) and (3). Every (14a) set is
invariant under `(b, c) ↦ (−c, −b)`, because `b − c` and `|b + c|` are
unchanged. But `M_1 = [[1, 0], [3, 1]]` is in `int C_F`
(`det sym(F^T M_1) = 7/16`), while its image `M_2 = [[1, −3], [0, 1]]` is not
(`det = −8`). And `M_1` lies in no (14b) set, since
`3λ_1 ≤ 3 < √13 = ‖(a + d, b − c)‖`. (In round 0 this example was the only
argument for (2) and (3); review round 1, issue M3.)

In the sfree note's determinant model `M(x, y, w; h) = [[w, x], [y, h]]`,
`S = {w ≤ xy}` is one side of BCM's minor equation `ad = bc`. The (14a) sets
are therefore the one-parameter rotation subfamily of the three-parameter
orbit `{C_F : det F > 0}`. In this light, the sfree note's §8 results read as
follows:

- the explicit orbit (Lemma 10(2)), completion = upward closure (Lemma 10(4)),
  quasiconvex best-orbit computation (Prop. 12), tangent-edge rigidity
  (Lemma 13) and the certified obstruction (Theorem 14, Prop. 16) extend BCM's
  family. No prior statement of any of these was found;
- the old audit's remark that the tangent-edge question for implied minors was
  "not checked" stands; it is the topic of the `minor-sets/` stream.

## 6. Solver relevance baseline (SCIP)

| Fact | Source and locator |
|---|---|
| Quadratic intersection cuts introduced with the quadratic nonlinear handler, "currently disabled" | SCIP `CHANGELOG`, release notes 8.0.0 (line 1681 of the 10.0.3 file); SCIP 8 report, arXiv:2112.08872, §4.3.1 (p. 43) and §4.3.3 (p. 44) |
| `sepa_interminor` (minor intersection cuts) disabled by default | SCIP 8 report §4.11 (p. 55); `sepa_interminor.c`: `SEPA_FREQ -1` |
SCIP 8 leaves these dense cuts disabled because their net benefit is unclear.
| Monoidal strengthening added in 9.0; still "currently disabled by default"; "the strengthened intersection cuts significantly outperform the pure intersection cuts whenever monoidal strengthening can be applied" | SCIP 9 report, arXiv:2402.17702 v2, §3.2.2 (p. 10); `CHANGELOG` 9.0.0 (lines 1027, 1190–1193) |
| SCIP 10.0 report: no mention of quadratic intersection cuts | arXiv:2511.18580 v1 (grep count 0) |
| Defaults in 10.0.3: `useintersectioncuts FALSE`, `usestrengthening FALSE`, `usemonoidal TRUE`, `useboundsasrays FALSE`, `sparsifycuts FALSE`; also switched off in sub-SCIPs | `nlhdlr_quadratic.c` lines 78–85 and 3934–3936; PySCIPOpt 6.2.1 (`logs/scip_source_grep.log`) |
| No option to choose the S-free set; one Muñoz–Serrano set per cut, with the eigenvector-based `λ` | Chmiela et al., ZIB 20-29, Remark 3 (p. 11: other factorizations "can potentially lead to other maximal quadratic-free sets"), §3 Cases 1–4 |

**The published computational evaluation** (Chmiela–Muñoz–Serrano, ZIB-Report
20-29, §5, pp. 26–28; the Math. Program. 197 version was not accessible and
may differ):

- Setup: root-node experiments in "a development version of SCIP with CPLEX
  12.10.0.0", one-hour limit. The test set is the 587 MINLPLib instances (out
  of 705 nonconvex instances with a quadratic constraint) that have a primal
  and a dual bound and no failure.
- Mean gap closed (Table 1): DEFAULT 0.56; ICUTS 0.61 (rel. 1.08); ICUTS-S
  0.60; MINOR 0.59; ICUTS+MINOR-B 0.62 (rel. 1.09). On affected instances:
  0.52 versus 0.60 (rel. 1.15). The text says "an improvement of 8% in the gap
  closed. This improvement becomes 12% if we restrict to affected instances".
- Root solves: 90 (DEFAULT) versus 117 (ICUTS+MINOR-B), that is, 27 more.
- Strengthening has "a (slightly) negative effect", attributed to density.
- Branch-and-bound: only "preliminary experiments". With strengthening, about
  10% fewer LP iterations per second; without it, 4% fewer. No node or time
  comparison is reported.
- Final remarks (p. 29): full incorporation into spatial branch-and-bound "will
  require a much more careful handling of the density of the cuts we create, as
  well as special cut selection rules".

**In-house data** (not published; `research-20260922/scouting/brainstorm2-solvercore.md`,
probe D). With monoidal strengthening, intersection cuts gave +7.6 percentage
points of root gap on average over 140 instances. On 54 full solves the total
node ratio was 0.974, with large swings in both directions.

**Correct baseline statement.** In SCIP the cuts are off. The stated reasons
are density and the lack of a rule for when they help, not weakness of the
cuts. In the sources I could read, the only published evidence is root gap
closed, and there is no branch-and-bound comparison: ZIB 20-29 gives only
preliminary LP-speed remarks. The computations of the monoidal paper (which
the SCIP 9 report cites for "significantly outperform") and the Math. Program.
197 version of Chmiela et al. were not accessible, so a branch-and-bound
comparison there cannot be excluded. Serrano's MIP 2022 slides on monoidal
strengthening (`sources/serrano-mip2022-monoidal-slides.pdf`, slide 25) list
the SCIP implementation as "current and future work" and contain no
computations. A better choice of S-free set (the sfree
results) addresses cut strength, not density. Solver relevance would need a
selection rule that changes the on/off trade-off in branch-and-bound. The
`scip-set-selection/` stream is testing that. The sfree note's §9 numbers are
single-cut and root-loop prototypes outside SCIP.

## 7. Revised novelty assessment, result by result

"Not found" means: not found in the sources of Sections 2–6 and the searches
in `logs/`. It does not mean new.

| Result (sfree note) | Closest prior work (locator) | Verdict |
|---|---|---|
| **Thm 1(1), (3)** existence, Zorn | CCDLM Thm. 4.3 (preprint p. 11) | Standard; cite |
| **Thm 1(2)** sup over S-free sets = `z_K` for `w > 0` | CWY Thm. 1.1 and Kılınç-Karzan–Steffy Prop. 5 (p. 11) (exact, if `S − x̄ ⊆ cone R`); CCDLM Thm. 6.3 (if `cone R = R^k`); the corrected Kılınç-Karzan–Yang Cor. 3.12' (draft) implies it (Remark 4.4); Glover 1973 Remark 1 (trivial case `S ⊆` cone) | Known or derivable; present as background with these citations |
| **Thm 1(4)** attainment criterion (transversality at every minimizer, any `q ∈ C^1`) | KY Examples 4.2 (transversal approach, attained) and 4.3 (tangential, not attained), pp. 21–22; KY's corrected Cor. 3.12' and Prop. 4.3 do not decide the Theorem 14 corner (Section 4.4) | General sufficient condition not found; modest; present it as formalizing KY's Ex. 4.2/4.3 distinction and cite them |
| **Thm 1(5)** closure = `cl(conv X + R^N_+)` | Follows from (2); Kılınç-Karzan–Steffy Cor. 2 (p. 10; relaxed CGFs, no assumptions); CWY | Folklore; cite Kılınç-Karzan–Steffy |
| **Prop 2(a)** zero reduced cost | CCDLM §6, variant of Ex. 6.1 (HAL p. 25); KY Ex. 4.5 (p. 23) | Same mechanism; must cite CCDLM and KY |
| **Prop 2(b)** non-attainment with `w > 0` | KY Example 4.3 (p. 22): the same parabola `(1 − s, −s^2)` with coordinates swapped, discrete instead of a sublevel set | Known example (KY); cite it; the sfree version is a quadratic restatement |
| **Lemma 3** (`≤ rank P` rays) | Basic solutions / Carathéodory | Classical |
| **Thm 4** (inertia bound `ρ(q)`) | Second-order necessary conditions; support bounds for local solutions of standard QPs (Bomze 1998; Chen–Peng–Zhang, Math. Program. 141, 2013; Hager–Pardalos–Roussos–Sahinoglou, JOTA 68, 1991). None read (paywalled) | Not found in this form; technique standard; the reverse-convex corollary is classical (Tuy) |
| **Thm 5(1)–(3)** polynomial for fixed `r`; normal-fan count; closed forms | Renegar 1992; upper bound theorem; Eckstein–Nediak (the deepest-cut problem in MIP needs `p·2^p` parameters, restricted to pairs, §4.2) | Routine given Lemma 3/Thm 4; not found as a statement about best intersection cuts |
| **Thm 5(4)** NP-hardness and `1/(5k^2)` inapproximability | Motzkin–Straus 1965 (standard QP reduction) | Standard reduction; the transfer to "best single intersection cut" (via Theorem 1) not found |
| **Prop 6, Remark 7** (SCIP's set arbitrarily bad; closure factor → 0) | Qualitative: MS 2022 §6 and Example 9 (dependence on `T`); BCM v7 p. 24 Remark ("may not translate to finding the deepest cut"); Chmiela Remark 3 (p. 11) | Quantitative statements not found; cite the qualitative precedents |
| **Thm 8** (Lorentz orbit reaches all maximal sets in signatures `(n,1)`, `(1,m)`; λ free) | MPS 2025 Thms. 1.1–1.2 (pp. 4–5); MPS 2026 §2.1, Lemma 1 (p. 8); MS 2022 §7 conjecture (arXiv v2, p. 36). MPS do not discuss `m = 1` or group actions, and do not mention the MS conjecture | Not found; a short consequence of MPS plus Möbius 2-transitivity; partly answers MS's conjecture (homogenized-dimension reading) |
| **§6.1** (point rule one-parameter; misses `z_K` numerically) | BCM Lemma 24 Remark (point rule is violation-optimal, not depth-optimal) | The concern was raised by BCM; the analysis and numbers not found |
| **Prop 9** (rank-1 closure ≠ hull, triangle and disk) | Non-finite or slow convergence of pure concavity-cut methods: Zwart 1973 (Oper. Res. 21, 1260–1266), Porembski 2001 (zbMATH review) | Elementary instance of a known phenomenon |
| **Lemma 10** orbit `{sym(F^T M) ⪰ 0 : det F > 0}`; completion = upward closure | BCM (14a) = rotation subfamily (Proposition B); Sturm–Zhang 2003 (rank-one decomposition, not re-read) | Extension of BCM's family; not found |
| **Thm 11** (exact `z_K` for bilinear with `O(N^2)` closed forms) | Konno 1975/76 computes step lengths by LP for a different convex region | Not found |
| **Prop 12** (quasiconvex best orbit cut by 2×2 LMI bisection) | Eckstein–Nediak deepest-cut LPs (MIP, restricted sets) | Not found; standard technique |
| **Lemma 13, Thm 14, Prop 16** (tangent-edge rigidity; certified obstructions) | None | Not found |

## 8. Corrections to earlier notes

These corrections are recorded here; the earlier notes were not edited.

1. **sfree note, Theorem 1 Remark (ii) and §10.2.** Theorem 1 is described as
   the closed-S form of sufficiency "and folklore". Correction:
   - CWY (Math. Program. 152, 2015, Thm. 1.1) is a single-cut dominance
     theorem. It gives exact attainment of `z_K` for every `w ≥ 0` when
     `S − x̄ ⊆ cone(R)`;
   - CCDLM Thm. 6.3 does the same when `cone(R) = R^k`;
   - Kılınç-Karzan–Steffy (Math. Program. 159, 2016, Prop. 5) reprove the
     cone case, and their Cor. 2 gives domination by relaxed CGFs with no
     assumptions, which is close to Theorem 1(5);
   - the corrected form of Kılınç-Karzan–Yang (draft) Cor. 3.12 implies
     Theorem 1(2);
   - Proposition 2(a) uses the mechanism of CCDLM's variant of Example 6.1 and
     of KY Example 4.5, and must cite them.

   Theorem 1(4) remains, as a general sufficient condition in the equality
   case; KY Examples 4.2 and 4.3 already illustrate the distinction it
   formalizes.
1a. **sfree note, Section 10.2, "The attainment criterion (4) and the examples
   of Proposition 2 are elementary; I did not find them stated".** Proposition 2(b) is KY Example 4.3 (draft p. 22)
   with the coordinates swapped. (This correction is new in revision round 1;
   the round-0 version of this note also missed it.)
2. **sfree note §10.2, "deeper cuts" paragraph.** Eckstein–Nediak (Ann. Oper.
   Res. 139, 2005) were missing. They formulate a deepest-cut generation
   problem over S-free sets for MIP, which is the closest precedent for
   best-cut selection. Glover 1973 and Konno 1976 were read: they define the
   same coefficient-wise strength order, but have no set-selection theory for
   quadratic sets.
3. **sfree note §10.1 and the scout report §1.3: Porembski references.**
   - "Porembski (JOGO 2001, 2004)" is wrong: the 2004 paper is
     *Operations Research* 52(6), 942–953 ("Cutting planes for low-rank-like
     concave minimization problems").
   - The scout's "Porembski 2004 adds cone adaptation for forced depth"
     conflates two papers: cone adaptation is JOGO 24 (2002) 89–107.
   - The pages of the JOGO 2001 paper differ between Crossref (109–132) and
     zbMATH (113–136); the issue is 20(2).
4. **sfree note §10.2, Balas–Margot.** The paper is Math. Program. 137 (2013)
   19–35 (online 2011). GICs fix the S-free set and tighten the relaxation, then
   choose cuts by an LP over a point-ray collection. That is the axis
   complementary to the sfree note, not "optimizing the cut over a relaxation"
   in the same sense.
5. **sfree note §8 and §10.2, BCM.** The relation is now exact: BCM's (14a)
   sets are the orbit members with `F ∈ SO(2)` (Proposition B). BCM v7 p. 24
   already flags that the violation-maximizing `λ` may not give the deepest
   cut. The note should cite this. It also changes the novelty claim to "the
   three-parameter extension of a known one-parameter family".
6. **Scout report §1.1, BCM theorem numbers** ("Thm 4.3, 4.7, 4.10, 4.15")
   follow the local KB's numbering. In arXiv v7 they are Thm. 15/Cor. 16,
   Thm. 19, Cor. 25 and Thm. 27 (Section 5.1).
7. **sfree note §10.1, Semantic Scholar counts.** The list for arXiv:1911.12341
   now has 17 entries (one new survey). The citations of Chmiela et al., missed
   in September because of rate limits, are listed in §2.1. None concerns set
   selection.
8. **Solver statements** (sfree §5 and §9.4, PROGRAM.md). "Off by default" is
   correct. The published reason is density and the lack of a rule for when
   the cuts help. The only published evaluation I could read is root-node gap
   closed in a development SCIP. Statements about solver relevance should say
   that no branch-and-bound comparison was found in the accessible sources;
   the monoidal paper's computations and the Math. Program. 197 version were
   not accessible.

## 9. Related work any paper on these results must cite

Core:

- Muñoz–Serrano, Maximal quadratic-free sets, Math. Program. 192 (2022)
  229–270 (§6, Example 9, §7).
- Muñoz–Paat–Serrano, A characterization of maximal homogeneous-quadratic-free
  sets, Math. Program. 210 (2025) 641–668; IPCO 2023.
- Muñoz–Paat–Serrano, A characterization of maximal inhomogeneous-quadratic-free
  sets, arXiv:2605.30602 (2026).
- Chmiela–Muñoz–Serrano, On the implementation and strengthening of
  intersection cuts for QCQPs, Math. Program. 197 (2023) 549–586; IPCO 2021;
  ZIB-Report 20-29.
- Chmiela–Muñoz–Serrano, Monoidal strengthening and unique lifting in MIQCPs,
  Math. Program. B 210 (2025) 189–222.
- Bienstock–Chen–Muñoz, Outer-product-free sets for polynomial optimization and
  oracle-based cuts, Math. Program. 183 (2020) 105–148 (Lemma 22–24, Thm. 27,
  the Remark on depth).

Theory of S-free sets and cut-generating functions:

- Balas 1971 (Oper. Res. 19, 19–39).
- Tuy 1964.
- Glover 1973 (Oper. Res. 21, 123–134).
- Conforti–Cornuéjols–Daniilidis–Lemaréchal–Malick, MOR 40 (2015) 276–301.
- Cornuéjols–Wolsey–Yıldız, Math. Program. 152 (2015) 643–651.
- Kılınç-Karzan–Steffy, Math. Program. 159 (2016) 585–605 (Prop. 5, Cor. 2,
  relaxed CGFs).
- Kılınç-Karzan–Yang (draft, rev. 2017), if it has appeared by then: Examples
  4.2–4.5 (Proposition 2(b) is Example 4.3), and Cor. 3.12 with the
  correction of Section 4.4.
- Basu–Conforti–Di Summa survey (Math. Program. 151, 2015).
- Conforti–Cornuéjols–Zambelli, *Integer Programming*, Ch. 6.
- Averkov–Basu–Paat, SIOPT 28 (2018) 904–929 (families and closures).

Deeper or best cuts:

- Konno 1976 (Math. Program. 11, 14–27).
- Sherali–Shetty 1980 (Math. Program. 19, 14–31).
- Porembski 1999 (JOGO 15) and 2008 (NRL 55).
- Eckstein–Nediak 2005 (Ann. Oper. Res. 139, 95–129).
- Balas–Margot 2013 (Math. Program. 137, 19–35) and Kazachkov et al. 2020
  (Math. Program. Comput. 12).

Related S-free constructions:

- Fischetti–Monaci, bilinear-free sets (EJOR 2020).
- Serrano, factorable MINLP (IPCO 2019).
- Towle–Luedtke (MOR).
- Modaresi–Kılınç–Vielma (Math. Program. 155, 2016).
- Xu–Liberti (Math. Program. 2024).
- Xu–Pokutta (arXiv:2608.03318).

Complexity and technique:

- Motzkin–Straus 1965.
- Renegar 1992.
- Sturm–Zhang 2003.
- A support-bound reference for local minimizers of standard QPs (Bomze 1998
  or Chen–Peng–Zhang 2013), after checking that it states what is claimed.

Solver:

- The SCIP 8 report, the SCIP 8 MINLP paper (JOGO 2023) and the SCIP 9 report,
  for the default status.

## 10. Sources that could not be accessed

| Source | Reason | What was used instead |
|---|---|---|
| Tuy 1964 (Doklady / Soviet Math.) | No open copy found | Citations in Glover 1973, Eckstein–Nediak, Towle–Luedtke |
| Sherali–Shetty 1980 (Math. Program. 19) | Springer, paywalled | Title and metadata only |
| Porembski 1999, 2001, 2002 (JOGO), 2004 (Oper. Res.), 2008 (NRL), thesis 1996 | Paywalled or print only | zbMATH summaries and reviews, Crossref abstract (2004) |
| Balas–Margot 2013 (Math. Program. 137) | Paywalled | Kazachkov et al., arXiv:1703.02221 §1–2 |
| Cornuéjols–Wolsey–Yıldız 2015 (journal) and CORE DP 2013/27 | Journal paywalled; UCLouvain host did not resolve | Yıldız thesis Ch. 4 (same result and proof) |
| Eckstein–Nediak 2005 (journal) | Paywalled | RUTCOR RRR 23-2003 rev. (Internet Archive copy of the public report) |
| Chmiela–Muñoz–Serrano, Math. Program. 197 (2023) journal version | Paywalled | ZIB-Report 20-29 (Nov. 2020) |
| Chmiela–Muñoz–Serrano, monoidal (Math. Program. B 210; ZIB report 8913) | Paywalled; ZIB file "access not granted"; no preprint on the authors' publication page (rechecked 2026-10-02) | OPUS abstract; SCIP 9 report summary; Serrano's MIP 2022 slides (no computations) |
| Kılınç-Karzan–Steffy, Math. Program. 159 (2016) journal version | Paywalled | Author draft (rev. Jul. 2015) |
| Chmiela master's thesis (TU Berlin 2020) | Listed without file | — |
| Fischetti–Monaci, EJOR 2020 | ScienceDirect returned HTTP 403 | Descriptions in MPS 2026 and the scout report |
| Chen–Peng–Zhang 2013; Bomze 1998; Hager et al. 1991 | Paywalled | Not used for any claim |
| Rahimian–Mehrotra, SIOPT 2024 | Paywalled | Crossref abstract |
| Google Scholar citation lists | CAPTCHA; not attempted | Semantic Scholar, OpenAlex, OpenCitations |

## 11. Revision after review round 1 (2026-10-02)

Review: [`reviews/review-r1.md`](reviews/review-r1.md), verdict "major
problems". Each issue and how it was handled. Section numbers in this table
are those of the round-1 version: its §11 (Checks actually run), §12 (Limits)
and §13 (Open questions) are now §13, §14 and §15.

| Issue | Handling |
|---|---|
| **M1.** KY Examples 4.2–4.5 missed; Prop. 2(b) is KY Ex. 4.3 with coordinates swapped; KY already show the strict condition cannot be dropped | Accepted and verified against the draft (pp. 21–23). The claims "Prop. 2(b) shows the strict inequality cannot be dropped" and "Prop. 2(b) not found as an example" are withdrawn. Prop. 2(b) is now cited as a quadratic restatement of KY Ex. 4.3, and Prop. 2(a) also as KY Ex. 4.5. The Theorem 1(4) verdict is reduced to "a general sufficient condition formalizing the transversal/tangential distinction of KY Ex. 4.2/4.3". Changed: Summary item 1 and table, §3 KY row, §4.4, §7 rows, §8 items 1 and 1a (new), §9, §13 item 1 |
| **M2.** KY Cor. 3.12 false as printed; the note's §4.4 inference needs a corrected hypothesis | Accepted. Claim 4.4a states the printed corollary and refutes it with two counterexamples (KY Ex. 4.3 with `D_2 = {(1/2, 0)}`; Prop. 2(b) with `D_2 = {(1/2, 0), (0, 1/2)}`), checked exactly by the new `code/check_ky_cor312_counterexample.py`. The corrected form Cor. 3.12' (ray of each `D_2` point avoids `cl(B_2)`) is stated, with the point where KY's proof breaks. Remark 4.4 and the Theorem 14 inference now use Cor. 3.12' explicitly, and the Theorem 14 check adds the exact segment computation `q(s̄ + τ(t* − s̄)) = 3(1 − τ)/2` that makes `t* − s̄` the only admissible `D_1` point |
| **M3.** Proposition B's general claim proved only for one `F` | Fixed with a general proof: lineality spaces for (14a) (any invertible `F` that is not a multiple of a rotation), and `int C_F ⊆ {ad > bc}` versus `(14b) ⊆ {ad ≤ bc}` for (14b) (`det F > 0`), using the identity `det(S + kJ) = det S + k^2`. `check_bcm_orbit.py` Part 3 no longer prints a general conclusion from one witness; new Part 4 checks the identities used |
| **m1.** Wrong DOI for Muñoz–Serrano 2022 in OpenCitations | Rerun with the correct DOI via the new `code/opencitations.py`: 7 citers, all already in §2.1. Old log kept as `logs/opencitations_r0_superseded.log`; §11 corrected |
| **m2.** Kılınç-Karzan–Steffy (Math. Program. 159, 2016) missing | Author draft downloaded and read. Added to §3 (Prop. 3, 4, 5, Cor. 2 with page locators), to the §7 rows for Theorem 1(2) and 1(5), to §8 item 1 and to §9 |
| **m3.** "No published branch-and-bound comparison" too strong | Reworded everywhere (Summary, §6, §8 item 8, §12) to "none in the sources I could read", naming the unread sources. One more search found no open copy of the monoidal paper; Serrano's MIP 2022 slides (saved) contain no computations |
| **m4.** §4.3 tested only part (1) of Proposition A | Added a proof that, for `S = {w ≤ xy}` or `{w ≥ xy}`, part (2) holds iff part (1) does, so the conclusion covers both parts |
| **o1.** Infinite case of Remark 4.4 | Added (`D_1 = ∅`), with the caveat that KY must allow an empty `S(A, R^n_+, B)`. The round-1 text used `c = Mw`, which was wrong; corrected to `c = w/M` in round 2 (Section 12, n1) |
| **o2.** "C^1 quadratic constraints" | Replaced by "`S = {q ≤ 0}` with any `q ∈ C^1`" in §4.4 and §7 |

Further correction found during the revision: the KY page locator for
Prop. 3.11 was p. 14; it is p. 15 (determined from page breaks of the
extracted text).

Unchanged after re-checking: the SCIP baseline facts, the ZIB 20-29 numbers,
the BCM, CCDLM, CWY, Glover and Eckstein–Nediak comparisons, Proposition A,
and the 0/47 and 0/73 counts (rerun, byte-identical).

## 12. Revision after review round 2 (2026-10-02)

Review: [`reviews/review-r2.md`](reviews/review-r2.md), verdict "minor fixes".
The reviewer confirmed the round-1 fixes M1–M3 and m1–m4. Each remaining issue
and how it was handled:

| Issue | Handling |
|---|---|
| **n1.** Infinite case of Remark 4.4: `c = Mw` gives `z_V(w) ≥ 1/M`, not `≥ M` | Accepted. By the §4.1 dictionary, `ρ(p_j) ≤ c_j` gives `α_j ≥ 1/c_j`. §4.4 now uses `c = w/M`, which gives `α_j ≥ M/w_j` and `z_V(w) ≥ M`; the conclusion `sup = ∞` is unchanged. The §11 row o1 is annotated |
| **n2.** No statement about background processes | Added to §13: no background process was started in this revision, and `ps -ef` shows no process of this stream running |
| Optional: "gradient = 0" remark for KY Ex. 4.3 | Applied. The tangency `∇q(t*)^T(x̄ − t*) = 0` is now stated only for Prop. 2(b) (`∇q(0, 1) = (1, 0)`); for the discrete KY Examples 4.2/4.3 the note says the hypothesis is not informative |
| Optional: hand bound printed as if computed | Applied. `code/check_ky_cor312_counterexample.py` now prints the bound as a hand case split and adds a labelled floating-point sanity check (minimum distance 0.187885 over `n ≤ 10^5`, matching the reviewer's 0.1879 for `n < 200`). Log regenerated |
| Optional: OpenCitations self-record | Applied in §13: of the 6 records for Chmiela et al. (`10.1007/s10107-022-01808-5`), one is the paper itself, so it has 5 citing works. No conclusion changes. The log is kept as retrieved |
| Optional: revision log after the closing sections | Applied. The round-1 revision log is now §11 and this section is §12, so the note ends with Checks actually run (§13), Limits (§14) and Open questions (§15) |

No other text changed, apart from the header paragraph and the section numbers.

## 13. Checks actually run

All commands were run from
`research-20261001/intersection-literature/code/` (or with paths as shown),
with `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1` for the Python computations.
They are targeted checks for this stream only. No project-wide verification was
run, and CI was not consulted.

| Command | Outcome |
|---|---|
| `python3 openalex_citers.py W2990328892 W4288017533 W4226106437 W3123307255 W4377200032 W4398236802 W4308827732 W7163048902 W4377200016 W4400413373 W2533553031 > ../logs/openalex_citers.jsonl` | 70 citation records; no set-selection paper |
| `curl https://api.opencitations.net/index/v2/citations/doi:<DOI>` for six DOIs (round 0, shell loop) | Superseded: the Muñoz–Serrano 2022 DOI was mistyped (`…-x`), giving 0 citers; kept as `logs/opencitations_r0_superseded.log` |
| `python3 opencitations.py 10.1007/s10107-021-01738-8 10.1007/s10107-021-01738-x 10.1007/s10107-022-01808-5 10.1007/s10107-024-02092-1 10.1007/s10107-024-02112-0 10.1007/s10107-020-01484-3 10.1007/978-3-030-45771-6_24 > ../logs/opencitations.log` (revision round 1) | Correct MS 2022 DOI: 7 citers (signomial cuts SIOPT, Del Pia SIOPT, Xu–Liberti, monoidal IPCO, MPS IPCO, Chmiela et al., MPS journal; titles in `logs/opencitations_r1_titles.log`), all already in §2.1; mistyped DOI 0; others 6, 0, 0, 22, 12, as in round 0 where queried. Nothing new. Round 2: the 6 records for Chmiela et al. (`…01808-5`) include the paper itself, so it has 5 citing works |
| `python3 s2_citers.py arXiv:1911.12341 …` | **Failed**: HTTP 429 on every retry (`logs/s2_api_rate_limited_err.log`) |
| WebFetch of the Semantic Scholar citation endpoints (8 papers) | 7 lists retrieved, 2 IDs returned 404, keyword endpoint 429 (`logs/s2_citations_via_webfetch.md`) |
| `python3 arxiv_search.py '<10 queries>'` and two title-lookup runs | `logs/arxiv_searches.log`, `logs/arxiv_title_lookup.log`, `logs/arxiv_title_lookup2.log`, `logs/arxiv_stqp.log` |
| `python3 crossref_lookup.py '<17 references>'` | `logs/crossref_lookup.log` (volume and pages used above) |
| Crossref abstract loop (12 DOIs) | `logs/crossref_abstracts.log`; only 2 abstracts present |
| `python3 openalex_oa.py <20 DOIs> > ../logs/openalex_oa.jsonl`; `python3 openalex_abstract.py <13 DOIs>` | OA status (found the CCDLM HAL copy); abstracts mostly absent |
| `python3 zbmath_lookup.py '<queries>'` | `logs/zbmath_lookup.log`: Porembski reviews found; Tuy queries returned 404 |
| 28 WebSearch queries, WebFetch of listed pages | `logs/web_searches.md` |
| Revision round 1: 2 WebSearch queries, 1 WebFetch, 2 curl downloads | `logs/web_searches.md` (rows R1–R2): Kılınç-Karzan–Steffy author draft found and read; no open copy of the monoidal paper; Serrano MIP 2022 slides have no computations |
| `bash scip_defaults.sh` | `logs/scip_source_grep.log`: `DEFAULT_USEINTERCUTS FALSE`, `DEFAULT_USESTRENGTH FALSE`, `DEFAULT_USEMONOIDAL TRUE`; PySCIPOpt 6.2.1 reports the same; changelog lines 1027, 1190–1193, 1635, 1681, 2306 |
| `python3 check_bcm_orbit.py` (rerun in revision round 1 with the new Part 4) | `logs/check_bcm_orbit.log`: Part 1 both identities True (sympy); Part 2: 0 disagreements in 20000 random tests; Part 3 (one witness, labelled as such): `M_1` in `int C_F` (det 7/16), `M_2` not (det −8), `M_1` in no (14b) set; Part 4: the 3×3 minors of `M ↦ sym(AM)` are `(−r, p, s, −q)·det(A)/2`, `sym(A·A^{-1}J) = 0`, and `det(S + kJ) − det S − k^2 = 0` |
| `python3 check_ky_gap_thm14.py` (rerun in revision round 1) | `logs/check_ky_gap_thm14.log`: `λ(t*) = (1/2, 1/2, 0)`, cost 1; `q(t* + εn) = 18ε(−60ε − 11)`; exact points at `ε = 10^-3, 10^-6` with `q < 0` and a negative barycentric coordinate; new line `q(s̄ + τ(t* − s̄)) = 3/2 − 3τ/2`; `∇q(t*)^T(s̄ − t*) = 3/2` |
| `python3 check_ky_cor312_counterexample.py` (new in revision round 1; changed in round 2 and rerun as `OMP_NUM_THREADS=1 timeout 300 python3 check_ky_cor312_counterexample.py > ../logs/check_ky_cor312_counterexample.log`) | `logs/check_ky_cor312_counterexample.log` (regenerated in round 2, exit 0): Example 1 (KY Ex. 4.3): `(1/2, 0)` at distance `≥ 1/8` from `B_2` by a hand case split, now printed as such, with a floating-point sanity check giving minimum distance 0.187885 over `n ≤ 10^5`; `σ = 1/2`; `2d/σ = (2, 0)`. Example 2 (Prop. 2(b)): `q(1/2, 0) = 5/4`, `q(0, 1/2) = 1/4`, `σ = 1/2`; `q(−s^2, 1 − s) = −s^4` for `s = 1/10, 1/1000`; `σ((0, 1)) = 1` |
| `python3 cone_span_mccormick.py 11 150 4 4 3` (rerun in revision round 1) | `logs/cone_span_mccormick_11.log`: n = 47 (matches the sfree note), `cone(P) = R^3` in 0; rerun output byte-identical (`cmp`) |
| `python3 cone_span_mccormick.py 12 200 6 8 4` (rerun in revision round 1) | `logs/cone_span_mccormick_12.log`: n = 73 (matches), `cone(P) = R^3` in 0; rerun output byte-identical (`cmp`) |
| `pdftotext -layout`, `ps2pdf`, `grep`/`awk` locator extraction on files in `sources/` | Locators quoted in Sections 3–6 |
| `sha256sum` (in the manifest script) | `sources/MANIFEST.md`; the ZIB 20-29 copy is byte-identical to the scout's copy |
| `sha256sum sources/kilinc-steffy-sublinear-draft-web.pdf sources/serrano-mip2022-monoidal-slides.pdf` (revision round 1) | Hashes recorded in the manifest addendum |
| Revision round 2: `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 timeout 300 python3 check_ky_gap_thm14.py` and `… check_bcm_orbit.py`, output compared with `cmp` against `logs/` | Both exit 0; output byte-identical to the logs (scripts unchanged) |
| Revision round 2: `ps -ef \| grep intersection-literature` before returning | No process of this stream running |

**Background processes.** In revision round 2 every computation ran in the
foreground under `timeout 300`, and no background process was started. The
earlier rounds left none running: `ps -ef` before returning showed no process
of this stream (the reviewer of round 2 found the same).

## 14. Limits

- **Coverage of the searches.** Citation databases lag. Semantic Scholar was
  reached only through WebFetch, whose summarizing model transcribed the JSON;
  a dropped entry cannot be excluded. Google Scholar was not used. Springer,
  INFORMS and Elsevier full texts were not read. Conference talks, theses
  without files, and work in progress cannot be found this way.
- **Primary sources not read.** For Tuy, Sherali–Shetty, Porembski, Balas–Margot
  and the journal versions of Chmiela et al. and of the monoidal paper, the
  comparisons rest on secondary descriptions, abstracts or titles. The CWY
  comparison uses the thesis chapter, not the journal text, and the
  Kılınç-Karzan–Steffy comparison uses the author draft. The
  Kılınç-Karzan–Yang comparison uses an unrefereed draft whose Cor. 3.12 is
  false as printed. Remark 4.4 and the Theorem 14 inference use the corrected
  form Cor. 3.12', which rests on KY Prop. 3.11; I did not check every step of
  that proof. A later version of KY may have fixed the corollary; none was
  found.
- **Theorem 4.** I could not read the standard-QP support-bound papers that the
  reviewer cited from memory, so the "standard technique" verdict is my own
  assessment.
- **Proposition A** is not new and has no effect on the LP corners studied.
  The `cone(P) = R^3` test is LP-based with tolerance `10^-9`, and its
  explanation is heuristic. The equivalence of its parts (1) and (2) for
  bilinear `S` is proved (Section 4.3).
- **Solver baseline.** "No branch-and-bound comparison" refers only to the
  sources I could read.
- **Novelty.** The verdicts "not found" are only that. Concurrent work by the
  MPS group, which maintains SCIP's implementation, is the main risk.

## 15. Open questions

1. Is there a characterization of attainment in the equality case that covers
   both Theorem 1(4) and Kılınç-Karzan–Yang's corrected strict conditions? For
   example: attainment holds iff no corner minimizer is a tangential limit of
   outside points. KY Examples 4.2/4.3 and Proposition 2(b) suggest that the
   tangential case is the only obstruction for quadratics. KY also leave the
   gap between their sufficient and necessary conditions open.
2. Does the Eckstein–Nediak deepest-cut formulation (sets `X(d)` built from
   supporting hyperplanes at points of `S`) give a computational route to
   `z_K`-attaining maximal sets for quadratic `S`, beyond the orbit family?
   For quadratic `S`, `d(y)` would be the normal of a supporting hyperplane at
   `y ∈ ∂S`.
3. Have the Math. Program. versions of Chmiela et al. (2023) and of the monoidal
   paper (2025) published branch-and-bound comparisons that change the solver
   baseline? Answering this needs library access.
4. Does BCM's violation-maximizing `λ` (their Lemma 24) lose a factor against
   the best rotation member, or against the full orbit, on implied-minor
   corners, as Proposition 6 shows for quadratic constraints? This belongs to
   the `minor-sets/` stream.
