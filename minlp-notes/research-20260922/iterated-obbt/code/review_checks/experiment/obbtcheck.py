import json, math, numpy as np, pandas as pd
RES='/home/sgusev/repo/minlp-notes/research-20260922/iterated-obbt/results'
inst=pd.read_csv(RES+'/instances.csv'); inst=inst[inst.in_scope].set_index('name')
FS=inst.fstar_min.to_dict()
ob={}
for l in open(RES+'/obbt.jsonl'):
    r=json.loads(l)
    ob[(r['name'],r['src'])]=r
print('records',len(ob),'errors',sum(r['status']!='ok' for r in ob.values()))
def gc(LB,LB0,f):
    g=f-LB0
    if not(math.isfinite(LB0) and g>1e-6*max(1,abs(f))): return None
    if LB==math.inf: return 1.0
    return min(max((LB-LB0)/g,0),1)
def sgm(x,sh=1): x=np.asarray(x,float); return float(np.exp(np.mean(np.log(x+sh)))-sh)
for src in ('known','grb','scip'):
    recs=[r for (n,s),r in ob.items() if s==src and r['status']=='ok']
    G={k:[] for k in (1,2,3,5,10,50)}; T={1:[],50:[]}
    for r in recs:
        f=FS[r['name']]; full=r['trajs']['full']; H=full['hist']
        g0=gc(H[0]['LB'],full['LB0'],f)
        if g0 is None: continue
        for k in G:
            h=H[min(k,len(H))-1]; G[k].append(gc(h['LB'],full['LB0'],f))
        T[1].append(full['snaps']['r1']['time']); T[50].append(full['snaps']['fp']['time'])
    print(src,len(recs),'posgap',len(G[1]),' '.join('k=%d:%.3f'%(k,np.mean(v)) for k,v in G.items()),
          'sgm t1 %.2f tfp %.2f'%(sgm(T[1]),sgm(T[50])))
    # adaptive stops
    for th in ('ad0.5','ad0.8'):
        ks=[r['trajs']['restr']['snaps'][th]['round'] for r in recs]
        print('  ',th,'stop after r1:',sum(k==1 for k in ks),'/',len(ks),' >=5 rounds:',sum(k>=5 for k in ks))
# contraction on known
recs=[r for (n,s),r in ob.items() if s=='known']
med=[];t1=0;fp1=0;ge5=0
for r in recs:
    H=r['trajs']['full']['hist']
    rhos=[h['rho'] for h in H if h['nmoved']>0]
    if H[0]['nchanged']>0: t1+=1
    if len(H)==1 or (len(H)>=2 and all(h['nchanged']==0 for h in H[1:])): fp1+=1
    if len(H)>=5: ge5+=1
    if len(rhos)>=4: med.append(np.median(rhos[2:10]))
med=np.array(med)
print('known: r1 tightens',t1,'fp after 1 round',fp1,'>=5 rounds',ge5,'n>=4 moving rounds',len(med))
bins=[0,0.3,0.5,0.7,0.8,0.9,0.95,10]
print(' hist', np.histogram(med,bins=bins)[0], ' >0.95:',(med>0.95).sum(),' <=0.5:',(med<=0.5).sum())
# alternative: rho over rounds 3..10 by round index (not moving-round index)
med2=[]
for r in recs:
    H=r['trajs']['full']['hist']
    if sum(h['nmoved']>0 for h in H)>=4:
        rr=[h['rho'] for h in H[2:10] if h['nmoved']>0]
        med2.append(np.median(rr) if rr else np.nan)
med2=np.array(med2); print(' by round index: >0.95',(med2>0.95).sum(),'<=0.5',(med2<=0.5).sum(), 'nan',np.isnan(med2).sum())
# times known
t1=np.array([r['trajs']['full']['snaps']['r1']['time'] for r in recs]); tf=np.array([r['trajs']['full']['snaps']['fp']['time'] for r in recs])
print('known t1 median %.3f fp median %.3f; t1>10: %d, t1>120: %d; fp capped: %d'%(np.median(t1),np.median(tf),(t1>10).sum(),(t1>120).sum(),sum(r['trajs']['full']['hist'][-1]['capped'] for r in recs)))
# GS vs J
gs=sum(r['trajs']['full']['nlp'] for r in recs); jn=sum(r['trajs']['jacobi']['nlp'] for r in recs)
print('GS nlp',gs,'J nlp',jn,'GS time %.0f J time %.0f'%(sum(r['trajs']['full']['total'] for r in recs),sum(r['trajs']['jacobi']['total'] for r in recs)))
print('median rounds GS',np.median([len(r['trajs']['full']['hist']) for r in recs]),'J',np.median([len(r['trajs']['jacobi']['hist']) for r in recs]))
nf=sum(r['trajs']['nofilt1']['nlp'] for r in recs); f1=sum(r['trajs']['full']['hist'][0]['nlp'] for r in recs)
print('filtering round1 LPs',f1,'nofilt',nf, 'time f1 %.0f nf %.0f'%(sum(r['trajs']['full']['snaps']['r1']['time'] for r in recs), sum(r['trajs']['nofilt1']['total'] for r in recs)))
# infeasible LPs
print('infeasible LPs total', sum(h['infeasible'] for r in ob.values() if r['status']=='ok' for t in r['trajs'].values() for h in t['hist']))
print('which', sorted({(r['name'],r['src']) for r in ob.values() if r['status']=='ok' for t in r['trajs'].values() for h in t['hist'] if h['infeasible']}))
