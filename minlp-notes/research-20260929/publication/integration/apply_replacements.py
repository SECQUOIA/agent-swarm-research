"""Validate the entire ordered list on disposable copies; edit only owned files."""
import hashlib,json
from pathlib import Path
BASE=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
OWN={'open-instances-summary.md','bound-audit/audit-report.md'}
edits=json.loads((BASE/'publication/reviews/minor-fixes/integration-r2.json').read_text())
assert len(edits)==40
contents={}
records=[]
for i,e in enumerate(edits,1):
    p=BASE/e['target']
    if e['target'] not in contents:
        contents[e['target']]=p.read_text()
        (OUT/'before').mkdir(exist_ok=True)
        (OUT/'before'/e['target'].replace('/','__')).write_text(contents[e['target']])
    old=contents[e['target']]
    count=old.count(e['old'])
    assert count>0,(i,e['target'],count)
    contents[e['target']]=old.replace(e['old'],e['new'])
    records.append({'index':i,'target':e['target'],'matches':count,'applied_to_original':e['target'] in OWN,'reason':e.get('reason')})
    print(i,e['target'],count,'APPLIED' if e['target'] in OWN else 'SCRATCH ONLY (protected)')
(OUT/'ordered-validation').mkdir(exist_ok=True)
for target,content in contents.items():
    (OUT/'ordered-validation'/target.replace('/','__')).write_text(content)
    if target in OWN:(BASE/target).write_text(content)
(OUT/'replacements.json').write_text(json.dumps(records,indent=2)+'\n')
assert sum(r['applied_to_original'] for r in records)==33
(OUT/'PROGRESS.json').write_text(json.dumps({'status':'in_progress','date':'2026-10-03','phase':'33 owned edits applied; all 40 validated in order','protected_edits':7,'numerical_checks':'pending','background_jobs':[]},indent=2)+'\n')
