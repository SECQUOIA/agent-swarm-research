# Group D: verification of minor fixes for eg-recheck and scip-bug

Verifier group D, 2026-10-03. Tracks: `eg-recheck` (review `reviews/eg-recheck-review-r1.md`, 6 issues) and `scip-bug` (review `reviews/scip-bug-review-r1.md`, 7 issues). P = `research-20260929/publication`. No track or author files were edited. My scripts and logs are in `scratch-D/`. All runs were single-threaded and took seconds each. No solver or certifier was run.

Result: **no blocker and no major issue.** All 13 fixes are present, and every number I recounted matches. There are four minor problems in scip-bug (residual wording that the fixes missed, and internal references in the upstream draft) and one minor problem in the summary.md integration bullet for eg-recheck.

## eg-recheck

| # | issue | verdict | evidence |
|---|---|---|---|
| 1 | A1/A2 absent from headline and integration | OK | The first result claim (report.md:20) now says "under assumptions A1 and A2" and separates the 10,404-leaf interval sample ("a sample only"). The Section 10 integration wording is qualified the same way. The Section 1 "Rigor" bullet points to Section 4 for A1/A2. |
| 2 | Infeasibility overclaim | OK | My own recount from `eg-recheck/res/p*_c*.npz` (`scratch-D/eg_counts.py`): 1,114,361 leaves; all `ok`; sel per part = {0..n−1} with no repeats; +∞ margins 98,234 = how 1 (side) 85,685 + how 3 (Farkas) 373 + how 5 (split) 12,176; no +∞ margin under how 0 or 2. Sum check 85,685 + 373 + 12,176 = 98,234. Per-part +∞ and side/Farkas counts equal the report's tables (`eg_perpart.py`). The new margin definition and table heading are correct. The Farkas system uses cuts ≤ θ*, so "no feasible point with F < θ*" is a correct, slightly weaker statement. |
| 3 | Leaf numbering | OK | Position 69407 in the part-5 chunk concatenation has sel = 56587 and margin 1.401160438384777e-7, which is the part-5 minimum. The r1 reviewer's `leaves_p5.npz[56587]` is the same box (lo/hi equal) with the same margin. `recheck_leaves.py` sets sel to `verify_tree.py`'s leaf-list index (lines 118–125), so 56587 is the leaf-list index. All 80 `tight_leaves.log` entries match concatenation positions (`eg_tightnum.py`), so the stated convention also holds for that log. |
| 4 | Stale Git bullet | OK | `git show --stat 514a788f -- …/eg-recheck` lists exactly `coverage_check.py`, `logs/coverage_check.log`, `coverage_check_drop.log`, `negative_control.log`, `summarize.log` and `tight_leaves.log`. These are the six files the old bullet called untracked. `report.md` is now tracked (status M). `minor_review_check.py` and its log are untracked, which matches "working-tree changes". |
| 5 | Near-optimal regions outside part 1 | OK | The new paragraph matches `reviews/eg-recheck-r1/logs/local_min.log`: 0.00654975 at x = (0.323797, 1.0, 0.786309, 1.265499, 11, 35, 23) in part 0; 0.300794 / 0.293916 / 0.508047 / 0.989195 / 1.77104 / 2.76738 in parts 2–7. "Feasible" means side-row violation ≤ 1e-9 (local_min.py docstring). The report labels these values numerical. |
| 6 | Tree-free coverage proof | OK | `reviews/eg-recheck-r1/own_cover.py` and `logs/own_cover.log` exist. The log reads "guillotine proof: True (covered; 2n−1 nodes)" for all 8 parts and "COVERAGE PROVED". I read `prove_cover`: both sides of each cut are nonempty, leaves stay inside their node boxes, and a single-leaf node must contain its box. So coverage follows, and so does the interior-disjoint partition that the report's sentence "checks disjointness and coverage" claims. The relative paths `../reviews/eg-recheck-r1/...` resolve. Optional: the Section 1 "Coverage within each part" bullets (report.md:22–24) still list only the tree check and the volume cross-check, so the r1 proof could also be cited there. |

Also verified: the sum of `n_proc` over parts is 1,152,830 (processed boxes), and parts 0 and 2–7 contain 979,044 leaves. The union of r1 samples A/B/C over parts 0 and 2–7 is exactly 10,404 distinct leaves, with every `st` = 1 and 300 tight leaves per part.

**summary.md integration bullet (minor).** `reviews/minor-fixes/summary.md:16`:
- It says "Distinguish the earlier 1,152,830 **processed-leaf** count". 1,152,830 is the number of processed boxes, not leaves. The report (Section 1, "Correction to the counts") explicitly corrects exactly this confusion.
- The bullet also opens with "For eg_all", but the instance is eg_disc2_s.

Suggested fix: "For eg_disc2_s, … Distinguish the 1,152,830 processed boxes from the 1,114,361 leaves." The issue-table cells (summary.md:53–58) are correct.

## scip-bug

| # | issue | verdict | evidence |
|---|---|---|---|
| 1 | Inconsistent totals | OK | I recounted from the raw logs with my own parser (`scratch-D/scip_recount.py`), ignoring the logs' WRONG/ok labels. My rule: status optimal and claimed dual > exact witness + 1e-4. Results: 122 `varboundrelax=b` runs, 0 wrong, all optimal. Matched default runs (same model, build and seed) are 122, of which 78 are wrong: wheel 3+10+7+7 = 27/60, master 19/20, fm 30/40, small-excess 2/2. The second small-excess run is `binary_p4.log` 10.1.0 seed 4 at −6.72975433522885, and the first is 10.0.2 seed 3 at −6.72988938834578. My labels agree with the log labels in every run. `scan_summary.csv` has 12 b rows totalling 120 seeds and no row from `p4_smallexcess_vbr_b.log`, so it does omit the two later p4 tests. The old Section 1 numbers 102/70 are gone, and no "102" remains anywhere. |
| 2 | Uninstrumented seed 11 | **problem (minor)** | The fix itself is correct. `logs/dbgsol_pair2236_seed11.log` has 0 SCIPBUG lines. Its first loss is at line 85, "invalid local lower bound implication: <t_b35>[0] >= 1", with source "cons <-> (handler <->), prop <->, … node #2 depth 1". b47 ≥ 1 follows at line 111. In `models/pair2236.cip:249`, `e465_up: -0.15<b35> +1<x539> <= 0.85` makes b35 the pump of the 0.85 station. The table row is now seed 8 only. In all 16 table logs I checked, the first loss follows a SCIPBUG REVCUT / CUTOFF / SB line (`scip_traces.py`). However, two common-mechanism statements were not qualified, although the response row says "all common-mechanism claims" were: (a) report.md:243 still says "All traced cutoffs involve the 0.7 station". Seed 11 has a debug-solution trace whose first loss is at the 0.85 station, and the review asked for this exact sentence to be restricted to instrumented runs. (b) report.md:38 (Section 1, seed-dependent case) says "It has the same cause: a strong-branching child on 10.0.2, a tree node on master", which is shown only for instrumented seeds 8 and 14. Fix: "All instrumented cutoffs in Section 5.3 involve the 0.7 station", and "In the instrumented seeds (8 on 10.0.2, 14 on master) it has the same cause …". |
| 3 | Low pair claims | OK | Section 6 now reads "not refuted … consistent with tolerance effects or with the witness not being optimal". The distances are 55.689908 − 55.689858 = 5.0e-5 and 55.689908 − 55.689773 = 1.35e-4. The certified interval [55.0942, 55.689908] is kept. See collateral C2 for a remaining Section 1 sentence. |
| 4 | Seed-failure explanation | OK | Now labelled "A hypothesis, supported by instrumented seeds 8 and 14". The "4 to 8 of 30 seeds" range matches the pair2236 counts 7/8/8/5/5 and dbgsol 4. |
| 5 | Binary64 overclaim | OK, with a minor residual | The five examined solutions agree with the logs. `binary64_scip_solution.log` covers pumps_default (claim 1.198), p0 (169.9503268572512, which is seed 0) and tiny2 (−1.337, the default-settings solution). `pair_semantics.log` covers pair2236 seeds 0 and 7. Section 4 (report.md:169) and Section 8 are restricted, and summary.md:17 says "examined binary64 solutions". The draft and Section 7 make no binary64 claim about SCIP solutions. Residual (minor): report.md:173 still concludes "So no consistent reading of the model makes SCIP's answers right". That generalizes to all of SCIP's answers from the examined solutions plus pump-off examples. Suggested: "So, for the examined solutions, no consistent reading …", or tie the conclusion to the decimal-model refutation (which is proved for all claims) and SCIP's own tolerance acceptance of the witnesses. |
| 6 | Related upstream issues | OK, with a minor residual | I checked the saved JSON: `scip-bug/sources/`, whose sha256 sums match MANIFEST.md. #162: "Suboptimal solution for multilinear relations", opened 2025-08-07 and open. svigerske: wrong value disappears with symmetry handling off; cutoff "triggered by symmetry_orbitopal.c". christopherhojny (contributor) then judged the orbitopal reductions correct, so "points toward orbitopal symmetry handling" is accurate but not settled. #190: "Presolving renders problem infeasible", opened 2026-02-14 with SCIP 10.0.1, open. svigerske: "These 1e-6 in many constraints are likely problematic". With 2 presolve rounds the reporter's run finds a solution, which supports "false presolve infeasibility" in the draft. Links are present in Section 8 and in the draft. Residual (minor): the report never points to `sources/` (Section 8 says only "checked through the GitHub API"), and the Section 9 file table does not list `sources/` or `minor_review_check.py`. |
| 7 | Draft consistency and exact optima | OK, with a minor residual | The inline CIP in the draft (report.md:445–481) is byte-identical to `min/fm336_v1010.cip` after trailing-space stripping, including `Problem name : fm336_reduced`. The inline tiny2 CIP is identical to `minimal/tiny2.cip`. `reviews/scip-bug-r1/rv_runs.log:55–61, 155–161` shows that 10.0.2 and 10.0.3 read the `.sol` and report 6.92592587925926e-01 as optimal. The `n` hypothesis in the draft is labelled untested and is consistent with review §1.3 and with report Sections 5.4 and 8 ("not explained"). The fm336 and tiny2 case proofs are sound (details below). Residual (minor): the upstream draft, meant for SCIP developers, now cites internal artefacts: "These exact case comparisons are recorded in `logs/minor_review_check.log`" (report.md:527), "by review r1 (`../reviews/scip-bug-r1/rv_runs.log`)" (report.md:502), and "Review r1 proposed …" (report.md:555). Before filing, rephrase these as "we also checked on 10.0.2 and 10.0.3" and "one possible explanation (untested) is …", and drop the local paths. |

**fm336 case proof.** I checked this by hand against the CIP and in `scratch-D/fm336_cases.py` (exact Fractions plus a float grid). The objective is 5w0 + 0.2b1 + w1 + 0.1b2 + 2w2, all coefficients are nonnegative, and all variables are ≥ 0. The pow rows give w_i ≥ p_i + b_i − 1. The cases:
- b1 = 1: cost ≥ 0.2 + w1 ≥ 0.2 + p1 = 6513/8000 = 0.814125 > 187/270.
- b0 = 1: cost ≥ 5·p0 ≥ 5·0.343 = 1.715 > 187/270.
- b0 = b1 = 0: q0 ≤ 3·0.7 − 2.1 = 0 and q1 ≤ 2·0.85 − 1.7 = 0, using s1 = 0.85 because p1 = 0.614125 = 0.85³ exactly. If b2 = 0, then q2 ≤ 3·0.6 − 1.8 = 0, which violates demand ≥ 0.5. So b2 = 1, q2 ≥ 0.5, s2 ≥ (0.5 + 1.5)/3 = 2/3, and cost ≥ 0.1 + 2·(2/3)³ = 187/270. The witness attains this value.

The float grid minimum over the eight binary cases is 0.69268 ≥ 0.692593, with no case below 187/270.

**tiny2 case proof.** If b = 0, then s ≤ 0.7 ≤ s forces s = 0.7 and p = 0.343, giving objective −1337/1000. If b = 1, then s³ − 2.4s has its global minimum on s ≥ 0 at √0.8 ∈ [0.7, 1], so the value is ≥ 0.2 − 1.6√0.8 ≈ −1.23108. The claimed inequality "> −1.337" is equivalent to 0.8 < (1.537/1.6)² = 0.92280, which holds exactly. The draft states the b = 0 forcing only implicitly ("at b = 0, s = 0.7, p = 0.343"), which is acceptable.

**Observation (pre-existing, not part of the fixes).** The draft says the exact rational point "satisfies every constraint exactly … SCIP accepts it". The `.sol` file SCIP reads (`min/fm336_v1010.witness.sol`) contains rounded decimals (s2 = 0.6666666666666666, p2 = w2 = 0.2962962962962963), so SCIP accepts a rounded copy, within tolerance. A half-sentence would make this clear.

## Collateral (diff review)

### eg-recheck

`diff -u reviews/minor-fixes/before/eg-recheck.txt eg-recheck/report.md` has 7 hunks:
- Section 1 result sentence and certification bullet: issues 1 and 2.
- Margin definition and table heading: issue 2.
- Tight-leaf paragraph plus the new near-optimal paragraph: issues 3 and 5.
- Coverage item 2: issue 6.
- Git bullet: issue 4.
- Integration wording: issue 1.
- Appended response section.

No accidental deletions, no changed numbers, and no broken paths (`../reviews/eg-recheck-r1/{own_cover.py, logs/own_cover.log, logs/local_min.log}` exist). No stale "proved infeasible" or unqualified "verified on every leaf" remains. The body agrees with the response table. Only the optional Section 1 coverage-bullet note under issue 6 remains.

### scip-bug

The diff (`scratch-D/logs/scip_report.diff`, 161 lines) has hunks only at Section 1 (totals, "instrumented"), Section 4 (examined solutions), the Section 5.3 heading, intro, table row and seed-11 paragraph, the Section 6 bullets, Section 8 (binary64, issues #162/#190), the draft (CIP name, exact optima, readsol on 10.0.2/10.0.3, n hypothesis, related reports), and the appended response. No accidental deletions and no numbers changed other than 102/70 → 122/78. The relative links resolve: `../reviews/scip-bug-r1/rv_runs.log` and `logs/minor_review_check.log` exist. Stale statements not touched by the diff:
- **C1 (minor; part of issue 2).** report.md:243 "All traced cutoffs involve the 0.7 station" and report.md:38 "It has the same cause …". Details and fix under issue 2.
- **C2 (minor).** report.md:36, "Seed-dependent case (cell pair; claims 55.69 or 65.12): it is a **real error, not a tolerance effect**". The parenthetical includes the 55.69 claims, which Section 6 now says are not refuted. Suggested fix: "(cell pair; claims 56.49 and 65.12 are real errors; the 55.69 claims are not refuted)", or drop 55.69 from the parenthetical.
- **C3 (minor; issue 5 residual).** report.md:173 "no consistent reading …". See issue 5.
- **C4 (minor; issues 6 and 7 residuals).** `sources/` is not referenced in the report, and the upstream draft now contains internal paths and "review r1" references. See issues 6 and 7.

The summary.md cells for scip-bug (summary.md:17, 59–65) agree with the report.

## Commands

All were run from `/workspace/minlp-notes/research-20260929/publication` unless a different directory is shown. Python scripts were run with `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`, one at a time.

- `cat reviews/minor-fixes-review-r1/BRIEF.md`; `cat reviews/minor-fixes-review-r1/PROGRESS.json`; `grep -n -i -E "eg-recheck|scip-bug" reviews/minor-fixes/summary.md`; `sed -n 1,30p reviews/minor-fixes/summary.md`; `sed -n 55,70p reviews/minor-fixes/commands.md`; inline `python3 -c` read of `reviews/minor-fixes/issues.json`
- `cat reviews/eg-recheck-review-r1.md`; `cat reviews/scip-bug-review-r1.md`
- `diff -u reviews/minor-fixes/before/eg-recheck.txt eg-recheck/report.md`
- `diff -u reviews/minor-fixes/before/scip-bug.txt scip-bug/report.md > reviews/minor-fixes-review-r1/scratch-D/logs/scip_report.diff`
- `sed -n` reads of `eg-recheck/report.md`, `scip-bug/report.md`, `eg-recheck/margin_cert.py`, `eg-recheck/inspect_leaf.py`, `reviews/eg-recheck-r1/own_cover.py`, `reviews/eg-recheck-r1/local_min.py`; `cat eg-recheck/minor_review_check.py eg-recheck/logs/minor_review_check.log scip-bug/minor_review_check.py scip-bug/logs/minor_review_check.log`
- `grep -n -E "sel|verify_tree|leaves" eg-recheck/recheck_leaves.py`
- `cd scratch-D && python3 eg_counts.py | tee logs/eg_counts.log`
- `cd scratch-D && python3 eg_perpart.py | tee logs/eg_perpart.log`
- `cd scratch-D && python3 eg_tightnum.py | tee logs/eg_tightnum.log`
- `git show --stat --format='%H %s' 514a788f -- research-20260929/publication/eg-recheck`; `git status --short research-20260929/publication/eg-recheck research-20260929/publication/scip-bug`; `git ls-files research-20260929/publication/reviews/eg-recheck-r1`
- `cat reviews/eg-recheck-r1/logs/own_cover.log`; `tail -20 reviews/eg-recheck-r1/logs/local_min.log`
- `head`/`grep` of `scip-bug/logs/{seedscan_p0,seedscan_vbr_b_p0,fm_scan,p4_smallexcess_vbr_b,master_p4,master_vbr_b_p5,binary_p4}.log`, `scan_summary.csv`; `grep "^#" seedscan_*.log master_*.log binary_p4.log fm_scan.log`
- `cd scratch-D && python3 scip_recount.py | tee logs/scip_recount.log`
- `grep -n -i -E "invalid|cut off|SCIPBUG|debugging solution" scip-bug/logs/dbgsol_pair2236_seed11.log`; `sed -n 95,112p` of the same log; `grep -n -E "b35>" scip-bug/models/pair2236.cip`
- `cd scratch-D && python3 scip_traces.py | tee logs/scip_traces.log`; `grep -n -i -E "infeasible|reverseprop|activity"` over six 10.0.2 dbgsol logs
- `cat scip-bug/logs/binary64_scip_solution.log`; `grep -n -i -E "seed|viol|feasible|claim" scip-bug/logs/pair_semantics.log`
- `cat scip-bug/sources/MANIFEST.md`; `sha256sum scip-bug/sources/*.json`; inline `python3` printing title, state, dates, bodies and comments of issues 162 and 190 from the saved JSON
- `grep -n -E "sources/|minor_review_check|102|\b70\b|tolerance effect|same cause|traced|fm336_reduced|Problem name|at most" scip-bug/report.md`; `grep -n "Problem name" scip-bug/min/fm336_v1010.cip scip-bug/minimal/tiny2.cip`
- `awk` extraction of the inline CIP blocks from `scip-bug/report.md` and `diff` against `min/fm336_v1010.cip` (FM336_SAME) and `minimal/tiny2.cip` (TINY2_SAME); `cat scip-bug/min/fm336_v1010.witness.sol`
- `grep -n -E "^#|^==|…readsol…" reviews/scip-bug-r1/rv_runs.log`; `grep -n -A6 "10.0.3 fm336 witness read" reviews/scip-bug-r1/rv_runs.log`
- `cd scratch-D && python3 fm336_cases.py | tee logs/fm336_cases.log`. The first version used no float tolerance on q ≥ 0, so every case was spuriously infeasible. I fixed the tolerance with `sed -i` and reran; the final log is the rerun.

These are targeted checks only. No project-wide verification and no CI were consulted.
