Verdict: **revision required: no blockers, one major issue, four minor issues.** The headline counts, all 43 reported instance rows, the 19-pair refutation table, and the solver-campaign totals agree with the evidence. The requested second rocket proofs and exact GAMS/OSIL comparison reproduce. Three entries described as rigorous objective upper ends are rounded in the wrong direction; three stated numerical caps are too small. These corrections do not change the headline conclusions or class counts.

Paths below are relative to the repository root. `P` means `paper-open-minlplib`; `R` means `research-20260929`; `D` means `P/development`. Review date: 2026-10-04. The known stale hashes in `artifact/claims.json` were excluded from the findings, as requested.

1. **Major — three second-proof objective upper ends are rounded downward.**

   **Location:** `P/sections/E-audit.tex:292`, `:294`, `:300`; the caption at `:286` explicitly calls these entries upper ends, with truncations separately marked by an ellipsis.

   **Wrong text → correct text, retaining the existing decimal precision:**

   | Instance | Printed upper end | Outward upper end |
   |---|---:|---:|
   | glider100, p2 | −983842.2577881224 | **−983842.2577881223** |
   | methanol50, p4 | 0.0079302187992 | **0.0079302187993** |
   | nuclear14, p3 | −1.12968744117116 | **−1.12968744117115** |

   **Evidence:** `R/reviews/bound-audit-verification/logs/kraw_glider100.p2.json`, `kraw_methanol50.p4.json`, and `kraw_nuclear14.p3.json`, field `obj_hi`. Independently parsing those fields as fractions gives, respectively:

   ```text
   -37168509620875410572129648663 / 37778931862957161709568
   407787849209522638870562848971437134130116855810553934686973 /
     51422017416287688817342786954917203280710495801049370729644032
   -89503060179431832832201940465 / 79228162514264337593543950336
   ```

   The printed values fall below these upper ends by approximately 1.4500e−11, 4.0609e−14, and 3.3447e−15. Exact decimal ceilings give the corrected column. This is a presentation defect in a table of rigorous upper bounds: the stored second proofs remain valid, and the corrected displays still support every associated refutation and margin. The ghg_3veh entry is safely rounded upward.

2. **Minor — the binary64 witness-violation cap is too small.**

   **Location:** `P/sections/08-solvers.tex:54`.

   **Wrong text:** “in the binary64-rounded data their rows are violated by at most 2.9·10⁻¹⁵.”

   **Correct text:** “…by at most **2.93·10⁻¹⁵**” (or 3.0·10⁻¹⁵).

   **Evidence:** the four large witness/model pairs p0, p4, p5 and pair2236 in `R/publication/scip-bug/models/` and `witness/`. Exact evaluation with the decimal model coefficients confirms feasibility. Replacing coefficients by their exact binary64 values gives a maximum row violation of

   ```text
   32122061 / 10995116277760000000000
     = 2.921484428952681…e−15 > 2.9e−15.
   ```

   I checked all eight witnesses from copied inputs with `exact_check.py`; all are exactly feasible, and their tabled objective displays have the required direction. This correction does not affect the wrong-run verdicts.

3. **Minor — the methanol50 relative-coefficient-change cap is rounded downward.**

   **Location:** `P/sections/E-audit.tex:565`.

   **Wrong text:** “relative changes of at most 2.38·10⁻¹⁶.”

   **Correct text:** “relative changes of at most **2.39·10⁻¹⁶**.”

   **Evidence:** the rerun exact GAMS/OSIL comparison finds precisely 360 objective differences: one constant, 104 linear coefficients and 255 quadratic coefficients, with all 1,497 rows equal. Independently comparing the rational coefficients gives maximum relative change

   ```text
   1 / 4196280000000000 = 2.383063093978476…e−16.
   ```

   One coefficient attaining it is that of x597²: GAMS `314721/2500000000`, OSIL `12588840000000003/100000000000000000000`. The existing 2.38e−16 cap is strictly smaller. This does not alter the separate objective-difference bound used to transfer the refutation.

4. **Minor — the powerflow objective-enclosure-width cap is too small.**

   **Location:** `P/tables/tab-points.tex:20`; generating source `P/data/make_tables.py:1209`, fixed metadata `POINTS13`.

   **Wrong text:** “≤2.8·10⁻⁴².”

   **Correct text:** “**≤2.83·10⁻⁴²**” (or ≤2.9·10⁻⁴²). Correct the generating source and regenerate the table.

   **Evidence:** `R/publication/primal/powerflow/logs/certify.powerflow0039p.log` and `certify.powerflow0039r.log` already report widths near 2.82e−42. Reconstructing the objective interval from the copied proof boxes and OSIL data at the recorded 80-digit interval precision, and subtracting its dyadic endpoints exactly, gives:

   | Instance | Exact endpoint difference, approximately |
   |---|---:|
   | powerflow0030p | 2.2836141795583216e−42 |
   | powerflow0039p | 2.8208143336505333e−42 |
   | powerflow0039r | 2.820814333650795e−42 |

   For example, the exact width for powerflow0039p is `20414249065247698399153028003352421 / 7237005577332262213973186563042994240829374041602535252466099000494570602496`. Both case39 widths exceed the printed cap. The primal objective upper bounds themselves pass the outward-rounding checks.

5. **Minor — the description of automatic numerical verification overstates its scope.**

   **Location:** `P/sections/I-reproduction.tex:45`; the same overstatement appears in the introductory description in `P/data/make_tables.py:13`.

   **Wrong text:** “It checks every displayed number against its exact value in rational arithmetic.”

   **Correct text:** “It checks the certified bound, primal, gap and derived margin displays that it generates against their exact values in rational arithmetic; hand-written tables and fixed metadata require separate checks.”

   **Evidence:** the copied generator completes **673 checks with zero failures**, while reproducing the understated fixed width in issue 4. It does not read the hand-written second-proof table in `sections/E-audit.tex`, so it cannot detect issue 1. Regeneration agrees byte-for-byte with all existing generated tables. Passing this generator is useful evidence for its checked quantities, but does not establish the stated universal claim.

**Verified numerical evidence and coverage**

I inventoried all **56 table placements** across the two documents: 13 generated tables and 43 hand-written tables, including five longtables. I checked their provenance against the family certificates, point evidence, audit evidence, raw campaign records, dossier checks, claim metadata and recorded replay outputs. I also examined the numbers in main Sections 3, 7 and 8 and supplement S4 and S6, and compared their repeated counts with the abstract, conclusions, relevant tables and reproduction register. Apart from the issues above, I found no disagreement among the repeated counts. Historical solver versions, dates and times were checked against archived records; recorded times are not new performance measurements.

The independent instance-row check used `fractions.Fraction`, reading raw rational strings or converting stored binary64 endpoints to their exact fractions. It covered **all 43 instances**, exceeding the requested 30. It compared raw certificate and primal evidence with `numbers.json` and the rendered table values, checked minimization lower bounds downward and primal upper bounds upward, reversed these directions for maximization instance pricing050, checked gaps upward and water improvement factors downward. The first pass contained **470 checks with zero failures**. The extended pass contained **801 checks with zero failures for the checked contracts**; the unsafe displays/caps above were separately reported as findings, rather than included among those passing assertions.

The raw sources for those 43 rows were:

| Rows | Raw evidence used |
|---|---|
| lnts50–400 | `D/reviews/code/sol-lnts-review/certificate.json`, exact optimal brackets |
| dtoc5 | `D/reviews/code/sol-dtoc5-review/result.json` and `primal_exact.txt` |
| optcdeg2 | `R/reviews/bangbang-verification/logs/qcal_exact.json` and `primal_check.json` |
| lukvle10 | `R/reviews/closing-confirm-r2-checks/logs/lukvle10_lower_end.log`; `R/publication/primal/dtoc5-lukvle10/logs/lukvle10_enclose.json` |
| chain50–400 | `R/open-instances-wave2/cops/logs/chain*_bound.json`; `R/publication/primal/chain/points/chain*_box.json` |
| catmix100–800 | `R/publication/reproduction/cops/logs/exact_display_checks.json`, verifier duals and the documented primal policies |
| camshape100–800; hvycrash | `D/dossiers/checks/camshape/check_exact.json`; exact identity −437/2000 |
| ex6_2_5, ex6_2_7 | lower-end check log and `D/dossiers/primal-points-checks/logs/ex62_check.log` |
| etamac; pricing050 | `D/dossiers/small-checks/r2/{etamac_point,pricing_check}.log`, plus the etamac tangent lower bound |
| pindyck | `R/reviews/pindyck-review-checks/logs/primal_enclosure.txt`, including exact reconstruction of the penalty correction |
| powerflow0030p/0039p/0039r | stored SDP/branch-and-bound exact certificate bounds; `R/publication/primal/powerflow/logs/certify.*.log` |
| eg_int_s/eg_disc_s/eg_disc2_s | both route bounds in `D/dossiers/checks/eg/r2/logs/displays.log`; exact objective from the stored primal `.sol` |
| waterno2_06/09/12/18/24 | `certB_verify.json` or `cert_T_w1_impl.json`; `R/publication/primal/water-ann-kan/points/*.exact.json` |
| ann_cumene_tanh and six KAN rows | `R/publication/primal/water-ann-kan/points/*.point.json` |

For the remaining tables, the provenance checks included: the archived listed values and family verification logs in S1; the camshape constants, deficit and rounded-copy checks; the powerflow model/leaf/point records; the eg partition and rounding-audit outputs; water period/cell counts; KAN rerun results and infeasibility records; prior-status dossier assignments and the exact selection funnel; audit classes, inputs, second proofs, (i-r), emfl, rocket and history records; SCIP scan logs and exact witnesses; reproduction timings, claim-register entries and hash-prefix tables. The intentionally unsafe *old* displays in S8 were treated as examples to audit, not current certificate claims. The exact-arithmetic and Taylor-bound tables in S5 were compared with their defining formulas and stored check outputs.

**Audit recount**

I recomputed these counts from `R/bound-audit/results.json`, `pages.json` and `screen.json`, with exact arithmetic for the screen comparisons. A copied second HTML parser also reconstructed every page record from the archived HTML and agreed with all **1,633 pages, 2,816 points and 11,086 bounds** in `pages.json`.

| Quantity | Recomputed value |
|---|---:|
| Finite bounds; solver labels | 11,031; 19 |
| Page senses: minimization / maximization / none | 1,366 / 264 / 3 |
| Strictly screened bound–point triples | 158 |
| Screened instances / points / distinct instance–solver bounds | 46 / 56 / 131 |
| Screened triples involving “other points” | 110 |
| Display ties / instances | 3,851 / 1,133 |
| Class (i): bounds / instances | 19 / 15 |
| Class (i-r): bounds / instances | 12 / 4 |
| Proved valid: bounds / instances | 12 / 4 |
| Repairs: bounds / instances | 63 / 11 |
| Undecided: bounds / instances | 25 / 12 |
| Gross / tolerance-scale class (i) bounds | 11 / 8 |
| LINDO class (i) bounds | 13 |

The exact screen and tie sets agree with the stored sets, not merely their sizes. The class counts sum to 131 after choosing the strongest result per instance–solver bound. All 19 rows of `tab-audit-pairs` match the raw bound, point, date and class records; their displayed objective upper bounds are upward, and their margins and unit ratios are downward. The smallest exact margin/unit ratio is approximately **1.115843372866948**, safely above 10/9 and the printed lower value 1.115. The per-solver class table also agrees cell by cell. Adding the three rocket conflicts gives the stated **22 invalid bounds on 18 instances**, including **16 LINDO** bounds.

Further S4 checks reproduce the `.solu` aggregation for **589 entries: 422 exact matches and 167 within half a displayed unit**. The six/seven-significant-digit profile is **59/2** on 2013-09-17 and **263/471** on other dates. All 69 displayed OSIL hash prefixes in the two input/hash tables agree with the archived files.

**Open item 3: reruns reproduce**

I ran `D/dossiers/checks/audit-r2/rocket_kraw.py` for rocket100, rocket200 and rocket400 against copied models, point data and dependencies. Every Krawczyk inclusion test passed and the entire objective interval lay below the listed LINDO bound. The outward 13-decimal brackets reproduce:

```text
rocket100  [-1.0128320069151, -1.0128320069130]
rocket200  [-1.0128356770698, -1.0128356770677]
rocket400  [-1.0128365294843, -1.0128365294821]
```

Their maximum inclusion ratios were approximately 0.00010931985, 0.00011048747 and 0.00010996731. The pinned-thrust/mass counts reproduce as **76/64, 151/127 and 315/254**.

The copied exact-forms comparison reproduces **23 identical models** and the documented methanol50 exception: all 1,497 rows and variable data equal, with 360 objective-coefficient changes. Thus the statement “14 of the 15 class (i) instances,” plus three rockets, four emfl instances, spring and eniplac, is supported. I also reran the three negative controls: a 1e−13 coefficient perturbation in sssd20-04persp produces one differing row; a 1e−13 spring bound perturbation produces one variable-bound mismatch; a 1e−13 change in an exponential argument in ghg_3veh produces one differing row. Only filesystem paths were adapted to the copied inputs.

**Solver-campaign recount**

From `R/publication/solver-runs/results.csv`, independently joined to exact certificate bounds:

| Quantity | Recomputed value |
|---|---:|
| Outcomes | 129 = 43 instances × 3 solvers |
| Valid bound outcomes: BARON / Gurobi / SCIP | 43 / 43 / 40 = 126 |
| Finite duals: BARON / Gurobi / SCIP | 35 / 36 / 38 = 109 |
| Finite duals: OSIL / KAN descriptive comparisons | 91 / 18 |
| Certificate-consistent closures | 0 |
| Instances with an improved best listed dual | 5 |
| Returned values beyond a certificate / printed incumbents beyond a certificate | 36 / 38 |
| Union of flagged instance–solver pairs | 39 |
| Returned values beyond trace precision: OSIL / KAN | 30 / 5 |
| Returned points with stored all-row evaluations | 15 |

All 109 finite duals remain weaker than the applicable rigorous bound, including an allowance for their printed precision. BARON's two camshape optimality claims are rejected by the exact optima. The five improved instances are camshape100/200/400 (BARON), lnts200 (Gurobi) and waterno2_18 (SCIP). The one additional returned value, Gurobi/pindyck, lies beyond the certificate but within trace printing precision, as disclosed.

The caveats reproduce: **six BARON globality disclaimers; six SCIP domain-tightened outcomes; ten evaluator-overload warnings (4 BARON, 3 Gurobi, 3 SCIP); three SCIP memory failures; nine capability failures (8 BARON, 1 SCIP); one Gurobi power-expression failure**. The six tightened bounds are included among finite outcomes but are properly marked as referring to a modified model. The 75 SCIP scan-summary records match the seed-count footers or raw GAMS run records, and all eight witness objective displays agree with exact evaluation.

Other repeated counts agree: **31 closures**, of which **9 exact** and **11 additional relative gaps ≤3.00e−13**; the largest exact relative gap is approximately **3.0890035771634647e−9**, safely displayed as ≤3.09e−9; **12** closures have a listed-bound deficit above half the primal magnitude. The six structural classes total **15+4+3+5+1+3 = 31**. The prior-status partition is **7+8+16 = 31**; evidence levels for closures are **10 rerun, 11 stored, 9 hand+stored, 1 hand**. The selection funnel reproduces **1,633 → 1,257 → 596 → 360 → 294 → 155**, with **29 closures and 12 other instances** inside the last set, two closures outside, and the subsequent **11/9/146/32** selection accounting. The claim index has **66 entries**, consistent with **27 register rows plus 39 reported-value rows**; stale index hashes were not tested as current evidence.

**Targeted commands and limits**

Every repository script was executed from a copy under **`/tmp/sol-numbers.gymIP0`**. No repository script was run in place. Runs used at most four CPU cores (`taskset -c 0-3` where applicable), with numerical-library thread counts set to one. No project-wide verification or CI inspection was performed. The paper was not edited and no commits were made.

The targeted commands actually run were the copied `data/make_tables.py`, `data/make_campaign_table.py`, `data/make_points_table.py`; reviewer `independent.py` and `extra.py`; `rocket_kraw.py 100`, `200`, `400`; the copied exact-form `drive.py` and `drive_fn.py ghg_3veh glider100 rocket100 rocket200 rocket400 methanol50`, followed by the three perturbed-input controls; copied `step4_pages.py`; and copied `D/eg-audit/compare_audit.py`. Additional inline Fraction/interval checks independently calculated the methanol coefficient maximum and the three powerflow widths. All 13 regenerated table files match the repository files byte-for-byte.

The eg stored-output comparison passed for **1,234,542 leaves** and **63,017,129,222 exponential/power results**, with zero violations. This verifies the saved result coverage and comparisons; it is **not** a fresh computation of all 63 billion operations. Full solver campaigns and all family search trees were not rerun. Logs and reviewer code are in the temporary directory (`generator.log`, `independent.log`, `extra.log`, `width-check.log`, `eg-compare.log`, and `reruns/`).
