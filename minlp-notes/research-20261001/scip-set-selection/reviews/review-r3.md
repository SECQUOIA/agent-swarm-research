# Review round 3 (confirmation): `scip-set-selection/note.md`

Reviewer: independent confirming research agent. I did not write the note,
the patch, the stream code or the earlier reviews.
Date: 2026-10-04.

Scope: the fixes for N1 and N2 from
[review round 2](review-r2.md), the "Revision after review round 2" entry,
and the status lines just edited by the closing-record agent. I read the full
`git diff -- research-20261001/scip-set-selection/note.md` and the full
current note. The committed baseline is an early draft, so the diff contains
the whole round-1 and round-2 work. I reviewed it as a whole.

I did not edit the note or the stream code, change git state, or run a
solver or benchmark. Review code: [`r3-code/recheck.py`](r3-code/recheck.py).
Output: [`r3-logs/recheck.log`](r3-logs/recheck.log).

## Verdict

**Verified.** N1 and N2 are fixed correctly and completely. Every new
number matches my own recomputation from the raw logs. I found no new
error. The only follow-up is administrative: the status lines that say the
revision "has not been re-reviewed" should now cite this review (A1 below).

## Status of round-2 issues

| Issue | Status | Evidence |
|---|---|---|
| N1: stock-vs-`off` "benefit", `gabriel01` "genuine" completion, "instrumentation distortion" | **Resolved** | Text checks 1–3 and numeric checks 4–8 below |
| N2: node-count definition | **Resolved** | Check 9 |

### N1: where each withdrawn claim went

- **Summary.**
  - The stock rerun is now reported as cross-batch. The note says it shows
    neither help nor harm for full solves.
  - `gabriel01`, seed 2 is described as sensitive to batch speed, with the
    395 s estimate.
  - The within-batch ratio 1.103 on 68 pairs is the only timing evidence
    the note calls like-for-like. Its subset limit is stated: it "does not
    answer the full-solve enabling question".
  - The patched/stock gap is attributed to batch speed (1.1544 on 69
    pairs; same-load runs within ±3%).
  - Row capture is credited only with the `blend852` and `tln7` path
    outcomes and 5 of 74 changed signatures.
  - The Summary uses "shifted geometric mean" for both CPU and nodes.
  - An interleaved stock-off vs stock-scip run is recommended and marked
    as not run.
- **Section 2.** Rule 0 is defined as the patched point rule with capture.
  `stock-scip` is defined separately. Nothing claims a benefit.
- **Section 3.** It states that capture changes tree search. "On equal
  terms" refers only to rule-vs-rule comparisons, which is correct.
- **Section 7 intro and 7.1–7.3.** Original cut-on vs `off` comparisons are
  described as combining cuts and capture. The 7.3 status no longer claims a
  stock-SCIP answer.
- **Section 7.4.**
  - "The true enabling comparison" is gone. The heading is now
    "cross-batch outcomes".
  - The ratio table says all of its CPU ratios are cross-batch and cannot
    measure the effect of cuts or capture.
  - "Genuine additional completion", "modest observed benefit", "lower
    measured CPU time" and "instrumentation distortion" no longer appear.
  - The wall/CPU ratio of 1.2047 is explicitly said not to establish
    comparable CPU speed.
  - The batch-speed table, the same-load result and the archived-vs-same-load
    `off` table are reported.
  - The 1.103 ratio is qualified in three ways:
    - selected solved subset;
    - `off` need not follow the same path;
    - it includes the patch's instrumentation.
  - The 12–18% gap is attributed to batch speed.
- **Limits** (end of 7.4, Summary "Not known", 7.3).
  - The batch confound and the capture confound for `corner`/`eff` are
    both stated.
  - The interleaved follow-up is described correctly: use the stock binary
    for both settings.
- **Revision entries.**
  - The round-1 M1 entry now says the cross-batch timings do not establish
    an enabling benefit, and it points to the round-2 correction.
  - The round-2 entry summarizes the fix accurately.
- **Reproducibility.**
  - The round-2 commands are recorded, including the first audit run that
    failed and its correction.
  - `logs/audit_revision_r2.log` and `logs/check_revision_r2.log` end in
    PASS.

A search of the note for "benefit", "distortion", "genuine", "favourab",
"true enabling", "lower measured", "modest", "CPU mean" and "node mean"
found only correctly qualified uses. The remaining "benefit" occurrences
deny a benefit.

**No-go basis.** The no-go is stated correctly in three places: Section 7.4
("the root results and the comparisons among patched rules"), the round-2
revision entry ("root results and within-batch rule-vs-rule comparisons"),
and Summary paragraph 2. All three keep the capture confound for
comparisons of `corner` or `eff` with stock.

## New issues

None of major or minor severity.

**A1 (administrative, required once this review is accepted).** Several
lines say the revision was not re-reviewed:

- the header status ("The final revision was not re-reviewed by an
  independent agent after the r2 major issue");
- the Summary's last sentence ("This revision has not been re-reviewed");
- the round-2 revision entry ("this revision has not been re-reviewed");
- the `CLOSEOUT.md` key-files line for this stream, and the `PROGRAM.md`
  phrase "unconfirmed final independent-review state".

These were accurate when written. Once this review exists, they should say
that review round 3 confirmed the N1/N2 fix and link this file. The note
should still say it is not refereed.

**Optional wording comments (no change required).**

- O1. Summary and Section 7.4 call the 68-pair ratio "the only like-for-like
  timing evidence about enabling". Sections 7.1–7.2 also contain
  within-batch patched-`scip` vs `off` comparisons: common-solved 1.0999,
  p = 0.046. They include capture-changed paths, so the 68-pair subset is the
  cleaner estimate, and both point in the same direction. A short
  cross-reference would avoid the impression that these comparisons
  disagree.
- O2. Section 7.3 lists matching wall/CPU medians as a "mitigating fact" for
  within-batch timing. Section 7.4 now correctly says that wall/CPU does not
  measure CPU inflation. The 7.3 mention could carry the same caveat. Its
  instance-ordering argument is the real mitigation.
- O3. "Share their first 103 display rows": the rows are identical except
  for the time column and the memory column. The memory column differs from
  the first row, as expected when captured rows are kept alive. This does not
  affect the estimate.

## Checks run, with outcomes

All commands ran from the stream directory with `OMP_NUM_THREADS=1`,
`PYTHONDONTWRITEBYTECODE=1` and `timeout 120s`, in the foreground. The script
has its own parser and imports nothing from the stream code or earlier
review code.

```bash
OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 timeout 120s python3 reviews/r3-code/recheck.py > reviews/r3-logs/recheck.log 2>&1   # exit 0
OMP_NUM_THREADS=1 timeout 30s pgrep -af '[r]echeck.py|[s]cip-stock|build-lapack/bin/[s]cip'   # exit 1, no process
```

The first run had a column-index bug in my prefix comparison: it dropped
"LP it/n" instead of "mem/heur" and so found 0 shared rows. I fixed it and
reran. I also appended checks 10–12. The log above is from the final run.

1. **Diff and full-text read.** I read the whole diff and the current note:
   Summary, Sections 1–3, 5–7.4, both revision entries and Section 10.
2. **Term search** for the withdrawn phrases (listed above).
3. **No-go basis and limits**: wording confirmed in Section 7.4, the
   revision entry and the Summary.
4. **Solved counts and CPU shifted geometric means** (600 raw logs).
   - off / stock / patched: 75 / 77 / 75 solved; 17.709 / 15.962 / 17.979 s.
   - Per-seed values match the Section 7.4 table.
   - Without `ex5_4_2`, seed 1: 76 vs 75 solved; 16.361 vs 17.277 s;
     ratio 0.9499.
   - Stock-only pairs: `ex5_4_2` s1 and `gabriel01` s2. There are no
     `off`-only pairs.
5. **Common subset of all five settings**: 73 pairs, 37 instances. CPU
   1.926 (stock) vs 2.148 (off). Nodes 614.0 vs 616.8. Cross-batch ratios
   0.9066 / 0.9296 and 1.1189 / 1.1832. Pair-solved ratios 0.9236 (75 pairs)
   and 1.1807 (74 pairs). All match.
6. **Matching-signature pairs.** The signature is the last-run node count
   plus primal-LP and dual-LP calls and iterations.
   - 74 pairs are solved by both point rules; 69 match.
   - Patched/stock ratio 1.1544. By stock CPU time: 41 / 19 / 9 pairs with
     ratios 1.0398 / 1.3033 / 1.4384.
   - The 5 changed pairs are `blend531` s2, `carton9` s1/s2 and
     `edgecross14-039` s1/s2.
   - 51 of 120 signatures differ overall.
   - 68 matching pairs are also solved by `off`: stock/off 0.9535 and
     patched/off 1.1029. `off` has the same signature as patched on only 2 of
     them, which supports the note's caveat that `off` need not follow the
     same path.
7. **Path outcomes.**
   - `blend852`: stock 172.64 / 172.68 s with 84509 / 96144 nodes; patched
     times out at 99192 / 101835 nodes.
   - `tln7` s1: patched 283.04 s with 308290 nodes; stock times out at
     584309 nodes.
   - `gabriel01` s2: stock 256.83 s with 97603 nodes; patched times out at
     67878 nodes.
   - The `gabriel01` s2 prefix is 103 rows through node 6600, at 29.0 s
     (stock) vs 44.6 s (patched). The factor 1.5379 gives 395.0 s.
8. **Same-load runs** (`reviews/r2-logs/sameload/`, 16 logs).
   - Patched/stock CPU ratio with cuts off: 0.9704–0.9932. With cuts on:
     0.9960–1.0225. All are within ±3%.
   - All 16 runs reproduce the archived node counts. For the four stock
     cut-on runs this was also checked against the stock batch.
   - Archived off / same-load stock off: 1.42 / 1.46 / 1.38 / 1.59.
     Stock-batch cut-on times are 5.61 / 9.27 / 15.45 / 48.5 s. These match
     Section 7.4 and review round 2.
9. **N2.** Using total nodes over restarts instead of last-run nodes:
   - All-pair columns: the largest change is 0.5952801059670492 (`corner`
     seed 2, 3890.1 → 3890.6). `off` seed 1 changes 4739.2 → 4739.4.
   - Common-subset columns: at most 0.2 per seed and 0.1 pooled.
   - The note's "at most 0.5 at table precision" and the 0.595 unrounded
     figure are correct.
10. **Section 7.2 cross-check**: patched-scip/off over all pairs is 1.0144,
    matching the table (used for O1).
11. **Local links**: every relative link target in the note exists.
12. **Status and process.**
    - `logs/audit_revision_r2.log` and `logs/check_revision_r2.log` end in
      PASS.
    - No solver or review process remains.
    - The only files I created are `reviews/review-r3.md`,
      `reviews/r3-code/recheck.py` and `reviews/r3-logs/recheck.log`.
    - No CI was inspected and no project-wide verification was run.
