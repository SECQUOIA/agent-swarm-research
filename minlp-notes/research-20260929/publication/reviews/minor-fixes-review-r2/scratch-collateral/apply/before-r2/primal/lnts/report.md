<!-- Written to disk by the root from the structured return value of agent 'author:primal-lnts' (the harness blocks subagents from writing report files). Status: complete. -->

# Exactly feasible primal points for lnts50, lnts100, lnts200, lnts400 (track primal-lnts, 2026-10-01)

## 1. Result
All four instances are done. For each instance there is a point x* of the cached OSIL model (`~/.cache/minlplib/minlplib/osil/lnts<N>.osil`). Under the assumptions below, x* is proved to satisfy every row and every variable bound exactly. The models have no integer variables. Three coordinates come from an interval existence proof (Krawczyk test, outward-rounded mpmath interval arithmetic at 110 digits). The other coordinates are either exact rationals or are defined exactly by the model's own recursion. The objective N*h of x* is enclosed in an interval narrower than 3e-109. Each gap is the upper end of that enclosure minus our dual bound, computed exactly with Fractions and rounded up. The displayed absolute and relative gaps are rounded upward to three significant digits.

| instance | vars/rows | point file | objective enclosure of x* | gap to summary dual (rel.) | gap to verifier dual (rel.) |
|---|---|---|---|---|---|
| lnts50 | 256/200 | points/lnts50_point.json | [0.5546687649386788986220922, 0.5546687649386788986220923] | 5.79e-13 (1.05e-12) | 5.55e-13 (1.01e-12) |
| lnts100 | 506/400 | points/lnts100_point.json | [0.5545954011669111610017828, 0.5545954011669111610017829] | 6.12e-13 (1.11e-12) | 5.55e-13 (1.01e-12) |
| lnts200 | 1006/800 | points/lnts200_point.json | [0.5545770161030836720556252, 0.5545770161030836720556253] | 5.84e-13 (1.06e-12) | 5.55e-13 (1.01e-12) |
| lnts400 | 2006/1600 | points/lnts400_point.json | [0.5545724137006871088173911, 0.5545724137006871088173912] | 5.88e-13 (1.06e-12) | 5.55e-13 (1.01e-12) |

The two dual bounds:
- **Summary dual:** the truncated value displayed in open-instances-summary.md (0.5546687649381, 0.5545954011663, 0.5545770161025, 0.5545724137001).
- **Verifier dual:** certified N·h2 at margin 1e-12, shown here rounded down as 0.5546687649381242, 0.5545954011663565, 0.5545770161025290 and 0.5545724137001325. The older review displays for lnts100 and lnts200 were rounded to nearest and lie above N·h2; they are not lower bounds as displayed.

Against the certified verifier dual, each gap is at most 5.55e-13. Against the summary dual displays, the per-instance upper bounds are 5.79e-13, 6.12e-13, 5.84e-13 and 5.88e-13. The summary's 5.5e-13 is rounded to nearest and must be corrected.

The remaining gap comes entirely from the dual certificate's relative margin of 1e-12 (h2 = h*(1-1e-12)). The primal side adds less than 3e-109. A dual certificate with a smaller margin would shrink the gap. I did not compute one, because the dual side is outside this track.

The middle fixed control is a small exact rational (about 1e-112), inherited from rounding a numerical tangent-law solve. It is part of the stored point definition. Replacing it with zero would define a different point and require new enclosures, so it is retained. Its size does not affect the displayed objective or gaps.

The new points agree with the earlier tolerance-feasible vectors (open-instances/logs/lnts_lnts<N>_primal.txt) to within 3.6e-15 in every coordinate. In each earlier vector, all coordinates but one equal the new value rounded to double.

## 2. Model (asserted from the OSIL by exact string comparison in `check_structure`)
- **Variables:** θ_0..θ_N at indices 0..N, with bounds [-1.5707963267949, 1.5707963267949]. Then px, py, vx, vy (N+1 each). Then h at index 5N+5, with bounds [0, INF).
- **Fixed values:** px_0 = py_0 = vx_0 = vy_0 = vy_N = 0, py_N = 5, vx_N = 45.
- **Other variables:** all other states are free, and all variables are continuous.
- **Objective:** min N*h, with no constant.
- **Rows** (i = 0..N-1, lb = ub = 0):
  - p_{i+1} - p_i - .5 v_i h - .5 v_{i+1} h, for (p,v) = (px,vx) and (py,vy);
  - v_{i+1} - v_i + (100 f(θ_i) + 100 f(θ_{i+1}))(-.5) h, for (v,f) = (vx,cos) and (vy,sin).
- **Bound check:** every constant is exact in binary except ±1.5707963267949. The bound checks use the tighter of its exact decimal value and its double value. In every point, |θ| ≤ 0.953.

## 3. Construction and proof
1. **Fixed controls.** θ_1..θ_{N-1} are fixed at 40-digit decimal rationals that round the linear-tangent law (tan θ_j = μ + ν c_j/w_j) at the optimum.
2. **States.** Each row is linear in its "next" state with coefficient 1, so it can be solved for that state:
   - v_{i+1} = v_i + 50 h (f(θ_i) + f(θ_{i+1}));
   - p_{i+1} = p_i + h (v_i + v_{i+1})/2;
   - starting from px_0 = py_0 = vx_0 = vy_0 = 0.

   For any (θ, h), this recursion defines the free states uniquely, and all 4N rows hold exactly. The last rows also hold with the fixed values vx_N = 45, vy_N = 0, py_N = 5 if and only if F(z) := (vx_N(z) - 45, vy_N(z), py_N(z) - 5) = 0, where z = (θ_0, θ_N, h). px_N is free. This is an exact block elimination of the chain: a 4N×4N square subsystem reduces to a 3×3 system.
3. **Krawczyk test.** X is the outward-rounded box with the stored 75-digit centre and radius 1e-50 (θ_0, θ_N) and 1e-52 (h). The test computes K(X) = y - C F(y) + (I - C F'(X))(X - y), where:
   - F'(X) comes from forward-mode differentiation of the recursion over X in iv arithmetic;
   - C is the inverse of the midpoint of F'(X), used as exact numbers.

   For all four instances, K(X) ⊂ int X. So there is exactly one zero z* in X. For a second Krawczyk step, y is reset to a point at the midpoint of the step-1 box Z. The original stored centre is outside Z and cannot be reused in that step. The valid two-step enclosure is less than 2.1e-106 wide and lies strictly inside the exact decimal box centre ± radius. The check on all four stored boxes is saved in `logs/minor_review_check.log`; it also confirms the objective width below 3e-109 without regenerating the points.
4. **The point.** x* consists of the rational controls, z*, the recursion states, and the fixed values. All rows hold exactly. Bounds: θ_0 and θ_N are checked over the box, the rational controls are checked exactly with Fractions, h > 0, and all other variables are free or fixed exactly.
5. **Objective.** N*h with h in the final box, computed exactly from the binary end points. Gaps use exact Fractions and are rounded up.

**Proved** (assuming mpmath 1.3.0 iv encloses +, -, *, /, cos, sin correctly with outward rounding, and that the OSIL is read correctly): x* is exactly feasible, and its objective lies in the stated enclosure. The dual bounds themselves are the earlier, independently verified result and are not re-proved here.

**Numerical only:** the tangent-law solve, the Newton solve for the centre, and the choice of C.

**No fully rational point exists.** If all θ_j and h were rational, vx_N = 45 would require Σ w_j cos θ_j = 45/(50h) to be rational, with h > 0 and positive weights w_j. Lindemann–Weierstrass makes e^{iα} for distinct algebraic α linearly independent over the algebraic numbers. After grouping equal |θ_j|, every nonzero angle gives a strictly positive coefficient of e^{i|θ_j|}, so rationality forces every θ_j = 0. Then py_N = 0, contradicting py_N = 5. This is the linear-independence argument in independent review r1, item 8. Our construction uses an interval existence proof.

## 4. Checks (my own code; none of them is an independent review)
- **Generic row check** in lnts_primal.py. Every OSIL row is evaluated from the parsed XML trees over the full-variable box, and each enclosure contains 0. The widest is 7.7e-107. A generic check of all bounds also passes. This is a consistency check, not the proof.
- **crosscheck.py**, a second script that differs in three ways:
  - it reads the OSIL with the verifier's osilx.py reader;
  - it computes F and F' from the closed-form sums with hand-written derivatives (the sums are first checked against the exact rational recursion on all N+1 unit vectors and on one rational point with h = 3/7);
  - it reruns the Krawczyk test on the stored decimal box.

  All four pass, and K lies inside the exact box. Every row and bound is also re-evaluated over the stored 60-digit enclosures: every row contains 0 (width ≤ 1.03e-58). The objective enclosures agree.
- **jacobian_check.py** (numerical). A wrong Jacobian would not make the Krawczyk test fail when F(centre) is tiny, so this compares three Jacobians at the centre. Forward-mode vs closed form differ by at most 7.6e-111 (relative). Forward-mode vs central finite differences (step 1e-30) differ by at most 1.9e-65. |F(centre)| ≤ 1.7e-73.
- **mutation_test.py.** crosscheck.py correctly rejects three altered lnts50 files and accepts the unaltered copy:
  - control x2 changed by +1e-45: Krawczyk fails;
  - h centre moved by +2 radii: Krawczyk fails;
  - state enclosure shifted by +1e-55: the row check fails.

## 5. Point file format (points/lnts<N>_point.json)
- osil path and sha256;
- fixed_controls: θ_1..θ_{N-1}, i.e. x2..xN, as exact decimals;
- unknowns_box: centre (exact decimal) and radius for θ_0 (x1), θ_N (x<N+1>) and h (x<5N+7>). z* is the unique zero of F in this box;
- fixed_variables;
- enclosures: [lo, hi] for every variable in OSIL order, as 60-digit outward decimals;
- objective_enclosure: 25-digit outward decimals;
- description: how x* is defined from these data.

## 6. Notes for integration
- lnts50–400 can leave the summary's list of instances closed only against points with row violations. Their primal values are now values of exactly feasible points, with the enclosures above. The summary primal displays for lnts50, lnts200 and lnts400 are valid upper bounds. For lnts100, replace 0.5545954011669 by 0.5545954011670: the old display lies below the exact point objective.
- The gap to the certified verifier dual is at most 5.55e-13 and is set by the dual margin. Against the summary dual displays, use the four upper bounds in Section 1.

## 7. Files (all in /workspace/minlp-notes/research-20260929/publication/primal/lnts/)
- lnts_primal.py: proof and point files
- osil_iv.py: own OSIL reader and interval row evaluator
- crosscheck.py
- jacobian_check.py
- mutation_test.py
- minor_review_check.py and logs/minor_review_check.log: valid second-step and old-vector checks
- points/lnts{50,100,200,400}_point.json
- logs/: run_all.stdout, lnts_primal_50_100_200_400.json, crosscheck.stdout, crosscheck_50_100_200_400.json, jacobian_check.stdout, jacobian_check_50_100_200_400.json, mutation_test.stdout, compare_old_points.stdout

The historical `logs/run_all.stdout` and `logs/lnts_primal_50_100_200_400.json` predate the second-step centre correction; their contraction widths are obsolete. Use `logs/minor_review_check.log` for current widths. The reviewer reran the corrected construction in `../../reviews/minor-fixes-review-r1/scratch-A/lnts_repro/`; a round-2 byte comparison confirms that all four resulting point files equal the stored files. No construction was rerun in round 2.

## Commands run (from the agent's structured return)

- `python3 -c '<mpmath iv API tests: interval conversion of big ints/strings, endpoint access>' (in /tmp; exploration only)`
- `python3 -c '<inspect lnts50.osil: variables, objective, linear/quadratic/nonlinear sections, tag set>' (exploration only)`
- `cd OUTDIR && OMP_NUM_THREADS=1 python3 lnts_primal.py 50  -> passed (first trial; log superseded and deleted)`
- `cd OUTDIR && OMP_NUM_THREADS=1 python3 lnts_primal.py 50 100 200 400  -> all four Krawczyk tests pass; 0.4/0.7/1.7/5.2 s; logs/run_all.stdout, logs/lnts_primal_50_100_200_400.json, points/*.json`
- `cd OUTDIR && OMP_NUM_THREADS=1 python3 crosscheck.py 50 100 200 400  -> passed (run twice: before and after adding the exact-box check and decimal output); logs/crosscheck.stdout, logs/crosscheck_50_100_200_400.json`
- `cd OUTDIR && inline python mutation test (temporary mut/ folder, removed) -> 3 mutations rejected, unchanged copy accepted`
- `cd OUTDIR && OMP_NUM_THREADS=1 python3 mutation_test.py  -> all as expected; logs/mutation_test.stdout`
- `cd OUTDIR && OMP_NUM_THREADS=1 python3 jacobian_check.py 50 100 200 400  -> forward-mode vs closed form <= 7.6e-111 rel, vs finite differences <= 1.9e-65 rel; logs/jacobian_check.stdout`
- `cd OUTDIR && inline python comparison (now saved in minor_review_check.py) with open-instances/logs/lnts_lnts<N>_primal.txt (first float version was misleading at 5e-61 and was replaced by the exact version) -> max diff approximately 3.25e-15..3.54e-15; logs/compare_old_points.stdout`
- `cd OUTDIR && inline python computing rounded-up absolute/relative gaps from logs/lnts_primal_50_100_200_400.json`
- `rm -rf OUTDIR/__pycache__ ; git status --short (read-only)`

## Open issues (from the agent's structured return)

- The checks are by my own code: lnts_primal.py and a second script, crosscheck.py, that uses the verifier's OSIL reader and a closed-form Jacobian. These are author checks; independent review r1 subsequently verified the results, including an integer-only enclosure of sin and cos.
- The proof assumes that mpmath 1.3.0 interval arithmetic encloses +,-,*,/,cos,sin correctly with outward rounding.
- The remaining gap of at most 5.55e-13 (about 1e-12 relative) comes from the dual certificate's margin. A tighter dual at a smaller margin was not computed because it is outside this track.
- The summary dual displays give upper gaps 5.79e-13, 6.12e-13, 5.84e-13 and 5.88e-13. The 5.55e-13 upper bound applies to certified N·h2 and to the safe verifier displays above.

## Response to review

Review: `../../reviews/primal-lnts-review-r1.md`. Checked and resolved on 2026-10-03.

| issue | resolution and evidence |
|---|---|
| 1. Invalid second Krawczyk step | Changed only the second-step centre to a point in Z. Rechecked the two steps on all four stored boxes: widths < 2.1e-106, objective width < 3e-109; 25-digit objective displays unchanged. No construction rerun. |
| 2. Missing report | The full report is on disk with its commands and interval assumptions. Independent r1 evidence is acknowledged. |
| 3. Missing old-vector comparison script | Saved the comparison in `minor_review_check.py`; exact binary64 inputs and stored coordinate enclosures give distances approximately 3.25e-15–3.54e-15, all below 3.6e-15 and all but one matching rounding per instance. |
| 4. Conservative relative-gap rounding | Stated upward rounding to three significant digits in Section 1. |
| 5. Tiny middle control | Kept the stored exact rational to preserve the certified point; explained its numerical origin and checked |control| < 1e-110 for all four instances. |

Targeted check: `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 research-20260929/publication/primal/lnts/minor_review_check.py > research-20260929/publication/primal/lnts/logs/minor_review_check.log` (from the repository root). Results are in `logs/minor_review_check.log`. No main computation, solver campaign, project-wide verification or CI check was run for this revision.

### Round 2: independent minor-fixes review (2026-10-03)

Review: [minor-fixes-review-r1.md](../../reviews/minor-fixes-review-r1.md). Issue numbers below refer to that review.

| issue | resolution |
|---|---|
| 1 | Corrected the invalid lnts100 summary-display claim; recorded primal 0.5545954011670. |
| 8 | Rounded verifier dual displays downward; relative upper gaps to these safe displays are 1.01e-12 for all four instances. |
| 9 | Made upper-gap rounding consistent and labelled the coordinate-distance range approximate. |
| 10 | Supplied the linear-independence proof, labelled obsolete construction-width logs, checked reviewer rerun point bytes and completed the file list. |

Own exact checks and saved-source evidence: [check_r2.log](../../reviews/minor-fixes/check_r2.log). The full response is [response-r2.md](../../reviews/minor-fixes/response-r2.md); exact commands and results are in [commands.md](../../reviews/minor-fixes/commands.md). Integration edits remain pending in the main summary and audit report. No main computation or solver campaign was repeated.
