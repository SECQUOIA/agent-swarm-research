# Referee report (lens: senior MPC referee)

Manuscript: "Rigorous certificates for open MINLPLib instances and an audit of listed dual bounds", main paper `build/main.pdf` (62 pp.) and supplement `build/supplement.pdf` (138 pp.), built 2026-10-04 19:57.

**Recommendation: major revision.** The mathematics I checked is correct, and the results are unusually careful. In its current form the paper cannot be submitted. The headline table is clipped in the PDF, and the declarations are placeholders. Beyond that, the paper is about twice the length its content needs. The abstract frames three results more strongly than the evidence supports. The verification protocol does not say who wrote the "separately written" code.

Counts: 2 blockers, 7 major, 18 minor.

---

## 1. Summary of the submission

The authors take 43 nonconvex MINLPLib instances without a solved mark. They read the stored OSIL decimals as rationals and require exact feasibility. They report:

- 31 closures (relative gap at most 3.1e-9), 9 of them with exact optimal values;
- improved dual bounds for five waterno2 instances (factors 1.68 to 6.21) and ann_cumene_tanh;
- exact infeasibility of six KAN instances, with enclosures for a relaxed model;
- an audit of 11,086 listed per-solver dual bounds, 22 of which they prove invalid under a display hypothesis;
- a seed-dependent SCIP 10 propagation error with a 15-variable reproducer;
- invalid recorded bounds in the CAMINO data, and a false MINOTAUR infeasibility report;
- a one-hour run of BARON, Gurobi and SCIP.

Each certificate is built by hand from the model's structure. The paper states plainly that the mechanisms are classical and that no general solver is implemented.

## 2. Contribution and significance

The contribution is real and fits MPC, which has published benchmark-library papers (MIPLIB 2017, QPLIB). Three results stand out:

1. **Rigorous closures under a stated semantics**, including attractive exact results. These are the lnts linear-tangent law with a scalar root equation (Theorem 4.7), the camshape comparison/envelope theorem (Theorem 5.3) and the hvycrash identity (Proposition 5.13). They are short, checkable and of independent interest.
2. **The audit.** It is the first screen I know of that settles conflicts by proving that an exactly feasible point exists. Four of the refuted bounds are gross: glider100, topopt-cantilever_60x40_50 and methanol50 exceed the objective of an exactly feasible point by more than 1%.
3. **The SCIP defect.** It has a minimal reproducer and a traced mechanism (Lemma 8.4, Observation 8.5). This is useful to developers.

The significance of the 31 closures is uneven, and the paper says so in C1 and Section 3.4. For seven closures a floating-point closure or near-closure already existed, so the gain is rigor. Some other results depend on the chosen semantics: KAN infeasibility comes from coefficients rounded at the 1e-17 to 1e-15 level, and etamac's non-concavity from s = 1 + 4.14e-16. These are honest but narrow results. The paper is strongest when it stresses (a) the exact results, (b) the large dual-bound gains (12 of 31 closures had the best listed dual below U by more than |U|/2), (c) the audit and (d) the SCIP defect.

## 3. Originality against prior work

The positioning (Section 1.4, Section S3) is careful. The paper claims no new mechanism, credits Halbig et al. (2024) for convex MINLPLib certificates, and qualifies every priority claim with a search scope.

Two gaps remain:

- **Rigorous solvers as a baseline.** The paper does not discuss rigorous solvers such as IbexOpt (Trombettoni et al. 2011, cited only in S3) or GlobSol, nor why none was run. This matters for C7 (issue M2).
- **The split framework.** Section 4.1 is classical (Krotov, Lagrangian decomposition, SDDP-type cuts), and Appendix B proves extended-value versions of known results. That is fine as supporting material, but it does not justify 2.5 pages in the main text plus 4.5 pages of appendix (issue M1).

## 4. Correctness

What I checked myself (targeted checks only; no repository script was run; all computations in `/tmp`):

- **Appendix B, line by line.** Lemma 4.1(a)-(d); Lemma 4.2(b), including V(0) = 0 from positive homogeneity and superadditivity; Proposition 4.3(a)-(c); Proposition 4.4; Proposition 4.5, including the capped-potential construction for "best constants"; Lemma B.2, Proposition B.3 and the proof of Theorem 4.7. I found no error. Open item 1 of `development/open-items.md` asks for a separate check of the minorant induction and the finite potentials; my reading supports both.
- **lnts optimal values.** I recomputed them from (3) by mpmath bisection (numerical evidence): N = 50 gives 0.554668764938678898..., N = 100 gives 0.554595401166911161..., N = 400 gives 0.554572413700687108.... All match the brackets of Theorem 4.7.
- **camshape100.** I rebuilt v_100 from the OSIL constants in exact rationals (ū = 1.00015482411709, α = 1.86629266549889e-2, c = 1.99984519984971, c_0 = 3.14159265358979e-2). Checks K2 and K3 hold, and v_100 = -4.284147121746744... lies in the bracket of Table 2. I did not recheck feasibility of (E, d^E).
- **Lemma 8.4.** I confirmed a < fl(0.7)^3 < b exactly, with ulp(0.343) = 2^-54 and fl(0.7)^3 - fl(0.343) = -9.24e-17.
- **hvycrash witness.** κ = 6.5106e-3 < 6.52e-3; θ_{k-1} ≥ 2.617 > 2.6; -cos 2.6 = 0.8569; 50 fl(4.37e-3) - 0.2185 = -1.24e-17.
- **Spot checks of counts and displays.** Table 3 factors and δ; the ann δ = 0.19402% (shown as 0.195%); Table 6 class counts (11 margins above 1e-6, 4 above 1%, LINDO 13); 12 of 31 closures with the listed dual more than |U|/2 below U; 11 closures with δ ≤ 3e-13; 10 closures at level rerun. All agree with the text.
- **pindyck uniqueness.** P is not known to be convex, so uniqueness needs an interior argument. Section S1.5.5 supplies it (the ball B_ρ(p*) lies in P).

I found no mathematical error in the main text. The correctness concerns are about what the verification protocol guarantees (M3) and how replayable the rerun-level certificates are (M5), not about the mathematics.

## 5. Clarity and structure

**First two pages.** Section 1.1 and Box 1 (camshape800) motivate the work well: a concrete instance, a valid but weak listed dual, and a listed point below the optimum. The abstract and the first paragraph of Section 1 repeat each other, though, with six headline numbers each. A reader meets "closure" (Section 1.2, line 56) before the 1e-6 tolerance that defines it (Definition 2.4, p. 8).

**Readability for an expert.** The paper introduces at least twelve bespoke classification schemes (issue M7). An expert can follow each one, but holding them all at once is hard. The paper also presents 5.5 pages of bookkeeping (Section 2 plus Table 1) before the first certificate (p. 16).

**What confuses:**

- three notions of "listed dual": best single-solver, instance-list (third-best), and per-solver;
- four closure-like terms: closure, tolerance-level closure, fp closure, fp near-closure;
- the two KAN models, R_P and R;
- the three audit thresholds: half a unit, one unit, and 10/9 units (M6);
- "one certificate pattern" covering catmix, whose certificate the paper itself says is not an instance of Lemma 4.1 (m1).

## 6. Writing quality

The prose is plain, precise and free of the banned vocabulary. The weaknesses are structural:

- **Repeated caveats.** "Not a solve rate" appears 3 times in the main text. "To our knowledge, within the search ..." appears 5 times. "Separately written" appears 37 times. "We attribute no cause" and its variants appear 8 times.
- **A recurring "X, not Y" construction** (about 18 instances). Examples: "a consensus label, not a check"; "a bounded search, not a proof of priority"; "a lower bound ..., not a census"; "our explanation, not a measurement".
- **Scaffolding sentences.** For example: "Every mechanism ... predates this work. This holds for ... The same is true of ... It is also true of ..." (01-introduction.tex:170-173).
- **Lesson 1 is true by construction.** It is presented as a finding (M4).

Individually these are small. Together they make the text read as defensive and long.

## 7. Tables and figures

- **Table 2 is clipped in the PDF (B1).**
- **Table 1** is a full sideways page with a 10-line caption. Three of the six fields of each certificate box repeat it, and the "Replay" field repeats Table 8.
- **Table 7** is a sideways full page that is mostly empty. Its class column repeats Table 2.
- **Figure 1** is useful. However, the x-axis spans 50 decades, the legend has 7 marker types, and the KAN rows compare bounds for different models (the caption says so).

Details are in M1, m11, m13 and m14.

## 8. Reproducibility

The design is strong: the replay/regeneration distinction, the evidence levels, a number file with directed displays, and a claim register. The current artifact falls short of it (M5):

- no DOI;
- the claim index is stale (`development/open-items.md` §4);
- the archive "keeps the layout of our working tree" (I-reproduction.tex:23), with paths such as `$R/open-instances-wave3/...` and `$P/development/dossiers/...`;
- 10 closures, plus the waterno2, ann and KAN bounds, depend on rerunning searches whose trees are not stored; Section 10 admits that a different LP build can change whether a target is reached;
- the package versions of the original runs were not recorded consistently (10-reproducibility.tex:75).

## 9. Length and the main/supplement split

The main paper has 47 pages of body text, 7 pages of references and 8.5 pages of appendices. The supplement has 138 pages. The outline planned about 39 and 64 pages (`development/outline.md` lines 370 and 1071).

Page counts by section: Section 1, 5.5; Section 2, 6; Section 3, 4; Section 4, 8; Section 5, 8; Section 6, 2; Section 7, 4; Section 8, 3; Section 9, 3; Section 10, 1.5; Section 11, 2; Appendix A, 4; Appendix B, 4.5.

The main text should aim for about 30-35 pages; M1 lists where the cuts can come from.

---

## 10. Requested changes

### Blockers

**B1 (blocker). Table 2, the main results table, runs off the page; its caption opening and the three eg rows are not visible.**
- File: `tables/tab-closures.tex:4-56` (generated by `data/make_tables.py`); included at `sections/03-results.tex:13`.
- Problem: the sideways table is wider than the page. On p. 13 of `build/main.pdf`, the caption starts mid-sentence ("significant digits; δ = ∆/min(|L|,|U|) ..."). "Table 2: The 31 closures. Snapshot ..." is cut off. The last visible row is hvycrash, so eg_int_s, eg_disc_s and eg_disc2_s (source lines 53-55) are missing. LaTeX reports no warning.
- Evidence:
  - `pdftotext -f 13 -l 13 -raw build/main.pdf -` begins with "significant / digits; / δ".
  - `pdftotext -layout build/main.pdf` contains no "eg_int_s" table row and no "Table 2:".
  - Rendering p. 13 at 150 dpi shows the caption cut at the left edge and a partial row after hvycrash at the right edge.
  - The page MediaBox is A4 (595.28 × 841.89 pt).
- Fix:
  1. Shorten the caption to at most 4 lines. The class and prior-status legends can be defined once in the text of Section 3.2/3.4, or by pointing to Table 1 and Table 7.
  2. Drop the columns "n (n_int)/m" and "arith." (both in Table 1), or "class" (in Table 7).
  3. Alternatively, split the table into "attained exact optima and staged closures" and "other closures".
  4. Add a build check that greps the `pdftotext` output for "Table 2:" and for all 31 instance names.

**B2 (blocker). The declarations, archive and authors are placeholders.**
- File:
  - `main.tex:15` (`\author{}`);
  - `sections/01-introduction.tex:145`, `sections/10-reproducibility.tex:21`, `sections/11-conclusion.tex:77`, `:82` (`\archiveDOI`);
  - `sections/11-conclusion.tex:82, 87, 90` (`\TODO` licence, competing interests, funding).
- Problem: the printed PDF shows "[archive DOI]" and "[TODO: ...]". MPC's technical editor and the referees cannot assess reproducibility without the archive.
- Evidence: `/tmp/opus-main.txt` lines 230, 2482, 2658, 2663, 2671, 2674.
- Fix: deposit the curated archive (see M5) and insert the DOI. Fill in the licence (for example, "MIT for code, CC BY 4.0 for data"), the competing interests, the funding and the author list. This is the known decision D8; it must be closed before submission.

### Major

**M1 (major). The paper is about twice as long as its content needs, and much of the text repeats itself.**
- File: whole main paper; see the page counts in Section 9 of this report.
- Problem: an MPC reader must get through 47 pages of body text plus 8.5 pages of appendices. Several results are restated four to nine times:
  - the SCIP defect: `00-abstract.tex:13`, `01-introduction.tex:8`, `:67`, `:120-124`, `04-split.tex:359`, `:368`, Box 2 and Section 8.2, `11-conclusion.tex:37-38`, `A-semantics.tex:91`;
  - BARON on camshape: `01-introduction.tex:133-135`, `08-solvers.tex:11-24`, `09-interpretation.tex:43`, `11-conclusion.tex:39-40`;
  - prior status: C1, Section 3.4 and the Table 2 column;
  - "not a solve rate": `01:56`, `03:53`, `11:62`.
- Evidence: the 11 certificate boxes (`04-split.tex:165, 214, 251, 278, 302, 337, 370`; `05-other.tex:68, 132, 193, 242, 280`) repeat Table 1 (reading, implementations, level) and Table 8 (replay). The trust labels T-int to T-thm (`02-semantics.tex:169-177`) are used only in the supplement's claim register (27 uses in `I-reproduction.tex`, none elsewhere in the main text).
- Fix (target: 30-35 pages of body text):
  1. Cut C1-C9 (`01-introduction.tex:70-148`, about 2.5 pages) to five items of 2-3 lines each: closures; improved bounds; audit; solver and published claims; artifact. Keep the numbers in Section 3. This saves about 1.5 pages.
  2. Move Table 1, Section 2.4 (keep its first two sentences), the T-* list and Hypothesis H0's detail to the supplement. Keep a 6-row compact version of Table 1 (family, dual arithmetic, level). This saves about 3 pages.
  3. Delete the certificate boxes in the main text and keep them as "Certificate details" in Section S1. This saves about 3 pages.
  4. In Sections 4-5, keep the framework, lnts, dtoc5 and camshape as worked examples. Reduce optcdeg2, chain, catmix, lukvle10, waterno2, the Gibbs instances, pricing050, powerflow, etamac, pindyck, eg, ann and KAN to the statement plus a 3-5 line idea. This saves about 4 pages.
  5. Move Appendix B.1-B.5 (classical results) to the supplement and keep B.6 (the lnts proof). Move Appendices A.2-A.5 to the supplement. This saves about 6 pages.
  6. Cut Section 9 as in M4. This saves about 1.5 pages.
  7. Consider whether the audit (Section 7, Section S4) and the solver findings (Section 8) would serve readers better as a separate short paper. If they stay, Sections 7 and 8 together should fit in about 4 pages.

**M2 (major). The abstract and contributions C5 and C7 frame three results more strongly than the evidence supports.**
- File: `sections/00-abstract.tex:9, 12, 14`; `sections/01-introduction.tex:98-99, 130-136`; `sections/08-solvers.tex:131`.
- Problems:
  - (a) "In one-hour runs, BARON, Gurobi and SCIP closed no instance under exact feasibility" is true by construction. A floating-point solver returns points feasible only within a tolerance, so it cannot produce a closure in the paper's sense (Definition 2.4 needs a proof that x* ∈ F(M)). The informative facts are different: all 109 finite final dual bounds are weaker than the certificates, only five improve the listed dual, and BARON's two claims hold within tolerance. No rigorous (interval) solver was run, which is the baseline for which "closed under exact feasibility" would mean something.
  - (b) "we prove 22 ... invalid" gives no size breakdown. Eleven of the 22 are below MINLPLib's gap tolerance: eight class (i) bounds at 1.9e-9 to 3.4e-7 relative (`07-audit.tex:83`) and the three rocket bounds at 4.6e-8 to 1.9e-7 relative (Table S34, `E-audit.tex:504-506`). A reader of the abstract will assume gross errors.
  - (c) ann_cumene_tanh is presented as lacking a listed dual bound. Its algebraically identical twin ann_cumene_exp is closed in floating point by SCIP and LINDO at the value of our point (`B9-ann-kan.tex:156-157`). The rigorous gap is 0.195%, so this is the weakest result in the paper.
  - (d) The abstract does not say that for seven of the 31 closures the gain is rigor only.
- Fix, replacement abstract (about 230 words; numbers as in the paper):
  > MINLPLib lists tolerance-feasible points and solver-reported dual bounds, and marks an instance solved when three solvers claim global optimality; none of these records is a proof. We study 43 nonconvex instances without this mark, read the stored decimals as rationals and require exact feasibility. For 31 instances we prove a dual bound and exhibit an exactly feasible point within a relative gap of 3.1·10^-9; for nine we determine the optimal value exactly. For seven of the 31, floating-point closures or near-closures had been reported, so the gain there is rigor. For five pump-scheduling instances we raise the best listed dual bounds by factors 1.68 to 6.21, leaving relative gaps of at most 10.82%. The six Kolmogorov–Arnold network instances in our set have no exactly feasible point; without their partition-of-unity rows we enclose their optima within 2.42·10^-8. The certificates combine classical devices (Lagrangian and SDP duality, calibrations, Sturm comparison, hidden convexity, Taylor models) with exact or outward-rounded evaluation; apart from named exceptions, a second, separately written implementation rechecks them. Of the 11,086 per-solver dual bounds that MINLPLib lists, we prove 22 invalid under a stated hypothesis on page displays: four by more than 1%, seven by 1.2·10^-5 to 7.4·10^-5 relative, and eleven by less than MINLPLib's gap tolerance of 10^-6. We report a seed-dependent SCIP 10 error that returns wrong optimal values on waterno2 subproblems. In one-hour runs, every finite dual bound of BARON, Gurobi and SCIP was weaker than ours; BARON's optimality claims on two instances hold only within its tolerance. Code, certificates and points are archived.
- Fix, replacement for C7 (`01-introduction.tex:130-136`):
  > **C7 (one-hour runs).** We ran BARON 26.5.27, Gurobi 13.0.2 and SCIP 10.0.3 on all 43 instances (one thread, 3600 s, requested gaps 10^-9). All 109 finite final dual bounds are weaker than our certified bounds, and five improve the best listed dual. BARON claimed optimality on camshape100 and camshape200; its dual bounds are valid and lie within 4.80·10^-7, relative, of the exact optima, but its returned values lie below the optima (tolerance-level closures, Section 2.3). Floating-point solvers return points that are feasible only within a tolerance, so the runs measure how close their dual bounds come; they do not rank the solvers.
- Fix, C3: move ann_cumene_tanh out of the abstract, or keep it with the clause "whose exp twin SCIP and LINDO close in floating point".
- Fix, Section 1.4 (`01-introduction.tex:166`): add rigorous solvers (IbexOpt; GlobSol is already cited). Either run one of them on the 43 instances or state why it was not run.

**M3 (major). The paper does not say who wrote the "separately written" implementations or who "the verifier" is, so the central independence claim cannot be assessed.**
- File: `sections/02-semantics.tex:191-206`; `sections/11-conclusion.tex:1-2` (comment: "No AI-use statement (revision decision 8)") and `:79-90`; `main.tex:15`.
- Problem: rigor rests on "every computer-assisted dual certificate has at least two separately written implementations" (`02:197`). The phrase appears 37 times. The supplement contrasts "the authors' code" with "the verifier's code", but the verifier is never identified, and the author list is empty. The development records show that the second implementations and the critic passes were AI-agent work:
  - decision register G-09: "Distinguish 'reproduced by a separate implementation in this project (AI agent)' from a human review";
  - O-3: "the critics' passes are AI-agent reviews and should be described as such";
  - outline §8, item 10, forbids "'Independent' without the definition and the AI-agent disclosure".

  Decision D7 dropped the disclosure. Springer Nature's editorial policy requires LLM use beyond copy-editing to be documented in the methods. A reader also needs this to judge what "separately written" protects against: a shared misreading by two sessions with shared context is the common-mode risk that `02:206` names.
- Evidence: `development/decision-register.md` rows G-09 and O-3; `development/outline.md` §8 item 10 and §9 D7; `development/labels.md:48`.
- Fix:
  1. Add to Section 2.6, after line 192, a factual paragraph. Template, to be completed by the authors:
     > The first implementations were written by [persons / AI coding agents directed by the authors]. The second implementations were written by [ ... ] in separate sessions that had the model files and the statements to be proved but not the first code. "Separately written" therefore protects against independent coding errors; it protects less against a misreading shared through the statements both sessions received. No implementation was reviewed by a person outside the project; [name] read [which] codes.
  2. Add an "Use of AI tools" paragraph to the Statements and declarations, and a statement that the authors take responsibility for all results.
  3. Use the same words in Section S7.

**M4 (major). Section 9 and Lesson 1 present untested interpretation as a finding, and Lesson 1 holds by construction.**
- File:
  - `sections/01-introduction.tex:58-62` (Lessons 1 and 2);
  - `sections/09-interpretation.tex:13-65`;
  - `tables/tab-structure.tex` (Table 7);
  - `sections/11-conclusion.tex:41, 74-75`.
- Problem: "In every closure the decisive step was a bounding argument fitted to the structure of the model" cannot be otherwise: every certificate was built by hand from the structure. The informative part is that little search remained afterwards. The paper says it "did not test our interpretation ... by experiment" (`09:16`). Yet the reading that termwise relaxations, free variables and long equality chains held these instances back drives a solver recommendation (`11:41`) and the conclusion (`11:74-75`). The experiment that would test it is cheap: add the derived enclosures of Remark 4.6 as variable bounds and rerun.
- Evidence: `09:15-17`, `09:55` ("this is our explanation, not a measurement"); C8 at `01:142`.
- Fix, either option:
  - (a) Run the test. Give SCIP 10.0.3 and BARON 26.5.27 one hour each on chain50-chain400, optcdeg2, lukvle10 and waterno2_06 with the Remark 4.6 enclosures as bounds (about 14 CPU-hours), and report the final dual bounds next to Table S40.
  - (b) Cut Section 9 to at most one page, drop Table 7 (its class column is in Table 2), and remove the stage-structure recommendation from Section 11.1 or label it as untested.
- Fix, either way, replacement for Lesson 1:
  > 1. Once a bound fitted to the structure of the model was in place, little search remained: branching was absent in 12 closures and at most three-dimensional in 15 more; the pindyck certificate splits one box into 9, and the three eg certificates branch on their 7 original variables. Section 9 offers an interpretation, not tested by experiment, of why general-purpose solvers did not find such bounds.

**M5 (major). The artifact is not yet in a form an MPC technical editor can replay.**
- File: `sections/10-reproducibility.tex:21-48, 75`; `sections/I-reproduction.tex:23` and the claim register; `artifact/README.md`.
- Problems:
  1. No DOI (B2).
  2. The claim index is stale. `development/open-items.md` §4 reports that `artifact/check_claims.py` fails on the hashes of files edited since 17:17 on 2026-10-04.
  3. The archive "keeps the layout of our working tree" (`I-reproduction.tex:23`). The register points into `$R/open-instances-wave3/...`, `$R/reviews/wave2-small-verification/...` and `$P/development/dossiers/...` (17 dossier paths), with environment variables such as `EG_AUDIT_R` (`artifact/README.md`).
  4. Ten closures (lukvle10, chain50-chain400, ex6_2_5, ex6_2_7, eg ×3), plus the waterno2, ann and KAN bounds, are at level "rerun". Section 10 says a different LP build "can change ... in principle, whether the stored target is reached" (`10:33`).
  5. The versions and libm/BLAS dispatch of the original runs were not recorded consistently (`10:75`).
- Fix:
  - (i) Curate the archive: one directory per family, each with `README`, `replay.sh` (tier 1/2/3), expected output and recorded time, and neutral directory names; no "wave", "dossier" or "critique" paths.
  - (ii) Rebuild and validate the claim index after the last edit.
  - (iii) Where storage permits, archive leaf partitions with per-leaf certificate data (multipliers, LP duals). chain, lukvle10 and ex6_2_* are small; eg already records its trees; ann has about 1.85 million regions. Replay then becomes a stored check that needs no search and no LP solver, and those results move to level "stored".
  - (iv) Replay Tier 1 and Tier 2 on a second machine with a different BLAS, and report the outcome in Section S7.

**M6 (major). The audit's hypothesis and classes use three thresholds and one mixed class, which obscures what the "stated hypothesis" in the abstract assumes.**
- File: `sections/07-audit.tex:19-25, 32-56, 110`.
- Problem:
  - Class (i) is defined by a margin above half a unit (`07:21`).
  - Proposition 7.1(a) needs at least one unit under Hypothesis H, or 10/9 unit under the weaker rounding-chain assumption of Lemma S4.1(a) (`07:45-46`).
  - The text then notes that every class (i) margin is at least 1.115 units and every (i-r) margin is below 0.44 units (`07:55`).
  - Only rocket100 (1.06 units) actually needs H (`07:110`).
  - Class (ii) mixes "proved valid" with "repair (evidence, not proof)" (`07:23`).
- Evidence: `07:55-56`, `07:110`.
- Fix:
  - Define class (i) as "margin at least u(s)". No class changes, because no margin lies in [0.44, 1.115) units.
  - Split class (ii) into "(ii) proved valid" and "(ii′) not refuted (repair; evidence only)".
  - Replace `07:55-56` with:
    > Every class (i) margin is at least 1.115 u(s) > (10/9) u(s), so the 19 class (i) refutations need only that the display arises from the reported number by decimal roundings or truncations (Lemma S4.1(a)); of all 22 refutations, only rocket100 (1.06 units) needs Hypothesis H itself.
  - State the same in C5 (`01:110-112`).

**M7 (major). There are too many bespoke taxonomies for one paper.**
- File: `sections/02-semantics.tex` throughout; `01:130-148`; `tables/tab-closures.tex:9-18`; `sections/07-audit.tex:19-25`.
- Problem: a reader must hold at least these at once:
  - readings (a)/(b)/(c);
  - categories A/B;
  - audit classes (i)/(i-r)/(ii)/(iii);
  - six certificate classes;
  - seven prior-status codes;
  - arithmetic tags [E]/[I]/[F];
  - trust labels T-int/T-fp/T-mp/T-read/T-code/T-thm;
  - evidence levels hand/stored/rerun;
  - Tiers 1/2/3;
  - proved / verified by a separately written implementation / computed;
  - Hypotheses H0 and H;
  - closure / tolerance-level closure / fp closure / fp near-closure;
  - best listed dual / instance-list dual / per-solver dual;
  - R_P / R.
- Fix:
  1. Add a half-page glossary table at the end of Section 2 (term, meaning, where it is used).
  2. Move the T-* labels and the Tier names to the supplement; they are used only there and in Section 10.
  3. Define "best listed dual" against "instance-list dual" once, in Section 2.1 "Listed data", and use only "best listed dual" in the main text. Section 3.1 (`03:43`) is the only main-text use of the instance-list dual; move it to Section S3.4.
  4. Replace "fp near-closure" with the gap itself in the Table 2 column, for example "fp, ≤0.01%".

### Minor

**m1 (minor). Lesson 2 calls the 15 staged closures "one certificate pattern: a split of the objective", but catmix is not a split.**
- File: `sections/01-introduction.tex:63`; `sections/04-split.tex:8`; `sections/11-conclusion.tex:75`.
- Problem: `04:70` states that Lemma 4.2 (catmix) is not an instance of Lemma 4.1. Table S1 lists catmix as using "concave chord minorants".
- Fix, replacement:
  > 2. Fifteen closures exploit the stage structure of the model: eleven split the objective along the stages (Lemma 4.1), and the four catmix certificates bound the value functions of a backward dynamic program (Lemma 4.2); in both, every stage problem is small enough to be minimized rigorously (Section 4).

**m2 (minor). "Closure" is used before it is defined.**
- File: `sections/01-introduction.tex:53-56`.
- Fix: in line 53, write "A closure (a certified relative gap of at most 10^-6, MINLPLib's tolerance; Definition 2.4) then needs two certificates: ...".

**m3 (minor). The first paragraph of the introduction repeats the abstract.**
- File: `sections/01-introduction.tex:5-8`.
- Fix, replacement:
  > MINLPLib marks an instance solved when three solvers claim global optimality within a tolerance. We ask what can be proved about 43 nonconvex instances without this mark when the stored decimal data are read as rational numbers and feasibility is exact, and what the same standard says about the library's listed dual bounds and about solver output. Section 1.3 lists the results.

**m4 (minor). One phrase overstates MINLPLib's role.**
- File: `sections/01-introduction.tex:13`.
- Fix: replace "MINLPLib, the reference against which MINLP solvers and methods are measured," with "MINLPLib, a standard benchmark library for MINLP solvers,".

**m5 (minor). The "used as facts" paragraph mixes uses of MINLPLib records with solver claims.**
- File: `sections/01-introduction.tex:22-26`.
- Problem: the CAMINO and Karia et al. examples are solver claims, not uses of MINLPLib records.
- Fix: open the paragraph with "These records, and solver claims of the same kind, are nevertheless used as facts."

**m6 (minor). A scaffolding paragraph repeats "Every mechanism ... This holds for ... The same is true of ... It is also true of ...".**
- File: `sections/01-introduction.tex:170-174`.
- Fix, replacement:
  > Every mechanism in our certificates is classical: Lagrangian decomposition [cites], Krotov- and Mangasarian-type sufficiency [cites], discrete Sturm comparison [cite], the Gibbs tangent-plane test [cites], hidden convexity [cite], SDP relaxations of optimal power flow [cites], Taylor models and affine arithmetic [cites], interval existence tests [cites] and rational PSD certificates [cite]. What is new are the instance-specific constructions, their exact or outward-rounded evaluation on the stored models, and what they show about benchmark data and solver claims.

**m7 (minor). Inverted sentence.**
- File: `sections/01-introduction.tex:62`.
- Problem: "Why general-purpose solvers did not find such bounds we can only interpret".
- Fix: use the Lesson 1 replacement in M4.

**m8 (minor). One sentence about library functions is too broad.**
- File: `sections/02-semantics.tex:158`.
- Problem: "No displayed result assumes an error bound for a floating-point library function" sits beside results that trust mpmath's interval functions (T-mp). One audit proof also uses "mpmath at 90 digits with a relative widening of 10^-60" (`E-audit.tex:513`).
- Fix: replace it with:
  > No displayed result assumes an accuracy bound for the elementary functions of NumPy, the C library or Intel SVML; mpmath's interval functions are trusted where Table 1 shows [I].

**m9 (minor). The definition of level "rerun" does not fit eg.**
- File: `sections/02-semantics.tex:179`; `tables/tab-trust.tex` (eg row).
- Problem: "rerun" means the tree is not stored. For eg the trees are recorded (`B7-eg.tex:265, 295`; `F-eg-rounding.tex:359`), and only the per-leaf LP certificates are recomputed.
- Fix: add a sentence. "For eg the leaf partition is stored and checked for coverage; only the per-leaf certificates are recomputed." Or introduce a level "stored partition".

**m10 (minor). Parts of Section 4.1 and Appendix B are not used by any certificate.**
- File: `sections/04-split.tex:79-81, 113`; `sections/G-proofs-split.tex:180-189, 252-303`.
- Problem: Proposition 4.3(c) ("forced slopes") and the second half of Proposition 4.5 ("SP is the largest value of B over cellwise-affine splits", with about 1.5 pages of proof) explain but certify nothing.
- Fix: move both to the supplement and keep one sentence each in the main text.

**m11 (minor). The certificate boxes duplicate Table 1 and Table 8.**
- File: see M1, item 3.
- Fix: as in M1, item 3.

**m12 (minor). Table 3 uses an undefined term.**
- File: `tables/tab-unclosed.tex:11`.
- Problem: footnote a uses "separator branching", which the main text does not define. Section S1.8 calls the step "one slope vector per link and 113-162 cells per link" (`B8-waterno2.tex:263`).
- Fix: write "(one slope per separator on a 113-162-cell partition, δ ≤ 3.78%)", or drop the intermediate value.

**m13 (minor). Figure 1 mixes models and is hard to read.**
- File: `sections/03-results.tex:15-26`; `figures/make_fig_headline.py`.
- Problem: the KAN rows compare bounds for R with listed bounds for the stored models (the caption admits this). The axis spans 10^-45 to 10^10, and the legend has 7 marker types.
- Fix:
  - Drop the KAN rows, or show them in a separate panel.
  - Cap the axis at 10^-20 with a break mark for dtoc5 and pindyck.
  - Drop the hollow-triangle variant; state it in the caption.

**m14 (minor). Table 7 is a sideways full page that is mostly empty.**
- File: `tables/tab-structure.tex:4`.
- Problem: the class and instance columns repeat Table 2, and the "termwise relaxation" column is untested interpretation.
- Fix: remove it (see M4), or set it upright at `\footnotesize` with three columns: class, structural feature, branching.

**m15 (minor). The text addresses the referee.**
- File: `sections/10-reproducibility.tex:46`.
- Fix: replace "the order of magnitude a referee should expect" with "the order of magnitude to expect".

**m16 (minor). Report the SCIP defect and the invalid bounds upstream before submission.**
- File: `sections/08-solvers.tex:98`; `sections/01-introduction.tex:124`; Section 7.
- Problem: "To our knowledge ... had not been reported (SCIP issue tracker searched on 2026-10-02)" will be outdated by the time of review.
- Fix: file the fm336 reproducer with the SCIP developers and cite the issue number (decision D4). Send the 22 refuted bounds to the MINLPLib maintainer and ask for the stored per-solver values; with those values, Hypothesis H could be checked or dropped.

**m17 (minor). C2's novelty claim is weak, and C2 overlaps C1.**
- File: `sections/01-introduction.tex:86-92`.
- Problem: "What is new is the points themselves and their re-proofs" is a weak statement.
- Fix: merge into C1 as one sentence:
  > Every primal value is the upper end of a rigorous enclosure at a point proved exactly feasible; for 13 closures the floating-point points that first indicated a closure violate rows by 2.4·10^-20 to 7.91·10^-12, and we replace them using classical existence tests (Section 6).

**m18 (minor). The selection funnel takes main-text space but supports no claim.**
- File: `sections/03-results.tex:40-54`.
- Problem: the paper says it does not claim that small width made these instances hard or easy (`03:50`), yet the funnel takes about 15 lines.
- Fix: keep three sentences. "We chose the 43 instances from the 155 nonconvex instances that are open by a stricter rule than MINLPLib's (Section S3.4), in two rounds, by judged tractability; two closures (camshape100, lnts50) were not open by that rule. The 29 closures among the 155 are therefore not a solve rate." Move the remainder to Section S3.4.

---

## 11. Checks run for this review

All checks were targeted, run by this reviewer in `/tmp`; none of them is CI.

- `pdftotext -layout` of `build/main.pdf` and `build/supplement.pdf`, read in full for the main paper and in part for the supplement.
- `pdftoppm` renders of main pp. 1, 11, 13, 14, 36 and 42; crops of p. 13 (B1); `pdfinfo -box` for p. 13.
- `grep` of `build/main.log` for overfull or float warnings: none.
- Python with `fractions` and `mpmath`:
  - lnts optima for N = 50, 100 and 400 by bisection (numerical evidence);
  - camshape100 v_n and checks K2/K3 from the OSIL constants (copied to `/tmp/opus-ref/`, exact);
  - Lemma 8.4 (exact);
  - hvycrash constants (exact);
  - Table 3 factors and δ;
  - ann δ.
- Phrase counts with `grep` over the main-text sources.
