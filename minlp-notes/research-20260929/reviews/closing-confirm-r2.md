# Confirmation of the round-2 closing revision

Date: 2026-09-30. Referee: independent. I did not write the notes, the
closing audit or the revision. Scripts and logs:
[`closing-confirm-r2-checks/`](closing-confirm-r2-checks/).

**Scope.** Six closing-audit findings (F1–F6), the reviser's report of what it
applied, and its three refusals. I checked each finding from scratch against
the current notes and the reviews they cite. Targeted checks only: no
project-wide verification, no CI inspection, no commit. I edited no note; I
wrote only this file and the checks folder.

## Verdict

**Fixes needed (one item, minor).** F2–F6 are applied correctly, and so are the
camshape, powerflow0039r, ex6_2_7, etamac and ann_cumene_tanh parts of F1.
Nothing was strengthened. The refusals are justified.

F1 is not finished. The summary still claims on lines 10–11 that "each
displayed value is itself a valid bound", and two rows still break that
claim: ex6_2_5 and lukvle10. The reviser listed both as "valid as displayed".
It compared the summary against the verifiers' printed strings. Those strings
are rounded to nearest, not outward, so they can lie above the certified
interval end.

## Remaining problem

**R1. `open-instances-summary.md`, lines 26 and 30: two displayed duals lie
above their certified bounds, so the claim on lines 10–11 is still false for
these rows.**

| row | displayed | certified lower end | excess | source of the displayed string |
|---|---|---|---|---|
| ex6_2_5 (line 30) | −70.75207783344770758 | −70.7520778334477075803539469 | 3.5e-19 | `wave2-small-verification/gibbs_bound.py` l. 64: `mpmath.nstr(lb.a, 20)` (round to nearest) |
| lukvle10 (line 26) | 352.2380254050785 | 352.23802540507845563 | 4.4e-14 | `open-instances-verification/v_lukvle10_bnb.py` l. 312: `mpmath.nstr(lo(bound), 16)` (round to nearest) |

- ex6_2_5: I reran the verifier's `gibbs_bound.py` unchanged, from a
  temporary directory, with only its 20-digit print widened to 40 digits.
  The lower end is exactly λ·b − 2.0e-15. The same run gives ex6_2_7's end
  as −0.16084761546364904344…, so the new ex6_2_7 display
  (−0.16084761546364905) is valid.
- lukvle10: I recomputed `lo(bound)` from the verifier's stored per-group
  lower ends, with the same 1e-18 safety subtraction and the stored
  `sum_lam`. Computations at 64 and 200 bits agree to 1e-19. No other
  certificate supports a higher value: the authors' own bound is
  352.238025369202.
- **Fix:**
  - line 30, ex6_2_5: `−70.75207783344770758` → `−70.75207783344770759`;
  - line 26, lukvle10: `352.2380254050785` → `352.2380254050784`.
  - The gap cells (2.0e-15 and 1.4e-9) stay as they are.
  - Alternatively, weaken lines 10–11. Changing the two numbers is simpler.
- No root document repeats either value. The same strings appear in two
  wave reports (`open-instances-wave2/small/report.md` l. 553,
  `open-instances/open-instances-report.md` l. 622 and 786). There they are
  quotations of a verifier and carry no outward-rounding claim, so they
  need no change.

## Finding-by-finding check

**F1 (outward rounding in `open-instances-summary.md`).** I checked every
dual in the file against its certified source.

- Applied correctly:
  - camshape100–800 are now the exact optima rounded down, each 5.9e-15 to
    7.7e-15 below the value in `open-instances-verification`. They are
    labelled "(exact optimum, rounded down)", with primal "exact optimum,
    attained" and gap 0. The verification report supports all three.
  - powerflow0039r 41869.05148327243 is at most 41869051483272433/10¹².
  - ex6_2_7 −0.16084761546364905 is at most −0.16084761546364904344.
  - etamac −15.294675643368093 is at most −15.2946756433680921685.
  - ann_cumene_tanh −4024.495 is at most −4024.4949777104284.
- Valid as displayed:
  - lnts50–400: truncated, 2.4e-14 or more below the verifier's value.
  - dtoc5.
  - optcdeg2: the truncation of 293.87607509587509237940…
  - hvycrash: exact.
  - pricing050 (max, upper bound): the display is at or above `UB.b`. The
    string `−1813.8290784519730577` is the nearest-rounded `UB.b`, but the
    rounding window of the exact primal together with the recorded gap
    1.041e-17 forces `UB.b ≤ −1813.82907845197305770`.
  - chain50–400 and catmix100–800 (range endpoints).
  - powerflow0030p: 576.8934122988004 is at most 576.89341229880046985.
  - powerflow0039p: equal to the exact rational 41869051484850140/10¹².
  - pindyck: below both certified values.
  - waterno2_06–24: exact sums rounded down.
  - The KAN example value.
- Remaining: ex6_2_5 and lukvle10 (R1).

**F2 (`theory-bangbang/extension-n2.md`, Section 9 table).**
- Lines 1078, 1079 and 1083 now cite `reviews/ext-bangbang-n2-confirm.md`.
  That review's Verdict says it rechecked Lemma 14, Proposition 15 and the
  revised Proposition 12 line by line. Its item 4 names the two
  imprecisions and asks for the status update.
- Section 11.1 item 4 and the proof text (l. 952–955) carry the fix.
- Proposition 15 keeps its float caveat.
- Section 11.1 item 12 records the change.

**F3 (unescaped pipes).** I checked cell counts with a GitHub-style parser
(`gfm_cells.py`: split on unescaped `|`, including inside code spans; it
catches known defects).
- README.md:13, coupling.md:124 and decomposition-certificates.md:168 now
  have the header's cell count.
- So do all other tables in the edited notes and in every root document.
- Every added `\|` lies on a table row, except in the three dated entries
  that describe the escape. Outside a table, `\|` would render literally.
- The entries in coupling Section 11.1 item 8, decomposition Section 8.5,
  extension-n2 Section 11.1 item 13 and the consistency root edit name the
  right sections.

**F4 (`theory-calibration/scouting.md`, Section 7).** Line 1573 now reads
"obtained by a formal leading-order derivation", as
`recheck-calibration-confirm.md` point 3 asked. No root document restates
the claim. Section 11.1 item 6 records the change.

**F5 (`root-research-log.md`, closing entry).** Line 326 now reads "M1–M7
(M4 in the note only; the `jn_lifted_cert.py` docstring still says (c))".
This is accurate: the docstring still says "Theorem 5.1(c)", and coupling
Section 11.1 item 3 says the same.

**F6 (consistency header).** The header cites `consistency-confirm-r1.md`
with the suggested wording. That review found no mathematical error and two
optional points, and both are applied in the root edit at the end of
Section 12.

**Strengthening.**
- The only new wording in the summary is "exact optimum, attained". The
  verification report supports it: the envelope point is exactly feasible.
- The F2 status changes cite a review that did the checks.
- Every other edit is a correction, a citation or a rendering fix.

**Refusals.**
1. *Pipes in `theory-decomposition/extension-adaptive.md` and
   `rlct/rlct-node-complexity.md`.* Justified. No finding covers them, and
   the audit limited F3 to rows edited in this revision. The defects are
   real: `gfm_cells.py` finds six broken rows in extension-adaptive.md
   (164, 165, 167, 169, 170, 1400). In rlct-node-complexity.md, the table
   at line 835 does not render, and rows 838 and 1206 break. Optional
   follow-up.
2. *`jn_lifted_cert.py` docstring not changed.* Justified. F5 asked only
   for the log wording, and the log now states the discrepancy.
3. *No round-2 entry in `root-research-log.md`.* Justified; no finding asked
   for one. Optional: the summary's changed values (F1) are recorded in no
   dated entry. A single sentence in the closing entry would record them,
   next to "These root edits have not been rechecked".

## Optional, not required

- `open-instances-summary.md` line 27: "293.87607509587509 (exact value of
  the certificate)" shows a truncation. Lines 10–11 cover this, but
  "(certificate value, truncated)" would match SYNTHESIS.md and the
  bang-bang report.
- `theory-bangbang/extension-n2.md` line 1285 (Section 11, item 8) still
  says "This revised proof has not been checked independently". It is a
  historical revision entry, and Section 11.1 records the later check, so
  it is not wrong.

## Commands run (targeted checks only)

Run from `research-20260929/`:

```
python3 reviews/closing-confirm-r2-checks/ex6_2_5_lower_end.py   # logs/ex6_2_5_lower_end.log
python3 reviews/closing-confirm-r2-checks/lukvle10_lower_end.py  # logs/lukvle10_lower_end.log
python3 reviews/closing-confirm-r2-checks/gfm_cells.py <notes>   # logs/gfm_cells.log
```

Everything else was reading files and using grep. `ex6_2_5_lower_end.py`
runs the verifier's script in a temporary directory; no file under
`reviews/wave2-small-verification/` or `reviews/open-instances-verification/`
changed. No project-wide verification was run and CI was not inspected.
