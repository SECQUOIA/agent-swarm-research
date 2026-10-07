<!-- Written to disk by the root from the structured return value of agent 'author:audit-ir' (the harness blocks subagents from writing report files). Status: complete; minor-review fixes applied 2026-10-03. -->

# Independent check of the audit's class (i-r) results and page parsing (track audit-ir, 2026-10-01)

The full report is on disk, including the exact constructions, parser checks, assumptions and command list. Independent review r1 verified the substantive claims. Nothing was committed and no one was contacted.

## 1. Summary

**All 12 (i-r) pairs are confirmed, with exact rational arithmetic.**
- For each pair, an exactly feasible point exists whose objective is below the listed dual bound.
- Each margin is within the audit's slack, which is half a unit in the last shown digit.
- All 12 entries are dated 17 Sep 2013.
- "Display unit" below means half a unit in the coarser of the 10th significant digit and the 8th decimal. The 10th-digit floor is a conservative choice; it changes no screened pair (Section 1).

| instance | solvers | listed d | audit slack | proven exactly feasible objective f | d − f | (d − f)/\|d\| | (d − f)/slack | (d − f)/display unit |
|---|---|---|---|---|---|---|---|---|
| eniplac | COUENNE, LINDO, SCIP | −132117. | 0.5 | −132117.08301998871378… (exact rational) | 0.0830200 | 6.28e-7 | 0.166 | 1660 |
| lop97icx | ANTIGONE | 4099.06 | 0.005 | 4099.059953600000099 exactly | 4.6399999901e-5 exactly | 1.13e-8 | 0.0093 | 92.8 |
| spring | ANTIGONE, BARON, COUENNE, LINDO, SCIP | 0.84624567 | 5e-9 | 0.84624566564315428125166463503… (exact rational) | 4.3568e-9 | 5.15e-9 | 0.871 | 0.871 |
| stockcycle | ANTIGONE, BARON, COUENNE | 119949. | 0.5 | 71969213/600 = 119948.68833… | 187/600 = 0.31167 | 2.60e-6 | 0.623 | 6233 |

That is 3 + 1 + 5 + 3 = 12 pairs. For spring, the two flagged points p2 and p3 have the same integer assignment and lead to the same exactly feasible point.

**Every stated enclosure in the audit report is confirmed.** Each contains the objective of an exactly feasible point built here.
- lop97icx and stockcycle: the listed point itself.
- spring: a rational point built from the listed point.
- eniplac: a point built from the audit's proof-box centre, used as input data. Its objective is −132117.083014502033660740…, inside [−132117.0830149, −132117.0830141].
- eniplac, built from the listed point instead: objective −132117.08301998871…. That is 5.1e-6 below the lower end of the stated enclosure, so the margin is slightly larger.
- The audit's repair (route C) gave up 5.5e-6 of objective by stepping into the interior. No class changes.

**spring is fully explained by rounding.**
- I proved the global optimum of spring exactly: 0.8462456656431542812516646… (25 decimals).
- The five listed bounds 0.84624567 equal this optimum rounded at the 8th decimal.
- None of the 13,847 numeric values on the pages has more than 8 decimals. So these entries are what an 8-decimal listing of the exact optimum shows. They need not be solver errors: display rounding explains these listed values. The listing alone cannot establish that the underlying stored solver bounds were at most the exact optimum.
- Side result: the bold primal bound on the spring page (0.8462441, point p3; minlplib.solu =best= 0.8462441005) lies 1.57e-6 below the exact optimum. No exactly feasible point attains it.

**eniplac, lop97icx and stockcycle (7 pairs) are within the slack only if the values were rounded to 6 significant digits before MINLPLib stored them.**
- The same pages show other bounds with 9 or 10 digits: eniplac BARON −132117.083, lop97icx GUROBI 4099.059954, stockcycle BONMIN 119948.6882. So the page display did not do this rounding.
- If the listed numbers are taken as exact, these 7 pairs would be class (i):
  - eniplac (6.3e-7 of |d|) and lop97icx (1.1e-8): tolerance-scale;
  - stockcycle (2.6e-6 of |d|): gross by the audit's 1e-6 label.
- Evidence, not proof, that the 6-digit rounding happened:
  - Among dual bounds dated 17 Sep 2013, 59 values show exactly 6 significant digits and only 2 show 7. Among all other dual bounds and among points, 7-digit values are more common than 6-digit ones (471 vs 263; 149 vs 98).
  - All 7 values equal the best listed point value rounded half-up to 6 digits.
- The listed data cannot decide this.

**The page parsing is confirmed.**
- I re-parsed all 1633 stored pages and instances.html with my own parser.
- There are zero differences from pages.json in:
  - 2816 points (label, value, infeas, section, date, bold);
  - 11086 dual bounds (value, solver, date, bold);
  - objective sense, problem type and file size of all 1633 pages;
  - 11431 listing fields.
- The required subset has zero differences: a random sample of 50 pages (seed 20261001) plus the 23 pages with a class (i), (i-r) or emfl finding, together 73 pages, 142 points and 507 dual bounds.
- The screen recomputed from my parse gives the same set of 158 flagged pairs and 3851 ties as screen.json: 46 instances, 56 points, 131 (instance, solver) pairs.
- The 23 finding pages fetched live on 2026-10-01 are unchanged.

**One correction to audit-report Section 2.** It says values are shown with "at most 10 significant digits and at most 8 decimals".
- The 8-decimal limit holds for all values.
- The 10-digit limit does not. 35 displayed entries (18 distinct strings) with a nonempty fractional part show 11 to 17 significant digits (first through last nonzero digit), for example GUROBI 292.41713458 on optcdeg2 and 160912612.40000001 on fac1.
- Without the fractional-part filter there are 38 displayed entries with 11–19 digits; counting trailing integer zeros as significant (for example in −10000000000.) gives 46 displayed entries with 11–20 digits. The extra integer-valued display −99999999809999994880. appears on gasoil50, gasoil100 and shiporig. `logs/minor_review_check.log` records all three definitions.
- No class depends on this. None of these values is in a flagged pair. Values on three instances (fac1, fac2, waternd_fosspoly0) occur in 17 display-tie pairs.
- The 10th-significant-digit slack floor no longer follows from a display limit. Retain it as an explicit conservative choice: an independent exact check finds that it changes the slack of 0 of the 158 screened pairs, so no screened-pair class changes.

## 2. Independence

**Own code** (all in the output folder):
- osilq.py: OSiL reader with exact Fraction evaluation and exact rational intervals.
- check_ir.py: exact checks and constructions for the four instances, and the margins.
- spring_global.py: the exact global optimum of spring.
- xcheck_scip.py: SCIP cross-check of the model reading.
- fetch_sols.py, parse_check.py, digits_check.py, refetch_pages.py.

**Not opened or imported:** audit.py, audit_eval.py, verify.py, verify_one.py, cert_*.py, parse_pages.py, and the reviewers' code (including osilx.py).

**Data used:**
- As inputs: the cached OSIL files, bound-audit/sol/, bound-audit/logs/verify/eniplac.p2.center.sol and bound-audit/pages/.
- As comparison targets only: pages.json, screen.json and results.json.

**Inputs checked.** The five flagged points were re-downloaded on 2026-10-01, sequentially with a 1 s delay. They are byte-identical to bound-audit/sol/. I also fetched spring.p1.

## 3. Method

**Reader.**
- Every number is converted from its decimal string to an exact Fraction.
- It handles mult/incr arrays, row-major and column-major coefficients, quadratic terms, summed nonlinear expressions, constants and binary default bounds.
- It raises on any unknown section, attribute or operator.
- The supported operators are sum, plus, minus, negate, times, product, divide, square, integer power, number and variable.
- All four instances are rational-function models. So every check is exact rational. No Krawczyk test was needed.

**Exact check:** every variable bound, integrality and both sides of every row, with the objective as an exact rational.

**Constructions:**
- lop97icx p2 and stockcycle p2: the listed point as is.
- eniplac p2:
  - x1..x24, x99..x110 and the binaries keep their listed decimals.
  - The other 81 variables are recomputed, each from an equality row that is linear in it: x25..x48, x49..x72, x73..x96 = q_i(x_i)·b_i, x97, x98 and x111..x117.
  - The demand rows e27..e32 hold exactly at the listed decimals. The largest change from the listed point is 2.9e-10.
  - From the audit's centre, one variable per demand row is also recomputed (x3, x7, x11, x16, x19, x21), because the centre misses those rows by about 4e-14.
- spring:
  - p2 and p3 share i4 = 9 and b11 = 1, so x2 = 0.283.
  - The objective increases with x1, and x3 ≥ lb(x3) = 1.78571428571429e-3 is binding. The listed points have x3 2.9e-16 below this bound.
  - With x3 at its bound, x5 = cbrt(A), where A = lb(x3)·x2/(9c) and c = 6.95652173913044e-7.
  - Rational point: x5 is rounded up at 1e-30, x1 = 0.283·x5, and x5, x6, x3 follow exactly from e2, e3 and e5. x3 then exceeds its bound by 9.1e-34.
  - Infimum point: the cube root is bracketed by rationals, checked by exact cubing. Its inequality rows are enclosed in exact rational intervals: e4 is 187991.19 ≤ 189000, e6 is 5.054 ≤ 14, e7 is 1.506 ≤ 3.

**Global optimum of spring:**
- For each integer assignment (i4 = n, x2 = c_k), the model reduces to one variable x5.
- The objective K_n·c_k³·x5 increases in x5. Every condition is an interval in x5. e4 becomes a quadratic, because g(x5) = x6·x5 is convex for x5 > 1.
- The script checks the reduction exactly against the model at 200 random rational points, for every row and the objective.
- Of the 1100 assignments, 890 are proven infeasible. The other 210 have their minima enclosed with width below 1e-29.
- The optimum is at i4 = 9, b11, with x3 ≥ lb binding. The next best is i4 = 5, b12, at 0.8592755….
- The optimum lies in [0.8462456656431542812516646, 0.846245665643154281251664635037…].

**Assumptions of the proofs:**
- Python's Fraction is exact.
- osilq.py reads the files correctly.
- The model is the cached OSIL file, and the points are the stored .sol files.

No floating-point number enters any proof.

**Cross-checks of the reading (evidence):**
- The exact objectives match the objvar entries of the .sol files and the page values.
- SCIP's own OSiL reader accepts all five proof points at feasibility tolerance 1e-9.
- SCIP's objectives agree to 2.4e-13 relative or better. The exception is spring, at 1.0e-9; this comes from the bisection on SCIP's objective row and equals the tolerance.
- Negative controls: these perturbations are rejected by both codes:
  - lop97icx x1 + 1e-6;
  - stockcycle x1 − 1e-6;
  - eniplac x73 + 1e-3;
  - spring x3 − 1e-6.

## 4. Details per instance

**lop97icx** (986 variables, 87 rows; solved):
- p2 (14 Sep 2009) is exactly feasible as listed, with f = 4099059953600000099/10^15.
- BARON's 4099.059949 is below f.
- GUROBI, LINDO, SCIP and SHOT list 4099.059954, a display tie with p2.

**stockcycle** (480 variables, 97 rows; marked convex, not marked solved):
- p2 (01 May 2001) is exactly feasible as listed, with f = 71969213/600.
- The listing row shows dual 119949. above primal 119948.6883.

**eniplac** (141 variables, 189 rows; solved):
- Listed p2 (26 Oct 2004) violates 31 equality rows by 4.8e-14 to 2.5e-10.
- The repaired points are in logs/eniplac.p2.exact.sol and logs/eniplac.p2.centre.exact.sol.

**spring** (17 variables, 8 rows; not marked solved):
- Point p1 (01 May 2001) has violations up to 1.1e-14. Its objective 0.84624566564315562… is within 1.4e-15 of the optimum: p1 is the optimal point, listed with rounded decimals.
- Point p3 violates e5 by 9.9e-9; point p2 violates e3 by 4.9e-7.
- MINLPLib's =bestdual= 0.8462206712 is valid.

## 5. Margins versus rounding slack

| pairs | invalid as listed | vs audit slack | vs display rounding | class if listed numbers are exact |
|---|---|---|---|---|
| spring × 5 | proven | 0.871 | 0.871 | (i-r), explained by 8-decimal rounding of the proven optimum |
| eniplac × 3 | proven | 0.166 | 1660 | (i), tolerance-scale (6.3e-7) |
| lop97icx × 1 | proven | 0.0093 | 92.8 | (i), tolerance-scale (1.1e-8) |
| stockcycle × 3 | proven | 0.623 | 6233 | (i), gross by the 1e-6 label (2.6e-6) |

- Under truncation (a full unit in the last shown digit), all 12 margins are 0.0046 to 0.44 of the unit.
- The closing bounds of eniplac and lop97icx stay below MINLPLib's 1e-6 gap convention even if read as exact.

**Digit histogram** (17 Sep 2013 dual bounds, counts for 1, 2, …, 10, >10 significant digits): 48, 65, 77, 36, 24, 59, 2, 17, 30, 86, 5.
- 11 of the 59 six-digit values equal a listed point value rounded half-up to 6 digits:
  - eniplac ×3, lop97icx, stockcycle ×3;
  - cecil_13 and hda ×2 (both audit (iii), "at most (i-r)");
  - product2.
- The batch is mixed: the spring entries of the same date show 8 digits.

## 6. What is proved and what is not

**Proved** (exact rational arithmetic):
- the 12 invalid-as-listed results with exact margins;
- an exactly feasible point inside each stated enclosure;
- the global optimum of spring to 25 decimals.

**Evidence only:**
- the SCIP cross-check;
- the reading of the digit histogram.

**Not done:**
- global optima of eniplac, lop97icx and stockcycle, so for those 7 pairs I cannot say whether a valid bound lies behind the listed number;
- instance change histories (the OSIL files carry a 2019 file date; the bounds are from 2013);
- the audit's other classes.

## Commands run (from the agent's structured return)

- `python3 fetch_sols.py: 5 points byte-identical to bound-audit/sol, spring.p1 fetched (logs/fetch_sols.log)`
- `python3 check_ir.py: 4 development runs. The second added the eniplac centre route. The third changed the adjust rule after the first rule (transfer variables) left e136 violated by 2.8e-14. The fourth saved the points. Final run: all 12 pairs confirmed (logs/check_ir.json, logs/check_ir.out)`
- `python3 xcheck_scip.py: 3 runs. The first two used a wrong objective control (SCIP keeps the linear part of lop97icx's objective outside nlobjvar); this was replaced by bisection. Final run: all points feasible at 1e-9, objectives agree, negative controls rejected (logs/xcheck_scip.log)`
- `python3 spring_global.py: 1100 assignments, 890 infeasible, 0 undecided, optimum enclosed (logs/spring_global.json, .log)`
- `python3 parse_check.py: 3 runs, adding the screen.json set comparison and then the negative control. Final run: 0 differences, control detected, screen identical (logs/parse_check.json, .log)`
- `python3 digits_check.py: digit histograms (logs/digits_check.json, .log)`
- `python3 refetch_pages.py: 23/23 unchanged (logs/refetch_pages.log). It ran a second time by mistake with output discarded; an offline re-comparison of that fetch gave 23/23 unchanged`
- `Exploratory inline python3: read results.json, pages.json, screen.json and the verify logs; evaluated listed points and the eniplac centre with osilq.py; surveyed HTML shapes and digit counts. No files changed outside the output folder`

## Open issues (from the agent's structured return)

- For eniplac, lop97icx and stockcycle (7 of the 12 pairs), 'within rounding' depends on whether the 2013 values were rounded to 6 significant digits before MINLPLib stored them. The page display did not do this rounding. The digit histogram supports it but cannot prove it. If the stored numbers are exact, these 7 pairs are class (i).
- The global optima of eniplac, lop97icx and stockcycle were not proven, so whether a valid bound lies behind the listed number is open for those 7 pairs. spring's optimum is proven.
- audit-report.md Section 2 should drop 'at most 10 significant digits' and define the counts as displayed entries (35 with a nonempty fractional part, 38 without that filter, or 46 counting trailing integer zeros). The 8-decimal limit holds.
- New finding for the paper: spring's bold primal bound 0.8462441 (p3) and minlplib.solu =best= 0.8462441005 lie 1.57e-6 below the proven exact optimum. This is the same pattern as emfl and camshape.
- Instance change histories were not checked: the OSIL files carry a 2019 file date and the bounds are from 2013.
- pages_live/ holds about 15 MB of re-fetched HTML. It is gitignored by the *.html rule.

## Response to review

Review: `../reviews/audit-ir-review-r1.md`. Checked and resolved on 2026-10-03.

| issue | resolution and evidence |
|---|---|
| 1. Missing and truncated report | The full report is on disk and its complete method and commands have been read. |
| 2. Digit count definition | Recounted the saved pages: 35 with a nonempty fractional part (11–17 digits); 38 without that filter (11–19); 46 if trailing integer zeros count (11–20). Corrected Section 1. |
| 3. spring solver-error wording | Reworded as "need not be solver errors; display rounding explains them". The underlying stored solver bound remains unknown. |
| 4. spring SCIP objective tolerance | No further numerical change needed: the report already explains the bisection/tolerance origin of the 1.0e-9 difference; checked `logs/xcheck_scip.log`. |

Targeted check: `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 research-20260929/publication/audit-ir/minor_review_check.py > research-20260929/publication/audit-ir/logs/minor_review_check.log` (from the repository root). Results are in `logs/minor_review_check.log`. No main computation, solver campaign, project-wide verification or CI check was run for this revision.

### Round 2: independent minor-fixes review (2026-10-03)

Review: [minor-fixes-review-r1.md](../reviews/minor-fixes-review-r1.md). Issue numbers below refer to that review.

| issue | resolution |
|---|---|
| 6 | Kept the 10th-digit floor as an explicit conservative choice: 0 of 158 screened pairs affected. |
| 21 | Defined displayed-entry multiplicity, trailing integer zeros and the 17 tie pairs on three instances. |

Own exact checks and saved-source evidence: [check_r2.log](../reviews/minor-fixes/check_r2.log). The full response is [response-r2.md](../reviews/minor-fixes/response-r2.md); exact commands and results are in [commands.md](../reviews/minor-fixes/commands.md). Integration edits remain pending in the main summary and audit report. No main computation or solver campaign was repeated.

### Round 3: independent minor-fixes review (2026-10-03)

Review: [minor-fixes-review-r2.md](../reviews/minor-fixes-review-r2.md). Issue numbers below refer to that review.

| issue | resolution and evidence |
|---|---|
| 9 | Replaced the display-limit justification by the explicit conservative-floor choice; defined the 35/38/46 counts as displayed entries in the remaining sentence. |

Targeted checks and the full response: [response-r3.md](../reviews/minor-fixes/response-r3.md), [check_r3.log](../reviews/minor-fixes/check_r3.log) and [commands-r3.json](../reviews/minor-fixes/commands-r3.json). Scientific scripts were run only in disposable copies. Scientific logs and point files in this track were preserved. No solver campaign or project-wide check was run.
