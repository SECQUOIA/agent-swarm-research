"""Write the track-only round-3 response and report response sections."""
from pathlib import Path
import json

W = Path(__file__).resolve().parent
P = W.parents[1]
R = P.parent

def snapshot(f):
    dest = W / 'before-r3' / f.relative_to(R).as_posix().replace('/', '__')
    if not dest.exists():
        dest.write_bytes(f.read_bytes())

tracks = {
    'primal/chain': [(3, 'Corrected the authorized older chain dual displays and the chain50/chain200 COPS gaps to 9.7e-15/9.4e-15. Qualified the historical “as claimed” sentence.'),
                     (10, 'Clarified that only the first two listed older documents used the chain200 value.')],
    'primal/lnts': [(3, 'Corrected the older lnts100/lnts200 margin-1e-12 displays and lnts200/lnts400 margin-1e-10 displays downward; exact checks include h2 printing uncertainty.'),
                    (7, 'Corrected the rational-point proof to 45/(100h), defined trapezoid weights and listed logs/review_r2_check.log.'),
                    (11, 'Escaped the control-magnitude pipes in the response table.')],
    'primal/powerflow': [(11, 'Escaped the four norm pipes in the uniqueness response row.')],
    'primal/water-ann-kan': [(10, 'Fixed the introduction comma splice and the dangling gap-display clause.'),
                             (11, 'Recorded the waterno2_06 1.67% → 1.68% edit in both round-2 response tables and added the existing check log to FILES-r2.json.')],
    'audit-ir': [(9, 'Replaced the display-limit justification by the explicit conservative-floor choice; defined the 35/38/46 counts as displayed entries in the remaining sentence.')],
    'scip-bug': [(1, 'Separated the three refuted wrong claims from tiny2’s correct default optimum and pair2236 seed 0’s unrefuted low claim; retained the five-vector binary64 scope.'),
                (8, 'Removed the seeds-8-and-14 restriction from Section 5.3’s mechanism scope and restored the 10.0.2/10.0.3 fm336 acceptance citation in the report body. The table has 14 rows covering 15 runs: one p5 row combines seeds 0 and 2.')],
    'literature/control': [(11, 'Added the missing round-2 ≤ 5.55e-13 disclosure. The reference checker now parses 99,997/99,983 from saved warnings and computes 14 by subtraction; it also prints the minimum listed coordinate. Reran it in a disposable copy and saved its output.')],
}
for track, rows in tracks.items():
    f = P / track / 'report.md'
    snapshot(f)
    rel = '../../reviews/' if '/' in track else '../reviews/'
    part = ['### Round 3: independent minor-fixes review (2026-10-03)', '',
            f'Review: [minor-fixes-review-r2.md]({rel}minor-fixes-review-r2.md). Issue numbers below refer to that review.', '',
            '| issue | resolution and evidence |', '|---|---|']
    part.extend(f'| {n} | {text} |' for n, text in rows)
    preservation = ('Saved sources and point data were preserved; only the reference-check output log was refreshed.'
                    if track == 'literature/control' else 'Scientific logs and point files in this track were preserved.')
    part.extend(['', f'Targeted checks and the full response: [response-r3.md]({rel}minor-fixes/response-r3.md), [check_r3.log]({rel}minor-fixes/check_r3.log) and [commands-r3.json]({rel}minor-fixes/commands-r3.json). Scientific scripts were run only in disposable copies. {preservation} No solver campaign or project-wide check was run.', ''])
    marker = '### Round 3: independent minor-fixes review (2026-10-03)'
    f.write_text(f.read_text().split(marker)[0].rstrip() + '\n\n' + '\n'.join(part))

response = '''# Response to the independent minor-fixes review, round 3

Review: [minor-fixes-review-r2.md](../minor-fixes-review-r2.md). Date: 2026-10-03. This implementation addresses the assigned track-level items 1, 3, 7, 8, 9, 10 and 11. Items 2, 4, 5 and 6 belong to the separate integration agent. Neither `research-20260929/open-instances-summary.md` nor `research-20260929/bound-audit/audit-report.md` was edited here. `publication/reproduction/` and `publication/solver-runs/` were not edited. The SCIP draft was not sent. No commits, pushes or outside contact occurred.

The reviewer’s evidence was checked directly in the report bodies, saved solution/acceptance logs, lnts construction and certificate data, saved MINOTAUR warning counts, and the historical patch and inventory. Exact Fraction checks and GNU patch checks are recorded in [check_r3.log](check_r3.log). The changed scientific checker was run in a disposable copy, with one numerical thread per process and a two-core affinity limit. No project-wide verification or CI status/log inspection was performed.

| item | resolution and evidence |
|---|---|
| 1. SCIP five-solution overclaim | Used the reviewer’s replacement. Only pumps_default (1.198), p0 seed 0 (169.9503) and pair2236 seed 7 (65.124) are refuted wrong claims. `scip-bug/logs/binary64_scip_solution.log` reports tiny2’s correct −1.337; `scip-bug/logs/pair_semantics.log` reports seed 0’s unrefuted 55.68977300185796. All five examined vectors fail exact binary64 feasibility; no conclusion is drawn about other scanned vectors. |
| 3. Older chain/lnts displays | Applied the named chain50/chain200 safe-display corrections directly to the COPS report and verification report; applied the chain50 correction to closing-audit-a and solver-campaign-review-r1. Updated the two COPS gap cells to 9.7e-15 and 9.4e-15 and qualified the original verification gaps as measured against the original binary64 displays. Corrected lnts100’s 0.5545954011663566 to …3565 in open-instances verification and closing-audit-a; corrected lnts200’s …1025291 to …1025290 and …047626 to …0476259, and lnts400’s …6452299 to …6452298 in open-instances verification. Exact checks bracket the printed h2 values and verify all four downward replacements. These older-document edits are already applied; their original round-2 integration replacements should not be reapplied. The solver-runs correction remains outside this task. |
| 7. lnts proof/files | Changed 45/(50h) to 45/(100h) and defined w = (1/2, 1, …, 1, 1/2). Summing the velocity recursion gives 100h Σ w_j cos θ_j. Listed the existing `logs/review_r2_check.log`; preserved its bytes. |
| 8. SCIP mechanism scope/evidence | Removed “(seeds 8 and 14)” from the sentence covering all instrumented Section 5.3 cutoffs. Restored `../reviews/scip-bug-r1/rv_runs.log` as body evidence of fm336 witness acceptance by 10.0.2/10.0.3 (lines 55–57 and 155–157); the developer-facing draft is unchanged. **Count qualification:** the review says 14 runs, but the table has 14 rows covering 15 runs, since the dbgsol 10.0.2 p5 row combines seeds 0 and 2. Both saved seed logs exist and record the cubic reverse-propagation cutoff. This does not change the requested scope correction. |
| 9. audit-ir wording | Replaced the remaining page-display-limit assertion with the conservative-floor choice and no-screened-pair-change result. Defined the remaining 35/38/46 count sentence as displayed entries. The saved audit check reports 0 of 158 screened pairs affected and the three count definitions; no numerical audit result changed. |
| 10. Water/chain wording | Split the water introduction into two sentences and made the upward-display sentence explicitly refer to the exactly feasible point’s gap. Clarified that the chain200 value appears only in the first two of the five named older documents. |
| 11. Records/tables/checker | Added the existing water check log to `FILES-r2.json`. Added the control ≤ 5.55e-13 and waterno2_06 1.67% → 1.68% disclosures to the track round-2 response tables and `response-r2.md`. Added the final strengthened `check_r2.py` rerun to `commands-r2.json`, explicitly marked retrospective. Regenerated the round-1 patch from `before/` and final round-1 `before-r2/` report snapshots; GNU patch applies it and reproduces all ten snapshots byte for byte. Escaped the pipes in the lnts/powerflow response rows. The control checker parses the saved warning counts, subtracts them to obtain 14 extra finite lower bounds, and prints the saved minimum/maximum coordinates; its output was refreshed from a disposable copy. The current command handoff is covered by the round-3 patch; no missing historical commands.md snapshot was invented. |

The only disagreement is the item-8 distinction between 14 table rows and 15 instrumented runs. All requested fixes were made. Round-3 response sections were added to the seven affected track reports. Exact executed commands and results are in [commands-r3.json](commands-r3.json); the round-3 write inventory and diff are in [FILES-r3.json](FILES-r3.json) and [report_changes_r3.patch](report_changes_r3.patch). FILES-r3 paths are relative to research-20260929. Historical round-2 artifacts remain historical; their original validator is not a post-integration validator. The first round-3 check passed the data/text/preservation checks but rejected the regenerated patch because the original control report lacked a terminal newline. The generator now emits GNU’s missing-newline marker; the rerun passed.
'''
(W / 'response-r3.md').write_text(response)

f = W / 'commands.md'
snapshot(f)
f.write_text(f.read_text().split('## Round 3 (2026-10-03)')[0].rstrip() + '''

## Round 3 (2026-10-03)

Assigned track-level items: 1, 3, 7, 8, 9, 10 and 11 of minor-fixes-review-r2.md. The exact executed commands, including evidence reads and disposable-copy setup, are in [commands-r3.json](commands-r3.json). The targeted arithmetic, Markdown, preservation and GNU patch checks are in [check_r3.log](check_r3.log); the control reference checker output is in [dtoc5_reference_r3.log](dtoc5_reference_r3.log). Scientific scripts were never imported or executed in the main tree. Numerical checks used one thread per process and at most two CPU cores. No solver campaign, project-wide check or CI inspection was run.

The missing final round-2 check_r2.py rerun is now recorded retrospectively in commands-r2.json. The regenerated round-1 patch uses final round-1 before-r2 report snapshots, without round-2 or round-3 edits. commands.md had no before-r2 snapshot and was edited after the round-2 patch; the round-3 snapshot and patch cover its current update without fabricating a historical baseline.
''')

f = W / 'PROGRESS.json'
snapshot(f)
progress = json.loads(f.read_text())
progress['round3'] = {
    'status': 'complete', 'review': '../minor-fixes-review-r2.md',
    'assigned_items': [1, 3, 7, 8, 9, 10, 11],
    'addressed_items': [1, 3, 7, 8, 9, 10, 11],
    'separate_integration_items': [2, 4, 5, 6],
    'partial_disagreements': {'8': '14 table rows cover 15 instrumented runs; p5 seeds 0 and 2 share one row.'},
    'cpu_limit': 2, 'background_jobs': [],
    'commands': 'commands-r3.json', 'validation': 'check_r3.log',
    'scope': 'Track-level reports, named older-document corrections and minor-fixes records only; integration files, reproduction and solver-runs untouched.'
}
f.write_text(json.dumps(progress, indent=2) + '\n')
print('Wrote round-3 response, seven report response sections and command/progress handoff.')
