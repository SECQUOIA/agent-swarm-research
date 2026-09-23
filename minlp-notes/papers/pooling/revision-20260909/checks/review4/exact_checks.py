"""Independent rational checks of the printed gadgets; not a formal proof."""
from fractions import Fraction as F
from collections import defaultdict
import json

class Net:
    def __init__(self):
        self.nodes={}; self.arcs={}; self.counter=0; self.pins={}
    def node(self,kind,cap,quality=0,marked=False):
        self.counter+=1; name=f'{kind}{self.counter}'
        self.nodes[name]=[kind,F(cap),F(quality),marked]; return name
    def arc(self,u,v,f):
        assert (u,v) not in self.arcs
        self.arcs[u,v]=F(f)
    def verify(self):
        ins=defaultdict(F); outs=defaultdict(F); mass=defaultdict(F)
        for (u,v),f in self.arcs.items():
            assert f>=0
            assert (self.nodes[u][0],self.nodes[v][0]) in [('i','p'),('p','j')]
            outs[u]+=f; ins[v]+=f
        quality={u:d[2] for u,d in self.nodes.items() if d[0]=='i'}
        for u,(kind,cap,q,marked) in self.nodes.items():
            total=outs[u] if kind!='j' else ins[u]
            assert total<=cap,(u,total,cap)
            if marked: assert total==cap
            if kind=='p':
                assert ins[u]==outs[u]
                quality[u]=sum(self.arcs[a,b]*quality[a] for a,b in self.arcs if b==u)/ins[u] if ins[u] else F(0)
        for (u,v),f in self.arcs.items():
            if self.nodes[v][0]=='j': mass[v]+=quality[u]*f
        for u,(kind,cap,q,marked) in self.nodes.items():
            if kind=='j':
                assert 0<=mass[u]<=ins[u]
                if u in self.pins: assert mass[u]==self.pins[u]*ins[u]
        profit=F(0)
        for (u,v),f in self.arcs.items():
            cost=int(self.nodes[u][3])+int(self.nodes[v][0]=='j' and self.nodes[v][3])
            assert cost in (0,1,2)
            profit+=cost*f
        assert profit==sum(cap for kind,cap,q,marked in self.nodes.values() if marked)
        return profit

def many_pool(vals,eqs):
    n=Net(); storage=[]; emitted=[]; equation_products=[]; roots={}; B=101
    def store(src,a):
        q=n.node('p',B,marked=True); dil=n.node('i',B); slack=n.node('j',B)
        n.arc(src,q,a); storage.append((q,dil,slack,F(a))); return q
    def emit(q,a):
        r=n.node('i',2,marked=True); h=n.node('p',2); t=n.node('j',2,marked=True)
        n.arc(q,t,1/a); n.arc(r,h,2-1/a); n.arc(h,t,2-1/a); emitted.append(t)
        return r,1/a
    def flip(r,d):
        h0=n.node('p',2); h1=n.node('p',2); t=n.node('j',2,marked=True); r1=n.node('i',2,1,True)
        n.arc(r,h0,d); n.arc(h0,t,d); n.arc(r1,h1,2-d); n.arc(h1,t,2-d)
        return r1,d
    for v,a in vals.items():
        s=n.node('i',F(5,2),1,True)
        p=store(s,a); pb=store(s,F(5,2)-a)
        rs,ra=flip(*emit(p,a)); r=store(rs,ra)
        rbs,rba=flip(*emit(pb,F(5,2)-a)); rb=store(rbs,rba)
        roots[v]=(p,pb,r,rb)
    for op,x,y,z in eqs:
        t=n.node('j',F(5,2),marked=True); equation_products.append(t)
        if op=='inv':
            assert vals[x]*vals[y]==1
            r,d=emit(roots[y][3],1/(F(5,2)-vals[y])); h=n.node('p',F(5,2))
            n.arc(r,h,d); n.arc(h,t,d); n.arc(roots[x][0],t,vals[y])
        else:
            assert vals[x]+vals[y]==vals[z]
            h=n.node('p',4)
            for v in (x,y):
                r,d=emit(roots[v][2],1/vals[v]); n.arc(r,h,d)
            n.arc(h,t,vals[z]); n.arc(roots[z][3],t,F(5,2)-vals[z])
    M=max(sum(u==q for u,v in n.arcs) for q,dil,slack,a in storage)
    assert 1<=M<=2*len(eqs)+1
    B=2*M+3
    for q,dil,slack,a in storage:
        for u in (q,dil,slack): n.nodes[u][1]=F(B)
        n.arc(dil,q,B-a)
        leftover=B-sum(f for (u,v),f in n.arcs.items() if u==q)
        assert 3<=leftover<=B
        n.arc(q,slack,leftover)
    for t in emitted: n.pins[t]=F(1,2*B)
    for t in equation_products: n.pins[t]=F(2,5*B)
    profit=n.verify()
    for u,(kind,*_) in n.nodes.items():
        indeg=sum(v==u for s,v in n.arcs); outdeg=sum(s==u for s,v in n.arcs)
        if kind=='i': assert outdeg<=2
        if kind in ('p','j'): assert indeg<=2
        if kind=='p' and not n.nodes[u][3]: assert outdeg==1
    return dict(nodes=len(n.nodes),arcs=len(n.arcs),B=B,profit=str(profit))

def one_pool(vals,eqs):
    """Check every source/auxiliary attribute mass, including all unpinned bounds."""
    vals=dict(vals); eqs=list(eqs)
    for index,(op,x,y,z) in enumerate(list(eqs)):
        if op=='add' and x==y:
            u=f'inverse{index}'; xp=f'copy{index}'; vals[u]=1/vals[x]; vals[xp]=vals[x]
            eqs[index]=('add',x,xp,z); eqs.extend([('inv',x,u,None),('inv',u,xp,None)])
    tau={}; pins=[]; addition={}; inversions=set()
    def aux(a):
        h=f'aux{len(tau)}'; tau[h]=a; return h
    for index,(op,x,y,z) in enumerate(eqs):
        if op=='inv':
            inversions.update((x,y)); a=aux(vals[y]); b=aux(1/vals[y])
            pins.extend([(a,x,F(1)),(b,a,F(1)),(b,y,F(1))])
        else:
            assert x!=y
            a=aux(2/vals[z]); attribute=f'sum{index}'; addition[attribute]={x,y}
            pins.extend([(a,z,F(2)),(a,attribute,F(2))])
    for v in vals:
        if v not in inversions: pins.append((aux(1/vals[v]),v,F(1)))
    intakes={**vals,**tau}; N=len(intakes); B=4*N
    attributes={v:{v} for v in intakes}; attributes.update(addition)
    filler=B-sum(intakes.values()); slack=B-sum(tau.values())
    assert B/2<=filler<=B and B/2<=slack<=B
    assert sum(intakes.values())+filler==sum(tau.values())+slack==B
    for v,a in intakes.items(): assert F(1,2)<=a<=2
    qualities={k:sum(intakes[v] for v in support)/B for k,support in attributes.items()}
    for h,a in tau.items():
        assert 0<=2-a<=2
        for k,support in attributes.items():
            mass=qualities[k]*a+int(h in support)*(2-a)
            assert 0<=mass<=2
    for h,k,numerator in pins:
        assert h not in attributes[k]
        assert qualities[k]*tau[h]==numerator/B
    return dict(variables=len(vals),auxiliaries=len(tau),attributes=len(attributes),B=B,profit=B+4*len(tau))

cases=[]
for a in [F(1,2),F(2,3),F(3,4),F(1),F(4,3),F(3,2),F(2)]:
    vals={'x':a,'y':1/a,'u':F(1)}
    eq=[('inv','x','y',None),('inv','u','u',None)]
    cases.append((vals,eq))
for a,b in [(F(1,2),F(1,2)),(F(1,2),F(3,2)),(F(2,3),F(3,4)),(F(1),F(1))]:
    vals={'x':a,'y':b,'z':a+b,'u':F(1)}
    eq=[('add','x','y','z'),('inv','u','u',None)]
    if a==b: eq.append(('add','x','x','z'))
    cases.append((vals,eq))
# No equations, and many repeated uses stress the maximum outlet count.
cases.append(({'x':F(1,2),'y':F(2)},[]))
cases.append(({'x':F(1),'y':F(2)},[('add','x','x','y')]*15+[('inv','x','x',None)]*15))
results=[dict(many=many_pool(v,e),one=one_pool(v,e)) for v,e in cases]
# Cyclic near-singular example, including its exact residual.
for eps in [F(1,2),F(1,100),F(1,10**20)]:
    lam=F(3,7); q=lam+1
    assert q-(1-eps)*q-eps*lam==eps
    assert -q+q==0
# Cramer verifier has the claimed sign for either denominator sign.
for delta in [F(-3),F(-1,2),F(1,2),F(3)]:
    for A,U,b in [(F(2),F(3),F(1)),(F(-2),F(3),F(4)),(F(0),F(2),F(0))]:
        assert (A*U/delta<=b)==((A*U-b*delta)*delta<=0)
print(json.dumps({'passed_cases':len(cases),'results':results,'cyclic_residual':'passed','determinant_sign':'passed'},indent=2))
