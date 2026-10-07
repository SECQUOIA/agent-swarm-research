from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import glob, json, collections
base=(_PUBLIC_REPO + '/research-20261001/multiround/')
zp={}
for size in ('4x4','6x8','8x12','10x20'):
    D=json.load(open(base+'data/inst_%s.json'%size))
    for k,r in enumerate(D['instances']): zp[(size,k)]=(r['zbil'],r['zbil_primal'],r['zlp'])
cnt=collections.Counter(); worst=[]
for size in ('4x4','6x8','8x12','10x20'):
    for f in glob.glob(base+'logs/main/main_%s_*.jsonl'%size)+glob.glob(base+'logs/new/new_%s_*.jsonl'%size):
        for line in open(f):
            r=json.loads(line); zd,zpr,zlp=zp[(size,r['inst'])]
            assert abs(zd-r['zbil'])<1e-12
            for ri in r['rounds']:
                ex=(ri['z']-zpr)/max(1,abs(zpr))
                if ri['z']>zd+1e-9: cnt['above_dual']+=1
                if ex>1e-9: cnt['above_primal_1e-9']+=1; worst.append((ex,r['rule'],size,r['inst'],ri['r'], (ri['z']-zd)/(zd-zlp)))
                if ex>1e-6: cnt['above_primal_1e-6']+=1
print(cnt); worst.sort(reverse=True); print(worst[:15])
gaps=[(v[1]-v[0])/max(1,abs(v[1])) for v in zp.values()]; print('max rel scip gap', max(gaps))
