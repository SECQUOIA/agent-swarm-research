<!-- Written to disk by the root from the structured return value of agent 'author:primal-dtoc5-lukvle10' (the harness blocks subagents from writing report files). Status: complete. -->

# Exactly feasible primal points for dtoc5 and lukvle10

Date: 2026-10-01. Output folder: /workspace/minlp-notes/research-20260929/publication/primal/dtoc5-lukvle10 (OUTDIR). Models: the cached ~/.cache/minlplib/minlplib/osil/dtoc5.osil and lukvle10.osil.

## Result

Both instances now have a point that satisfies every row and variable bound of the OSIL model exactly. Neither model has integer variables. Each point comes with a rigorous objective enclosure and a rigorous gap to our dual bound.

| instance | point file(s) | how exactness is shown | objective of the exactly feasible point | our dual (summary) | rigorous gap (upper bound) |
|---|---|---|---|---|---|
| dtoc5 | points/dtoc5_point.txt.gz (all 99,999 values as exact decimals) | every row, bound and the objective evaluated in exact rational arithmetic | the exact rational in logs/dtoc5_check_objective_exact.txt; 5.3896721191811404674239664991362718688313 <= f <= ...8314 | 5.38967211918114 | 4.675e-16 abs, 8.673e-17 rel |
| lukvle10 | points/lukvle10_seed.txt (2 exact rational seeds, 640 decimals) and points/lukvle10_box.txt.gz (centre +- radius for all 1000 variables, radius <= 5e-61) | the point is defined by the seeds and the rows, so every row holds exactly; every coordinate is enclosed with outward-rounded intervals | f in [352.2380254064956226308712710293664647979978, 352.2380254064956226308712710293664647979979] | 352.2380254050784 | 1.418e-9 abs, 4.024e-12 rel |

Against the verifier's sharper dtoc5 bound (lower end 5.38967211918114046742396472386..., from reviews/open-instances-verification/logs/dtoc5_verify.json), the dtoc5 gap is at most 1.776e-24 (3.294e-25 relative).

What changes for the paper:
- dtoc5: replace the summary primal display 5.38967211918114 by 5.389672119181141. The old decimal remains valid as a dual display but lies below the exact point objective. The gap is now measured against an exactly feasible point. It is below 4.7e-16 against the summary's dual, and nearly all of that comes from displaying the dual to 15 digits.
- lukvle10: the gap stays at 1.4e-9, but its primal side is now an exactly feasible point. That point's value is 4.8e-13 below p5's displayed objective 352.2380254064961. Evaluating the objective at p5's stored 15-digit coordinates instead gives 352.23802540649613695, about 5.14e-13 above f(x*); its objvar line is a third value, 352.238025406498025. The maximum row violation of p5 is 3.48e-15. The exactly feasible x* agrees with the numerical KKT point to about 205 digits (max coordinate difference 5.8e-206; stationarity residual about 1.4e-205). KKT conditions do not prove global optimality. If that KKT point is the global minimizer, the remaining gap is on the dual side.
- The summary sentence "For lnts50-400, dtoc5, lukvle10, chain50-400 and powerflow... no exactly feasible point was constructed" no longer holds for dtoc5 and lukvle10. I did not edit the summary.

## dtoc5

Model (asserted from the OSIL with exact constants in dtoc5_construct.py):
- 99,999 variables: u_t = x_{t+2} for t < T = 49,999, and y_t = x_{50001+t} for t <= T.
- All variables are free except y_0, which has lb = ub = 1.
- Objective: min (1/50000)(sum_{t<T} u_t^2 + sum_{t<T} y_t^2).
- Rows: -(1/50000) u_t + y_t - y_{t+1} + (1/12500) y_t^2 = 0. The OSIL coefficients 2e-5 and 8e-5 are exactly 1/50000 and 1/12500.

Construction:
1. Start from the existing double-precision Newton solution (open-instances/logs/dtoc5_y.npy). Three Newton steps in 50-digit mpmath (tridiagonal Hessian, Thomas algorithm) reduced the max gradient from 2.9e-11 to 4.8e-26 to 4.3e-46; the last step was 1.4e-49.
2. Round y_1..y_T to 30 decimals and set y_0 = 1.
3. Compute each control from its row in exact rational arithmetic: u_t = 50000(y_t - y_{t+1}) + 4 y_t^2. This is a terminating decimal with at most 60 decimals.

Every row therefore holds exactly by construction.

Checks:
- check_exact_point.py is generic and uses my OSIL reader, osil_exact.py. It evaluates all 49,999 rows, all bounds, the integrality requirements (there are none) and the objective in Python Fraction arithmetic. Result: 0 failures. The objective is an exact rational with a 124-digit denominator.
- Negative test: adding 1e-60 to one control (x500) makes the checker report exactly one failing row (e500).
- dtoc5_crosscheck.py re-reads the OSIL with the verifier's independently written reader and row evaluator (reviews/open-instances-verification/osilx.py), using num = Fraction. Result: 0 bad rows or bounds, and the identical exact objective. The driver script is mine.
- Assumptions: Python Fraction and integer arithmetic are correct, and the two OSIL readers interpret the file correctly; they agree.

## lukvle10

Model (asserted from the OSIL):
- 1000 free continuous variables x_0..x_999 (names x1..x1000).
- 998 equality rows: -x_j + 3x_{j+1} - 2x_{j+2} - 2x_{j+1}^2 = -1.
- Objective: sum over pairs of power(square(x_a), square(x_b)+1) + power(square(x_b), square(x_a)+1).

Why a plain rational point is not practical:
- Row j gives x_{j+2} as a polynomial in (x_j, x_{j+1}). With rational seeds, the denominator of each new coordinate is at least the square of the previous one, so the exact rationals double in size every step and cannot be written out.
- The near-optimal trajectory follows the saddle at -1/sqrt2 (eigenvalues 2.73 and 0.18) for about 990 steps. Forward propagation therefore amplifies seed errors by about 2.73^999, roughly 1e436.

Seed-sensitivity illustration (lukvle10_seed_sensitivity.py; 1500-digit floating point, not a proof):
- With p5's 15-digit seeds, the trajectory leaves |x| <= 10 at index 40.
- With seeds that match the KKT point to 50-420 decimals, the trajectory falls off the saddle early. These points are still exactly feasible, but their objectives are 352.89-353.00.
- With 440 decimals the objective is 352.2380254064956; with 460 or more decimals it agrees with the KKT value to 20 digits.

Construction:
1. KKT point (lukvle10_kkt.py; heuristic). Start from p5 with least-squares multipliers. The KKT system has 1998 unknowns. Each iteration computes the residual in 650-digit mpmath and solves for the correction with the double-precision KKT matrix (cond 5.4). Each iteration gains about 15.6 digits; after 41 iterations the residual fell from 4.4e-14 to 1.5e-638. The KKT objective is 352.23802540649562263087127102..., and the maximum distance from p5 is 1.9e-14.
2. Seeds: x_0 and x_1 are the KKT values rounded to 640 decimals.
3. The point x* is the unique vector with these seeds whose other coordinates solve the rows. It is rational and satisfies all 998 rows exactly. All variables are free and there is no integrality.
4. Enclosure (lukvle10_enclose.py):
   - The script asserts the triangular pivot structure generically from the OSIL: each row is linear in its largest-index variable, with an exact nonzero coefficient; that variable does not appear in the quadratic or nonlinear parts; the pivots are distinct. The seeds are x1 and x2.
   - The recursion is run in mpmath iv at 750 digits. The maximum coordinate radius is 8.0e-265.
   - Every |x_k| is at least 0.26003, so every power base is at least 0.0676 > 0, and a^e is evaluated as exp(e log a).
   - As a sanity check, every row, re-evaluated over the enclosure, contains its right-hand side.
5. Saved box: each variable gets a 60-decimal centre and a radius, both exact decimals. Each radius is rounded up and is at most 5e-61, and the box contains the interval enclosure.
6. Objective over the saved box: [352.2380254064956226308712710293664647979978, ...979] (width 6.1e-58). The tight enclosure (width 2.0e-264) gives the same 40 decimals.

Second implementation without mpmath (lukvle10_crosscheck.py):
- It reads the OSIL with the verifier's reader (osilx.py) and uses my own fixed-point interval arithmetic on Python integers, with explicit floor/ceil rounding.
- exp is enclosed by a Taylor series with an explicit remainder after dividing the argument by 2^16, followed by 16 squarings. log uses the atanh series after reduction to [1,2), with ln2 = 2 atanh(1/3).
- It propagates the rows at 2^-2700 resolution (max coordinate width 2.6e-326) and confirms that every enclosure lies inside the saved box.
- It encloses the objective at 2^-500 resolution, over both the coordinate enclosures and the box. It gives the same 40-decimal enclosure as mpmath.
- So the result does not depend on mpmath's exp and log. I wrote both implementations, so this is a second implementation, not an independent review.

Assumptions:
- Main result: mpmath iv 1.3.0 encloses +, -, *, /, integer powers, exp and log correctly.
- Second implementation: Python integer arithmetic is correct, and the standard remainder bounds hold: exp remainder <= |w|^(N+1)/(N+1)! e^|w| with |w| <= 2^-10; atanh remainder <= t^(2k+3)/((2k+3)(1-t^2)) with 0 <= t < 1/2.
- The OSIL power node with a positive base means the real power exp(e log a).
- The KKT computation only chooses the seeds; the claim does not depend on its accuracy.

## What is proved and what is not

Proved:
- dtoc5 (exact rational arithmetic): the point satisfies every row and bound exactly, and its objective is the stated exact rational.
- lukvle10 (interval arithmetic under the stated assumptions, confirmed by a second implementation): the seed-defined point satisfies every row exactly, lies in the saved box, and has its objective in the stated interval.
- The gaps are upper bounds computed in exact rational arithmetic and rounded up (gaps.py). The dual bounds are taken from the summary and were not rechecked here.

Numerical only:
- the KKT solve and the dtoc5 Newton polish, which only choose the points;
- the seed-sensitivity illustration;
- the agreement of x* with the KKT point to about 205 digits. No proof of local or global optimality of that KKT point was attempted, so the remaining gap is not assigned entirely to the dual side.

Caveats:
- open-instances/logs/dtoc5_bound.json still holds the authors' older dtoc5 bound 5.3896721191811325. Against it the gap would be 8.0e-15. The summary's 5.38967211918114 comes from the verifier. The paper must say which dual it uses.
- The dtoc5 point file is 2.4 MB gzip-compressed.
- Independent review r1 rechecked the exact points, enclosures and gaps (`../../reviews/primal-dtoc5-lukvle10-review-r1.md`).

## Files (in OUTDIR)

- Code: osil_exact.py, exact_io.py, check_exact_point.py, dtoc5_construct.py, dtoc5_crosscheck.py, lukvle10_kkt.py, lukvle10_enclose.py, lukvle10_crosscheck.py, lukvle10_seed_sensitivity.py, gaps.py.
- Points: points/dtoc5_point.txt.gz, points/lukvle10_seed.txt, points/lukvle10_box.txt.gz.
- Logs: logs/*.json, logs/*.log, logs/dtoc5_check_objective_exact.txt (exact p/q), logs/lukvle10_kkt_x.txt (KKT point, 640 digits), logs/lukvle10_kkt_lam.txt (multipliers, 40 digits).

## Commands run (from the agent's structured return)

- `python3 dtoc5_construct.py -> structure asserted; Newton polish (max grad 2.9e-11 -> 4.8e-26 -> 4.3e-46); point written; 19 s`
- `python3 check_exact_point.py dtoc5 points/dtoc5_point.txt.gz logs/dtoc5_check.json -> exactly feasible, 0 row/bound/integrality failures; 9.3 s`
- `python3 check_exact_point.py dtoc5 logs/tmp_perturbed.txt.gz logs/tmp_perturbed_check.json (x500 + 1e-60, temporary files deleted) -> 1 row failure (e500), as expected`
- `python3 dtoc5_crosscheck.py -> 0 bad rows/bounds/integrality with the verifier's osilx reader; exact objective identical; 4.3 s`
- `python3 lukvle10_kkt.py -> cond(K)=5.4; KKT residual 4.4e-14 -> 1.5e-638 in 41 iterations; KKT objective 352.2380254064956226...; 63 s`
- `python3 lukvle10_enclose.py (run twice; the second run only changed how the dual is displayed in the JSON) -> 998 pivot rows, seeds x1,x2; coordinate radius <= 8.0e-265; box objective enclosure [..979978, ..979979]; 4 s`
- `python3 lukvle10_crosscheck.py (run twice; the second run fixed a float underflow in the printed width) -> all coordinate enclosures inside the saved box; identical 40-decimal objective enclosure; 11 s`
- `python3 lukvle10_seed_sensitivity.py -> p5 seeds diverge at index 40; 50-420 seed decimals give objectives 352.89-353.00; 460 or more give the KKT value`
- `python3 gaps.py -> dtoc5 4.675e-16 (vs summary) and 1.776e-24 (vs verifier); lukvle10 1.418e-9 abs, 4.024e-12 rel`
- `Exploratory: python OSIL tag/attribute counts and section dumps for both OSIL files; small mpmath iv behaviour tests; gmpy2/flint availability check (neither installed)`

## Open issues (from the agent's structured return)

- Independent review r1 rechecked the exact points, enclosures and gaps (`../../reviews/primal-dtoc5-lukvle10-review-r1.md`). The dtoc5 cross-check and the lukvle10 second implementation use the verifier's OSIL reader, but I wrote all the arithmetic and driver code.
- Inconsistency to resolve: open-instances/logs/dtoc5_bound.json still holds the older authors' dtoc5 dual 5.3896721191811325, while the summary uses 5.38967211918114 (from the verifier). Against the older value the dtoc5 gap would be 8.0e-15. The paper must say which dual it uses.
- The open-instances-summary.md sentence saying no exactly feasible point was constructed for dtoc5 and lukvle10 needs updating at integration; I did not edit it.
- It is not proved that the lukvle10 gap of 1.4e-9 lies entirely on the dual side; KKT agreement is numerical evidence only.
- No local or global optimality proof for the lukvle10 KKT point was attempted. Validity of the primal point does not depend on optimality.

## Response to review

Review: `../../reviews/primal-dtoc5-lukvle10-review-r1.md`. Checked and resolved on 2026-10-03.

| issue | resolution and evidence |
|---|---|
| 1. Missing or truncated report | The full report is on disk, with complete construction, assumptions, proved/numerical labels and command list. |
| 2. KKT overclaim | Removed the unconditional dual-side claim everywhere. Recorded 205-digit agreement of x* with the KKT vector and distinguished its residual from the unrounded vector; inspected r1 KKT evidence. |
| 3. p5 comparison | Distinguished the displayed value, coordinate-evaluated objective and objvar entry; re-evaluated the stored p5 coordinate objective in `logs/minor_review_check.log` without recomputing the point. |
| 4. sci_up carry | Fixed the mantissa carry with a minimal change in `gaps.py`; boundary cases in `minor_review_check.py` remain upper bounds. Current reported gaps were unaffected. |

Targeted check: `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 research-20260929/publication/primal/dtoc5-lukvle10/minor_review_check.py > research-20260929/publication/primal/dtoc5-lukvle10/logs/minor_review_check.log` (from the repository root). Results are in `logs/minor_review_check.log`. No main computation, solver campaign, project-wide verification or CI check was run for this revision.

### Round 2: independent minor-fixes review (2026-10-03)

Review: [minor-fixes-review-r1.md](../../reviews/minor-fixes-review-r1.md). Issue numbers below refer to that review.

| issue | resolution |
|---|---|
| 2 | Checked the exact objective rational; recorded dtoc5 primal 5.389672119181141, with the dual unchanged. |
| 12 | Qualified p5’s maximum row violation and removed the stale local-minimizer statement. |

Own exact checks and saved-source evidence: [check_r2.log](../../reviews/minor-fixes/check_r2.log). The full response is [response-r2.md](../../reviews/minor-fixes/response-r2.md); exact commands and results are in [commands.md](../../reviews/minor-fixes/commands.md). Integration edits remain pending in the main summary and audit report. No main computation or solver campaign was repeated.
