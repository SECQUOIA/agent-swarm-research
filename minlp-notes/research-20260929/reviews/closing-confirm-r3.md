# Confirmation of the round-3 closing revision

Date: 2026-09-30. Referee: independent. I did not write the notes, the
closing audit, the r2 confirmation or the revision. Scripts and logs:
[`closing-confirm-r3-checks/`](closing-confirm-r3-checks/).

**Scope.** One finding (R1 of
[`closing-confirm-r2.md`](closing-confirm-r2.md)): two displayed duals in
`open-instances-summary.md` lay above their certified bounds, so the claim on
lines 10–11 ("each displayed value is itself a valid bound") failed for them.
I also checked the reviser's three reported edits and its two refusals.
Targeted checks only: no project-wide verification, no CI inspection, no
commit. I edited no note. I wrote only this file and the checks folder.

## Verdict

**Verified. No remaining problems.** Both displays are now valid bounds. The
gap cells are still correct. The added sentence in
`closing-research-results.md` is accurate. Nothing was strengthened, and both
refusals are justified.

## The finding, checked from scratch

I did not reuse the r2 scripts. For each instance, my scripts:

- evaluate the verifier's certified expression exactly in rationals;
- replay the verifier's own interval arithmetic, in the same order of
  operations, to get the exact binary value of its lower end;
- assert that the replayed lower end, printed as the verifier prints it,
  reproduces the verifier's stored string.

| row | new display | certified value (exact) | verifier's lower end | display minus lower end |
|---|---|---|---|---|
| lukvle10 (line 26) | 352.2380254050784 | 352.238025405078455701737… | 352.238025405078455654095… (64-bit `lo(bound)`) | −5.57e-14 |
| ex6_2_5 (line 30) | −70.75207783344770759 | −70.7520778334477075803539469 (= λ·b − 2.0e-15) | same to about 1e-48 (50-digit `lb.a`) | −9.6e-18 |

- **lukvle10** (`lukvle10_display.py`). The certified expression comes from
  `open-instances-verification/v_lukvle10_bnb.py`, lines 298–306:
  Σ count·(LB − 1e-18) + (LB_tail − 1e-18) + Σλ. I summed Σλ exactly from the
  stored multipliers, with λ[30:961] set to λ[495] as the verifier does. I did
  not use the rounded `sum_lam` string. The replay reproduces the verifier's
  `sum_lam` and `dual_bound` strings. The old display, 352.2380254050785, was
  4.43e-14 above the lower end. The new display is 5.57e-14 below the exact
  value, so it is valid.
- **ex6_2_5** (`ex6_2_5_display.py`). The certified expression comes from
  `wave2-small-verification/gibbs_bound.py`:
  λ·b + Σ_p [min(0, tmax·m_p) − max R_p/e].
  - All max R_p are 0, and the ideal-phase minimum m₂ has a positive lower
    end, so its term is 0.
  - With tmax = 100 and τ = 1e-17, the certified value is exactly
    λ·b − 2.0e-15.
  - The replay reproduces the verifier's printed −70.75207783344770758. That
    string is the nearest rounding of the lower end, 3.54e-19 above it. The
    new display is 9.6e-18 below it, so it is valid.
- **Gap cells.**
  - lukvle10: p5 − new display = 1.418e-9, shown as 1.4e-9.
  - ex6_2_5: the verifier's exact primal −70.75207783344770558 minus the new
    display = 2.01e-15, shown as 2.0e-15.
  - Both cells were correct before the revision and are still correct. The
    ex6_2_5 gap is measured against the exact primal, not the 17-digit primal
    cell. The r2 confirmation already noted this.
- **No other certificate is involved.** The r2 confirmation notes that the
  authors' lukvle10 bound (352.238025369202) is lower. So the verifier's value
  is the right reference.

## Reviser's reported edits

1. **Line 26, lukvle10: 352.2380254050785 → 352.2380254050784.** This is
   correct. The report says the lower end is 352.23802540507845563 "at both 64
   and 200 bits". That is slightly imprecise. The r2 log gives
   …845562634 at 64 bits and …845569990 at 200 bits, both computed from the
   rounded `sum_lam` string. The r2 report's "agree to 1e-19" is also too
   strong: the two values differ by about 7e-17. These imprecisions appear
   only in the review record and the reviser's report, not in any note. They
   are about 1000 times smaller than the 5.6e-14 margin, so they do not affect
   the fix.
2. **Line 30, ex6_2_5: −70.75207783344770758 → −70.75207783344770759.** This
   is correct, as the table above shows.
3. **`closing-research-results.md`, lines 207–210.** The sentence says the
   two displays were checked against their certified interval ends, which the
   two scripts in `reviews/closing-confirm-r2-checks/` recompute. This is
   accurate. Those scripts compute exactly those ends, and their logs show
   them.

**Strengthening.** Only these two files changed after the r2 report (checked
by modification time across the repository). In the summary, only the two
numbers changed, and both moved in the safe direction, making the bounds
weaker. The added sentence reports a check and makes no new claim.

## Refusals

1. *Gap cells unchanged.* Justified: the finding asked for this, and both
   cells are still correct (see above).
2. *No edits to notes or wave reports.* Justified. I repeated the grep over
   every `.md` file in the repository. No root document repeats either value.
   The old strings still appear in:
   - `open-instances-wave2/small/report.md` l. 553;
   - `open-instances/open-instances-report.md` l. 622 and 786;
   - `reviews/open-instances-verification/verification-report.md` l. 27 and
     358;
   - `reviews/wave2-small-verification/verification-report.md` l. 16 and 120.

   The last two are review records, which the reviser did not mention. None
   of these files claims outward rounding. Each quotes a verifier's printout,
   rounded to nearest, of a certified quantity. The differences, 4.4e-14 and
   3.5e-19, are far below the stated gaps of 1.4e-9 and 2.0e-15. No fix is
   needed.

## Optional, carried over from r2 (not required)

The r2 report lists two optional points. Neither changed and neither has
become required: the "(exact value of the certificate)" wording on summary
line 27, and the historical revision entry at
`theory-bangbang/extension-n2.md` l. 1285.

## Commands run (targeted checks only)

Run from `research-20260929/`:

```
python3 reviews/closing-confirm-r3-checks/lukvle10_display.py   # logs/lukvle10_display.log
python3 reviews/closing-confirm-r3-checks/ex6_2_5_display.py    # logs/ex6_2_5_display.log
```

The first run of `ex6_2_5_display.py` failed an assertion. The cause was a
bug in my own script: `mpf.man_exp` drops the sign, so the negative lower end
was converted with the wrong sign. I fixed both scripts to read the sign from
the `_mpf_` tuple before the logged runs. Everything else was reading files,
`grep`, and `find -newer` against the r2 report. Both scripts only read files
under `reviews/open-instances-verification/` and
`reviews/wave2-small-verification/`. No project-wide verification was run
and CI was not inspected.
