# Review round 2, lens "numbers and claims from data"

Written 2026-10-03. Manuscript: `main.tex` and `sections/*.tex` as compiled in
`main.pdf` (text in `development/draft-round2/main.txt`; the sections in
`development/draft-round2/sections/` are identical to `sections/`). Page
numbers are the printed PDF pages. Nothing under `experiments/`, `evidence/`
(except this file) or the manuscript was changed. No SCIP or Gurobi solve was
started.

## What was run (targeted checks only; no project-wide tests, no CI)

All with `/workspace/minlp-notes/code/minlp_solver_lab/.venv/bin/python`
and `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`, from
`verification/`:

| Command | Purpose | Result |
|---|---|---|
| `R9_numbers_recompute.py` | replay totals, Table 3, root runs A/B/B2, Table 4 funnel, Table 5 medians and solved counts, C3/C4 text, 19/22/11, loads, primal checks | ran in 5 min 9 s; output used below |
| `R9_numbers_tables.py` | every cell of Tables 7, 8, 9 (Part D), 11, 12 (`sections/B-tables.tex`) against the raw records, plus distinct cuts, native separators, seed variation | 140 rows checked, **0 mismatches** (5 min 6 s) |
| `R9_numbers_spot.py` (new, this review) | independent recomputation of the headline numbers (it imports no other R9 script and no producer code) and of claims the two scripts above do not cover: borderline Table 5 cells, native separators, Part B2 closure, Part D cut models, Gurobi gaps, loads, campaigns 1 and 2 (App. F) at tolerance 1e-4, ablation removal sets | ran in 6 min 31 s |
| `E1_audit_experiments.py` | campaigns 1-2 and repair cohort against Reports A/B | 418/418 pass |

`R9_numbers_recompute.py` and `R9_numbers_tables.py` were already present
(written earlier on 2026-10-03 for this lens). I read their definitions
(solved, time, root bound, gap closed, SGM, bound tolerance) against Section
8.1 before using their output. Short read-only Python snippets were also run
for: the Part B/D selection counts (`v3/scan`, `v4/scanD`), stored-row
rejection causes per part, the separator configuration per mode, the
campaign-2 "10% slower" count, node counts of the whole-row wide runs, the
flagged `waternd2` record, Part D `all-diag-rowdir`, the per-mode tamper
controls in every `replay.json`, and the C4 reference file.

## Verdict

Almost every number in the abstract, Section 1, Section 8, Section 9,
Appendix F, Appendix G and the appendix tables matches the raw records. All
140 rows of the per-model and per-instance tables match cell by cell. The
headline numbers are reproduced: 143,267 replayed cuts (7,498 + 30,998 +
104,771); 19, 22 and 11 solved by SCIP, SCIP with its disabled separators and
Gurobi on the 40 fresh instances, against 40 for `rowdir-wide`; minimum root
gap closed 0.9739 ("at least 97%"); Tables 2, 3 and 4; the ablation counts;
and the time ratios. The problems are of four kinds:

1. Two conclusion-level statements go beyond the data. The "only if
   whole-row directions" conclusion (Section 1, Section 9) is contradicted by
   the remainder-direction runs. The "38% / nearly all" error rate is
   attributed to "samples or a local solver", but it holds only for samples.
2. The headline count of 143,267 replayed cuts counts every path-family cut
   twice, because root and full runs record identical cut lists. Only 59,220
   exported rows are distinct.
3. Several numbers mix run sets or are rounded wrongly: two Table 5 medians,
   the Gurobi gap range, "12 of them at the root node", "21 of the 25", the
   load ranges, and the order of "3.2 and 3.5".
4. A few general words ("no SCIP setting", "rarely", "already contained",
   "needed about 16") are stronger than the data.

## Findings

### F1 (major). "Only if ... whole-row directions first" is contradicted by the remainder-direction runs

- **Location.**
  - `sections/01b-results.tex:14-17` (p. 3): "A post hoc diagnostic,
    confirmed by a later prospective control, showed that the separator
    closes the gap beyond that level only if it may add enough cuts per
    block and tries the exact support of each whole row first."
  - `sections/09-conclusions.tex:30-33` (p. 32): "They did so only with the
    exact support of each whole row as a first direction, enough cuts per
    block, and, when a coupling row binds, a direction search that finds
    sloped cuts."
  - `sections/08e-path.tex:126-127` (p. 29): "the whole-row directions for
    the part beyond the pair-hull level."
- **Evidence.**
  - The prospective control (C2, `frozen-wide`: remainder directions, wide
    limits) went above the pair-hull level on 7 of the 20 instances. These
    are n10_s0, n10_s4, n20_s2, n20_s3, n20_s4, n80_s1 and n80_s4 (root bound
    > 0; `R9_numbers_recompute.py`, block 5). It closed a median of 86-90%
    and solved 13 instances. The manuscript says so itself
    (`08e-path.tex:121-122`, "above it on 7 of the 20 instances").
  - With a binding coupling row (C4), the remainder-direction mode
    `frozen-wide` solved **20/20** instances. Its median closure was 95%
    (range 0.875-0.9993), and 99.9% of its cuts came from the LP direction
    search (Table 5; `campaign4-c4-digest.md` (f)). So the whole-row first
    direction is not necessary in C4.
  - What the data support: on the non-binding family, **closing the whole
    gap and solving all instances** required both the whole-row direction
    and the wide limits.
- **Fix.**
  - 01b: "... showed that the separator closes the whole gap only if it may
    add enough cuts per block and tries the exact support of each whole row
    first; with enough cuts but remainder directions it reached about the
    pair-hull level (median 86-90% of the gap) and solved 13 of 20 instances."
  - Section 9: "On the family with a non-binding coupling row they did so
    only with the exact support of each whole row as a first direction and
    enough cuts per block. With a binding coupling row, both first-direction
    rules solved every instance, and the cuts that mattered came from the LP
    direction search."
  - 08e:126-127: "... the limits account for most of the closure, and the
    whole-row directions for the remaining 10-14% of the gap."

### F2 (major). The "38% / nearly all" error rate is attributed to "samples or a local solver", but it holds only for samples

- **Location.**
  - `sections/01b-results.tex:5-8` (p. 3): "Constants computed without a
    certificate, from samples or from a local solver, would have been wrong
    for 38% of the cuts on MINLPLib models and for nearly all cuts on the
    path family".
  - Repeated in weaker form at `sections/08g-summary.tex:195-197` (p. 31):
    "on seven MINLPLib models and on 58 of the 60 sampled path-family
    instances".
  - And at `sections/09-conclusions.tex:18-20` (p. 32): "constants taken
    from samples or from a local solver were wrong for a large share of the
    cuts".
- **Evidence.** Table 2 and `ablation-final-summary.md`, reproduced by
  `ablation-verify.md` (A2, A3):
  - The sample minimum (U1) was wrong for 1,969/5,116 = 38.5% of the cuts
    and for 976/1,000 sampled path cuts. Its rows removed feasible points on
    7 models and 58 instances.
  - With SLSQP (U2), it was wrong for 230/5,116 = **4.5%** and 73/1,000 =
    **7.3%**. Its rows removed feasible points on **2** models and **19**
    instances.
  - Readers of Section 1 will take 38% as the error rate of a local solver.
- **Fix.**
  - 01b: "Constants taken from the separator's own samples would have been
    wrong for 38% of the cuts on MINLPLib models and for nearly all sampled
    cuts on the path family; local minimization from the best samples
    reduced this to 4.5% and 7.3%, but still left rows that cut off feasible
    solutions, on the path family including known optima."
  - 08g: "constants taken from samples would have cut off feasible points on
    seven MINLPLib models and on 58 of the 60 sampled path-family instances,
    and constants improved by local minimization still did so on two models
    and 19 instances."
  - Section 9: "constants taken from samples were wrong for a large share of
    the cuts, and constants improved by a local solver for a few percent of
    them; both would have cut off feasible solutions, including known
    optima".

### F3 (major). The headline 143,267 counts every path-family cut twice; only 59,220 rows are distinct

- **Location.**
  - `sections/00-abstract.tex:15` (p. 1);
  - `sections/01b-results.tex:2-4` (p. 3);
  - `sections/08b-validity.tex:88-90` (p. 23);
  - `sections/08g-summary.tex:194` (p. 31);
  - Table 2 caption, `08b-validity.tex:116-117` ("1,000 of the 138,000
    recorded cuts").
- **Evidence.**
  - In the path family the separator runs only at the root. In every one of
    the 160 root/full pairs of the same instance and mode (v3 partC 20, v3d
    40, C2 20, C3 40, C4 40), the full run recorded **the same cut list** as
    the root run (`R9_numbers_recompute.py`, block 1). So the 138,000
    path-family records are 69,000 cut lists recorded twice.
  - Counting distinct exported rows over all 143,267 records, keyed by
    model SHA-256, binary64 coefficients and right-hand side, gives
    **59,220**: 57,499 path-family and 1,721 MINLPLib
    (`R9_numbers_spot.py`, block H). `R9_numbers_tables.py`, which keys by
    the exact rational row and variables, gives 59,315.
  - The number is literally correct ("recorded cuts"). But the abstract uses
    it as evidence of validity at scale, and a referee will ask how many
    distinct rows were checked. Replay is also a re-execution of the
    generator's code, not an independent checker (`06-certification.tex:
    135-139`), so repeated records add little evidence.
- **Fix.** Keep 143,267 but add the distinct count at first use.
  - Abstract: "In SCIP, all 143,267 recorded cuts (59,220 distinct rows)
    passed replay ...".
  - 08b: "... 143,267 in total, or 59,220 distinct rows; in the path family
    the root and full runs record the same cuts, so each path-family cut
    appears twice."
  - Table 2 caption: "a random sample of 1,000 of the 138,000 recorded cuts
    (69,000 distinct records; the sample contains 995 distinct cuts)."

### F4 (minor). Two Table 5 medians are rounded wrongly, and the text repeats one of them

- **Location.** `sections/08e-path.tex:62` (Table 5, "glued pair hulls",
  seeds 0-4, n=40), `08e-path.tex:72` ("remainder, mech.", seeds 5-9, n=80),
  `08e-path.tex:139` ("closed 21--32% of the root gap"); p. 29-30.
- **Evidence.** Full-precision medians (`R9_numbers_spot.py`, block T5):
  - Seeds 0-4, n=40, bound 0: the closures are 0.906391, 0.912893,
    **0.934931**, 0.940345 and 0.941826. The median is 0.9349 → **0.93**;
    the table shows 0.94.
  - Seeds 5-9, n=80, `all-diag-mech`: the closures are 0.157699, 0.190937,
    **0.204782**, 0.22417 and 0.29462. The median is 0.2048 → **0.20**; the
    table shows 0.21.
  - Both errors come from double rounding of the digest values 0.935 and
    0.205 (`campaign4-digest.md` lines 97 and 213). The per-n medians of the
    remainder mode on seeds 5-9 range over 0.2048-0.3226.
  - The per-instance Table 11/12 values reproduce these medians exactly.
- **Fix.** Table 5: 0.94 → 0.93 (glued pair hulls, n=40, seeds 0-4) and
  0.21 → 0.20 (remainder, mech., n=80, seeds 5-9). Line 139: "closed 20--32%
  of the root gap".

### F5 (minor). "The total time was comparable (median ratio 0.86)" hides two opposite groups

- **Location.** `sections/08e-path.tex:135-136` (p. 30).
- **Evidence.** The per-instance ratios `rowdir-wide`/baseline on the nine
  instances SCIP solved in C3 are 1.86, 3.44, 3.41, 1.84 and 0.86 for n=10,
  and 0.141, 0.091, 0.270 and 0.051 for n=20. The median is 0.860
  (`R9_numbers_spot.py`, block H). On n=10 the cut mode was up to 3.4 times
  slower; on n=20 it was 4 to 20 times faster. "Comparable" describes neither
  group.
- **Fix.** "On the nine instances that SCIP solved, the cut mode was slower
  on four of the five instances with n=10 (by factors up to 3.4, because of
  the separator's fixed cost) and 4 to 20 times faster on the four with
  n=20 (median ratio over the nine 0.86) ...".

### F6 (minor). The Gurobi gap range comes from a different run set than the sentence it is in

- **Location.** `sections/08e-path.tex:98-99` (p. 28), in the paragraph on
  the campaign-3 instances: "Gurobi 13 solved the instances with n=10 and two
  with n=20; on n=40 and n=80 its gap after 300 s was 53 to 121%."
- **Evidence.**
  - "n=10 and two with n=20" matches seeds 0-4 (7 solved).
  - The Gurobi `mip_gap` on n=40 and n=80 is 0.609-1.130 on seeds 0-4. On
    seeds 5-9 it is 0.534-1.214 (`R9_numbers_spot.py`, block G). So "53 to
    121%" is the seeds 5-9 range (or the union of both sets), not the range
    of the instances in the sentence.
- **Fix.** "... on n=40 and n=80 its gap after 300 s was 61 to 113% (53 to
  121% on the fresh instances of campaign 4)."

### F7 (minor). "12 of them at the root node" counts root runs, not the full runs in the same sentence

- **Location.** `sections/08e-path.tex:117-119` (p. 29): "together with the
  wide limits it closed the root gap on all 20 instances, and all 20 were
  solved, 12 of them at the root node."
- **Evidence.**
  - In the root runs (node limit 1) of `all-diag-mech-wide` (v3d), 12 ended
    `optimal` and 8 `nodelimit`. In those 8 the root bound equalled the
    optimum, but no optimal incumbent had been found.
  - In the full runs, which the sentence describes ("all 20 were solved"),
    **18 of 20** finished at one node; the other two needed 2 and 6 nodes
    (`R9_numbers_tables.py`, "v3d wide full runs: nodes").
- **Fix.** "... and all 20 were solved, 18 of them at the root node." Or
  name the run set: "12 of its root runs already proved optimality".

### F8 (minor). "Needed about 16 cuts per block" is not shown; 16 cuts per block was the cap

- **Location.** `sections/08e-path.tex:159-161` (p. 30): "on these instances
  it needed about 16 cuts per block to come close to the block closure".
  Also `sections/09-conclusions.tex:43-44` (p. 32): "the search needed about
  sixteen cuts per block to approach the block closure".
- **Evidence.** Every C4 cut-mode run (40/40 per mode) stopped at the cap of
  16n cuts. No smaller cap was run on C4, so the data do not show that fewer
  cuts would fail. At the cap, the root bound was still 0.016-0.029 below
  bound (ii) for n=80 (`R9_numbers_recompute.py`, block 5; the manuscript's
  own line 152-154).
- **Fix.** 08e: "with 16 cuts per block, the cap, it came within 1.1e-5 to
  0.029 of the block closure". Section 9: "on the binding-coupling family 16
  cuts per block, the cap, did not reach the block closure."

### F9 (minor). "No SCIP setting closed any part of the gap" generalizes from three settings and 20 instances

- **Location.** `sections/08e-path.tex:94-96` (p. 28): "no SCIP setting
  closed any part of the gap between this level and the optimum". Also
  `01b-results.tex:12-14`: "with that step disabled, SCIP reaches the level
  of glued pair relaxations and no further".
- **Evidence.**
  - Three settings were run: default, `checkvarlocks` off and the disabled
    separators. Their combination was not run.
  - `baseline-novarlocks` was run only on seeds 0-4 (20 instances). Its root
    bounds lie between -0.0099 and -0.0009, all below 0
    (`R9_numbers_recompute.py`, block 5).
- **Fix.** "none of the three SCIP settings we ran (default, implicit
  discreteness off, disabled separators on) closed any part of the gap
  between this level and the optimum".

### F10 (minor). "Rarely gets past discovery": it got past on 8 of 20 models

- **Location.** `sections/08c-minlplib.tex:127-129` (p. 27): "On models of
  this size the frozen separator rarely gets past discovery".
- **Evidence.** In mode `all` discovery stopped on 12 of 20 models and
  completed on 8. On 2 of these 8 it added cuts (`kall_ellipsoids_tc02b`,
  11; `kriging_peaks-full100`, 3); on the other 6 it added none
  (`R9_numbers_tables.py`, `R9_numbers_spot.py`, block D).
- **Fix.** "On models of this size the frozen separator stops during
  discovery on most models (12 of 20), and where it gets past discovery its
  cuts are not stronger than SCIP's relaxation."

### F11 (minor). "SCIP's own relaxation already contained what the cuts could add" is too strong

- **Location.** `sections/09-conclusions.tex:46-47` (p. 32).
- **Evidence.**
  - The cuts improved SCIP's **default** root bound on four Part B models
    (`pooling_bental4tp`, `pooling_bental4pq`, `ex3_1_4`, `pointpack04`) and,
    with aggregation disabled, on 6 models of Part B2.
  - On `multiplants_mtg1c` (Part D, max) the `all-diag` root bound 8574 is
    better than both SCIP default (8893) and SCIP with its disabled
    separators (8647) (Table 9).
  - What holds is weaker: the cuts never changed a full solve, and SCIP's
    disabled separators matched or beat the cuts on the Part B models.
- **Fix.** "... and on our MINLPLib samples the cuts improved SCIP's root
  bound on few models and changed no full solve, while SCIP's disabled
  separators achieved as much or more on nearly all of them."

### F12 (minor). Appendix F: "both cut modes were more than 10% slower on 21 of the 25" — 21 holds for each mode, 19 for both

- **Location.** `sections/A-campaigns12.tex:107-108` (p. 49).
- **Evidence.** Time charged to the budget (`total_seconds` +
  `preparation_seconds`) on the 25 commonly solved campaign-2 models:
  - `all` > 1.1 × baseline on 21;
  - `auto` > 1.1 × baseline on 21;
  - both at once on **19**.

  `total_seconds` alone gives the same counts. The other numbers of the
  paragraph reproduce: SGM 0.549 → 0.989 / 0.957 s; callback 27.63 s with
  discovery 24.41, LPs 0.67 and certification 2.36. At tolerance 1e-4 there
  are no better bounds; four time-limited models have worse final bounds
  (`ex5_2_5`, `graphpart_clique-40`, `tln7`, `waterx`), and
  `graphpart_clique-40` has a worse root bound, in both cut modes. There
  were 7 models with cuts (38 cuts) and 3 (10 cuts), 4 of them solved at the
  root. `btest14` gives -72.30 / -115.60. There were 271 + 67 = 338
  incumbents. In the repair cohort, `waterno2_06` gives 76.75 / 81.64 with
  no cut. (`R9_numbers_spot.py`, block F2.)
- **Fix.** "each cut mode was more than 10% slower on 21 of the 25 (both on
  19)".

### F13 (minor). The load ranges in Section 8.1 omit campaign 4's high-load runs and the diagnostic

- **Location.** `sections/08a-setup.tex:31-32` (p. 23): "the one-minute load
  average was 14 to 21 during the timed runs of campaign 3 and about 3 to 8
  during campaign 4."
- **Evidence.** Load at run start (`R9_numbers_spot.py`, block L):

  | Run set | Min | p5 | Median | p95 | Max |
  |---|---:|---:|---:|---:|---:|
  | Campaign 3, prospective | 14.06 | 16.03 | 16.37 | 20.37 | 20.63 |
  | Post hoc 3D | 2.05 | 2.05 | 5.20 | 19.57 | 20.70 |
  | Campaign 4 | 0.76 | 2.36 | 7.07 | 9.04 | 14.85 |

  - The 3D range comes from the A/B root runs at 2-6 and Part C at 14-21.
  - In Part C4, 45 of 180 runs started at a load above 9.
- **Fix.** "... 14 to 21 during the prospective runs of campaign 3 (2 to 21
  during the post hoc diagnostic) and 2 to 9 during campaign 4 (5th to 95th
  percentile; at most 15, in Part C4)."

### F14 (minor). The Table 5 solved counts for seeds 0-4 compare runs from different campaigns and loads

- **Location.** Table 5 (`sections/08e-path.tex:43-82`, p. 29) and the rule
  in `08g-summary.tex:214-216`: "we compare times only within paired runs
  of one campaign".
- **Evidence.** For seeds 0-4:
  - "SCIP default" and "remainder, mech." come from campaign 3, Part C (load
    14.1-16.5).
  - The two whole-row rows come from the post hoc diagnostic (Part C load
    14.1-20.7).
  - "checkvarlocks off", "disabled separators on", Gurobi and "remainder,
    wide" come from campaign 4, Part C2 (load 2.3-7.4).

  "Solved within 300 s" is a time-based outcome, so these counts are not
  paired. The text discusses this only for the four cells of the 2×2
  design. The root-gap columns are unaffected, because every cut-mode root
  run stopped at its cut cap.
- **Fix.** Add to the Table 5 caption: "For seeds 0-4 the rows come from
  campaign 3 (SCIP default, remainder mech.), the post hoc diagnostic
  (whole row) and campaign 4, Part C2 (the others), run under different host
  loads; their solved counts are not paired."

### F15 (minor). The order of "3.2 and 3.5" does not match the order of the modes

- **Location.** `sections/08e-path.tex:146-148` (p. 30): "the cut modes were
  slower by median factors of 3.2 and 3.5". The next sentence lists
  "(remainder directions) and ... (whole-row directions)".
- **Evidence.** The medians on the 10 baseline-solved C4 instances are 3.514
  for `frozen-wide` (remainder) and 3.248 for `rowdir-wide` (whole row)
  (`R9_numbers_recompute.py`, block 5). Read in order, the sentence swaps
  them.
- **Fix.** "slower by median factors of 3.5 (remainder directions) and 3.2
  (whole-row directions)".

### F16 (minor). Appendix G says the other modes raise only the limits in Table 10, but they also raise the callback limit

- **Location.** `sections/A-instances.tex:5-8` (p. 49): "the other modes
  raise only the limits named in Table tab:modes"; Table 10
  (`A-instances.tex:43-69`, p. 51).
- **Evidence.** Every raised mode records `max_rounds` = 10, against 3 for
  `all`/`auto` ("Root callbacks 3" in Table 9). This holds for `all-diag`,
  `all-diag-rowdir`, `all-diag-mech`, `all-diag-mech-wide`, `frozen-wide`
  and `rowdir-wide` (`config` and `config_overrides` in the records). Table
  10 has no callbacks column. The campaign-4 protocol states "10 callbacks"
  for the mechanism and wide limits.
- **Fix.** Add a column "Callbacks" to Table 10: 3 for `all`/`auto`, 10 for
  every other separator mode.

### F17 (minor). The abstract's complexity bound omits the m_0 term

- **Location.** `sections/00-abstract.tex:11-12` (p. 1): "O((m+k)log(m+k))
  operations". Compare `01-introduction.tex:65-66` and Theorem 4.4
  (`04-quadratic.tex:129`): "O(m_0+(m+k)log(m+k))", with m_0 rows in the
  center alone.
- **Fix.** "... with O(m_0+(m+k)log(m+k)) operations, where m_0 rows involve
  the center alone". Or say "in nearly linear time".

### F18 (minor). The abstract omits the strongest SCIP comparator on the fresh instances

- **Location.** `sections/00-abstract.tex:19-21` (p. 1): "... against 19 for
  SCIP and 11 for Gurobi."
- **Evidence.** SCIP with its disabled separators solved 22 of the 40
  (`R9_numbers_spot.py`, block H; Section 1 reports it). Leaving out the
  strongest comparator in the abstract invites a charge of selective
  reporting.
- **Fix.** "... against 19 for SCIP, 22 for SCIP with its disabled
  separators and 11 for Gurobi."

### F19 (suggestion). Appendix F: scope of the "418 checks", and the campaign-1 control value

- **Location.** `sections/A-campaigns12.tex:50-52` and `:80-82` (p. 48).
- **Evidence.**
  - The 418 checks of `E1_audit_experiments.py` test the numbers of the
    earlier Reports A and B. Several Appendix F statements are not among
    them: the comparisons at tolerance 1e-4 (E1 uses 1e-6), the SGMs and
    "21 of the 25". I recomputed them in `R9_numbers_spot.py`. All hold
    except the count in F12.
  - For `waterno2_06` the appendix compares the cut modes (7.05, 2.41) with
    the baseline (26.59). It omits the control value 21.17, although the
    paragraph argues that the control is the right comparator for
    lifted cuts.
- **Fix.**
  - "Their records were audited independently from the raw run records (418
    checks of the original reports); the statistics below were recomputed
    from the same records."
  - "... 26.59 for the baseline and 21.17 for the control, against 7.05
    (all) and 2.41 (auto)".

## Claims verified without change (selection)

Values are recomputed from the raw records unless noted.

- **Replay.**
  - 7,498 / 30,998 / 104,771 / 143,267 cuts; every `replay.json` passed,
    with `cuts` = `replayed_cuts` = the count from the records.
  - 14/14 tamper controls rejected in every part. The per-mode controls are
    recorded in the `v3`/`v4` blocks of `replay.json`.
  - Every one of 1,914 checked incumbents passed except `waternd2`
    `baseline-extra` root: discrepancy 0.342, max scaled violation 3.4e-11.
  - 0 rows rejected by safe rounding in any record.
- **Rounding census** (`ablation-final-summary.md`, `ablation-verify.md`
  B11): 710/5,267 = 13.5% and 127,678/138,000 = 92.5% of rows rounded;
  max |E| = 8.48e-16.
- **Table 2.** Every count matches. Every removing row also removes at
  least one recorded incumbent, not only the case witness, so the caption's
  "incumbent" is accurate. The tenfold-tolerance robustness holds
  (405 → 389, 132 → 128, 506 → 503).
- **Table 3 and Section 8.3.**
  - Solved counts: 80/90 in Part A; 52/60 in Part B; 2, 2, 2 and 1 of 20 in
    Part D.
  - Cuts (runs): 151 (33), 37 (15), 179 (40), 145 (38), 14 (2).
  - SGMs: A 1.053 / 1.267 / 1.213, SCIP-excl. 0.986-0.989; B 1.331 / 1.872 /
    1.820, SCIP-excl. 1.269 / 1.249 / 1.228.
  - Median ratios 1.336, 1.290, 2.655, 2.547. Bound counts 2/4, 3/3, 2/0,
    2/0, 5/1, 4/0, 7/7.
  - Slowdowns: A 15.2-20.3%; B 36.7-40.6%. Node sums differ by at most
    2.64%.
  - Seed variation in Part A: 3 of 30 between seed 0 and seeds 1 or 2.
  - The two Part B improvements are both on `kall_circles_c8a`.
  - The Part D final-bound differences are all on models without cuts. Cuts
    went only to `kall_ellipsoids_tc02b` and `kriging_peaks-full100`.
  - Root effects: `ex3_1_4` -6 → -5.79 / -5.69; `haverly2pq` -617.7 →
    -857.1; 403 and 358 `all-diag` cuts.
  - Part B2: 3 better / 0 worse and 6 / 1; aggregation off weakens 6
    models; rejection share 5.3% and 9.5%; `c1p12` had 127/152 rejected,
    then 104 cuts with root bound 0 against 0.3396.
  - SCIP with its disabled separators: 12 better / 1 worse; completely
    closed on 5 models; > 95% on 2 (`pointpack04` 0.958, `adhya4tp` 0.957);
    13 against 8 solved at the root. Intersection cuts were productive on 26
    models, interminor on 21, edge-concave on 0.
  - Part D: discovery stopped on 12 models (scan 1.01-7.70 s); 891 cuts on
    13 models; `mtg1c` closed 3.9%; 5 models worse, by at most 3.06%; SCIP
    with its disabled separators 8 better / 3 worse (waternd2 excluded).
  - Selection: 422, 392, 111, 322, 301, 85, 27, 58 and 20, and the order of
    the 20 Part D models.
- **Table 4 and Section 8.4.**
  - Every row reproduces. Calls minus failures equals below + rejected +
    added in every row.
  - Below threshold: 65.0-85.6% of the certified rows. Stored-row losses on
    the path family: 1.8-2.9%, all classified "tiny coefficient dropped" in
    campaign 4. Strictly, "2 to 3%" should read "about 2 to 3%".
  - Callback 0.548 s per run in Part B, of which certification is 70%. Part
    D discovery took 85% of the callback time. 307 of 313 Part D failures
    were on `kriging_peaks-full100`. The Part B median SCIP time is 0.160 s.
- **Table 5 (other cells) and Section 8.5.**
  - All other medians and all solved counts reproduce: 9, 10, 10, 7, 9, 13,
    10, 20; 9, 9, 5, 10, 20; 10, 13, 6, 20, 20.
  - Per-copy baseline bounds lie in [-0.0354, -0.0131].
  - Semidefinite minor cuts were productive in 20/20 `novarlocks` runs and
    in 0 default runs. Only intersection cuts were productive with the
    disabled separators on.
  - Campaign 3 mode: SGM 10.27 → 6.66 s, fewer nodes on all 9 instances,
    root bound improved on 20/20.
  - The four extra solves took 8.9-167.5 s. All four cells stopped at the
    cut cap.
  - On the 20 fresh C3 instances, `rowdir-wide` came within [-2.0e-7,
    7.1e-13] of the optimum. It took 3.17-33.17 s, with a median of 1 node
    and at most 38. 96.0% of its time was in the callback, and SCIP's time
    fell to a median of 3.7% of the baseline's.
  - C4: closures 95.3% and 98.6%; bound (ii) equals the optimum on 13 of 20
    and is at most 6.47e-4 below it otherwise; no root run reached (ii); the
    distance at n=80 was 0.0158-0.0288; times 3.24-133.7 s; only the cut
    modes solved n=80; 99.9% and 93.6% of the cuts were LP directions
    (`campaign4-c4-digest.md` (f)).
  - Fresh instances: 19 / 22 / 11 against 40; minimum closure 0.9739.
  - Comparators solved at most 13/20, which is below two thirds.
- **Section 8.6** (`experiments/v4/star-bench.md`): median times 1.28 ms,
  11.8 ms, 0.165 s and 2.07 s, against 6.0 ms, 0.427 s and 29 s. The time of
  the simpler oracle grows by a factor of about 70 per tenfold increase in
  k. Pieces 900 against 416. The minima have at most 94/78 bits. The
  minima agree on 15/15 instances, and the sweep's minimizer is exactly
  feasible on 20/20.
- **Appendix F, campaign 1.**
  - 24 models; 20 admitted; 19/19/18/18 solved.
  - `genpooling_lee2` took 5.61 s (baseline) and 4.89 s (control).
  - SGM 0.262 / 0.406 / 0.573 / 0.463 s.
  - Mechanism cases: 13/13/13/12.
  - 1,082 cuts: 450 polygon, 125 star, 460 Bernstein and 47 Arb, recounted
    from `certificate.method` in the campaign-1 records; 12/12 tamper
    controls; 270 incumbents.
  - Budgets 6 s and 2 s.
  - The 8 runs of `cvxnonsep_pcon40r` that failed on the variable power have
    no cut log. That is consistent with the text.
- **Appendix G.** 279, 123, 422, 160 excluded names, 7 parser refusals, and
  strata 85/208/129.
