# pattern-theory critique check (2026-10-04). Run from a scratch dir holding copies of the inputs
# (pages.json, fetched.json, candidates.json, census_merged.json from research-20260929; OSIL from ~/.cache/minlplib).
import xml.etree.ElementTree as ET, sys
from collections import defaultdict
ns={'o':'os.optimizationservices.org'}
tag=lambda e:e.tag.split('}')[1]
def dec(el):
    out=[]
    for x in el:
        m=int(x.get('mult',1)); inc=x.get('incr'); v=int(x.text)
        out+= [v]*m if inc is None else [v+k*int(inc) for k in range(m)]
    return out
def build(fn, drop=set()):
    root=ET.parse(fn).getroot()
    G=defaultdict(set)
    def add(a,b):
        if a!=b: G[a].add(b); G[b].add(a)
    lin=root.find('.//o:linearConstraintCoefficients',ns); rowvars=defaultdict(set)
    if lin is not None:
        st=dec(lin.find('o:start',ns)); idxel=lin.find('o:rowIdx',ns); cm=idxel is not None
        if not cm: idxel=lin.find('o:colIdx',ns)
        idx=dec(idxel)
        for k in range(len(st)-1):
            for p in range(st[k],st[k+1]):
                (rowvars[idx[p]].add(k) if cm else rowvars[k].add(idx[p]))
    terms=defaultdict(list)
    q=root.find('.//o:quadraticCoefficients',ns)
    if q is not None:
        for t in q: terms[int(t.get('idx'))].append({int(t.get('idxOne')),int(t.get('idxTwo'))})
    vset=lambda e:{int(x.get('idx')) for x in e.iter() if tag(x)=='variable'}
    def split(e):
        t=tag(e); ch=list(e)
        if t=='sum': return [u for c in ch for u in split(c)]
        if t=='negate': return split(ch[0])
        return [e]
    for nl in root.findall('.//o:nonlinearExpressions/o:nl',ns):
        for tm in split(list(nl)[0]): terms[int(nl.get('idx'))].append(vset(tm))
    for c in root.find('.//o:objectives/o:obj',ns).findall('o:coef',ns): rowvars[-1].add(int(c.get('idx')))
    for r in set(rowvars)|set(terms):
        rn=('r',r)
        for v in rowvars[r]-drop: add(rn,('v',v))
        for i,s in enumerate(terms[r]):
            s=s-drop
            if len(s)==1: add(rn,('v',next(iter(s))))
            elif len(s)>1:
                tn=('t',r,i); add(rn,tn); [add(tn,('v',v)) for v in s]
    return G
def elim(G,rule):
    G={k:set(v) for k,v in G.items()}; w=0
    def fill(n):
        nb=list(G[n]); return sum(1 for i in range(len(nb)) for j in range(i+1,len(nb)) if nb[j] not in G[nb[i]])
    while G:
        n=min(G,key=(lambda k:len(G[k])) if rule=='deg' else (lambda k:(fill(k),len(G[k]))))
        nb=G.pop(n); w=max(w,len(nb))
        for a in nb: G[a].discard(n); G[a]|=(nb-{a})
    return w
fn=sys.argv[1]; drop=set(int(x) for x in sys.argv[2:])
G=build(fn,drop); print(fn, 'drop',drop,'min-degree',elim(G,'deg'),'min-fill',elim(G,'fill'))
