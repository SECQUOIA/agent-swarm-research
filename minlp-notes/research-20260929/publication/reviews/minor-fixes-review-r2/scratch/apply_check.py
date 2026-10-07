# Apply the 40 integration edits in memory, sequentially; check each old string occurs
# (count) in the current text; check summary.md blocks equal the JSON.
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import json, re, os, collections
R=(_PUBLIC_REPO + '/research-20260929')
d=json.load(open(R+'/publication/reviews/minor-fixes/integration-r2.json'))
def path(t):
    for c in [R+'/'+t, R+'/publication/'+t, R+'/'+t.replace('publication/','publication/')]:
        if os.path.exists(c): return c
    return None
texts={}
for i,e in enumerate(d,1):
    p=path(e['target'])
    if p not in texts: texts[p]=open(p).read()
    t=texts[p]; n=t.count(e['old'])
    print(f"{i:2d} {e['target']:55s} count={n} newcount_before={t.count(e['new'])} | {e['reason'][:70]}")
    texts[p]=t.replace(e['old'],e['new'])
# summary.md consistency
s=open(R+'/publication/reviews/minor-fixes/summary.md').read()
blocks=re.findall(r"Old:\n```text\n(.*?)\n```\nNew:\n```text\n(.*?)\n```",s,re.S)
print('summary blocks',len(blocks))
for i,(b,e) in enumerate(zip(blocks,d),1):
    if b!=(e['old'],e['new']): print('MISMATCH',i)
print('keys',collections.Counter(tuple(sorted(e)) for e in d))
