import sys
from fractions import Fraction as F
import importlib.util
spec=importlib.util.spec_from_file_location('nstruct',__import__('os').path.join(__import__('os').path.dirname(__file__),'nstruct.py')); ns=importlib.util.module_from_spec(spec); spec.loader.exec_module(ns)
def check(name):
    V,C,O,rep,S=ns.analyze(name)
    N,T,kvar,Vw=S['N'],S['T'],S['kvar'],S['Vw']
    kT={kvar[(i,T-1)]:i for i in range(N)}
    rows={}
    for r,c in enumerate(C):
        for i in range(N):
            if c['lin'].get(kvar[(i,0)])==1: rows.setdefault(i,[]).append(r)
    # the burnup row of k_{i,1} has coefficient -1, so only the reload row should have +1
    assert all(len(rows[i])==1 for i in range(N)), rows
    out={}
    isB=lambda j: V[j]['type']=='B' and V[j]['lb']==0 and V[j]['ub']==1
    alias={}
    for cc in C:
        if cc['lb']==cc['ub']==0 and not cc['quad'] and len(cc['lin'])==2 and sorted(cc['lin'].values())==[-1,1]:
            a,b=list(cc['lin'])
            if isB(a) and not isB(b): alias[b]=a
            elif isB(b) and not isB(a): alias[a]=b
    canon=lambda j: alias.get(j,j)
    binv=lambda j: isB(canon(j))
    KFs=set()
    fam=None
    for i in range(N):
        c=C[rows[i][0]]; assert c['lb']==c['ub']==0
        lin={j:v for j,v in c['lin'].items() if j!=kvar[(i,0)]}
        for j,v in lin.items():
            if v!=-1: KFs.add(-v); assert binv(j)
        qs=c['quad']
        kinds=set()
        for (a,b),v in qs.items():
            assert v==-1
            if a in kT or b in kT: kinds.add('F2')
            else: kinds.add('F1')
        if not qs: kinds.add('F3')
        assert len(kinds)==1; f=kinds.pop(); fam=fam or f; assert fam==f
    assert len(KFs)==1; KF=KFs.pop()
    info=dict(fam=fam,KF=KF)
    if fam=='F2':
        # each node row: b0 + sum_j b_ij = 1 equality over exactly the binaries in its k-row
        for i in range(N):
            c=C[rows[i][0]]
            bs=set(c['lin'])-{kvar[(i,0)]}|{(a if b in kT else b) for (a,b) in c['quad']}
            for (a,b) in c['quad']: assert binv(a if b in kT else b)
            ok=[r for r,cc in enumerate(C) if cc['lb']==cc['ub']==1 and not cc['quad'] and set(cc['lin'])==bs and all(v==1 for v in cc['lin'].values())]
            assert ok, ('no assignment row',i)
        info['phi_lb_pos']=all(V[p]['lb']!='-INF' and V[p]['lb']>0 for p in S['phi'].values())
        info['k_lb']=min(V[k]['lb'] for k in kvar.values())
        info['phi_lb']=min(V[p]['lb'] for p in S['phi'].values())
    if fam=='F3':
        for i in range(N):
            c=C[rows[i][0]]
            b0=[j for j,v in c['lin'].items() if j!=kvar[(i,0)] and v==-KF]
            zs=[j for j,v in c['lin'].items() if v==-1]
            assert len(b0)==1 and len(zs)+1+1==len(c['lin'])
            bs=set(b0)
            for z in zs:
                assert V[z]['lb']!='-INF' 
                # find z <= KF b and z <= k_T rows
                r1=[cc for cc in C if cc['ub']==0 and cc['lb']=='-INF' and not cc['quad'] and cc['lin'].get(z)==1 and len(cc['lin'])==2]
                ks=[j for cc in r1 for j,v in cc['lin'].items() if j!=z and v==-1 and j in kT]
                bb=[j for cc in r1 for j,v in cc['lin'].items() if j!=z and v==-KF and binv(j)]
                assert len(ks)==1 and len(bb)==1, (i,z,r1)
                bs.add(bb[0])
            ok=[r for r,cc in enumerate(C) if cc['lb']==cc['ub']==1 and not cc['quad'] and set(cc['lin'])==bs and all(v==1 for v in cc['lin'].values())]
            assert ok, ('no assignment row',i)
    if fam=='F1':
        ymap={}; kappas={}
        for i in range(N):
            c=C[rows[i][0]]
            for j in c['lin']:
                if j!=kvar[(i,0)]: ymap[canon(j)]=(i,'fresh')
            for (a,b) in c['quad']:
                ya,ka=(a,b) if binv(a) else (b,a); assert binv(ya) and not binv(ka)
                ymap[canon(ya)]=(i,ka); kappas.setdefault(ka,set()).add(i)
        # node rows
        for i in range(N):
            ys={y for y,(ii,_) in ymap.items() if ii==i}
            assert any(cc['lb']==cc['ub']==1 and not cc['quad'] and set(cc['lin'])==ys and all(v==1 for v in cc['lin'].values()) for cc in C), ('node row',i)
        # type rows: equality 1, linear, one y per node, weights W
        types=[]
        for cc in C:
            if cc['lb']==cc['ub']==1 and not cc['quad'] and all(j in ymap for j in cc['lin']):
                nodes=[ymap[j][0] for j in cc['lin']]
                if len(set(nodes))==len(nodes)==N and len({ymap[j][1] for j in cc['lin']})==1:
                    types.append(cc)
        # every y in exactly one type row
        ty={}
        for g,cc in enumerate(types):
            for j,w in cc['lin'].items(): assert j not in ty; ty[j]=g; assert w==Vw[ymap[j][0]], 'type weight != V'
        assert set(ty)==set(ymap)
        # type content consistent: all y in type g are fresh or have same kappa
        tkind={}
        for j,g in ty.items(): tkind.setdefault(g,set()).add(ymap[j][1])
        assert all(len(s)==1 for s in tkind.values()); tkind={g:s.pop() for g,s in tkind.items()}
        # kappa rows
        pred={}
        for ka in kappas:
            rr=[cc for cc in C if cc['lin'].get(ka)==1 and cc['lb']==cc['ub']==0]
            assert len(rr)==1; cc=rr[0]; assert len(cc['lin'])==1
            gs=set()
            for (a,b),v in cc['quad'].items():
                y,k=(a,b) if canon(a) in ymap else (b,a); y=canon(y)
                assert k in kT and ymap[y][0]==kT[k], 'kappa pairs k_T of same node'
                assert -v==Vw[kT[k]], 'kappa weight != V'
                gs.add(ty[y])
            assert len(gs)==1 and len(cc['quad'])==N
            g_self=[g for g,kd in tkind.items() if kd==ka]; assert len(g_self)==1
            pred[g_self[0]]=gs.pop()
        # acyclic, age
        def age(g,seen=()):
            assert g not in seen, 'cycle'
            return 0 if tkind[g]=='fresh' else 1+age(pred[g],seen+(g,))
        ages=[age(g) for g in tkind]
        info.update(ntypes=len(types),nfresh=sum(1 for v in tkind.values() if v=='fresh'),max_age=max(ages),
                    kappa_free=sorted(set(str(V[k]['lb']) for k in kappas)))
        neg=[j for j,v in enumerate(V) if v['lb']=='-INF' or v['lb']<0]
        info['neg_lb_all_kappa']=set(neg)<=set(kappas)
    # other negative lbs
    info['aliases']=len(alias); info['neg_lb']=sum(1 for v in V if v['lb']=='-INF' or v['lb']<0)
    info['binaries_ok']=all(v['type'] in ('B','C') for v in V) and all(binv(j) for j,v in enumerate(V) if v['type']=='B')
    return rep,info,S
if __name__=='__main__':
    for nm in sys.argv[1:]:
        rep,info,S=check(nm); print(nm, rep['N'],rep['T'],[str(a) for a in rep['alpha']],[str(p) for p in rep['peak']],[str(v) for v in rep['V']], 'philb',[str(x) for x in rep['phi_lb']][:2],'klb',[str(x) for x in rep['k_lb']]); print('   ',info)
