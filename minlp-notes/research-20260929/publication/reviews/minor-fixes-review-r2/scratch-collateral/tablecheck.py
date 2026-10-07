# Read-only: count markdown table rows whose cell count differs from the table header, before-r2 vs current.
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import json,os,re
P=(_PUBLIC_REPO + '/research-20260929/publication')
M=P+'/reviews/minor-fixes'
def cells(l):
    s=l.strip()
    s=re.sub(r'\\\|','',s)
    s=re.sub(r'`[^`]*`','',s)
    return s.strip('|').count('|')+1
def bad(text):
    out=[];hdr=None;infence=False
    for i,l in enumerate(text.split('\n'),1):
        if l.strip().startswith('```'): infence=not infence; continue
        if infence: hdr=None; continue
        if l.strip().startswith('|'):
            if hdr is None: hdr=cells(l)
            elif cells(l)!=hdr: out.append((i,cells(l),hdr))
        else: hdr=None
    return out
for f in json.load(open(M+'/FILES-r2.json')):
    if not f.endswith('.md'): continue
    b=M+'/before-r2/'+f.replace('/','__')
    nb=bad(open(b).read()) if os.path.exists(b) else None
    na=bad(open(P+'/'+f).read())
    if na or nb: print(f,'before',len(nb) if nb is not None else 'n/a','after',len(na),na[:8])
print('done')
