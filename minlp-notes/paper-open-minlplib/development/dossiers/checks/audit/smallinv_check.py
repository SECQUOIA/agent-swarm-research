from qosil_min import *
for inst,d in [('smallinvDAXr1b200-220','156.604269'),('smallinvDAXr2b200-220','156.604269'),('smallinvDAXr1b150-165','88.1049355')]:
    M=read(inst+'.osil'); 
    sol = inst+'.p2.sol'
    try: x=readsol(sol,M['V'])
    except FileNotFoundError: print('no sol',inst); continue
    print(inst,'n',len(M['V']),'rows',[ (c['name'],c['lb'],c['ub']) for c in M['C']], 'obj',M['oc'],M['sense'])
    print(' as listed violations:',[(a,b,float(c)) if len(t:=(a,b,c))==3 else (a,b) for (a,b,*c) in [(*v,) for v in violations(M,x)] for c in [c[0] if c else 0]])
    j=[i for i,v in enumerate(M['V']) if v['name']=='objvar'][0]
    # quadratic part of e1
    qv=sum(cf*x[a]*x[b] for a,b,cf in M['Q'][0]) + sum(c*x[jj] for jj,c in M['rows'][0].items() if jj!=j)
    x[j]=qv
    print(' objvar:=xQx =',qv, float(qv),' violations now:',violations(M,x))
    f=objval(M,x); D=Fraction(Decimal(d))
    print(' f =',f,'= ',float(f),' d-f =',D-f, float(D-f), 'rel',float((D-f)/D), ' max int', max(x[:30]))
