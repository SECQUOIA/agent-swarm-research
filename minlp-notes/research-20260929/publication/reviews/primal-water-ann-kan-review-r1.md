# Review of track primal-water-ann-kan (r1)

Verdict: verified. Written to disk by the root from the reviewer's structured return value (the harness blocks subagents from writing report files).

## Summary

# Review r1: track primal-water-ann-kan (exactly feasible primal points)

Reviewer: independent verifier, round 1. Date: 2026-10-01.
Author's folder: /workspace/minlp-notes/research-20260929/publication/primal/water-ann-kan
Reviewer's code and logs: /workspace/minlp-notes/research-20260929/publication/reviews/primal-water-ann-kan-r1/

## Verdict

**Verified, with minor issues only.** I checked every substantive numerical claim with my own code, with no author code imported or copied:
- my own OSIL reader (`rosil.py`);
- an exact multi-quadratic-field evaluator for waterno2 (`rev_water.py`);
- a rational interval arithmetic for ann_cumene_tanh and KAN that uses no floating point and no mpmath (`rint.py`, `rev_nn.py`).

All nine required points, and the three extra r3 KAN points, pass. Every objective value and gap the author states agrees with mine to the digits shown. My checks do not depend on mpmath's interval exp. The only assumption is exact rational arithmetic in Python (Fractions and integers).

Which claims are proved, and what "proved" means here:
- **waterno2_06/09/12/18/24: proved exactly feasible for the cached OSIL model**, in exact algebraic arithmetic. Each objective value is an exact rational.
- **ann_cumene_tanh: an exactly feasible point of the cached OSIL model is proved to exist.** The proof is a forward construction plus rigorous interval checks of everything else. The objective is enclosed to a width of 2.8e-89.
- **kan_r5_h1_n3/n5/n8 (and r3 n4/n5/n9): points of the relaxation R are proved to exist.** Each point satisfies every OSIL row except the partition-of-unity rows, every variable bound, and integrality. These are not points of the OSIL models, which are exactly infeasible.

## 1. waterno2 (exact)

Method (`rev_water.py`):
- I wrote each symbol w_k in exact form, p_k + q_k·sqrt(D_k) with D_k = B² − 4AC.
- I checked that the quadratic changes sign on (lo, hi), using exact rationals. This means exactly one root lies in the interval. I picked the ± root whose exact value lies in (lo, hi) and checked that it satisfies A w² + B w + C = 0 exactly.
- I evaluated every row, bound and binary in Q(sqrt(D_1), …, sqrt(D_m)). Each element is stored as {subset: rational coefficient}, with sqrt(D_i)² = D_i.
- Equalities: all coefficients must be exactly zero.
- Inequalities: the sign is decided exactly. For single-field elements I compare a² with b²D. As a cross-check I also use enclosures built from integer square roots (isqrt), at 400 and 2000 bits.

| instance | rows (eq/ineq) | violated | undecided | objective (exact rational, equals the author's) | dual (exact certified rational) | rigorous gap | gap/abs(dual) | gap/abs(primal) |
|---|---|---|---|---|---|---|---|---|
| waterno2_06 | 735/499 | 0 | 0 | 282888037386904807969455615812871/10^30 | 39157472136693483/140737488355328 | 4.657463612 | 1.67396e-2 | 1.64640e-2 |
| waterno2_09 | 1104/748 | 0 | 0 | 914.011975237085991… | 824.8346924546364 | 89.17728278 | 1.081153e-1 | 9.75669e-2 |
| waterno2_12 | 1473/997 | 0 | 0 | 2233.821345608215233… | 2089.7545654395158 | 144.0667802 | 6.89396e-2 | 6.44934e-2 |
| waterno2_18 | 2211/1495 | 0 | 0 | 5023.982760460661871… | 4790.820715376162 | 233.1620451 | 4.86685e-2 | 4.64098e-2 |
| waterno2_24 | 2949/1993 | 0 | 0 | 6963.795180156419512… | 6576.151388415564 | 387.6437917 | 5.89469e-2 | 5.56656e-2 |

Further results for waterno2:
- All variable bounds hold exactly, and all binaries are 0 or 1.
- No row's value involves two fields, which confirms the author's statement.
- The dual rationals I took from the reviews (waterno2-cellslopes-review.md line 237; waterno2-recheck.md lines 262–265) equal the values the author read from certB_verify.json and cert_TT_w1_impl.json.

Comparison with the source points (`rev_water_src.py`; source rows evaluated exactly from their decimal strings):
- **waterno2_06.** MINLPLib's listed p4 has a largest row violation of 1.080e-11, in row e94, and no bound violation. The sum of its cost values is 282.8880373869047. The exact point differs from p4 by at most 3.064e-13 in any coordinate. Its objective is 1.08e-13 above that sum and 2.04e-13 below the objvar 282.888037386905012. All of the author's statements here are confirmed.
- **waterno2_09–24.** The earlier points violate rows by at most 1.0e-9, 1.0e-9, 4.437e-9 and 1.0e-9. They also violate bounds by up to 5.7e-11, 3.1e-10, 8.9e-10 and 9.0e-10, which the report does not mention. The exact points cost 4.887e-6, 1.033e-5, 2.532e-5 and 2.570e-5 more (relative 3.7e-9 to 5.3e-9). Each exact point lies within 8.7e-7 to 2.8e-6 of its source point.

## 2. ann_cumene_tanh and KAN (forward construction, intervals)

Method (`rev_nn.py`, my own existence argument):
- Fix the inputs at exact rationals. For KAN, also fix the binaries at the author's 0/1 values.
- Repeatedly take an equality row in which exactly one variable is unknown. That variable must not occur inside a nonlinear expression or a square term, and its total coefficient (linear coefficient plus bilinear partners) must be provably nonzero. Define the variable as the unique solution of the row. The real point defined this way satisfies every defining row exactly.
- Check all other rows, all bounds and integrality, exactly where the values are rational and by rigorous enclosures otherwise.
- Enclosures (`rint.py`): rational endpoints rounded outward to 320 bits. exp comes from a Taylor polynomial evaluated exactly in rationals, with a Lagrange remainder bound and outward squaring; tanh = 1 − 2/(exp(2x)+1), which is monotone.
- Self-test (`test_rint.py`): 400 random exp and tanh arguments in [−60, 60] against 120-digit mpmath (used only as a reference); 3,000 outward-rounding checks; 2,000 random interval +, −, ×, ÷ containment checks. All passed.
- KAN partition rows: identified independently as equality rows of continuous variables with all coefficients 1 and right-hand side 1. This gives 54, 90 and 144 rows for r5 n3/n5/n8 (3 per edge), the same set as the author's dropped_rows. R in wave 3 drops these rows, the B ≥ 0 bounds and most intermediate bounds. The points satisfy all of those anyway, so they lie in R.

| instance | inputs match source | rows used as definitions | other rows | bounds / integrality | objective enclosure (mine, width) | dual | rigorous gap (mine) | author |
|---|---|---|---|---|---|---|---|---|
| ann_cumene_tanh | yes (wave3.sol decimals) | 789 (all equalities) | 1 inequality (e789, margin 9.979e-13) | all hold | −3379.982394071771548095722619880928244… (2.8e-89) | −3386.5402291369187 (binary64) | 6.557835065 | 6.55784 |
| kan_r5_h1_n3 | yes (binary64 u) | 617 | 18 one-hot rows exact; 432 inequalities | all hold; 216 binaries 0/1 | −262.86422588506524044453558108664… (3.0e-89) | −262.86422590922143 | 2.4156191e-8 | 2.41562e-8 |
| kan_r5_h1_n5 | yes | 1027 | 30 exact; 720 inequalities | all; 360 binaries | 0.27258325395662269730746585336402… (1.2e-89) | 0.2725832538548472 | 1.0177548e-10 | 1.01776e-10 |
| kan_r5_h1_n8 | yes | 1642 | 48 exact; 1152 inequalities | all; 576 binaries | 0.06932786060619108532659407018319… (3.2e-89) | 0.06932786051052511 | 9.5665972e-11 | 9.56660e-11 |
| kan_r3_h1_n4 (extra) | yes | 838 | 16 exact; 576 inequalities | all | 0.00278123722144181412905… | 0.0027812371525813705 | 6.886044e-11 | 6.88605e-11 |
| kan_r3_h1_n5 (extra) | yes | 1047 | 20 exact; 720 inequalities | all | −0.01104267941448729530645… | −0.011042679521782046 | 1.072948e-10 | 1.07295e-10 |
| kan_r3_h1_n9 (extra) | yes | 1883 | 36 exact; 1296 inequalities | all | 0.01296366005303932849663… | 0.01296365996347472 | 8.956461e-11 | 8.95647e-11 |

Further results for ann and KAN:
- My definition rows are the same as the author's 'defined_by' for every interval-valued variable.
- The author's stored values are consistent with my enclosures for every variable of every instance.
- The author's objective enclosures contain mine.
- The smallest margins of interval-valued inequalities in KAN are 1.4e-2 to 6.5e-2 for r5, and 7.3e-5 to 3.4e-3 for r3. On layer 2 there is therefore no knot ambiguity; layer-1 big-M rows are decided exactly.
- In ann, two saturated tanh neurons give enclosures that touch a bound of ±1 exactly (x657 in my run, x650 in the author's). This is still a proof, because the enclosure is outward and tanh lies strictly inside (−1, 1).
- Relative gaps (mine): ann 1.9364e-3 of abs(dual) and 1.9402e-3 of abs(primal), matching the summary's 0.194%. KAN r5: 9.19e-11, 3.734e-10, 1.380e-9.

## 3. Parser validation and negative controls (`rev_parse_controls.py`)

- MINLPLib's listed points, read with my reader, satisfy the rows to 8.2e-12 (ann p1), 3.6e-12 (kan_r5_h1_n3 p2), 9.0e-11 (n5 p2) and 2.3e-12 (n8 p3), with no bound violations. waterno2_06 p4 gives 1.08e-11. A misread coefficient would show up as a large violation here.
- Negative controls, all rejected for the expected reason:
  - waterno2_06: one coordinate shifted by 1e-30 (row e20 fails); a root interval moved off its root (no sign change); a field coefficient c0 shifted by 1e-40 (row e18 fails); one binary flipped (rows e180, e396, e450 and e960 fail).
  - kan_r5_h1_n3: knot binary moved to the neighbouring interval (big-M row e33 fails by 0.151); partition rows kept (rows not exact, as expected for an exactly infeasible model); an input changed by 1e-20 (no longer equal to the wave-3 u).

## 4. Issues (all minor)

1. The author's report.md does not exist. The text I received was cut off in Section 2, step 2, so I did not review the rest of the method, the assumptions or the command list. The integration step must save the full text, and someone should read the omitted sections.
2. Some relative gaps are rounded up or rounded twice without saying so: 10.82% (exact 10.8115%), 5.90% (exact 5.8947%), and the table's 1.647e-2 and 6.450e-2 (exact 1.6464e-2 and 6.4493e-2). This is conservative but should be stated, or the nearest values used. 'Relative 4e-9 to 5e-9' is really 3.7e-9 to 5.3e-9.
3. The earlier waterno2_09–24 points also violate bounds (up to 9.0e-10). The table reports only row violations.
4. The log line 'smallest proved margin 0.000e+00 (x650 ub)' should be explained in the report as a saturated neuron. It is a valid proof.
5. The JSON 'construction' text says '(mid, rad)', but values are stored as lo/hi.

The author's statement that the work was not independently reviewed is accurate. This review now provides that independent check for all the numerical claims in the visible text.

## 5. Commands run (from /workspace/minlp-notes/research-20260929/publication/reviews/primal-water-ann-kan-r1; one core, each under 15 s)

- `python3 rev_water.py 06|09|12|18|24` → logs/rev_water_XX.log. All pass. The final logs were regenerated after the fix in the next item; the earlier runs gave the same output.
- `python3 rev_water_src.py` → logs/rev_water_src.log. The first run failed on a bug in my own code: a cache of square-root bounds was not reset between instances within one process. My exact-versus-enclosure cross-check caught it. After the fix the run passed.
- `python3 test_rint.py` → logs/test_rint.log (pass, 12.4 s). An earlier inline version used unrealistic exp arguments up to 1e18. It hung, and my pkill also ended its shell.
- `python3 rev_nn.py ann_cumene_tanh` → logs/rev_nn_ann_cumene_tanh.log. The first run stopped on my own overly strict assertion against a zero margin of an interval value (x657, a saturated tanh). I relaxed it, since a zero margin is still a proof, and the run passed.
- `python3 rev_nn.py kan_r5_h1_n3|kan_r5_h1_n5|kan_r5_h1_n8|kan_r3_h1_n4|kan_r3_h1_n5|kan_r3_h1_n9` → logs/rev_nn_*.log. All pass.
- `python3 rev_parse_controls.py` → logs/rev_parse_controls.log. Parser checks pass; all 7 negative controls rejected.
- An inline Python check that the author's dual sources (certB_verify.json, cert_TT_w1_impl.json) equal the review rationals: all 5 equal.
- Read-only inspection of the author's code, points and logs, the wave-3 KAN/ANN notes, and the OSIL files.

No CI checks or project-wide checks were run. No git operations were performed.

## Issues

- **minor**: The author's report.md does not exist in /workspace/minlp-notes/research-20260929/publication/primal/water-ann-kan/. The report text passed to the reviewer was cut off in Section 2, step 2 ('The pum...'). I could not review the rest of the waterno2 method, the ann/KAN method text, the stated assumptions or the command list. The integration step should save the full text word for word, and someone should read the omitted sections. All numerical claims in the part I received were checked independently, and they hold.
- **minor**: Some relative gaps are rounded up, and some are rounded twice, without saying so in the text. Exact values: waterno2_09 gap/dual = 10.8115% (text says 10.82%, table 1.082e-1); waterno2_24 = 5.8947% (text 5.90%); waterno2_06 gap/primal = 1.6464e-2 (table 1.647e-2); waterno2_12 gap/primal = 6.4493e-2 (table 6.450e-2). Upward rounding is conservative and is documented in code/gaps.py, but the paper should either say 'rounded up' or give the nearest values (10.81%, 6.89%, 4.87%, 5.89%). Similarly, 'in relative terms this is 4e-9 to 5e-9' is really 3.7e-9 to 5.3e-9.
- **minor**: The earlier tolerance-feasible points for waterno2_09–24 also violate variable bounds, by 5.7e-11, 3.1e-10, 8.9e-10 and 9.0e-10. The table column 'earlier primal (max row violation)' reports only row violations. This matters only when describing the old points.
- **minor**: In the ann_cumene_tanh log, the author's line 'smallest proved margin 0.000e+00 (x650 ub)' looks like an unproved bound, but it is not one. x650 = tanh(x670) with x670 ≈ 101.8 is a saturated neuron, so the 60-digit enclosure ends exactly at 1. With 96 digits I see the same effect for x657 = tanh(x677), x677 ≈ −125.75, at the bound −1. A zero margin of an outward enclosure is still a valid proof, and tanh lies strictly inside (−1, 1). The report should explain this line.
- **minor**: Point JSON files for ann and KAN: the 'construction' string says interval values are given as '(mid, rad)', but they are stored as lo/hi. This is cosmetic.

## Commands run

- `python3 rev_water.py 06 / 09 / 12 / 18 / 24 (exact multi-quadratic-field check of the waterno2 points; all pass)`
- `python3 rev_water_src.py (comparison with p4 and the earlier wave-2 points; first run hit a cache bug in the reviewer's code, fixed and rerun: pass)`
- `python3 test_rint.py (self-test of the rational interval arithmetic against 120-digit mpmath: pass)`
- `python3 rev_nn.py ann_cumene_tanh (first run stopped on the reviewer's overly strict zero-margin assertion; relaxed and rerun: pass)`
- `python3 rev_nn.py kan_r5_h1_n3 / kan_r5_h1_n5 / kan_r5_h1_n8 (pass)`
- `python3 rev_nn.py kan_r3_h1_n4 / kan_r3_h1_n5 / kan_r3_h1_n9 (extra instances; pass)`
- `python3 rev_parse_controls.py (parser validation on MINLPLib listed points; 7 negative controls all rejected)`
- `inline python: author's dual sources certB_verify.json and cert_TT_w1_impl.json equal the review rationals (5/5)`
- `read-only inspection: author's code/points/logs, open-instances-wave3 report and kan_model.py, OSIL files in ~/.cache/minlplib/minlplib/osil`
