from pathlib import Path as _CleanupPath
_NOTES_ROOT = _CleanupPath(__file__).resolve().parent.joinpath('../../..').resolve()

import sys, collections
sys.path.insert(0,(str(_NOTES_ROOT) + '/research-20260922/scouting/minlplib-open-data'))
from osil import read
I=read((str(_CleanupPath.home()) + '/.cache/minlplib/minlplib/osil/autocorr_bern30-15.osil'))
t=I['rows'][0]['nl']; print(t[0], len(t)-1)
mons=collections.Counter(); 
for term in t[1:]:
    c=1; vs=[]
    def walk(u):
        global c
        if u[0]=='var': vs.append(u[1])
        elif u[0]=='num': c*=u[1]
        elif u[0]=='times':
            for w in u[1:]: walk(w)
        else: print('??',u[0])
    walk(term); mons[tuple(sorted(vs))]+=c
bydeg=collections.defaultdict(list)
for m,c in mons.items(): bydeg[len(m)].append((m,c))
for d in sorted(bydeg): print(d,len(bydeg[d]),collections.Counter(c for m,c in bydeg[d]).most_common(6), sorted(bydeg[d])[:6])
print(I['rows'][0]['lin'], I['rows'][0]['quad'][:5], len(I['rows'][0]['quad']))
