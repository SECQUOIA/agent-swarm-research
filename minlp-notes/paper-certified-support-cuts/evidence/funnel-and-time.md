# Separator funnel and time decomposition (campaign 2, repair cohort, campaign 3, v3d diagnostic)

Written 2026-10-03. This is a read-only analysis of the archived records. The
causes of stored-row rejections and the outcomes of failed support calls are
not recorded in the archive, so they come from reruns of the affected runs.

- `verification/analyze_funnel.py` (standard library only) computes every
  table below from the records and from the rerun file.
- `verification/reproduce_funnel.py` (PySCIPOpt) reruns every cut-mode run
  that had a certification failure or a stored-row (row-binding) rejection.
  There are 282 such runs. Each runs in a fresh single-threaded process from
  a scratch copy of its own snapshot, with its recorded Config, seed and
  solver time limit. Full and repeat runs were rerun with node limit 1, because
  the separator runs only at depth 0. The callback code is unchanged. The
  script wraps `certify_support` (to record outcomes) and
  `_audit_inserted_row` (to record why SCIP's stored row differs from the
  certified row). Output: `verification/funnel_repro.jsonl`.

Commands run (targeted, local; no project-wide tests, no CI):

```bash
PY=/workspace/minlp-notes/code/minlp_solver_lab/.venv/bin/python
cd /workspace/minlp-notes/paper-certified-support-cuts/verification
$PY -B reproduce_funnel.py --jobs 3 --out funnel_repro.jsonl   # final pass: 282 reruns, 7 min wall, 1,197 s summed
python3 -B analyze_funnel.py                                  # tables below (Appendix is its verbatim output)
```

The reruns were done in three passes. The cause classifier was corrected
twice: tiny dropped coefficients had first been labelled "column set changed",
and then as "rounded to integer". The final file holds only rows from the
final classifier (version 4), and all 282 runs were rerun with it. No archived
file was written; mtimes in `experiments/v3`, `experiments/v3d` and
`research-2026100{2,3}-convexification` are unchanged.

## Definitions

- The callback ends every support (certification) call in exactly one of five
  ways: certification failure (no cut), rounding rejection, insufficient
  violation, stored-row rejection, or cut added. Hence *certified* = calls -
  failures. *Insufficient violation* = certified - rounding - stored-row - added.
  The callback does not count this case. The script checks that it is never
  negative.
- *Violated* = certified rows that passed the violation test and safe rounding,
  that is, stored-row rejections + cuts added. *Share* = stored-row rejections /
  violated.
- *Presolve* cause: a block variable with a nonzero coefficient is no longer an
  active column (SCIP status AGGREGATED, MULTAGGR or FIXED; NEGATED never
  occurred). SCIP therefore stores the row in other columns, and sometimes with
  a constant.
- *SCIP* cause: all variables are active, but SCIP stored a coefficient
  differently. Either it dropped a coefficient with |c| <= epsilon = 1e-9
  (examples: 4.0e-21, -5.6e-17), or it snapped a coefficient within epsilon of
  an integer (example: -0.9999999999999998 -> -1.0).
- *Time*: total = total_seconds + preparation_seconds (the paper's measure).
  SCIP excl. callback = scip_solve_seconds - callback_seconds; the callback
  includes discovery, direction LPs, certification and row export. Shifted
  geometric means (SGM) use a shift of 1 s. Full phases use the (model, seed)
  pairs solved in every mode (summarize_v3 definition). Root phases use pairs
  completed in every mode.
- *Matched rerun*: all six separator counters equal the archived run's
  (calls, support calls, failures, stored-row rejections, rounding
  rejections, cuts). 271 of 282 reruns matched. Each of the 11 unmatched runs
  had reached its callback time allowance (budget_exhausted, callback = 0.25 s
  or 1 s). Every C3 and v3d failure count and every Part C stored-row count
  reproduced exactly.

## Key results

1. **Rounding never rejected a row.** row_rounding_rejections = 0 in every set,
   phase and mode (38,661 cuts added in total).
2. **The largest loss is insufficient violation, not the stored-row check.**
   Campaign 3 Part B full, mode all: 884 support calls -> 870 certified -> 646
   not violated enough -> 45 stored-row rejections -> 179 cuts. In Part A full
   (all), 461 of 627 certified rows were not violated enough.
3. **Failed certifications are all `incomplete` or `unsupported`; none were
   `empty`.** C3 Part A full (all): 57 of 57 incomplete (Arb 51, Bernstein 6;
   depth budget or unresolved domain). C3 Part B root (all-diag): 9 incomplete,
   10 unsupported. The 10 unsupported calls fell back to Bernstein after
   the 2,000-subset polytope budget was exceeded, and Bernstein supports only
   small 1D/2D tensors. Mode auto uses only quadratic blocks, and none of
   its support calls failed.
4. **Oracle of the added cuts.** quadratic_polytope 38,470; quadratic_star 0;
   bernstein 11; arb 180 (of 38,661 cuts in all sets). No added cut came from
   the polytope-budget fallback. Bernstein and Arb cuts occur only in campaign
   2, the repair cohort and Part A (including v3d Part A). Every Part B, Part C and v3d B/C cut came
   from the polytope oracle.
5. **Causes of stored-row rejections.** In Part A (all, auto) and in campaign 2
   holdout and repair holdout, 100% were presolve (aggregation). In Part B,
   presolve caused 74-85% (all-diag: 171 of 202 = 157 aggregated + 14 fixed;
   31 SCIP coefficient changes). In the path family (Part C and v3d C), 0%
   were presolve: all 71 / 57 / 308 rejections are coefficients below 1e-9
   that SCIP dropped.
6. **SCIP's time excluding the callback is unchanged on the MINLPLib samples.**
   The cuts change it only on the path family. See the time table below.

## Referee statement 1: "20-36% of certified cuts in Part B were discarded by the stored-row check because presolve aggregated block variables"

**Verdict: the numbers are right for modes all and all-diag, but the
statement needs three qualifications.**

| Part B (C3) | Certified | Violated | Stored-row rej. | Share of violated | Share of certified | Presolve-caused (reruns) | Presolve-caused share of violated |
|---|---:|---:|---:|---:|---:|---:|---:|
| full, all | 870 | 224 | 45 | 20.1% | 5.2% | 34 of 46 | 15.5% |
| full, auto | 726 | 176 | 31 | 17.6% | 4.3% | 25 of 31 | 14.2% |
| root, all | 429 | 113 | 23 | 20.4% | 5.4% | 18 of 23 | 15.9% |
| root, auto | 358 | 89 | 16 | 18.0% | 4.5% | 13 of 16 | 14.6% |
| root, all-diag | 1,599 | 560 | 202 | 36.1% | 12.6% | 171 of 202 | 30.5% |
| v3d root, all-diag | 1,665 | 560 | 202 | 36.1% | 12.1% | 171 of 202 | 30.5% |

1. *Denominator.* 20-36% is the share of *violated* certified rows, those that
   would otherwise have been added. Over all modes the range is 17.6-36.1%,
   because auto is lower. As a share of all certified support results (most of
   which fail the violation test), it is 4.3-12.6%.
2. *Cause.* Presolve explains 74-85% of the Part B rejections, not all of
   them. Most are aggregations; fixed variables account for 2, 2, 1, 1 and 14
   rejections in the five rows of the table. The rest come from SCIP's own
   coefficient handling. All-diag: 14 coefficients below epsilon dropped, 6
   dropped coefficients plus an integer snap, and 11 integer snaps. The
   presolve-caused loss is 14.2-30.5% of violated rows. Five models have only
   SCIP causes: bayes2_50 (35 rerun rejections), bayes2_30 (6), pooling_rt2tp
   (4), pooling_bental4pq (1) and wastewater04m2 (1). The full-all reruns had
   46 rejections against 45 archived; the three unmatched runs (bayes2_50 and
   bayes2_30) reached the 1 s allowance.
3. *Concentration.* 127 of the 202 all-diag rejections are on one model,
   kall_circlespolygons_c1p12 (25 cuts added; all its rejections are presolve).
   Without it, the all-diag share is 75/408 = 18.4%. Rejections occur on 10
   (full all), 8 (full auto), 9, 8 and 17 (root all, auto, all-diag) of the 30
   models. On 4, 4, 3, 4 and 1 of these models respectively, every violated
   row was rejected and no cut was added. In modes all and auto these are
   kall_circlespolygons_c1p12, bayes2_50 and sep1, plus bayes2_30 (full all)
   or pooling_haverly3tp (auto). In all-diag it is bayes2_30.

Suggested wording: "In Part B the stored-row check discarded 18-20% of the
certified, violated rows in the frozen modes and 36% in all-diag (127 of the
202 on one model). Most of these rows (74-85%) touched a variable that presolve
had aggregated or fixed. The others had a coefficient that SCIP dropped as zero
(|c| <= 1e-9) or rounded to an integer."

Elsewhere the shares are smaller. Part A: 7.5-9.2% of violated rows. In Part A
all-diag, 29 of 41 were presolve (12 aggregated, 17 fixed) and 12 were integer
snaps. Campaign 2 holdout full (all): 4/42 = 9.5%, all aggregated. Repair
diagnostic full (all): 12/22 = 54.5%, of which 11 presolve (7 aggregated, 4
multi-aggregated) and 1 snap. Path family: 1.9-2.5%, all epsilon drops.

## Referee statement 2: "SCIP's own time is essentially unchanged once the callback is removed"

**Verdict: correct for the MINLPLib samples (campaign 3 Parts A and B,
campaign 2), where the slowdown equals the callback time. It is not correct for
the path family, where the cuts reduce SCIP's own time and nodes in full runs.**

| Set (full runs) | Pairs | Mode | SGM total (s) | SGM SCIP excl. callback (s) | SGM callback (s) | Nodes | SCIP excl. callback / baseline, median per run | Total / baseline, median per run |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| C3 A full | 80 | baseline | 1.053 | 0.986 | 0.000 | 695,712 | - | - |
| | | all | 1.267 | 0.988 | 0.195 | 695,959 | 1.003 | 1.336 |
| | | auto | 1.213 | 0.989 | 0.164 | 694,230 | 1.037 | 1.290 |
| C3 B full | 52 | baseline | 1.331 | 1.269 | 0.000 | 771,221 | - | - |
| | | all | 1.872 | 1.249 | 0.436 | 791,603 | 0.985 | 2.655 |
| | | auto | 1.820 | 1.228 | 0.417 | 762,375 | 0.975 | 2.547 |
| C3 C full (path) | 9 | baseline | 10.270 | 10.165 | 0.000 | 452,550 | - | - |
| | | all-diag-mech | 6.661 | 4.692 | 1.249 | 283,144 | 0.395 | 0.773 |
| C2 holdout full | 25 | baseline | 0.549 | 0.496 | 0.000 | 12,995 | - | - |
| | | all | 0.989 | 0.504 | 0.446 | 12,783 | 1.036 | 1.870 |
| | | auto | 0.957 | 0.522 | 0.408 | 13,608 | 1.044 | 1.582 |
| v3d C full (path, post hoc) | 9 | baseline | 10.277 | 10.172 | 0.000 | 452,550 | - | - |
| | | all-diag-mech | 2.556 | 1.234 | 1.275 | 6,653 | 0.174 | 0.514 |
| | | all-diag-mech-wide | 4.752 | 0.135 | 4.577 | 9 | 0.036 | 1.402 |

- Part A: SCIP's time excluding the callback differs by at most 0.3% between
  modes (SGM 0.986 / 0.988 / 0.989 s), and the nodes by at most 0.2%. The total
  SGM rises 20.3% (all) and 15.2% (auto). In SGM terms this rise is the callback.
- Part B: SCIP excl. callback is 1.6% and 3.2% *lower* in the cut modes (median
  per-run ratio 0.985, 0.975), and the nodes differ by +2.6% and -1.1%. The
  total SGM rises 40.6% and 36.7%. The median per-run total ratio, 2.66 and
  2.55, is larger than the SGM suggests.
- Root runs show the same picture (completed pairs). C3 A root SCIP excl.
  callback: 0.309 / 0.307 / 0.312 / 0.314 s (baseline / all / auto / all-diag).
  C3 B root: 0.171 / 0.168 / 0.166 / 0.165 s.
- Path family: in full runs the cuts cut SCIP's own time from 10.17 to
  4.69 s (SGM) and the nodes from 452,550 to 283,144 on the 9 instances solved
  by both. At the root, SCIP excl. callback rises from 1.022 to 1.198 s (median
  ratio 1.18), because every run adds exactly 4n cuts to the root LP.

Suggested wording: "On the MINLPLib samples SCIP's own solving time (excluding
the separator callback) and its node counts were essentially unchanged: SGM
0.986 vs 0.988/0.989 s in Part A and 1.269 vs 1.249/1.228 s in Part B. The
15-41% increase of the SGM total time is the Python callback."

Caveats. The host was shared (load 14-21 during the v3 runs), so timings are
descriptive. The subtraction assumes that callback time is additive; SCIP
calls made inside the callback (row creation, addCut) count as callback time.
scip_solve_seconds agrees with the measured wall time around optimize() to
within 0.153 s on every C3 run, with a median difference of 0.0001 s.

## Paper tables

The two compact tables (campaign 3 and the post hoc diagnostic) are printed
by the script under "Paper tables" in the Appendix. Row "C3 B full, all"
carries a dagger: the cause split 34 / 12 comes from reruns totalling 46
rejections, against 45 archived.

# Appendix: output of `python3 -B verification/analyze_funnel.py`

## Record sets

- C2: `research-20261003-convexification/experiments/campaign-v2/records.jsonl`
- Repair: `research-20261003-convexification/experiments/repair-discovery-v1/records.jsonl`
- C3 A: `paper-certified-support-cuts/experiments/v3/runs/partA-full/records.jsonl`
- C3 A: `paper-certified-support-cuts/experiments/v3/runs/partA-root/records.jsonl`
- C3 B: `paper-certified-support-cuts/experiments/v3/runs/partB/records.jsonl`
- C3 C: `paper-certified-support-cuts/experiments/v3/runs/partC/records.jsonl`
- v3d A: `paper-certified-support-cuts/experiments/v3d/runs/partA-root-rowdir/records.jsonl`
- v3d B: `paper-certified-support-cuts/experiments/v3d/runs/partB-root-rowdir/records.jsonl`
- v3d C: `paper-certified-support-cuts/experiments/v3d/runs/partC-rowdir/records.jsonl`

C2 diagnostic full: 30, C2 holdout full: 90, C2 holdout repeat: 18, C2 holdout root: 90, C2 synthetic full: 39, C2 synthetic root: 15, Repair diagnostic full: 21, Repair holdout full: 24, Repair holdout repeat: 3, Repair holdout root: 27, C3 A full: 270, C3 A root: 120, C3 B full: 180, C3 B root: 120, C3 C full: 40, C3 C root: 40, v3d A root: 120, v3d B root: 120, v3d C full: 60, v3d C root: 60 (total 1487 records)

### Funnel per record set, phase and mode (cut modes)

Certified = support calls - failed. Insufficient violation, rounding, row binding and cuts added partition the certified calls. Row-binding share = row binding / (row binding + cuts), i.e. the share of certified, violated, safely rounded rows that the stored-row check discarded.

Discovery: runs whose discovery completed (in parentheses: stopped at its deadline). Blocks are summed over runs (auto-eligible in parentheses). Row-binding models: models with at least one rejection; in brackets, models on which every violated certified row was rejected (no cut added).

| Set / phase | Mode | Runs (failed) | Runs with callback | Discovery (incomplete) | Blocks (auto-eligible) | Support calls | Certified | Failed | Insufficient violation | Rounding rej. | Row-binding rej. (runs / models [all rejected]) | Cuts added (runs) | Row-binding share |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| C2 diagnostic full | all | 10 (2) | 8 | 8 (0) | 136 (37) | 58 | 21 | 37 | 6 | 0 | 0 (0 / 0 [0]) | 15 (2) | 0.0% |
| C2 diagnostic full | auto | 10 (2) | 8 | 8 (0) | 136 (37) | 11 | 11 | 0 | 6 | 0 | 0 (0 / 0 [0]) | 5 (1) | 0.0% |
| C2 holdout full | all | 30 (0) | 28 | 28 (0) | 156 (63) | 138 | 119 | 19 | 77 | 0 | 4 (2 / 2 [1]) | 38 (7) | 9.5% |
| C2 holdout full | auto | 30 (0) | 28 | 28 (0) | 156 (63) | 51 | 51 | 0 | 41 | 0 | 0 (0 / 0 [0]) | 10 (3) | 0.0% |
| C2 holdout repeat | all | 6 (0) | 6 | 6 (0) | 38 (4) | 31 | 31 | 0 | 28 | 0 | 1 (1 / 1 [0]) | 2 (1) | 33.3% |
| C2 holdout repeat | auto | 6 (0) | 6 | 6 (0) | 38 (4) | 21 | 21 | 0 | 19 | 0 | 0 (0 / 0 [0]) | 2 (1) | 0.0% |
| C2 holdout root | all | 30 (0) | 28 | 28 (0) | 156 (63) | 64 | 56 | 8 | 34 | 0 | 1 (1 / 1 [1]) | 21 (6) | 4.5% |
| C2 holdout root | auto | 30 (0) | 28 | 28 (0) | 156 (63) | 6 | 6 | 0 | 4 | 0 | 0 (0 / 0 [0]) | 2 (2) | 0.0% |
| C2 synthetic full | all | 13 (0) | 6 | 6 (0) | 5 (1) | 19 | 15 | 4 | 1 | 0 | 1 (1 / 1 [0]) | 13 (4) | 7.1% |
| C2 synthetic full | auto | 13 (0) | 6 | 6 (0) | 5 (1) | 2 | 2 | 0 | 0 | 0 | 0 (0 / 0 [0]) | 2 (1) | 0.0% |
| C2 synthetic root | all | 5 (0) | 4 | 4 (0) | 3 (1) | 15 | 13 | 2 | 1 | 0 | 1 (1 / 1 [0]) | 11 (3) | 8.3% |
| C2 synthetic root | auto | 5 (0) | 4 | 4 (0) | 3 (1) | 2 | 2 | 0 | 0 | 0 | 0 (0 / 0 [0]) | 2 (1) | 0.0% |
| Repair diagnostic full | all | 7 (0) | 7 | 5 (2) | 52 (22) | 72 | 63 | 9 | 41 | 0 | 12 (3 / 3 [1]) | 10 (2) | 54.5% |
| Repair diagnostic full | auto | 7 (0) | 7 | 5 (2) | 52 (22) | 24 | 24 | 0 | 24 | 0 | 0 (0 / 0 [0]) | 0 (0) | - |
| Repair holdout full | all | 8 (0) | 8 | 8 (0) | 52 (42) | 88 | 88 | 0 | 75 | 0 | 1 (1 / 1 [0]) | 12 (4) | 7.7% |
| Repair holdout full | auto | 8 (0) | 8 | 8 (0) | 52 (42) | 48 | 48 | 0 | 44 | 0 | 1 (1 / 1 [0]) | 3 (2) | 25.0% |
| Repair holdout repeat | all | 1 (0) | 1 | 1 (0) | 5 (0) | 24 | 24 | 0 | 21 | 0 | 0 (0 / 0 [0]) | 3 (1) | 0.0% |
| Repair holdout repeat | auto | 1 (0) | 1 | 1 (0) | 5 (0) | 0 | 0 | 0 | 0 | 0 | 0 (0 / 0 [0]) | 0 (0) | - |
| Repair holdout root | all | 9 (0) | 9 | 8 (1) | 78 (46) | 83 | 83 | 0 | 71 | 0 | 1 (1 / 1 [0]) | 11 (3) | 8.3% |
| Repair holdout root | auto | 9 (0) | 9 | 8 (1) | 78 (46) | 38 | 38 | 0 | 34 | 0 | 1 (1 / 1 [0]) | 3 (2) | 25.0% |
| C3 A full | all | 90 (0) | 84 | 84 (0) | 468 (189) | 684 | 627 | 57 | 461 | 0 | 15 (9 / 3 [1]) | 151 (33) | 9.0% |
| C3 A full | auto | 90 (0) | 84 | 84 (0) | 468 (189) | 303 | 303 | 0 | 263 | 0 | 3 (3 / 1 [0]) | 37 (15) | 7.5% |
| C3 A root | all | 30 (0) | 28 | 28 (0) | 156 (63) | 228 | 209 | 19 | 154 | 0 | 5 (3 / 3 [1]) | 50 (11) | 9.1% |
| C3 A root | auto | 30 (0) | 28 | 28 (0) | 156 (63) | 101 | 101 | 0 | 88 | 0 | 1 (1 / 1 [0]) | 12 (5) | 7.7% |
| C3 A root | all-diag | 30 (0) | 28 | 28 (0) | 200 (67) | 1074 | 1040 | 34 | 596 | 0 | 41 (5 / 5 [1]) | 403 (11) | 9.2% |
| C3 B full | all | 60 (0) | 54 | 54 (0) | 668 (448) | 884 | 870 | 14 | 646 | 0 | 45 (20 / 10 [4]) | 179 (40) | 20.1% |
| C3 B full | auto | 60 (0) | 54 | 54 (0) | 668 (448) | 726 | 726 | 0 | 550 | 0 | 31 (15 / 8 [4]) | 145 (38) | 17.6% |
| C3 B root | all | 30 (0) | 27 | 27 (0) | 334 (224) | 436 | 429 | 7 | 316 | 0 | 23 (9 / 9 [3]) | 90 (20) | 20.4% |
| C3 B root | auto | 30 (0) | 27 | 27 (0) | 334 (224) | 358 | 358 | 0 | 269 | 0 | 16 (8 / 8 [4]) | 73 (19) | 18.0% |
| C3 B root | all-diag | 30 (0) | 27 | 27 (0) | 383 (229) | 1618 | 1599 | 19 | 1039 | 0 | 202 (17 / 17 [1]) | 358 (25) | 36.1% |
| C3 C full | all-diag-mech | 20 (0) | 20 | 20 (0) | 750 (0) | 3462 | 3462 | 0 | 391 | 0 | 71 (13 / 13 [0]) | 3000 (20) | 2.3% |
| C3 C root | all-diag-mech | 20 (0) | 20 | 20 (0) | 750 (0) | 3462 | 3462 | 0 | 391 | 0 | 71 (13 / 13 [0]) | 3000 (20) | 2.3% |
| v3d A root | all | 30 (0) | 28 | 28 (0) | 156 (63) | 232 | 213 | 19 | 156 | 0 | 5 (3 / 3 [1]) | 52 (11) | 8.8% |
| v3d A root | auto | 30 (0) | 28 | 28 (0) | 156 (63) | 104 | 104 | 0 | 89 | 0 | 1 (1 / 1 [0]) | 14 (5) | 6.7% |
| v3d A root | all-diag | 30 (0) | 28 | 28 (0) | 200 (67) | 1105 | 1071 | 34 | 627 | 0 | 41 (5 / 5 [1]) | 403 (11) | 9.2% |
| v3d B root | all | 30 (0) | 27 | 27 (0) | 334 (224) | 450 | 441 | 9 | 324 | 0 | 22 (9 / 9 [3]) | 95 (20) | 18.8% |
| v3d B root | auto | 30 (0) | 27 | 27 (0) | 334 (224) | 370 | 370 | 0 | 279 | 0 | 15 (8 / 8 [4]) | 76 (19) | 16.5% |
| v3d B root | all-diag | 30 (0) | 27 | 27 (0) | 383 (229) | 1686 | 1665 | 21 | 1105 | 0 | 202 (17 / 17 [1]) | 358 (25) | 36.1% |
| v3d C full | all-diag-mech | 20 (0) | 20 | 20 (0) | 750 (0) | 3804 | 3804 | 0 | 747 | 0 | 57 (15 / 15 [0]) | 3000 (20) | 1.9% |
| v3d C full | all-diag-mech-wide | 20 (0) | 20 | 20 (0) | 750 (0) | 15361 | 15361 | 0 | 3053 | 0 | 308 (20 / 20 [0]) | 12000 (20) | 2.5% |
| v3d C root | all-diag-mech | 20 (0) | 20 | 20 (0) | 750 (0) | 3804 | 3804 | 0 | 747 | 0 | 57 (15 / 15 [0]) | 3000 (20) | 1.9% |
| v3d C root | all-diag-mech-wide | 20 (0) | 20 | 20 (0) | 750 (0) | 15361 | 15361 | 0 | 3053 | 0 | 308 (20 / 20 [0]) | 12000 (20) | 2.5% |

### Oracle method of every added cut

| Set / phase | Mode | Cuts | quadratic_polytope | quadratic_star | quadratic_polygon | bernstein | arb | polytope budget fallback |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| C2 diagnostic full | all | 15 | 4 | 0 | 0 | 0 | 11 | 0 |
| C2 diagnostic full | auto | 5 | 5 | 0 | 0 | 0 | 0 | 0 |
| C2 holdout full | all | 38 | 25 | 0 | 0 | 1 | 12 | 0 |
| C2 holdout full | auto | 10 | 10 | 0 | 0 | 0 | 0 | 0 |
| C2 holdout repeat | all | 2 | 2 | 0 | 0 | 0 | 0 | 0 |
| C2 holdout repeat | auto | 2 | 2 | 0 | 0 | 0 | 0 | 0 |
| C2 holdout root | all | 21 | 17 | 0 | 0 | 1 | 3 | 0 |
| C2 holdout root | auto | 2 | 2 | 0 | 0 | 0 | 0 | 0 |
| C2 synthetic full | all | 13 | 10 | 0 | 0 | 0 | 3 | 0 |
| C2 synthetic full | auto | 2 | 2 | 0 | 0 | 0 | 0 | 0 |
| C2 synthetic root | all | 11 | 10 | 0 | 0 | 0 | 1 | 0 |
| C2 synthetic root | auto | 2 | 2 | 0 | 0 | 0 | 0 | 0 |
| Repair diagnostic full | all | 10 | 2 | 0 | 0 | 0 | 8 | 0 |
| Repair diagnostic full | auto | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Repair holdout full | all | 12 | 12 | 0 | 0 | 0 | 0 | 0 |
| Repair holdout full | auto | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| Repair holdout repeat | all | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| Repair holdout repeat | auto | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Repair holdout root | all | 11 | 11 | 0 | 0 | 0 | 0 | 0 |
| Repair holdout root | auto | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| C3 A full | all | 151 | 112 | 0 | 0 | 3 | 36 | 0 |
| C3 A full | auto | 37 | 37 | 0 | 0 | 0 | 0 | 0 |
| C3 A root | all | 50 | 37 | 0 | 0 | 1 | 12 | 0 |
| C3 A root | auto | 12 | 12 | 0 | 0 | 0 | 0 | 0 |
| C3 A root | all-diag | 403 | 360 | 0 | 0 | 2 | 41 | 0 |
| C3 B full | all | 179 | 179 | 0 | 0 | 0 | 0 | 0 |
| C3 B full | auto | 145 | 145 | 0 | 0 | 0 | 0 | 0 |
| C3 B root | all | 90 | 90 | 0 | 0 | 0 | 0 | 0 |
| C3 B root | auto | 73 | 73 | 0 | 0 | 0 | 0 | 0 |
| C3 B root | all-diag | 358 | 358 | 0 | 0 | 0 | 0 | 0 |
| C3 C full | all-diag-mech | 3000 | 3000 | 0 | 0 | 0 | 0 | 0 |
| C3 C root | all-diag-mech | 3000 | 3000 | 0 | 0 | 0 | 0 | 0 |
| v3d A root | all | 52 | 39 | 0 | 0 | 1 | 12 | 0 |
| v3d A root | auto | 14 | 14 | 0 | 0 | 0 | 0 | 0 |
| v3d A root | all-diag | 403 | 360 | 0 | 0 | 2 | 41 | 0 |
| v3d B root | all | 95 | 95 | 0 | 0 | 0 | 0 | 0 |
| v3d B root | auto | 76 | 76 | 0 | 0 | 0 | 0 | 0 |
| v3d B root | all-diag | 358 | 358 | 0 | 0 | 0 | 0 | 0 |
| v3d C full | all-diag-mech | 3000 | 3000 | 0 | 0 | 0 | 0 | 0 |
| v3d C full | all-diag-mech-wide | 12000 | 12000 | 0 | 0 | 0 | 0 | 0 |
| v3d C root | all-diag-mech | 3000 | 3000 | 0 | 0 | 0 | 0 | 0 |
| v3d C root | all-diag-mech-wide | 12000 | 12000 | 0 | 0 | 0 | 0 | 0 |
| **all sets** | | 38661 | 38470 | 0 | 0 | 11 | 180 | 0 |

### Time decomposition over runs solved (full, repeat) or completed (root) in every mode

SGM with shift 1 s. SCIP excl. callback = scip_solve_seconds - callback_seconds. Ratio columns are per-run ratios to baseline over the same pairs (median; geometric mean).

| Set / phase | Pairs | Mode | SGM total | SGM SCIP solve | SGM SCIP excl. callback | SGM callback | Sum callback (s) | Nodes | SCIP excl. callback / baseline, median; geo. mean | Total / baseline, median |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| C2 diagnostic full | 5 | baseline | 0.706 | 0.611 | 0.611 | 0.000 | 0.00 | 2,013 | - | - |
| C2 diagnostic full | 5 | all | 2.246 | 2.156 | 0.623 | 1.401 | 7.31 | 2,013 | 1.067; 1.040 | 6.081 |
| C2 diagnostic full | 5 | auto | 2.147 | 2.057 | 0.606 | 1.330 | 7.02 | 2,013 | 1.077; 0.994 | 5.920 |
| C2 holdout full | 25 | baseline | 0.549 | 0.496 | 0.496 | 0.000 | 0.00 | 12,995 | - | - |
| C2 holdout full | 25 | all | 0.989 | 0.935 | 0.504 | 0.446 | 15.90 | 12,783 | 1.036; 1.080 | 1.870 |
| C2 holdout full | 25 | auto | 0.957 | 0.902 | 0.522 | 0.408 | 15.26 | 13,608 | 1.044; 1.067 | 1.582 |
| C2 holdout repeat | 6 | baseline | 1.201 | 1.142 | 1.142 | 0.000 | 0.00 | 4,289 | - | - |
| C2 holdout repeat | 6 | all | 1.780 | 1.723 | 1.119 | 0.569 | 5.39 | 4,829 | 0.983; 0.955 | 1.437 |
| C2 holdout repeat | 6 | auto | 1.786 | 1.730 | 1.118 | 0.567 | 5.41 | 4,829 | 0.938; 0.949 | 1.299 |
| C2 holdout root | 30 | baseline | 0.356 | 0.295 | 0.295 | 0.000 | 0.00 | 30 | - | - |
| C2 holdout root | 30 | all | 0.873 | 0.814 | 0.270 | 0.538 | 25.19 | 30 | 1.044; 1.030 | 2.725 |
| C2 holdout root | 30 | auto | 0.828 | 0.769 | 0.272 | 0.502 | 23.88 | 30 | 0.987; 0.926 | 1.864 |
| C2 synthetic full | 12 | baseline | 0.055 | 0.029 | 0.029 | 0.000 | 0.00 | 188 | - | - |
| C2 synthetic full | 12 | all | 0.068 | 0.044 | 0.018 | 0.026 | 0.32 | 186 | 0.999; 0.742 | 1.180 |
| C2 synthetic full | 12 | auto | 0.056 | 0.030 | 0.025 | 0.006 | 0.07 | 186 | 0.949; 0.883 | 1.089 |
| C2 synthetic root | 5 | baseline | 0.057 | 0.032 | 0.032 | 0.000 | 0.00 | 5 | - | - |
| C2 synthetic root | 5 | all | 0.112 | 0.085 | 0.028 | 0.057 | 0.29 | 5 | 0.948; 0.748 | 1.637 |
| C2 synthetic root | 5 | auto | 0.074 | 0.048 | 0.035 | 0.013 | 0.07 | 5 | 1.181; 0.907 | 1.302 |
| Repair diagnostic full | 4 | baseline | 0.869 | 0.766 | 0.766 | 0.000 | 0.00 | 2,009 | - | - |
| Repair diagnostic full | 4 | all | 0.980 | 0.872 | 0.605 | 0.288 | 1.21 | 1,299 | 0.946; 0.899 | 1.480 |
| Repair diagnostic full | 4 | auto | 0.962 | 0.856 | 0.741 | 0.105 | 0.42 | 2,009 | 0.879; 0.880 | 1.275 |
| Repair holdout full | 4 | baseline | 0.918 | 0.835 | 0.835 | 0.000 | 0.00 | 1,544 | - | - |
| Repair holdout full | 4 | all | 1.159 | 1.082 | 0.850 | 0.227 | 0.93 | 1,554 | 1.004; 1.028 | 1.256 |
| Repair holdout full | 4 | auto | 1.162 | 1.078 | 0.864 | 0.200 | 0.83 | 1,549 | 1.055; 1.055 | 1.275 |
| Repair holdout repeat | 1 | baseline | 1.296 | 1.226 | 1.226 | 0.000 | 0.00 | 436 | - | - |
| Repair holdout repeat | 1 | all | 1.913 | 1.835 | 1.585 | 0.250 | 0.25 | 298 | 1.293; 1.293 | 1.477 |
| Repair holdout repeat | 1 | auto | 1.450 | 1.380 | 1.237 | 0.143 | 0.14 | 436 | 1.009; 1.009 | 1.119 |
| Repair holdout root | 9 | baseline | 0.574 | 0.470 | 0.470 | 0.000 | 0.00 | 9 | - | - |
| Repair holdout root | 9 | all | 0.717 | 0.612 | 0.440 | 0.169 | 1.55 | 9 | 0.948; 0.943 | 1.199 |
| Repair holdout root | 9 | auto | 0.729 | 0.622 | 0.470 | 0.148 | 1.36 | 9 | 1.007; 0.999 | 1.190 |
| C3 A full | 80 | baseline | 1.053 | 0.986 | 0.986 | 0.000 | 0.00 | 695,712 | - | - |
| C3 A full | 80 | all | 1.267 | 1.198 | 0.988 | 0.195 | 17.92 | 695,959 | 1.003; 1.068 | 1.336 |
| C3 A full | 80 | auto | 1.213 | 1.146 | 0.989 | 0.164 | 15.60 | 694,230 | 1.037; 1.046 | 1.290 |
| C3 A root | 30 | baseline | 0.375 | 0.309 | 0.309 | 0.000 | 0.00 | 30 | - | - |
| C3 A root | 30 | all | 0.577 | 0.506 | 0.307 | 0.194 | 6.60 | 30 | 1.014; 0.996 | 1.548 |
| C3 A root | 30 | auto | 0.540 | 0.471 | 0.312 | 0.159 | 5.61 | 30 | 0.988; 0.992 | 1.439 |
| C3 A root | 30 | all-diag | 0.841 | 0.771 | 0.314 | 0.422 | 19.08 | 30 | 0.994; 1.054 | 1.773 |
| C3 B full | 52 | baseline | 1.331 | 1.269 | 1.269 | 0.000 | 0.00 | 771,221 | - | - |
| C3 B full | 52 | all | 1.872 | 1.809 | 1.249 | 0.436 | 24.75 | 791,603 | 0.985; 0.952 | 2.655 |
| C3 B full | 52 | auto | 1.820 | 1.759 | 1.228 | 0.417 | 23.81 | 762,375 | 0.975; 0.916 | 2.547 |
| C3 B root | 30 | baseline | 0.218 | 0.171 | 0.171 | 0.000 | 0.00 | 30 | - | - |
| C3 B root | 30 | all | 0.699 | 0.652 | 0.168 | 0.502 | 16.43 | 30 | 0.963; 0.976 | 3.456 |
| C3 B root | 30 | auto | 0.694 | 0.643 | 0.166 | 0.496 | 16.32 | 30 | 1.004; 0.982 | 3.393 |
| C3 B root | 30 | all-diag | 1.319 | 1.268 | 0.165 | 1.141 | 45.11 | 30 | 0.974; 1.006 | 7.363 |
| C3 C full | 9 | baseline | 10.270 | 10.165 | 10.165 | 0.000 | 0.00 | 452,550 | - | - |
| C3 C full | 9 | all-diag-mech | 6.661 | 6.596 | 4.692 | 1.249 | 11.60 | 283,144 | 0.395; 0.407 | 0.773 |
| C3 C root | 20 | baseline | 1.099 | 1.022 | 1.022 | 0.000 | 0.00 | 20 | - | - |
| C3 C root | 20 | all-diag-mech | 4.077 | 4.002 | 1.198 | 2.913 | 73.57 | 20 | 1.180; 1.156 | 3.986 |
| v3d A root | 30 | baseline | 0.342 | 0.285 | 0.285 | 0.000 | 0.00 | 30 | - | - |
| v3d A root | 30 | all | 0.515 | 0.459 | 0.285 | 0.170 | 5.78 | 30 | 1.021; 1.058 | 1.422 |
| v3d A root | 30 | auto | 0.478 | 0.421 | 0.283 | 0.138 | 4.85 | 30 | 0.999; 1.012 | 1.251 |
| v3d A root | 30 | all-diag | 0.732 | 0.672 | 0.282 | 0.365 | 15.86 | 30 | 1.031; 1.100 | 1.674 |
| v3d B root | 30 | baseline | 0.206 | 0.164 | 0.164 | 0.000 | 0.00 | 30 | - | - |
| v3d B root | 30 | all | 0.657 | 0.615 | 0.159 | 0.475 | 15.59 | 30 | 1.009; 1.012 | 3.835 |
| v3d B root | 30 | auto | 0.648 | 0.603 | 0.150 | 0.471 | 15.53 | 30 | 0.926; 0.916 | 3.717 |
| v3d B root | 30 | all-diag | 1.265 | 1.217 | 0.154 | 1.101 | 42.91 | 30 | 0.979; 0.989 | 6.354 |
| v3d C full | 9 | baseline | 10.277 | 10.172 | 10.172 | 0.000 | 0.00 | 452,550 | - | - |
| v3d C full | 9 | all-diag-mech | 2.556 | 2.508 | 1.234 | 1.275 | 11.85 | 6,653 | 0.174; 0.122 | 0.514 |
| v3d C full | 9 | all-diag-mech-wide | 4.752 | 4.708 | 0.135 | 4.577 | 43.57 | 9 | 0.036; 0.015 | 1.402 |
| v3d C root | 20 | baseline | 1.090 | 1.008 | 1.008 | 0.000 | 0.00 | 20 | - | - |
| v3d C root | 20 | all-diag-mech | 4.062 | 3.990 | 1.057 | 3.002 | 76.17 | 20 | 1.100; 1.066 | 4.201 |
| v3d C root | 20 | all-diag-mech-wide | 10.833 | 10.752 | 0.299 | 10.498 | 284.48 | 20 | 0.300; 0.273 | 10.067 |

### Reproduction coverage (reproduce_funnel.py)

Every cut-mode run with a certification failure or a row-binding rejection was rerun in a fresh process from a copy of its own snapshot, with its recorded Config, seed and time limit. Full runs were rerun with node limit 1 (the separator runs only at the root). Matched = all six separator counters equal the archived run's.

| Set / phase | Mode | Runs rerun | Counters matched | Archived failed / rerun | Archived row binding / rerun |
|---|---|---:|---:|---:|---:|
| C2 diagnostic full | all | 2 | 2 | 37 / 37 | 0 / 0 |
| C2 holdout full | all | 5 | 4 | 19 / 19 | 4 / 4 |
| C2 holdout repeat | all | 1 | 1 | 0 / 0 | 1 / 1 |
| C2 holdout root | all | 4 | 2 | 8 / 11 | 1 / 3 |
| C2 synthetic full | all | 3 | 3 | 4 / 4 | 1 / 1 |
| C2 synthetic root | all | 2 | 2 | 2 / 2 | 1 / 1 |
| Repair diagnostic full | all | 3 | 3 | 9 / 9 | 12 / 12 |
| Repair holdout full | all | 1 | 1 | 0 / 0 | 1 / 1 |
| Repair holdout full | auto | 1 | 1 | 0 / 0 | 1 / 1 |
| Repair holdout root | all | 1 | 1 | 0 / 0 | 1 / 1 |
| Repair holdout root | auto | 1 | 1 | 0 / 0 | 1 / 1 |
| C3 A full | all | 18 | 18 | 57 / 57 | 15 / 15 |
| C3 A full | auto | 3 | 3 | 0 / 0 | 3 / 3 |
| C3 A root | all | 6 | 6 | 19 / 19 | 5 / 5 |
| C3 A root | auto | 1 | 1 | 0 / 0 | 1 / 1 |
| C3 A root | all-diag | 8 | 8 | 34 / 34 | 41 / 41 |
| C3 B full | all | 22 | 19 | 14 / 14 | 45 / 46 |
| C3 B full | auto | 15 | 13 | 0 / 0 | 31 / 31 |
| C3 B root | all | 10 | 9 | 7 / 7 | 23 / 23 |
| C3 B root | auto | 8 | 7 | 0 / 0 | 16 / 16 |
| C3 B root | all-diag | 19 | 19 | 19 / 19 | 202 / 202 |
| C3 C full | all-diag-mech | 13 | 13 | 0 / 0 | 71 / 71 |
| C3 C root | all-diag-mech | 13 | 13 | 0 / 0 | 71 / 71 |
| v3d A root | all | 6 | 6 | 19 / 19 | 5 / 5 |
| v3d A root | auto | 1 | 1 | 0 / 0 | 1 / 1 |
| v3d A root | all-diag | 8 | 8 | 34 / 34 | 41 / 41 |
| v3d B root | all | 10 | 9 | 9 / 9 | 22 / 22 |
| v3d B root | auto | 8 | 8 | 0 / 0 | 15 / 15 |
| v3d B root | all-diag | 19 | 19 | 21 / 21 | 202 / 202 |
| v3d C full | all-diag-mech | 15 | 15 | 0 / 0 | 57 / 57 |
| v3d C full | all-diag-mech-wide | 20 | 20 | 0 / 0 | 308 / 308 |
| v3d C root | all-diag-mech | 15 | 15 | 0 / 0 | 57 / 57 |
| v3d C root | all-diag-mech-wide | 20 | 20 | 0 / 0 | 308 / 308 |

### Outcomes of failed support calls (reruns)

Counts over all reruns; in parentheses the part from runs whose counters matched the archive.

| Set / phase | Mode | incomplete (depth budget or unresolved domain/target) | incomplete (target not certified) | unsupported (unsupported expression) |
|---|---|---:|---:|---:|
| C2 diagnostic full | all | 13 (13) | 0 (0) | 24 (24) |
| C2 holdout full | all | 19 (19) | 0 (0) | 0 (0) |
| C2 holdout root | all | 11 (5) | 0 (0) | 0 (0) |
| C2 synthetic full | all | 2 (2) | 0 (0) | 2 (2) |
| C2 synthetic root | all | 2 (2) | 0 (0) | 0 (0) |
| Repair diagnostic full | all | 9 (9) | 0 (0) | 0 (0) |
| C3 A full | all | 57 (57) | 0 (0) | 0 (0) |
| C3 A root | all | 19 (19) | 0 (0) | 0 (0) |
| C3 A root | all-diag | 34 (34) | 0 (0) | 0 (0) |
| C3 B full | all | 8 (8) | 6 (6) | 0 (0) |
| C3 B root | all | 4 (4) | 3 (3) | 0 (0) |
| C3 B root | all-diag | 6 (6) | 3 (3) | 10 (10) |
| v3d A root | all | 19 (19) | 0 (0) | 0 (0) |
| v3d A root | all-diag | 34 (34) | 0 (0) | 0 (0) |
| v3d B root | all | 4 (4) | 5 (5) | 0 (0) |
| v3d B root | all-diag | 6 (6) | 5 (5) | 10 (10) |

### Causes of row-binding rejections (reruns)

Each cell: rejections over all reruns (in parentheses: from runs whose counters matched the archive). presolve: a block variable of the row is no longer an active column (SCIP status AGGREGATED, MULTAGGR, FIXED or NEGATED), so SCIP stores the row in other columns and with a constant. SCIP: all variables active, but SCIP stored a coefficient differently (dropped as zero below epsilon 1e-9, or snapped to the nearest integer within epsilon).

| Set / phase | Mode | Rejections | presolve: AGGREGATED | presolve: FIXED | presolve: MULTAGGR | SCIP: coefficient below epsilon dropped | SCIP: coefficient below epsilon dropped and coefficient rounded to integer | SCIP: coefficient rounded to integer | Presolve share |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| C2 holdout full | all | 4 | 4 (3) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 100.0% |
| C2 holdout repeat | all | 1 | 1 (1) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 100.0% |
| C2 holdout root | all | 3 | 3 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 100.0% |
| C2 synthetic full | all | 1 | 0 (0) | 0 (0) | 0 (0) | 1 (1) | 0 (0) | 0 (0) | 0.0% |
| C2 synthetic root | all | 1 | 0 (0) | 0 (0) | 0 (0) | 1 (1) | 0 (0) | 0 (0) | 0.0% |
| Repair diagnostic full | all | 12 | 7 (7) | 0 (0) | 4 (4) | 0 (0) | 0 (0) | 1 (1) | 91.7% |
| Repair holdout full | all | 1 | 1 (1) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 100.0% |
| Repair holdout full | auto | 1 | 1 (1) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 100.0% |
| Repair holdout root | all | 1 | 1 (1) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 100.0% |
| Repair holdout root | auto | 1 | 1 (1) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 100.0% |
| C3 A full | all | 15 | 15 (15) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 100.0% |
| C3 A full | auto | 3 | 3 (3) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 100.0% |
| C3 A root | all | 5 | 5 (5) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 100.0% |
| C3 A root | auto | 1 | 1 (1) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 100.0% |
| C3 A root | all-diag | 41 | 12 (12) | 17 (17) | 0 (0) | 0 (0) | 0 (0) | 12 (12) | 70.7% |
| C3 B full | all | 46 | 32 (32) | 2 (2) | 0 (0) | 7 (1) | 2 (0) | 3 (3) | 73.9% |
| C3 B full | auto | 31 | 23 (23) | 2 (2) | 0 (0) | 4 (0) | 2 (0) | 0 (0) | 80.6% |
| C3 B root | all | 23 | 17 (17) | 1 (1) | 0 (0) | 2 (0) | 1 (0) | 2 (2) | 78.3% |
| C3 B root | auto | 16 | 12 (12) | 1 (1) | 0 (0) | 2 (0) | 1 (0) | 0 (0) | 81.2% |
| C3 B root | all-diag | 202 | 157 (157) | 14 (14) | 0 (0) | 14 (14) | 6 (6) | 11 (11) | 84.7% |
| C3 C full | all-diag-mech | 71 | 0 (0) | 0 (0) | 0 (0) | 71 (71) | 0 (0) | 0 (0) | 0.0% |
| C3 C root | all-diag-mech | 71 | 0 (0) | 0 (0) | 0 (0) | 71 (71) | 0 (0) | 0 (0) | 0.0% |
| v3d A root | all | 5 | 5 (5) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 100.0% |
| v3d A root | auto | 1 | 1 (1) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 100.0% |
| v3d A root | all-diag | 41 | 12 (12) | 17 (17) | 0 (0) | 0 (0) | 0 (0) | 12 (12) | 70.7% |
| v3d B root | all | 22 | 17 (17) | 1 (1) | 0 (0) | 2 (0) | 0 (0) | 2 (2) | 81.8% |
| v3d B root | auto | 15 | 12 (12) | 1 (1) | 0 (0) | 2 (2) | 0 (0) | 0 (0) | 86.7% |
| v3d B root | all-diag | 202 | 157 (157) | 14 (14) | 0 (0) | 14 (14) | 6 (6) | 11 (11) | 84.7% |
| v3d C full | all-diag-mech | 57 | 0 (0) | 0 (0) | 0 (0) | 57 (57) | 0 (0) | 0 (0) | 0.0% |
| v3d C full | all-diag-mech-wide | 308 | 0 (0) | 0 (0) | 0 (0) | 308 (308) | 0 (0) | 0 (0) | 0.0% |
| v3d C root | all-diag-mech | 57 | 0 (0) | 0 (0) | 0 (0) | 57 (57) | 0 (0) | 0 (0) | 0.0% |
| v3d C root | all-diag-mech-wide | 308 | 0 (0) | 0 (0) | 0 (0) | 308 (308) | 0 (0) | 0 (0) | 0.0% |
| **all reruns** | | 1567 | 500 (496) | 70 (70) | 4 (4) | 921 (905) | 18 (12) | 54 (54) | 36.6% |

Examples (first two per cause):

- presolve: AGGREGATED: `campaign-v2/012_nous1__all__full` {"certified_rhs": 0.0, "changed": [["t_v32", 1.0, 0.0], ["t_v33", 0.0, -1.0]], "constant": 1.0, "lhs": 0.0, "removed": [["v32", "AGGREGATED"]]}
- presolve: AGGREGATED: `campaign-v2/084_ex1223__all__full` {"certified_rhs": -0.9595629629629625, "changed": [["t_v4", -0.19555555555555493, 0.0], ["t_v8", 0.0, -0.19555555555555493]], "constant": 0.0, "lhs": -0.9595629629629625, "removed": [["v4", "AGGREGATED"]]}
- presolve: FIXED: `partA-root/012_pooling_adhya4pq__root__s0__all-diag` {"certified_rhs": -1.0000000000000002, "changed": [["t_v21", 0.05, 0.0]], "constant": 0.0, "lhs": -1.0000000000000002, "removed": [["v21", "FIXED"]]}
- presolve: FIXED: `partA-root/012_pooling_adhya4pq__root__s0__all-diag` {"certified_rhs": -1.0000000000000002, "changed": [["t_v21", 0.05, 0.0]], "constant": 0.0, "lhs": -1.0000000000000002, "removed": [["v21", "FIXED"]]}
- presolve: MULTAGGR: `repair-discovery-v1/027_syn15m__all__full` {"certified_rhs": -0.6516321612169417, "changed": [["t_v22", -0.6324344474303476, 0.0], ["t_v26", 0.0, -0.6324344474303476], ["t_v27", 0.0, -0.6324344474303476]], "constant": 0.0, "lhs": -0.6516321612169417, "removed": [["v22", "MULTAGGR"]]}
- presolve: MULTAGGR: `repair-discovery-v1/027_syn15m__all__full` {"certified_rhs": -0.5497838302271335, "changed": [["t_v25", -0.4726661586378877, 0.0], ["t_v33", 0.0, -0.4726661586378877], ["t_v34", 0.0, -0.4726661586378877], ["t_v35", 0.0, -0.4726661586378877]], "constant": 0.0, "lhs": -0.5497838302271335, "removed": [["v25", "MULTAGGR"]]}
- SCIP: coefficient below epsilon dropped: `campaign-v2/148_star_marginal_inconsistency__all__full` {"certified_rhs": -0.031372549019607884, "changed": [["t_v0", -5.551115123125783e-17, 0.0]], "constant": 0.0, "lhs": -0.031372549019607884, "removed": []}
- SCIP: coefficient below epsilon dropped: `campaign-v2/261_star_marginal_inconsistency__all__root` {"certified_rhs": -0.031372549019607884, "changed": [["t_v0", -5.551115123125783e-17, 0.0]], "constant": 0.0, "lhs": -0.031372549019607884, "removed": []}
- SCIP: coefficient below epsilon dropped and coefficient rounded to integer: `partB/016_bayes2_50__full__s0__all` {"certified_rhs": -0.9999999999999999, "changed": [["t_v10", -3.672728543607986e-21, 0.0], ["t_v63", -0.9999999999999998, -1.0]], "constant": 0.0, "lhs": -0.9999999999999999, "removed": []}
- SCIP: coefficient below epsilon dropped and coefficient rounded to integer: `partB/016_bayes2_50__full__s0__auto` {"certified_rhs": -0.9999999999999999, "changed": [["t_v10", -3.672728543607986e-21, 0.0], ["t_v63", -0.9999999999999998, -1.0]], "constant": 0.0, "lhs": -0.9999999999999999, "removed": []}
- SCIP: coefficient rounded to integer: `repair-discovery-v1/025_genpooling_lee2__all__full` {"certified_rhs": -3.0000000000000004, "changed": [["t_v32", -1.9999999999999998, -2.0]], "constant": 0.0, "lhs": -3.0000000000000004, "removed": []}
- SCIP: coefficient rounded to integer: `partA-root/004_nous1__root__s0__all-diag` {"certified_rhs": -1.0000000000000004, "changed": [["t_v37", -1.0000000000000002, -1.0]], "constant": 0.0, "lhs": -1.0000000000000004, "removed": []}

### Stored-row losses as shares of certified rows

Violated = certified rows that passed the violation test and safe rounding (row binding + cuts added). Presolve-caused = row-binding rejections classified as presolve in the reruns, scaled to the archived count when the rerun count differs.

| Set / phase | Mode | Certified | Violated | Row binding | Share of violated | Share of certified | Presolve-caused (rerun) | Presolve-caused share of violated |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| C2 holdout full | all | 119 | 42 | 4 | 9.5% | 3.4% | 4 of 4 | 9.5% |
| C2 holdout repeat | all | 31 | 3 | 1 | 33.3% | 3.2% | 1 of 1 | 33.3% |
| C2 holdout root | all | 56 | 22 | 1 | 4.5% | 1.8% | 3 of 3 | 4.5% |
| C2 synthetic full | all | 15 | 14 | 1 | 7.1% | 6.7% | 0 of 1 | 0.0% |
| C2 synthetic root | all | 13 | 12 | 1 | 8.3% | 7.7% | 0 of 1 | 0.0% |
| Repair diagnostic full | all | 63 | 22 | 12 | 54.5% | 19.0% | 11 of 12 | 50.0% |
| Repair holdout full | all | 88 | 13 | 1 | 7.7% | 1.1% | 1 of 1 | 7.7% |
| Repair holdout full | auto | 48 | 4 | 1 | 25.0% | 2.1% | 1 of 1 | 25.0% |
| Repair holdout root | all | 83 | 12 | 1 | 8.3% | 1.2% | 1 of 1 | 8.3% |
| Repair holdout root | auto | 38 | 4 | 1 | 25.0% | 2.6% | 1 of 1 | 25.0% |
| C3 A full | all | 627 | 166 | 15 | 9.0% | 2.4% | 15 of 15 | 9.0% |
| C3 A full | auto | 303 | 40 | 3 | 7.5% | 1.0% | 3 of 3 | 7.5% |
| C3 A root | all | 209 | 55 | 5 | 9.1% | 2.4% | 5 of 5 | 9.1% |
| C3 A root | auto | 101 | 13 | 1 | 7.7% | 1.0% | 1 of 1 | 7.7% |
| C3 A root | all-diag | 1040 | 444 | 41 | 9.2% | 3.9% | 29 of 41 | 6.5% |
| C3 B full | all | 870 | 224 | 45 | 20.1% | 5.2% | 34 of 46 | 14.8% |
| C3 B full | auto | 726 | 176 | 31 | 17.6% | 4.3% | 25 of 31 | 14.2% |
| C3 B root | all | 429 | 113 | 23 | 20.4% | 5.4% | 18 of 23 | 15.9% |
| C3 B root | auto | 358 | 89 | 16 | 18.0% | 4.5% | 13 of 16 | 14.6% |
| C3 B root | all-diag | 1599 | 560 | 202 | 36.1% | 12.6% | 171 of 202 | 30.5% |
| C3 C full | all-diag-mech | 3462 | 3071 | 71 | 2.3% | 2.1% | 0 of 71 | 0.0% |
| C3 C root | all-diag-mech | 3462 | 3071 | 71 | 2.3% | 2.1% | 0 of 71 | 0.0% |
| v3d A root | all | 213 | 57 | 5 | 8.8% | 2.3% | 5 of 5 | 8.8% |
| v3d A root | auto | 104 | 15 | 1 | 6.7% | 1.0% | 1 of 1 | 6.7% |
| v3d A root | all-diag | 1071 | 444 | 41 | 9.2% | 3.8% | 29 of 41 | 6.5% |
| v3d B root | all | 441 | 117 | 22 | 18.8% | 5.0% | 18 of 22 | 15.4% |
| v3d B root | auto | 370 | 91 | 15 | 16.5% | 4.1% | 13 of 15 | 14.3% |
| v3d B root | all-diag | 1665 | 560 | 202 | 36.1% | 12.1% | 171 of 202 | 30.5% |
| v3d C full | all-diag-mech | 3804 | 3057 | 57 | 1.9% | 1.5% | 0 of 57 | 0.0% |
| v3d C full | all-diag-mech-wide | 15361 | 12308 | 308 | 2.5% | 2.0% | 0 of 308 | 0.0% |
| v3d C root | all-diag-mech | 3804 | 3057 | 57 | 1.9% | 1.5% | 0 of 57 | 0.0% |
| v3d C root | all-diag-mech-wide | 15361 | 12308 | 308 | 2.5% | 2.0% | 0 of 308 | 0.0% |

### Part B stored-row rejections by model (campaign 3)

Cells: rejections / cuts added, summed over seeds. Causes: rerun classification over all Part B reruns of the model.

| Model | full all | full auto | root all | root auto | root all-diag | Causes in reruns |
|---|---:|---:|---:|---:|---:|---|
| kall_circlespolygons_c1p12 | 6 / 0 | 6 / 0 | 3 / 0 | 3 / 0 | 127 / 25 | presolve 145 |
| bayes2_50 | 6 / 0 | 6 / 0 | 3 / 0 | 3 / 0 | 17 / 8 | SCIP 35 |
| pooling_haverly3pq | 12 / 8 | 2 / 2 | 6 / 4 | 1 / 1 | 6 / 4 | SCIP 4, presolve 23 |
| pooling_adhya4tp | 2 / 4 | 2 / 4 | 1 / 2 | 1 / 2 | 17 / 29 | SCIP 3, presolve 20 |
| sep1 | 2 / 0 | 8 / 0 | 1 / 0 | 4 / 0 | 7 / 1 | presolve 22 |
| pooling_haverly2pq | 5 / 4 | 1 / 2 | 4 / 2 | 1 / 1 | 4 / 2 | SCIP 3, presolve 12 |
| pooling_haverly3tp | 6 / 4 | 2 / 0 | 3 / 2 | 1 / 0 | 3 / 2 | presolve 15 |
| pooling_bental4tp | 0 / 6 | 4 / 8 | 0 / 3 | 2 / 4 | 7 / 9 | presolve 13 |
| bayes2_30 | 2 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 3 / 0 | SCIP 6 |
| kall_congruentcircles_c32 | 2 / 8 | 0 / 8 | 1 / 4 | 0 / 4 | 1 / 4 | presolve 4 |
| pooling_haverly1tp | 2 / 4 | 0 / 2 | 1 / 2 | 0 / 1 | 1 / 2 | presolve 4 |
| pooling_rt2tp | 0 / 2 | 0 / 2 | 0 / 1 | 0 / 1 | 4 / 46 | SCIP 4 |
| kall_congruentcircles_c61 | 0 / 11 | 0 / 12 | 0 / 6 | 0 / 5 | 1 / 15 | presolve 1 |
| kall_congruentcircles_c71 | 0 / 8 | 0 / 9 | 0 / 5 | 0 / 6 | 1 / 21 | presolve 1 |
| kall_congruentcircles_c72 | 0 / 8 | 0 / 9 | 0 / 4 | 0 / 4 | 1 / 29 | presolve 1 |
| pooling_bental4pq | 0 / 6 | 0 / 10 | 0 / 3 | 0 / 5 | 1 / 11 | SCIP 1 |
| wastewater04m2 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 1 / 21 | SCIP 1 |

## Paper tables (campaign 3 and post hoc diagnostic)

Failed support calls split by outcome (incomplete / unsupported / empty) and stored-row rejections split by cause (presolve: variable aggregated, multi-aggregated or fixed by presolve; SCIP: coefficient dropped below epsilon or snapped to an integer) come from the reruns; a dagger marks rows whose rerun totals differ from the archive (runs that reached the 1 s callback allowance). Share = stored-row rejections / (stored-row rejections + cuts added).

| Set / phase | Mode | Support calls | Certified | Failed (inc. / uns. / empty) | Insufficient violation | Rounding | Stored-row rej. (presolve / SCIP) | Share | Cuts added | Polytope / star / Bernstein / Arb |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| C3 A full | all | 684 | 627 | 57 (57 / 0 / 0) | 461 | 0 | 15 (15 / 0) | 9.0% | 151 | 112 / 0 / 3 / 36 |
| C3 A full | auto | 303 | 303 | 0 (0 / 0 / 0) | 263 | 0 | 3 (3 / 0) | 7.5% | 37 | 37 / 0 / 0 / 0 |
| C3 A root | all | 228 | 209 | 19 (19 / 0 / 0) | 154 | 0 | 5 (5 / 0) | 9.1% | 50 | 37 / 0 / 1 / 12 |
| C3 A root | auto | 101 | 101 | 0 (0 / 0 / 0) | 88 | 0 | 1 (1 / 0) | 7.7% | 12 | 12 / 0 / 0 / 0 |
| C3 A root | all-diag | 1074 | 1040 | 34 (34 / 0 / 0) | 596 | 0 | 41 (29 / 12) | 9.2% | 403 | 360 / 0 / 2 / 41 |
| C3 B full | all | 884 | 870 | 14 (14 / 0 / 0) | 646 | 0 | 45 (34 / 12)† | 20.1% | 179 | 179 / 0 / 0 / 0 |
| C3 B full | auto | 726 | 726 | 0 (0 / 0 / 0) | 550 | 0 | 31 (25 / 6) | 17.6% | 145 | 145 / 0 / 0 / 0 |
| C3 B root | all | 436 | 429 | 7 (7 / 0 / 0) | 316 | 0 | 23 (18 / 5) | 20.4% | 90 | 90 / 0 / 0 / 0 |
| C3 B root | auto | 358 | 358 | 0 (0 / 0 / 0) | 269 | 0 | 16 (13 / 3) | 18.0% | 73 | 73 / 0 / 0 / 0 |
| C3 B root | all-diag | 1618 | 1599 | 19 (9 / 10 / 0) | 1039 | 0 | 202 (171 / 31) | 36.1% | 358 | 358 / 0 / 0 / 0 |
| C3 C full | all-diag-mech | 3462 | 3462 | 0 (0 / 0 / 0) | 391 | 0 | 71 (0 / 71) | 2.3% | 3000 | 3000 / 0 / 0 / 0 |
| C3 C root | all-diag-mech | 3462 | 3462 | 0 (0 / 0 / 0) | 391 | 0 | 71 (0 / 71) | 2.3% | 3000 | 3000 / 0 / 0 / 0 |
| v3d A root | all | 232 | 213 | 19 (19 / 0 / 0) | 156 | 0 | 5 (5 / 0) | 8.8% | 52 | 39 / 0 / 1 / 12 |
| v3d A root | auto | 104 | 104 | 0 (0 / 0 / 0) | 89 | 0 | 1 (1 / 0) | 6.7% | 14 | 14 / 0 / 0 / 0 |
| v3d A root | all-diag | 1105 | 1071 | 34 (34 / 0 / 0) | 627 | 0 | 41 (29 / 12) | 9.2% | 403 | 360 / 0 / 2 / 41 |
| v3d B root | all | 450 | 441 | 9 (9 / 0 / 0) | 324 | 0 | 22 (18 / 4) | 18.8% | 95 | 95 / 0 / 0 / 0 |
| v3d B root | auto | 370 | 370 | 0 (0 / 0 / 0) | 279 | 0 | 15 (13 / 2) | 16.5% | 76 | 76 / 0 / 0 / 0 |
| v3d B root | all-diag | 1686 | 1665 | 21 (11 / 10 / 0) | 1105 | 0 | 202 (171 / 31) | 36.1% | 358 | 358 / 0 / 0 / 0 |
| v3d C full | all-diag-mech | 3804 | 3804 | 0 (0 / 0 / 0) | 747 | 0 | 57 (0 / 57) | 1.9% | 3000 | 3000 / 0 / 0 / 0 |
| v3d C full | all-diag-mech-wide | 15361 | 15361 | 0 (0 / 0 / 0) | 3053 | 0 | 308 (0 / 308) | 2.5% | 12000 | 12000 / 0 / 0 / 0 |
| v3d C root | all-diag-mech | 3804 | 3804 | 0 (0 / 0 / 0) | 747 | 0 | 57 (0 / 57) | 1.9% | 3000 | 3000 / 0 / 0 / 0 |
| v3d C root | all-diag-mech-wide | 15361 | 15361 | 0 (0 / 0 / 0) | 3053 | 0 | 308 (0 / 308) | 2.5% | 12000 | 12000 / 0 / 0 / 0 |

Time over pairs solved in every mode (full phases); SGM in seconds, shift 1 s.

| Set | Pairs | Mode | SGM total | SGM SCIP excl. callback | SGM callback | Nodes | SCIP excl. callback / baseline (median per run) |
|---|---:|---|---:|---:|---:|---:|---:|
| C2 diagnostic full | 5 | baseline | 0.706 | 0.611 | 0.000 | 2,013 | - |
| C2 diagnostic full | 5 | all | 2.246 | 0.623 | 1.401 | 2,013 | 1.067 |
| C2 diagnostic full | 5 | auto | 2.147 | 0.606 | 1.330 | 2,013 | 1.077 |
| C2 holdout full | 25 | baseline | 0.549 | 0.496 | 0.000 | 12,995 | - |
| C2 holdout full | 25 | all | 0.989 | 0.504 | 0.446 | 12,783 | 1.036 |
| C2 holdout full | 25 | auto | 0.957 | 0.522 | 0.408 | 13,608 | 1.044 |
| C2 synthetic full | 12 | baseline | 0.055 | 0.029 | 0.000 | 188 | - |
| C2 synthetic full | 12 | all | 0.068 | 0.018 | 0.026 | 186 | 0.999 |
| C2 synthetic full | 12 | auto | 0.056 | 0.025 | 0.006 | 186 | 0.949 |
| Repair diagnostic full | 4 | baseline | 0.869 | 0.766 | 0.000 | 2,009 | - |
| Repair diagnostic full | 4 | all | 0.980 | 0.605 | 0.288 | 1,299 | 0.946 |
| Repair diagnostic full | 4 | auto | 0.962 | 0.741 | 0.105 | 2,009 | 0.879 |
| Repair holdout full | 4 | baseline | 0.918 | 0.835 | 0.000 | 1,544 | - |
| Repair holdout full | 4 | all | 1.159 | 0.850 | 0.227 | 1,554 | 1.004 |
| Repair holdout full | 4 | auto | 1.162 | 0.864 | 0.200 | 1,549 | 1.055 |
| C3 A full | 80 | baseline | 1.053 | 0.986 | 0.000 | 695,712 | - |
| C3 A full | 80 | all | 1.267 | 0.988 | 0.195 | 695,959 | 1.003 |
| C3 A full | 80 | auto | 1.213 | 0.989 | 0.164 | 694,230 | 1.037 |
| C3 B full | 52 | baseline | 1.331 | 1.269 | 0.000 | 771,221 | - |
| C3 B full | 52 | all | 1.872 | 1.249 | 0.436 | 791,603 | 0.985 |
| C3 B full | 52 | auto | 1.820 | 1.228 | 0.417 | 762,375 | 0.975 |
| C3 C full | 9 | baseline | 10.270 | 10.165 | 0.000 | 452,550 | - |
| C3 C full | 9 | all-diag-mech | 6.661 | 4.692 | 1.249 | 283,144 | 0.395 |
| v3d C full | 9 | baseline | 10.277 | 10.172 | 0.000 | 452,550 | - |
| v3d C full | 9 | all-diag-mech | 2.556 | 1.234 | 1.275 | 6,653 | 0.174 |
| v3d C full | 9 | all-diag-mech-wide | 4.752 | 0.135 | 4.577 | 9 | 0.036 |
