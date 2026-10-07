# Confirmation review (round 3) of `theory-bangbang/kappa-negative.md`

Date: 2026-10-01. Referee: fresh and independent. I did not write the note,
its scripts or the earlier reviews. Scope: check the round-3 revision (note
Section 15) against the one item of `reviews/kappa-negative-confirm-r2.md`
(P1, the phase position `theta_1` of a fractional first switch), recompute
the numbers that changed, and check that nothing was strengthened. My checks
and logs are in `reviews/kappa-negative-confirm-r3-checks/` (`c3_phase.py`,
`c3_summary.py`, `logs/`).

Labels: **float** means floating-point computation in my own code. I did not
import the author's code. My scripts read only the following from the
author's logs: the dyadic jump time `tk` of `k` (a problem datum), the logged
pattern (`s1`, `s2`, fractional stages), which I used only to choose which of
my own KKT points to compare, and the break offsets `break_minus_s1`. I
cross-checked those offsets against the round-1 referee's own sweep logs.

## Verdict

**P1 is resolved. Numbers verified; no fixes needed.** The corrected formula
is right, and the rerun log differs from the round-2 log only where it should.
All 13 quoted break times, the per-configuration ranges, the factors and the
implied matching times agree with my own independent rebuild. Nothing was
strengthened. I found two optional nits in the text, both small (Section 3).
Neither affects a number in the main text or a conclusion.

## 1. Check of P1

**Formula (proved, elementary).** In the Euler toy `x_{t+1} = x_t + h u_t`,
suppose stage `n` is replaced by a switch at `theta` in `[t_n, t_{n+1}]`,
with `+1` before it and `-1` after it. Then `x` moves by
`(theta - t_n) - (t_{n+1} - theta)`. Setting this equal to `h u_n` gives
`theta = t_n + h (1 + u_n) / 2`. [W, Remark 1.4] does not spell out the
interior control value. This "same state increment" reading is the natural
one, and it matches the rule in `run_multi.py kink`,
`theta = t_n + h (u_n - u_after) / (u_before - u_after)`. As `u_n -> -1` it
gives the vertex rule `theta_1 = t_{s_1}`. The corrected line in
`run_multi.py` (part `sweep`) implements exactly this formula, and its
comment is accurate.

**Independent rebuild (float, own code, `c3_phase.py`; about 11 s).** For
all 42 strong-drop grids (`kappa 1 -> 0`; `(0.5, 1.5)`, `(0.55, 1.45)`,
`(0.45, 1.55)`; `N = 1000 … 16000`), I enumerated every KKT point of the
form `+1 | vertex or fractional | -1 | vertex or fractional | +1` whose
switching stages lie within ±12 stages of the logged ones. I solved for the
fractional controls exactly (`J` is quadratic, with a hand-derived Hessian)
and checked all sign conditions. On every grid there is exactly one such
KKT point, and its pattern matches the log. Results (`logs/phase3.{log,json}`,
`logs/summary3.json`):

- `u_{s_1}` agrees with the new log field `u_s1` to within `4.7e-12`, and
  with the round-1 referee's sweep logs to within `9.3e-13`.
- My corrected `break time - theta_1` agrees with the new
  `break_time_minus_theta1` on all 42 grids, to within `7.8e-16`. My
  evaluation of the round-2 formula reproduces the old log to within
  `7.6e-16`. So the round-2 numbers came from the sign error alone.
- The four quoted values that changed: `(0.55, 1.45)`: `N = 4000`,
  `u = -0.8821`, `9.705e-4`; `N = 6000`, `u = +0.5`, `7.500e-4`.
  `(0.45, 1.55)`: `N = 1000`, `u = +0.6275`, `-1.627e-3`; `N = 6000`,
  `u = +0.2647`, `1.225e-4`. The other 9 quoted grids have a vertex first
  switch, and their values are unchanged.
- The break offsets `break_minus_s1` in the author's log equal the round-1
  referee's on every grid.

**Ranges and matching times (float, own tally, `c3_summary.py`).** I used
the 13 grids with a fractional second switch (5 + 5 + 3, the note's lists)
and took `N > 1000`. For `(0.5, 1.5)` the range is `5.714e-4 … 6.667e-4`
(factor 1.17). For `(0.55, 1.45)` it is `5.714e-4 … 9.705e-4` (factor 1.70).
For `(0.45, 1.55)` it is `1.225e-4 … 2.000e-4` (factor 1.63). Overall the
range is `1.2e-4 … 9.7e-4`. The layer-law ratios `exp(-gamma/|eta|)` are
`1.8900e-3`, `5.5809e-3` and `4.1989e-4`. The implied matching times are
0.302–0.353, 0.102–0.174 and 0.292–0.476, so overall 0.10–0.48. Their ratio
is 4.65, so "about 0.1 to 0.5, a factor of about 5" holds. At `N = 1000` the
values are `0` for `(0.5, 1.5)` (vertex first switch, break at `s_1`) and
`-1.627e-3` for `(0.45, 1.55)` (break at `s_1`, `0.814` stage before
`theta_1`). All these numbers match Sections 7.2, 9.3, 14 (R3) and 15 to the
digits quoted.

**Log comparison (float, own diff, `c3_summary.py`).** I diffed
`logs/sweep.json` against `logs/pre_revision/sweep_r2.json`. Both have 98
records. Apart from `time`, `break_time_minus_theta1` and the new `u_s1`,
no field differs. `break_time_minus_theta1` changed on exactly 24 records.
This is the number of records with a fractional first switch and a break
(22 strong-drop grids and 2 at `eta^X_1 = -0.275`, `N = 3500, 8000`). Each
changed record has a fractional `s_1`. None of the 20 changed values outside
the quoted set appears in the note. The per-grid times sum to 974.6 s (the
note says 975 s). `python3 tables.py sweep` regenerates the Section 9.3
break table (note lines 1394–1402) byte for byte (`diff`).

**Text.** I checked every place that quotes these numbers. Section 7.2
(lines 1095–1110), Section 9.3 (lines 1424–1446), Section 14 R3 (lines
1990–2017) and Section 15 are corrected. The `theta_1` convention is stated
once, in 9.3. The bracketed note in Section 14 gives the round-2 values
correctly: `5.3e-4 … 9.2e-4`, `2.0e-4 … 2.1e-4`, `-3.73e-4`, and matching
times 0.095–0.16 and 0.48–0.50, which I recomputed from the round-2 log. It
also correctly says that the `-3.7e-4` in `kappa-negative-confirm-r1.md`
(line 103) was read from the same log field. No stale value remains outside
these marked history notes. The new `rev3_checks.py` computes the ranges
from the log instead of typing them in. The comment in `rev2_checks.py`
marks its typed-in values as superseded. The Section 12 entries
(files, item 18 note, items 21–24) are accurate.

## 2. Declined items and strengthening

No item was declined. The revision narrows nothing and claims nothing new.
The only additions are descriptive: the per-configuration factors
1.2/1.7/1.6 and the remark that the `N = 1000` exception "is more
pronounced". Both are accurate. Section 15 Check 4 is labelled heuristic,
and the note says it does not replace the derivation. The hedged conclusion
(a consistency observation that needs an undetermined matching time of about
0.1–0.5; no asymptotic claim) is unchanged.

## 3. Remaining problems

None that need a fix. Two optional nits:

- **N1 (stale status line).** The Section 14 preamble still says "These
  changes have not been re-reviewed." The header and Section 15 say that
  `reviews/kappa-negative-confirm-r2.md` reviewed them. In round 2 the
  Section 13 preamble was updated in the same situation. *Suggested fix:*
  "This revision was re-reviewed in `reviews/kappa-negative-confirm-r2.md`
  (Section 15)."
- **N2 (reference in Check 4).** Section 15, Check 4 gives
  `theta_1(N) - theta_1(16000)` with the round-2 formula as `-1.33 … +0.52`
  stages. `rev3_checks.py` subtracts the *corrected* `theta_1(16000)` in
  both comparisons. For `(0.55, 1.45)` and `(0.45, 1.55)` the `N = 16000`
  first switch is fractional, so the two formulas give different reference
  values there. With each formula's own reference, the round-2 range is
  `-1.29 … +0.48` (my `c3_summary.py`; the corrected range stays
  `-0.70 … -0.01`). The contrast, and the heuristic reading of it, do not
  change. *Suggested fix:* say which reference is used, or quote the
  self-consistent range.

## 4. Literature examined by this referee

- [W] `theory-bangbang/window-exactness.md`, Remark 1.4 (phase model), read
  for the definition of the phase position.
- `reviews/kappa-negative-confirm-r1.md` (line 103) and
  `reviews/kappa-negative-confirm-r2.md`, with the round-1 referee's sweep
  logs (`kappa-negative-confirm-r1-checks/logs/sweep_m{590,690,490}.log`),
  used as an independent source of `u_{s_1}` and break offsets.
- No web searches and no new literature. The note's novelty statements did
  not change in round 3, and I did not re-examine them.

## 5. Commands run (targeted only)

All commands were run with `OMP_NUM_THREADS=1` and an explicit `timeout`
where they computed anything. No project-wide verification was run, CI was
not inspected, nothing was committed, and no process was killed.

1. `python3 c3_phase.py` (in `reviews/kappa-negative-confirm-r3-checks/`) →
   `logs/phase3.{log,json}` (float; 42 grids; about 11 s).
2. `python3 c3_summary.py` → `logs/summary3.json` (float tallies; own diff
   of `theory-bangbang/kneg/logs/sweep.json` against
   `logs/pre_revision/sweep_r2.json`; seconds).
3. `python3 tables.py sweep` in `theory-bangbang/kneg/` (read-only; output
   to `/tmp`), then `diff` against note lines 1394–1402: identical.
4. Read-only inspections: `run_multi.py` (part `sweep`, part `kink`),
   `rev3_checks.py`, `rev2_checks.py` (the new comment), `ktoy.py` (problem
   conventions only), `logs/rev3_{compare,tallies}.json`, and the note
   (header and Sections 7.2, 9, 9.3, 12–15).
