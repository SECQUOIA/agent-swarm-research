"""Independent exact matrix, section, and graph-flow tests for both Fibonacci forms."""
import itertools,json
from pathlib import Path
import sympy as s
R=s.Rational
F=[0,1,1]
for i in range(3,12):F.append(F[-1]+F[-2])
checks=0; lifted=0; excluded=0
for q in range(3,10):
    N=2*q-1
    names=[('P',i) for i in range(1,q+1)]+[('H',0)]+[('H',i) for i in range(3,q+1)]
    cols=[{('H',0),('P',1)},{('H',0),('P',2)}]
    for i in range(3,q+1):cols.extend([{('H',i),('P',i)},{('H',i),('P',i-1),('P',i-2)}])
    cols.append({('P',q),('P',q-1)})
    D=s.Matrix([[int(name in col) for col in cols] for name in names])
    alpha=s.Matrix([F[i] if ty=='P' else F[q+1]-(1 if i==0 else F[i]) for ty,i in names])
    assert sum(D)==5*q-4 and D.det()!=0
    assert D.T*alpha==F[q+1]*s.ones(N,1)
    assert sum(alpha)==(q-1)*F[q+1]+1
    for sparse in [False,True]:
        K=s.ones(N,N)-D if sparse else D
        assert K.det()!=0 and all(0<sum(K[i,:])<N for i in range(N))
        beta=(K.T*alpha)[0]; assert K.T*alpha==beta*s.ones(N,1) and beta>0
        r=names.index(('P',q)); ss=names.index(('P',1)); ratio=alpha[r]/alpha[ss]
        assert ratio==F[q]
        ar=next(j for j in range(N) if K[r,j]==0); ac=next(j for j in range(N) if K[ss,j]==0)
        aa=R(1,2*N);cc=aa/4;weight=1/R(N)
        inv=K.inv();norm=max(sum(abs(t) for t in inv[i,:]) for i in range(N))
        eps=aa/(16*(1+ratio)*(1+norm))
        aggregate=[sum(K[i,:])*aa+(N-sum(K[i,:]))*cc for i in range(N)]
        for u,v in itertools.product(range(-2,3),repeat=2):
            dr=eps*u/3;ds=eps*v/3
            delta=s.zeros(N,1);delta[r]=dr;delta[ss]=ds
            if (alpha.T*delta)[0]<0:
                assert (alpha.T*(-delta))[0]>0
                excluded+=1;continue
            tau=s.zeros(N,1);tau[ss]=ratio*dr+ds
            profile=aa*s.ones(N,1)+inv*(-delta+tau)
            assert sum(profile)==R(1,2) and all(0<=w<=weight for w in profile)
            fa=[]
            for i in range(N):
                row=[profile[j] if K[i,j] else cc for j in range(N)]
                if i==r:row[ar]+=dr
                if i==ss:row[ac]+=ds
                if i==ss:row[next(j for j in range(N) if K[i,j])]-=tau[ss]
                assert sum(row)==aggregate[i]
                assert all(0<=row[j]<=profile[j] for j in range(N))
                fa.append(row)
            # Construct simple split/subdivided network explicitly.
            source=0; sink=1; incoming={i:2+2*(i-1) for i in range(1,N)}
            outgoing={i:3+2*(i-1) for i in range(1,N)}
            subdiv={i:2*N+i for i in range(N)}
            edges=[]; state_values=[]; original_aggregates=[]
            for i in range(N):
                tail=source if i==0 else outgoing[i]
                head=sink if i==N-1 else incoming[i+1]
                edges.extend([(tail,head),(tail,subdiv[i]),(subdiv[i],head)])
                state_values.extend([fa[i],[profile[j]-fa[i][j] for j in range(N)],[profile[j]-fa[i][j] for j in range(N)]])
                original_aggregates.extend([aggregate[i],R(1,2)-aggregate[i],R(1,2)-aggregate[i]])
            for i in range(1,N):
                edges.append((incoming[i],outgoing[i]));state_values.append(list(profile));original_aggregates.append(R(1,2))
            edges.append((source,sink));state_values.append([weight-w for w in profile]);original_aggregates.append(R(1,2))
            assert len(edges)==4*N and len(set(edges))==len(edges)
            deg=[0]*(3*N);balances=[[0]*N for _ in range(3*N)]
            for (tail,head),vals,agg in zip(edges,state_values,original_aggregates):
                deg[tail]+=1;deg[head]+=1
                assert sum(vals)==agg and all(0<=f<=weight for f in vals)
                for j,f in enumerate(vals):balances[tail][j]-=f;balances[head][j]+=f
            assert max(deg)==3
            for vertex,bb in enumerate(balances):assert bb==([-weight]*N if vertex==source else ([weight]*N if vertex==sink else [0]*N))
            checks+=1;lifted+=N
record={'status':'PASS','q_values':[3,4,5,6,7,8,9],'versions':['dense','sparse complement'],'exact_feasible_section_points':checks,'exact_infeasible_section_certificates':excluded,'simple_lift_state_flows':lifted,'checks':['integer incidence balances','invertibility','Fibonacci ratios','section witnesses','sparse observation counts','simple maximum degree three graph counts','all state and aggregate arc balances and capacities']}
Path(__file__).with_name('fibonacci-result.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
