# Review round 3, lens "numbers"

**Resolution (2026-10-04, after this review).** The Part 5S replay finished: `experiments/v5/runs/partS5/replay.json` reports `passed: true`, 47,168 of 47,168 cuts replayed (40,700 polytope, 6,468 star), coverage complete, no failed runs, and all tampering controls rejected in modes agg-star, agg-star4 and rowdir-star4, including the star-certificate mutations in agg-star. `R10_numbers_check.py <extracts> replay` then gave 274,489 recorded cuts, 92,222 distinct rows and passing replays in every part. The campaign-5 summaries were regenerated; only their replay line changed. The blocking finding about the 5S replay is closed.

Written 2026-10-04. Manuscript: `main.tex` and `sections/*.tex` as compiled in
`main.pdf`; page numbers are those of `development/draft-round3/main.txt`
(identical to the current sources). Nothing under `experiments/`, `evidence/`
(except this file) or the manuscript was changed. No SCIP or Gurobi run was
started.

## What was run (targeted checks only; no project-wide tests, no CI)

All with `/workspace/minlp-notes/code/minlp_solver_lab/.venv/bin/python`
and `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`. The three new
scripts use only the standard library and import no producer code.

| Command | Purpose | Result |
|---|---|---|
| `verification/R10_numbers_extract.py <part> <out>` (17 parts, 6 in parallel, output in a `mktemp -d` directory) | stream every `records.jsonl` of v3, v3d, v4, v5 (incl. `partS5-rerun-spike`) into compact per-record summaries; per cut: distinct-row key (model SHA-256, binary64 coefficients, orientation, rhs), dimension, certificate method, rounding flag, bound correction E, direction class | 2,518 records, 275,624 cuts, 26 s |
| `verification/R10_numbers_check.py <dir> replay c5s c5a c5b load path minlplib funnel` | replay totals and per-run agreement with every `replay.json`; distinct rows; rounding census; Part 5S (Table 5), 5C-a, 5C-b; loads; path family (Table 4 and text); MINLPLib (Table 3 and text); funnel (Table 8) | output quoted below |
| `verification/R10_numbers_tables.py <dir>` | every cell of the nine appendix tables in `B-tables.tex` (Parts 3A, 3B/4B2, 4D, path seeds 0-4 root and full, seeds 5-9 root and full, stars root and full) | **1,988 cells, 0 mismatches**; a perturbation test (three cells changed in a copy) gave exactly 3 mismatches |
| `verification/R10_numbers_ablation.py` | Table 2 (U1, U2, U3, U3p, U3s) recomputed exactly (hex constant minus rational certified value) from the per-cut entries of `ablation-uncertified.json` and `ablation-global-solve.json` | all Table 2 cells reproduced; 0 disagreements with the stored `*_material` flags |
| short read-only snippets | campaign 1-2 numbers changed since round 2 (App. G), Part 4D scan counts, Part 4S benchmark, pilot, rejection causes, spike window | see "Verified" |

The partS5 replay (`experiments/v5/runs/replay-partS5.log`) was empty and its
process (`replay_v5.py runs/partS5`, started 23:24) still running when this
review started. A bounded wait with 60 s polls (00:06 to 01:07, the 60-minute
limit) ended with the log still empty and no `partS5/replay.json` (F1).

## Verdict

The numbers are in very good shape. Every cell of Tables 1-5 and 8 and of the nine
appendix tables reproduces from the raw records, and so do the headline totals:
274,489 recorded cuts (7,498 + 30,998 + 104,771 + 131,222), 92,222 distinct
rows, the Part 5S star table (all medians and solved counts per k), the 5C-a
closures and solved counts, the 5C-b closures and distances, the eight process
timeouts and the rerun (12 and 13 solved), the campaign-5 load range, and all of
Table 2 including U3. Every existing `replay.json` (v3, v3d, v4, v5 C5a/C5b)
reports `passed: true`, its cut count equals the cuts in `records.jsonl`, and the
per-run cut counts agree for every run.

The partS5 replay had not finished when the 60-minute wait ended, so the
validity claim for Part 5S is not yet backed by a replay result (F1). The other
findings are about (i) duplicated rows in Part 5S, (ii) explanations attached to
correct numbers that are wrong or incomplete for campaign 5 (distinct rows,
funnel caption, 32n vs 64n caps), (iii) one time comparison across campaigns
against the paper's own rule, and (iv) small scope and wording issues.

## Findings

### F1 (major; blocking until resolved). The Part 5S replay had not finished, so 47,168 of the 274,489 "replayed" records have no replay result

- **Location.**
  - `sections/00-abstract.tex:18` (p. 1): "Every recorded cut passed replay".
  - `01b-results.tex:2-4` (p. 3): "All 274,489 cut records of the last three
    campaigns passed a fresh-process replay".
  - `08b-validity.tex:3-9` (p. 25): "131,222 in campaign 5, 274,489 records in
    total"; "In every part and cut mode, each of the fourteen corrupted records
    ... was rejected".
  - `08g-summary.tex:3` (p. 34).
- **Evidence.**
  - `experiments/v5/runs/replay-partS5.log` was empty at the start of this
    review (23:42). It was still empty at the end of a bounded wait with 60 s
    polls from 00:06 to 01:07, when `replay_v5.py runs/partS5` had run for 103
    minutes (8.7 GB RSS). `experiments/v5/runs/partS5/replay.json` does not
    exist.
  - All other replays pass. Campaign 5 = 84,054 (5C-b, passed, 4 tamper
    modes) + 0 (5C-a, passed) + 47,168 (5S, no result). So 47,168 records
    (17% of the total, and all 3,292 + 3,176 star-oracle cuts) are not yet
    covered.
  - The star-specific tamper controls (`star_tamper_modes`) have so far run
    only in the smoke test (`v5/smoke`). The sum 274,489 itself is right.
- **Fix.** Do not submit before `runs/replay-partS5.log` reports `"passed":
  true` with `cuts == replayed_cuts == 47168` and the star tamper controls
  rejected. If it passes, no text change is needed. If it fails or is
  incomplete, the abstract, Sections 1, 8.2 and 8.7 must change, e.g. "All
  227,321 cut records of campaigns 3 and 4 and of Parts 5C-a and 5C-b passed
  replay; the replay of the 47,168 records of Part 5S ..." (with the actual
  outcome).

### F2 (minor). The explanation of the 92,222 distinct rows is wrong for Part 5S and omits the main campaign-5 sources; the Table 8 caption repeats the error

- **Location.** `sections/08b-validity.tex:5-8` (p. 25): "These records contain
  92,222 distinct exported rows: in the constructed families the separator runs
  only at the root, so the root and full runs of an instance and mode record the
  same cuts." `sections/A-instances.tex:108-109` (Table 8 caption, p. 58): "In
  the constructed families the separator runs only at the root, so full and root
  runs have the same funnel".
- **Evidence** (`R10_numbers_check.py replay`, `funnel`).
  - The count is right: 92,222 distinct (model SHA-256, binary64 coefficients,
    rhs); campaigns 3-4 give 59,220, campaign 5 adds 33,002.
  - In the path family every full run repeats its root run's cut list (20/20
    in each part). In Part 5S it does not: only 18 of 86 root/full pairs of an
    instance and cut mode have the same list (6/30 for agg-star4, 5/30 for
    agg-star). The separator stops at its 60 s allowance, so the result depends
    on timing. Full agg-star runs: 14,349 support calls and 8,039 cuts; root
    runs: 15,187 and 8,442 (Table 8 shows the root runs).
  - Most campaign-5 duplicates have other sources. Part 5C-b has 38,941
    distinct rows in 84,054 records, because the 32n and 64n runs give identical
    cut lists on 37 of 40 instance-rule pairs. 21,238 of these rows also occur
    in Part 4C4. Part 5S has 15,299 distinct rows in 47,168 records, and 7,311 of
    the records repeat a row that the same run had already added (F3).
- **Fix.**
  - 08b: "These records contain 92,222 distinct exported rows. Rows recur for
    three reasons. In the path family the separator runs only at the root, so
    the root and full runs of an instance and mode record the same cuts. The
    32n- and 64n-cap runs of Part 5C-b coincide on 37 of 40 instance-rule pairs
    and repeat many rows of Part 4C4. In Part 5S, overlapping blocks of one star
    give the same whole-row cut several times in a run."
  - Table 8 caption: "In the path family the separator runs only at the root,
    so full and root runs have the same funnel. In Part 5S the separator stops
    at its time allowance, so the full runs differ slightly (star blocks: 14,349
    support calls and 8,039 cuts). The rows show root runs."

### F3 (minor). In Part 5S, 15% of the "cuts added" repeat a row that the same run already added

- **Location.** Table 8 (`sections/A-instances.tex:130-131`, p. 58), rows 5S
  ("8,015" and "8,442" cuts added). `sections/08f-star.tex` (p. 33) does not
  mention the repeats.
- **Evidence** (`R10_numbers_extract.py` keys; snippet in this review).
  - Within-run repeats of an identical exported row in the root runs:
    rowdir-star4 1,631 of 7,720; agg-star4 1,469 of 8,015; agg-star 611 of 8,442.
    Over all Part 5S records: 7,311 of 47,168. The other parts have at most 123
    (Part 4D root) and the path family has none.
  - Example: in `032_constrained_star_k16_n20_s2__root__s0__rowdir-star4`, the
    row `t_1_1 + 0.4375 y_1 - 1.1982 x_1_1 >= -0.95215` was added 14 times. Each
    copy came from a different four-variable block (y_1, x_1_1, x_1_2, x_1_j)
    that contains the same source row, and each was certified by its own
    support call. The run reports `repeat_skips: 0`.
  - The repeated rows are valid and pass replay. But they count toward "cuts
    added", toward the 4nk cut cap and toward the separator's time.
- **Fix.** Add to the Table 8 caption: "In Part 5S, 1,469 (four-variable
  blocks) and 611 (stars) of the added cuts repeat a row already added in the
  same run, because overlapping blocks of a star share a source row." Optionally
  add to 08f after "with either direction rule": "(about a fifth of their cuts
  repeat a row already added from an overlapping block)".

### F4 (minor). Part 5C-b: the 32n cap did bind on three instances, so "ended by itself" and "the same results" are not exact

- **Location.** `sections/08e-path.tex:178-181` (p. 32): "separation ended by
  itself after 14 to 27 callbacks, with about 26 to 30 cuts per block, ...; the
  caps of 32n and 64n gave the same results."
- **Evidence** (`R10_numbers_check.py c5b`; snippet).
  - `frozen-cap32` reached its cap (`budget_exhausted`) on three instances:
    n10_s8 with 320 cuts, n40_s8 with 1,280 and n80_s8 with 2,560.
    `frozen-cap64` went on to 328, 1,284 and 2,602 cuts. The root bounds
    differ by at most 3.8e-5. On the other 37 of 40 pairs the cut lists are
    identical.
  - With the 64n cap, no run reached its cap or allowance, and separation
    ended after 14 to 27 callbacks (as stated).
  - Cuts per block: median 28.7 (remainder) and 26.3 (whole row), range
    19.9-32.8. "About 26 to 30" matches the two means (28.7 and 26.0), not the
    spread across runs.
  - The 1e-4-unit distances and the "within 8e-4" claim reproduce (maximum
    7.70e-4).
- **Fix.** "With the cap $64n$ and up to 40 callbacks (Part~5C-b), separation
  ended by itself after 14 to 27 callbacks, with a median of 29 (remainder) and
  26 (whole-row) cuts per block, and the root bound came within $8\cdot10^{-4}$
  of the block closure on every instance. The cap $32n$ gave identical runs,
  except on three instances where the remainder mode reached it; there the
  root bounds differed by less than $4\cdot10^{-5}$."

### F5 (minor). "SCIP-nolocks ... faster than the cut modes" compares times across campaigns, against the paper's own rule; "96 to 98%" is a range of medians

- **Location.**
  - `sections/08e-path.tex:166-169` (p. 32): "SCIP-nolocks, however, also
    solved all 20 instances, in 0.1 to 169 s and faster than the cut modes
    (shifted geometric means 2.0 s against 12 to 13 s), with a root bound that
    closed 96 to 98% of SCIP's root gap."
  - The same comparison: `01b-results.tex:26` (p. 3), "but so did SCIP
    without its presolve step, faster"; `08g-summary.tex:17` (p. 34);
    `09-conclusions.tex:45`.
  - The rule: `08a-setup.tex` (p. 24), "We compare times only within these
    paired runs of one part ... solved counts and times are not paired across
    campaigns, and we say so where it matters."
- **Evidence** (`R10_numbers_check.py c5a`, `load`).
  - SCIP-nolocks ran in Part 5C-a (campaign 5, one-minute load 4.9-8.6). The
    cut modes ran in Part 4C4 (campaign 4, load 1.9-14.8, 5th-95th percentile
    6.6-13.9).
  - Shifted geometric means: 2.02 s against 12.96 s (`frozen-wide`) and
    12.20 s (`rowdir-wide`). A factor of six is far beyond load effects, so the
    conclusion holds, but the sentence does not say that the times are not
    paired.
  - The root closures are 0.980, 0.980, 0.972 and 0.959 as medians per n.
    Single instances range from 0.947 to 0.992.
- **Fix** (08e): "SCIP-nolocks (Part 5C-a, run in campaign 5) also solved all
  20 instances, in 0.1 to 169 s. Its shifted geometric mean was 2.0 s, against
  12 to 13 s for the cut modes in Part 4C4. These times are not paired, but the
  factor of six is far larger than the effect of the host load. Its root bound
  closed a median of 96 to 98% of SCIP's root gap (95 to 99% per instance)."

### F6 (minor). Stars: "less than two percentage points" holds only for medians

- **Location.** `sections/08f-star.tex:70-72` (p. 33): "Blocks of four
  variables added less than two percentage points to SCIP's root bound, with
  either direction rule".
- **Evidence** (`R10_numbers_check.py c5s`).
  - Medians: the per-k medians minus SCIP's are +0.15, +0.58 and -0.41 points
    (rowdir-star4) and +0.90, +1.84 and +0.92 points (agg-star4).
  - Single instances: from -2.13 to +4.80 points (rowdir-star4) and from
    -2.11 to +6.69 points (agg-star4). More than 2 points on 7 and 10 of the 30
    instances. Example: k4 n10 s0, SCIP 0.9607 against agg-star4 0.9952
    (Table 16).
- **Fix.** "Blocks of four variables changed SCIP's median root bound by less
  than two percentage points with either direction rule (on single instances by
  -2 to +7 points): a block that ..."

### F7 (minor). Part 5S: "its bound was already optimal", "its whole allowance of 60 s" and "stopped at the hard limit of 360 s" need qualifying because of the load spike

- **Location.** `sections/08f-star.tex:79-92` (pp. 33-34); Table 17 caption
  (`sections/B-tables.tex:382`, p. 67): "the 8 runs whose worker process was
  stopped at the hard limit of 360 s".
- **Evidence** (`R10_numbers_check.py c5s`; spike snippet).
  - Of the 11 unsolved agg-star full runs, 10 have a final dual bound equal to
    the optimum (relative difference at most 1.8e-15). The eleventh
    (k16_n10_s3) is a process timeout with no bound.
  - During the spike, `019_constrained_star_k4_n20_s4__full__s0__agg-star`
    spent 203.6 s in the separator, 168.4 s of it in direction LPs, against the
    60 s allowance. Two other runs were charged more than the 300 s budget:
    agg-star4 k16_n10_s3 330.2 s and agg-star k16_n10_s4 305.2 s, shown as
    "t 330.2" and "t 305.2" in Table 17.
  - The timed-out workers ended after 360.0 to 554.4 s of wall time. Three of
    them ran 389, 400 and 554 s.
  - Seven further full runs overlapped the spike (02:39-02:52 UTC), ended
    unsolved and were not rerun. agg-star: k16_n10_s2 and k16_n10_s4.
    agg-star4: k8_n10_s1 and k16_n10_s3. SCIP: k8_n10_s2 and k16_n10_s3.
    SCIP-nolocks: k16_n10_s4. None of them can change the ranking, because SCIP
    could reach at most 14 and the star mode only gains.
- **Fix.**
  - 08f: "Where it did not solve an instance, its bound was already optimal
    (in all 10 such runs that recorded a bound) ... The separator also used its
    whole allowance of 60 s (204 s in one run during the load spike below) ...
    A rerun of these eight runs ... would not change. Seven further runs that
    overlapped the spike reached the time limit and were not rerun; at most two
    of them, both of SCIP, could change a count of a SCIP setting."
  - Table 17 caption: "stopped after exceeding the hard limit of 360 s (at 360
    to 554 s of wall time) during a load spike".

### F8 (minor). The 1,135 cuts of the out-of-protocol rerun were not replayed

- **Location.** `sections/08f-star.tex:88-92` (p. 34) describes the rerun.
  `00-abstract.tex:18` (p. 1): "Every recorded cut passed replay".
  `08b-validity.tex:3` (p. 25): "Every recorded cut of campaigns 3 to 5 passed
  replay". `08g-summary.tex:3` (p. 34).
- **Evidence.** `experiments/v5/runs/partS5-rerun-spike` has 8 records and
  1,135 cuts (rowdir-star4 267 and 251, agg-star 313, agg-star4 304). It has no
  `replay.json` and no replay log. The 274,489 total does not include it. Its
  own cut lists also contain 155 within-run repeats (F3).
- **Fix.** Replay it (`replay_v5.py runs/partS5-rerun-spike`) and say so.
  Otherwise add to 08f: "The rerun's 1,135 cuts are not among the 274,489
  replayed records", and in the abstract write "Every cut recorded under the
  protocols passed replay".

### F9 (minor). The rounding shares are for campaigns 3 and 4 only, but the paragraph covers campaigns 3 to 5

- **Location.** `sections/08b-validity.tex:18-21` (p. 26): "Binary64 rounding
  changed at least one coefficient in 13.5% of the exported rows on the
  MINLPLib models and in 92.5% on the path family; the bound correction ... was
  at most 8.5e-16".
- **Evidence** (`R10_numbers_check.py replay`).
  - MINLPLib 710 of 5,267 (13.5%) and path family 127,678 of 138,000 (92.5%)
    are the campaign-3 and 4 rows (`ablation-final-summary.md`, export census).
  - With Part 5C-b, the path family has 206,254 of 222,054 (92.9%); 5C-b alone
    has 93.5%.
  - The star family (Part 5S) has 24,269 of 47,168 (51.5%) and is not
    mentioned.
  - max |E| = 8.48e-16 holds for all campaigns (star family 3.35e-16).
    `row_rounding_rejections` is 0 in every part.
- **Fix.** "Binary64 rounding changed at least one coefficient in 13.5% of the
  exported rows on the MINLPLib models, in 92.9% on the path family and in
  51.5% on the star family; the bound correction ... was at most
  $8.5\cdot10^{-16}$ ..."

### F10 (minor). The 151 excluded Bernstein/ball-arithmetic cuts are not all in Part 3A

- **Location.** `sections/08b-validity.tex:59-60` (p. 26): "the 151 cuts
  certified by Bernstein or ball-arithmetic lower bounds, all in Part 3A, are
  excluded".
- **Evidence** (`R10_numbers_ablation.py`; snippet). The 151 come from
  `v3/partA-root` (56), `v3/partA-full` (39) and `v3d/partA-root-rowdir` (56).
  The last of these is Part 3P.
- **Fix.** "..., all on the models of Part 3A (95 in Part 3A and 56 in its
  Part 3P root runs), are excluded".

### F11 (suggestion). Part 4D: discovery stopped on 12 models in the root runs, on 11 in the full runs

- **Location.** `sections/08c-minlplib.tex:116-118` (p. 28); `01b-results.tex:
  15` (p. 3).
- **Evidence** (snippet). With mode `all`, `discovery_incomplete` holds on the
  12 models whose scan discovery took 1.0-7.7 s in the root runs, and on 11 of
  them in the full runs. `multiplants_mtg6` (scan 1.31 s) completed discovery
  in its full run. Table 3, beside which the sentence stands, shows full runs.
- **Fix.** "In mode all the separator stopped during block discovery on 12 of
  the 20 models in the root runs (11 in the full runs), exactly those ...".

### F12 (suggestion). The seed-to-seed range in Part 3A uses only seed 1 against seed 0

- **Location.** `sections/08c-minlplib.tex:78-80` (p. 28): "baseline runs of
  Part 3A that differ only in SCIP's seed differed per run by a median factor of
  1.03 (range 0.61 to 1.92)".
- **Evidence** (snippet; 26-27 models solved by both seeds of a pair):
  - seed 1/0: median 1.032, range 0.61-1.92;
  - seed 2/0: median 1.044, range 0.36-2.38;
  - seed 2/1: median 0.955, range 0.59-1.79.
- **Fix.** "... by a median factor of 1.03 (seed 1 against seed 0; range 0.36
  to 2.38 over all seed pairs)". This strengthens the argument.

### F13 (suggestion). Section 8.1 omits the 300 s root budget of Part 5C-b

- **Location.** `sections/08a-setup.tex:44-46` (p. 24): "root runs have a node
  limit of one and a budget of 60 s (Parts 3A, 3B, 4B2) or 120 s (path family,
  Parts 4D and 5S)".
- **Evidence.** The Part 5C-b records have `time_limit` 300 and `node_limit` 1
  (80 of 80). Table 14's caption states this, Section 8.1 does not.
- **Fix.** "... or 120 s (path family, Parts 4D and 5S; 300 s with up to 40
  callbacks in Part 5C-b)."

## Verified (no change needed)

Reproduced from the raw records (values in parentheses are the recomputed ones):

- **Replay.** All 15 existing `replay.json`: `passed: true`, `cuts ==
  replayed_cuts ==` cuts in `records.jsonl`, per-run counts equal, no failed run,
  14 tamper flags all `true`, no omitted run with cuts (the 60 omitted runs are
  Gurobi runs without cuts). Totals 7,498 / 30,998 / 104,771; campaign 5 =
  84,054 (5C-b) + 0 (5C-a) + 47,168 (5S records) = 131,222; total 274,489.
- **Distinct rows** 92,222 (c3-4: 59,220; c5: 54,240, of which 33,002 new).
- **Rounding census** 710/5,267 = 13.5% (MINLPLib, c3-4), 127,678/138,000 =
  92.5% (path, c3-4); max |E| = 8.48e-16 over all campaigns (star 3.35e-16).
- **Incumbents.** The only failed primal check in campaigns 3-5 is the Part 4D
  SCIP-extra root run of `waternd2` (discrepancy 0.342).
- **Table 2.** U1 1,969 (12) / 405 (7); U2 230 (4) / 132 (2); U3 4 (1, `nvs02`,
  one distinct cut, excess 1.78e-4) / 0; path U1 976 (60) / 506 (58) / 404; U2
  73 (37) / 27 (19) / 13; U3 0 / 0 / 0; U3p wrong on 3 path cuts; U3s wrong on the
  same 4 nvs02 cuts; 5,116 cuts / 47 models; 1,000 path cuts / 60 instances /
  995 distinct; 38.5%, 4.5%, 7.3%, 40.4%.
- **Table 3** (all cells), "15-20%" and "37-41%" slower, median ratios 1.34/1.29
  and 2.66/2.55, node sums within 2.64%, cuts on 11/5 (3A) and 20 (3B) models,
  better/worse 2/4, 3/3, 2/0 (`kall_circles_c8a`), 4D 5/1, 4/0, 7/7.
- **Section 8.3 text.** Root effects (ex3_1_4 -6 to -5.79 / -5.69,
  haverly2pq -617.7 to -857.1), all-diag 403 and 358 cuts, 3P: 10 of 180 runs
  changed cut counts, no root bound; 3B stored-row shares 20.4% and 36.1%;
  c1p12 127 of 152, then 104 cuts; 4B2 5.3% and 9.5%, 3 and 6 models improved,
  haverly1tp worse, noaggr baseline weaker on 6; all-diag-rowdir identical cut
  lists; SCIP-extra 12 better / sep1 worse, 5 closed, 2 above 95%, 13 vs 8 at
  the root, interminor 21, intersection 26, eccuts 0; 4D: 12 discovery stops
  (root runs; scan 1.0-7.7 s), 6 of 8 no cut, 11 of 25 rejected, caps 6 of 8 and
  10 of 20, 891 cuts on 13 models, mtg1c +3.9%, five worse by at most 3.06%,
  SCIP-extra 8 better / 3 worse without the flagged run; selection 322 / 301 /
  8 / 9 / 4 / 85 / 27 / 58.
- **Table 8 and Section 8.4.** Every funnel cell; 65.0-85.6% below threshold;
  307 of 313 failures on `kriging_peaks-full100`; dropped-coefficient
  rejections at most 2.9% of violated rows on the constructed families; SCIP-excl
  medians 0.958-1.005; 0.548 s callback per run vs 0.160 s median SCIP time;
  70% / 85% shares.
- **Table 4** (all cells, incl. borderline 0.5995 -> 0.600, 0.98147 -> 0.981,
  block closure n=20 0.999946 -> 1.000; 5C-b 0.999739/0.999403/0.999723/0.999461
  and 0.999661/0.999368/0.999546/0.999425) and the Section 8.5 text: -0.0354 to
  -0.0131 per copy; minor cuts 40/40 and 80/80 vs 0/80; Gurobi 61-113% and
  53-121%; 3C 9 same, SGM 6.66 vs 10.27; 3P 10 and 20 (18 at root); 4C2 above
  pair hulls on 7; all four configurations at the cap; 4C3 within 2e-7, 3.2-33.2
  s, median 1 node, max 38, ratios up to 3.44 and 3.7-19.6x faster, own time
  3.7%, 96.0% in the separator; 4C4 3.2-133.7 s, 10/13/6, median ratios 3.51 and
  3.25, root medians 0.953 and 0.986, LP shares 99.88% and 93.63%, sum of minima
  below SCIP on 10 of 20; Gurobi reformulation under 1 s on 19 of 20; block
  closure = optimum on 13, max 6.47e-4; 16n cap reached 20/20; whole-row
  distance at n=80 0.0158-0.0288; 5C-a 0.92 (all n), 0.980/0.980/0.972/0.959,
  10 and 20 solved, 0.0966-169 s, SGM 2.02 vs 12.96/12.20; 5C-b distance max
  7.7e-4, callbacks 14-27.
- **Table 5 and Section 8.6.** All medians and solved counts; agg-star root
  within 7.0e-7 relative; star-oracle calls 4,650 (750/1,350/2,550 on 5/9/17
  variables), median 7.76 ms, max 0.195 s; polytope medians 78.6/114.3/78.8 ms;
  k16 n20 incumbents 7.04-9.70% above; Gurobi incumbents within 1.6e-4, bound up
  to 1.35% below; 8 timeouts (3 SCIP, 1 Gurobi, 4 separator) between 02:35:39
  and 02:48:27 (12.8 min), peak load 125.9; rerun solved 2 SCIP + 1 rowdir-star4.
  Part 4S: medians 1.28 ms / 11.8 ms / 0.165 s / 2.07 s and 6.0 ms / 0.427 s /
  29.0 s, 94 and 78 bits.
- **Loads.** Campaign 3 14.1-20.6; 3P 2.1-20.7; campaign 4 start loads p5 2.4,
  p95 9.0, max 14.85 (4C4); campaign 5 1.1-19.9 outside the spike. At most six
  active runs in every part; 3P overlapped the last 28.2 min of 3A; all 100
  baseline root bounds of 3P equal those of campaign 3.
- **Appendix G** (numbers changed since round 2): waterno2_06 control bound
  21.17; campaign 1 SGM 0.262 / 0.406 / 0.573 / 0.463, genpooling_lee2 5.61 /
  4.89 s; campaign 2 SGM 0.549 / 0.989 / 0.957, more than 10% slower on 21 and
  21 (both 19) of 25. The rest of Appendix G is unchanged since round 2, where
  it was audited (418/418).
- **Appendix H.** All 1,988 table cells; Table 7 limits of the 5C-b modes equal
  the recorded configs (e.g. 2,560 / 640 / 40 / 6,400 / 150 s at n=40 for
  `frozen-cap64`).
