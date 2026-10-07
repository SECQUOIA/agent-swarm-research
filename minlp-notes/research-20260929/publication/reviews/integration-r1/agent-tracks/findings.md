# Track-statement check (helper agent, read-only), saved by the lead reviewer

The helper agent could not write report files; the lead saved the substance of its returned report here.
Scripts: count_solver.py (solver campaign recount), sub-eg-repro/ (eg leaf count, manifest staleness),
sub-ir-status/ (audit-ir, slack floor, status, listings). All read saved data only, exact Fraction arithmetic.

Confirmed: 129 kept outcomes / 43 instances; 126 pass the rule; 3 SCIP memory stops (ex6_2_5, ex6_2_7, pindyck);
only 1/1 statuses are BARON camshape100/200 (5.258e-7 and 2.053e-6 below the certified optima); 109 finite duals
(BARON 35, GUROBI 36, SCIP 38), all weaker than the certificates (91 vs OSIL, 18 vs R); globality warning on exactly
catmix100/200/400/800, dtoc5, optcdeg2 -> 103 without; six SCIP tightened rows (etamac, ex6_2_5, ex6_2_7, hvycrash,
lukvle10, pindyck); first batch = dtoc5, optcdeg2, waterno2_24 x 3 solvers + kan_r3_h1_n9/BARON; settings 3600 s,
optca=optcr=1e-9, one thread; versions BARON 26.5.27, GUROBI 13.0.2, SCIP 10.0.3 (d409edf9f6).
eg-recheck: 38 chunk logs give 1,114,361 certified leaves, 0 failures, 1,152,830 processed boxes, 41,151 CPU-s.
SCIP: 3 of 5 examined claims refuted; 10.0.2/10.0.3/10.1.0/master a01de2c; not submitted.
audit-ir: 12 pairs (eniplac 3, lop97icx 1, spring 5, stockcycle 3); counts 35(18)/38/46; floor 0/158 screened, 17 ties.
minlplib-status: refresh 2026-10-02, 69 instances unchanged; ghg_3veh 3 rounded constants.

Problems reported (lead spot-checked 1, 2, 9, 13): see integration-review-r1.md issues 2, 3, 6-12.
