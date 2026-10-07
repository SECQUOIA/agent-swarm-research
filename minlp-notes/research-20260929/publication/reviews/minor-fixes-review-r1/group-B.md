# Verifier group B: primal/dtoc5-lukvle10 and primal/powerflow

P = research-20260929/publication. All my checks are in `scratch-B/` (scripts and logs). They use my own code: a generic OSIL reader and evaluator (ElementTree, exact Fractions for coefficients, mpmath for evaluation) and my own ceiling formatter. I imported nothing from the author's code except the function under test, `sci_up`, which I loaded through the AST so that gaps.py's top-level code does not run.

Result: every issue in both tracks is fixed correctly. I found no blocker or major problem. There is one integration-list omission (dtoc5 primal display, from the lead's extra check) and a few minor wording points.

## primal/dtoc5-lukvle10 (review: reviews/primal-dtoc5-lukvle10-review-r1.md)

### Issue 1: report.md missing or truncated. OK
- P/primal/dtoc5-lukvle10/report.md is complete. It contains the full lukvle10 construction (steps 1-6, the second implementation, assumptions), the "What is proved and what is not" section with Proved / Numerical only labels, the caveats, the file list and the commands list (lines 108-119). The text the reviewer saw cut off ("Each iteration c...") continues at line 61.
- The only change in the diff is the title, which no longer says "report.md could not be written".
- Cosmetic: the title on line 3 has a trailing space.

### Issue 2: KKT overclaim. OK, with one minor stale sentence
- I grepped the whole report for "dual side", "global", "optimal", "local minim", "entirely" and "600 digits". The remaining dual-side statements are all conditional or negative: line 20 ("KKT conditions do not prove global optimality. If that KKT point is the global minimizer, the remaining gap is on the dual side."), line 95 and line 126. The old unconditional sentence and the old "Numerical only" bullet, which rested on the 1e-638 residual, are both gone.
- 205-digit agreement, checked by my script (`scratch-B/check_dtoc5_lukvle10.py`). I computed x* from the 640-decimal seeds by forward row solving at 1500 digits. The pivot structure was derived generically from the OSIL. Results:
  - max |x* − x_KKT| = 5.817e-206 at x1000, i.e. 205.2 digits, which matches "about 205 digits" and "5.8e-206";
  - row residual of x* is 2e-1501 (rounding only);
  - min |x*| = 0.26003;
  - f(x*) = 352.23802540649562263087127102936646479799788940671, inside the reported enclosure.
- I did not recompute the stationarity residual 1.4e-205. It equals the reviewer's logged value 10^-204.86 = 1.38e-205 (reviews/primal-dtoc5-lukvle10-r1/logs/kkt_lukvle10.log).
- Minor (stale wording, pre-existing): report.md:127 says "The claim that the lukvle10 KKT point is a local minimizer is numerical only". The body no longer makes any local-minimizer claim, and line 95 says no proof of local or global optimality was attempted. Suggested fix: change line 127 to "No local or global optimality of the KKT point is claimed; validity of the primal value does not depend on it." Or delete the line.

### Issue 3: p5 comparison. OK, with one minor ambiguity
I evaluated the OSIL objective tree generically at 60 digits on open-instances/minlplib_sol/lukvle10.p5.sol:
- f(p5) = 352.2380254064961369473386; f(p5) − f(x*) = 5.143e-13 (report: 5.14e-13);
- display 352.2380254064961 − f(x*) = 4.774e-13 (report: 4.8e-13);
- objvar 352.238025406498025, which differs again (+2.40e-12);
- p5 max row violation = 3.483e-15 (report: 3.48e-15).

All four numbers match. Minor: in report.md:20, "The row violation is 3.48e-15" does not say whose violation it is. Suggested wording: "p5's maximum row violation is 3.48e-15."

### Issue 4: sci_up carry. OK
- The diff is minimal: `if d == 10**digits: d //= 10; e += 1`. This is correct because the exponent loop guarantees q < 10^(e+1), so 1.000e(e+1) is an upper bound.
- I compared the new and old sci_up with an independent reference: the smallest 4-significant-digit decimal ≥ q, found by exhaustive search over exponents.
  - Boundary cases: 9.9999e-13, 9.9995e-13, 9.99950001e-13 and 9.9994e-13 → 1.000e-12; exact powers 1e-12, 1e0, 1e5, 1e-300 → 1.000eK; 9.999e3 → 9.999e3; 9.9990001e3 → 1.000e4; 0.99999 → 1.000e0; 99999 → 1.000e5; 9.99999999999999999e-25 → 1.000e-24; 1.0001 → 1.001e0; 1.2340000001e-7 → 1.235e-7.
  - Plus 20,000 random values, half of them placed just below 4-digit or 10^k boundaries.
  - New sci_up: 0 mismatches, and every output is a well-formed d.ddd upper bound.
  - Old sci_up: wrong on 8 of the listed cases (for example 9.9999e-13 → "1.0000e-13").
- The six reported gaps are unchanged. Old, new, reference and logs/gaps.json all agree: 4.675e-16, 8.673e-17, 1.776e-24, 3.294e-25, 1.418e-9, 4.024e-12.
- Note: with digits=1 the new code would print "1.e{e}". This is not used anywhere (default digits=4).

### summary.md integration cells (rows 29-32): OK, but dtoc5 needs one more item (see the extra check)

## primal/powerflow (review: reviews/primal-powerflow-review-r1.md)

### Issue 1: missing report and commands. OK
- The report is complete. It lists construct, certify, certify with radius 1e-30, scip_check, the negative tests and the sha256 commands (lines 130-138). It states the mpmath iv assumption (line 92).
- The status line and line 3 were updated. Line 3 says r1 verified the results with its own reader and interval code, which is true.

### Issue 2: active-slack bound. OK, with one minor wording point
`scratch-B/check_powerflow.py` uses my own OSIL evaluator at 50 digits on open-instances-wave3/sol/<name>.p1.sol, with missing entries set to 0. It computes the slacks of all inequality rows:
- 0030p: active rows e208 (−5.5e-17), e300 (0) and e211 (1.625e-16), so the maximum is 1.625e-16 ≤ 1.7e-16. Next smallest: e215, 4.304e-4.
- 0039p: 14 active rows, all with slack exactly 0. Next smallest: e346, 1.082e-3.
- 0039r: e363 (x270 ≤ 5.64) has slack 6.8e-13 and e386 (x273 ≥ 1.4) has slack 2.1e-13. The maximum absolute active slack is 6.8e-13. Next smallest: e306, 2.293e-3.

All numbers in report.md:44 are correct. Minor: the sentence "In 0039r, e363 has slack 6.8e-13 and e386 has slack 2.1e-13, and the next smallest are 4.3e-4, 1.08e-3 and 2.3e-3" attaches the three per-instance "next smallest" values to 0039r. Suggested fix: split it, e.g. "... In 0039r, e363 has slack 6.8e-13 and e386 has 2.1e-13. The next smallest slacks are 4.3e-4 (0030p), 1.08e-3 (0039p) and 2.3e-3 (0039r)."

### Issue 3: incomplete p1 violations. OK
My evaluator finds the following in 0039r:
- bound violations: e362 (1·x269 ≤ 5.8) by 9.0e-14, e359 (x266 ≤ 6.52) by 4.0e-14 and e360 (x267 ≤ 5.08) by 3.0e-14;
- voltage rows (x_e² + x_f² ≤ 1.1236): e307 2.23e-14, e309 6.74e-14, e310 2.35e-14, e311 1.96e-14, e312 5.75e-14, e313 3.85e-14 and e315 5.39e-14. That is exactly seven rows. e308 has slack 0 and e314 is inactive (−7.7e-3).

The range "2.0e-14–6.7e-14" and the row names in report.md:30 are correct.

### Issue 4: external reader dependency. OK
- `research-20260929/reviews/open-instances-verification/osilx.py` exists. My sha256 is 4bcdc1d830bd3fc0392756f10b3e5daccbce218198543e402158a24cf986a465, which matches report.md:94 and the hash asserted in minor_review_check.py.
- The pfmodel.py diff is path-only, so I ignored it.

### Issue 5: summary primal displays. OK
I computed, in exact rationals, against the enclosure upper ends:
- 0039p: upper end 41869.0515113202038027683845. The old display 41869.0515113202 is 3.80e-12 too low. The new display 41869.0515113203 is the exact 10-decimal upward rounding (9.6e-11 above the upper end).
- 0039r: upper end 41869.0515113209830932768582. The old display 41869.0515113208 is 1.83e-10 too low. The new display 41869.0515113210 is the exact upward rounding at both 10 and 9 decimals (1.7e-11 above). It keeps the summary's 10-decimal format.
- Neither display can be shorter at the summary's precision.
- Relative gaps with the new displays: (display − dual)/dual = 6.3221e-10 and 6.6991e-10, so 6.3e-10 and 6.7e-10 still hold.

### Issue 6: uniqueness citation. OK, with a small note
- The argument in report.md:57 is stated correctly. F is C¹ on the convex box X, and F_i(x) − F_i(y) = ∇F_i(ξ_i)(x − y) with ξ_i ∈ X, so A ∈ J(X). Then 0 = C A(x − y), so x − y = (I − C A)(x − y), and ||I − C A||∞ ≤ ||I − C J(X)||∞ < 1 forces x = y. ||I − C A|| < 1 also makes C A, and therefore C, nonsingular. Existence is cited to Moore 1977, which matches the reviewer's remark that Moore 1977 proves existence.
- The check is real. minor_review_check.py builds I − C J(X) in mpmath iv from the interval Jacobian over the stored box, with float C entries converted exactly. It sums magnitudes exactly as Fractions and asserts that the norm is below 5.4e-12. The log gives 1.9295e-12, 2.8550e-12 and 5.3758e-12, matching the reviewer's own independent code (reviews/primal-powerflow-r1/run_*.log: 1.930e-12, 2.855e-12, 5.376e-12).
- Note (no fix required): minor_review_check.py recomputes C from the point Jacobian at mp.dps = 50, while certify.py uses mp.dps = 30. The two C matrices may therefore differ in the last bits, so the logged norm is, strictly, for a possibly different C than the one in the Krawczyk test. This does not matter for two reasons. First, the uniqueness argument works with any C. Second, certify.py's own logged max |K − c|/r (≤ 5.376e-12) already bounds ||I − C J(X)||∞ for its C, because X − c ⊇ [−r, r] is symmetric, so the half-width of K_i is at least r·Σ_t mag(M_it). If desired, add one clause: "certify.py's ratio max|K − c|/r also bounds this norm for the same C".
- Line 128 still lists Neumaier (1990), Ch. 5 as a general reference, and Krawczyk 1969 is listed but no longer cited in the body. Both are harmless.

### summary.md integration cells (rows 38-43): OK

## Lead's extra check: open-instances-summary.md primal displays against the exact points

| instance | summary primal | enclosure upper end of the exact point | valid upper bound? | gap column |
|---|---|---|---|---|
| dtoc5 (line 21) | 5.38967211918114 | 5.38967211918114046742396649913627... | **No**: 4.67e-16 below f(x*), and also below the certified dual's lower end 5.38967211918114046742396472... | "< 1e-14" still true (rigorous 4.675e-16) |
| lukvle10 (line 26) | 352.2380254064961 (p5's display) | 352.2380254064956226...979979 | yes, 4.77e-13 above (tight upward display would be 352.2380254064957) | 1.4e-9 holds (1.418e-9) |
| powerflow0030p (line 35) | 576.8934134704 | 576.8934134703742598676684 | yes; it is the exact 10-decimal upward rounding | 2.0e-9 rel holds (2.0309e-9) |
| powerflow0039p | 41869.0515113202 → 41869.0515113203 | see issue 5 | new: yes | 6.3e-10 holds |
| powerflow0039r | 41869.0515113208 → 41869.0515113210 | see issue 5 | new: yes | 6.7e-10 holds |

**Problem (minor; integration list incomplete):** reviews/minor-fixes/summary.md:12 says only the 0039p/0039r displays need upward values. The dtoc5 primal display 5.38967211918114 (open-instances-summary.md:21) equals the displayed dual. It lies below the exactly feasible point's value and even below the certified dual's lower end, so it is not an upper bound.
- Suggested fix: add to summary.md line 12 and row 29: "Use upward primal display 5.389672119181141 for dtoc5 (or 5.38967211918115 at 14 decimals)". The gap stays "< 1e-14" (rigorous 4.675e-16 against the summary dual).
- Optionally, tighten lukvle10 to 352.2380254064957, since x* now supersedes p5. The current value is valid, so this is not required.

## Collateral (diff of before/*.txt against the current reports)

dtoc5-lukvle10: I checked every hunk.
- Title: OK (trailing space only).
- Line 20: the p5 and KKT rewrite. All numbers verified; one ambiguity, noted above.
- Line 95: Numerical-only bullet. OK.
- Lines 100 and 123: the reviewer status is now "Independent review r1 rechecked ...", which is accurate. It is stated twice (caveats and open issues), which is harmless.
- Old open issue "report.md not written": removed correctly.
- Line 126: the dual-side open issue was made conditional. OK.
- Response table and targeted check: added.
- No numbers changed elsewhere, no deletions of content, and no broken links. `../../reviews/primal-dtoc5-lukvle10-review-r1.md` exists.
- Stale: line 127, as above (pre-existing, now inconsistent in tone with line 95).

powerflow: I checked every hunk.
- Status comment and line 3: OK.
- Line 30: violations verified.
- Line 44: slacks verified; wording point noted above.
- Line 57: uniqueness argument OK. The removed "Krawczyk 1969; Neumaier 1990, Ch. 5" citation is replaced; the references list keeps them.
- Line 94: osilx path and hash verified. "Reused unchanged" was dropped, which is fine.
- Open issues: the "not independently verified" line was replaced by the r1 statement, which is accurate. The new display sentence was verified.
- Response table and link (`../../reviews/primal-powerflow-review-r1.md` exists): OK.
- No unexplained number changes and no accidental deletions.
- Lines 34 and 112 ("unique solution") are now supported by the line-57 argument.

## Commands (all from the repository root unless a cd is shown; one process at a time, single-threaded)

- `cat .../minor-fixes-review-r1/BRIEF.md; ls -la` and `cat PROGRESS.json`; `ls` of reviews/minor-fixes, the two track dirs and the review dirs
- `cat reviews/primal-dtoc5-lukvle10-review-r1.md`; `cat reviews/primal-powerflow-review-r1.md`
- `grep -n -i -E "dtoc5|lukvle|powerflow" reviews/minor-fixes/summary.md`; the same grep on commands.md
- `diff -u reviews/minor-fixes/before/primal__dtoc5-lukvle10.txt primal/dtoc5-lukvle10/report.md`; `git show HEAD:.../dtoc5-lukvle10/report.md | diff -q - before/...` (identical)
- `diff -u reviews/minor-fixes/before/primal__powerflow.txt primal/powerflow/report.md`; the same HEAD comparison (identical)
- `cat -n` of both report.md files; `grep -n -i -E "dual side|global|optimal|local minim|second-order|entirely|600 digits|KKT point"` on the dtoc5 report; a repo-wide grep for "dual side|600 digits" mentioning lukvle10
- `git diff primal/dtoc5-lukvle10/gaps.py`; `cat gaps.py minor_review_check.py logs/minor_review_check.log` (dtoc5 track)
- `cat primal/powerflow/minor_review_check.py logs/minor_review_check.log`; `git diff pfmodel.py` (path-only); `grep`/`sed` on certify.py (C construction, mp.dps = 30 vs 50)
- Inline python3 ElementTree inspection of lukvle10.osil and the three powerflow OSIL files (tag counts, con/var attributes, objective)
- `head` of points/lukvle10_seed.txt, logs/lukvle10_kkt_x.txt, logs/gaps.json, the p5 and p1 .sol files
- `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 scratch-B/check_dtoc5_lukvle10.py > scratch-B/check_dtoc5_lukvle10.log` → exit 0, 35 s
- `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 scratch-B/check_powerflow.py > scratch-B/check_powerflow.log` → exit 0, 0.2 s. I ran it twice; the first run had a bug in my own upward-display helper, which I fixed in place before the final run.
- `grep` on reviews/primal-powerflow-r1/run_*.log (reviewer norms), reviews/primal-dtoc5-lukvle10-r1/logs/kkt_lukvle10.log (stationarity 10^-204.86) and the before-file (line 128 is pre-existing)
- `sed -n 15,50p research-20260929/open-instances-summary.md`

Not run: no main constructions, certify runs, solver campaigns or the authors' check scripts. I did not recompute the 1.4e-205 stationarity residual (a large least-squares solve); I took it from the r1 reviewer's log. No CI checks were inspected.
