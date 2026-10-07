"""Summarize retained final lane runs; excludes explicitly archived pilots."""
from collections import Counter
from fractions import Fraction as F
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
lanes=('baseline','completed_grid','completed_exact','completed_recourse','completed_constraints','completed_sets')

def main():
    allrows=[];summary={}
    for lane in lanes:
        path=HERE/'results'/(lane+'.json')
        if not path.exists():continue
        rows=json.loads(path.read_text());allrows+=rows
        valid=lambda r:isinstance(r.get('certificate_check'),dict) and r['certificate_check'].get('valid') is True
        complete=lambda r:valid(r) and r['status'] in ('certified','exact','epsilon','epsilon_optimal','infeasible')
        summary[lane]={'runs':len(rows),'status_counts':dict(Counter(r['status'] for r in rows)),
           'valid_replays':sum(valid(r) for r in rows),'completed_certifications':sum(complete(r) for r in rows),
           'exact_reference_enclosures':sum(r.get('exact_reference_enclosed',False) for r in rows),
           'exact_values_certified':sum(valid(r) and r.get('lower') is not None and r.get('upper') is not None and F(r['lower'])==F(r['upper']) for r in rows),
           'total_subprocess_seconds':sum(r['total_subprocess_seconds'] for r in rows),
           'largest_worker_rss_kib':max((r.get('peak_rss_kib',0) for r in rows),default=0),
           'largest_checker_rss_kib':max((r.get('checker_peak_rss_kib',0) for r in rows),default=0)}
    summary['totals']={key:sum(s[key] for s in summary.values()) for key in
        ('runs','valid_replays','completed_certifications','exact_reference_enclosures','exact_values_certified')}
    (HERE/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    lines=['# Phase-two benchmark results','',
           'Each run used a two-second cooperative solve budget, a five-second hard',
           'worker deadline, a separate five-second proof replay deadline, one thread,',
           'and a 512 MiB address-space cap. Full inputs, refusals, source snapshots,',
           'and resource failures are retained. The initial baseline pilot is excluded.',
           '','| Lane | Runs | Completed certificates | Valid replays, including partial bounds | Exact reference enclosures |',
           '| --- | ---: | ---: | ---: | ---: |']
    for lane in lanes:
        if lane not in summary:continue
        s=summary[lane]
        lines.append(f"| {lane} | {s['runs']} | {s['completed_certifications']} | {s['valid_replays']} | {s['exact_reference_enclosures']} |")
    lines+=['','A valid replay at a resource limit certifies the reported bounds; it does',
            'not mean that the requested gap or exact result was reached. Input screening',
            'of the three continuous public QPLIB cases is separate from these run counts.',
            '','| Case | Lane | Method | Status | Gap | Solve + replay wall seconds | Peak solver/checker RSS, KiB |',
            '| --- | --- | --- | --- | --- | ---: | ---: |']
    for r in allrows:
        gap=r.get('gap')
        if gap is None and r.get('lower') is not None and r.get('upper') is not None:
            gap=F(r['upper'])-F(r['lower'])
        if gap is not None:
            exact=F(gap);gap='0' if not exact else f'{float(exact):.3g}'
        else:gap='—'
        lines.append(f"| {r['case']} | {r['lane']} | {r['method']} | {r['status']} | {gap} | {r['total_subprocess_seconds']:.3f} | {r.get('peak_rss_kib','—')}/{r.get('checker_peak_rss_kib','—')} |")
    (HERE/'RESULTS.md').write_text('\n'.join(lines)+'\n')
    extension_path=HERE/'extensions'/'summary.json'
    if extension_path.exists():
        extension=json.loads(extension_path.read_text());rows=extension['results']
        succeeded=sum(r['status'] in ('exact','certified') and isinstance(r.get('certificate_check'),dict)
                      and r['certificate_check'].get('valid') is True for r in rows)
        extra={'runs':extension['configurations'],'valid_replays':extension['valid_certificate_replays'],
               'completed_certifications':succeeded,
               'numeric_reference_enclosures':sum(r.get('certificate_check',{}).get('independent_reference_enclosed',False) for r in rows),
               'implicit_optimizer_containments':sum(r.get('certificate_check',{}).get('independent_analytic_optimizer_contained',False) for r in rows)}
        combined={key:summary['totals'][key]+extra[key] for key in ('runs','valid_replays','completed_certifications')}
        combined['checked_incomplete_bounds']=combined['valid_replays']-combined['completed_certifications']
        combined['outcomes_without_proof']=combined['runs']-combined['valid_replays']
        combined['numeric_reference_enclosures']=summary['totals']['exact_reference_enclosures']+extra['numeric_reference_enclosures']
        combined['implicit_optimizer_containments']=extra['implicit_optimizer_containments']
        combined['archived_exploratory_runs_excluded']=True
        (HERE/'combined-summary.json').write_text(json.dumps({'main':summary['totals'],'extensions':extra,'combined':combined},indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
