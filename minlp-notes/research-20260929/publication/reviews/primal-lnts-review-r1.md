# Review of track primal-lnts (r1)

Verdict: verified. Written to disk by the root from the reviewer's structured return value (the harness blocks subagents from writing report files).

## Summary

# Review of track primal-lnts (round 1): exactly feasible points for lnts50/100/200/400

**Verdict: verified.** I found no blocker or major issue, and 5 minor issues (listed below). For each instance, my own code confirms that the stored box (exact decimal centre ± radius) contains exactly one zero of the reduced 3×3 system. It also confirms that the resulting point is exactly feasible for the cached OSIL model, that its objective lies inside the author's 25-digit enclosure, and that the gaps are as reported. The existence proof was checked twice:
- with mpmath interval arithmetic at 120 digits;
- with no mpmath at all, using only exact integer and Fraction arithmetic plus the alternating-series remainder bound for sin and cos.

## What I checked, and how
All code is mine; nothing was imported or copied from the track. It is in `/workspace/minlp-notes/research-20260929/publication/reviews/primal-lnts-r1/`:
- `verify_lnts_points.py`
- `verify_no_mpmath.py`
- `sanity_checks.py`
- `compare_author_Z.py`

From the track I used only the point files: the controls, the box centre and radius, the stored enclosures, and the stored objective enclosure.

1. **Model.** My OSiL reader applies the OSiL defaults (var lb=0, ub=INF, type C) and rejects unknown attributes and node types. The OSIL sha256 hashes match the ones recorded in the point files. The structure matches the author's description:
   - θ_0..θ_N with bounds ±1.5707963267949;
   - h at index 5N+5, with bounds [0, INF);
   - px_0 = py_0 = vx_0 = vy_0 = vy_N = 0, py_N = 5, vx_N = 45 (several of these come from `ub="0"` plus the default lb=0);
   - objective N·h;
   - no integer variables;
   - every constant except ±1.5707963267949 is exact in binary.
2. **Construction, re-derived generically.** My code assumes no index layout. It repeatedly solves any row that has exactly one undetermined variable appearing only linearly. For lnts50/100/200/400 this:
   - solves 197/397/797/1597 rows, each for one variable with coefficient 1;
   - leaves exactly 3 residual rows (for lnts50: e151 = end of the vx chain, e201 = end of the vy chain, e101 = end of the py chain) in the 3 unknowns (θ_0, θ_N, h).

   So the exact block elimination to a 3×3 system is confirmed.
3. **Existence.** I ran my own Krawczyk test with my own forward-mode interval derivatives on the author's exact boxes. It passes for all four instances, in both the mpmath version and the mpmath-free version. The zero lies strictly inside each exact decimal box. My Jacobian matches central finite differences to between 1.8e-75 and 2.9e-77 relative (numerical check only).
4. **Bounds, rows and stored enclosures.**
   - Every variable meets its bounds over the full box, checked against both the exact decimal value and the double value of each bound string. |θ| ≤ 0.9523, and h > 0.
   - Every one of the 4N rows contains 0 over the box. This is only a consistency check; exactness follows from the construction.
   - The author's stored 60-digit per-variable enclosures and 25-digit objective enclosures contain mine.
5. **Mutation tests.** My checker rejects each of these changes: control x2 + 1e-45; h centre + 2 radii; OSIL constant 100 → 100 + 1e-40; fixed value 45 → 45 + 1e-40. It accepts the unchanged input.
6. **Reproducibility.** I re-ran the author's `lnts_primal.py` on a copy in /tmp. It reproduces all four point files byte for byte, and the log JSON is identical except for timings.
7. **Earlier vectors.** The author's claim holds. The maximum differences from the new points are 3.25e-15, 3.45e-15, 3.54e-15 and 3.54e-15. All coordinates except one equal the new value rounded to double; the exception is the middle control (old value 0.0, new value about 1e-112).
8. **"No fully rational point".** This claim is true. In a rational point every θ_j is rational, and feasibility needs Σ w_j cos θ_j = 45/(100h), a rational number, with all w_j > 0. By Lindemann–Weierstrass, e^{iα} for distinct algebraic α are linearly independent over the algebraic numbers. Grouping equal |θ_j|, the coefficient of e^{i|θ|} for each |θ| > 0 is a positive sum, so every θ_j must be 0. But then py_N = 0 ≠ 5. (The author's own argument was cut off in the text I received.)

## My results
All objective values below are upper ends; they agree with the lower ends to 30 digits. Gaps are exact upper end minus dual, with relative values in brackets.

| instance | my one-step z* box widths (θ_0, θ_N, h) | my objective enclosure (width) | gap to summary dual | gap to verifier dual |
|---|---|---|---|---|
| lnts50 | 6.6e-99, 7.2e-99, 1.4e-102 | 0.554668764938678898622092233973 (7.2e-101) | 5.78898622092234e-13 (1.0437e-12) | 5.54698622092234e-13 (1.00005e-12) |
| lnts100 | 4.6e-98, 4.7e-98, 2.6e-102 | 0.554595401166911161001782873904 (2.6e-100) | 6.11161001782874e-13 (1.10199e-12) | 5.54561001782874e-13 (9.99938e-13) |
| lnts200 | 3.6e-97, 3.6e-97, 5.0e-102 | 0.554577016103083672055625292604 (1.0e-99) | 5.83672055625293e-13 (1.05246e-12) | 5.54572055625293e-13 (9.99991e-13) |
| lnts400 | 2.8e-96, 2.8e-96, 9.9e-102 | 0.554572413700687108817391133151 (4.0e-99) | 5.87108817391133e-13 (1.05867e-12) | 5.54608817391133e-13 (1.00007e-12) |

The author's gaps are rounded up to 20 decimals. Each is at or above my exact value and within 1e-20 of it. The summary's displayed duals (0.5546687649381 etc.) and the verifier duals (0.5546687649381242 etc., margin 1e-12) match open-instances-summary.md and reviews/open-instances-verification/verification-report.md.

## Issues (all minor)
1. **Invalid second Krawczyk step.** In `lnts_primal.py`, `K2 = krawczyk(thfix_iv, Y, Z)` uses y = the stored centre. The centre is about 2e-76 to 5e-76 from z*, far outside the step-1 box Z (1e-98 to 3e-96 wide). The mean-value argument therefore does not apply, and the author's code does not prove the stated widths ("less than 2.1e-106", objective "narrower than 3e-109").
   - The stated widths are nevertheless true: my valid two-step enclosure lies inside the author's final Z for all four instances.
   - The 25-digit enclosures and the gaps do not depend on this step.
   - Fix: use a point of Z as y in step 2, or report the one-step widths.
2. **report.md is missing on disk**, and the report text I received was cut off. The integration step must write report.md, including the commands run.
3. **The old-vector comparison code is not saved** in the track folder. I confirmed the claim with my own code.
4. **Relative gaps are rounded up to 3 significant digits without saying so** (1.0437e-12 is shown as 1.05e-12). This is valid, but the report should state it.
5. **Cosmetic:** the middle control is stored as about 1e-112 instead of 0.

## Status of each claim
- **Proved by my code**, assuming exact Python integer and Fraction arithmetic and the Taylor remainder bound: an exactly feasible point exists in each stored box, its objective enclosure is as reported, and the gaps against both dual values are as reported.
- **Taken as given, not re-proved here:** the dual bounds themselves, which come from the earlier verified certificate. The remaining gap of about 5.5e-13 comes from that certificate's 1e-12 margin.
- **Numerical evidence only:** the Jacobian versus finite-difference comparison, and the Newton-produced centres.
- **Not done:** an independent interval library such as python-flint/Arb, which is not installed. I did not install packages on the shared machine.

No jobs from this track are running. I used 1 core.

## Issues

- **minor**: The second Krawczyk step in lnts_primal.py, `K2 = krawczyk(thfix_iv, Y, Z)`, is invalid as coded. It uses y = the stored box centre, but the centre is not in Z: |centre - z*| is about 2e-76 to 5e-76, while the step-1 box Z = K(X) n X is only 1e-98 to 3e-96 wide. The argument that the Krawczyk operator keeps every zero needs y in Z, or a Jacobian over hull(Z and y). So the author's code does not prove the stated widths ('box less than 2.1e-106 wide', 'objective enclosure narrower than 3e-109'). Impact on results: none. My valid second step (y = a point inside Z) gives an enclosure that lies inside the author's final Z for all four instances, so those widths are true. The one-step enclosure alone already gives the same 25-digit objective intervals and the same gaps. Fix: in step 2, use a point of Z (e.g. its midpoint) as y, or report the one-step widths (objective width at most 4e-99).
- **minor**: report.md does not exist on disk (the harness blocked it). The report text passed to me was cut off mid-sentence ('With θ rational and n...'), so I could not review the rest: the argument that no fully rational point exists, and any command list. The claim itself is true (my proof is in the summary). The integration step must write report.md and include the commands: `python3 lnts_primal.py 50 100 200 400 > logs/run_all.stdout`, crosscheck.py, jacobian_check.py, mutation_test.py, and the old-vector comparison.
- **minor**: The code behind logs/compare_old_points.stdout (the comparison with the earlier double-precision vectors) is not saved in the track folder, so that log cannot be reproduced from the folder. I redid the comparison with my own code and confirmed the claim: max differences 3.25e-15, 3.45e-15, 3.54e-15, 3.54e-15; the only differing coordinate is the middle control.
- **minor**: The results table rounds relative gaps up to 3 significant digits but does not say so. For example, 1.0437e-12 is shown as 1.05e-12, 1.0001e-12 as 1.01e-12, and the 5.79e-13 to 6.11e-13 range as '5.8e-13 to 6.2e-13'. Rounding up is valid, but the report should state it, because readers expect round-to-nearest.
- **minor**: Cosmetic: the middle control (x26, x51, x101, x201) is stored as a tiny nonzero decimal (e.g. -3.839e-112 for lnts50) instead of 0. It is the 40-significant-digit rounding of Newton noise around the symmetric value 0. It is harmless (exactly rational and within bounds) and is the one coordinate that differs from the earlier double vectors. Storing 0 would be cleaner.

## Commands run

- `ls -la publication/primal/lnts/ publication/primal/lnts/points/ publication/reviews/ (reviews/ did not exist)`
- `cat lnts_primal.py osil_iv.py crosscheck.py jacobian_check.py mutation_test.py; head of every file in logs/`
- `python3 inline: inspect structure of points/lnts50_point.json`
- `ls -la and sha256sum ~/.cache/minlplib/minlplib/osil/lnts{50,100,200,400}.osil (hashes match the point files); python3 inline regex dump of OSIL sections and variable-bound patterns`
- `grep lnts in open-instances-summary.md and reviews/open-instances-verification/verification-report.md; sed to read the lnts sections (dual values confirmed)`
- `mkdir publication/reviews/primal-lnts-r1; head of open-instances/logs/lnts_lnts50_primal.txt; nproc; uptime`
- `python3 verify_lnts_points.py 50 (first run, rc 0; output superseded)`
- `python3 verify_lnts_points.py 50 100 200 400 > verify_run.stdout (rc 0, 8.3 s): Krawczyk passes on all stored boxes; all bounds, rows, stored enclosures and objective enclosures confirmed; centre_in_Z1 = False for all four`
- `python3 sanity_checks.py > sanity_checks.stdout (rc 0, 10 s): Jacobian vs finite differences 1.8e-75 to 2.9e-77 relative; all 4 mutations rejected, unchanged input accepted; old-vector max differences 3.25e-15 to 3.54e-15, all coordinates but the middle control equal to double rounding`
- `cp lnts_primal.py osil_iv.py to /tmp/lnts_repro_r1; python3 lnts_primal.py 50 100 200 400 (rc 0, 6.9 s); cmp of the 4 point files: identical; log JSON equal except timings`
- `/tmp copy patched to dump Z: python3 lnts_primal_dumpZ.py 50 100 200 400 (rc 0)`
- `python3 compare_author_Z.py | tee compare_author_Z.stdout (rc 0): centre outside the author's step-1 box; my valid Z2 inside the author's final Z for all 4`
- `ps -eo pid,etime,args | grep lnts_primal|crosscheck|... (no running jobs); rm -rf /tmp/lnts_repro_r1`
- `python3 -c 'import flint' (not installed); pip list | grep flint/arb (none)`
- `python3 inline: unit test of my Taylor sin/cos enclosures against mpmath at 140 digits (all contain the reference)`
- `python3 verify_no_mpmath.py 50 (rc 0, 8 s)`
- `python3 verify_no_mpmath.py 50 100 200 400 > verify_no_mpmath.stdout (rc 0, 113 s): Krawczyk passes without mpmath; objective enclosures inside the stored 25-digit intervals; same gaps`
- `python3 -c: full-precision zero_enclosure_widths and obj_width from the author's log (max 2.097e-106 and 2.18e-109)`
