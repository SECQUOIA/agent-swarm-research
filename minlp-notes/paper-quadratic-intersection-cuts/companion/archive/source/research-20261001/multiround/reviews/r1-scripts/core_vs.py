from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[8])

import json, glob, collections, numpy as np
from scipy import stats
base=(_PUBLIC_REPO + '/research-20261001/multiround/logs/')
def ci(d):
    d=np.array(d); h=stats.t.ppf(.975,len(d)-1)*d.std(ddof=1)/np.sqrt(len(d)); return '%+.4f [%+.4f,%+.4f] n=%d'%(d.mean(),d.mean()-h,d.mean()+h,len(d))
R=collections.defaultdict(dict)
for line in open(base+'fid2_exploop_6x8.jsonl'):
    r=json.loads(line); R[r['rule']][r['inst']]=r['closed']
ids=sorted(R['orbit'])
for s in (1,3,10): print('exploop6x8 orbit-orbit_core r%d'%s, ci([R['orbit'][i][s]-R['orbit_core'][i][s] for i in ids]))
print([round(R['orbit'][i][10]-R['orbit_core'][i][10],3) for i in ids])
R=collections.defaultdict(dict)
for size in ('4x4','6x8','8x12','10x20'):
    for f in glob.glob(base+'main/main_%s_*.jsonl'%size):
        for line in open(f):
            r=json.loads(line); R[r['rule']][(size,r['inst'])]=r['closed']
ids=sorted(R['orbit'])
for s in (1,3,10,20): print('220 orbit-orbit_core r%d'%s, ci([R['orbit'][i][s]-R['orbit_core'][i][s] for i in ids]))
for size in ('4x4','6x8','8x12','10x20'):
    ii=[i for i in ids if i[0]==size]; print(size,'r10',ci([R['orbit'][i][10]-R['orbit_core'][i][10] for i in ii]))
