# Review of track primal-dtoc5-lukvle10 (r1)

Verdict: verified. Written to disk by the root from the reviewer's structured return value (the harness blocks subagents from writing report files).

## Summary

I found no blocker or major issue. Both points are exactly feasible for the cached OSIL models, and every objective enclosure and gap in the author's results table matches my independent code. All four issues are minor.

What I checked, all with my own code (no imports from the author's code):
- OSIL reader: written for this review (osil_rev.py). It reads the models in exact Fractions and handles mult/incr compression, row-major or column-major linear storage, quadratic terms and expression trees.
- Model descriptions: the author's descriptions of both models match the OSIL files exactly.
  - dtoc5: 99,999 variables, all continuous. Only x50001 = y_0 is bounded (lb = ub = 1). Rows: -(1/50000)u_t + y_t - y_{t+1} + (1/12500)y_t^2 = 0. Objective: (1/50000)(sum u_t^2 + sum_{t<T} y_t^2).
  - lukvle10: 1000 free continuous variables. 998 rows: -x_j + 3x_{j+1} - 2x_{j+2} - 2x_{j+1}^2 = -1. The objective is the 1000 power terms over the pairs (2i, 2i+1), both ways.

dtoc5 (proved, exact rational arithmetic):
- The point file has 99,999 exact decimals (states 30 decimals, controls up to 60).
- All 49,999 rows and all bounds hold exactly. There are no integer variables.
- The exact objective equals the author's rational (124-digit denominator), in [5.3896721191811404674239664991362718688313, ...8314].
- Gap upper bounds:
  - against the summary dual 5.38967211918114: 4.675e-16 absolute, 8.673e-17 relative;
  - against the verifier's lower end 5.3896721191811404674239647238640027 (and against the author's 30-digit truncation of it): 1.776e-24 absolute, 3.294e-25 relative.
- Negative test: adding 1e-60 to x500 makes exactly row e500 fail.
- Assumption: Python Fraction and integer arithmetic are correct.

lukvle10 (proved, given the stated assumptions):
- Construction: I derived the elimination order from the OSIL myself. Each row is linear in exactly one unknown variable with a nonzero coefficient; the seeds are x1 and x2. With the exact 640-decimal seeds, solving the rows forward defines a rational point x* that satisfies every row exactly. All variables are free and continuous, so x* is exactly feasible.
- Coordinate enclosure: integer fixed-point intervals with exact floor/ceil rounding. Maximum width 4.3e-537 at P = 3400 bits and 4.6e-236 at 2400 bits. No interval contains 0; min |x| = 0.260029.
- Objective enclosure, computed two ways:
  - (a) mpmath.iv exp and log at P + 128 bits, with exact conversion into iv intervals (assumption: mpmath iv rounds outward correctly);
  - (b) a second route with no mpmath and no floating point: integer arithmetic only, with ln from the atanh series and exp from argument halving plus Taylor, both with explicit remainder bounds. Only Python integer arithmetic is assumed. A sanity test of 600 random ln/exp bounds against mpmath found 0 failures.
- Both routes give f(x*) in [352.238025406495622630871271029366464797997889406, ...407]. This lies inside the author's enclosure [...4647979978, ...4647979979]e-40.
- Every coordinate enclosure lies inside the saved box (maximum radius 5.0e-61).
- Gap upper bound against 352.2380254050784: 1.418e-9 absolute, 4.024e-12 relative. The same holds against the certified end 352.23802540507845563.

Numerical checks only (evidence, not proof):
- The author's seed-sensitivity illustration reproduces exactly:
  - with p5's seeds, |x| first exceeds 10 at index 40;
  - D = 420: objective 352.98371886907387985;
  - D = 440: objective 352.23802540649563853;
  - D = 460: max deviation 6.78e-26;
  - D = 640: max deviation 5.82e-206.
- The KKT residuals of x* are given in issue 2.
- No background job of this track is running. The dtoc5 GAMS processes on the machine belong to the solver-runs track.

Issues (all minor; details in the issues list):
1. report.md is not on disk, and the copy I received is cut off, so I could not check the commands section.
2. 'The whole remaining gap is on the dual side, because our point is a KKT point to more than 600 digits' is unproved. KKT does not imply global optimality, and x* itself matches the KKT point only to about 205 digits.
3. The '4.8e-13 below p5' figure uses p5's displayed value; evaluated at p5's own values the difference is 5.1e-13.
4. gaps.py's sci_up() can print a value ten times too small when the mantissa rounds up to 10. It does not affect the current numbers.

What should change for the paper: the author's claims hold. The sentence in the summary that says no exactly feasible point was constructed for dtoc5 and lukvle10 should be updated in integration, and the KKT sentence should be reworded as in issue 2.

The review .md was not written because subagents may not write report .md files; the integration step should save this text at the report_path.

## Issues

- **minor**: report.md is not on disk. The harness refused the author's Write, and the copy of the report text that reached me is cut off partway through the lukvle10 construction (at 'Each iteration c'). So I could not review the rest of the lukvle10 method, the assumptions list or the commands section. The integration step must save the full text, and round 2 should check that it lists the commands and keeps the proved/numerical labels.
- **minor**: Overclaim in 'What changes for the paper': 'The whole remaining gap is on the dual side, because our point is a KKT point to more than 600 digits.' (a) A KKT point need not be a global minimizer, and nothing here proves that x* is one, so it is unproved that the 1.4e-9 gap lies wholly on the dual side. (b) The 600-digit residual belongs to the unrounded KKT point (logs/lukvle10_kkt_x.txt). My check found row residual 8.6e-639 and least-squares stationarity residual 1.0e-640 there. The exactly feasible point x* (seeds rounded to 640 decimals) differs from that point by up to 5.8e-206 (at x1000), and its stationarity residual with least-squares multipliers is 1.4e-205. Suggested wording: 'x* agrees with a numerically computed KKT point to about 205 digits; if that KKT point is the global minimizer, the remaining gap is on the dual side.'
- **minor**: The p5 comparison ('4.8e-13 below MINLPLib point p5 (352.2380254064961)') is measured against the displayed value. Evaluating the objective at p5's 15-digit values in open-instances/minlplib_sol/lukvle10.p5.sol gives 352.23802540649614, which is 5.1e-13 above f(x*). The sol file's objvar line says 352.238025406498025. The row violation 3.48e-15 is confirmed. The report should say which p5 value it compares against.
- **minor**: Latent display bug in gaps.py, sci_up(): when the 4-digit mantissa rounds up to 10 (for example m = 9.9999), it prints '1.0000e{e}', which is ten times too small and so not an upper bound. None of the six current gap values triggers it; my own code reproduces all six. Fix it if gaps.py is reused.

## Commands run

- `python3 publication/reviews/primal-dtoc5-lukvle10-r1/check_dtoc5.py  -> exit 0, 9.9 s: 0 bad rows, 0 bad bounds, 0 integer variables; exact objective equals the author's rational; gaps 4.675e-16 / 1.776e-24 absolute; perturbing x500 makes only e500 fail (logs/check_dtoc5.json)`
- `python3 publication/reviews/primal-dtoc5-lukvle10-r1/check_lukvle10.py 3400  -> exit 0: elimination order 998 rows, seeds x1 x2; row form and objective pairs match the OSIL; max coordinate width 4.289e-537; f in [352.238025406495622630871271029366464797997889406, ...407]; inside the author's enclosure and box; gap 1.418e-9 absolute, 4.024e-12 relative`
- `python3 publication/reviews/primal-dtoc5-lukvle10-r1/check_lukvle10.py 2400  -> exit 0: same objective enclosure, max coordinate width 4.595e-236`
- `python3 publication/reviews/primal-dtoc5-lukvle10-r1/objective_noniv_lukvle10.py 400 and 600  -> exit 0: same 45-digit enclosure with integer-only ln/exp, width 2^-373 and 2^-573; inside the author's enclosure`
- `inline python: sanity test of the reviewer's integer ln/exp bounds against mpmath at 200 digits -> 0 failures in 600 random tests (logs/noniv_selftest.log)`
- `python3 publication/reviews/primal-dtoc5-lukvle10-r1/kkt_lukvle10.py  -> numerical only: KKT point row residual 1e-638.06, least-squares stationarity residual 1e-640.0; x* deviation from the KKT point 5.8e-206, stationarity residual 1e-204.86; stored multipliers have only about 40 digits`
- `python3 publication/reviews/primal-dtoc5-lukvle10-r1/seed_sens_lukvle10.py  -> numerical only: reproduces the author's p5 escape index 40 and the D = 420/440/460/640 values`
- `inline python (mpmath 50 digits): f(p5) = 352.23802540649613695, max row violation 3.4832e-15, f(p5) - f(x*) = 5.14e-13`
- `inspection: ls/cat/zcat/awk on the author's logs and point files (seed decimals 640/640; box centre decimals 59-60; dtoc5 decimals 60/30); grep/sed on the summary, closing-confirm-r2 and the verifier's v_dtoc5.py and dtoc5_verify.json to identify the dual bounds; regex tag census of both OSIL files; ps check for running jobs of this track (none)`
