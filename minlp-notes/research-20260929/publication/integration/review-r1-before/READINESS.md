# Publication readiness

Updated 2026-10-03. Scope: the September 29 certificates and listed-bound
audit, with the completed publication tracks integrated into
[open-instances-summary.md](../open-instances-summary.md) and
[audit-report.md](../bound-audit/audit-report.md). The summary's checked
bounds and upward gap displays are authoritative for the paper; older
notes sometimes retain shorter, unsafe rounded displays.

The evidence supports a computational paper with the limits below stated
explicitly. Final packaging remains pending. This record does not claim
that every revised report received a new independent review: it preserves
the latest review's actual verdict and distinguishes the subsequent
response from that verdict. Reviewers are the independent verifiers named
in the linked reviews; the reproduction reviewer identifies itself as
Claude. No new reviewer was commissioned during this integration.

## Evidence by result family

Paths in this record are relative to publication/ unless a link points
elsewhere. "Verified" means the review's verdict, under the stated
arithmetic and model assumptions. Except where an attained exact optimum
is proved, a closure is an optimum enclosure with the summary's gap.

| paper claim/result family | evidence and independent review | verification status | caveats and what is not established |
|---|---|---|---|
| lnts50/100/200/400 duals and exactly feasible primals | [original verification](../reviews/open-instances-verification/verification-report.md); [primal report](primal/lnts/report.md), points/ and logs/; [independent primal r1](reviews/primal-lnts-review-r1.md) | Original dual verified; primal r1 **verified**, with minor issues addressed in the report and minor-fixes responses. | Point is defined by a reduced-system existence proof, not a rounded .sol vector. Reviewer checked existence using its own intervals and exact rational trigonometric bounds. Gap uses the summary dual display; no new smaller-margin dual was computed. Prior floating-point results are partly known. |
| dtoc5 certificate and exact rational point | [original verification](../reviews/open-instances-verification/verification-report.md); [primal report](primal/dtoc5-lukvle10/report.md), points/dtoc5_point.txt.gz and exact objective log; [independent primal r1](reviews/primal-dtoc5-lukvle10-review-r1.md) | Dual verified; primal r1 **verified**, minor issues addressed. Integration independently recomputed the OSIL objective exactly. | Certificate is for the stored MINLPLib coefficient, which differs from CUTEst by a factor of 4. Prior MINOTAUR floating-point closure assumed default bounds. Exact feasibility does not establish the numerical point's local-minimizer claim. |
| lukvle10 certificate and exact feasible point | Same [original verification](../reviews/open-instances-verification/verification-report.md) and [primal track/review](primal/dtoc5-lukvle10/report.md); logs/lukvle10_enclose.json | Dual verified; independent primal r1 **verified**. | The point is defined by exact seeds and recurrence, with an objective enclosure. KKT agreement is numerical; saying the remaining gap comes only from the dual is conditional on the KKT point being globally minimizing. |
| camshape100/200/400/800 exact optima | [original verification](../reviews/open-instances-verification/verification-report.md); exact rational comparison/envelope proofs; [control literature](literature/control/report.md) | Exact attained optima independently verified; literature r2 **verified**, with minor issues subsequently addressed. | camshape100 was already solved globally in floating point. camshape200 has an older uncheckable closure listing. QPLIB copies differ by rounded constants; the camshape800 contradiction on the QPLIB copy is strong evidence, not a transported exact proof. |
| optcdeg2 quadratic calibration and feasible point | [bang-bang report](../theory-bangbang/report.md); [independent verification](../reviews/bangbang-verification/verification-report.md), logs/qcal_exact.json and primal_check.json | Exact rational calibration verified; primal existence verified. Integration checked the rounded certificate label and the gap exactly. | Displayed dual is rounded down, not the exact certificate value. Stored MINLPLib damping differs from the CUTEst source by a factor of 4. Older global closure listing has no retained value/log. |
| hvycrash constant objective and explicit witness | [small verification](../reviews/wave2-small-verification/verification-report.md); [small literature](literature/small/report.md), SIF bound-card checks | Exact identity and witness verified; latest literature review r3: **issues**, no blocker or major issue; four minor corrections addressed in the report. | Same CUTE problem at N=50. The value was already listed; novelty is the identity and witness, not discovery of the value. This does not establish physical validity of the source model. |
| ex6_2_5/ex6_2_7, etamac and pricing050 certificates | [small verification](../reviews/wave2-small-verification/verification-report.md), per-instance logs; [small literature](literature/small/report.md) | Independent certificate verification **verified**. Integration checked bounds, primal display directions and upward gaps using saved endpoints. | ex6_2_* may have earlier ε-global floating-point results in unread sources. For pricing050 the summary uses conservative subtraction of safe displays because the saved log does not retain the full exact primal objective. Sources' scaled models and values are not automatically interchangeable. |
| chain50/100/200/400 exact points and duals | [COPS verification](../reviews/cops-verification/verification-report.md); [primal report](primal/chain/report.md), points/*_generator.json and *_box.json; [independent primal r1](reviews/primal-chain-review-r1.md) | Dual independently verified; primal r1 **verified**, minor issues addressed. | Exact algebraic points, not rounded numerical vectors. Summary gaps use safe individual decimal duals, not the compact range. Some older detailed reports contain unsafe shortest decimal forms; use the summary and saved exact binary64 values. |
| catmix100/200/400/800 DP certificates and exact primal policy values | [COPS verification](../reviews/cops-verification/verification-report.md); [catmix recheck](../reviews/catmix-recheck.md); [exact display record](reproduction/cops/logs/exact_display_checks.json) | All four duals independently recomputed; catmix recheck confirmed the later 400/800 certificates. Integration checked all four exact-point gaps. | OSIL coefficients differ slightly from GAMS text. Claim is for OSIL; no exact transport to GAMS or COPS 3.0 is established. The summary uses stronger verifier duals, exact author points for 100/200/400, and the verifier policy point for 800 rather than the short Newton display. |
| powerflow0030p/0039p/0039r bounds and exactly feasible primals | [wave-3 verification](../reviews/wave3-verification/verification-report.md); [0039 review](../reviews/powerflow0039-review.md); [primal report](primal/powerflow/report.md), certify logs; [independent primal r1](reviews/primal-powerflow-review-r1.md) | Exact dual evaluation/PSD proof and leaf certificates independently verified; primal r1 **verified**, minor issues addressed. | Exactly feasible point existence uses outward enclosures; reviewer used its own rational intervals. MINLPLib 0030p drops two shunts, and 0039p/r drop taps. Rounded 0030p/r twins do not permit rigorous bound transport without a perturbation proof. New numerical solves need not recover the saved certificate. Prior certified ACOPF exists on other models. |
| pindyck concavity certificate and feasible point | [extension](../open-instances-wave2/small/pindyck-extension.md); [independent review](../reviews/pindyck-review.md), primal_check.txt | Independent rebuild **verified**; integration checked the gap from the saved primal value with a last-digit allowance. | COCONUT's better value belongs to a mistranslation. No claim is made for that different model or for unrelated numerical solves. |
| eg_int_s/eg_disc_s/eg_disc2_s duals and primal witnesses | [retry note](../open-instances-wave3/eg/retry.md); [independent retry review](../reviews/eg-retry-review.md); [all-leaf report](eg-recheck/report.md), rec/, res/ and logs/; [independent all-leaf r1](reviews/eg-recheck-review-r1.md) | Retry independently verified. All-leaf r1 **verified**, minor issues addressed. Run G has 1,114,361 certified leaves, zero failures; 1,152,830 counts processed boxes. Integration independently summed the chunk totals. | All three dual certificates use A1 (hand-checked float-padding error analysis) and A2 (sampled numpy exp relative-error assumption). Coverage has an exact independent proof. Only a separate 10,404-leaf sample in parts 0 and 2–7 was re-certified with outward intervals without the libm assumption. Uniform exp accuracy and assumption-free certification of every leaf are not established. eg_int_s had prior floating-point closure; CAMINO Gurobi claims are refuted, with cause and exact termination status unknown. |
| waterno2_06/09/12/18/24 improvements and exactly feasible points | [wave-2 verification](../reviews/waterno2-verification/verification-report.md); [later-period review](../reviews/waterno2-recheck.md); [separator review](../reviews/waterno2-sepbranch-review.md); [cell-slope review](../reviews/waterno2-cellslopes-review.md); [primal report](primal/water-ann-kan/report.md) and [independent primal r1](reviews/primal-water-ann-kan-review-r1.md) | Period and separator certificates independently verified, including every cell-pair bound in the cell-slope review; primal r1 **verified**, minor issues addressed. Integration recomputed all five OSIL objectives exactly. | Points use exact rational/algebraic definitions. These five gaps remain nonzero; no closure is claimed. Huang's related extended models differ, and the cited MSc thesis was not obtained. |
| ann_cumene_tanh finite bound and exact feasible point | [extension](../open-instances-wave3/ann/extension.md); [independent extension review](../reviews/ann-extension-review.md); [primal report/review](primal/water-ann-kan/report.md); [network literature](literature/network/report.md) | Extension independently re-certified; primal r1 **verified**. Current upward gap is 0.195%. | Primal existence uses forward definitions and assumes mpmath iv outward rounding. No closure. Exact exp twin was already closed in floating point; our finite bound is weaker than those claims. Novelty is restricted to the rigorous bound found for this stored model. |
| six KAN models: exact OSIL infeasibility and enclosure of R | [wave-3 verification](../reviews/wave3-verification/verification-report.md); [primal report/review](primal/water-ann-kan/report.md), six point JSONs; [network literature](literature/network/report.md) | OSIL inconsistency proved; R duals independently verified; primal r1 **verified**. All six current gaps checked exactly in integration. | Original OSIL models have no exactly feasible point. R drops partition rows and additional intermediate restrictions. The network-point enclosure assumes mpmath iv; no feasible OSIL point or OSIL optimum is asserted. Largest absolute gap is 2.42e-8; a blanket 1e-10 absolute claim would be false. Published n4/n5 optimal values are tolerance artifacts. |
| listed-bound audit: class (i), emfl bounds and remaining classes | [audit report](../bound-audit/audit-report.md); [first verifier](../reviews/bound-audit-verification/verification-report.md); [recheck](../reviews/bound-audit-recheck.md); [last confirmation](../reviews/audit-confirm-r2.md); bound-audit results.json and certificate logs | All 19 class (i) pairs and four emfl optimum enclosures confirmed independently. Three confirmation rounds; last verdict **verified**, no remaining problem. Integration retains the classifications and checks the emfl relative lower display. | Gross/tolerance-scale are size labels. Small exact conflicts need not mean solver bugs under unknown original settings. Class (ii)-repair does not prove dual validity; class (iii) is undecided. Display ties and unscreened invalid bounds are not resolved. Physical plausibility is not established for glider100. |
| class (i-r), parsing and screen | [audit-ir report](audit-ir/report.md), check_ir/spring_global/parse/digit logs; [independent r1](reviews/audit-ir-review-r1.md) | r1 **verified**, minor issues addressed. All 12 pairs independently re-proved; parser and screen independently checked. | Literal displayed numbers are contradicted. Five spring entries can be explained by page rounding; underlying solver bounds are unknown. Earlier six-digit rounding of the other seven is supported but not proved. No additional class (i) pairs are asserted. |
| MINLPLib refresh and historical model identity | [status report](minlplib-status/report.md), data/part_a.json, exact_forms/listing/history logs; [r1](reviews/minlplib-status-review-r1.md), [r2](reviews/minlplib-status-review-r2.md) | r1 independently confirmed refresh; r2 **issues**, with the earlier major issue resolved and four minor corrections addressed in the report. | Relevant status unchanged at the saved 2026-10-02 refresh. Three ghg_3veh constants changed by rounding; old-text contradiction survives. Archive gaps and truncated captures limit historical completeness. Numerical row agreement is evidence, not an algebraic identity proof. Report Table B1 supersedes the older data table. |
| literature priority and model provenance | [control report](literature/control/report.md)/[r2](reviews/lit-control-review-r2.md); [network report](literature/network/report.md)/[r2](reviews/lit-network-review-r2.md); [small report](literature/small/report.md)/[r3](reviews/lit-small-review-r3.md), saved source manifests | Independent reviewers: control rounds 1–2, latest **verified**; network rounds 1–2, latest **verified**; small rounds 1–3, latest **issues**, no blocker/major issue. Subsequent minor-fixes/report responses address the listed issues. | Searches cannot prove novelty. Unread sources, unavailable old logs, rounded QPLIB copies, source scaling differences and cumene source-version discrepancies remain explicit. No unconditional priority claim or blanket “previously unsolved globally” claim is supported. |
| matched-budget solver comparison | [campaign report](solver-runs/report.md), [table](solver-runs/results_table.md), results_table.csv, run.json/trace/logs; [setup r1](reviews/solver-campaign-review-r1.md); [final-analysis r1](reviews/solver-analysis-review-r1.md) | Independent final-analysis verdict **issues**; raw values/counts confirmed. The final report and tables incorporate globality disclaimers, first-batch overload and the minor interpretation corrections. Integration independently recounted and compared every finite dual with exact source decimals. | BARON 26.5.27/GUROBI 13.0.2/SCIP 10.0.3, 3600-second solver limit, one thread. Zero accepted closures; BARON's two claims conflict with certificates. Six BARON values lack a globality guarantee, six SCIP comparisons use tightened models, and KAN comparisons use R. Ten overloaded-batch rows and three SCIP memory stops limit benchmarking. No ranking, isolated-core timing or failure under other budgets/settings is established. |
| SCIP wrong-optimal-value bug | [SCIP report](scip-bug/report.md), witnesses, minimal models, debug traces and source snapshots; [independent r1](reviews/scip-bug-review-r1.md) | r1 **verified**; exact witnesses reproduced independently. The [round-3 response](reviews/minor-fixes/response-r3.md) corrects the scope: Section 5.3 has 14 rows for 15 instrumented runs, and only three of the five examined solutions have refuted wrong claims. | Traced mechanism applies to instrumented wrong runs, not all SCIP results. Low cell-pair claims are not refuted. Exact infeasibility of examined returned binary64 vectors was not checked for every scan. Upstream report is drafted and NOT submitted; no maintainer confirmation or fix is established. |
| reproduction and portability | [README](reproduction/README.md), [report](reproduction/report.md), maps, manifest, archived inputs, command index, strict relocated smoke logs; [independent r1](reviews/repro-package-review-r1.md) | Independent reviewer Claude, r1 **issues**, no blocker; dependency-list major issue and minor packaging issues addressed in the package response. Final manifest intentionally awaits integration. | Replay is distinguished from regeneration. The audit topopt p5 displays use the committed certificate; one-BLAS-thread regeneration selects a different valid point. Optimizer endpoints, QR basis and long wall-limited frontiers are not promised identical across builds or loads. Final map/manifest synchronization and commit dependencies remain to be checked. |
| numerical display and integration corrections | [minor-fixes list](reviews/minor-fixes/summary.md), integration-r2.json; [independent r2](reviews/minor-fixes-review-r2.md); [integration exact checks](integration/numbers.log), [objective recomputation](integration/objectives.log), [page/count/handoff checks](integration/publication-counts.log), [audit display replay](integration/audit-displays.log) | Minor-fixes rounds 1–2; latest verdict **issues**, while all 40 ordered replacements are explicitly confirmed correct. This implementation applied 33 owned replacements and validated the seven protected replacements on disposable copies. Current main-document gap cells, A1/A2, spring antecedent and three display/wording issues are resolved. | Six protected replacements are already applied by the round-3 owner; the historical solver-runs/report.prev.md display remains with its protected owner. Track-level round-3 corrections are recorded in response-r3.md. No protected replacement was applied or reapplied here. This integration is an implementation check, not a fresh independent review of the revised whole. No scientific search was rerun. |

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
solver-runs/report.prev.md display is outside both agents' edit scope and
remains with the solver-run owner. It does not override the current summary.
No protected file was edited by this integration. Final packaging is deferred
because integration changed summary rows and concurrent track edits can
invalidate hashes. It must be done after all those edits stop.

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
3. **Commit the publication work and final package refresh:** confirm the
   completed round-3 track fixes and arrange the remaining historical
   solver-runs/report.prev.md display correction with its owner, then commit
   the untracked publication files together with all modified dependencies
   named in the package's files-to-commit.json and the minor-fixes file
   lists. No commit or push was made here. Because this integration changes
   summary rows, rebuild the result maps before the final manifest:

   ```sh
   python3 research-20260929/publication/reproduction/tools/build_result_maps.py
   python3 research-20260929/publication/reproduction/tools/rebuild_manifest.py
   python3 research-20260929/publication/reproduction/tools/check_package.py
   ```

   Run rebuild_manifest.py and the default check_package.py immediately
   before the commit, after every covered edit is final. Require the
   default package check to pass; rerun both if any covered file changes.
   These steps write reproduction/ and therefore are recorded for its
   owner/user rather than run by this implementation task.

## Final gap check

**Scientific evidence still missing for the scoped computational paper:
none, if the claims retain the assumptions and limits above.** Saved
models, certificate inputs/outputs, exact primal definitions, independent
reviews, prior-literature context, solver versions/settings/raw outcomes,
and a relocated reproduction package cover each result family. The work
supports certificates, optimum enclosures and bounded-budget comparisons;
it does not require resolving every MINLPLib instance or reproducing an
identical optimizer endpoint on every machine.

**Release preparation still pending:** the protected historical
solver-runs/report.prev.md display cleanup; rebuilding the maps and
manifest after integration; a passing final package check;
and committing the complete dependency set when the user chooses. This
record does not call the archive frozen or commit-ready before those steps.
An independent review of this final integration has not been performed.
Upstream filing and additional solver reruns are decisions, not missing
proofs for the claims currently stated. Formal machine verification of
A1/A2, exact transport to related models, full unscreened-bound coverage,
and comparative speed rankings would require new work if added as claims.
