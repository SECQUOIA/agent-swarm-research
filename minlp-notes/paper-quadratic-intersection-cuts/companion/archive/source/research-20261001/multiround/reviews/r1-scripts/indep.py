from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[8])

import glob, json, collections, math
import numpy as np
from scipy import stats
base=(_PUBLIC_REPO + '/research-20261001/multiround/logs/')
R=collections.defaultdict(dict); viol=[]; nrec=0; statuses=collections.Counter()
for size in ('4x4','6x8','8x12','10x20'):
    for f in glob.glob(base+'main/main_%s_*.jsonl'%size)+glob.glob(base+'new/new_%s_*.jsonl'%size):
        for line in open(f):
            r=json.loads(line); nrec+=1; statuses[r['status']]+=1
            key=(size,r['inst'])
            if key in R[r['rule']]:
                if R[r['rule']][key]['closed']!=r['closed']: print('DUP DIFF',r['rule'],key)
            R[r['rule']][key]=r
            gap=r['zbil']-r['zlp']
            for ri in r['rounds']:
                e=(ri['z']-r['zbil'])/gap
                if e>1e-6: viol.append((r['rule'],key,ri['r'],e))
print('records',nrec,statuses)
print('LP above zbil (rel >1e-6):',len(viol), sorted(viol,key=lambda t:-t[3])[:10])
S=R['scip']; print('scip n',len(S), collections.Counter(k[0] for k in S))
def ci(d):
    d=np.array(d); h=stats.t.ppf(.975,len(d)-1)*d.std(ddof=1)/math.sqrt(len(d)); return d.mean(),d.mean()-h,d.mean()+h,stats.ttest_1samp(d,0).pvalue,len(d)
for rule in sorted(R):
    if rule=='scip': continue
    ids=sorted(set(R[rule])&set(S))
    out=[]
    for s in (1,3,10,20):
        out.append('r%d %+.4f[%+.4f,%+.4f]'%(s,*ci([R[rule][i]['closed'][s]-S[i]['closed'][s] for i in ids])[:3]))
    m,l,h,p,n=ci([np.mean(R[rule][i]['closed'][1:11])-np.mean(S[i]['closed'][1:11]) for i in ids])
    print('%-11s n=%3d %s AUC %+.4f p=%.3g'%(rule,n,' '.join(out),m,p))
# per size for orbit
for size in ('4x4','6x8','8x12','10x20'):
    ids=[i for i in S if i[0]==size]
    for rule in ('orbit','eff','eff2','o2s','s5o','s1o','o1s','first_orbit'):
        ii=[i for i in ids if i in R[rule]]
        if not ii: continue
        r10=ci([R[rule][i]['closed'][10]-S[i]['closed'][10] for i in ii])
        print(size,rule,len(ii),'r10 %+.4f[%+.4f,%+.4f] p %.3g'%r10[:4], 'W/L', sum(R[rule][i]['closed'][10]-S[i]['closed'][10]>0.01 for i in ii), sum(R[rule][i]['closed'][10]-S[i]['closed'][10]<-0.01 for i in ii))
    print(size,'scip means r1/3/10/20', [round(np.mean([S[i]['closed'][s] for i in ids]),3) for s in (1,3,10,20)], 'closed>0.999 at r20', sum(S[i]['closed'][20]>0.999 for i in ids))
