"""Verifier check: citation keys of the files that main.tex actually inputs (recursively), versus references.bib."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import re,os
root=(_PUBLIC_REPO + '/paper-decomposition-aware')
def strip(t): return re.sub(r'(?<!\\)%.*','',t)
def walk(f,seen):
    p=os.path.join(root,f if f.endswith('.tex') else f+'.tex')
    seen.append(p)
    t=strip(open(p,encoding='utf8').read())
    for m in re.finditer(r'\\input\{([^}]*)\}',t):
        if m.group(1)!='macros': walk(m.group(1),seen)
seen=[]; walk('main',seen)
cites={}
for p in seen:
    t=strip(open(p,encoding='utf8').read())
    for m in re.finditer(r'\\cite\w*\*?(?:\[[^\]]*\])*\{([^}]*)\}',t):
        for k in m.group(1).split(','):
            k=k.strip()
            if k: cites.setdefault(k,set()).add(os.path.basename(p))
bib=re.findall(r'@\w+\{([^,\s]+),',open(root+'/references.bib',encoding='utf8').read())
print('files',len(seen)); print('cited',len(cites))
print('missing',[k for k in cites if k not in bib])
print('uncited',[k for k in bib if k not in cites])
