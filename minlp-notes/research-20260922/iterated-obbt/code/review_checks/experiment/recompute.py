import json, math, hashlib, os, numpy as np, pandas as pd
RES='/home/sgusev/repo/minlp-notes/research-20260922/iterated-obbt/results'
inst=pd.read_csv(RES+'/instances.csv'); inst=inst[inst.in_scope].set_index('name')
FS=inst.fstar_min.to_dict()
F={}
for l in open(RES+'/final.jsonl'):
    r=json.loads(l); F[r['key']]=r
roots={}
for l in open(RES+'/roots.jsonl'):
    r=json.loads(l); roots[(r['name'],r['solver'])]=r
ob={}
for l in open(RES+'/obbt.jsonl'):
    r=json.loads(l)
    if r['status']=='ok': ob[(r['name'],r['src'])]=r
RULES=['r1','r5','ad0.5','ad0.8','fp']
H={}
def bh(tag):
    if tag not in H:
        f=np.load(RES+'/boxes/'+tag+'.npz'); H[tag]=hashlib.md5(f['lb'].tobytes()+f['ub'].tobytes()).hexdigest()
    return H[tag]
def okobj(p,f): return p is not None and abs(p-f)<=1e-3*max(1,abs(f))
def outcome(n,s,arm,seed,strict):
    f=FS[n]
    if arm in('base','obbt3'):
        r=F.get(f'{n}/{s}/{arm}/{seed}')
        if r is None: return None
        solved = r['status']=='optimal' and r['time']<=600 and (okobj(r['primal'],f) or not strict)
        t = r['time'] if solved else 600.0
        return dict(t=min(t,600), solved=solved, nodes=r.get('nodes',0), raw=r['time'])
    kind,rule=arm.split('-',1)
    if kind=='known':
        r=F.get(f'{n}/{s}/known-fp/{seed}')
        if r is None: return None
        tot=ob[(n,'known')]['trajs']['full']['snaps']['fp']['time']+r['time']
        solved=r['status']=='optimal' and tot<=600 and (okobj(r['primal'],f) or not strict)
        return dict(t=min(tot,600) if solved else 600, solved=solved, nodes=r.get('nodes',0), raw=tot)
    rt=roots[(n,s)]
    if rt['status']=='optimal':
        solved = okobj(rt['primal'],f) or not strict
        return dict(t=rt['time'] if solved else 600, solved=solved, nodes=rt['nodes'], raw=rt['time'])
    if rule=='none':
        r=F.get(f'{n}/{s}/pipe-none/{seed}'); tob=0.0
    else:
        o=ob[(n,s)]
        tob=o['trajs']['restr' if rule.startswith('ad') else 'full']['snaps'][rule]['time']
        h=bh(f'{n}__{s}__{rule}'); r=None
        for rr in RULES:
            if bh(f'{n}__{s}__{rr}')==h:
                r=F.get(f'{n}/{s}/pipe-{rr}/{seed}'); break
    if r is None: return None
    tot=rt['time']+tob+r.get('time',0) if r['status']!='error' else 600
    p=r.get('primal')
    if rt.get('primal') is not None: p=rt['primal'] if p is None else min(p,rt['primal'])
    solved = r['status']=='optimal' and tot<=600 and (okobj(p,f) or not strict)
    return dict(t=min(tot,600) if solved else 600, solved=solved, nodes=r.get('nodes',0), raw=tot)
def sgm(x,sh): x=np.asarray(x,float); return float(np.exp(np.mean(np.log(x+sh)))-sh)
ARMS={'grb':['base','obbt3','pipe-none']+['pipe-'+r for r in RULES]+['known-fp'],
      'scip':['base','pipe-none']+['pipe-'+r for r in RULES]+['known-fp']}
for strict in (False,True):
  print('==== strict objective check:',strict)
  for s,arms in ARMS.items():
    O={}
    for arm in arms:
        for n in inst.index:
            for seed in (0,1):
                o=outcome(n,s,arm,seed,strict)
                if o: O[(arm,n,seed)]=o
    for ref in ('base','pipe-none'):
      for arm in arms:
        keys=[(n,sd) for (a,n,sd) in O if a==arm and (ref,n,sd) in O]
        if ref=='pipe-none':
            keys=[k for k in keys if (k[0],s) in ob]
        if not keys: continue
        A=[O[(arm,)+k] for k in keys]; B=[O[(ref,)+k] for k in keys]
        both=[i for i in range(len(keys)) if A[i]['solved'] and B[i]['solved']]
        ta=sgm([a['t'] for a in A],1); tb=sgm([b['t'] for b in B],1)
        # alternative: raw time (unsolved not forced to 600)
        tar=sgm([min(a['raw'],600) for a in A],1); tbr=sgm([min(b['raw'],600) for b in B],1)
        nr=sgm([A[i]['nodes'] for i in both],10)/sgm([B[i]['nodes'] for i in both],10)
        print(f'{s:4s} ref={ref:9s} {arm:10s} pairs={len(keys):4d} solved={sum(a["solved"] for a in A):4d}/{sum(b["solved"] for b in B):4d} sgm={ta:6.2f}/{tb:6.2f} ratio={ta/tb:.3f} rawratio={tar/tbr:.3f} nodes={nr:.3f} both={len(both)}')

# ---- split table (pipe rule vs control, by gc of rule box), non-strict
import collections
def gcval(n,s,rule):
    o=ob[(n,s)]; f=FS[n]; T=o['trajs']; tag='restr' if rule.startswith('ad') else 'full'
    snap=T[tag]['snaps'][rule]; h=T[tag]['hist'][snap['round']-1]; LB0=T['full']['LB0']
    g=f-LB0
    if not(math.isfinite(LB0) and g>1e-6*max(1,abs(f))): return None
    if h['LB']==math.inf: return 1.0
    return min(max((h['LB']-LB0)/g,0),1)
print('==== split table')
def fsolve(n,s,arm,seed):
    # final-solve time only
    rt=roots[(n,s)]
    kind,rule=arm.split('-',1)
    if rule=='none': r=F.get(f'{n}/{s}/pipe-none/{seed}')
    else:
        h=bh(f'{n}__{s}__{rule}')
        for rr in RULES:
            if bh(f'{n}__{s}__{rr}')==h: r=F.get(f'{n}/{s}/pipe-{rr}/{seed}'); break
    return r
for s in ('grb','scip'):
    for rule in ('fp','ad0.8'):
        G=collections.defaultdict(list)
        for n in inst.index:
            if (n,s) not in ob: continue
            g=gcval(n,s,rule)
            for seed in (0,1):
                a=outcome(n,s,'pipe-'+rule,seed,False); b=outcome(n,s,'pipe-none',seed,False)
                if not(a and b and a['solved'] and b['solved']): continue
                ra=fsolve(n,s,'pipe-'+rule,seed); rb=fsolve(n,s,'pipe-none',seed)
                key='nan' if g is None else ('>=.5' if g>=0.5 else ('0<gc<.5' if g>0 else '0'))
                G[key].append((ra['nodes'],rb['nodes'],ra['time'],rb['time'],b['t']))
        for k,v in sorted(G.items()):
            v=np.array(v,float)
            print(s,rule,k,len(v),'nodes %.2f solve %.2f meanctl %.1f'%(sgm(v[:,0],10)/sgm(v[:,1],10), sgm(v[:,2],1)/sgm(v[:,3],1), v[:,4].mean()))
print('==== hard vs control')
for s in ('grb','scip'):
    hard=set()
    for n in inst.index:
        for sd in (0,1):
            o=outcome(n,s,'base',sd,False)
            if o and (o['t']>=10 or not o['solved']): hard.add(n)
    ch=set()
    for n in hard:
        if (n,s) not in ob: continue
        f=np.load(RES+'/fbbt/%s.npz'%n); b=np.load(RES+'/boxes/%s__%s__fp.npz'%(n,s))
        if (b['lb']>f['lb']).any() or (b['ub']<f['ub']).any(): ch.add(n)
    for label,S in (('hard&obbt_ran',{n for n in hard if (n,s) in ob}),('hard&changed',ch)):
        for rule in RULES:
            A=[];B=[]
            for n in S:
                for sd in (0,1):
                    a=outcome(n,s,'pipe-'+rule,sd,False); b=outcome(n,s,'pipe-none',sd,False)
                    if a and b: A.append(a); B.append(b)
            both=[i for i in range(len(A)) if A[i]['solved'] and B[i]['solved']]
            print(s,label,len(S),rule,'nodes %.3f time %.3f solved %d/%d'%(sgm([A[i]['nodes'] for i in both],10)/sgm([B[i]['nodes'] for i in both],10), sgm([a['t'] for a in A],1)/sgm([b['t'] for b in B],1), sum(a['solved'] for a in A), sum(b['solved'] for b in B)))
print('==== robustness: shift 10, bootstrap CI (by instance), oracle skip of useless OBBT')
rng=np.random.default_rng(0)
for s in ('grb','scip'):
    names=[n for n in inst.index if (n,s) in ob]
    ctl={(n,sd):outcome(n,s,'pipe-none',sd,False) for n in names for sd in (0,1)}
    for rule in ('r1','ad0.8','fp'):
        tob={n:ob[(n,s)]['trajs']['restr' if rule.startswith('ad') else 'full']['snaps'][rule]['time'] for n in names}
        a=np.array([[outcome(n,s,'pipe-'+rule,sd,False)['t'] for sd in (0,1)] for n in names])
        b=np.array([[ctl[(n,sd)]['t'] for sd in (0,1)] for n in names])
        # oracle: if rule box == FBBT box, pipeline would skip OBBT final -> use control time + 0 obbt (charged nothing)
        same=np.array([np.array_equal(np.load(RES+'/boxes/%s__%s__%s.npz'%(n,s,rule))['lb'],np.load(RES+'/fbbt/%s.npz'%n)['lb']) and np.array_equal(np.load(RES+'/boxes/%s__%s__%s.npz'%(n,s,rule))['ub'],np.load(RES+'/fbbt/%s.npz'%n)['ub']) for n in names])
        ao=a.copy(); ao[same]=b[same]
        # free OBBT: subtract obbt time when solved
        af=np.array([[max(outcome(n,s,'pipe-'+rule,sd,False)['t']-(tob[n] if outcome(n,s,'pipe-'+rule,sd,False)['solved'] else 0),0) for sd in (0,1)] for n in names])
        def ratio(x,y,sh): return (np.exp(np.mean(np.log(x+sh)))-sh)/(np.exp(np.mean(np.log(y+sh)))-sh)
        bs=[]
        for _ in range(2000):
            idx=rng.integers(0,len(names),len(names)); bs.append(ratio(a[idx],b[idx],1))
        print(s,rule,'n=%d ratio(sh1) %.3f CI95 [%.3f, %.3f]  sh10 %.3f  oracle-skip %.3f  free-OBBT %.3f  (useless boxes %d)'%(len(names),ratio(a,b,1),*np.percentile(bs,[2.5,97.5]),ratio(a,b,10),ratio(ao,b,1),ratio(af,b,1),same.sum()))
