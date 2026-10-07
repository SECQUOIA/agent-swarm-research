from qosil_min import *
import sys
def build(inst, pt, d):
    M=read(inst+'.osil'); V=M['V']; x=readsol(inst+'.'+pt+'.sol',V)
    xs=list(x)
    nb=0
    for i,v in enumerate(V):
        if v['type']=='B':
            r=round(x[i]); 
            if x[i]!=r: nb+=1
            x[i]=Fraction(r)
    # set continuous variables: utilisation u (in load rows), queue q (in quadratic rows)
    C=M['C']
    Uset=set(); 
    for k,c in enumerate(C):
        if not M['Q'][k] and c['lb']==c['ub'] and any(V[j]['type']=='C' for j in M['rows'][k]):
            us=[j for j in M['rows'][k] if V[j]['type']=='C']
            # link binaries for each u: find row u - b <= 0
            for j in us: Uset.add(j)
    link={}
    for k,c in enumerate(C):
        r=M['rows'][k]
        if not M['Q'][k] and len(r)==2 and any(V[j]['type']=='C' for j in r):
            u=[j for j in r if V[j]['type']=='C'][0]; b=[j for j in r if V[j]['type']=='B'][0]
            assert r[u]==1 and r[b]==-1 and c['ub']==0 and c['lb'] is None
            link[u]=b
    for k,c in enumerate(C):
        if not M['Q'][k] and c['lb']==c['ub'] and any(V[j]['type']=='C' for j in M['rows'][k]):
            r=M['rows'][k]; us=[j for j in r if V[j]['type']=='C']
            for j in us:
                if x[link[j]]==0: x[j]=Fraction(0)
            on=[j for j in us if x[link[j]]==1]
            assert len(on)<=1, on
            rest=sum(cf*x[j] for j,cf in r.items() if V[j]['type']=='B')+c['const']
            if on:
                j=on[0]; x[j]=(c['lb']-rest)/r[j]
            else:
                assert rest==c['lb']
    for k,c in enumerate(C):
        if M['Q'][k]:
            terms=M['Q'][k]
            # -b*q + b*u + q*u <= 0
            vs={a for a,b,_ in terms}|{b for a,b,_ in terms}
            b=[j for j in vs if V[j]['type']=='B'][0]; cont=[j for j in vs if V[j]['type']=='C']
            u=[j for j in cont if j in Uset][0]; q=[j for j in cont if j!=u][0]
            if x[b]==1: x[q]=x[u]/(1-x[u])
            else: x[q]=Fraction(0)
    viol=violations(M,x); f=objval(M,x); D=Fraction(Decimal(d))
    mv=max(abs(a-b) for a,b in zip(x,xs))
    print(inst,pt,'nonint binaries',nb,'violations',viol,'f=',float(f),'(',str(Fraction(f).limit_denominator(1)) ,') d-f=',float(D-f),'rel',float((D-f)/abs(D)),'max move',float(mv))
    return f
build('sssd25-08persp','p4','472098.947')
build('sssd25-08persp','p3','472098.947')
build('sssd22-08persp','p4','508748.972')
