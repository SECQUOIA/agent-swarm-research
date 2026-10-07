# Check of the non-dyadic certificate computations in `decomposition-certificates.md` (Sections 5.2–5.3)

Date: 2026-09-30. Scope: the computed numbers in Sections 5.2 and 5.3 of
[`../theory-decomposition/decomposition-certificates.md`](../theory-decomposition/decomposition-certificates.md)
([D] below). These are certificates centred at a non-dyadic `x*` (random linear terms `c`). The
question is whether the closed leaf-cell intersection test in
[`../theory-decomposition/dp_certificate.py`](../theory-decomposition/dp_certificate.py)
loses pairs through rounding, as it did in the RC runs of `extension-adaptive.md` (its Section A.5
and Section F, item 6), and whether that changes any reported number. The proven theorems were not
re-examined.

Scripts and logs: [`decomposition-nondyadic-check-checks/`](decomposition-nondyadic-check-checks/).

## 1. Result

**Verdict: two numbers change.** Both are zero-slope gaps in the `n = 8` table of Section 5.3:

| `h` | gap, zero slopes, as reported | with the widened or exact test |
|---|---|---|
| `2^-2` | `1.72e-1` | `1.88e-1` |
| `2^-4` | `3.12e-2` | `3.17e-2` |

Every other number in Sections 5.2–5.3 is unchanged at the printed precision:

- all roots, gaps and sizes of the E2 table;
- the whole E3 table (roots and validity margins);
- the review's validity margins quoted in Section 5.2;
- the E4 table;
- the text statements (`≈ 1.6 h^2`, the stall at `2.2e-3`, the floor `2|lambda_1| h = 3.84e-6`,
  the `theta^2` scaling).

In more detail:

- **The pairs are lost, as suspected.** In every non-dyadic certificate of Sections 5.2–5.3, the
  closed test on rounded edges misses some (leaf, cell) pairs that touch in exact arithmetic. The
  count is 26 to 7,657 pairs per certificate. It never misses a pair whose boxes overlap with
  positive length. At `x* = 0`, no pair is lost.
- **The fix recovers exactly the intended pairs.** Widening the test by `1e-12` gives exactly the
  pair set of a closed test on exact rational edges, which is the pair set of Definition 1.2 and
  Lemma 1.5. The roots of the two versions are bit-identical in all 34 certificates of E2, E3
  and E4.
- **Sizes are unaffected.** Sizes count boxes, not pairs, and the floating-point box filters of
  `shells` keep the same boxes as exact arithmetic (0 mismatches).
- **The two first-version numbers were still valid lower bounds, but for a slightly different
  certificate.** Dropping only touching pairs keeps the bound valid (Section 4.3), so they were
  gaps of valid bounds. They were not the gaps of the certificate the note defines, which
  includes the touching pairs. The defined certificate's gap is larger, by `1.6e-2` at `h = 2^-2`
  and by `5.2e-4` at `h = 2^-4`.

## 2. The mechanism in `dp_certificate.py`

`shells` computes the edges of level `j` as `p - R_j + g_j k` in floating point. It computes the
central boxes as `p + (corner - 1) h` and `L + h`. For a non-dyadic centre `p`, an edge shared by
boxes of different levels is computed by different operations on each side. An example is
`p - R_j + g_j 2^mu` against `p - R_{j-1}`. The two results can differ by one rounding unit. The
largest difference between a computed edge and its exact value in these runs is `2.2e-16`.

`certificate` pairs boxes with the closed test `lo_D <= u_B and hi_D >= l_B` in two places:

- the leaves of bag `t` against the cells of `S_t`;
- the leaves of bag `t` against the cells of the child separator `S_{t+1}`.

When two boxes touch in exact arithmetic but the rounded edges leave a one-unit gap, the test drops
the pair. For `x* = 0`, all edges are dyadic and exact, so nothing is dropped.

## 3. What was run

`nondyadic_check.py` defines `certificate_mode`. It is `dp_certificate.certificate` with a
selectable pairing test:

| mode | test |
|---|---|
| `closed` | closed test on the rounded edges (the original) |
| `tol` | closed test widened by `1e-12` (the fix used in `adaptive/rc_lib.py`) |
| `exact` | closed test on exact rational edges |
| `open` | only pairs whose boxes overlap with positive length in exact arithmetic |

The exact edges are computed with `fractions.Fraction` from the same floating-point `x*` and `h`.
They are the exact edges of the partition the code intends. Every run also counts, per
certificate:

- the pairs on which the modes differ;
- disagreements between the floating-point and exact box filters of `shells`;
- the largest edge error.

The experiment functions `E2`, `E3` and `E4` of `run_experiments.py` were run unchanged, with
`run_experiments.certificate` replaced by `certificate_mode`. `E4m5` is `E4` restricted to
`theta >= 1/32`, the rows that Section 5.3 quotes. The `theta = 1/64` row appears in the log but
not in the note, and the dense pair matrices would need about 10 GB for it.

**Regression.** In `closed` mode, the output is identical to `logs/E3_validity.log` and
`logs/E2_slopes.log`, and to the rows `theta = 1/2 … 1/32` of `logs/E4_theta.log`.

`review_valid_tol.py` reruns the review's validity check (`indep_dp.py valid 5 0 3 6` and
`valid 6 1 2 5`, whose margins Section 5.2 quotes). It widens the two closed tests of the review's
code in memory and does not modify the review's file. The review's code builds edges the same way,
so its earlier agreement with the note did not rule out a shared effect.

## 4. Findings

### 4.1 Pairs

Pairs per certificate, summed over bags. "Lost" means pairs in the exact closed pair set but not
in the rounded closed test.

| experiment | certificates | lost by the rounded test | lost with positive overlap | `tol` ≠ `exact` | box-filter mismatches |
|---|---|---|---|---|---|
| E3, `n = 4`, seed 0, `h = 2^-6`, `theta = 1/8` | 2 | 1,626 of 64,283 | 0 | 0 | 0 |
| E3, `n = 6`, seed 0, `h = 2^-8`, `theta = 1/8` | 2 | 3,732 of 187,932 | 0 | 0 | 0 |
| E3, `n = 6`, seed 1, `h = 2^-5`, `theta = 1/4` | 2 | 545 of 25,344 | 0 | 0 | 0 |
| E3, `n = 5`, `c = 0` | 2 | 0 | 0 | 0 | 0 |
| E2, `n = 8`, `h = 2^-2, 2^-4, 2^-6` | 2 each | 1,173; 4,294; 6,170 | 0 | 0 | 0 |
| E2, `n = 8`, `h = 2^-8 … 2^-16` | 10 | 6,458 each | 0 | 0 | 0 |
| E4, `n = 3`, `h = 2^-14`, `theta = 1/2 … 1/32` | 2 each | 26; 118; 479; 1,936; 7,657 | 0 | 0 | 0 |
| Section 5.4 samples, `x* = 0` (`n = 4, 8`) | 2 | 0 | 0 | 0 | 0 |

For comparison, the E2 certificate at `h = 2^-16` has 765,591 exact pairs, of which 286,124 only
touch. The rounded test lost 2.3% of those touching pairs. The review's code, rerun with the
widened test, gains 1,413 pairs (`n = 5`) and 212 pairs (`n = 6`).

### 4.2 Numbers

Differences between the full-precision roots, `l_r(closed) - l_r(exact)`
(`logs/compare.log`):

- **E2.** The difference is `+1.383e-5` (affine slopes) and `+1.563e-2` (zero slopes) at
  `h = 2^-2`, and `+5.176e-4` (zero slopes) at `h = 2^-4`. It is exactly 0 in the other 13
  certificates. The gaps with the exact test are:
  - `h = 2^-2`, affine: `1.0294e-1` (was `1.0293e-1`); the note prints `1.03e-1` either way;
  - `h = 2^-2`, zero: `1.8756e-1` (was `1.7193e-1`);
  - `h = 2^-4`, zero: `3.1740e-2` (was `3.1222e-2`).
- **E3.** The difference is exactly 0 in all 8 certificates. The printed output, including the
  margins `max(l - phi^grid)`, is identical in all modes except `open`.
- **E4** (`theta = 1/2 … 1/32`). The difference is exactly 0 in all 10 certificates.
- **Review's validity check.** With the widened test, the output is identical to
  `valid_n5_seed0.log` and `valid_n6_seed1.log`: `l_r`, and the margins `-1.435e-7` and
  `-1.787e-6`.

Why only the coarsest E2 certificates change: a lost touching pair matters only when it attains
the minimum in some `beta`. That happens only when the minimizing configuration crosses a face
between large boxes, here at `h = 2^-2` and `2^-4` with zero slopes.

### 4.3 The first-version numbers are valid lower bounds

A certificate that uses only pairs whose boxes overlap with positive length still satisfies the
conclusion of Lemma 1.3. In the proof of Lemma 1.3, the leaf `B ∋ z = (s, y)` can always be chosen
with `int B_{S_t} ∩ int D ≠ ∅`:

1. Take points `z_k -> z` with `(z_k)_{S_t} ∈ int D`, each in the interior of some leaf.
2. Some leaf contains infinitely many of them.
3. That leaf is closed, so it contains `z`.

The same argument, with points in `int B_{S_u}`, chooses the child cell `D' ∋ z_{S_u}`. So (CM)
and (LC) are only needed for such pairs.

The rounded closed test keeps all of these pairs (column "lost with positive overlap" is 0). Its
root is therefore at most the `open`-mode root, which is a valid bound. Numerically,
`l_r(open) <= f*` in all 34 certificates of E2, E3 and E4. For E4 this is read from the printed
gaps, which are all positive. The `open`-mode E3 margins are the same as in the table (all
negative).

So the first-version numbers were gaps of valid bounds. They were not the certificate of
Definition 1.2 and Lemma 1.5, and they depended on rounding.

**Side remark, not a correction.** Touching pairs have a large effect on these numbers. With
positive-overlap pairs only:

- the E2 zero-slope stall is `4.4e-4` instead of `2.2e-3`;
- the E4 zero-slope floor is `1.921e-6 = |lambda_1| h` instead of `3.837e-6 = 2|lambda_1| h`.

This agrees with the note's explanation of the floor: drift up to `2h` needs a copy across a
touching face. Whether the lower bounds of [D] would still hold if Definition 1.2 used interior
intersections was not checked.

**Bearing on `extension-adaptive.md`** (an observation; its RC runs were not rechecked here). Its
Section A.5 says that a dropped pair makes "the computed `l_r` … too high, so it is not a valid
bound". The `rc_lib.py` docstring says the same. By the argument above, "too high" (above the
bound Lemma 1.5 defines) is correct. "Not a valid bound" does not follow as long as no
positive-overlap pair is lost. That was verified here for [D]'s runs; RC uses the same `shells`
function, but I did not check RC. The practical conclusion there (widen the test, because the
closed-test results depend on rounding) is unaffected. Its Section D says that the non-dyadic
computations of [D] were not checked; this review answers that point.

## 5. Corrections for `decomposition-certificates.md`

1. **Section 5.3, `n = 8` table.** In row `2^-2`, change the zero-slope gap `1.72e-1` to
   `1.88e-1`. In row `2^-4`, change `3.12e-2` to `3.17e-2`. No other cell changes. The text below
   the table remains correct.
2. **Section 5, opening paragraph.** Add after the sentence on shell boundaries:
   "(Leaf, cell) pairs are found by a closed test on these rounded edges. For a non-dyadic `x*`
   (Sections 5.2–5.3), this misses some pairs that touch in exact arithmetic (26 to 7,657 per
   certificate). Widening the test by `1e-12` recovers exactly the pairs of Definition 1.2.
   This changes two zero-slope entries of the `n = 8` table in Section 5.3 and nothing else.
   The first-version values were valid lower bounds, because only touching pairs were lost
   (`reviews/decomposition-nondyadic-check.md`)."
3. **`dp_certificate.py`.** Widen both closed tests in `certificate` by `1e-12`, as in
   `adaptive/ls_lib.interval_pairs`, so that reruns compute the certificate of Lemma 1.5. In
   these runs, the widened set equals the exact set. A tolerance must stay below the narrowest
   box width; boxes clipped at `±1` can be as narrow as `1e-15` in general. Only
   `run_experiments.py` and `revision_checks.py` call `certificate`, and the latter uses
   `x* = 0`. The other importers, including `rc_lib.py`, use only `shells`, which does not
   change.
4. **`logs/E2_slopes.log`.** Rerun E2 after item 3, or append a line with the two corrected
   values. E3 and E4 print the same output with the widened test (checked), so their logs can
   stay.
5. **Section 7 (commands) and Section 8.** These need no change beyond a pointer to this
   check, if the author wants one.

## 6. Commands run

All commands were targeted and run from `reviews/decomposition-nondyadic-check-checks/` with
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`. No project-wide verification was
run, and no CI results were consulted.

| Command | Logs | Result |
|---|---|---|
| `./run_all.sh`: `python3 nondyadic_check.py {closed,tol,exact,open} {E3,E2,E4m5,E1x0}`, then `python3 compare.py` (8.5 min) | `logs/{E3,E2,E4m5,E1x0}_{closed,tol,exact,open}.log`, `logs/compare.log` | Section 4 |
| `diff` of the `closed`, `tol` and `exact` outputs against `theory-decomposition/logs/{E3_validity,E2_slopes,E4_theta}.log` | none | `closed` identical; `tol` and `exact` identical except the two E2 entries |
| `python3 review_valid_tol.py 0`; `python3 review_valid_tol.py 1e-12` | `logs/review_valid_tol0.log`, `logs/review_valid_tol1e-12.log` | identical to the review's `valid_*.log` in both cases |

Not checked:

- the E4 row `theta = 1/64`, which appears in the log but not in the note;
- Section 5.4 beyond two sample certificates at `x* = 0` (dyadic edges, no pairs lost);
- the RC runs of `extension-adaptive.md`.
