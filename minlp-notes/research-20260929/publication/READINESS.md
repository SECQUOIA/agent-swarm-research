# Publication readiness

Updated 2026-10-04: responses to integration reviews r1 and r2; final package rebuilt. Scope: the September 29 certificates and listed-bound
audit, with the completed publication tracks integrated into
[open-instances-summary.md](../open-instances-summary.md) and
[audit-report.md](../bound-audit/audit-report.md). The summary's checked
bounds and upward gap displays are authoritative for the paper; older
notes sometimes retain shorter, unsafe rounded displays.

The evidence supports a computational paper with the limits below stated
explicitly. The final package rebuild and default package check passed on
2026-10-04; release decisions and a user-authorized commit remain pending. This record does not claim
that every revised report received a new independent review: it preserves
the latest review's actual verdict and distinguishes the subsequent
response from that verdict. Reviewers are the independent verifiers named
in the linked reviews; the reproduction reviewer identifies itself as
Claude. The subsequent [independent integration review r1](reviews/integration-review-r1.md)
returned **issues**: 0 blockers, 3 major and 12 minor. It confirmed every
recomputed gap cell and count. The response below distinguishes these
implementation fixes from an additional independent review round.

## Evidence by result family

Paths in this record are relative to publication/ unless a link points
elsewhere. "Verified" means the review's verdict, under the stated
arithmetic and model assumptions. Except where an attained exact optimum
is proved, a closure is an optimum enclosure with the summary's gap.

| paper claim/result family | evidence and independent review | verification status | caveats and what is not established |
|---|---|---|---|
| lnts50/100/200/400 duals and exactly feasible primals | [original verification](../reviews/open-instances-verification/verification-report.md); [primal report](primal/lnts/report.md), points/ and logs/; [independent primal r1](reviews/primal-lnts-review-r1.md) | Original dual verified; primal r1 **verified**, with minor issues addressed in the report and minor-fixes responses. | Point is defined by a reduced-system existence proof, not a rounded .sol vector. Reviewer checked existence using its own intervals and exact rational trigonometric bounds. Gap uses the summary dual display; no new smaller-margin dual was computed. lnts is partly known: Gurobi closed lnts50 to tolerance, and Göß 2026 PARA prints 0.00–0.01% gaps (floating point). |
| dtoc5 certificate and exact rational point | [original verification](../reviews/open-instances-verification/verification-report.md); [primal report](primal/dtoc5-lukvle10/report.md), points/dtoc5_point.txt.gz and exact objective log; [independent primal r1](reviews/primal-dtoc5-lukvle10-review-r1.md) | Dual verified; primal r1 **verified**, minor issues addressed. Integration independently recomputed the OSIL objective exactly. | Certificate is for the stored MINLPLib coefficient, which differs from CUTEst by a factor of 4. Prior MINOTAUR floating-point closure assumed default bounds. Exact feasibility does not establish the numerical point's local-minimizer claim. |
| lukvle10 certificate and exact feasible point | Same [original verification](../reviews/open-instances-verification/verification-report.md) and [primal track/review](primal/dtoc5-lukvle10/report.md); logs/lukvle10_enclose.json | Dual verified; independent primal r1 **verified**. | The point is defined by exact seeds and recurrence, with an objective enclosure. KKT agreement is numerical; saying the remaining gap comes only from the dual is conditional on the KKT point being globally minimizing. |
| camshape100/200/400/800 exact optima | [original verification](../reviews/open-instances-verification/verification-report.md); exact rational comparison/envelope proofs; [control literature](literature/control/report.md) | Exact attained optima independently verified; literature r2 **verified**, with minor issues subsequently addressed. | camshape100 was already solved globally in floating point. camshape200 has an older uncheckable closure listing. QPLIB copies differ by rounded constants; the camshape800 contradiction on the QPLIB copy is strong evidence, not a transported exact proof. |
| optcdeg2 quadratic calibration and feasible point | [bang-bang report](../theory-bangbang/report.md); [independent verification](../reviews/bangbang-verification/verification-report.md), logs/qcal_exact.json and primal_check.json | Exact rational calibration verified; primal existence verified. Integration checked the rounded certificate label and the gap exactly. | Displayed dual is rounded down, not the exact certificate value. Stored MINLPLib damping differs from the CUTEst source by a factor of 4. Older global closure listing has no retained value/log. |
| hvycrash constant objective and explicit witness | [small verification](../reviews/wave2-small-verification/verification-report.md); [small literature](literature/small/report.md), SIF bound-card checks | Exact identity and witness verified; latest literature review r3: **issues**, no blocker or major issue; four minor corrections addressed in the report. | Same CUTE problem at N=50. The value was already listed; novelty is the identity and witness, not discovery of the value. This does not establish physical validity of the source model. |
| ex6_2_5/ex6_2_7, etamac and pricing050 certificates | [small verification](../reviews/wave2-small-verification/verification-report.md), per-instance logs; [small literature](literature/small/report.md) | Independent certificate verification **verified**. Integration checked bounds, primal display directions and upward gaps using saved endpoints. | ex6_2_* very likely have earlier ε-global floating-point results (McDonald–Floudas; sources not read). For pricing050 the summary uses conservative subtraction of safe displays because the saved log does not retain the full exact primal objective. Sources' scaled models and values are not automatically interchangeable. |
| chain50/100/200/400 exact points and duals | [COPS verification](../reviews/cops-verification/verification-report.md); [primal report](primal/chain/report.md), points/*_generator.json and *_box.json; [independent primal r1](reviews/primal-chain-review-r1.md) | Dual independently verified; primal r1 **verified**, minor issues addressed. | Exact algebraic points, not rounded numerical vectors. Summary gaps use safe individual decimal duals, not the compact range. Some older detailed reports contain unsafe shortest decimal forms; use the summary and saved exact binary64 values. |
| catmix100/200/400/800 DP certificates and exact primal policy values | [COPS verification](../reviews/cops-verification/verification-report.md); [catmix recheck](../reviews/catmix-recheck.md); [exact display record](reproduction/cops/logs/exact_display_checks.json) | All four duals independently recomputed; catmix recheck confirmed the later 400/800 certificates. Integration checked all four exact-point gaps. | OSIL coefficients differ slightly from GAMS text. Claim is for OSIL; no exact transport to GAMS or COPS 3.0 is established. The summary uses stronger verifier duals, exact author points for 100/200/400, and the verifier policy point for 800 rather than the short Newton display. |
| powerflow0030p/0039p/0039r bounds and exactly feasible primals | [wave-3 verification](../reviews/wave3-verification/verification-report.md); [0039 review](../reviews/powerflow0039-review.md); [primal report](primal/powerflow/report.md), certify logs; [independent primal r1](reviews/primal-powerflow-review-r1.md) | Exact dual evaluation/PSD proof and leaf certificates independently verified; primal r1 **verified**, minor issues addressed. | Exactly feasible point existence uses outward enclosures; reviewer used its own rational intervals. MINLPLib 0030p drops two shunts, and 0039p/r drop taps. Rounded 0030p/r twins do not permit rigorous bound transport without a perturbation proof. New numerical solves need not recover the saved certificate. Prior certified ACOPF exists on other models. |
| pindyck concavity certificate and feasible point | [extension](../open-instances-wave2/small/pindyck-extension.md); [independent review](../reviews/pindyck-review.md), primal_check.txt | Independent rebuild **verified**; integration checked the gap from the saved primal value with a last-digit allowance. | COCONUT's better value belongs to a mistranslation. No claim is made for that different model or for unrelated numerical solves. |
| eg_int_s/eg_disc_s/eg_disc2_s duals and primal witnesses | [retry note](../open-instances-wave3/eg/retry.md); [independent retry review](../reviews/eg-retry-review.md); [all-leaf report](eg-recheck/report.md), rec/, res/ and logs/; [independent all-leaf r1](reviews/eg-recheck-review-r1.md) | Retry independently verified. All-leaf r1 **verified**, minor issues addressed. Run G has 1,114,361 certified leaves, zero failures; 1,152,830 counts processed boxes. Integration independently summed the chunk totals. | All three dual certificates use A1 (hand-checked float-padding error analysis) and A2 (sampled numpy exp relative-error assumption). Coverage has an exact independent proof for eg_disc2_s; eg_int_s and eg_disc_s coverage rests on the retry reviewer's exact tree bookkeeping. Only a separate 10,404-leaf sample in parts 0 and 2–7 was re-certified with outward intervals without the libm assumption. Uniform exp accuracy and assumption-free certification of every leaf are not established. eg_int_s had prior floating-point closure; for eg_disc_s and eg_disc2_s, CAMINO's Gurobi 13.0.0 optimality claim is refuted by a feasible point; the data do not record Gurobi's termination status, and the cause is unknown. |
| waterno2_06/09/12/18/24 improvements and exactly feasible points | [wave-2 verification](../reviews/waterno2-verification/verification-report.md); [later-period review](../reviews/waterno2-recheck.md); [separator review](../reviews/waterno2-sepbranch-review.md); [cell-slope review](../reviews/waterno2-cellslopes-review.md); [primal report](primal/water-ann-kan/report.md) and [independent primal r1](reviews/primal-water-ann-kan-review-r1.md) | Period and separator certificates independently verified, including every cell-pair bound in the cell-slope review; primal r1 **verified**, minor issues addressed. Integration recomputed all five OSIL objectives exactly. | Points use exact rational/algebraic definitions. These five gaps remain nonzero; no closure is claimed. Huang's related extended models differ, and the cited MSc thesis was not obtained. |
| ann_cumene_tanh finite bound and exact feasible point | [extension](../open-instances-wave3/ann/extension.md); [independent extension review](../reviews/ann-extension-review.md); [primal report/review](primal/water-ann-kan/report.md); [network literature](literature/network/report.md) | Extension independently re-certified; primal r1 **verified**. Current upward gap is 0.195%. | Primal existence uses forward definitions and assumes mpmath iv outward rounding. No closure. Exact exp twin was already closed in floating point; our finite bound is weaker than those claims. Novelty is restricted to the rigorous bound found for this stored model. |
| six KAN models: exact OSIL infeasibility and enclosure of R | [wave-3 verification](../reviews/wave3-verification/verification-report.md); [primal report/review](primal/water-ann-kan/report.md), six point JSONs; [network literature](literature/network/report.md) | OSIL inconsistency proved; R duals independently verified; primal r1 **verified**. All six current gaps checked exactly in integration. | Original OSIL models have no exactly feasible point. R drops partition rows and additional intermediate restrictions. The network-point enclosure assumes mpmath iv; no feasible OSIL point or OSIL optimum is asserted. Largest absolute gap is 2.42e-8; a blanket 1e-10 absolute claim would be false. Published n4/n5 optimal values are tolerance artifacts. |
| listed-bound audit: class (i), emfl bounds and remaining classes | [audit report](../bound-audit/audit-report.md); [first verifier](../reviews/bound-audit-verification/verification-report.md); [recheck](../reviews/bound-audit-recheck.md); [last confirmation](../reviews/audit-confirm-r2.md); bound-audit results.json and certificate logs | All 19 class (i) pairs and four emfl optimum enclosures confirmed independently. Three confirmation rounds; last verdict **verified**, no remaining problem. Integration retains the classifications and checks the emfl relative lower display. | Gross/tolerance-scale are size labels. Small exact conflicts need not mean solver bugs under unknown original settings. Class (ii)-repair does not prove dual validity; class (iii) is undecided. Display ties and unscreened invalid bounds are not resolved. Physical plausibility is not established for glider100. |
| class (i-r), parsing and screen | [audit-ir report](audit-ir/report.md), check_ir/spring_global/parse/digit logs; [independent r1](reviews/audit-ir-review-r1.md) | r1 **verified**, minor issues addressed. All 12 pairs independently re-proved; parser and screen independently checked. | Literal displayed numbers are contradicted. Five spring entries can be explained by page rounding; underlying solver bounds are unknown. Earlier six-digit rounding of the other seven is supported but not proved. No additional class (i) pairs are asserted. |
| MINLPLib refresh and historical model identity | [status report](minlplib-status/report.md), data/part_a.json, exact_forms/listing/history logs; [r1](reviews/minlplib-status-review-r1.md), [r2](reviews/minlplib-status-review-r2.md) | r1 independently confirmed refresh; r2 **issues**, with the earlier major issue resolved and four minor corrections addressed in the report and checked by the parent orchestrator against the reviews; see the [saved response](minlplib-status/report.md#response-to-review-round-2). | Relevant status unchanged at the saved 2026-10-02 refresh. Three ghg_3veh constants changed by rounding; old-text contradiction survives. Nine instances (four sssd*persp, watercontamination0303 and four smallinvDAX*) have no pre-bound copy; no copy covers March–December 2014. Their identity rests on 2014-12 statistics and 2017 full copies. Archive gaps and truncated captures limit historical completeness. Numerical row agreement is evidence, not an algebraic identity proof. Report Table B1 supersedes the older data table. |
| literature priority and model provenance | [control report](literature/control/report.md)/[r2](reviews/lit-control-review-r2.md); [network report](literature/network/report.md)/[r2](reviews/lit-network-review-r2.md); [small report](literature/small/report.md)/[r3](reviews/lit-small-review-r3.md), saved source manifests | Independent reviewers: control rounds 1–2, latest **verified**; network rounds 1–2, latest **verified**; small rounds 1–3, latest **issues**, no blocker/major issue. Subsequent minor-fixes/report responses address the listed issues; the parent checked the final small-literature minor fixes against its reviews; see the [saved response and checks](literature/small/report.md#18-response-to-review-round-3-2026-10-03). | Searches cannot prove novelty. Unread sources, unavailable old logs, rounded QPLIB copies, source scaling differences and cumene source-version discrepancies remain explicit. No unconditional priority claim or blanket “previously unsolved globally” claim is supported. |
| matched-budget solver comparison | [campaign report](solver-runs/report.md), [table](solver-runs/results_table.md), results_table.csv, run.json/trace/logs; [setup r1](reviews/solver-campaign-review-r1.md); [final-analysis r1](reviews/solver-analysis-review-r1.md) | Setup review r1: **issues** (two major), addressed by the final relaunch. The campaign's own round-2 driver review was interrupted and never finished; it has no completed findings or verdict. Solver-analysis review r1: **issues** (two major: six BARON values without a globality guarantee and the overloaded first batch; four minor); it independently re-derived run validity from raw logs and confirmed raw values/counts. The author fixed all six issues. The parent orchestrator (Claude) checked the fixes directly against the review: collect.py diff additive only, per-row flags and report wording; see the [saved response](solver-runs/report.md#response-to-review-round-1). No second independent solver-analysis review round was performed. Integration independently recounted and compared every finite dual with exact source decimals. | BARON 26.5.27/GUROBI 13.0.2/SCIP 10.0.3, 3600-second solver limit, one thread. Zero accepted closures; BARON's two claims conflict with certificates. Six BARON values lack a globality guarantee, six SCIP comparisons use tightened models, and KAN comparisons use R. Ten overloaded-batch rows and three SCIP memory stops limit benchmarking. No ranking, isolated-core timing or failure under other budgets/settings is established. |
| SCIP wrong-optimal-value bug | [SCIP report](scip-bug/report.md), witnesses, minimal models, debug traces and source snapshots; [independent r1](reviews/scip-bug-review-r1.md) | r1 **verified**; exact witnesses reproduced independently. The [round-3 response](reviews/minor-fixes/response-r3.md) corrects the scope: Section 5.3 has 14 rows for 15 instrumented runs, and only three of the five examined solutions have refuted wrong claims. Independent minor-fixes review r2 found one major overstatement (SCIP report line 173); round 3 applied the reviewer's exact replacement. The parent spot-checked those fixes, recorded in the [round-3 response](reviews/minor-fixes/response-r3.md), and integration review r1 covers them; there was no further independent minor-fixes track round. | Traced mechanism applies to instrumented wrong runs, not all SCIP results. Low cell-pair claims are not refuted. Exact infeasibility of examined returned binary64 vectors was not checked for every scan. Upstream report is drafted and NOT submitted; no maintainer confirmation or fix is established. |
| reproduction and portability | [README](reproduction/README.md), [report](reproduction/report.md), maps, manifest, archived inputs, command index, strict relocated smoke logs; [independent r1](reviews/repro-package-review-r1.md) | Independent reviewer Claude, r1 **issues**, no blocker; dependency-list major issue and minor packaging issues addressed in the package response; the parent spot-checked those fixes; see the [saved package response](reproduction/report.md#response-to-review-round-1) and [integration response](reproduction/report.md#response-to-integration-review-r1). No second independent package review round was performed. Maps and manifest were rebuilt and the default package check passed on 2026-10-04. | Replay is distinguished from regeneration. The audit topopt p5 displays use the committed certificate; one-BLAS-thread regeneration selects a different valid point. Optimizer endpoints, QR basis and long wall-limited frontiers are not promised identical across builds or loads. eg_disc2_s all-leaf evidence is mapped; manifest scopes include eg-recheck/ and reviews/eg-recheck-r1/. Final map/manifest synchronization and commit dependencies passed targeted checks; copied copyrighted literature stays local, with hashes in tracked manifests. |
| computational environment and run times | [environment capture](integration/environment-r1.json), [recorded timing evidence](integration/runtime-evidence-r1.json), [command index](reproduction/commands.json), source terms below | Collected for this response: current host, pinned reproduction environment and selected recorded timings; timing sources and hashes checked. | Original per-run environments and CPU times are not fully recoverable. Shared machine; the release licence remains a user decision. |
| numerical display and integration corrections | [minor-fixes list](reviews/minor-fixes/summary.md), integration-r2.json; [independent r2](reviews/minor-fixes-review-r2.md); [integration exact checks](integration/numbers.log), [objective recomputation](integration/objectives.log), [page/count/handoff checks](integration/publication-counts.log), [audit display replay](integration/audit-displays.log) | Minor-fixes reviews r1 and r2 were independent; latest verdict **issues** (one major and ten minor), while all 40 ordered replacements are explicitly confirmed correct. Round 3 fixed the major and track-level minor issues; the parent spot-checked those fixes, recorded in the [round-3 response](reviews/minor-fixes/response-r3.md), and integration review r1 covers them. There was no further independent minor-fixes track round. This implementation applied 33 owned replacements and validated the seven protected replacements on disposable copies. Current main-document gap cells, A1/A2, spring antecedent and three display/wording issues are resolved. | Six protected replacements are already applied by the round-3 owner; the historical solver-runs/report.prev.md was a byte-identical backup of the git HEAD report and was removed on 2026-10-04; git history keeps that version. Track-level round-3 corrections are recorded in response-r3.md. No protected replacement was applied or reapplied here. This integration is an implementation check, not a fresh independent review of the revised whole. No scientific search was rerun. |

## Integration checks and limits

[commands.md](integration/commands.md) lists the targeted commands actually
run. [number-checks.json](integration/number-checks.json) records exact-check
results and source hashes; [gap-values.json](integration/gap-values.json)
contains the rational quantities behind every numerical gap cell. The
integration independently evaluated the dtoc5 and five water objectives
from the stored exact points and OSIL models, checked corrected primal and
dual directions, recounted campaign totals and run-G chunk totals, and ran
the existing audit display checker in a disposable copy. No scientific
module was imported or executed in the main tree. No solver, full research
computation, project-wide check or CI inspection was run.

The original audit display checker still gives 84 accepted displays, eight
known quoted historical displays, and one skipped histogram entry. Those
eight are explicitly identified in the audit's revision history. They do
not represent failures of the current certificates. The checker uses the
committed topopt p5 certificate; it did not regenerate a new point.

The integration's scope excludes track reports, older reports, solver-runs/
and reproduction/. The [round-3 response](reviews/minor-fixes/response-r3.md), item 3, records
that the older COPS and closing-audit corrections are already applied.
[replacements.json](integration/replacements.json) retains the initial
ordered validation; [protected-handoff.json](integration/protected-handoff.json)
records a subsequent read-only check. Six of the seven protected entries
now have their safe replacements. The remaining historical
solver-runs/report.prev.md was a byte-identical backup of the git HEAD
report; it was removed on 2026-10-04, and git history keeps that version.
No protected file was edited by this integration. This implementation task owns the final map and manifest rebuild. It ran
build_result_maps.py, rebuild_manifest.py and the default check_package.py
on 2026-10-04 after all covered edits were final; all passed. Covered edits
after that date require another rebuild and default check.

## Computing environment and run times

The current computing environment, as seen inside the WSL2 VM, was
captured on 2026-10-04 from /proc, uname and /etc/os-release: Intel Xeon w5-2565X, 18 physical cores / 36 logical CPUs,
49,321,416 KiB RAM (47.04 GiB), Ubuntu 24.04.4 LTS, x86-64 WSL2 kernel
6.18.33.2-microsoft-standard-WSL2. The CPU exposes AVX2/FMA and AVX-512.
[environment-r1.json](integration/environment-r1.json) retains the exact
CPU flags, OS/kernel, memory and current NumPy build/runtime output.
The machine was shared with other sessions. These are current-host facts,
not recovered metadata for every original certificate run.

The pinned [reproduction environment](reproduction/environment.json) and
[requirements](reproduction/requirements.txt) specify Python 3.13.11
(Anaconda, GCC 14.3.0), NumPy 2.5.1, SciPy 1.18.0, mpmath 1.3.0,
SymPy 1.14.0, PySCIPOpt 6.2.1, CVXPY 1.9.3, Clarabel 0.11.1 and
highspy 1.15.1; PySCIPOpt's SCIP is 10.0.2. The current NumPy build reports
OpenBLAS 0.3.33.112.0, USE64BITINT/DYNAMIC_ARCH, and AVX512_SPR support;
current glibc/libm is 2.39. Active BLAS dispatch was not resolved because
threadpoolctl is unavailable. Only the reproduction versions are pinned:
the original BLAS/libm builds, SIMD dispatch and per-run package versions
were not consistently recorded. A2's exp sampling cannot certify another
dispatch. topopt p5 replay uses the committed certificate; regeneration
with one BLAS thread selects a different valid point.

Saved [campaign logs](solver-runs/runs/camshape100__BARON/gams.log) and
[settings](solver-runs/report.md) record GAMS 54.3.1 (build 61154be4),
BARON 26.5.27, GUROBI 13.0.2 and SCIP 10.0.3, with one solver thread.
These versions describe the comparison campaign, not every certificate
computation. The SCIP bug track separately tested 10.0.2, 10.0.3, 10.1.0
and master a01de2c.

The [command index](reproduction/commands.json), captured for this response,
contained 443 historical reproduction commands with wall times. The table selects successful
certificate generation or replay commands, with seconds in instance order;
single values for lnts and camshape cover all four instances in one command.
It is not a total of original search, tuning and review costs. ANN timings
are extension replay/verification; eg_disc2_s's indexed run covers part 1
only; the later all-leaf recheck is described below. Full command IDs,
exact recorded times and verified output hashes are in
[runtime-table-r1.md](integration/runtime-table-r1.md) and
[runtime-evidence-r1.json](integration/runtime-evidence-r1.json).

| family / recorded operation | wall seconds, in listed order |
|---|---|
| lnts50/100/200/400 | 1.84 |
| dtoc5 / camshape100–800 / lukvle10 / optcdeg2 calibration | 5.96 / 0.8 / 337.8 / 8.32 |
| hvycrash / ex6_2_7 / ex6_2_5 / etamac / pricing050 / pindyck | 0.17 / 167.34 / 800.71 / 27.09 / 8.28 / 18.67 |
| chain50/100/200/400 | 11.56 / 15.69 / 20.69 / 28.76 |
| catmix100/200/400/800 | 1049.26 / 1728.27 / 3000.91 / 4602.0 |
| powerflow0030p/0039p/0039r | 12.67 / 316.23 / 463.46 |
| waterno2_06/09/12/18/24 period certificates | 221.25 / 772.61 / 994.2 / 2385.66 / 3210.92 |
| waterno2_06 cell-slope replay | 10.72 |
| ann extension replay runs 1/2; region verification runs 1/2; open-box verification run 2 | 1951.92 / 5613.0 / 668.11 / 3044.08 / 532.1 |
| KAN R: r3 n4/n5/n9; r5 n3/n5/n8 | 22.57 / 23.83 / 22.34 / 1083.76 / 101.5 / 87.33 |
| eg_int_s; eg_disc_s parts 0/1; eg_disc2_s part 1 | 211.51 / 279.04 / 234.6 / 635.18 |
| audit linear / nd_netgen / emfl050_3_3, 050_5_5, 100_3_3, 100_5_5 / topopt p4/p5 regeneration | 6.18 / 0.93 / 3.18 / 14.56 / 5.77 / 26.25 / 167.62 / 164.44 |

For the eg_disc2_s all-leaf recheck, the 38 saved chunk timing fields sum
to 41,162 seconds rounded once (summing individually printed whole seconds
instead gives 41,151); the scheduler log records 5,372 elapsed wall seconds.
The corrected track report and summarize.py label this sum as chunk wall
time: recheck_leaves.py measures time.time(). Concurrent chunk times must not be read as end-to-end duration.
Original per-certificate CPU times are not consistently available. Shared
load and varying concurrency limit timing comparisons; these measurements
support no isolated-core speed ranking. This response reran no certificate
or solver and used at most three single-thread checks concurrently.

Source licences/terms checked on 2026-10-04:

| source | recorded licence or terms |
|---|---|
| MINLPLib models and pages | The [download page](https://www.minlplib.org/download.html) identifies CC BY 4.0. Preserve source attribution and identify changes under its terms. |
| QPLIB instances | [QPLIB documentation](https://qplib.zib.de/doc.html) identifies CC BY 4.0 for QPLIB and separately reserves website copyright to ZIB and GAMS. Do not assume the instance licence also covers every website asset. |
| CUTEst software and SIF problem collection | The separate [CUTEst LICENSE](https://github.com/ralna/CUTEst/blob/master/LICENSE) and [SIF LICENSE](https://github.com/ralna/SIF/blob/master/LICENSE) each give three-clause BSD terms: retain or reproduce copyright, conditions and disclaimer; no endorsement without permission. Preserve problem-source credits in the SIF files. HVYCRASH.SIF came from ralna/SIF. The four control SIF files came from [bitbucket.org/optrove/sif](https://bitbucket.org/optrove/sif/src/master/LICENSE) (MIT, © 2022 Nick Gould, Dominique Orban and Philippe Toint); they are byte-identical to the ralna/SIF copies. Include the notice of the source actually redistributed. |
| MATPOWER software and case data | [MATPOWER software](https://matpower.org/license/) uses three-clause BSD from version 5.1. Its [manual 8.1, Section 1.2](https://matpower.org/docs/MATPOWER-manual-8.1.pdf) explicitly excludes case data from that licence: data were "in most cases" included by permission or converted from public sources. The saved [case30](literature/network/sources/matpower_case30.m) and [case39](literature/network/sources/matpower_case39.m) headers identify their sources; retain those credits. |

MATPOWER (manual 8.1, Section 1.3) and [QPLIB](https://qplib.zib.de/) request
citation when their data are used. Saved primary-source licence evidence
and verified hashes are in [review-r2-evidence.log](integration/review-r2-evidence.log).

These source terms do not choose a licence for our own paper data or code.
The user must choose the release licence(s), and the package owner must
include the applicable third-party attribution and notices for the actual
release contents. Source articles, archived pages and case data do not
inherit a licence selected for our original code.

## Open decisions for the user

1. **SCIP upstream filing:** decide whether to submit the drafted report
   and reproducer. Nothing has been submitted or sent by this task.
2. **Solver reruns:** decide whether to rerun the ten overloaded first-batch
   runs under controlled machine load, the three SCIP memory-limit runs,
   both groups, or neither. Current tables disclose both limitations. A
   speed-ranking claim would need additional controlled measurements;
   the present certificate-strength comparison does not depend on such a
   claim. The three memory stops are SCIP on ex6_2_5, ex6_2_7 and pindyck.
   The overloaded group is dtoc5, optcdeg2 and waterno2_24 for each solver,
   plus kan_r3_h1_n9/BARON. No rerun is authorized by this integration.
3. **Commit the publication work:** when authorized, commit the untracked
   publication files with all modified dependencies in
   [files-to-commit.json](reproduction/files-to-commit.json) and the
   minor-fixes lists. Include .gitignore, literature reports, checks, logs
   and source SHA-256 manifests. Copied sources in each literature sources/
   folder stay local and untracked; their hashes are in the tracked
   manifests. The paper's data release must not redistribute copyrighted
   sources. The root literature/ collection remains ignored. No staging,
   commit or push was performed. The redundant
   solver-runs/report.prev.md backup was removed on 2026-10-04.

   This implementation task completed the final package refresh on
   2026-10-04, after all covered edits: build_result_maps.py, then
   rebuild_manifest.py, then the default check_package.py, all passed.
   Repeat those commands if covered files change before committing; require
   the default package check to pass. Exact commands and outputs are in
   [commands.md](integration/commands.md).

4. **Release licence:** choose the licence(s) for the paper's original data
   and code. The source terms above remain attached to third-party material;
   this task has not invented or applied a blanket release licence. The
   package owner must carry the applicable attributions and notices into
   the final archive.

## Response to integration review r1

The [independent review](reviews/integration-review-r1.md) returned
**issues** (0 blockers, 3 major, 12 minor); its gap cells and counts were
correct. [Exact checks](integration/review-r1-evidence.log), the renewed
[number checks](integration/review-r1-numbers.log), and
[commands](integration/commands.md) record this implementation response.
The fixes below have targeted implementation checks; no second independent
integration review is claimed. Items 2 and 15 were resolved by the package owner; this r2 response closes
the remaining track displays and the final manifest rebuild.

| item | resolution |
|---|---|
| 1, major: literature table | Removed both blank lines after the delimiter. The Markdown parser now checks all tables in the summary, audit and this record, including header attachment and the 43 literature rows. A negative control rejects the original broken table. |
| 2, major: eg_disc2_s package coverage | Resolved by the package owner; see [reproduction/report.md, Response to integration review r1](reproduction/report.md#response-to-integration-review-r1): README, result map, 54 EG command records and relocated smoke checks. This task completed the manifest rebuild on 2026-10-04. |
| 3, major: environment, timings and licence | Added current /proc and uname metadata, pinned reproduction versions, solver versions and a sourced timing table. Original environments and CPU times remain explicitly incomplete; source terms are recorded and choosing our release licence is an open user decision. |
| 4: gap-source list | Added dtoc5, lukvle10, pindyck and all three eg rows to the displayed-dual exceptions; numerical gaps are unchanged. |
| 5: eg_disc_s display | Added its binary64 excess and the independent exact-decimal leaf certification that justifies it, under A1/A2. |
| 6: literature labels/wording | Corrected Martin, camshape100/800 and eg_int_s labels; catmix sourcing; powerflow provenance and transport limits; KAN evaluation precision; CAMINO status limits; PARA percentages and DTOC5 source-model scope. Cited the unread publisher correction, credited hvycrash's SIF value and identified lukvle10 SOLTN as a tolerance artifact. |
| 7: SCIP scope | Named waterno2_06 periods 0, 4 and 5, seed dependence, both higher cell-pair claims and the unrefuted low claims in the two main documents. |
| 8: rounding and spring bisection | Limited the page-rounding explanation to the five spring conflicts; earlier rounding for the other seven is evidence only. Corrected pair terminology and credited the audit-ir script's bisection at feasibility tolerance 1e-9. |
| 9: historical model evidence | Named the nine instances with no pre-bound copy and the uncovered archive window in both main documents and this record; credited status review r1 for the refresh and preserved r2's actual verdict. |
| 10: review facts | Recorded the interrupted driver review, independent solver-analysis r1 (2 major + 4 minor), author fixes and Claude's direct checks without another independent round. Recorded independent minor-fixes r1/r2 and parent spot-checks of round 3, covered by integration r1; also recorded parent checks of status, lit-small and reproduction fixes. |
| 11: readiness wording | Made lnts prior results and the likely ex6_2_* history precise; limited the separate exact coverage proof to eg_disc2_s and cited integration r1's actual verdict. |
| 12: earlier closeness | Restored 1.3e-6 for camshape100 and 3.9e-5 for lnts50 (upward bounds corrected in r2) after exact checks against saved values. These are approximate historical gaps, not the current closure enclosures. |
| 13: old SCIP incumbent | Identified the earlier unchecked exploratory run and distinguished the campaign's 1.5e-7 deficit and 7.7e-10 row violation. |
| 14: audit details | Added the methanol50 2022 precision exception and recorded the replacement-33 spring rewrite requested by minor-fixes r2, issue 5. |
| 15: stale track/package displays | Resolved by the package owner; see [reproduction/report.md, Response to integration review r1](reproduction/report.md#response-to-integration-review-r1). The remaining track displays identified in integration review r2 issue 7 are corrected below. |

At r1 the only numerical interpretation disagreement concerned the eg
runtime label: the saved timing fields measured wall time despite the then
CPU label. This r2 response agrees with the reviewer and corrects that label.
For item 10, the parent's checks link to the saved response sections above;
they are not a second independent review. No gap-cell correction was
needed.

## Final gap check

**Scientific evidence still missing: none for the stated claims, if
they retain the assumptions and limits above.** Environment and timing
metadata are now collected to the extent the records allow; complete
original per-run environments and CPU times were not recorded. Source
licence facts are documented, but the paper's data/code release licence
and final third-party notices remain to be chosen/prepared. Saved
models, certificate inputs/outputs, exact primal definitions, independent
reviews, prior-literature context, solver versions/settings/raw outcomes,
and a relocated reproduction package cover each result family. The work
supports certificates, optimum enclosures and bounded-budget comparisons;
it does not require resolving every MINLPLib instance or reproducing an
identical optimizer endpoint on every machine.

**Release preparation still pending:** choosing the data/code release
licence and preparing third-party notices; publishing a persistent public
archive with a DOI and a data/code-availability statement; adding the
required MINLPLib, QPLIB, MATPOWER and Göß–Burlacu–Martin publisher-correction
citations; presenting timings as wall times from reproduction runs on a
shared machine; and committing the complete dependency set when authorized.
Source copies stay local and untracked, with hashes in tracked manifests;
the public data release must not redistribute copyrighted sources.

**Open user decisions:** file the drafted SCIP report; optionally notify
MINLPLib maintainers about invalid listed bounds and BARON developers about
the two contradicted optimality claims; rerun the 10 overloaded or 3
memory-limited solver runs; and choose the release licence. No outside
contact or solver rerun was performed by this task.

The independent integration review r2 found issues (0 blockers, 1 major,
8 minor). This response resolves all nine findings. Items 2 and 15 of r1
were resolved by the package owner; the residual displays in r2 issue 7
are now corrected. The maps and manifest were rebuilt on 2026-10-04 and
the default package check passed. These are implementation checks, not a
new independent review verdict.
Upstream filing and additional solver reruns are decisions, not missing
proofs for the claims currently stated. Formal machine verification of
A1/A2, exact transport to related models, full unscreened-bound coverage,
and comparative speed rankings would require new work if added as claims.


## Response to integration review r2

The [review](reviews/integration-review-r2.md) returned **issues**: 0 blockers,
1 major and 8 minor. I checked the review evidence before changing each
claim, using my own exact Fraction arithmetic for the numbers. The
[exact evidence](integration/review-r2-evidence.log) and
[commands/results](integration/commands.md) record this implementation.

| issue | resolution |
|---|---|
| 1, major: ignored literature | Negation rules expose the literature reports, checks, logs and source manifests while keeping all copied sources local and ignored. files-to-commit.json excludes those copies. git check-ignore and status checks confirm the policy and unchanged root literature/ status. Copyrighted sources must not be redistributed in the paper data release. |
| 2: historical closeness | Exact checks give 1.2157e-6 and 3.8248e-5; upward bounds are 1.3e-6 and 3.9e-5 in the summary, this record and the control report. |
| 3: SCIP seeds | Summary and audit now state seed and version dependence; p4 failed for all 10 tried seeds on 10.1.0 and GAMS/SCIP. Raw scan logs were checked. |
| 4: timing labels | EG report, summarize.py and reproduction README now say wall time summed over chunks. The original independent review has an appended clarification. Timing data are unchanged; no full recheck was rerun. |
| 5: readiness and rebuild ownership | r1 items 2 and 15 are resolved. This implementation task owns and completed the final map/manifest rebuild and default package check on 2026-10-04. The all-leaf scopes are explicit above. |
| 6: source terms | optrove/sif is MIT; ralna/SIF is BSD. MATPOWER data terms retain "in most cases" and cite manual 8.1. MATPOWER and QPLIB citation requests are recorded. |
| 7: displays and prose | EG and water primal displays round upward from saved exact objectives; the water gaps round upward. Martin is spelled consistently. All 13 former tolerance-only closures now have exactly feasible points. The all-leaf EG status is current. |
| 8: package evidence and smoke tool | Recorded-tree inputs include the pinned OSIL, listed point and producer modules; interval samples include OSIL and sample C's minF inputs. eg_disc_s maps the binding part-1 bound and documents its binary64 caveat. The smoke tool writes fresh output, cleans its temporary scientific copy and documents bwrap/strace. |
| 9: wording and records | Fixed the case typo, Gurobi 13.0.0/status caveat, audit date and WSL2 VM scope. Parent-check statements link to saved response sections and retain the distinction from an independent review. |

Final commands ran in the required order: build_result_maps.py,
rebuild_manifest.py, default check_package.py, then the targeted relocated
EG smoke checks. All passed. Scientific scripts ran only in disposable
copies, sequentially with one BLAS/OpenMP thread and at most four CPU cores.
The existing 25 package smoke records were revalidated by the default
check; the three EG smoke checks were executed afresh. No project-wide
verification, CI inspection, staging, commit, push or outside contact occurred.

There is no disagreement with the review. Publishing an archive, release
licence choice, citations, upstream filing, optional notifications and solver
reruns remain the paper-preparation decisions listed above.
