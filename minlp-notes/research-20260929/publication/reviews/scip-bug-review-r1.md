<!-- Written to disk by the root from the structured return value of verifier round 1 of track scip-bug in workflow wf_2951b32d-9f3 (the harness blocks subagents from writing report files). -->

# Review of track scip-bug, round 1

Reviewer folder: `/workspace/minlp-notes/research-20260929/publication/reviews/scip-bug-r1/`. Everything I ran there uses my own code. Nothing imports the track's checkers, and the exact checks do not use SCIP.

**Verdict: verified.** I found no blocker or major issue, and seven minor issues (listed at the end). The SCIP wrong-optimal-value finding is reproduced and refuted with exact arithmetic by independent code. The root-cause evidence (debug-solution traces, settings toggles, SCIP source) supports the report's description, with one overstated trace row.

## 1. What I checked independently

### 1.1 Exact feasibility of the witnesses (own code, exact rationals, no SCIP)

**CIP files.** `rv_cip_exact.py` is my own CIP parser. It reads every decimal literal as an exact `Fraction`. It checks every variable's bounds, binary integrality, every row exactly, and computes the objective exactly. Log: `rv_cip_exact.log`.

| model | witness | violations | exact objective | smallest wrong claim | obj − claim |
|---|---|---|---|---|---|
| models/p0.cip | witness/p0.json | 0 | 168.108652029808 | 169.950250085232 | −1.8416 |
| models/p4.cip | witness/p4.json | 0 | −6.73064369981647 | −6.72988938834578 | −7.54e−4 |
| models/p5.cip | witness/p5.json | 0 | −232.172853003462 | −231.905843299873 | −0.2670 |
| models/pair2236.cip | witness/pair2236.json | 0 | 55.689908409449 | 56.4920384487893 | −0.8021 |
| minimal/tiny2.cip | tiny2_witness.json | 0 | −1337/1000 | −1.23108446311479 | −0.1059 |
| minimal/pumps_default.cip | pumps_default_witness.json | 0 | 153/250 | 1.19799998144798 | −0.586 |
| min/fm336_v1010.cip | fm336_v1010.witness.json | 0 | 187/270 | 0.814125 | −0.1215 |
| min/fm318_master.cip | fm318_master.witness.json | 0 | 729/500 | 2.0 | −0.542 |

- **Mutation test** (`rv_mutation.log`): five random continuous p4 witness entries perturbed by 1e−30, and b6 set to 1/2. All six are rejected.
- **Smallest wrong claims.** I re-derived them from the raw scan logs with my own parser and my own witness values (`rv_tally.py`, see 1.4). They match the report's table in Section 4.

**GAMS models.** `rv_gms_exact.py` is my own parser for the GAMS subset used. Log: `rv_gms_exact.log`.
- For all eight `.gms` files (p0, p4, p5, pair2236, tiny2, pumps_default, fm336, fm318), the model is exactly identical to the corresponding CIP file: same variables, types, bounds, objective coefficients, and every row as a polynomial with exact rational coefficients.
- Every witness is exactly feasible for its `.gms` model.
- So the GAMS/SCIP claims are refuted on the GAMS models themselves.

**Models against the cached OSIL.** `rv_osil_crosscheck.py` reads `~/.cache/minlplib/minlplib/osil/waterno2_06.osil` with exact rationals: linear, quadratic and `power` terms. Log: `rv_osil_crosscheck.log`.
- For p0, p4, p5 and pair2236, each of the 203 rows is an exact copy of the same-named OSIL row. Rows with suffixes `_lo`/`_up` are the corresponding side of the OSIL row.
- No OSIL row whose variables all lie in the period's variable set is missing.
- Variable bounds equal the OSIL bounds. In pair2236, 17 bounds are tighter: these are the cell box.
- pair2236's objective coefficients equal `lam_in`/`lam_out` of cert2 record 2236.
- So the CIP models are genuine waterno2_06 period restrictions with a Lagrangian objective.

**Binary64 residuals** (`rv_binary64.py`). fl(L)³ − fl(L³) is −2.15e−17 for 0.6, −9.24e−17 for 0.7, +7.46e−17 for 0.8 and −8.01e−17 for 0.85. This matches the report.
- The tightest double enclosure of fl(0.7)³ has upper end 0.34299999999999997. That is the double just below fl(0.343), a gap of 5.55e−17.
- So even a tightest enclosure misses p = fl(0.343). This matches the traced activity [−1.665e−16, −5.55e−17].

**True optima of fm336 and tiny2 are exact, not just upper bounds** (short hand proof; the report only says "at most").
- fm336:
  - All pumps off is infeasible: q0, q1, q2 ≤ 0, but the demand row needs a total of at least 0.5.
  - b1 = 1 costs at least 0.2 + 0.614125.
  - b0 = 1 costs at least 5·0.343.
  - Otherwise b2 = 1 and q2 ≥ 0.5, so s2 ≥ 2/3 and the cost is at least 0.1 + 2·8/27 = 187/270.
- tiny2: with b = 1, the minimum over s ∈ [0.7, 1] of 0.2 − 2.4s + s³ is −1.2311 > −1.337. So the optimum is exactly −1.337.

### 1.2 Reproduction (own runs, sequential, one thread)

**Official binaries and master** (`rv_runs.sh` → `rv_runs.log`). Version banners checked: 10.0.2 b8eaf989f9 / SoPlex 8.0.2 / PaPILO 3.0.0; 10.0.3 d409edf9f6; 10.1.0 c8e5737a84 / Ipopt 3.14.20; master 11.0.0 a01de2c / SoPlex 9.0.0 996f032.
- fm336, default settings, seeds 0–5:
  - 10.0.2, 10.0.3 and 10.1.0: 1.50521312595154, 1 node, in all seeds.
  - master: 0.814125 in seeds 0, 1, 2 and 5; 1.505213 in seeds 3 and 4. This matches the report's "8 of 10 / 2 of 10".
- fm336 witness read from the `.sol` file: all four versions print "1/1 feasible solution given by solution candidate storage, new primal bound 6.925926e-01" and finish at 0.692592587925926. This includes 10.0.2 and 10.0.3, which the report does not mention.
- fm336 with `varboundrelax = a`, `b` or `n`: correct (0.692593) on all four versions.
- tiny2: default settings give −1.337 (correct). With heuristics and separation off, every version gives −1.23108446311479 with b = 1. With `varboundrelax = b` added, every version gives −1.337.

**PySCIPOpt 6.2.1 wheel** (SCIP 10.0.2; `rv_wheel.py` → `rv_wheel.log`):
- fm336 is wrong in 10/10 seeds (1.505213).
- tiny2 with heuristics and separation off is wrong in 3/3 seeds; with default settings it is correct.
- SCIP's `checkSol` accepts the fm336, tiny2, p4, pair2236 and fm318 witnesses.

**GAMS 54.3.1 / SCIP 10.0.3** (`rv_gams.log`; I confirmed that the option file was read):
- fm336: 1.50521312595154 "Optimal" with no option file and with seed shift 3.
- tiny2 with heuristics and separation off: −1.2311 with b = 1. With default settings: −1.337.

**Toggles** (`rv_toggles.py` → `rv_toggles.log`; fm336, wheel, seeds 0–4). All 14 rows I ran agree with `logs/toggles_fm336.log`:
- 0/5 wrong: `propagating/maxrounds = 0` (with `maxroundsroot = 0`), nonlinear `propfreq = −1`, `maxproprounds = 0`, `varboundrelax = a`, `b` or `n`, and `feastol = 1e−9`.
- 5/5 wrong: `varboundrelaxamount = 1e−6`, `conssiderelaxamount = 1e−6`, `propauxvars = FALSE`, redcost off, `epsilon = 1e−12`, and conflict analysis off.

**Seed-dependent case** (`rv_pair2236.py` → `rv_pair2236.log`):
- Seed 0: 55.68977300185796 (29 nodes). Seed 7: 65.12399304921561 (194 nodes).
- SCIP's points: maximum row violation 1.496e−8 and 8.858e−7, maximum bound violation 8.943e−8 and 6.308e−9. This matches `logs/pair_semantics.log`.
- Binaries: the witness and the seed-0 point have all pumps off. The 65.12 point has b5 = b23 = b47 = 1.
- The witness violates the binary64-rounded rows by at most 2.921e−15. This matches the report's 2.9e−15.
- I checked `cert2.pkl` directly. Records 2236 and 5539 share t, cells, boxes, multipliers and mu. Record 5539 is "certified" with bound 55.0942345372475, so the interval [55.0942, 55.689908] is consistent. This relies on rbb's validity, which was reviewed outside this track.

**Original reproducer.** `python3 -B open-instances-wave2/waterno2/scip_unreliable.py` → `rv_orig_scip_unreliable.log`. Apart from run times, the output is identical to `logs/orig_scip_unreliable.log`: all 15 claims, node counts, violations and pump configurations. The wave2 folder is unchanged.

**Newest versions** (`rv_web_versions.log`, at 19:30 EDT on 2026-10-02):
- master head is a01de2cfde (2026-10-02T10:14Z).
- v101-bugfix is 0 commits ahead of master.
- The newest release is v10.1.0 (2026-09-18); the newest PySCIPOpt on PyPI is 6.2.1.
- The last-change dates of cons_nonlinear.c (2026-06-14) and of intervalarith.c, nlhdlr_default.c, expr_sum.c and expr_pow.c (January 2026) match the report.

### 1.3 Root cause: traces and source

- **Traces.** I read the step before the first "debugging solution was cut off" or "invalid ... bound" in these traces: mdbg_fm336_s0, dbgsol_fm336_v1010, tiny2_debugprop, mdbg_tiny2_hsoff, dbgsol_pumps_default, mdbg_pumps_default_s3, mdbg_fm318_s0, mdbg_pair2236_s14, dbgsol_expr_pair2236_seed8, dbgsol_expr_p4_seed0, mdbg_p4_s0, dbgsol_expr_p5_seed0, dbgsol_expr_p5_seed2, mdbg_p5_s3 and dbgsol_expr_p0_seed2.
  - In each one, that step is `SCIPBUG REVCUT: nlhdlr <default> reverseprop declared INFEASIBLE with propbounds [0,0], activity [-1.6653e-16,-5.5511e-17]` on x³ − y at a 0.7 station.
  - The one exception is pair2236 seed 11 (issue 2 below).
- **tiny2 propagation steps.** The `tiny2_debugprop.log` trace shows the steps the report describes:
  - s is fixed to fl(0.7).
  - Round 0: the root activity [−0.657, 9.99e−10] contains 0 only because p's bound is still relaxed by 1e−9. The root propbounds become [0,0], and p is fixed to fl(0.343).
  - Round 1: "applied previous propbounds: [0,0]", then the exact reverse propagation fails.
- **Source (master a01de2c).**
  - `intEvalVarBoundTightening` (cons_nonlinear.c, about lines 840–960) applies, in mode `r`, MIN(amount·MAX(1,|bnd|), 0.001·|ub−lb|). This is 0 for fixed variables.
  - `SCIPintervalPropagateWeightedSum` calls the exact `SCIPintervalIntersect` at intervalarith.c about line 4793.
  - `reversepropSum` (expr_sum.c:977) calls it.
  - cons_nonlinear.c has 6 `IntersectEps` calls and no exact intersection; nlhdlr_default.c has one of each.
  - The report's pointers are therefore accurate.
- **Why `varboundrelax = n` avoids the error** (a hypothesis, not tested). Under `n`, p is not relaxed in round 0, so the root activity [−0.657, −5.55e−17] does not contain 0. `SCIPintervalIntersectEps` (intervalarith.c:591) then returns the singleton −5.55e−17 instead of [0,0]. Later reverse propagation therefore has a non-[0,0] right-hand side and does not fail. If this holds, the defect is the combination "propbounds fixed at [0,0] while a relaxed bound still made 0 reachable, then kept after the relaxation vanishes on fixing, then an exact intersection". It would be worth stating as a hypothesis in the upstream draft.

### 1.4 Tables against the logs

`rv_tally.py` (→ `rv_tally.log`) re-parses every scan log and re-applies the rule "optimal and dual bound > witness + 1e−4" with my exact witness values.
- Every count and min/max wrong claim in the report's Section 3.2 tables matches. Examples: p4 wheel 19/20; bins 8/8/10 of 10; master 9/10; dbgsol 8/10; GAMS 10/10; pair2236 7/8/8/5/5 of 30 and GAMS 1/10; fm336 10/10 everywhere.
- The GAMS fm336 (5/5) and fm318 (0/5) counts come from `gams/logs/scan_*.txt`.
- The Section 5.5 table is correct: wheel seeds 0–9 give p0 3 + p4 10 + p5 7 = 20, plus pair2236 7, for 27/60; master 19/20; fm 30/40; p4 small-excess 2/2. Total 78/122 with default settings, 0/122 with `varboundrelax = b`.

## 2. Is the report clear about proved, numerical and open?

Mostly yes.
- The proof is exact and is separated from solver output.
- The traces are called numerical evidence.
- Section 5.5 is described as evidence, not proof, for the uninstrumented runs.
- The open items are listed: no fix tested, `n` unexplained, p4 small-excess runs untraced, witnesses only upper bounds.
- Commands are recorded for all three authors.

The issues below concern a few places where the wording claims more than the logs show.

## 3. Issues (all minor)

1. **Inconsistent totals.** Section 1 and the structured summary say "0 of 102 runs wrong; 70 of those wrong under default settings". Section 5.5 and per-item (3) say 0/122 and 78/122. My recount confirms 122 and 78. Fix Section 1 and the summary.
2. **Trace table row "pair2236, 8 and 11".**
   - `logs/dbgsol_pair2236_seed11.log` has no SCIPBUG instrumentation. Its first invalid reduction is `invalid local lower bound implication: <t_b35>[0] >= 1` at node #2, with source "cons <->, prop <->" (presumably strong branching). b47 ≥ 1 follows.
   - b35 belongs to the 0.85 station (`e465_up: x539 − 0.15 b35 ≤ 0.85`). So the first loss in seed 11 is untraced and may involve the 0.85 station.
   - Restrict the row to seed 8. Qualify "every traced wrong run loses the witness at the same step" and "all traced cutoffs involve the 0.7 station" to the instrumented runs.
3. **"The low claims are a tolerance effect"** (Section 6, per-item 4). 55.689773 and 55.689858 lie below an upper bound, and the true optimum is only known to lie in [55.0942, 55.689908]. These claims are not refuted, and their cause is not shown. Suggested wording: "not refuted; consistent with tolerance effects or with the witness not being optimal".
4. **Section 6, why seeds fail.** "Whether a seed fails depends on whether the search reaches a pump-off node of the 0.7 station ..." is a hypothesis; only seeds 8 and 14 were traced to that step. Label it as such.
5. **Section 8, "Proved: SCIP's reported solutions are not exactly feasible for the binary64 data".** This was shown only for the solutions examined: pumps_default, p0 seed 0, tiny2, and pair2236 seeds 0 and 7. Say so.
6. **Missed issue reports.** The GitHub search missed two open nonlinear wrong-result issues:
   - scipopt/scip #162, "Suboptimal solution for multilinear relations" (2025-08). Developers traced it towards orbitopal symmetry handling.
   - scipopt/scip #190, "Presolving renders problem infeasible" (2026-02, SCIP 10.0.1). Developers suspected 1e−6 coefficients.

   Neither looks like the same cause. Both should be cited in Section 8 and in the upstream draft as related but apparently different reports, so that the SCIP developers see the draft was checked against them. Logs: `rv_issue_search.log`, `rv_issue_bodies.log`.
7. **Upstream draft nits.**
   - The inline CIP says "Problem name : fm336", but the file to attach says `fm336_reduced`. Make them the same.
   - "Expected: the optimum is at most 187/270" can be "is 187/270", with the one-line case argument from 1.1. tiny2's optimum is likewise exactly −1.337.
   - Optionally add that 10.0.2 and 10.0.3 also accept the witness from a `.sol` file and then report 0.6926 as optimal (verified here).
   - Optionally add the `varboundrelax = n` hypothesis from 1.3, clearly marked as untested.

## 4. Commands I ran

All from the review folder or the track folder. One SCIP process at a time with OMP_NUM_THREADS = 1, at most 2 cores. No background jobs; no processes of mine are left running. Nothing was posted. I made no edits outside the review folder. The original reproducer was run with `python3 -B`, and the wave2 folder is unchanged.

- `python3 rv_cip_exact.py <model.cip> <witness.json> <claims>`, 8 runs → `rv_cip_exact.log`: all FEASIBLE and below the claims.
- Inline mutation test of `rv_cip_exact.py` on p4 → `rv_mutation.log`: 6/6 rejected.
- `python3 rv_gms_exact.py <model.gms> <witness> <model.cip> [claims]`, 8 runs → `rv_gms_exact.log`: all feasible, all identical to the CIP files.
- `python3 rv_osil_crosscheck.py waterno2_06.osil models/{p0,p4,p5,pair2236}.cip` → `rv_osil_crosscheck.log`: 0 rows differ. An inline check found no one-sided ranged rows and no missing in-scope OSIL rows.
- `python3 rv_binary64.py` → `rv_binary64.log`.
- `./rv_runs.sh` → `rv_runs.log`. The first attempt hung in the interactive `set` command and was killed by `timeout`. The rerun with `.set` files and stdin from /dev/null completed.
- `python3 rv_wheel.py` → `rv_wheel.log`.
- GAMS: `gams m.gms lo=3 [--scipopt=1]` for fm336 (no option file, seed 3) and tiny2 (none, heuristics and separation off) → `rv_gams.log`, `gamsrun/`.
- `python3 rv_tally.py` → `rv_tally.log`; grep counts of wheel seeds 0–9.
- `python3 rv_pair2236.py` → `rv_pair2236.log`; inline read of `sepbranch/logs/cert2.pkl` records 2236 and 5539.
- `python3 rv_toggles.py` → `rv_toggles.log`.
- `python3 -B scip_unreliable.py` (in open-instances-wave2/waterno2) → `rv_orig_scip_unreliable.log`; `diff` against the track's log: identical apart from times.
- grep/sed/awk reads of the trace logs listed in 1.3; reads of `src/scip-master` (cons_nonlinear.c, intervalarith.c, expr_sum.c).
- curl (read-only, sequential with delays): GitHub API for master, bugfix branches, compare, releases, per-file last commits, issue search (6 queries) and issues #162, #190, #126, #142 and #26 with comments; PyPI JSON. Logs: `rv_web_versions.log`, `rv_issue_search.log`, `rv_issue_bodies.log`.

These are targeted checks for this track only; no CI or project-wide checks were run.
