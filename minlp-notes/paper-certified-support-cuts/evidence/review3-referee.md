# Review round 3: referee closure (Journal of Global Optimization)

**Resolution (2026-10-04, after this review).** The Part 5S replay finished: `experiments/v5/runs/partS5/replay.json` reports `passed: true`, 47,168 of 47,168 cuts replayed (40,700 polytope, 6,468 star), coverage complete, no failed runs, and all tampering controls rejected in modes agg-star, agg-star4 and rowdir-star4, including the star-certificate mutations in agg-star. `R10_numbers_check.py <extracts> replay` then gave 274,489 recorded cuts, 92,222 distinct rows and passing replays in every part. The campaign-5 summaries were regenerated; only their replay line changed. The blocking finding about the 5S replay is closed.

Manuscript: "Certified support cuts for shared nonlinear expressions and quadratic blocks"
(`main.tex`, `sections/*.tex`, `main.pdf`, 67 pages). I read the typeset text in
`development/draft-round3/main.txt`. Its sources, figures, bibliography and PDF are identical to
the current files (`diff -rq`, `cmp`). Page numbers are PDF pages.

The task of this lens: check every finding of the six round-2 lenses
(`evidence/review2-{referee,math,numbers,implementation,literature,writing}.md`, 100 items) against
the current manuscript, list what is not fully resolved, and give an overall assessment.

**Replay status at the time of this review:** the replay of Part 5S (47,168 cuts) had not finished when this review ended. The process `replay_v5.py runs/partS5` started at 23:24 on 2026-10-03, after the run summaries and 16 minutes before `main.pdf` was compiled (23:40). It was still running at 00:43 on 2026-10-04, the end of this review's 60-minute bounded wait. At that point `runs/replay-partS5.log` was empty and `runs/partS5/replay.json` did not exist. Parts 5C-a and 5C-b passed. Finding O1 is therefore open. If the replay passes, O1 reduces to housekeeping.

---

## 1. Summary

Of the 100 round-2 items, **76 are resolved, 23 partially resolved and 1 not resolved**. Many of the
partial items are the same issue seen by several lenses (abstract: referee F6 = numbers F18 =
writing W3; figures: F14 = W11; front matter: F15 = W22; length: F3 = W13). Counted once, the open
issues are:

| # | Issue | Severity | Round-2 items |
|---|---|---|---|
| 1 | The Part 5S replay (47,168 cuts) had not finished when the manuscript was compiled, yet the abstract, Section 1, Section 8.2 and Section 8.7 state that all 274,489 records passed replay | critical until the replay passes | new (N1) |
| 2 | Length: 67 pages (main text 36, references 9 with 130 entries, appendices 22); round 2 asked for at most 25 pages of main text | major | F3, W13 |
| 3 | Front matter: no authors, no funding or competing-interest declarations, no archive DOI or licence, no MINLPLib terms | minor (mandatory for Springer) | F15, W22 |
| 4 | Abstract: "fixed in advance" without saying that the configuration was selected after a post hoc diagnostic; omits that SCIP-nolocks solved the whole binding-row family faster and that Gurobi solved more star instances; (C2) not named | minor | F6, N-F18, W3 |
| 5 | Section 8.6, the Section 8 introduction and the conclusions say that the star algorithm of Theorem 4.4 was run in the solver and "makes them cheap to certify"; the solver used the simpler cubic oracle | minor | F4 (residual), new (N2) |
| 6 | Smaller residuals: replay total not split by family (F11); presolved-space remedy in the conclusions (F12); Figure 2 "LP point" label (F14); "achieved as much or more" (N-F11); Section 8.7 lacks the convex-reformulation limitation (F10); "against the row stored by SCIP" (I-F14); orphan bibliography entries (L-F1, L-F12); App. H labels "Part B2/D" (W8); "path-family" before definition (W17); HiGHS citation (W18); "We answer" (F17); Table 1 Gurobi runs (F16 iv); standard references (F20); structure suggestions (W23) | minor / suggestion | see Section 3 |
| 7 | New, small: paragraph order in Section 8.5 (N4); Part 5C-b "ended by itself ... same results" (N5); Table 6 header "Campaigns 2--4" (N6); strict invalidity of global-solve constants not reported (N7); campaign-5 summaries say "Replay: not run yet" (N8) | minor / suggestion | new |

Everything a round-2 referee called *major* in the science is resolved: the "representation"
reading is restricted to three variables and the four-variable counterexample is developed into a
positive result (F1/M1/L-F5); the "only if" necessity claims are gone (F2/M6/N-F1/W1); the 38% error
rate is attributed to samples only (N-F2/W2); the distinct-row count is given (N-F3); the star
structure is tested in the solver (F4, Part 5S); a numerical global solve is compared with the
certificate (F5, Part 5U); the callback limit, concurrency and exact-arithmetic refusals are
disclosed (I-F1 to I-F3); the missing literature is cited (L-F1 to L-F4); the mode names and the
attribution paragraph are rewritten (W4 to W7). Only length (F3) remains open among the round-2
majors, and it got worse.

---

## 2. Status of every round-2 finding

Status codes: **R** resolved, **P** partially resolved, **N** not resolved. "Where now" cites the
current file and line; "remains" points to Section 3.

### 2.1 Referee lens (`review2-referee.md`, F1-F20)

| # | Round-2 issue | Status | Where now / what remains |
|---|---|---|---|
| F1 [major] | "Representation, not strength" stated generally | R | 01-introduction.tex:59-67; 03-composition.tex:297, 332-354 (BNW Example 4, full-gap instances with 5 and 7 variables, verified by `M7_dense_fullgap.py`, re-run here); 09-conclusions.tex:6-13. The optional BNW-path experiment was not run (optional). |
| F2 [major] | "Only if ... whole row first" | R | 01b-results.tex:19-22; 08e-path.tex:142-144; 09-conclusions.tex:37-43. |
| F3 [major] | Paper too long | **N** | Worse: 67 pp. (main text pp. 1-36, references pp. 36-45, appendices pp. 45-67), 130 cited references (was 56 pp., 112). Moved: Prop. 3.5 examples (App. A), hierarchy (App. D), funnel table (App. H). Not done: halving Sec. 3.4 (it grew), cutting 6.2/6.3/7.1, one statement of the MINLPLib result, condensing App. F, pruning the bibliography. → Section 3, item O2. |
| F4 [major] | Star algorithm not used by the solver | P | Part 5S (08f-star.tex:23-92) puts star blocks with up to 16 leaves into the separator and compares with SCIP, SCIP-nolocks, SCIP-extra and Gurobi; Sec. 4.2 (04-quadratic.tex:99, 240-253) describes the implemented oracle accurately. Remaining: the solver certifies star blocks with the simpler $O((m+k)^3)$ oracle, not the sweep of Theorem 4.4, but 08a-setup.tex:19, 08f-star.tex:3-6 and 09-conclusions.tex:49-51 say otherwise → O5. |
| F5 [major] | No comparison with a numerical global solve | R | Table 2 row U3; 08b-validity.tex:78-92; 09-conclusions.tex:25-28; `evidence/ablation-global-solve.md`. Suggestion N7. |
| F6 [minor] | Abstract | P | (i) δ defined, (ii) $m_0$, (iii) moot ("did not help SCIP"), (v) "20 fresh path instances": done. (iv) "fixed in advance" still hides the post hoc selection; (vi) exact elimination (C2) not named; (vii) "at most 10 for SCIP" does not say three settings → O4. |
| F7 [minor] | Part D informativeness in the introduction | R | 01b-results.tex:13-16. |
| F8 [minor] | C4 cap binding; "needed sixteen cuts" | R | Part 5C-b, 08e-path.tex:178-182; conclusions no longer claim a requirement. Precision item N5. |
| F9 [minor] | "No SCIP setting"; Gurobi root | R | 08e-path.tex:118-120, 200-204; SCIP-nolocks now run on 4C3/4C4 (Part 5C-a). |
| F10 [minor] | Convex reformulation; Shapley-Folkman | P | 08e-path.tex:33-36, 190-199. Remaining: the one-sentence limitation in Section 8.7 (08g-summary.tex:34-37) → O6(e). |
| F11 [minor] | Replay total dominated by the constructed family | P | Distinct rows given (08b-validity.tex:5-8), but the family split is never stated; now 5,267 of 274,489 records (1.9%) are MINLPLib cuts → O6(a). |
| F12 [minor] | Presolved-space remedy breaks the certificate chain | P | 08d-funnel.tex:27-29 fixed; 09-conclusions.tex:28-32 still offers "works in the presolved space" as a remedy → O6(b). |
| F13 [sugg.] | Mimic SCIP's coefficient handling | R | 08d-funnel.tex:29-31. |
| F14 [minor] | Figure label overlaps | P | Figure 1 clean (rendered p. 8). Figure 2: no overlap, but "LP point" now sits beside the solid builder-to-discovery line, not the dotted arrow (rendered p. 21) → O6(c). |
| F15 [minor] | Front matter, declarations, availability | P | Keywords and MSC added (main.tex:25-30); availability lists versions, CPU, Gurobi licence; App. F cross-reference fixed (A-separation.tex:234). Missing: authors (main.tex:18), funding and competing-interest statements, DOI and licence, MINLPLib terms → O3. |
| F16 [minor] | Tables | P | (i) sense marked in Tables 9-11; (ii) full-run tables with all comparators (Tables 13, 15); (iii) 3P row and the 3P A/B sentence (08c-minlplib.tex:74-76). (iv) Table 1 rows 4C2-4C4 still list Gurobi under "full, root" (08a-setup.tex:96-98); Table 4's caption says Gurobi had no root runs → O6(k). |
| F17 [minor] | Wording and attribution | P | RLT, SOC, DAG, Anstreicher-Burer placement, Ballerstein, model import, filler, contrast pattern: done. "We answer these questions" remains (01-introduction.tex:46) → O6(j). |
| F18 [sugg.] | A/A timing | R | 08c-minlplib.tex:79-80. |
| F19 [sugg.] | Appendix order | R | main.tex:47-54 (A: Sec. 3, ..., H: tables). |
| F20 [sugg.] | Standard references | P | Tawarmalani-Richard-Xiong 2013 and Aubin-Ekeland 1976 added. Tawarmalani-Sahinidis 2002, Yildiran 2009 / Modaresi-Vielma 2017 still absent → O6(l). |

### 2.2 Mathematics lens (`review2-math.md`, M1-M9)

| # | Round-2 issue | Status | Where now |
|---|---|---|---|
| M1 [major] | Representation reading | R | as F1. |
| M2 [minor] | C4 block-closure derivation | R | 08e-path.tex:37-50 (domain $[0,1]^3$, $c\ge1$, projection argument, Lagrangian form, "block closure" defined); Table 14 column "opt.−closure". |
| M3 [minor] | Coupling row at the zero points | R | 08e-path.tex:14-17. |
| M4 [minor] | Hardness example for two-leaf rows | R | 04-quadratic.tex:110-119 (stable-set reduction, Nemhauser-Trotter). |
| M5 [minor] | Implemented star oracle description | R | 04-quadratic.tex:240-247; 07-implementation.tex:97-99. (A new inconsistency elsewhere: O5.) |
| M6 [minor] | Necessity claims | R | as F2. |
| M7 [minor] | Notation clashes | R | masses written out (03:215-219); $\eta_A,\eta_C$ (03:136-137, A-composition.tex:9-10); $\mu_A,\mu_C$ (A-composition.tex:44-46); $\ell_0$ (A-separation.tex:149); $d_i$ (08e:45); alt$=0$ (03:170); abstract $m_0$; rational $p_c$ (A-separation.tex:52). |
| M8 [sugg.] | "Exactly" for C4 references | R | 08e-path.tex:32-36, 49-50. |
| M9 [sugg.] | Small precision items | R | 05-original.tex:175-176; 03:304-305; 04:99; 02:162-168. |

### 2.3 Numbers lens (`review2-numbers.md`, F1-F19)

| # | Round-2 issue | Status | Where now / what remains |
|---|---|---|---|
| F1 [major] | "Only if" | R | as referee F2. |
| F2 [major] | 38% attributed to local solver too | R | 01b-results.tex:5-10; 08g-summary.tex:4-8; 09-conclusions.tex:21-25. |
| F3 [major] | 143,267 counts path cuts twice | R | 08b-validity.tex:5-8 (92,222 distinct rows); Table 2 caption "(995 distinct)". |
| F4 [minor] | Two Table 5 (now Table 4) medians | R | 0.93 and 0.20 in Table 4; "20--32%" (08e:157). |
| F5 [minor] | "Comparable (0.86)" | R | 08e-path.tex:152-155. |
| F6 [minor] | Gurobi gap range | R | 08e-path.tex:121-122. |
| F7 [minor] | "12 at the root node" | R | 08e-path.tex:137 ("18 of them"). |
| F8 [minor] | "Needed 16 cuts per block" | R | Part 5C-b. |
| F9 [minor] | "No SCIP setting" | R | 08e-path.tex:118-120. |
| F10 [minor] | "Rarely gets past discovery" | R | 08c-minlplib.tex:134-137. |
| F11 [minor] | "Already contained what the cuts could add" | P | Rewritten (09-conclusions.tex:34-36), but "SCIP's disabled-by-default separators achieved as much or more" is contradicted by `multiplants_mtg1c` (Table 11: all-diag 8574 vs SCIP-extra 8647, maximization) → O6(d). |
| F12 [minor] | "21 of the 25" | R | A-campaigns12.tex:62-63. |
| F13 [minor] | Load ranges | R | 08a-setup.tex:29-32 (campaign-5 range checked here: 1.09-19.88 apart from 34 spike readings up to 125.85). |
| F14 [minor] | Table 5 (now Table 4) provenance | R | Table 4 "Part" column and caption. |
| F15 [minor] | Order of 3.2 and 3.5 | R | 08e-path.tex:165-166. |
| F16 [minor] | Callbacks column | R | Table 7 "Callbacks". |
| F17 [minor] | Abstract $m_0$ | R | 00-abstract.tex:15. |
| F18 [minor] | Abstract omits SCIP-extra | P | "at most 10 for SCIP" (00-abstract.tex:22-23) → O4. |
| F19 [sugg.] | App. F audit scope, control value | R | A-campaigns12.tex:3-6, 35-37. |

### 2.4 Implementation lens (`review2-implementation.md`, F1-F16)

| # | Round-2 issue | Status | Where now / what remains |
|---|---|---|---|
| F1 [major] | Callbacks 3 → 10 undisclosed | R | Table 7; A-instances.tex:6-9; 07-implementation.tex:147-149. |
| F2 [major] | Up to ten concurrent runs | R | 08a-setup.tex:33-36. |
| F3 [major] | Exact-arithmetic refusals | R | 07-implementation.tex:72-78; A-instances-D.tex:5-9. |
| F4 [minor] | Paired comparisons | R | 08a-setup.tex:36-41; 08g-summary.tex:31-33. |
| F5 [minor] | Kernel coverage, "required value" | R | 07-implementation.tex:86-105, 124-126. |
| F6 [minor] | Table 1, root limits, seed meaning, $t_i$ bounds | R | Table 1; 08a-setup.tex:44-48; 08e-path.tex:6. |
| F7 [minor] | C4 load | R | 08a-setup.tex:30-31. |
| F8 [minor] | Block cap tie-break, Part D cap | R | 07-implementation.tex:91-92; 08c-minlplib.tex:122-125. |
| F9 [minor] | C4 references not "exact" | R | 08e-path.tex:32-36, 49-50; A-instances-D.tex:31-32. |
| F10 [minor] | C4 code written during campaign 4 | R | 08a-setup.tex:16-18. |
| F11 [minor] | Part U deviates from the protocol set | R | 08b-validity.tex:58-61; Table 2 caption lists 3P. |
| F12 [minor] | Availability dependencies | R | 99-availability.tex:13-23. |
| F13 [sugg.] | "LPs" column | R | Table 8 header "directions", caption "sampling and direction LPs". |
| F14 [sugg.] | Replay checks the recorded stored row | P | 06-certification.tex:136-137 is now exact, but 01b-results.tex:3-4 and 08g-summary.tex:3-4 still say replay is "against ... the row stored by SCIP" → O6(f). |
| F15 [sugg.] | Priority/forcecut, once per block, vertices, $T$ | R | 07-implementation.tex:123, 141-143, 120-122. (The definition of $T$ as budget minus preparation is still absent; harmless.) |
| F16 [sugg.] | Prespecified metrics not reported | R | 08a-setup.tex:77-80. |

### 2.5 Literature lens (`review2-literature.md`, F1-F13)

| # | Round-2 issue | Status | Where now / what remains |
|---|---|---|---|
| F1 [major] | Kojima-Kim-Arima missing | P | 03-composition.tex:267-277 (KKA, Kim-Kojima-Toh). The second suggested sentence (Shor exactness on forests/bipartite graphs under sign conditions: Kim-Kojima 2003, Sojoudi-Lavaei 2014, Azuma et al. 2022) was not added, and `SojoudiLavaei2014` is now an uncited bibliography entry → O6(g). |
| F2 [major] | SCIP's cut cleanup | R | 02-setting.tex:137-139; 06-certification.tex:35-47. |
| F3 [major] | Prop. 3.5(ii) is Lagrangian decomposition | R | 03-composition.tex:377-383; 01-introduction.tex:68-69. |
| F4 [major] | Original sources of SCIP's separators | R | 02-setting.tex:160-178. |
| F5 [major] | BNW beyond its scope | R | as referee F1. |
| F6 [minor] | Anstreicher-Burer attribution | R | 02-setting.tex:98-104. |
| F7 [minor] | Fixed-dimension attribution; DK theorem numbers | R | 04-quadratic.tex:67-74, 93-95. |
| F8 [minor] | Xu-Pokutta, He-Liu-Tawarmalani, Saxena-Bonami-Lee, Halbig et al. | R | 02-setting.tex:64-66, 92-94, 126; 01-introduction.tex:23; 05-original.tex:54-55. |
| F9 [minor] | Known facts presented as findings | R | 00-abstract.tex:6-7; 09-conclusions.tex:15-16. |
| F10 [minor] | "Merged blocks are mostly stars" | R | 04-quadratic.tex:99; 09-conclusions.tex:13-14. |
| F11 [minor] | Implicit-discreteness description | R | 02-setting.tex:162-168. |
| F12 [sugg.] | Bibliography hygiene | P | arXiv id for SCIP 8 added; DK locator "Theorem 2 and Corollary 4". Still: uncited `FuriniEtAl2018` (and now `SojoudiLavaei2014`); Nie-Demmel and Nie-Qu-Tang-Zhang example numbers not checked against the journal versions; key/year mismatches → O6(g). |
| F13 [sugg.] | Bernstein enclosure source | R | A-bounds.tex:17. |

### 2.6 Writing lens (`review2-writing.md`, W1-W23)

| # | Round-2 issue | Status | Where now / what remains |
|---|---|---|---|
| W1 [major] | Necessity of whole-row direction | R | as referee F2. |
| W2 [major] | 38% attributed to local minimization | R | as numbers F2. |
| W3 [major] | Abstract: bound, conditions, status | P | $m_0$, δ, "no positive bound", "did not help SCIP", "constructed": done. Post hoc selection and (C2) not stated → O4. |
| W4 [major] | Mode and limit names | R | SCIP / SCIP-nolocks / SCIP-extra defined (08a-setup.tex:50-55); base and wide limits defined (07-implementation.tex:144-149); Table 7 maps code names; Table 14 columns labeled. Code names remain only in Tables 1 and 7, which is acceptable. |
| W5 [major] | "Remainder" in two senses | R | 05-original.tex:24, 101, 187; "Free affine columns" (A-feasible-hull.tex:8); 06-certification.tex:85-86. |
| W6 [major] | Attribution paragraph | R | 08e-path.tex:124-144. |
| W7 [major] | Gurobi root claim | R | 08e-path.tex:200-206. |
| W8 [minor] | Part labels | P | Main text uses 3A-3P, 4B2-4S, 5S-5U. App. H still writes "Part B2", "Part B", "Part D" (A-instances-D.tex:2-3, 13) → O6(h). |
| W9 [minor] | Table 5 (now Table 4) provenance and cells | R | Table 4 (Part column, caption notes, block-closure row, three decimals). |
| W10 [minor] | Appendix-table labels, senses, Table 2 | R | Tables 2, 9-11, 14. |
| W11 [minor] | Figure collisions; Fig. 1(b) sets | P | Fig. 1 fixed, "DAG" removed. Fig. 2 label → O6(c). |
| W12 [minor] | Cross-reference to availability | R | A-separation.tex:234. |
| W13 [minor] | Results stated four times | P | Conclusions rewritten along the W13 text; roadmap duplicate removed. The results still appear in full in the abstract, 01b-results.tex (a 30-line paragraph), Section 8.7 and Section 9 → part of O2. |
| W14 [minor] | Unsupported generalizations | R | 04:99; 09-conclusions.tex:13-14; 08d-funnel.tex:42-43. |
| W15 [minor] | Support cut vs support inequality | R | 02-setting.tex:33-35. |
| W16 [minor] | Presolve step description | R | 02-setting.tex:162-168. |
| W17 [minor] | Terms used before definition | P | glued pair relaxation, remainder direction, block closure, "no positive bound": done. 01b-results.tex:6 still says "path-family cuts" ten lines before the family is introduced (01b:16-17) → O6(i). |
| W18 [minor] | Abbreviations, tool citations | P | RLT, SOC, OSiL, SLSQP (Kraft), "time budget": done. HiGHS is cited only in the availability statement, not at first use (07-implementation.tex:6) → O6(i). |
| W19 [minor] | Notation clashes in Sec. 3 and 8.1 | R | as M7; 08a-setup.tex:69 ($z$, $z'$). |
| W20 [minor] | Informal sentences | R | 07-implementation.tex:21; 08b-validity.tex:15; 08g-summary.tex:26; 09-conclusions.tex:21; 03-composition.tex:224-225. |
| W21 [minor] | Overlong sentences | R | 08c-minlplib.tex:13-18; 06-certification.tex:44-47; 08b-validity.tex:52-58. |
| W22 [minor] | Front matter | P | as F15 → O3. |
| W23 [sugg.] | Structure | P | Contribution bullets split, Prop. 3.5 examples and hierarchy moved, 8.3 lead sentence added. Still open (optional): forward reference in the proof of Prop. 3.1 to Theorem 3.2; uncited application examples (01-introduction.tex:11-12); Table 7 in the appendix → O6(m). |

---

## 3. Items still open, with fixes

Severity: *critical* = wrong headline claim or result; *major* = a referee would require the change;
*minor*; *suggestion*.

### O1 (= N1) [critical until the replay passes] The replay of Part 5S had not finished when the replay claim was written

- **Location.** 00-abstract.tex:18-19 (p. 1: "Every recorded cut passed replay"); 01b-results.tex:2-4
  (p. 3: "All 274,489 cut records of the last three campaigns passed a fresh-process replay");
  08b-validity.tex:3-9 (p. 25: "Every recorded cut of campaigns 3 to 5 passed replay ... 131,222 in
  campaign 5 ... In every part and cut mode, each of the fourteen corrupted records ... was
  rejected"); 08g-summary.tex:3-4 (p. 34).
- **Evidence.** `verification/R10_referee_closure.py`: campaign 5 recorded 47,168 cuts in Part 5S
  and 84,054 in Part 5C-b (0 in 5C-a); 7,498 + 30,998 + 104,771 + 131,222 = 274,489, so the total
  includes Part 5S. `experiments/v5/runs/partC5a/replay.json` and `partC5b/replay.json` exist with
  `passed: true` (84,054 cuts replayed, tamper modes rejected). For Part 5S there was no
  `replay.json`; `runs/replay-partS5.log` was empty and the replay process (`replay_v5.py
  runs/partS5`, started 23:24, after the run summaries) was still running when `main.pdf` was
  compiled (23:40). `experiments/v5/results-s5/results.md` says "Replay: not run yet". The README
  estimates 1-1.5 h for this replay (0.12 s per four-variable polytope cut).
  I waited 60 minutes (23:43-00:43), polling every 60 s. At 00:43 the process had run for 1 h 19 min and the log was still empty.
  The 1,135 cuts of the out-of-protocol rerun `partS5-rerun-spike` have no replay and are not
  mentioned.
- **Fix.** Let the replay finish. If it passes (all 47,168 cuts replayed, the fourteen corruptions and the star-specific corruptions rejected), keep the text and regenerate `results-s5` (N8). Then either replay the 1,135 cuts of the rerun or exclude them explicitly, by adding "; its cuts are not part of the replay total" after "would not change" (08f-star.tex:92). If the replay does not pass, or has not finished at submission, replace 08b-validity.tex:3-5 by "Every recorded cut of campaigns 3 and~4 and of Part~5C-b passed replay: 7{,}498 cuts in the prospective parts of campaign~3, 30{,}998 in Part~3P, 104{,}771 in campaign~4 and 84{,}054 in Part~5C-b, 227{,}321 records in total." Then state the Part 5S status separately, and restrict 00-abstract.tex:18, 01b-results.tex:2-4 and 08g-summary.tex:3 to the same scope.

### O2 (= F3, W13) [major] The paper is longer than in round 2

- **Location.** Whole manuscript. Main text pp. 1-36 (§1 1-3, §2 3-6, §3 6-12, §4 12-16, §5
  16-19, §6 19-21, §7 21-24, §8 24-35, §9 35-36), references pp. 36-45 (130 entries), appendices
  pp. 45-67.
- **Evidence.** `pdfinfo` 67 pages; `R10_referee_closure.py`: 130 cited references, 2 uncited
  entries. Round 2 measured 56 pages, 31.5 pages of main text and 112 references, and asked for at
  most 25 pages of main text in this format. At 11 pt with 1 in margins, 36 pages is about 40 pages
  in the Springer template, plus about 30 pages of references and appendices.
- **Issue.** Campaign 5 and the new four-variable material added about 4.5 pages to the main text
  and 6 pages of appendices. The round-2 cut list was mostly not applied. The computational outcome
  is still stated in full four times (abstract; the 30-line paragraph 01b-results.tex:1-30;
  08g-summary.tex:3-23; 09-conclusions.tex:21-51).
- **Fix.** Either split the work (Sections 3-4 and App. A-C as a theory paper; Sections 5-8 as a
  certified-separator paper) or cut to about 28 pages of main text:
  - Replace 01b-results.tex:5-30 by four sentences (validity and Part U; MINLPLib neutral; path
    family; star family), and delete the duplicate statements of Section 8.7 (keep its
    "Limitations" paragraph).
  - Section 3.4: keep the BNW paragraph and the four-variable paragraph; shorten the KKA/DK
    paragraph (03-composition.tex:262-295) to its novelty sentence and two citations.
  - Section 6.2 and 6.3: move the corruption list and the trusted-base enumeration to App. F or the
    availability statement.
  - Section 7.1: keep the three paragraph leads and move the examples ($(0.1x)^2$, domain list, 8
    refused models) to App. H.
  - Section 8.3: move "Presolve and the stored-row check (Part 4B2)" and "Larger models (Part 4D)"
    to App. H with two summary sentences.
  - App. F: keep the contract, Theorem F.2 and the irrational example; reduce the ellipsoid and
    grid variants to a remark.
  - Move Tables 8-17 to an online supplement.
  - Prune the bibliography to about 90 entries (round 2 listed candidates).

### O3 (= F15, W22) [minor, mandatory for submission] Front matter and declarations

- **Location.** main.tex:18 (`\author{}`); no declarations section; 99-availability.tex:1-23.
- **Evidence.** p. 1 has no author block; no funding, competing-interest or ethics statement;
  the availability statement names "the supplementary archive" without a persistent identifier or
  licence and does not state under which terms the MINLPLib files are redistributed.
- **Fix.** Add authors and affiliations; add after the availability statement:
  "\section*{Declarations} \paragraph{Funding.} [...] \paragraph{Competing interests.} The authors
  have no competing interests to declare." In 99-availability.tex:1 replace "The supplementary
  archive of this article contains" by "The supplementary archive (Zenodo, doi:[...], licence
  [MIT/CC BY 4.0]) contains", and after "archived with their hashes" add "under the MINLPLib terms
  of use".

### O4 (= F6, N-F18, W3) [minor] Abstract: selection, binding row, stars, (C2)

- **Location.** 00-abstract.tex:15-23 (p. 1).
- **Issue.** (a) "a configuration fixed in advance" is literally true (it was fixed before the fresh
  instances were generated) but hides that it was chosen after a post hoc diagnostic on earlier
  instances of the same generator (08e-path.tex:124-144). (b) The abstract reports only the
  favorable comparisons: it omits that on the binding-row variant SCIP-nolocks solved all 20
  instances faster than the cut modes (08e-path.tex:166-172) and that on the star family Gurobi
  solved 22 instances against 19 (Table 5). Both are stated in Section 1 and Section 9. (c) "at
  most 10 for SCIP" covers three SCIP settings. (d) "Eliminating the model rows gives cuts ...
  valid as stored if ..." omits that elimination must be exact (C2).
- **Fix.** Replace the abstract by the text below (250 words with math counted as one word, the
  count used in round 2; the current abstract has 248):

  > Global solvers for nonconvex mixed-integer nonlinear programs relax nonlinear expressions one
  > at a time and lose their dependence through shared variables; support cuts of the hull of their
  > joint graph keep it. Gluing exact pair hulls on shared moments is known to lose strength; we
  > quantify the loss. For a family of quadratic directions on a three-variable path, the glued
  > relaxation misses nothing or $\delta^2/2$, depending on whether two point sets at distance
  > $\delta$ interleave; an interface that shares $\kappa$ moments gives no positive bound exactly
  > when local zero sets alternate at least $\kappa+1$ times; and from four variables on, joint
  > blocks can be strictly stronger than first-level semidefinite relaxations. For quadratic stars
  > with $k$ leaves, $m$ center--leaf rows and $m_0$ center rows we give an exact rational support
  > algorithm with $O(m_0+(m+k)\log(m+k))$ operations. Eliminating the model rows exactly gives
  > cuts in the original variables, valid as stored if their bound is certified for the exact
  > binary64 direction, rounding is corrected and the stored row is checked. Every recorded cut
  > passed replay, whereas sample-based constants would have cut off feasible solutions. On
  > MINLPLib models the cuts did not help SCIP. On constructed path and star families they closed
  > nearly all of SCIP's root gap. A configuration chosen after a diagnostic on earlier instances
  > solved all 20 fresh path instances, against at most 10 for three SCIP settings and 5 for
  > Gurobi; with a binding coupling row, SCIP without one presolve step solved all instances
  > faster, and on stars Gurobi solved more.

  (The sentence "Every recorded cut passed replay" depends on O1.) "First-level" also fixes a
  small overstatement of the current abstract: dense Lasserre relaxations of higher order converge
  (03-composition.tex:253-258), so "dense semidefinite relaxations" without the qualifier is too
  broad; Section 3.4 and Section 9 already say "first-level".

### O5 (= F4 residual, N2) [minor] Theorem 4.4 versus the oracle that ran in the solver

- **Location.** 08a-setup.tex:19-20 (p. 24: "Campaign 5 ... runs the star algorithm in the
  solver"); 08f-star.tex:3-6 (p. 33: "the star algorithm of Theorem 4.4 was not needed there. We
  test it in two ways: offline at large scale, and inside the solver"); 09-conclusions.tex:49-51
  (p. 35: "Joint blocks larger than the separator's default of four variables thus matter, and the
  near-linear star algorithm makes them cheap to certify").
- **Evidence.** 04-quadratic.tex:240-251 and 07-implementation.tex:97-99 say correctly that the
  separator uses the simpler oracle ($O((m+k)^3)$ operations). `campaign-v5-protocol.md:30-35` and
  `experiments/v5/README.md:76-83`: star blocks are certified by "the inherited constrained-star
  oracle (`theory/quadratic_star.py`)", certificate `quadratic_star`. `results-s5/results.md`
  (root runs): 4,650 `quadratic_star` calls on blocks of 5, 9 and 17 variables, median 7.8 ms. At
  these sizes the cubic oracle is already cheap; the near-linear sweep matters only at hundreds of
  leaves (Part 4S: 0.43 s against 12 ms at $k=100$).
- **Fix.**
  - 08a-setup.tex:19-20: "Campaign~5 was designed after campaign~4: it adds star blocks, certified
    by the star oracle, to the solver, adds the remaining comparators ...".
  - 08f-star.tex:3-6: "The blocks of Sections~\ref{sec:minlplib}--\ref{sec:mechanism} have at most
    four variables, so no star oracle was needed there. We test the algorithm of
    Theorem~\ref{thm:star} offline at large scale, and star blocks, certified by the simpler star
    oracle of Section~\ref{sec:star}, inside the solver on a family whose merged blocks are stars
    with up to 16 leaves."
  - 09-conclusions.tex:49-51: "Joint blocks larger than the separator's default of four
    variables thus matter. With up to 16 leaves even the simpler star oracle certified them in a
    few milliseconds; the near-linear algorithm of Theorem~\ref{thm:star} keeps this cost low for
    stars with thousands of leaves (Part~4S)."

### O6 Smaller residuals (minor unless marked)

(a) **F11 — family split of the replay total.** 08b-validity.tex:3-6 (p. 25). Of the 274,489
records, 5,267 are MINLPLib cuts (1.9%); the rest come from 110 instances of two generators with
dyadic data. Add after "274,489 records in total": "; 5,267 of them are cuts on MINLPLib models,
the others on the constructed families".

(b) **F12 — presolved-space remedy.** 09-conclusions.tex:28-32 (p. 35). Replace "loses cuts
unless it works in the presolved space or prevents these reductions, and preventing them weakens
SCIP's own relaxation" by "loses cuts unless it prevents these reductions, which weakens SCIP's own
relaxation, or certifies the floating-point presolve steps it relies on".

(c) **F14/W11 — Figure 2 label.** figures/pipeline.tex:68 (p. 21). Rendered at 200 dpi: "LP point"
sits immediately right of the solid arrow from the model builder to block discovery, so it reads as
labeling that arrow. Change `node[pos=0.25,above,font=\small] {LP point}` to
`node[pos=0.25,below,font=\small] {LP point}`, which puts the label under the dotted segment, in
the empty band above the direction-LP box.

(d) **N-F11 — "as much or more".** 09-conclusions.tex:34-36 (p. 35). Table 11:
`multiplants_mtg1c` (maximization) has root bound 8574 with `all-diag` against 8647 for SCIP-extra,
so the cuts did better there. Replace "while SCIP's disabled-by-default separators achieved as much
or more" by "while SCIP's disabled-by-default separators achieved as much or more on all but one of
them".

(e) **F10 — limitation sentence.** 08g-summary.tex:34-37 (p. 34). After "The constructed families
favor block cuts" add "; both path families also have a convex mixed-integer reformulation that
Gurobi solves in about a second, so they test whether a solver recovers the block structure from
the nonconvex formulation, not whether the problems are hard".

(f) **I-F14 — what replay compares.** 01b-results.tex:3-4 (p. 3) and 08g-summary.tex:3-4 (p. 34):
replace "against the source model and the row stored by SCIP" by "against the source model and the
SCIP row recorded when the cut was generated" (as 06-certification.tex:136-137 says).

(g) **L-F1, L-F12 — orphan bibliography entries** [suggestion]. `SojoudiLavaei2014` (new) and
`FuriniEtAl2018` are in references.bib but never cited (BibTeX drops them, so readers see nothing).
Either add the sentence proposed in round 2 after 03-composition.tex:301 ("Exactness of Shor
relaxations on forests and bipartite graphs under sign conditions
\citep{KimKojima2003,SojoudiLavaei2014,AzumaEtAl2022} concerns homogeneous formulations; the linear
terms of \eqref{eq:family} add the homogenizing variable to every clique, so these results do not
apply here.") or delete both entries.

(h) **W8 — appendix labels.** A-instances-D.tex:2-3, 13 (p. 57): "Part~B2 ... Part~B ... Part~D"
→ "Part~4B2 ... Part~3B ... Part~4D".

(i) **W17, W18** [suggestion]. 01b-results.tex:6: "sampled path-family cuts" → "sampled cuts on the
constructed path family of Section~\ref{sec:composition}". 07-implementation.tex:6: "HiGHS
\citep{HuangfuHall2018} for the direction LPs".

(j) **F17** [suggestion]. 01-introduction.tex:46: "We answer these questions" → "We address these
questions"; Section 9 itself lists question (1) as partly open (09-conclusions.tex:56-59).

(k) **F16(iv)** [suggestion]. Table 1 caption (08a-setup.tex:84-86): add "Gurobi had full runs
only."

(l) **F20** [suggestion]. Cite Tawarmalani and Sahinidis (2002) with the factorable-relaxation
references (02-setting.tex:51) and Modaresi and Vielma (2017) or Yildiran (2009) next to
Blekherman-Dey-Sun (02-setting.tex:90).

(m) **W23** [suggestion]. The proof of Prop. 3.1 still invokes Theorem 3.2 "below"
(03-composition.tex:70-71); the application examples at 01-introduction.tex:11-12 have no
citations; Table 7, needed to read Section 8, is in App. H.

---

## 4. New findings of this round (not in round 2)

N1 is O1 above, and N2 is O5.

### N3 [suggestion] → see O4 (the "first-level" qualifier).

### N4 [minor] Paragraph order in "A binding coupling row" makes "they" ambiguous

- **Location.** 08e-path.tex:160-188 (p. 32).
- **Issue.** The SCIP-nolocks sentences (166-172) were inserted between the cut-mode results;
  the next sentence, "At the root they closed a median of 95% and 99% of SCIP's root gap" (173),
  now reads as if "they" were the joint blocks of the preceding clause or SCIP-nolocks.
- **Fix.** Move 166-172 ("SCIP-nolocks, however, ... is small.") to the end of the paragraph, after
  "... below SCIP's root bound on half of the instances." (188), and begin 173 with "At the root
  the two cut modes closed a median of ...".

### N5 [minor] Part 5C-b: "ended by itself" and "the same results"

- **Location.** 08e-path.tex:178-182 (p. 32).
- **Evidence.** `R10_referee_closure.py` on `experiments/v5/runs/partC5b/records.jsonl`: callbacks
  14-27 (as stated), but `frozen-cap32` reached its cap of $32n$ cuts on three instances
  (n10_s8: 320, n40_s8: 1,280, n80_s8: 2,560 cuts; `budget_exhausted` true), so separation did not
  end by itself there. Root bounds with $32n$ and $64n$ differ by at most $3.8\cdot10^{-5}$
  (remainder directions) and not at all (whole-row directions). With $64n$ no run reached the cap.
- **Fix.** "With larger cut caps and up to 40 callbacks (Part~5C-b), separation ended by itself
  after 14 to 27 callbacks with the cap of $64n$, with about 26 to 30 cuts per block, and the root
  bound came within $8\cdot10^{-4}$ of the block closure on every instance; with $32n$ the
  remainder-direction runs reached the cap on three instances, and the root bounds differed from
  those with $64n$ by at most $4\cdot10^{-5}$."

### N6 [minor] Table 6 header still says "Campaigns 2--4"

- **Location.** A-instances.tex:18 (Table 6, p. 56).
- **Issue.** Campaign 5 used the same separator limits (Table 7 lists its modes), so the column
  header is out of date.
- **Fix.** "Campaigns 2--5 (original variables)", and add a row "Star blocks & --- & campaign 5
  only: center plus up to 16 leaves, star oracle".

### N7 [suggestion] Report how often the global-solve constants were strictly invalid

- **Location.** 08b-validity.tex:78-87 and Table 2 (pp. 26-27).
- **Evidence.** `evidence/ablation-global-solve.md`, "Key counts": Gurobi's bound (U3) exceeded the
  exact support value for 2,311 of the 5,116 MINLPLib cuts (45%) and for 40 of the 1,000 path cuts,
  in all but the four `nvs02` records by at most $2.2\cdot10^{-16}$ (MINLPLib) and
  $5.5\cdot10^{-8}$ (path). Table 2 counts only "materially" wrong constants (excess above
  $10^{-6}\max\{1,|\text{value}|\}$).
- **Fix.** After "materially wrong for only one distinct cut" add: "Gurobi's bound exceeded the
  exact support value, by rounding-level amounts, for 45\% of the MINLPLib cuts, so even these
  constants would need a safe correction." This supports the paper's case for certification.

### N8 [minor, archive] Campaign-5 summaries predate the replay

- **Location.** `experiments/v5/results-s5/results.md`, `results-c5a/results.md`,
  `results-c5b/results.md` (each: "Replay: not run yet"), cited by the availability statement as
  "the replay outputs" and "the scripts that produce every table".
- **Fix.** Re-run `summarize_v5.py` after the Part 5S replay so that the archived summaries record
  the replay results.

---

## 5. Overall assessment

**Contribution.** Three contributions, unchanged in kind but sharper than in round 2:

1. *Limits of gluing pair hulls* (Section 3): the 1/128 witness with a separating cut in model
   coordinates; the $\delta^2/2$ dichotomy; the alternation criterion for $\kappa$-moment
   interfaces (correctly credited to the Radon-partition literature); a full gap for every
   $\kappa$; the three-variable representation result via BNW; and, new in this round, the
   observation that from four variables on joint support cuts are strictly stronger than the dense
   first-level relaxation with all McCormick inequalities, by a relative gap of nearly 100% on the
   full-gap instances with five and seven variables. I re-ran `verification/M7_dense_fullgap.py`:
   rational feasible points with values $1.85\cdot10^{-7}$ ($r=2$) and $7.99\cdot10^{-7}$ ($r=3$)
   against the minimum 1/2, and $-0.1221$ on the four-variable path; the $-109/1024$ point of BNW
   Prop. 12 satisfies all RLT inequalities, as BNW state (their p. 44). This turns the round-2
   objection into a positive argument for joint blocks.
2. *Exact support for constrained stars* (Section 4.2): an $O(m_0+(m+k)\log(m+k))$ rational
   algorithm with a matching algebraic-decision-tree lower bound, correctly positioned against
   Del Pia-Khajavirad.
3. *A certified separator in the original variables* (Sections 5-8): Lagrangian aggregation cuts
   with the four-part contract (C1)-(C4), including the stored-row check, translation validation
   of the model import, and fresh-process replay.

**Correctness.** Two rounds of exact checks found no error in any theorem, proposition or example,
and the round-2 math items are all resolved. The round-2 numbers lens reproduced every table cell
of campaigns 3-4; the campaign-5 numbers I spot-checked agree with the records (Table 5 medians,
4,650 star-oracle calls at 7.8 ms, 5C-b callbacks and cuts per block, campaign-5 load). The one
open correctness item is procedural: the replay claim must wait for the Part 5S replay (O1).

**Presentation.** Clear, plain and consistent. Terminology (glued pair relaxation, block closure,
remainder and whole-row directions, base and wide limits, SCIP-nolocks and SCIP-extra) is now
defined once and used throughout, and the attribution paragraph of Section 8.5 is easy to follow.
The main weakness is length (O2): 67 pages with 130 references, and the computational outcome
repeated four times.

**Evidence.** Validity evidence is strong within the stated trusted base, though 98% of the replayed
records come from two constructed generators (O6(a)). The certificate ablation is now complete:
samples, local minimization and a numerical global solve, and the global solve's one material error
(a slope inside Gurobi's optimality tolerance on `nvs02`) is a convincing example of why a fixed
safety shift is not enough. Usefulness evidence is narrow and honestly reported: neutral on
MINLPLib, SCIP's own disabled separators stronger there, a clear root-bound advantage on the
constructed path and star families, but SCIP-nolocks was as successful and faster on the
binding-row variant and Gurobi solved more star instances.

**Honesty about limitations.** Good in the body: post hoc versus prospective is labeled
everywhere, the pre-diagnostic hand tests and pilot are disclosed, campaign 5 reports its negative
results, the load spike and the out-of-protocol rerun are reported without changing the counts,
and the convex reformulation and the Shapley-Folkman reason for the tight block closure are stated.
The abstract is the one place where the reporting is selective (O4).

**Recommendation for JOGO: minor revision, conditional on O1** (the Part 5S replay must finish and pass before the replay statements can stand). If the Part 5S replay passes and the
replay statements are updated accordingly, the remaining scientific items are wording fixes. The
editor should still require a substantial shortening (O2); if the editor does not enforce length,
the paper is acceptable after the minor changes below.

**Remaining weaknesses a referee would require before acceptance:**

1. O1: finish the Part 5S replay and make the replay statements match the replay outputs (or
   restrict them to the replayed parts).
2. O2: shorten the paper to about 28 pages of main text, or split it.
3. O3: authors, declarations, archive DOI and licence, MINLPLib terms.
4. O4: an abstract that states the post hoc selection and the two unfavorable comparisons.
5. O5: do not attribute the in-solver star results, or their low cost, to Theorem 4.4.
6. N4, N5 and O6(a)-(f): short wording fixes in Sections 1, 8.2, 8.5, 8.7, 9 and Figure 2.

---

## 6. Checks run (targeted, local)

No SCIP or Gurobi solve was run, no project-wide tests were run, and CI was not consulted. Scripts
ran with `/workspace/minlp-notes/code/minlp_solver_lab/.venv/bin/python` and
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`.

- `diff -rq development/draft-round3/sections sections`, `diff -rq` of figures, `cmp` of
  `main.pdf` and `references.bib`: identical.
- `verification/R10_referee_closure.py` (new): page layout (67 pages; references from p. 36,
  appendices from p. 45), 130 cited references and 2 uncited entries, abstract 248 words, campaign-5
  cut counts and replay status per part, 5C-b callbacks, cap hits and cap-32/64 root differences,
  campaign-5 load.
- `verification/M7_dense_fullgap.py` (re-run): values quoted in Section 5.
- BNW full text and PDF (`literature/papers/burer2025-on-the-semidefinite-representability-of/`):
  Prop. 12 point $-109/1024$ and its RLT feasibility.
- Read `experiments/v5/results-{s5,c5a,c5b}/results.md`, `campaign-v5-protocol.md`,
  `experiments/v5/README.md`, `runs/replay-part*.log`, `runs/partC5{a,b}/replay.json`,
  `runs/launch-rerun-spike.log`, `evidence/ablation-global-solve.md`.
- Inline read-only probes of `runs/partS5/records.jsonl` and `runs/partC5b/records.jsonl` (cut
  counts, separation counters, root bounds, load readings) and a citation inventory of
  `sections/*.tex` against `references.bib`.
- `pdftoppm` renderings of pp. 8 and 21 in a `mktemp -d` directory (Figures 1 and 2).
- A bounded wait for the Part 5S replay: I polled `runs/replay-partS5.log` and the replay process from 23:43 to 00:43, every 60 s in a background loop and every 20 s in the final foreground checks. The log stayed empty, and the process was still running when the bound expired.
