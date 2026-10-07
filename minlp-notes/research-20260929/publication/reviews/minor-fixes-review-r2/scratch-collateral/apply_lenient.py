# Read-only lenient unified-diff applier: applies hunks to copies of before/ files, writes results under scratch only.
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import sys,re,os
P=(_PUBLIC_REPO + '/research-20260929/publication')
M=P+'/reviews/minor-fixes'
S=P+'/reviews/minor-fixes-review-r2/scratch-collateral'
lines=open(M+'/report_changes.patch',encoding='utf-8').read().split('\n')
files={}; cur=None; i=0
while i<len(lines):
    l=lines[i]
    if l.startswith('--- before/') and i+1<len(lines) and lines[i+1].startswith('+++ after/'):
        cur=l[len('--- before/'):]; files[cur]=[]; i+=2; continue
    m=re.match(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@',l)
    if m: files[cur].append([int(m.group(1)),[]]); i+=1; continue
    if cur and files[cur]:
        files[cur][-1][1].append(l)
    i+=1
for f,hunks in files.items():
    src=open(M+'/before/'+f.replace('/report.md','').replace('/','__')+'.txt',encoding='utf-8').read()
    nonl=not src.endswith('\n')
    a=src.split('\n')
    if not nonl: a=a[:-1]
    out=[]; pos=0; ok=True
    for start,body in hunks:
        # strip trailing empty strings (artifact of split)
        while body and body[-1]=='' : body=body[:-1]
        body=[b for b in body if not b.startswith('\\ No newline')]
        old=[b[1:] for b in body if b[:1] in ' -']
        new=[b[1:] for b in body if b[:1] in ' +']
        s=start-1 if old else start
        if a[s:s+len(old)]!=old:
            ok=False; print('HUNK MISMATCH',f,start); 
        out+=a[pos:s]; out+=new; pos=s+len(old)
    out+=a[pos:]
    txt='\n'.join(out)+('' if nonl else '\n')
    d=S+'/r1lenient/'+f; os.makedirs(os.path.dirname(d),exist_ok=True); open(d,'w',encoding='utf-8').write(txt)
    b=M+'/before-r2/'+f.replace('/','__')
    same=open(b,encoding='utf-8').read()==txt
    print(('OK ' if ok else 'BAD ')+('R1-RESULT==BEFORE-R2 ' if same else 'MISMATCH ')+f)
