# Referee check of the third revision of "Split-robust lower bounds for single-tree spatial branch-and-bound on paths"

Date: 2026-09-30. Note checked:
`research-20260929/theory-robust-lb/robust-lower-bound.md`, the third
revision (1545 lines). Its changes are listed in Section 10.3. The report
that asked for them is `reviews/recheck-robust-lb-confirm.md` (the
"confirmation"). I wrote neither the note nor any earlier report. My script
and log are in `reviews/robust-lb-confirm-r1-checks/`. They share no code
with the authors, the review, the recheck or the confirmation.

Following `AGENTS.md`, I ran only targeted checks: no project-wide
verification and no CI. I did not commit anything or edit the note.

No copy of the second revision exists. The only other copy
(`/tmp/robust-lower-bound.v1.md`) is the first version. So I judged each
revised passage against the confirmation's quotations of the old wording
and against the evidence.

## Verdict in brief

All six requested changes are applied correctly. I recomputed every number
that changed, with my own code, and every one agrees with the note. The two
items the authors did not apply were optional, and the reasons given are
sound. Nothing is strengthened. The one wider claim is the class-(a)
ceiling range, and it grew because of a correction (1.073 became 1.075).
The authors also found, and fixed, a problem nobody had asked about: four
`E_d` "lower bounds" had been rounded up. I found no remaining problem.

| Item | Verdict |
|---|---|
| 1. `d^2 E_d` range wrong for odd `d` | **fixed.** Recomputed: even `d` 0.0949–0.1803, odd `d` 0.1291–0.4058. |
| Extra: four `E_d` lower bounds rounded up | **fixed.** All six printed bounds are now at or below the grid-LP values. The Section 3.4 figure `> 0.0509` is right (0.05095). |
| 2. "independently" in Summary 6 | **fixed.** The Section 9 table was corrected too. |
| 3. Section 10.2 opening sentence | **fixed**, and the old wording is noted. |
| 4. Scope of the ceiling range (optional) | **fixed; goes beyond the request.** I recomputed `mu0` for all 20 sets: class-(a) ceilings are 1.0219–1.0752 at the 19 non-reference sets. |
| 5. Shares of `c y^2` (optional) | **fixed.** |
| 6. Bracket precision; `mu < mu0` evidence (optional) | **fixed.** Widths and the 0.110 margin recomputed. |
| Not applied: balanced-split rows | **acceptable.** |
| Not applied: "independent estimate" in Section 6.1 | **acceptable.** |

## 1. Each item, checked from scratch

### Item 1. Range of `d^2 E_d(L)` for odd `d`, and the rounded-up bounds

**Text.**
- Summary item 3 (lines 106–109) now reads "about `0.095/d^2` to `0.18/d^2`
  for even `d = 2, 4, ..., 12` at `y1 = 0.38`; odd degrees add nothing,
  `E_{2k+1} = E_{2k}`".
- Section 3.3 (lines 680–689) says the same. It explains `E_{2k+1} = E_{2k}`
  by evenness and gives the odd-`d` range as 0.13–0.41.
- Section 10.2 item 10 (lines 1447–1451) is annotated.

**Mathematics.** `L` is even. If `p` is a best approximation of degree at
most `2k+1`, then so is `p(-y)`, and their average is even with no larger
error. An even polynomial of degree at most `2k+1` has degree at most `2k`.
So `E_{2k} <= E_{2k+1}`, and the reverse inequality is trivial. The argument
in the text is this one.

**Recomputation.** I used a different basis and grid from the authors' and
the confirmation's. My LP uses a Legendre basis on 12,001 uniform points,
plus 3,001 Chebyshev extrema and the kinks `±y1`. The upper value is the
error of the LP polynomial on `2e6` points. At `y1 = 0.38`:

| `d` | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| grid-LP `E_d` | 0.04508393 | 0.04508393 | 0.01009008 | 0.01009007 | 0.00263494 | 0.00263493 | 0.00253622 | 0.00253623 | 0.00171648 | 0.00171648 | 0.00091097 |
| `d^2 E_d` | 0.1803 | 0.4058 | 0.1614 | 0.2523 | 0.0949 | 0.1291 | 0.1623 | 0.2054 | 0.1716 | 0.2077 | 0.1312 |

- **Even `d`.** The minimum is 0.0949 (`d = 6`) and the maximum 0.1803
  (`d = 2`), as stated ("about 0.095 (`d = 6`) and 0.180 (`d = 2`)").
- **Odd `d`.** The range is 0.1291–0.4058, as stated ("0.13 to 0.41"). For
  every odd `d`, `d^2 E_d > (d-1)^2 E_{d-1}`, as stated.
- **`E_{2k+1}` against `E_{2k}`.** The lower bounds differ by at most
  `1.2e-8`. The note says "about `1e-8`".
- **Brackets.** My brackets have width at most `8.3e-8`. The authors' are at
  most `8.0e-8` (`logs/revision3_checks.log`). The recheck's `E_4` and `E_8`
  widths are `7e-8` and `5e-8` (`check_gamma.log`). The review printed
  `[x, x]` to 5 decimals (`check5_props.log`). So Section 3.3's "width at
  most about `1e-7`" and "to the 5 decimals it printed" are accurate.

**Rounded-down lower bounds.** Section 3.3 now prints `E_2 >= 0.04508`,
`E_4 >= 0.01009`, `E_6 >= 0.002634`, `E_8 >= 0.002536`, `E_10 >= 0.001716`
and `E_12 >= 0.000910`. Each is at or below my grid-LP value.

The authors say the old values were rounded up. The first version
(`/tmp/robust-lower-bound.v1.md`, line 512) and the recheck's table
(`robust-lb-recheck.md`, lines 128–132) show `E_2 >= 0.0451`,
`E_4 >= 0.0101`, `E_8 >= 0.00254` and `E_10 >= 0.00172`. All four exceed the
LP values, so the correction was needed and is right.

**Section 3.4.** The band width is `eps_v + eta (1-y1)^2 = 0.03922`. Then
`2 E_2 - 0.03922 = 0.05095 > 0.0509`, as the text says.

### Item 2. "Checked independently"

- Summary item 6 (lines 139–141) now reads "both consistency-checked (not
  certified) for class (a) with `G <= 2`". This matches
  `logs/verify_leaves.log`, which covers class (a), `eps = 1e-4`, `G = 1, 2`:
  - 620 leaves, with maximum excess `2.75e-16`;
  - 618 split boxes, with maximum residual `1.2e-15` and the closest value
    `2.187e-6` below the target.
- The Section 9 file table (line 1269) now says "consistency checks (not
  certificates)".
- Section 10.2 item 5 is annotated.
- `grep` finds "independent" elsewhere only for the review's code, for the
  gadgets, and in Section 6.1's "independent estimate" (see Section 2).

### Item 3. Opening of Section 10.2

Lines 1365–1368 read: "No count or computed base changed; Lemma 1.3 was
broadened and Theorem 4.3(3) gained a proved cap." A note gives the old
wording. This is accurate: Section 10.2 items 6 and 2 describe those two
changes.

### Item 4. Scope of the ceiling range

**Text.** The following now say "for class (a), 1.022–1.075 at the 19
other parameter sets of the scan (in Section 6.5)":
- the Summary (lines 51–53);
- Section 4.4 (lines 956–960);
- the status table (line 1184);
- Section 8 (lines 1196–1198).

A new paragraph in Section 6.5 (lines 1132–1140) gives the endpoints and
the sets. It also says that no class-(a) base was computed at
`(0.38, 0.005, 0.002)`. Section 10.2 item 4 is annotated.

**Recomputation, step 1: the class-(a) gap.** The ceiling uses the
closed-form class-(a) gap `y1^2 (1-A)/A` at every set, including the 12 sets
where the scan ran no class-(a) job. So I first checked that this is the
exact class-(a) root gap, not only a lower bound.

- **By hand.** With `s = y^2`, `L` is concave in `s` and `U` is concave in
  `s`. So `max_s (q s - U) = max(0, q - A)`, and for
  `q in [y1, 1]`, `max_s (L - q s) = y1^2 (1-q)/q`. The sum is minimized at
  `q = A`, which gives `y1^2 (1-A)/A`.
- **Numerically.** A scalar search over `q` on a `2e5`-point grid agrees
  with the closed form to `3.3e-9` at all 20 sets.

So the ceiling formula is right at every set.

**Recomputation, step 2: `mu0`.** I searched over corner boxes
`[-1,-a] x [-1,-b] x [-1,-c]` with two methods:
- an `81^3` grid, then a Powell polish from the five best grid points;
- differential evolution with polishing, as a cross-check.

The two methods agree to 5 decimals at every set. They also agree with the
authors' Nelder–Mead values (`logs/revision3_checks.log`) within `5e-5`,
which is the rounding of the authors' 4-decimal output. The results:
- reference set: `mu0 = 2.3866`, ceiling 1.0624 per variable;
- 19 non-reference sets: class-(a) ceilings from **1.0219** at
  `(0.38, 0.05, 0.2)` to **1.0752** at `(0.38, 0.005, 0.002)`;
- `scan_bd.log` ran only b4 and b6 at `(0.38, 0.005, 0.002)`, as stated.

I also reran the authors' `revision3_checks.py` (3.3 s, the "about 3
seconds" of Section 9). Its output is byte-identical to
`logs/revision3_checks.log`.

**Scope.** "1.022–1.075" is right for class (a) at the 19 sets. It is not a
strengthening: the old range was 1.022–1.073, so the upper end rose. The
"about 1.063 at the reference parameters" claim is unchanged; the reference
value is 1.0624.

### Item 5. Shares of `c y^2`

Theorem 4.3(3), lines 884–890, now reads: "each factor is at least its share
of `c y^2`, and the shares add up to `c y^2 >= c/4`". The argument is
unchanged:
- with `r = 0` and nonnegative shares `s_1 + s_2 = 1`, the factor minima on
  `[-1,-1/2]^3` sum to at least `c/4`;
- so `V >= c/4`, and `(1/64) exp(mu/4) >= 1` once `mu >= 4 ln 64 = 16.6355`.

The misreading the confirmation pointed out is gone.

### Item 6. Bracket precision, and evidence for `mu < mu0`

- **Brackets.** "Agree to 8 digits" is replaced by "width at most about
  `1e-7`", which is accurate (item 1 above).
- **`mu < mu0`.** From `logs/scan_bd.log` (26 rows, 20 distinct sets) and my
  `mu0` values, every row has `mu < mu0`. The smallest margin is 0.110, for
  b6 at `(0.30, 0.02, 0.002)`, where `mu = 2.252` and `mu0 = 2.3621`. This
  matches Section 6.5 and Section 10.3 item 6.
- **Annotation.** Section 10.2 item 4 now says that `mu0` had been computed
  for only 8 of the 20 sets at the time. `logs/revision2_checks.log` indeed
  has 8 sets.

### Other changed passages

- **Header (lines 11–15) and Section 8 review history (lines 1247–1254).**
  Both describe the confirmation accurately ("every fix applied, no
  mathematical error; one range wrong for odd `d` and a few wording
  points"). Both say that the third revision has not been rechecked.
- **Section 6.5 table.** The `b_d`-row ceilings recompute as follows, all
  matching the table:
  - b4 at the reference parameters: 1.0062;
  - b4 at `(0.30, 0.005, 0.002)`: 1.0198;
  - b6 at the reference parameters: 1.0019;
  - b6 at `(0.50, 0.005, 0.002)`: 1.0062 with the log's `gamma = 0.00734`
    (1.0061 with the rounded 0.0073).
- **Status table, Prop 3.3 row.** It credits the third-revision brackets. The
  "valid lower bounds" wording is correct: a grid LP bounds the continuous
  minimax error from below.
- **Section 10.3.** Each entry matches what was done. The commands listed
  match the files.

## 2. Items not applied

1. **Balanced-split rows in Sections 6.1 and 8 (optional).** Both sections
   limit the reproduction to "classes (a), b4 and b6 with the theorem's base
   split". That phrase excludes the b6-balanced and env-balanced rows.
   Section 10.2 item 3 says explicitly that neither review's code ran them.
   The refusal is justified.
2. **"Independent estimate" in Section 6.1.** Here "independent" describes
   the method: a grid plus local search, separate from the LP and the root
   finder being checked. It does not describe who did the check. The same
   paragraph says "so it is a consistency check, not a certificate". The
   log line produced by `verify_leaves.py` uses the same phrase. The
   confirmation's concern was Summary 6, where the word could be read as a
   check by another party, and that is fixed. Keeping the word here is
   acceptable.

## 3. Silent strengthening and withdrawn claims

Nothing is strengthened. Every change either narrows or corrects a
statement:
- the `d^2 E_d` range is restricted to even `d`;
- four printed lower bounds are lowered, and so is the Section 3.4 figure;
- "independently" is removed;
- the ceiling range is widened to include 1.075;
- the Section 10.2 claims are annotated.

The added material is the 20-set `mu0` computation and the odd-`d` values.
Both rest on logged computations that I reproduced. Superseded statements
in Sections 10.2 items 4, 5 and 10 are kept for history and clearly point to
Section 10.3.

## 4. Remaining problems

None.

Two small observations need no change:
- **Section 10.3 opening.** It says "One stated range widened slightly
  (item 4)". Item 1 also restricted another range and lowered four printed
  bounds. The items describe this, so nothing is hidden.
- **Section 3.3 cites `logs/band_Ed.log`.** That log prints `E_d` rounded
  to nearest (for example `E_8 = 0.00254`). The rounded-down 8-digit values
  are in `logs/revision3_checks.log`, which is cited alongside it.

## 5. Checks run

All commands were run with
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1`,
single-threaded and time-limited. They are targeted checks only: no
project-wide checks and no CI. The note and the authors' files were not
modified.

| Command | Purpose | Result |
|---|---|---|
| `python3 check_r1.py > logs/check_r1.log`, in `reviews/robust-lb-confirm-r1-checks/` (30.5 s) | (1) `E_d(L)`, `d = 2..12`, Legendre-basis grid LP; (2) class-(a) gap by scalar search against the closed form at 20 sets; (3) `mu0` by grid plus Powell and by differential evolution at 20 sets, ceilings, `mu < mu0` for 26 rows; (4) arithmetic | Section 1; all agree with the note |
| `timeout 600 python3 revision3_checks.py > /tmp/r1_rev3_rerun.log`, in `theory-robust-lb/` (3.3 s), then `diff` against `logs/revision3_checks.log` | reproducibility of the authors' third-revision log | identical |
| Reading `theory-robust-lb/logs/{scan_bd,band_Ed,revision2_checks,revision3_checks,verify_leaves}.log`, `robust-lb-review-checks/logs/check5_props.log`, `robust-lb-recheck-checks/logs/check_gamma.log`, `recheck-robust-lb-confirm-checks/logs/check_confirm.log`, `/tmp/robust-lower-bound.v1.md` | evidence for items 1, 2, 4 and 6 | Section 1 |
