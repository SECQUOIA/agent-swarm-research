# Review of track primal-powerflow (r1)

Verdict: verified. Written to disk by the root from the reviewer's structured return value (the harness blocks subagents from writing report files).

## Summary

I found no errors in the proofs. All three exactly feasible points (powerflow0030p, powerflow0039p, powerflow0039r) and their objective enclosures and gaps are reproduced by my own code. I found 6 minor issues and no blocker or major issue. The track's only missing deliverable is report.md, which the harness blocked. My check code and logs are in /workspace/minlp-notes/research-20260929/publication/reviews/primal-powerflow-r1/ (verify.py, osil_read.py, dyiv.py, plus helper scripts and the run_*.log files). This session's instructions forbid writing review .md files, so the review below should be written to publication/reviews/primal-powerflow-r1.md by the integration step.

# Review: track primal-powerflow, round 1

## Verdict
Verified. Each of the three point files proves that an exactly feasible point of the cached OSIL model exists. I re-derived every claim with my own code, which does not use mpmath, osilx, pfmodel or any of the author's scripts. My numbers agree with the author's to every printed digit.

## What I checked, and how
1. **Model.**
   - I wrote my own OSIL reader, osil_read.py. It uses xml.etree, keeps every coefficient as an exact Fraction and handles the mult/incr compression.
   - The three cached files are byte-identical (same md5) to the copies at www.minlplib.org/osil, fetched 2026-10-01.
   - sha256 of the cached files: 0030p 5c4b386b..., 0039p 0a27073f..., 0039r d8ba3132...
   - All variables are continuous with bounds (-inf, +inf), so there are no variable bounds and no integrality. The objective is min, weight 1, quadratic, with no nl part. My code asserts all of this.
2. **Arithmetic.** I wrote my own outward-rounded interval arithmetic, dyiv.py: dyadic numbers at 2^-320, exact Python integers, floor for lower ends and ceil for upper ends.
   - sin and cos use the Taylor series at the midpoint with the Lagrange remainder bound, then widen by the half-width (valid because |sin'| <= 1).
   - The proof assumes that Python integer arithmetic is exact and that my code is correct.
   - As evidence for the code: 0 failures against 200-digit mpmath on 308 points, and 2000 random products and divisions passed.
3. **Krawczyk test.**
   - Setting: the square system S from the point file, the fixed variables at their exact rationals, and the box X = [c - 1e-45, c + 1e-45] around the stored 60-digit centre c.
   - I used my own preconditioner C, the float64 inverse of the midpoint of my J(X). It differs from the author's C.
   - Every component satisfies K_i - c_i in (-r, r).
   - max |K - c|/r is 1.930e-12, 2.859e-12 and 5.376e-12 for 0030p, 0039p and 0039r.
   - ||I - C J(X)||_inf <= 1.930e-12, 2.855e-12 and 5.376e-12. This gives existence (Brouwer applied to x -> x - C F(x)), uniqueness (contraction) and nonsingularity of C.
   - The 0030p run at radius 1e-30 also passes.
4. **Every row.**
   - Rows in S hold with equality at their side, and I checked that each side lies within the row's bounds.
   - Every equality row is either in S or has all its variables fixed and is checked exactly.
   - Every other row has an interval enclosure over X strictly inside its bounds.
   - Counts (S / exact / interval):
     - 0030p: 222 / 25 / 308. The author has 23 / 310 because e183 and e235 are quadratic rows on fixed variables only; I check them exactly, the author by intervals. Both are valid.
     - 0039p: 262 / 39 / 356.
     - 0039r: 270 / 23 / 180.
   - The smallest margins match the author's: 4.3038e-4 at e215, 1.0821e-3 at e346 and 2.2929e-3 at e306.
5. **Objective enclosures**, identical to the author's at 22 decimals:
   - 0030p: [576.8934134703742598676683, 576.8934134703742598676684].
   - 0039p: [41869.0515113202038027683844, ...845].
   - 0039r: [41869.0515113209830932768581, ...582].
6. **Gaps**, computed in exact rationals from the summary's duals (576.8934122988004, 41869.05148485014, 41869.05148327243):
   - 0030p: <= 1.171573860e-6 (2.030833e-9 relative).
   - 0039p: <= 2.6470063803e-5 (6.32211e-10 relative).
   - 0039r: <= 2.8048553094e-5 (6.69912e-10 relative).

   Each dual lies below its enclosure. Earlier reviews (reviews/closing-confirm-r2.md, reviews/powerflow0039-review.md) record that the displayed duals are at most the exact certified values. I did not re-verify the duals; that is outside this track.
7. **Negative controls.** My verifier rejects five damaged point files:
   - a centre moved by 1e-44;
   - x29 moved 1e-30 above its bound;
   - one row removed from S;
   - e208 taken at its missing lower side;
   - a radius of 1e-3.
8. **Comparison with p1 (evidence).** All of the author's p1 numbers match:
   - row violations 2.125e-13, 1.182e-12 and 7.906e-12;
   - objective of our point minus obj(p1): 2.873e-12, 4.643e-12 and 1.826e-10;
   - moves of the free variables from p1: 1.42e-14, 2.53e-13 and 7.78e-12.

   With my reader, p1 violates no row by more than 7.9e-12. Since p1 comes from MINLPLib's solution files, independent of both readers, this is evidence that the OSIL is read correctly.
9. **SCIP cross-check (evidence only, floating point).** I fixed every model variable at the double-rounded point values in SCIP's own OSIL reader, with feastol 1e-9 and one thread. SCIP reports all three problems feasible ("optimal"), with objectives 576.8934134703743, 41869.0515113202 and 41869.05151132099.

The report states plainly what is proved (certify.py) and what is only numerical (construct.py, scip_check.py).

## Issues (all minor)
See the issues list:
- report.md is missing, and the copy of its text I received is cut off, so I could not check its command list;
- the statement that active slacks are at most 1e-13 is false for 0039r;
- the list of p1's violations in 0039r is incomplete;
- certify.py depends on osilx.py in another folder;
- the summary's primal values need updating at integration;
- the Neumaier citation has no theorem number.

## Commands I ran (in publication/reviews/primal-powerflow-r1, with OPENBLAS/OMP/MKL_NUM_THREADS=1 except the first run)
- python3 test_dyiv.py -> 0 failures.
- python3 verify.py powerflow0030p | powerflow0039p | powerflow0039r -> all PASS, about 0.5 s each (run_*.log).
- python3 verify.py powerflow0030p 1e-30 -> PASS.
- python3 negative_controls.py -> all 5 rejected.
- python3 p1_slacks.py powerflow0030p powerflow0039p powerflow0039r -> active sets and slacks.
- python3 scip_fix.py powerflow0030p powerflow0039p powerflow0039r -> all three feasible.
- curl of the three OSIL files from www.minlplib.org/osil, 1 s apart, plus md5sum -> identical to the cached files.
- sha256sum of the OSIL files, the point files and osilx.py.
- Web searches to check the bibliographic data for Krawczyk 1969 and Moore 1977.

Core budget: my first verify.py run on 0030p let numpy's BLAS use about 18 threads for about 2.5 s, which briefly exceeded the 2-core budget. All later runs used 1 thread. No background jobs were started.

## Issues

- **minor**: The deliverable /workspace/minlp-notes/research-20260929/publication/primal/powerflow/report.md does not exist because the harness blocked the Write call. The report text exists only in the author's returned summary. The copy I was given is cut off in the SCIP paragraph, so I could not check the report's command list or its assumptions section. The logs in logs/ do not record command lines. When the integration step writes report.md, it should list the commands for each of the three instances: python3 construct.py <name>; python3 certify.py <name>; python3 certify.py <name> 1e-30 (logs/certify_r1e-30.*); python3 scip_check.py <name>. It should also state the assumption about mpmath iv.
- **minor**: The report says that active slacks at p1 are at most 1e-13. This is false for powerflow0039r. At p1, x270 <= 5.64 (row e363) has slack 6.8e-13 and x273 >= 1.4 (row e386) has slack 2.1e-13. The proof is not affected, because both variables are fixed exactly at their bounds and certify.py checks every row.
- **minor**: The report says that for 0039r p1 violated x269 <= 5.8 by 9e-14. That list is incomplete. p1 also violates x266 <= 6.52 (e359) by 4.0e-14 and x267 <= 5.08 (e360) by 3.0e-14. It also violates the voltage rows e307, e309, e310, e311, e312, e313 and e315 (e^2 + f^2 <= 1.1236) by 2.0e-14 to 6.7e-14. This matters only for the comparison with p1.
- **minor**: The author's proof script certify.py (through pfmodel.py) imports the OSIL reader osilx.py from another folder: research-20260929/reviews/open-instances-verification/osilx.py, sha256 4bcdc1d830bd3fc0392756f10b3e5daccbce218198543e402158a24cf986a465. If that file changes, the track's proof cannot be reproduced. The report should record this hash, or the track should keep its own copy of the reader. My independent reader gives the same model.
- **minor**: Note for the integration step on open-instances-summary.md. (1) For 0039r, the primal column shows 41869.0515113208, which is obj(p1). That is below the value of the new exactly feasible point, 41869.05151132098309... Replace it with an upward-rounded value such as 41869.0515113210. (2) For 0039p, the shown 41869.0515113202 is 3.8e-12 below the exact enclosure 41869.05151132020380... If primal values are meant to be valid upper bounds, round it up to 41869.0515113203. (3) Remove powerflow0030p/0039p/0039r from the sentence that says no exactly feasible point was constructed (lines 44-47). The gaps (2.0e-9, 6.3e-10, 6.7e-10 relative) are unchanged.
- **minor**: The report cites the Krawczyk-Moore theorem as Neumaier 1990, Ch. 5, without a theorem number. I confirmed the bibliographic data for Krawczyk 1969 (Computing 4(3):187-201) and Moore 1977 (SIAM J. Numer. Anal. 14:611-615). I could not access Neumaier's book. Moore 1977 proves existence only; uniqueness under K(X) in int(X) comes from later work. Give the exact theorem. Alternatively, note that the computation also shows ||I - C J(X)||_inf < 1, about 5.4e-12 or less, which gives uniqueness and nonsingularity of C directly.

## Commands run

- `python3 test_dyiv.py (reviewer interval sin/cos/mul tests vs 200-digit mpmath): 0 failures over 308 points, 2000 random products OK`
- `python3 verify.py powerflow0030p (first run, multithreaded BLAS ~18 threads for ~2.5 s): PASS`
- `OPENBLAS_NUM_THREADS=1 python3 verify.py powerflow0030p / powerflow0039p / powerflow0039r: all PASS; Krawczyk ratios 1.930e-12, 2.859e-12, 5.376e-12; enclosures and gaps identical to the author's`
- `OPENBLAS_NUM_THREADS=1 python3 verify.py powerflow0030p 1e-30: PASS`
- `python3 negative_controls.py: all 5 damaged point files rejected`
- `python3 p1_slacks.py powerflow0030p powerflow0039p powerflow0039r: active sets; 0039r active slacks up to 6.8e-13; p1 violates x266, x267, x269 bounds and voltage rows e307, e309-e313, e315 by 2e-14 to 9e-14`
- `python3 scip_fix.py powerflow0030p powerflow0039p powerflow0039r: SCIP (1 thread, feastol 1e-9) reports all three fixed problems feasible; objectives 576.8934134703743, 41869.0515113202, 41869.05151132099`
- `curl -s https://www.minlplib.org/osil/<name>.osil (3 files, 1 s apart) + md5sum: identical to the cached OSIL files`
- `sha256sum of the cached OSIL files, the point JSON files and reviews/open-instances-verification/osilx.py`
- `WebSearch/WebFetch: bibliographic check of Krawczyk 1969 (Computing 4:187-201) and Moore 1977 (SIAM J. Numer. Anal. 14:611-615); Neumaier 1990 Ch. 5 not accessible`
