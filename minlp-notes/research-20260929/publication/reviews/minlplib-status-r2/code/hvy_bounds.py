"""Review r2: compare variable bound multisets of PrincetonLib hvycrash (2006) and current hvycrash."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import re, collections
P=(_PUBLIC_REPO + '/research-20260929/publication/minlplib-status/pages/sources/gamsworld/PrincetonLib/Cute/Scalar_models/hvycrash.gms')
C=(_PUBLIC_REPO + '/research-20260929/publication/reviews/minlplib-status-r1/dl/gms/hvycrash.gms')
def bounds(path):
    s=open(path).read()
    names=re.search(r'Variables\s+(.*?);', s, re.S).group(1).replace('\n','').replace(' ','').split(',')
    pos=set()
    m=re.search(r'Positive Variables\s+(.*?);', s, re.S)
    if m: pos=set(m.group(1).replace('\n','').replace(' ','').split(','))
    b={n:['0' if n in pos else '-inf','inf'] for n in names}
    for v,a,val in re.findall(r'(\w+)\.(lo|up|fx)\s*=\s*([^;]+);', s):
        if a=='lo': b[v][0]=val.strip()
        elif a=='up': b[v][1]=val.strip()
        else: b[v]=[val.strip(),val.strip()]
    return b
bp,bc=bounds(P),bounds(C)
print('vars', len(bp), len(bc))
cp=collections.Counter(tuple(v) for v in bp.values()); cc=collections.Counter(tuple(v) for v in bc.values())
print('PrincetonLib minus current:', dict(cp-cc)); print('current minus PrincetonLib:', dict(cc-cp))
