# Review round 2: `scip-set-selection/note.md`

Reviewer: independent confirming research agent. I did not write the note,
the patch or the stream code, and I did not write review round 1.
Date: 2026-10-04 (local 2026-10-03 evening).

Scope:

- The revised note, with emphasis on the M1 rework (Sections 2, 3, 7, 7.4
  and the Summary).
- The stock build and the new logs in `logs/full_stock/` and
  `logs/stock_checks_r1/`.
- The round-1 minor items m1–m7.

I did not edit the note or the stream code, changed no git state and
started no benchmark. Review code is in `reviews/r2-code/` and outputs are in
`reviews/r2-logs/`. My only SCIP runs were 16 short single-instance runs,
described under check 6.

## Verdict

**Major problems: one new major issue, limited to how the stock rerun is
interpreted. Everything else is verified or needs only minor fixes.**

- **The stock build is verified.** It is unpatched SCIP 10.0.3 with the
  benchmark configuration. Its settings match `logs/full/`. The eight
  retried runs were handled without bias.
- **All numbers in Section 7.4 match my independent parser exactly.** This
  covers solved counts, CPU and node shifted geometric means (sgm), common
  subsets, paired ratios, p-values, solved-set differences, signature
  counts and root identity.
- **m1–m7 are resolved.** For m6 the author is right: the round-1 figure of
  0.18 ms per search mixed two populations.
- **The no-go recommendation for `corner` and `eff` stands.** It rests on
  root results and on rule-versus-rule comparisons made in one batch, and
  both are unaffected.

The major issue: the note reads the cross-batch difference between stock
and `off` as a "modest observed benefit" of SCIP's point rule. The note's
own logs show that the archived batch, which contains both `off` and the
patched runs, was much slower in CPU time. Identical search paths took a
geometric mean of 15% more CPU time there, and 30–50% more on runs over
1 s. Same-load reruns show that the patch itself adds no measurable CPU
cost. The whole stock-versus-`off` CPU advantage, and the one "genuine"
extra completion (`gabriel01`, seed 2), are therefore explained by batch
speed. They are not benefits of the point rule. The note attributes the
patched-versus-stock CPU gap to "instrumentation distortion", which these
reruns contradict.

## Status of round-1 issues

| Issue | Status | Evidence |
|---|---|---|
| M1 capture / stock comparison | **Partly resolved.** The fairness statements in Sections 2, 3, 7.1–7.3 and the Summary are corrected, and the stock build and rerun are sound. The interpretation of the stock rerun is wrong (N1). | Checks 1–6 |
| m1 `st_glmp_fp2` rows | Resolved | 73/73 rows have a positive helper coefficient; 73/73 were reported before the first incumbent; minimum slack 0.01754381880081 (`r2-logs/glmp_rows.log`). The supplied point has objective 7.6275; `.solu` gives 7.3445454180. The five distinct secants have domains between 6.3414 and 6.4806; all exclude 5.65. |
| m2 `kall_congruentcircles_c52` | Resolved | `r1-logs/kall_c52.eff.s2.log`: constraint violation 9.51357e-07, LP rows 1.34291e-08, bounds 9.73643e-10, "solution is feasible in original problem". |
| m3 median-gain range | Resolved | `checks_summary.md` rule-1 medians run from 1.049 to 1.651. |
| m4 search outputs | Resolved | The Section 4.4 table matches all seven `search_opt_*.out` files, including the `tln7` traceback on an empty array and `best_outside_halfcircle = 0` everywhere. |
| m5 load facts | Resolved for Section 7.3 | Log mtimes: full runs 19:37–21:35, debug runs 20:10–21:34. My wall/CPU medians are 1.2207 / 1.2054 / 1.2125 / 1.2052. See N1 for how Section 7.4 uses wall/CPU. |
| m6 populations and per-search cost | Resolved; the author is right | See check 7. |
| m7 corner-bound caveat | Resolved | Section 2, item 4 now qualifies "stored `z_K`" and points to Section 4.4 and `multiround`. |
| o1–o3 | Resolved | Sections 8.1 and 5, and the cross-reference to the sibling stream. |

## New issues

### Major

**N1. The stock-versus-`off` "benefit" and the patched-versus-stock CPU gap are batch-speed effects, not effects of cuts or capture.**

Location:

- Summary, paragraphs 3–4: "modest observed benefits", "CPU mean 1.926 s
  vs 2.148 s off", "The patch-vs-stock difference is material … CPU means
  17.979 vs 15.962 s".
- Section 7.4: "the true enabling comparison", "The genuine additional
  completion is `gabriel01`, seed 2", "shows a modest observed solve benefit
  and lower measured CPU time", "The original patched comparison
  understated that result", "Patched point rule vs stock: observed
  instrumentation distortion", and the argument that the median wall/CPU
  ratio of 1.2047 is "comparable".
- Revision section, M1 bullet: "The stock enabling comparison is more
  favourable than the original patched comparison."

Evidence:

1. **Identical paths, different CPU.** On 69 pairs, stock and patched-scip
   both solve with identical node and LP-iteration signatures, so the search
   is the same. Patched/stock shifted CPU ratio by stock CPU time
   (`r2-logs/batch_effect.log`):

   | Stock CPU | Pairs | Patched/stock ratio |
   |---|---|---|
   | < 1 s | 41 | 1.04 |
   | 1–10 s | 19 | 1.30 |
   | ≥ 10 s | 9 | 1.44 |
   | All | 69 | 1.154 |

   The note itself reports the result: patched vs stock has a CPU ratio of
   1.18, p = 2·10^-7, while nodes differ on only 3 of 37 instances.
2. **Same-load reruns show no patch cost.** I ran four instances (seed 1),
   with four processes each: {patched, stock} × {`off`, `scip`}, run
   concurrently (`r2-logs/sameload/`, load about 4). Every pair reproduced
   the archived node count. Patched/stock CPU ratios were 0.996–1.022 with
   cuts on and 0.97–0.99 with cuts off. The archived batch was slower for
   `off` as well, which has no rows to capture:

   | Instance | Archived `off` CPU (s) | Same-load `off` CPU (s) | Ratio |
   |---|---|---|---|
   | kall_diffcircles_5b | 5.61 | 3.96 | 1.42 |
   | nvs24 | 10.87 | 7.44 | 1.46 |
   | crudeoil_pooling_ct2 | 26.34 | 19.03 | 1.38 |
   | pointpack08 | 52.49 | 32.98 | 1.59 |

   The stock batch ran at roughly the same-load speed: 5.61, 9.27, 15.45
   and 48.50 s with cuts on, against 5.23–44.89 s now.
3. **Cross-batch comparison reverses the sign.** Take the 68 identical-path
   pairs that `off` also solves:
   - Cross-batch, stock/`off` = 0.954, so stock looks faster.
   - Same batch, patched/`off` = 1.103.

   Check 2 shows that patched and stock cost the same CPU on these paths.
   The same-batch figure is therefore the right estimate. On these pairs,
   enabling the cuts costs about 10% CPU against `off`; it does not save
   CPU.
4. **`gabriel01`, seed 2.** Stock and patched-scip share the first 103
   display rows, up to node 6600. That prefix took 29.0 s in the stock batch
   and 44.6 s in the archived batch, 1.54 times as long
   (`r2-logs/path_prefix.log`). Stock's 256.83 s solve would correspond to
   about 395 s in the archived batch, beyond the 300 s limit. This
   completion depends on batch speed, so it is not a genuine extra solve.
   Once `ex5_4_2`, seed 1 (off's numerical failure) is also set aside, no
   solve-count difference between stock and `off` remains that can be
   attributed to the cuts.
5. **The solve-count differences between patched and stock remain path
   effects.**
   - `blend852`: the paths diverge after 38 rows. Patched times out at
     99192 and 101835 nodes; stock needs only 84509 and 96144 nodes.
   - `tln7`, seed 1: patched solves at 308290 nodes; stock is still open at
     584309 nodes.

   These are real capture-induced divergences. Their CPU timings, however,
   are mixed with batch speed.
6. **Wall/CPU ratios do not show that conditions matched.** The two batches
   have the same median wall/CPU ratio (about 1.20) but differ by 15–50% in
   user CPU on identical paths. Wall/CPU measures scheduling delay, not CPU
   inflation from cache or memory contention.

Required change:

- Withdraw the following claims, or restate each as "not established":
  - "modest observed benefit(s)" and "lower measured CPU time" for the
    point rule;
  - "the true enabling comparison" as the heading for a cross-batch
    comparison;
  - "the genuine additional completion" for `gabriel01`, seed 2;
  - "The stock enabling comparison is more favourable";
  - "instrumentation distortion" as the explanation of the CPU gap.
- Report the identical-path batch effect (item 1) and the same-load
  finding (item 2). The patch-vs-stock difference that can be attributed to
  capture is the path divergence: 2 vs 1 load-insensitive solve differences
  and 5 of 74 changed signatures. The 12–18% CPU gap is batch speed.
- State the defensible conclusion for stock SCIP. The rerun gives no
  evidence that enabling the point rule helps or hurts full solves. The
  same-batch evidence on shared paths shows a CPU cost of about 10%. The
  solve counts differ only by `off`'s numerical failure and one
  load-sensitive completion.
- Describe a valid stock enabling comparison: run `off` and stock-`scip` in
  the same batch, interleaved. With cuts off, the two binaries behave
  identically, so either binary works for `off`. This is a recommendation;
  the change to the note does not require running it.
- In the Summary, also replace "CPU mean" and "node means" with "shifted
  geometric mean".

### Minor

**N2. Node-count definition.** Sections 7.1 and 7.4. The node means use
the first number on SCIP's "Solving Nodes" line. After a restart, that is
the node count of the last run only. Using total nodes over all runs
changes the sgms by at most 0.5 (for example, `off` seed 1: 4739.2 →
4739.4). Name the definition in one clause.

## Checks run, with outcomes

All commands ran with `OMP_NUM_THREADS=1` and under `timeout`, with at most
four concurrent processes. All parsing code is my own and imports nothing
from the stream code.

1. **Stock build identity** (`r2-code/build_identity.sh` →
   `r2-logs/build_identity.log`).
   - The tarball sha256 matches Section 10.
   - `diff -rq` of the fresh tarball against the build source tree finds
     only `scip/src/scip/nlhdlr_quadratic.c`. The stock handler source is
     byte-identical to the tarball's.
   - The stock link command has the same 464 arguments as `build-lapack`'s
     `link.txt`. Only the handler object and the output path differ.
   - No object or static library in `build-lapack` is newer than
     `bin/scip`.
   - `ldd` output is identical for the two binaries.
   - The stock handler object disassembles to the same instructions as
     review round 1's independently built pristine object. The objects
     differ only in embedded source paths.
   - **Outcome:** the stock binary is unpatched SCIP 10.0.3 with the
     benchmark configuration.
2. **Identity checks and settings.**
   - `off` checks: `nvs17` and `st_glmp_fp2`, seed 1, give display rows
     identical to the archived logs. `ex5_4_2`, seed 1, gives the same LP
     3040 / node 3643 failure.
   - `tln7` at 2000 nodes: stock 14.1602941176471 / 16.1, patched
     13.9974022605189 / 17.1, as stated.
   - All 120 stock logs and all 120 archived `scip` logs set exactly:
     `memory 6000`, `time 300`, `clocktype 1`, `useintersectioncuts TRUE`,
     the permutation seed, and the table. The first 30 lines of `nvs17`,
     seed 1 are identical between batches (version, GitHash, libraries).
   - SCIP's `clock.c` uses `tms_utime`, as the note says.
3. **Retry handling** (`r2-code/retry_check.py` →
   `r2-logs/retry_check.log`).
   - The first driver pass has 112 valid runs and 8 runs with return code
     124 at 720 s wall: `blend852`, `ex5_2_5`, `ex8_3_2` and `ex8_3_9`,
     both seeds. These are all of the failures, and only they were retried.
     No successful run was replaced.
   - Every retry repeats the killed attempt's display rows exactly, so the
     search is deterministic.
   - CPU time at the attempt's last node was 2–6% lower in the retry.
   - Only `blend852` depends on the retry, and it finishes at 172.6 s, far
     from the limit.
   - **Outcome:** no selection bias.
4. **Tables recomputed** (`r2-code/recompute_stock.py` →
   `r2-logs/recompute_stock_lastnodes.md`).
   - Run outcomes:
     - stock: 120 runs, 77 optimal, 43 time limit, all return code 0;
     - archived: 480 runs, 302 optimal, 177 time limit, 1 return code 255.
   - Every Section 7.1 and 7.4 number matches, including:
     - per-seed and pooled sgms;
     - 36 / 37 / 73 common pairs;
     - all-pair and common ratios 0.9066 / 0.9296 / 0.9960 and
       1.1189 / 1.1832 / 1.0088;
     - p-values 0.003315 / 0.007924 / 0.1207 and 1.666e-7 / 2.355e-7;
     - pair-solved values 75 / 0.9236 / 0.005131 and 74 / 1.1807;
     - the exclusion of `ex5_4_2`, seed 1: 76 vs 75, 16.361 vs 17.277,
       ratio 0.9499, p = 0.003473;
     - solved-set differences;
     - 5 of 74 and 51 of 120 signature differences;
     - 117 pairs with equal first-LP and root dual values.
   - Per seed, stock vs `off` CPU ratios are 0.876 (p = 0.054) and 0.939
     (p = 0.012). These are cross-batch numbers (N1).
   - The stock reference check (`r2-code/stock_reference.py`, objective
     sense from `instancedata.csv`) finds no dual-bound exclusion and no
     optimum mismatch.
5. **Load.**
   - `driver.jsonl`: 338 samples of the one-minute load, from 5.32 to
     125.85, median 14.8.
   - The eight attempts killed during the spike ran at about 20% CPU share.
   - Stock wall/CPU median is 1.2047 (67 runs over 5 s).
   - The note's load statements are accurate. Its inference about
     comparability is not (N1).
6. **Batch effect and same-load runs**
   (`r2-code/batch_effect.py`, `r2-code/path_prefix.py`,
   `r2-code/sameload_timing.sh` → `r2-logs/batch_effect.log`,
   `path_prefix.log`, `sameload/`, `sameload_summary.log`).
   - 16 single-instance runs: kall_diffcircles_5b, nvs24,
     crudeoil_pooling_ct2 and pointpack08, seed 1, each with 4 concurrent
     processes. Results under N1.
   - No process remains.
7. **m6 per-search cost** (`r2-code/search_cost.py` →
   `r2-logs/search_cost.log`).
   - Seed-0 root logs: 305 instances are complete in all seven settings.
     Excluding root-solved instances, which have no root dual, leaves
     exactly the note's 251.
   - On those 251:

     | Rule | Searches | Generated cuts | Search time (s) | ms per search | ms per generated cut |
     |---|---|---|---|---|---|
     | `corner` | 80350 | 95657 | 40.77 | 0.507 | 0.426 |
     | `eff` | 79785 | 95131 | 43.87 | 0.550 | 0.461 |

   - There are 0.84 searches per generated cut, not 2.4.
   - Over all 347 root logs:
     - `corner`: 228135 searches, 173928 changed;
     - `eff`: 233699 searches, 184473 changed;
     - 267 instances with a change for each rule.
   - Round 1's 0.18 ms is the 251-instance time divided by the all-log
     searches: 0.179 / 0.188 ms. **The author is right.** Over all logs
     the per-search cost is higher: 1.08 / 1.23 ms.
8. **m1 spot check** (`r2-code/glmp_rows.py`): see the status table.
   I also recovered the secant domains from the coefficients myself.
9. **m2–m5 and m7**: checked against the raw logs and files listed in the
   status table.
10. **Text review.**
    - I read the full revised note.
    - Sections 2, 3 and 7.1–7.3 now correctly separate patched and stock
      comparisons. "`off` is stock-equivalent on the checked instances" is
      accurate.
    - The Summary's figures match the body. Its interpretation of the stock
      rerun does not (N1).
    - The timeline in Section 7.4 matches `driver.jsonl`: 02:36:40–03:20:59
      and 03:21:15–03:28:45 UTC.
    - No other new error found.

Temporary files are in `/tmp/r2chk`, outside the stream. The extracted
tarball was deleted, and `build_identity.sh` recreates it.
