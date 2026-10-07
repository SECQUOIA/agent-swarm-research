# Numbers consistency check, revision 1 (main paper and supplement, 2026-10-04)

Scope: every `.tex` file in `paper-open-minlplib/sections/` (main text: 00–11, A, G; supplement:
B0–B9, C, D, E, F, H, I, J) and `paper-open-minlplib/tables/`. Reference: `data/numbers.json`,
the dossiers and critiques, the adopted reviews, the decision register and, where a number is not
in `numbers.json`, its raw source (`R/` = `research-20260929/`, read only). No `.tex` file was edited.

## Method and commands

- Read every section and table file in full.
- `/tmp/nc_r1/scan.py`: extracted every decimal with 6 or more fractional digits from all section
  and table files and classified it against the exact certified ends `L`, `U` of every instance in
  `numbers.json` (safe as dual, safe as primal, or strictly between the ends). All 50 hits that
  lie strictly between the ends were read in context (results below).
- `/tmp/nc_r1/derived.py`: recomputed in exact rational arithmetic the `waterno2` gaps and
  factors, the exact fractions of `tab:waterno2-values`, the `ann_cumene_tanh` bound and gaps,
  the `hvycrash` constant κ and `50·fl(4.37e-3) − 0.2185`, the `pricing050` value μᵀr, the
  `etamac` degree excess under readings (b) and (c), the `lnts` angle-bound excess, the
  `catmix` coefficient excesses, `fl(0.7)^3 − fl(0.343)`, and the `dtoc5` location bound.
- Inline scripts: footnote (b) marks of `tab:closures`; SHA-256 prefixes in `tab:sem-hashes` and
  in the certificate boxes against `numbers.json`; sizes in `tab:closures`; per-solver bound counts
  of `tab:audit-classes` against `R/bound-audit/pages.json`; one-hour run values against
  `R/publication/solver-runs/results_table.csv`; replay times against
  `R/publication/integration/runtime-evidence-r1.json`; reading-(c) audit changes against
  `development/data-semantics-checks/logs/`.
- Grepped for the strings of outline section 8 and for the decision items (KAN wording,
  "independent", "first", band theory).
- Every count of the task was recomputed where it appears (closures, exact optima, formerly
  tolerance-only, audit pairs, campaign runs and duals, funnel).

## Result in brief

No certified bound, primal value or gap cell in the text or tables differs from `numbers.json`,
and every one is on the safe side; all 18 items of `numbers-check.md` are resolved. The headline
counts agree everywhere they appear: 31 closures; 9 exact optima; 13 formerly tolerance-only
closures; 19 bounds on 15 instances (15 distinct conflicts; 11 gross, 8 tolerance-scale); 22
bounds on 18 instances with `rocket`; 129 kept runs, 109 finite duals (35 + 36 + 38; 91 + 18),
0 accepted closures, 5 improvements; funnel 1,633 / 1,257 / 596 / 360 / 294 / 155 with
29 + 12 + 2 and 361 / 295 for `fct`.

Two problems are of medium severity: one wrong number in Appendix A (a margin claim that
fails for `rocket100`) and one claim for reading (c) in Remark 2.3(3) that the rest of the paper
disowns. The other 15 items are low.

## Problems

### Medium

**1. Margin claim under binary64 data fails for `rocket100`.**
- Where: `sections/A-semantics.tex:94`.
- Wrong text: "and every margin still exceeds $1.11$ display units $\dunit{\sigma}$ of the listed bound".
- Correct text: "every class (i) margin still exceeds $1.11$ display units $\dunit{\sigma}$ of the
  listed bound, and the \inst{rocket} margins stay at 1.06, 4.70 and 18.9 units" (or: "every
  margin still exceeds one display unit; the smallest is 1.06 units, on \inst{rocket100}").
- Source: the sentence covers "the 19 refuted listed bounds and the three refuted rocket bounds"
  (line 93); `sections/E-audit.tex:567` ("the rocket margins are again 1.06, 4.70 and 18.9
  display units"); `tab:audit-rocket` (`E-audit.tex:505`); `numbers.json` `audit.rocket`;
  `development/data-semantics-checks/logs/summarize_b64.log` (rocket100: 1.069 units).

**2. Claim for reading (c) in Remark 2.3(3).**
- Where: `sections/02-semantics.tex:53`.
- Wrong text: "whereas the audit refutations survive binary64 data (computed, one implementation; \cref{app:semantics-binary64})."
- Correct text: "whereas the audit's existence certificates also succeed with binary64 data
  (computed with one implementation; not a claim of the paper; \cref{app:semantics-binary64})."
- Source: outline section 8, item 2 ("Any claim for reading (c)"); the paper itself says
  "we do not claim it" (`A-semantics.tex:95`), "not a claim of the paper" (`E-audit.tex:568`),
  "The corollary does not cover the binary64 data" (`07-audit.tex:67`) and "we do not claim the
  audit refutations for the binary64 models" (`11-conclusion.tex:60`).

### Low

**3. Generated audit table understates the exact proofs of `sssd20-04persp`.**
- Where: `tables/tab-audit-pairs.tex:23` (generated from `numbers.json`
  `audit.pairs[sssd20-04persp].second = "Krawczyk"` by `data/make_tables.py`).
- Wrong text: "\inst{sssd20-04persp}\textsuperscript{S} & LINDO & … & B/K".
- Correct text: "B/K,E" (or "B/E"), and the caption's list of second methods accordingly.
- Source: `tab:audit-second` (`E-audit.tex:295`: "V1, Krawczyk; V2, exact"); the counts
  "Twelve of the 19 refutations have a proof in exact rational arithmetic" (`07-audit.tex:76`)
  and "The 12 refutations with exact proofs" (`E-audit.tex:319`) include `sssd20-04persp`
  (its name is absent from the seven Krawczyk-only pairs, `07-audit.tex:77`);
  `development/dossiers/audit.md:584,753`. As printed, the table gives 11 exact and 8
  Krawczyk-only pairs.

**4. Rocket refutations stated without their hypothesis.**
- Where: `sections/07-audit.tex:118-119`; `sections/01-introduction.tex:106`.
- Wrong text (07): "prove these bounds invalid by at least $1.06\cdot10^{-7}$, … or 1.06, 4.70 and
  18.9 display units"; "With \inst{rocket}, 22 per-solver bounds on 18 instances are proved
  invalid". Wrong text (01): "… on \inst{rocket100}, \inst{rocket200} and \inst{rocket400}, are invalid too."
- Correct text (07): "prove these bounds invalid under Hypothesis~H by at least …; the
  \inst{rocket100} margin, 1.06 units, is below the $\tfrac{10}{9}$ units that also cover
  repeated roundings (\cref{lem:audit-display}(a)), so it rests on Hypothesis~H itself"; and
  "… 22 per-solver bounds on 18 instances are proved invalid under Hypothesis~H". (01): "are
  invalid under the same hypothesis".
- Source: `07-audit.tex:55-56` states the $\tfrac{10}{9}$ margin only for the 19 class (i)
  bounds; `development/dossiers/audit.md:335-338` ("rocket100 (1.069 units) is covered by
  Lemma 1(a), (b), and (c) when the last step rounds to nearest"); `numbers.json` `audit.rocket`.

**5. Figure 1 caption: the one-hour dual bounds of `hvycrash` are not all −2.185e8.**
- Where: `sections/03-results.tex:42`.
- Wrong text: "The listed and one-hour dual bounds of \inst{hvycrash} are $-\sci{2.185}{8}$."
- Correct text: "The listed dual bound and the best one-hour dual bound (SCIP) of
  \inst{hvycrash} are $-\sci{2.185}{8}$; GUROBI's is about $-\sci{2.14}{9}$."
- Source: `R/publication/solver-runs/results_table.csv` (hvycrash GUROBI dual −2141300000,
  SCIP −218500000); `tab:campaign-runs` (`tables/tab-campaign-runs.tex:43`: GUROBI $9.7\cdot10^{9}$,
  SCIP $9.9\cdot10^{8}$).

**6. `ann_cumene_tanh`: the forward rows do not determine all other variables.**
- Where: `sections/05-other.tex:339`.
- Wrong text: "Five inputs … determine all other variables through 529 linear rows and 250 rows $x_v=\tanh(x_s)$, after an elimination without division".
- Correct text: "Five inputs … determine 779 of the other variables through 529 linear rows and
  250 rows $x_v=\tanh(x_s)$; the objective follows through an elimination without division".
- Source: 529 + 250 = 779 of the 789 non-input variables; `B9-ann-kan.tex:19-22` ("They
  determine 779 variables …; the remaining ten variables are free except objvar"), `:46`
  ($\Omega$ drops the solvability of the product rows).

**7. "Optimum" of `eg_int_s` where only our point is meant.**
- Where: `sections/05-other.tex:312`; `sections/B7-eg.tex:317` (caption of `fig:eg-enclosures`).
- Wrong text: "at the \inst{eg_int_s} optimum the active objective row has …"; "(b) Cancellation at the \inst{eg_int_s} optimum".
- Correct text: "at our best point of \inst{eg_int_s} …"; "(b) Cancellation at our best point of \inst{eg_int_s}".
- Source: outline section 8, item 5 ("An exact optimum" for eg); `B7-eg.tex:66` ("At our
  point for \inst{eg_int_s}"); the optimum is only enclosed (gap $6.46\cdot10^{-9}$).

**8. Section 8 calls the deficit bound the largest deficit.**
- Where: `sections/08-solvers.tex:26`.
- Wrong text: "their deficits are about 87\% of the largest deficits that such violations allow".
- Correct text: "their deficits are about 87\% of the proved upper bound $D_n(\varepsilon)$ for such violations".
- Source: `05-other.tex:88` ("$D_n$ is a proved upper bound, not the worst case");
  `B3-camshape.tex:221`.

**9. Section 11 states the deficit growth as fact and drops a qualifier.**
- Where: `sections/11-conclusion.tex:22`.
- Wrong text: "the amount by which a tolerance-feasible point can fall below the optimum grows like $n^2\varepsilon$, and explicit points reach about 87\% of this limit".
- Correct text: "the amount by which a point with violations $\varepsilon\le10^{-8}$ can fall below
  the optimum is at most about $0.6\,n^2\varepsilon$ (proved), and explicit points reach about
  87\% of this bound (numerical evidence)".
- Source: `prop:camshape-deficit` (`05-other.tex:84,88`); `tab:camshape-deficit`
  (`B3-camshape.tex:233-238`).

**10. Published SCIP 8.1 dual for `eg_int_s` quoted without its one-decimal printing.**
- Where: `sections/B7-eg.tex:74`.
- Wrong text: "the floating-point closure of \inst{eg_int_s} by SCIP~8.1, with primal and dual value 6.5 after 9{,}085.1~s".
- Correct text: "… by SCIP~8.1, with primal and dual values printed to one decimal as 6.5, after 9{,}085.1~s".
- Source: `development/dossiers/eg.critique.md:171` (Table 17 prints "6.5 | 6.5");
  `D-literature.tex:178`. Read literally, a dual bound 6.5 exceeds $\Uprim=6.4531031593842275$
  and would be refuted by our point.

**11. Abstract: verification claim without its exceptions.**
- Where: `sections/00-abstract.tex:11`.
- Wrong text: "separately written code rechecks them, sometimes for a slightly weaker bound."
- Correct text: "separately written code rechecks them, with named exceptions and sometimes for a slightly weaker bound."
- Source: `01-introduction.tex:51` ("apart from named exceptions"); `02-semantics.tex:177-179`
  (shared mpmath, KAN exponential, interval core and reader; the second `ann_cumene_tanh` code's
  author read the first).

**12. Range of earlier violations rounded down at its upper end.**
- Where: `sections/01-introduction.tex:85`; `sections/06-points.tex:70`; `tables/tab-points.tex:20`
  (generated).
- Wrong text: "violate rows by \sci{2.4}{-20} to \sci{7.9}{-12}"; table cell
  "$2.1\cdot10^{-13}$ / $1.2\cdot10^{-12}$ / $7.9\cdot10^{-12}$".
- Correct text: "… to \sci{7.91}{-12}"; table cell "$2.13\cdot10^{-13}$ / $1.18\cdot10^{-12}$ /
  $7.91\cdot10^{-12}$" (in `make_tables.py`).
- Source: `B6-powerflow.tex:65` (50-digit evaluation: $2.13\cdot10^{-13}$, $1.18\cdot10^{-12}$,
  $7.91\cdot10^{-12}$). These are measured violations, not bounds, so the risk is presentational.

**13. Wrong table for the count of 37 points.**
- Where: `sections/11-conclusion.tex:24`.
- Wrong text: "the archive holds such points for 37 of our 43 instances (\cref{tab:points})".
- Correct text: "… (\cref{tab:points-all})".
- Source: `tab:points` lists only the 13 formerly tolerance-only closures; `tab:points-all`
  lists all 43 (31 + 5 + 1 exactly feasible points, 6 KAN points of $\RP$).

**14. Generated campaign table uses $R$ for the KAN relaxation.**
- Where: `tables/tab-solvers.tex:19` (generated by `data/make_tables.py`).
- Wrong text: "\quad compared with $R$ (KAN)".
- Correct text: "\quad compared with $\Rnet$ (KAN)".
- Source: `macros.tex` (`\Rnet`); every other table and the text use `\Rnet`
  (`tab-campaign-runs.tex:7`, `tab-claims-campaign.tex:9`, `08-solvers.tex:130`).

**15. Memory of the host given in two units.**
- Where: `sections/H-solvers.tex:20` ("about 47\,GB of memory") against
  `sections/10-reproducibility.tex:74` ("47\,GiB of memory").
- Correct text (H): "about 47\,GiB of memory" (47 GiB is about 50.5 GB).
- Source: `R/publication/integration/environment-r1.json` (`mem_total_gib_exact` 47.04).

**16. Replay times quoted from different runs without saying so (known).**
- `optcdeg2` point: "1.5~s" (`04-split.tex:311`) against "about 2\,s" (`B2-dtoc5-optcdeg2.tex:344`);
  bound: "16--18~s" (`04-split.tex:311`) against "about 5\,s for the enclosure and 17\,s"
  (`B2-dtoc5-optcdeg2.tex:308`) and "about 20\,s; 8\,s" (`I-reproduction.tex:153`).
- `chain` verifier: "up to 195\,s" (`10-reproducibility.tex:58`, `I-reproduction.tex:163`)
  against 50–154 s in `tab:chain-bnb` (`B4-chain-catmix.tex:253-256`).
- Correct text: name the run in each place, or use the claim-register run throughout.
- Source: `development/integration-notes-r1.md`, section 8, item 7 (open lead-author decision);
  `R/publication/integration/runtime-evidence-r1.json`.

**17. (Optional) Example list of displays below our duals omits `ex6_2_7`.**
- Where: `sections/02-semantics.tex:129`.
- Text: "which can fall below our dual bounds by rounding alone (as for \inst{lnts100}, \inst{lnts400}, \inst{lukvle10} and \inst{chain50}--\inst{chain200})".
- Note: the best listed point display of `ex6_2_7`, $-0.16084762$ (`B5-small.tex:13`;
  `numbers.json`), also lies $4.5\cdot10^{-9}$ below $\Lcert=-0.16084761546364905$. The list is
  given as examples, so it is not wrong; add `ex6_2_7` or write "for example". No source
  evaluates the objective of that point.

## Known open decision (not counted)

Claims for reading (c) beyond outline section 8, item 2: the `waterno2` points are stated to be
infeasible under binary64 data (`02-semantics.tex:51`, `06-points.tex:85`, `A-semantics.tex:82`,
`B8-waterno2.tex:54`, `11-conclusion.tex:60`), and the `lnts` and `lukvle10` points to remain
feasible (`02-semantics.tex:50`, `06-points.tex:86`, `A-semantics.tex:83`). The statements are
consistent with each other and with S1.8 and register WN-07; `integration-notes-r1.md`, section 8,
item 2, leaves the conflict with the outline to the lead author.

## Checked and consistent (no action)

- Long decimals: of 417 matches against certified ends, all dual displays lie at or below $\Lcert$
  and all primal displays at or above $\Uprim$ (reversed for `pricing050`). The 50 values strictly
  between the ends are, in context, intended: cross-instance matches (`powerflow0039p` against
  `0039r`); truncated exact values marked "…" (`B1:294,304`, `B2:325`, `B6:219`, `B7:367-368`);
  enclosure ends (`B5:175-176`); higher valid bounds (`B6:271`, `tab:kan-rerun`, `B9:130`);
  listed or solver values (`B6:66`, `tab-kan.tex:20`); and the unsafe strings of `tab:displays-unsafe`.
- Gap statements: every $\gapabs$ and $\gaprel$ in text and tables equals `numbers.json` and is
  rounded up (including $7.21\cdot10^{-43}$, $8.98\cdot10^{-16}$, $1.42\cdot10^{-9}$,
  $1.70\cdot10^{-29}$, $9.997\cdot10^{-10}$ for `eg`, 0.195\% and 0.194\% for `ann_cumene_tanh`,
  the five `waterno2` gaps 1.68/10.82/6.90/4.87/5.90\% and the steps 7.27\% and 3.78\%).
  Footnote (b) of `tab:closures` is set exactly where the printed displays differ by more than
  the gap cell; `tab:kan` explains its one such case (`kan_r5_h1_n3`) in the caption.
- Factors and margins, rounded down: `waterno2` 1.68/3.01/4.35/6.21/6.00; CAMINO 0.2445944,
  0.4312902, 5.2010558 and 4.33/7.48/80.5\% (4.3/7.4/80\% in Section 1); BARON
  $5.25\cdot10^{-7}$, $2.05\cdot10^{-6}$ and $1.23\cdot10^{-7}$, $4.80\cdot10^{-7}$ (up);
  KAN $1.70\cdot10^{-3}$, $2.03\cdot10^{-3}$ and `tab:kan-rerun`; QPLIB $3.162\cdot10^{-3}$,
  $1.552\cdot10^{-4}$; all rows of `tab:claims` and `tab:claims-campaign`; `emfl` shortfalls and
  $1.166\cdot10^{-6}$, $1.36\cdot10^{-6}$ relative; rocket $1.06\cdot10^{-7}$, $4.70\cdot10^{-8}$,
  $1.89\cdot10^{-7}$; `spring` $1.5\cdot10^{-6}$; topopt 4.48; glider "about 784"; `waterno2`
  primal improvements 8.58/29.53/245.65/368.92; KAN 0.558/$7.1\cdot10^{-5}$/0.291.
- Counts: classes A 15, A$'$ 4, B 3, C 5, D 1, E 3; branching 12/6/7/2 plus `pindyck` (9 and 6
  boxes) and `eg`; 10 closures at level S; 11 closures with $\gaprel\le3.00\cdot10^{-13}$; 12 of 31
  with the listed dual more than $|\Uprim|/2$ below; prior codes 4 F + 3 f, 2 Lst + 3 T + 1 K +
  2 U, 16 N; `tab:audit-classes` row and column sums and per-solver bounds (pages.json, 19 labels,
  other nine 358 + 316 + 43 + 48); 63 repairs on 11 and 25 undecided on 12 instances; 3,851 ties on
  1,133 instances; `tab:solvers` and every mark of `tab:campaign-runs` (b 4/3/3, t 6, M 3, C 8 + 1,
  g 6, finite duals 35/36/38); 36 returned values = 30 + 5 + 1; 15 instrumented and 78/122 runs;
  `eg` leaves 33,385 + 86,796 + 1,114,361 = 1,234,542, pieces, exponentials (pieces × 28 × 97 × 4)
  and powers summing to 63,017,129,222, times summing to 16,703 s; `ann` regions
  212,092 + 66,403 + 899,981 + 465,634 + 208,223 = 1,852,333; `waterno2` cell pairs 117,736 =
  79,919 + 37,817, records 33,899 + 15,416, 63 + 6 = 69 periods; `powerflow` rows
  164 + 82 + 56 + 30 = 332 and point systems summing to 555/657/473; KAN edges and binaries.
- Derived numbers recomputed exactly: κ = 81381972927/12500000000000; $50\fl(4.37\cdot10^{-3})-0.2185\approx-1.24\cdot10^{-17}$;
  μᵀr = −4535.6010320496854734372 and the `pricing050` bound; `etamac` $s-1=4.14\cdot10^{-16}$
  (b) and $3.7\cdot10^{-16}$ (c); $\bar\theta-\pi/2=3.38\cdot10^{-15}$ (b), $3.49\cdot10^{-15}$ (c);
  `catmix` $c-9a$ = 5, 3, 1, $1\cdot10^{-18}$; $\fl(0.7)^3-\fl(0.343)=-9.237\cdot10^{-17}$;
  the five exact `waterno2` fractions; $L^*=-7447080719734483\cdot2^{-41}$; the `dtoc5` deviation
  $1.899\cdot10^{-19}$; $u_{3091}\approx0.041823$; `lnts50` p1 margin $4.303\cdot10^{-11}$; the
  `camshape` copy shifts and listed gaps; the reading-(c) audit changes $2.128\cdot10^{-10}$,
  $2.848\cdot10^{-11}$, $1.033\cdot10^{-12}$ (displayed rounded up).
- Hashes and sizes: the 43 prefixes of `tab:sem-hashes` and the certificate-box prefixes of
  Sections 4, 5, S1.7 and S1.9 match `numbers.json`; `tab:closures` sizes match the OSIL files;
  97 of the 116 `pindyck` variables lack `lb`, and `pricing050` has 46 objective coefficients.
- Decisions: "the six KAN instances in/of our set" everywhere, "ten" and "four further" KAN
  instances in MINLPLib; no "independent review"; no band theory; no hard-coded reference numbers
  in generated tables; `tab:trust` camshape row and AI sentence fixed; the `eg` trust wording
  matches `reviews/sol-eg-audit.md`. Strings of outline section 8, item 11 occur only in
  `tab:displays-unsafe`. The `waterno2` comparison with Huang's 2019 values (`D-literature.tex:191`)
  follows register WN-06.
