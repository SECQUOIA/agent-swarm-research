"""Write round-2 responses and the command handoff inside the authorized scope."""
import difflib
import json
from pathlib import Path

W = Path(__file__).resolve().parent
P = W.parents[1]
tracks = {
 'primal/chain': [(4,'Added the exact summary gap correction to ≤ 1.01e-14.'),(11,'Completed the older-display location list and corrected the COPS document description.')],
 'primal/dtoc5-lukvle10': [(2,'Checked the exact objective rational; recorded dtoc5 primal 5.389672119181141, with the dual unchanged.'),(12,'Qualified p5’s maximum row violation and removed the stale local-minimizer statement.')],
 'primal/lnts': [(1,'Corrected the invalid lnts100 summary-display claim; recorded primal 0.5545954011670.'),(8,'Rounded verifier dual displays downward; relative upper gaps to these safe displays are 1.01e-12 for all four instances.'),(9,'Made upper-gap rounding consistent and labelled the coordinate-distance range approximate.'),(10,'Supplied the linear-independence proof, labelled obsolete construction-width logs, checked reviewer rerun point bytes and completed the file list.')],
 'primal/powerflow': [(12,'Assigned the next inactive slacks to the correct three instances/rows; checked them by exact rational OSIL evaluation.')],
 'primal/water-ann-kan': [(3,'Changed waterno2_12 to 6.90% and added assertions against the exact rational percentage gaps.'),(20,'Corrected independent-review status and the interval-format code comment.')],
 'audit-ir': [(6,'Kept the 10th-digit floor as an explicit conservative choice: 0 of 158 screened pairs affected.'),(21,'Defined displayed-entry multiplicity, trailing integer zeros and the 17 tie pairs on three instances.')],
 'eg-recheck': [(5,'Corrected integration to eg_disc2_s and 1,152,830 processed boxes; independently recounted the saved results.'),(22,'Added the exact tree-free coverage proof to the headline coverage bullet.')],
 'scip-bug': [(17,'Restricted the mechanism sentences to instrumented seeds 8 and 14.'),(18,'Qualified low claims and the five examined binary64 solutions.'),(19,'Removed internal review/log references from the unsubmitted draft and listed saved sources/checker files.')],
 'literature/control': [(7,'Corrected the MINOTAUR integration cell.'),(13,'Corrected all separate lower/upper default rules: upper 100 is inferable, the negative lower default is unknown because of 14 extra finite lower bounds. Verified saved reference-point containment.'),(14,'Refreshed the four-pair comparison log and corrected the README.'),(22,'Fixed spacing and QPLIB coefficient/bound scales; marked the round-0 report superseded. Disagreement: the saved logs explicitly print gap percentages 5.9096 / 13.3380 / 20.8425; the report now cites them.')],
 'literature/network': [(15,'Scoped the remaining novelty claim to this MINLPLib model.'),(16,'Checked and corrected Müller Table 5 pp. 69/72 and single-author Göß 2026.'),(22,'Unified the VSDP URL, listed the checker, identified the checked Default log and clarified arXiv v2 Table 4.')],
}
for track,issues in tracks.items():
    f = P/track/'report.md'
    rel = '../../reviews/minor-fixes/' if track.startswith(('literature/','primal/')) else '../reviews/minor-fixes/'
    review = rel.replace('minor-fixes/','')+'minor-fixes-review-r1.md'
    part = ['### Round 2: independent minor-fixes review (2026-10-03)','',
            f'Review: [minor-fixes-review-r1.md]({review}). Issue numbers below refer to that review.','',
            '| issue | resolution |','|---|---|']
    part += [f'| {n} | {resolution} |' for n,resolution in issues]
    part += ['',f'Own exact checks and saved-source evidence: [check_r2.log]({rel}check_r2.log). The full response is [response-r2.md]({rel}response-r2.md); exact commands and results are in [commands.md]({rel}commands.md). Integration edits remain pending in the main summary and audit report. No main computation or solver campaign was repeated.', '']
    marker = '### Round 2: independent minor-fixes review (2026-10-03)'
    before = f.read_text().split(marker)[0].rstrip()
    f.write_text(before+'\n\n'+'\n'.join(part))

f = P/'primal/water-ann-kan/report.md'
s = f.read_text().replace('This is the 1.67% of the summary, now measured against an exactly feasible point.',
 'The old summary 1.67% is rounded to nearest. Use 1.68% for an upward two-decimal percentage display, now measured against an exactly feasible point.')
f.write_text(s)
f = W/'summary.md'
s = f.read_text().replace('Correct all invalid numeric primal displays as listed below.','Correct all invalid numeric primal displays in the exact list above.').replace('inferred from Default logs reading only limits/time = 7200','inferred from the checked Default R3_H1_N4.log reading only limits/time = 7200')
f.write_text(s)

records = json.loads((W/'commands-r2.json').read_text())
cmd = W/'commands.md'
text = cmd.read_text().split('## Round 2 (2026-10-03)')[0].rstrip()
text += '\n\n## Round 2 (2026-10-03)\n\n'
text += 'The preceding four-core statement describes round 1 only. Round 2 ran serially with one numerical thread per process and at most two CPU cores. No main construction, solver campaign, project-wide check or CI inspection was run. No commit, push or outside contact occurred.\n\n'
text += 'From the repository root, these preparation/edit commands were run:\n\n```sh\npython3 research-20260929/publication/reviews/minor-fixes/edit_r2.py\npython3 research-20260929/publication/reviews/minor-fixes/build_integration_r2.py\npython3 research-20260929/publication/reviews/minor-fixes/run_checks_r2.py\npython3 research-20260929/publication/reviews/minor-fixes/finish_r2.py\n```\n\n'
text += 'The serial runner executed these exact targeted commands; all exited 0:\n\n```sh\n'
text += '\n'.join(r['command'] for r in records)+'\n```\n\n'
text += 'Results: independent rational display/gap/bound/slack checks, audit-page recount, eg saved-array counts, lnts byte comparisons, current stored-box Krawczyk check, SCIP raw-log recount and exact small-model comparisons all passed. The four comparison outputs refresh `literature/control/checks/qplib_camshape_compare.log`; the QPLIB_2703 maximum is now 4.708e-10 at x1.up, not the stale lower-bound-only result. The saved dtoc5 reference-point check passed with the corrected default-rule qualification.\n\n'
text += 'The independent checker was also run directly during development, with the same environment and redirection shown above. Early runs exposed mistakes in that new checker: waterno2_06 was incorrectly assumed to lie below 282.888; waterno2_09 was incorrectly expected to need a correction; Unicode minus signs had not yet been normalized. Those assertions/input errors were fixed before the final successful run. These failures did not concern a main certificate. The checker was strengthened afterward to cover remaining duals and powerflow slacks, then rerun successfully.\n\n'
text += 'Read-only evidence inspection used `rg`, `cat`, `sed`, `head`, `tail`, scoped `git status`, and small Python reads of saved JSON, XML and page text. No new downloads were needed. Inline Python writes made scoped snapshots/progress records and small prose follow-ups; their final edits are retained in `report_changes_r2.patch`. All independent numerical checks are saved in `check_r2.py`; none were hidden in an inline numerical command.\n'
cmd.write_text(text)

prev = P/'literature/control/report.prev.md'
snapshot = W/'before-r2/literature__control__report.prev.md'
if not snapshot.exists():
    snapshot.write_text(prev.read_text().split('\n\n',1)[1])
patch = []
for before in sorted((W/'before-r2').iterdir()):
    path = before.name.replace('__','/')
    after = P/path
    assert after.is_file()
    patch += difflib.unified_diff(before.read_text().splitlines(True),after.read_text().splitlines(True),
                                fromfile='before-r2/'+path,tofile=path)
(W/'report_changes_r2.patch').write_text(''.join(patch))
print('Wrote all ten round-2 responses, command handoff and the scoped patch.')
