# Critique of the `solvers` dossier (independent critic, 2026-10-04)

Dossier: `paper-open-minlplib/development/dossiers/solvers.md` (line numbers below refer to that file).
Paths: `R/` = `research-20260929/`, `P/` = `R/publication/`, `C/` = `paper-open-minlplib/development/dossiers/solvers-checks/`.
My scripts and logs: `C/critic/` (README gives the copy-then-run procedure). All runs used copies in `/tmp/crit_solv/`, one core, a few seconds each. No solver was run. Nothing under `R/` or `literature/` was edited or executed in place. Nothing was committed.

## Verdict

**Corrections needed. Nothing found invalidates a claimed result of this family.**

- Every proposition that carries a refutation survives: BARON camshape100/200 (Prop. 4), the SCIP witnesses (Prop. 6), the fm336 and tiny2 optima (Prop. 7), CAMINO (Prop. 13, under its assumptions), KAN (Prop. 14), MINOTAUR/ANTIGONE on the QPLIB copies (Prop. 15) and MINOTAUR on optcdeg2 (Prop. 16).
- A third implementation of the camshape-type bound, written here with a different parser and algorithm, reproduces all eight bounds of Proposition 3 to 20 digits, and the D(ε) values of Proposition 5.
- There are factual errors in supporting statements:
  - a sign error on QPLIB_2738;
  - an incorrect "exactly" in Lemma 8;
  - an over-broad description of the SCIP data trigger;
  - several margins that are rounded up although the dossier calls them lower bounds;
  - two issue resolutions (S15, S16) that do not do what they claim;
  - S1's prior-work wording for camshape200.

## 1. What I checked independently

| item | method | result |
|---|---|---|
| Lemma 2, Propositions 3 and 5 | Re-derived by hand: the closed form for z_j, the division steps, the ε relaxation. Checked monotonicity of the bound formula in ε. | Correct. One notational slip (C15). |
| Bounds of Proposition 3 on all 8 models | `C/critic/indep_bound.py`: sympy parser with exact rationals; a presence check of every needed row; smoothing iterated to convergence (not one forward/backward pass) | All 8 bounds agree with `C/r2/cambd.log` to 20 digits, e.g. QPLIB_3177 −4.27418715147174339059…, QPLIB_2738 −4.28414626780461160503… (`indep_bound.log`). |
| D(ε) of Proposition 5 | `C/critic/eps_check.py` | 6.0447e-7, 2.3551e-6, 2.8043e-5, 6.0449e-5, 1.5717e-4, 3.7443e-4, 3.7296e-3, and the ratios 0.870 / 0.872 / 0.291, all reproduced. |
| QPLIB `.sol` points | `C/critic/evalgms.py`: exact evaluation of the four `.sol` files against their `.gms` copies | See C1. The 2703/3177 deficits 8.154e-6 / 3.272e-5 are confirmed, with row violations of 3.0e-10 (e401, e801). |
| Lemma 8 and the trigger | `C/critic/enclosure.py`; `strong_criterion.py` (reads OSIL read-only; imports a `/tmp` copy of `pattern_scan.py`) | Residuals reproduced. See C2 and C3. |
| Campaign counts | `/tmp` copy of `results_table.csv`: first batch, CPU/wall ranking, overruns, claims. Logs: BARON CPU times, iterations. | All agree with Proposition 1: ten first-batch rows; ratios 0.9561–0.9811 are the ten lowest of 117; BARON CPU 3600.01–3601.65 s; 3 iterations / 0.45 s. |
| Margins | `fractions` (`margins_floor.log`) | BARON 5.2581469620e-7 and 2.0527074677e-6; KAN 1.70007303e-3 / 2.03831638e-3; CAMINO 0.244594 / 0.431290 / 5.201056. All agree. Rounding direction: see C4. |
| SCIP sources | `P/scip-bug/report.md`, review r1, `checksol_witness.log`, `rv_wheel.log`, checker logs, CIP of fm336/tiny2 | The model statements and the Prop. 7 proofs are correct. Acceptance of all eight witnesses is confirmed (union of the two logs). |
| Literature and logs | MINOTAUR/ANTIGONE/SCIP 9.2.1 logs, CAMINO CSV and `using_amplpy.py`, MINLPLib S-mark text, BARON/Gurobi release notes, Neumaier 19/209, `pages.json` (waterno2_01–04) | Agree, with exceptions C10, A3, A6. |

## 2. Corrections

**C1. Sign error: QPLIB's QPLIB_2738 point lies *below* the bound, not above (lines 396, 784–787; S4 evidence).**

- Problem. The dossier says QPLIB's point gives −4.284146267804670, "5.8e-14 above" the bound −4.284146267804612, and calls QPLIB_2738 and QPLIB_2480 "consistent".
  - −4.284146267804670 < −4.284146267804612, so the value is below the bound.
  - `C/r2/claims.log` itself prints "margin >= 5.839498e-14". It uses the same sign convention as the 2703/3177 rows, where a positive margin means "below".
- Evidence (`qplib_sol_eval.log`):
  - Exact evaluation of `QPLIB_2738.sol` gives f(r) = −4.2841462678046716, which is 5.97e-14 below the bound; objvar is 5.84e-14 below.
  - The maximum row violation is 1.96e-14 (e143), which is printing-level.
  - D(2e-14) ≈ 1.2e-10 ≫ 6e-14, so there is no contradiction with Proposition 3.
  - QPLIB_2480 is genuinely 1.48e-12 above.
- Fix. Write: "QPLIB's QPLIB_2738 point lies 5.8e-14 (objvar) below the bound. Its 15-decimal coordinates violate rows by ≤ 2e-14, which explains this. QPLIB_2480's point lies 1.5e-12 above." The 2703/3177 finding is unchanged. Strictly, all three of 2738, 2703 and 3177 have reference points below rigorous bounds; only 2703 and 3177 are beyond printing scale.

**C2. The data trigger is one row per period (the 0.7-station cube), not 12 (Observation 12, lines 667–689; Lemma 8; §9 lines 1384–1389; S18).**

- Problem. Observation 12 counts as "binary64-inconsistent" every row whose exact residual fl(L)^k − fl(L^k) has the infeasible sign: 12 per period, covering L = 0.6, 0.7, 0.85 and the 0.8 upper bound, for squares and cubes. The traced failure needs more than that: an *empty* exact intersection of a valid outward-rounded enclosure of fl(L)^k with fl(L^k). Any valid enclosure contains round-up(fl(L)^k) on the lower-bound side, or round-down on the upper-bound side.
- Evidence (`enclosure.log`):
  - The tightest enclosure misses the bound only for L = 0.7, k = 3: round-up = 0.34299999999999997 < fl(0.343).
  - For 0.6², 0.6³, 0.7², 0.85², 0.85³, 0.8² and 0.8³, round-up (or round-down) equals fl(L^k) itself. The residual is below one binary64 spacing there, so the intersection is non-empty and this mechanism cannot fire.
  - `strong_criterion.log`: waterno2_01 has 12 sign hits and 1 enclosure hit; waterno2_06 has 72 and 6; waterno2_24 has 288 and 24. All enclosure hits are lb 0.7, k = 3.
- Consequences.
  - This explains why every instrumented cutoff is at a 0.7 station. The report says "largest residual", but the actual reason is that 0.7³ is the only case whose residual exceeds the binary64 spacing.
  - It strengthens the seed-11 caveat: its first loss involves b35 at the 0.85 station, and the 0.85 cube row cannot produce this empty intersection.
- Fix.
  - In Observation 12, keep the syntactic count. Add: "Only rows where the enclosure misses the bound can trigger the traced exact-intersection cutoff. In MINLPLib (syntactic class) these are the 0.7-station cube rows of waterno2, one per period."
  - In §9, write "because the outward-rounded binary64 enclosure of fl(0.7)³ lies entirely below fl(0.343)".

**C3. Lemma 8: SCIP's activity is *not* "exactly" the tightest enclosure minus fl(0.343) (line 575).**

- Evidence. The tightest enclosure is [0.3429999999999999, 0.34299999999999997]. Subtracting fl(0.343) gives [−1.1102e-16, −5.5511e-17]. SCIP's traced activity is [−1.6653e-16, −5.5511e-17], which corresponds to SCIP's s³ enclosure [0.34299999999999986, …] (report §5.2). SCIP's lower end is one ulp looser. Only the upper ends coincide, and only the upper end matters for the cutoff.
- Fix. Write: "Its upper end equals the tightest enclosure's upper end minus fl(0.343). SCIP's lower end is one ulp looser."

**C4. Several "at least" values are rounded up (lines 772, 777, 778, 1376, 1405, 1411, 1459; §9 CAMINO sentence).**

- Evidence (`margins_floor.log`):

  | quantity | exact value | dossier | safe floor |
  |---|---|---|---|
  | MINOTAUR margin | 3.1628485e-3 | "≥ 3.162849e-3" | 3.162848e-3 |
  | ANTIGONE margin | 1.55232195e-4 | "≥ 1.552322e-4" | 1.552321e-4 |
  | SCIP 9.2.1 deficit | 5.45888272e-2 | 5.458883e-2 | — |
  | QPLIB_3177 shift | 8.6990e-5 | "at least … 8.7e-5" (§9, §10) | 8.6e-5 or 8.69e-5 |
  | QPLIB_2703/3177 below bounds (§9) | 8.154e-6 / 3.272e-5 | "by 8.2e-6 and 3.3e-5" | "by more than 8.1e-6 and 3.2e-5" |
  | CAMINO | 4.335% / 7.487% / 80.60% | "4.3%, 7.5% and 81%" | — |

- D is an upper bound on the deficit, so its safe display rounds *up*. "Can lie up to 6.0e-7 and 2.4e-6" (line 1376) should read "cannot lie more than 6.1e-7 and 2.4e-6".
- Fix. Use floors for lower bounds and ceilings for upper bounds. The 5.1 table (≥ 3.162e-3, ≥ 1.552e-4) is already safe.

**C5. D(ε) is a proved upper bound on the deficit, not the "worst case" (lines 75, 500, 1136, 1201, 1376, 1449; title of Prop. 5).**

- Problem. Proposition 5 proves f ≥ v_ε. Attainment is not shown. The bound uses (1−ε)³ in δ although the radii range over [1, 2], so it is likely not tight.
- Fix. Write "87% of a proved upper bound D(ε) on the deficit, so the true worst case for ε = 1e-10 lies between 0.87 D and D". In S5's replacement sentence, write "by at most", not "by up to".

**C6. S16 misdiagnoses the flags (lines 1298–1306).**

- Problem. S16 says Lemma 1 needs an accurately evaluated objective and that "30 flags rest on printed solver objectives without a checked vector".
  - Lemma 1 applies to the returned vector including objvar. Its objective is the printed objvar level. So every flag whose margin exceeds the printing uncertainty is already a proof of non-feasibility, given correct transcription.
  - The "30" are exactly the 30 OSIL flags beyond printing that the campaign report already separates (plus 5 for R only and 1 within printing).
  - What a checked vector adds is the residual profile, not non-feasibility.
- Evidence. `inconsistencies.md`. Of the 36 returned-primal flags, 15 have 50-digit savepoint checks. 21 do not: 17 OSIL flags beyond printing, 3 KAN flags and pindyck/GUROBI.
- Fix. Drop S16, or rewrite it as: "17 OSIL flags beyond printing have no evaluated vector, so their residuals are unknown. Their non-feasibility follows from Lemma 1 as printed." The proposed counting rule is the existing classification.

**C7. S15's single rbb run cannot "decide" both low pair2236 claims (line 1295).**

- Problem. The target 55.6898 lies between the claims 55.689773 and 55.689858.
  - If rbb certifies φ ≥ 55.6898, the lower claim becomes a primal-side tolerance artifact (category A), and the higher claim is undecided.
  - If rbb fails, nothing is proved.
  - Refuting either claim as an invalid dual needs a point below it, not an rbb run.
- Fix.
  - Use two targets just above each claim, for example 55.68978 and 55.68987. Each one decides "optimum above the claim (category A)".
  - Add a local search near the witness for points below 55.689773 to test category B.
  - The cost is still minutes.

**C8. S1's proposed prior-work wording is wrong for camshape200 (lines 1146–1151).**

- Problem. The proposed wording is "already solved globally in floating point (Octeract; BARON 26.5.27 in our campaign)".
  - Octeract's only camshape200 entry is QPLIB_2480, the rounded copy. Its value and log are unavailable.
  - By the dossier's own Proposition 15(5), the copy's optimum exceeds the MINLPLib optimum by ≥ 9.8233e-6. That is 2.3e-6 relative, more than the 1e-6 gap. A 1e-6 closure of QPLIB_2480 is therefore not a 1e-6 closure of camshape200.
  - The BARON run is our own campaign, not prior work.
- Fix.
  - camshape100: "solved in floating point by Octeract (Bestuzheva et al.); exact optimum new".
  - camshape200: "unverifiable floating-point claim on a rounded copy whose optimum differs by ≥ 2.3e-6 relative. In our campaign, BARON 26.5.27 closes it to MINLPLib's 1e-6 convention in 23 s (category A). The exact optimum is new."
  - The rest of S1 is right.

**C9. Proposition 9(b) overstates its reach (line 592).**

- Problem. The dossier says the output is "self-inconsistent, independent of any choice of data semantics". The argument actually lives *inside* SCIP's ε-tolerance semantics on binary64 data. Proposition 9(c) shows that in the zero-tolerance binary64 reading, SCIP's fm336 dual (1.505 / 0.814) is *valid*: the optimum is ≥ 2.247. There, the error is an infeasible returned point declared optimal, which is the category-A pattern but with a large objective error.
- A second point. ε-feasible points below a valid dual are not by themselves a contradiction for floating-point solvers; BARON's camshape points are an example. What makes the SCIP case decisive is the size ratio: the witnesses violate SCIP's rounded rows by ≤ 2.9e-15, while the claims exceed them by 7.5e-4 to 9.43.
- Acceptance status. Acceptance was tested in 10.0.2 for all eight witnesses and in all four versions for fm336 only.
- Fix. Write: "Under SCIP's own tolerance semantics the output is self-inconsistent. SCIP accepts points whose values lie 7.5e-4 to 9.43 below the values it declares optimal, although their binary64 residuals are ≤ 2.9e-15. In the decimal reading SCIP's dual is invalid. In the zero-tolerance binary64 reading (fm336) the dual is valid but the returned point is infeasible and its value is not the optimum."

**C10. SCIP 9.2.1 ran a different input file (§1.4 table, line 230; Prop. 15(3), line 778).**

- Evidence. `QPLIB_2703.sci.excerpt.txt`: "read problem <cnonconvex/QPLIB_2703.lp.gz>", 799 variables and 800 constraints. It is an LP-format file with the objective in the objective function, not the `.gms` copy.
- Fix. Add a §1.4 row: "SCIP 9.2.1, QPLIB_2703: `.lp.gz`; equality with the `.gms` copy assumed." The margin of 5.46e-2 makes the assumption harmless for any faithful conversion. Also note that the point is a fracdiving incumbent at a time-limit stop, with gap 16.32%, not a claim.

**C11. The violation thresholds can be stated more sharply (lines 491–492, 503–504, interpretation of Prop. 15).**

- Evidence (`eps_check.log`): v_{2.5e-8}(QPLIB_2738) = −4.2842974 > −4.2843015, and v_{8e-9}(QPLIB_3177) = −4.2771732 > −4.27735.
- Fix. Any point that reaches ANTIGONE's value violates some row or bound by more than **2.5e-8**. Any point that reaches MINOTAUR's value violates one by more than **8e-9**. The dossier's 1e-8 and 1e-9 are true but weaker.

**C12. "Eight code bases agree" (Prop. 6 proof) overstates coverage.**

- Evidence. `spec_check.log` covers only p0/p4/p5/pair2236. `exact_check_all.log` covers the first six plus the unminimized fuzz variants. `indep_check`, `gams_check` (on `.gms`), `rv_cip_exact`, `rv_gms_exact`, `mycheck` and `cipchk` cover all eight.
- Fix. Write "each witness is confirmed by six to eight independent exact checkers".

**C13. Appendix provenance (line 1481).**

- `scan2.py` / `scan2.log` do not exist. The saved files are `C/r2/pattern_scan.py` and `pattern_scan.log`.
- `claims.log` came from an inline script that was not saved, so it cannot be regenerated.
- Fix. Rename the appendix entry. Save the inline script.

**C14. Proposition 14 wording "SCIP's own duals … are valid for R" (line 760).**

- Problem. SCIP 9.0.1's dual is a bound for the Pyomo model it solved, not for R. R is a relaxation, so a bound for the model does not transfer to R.
- Fix. Write "SCIP's reported values lie below min R; as duals of the exactly infeasible model they are trivially valid".

**C15. Notation (Prop. 3).** "Assume U_m(c) ≥ 0" should read U_m(c/2), or "the recurrence values U_m", consistent with Lemma 2.

## 3. Additional issues

**A1. S18's optional SCIP experiment does not test what it is meant to test, and a cheaper bound exists.**

- The listed SCIP duals on waterno2_01–04 are dated 15 Feb 2022 (`pages.json`). That is an older SCIP than the 10.x line in which the mechanism was traced. A 10.1.0 run with `varboundrelax = b` says nothing about those listed values.
- Other solvers' listed duals bound how wrong SCIP's could be, if those duals are valid:
  - waterno2_03: LINDO 115.0044602 against SCIP 115.0045167, so at most 5.7e-5;
  - waterno2_04: BARON 145.4394212 against SCIP 145.4397918, so at most 3.7e-4;
  - waterno2_01/02: several solvers agree.
- Resolution. State these bounds, with the stated assumption, and drop the 2 × 1 h run.

**A2. A cheap falsifiable test of the mechanism exists.**

- C2 predicts the following. If fm336's station 0 is changed from (0.7, 0.343) to (0.6, 0.216) or (0.85, 0.614125), with the speed-row coefficients adjusted consistently, every version should solve it correctly. The same holds for tiny2 with L = 0.6 or 0.85.
- This costs seconds of SCIP time, if the user authorizes solver runs. It is a stronger test than the `varboundrelax = b` correlation, and cheaper than S14's source build and 122-case scan.

**A3. S9's second assumption is likely moot, and no fetch is needed.**

- Default bounds. In the QPLIB_3177 log the order is: presolve, transformer (LinearHandler, QuadHandler), presolve. QPLIB_8803 stops with "Detected infeasibility" in the *first* presolve, before the transformer. The QuadHandler defaults therefore had not been applied.
- The rule is already saved in `P/literature/control/sources/QuadHandler_master_r2.cpp`, lines 184–240: the default is 100 × the most extreme finite bound, else ±1000. For optcdeg2 this gives lb −100 (smallest finite lb −1) and ub 1000 (largest finite ub 10).
- Resolution. Keep ".nl = .gms" as the only stated assumption. The default-bound remark can cite the log order and the source.

**A4. S3 is partly discharged.**

- The third implementation (sympy parse, row-presence check, iterated smoothing) agrees on all eight bounds to 20 digits.
- I re-derived Lemma 2 and Propositions 3 and 5 by hand.
- What remains is a process question: whether the user accepts this critic pass as the independent review, since it is also by an AI agent.
- The upgrade from "strong evidence" to proof for the QPLIB copies is computationally sound, modulo `.nl` = `.gms` (MINOTAUR) and `.lp` = `.gms` (SCIP 9.2.1).

**A5. The S8, S14 and S15 cost estimates are reasonable in time but misdirected in design.** See C7 and A1/A2. S3's computation took under 15 s here.

**A6. CAMINO status information is partial, not absent.**

- `using_amplpy.py` writes a result row only when AMPL's `solve_result` is "solved" or "limit". Other outcomes are recorded as FAILED.
- Resolution. Write "the CSV has no status column; the pipeline kept only runs AMPL labelled 'solved' or 'limit'". This does not change Proposition 13.

**A7. The S19 statement is plausible but unproved.**

- `P/minlplib-status/report.md` says the catmix certificates were not rerun on the `.gms` form.
- "No comparison below is sensitive to this" is plausible, given relative perturbations of 1e-16 against the 1.48e-9 flag, but no sensitivity bound is given.
- Resolution. Mark it as plausible; the flag is unchecked anyway.

**A8. S7 detail.** `report.prev.md` was never committed (`git log` is empty for that path). Its content equals the HEAD `report.md`, so cite that commit's `report.md`.

## 4. The dossier's own examination

| issue | assessment |
|---|---|
| S1 (major) | The substance is correct: BARON's duals are valid and within 1.23e-7 / 4.80e-7 relative. The camshape200 prior-work wording must change (C8). "87% of worst case" must change (C5). |
| S2 | Correct. Adopt C9's sharper three-reading statement. |
| S3 | Partly done (A4). The QPLIB_2738 part needs C1. |
| S4 | Correct for 2703/3177. Fix the 2738 sign (C1). |
| S5 | Correct diagnosis. Use "at most" (C5). |
| S6, S7, S10, S11, S12, S13, S17, S19, S20 | Agree. S7 detail in A8; S19 in A7. |
| S8 | Agree. 13.0.3 was listed by 9 Sep 2026; BARON 2026.5.28 by 28 May. |
| S9 | Weaker than stated (A3). |
| S14 | Agree with the scope. A cheaper test exists (A2). |
| S15 | Resolution wrong (C7). |
| S16 | Misdiagnosed (C6). |
| S18 | Count over-broad (C2). The experiment is misdirected (A1). |

"Nothing invalidates a claimed result" (§8.3) is confirmed.

## 5. Numbers confirmed (no change needed)

- Campaign:
  - 129 / 126 / 3 outcomes; finite duals 35/36/38 (91 OSIL + 18 R); returned primals 35/40/30;
  - 2 claims; 6 disclaimers; 6 tightened; 10 first-batch rows (ratios 0.9561–0.9811, the lowest ten of 117);
  - overruns 3706.37–3728.4 s with BARON CPU 3600.01–3601.65 s;
  - 5 listed-dual improvements; 36/38 flags on 39 pairs;
  - minimum margin 5.2581469e-7 (exact 5.2581469620e-7).
- BARON camshape100/200: Solution = Best possible = −4.28414764756144 (3 iterations, wall 0.46 s, resusd 0.45 s) and −4.27850228570019 (23.22 s). Residuals ≈ 1e-10 at e100/x1 and e200/x1.
- Proposition 3 bounds and Proposition 15(5) shifts 8.5394e-7 / 9.8233e-6 / 3.7766e-5 / 8.6990e-5 (floors).
- Lemma 8 residual table.
- Proofs of Proposition 7 (fm336 = 187/270; tiny2 = −1.337; 0.8 < 0.92280).
- Proposition 9(c) bound 2.247.
- tiny2 offset 9.575e-7.
- Proposition 11 rbb values 168.107652 / −6.731984 / −232.173990.
- MINLPLib S-mark text.
- CAMINO limits 32.63 / 19.24 / 212.66 s.
- KAN values and the 9.34e-7 / 9.99e-7 residuals.
- ANTIGONE log lines 206–209 and CONOPT 8.7007237331e-6.
- MINOTAUR 3177: 1 node, LB "inf", 2.89 s.
- 8803: 119 s, presolve infeasibility.
- waterno2_01–04 listings.
- Stale-line citations (summary 314; SYNTHESIS 417; closing 232; report 402/513).

## 6. Commands run (targeted, from `/tmp/crit_solv/` copies)

- `python3 indep_bound.py camshape{100,200,400,800}.gms QPLIB_{2738,2480,2703,3177}.gms` produced `indep_bound.log` in under 10 s.
- `python3 eps_check.py` produced `eps_check.log`.
- `python3 evalgms.py` produced `qplib_sol_eval.log`.
- `python3 enclosure.py` produced `enclosure.log`.
- `python3 strong_criterion.py waterno2_01 waterno2_06 waterno2_24 kall_ellipsoids_tc02b` produced `strong_criterion.log`. It reads the cached OSIL read-only.
- Inline `fractions` scripts produced the margins (`margins_floor.log`), Lemma 8 and the fm336/tiny2 checks. An inline `csv` script recounted the first batch, ratios, overruns and claims from a copy of `results_table.csv`.
- Read-only `grep`/`sed`/`cat` on the logs, reports, reviews, sources and literature files cited above, plus `git log`/`git diff --stat` on the solver-runs paths.

No project-wide checks were run, and CI was not consulted.
