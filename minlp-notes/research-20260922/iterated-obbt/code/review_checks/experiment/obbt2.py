from pathlib import Path as _CleanupPath
_NOTES_ROOT = _CleanupPath(__file__).resolve().parent.joinpath('../../../../..').resolve()

import json, numpy as np, collections
RES=(str(_NOTES_ROOT) + '/research-20260922/iterated-obbt/results')
ob=[json.loads(l) for l in open(RES+'/obbt.jsonl')]
kn=[r for r in ob if r['src']=='known']
L=collections.Counter(len(r['trajs']['full']['hist']) for r in kn); print(sorted(L.items()))
# r1 box vs fbbt
ch=0
for r in kn:
    f=np.load(RES+'/fbbt/%s.npz'%r['name']); b=np.load(RES+'/boxes/%s__known__r1.npz'%r['name'])
    if (b['lb']>f['lb']).any() or (b['ub']<f['ub']).any(): ch+=1
print('r1 box differs from fbbt',ch)
print('nchanged>0 r1', sum(r['trajs']['full']['hist'][0]['nchanged']>0 for r in kn), 'nmoved>0 r1', sum(r['trajs']['full']['hist'][0]['nmoved']>0 for r in kn))
print('len==2', sum(len(r['trajs']['full']['hist'])==2 for r in kn))
for src in ('known','grb','scip'):
    R=[r for r in ob if r['src']==src]
    ks=[r['trajs']['restr']['snaps']['ad0.8']['round'] for r in R]
    print(src,'ad0.8 k>=5',sum(k>=5 for k in ks),'k>5',sum(k>5 for k in ks))
