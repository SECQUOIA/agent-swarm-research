# Review round 2: referee and handling editor (Journal of Global Optimization)

Manuscript: "Certified support cuts for shared nonlinear expressions and quadratic blocks"
(`main.tex`, `sections/*.tex`; `main.pdf`, 56 pages). I read the typeset text in
`development/draft-round2/main.txt`. Its sources and PDF are identical to the current
`sections/` and `main.pdf`; I checked this with `cmp`. Page numbers below are PDF pages.

**Recommendation: major revision.** No theorem and no reported number is wrong. Five
changes are needed before acceptance:

1. Correct two overstated conclusions. The "representation, not strength" reading holds
   only for three-variable paths, and it is false for four-variable paths (F1). The claim
   that the cuts work "only if" whole-row directions are tried first is contradicted by the
   paper's own data (F2).
2. Shorten the paper (F3).
3. Connect the star algorithm to the solver, or present it as a theoretical result (F4).
4. Measure certification against the uncertified alternative a solver developer would
   actually use, or qualify the claim (F5).

The remaining findings are minor. If these changes are made, I expect the paper to be
acceptable.

---

## 1. Overall assessment

**Contribution.** The paper makes three contributions.

1. *Limits of composing pair hulls* (Section 3, pp. 5-11):
   - the 1/128 path witness, with a separating cut in the model's own coordinates;
   - the interleaving dichotomy for family (6): the gap is either 0 or δ²/2;
   - the alternation criterion for κ-moment interfaces, which the paper correctly presents
     as a reading of the classical description of Radon partitions on the moment curve;
   - a 100% relative gap for every κ;
   - the observation, via Burer-Natarajan-Willemsen (BNW) Theorem 1, that a dense Shor
     relaxation with McCormick inequalities closes every three-variable path;
   - an exact minimax description (Proposition 3.5(ii)) of the gap of the glued
     relaxation in any star direction.
2. *Exact support for constrained stars* (Section 4.2, pp. 12-14). An exact rational
   O(m₀ + (m+k) log(m+k)) algorithm when rows couple the center with one leaf at a time,
   with a matching lower bound for algebraic computation trees when m = Θ(k). The
   box-constrained case is a special case of Del Pia and Khajavirad's forest algorithm,
   and the paper says so.
3. *A certified separator in the original variables* (Sections 5-8):
   - classical Lagrangian aggregation cuts;
   - a four-part validity contract (C1)-(C4) for the stored binary64 row;
   - a SCIP implementation with fresh-process replay;
   - four campaigns run under protocols fixed in advance, plus one post hoc diagnostic
     that is labeled as such.

**Novelty.** Moderate, and stated with care. The novelty claims are qualified with "to our
knowledge" and positioned against the right prior work:
- 03-composition.tex:280-285 (Section 3.4, p. 9);
- 04-quadratic.tex:212-213 (p. 14);
- 02-setting.tex:135-137 (p. 5);
- the introduction.

The relevant prior work includes Tawarmalani 2010, Breen 1973, Karlin-Studden, BNW 2025,
Dey-Khajavirad, Del Pia-Khajavirad, Chen-Luedtke, Neumaier-Shcherbina, Borradaile-Van
Hentenryck, Eifler-Gleixner and Brierley et al. The paper correctly labels as classical:
the support description, Lagrangian closure, Bernstein and ball bounds, safe rounding,
face enumeration and oracle separation. The stored-row check (C4) is a small but useful
engineering observation that I have not seen stated before; the paper motivates it with
SCIP's coefficient snapping in `lp.c`.

**Correctness.** The round-1 math lenses checked every theorem with exact scripts. I re-derived:
- Proposition 3.5(ii): Sion's theorem applied over the compact product of pair hulls; the
  nested example with re-split pair minima 3/4 and -1/4; the three-leaf example with Δ = 2/3;
- Proposition 5.5 (free remainders) and both hierarchy examples of Section 5.3;
- identity (7) and the BNW reduction;
- the solved counts and medians of Table 5 from Tables 11-12.

All are correct. The one substantive problem is a generalization made in the prose, not in
a theorem (F1).

**Significance.** A JOGO reader gains three things:
- a clean, quantitative explanation of why pairwise exact relaxations of quadratic paths
  miss strength, and when denser relaxations recover it;
- a certified-cut method that a solver developer can reuse, including the observation that
  the row the solver stores must be checked;
- an honest computational finding. On MINLPLib the cuts are neutral for SCIP, and SCIP's
  own disabled separators are stronger. On constructed families with the predicted
  structure, the cuts turn time-outs into solves.

The star algorithm is clean but has no use in the solver (F4). The positive result rests
on a separable, constructed family. That family has a convex perspective reformulation
which Gurobi solves in under a second for 19 of 20 instances (F10).

**Presentation.** The prose is plain and precise, with little filler. The post hoc versus
prospective distinction is defined (08a-setup.tex:6-9) and applied consistently in
Section 8. The remaining presentation problems are:
- overstated summary sentences (F1, F2, F7, F8, F9);
- length (F3);
- two figures with overlapping labels (F14);
- missing front matter (F15);
- a few counts that cannot be checked from the tables (F16).

**Computational evidence.**
- *Validity: strong.* I re-read every `replay.json`: 7,498 + 30,998 + 104,771 = 143,267 cuts,
  all `passed: true`. However, 138,000 of these (96.3%) are path-family cuts; only 5,267
  are MINLPLib cuts (F11).
- *Uncertified ablation (Part U).* It shows that sample minima and SLSQP constants would
  have cut off feasible points and known optima. It omits the strongest uncertified
  alternative, a numerical global solve (F5).
- *Usefulness: honest but narrow.* Campaign 4 closed most of the design gaps from round 1:
  the missing cell of the 2×2 design, fresh seeds, a binding row, native comparators,
  Gurobi, Part D (larger models) and Part U.

**Length and balance.** The PDF has 56 pages:

| Part | Pages | Length |
|---|---|---|
| Main text | 1-32 | 31.5 pp |
| References (112 entries) | 32-40 | 8 pp |
| Appendices | 40-56 | 16 pp |

Within the main text:

| Section | Pages |
|---|---|
| §1 | 1-3 |
| §2 | 3-5 |
| §3 | 5-11 |
| §4 | 11-14 |
| §5 | 15-18 |
| §6 | 18-20 |
| §7 | 20-22 |
| §8 | 22-31 |
| §9 | 31-32 |

Round 1 asked for 21-24 pages of main text. The structure has improved, but the main text
grew by about one page and the appendices doubled (F3). An editor could reasonably suggest
splitting the work in two: (a) Sections 3-4, the composition limits and exact oracles, and
(b) Sections 5-8, the certified separator and its evaluation. I do not require a split if
the paper is shortened.

---

## 2. Status of every round-1 finding (`evidence/review-round1.md`)

Status codes:
- **R**: resolved.
- **P**: partially resolved.
- **N**: not resolved.

Locations refer to the current files. Every P or N item is taken up again in Section 3
(findings F1-F20).

### R1-math (18 items)

| # | Round-1 issue | Status | Where now / what remains |
|---|---|---|---|
| 1 | [major] Star bound omits rows in y alone (m₀) | P | Fixed in Thm 4.4 (04-quadratic.tex:129), its proof and the intro (01-introduction.tex:65). The abstract (00-abstract.tex:12) still says O((m+k)log(m+k)) → F6. |
| 2 | σ₀ bookkeeping in star bit lengths | R | A-star.tex: τ = max over 0..k; endpoint sentence. |
| 3 | "δ²/2 exactly when interleave" | R | Thm 3.2 statement; intro :50-52. |
| 4 | Existence of PSD completion | R | App. C.3 cites Grone et al. |
| 5 | Sec. 7 hypotheses (W, rational F, R>0) | R | App. E: start point p₀, F(P∩Qᵈ)⊆Qʳ, ρ = 0 case in Thm E.2. |
| 6 | Anstreicher-Burer cited too broadly | P | The dimension statement is now right. The citation placement attributes the simplex and 2-D box hull results to Shor and Sherali-Adams (02-setting.tex:100-104) → F17. |
| 7 | Intro "optimal" qualifier | R | 01-introduction.tex:66-68. |
| 8 | "Counts attained" | R | "tight up to a constant factor" (p. 14). |
| 9 | min vs inf in Prop. 5.1 | R | (12) uses inf. |
| 10 | Prop. D.2 domain, symbol reuse | R | Rows gᵣ; statement over D. |
| 11 | Chord correction needs C² | R | Lemma D.3, Sec. 6.2. |
| 12 | Envelope notation | R | vex/cav (Cor. 5.3). |
| 13 | Fig. 1(b) caption | R | figures/chords.tex caption. |
| 14 | First inclusion strict | R | D = [0,2] example, Sec. 5.3. |
| 15 | Pairwise-intersection example | R | Three-leaf example, Δ = 2/3. |
| 16 | Why ε > 0 | R | App. E, √2 example. |
| 17 | Lagrangian-dual wording | R | Sec. 5.2 "dual bound ... equals the optimal value of its convexification". |
| 18 | Symbol reuse | R | κ, r, ρ, θ, ht, τ. The remaining reuse of Δ (Prop. 3.5, Prop. 6.1, Lemma E.3) is harmless. |

### R2-math (15 items)

| # | Round-1 issue | Status | Where now / what remains |
|---|---|---|---|
| 1 | [major] Thm 3.3 is about zero bounds, not exactness | R | 03-composition.tex:210-221 (κ = 3 example, 6103/16128). |
| 2 | [major] BNW implies the dense-closure result | R | 03-composition.tex:309-323; intro :56-59. *New problem:* the general reading drawn from it → F1. |
| 3 | [major] Cor. 6.5 depends on the split; re-splitting duality | R | Prop. 3.5(ii). |
| 4 | PSD completion lemma | R | Grone et al. |
| 5 | Dey-Khajavirad Thm 2 | R | 03-composition.tex:277-281. |
| 6 | Kelley / Brierley et al. positioning | R | App. E; 02-setting.tex Separation paragraph. |
| 7 | W initialization; cut depth η | R | App. E. |
| 8 | U_J ignores equality rows | R | Equalities are now two opposite rows throughout. |
| 9 | Intro optimality; m₀ | P | Intro fixed; the abstract lacks m₀ → F6. |
| 10 | coNP reduction wording | R | App. A.3. |
| 11 | vex/cav; hats only for binary64 | R | |
| 12 | Global notation | R | |
| 13 | Hierarchy (Σλ with Sv ∈ D; which example shows which inclusion) | R | Sec. 5.3. |
| 14 | Prop. 6.4 conventions | R | Prop. 3.4 statement. |
| 15 | Star rooted at x₂; parametric QP; Bhathena et al. | R | Remark 4.5; forest paragraph. |

### R3-lit (22 items)

| # | Round-1 issue | Status | Where now / what remains |
|---|---|---|---|
| 1 | [major] Radon partitions (Breen 1973) | R | Sec. 3.3, 3.4. |
| 2 | [major] Tawarmalani 2010 Ex. 3.8, Cor. 3.10 | R | Sec. 3 opening, Sec. 3.5. |
| 3 | [major] Müller et al. 2022 (surrogate duality) | R | 02-setting.tex; Sec. 5.3. |
| 4 | [major] Davarnia et al. 2017; Bao et al. 2009 | R | 02-setting.tex:69-75; intro :23. |
| 5 | Liers et al. misattribution | R | Sec. 5.3. |
| 6 | Schichl-Neumaier over-attribution | R | Sec. 7.1. |
| 7 | SCIP 8 "negative effect" | R | "have not been found to pay off in general". |
| 8 | Folklore hardness; DK treewidth two | R | Sec. 4.1. |
| 9 | Rikun as support | R | Replaced by Anstreicher 2012, Wu et al., Zhu et al. |
| 10 | Anstreicher-Burer dimension and attribution | P | Dimension right; attribution placement → F17. |
| 11 | Intro star claim hedge; Bertelè-Brioschi | R | |
| 12 | Boyd-Vandenberghe locator | R | |
| 13 | RLT, Shor, sparse-SDP references | R | |
| 14 | Moré-Vavasis | R | Subset-sum reduction given. |
| 15 | Dey-Khajavirad published | R | main.bbl: Math. Program. 2026, DOI. I could not check the locators against the journal version. |
| 16 | SCIP source tag | R | v10.0.2. |
| 17 | Bibliography rendering | R | arXiv IDs, Ballerstein DOI. |
| 18 | Current MINLPLib citation | R | Vigerske2026MINLPLib. |
| 19 | Ballerstein via secondary source | P | Fixed in related work. The intro (01-introduction.tex:21-23) still cites Ballerstein directly for "vectors of univariate functions" → F17. |
| 20 | [sugg.] "We show ... do not compose" | R | |
| 21 | [sugg.] CQ wording; αBB | R | |
| 22 | [sugg.] Optional references | P | Margot added. The others were optional; for further standard references see F20. |

### R4-numbers (19 items)

| # | Round-1 issue | Status | Where now / what remains |
|---|---|---|---|
| 1 | [critical] "Never changed which models SCIP solved" (campaign 1 lost genpooling_lee2) | P | The intro (01b-results.tex:8-9) and Sec. 8.7 now say "campaigns 2 to 4", and App. F reports the loss. The abstract (00-abstract.tex:17-18) is still unqualified → F6. |
| 2 | [major] Post hoc result as headline | R | The abstract now reports the prospective result on fresh instances. It does not say that the configuration was selected on earlier instances → F6. |
| 3 | [major] Diagnostic design and disclosure | R | Missing cell run (4C2); fresh seeds (4C3); hand tests and pilot disclosed (08e-path.tex:18-22, 114-115). |
| 4 | [major] Campaign-1 timing sets | R | App. F. |
| 5 | [major] Slowdown statistics | R | "Ratio" column in Table 3; 08c-minlplib.tex. |
| 6 | [major] Conclusions contradict Sec. 9 | R | Rewritten. *New overclaim* at 09-conclusions.tex:30-33 → F2. |
| 7 | [major] No hard structured sample | R | Part D was added. Its informativeness is overstated in the intro → F7. |
| 8 | 8 vs 10 of 180 runs | P | The 3D Part A/B root results are no longer reported, and Table 1 row 3D is inaccurate → F16. |
| 9 | Per-copy root-bound range | R | -0.035 to -0.013. |
| 10 | Small numbers | R | |
| 11 | Setup description | R | 08a-setup.tex. |
| 12 | Diagnostic replay; "independent" | R | 08b-validity.tex:3-5. |
| 13 | Separator statistics; caps | R | Table 4; caps stated. |
| 14 | "Reported in full" omissions | R | App. F. |
| 15 | "Frozen" caption | R | Table 5 labels. |
| 16 | Quantify haverly2pq; isolated cut strength | P | Quantified. There is no isolated LP-strength measurement, but the funnel's "below threshold" share partly substitutes. Acceptable. |
| 17 | "Half a second" understated | R | |
| 18 | Selection description | R | App. G. |
| 19 | [sugg.] Uncertainty, Part A table, A/A time, dense comparator | P | Part A table added (Table 8). No A/A timing variation → F18 (optional). |

### R5-impl (22 items)

| # | Round-1 issue | Status | Where now / what remains |
|---|---|---|---|
| 1 | [major] Trust base | R | Sec. 6.3. |
| 2 | [major] "Independent replay" | R | "a re-execution in a fresh process, not an independent checker". |
| 3 | [major] Diagnostic replay not reported | R | |
| 4 | [major] Conclusions' second reason | R | |
| 5 | Stored-row scope; removable/forcecut | R | Sec. 6.3. |
| 6 | Rejection counts | R | Table 4. |
| 7 | First-direction description, LP cone, filters | R | Sec. 7.2. |
| 8 | Fallback description | R | Sec. 7.2. |
| 9 | Degree ≥ 3 polynomials in 3-4 variables | R | Sec. 7.2. |
| 10 | Campaign-2 code differences | R | App. F. |
| 11 | Star oracle partition; star unused in campaigns 2-3 | R | 04-quadratic.tex:233-243 (but see F4). |
| 12 | Presolve cross-reference | R | 08e-path.tex:87-89. |
| 13 | (√x)² domain | R | |
| 14 | Four outcomes | R | Sec. 6.2. |
| 15 | Forms of the within-tolerance answer | R | App. E, grid fallback. |
| 16 | Fourteen corruptions wording | R | A multiplier corruption is still absent; this was optional. |
| 17 | Limits table | R | Table 6. |
| 18 | "Mode all attempts every block" | R | |
| 19 | [sugg.] VIPR | R | |
| 20 | [sugg.] x log x / x | R | |
| 21 | [sugg.] Witness tolerance | R | |
| 22 | [sugg.] 24.4 of 27.6 s scope | R | |

### R6-writing (26 items)

| # | Round-1 issue | Status | Where now / what remains |
|---|---|---|---|
| 1 | [major] Path-family credit; post hoc | R | Sec. 8.5 (but F2). |
| 2 | [major] "Never changed solved" | P | Abstract unqualified → F6. |
| 3 | [major] Conclusions contradictions | R | Rewritten (but F2). |
| 4 | [major] Sec. 8.2 first directions | R | |
| 5 | [major] F, k redefined in Sec. 7 | R | App. E uses r. |
| 6 | Conclusion restates intro | R | |
| 7 | Global notation | R | |
| 8 | Undefined terms | P | RLT, SOC and DAG are still not expanded → F17. |
| 9 | Sec. 9.6 cross-reference | R | |
| 10 | Per-copy range; 15-20% | R | |
| 11 | "Independent replay" | R | |
| 12 | Tables and figures | P | Table 9 still has no objective sense (pointpack02/04 maximize) → F16. |
| 13 | Overfull boxes | R | main.log has none. |
| 14 | Figure overlaps | **N** | Both are still present (rendered pp. 8 and 21) → F14. |
| 15 | Repetition | P | The negative result appears in the abstract, intro, 8.7 and 9 (F3). |
| 16 | Defensive disclaimers | R | |
| 17 | Abstract length; δ undefined | P | 250 words; δ still undefined → F6. |
| 18 | Campaign count | R | |
| 19 | Local precision errors (a)-(k) | R | All eleven fixed. |
| 20 | Filler phrases | P | "The study has limitations that the reader should weigh." (08g-summary.tex:19) → F17. |
| 21 | Contribution bullets | R | |
| 22 | Campaign-1 description gaps | R | |
| 23 | Front matter | P | Availability statement added. No authors, keywords, MSC codes or declarations → F15. |
| 24 | arXiv URLs; SCIP tag | R | |
| 25 | [sugg.] Structure | P | Screening dropped. The appendix order still does not follow the main text → F19. |
| 26 | [sugg.] "X, not Y" pattern | P | Reduced. "a real safeguard, not a formality" (09-conclusions.tex:17-18) remains → F17. |

### R7-editor (19 items)

| # | Round-1 issue | Status | Where now / what remains |
|---|---|---|---|
| 1 | [major] Path family vs SCIP root weakened by presolve; pair-hull reference; checkvarlocks; second solver | R | Pair-hull row, checkvarlocks row and Gurobi in Table 5. The generalization drawn from them → F9. |
| 2 | [major] Post hoc label | R | Residual in the abstract → F6. |
| 3 | [major] Conclusions | R | New overclaim → F2. |
| 4 | [major] Length and focus | P | Three contributions; classical tools in appendices. Main text is still 31.5 pp, total 56 pp → F3. |
| 5 | [major] SCIP time excluding callback | R | Table 3. |
| 6 | [major] Funnel; presolve losses | R | Table 4; Part B2. The remedy discussion is incomplete → F12. |
| 7 | [major] Baselines | R | |
| 8 | [major] Harder structured instances | P | Part D added; QPLIB not used. The Part D full runs say little → F7. |
| 9 | [major] Star oracle unused | P | Disclosed and benchmarked offline. Still not used in the solver → F4. |
| 10 | [major] Missing prior work | R | |
| 11 | [major] Code and data availability | P | Statement present; no persistent identifier or licence → F15. |
| 12 | Abstract scope and length | P | → F6. |
| 13 | Sec. 8.2 first directions | R | |
| 14 | Sec. 9.6 cross-reference and numbers | R | |
| 15 | Diagnostic replay counts | R | |
| 16 | Part A per-model table | R | Table 8. |
| 17 | Declarations; overfull boxes | P | Overfull boxes fixed; declarations missing → F15. |
| 18 | [sugg.] Binding coupling | R | Part C4 (see F8, F10). |
| 19 | [sugg.] Uncertified ablation | R | Part U (but F5). |

**Summary.** Of the 141 round-1 items, 115 are resolved, 25 partially resolved and 1 not
resolved (R6-14, the figures). The round-1 critical item (R4-1) survives only as a missing
qualifier in the abstract. Four resolved items generated new overclaims in the revised
text: R2-2 → F1; R4-6, R6-3 and R7-3 → F2.

---

## 3. Remaining weaknesses and required changes

Severity scale:
- *critical*: invalidates a result or a headline claim;
- *major*: a referee would require the change;
- *minor*: should be fixed;
- *suggestion*: optional.

### F1 [major] The "representation, not strength" reading is stated in general but holds only for three-variable paths; it is false for four-variable paths

**Location.**
- sections/01-introduction.tex:56-61 (contribution 1, p. 2);
- sections/03-composition.tex:287 and 321-323 (Section 3.4, pp. 9-10);
- sections/09-conclusions.tex:6-13 (Section 9, p. 31).

**Issue.** Section 3.4 correctly proves, via BNW Theorem 1 (n ≤ 3), that on a
three-variable path over a box the dense Shor relaxation with all McCormick inequalities
is exact. Three sentences state the consequence generally:
- 03-composition.tex:287: "The advantage of the joint block over its pairs does not extend
  to dense relaxations."
- Introduction: "the advantage of joint blocks over their pairs is therefore one of
  representation".
- Conclusions: "Second, the advantage of joint quadratic blocks over their pairs is one of
  representation ... dense moment relaxations with products that are absent from the
  model close the same gaps".

BNW themselves show that exactness fails at n = 4, and their counterexample has a
tridiagonal Hessian. It is therefore a four-variable *path*, and four-variable blocks are
exactly the size the separator uses (Table 6). The introduction also says "with the
McCormick inequalities of the missing product". The BNW argument needs the inequalities
of all products, that is, the pair constraints plus those of xz.

**Evidence.**
- BNW Example 4: Q tridiagonal with diagonal (8, 25, 25, 8) and off-diagonals
  (-14, -25, -14), c = (12, 29, 0, 0). I checked the data against the PDF via `pdftotext`.
  BNW report a relaxation value of -0.1220566, also with full RLT (their Table 6).
- `verification/R9_referee_path4.py`, re-run in this round:
  - exact minimum over [0,1]⁴ = 0, at x = 0 (face enumeration in rationals, Theorem 4.1);
  - dense Shor with the McCormick inequalities of all ten products and squares =
    **-0.12206**;
  - Shor with the McCormick inequalities of the path's own products only (the glued pair
    level) = -1.4544.
- So on a four-variable path, the exact support cut of the block, with value 0 in BNW's
  direction, is strictly stronger than the dense first-level relaxation.
- `R9_referee_star_dense.py`: on 60 random three-leaf stars from family (6), the dense
  relaxation was exact on all of them, while glued pairs were weaker on many. For some
  star families the representation reading may therefore hold; for general four-variable
  blocks it does not.

**Fix.**
- Introduction, replace 01-introduction.tex:56-61 ("A dense semidefinite ... already
  has.") with:

  > Adding the McCormick inequalities of the missing product to a dense semidefinite
  > relaxation of the pairs makes it exact on every three-variable path over a box, by a
  > theorem of \citet{BurerNatarajanWillemsen2025}; on such paths the advantage of the
  > joint block over its pairs is one of representation, which support cuts obtain in the
  > coordinates that the model already has. On four-variable paths even the dense
  > relaxation with all McCormick inequalities can leave a gap
  > \citep[Example~4]{BurerNatarajanWillemsen2025}, which an exact support cut of the
  > block closes.

- 03-composition.tex:287: replace "does not extend to dense relaxations" with "does not
  extend to dense relaxations on three-variable paths".
- 03-composition.tex:323: after "not of strength over such relaxations", add:

  > For four variables this is no longer true: on the path of
  > \citet[Example~4]{BurerNatarajanWillemsen2025} the dense relaxation with the McCormick
  > inequalities of all products has value about $-0.122$, whereas the minimum, and hence
  > the support value of the block in that direction, is $0$.

- Conclusions, replace 09-conclusions.tex:6-13 ("Second, ... own coordinates.") with:

  > Second, on three-variable paths the advantage of joint quadratic blocks over their
  > pairs is one of representation: pair hulls glued on finitely many moments of a shared
  > variable give the trivial bound zero exactly when the local zero sets alternate often
  > enough, a dense moment relaxation with the products absent from the model closes these
  > gaps, and support cuts obtain the same strength in the model's own coordinates. On
  > four-variable blocks exact support can be strictly stronger than the dense first-level
  > relaxation.

- *Idea to develop (optional, recommended).* This observation is a positive argument for
  exact four-variable blocks. A small path family built from perturbed copies of BNW
  Example 4 would test the separator where no first-level semidefinite relaxation closes
  the gap. That is a sharper test than the three-variable family, where a dense SDP with
  McCormick inequalities would suffice.

### F2 [major] "Only if ... tries the exact support of each whole row first" is contradicted by Parts C2 and C4

**Location.**
- sections/01b-results.tex:14-17 (introduction, p. 3);
- sections/09-conclusions.tex:30-33 (pp. 31-32).

**Issue.** The introduction says the diagnostic and the control "showed that the separator
closes the gap beyond that level only if it may add enough cuts per block and tries the
exact support of each whole row first". The conclusions say the cuts closed the gap "only
with the exact support of each whole row as a first direction, enough cuts per block, and
...". The paper's own data do not support that whole-row directions are necessary.

**Evidence.** `verification/R9_referee_tables.py`, re-run here, parses Tables 11-12 as
typeset.
- *Part C2* (seeds 0-4, non-binding row), remainder directions with wide limits:
  - median closure 0.86/0.87/0.89/0.90;
  - above the glued pair-hull level on 7 of 20 instances (n10 s0 and s4; n20 s2, s3 and
    s4; n80 s1 and s4);
  - 13 of 20 solved.
  - 08e-path.tex:121-122 itself reports this.
- *Part C4* (binding row), remainder directions with wide limits:
  - median closure 0.98/0.96/0.95/0.93 (range 0.875-0.999);
  - **20 of 20 solved**, the same count as with whole-row directions.
  - 99.9% of its cuts came from LP directions (08e-path.tex:155-157).
- The 2×2 design attributes "most of the closure" to the limits (08e-path.tex:125-127).
- Whole-row directions are needed for the *last* part of the gap only in the non-binding
  family. There the whole-row support of each block equals the optimum by construction
  (08e-path.tex:24-27).

**Fix.**
- Replace 01b-results.tex:14-17 ("A post hoc diagnostic ... whole row first.") with:

  > A post hoc diagnostic, followed by a prospective control, showed that the cut limits
  > account for most of the closure, and that trying the exact support of each whole row
  > first closes the rest of the gap when the coupling row does not bind; with a binding
  > coupling row, both direction orders solved every instance.

- Replace 09-conclusions.tex:30-33 ("They did so only with ... sloped cuts.") with:

  > They needed enough cuts per block. When the coupling row does not bind, the exact
  > support of each whole row closed the last part of the gap, which by construction is
  > the sum of the block minima; when it binds, both direction orders solved every
  > instance, and the cuts that did the work came from the LP direction search.

### F3 [major] The paper is still too long for its new content

**Location.** Whole manuscript: 56 pages; main text pp. 1-32; references pp. 32-40 (112
entries); appendices pp. 40-56.

**Issue.** Round 1 (R7-4) asked for 21-24 pages of main text. The structure is better, but
campaign 4 added material. The main text is 31.5 pages at 11 pt with 1 in margins, which
is about 35 pages in the JOGO template, and the appendices are 16 pages. Some content is
repeated:
- the negative MINLPLib result appears four times (abstract, 01b, 8.7, 9);
- the trusted-base paragraph (Sec. 6.3) restates what replay does.

A referee will ask for cuts.

**Fix.** These cuts save about 6-7 pages of main text; target at most 25 pages in this
format.

| Item | Change |
|---|---|
| (a) Sec. 3.4 | Halve the literature paragraph. |
| (a) Sec. 3.5 | Move Prop. 3.5 and its three examples to App. C, keeping a two-sentence summary in the text. |
| (b) Sec. 5.3 | Move the hierarchy and the two strictness examples to an appendix; keep Prop. 5.5 as one sentence. |
| (c) Sec. 6.2 | Cut to one paragraph; App. D has the details. |
| (c) Sec. 6.3 | Shorten the trusted-base paragraph to three sentences; list the components in the availability statement. |
| (d) Sec. 7.1 | Cut to half a page. |
| (e) Sec. 8.3 | Cut the Part A/B/B2 narrative to half a page. Move Table 4 to App. G with a three-sentence summary in the text. Part D in one paragraph. |
| (f) Sec. 8.6 | Cut to one paragraph. |
| (g) Sec. 8.7 and Sec. 9 | State the MINLPLib result once in full (Sec. 8.3) and briefly elsewhere. |
| (h) App. E | Keep the contract, Thm E.2 and the ε > 0 example; condense the ellipsoid variant to a remark. |
| (i) Tables 8-10 | Move to an online supplement. |
| (j) Bibliography | Prune to about 80 entries. Candidates: the second Garloff-Jansson-Smith entry, Necula, Pnueli et al., Mangasarian, Muñoz-Narkawicz, Kearfott, unless each is needed where cited. |

### F4 [major] The star algorithm, a headline contribution, is not used by the solver; the four-variable block cap, not the data, prevents it

**Location.**
- sections/00-abstract.tex:10-12;
- 01-introduction.tex:63-72;
- 04-quadratic.tex:97-98 ("Section 3 shows that the blocks worth merging are often
  stars", p. 12);
- 04-quadratic.tex:233-243 (p. 14);
- 08f-star.tex (Sec. 8.6, p. 30);
- 08g-summary.tex:20-22 (p. 31);
- 09-conclusions.tex:13 ("For stars, the most common merged blocks");
- Table 6 (A-instances.tex, "sides with 1-4 variables").

**Issue.**
- Theorem 4.4 appears in the abstract and in the contribution list, but no solver run uses
  it:
  - the separator caps blocks at four variables (Table 6);
  - the polytope oracle certified every quadratic cut (04-quadratic.tex:240-241);
  - Part S times an implementation of the sweep that lives in the verification scripts
    (`experiments/v4/star-bench.md`: `sweep_star` from `verification/M3_star_sweep.py`),
    not in the separator.
- Section 8.7 says "larger blocks, where the star algorithm would matter, did not occur
  within the frozen limits". This reads like an empirical finding, but it follows from the
  block cap.
- The motivation sentences ("the blocks worth merging are often stars"; "stars, the most
  common merged blocks") have no support. Section 3 studies a three-variable path, and no
  block statistics are reported.
- Round 1 raised this (R7-9). The paper now discloses it, but the idea is not developed to
  the point of showing that the algorithm matters in a solver.

**Evidence.** Table 6; 04-quadratic.tex:240-241; `star-bench.md`. The three-leaf example of
Sec. 3.5 (Δ = 2/3) and `R9_referee_star_dense.py` show that star directions with a gap
under glued pairs are easy to build. So a star family where merging pays is available.

**Fix.** Choose one option.

(a) *Develop it (preferred).*
- Wire the sweep of Theorem 4.4 into the separator, and lift the four-variable cap for
  blocks that are stars.
- Run a small prospective experiment on a k-leaf analogue of the path family: center y
  shared by leaves Φ_{A_j}(x_j, y), with k ∈ {4, 8, 16}, optionally with center-leaf rows.
- Report root gap closed and solved counts against SCIP, SCIP with its disabled
  separators, and Gurobi.
- This would connect Sec. 3.5, Sec. 4.2 and Sec. 8, and it is the only way the
  contribution can claim practical relevance.

(b) *Present Theorem 4.4 as a theoretical result.*
- Abstract: append "(our experiments, whose blocks have at most four variables, do not use
  it)".
- Replace 08g-summary.tex:20-22 with: "Blocks were capped at four variables (Table 6), so
  the star algorithm of Theorem 4.4 was not exercised in the solver."
- Replace 04-quadratic.tex:97-98 with: "Stars arise when several pairs share one
  variable, as the path of Section 3 does."
- Replace "For stars, the most common merged blocks," (09-conclusions.tex:13) with "For
  stars, blocks in which several pairs share one variable,".

### F5 [major] The certification ablation omits the uncertified alternative a solver developer would use: a numerical global solve, with or without a safety margin

**Location.**
- sections/08b-validity.tex:46-66 and Table 2 (Sec. 8.2, p. 24);
- 01b-results.tex:4-7 (p. 3);
- 09-conclusions.tex:17-21 ("Certification is a real safeguard, not a formality");
- 06-certification.tex:63-64.

**Issue.** Part U compares certified constants with two alternatives. U1 is the minimum over
the separator's sample set; U2 is U1 improved by SLSQP local minimization.
- U1 is biased toward being wrong by construction. The directions were chosen by an LP
  that separates the LP point from the hull of these same samples.
- For blocks of at most four variables, a developer would compute the support constant
  with a numerical global solver (BARON, SCIP or Gurobi on a tiny QP) at default
  tolerances, possibly minus a fixed margin.
- Sec. 6.1 argues that a fixed shift does not replace the calculation, but no experiment
  measures it.
- The conclusion "a real safeguard, not a formality" therefore rests on weak comparators.

The paper's own records contain relevant evidence: numerical global solvers do return
bounds above the exact optimum.
- `evidence/campaign4-digest.md`, "Surprises" 2-3: Gurobi's final dual bound exceeded the
  exact optimum on C2 n10_s2 (status OPTIMAL) and on C3 n10_s7, s8 and s9, by up to
  1.16e-6 absolute (1.95e-4 relative).
- SCIP with checkvarlocks off reported "optimal" values up to 3.8e-4 (relative) below the
  exact optimum.

**Fix.** Either option makes the claim accurate.

- *(a) Add a variant U3 to Table 2:* solve each recorded support problem (5,116 MINLPLib
  and 1,000 path-family directions, each with at most four variables) with SCIP or Gurobi
  at default tolerances, and use its dual bound with and without a shift of
  1e-6·max(1,|value|). Count wrong constants, removed incumbents and removed optima as for
  U1/U2. This is offline and cheap.
- *(b) Qualify.* Replace 09-conclusions.tex:17-18 with:

  > Certification guards against real errors: constants taken from samples or from a local
  > solver were wrong for a large share of the cuts and would have cut off feasible
  > solutions, including known optima.

  Add to Sec. 8.2: "We did not test constants from a numerical global solver; in our runs,
  Gurobi's final dual bounds exceeded the exact optimum by up to 1.2·10⁻⁶ on four
  path-family instances, so such constants would need a margin, whose size a certificate
  makes unnecessary."

### F6 [minor] Abstract: δ undefined, m₀ missing, no campaign qualifier, no disclosure of how the configuration was chosen, "40 fresh instances" overstated, validity conditions incomplete

**Location.** sections/00-abstract.tex:1-21 (p. 1).

**Issue and evidence.**
- (i) "zero or δ²/2" with δ undefined (R6-17).
- (ii) The complexity omits m₀, which Theorem 4.4 and the introduction include (R1-1).
- (iii) "the cuts changed neither which models SCIP solved" is unqualified; campaign 1 lost
  genpooling_lee2 (App. F). The introduction restricts the claim to campaigns 2-4 (R4-1).
- (iv) "a configuration fixed in advance" does not say that it was selected after a post
  hoc diagnostic on earlier instances of the same generator.
- (v) "40 fresh instances" are 20 fresh instances in two variants. The C4 instances
  "differ from the latter only in the right-hand side of the coupling row" (App. G,
  p. 50).
- (vi) Validity is stated as needing only the certified bound and the stored-row check.
  Exact elimination (C2) and safe rounding (C3) are also required.
- (vii) The abstract omits SCIP with its disabled separators (22 solved), which the
  introduction reports.

**Fix.** Replace the abstract with the text below (243 words):

> Global solvers for nonconvex mixed-integer nonlinear programs relax nonlinear expressions
> one at a time and lose their dependence through shared variables; support cuts of the
> convex hull of their joint graph recover it. Exact pair hulls glued on shared moments do
> not compose: for a family of quadratic directions on a three-variable path, the gap to
> the joint hull is zero or $\delta^2/2$, with $\delta$ the distance between two two-point
> sets, depending only on whether they interleave; an interface sharing $\kappa$ moments
> gives the trivial bound exactly when the local zero sets alternate at least $\kappa+1$
> times. For quadratic stars with $k$ leaves, $m$ center--leaf rows and $m_0$ center rows,
> we give an exact rational support algorithm with $O(m_0+(m+k)\log(m+k))$ operations.
> Eliminating the model rows gives cuts in the original variables; a stored cut is valid if
> its constant is certified for the exact binary64 direction, elimination and rounding are
> exact or safely corrected, and the stored row is checked. In SCIP, all 143{,}267 recorded
> cuts (5{,}267 on MINLPLib models) passed replay, whereas constants from samples or local
> solves would have cut off feasible solutions. On MINLPLib models the original-variable
> cuts never changed which models SCIP solved, and SCIP's disabled-by-default separators
> were stronger. On 20 fresh path-structured instances, each with a non-binding and a
> binding coupling row, a configuration selected on earlier instances solved all 40 runs
> within 300\,s, against 19 for SCIP, 22 for SCIP with its disabled separators and 11 for
> Gurobi.

In 01b-results.tex:39-40, replace "On 40 fresh instances, half of them with a binding
coupling row," with "On 20 fresh instances, each run with a non-binding and with a binding
coupling row,".

### F7 [minor] The introduction overstates the informativeness of Part D

**Location.** sections/01b-results.tex:7-11 (p. 3).

**Issue.** "On MINLPLib models, including 20 larger models that SCIP does not solve within
60 seconds, the cuts did not change which models SCIP solved ... and left SCIP's own
solving time unchanged" suggests a substantive test on hard models. The record shows
otherwise:
- In the full runs the frozen separator added cuts to only 2 of the 20 models.
- It stopped during discovery on 12, exactly the models whose discovery took more than the
  1 s allowance in the pre-run scan. This outcome was predictable before the runs
  (08c-minlplib.tex:111-124).
- "SCIP's own time unchanged" rests for Part D on root runs and one commonly solved model
  (blend480).

**Evidence.** 08c-minlplib.tex:111-131; Table 3 (Part D: "only two models were solved, and
times are not comparable"); `evidence/campaign4-digest.md` time table, rows "D full".

**Fix.** Replace 01b-results.tex:7-11 with:

> On MINLPLib models the cuts did not change which models SCIP solved in campaigns 2 to 4
> and left SCIP's own solving time unchanged; the Python separator made the runs slower,
> and SCIP's own disabled-by-default separators improved the root bound more often. On 20
> larger models that SCIP does not solve within 60 seconds, the frozen separator rarely got
> past block discovery within its one-second allowance; with raised limits at the root its
> cuts improved one root bound, by 4\% of the gap, and worsened five.

### F8 [minor] C4: the cut cap was binding in every run; "a larger cap would probably close more" is untested, and "needed about sixteen cuts per block" is the cap, not a measurement

**Location.**
- sections/08e-path.tex:153-154 and 160-162 (p. 30);
- 09-conclusions.tex:42-44 (p. 32).

**Issue.**
- Every cut-mode run stopped at its cap of 16n cuts, which is 16 per block.
- The text speculates that a larger cap "would probably close more", and then concludes
  that the search "needed about 16 cuts per block to come close to the block closure".
- The conclusions repeat "the search needed about sixteen cuts per block".
- No C4 run used a smaller or a larger cap: Table 1 lists only frozen-wide and
  rowdir-wide. The number 16 is therefore the imposed cap, not a measured requirement.

**Evidence.**
- Table 7: wide limits allow 16n cuts.
- `evidence/campaign4-c4-digest.md` item 2: "A larger cut cap might close more of the gap;
  this was not tested."
- Distances to bound (ii) at n = 80 with whole-row directions: 0.0158-0.0287
  (`R9_referee_tables.py`).

**Fix.** Either option.
- *Run the cheap test.* Root-only C4 runs for n ∈ {40, 80} with caps 4n, 32n and 64n, for
  both direction orders: 60 root runs of at most 2 minutes each. Report the distance to
  bound (ii).
- *Or rewrite.* 08e-path.tex:153-162: "Every cut-mode run stopped at its cap of 16n cuts;
  whether a larger cap closes the rest was not tested. The direction search can therefore
  find useful non-row directions; with 16 cuts per block it came within 0.016-0.029 of
  the block closure at n = 80." 09-conclusions.tex:43-44: "on the binding-coupling family
  the search used its full cap of sixteen cuts per block and stopped short of the block
  closure."

### F9 [minor] Comparator claims go beyond the comparator runs: "no SCIP setting" rests on three settings on the campaign-3 instances, and no Gurobi root bound was recorded

**Location.**
- sections/08e-path.tex:93-96 (p. 28);
- 08e-path.tex:166-168 (p. 30);
- 01b-results.tex:13-14;
- 09-conclusions.tex:28-30.

**Issue.**
- *Three SCIP settings only.* "No SCIP setting closed any part of the gap between this
  level and the optimum" and "SCIP reaches the level of glued pair relaxations and no
  further" rest on three settings: default, checkvarlocks off, and disabled separators on.
  Each was run once, on the 20 campaign-3 instances. checkvarlocks off, the strongest
  native relaxation, was not run on the fresh (C3) or binding-row (C4) instances
  (Table 1).
- *No Gurobi root data.* The closing paragraph says exact block support supplies strength
  that "neither SCIP ... nor Gurobi obtains at the root". Gurobi was run only in full mode
  (`campaign4-digest.md`: "20 Gurobi records omitted as designed" from the bound runs),
  and its root bound was not recorded. Gurobi solved every n = 10 instance in
  0.03-0.43 s, so on those instances its root may well be strong.

**Fix.**
- 08e-path.tex:94: replace "no SCIP setting closed" with "none of the three SCIP settings
  that we ran on these instances closed".
- 01b-results.tex:13-14: replace "SCIP reaches the level of glued pair relaxations and no
  further" with "SCIP reached the level of glued pair relaxations and, in the settings we
  tested, no further".
- 08e-path.tex:166-168: replace with: "They show that exact block support supplies
  strength that SCIP, with or without its disabled separators, does not obtain at the
  root, and that Gurobi did not reach within 300 s on the instances with $n\ge20$
  ($n\ge40$ with a binding row); we did not record Gurobi's root bound."
- Optionally run baseline-novarlocks on C3 and C4 (40 root and 40 full runs).

### F10 [minor] The constructed families are easy in a convex perspective reformulation, and their block closure is nearly exact for a known reason; this limitation is not stated, and the reformulation is misnamed

**Location.**
- sections/08e-path.tex:24-38 and 164-171 (Sec. 8.5, pp. 28-30);
- 08g-summary.tex:28-31.

**Issue.**
- *The reformulation is misnamed.* The C4 optimum is computed from "a convex mixed-integer
  quadratic reformulation" (08e-path.tex:32-33). The record shows a *perspective
  mixed-integer SOCP* with one binary per choice of nearest points. Gurobi solves it in
  under a second on 19 of the 20 instances.
- *The families are hard only in their nonconvex formulation.* The experiment therefore
  tests whether a solver recovers the block structure from the nonconvex formulation. The
  paper does not say so.
- *C3 confirms by construction.* With a non-binding row, whole-row cuts give the optimum
  by construction (08e-path.tex:24-27). The C3 fresh result therefore confirms that the
  implementation finds these cuts. It is not an independent test of strength.
- *C4 still favors block cuts.* Bound (ii) equals the optimum on 13 of 20 instances and is
  within 6.5e-4 on the others. This is what the Shapley-Folkman argument predicts for a
  separable objective with a single linking row. The binding-row family therefore also
  favors block cuts strongly.

**Evidence.** `verification/R9_referee_replay_breakdown.py` reads
`experiments/v4/c4-references.json`:
- formulation: "perspective MISOCP (binary per pair (s, t); w^2 <= r b)";
- final-attempt runtime: median 0.187 s, range 0.034-189.4 s; under 1 s on 19 of 20
  instances (n80_s5 took 189 s);
- Gurobi on the nonconvex formulation solved 6 of 20 C4 instances (Table 5).

**Fix.**
- 08e-path.tex:32-33: replace "a convex mixed-integer quadratic reformulation" with "a
  convex perspective reformulation with one binary variable per choice of nearest points
  (a mixed-integer second-order cone program)".
- Add to the closing paragraph of Sec. 8.5:

  > Both families have this convex reformulation, which Gurobi solves in under a second for
  > 19 of the 20 C4 instances; the experiment therefore tests whether a solver recovers
  > the block structure from the nonconvex formulation, not whether the problems are hard.
  > With a single coupling row the block closure is close to the optimum, as the
  > Shapley--Folkman lemma predicts for separable problems with one linking constraint
  > \citep{AubinEkeland1976}, so the binding-row family also favors block cuts.

- Add the same point, in one sentence, to the limitations in Sec. 8.7.

### F11 [minor] The headline replay count is dominated by the constructed family

**Location.**
- sections/00-abstract.tex:15-16;
- 01b-results.tex:2-4;
- 08b-validity.tex:3-5;
- 08g-summary.tex:3-5.

**Issue.** Of the 143,267 replayed cuts, 138,000 (96.3%) are path-family cuts on 60
instances of one generator with dyadic data. Only 5,267 are MINLPLib cuts. The breakdown
is never stated. A referee will read the count as evidence of validity on general models.

**Evidence.** `R9_referee_replay_breakdown.py`: totals from every `replay.json`; all
passed; split by part.

**Fix.** Write "all 143,267 recorded cuts (5,267 on MINLPLib models and 138,000 on the
path family) passed replay" at the first occurrence in the abstract, the introduction and
Sec. 8.2.

### F12 [minor] The proposed remedy for presolve losses would break the certificate chain; say so

**Location.**
- sections/08d-funnel.tex:53-57 (p. 27);
- 09-conclusions.tex:21-25 (p. 31).

**Issue.** The text says a separator "that works in the presolved space ... avoids most of
the presolve losses". SCIP's aggregations and fixings are derived in floating point. They
are not certified implications of the source model. A cut certified in the presolved space
would therefore refer to a model outside the trusted base of Section 6.3, unless the
reductions it uses are themselves certified, as in SCIP's exact mode, which is limited to
MILP. A reader may take this as a free remedy.

**Fix.** After "avoids most of the presolve losses" (08d-funnel.tex:55), add:

> but its certificates would then refer to SCIP's floating-point presolved model, which
> lies outside the trusted base of Section~\ref{sec:replay}, unless the reductions it uses
> are themselves certified

In 09-conclusions.tex:23-24, replace "unless it works in the presolved space or prevents
these reductions" with "unless it prevents these reductions or certifies the presolve
steps it relies on".

### F13 [suggestion] Most stored-row rejections that are not caused by presolve could be avoided by mimicking SCIP's coefficient handling in the exporter

**Location.**
- sections/06-certification.tex:58-62 (Prop. 6.1 discussion);
- Table 4 (08d-funnel.tex);
- 08c-minlplib.tex:96-98.

**Issue.** On the path family every stored-row rejection is a coefficient below 1e-9 that
SCIP dropped (2-3% of violated rows; `campaign4-digest.md` funnel table). In Part B2 the
remaining rejections are integer snapping and dropped coefficients. Proposition 6.1
already allows the removal of tiny coefficients with a bound correction. If the exporter
dropped |c| < 1e-9 and snapped near-integral coefficients itself, with the correction,
the stored row would equal the certified one, and these cuts would be kept.

**Fix.** Implement this and report the recovered rows, or add one sentence in Sec. 8.4
saying that these losses are avoidable in this way.

### F14 [minor] Figures 1 and 2 still have overlapping labels (round-1 R6-14 not resolved)

**Location.**
- figures/chords.tex (Figure 1(a), p. 8);
- figures/pipeline.tex (Figure 2, p. 21).

**Evidence.** I rendered pp. 8 and 21 with `pdftoppm` (temporary directory).
- Figure 1(a): the red label 5/8 sits on top of "(1/2, 5/16)", and both are hard to read.
- Figure 2: the dotted "LP point" arrow runs through the text "exact support".

**Fix.** I compiled and rendered these changes in a scratch directory; neither figure then
has an overlap.
- figures/chords.tex:15: change `node[below right] {$\tfrac58$}` to
  `node[right] {$\tfrac58$}`.
- figures/chords.tex:17: change `\node[anchor=west] at (0.5,0.27)` to
  `\node[anchor=north west] at (0.5,0.30)`.
- figures/pipeline.tex:12: change `below=9mm of src` to `below=14mm of src`.
- figures/pipeline.tex:23: replace the line with
  `\draw[->,dotted] ([xshift=2mm]scip.south west) -- ++(0,-5mm) -| node[pos=0.25,above,font=\small] {LP point} (lp.north);`

### F15 [minor] Front matter, declarations and availability are incomplete; one cross-reference points to the wrong section

**Location.**
- main.tex:18 (empty author);
- no keywords, MSC codes, funding or competing-interest statements;
- sections/99-availability.tex:1-15;
- sections/A-separation.tex:234 (typeset p. 48: "part of the verification scripts
  (Section 9)").

**Issue.**
- JOGO requires keywords and the Springer declarations.
- The availability statement names "the supplementary archive" but gives no persistent
  identifier and no licence. It does not say that rerunning the Gurobi comparisons needs a
  Gurobi licence, or under which terms the MINLPLib files are redistributed.
- `\label{sec:availability}` sits in an unnumbered `\section*`, so `\ref` prints the
  number of the preceding section, 9 (Discussion and conclusions).

**Fix.**
- Add authors and affiliations; keywords (simultaneous convexification; support cuts;
  nonconvex quadratic programming; safe rounding; MINLP); MSC 2020 codes (90C26, 90C20,
  90C11, 65G30); funding and competing-interest statements.
- Give a Zenodo (or similar) DOI and a licence; state the Gurobi and MINLPLib terms.
- A-separation.tex:234: replace "(Section~\ref{sec:availability})" with "(see the
  statement on code and data availability)".

### F16 [minor] Tables: one objective sense missing, several counts not checkable, Table 1 misdescribes Part 3D and Gurobi runs

**Location.**
- Table 9 (B-tables.tex, p. 53);
- Tables 11-12 (pp. 55-56);
- Table 1 (08a-setup.tex:65, 67-69, p. 24);
- Sec. 8.3.

**Issue and evidence.**
- (i) Table 9 has no sense column. pointpack02 and pointpack04 are maximization models,
  and the text calls 1.164 → 1.109 an improvement (R6-12).
- (ii) Tables 11-12 give no full-run status for SCIP with its disabled separators, or for
  checkvarlocks off in Table 11. The counts 10, 10, 9 and 13 in Table 5, and the "22" in
  the introduction, therefore cannot be checked per instance. `R9_referee_tables.py`
  reproduces every other median and count of Table 5 from Tables 11-12.
- (iii) Table 1 row 3D says "as 3A-3C". The Part A and B diagnostic runs were root runs
  only (`experiments/v3d/runs/partA-root-rowdir`, `partB-root-rowdir`). Their results are
  not reported: 469 and 529 cuts; cut counts changed in 10 of 180 runs; no root bound
  changed.
- (iv) Table 1 lists Gurobi in rows whose "Runs" column says "full, root". Gurobi had full
  runs only.

**Fix.**
- Add a sense column to Table 9.
- Add full-run status columns for baseline-extra (and for baseline-novarlocks in Table 11)
  to Tables 11-12.
- Change Table 1 row 3D to "3A, 3B: root; 3C: full and root".
- Add to Sec. 8.3: "In the post hoc root runs of Parts A and B, whole-row directions
  changed the number of cuts in 10 of 180 runs and no root bound."
- Add "Gurobi: full runs only" to the Table 1 caption.

### F17 [minor] Wording and attribution details

**Location and fix.**
- *Unexpanded abbreviations.* RLT, SOC and DAG are never expanded (02-setting.tex:100;
  04-quadratic.tex:203; figures/pipeline.tex:10). Expand at first use:
  "reformulation-linearization technique (RLT)", "second-order cone (SOC)", "expression
  DAG (directed acyclic graph)".
- *Citation placement.* 02-setting.tex:100-104 attributes the simplex and 2-D box hull
  results to Shor and Sherali-Adams. Replace with: "Semidefinite and RLT constraints
  \citep{Shor1987,SheraliAdams1990} describe the convex hull of $\{(x,xx\T)\}$ over a
  simplex of dimension at most three and over a box in dimension two, and polytopes of
  dimension at most three admit an extended formulation built from a triangulation
  \citep{AnstreicherBurer2010}; ...".
- *Secondary source in the introduction.* 01-introduction.tex:21-23: "vectors of
  univariate functions" rests on Ballerstein, whom the related-work section cites only
  through Liers et al. Cite \citet[Proposition~1]{LiersEtAl2021} here as well, or drop
  "of univariate functions".
- *Overstated model import.* 01-introduction.tex:83-85: "whose model import preserves the
  exact binary64 semantics and the domains of the source model" is stronger than the
  boundary stated in Sec. 7.1. Replace with "whose model import checks, without
  tolerance, that the expression objects passed to SCIP equal the binary64 source
  expressions and proves their domain requirements".
- *Overstated "answer".* 01-introduction.tex:43: "We answer these questions" claims too
  much for question (1), where Prop. 3.5 "does not say which directions to merge", and for
  (4). Write "We address these questions".
- *Filler.* 08g-summary.tex:19: delete "The study has limitations that the reader should
  weigh." and start with "The MINLPLib parts use ...".
- *Contrast pattern.* 09-conclusions.tex:17-18: drop the "X, not Y" pattern (see F5(b) for
  the replacement sentence).

### F18 [suggestion] Give the run-to-run time variation next to the timing claims

**Location.** sections/08c-minlplib.tex:74-80; Table 3.

**Issue.** "15-20% slower" and "SCIP's own time unchanged (within 4%)" appear without the
variation between identical baseline runs. Round 1 (R4-19) measured it for Part A, seed 1
against seed 0:
- median ratio 1.03, range 0.61-1.92 per run;
- SGM 0.822 against 0.852.

**Fix.** Add one sentence with this A/A ratio, or a bootstrap interval for the per-run
ratios.

### F19 [suggestion] Appendix order does not follow the main text

**Location.** main.tex:40-42.

**Issue.** Appendix C (details for Section 3) comes after Appendices A and B (details for
Section 4).

**Fix.** Order the appendices as: Section 3 details, polytope, star, bounds, separation,
campaigns, tables.

### F20 [suggestion] Standard references that the literature lanes list as must-cite are still absent

**Location.** references.bib; 02-setting.tex:54-116.

**Issue.** Lane L1's must-cite list includes several items not in `references.bib`:
- Tawarmalani-Sahinidis 2002 (book);
- Tawarmalani-Richard-Xiong 2013 (explicit envelopes through polyhedral subdivisions);
- Crama 1993;
- Khajavirad-Sahinidis 2012/2013;
- He-Liu-Tawarmalani 2023;
- Misener-Smadbeck-Floudas 2015.

Lane L4 asks for Yildiran 2009 or Modaresi-Vielma 2017 next to the aggregation results.

**Fix.**
- Add Tawarmalani-Sahinidis 2002 to the factorable-relaxation citations.
- Add Tawarmalani-Richard-Xiong 2013 to "Exact low-dimensional and structured quadratic
  hulls".
- Add Yildiran or Modaresi-Vielma next to Blekherman-Dey-Sun.
- Add Aubin-Ekeland 1976 if the Shapley-Folkman remark of F10 is adopted.
- Check the rest with this round's literature lens.

---

## 4. Honesty about limitations, post hoc versus prospective, contributions versus evidence

**Post hoc versus prospective.** The distinction is clear in the body.
- It is defined once (08a-setup.tex:6-9).
- It is labeled in Table 1 (3D), in Table 5 ("post hoc" rows), and in Sections 8.5 and 8.7.
- The introduction labels the diagnostic as post hoc.
- The two pre-diagnostic steps are disclosed (08e-path.tex:18-22, 114-115): the hand tests
  on 2 of the 20 evaluation instances, and the native pilot that preceded the randomized
  family.
- `experiments/campaign-v4-protocol.md` was fixed before any campaign-4 run (file time
  12:34; first C3 build 13:26), including Amendment 1 for C4 and Part U.

Two gaps remain, both in the summaries:
- The abstract says "fixed in advance" without saying that the configuration was selected
  on earlier instances of the same generator, and it counts the C4 variants as separate
  "fresh" instances (F6).
- The introduction and the conclusions turn the 2×2 attribution into an "only if" (F2).

**Limitations.** Section 8.7 states most of them:
- Python cost;
- shared host;
- one seed;
- one thread;
- Gurobi with default settings;
- constructed families that favor block cuts;
- blocks of at most four variables;
- no recommendation of default use.

Missing or misstated:
- the convex perspective reformulation that makes the families easy (F10);
- the block cap, not the data, kept the star algorithm out of the solver (F4);
- the cut cap bound every path-family run (F8);
- certification was compared only with sampling and local optimization (F5);
- the replay total is 96% constructed-family cuts (F11);
- the presolved-space remedy is not free of certification cost (F12).

**Claims versus evidence.**

*Supported:*
- validity of every recorded cut, within the stated trusted base;
- harm from uncertified constants obtained by sampling and local optimization;
- neutrality on MINLPLib in campaigns 2-4;
- SCIP's disabled separators are stronger on MINLPLib root bounds;
- every count and median of the path-family results that can be recomputed from
  Tables 11-12.

*Overstated:*
- the general "representation" reading (F1);
- the necessity of whole-row first directions (F2);
- the informativeness of Part D in the introduction (F7);
- "sixteen cuts per block were needed" (F8);
- "no SCIP setting" and "nor Gurobi at the root" (F9);
- "stars are the most common merged blocks" (F4);
- "certification is a real safeguard, not a formality", against untested stronger
  alternatives (F5);
- the unqualified sentences in the abstract (F6).

*Novelty:* the claims are qualified with "to our knowledge" where needed, and none goes
beyond the evidence in `evidence/literature-L*.md` and the round-1 audit.

---

## 5. Checks run (targeted, local)

No project-wide tests were run, CI was not consulted, and no SCIP or Gurobi solve was
started. All scripts ran with `/workspace/minlp-notes/code/minlp_solver_lab/.venv/bin/python`
and `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`.

**Scripts.**
- `verification/R9_referee_path4.py`, re-run on BNW Example 4 (data checked against the
  BNW PDF): exact minimum 0; dense Shor with all McCormick inequalities -0.12206;
  path-only -1.4544 (F1). SDPs solved with Clarabel via CVXPY.
- `verification/R9_referee_star_dense.py`, re-run on 60 random three-leaf stars from
  family (6): the dense relaxation with all RLT inequalities was exact on all of them (F1,
  F4).
- `verification/R9_referee_tables.py`, re-run: it parses Tables 11-12 and reproduces every
  Table 5 median and solved count, "above the pair-hull level on 7 of 20",
  "opt − (ii) = 0 on 13 of 20 (max 6.473e-4)", the distances 0.016-0.029 at n = 80, the
  minimum whole-row closure 0.9739 ("at least 97%"), and the abstract counts 19 and 11.
  The "22" and the SCIP-extra counts cannot be checked from the tables (F16). The
  glued-pair entry for seeds 0-4 at n = 40 rounds to 0.93 from the 4-digit table values
  against 0.935 in the raw digest; this is immaterial.
- `verification/R9_referee_replay_breakdown.py` (new this round): replay totals
  143,267, all passed; path family 138,000 (96.3%), MINLPLib 5,267 (F11). C4 reference:
  perspective MISOCP solved in a median of 0.187 s, under 1 s on 19 of 20 (F10).

**Other checks.**
- `pdfinfo` (56 pages).
- `cmp` of `main.pdf` and of every `sections/*.tex` against `development/draft-round2/`:
  identical.
- `main.log`: no overfull boxes, no undefined references.
- Abstract length: 250 words.
- `pdftoppm` renderings of pp. 8 and 21 in a `mktemp` directory (F14).
- Scratch compile (pdflatex, `mktemp` directory) of `figures/chords.tex` and
  `figures/pipeline.tex` with the F14 changes; rendered without overlaps.

**Files read.**
- `evidence/review-round1.md` (all seven lenses, every item);
- `campaign4-digest.md` and `campaign4-c4-digest.md`;
- `coverage.md`, `issues-raised.md` (open items), and the must-cite lists of `literature-L1.md`
  and `literature-L4.md`;
- `experiments/campaign-v4-protocol.md`, `experiments/v4/star-bench.md` and
  `experiments/v4/c4-references.json`;
- the BNW and Anstreicher-Burer full texts in `literature/papers/`.
