# Confirmation of the fifth-round revision of `decomposition-certificates.md` (round 3)

Date: 2026-09-30. Scope: the changes to
[`../theory-decomposition/decomposition-certificates.md`](../theory-decomposition/decomposition-certificates.md)
([D] below) and
[`../theory-decomposition/compare_pair_tol.py`](../theory-decomposition/compare_pair_tol.py) made in
response to [`decomposition-nondyadic-confirm-r2.md`](decomposition-nondyadic-confirm-r2.md)
("the second confirmation" below). These are [D] Section 8.4, the edited Section 8.3, item 2, the
edited Section 8.2, item 3, the header, the two new rows of Section 7, the `compare_pair_tol.py`
docstring and the new logs `logs/theta64_chunked.log` and `.time`. I checked each item from
scratch, recomputed every changed number with a pair enumeration of my own, and judged the item the
reviser did not apply. Scripts and logs are in
[`decomposition-nondyadic-confirm-r3-checks/`](decomposition-nondyadic-confirm-r3-checks/).

## 1. Verdict

**All applied changes are correct. Every changed number was reproduced, the roots bit for bit.
No claim was strengthened beyond what the computations support. The item not applied is
acceptable. One sentence in the new Section 8.4, item 1 is imprecise (Section 3). It affects no
number or conclusion.**

- The clause "which the confirmation's count of 34 includes," is gone from Section 8.3, item 2.
  The added sentence is correct: the first confirmation's 34 certificates are the 32 with
  non-dyadic `x*` plus the two E3 certificates at `x* = 0`.
- I computed all 36 E2, E3 and E4 certificates at `PAIR_TOL = 0` and `1e-12` with a new script,
  `ranges_roots.py`. It finds the (leaf, cell) pairs by binary search over sorted cell edges. It
  uses neither the dense arrays of `certificate()` nor the row-chunked copy `chunked()`. Its
  68 roots for the 34 certificates with `mu <= 5` equal `logs/compare_pair_tol.log` bit for bit.
  At `theta = 1/64`, its roots equal the values in [D] bit for bit at both tolerances. So of the
  34 certificates with non-dyadic `x*`, 3 are higher, 31 are bit-identical and none is lower, as
  [D] now states.
- The memory figures are correct, and "more than 10 GB" is a correct lower bound for the peak
  memory of `certificate()` at `theta = 1/64`.

## 2. Item-by-item check

| Item | Claim in [D] | Check | Result |
|---|---|---|---|
| 8.4.1 / 8.3.2 | Clause deleted. The first confirmation's `run_all.sh` runs E4 only for `theta = 1/2 … 1/32` (`run_tol.py 1e-12 E4m5`, `mu = 1..5`). Its E4 log has five rows. It lists "The E4 root at `theta = 1/64`" under "Not rechecked here". Its 34 certificates are 16 E2, 8 E3 (two at `x* = 0`) and 10 E4. | Read `decomposition-nondyadic-confirm-r1-checks/run_all.sh`, `run_tol.py`, all its logs, and its Sections 1, 3 and 4; read [D] Section 8.3, item 2 | Confirmed. `run_tol.py` loops `mu in range(1, 6)` for `E4m5`. `logs/E4m5_tol1e-12.log` has five data rows. `E2_tol0.log` and `E2_tol1e-12.log` each have 8 rows × 2 slopes. `E3_tol1e-12.log` has 8 runs, and the last two are `seed=None` (`x* = 0`). 16 + 8 + 10 = 34. The clause is gone from Section 8.3, item 2. The replacement sentence ("these 32 plus the two E3 certificates at `x* = 0`") is correct. One sentence of item 1 is imprecise (Section 3). |
| 8.4.2 | `chunked()` differs from `certificate()` only in the row blocking. At `theta = 1/64`, roots `-0.0097876251980369196` (affine) and `-0.0097914614120943721` (zero) at both tolerances. Gaps `1.268e-09`, `3.837e-06` and size 1,374,385 match `logs/E4_theta.log`. The `theta = 1/32` control equals `logs/compare_pair_tol.log`. So 3 are higher, 31 bit-identical and none lower among the 34 with non-dyadic `x*`. | Read `chunked()` against `certificate()`; read `logs/theta64_chunked.log` and the second confirmation's `logs/all_roots.log`; independent recomputation (Section 2.1) | Confirmed. The only differences in `chunked()` are the 20,000-row blocks and the `tol` argument in place of the module constant. The blocks are concatenated in row order, so the pair order equals that of `np.nonzero` on the full matrix. The four roots in `theta64_chunked.log` equal those in `all_roots.log` and those from my own script. The gaps check against `f* = -0.0097876239302313976`. The second confirmation's log has 34 "bit-identical" rows (original against chunked), as [D] says. |
| 8.2.3 (edited) | "identical at full precision in the other 31 E2, E3 and E4 certificates with non-dyadic `x*` (Sections 8.3 and 8.4)" | Counts above | Correct: 3 + 31 = 34 = 16 E2 + 6 non-dyadic E3 + 12 E4. For two of the 31, the full-precision roots come from `chunked()` and not from the original `certificate()`, and Section 8.4, item 2 says so. My script, which uses a different pair method, gives the same roots. Section 8.3, item 3 still records the earlier "29 others" wording. That is appropriate for a revision log, and Section 8.4, item 2 says so. |
| 8.4.3 | Bag 0 at `theta = 1/64` has 686,738 leaves and its separator has 1,793 cells. The dense `float64` array takes 9.85 GB and each Boolean array 1.23 GB. The second confirmation estimates about 14 GB. Section 8.3, item 2 and the docstring now say "more than 10 GB". | Inline `shells()` computation; my script's size output; read `certificate()` | Sizes confirmed: bag 0 has 686,738 leaves, bag 1 has 685,854 and `S_1` has 1,793 cells (total 1,374,385). The arrays take `686,738 × 1,793 × 8 B = 9.851 GB` (9.17 GiB) and `1.231 GB` per Boolean array. In `certificate()`, the Boolean `meet` is still live while `np.where(meet, cbeta[None, :], np.inf)` allocates its `float64` result. The peak is therefore at least 11.08 GB (10.3 GiB), and "more than 10 GB" is correct in either unit. The second confirmation's "about 14 GB" is quoted correctly. |
| 8.4.3 | Only the `compare_pair_tol.py` docstring changed, so the output is unchanged | Rerun of `compare_pair_tol.py`; `stat` | Confirmed. The rerun output is identical to `logs/compare_pair_tol.log` apart from the per-line timing column (`diff` after removing it). The last line is "non-dyadic certificates: 32; tol=0 root identical: 29, higher: 3, lower: 0". Since the second confirmation (12:30), only [D], `compare_pair_tol.py` and the two new logs have changed. `dp_certificate.py` is unchanged (last changed at 11:55). |
| 8.4.4 / header | Cites the second confirmation. Says the fixes of Sections 8.1 and 8.4 have not been rechecked. | Read | Accurate. After this report, Section 8.4 has been rechecked, apart from the issue in Section 3. |
| Section 7, new rows | Chunked rerun (17 min, peak memory 0.84 GB) and inline `shells()` sizes | `logs/theta64_chunked.time`; the sizes above | Consistent. Wall time 17:16.82. Maximum RSS 838,732 kB (0.84 GB if kB is read as 1,000 bytes; 0.86 GB with 1,024). The size row agrees with my computation. The inline driver of the chunked rerun was not saved (`python3 -`), but its log header states what it computed, and `ranges_roots.py` reproduces its results. |
| Status table | No change | Read | Correct. No result changed status. |
| Not applied | No independent implementation of the chunked evaluation. The original `certificate()` was not run at `theta = 1/64` (more than 10 GB on a shared machine). | Judged | **Acceptable.** [D] says the roots were "rerun here with the same copy" and claims no independent method. The second confirmation checked `chunked()` bit for bit against the original on 34 certificates. My range-based computation (Section 2.1) now provides a check with a different pair method, and it agrees bit for bit. |

### 2.1 Independent recomputation with range-based pairs

`ranges_roots.py` imports `shells`, `min_subbox`, `dphi` and `global_min` unchanged from
`dp_certificate.py` and writes its own DP loop. For each pair test, it sorts the separator cells
by lower edge and asserts that both the lower and the upper edges are then strictly increasing.
With sorted edges, the closed test `lo_k <= u + tol` and `hi_k >= l - tol` selects the index
range `[searchsorted(hi, l - tol, 'left'), searchsorted(lo, u + tol, 'right'))`. The numbers
`u + tol` and `l - tol` are rounded exactly as in `certificate()`, so the pair set equals that of
the dense test. The minima over pairs (`off`, `beta`) are taken with `np.minimum.at`. A minimum
has no rounding error, so the pair order does not matter. `min_subbox` works elementwise with
basic arithmetic, so its values do not depend on how the pairs are batched.

Results (`logs/ranges_roots.log`; 19.5 min; peak memory 0.75 GB):

- Every case of `compare_pair_tol.py` (16 E2, 8 E3, 10 E4 with `mu <= 5`): 34 of 34 root pairs
  equal the log bit for bit.
- Pair counts: with `PAIR_TOL = 1e-12` they equal the `exact` column of
  `logs/check_pairs_exact.log` in every E2, E3 and E4 row. The difference between the two
  tolerances equals its `lost` column (for example, 1,173 at E2 `h = 2^-2` and 7,657 at E4
  `theta = 1/32`).
- `theta = 1/64` (`n = 3`, seed 0, `h = 2^-14`):

  | slopes | root, `PAIR_TOL = 0` | root, `PAIR_TOL = 1e-12` | pairs (0 / 1e-12) | gap | size |
  |---|---|---|---|---|---|
  | affine | `-0.0097876251980369196` | same | 6,547,340 / 6,577,782 | `1.268e-09` | 1,374,385 |
  | zero | `-0.0097914614120943721` | same | 6,547,340 / 6,577,782 | `3.837e-06` | 1,374,385 |

  The widened count, 6,577,782, is the exact count in `logs/check_pairs_exact.log`. The
  difference, 30,442, is its `lost` count.
- Over all 34 certificates with non-dyadic `x*`: 31 bit-identical, 3 higher, 0 lower. The two
  certificates at `x* = 0` are identical.

This check still shares `shells()` and `min_subbox()` with [D]. It independently tests the pair
enumeration and the chunking, which are what the `theta = 1/64` result depended on.

## 3. Remaining issue

1. **Section 8.4, item 1: "covers the same set as".** The item correctly says that the first
   confirmation's 34 certificates are "the 32 with non-dyadic `x*` of Section 8.3 plus the two E3
   certificates at `x* = 0`". The next sentence then says: "So its "3 higher, 31 identical"
   covers the same set as "3 higher, 29 identical" there." Those counts cover 34 and 32
   certificates, so the sets are not the same. The second confirmation's suggested wording
   included "plus the two `x* = 0` certificates", but that phrase was dropped. Also, the first
   confirmation did not use the words "3 higher, 31 identical" (it wrote "higher in 3 of 34
   certificates … The other 31 were identical"), so the quotation marks present a paraphrase as
   a quotation. No number or conclusion is affected. **Fix:** for example, "So its count (higher
   in 3 of 34, the other 31 identical) is the count of Section 8.3 (3 higher, 29 identical) plus
   the two certificates at `x* = 0`."

No other problem found.

## 4. Commands run

All commands were targeted and run with `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
MKL_NUM_THREADS=1` and `timeout`. The `theory-decomposition` files were imported unchanged. No
project-wide verification was run, and no CI results were consulted.

| Command | Log | Result |
|---|---|---|
| `python3 ranges_roots.py` (from `decomposition-nondyadic-confirm-r3-checks/`, 19.5 min, peak memory 0.75 GB) | `logs/ranges_roots.log`, `logs/ranges_roots.time` | 36 certificates. 34 of 34 root pairs equal `theory-decomposition/logs/compare_pair_tol.log`. At `theta = 1/64` the roots equal [D]'s at both tolerances. Pair counts equal the exact and lost counts of `check_pairs_exact.log`. Non-dyadic: 31 same, 3 higher, 0 lower. |
| `python3 compare_pair_tol.py` (from `theory-decomposition/`, about 4 min) | `logs/compare_pair_tol_rerun.log` | identical to `theory-decomposition/logs/compare_pair_tol.log` apart from timings (`diff`) |
| inline Python: `shells()` sizes at `theta = 1/32` and `1/64` | none | `theta = 1/64`: bag 0 has 686,738 leaves, bag 1 has 685,854, `S_1` has 1,793 cells; 9.851 GB `float64`, 1.231 GB Boolean |
| Reading: [D] header, status table, Section 5 opening, Sections 7 and 8.2–8.4; `dp_certificate.certificate()`; `all_roots.chunked()`; the first confirmation's report, `run_all.sh`, `run_tol.py` and logs; the second confirmation's report and `all_roots.log`; `theta64_chunked.log` and `.time`; `stat` of all files changed since the second confirmation; `grep` of [D] for the changed counts and memory figures | none | Section 2 |
