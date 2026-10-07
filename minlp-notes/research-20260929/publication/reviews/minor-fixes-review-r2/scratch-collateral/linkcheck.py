# Read-only: check relative markdown links and backticked relative paths on lines added in round 2.
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import re,os,sys
P=(_PUBLIC_REPO + '/research-20260929/publication')
patch=open(P+'/reviews/minor-fixes-review-r2/scratch-collateral/r2_now.patch',encoding='utf-8').read().split('\n')
cur=None
for l in patch:
    if l.startswith('+++ after/'): cur=l[len('+++ after/'):]; continue
    if l.startswith('+') and not l.startswith('+++') and cur and cur.endswith('.md'):
        base=os.path.dirname(P+'/'+cur)
        for m in re.finditer(r'\]\(([^)#\s]+)(#[^)]*)?\)',l):
            t=m.group(1)
            if t.startswith('http'): continue
            ok=os.path.exists(os.path.normpath(os.path.join(base,t)))
            if not ok: print('BROKEN link',cur,t)
        for m in re.finditer(r'`([^`\s]+/[^`\s]*)`',l):
            t=m.group(1)
            if t.startswith('http') or '*' in t or '{' in t or '<' in t: continue
            cands=[os.path.join(base,t),os.path.join(P,t),os.path.join((_PUBLIC_REPO + '/research-20260929'),t),os.path.join((_PUBLIC_REPO),t),os.path.join((_PUBLIC_REPO + '/research-20260929/publication/..'),t)]
            if t.startswith('publication/'): cands.append(os.path.join((_PUBLIC_REPO + '/research-20260929'),t))
            if not any(os.path.exists(os.path.normpath(c)) for c in cands): print('UNRESOLVED path',cur,t)
print('done')
