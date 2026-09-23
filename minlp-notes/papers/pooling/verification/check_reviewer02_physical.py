"""Supplemental exact physical checks authored independently by stage-2 reviewer 02.

Retained from the reviewer temporary script for reproducibility. These finite
forward witnesses supplement the mathematical proof, including its reverse
directions. This file is not a general-purpose ETR instance converter.
"""
from fractions import Fraction as F
from collections import defaultdict

class Graph:
    def __init__(self):
        self.nodes={}; self.edges={}; self.pins={}; self.serial=0
    def node(self, kind, cap, marked=False, quality=0):
        self.serial+=1; name=f'{kind}{self.serial}'
        self.nodes[name]=(kind,F(cap),marked,quality); return name
    def arc(self,u,v,f):
        assert (u,v) not in self.edges
        assert (self.nodes[u][0],self.nodes[v][0]) in [('I','L'),('L','J'),('I','J')]
        self.edges[u,v]=F(f)
    def check(self,dim=1,maxout=None):
        incoming=defaultdict(list); outgoing=defaultdict(list)
        for (u,v),f in self.edges.items():
            assert f>=0
            incoming[v].append((u,f)); outgoing[u].append((v,f))
        q={u:([F(t)] if dim==1 else t) for u,(k,c,m,t) in self.nodes.items() if k=='I'}
        for u,(k,cap,marked,_) in self.nodes.items():
            total=sum(f for v,f in (outgoing[u] if k in ['I','L'] else incoming[u]))
            assert 0<=total<=cap,(u,total,cap)
            if marked: assert total==cap
            if k=='L':
                assert total==sum(f for v,f in incoming[u])
                q[u]=[sum(q[v][a]*f for v,f in incoming[u])/total if total else F(0) for a in range(dim)]
            assert k!='I' or len(outgoing[u])<=2
            assert k!='J' or len(incoming[u])<=2
            if maxout: assert len(outgoing[u])<=maxout
        for j,(kind,cap,marked,_) in self.nodes.items():
            if kind!='J': continue
            total=sum(f for v,f in incoming[j])
            for a in range(dim):
                mass=sum(q[v][a]*f for v,f in incoming[j])
                assert 0<=mass<=total
                if (j,a) in self.pins: assert mass==total*self.pins[j,a],(j,a,mass,total*self.pins[j,a])
        zeta=sum(c for k,c,m,_ in self.nodes.values() if m)
        profit=F(0)
        for (u,v),f in self.edges.items():
            ku,cu,mu,_=self.nodes[u];kv,cv,mv,_=self.nodes[v]
            count=int(mu and ku in ['I','L'])+int(mv and kv=='J')
            assert count<=2
            profit+=f*count
        assert profit==zeta
        return len(self.nodes),len(self.edges)

vals={'lo':F(1,2),'hi':F(2),'one':F(1),'a':F(3,4),'b':F(5,4),'c':F(3,2),'u':F(4,3),'unused':F(7,8)}
equations=[('inv','lo','hi'),('inv','one','one'),('inv','a','u'),('add','lo','lo','one'),('add','a','a','c'),('add','a','b','hi')]*13

def many(chain):
    g=Graph(); stores={}; scaled=[]
    def storage(a):
        p=g.node('L',0,True); stores[p]=a; return p
    def emit(p):
        a=stores[p]; t=g.node('J',2,True); h=g.node('L',2); r=g.node('I',2,True,0)
        g.arc(p,t,1/a);g.arc(r,h,2-1/a);g.arc(h,t,2-1/a);scaled.append((t,F(1,2)))
        return r,1/a
    def convert(r,d):
        h0=g.node('L',2);h1=g.node('L',2);t=g.node('J',2,True);r1=g.node('I',2,True,1)
        g.arc(r,h0,d);g.arc(h0,t,d);g.arc(r1,h1,2-d);g.arc(h1,t,2-d)
        return r1,d
    def link(p):
        r,d=convert(*emit(p));n=storage(d);g.arc(r,n,d);return n
    roots={}; types={}; positions={}; served=set()
    for v,a in vals.items():
        s=g.node('I',F(5,2),True,1)
        for bar,intake in [(False,a),(True,F(5,2)-a)]:
            p=storage(intake);g.arc(s,p,intake);roots[v,bar]=p
            r=link(p);types[v,bar,False]=p;types[v,bar,True]=r
            positions[v,bar]=(r,True)
    def get(v,bar,recip):
        if not chain:return types[v,bar,recip]
        p,t=positions[v,bar]
        if t!=recip:p=link(p);t=not t
        elif p in served:p=link(link(p))
        served.add(p);positions[v,bar]=(p,t);return p
    for eq in equations:
        if eq[0]=='inv':
            _,x,y=eq;r,d=emit(get(y,True,True));h=g.node('L',F(5,2));t=g.node('J',F(5,2),True)
            g.arc(r,h,d);g.arc(h,t,d);g.arc(get(x,False,False),t,vals[y]);scaled.append((t,F(2,5)))
        else:
            _,x,y,z=eq;h=g.node('L',4);t=g.node('J',F(5,2),True)
            for v in [x,y]:r,d=emit(get(v,False,True));g.arc(r,h,d)
            g.arc(h,t,vals[x]+vals[y]);g.arc(get(z,True,True),t,F(5,2)-vals[z]);scaled.append((t,F(2,5)))
    totals={p:sum(f for (u,v),f in g.edges.items() if u==p) for p in stores}
    M=max(sum(u==p for u,v in g.edges) for p in stores)
    B=F(7) if chain else F(2*M+3)
    for p,a in stores.items():
        g.nodes[p]=('L',B,True,0);d=g.node('I',B,False,0);s=g.node('J',B)
        g.arc(d,p,B-a);g.arc(p,s,B-totals[p]);assert B-totals[p]>=3
    for t,k in scaled:g.pins[t,0]=k/B
    assert all(sum(v==p for u,v in g.edges)<=2 for p in stores)
    n,e=g.check(maxout=3 if chain else None)
    print('chain' if chain else 'original', 'nodes',n,'arcs',e,'B',B,'max non-slack outlets',M)


def one():
    vv=dict(vals);eqs=[]
    for i,eq in enumerate(equations):
        if eq[0]=='add' and eq[1]==eq[2]:
            _,x,y,z=eq;u=f'fresh_u{i}';xx=f'fresh_x{i}';vv[u]=1/vv[x];vv[xx]=vv[x]
            eqs.extend([('inv',x,u),('inv',u,xx),('add',x,xx,z)])
        else:eqs.append(eq)
    auxiliaries=[];invvars=set();addattrs=[]
    for eq in eqs:
        if eq[0]=='inv':
            _,x,y=eq;h=len(auxiliaries);auxiliaries.extend([(vv[y],[('var',x,F(1,2))]),(1/vv[y],[('aux',h,F(1,2)),('var',y,F(1,2))])]);invvars.update([x,y])
        else:
            _,x,y,z=eq;a=len(addattrs);addattrs.append((x,y));auxiliaries.append((2/vv[z],[('var',z,F(1)),('add',a,F(1))]))
    for v in vv.keys()-invvars:auxiliaries.append((1/vv[v],[('var',v,F(1,2))]))
    N=len(vv)+len(auxiliaries);B=4*N;dim=N+len(addattrs);g=Graph();p=g.node('L',B,True)
    attrs={('var',v):i for i,v in enumerate(vv)}
    attrs.update({('aux',h):len(vv)+h for h in range(len(auxiliaries))})
    attrs.update({('add',i):N+i for i in range(len(addattrs))})
    for v,a in vv.items():
        q=[F(0)]*dim;q[attrs['var',v]]=1
        for j,(x,y) in enumerate(addattrs):q[N+j]=int(v in [x,y])
        s=g.node('I',2,False,q);g.arc(s,p,a)
    for h,(a,pins) in enumerate(auxiliaries):
        q=[F(0)]*dim;q[attrs['aux',h]]=1;s=g.node('I',2,True,q);j=g.node('J',2,True)
        g.arc(s,p,a);g.arc(s,j,2-a);g.arc(p,j,a)
        for typ,key,k in pins:g.pins[j,attrs[typ,key]]=k/B
    f=g.node('I',B,False,[F(0)]*dim);s=g.node('J',B)
    g.arc(f,p,B-sum(vv.values())-sum(a for a,pins in auxiliaries));g.arc(p,s,B-sum(a for a,pins in auxiliaries))
    n,e=g.check(dim=dim)
    print('one pool','nodes',n,'arcs',e,'attributes',dim,'B',B)

many(False);many(True);one()
