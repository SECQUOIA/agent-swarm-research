# W5 report: recA

Files edited (only these): `sections/recourse.tex`, `sections/recourse-valuefn.tex`,
`sections/recourse-local.tex`, `sections/recourse-convex.tex`,
`sections/appendix-recourse-convex.tex`.

No mathematical statement was weakened. The changes are two moves to
Appendix C (CUTPLAN recA), one precision fix to Theorem `thm:cv`(iv), one
added sentence on termination in Theorem `thm:cv`(iii), and wording fixes.
All 41 labels of the five files are still defined (label sets before and
after are identical); no label was deleted.

## CUTPLAN recA items

1. **Section 7.2 (done).** Kept the bag-cell definitions, `V_B`, `e_B(C)`,
   Lemma `lem:cr-cell` and Theorem `thm:cr-filter` (Section 7.4 uses both).
   Moved recourse-local.tex 67-147 of the snapshot (multilevel paragraph,
   gap/oscillation paragraph, "Grid min-marginals are not certified recourse"
   paragraph and setup, Proposition `prop:star`, its discussion) to
   Appendix C.2, placed after the proof of `thm:cr-filter` (multilevel
   paragraph), before `prop:cr-osc` (oscillation paragraph, shortened since
   the proposition now follows directly), and before the proof of
   `prop:star` (setup, statement, discussion, pointer to
   `ex:cr-star32`). The main text keeps a two-sentence summary: the
   appendix applies the theorem level by level and needs only small error
   oscillation for filtering (`prop:cr-osc`); with grid min-marginals a
   constant correction charged to one bag keeps a cell containing the bag
   projection of the minimizer only if the constant grows with the number
   of outside coordinates, already for bag size two and kappa < 11
   (`prop:star` in Appendix `app:recourse-convex`). The CORE proof
   (recourse-cuts.tex, Theorem `thm:cr-search`(d)) does its own multilevel
   argument and does not depend on the moved paragraph.
2. **Section 7.3, recognition (done).** Moved the paragraph "Recognizing a
   globally affine response", Theorem `thm:cv-recog` and the two sentences
   after it to Appendix C.4, now titled "Recognition of affine selectors"
   (statement, then the proof as a `proof` environment, then the two
   examples and the scope sentences). Main-text summary, appended to the
   paragraph that lists the appendix results: "For a block whose domain is
   a box, one exact convex quadratic program and one linear program decide
   whether some affine map is an optimal response on the whole scope box,
   and if so return it with a one-leaf certificate (Theorem `thm:cv-recog`
   in Appendix `app:recourse-convex`)." The qualifier "whose domain is a
   box" is required by the theorem (Y = [l^Y,u^Y]); the plan's sentence
   omitted it.
3. **Section 7.3, after Proposition `prop:cv-limit` (done).** Kept the
   definitions (admissible K, L_K, g_K) and the statement (cited by
   intro.tex and conclusion.tex). Kept "The proof is in Appendix ...",
   "Disjoint copies give ..." and "The instance is trivial to solve; ...";
   moved "The obstruction is a clipped piece ... (Section
   `sec:conclusion`, question 1)" to the end of Appendix C.7 (after the
   proof, "In the proof above ..."). The main text says the appendix
   locates the obstruction in a clipped piece.
4. **Roadmap in recourse.tex (updated).** Section 7.2 is no longer called a
   side result with `prop:star` in it; the roadmap now says that 7.2 shows
   validity with exact or certified recourse and points to `prop:star` in
   Appendix `app:recourse-convex`; Remark `rem:cr-mixed` is mentioned in its
   own sentence.

### Page savings (measured)

Measured in an isolated build: the pre-W5 snapshot with only my five files
replaced (`/tmp/w5-recA-iso`), against the snapshot build
(`/tmp/w5-recA-base`). Positions are in pages, from the PDF word boxes,
normalized to the text block.

| Part | Before | After | Change |
|---|---|---|---|
| 7.2 | 2.02 pp | 1.08 pp | -0.94 |
| 7.3 | 4.43 pp | 4.19 pp | -0.24 (includes about +0.1 for the M-recourse-1/4 text) |
| Section 7 (all of it) | 13.62 pp | 12.57 pp | -1.05 |
| Main text (start of Section 12) | p. 78.90 | p. 77.90 | -1.0 page |
| Appendix C | 8.18 pp | 9.66 pp | +1.48 |
| Whole PDF | 123 pp | 124 pp | +1 |

### Page span of my sections

* Before (snapshot build): Section 7 intro to 7.3 on pp. 31-39 (7.4 starts
  halfway down p. 39); 7.2 on pp. 33-35, 7.3 on pp. 35-39; Appendix C on
  pp. 101-109.
* After (current build with all agents' files, `/tmp/w5-recA/main.aux`):
  Section 7 starts p. 31; 7.1 p. 32; 7.2 pp. 33-34; 7.3 pp. 34-39 (7.4
  starts at the top of p. 39); Appendix C pp. 95-105 (C.1 p. 95, C.2 p. 96,
  C.3 p. 99, C.4 p. 101, C.5 p. 102, C.6 p. 103, C.7 p. 104).

## Labels moved

All to Appendix C (`app:recourse-convex`), labels unchanged:

* `prop:star` (Section 7.2 -> Appendix C.2), with its setup paragraph.
* `thm:cv-recog` (Section 7.3 -> Appendix C.4, retitled "Recognition of
  affine selectors"; `eq:recog-system` was already there).
* Unlabelled text: the multilevel paragraph and the oscillation paragraph
  (-> C.2), the discussion after `prop:cv-limit` (-> C.7).

`prop:cr-osc` and `ex:cr-star32` were already in Appendix C.

## Adjudication of assigned findings

* **M-recourse-1 - ACCEPTED (minimal fix, made precise).** The comparison in
  Theorem `thm:cv`(iv) holds for the Euclidean number only. (iv) now reads:
  L_i <= (H_0)_ii; hence, if F has point growth with constant g and L' is
  an upper coordinate curvature of F for every coordinate, retained and
  private, then kappa(L^+,g) <= kappa(L',g): the parameter kappa_V of (iii)
  never exceeds the Euclidean condition number of F with the private
  variables kept as ordinary coordinates. The proof of (iv) now derives
  L' >= max{(H_0)_ii,0} >= L_i^+ (Definition `def:curvature` needs L' >= 0,
  and l_i < u_i) and uses Lemma `lem:valuefunction`(b) for g. The optional
  strengthening (stating Theorems `thm:valuefn`(b) and `thm:cv`(iii) with
  the weighted kappa-bar_V) was not made: it is not needed for correctness,
  and it would change statements that the introduction and Table 1 cite.
* **M-recourse-2 - ACCEPTED.** recourse-valuefn.tex: "Section 7.3 evaluates
  V exactly and certifies curvature bounds that can cancel such stiff convex
  terms (Theorem `thm:cv`), though not always (Proposition `prop:cv-limit`);".
  The optional change in recourse-convex.tex:5-6 was also made ("depends
  only on the coordinate curvature and the growth of the reduced
  objective").
* **M-recourse-3 - ACCEPTED.** Section 7.2 retitled "Bag-local corrections
  with exact or certified recourse" (Theorem `thm:cr-filter` allows
  eps_or >= 0). The roadmap no longer says "valid with exact recourse" only.
* **M-recourse-4 - ACCEPTED (wording adjusted).** Added to Theorem
  `thm:cv`(iii): "Without point growth of F, the exact procedure has no
  termination guarantee; if every Y_t is a box, Theorem `thm:valuefn`(c)
  applies instead, and EX stops on every instance." "Has no termination
  guarantee" replaces "is not guaranteed to stop" with the same meaning; we
  do not claim an instance on which it fails to stop. Checked: with box Y_t
  the model is a rational quadratic on a mixed box of `eq:model`, the
  hypotheses of `thm:valuefn` hold (L_i^+ rational of polynomial length,
  exact QP oracle by Lemma `lem:cv-bits`), and `thm:exact` states that EX
  stops on every instance.
* **C-consistency-4 - ACCEPTED, no change in my files.** In Section 7, r is
  the number of private blocks, as CONVENTIONS section 4 prescribes; the fix
  (Table 2 entry for r, renames in Section 8) is in setting.tex and
  constraints.tex, owned by other groups.
* **C-consistency-5 - ACCEPTED for my file.** The polynomials P_L and P in
  the proof of Theorem `thm:valuefn`(b) (Appendix C.1) are now pi_L and
  pi_0 (P is reserved for {i : L_i > 0}). pi with a subscript is not used
  elsewhere; the Farkas multipliers pi (no subscript) in Section 7.3 and
  C.4 are in different parts. The eta, q, nu and ETH parts concern other
  groups' files.
* **C-writing-17 - ACCEPTED.** Appendix C retitled "Value functions, local
  corrections and convex recourse: proofs and supplements"; its opening
  sentence now says it contains the proofs and the supplementary results
  summarized in Sections 7.1-7.3. Subsection C.4 retitled "Recognition of
  affine selectors" because it now holds the statement.
* **C-writing-19 - ACCEPTED.** Every "optimizer" in my five files is now
  "minimizer" (Theorem `thm:cr-filter`(a),(b), Theorem `thm:cv`(ii),(iii)
  and proof, `prop:star`, `prop:cr-osc`, proofs in C.2, Example
  `ex:cr-star32`, Lemma `lem:cv-height` title, the proof of
  `thm:cv-recog` ("central minimizer")). "Affine optimal selector",
  "optimal set" and "optimal value" are unchanged.
* **C-writing-21 - MODIFIED.** recourse.tex now reads: "The condition
  numbers of Section 5 are built from the coordinate curvatures L_i of F and
  a growth constant. Stiff convex terms, which are easy to optimize, can
  make the curvatures large. A residual problem with combinatorial
  structure can make the point-growth constant small, through nearly tied
  endpoint assignments of its coordinates, and the bags large, if it is
  dense." Changed from the proposed text: "point-growth" (near ties of
  coordinates with L_i = 0 do not affect the weighted constant gamma), and
  the claim is about the growth constant, not kappa (with L = 0, kappa = 1;
  see the corrected C-writing-3 caveat).
* **R-referee-4 - ACCEPTED for my file, partly.** Appendix C.1 no longer
  names the exponent e_i: "The integer exponents that define the meshes
  h_ij in Section 5 are now O(pi_L(I))", so the text stays correct whether
  or not the core group renames e_i to varpi_i. The other renames (eta, J,
  R, Table 2) are in other groups' files. The unit vectors e_i, e_j in
  Sections 7.1 and 7.3 have the standard meaning and are unchanged.

## Requests for other files

1. **limits** (limits.tex:41, bullet "Local corrections"): Proposition
   `prop:star` is now in Appendix C. Change "(Proposition~\ref{prop:star}
   in Section~\ref{sec:recourse})" to "(Proposition~\ref{prop:star} in
   Appendix~\ref{app:recourse-convex})". Optional, limits.tex:678: add
   "(Appendix~\ref{app:recourse-convex})" after the first
   "Proposition~\ref{prop:star}".
2. **front** (intro.tex:230): if the rewritten "Conditional recourse"
   paragraph keeps the reference to `prop:star`, write
   "(Proposition~\ref{prop:star} in Appendix~\ref{app:recourse-convex})".
   The verified C-writing-2 text drops it, which is also fine. The
   paragraph may also say that bag-local corrections need "exact or
   certified" recourse, matching the new title of Section 7.2.
3. **front** (conclusion.tex): Appendix C.7 cites "Section
   `sec:conclusion`, question 1" for measuring curvature and growth only
   where near-optimal points lie. This was already so before W5. If the
   open questions are renumbered, keep "Negative curvature" as question 1 or
   tell recA (or the coordinator) the new number.
4. **coreA/coreB** (setting.tex, Table 2, C-consistency-4): the entry for r
   should say "in Section 7, the number of private blocks", which matches
   my files.

## Checks run (local, targeted)

* `latexmk -pdf -interaction=nonstopmode main.tex` in `/tmp/w5-recA` (copy
  of the current main.tex, macros.tex, references.bib, sections, figures):
  126 pages, no LaTeX errors. My five files give no warnings (no undefined
  references, no overfull or underfull boxes; attribution by the file
  stack in main.log). The final build has no undefined references; the
  remaining warnings are not from my files: the undefined citation
  `AbelloEtAl2001` (p. 61) and one overfull box in appendix-tu.tex. An
  earlier build in this round showed undefined tu labels from the tu
  group's work in progress.
* Baseline build of the pre-W5 snapshot (`/tmp/w5-recA-base`, 123 pages)
  and isolated build of the snapshot plus my five files (`/tmp/w5-recA-iso`,
  124 pages, no undefined references) for the page measurements above.
* Label sets of my five files before and after: identical (41 labels).
* grep of all sections for references to the moved labels (`prop:star`,
  `thm:cv-recog`, `prop:cr-osc`, `ex:cr-star32`, `rem:cv-unstable`,
  `prop:cv-limit`) and for uses of the multilevel paragraph: only the
  references listed in the requests above are outside my files.
* No exact-arithmetic script was needed: no formula or constant changed.
  The new (iv) is monotonicity of kappa(.,g) plus L' >= L^+, and the new
  sentence in (iii) cites existing results (checked against the statements
  of `thm:valuefn`(c) and `thm:exact`).

These are local checks only; CI results are separate and were not
inspected.

## Unresolved

* None in my files. The cross-file updates above (mainly limits.tex:41) are
  needed so that no text places `prop:star` in Section 7.

## Verification

Verifier for recA. I diffed the five files against
`process/w5/sections-before-w5/` and checked the result against CUTPLAN
(recA), CONVENTIONS and `process/w5/assign/recA.json`. None of the assigned
findings has a `verifier` field.

### Outcome

The revision is correct. All three cut-plan items are done. The moved blocks
are complete: every sentence of the snapshot either survives (in the main
text or Appendix C) or was reworded as the report states. I checked this
with a sentence-level comparison of the old and new files. The labels are
unchanged (41 before and after, the same set), and there are no duplicate
labels anywhere in `sections/`. The appendix proofs have all the definitions
they use:
* the setup paragraph of `prop:star` moved together with it;
* the definition of an affine optimal selector moved together with
  `thm:cv-recog`, and C.4 comes before Example `ex:cv-fm` (C.6), which uses
  the term;
* the discussion moved to C.7 cites `rem:cv-unstable` (C.6), which comes
  earlier.

The main text no longer uses `V^G`, `m^F`, "constant-correction test" or
"affine optimal selector". The CORE proof uses only `lem:cr-cell` and
`thm:cr-filter` (recourse-cuts.tex:205, 212). The cross-file request to
limits is already done: limits.tex:545 now cites `prop:star` in Appendix
`app:recourse-convex`. Conclusion question 1 is still "Negative curvature",
so the citation in C.7 is correct.

I agree with every adjudication. I re-derived each changed statement:
* **M-recourse-1.** The new (iv) is correct. Definition `def:curvature`
  needs L' >= 0, and l_i < u_i holds by `eq:model`. Def. `def:cv-model`
  makes (H_0)_ii the full diagonal entry. Hence L' >= max{(H_0)_ii, 0}
  >= L_i^+, and kappa(., g) = max{1, ./g} is nondecreasing. Lemma
  `lem:valuefunction`(b) gives the growth of V that (iii) needs.
* **M-recourse-4.** If every Y_t is a box, F is a rational quadratic on a
  mixed box of `eq:model`. The hypotheses of `thm:valuefn` hold: the
  curvatures L_i^+ are rational with polynomial length, and Lemma
  `lem:cv-bits` gives the exact oracle. `thm:exact` (exact.tex:345) states
  "EX stops", and C.1(c) derives termination from it.
* **C-writing-21.** The point-growth reading is right: near ties among
  residual coordinates with L_i = 0 do not change the weighted constant.
* **The 7.2 summary.** It matches `prop:star`(B): p = 2, kappa < 11, and
  the threshold dh(1/2-h)+2h^2-1/2 grows like sqrt(m) h. It also matches
  `prop:cr-osc`.
* **The 7.3 summary.** The qualifier "whose domain is a box" is required,
  because the theorem assumes Y = [l^Y, u^Y].

### Fixes made by the verifier

1. **Appendix C.1 (stale symbol).** The proof of `thm:valuefn`(b) still
   wrote the stage limit as `J`: "c(J+1)pI^2(...)" and "J=O(pi_L(I)+q)".
   In this round coreA/coreB renamed the stage limit to `j_max` in
   growth.tex and appendix-growth.tex (R-referee-4: J had four meanings).
   Both occurrences now read `j_max`, which matches growth.tex:255-256.
2. **Appendix C.2, multilevel paragraph.** Before the move, "by (a) and
   induction" followed the theorem statement. After the move it follows a
   proof, so "(a)" is ambiguous there. It now reads "by
   Theorem~\ref{thm:cr-filter}(a) and induction".
3. **recourse.tex, C-writing-21 sentence.** The sentence "can make the
   point-growth constant small, through ..., and the bags large, if it is
   dense" was hard to parse. It now reads: "A residual problem with
   combinatorial structure causes two other difficulties: nearly tied
   endpoint assignments of its coordinates make the point-growth constant
   small, and dense interactions among them make the bags large." The
   content is unchanged.
4. **recourse-local.tex, summary of `prop:star`.** "Only if the constant
   grows with the number of outside coordinates" now reads "only if the
   constant is at least a quantity that grows with the number of outside
   coordinates". The proposition gives a threshold for a fixed instance,
   and that threshold grows with m.
5. **Theorem `thm:cv`.** In (iii), "the exact procedure" is now "the
   exact-output procedure", which matches the title of the appendix proof.
   In (iv), "the number L' is an upper coordinate curvature of F for every
   coordinate" is now "L' is a common upper coordinate curvature of F for
   all coordinates". The meaning is unchanged.
6. Two source lines were rewrapped (appendix opening, recourse.tex). This
   does not change the output.

No statement was weakened, and no label was added, removed or renamed.

### Checks run by the verifier (local, targeted)

* Private build of the current tree in `/tmp/w5-recA-verify` (latexmk,
  run twice: after the edits and after the final rewrap). There are no
  LaTeX errors and no undefined references. There are no overfull or
  underfull boxes from the recA files. The only remaining warning is the
  undefined citation `AbelloEtAl2001` (front/limits). The first build also
  showed an overfull box (0.79pt) in setting-growthcert.tex, which belongs
  to another group; it was gone in the second build.
* Rendered text of the 7.2 summary checked with pdftotext.
* Label sets before and after compared, and duplicate labels checked
  across all sections.
* grep of all sections for the moved labels and for the notation of the
  moved blocks.
* Sentence-level comparison of snapshot and current text (no lost
  content).
* The page measurements in the report agree with the stored builds: Section
  12 starts on p. 78 in `/tmp/w5-recA-base` and on p. 77 in
  `/tmp/w5-recA-iso`, and 7.4 moves from p. 39 to p. 38. Main text: -1
  page.
* No exact-arithmetic script was run. No formula or constant changed, and
  the W4 exact checks of `prop:star`, `ex:cr-star32` and `prop:cv-limit`
  still cover the moved statements, which are verbatim.

These are local checks only; CI was not inspected.

### Page span after verification (current full tree, `/tmp/w5-recA-verify/main.aux`)

Section 7 starts on p. 30. 7.1 starts on p. 31, 7.2 on p. 32 and 7.3 on
p. 33; 7.4 starts on p. 38. Appendix C covers pp. 92-102 and Appendix D
starts on p. 102. The whole PDF has 126 pages. These numbers are one page
lower than in the revision report's build because other groups' concurrent
cuts come earlier in the paper.

### Unresolved

* None in the recA files.
* The optional strengthening of M-recourse-1 was not made: stating
  `thm:valuefn`(b) and `thm:cv`(iii) with the weighted kappa-bar_V. It is
  true but not needed for correctness. It would change statements that the
  introduction and Table 1 cite.
* Cross-file requests: both are already done. limits.tex:545 places
  `prop:star` in Appendix C, and setting.tex:189 (Table 2) lists r as the
  number of private blocks in Section 7.
