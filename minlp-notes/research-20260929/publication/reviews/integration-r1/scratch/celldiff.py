# For table rows of the summary, compare cells of (HEAD + 33 replacements) to the current document.
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

R=(_PUBLIC_REPO + '/research-20260929/')
a=open('applied_open-instances-summary.md').read().splitlines()
b=open(R+'open-instances-summary.md').read().splitlines()
def rows(L):
    d={}
    for l in L:
        if l.startswith('| ') and not l.startswith('|---'):
            c=[x.strip() for x in l.strip('|').split(' | ')]
            d.setdefault(c[0],c)
    return d
A,B=rows(a),rows(b)
for k in A:
    if k not in B: print('MISSING ROW',k); continue
    for j,(x,y) in enumerate(zip(A[k],B[k])):
        if x!=y: print(f'{k} col{j+1}:\n   applied: {x}\n   current: {y}')
