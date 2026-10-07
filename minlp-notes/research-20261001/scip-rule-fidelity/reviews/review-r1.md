# Review r1 of `scip-rule-fidelity/note.md`

Reviewer: independent research agent (did not write the material), review
round 1, 2026-10-03. Code: [`r1-code/`](r1-code/). Logs: [`r1-logs/`](r1-logs/).
The note and the stream's code and logs were not edited.

## Verdict

**Minor fixes.** The stream's main results hold up:

- The source-reading claims in Section 1 agree with SCIP 10.0.3.
- The patch only adds instrumentation.
- Every headline count reproduces from the saved dumps.
- An independent reimplementation reproduces SCIP's step lengths and the
  stream's `z_K`, degeneracy classes and ratios on a fresh sample.

One issue is rated **major** because it misstates evidence in the Summary
(item 4, the dynamism abort). The fix is local and does not affect the
fidelity or `z_K` results. The other issues (m1–m9) are minor wording, count and
caveat fixes.

## Issues

| # | Severity | Location | Description | Required change |
|---|---|---|---|---|
| M1 | major | Summary item 4; Section 6, first bullet; Open question 1 | "In 91% of sampled cases triggered by a coefficient that is `10^15` times smaller than the others (probably rounding noise)." The 1,799 / 1,974 split is only the split between failures on the 1–3/4a piece and on the 4b piece. Every dynamism abort has `min/max(|A|,|B|,|C|) ≤ 10^-15` by definition of the test (`SCIPisHugeValue(max/min)`, huge = `10^15`), so the statistic is true by construction. The data do not support "mostly rounding noise". On the 1,799 sampled failures, the ratio has median `4.6·10^-18` and 90th percentile `4.6·10^-16`, just past the threshold; only 27% are below `10^-25`, the range where squared rounding noise lies (`r1-logs/dyn_breakdown.log`). The reviewer's noise test (`r1-code/dyn_noise.py`) uses SCIP's dumped eigenvectors and the failing ray. It finds A and B consistent with 0 at dot-product rounding level in 36 of 138 sampled failures on the 1–3/4a piece (26%). In the other 102 failures, the negative-eigenspace or `w(ray)` components are not at rounding level (median ratio `7.6·10^-18`). | Remove the 91% statement as evidence. Report the distribution of the ratio. Either give a real test of whether the small entry is zero in exact arithmetic, or say that the cause is undetermined. Reword Open question 1 and "Solver relevance" accordingly. |
| m1 | minor | Summary item 3 ("Gurobi-certified bounds"); Section 5 definitions and the paragraph under the Claim 5.1 table; "Checks actually run" | Gurobi 13.0.2 statuses are not certificates on badly scaled corners. The reviewer's full-space Gurobi model reported "optimal", with bound = objective, at values above a feasible value. Example, `waterund25` k=410: 0.1635 with cap `2·z_K` and 0.2398 with cap `4·z_K`. Exact rational arithmetic shows a point of `S` at cost 0.156185, the stream's value (`r1-logs/exact_single_ray_waterund25_410.log`). `waterund32` k=1250 and `blend480` k=365 behave the same way (`r1-logs/gurobi_fullspace_summary.log`, `gurobi_relaxed.log`, `pairs_upper.log`). In all three cases the stream reports the lower, verified value, so its ratios are right there. The wording still overstates what the solver establishes. "175 closed to `10^-4`" and "ratio upper bounds all below 0.03" for the 46 bracketed records rest on Gurobi's best bounds. | Call Gurobi's values solver-reported, not certified. Mention the observed inconsistency. Optionally, recompute `q` at Gurobi's returned points so that incumbents become verified upper bounds. |
| m2 | minor | Section 5, "Validation of `z_K`" | "20 records with ratio below 0.1 (18 solved, all agree … to about `10^-6`; 2 hit the time limit)". `logs/gurobi_zk_lowratio.jsonl` has 16 optimal and 4 time limit. Two of the time-limited records have an incumbent equal to the stream's `z_K`. One optimal `kkt3` record (`pooling_digabel18` k=351) differs by `8.9·10^-5` (Gurobi lower). | Correct the counts and the agreement statement. |
| m3 | minor | Summary item 2 ("`κ` to relative `3·10^-14`"); Section 4 ("largest relative difference `2.8·10^-14`") | The quoted figure is `|Δκ|/max(1,|κ|)`. The largest true relative difference is `1.4·10^-13` (`ex7_3_3`, `κ ≈ −0.198`). | Say "absolute (for `|κ| ≤ 1`)" or quote `1.4·10^-13`. |
| m4 | minor | Section 4, Method ("59 further sampled records were zero-basis-status aborts") | 59 is the first sample only. With the second sample there are 207 such records (148 more in `space25a`), out of 4,785 sampled records. | Correct the count. |
| m5 | minor | Section 5.2, "Mechanism of the low ratios"; Summary item 3 ("half of the low ratios") | `low_ratio_mechanism.py` selects with the analysis `zK` and ignores the Gurobi incumbent. It covers 359 records, while the table's "< 0.5" share is 371 records (34.8% of 1,067). Fourteen `nvs23` records with `zK2 = ∞` are missing, and 2 others are included. "Half" survives (187/371). The log also has 4 records where the `z_C`-determining ray has zero rate and "S reached along j* alone". This contradicts their non-degenerate class and is not explained. It is probably `one_ray_vec` used without the `_on_boundary` check. | Use the same record set as the table, or state the difference. Explain the 4 records. |
| m6 | minor | Summary item 4 ("at least 14% … are later found in the LP; cut selection drops the rest") | "Drops the rest" contradicts "at least". Body Section 6 correctly calls these lower bounds over checkable cuts, with 2,982 uncheckable cuts on MINLPLib. | Reword, for example "at most 86% of the checkable added cuts were never seen in an LP". |
| m7 | minor | Section 4 (bisection class); "The differences are in SCIP's root finder … slightly weaker coefficient" | The bound "shorter by at most `5.9·10^-4`" holds for this stream's sample only. The sibling note [`scip-set-selection`](../../scip-set-selection/note.md) §4.3 shows the same `doBinarySearch` fallback halving steps in `ex8_3_2`. | Qualify as sample-specific and cross-reference the sibling §4.3. |
| m8 | minor | Limits, "Samples" | 34 of 64 MINLPLib runs stopped at the 120 s time limit. Writing the dumps (2.1 GB gzipped) slows SCIP. So the attempts reached, the Section 6 counts and the samples are those of the instrumented binary, not of an unpatched SCIP in 120 s. Behaviour per attempt is unchanged. | Add the instrumentation overhead to the existing machine-speed caveat. |
| m9 | minor | Section 1.1 item 5 ("is never reset during the solve"); Summary item 1 ("lifetime count") | A restart frees and re-detects the nonlinear-handler expression data (`cons_nonlinear.c`: `deinitSolve` → `freeEnfoData`, then `detectNlhdlrs`). The counter therefore starts again at 0 after a restart. This shows in `ex1264`: new expressions get counter 0 at LP 113, after the root restart. Two of the 64 MINLPLib runs restarted (`ex1264`, `squfl010-040persp`). | Say "not reset except at restarts", or "per expression data, i.e. per solve run". |
| o1 | optional | Summary, "Main answer" ("the gap … is small on the McCormick generator") | The medians are 0.976 and 0.992, but 35% and 25% of attempts are below 0.9, and 11% and 7% below 0.5. | Say "small in the median". |
| o2 | optional | Section 5.2, "Most corners are degenerate" | The note does not say why the zero-cost face meets `S`. In all 115 degenerate sampled corners with `ρ ≤ 2`, a single zero-reduced-cost ray already reaches `S`. A median 60% of corner rays have zero rate. The ray is a column of a variable outside the constraint (56), a constraint variable (33) or a row slack (26) (`r1-logs/degeneracy_why.log`). So the cause is heavy dual degeneracy of SCIP's LPs. This matches the sibling note's §8.1 (82% of root corners have the criterion at a zero-cost ray). | Add one sentence and a cross-reference. |
| o3 | optional | Section 5, `ρ ≥ 4` records | The reviewer's full-space formulation was solved by Gurobi in under 60 s on all 35 `upper`-kind records tried. These include `tln12` records that remained bracketed in the stream's reduced formulation. Subject to m1, this could close most brackets. | None required. |

## Checks run and outcomes

All checks were targeted and local. No project-wide verification and no CI
were run. At most 4 compute processes ran at a time, with `OMP_NUM_THREADS=1`
and `timeout` on every long command. No SCIP rebuild and no SCIP run were
needed. Running the stream's scripts refreshed bytecode caches in
`code/__pycache__/`; no other stream file changed. No background process is
left.

### 1. Source reading

Source: `/workspace/local-home/build-scip/scipoptsuite-10.0.3/scip/src/scip/nlhdlr_quadratic.c`.
All of the following agree with the note:

- *Defaults:* `DEFAULT_NCUTSROOT 20`, `DEFAULT_NCUTS 2`, `INTERCUTS_MINVIOL 1e-4`, and detection priority 1.
- *Cut limit:* the check `nlhdlrexprdata->ncutsadded >= ncutslimit(root)` is at lines 4313–4314. The node-based variant is commented out (4310–4311). The counter is incremented before `SCIPcleanupRowprep` (4394, 4403).
- *Reset at restarts:* the counter is reset (m9). `ex1264` restarted once at the root. Attempts before the restart (LPs 1–77) use four expressions with counters up to 18. After the restart (LP 113), new expression addresses appear with counter 0 (`index/minlplib__ex1264.jsonl`, `runs_minlplib/ex1264.log`).
- *`ignorebadrayrestriction`:* the dynamism test runs only `if( nlhdlrdata->ignorebadrayrestriction )` (2066). The description is "should cut be generated even with bad numerics…?", and the default is TRUE. So it works opposite to its description.
- *`ignorenhighre`:* the code is `if( ! ignorehighre || ratio < 1e9 ) add` (4437), with default TRUE. So it also works opposite to its description.
- *Other code details:*
  - `maxrank` appears only in the parameter definition and struct.
  - The `φ(0) ≥ 0` test is present.
  - Case 4 is chosen by `nlinexprs`, `auxvar` and an exact `wcoefs != 0`.
  - `κ` is zeroed by `SCIPisZero`.
  - `computeRoot` returns ∞ when `√A ≤ D`, and bisects when `φ > 10^-10`. It stops at the first midpoint with `φ ≤ 0` and `|φ| ≤ feastol`, or when ub and lb are feasibility-equal.
  - Case 4 uses the 4a root if the 4a condition holds, else `max(t4a, t4b)`.
  - `addRowToCut` aborts when a nonbasic row is not at its side.
  - The minimal-representation and monoidal coefficients apply in Case 2 only.
  - Intersection cuts are switched off in sub-SCIPs.
  - Row basis status `LOWER` means activity at the lhs (`lpi.h`).

### 2. Patch

- `diff -u` of the original and `fidelity/src` copies of `nlhdlr_quadratic.c` is identical to `patch/nlhdlr_quadratic_dump.diff`.
- `diff -rq` of the two suite trees reports only this file.
- All inserted code writes to a memory stream or file, increments its own static counters, or reads SCIP state: names, values, bounds, basis status, `SCIPgetColRedcost` (caches a reduced cost), `SCIProwGetDualsol`, `SCIPgetLPRows`, and the rowprep.
- No control-flow statement of SCIP was changed. The added branches only set `icdfail` before existing `goto`s and returns.
- The patch cannot change SCIP's decisions. It only adds run time (see m8).

### 3. Stream scripts rerun on the saved data

All outputs are byte-identical to the stream's logs:

| Command | Outcome |
|---|---|
| `python3 summarize.py` | identical to `logs/summary.log`; every number in the Claim 5.1 table, Claim 4.1 and the `n_+ = 0` check (189/189) confirmed |
| `python3 outcomes.py` | identical; all Section 6 table entries and percentages confirmed |
| `python3 lp_entry.py mc11 mc12 minlplib` | identical (296/767, 595/2,155, 3,152/21,886) |
| `python3 check_rates.py` on mc11, mc12 and MINLPLib | identical (296/296, 595/595, 314/316) |
| `python3 explain_mismatch.py …` (all analysis files) | identical: 819 / 31 / 200 / 128 / 33 = 1,211. The note's split of "other" into 107 bisection and 21 huge-step rays checked from the log: 107 with `t_scip < t_model`, max rel `4.9·10^-4`; 21 with steps `≥ 10^8` |
| `python3 certify_two_ray.py 11 150 …` | identical (3 wrong stored `z_K`, exact bounds) |

Further checks of stream numbers:

- `r1-code/dyn_breakdown.py`: dynamism share by case is 46.2% / 54.6% / 89.2% / 57.0%. 17 of 48 instances have more than half dynamism aborts. Both match the note.
- Gurobi status counts in `logs/gurobi_zk.jsonl`: 175 optimal / 47 time limit / 10 infeasible, as stated. For `gurobi_zk_validate.jsonl`, 38/40 solved, max `3.6·10^-3`, matches the note. For `gurobi_zk_lowratio.jsonl`, see m2.
- The generator dumps cover exactly the 47 and 73 trials of the sfree note's Section 9.2 files.
- The 30 solved and 34 interrupted MINLPLib runs are confirmed.
- Section 7.1 corrected values (0.724 / 0.864, 0.616 / 0.647, 0.783, 0.675, 27 / 3) agree with `recheck_note_affected_1{1,2}.log`.
- Section 7.1 loop-table claims (9 of 12 better and none worse after round 1; better in 1 and worse in 4 of 10 after 10 rounds) agree with `exp_loop_{small,big}_fixedzk.log`.

### 4. Independent recomputation (`r1-code/indep_check.py`, no stream code imported)

Sample (`r1-code/extract_sample.py`, seed 20261003): 524 dumped attempts.

- 60 attempts from mc11 and 60 from mc12.
- 404 MINLPLib attempts from all 48 instances. Per instance: up to 6 of the stream's `ratio` records, up to 2 degenerate or zero-rate records, and 4 uniformly random attempts.
- 113 of the 524 records are outside the stream's analysed sample.
- `lp` and `cons` of every shared record agree with the stream's analysis, so the record numbering is the same.

Own reconstruction of `q`, `s̄`, rays and rates:

- `q(s̄)` equals SCIP's violation to `8.7·10^-11` relative.
- No negative rate on a non-fixed corner ray.

Own SCIP set:

- It uses an eigendecomposition of the quadratic block only, as SCIP does, and the point rule.
- Steps are computed by bracketing plus `brentq`.
- Results (`r1-logs/summarize_indep.log`):
  - Case and `κ` agree with SCIP in 519/519 records with rays. All four cases occur, including Cases 2, 3 and 4 with `κ ≠ 0`.
  - Of 43,030 compared rays, 40,899 finite steps match to `10^-6` (max `9.8·10^-7`), and 2,034 are infinite in both.
  - The 97 others all have steps `≥ 2.7·10^8`. Two of them were checked in 60-digit arithmetic (`r1-code/mp_gauge_check.py`). In both, SCIP's `∞` is correct and the reviewer's float step was rounding.
- `z_C` from SCIP's steps equals `z_C` from the reviewer's steps to `3.7·10^-8`.
- Validity: on every ray, `q > 0` on `(s̄, s̄ + t_SCIP p)` at 199 points. The one apparent exception (`blend480` k=147, ray 32, `t = 5·10^12`) is float rounding: in exact arithmetic `q` is constant along that ray (`r1-logs/exact_ray_check_blend480_147_32.log`).

`z_K` for `ρ ≤ 2`:

- Method: single rays, plus all ray pairs on a 2001-point grid with bounded-Brent refinement. The final point is checked with `q ≤ 10^-9·scale`.
- Degeneracy class agrees in 284/284 records.
- On 217 ratio records, the reviewer's `z_K` matches the stream's: median relative difference `6·10^-15`, max `8.6·10^-6`.
- The ratio `z_C/z_K` agrees to `8.6·10^-6`.

`z_K` for `ρ ≥ 3` and a cross-check (`r1-code/gurobi_fullspace.py`; own LP writer, full space, 60 s; 81 records):

- 25 `exact` records agree to `≤ 6.2·10^-6`.
- 21 `kkt3` records agree to `≤ 8.3·10^-5`; Gurobi is lower on `sssd22-08persp`, as the note's Limits say.
- 32 of 35 `upper` records agree to `≤ 3.5·10^-4`.
- On the other 3, Gurobi's "optimal" value is wrong (m1). There the stream's value was confirmed by the reviewer's own verified support-2 point and, for `waterund25` k=410, in exact arithmetic.

Random MINLPLib attempts outside the stream sample (108 with rays):

- 48 degenerate and 5 non-degenerate among those with `ρ ≤ 2`.
- 12 have all rates zero.
- 43 have `ρ ≥ 3` and were not classified.

This supports "most corners are degenerate".

### 5. Consistency with the other notes

- *sfree note* (`research-20260928b/sfree/optimal-intersection-cuts.md`, Section 9.2):
  - The stored values the note corrects (0.700 / 0.591, 0.755 / 0.648, "26 of 120 … 3") are as quoted.
  - The sfree note itself has not been updated. This is outside this stream's scope, but the corrections live only here.
- *Sibling `scip-set-selection/note.md`:*
  - Its §4.2 describes the same `ms_set` Case-4 slip and credits this stream for the `two_ray` flaw.
  - Its §4.3 is not reflected here (m7).
  - Its §8.1 (dual degeneracy) is consistent with this note's degeneracy finding (o2).

### 6. Status labels

- The labels match the evidence, except "Gurobi-certified" (m1).
- Claim 7.2 is labelled "proved". The identity `((A + r)^2 − (A − r)^2)/(4r) = A` and the resulting `ms_set` defect are correct.
