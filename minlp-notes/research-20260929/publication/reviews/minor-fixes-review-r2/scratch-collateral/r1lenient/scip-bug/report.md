<!-- Written to disk by the root from the structured return value of author of track scip-bug in workflow wf_2951b32d-9f3 (the harness blocks subagents from writing report files). -->

# SCIP wrong-optimal-value finding: reproduction, proof, root cause, minimal reproducers

Track: scip-bug. Dates: 2026-10-01 to 2026-10-02. Folder:
`/workspace/minlp-notes/research-20260929/publication/scip-bug/`. Paths below are relative to this folder unless they are absolute.

Three agents worked on this track. Two were cut off by usage limits.
- **First author** (wf_6b4c8c17): most of the reproduction, witnesses, debug build, traces, toggles and minimal models. Its report draft was never written to disk; it was recovered from its transcript.
- **Second author** (wf_a89a60b6): built SCIP master, ran master scans, wrote `indep_check.py` and `pair_semantics.py`, reran the original reproducers, and fuzzed with master.
- **Third author** (this report): checked the GAMS models exactly and built the minimized all-version reproducer `min/fm336_v1010.cip`. Also built a debug-solution build of master, traced it, ran the p4 small-excess check, merged everything and drafted the upstream report.

Nothing was posted or sent anywhere. The upstream report at the end is a draft only.

## 1. Summary

- **Reproduced in every version and interface tested.**
  - PySCIPOpt 6.2.1 (SCIP 10.0.2 wheel).
  - Official binaries of SCIP 10.0.2, 10.0.3 and 10.1.0 (10.1.0 is the newest release).
  - GAMS 54.3.1 with SCIP 10.0.3.
  - A local build of SCIP master, 11.0.0-dev, commit a01de2c (2026-10-02). It was still the newest master commit at about 19:30 EDT on 2026-10-02.
  - Both original reproducers rerun with the same claims and node counts as their September logs:
    - `open-instances-wave2/waterno2/scip_unreliable.py` (periods 0, 4, 5 of waterno2_06);
    - `sepbranch/check_fail.py` (cert2 record 2236, the seed-dependent cell pair).
- **Proved wrong.** For each model there is an exactly feasible point (a "witness") whose objective value is strictly below every wrong "optimal" claim.
  - The proof uses exact rational arithmetic. Four checkers share no code and do not use SCIP (Section 4).
  - One checker reads the GAMS `.gms` files, so the GAMS/SCIP claims are refuted on the GAMS models themselves.
  - The wrong claims exceed the witness values by 7.5·10⁻⁴ to 9.43.
- **Root cause, traced.** SCIP's debug-solution mechanism was used in a 10.0.2 debug build and in a master debug build. In every instrumented wrong run listed in Section 5.3, the first step that loses the witness is the same:
  - The `default` nonlinear handler's reverse propagation declares a node infeasible.
  - The constraint is s³ − p = 0. A binary has forced s to its lower bound L, and p has been fixed to its lower bound L³.
  - The expression's activity is [−1.665·10⁻¹⁶, −5.55·10⁻¹⁷]; the required interval is [0, 0].
  - The trigger is a binary64 rounding residual. 0.7³ = 0.343 holds in decimal, but in binary64 fl(0.7)³ − fl(0.343) = −9.237·10⁻¹⁷.
  - With the default `constraints/nonlinear/varboundrelax = r`, fixed variables are not relaxed, and `SCIPintervalPropagateWeightedSum` intersects intervals exactly. Together these turn the residual into a cutoff.
  - With `varboundrelax = b`, 0 of 122 runs are wrong. Under default settings, 78 of those 122 runs were wrong. The raw-log recount includes the two later small-excess p4 checks missing from the older scan CSV (`logs/minor_review_check.log`).
- **Seed-dependent case** (cell pair; claims 55.69 or 65.12): it is a **real error, not a tolerance effect**.
  - The witness is exactly feasible with value 55.689908. That is 9.43 below 65.12, and 0.80 below master's wrong claim 56.492.
  - It has the same cause: a strong-branching child on 10.0.2, a tree node on master.
- **Minimal reproducers:**
  - `min/fm336_v1010.cip` (new): 15 variables, 12 rows. It is wrong with **default settings** in every interface and version tested, in all seeds tried (10/10 or 5/5). It is solved at the root.
  - `minimal/tiny2.cip`: 3 variables, 2 rows. It is wrong in all versions with heuristics and separation switched off.
  - An upstream bug report is drafted in the last section. It was not submitted.

## 2. Versions and builds tested

| label | how obtained | version string |
|---|---|---|
| wheel 10.0.2 | PySCIPOpt 6.2.1 (installed; newest on PyPI, checked 2026-10-02) | SCIP 10.0.2 [optimized], SoPlex 8.0.2, Ipopt 3.14.19; no PaPILO |
| bin 10.0.2 | official `scipoptsuite-10.0.2-glibc2_34-amd64.tgz` | SCIP 10.0.2 [b8eaf989f9], SoPlex 8.0.2, PaPILO 3.0.0 |
| bin 10.0.3 | official release binary | SCIP 10.0.3 [d409edf9f6], SoPlex 8.0.3, PaPILO 3.0.1 |
| bin 10.1.0 | official release binary (2026-09-18, newest release) | SCIP 10.1.0 [c8e5737a84], SoPlex 8.1.0, PaPILO 3.0.2, Ipopt 3.14.20 |
| GAMS/SCIP | GAMS 54.3.1 (installed) | SCIP 10.0.3 (d409edf9f6) |
| dbgsol 10.0.2 | source 10.0.2, Release, `-DDEBUGSOL=on`, no PaPILO/GMP, plus diagnostic patch `debug-instrumentation.patch` | SCIP 10.0.2 [b8eaf989f9], SoPlex 8.0.2, Ipopt 3.14.19 (conda-forge) |
| master | `git clone --depth 1` of scipopt/scip and scipopt/soplex master; Release; no PaPILO (`build/build_master.sh`) | SCIP 11.0.0 [GitHash a01de2c, 2026-10-02T10:14Z], SoPlex 9.0.0 [996f032], Ipopt 3.14.19 |
| master dbgsol | same source, `-DDEBUGSOL=on`, plus `debug-instrumentation-master.patch` (`build/build_master_dbgsol.sh`) | SCIP 11.0.0 [a01de2c] |

Notes:
- Platform: Ubuntu 24.04.4 LTS on WSL2, x86-64, gcc 13.3.0, cmake 3.28.3.
- The official binaries need `libpcre2-posix.so.3`, taken from the Ubuntu package `libpcre2-posix3` (unpacked locally, no root).
- `cons_nonlinear.c` on master was last changed on 2026-06-14. `intervalarith.c`, `nlhdlr_default.c`, `expr_sum.c` and `expr_pow.c` were last changed in January 2026 (GitHub API, checked 2026-10-02).
- The master debug build reproduces the master Release build's claims exactly in all six seeds compared.

## 3. Reproduction

### 3.1 Model files

`export_models.py` (first author) writes each subproblem as a JSON spec, a CIP file and a GAMS file:
- The same variable order, row order and row splitting are used as in the original model builder (`open-instances-wave2/waterno2/period.py`).
- All numbers are exact decimals: OSIL data, and `repr` of the float objective coefficients.

| file | model |
|---|---|
| `models/p0.cip`, `p4.cip`, `p5.cip` | single-period Lagrangian subproblems of waterno2_06 (wave-2 report, Section 5) |
| `models/pair2236.cip` | cert2 record 2236: period 3 of waterno2_06 on one entry/exit cell pair (the seed-dependent case) |
| `minimal/tiny2.cip` | 3 variables, 2 rows (first author, hand-made) |
| `minimal/pumps_default.cip` | 20 variables, 12 rows (first author, fuzzed then minimized) |
| `min/fm336_v1010.cip` | 15 variables, 12 rows (third author; fuzzed against master by the second author, minimized against 10.1.0) |
| `min/fm318_master.cip` | 10 variables, 8 rows; wrong on master only |

PySCIPOpt on the CIP files gives the same claims and node counts as the original runs:
- p0: 169.950327 (820 nodes);
- p4: −5.723535 (1625 nodes);
- p5: −229.759028 (893 nodes);
- pair2236 with seed shift 7: 65.123993 (194 nodes).

### 3.2 Wrong runs per version

A run counts as WRONG if it reports `optimal` with a dual bound above the exact witness value plus 10⁻⁴. All runs use default settings with only `randomization/randomseedshift` varied, except tiny2. Entries are wrong runs / seeds. Source: `logs/scan_summary.csv` (`summarize_scans.py`, which reads all scan logs).

| model (witness value) | wheel 10.0.2 | bin 10.0.2 | bin 10.0.3 | bin 10.1.0 | master a01de2c | GAMS/SCIP 10.0.3 | dbgsol 10.0.2 |
|---|---|---|---|---|---|---|---|
| p0 (168.108652) | 4/20 | 4/10 | 4/10 | 2/10 | 0/10 | 3/3 | – |
| p4 (−6.730644) | 19/20 | 8/10 | 8/10 | 10/10 | 9/10 | 10/10 | 8/10 |
| p5 (−232.172853) | 13/20 | 4/10 | 4/10 | 5/10 | 4/10 | 1/3 | – |
| pair2236 (55.689908) | 7/30 | 8/30 | 8/30 | 5/30 | 5/30 | 1/10 | 4/30 |
| pumps_default (0.612) | 20/20 | 10/10 | 10/10 | 10/10 | **1/20** | 0/5 | wrong (seed 0, traced) |
| **fm336** (187/270 ≈ 0.692593) | **10/10** | **10/10** | **10/10** | **10/10** | **10/10** | **5/5** | **10/10** |
| fm318 (729/500 = 1.458) | 0/10 | 0/10 | 0/10 | 0/10 | 10/10 | 0/5 | 0/10 |
| tiny2, heuristics and separation off (−1.337) | wrong | wrong | wrong | wrong | wrong | wrong | wrong |

Wrong claims by model (smallest wrong claim, then largest wrong claim, with the excess over the witness):

| model | smallest wrong claim (excess) | largest wrong claim (excess) |
|---|---|---|
| p0 | 169.950250 (1.84), GAMS | 169.950685 (1.84), bins |
| p4 | −6.729889 (7.5·10⁻⁴), bins 10.0.2/10.0.3 seed 3 | −4.646232 (2.08), wheel |
| p5 | −231.905843 (0.267), master | −228.343114 (3.83), GAMS |
| pair2236 | 56.492038 (0.802), master | 65.124528 (9.43), bins |
| pumps_default | 1.19800 (0.586) | 1.19800 (0.586) |
| fm336 | 0.814125 (0.122), master | 1.505213 (0.813), all |
| fm318 | 2.0 (0.542) | 2.0 (0.542) |
| tiny2 | −1.231084 (0.106) | −1.231084 (0.106) |

Remarks:
- 10.0.2 and 10.0.3 binaries follow identical paths: same claims and node counts.
- Master is right on p0 and nearly always right on pumps_default (1/20). That is why fm336, which fails everywhere, is the reproducer to report.
- GAMS/SCIP takes other paths: its models have an objective variable and a GAMS start point. It solves pumps_default and fm318 correctly, but fm336 is wrong in 5/5 seeds.
- tiny2 with default settings is solved correctly by every version (−1.337).
- Both SCIP master and 10.1.0 accept the fm336 witness when it is read from a `.sol` file before solving. They report "1/1 feasible solution given by solution candidate storage, new primal bound 6.925926e-01", then 0.692592587925926 as optimal. Without it they report 0.814125 (master, seed 0) and 1.50521312595154 (10.1.0) as optimal. Logs: `logs/cli_{master,10.1.0}_fm336_{readsol,default}.log`.

## 4. Proof that the claims are wrong

**Statement.** For each model file there is a point x* with:
- every row and every bound satisfied exactly, and binaries integral, with the file's decimal data read as exact rationals;
- objective value strictly below every wrong "optimal" claim listed in Section 3.

So the true optimum of the model as written is at most the witness value, and every listed claim is wrong.

**Checkers.** All four use exact rational arithmetic (`fractions.Fraction`), share no code, and do not use SCIP.

| checker | author | reads | log |
|---|---|---|---|
| `exact_check.py` | first | CIP files | `logs/exact_check_all.log`, `logs/exact_check_fuzz_master.log` |
| `spec_check.py` | first | JSON specs | `logs/spec_check.log` |
| `indep_check.py` | second (cases extended by third) | CIP files, own tokenizer | `logs/indep_check.log` |
| `gams_check.py` | third | the `.gms` files GAMS/SCIP solved; number literals parsed from their decimal text | `logs/gams_check.log` |

`gams_check.py` takes every claim GAMS/SCIP reported as optimal from `gams/logs/scan_*.txt`. A mutation test showed that it rejects perturbed witnesses: changing x995 by 10⁻³⁰, x546 by −10⁻³⁰, or b6 by 1/2 is detected.

| model | witness | exact objective | smallest wrong claim | objective − claim |
|---|---|---|---|---|
| p0 | `witness/p0.json` | 168.108652029808 | 169.950250085232 | −1.8416 |
| p4 | `witness/p4.json` | −6.730643699816 | −6.72988938834578 | −7.54·10⁻⁴ |
| p5 | `witness/p5.json` | −232.172853003462 | −231.905843299873 | −0.2670 |
| pair2236 | `witness/pair2236.json` | 55.689908409449 | 56.4920384487893 | −0.8021 |
| tiny2 | b = 0, s = 7/10, p = 343/1000 | −1337/1000 | −1.23108446311479 | −0.1059 |
| pumps_default | `minimal/pumps_default_witness.json` | 153/250 | 1.19799998144798 | −0.5860 |
| fm336 | `min/fm336_v1010.witness.json` | 187/270 | 0.814125 | −0.1215 |
| fm318 | `min/fm318_master.witness.json` | 729/500 | 2.0 | −0.5420 |

All checkers report "violated: none" and EXACTLY FEASIBLE / ALL CHECKS PASSED. `gams_check.py` refutes all 25 wrong GAMS/SCIP claims on the GAMS models. The unminimized `minimal/fuzz_master/fuzz_11_{318,336}.cip` are also covered by `indep_check.py`.

The fm336 witness can be checked by hand:
- pumps 0 and 1 off: b0 = b1 = 0, s0 = 7/10, p0 = 343/1000, s1 = 17/20, p1 = 4913/8000, q0 = q1 = w0 = w1 = 0;
- pump 2 on: b2 = 1, s2 = 2/3, p2 = w2 = 8/27, q2 = 1/2;
- objective 0.1 + 2·8/27 = 187/270.

**How the witnesses were built** (this does not matter for the proof):
- p0, p4 and p5 come from the earlier reviews (`vrepair.py`).
- pair2236 comes from `make_witness.py`: binaries fixed, other variables solved exactly from the equality rows.
- The small models were built by hand.

**Semantics caveat** (exact; `binary64_analysis.py`, `binary64_scip_solution.py`, `pair_semantics.py`):
- SCIP reads each decimal into the nearest double. Then a pump that is off at a station with speed bound 0.6, 0.7 or 0.85 is exactly infeasible. For example, s = fl(0.7) forces p = s³ < fl(0.343) = lb(p), a gap of 9.2·10⁻¹⁷.
- The witnesses violate the double-rounded rows by at most 2.9·10⁻¹⁵, far below SCIP's feasibility tolerance (10⁻⁶).
- SCIP accepts the witnesses as feasible:
  - `checkSol` in PySCIPOpt 10.0.2 accepts the first six (`logs/checksol_witness.log`);
  - master and 10.1.0 accept the fm336 witness when it is read as a solution file.
- The examined SCIP "optimal" solutions are not exactly feasible for the binary64 data either (pumps_default, p0 seed 0, tiny2, and pair2236 seeds 0 and 7). They also use pump-off configurations that a strict binary64, zero-tolerance reading would forbid:
  - pair2236, seed shift 7, claim 65.12: b35 = 0 (station 0.85 off). Its rows are violated by up to 8.9·10⁻⁷ in exact binary64 arithmetic (`logs/pair_semantics.log`).
  - fm336: SCIP's incumbent has b0 = 0, s0 = 0.7, p0 ≈ 0.343.

  So no consistent reading of the model makes SCIP's answers right. The claims are wrong for the decimal model and wrong under SCIP's own tolerance-based notion of feasibility.

## 5. Root cause

### 5.1 Method

The debug builds set the witness as debug solution (`misc/debugsol`). SCIP then reports the first reduction or cutoff that removes the witness. The diagnostic patch adds the source of each such step: constraint handler, propagator, strong-branching child, and the nonlinear handler with its intervals.
- The first author wrote the patch for 10.0.2 (`debug-instrumentation.patch`).
- The third author ported it to master (`debug-instrumentation-master.patch`; two `solve.c` hunks were ported by hand).

A 10.0.2 run with `SCIP_DEBUG` and `DEBUG_PROP` in `cons_nonlinear.c` gave a step-by-step trace for tiny2 (`logs/tiny2_debugprop.log`).

### 5.2 Mechanism (tiny2, 10.0.2 trace)

The model is: min 0.2 b − 2.4 s + p subject to p = s³ and s − 0.3 b ≤ 0.7, with b ∈ {0,1}, s ∈ [0.7, 1], p ∈ [0.343, 1].

SCIP branches on b at the root. At node 2 (b = 0):
1. Linear propagation fixes s = fl(0.7).
2. Nonlinear propagation, round 0:
   - The outward-rounded activity of s³ is [0.34299999999999986, 0.34299999999999997].
   - Reverse propagation of s³ − p ∈ [0, 0] gives p ≤ 0.34299999999999997. This is 5.5·10⁻¹⁷ below lb(p) = fl(0.343) = 0.34300000000000003.
   - SCIP accepts this within tolerance and fixes p = fl(0.343).
3. Nonlinear propagation, round 1:
   - s and p are both fixed. Under the default `varboundrelax = r`, the relaxation is min(ε·max(1,|b|), 0.001·(ub − lb)), which is 0 for fixed variables.
   - The auxiliary variable of the constraint is fixed at [0, 0].
   - The default nlhdlr calls the sum's reverse propagation (`reversepropSum`, `expr_sum.c:977` on master), which calls `SCIPintervalPropagateWeightedSum`.
   - That function intersects exactly (`SCIPintervalIntersect`, `intervalarith.c:4793` on master). The intersection [fl(0.343)] ∩ [0.34299999999999986, 0.34299999999999997] is empty, so the node is reported infeasible.
   - The node b = 0, which contains the optimum, is cut off, and b ≥ 1 becomes global. SCIP reports −1.2311 as optimal.

In step 2 SCIP treats the 5.5·10⁻¹⁷ discrepancy as feasible; in step 3 it treats the same discrepancy as infeasible. Most intersections in `cons_nonlinear.c` and `nlhdlr_default.c` use the epsilon-tolerant `SCIPintervalIntersectEps`, but this one is exact.

### 5.3 Every instrumented wrong run listed here loses the witness at the same step

In every instrumented run in the table, the first "debugging solution was cut off" or invalid bound comes right after a "declared INFEASIBLE" from the `default` nlhdlr's reverse propagation:
- the expression is x³ − y, with x fixed at fl(L) and y fixed at fl(L³), at a station with L = 0.7;
- the activity is [−1.6653·10⁻¹⁶, −5.5511·10⁻¹⁷] and the propagation bounds are [0, 0].

| build | model, seed shift (claim) | where the witness is lost | log |
|---|---|---|---|
| dbgsol 10.0.2 | tiny2, heur+sepa off (−1.2311) | node 2 (b = 0) cut off; b ≥ 1 global | `logs/dbgsol_tiny2.log` |
| dbgsol 10.0.2 | pumps_default, 0 (1.198) | b1 = 0 fixed at the root (reduced-cost fixing; `propagating/redcost/freq = −1` avoids it), then the root is declared infeasible | `logs/dbgsol_pumps_default.log` |
| dbgsol 10.0.2 | **fm336, 0 (1.5052)** | the root (depth 0) is declared infeasible on s0³ − p0; the incumbent 1.5052 (b0 = 0, b1 = b2 = 1) is returned | `logs/dbgsol_fm336_v1010.log` |
| dbgsol 10.0.2 | pair2236, 8 (65.1235) | strong branching on b47 at node 2: the down child (contains the witness) is "infeasible" on x545³ − x993; relpscost sets b47 ≥ 1 | `logs/dbgsol_sb_pair2236_seed8.log`, `logs/dbgsol_expr_pair2236_seed8.log` |
| dbgsol 10.0.2 | p4, 0 (−5.7235) | node 1282 (depth 9) cut off, x546³ − x995 | `logs/dbgsol_expr_p4_seed0.log` |
| dbgsol 10.0.2 | p5, 0 and 2 | nodes 536 and 660 cut off, x547³ − x997 | `logs/dbgsol_expr_p5_seed*.log` |
| dbgsol 10.0.2 | p0, 2 | node 328 (depth 7) cut off, x542³ − x987 | `logs/dbgsol_expr_p0_seed2.log` |
| master dbgsol | **fm336, 0 (0.814125)** | root declared infeasible on s0³ − p0, right after the feasjump heuristic found 0.814125 | `logs/mdbg_fm336_s0.log` |
| master dbgsol | fm318, 0 (2.0) | root declared infeasible on −p0 + s0³ | `logs/mdbg_fm318_s0.log` |
| master dbgsol | pumps_default, 3 (1.198) | root declared infeasible on s1³ − p1 | `logs/mdbg_pumps_default_s3.log` |
| master dbgsol | tiny2, heur+sepa off (−1.2311) | node 2 (depth 1) cut off on s³ − p; b ≥ 1 global | `logs/mdbg_tiny2_hsoff.log` |
| master dbgsol | pair2236, 14 (56.4920) | node #6 (depth 2) cut off on x545³ − x993; then the invalid global bound b23 ≥ 1 | `logs/mdbg_pair2236_s14.log` |
| master dbgsol | p4, 0 (−5.7235) | strong branching at node #298: the down child of b48 (contains the witness) is "infeasible" on x546³ − x995 in probing; b48 ≥ 1 | `logs/mdbg_p4_s0.log` |
| master dbgsol | p5, 3 (−230.8802) | node #902 (depth 9) cut off on x547³ − x997 | `logs/mdbg_p5_s3.log` |

Seed 11 is not instrumented: `logs/dbgsol_pair2236_seed11.log` first reports an invalid local implication b35 ≥ 1 at node 2 with no recorded constraint or propagator source, then b47 ≥ 1. b35 belongs to the 0.85 station. Its first witness loss is untraced and cannot be assigned to the 0.7-station mechanism.

The root cutoffs (fm336, fm318, pumps_default) start the same way:
1. An incumbent is found.
2. Valid propagation fixes a pump binary to 0 (objective propagation or reduced-cost fixing).
3. Speed and power are then fixed, and the next nonlinear propagation round declares the root infeasible.
4. SCIP returns the incumbent as optimal.

In fm336 the node declared infeasible contains SCIP's own incumbent, which also has b0 = 0.

**The data trigger is exact** (`logs/binary64_analysis.log`, `logs/indep_check.log`). The residuals fl(L)³ − fl(L³) are:
- L = 0.6: −2.15·10⁻¹⁷;
- L = 0.7: −9.24·10⁻¹⁷;
- L = 0.8: +7.46·10⁻¹⁷;
- L = 0.85: −8.01·10⁻¹⁷.

The squares behave the same way. Every waterno2 period has stations with L = 0.6, 0.7 and 0.85, and a pump that is off forces s = L. All traced cutoffs involve the 0.7 station, which has the largest residual.

### 5.4 Component toggles

Each row is default settings plus one change, run in the PySCIPOpt 10.0.2 wheel with seeds 0–4. Logs: `logs/toggles_fm336.log`, `logs/toggles_pumps_default*.log`. These are diagnostics, not proposed fixes; some changes only alter the search path.

| change | fm336 wrong | pumps_default wrong |
|---|---|---|
| none (default) | 5/5 (1.5052) | 5/5 (1.198) |
| `propagating/maxrounds = 0` and `maxroundsroot = 0` | 0/5 | 0/5 |
| `constraints/nonlinear/propfreq = −1` | 0/5 | 0/5 |
| `constraints/nonlinear/maxproprounds = 0` | 0/5 | 0/5 |
| `constraints/nonlinear/varboundrelax = a`, `b` or `n` | 0/5 each | 0/5 each |
| `varboundrelaxamount = 1e-6` | 5/5 | 0/5 |
| `conssiderelaxamount = 1e-6` | 5/5 | 5/5 |
| `propauxvars = FALSE` | 5/5 | 5/5 |
| `propagating/obbt/freq = −1` | 5/5 | 5/5 |
| `propagating/redcost/freq = −1` | 5/5 | 0/5 (removes the trigger) |
| `propagating/rootredcost/freq = −1` | 5/5 | 5/5 |
| probing off | 5/5 | 0/5 |
| `branching/relpscost/maxproprounds = 0` | 5/5 | 5/5 |
| `conflict/enable = FALSE` | 5/5 | 5/5 |
| `misc/usesymmetry = 0` | 5/5 | 5/5 |
| `presolving/maxrestarts = 0` | 5/5 | 5/5 |
| `numerics/feastol = 1e-9` | 0/5 | 0/5 |
| `numerics/epsilon = 1e-12` | 5/5 | 5/5 |

tiny2 with heuristics and separation off (`logs/tiny2_settings.log`):
- Wrong under `varboundrelax = r` (default), `varboundrelaxamount = 1e-6`, `conssiderelaxamount = 1e-6`, `propauxvars = FALSE`, `feastol = 1e-9` and `epsilon = 1e-12`.
- Right under `varboundrelax = n`, `a` or `b`, nonlinear `propfreq = −1`, `maxproprounds = 0`, and `propagating/maxrounds = 0`.

On master, fm336 with `varboundrelax = n` gives no infeasibility report and the right value 0.692593 (`logs/mdbg_fm336_vbrn_s0.log`). **Why `n` avoids the cutoff, although it does not relax fixed variables either, was not determined.**

The only changes that remove the error in all three small models switch off nonlinear propagation or change how it relaxes variable bounds.

### 5.5 Relaxing fixed domains removes every wrong claim

`constraints/nonlinear/varboundrelax = b` relaxes all bounds by ε, including fixed ones. Results:

| runs | wrong with default settings | wrong with `varboundrelax = b` |
|---|---|---|
| wheel: p0, p4, p5 seeds 0–9, pair2236 seeds 0–29 (`logs/seedscan_vbr_b_*.log`) | 27/60 | 0/60 |
| master: every wrong run of p4, p5, pair2236 and pumps_default, plus p4 seed 5 (`logs/master_vbr_b_*.log`) | 19/20 | 0/20 |
| fm336 and fm318, seeds 0–9, on master and 10.1.0 (`logs/fm_scan.log`) | 30/40 | 0/40 |
| the two p4 small-excess runs (bin 10.0.2 seed 3, bin 10.1.0 seed 4; `logs/p4_smallexcess_vbr_b.log`) | 2/2 | 0/2 |
| total | 78/122 | 0/122 |

The wheel's claims under this setting agree with the witnesses within tolerance. This is numerical evidence that the untraced wrong runs (wheel, binaries, GAMS) have the same cause. It does not prove that each of them takes exactly this path.

### 5.6 Two p4 claims with small excess (not traced)

Two p4 runs are wrong by only 7.5·10⁻⁴ and 8.9·10⁻⁴:
- bins 10.0.2/10.0.3, seed 3: −6.729889;
- bin 10.1.0, seed 4: −6.729754.

The first was inspected (`logs/p4_bin1002_s3_solution.log`). SCIP's solution has b6 = 1 and b12 = 0; the witness has b6 = b12 = 1. So a subtree with a different pump configuration was lost; this is not a tolerance effect. Both runs become correct with `varboundrelax = b`. Neither the 10.0.2 debug build nor master produces these claims (`logs/p4_dbgsol_master_scan.log`), so they were not traced.

## 6. The seed-dependent case (cell pair, cert2 record 2236)

SCIP 10.0.2 (wheel) reported `optimal` at:
- 55.689858 with no propagation;
- 55.689773 with default settings;
- 65.123993 with default settings and seed shift 7.

Master reports 56.492038 in 5 of 30 seeds.

- **Real error or tolerance effect?** A real error. The reasons:
  - `witness/pair2236.json` is exactly feasible with value 55.689908409449. That is 9.43 below 65.12 and 0.80 below 56.49, far beyond any tolerance.
  - SCIP's own checker accepts the witness.
  - SCIP's 65.12 solution itself relies on tolerances: b35 = 0, and rows violated by up to 8.9·10⁻⁷ in exact binary64 arithmetic.
- **The low claims are not refuted.** 55.689773 and 55.689858 lie 5·10⁻⁵ to 1.4·10⁻⁴ below the witness. SCIP's points violate rows by up to 1.5·10⁻⁸ and bounds by up to 8.9·10⁻⁸ (`logs/pair_semantics.log`). They are consistent with tolerance effects or with the witness not being optimal; the cause and validity of those lower claims are not established.
- **True optimum.** It lies in [55.0942, 55.689908]:
  - the lower end is rbb's certified bound for the same subproblem (cert2 retry record 5539: same multipliers and cell boxes, status certified);
  - the upper end is the witness.
- **Cause.** The same propagation defect:
  - 10.0.2: strong-branching child b47 = 0 declared infeasible (instrumented seed 8). Seed 11's first loss is untraced, as noted in Section 5.3;
  - master: node #6 cut off (seed 14).

  A hypothesis, supported by instrumented seeds 8 and 14, is that seed failure depends on whether the search reaches a pump-off node of the 0.7 station along a path where p is fixed by propagation before s³ − p is propagated again. This happens in 4 to 8 of 30 seeds per version.
- **Original reproducer.** `sepbranch/check_fail.py logs/cert2.pkl 2236` still gives 65.123993 with seed shift 7 (`logs/orig_check_fail_2236.log`).

## 7. Consequences for the paper

Suggested wording, supported by the files above:

> SCIP 10.0.2, 10.0.3, 10.1.0 and the development version (master, 2026-10-02) report wrong optimal values on waterno2 period subproblems: up to 3.8 above exactly feasible points; on one cell-pair subproblem 9.4 above, for some random seeds. The same happens through PySCIPOpt and GAMS. The cause is in SCIP's nonlinear domain propagation. The decimal data satisfy 0.7³ = 0.343, but after rounding to binary64, fl(0.7)³ < fl(0.343) by 9.2·10⁻¹⁷. When a pump is off, its speed and power variables become fixed to these values, and reverse propagation declares the node infeasible. A 15-variable model reproduces the error with default settings in every version tested.

Points to keep:
- Our certified bounds never used SCIP's bounds.
- The MINLPLib SCIP dual bounds listed for waterno2 lie far below our certified bounds, so they are not contradicted. The defect could in principle make a listed SCIP bound too high on instances with this data pattern; this was not examined.
- Say that a report is planned or filed only if the user files one.

## 8. What is proved, what is numerical, what is not done

**Proved** (exact rational arithmetic, four independent checkers, no SCIP):
- All eight witnesses (p0, p4, p5, pair2236, tiny2, pumps_default, fm336, fm318) are exactly feasible for their CIP files. The five that GAMS/SCIP solved wrongly, and fm318, are also exactly feasible for their `.gms` files.
- Their objective values lie strictly below every wrong claim (Sections 3 and 4).
- In binary64, fl(L)³ ≠ fl(L³) for L = 0.6, 0.7, 0.85 and 0.8. The residuals are negative for 0.6, 0.7 and 0.85.
- The examined SCIP solutions (pumps_default, p0 seed 0, tiny2, and pair2236 seeds 0 and 7) are not exactly feasible for the binary64 data. This was not checked for every solution in the scan tables.

**Numerical** (solver output, evidence only): all SCIP claims, node counts, version and seed tables, toggles, `varboundrelax = b` experiments, and the debug-build traces (they show what SCIP computed in those runs).

**Not done, or limits:**
- No fix was written or tested in source. The pointers in Section 5.2 are where the trace leads, not a verified fix.
- Why `varboundrelax = n` avoids the cutoff is not explained.
- The wheel, official binaries and GAMS cannot be instrumented. Their wrong runs are tied to the mechanism by Section 5.5 only. The 10.0.2 debug build has no PaPILO and takes other paths than the binaries.
- The two small-excess p4 claims (Section 5.6) were not traced.
- The true optima of p0, p4, p5, pumps_default and fm318 were not certified here; the witnesses are upper bounds. The first author states that the earlier rbb certificates bound p0, p4 and p5 from below within 10⁻³ of the witnesses; this author did not re-verify that.
- The earlier note that switching presolving off makes SCIP crash was not re-examined.
- Delta debugging of `models/p4.cip` was stopped after 59 tests (first author). The minimizer found little to remove from fm336 (13 → 12 rows) and fm318 (9 → 8 rows).
- Issue search on github.com/scipopt/scip (queries "varboundrelax", "wrong optimal nonlinear", "reverse propagation infeasible", "cutoff nonlinear propagation"; some queries hit the API rate limit) found nothing matching. Issue #22, "SCIP 8 incorrectly reports a second-order cone program as infeasible" (closed 2022), is a similar kind of error, but nothing shows that it has the same cause. Review r1 also found [#162, Suboptimal solution for multilinear relations](https://github.com/scipopt/scip/issues/162) (opened August 2025; developer discussion points toward orbitopal symmetry handling) and [#190, Presolving renders problem infeasible](https://github.com/scipopt/scip/issues/190) (February 2026, SCIP 10.0.1; discussion concerns coefficients near 1e-6). Both are related nonlinear wrong-result reports but apparently have different causes; neither establishes a match to this defect. Bodies and developer comments were checked through the GitHub API for this revision. Other channels were not searched.

## 9. Files

| path | content |
|---|---|
| `PROGRESS.json` | state for successors |
| `export_models.py` | writes `models/*.{json,cip,gms}` from the waterno2 data |
| `exact_check.py`, `spec_check.py`, `indep_check.py`, `gams_check.py` | exact feasibility proofs (no SCIP) |
| `make_witness.py`, `cip2spec.py` | witness construction; CIP to spec for the minimizer |
| `binary64_analysis.py`, `binary64_scip_solution.py`, `pair_semantics.py` | exact binary64 analysis of the data and of SCIP's solutions |
| `checksol_witness.py` | SCIP's own check of the witnesses |
| `run_scip.py`, `seed_scan.py`, `toggles.py` | PySCIPOpt runs |
| `run_binary.py` | official binaries, `dbgsol` (10.0.2 debug build) and `master` |
| `summarize_scans.py` | merges all scan logs into `logs/scan_summary.csv` and `logs/scan_summary.txt` |
| `minimize.py`, `scip_worker.py`, `minimal/fuzz.py` | delta debugging and fuzzing (`ORACLE=` selects a binary) |
| `min/fm336_v1010.{cip,json,witness.json,witness.sol}`, `min/dbg_fm336.set` | **main reproducer**, default settings, all versions |
| `min/fm318_master.*` | master-only reproducer |
| `minimal/tiny2.cip`, `tiny2_witness.{json,sol}`, `repro_tiny.py` | 3-variable reproducer (heuristics and separation off) |
| `minimal/pumps_default.cip`, `pumps_default_witness.{json,sol}`, `repro_pumps.py` | 20-variable reproducer (10.x default) |
| `minimal/fuzz_master/` | 8 fuzz candidates found with master; exact witnesses for 318 and 336 |
| `minimal/fuzz_out/`, `minimal/variants/`, `min/fz*` | earlier fuzz and minimization outputs |
| `models/`, `witness/` | waterno2 models; exact witnesses (`*.sol` for debug runs) |
| `gams/` | GAMS models (including `fm336.gms`, `fm318.gms`), scripts and logs |
| `debug-instrumentation.patch`, `debug-instrumentation-master.patch` | local diagnostic patches (not for upstream) |
| `build/build_master.sh`, `build/build_master_dbgsol.sh` (+ `.log`) | master builds |
| `logs/` | all run logs named in this report |
| `.gitignore` | ignores `build/ src/ install/ conda-env/ tmp/ venv/ *.tgz *.tar.gz` (about 1.4 GB) |

## 10. Commands actually run

All solver runs used OMP_NUM_THREADS = 1 and at most 2 concurrent processes. Only targeted checks were run: no project-wide checks, and CI was not consulted.

**Third author (this session), from the track folder:**
- Read predecessor transcripts with a Python JSONL parser. Recovered the first author's report draft (transcript line 892).
- `python3 gams_check.py` → `logs/gams_check.log`, exit 0. Then an inline mutation test of `gams_check.check` (3 perturbations, all rejected).
- `setsid nohup logs/fuzz_master_scan.sh` (PID 816098): `run_binary.py minimal/fuzz_master/fuzz_11_K.cip W master,10.1.0 0-9` for 8 candidates → `logs/fuzz_master_scan.log`.
- Exact witnesses written for fuzz_11_318 and fuzz_11_336. Then `python3 exact_check.py minimal/fuzz_master/fuzz_11_{318,336}.cip ... {2.0,1.5051}` → `logs/exact_check_fuzz_master.log`.
- `python3 cip2spec.py ... fm318` and `... fm336`.
- Minimizations, both finished in seconds:
  - `ORACLE=master WORKERS=1 python3 minimize.py fm318 '{}' 0,1,2,3,4 5 min/fm318_master` (PID 817875);
  - `ORACLE=10.1.0 WORKERS=1 python3 minimize.py fm336 '{}' 0,1,2,3,4 5 min/fm336_v1010` (PID 817877).
- `setsid nohup logs/fm_scan.sh` (PID 820436): `run_binary.py` on `min/fm318_master.cip` and `min/fm336_v1010.cip` for master, 10.1.0, 10.0.3, 10.0.2 and dbgsol, seeds 0–9, default and `varboundrelax=b`; then `seed_scan.py` (wheel) → `logs/fm_scan.log`.
- `SCIPBUG_SB=1 SCIPBUG_EXPR=1 build/dbgsol-10.0.2/bin/scip -s dbg_fm336.set -c "read fm336_v1010.cip" -c optimize -c "display solution" -c quit` → `logs/dbgsol_fm336_v1010.log`.
- `python3 toggles.py min/fm336_v1010.cip 0.692592592593 5` → `logs/toggles_fm336.log`.
- Master debug build:
  - `rsync` of master source to `src/scip-master-dbgsol`;
  - `patch -p1 < debug-instrumentation.patch` (2 `solve.c` hunks failed and were ported by a Python edit);
  - `diff -ru` → `debug-instrumentation-master.patch`;
  - `setsid nohup build/build_master_dbgsol.sh` (PID 822528; cmake `-DDEBUGSOL=on`, `make -j2 scip`) → `build/build_master_dbgsol.log`, BUILD_DONE.
- `setsid nohup logs/master_dbgsol_runs.sh` (PID 831142) → `logs/mdbg_*.log`, summary `logs/master_dbgsol_runs.out`.
- GAMS: `python3 -c "export_models.write_gms(...)"` → `gams/fm336.gms`, `gams/fm318.gms`; then `gams/scan_gams.sh fm336 0.692592592593 0 1 2 3 4` and `gams/scan_gams.sh fm318 1.458 0 1 2 3 4`.
- `python3 indep_check.py` (fm cases added) → `logs/indep_check.log`, exit 0.
- `python3 summarize_scans.py` → `logs/scan_summary.{csv,txt}`.
- p4 small-excess checks:
  - `install/10.0.2/.../scip -s tmp/p4s3.set -c "read models/p4.cip" -c optimize -c "display solution"` → `logs/p4_bin1002_s3_solution.log`;
  - `run_binary.py models/p4.cip -6.730643699816 10.0.2 3 constraints/nonlinear/varboundrelax=b` and the same for `10.1.0 4` → `logs/p4_smallexcess_vbr_b.log`;
  - `run_binary.py models/p4.cip -6.730643699816 dbgsol,master 0-9` → `logs/p4_dbgsol_master_scan.log`.
- Witness acceptance and default claims on fm336, for master and 10.1.0: `scip -c "read fm336_v1010.cip" -c "read fm336_v1010.witness.sol" -c optimize` and `scip -c "read fm336_v1010.cip" -c optimize -c "display solution"` → `logs/cli_{master,10.1.0}_fm336_{readsol,default}.log`.
- Read-only web: GitHub API for master commits and per-file last commits, issue search (5 queries) and issue #22; the PyPI JSON for PySCIPOpt.

**Second author** (from its transcript):
- `git clone --depth 1` of scip and soplex master; `build/build_master.sh`.
- Minimal models on master (`logs/cli_master_*.log`).
- `logs/master_scans.sh`; `python3 indep_check.py`; `python3 pair_semantics.py`.
- Original reproducers: `scip_unreliable.py` → `logs/orig_scip_unreliable.log`; `check_fail.py logs/cert2.pkl 2236` → `logs/orig_check_fail_2236.log`.
- `run_binary.py models/pair2236.cip 55.689908409449 dbgsol 0-29`.
- `ORACLE=master python3 minimal/fuzz.py 400 11 fuzz_master` → `logs/fuzz_master_s11.log`.
- `logs/master_vbr_b.sh`.

**First author** (from its report draft): downloads and builds (release binaries, conda Ipopt, 10.0.2 source with `-DDEBUGSOL=on` and patch steps), `export_models.py`, `make_witness.py`, `exact_check.py`, `spec_check.py`, the binary64 scripts, `checksol_witness.py`, `run_scip.py`, `seed_scan.py` (20 or 30 seeds), `run_binary.py` (10.0.2, 10.0.3, 10.1.0), CLI runs of tiny2 and pumps_default, `toggles.py`, debug-build traces with `addr2line`, GAMS runs and scans, fuzzing and minimization.

**Background jobs:** none are left running. Every job listed above was waited for, and a final process check showed no process of this track.

---

## upstream-report-draft.md (content)

> DRAFT, not submitted. For the user to review and file, for example as a GitHub issue at scipopt/scip or by email to the SCIP team. Attach `min/fm336_v1010.cip` (as `fm336.cip`), `min/fm336_v1010.witness.sol` (as `fm336_opt.sol`), `minimal/tiny2.cip` and `minimal/tiny2_witness.sol`.

**Title:** Wrong "optimal solution found" on small MINLPs: nonlinear reverse propagation cuts off a node because of a 1e-16 binary64 rounding residual (s fixed at 0.7, p fixed at 0.343, p = s^3)

**Versions affected.** All versions tested:
- SCIP 10.0.2: PySCIPOpt 6.2.1 wheel, and the official `scipoptsuite-10.0.2-glibc2_34-amd64` binary;
- SCIP 10.0.3: official binary, and through GAMS 54.3.1;
- SCIP 10.1.0: official binary;
- master a01de2c (2026-10-02), built locally with SoPlex master 996f032 and Ipopt 3.14.19.

Platform: Ubuntu 24.04 x86-64, gcc 13.3.

**Reproducer 1 (default settings, 15 variables).** File `fm336.cip`:

```
STATISTICS
  Problem name     : fm336_reduced
  Variables        : 15
  Constraints      : 12
OBJECTIVE
  Sense            : minimize
VARIABLES
  [binary] <b0>: obj=0, original bounds=[0,1]
  [continuous] <s0>: obj=0, original bounds=[0.7,1]
  [continuous] <p0>: obj=0, original bounds=[0.343,1]
  [continuous] <q0>: obj=0, original bounds=[0,1]
  [continuous] <w0>: obj=5, original bounds=[0,1]
  [binary] <b1>: obj=0.2, original bounds=[0,1]
  [continuous] <s1>: obj=0, original bounds=[0.85,1]
  [continuous] <p1>: obj=0, original bounds=[0.614125,0.614125]
  [continuous] <q1>: obj=0, original bounds=[0,1]
  [continuous] <w1>: obj=1, original bounds=[0,1]
  [binary] <b2>: obj=0.1, original bounds=[0,1]
  [continuous] <s2>: obj=0, original bounds=[0.6,1]
  [continuous] <p2>: obj=0, original bounds=[0.216,1]
  [continuous] <q2>: obj=0, original bounds=[0,0.5]
  [continuous] <w2>: obj=2, original bounds=[0,1]
CONSTRAINTS
  [nonlinear] <cube0>: -1*<p0> +1*<s0>*<s0>*<s0> == 0;
  [linear] <speed0>: +1<s0> -0.3<b0> <= 0.7;
  [linear] <flow0>: +1<q0> -3<s0> -0.3<b0> <= -2.1;
  [linear] <pow0>: +1<w0> -1<p0> -1<b0> >= -1;
  [linear] <speed1>: +1<s1> -0.15<b1> <= 0.85;
  [linear] <flow1>: +1<q1> -2<s1> -0.3<b1> <= -1.7;
  [linear] <pow1>: +1<w1> -1<p1> -1<b1> >= -1;
  [nonlinear] <cube2>: -1*<p2> +1*<s2>*<s2>*<s2> == 0;
  [linear] <speed2>: +1<s2> -0.4<b2> <= 0.6;
  [linear] <flow2>: +1<q2> -3<s2> -0.3<b2> <= -1.8;
  [linear] <pow2>: +1<w2> -1<p2> -1<b2> >= -1;
  [linear] <demand>: +1<q0> +1<q1> +1<q2> >= 0.5;
END
```

Run: `scip -c "read fm336.cip" -c optimize -c "display solution" -c quit`

Observed: "problem is solved [optimal solution found]" after 1 node.
- 10.0.2, 10.0.3 and 10.1.0: dual bound 1.50521312595154 for every `randomization/randomseedshift` in 0–9.
- master: 0.814125 (8 of seeds 0–9) or 1.50521312595154 (2 of them).
- GAMS/SCIP 10.0.3: 1.50521312595154 for seeds 0–4.

Expected for the exact decimal model: the optimum is 187/270 = 0.6925925…, attained at:
- b0 = 0, s0 = 0.7, p0 = 0.343, q0 = 0, w0 = 0;
- b1 = 0, s1 = 0.85, p1 = 0.614125, q1 = 0, w1 = 0;
- b2 = 1, s2 = 2/3, p2 = w2 = 8/27, q2 = 0.5.

The exact optimum follows by cases: all pumps off violates demand; b1 = 1 costs at least 0.814125 and b0 = 1 at least 1.715; otherwise b2 = 1, q2 ≥ 0.5 and s2 ≥ 2/3 force cost at least 187/270. The point above attains it.

This point satisfies every constraint exactly in rational arithmetic; for example, (2/3)³ = 8/27 and 0.7³ = 0.343. SCIP accepts it:

`scip -c "read fm336.cip" -c "read fm336_opt.sol" -c optimize`

prints "1/1 feasible solution given by solution candidate storage, new primal bound 6.925926e-01" and then reports 0.692592587925926 as optimal. This was checked on master and on 10.1.0 by the author, and on 10.0.2 and 10.0.3 by review r1 (`../reviews/scip-bug-r1/rv_runs.log`).

**Reproducer 2 (3 variables, heuristics and separation off).** File `tiny2.cip`:

```
STATISTICS
  Problem name     : tiny2
  Variables        : 3
  Constraints      : 2
OBJECTIVE
  Sense            : minimize
VARIABLES
  [binary] <b>: obj=0.2, original bounds=[0,1]
  [continuous] <s>: obj=-2.4, original bounds=[0.7,1]
  [continuous] <p>: obj=1, original bounds=[0.343,1]
CONSTRAINTS
  [nonlinear] <cube>: -1*<p> +1*<s>*<s>*<s> == 0;
  [linear] <speed>: +1<s> -0.3<b> <= 0.7;
END
```

Run: `scip -c "set heuristics emphasis off" -c "set separating emphasis off" -c "read tiny2.cip" -c optimize -c "display solution" -c quit`

Observed (all versions above, master included): optimal −1.23108446311479 with b = 1.

Expected for the exact decimal model: the optimum is exactly −1.337 at b = 0, s = 0.7, p = 0.343. For b = 1, minimizing 0.2 − 2.4s + s³ on [0.7, 1] gives 0.2 − 1.6√0.8 > −1.337. These exact case comparisons are recorded in `logs/minor_review_check.log`. With default settings SCIP returns −1.337.

**What happens.** We traced this with a `-DDEBUGSOL=on` build: the optimal point as debug solution, plus printf instrumentation in `cons_nonlinear.c`. In tiny2, at node 2 (b = 0):
1. `speed` fixes s = fl(0.7) = 0.69999999999999996.
2. Nonlinear propagation, first round:
   - The activity of s³ is [0.34299999999999986, 0.34299999999999997].
   - Reverse propagation of s³ − p ∈ [0, 0] gives p ≤ 0.34299999999999997, which is below lb(p) = fl(0.343) = 0.34300000000000003 by 5.5e-17.
   - The bound change is accepted as within tolerance, and p is fixed to 0.34300000000000003.
3. Next round:
   - s and p are both fixed. With the default `constraints/nonlinear/varboundrelax = r`, the relaxation min(eps·max(1,|bnd|), 0.001·(ub − lb)) is 0 for fixed variables.
   - The constraint's auxiliary variable is fixed at [0, 0].
   - The `default` nlhdlr calls `reversepropSum`, which calls `SCIPintervalPropagateWeightedSum` with activity [−1.6653e−16, −5.5511e−17] and rhs [0, 0].
   - The exact `SCIPintervalIntersect` (intervalarith.c:4793 on master) gives an empty interval, so the function sets `*infeasible`.
   - The node is cut off, and SCIP's debug check reports "debugging solution was cut off in local node #2" followed by "invalid global lower bound: b >= 1".

So the same 5.5e-17 discrepancy is treated as feasible in round 1 and as infeasible in round 2. The cause is that fl(0.7)³ − fl(0.343) = −9.24e−17 in binary64, although 0.7³ = 0.343 in decimal. 0.6/0.216 and 0.85/0.614125 behave the same way.

In `fm336.cip` the same infeasibility report appears at the root (depth 0), on s0³ − p0:
1. The heuristics find an incumbent: 0.814125 on master, 1.505 on 10.x.
2. Propagation then fixes b0 = 0 (validly), so s0 = 0.7 and p0 = 0.343.
3. The next nonlinear propagation round declares the root infeasible, and the incumbent is returned as optimal.

The node declared infeasible contains SCIP's own incumbent, which also has b0 = 0, s0 = 0.7 and p0 ≈ 0.343.

**Settings** (fm336, PySCIPOpt 10.0.2, seeds 0–4):
- These avoid the wrong result: `constraints/nonlinear/varboundrelax = a`, `b` or `n`; `constraints/nonlinear/propfreq = -1`; `constraints/nonlinear/maxproprounds = 0`; `propagating/maxrounds = 0` together with `maxroundsroot = 0`; `numerics/feastol = 1e-9` (for fm336 only; tiny2 is still wrong).
- These do not: `varboundrelaxamount = 1e-6`, `conssiderelaxamount = 1e-6`, `propauxvars = FALSE`, `numerics/epsilon = 1e-12`, switching off obbt, redcost, rootredcost or probing, `conflict/enable = FALSE`, `misc/usesymmetry = 0`, and `presolving/maxrestarts = 0`.

We did not find out why `varboundrelax = n` avoids it. Review r1 proposed an untested explanation: without bound relaxation in round 0, the activity already misses zero, so an epsilon-tolerant intersection may retain a singleton residual rather than [0,0]. Later reverse propagation then has a different right-hand side. This is a hypothesis, not a tested fix.

Related reports checked: [SCIP #162](https://github.com/scipopt/scip/issues/162) (multilinear suboptimal result, discussion points toward orbitopal symmetry) and [SCIP #190](https://github.com/scipopt/scip/issues/190) (false presolve infeasibility with small coefficients). They appear to have different causes; no common cause was established.

**Possible direction** (only a suggestion; we have not tested a fix): most intersections in `cons_nonlinear.c` and `nlhdlr_default.c` use `SCIPintervalIntersectEps`, but the intersection in `SCIPintervalPropagateWeightedSum` is exact. Another option is to relax fixed variables and fixed auxiliary variables by epsilon in mode `r`.

**Impact.** We found this while computing bounds for decomposed subproblems of the MINLPLib instance waterno2_06. On those 166-variable subproblems SCIP's "optimal" values were too high by up to 9.4 (about 17 %), depending on the random seed. We can provide those models (CIP and GAMS) if useful.

## Response to review

Review: `../reviews/scip-bug-review-r1.md`. Checked and resolved on 2026-10-03.

| issue | resolution and evidence |
|---|---|
| 1. Inconsistent totals | Raw-log recount confirms 0/122 with b, versus 78/122 for matched default cases. Corrected the headline; the old CSV omits two later p4 tests. |
| 2. Uninstrumented seed 11 | Restricted the trace table to seed 8 and all common-mechanism claims to instrumented runs; recorded seed 11's first b35 implication and 0.85-station caveat. |
| 3. Low pair claims | Reworded as not refuted and consistent with either tolerance effects or a nonoptimal witness; retained the certified optimum interval. |
| 4. Seed-failure explanation | Labelled the search-path explanation as a hypothesis supported by instrumented seeds 8 and 14. |
| 5. All-solution binary64 overclaim | Restricted the exact binary64 feasibility statement to the five examined solutions in the summary of proof claims. |
| 6. Related upstream issues | Read #162/#190 and developer comments; added links and apparently different causes in Section 8 and the unsubmitted draft. |
| 7. Draft consistency and exact optima | Matched the inline CIP name fm336_reduced to the attachment; gave exact case proofs for fm336 and tiny2; added r1 witness acceptance on 10.0.2/10.0.3. The optional n explanation in the draft is explicitly labelled an untested hypothesis. |

Targeted check: `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 research-20260929/publication/scip-bug/minor_review_check.py > research-20260929/publication/scip-bug/logs/minor_review_check.log` (from the repository root). Results are in `logs/minor_review_check.log`. No main computation, solver campaign, project-wide verification or CI check was run for this revision.
