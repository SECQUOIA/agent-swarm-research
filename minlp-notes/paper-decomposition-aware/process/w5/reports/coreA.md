# W5 report: group coreA

Files: `sections/setting.tex`, `sections/setting-growthcert.tex`,
`sections/grids.tex`. CUTPLAN assigns coreA only its minor findings, with no
moves or cuts. I applied the verifier's `corrected_fix` where one exists
(C-writing-3). The other six findings have no `verifier` field, so I used the
reviewers' fixes.

## 1. Adjudication

| id | decision | reason | change |
|---|---|---|---|
| C-writing-3 | ACCEPTED (verifier's corrected fix; my part) | The remark credited growth with a restriction that minimality already implies. Lemma `lem:growthcert`(b) gives H_{J0J0} ⪰ 0 at every minimizer. | `setting-growthcert.tex`, Remark `rem:nonconvex` (label kept), retitled "What growth restricts". Lines 60-66 were replaced by the verifier's text: minimality alone; point growth equivalent to uniqueness (Lemma `lem:unique-growth`); H_{J0J0} ⪰ 2gI, so κ ≥ 2L/λ_min if J0 ≠ ∅; the weighted bound; the global inequalities κ ≥ L‖x'-x*‖²/(F(x')-OPT) and κ̄ ≥ ‖x'-x*‖²_L/(F(x')-OPT); Example `ex:family`. I added one gloss sentence: "Since ‖d‖²_L ≤ L‖d‖², nearly optimal points far from x* in the norm ‖·‖_L make both condition numbers large." It is stated in the L-norm, so it stays true when L=0, which addresses the verifier's warning. The part (a) sentences are kept. `setting.tex` line 133: the pointer now says the remark "states what growth restricts for box QPs". |
| R-referee-3 | ACCEPTED (same change) | Same defect as C-writing-3. | Covered by the C-writing-3 text. The referee's "excludes nearly optimal points far from the minimizer" is now the pair of global inequalities and the gloss. |
| C-writing-8 | ACCEPTED, slightly generalized | Validity of filtering runs had been proved only in running text, and Thm 5.7(a) relied on it. | `grids.tex` 269-292: new Corollary `cor:filtercert` ("Filtering runs give valid certificates") with a full proof. It replaces the old paragraph at lines 274-282. Two differences from the reviewer's version: (i) the hypothesis is U_j ≥ OPT ("for example the value of a feasible point"), because the proof uses only that; (ii) the conclusion also states that every threshold meets the condition of Def `def:filter` and that every minimizer lies in every X^(j), which Section 5 uses. The proof is an induction via Prop `prop:cellwise`(b) and Prop `prop:filter`. It checks every requirement of Def `def:cert`, including i ∈ P for (C1). The rest of the paragraph is kept as discussion after the corollary ("So a filtering run is certified by ..."). coreB has already replaced the citations in growth.tex 62 and 222 and in appendix-growth.tex 152. |
| C-writing-10 | ACCEPTED (my part: (a), Table 2) | Table 2 claimed "one meaning throughout", but listed J twice. | `setting.tex` 152-154: the lead sentence now reads "lists the symbols used in several sections and the second meanings of a few of them; symbols local to one proof, example or algorithm are defined where they are used." The stage-limit row is replaced: coreB renamed the Section 5 stage limit to `j_max`, which is now in the row "h_j, j_max: common mesh, stage limit of TRIAL and CT". The J row now lists the meaning that remains: "also the last level of CORE, TU-GRID and UC (§§7-9)". Parts (b) (x°, exact) and (c) (f(p,t): coreB, front, limits) are not in my files. |
| C-literature-3 | ACCEPTED as proposed | Hasan (2018) introduced the edge-concave underestimator; Bajaj and Hasan (2020) evaluate it at the vertices. | `grids.tex` 46-49: "...vertex bound of Bajaj and Hasan \cite{BajajHasan2020}, who evaluate at the vertices the edge-concave underestimator of Hasan \cite{Hasan2018}, built from an upper bound on the diagonal Hessian entries; we use one bound L_i per coordinate." The `Hasan2018` key exists. |
| R-referee-6 | ACCEPTED (my part) | Under the convention at setting.tex 98-103, κ̄ came from *some* valid constant, so "the parameter κ̄" was not a function of the instance. | `setting.tex` 103-112, after the convention: if a condition holds, its largest valid constant is the infimum of (F(x)-OPT) divided by ‖x-x*‖², ‖x-x*‖²_L or dist(x,S)², taken over the points where that denominator is positive; every positive constant is valid if there are none. For weighted growth this does not depend on x*, because (eq:wgrowth) forces x'_P = x*_P for every minimizer x'. So each condition number has a smallest value, determined by the instance and the curvature bounds. As a parameter, κ̄ denotes max{1,1/γ*} (κ̄=1 if P=∅). "Curvature bounds" is included because κ̄ scales with the L_i in use. |
| R-referee-4 | ACCEPTED (my part) | The overloads are mostly in other groups' files. My parts are Table 2 and one local index. | Table 2 now reflects the renames that other groups reported. Row "θ, h_ij, η_j, r_i": mesh η_j r_i, scale 2^{E-j}, r_i = 2^{-ϖ_i}. coreB renamed the exponent e_i to ϖ_i. New row "h_j, j_max". Row Δ,R,Ω,τ adds "(radius R in §5)", because coreB kept R, R_0, R_j, R_ij as radii in §5 and App. A. New row "r: number of private blocks (§7); bound on all \|S_i\| (§§8-10)", as requested by optsets, tu and recA (C-consistency-4). The row "L̄, κ_c, η" adds the TU mesh unit η without a new line, as tu requested. `grids.tex` 168, proof of Lemma `lem:dp`: the tree-node index r is renamed t'. The unit vector e_i in Def `def:curvature` and Lemma `lem:growthcert` is kept, as standard notation. |

## 2. Cut-plan items

None are assigned to coreA. The findings add text: a corollary with proof, the
largest-constant paragraph, a longer remark, and two table rows. To offset
part of it I compressed text in my files without removing any statement:
- I tightened the "Families of intervals", "Randomized rounding" and
  "Enumerating the cells" paragraphs and the paragraph after
  Cor. `cor:filtercert`.
- The branch-and-bound / OBBT / checkable-certificate comparison at the end
  of Section 4 was a duplicate of related.tex 78-95. It is shortened to one
  clause with a pointer to Section 2.
- I merged two sentences of the point/weighted-growth paragraph. "Weighted
  growth makes x*_P unique" is now said once, in the R-referee-6 paragraph.

Page measurements, all from `latexmk` builds:
- **Before** (`/tmp/w5-coreA-before`, the pre-W5 snapshot): Section 3 starts
  on p. 10 at y=121pt. Section 4 starts on p. 13 at y=497pt. Section 5 starts
  on p. 17 at y=533pt. 123 pages.
- **After, isolated** (`/tmp/w5-coreA-iso`, the snapshot with only my three
  files replaced): Section 3 starts on p. 10, Section 4 on p. 13 at y=645pt,
  and Section 5 at the top of p. 18. Page 17 has about 42pt free at the
  bottom. 124 pages.
- **Net change:** Section 3 grew by about 148pt, roughly 11 lines: +7 lines
  for R-referee-6, +4 for the remark, +2 table rows, -2 from merging.
  Section 4 is roughly unchanged: the corollary's ~13 lines against ~11 lines
  of removed and compressed text. The total is about +0.25 page of content.
  Because Section 5 no longer fits on p. 17, the isolated build is one page
  longer.
- **Current full tree** (`/tmp/w5-coreA`, with other groups' concurrent
  edits): my sections span pp. 9-17. Section 3 starts on p. 9, Table 2 is on
  p. 12, Section 4 starts on p. 13, Cor. 4.8 is on p. 16, and Section 5
  starts on p. 17. 126 pages at the time of the build.

## 3. Labels

- New: `cor:filtercert` (Corollary 4.8, grids.tex). It is already cited by
  coreB in growth.tex (2x) and appendix-growth.tex.
- None moved, renamed or deleted. Remark `rem:nonconvex` keeps its label,
  with the new title "What growth restricts".

## 4. Requests for other files

1. **coreB (growth.tex, Remark `rem:fpt`):** the existence argument for the
   smallest κ̄ ("It exists: since weighted growth determines x*_P ... or 1.")
   now duplicates setting.tex 103-112. Suggested replacement: "As the
   parameter we take the smallest weighted condition number of the instance,
   which exists (Section~\ref{sec:setting}, after
   Definition~\ref{def:growth})." Both texts are correct and consistent, so
   this is optional and only saves 2-3 lines.
2. **front (intro.tex "Parameterized form"):** optional. To name the
   parameter precisely, cite "the smallest weighted condition number of the
   instance (Section~\ref{sec:setting})" or Remark `rem:fpt`. The current
   intro scope paragraph (intro.tex 180-192) matches Remark `rem:nonconvex`.
3. **coordinator:**
   - CONVENTIONS §5: replace the "Growth scope" bullet with the verifier's
     text (C-writing-3 corrected_fix, last paragraph).
   - CONVENTIONS §4: record `j_max` (stage limit of TRIAL/CT), `\varpi_i`
     (curvature exponent), J as the last level of CORE/TU-GRID/UC, and the r
     entry.
   - The full-tree build reports an undefined citation `AbelloEtAl2001`
     (limits, p. 60). The bib key is presumably still to be added.
4. **tu / recB / optsets (optional):** if the last level J of TU-GRID, CORE
   and UC is renamed to `j_max` for uniformity, delete the row "J & also the
   last level of CORE, TU-GRID and UC" in Table `tab:notation` (setting.tex
   182), or ask the coordinator to do it.

## 5. Checks run (local, targeted; CI not consulted)

- `latexmk -pdf -interaction=nonstopmode main.tex` in three private copies:
  - `/tmp/w5-coreA-before` (snapshot): no errors or warnings.
  - `/tmp/w5-coreA-iso` (snapshot plus my three files): no errors, no
    undefined references, no overfull boxes. An intermediate version of
    Table 2 was 0.8-3pt too wide; I shortened two rows.
  - `/tmp/w5-coreA` (current full tree): no LaTeX errors. The only undefined
    item is the citation `AbelloEtAl2001` (not mine). No overfull boxes.
  - An earlier full-tree build showed errors in appendix-growth.tex while
    coreB was mid-edit; they are gone in the final build.
- `python3 process/w5/checks/coreA-scope.py`: PASS. In exact arithmetic on
  one block of Example `ex:family`, it checks:
  - point growth with g=1/2 on a 13³ rational grid;
  - κ ≥ 2L/λ_min(H_{J0J0});
  - κ ≥ L‖x'-x*‖²/(F(x')-OPT) and κ̄ ≥ ‖x'-x*‖²_L/(F(x')-OPT) at the local
    minimizer (0,0,0);
  - ‖d‖²_L ≤ L‖d‖²;
  - the verifier's L=0 example, where κ=1 although the near-tied minima are
    far apart.
- By hand: the proof of Cor `cor:filtercert`, and the closedness argument
  for the largest valid growth constants (the infimum is itself valid; for
  weighted growth all minimizers share x_P).

## 6. Unresolved

- Table 2 still lists J with a second meaning (the last level in §§7-9),
  because those files keep J.
- Not added to Table 2, because these symbols are local: the unit vector
  e_i versus the Section 7 allowance e, e_B(C), e_j (always with a bag or
  level subscript); ω (proximal weight, §9.3); x° (a minimizer, §6); J_f
  (free set, §6).
- My sections are about 0.25 page longer than before W5. The assigned
  findings require the additions. I offset what was possible without
  removing content.

## Verification (W5 verifier for coreA)

Scope: I diffed `sections/setting.tex`, `sections/setting-growthcert.tex` and
`sections/grids.tex` against `process/w5/sections-before-w5/`. Then I
re-derived every changed statement and proof, checked Table 2 against the
current notation in the other groups' files, and rebuilt the paper. The task
names `process/w5/assign/coreA-verify.json`, which does not exist. The
assigned findings are those in `process/w5/assign/coreA.json` (7 findings),
and all of them are covered below.

### Findings

| id | verdict on the revision | notes |
|---|---|---|
| C-writing-3 | correct | The remark follows the verifier's corrected fix, and I re-derived each claim. Minimality gives H_{J0J0} ⪰ 0. Point growth ⇔ uniqueness: Def. `def:growth`(a) gives one direction and Lemma `lem:unique-growth` (exact.tex 300) the other. H_{J0J0} ⪰ 2gI gives λ_min ≥ 2g > 0, so κ ≥ L/g ≥ 2L/λ_min. (3.2) gives g ≤ (F(x')-OPT)/‖x'-x*‖², hence κ ≥ L‖x'-x*‖²/(F(x')-OPT); (3.3) gives the κ̄ bound in the same way. The added gloss is stated in the L-seminorm, so it does not make the false claim the verifier warned about when L=0. Example `ex:family` states κ ≤ 21/4 and indefinite block Hessians. **Changed:** "indefinite Hessian blocks" → "an indefinite Hessian". The remark has just shown that the block H_{J0J0} is positive definite, so "Hessian blocks" could be read as that block. The full Hessian of `ex:family` is indefinite, because its block principal submatrices are. |
| R-referee-3 | correct | Same text as C-writing-3. |
| C-writing-8 | correct | Re-derived Cor. `cor:filtercert`. By induction, every minimizer lies in X^(j). Prop. `prop:cellwise`(b) then gives β_j ≤ min_{X^(j)}F = OPT ≤ U_j, so the condition U ≥ β of Def. `def:filter` holds. Prop. `prop:filter` keeps every x with F(x) ≤ U_j. X'' ⊆ X' holds by construction, integer nodes come from "grid for a subbox", and (C2) holds with equality. For (C1): i ∉ P keeps X'_i, so every interval not contained in the next hull has i ∈ P and was not retained, which gives min m > U_j ≥ OPT ≥ β_k. Relaxing the hypothesis to U_j ≥ OPT is sound. The citations in growth.tex 62 and 223 and in appendix-growth.tex 152 match the statement: the TRIAL grids are grids for the filtered subbox, with G_i = {ℓ_i, u_i} for i ∉ P, and the thresholds are values of feasible points. Dropping stages that remove nothing still leaves a certificate of the corollary's form. **Changed:** the statement used X^(j) without naming it; it now says "a grid for X^(0)=X" and "a grid for the subbox X^(j+1) obtained from G^(j)". This is consistent with Def. `def:cert`, because a grid for a subbox spans it. |
| C-writing-10 (my part) | correct | The Table 2 lead sentence no longer claims "one meaning throughout". I checked every row against the current files. j_max appears in growth.tex 42 and 188 and in appendix-growth. ϖ_i and r_i = 2^{-ϖ_i} with η_j = 2^{E-j} appear in growth.tex 35-38. R is a radius in growth-sharp.tex 45. J is the last level in recourse-cuts 175, constraints 251/293 and optsets 75. r appears in recourse-valuefn 59, constraints 387, optsets 136 and limits 465. η is the TU mesh unit at constraints 39. The renames x° and J_f are in exact.tex 64 and exact-localized 91, and ω is in appendix-proximal 255. |
| C-literature-3 | correct | The wording follows the reviewer's fix. Both keys exist in references.bib (Hasan2018 is JOGO 71(4):735-752). |
| R-referee-6 | correct | Re-derived. If growth holds with some constant, every ratio is at least that constant, so the infimum is positive and is itself valid, and it is therefore the largest valid constant. With no positive denominator, every constant is valid and the smallest condition number is 1. (3.3) at a minimizer x' gives ‖x'-x*‖_L = 0, so ‖·-x'‖_L = ‖·-x*‖_L and γ* does not depend on x*. P = ∅ gives κ̄ = 1. Remark `rem:fpt` (growth.tex) and intro.tex 105-107 already refer to this paragraph. **Changed:** added "respectively" so that each of the three ratios is matched to its growth condition. |
| R-referee-4 (my part) | correct | The rows match current usage (see C-writing-10). Lemma `lem:dp`: the index r → t' is consistent, and t' is not used elsewhere in the proof. |

### Other edits by the agent

I checked these against the snapshot. No statement or needed hypothesis was
lost, with one exception, noted in item 2.

1. "Enumerating the cells": correct, because Q has the scopes of F (line 35).
   **Changed:** word order ("instead computes β and all min-marginals by
   dynamic programming").
2. "Randomized rounding": correct. Var(Y_i) = (x_i-a)(a'-x_i) ≤ w²/4, and
   d_i(Y_i) ≥ L_i w(J_i)²/8 because J_i has endpoint Y_i. With w(J_i)=0, an
   integer x_i is an endpoint, so Y_i = x_i. **Changed:** the compression had
   dropped the domain of x; the paragraph now says "for x∈X'".
3. "Families of intervals": correct. The proof of Prop. `prop:cellwise` uses
   exactly the two stated properties, together with the replaced domain.
4. The shortened B&B/OBBT sentence at the end of Section 4: the full
   comparison is in related.tex 79-95, so nothing is lost.
5. Point/weighted paragraph: "x*_P unique" is now said once, in the
   R-referee-6 paragraph ("forces x'_P = x*_P"). "κ̄ can be taken at most κ"
   is still proved.

### Cut plan, labels

- CUTPLAN assigns coreA no moves or cuts.
- Labels: every label of the snapshot is present in the three files. One
  label is new (`cor:filtercert`), and none is duplicated across
  `sections/*.tex`.

### Checks run (local, targeted; CI not consulted)

- **`python3 process/w5/checks/coreA-verify-filtercert.py` (new): PASS.** It
  runs 60 random mixed box QPs (two continuous coordinates and one integer
  coordinate) with three filtering stages each, in exact rational
  arithmetic. The thresholds U_j are values of feasible points, sometimes
  increased. It checks:
  - U_j ≥ β_j;
  - nested subboxes, with integer nodes in integer coordinates;
  - (C1) against β_k;
  - F ≥ β_k at 2205 feasible sample points;
  - every sampled point with F ≤ min_j U_j lies in X^(k).
- **`python3 process/w5/checks/coreA-scope.py` (the agent's): PASS** (rerun).
- **Build:** `latexmk -pdf -interaction=nonstopmode main.tex` in
  `/tmp/w5-coreA-verify` (full current tree, after my edits):
  - no LaTeX errors, no overfull boxes, no undefined or multiply defined
    references;
  - 12 undefined citations, all from related.tex (front: DelPiaWeismantel2014,
    AriHildebrand2026, EiflerGleixner2023, PeyrlParrilo2008, KaltofenEtAl2008,
    Meyer1977, DavarniaVanHoeve2021, DavarniaKiaghadiQiu2026, Ye1992,
    MehrotraYe1993, BachocCesariGerchinovitz2021) and limits.tex
    (AbelloEtAl2001); none is cited in my files.
- I read the rendered PDF text of Remark 3.4, Table 2 and Corollary 4.8.
- **Page span** (from main.aux, 126 pp.):
  - Section 3 starts on p. 9, Remark 3.4 is on p. 12, Section 4 starts on
    p. 12, and Table 2 is on p. 13;
  - Cor. 4.8 is on p. 17, and Section 5 starts on p. 17;
  - my sections therefore span pp. 9-17;
  - my verifier edits do not change the line count measurably.

### Requests for other files

- **front (optional):** intro.tex 186-187 says "indefinite Hessian blocks"
  right after defining the block H_{J0J0}. For the same reason as in the
  remark, write "an indefinite Hessian".
- **coordinator:** CONVENTIONS §5 "Growth scope" still prescribes the old
  wording. Replace it with the verifier's text, as the agent requested.
- **coordinator:** add bib entries for the 12 undefined citations listed
  above.

### Unresolved

- None in coreA's files.
- These remain as documented by the agent:
  - Table 2 lists J a second time, as the last level in §§7-9, because
    those files keep J;
  - my sections are about 0.25 page longer than before W5, a cost of the
    required additions.
