# Confirmation review (round 1) of `open-instances-wave3/eg/retry.md`

Date: 2026-10-01. Referee: fresh and independent. I did not write the retry,
its code or the first review. Scope: the revision that applied the minor
items of [`eg-retry-review.md`](eg-retry-review.md), Section 1 (retry
Section 10). I checked each item from scratch, recomputed every number that
changed, judged the one partial refusal, and checked that nothing was
strengthened and no new error was introduced. My scripts and logs are in
[`eg-retry-confirm-r1-checks/`](eg-retry-confirm-r1-checks/). Only targeted
checks were run, single-threaded (`OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=1`)
and under `timeout`. No project-wide verification was run and no CI results
were consulted.

Labels used below.

- **Exact**: rational arithmetic (`fractions.Fraction`), or an exact
  floating-point error term (Knuth's TwoSum).
- **Own code**: written for this review. It does not import the retry's
  decoder (`egdata`/`eg_model`). Where noted, it uses the first review's
  independent GAMS reader.
- **Rerun**: the retry's code run again, with its output compared with the
  original log.
- **By hand**: I redid the argument myself.

## Verdict

**Verified.** All six items are applied correctly. Every changed number
agrees with my recomputation. The refusal on the `fexp` premise is justified:
x − mL1 is always exact. No bound, primal value or closure claim changed, and
nothing was strengthened. Two optional nits remain (Section 3). Neither
affects a result.

## 1. The items

### 1.1 CPU time of eg_int_s (review item 1)

`logs/int9_final.log` ends with `time 274s`; `logs/int_1e-9.log` (run A)
ends with `time 401s`. Section 5 now says "4.6 min (274 s, run C)", and
274/60 = 4.57. Correct.

### 1.2 Justification of the exp cap (review item 2)

- **Own code, exact** (`ell_bound_indep.py`, `logs/ell_bound_indep.log`). The
  term data come from the GAMS files through the first review's reader
  `gms_model.py`, not through `egdata`. For a box with centre in the root box
  and radii r_i ≤ (ub_i − lb_i)/2, ℓ = Σ_i 2|γ_i| s_i |t_i| r_i ≤
  Σ_i |γ_i| s_i (ub_i − lb_i) max(|μ_i + s_i lb_i|, |μ_i + s_i ub_i|). Over
  all 2,716 terms of each instance, the maximum is 16.963974 (row e7,
  term 74), with max |t| = 3.0, for all three instances.
- **Rerun.** `check_ell_bound.py` reproduced `logs/check_ell_bound.log`
  exactly (16.9640, e7, term 74).
- **Code.** `egtm.Model.taylor` forms ℓ as `usum(up(|V|·r))`, with r the
  outward-rounded half-width of the current box, and passes only ℓ to
  `iexp_up`. Every box lies in the root box, so ℓ ≤ 16.97 up to rounding.
  The cap at 700 could not have been reached.
- **`egtm.FastModel`** still has `np.minimum(ell, 700.0)` (line 320). `grep`
  finds no use of the class in `open-instances-wave3/eg/` or in the first
  review's checks. Leaving it unchanged and only noting it is acceptable.
- **The rerun of run B** with the uncapped `iexp_up` and `EG_ORDER=2` gives a
  log equal to the original apart from timings (Section 1.3).

The new text in Section 6 and Section 10 item 2 is correct.

### 1.3 The `S.lo > 0` guard in `egbb.BB.dual_value` (review item 3)

**Code, by hand.** The new code is:

```python
if vl >= 0:
    q = vl / float(S.hi)
elif float(S.lo) > 0:
    q = vl / float(S.lo)
else:      # sum y not proved > 0: no bound from this dual vector
    return -INF
```

- **vl < 0 with S.lo > 0** gives vl/S.lo ≤ val/S for every S in [S.lo, S.hi].
  This is valid.
- **The branch vl ≥ 0 is unchanged** and is valid because Σ y_k > 0 holds
  exactly. `LP.solve` returns y = max(−row_dual, 0) ≥ 0, and `dual_value`
  returns −∞ unless the float sum of y is positive. A positive float sum of
  nonnegative numbers implies a positive exact sum.
- **Old behaviour.** `egtm.isum` subtracts an absolute 1e-300, so S.lo ≤ 0
  needs Σ y ≲ 1e-300. Then the old code returned vl/S.lo > 0 (unjustified),
  or raised `ZeroDivisionError` when S.lo = 0 (Python floats).
- **Dual feasibility.** The LP has a free variable t with cost 1 and
  coefficient −1 in each objective row, so Σ_obj y_k = 1 up to HiGHS's
  tolerances.

The description in Section 10 item 3 is correct.

**The reruns.**

- **The wrapper.** `check_guard.py` counts calls with S.lo ≤ 0 (a superset of
  the calls where the guard acts), then calls the real `dual_value`.
- **The settings.** `run_guard.sh` uses the stated settings: `EG_ORDER=2` for
  A, B and D; `EGMODEL=ni` for B, H and I; no checkpoint file; time limits
  3,600–9,000 s, never below the original limits.
- **My own diff.** I compared each of the 18 rerun logs with its original
  after removing only the timing fields (`sed`; independent of
  `compare.py`). All 18 are equal, including the final lines with the
  certified value, the incumbent and the point.
- **The totals, recomputed by hand from `compare.log`.**
  - dual_value calls: run D 93,844 + 73,367 = 167,211; run E 59,630; run G
    583,148; run I 59,628; 993,781 in total.
  - CPU time: 39,373 s in total (10.9 h), with pieces from 803 to 3,823 s.
  - Smallest float sum: 0.9999999999999998. Smallest S.lo:
    0.9999999999999938.
  - Calls with S.lo ≤ 0: none.

  These agree with the table in Section 10.
- **My own reruns.** I ran the current, guarded `egbb.py` without the
  wrapper for run C (`egbb.py eg_int_s 1e-9 3600`) and run E part 1
  (`egbb.py eg_disc_s 1e-9 3600 - - 1 2`). Both logs equal the originals
  apart from timings (`logs/rerun_C.log`, `logs/rerun_E_p1.log`).
- **Why my reruns add something.** `egfast.py` was last modified at 11:59,
  one minute after `run_guard.sh` (11:58). The guard reruns may therefore
  have imported `egfast.py` from before its docstring edit. My reruns used
  the current file, so the edit changed no behaviour on these two runs.

Not rerun with the guard: run F, the ablations and `test_bound.py`. This is
acceptable. Run F is superseded, and no reported bound depends on these
runs. The guard can only replace an unjustified value by −∞.

### 1.4 Table 17 of Göß, Burlacu and Martin (review item 4)

I checked `fulltext.md` and `pdftotext` of PDF pages 37–39 of the local copy.
Table 17 starts on printed page 988 (PDF page 38).

- **Headers.** They read "primal value | dual value".
- **Values.** SCIP on the original models: eg_int_s 9085.1 s, 6.5 | 6.5;
  eg_disc_s limit, 3.6 | 5.8; eg_disc2_s limit, −1.1 | 6.3. Only the
  reverse reading fits a minimization with optimum 5.76 or 5.64. Many rows
  show "inf" in the second column, which fits a missing primal solution.
- **Asterisk.** The asterisk is on the SCIP entry of eg_disc_s. Appendix B.5
  says that eg_disc_s was excluded for SCIP and ex8_4_6 for Gurobi, because
  they "caused numerical and/or memory errors".
- **Gurobi.** On the original models, all three runs show `limit`.
  Gurobi's "both" run of eg_int_s shows 989.0 s with "inf | inf".
- **Setup.** 8 threads and 4 h (14,400 s) are stated in Section 4; SCIP 8.1
  and Gurobi 11.0.x elsewhere in the paper.

Section 7 and Section 10 item 4 state all of this correctly. The new Gurobi
bullet ("reaches the time limit on the original model of all three") is
accurate and weaker than the old wording.

### 1.5 Tightness ratios (review item 5, first bullet)

- **Rerun.** `cmp_bounds.py` reproduced `logs/cmp_bounds.log` exactly
  (`diff`; `logs/rerun_cmp_bounds.log`).
- **The ratios.** Recomputed from the log: 7.688/2.437 = 3.2,
  1.174/0.06133 = 19.1, 0.1150/0.007465 = 15.4, 0.01301/0.001840 = 7.1 and
  0.001627/0.0005542 = 2.9. These match Sections 3.1 and 6.
- **The wording.** "15–19 times at ρ = 0.1 and 0.03, about 3–7 times at the
  other sizes" is correct. The hedged remark is sound in direction: a shared
  overstatement of the minimum, added to both gaps, pulls their ratio toward
  1. The remark also says that the amount was not measured.

### 1.6 The `fexp` docstring, and the partial refusal (review item 5, second bullet)

The reviser rejected the review's premise that x − mL1 can be inexact at the
reduction boundary. I agree.

- **By hand.**
  - m = rint(fl(x·64/ln2)) differs from the exact quotient by at most
    ½ + ~2u(|m| + ½).
  - For m ≥ 2, the margin in Sterbenz's condition mL1/2 ≤ x ≤ 2mL1 is at
    least half a reduction step.
  - The only tight case is m = ±1 at x ≈ ±½·ln2/64. There the condition
    needs L1 < ln2/64. Since L1 is a truncation, it is below ln2/64 by a
    relative 2.75e-10, and the rounding error of the computed m is about
    2e-16.
  - mL1 is exact for |m| < 2^20, so Sterbenz's lemma applies and
    fl(x − mL1) = x − mL1.
- **Exact, own code** (`fexp_sterbenz_all.py`,
  `logs/fexp_sterbenz_all.log`).
  - Arguments: 4,595,045 floats. They are the floats within ±8 ulps of every
    reduction boundary (m ± ½)ln2/64 in [−700, 700], for all |m| ≤ 64,641,
    plus 200,001 points in [−0.01, 0.01].
  - Results: the TwoSum error term of x − mL1 was 0 in every case, and the
    Sterbenz condition held in every case.
  - The tightest case is m = ±1, at a relative margin of 2.753e-10, as the
    retry says.
  - L1 < ln2/64 (relative gap 2.7530e-10), and mL1 is exact for
    |m| ≤ 64,641.
- **Rerun.** `check_fexp_r.py` reproduced `logs/check_fexp_r.log` exactly
  (152,472 arguments, 0 inexact, max |r̃ − r| = 4.337e-19).
- **The bounds in the docstring.**
  - The rounding of the last subtraction is at most u·0.0055 = 6.1e-19 <
    6.2e-19.
  - fl(mL2) and the split add at most about 2.2e-23 + 6.5e-23 < 1e-22.
  - Without the exactness of x − mL1, a further u·(0.0055 + 1.9e-7) =
    6.1e-19 is added, which gives about 1.23e-18 ≤ 1.3e-18.
  - Both bounds are far inside the factors 1 ± 4e-15.
- **Comment only.** The edit to `egfast.py` is a comment. My reruns of C and
  E part 1 and of `cmp_bounds.py` with the current file reproduce the
  original logs.

### 1.7 Other edits

- **Status line.** It reports the review's verdict and its sampling caveat
  for the seven eg_disc2_s parts without the optimum. It matches the review.
- **Section 4.** The note on the review's interval replay of eg_disc2_s
  part 1 (134,607 boxes, same certified value) matches review Section 6.
- **Sections 8 and 9.** They list the new commands and files, which exist.

## 2. Nothing strengthened, no new error

- All results tables (Sections 1 and 5) and all certified values are
  unchanged.
- The novelty statements are unchanged and remain qualified.
- The changes to Sections 3.1, 6 and 7 weaken or make precise earlier
  wording.
- The only code change is the guard. It can only turn a value into −∞.

## 3. Optional nits (do not affect any result)

- **N1 (new wording, Section 3.4 step 3).** "If that enclosure is not proved
  positive, the LP gives no bound" is broader than the code. The code
  refuses only when the combined value vl is negative and S.lo ≤ 0. When
  vl ≥ 0, it divides by S.hi whatever S.lo is. That branch is valid, because
  y ≥ 0 and the float-sum test imply Σ y_k > 0 (Section 1.3). Suggested
  wording: "If the combined value is negative and that enclosure is not
  proved positive, the LP gives no bound (…)". Section 10 item 3 already
  describes the code exactly.
- **N2 (wording that predates the revision).** Section 4 says that an
  interval replay of eg_disc2_s would cost "6–10 times" as much. Section 3.2
  says that the interval model "was 4–8 times slower in these runs". The
  measured ratios are 5.7 (B/A), 7.7 (H/C) and 3.7 (I/E), and 3.8 for the
  review's replay of eg_disc2_s part 1 (5,755/1,515 s). The figure in Section 4
  could be aligned with these. Timings are indicative only (shared machine),
  and nothing depends on this figure.

## 4. Commands run

All with `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=1` and `timeout`.

- From `reviews/eg-retry-confirm-r1-checks/`:
  - `python3 ell_bound_indep.py` (`logs/ell_bound_indep.log`): 16.963974 for
    all three instances.
  - `python3 fexp_sterbenz_all.py` (`logs/fexp_sterbenz_all.log`): 0 inexact,
    0 Sterbenz failures in 4,595,045 arguments.
- From `open-instances-wave3/eg/retry/`:
  - `python3 check_ell_bound.py` and `python3 check_fexp_r.py`: output
    identical to `logs/check_ell_bound.log` and `logs/check_fexp_r.log`.
  - `python3 cmp_bounds.py`: identical to `logs/cmp_bounds.log`.
  - `python3 egbb.py eg_int_s 1e-9 3600` and
    `python3 egbb.py eg_disc_s 1e-9 3600 - - 1 2` (current, guarded code):
    equal to `logs/int9_final.log` and `logs/disc9_p1.log` apart from timings.
  - A `sed`-normalised comparison of all 18 `logs/guard/*_guard.log` with the
    original logs: all equal.
  - `grep -rn FastModel`: no user of the class.
- In `literature/papers/go2026-parabolic-approximation-relaxation-for-minlp/`:
  `grep` of `fulltext.md` and `pdftotext -f 37 -l 39 -layout original.pdf`.

Compute: about 10 CPU-minutes in total (the two B&B reruns took 213 s and
245 s of search time).
