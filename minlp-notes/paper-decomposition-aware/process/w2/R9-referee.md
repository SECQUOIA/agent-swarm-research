# Referee report (R9): overall assessment for Mathematical Programming

**Manuscript:** "Decomposition-aware global optimization: certified coordinate grids,
conditional recourse, and structural limits"

**Version reviewed:** the sources in `sections/*.tex`, read on 2026-10-03 between 01:00
and 01:25, and `build/main.pdf`. The paper changed while I read it: the PDF grew from 99
to 104 pages (build of 01:19). The additions were Section 6.6 (localized acceptance),
Lemma `lem:growthcert`, Proposition `prop:sharp` and Appendix G. My comments refer to that
version. Page numbers are from the 104-page PDF. Line numbers are from the source files at
the time of reading.

**Recommendation: major revision.**

The core results look correct, and I believe they are new and of interest to this
journal: the corrected grid, the filtering certificate, accuracy-independent graded grids
under growth, exact output, and the lower bounds. The manuscript is not publishable in its
current form for three reasons:

1. **Length.** It is about two papers long. The main line is buried under roughly 45
   pages of extensions of uneven weight.
2. **Overstated claims.** Several statements in the abstract and introduction say more
   than the theorems prove. The clearest case is the TU-constraint complexity claim, which
   one of the paper's own propositions contradicts.
3. **Thin computations.** The computational evidence comes only from designed instances.

---

## 1. Summary of the submission

The paper studies min F(x) = sum_a f_a(x_{S_a}) over a mixed-integer box, with a
supplied tree decomposition of maximum bag size p.

1. **Corrected grids (Section 4).** Given upper coordinate curvatures L_i, the paper
   subtracts the unary correction L_i w_i(v)^2/8 at each grid node, where w_i(v) is the
   largest adjacent interval. The minimum of the corrected objective over a product grid
   is then a valid lower bound. It equals the best Bajaj–Hasan vertex bound over all
   cells (Prop. `prop:cellwise`), and ordinary two-pass min-sum dynamic programming
   computes it. The min-marginals give a safe filter (Prop. `prop:filter`). The stage
   grids, one bound and one feasible point form a "path certificate" that is checked by
   recomputation (Thm. `thm:certificate`).
2. **Accuracy-independent grids (Section 5).** Assume weighted quadratic growth with a
   scale-invariant condition number κ̄. Grids graded linearly around the current
   corrected minimizer, together with filtering, keep O(√κ̄ log n) nodes per coordinate
   at every stage (Lemmas `lem:inv`, `lem:states`). Capped trials remove the need to
   know the growth constant. The result is a certified 2^{-q}-approximation in
   f(p,κ̄)(I+q+1)^5 bit operations (Thm. `thm:approx`).
3. **Exact output (Section 6).** Height bounds from stationary polytopes, an acceptance
   rule and a snapping recovery give an exact rational minimizer in f(p,κ)poly(I)
   (Thm. `thm:exact`). The certificate's validity uses neither growth nor uniqueness.
   Polynomial factors are covered with exact output for all-integer instances. A
   localized acceptance test was added in Section 6.6.
4. **Extensions.**
   - Section 7, conditional recourse (24 pp.): value functions, a local filter, certified
     convex value factors, minimum-cut residuals, submodular concave–convex residuals and
     balanced quadratics without a decomposition.
   - Section 8, TU coupling constraints (11 pp.).
   - Section 9, several minimizers (9 pp.): two-center hardness for graded grids,
     uniform cells, the optimal set of coordinatewise concave QPs, and discovery under a
     diagonal Lagrangian certificate.
5. **Lower bounds (Section 10).**
   - Box QP with p=3, a unique minimizer and log κ = O(I) is NP-hard.
   - Under ETH, the dependence on p is exponential at κ ≤ 2.
   - Under rETH, the exponent of κ cannot be o(p) (integer instances).
   - In the value-oracle model, the exponent p/2 is optimal.
   - Further results: exponential exact messages at κ ≤ 80, set-growth barriers,
     NP-hardness with one local equality chain, and a finite-order moment obstruction.
6. **Computation (Section 11).** A Python exact-rational implementation with an
   independent checker, run on planted families, the expanding-box chain, 20 small exact
   instances, a SCIP comparison and recourse diagnostics.

## 2. Significance and novelty

**Strengths.**

- The framework is clean, and its certificate is independently checkable. The
  observation that the unary correction gives the best vertex bound over all cells of a
  product grid, at the cost of one min-sum pass, is simple and useful.
- The main theorem is a certified algorithm whose running time is f(p,κ̄)·poly(I+q),
  plus exact output in f(p,κ)·poly(I). The growth constant need not be known. The
  literature audits in `process/w1` (lit-core, lit-ext) found no earlier result of this
  form, and I know of none either.
- The lower bounds give a fairly complete picture of what the parameterization can
  achieve:
  - κ cannot become log κ;
  - p cannot be dropped;
  - the exponent of κ cannot be o(p);
  - p/2 is optimal for value oracles.
- The technical step from an XP bound to an FPT bound is the graded grid. Uniform cells
  give O(√(nκ)) labels per coordinate (Thm. `thm:cells`, Prop. `prop:sharp`), while
  graded grids give O(√κ̄ log n). This step is genuinely new, and it is the part a
  referee would most want to see highlighted.

**Weaknesses that affect the significance.**

- **Scope of the hypothesis.** Global quadratic growth at a unique minimizer with
  moderate κ is strong for nonconvex problems.
  - Lemma `lem:growthcert`(b) shows that for continuous box QP, growth forces the Hessian
    block of the free coordinates to be positive definite. Nonconvexity can live only in
    directions blocked by active bounds, or in integer coordinates.
  - This is the main qualitative fact about the class the theorem covers. It appears
    only as a lemma and remark in Section 3, which was added late. It should appear in
    the introduction.
  - The paper gives no evidence that κ̄ is moderate on any instance class from the
    applications named in the first paragraph (process systems, energy networks,
    optimal control).
- **"Fixed-parameter tractable".** The parameter κ̄ is a real number that the algorithm
  never computes. Computing it is presumably hard. Standard parameterized complexity
  (e.g., Flum–Grohe) requires a polynomial-time computable integer parameterization.
  Remark `rem:fpt` explains the intended meaning. The abstract, introduction and
  conclusion should state the bound itself, or define the notion they use.
- **Uneven extensions.** Some extensions are compositions of classical tools. The paper
  says so in places (e.g., Remark `rem:shor`, Remark `rem:cr-cut-prior`). Several are
  explicitly of limited use:
  - Appendix C states that its smoothed count "is not a device for approximating the
    unperturbed problem".
  - Lemmas `lem:cv-energy` and `lem:cv-envelope` "give no sparse algorithm".
  - Proposition `lim:prop:moments` rules out a relaxation that no one proposed as an
    algorithm here.

  These dilute the contribution.

## 3. Correctness (spot-checks of the main proofs)

I re-derived the following and found no error:

- **Prop. `prop:cellwise`** (a)–(c). Concavity after subtracting
  (L_i/2)(x_i − mid I_i)^2. The bijection between (cell, vertex) pairs and (grid point,
  independent interval choices) gives (b).
- **Prop. `prop:filter` and Thm. `thm:certificate`** (C1)–(C2), and the statement that a
  filtering run yields a valid certificate.
- **Lemma `lem:inv`**:
  - the energy inequality (eq. `eq:energy`);
  - (ii) at j=0, which uses L_i r_i^2 ≤ 1 and s_i ≤ η_0 r_i;
  - (iii): Y ≤ (4/15)(γ^{-1}+κ̄)a ≤ (8/15)κ̄a;
  - (iv): (9/16)a;
  - (v): (17/15)κ̄a.
- **Lemma `lem:states`**:
  - radius constant 2+2√(17/15)+1+(2+√(17/15))/√2 = 7.296 < 7.3 < 8;
  - φ(1) = 16.21, φ(2) = 18.55;
  - the derivative comparison 4/m vs 7.2/m.
- **Thm. `thm:approx`**:
  - termination in (a), with gap ≤ (8/9)ε;
  - μ* and 2^{μ*} ≤ 4√2·√κ̄ ≤ 6√κ̄;
  - the absorption (eq. `eq:logabsorb`), via (log₂(2n+4))^p ≤ (p/(e ln 2))^p(2n+4);
  - the denominator argument in Appendix A.
- **Section 6**:
  - Lemma `lem:statpoly` (vertex ⇒ P_TT ≻ 0, Cramer, Hadamard);
  - Cor. `cor:height`;
  - Lemma `lem:snap` (1/Δ ≥ 4nτ, φ(s) ≤ 3/(8R) < 1/ρ);
  - Thm. `thm:transfer`;
  - Lemma `lem:unique-growth`;
  - Thm. `thm:exact`, including the claim that singular H_JJ calls can be skipped;
  - Remark `rem:cf` (1/√32 < 1/4);
  - Example `ex:polylimits`: (x−√2)^2(x+2√2) expands to x^3 − 6x + 4√2.
- **Section 10**:
  - Prop. `lim:prop:unique`, including γ ≥ ε, eq. `lim:eq:phigrowth`, and the requirement
    g ≤ 1/(n(n−1));
  - Cor. `lim:cor:nopolylog`;
  - Prop. `prop:lbwidth` (κ = κ̄ = 2);
  - Prop. `prop:lbproduct` (Appendix E: isolation probability ≥ 1/2, κ ≤ (kN)^{c₂}, and
    an N^{o(k)} running time);
  - Prop. `lim:prop:oracle`;
  - Prop. `lim:prop:messages` (the constants 4/3, 8/3 and 8);
  - Prop. `lim:prop:setgrowth`;
  - Prop. `prop:oraclebarrier`;
  - Prop. `lim:prop:constraints`.
- **Elsewhere**:
  - Prop. `prop:twocenters` (the 23M/100 bound and 0.23²/20 > 1/379);
  - Thm. `thm:cells` (K_S = 12r(2√(nκ_S)+1));
  - Prop. `prop:star` (A) and (B), including the eigenvalues 3 ± √5;
  - Prop. `prop:cv-limit`;
  - Prop. `prop:cv-ladder` (the expansion identity);
  - Example `ex:cv-fm` (all three pieces, σ = 2M);
  - Lemma `lem:proximal`(ii) (the constant 99/64).

**Exact-arithmetic checks.** I wrote two scripts in `process/w2/checks/`.
`R9_spotchecks.py` contains five checks, all of which pass:

1. The graded-grid example after Prop. `prop:tu-misaligned`: 11 nodes each, common nodes
   {0,1}, and (tu-gap) holds.
2. Prop. `prop:sharp` on four parameter sets with exact min-marginals: m_i(a) ≤ U holds
   within the stated radius.
3. Lemma `lem:graded`(b): no violation in 3000 random continuous and integer cases.
4. Example `ex:cr-star32`: V_h = (0, 23/32, 31/16) and corners
   (23/32, 27/32, 31/16, 31/16).
5. Example `ex:tu-sum`: corrected values 31/64 L, 51/64 L, 21/8 L, 175/64 L.

`R9_chain_start.py` re-runs the chain experiment from the other corner (§6).

**Verdict.** I found no false main claim and no invalid proof. The W1 verification
reports (`process/w1/*-report.md`) reached the same verdict. The correctness problems I
found are statements that say more than the theorems prove (see R2 and R10). They are not
errors in the proofs.

## 4. Clarity, writing and terminology

The prose is plain and precise, and it is mostly free of filler. A search for filler
words ("crucially", "notably", "it is worth noting", "leverage", "robust", ...) found
none. The problems are structural:

- **Abstract.** About 370 words, mostly a list of results; MP abstracts are normally
  150–250 words. The main theorem is only one of eight claims.
- **Introduction.** "Main results" (§1.1, three pages) and "Contributions" (§1.2)
  overlap almost completely.
- **Section 6 opening.** The first paragraph promises content that is in Section 9. Its
  scope sentence ("Throughout Sections 6.1–9.1", exact.tex:19) spans three sections.
- **Duplicated text.** Remark `rem:cluster` (growth.tex:243–253) repeats the
  related-work paragraph "Accuracy-independent work under growth" (related.tex:86–106)
  nearly verbatim.
- **Notation overload**, which affects reading:
  - 𝓡 means the *retained* coordinates in §7.3 (recourse-convex.tex:14) but the
    *residual* (eliminated) coordinates in §7.4 (recourse-cuts.tex:7–9). In §7.1,
    R = [n]∖K means the *recourse* coordinates.
  - P is {i : L_i>0} (setting.tex:50), the matrix ΔH (exact.tex:31), a leaf polytope
    (Def. `def:leaf`), the set 𝒫 in §7.5, and P(s).
  - R is a localization radius, a height constant and a set of rows.
  - γ is the weighted growth constant, the polytope right-hand side γ_t, a grid gap in
    Prop. `prop:tu-misaligned`, a complementarity margin in App. F, and monomial
    coefficients γ_m.
  - Lower bounds are written ℓ_i in §§3–6 and l_i in §§7, 9.
  - D, E, K, η, τ and g are each used for several unrelated objects.
- **Unnamed algorithms.** The paper has about ten procedures, each defined only in prose:
  - Algorithm 1 and CT;
  - EX and REC;
  - UC;
  - TU-GRID, TU-REC and TU-EXACT;
  - the "proximal iteration", the "core search" and "the procedure" of App. F.

  One of them, "FG", is used but never defined (optsets.tex:45, 92).
- **Terminology drift.**
  - "graded grids" vs "geometric grids" (§11 figures; App. B);
  - "nodes" vs "labels" vs "states";
  - "capped trials" vs "pruned-grid trials" (App. F);
  - "point growth" vs "quadratic growth".

## 5. Length and organization

**Page budget of the 104-page PDF:**

| Part | Content | Pages |
|---|---|---|
| Opening | Introduction and related work | 2–7 |
| Core | Sections 3–6 | 7–24 |
| §7 | Recourse | 24–48 (§7.3 alone is 10 pp.) |
| §8 | TU constraints | 48–59 |
| §9 | Several minimizers | 59–68 |
| §10 | Limits | 68–77 |
| §11 | Computation | 77–81 |
| Back matter | References | 82–91 (156 entries) |
| Back matter | Appendices A–G | 92–104 |

The main line is Sections 4, 5, 6.1–6.4, 10.1–10.3 and §11.1–11.3. It fills about 30
pages.

**Preferred option: split into two papers.**

- **Paper A** (about 40 pp. plus references):
  - §§1–6, with §6.5 reduced to Cor. `cor:poly` and Example `ex:polylimits`;
  - §9.1 (Prop. `prop:twocenters` and Thm. `thm:cells`);
  - §10.1–10.4;
  - §11.1–11.5;
  - Appendices A and E.
- **Paper B** (recourse, constraints and optimal sets):
  - §§7, 8, 9.2–9.3 and 10.5–10.6;
  - Appendices B, C, D and G.

**If the authors keep one paper**, these cuts would bring it to about 55–60 pages
including the appendices:

- **Delete:**
  - Appendix C (smoothed core count), with the text after Example `ex:cr-flat`;
  - Appendix F (implicit polynomial boundary output), keeping one sentence and the
    open question;
  - Lemmas `lem:cv-energy` and `lem:cv-envelope` and the paragraph "The
    negative-curvature target";
  - Cor. `cor:cv-nu`;
  - Remark `rem:cv-unstable`, reduced to one sentence;
  - §7.5 (concave–convex residuals, classical by the paper's own account), reduced to a
    remark with citations;
  - Remark `rem:cluster` (a duplicate);
  - the table of contents.
- **Move to appendices:**
  - proofs of Prop. `prop:star`, Prop. `prop:cert-exist` and Thm. `thm:cv-recog`;
  - Lemmas `lem:cv-bits` and `lem:cv-height`;
  - Example `ex:cv-fm` and Props. `prop:cv-ladder` and `prop:cv-limit`;
  - Lemma `lem:cr-height`, Thm. `thm:cr-exact` and Prop. `prop:cr-greedy`;
  - all of §8.6 (TU exact output, which parallels §6);
  - Prop. `prop:tu-misaligned` and Example `ex:tu-sum`;
  - Remark `rem:tu-hybrid`, which is only an outline;
  - Lemma `lem:diagcert`'s proof, Thm. `thm:diagdiscovery`, Prop. `prop:sshard` and
    Remark `rem:np`;
  - §10.6 with Appendix D;
  - Corollary `cor:local` with Appendix G.
- **Merge:**
  - §1.1 and §1.2 into one results section of at most two pages;
  - Lemma `lem:cr-semiconcave` into Lemma `lem:valuefunction`.
- **Add:**
  - one table that lists, for each result, the setting, the parameter, the bound and the
    certificate type;
  - formal algorithm boxes for Algorithm 1, CT, EX/REC and UC.

## 6. The computational section

The section is honest about its scope ("not a benchmark", "partly designed"). The
replayed certificates are a strength. As evidence for the claims in the introduction and
conclusion, however, it is thin:

1. **The chain never tests convergence to an off-grid minimizer.** In Table 1, the
   minimizer 0 is the lower corner of the box. It is the default starting point
   (solver `certified_grid.py:395`) and a node of every grid. So the incumbent is optimal
   from the first stage, with initial upper bound 0.
   - I re-ran m = 4, 8, 16 starting from the upper corner (`R9_chain_start.py`).
     Stages (12/16/25) and maximum nodes (6/8/9) were unchanged, and the state count
     rose by 3–8%. The starting point is therefore not what matters.
   - The real gap is that the family never tests convergence to a minimizer that is not
     a grid node. A variant whose minimizer is non-dyadic should be added.
2. **All instances are synthetic.** The families are a planted family, which by the
   authors' own description is certified by a quadratic minorant, plus the chain and
   tiny random instances.
   - No library or application instance with small width is solved. The two QPLIB
     attempts stopped before the first stage (widths 19 and 93).
   - The introduction motivates the method by process systems, energy networks and
     optimal control. One application family with small width would make the motivation
     concrete, for example a multiperiod chain-structured model. Its κ or κ̄ should be
     reported, or bracketed by certificates.
3. **The SCIP comparison is weak.** It covers one family, a 20-second limit, an epigraph
   formulation and three seeds. Either strengthen it (longer limits, a second solver,
   exact evaluation of reported bounds) or reduce it to a short remark about tolerance
   violations. The note that SCIP's primal bounds lie below OPT is useful and should
   stay.
4. **Inconsistent numbers.**
   - Section 6.6 (exact-localized.tex:96–98) reports 30 random instances, 29 accepted
     within four stages, and up to 542 stages for the height rule. Section 11.4 reports
     20 instances and at most 534 stages. These are different experiments (S1 vs E4 in
     `experiments/results/summary.json`).
   - Section 11 must describe S1. Otherwise §6.6 cites results that are not reported.
5. **The implementation is not the analysed algorithm.** It uses the Euclidean-κ
   variant, a common mesh, the cap 100θ^{-1}⌈log₂(n+2)⌉ and restarts at the incumbent
   (computation.tex:18–25). The paper says so. Figure 2 and the "≤ 0.4% of the cap"
   statement should name the cap they are compared with.

## 7. Recommendation

**Major revision.** I expect a revised version that is (i) split or cut to a focused
main line, (ii) precise in its abstract and introduction claims, and (iii) equipped with
a computational section that includes at least one non-designed family. Such a version
could be acceptable. The mathematics I checked is sound.

## 8. The ten most important required changes

| # | Severity | Location | Required change |
|---|---|---|---|
| R1 | major | whole paper (104 pp.) | Split into two papers, or cut as in §5 above, so the main text is about 45 pages. Section 7 alone is 24 pages, longer than the core (§§4–6). |
| R2 | major | abstract lines 30–32; intro.tex:109–114; constraints.tex:419–428; limits.tex:591–595 | The TU complexity claim is false as stated. The abstract says "polynomial complexity for fixed width", and the introduction says "polynomial for fixed width and conditioning". Prop. `lim:prop:constraints` with the remark after it (limits.tex:591–595) gives NP-hard TU instances with p = 3 and κ = 1. Thm. `thm:tu-approx` is polynomial only when W/η, d and r are also polynomially bounded. Replacement for the introduction: "the algorithm runs in polynomial time when the width p is fixed and κ_c, the scaled box widths W/η, the label counts d and the number r of optimal values per coordinate are polynomially bounded; it is not fixed-parameter tractable, and the pseudopolynomial dependence on W/η cannot be removed unless P = NP (Prop. 10.11)". Also qualify "the uniform meshes … are forced" to "are forced for corrections that depend only on curvature and the grids (Prop. `prop:tu-misaligned`)". |
| R3 | major | intro §1.1 opening; setting.tex §3.3; setting-growthcert.tex:42–58 | State the scope of the growth hypothesis in the introduction. For continuous box QP, growth at the minimizer forces H_SS ≻ 0 on the free face (Lemma `lem:growthcert`(b)), so the covered nonconvexity sits at active bounds or in integer coordinates. On hard instances κ is typically exponential in I (Prop. `lim:prop:unique`). Proposed sentence: "For continuous box QPs, quadratic growth forces the Hessian of the free coordinates to be positive definite at the minimizer; the nonconvexity our bounds cover lies in coordinates at active bounds and in integer coordinates." |
| R4 | major | abstract; intro.tex:72, 152; conclusion.tex:9; Remark `rem:fpt` | Make the "fixed-parameter tractable" claim precise. κ̄ is a real-valued, non-input parameter that is not known to be polynomial-time computable. Either state the bound "f(p,κ̄)·(I+q+1)^5 on every instance with weighted growth" without the FPT label, or define the notion and cite it. For example: "FPT with respect to the (not necessarily computable) structural parameter (p, ⌈κ̄⌉)". |
| R5 | major | computation.tex:100–141; Table 1; exact-localized.tex:96 | Computational section: (a) add a chain or planted variant whose minimizer is not a grid node; (b) add one non-designed family of small width with a reported κ bracket; (c) report experiment S1 behind §6.6 and reconcile it with §11.4 (30 vs 20 instances, 542 vs 534 stages); (d) strengthen the SCIP comparison or reduce it to a remark. |
| R6 | major | abstract (≈370 words); intro §§1.1–1.2 | Rewrite the abstract to about 200 words centred on Thms. `thm:approx` and `thm:exact` and the lower bounds. Mention the extensions in one sentence. Merge §1.1 and §1.2. Remove the table of contents. |
| R7 | major | recourse-convex.tex:14 vs recourse-cuts.tex:7–9 vs recourse-valuefn.tex:3; setting.tex:50 vs exact.tex:31; γ, R, D, ℓ/l throughout | Resolve the notation clashes. Use a single symbol for retained coordinates (e.g. K, as in §7.1) and another for eliminated or residual coordinates. Rename ΔH to an unused letter (e.g. Ĥ). Rename the polytope RHS γ_t to e.g. c_t. Use ℓ_i everywhere. Add a notation table in §3. |
| R8 | minor | recourse-balanced.tex:163–165; optsets.tex:45, 92; appendix-localized.tex:53; exact.tex:12–14, 19 | Remove internal artifacts and broken references. (a) "…in the cut-based recourse of the report" becomes "This removes the restriction to nonpositive residual diagonals in Section 7.4: …". (b) "FG" becomes "Algorithm 1". (c) "by (F)" becomes "by Proposition `prop:filter`". (d) exact.tex:19: "Throughout Sections 6.1–6.4"; delete the clause about unions of uniform cells in exact.tex:12–14 or point to Section 9.1. |
| R9 | minor | optsets.tex:440–446 (§9.2); recourse-convex.tex:429–432 (§7.3); intro.tex:146–149 | Attribute within the sections, not only in §2. Thm. `thm:endpointset` and Cor. `cor:facecsp` are Rosenberg's face criterion [Rosenberg1972] combined with the zero-residual (tree reparameterization) description of discrete optima [WainwrightJaakkolaWillsky2005, Werner2007]. Say so, and state that the new part is the tree-structured pattern problem and its 2^{O(p)} computations. In §7.3, contrast the value factors with Khajavirad's elimination of positive-diagonal components [Khajavirad2026PolyBox]. In contribution (i), call the cellwise identity an "observation". |
| R10 | minor | abstract line 24; intro.tex:131; limits.tex:16, 292, 344–352; conclusion.tex:14–15 | Make the lower-bound statements say what is proved. Prop. `prop:lbproduct` excludes exponents p/ψ(p) for unbounded ψ, i.e. the exponent cannot be o(p), on all-integer instances. Replace "must grow linearly with p" by "cannot be o(p) (on integer box QPs, under rETH)". In the conclusion, replace "the dependence on the condition number must be polynomial" by "cannot be polylogarithmic unless P = NP". |

## 9. Further findings

| # | Severity | Location | Issue | Fix |
|---|---|---|---|---|
| F1 | minor | recourse-valuefn.tex:46–58 | Lemma `lem:cr-semiconcave` restates Lemma `lem:valuefunction`(a) with a uniform L. The proof of Lemma `lem:cr-cell` cites `lem:valuefunction`(a) anyway. | Delete `lem:cr-semiconcave`. Note after `lem:valuefunction` that it applies to W_B with K = B. |
| F2 | minor | recourse-valuefn.tex:97–98 | "Part (a) explains why … part (b) why …" follows Lemma `lem:cr-cell`, so "part (a)" has no clear referent. | Move the paragraph directly after Lemma `lem:valuefunction` and write "Lemma 7.1(a)". |
| F3 | minor | recourse-convex.tex:341–343 (eq. `eq:cv-L`) | L_i can be negative, but Def. `def:curvature` requires L_i ≥ 0, and Thm. `thm:cv`(iii) uses L_i as a curvature bound. | Define L_i = max{0, (H_0)_ii − Σσ}, and keep the signed value for part (ii). |
| F4 | minor | Thm. `thm:cv`(iii) | The approximation part assumes growth in all original variables, including the private y. Growth of V alone suffices for the grid algorithm (Lemma `lem:valuefunction`(b) gives only one direction). | Assume growth of V for the approximation bound. Keep growth of F (uniqueness) only for exact output. |
| F5 | minor | growth-sharp.tex:45–48 vs Thm. `thm:cells` eq. `eq:cellcount` | The text claims "(2+√2)√(nκ)+7 labels per coordinate … (Theorem `thm:cells` with a single minimizer)", but Thm. `thm:cells` states K_S = 12r(2√(nκ_S)+1) = 24√(nκ)+12. | Prove the sharper count, or cite the stated bound: "at most 12(2√(nκ)+1) nodes per coordinate". |
| F6 | minor | growth.tex:243–253 | Remark `rem:cluster` duplicates related.tex:86–106. | Delete the remark, or reduce it to one sentence pointing to §2. |
| F7 | minor | Thm. `thm:diagdiscovery`(b),(c) (optsets.tex) | κ is not defined there. The section uses κ_S = max{1, L/g_S}. | Write κ_S. |
| F8 | minor | Prop. `prop:sshard`, last sentence | "the ratio κ … is not bounded by any polynomial" holds only unless P = NP. | Write "and, unless P = NP, the ratio κ_S of these instances is not bounded by a polynomial in I". |
| F9 | minor | conclusion.tex:45 | "Propositions~\ref{prop:tu-misaligned}" has one reference. | Write "Proposition~\ref{prop:tu-misaligned} and Example~\ref{ex:tu-sum}". |
| F10 | minor | appendix-smoothed.tex:2 | The appendix opens with "remove this effect", which refers to Example `ex:cr-flat` in another section. | Write "remove the effect of Example 7.x" (if the appendix is kept). |
| F11 | minor | computation.tex figures and §11.2; appendix-proximal.tex:19; appendix-boundary.tex | Terminology drift: "geometric grid" vs "graded grid"; "pruned-grid trials" vs "capped trials"; "labels" vs "nodes". | Use "graded grid", "capped trials" and "nodes" throughout, including figure legends. |
| F12 | minor | intro.tex:116–117 | "unions of uniform cells restore a polynomial bound for fixed width when the optimal set is finite": the bound is polynomial only if κ_S and r are polynomially bounded too. | Add "and κ_S polynomially bounded". |
| F13 | minor | abstract lines 26–29 | "private convex blocks with certified piecewise-affine responses, convex value factors": these are the same object. | Write "private convex blocks, eliminated as value factors whose curvature is certified by piecewise-affine responses". |
| F14 | minor | §11.7 (computation.tex:217–226) | "A first release of the code" is ambiguous. | Name the version and say whether the current code gives the same result. |
| F15 | minor | Section 7 opening (recourse.tex) | Section 7 has six subsections with no roadmap of which results the main theorems use. | Add a three-line roadmap. Mark §§7.2 and 7.5 as side results. |

## 10. Optional suggestions

- State in one place what the certificate contains and what the checker must trust:
  the curvature bounds, exact factor evaluation, and the decomposition. For polynomial
  factors, the interval curvature certificate of Lemma `lem:intcurv` must also be
  replayed.
- Discuss the size of the factor p^p. It comes from absorbing (log n)^p. Mention it in
  the conclusion together with open question (2).
- Explain why the graded grid is centered at the corrected minimizer rather than at the
  incumbent. The analysis uses ‖c−x*‖ ≤ 2√(κ̄a). The implementation centers at the
  incumbent.
- Add the related work on exact and safe MIP solving with certificate replay
  (e.g., Cook–Koch–Steffy–Wolter) next to Cheung–Gleixner–Steffy.
- In Example `ex:chain`, also report the Euclidean κ of the unit-box version measured in
  the experiments. This would show concretely that κ̄ matters.
- The conclusion's claim that corrected-grid bounds are "valid node bounds inside spatial
  branch-and-bound" is plausible but undemonstrated. Either show a small example or mark
  it as a possible use.

## 11. Commands run (targeted, local)

- `python3 process/w2/checks/R9_spotchecks.py`: five exact-arithmetic checks, all pass
  (output summarized in §3).
- `python3 process/w2/checks/R9_chain_start.py`: chain m = 4, 8, 16 from the lower and
  upper corners. All certified, all replays valid. The stage counts and maximum node
  counts are equal for both starts, and the state counts differ by 3–8%.

No project-wide verification was run. CI checks were not consulted.
