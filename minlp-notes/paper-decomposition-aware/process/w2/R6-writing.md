# R6 — Writing quality and structure

Reviewer role: writing quality and structure for an expert reader (MP / SIOPT / MOR).
Snapshot: sources as of 2026-10-03 01:20 EDT. The paper was being edited during the
review. New files appeared while I was reading (`growth-sharp.tex`,
`setting-growthcert.tex`, `exact-localized.tex`, `appendix-localized.tex`, a new
Recourse subsection in `computation.tex`). I read them, but line numbers below
refer to the files as they were at 01:20 and may shift. Every finding also names a
label or a quoted phrase, so it can be found again.

Checks run (targeted, exact arithmetic):
`python3 process/w2/checks/r6_examples.py` (graded-grid counterexample after
Prop. `prop:tu-misaligned`, Example `ex:tu-sum`). Every quoted number was confirmed: two
11-node grids that share only {0,1}; corrected values 21/8, 31/64, 51/64 and
175/64 (times L). I also checked Example `ex:cr-star32` by hand
(23/32, 27/32, 31/16, 31/16; budgets 1/8 and 33/16). No numerical errors were found in the
quoted examples. All findings below concern writing, accuracy of
summary statements, and structure.

---

## 1. Overall assessment

The mathematics is written precisely, the prose is mostly plain, and there is very little
filler. I found almost none of the usual "LLM slop" words. The main problems are
**focus, length and consistency**, not sentence style.

1. **The main result is present but buried.** It is the second of five equal-weight
   paragraphs in "Main results" (Theorems 5.5/6.11: certified approximation that is FPT in
   (p, κ), and exact output). Nowhere does the introduction state a formal headline theorem.
   "Main results" (5 paragraphs, ~1.5 pages) is followed by "Contributions" (6 items),
   which lists the same results a second time.
2. **Some summary statements in the abstract, introduction and conclusion are
   stronger than the theorems.** One of them is literally contradicted by the paper's own
   hardness result (TU constraints, see C1). These are wording errors; the theorems are fine.
3. **The paper is two or three papers in one.** The compiled version has 99 pages: about 77 pages of
   body, 11 of references and 11 of appendices. Section 7 ("Conditional recourse") alone runs from
   p. 21 to p. 45, has 48 numbered environments (Theorem 7.46) and is longer than the core
   (§§3–6). Large parts of §7–§9 are side results, non-results
   ("Neither lemma gives a sparse algorithm"), outlines, or repeats of
   machinery from §6.
4. **Repetition of machinery and of the discussion of prior work.** There are four separate rational-height
   lemmas, two snapping procedures, two acceptance propositions and two "uniform
   grids keep Θ(√n) nodes" propositions. The discussion of prior work appears both in §2 and in
   in-section remarks, in one case almost word for word.
5. **Notation and terminology are overloaded.** P, Δ, R, K, γ, β, η, 𝓡, 𝒞, ℓ, W and D each have
   3–7 meanings. Sometimes two meanings occur inside one section. The main algorithm has
   no single name: Algorithm 1, CT, FG (undefined), "capped algorithm", "corrected-grid
   algorithm", "filtered-grid algorithm", "certified grid algorithm", "box algorithm",
   "pruned-grid trials". The per-coordinate grid size is called "nodes", "labels",
   "points" or "states".
6. **Leftovers from drafting**: "of the report" (`recourse-balanced.tex` 163–164) and the
   undefined acronym "FG" (`optsets.tex` 45, 92). In the current build, the description of
   Section 6 no longer matches its contents.

The related-work section is fair and well sourced. It is a catalogue (71 `\cite` commands in 9
paragraphs) rather than an argument organised around the contributions, and
several of its paragraphs are repeated later as remarks.

---

## 2. Findings (severity, location, issue, fix)

### Critical

**C1. The abstract and introduction misstate the complexity of the TU extension, and
the paper's own Prop. 10.x (`lim:prop:constraints`) contradicts the misstatement.**
- `abstract.tex` 30–32: "Totally unimodular coupling constraints admit exactly feasible
  correlated rounding with polynomial complexity for fixed width".
- `intro.tex` 112–113: "the algorithm is polynomial for fixed width and conditioning but
  not fixed-parameter tractable".
- What the paper proves: Theorem `thm:tu-approx` gives polynomial time only when κ_c,
  W/η, d and r are polynomially bounded. Without growth the tables grow like
  (W√(n_c L̄/ε))^p, which is polynomial in 1/ε, not in q. Prop. `lim:prop:constraints` together with the
  paragraph after it shows that, with a TU path matrix, p = 3 and κ = 1, the problem is NP-hard,
  and that the pseudopolynomial level-0 grid cannot be removed unless P = NP. Read literally,
  the abstract and introduction claim that this NP-hard case is polynomial.
- This is a wording fix; the theorems are correct. Replacement text is in Rewrites 2 and 3.

### Major

**M1. The abstract is too long (≈330 words) and its second half is a list.** `abstract.tex` 1–38.
MP asks for 150–250 words. The last 12 lines list about ten secondary results in specialised
terms ("separately concave submodular residuals", "cut-based grid oracles for balanced
quadratics", "endpoint program", "point localization under set growth", "local moment
matching"). An expert reader cannot tell which result matters. Fix: Rewrite 1.

**M2. The introduction has no headline theorem, and "Main results" and "Contributions"
repeat each other.** `intro.tex` 36–179. Fix: state Theorem 1.1, combining the certificate validity
of Thm 4.7, the approximation bound of Thm 5.5 and the exact output of Thm 6.11, and Theorem 1.2, combining the lower
bounds of Cor. 10.2, Prop. 10.6 and Prop. 10.7. Then give one short paragraph per extension. Merge "Contributions" into
these paragraphs as a one-line novelty statement each, or keep the list and cut
"Main results" to the theorems. Rewrite 4 gives a draft of Theorem 1.1.

**M3. The introduction omits a scope limit that the paper now proves itself.** Lemma
`lem:growthcert`(b) and Remark `rem:nonconvex` (`setting-growthcert.tex`): for a
continuous box QP, quadratic growth forces H_SS ≻ 0 on the coordinates strictly inside
their bounds, and a fully interior minimizer forces strong convexity. The abstract
("Many nonconvex mixed-integer optimization problems…") and the introduction (Example 5.8 "many local
minima") let the reader assume that growth with moderate κ is common among nonconvex
continuous instances. An expert referee will raise this objection immediately. The paper should
anticipate it in the introduction. Fix: Rewrite 5.

**M4. The claim about unions of cells omits the parameters it depends on.** `intro.tex` 116–118: "unions of
uniform cells restore a polynomial bound for fixed width when the optimal set is finite".
Theorem `thm:cells` gives K_S = 12r(2√(nκ_S)+1). The bound is polynomial in n, κ_S and r
for fixed p, and κ_S can be exponential in I. Fix: Rewrite 3.

**M5. The conclusion overstates the lower bound.** `conclusion.tex` 13–15: "the dependence on the
condition number must be polynomial". What is proved (Cor. `lim:cor:nopolylog`) is
that it cannot be polylogarithmic unless P = NP. Quasi-polynomial dependence is not
excluded. Fix: Rewrite 20.

**M6. Open problem (1) in the conclusion contradicts Remark `rem:cv-unstable`.** `conclusion.tex` 31–32:
"Theorem cv answers this when the convex part can be eliminated with certified
responses whose pieces are small". Remark `rem:cv-unstable` shows that the certified
cancellation is a maximum over pieces, "however small the piece". Small pieces are the
problem, not the condition under which the theorem helps. The correct condition is Corollary `cor:cv-nu`
(L ≤ C₀ν). Fix: Rewrite 21.

**M7. Drafting artifacts and an undefined acronym.**
- `recourse-balanced.tex` 163–164: "the cut-based recourse of the report".
- `optsets.tex` 45 and 92: "in FG and CT", "every box of FG". FG is never defined; it
  survives from `process/fragments/several-draft.tex`.
- Fix: Rewrites 13 and 14.

**M8. The description of Section 6 does not match its contents, and the scope statement
crosses sections.** `exact.tex` 3–15 promises "unions of uniform cells restore a rate that is
polynomial for fixed bag size", but that material is in §9.1. It also says "The last subsection treats
explicit polynomial factors", but `exact-localized.tex` is now input after it. `exact.tex` 19:
"Throughout Sections 6.1–9.1" (`sec:exact-data`–`sec:exact-nonunique`) makes a standing assumption
that spans three sections. Remark `rem:np` (rational witnesses, NP/coNP) sits in §9.1 but
belongs to §6. Fix: Rewrites 9 and 10. Move `rem:np` to the end of §6.2.

**M9. Section 7 is overloaded and is longer than the core.** Recourse covers about 24 pages,
48 numbered items and four unrelated mechanisms: value functions, piecewise-affine convex responses,
min-cut residuals and balanced grid oracles. It also contains:
- non-results: "The negative-curvature target" (`recourse-convex.tex` 748–798), Lemmas
  `lem:cv-energy` and `lem:cv-envelope`, followed by "Neither lemma gives a sparse algorithm";
- speculation: 734–746 ("a localized analysis could treat separately … no such analysis is
  given here");
- side corollaries: `cor:cv-affine`, `cor:cv-nu`, and Prop. `prop:cv-ladder` with the remark after it;
- §7.4 (concave–convex residuals). It is never connected to the corrected-grid
  framework and is not mentioned in the introduction or abstract;
- Theorem `thm:balanced`. It is not recourse; it is a different min-oracle for the same grids.

The section introduction (`recourse.tex`) gives no roadmap. Fix: see §4 (restructuring). As a
minimum, cut 734–798, move `prop:cert-exist`, `lem:cv-bits`, `lem:cv-height`, the
proof of `thm:cv-recog`, `cor:cv-affine`, `cor:cv-nu`, `prop:cv-ladder`,
`rem:cv-unstable`, §7.4 and `lem:cr-height`/`thm:cr-exact` to an appendix, and make
"Corrected grids without a tree decomposition" its own short section. It could also become a remark
in §4 ("any exact oracle for β and m_i can replace the messages").

**M10. The same machinery appears several times.**
- Rational height appears four times: Cor. `cor:height` (box), Lemma `lem:cv-height` (polytope, unique
  minimizer), Lemma `lem:cr-height` (core with endpoint labels) and Cor. `cor:tu-height` (TU).
- Snapping appears twice: REC (Lemma `lem:snap`) and TU-REC (Lemma `lem:tu-snap`). Acceptance appears twice:
  `prop:accept` and `prop:tu-accept`, which have identical proofs.
- "Filtered uniform grids keep Θ(√n) nodes" appears twice: Prop. `prop:sharp` (new, §5) and
  Prop. `prop:tu-tight` (§8.7, "a box problem in disguise").
- `lem:cr-semiconcave` restates `lem:valuefunction`(a). `lem:cr-cell`, the rounding remark after
  `prop:cellwise` and the proof of `lem:cells` are three versions of one Jensen argument.
- Fix: state one height/snap/accept lemma for a polytope {x : Mx ≤ d} with integral M.
  Box rows (I; −I) and TU rows are special cases with the constants R and Ω. Then
  derive Cor. `cor:height`, Cor. `cor:tu-height` and Lemma `lem:cv-height` as corollaries.
  Replace `prop:tu-tight` by one sentence citing `prop:sharp`. Delete `lem:cr-semiconcave`.

**M11. Prior-work discussion is repeated between §2 and the remarks.**
- `related.tex` 87–106 and Remark `rem:cluster` (`growth.tex` 243–254) are nearly the same text
  ("In branch-and-bound with second-order convergent (lower) bounds, the number of boxes
  that remain near a nondegenerate minimizer is independent of the tolerance …").
- `related.tex` "Exact rational output" repeats Remark `rem:np` (`optsets.tex` 234–252).
- `related.tex` "Cuts and submodularity" repeats Remark `rem:cr-cut-prior` and
  Remark "Position of Theorem `thm:balanced`".
- `related.tex` "Constraints, optimal sets and limits" repeats Remark `rem:tu-bm`.
- `grids.tex` 225–230 repeats `related.tex` "Filtering and certificates".
- Fix: keep each comparison in one place. Use the in-section remark when it needs the technical
  statement, as with Bienstock–Muñoz, and otherwise §2. Delete Remark `rem:cluster` (Rewrite 12).

**M12. Notation is heavily overloaded, sometimes inside one section.** Examples:
- P: {i : L_i > 0} (§3); ΔH (§6, §8.6); polytope (Def. `def:leaf`, Lemma `lem:cv-height`); 𝒫_i
  pattern sets (§9.2).
- Δ: effective width Δ_i (§4); common denominator (§6, §8.6); maximum degree (Example 5.8); simplex
  (Prop. `prop:cert-exist`).
- R: height bound (§6, §8.6); recourse index set (§7.1); radius R_ij (§5); number of leaves
  (Def. `def:leaf`); edge set (App. E); relaxation value R_k (§10.6).
- K: grid cap; retained set (§7.1); matrix K_t (§7.2); KKT matrix (Lemma `lem:tu-statpoly`); guess K
  (§9.3); node set K_i (§6 localized); 𝒦 subspace (§8).
- γ: weighted growth (§3); Euclidean growth in Lemma `lem:growthcert`, which sits in the same section;
  polytope right-hand side γ_t; monomial coefficient γ_m; minimum gap (Prop. `prop:tu-misaligned`);
  smallest active derivative (App. F); perturbation γ_i (App. C).
- η: η_j = 2^{E−j} (§5); oracle error (§7.2); mesh unit (§8); proximal weight (App. B); a constant
  (Prop. `prop:cv-ladder`); unary terms η_i (§7.5).
- 𝓡: *retained* variables in Def. `def:cv-model` (§7.2), but *residual* variables in §7.3–7.4, the
  next two subsections. R (plain) is the *recourse* set in §7.1.
- 𝒞: core (§7.3); diagonal-certificate class (§9.3).
- ℓ: lower bounds, but also oracle lower values ℓ(v) (Thm `thm:cr-filter`) and the gradient ℓ(x)
  (`exact-localized.tex` 7, while ℓ_i are bounds in the same subsection).
- Lower bounds are written both ℓ_i (§3–§6) and l_i (67 occurrences in §7, §9, §10, App. F).
- Fix: add a notation table after §3. Rename at least: 𝓡 → 𝒦 or Z-indices (retained) in §7.2 and
  keep 𝓡 for residual; P = ΔH → Ĥ; Δ (denominator) → δ_F or Λ; γ in `lem:growthcert` →
  g; ℓ(x) in §6 localized → ζ(x) (as already used in its proposition); use ℓ_i everywhere.

**M13. The main algorithm and its objects have no stable names.**
- The algorithm: "Algorithm 1" and "Algorithm 2 (CT)" in §5; "FG" in §9.1; "capped algorithm" in §7.5 and §10.2;
  "corrected-grid algorithm" in §7.2 and §10.3; "filtered-grid algorithm" in §10.4; "certified grid
  algorithm" in §7.5; "box algorithm" in §8.7; "pruned-grid trials" and "capped pruned-grid algorithm" in
  App. F; "common-mesh variant".
- The grids: "graded" in §5, "geometric" in §11 and App. B. The grading parameter θ is called a
  "slope" in `growth-sharp.tex`.
- The size per coordinate: "nodes" (§5, Table 1), "labels" (§8, §11, `growth-sharp.tex`), "points" (§8.4) and
  "states" (§11, Fig. 1, which means bag-table entries).
- Fix: use CT for the algorithm everywhere, and "CT with a common mesh" for the variant. Use
  "graded grid" and "grading θ". Use "nodes per coordinate" for |G_i| and "table entries" for bag-table
  size. Define each term once in §4 or §5.

**M14. A main-text theorem relies on an algorithm defined only in an appendix.** Theorem
`thm:diagdiscovery` (`optsets.tex` 540–556) says "run the proximal iteration with guess K for
stages 0,…,J_K", but the proximal iteration is defined only in App. B. The remark after it
uses an undefined constant C₀ (`optsets.tex` 588, "(C₀p)^p"). Fix: Rewrite 25. Also define C₀ or replace it with
the explicit constant from Lemma `lem:proximal`(i).

**M15. The order of material in §7.1 is wrong.** In `recourse-valuefn.tex`, 32–95 insert bag cells, e_B,
Lemma `lem:cr-semiconcave` and Lemma `lem:cr-cell` between Lemma `lem:valuefunction` and the paragraph
that discusses it. That paragraph (97: "Part (a) explains why …") now refers back across
two lemmas. Lemma `lem:cr-semiconcave` restates `lem:valuefunction`(a), and the proof of
`lem:cr-cell` cites `lem:valuefunction`(a) anyway. These lemmas use the global L and l_i
instead of L_i and ℓ_i. Fix: Rewrite 17. Move the bag-cell material to the start of §7.2, where it is used.

### Minor

- m1. `intro.tex` 163–164, "the unique-minimizer hardness at width three". The paper defines
  width = p − 1, and the result is at bag size three, i.e. width two (Rewrite 6).
- m2. `intro.tex` 14–15, "Global solvers based on spatial branch-and-bound bound individual terms":
  the double "bound" makes the sentence hard to parse (Rewrite 7).
- m3. `intro.tex` 73–76, "turns any point within poly(I)+log₂(1/g_S) bits of the optimum into
  an exact minimizer". "Within k bits of the optimum" is not defined (Rewrite 8).
- m4. `intro.tex` 86–93: the paragraph "Conditional recourse" never says what recourse is. The
  term comes from stochastic programming, where it means something different (Rewrite 8b).
- m5. `intro.tex` 122: "found exactly in f(p,κ)poly(I)". The theorem uses the set-growth
  constant, so the parameter should be κ_S.
- m6. Abstract "(I+q)^{O(1)}" versus intro and Theorem 5.5 "(I+q+1)^5". Use one form (q = 0 is
  allowed, so (I+q+1)).
- m7. `growth.tex` 43–44, "U the smallest objective value of a feasible point known so far (at
  least F(ℓ))". "At least F(ℓ)" reads as U ≥ F(ℓ), the opposite of what is meant (Rewrite 11).
- m8. `exact.tex` 7, "in a form that serves two purposes at once" is vague: name the two purposes.
- m9. `recourse-balanced.tex` 115, "the coordinate curvature condition~Definition 3.1". The words
  "condition" and "Definition" collide; write "the condition of Definition~\ref{def:curvature}" (Rewrite 15).
- m10. `recourse-balanced.tex` 141–143: "the proof of Theorem `thm:exact`, which uses … rational
  reconstruction". That proof uses snapping recovery (REC), not reconstruction (Rewrite 16).
- m11. `recourse-convex.tex` 4: "This section eliminates" in a subsection (Rewrite 18).
- m12. `conclusion.tex` 45: "Propositions~\ref{prop:tu-misaligned} and the example after it"
  uses a plural with one reference and leaves the example unnamed (Rewrite 22).
- m13. `computation.tex` 139–141, "this is the behaviour expected without growth". By Remark
  `rem:setgrowth` set growth always exists. The segment instances lack *point* growth (Rewrite 23).
- m14. `setting-growthcert.tex` 25: "F(x)−F(x*)=ℓ^T d+½dᵀHd". This should be ζᵀd, since ℓ is the lower
  bound vector. `exact-localized.tex` 7 calls the gradient ℓ(x) and then uses ζ in the
  proposition (Rewrite 24).
- m15. `limits.tex` 191–192, "By the qualitative growth lemma for quadratics with a unique
  minimizer": cite Lemma~\ref{lem:unique-growth}.
- m16. `appendix-smoothed.tex` 2, "Random linear perturbations of the core remove this effect":
  "this effect" has no antecedent in the appendix. Write "remove the effect of Example `ex:cr-flat`".
- m17. `appendix-boundary.tex` 23: "We use the rounder constants 22/15 and 5". 22/15 is not
  rounder than 17/15. Write "We use the weaker constants 22/15 and 5, which also cover the
  graded variant", or just use 17/15.
- m18. Untitled remarks: `recourse-local.tex` 49, `recourse-cuts.tex` 282,
  `recourse-balanced.tex` 78 and `optsets.tex` 519. Give each a title, as the other remarks have.
- m19. British spellings in an otherwise American text: centre (6×, `recourse-local.tex`),
  neighbour(s) (4×), behaviour (2×), favours (1×).
- m20. Idioms: "does real work" (`intro.tex` 126, `limits.tex` 7) → "is needed"; "is really
  incurred" (`constraints.tex` 425) → "is incurred"; "are actually retained" (676) → "are
  retained"; "The instance is trivial for other methods; the point is that …"
  (`optsets.tex` 103) → "Other methods solve this instance easily; it shows that …".
- m21. In Def. `def:growth`, κ = max{1, L/g} is defined from *a* growth constant g, whereas κ̄ uses
  the largest constant γ*. Define g* as the largest constant and κ = max{1, L/g*}.
- m22. Undefined jargon: "attachment box" (`recourse-convex.tex` 265, 338, 435, 494), "calibrated
  table entry" (286, 296), "box-stable" (`recourse-cuts.tex` 125), "XP factor"
  (`constraints.tex` 807), "rETH" (`limits.tex` 346, without expansion near it), "cell fiber"
  (`constraints.tex` 172).
- m23. `recourse-cuts.tex` 136 and 147: the paragraph heading "Search over a continuous core." is
  followed directly by "Core search.". Merge them.
- m24. `recourse.tex`: the section introduction has no roadmap of §7.1–7.5. Add one sentence per subsection.
- m25. `limits.tex` 1–31: the bullet list repeats the introduction's "Structural limits" paragraph and
  omits Prop. `prop:oraclebarrier`. Two items point to results proved elsewhere (`prop:star` in §7,
  `prop:twocenters` in §9).
- m26. Proof of Prop. `prop:lbwidth` (`limits.tex` 319–327): "Let V have independent coordinates"
  reuses V, the vertex set, and "M" is the multilinear part, not the earlier M = Σa_i². Rename to Y and Ψ_ml.
- m27. Prop. `prop:sshard` (`optsets.tex` 603–607): "and the ratio κ of these instances is not
  bounded by any polynomial" is also conditional on P ≠ NP. Write "Consequently, unless P = NP,
  (i) …, and (ii) κ is not polynomially bounded on these instances."
- m28. Appendix order does not follow section order. B relates to §9, C to §7, D to §10.6, E to
  §10.2 and F to §6. The titles "Proof of Proposition 10.14" and "Proof of Proposition 10.7" say
  nothing in the TOC. Order the appendices by section and give them content titles.
- m29. The "Organization" paragraph (`intro.tex` 170–179) ends with "Longer proofs are in the appendices". The
  appendices also contain new results: Thm `thm:boundary`, Props `prop:margin` and
  `prop:weakcompl`, Thm `thm:cr-smoothed`, the proximal algorithm and the localized acceptance proof.
  Say so.
- m30. Remark `rem:tu-hybrid` (`constraints.tex` 795–812) states a result "only as an outline"
  and says the constants have not been written out. Cut it, or move it to the open problems.
- m31. Seven overfull boxes in the last build: `growth.tex` 51–53, `recourse-local.tex` 8–12 and
  111–124, `optsets.tex` 465–466, `computation.tex` 10–28 and two in the appendices. The worst
  is 18.9 pt.
- m32. The title is generic. "Decomposition-aware global optimization" does not say what is
  proved. Consider, for example, "Certified global optimization of sparse mixed-integer
  quadratic programs: fixed-parameter tractability in treewidth and conditioning".
- m33. §2 "Related work" reads as a catalogue (71 `\cite` commands in 9 paragraphs). Peripheral items
  (Benders, MPC condensing, rotamer dead-end elimination, structured-prediction cascades, smoothed
  analysis) could go to the sections that use them. Organise §2 around three questions: (i) what is
  known about tractability of sparse nonconvex QP (Del Pia–Khajavirad, Bhathena et al.,
  Bienstock–Muñoz, Vavasis/Del Pia); (ii) grid and vertex bounds and certificates; (iii) why
  accuracy independence is new (cluster problem, proximity scaling). The section is fair. I
  found no misattribution in the passages I checked against the knowledge base, for example Bhathena et al.:
  convex objective, indicator constraints, margin and decay conditions.

---

## 3. The 25 most valuable concrete rewrites (old → new)

**Rewrite 1 — Abstract (`abstract.tex` 1–38), full replacement (~230 words).**
New:
> Many nonconvex mixed-integer optimization problems have objectives that are sums of local
> terms whose interaction graph has small treewidth. Small treewidth alone does not make them
> tractable: box-constrained nonconvex quadratic programming is strongly NP-hard at treewidth
> two. We identify two checkable quantities that make tree decompositions useful for certified
> global optimization: upper bounds $L_i$ on the curvature of the objective along each
> coordinate, and quadratic growth at the minimizer. Subtracting $L_iw^2/8$ at each grid node,
> where $w$ is the largest adjacent grid interval, turns exact dynamic programming over a
> product grid into a valid lower bound. Coordinate min-marginals then discard intervals that
> cannot contain an improving point, and the grids of the successive stages form a certificate
> that is checked by recomputation. Under quadratic growth, graded grids keep
> $O(\sqrt{\bar\kappa}\log n)$ nodes per coordinate at every accuracy, where $\bar\kappa$ is a
> scale-invariant ratio of curvature to growth. For rational mixed-integer quadratic programs on
> a box with bag size $p$, this gives a certified $2^{-q}$-approximation in
> $f(p,\bar\kappa)(I+q+1)^{O(1)}$ bit operations and the exact minimizer in
> $f(p,\kappa)I^{O(1)}$, without knowledge of the growth constant. The dependence on $\kappa$
> cannot be polylogarithmic unless P${}={}$NP, and under the randomized exponential-time
> hypothesis its exponent must grow linearly with $p$. We extend the method to exact partial
> minimization (recourse), totally unimodular coupling constraints and several minimizers, and
> report an exact-arithmetic implementation whose certificates are replayed by an independent
> checker.

**Rewrite 2 — Abstract TU sentence, if the long abstract is kept (`abstract.tex` 30–32).**
Old: "Totally unimodular coupling constraints admit exactly feasible correlated rounding with
polynomial complexity for fixed width,"
New: "Totally unimodular coupling constraints with data aligned to a mesh admit exactly
feasible correlated rounding; for fixed width the resulting algorithm is polynomial when the
conditioning and the box widths measured in mesh units are polynomially bounded,"

**Rewrite 3 — Introduction, TU and several minimizers (`intro.tex` 110–118).**
Old: "restores the certificate, with exact feasibility and exact output for quadratics; the
algorithm is polynomial for fixed width and conditioning but not fixed-parameter tractable, and
we show that the uniform meshes responsible for this are forced (Section~\ref{sec:constraints}).
With several minimizers, a single graded grid can need exponential time even for two isolated
minimizers (Proposition~\ref{prop:twocenters}); unions of uniform cells restore a polynomial
bound for fixed width when the optimal set is finite (Theorem~\ref{thm:cells})."
New: "restores the certificate, with exact feasibility and exact output for quadratics. For
fixed width the algorithm is polynomial when the conditioning, the box widths measured in mesh
units and the number of optimal values per coordinate are polynomially bounded. It is not
fixed-parameter tractable: the uniform meshes it needs are forced
(Section~\ref{sec:tu-limits}), and the dependence on the box widths cannot be removed unless
P${}={}$NP (Section~\ref{sec:limits-constraints}). With several minimizers, a single graded grid
can need exponential time even for two isolated minimizers
(Proposition~\ref{prop:twocenters}); when the optimal set is finite, unions of uniform cells give
grids with $O(r\sqrt{n\kappa_S})$ nodes per coordinate, where $r$ bounds the optimal values per
coordinate and $\kappa_S$ uses the growth constant towards the optimal set
(Theorem~\ref{thm:cells})."

**Rewrite 4 — Introduction, add a headline theorem at the start of §1.1 (new text after
`intro.tex` 45).**
New:
> The following theorem summarizes the main results; the rest of this subsection explains its
> parts and the extensions.
>
> **Theorem 1.1.** Let $F$ be an explicit rational quadratic on a mixed box $X$, given with a
> tree decomposition of maximum bag size $p$, and let $I$ be the input length.
> (a) For every $q$, algorithm CT returns a feasible point and a certificate, checkable in exact
> arithmetic, that its value is within $2^{-q}$ of $\min_XF$. The certificate's validity uses no
> convexity, uniqueness or growth (Theorem~\ref{thm:certificate}).
> (b) If $F$ has weighted quadratic growth with condition number $\bar\kappa$, CT uses
> $f(p,\bar\kappa)(I+q+1)^5$ bit operations, with $f(p,\kappa)=c_0(c_1p\sqrt\kappa)^p\kappa
> (1+\log_2\kappa)^2$; neither the growth constant nor $\bar\kappa$ is an input
> (Theorem~\ref{thm:approx}).
> (c) Algorithm EX returns an exact global minimizer and $\min_XF$ on every instance, in
> $f_1(p,\kappa)(I+1)^{C}$ bit operations under quadratic growth (Theorem~\ref{thm:exact}).
> (d) Unless P${}={}$NP, $f(3,\kappa)$ cannot be polylogarithmic in $\kappa$; under ETH the
> dependence on $p$ is exponential even for $\kappa\le2$; under rETH the exponent of $\kappa$
> cannot be $o(p)$ (Section~\ref{sec:limits}).

**Rewrite 5 — Introduction, scope of growth (insert after `intro.tex` 45, "…(Definition~\ref{def:growth}).").**
New: "Growth restricts where nonconvexity can occur. For a continuous box QP, growth forces
the Hessian block of the coordinates strictly inside their bounds to be positive definite
(Lemma~\ref{lem:growthcert}). The nonconvex instances covered by our bounds therefore have their
negative curvature in directions that involve active bounds or integer coordinates. Such instances
include problems with exponentially many strict local minima (Example~\ref{ex:family})."

**Rewrite 6 — Contributions item (v) (`intro.tex` 162–164).**
Old: "in particular the expanding-box chain, the unique-minimizer hardness at width three and the
finite-order moment obstruction;"
New: "in particular the expanding-box chain, NP-hardness with a unique minimizer at bag size
three, and the finite-order moment obstruction;"

**Rewrite 7 — Introduction, second paragraph (`intro.tex` 14–17).**
Old: "Global solvers based on spatial branch-and-bound bound individual terms by convex
relaxations and branch on variable domains \cite{…}; they do not use a tree decomposition to
organize the search."
New: "Spatial branch-and-bound solvers relax individual nonconvex terms by convex underestimators
and branch on variable domains \cite{…}; they do not use a tree decomposition to organize the
search."

**Rewrite 8 — Introduction, snapping sentence (`intro.tex` 72–76).**
Old: "A snapping procedure based on explicit rational height bounds turns any point within
$\poly(I)+\log_2(1/g_S)$ bits of the optimum into an exact minimizer, where $g_S$ is the growth
constant towards the optimal \emph{set}, so exactness itself needs no uniqueness
(Theorem~\ref{thm:transfer})."
New: "Explicit rational height bounds give a snapping procedure that turns any feasible point
with certified gap at most $2^{-k}$, $k=\poly(I)+\log_2(1/g_S)$, into an exact minimizer, where
$g_S$ is the growth constant towards the optimal \emph{set}. Exactness itself therefore needs no
uniqueness (Theorem~\ref{thm:transfer})."

(8b) Opening of the paragraph "Conditional recourse" (`intro.tex` 87–88). Old: "The condition number uses
diagonal curvature, so a stiff convex coupling term inflates it although convex subproblems are
easy." New: "We call exact minimization over some variables, for fixed values of the others,
*recourse*. The condition number uses diagonal curvature, so a stiff convex coupling term
inflates it even though the convex subproblem it defines is easy."

**Rewrite 9 — Opening of Section 6 (`exact.tex` 3–15).**
Old: "… This section proves the height bound in a form that serves two purposes at once, gives an
acceptance rule … Without uniqueness, the single-center grids of Section~\ref{sec:growth} can be
exponentially slow, and we show that unions of uniform cells restore a rate that is polynomial
for fixed bag size. The last subsection treats explicit polynomial factors."
New: "… This section proves a height bound for minimizers and for the optimal value, gives
an acceptance rule that needs neither uniqueness nor growth, and shows that an exact optimizer
can be recovered from any feasible point close to the \emph{set} of minimizers. Under quadratic
growth at a unique minimizer this yields exact output within the bound of
Theorem~\ref{thm:approx}. Section~\ref{sec:polynomial} treats explicit polynomial factors, and
Section~\ref{sec:localized} gives an acceptance test that uses the filtering history. Several
minimizers are treated in Section~\ref{sec:optsets}."

**Rewrite 10 — Scope statement (`exact.tex` 19).**
Old: "Throughout Sections~\ref{sec:exact-data}--\ref{sec:exact-nonunique}, $F$ is a quadratic
with rational data,"
New: "In this section, except in Section~\ref{sec:polynomial}, $F$ is a quadratic with
rational data,"
(Section 9 already restates its assumption in its first paragraph.)

**Rewrite 11 — Algorithm 1 (`growth.tex` 43–44).**
Old: "and $U$ the smallest objective value of a feasible point known so far (at least
$F(\ell)$)."
New: "and $U=F(\ell)$, or the value of a better feasible point if one is known."

**Rewrite 12 — Delete Remark `rem:cluster` (`growth.tex` 243–254), which repeats `related.tex` 87–106.**
Replace it with one sentence after Lemma `lem:states`: "Lemmas~\ref{lem:inv} and~\ref{lem:states}
are a global, non-asymptotic form of the cluster-problem bound of branch-and-bound
(Section~\ref{sec:related}); because filtering is coordinatewise, the exponential dependence
falls on $p$ rather than on $n$."

**Rewrite 13 — Undefined "FG" (`optsets.tex` 45 and 92).**
Old (45): "Consequently, in FG and CT every stage has certified gap"
New: "Consequently, in every trial of Algorithm~1 and of CT every stage has certified gap"
Old (92): "so every box of FG is $[0,M]^2$"
New: "so every box of every trial is $[0,M]^2$"

**Rewrite 14 — Drafting artifact (`recourse-balanced.tex` 163–165).**
Old: "This removes the restriction to nonpositive residual diagonals in the cut-based recourse of
the report: residual coordinates with positive diagonal are gridded and filtered like the core,
and the residual graph may be dense."
New: "Compared with Section~\ref{sec:cuts}, residual coordinates may now have positive diagonal:
they are gridded and filtered like the core, and the residual graph may still be dense."

**Rewrite 15 — `recourse-balanced.tex` 114–116.**
Old: "depend on $F$ only through the coordinate curvature condition~Definition~\ref{def:curvature},
which holds with this $L$ because"
New: "depend on $F$ only through the condition of Definition~\ref{def:curvature}, which holds
with this $L$ because"

**Rewrite 16 — `recourse-balanced.tex` 141–143.**
Old: "which uses only the approximation algorithm, the height bounds of
Corollary~\ref{cor:height}, rational reconstruction and exact checks;"
New: "which uses only the approximation algorithm, the height bounds of
Corollary~\ref{cor:height}, snapping recovery (Lemma~\ref{lem:snap}) and exact checks;"

**Rewrite 17 — Reorganise §7.1 (`recourse-valuefn.tex` 32–103).**
(a) Delete Lemma `lem:cr-semiconcave` (46–58). It restates Lemma `lem:valuefunction`(a).
(b) Move the paragraph "Part~(a) explains … stiff convex terms." (97–103) to directly after the proof of
Lemma `lem:valuefunction` (after line 30).
(c) Move "For a nonempty set $B$ … corners" (32–44) and Lemma `lem:cr-cell` with its proof
(60–95) to the start of §7.2. Write $L_i$ and $\ell_i$ in place of $L$ and $l_i$, so that
$e_B(C)=\sum_{i\in B}\frac{L_i}8w_i(C)^2$.
(d) Merge the two blank lines at 95–96.

**Rewrite 18 — `recourse-convex.tex` 3–9.**
Old: "Large positive curvature often sits in variables that enter the objective convexly once
the remaining variables are fixed. This section eliminates such variables exactly, as convex
value factors, and shows that the corrected-grid algorithm then depends on the upper coordinate
curvature of the \emph{reduced} objective. One curvature lemma covers three cases: … The section
ends with the limits of this route."
New: "Large positive curvature often sits in variables that enter the objective convexly once
the other variables are fixed. This subsection eliminates such variables exactly, as convex
value factors, and shows that CT then depends only on the coordinate curvature of the reduced
objective. Proposition~\ref{prop:vf-curv} covers the three cases (no certificate, a globally
affine response, a piecewise-affine response), and Proposition~\ref{prop:cv-limit} shows the
limits of this approach."

**Rewrite 19 — Cut the speculative paragraph (`recourse-convex.tex` 734–746) and the subsection "The
negative-curvature target" (748–798).**
Replace both with one sentence after Remark `rem:cv-unstable`: "The large ratios in
Proposition~\ref{prop:cv-limit} come from pieces that contain no near-optimal point; a bound in
terms of $p$ and $\nu/g$ would need curvature measured only where near-optimal points can lie
(Section~\ref{sec:conclusion}, question~1)." Lemmas `lem:cv-energy` and
`lem:cv-envelope` do not lead to an algorithm, as the paper itself says. Drop them, or move
them to an appendix on open problems.

**Rewrite 20 — Conclusion (`conclusion.tex` 12–15).**
Old: "show that this parameterization is close to the right one: neither parameter can be
dropped, the dependence on the condition number must be polynomial, and its exponent must grow
with the bag size."
New: "show that neither parameter can be dropped: the dependence on the condition number cannot
be polylogarithmic unless P${}={}$NP, and under rETH its exponent cannot be $o(p)$."

**Rewrite 21 — Conclusion, question 1 (`conclusion.tex` 31–33).**
Old: "Theorem~\ref{thm:cv} answers this when the convex part can be eliminated with certified
responses whose pieces are small,"
New: "Theorem~\ref{thm:cv} and Corollary~\ref{cor:cv-nu} answer this when certified responses
reduce every coordinate curvature to $O(\nu)$,"

**Rewrite 22 — Conclusion, question 3 (`conclusion.tex` 45–46).**
Old: "Propositions~\ref{prop:tu-misaligned} and the example after it show that curvature-only
corrections on graded grids fail,"
New: "Proposition~\ref{prop:tu-misaligned} and Example~\ref{ex:tu-sum} show that
curvature-only corrections on graded grids fail,"

**Rewrite 23 — §11 Exact output (`computation.tex` 139–141).**
Old: "this is the behaviour expected without growth, where only finite termination is guaranteed
(Theorem~\ref{thm:exact})."
New: "these instances have set growth but no point growth, and for them Theorem~\ref{thm:exact}
guarantees only finite termination."

**Rewrite 24 — Notation slips that use ℓ for a gradient.**
`setting-growthcert.tex` 25. Old: "$F(x)-F(x^*)=\ell^{\T}d+\frac12d^{\T}Hd$". New:
"$F(x)-F(x^*)=\zeta^{\T}d+\frac12d^{\T}Hd$".
`exact-localized.tex` 6–7. Old: "In this subsection $F$ is a quadratic with gradient
$\ell(x)=\nabla F(x)$," New: "In this subsection $F$ is a quadratic,". The proposition already
writes $\zeta=\nabla F(\hat x)$. Also rename γ in Lemma `lem:growthcert`(a) to $g$, because γ is the
weighted growth constant two pages earlier.

**Rewrite 25 — Theorem `thm:diagdiscovery` (`optsets.tex` 540–547): define the proximal iteration in the
main text.**
Insert before the theorem:
"The \emph{proximal iteration with guess $K$} runs stages $j=0,1,\dots$ with mesh $h_j=s2^{-j}$.
Stage $j$ centers a graded grid with grading $\theta\le(8K)^{-1/2}$ at the previous output, on
the box of radius $2\lceil\sqrt{Kn}\rceil h_j$, and minimizes the corrected objective plus
$\frac{L\theta^2}4\norm{y-c}^2$ by the dynamic program of Lemma~\ref{lem:dp}.
Appendix~\ref{app:proximal} gives the details and shows that, if $K\ge L/g$, the outputs
approach $S$ at the rate of the mesh (Lemma~\ref{lem:proximal})."
In the remark after the theorem (`optsets.tex` 588), replace "$(C_0p)^p$" with the constant that
follows from Lemma `lem:proximal`(i), or define $C_0$.

---

## 4. Recommended section-level restructuring

**Diagnosis.** The core contribution (§§3–6 with §10.1–10.3) takes about 30 pages. The three
extensions (§7–§9) take about 45 pages and contain many side results. A referee for MP or SIOPT
will ask for focus. The paper also states the same height, snapping and acceptance arguments
three to four times.

**Option A (recommended): split into two papers.**
- *Paper 1* (about 45 pages plus appendix): "Certified global optimization of sparse mixed-integer
  QPs: FPT in treewidth and conditioning". Sections: Introduction (with Theorems 1.1 and 1.2), Setting (with
  Lemma `lem:growthcert`), Corrected grids and path certificates, Accuracy-independent grids
  (with `prop:sharp`), Exact output (with localized acceptance and Remark `rem:np`; polynomial
  factors as a short subsection), Lower bounds (§10.1–10.4), Computation (§11 without the recourse table),
  Conclusion. Appendices: proofs of §5 and §10.2, polynomial boundary output.
- *Paper 2*: "Recourse, coupling constraints and optimal sets for corrected-grid certificates",
  covering §7, §8, §9 and §10.5–10.6, with references to Paper 1 for the core.

**Option B: one paper, two parts (target about 60 pages before references).**
1. Introduction (≤3 pages). Theorem 1.1 (Rewrite 4), Theorem 1.2 (lower bounds), one paragraph per
   extension, and no separate contributions list (or a list of 4 items).
2. Related work (≤1.5 pages), organised around three questions (m33). Remove the repeated remarks
   (M11).
3. Model, curvature, growth (current §3 with `lem:growthcert`), plus a notation table (M12).
4. Corrected grids and path certificates (current §4). State here, as a remark, that any exact
   oracle for β, a minimizer and the m_i can replace messages, and point to §8.4 (balanced quadratics).
5. Accuracy-independent grids (current §5). Move the constant-chasing in the proof of Lemma
   `lem:states` and the proof of `prop:sharp` to Appendix A, and keep a 5-line sketch.
6. Exact output (current §6 + `rem:np` + localized acceptance). Prove one height/snap/accept lemma for
   polytopes {Mx ≤ d} with integral M (M10), and derive the box case here.
7. Lower bounds (current §10.1–10.4). Move §10.6 (local moments) and Remark `lim:rem:dk` to an appendix.
   Keep `prop:star` where it is proved and only cite it.
8. Extension I: recourse (about 10 pages). §8.1 value functions and the bag-local filter (Thm
   `thm:cr-filter`, Prop. `prop:star`). §8.2 convex recourse: Lemma `lem:leaf`, Prop.
   `prop:vf-curv`, Thm `thm:cv`, statement of Thm `thm:cv-recog`, statement of Prop.
   `prop:cv-limit`. §8.3 cut recourse: Thm `thm:cr-oracle`, core search, Prop.
   `prop:cr-growth`. §8.4 balanced quadratics without decomposition (Thm `thm:balanced`).
   Move to appendices: `prop:cert-exist`, `lem:cv-bits`, `lem:cv-height` (now a corollary of the §6 lemma),
   proofs of `thm:cv-recog` and `prop:cv-limit`, `cor:cv-affine`, `cor:cv-nu`,
   `prop:cv-ladder`, `rem:cv-unstable`, `lem:cr-height`, `thm:cr-exact`, §7.4 (concave–convex
   residuals), App. C (smoothed). Cut: "The negative-curvature target", `recourse-convex.tex`
   734–746, `lem:cr-semiconcave`.
9. Extension II: TU coupling constraints (current §8.1–8.5 and 8.7). §8.6 (exact output) becomes
   a corollary of the §6 lemma with a one-paragraph proof. Replace `prop:tu-tight` with a citation of
   `prop:sharp`. Cut `rem:tu-hybrid` or turn it into an open problem.
10. Extension III: several minimizers (current §9). Give the proximal iteration in the main text (Rewrite 25).
11. Computation (current §11).
12. Conclusion (current §12, with Rewrites 20–22).
Appendices are ordered by section, with content titles (m28).

Either option removes the most visible weaknesses: the buried main result, the 24-page §7,
the repeated height and acceptance arguments, and the repeated discussion of prior work. Option B
removes roughly 15 pages from the body without removing any proved result.

---

## 5. Items checked and found satisfactory

- Proofs of Prop. `prop:cellwise`, Thm `thm:certificate`, Lemma `lem:dp`, Lemma `lem:snap` and
  Thm `thm:transfer` read well: short, complete, and with every step justified.
- Example `ex:chain` and Table 1 agree with the claim in the introduction (at most eleven nodes, m = 64).
- The claims in the introduction about the balanced-quadratic theorem, cut recourse and the
  value-oracle lower bound match the corresponding theorems.
- Hedging is rare and mostly justified ("To the best of our knowledge", once in §1 and once in §2).
- The numbers in Example `ex:cr-star32`, the counterexample after `prop:tu-misaligned` and Example `ex:tu-sum` were
  confirmed exactly (`process/w2/checks/r6_examples.py`).
