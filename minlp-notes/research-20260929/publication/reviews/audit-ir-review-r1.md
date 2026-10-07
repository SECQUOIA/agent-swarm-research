# Review of track audit-ir (round 1): independent check of the audit's class (i-r) results

Date: 2026-10-01. Reviewer code, outputs and live copies:
`research-20260929/publication/reviews/audit-ir-r1/`. Nothing was committed and
no one was contacted. At most 1 core was used.

## Verdict

**Verified, with minor issues.** Every numerical claim I checked in the
author's report text reproduces with my own code: the 12 (i-r) pairs, their
margins, the four stated enclosures, the spring global optimum, the page
parse, the screen, and the digit statistics. I found no blocker and no major
issue. The minor issues are listed in Section 6. Two of them concern the
report itself:
- `report.md` was never written. The harness blocked it.
- The report text I received was cut off after the first lines of Section 2.
  I could therefore not check its list of commands.

## 1. Independence and model

- My own code:
  - an OSiL reader with exact `Fraction` evaluation (`rv_osil.py`);
  - an HTML parser built on `html.parser` (`step4_pages.py`).
- It does not import or copy the audit's code (`audit*.py`, `verify*.py`,
  `cert_*.py`, `osilx.py`) or the author's code (`osilq.py`, `check_ir.py`,
  `parse_check.py`). I read the author's scripts only to find inputs and to
  look for gaps. A grep confirms that the author's scripts import nothing
  from the audit.
- The four cached OSIL models are byte-identical to the live MINLPLib files
  (re-fetched 2026-10-01, `step8b_osil_live.py`).
- The five stored points (`bound-audit/sol/`) are byte-identical to the live
  `.sol` files (`step8_live.py`).
- Floating-point cross-check of my OSIL reading with SCIP's own OSiL reader
  (`step9_scip_xcheck.py`, pyscipopt 6.2.1, feastol 1e-9; evidence, not
  proof):
  - SCIP accepts all five of my exactly feasible points. nlobjvar is set to
    my exact nonlinear objective part plus 1e-12 relative.
  - SCIP rejects each point when nlobjvar is 1e-7 relative below.
  - SCIP rejects perturbed points.
  - SCIP's objective agrees with my exact objective to 1e-12 relative.

## 2. The 12 (i-r) pairs

The 17 (i-r) rows of `results.json` form 12 distinct (instance, solver)
pairs on 4 instances. All 12 dual bounds are dated 17 Sep 2013. All four
instances are minimization problems.

| instance | pairs | listed d | how I built the exactly feasible point | exact objective f (mine) | d − f | (d − f)/\|d\| | /audit slack | /display unit |
|---|---|---|---|---|---|---|---|---|
| eniplac | COUENNE, LINDO, SCIP | −132117. | listed point; recomputed 81 variables from their defining equalities | −132117.08301998871378103160657992… | 0.08301998871 | 6.284e-7 | 0.166 (slack 0.5) | 1660 (5e-5) |
| lop97icx | ANTIGONE | 4099.06 | listed point as it is | 4099059953600000099/10^15 = 4099.059953600000099 | 4.6399999901e-5 | 1.13e-8 | 0.0093 (0.005) | 92.8 (5e-7) |
| spring | ANTIGONE, BARON, COUENNE, LINDO, SCIP | 0.84624567 | i4 = 9, b11 = 1 (the assignment of p2 and p3); x5 = 40-decimal rational with x3 − lb = 1.2e-43 | 0.846245665643154281251664635037141295275348… | 4.35685e-9 | 5.15e-9 | 0.871 (5e-9) | 0.871 (5e-9) |
| stockcycle | ANTIGONE, BARON, COUENNE | 119949. | listed point as it is | 71969213/600 = 119948.688333… | 187/600 = 0.311667 | 2.60e-6 | 0.623 (0.5) | 6233 (5e-5) |

The listed points of lop97icx and stockcycle are exactly feasible as they
are: there are 0 violations in exact arithmetic, integrality included.

The listed points of eniplac and spring are not exactly feasible:
- eniplac p2: 31 violations, the largest 2.47e-10 (row e1).
- spring p2: 4 violations, the largest 4.9e-7 (e3).
- spring p3: 4 violations, the largest 9.9e-9 (e5).

The constructed points pass `rv_osil.check` with 0 violations. That check
covers every row, bound and integrality condition of the OSIL model.

**Stated enclosures.** All four contain the objective of an exactly feasible
point that I built:
- lop97icx [4099.059953600, 4099.059953601]: the listed point.
- stockcycle [119948.6883333, 119948.6883334]: the listed point.
- spring [0.8462456656363, 0.8462456656500]: my rational point.
- eniplac [−132117.0830149, −132117.0830141]: a point built from the audit's
  proof-box centre (`logs/verify/eniplac.p2.center.sol`).
  - In each period I moved one interior flow so that the demand equalities
    e27–e32 hold exactly. I chose different flows from the author: x4, x8,
    x12, x16, x20 and x21, against the author's x3, x7, x11, x16, x19 and
    x21. The largest move was 3.9e-14.
  - The point's objective is −132117.0830145020334205…, which is inside the
    enclosure.
  - The author's centre-based point has objective −132117.0830145020336607…,
    also inside.

**eniplac from the listed point.** My construction gives exactly the
author's objective, −132117.083019988713781031606579922836… (the same
rational). This value is 5.1e-6 below the lower end of the stated enclosure,
as the author says. So the class does not change, and the margin is slightly
larger.

**Conclusion for each pair.** Each listed bound is invalid as listed, because
an exactly feasible point has a smaller objective. Each margin is within the
audit's slack (half a unit in the last shown digit). Measured against the
display unit (half a unit in the coarser of the 10th significant digit and
the 8th decimal):
- spring stays within the slack (0.871 of it);
- the other 7 pairs exceed it by factors of 93 to 6233.

## 3. spring global optimum (side result)

`step3_spring.py` gives an independent proof with exact rational comparisons.
The model is reduced to one variable x5 for each (i4, wire diameter)
combination. At 200 random rational points, the reduced formulas match every
OSIL row and the objective exactly.

The objective, (a + bN)·d³·x5, is increasing in x5. I split the 1100
combinations as follows:
- 723 are excluded by simple constraints: the x3 bounds, e6 and e7.
- 0 of the remaining combinations can reach an objective ≤ T, where T is the
  lower end of the bracket of f* given below (T < f*).
  - Either the relaxed lower bound (x5 ≥ max(1.1, 0.414/d, cbrt(L3·d/(kN))))
    exceeds T,
  - or e4 fails on the whole remaining x5 interval.
  - For e4 I use the exact identity x5·x6 = x5 + 3/4 + 3/(4(x5 − 1)) + 0.615,
    which is convex for x5 > 1, with minimum value 2.365 + √3 at
    x5 = 1 + √3/2. √3 is bracketed by rationals.
- The combination (9, b11) cannot reach ≤ T either. Its infimum is
  f* = (a + 9b)·0.283³·cbrt(L3·0.283/(9k)).

Result: the global optimum lies in

[0.84624566564315428125166463503714129527532857794010,
 0.84624566564315428125166463503714129527534815925597],

with the upper end attained by my exactly feasible point. This confirms the
author's 25-decimal value 0.8462456656431542812516646.

It also confirms:
- The listed bounds 0.84624567 equal f* rounded at the 8th decimal.
- The bold primal 0.8462441 (p3; `minlplib.solu` =best= 0.8462441005) is
  1.57e-6 below the optimum, so no exactly feasible point attains it.

A floating-point enumeration, which is evidence only, also reproduces the
author's counts:
- 210 feasible combinations (890 infeasible);
- second best 0.85928 at (5, b12).

## 4. Page parsing and screen

| check | result |
|---|---|
| my parse of all 1633 stored pages against `pages.json` (points: label, value, infeas, section, date, bold; duals: value, solver, date, bold; sense; problem type) | 0 differences; 2816 points, 11086 duals |
| my own required subset: 50 random pages (seed 777) + the 23 finding pages (the finding list re-derived from `results.json`) | 73 pages, 170 points, 521 duals, 0 differences |
| the author's subset (seed 20261001), recounted | 73 pages, 142 points, 507 duals, 0 differences |
| listing fields in `instances.html` (type, convex, #vars, #cons, S, listing dual, listing primal) | 1633 rows, 11431 fields, 0 differences |
| screen recomputed from my parse | 158 flagged pairs, 46 instances, 56 points, 131 (instance, solver) pairs, 3851 ties on 1133 instances. Identical to `screen.json` (pairs and ties) and to the pair set of `results.json`. No point with infeas > 1e-5 lies beyond any dual |
| live re-fetch (2026-10-01) | the 4 (i-r) pages: my parse unchanged; the author's 23 live copies in `pages_live/`: my parse identical to the stored pages |

## 5. Display precision and the 6-digit question

- **Digit histograms.** With the author's definition (first to last nonzero
  digit; zero and inf excluded), I reproduce the histograms exactly:
  - duals dated 17 Sep 2013: 59 with 6 digits, 2 with 7;
  - other duals: 263 with 6 digits, 471 with 7;
  - points: 98 with 6 digits, 149 with 7.
- **Rounded points.** All 7 short values equal the best listed point rounded
  half-up to 6 significant digits. On the same pages, other entries show
  more digits: BARON −132117.083 (eniplac), GUROBI 4099.059954 (lop97icx),
  BONMIN 119948.6882 (stockcycle).
- **Decimals.** No value shows more than 8 decimals (13,847 finite values).
- **Supporting evidence for the author's "display unit"** (my own test,
  `step10_display_rule.py`, floating point). I tested the rule "round to 10
  significant digits, print with 8 decimals, strip trailing zeros" on all
  13,847 finite values:
  - 13,723 values are fixed points of the rule;
  - 122 others are "-0." (only the sign of zero differs);
  - only 2 show more digits than the rule allows: hydroenergy1 209721.016897
    and optcdeg2 GUROBI 292.41713458.
  - The rule also reproduces artifacts such as 160912612.40000001 and
    −99999999809999994880.
  So the page display does not round more coarsely than 10 significant
  digits. A displayed "−132117." then means a stored value within 5e-5 of
  −132117, unless the value was rounded before it was stored. The listed data
  cannot decide that, as the author says. The author's statement that the 7
  eniplac, lop97icx and stockcycle pairs are (i-r) only under pre-storage
  6-digit rounding is correct.

## 6. Issues

All issues are minor. None changes a class, count, margin or verdict.

1. **`report.md` is missing (process).** The harness blocked it, and the full
   text exists only in the structured summary. The copy I received was cut
   off at "fetch_sols.py, parse_check.py, digits_check.py, refetch_page" in
   Section 2. I could therefore not review the rest of Section 2 or the list
   of commands run. The integration step needs the full text from the
   orchestrator's record.
2. **">10 significant digits" count.** The report says "35 values show 11 to
   20 significant digits". The count 35 comes from `parse_check.py`, which
   only counts values with a nonempty fractional part; these 35 have 11 to 17
   digits. Two other counts are possible:
   - With the author's own digit definition and no such filter, 38 values
     (11 to 19 digits). This adds −99999999809999994880. on gasoil50,
     gasoil100 and shiporig.
   - Counting the trailing zeros of integer-valued displays, 46 values (11 to
     20 digits).

   The conclusion is unaffected: under every definition, no such value is in
   a flagged pair, and the ties are only on fac1, fac2 and waternd_fosspoly0.
   Suggested fix: state the definition, or say "35 values with decimals show
   11 to 17 significant digits; 3 integer-valued displays show up to 20".
3. **spring wording.** "They are not solver errors" goes slightly beyond the
   data. The listing is consistent with a valid bound shown at 8 decimals,
   but the data cannot show that the stored solver value was ≤ f*. Suggested
   wording: "need not be solver errors; display rounding explains them".
4. **SCIP cross-check log (evidence only).** For spring,
   `logs/xcheck_scip.log` shows "rel. diff 1.0e-09". This is because the
   bisection on nlobjvar finds the smallest value SCIP accepts, which is
   g(x) minus the 1e-9 feasibility tolerance. It is not a disagreement. If
   the report quotes this check, it should say so.

## 7. Commands run by the reviewer

All commands ran in `research-20260929/publication/reviews/audit-ir-r1/`
with Python 3.13. The final run of each completed without error; the table
notes the earlier failed or corrected runs. Results are as stated above.

| # | command | outcome |
|---|---|---|
| 1 | `python3 step1_listed.py` | lop97icx p2 and stockcycle p2 have 0 exact violations; eniplac p2 has 31 (max 2.47e-10); spring p3 has 4 (max 9.9e-9) and spring p2 has 4 (max 4.9e-7); exact objectives as in Section 2 |
| 2 | `python3 step2_eniplac.py` | both eniplac points have 0 violations; the listed-point objective equals the author's rational; the centre-based point is inside the enclosure |
| 3 | `python3 step3_spring.py` (run twice; the second run after appending the e4 analysis) | spring point has 0 violations; global optimum enclosure; 0 combinations left; 210 feasible combinations (float) |
| 4 | `python3 step4_pages.py` (the first run failed on a key-matching bug in my parser, fixed with `sed`, then rerun) | 0 differences on all 1633 pages and on my subset |
| 5 | `python3 step5_digits.py`, `python3 step5b_digits.py` | digit statistics (Section 5; item 2 of Section 6) |
| 6 | `python3 step6_screen.py` (run twice; the second run after appending the tie comparison) | 158 pairs and 3851 ties, identical to `screen.json` |
| 7 | `python3 step7_listing.py` | 11431 listing fields, 0 differences |
| 8 | `python3 step8_live.py` (9 requests, 1 s apart) | pages and points unchanged |
| 9 | inline heredoc, saved as `step8b_osil_live.py` (4 requests, 1 s apart) | OSIL files identical to the cache |
| 10 | `python3 step9_scip_xcheck.py` (run twice; the first run set nlobjvar to the full objective, which is wrong for lop97icx's linear-plus-quadratic objective; fixed to the nonlinear part) | SCIP agrees (Section 1) |
| 11 | `python3 step10_display_rule.py` and an inline follow-up (now appended to the script) | 13,723 fixed points; 122 "-0."; 2 exceptions |
| 12 | inline heredoc, saved as `step4b_author_subset.py` | the author's subset is 142 points and 507 duals, 0 differences |
| 13 | read-only inspection (`grep`, `sed`, `cat`, `ls`) of the audit report, `results.json`, `pages.json`, the OSIL files, and the author's scripts and logs | not checks in themselves |

No CI or project-wide checks were run. Every result above comes from these
targeted commands.
