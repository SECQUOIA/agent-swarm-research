"""Write review handoff artifacts from the checked issue inventory."""
from pathlib import Path
import json,hashlib,difflib
p=Path(__file__).resolve().parents[2];d=Path(__file__).resolve().parent
issues=json.loads((d/'issues.json').read_text())
reviews={'primal/chain':'primal-chain-review-r1','primal/dtoc5-lukvle10':'primal-dtoc5-lukvle10-review-r1','primal/lnts':'primal-lnts-review-r1','primal/powerflow':'primal-powerflow-review-r1','primal/water-ann-kan':'primal-water-ann-kan-review-r1','audit-ir':'audit-ir-review-r1','eg-recheck':'eg-recheck-review-r1','scip-bug':'scip-bug-review-r1','literature/control':'lit-control-review-r2','literature/network':'lit-network-review-r2'}
summary='''# Minor review fixes

Completed 2026-10-03: checked and resolved all 57 minor issues in the ten authorized tracks. Each report ends with a response table. No main computation or solver campaign was repeated. No commit, push, external message or SCIP submission was made. The main summary, audit report and other tracks were not edited.

Every final targeted check passed. [commands.md](commands.md) records the exact commands and results; [PROGRESS.json](PROGRESS.json) records completion and the absence of background jobs. The report changes are in [report_changes.patch](report_changes.patch). Numerical point data were preserved; the seven ANN/KAN point JSON changes correct only the interval-format description.

## Integration changes

These changes are recorded for the integrating agent; they have not been applied outside the owned tracks.

- Remove the obsolete no-exactly-feasible-point statement for chain50–400, lnts50–400, dtoc5, lukvle10 and powerflow0030p/0039p/0039r. The reports give the exact point definitions and proof assumptions.
- Use upward primal displays 41869.0515113203 for powerflow0039p and 41869.0515113210 for powerflow0039r. Preserve the reported enclosures.
- The compact chain range in the main summary is valid. Correct the overly rounded chain50/chain200 displays in the three older documents named in the chain report. State whether gaps use exact binary64 duals or safe decimal displays. The safe-display absolute gaps are at most 9.62e-15, 1.01e-14, 9.41e-15 and 1.01e-14.
- For lnts, 5.5e-13 describes gaps against full verifier duals; displayed-summary duals give about 5.8e-13–6.2e-13. For lukvle10, put the remaining gap on the dual side only conditionally on the KKT point being the global minimizer.
- Audit Section 2: retain the 8-decimal display limit, remove the claimed 10-significant-digit limit, and define the count convention (35/38/46). Qualify spring's five (i-r) pairs as explainable by rounding; the underlying solver bounds are unknown. No audit class or flagged-pair count changes.
- For eg_all, state A1/A2 for the all-leaf result: 1,114,361 checked leaves. The rigorous interval sample has 10,404 leaves. The 98,234 exclusions mean no feasible point with objective below θ*, not all leaves are side-infeasible. Only 85,685 are directly side-infeasible; 373 use Farkas and 12,176 splits. Distinguish the earlier 1,152,830 processed-leaf count.
- Any SCIP diagnostic totals should read 0/122 versus 78/122 matched defaults. Keep the limits on the instrumented mechanism and examined binary64 solutions. The report and draft remain unsubmitted.
- Update literature wording: all-four camshape maximum bound difference 4.7e-10; Waki tested M = 600–1000; distinguish cumene source versions; cite prior certified OPF work by Oustry et al.; restrict novelty to the stored MINLPLib models. Rigorous 0030r bound transport to 0030p requires a perturbation argument. Label Huang extended-model values and the separate 5-period gap.
- Preserve existing round-1 integration notes, including the ANN finite-dual wording correction and the literature status labels. The remaining issues below do not change those labels.

## Issue inventory

| track / review | issue | resolution and evidence | integration change |
|---|---|---|---|
'''
for track,rows in issues.items():
 for i,title,res,integ in rows:
  esc=lambda x:str(x).replace('|','\\|').replace('\n',' ')
  summary+=f'| [{track}](../../{track}/report.md) / [{reviews[track]}](../{reviews[track]}.md) | {esc(i)}. {esc(title)} | {esc(res)} | {esc(integ)} |\n'
summary+='''
## Remaining limits

The JOTA publisher full text for cumene remains unchecked; the arXiv and dissertation results are kept separate. Huang's 2011 MSc thesis, the original Hijazi report and the AIChE 2025 KAN abstract remain unobtained. Some Crossref requests failed (429 or 404); saved primary paper headers supply titles where available, and the errors remain in the metadata JSON. The MINOTAUR default-bound inference uses saved master source, whose rule may differ from the benchmark revision. Rounded twin models do not justify exact certificate transport without a perturbation proof. These are documented limits, not unfinished minor fixes.
'''
(d/'summary.md').write_text(summary)
patch=''
for track in issues:
 old=d/'before'/f'{track.replace("/","__")}.txt';new=p/track/'report.md'
 patch+=''.join(difflib.unified_diff(old.read_text().splitlines(True),new.read_text().splitlines(True),fromfile=f'before/{track}/report.md',tofile=f'after/{track}/report.md'))
(d/'report_changes.patch').write_text(patch)
# Complete source provenance for newly added supporting files.
entries=[('literature/control','QuadHandler_master_r2.cpp','saved reviews/lit-control-r2/web/minotaur/QuadHandler.cpp; GitHub master fetched 2026-10-02'),('literature/control','qplib/QPLIB_8585.sol','https://qplib.zib.de/sol/QPLIB_8585.sol; fetched 2026-10-03; matches saved r2 hash'),('literature/network','oustry2022_pscc22.txt','pdftotext -layout of oustry2022_pscc22.pdf')]
for n in [162,190]:
 for suffix in ['', '_comments']:
  entries.append(('scip-bug',f'issue_{n}{suffix}_20261003.json',f'https://api.github.com/repos/scipopt/scip/issues/{n}'+('/comments' if suffix else '')+'; fetched read-only 2026-10-03'))
for track,name,origin in entries:
 src=p/track/'sources';file=src/name;data=file.read_bytes();manifest=src/'MANIFEST.md'
 if not manifest.exists():manifest.write_text('# Minor-review source manifest\n\nFetched read-only; no issue or comment was submitted.\n')
 text=manifest.read_text()
 if f'| `{name}` |' not in text:
  with manifest.open('a') as out:
   if track!='literature/network' and '## Minor-review revision (2026-10-03)' not in text:out.write('\n## Minor-review revision (2026-10-03)\n\n| file | origin | bytes | sha256 |\n|---|---|---|---|\n')
   out.write(f'| `{name}` | {origin} | {len(data)} | `{hashlib.sha256(data).hexdigest()}` |\n')
print('wrote summary with',sum(map(len,issues.values())),'issues; report diff and added-source manifest entries')
