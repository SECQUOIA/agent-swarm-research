# Confirmation of the fourth-round revision of `decomposition-certificates.md` (round 2)

Date: 2026-09-30. Scope: the changes to
[`../theory-decomposition/decomposition-certificates.md`](../theory-decomposition/decomposition-certificates.md)
([D] below) and
[`../theory-decomposition/dp_certificate.py`](../theory-decomposition/dp_certificate.py) made in
response to [`decomposition-nondyadic-confirm-r1.md`](decomposition-nondyadic-confirm-r1.md)
("the confirmation" below). These are [D] Section 8.3, the revised items 3 and 6 of Section 8.2,
the header, the two new rows of Section 7, the new script `compare_pair_tol.py` and its log. I
checked each item from scratch, recomputed every changed number, and judged the one item the
reviser did not apply. Scripts and logs are in
[`decomposition-nondyadic-confirm-r2-checks/`](decomposition-nondyadic-confirm-r2-checks/).

## 1. Verdict

**All four applied changes are correct. My recomputation reproduces every changed number bit for
bit. No claim was strengthened. Leaving `theta = 1/64` out is acceptable, but the reason given
for it contains one factual error.**

- The two wording fixes asked for by the confirmation are made as asked. The related fix to
  Section 8.2, item 3 is correct and follows from how `certificate()` computes the bound.
- An independent driver enumerates the certificates by running the unchanged `E2()`, `E3()` and
  `E4()` of `run_experiments.py`. Its 34 root pairs match `logs/compare_pair_tol.log` exactly, in
  the same order: 3 higher, 29 bit-identical and 0 lower among the 32 with non-dyadic `x*`, and
  the two certificates at `x* = 0` are identical.
- I also computed the two E4 certificates at `theta = 1/64` that the reviser left out. A
  row-chunked copy of `certificate()` needs 1.6 GB peak memory. Their roots with `PAIR_TOL = 0`
  and `1e-12` are bit-identical.

Remaining issue (Section 3): Section 8.3, item 2 says that the confirmation's count of 34
includes the two E4 certificates at `theta = 1/64`. It does not.

## 2. Item-by-item check

| Item | Claim in [D] | Check | Result |
|---|---|---|---|
| 8.3.1 | Section 8.2, item 6 misquoted `adaptive/rc_lib.py`. The docstring says only "(which makes l_r too high)". The file was last changed at 10:16, before the check (11:21). Only Section A.5 of `extension-adaptive.md` says "not a valid bound". The error came from the check's Section 4.3. | `grep`; `stat`; read | Confirmed. `rc_lib.py` lines 9–11 contain "(which makes l_r too high)" and no "valid" wording. `grep` over `extension-adaptive.md` and `adaptive/*.py` finds "not a valid bound" only at `extension-adaptive.md` line 602 (Section A.5). Modification times: `rc_lib.py` 10:16:14; check 11:21:01. The check's Section 4.3 says: "The `rc_lib.py` docstring says the same." Neither `rc_lib.py` nor `extension-adaptive.md` (11:28) has changed since the confirmation (11:42). |
| 8.2.6 (revised) | Quotes Section A.5, says such an `l_r` "can be higher than the bound Lemma 1.5 defines but remains valid as long as no pair with positive-length overlap is lost", limits that condition to [D]'s runs, and says the `rc_lib.py` wording is correct | Read against the remark after Lemma 1.3 | Consistent with the remark, and not stronger than it. "Too high" in `rc_lib.py` is correct about the direction of the error. Like the old `dp_certificate.py` wording, it could be read as "always". It belongs to the extension note's code, and item 6 states the "can be higher" qualification next to it, so I agree that no change is needed. |
| 8.3.2 | Docstring now reads "which can give a bound higher than Lemma 1.5's" | Read; E2 rerun; roots from the original `certificate()` | The wording is changed as stated. The code behaves as before: `python3 run_experiments.py E2` gives output identical to `logs/E2_slopes.log`, and `certificate()` reproduces the logged roots at both tolerances (next row). I could not `diff` the file against its previous version because `research-20260929/` is untracked and no copy exists. |
| 8.3.2 | `compare_pair_tol.py`: of 32 certificates with non-dyadic `x*`, the unwidened root is higher in 3 (E2 at `h = 2^-2`, affine and zero slopes, by `1.38e-5` and `1.56e-2`; E2 at `h = 2^-4`, zero slopes, by `5.18e-4`), bit-identical in 29 and lower in none; E3 at `x* = 0` identical | `all_roots.py` (below) | Same result. Differences `1.3828e-05`, `1.5630e-02`, `5.1763e-04`, as in the confirmation's `full_precision.log`. All 34 root pairs equal those in `logs/compare_pair_tol.log`. The case list of `compare_pair_tol.py` is exactly the set of `certificate()` calls made by `E2()`, `E3()` and `E4()` with `mu <= 5`, in the same order. |
| 8.3.3 / 8.2.3 (revised) | The first-version bounds "are at least the bound of Lemma 1.5; they were higher in the three E2 certificates of item 1 and identical in the 29 other certificates recomputed" | Read `certificate()`; counts above | Correct. "At least" follows from the code, not only from the runs. Dropping a pair removes a term from the minimum that defines `off` or `beta`. A pair's own `min_subbox` value does not depend on which other pairs are present. Floating-point addition and `min` are monotone. So the unwidened root cannot be below the widened one, which agrees with "lower in none". "Three E2 certificates of item 1" matches item 1 (both slopes at `2^-2`; zero slopes at `2^-4`). 3 + 29 = 32. |
| 8.3.4 | Header cites the confirmation and says the fixes of Sections 8.1 and 8.3 have not been rechecked | Read | Accurate. After this report, Section 8.3 has been rechecked, apart from issue 1. |
| Section 7, new rows | `compare_pair_tol.py` (about 4 min), roots for all E2, E3, E4 except `theta = 1/64`, 3 higher / 29 identical / 2 at `x* = 0` identical; E2 rerun after the docstring edit identical | Reruns above; file times | Correct. The script was saved at 11:56:36 and its log at 12:00:34, which agrees with "about 4 min". |
| Status table | No change | Read | Correct: no result changed status. The Lemma 1.3 row already notes the touching-pairs remark. |
| Not applied | The two E4 certificates at `theta = 1/64` were not recomputed at full precision; dense pair arrays need about 20 GB | Judged; computed with a row-chunked copy | **Acceptable.** The note's E4 table stops at `theta = 1/32`, and every count in the note is restricted to the certificates actually recomputed. The stated reason contains a false statement about the confirmation (issue 1). The `theta = 1/64` gap is now closed (Section 2.1). My estimate of the dense peak is about 14 GB rather than 20 GB: 9.9 GB for the `float64` array `np.where(meet, cbeta, inf)` in bag 0, plus about 1.2 GB for each Boolean temporary. Either amount is too much to use casually on a shared machine. |

### 2.1 The certificates at `theta = 1/64`

`all_roots.py` replaces `certificate` inside `run_experiments.py` with a recorder. It then runs
the unchanged `E2()`, `E3()` and `E4()`, so the case list is taken from the experiments
themselves (36 certificates, including `mu = 6`).

For each call, the recorder evaluates a copy of `certificate()` that processes the pair tests
in blocks of 20,000 leaves. The copy uses the same comparisons, the same pair order (row-major
`np.nonzero` blocks concatenated in row order) and the same `min_subbox` calls. It does this at
`PAIR_TOL = 0` and at `1e-12`. For the 34 certificates other than `mu = 6`, it also calls the
original `dp_certificate.certificate()` at both tolerances and asserts bit-identical roots; all
34 passed.

Results for `theta = 1/64` (`n = 3`, seed 0, `h = 2^-14`):

| slopes | root, `PAIR_TOL = 0` | root, `PAIR_TOL = 1e-12` |
|---|---|---|
| affine | `-0.0097876251980369196` | same |
| zero | `-0.0097914614120943721` | same |

These are also bit-identical to the `theta = 1/32` roots. The E4 output printed with the widened
test, including the `theta = 1/64` row (`1.268e-09`, `3.837e-06`, size 1,374,385), is identical
to `logs/E4_theta.log`. So the earlier Section 7 statement that all six E4 rows are unchanged
holds, and at `theta = 1/64` it holds at full precision, not only to four significant digits.

Over all 36 certificates of E2, E3 and E4, the unwidened root is higher in 3 and bit-identical
in 33. This includes 31 of the 34 with non-dyadic `x*`. None is lower.

## 3. Remaining issue

1. **Section 8.3, item 2 misstates the confirmation's count.** It says: "The two E4
   certificates at `theta = 1/64`, which the confirmation's count of 34 includes, were not
   recomputed". The confirmation's 34 certificates were the 16 E2 certificates (run at both
   tolerances), the 8 E3 certificates (including the two at `x* = 0`) and the 10 E4 certificates
   at `theta = 1/2 … 1/32`. Its `run_all.sh` runs "E4 (theta = 1/2 .. 1/32)", and it lists "The
   E4 root at `theta = 1/64`" under "Not rechecked here". Its "3 of 34 higher, 31 identical" is
   therefore the same set as [D]'s "3 higher, 29 identical" plus the two certificates at
   `x* = 0`. As written, the sentence tells the reader that [D] checked fewer certificates than
   the confirmation, but both checked the same 34. No number or conclusion is affected.
   **Fix:** delete the clause "which the confirmation's count of 34 includes,". Optionally, say
   that the confirmation's 34 are these 32 plus the two E3 certificates at `x* = 0`. If the
   reviser wants to close the `theta = 1/64` gap, Section 2.1 of this report gives
   bit-identical roots for both slopes. With them, the counts are 3 higher and 31 identical of
   the 34 certificates with non-dyadic `x*`.

No other problem found.

## 4. Commands run

All commands were targeted and run with `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
MKL_NUM_THREADS=1` and `timeout`. The `theory-decomposition` files were imported unchanged. No
project-wide verification was run, and no CI results were consulted.

| Command | Log | Result |
|---|---|---|
| `python3 run_experiments.py E2` (from `theory-decomposition/`, 18 s) | `decomposition-nondyadic-confirm-r2-checks/logs/E2_direct.log` | identical to `theory-decomposition/logs/E2_slopes.log` (`diff`) |
| `python3 all_roots.py` (from `decomposition-nondyadic-confirm-r2-checks/`, 22 min, peak memory 1.6 GB) | `logs/all_roots.log`, `logs/all_roots.time`, `logs/E2_widened.log`, `logs/E3_widened.log`, `logs/E4_widened.log` | 36 certificates. The original `certificate()` and the chunked copy give bit-identical roots at both tolerances in all 34 certificates with `mu <= 5`. Unwidened root: 3 higher, 33 identical, 0 lower. The 34 roots without `theta = 1/64` equal `theory-decomposition/logs/compare_pair_tol.log` exactly. E2 and E3 output is identical to the note's logs. E4 output, including `theta = 1/64`, is identical to `logs/E4_theta.log` apart from two trailing lines (a blank line and "[exited with code 0]") that are in the note's log file and predate this revision. |
| inline Python: exact comparison of the root columns of `all_roots.log` and `compare_pair_tol.log` | none | 34 of 34 pairs equal, same order |
| inline Python: sizes of the `theta = 1/32` and `1/64` shell partitions | none | `theta = 1/64`: 686,738 bag-0 leaves × 1,793 cells, so 9.9 GB for the dense `float64` array |
| `grep` of `rc_lib.py`, `extension-adaptive.md`, `adaptive/*.py` and the check; `stat` of the files involved; reading of [D]'s header, status table, remark after Lemma 1.3, Sections 5, 5.3, 7 and 8.2–8.3 | none | Section 2 |
