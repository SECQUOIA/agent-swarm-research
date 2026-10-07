## Exact old → new integration edits (round 2)

Apply these ordered edits; the target files were read only. The machine-readable list is [integration-r2.json](integration-r2.json). Each replacement was tested in memory against the current files. All new numeric primal displays are checked in [check_r2.log](check_r2.log).

### `open-instances-summary.md`

lnts50: column 5, 5.5e-13 -> 5.79e-13

Old:
```text
| lnts50 | 0.55464755 | 0.5546687649381 | 0.5546687649387 | 5.5e-13 | chain Lagrangian, linear-tangent law, monotone in h | [verified](reviews/open-instances-verification/verification-report.md) |
```
New:
```text
| lnts50 | 0.55464755 | 0.5546687649381 | 0.5546687649387 | 5.79e-13 | chain Lagrangian, linear-tangent law, monotone in h | [verified](reviews/open-instances-verification/verification-report.md) |
```

lnts100: column 4, 0.5545954011669 -> 0.5545954011670

Old:
```text
| lnts100 | 0.55299042 | 0.5545954011663 | 0.5545954011669 | 5.5e-13 | same | verified |
```
New:
```text
| lnts100 | 0.55299042 | 0.5545954011663 | 0.5545954011670 | 5.5e-13 | same | verified |
```

lnts100: column 5, 5.5e-13 -> 6.12e-13

Old:
```text
| lnts100 | 0.55299042 | 0.5545954011663 | 0.5545954011670 | 5.5e-13 | same | verified |
```
New:
```text
| lnts100 | 0.55299042 | 0.5545954011663 | 0.5545954011670 | 6.12e-13 | same | verified |
```

lnts200: column 5, 5.5e-13 -> 5.84e-13

Old:
```text
| lnts200 | 0.55219867 | 0.5545770161025 | 0.5545770161031 | 5.5e-13 | same | verified |
```
New:
```text
| lnts200 | 0.55219867 | 0.5545770161025 | 0.5545770161031 | 5.84e-13 | same | verified |
```

lnts400: column 5, 5.5e-13 -> 5.88e-13

Old:
```text
| lnts400 | 0.55204395 | 0.5545724137001 | 0.5545724137007 | 5.5e-13 | same | verified |
```
New:
```text
| lnts400 | 0.55204395 | 0.5545724137001 | 0.5545724137007 | 5.88e-13 | same | verified |
```

dtoc5: column 4, 5.38967211918114 -> 5.389672119181141

Old:
```text
| dtoc5 | 0.00243096 | 5.38967211918114 | 5.38967211918114 | < 1e-14 | Lagrangian convex at the costate (Mangasarian/Arrow-type) | verified |
```
New:
```text
| dtoc5 | 0.00243096 | 5.38967211918114 | 5.389672119181141 | < 1e-14 | Lagrangian convex at the costate (Mangasarian/Arrow-type) | verified |
```

chain50–400: column 4, same to 1e-14 -> exact-point objectives within 1.01e-14 of the duals

Old:
```text
| chain50–400 | 0.0826–0.1745 | 5.06862 … 5.07226 | same to 1e-14 | ≤ 1.0e-14 | discrete catenary calibration + 2-D end-window B&B | [verified](reviews/cops-verification/verification-report.md) |
```
New:
```text
| chain50–400 | 0.0826–0.1745 | 5.06862 … 5.07226 | exact-point objectives within 1.01e-14 of the duals | ≤ 1.0e-14 | discrete catenary calibration + 2-D end-window B&B | [verified](reviews/cops-verification/verification-report.md) |
```

chain50–400: column 5, ≤ 1.0e-14 -> ≤ 1.01e-14

Old:
```text
| chain50–400 | 0.0826–0.1745 | 5.06862 … 5.07226 | exact-point objectives within 1.01e-14 of the duals | ≤ 1.0e-14 | discrete catenary calibration + 2-D end-window B&B | [verified](reviews/cops-verification/verification-report.md) |
```
New:
```text
| chain50–400 | 0.0826–0.1745 | 5.06862 … 5.07226 | exact-point objectives within 1.01e-14 of the duals | ≤ 1.01e-14 | discrete catenary calibration + 2-D end-window B&B | [verified](reviews/cops-verification/verification-report.md) |
```

ex6_2_5: column 4, −70.752077833447706 -> −70.752077833447705

Old:
```text
| ex6_2_5 | −111.4201713 | −70.75207783344770759 | −70.752077833447706 | 2.0e-15 | same | verified |
```
New:
```text
| ex6_2_5 | −111.4201713 | −70.75207783344770759 | −70.752077833447705 | 2.0e-15 | same | verified |
```

powerflow0039p: column 4, 41869.0515113202 -> 41869.0515113203

Old:
```text
| powerflow0039p | 41818.27916 | 41869.05148485014 | 41869.0515113202 | 6.3e-10 rel. | SDP dual + exact leaf-bus identity (bus 29) + exact vertex cuts, B&B on 3 leaf coordinates ([extension](open-instances-wave3/powerflow/extension-report.md)) | [verified](reviews/powerflow0039-review.md) |
```
New:
```text
| powerflow0039p | 41818.27916 | 41869.05148485014 | 41869.0515113203 | 6.3e-10 rel. | SDP dual + exact leaf-bus identity (bus 29) + exact vertex cuts, B&B on 3 leaf coordinates ([extension](open-instances-wave3/powerflow/extension-report.md)) | [verified](reviews/powerflow0039-review.md) |
```

powerflow0039r: column 4, 41869.0515113208 -> 41869.0515113210

Old:
```text
| powerflow0039r | 41804.88153 | 41869.05148327243 | 41869.0515113208 | 6.7e-10 rel. | same | verified |
```
New:
```text
| powerflow0039r | 41804.88153 | 41869.05148327243 | 41869.0515113210 | 6.7e-10 rel. | same | verified |
```

eg_int_s: column 4, 6.4531031593842274 (exactly feasible) -> 6.4531031593842275 (exactly feasible)

Old:
```text
| eg_int_s | 6.32629896 (SCIP) | 6.4531031529331155 | 6.4531031593842274 (exactly feasible) | 1.0e-9 rel. | second-order Taylor models keeping the signed cancellation of the Gaussian-kernel rows, per-box LP over the 24 minimax rows, domain reduction, exact integer splits ([note](open-instances-wave3/eg/retry.md)); SCIP 8.1 had solved it in floating point (Göß–Burlacu–Martin) | [verified](reviews/eg-retry-review.md) (all leaves re-certified independently) |
```
New:
```text
| eg_int_s | 6.32629896 (SCIP) | 6.4531031529331155 | 6.4531031593842275 (exactly feasible) | 1.0e-9 rel. | second-order Taylor models keeping the signed cancellation of the Gaussian-kernel rows, per-box LP over the 24 minimax rows, domain reduction, exact integer splits ([note](open-instances-wave3/eg/retry.md)); SCIP 8.1 had solved it in floating point (Göß–Burlacu–Martin) | [verified](reviews/eg-retry-review.md) (all leaves re-certified independently) |
```

eg_disc_s: column 4, 5.7605396164535106 (exactly feasible) -> 5.7605396164535107 (exactly feasible)

Old:
```text
| eg_disc_s | 3.36596129 (SCIP) | 5.760539610694994 | 5.7605396164535106 (exactly feasible) | 1.0e-9 rel. | same | verified (all leaves) |
```
New:
```text
| eg_disc_s | 3.36596129 (SCIP) | 5.760539610694994 | 5.7605396164535107 (exactly feasible) | 1.0e-9 rel. | same | verified (all leaves) |
```

eg_disc2_s: column 7, verified (part with the optimum fully; other parts by a sample of 110,676 of 979,044 leaves) -> verified on all 1,114,361 leaves under A1/A2; separate outward-rounded interval sample: 10,404 leaves of parts 0 and 2–7

Old:
```text
| eg_disc2_s | 0 (SHOT) | 5.642100574331458 | 5.6421005799711068 (exactly feasible) | 1.0e-9 rel. | same | verified (part with the optimum fully; other parts by a sample of 110,676 of 979,044 leaves) |
```
New:
```text
| eg_disc2_s | 0 (SHOT) | 5.642100574331458 | 5.6421005799711068 (exactly feasible) | 1.0e-9 rel. | same | verified on all 1,114,361 leaves under A1/A2; separate outward-rounded interval sample: 10,404 leaves of parts 0 and 2–7 |
```

waterno2_06: column 4, 282.888 (listed) -> 282.888038 (exactly feasible)

Old:
```text
| waterno2_06 | 165.19 | **278.230573** (separator branching: 272.584700; wave 2: 263.735099) | 282.888 (listed) | 1.67% (3.78%; 7.26%) | wave 2 [verified](reviews/waterno2-verification/verification-report.md); separator branching [verified](reviews/waterno2-sepbranch-review.md); cell-dependent slopes [verified](reviews/waterno2-cellslopes-review.md) (all 49,315 pair bounds re-bounded independently) |
```
New:
```text
| waterno2_06 | 165.19 | **278.230573** (separator branching: 272.584700; wave 2: 263.735099) | 282.888038 (exactly feasible) | 1.67% (3.78%; 7.26%) | wave 2 [verified](reviews/waterno2-verification/verification-report.md); separator branching [verified](reviews/waterno2-sepbranch-review.md); cell-dependent slopes [verified](reviews/waterno2-cellslopes-review.md) (all 49,315 pair bounds re-bounded independently) |
```

waterno2_06: column 5, 1.67% (3.78%; 7.26%) -> 1.68% (3.78%; 7.26%)

Old:
```text
| waterno2_06 | 165.19 | **278.230573** (separator branching: 272.584700; wave 2: 263.735099) | 282.888038 (exactly feasible) | 1.67% (3.78%; 7.26%) | wave 2 [verified](reviews/waterno2-verification/verification-report.md); separator branching [verified](reviews/waterno2-sepbranch-review.md); cell-dependent slopes [verified](reviews/waterno2-cellslopes-review.md) (all 49,315 pair bounds re-bounded independently) |
```
New:
```text
| waterno2_06 | 165.19 | **278.230573** (separator branching: 272.584700; wave 2: 263.735099) | 282.888038 (exactly feasible) | 1.68% (3.78%; 7.26%) | wave 2 [verified](reviews/waterno2-verification/verification-report.md); separator branching [verified](reviews/waterno2-sepbranch-review.md); cell-dependent slopes [verified](reviews/waterno2-cellslopes-review.md) (all 49,315 pair bounds re-bounded independently) |
```

waterno2_09: column 4, 914.012 (ours, viol. ≤ 4.4e-9) -> 914.012 (exactly feasible)

Old:
```text
| waterno2_09 | 273.90 | 824.834692 | 914.012 (ours, viol. ≤ 4.4e-9) | 10.8% | [verified](reviews/waterno2-recheck.md) (all periods) |
```
New:
```text
| waterno2_09 | 273.90 | 824.834692 | 914.012 (exactly feasible) | 10.8% | [verified](reviews/waterno2-recheck.md) (all periods) |
```

waterno2_09: column 5, 10.8% -> 10.82%

Old:
```text
| waterno2_09 | 273.90 | 824.834692 | 914.012 (exactly feasible) | 10.8% | [verified](reviews/waterno2-recheck.md) (all periods) |
```
New:
```text
| waterno2_09 | 273.90 | 824.834692 | 914.012 (exactly feasible) | 10.82% | [verified](reviews/waterno2-recheck.md) (all periods) |
```

waterno2_12: column 4, 2233.821 (ours) -> 2233.821346 (exactly feasible)

Old:
```text
| waterno2_12 | 479.51 | 2089.754565 | 2233.821 (ours) | 6.9% | verified (all periods) |
```
New:
```text
| waterno2_12 | 479.51 | 2089.754565 | 2233.821346 (exactly feasible) | 6.9% | verified (all periods) |
```

waterno2_12: column 5, 6.9% -> 6.90%

Old:
```text
| waterno2_12 | 479.51 | 2089.754565 | 2233.821346 (exactly feasible) | 6.9% | verified (all periods) |
```
New:
```text
| waterno2_12 | 479.51 | 2089.754565 | 2233.821346 (exactly feasible) | 6.90% | verified (all periods) |
```

waterno2_18: column 4, 5023.983 (ours) -> 5023.983 (exactly feasible)

Old:
```text
| waterno2_18 | 770.74 | 4790.820715 | 5023.983 (ours) | 4.9% | verified (all periods) |
```
New:
```text
| waterno2_18 | 770.74 | 4790.820715 | 5023.983 (exactly feasible) | 4.9% | verified (all periods) |
```

waterno2_18: column 5, 4.9% -> 4.87%

Old:
```text
| waterno2_18 | 770.74 | 4790.820715 | 5023.983 (exactly feasible) | 4.9% | verified (all periods) |
```
New:
```text
| waterno2_18 | 770.74 | 4790.820715 | 5023.983 (exactly feasible) | 4.87% | verified (all periods) |
```

waterno2_24: column 4, 6963.795 (ours) -> 6963.795181 (exactly feasible)

Old:
```text
| waterno2_24 | 1095.13 | 6576.151388 | 6963.795 (ours) | 5.9% | verified (all periods) |
```
New:
```text
| waterno2_24 | 1095.13 | 6576.151388 | 6963.795181 (exactly feasible) | 5.9% | verified (all periods) |
```

waterno2_24: column 5, 5.9% -> 5.90%

Old:
```text
| waterno2_24 | 1095.13 | 6576.151388 | 6963.795181 (exactly feasible) | 5.9% | verified (all periods) |
```
New:
```text
| waterno2_24 | 1095.13 | 6576.151388 | 6963.795181 (exactly feasible) | 5.90% | verified (all periods) |
```

ann_cumene_tanh: column 3, **−3386.5403** (wave 3: −4024.495, the first finite dual) -> **−3386.5403** (wave 3: −4024.495, first rigorous finite dual found for this MINLPLib model; the identical exp twin was closed in floating point)

Old:
```text
| ann_cumene_tanh | none | **−3386.5403** (wave 3: −4024.495, the first finite dual) | −3379.9824 | 0.194% (wave 3: 19%) | wave 3 verified with caveats; extension [independently re-certified](reviews/ann-extension-review.md) |
```
New:
```text
| ann_cumene_tanh | none | **−3386.5403** (wave 3: −4024.495, first rigorous finite dual found for this MINLPLib model; the identical exp twin was closed in floating point) | −3379.9824 | 0.194% (wave 3: 19%) | wave 3 verified with caveats; extension [independently re-certified](reviews/ann-extension-review.md) |
```

ann_cumene_tanh: column 4, −3379.9824 -> −3379.9823940 (exactly feasible)

Old:
```text
| ann_cumene_tanh | none | **−3386.5403** (wave 3: −4024.495, first rigorous finite dual found for this MINLPLib model; the identical exp twin was closed in floating point) | −3379.9824 | 0.194% (wave 3: 19%) | wave 3 verified with caveats; extension [independently re-certified](reviews/ann-extension-review.md) |
```
New:
```text
| ann_cumene_tanh | none | **−3386.5403** (wave 3: −4024.495, first rigorous finite dual found for this MINLPLib model; the identical exp twin was closed in floating point) | −3379.9823940 (exactly feasible) | 0.194% (wave 3: 19%) | wave 3 verified with caveats; extension [independently re-certified](reviews/ann-extension-review.md) |
```

Replace the obsolete tolerance-only claim and state gap conventions.

Old:
```text
For lnts50–400, dtoc5, lukvle10, chain50–400 and
powerflow0030p/0039p/0039r, the primal side is a point feasible to row
violations of 1e-20 to 8e-12; closure is measured against its value, and no
exactly feasible point was constructed.
```
New:
```text
For lnts50–400, dtoc5, lukvle10, chain50–400 and
powerflow0030p/0039p/0039r, exactly feasible points have now been constructed
and independently reviewed in publication/primal/. The gaps use the upper
ends of their objective enclosures. The lnts gap cells use the displayed
summary duals; against the certified verifier N·h2 bounds the gaps are at
most 5.55e-13. The lukvle10 KKT agreement is numerical and does not prove
global optimality; attributing its remaining gap to the dual requires that
additional assumption.
```

State display directions and distinguish exact-point gaps from display subtraction.

Old:
```text
Displayed dual bounds are truncated or rounded outward, so each displayed
value is itself a valid bound.
```
New:
```text
Displayed dual bounds are truncated or rounded outward, so each displayed
value is itself a valid bound. Numeric primal bounds are rounded upward for
minimization and downward for maximization. A point objective enclosure
can give a tighter gap than subtraction of the two displayed bounds.
```

Remove the obsolete eg coverage qualifier.

Old:
```text
(all
independently verified, eg_disc2_s partly by sampling;
```
New:
```text
(all
independently verified, eg_disc2_s on every leaf under A1/A2 with a separate interval sample;
```

Remove the second stale tolerance-only claim.

Old:
```text
for 13 of them the
primal side is only tolerance feasible, see the note below the first
table)
```
New:
```text
exactly feasible primal points now also cover the 13 formerly tolerance-only instances, see the note below the first
table)
```

### `bound-audit/audit-report.md`

Correct precision and define all three entry counts.

Old:
```text
- **Display precision.** Values are shown with at most 10 significant digits
  and at most 8 decimals, and trailing zeros are dropped.
```
New:
```text
- **Display precision.** Values are shown with at most 8 decimals; there is
  no 10-significant-digit limit. Counts refer to displayed entries, not
  distinct numbers: 35 entries (18 distinct strings) with a nonempty
  fractional part have 11–17 digits from the first through last nonzero
  digit; dropping the fractional-part filter gives 38 entries with 11–19
  digits; counting trailing integer zeros as significant gives 46 entries
  with 11–20 digits (for example −10000000000.). Trailing fractional zeros
  are dropped.
```

Keep the floor with its actual justification and checked effect.

Old:
```text
  - For each listed dual, the **slack** is half a unit in its last shown
    digit, but never less than half a unit in the 10th significant digit.
    For the value 0, the slack is 5e-9.
```
New:
```text
  - For each listed dual, the **slack** is half a unit in its last shown
    digit, but never less than half a unit in the 10th significant digit.
    This floor is an explicit conservative choice, not a consequence of a
    display limit. It changes the slack of 0 of the 158 screened pairs and
    therefore changes no screened-pair class. It changes 17 display-tie
    pairs on three instances: fac1, fac2 and waternd_fosspoly0.
    For the value 0, the slack is 5e-9.
```

Integrate qualified spring wording without changing classes or counts.

Old:
```text
  dated 17 Sep 2013: eniplac (a 6-digit value) and spring (8 digits).
```
New:
```text
  dated 17 Sep 2013: eniplac (a 6-digit value) and spring (8 digits).
  The five spring (i-r) solver-point pairs need not be solver errors:
  display rounding explains their listed conflict, while the underlying
  stored solver bounds are unknown. The spring SCIP objective difference
  of about 1e-9 comes from bisection and feasibility tolerance; it is not
  an independent objective disagreement.
```

### `open-instances-wave2/cops/report.md`

Use a chain dual display below the exact binary64 certificate; apply to every occurrence.

Old:
```text
5.072261493982863
```
New:
```text
5.0722614939828627
```

Use a chain dual display below the exact binary64 certificate; apply to every occurrence.

Old:
```text
5.068917341793162
```
New:
```text
5.0689173417931616
```

### `reviews/cops-verification/verification-report.md`

Use a chain dual display below the exact binary64 certificate; apply to every occurrence.

Old:
```text
5.072261493982863
```
New:
```text
5.0722614939828627
```

Use a chain dual display below the exact binary64 certificate; apply to every occurrence.

Old:
```text
5.068917341793162
```
New:
```text
5.0689173417931616
```

### `reviews/closing-audit-a.md`

Use a chain dual display below the exact binary64 certificate; apply to every occurrence.

Old:
```text
5.072261493982863
```
New:
```text
5.0722614939828627
```

### `publication/reviews/solver-campaign-review-r1.md`

Use a chain dual display below the exact binary64 certificate; apply to every occurrence.

Old:
```text
5.072261493982863
```
New:
```text
5.0722614939828627
```

### `publication/solver-runs/report.prev.md`

Use a chain dual display below the exact binary64 certificate; apply to every occurrence.

Old:
```text
5.072261493982863
```
New:
```text
5.0722614939828627
```
