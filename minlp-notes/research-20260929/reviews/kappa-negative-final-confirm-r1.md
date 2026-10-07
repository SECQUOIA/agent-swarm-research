# Final confirmation review (round 1) of `theory-bangbang/kappa-negative.md`

Date: 2026-10-01. Referee: fresh and independent. I did not write the note,
its scripts or any earlier review. Scope: the round-4 revision (note
Section 16), which applied the two optional nits N1 and N2 of
`reviews/kappa-negative-confirm-r3.md`. I checked both items from scratch,
recomputed every number that changed, and checked that nothing was
strengthened and that no new error was introduced. My script and logs are in
`reviews/kappa-negative-final-confirm-r1-checks/` (`f1_theta.py`, `logs/`).

Labels: **float** means floating-point computation. "Own code" means code I
wrote for this review. It does not import the author's code or the earlier
referees' code.

## Verdict

**Verified.** N1 and N2 are applied correctly. All new numbers in Section 15
(Check 4) and Section 16 agree with my independent rebuild of the KKT points,
to within `5e-12` stages. No other number, claim or conclusion changed. The
heuristic reading of Check 4 is no stronger than before. Two purely optional
nits remain (Section 3). Neither affects a number in the main text or a
conclusion.

## 1. N1 (stale review-status lines)

- **Section 14 preamble** (line 1973) now says "This revision was re-reviewed
  in `reviews/kappa-negative-confirm-r2.md` (Section 15)". This is what the
  round-4 review suggested, and it is correct.
- **Section 15 preamble** (line 2070) now says the same with
  `reviews/kappa-negative-confirm-r3.md` (Section 16). It is correct: that
  review covered the round-3 changes.
- **Section 13 preamble** (line 1839) already pointed to
  `kappa-negative-confirm-r1.md` (Section 14). It is unchanged and correct.
- **Header** (lines 3–16). It lists all four reviews, and I checked each
  quoted verdict against its review file: "fixes needed", "minor fixes needed
  (text only)", "minor fixes needed (numbers only)" and "P1 is resolved.
  Numbers verified; no fixes needed". It says that only the round-4 changes
  are unreviewed, which was true when it was written.
- **Search.** No other review-status line in the note contradicts the review
  record.

## 2. N2 (reference in Section 15, Check 4)

**Algebra (checked by hand).** The round-2 rule is `t_n + h (1 - u)/2` and
the corrected rule is `t_n + h (1 + u)/2`. They differ by `-h u`. Suppose the
round-2 values are measured against the round-2 `theta_1(16000)` instead of
the corrected one. In stages of grid `N`, each value then shifts by
`+(h_16000 / h_N) u_{s_1}(16000) = (N/16000) u_{s_1}(16000)`. This matches
Section 16, including its sign and `h = 1/8000` at `N = 16000` (`T = 2`).

**Independent rebuild (float, own code, `f1_theta.py`; 17 s).** The problem
data come from the toy's definition (target `a`, `k`, `Phi`, `T = 2`). From
the author's log I read only the dyadic jump time `tk` and the logged switching
stages. I used the stages only to centre the search window and to pick which
KKT point to compare. I derived the gradient by hand and checked it against
finite differences (maximum deviation `3e-9` at `N = 40`). I took the Hessian
on the free stages from gradient differences, because `J` is exactly
quadratic.

For each of the 42 strong-drop grids (`kappa 1 -> 0`; `(0.5, 1.5)`,
`(0.55, 1.45)`, `(0.45, 1.55)`; `N = 1000 … 16000`), I enumerated every KKT
point of the following shape whose switching stages lie within ±10 stages of
the logged ones:

`+1 | u_{s_1} vertex or fractional | -1 | u_{s_2} vertex or fractional | +1`

I checked the sign conditions on all other stages. Results:

- Each grid has exactly one such KKT point. On all 42 grids it matches the
  logged pattern (`s1`, `s2`, fractional stages).
- `u_{s_1}` agrees with the log to within `8.9e-12`.
- The stationarity residual on the fractional stages is at most `2.8e-15`.
- The `N = 16000` first switch is a vertex for `(0.5, 1.5)`. It is
  fractional for `(0.55, 1.45)` (`u = -0.54361`) and for `(0.45, 1.55)`
  (`u = +0.58911`). This matches Section 16.

**Ranges over the 20 grids with a fractional first switch and `N < 16000`**
(5 + 8 + 7 grids; stages of grid `N`):

| formula | reference `theta_1(16000)` | mine | note |
|---|---|---|---|
| corrected | corrected | `-0.70075 … -0.01408` | `-0.701 … -0.014` |
| round 2 | corrected | `-1.32902 … +0.52177` | `-1.329 … +0.522` (round-3 text) |
| round 2 | its own | `-1.28943 … +0.47757` | `-1.289 … +0.478` |

The extremes of the self-consistent range lie at `(0.55, 1.45)`, `N = 6000`
and `(0.45, 1.55)`, `N = 2500`, as Section 16 says. Per grid, my three values
agree with the fields of `logs/rev3_tallies.json` to within `5.0e-12` stages.
They also agree with `logs/summary3.json` of the round-4 referee to within
`3e-12`, which confirms the note's statement about that file.

**Text.** Section 15, Check 4 now quotes `-1.29 … +0.48` and says which
reference it uses. The bracketed note gives the round-3 range
`-1.33 … +0.52` and its reference correctly. `-1.33 … +0.52` appears nowhere
else in `research-20260929/` outside that bracket and the round-4 review. The
heuristic reading is unchanged. The text still says that the comparison
supports the derivation but does not replace it, and that the negative
offset of the corrected values was not analysed.

**Code and logs.**

- In `theory-bangbang/kneg/`, the only files modified after the round-3 logs
  are `rev3_checks.py` and `logs/rev3_tallies.json` (file timestamps). This
  is consistent with "no other code changed".
- The new code in part `tallies` pairs `dev` and `own` with `zip`. Both lists
  come from the same filter in the same order, so the pairing is correct.
- I ran part `tallies` on a `/tmp` copy of the script and of
  `logs/sweep.json`. The output file is byte-identical to the author's
  `logs/rev3_tallies.json`.
- My own comparison against `/tmp/rev3_tallies_before_r4.json` agrees with
  Section 12, item 25. The six old records are unchanged in every old field.
  Each `P1_theta1_vs_N16000_in_stages` record gained exactly the two new
  fields, and one record `P1_theta1_overall` was added. (That `/tmp` copy was
  made by the reviser. The old fields also agree with the numbers that the
  round-4 review verified independently.)
- `python3 tables.py sweep` still reproduces the Section 9.3 break table
  (now lines 1398–1406). All 9 lines match.
- The Section 12 script description and items 25–26 are accurate.

## 3. Declined items, strengthening, remaining problems

No item was declined. Nothing was strengthened. The only new content is
bookkeeping and a corrected heuristic range, which agrees with the review
that suggested it. Section 16's "Not changed" list is consistent with
everything I checked: Sections 7.2, 9.3 and 14 still carry the values that
the round-4 review verified.

No fixes are needed. Two purely optional nits:

- **O1 (optional; rounding in a worked example).** Section 16 writes
  `-1.086 + (6000/16000)(-0.5436) = -1.289`. With the rounded inputs shown,
  the left side is `-1.28985`, which rounds to `-1.290`. The stated `-1.289`
  is the correct unrounded result (`-1.08557 - 0.20386 = -1.28943`). Writing
  `-1.0856` or `≈` would make the line check exactly. The quoted range is
  unaffected.
- **O2 (optional; follow-on bookkeeping).** The header (lines 12–14) and the
  Section 16 preamble (line 2179) say that the round-4 changes "have not been
  re-reviewed". This is accurate now. Once this review is filed, those lines
  will be stale in the same way N1 described, so they will need the same
  one-line update.

## 4. Literature examined by this referee

No literature was needed. Round 4 changed bookkeeping and one heuristic float
range. I read `reviews/kappa-negative-confirm-r3.md` (the nits and its
reported numbers) and `reviews/kappa-negative-confirm-r3-checks/logs/{phase3,summary3}.json`
(only for comparison after my own computation). I also read the verdict
lines of `reviews/kappa-negative-review.md`, `-confirm-r1.md` and
`-confirm-r2.md` to check the header. No web searches.

## 5. Commands run (targeted only)

The runs in items 2, 3 and 5 used `OMP_NUM_THREADS=1` and an explicit
`timeout`. The small comparisons in items 1 and 4 were run without them; each
took under a second. No project-wide verification was run, CI was not
inspected, nothing was committed and no process was killed.

1. Wrote `reviews/kappa-negative-final-confirm-r1-checks/f1_theta.py`. Tested
   its gradient against central finite differences at `N = 40` (random `u`;
   maximum deviation `3.2e-9`).
2. `python3 f1_theta.py` → `logs/f1_theta.{log,json}` (float; 42 grids;
   17 s).
3. Copied `theory-bangbang/kneg/rev3_checks.py` and `logs/sweep.json` to
   `/tmp/fcr1/`, ran `python3 rev3_checks.py tallies` there (read-only for
   the note's files), then `cmp` against the author's
   `logs/rev3_tallies.json`: identical.
4. Own Python comparison: `/tmp/rev3_tallies_before_r4.json` against the new
   `logs/rev3_tallies.json` (old fields, new fields, new record); and my
   per-grid values against `logs/rev3_tallies.json` and the round-4
   referee's `logs/summary3.json`.
5. `python3 tables.py sweep` in `theory-bangbang/kneg/` (output to `/tmp`),
   then a line match against note lines 1398–1406: all 9 lines present.
6. Read-only inspections: the note (header, Sections 9.3, 12–16), grep for
   stale ranges and review-status lines across `research-20260929/`, file
   timestamps in `theory-bangbang/kneg/`, `rev3_checks.py`, `run_multi.py`
   (part `sweep`), `ktoy.py` (problem definition only).
