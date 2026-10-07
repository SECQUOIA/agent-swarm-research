# Referee report (R-referee, round w4): overall assessment for Mathematical Programming

**Manuscript:** "Decomposition-aware global optimization: certified coordinate grids,
conditional recourse, and structural limits".

**Version reviewed:** sources `sections/*.tex` as of 2026-10-03 (about 12:00) and the build
`/tmp/dpaper/out/main.pdf` (123 pages; main text pp. 1-80, references pp. 80-91, appendices
pp. 92-123). Page numbers come from `/tmp/dpaper/out/main.aux`. Line numbers refer to the
individual source files.

**Recommendation: major revision, for length and organization only.** I found no error in the
mathematics. The claims in the abstract, introduction and conclusion now match the theorems.
The one remaining obstacle is length: the paper has grown from 104 to 123 pages, and the main
text is still about 78 pages. The mathematical content is ready.

---

## 1. Summary

The paper studies min F(x) = sum_a f_a(x_{S_a}) over a mixed-integer box, with a supplied tree
decomposition of maximum bag size p and upper coordinate curvatures L_i.

1. **Corrected grids (Sec. 4).**
   - Subtracting the unary correction L_i w_i(v)^2/8 at each node turns the minimum over a
     product grid into a valid lower bound. This bound equals the best Bajaj-Hasan vertex bound
     over all cells (Prop. `prop:cellwise`).
   - Two-pass min-sum dynamic programming computes the bound and all min-marginals, and the
     min-marginals give a safe filter (Prop. `prop:filter`).
   - The stage grids, one bound and one feasible point form a path certificate, which a checker
     verifies by recomputation (Thm. `thm:certificate`).
2. **Accuracy-independent grids (Sec. 5).**
   - Assume weighted growth with the scale-invariant condition number κ̄. Then filtered grids
     graded around the corrected minimizer keep O(√κ̄ log(n+2)) nodes per coordinate
     (Lemmas `lem:inv`, `lem:states`).
   - The capped trials of CT remove the need to know the growth constant. CT gives a certified
     2^{-q}-approximation in f(p,κ̄)(I+q+1)^5 bit operations (Thm. `thm:approx`).
3. **Exact output (Sec. 6).**
   - Stationary-polytope height bounds, an acceptance rule and snapping recovery give the exact
     minimizer in f_1(p,κ)(I+1)^{C_1} (Thm. `thm:exact`).
   - Also in this section: localized acceptance and fixed-degree polynomial factors.
4. **Extensions (Secs. 7-9):**
   - value functions and convex or cut recourse;
   - balanced quadratics without a decomposition;
   - totally unimodular (TU) coupling constraints;
   - several minimizers: two-center hardness, unions of uniform cells, the optimal set of
     coordinatewise concave QPs, and discovery under a diagonal certificate.
5. **Lower bounds (Sec. 10).**
   - NP-hardness with p = 3, a unique minimizer and log κ = O(I).
   - ETH at κ ≤ 2.
   - Under rETH, the exponent of κ cannot be o(p).
   - The value-oracle exponent p/2.
   - Further limits: exponential messages, set growth, product domains and local moments.
6. **Computation (Sec. 11).** An exact-rational reference implementation with an independent
   checker, run on planted, chain, random unplanted and exact-output families, with a SCIP
   comparison and recourse diagnostics.

## 2. Significance and novelty

**Strengths:**

- The main theorem is a certified algorithm with running time f(p,κ̄)·poly(I+q), together with
  exact output in f_1(p,κ)·poly(I). Neither growth constant is an input. I know of no earlier
  result of this form for nonconvex or mixed-integer box QP.
- The technical step from XP to an f(p,κ̄)·poly bound is the combination of graded grids and
  coordinatewise filtering. It is new.
- Prop. `prop:sharp` and Cor. `cor:uniformgrid` show that the step is needed, since uniform
  grids keep order √(nκ) nodes. The graded lower bound in Cor. `cor:uniformgrid` shows that
  Θ(√κ̄ log n) is attained.
- The lower bounds give a coherent picture:
  - κ cannot become log κ;
  - p cannot be dropped;
  - the exponent of κ cannot be o(p) under rETH;
  - p/2 is optimal for value oracles.
- The certificates are independently checkable and do not use growth. This is useful in its own
  right, as the SCIP tolerance observations illustrate.

**Limits of the contribution:**

- The paper now states these limits honestly.
- The growth hypothesis amounts to a well-conditioned unique minimizer.
- On hard instances κ is exponential in I, and the paper makes no claim about κ on application
  models (intro.tex:145-150).
- Several extensions are classical constructions placed inside the certified-grid framework. The
  paper says so (Remarks `rem:cr-cut-prior`, `rem:cv-instances`, `rem:shor`).

I consider the core contribution (Secs. 4-6 and 10.1-10.3) of a quality appropriate for
Mathematical Programming.

## 3. Correctness

**Proofs re-derived line by line.** No error found in any of them.

- **Prop. `prop:cellwise` (a)-(c)** (grids.tex:55-111).
  - Concavity after subtracting (L_i/2)(x_i - mid J_i)^2, including the case of integer
    intervals of length one.
  - The bijection between (cell, vertex) pairs and (grid point, choice of incident interval).
  - Part (c) with coordinate i held fixed.
- **Prop. `prop:filter` and Thm. `thm:certificate`** (grids.tex:208-290).
  - Both alternatives of (C1).
  - The argument that a filtering run with feasible thresholds yields a valid certificate.
- **Lemma `lem:inv`** (growth.tex:71-124). I checked:
  - the energy inequality (`eq:energy`), using L_i h_ij^2 ≤ η_j^2;
  - (ii) at j = 0 for every first center;
  - (iii): Y ≤ (4/15)(γ^{-1}+k)a ≤ (8/15)ka;
  - (iv): (1/4 + 5/16)a = (9/16)a;
  - (v): Z ≤ ((13/15)γ^{-1} + (4/15)k)a ≤ (17/15)ka.
- **Lemma `lem:states`** (growth.tex:130-175).
  - The radius constant is 3 + 2√(17/15) + (2+√(17/15))/√2 = 7.2961 < 7.3.
  - θR/ĥ ≤ 4√(2n_P) + 1/4.
  - φ(1) = 16.21 and φ(2) = 18.55, and the derivative comparison 4/m ≤ 7.2/m holds for m ≥ 2.
- **Thm. `thm:approx`** (growth.tex:199-263; App. A, appendix-growth.tex:115-144). I checked:
  - the termination argument in (a), including integer coordinates with h_ij < 1;
  - μ* and 2^{μ*} ≤ 4√2·√κ̄;
  - Σ_μ K_μ^p ≤ 2K_{μ*}^p;
  - (`eq:logabsorb`) via sup t^p e^{-t};
  - the denominator invariant Γ_X 2^α, the bit length b ≤ c(1+μ2^μ)(I+q+1) and μ* ≤ 3(1+log₂κ̄);
  - the final (I+q+1)^5.
- **Lemma `lem:commonmesh`** (proof in App. A). I checked (G1)-(G5): 4.148 < 4.2, ψ(1) < 12.4,
  ψ(2) < 14.4, and termination.
- **Prop. `prop:sharp`, Cor. `cor:uniformgrid`** (App. A).
  - The bound 2g(Λ-g)a²/Λ.
  - The induction on ρ_j, including the case (ν+1)h_j > 1.
  - 4ν+5 ≥ √((n-2)κ)+1 and the graded lower bound.
- **Sec. 6.**
  - Lemma `lem:statpoly`: kernel argument, Cramer's rule, Hadamard's inequality.
  - Cor. `cor:height`.
  - Lemma `lem:snap`: 1/Δ ≥ 1/R = 4nτ, φ(s) ≤ 3/(8R) < 1/ρ, and no nonsingularity used.
  - Thm. `thm:transfer`, Lemma `lem:unique-growth`, Thm. `thm:exact`, including the claim that
    calls with singular H_JJ may be skipped.
  - Prop. `prop:local` and Cor. `cor:local` (App. B.1: the 3.6 and 5 radii, (5/5.2)Γ ≥ Γ/2,
    the Schur complement, δ_X ≥ 1/R and λ_A ≥ 1/(ΔR)).
  - Remark `rem:cf`, Lemma `lem:intcurv`, Prop. `prop:lattice`, Cor. `cor:poly`.
  - Example `ex:polylimits`: (x-√2)²(x+2√2) = x³ - 6x + 4√2.
- **Prop. `lim:prop:unique`** (limits.tex:61-167).
  - The split identity (`lim:eq:split`); σ_k ∈ [-A,2A]; the path inequality.
  - Uniqueness of the vertex minimizer; the gap ≥ λ; Jensen's inequality for concave Φ.
  - The growth constant g = λ/(m(1+2(m-1)‖a‖²)) < 1/(m(m-1)); L = 4 and the bound on κ.
- **Cor. `lim:cor:nopolylog`, Prop. `lim:prop:oracle`, Prop. `prop:lbwidth`** (κ = κ̄ = 2;
  floor(Ψ̃/2^n) = -α for every value within 1/2).
- **Prop. `prop:lbproduct`** (App. G.2).
  - The encoding forces exactly one ζ_l = 1 per pair.
  - The weight bound W_0 - 1; κ, I ≤ (kN_0)^{c₂}.
  - Isolation with probability ≥ 1/2. Because the error is one-sided, the composition with
    sparsification remains valid.
  - The ψ' construction for the corollary on f(p)κ^{a(p)}I^C, and a(p) = p/2 + 2.
- **Elsewhere:**
  - Lemma `lem:growthcert` (a), (b); Example `ex:family` (a)-(c); Example `ex:chain` (20δ² and
    the rescaled bounds);
  - Prop. `prop:twocenters`; Thm. `thm:cells` (K_S = 3·2r(4√(nκ_S)+2));
  - Lemma `lem:tu-round`, Prop. `prop:tu-sound`, Thm. `thm:tu-states`, Lemma `lem:tu-statpoly`
    (|det K| ≤ (√2 n_c C)^{n_c}), Lemma `lem:tu-snap`;
  - Prop. `prop:tu-misaligned` with its instance (75L/288), Example `ex:tu-sum` (31L/64 and the
    seven feasible grid points), Example `ex:tu-union` (g_S = 1/6, L̄ = 12);
  - Lemma `lem:leaf`(b) and Prop. `prop:vf-curv`; Prop. `prop:star` (A) and (B), with U_G,
    corner minima, κ ≤ 2(3+√5);
  - Thm. `thm:cr-search` and Prop. `prop:cr-growth`; Example `ex:cr-flat`; Lemma `lem:chaincut`;
  - Lemma `lem:endpointid` and Cor. `cor:facecsp`; Lemma `lem:diagcert`(i) (the identity checked
    coordinatewise); Lemma `lem:proximal`(ii) (the constant 99/64, hence 99/256 Lnh²);
    Thm. `thm:diagdiscovery`(b); Prop. `prop:sshard`;
  - Prop. `lim:prop:messages`, Prop. `lim:prop:setgrowth`, Prop. `prop:oraclebarrier`,
    Prop. `lim:prop:constraints`.

**Exact and numerical checks** (`process/w4/checks/R-referee-spot.py`; all pass):

1. The constants of Lemma `lem:states` and of Lemma `lem:commonmesh` (G4)-(G5), for m up to 10⁶.
2. Prop. `prop:twocenters`: β ≤ -max{θ²M²/379, h²/20} on 300 random graded grids, in exact
   arithmetic.
3. Prop. `prop:cv-limit`: a grid estimate of L_K/g_K for M = 1, 4, 16 and for each admissible
   retained set K. All estimates exceed (4M - 1/2)/3; the closest is 21.68 vs 21.17 at M = 16.

**Consistency of claims.**

- The abstract, Thm. `thm:intro-main`, Thm. `thm:intro-lower`, Table `tab:results`, Remark
  `rem:fpt` and the conclusion agree with the theorems they cite.
- The numbers of experiment S1 agree between Sec. 6.5 (exact-localized.tex:131-139) and
  Sec. 11.6 (computation.tex:334-357): 29/30 accepted, within nine and five stages; 40-72 stages;
  542.
- The 21-315 bit range in exact-localized.tex:5 agrees with computation.tex:322.
- The replay ratio range 0.81-2.54 is consistent with Tables `tab:chain`, `tab:scip` and
  `tab:recourse`.
- The build has no undefined references and no overfull boxes.

## 4. Clarity, length and organization

The prose is plain and precise, and the notation table (setting.tex:145-184) helps. The
procedures are now ten numbered algorithm environments: TRIAL, CT, REC, EX, CORE, TU-GRID,
TU-EXACT, UC, PROX and DISC. Two structural problems remain.

**Length.** Page budget from main.aux:

| Part | Pages |
|---|---|
| §1-2 | 1-10 |
| §3-6 | 10-31 |
| §7 | 31-44 |
| §8 | 44-53 |
| §9 | 53-62 |
| §10 | 62-71 |
| §11 | 71-78 |
| §12 | 78-80 |
| References (176 entries) | 80-91 |
| Appendices | 92-123 |

- The core (Secs. 3-6 and 10.1-10.3) is about 26 pages.
- Secs. 7-9 and 10.4-10.7 add about 36 pages to the main text.
- The decision to keep one paper is deliberate (process/w3/CONVENTIONS.md), and I do not
  re-request a split. Within one paper, however, the main text should still be cut substantially
  (finding R-referee-1).

**Introduction.** §1.1 and §1.2 were merged, but the "Results" subsection still runs from p. 2 to
p. 7. Two of its parts repeat material that appears elsewhere:

- The extension paragraphs repeat the openings of Secs. 7-9.
- The lower-bound summary appears six times (finding R-referee-2).

## 5. The computational section

The section is careful and honest about its scope. Every certificate on which a claim rests was
replayed. Compared with the previous round:

- **Off-grid minimizers are now tested.**
  - The planted free coordinates are k/21 (computation.tex:97-124). It is explained why 11% of
    them nevertheless became nodes.
  - The chain was rerun from the upper corner (computation.tex:278-283).
- **E6 is new** (computation.tex:201-264): unplanted random instances. Growth is certified, and κ
  is bracketed, on 11 of the 40.
- **Experiment S1 is reported** and agrees with Sec. 6.5.
- **The SCIP comparison** now evaluates SCIP's incumbents exactly and covers 60-second runs and
  tighter tolerances. It is framed as "not a performance ranking".

What is still missing is any application-derived instance with continuous nonconvexity and small
width. The opening paragraph of the introduction motivates the method by such applications
(finding R-referee-5). Given the honest scope statements (intro.tex:148-150 and
computation.tex:5-7), I regard this as minor.

## 6. Status of the required changes R1-R10 of the previous report (process/w2/R9-referee.md §8)

**R1. Length (split, or main text of about 45 pp.): not resolved (partly addressed).**

What was done:
- Appendix C (smoothed count) is no longer input; appendix.tex does not include
  appendix-smoothed.tex.
- Deleted: `rem:cluster`, `lem:cv-energy`, `lem:cv-envelope`, `rem:tu-hybrid`, and the table of
  contents.
- Moved to appendices: `lem:cr-height`, `thm:cr-exact`, `prop:cr-greedy`, `prop:cert-exist`,
  `lem:cv-bits`, `lem:cv-height`, `ex:cv-fm`, `prop:cv-ladder`, `cor:cv-nu`, `rem:cv-unstable`,
  and the proofs of `thm:cv-recog`, `cor:local` and `prop:star`.

What remains:
- The main text still runs to p. 80 (previously about 81).
- The PDF grew from 104 to 123 pages, and the references from 156 to 176 entries.
- See R-referee-1.

**R2. TU complexity claim: resolved.**
- The abstract no longer states TU complexity.
- intro.tex:252-261 and constraints.tex:458-475 give the exact conditions (κ_c, s/η and r
  polynomially bounded), say "not FPT", and cite `lim:prop:constraints` for the pseudopolynomial
  level-0 grid.
- "Forced" is replaced by "give invalid bounds with curvature-only corrections"
  (intro.tex:262-264, constraints.tex:16-18).

**R3. Scope of the growth hypothesis in the introduction: resolved.**
- See intro.tex:137-150 and Remark `rem:nonconvex`.
- A logical slip remains in the wording: the location of negative curvature already follows from
  minimality. See R-referee-3.

**R4. Precise "fixed-parameter" claim: resolved.**
- The abstract and conclusion state the bound without the FPT label.
- intro.tex:124-135 and Remark `rem:fpt` (growth.tex:265-285) explain the sense.
- A one-sentence precision about which κ̄ is the parameter is still missing (R-referee-6).

**R5. Computational section: partly resolved.**
- (a) Resolved (§5 above).
- (b) Partly resolved: E6 is unplanted, but there is no application family (R-referee-5).
- (c) Resolved: S1 is in §11.6 and consistent with §6.5.
- (d) Acceptable: one solver, framed as an illustration, with exact evaluation of SCIP's bounds.

**R6. Abstract of about 200 words; merge §1.1/1.2; remove the TOC: partly resolved.**
- The abstract has about 250 words plus formulas (previously about 370). It is centred on the
  main theorems, with one sentence on the extensions.
- The sections were merged and the TOC removed.
- "Results" is still about 6 pp. rather than at most 2 (R-referee-2).

**R7. Notation clashes: partly resolved.**
- 𝓡 now means recourse/residual consistently (recourse.tex:8-10, recourse-cuts.tex:4-6).
- ΔH was replaced by Ĥ (exact.tex:32).
- γ is now used only for weighted growth.
- ℓ_i is used everywhere.
- A notation table was added (setting.tex:145-184).
- Overloads of e_i, η, J, R and r remain (R-referee-4).

**R8. Internal artifacts ("of the report", "FG", "by (F)", "Throughout Sections 6.1-9.1"):
resolved.** A grep finds none of these strings.

**R9. Attribution inside the sections: resolved.**
- optsets.tex:458-474 credits Rosenberg, Wainwright-Jaakkola-Willsky and Werner, and states what
  is new.
- Remark `rem:cv-instances` (recourse-convex.tex:255-271) contrasts the method with Khajavirad.
- intro.tex:53 calls the cellwise identity "the observation".

**R10. Lower-bound statements say what is proved: resolved.**
- limits.tex:362-379 and intro.tex:179-198 say "cannot be o(p) ... integer box quadratics, under
  rETH".
- conclusion.tex:14-18 says "cannot be polylogarithmic".

## 7. Status of the further findings F1-F15

| # | Status | Evidence |
|---|---|---|
| F1 | resolved | `lem:cr-semiconcave` deleted (no label in sections/) |
| F2 | resolved | recourse-valuefn.tex:42-45: "Lemma 7.1(a) explains why ...", placed right after the lemma |
| F3 | resolved | recourse-convex.tex:184-186 defines L_i^+ = max{L_i, 0} and uses L^+ in (iii) |
| F4 | resolved | recourse-convex.tex:197-206: approximation under growth of V, exact output under growth of F |
| F5 | resolved | growth-sharp.tex:50-54 now cites 12(2√(nκ)+1) from Thm. `thm:cells` |
| F6 | resolved | `rem:cluster` deleted; one pointer sentence at growth.tex:177-178 |
| F7 | resolved | `thm:diagdiscovery` uses κ_S throughout (optsets.tex:597-611) |
| F8 | resolved | `prop:sshard`(ii) says "unless P = NP ... no polynomial π" (optsets.tex:636-643) |
| F9 | resolved | conclusion.tex:64-65: "Proposition ... and Example ..." |
| F10 | resolved (moot) | Smoothed appendix removed from the build. The orphan file sections/appendix-smoothed.tex still exists and contains the undefined reference `lem:cr-charge`; delete it from the submission sources |
| F11 | resolved | No "geometric grid", "pruned-grid" or "labels per coordinate" in the sources; figure legends say "graded" |
| F12 | resolved | intro.tex:276-277: "polynomial in n, r, κ_S and I+q" |
| F13 | resolved | The abstract no longer lists the item; intro.tex:230-232 uses the suggested wording |
| F14 | resolved | The ambiguous "first release" statement is gone from §11 |
| F15 | resolved | Roadmap at recourse.tex:15-31, marking side results |

The optional suggestions of the previous report were also taken up:
- The checker's trust base is stated at grids.tex:282-290 and constraints.tex:320-326.
- The centring at the corrected minimizer is explained at growth.tex:60-66.
- Cook-Koch-Steffy-Wolter is now cited at related.tex:90.
- The Euclidean κ of the rescaled chain is reported (Example `ex:chain`).
- The branch-and-bound claim is marked as untested (conclusion.tex:21-25).

## 8. Findings of this round

### R-referee-1 (major): the main text is still about 78 pages; the length target of R1 is not met

**Where:** whole paper.
- §7 (pp. 31-44), §8 (pp. 44-53), §9 (pp. 53-62) and §10.4-10.7 (pp. 67-71) together form about
  36 pages of extensions in the main text.
- The total is 123 pages (previously 104), with 176 references.

**Problem:** A reader of Mathematical Programming must cross 50 pages of extensions to see the
whole paper, and the paper exceeds the usual length of even long MP articles by a factor of
about two. The previous report made this its first required change. The revision moved proofs
into appendices but kept almost all statements and discussion in the main text.

**Fix (keeping one paper):** move the following to the appendices or to an online supplement,
leaving a one-paragraph summary with the statements' labels in the main text.

- §7.2 "Local corrections need exact recourse" (recourse-local.tex:1-147). Keep the statement of
  Thm. `thm:cr-filter`, which §7.4 uses, and one sentence on Prop. `prop:star`.
- From §7.3:
  - the paragraph "Recognizing a globally affine response" together with Thm. `thm:cv-recog`
    (recourse-convex.tex:282-302);
  - the paragraph "Limits of global recourse curvature" together with Prop. `prop:cv-limit`
    (recourse-convex.tex:304-345). Keep one sentence in the main text.
- From §8:
  - §8.6 except the paragraph stating the constants (eq:tu-constants) and Thm. `thm:tu-exact`
    (constraints.tex:477-571);
  - Prop. `prop:tu-misaligned`, its instance and Example `ex:tu-sum` (constraints.tex:590-650).
    Keep one sentence and the reference.
- §9.3 (optsets.tex:476-660). Keep Remark `rem:shor` in shortened form and the statement of
  Thm. `thm:diagdiscovery`.
- §10.4-10.7 (limits.tex:381-701). Keep the four propositions as statements with one sentence
  each. Their proofs are 1-2 pages each.
- §11:
  - drop the E3 paragraph (computation.tex:189-199), or merge it into E2;
  - merge §11.5 and §11.6;
  - shorten §11.9.
- Remove the duplicated novelty sentence. It appears at intro.tex:109-112 and at
  related.tex:54-56; keep one.

Together with R-referee-2, this should bring the main text to about 50-55 pages. The appendix
order would follow the sections, as it does now.

### R-referee-2 (minor): the introduction's "Results" subsection is still about six pages and repeats material

**Where:**
- intro.tex:37-297 (pp. 2-7).
- The paragraphs "Exact messages" (152-158), "Conditional recourse" (219-246), "Coupling
  constraints" (248-268) and "Several minimizers" (270-294).
- The lower-bound summary "unless P=NP neither parameter can be dropped ... cannot be o(p)"
  appears six times: abstract.tex:20-23, intro.tex:194-198, growth.tex:279-284,
  limits.tex:14-23, conclusion.tex:14-18, and in Thm. `thm:intro-lower` itself.

**Problem:**
- R6 asked for a results section of at most two pages.
- The four extension paragraphs each restate the opening of the corresponding section, including
  attributions that the sections already contain (optsets.tex:458-474, Remarks
  `rem:cr-cut-prior`, `rem:cv-instances`, `rem:tu-bm`).
- Table `tab:results` already lists every extension with its hypotheses and bounds.

**Fix:**
- Keep Thm. `thm:intro-main`, Thm. `thm:intro-lower`, the paragraphs "Parameterized form" and
  "Scope", and Table `tab:results`.
- Replace intro.tex:152-158 and 219-294 by one paragraph of at most 15 lines. Suggested opening:
  "The method extends in three directions, summarized in Table 1: exact or certified recourse for
  eliminated variables (Section 7), totally unimodular coupling constraints with mesh-aligned
  data (Section 8), and several minimizers (Section 9). Section 10 shows what fails without each
  hypothesis; Section 11 reports an exact-arithmetic implementation."
- State the lower-bound summary only in Thm. `thm:intro-lower` with the paragraph after it, and
  in §10. In growth.tex:279-284 and conclusion.tex:14-18, replace it by a reference to
  Section 10.

### R-referee-3 (minor): the scope paragraph attributes to growth a restriction that minimality already implies

**Where:** intro.tex:137-145; setting-growthcert.tex:59-70 (Remark `rem:nonconvex`).

**Problem:**
- The paragraph opens with "Growth restricts where nonconvexity can occur" and then concludes:
  "The nonconvex instances covered by our bounds therefore have their negative curvature in
  directions that involve active bounds or integer coordinates."
- But Lemma `lem:growthcert`(b) (setting-growthcert.tex:24-25) proves H_{J_0J_0} ⪰ 0 at every
  global minimizer of every box QP, without growth. So every box QP has its negative curvature
  (as seen from a global minimizer) in such directions, with or without growth.
- What growth adds is:
  1. definiteness of this block, with a quantitative lower bound;
  2. uniqueness of the minimizer (of x*_P under weighted growth);
  3. the exclusion of flat and nearly flat directions and of near-ties, which is what κ and κ̄
     measure.
- As written, the paragraph tells the reader the wrong thing about which instances the hypothesis
  excludes. The "therefore" is not false, but it is vacuous as a restriction.

**Fix.** Replace intro.tex:138-145 (from "Growth restricts" to "(Example~\ref{ex:family}).") by:

> "At a global minimizer of a box QP, the Hessian block of the continuous coordinates strictly
> inside their bounds is positive semidefinite, so negative curvature always involves active
> bounds or integer coordinates (Lemma~\ref{lem:growthcert}(b)). Growth adds three things. It
> makes this block positive definite: point growth bounds it below by $2gI$, and weighted growth
> by $2\gamma\diag(L_i)$. It makes the minimizer unique (in $x_P$ for weighted growth). And it
> excludes nearly optimal points far from the minimizer, which is what $\kappa$ and $\bar\kappa$
> measure. Instances with growth can still have exponentially many strict local minima
> (Example~\ref{ex:family})."

Adjust the first three sentences of Remark `rem:nonconvex` in the same way.

### R-referee-4 (minor): remaining symbol overloads

**Where and what:**

- **e_i** is the exponent with 4^{e_i-1} < L_i ≤ 4^{e_i} (growth.tex:35-36,
  appendix-growth.tex:118-125, appendix-recourse-convex.tex:22). It is also the unit vector in
  Def. `def:curvature` (setting.tex:50), Lemma `lem:valuefunction` (recourse-valuefn.tex:20-34)
  and Prop. `prop:vf-curv` (recourse-convex.tex:141). In addition, e_j is the CORE allowance
  (recourse-cuts.tex:173) and e_i(v_i;x_i) appears in §9.2 (optsets.tex:273).
- **η** has three meanings: the scale η_j (growth.tex:37), the TU mesh unit (constraints.tex:37)
  and the proximal weight η = Lθ²/4 (optsets.tex:547).
- **J** has four meanings: a grid interval (grids.tex:16), the stage limit (growth.tex:41), the
  free set of REC (exact.tex:187-188) and the last TU level (constraints.tex:417). The notation
  table lists only the first two.
- **R** has two meanings: the height constant (exact.tex:33; the notation table) and a radius
  (growth.tex:23, 28; growth-sharp.tex:45; appendix-growth.tex (G5) "R = 4.2ρh").
- **r** has four meanings: r_i = 2^{-e_i} (growth.tex:36), r_i or r = the number of optimal
  values per coordinate (constraints.tex:337, optsets.tex), r = the number of private blocks
  (§7), and r_{ij} (recourse-cuts.tex:65).

**Problem:** The previous R7 asked for these clashes to be resolved. The exponent e_i and the unit
vector e_i coexist in Sec. 5 and App. A, close to Lemma `lem:valuefunction`, which uses both
kinds of index.

**Fix:**
- Rename the exponent e_i to ϖ_i (unused in the paper), and r_i = 2^{-e_i} to ϱ_i or 2^{-ϖ_i}.
  Check that ϱ is free in Sec. 5; it is used in PROX.
- Rename the proximal weight in PROX to ω (or keep η and add it to the notation table with its
  section).
- Rename the REC free set to J_f.
- Use ρ or "radius" wording for the local radii R.
- Add the remaining double uses to Table `tab:notation`.

### R-referee-5 (minor): no application-derived instance, although the introduction is motivated by applications

**Where:** intro.tex:3-8 (process systems, energy networks, optimal control); computation.tex:5-7
and 454-470.

**Problem:**
- All continuous instances are planted, chain, random or designed.
- The only library instances (QPLIB_3852 and QPLIB_5881) are binary, so for them the method is
  plain dynamic programming.
- Item (b) of the previous R5 is therefore met only by unplanted random instances. The paper says
  so honestly (intro.tex:148-150), so this is not a misstatement. But readers cannot tell whether
  the class with moderate κ̄ and small width contains any modelled instance.

**Fix (either):**
- (a) Add one small-width continuous or mixed family taken from a model library, for example a
  multiperiod chain or a pooling or network instance from MINLPLib/QPLIB with bag size at most 4
  after presolve. Report its κ bracket by Lemma `lem:growthcert`(a)/(b), or report that growth
  could not be certified and give the measured node counts.
- (b) Add to computation.tex:5-7 the sentence: "We did not find library instances with
  continuous nonconvex terms and decompositions of bag size at most four; the families below
  are therefore synthetic."

### R-referee-6 (minor): the parameter in the "fixed-parameter" statement should be the best κ̄ of the instance

**Where:** intro.tex:124-131; growth.tex:265-271 (Remark `rem:fpt`); setting.tex:98-103.

**Problem:**
- By the convention at setting.tex:98-103, κ̄ is defined from *some* valid weighted-growth
  constant, and a result "holds for every valid constant".
- A parameterization in the sense of parameterized complexity must be a function of the instance.
  "The parameters p and ⌈κ̄⌉" is therefore ambiguous as written.
- The intended object exists and is unique. Weighted growth determines x*_P (setting.tex:121),
  ‖x - x*‖_L depends only on x_P, and the set of valid γ is a closed interval (0, γ*]. So
  κ̄* = max{1, 1/γ*} is a well-defined function of the instance, and the bound holds with it.

**Fix.** After "fixed-parameter bound in the parameters p and ⌈κ̄⌉" (intro.tex:129-130 and
growth.tex:270), add: "where $\bar\kappa$ is taken as the smallest weighted condition number of
the instance, $\max\{1,1/\gamma^*\}$ with $\gamma^*$ the largest valid constant in
\eqref{eq:wgrowth}; this maximum exists because the set of valid constants is closed."

## 9. Recommendation and prioritized list of remaining required changes

**Recommendation: major revision, limited to length and organization.**
- The mathematics is correct as far as I checked (§3), and the main claims are now stated
  precisely.
- Once the main text is cut to about 50-55 pages, I would expect to recommend acceptance after a
  light check.

**Required changes, in order of priority:**

1. **R-referee-1 (major).** Cut the main text to about 50-55 pages by moving the listed
   extension material to the appendices or a supplement.
2. **R-referee-2.** Shorten "Results" to at most 3 pages, and state the lower-bound summary only
   in the introduction and in Sec. 10.
3. **R-referee-3.** Correct the logic of the scope paragraph (intro.tex:137-145) and of Remark
   `rem:nonconvex`.
4. **R-referee-6.** Define the parameter κ̄ in the FPT statement as the best constant of the
   instance.
5. **R-referee-4.** Remove the remaining symbol overloads (e_i, η, J, R, r).
6. **R-referee-5.** Add one application-derived family, or state explicitly that none was
   tested.
7. **Housekeeping.** Delete the orphan sections/appendix-smoothed.tex from the submission
   sources.

## 10. Commands run (targeted, local)

- `python3 process/w4/checks/R-referee-spot.py`: 10 checks, all pass (output in §3).
- Grep and aux checks:
  - section page numbers from /tmp/dpaper/out/main.aux;
  - 123 pages (pdfinfo);
  - 0 overfull boxes and no undefined-reference warnings in /tmp/dpaper/out/main.log;
  - label/reference cross-check (the only unresolved reference is in the orphan
    appendix-smoothed.tex);
  - greps for the R8 artifacts and for the F11 terminology;
  - pdftotext of the figure legends;
  - 176 bibliography entries.

No project-wide verification was run. CI was not consulted.
