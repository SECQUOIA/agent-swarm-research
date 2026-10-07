# Confirmation of the non-dyadic revision of `decomposition-certificates.md` (round 1)

Date: 2026-09-30. Scope: the revision of
[`../theory-decomposition/decomposition-certificates.md`](../theory-decomposition/decomposition-certificates.md)
([D] below) and
[`../theory-decomposition/dp_certificate.py`](../theory-decomposition/dp_certificate.py) made in
response to [`decomposition-nondyadic-check.md`](decomposition-nondyadic-check.md). I checked
each item from scratch, recomputed the changed numbers, and judged the one item the reviser did
not apply. Scripts and logs are in
[`decomposition-nondyadic-confirm-r1-checks/`](decomposition-nondyadic-confirm-r1-checks/).

## 1. Verdict

**All five applied items are correct, and the refusal of item 6 is justified. Two small wording
errors remain; neither affects a number or a proof.**

- The two corrected table entries and every other number I recomputed match the revised note to
  the printed precision.
- The new "Touching pairs" remark after Lemma 1.3 is correct. It adds a proved statement but does
  not change Definition 1.2 or any lower bound, so nothing was strengthened beyond what the proof
  supports.
- An independent exact pair check, written with a different method from both
  `check_pairs_exact.py` and the check's `nondyadic_check.py`, gives the same pair counts as the
  revised note in all 20 partitions.

Remaining issues (Section 3):

1. Section 8.2, item 6 says that the `adaptive/rc_lib.py` docstring says a dropped pair makes
   `l_r` "not a valid bound". It does not.
2. The `dp_certificate.py` docstring says the unwidened test "gives a bound higher than
   Lemma 1.5's". It can give a higher bound, but in 31 of 34 certificates the bound was the same.

## 2. Item-by-item check

| Item | Claim | Check | Result |
|---|---|---|---|
| 1 | `n = 8` table: zero-slope gap `1.88e-1` at `h = 2^-2`, `3.17e-2` at `h = 2^-4`; full precision `1.8756e-1`, `3.1740e-2`; first version `1.7193e-1`, `3.1222e-2`; affine gap at `2^-2` `1.02928e-1 -> 1.02942e-1`; `6.42227e-3` unchanged | `full_precision.py` evaluates both certificates with `PAIR_TOL = 0` and `1e-12` | `1.719302e-1 -> 1.875598e-1`, `3.122246e-2 -> 3.174009e-2`, affine `1.029284e-1 -> 1.029422e-1`, `6.422269e-3` both. All match; table rounding correct (`1.88e-1`, `3.17e-2`, `1.03e-1`). Text below the table (`≈ 1.6 h^2`, stall at `2.2e-3`) still holds. |
| 1 | Only these two cells change | E2 rerun with the current code; E2 rerun with `PAIR_TOL = 0` | Current code: byte-identical to `logs/E2_slopes.log`. `PAIR_TOL = 0`: identical to the check's `E2_closed.log` (the first version), and differs from the current log only in the two cells. |
| 2 | Section 5 opening: closed test on rounded edges; first version missed 26 to 7,657 touching pairs per certificate; widening by `1e-12` recovers exactly the pairs of Definition 1.2; first-version values were valid lower bounds; nothing changes at `x* = 0` | `pairs_ranges.py` (independent method, below) over all 20 partitions of `check_pairs_exact.py` | Same counts in every row: E2 1,173, 4,294, 6,170, then 6,458; E3 1,626, 3,732, 545, 0; E4 26, 118, 479, 1,936, 7,657 (30,442 at `theta = 1/64`); 0 at `x* = 0`. No lost pair has positive-length overlap; no spurious pair; widened set = exact set in all 20. Smallest gap between non-meeting boxes `9.54e-7`; largest edge error `2.2e-16`. |
| 3 | Remark after Lemma 1.3: (LC) and (CM) are needed only for pairs whose interiors meet | Proof read line by line | Correct. Points of `X0_{V_t}` whose `S_t`-part lies in `int D` accumulate at `z`, and the union of leaf interiors is open and dense, so the points can be taken inside leaf interiors. One leaf contains infinitely many of them; it is closed, so it contains `z`, and its projection's interior meets `int D`. The child cell is chosen the same way. The induction hypothesis is still stated for every cell. The remark says the bounds can be higher than those of Lemma 1.5, keeps Definition 1.2, and says Section 2 uses the definition as stated. It does not claim Lemma 1.4 or any lower bound for certificates that omit touching pairs. |
| 3 | Status table, Lemma 1.3 row | Read | Consistent with the remark. |
| 4 | `dp_certificate.py`: both closed tests in `certificate()` widened by `PAIR_TOL = 1e-12`; only `run_experiments.py` and `revision_checks.py` call `certificate()` | Code read; `grep` of all importers | Both tests are widened. Only those two files call `dp_certificate.certificate()`; `adaptive/check_staircase.py` and `reviews/decomposition-review-checks/indep_dp.py` define their own `certificate`. Other importers use `shells`, `min_subbox`, `phi`, `dphi`, `F` or `global_min`, which did not change. When a widened pair is 1 ulp apart, `min_subbox` gets `L1 > U1` and evaluates at `L1` (its `U1 - L1 <= 0` branch), so the added pairs are handled correctly. |
| 5 | `logs/E2_slopes.log` replaced; E3, E4 and `revision_checks.py` unchanged | E3 rerun; E4 rerun for `theta = 1/2 … 1/32`; item 2 of `revision_checks.py` (its only `certificate()` call) | E3 byte-identical to `logs/E3_validity.log`. E4 rows `theta = 1/2 … 1/32` identical to `logs/E4_theta.log`. `n = 9`, `x* = 0` certificate: gap `2.899e-05`, size 198,446, as in `logs/revision_checks.log`. |
| Bookkeeping | Header, Section 7 rows, Section 8.2 | Read; compared each number with the logs above | Accurate, except item 6 (issue 1 below). The header still says Sections 8.1 and 8.2 have not been rechecked; after this report, Section 8.2 has been rechecked. |
| 6 (not applied) | Did not edit `extension-adaptive.md` Section A.5 or `adaptive/rc_lib.py`; recorded the point in Section 8.2, item 6 | Read both files | The refusal is acceptable: both files belong to the extension note, which is under its own revision (`decomposition-adaptive-confirm-r2.md` is later than the check), and the check marked this item as an observation not rechecked on RC. Section A.5 (line ~602) still says "so it is not a valid bound", and Section D still says [D]'s non-dyadic computations were not checked. Those are for the extension note's reviser. |

**Independent pair check.** `pairs_ranges.py` differs in method from both earlier scripts:

- It builds the exact edges with `fractions.Fraction` directly from the formulas in `shells`:
  the central box, the level-`j` edges `p - 2^j h + 2^(j-1-mu) h k`, exact clipping at `±1`, and
  exact versions of the `ok` and `keep` filters. It does not round float edges to a lattice.
- It then checks that its exact boxes correspond one to one with the float output of
  `dp_certificate.shells`: the counts are equal and every edge differs by less than `1e-14`.
- It counts pair sets as index ranges over the cells sorted by exact lower edge, not with dense
  matrices. It asserts that the cells tile `[-1, 1]` and that the float cell edges are strictly
  increasing, which makes every pair set a contiguous range.

Its counts and smallest gaps are identical to `logs/check_pairs_exact.log` in all 20 rows. Its
edge-error column is `1.6e-16` instead of `5.6e-17` for the E4 rows, because it also measures
the edges of coordinates not used in pair tests. The overall maximum is `2.2e-16` in both.

## 3. Remaining issues

1. **Section 8.2, item 6 misquotes `adaptive/rc_lib.py`.** The item says: "Its Section A.5 and
   the `adaptive/rc_lib.py` docstring say that a dropped touching pair makes `l_r` 'not a valid
   bound'." The `rc_lib.py` docstring says only "(which makes l_r too high)". It has no
   "valid" wording, and the file is dated before the check. "Too high" agrees with the new
   remark. Only Section A.5 of `extension-adaptive.md` uses "not a valid bound". The error comes
   from the check (its Section 4.3) and was repeated in the task's issue list and in the
   reviser's suggested wording ("make the same change in the rc_lib.py docstring"), which is
   therefore unnecessary. **Fix:** in item 6, refer only to Section A.5 of
   `extension-adaptive.md`, or add that the `rc_lib.py` docstring says "too high", which is
   correct.
2. **`dp_certificate.py` docstring overstates the effect.** "The unwidened test (first version)
   drops such pairs, which gives a bound higher than Lemma 1.5's" reads as always strictly
   higher. In the runs, the bound was higher in 3 of 34 certificates: E2 at `h = 2^-2` (both
   slopes) and at `h = 2^-4` (zero slopes). The other 31 were identical. The note's remark says
   "can be higher", which is correct. **Fix:** "which can give a bound higher than Lemma 1.5's".

No other problem found. The E2, E3 and E4 tables, the Section 5.2 margins and the Section 5.3
text are consistent with the recomputed values. The Section 5.2 margins are the review's, whose
widened rerun was done by the check (`review_valid_tol.py`), not here.

## 4. Commands run

All commands were targeted and run from `reviews/decomposition-nondyadic-confirm-r1-checks/`
with `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1` and `timeout`. The
`theory-decomposition` files were imported unchanged; `run_tol.py` only overrides the module
constant `PAIR_TOL`. No project-wide verification was run, and no CI results were consulted.

| Command | Log | Result |
|---|---|---|
| `./run_all.sh`: `python3 run_tol.py 1e-12 E2`, `run_tol.py 0 E2`, `run_tol.py 1e-12 E3`, `run_tol.py 1e-12 E4m5` (2 min 17 s) | `logs/E2_tol1e-12.log`, `logs/E2_tol0.log`, `logs/E3_tol1e-12.log`, `logs/E4m5_tol1e-12.log` | E2 (current code) identical to `theory-decomposition/logs/E2_slopes.log`; E2 with `PAIR_TOL = 0` identical to the check's `E2_closed.log` (first version); E3 identical to `logs/E3_validity.log`; E4 `theta = 1/2 … 1/32` identical to `logs/E4_theta.log` |
| `python3 full_precision.py` | `logs/full_precision.log` | full-precision gaps of item 1 (Section 2) |
| `python3 pairs_ranges.py 6` (54 s) | `logs/pairs_ranges.log` | all 20 partitions: counts and smallest gaps identical to `theory-decomposition/logs/check_pairs_exact.log` |
| `python3 rc_item2.py` | `logs/rc_item2.log` | `n = 9`, `x* = 0`: gap `2.899e-05`, size 198,446, as in `logs/revision_checks.log` |
| `diff` of the logs above against the note's logs; `grep` of importers of `dp_certificate`; reading of `extension-adaptive.md` Sections A.5 and D and of `adaptive/rc_lib.py` | none | Section 2 |

Not rechecked here:

- The E4 root at `theta = 1/64`. It is not in the note, and the dense arrays of `certificate()`
  would need about 20 GB on this shared machine. Its pair set was checked: the widened set
  equals the exact set.
- The review's validity check with the widened test. The check did this rerun.
- Items 1, 3, 4 and 5 of `revision_checks.py`. They do not call `certificate()`. Item 1's
  closed test runs at `x* = 0`, where the edges are exact.
- The RC runs of `extension-adaptive.md`.
