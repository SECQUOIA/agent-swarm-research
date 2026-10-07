# Apply the 33 owned replacements of minor-fixes/integration-r2.json to HEAD copies.
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import json, difflib, sys
R=(_PUBLIC_REPO + '/research-20260929/')
items=json.load(open(R+'publication/reviews/minor-fixes/integration-r2.json'))
summ=open(R+'publication/reviews/minor-fixes/summary.md').read()
docs={'open-instances-summary.md':open('head_summary.md').read(),'bound-audit/audit-report.md':open('head_audit.md').read()}
cur={k:open(R+k).read() for k in docs}
for i,it in enumerate(items,1):
    # summary.md must contain the same old/new text (as code blocks)
    insum = (it['old'] in summ) and (it['new'] in summ)
    if it['target'] not in docs:
        print(i,it['target'],'protected; in summary.md:',insum); continue
    n=docs[it['target']].count(it['old'])
    docs[it['target']]=docs[it['target']].replace(it['old'],it['new'])
    print(i,it['target'],'old matches',n,'| new text present verbatim in current doc:',it['new'] in cur[it['target']],'| in summary.md:',insum)
for k in docs:
    open('applied_'+k.replace('/','__'),'w').write(docs[k])
