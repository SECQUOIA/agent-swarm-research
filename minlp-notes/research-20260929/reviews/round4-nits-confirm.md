# Confirmation review of the optional-nit revisions of three notes

Date: 2026-10-01. Referee: fresh and independent. I did not write any of
the three notes, their scripts or the earlier reviews. Scope: the revision
that applied the remaining optional nits of the last confirmation review of
each note:

- (a) `open-instances-wave3/eg/retry.md`: nits N1 and N2 of
  `reviews/eg-retry-confirm-r1.md`, and the header status;
- (b) `theory-robust-lb/robust-chains.md`: the optional items of
  `reviews/robust-lb-chains-final-confirm-r1.md` (Sections 5.1–5.3);
- (c) `theory-bangbang/kappa-negative.md`: O1 and O2 of
  `reviews/kappa-negative-final-confirm-r1.md`.

I checked each change from scratch against the code and logs, recomputed
every number that the changed text states, and checked that no result or
certified value changed. Following `AGENTS.md`, I ran only targeted checks
(listed in Section 5), single-threaded and under `timeout`. I ran no
project-wide verification, did not look at CI, committed nothing and
edited none of the notes.

## Verdict

**Verified.** Every requested change was made correctly, and the
reviser's one deviation from a suggestion (b, "largest value `1.12e-8`"
instead of "at most `1.12e-8`") is correct. Every number in the changed
text agrees with the logs or with my recomputation. No bound, certified
value, proved statement or conclusion changed. No code or log file was
modified after the three confirmation reviews were filed. Each note
records the changes in its revision section. Only optional nits remain
(Section 4). None affects a result.

| Note | Item | Verdict |
|---|---|---|
| (a) retry.md | N1, Section 3.4 step 3 | fixed; matches `egbb.BB.dual_value` exactly |
| (a) retry.md | N2, Sections 3.2 and 4 | fixed; ratios recomputed from the logs |
| (a) retry.md | header status, Section 10 item 8 | accurate |
| (b) robust-chains.md | Section 7 row | fixed; runs, `n` values and the cited proof checked |
| (b) robust-chains.md | Section 10.4 item 2 | fixed; the reviser's wording is the accurate one |
| (b) robust-chains.md | header, Section 10.5, Summary left unchanged | accurate |
| (c) kappa-negative.md | O1, worked example in Section 16 | fixed; recomputed from `logs/rev3_tallies.json` |
| (c) kappa-negative.md | O2, header and Section 16 preamble | fixed |
| (c) kappa-negative.md | Section 17, Section 12 item 27 | accurate |

## 1. (a) `open-instances-wave3/eg/retry.md`

### 1.1 N1 (Section 3.4, step 3)

**Code.** `retry/egbb.py`, `BB.dual_value` (lines 279–297):

```python
if not ys.sum() > 0:
    return -INF
...
if vl >= 0:
    q = vl / float(S.hi)
elif float(S.lo) > 0:
    q = vl / float(S.lo)
else:      # sum y not proved > 0: no bound from this dual vector
    return -INF
```

`LP.solve` returns `y = max(-row_dual, 0)` (line 109), so `y >= 0`.

**New text.** "If this minimum (the combined value vl) is negative and that
enclosure is not proved positive, the LP gives no bound (…). If vl ≥ 0, it
is divided by the upper end of the enclosure; this needs no guard, because
y ≥ 0 and its float sum is positive, so Σ_k y_k > 0."

**Check (by hand).** The code returns −∞ from the guard only when
`vl < 0` and `S.lo <= 0`, which is what the text now says. For `vl >= 0` it
divides by `S.hi` whatever `S.lo` is. This is valid: at that point the
float sum of `y` is positive (otherwise the function already returned −∞),
and a positive float sum of nonnegative numbers means that some term is
positive, so the exact sum is positive and at most `S.hi`. The new wording
matches the code and is no longer broader than it. The parenthetical
"it never acted when runs A–E and G–I were run again with it" agrees with
the table in Section 10 item 3 (0 calls with `S.lo <= 0` in all eight
runs), which the confirmation review checked.

### 1.2 N2 (Sections 3.2 and 4)

**Check (read from the logs).** The final `B&B: done=True …` line of each
log gives:

| ratio | interval run | fast run | ratio |
|---|---|---|---|
| B/A | `int_ni_1e-9.log`: 2280 s | `int_1e-9.log`: 401 s | 5.69 |
| H/C | `int9_ni3.log`: 2113 s | `int9_final.log`: 274 s | 7.71 |
| I/E | `disc9_ni3_p0/p1.log`: 2660 + 2373 s | `disc9_p0/p1.log`: 726 + 650 s | 5033/1376 = 3.66 |

The review's replay of eg_disc2_s part 1: 5,755 s (`eg-retry-review.md`,
Section 6) against 1,515 s (`disc2_9_p1.log`, final line), ratio 3.80.

So Section 3.2's "3.7–7.7 times slower … 5.7 for B/A, 7.7 for H/C, 3.7 for
I/E" is correct, and Section 4's "about 4–8 times the cost of the fast runs
(Section 3.2)" is a fair rounding. The replay sentence in Section 4
(134,607 boxes, same certified value, 5,755 s against 1,515 s, ratio 3.8)
agrees with review Section 6 and with the log. No other "6–10" or "4–8"
figure remains in the note (`grep`).

### 1.3 Header and Section 10 item 8

The header now says that the independent review (`eg-retry-review.md`)
found the results **verified**, that its corrections are items 1–7 of
Section 10, that the confirmation review (`eg-retry-confirm-r1.md`)
checked them and found them **verified**, and that the two nits (item 8)
have not been re-reviewed. Both verdicts match the review files. Item 8
records N1, N2 and the header change, each with its check, and says that
no bound, primal value or closure claim changed. That is accurate.

### 1.4 Nothing else changed

- The certified values in the Section 1 table and the Section 5 run table
  agree with the final lines of `int9_final.log` (6.4531031529331155),
  `disc9_p1.log` (5.760539610694994) and all eight `disc2_9_p*.log`
  (5.642100574331458).
- No file in `retry/` (code or logs) is newer than
  `reviews/eg-retry-confirm-r1.md` (`find -newer`). Only `retry.md` is.

## 2. (b) `theory-robust-lb/robust-chains.md`

### 2.1 Section 7 row (review Sections 5.1 and 5.2)

**New text.** "ball `M = 1.1`–`1.5`: runs at `M = 1.1`, `1.3`, `1.5` and
`n = 5, 8, 16, 32`, and at `n = 12, 24` in the third review; the radii in
between rely on the value being nonincreasing in `M` (proved in the fourth
review, `../reviews/robust-lb-chains-confirm-r3.md`, Section 1), so that no
gap at `M = 1.5` means none at smaller `M` for the same `n`."

**Checks.**

- *Read.* `chains/logs/revision3_radius.log` has `M = 1.1, 1.3, 1.5, 2` at
  exactly `n = 5, 8, 16, 32`. The third review's `d5_radius_n.log`
  (`reviews/robust-lb-chains-confirm-r2-checks/`) has the same radii at
  `n = 12, 16, 24, 32`. So "`n = 12, 24` in the third review" names exactly
  the values of `n` that the note's own runs lack.
- *Rerun.* `python3 -B revision3_chains.py radius` (output to `/tmp`) is
  identical to `logs/revision3_radius.log` (`diff`).
- *The cited proof (by hand).* The fourth review, Section 1, proves the
  monotonicity. The localizing matrix of `2M^2 - x^2 - y^2` in the basis
  `(1, x, y)` has entries `L((2M^2 - x^2 - y^2) b_i b_j)
  = 2M^2 L(b_i b_j) - L((x^2 + y^2) b_i b_j)`, that is `2M^2 M_1` minus a
  matrix that does not depend on `M`. `M_1` is a principal submatrix of the
  order-2 moment matrix, so it is PSD at every feasible point. Raising `M`
  adds `2(M'^2 - M^2) M_1`, which is PSD, so every feasible point stays
  feasible and the value cannot increase. The value is at most 0 (the
  Dirac measure at the minimizer `0` is feasible). Hence a value of about 0
  at `M = 1.5` gives a value of about 0 at every smaller `M`, as the row
  says. The direction of the implication is correct.
- The row now names the tested radii and `n` values and says what the
  range between them rests on. This removes the ambiguity the review
  pointed out. No claim was strengthened.

### 2.2 Section 10.4 item 2

The text now reads "with largest value `1.12e-8` for `M <= 1.5`
[round 5: was "values at most `1.2e-8`"; Section 10.5]". The largest such
value in `d5_radius_n.log` is `1.121682e-8` (`M = 1.1`, `n = 32`). The
reviser is right that the review's suggested "at most `1.12e-8`" would be
slightly false, since `1.121682e-8 > 1.12e-8`. "Largest value `1.12e-8`"
is a correct three-digit rounding.

### 2.3 Header, Section 10.5 and the unchanged Summary sentence

- The header reads "revised after review rounds 1 to 5" and says that the
  round-5 changes (wording only) have not been re-reviewed. Correct.
- Section 10.5 identifies the fifth review and its verdict correctly, and
  records both changes with their checks. The naming of the third, fourth
  and fifth reviews follows the mapping used elsewhere in the note.
- The Summary's "ball-radius runs up to `n = 32` come from the third
  review and were reproduced here" was left unchanged. The third review's
  runs are at `n = 12, 16, 24, 32`, so "up to `n = 32`" describes them
  accurately. Leaving it is reasonable.
- *No collateral change.* The fifth review counted 2033 lines. The note now
  has 2080. Section 10.5 accounts for 45 lines (2036–2080) and the header
  sentence for 1; the Section 7 row is a single line, and the bracket in
  Section 10.4 item 2 adds 1. This is consistent with no other edits. No
  file in `chains/` (code or logs) is newer than the fifth review.

## 3. (c) `theory-bangbang/kappa-negative.md`

### 3.1 O1 (worked example in Section 16)

**Check (float, own one-line computation from `kneg/logs/rev3_tallies.json`).**

- `(0.55, 1.45)`: `u_{s_1}(16000) = -8000 (0.4218464757575688 -
  0.42177852424243123) = -0.5436121`. The value against the corrected
  reference at `N = 6000` is `-1.0855727`. Then
  `-1.0855727 + 0.375 (-0.5436121) = -1.2894273`, equal to the logged
  `rows_N_roundtwo_own_ref` entry `-1.2894272727`.
- `(0.45, 1.55)`: `u_{s_1}(16000) = +0.5891100`; at `N = 2500`,
  `0.3855223 + 0.15625 (0.5891100) = 0.4775708`, equal to the logged
  `0.47757077858`.
- With the rounded inputs now shown: `-1.0856 + 0.375 (-0.5436) =
  -1.28945` (rounds to `-1.289`), and `0.386 + 0.15625 (0.5891) =
  0.478047` (rounds to `0.478`). With the old `-1.086` the first gives
  `-1.28985`. Both lines now check, and `≈` is the right sign for rounded
  inputs.
- The quoted range `-1.289 … +0.478` matches record `P1_theta1_overall`
  (`[-1.2894272727, 0.4775707786]`) and is unchanged.

The Section 17 record of O1 states these numbers correctly
(`-1.085573`, `-0.543612`, `-1.28943`, `-1.2894273`, `-1.28985`,
`-1.28945`, `0.47805`, `0.47757`).

### 3.2 O2 (review-status lines)

- The Section 16 preamble now says "This revision was re-reviewed in
  `reviews/kappa-negative-final-confirm-r1.md` (Section 17)". This follows
  the pattern of the Section 13–15 preambles, which I also checked (each
  points to the review that covered that round).
- The header lists five reviews. The fifth is quoted with verdict
  "Verified", which matches the review file. The header says that this
  review re-reviewed the round-4 changes (review-status lines, the
  heuristic range in Section 15, the extension of a read-only check
  script), which is what the round-4 changes were, and that only the
  round-5 changes are unreviewed. The date line reads "round-3 to round-5
  revisions 2026-10-01". All correct.

### 3.3 Records, and nothing else changed

- Section 17 records O1 and O2, each with its check, and a "Not changed"
  statement. Section 12 item 27 records the one read-only Python
  computation of this round.
- *Code and logs.* No file in `kneg/` is newer than the fifth review. The
  newest are `rev3_checks.py` and `logs/rev3_tallies.json` (11:54), both
  before the fifth review was filed (12:00) and both covered by it.
- *Line count.* The line numbers that the fifth review cites have all
  shifted by +15 up to Section 16 (e.g. Section 13 preamble 1839 → 1854,
  Section 16 preamble 2179 → 2194). The header and the item-27 block
  account for these 15 lines.
- *Rerun.* `python3 tables.py sweep` (output to `/tmp`) still reproduces
  the Section 9.3 break table: all 9 lines are present in the note (now
  lines 1401–1409).

## 4. Remaining points (all optional; none affects a result)

1. **(a) "CPU time" is elapsed time.** The `time` field in the egbb logs is
   elapsed wall-clock time per process (`time.time()` in `egbb.BB.run`,
   printed at line 516), not CPU time. The new text in Section 3.2 and
   Section 10 item 8 calls the ratios "CPU-time ratios", following the
   older label in Section 5 and Section 10 items 1 and 3. Each process is
   single-threaded, so elapsed time is close to CPU time when the machine
   is not oversubscribed, and the note already says that timings are
   indicative only. "Elapsed-time ratios" would be exact.
2. **(a) Section 3.4, step 3.** "this needs no guard, because y ≥ 0 and its
   float sum is positive" relies on the earlier test that returns no bound
   when the float sum of `y` is not positive. Step 3 does not mention that
   test (Section 10 item 8 does). Adding "(otherwise no bound is taken)"
   would make step 3 self-contained.
3. **(b) Section 10.5 item 1.** "values from `1.59e-8` to `5.23e-7`" holds
   for the Clarabel values only. The same log also has SCS values at
   `n = 5, 8`, from `-8.5e-10` to `2.3e-10`. "Clarabel values from …"
   would be exact. All these values are within `6e-7` of 0, so "no gap" is
   unaffected.
4. **Follow-on bookkeeping.** Once this review is filed, the "not
   re-reviewed" lines become stale in the same way as before: the retry
   header ("that wording change has not been re-reviewed"), the
   robust-chains header ("The round-5 changes … have not been
   re-reviewed"), and the kappa-negative header and Section 17 preamble.

## 5. Commands run (targeted only)

All runs used `OMP_NUM_THREADS=1` (and `OPENBLAS_NUM_THREADS=1` for the
SDP rerun) and `timeout`. Outputs went to `/tmp/r4nits/`. I checked
afterwards that no file under `theory-bangbang/`, `theory-robust-lb/` or
`open-instances-wave3/eg/` was modified by these runs.

| Command | Result | Kind |
|---|---|---|
| `grep -n time` on the final lines of `retry/logs/{int_1e-9,int_ni_1e-9,int9_final,int9_ni3,disc9_p0,disc9_p1,disc9_ni3_p0,disc9_ni3_p1,disc2_9_p1}.log` | times as in Section 1.2 | read |
| `grep` of the certified values in `int9_final.log`, `disc9_p*.log`, `disc2_9_p*.log` | as in the note's tables | read |
| `python3 -B revision3_chains.py radius` in `theory-robust-lb/chains/` | identical to `logs/revision3_radius.log` (`diff`) | float rerun |
| reading `d5_radius_n.log` of the third review | maximum for `M <= 1.5` is `1.121682e-8` | read |
| one-line Python computation from `kneg/logs/rev3_tallies.json` | numbers in Section 3.1 | float |
| `python3 tables.py sweep` in `theory-bangbang/kneg/` | 9 break-table lines found in the note | float rerun |
| `find -newer` / `ls --time-style=full-iso` on the three code and log directories | no code or log changed after the three confirmation reviews | read |

I also read `egbb.py` (line 109, lines 279–297, the timing in `BB.run`
and the final print at line 516),
the fourth review's Section 1 (`robust-lb-chains-confirm-r3.md`), and the
three confirmation reviews named above. No literature was needed: no
statement about prior work changed. No web searches.
