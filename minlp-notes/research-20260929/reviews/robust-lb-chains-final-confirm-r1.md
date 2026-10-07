# Referee check of the fourth revision of "Split-robust lower bounds on uniform chains"

Date: 2026-10-01. Note checked:
`research-20260929/theory-robust-lb/robust-chains.md`, revised after review
round 4 (2033 lines; changes listed in its Section 10.4). The review that
asked for the changes is `reviews/robust-lb-chains-confirm-r3.md` (the
note's "fourth review"), Sections 4.1 and 4.2. I did not write the note, its
scripts or any earlier review. My scripts and logs are in
`reviews/robust-lb-chains-final-confirm-r1-checks/`. They share no code with
the note's `chains/` scripts or with the earlier reviews' checks.

Following `AGENTS.md`, I ran only targeted checks. I ran no project-wide
verification, did not look at CI, committed nothing and did not edit the
note.

Labels used below:

- **proved**: checked by hand, step by step;
- **float**: recomputed in floating point (cvxpy with Clarabel, and SCS
  where stated), not certified;
- **read**: checked by reading an existing log or text, without
  recomputing.

## Verdict in brief

**Verified.** All three requested changes were made correctly, and the one
point that was not applied is a reasonable refusal. No claim was
strengthened and no new error was introduced. Every number the changed text
relies on was recomputed with my own code and agrees with the note. The
note's round-3 script and the fourth review's script, rerun, reproduce
their logs exactly. Only optional wording points remain (Section 5).

| Item | Verdict |
|---|---|
| 1. Section 8: the third review's cross-check was attributed too broadly | **fixed.** Accurate attribution: the third review computed univariate multipliers only; the fourth review computed all three rows on both sides. |
| 2. Lasserre paragraph: "`n <= 32`" | **fixed.** It now lists `n = 5, 8, 16, 32` (note) and `n = 12, 24` (third review), and `M = 10` is marked `n = 5, 8`. Recomputed. |
| 3. Section 8: which ball rows were run at `n = 16, 32` | **fixed.** It now names `M = 1.1, 1.3, 1.5, 2`, the only radii run at those `n`. |
| Header and Section 10.4 | accurate |
| Not applied: monotonicity in `M` | acceptable refusal (optional point, outside this round's task); see Section 5.1 for one caveat about its stated reason |

## 1. Item 1: attribution of the cross-check in Section 8

**The change (lines 1602–1616).** The text now says that the gaps with
`|y_alpha| <= 1` and with Waki et al.'s scaled bounds were computed here on
the moment side only (Clarabel and SCS). It says the third review's code
gives the same values "for univariate multipliers". It also says the
fourth review's code reproduces "all three rows" (univariate multipliers
with either bound, and the opposite orientation with the scaled bounds)
from both the moment side and the SOS side, in floating point.

**Checks.**

- *Third review (read).* In
  `reviews/robust-lb-chains-confirm-r2-checks/d2_sdp.log`, the two rows
  with `"zbound": true` have `"place": "uni"`. The four rows with
  `"ybound": true` have `"uni"` or `"uni_quad"`. The other logs of that
  review (`d4_more_placements.log`, `d5_radius_n.log`) have no moment
  bounds. So the third review never computed the opposite orientation
  with any bound. Its univariate values (`-0.06276815`, `-0.1262654`,
  `-0.6988746`, `-1.331693`) match the note. The new sentence is
  accurate.
- *Fourth review (read and rerun).* `e1_waki.log` has the three rows with
  both `sos_*` and `mom_*` values: `uni`+`zb` (Clarabel and SCS), `opp`+`zb`
  (Clarabel and SCS), and `uni`+`yb` (Clarabel). I reran
  `e1_two_sides.py waki` with output sent to my check directory. Its
  result lines are identical to `e1_waki.log`. I confirmed that the
  rerun wrote nothing into the fourth review's directory: its file times
  are unchanged.
- *"Moment side only" for the note's own runs (read).* The note's SOS-side
  log (`chains/logs/revision2_independent_sos.log`) has no row with a
  moment bound. `revision2_sos.log` and `revision3_waki.log` have Clarabel
  and SCS on every bounded row. The phrase "(Clarabel and SCS)" is correct.
- *My own recomputation (float, moment side; `f1_moment.py bounds` →
  `f1_bounds.log`).*

  | row | note `n = 5` / `n = 8` | mine, Clarabel | mine, SCS |
  |---|---|---|---|
  | univariate multipliers + `\|y_alpha\| <= 1` | `-0.0628` / `-0.1263` | `-0.06276815` / `-0.1262654` | `-0.06276805` / `-0.1262654` |
  | univariate multipliers + scaled bounds | `-0.6989` / `-1.3317` | `-0.6988746` / `-1.331693` | `-0.6989318` / `-1.331681` |
  | opposite orientation + scaled bounds | `-0.0538` / `-0.1994` | `-0.05375047` / `-0.1994185` | `-0.05372812` / `-0.199373` |
  | opposite orientation, no bounds (control) | `-0.0553` / `-0.2072` | `-0.05530551` / `-0.2071795` | — |

  Every row agrees to the digits the note prints. (My SCS values differ
  from Clarabel's in the fifth digit. That is SCS's default accuracy, and
  it does not affect any value the note prints.)

The Section 7 row ("moment side only for the moment bounds") is unchanged.
That is correct, because it describes the note's own computations.

## 2. Item 2: the `n` values in the Lasserre paragraph

**The change (lines 1282–1285).** "shows no gap for `M = 1.1`, `1.3`,
`1.5` (floating point, `n = 5, 8, 16, 32`; the third review also found none
at `n = 12, 24`), and it has a gap for `M = 2` (`n = 8, 16, 32`) and
`M = 10` (`n = 5, 8`)."

**Checks.**

- *Read.* `chains/logs/revision3_radius.log` has `M = 1.1, 1.3, 1.5, 2` at
  exactly `n = 5, 8, 16, 32`. `d5_radius_n.log` of the third review has
  the same four radii at `n = 12, 16, 24, 32`. Its largest value for
  `M <= 1.5` is `1.121682e-8` (`M = 1.1`, `n = 32`). Section 10.4 says "at
  most `1.2e-8`". That is a true upper bound, slightly loose. In the note,
  `M = 10` appears only in `revision2_sos.log`, at `n = 5, 8`.
- *Same relaxation (read).* The third review's `d2_sdp.build(n, "opp", M)`
  uses the same placement: `1 - x_i` in clique `(i-1, i)` and `1 + x_i` in
  `(i, i+1)`, with both constraints of an end variable in its only clique.
  It also localizes the ball in every clique with the basis
  `(1, x, y)`. So its `n = 12, 24` rows are rows of the relaxation the note
  describes.
- *My own recomputation (float; `f1_moment.py lasserre` →
  `f1_lasserre.log`; Clarabel, status `optimal` on every row).*

  | `M` | `n = 5` | `8` | `12` | `16` | `24` | `32` |
  |---|---|---|---|---|---|---|
  | 1.1 | `6.8e-8` | `1.1e-7` | `1.4e-7` | `1.8e-7` | `2.5e-7` | `3.2e-7` |
  | 1.3 | `4.5e-8` | `8.8e-8` | `9.1e-8` | `1.1e-7` | `1.7e-7` | `2.2e-7` |
  | 1.5 | `1.6e-8` | `2.0e-7` | `2.2e-7` | `2.6e-7` | `4.0e-7` | `5.2e-7` |
  | 2 | `1.9e-7` | `-0.01581842` | `-0.07220158` | `-0.1328175` | `-0.255459` | `-0.3783857` |
  | 10 | `-0.04268874` | `-0.1782065` | — | — | — | — |

  So `M = 1.1, 1.3, 1.5` show no gap at any of the six `n`. `M = 2` has a
  gap at `n = 8, 16, 32` but not at `n = 5`, and `M = 10` has a gap at
  `n = 5, 8`. This confirms every part of the sentence. Three rows of the
  third review's `d5_radius_n.log` have status `optimal_inaccurate`,
  including `M = 1.3` at `n = 24`. My solves of the same rows reach
  `optimal`, so the attribution "also found none at `n = 12, 24`" does not
  rest on inaccurate solves alone.
- "computed" was replaced by "floating point". That is more precise.

## 3. Item 3: which ball rows were run at `n = 16, 32`

**The change (lines 1602–1604).** "at one parameter point and `n = 5, 8`
(the ball rows with `M = 1.1`, `1.3`, `1.5` and `2` also at `n = 16, 32`)."

**Check (read; recomputed above).** I searched every log in `chains/logs/`
for ball or moment-bound rows. Only `revision2_sos.log`,
`revision2_independent_sos.log`, `revision3_waki.log` and
`revision3_radius.log` contain them. Only `revision3_radius.log` has
`n = 16, 32`, and it has exactly these four radii. `M = 1`, `1.01` and `10`
appear only at `n = 5, 8`. The text is correct.

## 4. Header, Section 10.4, and was anything strengthened?

- The header now reads "revised after review rounds 1 to 4". Correct.
- Section 10.4 accurately describes the review (one accuracy nit in its
  Section 4.1, optional wording in its Section 4.2). Each entry gives the
  review point, the check and the change, and each check matches what I
  found above.
- The commands table in Section 10.4 is reproducible. I reran all three
  commands with `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`:
  - `revision3_chains.py radius` (8.4 s) and `waki` (19.6 s) are identical
    to `logs/revision3_radius.log` and `logs/revision3_waki.log` (`diff`);
  - `e1_two_sides.py waki` (30.2 s): result lines identical to
    `e1_waki.log`.

  The run times match the note's 9 s, 19 s and 29 s.
- *No strengthening.* Section 10.4 says that only wording changed. The
  changed passages (header, Lasserre paragraph, Section 8 numerics item)
  narrow or attribute claims: specific `n` instead of "`n <= 32`", named
  radii instead of "the ball rows", and a narrower credit to the third
  review. They add no proved statement and change no value. The one added
  claim, that the fourth review reproduced all three rows from both sides,
  is supported by that review's log. Every number in the changed text is
  labelled floating point.
- *No collateral change.* The note is untracked in git and I found no
  earlier copy. The fourth review reports 1958 lines for the round-3
  version. The current note has 2033 lines. Section 10.4 accounts for 68
  of the added lines, the Section 8 item for about 6 and the Lasserre
  paragraph for 1. This is consistent with no other edits. The passages
  around the edits (the Section 4.6 table, the radius bullet, the closing
  paragraph of Section 4.6, the Summary scope and novelty paragraphs, and
  Section 7) read as the fourth review described them.
- *Consistent naming.* "Third review" means
  `reviews/robust-lb-chains-confirm-r2.md`, and "fourth review" means
  `reviews/robust-lb-chains-confirm-r3.md`. Every place where these names
  occur (Sections 4.6, 8, 10.3 and 10.4, and the Summary) follows this
  mapping.

## 5. The refusal, and remaining points (all optional)

### 5.1 Monotonicity in `M` (not applied): acceptable

The fourth review offered, as an optional point, that the relaxation's
value is nonincreasing in `M`. The note declined because the point was not
among this round's items and because "the note's statements do not depend
on it". The refusal is acceptable: the point was optional and outside the
task for this round.

I checked the fact itself.

- *Proved.* The localizing matrix of `2M^2 - x^2 - y^2` in the basis
  `(1, x, y)` is `2M^2 M_1` minus a matrix that does not depend on `M`.
  Here `M_1` is the order-1 moment matrix of the clique, a principal
  submatrix of the order-2 moment matrix. So raising `M` keeps every
  feasible point feasible. The value is also at most 0, because the Dirac
  measure at `0` is feasible.
- *Float.* `f1_between.log`: `M = 1.2, 1.4, 1.45` at `n = 8, 32` all give
  values at most `2.4e-7`.

**One caveat on the stated reason (optional).** The note does use the
range notation once: the Section 7 row says "ball `M = 1.1`–`1.5` up to
`n = 32`". Read as an interval, that range is justified only by the
monotonicity fact, whose proof is in the fourth review (Section 1) and not
in the note. Elsewhere the note names the three radii. So "do not depend
on it" is true only if the Section 7 range is read as the three tested
radii. Either of these would remove the ambiguity:

- write "`M = 1.1`, `1.3`, `1.5`" in Section 7; or
- add the one-line monotonicity remark.

The statement is not wrong under either reading.

### 5.2 "up to `n = 32`" in Section 7 (optional)

The same Section 7 row says "up to `n = 32`". This is the same kind of
wording as the Lasserre "`n <= 32`" that this round corrected. The runs
were at `n = 5, 8, 16, 32` (and `12, 24` in the third review). In a
summary table this is a fair shorthand. Matching the Lasserre paragraph is
optional.

### 5.3 Section 10.4, item 2 (cosmetic)

"values at most `1.2e-8`" is true. The actual maximum is `1.12e-8`. No
change is needed.

## 6. Commands run

All were run with `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1` on a machine
with a load average of about 0.2. All solves are floating point (cvxpy
1.9.3, Clarabel 0.11.1, SCS 3.3.1), and none is certified. Total wall
time was under 2 minutes.

| Command | Log | What | Kind |
|---|---|---|---|
| `python3 revision3_chains.py radius` (note's script, from `chains/`) | `rerun/revision3_radius.out` | reproducibility; `diff` with `logs/revision3_radius.log`: identical | float |
| `python3 revision3_chains.py waki` (note's script, from `chains/`) | `rerun/revision3_waki.out` | reproducibility; `diff` with `logs/revision3_waki.log`: identical | float |
| `python3 e1_two_sides.py waki` (fourth review's script, run in its directory, output to my directory) | `rerun/e1_waki.out` | reproducibility; result lines identical to `e1_waki.log` | float |
| `python3 f1_moment.py bounds` (own code) | `f1_bounds.log` | moment side: univariate multipliers with `\|y_alpha\| <= 1` and with the scaled bounds; opposite orientation with the scaled bounds and without bounds; `n = 5, 8`; Clarabel and SCS | float |
| `python3 f1_moment.py lasserre` (own code) | `f1_lasserre.log` | opposite orientation + ball, `M = 1.1, 1.3, 1.5, 2` at `n = 5, 8, 12, 16, 24, 32`; `M = 10` at `n = 5, 8`; Clarabel | float |
| `python3 -c "import f1_moment as F; ..."` (own code) | `f1_between.log` | ball `M = 1.2, 1.4, 1.45` at `n = 8, 32` | float |

All paths are relative to `reviews/robust-lb-chains-final-confirm-r1-checks/`.

I also read the following:

- `chains/logs/revision2_sos.log`, `revision2_independent_sos.log` and
  `revision1_sos.log`;
- the third review's `d2_sdp.log`, `d4_more_placements.log`,
  `d5_radius_n.log` and the placement code in `d2_sdp.py`;
- the fourth review's `e1_waki.log` and `e1_radius.log`.

No literature was needed: this round changed no statement about prior
work.
